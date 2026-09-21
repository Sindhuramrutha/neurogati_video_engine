"""Making what each scene shows.

The other half of Generation. `generation.py` decides -- what kind of thing each
scene is, and which of the source's pictures it gets -- and this produces it:
slides composed from the deck, the source's own figures animated, diagrams drawn
from their nodes, charts from stated numbers, pictures from an image model.

The split is along a real seam. Deciding is cheap, calls no model and is meant
to be reviewed before anything is paid for; making is slow, calls models and
subprocesses, and fails in ways that must not take the rest of the video with
them. Keeping them in one module meant one 240-line function doing five
different kinds of work.

Every pass has the same shape -- take the scenes of one kind, make them, return
the ids it built -- so adding a kind is adding a pass, and a scene that cannot
be made is reported against itself and leaves the others alone.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pipeline.generation import (
    MAXIMUM_PARALLEL_COMPOSITIONS,
    MAXIMUM_PARALLEL_DIAGRAMS,
    MAXIMUM_PARALLEL_IMAGE_CALLS,
    SMALLEST_CHART,
    WORDS_PER_SECOND,
    Motion,
    SceneVisual,
    VisualKind,
    VisualPlanStore,
    _now,
    _stale_visual_ids,
    draw_chart,
    numbers_in,
)
from pipeline.on_screen import (
    compose_on_screen,
    draw_diagram,
    fallback_headline,
    spec_from_plan,
)

logger = logging.getLogger(__name__)


@dataclass
class Workshop:
    """Everything the making passes share, gathered once.

    Read here rather than inside the workers: every scene of a section shares
    its source text, and a dict filled from six threads is a race for no gain.

    It also carries `notes`, which is how a pass reports a scene it could not
    make without stopping the others -- one unavailable model call should not
    cost a whole video.
    """

    project: Any
    assets: Path
    style: Any
    narrations: dict[str, str]
    source_texts: dict[str, str]

    # The scene kinds this machine has proved it can draw, and which renderer
    # draws each. Composing a formula scene where nothing can typeset one
    # produces a still of a formula, which is worse than the flow that would
    # otherwise have been composed.
    offered: dict[str, str]
    by_renderer: dict[str, str]

    notes: list[str] = field(default_factory=list)

    def narration_of(self, visual: SceneVisual) -> str:
        return self.narrations.get(visual.scene_id, visual.narration_preview)

    def spoken_ms(self, visual: SceneVisual) -> int:
        return _spoken_milliseconds(self.narrations.get(visual.scene_id, ""))

    def source_of(self, visual: SceneVisual) -> str:
        return self.source_texts.get(visual.section_id, "")

    def blame(self, visual: SceneVisual, said: str) -> None:
        """Report a failure against the scene it happened to."""
        self.notes.append(f"Scene {visual.scene_number} of {visual.section_title}: {said}")


def build_visuals(slug: str, rebuild: bool = False) -> dict[str, Any]:
    """Compose what every scene shows, then produce it.

    Two kinds of work, in order, because they fail differently. First the
    words: every scene gets a headline and up to four labels, composed from its
    brief -- a scene without them falls back to printing the narration, which is
    the thing this stage exists to stop. Then the pictures, one pass per kind.

    Each pass takes the scenes it recognises, makes them, and returns the ids it
    built. A scene it cannot make is reported against itself and leaves the rest
    alone.
    """
    from pipeline.core import OperationFailed, require_project

    project = require_project(slug)
    store = VisualPlanStore(project.root)
    plan = store.load()
    if not plan.visuals:
        raise OperationFailed("Nothing is planned yet. Plan the visuals first.")

    stale = _stale_visual_ids(project)
    wanted = [
        visual for visual in plan.visuals
        if rebuild or visual.id in stale or not visual.is_built
    ]
    if not wanted:
        return plan.to_dict(stale) | {"built_ids": [], "notes": [
            "Every scene already has what it shows."]}

    shop = _workshop_for(project, wanted)
    _compose_the_words(wanted, shop, rebuild=rebuild, stale=stale)

    # Anything without a file yet. Asked once, after the words, because
    # composing can change a scene's kind -- a scene that turns out to have a
    # shape stops being words and starts needing a picture.
    to_build = [
        visual for visual in wanted
        if rebuild or visual.id in stale or not (visual.asset_path or visual.clip_path)
    ]
    animatable = [
        visual for visual in wanted
        if rebuild or visual.id in stale or not visual.clip_path
    ]

    built = [
        *_make_slides(_of_kind(to_build, VisualKind.SLIDE), shop),
        *_make_figures(_of_kind(animatable, VisualKind.SOURCE_PICTURE), shop),
        *_make_diagrams(_of_kind(to_build, VisualKind.DIAGRAM), shop),
        *_make_charts(_of_kind(to_build, VisualKind.CHART), shop),
        *_make_images(_of_kind(to_build, VisualKind.GENERATED_IMAGE), shop),
    ]

    plan.built_at = _now()
    plan.notes = shop.notes
    saved = store.save(plan)
    return saved.to_dict(_stale_visual_ids(project)) | {
        "built_ids": built, "notes": shop.notes,
    }


def _of_kind(visuals: list[SceneVisual], kind: str) -> list[SceneVisual]:
    return [visual for visual in visuals if visual.kind == kind]


def _workshop_for(project, wanted: list[SceneVisual]) -> Workshop:
    """Read everything the passes need, once."""
    from pipeline.extraction import ExtractionStore
    from pipeline.plan_drafting import section_source_text
    from pipeline.planning import PlanStore
    from pipeline.render_run import render_style_for
    from pipeline.scene_renderers import SCENE_KINDS, drawable_kinds
    from pipeline.scripting import ScriptStore

    script = ScriptStore(project.root).load()
    sections = {s.id: s for s in PlanStore(project.root).load().sections}
    extraction = ExtractionStore(project.root).load()

    source_texts: dict[str, str] = {}
    for section_id in {visual.section_id for visual in wanted}:
        section = sections.get(section_id)
        text, _cut = section_source_text(extraction, section.sources if section else [])
        source_texts[section_id] = text

    assets = project.root / "generation" / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    by_renderer = drawable_kinds()
    # `figure` is not offered to the composer: whether a scene shows the
    # source's own picture is decided by what was extracted, not by a model.
    offered = {kind: SCENE_KINDS[kind] for kind in by_renderer
               if kind in SCENE_KINDS and kind != "figure"}

    shop = Workshop(
        project=project,
        assets=assets,
        style=render_style_for(project),
        narrations={scene.id: scene.narration
                    for entry in script.section_scripts for scene in entry.scenes},
        source_texts=source_texts,
        offered=offered,
        by_renderer=by_renderer,
    )
    if not offered:
        shop.notes.append(
            "No scene renderer is available, so nothing is animated. "
            "Install one from Generation to have diagrams build on screen."
        )
    return shop


# --- what the viewer reads ------------------------------------------------------------


def _compose_the_words(
    visuals: list[SceneVisual], shop: Workshop, *, rebuild: bool, stale: set[str]
) -> None:
    """Give every scene a headline and its labels.

    Several at a time, because each is a round trip of its own. A scene whose
    call fails keeps a headline taken from its brief rather than losing one:
    with no headline at all the frame falls back to the narration.
    """
    from concurrent.futures import ThreadPoolExecutor

    from pipeline.llm import ModelCallFailed, ModelNotConfigured

    # A slide carries its own words, so nothing is composed for it: its headline
    # is the deck's own heading, verbatim, and its labels stay empty because the
    # slide already has its text where the author put it.
    for visual in visuals:
        if visual.kind == VisualKind.SLIDE and not visual.headline:
            visual.headline = visual.section_title
            visual.points = []

    unwritten = [
        visual for visual in visuals
        if visual.kind != VisualKind.SLIDE
        and (rebuild or visual.id in stale or not visual.headline)
    ]
    if not unwritten:
        return

    def compose(visual: SceneVisual):
        try:
            return visual, compose_on_screen(
                visual.section_title, visual.brief, shop.narration_of(visual),
                shop.source_of(visual), shop.offered), ""
        except (ModelCallFailed, ModelNotConfigured) as failure:
            return visual, None, str(failure)

    workers = min(MAXIMUM_PARALLEL_COMPOSITIONS, len(unwritten))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for visual, composed, failure in pool.map(compose, unwritten):
            fallback = fallback_headline(visual.brief, shop.narration_of(visual))
            if composed is None:
                shop.blame(visual, failure)
                visual.headline = visual.headline or fallback
                continue
            visual.headline = composed.headline.strip() or fallback
            visual.points = composed.points
            _take_the_shape(visual, composed, shop)


def _take_the_shape(visual: SceneVisual, composed, shop: Workshop) -> None:
    """Record the shape the composer found, and switch the scene to it.

    A scene drawn from the source's own terms beats an image model's impression
    of one: it can be checked against the source, and it can be built up while
    it is described. So a shape displaces words or a generated picture -- but
    never the source's own figure, and never a slide.
    """
    spec = spec_from_plan(composed, visual.headline, shop.offered)
    visual.diagram = spec.to_dict() if spec else None
    if spec and visual.kind in {VisualKind.TEXT, VisualKind.GENERATED_IMAGE}:
        visual.kind, visual.origin = VisualKind.DIAGRAM, "diagram"
        visual.asset_path, visual.clip_path, visual.drawn_by = "", "", ""
        visual.motion = Motion.HOLD


# --- making the pictures --------------------------------------------------------------


def _make_slides(visuals: list[SceneVisual], shop: Workshop) -> list[str]:
    """Compose each slide these scenes need, once, and point them at it.

    Once per slide, not once per scene: a slide narrated in three beats is three
    scenes showing the same frame, and drawing a 3840-wide background three
    times is work nobody asked for.

    A slide that cannot be drawn keeps its scene rather than losing it -- the
    scene falls back to its words on screen, and the reason is reported. A deck
    of forty slides must not lose the whole video to one unreadable shape.
    """
    from pipeline.assets import AssetLibraryStore
    from pipeline.slide_frame import cached_slide_path, compose_slide

    wanted = [visual for visual in visuals if visual.slide_number]
    if not wanted:
        return []

    wash = AssetLibraryStore(shop.project.root).load().look.slide_wash
    directory = shop.project.root / "generation" / "slides"
    built: list[str] = []
    drawn: dict[tuple[str, int], str] = {}
    notes_by_slide: dict[tuple[str, int], str] = {}

    for visual in sorted(wanted, key=lambda v: v.slide_number):
        deck = _deck_for(shop.project, visual)
        if deck is None:
            visual.kind, visual.origin = VisualKind.TEXT, "none"
            visual.note = "The source deck is no longer in this project."
            shop.notes.append(f"slide {visual.slide_number}: its deck is missing")
            continue

        key = (deck.name, visual.slide_number)
        if key not in drawn:
            target = cached_slide_path(directory, deck, visual.slide_number)
            try:
                composed = compose_slide(deck, visual.slide_number, target, wash=wash)
            except Exception as unreadable:
                logger.warning("slide %s could not be drawn: %s",
                               visual.slide_number, unreadable)
                shop.notes.append(
                    f"slide {visual.slide_number} could not be drawn: {unreadable}")
                visual.kind, visual.origin = VisualKind.TEXT, "none"
                visual.note = f"This slide could not be drawn: {unreadable}"
                continue
            drawn[key] = _stored(shop.project, composed.path)
            notes_by_slide[key] = composed.notes[0] if composed.notes else ""

        # Set either way, so a note from an earlier build with different
        # settings does not outlive the settings that produced it.
        visual.note = notes_by_slide.get(key, "")
        visual.asset_path = drawn[key]
        visual.built_at = _now()
        built.append(visual.id)

    return built


def _make_figures(visuals: list[SceneVisual], shop: Workshop) -> list[str]:
    """The author's own pictures, with each scene's labels arriving beside them.

    A source figure used to be a still held for as long as its words lasted. It
    is the most trustworthy thing in the video -- somebody drew it for this
    material -- and it is the last thing that should sit motionless. Nothing is
    drawn on top of it: where a label belongs *inside* a scanned diagram is not
    something anything here has measured.
    """
    from concurrent.futures import ThreadPoolExecutor

    from pipeline.scene_renderers import DiagramSpec, render_animated_diagram

    if "figure" not in shop.by_renderer:
        return []
    wanted = [
        visual for visual in visuals
        if visual.points and (shop.project.root / visual.asset_path).exists()
    ]
    if not wanted:
        return []

    def build(visual: SceneVisual) -> str:
        spec = DiagramSpec(
            kind="figure", caption=visual.headline, nodes=list(visual.points),
            image=str(shop.project.root / visual.asset_path),
        )
        clip = shop.assets / f"figure-{visual.id}.mp4"
        made, by = render_animated_diagram(
            spec, clip, shop.spoken_ms(visual), shop.style)
        if made is None:
            return ""
        visual.clip_path = _stored(shop.project, clip)
        visual.drawn_by = by
        visual.note = f"The source's own figure, built up by {by}."
        visual.built_at = _now()
        return visual.id

    workers = min(MAXIMUM_PARALLEL_DIAGRAMS, len(wanted))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return [made for made in pool.map(build, wanted) if made]


def _make_diagrams(visuals: list[SceneVisual], shop: Workshop) -> list[str]:
    """Draw each scene's shape: a still always, and a clip where one can be made.

    Animating is a subprocess doing real work, so a few at a time and no more:
    the point of the bound is that a twenty-scene video does not start twenty
    renderers at once.
    """
    from concurrent.futures import ThreadPoolExecutor

    from pipeline.scene_renderers import DiagramSpec, render_animated_diagram

    wanted = [visual for visual in visuals if visual.diagram]
    if not wanted:
        return []

    def build(visual: SceneVisual) -> str:
        spec = DiagramSpec.from_dict(visual.diagram)
        if spec is None:
            visual.kind, visual.origin = VisualKind.TEXT, "none"
            visual.note = "The diagram had too few parts to draw; showing the words."
            return ""

        still = shop.assets / f"diagram-{visual.id}.png"
        draw_diagram(spec, still, shop.style)
        visual.asset_path = _stored(shop.project, still)

        clip = shop.assets / f"diagram-{visual.id}.mp4"
        made, by = render_animated_diagram(
            spec, clip, shop.spoken_ms(visual), shop.style)
        if made is None:
            visual.clip_path, visual.drawn_by = "", ""
            visual.note = f"Held as a still: {by}."
        else:
            visual.clip_path = _stored(shop.project, clip)
            visual.drawn_by = by
            visual.note = f"Built up on screen by {by}."
        visual.built_at = _now()
        return visual.id

    workers = min(MAXIMUM_PARALLEL_DIAGRAMS, len(wanted))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return [made for made in pool.map(build, wanted) if made]


def _make_charts(visuals: list[SceneVisual], shop: Workshop) -> list[str]:
    """Plot the quantities the source states, and only those.

    A section with two numbers in it has nothing to plot, and inventing the rest
    is the one thing this pipeline must never do -- so a scene without enough of
    them stops being a chart and shows its words.
    """
    built: list[str] = []
    for visual in visuals:
        values = numbers_in(shop.source_of(visual))
        if len(values) < SMALLEST_CHART:
            visual.note = "Not enough stated numbers to chart; showing the words."
            visual.kind = VisualKind.TEXT
            continue
        path = shop.assets / f"chart-{visual.id}.png"
        draw_chart(values, visual.section_title, path)
        visual.asset_path = _stored(shop.project, path)
        visual.built_at = _now()
        built.append(visual.id)
    return built


def _make_images(visuals: list[SceneVisual], shop: Workshop) -> list[str]:
    """Ask the image model for the scenes that have nothing else to show."""
    from concurrent.futures import ThreadPoolExecutor

    from pipeline.llm import ModelCallFailed, ModelNotConfigured, draw_image

    if not visuals:
        return []

    def draw(visual: SceneVisual):
        try:
            return visual, draw_image(visual.prompt), ""
        except (ModelCallFailed, ModelNotConfigured) as failure:
            return visual, None, str(failure)

    built: list[str] = []
    workers = min(MAXIMUM_PARALLEL_IMAGE_CALLS, len(visuals))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for visual, drawn, failure in pool.map(draw, visuals):
            if drawn is None:
                shop.blame(visual, failure)
                continue
            path = shop.assets / f"scene-{visual.id}.png"
            path.write_bytes(drawn)
            visual.asset_path = _stored(shop.project, path)
            visual.built_at = _now()
            built.append(visual.id)
    return built


def _stored(project, path: Path) -> str:
    """A made file's path as the project records it: relative, forward slashes."""
    return str(path.relative_to(project.root)).replace("\\", "/")


def _deck_for(project, visual: SceneVisual) -> Path | None:
    """The source file a slide scene came from, if it is still there."""
    from pipeline.planning import PlanStore

    plan = PlanStore(project.root).load()
    section = next((s for s in plan.sections if s.id == visual.section_id), None)
    if section is None:
        return None
    for source in section.sources:
        if not source.slide_number or not source.file_name:
            continue
        candidate = project.root / "sources" / source.file_name
        if candidate.exists():
            return candidate
    return None


def _spoken_milliseconds(narration: str) -> int:
    """About how long this narration lasts, for a diagram that must fit inside it.

    An estimate is enough: the clip is padded or cut to the real speech length
    when the video is cut. What matters is that a six-node diagram spread over
    four seconds is not built at the pace of a two-node one.
    """
    seconds = len(narration.split()) / WORDS_PER_SECOND
    return int(max(2.5, min(14.0, seconds)) * 1000)
