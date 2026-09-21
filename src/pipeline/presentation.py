"""How an artifact is handed to a client, with the context its audit needs.

`present_artifact` is the single path: the browser, the CLI and MCP all receive
the same document, the same warnings and the same audit, because they run this
code rather than assembling a response each. They did not, briefly -- the web
routes assembled it and `operations` did not, so a script saved from the CLI came
back reporting every section as orphaned.

Two of the artifacts cannot be judged alone. A script's orphan count is
meaningless without the plan's section ids; the review's transcript comes from
the script; a timeline is only current if the plan it was built from still says
what it said. That cross-reading happens here, once.
"""

from __future__ import annotations

from typing import Any

from pipeline.composition import ClipKind, Composition, CompositionStore
from pipeline.core import OperationFailed, require_artifact, require_project
from pipeline.extraction import (
    ExtractionStore,
)
from pipeline.freshness import (
    cut_freshness,
    narration_fingerprints,
    narration_freshness,
    plan_freshness,
    source_outline,
)
from pipeline.planning import (
    Plan,
    PlanDraftStore,
    PlanStore,
)
from pipeline.projects import Project
from pipeline.rendering import (
    TITLE_CARD_MS,
)
from pipeline.review import (
    Review,
    ReviewStore,
)
from pipeline.scripting import (
    Script,
    ScriptStore,
    over_budget_warning,
)
from pipeline.stages import Stage


def present_artifact(project: Project, artifact_name: str, document: Any) -> dict[str, Any]:
    """Serialise an artifact together with the context its audit needs.

    Two of the four artifacts cannot be judged alone. A script's "orphaned" and
    "unwritten" counts are meaningless without the plan's section ids, and the
    review's transcript comes from the script. Assembling that here rather than
    in each client is the whole point of this module: the browser, the CLI and
    MCP get the same audit, because they run the same code to compute it.

    They did not, briefly. The web routes assembled it and `operations` did not,
    so a script saved from the CLI came back reporting every section as orphaned
    -- a warning that was pure noise and would have sent someone hunting a bug in
    their own data.
    """
    if artifact_name == "plan":
        extraction = ExtractionStore(project.root).load()
        freshness = plan_freshness(document, extraction)
        presented = document.to_dict()
        presented["warnings"] = [*presented["warnings"], *freshness["warnings"]]
        return presented | {
            "freshness": freshness,
            "source_outline": source_outline(extraction),
            "has_pending_draft": PlanDraftStore(project.root).load() is not None,
        }

    if artifact_name == "script":
        plan = PlanStore(project.root).load()
        section_ids = [section.id for section in plan.sections]
        budgets = {section.id: section.estimated_seconds for section in plan.sections}
        titles = {section.id: section.title for section in plan.sections}
        ordered = document.in_plan_order(section_ids)
        presented = ordered.to_dict(section_ids, budgets, titles)

        extraction = ExtractionStore(project.root).load()
        out_of_date = narration_freshness(plan, ordered, extraction)
        if out_of_date:
            presented["warnings"] = [*presented["warnings"], (
                f"{len(out_of_date)} section(s) were written against an earlier version "
                f"of their plan section or source content"
            )]

        return presented | {
            # Everything the writer needs next to the editor. The page used to get
            # a title and a summary, so narration was written without the target
            # length, the objectives or the source it was meant to come from.
            "plan_sections": [
                section.model_dump(mode="json", include={
                    "id", "title", "summary", "estimated_seconds", "sources",
                    "rendering_approach", "rendering_reason", "objective_ids",
                })
                for section in plan.sections
            ],
            "plan_objectives": [
                {"id": o.id, "text": o.text}
                for o in plan.learning_objectives if o.is_included
            ],
            "selected_audience": plan.selected_audience,
            "out_of_date": out_of_date,
            "comments_by_section": _open_comments_by_section(project, plan, Stage.SCRIPT_STAGING),
            "measured_seconds": _measured_narration_seconds(project, plan),
        }

    if artifact_name == "review":
        plan = PlanStore(project.root).load()
        script = ScriptStore(project.root).load()
        presented = document.to_dict()
        # Reviewing is the last gate before export, so it repeats what Scripting
        # found about length. A review reading "no warnings" over a section half
        # as long again as planned was how that went unnoticed.
        budget_audit = script.audit(
            [section.id for section in plan.sections],
            {section.id: section.estimated_seconds for section in plan.sections},
            {section.id: section.title for section in plan.sections},
        )
        # Chapters are what a viewer navigates by, so a chapter naming a section
        # the plan no longer has is the same defect as a stale timeline: the cut
        # describes work that was abandoned.
        planned_titles = {s.title.strip() for s in plan.sections if s.title.strip()}
        stale_chapters = [
            chapter.title for chapter in document.chapters
            if chapter.title.strip() and chapter.title.strip() not in planned_titles
        ]
        presented["warnings"] = [
            *presented["warnings"],
            *(over_budget_warning(section) for section in budget_audit["over_budget"]),
            *([
                f"{len(stale_chapters)} chapter(s) name sections that are not in the plan "
                f"any more: {', '.join(stale_chapters[:3])}"
                f"{'…' if len(stale_chapters) > 3 else ''}. This cut was made from a "
                f"different script."
            ] if stale_chapters else []),
            *cut_freshness(plan, CompositionStore(project.root).load())["warnings"],
        ]
        return presented | {
            "plan_sections": [
                {"id": s.id, "title": s.title, "estimated_seconds": s.estimated_seconds}
                for s in plan.sections
            ],
            "transcript": [
                {
                    "section_id": section.id,
                    "title": section.title,
                    "body": script.spoken_text(section.id),
                    # Measured from the render when there is one. Computing these
                    # in the page from `estimated_seconds` put the last line of an
                    # 8-minute video 109 seconds from where it is actually spoken.
                    "start_ms": start_ms,
                }
                for section, start_ms in zip(
                    plan.sections, section_start_times(project, plan), strict=False
                )
            ],
        }

    if artifact_name == "composition":
        plan = PlanStore(project.root).load()
        freshness = cut_freshness(plan, document)
        presented = document.to_dict()
        presented["warnings"] = [*presented.get("warnings", []), *freshness["warnings"]]
        return presented | {"freshness": freshness}

    return document.to_dict()

