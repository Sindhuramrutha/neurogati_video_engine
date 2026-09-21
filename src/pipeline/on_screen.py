"""What the viewer reads, and the shape the scene is drawn as.

Script & Staging writes, for every scene, a brief: what should be on screen
while it is said. This module turns one brief into the two things a frame needs
and the pipeline had no way to produce:

- **the words** -- a headline of a few words and up to four labels, which is
  what somebody can take in while listening to something else. Never the
  narration: it is already being spoken, and printing it as well is precisely
  what made the output read as slides with a voice over them.
- **the shape** -- which of the renderers' scene kinds this material already
  has, and the nodes, values or terms that fill it, so it can be drawn as data
  and built up as it is described.

Only the kinds a renderer on this machine has actually proved it can draw are
offered. Composing a formula scene where nothing can typeset one produces a
still of a formula, which is worse than the flow that would otherwise have been
composed.

Nothing here invents content. Every label, node, number and term has to come
from the brief, the narration or the source text, and a spec that names a step
the material does not is the one failure this pipeline cannot absorb.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

# What fits on a frame beside a picture while somebody is listening. A headline
# longer than this is a sentence, and a sentence on screen is the narration
# again.
MAXIMUM_HEADLINE_LENGTH = 60
MAXIMUM_POINT_LENGTH = 48
MAXIMUM_POINTS = 4


# --- the model's answer ------------------------------------------------------------


class OnScreenPlan(BaseModel):
    """The words a scene puts on screen, and the shape it is drawn as.

    One model for every kind of scene rather than one per kind, because it is
    one answer to one question. `scene_kind` says which of the fields below
    matter; the rest stay empty, and `DiagramSpec` checks that the ones that
    matter are there before anything is drawn.
    """

    headline: str = Field(
        description="Three to seven words naming what this scene is about. Not a "
                    "sentence, and never a line of the narration."
    )
    points: list[str] = Field(
        default_factory=list,
        description="Up to four labels of at most six words each: the real terms, "
                    "values and names from the source that the viewer should see "
                    "while this is said. Empty is correct when the picture carries it.",
    )

    scene_kind: str = Field(
        default="none",
        description="Which shape this scene is, or none when it is not about a "
                    "structure at all. Choose only from the kinds listed.",
    )

    # Filled according to `scene_kind`. Every one of them must come from the
    # source: a node, a number or a step that is not in the material is the one
    # thing this must never produce.
    nodes: list[str] = Field(
        default_factory=list,
        description="The parts, in order: steps, layers, vertices, events, the two "
                    "sides of a morph, or `left|right` rows for a table. Each at "
                    "most four words, in the source's own terms.",
    )
    edges: list[list[int]] = Field(
        default_factory=list,
        description="For tree and graph only: pairs of positions in `nodes` that are "
                    "connected, as [[0,1],[0,2]]. Leave empty for a plain chain.",
    )
    labels: list[str] = Field(
        default_factory=list,
        description="Headings: the column names of a compare or a table, the two axis "
                    "names of a plot, or one note under a morph.",
    )
    values: list[float] = Field(
        default_factory=list,
        description="For bars, the stated quantities in the same order as `nodes`. "
                    "For counter, exactly two: where the number starts and ends.",
    )
    expression: str = Field(
        default="",
        description="For plot only: a function of x in Python arithmetic, using only "
                    "sin, cos, tan, exp, log, sqrt, abs, atan, tanh, pi and e -- for "
                    "example 'exp(-x*x/2)'. Only when the source states the shape.",
    )
    formula: str = Field(
        default="",
        description="For formula only: the expression as the source writes it, in "
                    "LaTeX without dollar signs.",
    )
    steps: list[str] = Field(
        default_factory=list,
        description="For formula only: the later forms it is rearranged into, in "
                    "order, each in LaTeX.",
    )
    code: str = Field(
        default="",
        description="For code only: the source's own code, at most fourteen lines.",
    )


# What each kind needs filled in, in the words the model is given. Written here
# rather than left to the field descriptions because the choice and the filling
# are one decision: picking `bars` without values produces a scene that cannot
# be drawn, and it is cheaper to say so than to find out in a subprocess.
KIND_INSTRUCTIONS: dict[str, str] = {
    "flow": "nodes: each step, in order.",
    "compare": "nodes: the points being compared; labels: what each column is.",
    "stack": "nodes: the layers, topmost first.",
    "cycle": "nodes: the stages of the loop, in order.",
    "tree": "nodes: the root first, then the rest; edges: [parent, child] pairs.",
    "graph": "nodes: the things; edges: which pairs are connected.",
    "plot": "expression: the curve as a function of x; labels: [x axis, y axis].",
    "bars": "values: the stated quantities; nodes: what each one measures.",
    "timeline": "nodes: the events, each beginning with its date, in order.",
    "table": "nodes: rows written as 'left|right'; labels: the column headings.",
    "counter": "values: [where the number starts, where it ends]; nodes: [what it "
               "counts].",
    "formula": "formula: the expression; steps: the forms it becomes.",
    "code": "code: the source's own code.",
    "morph": "nodes: exactly two -- what it was, and what it becomes; labels: one "
             "note, if the change needs one.",
}

ON_SCREEN_RULES = (
    "You decide what is on screen while one scene of narration is spoken.\n\n"
    "The narration is already being heard. Never put it on screen: printing the "
    "spoken words is what makes a video read as slides with a voice over them, "
    "and a viewer who is reading has stopped listening.\n\n"
    "Give a headline of three to seven words, and up to four short labels -- the "
    "real terms, values and names the scene turns on. Take every one of them from "
    "the brief, the narration or the source text. Never invent a number, a label "
    "or a step.\n\n"
    "Then say what shape the scene is, so it can be drawn and built up as it is "
    "described. Pick the shape the material already has -- not the most "
    "impressive one. A scene that is a definition, an argument or an aside has no "
    "shape: say none, because a diagram of something unstructured is decoration, "
    "and decoration is what this stage exists to avoid."
)


def _scene_kind_rules(kinds: dict[str, str]) -> str:
    """The kinds this machine can actually draw, and what each one needs.

    Only what is installed and has passed its own probe. Offering a formula
    scene on a machine that cannot typeset one produces a still of a formula --
    worse than the flow it would otherwise have composed.
    """
    if not kinds:
        return ("\n\nNothing here can animate a scene, so set scene_kind to none "
                "and give only the headline and labels.")
    lines = [
        f"- {kind}: {describes}. Fill {KIND_INSTRUCTIONS.get(kind, 'nodes')}"
        for kind, describes in kinds.items()
    ]
    return ("\n\nThe shapes available for this video, and what each one needs:\n"
            + "\n".join(lines)
            + "\n- none: this scene is not about a structure.")


def compose_on_screen(
    section_title: str, brief: str, narration: str, source_text: str,
    kinds: dict[str, str] | None = None,
):
    """Ask for the scene's on-screen words and shape. Returns an `OnScreenPlan`."""
    from pipeline.llm import complete_structured

    user_prompt = "\n\n".join(part for part in [
        f"Section: {section_title}" if section_title else "",
        f"What this scene shows, as the script asked for it: {brief}" if brief else "",
        f"What is said while it is on screen: {narration[:600]}" if narration else "",
        f"Source material for this section:\n{source_text[:1200]}" if source_text else "",
    ] if part)
    return complete_structured(
        OnScreenPlan,
        ON_SCREEN_RULES + _scene_kind_rules(kinds or {}),
        user_prompt,
        max_tokens=4_000,
    )


