"""Brand assets: the things a video carries that no source document has.

A watermark, a logo in a corner, an intro before the lesson and an outro after
it. They are uploaded on Assets & Design, transferred with the rest of that
layer, and put on by the render (`render_brand.py`).

Everything is deterministic. Each file is stored under a name taken from its
content, so a transferred kit points at bytes that never change; replacing a
logo stores a new file rather than overwriting the old one.

A logo or a watermark has a **placement**: where its centre sits on the frame,
how wide it is, how see-through, how rounded, how much shadow, and when in the
lesson it is on screen. An intro or an outro has an **edit**: what is trimmed
off each end, and how long it cross-fades with the lesson. All of it is numbers
a person set, so the same kit always puts the same pixels in the same place at
the same time. `prepare_overlay` draws the finished logo or watermark once;
the page shows that same image, so the preview is the render.

Stored at `assets/brand.json`, files in `assets/brand/`.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator

from pipeline.core import OperationFailed, require_project
from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore
from pipeline.storage.layout import artifact_path

IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_TYPES = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}

# slot -> (kind, name, what it does in the video)
SLOTS = {
    "watermark": ("image", "Watermark", "Laid over the lesson, usually large and faint."),
    "logo": ("image", "Logo", "Laid over the lesson, usually small and in a corner."),
    "intro": ("video", "Intro video", "Plays before the lesson starts."),
    "outro": ("video", "Outro video", "Plays after the lesson ends."),
}

SMALLEST_IMAGE_PX = 64
LONGEST_CLIP_MS = 120_000
FRAME_WIDTH_PX, FRAME_HEIGHT_PX = 1920, 1080

# What a person can set, and how far. The page draws its sliders from these.
LIMITS = {
    "width": (0.02, 0.60), "opacity": (0.05, 1.0), "radius": (0.0, 0.5), "shadow": (0.0, 1.0),
    "fade": (0.0, 5.0), "cross_fade": (0.0, 2.0), "seconds": (1.0, 600.0),
}
SHOWS = ["whole", "first", "last", "range"]
SHORTEST_CLIP_SECONDS = 0.5

# The choices this kit had before placements: a corner, three sizes, three
# opacities. Read once, to put an older kit's logo exactly where it was.
_OLD_SIZES = {"small": 0.06, "medium": 0.09, "large": 0.12}
_OLD_OPACITIES = {"faint": 0.10, "light": 0.18, "clear": 0.30}
_OLD_MARGIN_PX = 48


def _within(value: float, limit: str) -> float:
    low, high = LIMITS[limit]
    return round(min(high, max(low, float(value))), 4)


class Placement(BaseModel):
    """Where a logo or watermark sits, how it looks, and when it is on screen."""

    x: float = 0.5            # its centre, as a share of the frame's width
    y: float = 0.5            # ... and of the frame's height
    width: float = 0.09       # as a share of the frame's width
    opacity: float = 1.0
    radius: float = 0.0       # corner rounding, as a share of its shorter side
    shadow: float = 0.0       # 0 none, 1 strongest
    show: str = "whole"       # whole | first | last | range
    seconds: float = 5.0      # for first and last
    start: float = 0.0        # for range: seconds into the lesson
    end: float = 10.0
    fade_in: float = 0.0
    fade_out: float = 0.0

    @model_validator(mode="after")
    def _inside_the_limits(self) -> Placement:
        self.x, self.y = (round(min(1.0, max(0.0, float(v))), 4) for v in (self.x, self.y))
        for name in ("width", "opacity", "radius", "shadow"):
            setattr(self, name, _within(getattr(self, name), name))
        self.fade_in, self.fade_out = _within(self.fade_in, "fade"), _within(self.fade_out, "fade")
        self.seconds = _within(self.seconds, "seconds")
        self.show = self.show if self.show in SHOWS else "whole"
        self.start = round(max(0.0, float(self.start)), 2)
        self.end = round(max(self.start + 0.5, float(self.end)), 2)
        return self

    def window(self, lesson_seconds: float) -> tuple[float, float]:
        """When it is on screen, in seconds from the start of the lesson."""
        if self.show == "first":
            return 0.0, min(self.seconds, lesson_seconds)
        if self.show == "last":
            return max(0.0, lesson_seconds - self.seconds), lesson_seconds
        if self.show == "range":
            return min(self.start, lesson_seconds), min(self.end, lesson_seconds)
        return 0.0, lesson_seconds


class ClipEdit(BaseModel):
    """What is cut off an intro or outro, and how it meets the lesson."""

    trim_start: float = 0.0   # seconds cut from its start
    trim_end: float = 0.0     # seconds cut from its end
    fade: float = 0.0         # seconds of cross-fade with the lesson

    def length(self, clip: BrandFile | None) -> float:
        """How long the clip runs once trimmed. Never less than half a second."""
        if clip is None:
            return 0.0
        whole = clip.duration_ms / 1000
        start = min(max(0.0, self.trim_start), max(0.0, whole - SHORTEST_CLIP_SECONDS))
        end = min(max(0.0, self.trim_end), max(0.0, whole - start - SHORTEST_CLIP_SECONDS))
        return round(whole - start - end, 3)

    def overlap(self, clip: BrandFile | None) -> float:
        """The cross-fade actually used: never more than half the clip."""
        return round(min(_within(self.fade, "cross_fade"), self.length(clip) / 2), 3)


class BrandFile(BaseModel):
    path: str = ""          # relative to the project root
    file_name: str = ""     # as uploaded
    width: int = 0
    height: int = 0
    duration_ms: int = 0
    has_audio: bool = False


class BrandKit(BaseModel):
    watermark: BrandFile | None = None
    logo: BrandFile | None = None
    intro: BrandFile | None = None
    outro: BrandFile | None = None
    logo_place: Placement = Field(
        default_factory=lambda: Placement(x=0.93, y=0.1, width=0.09))
    watermark_place: Placement = Field(
        default_factory=lambda: Placement(width=0.40, opacity=0.10))
    intro_edit: ClipEdit = Field(default_factory=ClipEdit)
    outro_edit: ClipEdit = Field(default_factory=ClipEdit)

    @model_validator(mode="before")
    @classmethod
    def _from_the_older_choices(cls, data):
        """A kit saved with a corner, a size and an opacity keeps them, exactly."""
        if not isinstance(data, dict) or "logo_place" in data:
            return data
        data = dict(data)
        logo = data.get("logo") or {}
        width = _OLD_SIZES.get(data.get("logo_size", "medium"), 0.09)
        tall = width * FRAME_WIDTH_PX * (logo.get("height") or 1) / (logo.get("width") or 1)
        corner = data.get("logo_corner", "top-right")
        across = (_OLD_MARGIN_PX + width * FRAME_WIDTH_PX / 2) / FRAME_WIDTH_PX
        down = (_OLD_MARGIN_PX + tall / 2) / FRAME_HEIGHT_PX
        data["logo_place"] = {"x": across if "left" in corner else 1 - across,
                              "y": down if "top" in corner else 1 - down, "width": width}
        data["watermark_place"] = {"width": 0.40, "opacity": _OLD_OPACITIES.get(
            data.get("watermark_opacity", "faint"), 0.10)}
        return data

    @property
    def is_empty(self) -> bool:
        return not any(getattr(self, slot) for slot in SLOTS)

    @property
    def intro_seconds(self) -> float:
        return self.intro_edit.length(self.intro)

    @property
    def outro_seconds(self) -> float:
        return self.outro_edit.length(self.outro)

    @property
    def lesson_starts_at_ms(self) -> int:
        """Where the lesson begins in the finished video: after the intro, less
        the time the two overlap in their cross-fade."""
        return round((self.intro_seconds - self.intro_edit.overlap(self.intro)) * 1000)

    def total_ms(self, lesson_ms: int) -> int:
        """How long the finished video is, for a lesson of this length."""
        outro = self.outro_seconds - self.outro_edit.overlap(self.outro)
        return self.lesson_starts_at_ms + lesson_ms + round(outro * 1000)


class BrandKitStore(JsonDocumentStore[BrandKit]):
    def __init__(self, project_root) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.ASSETS).with_name("brand.json"),
            model_type=BrandKit, build_default=BrandKit, description="brand assets",
        )


def brand_directory(project) -> Path:
    return artifact_path(project.root, Stage.ASSETS).parent / "brand"


def brand_fingerprint(kit: BrandKit) -> str:
    return hashlib.sha256(json.dumps(kit.model_dump(), sort_keys=True)
                          .encode("utf-8")).hexdigest()[:20]


# --- measuring ----------------------------------------------------------------------


def _measure_image(path: Path) -> dict[str, Any]:
    from PIL import Image

    try:
        with Image.open(path) as image:
            width, height = image.size
    except OSError as failure:
        raise OperationFailed(f"That picture cannot be opened: {failure}") from failure
    if min(width, height) < SMALLEST_IMAGE_PX:
        raise OperationFailed(f"That picture is {width}×{height} px. It needs to be at "
                              f"least {SMALLEST_IMAGE_PX} px on each side to stay sharp.")
    return {"width": width, "height": height}


def _measure_video(path: Path) -> dict[str, Any]:
    probe = shutil.which("ffprobe")
    if not probe:
        raise OperationFailed("ffprobe is not on PATH, so the video cannot be measured. "
                              "Install ffmpeg (winget install Gyan.FFmpeg).")
    try:
        output = subprocess.run(
            [probe, "-v", "error", "-show_entries",
             "format=duration:stream=codec_type,width,height", "-of", "json", str(path)],
            capture_output=True, text=True, timeout=60, check=True).stdout
        facts = json.loads(output)
    except (subprocess.SubprocessError, ValueError) as failure:
        raise OperationFailed("That video cannot be read. Try an .mp4 file.") from failure
    streams = facts.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    if not video:
        raise OperationFailed("That file has no video in it.")
    duration_ms = int(float(facts.get("format", {}).get("duration") or 0) * 1000)
    if not 0 < duration_ms <= LONGEST_CLIP_MS:
        raise OperationFailed(f"An intro or outro can be up to {LONGEST_CLIP_MS // 1000} "
                              f"seconds long; that one is {duration_ms / 1000:.0f}.")
    return {"width": video.get("width", 0), "height": video.get("height", 0),
            "duration_ms": duration_ms,
            "has_audio": any(s.get("codec_type") == "audio" for s in streams)}


# --- what the person does -----------------------------------------------------------


def store_brand_file(slug: str, slot: str, file_name: str, content: bytes) -> dict[str, Any]:
    """Keep an uploaded brand file, under a name taken from its content."""
    if slot not in SLOTS:
        raise OperationFailed(f"{slot!r} is not a brand asset. Use one of: {', '.join(SLOTS)}.")
    kind = SLOTS[slot][0]
    suffix = Path(file_name).suffix.lower()
    allowed = IMAGE_TYPES if kind == "image" else VIDEO_TYPES
    if suffix not in allowed:
        raise OperationFailed(f"The {SLOTS[slot][1].lower()} must be one of "
                              f"{', '.join(sorted(allowed))}; that is {suffix or 'no type'}.")
    project = require_project(slug)
    directory = brand_directory(project)
    directory.mkdir(parents=True, exist_ok=True)
    stored = directory / f"{hashlib.sha256(content).hexdigest()[:16]}{suffix}"
    if not stored.exists():
        stored.write_bytes(content)
    try:
        facts = _measure_image(stored) if kind == "image" else _measure_video(stored)
    except OperationFailed:
        stored.unlink(missing_ok=True)
        raise
    store = BrandKitStore(project.root)
    kit = store.load()
    setattr(kit, slot, BrandFile(
        path=str(stored.relative_to(project.root)).replace("\\", "/"),
        file_name=Path(file_name).name, **facts))
    store.save(kit)
    return brand_view(project, kit)


def remove_brand_file(slug: str, slot: str) -> dict[str, Any]:
    """Take a slot off the kit. The file stays: a transfer may still point at it."""
    if slot not in SLOTS:
        raise OperationFailed(f"{slot!r} is not a brand asset.")
    project = require_project(slug)
    store = BrandKitStore(project.root)
    kit = store.load()
    setattr(kit, slot, None)
    store.save(kit)
    return brand_view(project, kit)


EDITABLE = {"logo_place": Placement, "watermark_place": Placement,
            "intro_edit": ClipEdit, "outro_edit": ClipEdit}


def set_brand_options(slug: str, options: dict[str, Any]) -> dict[str, Any]:
    """Change a placement or an edit. Each is given as the fields to change;
    values outside their limits are brought inside them, never refused, so a
    slider dragged past its end saves its end."""
    project = require_project(slug)
    store = BrandKitStore(project.root)
    kit = store.load()
    for key, changes in options.items():
        if key not in EDITABLE or not isinstance(changes, dict):
            raise OperationFailed(f"{key!r} is not something that can be set on a brand asset.")
        current = getattr(kit, key).model_dump()
        unknown = [name for name in changes if name not in current]
        if unknown:
            raise OperationFailed(f"{key} has no {', '.join(unknown)}.")
        try:
            setattr(kit, key, EDITABLE[key].model_validate(current | changes))
        except ValueError as invalid:
            raise OperationFailed(f"{key} could not be set: {invalid}") from invalid
    store.save(kit)
    return brand_view(project, kit)


def brand_file_path(project, file_name: str) -> Path | None:
    directory = brand_directory(project).resolve()
    candidate = (directory / Path(file_name).name).resolve()
    return candidate if candidate.is_file() and candidate.parent == directory else None


# --- what the page shows ------------------------------------------------------------


def brand_view(project, kit: BrandKit | None = None) -> dict[str, Any]:
    from pipeline.brand_overlay import overlay_views

    kit = kit or BrandKitStore(project.root).load()
    return {
        "kit": kit.model_dump(),
        "slots": [{"key": key, "kind": kind, "name": name, "does": does}
                  for key, (kind, name, does) in SLOTS.items()],
        "limits": LIMITS, "shows": SHOWS,
        # The finished logo and watermark, and where each sits on the frame.
        "overlays": overlay_views(project, kit),
        # What the trims and cross-fades come to.
        "timing": {"intro_seconds": kit.intro_seconds, "outro_seconds": kit.outro_seconds,
                   "intro_overlap": kit.intro_edit.overlap(kit.intro),
                   "outro_overlap": kit.outro_edit.overlap(kit.outro),
                   "lesson_starts_at": kit.lesson_starts_at_ms / 1000},
    }
