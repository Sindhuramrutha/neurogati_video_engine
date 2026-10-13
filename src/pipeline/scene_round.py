"""One round of making a scene: render what is written, check it, and -- when every
check passes -- have its frames reviewed.

What comes back is the feedback for the next round: the failing checks (and what
a crash printed, or -- when a layout check fails -- what the frames show), or what
the review says must change and what is only polish.
"""

from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Any

from pipeline.llm import ModelCallFailed
from pipeline.scene_program import ENTRY_FILES

LONGEST_LOG_SHOWN = 2500
# Checks about where things are on screen: when one fails, the frames are looked at.
LAYOUT_CHECKS = {"bounds", "overlap", "crossing", "collide", "fills", "pictured", "edges",
                 "moments"}
# Rendering (Manim, a browser, ffmpeg) is what uses the machine's memory: four renders
# at once ran a 16 GB machine out ("x264 malloc failed"). Scenes still think side by
# side; only this many render at the same moment.
_render_slots = threading.Semaphore(max(1, int(os.environ.get("SCENE_RENDERS_AT_ONCE", "2") or 2)))


def render_round(slug: str, visual_id: str, folder: Path, renderer: str,
                 spec: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    from pipeline.scene_lab import run_scene
    from pipeline.scene_program import save_spec
    from pipeline.scene_review import review_frames

    save_spec(folder, spec | {"renderer": renderer, "entry": ENTRY_FILES[renderer]})
    state["renders"] += 1
    with _render_slots:
        result = run_scene(slug, visual_id)
    failing = [c for c in result["checks"] if c["status"] == "fail"]
    warnings = [f"warn {c['name']}: {c['detail']}" for c in result["checks"]
                if c["status"] == "warn"]
    outcome: dict[str, Any] = {
        "passed": not failing, "good": False, "reviewed": False, "verdict": None,
        "failing": [c["name"] for c in failing], "problems": [], "polish": [],
        "scores": {}, "score": 0.0}

    if failing:
        lines = ["These checks FAIL:"]
        lines += [f"- {c['name']}: {c['detail']} (rule: {c['rule']})" for c in failing]
        if any(c["key"] in ("ran", "video") for c in failing):
            lines.append("What it printed (the end):\n" + result["log"][-LONGEST_LOG_SHOWN:])
        elif any(c["key"] in LAYOUT_CHECKS for c in failing):
            lines += _layout_seen(folder, result["brief"], failing, state)
    else:
        state["calls"]["vision"] += 1
        try:
            verdict = review_frames(folder, result["brief"])
        except ModelCallFailed as unavailable:
            outcome["feedback"] = ("Every check passed. The frames could not be reviewed: "
                                   f"{unavailable}")
            return outcome
        outcome.update(reviewed=True, good=verdict.good, verdict=verdict.model_dump(),
                       problems=verdict.problems, polish=verdict.polish,
                       scores=verdict.scores.model_dump(), score=verdict.scores.mean())
        lines = ["Every check passed. A reviewer scored the frames, 1 to 5 (the bar: none "
                 "below 3, teaches and accuracy 4 or more), weakest first -- fix the "
                 "weakest first:",
                 "  " + ", ".join(f"{name} {value}" for name, value
                                  in verdict.scores.weakest())]
        lines += [f"- MUST FIX: {problem}" for problem in verdict.problems]
        lines += [f"- optional polish: {item}" for item in verdict.polish]
        if verdict.good:
            lines.append("It is good as it stands.")
    outcome["feedback"] = "\n".join(lines + warnings)
    return outcome


def _layout_seen(folder: Path, brief: dict[str, Any], failing: list[dict[str, Any]],
                 state: dict[str, Any]) -> list[str]:
    """A layout that fails a check, looked at: the model that writes the program
    reads only text, and from a check's coordinates alone it kept re-placing the
    same boxes the same wrong way. What the frames show, and how to rearrange."""
    from pipeline.llm import ModelNotConfigured
    from pipeline.scene_review import review_frames

    if not (folder / "frames").is_dir():
        return []
    question = ("These layout checks failed: "
                + "; ".join(f"{c['name']} ({c['detail'][:200]})" for c in failing
                            if c["key"] in LAYOUT_CHECKS)
                + ". Say, in the frames, what causes each one and how to rearrange the "
                "layout so it cannot happen -- where things should go, not 'move it a bit'.")
    state["calls"]["vision"] += 1
    try:
        seen = review_frames(folder, brief, question)
    except (ModelCallFailed, ModelNotConfigured):
        return []
    found = seen.problems + seen.polish
    return ["What a reviewer sees in the frames:"] + [f"- {item}" for item in found] \
        if found else []
