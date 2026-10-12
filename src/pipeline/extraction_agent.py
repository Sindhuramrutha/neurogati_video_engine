"""The Extraction agent, as conversations beside the extracted blocks.

You say what you want -- "merge the timeline items", "make this a heading",
"redraw this diagram with larger labels" -- and the agent answers with a reply
and, when something should change, a proposal: a list of `BlockChange`s shown
one line each. Nothing changes until you apply it; applied changes can be
undone. See `extraction_edits` for what a change is and how it lands.

The agent is shown the slide on screen as it looks -- the whole slide drawn as
a picture, its figures and its background -- with that slide's blocks, layout
and background in full, and a compact index of the rest of the file so it can
act more widely when asked.

Each file has its own conversations: a new one can be started at any time and
a past one reopened. Kept at `extraction/agent.json`.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from pipeline.core import OperationFailed, require_project
from pipeline.extraction import ExtractedDocument, ExtractionCollectionStore
from pipeline.extraction_agent_pictures import agent_pictures, looked_at_summary
from pipeline.extraction_edits import (
    BlockChange,
    check_change,
    describe_change,
    undo_point,
)
from pipeline.projects import Project
from pipeline.storage.documents import JsonDocumentStore, new_identifier

logger = logging.getLogger(__name__)

MAXIMUM_CONVERSATIONS_KEPT = 30
MAXIMUM_TURNS_KEPT = 60
MAXIMUM_TURNS_SHOWN_TO_THE_AGENT = 8
MAXIMUM_INDEX_CHARACTERS = 20_000
MAXIMUM_BLOCK_CHARACTERS = 1_200

GUIDE = """
You are working with a person on the extracted content of ONE file, shown below
as blocks. Each block has an id in square brackets, a kind and its text.

Pictures are attached after the text when there are any: the whole slide as
it looks, then each figure and the background, each labelled with the block it
belongs to. Look at them -- you can see them; no tool is needed. Say what you
see when it matters, and never claim to see something that is not there.

Reply to what they ask. If they want the extraction changed, propose changes;
if they only ask a question, answer it and propose none. Changes you can
propose (each names blocks by their exact ids):

- edit_text: rewrite one block. `block_ids` = [id], `text` = the new text.
  For a figure this is its caption.
- change_kind: make text blocks a heading, paragraph, list_item or table.
  `block_ids`, `kind`.
- merge: join two or more text blocks into the first. `block_ids` in reading
  order; optional `text` for the merged wording, optional `kind`.
- move: move blocks after another block. `block_ids`, `after_block_id`
  ("" = to the top of the slide they are on).
