"""Extraction — pull structured content out of the source documents.

The stage that was declared and never written. Until now the Planning agent saw
only the *names* of the source files, so asking it to plan a video about a
document it could not read was a guarantee of invention: it would produce a
plausible plan about the title.

The output is deliberately **structural, not summarised**. Headings stay
headings, tables stay tables, and nothing is paraphrased on the way in. Summarising
here would put an unreviewable lossy step between the source and every later
stage -- and when a fact went wrong nobody could tell whether the source was
wrong, the extraction dropped it, or the planner invented it. Blocks carry the
file and the heading path they came from, so any claim downstream can be traced
back to a place in a document.

No model is called. This is parsing, and a parser that is wrong is debuggable in
a way that a model that hallucinated a heading is not.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MAXIMUM_BLOCK_LENGTH = 20000
MAXIMUM_BLOCKS_PER_DOCUMENT = 5000

# Extracted figures are a copy of the pictures inside the source files, so a
# picture-heavy deck can approach the size of the deck itself. This is a ceiling
# against the pathological case -- a folder of large decks quietly filling the
# disk -- not a target; normal documents land far below it.
MAXIMUM_EXTRACTED_ASSET_BYTES = 512 * 1024 * 1024

# Word counts are what the Planning stage reasons about when estimating spoken
# duration, so they are computed once here rather than re-derived per stage.
WORDS_PER_MINUTE_OF_NARRATION = 150


class BlockKind:
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    TABLE = "table"
    FIGURE = "figure"


class ContentBlock(BaseModel):
    """One piece of a source document, kept in document order.

    `heading_path` is what makes a block quotable: "the 400 Hz figure came from
    2.2 Electrodes and Sensors > 2.2.3 Impedance" is a checkable statement, and
    a flat list of paragraphs cannot produce one.
    """

    id: str = Field(default_factory=new_identifier)
    kind: str = BlockKind.PARAGRAPH
    level: int = 0
    text: str = ""
    heading_path: list[str] = Field(default_factory=list)

    # Where the extracted image was written, relative to the project root. Only
    # a FIGURE block has one. Text extraction alone dropped every diagram on the
    # floor: a document could say "as Figure 2.1 shows" and nothing downstream
    # had any figure to show, so Studio narrated a picture that did not exist.
    asset_path: str = ""

    @field_validator("text")
    @classmethod
    def _cap_text(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_BLOCK_LENGTH]

    @property
    def word_count(self) -> int:
        return len(self.text.split())


class ExtractedDocument(BaseModel):
    file_name: str = ""
    blocks: list[ContentBlock] = Field(default_factory=list)
    extraction_note: str = ""

    @field_validator("blocks")
    @classmethod
    def _cap_blocks(cls, value: list[ContentBlock]) -> list[ContentBlock]:
        return value[:MAXIMUM_BLOCKS_PER_DOCUMENT]

    @property
    def word_count(self) -> int:
        return sum(block.word_count for block in self.blocks)

    def as_markdown(self) -> str:
        """The document as text a model can read.

        Markdown rather than the JSON: heading levels survive as `##`, which is a
        shape every model already understands, and it costs a fraction of the
        tokens that the block objects would.
        """
        lines: list[str] = []
        for block in self.blocks:
            if block.kind == BlockKind.HEADING:
                lines.append(f"\n{'#' * max(1, min(block.level, 6))} {block.text}")
            elif block.kind == BlockKind.LIST_ITEM:
                lines.append(f"- {block.text}")
            elif block.kind == BlockKind.TABLE:
                lines.append(f"\n{block.text}\n")
            elif block.kind == BlockKind.FIGURE:
                # Marked as a figure so the planner knows a real image exists at
                # this point and can plan to show it, instead of reading the
                # caption as one more sentence of prose.
                lines.append(f"[figure: {block.text}]")
            else:
                lines.append(block.text)
        return "\n".join(lines).strip()


class Extraction(BaseModel):
    documents: list[ExtractedDocument] = Field(default_factory=list)
    extracted_at: str = ""

    @property
    def total_word_count(self) -> int:
        return sum(document.word_count for document in self.documents)

    def as_markdown(self) -> str:
        return "\n\n".join(
            f"===== {document.file_name} =====\n{document.as_markdown()}"
            for document in self.documents
        )

    def audit(self) -> dict:
        return {
            "document_count": len(self.documents),
            "block_count": sum(len(d.blocks) for d in self.documents),
            "empty_document_names": [d.file_name for d in self.documents if not d.blocks],
            "heading_count": sum(
                1 for d in self.documents for b in d.blocks if b.kind == BlockKind.HEADING
            ),
            "figure_count": sum(
                1 for d in self.documents for b in d.blocks if b.kind == BlockKind.FIGURE
            ),
        }

    def to_dict(self) -> dict:
        audit = self.audit()
        estimated_minutes = round(
            self.total_word_count / WORDS_PER_MINUTE_OF_NARRATION, 1
        )
        return self.model_dump(mode="json") | {
            "total_word_count": self.total_word_count,
            "estimated_narration_minutes": estimated_minutes,
            "audit": audit,
            "warnings": self._warnings(audit),
            "is_empty": not self.documents,
        }

    def _warnings(self, audit: dict) -> list[str]:
        found: list[str] = []
        if audit["empty_document_names"]:
            found.append(
                f"nothing could be read from: {', '.join(audit['empty_document_names'])}"
            )
        if self.documents and not audit["heading_count"]:
            found.append(
                "no headings were found, so the planner has no structure to follow"
            )
        return found


class ExtractionStore(JsonDocumentStore[Extraction]):
    """Persistence for the extracted content."""

    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.EXTRACTION),
            model_type=Extraction,
            build_default=Extraction,
            description="extraction",
        )

    @property
    def extraction_path(self) -> Path:
        return self.document_path


# --- readers ----------------------------------------------------------------
#
# One per format. Each returns blocks in document order, or raises with a
# message naming the file -- an extraction that silently yields nothing looks
# identical to an empty document, and the two need different fixes.


class SourceUnreadable(Exception):
    """A source file could not be parsed. Names the file and the reason."""


def _heading_level(style_name: str) -> int:
    """Word's heading styles are 'Heading 1'..'Heading 9'."""
    digits = "".join(character for character in style_name if character.isdigit())
    return int(digits) if digits else 1


