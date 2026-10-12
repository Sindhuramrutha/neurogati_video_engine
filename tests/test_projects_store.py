"""ProjectStore failure-path tests.

These cover the states a happy-path test never reaches: a partially created
project, a corrupt metadata file, a slug collision. Each one was a real defect
before it was a test.
"""

import json

import pytest

from pipeline.projects import ProjectStore
from pipeline.stages import Stage


def test_creating_a_project_lays_out_every_stage_directory(tmp_path):
    store = ProjectStore(tmp_path)
    project = store.create("Demystifying the Brain")

    assert project.slug == "demystifying-the-brain"
    assert project.sources_dir.is_dir()
    for stage in Stage:
        if stage is not Stage.INPUTS:
            assert project.stage_dir(stage).is_dir(), f"missing {stage.value}/"


def test_slug_collision_is_a_value_error_not_a_filesystem_error(tmp_path):
    """Different names can slugify to the same folder. The second create must
    fail as a handled 400, not a raw FileExistsError surfacing as a 500."""
    store = ProjectStore(tmp_path)
    store.create("The Brain")

    with pytest.raises(ValueError) as collision:
        store.create("the  BRAIN!!")  # same slug, different name
    assert "already uses the folder name" in str(collision.value)


def test_project_metadata_is_written_atomically(tmp_path):
    """No .tmp file may survive a successful create; an interrupted write must
    never leave a truncated project.json that _load then rejects."""
    store = ProjectStore(tmp_path)
    project = store.create("Atomic")

    assert project.meta_path.exists()
    assert not list(project.root.glob("*.tmp"))
    assert json.loads(project.meta_path.read_text(encoding="utf-8"))["name"] == "Atomic"


def test_corrupt_metadata_hides_the_project_but_is_logged_loudly(tmp_path, caplog):
    """A project that silently vanishes reads to a user as 'it deleted my work'.
    It stays hidden -- it genuinely cannot be read -- but must not be silent."""
    store = ProjectStore(tmp_path)
    project = store.create("Corruptible")
    project.meta_path.write_text("{ this is not json", encoding="utf-8")

    with caplog.at_level("ERROR"):
        assert store.get(project.slug) is None
        assert store.list() == []

    assert any("unreadable" in record.message for record in caplog.records), (
        "a corrupt project disappeared without any log line"
    )


def test_metadata_that_is_valid_json_but_not_an_object_is_rejected(tmp_path, caplog):
    store = ProjectStore(tmp_path)
    project = store.create("Listy")
    project.meta_path.write_text("[1, 2, 3]", encoding="utf-8")

    with caplog.at_level("ERROR"):
        assert store.get(project.slug) is None


def test_directories_without_metadata_are_ignored_silently(tmp_path, caplog):
    """Stray folders under projects/ are not errors and must not log noise."""
    (tmp_path / "not-a-project").mkdir()
    store = ProjectStore(tmp_path)

    with caplog.at_level("ERROR"):
        assert store.list() == []
    assert not caplog.records


def test_a_name_that_slugifies_to_nothing_still_produces_a_usable_project(tmp_path):
    store = ProjectStore(tmp_path)
    project = store.create("!!!")
    assert project.slug  # never empty
    assert project.name == "!!!"  # the display name is preserved verbatim
    assert store.get(project.slug) is not None


def test_deleting_a_project_requires_it_to_actually_be_one(tmp_path):
    """delete() must not remove an arbitrary directory that happens to be named
    like a slug."""
    store = ProjectStore(tmp_path)
    (tmp_path / "innocent-folder").mkdir()
    (tmp_path / "innocent-folder" / "important.txt").write_text("keep me")

    assert store.delete("innocent-folder") is False
    assert (tmp_path / "innocent-folder" / "important.txt").exists()
