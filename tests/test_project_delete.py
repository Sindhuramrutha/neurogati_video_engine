"""Deleting a project: erased for good (no trash), and never under a render."""

import pytest
from litestar.testing import TestClient

from pipeline import operations, render_queue
from pipeline.render_queue import QueueJob, RenderQueue, RenderQueueStore
from pipeline.web.app import create_app


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def test_a_deleted_project_is_erased_for_good_with_no_trash(project_root):
    import os
    import stat

    slug = operations.create_project("Old Draft")["slug"]
    notes = project_root / slug / "sources" / "notes.txt"
    notes.write_text("gone")
    os.chmod(notes, stat.S_IREAD)            # a read-only file does not stop it

    with TestClient(app=create_app()) as client:
        answer = client.delete(f"/api/projects/{slug}")
        listed = client.get("/api/projects").json()

    assert answer.status_code == 200 and answer.json() == {"deleted": slug, "name": "Old Draft"}
    assert slug not in [project["slug"] for project in listed]
    assert not (project_root / slug).exists(), "the folder is gone"
    assert not (project_root / ".trash").exists(), "and nothing was kept anywhere"


def test_a_project_with_a_render_queued_is_still_deleted_and_its_job_dropped(project_root):
    slug = operations.create_project("Rendering")["slug"]
    another = operations.create_project("Another")["slug"]
    render_queue.hold_queue(True)
    RenderQueueStore().save(RenderQueue(paused=True, jobs=[
        QueueJob(slug=slug, status="queued"), QueueJob(slug=another, status="queued")]))

    with TestClient(app=create_app()) as client:
        answer = client.delete(f"/api/projects/{slug}")

    assert answer.status_code == 200 and not (project_root / slug).exists()
    assert [job.slug for job in RenderQueueStore().load().jobs] == [another], \
        "its job went; another project's stayed"


def test_a_job_whose_project_is_gone_leaves_the_queue_when_it_starts(project_root,
                                                                     monkeypatch):
    """A project deleted before deleting dropped its jobs -- or by hand -- left a
    finished render listed for good, for a project nobody could open."""
    kept = operations.create_project("Kept")["slug"]
    RenderQueueStore().save(RenderQueue(paused=True, jobs=[
        QueueJob(slug="module-2", status="done"), QueueJob(slug=kept, status="done")]))
    monkeypatch.setattr(render_queue, "_worker", None)

    render_queue.ensure_worker()

    assert [job.slug for job in RenderQueueStore().load().jobs] == [kept]


def test_deleting_kills_what_is_running_for_the_project(project_root):
    import sys
    import threading
    import time

    from pipeline import project_work

    slug = operations.create_project("Busy")["slug"]
    started, result = threading.Event(), {}

    def work():
        with project_work.working_on(slug):
            started.set()
            try:
                project_work.run([sys.executable, "-c", "import time; time.sleep(60)"],
                                 timeout=120)
            except Exception as ended:       # noqa: BLE001 -- what it ended with is the point
                result["ended"] = type(ended).__name__
            result["told_to_stop"] = project_work.stopped()

    thread = threading.Thread(target=work)
    thread.start()
    assert started.wait(5)
    time.sleep(1)                                 # the process is really running
    began = time.monotonic()

    with TestClient(app=create_app()) as client:
        answer = client.delete(f"/api/projects/{slug}")

    thread.join(15)
    assert answer.status_code == 200 and not (project_root / slug).exists()
    assert not thread.is_alive() and time.monotonic() - began < 20, "it did not wait 60 s"
    assert result["told_to_stop"], "the work was told the project was stopped"


def test_work_started_after_a_deletion_is_not_stopped_by_it(project_root):
    from pipeline import project_work

    project_work.stop_everything("same-name")          # an old project of this name was deleted
    with project_work.working_on("same-name"):          # a new one, made afterwards
        assert not project_work.stopped()


def test_work_in_another_process_stops_when_its_project_is_deleted(project_root):
    """v8 was deleted on the page while a command-line run made its scenes: that run's
    process never heard the stop, and wrote the folder back. Work also asks the folder:
    gone, or now another project of the same name, and it is stopped."""
    import shutil
    import time

    from pipeline import project_work

    slug = operations.create_project("Elsewhere")["slug"]
    with project_work.working_on(slug):
        assert not project_work.stopped()
        shutil.rmtree(project_root / slug)            # deleted by another process
        assert project_work.stopped()
        time.sleep(1.1)                               # a later creation time
        operations.create_project("Elsewhere")        # a new project, same name
        assert project_work.stopped(), "the new project is not the old one's work"


def test_deleting_a_project_that_does_not_exist_says_so(project_root):
    with TestClient(app=create_app()) as client:
        assert client.delete("/api/projects/nope").status_code == 404


def test_every_project_can_be_deleted_at_once(project_root):
    """The project menu's "Delete all": each erased the way one is, nothing kept."""
    slugs = [operations.create_project(name)["slug"] for name in ("One", "Two", "Three")]

    with TestClient(app=create_app()) as client:
        answer = client.delete("/api/projects")
        listed = client.get("/api/projects").json()

    assert answer.status_code == 200
    assert sorted(answer.json()["deleted"]) == ["One", "Three", "Two"]
    assert answer.json()["failed"] == []
    assert listed == [] and not any((project_root / slug).exists() for slug in slugs)