def read_artifact(slug: str, artifact_name: str) -> dict[str, Any]:
    """The artifact as the UI sees it: values plus audit plus warnings."""
    project = require_project(slug)
    binding = require_artifact(artifact_name)
    return present_artifact(project, artifact_name, binding.store(project).load())

def write_artifact(slug: str, artifact_name: str, values: dict[str, Any]) -> dict[str, Any]:
    """Replace an artifact wholesale from a plain dict.

    Validation is the model's, not this function's -- the same clamping and
    trimming an edit from the browser goes through. A caller that sends a
    40-hour section gets it clamped and flagged in `warnings`, not rejected,
    because losing the rest of a large edit over one bad number is worse.
    """
    # Resolved here so an unknown project fails before the payload is parsed.
    require_project(slug)
    binding = require_artifact(artifact_name)

    try:
        document = binding.model_type.model_validate(values)
    except Exception as validation_failure:
        raise OperationFailed(
            f"That is not a valid {artifact_name}: {validation_failure}"
        ) from validation_failure

    return save_artifact(slug, artifact_name, document)

def save_artifact(slug: str, artifact_name: str, document: Any) -> dict[str, Any]:
    """Persist an already-validated artifact from a client.

    The single write path for every client, so the rules below cannot be skipped
    by picking a different interface. The web routes used to call the stores
    directly and bypassed exactly this.
    """
    project = require_project(slug)
    binding = require_artifact(artifact_name)
    _mark_as_hand_edited(document)
    if artifact_name == "script":
        document = _script_in_plan_order(project, document)
        _stamp_rewritten_narration(project, document)
    return present_artifact(project, artifact_name, binding.store(project).save(document))

def _script_in_plan_order(project: Project, script: Script) -> Script:
    """Stored in plan order, so the file reads the way the video plays."""
    plan = PlanStore(project.root).load()
    return script.in_plan_order([section.id for section in plan.sections])

def _mark_as_hand_edited(document: Any) -> None:
    """Clear the "a render wrote this" markers on any write from a client.

    Every client sends the whole document back, markers included, so without
    this an edited timeline still claimed to be the renderer's and the next
    render replaced it. The renderer sets the markers again itself, after it
    writes.
    """
    if isinstance(document, Composition):
        document.generated_from_render_at = ""
        document.generated_fingerprint = ""
    elif isinstance(document, Review):
        document.chapters_generated_from_render_at = ""

