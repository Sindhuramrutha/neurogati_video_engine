"""Generation — turning each scene's brief into something to look at.

Script & Staging writes, for every scene, what should be on screen while it is
said. Nothing ever read those sentences. The video showed whatever picture the
section happened to have, held still for as long as the words lasted, which is
the shape of every "AI narration over slides" tool and is not worth a pipeline.

This stage is the missing step between deciding what to show and cutting it
together. Per scene it produces one *shot*: a picture, and how the camera moves
over it.

Four ways a shot can be made, in the order they are preferred:

1. **From the source.** A diagram the author drew, matched to the scene by the
   section's own sources. Always first: the author's figure beats anything
   generated from a description of it.
2. **A chart.** When the plan says this section is shown as a plot and the source
   has numbers in it, the numbers are drawn -- from the source's own values, not
   from an impression of them.
3. **Generated.** An image model draws the brief when there is nothing to show.
   Recorded as generated, with the prompt kept, because a picture nobody can
   trace is a claim nobody can check.
4. **Words.** No picture at all, typeset on the project's own background. Not a
   failure -- some scenes are a definition, and a decorative image would be
   worse than none.

Motion is part of the shot, not a post-process: a still held for eleven seconds
reads as a slide, and the same picture pushed in slowly reads as a film. The
motion is deliberately small -- a push in, a slow pan -- because motion that
competes with the narration is worse than none.

Stored at `projects/<slug>/generation/visuals.json`, with the pictures it makes
in `generation/assets/`.
"""

from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from pipeline.on_screen import (
    MAXIMUM_HEADLINE_LENGTH,
    MAXIMUM_POINT_LENGTH,
    MAXIMUM_POINTS,
)
from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MAXIMUM_VISUALS = 500
MAXIMUM_PROMPT_LENGTH = 2_000
MAXIMUM_PARALLEL_IMAGE_CALLS = 4
MAXIMUM_PARALLEL_COMPOSITIONS = 6
MAXIMUM_PARALLEL_DIAGRAMS = 3

# Speech, for guessing how long a scene lasts before it has been spoken.
WORDS_PER_SECOND = 150 / 60



# Numbers with a unit or a percent, as a source states them: "50 microvolts",
# "1,000 Hz", "38%". A bare year or a section number is not a data point.
NUMBER_IN_TEXT = re.compile(
    r"(-?\d[\d,]*\.?\d*)\s*(%|percent|hz|khz|mhz|ms|s\b|mv|µv|uv|microvolts?|volts?|"
    r"db|px|kb|mb|gb|x\b)", re.IGNORECASE)


class VisualKind:
    # The source's own slide, drawn as its author designed it. First in the list
    # because it beats every other option: nothing this pipeline composes is
    # better than the thing somebody already made.
    SLIDE = "slide"

    SOURCE_PICTURE = "source_picture"
    CHART = "chart"
    DIAGRAM = "diagram"
    GENERATED_IMAGE = "generated_image"
    TEXT = "text"


class Motion:
    """How the camera moves over a shot.

    Small on purpose. A push that crosses the frame in eight seconds reads as
    deliberate; one that crosses it in two reads as a screensaver.
    """

    HOLD = "hold"
    PUSH_IN = "push_in"
    PULL_BACK = "pull_back"
    PAN_RIGHT = "pan_right"
    PAN_LEFT = "pan_left"

    ALL = (HOLD, PUSH_IN, PULL_BACK, PAN_RIGHT, PAN_LEFT)


