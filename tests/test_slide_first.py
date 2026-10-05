"""The deck's own slides, in the deck's own order.

A designed slide put through the old path came out as the renderer's template
with one extracted figure in a box -- the deck's background, typography and
layout all discarded. And nothing guaranteed the video even followed the deck:
sections were grouped by a model, so slides could be merged, reordered or
dropped and nothing said so.

Two promises are tested here, because both were broken:

1. **Every slide appears, in the deck's order.** Scenes may outnumber slides --
   a dense slide is narrated in several beats -- but never the reverse, and the
   slide a scene belongs to never goes backwards.
2. **A slide is shown, not rebuilt.** Its own background, pictures and text, and
   nothing of the renderer's drawn over them.
"""

from __future__ import annotations

import io

import pytest
from PIL import Image, ImageDraw

from pipeline import operations
from pipeline.slide_plan import coverage_of, plan_from_slides, slide_coverage, slides_in


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def a_deck(path, slides: int = 5, heading_size: int = 40):
    """A real .pptx with a heading in a plain text box on every slide.

    A text box, not a title placeholder, because that is how designed decks are
    actually built -- and it is exactly the case that used to come through as
    "Slide 7".
    """
    from pptx import Presentation
    from pptx.util import Emu, Inches, Pt

    presentation = Presentation()
    presentation.slide_width = Inches(16)
    presentation.slide_height = Inches(9)
    blank = presentation.slide_layouts[6]

    for number in range(1, slides + 1):
        slide = presentation.slides.add_slide(blank)
        box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(12), Inches(1.2))
        run = box.text_frame.paragraphs[0].add_run()
        run.text = f"Heading number {number}"
        run.font.size = Pt(heading_size)
        run.font.bold = True

        body = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(12), Inches(4))
        written = body.text_frame.paragraphs[0].add_run()
        written.text = (f"Slide {number} explains a particular idea in enough words "
                        f"to be worth narrating for a while.")
        written.font.size = Pt(16)
        assert Emu(1).inches >= 0    # the import is load-bearing above
    presentation.save(str(path))
    return path


def a_deck_project(name: str, slides: int = 5):
    slug = operations.create_project(name)["slug"]
    project = operations.require_project(slug)
    (project.root / "sources").mkdir(parents=True, exist_ok=True)
    a_deck(project.root / "sources" / "deck.pptx", slides=slides)
    operations.run_extraction(slug, "deck.pptx")
    operations.confirm_extraction(slug)
    return slug, project


# --- every slide, in order ----------------------------------------------------------


def test_a_plan_built_from_a_deck_has_one_section_per_slide_in_order(project_root):
    slug, _ = a_deck_project("Ordered", slides=7)

    built = plan_from_slides(slug)

    assert built["slide_count"] == 7
    assert built["section_count"] == 7
    assert built["coverage"]["is_complete"]
    assert [s["title"] for s in built["sections"]] == [
        "Opening", *(f"Heading number {n}" for n in range(1, 8)), "Recap", "Close",
    ], "the sections must follow the deck, carry its own headings, inside the lesson frame"
    assert all(s["rendering_approach"] == "slide"
               for s in built["sections"] if s["role"] == "teach")


def test_the_deck_s_own_heading_survives_even_without_a_title_placeholder(project_root):
    """Designed decks set headings as plain text boxes. Every slide used to come
    through as "Slide 7", which lost the one line the author most wanted kept."""
    slug, _project = a_deck_project("Headings", slides=3)

    from pipeline.extraction import ExtractionStore

    project = operations.require_project(slug)
    slides = slides_in(ExtractionStore(project.root).load())

    assert [s["title"] for s in slides] == [f"Heading number {n}" for n in (1, 2, 3)]
    assert not any(s["title"].startswith("Slide ") for s in slides)


