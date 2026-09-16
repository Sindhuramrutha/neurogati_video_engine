"""Reading source documents: order, figures, and knowing when it is out of date.

Each test here is one of three defects the Extraction agent reported against a
real project -- a table filed under the wrong section, a figure that was never
extracted, and a deck that was uploaded after the last run and silently left out.
The documents are built in the test so every assertion is about a structure we
know, not about whatever a sample file happens to contain.
"""

import io
import json

import docx
import pytest
from PIL import Image
from pptx import Presentation
from pptx.util import Inches

from pipeline import operations, orchestrator
from pipeline.extraction import (
    AssetSink,
    BlockKind,
    ContentBlock,
    ExtractedDocument,
    Extraction,
    read_docx,
    read_pptx,
)


def png_bytes(colour: str = "red", size: int = 24) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (size, size), colour).save(buffer, format="PNG")
    return buffer.getvalue()


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path / "projects"))
    get_settings.cache_clear()
    yield tmp_path / "projects"
    get_settings.cache_clear()


def chapter_with_a_table_and_a_figure(path, figure_colour="red"):
    """Two sections; the table and the figure both belong to the FIRST one."""
    document = docx.Document()
    document.add_heading("2.2 Electrodes", level=1)
    document.add_heading("2.2.9 Comparison of sensors", level=2)
    document.add_paragraph("The table below compares them.")

    table = document.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "Sensor"
    table.cell(0, 1).text = "Noise"
    table.cell(1, 0).text = "Wet"
    table.cell(1, 1).text = "Low"

    picture = path.parent / f"figure-{figure_colour}.png"
    picture.write_bytes(png_bytes(figure_colour))
    document.add_picture(str(picture), width=docx.shared.Inches(1))
    document.add_paragraph("Figure 2.1 The acquisition chain.")

    document.add_heading("2.3 Summary", level=1)
    document.add_paragraph("In closing.")
    document.save(path)
    return path


# --- document order ------------------------------------------------------------


def test_a_table_stays_where_it_is_in_the_document(tmp_path):
    """python-docx keeps paragraphs and tables in two separate lists. Reading
    one then the other put every table at the end of the document."""
    blocks = read_docx(chapter_with_a_table_and_a_figure(tmp_path / "chapter.docx"))
    kinds = [block.kind for block in blocks]

    table_at = kinds.index(BlockKind.TABLE)
    summary_at = next(
        index for index, block in enumerate(blocks) if block.text == "2.3 Summary"
    )
    assert table_at < summary_at, "the table was moved after a later section"


def test_a_table_is_filed_under_its_own_section(tmp_path):
    """The reported defect: the comparison table from 2.2.9 carried the heading
    path of the closing summary, so any claim quoting it pointed at the wrong
    section."""
    blocks = read_docx(chapter_with_a_table_and_a_figure(tmp_path / "chapter.docx"))
    table = next(block for block in blocks if block.kind == BlockKind.TABLE)

    assert table.heading_path == ["2.2 Electrodes", "2.2.9 Comparison of sensors"]
    assert "Wet | Low" in table.text


# --- figures -------------------------------------------------------------------


def test_a_word_figure_is_extracted_as_an_image(tmp_path):
    sink = AssetSink(tmp_path / "assets")
    blocks = read_docx(chapter_with_a_table_and_a_figure(tmp_path / "chapter.docx"), sink)

    figures = [block for block in blocks if block.kind == BlockKind.FIGURE]
    assert len(figures) == 1
    assert figures[0].heading_path[-1] == "2.2.9 Comparison of sensors"

    stored = tmp_path / "assets" / figures[0].asset_path.split("/")[-1]
    assert stored.exists()
    assert stored.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_reading_without_a_sink_writes_nothing(tmp_path):
    """Figures are opt-in, so a reader stays a pure function of its file."""
    before = set(tmp_path.rglob("*"))
    blocks = read_docx(chapter_with_a_table_and_a_figure(tmp_path / "chapter.docx"))
    written = set(tmp_path.rglob("*")) - before - {tmp_path / "chapter.docx",
                                                   tmp_path / "figure-red.png"}

    assert written == set()
    figure = next(block for block in blocks if block.kind == BlockKind.FIGURE)
    assert figure.asset_path == ""