class SceneVisual(BaseModel):
    """One scene's shot: what is shown, where it came from, how it moves."""

    # Building a scene sets these fields one at a time; the caps below have to
    # hold for a headline assigned afterwards exactly as for one passed in.
    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=new_identifier)
    section_id: str = ""
    section_title: str = ""
    scene_id: str = ""
    scene_number: int = 0

    # Copied from the scene so a rewritten brief is detectable without holding
    # the script open beside this.
    brief: str = ""
    narration_preview: str = ""
    brief_fingerprint: str = ""

    kind: str = VisualKind.TEXT
    asset_path: str = ""          # relative to the project root
    origin: str = "none"          # source | chart | diagram | generated | none
    prompt: str = ""              # for a generated picture: exactly what was asked
    motion: str = Motion.HOLD
    note: str = ""
    built_at: str = ""

    # What the viewer reads. Not the narration: the words are already being
    # spoken, and printing them again is the single thing that makes a video
    # read as slides with a voice over them. A headline of a few words and two
    # or three labels is what a person can take in while listening.
    headline: str = ""
    points: list[str] = Field(default_factory=list)

    # A diagram as data, when the scene is about a sequence or a comparison.
    # Whatever draws it cannot add a step, because the steps are these.
    diagram: dict[str, Any] | None = None

    # An animated clip, when a renderer that can animate is installed. The still
    # stays in `asset_path` either way, so a project that loses its animator
    # still renders.
    clip_path: str = ""
    drawn_by: str = ""

    # Which slide of the source deck this scene shows, 1-based, or 0 for a scene
    # that is not a slide. What makes a deck-driven video follow the deck.
    slide_number: int = 0

    @field_validator("headline")
    @classmethod
    def _cap_headline(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_HEADLINE_LENGTH]

    @field_validator("points")
    @classmethod
    def _cap_points(cls, value: list[str]) -> list[str]:
        return [point.strip()[:MAXIMUM_POINT_LENGTH]
                for point in value if point.strip()][:MAXIMUM_POINTS]

    @field_validator("prompt")
    @classmethod
    def _cap_prompt(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_PROMPT_LENGTH]

    @field_validator("motion")
    @classmethod
    def _known_motion(cls, value: str) -> str:
        return value if value in Motion.ALL else Motion.HOLD

    @property
    def is_built(self) -> bool:
        """Whether this scene has what it needs to be drawn.

        Every scene needs its words; only some need a file. A text scene with no
        headline is not built -- it would fall back to printing the narration,
        which is what this stage exists to stop.
        """
        if not self.headline:
            return False
        return self.kind == VisualKind.TEXT or bool(self.asset_path or self.clip_path)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump() | {"is_built": self.is_built}


class VisualPlan(BaseModel):
    visuals: list[SceneVisual] = Field(default_factory=list)
    planned_at: str = ""
    built_at: str = ""
    notes: list[str] = Field(default_factory=list)

    @field_validator("visuals")
    @classmethod
    def _cap_visuals(cls, value: list[SceneVisual]) -> list[SceneVisual]:
        return value[:MAXIMUM_VISUALS]

    def for_section(self, section_id: str) -> list[SceneVisual]:
        return [visual for visual in self.visuals if visual.section_id == section_id]

    def audit(self) -> dict[str, Any]:
        return {
            "scene_count": len(self.visuals),
            "built_count": sum(1 for v in self.visuals if v.is_built),
            "slides": sum(1 for v in self.visuals if v.kind == VisualKind.SLIDE),
            "from_source": sum(1 for v in self.visuals if v.kind == VisualKind.SOURCE_PICTURE),
            "charts": sum(1 for v in self.visuals if v.kind == VisualKind.CHART),
            "generated": sum(1 for v in self.visuals if v.kind == VisualKind.GENERATED_IMAGE),
            "diagrams": sum(1 for v in self.visuals if v.kind == VisualKind.DIAGRAM),
            "animated": sum(1 for v in self.visuals if v.clip_path),
            "words_only": sum(1 for v in self.visuals if v.kind == VisualKind.TEXT),
            "moving": sum(1 for v in self.visuals if v.motion != Motion.HOLD),
        }

    def to_dict(self, stale_ids: set[str] | None = None) -> dict[str, Any]:
        stale = stale_ids or set()
        audit = self.audit()
        warnings: list[str] = []
        unbuilt = [v for v in self.visuals if not v.is_built]
        if unbuilt:
            warnings.append(
                f"{len(unbuilt)} scene(s) have nothing to show yet. Build the visuals, "
                f"or they fall back to their words on screen."
            )
        if stale:
            warnings.append(
                f"{len(stale)} scene(s) were rewritten after their visual was made."
            )
        return {
            "visuals": [
                visual.to_dict() | {"is_stale": visual.id in stale} for visual in self.visuals
            ],
            "planned_at": self.planned_at,
            "built_at": self.built_at,
            "notes": self.notes,
            "audit": audit,
            "warnings": warnings,
            "is_empty": not self.visuals,
        }