class AssetSink:
    """Somewhere to put the images pulled out of a document.

    Content-addressed by digest, so a logo repeated on forty slides is stored
    once rather than forty times -- which on a real 80 MB deck is the difference
    between a few megabytes of assets and most of the deck copied out again.

    Passed in rather than derived inside the readers so a reader stays a pure
    function of its file when nobody wants the images: `read_docx(path)` with no
    sink extracts text and writes nothing, which is what the tests and the
    preview path want.
    """

    def __init__(self, directory: Path, relative_to: Path | None = None) -> None:
        self.directory = directory
        self.relative_to = relative_to
        self.written: dict[str, str] = {}
        self.bytes_written = 0
        self.skipped_for_size = 0

    def store(self, blob: bytes, suffix: str) -> str:
        digest = hashlib.sha256(blob).hexdigest()[:16]
        if digest in self.written:
            return self.written[digest]

        if self.bytes_written + len(blob) > MAXIMUM_EXTRACTED_ASSET_BYTES:
            # Reported rather than raised: losing the last few figures of a very
            # large deck is a much smaller problem than failing the extraction
            # and keeping none of its text.
            self.skipped_for_size += 1
            return ""

        self.directory.mkdir(parents=True, exist_ok=True)
        destination = self.directory / f"{digest}{suffix.lower()}"
        if not destination.exists():
            destination.write_bytes(blob)

        stored = str(
            destination.relative_to(self.relative_to) if self.relative_to else destination
        ).replace("\\", "/")
        self.written[digest] = stored
        self.bytes_written += len(blob)
        return stored

    def prune_unreferenced(self) -> int:
        """Delete figures this run did not produce. Returns how many went.

        Called only after the new extraction is safely saved. Without it, removing
        a picture-heavy deck from a project left most of its size behind in
        `extraction/assets/` for good, referenced by nothing.
        """
        if not self.directory.exists():
            return 0
        kept = {Path(stored).name for stored in self.written.values()}
        removed = 0
        for candidate in self.directory.iterdir():
            if candidate.is_file() and candidate.name not in kept:
                candidate.unlink()
                removed += 1
        return removed


def _render_table(table) -> str:
    """A table as pipe rows, so its shape survives into the markdown a model reads."""
    rows = [
        " | ".join(cell.text.strip().replace("\n", " ") for cell in row.cells)
        for row in table.rows
    ]
    return "\n".join(row for row in rows if row.replace("|", "").strip())


