"""Generation, handed on: the checks the scenes must pass, and the transferred --
frozen -- copy the render reads.

Every scene is a program that was run, checked and approved (`scene_lab.py`).
The render reads one set of scenes: the transferred one. A scene's files are
named by scene, so making it again rewrites them in place; a transfer therefore
*freezes* every file -- copies it under a name taken from its content -- so what
was transferred cannot change under the render when the scene is made again.

Before the first transfer the render reads the working scenes; from the first
transfer on, only the transferred copy.

Stored at `generation/visuals.transferred.json`, the frozen files in
`generation/transferred/`.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from pipeline import upstream
from pipeline.core import OperationFailed, require_project
from pipeline.generation import VisualPlan, VisualPlanStore, _stale_visual_ids
from pipeline.plan_handoff import FAIL, NOT_APPLICABLE, PASS, WARN
from pipeline.scene_agent import MOST_RENDERS
from pipeline.script_handoff import handoff_state as script_handoff_state
from pipeline.script_handoff import script_for_later_stages
from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore
from pipeline.storage.layout import artifact_path

FROZEN_DIRECTORY = "generation/transferred"

class TransferredVisuals(BaseModel):
    visuals: VisualPlan = Field(default_factory=VisualPlan)
    transferred_at: str = ""
    fingerprint: str = ""


class TransferredVisualStore(JsonDocumentStore[TransferredVisuals]):
    def __init__(self, project_root) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.GENERATION).with_name(
                "visuals.transferred.json"),
            model_type=TransferredVisuals, build_default=TransferredVisuals,
            description="transferred scenes",
        )


def fingerprint(plan: VisualPlan) -> str:
    """What the scenes are, not when they were planned."""
    scenes = [v.model_dump(mode="json", exclude={"built_at"}) for v in plan.visuals]
    return hashlib.sha256(json.dumps(scenes, sort_keys=True).encode()).hexdigest()[:20]


def visuals_for_later_stages(project) -> VisualPlan:
    """The scenes the render reads: the transferred ones, or -- before anything
    was ever transferred -- the working ones."""
    transferred = TransferredVisualStore(project.root).load()
    if transferred.transferred_at:
        return transferred.visuals
    return VisualPlanStore(project.root).load()


# --- what making will do ---------------------------------------------------------------


def make_preview(plan: VisualPlan) -> dict[str, Any]:
    """How many scenes there are and where each stands, before anything is paid for."""
    return {
        "scenes": len(plan.visuals),
        "passed": sum(1 for v in plan.visuals if v.clip_path),
        "approved": sum(1 for v in plan.visuals if v.clip_path and v.approved_at),
        "waiting": sum(1 for v in plan.visuals if not v.clip_path),
        "agent_budget": {"renders": MOST_RENDERS},
    }


# --- the checks ----------------------------------------------------------------------


def _check(key: str, name: str, rule: str, status: str, detail: str) -> dict[str, str]:
    return {"key": key, "name": name, "rule": rule, "status": status, "detail": detail}


def generation_checks(project, plan: VisualPlan) -> list[dict[str, str]]:
    from pipeline.plan_handoff import TransferredPlanStore, plan_for_later_stages

    # Only scenes of sections the plan has: narration left over from sections
    # it dropped is never rendered, so it needs no program.
    planned = {section.id for section in plan_for_later_stages(project).sections}
    script = script_for_later_stages(project)
    scenes = {scene.id for entry in script.section_scripts if entry.section_id in planned
              for scene in entry.scenes}
    planned_scenes = {v.scene_id for v in plan.visuals}
    missing, extra = scenes - planned_scenes, planned_scenes - scenes
    from pipeline.scene_approval import render_blockers
    blockers = render_blockers([v for v in plan.visuals if v.scene_id in scenes])
    checks = [_check(
        "programs", "Every scene is an approved program",
        "Each scene's program passed every check and was approved after its preview",
        FAIL if blockers else PASS if plan.visuals else NOT_APPLICABLE,
        f"{len(blockers)} not yet: " + "; ".join(blockers[:4]) if blockers
        else "Every scene's program passed and is approved." if plan.visuals
        else "No scenes are set up yet."), _check(
        "match", "Scenes match the script", "One scene per scene of the transferred script",
        NOT_APPLICABLE if not scenes else FAIL if missing or extra else PASS,
        "; ".join(part for part in [
            f"{len(missing)} scene(s) have not been set up" if missing else "",
            f"{len(extra)} scene(s) belong to scenes the script no longer has" if extra else "",
        ] if part) + (" -- set the scenes up again." if missing or extra else "")
        if missing or extra else f"{len(scenes)} scene(s), one program each."
        if scenes else "The script has no scenes yet.")]

    unbuilt = [v for v in plan.visuals if not v.is_built]
    checks.append(_check(
        "made", "Every scene made",
        "Each scene has a clip whose program passed every check",
        NOT_APPLICABLE if not plan.visuals else FAIL if unbuilt else PASS,
        f"{len(unbuilt)} scene(s) have no program that passed -- write or fix them on the "
        f"Make tab." if unbuilt else "Every scene is made."))

    checks.append(_check(
        "watched", "Scenes watched against their brief",
        "A scene's checks prove it runs and fits, not that it is right: a person watches "
        "each one",
        WARN if plan.visuals else PASS,
        f"{len(plan.visuals)} scene(s) are programs. Watch each on the Make tab."
        if plan.visuals else "None."))

    stale = _stale_visual_ids(project)
    checks.append(_check(
        "current", "Made for the scene as written", "No scene rewritten since its program was made",
        FAIL if stale else PASS if plan.visuals else NOT_APPLICABLE,
        f"{len(stale)} scene(s) were rewritten after their program was made -- make them again."
        if stale else "Every program matches its scene."))

    checks.append(_check(
        "notes", "Making went cleanly", "No scene reported a problem while being made",
        WARN if plan.notes else PASS,
        " ".join(plan.notes)[:400] if plan.notes else "No problems reported."))

    script_state = script_handoff_state(project)
    checks.append(_check(
        "script", "Script transferred",
        "Scenes made from a transferred script with no changes waiting",
        WARN if not script_state["has_transferred"] or script_state["pending"] else PASS,
        "The script has never been transferred." if not script_state["has_transferred"]
        else "The script has changes that are not transferred yet."
        if script_state["pending"] else "Made from the transferred script."))

    # Pictures, brand kit and look come through the plan, never from Assets &
    # Design directly.
    carried = TransferredPlanStore(project.root).load()
    checks.append(_check(
        "assets", "Assets carried by the plan",
        "Each section's pictures, the brand kit and the look come from the transferred plan",
        PASS if carried.transferred_at and carried.assets is not None else WARN,
        "From the transferred plan." if carried.transferred_at and carried.assets is not None
        else "The plan was transferred before it carried Assets & Design; transfer it "
        "again so the pictures are the ones attached to its sections."
        if carried.transferred_at else "The plan has never been transferred."))
    return checks


# --- the transfer --------------------------------------------------------------------


def handoff_state(project) -> dict[str, Any]:
    plan = VisualPlanStore(project.root).load()
    transferred = TransferredVisualStore(project.root).load()
    checks = generation_checks(project, plan)
    return {
        "checks": checks,
        "failing": sum(1 for c in checks if c["status"] == FAIL),
        "warning": sum(1 for c in checks if c["status"] == WARN),
        "has_transferred": bool(transferred.transferred_at),
        "transferred_at": transferred.transferred_at,
        "pending": bool(plan.visuals) and (fingerprint(plan) != transferred.fingerprint
                                           or upstream.is_behind(project, "generation")),
        "make_preview": make_preview(plan),
        "pictures": _pictures_handed_on(project),
    }


def _pictures_handed_on(project) -> dict[str, Any]:
    """The deck's pictures the plan carried, how many of them the video shows, and
    what was measured about the rest. Every one is offered to every scene, nearest
    first; what was measured is said to the agent, not used to refuse it."""
    from pipeline.plan_pictures import assets_for_later_stages
    from pipeline.scene_pictures import deck_usage

    library = assets_for_later_stages(project).library
    handed_on = library.handed_on()
    usage = deck_usage(project, library)
    return {
        "handed_on": len(handed_on),
        "shown": usage["shown"],
        "not_shown": [{"name": p["name"], "slide_number": p["slide_number"]}
                      for p in usage["not_shown"]],
        "measured": [{"name": f.name, "why": f.why_not_a_frame}
                     for f in handed_on if f.why_not_a_frame],
    }


def read_generation_handoff(slug: str) -> dict[str, Any]:
    return handoff_state(require_project(slug))


def _freeze(project, relative: str) -> str:
    """A made file, copied under a name taken from its content, and its new path.
    Files from other stages (the source's pictures) are left where they are:
    those are not rewritten by making again."""
    if not relative.startswith("generation/") or relative.startswith(FROZEN_DIRECTORY):
        return relative
    source = project.root / relative
    if not source.is_file():
        return relative
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:20]
    frozen = project.root / FROZEN_DIRECTORY / f"{digest}{source.suffix}"
    if not frozen.exists():
        frozen.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, frozen)
    return f"{FROZEN_DIRECTORY}/{frozen.name}"


def transfer_generation(slug: str) -> dict[str, Any]:
    """Freeze the scenes as they stand and hand them to the render. Refused while
    a check fails."""
    project = require_project(slug)
    plan = VisualPlanStore(project.root).load()
    failing = [c for c in generation_checks(project, plan) if c["status"] == FAIL]
    if failing:
        raise OperationFailed(
            "The scenes cannot be transferred while a check fails: "
            + "; ".join(f"{c['name']} -- {c['detail']}" for c in failing))
    frozen = plan.model_copy(deep=True)
    for visual in frozen.visuals:
        visual.asset_path = _freeze(project, visual.asset_path)
        visual.clip_path = _freeze(project, visual.clip_path)
    TransferredVisualStore(project.root).save(TransferredVisuals(
        visuals=frozen, transferred_at=datetime.now(UTC).isoformat(timespec="seconds"),
        fingerprint=fingerprint(plan)))
    upstream.record(project, "generation")
    return handoff_state(project)
