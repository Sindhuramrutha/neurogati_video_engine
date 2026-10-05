"""The render queue: one job at a time through a worker, paused, resumed,
deleted, and found again after the app stopped."""
# The fixtures are shared with the render-job tests by import, which ruff
# reads as redefinition when a test takes them as arguments.
# ruff: noqa: F811

import time

import pytest

from pipeline import render_job, render_queue
from pipeline.operations import OperationFailed
from pipeline.render_queue import QueueJob, RenderQueue, RenderQueueStore
from tests.test_render_job import fakes, project_root, three_sections  # noqa: F401


def wait_for(condition, seconds=15.0):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        view = render_queue.queue_view()
        if condition(view):
            return view
        time.sleep(0.1)
    raise AssertionError(f"timed out; queue was {render_queue.queue_view()}")


def statuses(view):
    return [job["status"] for job in view["jobs"]]


def test_a_job_added_to_the_queue_is_rendered(project_root, fakes):
    slug, project = three_sections("Queued")
    render_queue.add_job(slug, "silent")

    view = wait_for(lambda v: statuses(v) == ["done"])

    job = view["jobs"][0]
    render_id = render_job.RenderJobStore(project.root).load().render_id
    assert job["video_file"] == f"{slug}-{render_id}.mp4"
    assert (project.root / "reviewing" / "output" / job["video_file"]).exists()


def test_a_project_is_in_the_queue_once_until_it_finishes(project_root, fakes):
    slug, _ = three_sections("Once")
    render_queue.hold_queue(True)
    render_queue.add_job(slug)
    with pytest.raises(OperationFailed, match="already in the render queue"):
        render_queue.add_job(slug)


def test_a_paused_job_resumes_from_where_it_stopped(project_root, fakes):
    slug, _ = three_sections("Paused")
    fakes.update(slug=slug, halt_after_cut=0)
    render_queue.add_job(slug)
    view = wait_for(lambda v: statuses(v) == ["paused"])
    assert view["jobs"][0]["sections"]["cut"] == 1 and view["jobs"][0]["partial_video"]

    fakes.update(spoken=[], cut=[], halt_after_cut=None)
    render_queue.resume_job(view["jobs"][0]["id"])
    wait_for(lambda v: statuses(v) == ["done"])

    assert fakes["spoken"] == [] and fakes["cut"] == [1, 2], "carried on, nothing redone"


def test_deleting_a_paused_job_deletes_its_work(project_root, fakes):
    slug, project = three_sections("Deleted")
    fakes.update(slug=slug, halt_after_cut=0)
    render_queue.add_job(slug)
    view = wait_for(lambda v: statuses(v) == ["paused"])

    render_queue.delete_job(view["jobs"][0]["id"])

    assert render_queue.queue_view()["jobs"] == []
    assert not list((project.root / "reviewing" / "output" / "frames").glob("*"))


def test_a_held_queue_starts_nothing_until_released(project_root, fakes):
    slug, _ = three_sections("Held")
    render_queue.hold_queue(True)
    render_queue.add_job(slug)
    time.sleep(0.5)
    assert statuses(render_queue.queue_view()) == ["queued"]

    render_queue.hold_queue(False)
    wait_for(lambda v: statuses(v) == ["done"])


def test_a_job_left_rendering_by_a_stopped_app_is_found_paused(project_root, fakes):
    slug, _ = three_sections("Crashed")
    RenderQueueStore().save(RenderQueue(jobs=[QueueJob(slug=slug, status="rendering")]))
    render_queue._worker = None           # as on a fresh start of the app

    job = render_queue.queue_view()["jobs"][0]

    assert job["status"] == "paused" and "stopped while this was rendering" in job["message"]
