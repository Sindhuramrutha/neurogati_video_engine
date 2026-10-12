"""The text checks a scene program's layout goes through, on layouts written by
hand: the same layout always gives the same results."""

from pipeline.scene_checks import duration_check, renderer_check, text_checks

BRIEF = {"width": 1920, "height": 1080, "narration": "Padma lost her father, and guilt began.",
         "on_screen": "", "source_text": "Loss and Guilt", "section_title": "The Descent",
         "headline": ""}


def piece(text, box, color="#e8eaf0", behind="#0d0f14", line_height=60):
    return {"text": text, "box": box, "color": color, "behind": behind,
            "line_height": line_height}


def results(snapshots):
    return {c["key"]: c["status"] for c in text_checks({"snapshots": snapshots}, BRIEF)}


def test_a_clean_beat_passes():
    found = results([{"at": 1.0, "graphics": 3, "texts": [
        piece("Loss and Guilt", [200, 100, 900, 180]),
        piece("Padma lost her father", [200, 600, 1100, 680])]}])
    assert set(found.values()) <= {"pass", "n/a"}, found


def test_text_outside_the_margin_overlapping_faint_or_small_fails():
    found = results([{"at": 1.0, "graphics": 3, "texts": [
        piece("Loss and Guilt", [20, 100, 900, 180]),                       # in the margin
        piece("guilt began", [500, 120, 1100, 200]),                         # overlaps it
        piece("her father", [300, 600, 700, 660], color="#1a1d24"),          # faint
        piece("Padma", [300, 800, 500, 820], line_height=20)]}])             # small
    assert found["bounds"] == found["overlap"] == "fail"
    assert found["contrast"] == found["legible"] == "fail"


def test_a_paragraph_on_screen_fails():
    words = " ".join(["guilt"] * 20)
    assert results([{"at": 1.0, "graphics": 3, "texts": [
        piece(words, [200, 200, 1700, 400])]}])["paragraphs"] == "fail"


def test_words_and_numbers_not_in_the_narration_or_source_fail():
    found = results([{"at": 1.0, "graphics": 3, "texts": [
        piece("Seventeen percent recover", [200, 200, 1200, 280]),
        piece("1999", [200, 500, 400, 560])]}])
    assert found["grounded"] == "fail"


def test_animated_quotations_are_not_a_picture_of_the_idea():
    words_only = [{"at": t, "graphics": 0, "texts": [piece("Loss and Guilt",
                                                          [200, 100, 900, 180])]}
                  for t in (1.0, 2.0, 3.0)]
    assert results(words_only)["pictured"] == "fail"


def test_renderer_and_length():
    assert renderer_check("from manim import Text", "manim")["status"] == "pass"
    assert renderer_check("from PIL import Image", "manim")["status"] == "fail"
    assert renderer_check("anything", "revideo")["status"] == "fail"
    assert duration_check(10.4, 10.0)["status"] == "pass"
    assert duration_check(11.0, 10.0)["status"] == "fail"


def test_a_shape_through_words_fails():
    found = results([{"at": 1.0, "graphics": 3, "texts": [
        piece("Loss and Guilt", [200, 100, 900, 180])],
        "crossings": [{"text": "Loss and Guilt", "shape": "Arrow"}]}])
    assert found["crossing"] == "fail"


def test_a_section_with_pictures_must_show_one():
    snapshots = [{"at": 1.0, "graphics": 3, "pictures": [],
                  "texts": [piece("Loss and Guilt", [200, 100, 900, 180])]}]
    with_pictures = BRIEF | {"assets": {"pictures": ["slide-picture.png"]}}
    found = {c["key"]: c["status"]
             for c in text_checks({"snapshots": snapshots}, with_pictures)}
    assert found["pictures"] == "fail"
    snapshots[0]["pictures"] = [[100, 100, 500, 400]]
    found = {c["key"]: c["status"]
             for c in text_checks({"snapshots": snapshots}, with_pictures)}
    assert found["pictures"] == "pass"
    assert results(snapshots)["pictures"] == "n/a", "no pictures offered, nothing asked"


def test_words_laid_on_a_picture_fail_as_overlap():
    """A real run: a label sat on the slide's diagram, over the diagram's own
    'dendrites', and every check passed -- the picture's words cannot be seen
    from the layout. Words on a picture are now an overlap."""
    beat = {"at": 1.0, "graphics": 3, "pictures": [[100, 300, 1800, 800]], "texts": [
        piece("Loss and Guilt", [200, 100, 900, 180])]}
    assert results([beat])["overlap"] == "pass"
    assert results([beat | {"on_pictures": ["Loss and Guilt"]}])["overlap"] == "fail"


def test_boxes_laid_over_boxes_fail_and_apart_they_pass():
    """Scene 002 of a real run passed every check with two boxes laid half over each
    other: nothing looked at shapes against shapes."""
    beat = {"at": 1.0, "graphics": 3, "texts": [piece("Loss and Guilt", [200, 300, 900, 380])],
            "extent": [150, 100, 1700, 800]}
    over = results([beat | {"collisions": [{"a": "RoundedRectangle around “Loss”",
                                            "b": "RoundedRectangle around “Guilt”"}]}])
    apart = results([beat | {"collisions": []}])
    assert over["collide"] == "fail" and apart["collide"] == "pass"


def test_a_diagram_in_one_strip_of_the_frame_fails():
    """Scene 002 again: its diagram used 28% of the height, the rest empty."""
    beat = {"at": 1.0, "graphics": 3, "collisions": [],
            "texts": [piece("Loss and Guilt", [200, 240, 900, 320])]}
    assert results([beat | {"extent": [115, 240, 1800, 545]}])["fills"] == "fail"
    assert results([beat | {"extent": [115, 76, 1800, 760]}])["fills"] == "pass"
    # Its fullest moment counts: a scene that builds up is not failed for its start.
    built = [beat | {"at": 1.0, "extent": [800, 240, 1100, 320]},
             beat | {"at": 4.0, "extent": [115, 76, 1800, 760]}]
    assert results(built)["fills"] == "pass"


def test_a_renderer_that_does_not_record_shapes_is_not_judged_on_them():
    found = results([{"at": 1.0, "graphics": 3,
                      "texts": [piece("Loss and Guilt", [200, 100, 900, 180])]}])
    assert found["collide"] == found["fills"] == "n/a"