def _stamp_rewritten_narration(project: Project, script: Script) -> None:
    """Record what each section's narration was written against, when it changes.

    Only sections whose words or briefs actually changed are stamped: saving the
    whole script after editing one section must not declare every other section
    freshly checked against the current plan.
    """
    plan = PlanStore(project.root).load()
    sections = {section.id: section for section in plan.sections}
    extraction = ExtractionStore(project.root).load()
    stored = {s.section_id: s for s in ScriptStore(project.root).load().section_scripts}

    for section_script in script.section_scripts:
        section = sections.get(section_script.section_id)
        if section is None:
            continue
        before = stored.get(section_script.section_id)
        content_now = [(s.narration.strip(), s.brief) for s in section_script.scenes]
        content_before = [(s.narration.strip(), s.brief) for s in before.scenes] if before else []
        if content_now != content_before and section_script.body.strip():
            section_script.written_from = narration_fingerprints(section, extraction)

def _open_comments_by_section(project: Project, plan: Plan, stage: Stage) -> dict[str, list]:
    """Open review comments routed to a stage, placed on the section they fall in.

    Placed by time: a comment is anchored where it was made in the video, and
    each section starts where its title card does (measured once rendered).
    """
    review = ReviewStore(project.root).load()
    routed = [c for c in review.comments if c.is_open and c.routed_to_stage is stage]
    if not routed or not plan.sections:
        return {}

    starts = section_start_times(project, plan)
    placed: dict[str, list] = {}
    for comment in sorted(routed, key=lambda c: c.at_ms):
        index = max((i for i, start in enumerate(starts) if start <= comment.at_ms), default=0)
        placed.setdefault(plan.sections[index].id, []).append({
            "id": comment.id, "author": comment.author, "body": comment.body,
            "at_ms": comment.at_ms,
        })
    return placed

def _measured_narration_seconds(project: Project, plan: Plan) -> dict[str, float]:
    """How long each section's narration actually ran in the last render.

    Only while the Studio timeline is still the render's own: once someone edits
    it, its clips no longer say how long the render was, and a stale number is
    worse than none.
    """
    from pipeline.composition import TrackKind

    composition = CompositionStore(project.root).load()
    if not composition.generated_from_render_at:
        return {}

    starts = section_start_times(project, plan)
    audio_clips = [
        clip for track in composition.tracks if track.kind is TrackKind.AUDIO
        for clip in track.clips
    ]
    by_section = {clip.section_id: clip for clip in audio_clips if clip.section_id}

    measured = {}
    for section, start in zip(plan.sections, starts, strict=False):
        clip = by_section.get(section.id)
        if clip is None:
            # A timeline written before clips recorded their section. Its
            # narration sat one title card in, because every section had one.
            clip = next((c for c in audio_clips if c.start_ms == start + TITLE_CARD_MS), None)
        if clip is not None:
            measured[section.id] = round(clip.duration_ms / 1000, 1)
    return measured

def section_start_times(project: Project, plan) -> list[int]:
    """Where each plan section begins in the finished video.

    From the render's title cards when one exists -- those are measured. Before
    a render, the plan's estimates are the only answer available, and they are
    a guess made before a word was spoken.
    """
    from pipeline.composition import TrackKind

    composition = CompositionStore(project.root).load()
    if composition.generated_from_render_at:
        scenes = sorted(
            (
                clip
                for track in composition.tracks if track.kind is TrackKind.VIDEO
                for clip in track.clips if clip.kind is ClipKind.SCENE
            ),
            key=lambda clip: clip.start_ms,
        )
        # A section begins at its first scene. The video track carries one clip
        # per scene, so counting clips would say a four-scene section is four
        # sections; the clip says which section it belongs to instead.
        earliest: dict[str, int] = {}
        for clip in scenes:
            if clip.section_id and clip.section_id not in earliest:
                earliest[clip.section_id] = clip.start_ms
        if plan.sections and all(section.id in earliest for section in plan.sections):
            return [earliest[section.id] for section in plan.sections]
        # A timeline written before clips recorded their section: it had exactly
        # one clip per section, so their order is the answer.
        if len(scenes) == len(plan.sections):
            return [clip.start_ms for clip in scenes]

    starts: list[int] = []
    running_ms = 0
    for section in plan.sections:
        starts.append(running_ms)
        running_ms += section.estimated_seconds * 1000
    return starts
