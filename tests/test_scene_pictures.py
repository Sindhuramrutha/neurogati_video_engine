"""A scene is offered every deck picture, nearest first, with what each is; the
video's use of the deck is counted; what the deck does not show is found on the
open web (commercial licences only) or drawn as an icon, and credited.

In Demo 001 a vision verdict withheld ten of twenty-two deck pictures, scenes were
offered only their own slide's, and a painting came first in every list: 32 of 43
scenes showed a painting and most of the deck appeared nowhere."""

import json
from types import SimpleNamespace as Thing

import pytest

from pipeline import outside_pictures, scene_pictures, scene_vetting
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
    assert by_file["cover.png"]["shown_in_video"] == "scene 1, scene 4"
    assert by_file["volta.png"]["shown_in_video"].startswith("not yet")
    assert "plain graphic" in by_file["banner.png"]["measured"].lower(), \
        "what was measured is said, not used to refuse it"


@pytest.mark.real_vetting
def test_no_deck_picture_is_withheld_and_each_is_described_once(tmp_path, monkeypatch):
    asked = []
    monkeypatch.setattr(scene_vetting, "_ask", lambda path: asked.append(path) or {
        "what": "a Check for updates badge", "role": "furniture"})

    on_screen, offered = scene_vetting.offered(tmp_path, "DRAW: a frog's leg", ["badge.png"])
    assert offered == ["badge.png"], "furniture is offered, described; the agent decides"
    assert "ILLUSTRATE" not in on_screen, "a deck picture is there: nothing painted by rule"
    scene_vetting.offered(tmp_path, "DRAW: a frog's leg", ["badge.png"])
    assert [str(p) for p in asked] == ["badge.png"], "asked once per picture, then kept"
    assert scene_vetting.notes(tmp_path, ["badge.png"])["badge.png"]["role"] == "furniture"


def test_with_no_deck_picture_at_all_one_is_painted_from_the_brief(tmp_path):
    on_screen, offered = scene_vetting.offered(tmp_path, "DRAW: a frog's leg on a hook", [])
    assert offered == [] and "ILLUSTRATE: a frog's leg on a hook" in on_screen


def test_a_verdict_kept_before_roles_is_read_as_a_note(tmp_path):
    (tmp_path / scene_vetting.VERDICTS).write_text(json.dumps({
        "a.png": {"teaches": True, "what": "Galen"},
        "b.png": {"teaches": False, "what": "a floral brain"}}), encoding="utf-8")
    notes = scene_vetting.notes(tmp_path, ["a.png", "b.png"])
    assert notes["a.png"]["role"] == "explains"
    assert notes["b.png"]["role"] == "sets_scene", "the deck's art, offered as a backdrop"


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


# --- pictures from outside the deck ---------------------------------------------------------


@pytest.mark.parametrize("licence, allowed", [
    ("Public domain", True), ("CC0", True), ("CC BY 4.0", True), ("CC BY-SA 3.0", True),
    ("by-sa-4.0", True), ("pdm-1.0", True),
    ("CC BY-NC 2.0", False), ("CC BY-ND 4.0", False), ("CC BY-NC-SA 3.0", False),
    ("GFDL", False), ("", False), ("All rights reserved", False)])
def test_only_licences_that_allow_commercial_use_are_kept(licence, allowed):
    assert outside_pictures.commercial_licence(licence) is allowed


def test_the_brief_asks_for_a_photo_and_icons_on_their_own_lines():
    photo, icons = outside_pictures.wanted(
        "PICTURE: none\nPHOTO: Ivan Pavlov with a dog in his laboratory\n"
        "ICON: microscope, brain and lightning, bell")
    assert photo == "Ivan Pavlov with a dog in his laboratory"
    assert icons == ["microscope", "brain", "lightning"], "at most three"
    assert outside_pictures.wanted("PHOTO: none\nICON: -") == ("", [])


def state():
    return {"calls": {"agent": 0, "vision": 0}, "events": []}


def test_a_found_photo_is_the_one_the_vision_model_picked_and_is_credited(tmp_path,
                                                                           monkeypatch):
    results = [{"source": "Wikimedia Commons", "title": f"File:Pavlov {n}.jpg",
                "url": f"https://x/{n}.jpg", "page": f"https://x/page/{n}",
                "licence": "CC BY 4.0", "licence_url": "", "author": f"Author {n}"}
               for n in (1, 2)]
    monkeypatch.setattr(outside_pictures, "search_commons", lambda q: results)
    monkeypatch.setattr(outside_pictures, "search_openverse", lambda q: [
        results[0] | {"source": "Openverse (wikimedia)", "url": "https://y/1.jpg",
                      "title": "File:Pavlov 1.jpg"}])
    monkeypatch.setattr(outside_pictures, "_picture_bytes", lambda url: url.encode())
    looked = []
    monkeypatch.setattr(outside_pictures, "_choose",
                        lambda asked, said, candidates: looked.append(candidates) or 2)

    path = outside_pictures.find_photo(tmp_path, "Pavlov's dog", "Pavlov rang", state())

    assert len(looked[0]) == 2, "the same file found twice is looked at once"
    assert path.read_bytes() == b"https://x/2.jpg"
    record = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
    assert record["author"] == "Author 2" and record["licence"] == "CC BY 4.0"
    sources = json.loads((tmp_path / "sources.json").read_text(encoding="utf-8"))
    assert sources[0]["file"] == path.name and sources[0]["author"] == "Author 2"
    kept = outside_pictures.kept(tmp_path, "PHOTO: Pavlov's dog")
    assert kept and kept[0][0] == path


def test_nothing_right_is_found_and_the_photo_is_painted_instead(tmp_path, monkeypatch):
    from pipeline import scene_illustration

    monkeypatch.setattr(outside_pictures, "search_commons", lambda q: [])
    monkeypatch.setattr(outside_pictures, "search_openverse", lambda q: [])
    painted = []
    monkeypatch.setattr(scene_illustration, "paint",
                        lambda folder, on_screen, *a, **k: painted.append(on_screen))
    monkeypatch.setattr("pipeline.scene_program.scene_folder",
                        lambda project, visual, create=False: tmp_path)
    monkeypatch.setattr("pipeline.scene_lab.write_brief", lambda project, visual: {"again": 1})

    brief = {"on_screen": "PHOTO: a frog's leg twitching", "look": {}, "narration": ""}
    again = scene_pictures.prepare(Thing(root=tmp_path), Thing(), brief, state())

    assert painted == ["ILLUSTRATE: a frog's leg twitching"]
    assert again == {"again": 1}, "the brief is written again with what was made"


def test_an_icon_comes_from_the_bundled_set_when_the_web_is_not_there(tmp_path, monkeypatch):
    def offline(name):
        raise OSError("no network")

    monkeypatch.setattr(outside_pictures, "_iconify", offline)
    monkeypatch.setattr(outside_pictures, "rasterise", lambda svg, colour: b"PNG" + colour.encode())

    path = outside_pictures.find_icon(tmp_path, "brain", "#4472c4", state())

    record = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
    assert record["source"] == "Lucide (bundled)" and record["licence"] == "ISC"
    assert path.read_bytes() == b"PNG#4472c4", "drawn in the scene's colour"


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

    assert outside_pictures.credits(Thing(root=tmp_path)) == [entry]
