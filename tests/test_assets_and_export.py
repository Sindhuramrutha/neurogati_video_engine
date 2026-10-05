"""The two stages added either end of the middle: Assets & Design, and Export.

Assets exists because nothing decided *which* extracted pictures were worth
showing, and nothing carried a deck's own look forward. Export exists because a
finished render is an .mp4 in a folder, and because the last place a wrong video
can be stopped had no checks on it at all.
"""

import io

import pytest
from PIL import Image, ImageDraw

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


def picture_bytes(colour="blue", size=(480, 360)):
    """Something shaped like a figure: content inside a margin.

    Not a flat block with one stray pixel. The library now opens each picture,
    trims its border and says what is in it, and a flat block is a divider rule.
    """
    image = Image.new("RGB", size, colour)
    draw = ImageDraw.Draw(image)
    inset = (max(1, size[0] // 8), max(1, size[1] // 8))
    draw.rectangle([inset, (size[0] - inset[0], size[1] - inset[1])],
                   outline=(0, 0, 0), width=max(1, size[0] // 80))
    draw.line([inset, (size[0] - inset[0], size[1] - inset[1])],
              fill=(255, 255, 255), width=2)
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
    assert library["figures"][1]["fills_a_frame"] is False
    assert library["audit"]["usable_count"] == 1, "decoration cannot be a scene's picture"
    assert library["audit"]["handed_on_count"] == 2, "but it is listed and handed on"


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

    assert library["figures"] == [], "only what the last transfer has is listed"
    assert library["audit"]["figure_count"] == 0 and library["audit"]["gone_count"] == 1
    assert library["gone_figures"] == ["Figure 1"], "named on the page, not just counted"
    assert any("not in the" in w and "not handed on" in w for w in library["warnings"])

    # It comes back, and so does the decision about it.
    ExtractionStore(project.root).save(Extraction(documents=[ExtractedDocument(
        file_name="chapter.docx", blocks=[ContentBlock(
            kind=BlockKind.FIGURE, text="Figure 1", heading_path=["Chapter"],
            asset_path="extraction/assets/pic0.png")])]))
    assert operations.refresh_asset_library(slug)["figures"][0]["use"] == FigureUse.USE


def test_a_new_transfer_is_gathered_when_the_page_opens(project_root):
    """It used to wait for the Gather button, so the page kept showing the
    previous transfer's pictures."""
    slug, project = project_with_pictures("Follows", [("Old chapter figure", (400, 300), "source")])
    operations.refresh_asset_library(slug)

    (project.root / "extraction" / "assets" / "new.png").write_bytes(picture_bytes("red"))
    ExtractionStore(project.root).save(Extraction(documents=[ExtractedDocument(
        file_name="next-chapter.pptx", blocks=[ContentBlock(
            kind=BlockKind.FIGURE, text="New chapter figure", heading_path=["Next"],
            asset_path="extraction/assets/new.png")])],
        extracted_at="2026-09-27T00:00:00+00:00", confirmed_at="2026-09-27T00:00:00+00:00"))

    library = operations.read_asset_library(slug)

    assert [f["caption"] for f in library["figures"]] == ["New chapter figure"]


def test_clearing_forgets_every_picture_and_decision(project_root):
    slug, project = project_with_pictures("Clear", [("Figure 1", (400, 300), "source")])
    operations.refresh_asset_library(slug)
    figure_id = operations.read_asset_library(slug)["figures"][0]["id"]
    operations.decide_figure(slug, figure_id, FigureUse.SKIP)

    library = operations.refresh_asset_library(slug, clear=True)

    assert library["figures"] == [] and library["is_empty"] is True
    assert operations.read_asset_library(slug)["is_empty"] is True, "and it stays empty"

    gathered = operations.refresh_asset_library(slug)
    assert [f["use"] for f in gathered["figures"]] == [FigureUse.UNDECIDED]
    assert gathered["figures"][0]["id"] == figure_id,         "the same picture always has the same id: it is derived from the picture"


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


# --- the video is made of the source material -----------------------------------------


def _figure_block(caption, heading_path, asset_path, origin="source"):
    return ContentBlock(kind=BlockKind.FIGURE, text=caption, heading_path=list(heading_path),
                        asset_path=asset_path, asset_origin=origin)


def project_with_sourced_sections(project_root):
    """Two plan sections, each pointing at its own heading, each with a figure."""
    from pipeline.planning import SourceReference

    slug = operations.create_project("Illustrated")["slug"]
    project = operations.require_project(slug)
    (project.root / "extraction" / "assets").mkdir(parents=True, exist_ok=True)
    for name, colour in (("one.png", "blue"), ("two.png", "green"), ("loose.png", "red")):
        (project.root / "extraction" / "assets" / name).write_bytes(picture_bytes(colour))

    ExtractionStore(project.root).save(Extraction(documents=[ExtractedDocument(
        file_name="chapter.docx",
        blocks=[
            ContentBlock(kind=BlockKind.HEADING, text="Signals", heading_path=["Signals"]),
            _figure_block("Figure 1", ["Signals"], "extraction/assets/one.png"),
            ContentBlock(kind=BlockKind.HEADING, text="Electrodes", heading_path=["Electrodes"]),
            _figure_block("Figure 2", ["Electrodes"], "extraction/assets/two.png"),
            ContentBlock(kind=BlockKind.HEADING, text="Appendix", heading_path=["Appendix"]),
            _figure_block("Figure 3", ["Appendix"], "extraction/assets/loose.png"),
        ],
    )], extracted_at="2026-09-17T00:00:00+00:00"))

    PlanStore(project.root).save(Plan(sections=[
        PlanSection(id="s1", title="Signals", estimated_seconds=30,
                    sources=[SourceReference(file_name="chapter.docx", heading_path=["Signals"])]),
        PlanSection(id="s2", title="Electrodes", estimated_seconds=30,
                    sources=[SourceReference(file_name="chapter.docx",
                                             heading_path=["Electrodes"])]),
    ]))
    return slug, project


def test_a_section_shows_the_pictures_from_its_own_source(project_root):
    """The whole point: a diagram appears beside the words it belongs to. Before
    this, sixty-three extracted pictures sat on disk and the video was text."""
    from pipeline.render_run import pictures_for_sections

    slug, project = project_with_sourced_sections(project_root)
    chosen = pictures_for_sections(project, operations.read_artifact(slug, "plan"))

    assert [p.name for p in chosen["s1"]] == ["one.png"]
    assert [p.name for p in chosen["s2"]] == ["two.png"]
    assert all("loose.png" not in [p.name for p in pictures] for pictures in chosen.values()), \
        "a figure under a heading no section covers belongs to no section"


def test_skipping_a_picture_in_the_library_keeps_it_out_of_the_video(project_root):
    from pipeline.render_run import pictures_for_sections

    slug, project = project_with_sourced_sections(project_root)
    operations.refresh_asset_library(slug)
    first = next(f for f in operations.read_asset_library(slug)["figures"]
                 if f["asset_path"].endswith("one.png"))
    operations.decide_figure(slug, first["id"], FigureUse.SKIP)

    chosen = pictures_for_sections(project, operations.read_artifact(slug, "plan"))

    assert chosen["s1"] == []
    # Its trimmed copy, not the file as the deck stored it: the margin around a
    # figure is not part of the figure, and drawing it wastes the frame.
    assert [p.stem.split("-")[0] for p in chosen["s2"]] == ["two"]


def test_a_trimmed_figure_is_what_the_video_actually_draws(project_root):
    """A deck's figure comes out with the slide background around it. Until the
    library opened one, that margin went on the frame at full size."""
    from pipeline.render_run import pictures_for_sections

    slug, project = project_with_sourced_sections(project_root)
    library = operations.refresh_asset_library(slug)

    trimmed = next(f for f in library["figures"] if f["asset_path"].endswith("two.png"))
    assert trimmed["prepared_path"], "a picture with a margin should have a trimmed copy"
    assert trimmed["trimmed_fraction"] > 0.1
    assert trimmed["width"] == 480, "the stored size is still what the deck held"
    assert trimmed["prepared_width"] < trimmed["width"]
    assert (project.root / trimmed["prepared_path"]).exists()

    chosen = pictures_for_sections(project, operations.read_artifact(slug, "plan"))
    assert chosen["s2"] == [project.root / trimmed["prepared_path"]]


def test_a_picture_with_nothing_in_it_is_not_proposed_for_the_video(project_root):
    """A divider rule is one flat tone from edge to edge. It was offered as a
    figure because nothing had ever opened it."""
    slug, project = project_with_pictures("Rules", [("Figure 1", (400, 300), "source")])
    flat = project.root / "extraction" / "assets" / "pic0.png"
    Image.new("RGB", (400, 300), (210, 210, 210)).save(flat)

    library = operations.refresh_asset_library(slug)
    figure = library["figures"][0]

    assert "blank" in figure["flags"]
    assert not figure["fills_a_frame"] and figure["why_not_a_frame"]
    assert library["audit"]["unfit_count"] == 1

    # Still choosable: the measurement is a default, not a veto.
    operations.decide_figure(slug, figure["id"], FigureUse.USE)
    from pipeline.assets import AssetLibraryStore

    assert len(AssetLibraryStore(project.root).load().usable()) == 1


def test_the_video_keeps_the_app_look_until_the_project_asks_for_the_deck_s(project_root):
    from pipeline.render_run import render_style_for
    from pipeline.rendering import DEFAULT_STYLE

    slug, project = project_with_sourced_sections(project_root)
    extraction = ExtractionStore(project.root).load()
    extraction.documents[0].design = DocumentDesign(
        aspect_ratio="16:9", theme_name="Office Theme",
        colours={"lt1": "#FFFFFF", "accent1": "#4472C4"},
        major_font="Calibri Light", minor_font="Calibri")
    ExtractionStore(project.root).save(extraction)
    operations.refresh_asset_library(slug)

    assert render_style_for(project) is DEFAULT_STYLE

    operations.set_project_look(slug, True)
    assert render_style_for(project) is DEFAULT_STYLE, "not until it is transferred"

    from pipeline.assets_handoff import confirm_assets

    confirm_assets(slug)
    style = render_style_for(project)

    assert style.background_colour == (255, 255, 255)
    assert style.accent_colour == (68, 114, 196)
    assert style.heading_font == "Calibri Light"
    assert style.is_light and style.text_colour != DEFAULT_STYLE.text_colour, \
        "text has to darken on a white deck or the video is unreadable"


def test_a_frame_actually_contains_the_picture(project_root):
    """Not "was passed a path" -- drawn. The pixels are the deliverable."""
    from pipeline.rendering import RenderStyle, _draw_frame

    picture = project_root / "diagram.png"
    picture.write_bytes(picture_bytes("blue", size=(400, 300)))
    style = RenderStyle(background_colour=(255, 255, 255))

    with_picture = _draw_frame("What a neuron does", ["threshold", "weights"],
                               "Signals", "Section 1", style, picture=picture)
    without = _draw_frame("What a neuron does", ["threshold", "weights"],
                          "Signals", "Section 1", style)

    blues = sum(1 for pixel in with_picture.getdata() if pixel[2] > 200 > pixel[0])
    assert blues > 50_000, f"the picture is not on the frame ({blues} of its pixels)"
    assert with_picture.tobytes() != without.tobytes()


def test_a_frame_draws_the_headline_and_its_labels_not_the_narration(project_root):
    """The words are being spoken. Printing them as well is what made this read
    as slides with a voice over them."""
    from pipeline.rendering import (
        RenderStyle,
        _draw_frame,
        _draw_point_layer,
        _words_layout,
    )

    style = RenderStyle(background_colour=(255, 255, 255))
    points = ["threshold", "weights"]

    bare = _draw_frame("What a neuron does", points, "Signals", "Section 1", style)
    with_first = _draw_frame("What a neuron does", points, "Signals", "Section 1",
                             style, revealed=1)
    with_both = _draw_frame("What a neuron does", points, "Signals", "Section 1",
                            style, revealed=2)

    assert bare.tobytes() != with_first.tobytes(), "a revealed label must be drawn"
    assert with_first.tobytes() != with_both.tobytes()

    # The overlay a label arrives on has to land where the frame would have
    # drawn it, or a build jumps as each one appears.
    layout = _words_layout("What a neuron does", points, style, False, False)
    layer_path = project_root / "layer.png"
    _draw_point_layer("What a neuron does", points, 0, style, False, layer_path)

    from PIL import Image

    with Image.open(layer_path) as layer:
        drawn = layer.convert("RGBA").getbbox()
    _text, left, top = layout.point_rows[0]
    assert drawn is not None and drawn[0] >= left - 2 and abs(drawn[1] - top) < 60


def test_an_unreadable_picture_does_not_stop_the_render(project_root):
    """A broken figure is exactly what the extraction review exists to find; it
    must not also take the whole video down."""
    from pipeline.rendering import _draw_frame

    broken = project_root / "broken.png"
    broken.write_bytes(b"this is not an image")

    frame = _draw_frame("What a neuron does", [], "Signals", "Section 1", picture=broken)

    assert frame.size == (1920, 1080)
