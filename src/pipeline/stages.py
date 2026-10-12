"""The pipeline stages.

One definition, used by the CLI, the API, the UI tabs, and the graph — so a stage
cannot exist in the interface but not in the pipeline.

Each stage:
  - consumes the previous stage's artifact
  - is governed by an AGENT.md the operator can edit (no code change, no redeploy)
  - produces an artifact on disk, at the path its `produces` field declares

`AGENT.md` is the important part: a stage's instructions are content, editable by
whoever owns the material, diffable when output quality shifts, versionable in git.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Stage(StrEnum):
    INPUTS = "inputs"
    EXTRACTION = "extraction"
    ASSETS = "assets"
    SCENE_PLAN = "scene-plan"
    SCRIPT_STAGING = "script-staging"
    GENERATION = "generation"
    STUDIO = "studio"
    REVIEWING = "reviewing"
    EXPORT = "export"



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
        Stage.ASSETS,
        "Assets & Design",
        "Everything the video can show, and how it should look: the extracted "
        "pictures, which of them are worth using, and the deck's own colours "
        "and fonts.",
        has_agent=True,
        produces="assets/library.json",
        color="#FFD93D",
    ),
    StageSpec(
        Stage.SCENE_PLAN,
        "Scene Plan",
        "Decide what gets taught, in what order, and how each part is shown — the "
        "sections, their objectives, and the source content each one draws on.",
        has_agent=True,
        produces="scene-plan/plan.json",
        color="#B197FC",
    ),
    StageSpec(
        Stage.SCRIPT_STAGING,
        "Script & Staging",
        "Each section as scenes: what is said, and what is on screen while it is "
        "said.",
        has_agent=True,
        produces="script-staging/script.json",
        color="#A3E635",
    ),
    StageSpec(
        Stage.GENERATION,
        "Generation",
        "Make what each scene shows: the author's own figures, a chart of the "
        "source's numbers, or a picture drawn for the brief — and how the camera "
        "moves over it.",
        has_agent=True,
        produces="generation/visuals.json",
        color="#38D89B",
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
    StageSpec(
        Stage.EXPORT,
        "Export",
        "The video and everything that travels with it: transcript, chapter "
        "marks, subtitles and a description, written as files you can hand over.",
        has_agent=True,
        produces="export/manifest.json",
        color="#4ECDC4",
    ),
)

BY_KEY: dict[Stage, StageSpec] = {s.key: s for s in STAGES}


def order(stage: Stage) -> int:
    return [s.key for s in STAGES].index(stage)


def downstream_of(stage: Stage) -> list[Stage]:
    """Stages invalidated when `stage` changes.

    Editing the Scene Plan agent makes Script & Staging, Studio and Reviewing
    stale, and leaves Inputs and Extraction alone. This is *which* stages come
    after, not whether they are out of date: that is `upstream.py`, from what each
    layer's last transfer was built from.
    """
    i = order(stage)
    return [s.key for s in STAGES[i + 1 :]]
