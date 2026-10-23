"""What the Assets, Generation, Export and Reviewing agents are shown of their own
work, as text: the deck's pictures, every scene's state, and what Export would say.

Asked to review Chapter 1, the Assets, Generation and Export agents each answered
that they could not see their inputs -- no figure inventory, no scene checks, no
render or export state -- and gave methods instead of findings; Reviewing saw an
empty comment list and could not tell "every check passed" from "no check ran".
Everything here is read from what is on disk; nothing is made or asked for.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pipeline.core import Project


def assets_text(project: Project) -> str:
    """The deck's pictures handed on: what each shows, what it is for, where it is
    shown -- and those no scene shows."""
    from pipeline.plan_pictures import assets_for_later_stages
    from pipeline.scene_pictures import deck_usage
    from pipeline.scene_vetting import VERDICTS
    from pipeline.storage.documents import read_json_object

    library = assets_for_later_stages(project).library
    usable = {f.asset_path for f in library.usable()}
    verdicts = read_json_object(project.root / "generation" / "scenes" / VERDICTS,
                                "picture notes") or {}
    usage = {p["path"]: p["shown_in"] for p in deck_usage(project, library)["pictures"]}
    lines = [f"{len(library.handed_on())} pictures handed on, {len(usable)} usable as a "
             "scene's picture."]
    for figure in library.handed_on():
        seen = verdicts.get(str(project.root / figure.asset_path)) or verdicts.get(
            str(project.root / figure.shown_path)) or {}
        shown = usage.get(figure.shown_path) or []
        lines.append(
            f"- {figure.name} (slide {figure.slide_number}, {figure.asset_path}): "
            f"{seen.get('what') or 'not described yet'}; role {seen.get('role') or '?'}; "
            + ("usable" if figure.asset_path in usable else "too small or unclear to fill a "
               "frame")
            + f"; shown in: {', '.join(shown) if shown else 'no scene'}")
    return "\n".join(lines)


def scenes_text(project: Project) -> str:
    """Every scene: whether it has a clip, its checks, the reviewer's last word, and
    how many rounds it took."""
    from pipeline.generation import VisualPlanStore
    from pipeline.scene_kept import failing_checks
    from pipeline.scene_program import scene_folder

    lines = []
    for number, visual in enumerate(VisualPlanStore(project.root).load().visuals, start=1):
        folder = scene_folder(project, visual)
        state = _read(folder / "agent.json") if folder else {}
        last = state.get("last_render") or {}
        failing = [c.get("name", "") for c in failing_checks(folder)] if folder else []
        scores = last.get("scores") or {}
        lines.append(
            f"Scene {number} ({visual.section_title}): "
            + ("no clip" if not visual.clip_path else "clip made")
            + f"; status {state.get('status', 'not started')}"
            + f"; rounds {state.get('renders', 0)}"
            + ("; checks: all pass" if folder and not failing and visual.clip_path
               else f"; FAILING: {', '.join(failing)}" if failing else "")
            + (f"; reviewer scores {json.dumps(scores)}" if scores else "")
            + ("; reached the reviewer's bar" if last.get("good") else
               f"; below the bar: {visual.below_bar}" if visual.below_bar else "")
            + ("" if visual.below_bar else "".join(
                f"\n    still wanted: {p}" for p in (last.get("problems") or [])[:3])))
    return "\n".join(lines) or "No scenes planned yet."


def export_text(project: Project) -> str:
    """What Export would say now: what blocks it and what it warns of, scene by scene."""
    from pipeline.exporting import export_readiness

    blockers, warnings = export_readiness(project)
    return "\n".join(["Blocks the export:"] + [f"- {b}" for b in blockers or ["nothing"]]
                     + ["Warnings:"] + [f"- {w}" for w in warnings or ["none"]])


def _read(path: Path) -> dict[str, Any]:
    try:
        found = json.loads(path.read_text(encoding="utf-8"))
        return found if isinstance(found, dict) else {}
    except (OSError, ValueError):
        return {}