def test_a_kicker_above_a_title_does_not_become_the_heading(project_root):
    """"4.Chapter" over "Networks that Learn" is a label above a title. The
    larger of two near-equal sizes is not reliably the heading; the longer is."""
    from pptx import Presentation
    from pptx.util import Inches, Pt

    slug = operations.create_project("Kicker")["slug"]
    project = operations.require_project(slug)
    (project.root / "sources").mkdir(parents=True, exist_ok=True)

    presentation = Presentation()
    presentation.slide_width, presentation.slide_height = Inches(16), Inches(9)
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    for text, size, top in (("4.Chapter", 40, 0.5), ("Networks that Learn", 39, 1.3)):
        box = slide.shapes.add_textbox(Inches(7), Inches(top), Inches(6), Inches(0.8))
        run = box.text_frame.paragraphs[0].add_run()
        run.text, run.font.size = text, Pt(size)
    presentation.save(str(project.root / "sources" / "deck.pptx"))
    operations.run_extraction(slug, "deck.pptx")
    operations.confirm_extraction(slug)

    built = plan_from_slides(slug)
    assert built["sections"][1]["title"] == "Networks that Learn"


def test_scenes_may_outnumber_slides_but_never_the_reverse(project_root):
    slug, project = a_deck_project("Counting", slides=4)
    plan_from_slides(slug)

    from pipeline.scripting import Script, ScriptScene, ScriptStore, SectionScript

    sections = operations.read_artifact(slug, "plan")["sections"]
    # Slide 2 is dense enough for three beats; the rest take one each.
    ScriptStore(project.root).save(Script(section_scripts=[
        SectionScript(
            section_id=section["id"],
            scenes=[ScriptScene(narration=f"Beat {beat}.", brief="x")
                    for beat in range(1, 4 if index == 1 else 2)],
        )
        for index, section in enumerate(sections)
    ]))

    coverage = slide_coverage(slug)
    assert coverage["slide_count"] == 4
    assert coverage["scene_count"] == 6, "three beats on slide 2, one on each of the rest"
    assert coverage["follows_the_deck"]
    assert coverage["warnings"] == []


def test_a_dropped_slide_is_reported_rather_than_rendered_anyway(project_root):
    """The guarantee has to be checkable, because a re-plan or a hand edit can
    break it silently and the video would just be missing a slide."""
    slug, project = a_deck_project("Dropped", slides=5)
    plan_from_slides(slug)

    from pipeline.planning import PlanStore

    store = PlanStore(project.root)
    plan = store.load()
    plan.sections = [s for s in plan.sections if s.id != "slide-003"]
    store.save(plan)

    coverage = slide_coverage(slug)
    assert coverage["missing_slides"] == [3]
    assert not coverage["follows_the_deck"]
    assert any("not covered" in warning for warning in coverage["warnings"])


def test_sections_out_of_the_deck_s_order_are_reported():
    """Order is checked separately from coverage: every slide can be present and
    the video still not follow the deck."""
    slides = [{"number": n} for n in (1, 2, 3)]

    class Section:
        def __init__(self, number):
            self.sources = [type("Ref", (), {"slide_number": number})()]

    jumbled = coverage_of(slides, [Section(2), Section(1), Section(3)])

    assert jumbled["missing_slides"] == []
    assert not jumbled["is_in_order"]
    assert not jumbled["is_complete"]


# --- the slide is shown, not rebuilt ------------------------------------------------


