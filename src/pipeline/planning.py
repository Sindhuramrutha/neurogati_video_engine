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

import logging
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MAXIMUM_SECTION_TITLE_LENGTH = 120
MAXIMUM_SECTION_SUMMARY_LENGTH = 400
MAXIMUM_OBJECTIVE_LENGTH = 200
MAXIMUM_SECTIONS_PER_PLAN = 60

# A section shorter than this cannot carry a complete thought; longer than this and
# it should have been split. Advisory only -- the UI flags it, nothing rejects it.
MINIMUM_REASONABLE_SECTION_SECONDS = 10
MAXIMUM_REASONABLE_SECTION_SECONDS = 600


class PlanSection(BaseModel):
    id: str = Field(default_factory=new_identifier)
    title: str = ""
    summary: str = ""
    estimated_seconds: int = 60

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

    # Populated by Extraction once it runs; hand-editable until then.
    key_themes: list[str] = Field(default_factory=list)

    @field_validator("sections")
    @classmethod
    def _cap_sections(cls, value: list[PlanSection]) -> list[PlanSection]:
        return value[:MAXIMUM_SECTIONS_PER_PLAN]

    @property
    def total_estimated_seconds(self) -> int:
        return sum(section.estimated_seconds for section in self.sections)

    @property
    def is_empty(self) -> bool:
        return not self.sections and not self.learning_objectives

    def to_dict(self) -> dict:
        return self.model_dump() | {
            "total_estimated_seconds": self.total_estimated_seconds,
            "is_empty": self.is_empty,
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

