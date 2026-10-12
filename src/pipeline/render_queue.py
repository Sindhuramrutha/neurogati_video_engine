"""The render queue: renders as jobs you line up, like an editor's Deliver page.

Rendering is not one button press. It is minutes a section, so it has to be
visible while it runs, and it has to be something you can manage: line several
up, reorder them, pause one, stop and delete one, retry one that failed, and
see what finished and how long it took. Pressing Render three times
would otherwise start three renders of the same video at once, each three times
slower, with nothing on screen to say so.

So renders go through one queue for the whole app (`projects/render-queue.json`):

- **One at a time.** A worker thread takes the first queued job, renders it,
  and moves on. Two renders at once only make both slower.
- **A job is a project to render, with its settings** (the voice). A project
  is in the queue at most once until that job finishes -- an unfinished render
  owns the project's working files.
- **Pause** stops the job at its next section boundary and keeps what it made
  (`render_job`); **Resume** puts it back in the queue, and it continues from
  there. **Delete** stops it if it runs and throws its work away. A finished
  job's video is never deleted with it; removing it only clears the list.
- **Survives the page.** The job runs on the server; reloading the page loses
  nothing, and the panel finds it again. If the app itself stops mid-render,
  the job is found as paused on the next start, its work kept, ready to resume.
"""

from __future__ import annotations

import logging
import threading
import time
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from pipeline import progress, render_job
from pipeline.core import OperationFailed, projects_root, require_project
from pipeline.storage.documents import JsonDocumentStore, new_identifier

logger = logging.getLogger(__name__)

MAXIMUM_JOBS_KEPT = 50
UNFINISHED = {"queued", "rendering", "paused", "failed"}


class QueueJob(BaseModel):
    id: str = Field(default_factory=new_identifier)
    slug: str
    project: str = ""
    voice_provider: str = ""
    voice: str = ""
    status: str = "queued"     # queued | rendering | paused | failed | done
    added_at: str = ""
    started_at: str = ""
    finished_at: str = ""
    render_seconds: int = 0    # time spent rendering, across pauses
    continues: bool = False    # a paused or failed job: carry on from its work
    deleting: bool = False     # delete asked for while it rendered
    video_file: str = ""
    duration_ms: int = 0
    message: str = ""


class RenderQueue(BaseModel):
    jobs: list[QueueJob] = Field(default_factory=list)
    paused: bool = False       # the whole queue held: nothing new starts


class RenderQueueStore(JsonDocumentStore[RenderQueue]):
    def __init__(self) -> None:
        super().__init__(
            document_path=projects_root() / "render-queue.json",
            model_type=RenderQueue, build_default=RenderQueue, description="render queue",
        )


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


# Every read-change-write of the queue holds this, the worker's included.
_lock = threading.RLock()
_wake = threading.Event()
_worker: threading.Thread | None = None
_worker_root = None


def _change(edit) -> RenderQueue:
    with _lock:
        store = RenderQueueStore()
        queue = store.load()
        edit(queue)
        return store.save(queue)


def _find(queue: RenderQueue, job_id: str) -> QueueJob:
    job = next((job for job in queue.jobs if job.id == job_id), None)
    if job is None:
        raise OperationFailed("That job is not in the render queue any more.")
    return job


# --- what the panel shows -----------------------------------------------------------


def queue_view() -> dict[str, Any]:
    ensure_worker()
    queue = RenderQueueStore().load()
    jobs = []
    for job in queue.jobs:
        entry = job.model_dump()
        if job.status == "rendering":
            live = progress.read(job.slug, render_job.JOB)
            entry["progress"] = live
        if job.status in {"paused", "failed", "rendering"}:
            record = render_job.job_view(job.slug)
            entry["sections"] = {"count": record["section_count"], "spoken": record["spoken"],
                                 "cut": record["cut"]}
            entry["partial_video"] = record["partial_video"]
        jobs.append(entry)
    return {
        "jobs": jobs,
        "paused": queue.paused,
        # Anything else running, so the panel is the one place to look.
        "activity": [entry for entry in progress.running() if entry["job"] != render_job.JOB],
    }


# --- what a person does -------------------------------------------------------------


def add_job(slug: str, voice_provider: str = "", voice: str = "") -> dict[str, Any]:
    """Put a project in the queue. Once: an unfinished job owns its working files."""
    project = require_project(slug)

    def edit(queue: RenderQueue) -> None:
        waiting = next((job for job in queue.jobs
                        if job.slug == slug and job.status in UNFINISHED), None)
        if waiting is not None:
            raise OperationFailed(
                f"{project.name} is already in the render queue ({waiting.status}). "
                f"Resume or delete that job instead of adding another.")
        queue.jobs.append(QueueJob(slug=slug, project=project.name,
                                   voice_provider=voice_provider, voice=voice, added_at=_now()))
        finished = [job for job in queue.jobs if job.status == "done"]
        for old in finished[:max(0, len(queue.jobs) - MAXIMUM_JOBS_KEPT)]:
            queue.jobs.remove(old)

    _change(edit)
    _wake.set()
    return queue_view()


def pause_job(job_id: str) -> dict[str, Any]:
    """Rendering: stop at the next section, keeping the work. Queued: hold it."""
    def edit(queue: RenderQueue) -> None:
        job = _find(queue, job_id)
        if job.status == "rendering":
            render_job.request_halt(job.slug)
        elif job.status == "queued":
            job.status = "paused"
        else:
            raise OperationFailed(f"A {job.status} job cannot be paused.")

    _change(edit)
    return queue_view()


