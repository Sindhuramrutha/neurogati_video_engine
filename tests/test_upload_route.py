"""End-to-end upload tests through the real HTTP route.

The unit tests in test_sources.py prove the validator refuses traversal. These
prove the route actually uses it -- a validator nothing calls protects nothing.
"""

import pytest
from litestar.testing import TestClient

from pipeline.web.app import create_app


@pytest.fixture
def client_with_temporary_projects_directory(tmp_path, monkeypatch):
    """Point the app at a throwaway projects directory.

    get_settings is lru_cached, so the cache is cleared on the way in and out;
    otherwise this test would leak a temp path into every later test in the run.
    """
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path / "projects"))
    get_settings.cache_clear()

    import pipeline.web.routes_project as routes_project_module
    routes_project_module._service = None  # rebuild against the new settings

    with TestClient(app=create_app()) as client:
        yield client

    routes_project_module._service = None
    get_settings.cache_clear()


def _create_project(client, name="Audit Project"):
    response = client.post("/api/projects", json={"name": name})
    assert response.status_code in (200, 201), response.text
    return response.json()["slug"]


def test_traversal_filename_cannot_write_outside_the_project(
    client_with_temporary_projects_directory, tmp_path
):
    client = client_with_temporary_projects_directory
    slug = _create_project(client)

    response = client.post(
        f"/api/projects/{slug}/sources",
        files={"file0": ("../../../ESCAPED.md", b"pwned", "text/markdown")},
    )
    assert response.status_code == 201, response.text

    projects_root = tmp_path / "projects"
    escaped_candidates = [
        projects_root.parent / "ESCAPED.md",
        projects_root / "ESCAPED.md",
        tmp_path / "ESCAPED.md",
    ]
    for candidate in escaped_candidates:
        assert not candidate.exists(), f"file escaped to {candidate}"

    # It was either refused or stored safely inside sources/ -- never outside.
    stored = list((projects_root / slug / "sources").iterdir())
    for stored_file in stored:
        assert stored_file.parent == projects_root / slug / "sources"


def test_unsupported_type_is_reported_per_file_not_as_a_server_error(
    client_with_temporary_projects_directory,
):
    client = client_with_temporary_projects_directory
    slug = _create_project(client)

    response = client.post(
        f"/api/projects/{slug}/sources",
        files={"file0": ("clip.mp4", b"not a document", "video/mp4")},
    )
    assert response.status_code == 201, response.text
    payload = response.json()
    assert payload["accepted"] == []
    assert len(payload["rejected"]) == 1
    assert "supported types" in payload["rejected"][0]["reason"].lower()


def test_partial_success_keeps_the_good_files(
    client_with_temporary_projects_directory,
):
    """Dropping five files where one is bad must store the four good ones and say
    which failed -- not refuse the batch."""
    client = client_with_temporary_projects_directory
    slug = _create_project(client)

    response = client.post(
        f"/api/projects/{slug}/sources",
        files=[
            ("file0", ("good-one.md", b"# content", "text/markdown")),
            ("file1", ("clip.mp4", b"video", "video/mp4")),
            ("file2", ("good-two.txt", b"more content", "text/plain")),
        ],
    )
    assert response.status_code == 201, response.text
    payload = response.json()

    accepted_names = sorted(f["file_name"] for f in payload["accepted"])
    assert accepted_names == ["good-one.md", "good-two.txt"]
    assert [f["file_name"] for f in payload["rejected"]] == ["clip.mp4"]


def test_empty_file_is_rejected_with_a_reason(
    client_with_temporary_projects_directory,
):
    client = client_with_temporary_projects_directory
    slug = _create_project(client)

    response = client.post(
        f"/api/projects/{slug}/sources",
        files={"file0": ("empty.md", b"", "text/markdown")},
    )
    payload = response.json()
    assert payload["accepted"] == []
    assert "empty" in payload["rejected"][0]["reason"].lower()


def test_upload_to_a_missing_project_is_a_404_not_a_crash(
    client_with_temporary_projects_directory,
):
    client = client_with_temporary_projects_directory
    response = client.post(
        "/api/projects/no-such-project/sources",
        files={"file0": ("notes.md", b"x", "text/markdown")},
    )
    assert response.status_code == 404


def test_deleting_a_source_removes_it(client_with_temporary_projects_directory, tmp_path):
    client = client_with_temporary_projects_directory
    slug = _create_project(client)
    client.post(f"/api/projects/{slug}/sources",
                files={"file0": ("notes.md", b"# hi", "text/markdown")})

    response = client.delete(f"/api/projects/{slug}/sources/notes.md")
    assert response.status_code == 200, response.text
    assert response.json()["deleted"] == "notes.md"
    assert not (tmp_path / "projects" / slug / "sources" / "notes.md").exists()


def test_deleting_a_missing_source_is_a_404(client_with_temporary_projects_directory):
    client = client_with_temporary_projects_directory
    slug = _create_project(client)
    assert client.delete(f"/api/projects/{slug}/sources/ghost.md").status_code == 404


def test_delete_cannot_traverse_outside_the_sources_directory(
    client_with_temporary_projects_directory, tmp_path
):
    """The filename comes from the URL and is as untrusted as an upload filename.
    Regression guard for the deletion equivalent of the upload traversal."""
    client = client_with_temporary_projects_directory
    slug = _create_project(client)

    victim = tmp_path / "projects" / slug / "project.json"
    assert victim.exists()

    for hostile in ["..%2Fproject.json", "..%5Cproject.json", "%2E%2E%2Fproject.json"]:
        client.delete(f"/api/projects/{slug}/sources/{hostile}")
        assert victim.exists(), f"{hostile} deleted a file outside sources/"
