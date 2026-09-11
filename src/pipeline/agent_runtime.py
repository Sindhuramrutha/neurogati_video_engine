"""Running an agent — where AGENT.md stops being a document and starts working.

Until now `AGENT.md` was a surface: readable, editable, overridable per project,
and connected to nothing. This module is the connection. It loads the agent for a
stage, assembles the project state that stage is responsible for, and calls the
model.

**The instructions are the file, not the code.** v1 buried a 36 KB system prompt
inside `agents/scene_coder.py`, so changing how a stage behaved needed a
programmer and a commit. Here the system prompt *is* the AGENT.md body -- whoever
owns the material edits it in the panel, and the next run uses it. Nothing in
this module writes instructions of its own; it only supplies context and states
the output contract.

Two ways to run an agent, and the difference matters:

- `ask_stage_agent` returns prose. The agent looks at the stage and answers.
  Nothing is written. This is what the Agent panel uses, and it is safe to run
  against a project you care about.
- `draft_plan_with_agent` returns a **validated `Plan`** via structured output.
  It still writes nothing by itself -- the caller decides whether to save --
  because an agent silently replacing a plan someone spent an hour on is the
  kind of "helpful" that loses work.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from pydantic import BaseModel, Field

from pipeline.agents import Agent, AgentRegistry
from pipeline.config import REPO_ROOT
from pipeline.llm import (
    ModelCallFailed,
    ModelNotConfigured,
    complete_structured,
    complete_text,
)
from pipeline.operations import (
    OperationFailed,
    extracted_content_as_markdown,
    read_artifact,
    require_project,
    write_section_script,
)
from pipeline.planning import Plan
from pipeline.projects import Project
from pipeline.stages import BY_KEY, Stage

logger = logging.getLogger(__name__)

AGENTS_DIR = REPO_ROOT / "agents"

# Enough of an artifact for the model to reason about, small enough that a large
# project does not blow the context window on a question about one section.
MAXIMUM_CONTEXT_CHARACTERS = 12000

# The source gets a bigger budget than the artifacts: a plan invented from
# half a document is worse than a plan that costs more tokens.
MAXIMUM_SOURCE_CHARACTERS = 40000

# Narration is spoken, so a section's word budget follows from its duration.
# 150 wpm is the rate the rest of the pipeline already assumes.
WORDS_PER_SECOND_OF_SPEECH = 150 / 60


def resolve_agent(project: Project, stage: Stage) -> Agent:
    agent = AgentRegistry(AGENTS_DIR, project.root).get(stage)
    if agent is None:
        raise OperationFailed(
            f"The {stage.value} stage has no agent definition. "
            f"Stages with agents: "
            f"{', '.join(s.key.value for s in BY_KEY.values() if s.has_agent)}."
        )
    return agent


def stage_context(project: Project, stage: Stage) -> str:
    """The project state this stage is accountable for, as JSON.

    Each stage sees its own artifact and the one it consumes -- not the whole
    project. A Scripting agent asked about pacing does not need the timeline, and
    sending it costs tokens while making the relevant part harder to find.
    """
    upstream_by_stage: dict[Stage, list[str]] = {
        Stage.EXTRACTION: [],
        Stage.PLANNING: [],
        Stage.SCRIPTING: ["plan", "script"],
        Stage.STUDIO: ["script", "composition"],
        Stage.REVIEWING: ["plan", "script", "composition", "review"],
    }

    parts: list[str] = [
        f"Project: {project.name} (slug: {project.slug})",
        f"Source documents: "
        f"{', '.join(s['name'] for s in project.sources()) or 'none uploaded yet'}",
    ]

    for artifact_name in upstream_by_stage.get(stage, []):
        try:
            document = read_artifact(project.slug, artifact_name)
        except OperationFailed:
            continue
        rendered = json.dumps(document, indent=2, ensure_ascii=False)
        if len(rendered) > MAXIMUM_CONTEXT_CHARACTERS:
            rendered = rendered[:MAXIMUM_CONTEXT_CHARACTERS] + "\n... (truncated)"
        parts.append(f"\n--- {artifact_name}.json ---\n{rendered}")

    # Extraction, Planning and Scripting get the source text itself. Without it
    # the Planning agent saw only file names, which is a guarantee of invention:
    # asked to plan a video about a document it cannot read, a model writes a
    # plausible plan about the title. This is the most important block here.
    if stage in (Stage.EXTRACTION, Stage.PLANNING, Stage.SCRIPTING):
        source_text = extracted_content_as_markdown(project)
        if source_text:
            if len(source_text) > MAXIMUM_SOURCE_CHARACTERS:
                source_text = (
                    source_text[:MAXIMUM_SOURCE_CHARACTERS]
                    + "\n\n... (source truncated; use only what is shown above)"
                )
            parts.append(f"\n--- extracted source material ---\n{source_text}")
        else:
            parts.append(
                "\nNo source material has been extracted yet. Say so rather than "
                "working from the project name."
            )

    if stage is Stage.PLANNING:
        parts.append("\nThe current plan is below; propose changes against it.")
        try:
            parts.append(json.dumps(read_artifact(project.slug, "plan"), indent=2))
        except OperationFailed:
            pass

    return "\n".join(parts)


def build_system_prompt(agent: Agent) -> str:
    """The agent's own file, plus the tool grant it was given.

    Naming the granted tools matters: the declaration in AGENT.md *is* the grant,
    so an agent told it has `web_search` when it does not will confidently claim
    to have checked something it could not.
    """
    granted = ", ".join(tool.name for tool in agent.tools.granted) or "none"
    return (
        f"{agent.body.strip()}\n\n"
        f"---\n"
        f"You are the {agent.name} agent for this pipeline.\n"
        f"Tools granted to you: {granted}.\n"
        f"None of them are executable in this conversation yet, so do not claim "
        f"to have used one. If a question needs a tool you cannot run, say so."
    )


def ask_stage_agent(slug: str, stage_key: str, question: str) -> dict[str, Any]:
    """Ask a stage's agent a question about the project. Writes nothing.

    Returns the answer along with which agent definition was used and where it
    came from, so an unexpected reply can be traced to the file that produced it
    rather than guessed at.
    """
    project = require_project(slug)

    try:
        stage = Stage(stage_key)
    except ValueError as unknown_stage:
        valid = ", ".join(s.key.value for s in BY_KEY.values())
        raise OperationFailed(f"No stage {stage_key!r}. Stages: {valid}.") from unknown_stage

    agent = resolve_agent(project, stage)

    try:
        answer = complete_text(
            build_system_prompt(agent),
            f"{stage_context(project, stage)}\n\n--- question ---\n{question}",
        )
    except ModelNotConfigured as not_configured:
        raise OperationFailed(str(not_configured)) from not_configured
    except ModelCallFailed as call_failure:
        # Otherwise this reaches the CLI as a traceback and the browser as a 500,
        # when the useful thing -- what the provider actually said -- is right here.
        raise OperationFailed(f"The model call failed. {call_failure}") from call_failure

    return {
        "stage": stage.value,
        "agent": agent.name,
        "agent_source": agent.source,
        "agent_path": str(agent.path),
        "question": question,
        "answer": answer,
    }


def draft_plan_with_agent(slug: str, instruction: str) -> dict[str, Any]:
    """Have the Planning agent draft a plan as a validated `Plan` object.

    **Returns a proposal; saves nothing.** The caller decides. An agent that
    overwrote a hand-built plan the moment someone asked it a question would be
    the single most destructive thing in this pipeline.

    Structured output rather than prose is the point ([ADR 0002]): the result is
    either a `Plan` that satisfies the schema, or an error raised right here.
    There is no parsing step downstream that can misread it.
    """
    project = require_project(slug)
    agent = resolve_agent(project, Stage.PLANNING)

    system_prompt = (
        f"{build_system_prompt(agent)}\n\n"
        f"Return a plan as structured data. Every section needs a title that says "
        f"what it teaches, and an estimated spoken duration in seconds -- 45 to 120 "
        f"is the usual range. Do not invent facts that are not in the material you "
        f"were given."
    )

    try:
        drafted = complete_structured(
            Plan,
            system_prompt,
            f"{stage_context(project, Stage.PLANNING)}\n\n--- instruction ---\n{instruction}",
        )
    except ModelNotConfigured as not_configured:
        raise OperationFailed(str(not_configured)) from not_configured
    except ModelCallFailed as call_failure:
        raise OperationFailed(f"The model call failed. {call_failure}") from call_failure

    return {
        "stage": Stage.PLANNING.value,
        "agent": agent.name,
        "agent_source": agent.source,
        "instruction": instruction,
        "is_saved": False,
        "note": (
            "This is a proposal. Nothing was written. Save it with "
            "`write_artifact(project, 'plan', proposed_plan)` if you want it."
        ),
        "proposed_plan": drafted.to_dict(),
    }


class DraftedNarration(BaseModel):
    """The Scripting agent's output for one section.

    A model rather than a string so the agent has to commit to a word count it
    then has to satisfy -- and so a response that is a refusal or a preamble
    fails validation here rather than being stored as narration.
    """

    narration: str = Field(min_length=1)
    word_count: int = 0


def draft_section_script_with_agent(
    slug: str, section_id: str, extra_instruction: str = ""
) -> dict[str, Any]:
    """Write narration for one plan section, and save it.

    This one *does* write, unlike `draft_plan_with_agent`, and the asymmetry is
    deliberate: a section's narration is addressed by id, so writing it replaces
    only that section and leaves every other word in the script untouched. A plan
    is a single document, and rewriting it wholesale could discard an hour of
    structuring.
    """
    project = require_project(slug)
    agent = resolve_agent(project, Stage.SCRIPTING)

    plan = read_artifact(slug, "plan")
    section = next((s for s in plan["sections"] if s["id"] == section_id), None)
    if section is None:
        listed = ", ".join(f"{s['id']} ({s['title']})" for s in plan["sections"]) or "none"
        raise OperationFailed(f"The plan has no section {section_id!r}. Sections: {listed}.")

    target_words = max(20, int(section["estimated_seconds"] * WORDS_PER_SECOND_OF_SPEECH))

    system_prompt = (
        f"{build_system_prompt(agent)}\n\n"
        f"Write the spoken narration for ONE section of the video. It is read "
        f"aloud, so write for the ear: short sentences, no bullet points, no "
        f"headings, no stage directions, no markdown. Around {target_words} words "
        f"to fill {section['estimated_seconds']} seconds. Every fact must come "
        f"from the source material provided -- do not add examples, numbers or "
        f"analogies that are not in it."
    )

    user_prompt = (
        f"{stage_context(project, Stage.SCRIPTING)}\n\n"
        f"--- write narration for this section ---\n"
        f"Title: {section['title']}\n"
        f"Summary: {section.get('summary') or '(none given)'}\n"
        f"Target: {section['estimated_seconds']} seconds, about {target_words} words.\n"
        f"{extra_instruction}"
    )

    try:
        drafted = complete_structured(DraftedNarration, system_prompt, user_prompt)
    except ModelNotConfigured as not_configured:
        raise OperationFailed(str(not_configured)) from not_configured
    except ModelCallFailed as call_failure:
        raise OperationFailed(f"The model call failed. {call_failure}") from call_failure

    script = write_section_script(slug, section_id, drafted.narration)

    return {
        "stage": Stage.SCRIPTING.value,
        "agent": agent.name,
        "section_id": section_id,
        "section_title": section["title"],
        "target_words": target_words,
        "written_words": len(drafted.narration.split()),
        "is_saved": True,
        "script": script,
    }
