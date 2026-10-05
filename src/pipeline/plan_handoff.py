"""The Scene Plan, handed on: the checks it must pass, and the transferred copy
every later stage reads.

The plan is edited on its page -- by hand, by following the deck, or by
accepting what the Scene Plan agent proposes. Later stages (the script, the
visuals, the render, the review, the export) read one plan: the one that was
**transferred**. Editing an outline mid-way never shifts a script under
someone writing it.

Before the first transfer, later stages read the working plan, as they always
did, so a project from before transfers existed keeps working unchanged. From
the first transfer on, they read only the transferred copy. The page says which.

The plan also carries Assets & Design on: each section's pictures, the brand kit
and the look are copied into the transferred plan, and every later layer reads
them from there (`plan_pictures.py`). So the plan cannot be transferred before
Assets & Design has been.

The checks are fixed rules over the plan, the transferred extraction and the
deck; none calls a model. A failing check blocks the transfer; a warning is
shown and allowed. The agent's draft is the only thing on this layer a model
makes, and it changes nothing until a person accepts it.

Stored at `planning/plan.transferred.json`.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from pipeline import upstream
from pipeline.assets_handoff import ConfirmedAssets, ConfirmedAssetStore
from pipeline.core import OperationFailed, require_project
from pipeline.extraction import ExtractionStore
from pipeline.freshness import plan_freshness
from pipeline.planning import (
    MAXIMUM_REASONABLE_SECTION_SECONDS,
    MINIMUM_REASONABLE_SECTION_SECONDS,
    Plan,
    PlanStore,
)
from pipeline.slide_plan import coverage_of, slides_in
from pipeline.stage_options import video_preferences
from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore
from pipeline.storage.layout import artifact_path

PASS, WARN, FAIL, NOT_APPLICABLE = "pass", "warn", "fail", "n/a"


class TransferredPlan(BaseModel):
    plan: Plan = Field(default_factory=Plan)
    transferred_at: str = ""
    fingerprint: str = ""
    # What Assets & Design had transferred when the plan was: the pictures its
    # sections show, the brand kit and the look. None for a plan transferred
    # before plans carried them.
    assets: ConfirmedAssets | None = None


class TransferredPlanStore(JsonDocumentStore[TransferredPlan]):
    def __init__(self, project_root) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.SCENE_PLAN).with_name(
                "plan.transferred.json"),
            model_type=TransferredPlan, build_default=TransferredPlan,
            description="transferred plan",
        )


def fingerprint(plan: Plan) -> str:
    text = json.dumps(plan.model_dump(mode="json"), sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:20]


def plan_for_later_stages(project) -> Plan:
    """The plan every stage after Scene Plan reads: the transferred one, or --
    before anything was ever transferred -- the working one."""
    transferred = TransferredPlanStore(project.root).load()
    if transferred.transferred_at:
        return transferred.plan
    return PlanStore(project.root).load()


# --- the checks ----------------------------------------------------------------------


def _check(key: str, name: str, rule: str, status: str, detail: str) -> dict[str, str]:
    return {"key": key, "name": name, "rule": rule, "status": status, "detail": detail}


def plan_checks(project, plan: Plan) -> list[dict[str, str]]:
    """Every check the plan goes through, in order, with what each found."""
    extraction = ExtractionStore(project.root).load()
    freshness = plan_freshness(plan, extraction)
    sections = plan.sections
    target = video_preferences(project.root)
    checks = []

    checks.append(_check(
        "sections", "Has sections", "At least one section",
        PASS if sections else FAIL,
        f"{len(sections)} section(s)." if sections else "The plan has no sections."))

    missing = freshness["sections_with_missing_sources"]
    checks.append(_check(
        "sources-exist", "Sources exist", "Every source a section names is in the extraction",
        FAIL if missing else PASS if sections else NOT_APPLICABLE,
        "; ".join(f"{m['title'] or 'Untitled'}: {', '.join(m['missing'])}" for m in missing)
        or "Every named source is in the extraction."))

    from pipeline.lesson_plan import (
        FRAME_ROLES,
        MOST_SQUEEZE,
        MOST_STRETCH,
        objective_suggestions,
        summary_problem,
        timing,
    )

    body = [s for s in sections if s.role not in FRAME_ROLES]
    checks.append(_check(
        "frame", "Lesson frame", "An Opening says what the viewer will learn; a Recap and a "
        "Close bring it together",
        NOT_APPLICABLE if not body else PASS if plan.lesson_frame else WARN,
        ("With " + ", ".join(p.capitalize() for p in plan.lesson_frame) + "."
         + ("" if len(plan.lesson_frame) == 3 else " The rest is switched off."))
        if plan.lesson_frame else "Switched off: the video starts and ends on the "
        "material itself. Turn it on in the Brief."))

    without = [s for s in body if not s.sources]
    checks.append(_check(
        "has-sources", "Every section has a source",
        "Each teaching section names the content it teaches (the lesson frame is written "
        "from the plan)",
        WARN if without else PASS if sections else NOT_APPLICABLE,
        f"{len(without)} section(s) name no source: "
        + ", ".join(s.title or "Untitled" for s in without[:6]) if without
        else "Every section names its source."))

    checks.append(_check(
        "extraction", "Matches the extraction",
        "Drafted or checked against the extraction as it is now",
        WARN if freshness["is_stale"] or freshness["is_unlinked"] else PASS if sections
        else NOT_APPLICABLE,
        "The extraction changed since this plan was drafted or checked."
        if freshness["is_stale"] else
        "Nothing records which extraction this plan was made from."
        if freshness["is_unlinked"] else "Made from the extraction as it is now."))

    slides = slides_in(extraction)
    follows = any(src.slide_number for s in sections for src in s.sources)
    if slides and follows:
        coverage = coverage_of(slides, sections)
        problems = []
        if coverage["missing_slides"]:
            problems.append(f"slides not covered: "
                            f"{', '.join(map(str, coverage['missing_slides'][:10]))}")
        if not coverage["is_in_order"]:
            problems.append("sections are out of the deck's order")
        checks.append(_check(
            "deck", "Follows the deck", "Every slide covered, in the deck's order",
            WARN if problems else PASS,
            "; ".join(problems).capitalize() if problems
            else f"All {coverage['slide_count']} slides, in order."))
    else:
        checks.append(_check(
            "deck", "Follows the deck", "Every slide covered, in the deck's order",
            NOT_APPLICABLE, "The plan is not built slide by slide."))

    untitled = [i + 1 for i, s in enumerate(sections) if not s.title]
    checks.append(_check(
        "titles", "Titles", "Every section has a title",
        WARN if untitled else PASS if sections else NOT_APPLICABLE,
        f"Sections without a title: {', '.join(map(str, untitled))}." if untitled
        else "Every section has a title."))

    odd = [s for s in sections if s.is_unusually_short or s.is_unusually_long]
    checks.append(_check(
        "durations", "Section lengths",
        f"Each section between {MINIMUM_REASONABLE_SECTION_SECONDS} s and "
        f"{MAXIMUM_REASONABLE_SECTION_SECONDS // 60} min",
        WARN if odd else PASS if sections else NOT_APPLICABLE,
        ", ".join(f"{s.title or 'Untitled'} ({s.estimated_seconds} s)" for s in odd[:6])
        if odd else "Every section is a sensible length."))

    shortest, longest = target.target_seconds
    total = plan.total_estimated_seconds
    checks.append(_check(
        "length", "Total length", f"Within the target duration ({target.target_phrase})",
        NOT_APPLICABLE if not sections else PASS if shortest <= total <= longest else WARN,
        f"About {round(total / 60, 1)} min planned against {target.target_phrase}."))

    included = [o for o in plan.learning_objectives if o.is_included]
    # Judged on the body: the frame links every objective by itself, and counting
    # that would say every objective is taught when none is.
    uncovered = [o.text for o in included if not any(o.id in s.objective_ids for s in body)]
    idle = [s.title or "Untitled" for s in body if not s.objective_ids]
    suggested = len(objective_suggestions(plan, extraction))
    checks.append(_check(
        "objectives", "Learning objectives",
        "At least one objective; each taught by a section, and each section teaching one",
        NOT_APPLICABLE if not body else WARN if not included or uncovered or idle else PASS,
        "No learning objective is selected." if not included else "; ".join(filter(None, [
            f"Not taught by any section: {'; '.join(uncovered[:3])}" if uncovered else "",
            f"{len(idle)} section(s) serve no objective" if idle else "",
            f"{suggested} link(s) are suggested on the Outline tab" if suggested else "",
        ])) + "." if uncovered or idle else f"{len(included)} objective(s), each taught."))

    problems = [(s.title or "Untitled", problem) for s in body
                if (problem := summary_problem(s))]
    checks.append(_check(
        "summaries", "Summaries", "Each teaching section says, in one line, what the viewer "
        "learns -- not the source's text, and not \"the chapter explores\"",
        NOT_APPLICABLE if not body else WARN if problems else PASS,
        f"{len(problems)} of {len(body)}: " + "; ".join(
            f"{title} ({problem})" for title, problem in problems[:4])
        + (". Write them, or use AI · write summaries on the Outline tab." if problems else "")
        if problems else "Every section says what the viewer learns."))

    shares = timing(plan, extraction, target.target_seconds)
    stretched, squeezed = shares["is_stretched"], shares["is_squeezed"]
    checks.append(_check(
        "timing", "Time for the material",
        f"The target neither stretches the material past x{MOST_STRETCH} nor squeezes it "
        f"below x{MOST_SQUEEZE}",
        NOT_APPLICABLE if not body else WARN if stretched or squeezed else PASS,
        f"The material needs about {round(shares['needed_total'] / 60, 1)} min; "
        f"{target.target_phrase} stretches it x{shares['scale']}, so the narration will "
        f"pad. Choose a shorter target, or add material." if stretched else
        f"The material needs about {round(shares['needed_total'] / 60, 1)} min; "
        f"{target.target_phrase} squeezes it x{shares['scale']}, so each section is cut "
        f"hard. Choose a longer target, or split the video." if squeezed else
        f"The material needs about {round(shares['needed_total'] / 60, 1)} min, "
        f"shared out x{shares['scale']} to fit {target.target_phrase}."))

    checks.append(_check(
        "audience", "Audience", "One audience is chosen",
        PASS if plan.selected_audience else WARN,
        plan.selected_audience or "No audience is chosen."))
    checks.append(_assets_check(project))
    return checks


def _assets_check(project) -> dict[str, str]:
    """The plan carries Assets & Design on, so it needs a transfer of it."""
    from pipeline.assets import AssetLibraryStore
    from pipeline.assets_handoff import confirmed_library
    from pipeline.assets_handoff import handoff_state as assets_state

    confirmed_library(project)     # a project from before transfers: taken as transferred
    rule = "Assets & Design is transferred: the plan carries its pictures, brand kit and look"
    state = assets_state(project, AssetLibraryStore(project.root).load())
    if not state["has_confirmed"]:
        return _check("assets", "Assets transferred", rule, FAIL,
                      "Assets & Design has never been transferred. Transfer it first: "
                      "the plan hands its pictures, brand kit and look to every later layer.")
    if state["pending"]:
        return _check("assets", "Assets transferred", rule, WARN,
                      "Assets & Design has changes that are not transferred; the plan "
                      "carries the last transfer.")
    return _check("assets", "Assets transferred", rule, PASS,
                  "The plan carries the last transfer of Assets & Design.")


# --- the transfer --------------------------------------------------------------------


def handoff_state(project) -> dict[str, Any]:
    plan = PlanStore(project.root).load()
    transferred = TransferredPlanStore(project.root).load()
    checks = plan_checks(project, plan)
    return {
        "checks": checks,
        "failing": sum(1 for c in checks if c["status"] == FAIL),
        "warning": sum(1 for c in checks if c["status"] == WARN),
        "has_transferred": bool(transferred.transferred_at),
        "transferred_at": transferred.transferred_at,
        "pending": bool(plan.sections) and (fingerprint(plan) != transferred.fingerprint
                                            or upstream.is_behind(project, "scene-plan")),
        "transferred_sections": len(transferred.plan.sections),
    }


def read_plan_handoff(slug: str) -> dict[str, Any]:
    return handoff_state(require_project(slug))


def transfer_plan(slug: str) -> dict[str, Any]:
    """Hand the plan as it stands to the next layer, with the assets it carries.
    Refused while a check fails."""
    from pipeline.lesson_plan import save_plan

    project = require_project(slug)
    # Attached to the latest assets first, so what is carried is in step.
    plan = save_plan(project, PlanStore(project.root).load())
    failing = [c for c in plan_checks(project, plan) if c["status"] == FAIL]
    if failing:
        raise OperationFailed(
            "The plan cannot be transferred while a check fails: "
            + "; ".join(f"{c['name']} -- {c['detail']}" for c in failing))
    TransferredPlanStore(project.root).save(TransferredPlan(
        plan=plan, transferred_at=datetime.now(UTC).isoformat(timespec="seconds"),
        fingerprint=fingerprint(plan), assets=ConfirmedAssetStore(project.root).load()))
    upstream.record(project, "scene-plan")
    return handoff_state(project)
