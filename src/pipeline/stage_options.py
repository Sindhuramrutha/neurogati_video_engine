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
    ),
    StageOption("extract_tables", OptionKind.TOGGLE, "Extract tables", True,
                "Tables become structured rows rather than run-together text."),
    StageOption("extract_images", OptionKind.TOGGLE, "Extract images (with captions)", True,
                "Registers embedded figures as assets Graphics can reuse."),
    StageOption("detect_key_fields", OptionKind.TOGGLE, "Detect key fields (auto)", True,
                "Pulls out labelled values — dates, references, totals."),
    StageOption("handwriting_ocr", OptionKind.TOGGLE, "Use handwriting recognition (OCR)", False,
                "Much slower. Only worth enabling for handwritten source pages."),
)


PLANNING_OPTIONS: tuple[StageOption, ...] = (
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
    Stage.PLANNING: PLANNING_OPTIONS,
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
