"""Changes to extracted blocks: what the Extraction agent can propose, and how an
accepted set of them is applied.

The agent never edits anything itself. It proposes `BlockChange`s; a person
reads them and accepts or discards the lot. Accepting applies every change to
the collection in one save -- all of them or, if any fails, none -- and keeps
the file's blocks as they were, so the last accepted set can be undone.

Every change names the blocks it touches by id, and is checked against the
document before anything is written: a change to a block that has since been
removed or re-extracted is refused rather than applied to whatever now sits in
its place.

Pictures are the one thing a change can make that the source did not contain.
They are made and placed by the picture procedure in `figure_pictures`: the
picture only, never the slide's text, taking the old picture's place on the
slide, and recorded as generated so later stages can say so.
"""

from __future__ import annotations

import mimetypes
from typing import Any, Literal

from pydantic import BaseModel, Field

from pipeline.core import OperationFailed
from pipeline.extraction import (
    BlockKind,
    ContentBlock,
    ExtractedDocument,
    ExtractionCollectionStore,
)
from pipeline.figure_pictures import (
    edit_instruction,
    picture_prompt,
    set_picture,
    store_picture,
)
from pipeline.llm import ModelCallFailed, ModelNotConfigured
from pipeline.projects import Project
from pipeline.storage.documents import JsonDocumentStore

TEXT_KINDS = {BlockKind.HEADING, BlockKind.PARAGRAPH, BlockKind.LIST_ITEM, BlockKind.TABLE}
IMAGE_ACTIONS = {"redraw_image", "edit_image"}


class BlockChange(BaseModel):
    """One change to the extracted blocks of one file."""

    action: Literal[
        "edit_text", "change_kind", "merge", "move", "delete",
        "redraw_image", "edit_image", "add_image",
    ]
    # The blocks it acts on, by id. `merge` takes two or more, in the order the
    # merged text should read; `move` and `delete` take any number.
    block_ids: list[str] = Field(default_factory=list)
    text: str = ""            # edit_text: the new text; merge: optional merged text
    kind: str = ""            # change_kind: the new kind; merge: optional
    after_block_id: str = ""  # move / add_image: place after this block ("" = top of slide)
    instruction: str = ""     # redraw_image / edit_image / add_image: what to picture
    reason: str = ""          # why, in a sentence, for the person deciding


def _blocks_by_id(document: ExtractedDocument) -> dict[str, ContentBlock]:
    return {block.id: block for block in document.blocks}


def check_change(document: ExtractedDocument, change: BlockChange) -> str:
    """What is wrong with this change against this document, or "" if nothing."""
    blocks = _blocks_by_id(document)
    if change.action == "add_image":
        # A new picture is placed after a block rather than made of one.
        if change.after_block_id not in blocks:
            return "a new picture needs the block it goes after"
        if not change.instruction.strip():
            return "a new picture needs a description of what to draw"
        return ""
    missing = [block_id for block_id in change.block_ids if block_id not in blocks]
    if not change.block_ids:
        return "it names no block"
    if missing:
        return f"it names {len(missing)} block(s) this file does not have"
    targets = [blocks[block_id] for block_id in change.block_ids]

    if change.action == "edit_text":
        if len(targets) != 1 or not change.text.strip():
            return "an edit needs exactly one block and its new text"
    elif change.action == "change_kind":
        if change.kind not in TEXT_KINDS or any(t.kind not in TEXT_KINDS for t in targets):
            return "only text blocks can change kind, into heading, paragraph, list_item or table"
    elif change.action == "merge":
        if len(targets) < 2:
            return "a merge needs at least two blocks"
        if any(t.kind not in TEXT_KINDS for t in targets):
            return "only text blocks can be merged; figures stay whole"
        if change.kind and change.kind not in TEXT_KINDS:
            return f"{change.kind!r} is not a text kind"
    elif change.action == "move":
        if change.after_block_id and change.after_block_id not in blocks:
            return "the block to move it after is not in this file"
        if change.after_block_id in change.block_ids:
            return "a block cannot be moved after itself"
    elif change.action == "delete":
        if len(targets) >= len(document.blocks):
            return "it would delete every block of the file"
    elif change.action in IMAGE_ACTIONS:
        if len(targets) != 1 or targets[0].kind != BlockKind.FIGURE:
            return "a picture change needs exactly one figure block"
        if not change.instruction.strip():
            return "a picture change needs an instruction"
        if change.action == "edit_image" and not targets[0].asset_path:
            return "that figure has no stored picture to edit; redraw it instead"
    return ""


