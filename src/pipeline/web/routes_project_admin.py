"""Deleting a project. Its own module so `routes_project.py` does not grow.

The folder is moved to `projects/.trash/`, not erased (`ProjectStore.delete`),
and a project with a render queued, running or paused is refused: deleting it
under a render would leave the queue pointing at nothing.
"""

from __future__ import annotations

from typing import Any

from litestar import delete
from litestar.exceptions import ClientException, NotFoundException
from litestar.params import FromPath

from pipeline import progress, render_queue
from pipeline.core import project_store


@delete("/api/projects/{slug:str}", status_code=200, sync_to_thread=False)
def delete_project(slug: FromPath[str]) -> dict[str, Any]:
    """Move a project to the trash. Refused while it has unfinished renders or
    anything else running."""
    store = project_store()
    project = store.get(slug)
    if project is None:
        raise NotFoundException(detail=f"no such project: {slug}")
    waiting = [job for job in render_queue.queue_view()["jobs"]
               if job["slug"] == slug and job["status"] in render_queue.UNFINISHED]
    if waiting:
        raise ClientException(detail=(
            f"{project.name} has a render in the queue ({waiting[0]['status']}). "
            f"Delete that render job first."))
    if any(entry["slug"] == slug for entry in progress.running()):
        raise ClientException(detail=f"{project.name} has work running. Wait for it to finish.")
    moved_to = store.delete(slug)
    return {"deleted": slug, "name": project.name,
            "moved_to": str(moved_to.relative_to(store.root)).replace("\\", "/")}


PROJECT_ADMIN_ROUTES = [delete_project]