def resume_job(job_id: str) -> dict[str, Any]:
    """Back in the queue, to carry on from what it made (paused or failed)."""
    def edit(queue: RenderQueue) -> None:
        job = _find(queue, job_id)
        if job.status not in {"paused", "failed"}:
            raise OperationFailed(f"A {job.status} job has nothing to resume.")
        job.status, job.message = "queued", ""
        job.continues = render_job.job_view(job.slug)["can_resume"]

    _change(edit)
    _wake.set()
    return queue_view()


def drop_project(slug: str) -> None:
    """Take every job of a project out of the queue, whatever its state (the project
    is being deleted: nothing of it is kept, and a render under way is stopped by
    `project_work.stop_everything`)."""
    def edit(queue: RenderQueue) -> None:
        queue.jobs = [job for job in queue.jobs if job.slug != slug]

    _change(edit)


def delete_job(job_id: str) -> dict[str, Any]:
    """Take a job out. Rendering, it stops at its next section and its work is
    deleted; otherwise its unfinished work is deleted now. A finished job's
    video stays -- only the list entry goes."""
    def edit(queue: RenderQueue) -> None:
        job = _find(queue, job_id)
        if job.status == "rendering":
            job.deleting = True
            render_job.request_halt(job.slug, discard=True)
            return
        if job.status in {"paused", "failed"}:
            render_job.discard(job.slug)
        queue.jobs.remove(job)

    _change(edit)
    return queue_view()


def move_job(job_id: str, step: int) -> dict[str, Any]:
    """Earlier (-1) or later (+1) among the jobs still waiting."""
    def edit(queue: RenderQueue) -> None:
        job = _find(queue, job_id)
        at = queue.jobs.index(job)
        to = at + (1 if step > 0 else -1)
        if 0 <= to < len(queue.jobs) and queue.jobs[to].status not in {"rendering", "done"}:
            queue.jobs[at], queue.jobs[to] = queue.jobs[to], queue.jobs[at]

    _change(edit)
    return queue_view()


def hold_queue(paused: bool) -> dict[str, Any]:
    """Hold the whole queue -- the running job finishes, nothing new starts --
    or let it go on."""
    _change(lambda queue: setattr(queue, "paused", bool(paused)))
    _wake.set()
    return queue_view()


def clear_finished() -> dict[str, Any]:
    _change(lambda queue: setattr(
        queue, "jobs", [job for job in queue.jobs if job.status != "done"]))
    return queue_view()


# --- the worker ---------------------------------------------------------------------


def ensure_worker() -> None:
    """Start the worker, once per projects folder. On its first start a job left
    "rendering" by a stopped app is found and marked paused, its work kept."""
    global _worker, _worker_root
    root = projects_root()
    with _lock:
        if _worker is not None and _worker.is_alive() and _worker_root == root:
            return
        _change(_recover)
        _worker_root = root
        _worker = threading.Thread(target=_work, args=(root,), name="render-queue", daemon=True)
        _worker.start()


def _recover(queue: RenderQueue) -> None:
    for job in queue.jobs:
        if job.status == "rendering" and not progress.read(job.slug, render_job.JOB)["active"]:
            job.status, job.continues = "paused", True
            job.message = "The app stopped while this was rendering. Its work is kept: resume it."


def _next_job() -> QueueJob | None:
    with _lock:
        store = RenderQueueStore()
        queue = store.load()
        if queue.paused:
            return None
        job = next((job for job in queue.jobs if job.status == "queued"), None)
        if job is None:
            return None
        job.status, job.message = "rendering", ""
        job.started_at = job.started_at or _now()
        store.save(queue)
        return job


def _work(root) -> None:
    while projects_root() == root:
        job = _next_job()
        if job is None:
            _wake.wait(timeout=2.0)
            _wake.clear()
            continue
        _run(job)


def _run(job: QueueJob) -> None:
    from pipeline.render_run import render_video

    started = time.monotonic()
    outcome: dict[str, Any] = {}
    failure = ""
    try:
        try:
            outcome = render_video(job.slug, job.voice_provider, job.voice, resume=job.continues)
        except OperationFailed as refused:
            if not job.continues:
                raise
            # Its work cannot be continued -- the plan or script changed, or it
            # is gone -- so it renders from the beginning instead.
            logger.info("render %s starts over: %s", job.id, refused)
            outcome = render_video(job.slug, job.voice_provider, job.voice)
            outcome.setdefault("warnings", []).append(
                f"Rendered from the beginning: {refused}")
    except Exception as error:   # the worker must outlive any one render
        logger.exception("render job %s failed", job.id)
        failure = str(error) or type(error).__name__

    def record(queue: RenderQueue) -> None:
        current = next((j for j in queue.jobs if j.id == job.id), None)
        if current is None:
            return
        current.render_seconds += round(time.monotonic() - started)
        if current.deleting or outcome.get("discarded"):
            queue.jobs.remove(current)
        elif failure:
            current.status, current.message = "failed", failure
            current.continues = True
        elif outcome.get("halted"):
            current.status, current.continues = "paused", True
        else:
            current.status, current.continues = "done", False
            current.finished_at = _now()
            current.video_file = outcome.get("video_file_name", "")
            current.duration_ms = int(outcome.get("duration_ms", 0))
            current.message = " · ".join(outcome.get("warnings", []))[:500]

    _change(record)
