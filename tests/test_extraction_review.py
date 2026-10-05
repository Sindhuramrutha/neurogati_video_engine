"""Reviewing what extraction produced.

The checks are the point of these tests: a blank diagram, a corrupt file and a
3-pixel rule are things a person would notice immediately and that nothing in
the pipeline noticed at all. They must be found without a model, so none of
these tests stand one up except the ones about the agent pass.
"""

import io

import pytest
from PIL import Image

from pipeline import extraction_review, operations
from pipeline.extraction import (
    BlockKind,
    ContentBlock,
    ExtractedDocument,
    Extraction,
    ExtractionCollectionStore,
)
from pipeline.extraction_review import (
    ExtractionReviewStore,
    FindingKind,
    review_extraction,
)
from pipeline.operations import OperationFailed


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def picture_bytes(colour="red", size=(120, 90), noise=True):
    image = Image.new("RGB", size, colour)
    if noise:
        # A real diagram has more than one tone in it.
        image.putpixel((0, 0), (0, 0, 0))
        image.putpixel((size[0] - 1, size[1] - 1), (255, 255, 255))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def project_with_figures(slug, figures, extra_blocks=()):
    """A project whose extraction holds these figures.

    `figures` is a list of (caption, bytes or None, stored name or None).
    """
    created = operations.create_project(slug)["slug"]
    project = operations.require_project(created)
    assets = project.root / "extraction" / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    blocks = [ContentBlock(kind=BlockKind.HEADING, text="Chapter 2", heading_path=["Chapter 2"])]
    for caption, content, name in figures:
        stored = ""
        if name:
            stored = f"extraction/assets/{name}"
            if content is not None:
                (project.root / stored).write_bytes(content)
        blocks.append(ContentBlock(
            kind=BlockKind.FIGURE, text=caption, heading_path=["Chapter 2"],
            asset_path=stored,
        ))
    blocks.extend(extra_blocks)

    ExtractionCollectionStore(project.root).save(Extraction(
        documents=[ExtractedDocument(file_name="chapter-2.docx", blocks=blocks)],
        extracted_at="2026-09-17T00:00:00+00:00",
    ))
    return created, project


def kinds_of(result):
    return [finding["kind"] for finding in result["findings"]]


# --- the pictures themselves -------------------------------------------------------


def test_a_blank_picture_is_reported(project_root):
    """A diagram that extracted as a flat white rectangle looks fine in the
    block list and shows as nothing at all in the video."""
    slug, _ = project_with_figures("blank", [
        ("Figure 2.1 the acquisition chain", picture_bytes("white", noise=False), "blank.png"),
    ])

    result = review_extraction(slug)

    assert kinds_of(result) == [FindingKind.PICTURE_BLANK]
    assert result["error_count"] == 1
    assert "Figure 2.1" in result["findings"][0]["what"]
    assert result["findings"][0]["where"] == "chapter-2.docx › Chapter 2"


def test_a_corrupt_file_is_reported(project_root):
    slug, _ = project_with_figures("corrupt", [
        ("Figure 2.2", b"this is not a png", "broken.png"),
    ])

    result = review_extraction(slug)

    assert kinds_of(result) == [FindingKind.PICTURE_UNREADABLE]
    assert result["findings"][0]["severity"] == "error"


def test_a_picture_whose_file_went_missing_is_reported(project_root):
    slug, _ = project_with_figures("missing", [("Figure 2.3", None, "gone.png")])

    result = review_extraction(slug)

    assert kinds_of(result) == [FindingKind.PICTURE_MISSING]


def test_a_figure_with_no_saved_picture_is_reported(project_root):
    slug, _ = project_with_figures("unsaved", [("Figure 2.4", None, None)])

    result = review_extraction(slug)

    assert kinds_of(result) == [FindingKind.PICTURE_NOT_SAVED]
    assert "Extract images" in result["findings"][0]["suggestion"]


def test_a_rule_and_a_bullet_are_notes_not_errors(project_root):
    """Decks are full of 8-pixel spacers. Reporting them as errors would bury
    the one figure that actually broke."""
    slug, _ = project_with_figures("decoration", [
        ("bullet", picture_bytes("red", size=(8, 8)), "bullet.png"),
        ("divider", picture_bytes("red", size=(600, 4)), "rule.png"),
    ])

    result = review_extraction(slug)

    assert kinds_of(result) == [FindingKind.PICTURE_TINY, FindingKind.PICTURE_TINY]
    assert result["error_count"] == 0


def test_a_good_picture_is_not_reported(project_root):
    slug, _ = project_with_figures("fine", [
        ("Figure 2.5", picture_bytes("blue"), "good.png"),
    ])

    result = review_extraction(slug)

    assert result["findings"] == []
    assert result["open_count"] == 0


