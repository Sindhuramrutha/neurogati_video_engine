"""Tool and resource catalogue — what agents can actually operate.

An AGENT.md declares which of these its agent may use. That declaration is the
grant: an agent cannot reach a tool it has not been given, so capability is
inspectable in one markdown file rather than buried in code.

Most of these do not execute yet: they are the contract the stages will implement
against, and the thing the UI reads to show what each agent can do. The
orchestration tools at the bottom are the exception -- those run, which is why
the orchestrator is told it may actually use them and the stage agents are told
they may not.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ToolKind(StrEnum):
    READ = "read"        # inspects existing artifacts
    DELEGATE = "delegate"  # puts another agent to work and reads its answer
    WRITE = "write"      # produces or edits an artifact
    FETCH = "fetch"      # reaches outside the project
    MEASURE = "measure"  # returns facts about something built
    RENDER = "render"    # produces media


@dataclass(frozen=True)
class Tool:
    name: str
    kind: ToolKind
    summary: str
    # Fetch tools name the resources they draw on, so "where did this asset come
    # from?" is answerable from the agent definition alone.
    resources: tuple[str, ...] = ()


@dataclass(frozen=True)
class Resource:
    name: str
    kind: str          # "library" | "api" | "site"
    summary: str
    licence: str
    requires_key: bool = False


# --- resources ---------------------------------------------------------------
# Deliberately conservative. Everything here is licence-clear, because a
# generated video that ships someone else's copyrighted image is a real problem
# and the agent will not be the one to notice.

RESOURCES: tuple[Resource, ...] = (
    Resource("asset-library", "library",
             "Project and shared assets: registered icons, figures, previously "
             "generated images.", "owned"),
    Resource("openverse", "api",
             "Openly licensed images aggregated across sources.", "CC / public domain"),
    Resource("wikimedia-commons", "api",
             "Freely licensed media, strong for scientific and anatomical figures.",
             "CC / public domain"),
    Resource("bootstrap-icons", "library",
             "Flat vector icons for recognisable objects.", "MIT"),
    Resource("openmoji", "library",
             "Flat emoji-style pictograms.", "CC BY-SA 4.0"),
    Resource("image-generation", "api",
             "Generate an image from a description when nothing suitable exists.",
             "generated", requires_key=True),
    Resource("web-search", "api",
             "Look up reference material to ground a plan.",
             "reference only", requires_key=True),
)

RESOURCES_BY_NAME = {r.name: r for r in RESOURCES}


# --- tools -------------------------------------------------------------------

TOOLS: tuple[Tool, ...] = (
    # extraction
    Tool("read_source", ToolKind.READ, "Read a source document (PDF/DOCX/PPTX/MD)."),
    Tool("extract_structure", ToolKind.WRITE,
         "Produce headings, prose, code blocks, tables and figure references."),
    Tool("extract_figures", ToolKind.WRITE,
         "Pull embedded images out of a source and register them as assets."),
    Tool("ocr_page", ToolKind.READ, "Read text off a page image when there is no text layer."),

    # planning
    Tool("read_extraction", ToolKind.READ, "Read the extracted content."),
    Tool("web_search", ToolKind.FETCH,
         "Look up reference material to check an understanding. Never a source of "
         "facts for narration.", ("web-search",)),
    Tool("choose_renderer", ToolKind.WRITE,
         "Assign a rendering approach per segment -- dynamic tool calling."),
    Tool("estimate_duration", ToolKind.MEASURE, "Estimate spoken length of planned content."),

    # scripting
    Tool("read_plan", ToolKind.READ, "Read the teaching plan."),
    Tool("write_scenes", ToolKind.WRITE, "Write narration and per-scene beats."),
    Tool("synthesize_speech", ToolKind.RENDER, "Produce narration audio."),
    Tool("align_words", ToolKind.MEASURE, "Word-level timings from narration audio."),
    Tool("check_fidelity", ToolKind.MEASURE,
         "Verify every claim in narration traces to the source."),

    # assets & design
    Tool("inspect_image", ToolKind.MEASURE,
         "Open a stored picture and measure it: size, proportions, whether it is blank."),
    Tool("describe_image", ToolKind.READ,
         "Say what a picture shows, to judge whether it carries information the "
         "words do not."),
    Tool("choose_look", ToolKind.WRITE,
         "Set whether the video follows the source deck's colours and fonts."),

    # export
    Tool("read_review", ToolKind.READ, "Read the review: comments, chapters and versions."),
    Tool("read_composition", ToolKind.READ, "Read the Studio timeline."),
    Tool("read_script", ToolKind.READ, "Read the narration, scene by scene."),
    Tool("write_export", ToolKind.WRITE,
         "Write the transcript, chapter marks and description beside the video."),

    # studio
    Tool("search_asset_library", ToolKind.READ,
         "Find an existing asset before making a new one.", ("asset-library",)),
    Tool("fetch_external_asset", ToolKind.FETCH,
         "Retrieve a licence-clear image or icon from an approved source.",
         ("openverse", "wikimedia-commons", "bootstrap-icons", "openmoji")),
    Tool("generate_image", ToolKind.FETCH,
         "Generate an image when nothing suitable exists.", ("image-generation",)),
    Tool("register_asset", ToolKind.WRITE,
         "Add an asset to the library with its source and licence recorded.",
         ("asset-library",)),
    Tool("compose_scene", ToolKind.WRITE, "Lay out a scene on the timeline."),
    Tool("measure_layout", ToolKind.MEASURE,
         "Bounding boxes, overlaps and frame fit for a built scene."),
    Tool("render_scene", ToolKind.RENDER, "Render a scene to video."),
    Tool("edit_timeline", ToolKind.WRITE,
         "Move, trim, retime or restack clips, assets and captions."),

    # reviewing
    Tool("run_checks", ToolKind.MEASURE, "Run the mechanical check suite over a scene."),
    Tool("extract_frames", ToolKind.READ, "Sample frames from a rendered clip."),
    Tool("compare_to_source", ToolKind.MEASURE,
         "Diff every on-screen string against the source document."),
    Tool("route_feedback", ToolKind.WRITE,
         "Send feedback to the earliest stage that could have prevented the defect."),

    # orchestration -- the only tools here that actually run
    Tool("consult_agents", ToolKind.DELEGATE,
         "Put a question to one or more stage agents at once and collect their "
         "answers."),
    Tool("read_artifact", ToolKind.READ,
         "Read any stage's artifact whole, across the whole pipeline."),
    Tool("inspect_pipeline", ToolKind.READ,
         "Which stages have produced something, and what the project contains."),
)

TOOLS_BY_NAME = {t.name: t for t in TOOLS}


@dataclass
class ToolGrant:
    """Resolved capability for one agent: what it declared, and what actually exists."""

    granted: list[Tool] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)

    @property
    def resources(self) -> list[Resource]:
        names: list[str] = []
        for tool in self.granted:
            for r in tool.resources:
                if r not in names:
                    names.append(r)
        return [RESOURCES_BY_NAME[n] for n in names if n in RESOURCES_BY_NAME]


def resolve(names: list[str]) -> ToolGrant:
    """Unknown names are reported, not silently dropped.

    A typo in an AGENT.md would otherwise quietly remove a capability, and the
    symptom -- an agent that stops doing something it used to -- is hard to trace
    back to a misspelling.
    """
    grant = ToolGrant()
    for n in names:
        tool = TOOLS_BY_NAME.get(n)
        if tool:
            grant.granted.append(tool)
        else:
            grant.unknown.append(n)
    return grant
