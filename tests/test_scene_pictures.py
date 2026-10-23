"""A scene is offered every deck picture, nearest first, with what each is; the
video's use of the deck is counted; what the deck does not show is found on the
open web (commercial licences only) or drawn as an icon, and credited.

In Demo 001 a vision verdict withheld ten of twenty-two deck pictures, scenes were
offered only their own slide's, and a painting came first in every list: 32 of 43
scenes showed a painting and most of the deck appeared nowhere."""

import json
from types import SimpleNamespace as Thing

import pytest

from pipeline import scene_pictures, scene_vetting
from pipeline.assets import AssetLibrary, LibraryFigure
from pipeline.planning import Plan, PlanScene, PlanSection, SourceReference
from pipeline.scene_shots import program_for

# --- what a scene is offered --------------------------------------------------------------


def a_deck(tmp_path, monkeypatch):
    """Five slides' pictures, one left out by a person, one an unreadable file."""
    figures = []
    blocks = []
    for slide, name, extra in ((1, "cover", {}), (2, "galen", {}), (2, "heart", {}),
                               (3, "volta", {}), (5, "banner", {"flags": ["plain"]}),
                               (4, "skipped", {"use": "skip"}),
                               (4, "broken", {"flags": ["unreadable"]})):
        path = f"extraction/assets/{name}.png"
        (tmp_path / "extraction/assets").mkdir(parents=True, exist_ok=True)
        (tmp_path / path).write_bytes(b"png")
        figures.append(LibraryFigure(asset_path=path, block_id=f"b-{name}", slide_number=slide,
                                     slide_title=f"Slide {slide}", caption=f"{name} figure",
                                     width=800, height=600, **extra))
        blocks.append(Thing(id=f"b-{name}", slide_number=slide))
    monkeypatch.setattr("pipeline.extraction.ExtractionStore.load",
                        lambda self: Thing(documents=[Thing(blocks=blocks)]))
    section = PlanSection(id="s", sources=[SourceReference(file_name="d.pptx", slide_number=2),
                                           SourceReference(file_name="d.pptx", slide_number=3)],
                          scenes=[PlanScene(id="one", slides=[2]), PlanScene(id="two", slides=[3])])
    plan = Plan(sections=[section])
    return Thing(root=tmp_path), section, plan, AssetLibrary(figures=figures)


def names(tiers):
    return [(where, figure.asset_path.split("/")[-1][:-4]) for where, figure in tiers]


def test_a_scene_is_offered_every_deck_picture_nearest_first(tmp_path, monkeypatch):
    project, section, plan, library = a_deck(tmp_path, monkeypatch)
    visual = Thing(scene_id="one", slide_number=2)

    tiers = scene_pictures.deck_tiers(project, visual, section, plan, library,
                                      "PICTURE: none", "The heart pumps blood")

    assert names(tiers) == [
        ("this scene's own slide", "heart"), ("this scene's own slide", "galen"),
        ("this section", "volta"),
        ("elsewhere in the deck", "cover"), ("elsewhere in the deck", "banner"),
    ], "own slide (the one the narration names first), section, then the rest of the deck"
    assert "skipped" not in str(tiers), "a person left it out: never offered"
    assert "broken" not in str(tiers), "a file that cannot be opened cannot be shown"


def test_the_picture_the_brief_names_comes_first(tmp_path, monkeypatch):
    project, section, plan, library = a_deck(tmp_path, monkeypatch)
    visual = Thing(scene_id="two", slide_number=3)

    tiers = scene_pictures.deck_tiers(project, visual, section, plan, library,
                                      "PICTURE: banner figure\nDRAW: the deck's banner", "")

    assert names(tiers)[0] == ("named in this scene's brief", "banner"), \
        "from another slide, plain -- but the script chose it"
    assert names(tiers)[1] == ("this scene's own slide", "volta")


