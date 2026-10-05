"""One contract, checked against every reader.

Extraction's docstring promises the same four things whatever the format: the
output is structural rather than summarised, headings stay headings, lists stay
lists, and nothing comes through twice. Each reader was written on its own and
tested on its own, so nothing held them to any of it -- which is how a deck came
to emit every slide heading a second time as a paragraph, and how a bulleted
deck lost every list it had while nobody noticed.

The fixtures below say the same document in each format. A reader that cannot
carry a structure simply does not claim it; what it does claim, it must get
right.
"""

import io

import docx
import pytest
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt

from pipeline.extraction import (
    AssetSink,
    BlockKind,
    read_docx,
    read_plain_text,
    read_pptx,
)

HEADING = "How Neurons Fire"
BULLET = "Dendrites collect signals"
SECOND_BULLET = "Axons carry them"
PROSE = "Walter Pitts formalised the idea in 1943."
CAPTION = "The McCulloch-Pitts neuron"


def png_bytes(colour: str = "blue", size: int = 24) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (size, size), colour).save(buffer, format="PNG")
    return buffer.getvalue()


def markdown_fixture(directory):
    path = directory / "chapter.md"
    path.write_text(
        f"# {HEADING}\n\n{PROSE}\n\n- {BULLET}\n- {SECOND_BULLET}\n",
        encoding="utf-8",
    )
    return path, lambda path, _sink: read_plain_text(path), {"heading", "list", "prose"}


def docx_fixture(directory):
    path = directory / "chapter.docx"
    document = docx.Document()
    document.add_heading(HEADING, level=1)
    document.add_paragraph(PROSE)
    document.add_paragraph(BULLET, style="List Bullet")
    document.add_paragraph(SECOND_BULLET, style="List Bullet")

    table = document.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "Sensor"
    table.cell(1, 0).text = "Wet"

    picture = directory / "figure.png"
    picture.write_bytes(png_bytes())
    document.add_picture(str(picture), width=docx.shared.Inches(1))
    document.save(path)
    return path, read_docx, {"heading", "list", "prose", "table", "figure"}


def pptx_placeholder_fixture(directory):
    """A deck built the ordinary way: the heading is in the title placeholder."""
    path = directory / "placeholder.pptx"
    deck = Presentation()
    slide = deck.slides.add_slide(deck.slide_layouts[1])
    slide.shapes.title.text = HEADING
    body = slide.placeholders[1].text_frame
    body.text = BULLET
    body.add_paragraph().text = SECOND_BULLET
    deck.save(path)
    return path, read_pptx, {"heading", "list"}


def pptx_textbox_fixture(directory):
    """A designed deck: no title placeholder, the heading is a plain text box.

    This is the shape real decks arrive in, and the one that produced every
    heading twice -- once as the heading and again as a paragraph.
    """
    path = directory / "designed.pptx"
    picture = directory / "figure.png"
    picture.write_bytes(png_bytes())

    deck = Presentation()
    slide = deck.slides.add_slide(deck.slide_layouts[6])  # blank: no placeholders

    head = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(1))
    head.text_frame.text = HEADING
    head.text_frame.paragraphs[0].runs[0].font.size = Pt(32)

    prose = slide.shapes.add_textbox(Inches(0.5), Inches(1.6), Inches(4), Inches(1))
    prose.text_frame.text = PROSE
    prose.text_frame.paragraphs[0].runs[0].font.size = Pt(14)

    slide.shapes.add_picture(str(picture), Inches(5), Inches(2), width=Inches(2))
    caption = slide.shapes.add_textbox(Inches(5), Inches(4.1), Inches(3), Inches(0.4))
    caption.text_frame.text = CAPTION
    caption.text_frame.paragraphs[0].runs[0].font.size = Pt(11)

    deck.save(path)
    return path, read_pptx, {"heading", "prose", "figure"}


FIXTURES = {
    "markdown": markdown_fixture,
    "docx": docx_fixture,
    "pptx-placeholder": pptx_placeholder_fixture,
    "pptx-textbox": pptx_textbox_fixture,
}


@pytest.fixture(params=sorted(FIXTURES))
def reading(request, tmp_path):
    path, reader, claims = FIXTURES[request.param](tmp_path)
    return reader(path, AssetSink(tmp_path / "assets")), claims


def test_every_reader_keeps_the_heading_as_a_heading(reading):
    blocks, claims = reading
    if "heading" not in claims:
        pytest.skip("this format carries no headings")

    headings = [b for b in blocks if b.kind == BlockKind.HEADING]
    assert HEADING in [b.text for b in headings]


def test_no_reader_emits_a_heading_twice(reading):
    """The defect this whole file exists for.

    A heading that is also a paragraph is the same words twice: read by the
    Scene Plan agent, written from by the Script agent, and counted again by the
    spoken-duration estimate that steers the plan.
    """
    blocks, _claims = reading
    headings = {b.text for b in blocks if b.kind == BlockKind.HEADING}
    repeated = [b.text for b in blocks
                if b.kind != BlockKind.HEADING and b.text in headings]

    assert repeated == [], f"emitted again as body text: {repeated}"


def test_a_bulleted_line_becomes_a_list_item(reading):
    blocks, claims = reading
    if "list" not in claims:
        pytest.skip("this fixture has no bulleted lines")

    items = [b.text for b in blocks if b.kind == BlockKind.LIST_ITEM]
    assert BULLET in items


def test_prose_stays_a_paragraph_and_is_not_mistaken_for_a_list(reading):
    blocks, claims = reading
    if "prose" not in claims:
        pytest.skip("this fixture has no prose")

    paragraphs = [b.text for b in blocks if b.kind == BlockKind.PARAGRAPH]
    assert PROSE in paragraphs


def test_a_table_survives_as_a_table(reading):
    blocks, claims = reading
    if "table" not in claims:
        pytest.skip("this format carries no tables")

    assert any(b.kind == BlockKind.TABLE for b in blocks)


def test_a_figure_survives_as_a_figure(reading):
    blocks, claims = reading
    if "figure" not in claims:
        pytest.skip("this format carries no figures")

    assert any(b.kind == BlockKind.FIGURE for b in blocks)


def test_nothing_is_extracted_twice(reading):
    blocks, _claims = reading
    seen = [(b.kind, b.text) for b in blocks if b.kind != BlockKind.FIGURE]

    assert len(seen) == len(set(seen)), f"duplicated blocks: {sorted(seen)}"


def test_no_reader_summarises(reading):
    """Structural, not summarised: every word out came from the document."""
    blocks, _claims = reading
    written = {BULLET, SECOND_BULLET, PROSE, HEADING, CAPTION}

    for block in blocks:
        if block.kind in (BlockKind.TABLE, BlockKind.FIGURE):
            continue
        assert any(known in block.text for known in written), \
            f"text that is in no fixture: {block.text!r}"


def test_a_slide_figure_is_captioned_from_the_slide_not_from_the_xml(tmp_path):
    """PowerPoint names every picture "Image 0"; the caption beside it is the caption.

    Everything downstream reads this string -- the drawing agent describes from
    it, Assets & Design asks Use or Skip on it, Generation matches the author's
    own figures by it -- so a shape name from the XML is worse than useless.
    """
    path, reader, _claims = pptx_textbox_fixture(tmp_path)
    blocks = reader(path, AssetSink(tmp_path / "assets"))

    figure = next(b for b in blocks if b.kind == BlockKind.FIGURE)

    assert CAPTION in figure.text
    assert "Image" not in figure.text
