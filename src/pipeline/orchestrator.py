"""The orchestrator — one agent above all the others.

Every other agent in this pipeline owns a stage and sees only that stage. That is
right for doing the work and wrong for talking to a person: it means whoever is
asking has to already know which stage owns their question, and be standing on
that tab before they ask it.

This module is the agent that answers instead. It belongs to no stage. It has the
stage agents as its instrument: it decides who to ask, asks **several of them at
once**, reads whatever artifacts it needs, and answers from what came back.

## Why a gather loop rather than tool-calling

The obvious build is OpenAI-style tool calls. It is not available here: the
structured path already had to drop to `Mode.JSON` because this provider rejects
`tool_choice: required` in thinking mode (see `llm.complete_structured`), and
building the orchestrator on a mechanism the provider is unreliable about would
make the master agent the least dependable thing in the system.

So each turn the model returns an `OrchestratorTurn` -- a validated object naming
who to consult and what to read, or the final answer. We execute it, hand back
what we found, and ask again. Same capability, over the one path this provider is
known to honour.

## What it may do

It reads and it asks. It does not write. An agent that could rewrite a plan
because someone asked it a question about pacing is a bad trade at any level of
capability, and it is a worse one for the agent that can reach every stage.
"""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from pydantic import BaseModel, Field

from pipeline.agent_runtime import AGENTS_DIR, artifact_for_agents, ask_stage_agent
from pipeline.agents import Agent, AgentRegistry
from pipeline.conversations import ConversationStore, ConversationTurn
from pipeline.llm import ModelCallFailed, ModelNotConfigured, complete_structured
from pipeline.operations import (
    ARTIFACTS,
    OperationFailed,
    extraction_freshness,
    freshness_warnings,
    read_artifact,
    require_project,
)
from pipeline.projects import Project
from pipeline.stages import STAGES

logger = logging.getLogger(__name__)

ORCHESTRATOR_FOLDER = "orchestrator"

# Two rounds of gathering, then it answers with what it has. A loop that runs
# until it is satisfied is a loop that can spend an unbounded amount of the
# user's money on one question typed into a chat box.
MAXIMUM_ROUNDS = 2

# There are five stage agents. More calls than that in a round means the model is
# repeating itself, and every entry is a paid model call.
MAXIMUM_CONSULTATIONS_PER_ROUND = 5

# Long enough for a real answer, short enough that five of them do not bury the
# orchestrator's own context.
MAXIMUM_CONSULTATION_CHARACTERS = 4000

MAXIMUM_ARTIFACT_CHARACTERS = 8000


class Consultation(BaseModel):
    """One question for one stage agent."""

    stage: str = Field(
        description="One of: extraction, scene-plan, script-staging, generation, studio, reviewing."
    )
    question: str = Field(
        description="A specific question about that stage's own work."
    )


class OrchestratorTurn(BaseModel):
    """Either a round of gathering, or the answer.

    Both are one schema rather than two calls, because the decision "do I know
    enough yet?" is the same decision as "what do I still need?" -- splitting
    them would ask the model to make it twice and let it answer differently.
    """

    reasoning: str = Field(
        default="",
        description="One line on why these agents, or why you can answer now.",
    )
    consult: list[Consultation] = Field(
        default_factory=list,
        description="Stage agents to ask. They run at the same time.",
    )
    read: list[str] = Field(
        default_factory=list,
        description="Artifacts to read whole: extraction, plan, script, composition, review.",
    )
    answer: str = Field(
        default="",
        description="The reply to the person. Leave empty while still gathering.",
    )


def resolve_orchestrator(project: Project) -> Agent:
    agent = AgentRegistry(AGENTS_DIR, project.root).get_standalone(ORCHESTRATOR_FOLDER)
    if agent is None:
        raise OperationFailed(
            f"No orchestrator agent is defined. Expected "
            f"{AGENTS_DIR / ORCHESTRATOR_FOLDER / 'AGENT.md'}."
        )
    return agent


