"""Generation, handed on: what making will do, the checks the shots must pass,
and the transferred -- frozen -- copy the render reads.

Generation works in two steps, and they are different kinds of work:

- **Decide** (`generation.plan_visuals`): what each scene shows -- the deck's
  slide, a picture from the source, a chart of stated numbers, a picture drawn
  by an image model, or words. Fixed rules, in a fixed order; no model.
- **Make** (`visual_build.build_visuals`): produce it. Slides, the source's
  figures, charts and diagrams are made by local code; two things call a
  model -- the headline and labels composed from each scene's brief, and the
  pictures drawn for scenes the source has nothing for. `make_preview` says in
  advance which scenes each applies to.

The render reads one set of shots: the transferred one. Made files are named by
scene, so making again rewrites them in place; a transfer therefore *freezes*
every made file -- copies it under a name taken from its content -- so what was
transferred cannot change under the render when the scene is made again.

Before the first transfer, the render reads the working shots, as it always
did; from the first transfer on, only the transferred copy.

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
from pipeline.generation import VisualKind, VisualPlan, VisualPlanStore, _stale_visual_ids
from pipeline.plan_handoff import FAIL, NOT_APPLICABLE, PASS, WARN
from pipeline.scene_lab import MAXIMUM_SCRIPT_ATTEMPTS, SCRIPTED
from pipeline.script_handoff import handoff_state as script_handoff_state
from pipeline.script_handoff import script_for_later_stages
from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore
from pipeline.storage.layout import artifact_path

FROZEN_DIRECTORY = "generation/transferred"

# The order Decide prefers, with what makes each apply. The page shows these;
# `generation.plan_visuals` applies them.
DECISION_RULES = [
    {"kind": "scripted", "name": "A scripted scene", "made_by": "AI (writes a script)",
     "when": "You chose it, for this scene or for every scene. A Python script draws the "
             "scene; fixed checks decide whether its clip is used"},
    {"kind": "slide", "name": "The deck's slide", "made_by": "Local code",
     "when": "The section follows a slide of the deck"},
    {"kind": "source_picture", "name": "A picture from the source", "made_by": "Local code",
     "when": "Assets & Design handed on a picture from the section's own source that is "
             "large and clear enough to fill a frame"},
    {"kind": "chart", "name": "A chart", "made_by": "Local code",
     "when": "The section is planned as a plot and its source states enough numbers"},
    {"kind": "generated_image", "name": "A drawn picture", "made_by": "AI (image model)",
     "when": "Nothing above applies, the section teaches or tells a story (the lesson "
             "frame shows words), and an image model is configured"},
    {"kind": "text", "name": "Words on screen", "made_by": "Local code",
     "when": "Nothing above applies"},
]


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
            description="transferred shots",
        )


def fingerprint(plan: VisualPlan) -> str:
    """What the shots are, not when they were planned."""
    shots = [v.model_dump(mode="json", exclude={"built_at"}) for v in plan.visuals]
    return hashlib.sha256(json.dumps(shots, sort_keys=True).encode()).hexdigest()[:20]


def visuals_for_later_stages(project) -> VisualPlan:
    """The shots the render reads: the transferred ones, or -- before anything
    was ever transferred -- the working ones."""
    transferred = TransferredVisualStore(project.root).load()
    if transferred.transferred_at:
        return transferred.visuals
    return VisualPlanStore(project.root).load()


# --- what making will do ---------------------------------------------------------------


def make_preview(project, plan: VisualPlan) -> dict[str, Any]:
    """Which scenes Make would produce, by how, before anything is made or paid for."""
    stale = _stale_visual_ids(project)
    behind = [v for v in plan.visuals if v.id in stale or not v.is_built]
    # A scripted scene is made by its own script, not by Make.
    wanted = [v for v in behind if v.kind != SCRIPTED]
    waiting = len(behind) - len(wanted)
    compose = [v for v in wanted
               if v.kind != VisualKind.SLIDE and (v.id in stale or not v.headline)]
    count = lambda kind: sum(1 for v in wanted if v.kind == kind)  # noqa: E731
    return {
        "to_make": len(wanted),
        "ai_words": len(compose),
        "ai_pictures": count(VisualKind.GENERATED_IMAGE),
        "slides": count(VisualKind.SLIDE),
        "source_pictures": count(VisualKind.SOURCE_PICTURE),
        "charts": count(VisualKind.CHART),
        "diagrams": count(VisualKind.DIAGRAM),
        "words": count(VisualKind.TEXT),
        "scripted": sum(1 for v in plan.visuals if v.kind == SCRIPTED),
        "scripted_waiting": waiting,
        "script_calls_at_most": waiting * MAXIMUM_SCRIPT_ATTEMPTS,
    }


# --- the checks ----------------------------------------------------------------------


def _check(key: str, name: str, rule: str, status: str, detail: str) -> dict[str, str]:
    return {"key": key, "name": name, "rule": rule, "status": status, "detail": detail}


def generation_checks(project, plan: VisualPlan) -> list[dict[str, str]]:
    from pipeline.plan_handoff import TransferredPlanStore
    from pipeline.plan_handoff import plan_for_later_stages

    # Only scenes of sections the plan has: narration left over from sections
    # it dropped is never rendered, so it needs no shot.
    planned = {section.id for section in plan_for_later_stages(project).sections}
    script = script_for_later_stages(project)
    scenes = {scene.id for entry in script.section_scripts if entry.section_id in planned
              for scene in entry.scenes}
    shot_scenes = {v.scene_id for v in plan.visuals}
    missing, extra = scenes - shot_scenes, shot_scenes - scenes
    checks = [_check(
        "match", "Shots match the script", "One shot per scene of the transferred script",
        NOT_APPLICABLE if not scenes else FAIL if missing or extra else PASS,
        "; ".join(part for part in [
            f"{len(missing)} scene(s) have no shot" if missing else "",
            f"{len(extra)} shot(s) belong to scenes the script no longer has" if extra else "",
        ] if part) + (" -- Decide again." if missing or extra else "")
        if missing or extra else f"{len(scenes)} scene(s), one shot each."
        if scenes else "The script has no scenes yet.")]

    unbuilt = [v for v in plan.visuals if not v.is_built]
    unscripted = sum(1 for v in unbuilt if v.kind == SCRIPTED)
    checks.append(_check(
        "made", "Every shot made",
        "Each shot has its words, and its picture if it needs one; each scripted scene has "
        "a clip that passed its checks",
        NOT_APPLICABLE if not plan.visuals else FAIL if unbuilt else PASS,
        "; ".join(part for part in [
            f"{len(unbuilt) - unscripted} shot(s) not made yet -- Make what is missing"
            if len(unbuilt) > unscripted else "",
            f"{unscripted} scripted scene(s) have no clip that passed -- write or fix "
            f"their scripts on the Make tab" if unscripted else ""] if part) + "."
        if unbuilt else "Every shot is made."))

    scripted = [v for v in plan.visuals if v.kind == SCRIPTED]
    checks.append(_check(
        "scripted", "Scenes drawn by scripts",
        "Every scripted scene watched against its brief: its checks prove it runs and "
        "fits, not that it is right",
        WARN if scripted else PASS,
        f"{len(scripted)} scene(s) are drawn by scripts. Watch each on the Make tab."
        if scripted else "None."))

    stale = _stale_visual_ids(project)
    checks.append(_check(
        "current", "Made for the scene as written", "No scene rewritten since its shot was made",
        FAIL if stale else PASS if plan.visuals else NOT_APPLICABLE,
        f"{len(stale)} scene(s) were rewritten after their shot was made -- Make again."
        if stale else "Every shot matches its scene."))

    drawn = [v for v in plan.visuals if v.kind == VisualKind.GENERATED_IMAGE]
    checks.append(_check(
        "ai-pictures", "Pictures drawn by AI", "Every drawn picture looked at against its brief",
        WARN if drawn else PASS,
        f"{len(drawn)} picture(s) were drawn by an image model, not taken from the source. "
        f"Check each on the Make tab." if drawn else "None: every picture is the source's own "
        "or made by local code."))

    checks.append(_check(
        "notes", "Making went cleanly", "No scene reported a problem while being made",
        WARN if plan.notes else PASS,
        " ".join(plan.notes)[:400] if plan.notes else "No problems reported."))

    script_state = script_handoff_state(project)
    checks.append(_check(
        "script", "Script transferred",
        "Shots made from a transferred script with no changes waiting",
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
        "make_preview": make_preview(project, plan),
        "rules": DECISION_RULES,
        "pictures": _pictures_handed_on(project),
    }


def _pictures_handed_on(project) -> dict[str, Any]:
    """The pictures Assets & Design handed on, and which of them cannot be a
    scene's picture. Judged here, where a picture is chosen for a scene: that
    layer lists what exists and judges nothing."""
    from pipeline.plan_pictures import assets_for_later_stages

    library = assets_for_later_stages(project).library
    handed_on = library.handed_on()
    return {
        "handed_on": len(handed_on),
        "usable": len(library.usable()),
        "cannot_fill_a_frame": [
            {"name": f.name, "why": f.why_not_a_frame}
            for f in handed_on if f not in library.usable()],
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
    """Freeze the shots as they stand and hand them to the render. Refused while
    a check fails."""
    project = require_project(slug)
    plan = VisualPlanStore(project.root).load()
    failing = [c for c in generation_checks(project, plan) if c["status"] == FAIL]
    if failing:
        raise OperationFailed(
            "The shots cannot be transferred while a check fails: "
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
