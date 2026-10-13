"""The verbs that edit an artifact on someone's behalf.

Everything here is a small, complete change a client can ask for -- add a
section, write one section's narration, route a comment
to the stage that should fix it -- rather than "save this whole document", which
is `presentation.save_artifact`.

They are together because they share one rule: an edit is applied to the
document as it is on disk *now*, re-read inside the call, so two clients editing
different parts of the same artifact cannot overwrite each other with a copy
either of them was holding.
"""

from __future__ import annotations

from typing import Any

from pipeline.composition import Clip, ClipKind, CompositionStore
from pipeline.core import OperationFailed, require_project
from pipeline.extraction import (
    ExtractionStore,
)
from pipeline.freshness import narration_fingerprints
from pipeline.planning import PlanSection, PlanStore
from pipeline.presentation import (
    _mark_as_hand_edited,
    _script_in_plan_order,
    _stamp_rewritten_narration,
    present_artifact,
)
from pipeline.projects import Project
from pipeline.review import (
    Comment,
    ReviewStore,
    chapters_from_plan,
)
from pipeline.scripting import (
    ScriptScene,
    ScriptStore,
    SectionScript,
)
from pipeline.stages import STAGES, Stage


def clear_timeline(slug: str) -> dict[str, Any]:
    """Empty the Studio timeline so the next render builds it again.

    The hand-edit protection is right to refuse to overwrite a timeline someone
    has worked on, but it left no way out except deleting clips one at a time --
    which is how a timeline from an abandoned script survived four renders.
    """
    project = require_project(slug)
    store = CompositionStore(project.root)
    composition = store.load()
    for track in composition.tracks:
        track.clips = []
    composition.generated_from_render_at = ""
    composition.generated_fingerprint = ""
    return present_artifact(project, "composition", store.save(composition))

def add_plan_section(
    slug: str, title: str, summary: str = "", estimated_seconds: int = 60
) -> dict[str, Any]:
    project = require_project(slug)
    store = PlanStore(project.root)

    plan = store.load()
    plan.sections.append(
        PlanSection(title=title, summary=summary, estimated_seconds=estimated_seconds)
    )
    return present_artifact(project, "plan", store.save(plan))

def write_section_script(slug: str, section_id: str, body: str) -> dict[str, Any]:
    """Set the narration for one plan section, creating the entry if needed.

    Rejects a section id the plan does not have. The model would happily store
    it -- orphaned scripts are kept on purpose, so deleting a plan section does
    not destroy its writing -- but an agent inventing an id is a mistake, not an
    edit, and it should hear about it immediately rather than through a warning
    three stages later.
    """
    from pipeline.plan_handoff import plan_for_later_stages
    project = require_project(slug)
    plan = plan_for_later_stages(project)
    known_section_ids = {section.id for section in plan.sections}

    if section_id not in known_section_ids:
        listed = ", ".join(f"{s.id} ({s.title})" for s in plan.sections) or "none"
        raise OperationFailed(
            f"The plan has no section {section_id!r}. Sections: {listed}."
        )

    from pipeline.scripting import SCRIPT_WRITE

    store = ScriptStore(project.root)
    with SCRIPT_WRITE:
        script = store.load()
        # One scene holding the whole body. Assigning `body` alone would be undone
        # on the next load: the scenes are the narration, and they would still hold
        # the old text.
        replacement = SectionScript(section_id=section_id,
                                    scenes=[ScriptScene(narration=body)])
        script.section_scripts = [
            s for s in script.section_scripts if s.section_id != section_id
        ] + [replacement]
        ordered = _script_in_plan_order(project, script)
        _stamp_rewritten_narration(project, ordered)
        saved = store.save(ordered)
    return present_artifact(project, "script", saved)

def confirm_section_narration(slug: str, section_id: str) -> dict[str, Any]:
    """Record that this section's narration was checked against the current plan
    and source, without changing a word of it."""
    from pipeline.plan_handoff import plan_for_later_stages
    project = require_project(slug)
    plan = plan_for_later_stages(project)
    section = next((s for s in plan.sections if s.id == section_id), None)
    if section is None:
        raise OperationFailed(f"The plan has no section {section_id!r}.")

    store = ScriptStore(project.root)
    script = store.load()
    written = next((s for s in script.section_scripts if s.section_id == section_id), None)
    if written is None or not written.body.strip():
        raise OperationFailed("That section has no narration to confirm.")

    written.written_from = narration_fingerprints(section, ExtractionStore(project.root).load())
    return present_artifact(project, "script", store.save(_script_in_plan_order(project, script)))