def artifact_exists(project: Project, artifact_name: str) -> bool:
    """Whether this artifact was ever written, as opposed to defaulted.

    `read_artifact` never fails for a missing file -- the stores return an empty
    default document instead, which is right for the editors (a new project opens
    on a blank plan rather than an error) and wrong here. Asking it alone, the
    snapshot reported that a brand-new project already had a plan, a script and a
    composition, and an orchestrator told that will answer questions about
    content that does not exist.
    """
    binding = ARTIFACTS.get(artifact_name)
    if binding is None:
        return False
    return binding.store(project).document_path.exists()


def pipeline_snapshot(project: Project) -> str:
    """The whole project at a glance — every stage, not one slice of it.

    This is the difference between the orchestrator and a stage agent in one
    function: a stage agent is handed its own artifact and the one it consumes,
    while this is handed the state of all of them, so it can tell that Scripting
    is waiting on a plan that was never made.
    """
    lines = [
        f"Project: {project.name} (slug: {project.slug})",
        f"Source documents: "
        f"{', '.join(s['name'] for s in project.sources()) or 'none uploaded yet'}",
        "",
        "Stages:",
    ]

    artifact_by_stage = {binding.stage: name for name, binding in ARTIFACTS.items()}

    for spec in STAGES:
        notes = []
        if not spec.has_agent:
            notes.append("no agent (file handling only)")

        artifact_name = artifact_by_stage.get(spec.key)
        if artifact_name:
            if artifact_exists(project, artifact_name):
                document = read_artifact(project.slug, artifact_name)
                notes.append(f"{artifact_name!r} exists ({len(json.dumps(document))} bytes)")
            else:
                notes.append(f"{artifact_name!r} not produced yet")

        detail = " — ".join(notes)
        lines.append(f"  {spec.key.value}: {spec.title}{' — ' + detail if detail else ''}")

    # The one staleness the files can prove. Without it the orchestrator answers
    # from an extraction that silently leaves out a document.
    freshness = extraction_freshness(project)
    if freshness["is_stale"]:
        lines.append("")
        lines.append("Extraction is out of date:")
        lines.extend(f"  {warning}" for warning in freshness_warnings(freshness))

    # Said even when nothing is stale: files are extracted one at a time, so one
    # not extracted is a choice still to make, not a document that failed.
    if freshness["added"]:
        lines.append("")
        lines.append("Not extracted yet: " + ", ".join(freshness["added"]))

    return "\n".join(lines)


def agent_roster(project: Project) -> str:
    """Who the orchestrator can command, named with what each is for.

    Read from the same AGENT.md files the agents themselves run on, so a project
    that overrides an agent's role sees the override here too. A hardcoded list
    would drift the moment someone edited one.
    """
    registry = AgentRegistry(AGENTS_DIR, project.root)
    lines = []
    for spec in STAGES:
        if not spec.has_agent:
            continue
        agent = registry.get(spec.key)
        if agent is None:
            continue
        lines.append(f"  {spec.key.value} — {agent.name}: {agent.role}")
    return "\n".join(lines)


def build_system_prompt(agent: Agent, project: Project) -> str:
    """The orchestrator's own file, its roster, and the shape of a turn.

    Unlike `agent_runtime.build_system_prompt`, this does **not** tell the agent
    its tools are unavailable, because for this agent they are not: consulting
    and reading genuinely execute.
    """
    return (
        f"{agent.body.strip()}\n\n"
        f"---\n"
        f"You are the {agent.name}, the master agent for this pipeline. You command "
        f"these stage agents, and they answer to you:\n\n"
        f"{agent_roster(project)}\n\n"
        f"Readable artifacts: {', '.join(ARTIFACTS)}.\n\n"
        f"Your tools do run. Consulting an agent really calls it, and several "
        f"consultations in one turn really run at the same time. Never claim to "
        f"have asked someone you did not put in `consult`.\n\n"
        f"Reply every turn as the given object. While gathering, fill `consult` "
        f"and/or `read` and leave `answer` empty. When you can answer, fill "
        f"`answer` and leave the others empty. You have at most "
        f"{MAXIMUM_ROUNDS} rounds of gathering."
    )