def spec_from_plan(composed: OnScreenPlan, headline: str, kinds: dict[str, str]):
    """The composed scene as a drawable spec, or None.

    None whenever the kind is not one this machine can draw or the fields that
    kind needs are not there -- checked here, before a subprocess is started for
    a scene that could never have worked.
    """
    from pipeline.scene_renderers import DiagramSpec

    kind = (composed.scene_kind or "none").strip().lower()
    if kind in {"", "none"} or kind not in kinds:
        return None
    return DiagramSpec.from_dict({
        "kind": kind,
        "caption": headline,
        "nodes": composed.nodes,
        "edges": composed.edges,
        "labels": composed.labels,
        "values": composed.values,
        "expression": composed.expression,
        "formula": composed.formula,
        "steps": composed.steps,
        "code": composed.code,
    })


def fallback_headline(brief: str, narration: str) -> str:
    """Something honest to show when no model composed the scene.

    The first clause of the brief, which the script already wrote as a
    description of what is on screen -- not the narration, which is the one
    thing that must not be printed.
    """
    source = (brief or narration).strip()
    for separator in (":", " -- ", ". ", ";"):
        if separator in source:
            source = source.split(separator)[0]
            break
    return " ".join(source.split()[:7])[:MAXIMUM_HEADLINE_LENGTH]


def draw_diagram(spec, path: Path, style=None) -> None:
    """The diagram as a still, drawn deterministically.

    Every machine can draw this; only some can animate it. A project without an
    animation backend shows the same nodes in the same order, held rather than
    built -- which is a smaller loss than a picture of a diagram that nobody can
    check.
    """
    from PIL import Image, ImageDraw

    from pipeline.rendering import DEFAULT_STYLE, FRAME_HEIGHT, FRAME_WIDTH, _load_font

    style = style or DEFAULT_STYLE
    image = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), style.background_colour)
    draw = ImageDraw.Draw(image)
    nodes = list(spec.nodes)[:6]
    if not nodes:
        return

    stacked = spec.kind == "stack"
    box_font = _load_font(34, family=style.body_font)
    if spec.caption:
        draw.text((120, 90), spec.caption[:70],
                  font=_load_font(38, bold=True, family=style.heading_font),
                  fill=style.text_colour)

    if stacked:
        height = min(150, (FRAME_HEIGHT - 400) // len(nodes))
        width = 700
        for index, label in enumerate(nodes):
            top = 260 + index * (height + 24)
            box = [(FRAME_WIDTH // 2 - width // 2, top),
                   (FRAME_WIDTH // 2 + width // 2, top + height)]
            draw.rounded_rectangle(box, radius=16, outline=style.accent_colour, width=5)
            draw.text((box[0][0] + 28, top + height // 2 - 20), label[:28],
                      font=box_font, fill=style.text_colour)
        return

    width = min(360, (FRAME_WIDTH - 260) // len(nodes) - 40)
    height = 170
    top = FRAME_HEIGHT // 2 - height // 2
    gap = (FRAME_WIDTH - 200 - width * len(nodes)) // max(1, len(nodes) - 1) \
        if len(nodes) > 1 else 0
    for index, label in enumerate(nodes):
        left = 100 + index * (width + gap)
        draw.rounded_rectangle([(left, top), (left + width, top + height)],
                               radius=16, outline=style.accent_colour, width=5)
        words = label[:26]
        draw.text((left + 24, top + height // 2 - 18), words, font=box_font,
                  fill=style.text_colour)
        if index and spec.kind in {"flow", "cycle"}:
            arrow_y = top + height // 2
            start = left - gap + 10
            draw.line([(start, arrow_y), (left - 12, arrow_y)],
                      fill=style.accent_colour, width=6)
            draw.polygon([(left - 12, arrow_y), (left - 30, arrow_y - 12),
                          (left - 30, arrow_y + 12)], fill=style.accent_colour)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
