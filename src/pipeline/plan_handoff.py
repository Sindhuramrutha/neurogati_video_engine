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
from pipeline.planning import SLIDE_ORDERS, Plan, PlanStore
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
    from pipeline.plan_order import plan_order_report
    from pipeline.plan_units import unit_word, units_of

    extraction = ExtractionStore(project.root).load()
    freshness = plan_freshness(plan, extraction)
    sections = plan.sections
    units = units_of(extraction)
    word = unit_word(units)
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

    report = plan_order_report(plan, units)
    body = [s for s in sections if s.sources]
    checks.append(_check(
        "order", f"{word.capitalize()} order", SLIDE_ORDERS[plan.slide_order],
        NOT_APPLICABLE if not body else
        (FAIL if plan.slide_order == "strict" else WARN) if report["order"] else PASS,
        "; ".join(report["order"]).capitalize() + "." if report["order"]
        else f"The {word}s keep the chosen order."))

    checks.append(_check(
        "coverage", f"Every {word} covered",
        f"Each {word} is in a section, or left out on purpose with why",
        NOT_APPLICABLE if not body else WARN if report["coverage"] else PASS,
        "; ".join(report["coverage"]).capitalize() + "." if report["coverage"]
        else f"All {len(units)} {word}s are covered"
        + (f", {len(plan.slides_left_out)} left out on purpose." if plan.slides_left_out
           else ".")))

    empty = [s.title or "Untitled" for s in sections if not s.scenes]
    checks.append(_check(
        "scenes", "Every section has scenes",
        "Each section is broken into the scenes every later layer works on",
        NOT_APPLICABLE if not sections else FAIL if empty else PASS,
        f"No scenes yet: {', '.join(empty[:6])}." if empty
        else f"{plan.scene_count} scenes in {len(sections)} sections."))

    total = plan.total_estimated_seconds
    length = plan.length
    within = length.shortest_seconds <= total <= length.longest_seconds
    checks.append(_check(
        "length", "Length", "Within the length asked for, as understood",
        NOT_APPLICABLE if not sections or not length.is_known else PASS if within else WARN,
        f"About {round(total / 60, 1)} min planned. Asked for: {length.understood}"
        if length.is_known else "No length is understood yet."))

    checks.append(_check(
        "extraction", "Matches the extraction",
        "Planned from the extraction as it is now",
        WARN if freshness["is_stale"] or freshness["is_unlinked"] else PASS if sections
        else NOT_APPLICABLE,
        "The extraction changed since this plan was made."
        if freshness["is_stale"] else
        "Nothing records which extraction this plan was made from."
        if freshness["is_unlinked"] else "Made from the extraction as it is now."))

    untitled = [i + 1 for i, s in enumerate(sections) if not s.title]
    checks.append(_check(
        "titles", "Titles", "Every section has a title",
        WARN if untitled else PASS if sections else NOT_APPLICABLE,
        f"Sections without a title: {', '.join(map(str, untitled))}." if untitled
        else "Every section has a title."))

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
