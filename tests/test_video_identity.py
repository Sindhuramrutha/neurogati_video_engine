"""What the video is -- its course, which part, what it teaches -- and that every
picture the person chose is placed somewhere in it."""

from types import SimpleNamespace

from pipeline.plan_agent import _unshown_chosen
from pipeline.plan_answers import ShapeAnswer, ShapeSection
from pipeline.video_identity import deck_defaults, title_slide_text


def deck(file_name, *blocks):
    return SimpleNamespace(documents=[SimpleNamespace(file_name=file_name, blocks=[
        SimpleNamespace(slide_number=slide, kind=kind, text=text, asset_path="")
        for slide, kind, text in blocks])])


def test_the_course_and_part_come_from_the_deck():
    """A whole video was narrated without once saying which course it belongs to."""
    chapter = deck("Demystifying-the-Brain Chapter 1.pptx",
                   (1, "heading", "Demystifying the Brain"),
                   (1, "paragraph", "A Computational Approach"),
                   (2, "heading", "Cognitive Complexity"))

    assert deck_defaults(chapter) == ("Demystifying the Brain", "Chapter 1")
    assert title_slide_text(chapter) == "Demystifying the Brain | A Computational Approach"


def shape(*sections):
    return ShapeAnswer(reply="", shortest_minutes=30, longest_minutes=40,
                       length_understood="About 35 min.", sections=[
                           ShapeSection(title=t, units=u, how="", minutes=5, scenes=2,
                                        summary="", shows_chosen=list(names))
                           for t, u, names in sections])


def test_a_chosen_picture_off_every_taught_slide_must_be_placed_by_name():
    """The title slide's cover was planned as 'a title page' and never shown."""
    cover = [{"path": "f.png", "name": "Book cover", "slide": 1}]

    assert _unshown_chosen(shape(("Body", [2, 3], [])), cover), "no section shows it"
    assert not _unshown_chosen(shape(("Opening", [], ["book cover"]), ("Body", [2, 3], [])),
                               cover), "placed by name in the opening"
    assert not _unshown_chosen(shape(("Opening", [1, 2], [])), cover), "its slide is taught"


def test_what_the_video_teaches_is_never_cut_inside_a_word():
    """v8's was cut at 400 characters to '...localization, con'."""
    from pipeline.planning import LONGEST_TEACHES, Plan

    long = "You will trace the brain's story. " * 40
    kept = Plan(teaches=long).teaches
    assert len(kept) <= LONGEST_TEACHES and kept.endswith("story.")
    assert Plan(teaches="Short and whole.").teaches == "Short and whole."
