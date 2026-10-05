"""The Look: which source it follows, and choices from that source's own palette
and fonts -- closed sets, applied the same way every time."""

# ruff: noqa: F811
import pytest

from pipeline import operations
from pipeline.assets import AssetLibraryStore
from pipeline.assets_handoff import assets_page, fingerprint
from pipeline.extraction import DocumentDesign, ExtractedDocument, ExtractionStore
from pipeline.operations import OperationFailed
from pipeline.project_look import ProjectLook, choose_look, effective_look
from tests.test_assets_and_export import (  # noqa: F401
    project_root,
    project_with_pictures,
)

BLUE = DocumentDesign(aspect_ratio="16:9", theme_name="Blue",
                      colours={"lt1": "#FFFFFF", "lt2": "#EEEEEE", "accent1": "#0000FF",
                               "accent2": "#FF8800", "dk2": "#223344"},
                      major_font="Georgia", minor_font="Verdana")
GREEN = DocumentDesign(aspect_ratio="4:3", theme_name="Green",
                       colours={"lt1": "#F0FFF0", "accent1": "#00AA00"}, major_font="Arial")


def two_decks():
    slug, project = project_with_pictures("Look", [("Figure", (400, 300), "source")], design=BLUE)
    store = ExtractionStore(project.root)
    extraction = store.load()
    extraction.documents.append(ExtractedDocument(file_name="green.pptx", design=GREEN))
    store.save(extraction)
    operations.refresh_asset_library(slug)
    return slug, project


def test_every_deck_with_styling_is_an_option(project_root):
    slug, _ = two_decks()
    sources = assets_page(slug)["look_options"]["sources"]
    assert [s["from_file"] for s in sources] == ["chapter.docx", "green.pptx"]


def test_choosing_a_deck_follows_it_and_the_renderer_look_is_an_option(project_root):
    slug, project = two_decks()
    choose_look(slug, {"from_file": "green.pptx"})
    look = AssetLibraryStore(project.root).load().look
    assert look.use_source_styling and look.from_file == "green.pptx"
    assert assets_page(slug)["look_preview"]["accent"] == "#00aa00"

    choose_look(slug, {"from_file": ""})
    assert not AssetLibraryStore(project.root).load().look.use_source_styling
    assert assets_page(slug)["look_preview"]["background"] == "#0d0f14", "the renderer's own"


def test_roles_take_the_decks_own_colours_and_fonts(project_root):
    slug, project = two_decks()
    choose_look(slug, {"from_file": "chapter.docx"})
    choose_look(slug, {"role": "accent", "value": "accent2"})
    choose_look(slug, {"role": "background", "value": "dk2"})
    choose_look(slug, {"role": "heading_font", "value": "body"})
    choose_look(slug, {"role": "body_font", "value": "renderer"})

    effective = effective_look(AssetLibraryStore(project.root).load().look)
    assert effective["colours"]["accent1"] == "#FF8800"
    assert effective["background_colour"] == "#223344"
    assert (effective["heading_font"], effective["body_font"]) == ("Verdana", "")
    preview = assets_page(slug)["look_preview"]
    assert preview["accent"] == "#ff8800" and preview["text"] != "#1a1816", "dark: light text"

    choose_look(slug, {"role": "accent", "value": ""})
    assert "accent" not in AssetLibraryStore(project.root).load().look.choices


def test_a_colour_may_be_any_colour_and_nothing_else_is_accepted(project_root):
    slug, project = two_decks()
    choose_look(slug, {"from_file": "chapter.docx"})

    choose_look(slug, {"role": "accent", "value": "#12ab56"})
    look = AssetLibraryStore(project.root).load().look
    assert look.choices["accent"] == "#12AB56", "a picked colour is kept as a colour"
    assert effective_look(look)["colours"]["accent1"] == "#12AB56"
    assert assets_page(slug)["look_preview"]["accent"] == "#12ab56"

    for wrong in ("blue", "#12", "accent99"):
        with pytest.raises(OperationFailed):
            choose_look(slug, {"role": "accent", "value": wrong})
    with pytest.raises(OperationFailed):
        choose_look(slug, {"role": "sparkle", "value": "accent1"})
    with pytest.raises(OperationFailed):
        choose_look(slug, {"from_file": "not-there.pptx"})


def test_a_chosen_panel_colour_is_honoured_on_a_light_background(project_root):
    """The renderer drew panels white on any light background, whatever was
    chosen. A control that does nothing is a lie; the choice is honoured."""
    from pipeline.project_look import style_for

    slug, project = two_decks()
    choose_look(slug, {"from_file": "chapter.docx"})
    look = AssetLibraryStore(project.root).load().look
    assert style_for(look, project.root).panel_colour == (255, 255, 255), "the default"

    choose_look(slug, {"role": "panels", "value": "accent2"})
    look = AssetLibraryStore(project.root).load().look
    assert style_for(look, project.root).panel_colour == (255, 136, 0)
    assert assets_page(slug)["look_preview"]["panel"] == "#ff8800"