def test_text_that_promises_a_figure_nobody_extracted(project_root):
    slug, _ = project_with_figures("promised", [], extra_blocks=[
        ContentBlock(kind=BlockKind.PARAGRAPH, heading_path=["Chapter 2"],
                     text="As Figure 2.1 shows, the signal is amplified before filtering."),
    ])

    result = review_extraction(slug)

    assert kinds_of(result) == [FindingKind.REFERENCE_WITHOUT_FIGURE]
    assert "Figure 2.1" in result["findings"][0]["what"]


def test_a_document_with_figures_is_not_nagged_about_references(project_root):
    """"Figure 2.1" in a document full of figures is a reference to one of them."""
    slug, _ = project_with_figures("has-figures", [
        ("Figure 2.1", picture_bytes("green"), "fig.png"),
    ], extra_blocks=[
        ContentBlock(kind=BlockKind.PARAGRAPH, heading_path=["Chapter 2"],
                     text="As Figure 2.1 shows, the signal is amplified."),
    ])

    result = review_extraction(slug)

    assert result["findings"] == []


def test_a_chapter_that_lost_one_figure_of_many_is_still_reported(project_root):
    """The case that actually happens, and the one the old check could not see.

    It skipped any document that extracted at least one figure, so a chapter
    with figures 1 and 2 present and "as Figure 7 shows" in the text read as
    clean -- only the all-or-nothing case was ever caught.
    """
    slug, _ = project_with_figures("partly-lost", [
        ("Figure 2.1", picture_bytes("green"), "one.png"),
        ("Figure 2.2", picture_bytes("blue"), "two.png"),
    ], extra_blocks=[
        ContentBlock(kind=BlockKind.PARAGRAPH, heading_path=["Chapter 2"],
                     text="As Figure 2.7 shows, the signal is amplified."),
    ])

    result = review_extraction(slug)

    assert kinds_of(result) == [FindingKind.REFERENCE_WITHOUT_FIGURE]
    assert "Figure 2.7" in result["findings"][0]["what"]


def test_a_document_that_extracted_to_nothing_is_reported(project_root):
    slug = operations.create_project("Empty Doc")["slug"]
    project = operations.require_project(slug)
    ExtractionCollectionStore(project.root).save(Extraction(
        documents=[
            ExtractedDocument(file_name="scan.pdf", blocks=[]),
            ExtractedDocument(file_name="real.docx", blocks=[
                ContentBlock(kind=BlockKind.PARAGRAPH, text="Words."),
            ]),
        ],
        extracted_at="2026-09-17T00:00:00+00:00",
    ))

    result = review_extraction(slug)

    assert kinds_of(result) == [FindingKind.EMPTY_DOCUMENT]
    assert result["findings"][0]["file_name"] == "scan.pdf"


def test_reviewing_nothing_is_refused(project_root):
    slug = operations.create_project("Nothing Yet")["slug"]

    with pytest.raises(OperationFailed, match="nothing in its extraction collection"):
        review_extraction(slug)


# --- acting on a finding -----------------------------------------------------------


def test_a_finding_can_be_acknowledged_and_stays_that_way(project_root):
    slug, _ = project_with_figures("ack", [
        ("Figure 2.1", picture_bytes("white", noise=False), "blank.png"),
    ])
    result = review_extraction(slug)
    finding_id = result["findings"][0]["id"]

    after = extraction_review.acknowledge_finding(slug, finding_id)
    assert after["open_count"] == 0
    assert after["findings"][0]["acknowledged"] is True

    again = review_extraction(slug)
    assert again["open_count"] == 0, "re-reviewing must not resurrect what was dismissed"


def test_acknowledging_something_that_is_not_there_is_refused(project_root):
    slug, _ = project_with_figures("no-finding", [])
    ExtractionReviewStore(operations.require_project(slug).root).load()

    with pytest.raises(OperationFailed, match="no finding"):
        extraction_review.acknowledge_finding(slug, "made-up")


def test_a_replacement_picture_is_stored_and_the_block_points_at_it(project_root):
    slug, project = project_with_figures("replace", [
        ("Figure 2.1", picture_bytes("white", noise=False), "blank.png"),
    ])
    block_id = next(
        block.id for block in ExtractionCollectionStore(project.root).load().documents[0].blocks
        if block.kind == BlockKind.FIGURE
    )

    result = extraction_review.replace_figure(
        slug, block_id, picture_bytes("blue"), ".png")

    stored = ExtractionCollectionStore(project.root).load().documents[0].blocks[1]
    assert stored.asset_path == result["asset_path"] != "extraction/assets/blank.png"
    assert (project.root / stored.asset_path).exists()
    # Said, because the next layer only gets it once it is transferred again.
    assert "Transfer again" in result["note"]

    assert review_extraction(slug)["findings"] == [], \
        "the finding must be gone once the picture is fixed"