def test_a_picture_detached_from_the_section_is_not_offered_back(tmp_path, monkeypatch):
    project, section, plan, library = a_deck(tmp_path, monkeypatch)
    section.pictures_chosen = True
    section.picture_paths = ["extraction/assets/galen.png"]
    plan.pictures_from = "transferred"

    tiers = scene_pictures.deck_tiers(project, Thing(scene_id="one", slide_number=2),
                                      section, plan, library, "", "")

    assert "heart" not in [name for _, name in names(tiers)]


def test_the_catalogue_says_what_each_picture_is_and_whether_the_video_shows_it(
        tmp_path, monkeypatch):
    from PIL import Image

    project, section, plan, library = a_deck(tmp_path, monkeypatch)
    for figure in library.figures:
        Image.new("RGB", (40, 30), "white").save(tmp_path / figure.asset_path)
    slide = tmp_path / "slide.png"
    Image.new("RGB", (192, 108), "white").save(slide)
    tiers = scene_pictures.deck_tiers(project, Thing(scene_id="one", slide_number=2),
                                      section, plan, library, "", "")
    cover = str(tmp_path / "extraction/assets/cover.png")
    paths, catalogue = scene_pictures.catalogue(
        project, tiers, [], {cover: {"what": "a book cover", "role": "furniture"}},
        {cover: ["scene 1", "scene 4"]}, slide)

    assert [entry["index"] for entry in catalogue] == list(range(len(paths)))
    by_file = {entry["file"]: entry for entry in catalogue}
    assert by_file["slide.png"]["role"] == "slide", "the slide itself is offered, as itself"
    assert paths.index(str(slide)) == 2, "after the scene's own slide's pictures"
    assert by_file["cover.png"]["role"] == "furniture"
    assert by_file["cover.png"]["shown_in"] == ["scene 1", "scene 4"]
    assert by_file["volta.png"]["shown_in"] == []
    assert by_file["heart.png"]["near"] and not by_file["volta.png"]["near"], \
        "its own slide's are its own; its section's are offered, not expected"
    assert "plain graphic" in by_file["banner.png"]["measured"].lower(), \
        "what was measured is said, not used to refuse it"


@pytest.mark.real_vetting
def test_no_deck_picture_is_withheld_and_each_is_described_once(tmp_path, monkeypatch):
    asked = []
    monkeypatch.setattr(scene_vetting, "_ask", lambda path: asked.append(path) or {
        "what": "a Check for updates badge", "role": "furniture"})

    on_screen = scene_vetting.with_painting_asked("DRAW: a frog's leg", ["badge.png"])
    assert "ILLUSTRATE" not in on_screen, "a deck picture is there: nothing painted by rule"
    scene_vetting.notes(tmp_path, ["badge.png"])
    assert scene_vetting.notes(tmp_path, ["badge.png"])["badge.png"]["role"] == "furniture", \
        "furniture is described, not withheld; the agent decides"
    assert [str(p) for p in asked] == ["badge.png"], "asked once per picture, then kept"


def test_with_no_deck_picture_at_all_one_is_painted_from_the_brief(tmp_path):
    on_screen = scene_vetting.with_painting_asked("DRAW: a frog's leg on a hook", [])
    assert "ILLUSTRATE: a frog's leg on a hook" in on_screen


@pytest.mark.real_vetting
def test_a_verdict_kept_before_roles_is_asked_again_not_guessed(tmp_path, monkeypatch):
    """Guessed from "does it teach?", a Check for updates badge was offered as the
    deck's art, and a script built a scene on it."""
    (tmp_path / scene_vetting.VERDICTS).write_text(json.dumps({
        "badge.png": {"teaches": False, "what": "Check for updates button"},
        "galen.png": {"what": "Galen", "role": "explains"}}), encoding="utf-8")
    asked = []
    monkeypatch.setattr(scene_vetting, "_ask", lambda path: asked.append(str(path)) or {
        "what": "a Check for updates badge", "role": "furniture"})

    notes = scene_vetting.notes(tmp_path, ["badge.png", "galen.png"])

    assert asked == ["badge.png"], "only the one kept without a role"
    assert notes["badge.png"]["role"] == "furniture"
    assert notes["galen.png"]["role"] == "explains"


