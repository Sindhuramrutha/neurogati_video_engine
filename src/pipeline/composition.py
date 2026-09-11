"""The composition — the Studio's artifact: what appears on screen, and when.

A multi-track timeline. Tracks stack bottom-to-top for compositing; clips within a
track are placed on an absolute timeline in milliseconds.

**Milliseconds, integer, everywhere.** Floating-point seconds accumulate error
across trims and moves, and "why is this clip 3 frames off?" is a miserable bug to
chase. Frame numbers would tie the document to a frame rate that can change. An
integer millisecond survives both.

Stored at `projects/<slug>/studio/composition.json`.
"""

from __future__ import annotations

import logging
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

DEFAULT_FRAME_RATE = 30
DEFAULT_FRAME_WIDTH = 1920
DEFAULT_FRAME_HEIGHT = 1080

MINIMUM_CLIP_DURATION_MS = 100      # below this a clip cannot be grabbed or seen
MAXIMUM_COMPOSITION_DURATION_MS = 4 * 60 * 60 * 1000   # 4 hours
MAXIMUM_CLIPS_PER_TRACK = 500
MAXIMUM_TRACKS = 24


class TrackKind(StrEnum):
    VIDEO = "video"
    TEXT = "text"
    GRAPHICS = "graphics"
    AUDIO = "audio"


class ClipKind(StrEnum):
    VIDEO = "video"
    IMAGE = "image"
    TEXT = "text"
    SHAPE = "shape"
    AUDIO = "audio"
    SCENE = "scene"      # a rendered pipeline scene


class Clip(BaseModel):
    id: str = Field(default_factory=new_identifier)
    kind: ClipKind = ClipKind.TEXT
    label: str = ""

    start_ms: int = 0
    duration_ms: int = 3000

    # What this clip shows. `asset_id` points at the media library; `text` carries
    # literal content for text clips. Kept as separate fields rather than one
    # untyped payload so a text clip cannot silently reference a missing asset.
    asset_id: str | None = None
    text: str = ""

    # Source trim, for clips backed by timed media.
    source_in_ms: int = 0

    @field_validator("start_ms")
    @classmethod
    def _clamp_start(cls, value: int) -> int:
        return max(0, min(int(value), MAXIMUM_COMPOSITION_DURATION_MS))

    @field_validator("duration_ms")
    @classmethod
    def _clamp_duration(cls, value: int) -> int:
        # A zero or negative duration produces a clip that cannot be selected or
        # deleted from the UI -- effectively a stuck row.
        return max(MINIMUM_CLIP_DURATION_MS,
                   min(int(value), MAXIMUM_COMPOSITION_DURATION_MS))

    @field_validator("source_in_ms")
    @classmethod
    def _clamp_source_in(cls, value: int) -> int:
        return max(0, int(value))

    @property
    def end_ms(self) -> int:
        return self.start_ms + self.duration_ms

    def overlaps(self, other: Clip) -> bool:
        return self.start_ms < other.end_ms and other.start_ms < self.end_ms


class Track(BaseModel):
    id: str = Field(default_factory=new_identifier)
    kind: TrackKind = TrackKind.VIDEO
    label: str = ""
    is_locked: bool = False
    is_visible: bool = True
    clips: list[Clip] = Field(default_factory=list)

    @field_validator("clips")
    @classmethod
    def _cap_clips(cls, value: list[Clip]) -> list[Clip]:
        return value[:MAXIMUM_CLIPS_PER_TRACK]

    @property
    def end_ms(self) -> int:
        return max((clip.end_ms for clip in self.clips), default=0)

    def overlapping_clip_ids(self) -> list[str]:
        """Clips that collide on this track.

        Two clips on one track cannot both be shown, so an overlap is a real
        defect -- but it is reported rather than prevented, because forbidding it
        mid-drag makes the timeline fight the pointer.
        """
        ordered = sorted(self.clips, key=lambda clip: clip.start_ms)
        colliding: list[str] = []
        for earlier, later in zip(ordered, ordered[1:], strict=False):
            if earlier.overlaps(later):
                colliding.extend([earlier.id, later.id])
        return sorted(set(colliding))


