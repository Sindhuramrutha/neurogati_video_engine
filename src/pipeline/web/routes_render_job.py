"""The render queue: adding jobs, pausing, resuming, deleting, reordering.

Rendering from the page goes through the queue -- one job at a time, on the
server, so it survives a reload. `POST /render` stays for scripts and the CLI.
Their own module so `routes_project.py` does not grow; the work is in
`pipeline.render_queue`.
"""

from __future__ import annotations

from typing import Any

from litestar import get, post
from litestar.exceptions import ClientException
from litestar.params import FromPath
from pydantic import BaseModel

from pipeline import render_queue
from pipeline.core import OperationFailed
from pipeline.render_job import job_view


class NewRenderJob(BaseModel):
    slug: str
    voice_provider: str = ""
    voice: str = ""


class QueueHold(BaseModel):
    paused: bool


def _client_error(call, *args) -> dict[str, Any]:
    try:
        return call(*args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/render-queue", sync_to_thread=False)
def get_render_queue() -> dict[str, Any]:
    """Every job -- rendering, waiting, paused, failed, finished -- and anything
    else running."""
    return _client_error(render_queue.queue_view)


@post("/api/render-queue", sync_to_thread=False)
def add_render_job(data: NewRenderJob) -> dict[str, Any]:
    """Add a project to the queue. It starts when the jobs before it are done."""
    return _client_error(render_queue.add_job, data.slug, data.voice_provider, data.voice)


@post("/api/render-queue/hold", sync_to_thread=False)
def hold_render_queue(data: QueueHold) -> dict[str, Any]:
    """Hold the queue (the running job finishes, nothing new starts), or release it."""
    return _client_error(render_queue.hold_queue, data.paused)


@post("/api/render-queue/clear-finished", sync_to_thread=False)
def clear_finished_render_jobs() -> dict[str, Any]:
    """Clear finished jobs from the list. Their videos stay."""
    return _client_error(render_queue.clear_finished)


@post("/api/render-queue/{job_id:str}/{action:str}", sync_to_thread=False)
def act_on_render_job(
    job_id: FromPath[str], action: FromPath[str], step: int = 0,
) -> dict[str, Any]:
    """pause | resume | delete | move (with `step` -1 or 1)."""
    actions = {
        "pause": lambda: render_queue.pause_job(job_id),
        "resume": lambda: render_queue.resume_job(job_id),
        "delete": lambda: render_queue.delete_job(job_id),
        "move": lambda: render_queue.move_job(job_id, step),
    }
    if action not in actions:
        raise ClientException(detail=f"{action!r} is not something a render job can do.")
    return _client_error(actions[action])


@get("/api/projects/{slug:str}/render/job", sync_to_thread=False)
def get_render_job(slug: FromPath[str]) -> dict[str, Any]:
    """A project's last render: how far it got and whether it can continue."""
    return _client_error(job_view, slug)


@post("/api/projects/{slug:str}/finish", sync_to_thread=False)
def finish_video(slug: FromPath[str]) -> dict[str, Any]:
    """Finish the video in one go: the scenes still missing or failing, the render,
    the export (`pipeline.finishing`)."""
    from pipeline import finishing

    return _client_error(finishing.start, slug)


@get("/api/projects/{slug:str}/finish", sync_to_thread=False)
def get_finish_status(slug: FromPath[str]) -> dict[str, Any]:
    from pipeline import finishing

    return _client_error(finishing.status, slug)


RENDER_JOB_ROUTES = [
    get_render_queue, add_render_job, hold_render_queue, clear_finished_render_jobs,
    act_on_render_job, get_render_job, finish_video, get_finish_status,
]