def test_a_scene_is_not_made_to_show_a_badge_or_the_slide():
    from pipeline.scene_review import own_pictures

    brief = {"picture_catalogue": [
        {"file": "badge.png", "near": True, "role": "furniture", "what": "badge"},
        {"file": "slide.png", "near": True, "role": "slide", "what": "slide"},
        {"file": "galen.png", "near": False, "role": "explains", "what": "Galen"}]}
    assert own_pictures(brief) == [], "nothing of its own that it should show"
    brief["picture_catalogue"][0]["role"] = "explains"
    assert own_pictures(brief) == ["badge.png (badge)"]
    brief["picture_catalogue"][0]["main_of"] = "scene 3"
    assert own_pictures(brief) == [], "another scene's subject is not expected here"


# --- which deck pictures the video shows ----------------------------------------------------


def test_a_scene_shows_the_pictures_its_shots_and_its_program_use(tmp_path):
    shots = tmp_path / "shots"
    shots.mkdir()
    (shots / "spec.json").write_text(json.dumps({"shots": [
        {"template": "hero", "picture": 2}, {"template": "key_idea", "picture": None},
        {"template": "steps", "steps": [{"label": "a", "picture": 0}]}]}), encoding="utf-8")
    assert scene_pictures._shown_indexes(shots) == {0, 2}

    hand = tmp_path / "hand"
    hand.mkdir()
    (hand / "spec.json").write_text(json.dumps({"renderer": "manim"}), encoding="utf-8")
    (hand / "scene.py").write_text("P = self.brief.assets.pictures\nself.hero(P[1], [])\n"
                                   "self.picture(self.brief.assets.pictures[3])",
                                   encoding="utf-8")
    assert scene_pictures._shown_indexes(hand) == {1, 3}


def test_a_moved_project_still_knows_its_pictures(tmp_path):
    project = Thing(root=tmp_path / "now")
    moved = r"D:\desktop\old\projects\demo\extraction\assets\a.png"
    assert scene_pictures._same_file(project, moved) == str(
        tmp_path / "now" / "extraction" / "assets" / "a.png")


# --- the opener: the deck's art behind a topic's opening ------------------------------------


def test_an_opener_shot_is_written_as_the_kit_s_template():
    program = program_for({"shots": [
        {"template": "opener", "picture": 1, "title": "Brain ideas through the centuries",
         "when": "for most of history",
         "lines": [{"text": "Heart or brain?", "when": "the heart"}]}]}, pictures=2)
    assert ("self.opener(P[1], 'Brain ideas through the centuries', "
            "[('Heart or brain?', 'the heart')], cue=None)") in program


def test_an_opener_needs_a_picture():
    with pytest.raises(ValueError, match="needs a picture"):
        program_for({"shots": [{"template": "opener", "title": "x", "picture": None}]}, 1)


# --- pictures made for a scene: painted by the image model, or a bundled icon ---------------


def state():
    return {"calls": {"agent": 0, "vision": 0}, "events": []}


def test_the_brief_asks_for_a_painting_and_icons_on_their_own_lines():
    from pipeline import icon_pictures, scene_illustration

    brief = "PICTURE: none\nILLUSTRATE: two frog hearts in beakers\nICON: microscope, brain"
    assert scene_illustration.wanted(brief) == "two frog hearts in beakers"
    assert icon_pictures.wanted(brief) == ["microscope", "brain"]
    assert icon_pictures.wanted("ICON: a, b, c, d") == ["a", "b", "c"], "at most three"


def test_a_photo_asked_for_is_painted_never_searched_for():
    """Every picture comes from the image model; an old brief's PHOTO line is read as
    a painting, and a real person is painted as an illustration, not a photograph."""
    from pipeline import scene_illustration

    assert scene_illustration.wanted("PHOTO: Ivan Pavlov with a dog") == \
        "Ivan Pavlov with a dog"
    asked = scene_illustration.prompt("Ivan Pavlov with a dog", {"background": "#ffffff"})
    assert "Never photorealistic" in asked and "illustrated portrait" in asked


