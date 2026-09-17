"""The two stages added either end of the middle: Assets & Design, and Export.

Assets exists because nothing decided *which* extracted pictures were worth
showing, and nothing carried a deck's own look forward. Export exists because a
finished render is an .mp4 in a folder, and because the last place a wrong video
can be stopped had no checks on it at all.
"""

import io

import pytest
from PIL import Image

from pipeline import operations
from pipeline.assets import AssetLibraryStore, FigureUse
from pipeline.exporting import ExportStore, chapters_text
from pipeline.extraction import (
    BlockKind,
    ContentBlock,
    DocumentDesign,
    ExtractedDocument,
    Extraction,
    ExtractionStore,
    SlideBackground,
    SlideLayout,
)
from pipeline.operations import OperationFailed
from pipeline.planning import Plan, PlanSection, PlanStore
from pipeline.review import Review, ReviewStore, VideoVersion
from pipeline.scripting import Script, ScriptStore, SectionScript


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def picture_bytes(colour="blue", size=(200, 150)):
    image = Image.new("RGB", size, colour)
    image.putpixel((0, 0), (0, 0, 0))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def project_with_pictures(name, pictures, design=None):
    """`pictures` is a list of (caption, size, origin)."""
    slug = operations.create_project(name)["slug"]
    project = operations.require_project(slug)
    (project.root / "extraction" / "assets").mkdir(parents=True, exist_ok=True)

    blocks = [ContentBlock(kind=BlockKind.HEADING, text="Chapter", heading_path=["Chapter"])]
    for index, (caption, size, origin) in enumerate(pictures):
        stored = f"extraction/assets/pic{index}.png"
        (project.root / stored).write_bytes(picture_bytes(size=size))
        blocks.append(ContentBlock(
            kind=BlockKind.FIGURE, text=caption, heading_path=["Chapter"],
            asset_path=stored, asset_origin=origin,
        ))

    document = ExtractedDocument(file_name="chapter.docx", blocks=blocks)
    if design is not None:
        document.design = design
        document.slides = [SlideLayout(
            number=1, background=SlideBackground(colour="#FFFFFF", inherited_from="theme"))]
    ExtractionStore(project.root).save(Extraction(
        documents=[document], extracted_at="2026-09-17T00:00:00+00:00"))
    return slug, project


# --- the library ---------------------------------------------------------------------


def test_gathering_finds_every_picture_and_measures_it(project_root):
    slug, _ = project_with_pictures("Gather", [
        ("Figure 1 the chain", (400, 300), "source"),
        ("bullet", (10, 10), "source"),
    ])

    library = operations.refresh_asset_library(slug)

    captions = [figure["caption"] for figure in library["figures"]]
    assert captions == ["Figure 1 the chain", "bullet"]
    assert library["figures"][0]["width"] == 400
    assert library["figures"][1]["is_decoration"] is True
    assert library["audit"]["usable_count"] == 1, "decoration is not proposed for use"


def test_a_decision_survives_re_extraction(project_root):
    """Block ids are regenerated on every run, so a library keyed on them would
    throw away every choice each time extraction ran."""
    slug, project = project_with_pictures("Survives", [("Figure 1", (400, 300), "source")])
    operations.refresh_asset_library(slug)
    figure_id = operations.read_asset_library(slug)["figures"][0]["id"]
    operations.decide_figure(slug, figure_id, FigureUse.SKIP, note="A logo, nothing more.")

    # A fresh extraction: same picture, brand new block id.
    extraction = ExtractionStore(project.root).load()
    extraction.documents[0].blocks[1] = ContentBlock(
        kind=BlockKind.FIGURE, text="Figure 1", heading_path=["Chapter"],
        asset_path="extraction/assets/pic0.png",
    )
    ExtractionStore(project.root).save(extraction)

    library = operations.refresh_asset_library(slug)

    assert library["figures"][0]["use"] == FigureUse.SKIP
    assert library["figures"][0]["note"] == "A logo, nothing more."