def test_the_default_panel_always_suits_the_background(project_root):
    """On a dark background the renderer took its panel from the deck's light
    "lt2", which put light text on a light panel. With no panel chosen, the
    panel is made readable; a chosen one is left exactly as chosen."""
    slug, _ = two_decks()
    choose_look(slug, {"from_file": "chapter.docx"})
    choose_look(slug, {"role": "background", "value": "dk2"})      # dark, panel not chosen

    preview = assets_page(slug)["look_preview"]
    assert preview["background"] == "#223344"
    assert preview["panel"] == "#3a4b5c", "the background, lifted a little; not the light lt2"
    assert preview["readability"]["text_is_readable"]


def test_a_mid_tone_background_still_gets_a_panel_its_text_reads_on():
    from pipeline.project_look import READABLE_CONTRAST, _panel_that_reads, contrast

    light_text, mid_blue = (232, 234, 240), (68, 114, 196)
    panel = _panel_that_reads(mid_blue, light_text)
    assert contrast(light_text, panel) >= READABLE_CONTRAST
    assert panel < mid_blue, "stepped darker, away from the light text"
    assert panel == _panel_that_reads(mid_blue, light_text), "the same every time"

    dark_text, mid_grey = (26, 24, 22), (150, 150, 150)
    assert contrast(dark_text, _panel_that_reads(mid_grey, dark_text)) >= READABLE_CONTRAST


def test_the_page_says_how_well_the_text_reads(project_root):
    from pipeline.project_look import contrast

    assert contrast((0, 0, 0), (255, 255, 255)) == 21.0
    assert contrast((255, 255, 255), (255, 255, 255)) == 1.0

    slug, _ = two_decks()
    choose_look(slug, {"from_file": "chapter.docx"})
    fine = assets_page(slug)["look_preview"]["readability"]
    assert fine["text_is_readable"] and fine["text_on_panel"] > 10

    choose_look(slug, {"role": "panels", "value": "dk2"})   # chosen: dark text, dark panel
    poor = assets_page(slug)["look_preview"]["readability"]
    assert not poor["text_is_readable"] and poor["text_on_panel"] < poor["needed"]


def test_themes_are_starting_points_from_the_decks_own_palette(project_root):
    slug, project = two_decks()
    choose_look(slug, {"from_file": "chapter.docx"})
    themes = {t["key"]: t for t in assets_page(slug)["look_preview"]["themes"]}
    assert set(themes) == {"deck", "light", "accent"}, "no dark theme: this deck has no dk1"
    assert themes["deck"]["is_current"]

    choose_look(slug, {"role": "heading_font", "value": "body"})
    choose_look(slug, {"theme": "accent"})
    look = AssetLibraryStore(project.root).load().look
    assert look.choices == {"heading_font": "body", "background": "accent1",
                            "accent": "accent2"}, "fonts are kept"
    page = assets_page(slug)["look_preview"]
    assert page["background"] == "#0000ff" and page["chosen"]["accent"] == "#ff8800"
    assert {t["key"] for t in page["themes"] if t["is_current"]} == {"accent"}

    assert page["readability"]["text_is_readable"], "a theme is always readable"
    assert all(t["key"] != "dark" for t in page["themes"])
    with pytest.raises(OperationFailed):
        choose_look(slug, {"theme": "dark"})


def test_switching_decks_drops_choices_made_for_the_other(project_root):
    slug, project = two_decks()
    choose_look(slug, {"from_file": "chapter.docx"})
    choose_look(slug, {"role": "accent", "value": "accent2"})
    choose_look(slug, {"from_file": "green.pptx"})
    assert AssetLibraryStore(project.root).load().look.choices == {}


def test_gathering_again_keeps_the_chosen_deck_and_choices(project_root):
    slug, project = two_decks()
    choose_look(slug, {"from_file": "green.pptx"})
    choose_look(slug, {"role": "heading_font", "value": "renderer"})
    operations.refresh_asset_library(slug)
    look = AssetLibraryStore(project.root).load().look
    assert look.from_file == "green.pptx" and look.choices == {"heading_font": "renderer"}


def test_background_art_can_be_left_off():
    look = ProjectLook(colours={"lt1": "#FFFFFF"}, background_asset_path="extraction/assets/a.png",
                       background_art=False)
    assert effective_look(look)["background_asset_path"] == ""


def test_default_choices_leave_earlier_fingerprints_alone():
    import hashlib
    import json

    from pipeline.assets import AssetLibrary

    plain = AssetLibrary()
    before = plain.look.model_dump()
    del before["choices"], before["background_art"]
    digest = hashlib.sha256(json.dumps([[], before], sort_keys=True).encode()).hexdigest()[:20]
    assert fingerprint(plain) == digest, "older transfers not pending"
    assert fingerprint(AssetLibrary(look=ProjectLook(choices={"accent": "accent2"}))) != digest
