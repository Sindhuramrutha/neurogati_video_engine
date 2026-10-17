"""Deleting a project. Its own module so `routes_project.py` does not grow.

The folder is erased for good (`ProjectStore.delete`): there is no trash and no
recovery. And it always works: whatever is running in the project -- scenes being
made, a render, queued jobs, their ffmpeg and browser processes -- is stopped first
(`stop_everything`), then the folder is erased.
"""

from __future__ import annotations

import time
from typing import Any

from litestar import delete
from litestar.exceptions import NotFoundException
from litestar.params import FromPath

from pipeline import progress, project_work, render_queue, scene_agent
from pipeline.core import project_store

STOP_WAIT_SECONDS = 30      # at most this long for running work to notice it was stopped


def _still_running(slug: str) -> bool:
    return scene_agent.is_working(slug) or any(
        entry["slug"] == slug for entry in progress.running())


def stop_and_wait(slug: str) -> None:
    """Stop everything running for a project, and give it a moment to let go."""
    scene_agent.stop_all(slug)                   # the queue is dropped
    render_queue.drop_project(slug)              # its jobs go from the queue
    project_work.stop_everything(slug)           # work stops; its processes are killed
    deadline = time.monotonic() + STOP_WAIT_SECONDS
    while _still_running(slug) and time.monotonic() < deadline:
        time.sleep(0.25)


def _erase(store, slug: str) -> None:
    stop_and_wait(slug)
    store.delete(slug)
    # Work that was slow to let go may have written a little back: erase that too.
    time.sleep(0.5)
    if (store.root / slug).exists():
        import shutil
        shutil.rmtree(store.root / slug, ignore_errors=True)


@delete("/api/projects/{slug:str}", status_code=200, sync_to_thread=False)
def delete_project(slug: FromPath[str]) -> dict[str, Any]:
    """Erase a project for good, whatever is running in it: that is stopped first."""
    store = project_store()
    project = store.get(slug)
    if project is None:
        raise NotFoundException(detail=f"no such project: {slug}")
    _erase(store, slug)
    return {"deleted": slug, "name": project.name}


@delete("/api/projects", status_code=200, sync_to_thread=False)
def delete_every_project() -> dict[str, Any]:
    """Erase every project for good, each the way one is: what runs in it is stopped
    first. One that cannot be erased is named; the others are still erased."""
    store = project_store()
    deleted, failed = [], []
    for project in store.list():
        try:
            _erase(store, project.slug)
            deleted.append(project.name)
        except OSError as failure:
            failed.append(f"{project.name}: {failure}")
    return {"deleted": deleted, "failed": failed}


PROJECT_ADMIN_ROUTES = [delete_project, delete_every_project]
