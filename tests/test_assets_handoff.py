"""Assets & Design hand-off: later stages read only what was transferred, and
everything on the layer is decided by fixed rules or by a person."""

# ruff: noqa: F811
import pytest

from pipeline import operations
from pipeline.assets import FigureUse
from pipeline.assets_handoff import (
    RULES,
    assets_page,
    confirm_assets,
    confirmed_library,
    set_slide_wash,
)
from pipeline.extraction import ExtractionStore
from pipeline.operations import OperationFailed
from tests.test_assets_and_export import (  # noqa: F401
    picture_bytes,
    project_root,
    project_with_pictures,
)


def test_a_decision_reaches_later_stages_only_once_transferred(project_root):
    slug, project = project_with_pictures("Handoff", [("Figure 1", (400, 300), "source")])
    operations.refresh_asset_library(slug)
    confirm_assets(slug)
    figure_id = assets_page(slug)["figures"][0]["id"]

    operations.decide_figure(slug, figure_id, FigureUse.SKIP)

    assert [f.use for f in confirmed_library(project).figures] == [FigureUse.UNDECIDED]
    page = assets_page(slug)
    assert page["handoff"]["pending"] is True, "the page says there is something to transfer"

    confirm_assets(slug)
    assert [f.use for f in confirmed_library(project).figures] == [FigureUse.SKIP]
    assert assets_page(slug)["handoff"]["pending"] is False


def test_this_layer_lists_every_picture_and_judges_none(project_root):
    """No verdict here: every picture is handed on unless a person leaves it
    out. Whether one can fill a frame is a fact Generation uses, not a decision
    made on this layer."""
    from pipeline.assets import AssetLibraryStore, set_picture

    slug, project = project_with_pictures("Listed", [
        ("A diagram", (400, 300), "source"), ("A bullet", (20, 20), "source")])
    operations.refresh_asset_library(slug)
    page = assets_page(slug)
    figures = {f["caption"]: f for f in page["figures"]}

    assert "will_show" not in figures["A diagram"] and "reason" not in figures["A diagram"]
    assert [f["is_left_out"] for f in page["figures"]] == [False, False]
    assert page["audit"]["handed_on_count"] == 2, "the bullet is handed on too"
    assert figures["A bullet"]["fills_a_frame"] is False
    assert "64 px" in figures["A bullet"]["why_not_a_frame"]

    library = AssetLibraryStore(project.root).load()
    offered = [f.caption for f in library.usable()]
    assert offered == ["A diagram"], "only a picture that can fill a frame is offered"

    set_picture(slug, figures["A diagram"]["id"], {"left_out": True})
    page = assets_page(slug)
    assert page["audit"]["left_out_count"] == 1 and page["audit"]["handed_on_count"] == 1
    set_picture(slug, figures["A diagram"]["id"], {"left_out": False})
    assert assets_page(slug)["audit"]["left_out_count"] == 0


def test_gathering_twice_gives_the_same_library(project_root):
    """Deterministic: the same transfer and decisions give the same library."""
    slug, _ = project_with_pictures("Same", [
        ("One", (400, 300), "source"), ("Two", (300, 200), "source")])
    first = operations.refresh_asset_library(slug)["figures"]
    second = operations.refresh_asset_library(slug)["figures"]

    keep = ("id", "asset_path", "flags", "width", "height", "is_left_out", "shown_path")
    assert [{k: f[k] for k in keep} for f in first] == [{k: f[k] for k in keep} for f in second]


def test_transferring_a_library_gathered_from_an_older_transfer_is_refused(project_root):
    slug, project = project_with_pictures("Older", [("Figure 1", (400, 300), "source")])
    operations.refresh_asset_library(slug)
    extraction = ExtractionStore(project.root).load()
    extraction.confirmed_at = "2026-09-28T00:00:00+00:00"
    ExtractionStore(project.root).save(extraction)

    with pytest.raises(OperationFailed, match="Gather again"):
        confirm_assets(slug)


