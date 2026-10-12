"""manimkit -- a Manim scene as a scene program, timed to the narration.

What a scene program writes with it:

    # /// script
    # requires-python = ">=3.11"
    # dependencies = ["manim>=0.19", "pillow"]
    # ///
    from manimkit import *      # every Manim name, and the kit


    class TheScene(ExplainerScene):
        def construct(self):
            title = self.label("Body image", size=60, at=(0, 2.6))
            self.play(FadeIn(title), run_time=0.8)
            self.until(self.when("sensors"))          # the moment the word is spoken
            ...
            self.finish()                               # holds to the exact length

    run(TheScene)

Layout is kept for you: anything with words or a picture is fitted inside the
frame's margin when it first appears, and words that would land on words or a
picture already on screen are moved to the nearest free place above or below.
Nothing runs past the end of the narration: a late animation is played faster,
a late pause is cut short. A picture given to
`Create` or `Write` fades in instead (only outlines can be drawn), a thing given
to `play()` without an animation is drawn in, and a run time of zero or less plays
for one frame: each of these would otherwise stop the whole scene.
`self.safe(m)` keeps anything inside the margin; `self.row([...], y)` and
`self.column([...], x)` place items so they never overlap or leave the frame;
`self.boxed(text)` puts words in a box sized to them; `self.connect(a, b)` draws an
arrow edge to edge, never through words; `self.picture(path)` shows a slide picture.

Diagrams laid out for you -- prefer them to placing boxes by hand, which is what
fails most (boxes over boxes, circles through their own labels, a diagram in one
strip of the frame): `self.flow(steps)` (boxes joined by arrows),
`self.hub(centre, around)` (one idea and what hangs off it), and
`self.timeline(events)` (things in order). Each comes back placed; reveal its
parts (.boxes/.arrows, .centre/.items/.lines, .spine/.dots/.labels) on the words.

It does four things the checks rely on:

1. **Frame and look**: the brief's size, frame rate and background colour.
2. **Time**: `self.when(words)` is the second those words are spoken (from the
   narration's own word timings); `self.until(t)` waits to it; `self.finish()`
   ends the scene at exactly `brief.seconds`.
3. **Text, recorded**: every `self.label(...)` is a `Text` whose box, colour,
   size and background are written to `layout.json` at each beat, so the checks
   can see bounds, overlap, contrast and size without guessing from pixels.
4. **Output**: the clip is copied to `render.mp4`.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import manim
import numpy as np
from manim import *  # noqa: F403 -- `from manimkit import *` gives every Manim name
from manim import Scene, Text, VMobject, tempconfig

from scenekit import load_brief

BRIEF = load_brief()
FRAME_WIDTH_UNITS = 14.222
FRAME_HEIGHT_UNITS = 8.0
# An outline is followed at most this many pixels between samples, so a 36 px line of
# words cannot fall between two of them (48 fixed samples left 30 px gaps on a long line).
SAMPLE_PX = 6.0
SMALLEST_SHAPE_PX = 40          # a dot or a marker is not a shape that collides
BACKGROUND_SHARE = 0.9          # a shape this much of the frame is a background


def _px(point) -> tuple[float, float]:
    x = (point[0] + FRAME_WIDTH_UNITS / 2) / FRAME_WIDTH_UNITS * BRIEF.width
    y = (FRAME_HEIGHT_UNITS / 2 - point[1]) / FRAME_HEIGHT_UNITS * BRIEF.height
    return x, y


def _px_all(points: np.ndarray) -> np.ndarray:
    """Scene points (n, 2) as pixels."""
    return np.column_stack([
        (points[:, 0] + FRAME_WIDTH_UNITS / 2) / FRAME_WIDTH_UNITS * BRIEF.width,
        (FRAME_HEIGHT_UNITS / 2 - points[:, 1]) / FRAME_HEIGHT_UNITS * BRIEF.height])


def _trace(m) -> np.ndarray:
    """Points along a shape's outline, in scene units, at most SAMPLE_PX apart:
    each cubic piece of it sampled by its own length."""
    count = len(m.points) // 4
    if not count:
        return np.zeros((0, 2))
    curves = np.asarray(m.points[:4 * count], dtype=float).reshape(count, 4, 3)[:, :, :2]
    lengths = (np.linalg.norm(np.diff(curves, axis=1), axis=2).sum(axis=1)
               * BRIEF.width / FRAME_WIDTH_UNITS)
    parts = []
    for curve, length in zip(curves, lengths, strict=False):
        t = np.linspace(0, 1, int(min(400, max(2, length / SAMPLE_PX))) + 1)[:, None]
        parts.append((1 - t) ** 3 * curve[0] + 3 * (1 - t) ** 2 * t * curve[1]
                     + 3 * (1 - t) * t ** 2 * curve[2] + t ** 3 * curve[3])
    return np.vstack(parts)


def _stroked(m) -> bool:
    """Whether a shape has an outline you can see. A filled shape with no stroke has
    none: Manim keeps the stroke's opacity at 1 when its width is 0."""
    return m.get_stroke_width() > 0 and m.get_stroke_opacity() > 0.3