def _consult_one(slug: str, call: Consultation) -> dict[str, Any]:
    """One stage agent, one question. Failure is reported, never raised.

    A raise here would take down the whole round: four agents answering and one
    unreachable would lose all five. The orchestrator is told which one failed
    and answers around it.
    """
    try:
        result = ask_stage_agent(slug, call.stage, call.question)
    except OperationFailed as failure:
        return {
            "stage": call.stage,
            "question": call.question,
            "agent": call.stage,
            "ok": False,
            "answer": f"(could not reach: {failure})",
        }

    answer = result["answer"]
    if len(answer) > MAXIMUM_CONSULTATION_CHARACTERS:
        answer = answer[:MAXIMUM_CONSULTATION_CHARACTERS] + "\n... (truncated)"
    return {
        "stage": call.stage,
        "question": call.question,
        "agent": result["agent"],
        "ok": True,
        "answer": answer,
    }


def run_consultations(slug: str, calls: list[Consultation]) -> list[dict[str, Any]]:
    """Every agent in a round, at the same time.

    This is the point of the orchestrator being able to command more than one
    agent: five sequential calls to a reasoning model is minutes of somebody
    watching a spinner, and the five questions do not depend on each other.
    """
    wanted = calls[:MAXIMUM_CONSULTATIONS_PER_ROUND]
    if not wanted:
        return []
    if len(wanted) == 1:
        return [_consult_one(slug, wanted[0])]

    with ThreadPoolExecutor(max_workers=len(wanted)) as pool:
        return list(pool.map(lambda call: _consult_one(slug, call), wanted))


def run_reads(slug: str, names: list[str]) -> list[dict[str, Any]]:
    """Artifacts, whole. Unknown names come back as a finding, not an exception."""
    found = []
    for name in names:
        if name not in ARTIFACTS:
            found.append({
                "artifact": name, "ok": False,
                "content": f"(no such artifact; choose from {', '.join(ARTIFACTS)})",
            })
            continue
        project = require_project(slug)
        if not artifact_exists(project, name):
            found.append({
                "artifact": name, "ok": False,
                "content": f"({name} has not been produced yet — the stage that "
                           f"makes it has not been run)",
            })
            continue

        try:
            # The artifact as agents read it -- not as the page receives it, with
            # heading lists and freshness flags filling the space.
            rendered = artifact_for_agents(project, name)
        except OperationFailed as failure:
            found.append({"artifact": name, "ok": False, "content": f"({failure})"})
            continue
        if len(rendered) > MAXIMUM_ARTIFACT_CHARACTERS:
            rendered = rendered[:MAXIMUM_ARTIFACT_CHARACTERS] + "\n... (truncated)"
        found.append({"artifact": name, "ok": True, "content": rendered})
    return found


def _render_findings(
    consultations: list[dict[str, Any]], reads: list[dict[str, Any]]
) -> str:
    parts = []
    for consultation in consultations:
        parts.append(
            f"--- {consultation['agent']} agent ({consultation['stage']}) was asked: "
            f"{consultation['question']}\n{consultation['answer']}"
        )
    for read in reads:
        parts.append(f"--- {read['artifact']}.json\n{read['content']}")
    return "\n\n".join(parts)


def list_conversations(slug: str) -> dict[str, Any]:
    """Every thread with the Orchestrator for this project, newest first."""
    project = require_project(slug)
    log = ConversationStore(project.root).load()
    return {"conversations": [c.summary() for c in log.newest_first()]}


def read_conversation(slug: str, conversation_id: str) -> dict[str, Any]:
    """One thread in full, so it can be reopened and continued."""
    project = require_project(slug)
    conversation = ConversationStore(project.root).load().find(conversation_id)
    if conversation is None:
        raise OperationFailed(f"This project has no conversation {conversation_id!r}.")
    return conversation.to_dict()


