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


def test_unsupported_type_is_refused_with_a_reason_not_a_server_error(
    client_with_temporary_projects_directory,
):
    client = client_with_temporary_projects_directory
    slug = _create_project(client)

    response = client.post(
        f"/api/projects/{slug}/sources",
        files={"file0": ("clip.mp4", b"not a document", "video/mp4")},
    )
    assert response.status_code == 400, response.text
    assert "supported types" in response.json()["detail"].lower()
    assert client.get(f"/api/projects/{slug}").json()["source"] is None


def test_a_project_takes_one_source_file(client_with_temporary_projects_directory):
    """One file runs through every layer, so an upload of several is refused
    whole: nothing is stored, and the reason says why."""
    client = client_with_temporary_projects_directory
    slug = _create_project(client)

    response = client.post(
        f"/api/projects/{slug}/sources",
        files=[
            ("file0", ("one.md", b"# content", "text/markdown")),
            ("file1", ("two.txt", b"more content", "text/plain")),
        ],
    )
    assert response.status_code == 400
    assert "one source file" in response.json()["detail"]
    assert client.get(f"/api/projects/{slug}").json()["sources"] == []


def test_a_second_file_replaces_the_first_only_when_asked(
    client_with_temporary_projects_directory,
):
    client = client_with_temporary_projects_directory
    slug = _create_project(client)
    client.post(f"/api/projects/{slug}/sources",
                files={"file0": ("first.md", b"# first", "text/markdown")})

    refused = client.post(f"/api/projects/{slug}/sources",
                          files={"file0": ("second.md", b"# second", "text/markdown")})
    assert refused.status_code == 400 and "Replace it" in refused.json()["detail"]
    assert client.get(f"/api/projects/{slug}").json()["source"]["name"] == "first.md"

    replaced = client.post(f"/api/projects/{slug}/sources?replace=true",
                           files={"file0": ("second.md", b"# second", "text/markdown")})
    assert replaced.status_code == 201, replaced.text
    assert replaced.json()["replaced"] == "first.md"
    project = client.get(f"/api/projects/{slug}").json()
    assert [s["name"] for s in project["sources"]] == ["second.md"]


def test_a_refused_replacement_keeps_the_source_as_it_was(
    client_with_temporary_projects_directory,
):
    client = client_with_temporary_projects_directory
    slug = _create_project(client)
    client.post(f"/api/projects/{slug}/sources",
                files={"file0": ("keep.md", b"# keep", "text/markdown")})

    response = client.post(f"/api/projects/{slug}/sources?replace=true",
                           files={"file0": ("empty.md", b"", "text/markdown")})
    assert response.status_code == 400 and "empty" in response.json()["detail"].lower()
    assert client.get(f"/api/projects/{slug}").json()["source"]["name"] == "keep.md"


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
    assert response.json()["was_in_extraction"] is False  # never extracted
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


def test_two_files_under_one_field_name_do_not_vanish_silently(
    client_with_temporary_projects_directory,
):
    """Reproduced with `curl -F files=@a -F files=@b`.

    Repeating a field name collapses the parts into a single entry that is not a
    file, so the route stored nothing, rejected nothing, and returned 201. The
    caller saw no error and no result -- the worst of both, and exactly the
    silent-write-loss class this project keeps closing.

    The contract asserted here is the outcome, not the wording: either the files
    are stored, or the request fails. Silent success is the bug.
    """
    client = client_with_temporary_projects_directory
    slug = _create_project(client, name="One Field Name")

    response = client.post(
        f"/api/projects/{slug}/sources",
        files=[
            ("files", ("a.md", b"# first", "text/markdown")),
            ("files", ("b.md", b"# second", "text/markdown")),
        ],
    )

    if response.status_code >= 400:
        return  # refused outright, which is an acceptable outcome

    payload = response.json()
    stored = payload["accepted"] + payload["rejected"]
    assert stored, (
        "the upload reported neither an accepted nor a rejected file, so the "
        "caller cannot tell that nothing was saved"
    )