def test_a_replacement_that_is_not_an_image_is_refused(project_root):
    slug, project = project_with_figures("bad-upload", [
        ("Figure 2.1", picture_bytes("white", noise=False), "blank.png"),
    ])
    block_id = next(
        block.id for block in ExtractionCollectionStore(project.root).load().documents[0].blocks
        if block.kind == BlockKind.FIGURE
    )

    with pytest.raises(OperationFailed, match="not an image"):
        extraction_review.replace_figure(slug, block_id, b"<html>nope</html>", ".png")


def test_replacing_something_that_is_not_a_figure_is_refused(project_root):
    slug, project = project_with_figures("not-a-figure", [])
    heading_id = ExtractionCollectionStore(project.root).load().documents[0].blocks[0].id

    with pytest.raises(OperationFailed, match="not a figure"):
        extraction_review.replace_figure(slug, heading_id, picture_bytes(), ".png")


def test_a_review_of_an_older_extraction_says_it_is_out_of_date(project_root):
    slug, project = project_with_figures("stale", [
        ("Figure 2.1", picture_bytes("white", noise=False), "blank.png"),
    ])
    review_extraction(slug)

    extraction = ExtractionCollectionStore(project.root).load()
    extraction.documents[0].blocks.append(
        ContentBlock(kind=BlockKind.PARAGRAPH, text="A new paragraph.",
                     heading_path=["Chapter 2"]))
    ExtractionCollectionStore(project.root).save(extraction)

    assert extraction_review.read_extraction_review(slug)["is_stale"] is True


def test_a_drawn_picture_is_recorded_as_drawn(project_root, monkeypatch):
    """Everything else in a project comes from the source documents. A picture a
    model drew is the one thing that does not, and a video that shows it as the
    author's own diagram is making a false claim about the material."""
    slug, project = project_with_figures("drawn", [
        ("Figure 2.1 the acquisition chain", None, None),
    ], extra_blocks=[
        ContentBlock(kind=BlockKind.PARAGRAPH, heading_path=["Chapter 2"],
                     text="Electrodes feed an amplifier, then a filter, then a converter."),
    ])
    block_id = next(
        b.id for b in ExtractionCollectionStore(project.root).load().documents[0].blocks
        if b.kind == BlockKind.FIGURE
    )
    asked = {}

    def fake_draw(prompt, **kwargs):
        asked["prompt"] = prompt
        return picture_bytes("green")

    monkeypatch.setattr("pipeline.llm.draw_image", fake_draw)

    result = extraction_review.generate_figure(slug, block_id, "side by side")

    stored = next(
        b for b in ExtractionCollectionStore(project.root).load().documents[0].blocks
        if b.id == block_id
    )
    assert stored.asset_origin == "generated"
    assert (project.root / stored.asset_path).exists()
    assert result["asset_origin"] == "generated"
    # The prompt is built from the figure's own surroundings, not invented.
    assert "Figure 2.1 the acquisition chain" in asked["prompt"]
    assert "Electrodes feed an amplifier" in asked["prompt"]
    assert "side by side" in asked["prompt"]
    assert "Do not invent numbers" in asked["prompt"]


def test_an_uploaded_picture_is_recorded_as_uploaded(project_root):
    slug, project = project_with_figures("uploaded", [
        ("Figure 2.1", picture_bytes("white", noise=False), "blank.png"),
    ])
    block_id = next(
        b.id for b in ExtractionCollectionStore(project.root).load().documents[0].blocks
        if b.kind == BlockKind.FIGURE
    )

    extraction_review.replace_figure(slug, block_id, picture_bytes("blue"), ".png")

    stored = next(
        b for b in ExtractionCollectionStore(project.root).load().documents[0].blocks
        if b.id == block_id
    )
    assert stored.asset_origin == "uploaded"


def test_drawing_reports_a_provider_failure_plainly(project_root, monkeypatch):
    slug, project = project_with_figures("draw-fails", [("Figure 2.1", None, None)])
    block_id = next(
        b.id for b in ExtractionCollectionStore(project.root).load().documents[0].blocks
        if b.kind == BlockKind.FIGURE
    )

    def unreachable(*_args, **_kwargs):
        from pipeline.llm import ModelCallFailed

        raise ModelCallFailed("Could not reach the model provider.")

    monkeypatch.setattr("pipeline.llm.draw_image", unreachable)

    with pytest.raises(OperationFailed, match="could not be drawn"):
        extraction_review.generate_figure(slug, block_id)