def test_a_picture_that_left_the_extraction_keeps_its_decision(project_root):
    slug, project = project_with_pictures("Gone", [("Figure 1", (400, 300), "source")])
    operations.refresh_asset_library(slug)
    figure_id = operations.read_asset_library(slug)["figures"][0]["id"]
    operations.decide_figure(slug, figure_id, FigureUse.USE)

    extraction = ExtractionStore(project.root).load()
    extraction.documents[0].blocks = extraction.documents[0].blocks[:1]
    ExtractionStore(project.root).save(extraction)

    library = operations.refresh_asset_library(slug)

    assert library["figures"][0]["in_extraction"] is False
    assert library["figures"][0]["use"] == FigureUse.USE
    assert library["audit"]["figure_count"] == 0
    assert any("no longer in the extraction" in w for w in library["warnings"])


def test_a_drawn_picture_is_marked_in_the_library(project_root):
    slug, _ = project_with_pictures("Drawn", [("Figure 1", (400, 300), "generated")])

    library = operations.refresh_asset_library(slug)

    assert library["figures"][0]["origin"] == "generated"
    assert library["audit"]["generated_count"] == 1


def test_an_unknown_decision_is_refused(project_root):
    slug, _ = project_with_pictures("Bad Decision", [("Figure 1", (400, 300), "source")])
    operations.refresh_asset_library(slug)
    figure_id = operations.read_asset_library(slug)["figures"][0]["id"]

    with pytest.raises(OperationFailed, match="not a decision"):
        operations.decide_figure(slug, figure_id, "maybe")


def test_gathering_before_extraction_is_refused(project_root):
    slug = operations.create_project("Nothing Yet")["slug"]

    with pytest.raises(OperationFailed, match="nothing extracted"):
        operations.refresh_asset_library(slug)


# --- the look ------------------------------------------------------------------------


def test_the_look_is_read_from_the_deck_but_never_applied_on_its_own(project_root):
    """A video that silently adopted a client's brand colours would be worse than
    one that asked."""
    slug, _ = project_with_pictures("Look", [("Figure 1", (400, 300), "source")], design=
        DocumentDesign(aspect_ratio="16:9", theme_name="Office Theme",
                       colours={"lt1": "#FFFFFF", "accent1": "#4472C4"},
                       major_font="Calibri Light", minor_font="Calibri"))

    library = operations.refresh_asset_library(slug)

    assert library["look"]["is_available"] is True
    assert library["look"]["use_source_styling"] is False
    assert library["look"]["heading_font"] == "Calibri Light"
    assert library["look"]["background_colour"] == "#FFFFFF"


def test_choosing_the_look_survives_gathering_again(project_root):
    slug, _ = project_with_pictures("Look Kept", [("Figure 1", (400, 300), "source")], design=
        DocumentDesign(aspect_ratio="16:9", colours={"lt1": "#FFFFFF"}, major_font="Calibri"))
    operations.refresh_asset_library(slug)
    operations.set_project_look(slug, True)

    library = operations.refresh_asset_library(slug)

    assert library["look"]["use_source_styling"] is True


def test_following_a_look_that_was_never_extracted_says_so(project_root):
    slug, _ = project_with_pictures("No Styling", [("Figure 1", (400, 300), "source")])
    operations.refresh_asset_library(slug)

    library = operations.set_project_look(slug, True)

    assert any("no styling was extracted" in w.lower() for w in library["warnings"])


# --- export --------------------------------------------------------------------------


def exportable_project(name, *, rendered=True, narration=True):
    slug = operations.create_project(name)["slug"]
    project = operations.require_project(slug)
    PlanStore(project.root).save(Plan(
        selected_audience="Students new to the topic",
        sections=[
            PlanSection(id="s1", title="Signals", estimated_seconds=60),
            PlanSection(id="s2", title="Electrodes", estimated_seconds=60),
        ],
    ))
    if narration:
        ScriptStore(project.root).save(Script(section_scripts=[
            SectionScript(section_id="s1", body="Signals are tiny."),
            SectionScript(section_id="s2", body="Electrodes detect them."),
        ]))
    if rendered:
        video = project.root / "reviewing" / "output" / "cut.mp4"
        video.parent.mkdir(parents=True, exist_ok=True)
        video.write_bytes(b"not really a video")
        (video.parent / "cut.vtt").write_text("WEBVTT\n", encoding="utf-8")
        version = VideoVersion(label="Render 1", duration_ms=120_000, file_path=str(video))
        ReviewStore(project.root).save(Review(
            versions=[version], active_version_id=version.id))
    return slug, project


