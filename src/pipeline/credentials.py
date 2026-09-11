"""API credentials — declared once, stored in `.env`, never returned to the browser.

The agents need a provider key. There are only two places it can live, and one of
them is wrong: in the browser, where it is readable by anyone with devtools and
travels in every page load; or on the server, where the process that actually
makes the call is the only thing that sees it. This module is the second.

**The invariant that matters: a secret value leaves this module in exactly one
direction.** `describe_credentials()` returns a mask and a status, never the
value. The only code that gets the real thing is `config.get_settings()`, which
runs server-side and hands it to the provider client. There is no route, and no
shape of response, that carries a key back to the page.

Values are written to `.env` at the repository root -- the same file
`config.Settings` already reads, so setting a key here and restarting is
indistinguishable from having typed it into the file by hand. `.env` is
gitignored, and `is_env_file_ignored()` reports whether that is still true
rather than assuming it.

One sharp edge is surfaced rather than hidden: a real environment variable beats
`.env` in pydantic-settings' precedence order. Someone with `LLM_API_KEY` exported
in their shell would save a new key here, see it stored, and watch the old one
keep being used. Those fields report `source: "environment"` and the UI says so.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from pipeline.config import REPO_ROOT, get_settings
from pipeline.storage.documents import write_text_atomically

logger = logging.getLogger(__name__)

ENVIRONMENT_FILE_PATH = REPO_ROOT / ".env"

# Long enough for any real key, short enough that nobody pastes a file in.
MAXIMUM_CREDENTIAL_LENGTH = 500

# Below this, a "last four characters" hint would give away most of a short
# secret, so the mask shows nothing at all.
MINIMUM_LENGTH_TO_REVEAL_A_SUFFIX = 12


@dataclass(frozen=True)
class CredentialField:
    """One setting the panel can edit.

    Declared here and rendered generically by the UI, the same way stage options
    are: adding a provider is one entry in `CREDENTIAL_FIELDS`, with no template
    change and no new route.
    """

    environment_variable_name: str
    label: str
    help_text: str
    # Secrets are masked on the way out. Non-secrets (a base URL, a model name)
    # are shown in full, because hiding them helps nobody and makes the panel
    # impossible to check at a glance.
    is_secret: bool
    placeholder: str = ""
    group: str = ""


CREDENTIAL_FIELDS: tuple[CredentialField, ...] = (
    CredentialField(
        "LLM_API_KEY",
        "API key",
        "Used by every agent unless the structured-output provider below overrides it.",
        is_secret=True,
        placeholder="sk-...",
        group="Text model",
    ),
    CredentialField(
        "LLM_BASE_URL",
        "Base URL",
        "Any OpenAI-compatible endpoint. Defaults to TokenRouter.",
        is_secret=False,
        placeholder="https://api.tokenrouter.com/v1",
        group="Text model",
    ),
    CredentialField(
        "LLM_MODEL",
        "Model",
        "Model identifier as the provider spells it.",
        is_secret=False,
        placeholder="deepseek/deepseek-v4-flash",
        group="Text model",
    ),
    CredentialField(
        "IR_LLM_API_KEY",
        "API key",
        "Leave empty to reuse the text model's key.",
        is_secret=True,
        placeholder="reuses the text model's key",
        group="Structured output",
    ),
    CredentialField(
        "IR_LLM_BASE_URL",
        "Base URL",
        "Leave empty to reuse the text model's endpoint.",
        is_secret=False,
        placeholder="reuses the text model's endpoint",
        group="Structured output",
    ),
    CredentialField(
        "IR_LLM_MODEL",
        "Model",
        "A stricter model is often worth it here; leave empty to reuse the text model.",
        is_secret=False,
        placeholder="reuses the text model",
        group="Structured output",
    ),
)

FIELDS_BY_NAME: dict[str, CredentialField] = {
    field.environment_variable_name: field for field in CREDENTIAL_FIELDS
}


def mask_secret(value: str) -> str:
    """A mask that proves which key is stored without revealing it.

    Showing the last four characters is enough to tell two keys apart when
    rotating one, and is the convention every provider dashboard uses. Anything
    shorter than `MINIMUM_LENGTH_TO_REVEAL_A_SUFFIX` reveals nothing, because on
    a short secret four characters is a meaningful fraction of it.
    """
    if not value:
        return ""
    if len(value) < MINIMUM_LENGTH_TO_REVEAL_A_SUFFIX:
        return "•" * 8
    return "•" * 8 + value[-4:]


def parse_environment_file(text: str) -> dict[str, str]:
    """Read `KEY=value` pairs, ignoring comments and blanks.

    Deliberately not a full dotenv implementation: no interpolation, no `export`
    prefixes, no multi-line values. This file is written by the panel and read by
    pydantic-settings, and a parser that quietly accepts more than it round-trips
    is how a value gets mangled on save.
    """
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[name.strip()] = value
    return values


def read_environment_file() -> dict[str, str]:
    if not ENVIRONMENT_FILE_PATH.exists():
        return {}
    try:
        return parse_environment_file(ENVIRONMENT_FILE_PATH.read_text(encoding="utf-8"))
    except OSError as read_failure:
        # Same posture as every document store: report it, do not destroy it.
        logger.error("could not read %s: %s", ENVIRONMENT_FILE_PATH, read_failure)
        return {}


def needs_quoting(value: str) -> bool:
    return value != value.strip() or any(character in value for character in " #\"'")


def render_environment_file(values: dict[str, str]) -> str:
    """Rebuild `.env` from scratch, grouped and commented.

    Rewriting rather than patching in place means the file always has one shape,
    so a hand-edit and a panel-save cannot leave it half in one style. The cost
    is that hand-written comments are not preserved, which the header says
    plainly so nobody loses notes without warning.
    """
    lines = [
        "# Written by the Explainer Pipeline API-keys panel.",
        "# Hand edits are kept, but comments and ordering are rewritten on save.",
        "# This file is gitignored. Never commit it.",
    ]

    for group in dict.fromkeys(field.group for field in CREDENTIAL_FIELDS):
        group_fields = [
            field for field in CREDENTIAL_FIELDS
            if field.group == group and values.get(field.environment_variable_name)
        ]
        if not group_fields:
            continue
        lines.append("")
        lines.append(f"# --- {group} ---")
        for field in group_fields:
            name = field.environment_variable_name
            value = values[name]
            lines.append(f'{name}="{value}"' if needs_quoting(value) else f"{name}={value}")

    # Anything the panel does not manage stays exactly as it was found.
    unmanaged = {
        name: value for name, value in values.items()
        if name not in FIELDS_BY_NAME and value
    }
    if unmanaged:
        lines.append("")
        lines.append("# --- other settings (not managed by the panel) ---")
        for name in sorted(unmanaged):
            value = unmanaged[name]
            lines.append(f'{name}="{value}"' if needs_quoting(value) else f"{name}={value}")

    return "\n".join(lines) + "\n"


def describe_credentials() -> dict:
    """Status of every field, with secrets masked.

    This is the *only* function the API layer may expose. It returns whether a
    value is set, a mask, and where it came from -- never the value itself.
    """
    stored = read_environment_file()
    fields: list[dict] = []
    shadowed_by_environment: list[str] = []

    for field in CREDENTIAL_FIELDS:
        name = field.environment_variable_name
        from_real_environment = os.environ.get(name)
        from_file = stored.get(name)

        # pydantic-settings resolves a real environment variable ahead of .env,
        # so report the value that will actually be used, not the one on disk.
        if from_real_environment:
            effective, source = from_real_environment, "environment"
            if from_file and from_file != from_real_environment:
                shadowed_by_environment.append(name)
        elif from_file:
            effective, source = from_file, "file"
        else:
            effective, source = "", "unset"

        fields.append({
            "name": name,
            "label": field.label,
            "help": field.help_text,
            "group": field.group,
            "is_secret": field.is_secret,
            "placeholder": field.placeholder,
            "is_set": bool(effective),
            "source": source,
            # A secret is reduced to a mask here and nowhere else.
            "display_value": mask_secret(effective) if field.is_secret else effective,
            "is_editable": source != "environment",
        })

    warnings: list[str] = []
    if shadowed_by_environment:
        warnings.append(
            f"{', '.join(shadowed_by_environment)} is set in your shell environment, "
            f"which overrides this panel. Unset it there, or edit it there instead."
        )
    if not any(f["is_set"] for f in fields if f["name"] == "LLM_API_KEY"):
        warnings.append("No API key set — agents cannot reach a model.")

    return {
        "fields": fields,
        "warnings": warnings,
        "environment_file": str(ENVIRONMENT_FILE_PATH),
        "is_gitignored": is_env_file_ignored(),
    }


def save_credentials(submitted: dict[str, str]) -> dict:
    """Merge submitted values into `.env` and report the new status.

    An empty string clears a field. A field absent from `submitted` is left
    alone, so the panel can save one group without resending the others -- and,
    more importantly, so a masked value the browser never received cannot be
    written back over the real one.
    """
    stored = read_environment_file()

    for name, raw_value in submitted.items():
        field = FIELDS_BY_NAME.get(name)
        if field is None:
            logger.warning("ignoring unknown credential field %r", name)
            continue

        value = str(raw_value).strip()[:MAXIMUM_CREDENTIAL_LENGTH]
        if value:
            stored[name] = value
        else:
            stored.pop(name, None)

    write_text_atomically(ENVIRONMENT_FILE_PATH, render_environment_file(stored))

    # Settings are cached for the process lifetime; without this the app would
    # keep using the previous key until someone restarted it, and the panel
    # would look like it had silently failed.
    get_settings.cache_clear()

    logger.info("credentials updated: %s", ", ".join(sorted(submitted)) or "(none)")
    return describe_credentials()


def is_env_file_ignored() -> bool:
    """Whether git would ignore `.env`.

    Read from `.gitignore` directly rather than shelling out to git: this is
    called on every panel open, and the answer must not depend on git being
    installed or the directory being a repository.
    """
    gitignore_path = REPO_ROOT / ".gitignore"
    if not gitignore_path.exists():
        return False
    try:
        patterns = gitignore_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return False
    return any(line.strip() in {".env", "*.env", ".env*"} for line in patterns)