def _walk_document_body(document):
    """Paragraphs and tables, interleaved, in the order they appear on the page.

    `document.paragraphs` and `document.tables` are two separate sequences, so
    the obvious reading -- all the paragraphs, then all the tables -- puts every
    table at the end of the document under whatever heading happened to come
    last. In a real chapter that meant a comparison table belonging to 2.2.9
    filed under the closing summary, which is not a cosmetic ordering problem:
    `heading_path` is what makes a block quotable, and it was pointing at the
    wrong section.

    The body's own XML children are already in document order, so walking those
    and wrapping each one is the only reading that matches the file.

    Yields `("paragraph" | "table", item)`. The tag is explicit because the two
    wrapper classes share enough of an interface to be mistaken for each other.
    """
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    for child in document.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield "paragraph", Paragraph(child, document)
        elif isinstance(child, CT_Tbl):
            yield "table", Table(child, document)


def _paragraph_images(paragraph, document) -> list[tuple[str, bytes]]:
    """Every image anchored in this paragraph, as (extension, bytes).

    Found through the drawing relationships rather than `document.part.image_parts`
    so each image is tied to the paragraph it sits in -- which is what gives a
    figure its position and its caption.
    """
    from docx.oxml.ns import qn

    found = []
    for blip in paragraph._element.findall(f".//{qn('a:blip')}"):
        relationship_id = blip.get(qn("r:embed")) or blip.get(qn("r:link"))
        if not relationship_id:
            continue
        try:
            part = document.part.related_parts[relationship_id]
        except KeyError:
            continue
        blob = getattr(part, "blob", None)
        if not blob:
            continue
        suffix = Path(str(getattr(part, "partname", ".png"))).suffix or ".png"
        found.append((suffix, blob))
    return found


def read_docx(path: Path, assets: AssetSink | None = None) -> list[ContentBlock]:
    import docx

    document = docx.Document(str(path))
    blocks: list[ContentBlock] = []
    heading_path: list[str] = []
    figure_number = 0

    for kind, item in _walk_document_body(document):
        if kind == "table":
            # It takes the heading path current *at this point in the document*,
            # which is the whole reason for walking in order. Tagged rather than
            # sniffed: a python-docx `Table` has a `.style` just as a paragraph
            # does, so telling them apart by attribute silently sends tables
            # down the paragraph branch.
            rendered = _render_table(item)
            if rendered:
                blocks.append(ContentBlock(
                    kind=BlockKind.TABLE, text=rendered, heading_path=list(heading_path),
                ))
            continue

        paragraph = item
        text = paragraph.text.strip()
        style_name = (paragraph.style.name or "").lower()

        # Images first: a figure usually sits in a paragraph of its own, so
        # checking text alone skips it entirely.
        for suffix, blob in _paragraph_images(paragraph, document):
            figure_number += 1
            caption = text or f"Figure {figure_number} from {path.name}"
            stored = assets.store(blob, suffix) if assets else ""
            blocks.append(ContentBlock(
                kind=BlockKind.FIGURE, text=caption,
                heading_path=list(heading_path), asset_path=stored,
            ))

        if not text:
            continue

        if style_name.startswith("heading"):
            level = _heading_level(paragraph.style.name)
            # Keep the path to this heading, dropping any deeper headings it
            # replaces, so every later block knows where in the document it sits.
            heading_path = heading_path[: level - 1] + [text]
            blocks.append(ContentBlock(
                kind=BlockKind.HEADING, level=level, text=text,
                heading_path=list(heading_path),
            ))
        elif style_name.startswith("list"):
            blocks.append(ContentBlock(
                kind=BlockKind.LIST_ITEM, text=text, heading_path=list(heading_path),
            ))
        else:
            blocks.append(ContentBlock(
                kind=BlockKind.PARAGRAPH, text=text, heading_path=list(heading_path),
            ))

    return blocks


def read_pdf(path: Path) -> list[ContentBlock]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    blocks: list[ContentBlock] = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            continue
        blocks.append(ContentBlock(
            kind=BlockKind.HEADING, level=2, text=f"Page {page_number}",
            heading_path=[f"Page {page_number}"],
        ))
        for chunk in (part.strip() for part in text.split("\n\n")):
            if chunk:
                blocks.append(ContentBlock(
                    kind=BlockKind.PARAGRAPH, text=chunk,
                    heading_path=[f"Page {page_number}"],
                ))
    return blocks


