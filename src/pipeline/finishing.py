"""Finish the video from the app, in one go: make every scene still missing or failing
its checks, render, and build the export -- on the server, so it survives the page.

Until this, finishing Chapter 1 took a person at a terminal: remaking the scenes that
ended failing, queueing the render once they were done, building the export once the
render was. Each step waits for the one before; what it is doing, and how it ended,
is kept in `finish.json` for the page.
"""

from __future__ import annotations

import json
import threading
import time
from datetime import UTC, datetime
from typing import Any

from pipeline.core import OperationFailed, require_project

STATUS_FILE = "finish.json"
POLL_SECONDS = 20
_running: set[str] = set()
_lock = threading.Lock()


def status(slug: str) -> dict[str, Any]:
    path = require_project(slug).root / STATUS_FILE
    try:
        found = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        found = {"state": "idle"}
    found["running"] = slug in _running
    return found


def start(slug: str) -> dict[str, Any]:
    """Start finishing this project, unless it is already being finished."""
    from pipeline.storyboard import gate

    reason = gate(require_project(slug))
    if reason:
        raise OperationFailed(reason)
    with _lock:
        if slug not in _running:
            _running.add(slug)
            threading.Thread(target=_run, args=(slug,), name=f"finish-{slug}",
                             daemon=True).start()
    return status(slug)


def _say(slug: str, state: str, step: str, **more: Any) -> None:
    from pipeline.storage.documents import write_text_atomically

    write_text_atomically(require_project(slug).root / STATUS_FILE, json.dumps(
        {"state": state, "step": step, "at": datetime.now(UTC).isoformat(timespec="seconds"),
         **more}, ensure_ascii=False))


def _run(slug: str) -> None:
    try:
        _scenes(slug)
        _render(slug)
        _export(slug)
    except Exception as failure:          # said on the page, not lost in a thread
        _say(slug, "failed", f"Stopped: {failure}")
    finally:
        _running.discard(slug)


def _scenes(slug: str) -> None:
    """Every scene without a clip is made; every scene failing its checks is made again
    from the start. Waits until none is working."""
    from pipeline import scene_agent
    from pipeline.generation import VisualPlanStore
    from pipeline.scene_kept import failing_checks
    from pipeline.scene_program import scene_folder

    project = require_project(slug)
    visuals = VisualPlanStore(project.root).load().visuals
    missing = [v.id for v in visuals if not v.clip_path]
    failing = [v.id for v in visuals if v.clip_path and (folder := scene_folder(project, v))
               and failing_checks(folder)]
    _say(slug, "working", f"Making {len(missing)} missing scene(s) and remaking "
         f"{len(failing)} that fail their checks")
    if missing:
        scene_agent.start(slug, missing)
    if failing:
        scene_agent.start(slug, failing, fresh=True)
    while scene_agent.is_working(slug):
        time.sleep(POLL_SECONDS)


def _render(slug: str) -> None:
    from pipeline import render_queue, video_setup
    from pipeline.scene_approval import approve_passed

    approve_passed(slug)
    _say(slug, "working", "Rendering the video")
    # A render of an older cut still in the queue would refuse this one: one rendering
    # is waited for, one paused or waiting (interrupted by a restart) is dropped.
    while any(j["slug"] == slug and j["status"] == "rendering"
              for j in render_queue.queue_view()["jobs"]):
        time.sleep(POLL_SECONDS)
    for job in render_queue.queue_view()["jobs"]:
        if job["slug"] == slug and job["status"] in render_queue.UNFINISHED:
            render_queue.delete_job(job["id"])
    before = {job["id"] for job in render_queue.queue_view()["jobs"]}
    voice = video_setup.edge_voice(require_project(slug).root, "en")
    render_queue.add_job(slug, "edge", voice)
    while True:
        time.sleep(POLL_SECONDS)
        job = next((j for j in render_queue.queue_view()["jobs"]
                    if j["slug"] == slug and j["id"] not in before), None)
        if job is None or job["status"] in ("failed", "paused"):
            raise OperationFailed("the render did not finish"
                                  + (f": {job.get('message', '')}" if job else ""))
        if job["status"] == "done":
            return


def _export(slug: str) -> None:
    from pipeline.exporting import build_export

    _say(slug, "working", "Building the export")
    built = build_export(slug)
    blockers = built.get("blockers") or []
    _say(slug, "done" if not blockers else "blocked",
         "Finished: the export is ready." if not blockers
         else "Rendered and exported, but not ready to hand over.",
         blockers=blockers, warnings=(built.get("warnings") or [])[:6],
         duration_ms=built.get("duration_ms"))
