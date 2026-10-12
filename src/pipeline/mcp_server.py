"""MCP server — lets an agent operate this pipeline directly.

The web app is a client of `pipeline.operations`, the CLI is another, and this is
the third. Every tool below is a thin wrapper over the same function the browser
calls, so an agent cannot reach a capability the UI lacks or skip a validation
the UI enforces. Adding a tool means exposing an existing operation, never
writing new logic here.

**Why this exists rather than "the agent can curl the API".** It can, and it did
during development. But an MCP client gets the tool list, the argument schemas
and the docstrings automatically, so a model knows what this pipeline offers
without being told -- the same reason Blender is driven through its Python API
rather than by simulating mouse clicks.

Run it with `pipeline mcp`, which speaks MCP over stdio. Point a client at it:

    {"mcpServers": {"explainer-pipeline": {
        "command": "uv",
        "args": ["run", "--directory", "<repo path>", "pipeline", "mcp"]}}}

Two deliberate limits:

- **No key is reachable through any tool.** Credentials are server-side, and
  nothing here reads them -- an agent can drive the pipeline without ever being
  in a position to exfiltrate the provider key.
- **Nothing here deletes a project.** Every tool either adds or replaces one
  artifact, all of which are recoverable by editing. Destructive operations
  should be a deliberate human act until there is an undo.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from mcp.server.mcpserver import MCPServer

from pipeline import operations
from pipeline.operations import OperationFailed

logger = logging.getLogger(__name__)

INSTRUCTIONS = """\
This pipeline turns written academic material into a narrated explainer video.

Work in stage order: Inputs (source documents) -> Extraction -> Planning ->
Scripting -> Studio -> Reviewing. Each stage reads the previous stage's artifact
and produces its own, and every artifact is a JSON document you can read and
write with these tools.

Start with `list_projects` and `describe_stages`. Read an artifact before writing
it: every response carries a `warnings` list and an `audit` object saying what is
inconsistent, and those are the fastest way to see what still needs doing.

Values are clamped rather than rejected -- an absurd duration comes back clamped
and flagged in `warnings` instead of erroring, so always read the response rather
than assuming your input was stored verbatim.
"""

server: MCPServer = MCPServer(
    name="explainer-pipeline",
    instructions=INSTRUCTIONS,
    version="0.1.0",
)


def as_tool_result(value: Any) -> str:
    """Serialise a result for the model.

    JSON rather than a formatted summary: the model is going to reason about
    section ids and millisecond offsets, and prose loses exactly those.
    """
    return json.dumps(value, indent=2, ensure_ascii=False)


def guarded(operation, *args, **kwargs) -> str:
    """Run an operation, turning a failure into readable tool output.

    An exception escaping a tool reaches the model as a stack trace, which is
    both useless to it and a way to leak filesystem paths. `OperationFailed`
    messages are written to be actionable -- they name the valid choices -- so
    passing one through as normal output lets the model correct itself and retry
    rather than giving up.
    """
    try:
        return as_tool_result(operation(*args, **kwargs))
    except OperationFailed as failure:
        return f"That did not work: {failure}"
    except Exception as unexpected:  # noqa: BLE001 -- the boundary to the model
        logger.exception("unexpected failure in MCP tool")
        return f"Unexpected error: {type(unexpected).__name__}: {unexpected}"


# --- discovery --------------------------------------------------------------


@server.tool()
def describe_stages() -> str:
    """The six pipeline stages, in order, and the artifact each one produces.

    Call this first if you have not worked with this pipeline before.
    """
    return guarded(operations.describe_stages)


@server.tool()
def list_projects() -> str:
    """Every project, with each one's per-stage status (`empty` or `ready`)."""
    return guarded(operations.list_projects)


@server.tool()
def describe_project(project: str) -> str:
    """One project: its source documents and the status of all six stages.

    Args:
        project: the project slug, as returned by `list_projects`.
    """
    return guarded(operations.describe_project, project)