- delete: remove blocks. `block_ids`.
- redraw_image: draw a figure again from a description. `block_ids` = [the
  figure's id], `instruction` = what it should show.
- edit_image: change a figure's existing picture (crop, recolour, remove or
  relabel something). `block_ids` = [the figure's id], `instruction`.
- add_image: draw a brand-new picture and add it as a figure. `after_block_id`
  = the block it goes after, `instruction` = what to draw, `text` = a short
  caption. Leave `block_ids` empty. It is marked as generated, not the
  author's own -- propose one when asked for a new or AI image.

Pictures: if the slide already has a figure the new picture should stand in
for -- a placeholder, a broken, blank or wrong picture -- use redraw_image on
that figure, so the new picture takes its place on the slide. add_image is only
for a picture the slide has no place for yet. An `instruction` describes the
picture itself (what it shows, how); never ask for the slide's title, text or
a caption to be drawn into it -- the slide shows its own text.

Rules: work on the current slide unless they ask for more. Use only ids that
appear below. Keep the source's meaning: rewrite wording when asked, but never
invent facts, numbers or names. Give every change a one-sentence `reason`.
Keep `reply` short and plain.
"""


class AgentProposal(BaseModel):
    """What the model returns: a reply, and the changes it proposes."""

    reply: str
    changes: list[BlockChange] = Field(default_factory=list)


class AgentTurn(BaseModel):
    id: str = Field(default_factory=new_identifier)
    role: Literal["person", "agent"]
    text: str
    at: str = ""
    slide_number: int = 0
    changes: list[BlockChange] = Field(default_factory=list)
    summaries: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)   # changes dropped, and why
    status: str = ""                                 # proposed | applied | discarded | undone
    looked_at: str = ""                              # the pictures the agent was shown


class AgentConversation(BaseModel):
    id: str = Field(default_factory=new_identifier)
    started_at: str = ""
    kind: str = ""  # "" for a chat; "review" for a slide-by-slide review
    turns: list[AgentTurn] = Field(default_factory=list)

    @property
    def title(self) -> str:
        if self.kind == "review":
            return "Slide-by-slide review"
        first = next((turn.text for turn in self.turns if turn.role == "person"), "")
        return (first[:60] + "…" if len(first) > 60 else first) or "New chat"


class AgentThreads(BaseModel):
    conversations: dict[str, list[AgentConversation]] = Field(default_factory=dict)
    # One running thread per file, as the first version kept them. Read once
    # and moved into `conversations`, so an earlier chat is not lost.
    threads: dict[str, list[AgentTurn]] = Field(default_factory=dict)

    def for_file(self, file_name: str) -> list[AgentConversation]:
        if file_name in self.threads:
            old = self.threads.pop(file_name)
            if old:
                self.conversations.setdefault(file_name, []).insert(0, AgentConversation(
                    started_at=old[0].at, turns=old))
        return self.conversations.setdefault(file_name, [])


class AgentThreadStore(JsonDocumentStore[AgentThreads]):
    def __init__(self, project_root) -> None:
        super().__init__(
            document_path=project_root / "extraction" / "agent.json",
            model_type=AgentThreads, build_default=AgentThreads,
            description="extraction agent conversations",
        )


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def extracted_document(project: Project, file_name: str) -> ExtractedDocument:
    document = ExtractionCollectionStore(project.root).load().document(file_name)
    if document is None:
        raise OperationFailed(f"{file_name} is not extracted yet; extract it first.")
    return document


def pick(conversations: list[AgentConversation], conversation_id: str) -> AgentConversation | None:
    """The conversation asked for, or the latest one."""
    if conversation_id:
        return next((c for c in conversations if c.id == conversation_id), None)
    return conversations[-1] if conversations else None


def view(project: Project, file_name: str, conversation: AgentConversation | None,
          conversations: list[AgentConversation]) -> dict[str, Any]:
    point = undo_point(project)
    return {
        "file_name": file_name,
        "conversation_id": conversation.id if conversation else "",
        "kind": conversation.kind if conversation else "",
        "turns": [t.model_dump(mode="json") for t in conversation.turns] if conversation else [],
        "conversations": [
            {"id": c.id, "title": c.title, "kind": c.kind, "started_at": c.started_at,
             "turn_count": len(c.turns)}
            for c in reversed(conversations)
        ],
        "undo_turn_id": point.turn_id if point.file_name == file_name else "",
    }


def read_thread(slug: str, file_name: str, conversation_id: str = "") -> dict[str, Any]:
    project = require_project(slug)
    threads = AgentThreadStore(project.root).load()
    conversations = threads.for_file(file_name)
    return view(project, file_name, pick(conversations, conversation_id), conversations)


def start_conversation(slug: str, file_name: str) -> dict[str, Any]:
    """A new, empty conversation about this file; the older ones stay in history."""
    project = require_project(slug)
    store = AgentThreadStore(project.root)
    threads = store.load()
    conversations = threads.for_file(file_name)
    if conversations and not conversations[-1].turns:
        conversation = conversations[-1]           # already an empty one: reuse it
    else:
        conversation = AgentConversation(started_at=now())
        conversations.append(conversation)
        del conversations[:-MAXIMUM_CONVERSATIONS_KEPT]
    store.save(threads)
    return view(project, file_name, conversation, conversations)


def delete_conversation(slug: str, file_name: str, conversation_id: str) -> dict[str, Any]:
    """Remove one conversation from the history. The extraction is untouched:
    changes it applied stay applied."""
    project = require_project(slug)
    store = AgentThreadStore(project.root)
    threads = store.load()
    conversations = threads.for_file(file_name)
    if not any(c.id == conversation_id for c in conversations):
        raise OperationFailed("That conversation is not in the history.")
    conversations[:] = [c for c in conversations if c.id != conversation_id]
    store.save(threads)
    return view(project, file_name, pick(conversations, ""), conversations)


# --- what the agent is shown: text -------------------------------------------------


def _block_line(block, full: bool) -> str:
    text = block.text.replace("\n", " / ")
    if not full and len(text) > 90:
        text = text[:90] + "…"
    elif len(text) > MAXIMUM_BLOCK_CHARACTERS:
        text = text[:MAXIMUM_BLOCK_CHARACTERS] + "…"
    picture = " (picture stored)" if block.asset_path else ""
    return f"- [{block.id}] {block.kind}{picture}: {text}"


def agent_context(document: ExtractedDocument, slide_number: int) -> str:
    """The current slide in full, then an index of the rest of the file."""
    on_slides = any(block.slide_number for block in document.blocks)
    lines = [f"File: {document.file_name} "
             f"({'a deck' if on_slides else 'a document'}, {len(document.blocks)} blocks)"]

    if on_slides and slide_number:
        lines.append(f"\nCurrent slide: {slide_number}")
        current = [b for b in document.blocks if b.slide_number == slide_number]
        lines += [_block_line(b, full=True) for b in current] or ["(no blocks on this slide)"]
        slide = next((s for s in document.slides if s.number == slide_number), None)
        if slide and slide.shapes:
            lines.append("Layout: " + "; ".join(
                f"{shape.kind} at {shape.left:.0%},{shape.top:.0%} "
                f"size {shape.width:.0%}x{shape.height:.0%}" for shape in slide.shapes[:20]))
        if slide and slide.background:
            background = slide.background
            lines.append(f"Background: {' to '.join(background.gradient) or background.colour} "
                         f"{'(picture)' if background.asset_path else ''}".rstrip())
        rest = [b for b in document.blocks if b.slide_number != slide_number]
    else:
        rest = document.blocks

    index, used = [], 0
    for block in rest:
        line = (f"slide {block.slide_number} " if block.slide_number else "") + \
            _block_line(block, full=not on_slides)
        used += len(line)
        if used > MAXIMUM_INDEX_CHARACTERS:
            index.append(f"... {len(rest) - len(index)} more blocks not shown")
            break
        index.append(line)
    if index:
        lines.append("\nThe rest of the file (act on these only if asked):"
                     if on_slides and slide_number else "\nBlocks:")
        lines += index
    return "\n".join(lines)


# --- asking and deciding -----------------------------------------------------------


def agent_turn(
    project: Project, document: ExtractedDocument, message: str, slide_number: int,
    history: str = "",
) -> AgentTurn:
    """Ask the model, and return its turn: the reply, and any changes it proposes
    that could apply to the file as it is now."""
    from pipeline.agent_runtime import build_system_prompt, resolve_agent
    from pipeline.llm import (
        ModelCallFailed,
        ModelNotConfigured,
        complete_structured,
        complete_structured_with_images,
    )
    from pipeline.stages import Stage

    system = build_system_prompt(resolve_agent(project, Stage.EXTRACTION)) + "\n" + GUIDE
    user = "\n\n".join(part for part in [
        agent_context(document, slide_number),
        f"--- conversation so far ---\n{history}" if history else "",
        f"--- the person says ---\n{message}",
    ] if part)

    # Shown the slide as it looks, not only described: the vision model sees
    # the pictures. If it cannot take them, the agent still answers from the
    # text, and says it could not look.
    pictures = agent_pictures(project, document, slide_number)
    looked_at, blind = looked_at_summary(pictures, slide_number), ""
    try:
        if pictures:
            try:
                proposal = complete_structured_with_images(AgentProposal, system, user, pictures)
            except ModelCallFailed as vision_failure:
                logger.warning("the agent could not be shown the pictures: %s", vision_failure)
                blind = f"I could not look at the pictures this time ({vision_failure})."
                looked_at = ""
                proposal = complete_structured(AgentProposal, system, user)
        else:
            proposal = complete_structured(AgentProposal, system, user)
    except ModelNotConfigured as not_configured:
        raise OperationFailed(str(not_configured)) from not_configured
    except ModelCallFailed as call_failure:
        raise OperationFailed(f"The agent could not answer. {call_failure}") from call_failure

    # Checked now, against the file as it is: a change that could never apply
    # is dropped with its reason rather than offered for someone to accept.
    kept, notes = [], [blind] if blind else []
    for change in proposal.changes:
        problem = check_change(document, change)
        if problem:
            notes.append(f"A proposed {change.action.replace('_', ' ')} was dropped: {problem}.")
        else:
            kept.append(change)
    return AgentTurn(
        role="agent", text=proposal.reply.strip() or "Done.", at=now(),
        slide_number=slide_number, changes=kept, notes=notes, looked_at=looked_at,
        summaries=[describe_change(document, change) for change in kept],
        status="proposed" if kept else "",
    )


def ask_extraction_agent(
    slug: str, file_name: str, message: str, slide_number: int = 0, conversation_id: str = "",
) -> dict[str, Any]:
    """Send a message; record it and the agent's reply, with any proposal."""
    project = require_project(slug)
    document = extracted_document(project, file_name)
    message = message.strip()
    if not message:
        raise OperationFailed("Say what you would like the agent to do.")

    store = AgentThreadStore(project.root)
    threads = store.load()
    conversations = threads.for_file(file_name)
    conversation = pick(conversations, conversation_id)
    if conversation is None:
        conversation = AgentConversation(started_at=now())
        conversations.append(conversation)
    turns = conversation.turns
    history = "\n".join(
        f"{'Person' if turn.role == 'person' else 'Agent'}: {turn.text}"
        + (f" [proposed {len(turn.changes)} change(s), {turn.status}]" if turn.changes else "")
        for turn in turns[-MAXIMUM_TURNS_SHOWN_TO_THE_AGENT:])

    reply = agent_turn(project, document, message, slide_number, history)
    turns.append(AgentTurn(role="person", text=message, at=now(), slide_number=slide_number))
    turns.append(reply)
    if conversation.kind != "review":  # a review keeps one answer for every slide
        del turns[:-MAXIMUM_TURNS_KEPT]
    store.save(threads)
    return view(project, file_name, conversation, conversations)