def test_a_slide_picture_is_extracted_as_a_figure(tmp_path):
    picture = tmp_path / "diagram.png"
    picture.write_bytes(png_bytes("blue"))

    deck = Presentation()
    slide = deck.slides.add_slide(deck.slide_layouts[5])
    slide.shapes.title.text = "Neural signal chain"
    slide.shapes.add_picture(str(picture), Inches(1), Inches(2), width=Inches(2))
    deck.save(tmp_path / "deck.pptx")

    sink = AssetSink(tmp_path / "assets")
    blocks = read_pptx(tmp_path / "deck.pptx", sink)
    figure = next(block for block in blocks if block.kind == BlockKind.FIGURE)

    assert figure.heading_path == ["Neural signal chain"]
    assert "slide 1" in figure.text
    assert (tmp_path / "assets" / figure.asset_path.split("/")[-1]).exists()


def test_the_same_image_repeated_is_stored_once(tmp_path):
    """A logo on forty slides must not become forty files."""
    sink = AssetSink(tmp_path / "assets")
    first = sink.store(png_bytes("green"), ".png")
    second = sink.store(png_bytes("green"), ".png")

    assert first == second
    assert len(list((tmp_path / "assets").iterdir())) == 1


def test_figures_past_the_ceiling_are_skipped_and_counted(tmp_path, monkeypatch):
    from pipeline import extraction

    monkeypatch.setattr(extraction, "MAXIMUM_EXTRACTED_ASSET_BYTES", 150)
    sink = AssetSink(tmp_path / "assets")

    kept = sink.store(b"x" * 100, ".png")
    skipped = sink.store(b"y" * 100, ".png")

    assert kept and skipped == ""
    assert sink.skipped_for_size == 1


def test_figures_are_named_in_the_text_the_planner_reads():
    document = ExtractedDocument(file_name="a.docx", blocks=[
        ContentBlock(kind=BlockKind.FIGURE, text="Figure 2.1 The chain"),
    ])
    assert "[figure: Figure 2.1 The chain]" in document.as_markdown()


# --- a real run, through operations ---------------------------------------------


def test_a_run_stores_figures_under_the_project(project_root, tmp_path):
    slug = operations.create_project("Figures")["slug"]
    project = operations.require_project(slug)
    chapter_with_a_table_and_a_figure(project.sources_dir / "chapter.docx")
    (project.sources_dir / "figure-red.png").unlink()

    result = operations.run_extraction(slug)
    figure = next(
        block for block in result["documents"][0]["blocks"]
        if block["kind"] == BlockKind.FIGURE
    )

    assert figure["asset_path"].startswith("extraction/assets/")
    assert (project.root / figure["asset_path"]).exists()
    assert result["audit"]["figure_count"] == 1


def test_a_rerun_removes_figures_nothing_refers_to(project_root):
    """Deleting a picture-heavy deck used to leave its images behind for good."""
    slug = operations.create_project("Pruning")["slug"]
    project = operations.require_project(slug)
    chapter_with_a_table_and_a_figure(project.sources_dir / "one.docx", "red")
    (project.sources_dir / "figure-red.png").unlink()
    chapter_with_a_table_and_a_figure(project.sources_dir / "two.docx", "blue")
    (project.sources_dir / "figure-blue.png").unlink()

    operations.run_extraction(slug)
    assets = project.root / "extraction" / "assets"
    assert len(list(assets.iterdir())) == 2

    (project.sources_dir / "two.docx").unlink()
    operations.run_extraction(slug)

    assert len(list(assets.iterdir())) == 1


# --- knowing the extraction is out of date --------------------------------------


def test_freshness_before_any_run(project_root):
    slug = operations.create_project("Fresh")["slug"]
    freshness = operations.extraction_freshness(operations.require_project(slug))

    assert freshness["has_run"] is False
    assert freshness["is_stale"] is False


