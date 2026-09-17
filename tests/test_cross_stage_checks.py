"""Defects found by checking an agent review of a real project against its files.

The review listed eighteen problems. Several were misreadings of the data, but
four pointed at real faults in the pipeline, and checking the rendered frames
turned up a fifth that no agent had noticed. Each test here is one of those.
"""

import pytest

from pipeline import operations
from pipeline.rendering import RenderedSection, _slides_for_narration, section_segments
from pipeline.review import Review, VideoVersion
from pipeline.scripting import Script, SectionScript


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def planned_project(name, sections):
    """A project whose plan has these (title, estimated_seconds) sections."""
    slug = operations.create_project(name)["slug"]
    for title, seconds in sections:
        operations.add_plan_section(slug, title=title, estimated_seconds=seconds)
    ids = [section["id"] for section in operations.read_artifact(slug, "plan")["sections"]]
    return slug, ids


# --- full stops on screen --------------------------------------------------------


def test_every_sentence_on_a_slide_keeps_its_full_stop():
    """The rendered video read "only a few microvolts Filters remove unwanted
    noise An analog-to-digital converter..." -- the script had the periods."""
    narration = (
        "The signal is amplified because it is only a few microvolts. "
        "Filters remove unwanted noise. "
        "An analog-to-digital converter turns it into numbers."
    )
    slides = _slides_for_narration(narration)

    assert " ".join(slides) == narration


def test_a_question_is_not_given_a_second_full_stop():
    slides = _slides_for_narration("Why does this matter? Because the signal is tiny.")

    assert "?." not in " ".join(slides)
    assert slides[0].startswith("Why does this matter? Because")


def test_a_closing_quote_stays_with_its_sentence():
    slides = _slides_for_narration('The label reads "fragile." Handle it with care.')

    assert slides == ['The label reads "fragile." Handle it with care.']


def test_a_decimal_is_not_a_sentence_boundary():
    slides = _slides_for_narration("The amplitude is 3.5 microvolts at most.")

    assert slides == ["The amplitude is 3.5 microvolts at most."]


def test_long_narration_still_splits_across_slides_without_losing_words():
    narration = " ".join(f"Sentence number {n} carries a few more words." for n in range(30))
    slides = _slides_for_narration(narration)

    assert len(slides) > 1
    assert " ".join(slides) == narration


def test_the_timeline_text_carries_the_full_stops_too():
    """The Studio timeline and the subtitles are cut from the same segments."""
    section = RenderedSection(
        "s1", "Title", "First sentence here. Second sentence here.",
        audio_duration_ms=6_000, start_ms=0,
    )
    slide_text = " ".join(s.text for s in section_segments(section) if s.kind == "slide")

    assert slide_text == "First sentence here. Second sentence here."


# --- the script reads in the order the video plays ---------------------------------


def test_a_script_is_presented_in_plan_order_however_it_was_stored(project_root):
    """Section 2 written last left script.json as 1, 3, 4, 5, 2. The render was
    unaffected, but a review agent reading the file reported the video as out of
    order -- and every agent reads the file."""
    slug, ids = planned_project("Order", [("One", 30), ("Two", 30), ("Three", 30)])
    project = operations.require_project(slug)

    from pipeline.scripting import ScriptStore

    ScriptStore(project.root).save(Script(section_scripts=[
        SectionScript(section_id=ids[0], body="one."),
        SectionScript(section_id=ids[2], body="three."),
        SectionScript(section_id=ids[1], body="two."),
    ]))

    presented = operations.read_artifact(slug, "script")

    assert [s["section_id"] for s in presented["section_scripts"]] == ids


def test_writing_a_section_later_stores_it_in_plan_order(project_root):
    slug, ids = planned_project("Late Section", [("One", 30), ("Two", 30), ("Three", 30)])
    for section_id in (ids[0], ids[2], ids[1]):
        operations.write_section_script(slug, section_id, "Some narration.")

    project = operations.require_project(slug)
    from pipeline.scripting import ScriptStore

    stored = ScriptStore(project.root).load()
    assert [s.section_id for s in stored.section_scripts] == ids


def test_orphaned_narration_is_kept_after_the_planned_sections():
    script = Script(section_scripts=[
        SectionScript(section_id="gone", body="kept on purpose."),
        SectionScript(section_id="b", body="b."),
        SectionScript(section_id="a", body="a."),
    ])

    ordered = script.in_plan_order(["a", "b"])

    assert [s.section_id for s in ordered.section_scripts] == ["a", "b", "gone"]


# --- a section far over its planned length is reported -----------------------------


def test_narration_well_over_the_plan_is_flagged_in_scripting(project_root):
    """331 words in a 90-second section: about 132 seconds, and nothing said so."""
    slug, ids = planned_project("Budget", [("Short", 90), ("Fine", 90)])
    operations.write_section_script(slug, ids[0], "word " * 331)
    operations.write_section_script(slug, ids[1], "word " * 220)

    script = operations.read_artifact(slug, "script")

    assert [s["section_id"] for s in script["audit"]["over_budget"]] == [ids[0]]
    assert any("132s against 90s planned" in warning for warning in script["warnings"])


