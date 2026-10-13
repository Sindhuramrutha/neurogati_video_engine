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
            "choices": [
                {"value": c.value, "label": c.label, "help_text": c.help_text}
                for c in self.choices
            ],
        }


# "Extraction mode" and "Output format" were here, both disabled. They were not
# unbuilt features but contradictions: the output is always structured blocks --
# that is the stage's whole thesis -- and a greyed-out "Balanced (Recommended)"
# recommends a choice that does nothing. A panel that offers settings it will
# never honour teaches people to distrust the ones that work.
EXTRACTION_OPTIONS: tuple[StageOption, ...] = (
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
    StageOption("handwriting_ocr", OptionKind.TOGGLE, "Use handwriting recognition (OCR)", False,
                "For PDFs: pages with no text layer — scanned or handwritten — are "
                "read by the vision model and marked as transcribed. Slower, and "
                "needs an API key. Pages that already have text are never sent."),
)


SCENE_PLAN_OPTIONS: tuple[StageOption, ...] = (
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

# How every video speaks. The aim is fixed -- teaching -- so the voice is too: not
# a choice, but one instruction, written as what to do rather than an adjective.
TEACHING_TONE = (
    "A teacher explaining to one viewer. Clear and direct: address the viewer as "
    "\"you\", one idea at a time, each leading into the next, in full sentences. "
    "Keep the source's terms and say what each means the first time it is used; "
    "qualify what the source qualifies. No filler, no jokes, no exclamation marks."
)

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
    """The video's language, resolved into what each stage needs: it reaches the
    narration and the voice that speaks it. The length is the plan's own, set in
    the person's words (`Plan.length_text`). There is no tone to choose: every
    video teaches (`TEACHING_TONE`).
    """

    language: str
    learners: str = ""          # the learners chosen in Video setup, with what each needs
    chosen_voice: str = ""      # the Edge voice chosen there, with its pace ("voice@rate")

    def audience(self, written: str = "") -> str:
        """Who the video is for: the person's own words and the learners chosen."""
        parts = [part for part in (written.strip(), self.learners) if part]
        return "\n".join(parts) or "not stated"

    @property
    def tone_sentence(self) -> str:
        return TEACHING_TONE

    @property
    def language_name(self) -> str:
        return LANGUAGES.get(self.language, LANGUAGES["en"])["name"]

    def voice_for(self, provider_key: str) -> str:
        """The provider's voice for this language -- the one chosen in Video setup,
        when one is -- or empty if it has none. Scenes are measured and the render
        speaks with this same voice, so the two cannot differ."""
        if provider_key == "edge" and self.chosen_voice:
            return self.chosen_voice
        return LANGUAGES.get(self.language, {}).get(provider_key, "")

    def to_dict(self) -> dict[str, Any]:
        return {
            "language": self.language,
            "language_name": self.language_name,
        }


def video_preferences(project_root: Path) -> VideoPreferences:
    """The preferences saved for this project, with every value coerced.

    Read from the same settings file the page writes, so there is no second
    place a preference can be stored and no chance of the two disagreeing.
    """
    from pipeline import video_setup

    saved = StageSettingsStore(project_root).load(Stage.SCENE_PLAN).values
    language = str(saved.get("language", "en"))
    return VideoPreferences(
        language=language,
        learners=video_setup.audience_text(project_root),
        chosen_voice=video_setup.edge_voice(project_root, language),
    )
