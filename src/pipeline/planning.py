"""The plan — Planning's output artifact, and the first thing a human edits directly.

Extraction has settings that shape a run. Planning is different: the plan itself is
the artifact, it is hand-editable, and an agent can also generate or amend it. Both
paths write the same document, so there is exactly one representation of "what this
video will contain" rather than a generated one and an edited one that drift.

Stored at `projects/<slug>/planning/plan.json` — inside the stage directory,
because unlike settings this genuinely *is* the stage's output, and
`stage_state` reporting the stage as "ready" once a plan exists is correct.
"""

from __future__ import annotations

import json
import logging
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator

from pipeline.stages import Stage
from pipeline.storage.documents import (
    JsonDocumentStore,
    new_identifier,
    read_json_object,
    write_text_atomically,
)
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MAXIMUM_SECTION_TITLE_LENGTH = 120
MAXIMUM_SECTION_SUMMARY_LENGTH = 400
MAXIMUM_OBJECTIVE_LENGTH = 200
MAXIMUM_SECTIONS_PER_PLAN = 60
MAXIMUM_RENDERING_REASON_LENGTH = 240
MAXIMUM_SOURCES_PER_SECTION = 20

# A section shorter than this cannot carry a complete thought; longer than this and
# it should have been split. Advisory only -- the UI flags it, nothing rejects it.
MINIMUM_REASONABLE_SECTION_SECONDS = 10
MAXIMUM_REASONABLE_SECTION_SECONDS = 600


class RenderingApproach(StrEnum):
    """How a section should be shown. The same five choices the Planning agent's
    instructions describe, so what it is told to choose and what it can record
    are the same list."""

    COMPOSITION = "composition"
    PLOT = "plot"
    SIMULATION = "simulation"
    CODE = "code"
    STILL = "still"


class SourceReference(BaseModel):
    """A place in the extracted content: a document, and a heading within it.

    A location rather than a block id, because block ids are regenerated on every
    extraction run and a reference to one would break the next time extraction
    ran. An empty heading path means the whole document.
    """

    file_name: str = ""
    heading_path: list[str] = Field(default_factory=list)

    @property
    def label(self) -> str:
        return " › ".join([self.file_name, *self.heading_path])


class PlanSection(BaseModel):
    id: str = Field(default_factory=new_identifier)
    title: str = ""
    summary: str = ""
    estimated_seconds: int = 60

    # What the section teaches from. Without these a plan could be about
    # material that is not in the extraction at all -- and one was: every
    # section of a real plan described a chapter the extraction no longer held.
    sources: list[SourceReference] = Field(default_factory=list)

    # How it should be shown, and one sentence of why. The Planning agent was
    # always told to choose these; the plan had nowhere to put them, so the
    # choice was silently thrown away.
    rendering_approach: str = ""
    rendering_reason: str = ""

    # Which of the plan's learning objectives this section serves.
    objective_ids: list[str] = Field(default_factory=list)

    @field_validator("rendering_approach")
    @classmethod
    def _known_approach(cls, value: str) -> str:
        # Unknown values become "not chosen" rather than an error: an older or
        # hand-edited plan must still load.
        cleaned = (value or "").strip().lower()
        return cleaned if cleaned in {a.value for a in RenderingApproach} else ""

    @field_validator("rendering_reason")
    @classmethod
    def _cap_reason(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_RENDERING_REASON_LENGTH]

    @field_validator("sources")
    @classmethod
    def _cap_sources(cls, value: list[SourceReference]) -> list[SourceReference]:
        unique: list[SourceReference] = []
        for reference in value:
            if reference.file_name and reference not in unique:
                unique.append(reference)
        return unique[:MAXIMUM_SOURCES_PER_SECTION]

    @field_validator("title")
    @classmethod
    def _cap_title(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_SECTION_TITLE_LENGTH]

    @field_validator("summary")
    @classmethod
    def _cap_summary(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_SECTION_SUMMARY_LENGTH]

    @field_validator("estimated_seconds")
    @classmethod
    def _clamp_duration(cls, value: int) -> int:
        # A negative or absurd duration would poison the plan total and, later,
        # the narration budget. Clamped rather than rejected so a typo does not
        # lose the rest of an edit.
        return max(1, min(int(value), 3600))

    @property
    def is_unusually_short(self) -> bool:
        return self.estimated_seconds < MINIMUM_REASONABLE_SECTION_SECONDS

    @property
    def is_unusually_long(self) -> bool:
        return self.estimated_seconds > MAXIMUM_REASONABLE_SECTION_SECONDS


class LearningObjective(BaseModel):
    id: str = Field(default_factory=new_identifier)
    text: str = ""
    is_included: bool = True

    @field_validator("text")
    @classmethod
    def _cap_text(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_OBJECTIVE_LENGTH]


