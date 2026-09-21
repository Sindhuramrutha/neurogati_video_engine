"""The scene repertoire, drawn with Manim.

Run as a subprocess, reading one spec as JSON on stdin. Not imported: Manim
configures itself globally -- media directory, quality, logging, ffmpeg -- and
doing that inside the web process would leak those settings into every later
render and every other stage.

**Fifteen kinds, not one.** The first version of this drew boxes and arrows and
nothing else, so every scene that was not a sequence of steps got a still. A
sequence, a comparison, layers, a loop, a tree, a network, a plotted function,
bars, a timeline, a table, a counting number, a formula built term by term, the
author's own figure with its labels arriving, one thing becoming another, and
code read line by line -- each is a shape a piece of teaching actually takes,
and each assembles while the narration describes it.

**Nothing here invents content.** Every label, number, edge and term comes from
the spec, which came from the source material. A spec with three nodes draws
three nodes. Where something cannot be known -- which part of a scanned figure a
caption refers to, for instance -- it is not guessed: the figure's labels are
laid beside it rather than circled on top of a position nobody measured.

**No LaTeX is assumed.** `MathTex` needs a TeX distribution, which most machines
do not have, so every kind here is built from Pango text and vector shapes.
A formula is typeset with TeX only when `latex` is actually on PATH, and reads
as plain text when it is not.

`--probe <kind>` renders that one kind into a temporary file and prints ok or
the reason it failed, which is how the registry knows what this machine can
really draw rather than what this file claims.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

KINDS = (
    "flow", "compare", "stack", "cycle", "tree", "graph", "plot", "bars",
    "timeline", "table", "counter", "formula", "figure", "morph", "code",
)


def has_latex() -> bool:
    return bool(shutil.which("latex") or shutil.which("xelatex") or shutil.which("pdflatex"))


# --- what every scene shares ---------------------------------------------------------


class Palette:
    """The project's colours, so a clip matches the frames around it."""

    def __init__(self, spec: dict) -> None:
        self.background = spec.get("background", "#0D0F14")
        self.accent = spec.get("accent", "#E879A8")
        self.text = spec.get("text", "#E8EAF0")
        self.dim = spec.get("dim", "#9AA3B5")


def beat_for(seconds: float, parts: int) -> float:
    """How long one thing takes to arrive.

    Divided by what is being built rather than fixed, so a six-part diagram over
    four seconds does not run at the pace of a two-part one -- and floored, so a
    long list does not flicker.
    """
    return max(0.28, min(1.1, seconds / max(2, parts + 2)))


def labelled_box(label: str, palette: Palette, width: float = 3.2, height: float = 1.3):
    from manim import Rectangle, Text, VGroup

    box = Rectangle(width=width, height=height, color=palette.accent, stroke_width=3)
    words = Text(label[:30], font_size=22, color=palette.text)
    if words.width > width - 0.3:
        words.scale((width - 0.3) / words.width)
    words.move_to(box.get_center())
    return VGroup(box, words)


def fitted(group, width: float = 12.0, height: float = 6.0, most: float = 1.0):
    """Fit a group to the frame, growing it no more than `most`.

    Shrinking is unconditional: anything that would run off the frame has to
    come in. Growing is bounded, because these groups are built out of boxes
    sized to hold their text -- but left at exactly their natural size, four
    boxes in a row occupy a band across the middle of a 1080-tall frame and
    leave two thirds of it empty, which reads as a placeholder.
    """
    scale = min(most, width / max(0.01, group.width), height / max(0.01, group.height))
    return group.scale(scale)


def filled(group, width: float = 11.5, height: float = 5.4):
    """Scale a shape to fill the frame, up or down.

    For the kinds whose size means nothing on its own -- bars, a line of events,
    a number. Drawn at their natural size they sit in the middle of a 1920-wide
    frame taking up a third of it, which reads as a placeholder.
    """
    scale = min(width / max(0.01, group.width), height / max(0.01, group.height))
    return group.scale(scale)


def caption_for(scene, spec: dict, palette: Palette, beat: float):
    from manim import UP, FadeIn, Text

    if not spec.get("caption"):
        return None
    caption = Text(str(spec["caption"])[:70], font_size=30, color=palette.text)
    caption.to_edge(UP, buff=0.5)
    scene.play(FadeIn(caption), run_time=beat * 0.6)
    return caption