def checked(matches=True, framed=True, clean=True, wrong=""):
    from pipeline.scene_illustration import Checked

    return Checked(matches=matches, framed=framed, clean=clean, wrong=wrong)


def test_a_painting_is_used_only_once_it_is_right_and_well_framed(tmp_path, monkeypatch):
    from pipeline import scene_illustration

    verdicts = [checked(framed=False, wrong="the heart is cut off at the top"), checked()]
    monkeypatch.setattr(scene_illustration, "check", lambda path, asked, said: verdicts.pop(0))
    monkeypatch.setattr(scene_illustration, "blend", lambda path, background: None)
    asked = []

    path = scene_illustration._paint_checked(
        tmp_path / "illustration-x.png", "a frog heart", {}, "", state(),
        lambda request: asked.append(request) or b"png")

    assert path is not None and path.exists()
    assert "cut off at the top" in asked[1], "painted again with what was wrong"


def test_a_painting_never_right_is_not_used(tmp_path, monkeypatch):
    """Kept after one retry, a wrong painting (human hearts for frog hearts) went
    into the scene. Now it is left out, and the scene is made without it."""
    from pipeline import scene_illustration

    monkeypatch.setattr(scene_illustration, "check",
                        lambda path, asked, said: checked(matches=False, wrong="human hearts"))
    record = state()

    path = scene_illustration._paint_checked(
        tmp_path / "illustration-x.png", "two frog hearts", {}, "", record, lambda r: b"png")

    assert path is None and not (tmp_path / "illustration-x.png").exists()
    assert record["calls"]["image"] == scene_illustration.PAINTED_AT_MOST
    assert "made without it" in record["events"][-1]["text"]


def test_a_painting_left_unchecked_by_a_stopped_run_is_painted_again(tmp_path):
    """A run stopped mid-painting left a picture with no record of its check, and
    the next run used it as painted."""
    from pipeline import scene_illustration

    brief, look = "ILLUSTRATE: two frog hearts", {"background": "#ffffff"}
    path = scene_illustration._path(tmp_path, "two frog hearts", look)
    path.write_bytes(b"png")
    assert scene_illustration.kept(tmp_path, brief, look) is None
    path.with_suffix(".json").write_text('{"checked": true}', encoding="utf-8")
    assert scene_illustration.kept(tmp_path, brief, look) == path


def test_an_icon_comes_from_the_bundled_set(tmp_path, monkeypatch):
    from pipeline import icon_pictures

    monkeypatch.setattr(icon_pictures, "rasterise",
                        lambda svgs, colour: [b"PNG" + colour.encode() for _ in svgs])

    path = icon_pictures.find_icon(tmp_path, "brain", "#4472c4", state())

    record = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
    assert record["source"] == "Lucide (bundled)" and record["licence"] == "ISC"
    assert path.read_bytes() == b"PNG#4472c4", "drawn in the scene's colour"


# --- a pointer lands on the part it names -------------------------------------------------


PARTS = [{"name": "cerebellum", "box": [0.5, 0.6, 0.7, 0.8], "sure": True},
         {"name": "pineal gland", "box": [0.4, 0.4, 0.5, 0.5], "sure": False},
         {"name": "spinal cord", "box": [0.55, 0.8, 0.6, 1.0], "sure": True}]


def test_a_callout_points_at_the_middle_of_the_part_it_names():
    from pipeline.picture_parts import anchor

    assert anchor(PARTS, "Cerebellum") == (0.6, 0.7)
    assert anchor(PARTS, "the cerebellum") == (0.6, 0.7), "a near enough name"
    assert anchor(PARTS, "pineal gland") is None, "not sure where it is: no pointer"
    assert anchor(PARTS, "toga") is None, "not in the picture: no pointer"