def read_plain_text(path: Path) -> list[ContentBlock]:
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks: list[ContentBlock] = []
    heading_path: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            title = line.lstrip("#").strip()
            heading_path = heading_path[: level - 1] + [title]
            blocks.append(ContentBlock(
                kind=BlockKind.HEADING, level=level, text=title,
                heading_path=list(heading_path),
            ))
        elif line.startswith(("- ", "* ")):
            blocks.append(ContentBlock(
                kind=BlockKind.LIST_ITEM, text=line[2:].strip(),
                heading_path=list(heading_path),
            ))
        else:
            blocks.append(ContentBlock(
                kind=BlockKind.PARAGRAPH, text=line, heading_path=list(heading_path),
            ))
    return blocks


def read_pptx(path: Path, assets: AssetSink | None = None) -> list[ContentBlock]:
    """One heading per slide, then its text and tables.

    `.pptx` was accepted on upload and advertised on the Inputs page from the
    start, with no reader behind it: a deck uploaded fine and then dead-ended at
    extraction with "no reader for .pptx". Advertising a format the pipeline
    cannot read is worse than refusing it.
    """
    from pptx import Presentation

    presentation = Presentation(str(path))
    blocks: list[ContentBlock] = []
    figure_number = 0

    for number, slide in enumerate(presentation.slides, start=1):
        # A slide's own title if it has one, so the heading path means something.
        title = ""
        if slide.shapes.title is not None and slide.shapes.title.has_text_frame:
            title = slide.shapes.title.text.strip()
        heading = title or f"Slide {number}"
        heading_path = [heading]

        blocks.append(ContentBlock(
            kind=BlockKind.HEADING, level=2, text=heading, heading_path=list(heading_path),
        ))

        for shape in slide.shapes:
            if shape is slide.shapes.title:
                continue
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    line = "".join(run.text for run in paragraph.runs).strip()
                    if not line:
                        continue
                    # Bulleted levels stay list items so the structure survives.
                    kind = BlockKind.LIST_ITEM if paragraph.level else BlockKind.PARAGRAPH
                    blocks.append(ContentBlock(
                        kind=kind, text=line, heading_path=list(heading_path),
                    ))
            elif getattr(shape, "has_table", False):
                rendered = _render_table(shape.table)
                if rendered:
                    blocks.append(ContentBlock(
                        kind=BlockKind.TABLE, text=rendered, heading_path=list(heading_path),
                    ))
            else:
                # A picture. Slides carry most of their meaning in diagrams, so a
                # text-only reading of a deck loses more than it keeps.
                image = getattr(shape, "image", None)
                if image is None:
                    continue
                figure_number += 1
                caption = (getattr(shape, "name", "") or "").strip()
                blocks.append(ContentBlock(
                    kind=BlockKind.FIGURE,
                    text=f"{caption or 'Figure'} (slide {number})",
                    heading_path=list(heading_path),
                    asset_path=assets.store(image.blob, f".{image.ext}") if assets else "",
                ))

        if slide.has_notes_slide:
            notes = (slide.notes_slide.notes_text_frame.text or "").strip()
            if notes:
                blocks.append(ContentBlock(
                    kind=BlockKind.PARAGRAPH, text=f"[speaker notes] {notes}",
                    heading_path=list(heading_path),
                ))

    return blocks


READERS_BY_SUFFIX = {
    ".docx": read_docx,
    ".pptx": read_pptx,
    ".pdf": read_pdf,
    ".md": read_plain_text,
    ".txt": read_plain_text,
}


def extract_document(path: Path, assets: AssetSink | None = None) -> ExtractedDocument:
    reader = READERS_BY_SUFFIX.get(path.suffix.lower())
    if reader is None:
        raise SourceUnreadable(
            f"{path.name}: no reader for {path.suffix}. "
            f"Supported: {', '.join(sorted(READERS_BY_SUFFIX))}."
        )

    # Only the readers that can produce figures take a sink; the rest stay
    # single-argument, so adding one later is a signature change rather than a
    # silently ignored keyword.
    takes_assets = reader in (read_docx, read_pptx)

    try:
        blocks = reader(path, assets) if takes_assets else reader(path)
    except SourceUnreadable:
        raise
    except Exception as parse_failure:
        raise SourceUnreadable(
            f"{path.name}: {type(parse_failure).__name__}: {parse_failure}"
        ) from parse_failure

    return ExtractedDocument(
        file_name=path.name,
        blocks=blocks,
        extraction_note=f"{len(blocks)} block(s) read by {reader.__name__}",
    )
