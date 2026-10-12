"""The source, as the units a plan is made of: slides for a deck, top headings
otherwise.

A section covers one unit or a run of them, and a unit has a number, so a plan's
order can be checked (`plan_order.py`). For a deck the number is the slide's own.
For a document it is the heading's place in the document, counting only the
shallowest level that divides it -- so units never contain one another, and no
material is counted twice.
"""

from __future__ import annotations

from dataclasses import dataclass

from pipeline.planning import SourceReference


@dataclass(frozen=True)
class Unit:
    number: int
    title: str
    words: int
    pictures: int
    reference: SourceReference
    is_slide: bool


def _slides(document) -> list[Unit]:
    numbers = sorted({b.slide_number for b in document.blocks if b.slide_number})
    found = []
    for number in numbers:
        blocks = [b for b in document.blocks if b.slide_number == number]
        heading = next((b for b in blocks if b.kind == "heading"), None)
        title = heading.text if heading else f"Slide {number}"
        found.append(Unit(
            number=number, title=title,
            words=sum(len(b.text.split()) for b in blocks if b.kind not in ("heading", "figure")),
            pictures=sum(1 for b in blocks if b.kind == "figure"),
            reference=SourceReference(
                file_name=document.file_name, slide_number=number,
                heading_path=list(heading.heading_path) if heading else []),
            is_slide=True))
    return found


def _headings(document, start: int) -> list[Unit]:
    outline = document.heading_outline()
    levels = sorted({entry["level"] for entry in outline})
    level = next((lv for lv in levels if sum(e["level"] == lv for e in outline) >= 2),
                 levels[0] if levels else 0)
    found = []
    for entry in (e for e in outline if e["level"] == level):
        path = list(entry["heading_path"])
        blocks = document.blocks_under(path)
        found.append(Unit(
            number=start + len(found), title=" › ".join(path) or document.file_name,
            words=entry.get("words", 0),
            pictures=sum(1 for b in blocks if b.kind == "figure"),
            reference=SourceReference(file_name=document.file_name, heading_path=path),
            is_slide=False))
    if not found:
        found.append(Unit(
            number=start, title=document.file_name,
            words=sum(len(b.text.split()) for b in document.blocks),
            pictures=sum(1 for b in document.blocks if b.kind == "figure"),
            reference=SourceReference(file_name=document.file_name), is_slide=False))
    return found


def units_of(extraction) -> list[Unit]:
    """Every unit of the source, in order."""
    units: list[Unit] = []
    for document in extraction.documents:
        if any(b.slide_number for b in document.blocks):
            units.extend(_slides(document))
        else:
            units.extend(_headings(document, len(units) + 1))
    return units


def unit_numbers(section, units: list[Unit]) -> list[int]:
    """The units a plan section covers, by number, in its own order."""
    index = {_unit_key(u.reference, u.is_slide): u.number for u in units}
    numbers: list[int] = []
    for reference in section.sources:
        for is_slide in (True, False):
            number = index.get(_unit_key(reference, is_slide))
            if number is not None and number not in numbers:
                numbers.append(number)
    return numbers


def _unit_key(reference, is_slide: bool) -> tuple:
    """A slide is matched by its number, a part by its heading path."""
    return (reference.file_name, is_slide,
            reference.slide_number if is_slide else tuple(reference.heading_path))


def references_for(numbers: list[int], units: list[Unit]) -> list[SourceReference]:
    by_number = {unit.number: unit for unit in units}
    return [by_number[n].reference for n in numbers if n in by_number]


def unit_word(units: list[Unit]) -> str:
    return "slide" if units and units[0].is_slide else "part"


# One section's own source text. A section that covers a whole book is cut here,
# and the caller says so.
MAXIMUM_SECTION_SOURCE_CHARACTERS = 24_000


def section_source_text(extraction, references: list[SourceReference]) -> tuple[str, bool]:
    """The full text of these places, and whether it had to be cut. A slide is
    read by its number: two slides with the same title are two slides."""
    from pipeline.extraction import ExtractedDocument

    parts = []
    for reference in references:
        document = extraction.document(reference.file_name)
        if document is None:
            continue
        if reference.slide_number:
            blocks = [b for b in document.blocks if b.slide_number == reference.slide_number]
            text = ExtractedDocument(file_name=document.file_name, blocks=blocks).as_markdown()
            parts.append(f"--- slide {reference.slide_number} ---\n{text}")
        else:
            parts.append(f"--- {reference.label} ---\n"
                         f"{document.text_under(reference.heading_path)}")
    text = "\n\n".join(parts)
    if len(text) > MAXIMUM_SECTION_SOURCE_CHARACTERS:
        return text[:MAXIMUM_SECTION_SOURCE_CHARACTERS], True
    return text, False