def test_a_hero_s_callouts_are_drawn_to_located_parts_and_unknown_ones_left_out():
    from pipeline.scene_shots import Pictures

    program = program_for({"shots": [{"template": "hero", "picture": 0, "title": "The brain",
                                      "callouts": [
        {"label": "Cerebellum", "part": "cerebellum", "when": "balance"},
        {"label": "Brain", "part": "toga", "when": "statue"}],
        "moves": [{"through": ["cerebellum", "spinal cord"], "when": "down"}]}]},
        Pictures(1, {0: PARTS}))

    assert "('Cerebellum', (0.60, 0.70), 'balance')" in program
    assert "Brain'" not in program, "a pointer at the statue's clothing is not drawn"
    assert "moves=[([(0.60, 0.70), (0.57, 0.90)], 'down')]" in program


def test_another_scene_s_subject_is_never_this_scene_s_main_picture():
    """The robot hand holding a brain was the subject of the opening and again of the
    next section's scene."""
    from pipeline.scene_shots import Pictures

    taken = Pictures(2, {}, frozenset({0}))
    with pytest.raises(ValueError, match="another scene's subject"):
        program_for({"shots": [{"template": "key_idea", "statement": "A mind", "picture": 0,
                                "when": "x"}]}, taken)
    for template in ("person", "opener"):
        with pytest.raises(ValueError, match="another scene's subject"):
            program_for({"shots": [{"template": template, "picture": 0, "name": "N",
                                    "line": "L", "title": "T"}]}, taken)
    small = program_for({"shots": [{"template": "steps", "title": "Steps", "steps": [
        {"label": "One", "picture": 0, "when": "a"},
        {"label": "Two", "picture": 1, "when": "b"}]}]}, taken)
    assert "P[0]" in small, "small, in steps, it may still be shown"


def test_a_picture_belongs_to_the_first_scene_that_names_or_shows_it_large():
    from pipeline.scene_pictures import _owner

    assert _owner(["scene 3, planned", "scene 7"], False, 5) == 3
    assert _owner(["scene 7"], True, 5) == 5, "this scene names it, and comes first"
    assert _owner(["scene 2, small"], False, 5) == 0, "shown small claims nothing"


def test_export_credits_every_outside_picture_once(tmp_path, monkeypatch):
    folders = [tmp_path / "a", tmp_path / "b"]
    entry = {"file": "found-1.png", "title": "Pavlov", "source": "Wikimedia Commons",
             "licence": "CC BY 4.0", "author": "Wellcome", "page": "https://x/p"}
    for folder in folders:
        folder.mkdir()
        (folder / "sources.json").write_text(json.dumps([entry]), encoding="utf-8")
    monkeypatch.setattr("pipeline.generation.VisualPlanStore.load",
                        lambda self: Thing(visuals=folders))
    monkeypatch.setattr("pipeline.scene_program.scene_folder", lambda project, visual: visual)

    from pipeline.exporting import outside_credits

    assert outside_credits(Thing(root=tmp_path)) == [entry]


def test_a_picture_another_scene_plans_to_show_is_not_offered_as_unused(tmp_path, monkeypatch):
    """Scenes are made four at a time. Three scenes of one section each saw the
    robot-hand picture as "not yet shown" and all made it their subject."""
    project, section, plan, library = a_deck(tmp_path, monkeypatch)
    visuals = [Thing(id="v1", brief="PICTURE: galen figure\nDRAW: Galen"),
               Thing(id="v2", brief="PICTURE: none"),
               Thing(id="v3", brief="PICTURE: volta figure")]
    monkeypatch.setattr("pipeline.generation.VisualPlanStore.load",
                        lambda self: Thing(visuals=visuals))
    monkeypatch.setattr("pipeline.scene_program.scene_folder",
                        lambda project, visual, create=False: None)
    monkeypatch.setattr("pipeline.plan_pictures.assets_for_later_stages",
                        lambda project: Thing(library=library))

    shown = scene_pictures.shown_pictures(project, skip_visual_id="v3")

    assert shown == {str(tmp_path / "extraction/assets/galen.png"): ["scene 1, planned"]}
    assert scene_pictures.shown_pictures(project, planned=False) == {}, \
        "the video's count is of what was made, not what was planned"