@server.tool()
def create_project(name: str) -> str:
    """Start a new project. Returns it, including the slug every other tool needs.

    Args:
        name: a human-readable title, e.g. "Gradient Descent".
    """
    return guarded(operations.create_project, name)


# --- reading and writing artifacts ------------------------------------------


@server.tool()
def read_artifact(project: str, artifact: str) -> str:
    """Read one artifact, with its audit and warnings.

    Args:
        project: the project slug.
        artifact: one of "plan", "script", "composition", "review".
    """
    return guarded(operations.read_artifact, project, artifact)


@server.tool()
def write_artifact(project: str, artifact: str, document: dict[str, Any]) -> str:
    """Replace an artifact wholesale.

    Read it first and send back a modified version: this replaces the document,
    so any field you omit reverts to its default. For a single addition prefer
    `add_plan_section`, `write_section_script`, `add_clip` or `add_review_comment`.

    Args:
        project: the project slug.
        artifact: one of "plan", "script", "composition", "review".
        document: the complete artifact as a JSON object.
    """
    return guarded(operations.write_artifact, project, artifact, document)


# --- planning ---------------------------------------------------------------


@server.tool()
def add_plan_section(
    project: str, title: str, summary: str = "", estimated_seconds: int = 60
) -> str:
    """Append a section to the plan — one teaching beat of the video.

    Args:
        project: the project slug.
        title: what this section teaches, e.g. "What a gradient is".
        summary: optional note on how to approach it.
        estimated_seconds: rough spoken duration. 45-120 is typical.
    """
    return guarded(
        operations.add_plan_section, project, title, summary, estimated_seconds
    )


# --- scripting --------------------------------------------------------------


@server.tool()
def write_section_script(project: str, section_id: str, body: str) -> str:
    """Set the narration for one plan section.

    The section must already exist in the plan; call `read_artifact` with "plan"
    to get section ids. Narration is spoken aloud, so write it to be heard rather
    than read.

    Args:
        project: the project slug.
        section_id: an id from the plan's sections.
        body: the narration text.
    """
    return guarded(operations.write_section_script, project, section_id, body)


# --- studio -----------------------------------------------------------------


@server.tool()
def add_clip(
    project: str,
    track_id: str,
    kind: str = "text",
    label: str = "",
    start_ms: int = 0,
    duration_ms: int = 3000,
    text: str = "",
) -> str:
    """Place a clip on a timeline track.

    All timing is integer milliseconds from the start of the video. Read the
    composition first for track ids and to see where existing clips sit --
    overlaps are reported in `audit`, not prevented.

    Args:
        project: the project slug.
        track_id: an id from the composition's tracks.
        kind: video, image, text, shape, audio or scene.
        label: name shown on the clip in the timeline.
        start_ms: offset from the start of the video, in milliseconds.
        duration_ms: length in milliseconds.
        text: on-screen text, for a text clip.
    """
    return guarded(
        operations.add_clip, project, track_id, kind, label, start_ms, duration_ms, text
    )


# --- reviewing --------------------------------------------------------------


@server.tool()
def add_review_comment(
    project: str,
    body: str,
    author: str = "",
    at_ms: int = 0,
    routed_to_stage: str | None = None,
) -> str:
    """Leave feedback, routed to the stage that can act on it.

    Routing is the point: "the pacing is frantic" is a Scripting defect, not a
    Studio one, and fixing it in Studio treats the symptom.

    Args:
        project: the project slug.
        body: the feedback.
        author: who is saying it.
        at_ms: the timecode it refers to, in milliseconds.
        routed_to_stage: extraction, scene-plan, script-staging, generation or studio.
    """
    return guarded(
        operations.add_review_comment, project, body, author, at_ms, routed_to_stage
    )


@server.tool()
def seed_review_chapters(project: str) -> str:
    """Rebuild the review's chapters from the plan's sections and durations.

    Destructive: this replaces existing chapters, discarding hand-edited titles.

    Args:
        project: the project slug.
    """
    return guarded(operations.seed_review_chapters, project)