def forget_conversation(slug: str, conversation_id: str) -> dict[str, Any]:
    """Delete one thread. The artifacts it discussed are untouched."""
    project = require_project(slug)
    store = ConversationStore(project.root)
    log = store.load()
    if log.find(conversation_id) is None:
        raise OperationFailed(f"This project has no conversation {conversation_id!r}.")
    log.conversations = [c for c in log.conversations if c.id != conversation_id]
    store.save(log)
    return {"conversations": [c.summary() for c in log.newest_first()]}


def ask_the_orchestrator(
    slug: str, question: str, conversation_id: str = ""
) -> dict[str, Any]:
    """Answer a question about the project, using whichever agents it takes.

    Changes no artifact. It does append to the conversation it was asked in, so
    the thread survives closing the panel and a follow-up like "and why is that?"
    has something to refer to. Returns the answer along with every agent
    consulted and what each one said, so an answer can be traced to the agents
    that produced it rather than taken on trust.
    """
    project = require_project(slug)
    agent = resolve_orchestrator(project)

    store = ConversationStore(project.root)
    log = store.load()
    conversation = log.find(conversation_id) if conversation_id else None
    history = conversation.history_for_model() if conversation else ""

    system_prompt = build_system_prompt(agent, project)
    transcript: list[str] = [pipeline_snapshot(project)]
    if history:
        transcript.append(
            f"\n--- earlier in this conversation ---\n{history}\n"
            "(Answer the new question below. Do not repeat what you already said "
            "unless it is asked for again.)"
        )
    transcript.append(f"\n--- the person asks ---\n{question}")

    consulted: list[dict[str, Any]] = []
    artifacts_read: list[str] = []
    rounds = 0

    def finished(answer: str) -> dict[str, Any]:
        # Recorded here rather than at the call site: every way out of the loop
        # is an answer the person saw, and one that is shown but not kept would
        # break the thread the next time they ask.
        turn = ConversationTurn(
            question=question, answer=answer,
            consulted=consulted, artifacts_read=artifacts_read,
        )
        thread = log.record(conversation_id, turn)
        store.save(log)
        return {
            "agent": agent.name,
            "agent_source": agent.source,
            "agent_path": str(agent.path),
            "question": question,
            "answer": answer,
            "rounds": rounds,
            "consulted": consulted,
            "artifacts_read": artifacts_read,
            "conversation_id": thread.id,
            "conversation_title": thread.display_title,
            "turn_id": turn.id,
        }

    try:
        for round_number in range(MAXIMUM_ROUNDS + 1):
            is_final = round_number == MAXIMUM_ROUNDS
            instruction = (
                "\n\nThis is your last turn — answer now from what you have, and "
                "say plainly if something is still unknown."
                if is_final
                else "\n\nDecide: consult, read, or answer."
            )

            turn = complete_structured(
                OrchestratorTurn, system_prompt, "\n".join(transcript) + instruction
            )

            if turn.answer.strip():
                return finished(turn.answer.strip())
            if is_final:
                return finished(
                    "I could not settle this within my rounds of gathering. "
                    "Ask something narrower, or a single stage directly."
                )

            if not turn.consult and not turn.read:
                # Neither gathering nor answering: nothing would change next
                # round, so looping again only spends a call to arrive back here.
                transcript.append(
                    "\n(You asked for nothing and answered nothing. Answer now.)"
                )
                continue

            rounds += 1
            found_agents = run_consultations(slug, turn.consult)
            found_artifacts = run_reads(slug, turn.read)
            consulted.extend(found_agents)
            artifacts_read.extend(read["artifact"] for read in found_artifacts if read["ok"])

            transcript.append(
                f"\n--- what you found (round {rounds}) ---\n"
                f"{_render_findings(found_agents, found_artifacts)}"
            )

    except ModelNotConfigured as not_configured:
        raise OperationFailed(str(not_configured)) from not_configured
    except ModelCallFailed as call_failure:
        raise OperationFailed(f"The model call failed. {call_failure}") from call_failure

    raise OperationFailed("The orchestrator finished without an answer.")
