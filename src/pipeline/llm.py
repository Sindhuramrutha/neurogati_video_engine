"""The model client — the one place this pipeline talks to a provider.

Two entry points, and the difference between them is the whole argument:

- `complete_text` returns prose, for an agent answering a question.
- `complete_structured` returns a **validated Pydantic model**, for an agent
  producing an artifact.
- `complete_scene` is one round of making a scene, as plain text, with hidden
  reasoning off and a time limit (a reasoning model once spent 70 minutes thinking
  and wrote nothing). A cut-off reply is `ModelOutputTruncated`.

Free text parsed with regexes means a model that phrases its answer differently
crashes three stages later, in a component that has nothing to do with the
mistake. A malformed response fails inside `complete_structured`, next to the
call that caused it, and is retried against the schema rather than repaired by
hand.

Timeout and retries are set explicitly, not left to defaults, because with
defaults a dropped connection surfaces as a failed scene with no code
generated -- minutes of work lost, with no error that names the cause.
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
# A vision model thinks before it answers, and the thinking counts against this.
VISION_TOKENS = 16000
PROGRAM_CALL_SECONDS = 600       # a scene agent's turn; it is asked to skip hidden reasoning
NO_HIDDEN_REASONING = {"thinking": {"type": "disabled"}}


class ModelNotConfigured(Exception):
    """No API key is set.

    Its own type because it is the one failure with an obvious fix, and every
    interface should be able to say so precisely: open the API keys panel, or run
    `pipeline credentials set LLM_API_KEY`.
    """


class ModelCallFailed(Exception):
    """The provider was reachable but the call did not produce a usable answer."""


class ModelOutputTruncated(ModelCallFailed):
    """The answer stopped at the token limit, so it is not the whole answer."""

    transient = False          # asking the same way again stops at the same place


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
    import httpx
    from openai import OpenAI

    from pipeline.llm_pace import notice, take_a_place

    if not api_key or api_key == "not-needed":
        raise ModelNotConfigured(
            f"No API key set, so the {purpose} model cannot be reached. Add one in the API "
            f"keys panel, or run: echo -n '<key>' | pipeline credentials set LLM_API_KEY")
    settings = get_settings()
    # Every request -- retries and re-asks included -- waits for a place in the
    # provider's per-minute limit (llm_pace.py) instead of being refused.
    paced = httpx.Client(event_hooks={"request": [lambda _request: take_a_place()],
                                      "response": [notice]})
    return OpenAI(base_url=base_url, api_key=api_key, http_client=paced,
                  timeout=settings.llm_timeout_seconds, max_retries=settings.llm_max_retries)


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


def _chat(
    endpoint: tuple[str, str, str], purpose: str, messages: list[dict[str, Any]],
    max_tokens: int, *, program: bool = False,
) -> tuple[str, dict[str, int]]:
    """One chat completion with the failure vocabulary above: the answer's text, and
    what it used (hidden reasoning included).

    Every free-text call goes through here, so a provider error is described the
    same way whether the question was words, a picture or a program. A `program`
    call has a time limit, asks for no hidden reasoning (again without the switch
    if the provider refuses it), and fails when cut off at the token limit.
    """
    import openai

    base_url, api_key, model_name = endpoint
    client = _build_client(base_url, api_key, purpose)
    if program:
        client = client.with_options(timeout=PROGRAM_CALL_SECONDS)
    ask = {"model": model_name, "max_tokens": max_tokens, "messages": messages}

    try:
        try:
            response = client.chat.completions.create(
                **ask, **({"extra_body": NO_HIDDEN_REASONING} if program else {}))
        except openai.BadRequestError:
            if not program:
                raise
            response = client.chat.completions.create(**ask)
    except Exception as call_failure:
        logger.exception("%s completion failed", purpose)
        raise ModelCallFailed(
            _what_went_wrong(call_failure)
            or f"{type(call_failure).__name__}: {call_failure}"
        ) from call_failure

    usage = getattr(response, "usage", None)
    details = getattr(usage, "completion_tokens_details", None)
    used = {"prompt": getattr(usage, "prompt_tokens", 0) or 0,
            "completion": getattr(usage, "completion_tokens", 0) or 0,
            "reasoning": getattr(details, "reasoning_tokens", 0) or 0}
    choices = getattr(response, "choices", None)
    if not choices:
        raise ModelCallFailed(f"{model_name} returned no answer.")
    if program and choices[0].finish_reason == "length":
        raise ModelOutputTruncated(
            f"The answer was cut off at the token limit ({used['completion']} tokens, "
            f"{used['reasoning']} of them hidden reasoning).")
    return (choices[0].message.content or "").strip(), used


def complete_text(system_prompt: str, user_prompt: str, *, max_tokens: int = 2000) -> str:
    """Ask for prose. Used where the answer is for a person to read.

    Deliberately not used to produce an artifact: see the module note.
    """
    settings = get_settings()
    return _chat(
        (settings.llm_base_url, settings.llm_api_key, settings.llm_model), "text",
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens,
    )[0]


def complete_scene(system_prompt: str, user_prompt: str, *,
                   max_tokens: int) -> tuple[str, dict[str, int]]:
    """One round of making a scene, as plain text, and what it used."""
    return _chat(get_settings().ir_llm, "scene",
                 [{"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_prompt}],
                 max_tokens, program=True)


def _structured[ModelType: BaseModel](
    endpoint: tuple[str, str, str], purpose: str, response_model: type[ModelType],
    messages: list[dict[str, Any]], max_tokens: int,
) -> ModelType:
    """One schema-checked completion, re-asked on a misfit, failing here if not.

    instructor re-asks the model with the validation errors attached when the
    first attempt does not fit the schema. That retry is the point: the failure
    is corrected against the schema by the thing that produced it, instead of
    being patched downstream by a human reading a traceback.
    """
    import instructor

    base_url, api_key, model_name = endpoint
    # JSON mode rather than instructor's default forced tool-calling. Reasoning
    # models reject `tool_choice: required` -- TokenRouter's deepseek-v4-flash
    # answers a structured request with
    #   "The tool_choice parameter does not support being set to required or
    #    object in thinking mode"
    # and no amount of retrying fixes it, because the request shape is the
    # problem. JSON mode asks for a JSON object and validates it against the
    # schema, which every OpenAI-compatible provider supports.
    client = instructor.from_openai(
        _build_client(base_url, api_key, purpose), mode=instructor.Mode.JSON)

    try:
        return client.chat.completions.create(
            model=model_name,
            max_tokens=max_tokens,
            max_retries=MAXIMUM_SCHEMA_RETRIES,
            response_model=response_model,
            messages=messages,
        )
    except ModelNotConfigured:
        raise
    except Exception as call_failure:
        logger.exception("%s completion failed", purpose)
        raise ModelCallFailed(
            _what_went_wrong(call_failure)
            or f"The model did not return a valid {response_model.__name__} after "
               f"{MAXIMUM_SCHEMA_RETRIES} retries: {type(call_failure).__name__}: {call_failure}"
        ) from call_failure


def complete_structured[ModelType: BaseModel](
    response_model: type[ModelType],
    system_prompt: str,
    user_prompt: str,
    *,
    max_tokens: int = STRUCTURED_OUTPUT_TOKEN_BUDGET,
) -> ModelType:
    """Ask for an object that satisfies `response_model`, or fail here."""
    return _structured(
        get_settings().ir_llm, "structured-output", response_model,
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens,
    )


def complete_structured_with_images[ModelType: BaseModel](
    response_model: type[ModelType],
    system_prompt: str,
    user_prompt: str,
    pictures: list[tuple[str, bytes]],
    *,
    max_tokens: int = STRUCTURED_OUTPUT_TOKEN_BUDGET,
) -> ModelType:
    """The same, from the vision model, with pictures to look at.

    `pictures` are (label, JPEG bytes); each label is sent as text just before
    its picture, so the model can say which one it means.
    """
    import base64

    content: list[dict[str, Any]] = [{"type": "text", "text": user_prompt}]
    for label, picture in pictures:
        encoded = base64.b64encode(picture).decode("ascii")
        content.append({"type": "text", "text": label})
        content.append({"type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}})
    return _structured(
        get_settings().vision_llm, "vision", response_model,
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
        max_tokens,
    )


def picture_in_reply(message: Any) -> bytes:
    """The picture an image model put in its chat reply, or empty bytes.

    Gemini's image models, as TokenRouter serves them, answer a chat request with
    the picture embedded in the text as `![image](data:image/png;base64,...)`;
    OpenRouter-style providers attach it as `images[0].image_url.url`. Both are
    read here, so the caller does not care which it got.
    """
    import base64
    import re

    candidates: list[str] = []
    extra = getattr(message, "model_extra", None) or {}
    for image in extra.get("images") or []:
        url = (image.get("image_url") or {}).get("url", "") if isinstance(image, dict) else ""
        candidates.append(url)
    candidates.append(getattr(message, "content", "") or "")

    for text in candidates:
        found = re.search(r"data:image/[a-zA-Z+.-]+;base64,([A-Za-z0-9+/=\s]+)", text)
        if found:
            return base64.b64decode(re.sub(r"\s", "", found.group(1)))
    return b""


def _picture_from_chat(content: Any, purpose: str) -> bytes:
    """Ask the image model for a picture through the chat endpoint.

    The way Gemini image models are served: the picture comes back in the reply.
    Returns empty bytes when the reply has none, so a caller can try the image
    endpoint instead for a provider that uses that.
    """
    base_url, api_key, model_name = get_settings().image_llm
    client = _build_client(base_url, api_key, "images")
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": content}],
            extra_body={"modalities": ["image", "text"]},
        )
    except Exception as call_failure:
        logger.exception("%s failed", purpose)
        raise ModelCallFailed(
            _what_went_wrong(call_failure)
            or f"{model_name} could not make the picture: "
               f"{type(call_failure).__name__}: {call_failure}"
        ) from call_failure
    choices = getattr(response, "choices", None) or []
    return picture_in_reply(choices[0].message) if choices else b""


def draw_image(prompt: str, *, size: str = "1024x1024") -> bytes:
    """Ask the image model for a picture, and return the bytes.

    Deliberately here beside the text calls: it is the same providers, the same
    key handling and the same failure vocabulary, and a second module for one
    endpoint would drift from this one the first time a timeout changed.

    Through the chat endpoint first, which is how the configured Gemini image
    model answers; the dedicated image endpoint only when the reply carried no
    picture. That endpoint alone answered "model not found" for Gemini.
    """
    import base64

    picture = _picture_from_chat(prompt, "image generation")
    if picture:
        return picture

    base_url, api_key, model_name = get_settings().image_llm
    client = _build_client(base_url, api_key, "images")
    try:
        response = client.images.generate(model=model_name, prompt=prompt, size=size, n=1)
    except Exception as call_failure:
        logger.exception("image generation failed")
        raise ModelCallFailed(
            f"{model_name} returned no picture in its reply, and its image endpoint "
            f"failed too: {_what_went_wrong(call_failure) or call_failure}"
        ) from call_failure
    data = getattr(response, "data", None) or []
    encoded = getattr(data[0], "b64_json", "") if data else ""
    if not encoded:
        raise ModelCallFailed(f"{model_name} returned no image. It may not be an image model.")
    return base64.b64decode(encoded)


def edit_image(image_bytes: bytes, mime_type: str, instruction: str) -> bytes:
    """Ask the image model to change an existing picture, and return the result.

    The picture itself goes with the instruction, so a crop, a recolour or a
    removed element keeps the rest of the original -- which redrawing from a
    description cannot.
    """
    import base64

    encoded = base64.b64encode(image_bytes).decode("ascii")
    picture = _picture_from_chat([
        {"type": "text", "text": f"Edit this picture: {instruction}. Return the edited picture."},
        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{encoded}"}},
    ], "image edit")
    if not picture:
        raise ModelCallFailed(
            f"{get_settings().image_llm[2]} did not return an edited picture.")
    return picture


def read_image_text(image_bytes: bytes, mime_type: str, instruction: str) -> str:
    """Ask the vision model what text a picture contains. Returns it as written.

    The one call that sends pixels rather than words: a handwritten or scanned
    page has no text layer for a parser to read, so the only reader available is
    a model that can see. The caller records the result as transcribed, never as
    text the file contained.
    """
    import base64

    encoded = base64.b64encode(image_bytes).decode("ascii")
    return _chat(
        get_settings().vision_llm, "vision",
        [{"role": "user", "content": [
            {"type": "text", "text": instruction},
            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{encoded}"}},
        ]}],
        4000,
    )[0]