def hold_to_length(scene, seconds: float) -> None:
    """Stay on the finished picture for whatever is left of the narration."""
    scene.wait(max(0.3, seconds - scene.renderer.time))


# --- the kinds -----------------------------------------------------------------------


def draw_flow(scene, spec, palette, seconds):
    """Steps in order, each arriving, then the arrows between them."""
    from manim import LEFT, RIGHT, UP, Arrow, Create, FadeIn, VGroup

    nodes = spec["nodes"][:6]
    beat = beat_for(seconds, len(nodes))
    caption = caption_for(scene, spec, palette, beat)

    boxes = VGroup(*[labelled_box(label, palette) for label in nodes])
    boxes.arrange(RIGHT, buff=0.9)
    fitted(boxes, 12.4, 4.6, most=1.7).move_to([0, -0.4 if caption else 0, 0])

    # The arrow arrives with the step it points at, not in a second pass over
    # the whole chain: the narration says "and then the amplifier", and the link
    # and the thing linked to belong to that same moment.
    scene.play(FadeIn(boxes[0], shift=UP * 0.2), run_time=beat)
    for first, second in zip(boxes[:-1], boxes[1:], strict=False):
        arrow = Arrow(first.get_right(), second.get_left(), buff=0.1,
                      color=palette.accent, stroke_width=4,
                      max_tip_length_to_length_ratio=0.25)
        scene.play(Create(arrow), FadeIn(second, shift=UP * 0.2), run_time=beat)
    assert LEFT is not None
    hold_to_length(scene, seconds)


