"""Making every scene, on the server, a few at a time and in the video's order.

How one scene is made is `scene_maker.py` (write, render, review, edit). This is
the queue around it:

- `start` queues scenes; they are taken in the order of the video, `MOST_AT_ONCE`
  at a time; leaving the page does not stop them;
- `stop` and `stop_all` drop a scene from the queue, or tell one that is working to
  stop after its round (nothing it made is deleted);
- `agent_view` and `queue_view` are what the page shows: never a conversation, only
  status, what is happening now, and the steps taken.

A scene never waits for an answer: it finishes, or fails with the reason; the
person changes it afterwards by saying what to change (`instruction`).
"""

from __future__ import annotations

import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from pipeline.core import require_project
from pipeline.generation import VisualPlanStore, _now
from pipeline.scene_lab import _visual, scene_folder
from pipeline.scene_maker import MOST_ROUNDS, make_scene
from pipeline.scene_state import STOP, add_event, load_state, save_state

logger = logging.getLogger(__name__)

MOST_RENDERS = MOST_ROUNDS      # what the page and the transfer say a scene may use
# Side by side. Not more: six renders at once (Manim, Chromium) left a 16 GB machine
# with about 1 GB free, and the provider's per-minute limit caps throughput anyway.
MOST_AT_ONCE = max(1, int(os.environ.get("SCENE_AGENTS_AT_ONCE", "4") or 4))

_pool = ThreadPoolExecutor(max_workers=MOST_AT_ONCE, thread_name_prefix="scene-maker")
_running: set[tuple[str, str]] = set()     # queued or working, in this server
_working: set[tuple[str, str]] = set()     # working now
_waiting_for_a_place: dict[tuple[str, str], Any] = {}   # queued: not started yet


def _run_safely(slug: str, visual_id: str, instruction: str, fresh: bool) -> None:
    _working.add((slug, visual_id))
    _waiting_for_a_place.pop((slug, visual_id), None)
    try:
        make_scene(slug, visual_id, instruction=instruction, fresh=fresh)
    except Exception as failure:
        logger.exception("scene %s failed", visual_id)
        _record_failure(slug, visual_id, failure)
    finally:
        _working.discard((slug, visual_id))
        _running.discard((slug, visual_id))


def _record_failure(slug: str, visual_id: str, failure: Exception) -> None:
    """What the disk says is what happened: a scene that stopped on an error is
    `failed`, with the reason, not left `working` for the page to guess at."""
    try:
        project = require_project(slug)
        folder = scene_folder(project, _visual(VisualPlanStore(project.root).load(), visual_id),
                              create=True)
        state = load_state(folder)
        state.update(status="failed", doing="", error=str(failure)[:500] or type(failure).__name__)
        add_event(state, "note", f"Stopped on an error: {state['error']}")
        save_state(folder, state)
    except Exception:                       # the project may be gone; nothing to record
        logger.exception("could not record the failure of scene %s", visual_id)


def is_working(slug: str) -> bool:
    """Is any scene of this project being made (or about to be) right now?"""
    return any(project_slug == slug for project_slug, _ in _running)


def _shown_status(slug: str, visual_id: str, status: str) -> str:
    """What the page says. A scene saved as queued or working that this server is
    not running was interrupted (the app restarted): making the missing resumes it."""
    if (slug, visual_id) in _working:
        return "working"
    if (slug, visual_id) in _running:
        return "queued"
    return "interrupted" if status in ("queued", "working") else status


def start(slug: str, visual_ids: list[str], *, instruction: str = "",
          fresh: bool = False) -> dict[str, Any]:
    """Queue these scenes. Ones already queued or working are left."""
    project = require_project(slug)
    plan = VisualPlanStore(project.root).load()
    # Start to end, in the video's own order -- the queue takes them in this order.
    place = {visual.id: index for index, visual in enumerate(plan.visuals)}
    visual_ids = sorted(visual_ids, key=lambda visual_id: place.get(visual_id, len(place)))
    started = []
    for visual_id in visual_ids:
        if (slug, visual_id) in _running:
            continue
        folder = scene_folder(project, _visual(plan, visual_id), create=True)
        state = load_state(folder)
        state.update(status="queued", doing="Waiting for a place")
        save_state(folder, state)
        _running.add((slug, visual_id))
        _waiting_for_a_place[(slug, visual_id)] = _pool.submit(
            _run_safely, slug, visual_id, instruction, fresh)
        started.append(visual_id)
    return {"started": started, "running": sorted(v for s, v in _running if s == slug)}


def stop(slug: str, visual_id: str) -> dict[str, Any]:
    """Stop one scene. One that is working stops after its round; one still queued
    is dropped before it starts. Nothing it made is deleted."""
    project = require_project(slug)
    folder = scene_folder(project, _visual(VisualPlanStore(project.root).load(), visual_id),
                          create=True)
    key = (slug, visual_id)
    queued = _waiting_for_a_place.get(key)
    if queued is not None and queued.cancel():
        _waiting_for_a_place.pop(key, None)
        _running.discard(key)
        state = load_state(folder)
        state.update(status="stopped", doing="")
        add_event(state, "stopped", "Stopped before it started.")
        save_state(folder, state)
    else:
        (folder / STOP).write_text(_now(), encoding="utf-8")
    return agent_view(slug, visual_id)


def stop_all(slug: str) -> dict[str, Any]:
    """Stop every scene of this project: the queue is dropped, and the ones working
    stop after their round. Nothing is deleted; Make the missing resumes."""
    stopped = [visual_id for project_slug, visual_id in sorted(_running) if project_slug == slug]
    for visual_id in stopped:
        stop(slug, visual_id)
    return {"stopped": len(stopped)}


def agent_view(slug: str, visual_id: str) -> dict[str, Any]:
    """What the page shows of one scene's making."""
    project = require_project(slug)
    folder = scene_folder(project, _visual(VisualPlanStore(project.root).load(), visual_id))
    state = load_state(folder)
    return {key: state[key] for key in ("status", "summary", "remarks", "renders", "calls",
                                        "tokens", "last_render", "error", "doing",
                                        "updated_at")} \
        | {"events": state["events"][-60:], "running": (slug, visual_id) in _running,
           "status": _shown_status(slug, visual_id, state["status"]),
           "most_renders": MOST_RENDERS}


def queue_view(slug: str) -> dict[str, Any]:
    """Every scene at a glance, for the Make tab."""
    project = require_project(slug)
    scenes = []
    for visual in VisualPlanStore(project.root).load().visuals:
        state = load_state(scene_folder(project, visual))
        scenes.append({"id": visual.id,
                       "status": _shown_status(slug, visual.id, state["status"]),
                       "running": (slug, visual.id) in _running, "doing": state["doing"],
                       "renders_used": state["renders"], "most_renders": MOST_RENDERS,
                       "remarks": len(state["remarks"])})
    count = lambda status: sum(1 for s in scenes if s["status"] == status)  # noqa: E731
    return {"scenes": scenes, "working": count("working"), "queued": count("queued"),
            "interrupted": count("interrupted"), "failed": count("failed"),
            "running": sum(1 for s in scenes if s["running"]), "at_once": MOST_AT_ONCE}