def add_clip(
    slug: str,
    track_id: str,
    kind: str = "text",
    label: str = "",
    start_ms: int = 0,
    duration_ms: int = 3000,
    text: str = "",
) -> dict[str, Any]:
    project = require_project(slug)
    store = CompositionStore(project.root)
    composition = store.load()

    track = next((t for t in composition.tracks if t.id == track_id), None)
    if track is None:
        listed = ", ".join(f"{t.id} ({t.kind.value})" for t in composition.tracks) or "none"
        raise OperationFailed(f"No track {track_id!r}. Tracks: {listed}.")

    track.clips.append(
        Clip(kind=kind, label=label, start_ms=start_ms, duration_ms=duration_ms, text=text)
    )
    _mark_as_hand_edited(composition)
    return present_artifact(project, "composition", store.save(composition))

def add_review_comment(
    slug: str,
    body: str,
    author: str = "",
    at_ms: int = 0,
    routed_to_stage: str | None = None,
) -> dict[str, Any]:
    project = require_project(slug)
    store = ReviewStore(project.root)
    review = store.load()

    stage: Stage | None = None
    if routed_to_stage:
        try:
            stage = Stage(routed_to_stage)
        except ValueError as unknown_stage:
            valid = ", ".join(s.key.value for s in STAGES)
            raise OperationFailed(
                f"No stage {routed_to_stage!r} to route to. Stages: {valid}."
            ) from unknown_stage

    review.comments.append(
        Comment(body=body, author=author, at_ms=at_ms, routed_to_stage=stage)
    )
    return present_artifact(project, "review", store.save(review))

def chapters_for(project: Project) -> list:
    """Chapter marks for this project, preferring the finished video.

    A render writes its title cards onto the timeline at their **measured**
    positions, so those are where the sections actually begin. The plan's
    `estimated_seconds` are a guess made before any narration was spoken, and
    seeding from them was wrong by up to 109 seconds on an 8-minute video --
    chapter 5 pointed at 5:30 for a section that starts at 7:19. Chapters are
    navigation; navigation that lands in the wrong place is worse than none.

    Falls back to the plan's estimates when nothing has been rendered yet, which
    is the best available answer at that point.
    """
    from pipeline.composition import TrackKind
    from pipeline.plan_handoff import plan_for_later_stages
    from pipeline.review import Chapter

    composition = CompositionStore(project.root).load()
    if composition.generated_from_render_at:
        scenes = sorted(
            (clip
             for track in composition.tracks if track.kind is TrackKind.VIDEO
             for clip in track.clips if clip.kind is ClipKind.SCENE),
            key=lambda clip: clip.start_ms,
        )
        # One chapter per section, at its first clip. The video track carries a
        # clip per *scene* now, so taking a chapter from each one turned a
        # six-section video into forty-one chapters named after scenes -- and a
        # chapter list that long is not navigation.
        #
        # Grouped by the section a clip names where it has one, and otherwise by
        # a run of clips sharing a title, which is what a timeline written
        # before clips recorded their section looks like.
        chapters: list = []
        seen: set[str] = set()
        for clip in scenes:
            name = clip.text or clip.label
            key = clip.section_id or name
            if key in seen:
                continue
            seen.add(key)
            chapters.append(Chapter(title=name, start_ms=clip.start_ms))
        if chapters:
            return chapters

    plan = plan_for_later_stages(project)
    return chapters_from_plan([
        {"title": section.title, "estimated_seconds": section.estimated_seconds}
        for section in plan.sections
    ])

def seed_review_chapters(slug: str) -> dict[str, Any]:
    """Replace chapters with ones matching the rendered video, or the plan if
    nothing is rendered yet.

    Destructive and therefore never automatic on load: seeding every time
    something opened the review would discard hand-edited chapter titles.
    """
    project = require_project(slug)
    store = ReviewStore(project.root)

    review = store.load()
    review.chapters = chapters_for(project)
    return present_artifact(project, "review", store.save(review))