def _inside(points: np.ndarray, polygon: np.ndarray) -> np.ndarray:
    """Which of `points` lie inside the closed outline `polygon` (ray casting)."""
    x, y = points[:, :1], points[:, 1:2]
    x0, y0 = polygon[None, :, 0], polygon[None, :, 1]
    x1, y1 = np.roll(polygon[:, 0], -1)[None, :], np.roll(polygon[:, 1], -1)[None, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        crosses = ((y0 > y) != (y1 > y)) & (x < (x1 - x0) * (y - y0) / (y1 - y0) + x0)
    return crosses.sum(axis=1) % 2 == 1


def _cross(a: np.ndarray, b: np.ndarray, room: float = 4.0) -> bool:
    """Whether outline `a` runs through the closed outline `b`: part of it well
    inside and part well outside. One inside the other, or two touching, is not."""
    if (a[:, 0].max() < b[:, 0].min() or b[:, 0].max() < a[:, 0].min()
            or a[:, 1].max() < b[:, 1].min() or b[:, 1].max() < a[:, 1].min()):
        return False
    clear = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)).min(axis=1) > room
    inside = _inside(a, b)
    return bool((inside & clear).any() and (~inside & clear).any())


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower())


def _drawn_or_faded(kind) -> None:
    """`Create(picture)` is a TypeError in Manim: only outlines can be drawn. A
    picture (or a group holding one) fades in instead of stopping the scene."""
    def __new__(cls, mobject=None, *args, **kwargs):
        if mobject is not None and not isinstance(mobject, VMobject):
            kept = {k: v for k, v in kwargs.items() if k in ("run_time", "rate_func")}
            return manim.FadeIn(mobject, **kept)
        return object.__new__(cls)
    kind.__new__ = __new__


for _kind in (manim.Create, manim.Write, manim.DrawBorderThenFill):
    _drawn_or_faded(_kind)

TEXT_KINDS = (manim.Text, manim.MarkupText, manim.Paragraph)


def _motion_names(animation) -> list[str]:
    """What kinds of motion an animation is, for the motion check: a group is the
    animations in it; `mobject.animate...` is a move."""
    inner = getattr(animation, "animations", None)
    if inner:
        return [name for part in inner for name in _motion_names(part)]
    name = type(animation).__name__
    return ["Move" if name in ("_AnimationBuilder", "_MethodAnimation") else name]


class _Seconds(float):
    """A number of seconds that can also be called for itself."""

    def __call__(self) -> float:
        return float(self)


