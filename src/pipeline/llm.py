"""The model client — the one place this pipeline talks to a provider.

Two entry points, and the difference between them is the whole argument of
[ADR 0002](../../docs/decisions/0002-structured-output-over-free-text.md):

- `complete_text` returns prose, for an agent answering a question.
- `complete_structured` returns a **validated Pydantic model**, for an agent
  producing an artifact.

v1 asked for free text and then parsed it with regexes, so a model that phrased
its answer differently produced a crash three stages later, in a component that
had nothing to do with the mistake. Here a malformed response fails inside
`complete_structured`, next to the call that caused it, and is retried against
the schema rather than repaired by hand.

Timeout and retries are set explicitly, not left to defaults, because v1 left
them unset and a dropped connection surfaced as a failed scene with no code
generated -- minutes of work lost per scene, with no error that named the cause.
Both come from `config.Settings`, so changing them is configuration.

**No key is read here.** Credentials come from `get_settings()`, which resolves
them from the environment and `.env`. Nothing in this module accepts a key as an
argument, so no caller -- including an agent -- is ever in a position to pass one
in or read one out.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel

from pipeline.config import get_settings

logger = logging.getLogger(__name__)

# Retries here are instructor re-asking the model when its output does not fit
# the schema -- a different failure from the transport retries the OpenAI client
# does, which are configured separately in Settings.
MAXIMUM_SCHEMA_RETRIES = 2

# Generous because reasoning models spend the budget twice: once on hidden
# thinking tokens and once on the answer. At 4000 a 225-word narration failed
# with IncompleteOutputException -- the model had reasoned its way past the limit
# before emitting any JSON, so retrying could not help and the section silently
# went unwritten. The cost of a high ceiling is nothing when the response is
# short; the cost of a low one is a stage that fails on its longest sections.
STRUCTURED_OUTPUT_TOKEN_BUDGET = 16000


class ModelNotConfigured(Exception):
    """No API key is set.

    Its own type because it is the one failure with an obvious fix, and every
    interface should be able to say so precisely: open the API keys panel, or run
    `pipeline credentials set LLM_API_KEY`.
    """


class ModelCallFailed(Exception):
    """The provider was reachable but the call did not produce a usable answer."""


def is_configured() -> bool:
    """Whether a real key is present.

    Checked before offering to run an agent, so the interface can say "no key
    set" up front rather than after a request that was never going to work.
    """
    settings = get_settings()
    return bool(settings.llm_api_key) and settings.llm_api_key != "not-needed"


def describe_model() -> dict[str, Any]:
    """What a call would use right now. Never includes the key."""
    settings = get_settings()
    ir_base_url, _, ir_model = settings.ir_llm
    return {
        "is_configured": is_configured(),
        "text_model": settings.llm_model,
        "text_base_url": settings.llm_base_url,
        "structured_model": ir_model,
        "structured_base_url": ir_base_url,
        "timeout_seconds": settings.llm_timeout_seconds,
        "max_retries": settings.llm_max_retries,
    }


def _build_client(base_url: str, api_key: str, purpose: str):
    from openai import OpenAI

    if not api_key or api_key == "not-needed":
        raise ModelNotConfigured(
            f"No API key set, so the {purpose} model cannot be reached. "
            f"Add one in the API keys panel, or run: "
            f"echo -n '<key>' | pipeline credentials set LLM_API_KEY"
        )

    settings = get_settings()
    return OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=settings.llm_timeout_seconds,
        max_retries=settings.llm_max_retries,
    )


def _what_went_wrong(call_failure: Exception) -> str:
    """Name the cause when it is not the model's answer.

    A dropped connection surfaced as "The model did not return a valid
    OrchestratorTurn after 2 retries: InstructorRetryException: Connection
    error." -- which blames the model and the schema for a network problem and
    tells the reader nothing they can act on. The retry wrappers bury the real
    error in the cause chain, so it is looked for there.
    """
    import openai

    causes: list[BaseException] = []
    seen: set[int] = set()
    cause: BaseException | None = call_failure
    while cause is not None and id(cause) not in seen:
        seen.add(id(cause))
        causes.append(cause)
        cause = cause.__cause__ or cause.__context__

    for cause in causes:
        if isinstance(cause, openai.AuthenticationError | openai.PermissionDeniedError):
            return ("The model provider rejected the API key. Check it in the API keys "
                    "panel.")
        if isinstance(cause, openai.RateLimitError):
            return ("The model provider is rate limiting these requests. Wait a moment "
                    "and try again.")
        if isinstance(cause, openai.APITimeoutError):
            return ("The model provider did not answer in time. Try again; if it keeps "
                    "happening the model may be overloaded.")
        if isinstance(cause, openai.APIConnectionError):
            return ("Could not reach the model provider. Check your internet connection "
                    "and try again.")
    if any("Connection error" in str(cause) for cause in causes):
        return ("Could not reach the model provider. Check your internet connection and "
                "try again.")
    return ""


def complete_text(system_prompt: str, user_prompt: str, *, max_tokens: int = 2000) -> str:
    """Ask for prose. Used where the answer is for a person to read.

    Deliberately not used to produce an artifact: see the module note.
    """
    settings = get_settings()
    client = _build_client(settings.llm_base_url, settings.llm_api_key, "text")

    try:
        response = client.chat.completions.create(
            model=settings.llm_model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except Exception as call_failure:
        logger.exception("text completion failed")
        raise ModelCallFailed(
            _what_went_wrong(call_failure)
            or f"{type(call_failure).__name__}: {call_failure}"
        ) from call_failure

    choices = getattr(response, "choices", None)
    if not choices:
        raise ModelCallFailed("The provider returned no choices.")

    return (choices[0].message.content or "").strip()


def complete_structured[ModelType: BaseModel](
    response_model: type[ModelType],
    system_prompt: str,
    user_prompt: str,
    *,
    max_tokens: int = STRUCTURED_OUTPUT_TOKEN_BUDGET,
) -> ModelType:
    """Ask for an object that satisfies `response_model`, or fail here.

    instructor re-asks the model with the validation errors attached when the
    first attempt does not fit the schema. That retry is the point: the failure
    is corrected against the schema by the thing that produced it, instead of
    being patched downstream by a human reading a traceback.
    """
    import instructor

    settings = get_settings()
    base_url, api_key, model_name = settings.ir_llm

    # JSON mode rather than instructor's default forced tool-calling. Reasoning
    # models reject `tool_choice: required` -- TokenRouter's deepseek-v4-flash
    # answers a structured request with
    #   "The tool_choice parameter does not support being set to required or
    #    object in thinking mode"
    # and no amount of retrying fixes it, because the request shape is the
    # problem. JSON mode asks for a JSON object and validates it against the
    # schema, which every OpenAI-compatible provider supports.
    client = instructor.from_openai(
        _build_client(base_url, api_key, "structured-output"),
        mode=instructor.Mode.JSON,
    )

    try:
        return client.chat.completions.create(
            model=model_name,
            max_tokens=max_tokens,
            max_retries=MAXIMUM_SCHEMA_RETRIES,
            response_model=response_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except ModelNotConfigured:
        raise
    except Exception as call_failure:
        logger.exception("structured completion failed")
        raise ModelCallFailed(
            _what_went_wrong(call_failure)
            or f"The model did not return a valid {response_model.__name__} after "
               f"{MAXIMUM_SCHEMA_RETRIES} retries: {type(call_failure).__name__}: {call_failure}"
        ) from call_failure
