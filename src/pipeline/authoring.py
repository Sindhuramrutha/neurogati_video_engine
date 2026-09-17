"""The verbs that edit an artifact on someone's behalf.

Everything here is a small, complete change a client can ask for -- add a
section, write one section's narration, accept a drafted plan, route a comment
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
from pipeline.planning import (
    LearningObjective,
    Plan,
    PlanDraftStore,
    PlanSection,
    PlanStore,
)
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

def confirm_plan_matches_extraction(slug: str) -> dict[str, Any]:
    """Record that someone checked this plan against the current extraction.

    The way out of "out of date" without redrafting: the extraction changed, a
    person looked, and the plan still holds. Refused when there is nothing
    extracted to confirm against.
    """
    project = require_project(slug)
    extraction = ExtractionStore(project.root).load()
    if not extraction.documents:
        raise OperationFailed("Nothing has been extracted yet, so there is nothing to confirm.")

    store = PlanStore(project.root)
    plan = store.load()
    plan.extraction_fingerprint = extraction.content_fingerprint()
    return present_artifact(project, "plan", store.save(plan))

def read_plan_draft(slug: str) -> dict[str, Any]:
    """The pending drafted plan, with what accepting it would do."""
    project = require_project(slug)
    draft = PlanDraftStore(project.root).load()
    if draft is None:
        return {"is_pending": False}

    current = PlanStore(project.root).load()
    script = ScriptStore(project.root).load()
    narrated = {s.section_id for s in script.section_scripts if s.body.strip()}
    proposed = Plan.model_validate(draft.get("plan", {}))
    extraction = ExtractionStore(project.root).load()

    return draft | {
        "is_pending": True,
        "plan": proposed.to_dict(),
        # Accepting all replaces the sections, and narration is attached to
        # section ids: say how much written narration would be left unattached
        # before anyone clicks, not after.
        "replaces_narrated_sections": sum(1 for s in current.sections if s.id in narrated),
        "is_behind_extraction": (
            draft.get("extraction_fingerprint", "") != extraction.content_fingerprint()
        ),
    }

def accept_plan_draft(slug: str, section_ids: list[str] | None = None) -> dict[str, Any]:
    """Take a drafted plan in whole, or some of its sections.

    **All** replaces the sections, objectives and key themes, keeps the chosen
    audience, and records the extraction the draft was made from.

    **Some** appends just those sections to the current plan. Their learning
    objectives come with them -- matched by wording against the plan's own, so
    the same objective is never added twice -- and the rest of the plan is left
    exactly as it was. Partly accepting a draft is not a claim that the plan
    matches the extraction, so the plan's record of that is not changed.
    """
    project = require_project(slug)
    drafts = PlanDraftStore(project.root)
    draft = drafts.load()
    if draft is None:
        raise OperationFailed("There is no drafted plan to accept.")

    proposed = Plan.model_validate(draft.get("plan", {}))
    store = PlanStore(project.root)
    plan = store.load()

    if section_ids is None:
        plan.sections = proposed.sections
        plan.learning_objectives = proposed.learning_objectives
        plan.key_themes = proposed.key_themes or plan.key_themes
        plan.extraction_fingerprint = draft.get("extraction_fingerprint", "")
        saved = store.save(plan)
        drafts.clear()
        return present_artifact(project, "plan", saved)

    by_id = {section.id: section for section in proposed.sections}
    unknown = [sid for sid in section_ids if sid not in by_id]
    if unknown:
        raise OperationFailed(f"The draft has no section(s) {', '.join(unknown)}.")

    proposed_objectives = {o.id: o for o in proposed.learning_objectives}
    existing_by_wording = {o.text.strip().lower(): o.id for o in plan.learning_objectives}

    for section_id in section_ids:
        section = by_id[section_id].model_copy(deep=True)
        linked = []
        for objective_id in section.objective_ids:
            objective = proposed_objectives.get(objective_id)
            if objective is None:
                continue
            wording = objective.text.strip().lower()
            if wording not in existing_by_wording:
                added = LearningObjective(text=objective.text)
                plan.learning_objectives.append(added)
                existing_by_wording[wording] = added.id
            linked.append(existing_by_wording[wording])
        # A fresh id each time, so adding the same proposed section twice gives
        # two sections rather than two entries sharing one identity.
        section.id = PlanSection().id
        section.objective_ids = linked
        plan.sections.append(section)

    saved = store.save(plan)

    accepted = sorted(set(draft.get("accepted_section_ids", [])) | set(section_ids))
    if set(accepted) >= set(by_id):
        drafts.clear()
    else:
        drafts.save(draft | {"accepted_section_ids": accepted})
    return present_artifact(project, "plan", saved)

def discard_plan_draft(slug: str) -> dict[str, Any]:
    project = require_project(slug)
    return {"discarded": PlanDraftStore(project.root).clear()}

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
    project = require_project(slug)
    plan = PlanStore(project.root).load()
    known_section_ids = {section.id for section in plan.sections}

    if section_id not in known_section_ids:
        listed = ", ".join(f"{s.id} ({s.title})" for s in plan.sections) or "none"
        raise OperationFailed(
            f"The plan has no section {section_id!r}. Sections: {listed}."
        )

    store = ScriptStore(project.root)
    script = store.load()

    # One scene holding the whole body. Assigning `body` alone would be undone
    # on the next load: the scenes are the narration, and they would still hold
    # the old text.
    replacement = SectionScript(section_id=section_id, scenes=[ScriptScene(narration=body)])
    script.section_scripts = [
        s for s in script.section_scripts if s.section_id != section_id
    ] + [replacement]

    ordered = _script_in_plan_order(project, script)
    _stamp_rewritten_narration(project, ordered)
    return present_artifact(project, "script", store.save(ordered))

def confirm_section_narration(slug: str, section_id: str) -> dict[str, Any]:
    """Record that this section's narration was checked against the current plan
    and source, without changing a word of it."""
    project = require_project(slug)
    plan = PlanStore(project.root).load()
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

def section_source_material(slug: str, section_id: str) -> dict[str, Any]:
    """The full text of the content a plan section records, for reading while writing."""
    from pipeline.plan_drafting import MAXIMUM_SECTION_SOURCE_CHARACTERS

    project = require_project(slug)
    plan = PlanStore(project.root).load()
    section = next((s for s in plan.sections if s.id == section_id), None)
    if section is None:
        raise OperationFailed(f"The plan has no section {section_id!r}.")

    extraction = ExtractionStore(project.root).load()
    parts, missing = [], []
    for reference in section.sources:
        document = extraction.document(reference.file_name)
        if document is None or not document.has_location(reference.heading_path):
            missing.append(reference.label)
            continue
        parts.append({"label": reference.label,
                      "text": document.text_under(reference.heading_path)})

    total = sum(len(part["text"]) for part in parts)
    return {
        "section_id": section_id,
        "has_sources": bool(section.sources),
        "parts": parts,
        "missing": missing,
        "characters": total,
        "longer_than_an_agent_reads": total > MAXIMUM_SECTION_SOURCE_CHARACTERS,
    }

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
    from pipeline.review import Chapter

    composition = CompositionStore(project.root).load()
    if composition.generated_from_render_at:
        title_cards = [
            clip
            for track in composition.tracks if track.kind is TrackKind.VIDEO
            for clip in track.clips if clip.kind is ClipKind.SCENE
        ]
        if title_cards:
            return [
                Chapter(title=clip.text or clip.label, start_ms=clip.start_ms)
                for clip in sorted(title_cards, key=lambda c: c.start_ms)
            ]

    plan = PlanStore(project.root).load()
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