# --- running the stage agents -----------------------------------------------


@server.tool()
def ask_stage_agent(project: str, stage: str, question: str) -> str:
    """Ask a stage's own agent about this project. Writes nothing.

    Each stage has an AGENT.md defining its speciality and instructions, and the
    agent sees the artifacts that stage is responsible for. Useful for "is this
    plan well paced?" or "what is missing from this script?".

    Args:
        project: the project slug.
        stage: extraction, scene-plan, script-staging, generation, studio or reviewing.
        question: what to ask.
    """
    from pipeline.agent_runtime import ask_stage_agent as run

    return guarded(run, project, stage, question)


@server.tool()
def plan_say(project: str, message: str) -> str:
    """Tell the planning agent what the video should be; it answers and proposes
    the shape -- length, sections (each a run of slides), scenes per section. The
    plan is not changed until the shape is agreed with `plan_agree`.

    Args:
        project: the project slug.
        message: what you want, in your own words.
    """
    from pipeline.plan_agent import send_message

    return guarded(send_message, project, message)


@server.tool()
def plan_agree(project: str) -> str:
    """Agree to the proposed shape: it becomes the plan, and the scenes of every
    new or changed section are written (one model call per section).

    Args:
        project: the project slug.
    """
    from pipeline.plan_agent import agree

    return guarded(agree, project)


@server.tool()
def plan_discard(project: str) -> str:
    """Throw away the proposed shape. The plan itself is not touched.

    Args:
        project: the project slug.
    """
    from pipeline.plan_agent import discard_proposal

    return guarded(discard_proposal, project)


@server.tool()
def draft_section_script(project: str, section_id: str, instruction: str = "") -> str:
    """Have the Scripting agent write one plan section as scenes, and save it.

    Each scene is narration plus a brief of what is on screen. Writes, unlike
    `plan_agree`: narration is addressed by section id, so this replaces one
    section's scenes and leaves the rest of the script alone.

    Args:
        project: the project slug.
        section_id: an id from the plan's sections.
        instruction: optional extra steer, e.g. "open with a question".
    """
    from pipeline.agent_runtime import draft_section_script_with_agent

    return guarded(draft_section_script_with_agent, project, section_id, instruction)


@server.tool()
def draft_unwritten_sections(project: str, instruction: str = "") -> str:
    """Draft every plan section that has no narration yet, and save them.

    Never replaces narration that is already written.

    Args:
        project: the project slug.
        instruction: optional steer for every section.
    """
    from pipeline.script_drafting import draft_unwritten_sections as draft_all

    return guarded(draft_all, project, instruction)


@server.tool()
def list_voices() -> str:
    """Every text-to-speech provider and whether it can be used right now.

    Call this before `render_video` to pick a provider, or to find out what a
    missing one needs installed.
    """
    return guarded(operations.list_voice_providers)


@server.tool()
def render_video(project: str, voice_provider: str = "", voice: str = "") -> str:
    """Synthesise the narration and render the video file.

    Long-running: one synthesis round trip per section, then ffmpeg. Returns
    where the .mp4 and .srt landed.

    Args:
        project: the project slug.
        voice_provider: from `list_voices`; empty picks the best available.
        voice: provider-specific voice id; empty uses that provider's default.
    """
    return guarded(operations.render_video, project, voice_provider, voice)


@server.tool()
def model_status() -> str:
    """Whether an API key is configured and which model would be used.

    Call this before an agent tool if one fails: the usual cause is no key.
    Never returns the key itself.
    """
    from pipeline.llm import describe_model

    return guarded(describe_model)


def run_stdio_server() -> None:
    """Serve MCP over stdio.

    stdio, not HTTP: the client launches this as a subprocess, so there is no
    port to collide and no listening socket on the machine. That also means
    stdout belongs to the protocol -- anything printed there corrupts the stream,
    which is why every diagnostic in this module goes through `logging`.
    """
    server.run(transport="stdio")


if __name__ == "__main__":
    run_stdio_server()
