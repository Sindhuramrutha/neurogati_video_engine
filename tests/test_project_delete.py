"""Deleting a project: moved to the trash, not erased, and never under a render."""

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


def test_a_deleted_project_goes_to_the_trash_and_out_of_the_list(project_root):
    slug = operations.create_project("Old Draft")["slug"]
    (project_root / slug / "sources" / "notes.txt").write_text("kept")

    with TestClient(app=create_app()) as client:
        answer = client.delete(f"/api/projects/{slug}")
        listed = client.get("/api/projects").json()

    assert answer.status_code == 200 and answer.json()["moved_to"].startswith(".trash/old-draft-")
    assert slug not in [project["slug"] for project in listed]
    trashed = next((project_root / ".trash").iterdir())
    assert (trashed / "sources" / "notes.txt").read_text() == "kept", "recoverable"


def test_a_project_with_a_render_waiting_is_not_deleted(project_root):
    slug = operations.create_project("Rendering")["slug"]
    render_queue.hold_queue(True)
    RenderQueueStore().save(RenderQueue(paused=True, jobs=[QueueJob(slug=slug, status="queued")]))

    with TestClient(app=create_app()) as client:
        answer = client.delete(f"/api/projects/{slug}")

    assert answer.status_code == 400 and "render in the queue" in answer.json()["detail"]
    assert (project_root / slug / "project.json").exists()


def test_deleting_a_project_that_does_not_exist_says_so(project_root):
    with TestClient(app=create_app()) as client:
        assert client.delete("/api/projects/nope").status_code == 404