def test_narration_slightly_over_the_estimate_is_not_noise(project_root):
    slug, ids = planned_project("Close Enough", [("Section", 90)])
    operations.write_section_script(slug, ids[0], "word " * 250)   # ~100s, within 25%

    assert operations.read_artifact(slug, "script")["audit"]["over_budget"] == []


def test_reviewing_repeats_the_length_warning(project_root):
    """Reviewing is the last gate, and it read "no warnings" over this."""
    slug, ids = planned_project("Review Budget", [("Long", 60)])
    operations.write_section_script(slug, ids[0], "word " * 300)

    review = operations.read_artifact(slug, "review")

    assert any("planned" in warning and "% over" in warning for warning in review["warnings"])


# --- versions that are really one file ---------------------------------------------


def test_versions_sharing_one_file_are_reported():
    """Renders from before per-render file names all wrote the same path: three
    versions listed, one video, and picking an older one played the newest."""
    review = Review(versions=[
        VideoVersion(label="a", file_path="out/video.mp4"),
        VideoVersion(label="b", file_path="out/video.mp4"),
        VideoVersion(label="c", file_path="out/video.mp4"),
        VideoVersion(label="d", file_path="out/video-20260915.mp4"),
        VideoVersion(label="not rendered"),
    ])

    presented = review.to_dict()

    assert len(presented["audit"]["shared_file_version_ids"]) == 1
    assert len(presented["audit"]["shared_file_version_ids"][0]) == 3
    assert any("3 versions share one video file" in w for w in presented["warnings"])


def test_distinct_renders_raise_no_shared_file_warning():
    review = Review(versions=[
        VideoVersion(label="a", file_path="out/one.mp4"),
        VideoVersion(label="b", file_path="out/two.mp4"),
    ])

    assert review.to_dict()["audit"]["shared_file_version_ids"] == []


# --- a cut that no longer matches its script -------------------------------------------


def _timeline_with_titles(slug, titles):
    from pipeline.composition import Clip, ClipKind, CompositionStore, TrackKind

    project = operations.require_project(slug)
    store = CompositionStore(project.root)
    composition = store.load()
    video = next(track for track in composition.tracks if track.kind == TrackKind.VIDEO)
    video.clips = [
        Clip(kind=ClipKind.SCENE, label=title[:80], text=title,
             start_ms=index * 10_000, duration_ms=9_000)
        for index, title in enumerate(titles)
    ]
    return store.save(composition)


def test_a_timeline_from_an_abandoned_script_is_reported(project_root):
    """The defect this exists for: a plan was re-drafted from a different source,
    the timeline and chapters stayed as an earlier render left them, and every
    later render refused to rebuild them because they counted as hand-edited.
    Studio and Reviewing went on describing a video nobody was making."""
    slug, _ = planned_project("Wrong Cut", [
        ("Perceptrons: Architecture and Learning", 90),
        ("Backpropagation: The Breakthrough", 90),
    ])
    _timeline_with_titles(slug, [
        "The Neural Signal Acquisition Chain: An Overview",
        "Electrodes and Sensors: The Interface with the Body",
    ])

    composition = operations.read_artifact(slug, "composition")

    assert composition["freshness"]["is_stale"] is True
    assert len(composition["freshness"]["unknown_sections"]) == 2
    assert any("built from a different script" in warning
               for warning in composition["warnings"])


def test_a_timeline_that_matches_the_plan_is_not_flagged(project_root):
    slug, _ = planned_project("Right Cut", [
        ("Perceptrons: Architecture and Learning", 90),
    ])
    _timeline_with_titles(slug, ["Perceptrons: Architecture and Learning"])

    composition = operations.read_artifact(slug, "composition")

    assert composition["freshness"]["is_stale"] is False
    assert composition["warnings"] == []


def test_reviewing_repeats_that_the_cut_is_wrong(project_root):
    """Reviewing is the last gate before someone calls a video finished."""
    slug, _ = planned_project("Wrong Cut Reviewed", [
        ("Perceptrons: Architecture and Learning", 90),
    ])
    _timeline_with_titles(slug, ["Electrodes and Sensors: The Interface with the Body"])
    from pipeline.review import Chapter, ReviewStore

    project = operations.require_project(slug)
    store = ReviewStore(project.root)
    review = store.load()
    review.chapters = [Chapter(title="Electrodes and Sensors", start_ms=0)]
    store.save(review)

    warnings = operations.read_artifact(slug, "review")["warnings"]

    assert any("not in the plan any more" in warning for warning in warnings)
    assert any("different script" in warning for warning in warnings)


def test_emptying_the_timeline_lets_a_render_rebuild_it(project_root):
    """The only way out used to be deleting clips one at a time."""
    slug, _ = planned_project("Emptied", [("Perceptrons", 90)])
    _timeline_with_titles(slug, ["Something else entirely"])

    cleared = operations.clear_timeline(slug)

    assert sum(len(track["clips"]) for track in cleared["tracks"]) == 0
    assert cleared["freshness"]["is_stale"] is False
    assert cleared["generated_from_render_at"] == ""