def test_an_export_writes_the_transcript_chapters_and_description(project_root):
    slug, project = exportable_project("Handover")

    manifest = operations.build_export(slug)

    names = [file["name"] for file in manifest["files"]]
    assert names[:3] == ["transcript.md", "chapters.txt", "description.md"]
    transcript = (project.root / "export" / "transcript.md").read_text(encoding="utf-8")
    assert "Signals are tiny." in transcript and "Electrodes detect them." in transcript
    description = (project.root / "export" / "description.md").read_text(encoding="utf-8")
    assert "Students new to the topic" in description
    assert manifest["is_ready"] is True


def test_the_chapter_marks_are_what_a_video_host_reads():
    text = chapters_text([
        {"title": "Signals", "start_ms": 0},
        {"title": "Electrodes", "start_ms": 62_000},
        {"title": "Amplifiers", "start_ms": 3_723_000},
    ])

    assert text.splitlines() == ["0:00 Signals", "1:02 Electrodes", "1:02:03 Amplifiers"]


def test_the_video_and_its_subtitles_are_listed(project_root):
    slug, _ = exportable_project("With Video")

    manifest = operations.build_export(slug)

    kinds = {file["kind"] for file in manifest["files"]}
    assert {"video", "subtitles"} <= kinds


def test_a_section_with_no_narration_blocks_the_hand_over(project_root):
    slug, project = exportable_project("Half Written")
    ScriptStore(project.root).save(Script(section_scripts=[
        SectionScript(section_id="s1", body="Only the first section."),
    ]))

    manifest = operations.build_export(slug)

    assert manifest["is_ready"] is False
    assert any("no narration" in blocker for blocker in manifest["blockers"])
    assert "Electrodes" in " ".join(manifest["blockers"])


def test_nothing_rendered_blocks_the_hand_over(project_root):
    slug, _ = exportable_project("Unrendered", rendered=False)

    manifest = operations.build_export(slug)

    assert any("rendered" in blocker for blocker in manifest["blockers"])


def test_a_cut_built_from_an_abandoned_script_blocks_the_hand_over(project_root):
    """The failure that made a project look finished while its video was wrong."""
    from pipeline.composition import Clip, ClipKind, CompositionStore, TrackKind

    slug, project = exportable_project("Wrong Cut")
    store = CompositionStore(project.root)
    composition = store.load()
    video_track = next(t for t in composition.tracks if t.kind == TrackKind.VIDEO)
    video_track.clips = [Clip(kind=ClipKind.SCENE, text="A section nobody planned")]
    store.save(composition)

    manifest = operations.build_export(slug)

    assert manifest["is_ready"] is False
    assert any("different script" in blocker for blocker in manifest["blockers"])


def test_an_open_comment_is_a_warning_not_a_blocker(project_root):
    """Whether one open comment stops a hand-over is a judgement the person makes."""
    slug, _ = exportable_project("Open Comment")
    operations.add_review_comment(slug, "Pacing feels quick.", author="Reviewer")

    manifest = operations.build_export(slug)

    assert manifest["is_ready"] is True
    assert any("still open" in warning for warning in manifest["warnings"])


def test_reading_the_export_reports_todays_problems_not_the_ones_it_was_built_with(
    project_root
):
    slug, project = exportable_project("Changed Since")
    operations.build_export(slug)
    assert operations.read_export(slug)["is_ready_now"] is True

    plan = PlanStore(project.root).load()
    plan.sections.append(PlanSection(id="s3", title="Amplifiers", estimated_seconds=60))
    PlanStore(project.root).save(plan)

    later = operations.read_export(slug)

    assert later["is_ready"] is True, "the manifest still says what it said when built"
    assert later["is_ready_now"] is False
    assert any("no narration" in blocker for blocker in later["blockers_now"])


def test_the_export_is_saved_and_can_be_read_back(project_root):
    slug, project = exportable_project("Saved")
    operations.build_export(slug)

    stored = ExportStore(project.root).load()

    assert stored.title == "Saved"
    assert stored.files and stored.built_at


def test_the_library_and_the_export_are_separate_artifacts(project_root):
    """Each stage owns one file, so deleting one cannot take the other with it."""
    slug, project = exportable_project("Two Files")
    project_with = AssetLibraryStore(project.root)

    assert project_with.document_path.name == "library.json"
    assert ExportStore(project.root).document_path.name == "manifest.json"
