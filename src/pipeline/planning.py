"""The plan: the video's agreed shape -- its sections, the slides each covers, and
the scenes each is made of.

The plan is made in a conversation with the planning agent (`plan_agent.py`).
The person sets the length in their own words and how strictly the slides' order
is kept. The agent proposes the shape: sections, minutes, scenes per section. The
person agrees to it or says what to change, and only then are the scenes
detailed. After that everything is editable by hand. Both paths write this one
document.

Stored at `projects/<slug>/scene-plan/plan.json`.
"""

from __future__ import annotations

import json
import logging
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
MAXIMUM_SECTIONS_PER_PLAN = 60
MAXIMUM_SCENES_PER_SECTION = 60
MAXIMUM_SOURCES_PER_SECTION = 40
MAXIMUM_SCENE_TEXT_LENGTH = 400
LONGEST_SETUP_TEXT = 300


# How strictly the slides' order is kept. Held by code (`plan_order.py`), not by
# trusting the agent.
SLIDE_ORDERS = {
    "strict": "Strict: each section is an unbroken run of slides, in the deck's order.",
    "nearly": "Nearly strict: sections follow the deck; a slide may move within a section.",
    "loose": "Loose: the deck's order is a guide; no slide is used twice.",
    "free": "Free: no need to follow the deck's order.",
}


class SourceReference(BaseModel):
    """A place in the extracted content: a document, a heading within it, and --
    for a deck -- the slide. A location rather than a block id, because block ids
    change on every extraction run."""

    file_name: str = ""
    heading_path: list[str] = Field(default_factory=list)
    slide_number: int = 0

    @property
    def label(self) -> str:
        named = " › ".join([self.file_name, *self.heading_path])
        return f"{named} (slide {self.slide_number})" if self.slide_number else named


class PlanScene(BaseModel):
    """One scene: what it does, the slides it is about, and how long it runs.
    Every later layer works scene by scene -- the script writes its narration,
    Generation its `scene.py` -- and this is where a scene is decided."""

    id: str = Field(default_factory=new_identifier)
    does: str = ""
    slides: list[int] = Field(default_factory=list)
    seconds: int = 30

    @field_validator("does")
    @classmethod
    def _cap_does(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_SCENE_TEXT_LENGTH]

    @field_validator("seconds")
    @classmethod
    def _clamp_seconds(cls, value: int) -> int:
        return max(3, min(int(value), 900))


class PlanSection(BaseModel):
    id: str = Field(default_factory=new_identifier)
    title: str = ""
    summary: str = ""
    estimated_seconds: int = 60

    # How this section is told, in the planning agent's own words -- there are no
    # fixed kinds of section. A section with no slides (an opening, a recap,
    # whatever the video needs) is written from the rest of the plan.
    how: str = ""

    # The slides (or headings) it covers. For a deck, one reference per slide.
    sources: list[SourceReference] = Field(default_factory=list)

    # The scenes it is made of. Its length is theirs once it has any.
    scenes: list[PlanScene] = Field(default_factory=list)

    # The pictures it shows, from what Assets & Design transferred, and whether a
    # person chose them rather than the rule (`plan_pictures.py`).
    picture_paths: list[str] = Field(default_factory=list)
    pictures_chosen: bool = False

    @field_validator("sources")
    @classmethod
    def _cap_sources(cls, value: list[SourceReference]) -> list[SourceReference]:
        unique: list[SourceReference] = []
        for reference in value:
            if reference.file_name and reference not in unique:
                unique.append(reference)
        return unique[:MAXIMUM_SOURCES_PER_SECTION]

    @field_validator("scenes")
    @classmethod
    def _cap_scenes(cls, value: list[PlanScene]) -> list[PlanScene]:
        return value[:MAXIMUM_SCENES_PER_SECTION]

    @field_validator("title")
    @classmethod
    def _cap_title(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_SECTION_TITLE_LENGTH]

    @field_validator("summary", "how")
    @classmethod
    def _cap_summary(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_SECTION_SUMMARY_LENGTH]

    @field_validator("estimated_seconds")
    @classmethod
    def _clamp_duration(cls, value: int) -> int:
        return max(1, min(int(value), 4 * 3600))

    @model_validator(mode="after")
    def _length_is_its_scenes(self) -> PlanSection:
        if self.scenes:
            self.estimated_seconds = sum(scene.seconds for scene in self.scenes)
        return self


class PlanLength(BaseModel):
    """The length the person asked for, as the agent understood it -- shown back
    to them, and what the checks hold the plan to."""

    shortest_seconds: int = 0
    longest_seconds: int = 0
    understood: str = ""     # in words, e.g. "About 60 min. May run longer, not shorter."

    @property
    def is_known(self) -> bool:
        return self.longest_seconds > 0


class Plan(BaseModel):
    """Everything the Scene Plan decides, in one document."""

    sections: list[PlanSection] = Field(default_factory=list)

    # The setup, in the person's own words.
    length_text: str = ""
    length: PlanLength = Field(default_factory=PlanLength)
    slide_order: str = "strict"
    audience: str = ""

    # Slides the agreed shape leaves out on purpose, with why.
    slides_left_out: dict[int, str] = Field(default_factory=dict)

    # When the person agreed to the shape; empty until they do.
    shape_agreed_at: str = ""

    # Which extraction this plan was made from, as its content fingerprint.
    extraction_fingerprint: str = ""

    # The Assets & Design transfer the sections' pictures were attached from.
    pictures_from: str = ""

    @field_validator("slide_order")
    @classmethod
    def _known_order(cls, value: str) -> str:
        return value if value in SLIDE_ORDERS else "strict"

    @field_validator("length_text", "audience")
    @classmethod
    def _cap_setup(cls, value: str) -> str:
        return value.strip()[:LONGEST_SETUP_TEXT]

    @field_validator("sections")
    @classmethod
    def _cap_sections(cls, value: list[PlanSection]) -> list[PlanSection]:
        return value[:MAXIMUM_SECTIONS_PER_PLAN]

    @property
    def total_estimated_seconds(self) -> int:
        return sum(section.estimated_seconds for section in self.sections)

    @property
    def scene_count(self) -> int:
        return sum(len(section.scenes) for section in self.sections)

    @property
    def is_empty(self) -> bool:
        return not self.sections

    def to_dict(self) -> dict:
        return self.model_dump(mode="json") | {
            "total_estimated_seconds": self.total_estimated_seconds,
            "scene_count": self.scene_count,
            "is_empty": self.is_empty,
            "warnings": self.warnings(),
        }

    def warnings(self) -> list[str]:
        """Advisory problems, shown on the page; nothing refuses to save."""
        untitled = sum(1 for section in self.sections if not section.title)
        return [f"{untitled} section(s) have no title"] if untitled else []


class PlanStore(JsonDocumentStore[Plan]):
    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.SCENE_PLAN),
            model_type=Plan,
            build_default=Plan,
            description="plan",
        )

    @property
    def plan_path(self) -> Path:
        return self.document_path


class PlanDraftStore:
    """The planning agent's latest proposal, waiting to be agreed to or discarded.
    On disk, so a reload does not lose a model's work; outside `scene-plan/`, so
    it is never mistaken for the plan."""

    def __init__(self, project_root: Path) -> None:
        self.path = project_root / "drafts" / "plan.json"

    def load(self) -> dict | None:
        return read_json_object(self.path, "plan proposal")

    def save(self, draft: dict) -> dict:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomically(self.path, json.dumps(draft, indent=2, ensure_ascii=False))
        return draft

    def clear(self) -> bool:
        if self.path.exists():
            self.path.unlink()
            return True
        return False