class Plan(BaseModel):
    """Everything Planning decides, in one document."""

    sections: list[PlanSection] = Field(default_factory=list)
    learning_objectives: list[LearningObjective] = Field(default_factory=list)

    # Audiences are offered as choices and one is active, because tone and depth
    # are written for a single reader -- "professionals and children" produces
    # material that serves neither.
    audience_choices: list[str] = Field(
        default_factory=lambda: ["Students new to the topic", "Practitioners", "Mixed"]
    )
    selected_audience: str = "Students new to the topic"

    # Proposed by a drafted plan, from the source material, or added by hand.
    # (This comment used to say Extraction fills these in. It never did.)
    key_themes: list[str] = Field(default_factory=list)

    # Which extraction this plan was drafted from, or last confirmed against, as
    # the extraction's content fingerprint. Empty for a plan made by hand that
    # nobody has checked against the extraction. Hand edits do not update it:
    # editing a title is not a statement that the plan matches new material.
    extraction_fingerprint: str = ""

    @field_validator("sections")
    @classmethod
    def _cap_sections(cls, value: list[PlanSection]) -> list[PlanSection]:
        return value[:MAXIMUM_SECTIONS_PER_PLAN]

    @model_validator(mode="after")
    def _drop_links_to_missing_objectives(self) -> Plan:
        # Deleting an objective must not leave sections pointing at it, whichever
        # client did the deleting.
        known = {objective.id for objective in self.learning_objectives}
        for section in self.sections:
            section.objective_ids = [oid for oid in section.objective_ids if oid in known]
        return self

    def objective_coverage(self) -> dict[str, list[str]]:
        """For each included objective, the ids of the sections that serve it."""
        return {
            objective.id: [s.id for s in self.sections if objective.id in s.objective_ids]
            for objective in self.learning_objectives if objective.is_included
        }

    @property
    def total_estimated_seconds(self) -> int:
        return sum(section.estimated_seconds for section in self.sections)

    @property
    def is_empty(self) -> bool:
        return not self.sections and not self.learning_objectives

    def to_dict(self) -> dict:
        return self.model_dump(mode="json") | {
            "total_estimated_seconds": self.total_estimated_seconds,
            "is_empty": self.is_empty,
            "objective_coverage": self.objective_coverage(),
            "warnings": self.warnings(),
        }

    def warnings(self) -> list[str]:
        """Advisory problems a reviewer should see before moving on.

        Deliberately not errors: a plan mid-edit is allowed to be inconsistent,
        and blocking on it would make the outline hostile to work in. The UI shows
        these; nothing refuses to save because of them.
        """
        found: list[str] = []

        untitled_count = sum(1 for section in self.sections if not section.title)
        if untitled_count:
            found.append(f"{untitled_count} section(s) have no title")

        odd_durations = [
            section for section in self.sections
            if section.is_unusually_short or section.is_unusually_long
        ]
        if odd_durations:
            found.append(f"{len(odd_durations)} section(s) have an unusual duration")

        if self.sections and not any(o.is_included for o in self.learning_objectives):
            found.append("no learning objectives are selected")

        if not self.selected_audience:
            found.append("no audience selected")

        # Coverage is only judged once sections are linked to objectives at all;
        # before that every objective would read as uncovered, which is noise.
        if any(section.objective_ids for section in self.sections):
            uncovered = [oid for oid, ids in self.objective_coverage().items() if not ids]
            if uncovered:
                found.append(
                    f"{len(uncovered)} learning objective(s) are not covered by any section"
                )

        return found


class PlanStore(JsonDocumentStore[Plan]):
    """Persistence for the plan. Durability behaviour lives in
    `JsonDocumentStore`; this only names the path, the model and the default."""

    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.PLANNING),
            model_type=Plan,
            build_default=Plan,
            description="plan",
        )

    @property
    def plan_path(self) -> Path:
        """Kept as a named alias: tests and callers read better saying
        `store.plan_path` than `store.document_path`."""
        return self.document_path


class PlanDraftStore:
    """A plan the Planning agent proposed, waiting to be accepted or discarded.

    Kept on disk rather than only in the page because drafting reads the whole
    source and makes one model call per section: a reload must not throw that
    away. Stored outside `planning/` so a pending draft never makes the stage look
    finished, and never mistaken for the plan itself.
    """

    def __init__(self, project_root: Path) -> None:
        self.path = project_root / "drafts" / "plan.json"

    def load(self) -> dict | None:
        return read_json_object(self.path, "plan draft")

    def save(self, draft: dict) -> dict:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomically(self.path, json.dumps(draft, indent=2, ensure_ascii=False))
        return draft

    def clear(self) -> bool:
        if self.path.exists():
            self.path.unlink()
            return True
        return False