def default_visual_plan() -> VisualPlan:
    return VisualPlan()


class VisualPlanStore(JsonDocumentStore[VisualPlan]):
    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.GENERATION),
            model_type=VisualPlan,
            build_default=default_visual_plan,
            description="scene visuals",
        )


def brief_fingerprint(brief: str, narration: str) -> str:
    """What the shot was made for. A rewritten scene should not keep a picture
    of what it used to say."""
    material = f"{brief.strip()}\n{narration.strip()}".encode()
    return hashlib.sha256(material).hexdigest()[:16]


def numbers_in(text: str) -> list[tuple[float, str, str]]:
    """Every stated quantity, as (value, unit, the words around it).

    Used to decide whether a chart is possible at all: a section with one number
    in it has nothing to plot, and inventing the rest is the one thing this
    pipeline must never do.
    """
    found: list[tuple[float, str, str]] = []
    for match in NUMBER_IN_TEXT.finditer(text):
        try:
            value = float(match.group(1).replace(",", ""))
        except ValueError:
            continue
        start = max(0, match.start() - 40)
        found.append((value, match.group(2).lower(), text[start:match.end()].strip()))
    return found


# --- deciding what each scene shows --------------------------------------------------


# A chart needs enough stated quantities to be a chart. Two numbers is a
# sentence; five is a shape.
SMALLEST_CHART = 3

CHART_WIDTH, CHART_HEIGHT = 1200, 900

IMAGE_STYLE = (
    "A clear, simple diagram for an educational video. Flat vector style, plain "
    "white background, strong contrast, large legible labels, no watermark, no "
    "signature, no photographic texture, no text other than the labels named."
)


def _motion_for(kind: str, scene_number: int) -> str:
    """How the camera moves over this shot.

    Alternating the direction matters more than which one starts: three scenes
    that all push in read as one long zoom, and the eye stops believing the cut.
    A chart holds still -- panning across numbers makes them harder to read, and
    the numbers are the point.
    """
    if kind == VisualKind.CHART:
        return Motion.HOLD
    if kind == VisualKind.TEXT:
        return Motion.HOLD
    if kind == VisualKind.SLIDE:
        # A slow push and nothing else. The slide is a finished composition, and
        # panning across one crops the author's layout.
        return Motion.PUSH_IN
    return (Motion.PUSH_IN, Motion.PAN_RIGHT, Motion.PULL_BACK, Motion.PAN_LEFT)[
        scene_number % 4
    ]


def _prompt_for(section, scene_brief: str, narration: str, source_text: str) -> str:
    """What an image model is asked for, built from the scene's own words."""
    parts = [
        f"Draw what this scene shows: {scene_brief.strip() or narration.strip()[:200]}",
        f"It illustrates a section titled: {section.title}." if section.title else "",
        f"The narration says: {narration.strip()[:400]}" if narration.strip() else "",
        f"The source material says: {source_text[:600]}" if source_text else "",
        "Show only what those words support. Do not invent numbers, data points "
        "or labels that are not in them.",
        IMAGE_STYLE,
    ]
    return "\n".join(part for part in parts if part)