def draw_compare(scene, spec, palette, seconds):
    """Two or three things set against each other, side by side.

    A dividing rule down the middle rather than arrows: the point of a
    comparison is that the parts are separate, and an arrow between them says
    the opposite.
    """
    from manim import DOWN, RIGHT, UP, Create, FadeIn, Line, Text, VGroup

    nodes = spec["nodes"][:6]
    labels = spec.get("labels") or []
    beat = beat_for(seconds, len(nodes))
    caption = caption_for(scene, spec, palette, beat)

    columns = min(len(labels) or 2, 3) if labels else 2
    per_column = max(1, -(-len(nodes) // columns))

    groups = []
    for index in range(columns):
        items = nodes[index * per_column:(index + 1) * per_column]
        if not items:
            continue
        stack = VGroup()
        if index < len(labels):
            heading = Text(str(labels[index])[:24], font_size=28, color=palette.accent)
            stack.add(heading)
        for item in items:
            stack.add(labelled_box(item, palette, width=4.4, height=1.0))
        stack.arrange(DOWN, buff=0.35)
        groups.append(stack)

    laid = VGroup(*groups).arrange(RIGHT, buff=1.6)
    fitted(laid, 12.5, 5.4, most=1.5).move_to([0, -0.4 if caption else 0, 0])

    for index, group in enumerate(laid):
        if index:
            rule = Line(
                group.get_left() + UP * (laid.height / 2) + RIGHT * -0.8,
                group.get_left() + DOWN * (laid.height / 2) + RIGHT * -0.8,
                color=palette.dim, stroke_width=2,
            )
            scene.play(Create(rule), run_time=beat * 0.3)
        for part in group:
            scene.play(FadeIn(part, shift=UP * 0.15), run_time=beat * 0.8)
    hold_to_length(scene, seconds)


def draw_stack(scene, spec, palette, seconds):
    """Layers, built from the bottom up, because that is how a stack is read."""
    from manim import UP, FadeIn, VGroup

    nodes = spec["nodes"][:7]
    beat = beat_for(seconds, len(nodes))
    caption = caption_for(scene, spec, palette, beat)

    boxes = VGroup(*[labelled_box(label, palette, width=6.4, height=0.95)
                     for label in reversed(nodes)])
    boxes.arrange(UP, buff=0.18)
    fitted(boxes, 12.0, 5.4, most=1.4).move_to([0, -0.4 if caption else 0, 0])

    for box in boxes:
        scene.play(FadeIn(box, shift=UP * 0.25), run_time=beat)
    hold_to_length(scene, seconds)


def draw_cycle(scene, spec, palette, seconds):
    """A loop: the parts placed round a circle, then arrows closing the ring."""
    import math

    from manim import Arrow, Create, FadeIn, VGroup

    nodes = spec["nodes"][:6]
    beat = beat_for(seconds, len(nodes))
    caption = caption_for(scene, spec, palette, beat)

    radius = 2.6
    boxes = VGroup()
    for index, label in enumerate(nodes):
        angle = math.pi / 2 - index * (2 * math.pi / max(1, len(nodes)))
        box = labelled_box(label, palette, width=2.7, height=1.0)
        box.move_to([radius * math.cos(angle), radius * math.sin(angle), 0])
        boxes.add(box)
    fitted(boxes, 11.5, 5.4, most=1.3).move_to([0, -0.4 if caption else 0, 0])

    for box in boxes:
        scene.play(FadeIn(box, scale=0.9), run_time=beat)
    for index in range(len(boxes)):
        first, second = boxes[index], boxes[(index + 1) % len(boxes)]
        arrow = Arrow(first.get_center(), second.get_center(), buff=1.15,
                      color=palette.accent, stroke_width=3, path_arc=-0.9,
                      max_tip_length_to_length_ratio=0.2)
        scene.play(Create(arrow), run_time=beat * 0.4)
    hold_to_length(scene, seconds)


def _edges_of(spec, count: int) -> list[tuple[int, int]]:
    """The edges the spec names, kept inside the node list.

    A chain when none are given: a list of things with no stated relationships
    is at least in an order, and drawing that is honest where inventing a
    topology would not be.
    """
    edges = []
    for pair in spec.get("edges") or []:
        if len(pair) == 2 and all(0 <= int(end) < count for end in pair) and pair[0] != pair[1]:
            edges.append((int(pair[0]), int(pair[1])))
    return edges or [(index, index + 1) for index in range(count - 1)]


def draw_tree(scene, spec, palette, seconds):
    """A hierarchy, laid out by depth from its first node."""
    from manim import DOWN, UP, Create, FadeIn, Line, VGroup

    nodes = spec["nodes"][:10]
    edges = _edges_of(spec, len(nodes))
    beat = beat_for(seconds, len(nodes))
    caption = caption_for(scene, spec, palette, beat)

    depth = {0: 0}
    children: dict[int, list[int]] = {}
    for parent, child in edges:
        children.setdefault(parent, []).append(child)
        depth[child] = depth.get(parent, 0) + 1

    rows: dict[int, list[int]] = {}
    for index in range(len(nodes)):
        rows.setdefault(depth.get(index, 0), []).append(index)

    placed = {}
    boxes = VGroup()
    for level, row in sorted(rows.items()):
        width = 2.6
        span = (len(row) - 1) * (width + 0.5)
        for position, index in enumerate(row):
            box = labelled_box(nodes[index], palette, width=width, height=0.9)
            box.move_to([-span / 2 + position * (width + 0.5), 2.0 - level * 1.7, 0])
            placed[index] = box
            boxes.add(box)
    fitted(boxes, 12.5, 5.4, most=1.4).move_to([0, -0.4 if caption else 0, 0])

    for level, row in sorted(rows.items()):
        scene.play(*[FadeIn(placed[index], shift=DOWN * 0.2 if level else UP * 0.2)
                     for index in row], run_time=beat)
        for parent, child in edges:
            if depth.get(child, 0) != level or parent not in placed:
                continue
            scene.play(Create(Line(placed[parent].get_bottom(), placed[child].get_top(),
                                   color=palette.dim, stroke_width=2)),
                       run_time=beat * 0.25)
    hold_to_length(scene, seconds)


def draw_graph(scene, spec, palette, seconds):
    """A network: the things, then the connections between them.

    Laid out by spring forces rather than placed by hand, because a network's
    shape is a property of its connections and putting the nodes anywhere else
    tells the viewer something untrue about it.
    """
    import networkx
    from manim import Create, Dot, FadeIn, Line, Text, VGroup

    nodes = spec["nodes"][:12]
    edges = _edges_of(spec, len(nodes))
    beat = beat_for(seconds, len(nodes))
    caption = caption_for(scene, spec, palette, beat)

    graph = networkx.Graph()
    graph.add_nodes_from(range(len(nodes)))
    graph.add_edges_from(edges)
    layout = networkx.spring_layout(graph, seed=7, k=1.4)

    dots, labels = {}, VGroup()
    for index, label in enumerate(nodes):
        x, y = layout[index]
        dot = Dot([x * 4.2, y * 2.6, 0], color=palette.accent, radius=0.13)
        words = Text(label[:18], font_size=20, color=palette.text)
        words.next_to(dot, direction=[0, -1, 0], buff=0.18)
        dots[index] = dot
        labels.add(VGroup(dot, words))
    fitted(labels, 12.0, 5.4, most=1.3).move_to([0, -0.4 if caption else 0, 0])

    for pair in labels:
        scene.play(FadeIn(pair, scale=0.85), run_time=beat * 0.7)
    for first, second in edges:
        scene.play(Create(Line(dots[first].get_center(), dots[second].get_center(),
                               color=palette.dim, stroke_width=2)),
                   run_time=beat * 0.22)
    hold_to_length(scene, seconds)


def _safe_expression(expression: str):
    """A one-variable function of x, evaluated from a named, closed vocabulary.

    A closed vocabulary rather than `eval` on whatever arrives: this text came
    from a model, the process it runs in can read the whole project, and there
    is no expression worth that.
    """
    import math

    allowed = {
        "sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp,
        "log": math.log, "sqrt": math.sqrt, "abs": abs, "pi": math.pi, "e": math.e,
        "atan": math.atan, "tanh": math.tanh, "floor": math.floor, "pow": pow,
        "min": min, "max": max,
    }
    code = compile(expression, "<plot>", "eval")
    for name in code.co_names:
        # `x` is the variable itself; in an eval-compiled expression it is
        # looked up by name like everything else.
        if name != "x" and name not in allowed:
            raise ValueError(f"{name!r} is not something a plot may call")

    def evaluate(x: float) -> float:
        return float(eval(code, {"__builtins__": {}}, {**allowed, "x": x}))   # noqa: S307

    evaluate(0.0)     # fail here, before anything is drawn
    return evaluate


def _plain_axes(palette, x_range, y_range):
    from manim import Axes

    return Axes(
        x_range=x_range, y_range=y_range, x_length=9.5, y_length=4.8,
        axis_config={"color": palette.dim, "stroke_width": 2,
                     "include_ticks": True, "include_numbers": False},
        tips=False,
    )


def draw_plot(scene, spec, palette, seconds):
    """A curve drawn as it is described, with a dot running along it."""
    from manim import DOWN, LEFT, Create, Dot, FadeIn, Text, ValueTracker, VGroup, always_redraw

    beat = beat_for(seconds, 4)
    caption = caption_for(scene, spec, palette, beat)
    evaluate = _safe_expression(spec.get("expression") or "sin(x)")

    span = spec.get("x_range") or [-4, 4]
    sampled = [evaluate(span[0] + step * (span[1] - span[0]) / 40) for step in range(41)]
    low, high = min(sampled), max(sampled)
    pad = max(0.5, (high - low) * 0.15)

    axes = _plain_axes(palette, [span[0], span[1]], [low - pad, high + pad])
    labels = VGroup()
    names = spec.get("labels") or []
    if names:
        labels.add(Text(str(names[0])[:22], font_size=22, color=palette.dim)
                   .next_to(axes, DOWN, buff=0.25))
    if len(names) > 1:
        labels.add(Text(str(names[1])[:22], font_size=22, color=palette.dim)
                   .next_to(axes, LEFT, buff=0.25).rotate(1.5708))

    frame = VGroup(axes, labels)
    fitted(frame, 12.0, 5.4).move_to([0, -0.4 if caption else 0, 0])

    scene.play(Create(axes), run_time=beat)
    if len(labels):
        scene.play(FadeIn(labels), run_time=beat * 0.5)

    curve = axes.plot(evaluate, x_range=[span[0], span[1]], color=palette.accent, stroke_width=4)
    scene.play(Create(curve), run_time=max(beat * 2, seconds * 0.35))

    walker = ValueTracker(span[0])
    dot = always_redraw(
        lambda: Dot(axes.c2p(walker.get_value(), evaluate(walker.get_value())),
                    color=palette.text, radius=0.08))
    scene.add(dot)
    scene.play(walker.animate.set_value(span[1]),
               run_time=max(0.8, seconds - scene.renderer.time - 0.4))
    hold_to_length(scene, seconds)


def draw_bars(scene, spec, palette, seconds):
    """The stated quantities, growing in the order they are said."""
    from manim import DOWN, UP, GrowFromEdge, Rectangle, Text, VGroup

    values = [float(value) for value in (spec.get("values") or [])][:8]
    names = (spec.get("nodes") or spec.get("labels") or [])[:8]
    if not values:
        raise ValueError("a bar chart needs values")
    beat = beat_for(seconds, len(values))
    caption = caption_for(scene, spec, palette, beat)

    largest = max(abs(value) for value in values) or 1
    bars = VGroup()
    for index, value in enumerate(values):
        height = max(0.15, 4.0 * abs(value) / largest)
        bar = Rectangle(width=0.9, height=height, color=palette.accent,
                        fill_color=palette.accent, fill_opacity=0.75, stroke_width=0)
        number = Text(f"{value:g}", font_size=22, color=palette.text)
        name = Text(str(names[index])[:14] if index < len(names) else "",
                    font_size=20, color=palette.dim)
        column = VGroup(number, bar, name).arrange(DOWN, buff=0.16)
        bars.add(column)
    bars.arrange([1, 0, 0], buff=0.8, aligned_edge=DOWN)
    filled(bars, 11.0, 5.2).move_to([0, -0.5 if caption else 0, 0])
    assert UP is not None

    for column in bars:
        scene.play(GrowFromEdge(column, DOWN), run_time=beat)
    hold_to_length(scene, seconds)


def draw_timeline(scene, spec, palette, seconds):
    """Events on a line, arriving in order."""
    from manim import DOWN, UP, Create, Dot, FadeIn, Line, Text, VGroup

    nodes = spec["nodes"][:7]
    beat = beat_for(seconds, len(nodes))
    caption = caption_for(scene, spec, palette, beat)

    line = Line([-5.6, 0, 0], [5.6, 0, 0], color=palette.dim, stroke_width=3)
    marks = VGroup()
    for index, label in enumerate(nodes):
        at = -5.2 + index * (10.4 / max(1, len(nodes) - 1)) if len(nodes) > 1 else 0
        dot = Dot([at, 0, 0], color=palette.accent, radius=0.1)
        words = Text(str(label)[:22], font_size=21, color=palette.text)
        words.next_to(dot, UP if index % 2 == 0 else DOWN, buff=0.3)
        marks.add(VGroup(dot, words))

    frame = VGroup(line, marks)
    filled(frame, 12.4, 4.6).move_to([0, -0.4 if caption else 0, 0])

    scene.play(Create(line), run_time=beat)
    for mark in marks:
        scene.play(FadeIn(mark, shift=UP * 0.15), run_time=beat * 0.8)
    hold_to_length(scene, seconds)


def draw_table(scene, spec, palette, seconds):
    """Rows arriving one at a time, under a header that is already there."""
    from manim import DOWN, RIGHT, Create, FadeIn, Line, Text, VGroup

    headers = (spec.get("labels") or [])[:4]
    rows = [str(row).split("|") for row in (spec.get("nodes") or [])][:7]
    if not rows:
        raise ValueError("a table needs rows")
    columns = max(len(headers), max(len(row) for row in rows))
    beat = beat_for(seconds, len(rows))
    caption = caption_for(scene, spec, palette, beat)

    def cell(text, size, colour):
        words = Text(str(text).strip()[:22], font_size=size, color=colour)
        holder = VGroup(words)
        holder.width = max(words.width, 0.1)
        return holder

    # Columns at a readable spacing, centred, rather than spread to the frame
    # edges: a two-column table pinned to both sides is two lists, not a table.
    gap = 3.4
    span = (columns - 1) * gap
    laid = VGroup()
    header_row = VGroup(*[cell(headers[index] if index < len(headers) else "", 26, palette.accent)
                          for index in range(columns)])
    for index, item in enumerate(header_row):
        item.move_to([-span / 2 + index * gap, 2.2, 0])
    laid.add(header_row)

    drawn_rows = []
    for position, row in enumerate(rows):
        line = VGroup(*[cell(row[index] if index < len(row) else "", 24, palette.text)
                        for index in range(columns)])
        for index, item in enumerate(line):
            item.move_to([-span / 2 + index * gap, 1.5 - position * 0.8, 0])
        drawn_rows.append(line)
        laid.add(line)
    fitted(laid, 12.0, 5.4, most=1.4).move_to([0, -0.4 if caption else 0, 0])

    scene.play(FadeIn(header_row), run_time=beat * 0.8)
    rule_y = header_row.get_bottom()[1] - 0.25
    scene.play(Create(Line([laid.get_left()[0] - 0.4, rule_y, 0],
                           [laid.get_right()[0] + 0.4, rule_y, 0],
                           color=palette.dim, stroke_width=2)), run_time=beat * 0.3)
    for line in drawn_rows:
        scene.play(FadeIn(line, shift=RIGHT * 0.2), run_time=beat * 0.7)
    assert DOWN is not None
    hold_to_length(scene, seconds)


def draw_counter(scene, spec, palette, seconds):
    """One number moving from where it starts to where it ends.

    For the scenes that turn on a quantity changing -- and unlike a bar, it is
    the number itself the viewer watches, which is what the narration is saying.
    """
    from manim import DOWN, DecimalNumber, FadeIn, Text, ValueTracker, VGroup

    values = [float(value) for value in (spec.get("values") or [0, 100])][:2]
    start, end = (values + [values[0]])[:2] if len(values) == 1 else values[:2]
    places = 0 if float(end).is_integer() and float(start).is_integer() else 2
    beat = beat_for(seconds, 2)
    caption = caption_for(scene, spec, palette, beat)

    number = DecimalNumber(start, num_decimal_places=places, color=palette.accent,
                           font_size=140, mob_class=Text)
    label = Text(str((spec.get("nodes") or [""])[0])[:36], font_size=30, color=palette.text)
    frame = VGroup(number, label).arrange(DOWN, buff=0.5)
    fitted(frame, 11.0, 5.0).move_to([0, -0.4 if caption else 0, 0])

    scene.play(FadeIn(frame), run_time=beat * 0.7)
    tracker = ValueTracker(start)
    number.add_updater(lambda mob: mob.set_value(tracker.get_value()))
    scene.play(tracker.animate.set_value(end),
               run_time=max(1.0, seconds - scene.renderer.time - 0.5))
    number.clear_updaters()
    hold_to_length(scene, seconds)


def draw_formula(scene, spec, palette, seconds):
    """An expression written out, then each later step replacing the last.

    Typeset with TeX where a TeX distribution exists and as plain text where it
    does not: a machine without LaTeX still gets the derivation, one line at a
    time, which is the part that matters.
    """
    from manim import FadeOut, Text, TransformMatchingShapes, Write

    steps = [str(step) for step in (spec.get("steps") or []) if str(step).strip()]
    if spec.get("formula"):
        steps = [str(spec["formula"]), *steps]
    if not steps:
        raise ValueError("a formula needs something to write")
    beat = beat_for(seconds, len(steps))
    caption = caption_for(scene, spec, palette, beat)

    def typeset(text: str):
        if has_latex():
            from manim import MathTex

            try:
                return MathTex(text, color=palette.text, font_size=64)
            except Exception:       # a malformed expression must not lose the scene
                pass
        return Text(text[:80], font_size=52, color=palette.text)

    current = typeset(steps[0])
    current.move_to([0, -0.4 if caption else 0, 0])
    scene.play(Write(current), run_time=max(beat, 0.9))

    for step in steps[1:5]:
        following = typeset(step)
        following.move_to(current.get_center())
        scene.play(TransformMatchingShapes(current, following),
                   run_time=max(beat, 0.8))
        current = following
    assert FadeOut is not None
    hold_to_length(scene, seconds)


def draw_figure(scene, spec, palette, seconds):
    """The author's own figure, with this scene's labels arriving beside it.

    Beside it, never drawn on top of it. Circling a region would mean knowing
    where in the picture that region is, and nothing here has looked at the
    picture -- a ring around a guessed position is a confident lie about
    somebody else's diagram.
    """
    from manim import DOWN, LEFT, RIGHT, FadeIn, ImageMobject, Text, VGroup

    path = spec.get("image") or ""
    if not path or not Path(path).exists():
        raise ValueError("the figure is not on disk")
    labels = [str(label) for label in (spec.get("nodes") or []) if str(label).strip()][:4]
    beat = beat_for(seconds, len(labels) + 1)
    caption = caption_for(scene, spec, palette, beat)

    # Scaled up to fill its side of the frame, not left at whatever size the
    # file happened to be: an extracted figure is often a few hundred pixels,
    # and drawn at its own size it sits in a corner of a 1920-wide frame.
    picture = ImageMobject(path)
    picture.height = 5.4 if not labels else 5.0
    if picture.width > (7.0 if labels else 11.5):
        picture.width = 7.0 if labels else 11.5

    written = VGroup(*[Text(f"— {label[:26]}", font_size=28, color=palette.text)
                       for label in labels])
    if len(written):
        written.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        picture.to_edge(LEFT, buff=0.9)
        written.next_to(picture, RIGHT, buff=0.8)
    if caption:
        picture.shift([0, -0.4, 0])
        if len(written):
            written.shift([0, -0.4, 0])

    scene.add(picture)
    scene.play(picture.animate.scale(1.02), run_time=beat)
    for line in written:
        scene.play(FadeIn(line, shift=RIGHT * 0.2), run_time=beat)
    hold_to_length(scene, seconds)


def draw_morph(scene, spec, palette, seconds):
    """One thing becoming another, which is the only way to show that it does."""
    from manim import DOWN, Arrow, Create, FadeIn, Text, Transform, VGroup

    nodes = [str(node) for node in spec["nodes"]][:2]
    if len(nodes) < 2:
        raise ValueError("a morph needs something to become something else")
    beat = beat_for(seconds, 3)
    caption = caption_for(scene, spec, palette, beat)

    before = Text(nodes[0][:26], font_size=56, color=palette.text)
    after = Text(nodes[1][:26], font_size=56, color=palette.accent)
    for words in (before, after):
        words.move_to([0, -0.4 if caption else 0, 0])

    note = VGroup(*[Text(str(label)[:30], font_size=24, color=palette.dim)
                    for label in (spec.get("labels") or [])[:1]])
    if len(note):
        note.arrange(DOWN).next_to(before, DOWN, buff=0.9)

    scene.play(FadeIn(before), run_time=beat)
    if len(note):
        scene.play(FadeIn(note), run_time=beat * 0.5)
    scene.play(Transform(before, after), run_time=max(beat * 2, 1.0))
    assert Arrow is not None and Create is not None
    hold_to_length(scene, seconds)


def draw_code(scene, spec, palette, seconds):
    """Code, highlighted, with each line arriving as it is read out.

    Pygments does the highlighting, which Manim already depends on, so this
    needs nothing a machine drawing a flow does not already have.
    """
    from manim import UP, Code, FadeIn

    source = str(spec.get("code") or "\n".join(spec.get("nodes") or []))
    if not source.strip():
        raise ValueError("a code scene needs code")
    lines = source.splitlines()[:14]
    beat = beat_for(seconds, len(lines))
    caption = caption_for(scene, spec, palette, beat)

    block = Code(
        code_string="\n".join(lines),
        language=str(spec.get("language") or "python"),
        formatter_style="monokai",
        background="window",
        add_line_numbers=True,
    )
    fitted(block, 11.0, 5.4, most=1.3).move_to([0, -0.4 if caption else 0, 0])

    # The window and the numbers arrive first, then the lines in turn: the
    # frame around the code is not part of what is being said.
    scene.play(FadeIn(block[0]), run_time=beat * 0.6)
    for part in block[1:]:
        scene.play(FadeIn(part, shift=UP * 0.1), run_time=max(0.18, beat * 0.6))
    hold_to_length(scene, seconds)


BUILDERS = {
    "flow": draw_flow,
    "compare": draw_compare,
    "stack": draw_stack,
    "cycle": draw_cycle,
    "tree": draw_tree,
    "graph": draw_graph,
    "plot": draw_plot,
    "bars": draw_bars,
    "timeline": draw_timeline,
    "table": draw_table,
    "counter": draw_counter,
    "formula": draw_formula,
    "figure": draw_figure,
    "morph": draw_morph,
    "code": draw_code,
}


# --- running one -------------------------------------------------------------------


def build(spec: dict) -> None:
    from manim import Scene, config

    kind = spec.get("kind", "flow")
    builder = BUILDERS.get(kind)
    if builder is None:
        raise SystemExit(f"{kind!r} is not a kind this renderer draws")

    palette = Palette(spec)
    seconds = max(1.5, float(spec.get("seconds", 4)))

    config.pixel_width = int(spec.get("width", 1920))
    config.pixel_height = int(spec.get("height", 1080))
    config.frame_rate = int(spec.get("frame_rate", 30))
    config.background_color = palette.background
    config.disable_caching = True
    config.verbosity = "ERROR"
    # No progress bars: this runs as a subprocess whose stderr is read to find
    # out why a render failed, and a thousand lines of bar redraws bury it.
    config.progress_bar = "none"

    class SceneFromSpec(Scene):
        def construct(self) -> None:
            builder(self, spec, palette, seconds)

    output = Path(spec["output"])
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as working:
        config.media_dir = working
        config.output_file = output.stem
        SceneFromSpec().render()
        made = sorted((path for path in Path(working).rglob(f"{output.stem}.mp4")),
                      key=lambda path: len(path.parts))
        if not made:
            raise SystemExit("manim wrote no clip")
        output.write_bytes(made[0].read_bytes())


PROBES = {
    "flow": {"nodes": ["electrode", "amplifier", "filter"]},
    "compare": {"nodes": ["one", "two", "three", "four"], "labels": ["Before", "After"]},
    "stack": {"nodes": ["application", "transport", "link"]},
    "cycle": {"nodes": ["sense", "decide", "act"]},
    "tree": {"nodes": ["root", "left", "right"], "edges": [[0, 1], [0, 2]]},
    "graph": {"nodes": ["a", "b", "c", "d"], "edges": [[0, 1], [1, 2], [2, 3], [3, 0]]},
    "plot": {"expression": "sin(x)", "x_range": [-3.2, 3.2], "labels": ["time", "amplitude"]},
    "bars": {"values": [3, 7, 5], "nodes": ["one", "two", "three"]},
    "timeline": {"nodes": ["1943", "1958", "1986"]},
    "table": {"nodes": ["alpha|1", "beta|2"], "labels": ["name", "value"]},
    "counter": {"values": [0, 120], "nodes": ["samples per second"]},
    "formula": {"formula": "y = mx + c", "steps": ["y - c = mx"]},
    "figure": {"nodes": ["a label", "another"]},
    "morph": {"nodes": ["a spike", "a number"]},
    "code": {"code": "def spike(v):\n    return v > 50", "language": "python"},
}


def probe(kind: str) -> int:
    """Draw the smallest real example of one kind, and say what happened."""
    if kind not in BUILDERS:
        print(f"no such kind: {kind}")
        return 2

    spec = dict(PROBES[kind]) | {"kind": kind, "seconds": 2, "caption": "probe",
                                 "width": 480, "height": 270, "frame_rate": 15}
    with tempfile.TemporaryDirectory() as working:
        if kind == "figure":
            from PIL import Image

            sample = Path(working) / "probe.png"
            Image.new("RGB", (400, 300), (240, 240, 240)).save(sample)
            spec["image"] = str(sample)
        spec["output"] = str(Path(working) / f"{kind}.mp4")
        try:
            build(spec)
        except Exception as failure:
            print(f"{type(failure).__name__}: {failure}")
            return 1
        made = Path(spec["output"])
        if not made.exists() or made.stat().st_size < 512:
            print("produced no clip")
            return 1
    print("ok")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--probe":
        raise SystemExit(probe(sys.argv[2]))
    build(json.loads(sys.stdin.read()))
