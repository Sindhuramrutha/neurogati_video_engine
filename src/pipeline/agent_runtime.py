"""Running an agent — where AGENT.md stops being a document and starts working.

`AGENT.md` is readable, editable and overridable per project; this module is what
connects it to the model. It loads the agent for a
stage, assembles the project state that stage is responsible for, and calls the
model.

**The instructions are the file, not the code.** The system prompt *is* the
AGENT.md body, so changing how a stage behaves needs no programmer -- whoever
owns the material edits it in the panel, and the next run uses it. Nothing in
this module writes instructions of its own; it only supplies context and states
the output contract.

Two ways to run an agent, and the difference matters:

- `ask_stage_agent` returns prose. The agent looks at the stage and answers.
  Nothing is written. This is what the Agent panel uses, and it is safe to run
  against a project you care about.
- Planning is a conversation (`plan_agent.py`): the agent proposes the video's
  shape, and nothing changes the plan until a person agrees to it.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from pipeline.agents import Agent, AgentRegistry
from pipeline.config import REPO_ROOT
from pipeline.extraction import ExtractionCollectionStore, ExtractionStore
from pipeline.llm import (
    ModelCallFailed,
    ModelNotConfigured,
    complete_text,
)
from pipeline.operations import (
    OperationFailed,
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

    # Files that are not in the extraction are named as such, so an agent does not
    # take a deck nobody extracted for one it failed to read. The Extraction agent
    # is asked about the collection its page shows; every other stage reads what
    # was confirmed.
    extracted_store = ExtractionCollectionStore if stage is Stage.EXTRACTION else ExtractionStore
    extracted = {d.file_name for d in extracted_store(project.root).load().documents}
    listed_sources = ", ".join(
        s["name"] if s["name"] in extracted else f"{s['name']} (not extracted)"
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
        source_text = extracted_content_as_markdown(
            project, collection=stage is Stage.EXTRACTION)
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

    Not the plan as the page receives it: that carries the extraction's full
    heading list, freshness flags and warnings, and a real twelve-section plan
    came to 23,000 characters, more than an agent reads. Every section is here.
    """
    lines = [f"Audience: {plan.audience or 'not stated'}", "Sections, in order:"]
    for number, section in enumerate(plan.sections, start=1):
        marker = "  <- this section" if section.id == marked_section_id else ""
        lines.append(f"  {number}. {section.title or 'Untitled'} "
                     f"(~{section.estimated_seconds} s){marker}")
        if section.summary:
            lines.append(f"     Summary: {section.summary}")
        if section.sources:
            lines.append("     Sources: " + "; ".join(r.label for r in section.sources))
        for scene_number, scene in enumerate(section.scenes, start=1):
            lines.append(f"     Scene {scene_number} (~{scene.seconds} s): {scene.does}")
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
        from pipeline.plan_handoff import plan_for_later_stages

        plan = plan_for_later_stages(project)
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
        f"They name your stage's work; you cannot call them in this conversation, "
        f"so do not claim to have used one. If a question needs one, say so."
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


def draft_section_script_with_agent(
    slug: str, section_id: str, extra_instruction: str = ""
) -> dict[str, Any]:
    """Write one plan section's narration, as scenes, and save it.

    This one *does* write, unlike a planning proposal, and the asymmetry is
    deliberate: a section's narration is addressed by section id, so writing it
    replaces only that section and leaves every other word in the script
    untouched. See `pipeline.script_drafting`; imported here to avoid a cycle.
    """
    from pipeline.script_drafting import draft_section

    return draft_section(slug, section_id, extra_instruction)
