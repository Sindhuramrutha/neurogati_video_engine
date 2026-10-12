"""Routes for the Extraction agent's conversation: ask, apply, discard, undo.

A module of its own so `routes_project.py` does not grow. Thin like the rest:
the work is in `pipeline.extraction_agent`.
"""

from __future__ import annotations

from typing import Any

from litestar import delete, get, post
from litestar.exceptions import ClientException
from litestar.params import FromPath
from pydantic import BaseModel

from pipeline.core import OperationFailed
from pipeline.extraction_agent import (
    ask_extraction_agent,
    delete_conversation,
    read_thread,
    start_conversation,
)
from pipeline.extraction_agent_decisions import (
    apply_proposal,
    discard_proposal,
    undo_agent_changes,
)
from pipeline.extraction_slide_review import review_slide


class AgentMessage(BaseModel):
    file_name: str
    message: str
    slide_number: int = 0     # the slide on screen, 1-based; 0 for a document
    conversation_id: str = ""  # "" continues the latest conversation


class AgentFile(BaseModel):
    file_name: str


class ProposalToApply(AgentFile):
    continues: str = ""    # "apply all": the batch's ids so far, so one Undo undoes all


class SlideToReview(BaseModel):
    file_name: str
    slide_number: int = 0     # 1-based; 0 reviews a document as a whole
    conversation_id: str = ""  # the review under way; "" starts one


def _client_error(call, *args) -> dict[str, Any]:
    try:
        return call(*args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/extraction/agent", sync_to_thread=False)
def get_extraction_agent_thread(
    slug: FromPath[str], file_name: str, conversation_id: str = "",
) -> dict[str, Any]:
    """One conversation about a file -- the latest unless another is named -- and
    the list of all of them."""
    return _client_error(read_thread, slug, file_name, conversation_id)


@post("/api/projects/{slug:str}/extraction/agent/new", sync_to_thread=False)
def start_extraction_agent_conversation(slug: FromPath[str], data: AgentFile) -> dict[str, Any]:
    """Start a new conversation; earlier ones stay in the history."""
    return _client_error(start_conversation, slug, data.file_name)


@delete("/api/projects/{slug:str}/extraction/agent/conversations/{conversation_id:str}",
        status_code=200, sync_to_thread=False)
def delete_extraction_agent_conversation(
    slug: FromPath[str], conversation_id: FromPath[str], file_name: str,
) -> dict[str, Any]:
    """Remove one conversation from the history; the extraction is untouched."""
    return _client_error(delete_conversation, slug, file_name, conversation_id)


@post("/api/projects/{slug:str}/extraction/agent", sync_to_thread=True)
def ask_extraction_agent_route(slug: FromPath[str], data: AgentMessage) -> dict[str, Any]:
    """Send a message; the reply may carry proposed changes. Threaded: a model call."""
    return _client_error(
        ask_extraction_agent, slug, data.file_name, data.message, data.slide_number,
        data.conversation_id)


@post("/api/projects/{slug:str}/extraction/agent/review-slide", sync_to_thread=True)
def review_extraction_slide(slug: FromPath[str], data: SlideToReview) -> dict[str, Any]:
    """The agent reviews one slide against its extraction. Threaded: a model call."""
    return _client_error(
        review_slide, slug, data.file_name, data.slide_number, data.conversation_id)


@post("/api/projects/{slug:str}/extraction/agent/{turn_id:str}/apply", sync_to_thread=True)
def apply_extraction_agent_proposal(
    slug: FromPath[str], turn_id: FromPath[str], data: ProposalToApply,
) -> dict[str, Any]:
    """Apply a proposal. Threaded: a picture change calls the image model."""
    return _client_error(apply_proposal, slug, data.file_name, turn_id, data.continues)


@post("/api/projects/{slug:str}/extraction/agent/{turn_id:str}/discard", sync_to_thread=False)
def discard_extraction_agent_proposal(
    slug: FromPath[str], turn_id: FromPath[str], data: AgentFile,
) -> dict[str, Any]:
    return _client_error(discard_proposal, slug, data.file_name, turn_id)


@post("/api/projects/{slug:str}/extraction/agent/undo", sync_to_thread=True)
def undo_extraction_agent_changes(slug: FromPath[str], data: AgentFile) -> dict[str, Any]:
    """Put back what the last applied proposal changed."""
    return _client_error(undo_agent_changes, slug, data.file_name)


EXTRACTION_AGENT_ROUTES = [
    get_extraction_agent_thread,
    start_extraction_agent_conversation,
    delete_extraction_agent_conversation,
    ask_extraction_agent_route,
    review_extraction_slide,
    apply_extraction_agent_proposal,
    discard_extraction_agent_proposal,
    undo_extraction_agent_changes,
]
