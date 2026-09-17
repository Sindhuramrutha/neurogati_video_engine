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

from pipeline.agents import Agent, AgentRegistry
from pipeline.config import REPO_ROOT
from pipeline.extraction import ExtractionStore
from pipeline.llm import (
    ModelCallFailed,
    ModelNotConfigured,
    complete_text,
)
from pipeline.operations import (
    OperationFailed,
    excluded_sources,
    extracted_content_as_markdown,
    require_project,
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


def stage_context(project: Project, stage: Stage, include_source: bool = True) -> str:
    """The project state this stage is accountable for, as JSON.

    Each stage sees its own artifact and the one it consumes -- not the whole
    project. A Scripting agent asked about pacing does not need the timeline, and
    sending it costs tokens while making the relevant part harder to find.
    """
    upstream_by_stage: dict[Stage, list[str]] = {
        Stage.EXTRACTION: [],
        Stage.SCENE_PLAN: [],
        Stage.SCRIPT_STAGING: ["plan", "script"],
        Stage.STUDIO: ["script", "composition"],
        Stage.REVIEWING: ["plan", "script", "composition", "review"],
    }

    # Files left out of extraction are named as such. Listed plainly, a stage
    # agent reported an unticked deck as a document that "was never extracted".
    left_out = set(excluded_sources(project))
    listed_sources = ", ".join(
        f"{s['name']} (left out of extraction by choice)" if s["name"] in left_out
        else s["name"]
        for s in project.sources()
    )
    parts: list[str] = [
        f"Project: {project.name} (slug: {project.slug})",
        f"Source documents: {listed_sources or 'none uploaded yet'}",
    ]

    for artifact_name in upstream_by_stage.get(stage, []):
        parts.append(f"\n--- {artifact_name} ---\n{artifact_for_agents(project, artifact_name)}")

    # Extraction, Planning and Scripting get the source text itself. Without it
    # the Planning agent saw only file names, which is a guarantee of invention:
    # asked to plan a video about a document it cannot read, a model writes a
    # plausible plan about the title. This is the most important block here.
    if include_source and stage in (Stage.EXTRACTION, Stage.SCENE_PLAN, Stage.SCRIPT_STAGING):
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

    if stage is Stage.SCENE_PLAN:
        parts.append("\nThe current plan is below; propose changes against it.")
        parts.append(artifact_for_agents(project, "plan"))

    return "\n".join(parts)


# --- artifacts, as an agent reads them ----------------------------------------

# A compact plan is small -- a twelve-section plan is a few thousand characters --
# so this only bounds the pathological case.
MAXIMUM_PLAN_CHARACTERS_FOR_AGENTS = 30_000


def _capped(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit] + "\n... (truncated)"


def compact_plan_text(plan: Plan, marked_section_id: str | None = None) -> str:
    """The plan as an agent needs it: every section, in order, and nothing else.

    Agents used to be handed the plan exactly as the page receives it -- with the
    extraction's full heading list, freshness flags and warnings -- then cut at
    12,000 characters. A real twelve-section plan came to 23,000, so the Scripting
    agent could see only ten of its sections.
    """
    numbers = {o.id: n for n, o in enumerate(plan.learning_objectives, start=1)}
    lines = [f"Audience: {plan.selected_audience or 'not chosen'}"]
    if plan.learning_objectives:
        lines.append("Learning objectives:")
        lines.extend(f"  {numbers[o.id]}. {o.text}" for o in plan.learning_objectives
                     if o.is_included)
    if plan.key_themes:
        lines.append(f"Key themes: {'; '.join(plan.key_themes)}")
    lines.append("Sections, in order:")
    for number, section in enumerate(plan.sections, start=1):
        marker = "  <- this section" if section.id == marked_section_id else ""
        lines.append(f"  {number}. {section.title or 'Untitled'} "
                     f"(~{section.estimated_seconds} s){marker}")
        if section.summary:
            lines.append(f"     Summary: {section.summary}")
        if section.rendering_approach:
            lines.append(f"     Shown as: {section.rendering_approach}"
                         f"{' -- ' + section.rendering_reason if section.rendering_reason else ''}")
        if section.sources:
            lines.append("     Sources: " + "; ".join(r.label for r in section.sources))
        served = [str(numbers[oid]) for oid in section.objective_ids if oid in numbers]
        if served:
            lines.append(f"     Objectives: {', '.join(served)}")
    return _capped("\n".join(lines), MAXIMUM_PLAN_CHARACTERS_FOR_AGENTS)


def artifact_for_agents(project: Project, artifact_name: str) -> str:
    """One artifact as text an agent reads, without anything only the page needs."""
    from pipeline.composition import CompositionStore
    from pipeline.planning import PlanStore
    from pipeline.review import ReviewStore
    from pipeline.scripting import ScriptStore

    if artifact_name == "plan":
        return compact_plan_text(PlanStore(project.root).load())

    if artifact_name == "script":
        plan = PlanStore(project.root).load()
        script = ScriptStore(project.root).load()
        lines = []
        for number, section in enumerate(plan.sections, start=1):
            spoken = script.spoken_text(section.id)
            lines.append(f"{number}. {section.title} -- "
                         f"{len(spoken.split())} words" if spoken else
                         f"{number}. {section.title} -- not written yet")
            if spoken:
                lines.append(spoken)
        return _capped("\n".join(lines), MAXIMUM_CONTEXT_CHARACTERS)

    if artifact_name == "extraction":
        return _capped(ExtractionStore(project.root).load().as_markdown(),
                       MAXIMUM_CONTEXT_CHARACTERS)

    stores = {"composition": CompositionStore, "review": ReviewStore}
    if artifact_name in stores:
        document = stores[artifact_name](project.root).load().model_dump(mode="json")
        return _capped(json.dumps(document, indent=2, ensure_ascii=False),
                       MAXIMUM_CONTEXT_CHARACTERS)

    raise OperationFailed(f"No artifact {artifact_name!r}.")


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

    **Never changes the plan.** The proposal is kept as a pending draft for
    someone to accept or discard. An agent that overwrote a hand-built plan the
    moment someone asked it a question would be the single most destructive thing
    in this pipeline.

    Structured output rather than prose is the point ([ADR 0002]): the result is
    either a `Plan` that satisfies the schema, or an error raised right here.
    There is no parsing step downstream that can misread it.
    """
    # Drafting reads the whole extraction in two passes -- every heading first,
    # then each section from its own text -- instead of the first 40,000
    # characters, which left the end of a long source out of every plan. See
    # `pipeline.plan_drafting`. Imported here to avoid a cycle: that module is
    # built on this one.
    from pipeline.plan_drafting import draft_plan

    draft = draft_plan(slug, instruction)
    return draft | {
        "stage": Stage.SCENE_PLAN.value,
        "is_saved": False,
        "note": (
            "Kept as a pending draft; the plan was not changed. Accept it whole or by "
            "section with `accept_plan_draft`, or discard it with `discard_plan_draft`."
        ),
        "proposed_plan": draft.get("plan", {}),
    }


def draft_section_script_with_agent(
    slug: str, section_id: str, extra_instruction: str = ""
) -> dict[str, Any]:
    """Write one plan section's narration, as scenes, and save it.

    This one *does* write, unlike `draft_plan_with_agent`, and the asymmetry is
    deliberate: a section's narration is addressed by section id, so writing it
    replaces only that section and leaves every other word in the script
    untouched. See `pipeline.script_drafting`; imported here to avoid a cycle.
    """
    from pipeline.script_drafting import draft_section

    return draft_section(slug, section_id, extra_instruction)
