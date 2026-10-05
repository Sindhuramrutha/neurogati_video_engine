"""The Extraction agent reviewing a file one slide at a time.

The first review had the agent read the whole extraction and report every
problem in one reply. On a real deck that reply outgrew the model's limit and
came back cut off, so the review said nothing -- and it only ever read text,
so a wrong or blank picture was invisible to it.

Here each call is one slide: the agent sees that slide drawn as a picture
beside what was extracted from it, and answers the way it answers in chat --
a short reply and, when something is wrong, changes to apply. A reply is small
whatever the size of the deck, and one slide that fails does not lose the rest.
The page walks the slides and calls this once for each.

The turns go into a conversation of their own, one per slide in slide order,
so the chat's Apply, Discard and Undo work on them unchanged.
"""

from __future__ import annotations

from typing import Any

from pipeline.core import require_project
from pipeline.extraction_agent import (
    MAXIMUM_CONVERSATIONS_KEPT,
    AgentConversation,
    AgentThreadStore,
    agent_turn,
    extracted_document,
    now,
    pick,
    view,
)

REVIEW_REQUEST = """
Review what was extracted from this slide against the slide itself. Look at the
picture of the slide, then at its blocks. Propose changes only for real
problems: text that is missing, garbled or run together; blocks in the wrong
reading order; a heading extracted as text, or the reverse; one sentence split
over several blocks; a figure that is blank, cut off or not the picture on the
slide. Do not rewrite wording that is correct, and do not add anything the
slide does not have. If the extraction matches the slide, propose nothing and
say so in a few words.
""".strip()

# A turn that is still only a proposal can be replaced by a fresh review of
# its slide; one that was applied or undone is a record of what happened.
REPLACEABLE = {"", "proposed", "discarded"}


def review_slide(
    slug: str, file_name: str, slide_number: int = 0, conversation_id: str = "",
) -> dict[str, Any]:
    """Have the agent review one slide (0: the whole of a document), and add
    its answer to the review conversation named, or to a new one."""
    project = require_project(slug)
    document = extracted_document(project, file_name)
    # The model call first, and the conversation loaded after it: the call
    # takes seconds, and a chat message saved meanwhile must not be lost.
    turn = agent_turn(project, document, REVIEW_REQUEST, slide_number)

    store = AgentThreadStore(project.root)
    threads = store.load()
    conversations = threads.for_file(file_name)
    conversation = pick(conversations, conversation_id) if conversation_id else None
    if conversation is None or conversation.kind != "review":
        conversation = AgentConversation(started_at=now(), kind="review")
        conversations.append(conversation)
        del conversations[:-MAXIMUM_CONVERSATIONS_KEPT]

    # Reviewed again, a slide's open answer is replaced rather than repeated.
    conversation.turns = [
        kept for kept in conversation.turns
        if kept.slide_number != slide_number or kept.status not in REPLACEABLE
    ] + [turn]
    conversation.turns.sort(key=lambda kept: kept.slide_number)
    store.save(threads)
    return view(project, file_name, conversation, conversations)
