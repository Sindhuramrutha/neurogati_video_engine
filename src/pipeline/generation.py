"""Generation — one scene program per scene of the script.

Script & Staging writes, for every scene, what should be on screen while it is
said. This stage turns each of those briefs into a *scene*: a program (Manim,
matplotlib, Pillow, a web page or a Revideo scene) that is written, run,
checked and watched, then approved (`scene_lab.py`, `scene_maker.py`).

`plan_visuals` lists the scenes of the transferred script, one `SceneVisual`
each, and keeps a scene's program while its brief and narration are unchanged;
the render reads only the scenes whose program passed its checks and was
approved.

Stored at `projects/<slug>/generation/visuals.json`, each scene's program and
clip in `generation/scenes/<scene>/`.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MAXIMUM_VISUALS = 500

# Speech, for guessing how long a scene lasts before it has been spoken.
WORDS_PER_SECOND = 150 / 60


class SceneVisual(BaseModel):
    """One scene: the brief it was made for, and its program's result."""

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

    note: str = ""
    built_at: str = ""
    headline: str = ""
    asset_path: str = ""          # the scene's poster frame, relative to the project root
    clip_path: str = ""           # the scene's rendered clip, once its checks passed
    drawn_by: str = ""            # the program file: scene.py, scene.html or scene.tsx
    # When a person approved this scene's program after watching its preview;
    # empty until then. The render uses only approved scenes (`scene_lab.py`).
    approved_at: str = ""

    # Which slide of the source deck this scene refers to, 1-based, or 0. The
    # slide is material the program may use, never the shot.
    slide_number: int = 0

    @property
    def is_built(self) -> bool:
        """Whether this scene has a clip whose program passed every check."""
        return bool(self.clip_path)

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
            "approved_count": sum(1 for v in self.visuals if v.approved_at),
        }

    def to_dict(self, stale_ids: set[str] | None = None) -> dict[str, Any]:
        stale = stale_ids or set()
        warnings: list[str] = []
        unbuilt = [v for v in self.visuals if not v.is_built]
        if unbuilt:
            warnings.append(f"{len(unbuilt)} scene(s) have no program that passed its checks yet.")
        if stale:
            warnings.append(f"{len(stale)} scene(s) were rewritten after their program was made.")
        return {
            "visuals": [
                visual.to_dict() | {"is_stale": visual.id in stale} for visual in self.visuals
            ],
            "planned_at": self.planned_at,
            "built_at": self.built_at,
            "notes": self.notes,
            "audit": self.audit(),
            "warnings": warnings,
            "is_empty": not self.visuals,
        }


class VisualPlanStore(JsonDocumentStore[VisualPlan]):
    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.GENERATION),
            model_type=VisualPlan,
            build_default=VisualPlan,
            description="scenes",
        )


def brief_fingerprint(brief: str, narration: str) -> str:
    """What the scene was made for. A rewritten scene should not keep a program
    for what it used to say."""
    material = f"{brief.strip()}\n{narration.strip()}".encode()
    return hashlib.sha256(material).hexdigest()[:16]


def plan_visuals(slug: str) -> dict[str, Any]:
    """One scene per scene of the transferred script.

    A scene already planned keeps its program; one whose narration or brief was
    rewritten waits to be made again. The deck's slide and the section's
    pictures are material a program may use, named in its brief, never the
    shot. No model is called.
    """
    from pipeline.core import OperationFailed, require_project
    from pipeline.plan_handoff import plan_for_later_stages
    from pipeline.script_handoff import script_for_later_stages
    from pipeline.slide_plan import scene_slide

    project = require_project(slug)
    plan = plan_for_later_stages(project)
    script = script_for_later_stages(project)
    if not plan.sections:
        raise OperationFailed("The plan has no sections, so there are no scenes to show.")

    store = VisualPlanStore(project.root)
    previous = store.load()
    existing = {visual.scene_id: visual for visual in previous.visuals}
    visuals: list[SceneVisual] = []

    for section in plan.sections:
        entry = next(
            (s for s in script.section_scripts if s.section_id == section.id), None)
        scenes = entry.scenes if entry else []
        for number, scene in enumerate(scenes):
            fingerprint = brief_fingerprint(scene.brief, scene.narration)
            was = existing.get(scene.id)
            if was is not None and was.brief_fingerprint == fingerprint:
                visuals.append(was)                      # planned already; leave it
                continue
            slide_number = scene_slide(section, number, len(scenes))
            visuals.append(SceneVisual(
                id=was.id if was else new_identifier(),
                section_id=section.id, section_title=section.title,
                scene_id=scene.id, scene_number=number + 1,
                brief=scene.brief, narration_preview=scene.narration[:160],
                brief_fingerprint=fingerprint, slide_number=slide_number,
                note="Waiting for its program."
                     + (f" Reference: slide {slide_number}." if slide_number else ""),
            ))

    saved = store.save(VisualPlan(
        visuals=visuals, planned_at=_now(), built_at=previous.built_at))
    return saved.to_dict(_stale_visual_ids(project))


def _now() -> str:
    from datetime import UTC, datetime

    return datetime.now(UTC).isoformat(timespec="seconds")


def _stale_visual_ids(project) -> set[str]:
    """Scenes rewritten since their program was made.

    Compared against the script rather than remembered at build time: the script
    is what the video will say, and a program for an older sentence is exactly
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
    """The scenes, and which of them no longer match their script."""
    from pipeline.core import require_project

    project = require_project(slug)
    return VisualPlanStore(project.root).load().to_dict(_stale_visual_ids(project))