def test_a_slide_scene_shows_the_composed_slide_and_says_which_one(project_root):
    slug, project = a_deck_project("Shown", slides=3)
    plan_from_slides(slug)

    from pipeline.scripting import Script, ScriptScene, ScriptStore, SectionScript

    sections = operations.read_artifact(slug, "plan")["sections"]
    ScriptStore(project.root).save(Script(section_scripts=[
        SectionScript(section_id=s["id"],
                      scenes=[ScriptScene(narration="Some narration here.", brief="x")])
        for s in sections
    ]))

    planned = operations.plan_visuals(slug)
    # The lesson frame shows words; each slide section shows its slide.
    assert [v["kind"] for v in planned["visuals"]] == ["text", *["slide"] * 3, "text", "text"]
    assert [v["slide_number"] for v in planned["visuals"]] == [0, 1, 2, 3, 0, 0]

    built = operations.build_visuals(slug)
    assert built["audit"]["slides"] == 3
    for visual in (v for v in built["visuals"] if v["slide_number"]):
        assert visual["asset_path"].startswith("generation/slides/")
        assert (project.root / visual["asset_path"]).exists()
        # Its own heading, verbatim, and no composed labels: the slide already
        # carries its text where the author put it.
        assert visual["headline"] == f"Heading number {visual['slide_number']}"
        assert visual["points"] == []


def test_a_composed_slide_carries_the_deck_s_own_pixels(project_root):
    """Not "was handed a path" -- drawn. A recognisable mark on the slide has to
    survive into the frame."""
    from pptx import Presentation
    from pptx.util import Inches

    from pipeline.slide_frame import compose_slide

    slug = operations.create_project("Pixels")["slug"]
    project = operations.require_project(slug)
    (project.root / "sources").mkdir(parents=True, exist_ok=True)

    picture = Image.new("RGB", (800, 600), (0, 0, 255))
    ImageDraw.Draw(picture).rectangle([(10, 10), (790, 590)], outline=(0, 0, 200), width=8)
    buffer = io.BytesIO()
    picture.save(buffer, format="PNG")

    presentation = Presentation()
    presentation.slide_width, presentation.slide_height = Inches(16), Inches(9)
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    buffer.seek(0)
    slide.shapes.add_picture(buffer, Inches(0), Inches(0), Inches(16), Inches(9))
    deck = project.root / "sources" / "deck.pptx"
    presentation.save(str(deck))

    composed = compose_slide(deck, 1, project.root / "slide.png")
    with Image.open(composed.path) as frame:
        blues = sum(1 for pixel in frame.convert("RGB").getdata()
                    if pixel[2] > 150 > pixel[0])

    assert frame.size == (1920, 1080)
    assert blues > 1_500_000, f"the slide's own artwork is not on the frame ({blues} px)"


def test_a_full_bleed_shot_has_nothing_of_ours_drawn_over_it(project_root):
    """The slide already has its heading, its body text and its artwork exactly
    where they belong. Every mark this renderer adds is on somebody's layout."""
    from pipeline.rendering import RenderedSection, Shot, _fill_frame, section_segments

    slide = project_root / "slide.png"
    Image.new("RGB", (1920, 1080), (12, 200, 90)).save(slide)

    filled = _fill_frame(slide)
    greens = sum(1 for pixel in filled.getdata() if pixel[1] > 150 > pixel[0])
    assert greens == 1920 * 1080, "a 16:9 slide should land edge to edge"

    # And the renderer treats such a shot as carrying its own words.
    section = RenderedSection("s1", "A section", "Some narration here.",
                              audio_duration_ms=4_000,
                              shots=[Shot(picture=slide, full_bleed=True,
                                          headline="ignored", points=["ignored"])])
    assert [s.kind for s in section_segments(section)] == ["slide"]


def test_a_letterboxed_deck_keeps_its_whole_layout(project_root):
    """A 4:3 deck is letterboxed rather than cropped: losing a centimetre of
    somebody's layout to fill the frame is not a trade worth making."""
    from pipeline.rendering import _fill_frame

    slide = project_root / "slide43.png"
    Image.new("RGB", (1024, 768), (200, 30, 30)).save(slide)

    filled = _fill_frame(slide)
    reds = sum(1 for pixel in filled.getdata() if pixel[0] > 150 > pixel[1])

    assert filled.size == (1920, 1080)
    # 4:3 in 16:9 fills three quarters of the width, and none of it is cropped.
    assert 0.70 < reds / (1920 * 1080) < 0.80
