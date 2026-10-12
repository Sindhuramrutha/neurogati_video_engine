"""What was asked of the Orchestrator, and what it answered.

Every ask belongs to a thread: it is written down, so closing the drawer keeps it
and the Orchestrator is told what was already said. Asking "and why is that?"
continues the conversation.

A conversation is kept per project, with the agents each answer consulted, so a
thread can be reopened later and an answer can still be traced to the agents that
produced it. Replay to the model is bounded (`MAXIMUM_HISTORY_CHARACTERS`): a
long thread sends its most recent turns, not all of them, because the context it
costs grows with every question otherwise.

Stored at `projects/<slug>/agents/conversations.json`.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

from pipeline.storage.documents import JsonDocumentStore, new_identifier

# Bounds. A chat box is the easiest place in the app to produce unbounded data,
# and the file is read whole on every ask.
MAXIMUM_CONVERSATIONS = 50
MAXIMUM_TURNS_PER_CONVERSATION = 100
MAXIMUM_QUESTION_LENGTH = 4_000
MAXIMUM_ANSWER_LENGTH = 20_000
MAXIMUM_TITLE_LENGTH = 70

# How much of a thread is replayed to the model. Enough for "and why is that?"
# to mean something, capped so a long thread cannot grow the prompt without end.
MAXIMUM_HISTORY_CHARACTERS = 6_000


def _now() -> str:
    # Milliseconds, not seconds: two questions asked in the same second are
    # ordinary, and at second resolution the list order between them is
    # arbitrary -- which reads as the list shuffling itself.
    return datetime.now(UTC).isoformat(timespec="milliseconds")


class ConversationTurn(BaseModel):
    """One question and the answer it got.

    Failed asks are not turns: a connection error is not something the
    Orchestrator said, and replaying it as if it were would teach it to answer
    that way.
    """

    id: str = Field(default_factory=new_identifier)
    asked_at: str = Field(default_factory=_now)
    question: str = ""
    answer: str = ""
    consulted: list[dict[str, Any]] = Field(default_factory=list)
    artifacts_read: list[str] = Field(default_factory=list)

    @field_validator("question")
    @classmethod
    def _cap_question(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_QUESTION_LENGTH]

    @field_validator("answer")
    @classmethod
    def _cap_answer(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_ANSWER_LENGTH]


class Conversation(BaseModel):
    id: str = Field(default_factory=new_identifier)
    title: str = ""
    started_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)
    turns: list[ConversationTurn] = Field(default_factory=list)

    @field_validator("turns")
    @classmethod
    def _cap_turns(cls, value: list[ConversationTurn]) -> list[ConversationTurn]:
        # The most recent are the ones worth keeping.
        return value[-MAXIMUM_TURNS_PER_CONVERSATION:]

    @property
    def display_title(self) -> str:
        """A name for the list. The first question, because that is what the
        person will recognise -- not "Conversation 4"."""
        if self.title.strip():
            return self.title.strip()[:MAXIMUM_TITLE_LENGTH]
        first = next((turn.question for turn in self.turns if turn.question), "")
        return first[:MAXIMUM_TITLE_LENGTH] or "New conversation"

    def summary(self) -> dict[str, Any]:
        last = self.turns[-1] if self.turns else None
        return {
            "id": self.id,
            "title": self.display_title,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
            "turn_count": len(self.turns),
            "last_answer_preview": (last.answer[:120] if last else ""),
        }

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump() | {"title": self.display_title}

    def history_for_model(self) -> str:
        """The thread so far, most recent turns first to survive the cap.

        Returned oldest-first for reading, but *trimmed* from the oldest end: if
        something has to go, it is the question from ten turns ago, not the one
        just asked.
        """
        kept: list[str] = []
        budget = MAXIMUM_HISTORY_CHARACTERS
        for turn in reversed(self.turns):
            entry = f"They asked: {turn.question}\nYou answered: {turn.answer}"
            if len(entry) > budget:
                break
            kept.append(entry)
            budget -= len(entry)
        return "\n\n".join(reversed(kept))


class ConversationLog(BaseModel):
    conversations: list[Conversation] = Field(default_factory=list)

    @field_validator("conversations")
    @classmethod
    def _cap_conversations(cls, value: list[Conversation]) -> list[Conversation]:
        return value[-MAXIMUM_CONVERSATIONS:]

    def find(self, conversation_id: str) -> Conversation | None:
        return next((c for c in self.conversations if c.id == conversation_id), None)

    def newest_first(self) -> list[Conversation]:
        """Most recently used first, with the order they were started as the
        tie-breaker, so equal timestamps never reorder the list at random."""
        ordered = sorted(
            enumerate(self.conversations),
            key=lambda pair: (pair[1].updated_at, pair[0]),
            reverse=True,
        )
        return [conversation for _, conversation in ordered]

    def record(self, conversation_id: str, turn: ConversationTurn) -> Conversation:
        """Append a turn, starting the conversation if it is new."""
        conversation = self.find(conversation_id)
        if conversation is None:
            conversation = Conversation(id=conversation_id or new_identifier())
            self.conversations.append(conversation)
        conversation.turns = [*conversation.turns, turn][-MAXIMUM_TURNS_PER_CONVERSATION:]
        conversation.updated_at = _now()
        self.conversations = self.conversations[-MAXIMUM_CONVERSATIONS:]
        return conversation


def default_conversation_log() -> ConversationLog:
    return ConversationLog()


class ConversationStore(JsonDocumentStore[ConversationLog]):
    """Persistence for the Orchestrator's conversations.

    Beside the project's agent overrides rather than under a stage, because the
    Orchestrator belongs to no stage.
    """

    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=project_root / "agents" / "conversations.json",
            model_type=ConversationLog,
            build_default=default_conversation_log,
            description="orchestrator conversations",
        )