class Composition(BaseModel):
    """Tracks are ordered bottom-to-top: later tracks composite over earlier ones."""

    frame_rate: int = DEFAULT_FRAME_RATE
    frame_width: int = DEFAULT_FRAME_WIDTH
    frame_height: int = DEFAULT_FRAME_HEIGHT
    tracks: list[Track] = Field(default_factory=list)

    @field_validator("frame_rate")
    @classmethod
    def _sane_frame_rate(cls, value: int) -> int:
        return max(1, min(int(value), 120))

    @field_validator("tracks")
    @classmethod
    def _cap_tracks(cls, value: list[Track]) -> list[Track]:
        return value[:MAXIMUM_TRACKS]

    @property
    def duration_ms(self) -> int:
        return max((track.end_ms for track in self.tracks), default=0)

    @property
    def clip_count(self) -> int:
        return sum(len(track.clips) for track in self.tracks)

    def track_by_id(self, track_id: str) -> Track | None:
        return next((t for t in self.tracks if t.id == track_id), None)

    def audit(self, known_asset_ids: set[str] | None = None) -> dict:
        """Problems worth surfacing before a render is attempted.

        Missing assets are the expensive one: a render that fails ten minutes in
        because a clip points at a deleted file is exactly the kind of late failure
        v1 was full of.
        """
        known = known_asset_ids or set()

        overlaps: dict[str, list[str]] = {}
        missing_assets: list[str] = []
        empty_text_clips: list[str] = []

        for track in self.tracks:
            colliding = track.overlapping_clip_ids()
            if colliding:
                overlaps[track.id] = colliding
            for clip in track.clips:
                if clip.asset_id and known and clip.asset_id not in known:
                    missing_assets.append(clip.id)
                if clip.kind is ClipKind.TEXT and not clip.text.strip():
                    empty_text_clips.append(clip.id)

        return {
            "overlapping_clips": overlaps,
            "missing_asset_clip_ids": missing_assets,
            "empty_text_clip_ids": empty_text_clips,
        }

    def to_dict(self, known_asset_ids: set[str] | None = None) -> dict:
        audit = self.audit(known_asset_ids)
        return self.model_dump(mode="json") | {
            "duration_ms": self.duration_ms,
            "clip_count": self.clip_count,
            "audit": audit,
            "warnings": self._warnings(audit),
        }

    def _warnings(self, audit: dict) -> list[str]:
        found: list[str] = []
        overlapping_total = sum(len(ids) for ids in audit["overlapping_clips"].values())
        if overlapping_total:
            found.append(f"{overlapping_total} clip(s) overlap on the same track")
        if audit["missing_asset_clip_ids"]:
            found.append(
                f"{len(audit['missing_asset_clip_ids'])} clip(s) reference media that "
                f"is no longer in the library"
            )
        if audit["empty_text_clip_ids"]:
            found.append(f"{len(audit['empty_text_clip_ids'])} text clip(s) are empty")
        return found


def default_composition() -> Composition:
    """The four-track layout this pipeline composes into.

    Ordered bottom-to-top so the list reads the way the frame stacks: video at the
    base, then text, then graphics over both. Audio is last and composites nothing.

    **The four ids are fixed, not generated.** A default composition is rebuilt on
    every read until something saves it, so random ids meant reading the timeline
    twice returned two different sets. A client that read the composition, took a
    track id and then placed a clip on it got "no such track" -- fatal for an
    agent, which does exactly that, and invisible in the browser only because it
    renders and posts within a single load. Fixed ids also read better in a diff
    than twelve hex characters.
    """
    return Composition(tracks=[
        Track(id="track-video", kind=TrackKind.VIDEO, label="V1 · Video"),
        Track(id="track-text", kind=TrackKind.TEXT, label="V2 · Text"),
        Track(id="track-graphics", kind=TrackKind.GRAPHICS, label="V3 · Graphics"),
        Track(id="track-audio", kind=TrackKind.AUDIO, label="A1 · Audio"),
    ])


class CompositionStore(JsonDocumentStore[Composition]):
    """Persistence for the composition. Durability behaviour lives in
    `JsonDocumentStore`; this only names the path, the model and the default."""

    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.STUDIO),
            model_type=Composition,
            build_default=default_composition,
            description="composition",
        )

    @property
    def composition_path(self) -> Path:
        """Kept as a named alias: tests and callers read better saying
        `store.composition_path` than `store.document_path`."""
        return self.document_path

