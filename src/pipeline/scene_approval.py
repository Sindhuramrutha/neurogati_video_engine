"""Approval: a person watches a scene that passed every check and says it is right.
The render uses only approved scenes, and says which are not.
"""

from __future__ import annotations

from typing import Any

from pipeline.core import OperationFailed, require_project
from pipeline.generation import VisualPlanStore, _now
from pipeline.scene_lab import PLAN_LOCK, _visual, read_scene


def approve_scene(slug: str, visual_id: str, approved: bool = True) -> dict[str, Any]:
    """A person has watched the preview and says it is right -- or takes that back."""
    project = require_project(slug)
    store = VisualPlanStore(project.root)
    with PLAN_LOCK:
        plan = store.load()
        visual = _visual(plan, visual_id)
        if approved and not visual.clip_path:
            raise OperationFailed("Only a scene whose program passed every check can be "
                                  "approved.")
        visual.approved_at = _now() if approved else ""
        store.save(plan)
    return read_scene(slug, visual_id)


def approve_passed(slug: str) -> dict[str, Any]:
    """Approve, in one go, every scene whose program passed every check and is not
    approved yet. Scenes without a passing clip are left as they are, and counted."""
    project = require_project(slug)
    store = VisualPlanStore(project.root)
    with PLAN_LOCK:
        plan = store.load()
        waiting = [v for v in plan.visuals if v.clip_path and not v.approved_at]
        for visual in waiting:
            visual.approved_at = _now()
        store.save(plan)
    return {"approved": len(waiting),
            "not_passed": sum(1 for v in plan.visuals if not v.clip_path)}


def render_blockers(visuals) -> list[str]:
    """Why the render cannot use these scenes. Never a fallback to a still."""
    blockers = []
    for visual in visuals:
        name = f"“{visual.section_title}” scene {visual.scene_number}"
        if not visual.clip_path:
            blockers.append(f"{name} has no program that passed its checks")
        elif not visual.approved_at:
            blockers.append(f"{name} is not approved")
    return blockers