def describe_change(document: ExtractedDocument, change: BlockChange) -> str:
    """The change in a line, for the person who has to accept it."""
    blocks = _blocks_by_id(document)

    def quote(block_id: str) -> str:
        block = blocks.get(block_id)
        text = (block.text if block else "?").replace("\n", " ")
        return f"“{text[:60]}{'…' if len(text) > 60 else ''}”"

    count = len(change.block_ids)
    first = quote(change.block_ids[0]) if change.block_ids else ""
    return {
        "edit_text": f"Rewrite {first}",
        "change_kind": f"Make {first} a {change.kind.replace('_', ' ')}",
        "merge": f"Merge {count} blocks, starting {first}, into one",
        "move": f"Move {count} block(s), starting {first}, "
                + (f"after {quote(change.after_block_id)}" if change.after_block_id
                   else "to the top of the slide"),
        "delete": f"Delete {count} block(s), starting {first}",
        "redraw_image": f"Redraw the figure {first}: {change.instruction}",
        "edit_image": f"Edit the picture of {first}: {change.instruction}",
        "add_image": f"Add a new picture after {quote(change.after_block_id)}: "
                     f"{change.instruction}",
    }[change.action]


# --- applying ---------------------------------------------------------------------


def _apply_one(project: Project, document: ExtractedDocument, change: BlockChange) -> None:
    blocks = _blocks_by_id(document)
    targets = [blocks[block_id] for block_id in change.block_ids]

    if change.action == "add_image":
        _add_picture(project, document, blocks[change.after_block_id], change)
    elif change.action == "edit_text":
        targets[0].text = change.text
    elif change.action == "change_kind":
        for target in targets:
            target.kind = change.kind
            if change.kind == BlockKind.HEADING and not target.level:
                target.level = 2
    elif change.action == "merge":
        keep, rest = targets[0], targets[1:]
        joiner = "\n" if keep.kind in (BlockKind.TABLE, BlockKind.LIST_ITEM) else " "
        keep.text = change.text.strip() or joiner.join(t.text for t in targets)
        keep.kind = change.kind or keep.kind
        gone = {t.id for t in rest}
        document.blocks = [b for b in document.blocks if b.id not in gone]
    elif change.action == "delete":
        gone = set(change.block_ids)
        document.blocks = [b for b in document.blocks if b.id not in gone]
    elif change.action == "move":
        _move(document, change)
    elif change.action in IMAGE_ACTIONS:
        _change_picture(project, document, targets[0], change)


def _move(document: ExtractedDocument, change: BlockChange) -> None:
    """Take the blocks out and put them back after the anchor, in their order.

    A moved block takes the anchor's slide and place in the headings: it now
    belongs where it was put, and a later stage asking "what is on slide 3"
    should find it there.
    """
    moving = set(change.block_ids)
    moved = [b for b in document.blocks if b.id in moving]
    kept = [b for b in document.blocks if b.id not in moving]

    if change.after_block_id:
        anchor = next(b for b in kept if b.id == change.after_block_id)
        position = kept.index(anchor) + 1
    else:
        slide = moved[0].slide_number
        position = next((i for i, b in enumerate(kept) if b.slide_number == slide), 0)
        anchor = kept[position] if position < len(kept) else None
    if anchor is not None:
        for block in moved:
            block.slide_number = anchor.slide_number
            block.heading_path = list(anchor.heading_path)
    document.blocks = kept[:position] + moved + kept[position:]


def _draw(project: Project, document: ExtractedDocument, near: ContentBlock,
          what: str, instruction: str = "") -> str:
    """Draw a picture for where `near` is, by the picture procedure, and store it."""
    from pipeline.llm import draw_image

    return store_picture(project, draw_image(picture_prompt(document, near, what, instruction)))


