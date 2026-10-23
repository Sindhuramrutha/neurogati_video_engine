"""Only the deck pictures a person chose reach the video: a video built from all of
the deck's pictures looked like its slides."""

import pytest

from pipeline import chosen_pictures, operations
from pipeline.assets import AssetLibraryStore
from pipeline.core import OperationFailed
from tests.test_assets_and_export import project_root, project_with_pictures  # noqa: F401


@pytest.mark.real_picks
def test_only_the_chosen_pictures_are_handed_on_under_their_names(project_root):  # noqa: F811
    slug, project = project_with_pictures("Picks", [
        ("Figure 1", (800, 600), "source"), ("Figure 2", (800, 600), "source"),
        ("Figure 3", (800, 600), "source"), ("Figure 4", (800, 600), "source")])
    library = operations.refresh_asset_library(slug)
    paths = [f["asset_path"] for f in library["figures"]]
    assert operations.read_asset_library(slug)["audit"]["handed_on_count"] == 0, \
        "nothing from the deck until a person chooses"

    chosen_pictures.choose(slug, paths[1], "Galvani's frog")
    handed = AssetLibraryStore(project.root).load().handed_on()
    assert [f.asset_path for f in handed] == [paths[1]]
    assert handed[0].name == "Galvani's frog"

    for path in paths[:3]:
        chosen_pictures.choose(slug, path, f"Picture {path[-6:]}")
    with pytest.raises(OperationFailed, match="At most 3"):
        chosen_pictures.choose(slug, paths[3], "One too many")
    with pytest.raises(OperationFailed, match="name"):
        chosen_pictures.choose(slug, paths[3], "  ")

    chosen_pictures.choose(slug, paths[1], keep=False)
    assert len(chosen_pictures.view(slug)["chosen"]) == 2