def test_the_slide_wash_is_a_choice_that_survives_gathering_again(project_root):
    slug, project = project_with_pictures("Wash", [("Figure 1", (400, 300), "source")])
    operations.refresh_asset_library(slug)
    set_slide_wash(slug, "inverted")
    operations.refresh_asset_library(slug)

    assert assets_page(slug)["look"]["slide_wash"] == "inverted"
    with pytest.raises(OperationFailed, match="not a slide wash"):
        set_slide_wash(slug, "psychedelic")


def test_a_project_from_before_transfers_keeps_rendering_what_it_had(project_root):
    slug, project = project_with_pictures("Legacy", [("Figure 1", (400, 300), "source")])
    operations.refresh_asset_library(slug)          # never transferred

    assert [f.caption for f in confirmed_library(project).figures] == ["Figure 1"]


def test_the_page_lists_every_rule_with_its_numbers(project_root):
    assert [rule["flag"] for rule in RULES] == [
        "decoration", "blank", "sliver", "tiny", "unreadable", "cut_off", "trimmed"]
    assert "64 px" in RULES[0]["test"] and "120 px" in RULES[3]["test"]


def test_a_picture_says_which_slide_it_came_from(project_root):
    from pipeline.assets import AssetLibraryStore
    from pipeline.extraction import ExtractionStore

    slug, project = project_with_pictures("Slides", [("Padma — figure 2 (slide 2)", (400, 300),
                                                      "source")])
    store = ExtractionStore(project.root)
    extraction = store.load()
    figure_block = next(b for b in extraction.documents[0].blocks if b.kind == "figure")
    figure_block.slide_number, figure_block.heading_path = 2, ["Padma's Story"]
    store.save(extraction)

    picture = operations.refresh_asset_library(slug)["figures"][0]
    assert (picture["slide_number"], picture["slide_title"]) == (2, "Padma's Story")
    assert picture["own_caption"] == "", "a label extraction gave it is not its caption"
    assert AssetLibraryStore(project.root).load().figures[0].slide_title == "Padma's Story"


def test_the_trimmed_copy_is_used_unless_the_original_is_chosen(project_root):
    from pipeline.assets import AssetLibraryStore, set_picture
    from pipeline.assets_handoff import fingerprint

    slug, project = project_with_pictures("Trim", [("A diagram", (400, 300), "source")])
    operations.refresh_asset_library(slug)
    page = assets_page(slug)
    picture = page["figures"][0]
    assert picture["prepared_path"] and picture["shown_path"] == picture["prepared_path"]
    assert page["picture_rules"]["trim_at"] == 0.03, "the page can say when it trims"
    before = fingerprint(AssetLibraryStore(project.root).load())

    set_picture(slug, picture["id"], {"use_original": True})
    chosen = assets_page(slug)["figures"][0]
    assert chosen["shown_path"] == chosen["asset_path"]
    assert fingerprint(AssetLibraryStore(project.root).load()) != before, \
        "a different file is handed on, so there is something to transfer"
    operations.refresh_asset_library(slug)
    assert assets_page(slug)["figures"][0]["use_original"], "kept when gathering again"


def test_a_crop_flag_names_the_edge_and_can_be_answered(project_root):
    from PIL import Image, ImageDraw

    from pipeline.assets import set_picture

    slug, project = project_with_pictures("Crop", [("A chart", (400, 300), "source")])
    image = Image.new("RGB", (400, 300), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([60, 60, 340, 200], outline="black", width=4)
    draw.rectangle([0, 288, 400, 300], fill="black")          # something cut at the bottom
    image.save(project.root / "extraction" / "assets" / "pic0.png")

    picture = operations.refresh_asset_library(slug)["figures"][0]
    assert "cut_off" in picture["flags"] and picture["cut_edges"] == ["bottom"]
    assert picture["needs_crop_check"] is True

    set_picture(slug, picture["id"], {"crop_checked": True})
    answered = assets_page(slug)["figures"][0]
    assert answered["needs_crop_check"] is False and answered["crop_checked"] is True
