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

Shot templates -- start here: each builds a whole scene from a few slots and the
words each part arrives on, laid out, timed and moved so it passes every check:
`self.hero(picture, [(label, (x, y), cue)], title)` -- a picture and its parts
named ((x, y) are the part's place as fractions of the picture, from its
description); `self.steps([(label, picture, cue)], title)` -- an experiment or
process; `self.compare((heading, picture, [points], cue), (...), title)`;
`self.person(picture, name, line, cue)`; `self.key_idea(statement, picture, cue)`;
`self.opener(picture, title, [(line, cue)], cue)` -- a topic opened on a picture that
sets the scene (the deck's own art), not one explained part by part.

Diagrams laid out for you -- prefer them to placing boxes by hand, which is what
fails most (boxes over boxes, circles through their own labels, a diagram in one
strip of the frame): `self.flow(steps)` (boxes joined by arrows),
`self.hub(centre, around)` (one idea and what hangs off it), and
`self.timeline(events)` (things in order). Each comes back placed; reveal its
parts (.boxes/.arrows, .centre/.items/.lines, .spine/.dots/.labels) on the words.
Every scene uses the same type and moves: `self.title(text)` for its title,
`self.heading(text)` below it; bring things on with `self.play(self.reveal(x))`,
draw with `self.draw(x)`, connect with `self.grow(arrow)`, point attention with
`self.focus(target, *others)`, change one thing into another with
`self.swap(a, b)`.
A label on a picture is `self.callout(text, (x, y), side)`: beside the point it
names, joined to it by a short line from its edge -- never an arrow drawn from
the middle of a label, never a label far from its thing.

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


def _composed(template):
    """A shot template lays its scene out by construction: what it adds is not
    moved out of the way afterwards. Nudged clear of the arrow arriving with it,
    a step's panel dropped below the badge the arrow had been drawn to."""
    import functools

    @functools.wraps(template)
    def compose(self, *args, **kwargs):
        self._composing = True
        try:
            return template(self, *args, **kwargs)
        finally:
            self._composing = False
    return compose


def _trimmed(path: str) -> str:
    """The picture without its empty margin: a painted illustration came with
    a wide white border, and a hero picture fitted to its box showed a small
    drawing lost in white. A copy is kept beside the render, never in assets/."""
    import hashlib
    import tempfile

    from PIL import Image, ImageChops
    source = Path(path)
    try:
        key = hashlib.sha1(f"{source.resolve()}:{source.stat().st_mtime_ns}".encode()).hexdigest()
        out = Path(tempfile.gettempdir()) / "manimkit-trimmed" / f"{key[:16]}.png"
        if out.exists():
            return str(out)
        image = Image.open(source)
        image.load()
        if image.mode in ("RGBA", "LA") and image.getextrema()[-1][0] < 250:
            box = image.getchannel("A").point(lambda a: 255 if a > 12 else 0).getbbox()
        else:
            rgb = image.convert("RGB")
            plain = Image.new("RGB", rgb.size, rgb.getpixel((0, 0)))
            box = ImageChops.difference(rgb, plain).convert("L").point(
                lambda v: 255 if v > 24 else 0).getbbox()
        if not box:
            return path
        width, height = image.size
        pad = round(0.02 * max(width, height))
        box = (max(0, box[0] - pad), max(0, box[1] - pad),
               min(width, box[2] + pad), min(height, box[3] + pad))
        if (box[2] - box[0]) * (box[3] - box[1]) > 0.92 * width * height:
            return path
        out.parent.mkdir(parents=True, exist_ok=True)
        image.crop(box).save(out)
        return str(out)
    except OSError:
        return path

BRIEF = load_brief()
FRAME_WIDTH_UNITS = 14.222
FRAME_HEIGHT_UNITS = 8.0
# An outline is followed at most this many pixels between samples, so a 36 px line of
# words cannot fall between two of them (48 fixed samples left 30 px gaps on a long line).
SAMPLE_PX = 6.0
SMALLEST_SHAPE_PX = 40          # a dot or a marker is not a shape that collides
BACKGROUND_SHARE = 0.9          # a shape this much of the frame is a background
MOTION_SNAPSHOT_GAP = 0.25      # seconds: what each animation leaves, at most this often


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


def _point(where) -> np.ndarray:
    """(x, y), (x, y, z) or a thing's centre, as Manim's three numbers."""
    if isinstance(where, (tuple, list)) and len(where) == 2:
        return np.array([float(where[0]), float(where[1]), 0.0])
    return where.get_center() if isinstance(where, manim.Mobject) else np.asarray(where, float)


def _edge(where, toward: np.ndarray) -> np.ndarray:
    """Where the line from a thing's centre toward `toward` leaves its box. Manim's
    own choice is its furthest point that way -- on a rounded box, any corner -- and
    arrows between two level boxes came out slanted; a leader line started inside
    its own label."""
    if not isinstance(where, manim.Mobject):
        return _point(where)
    centre = where.get_center()
    dx, dy = (toward - centre)[:2]
    reach = min(where.width / 2 / abs(dx) if dx else np.inf,
                where.height / 2 / abs(dy) if dy else np.inf)
    return centre if reach == np.inf else centre + (toward - centre) * reach


def _rgb(colour: str) -> tuple[int, int, int]:
    value = colour.lstrip("#")[:6]
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def _mix(base: str, colour: str, share: float) -> str:
    """`share` of `colour` over `base`, as a colour."""
    mixed = [round(b + (c - b) * share) for b, c in zip(_rgb(base), _rgb(colour), strict=False)]
    return "#{:02x}{:02x}{:02x}".format(*mixed)


def _contrast(first: str, second: str) -> float:
    def luminance(colour: str) -> float:
        channels = [c / 255 for c in _rgb(colour)]
        linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


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
        # What each animation leaves on screen is checked too, not only the beats:
        # an arrow drawn and gone between two beats was never seen by a check.
        if not self._snapshots or self.now - self._snapshots[-1]["at"] >= MOTION_SNAPSHOT_GAP:
            self.snapshot(beat=False)

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
                if not self._composing:
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
        if not wanted:
            return self.now if default is None else default
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

    def smallest_size(self) -> int:
        return int(BRIEF.__dict__.get("smallest_text_px") or 36)

    def label(self, text: str, size: int = 44, color: str | None = None,
              at: tuple[float, float] | None = None, on: str | None = None,
              bold: bool = False, **kwargs) -> Text:
        """On-screen words, recorded for the checks. `size` is in points at 1080p;
        `on` is the colour behind the text when it sits on a panel."""
        fill = color or self.look["text"]
        # Never under the smallest the platforms allow: larger for a classroom.
        size = max(size, self.smallest_size())
        mobject = Text(text, font_size=size, color=fill,
                       weight="BOLD" if bold else "NORMAL", **kwargs)
        if at is not None:
            mobject.move_to([at[0], at[1], 0])
        # The colour asked for: Manim's get_color() reports the outline, not the fill.
        self._labels.append((mobject, text, on or self.look["background"], fill))
        return mobject

    # --- one type scale, one set of moves: every scene of a video alike ------------------

    TITLE_SIZE, HEADING_SIZE, LABEL_SIZE = 60, 46, 38
    _composing = False

    def title(self, text: str) -> Text:
        """The scene's title, always the same size, weight and place (top centre)."""
        return self.safe(self.label(text, size=self.TITLE_SIZE, bold=True, at=(0, 3.25)))

    def heading(self, text: str, at: tuple[float, float] = (0, 2.2)) -> Text:
        """A heading inside the scene: one step below the title."""
        return self.safe(self.label(text, size=self.HEADING_SIZE, bold=True, at=at))

    def reveal(self, thing, run_time: float = 0.5):
        """Bring something on: a short rise into place as it fades in."""
        from manim import UP
        return manim.FadeIn(thing, shift=UP * 0.15, run_time=run_time)

    def draw(self, thing, run_time: float = 0.8):
        """Draw an outline or a diagram stroke by stroke."""
        return manim.Create(thing, run_time=run_time)

    def grow(self, arrow, run_time: float = 0.5):
        """Grow an arrow or a connecting line from its start to its end."""
        if isinstance(arrow, manim.Arrow):
            return manim.GrowArrow(arrow, run_time=run_time)
        return manim.Create(arrow, run_time=run_time)

    def focus(self, target, *others, run_time: float = 0.6):
        """Put attention on `target`: everything in `others` dims, the target pulses."""
        from manim import AnimationGroup
        dims = [other.animate(run_time=run_time).set_opacity(0.3) for other in others]
        return AnimationGroup(*dims, manim.Indicate(target, scale_factor=1.06,
                                                    color=self.colour(0), run_time=run_time))

    def swap(self, before, after, run_time: float = 0.7):
        """One thing becoming another, in place."""
        return manim.ReplacementTransform(before, after, run_time=run_time)

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

    # --- colour ---------------------------------------------------------------------------

    def colour(self, index: int = 0) -> str:
        """The deck's accent colours in turn -- colour(0) is the main accent -- so a
        diagram's parts each have their own. Ones too faint to see on the
        background are skipped."""
        palette = list(dict.fromkeys(
            c.lower() for c in [self.look["accent"], *(self.look.get("accents") or [])]
            if _contrast(c, self.look["background"]) >= 2.0)) or [self.look["accent"]]
        return palette[index % len(palette)]

    def tint(self, colour: str, share: float = 0.16) -> str:
        """`colour` mixed into the background: a box's fill that its words still read on."""
        return _mix(self.look["background"], colour, share)

    # --- shapes that cannot get in the way of words ------------------------------------

    def boxed(self, text: str, size: int = 40, color: str | None = None, pad: float = 0.25,
              at: tuple[float, float] | None = None, stroke: str | None = None,
              fill: str | None = None):
        """Words in a box sized to them, so they can never spill out of it. Filled
        with a tint of its outline's colour, so the box reads as a thing, and a line
        behind it is covered instead of running through."""
        from manim import RoundedRectangle, VGroup
        stroke = stroke or self.colour(0)
        fill = fill or self.tint(stroke)
        label = self.label(text, size=size, color=color, on=fill)
        box = RoundedRectangle(corner_radius=0.12, width=label.width + 2 * pad,
                               height=label.height + 2 * pad, stroke_color=stroke,
                               stroke_width=5, fill_color=fill, fill_opacity=1).move_to(label)
        group = VGroup(box, label)
        if at is not None:
            group.move_to([at[0], at[1], 0])
        return group

    def connect(self, start, end, color: str | None = None, buff: float = 0.18):
        """An arrow from the edge of `start` to the edge of `end`: it never runs
        through the words or shapes it joins."""
        from manim import Arrow

        a, b = _point(start), _point(end)
        return Arrow(_edge(start, b), _edge(end, a), buff=buff, color=color or self.look["accent"],
                     stroke_width=5, max_tip_length_to_length_ratio=0.18)

    def callout(self, text: str, target, side: str = "right", size: int = 34,
                gap: float = 1.1, color: str | None = None):
        """A label beside the point it names on a picture -- `target` is (x, y) or a
        thing -- joined to it by a short leader line from the label's edge to a dot
        on the point. `side` is where the label sits: right, left, up or down. Has
        .label, .line, .dot; bring them on together when the thing is named."""
        from manim import DOWN, LEFT, RIGHT, UP, Dot, Line, VGroup
        point = _point(target)
        colour = color or self.colour(0)
        label = self.label(text, size=size)
        direction = {"right": RIGHT, "left": LEFT, "up": UP, "down": DOWN}.get(side, RIGHT)
        label.move_to(point + direction * (gap + max(label.width, label.height) / 2))
        self.safe(label)
        dot = Dot(point, radius=0.07, color=colour)
        line = Line(_edge(label, point), point, buff=0.06, color=colour, stroke_width=3)
        whole = VGroup(line, dot, label)
        whole.label, whole.line, whole.dot = label, line, dot
        return whole

    def picture(self, path: str, height: float = 3.0, at: tuple[float, float] | None = None):
        """A picture from the slides (a path from brief.assets.pictures), its empty
        margin trimmed so the size given is the size of what it shows."""
        from manim import ImageMobject
        image = ImageMobject(_trimmed(path)).set(height=height)
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
        boxes = [self.boxed(text, size=size, stroke=self.colour(i))
                 for i, text in enumerate(steps)]
        group = VGroup(*boxes).arrange(RIGHT, buff=gap).move_to([0, y, 0])
        if group.width > 2 * self.SAFE_X:
            group.arrange(DOWN, buff=gap * 0.6).move_to([0, y, 0])
        self.safe(group)
        arrows = [self.connect(a, b, color=self.look["text"])
                  for a, b in zip(boxes, boxes[1:], strict=False)]
        whole = VGroup(*boxes, *arrows)
        whole.boxes, whole.arrows = boxes, arrows
        return whole

    def hub(self, centre: str, around: list[str], y: float = -0.3, size: int = 38,
            gap: float = 1.2):
        """One idea in the middle and what hangs off it, in a column either side, each
        joined to the middle by a line from edge to edge. Has .centre, .items, .lines
        (lines[i] joins the centre to items[i])."""
        from manim import DOWN, LEFT, RIGHT, Line, VGroup
        middle = self.boxed(centre, size=size + 4, stroke=self.colour(0),
                            fill=self.tint(self.colour(0), 0.3))
        items = [self.boxed(text, size=size, stroke=self.colour(i + 1))
                 for i, text in enumerate(around)]
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
            lines.append(Line(start, end, buff=0.1, color=self.colour(index + 1),
                              stroke_width=4))
        whole = VGroup(middle, *items, *lines)
        whole.centre, whole.items, whole.lines = middle, items, lines
        return whole

    def timeline(self, events: list[str], y: float = -0.4, size: int = 36):
        """Things in order on a line, a dot and a label each. Across the frame with
        labels above and below in turn; down its left side when they do not fit across.
        Has .spine, .dots, .labels."""
        from manim import DOWN, RIGHT, UP, Dot, Line, VGroup
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
                dot = Dot([-span / 2 + (index + 0.5) * step, y, 0], radius=0.14,
                          color=self.colour(index))
                label.next_to(dot, UP if index % 2 == 0 else DOWN, buff=0.35)
                dots.append(dot)
        else:
            top, bottom = self.SAFE_Y - 1.5, -self.SAFE_Y + 0.3
            x = -self.SAFE_X + 0.6
            spine = Line([x, top, 0], [x, bottom, 0], color=self.look["text"], stroke_width=4)
            step = (top - bottom) / max(1, len(events))
            for index, label in enumerate(labels):
                dot = Dot([x, top - (index + 0.5) * step, 0], radius=0.14,
                          color=self.colour(index))
                label.next_to(dot, RIGHT, buff=0.4)
                dots.append(dot)
        whole = VGroup(spine, *dots, *labels)
        self.safe(whole)
        whole.spine, whole.dots, whole.labels = spine, dots, labels
        return whole

    # --- shot templates: a whole scene from a few slots ---------------------------------
    # Each lays out, times and moves a complete scene that passes every check by
    # construction; the program only fills the slots and names the words each part
    # arrives on (`cue`: words from the narration). End the scene with self.finish().

    def _at_cue(self, cue: str | None) -> None:
        if cue:
            self.until(self.when(cue))

    def _wrapped(self, text: str, width: float, size: int) -> Text:
        """Words broken into lines that fit `width` (scene units) at `size`,
        measured -- between words only, never inside one ("Electroc/hemical"); a
        word wider than the line sets the type smaller, down to the smallest."""
        size = max(size, self.smallest_size())
        words = text.split() or [text]
        widest = max(Text(word, font_size=size).width for word in words)
        if widest > width:
            size = max(self.smallest_size(), int(size * width / widest))
        lines: list[str] = []
        for word in words:
            trial = f"{lines[-1]} {word}" if lines else word
            if lines and Text(trial, font_size=size).width <= width:
                lines[-1] = trial
            else:
                lines.append(word)
        return self.label("\n".join(lines), size=size)

    def _fit(self, path: str, width: float, height: float, at: tuple[float, float]):
        image = self.picture(path, height=1.0)
        image.scale(min(width / image.width, height / image.height))
        image.move_to([at[0], at[1], 0])
        return image

    @_composed
    def hero(self, picture: str, callouts: list, title: str = "", cue: str | None = None,
             moves: list | None = None):
        """One picture, large, and its parts named on it: `callouts` are
        (label, (x, y), cue) with (x, y) the part's place as fractions of the
        picture from its top left -- the picture's description gives them. The
        labels stand in a column beside the picture -- both sides, picture centred,
        when the parts are spread across it -- each joined to its part by a line
        that crosses the picture level and bends only in the gutter, so no two
        lines cross. `moves` are ([(x, y), ...], cue): a pulse runs along those
        points of the picture on the cue -- a signal travelling, liquid carried."""
        from manim import Dot, VMobject
        top = 2.55 if title else 3.3
        if title:
            self.play(self.reveal(self.title(title)))
        xs = [fx for _, (fx, _), _ in callouts]
        both = len(callouts) > 1 and min(xs) < 0.4 and max(xs) > 0.6
        middle = (top - 3.3) / 2
        # Each label column as wide as its longest word. Labels both sides only
        # when that still leaves the picture nearly as large as one column would:
        # the picture is the scene, the labels serve it.
        longest = max((Text(word, font_size=max(self.LABEL_SIZE, self.smallest_size())).width
                       for text, _, _ in callouts for word in text.split()), default=2.0)
        room = max(2.4, longest + 0.15)
        from PIL import Image as _Image
        with _Image.open(_trimmed(picture)) as opened:
            aspect = opened.width / max(1, opened.height)
        tall = top + 3.3
        centred = min(6.8, 2 * (self.SAFE_X - 0.85 - room))
        beside = 2 * self.SAFE_X - 0.85 - room
        both = both and min(centred, tall * aspect) >= 0.8 * min(beside, tall * aspect)
        if both:
            image = self._fit(picture, centred, tall, (0.0, middle))
        else:
            image = self._fit(picture, beside, tall, (0.0, middle))
            # The picture and its label column centred together: a tall picture
            # held to the left edge left most of the frame empty beside it.
            widest = max((Text(text, font_size=max(self.LABEL_SIZE, self.smallest_size())).width
                          for text, _, _ in callouts), default=0.0)
            column = min(widest, 2 * self.SAFE_X - image.width - 0.85) + 0.85 if callouts else 0
            image.align_to([max(-self.SAFE_X, -(image.width + column) / 2), 0, 0], manim.LEFT)
        self._at_cue(cue)
        self.play(manim.FadeIn(image, scale=0.96, run_time=0.7))
        sides = {1: [], -1: []}
        for text, (fx, fy), part_cue in callouts:
            sides[-1 if both and fx < 0.5 else 1].append((text, fx, fy, part_cue))
        placed = []
        for side, items in sides.items():
            edge = (image.get_right() if side > 0 else image.get_left())[0]
            gutter, column = edge + side * 0.15, edge + side * 0.85
            room = self.SAFE_X - abs(column)
            items = sorted(items, key=lambda c: c[2])
            points = [np.array([image.get_left()[0] + fx * image.width,
                                image.get_top()[1] - fy * image.height, 0.0])
                      for _, fx, fy, _ in items]
            labels = [self._wrapped(text, room, self.LABEL_SIZE) for text, *_ in items]
            for label, y in zip(labels, self._stacked(labels, [p[1] for p in points], top),
                                strict=True):
                label.move_to([column + side * label.width / 2, y, 0])
            for (_, _, _, part_cue), point, label in zip(items, points, labels, strict=True):
                y = label.get_center()[1]
                start = np.array([column - side * 0.08, y, 0.0])
                # Level across the picture at the part's height, bent only in the
                # gutter: labels keep the parts' order, so no two lines cross.
                line = VMobject(stroke_width=4).set_points_as_corners(
                    [start, [gutter, point[1], 0.0], point])
                placed.append((label, point, line, part_cue))
        def at(fx: float, fy: float):
            return np.array([image.get_left()[0] + fx * image.width,
                             image.get_top()[1] - fy * image.height, 0.0])

        events = [(self.when(c or ""), "callout", (label, point, line))
                  for label, point, line, c in placed]
        events += [(self.when(c or ""), "move", [at(*xy) for xy in path])
                   for path, c in (moves or []) if len(path) > 1]
        named = 0
        for moment, kind, what in sorted(events, key=lambda e: e[0]):
            self.until(moment)
            if kind == "move":
                self._travel(what)
                continue
            label, point, line = what
            colour = self.colour(named)
            named += 1
            # A halo of the background under the line, as a textbook plate
            # draws it: a leader crossing the drawing stays readable.
            line.set_stroke(colour, width=4).set_stroke(self.look["background"], width=11,
                                                       background=True)
            dot = Dot(point, radius=0.09, color=colour)
            self.play(self.draw(line, run_time=0.45), manim.FadeIn(dot, scale=2.2),
                      self.reveal(label, run_time=0.45))
            self.play(manim.Flash(point, color=colour, line_length=0.22, num_lines=10,
                                  flash_radius=0.3, run_time=0.5))

    def _travel(self, points: list) -> None:
        """A glowing pulse runs along `points` over the picture -- a signal down a
        nerve, current through a wire, liquid carried across -- and leaves nothing
        behind: what it shows is the movement."""
        from manim import Dot, MoveAlongPath, ShowPassingFlash, VGroup, VMobject
        path = VMobject().set_points_smoothly([np.array(p) for p in points])
        length = sum(np.linalg.norm(np.array(b) - np.array(a))
                     for a, b in zip(points, points[1:], strict=False))
        colour = self.look.get("accent") or self.colour(0)
        trail = path.copy().set_stroke(colour, width=10)
        glow = Dot(points[0], radius=0.22, color=colour, fill_opacity=0.35)
        pulse = VGroup(glow, Dot(points[0], radius=0.11, color=colour))
        seconds = min(2.4, max(1.0, length / 3))
        self.play(manim.FadeIn(pulse, scale=0.5, run_time=0.2))
        self.play(MoveAlongPath(pulse, path), ShowPassingFlash(trail, time_width=0.5),
                  run_time=seconds, rate_func=manim.linear)
        self.play(manim.FadeOut(pulse, scale=1.8, run_time=0.3))

    def _stacked(self, labels: list, wanted: list[float], top: float) -> list[float]:
        """Heights for a column of labels, in order, each as near the part it
        names as the others allow: spread evenly around the parts, not pushed
        only downward -- a pile-up below the picture made long bent lines."""
        gap = 0.25
        ys: list[float] = []
        for label, want in zip(labels, wanted, strict=True):
            limit = (ys[-1] - labels[len(ys) - 1].height / 2 - gap - label.height / 2
                     if ys else want)
            ys.append(min(want, limit))
        if ys:
            ys = [y + sum(w - y for w, y in zip(wanted, ys, strict=True)) / len(ys)
                  for y in ys]
            high = ys[0] + labels[0].height / 2 - top
            low = -self.SAFE_Y - (ys[-1] - labels[-1].height / 2)
            ys = [y - max(0.0, high) + max(0.0, low) for y in ys]
        return ys

    @_composed
    def steps(self, steps: list, title: str = ""):
        """Two to four steps in order -- an experiment, a process: `steps` are
        (label, picture or None, cue). Each arrives numbered, in its own panel,
        joined to the one before by an arrow."""
        from manim import Circle, Group
        if title:
            self.play(self.reveal(self.title(title)))
        count = max(1, len(steps))
        width = (2 * self.SAFE_X - (count - 1) * 0.5) / count
        top = 2.45 if title else 3.2
        # A picture for every step stands over its own step; fewer than that, the
        # first stands once over them all -- one panel with a picture, the rest
        # empty, looked lopsided.
        each = all(picture for _, picture, _ in steps)
        shared = next((picture for _, picture, _ in steps if picture), None)
        if shared and not each:
            self.play(manim.FadeIn(self._fit(shared, 7.0, top + 0.6, (0, (top - 1.2) / 2 + 0.3)),
                                   run_time=0.6))
        # With no picture the row stands mid-frame, not under an empty top half.
        badge_y = -1.55 if shared else 0.6
        panels = []
        for index, (text, picture, cue) in enumerate(steps):
            x = -self.SAFE_X + width / 2 + index * (width + 0.5)
            parts = []
            if picture and each:
                parts.append(self._fit(picture, width - 0.2, top + 0.6, (x, (top - 1.2) / 2 + 0.3)))
            colour = self.colour(index)
            badge = Circle(radius=0.34, color=colour, fill_color=self.tint(colour, 0.25),
                           fill_opacity=1, stroke_width=4).move_to([x, badge_y, 0])
            number = self.label(str(index + 1), size=self.LABEL_SIZE, on=self.tint(colour, 0.25),
                                bold=True).move_to(badge)
            words = self._wrapped(text, width - 0.1, self.LABEL_SIZE)
            words.next_to(badge, manim.DOWN, buff=0.3)
            panels.append((Group(*parts, badge, number, words), badge, cue))
        for index, (panel, badge, cue) in enumerate(panels):
            self._at_cue(cue)
            moves = [self.reveal(panel)]
            if index:
                moves.append(self.grow(self.connect(panels[index - 1][1], badge,
                                                    color=self.look["text"])))
            self.play(*moves)

    @_composed
    def compare(self, left: tuple, right: tuple, title: str = ""):
        """Two sides set against each other: each (heading, picture or None,
        [up to three short points], cue)."""
        from manim import Line
        if title:
            self.play(self.reveal(self.title(title)))
        top = 2.3 if title else 3.0
        self.play(self.draw(Line([0, top + 0.2, 0], [0, -3.2, 0], color=self.look["dim"],
                                 stroke_width=3), run_time=0.4))
        for side, (heading, picture, points, cue) in ((-1, left), (1, right)):
            x = side * 3.25
            colour = self.colour(0 if side < 0 else 1)
            # Words in an accent only where the accent reads; else in the ink.
            readable = _contrast(colour, self.look["background"]) >= 4.5
            ink = colour if readable else self.look["text"]
            parts = [self.label(heading, size=self.HEADING_SIZE, bold=True, color=ink,
                                at=(x, top))]
            y = top - 0.6
            if picture:
                image = self._fit(picture, 5.6, 2.6, (x, y - 1.3))
                parts.append(image)
                y = image.get_bottom()[1] - 0.2
            for point in points[:3]:
                words = self._wrapped(point, 5.8, 36)
                words.move_to([x, y - words.height / 2, 0])
                y = words.get_bottom()[1] - 0.25
                parts.append(words)
            self._at_cue(cue)
            self.play(*[self.reveal(part) for part in parts])

    @_composed
    def person(self, picture: str, name: str, line: str, cue: str | None = None,
               line_cue: str | None = None):
        """A person: their portrait, their name, and one line on what they did."""
        portrait = self._fit(picture, 5.2, 5.8, (-3.4, -0.2))
        named = self.label(name, size=self.TITLE_SIZE - 6, bold=True)
        named.move_to([0.3 + named.width / 2, 1.3, 0])
        self.safe(named)
        said = self._wrapped(line, 5.6, self.LABEL_SIZE)
        said.move_to([0.3 + said.width / 2, named.get_bottom()[1] - 0.45 - said.height / 2, 0])
        self._at_cue(cue)
        self.play(manim.FadeIn(portrait, run_time=0.6), self.reveal(named))
        self._at_cue(line_cue)
        self.play(self.reveal(said))

    @_composed
    def key_idea(self, statement: str, picture: str | None = None, cue: str | None = None):
        """One idea to remember, large, with a line drawn under it -- and a picture
        beside it when there is one."""
        from manim import Line
        if picture:
            image = self._fit(picture, 5.6, 5.8, (3.4, -0.1))
            words = self._wrapped(statement, 6.4, 50)
            words.move_to([-3.2, 0.2, 0])
        else:
            image, words = None, self._wrapped(statement, 11.5, 56)
            words.move_to([0, 0.3, 0])
        self.safe(words)
        rule = Line(words.get_corner(manim.DL) + np.array([0, -0.35, 0]),
                    words.get_corner(manim.DR) + np.array([0, -0.35, 0]),
                    color=self.colour(0), stroke_width=6)
        self._at_cue(cue)
        self.play(self.reveal(words), *([manim.FadeIn(image, run_time=0.6)] if image else []))
        self.play(self.draw(rule, run_time=0.6))

    @_composed
    def opener(self, picture: str, title: str, lines: list | None = None,
               cue: str | None = None):
        """A topic opened on a picture that sets the scene -- the deck's own art, a
        cover, a portrait of the era -- rather than one explained part by part: the
        picture large on one side (across the top when it is a banner), slowly
        drawing nearer, the topic's title beside it and up to three short `lines`,
        each (text, cue), arriving on their words."""
        from manim import Dot, Line
        from PIL import Image as _Image
        with _Image.open(_trimmed(picture)) as opened:
            aspect = opened.width / max(1, opened.height)
        banner = aspect >= 1.9
        if banner:
            image = self._fit(picture, 2 * self.SAFE_X - 0.6, 2.9, (0.0, 1.75))
            left, width, top = -self.SAFE_X + 0.2, 2 * self.SAFE_X - 0.4, \
                image.get_bottom()[1] - 0.35
        else:
            image = self._fit(picture, 5.4, 6.2, (3.25, -0.05))
            left, width, top = -self.SAFE_X + 0.1, 5.9, 2.3
        heading = self._wrapped(title, width, self.TITLE_SIZE - 8)
        heading.move_to([left + heading.width / 2, top - heading.height / 2, 0])
        rule = Line([left, heading.get_bottom()[1] - 0.25, 0],
                    [left + min(width, max(2.5, heading.width)), heading.get_bottom()[1] - 0.25, 0],
                    color=self.colour(0), stroke_width=6)
        placed, y = [], rule.get_center()[1] - 0.45
        for index, (text, line_cue) in enumerate((lines or [])[:3]):
            words = self._wrapped(text, width - 0.6, self.LABEL_SIZE)
            words.move_to([left + 0.55 + words.width / 2, y - words.height / 2, 0])
            dot = Dot([left + 0.2, words.get_top()[1] - 0.22, 0], radius=0.09,
                      color=self.colour(index + 1))
            placed.append((manim.VGroup(dot, words), line_cue))
            y = words.get_bottom()[1] - 0.35
        self._at_cue(cue)
        self.play(manim.FadeIn(image, scale=0.94, run_time=0.8), self.reveal(heading))
        self.play(self.draw(rule, run_time=0.5))
        grown = 1.0
        for group, line_cue in placed:
            grown = self._drift(image, self.when(line_cue) if line_cue else self.now, grown)
            self.play(self.reveal(group))
        self._drift(image, min(BRIEF.seconds - 0.1, self.now + 4.0), grown)

    def _drift(self, image, until: float, grown: float) -> float:
        """The picture drawing slowly nearer until `until` -- the waiting is
        movement -- never more than six percent in all. Returns how far it has grown."""
        seconds = until - self.now
        if seconds < 0.3 or grown >= 1.06:
            if seconds > 0.02:
                self.until(until)
            return grown
        step = min(1.06 / grown, 1 + 0.01 * seconds)
        self.play(image.animate.scale(step), run_time=seconds, rate_func=manim.linear)
        self.snapshot()
        return grown * step

    # --- what is on screen, for the checks ------------------------------------------------

    def snapshot(self, beat: bool = True) -> None:
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
        self._snapshots.append({"at": round(self.now, 2), "beat": beat, "texts": texts,
                                "graphics": len(graphics), "pictures": pictures,
                                "crossings": crossings, "on_pictures": on_pictures,
                                "collisions": collisions, "extent": extent})

    @staticmethod
    def _collisions(drawn, texts) -> list[dict[str, str]]:
        """Closed outlines (boxes, circles) that run through each other -- a box laid
        half over another box -- and lines or arrows that run through a box rather
        than stopping at its edge. Named by the words in them, when there are any."""
        outlined = [(m, p) for m, p in drawn if _stroked(m) and "Tip" not in type(m).__name__]
        closed = [(m, p) for m, p in outlined
                  if np.allclose(m.points[0], m.points[-1], atol=1e-3)
                  and np.ptp(p[:, 0]) >= SMALLEST_SHAPE_PX and np.ptp(p[:, 1]) >= SMALLEST_SHAPE_PX]
        lines = [(m, p) for m, p in outlined
                 if not np.allclose(m.points[0], m.points[-1], atol=1e-3)]

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
        # A line that starts or ends at a box's edge is clear of it; one that goes in
        # and comes out again -- or ends inside -- runs over what the box holds.
        for m, p in lines:
            for other, q in closed:
                if _cross(p, q):
                    found.append({"a": type(m).__name__, "b": name(other, q)})
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
        "snapshots": scene._snapshots, "plays": scene._plays}, indent=1, ensure_ascii=False),
        encoding="utf-8")