def plan_visuals(slug: str) -> dict[str, Any]:
    """Decide what every scene shows, keeping the decisions already made.

    Nothing is produced here and no model is called: this is the cheap pass that
    says what each scene *would* show, so the expensive one can be reviewed
    first. A scene whose brief has since been rewritten is re-planned; one that
    has not is left exactly as it was, including a picture someone chose by hand.
    """
    from pipeline.core import OperationFailed, require_project
    from pipeline.extraction import ExtractionStore
    from pipeline.llm import is_configured
    from pipeline.plan_drafting import section_source_text
    from pipeline.plan_handoff import plan_for_later_stages
    from pipeline.plan_pictures import assets_for_later_stages
    from pipeline.render_run import pictures_for_sections
    from pipeline.slide_plan import scene_slide

    project = require_project(slug)
    plan = plan_for_later_stages(project)
    from pipeline.script_handoff import script_for_later_stages
    script = script_for_later_stages(project)
    if not plan.sections:
        raise OperationFailed("The plan has no sections, so there are no scenes to show.")

    extraction = ExtractionStore(project.root).load()
    # The section's own pictures, as the transferred plan attached them.
    library = assets_for_later_stages(project).library
    pictures = pictures_for_sections(project, plan.model_dump(mode="json"))
    can_generate = is_configured()

    store = VisualPlanStore(project.root)
    existing = {visual.scene_id: visual for visual in store.load().visuals}

    visuals: list[SceneVisual] = []
    notes: list[str] = []

    for section in plan.sections:
        entry = next(
            (s for s in script.section_scripts if s.section_id == section.id), None)
        scenes = entry.scenes if entry else []
        if not scenes:
            continue

        available = list(pictures.get(section.id, []))
        source_text, _cut = section_source_text(extraction, section.sources)
        numbers = numbers_in(source_text)

        for number, scene in enumerate(scenes):
            fingerprint = brief_fingerprint(scene.brief, scene.narration)
            was = existing.get(scene.id)
            if was is not None and was.brief_fingerprint == fingerprint:
                visuals.append(was)                      # decided already; leave it
                if was.kind == VisualKind.SOURCE_PICTURE and was.asset_path:
                    chosen = project.root / was.asset_path
                    if chosen in available:
                        available.remove(chosen)
                continue

            kind, asset_path, origin, prompt, note = VisualKind.TEXT, "", "none", "", ""
            slide_number = scene_slide(plan, section, number, len(scenes))

            if slide_number:
                # The section is a slide of the deck, so the scene shows that
                # slide. Nothing else is considered: a figure lifted out of the
                # slide and recomposed on our own background is strictly worse
                # than the slide it came from.
                kind, origin = VisualKind.SLIDE, "source"
                note = f"Slide {slide_number} of the deck"
            elif available:
                # One picture per scene while they last, so a section with four
                # diagrams shows four different things rather than one of them
                # four times.
                picture = available.pop(0)
                kind, origin = VisualKind.SOURCE_PICTURE, "source"
                asset_path = str(picture.relative_to(project.root)).replace("\\", "/")
            elif section.rendering_approach == "plot" and len(numbers) >= SMALLEST_CHART:
                kind, origin = VisualKind.CHART, "chart"
                note = f"{len(numbers)} figure(s) stated in this section's source"
            elif can_generate and section.role in ("teach", "story"):
                kind, origin = VisualKind.GENERATED_IMAGE, "generated"
                prompt = _prompt_for(section, scene.brief, scene.narration, source_text)
            else:
                note = ("No picture in the source, and no image model is configured."
                        if section.role in ("teach", "story") else "The lesson frame: words.")

            visuals.append(SceneVisual(
                id=was.id if was else new_identifier(),
                section_id=section.id, section_title=section.title,
                scene_id=scene.id, scene_number=number + 1,
                brief=scene.brief, narration_preview=scene.narration[:160],
                brief_fingerprint=fingerprint,
                kind=kind, asset_path=asset_path, origin=origin, prompt=prompt,
                motion=_motion_for(kind, number), note=note,
                slide_number=slide_number,
                built_at="" if kind != VisualKind.SOURCE_PICTURE else _now(),
            ))

    if library.figures and not library.usable():
        notes.append("Every picture in the library is skipped, so no scene uses one.")
    if not can_generate:
        notes.append("No model key is set, so nothing can be drawn for a scene "
                     "that has no picture.")

    from pipeline.scene_lab import keep_scripted
    saved = store.save(VisualPlan(
        visuals=keep_scripted(existing, visuals),
        planned_at=_now(),
        built_at=store.load().built_at,
        notes=notes,
    ))
    return saved.to_dict(_stale_visual_ids(project))