class ExplainerScene(Scene):
    """A Manim scene that knows the brief, the narration's timing and its text."""

    brief = BRIEF
    look = BRIEF.look

    def setup(self) -> None:
        self._placed: set[int] = set()
        self._plays: list[list[str]] = []
        self._leaving: set[int] = set()
        self._labels: list[tuple[Text, str, str, str]] = []
        self._snapshots: list[dict] = []
        self._spoken = BRIEF.__dict__.get("words") or []
        self._flat = [(i, w) for i, timed in enumerate(self._spoken)
                      for w in _words(timed.get("text", ""))]
        self._narration = _words(BRIEF.narration)

    # --- layout kept for the script -----------------------------------------------------

    def play(self, *animations, **kwargs):
        # `self.play(arrow)` -- a thing, not an animation of it -- is a TypeError in
        # Manim that stops the whole scene. It means "bring it on": draw an outline,
        # fade anything else in.
        animations = tuple(
            (manim.Create(a) if isinstance(a, VMobject) else manim.FadeIn(a))
            if isinstance(a, manim.Mobject) else a for a in animations)
        # What is fading out now is not in the way of what fades in to replace it.
        self._leaving = {id(part) for a in animations if getattr(a, "remover", False)
                         for part in a.mobject.get_family()}
        self._plays.append([name for a in animations for name in _motion_names(a)])
        # A run time worked out from the narration ("until the next word") can come
        # to zero or less when the words have already been spoken; Manim refuses to
        # play that, and the whole scene stops. One frame instead.
        if kwargs.get("run_time") is not None and kwargs["run_time"] <= 0:
            kwargs["run_time"] = 1 / BRIEF.fps
        # The scene lasts exactly as long as its narration: an animation that would
        # run past the end is played faster, to finish on the last word.
        asked = kwargs.get("run_time") or max(
            [getattr(a, "run_time", 1.0) for a in animations] or [1.0])
        if self.now + asked > BRIEF.seconds:
            kwargs["run_time"] = max(1 / BRIEF.fps, BRIEF.seconds - self.now)
        try:
            super().play(*animations, **kwargs)
        finally:
            self._leaving = set()

    def wait(self, duration: float = 1.0, *args, **kwargs):
        """A pause never runs past the end of the narration."""
        return super().wait(min(duration, max(1 / BRIEF.fps, BRIEF.seconds - self.now)),
                            *args, **kwargs)

    def add(self, *mobjects):
        for mobject in mobjects:
            if id(mobject) in getattr(self, "_placed", {id(mobject)}):
                continue
            self._placed.add(id(mobject))
            family = mobject.get_family()
            if any(isinstance(m, TEXT_KINDS + (manim.ImageMobject,)) for m in family):
                self.safe(mobject)
                self._clear_of_words(mobject, {id(m) for m in family})
        return super().add(*mobjects)

    @staticmethod
    def _boxes(mobjects, skip: set[int], solid: bool) -> list[tuple[float, ...]]:
        found = []
        for top in mobjects:
            for m in top.get_family():
                if (isinstance(m, TEXT_KINDS) and id(m) not in skip
                        and (not solid or m.get_fill_opacity() >= 0.5)):
                    found.append((m.get_left()[0], m.get_bottom()[1],
                                  m.get_right()[0], m.get_top()[1]))
        return found

    def _outline_points(self, skip: set[int]) -> np.ndarray:
        """Points along the outline of every shape on screen (not words, not `skip`),
        in scene units -- the same outlines, as finely followed, as the checks see."""
        words = {id(part) for top in self.mobjects for m in top.get_family()
                 if isinstance(m, TEXT_KINDS) for part in m.get_family()}
        traces = [_trace(m) for top in self.mobjects for m in top.get_family()
                  if id(m) not in skip and id(m) not in words and isinstance(m, VMobject)
                  and len(m.points) and _stroked(m)]
        return np.vstack(traces) if traces else np.zeros((0, 2))

    def _clear_of_words(self, mobject, own: set[int]) -> None:
        """Move `mobject` up or down to the nearest place where its words land
        neither on words already on screen, nor on a picture (whose own words
        cannot be seen from here), nor on a line, arrow or outline, staying
        inside the margin."""
        others = self._boxes(self.mobjects, own | self._leaving, solid=True)
        if not any(isinstance(m, manim.ImageMobject) for m in mobject.get_family()):
            others += [(m.get_left()[0], m.get_bottom()[1], m.get_right()[0], m.get_top()[1])
                       for top in self.mobjects for m in top.get_family()
                       if isinstance(m, manim.ImageMobject) and id(m) not in self._leaving]
        outline = self._outline_points(own | self._leaving)
        if not others and not len(outline):
            return
        x, y = outline[:, 0], outline[:, 1]

        def clashes() -> bool:
            pad = 0.06
            mine = self._boxes([mobject], set(), solid=False)
            return any(a[0] < b[2] + pad and b[0] < a[2] + pad
                       and a[1] < b[3] + pad and b[1] < a[3] + pad
                       for a in mine for b in others) or any(
                bool(((a[0] < x) & (x < a[2]) & (a[1] < y) & (y < a[3])).any()) for a in mine)

        if not clashes():
            return
        for step in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 8, -8, 10, -10):
            offset = -0.35 * step
            mobject.shift([0, offset, 0])
            inside = (mobject.get_top()[1] <= self.SAFE_Y
                      and mobject.get_bottom()[1] >= -self.SAFE_Y)
            if inside and not clashes():
                return
            mobject.shift([0, -offset, 0])

    # --- time -------------------------------------------------------------------------

    @property
    def now(self) -> float:
        """Seconds into the scene. `self.now()` works too: it is an easy slip, and
        it would otherwise stop the scene with "'float' object is not callable"."""
        return _Seconds(self.renderer.time)

    def when(self, phrase: str, default: float | None = None) -> float:
        """The second these words start being spoken. Falls back to `default`, or
        to a proportional guess, when the narration has no word timings."""
        wanted = _words(phrase)
        flat = self._flat
        for start in range(len(flat) - len(wanted) + 1):
            if [w for _, w in flat[start:start + len(wanted)]] == wanted:
                return self._spoken[flat[start][0]]["start_ms"] / 1000
        if default is not None:
            return default
        narration = self._narration
        for start in range(len(narration) - len(wanted) + 1):
            if narration[start:start + len(wanted)] == wanted:
                return BRIEF.seconds * start / max(1, len(narration))
        return self.now

    def until(self, seconds: float) -> None:
        """Wait until `seconds` into the scene, then record what is on screen."""
        seconds = min(seconds, BRIEF.seconds - 0.05)
        if seconds > self.now + 0.02:
            self.wait(seconds - self.now)
        self.snapshot()

    def finish(self) -> None:
        self.snapshot()
        if BRIEF.seconds - self.now > 0.02:
            self.wait(BRIEF.seconds - self.now)

    # --- text ---------------------------------------------------------------------------

    def label(self, text: str, size: int = 44, color: str | None = None,
              at: tuple[float, float] | None = None, on: str | None = None,
              bold: bool = False, **kwargs) -> Text:
        """On-screen words, recorded for the checks. `size` is in points at 1080p;
        `on` is the colour behind the text when it sits on a panel."""
        fill = color or self.look["text"]
        mobject = Text(text, font_size=size, color=fill,
                       weight="BOLD" if bold else "NORMAL", **kwargs)
        if at is not None:
            mobject.move_to([at[0], at[1], 0])
        # The colour asked for: Manim's get_color() reports the outline, not the fill.
        self._labels.append((mobject, text, on or self.look["background"], fill))
        return mobject

    # --- layout that cannot leave the frame or overlap -----------------------------------

    SAFE_X = FRAME_WIDTH_UNITS / 2 * 0.88      # inside the 5% margin, with room to spare
    SAFE_Y = FRAME_HEIGHT_UNITS / 2 * 0.86

    def safe(self, mobject):
        """Shrink `mobject` if it is wider or taller than the safe area, then move it
        just inside it. Call it after positioning anything near an edge."""
        width_room, height_room = 2 * self.SAFE_X, 2 * self.SAFE_Y
        if mobject.width > width_room or mobject.height > height_room:
            mobject.scale(min(width_room / mobject.width, height_room / mobject.height))
        dx = max(0.0, -self.SAFE_X - mobject.get_left()[0]) - max(
            0.0, mobject.get_right()[0] - self.SAFE_X)
        dy = max(0.0, -self.SAFE_Y - mobject.get_bottom()[1]) - max(
            0.0, mobject.get_top()[1] - self.SAFE_Y)
        mobject.shift([dx, dy, 0])
        return mobject

    def row(self, mobjects, y: float = 0.0, gap: float = 0.6):
        """Lay `mobjects` out left to right at height `y`, never overlapping, scaled
        down together if the row would be wider than the safe area."""
        from manim import RIGHT, VGroup
        group = VGroup(*mobjects).arrange(RIGHT, buff=gap)
        group.move_to([0, y, 0])
        return self.safe(group)

    def column(self, mobjects, x: float = 0.0, gap: float = 0.35):
        """Lay `mobjects` out top to bottom at `x`, never overlapping, scaled down
        together if the column would be taller than the safe area."""
        from manim import DOWN, VGroup
        group = VGroup(*mobjects).arrange(DOWN, buff=gap)
        group.move_to([x, 0, 0])
        return self.safe(group)

    # --- shapes that cannot get in the way of words ------------------------------------

    def boxed(self, text: str, size: int = 40, color: str | None = None, pad: float = 0.25,
              at: tuple[float, float] | None = None, stroke: str | None = None,
              fill: str | None = None):
        """Words in a box sized to them, so they can never spill out of it."""
        from manim import RoundedRectangle, VGroup
        label = self.label(text, size=size, color=color, on=fill or self.look["background"])
        box = RoundedRectangle(corner_radius=0.12, width=label.width + 2 * pad,
                               height=label.height + 2 * pad,
                               stroke_color=stroke or self.look["accent"],
                               fill_color=fill or self.look["background"],
                               fill_opacity=1 if fill else 0).move_to(label)
        group = VGroup(box, label)
        if at is not None:
            group.move_to([at[0], at[1], 0])
        return group

    def connect(self, start, end, color: str | None = None, buff: float = 0.18):
        """An arrow from the edge of `start` to the edge of `end`: it never runs
        through the words or shapes it joins."""
        from manim import Arrow, Mobject

        def point(where):
            # (x, y) is a point too: Manim's own Arrow wants three numbers.
            if isinstance(where, (tuple, list)) and len(where) == 2:
                return np.array([float(where[0]), float(where[1]), 0.0])
            return where.get_center() if isinstance(where, Mobject) else np.asarray(where)

        def edge(where, toward):
            # Where the line between the two centres leaves this thing's box. Manim's
            # own choice is its furthest point that way -- on a rounded box, any
            # corner -- and the arrows between two level boxes came out slanted.
            if not isinstance(where, Mobject):
                return point(where)
            centre = where.get_center()
            dx, dy = (toward - centre)[:2]
            reach = min(where.width / 2 / abs(dx) if dx else np.inf,
                        where.height / 2 / abs(dy) if dy else np.inf)
            return centre if reach == np.inf else centre + (toward - centre) * reach

        a, b = point(start), point(end)
        return Arrow(edge(start, b), edge(end, a), buff=buff, color=color or self.look["accent"],
                     stroke_width=5, max_tip_length_to_length_ratio=0.18)

    def picture(self, path: str, height: float = 3.0, at: tuple[float, float] | None = None):
        """A picture from the slides (a path from brief.assets.pictures)."""
        from manim import ImageMobject
        image = ImageMobject(path).set(height=height)
        if at is not None:
            image.move_to([at[0], at[1], 0])
        return image

    # --- diagrams laid out for you ---------------------------------------------------------
    # Each returns a group already placed: nothing in it overlaps, crosses words or
    # leaves the frame. Bring its parts on as they are spoken, e.g.
    #     f = self.flow(["Sense", "Signal", "Act"])
    #     for i, box in enumerate(f.boxes):
    #         self.until(self.when(...)); self.play(FadeIn(box))
    #         if i: self.play(GrowArrow(f.arrows[i - 1]))

    def flow(self, steps: list[str], y: float = -0.3, size: int = 38, gap: float = 0.9):
        """Steps in boxes joined by arrows, left to right -- top to bottom when they
        do not fit across. Has .boxes and .arrows (arrows[i] joins boxes[i] to [i+1])."""
        from manim import DOWN, RIGHT, VGroup
        boxes = [self.boxed(text, size=size) for text in steps]
        group = VGroup(*boxes).arrange(RIGHT, buff=gap).move_to([0, y, 0])
        if group.width > 2 * self.SAFE_X:
            group.arrange(DOWN, buff=gap * 0.6).move_to([0, y, 0])
        self.safe(group)
        arrows = [self.connect(a, b) for a, b in zip(boxes, boxes[1:], strict=False)]
        whole = VGroup(*boxes, *arrows)
        whole.boxes, whole.arrows = boxes, arrows
        return whole

    def hub(self, centre: str, around: list[str], y: float = -0.3, size: int = 38,
            gap: float = 1.2):
        """One idea in the middle and what hangs off it, in a column either side, each
        joined to the middle by a line from edge to edge. Has .centre, .items, .lines
        (lines[i] joins the centre to items[i])."""
        from manim import DOWN, LEFT, RIGHT, Line, VGroup
        middle = self.boxed(centre, size=size + 4)
        items = [self.boxed(text, size=size) for text in around]
        left = VGroup(*items[0::2]).arrange(DOWN, buff=0.5, aligned_edge=RIGHT)
        right = VGroup(*items[1::2]).arrange(DOWN, buff=0.5, aligned_edge=LEFT) \
            if len(items) > 1 else VGroup()
        left.next_to(middle, LEFT, buff=gap)
        sides = [left]
        if len(right):
            right.next_to(middle, RIGHT, buff=gap)
            sides.append(right)
        self.safe(VGroup(middle, *sides).move_to([0, y, 0]))
        lines = []
        for index, item in enumerate(items):
            start, end = ((middle.get_left(), item.get_right()) if index % 2 == 0
                          else (middle.get_right(), item.get_left()))
            lines.append(Line(start, end, buff=0.1, color=self.look["accent"], stroke_width=4))
        whole = VGroup(middle, *items, *lines)
        whole.centre, whole.items, whole.lines = middle, items, lines
        return whole

    def timeline(self, events: list[str], y: float = -0.4, size: int = 36):
        """Things in order on a line, a dot and a label each. Across the frame with
        labels above and below in turn; down its left side when they do not fit across.
        Has .spine, .dots, .labels."""
        from manim import DOWN, LEFT, RIGHT, UP, Dot, Line, VGroup
        accent = self.look["accent"]
        labels = [self.label(text, size=size) for text in events]
        span = 2 * self.SAFE_X - 0.6
        step = span / max(1, len(events))
        # Neighbours on one side are two steps apart; the end labels must not reach
        # past the frame, or the whole timeline would be shrunk to fit.
        across = max(label.width for label in labels) <= min(2 * step - 0.4, step + 0.6)
        dots = []
        if across:
            spine = Line([-span / 2, y, 0], [span / 2, y, 0], color=self.look["text"],
                         stroke_width=4)
            for index, label in enumerate(labels):
                dot = Dot([-span / 2 + (index + 0.5) * step, y, 0], radius=0.11, color=accent)
                label.next_to(dot, UP if index % 2 == 0 else DOWN, buff=0.35)
                dots.append(dot)
        else:
            top, bottom = self.SAFE_Y - 1.5, -self.SAFE_Y + 0.3
            x = -self.SAFE_X + 0.6
            spine = Line([x, top, 0], [x, bottom, 0], color=self.look["text"], stroke_width=4)
            step = (top - bottom) / max(1, len(events))
            for index, label in enumerate(labels):
                dot = Dot([x, top - (index + 0.5) * step, 0], radius=0.11, color=accent)
                label.next_to(dot, RIGHT, buff=0.4)
                dots.append(dot)
        whole = VGroup(spine, *dots, *labels)
        self.safe(whole)
        whole.spine, whole.dots, whole.labels = spine, dots, labels
        return whole

    # --- what is on screen, for the checks ------------------------------------------------

    def snapshot(self) -> None:
        """Everything on screen now: every piece of text however it was made, the
        outline of every shape, and every picture -- with pixel boxes, and where a
        shape's outline crosses words."""
        from manim import ImageMobject, MarkupText, Paragraph
        text_kinds = (Text, MarkupText, Paragraph)
        recorded = {id(m): (text, behind, fill) for m, text, behind, fill in self._labels}
        texts, word_ids = [], set()
        for top in self.mobjects:
            for m in top.get_family():
                if not isinstance(m, text_kinds) or id(m) in word_ids:
                    continue
                word_ids.update(id(part) for part in m.get_family())
                if m.get_fill_opacity() < 0.5:
                    continue
                text, behind, fill = recorded.get(id(m), (
                    getattr(m, "original_text", "") or getattr(m, "text", ""),
                    self.look["background"], m.get_fill_color().to_hex()))
                left, top_px = _px(m.get_corner([-1, 1, 0]))
                right, bottom = _px(m.get_corner([1, -1, 0]))
                lines = max(1, str(text).count("\n") + 1)
                texts.append({"text": str(text), "box": [round(left), round(top_px),
                                                         round(right), round(bottom)],
                              "line_height": round((bottom - top_px) / lines),
                              "color": fill, "behind": behind,
                              "recorded": id(m) in recorded})
        shapes, pictures = [], []
        for top in self.mobjects:
            for m in top.get_family():
                if isinstance(m, ImageMobject):
                    left, top_px = _px(m.get_corner([-1, 1, 0]))
                    right, bottom = _px(m.get_corner([1, -1, 0]))
                    pictures.append([round(left), round(top_px), round(right), round(bottom)])
                # Its own outline: an arrow's shaft counts even though its tip is
                # a part of it.
                elif (isinstance(m, VMobject) and id(m) not in word_ids and len(m.points)
                      and (m.get_stroke_opacity() > 0.3 or m.get_fill_opacity() > 0.3)):
                    shapes.append(m)
        # Each outline followed once, not once per piece of text, in pixels.
        traced = [(m, _px_all(_trace(m))) for m in shapes]
        frame_w, frame_h = BRIEF.width, BRIEF.height
        background = [len(p) and (np.ptp(p[:, 0]) >= BACKGROUND_SHARE * frame_w
                                  and np.ptp(p[:, 1]) >= BACKGROUND_SHARE * frame_h)
                      for _, p in traced]
        drawn = [(m, p) for (m, p), back in zip(traced, background, strict=False)
                 if len(p) and not back]
        outlines = [(type(m).__name__, p) for m, p in drawn if _stroked(m)]
        crossings, on_pictures = [], []
        for piece in texts:
            x0, y0, x1, y1 = piece["box"]
            x0, y0, x1, y1 = x0 + 4, y0 + 4, x1 - 4, y1 - 4
            for name, points in outlines:
                x, y = points[:, 0], points[:, 1]
                if ((x0 < x) & (x < x1) & (y0 < y) & (y < y1)).any():
                    crossings.append({"text": piece["text"][:40], "shape": name})
            # Words laid on a picture cover what is drawn there -- often the
            # picture's own labels, which nothing here can see.
            if any(x0 < p[2] and p[0] < x1 and y0 < p[3] and p[1] < y1 for p in pictures):
                on_pictures.append(piece["text"][:40])
        collisions = self._collisions(drawn, texts)
        boxes = ([t["box"] for t in texts] + pictures
                 + [[p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()]
                    for _, p in drawn])
        extent = ([round(float(min(b[0] for b in boxes))), round(float(min(b[1] for b in boxes))),
                   round(float(max(b[2] for b in boxes))), round(float(max(b[3] for b in boxes)))]
                  if boxes else None)
        graphics = [top for top in self.mobjects
                    if not isinstance(top, text_kinds)
                    and any(id(m) not in word_ids and (isinstance(m, ImageMobject) or (
                        isinstance(m, VMobject) and len(m.points)
                        and (m.get_stroke_opacity() > 0.3 or m.get_fill_opacity() > 0.3)))
                            for m in top.get_family())]
        self._snapshots.append({"at": round(self.now, 2), "texts": texts,
                                "graphics": len(graphics), "pictures": pictures,
                                "crossings": crossings, "on_pictures": on_pictures,
                                "collisions": collisions, "extent": extent})

    @staticmethod
    def _collisions(drawn, texts) -> list[dict[str, str]]:
        """Closed outlines (boxes, circles) that run through each other -- a box laid
        half over another box. Named by the words in them, when there are any."""
        closed = [(m, p) for m, p in drawn
                  if _stroked(m) and "Tip" not in type(m).__name__
                  and np.allclose(m.points[0], m.points[-1], atol=1e-3)
                  and np.ptp(p[:, 0]) >= SMALLEST_SHAPE_PX and np.ptp(p[:, 1]) >= SMALLEST_SHAPE_PX]

        def name(m, p) -> str:
            x0, y0, x1, y1 = p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()
            words = next((t["text"][:30] for t in texts
                          if x0 < (t["box"][0] + t["box"][2]) / 2 < x1
                          and y0 < (t["box"][1] + t["box"][3]) / 2 < y1), "")
            return type(m).__name__ + (f" around “{words}”" if words else "")

        found = []
        for index, (m, p) in enumerate(closed):
            for other, q in closed[index + 1:]:
                if _cross(p, q) or _cross(q, p):
                    found.append({"a": name(m, p), "b": name(other, q)})
        return found


def run(scene_class) -> None:
    """Render the scene to `render.mp4`, and write `layout.json`."""
    with tempconfig({"pixel_width": BRIEF.width, "pixel_height": BRIEF.height,
                     "frame_rate": BRIEF.fps, "background_color": BRIEF.look["background"],
                     "media_dir": "manim_media", "output_file": "scene",
                     "disable_caching": True, "verbosity": "WARNING"}):
        scene = scene_class()
        scene.render()
        shutil.copy(scene.renderer.file_writer.movie_file_path, BRIEF.out)
    Path("layout.json").write_text(json.dumps({
        "renderer": "manim", "width": BRIEF.width, "height": BRIEF.height,
        "snapshots": scene._snapshots, "plays": scene._plays}, indent=1, ensure_ascii=False), encoding="utf-8")
