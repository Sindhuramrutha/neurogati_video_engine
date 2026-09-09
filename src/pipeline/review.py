"""Review — comments, chapters and version history for a finished cut.

The important part is the comment log. v1's feedback existed only as prose typed
into a terminal and was gone the moment the scrollback rolled: nobody could answer
"what did we ask for last time, and did it get done?".

Here a comment is anchored to a timecode, attributed, routed to the stage that can
actually fix it, and resolvable. Feedback becomes a record rather than an
instruction shouted once.

Stored at `projects/<slug>/reviewing/review.json`.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MAXIMUM_COMMENT_LENGTH = 2000
MAXIMUM_AUTHOR_LENGTH = 80
MAXIMUM_CHAPTER_TITLE_LENGTH = 100
MAXIMUM_COMMENTS = 2000
MAXIMUM_CHAPTERS = 100


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


class CommentStatus(StrEnum):
    OPEN = "open"
    ADDRESSED = "addressed"
    DECLINED = "declined"


class Comment(BaseModel):
    """One piece of feedback, anchored in time and routed to a stage.

    `routed_to_stage` is the point: "the pacing is frantic" is a Scripting defect,
    not a Studio one, and fixing it in Studio treats the symptom. Routing makes the
    responsible stage explicit instead of leaving it to whoever picks the comment
    up.
    """

    id: str = Field(default_factory=new_identifier)
    author: str = ""
    body: str = ""
    at_ms: int = 0                       # integer ms, matching the composition
    created_at: str = Field(default_factory=_now)
    status: CommentStatus = CommentStatus.OPEN
    routed_to_stage: Stage | None = None
    resolution_note: str = ""

    @field_validator("author")
    @classmethod
    def _cap_author(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_AUTHOR_LENGTH] or "Anonymous"

    @field_validator("body")
    @classmethod
    def _cap_body(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_COMMENT_LENGTH]

    @field_validator("at_ms")
    @classmethod
    def _clamp_at(cls, value: int) -> int:
        return max(0, int(value))

    @property
    def is_open(self) -> bool:
        return self.status is CommentStatus.OPEN


class Chapter(BaseModel):
    id: str = Field(default_factory=new_identifier)
    title: str = ""
    start_ms: int = 0

    @field_validator("title")
    @classmethod
    def _cap_title(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_CHAPTER_TITLE_LENGTH]

    @field_validator("start_ms")
    @classmethod
    def _clamp_start(cls, value: int) -> int:
        return max(0, int(value))


class VideoVersion(BaseModel):
    """A rendered cut. Recorded even before rendering exists, so the review log
    can always say which version a comment was made against."""

    id: str = Field(default_factory=new_identifier)
    label: str = ""
    created_at: str = Field(default_factory=_now)
    notes: str = ""
    duration_ms: int = 0
    file_path: str | None = None         # None until a render actually produces one

    @property
    def is_rendered(self) -> bool:
        return self.file_path is not None


class Review(BaseModel):
    comments: list[Comment] = Field(default_factory=list)
    chapters: list[Chapter] = Field(default_factory=list)
    versions: list[VideoVersion] = Field(default_factory=list)
    active_version_id: str | None = None

    @field_validator("comments")
    @classmethod
    def _cap_comments(cls, value: list[Comment]) -> list[Comment]:
        return value[:MAXIMUM_COMMENTS]

    @field_validator("chapters")
    @classmethod
    def _cap_chapters(cls, value: list[Chapter]) -> list[Chapter]:
        return value[:MAXIMUM_CHAPTERS]

    @property
    def open_comments(self) -> list[Comment]:
        return [comment for comment in self.comments if comment.is_open]

    def comments_by_stage(self) -> dict[str, int]:
        """Open comment counts per routed stage.

        This is the number that tells an operator where to go next: six open
        comments all routed to Scripting means the script is the problem, not the
        timeline.
        """
        counts: dict[str, int] = {}
        for comment in self.open_comments:
            key = comment.routed_to_stage.value if comment.routed_to_stage else "unrouted"
            counts[key] = counts.get(key, 0) + 1
        return counts

    def ordered_chapters(self) -> list[Chapter]:
        return sorted(self.chapters, key=lambda chapter: chapter.start_ms)

    def audit(self) -> dict:
        ordered = self.ordered_chapters()
        duplicate_starts = [
            later.id for earlier, later in zip(ordered, ordered[1:], strict=False)
            if earlier.start_ms == later.start_ms
        ]
        return {
            "open_comment_count": len(self.open_comments),
            "unrouted_comment_ids": [
                c.id for c in self.open_comments if c.routed_to_stage is None
            ],
            "untitled_chapter_ids": [c.id for c in self.chapters if not c.title],
            "duplicate_chapter_ids": duplicate_starts,
            "by_stage": self.comments_by_stage(),
        }

    def to_dict(self) -> dict:
        audit = self.audit()
        return self.model_dump() | {
            "chapters": [c.model_dump() for c in self.ordered_chapters()],
            "audit": audit,
            "warnings": self._warnings(audit),
            "is_ready_to_export": not self.open_comments,
        }

    def _warnings(self, audit: dict) -> list[str]:
        found: list[str] = []
        if audit["open_comment_count"]:
            found.append(f"{audit['open_comment_count']} comment(s) still open")
        if audit["unrouted_comment_ids"]:
            found.append(
                f"{len(audit['unrouted_comment_ids'])} open comment(s) are not routed "
                f"to a stage"
            )
        if audit["untitled_chapter_ids"]:
            found.append(f"{len(audit['untitled_chapter_ids'])} chapter(s) have no title")
        if audit["duplicate_chapter_ids"]:
            found.append("two chapters start at the same time")
        return found


class ReviewStore(JsonDocumentStore[Review]):
    """Persistence for the review. Durability behaviour lives in
    `JsonDocumentStore`; this only names the path, the model and the default."""

    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.REVIEWING),
            model_type=Review,
            build_default=Review,
            description="review",
        )

    @property
    def review_path(self) -> Path:
        """Kept as a named alias: tests and callers read better saying
        `store.review_path` than `store.document_path`."""
        return self.document_path


def chapters_from_plan(plan_sections: list[dict]) -> list[Chapter]:
    """Seed chapters from the plan's sections and their estimated durations.

    A starting point, not a binding: chapters are editable afterwards, and a real
    render's timings will differ from the plan's estimates.
    """
    chapters: list[Chapter] = []
    running_ms = 0
    for section in plan_sections:
        chapters.append(Chapter(title=section.get("title", ""), start_ms=running_ms))
        running_ms += int(section.get("estimated_seconds", 0)) * 1000
    return chapters