def _change_picture(
    project: Project, document: ExtractedDocument, figure: ContentBlock, change: BlockChange,
) -> None:
    """Redraw a figure from a description, or edit its picture; either way the
    new picture takes the old one's place on the slide too."""
    from pipeline.llm import edit_image

    try:
        if change.action == "redraw_image":
            stored = _draw(project, document, figure,
                           figure.text or "an unnamed figure", change.instruction)
        else:
            source = project.root / figure.asset_path
            mime = mimetypes.guess_type(source.name)[0] or "image/png"
            stored = store_picture(project, edit_image(
                source.read_bytes(), mime, edit_instruction(change.instruction)))
    except ModelNotConfigured as failure:
        raise OperationFailed(str(failure)) from failure
    except ModelCallFailed as failure:
        raise OperationFailed(f"The picture could not be changed. {failure}") from failure
    set_picture(document, figure, stored, "generated")


def _add_picture(
    project: Project, document: ExtractedDocument, anchor: ContentBlock, change: BlockChange,
) -> None:
    """Draw a new picture and put it in as a figure after the anchor block.

    It takes the anchor's slide and place in the headings, and is recorded as
    generated: the source never contained it. It has no place on the original
    slide's layout -- replacing a picture the slide has is `redraw_image`.
    """
    try:
        stored = _draw(project, document, anchor, change.instruction)
    except ModelNotConfigured as failure:
        raise OperationFailed(str(failure)) from failure
    except ModelCallFailed as failure:
        raise OperationFailed(f"The picture could not be drawn. {failure}") from failure

    figure = ContentBlock(
        kind=BlockKind.FIGURE, text=(change.text.strip() or change.instruction.strip())[:300],
        heading_path=list(anchor.heading_path), slide_number=anchor.slide_number,
        asset_path=stored, asset_origin="generated",
    )
    position = document.blocks.index(anchor) + 1
    document.blocks = [*document.blocks[:position], figure, *document.blocks[position:]]


def apply_changes(
    project: Project, file_name: str, changes: list[BlockChange],
) -> tuple[ExtractedDocument, ExtractedDocument]:
    """Apply every change to one file's blocks, and save the collection once.

    Returns the document before and after. Nothing is saved unless every
    change applies -- a set is accepted as a whole, so it lands as a whole.
    """
    store = ExtractionCollectionStore(project.root)
    collection = store.load()
    before = collection.document(file_name)
    if before is None:
        raise OperationFailed(f"{file_name} is not in the extraction; extract it first.")

    working = before.model_copy(deep=True)
    for change in changes:
        problem = check_change(working, change)
        if problem:
            raise OperationFailed(
                f"Could not apply “{describe_change(working, change)}”: {problem}. "
                "Nothing was changed.")
        _apply_one(project, working, change)

    collection.documents = [working if d.file_name == file_name else d
                            for d in collection.documents]
    store.save(collection)
    return before, working


# --- undoing the last accepted set --------------------------------------------------


class UndoPoint(BaseModel):
    file_name: str = ""
    turn_id: str = ""
    document: ExtractedDocument | None = None
    # The collection's stamp right after the changes landed: undo is refused
    # once anything else has changed it, rather than throwing that away too.
    applied_stamp: str = ""


class UndoStore(JsonDocumentStore[UndoPoint]):
    def __init__(self, project_root) -> None:
        super().__init__(
            document_path=project_root / "extraction" / "agent-undo.json",
            model_type=UndoPoint, build_default=UndoPoint, description="agent undo point",
        )


def remember_for_undo(project: Project, file_name: str, turn_id: str,
                      before: ExtractedDocument) -> None:
    stamp = ExtractionCollectionStore(project.root).load().extracted_at
    UndoStore(project.root).save(UndoPoint(
        file_name=file_name, turn_id=turn_id, document=before, applied_stamp=stamp))


def undo_point(project: Project) -> UndoPoint:
    return UndoStore(project.root).load()


def undo_last(project: Project, file_name: str) -> dict[str, Any]:
    """Put a file's blocks back as they were before the last accepted changes."""
    point = UndoStore(project.root).load()
    if point.file_name != file_name or point.document is None:
        raise OperationFailed("There is nothing to undo for this file.")

    store = ExtractionCollectionStore(project.root)
    collection = store.load()
    if collection.extracted_at != point.applied_stamp:
        raise OperationFailed(
            "The extraction has changed since those edits, so undoing them would "
            "throw away the later changes too.")
    collection.documents = [point.document if d.file_name == file_name else d
                            for d in collection.documents]
    store.save(collection)
    UndoStore(project.root).save(UndoPoint())
    return {"file_name": file_name, "turn_id": point.turn_id}
