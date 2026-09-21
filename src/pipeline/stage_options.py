"""Per-stage options — declared once, rendered generically.

An option is defined here and the UI builds its control from the declaration. That
means adding an option is a single entry in this file rather than a change to the
backend, the frontend, and the storage layer independently, which is how the three
end up disagreeing about what a setting means.

Options are *inputs* to a stage, not outputs, so they are stored outside the stage
directory: `projects/<slug>/settings/<stage>.json`. Putting them inside would make
`stage_state` report a stage as "ready" the moment someone changed a toggle,
because readiness is "this directory has content".
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from pipeline.stages import Stage
from pipeline.storage.documents import read_json_object, write_text_atomically

logger = logging.getLogger(__name__)


class OptionKind(StrEnum):
    CHOICE = "choice"
    TOGGLE = "toggle"


@dataclass(frozen=True)
class OptionChoice:
    value: str
    label: str
    help_text: str = ""


@dataclass(frozen=True)
class StageOption:
    key: str
    kind: OptionKind
    label: str
    default: Any
    help_text: str = ""
    choices: tuple[OptionChoice, ...] = ()
    # False for an option nothing reads yet. It is still declared, so the page
    # can show what is planned -- but marked, and not operable, because a
    # control that saves a value and changes nothing is indistinguishable from a
    # broken one. Every option on the Extraction and Planning pages was exactly
    # that until the first two below were wired in.
    implemented: bool = True

    def coerce(self, raw_value: Any) -> Any:
        """Force a stored or submitted value into a valid one.

        Settings files are hand-editable and survive schema changes, so a value
        can legitimately be missing, the wrong type, or a choice that no longer
        exists. Falling back to the default keeps a stale file from breaking the
        stage; the alternative is a 500 on a page someone can only fix by
        deleting a file they cannot see.
        """
        if self.kind is OptionKind.TOGGLE:
            return bool(raw_value)
        valid_values = {choice.value for choice in self.choices}
        return raw_value if raw_value in valid_values else self.default

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "kind": self.kind.value,
            "label": self.label,
            "default": self.default,
            "help_text": self.help_text,
            "implemented": self.implemented,
            "choices": [
                {"value": c.value, "label": c.label, "help_text": c.help_text}
                for c in self.choices
            ],
        }


EXTRACTION_OPTIONS: tuple[StageOption, ...] = (
    StageOption(
        key="extraction_mode",
        kind=OptionKind.CHOICE,
        label="Extraction mode",
        default="balanced",
        choices=(
            OptionChoice("fast", "Fast",
                         "Quickest pass. Text only, no layout analysis."),
            OptionChoice("balanced", "Balanced (Recommended)",
                         "Good accuracy and speed for most documents."),
            OptionChoice("thorough", "Thorough",
                         "Slowest. Full layout analysis; best for dense or scanned pages."),
        ),
        implemented=False,
    ),
    StageOption(
        key="output_format",
        kind=OptionKind.CHOICE,
        label="Output format",
        default="markdown",
        choices=(
            OptionChoice("markdown", "Structured text (Markdown)",
                         "Preserves structure like headings, tables, lists."),
            OptionChoice("plain", "Plain text",
                         "Strips all structure. Smallest output."),
            OptionChoice("blocks", "Positioned blocks (JSON)",
                         "Keeps each block's page and coordinates."),
        ),
        implemented=False,
    ),
    StageOption("extract_tables", OptionKind.TOGGLE, "Extract tables", True,
                "Tables become structured rows rather than run-together text."),
    StageOption("extract_images", OptionKind.TOGGLE, "Extract images (with captions)", True,
                "Saves embedded figures as images later stages can show."),
    StageOption("extract_layout", OptionKind.TOGGLE, "Extract slide layout", True,
                "For decks: where each title, picture and text box sits on the "
                "slide, so the video can place things the way the slide did."),
    StageOption("extract_backgrounds", OptionKind.TOGGLE, "Extract background images", True,
                "For decks: the picture or colour behind each slide, saved like "
                "any other image — a background is a picture in its own right, "
                "not a detail of the styling."),
    StageOption("extract_styling", OptionKind.TOGGLE, "Extract styling (theme colours and fonts)",
                True,
                "For decks: the theme's colour scheme, its heading and body fonts, "
                "and the slide proportions, so the video can look like the deck "
                "rather than the renderer's defaults."),
    StageOption("detect_key_fields", OptionKind.TOGGLE, "Detect key fields (auto)", True,
                "Pulls out labelled values — dates, references, totals.",
                implemented=False),
    StageOption("handwriting_ocr", OptionKind.TOGGLE, "Use handwriting recognition (OCR)", False,
                "Much slower. Only worth enabling for handwritten source pages.",
                implemented=False),
)


SCENE_PLAN_OPTIONS: tuple[StageOption, ...] = (
    StageOption(
        key="target_duration",
        kind=OptionKind.CHOICE,
        label="Target duration",
        default="7-10",
        choices=(
            OptionChoice("3-5", "3-5 minutes", "A single focused idea."),
            OptionChoice("7-10", "7-10 minutes", "A chapter with room for an example."),
            OptionChoice("12-18", "12-18 minutes", "A full module. Expect 8-12 sections."),
        ),
    ),
    StageOption(
        key="tone",
        kind=OptionKind.CHOICE,
        label="Tone",
        default="professional",
        choices=(
            OptionChoice("professional", "Professional",
                         "Measured and precise. Assumes the viewer is here to learn."),
            OptionChoice("conversational", "Conversational",
                         "Warmer and more direct, without losing rigour."),
            OptionChoice("academic", "Academic",
                         "Formal, careful with qualifiers, heavier on terminology."),
        ),
    ),
    StageOption(
        key="language",
        kind=OptionKind.CHOICE,
        label="Language",
        default="en",
        choices=(
            OptionChoice("en", "English", ""),
            OptionChoice("hi", "Hindi", "Narration voice availability varies by language."),
            OptionChoice("te", "Telugu", "Narration voice availability varies by language."),
        ),
    ),
)


OPTIONS_BY_STAGE: dict[Stage, tuple[StageOption, ...]] = {
    Stage.EXTRACTION: EXTRACTION_OPTIONS,
    Stage.SCENE_PLAN: SCENE_PLAN_OPTIONS,
}


def options_for(stage: Stage) -> tuple[StageOption, ...]:
    """Stages with no options yet return empty rather than raising -- the UI
    renders no options panel, which is the correct outcome."""
    return OPTIONS_BY_STAGE.get(stage, ())


@dataclass
class StageSettings:
    """Resolved settings for one stage: every declared option, always present."""

    stage: Stage
    values: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage.value,
            "values": self.values,
            "options": [option.to_dict() for option in options_for(self.stage)],
        }


class StageSettingsStore:
    """Reads and writes `projects/<slug>/settings/<stage>.json`.

    Every read returns a complete set of values: unknown keys are dropped and
    missing ones filled from defaults. A caller therefore never has to check
    whether a setting exists, which is where `KeyError` on a renamed option would
    otherwise surface -- far from the rename that caused it.
    """

    def __init__(self, project_root: Path) -> None:
        self.settings_directory = project_root / "settings"

    def _path_for(self, stage: Stage) -> Path:
        return self.settings_directory / f"{stage.value}.json"

    def load(self, stage: Stage) -> StageSettings:
        declared_options = options_for(stage)
        # Defaults are a safe outcome, but silence would leave a user wondering
        # why their settings keep reverting -- read_json_object logs it.
        stored_values = read_json_object(
            self._path_for(stage), f"{stage.value} settings") or {}

        return StageSettings(
            stage=stage,
            values={
                option.key: option.coerce(stored_values.get(option.key, option.default))
                for option in declared_options
            },
        )

    def save(self, stage: Stage, submitted_values: dict[str, Any]) -> StageSettings:
        """Coerce, then write atomically.

        Only declared keys are persisted, so a client cannot grow the settings file
        with arbitrary content, and a removed option disappears on next write
        rather than lingering forever.
        """
        declared_options = options_for(stage)
        coerced_values = {
            option.key: option.coerce(submitted_values.get(option.key, option.default))
            for option in declared_options
        }

        write_text_atomically(
            self._path_for(stage), json.dumps(coerced_values, indent=2))

        return StageSettings(stage=stage, values=coerced_values)


# --- what the Scene Plan's preferences actually mean ---------------------------------

# The spoken length each choice is asking for, as (shortest, longest) seconds.
# A range rather than a number: "about eight minutes" is the real intent, and a
# plan that lands at 7:40 has not missed.
TARGET_DURATIONS: dict[str, tuple[int, int]] = {
    "3-5": (180, 300),
    "7-10": (420, 600),
    "12-18": (720, 1080),
}

# What a tone means, written as an instruction rather than an adjective: an agent
# told "conversational" guesses, and told "use the second person" does not.
TONE_GUIDANCE: dict[str, str] = {
    "professional": (
        "Measured and precise. Full sentences, no filler, no exclamation marks. "
        "Assume the viewer is here to learn and does not need warming up."
    ),
    "conversational": (
        "Warm and direct, without losing rigour. Address the viewer as \"you\", "
        "use short sentences and contractions, and let one idea lead into the "
        "next. Never chatty for its own sake: no jokes, no filler openers."
    ),
    "academic": (
        "Formal and careful. Keep the field's terminology and define it on first "
        "use, qualify claims the source qualifies, and prefer the passive where "
        "the source uses it. Do not simplify away precision."
    ),
}

# Each language, and the voice each provider has for it. A language with no voice
# is still a language: the narration is written in it and the render says plainly
# that it could not be spoken.
LANGUAGES: dict[str, dict[str, str]] = {
    "en": {"name": "English", "edge": "en-US-AriaNeural", "openai": "alloy"},
    "hi": {"name": "Hindi", "edge": "hi-IN-SwaraNeural"},
    "te": {"name": "Telugu", "edge": "te-IN-ShrutiNeural"},
}


@dataclass(frozen=True)
class VideoPreferences:
    """The Scene Plan's three choices, resolved into what each stage needs.

    Read together because they are decided together and each is used by more
    than one stage: the duration steers drafting and is checked against the
    finished plan, the tone reaches the narration, and the language reaches both
    the narration and the voice that speaks it.
    """

    target_duration: str
    tone: str
    language: str

    @property
    def target_seconds(self) -> tuple[int, int]:
        return TARGET_DURATIONS.get(self.target_duration, TARGET_DURATIONS["7-10"])

    @property
    def target_phrase(self) -> str:
        shortest, longest = self.target_seconds
        return f"{shortest // 60} to {longest // 60} minutes"

    @property
    def tone_sentence(self) -> str:
        return TONE_GUIDANCE.get(self.tone, TONE_GUIDANCE["professional"])

    @property
    def language_name(self) -> str:
        return LANGUAGES.get(self.language, LANGUAGES["en"])["name"]

    def voice_for(self, provider_key: str) -> str:
        """The provider's voice for this language, or empty if it has none."""
        return LANGUAGES.get(self.language, {}).get(provider_key, "")

    def to_dict(self) -> dict[str, Any]:
        shortest, longest = self.target_seconds
        return {
            "target_duration": self.target_duration,
            "target_seconds": [shortest, longest],
            "target_phrase": self.target_phrase,
            "tone": self.tone,
            "language": self.language,
            "language_name": self.language_name,
        }


def video_preferences(project_root: Path) -> VideoPreferences:
    """The preferences saved for this project, with every value coerced.

    Read from the same settings file the page writes, so there is no second
    place a preference can be stored and no chance of the two disagreeing.
    """
    saved = StageSettingsStore(project_root).load(Stage.SCENE_PLAN).values
    return VideoPreferences(
        target_duration=str(saved.get("target_duration", "7-10")),
        tone=str(saved.get("tone", "professional")),
        language=str(saved.get("language", "en")),
    )
