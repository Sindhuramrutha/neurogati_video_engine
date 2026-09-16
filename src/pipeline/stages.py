"""The six pipeline stages.

One definition, used by the CLI, the API, the UI tabs, and the graph — so a stage
cannot exist in the interface but not in the pipeline, which is exactly how v1's
`workflow.py` and `run_chapter.py` drifted apart.

Each stage:
  - consumes the previous stage's artifact
  - is governed by an AGENT.md the operator can edit (no code change, no redeploy)
  - produces an artifact on disk, at the path its `produces` field declares

`AGENT.md` is the important part. v1 buried a 36 KB system prompt inside
agents/scene_coder.py, where only a programmer could change how a stage behaved
and every tweak was a commit. Skills move that into content: editable by whoever
owns the material, diffable when output quality shifts, versionable in git.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Stage(StrEnum):
    INPUTS = "inputs"
    EXTRACTION = "extraction"
    PLANNING = "planning"
    SCRIPTING = "scripting"
    STUDIO = "studio"
    REVIEWING = "reviewing"


@dataclass(frozen=True)
class StageSpec:
    key: Stage
    title: str
    blurb: str
    # Every stage but Inputs is run by an agent with its own AGENT.md: a
    # speciality, an instruction set, and a declared set of tools it may operate.
    # Inputs is file handling -- there is nothing to steer.
    has_agent: bool
    produces: str
    # Every stage carries its own colour, Inputs included: a neutral stage reads
    # as a disabled one, and the rail should show six places, not five plus a
    # waiting room.
    color: str


STAGES: tuple[StageSpec, ...] = (
    StageSpec(
        Stage.INPUTS,
        "Inputs",
        "Source documents for this project — PDF, MD, PPTX, DOCX.",
        has_agent=False,
        produces="sources/",
        color="#4D96FF",
    ),
    StageSpec(
        Stage.EXTRACTION,
        "Extraction",
        "Agent that pulls structured content out of the sources: headings, prose, "
        "code, tables, figures — losing nothing, inventing nothing.",
        has_agent=True,
        produces="extraction/content.json",
        color="#4ECDC4",
    ),
    StageSpec(
        Stage.PLANNING,
        "Planning",
        "Decide what gets taught, in what order, and which tool renders each part "
        "— dynamic tool calling, not a fixed renderer.",
        has_agent=True,
        produces="planning/plan.json",
        color="#B197FC",
    ),
    StageSpec(
        Stage.SCRIPTING,
        "Scripting",
        "Plan to scenarios to scenes: narration and a per-scene brief.",
        has_agent=True,
        produces="scripting/script.json",
        color="#A3E635",
    ),
    StageSpec(
        Stage.STUDIO,
        "Studio",
        # Named Studio rather than Graphics because the stage is not only about
        # imagery: it owns the media library, the multi-track timeline, layer
        # properties and effects, preview renders and final output. "Graphics"
        # described one of its panels.
        "Compose the video: media, timeline, layers, effects and rendering — with "
        "an agent that can build and edit alongside you.",
        has_agent=True,
        produces="studio/composition.json",
        color="#FF8A5B",
    ),
    StageSpec(
        Stage.REVIEWING,
        "Reviewing",
        "Mechanical checks, then human judgement. Feedback returns to any earlier stage.",
        has_agent=True,
        produces="reviewing/review.json",
        color="#FF6B9D",
    ),
)

BY_KEY: dict[Stage, StageSpec] = {s.key: s for s in STAGES}


def order(stage: Stage) -> int:
    return [s.key for s in STAGES].index(stage)


def downstream_of(stage: Stage) -> list[Stage]:
    """Stages invalidated when `stage` changes.

    Editing the Planning agent makes scripting, studio and reviewing stale, and
    leaves inputs and extraction alone.

    This computes *which* stages go stale, not *whether* they have. Answering
    that needs content hashes of each stage's artifact, which nothing records
    yet -- see docs/design/data-layout.md#the-manifest--incremental-rebuild for
    the design and docs/open-questions.md for why it waits on stage execution.
    """
    i = order(stage)
    return [s.key for s in STAGES[i + 1 :]]
