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

import logging
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MAXIMUM_BLOCK_LENGTH = 20000
MAXIMUM_BLOCKS_PER_DOCUMENT = 5000

# Word counts are what the Planning stage reasons about when estimating spoken
# duration, so they are computed once here rather than re-derived per stage.
WORDS_PER_MINUTE_OF_NARRATION = 150


class BlockKind:
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    TABLE = "table"


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


def read_docx(path: Path) -> list[ContentBlock]:
    import docx

    document = docx.Document(str(path))
    blocks: list[ContentBlock] = []
    heading_path: list[str] = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue

        style_name = (paragraph.style.name or "").lower()

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

    # Tables come after the paragraph pass because python-docx does not interleave
    # them in `.paragraphs`. Rendered as pipe rows so the shape survives into the
    # markdown a model reads.
    for table in document.tables:
        rows = [
            " | ".join(cell.text.strip().replace("\n", " ") for cell in row.cells)
            for row in table.rows
        ]
        rendered = "\n".join(row for row in rows if row.replace("|", "").strip())
        if rendered:
            blocks.append(ContentBlock(
                kind=BlockKind.TABLE, text=rendered, heading_path=list(heading_path),
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


READERS_BY_SUFFIX = {
    ".docx": read_docx,
    ".pdf": read_pdf,
    ".md": read_plain_text,
    ".txt": read_plain_text,
}


def extract_document(path: Path) -> ExtractedDocument:
    reader = READERS_BY_SUFFIX.get(path.suffix.lower())
    if reader is None:
        raise SourceUnreadable(
            f"{path.name}: no reader for {path.suffix}. "
            f"Supported: {', '.join(sorted(READERS_BY_SUFFIX))}."
        )

    try:
        blocks = reader(path)
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