def _now() -> str:
    from datetime import UTC, datetime

    return datetime.now(UTC).isoformat(timespec="seconds")


def _stale_visual_ids(project) -> set[str]:
    """Scenes rewritten since their visual was made.

    Compared against the script rather than remembered at build time: the script
    is what the video will say, and a picture of an older sentence is exactly
    what nobody notices.
    """

    from pipeline.script_handoff import script_for_later_stages
    script = script_for_later_stages(project)
    current = {
        scene.id: brief_fingerprint(scene.brief, scene.narration)
        for entry in script.section_scripts for scene in entry.scenes
    }
    plan = VisualPlanStore(project.root).load()
    return {
        visual.id for visual in plan.visuals
        if visual.scene_id in current and current[visual.scene_id] != visual.brief_fingerprint
    }


def read_visuals(slug: str) -> dict[str, Any]:
    """What each scene shows, and which of them no longer match their scene."""
    from pipeline.core import require_project

    project = require_project(slug)
    return VisualPlanStore(project.root).load().to_dict(_stale_visual_ids(project))



# --- making them ---------------------------------------------------------------------


def draw_chart(values: list[tuple[float, str, str]], title: str, path: Path) -> None:
    """A bar chart of the quantities the source states, drawn with Pillow.

    Drawn here rather than with a plotting library because the chart has exactly
    one job -- show these numbers, at this size, in these colours -- and a
    dependency that can draw a hundred other kinds of chart is a dependency that
    can also disagree with the frame's fonts and colours.
    """
    from PIL import Image, ImageDraw

    from pipeline.rendering import _load_font

    image = Image.new("RGB", (CHART_WIDTH, CHART_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((60, 50), title[:60], font=_load_font(44, bold=True), fill=(26, 24, 22))

    shown = values[:8]
    largest = max((value for value, _unit, _context in shown), default=1) or 1
    left, bottom, top = 90, CHART_HEIGHT - 150, 160
    width = (CHART_WIDTH - left - 80) // max(1, len(shown))
    label_font = _load_font(24)

    for index, (value, unit, _context) in enumerate(shown):
        height = int((bottom - top) * (abs(value) / largest))
        x = left + index * width
        draw.rectangle([(x + 12, bottom - height), (x + width - 24, bottom)],
                       fill=(68, 114, 196))
        draw.text((x + 12, bottom - height - 34),
                  f"{value:g} {unit}".strip(), font=label_font, fill=(26, 24, 22))

    draw.line([(left, bottom), (CHART_WIDTH - 60, bottom)], fill=(26, 24, 22), width=3)
    draw.text((60, CHART_HEIGHT - 100),
              "Values as stated in the source material.",
              font=_load_font(22), fill=(92, 86, 80))
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def set_scene_visual(
    slug: str, visual_id: str, kind: str | None = None, motion: str | None = None
) -> dict[str, Any]:
    """Change what one scene shows, or how it moves."""
    from pipeline.core import OperationFailed, require_project

    project = require_project(slug)
    store = VisualPlanStore(project.root)
    plan = store.load()
    visual = next((v for v in plan.visuals if v.id == visual_id), None)
    if visual is None:
        raise OperationFailed(f"No scene visual {visual_id!r}.")

    if kind is not None:
        known = {VisualKind.SLIDE, VisualKind.SOURCE_PICTURE, VisualKind.CHART,
                 VisualKind.DIAGRAM, VisualKind.GENERATED_IMAGE, VisualKind.TEXT}
        if kind not in known:
            raise OperationFailed(f"{kind!r} is not a kind of visual. One of: {sorted(known)}.")
        if kind != visual.kind:
            # The old picture is not this scene's any more; it is not deleted,
            # because the same file may be another scene's source figure.
            visual.kind = kind
            visual.asset_path = visual.clip_path = visual.drawn_by = visual.built_at = ""
            visual.origin = {"source_picture": "source", "chart": "chart",
                             "diagram": "diagram",
                             "generated_image": "generated"}.get(kind, "none")
    if motion is not None:
        visual.motion = motion

    return store.save(plan).to_dict(_stale_visual_ids(project))