def test_a_source_added_after_the_run_makes_it_stale(project_root):
    """The reported defect: a deck uploaded after extraction was simply absent,
    and nothing on any page said so."""
    slug = operations.create_project("Stale")["slug"]
    project = operations.require_project(slug)
    (project.sources_dir / "notes.md").write_text("# One\n\ntext", encoding="utf-8")
    operations.run_extraction(slug)

    assert operations.extraction_freshness(project)["is_stale"] is False

    (project.sources_dir / "later.md").write_text("# Two\n\ntext", encoding="utf-8")
    freshness = operations.extraction_freshness(project)

    assert freshness["is_stale"] is True
    assert freshness["added"] == ["later.md"]


def test_a_removed_source_makes_it_stale_too(project_root):
    slug = operations.create_project("Removed")["slug"]
    project = operations.require_project(slug)
    (project.sources_dir / "a.md").write_text("# A\n\ntext", encoding="utf-8")
    (project.sources_dir / "b.md").write_text("# B\n\ntext", encoding="utf-8")
    operations.run_extraction(slug)

    (project.sources_dir / "b.md").unlink()
    freshness = operations.extraction_freshness(project)

    assert freshness["removed"] == ["b.md"]
    assert freshness["is_stale"] is True


def test_the_orchestrator_is_told_extraction_is_behind(project_root):
    slug = operations.create_project("Told")["slug"]
    project = operations.require_project(slug)
    (project.sources_dir / "a.md").write_text("# A\n\ntext", encoding="utf-8")
    operations.run_extraction(slug)
    (project.sources_dir / "deck.md").write_text("# Deck\n\ntext", encoding="utf-8")

    snapshot = orchestrator.pipeline_snapshot(project)

    assert "Extraction is out of date" in snapshot
    assert "not extracted yet: deck.md" in snapshot


# --- over HTTP --------------------------------------------------------------------


@pytest.fixture
def client(project_root):
    """The project service is a process-wide singleton holding the projects
    folder it was first built with, so each test starts it again against its own
    temporary folder -- the same reset the operations tests do."""
    from litestar.testing import TestClient

    from pipeline.web import routes_project as routes_project_module
    from pipeline.web.app import create_app

    routes_project_module._service = None
    with TestClient(app=create_app()) as test_client:
        yield test_client
    routes_project_module._service = None


def test_the_extraction_route_reports_staleness(project_root, client):
    slug = operations.create_project("Route")["slug"]
    project = operations.require_project(slug)
    (project.sources_dir / "a.md").write_text("# A\n\ntext", encoding="utf-8")
    operations.run_extraction(slug)
    (project.sources_dir / "b.md").write_text("# B\n\ntext", encoding="utf-8")

    body = client.get(f"/api/projects/{slug}/extraction").json()

    assert body["freshness"]["added"] == ["b.md"]
    assert any("b.md has not been extracted" in warning for warning in body["warnings"])


def test_an_extracted_figure_is_served_inert(project_root, client):
    slug = operations.create_project("Served")["slug"]
    project = operations.require_project(slug)
    assets = project.root / "extraction" / "assets"
    assets.mkdir(parents=True)
    (assets / "abc.png").write_bytes(png_bytes())

    response = client.get(f"/api/projects/{slug}/extraction/assets/abc.png")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/png")
    # Bytes from someone's upload, on this app's origin: never able to run.
    assert "sandbox" in response.headers["content-security-policy"]
    assert response.headers["x-content-type-options"] == "nosniff"


def test_the_asset_route_cannot_reach_outside_the_assets_folder(project_root, client):
    slug = operations.create_project("Escape")["slug"]
    project = operations.require_project(slug)
    (project.root / "extraction" / "assets").mkdir(parents=True)

    for attempt in ("..%2F..%2Fproject.json", "..\\..\\project.json", "project.json"):
        response = client.get(f"/api/projects/{slug}/extraction/assets/{attempt}")
        assert response.status_code == 404, attempt


def test_extraction_round_trips_with_figures():
    """An older content.json has no asset_path; it must still load."""
    old_shape = {"documents": [{"file_name": "a.docx", "blocks": [
        {"kind": "paragraph", "text": "hello", "heading_path": []},
    ]}], "extracted_at": "2026-01-01T00:00:00+00:00"}

    loaded = Extraction.model_validate(json.loads(json.dumps(old_shape)))
    assert loaded.documents[0].blocks[0].asset_path == ""
