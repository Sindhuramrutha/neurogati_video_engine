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
`self.hero(picture, [(label, (x, y), cue, box, style)], title)` -- a picture and the
parts the narration teaches pointed out ((x, y) and box are the part's place as
fractions of the picture, from its description; style is tag, glow, zoom, lens,
sketch or caption -- a person is always named by a caption);
`self.steps([(label, picture, cue)], title)` -- an experiment or process;
`self.compare((heading, picture, [points], cue), (...), title)`;
`self.person(picture, name, line, cue)`; `self.key_idea(statement, picture, cue)`;
`self.opener(picture, title, [(line, cue)], cue)` -- a topic opened on a picture that
sets the scene (the deck's own art), not one explained part by part.

Every template and diagram takes `layout={name: (x, y) or (x, y, width)}`: the
centre of each of its parts (a picture's width too), in scene units with (0, 0) the
frame's middle. A part named there is put there; one left out is worked out, and
where every part went is written to `decisions.json`, so a program written from
shots can carry each place as a number (scene_bake). A cue is the narration's words
or the second itself (`at=12.4`, `cue=12.4`); entries may be written as dicts
(`dict(label=..., point=..., at=..., part=..., style=...)`) or as tuples.

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
the middle of a label, never a label far from its thing. Point out only what is
being taught, at most three things on a picture: a frame never crowded.

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


def _recorded(template, composing: bool = False):
    """A template or diagram that takes `layout={name: (x, y) or (x, y, width)}` --
    where each of its pictures, titles, tags and cards goes -- and records where it
    put every one (`decisions.json`), so the program can carry them as numbers: a
    place the program gives is used as given, one it leaves out is worked out."""
    import functools

    @functools.wraps(template)
    def record(self, *args, layout: dict | None = None, **kwargs):
        before = (self._composing, self._fixed, self._made)
        self._fixed, self._made = dict(layout or {}), {}
        if composing:
            self._composing = True
        try:
            return template(self, *args, **kwargs)
        finally:
            self._decisions.append({"call": template.__name__, "layout": self._made})
            self._composing, self._fixed, self._made = before
    return record


def _composed(template):
    """A shot template lays its scene out by construction: what it adds is not
    moved out of the way afterwards. Nudged clear of the arrow arriving with it,
    a step's panel dropped below the badge the arrow had been drawn to."""
    return _recorded(template, composing=True)


def _entry(item, keys: tuple[str, ...]) -> tuple:
    """An entry written as a dict (`dict(label=..., at=...)`), as the program does,
    or as a tuple in the same order."""
    if isinstance(item, dict):
        return tuple(item.get(key) for key in keys)
    return tuple(item) + (None,) * (len(keys) - len(item))


def _trim_box(path: str) -> tuple[int, int, int, int, int, int] | None:
    """Where the picture's drawing is, without its empty margin, as (left, top,
    right, bottom, width, height) in pixels; None when there is no margin to cut."""
    from PIL import Image, ImageChops
    try:
        image = Image.open(path)
        image.load()
    except OSError:
        return None
    if image.mode in ("RGBA", "LA") and image.getextrema()[-1][0] < 250:
        box = image.getchannel("A").point(lambda a: 255 if a > 12 else 0).getbbox()
    else:
        rgb = image.convert("RGB")
        plain = Image.new("RGB", rgb.size, rgb.getpixel((0, 0)))
        box = ImageChops.difference(rgb, plain).convert("L").point(
            lambda v: 255 if v > 24 else 0).getbbox()
    if not box:
        return None
    width, height = image.size
    pad = round(0.02 * max(width, height))
    box = (max(0, box[0] - pad), max(0, box[1] - pad),
           min(width, box[2] + pad), min(height, box[3] + pad))
    if (box[2] - box[0]) * (box[3] - box[1]) > 0.92 * width * height:
        return None
    return (*box, width, height)


def _in_trimmed(path: str, fx: float, fy: float) -> tuple[float, float]:
    """A place given as fractions of the whole picture, as fractions of the trimmed
    one that is shown: the parts are located on the whole picture, and a pointer
    read against the trimmed one landed off its part by the width of the margin."""
    box = _trim_box(path)
    if box is None:
        return fx, fy
    left, top, right, bottom, width, height = box
    return ((fx * width - left) / max(1, right - left),
            (fy * height - top) / max(1, bottom - top))


def _trimmed(path: str) -> str:
    """The picture without its empty margin: a painted illustration came with
    a wide white border, and a hero picture fitted to its box showed a small
    drawing lost in white. A copy is kept beside the render, never in assets/."""
    import hashlib
    import tempfile

    from PIL import Image
    source = Path(path)
    try:
        key = hashlib.sha1(f"{source.resolve()}:{source.stat().st_mtime_ns}".encode()).hexdigest()
        out = Path(tempfile.gettempdir()) / "manimkit-trimmed" / f"{key[:16]}.png"
        if out.exists():
            return str(out)
        box = _trim_box(path)
        if box is None:
            return path
        out.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as image:
            image.crop(box[:4]).save(out)
        return str(out)
    except OSError:
        return path


def _scenic(path: str) -> bool:
    """A painting with its own setting -- opaque, landscape, no empty margin round
    its subject -- is a scene, shown edge to edge; anything else stands on the
    scene's background. v7 boxed every such painting inside the frame."""
    from PIL import Image
    try:
        with Image.open(path) as image:
            image.load()
            alpha = image.getchannel(image.mode[-1]) if image.mode in ("RGBA", "LA") else None
            if alpha is not None and alpha.getextrema()[0] < 250:
                return False
            landscape = image.width / max(1, image.height) >= 1.4
    except OSError:
        return False
    return landscape and _trim_box(path) is None


def _drawn_share(source: str, image):
    """For a cut-out picture shown as `image`: a function giving how much of a box
    (scene units) lies over what is drawn, 0 to 1 -- its own transparency says where
    it is empty. None when the picture has no transparency."""
    from PIL import Image
    try:
        with Image.open(source) as opened:
            if opened.mode not in ("RGBA", "LA"):
                return None
            mask = np.asarray(opened.getchannel(opened.mode[-1]).reduce(4)) > 40
    except OSError:
        return None
    rows, cols = mask.shape
    left, top = image.get_left()[0], image.get_top()[1]
    width, height = image.width, image.height

    def share(box, own=None) -> float:
        x0 = int(np.clip((box[0] - left) / width * cols, 0, cols))
        x1 = int(np.clip((box[2] - left) / width * cols, 0, cols))
        y0 = int(np.clip((top - box[3]) / height * rows, 0, rows))
        y1 = int(np.clip((top - box[1]) / height * rows, 0, rows))
        area = max(1, (x1 - x0) * (y1 - y0))
        drawn = mask[y0:y1, x0:x1].astype(float)
        if own is not None:
            # Its own part costs less than another figure -- "Described by Broca" lay
            # on his patient -- but still costs: on the brain it named, a tag hid it.
            ox0 = int(np.clip((own[0] - left) / width * cols, 0, cols)) - x0
            ox1 = int(np.clip((own[2] - left) / width * cols, 0, cols)) - x0
            oy0 = int(np.clip((top - own[3]) / height * rows, 0, rows)) - y0
            oy1 = int(np.clip((top - own[1]) / height * rows, 0, rows)) - y0
            drawn[max(0, oy0):max(0, oy1), max(0, ox0):max(0, ox1)] *= 0.4
        whole = (box[2] - box[0]) * (box[3] - box[1])
        inside = max(0.0, min(box[2], left + width) - max(box[0], left)) * max(
            0.0, min(box[3], top) - max(box[1], top - height))
        return float(drawn.sum()) / area * (inside / max(whole, 1e-6))
    return share


def _softened(path: str, made_from: str = "") -> str:
    """A painting made for the scene that kept its own ground (its subject could not
    be cut out), with edges feathered into whatever lies behind it: v9 showed such
    paintings as rectangles on the backdrop, a picture inside the picture. A deck
    picture -- a book's cover -- keeps its edges: it is an object with a shape."""
    import hashlib
    import tempfile

    from PIL import Image, ImageDraw, ImageFilter
    if not Path(made_from or path).name.startswith("illustration-"):
        return path
    try:
        with Image.open(path) as opened:
            opened.load()
            alpha = opened.getchannel(opened.mode[-1]) if opened.mode in ("RGBA", "LA") else None
            if alpha is not None and alpha.getextrema()[0] < 250:
                return path                       # cut out already: nothing to soften
            image = opened.convert("RGBA")
        key = hashlib.sha1(f"{Path(path).resolve()}:{Path(path).stat().st_mtime_ns}".encode())
        out = Path(tempfile.gettempdir()) / "manimkit-softened" / f"{key.hexdigest()[:16]}.png"
        if out.exists():
            return str(out)
        width, height = image.size
        soft = round(0.06 * min(width, height))
        mask = Image.new("L", image.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (soft, soft, width - soft, height - soft), radius=soft * 2, fill=255)
        image.putalpha(mask.filter(ImageFilter.GaussianBlur(soft * 0.8)))
        out.parent.mkdir(parents=True, exist_ok=True)
        image.save(out)
        return str(out)
    except OSError:
        return path


def _box_of(m) -> tuple[float, float, float, float]:
    """(left, bottom, right, top) in scene units."""
    return (m.get_left()[0], m.get_bottom()[1], m.get_right()[0], m.get_top()[1])


def _overlap_area(a, b, gap: float = 0.0) -> float:
    """How much of box `a`, grown by `gap` all round, lies on box `b`."""
    wide = min(a[2] + gap, b[2]) - max(a[0] - gap, b[0])
    high = min(a[3] + gap, b[3]) - max(a[1] - gap, b[1])
    return max(0.0, wide) * max(0.0, high)


def _round_crop(source: str, box, ground: str) -> str:
    """The part of a picture inside `box` (fractions), squared round its middle and
    cut to a disc with a soft edge, on `ground` where the picture is empty -- the
    glass of a lens. Kept beside the picture."""
    from PIL import Image, ImageDraw, ImageFilter
    left, top, right, bottom = box
    out = Path(source).with_name(f"{Path(source).stem}-lens-{left:.3f}-{top:.3f}-"
                                 f"{right:.3f}-{bottom:.3f}.png")
    if out.exists():
        return str(out)
    with Image.open(source) as opened:
        image = opened.convert("RGBA")
    width, height = image.size
    x, y = (left + right) / 2 * width, (top + bottom) / 2 * height
    side = max((right - left) * width, (bottom - top) * height) * 1.25
    part = image.crop((round(x - side / 2), round(y - side / 2),
                       round(x + side / 2), round(y + side / 2))).resize((600, 600))
    glass = Image.new("RGBA", (600, 600), (*_rgb(ground), 255))
    glass.alpha_composite(part)
    mask = Image.new("L", (600, 600), 0)
    ImageDraw.Draw(mask).ellipse((6, 6, 594, 594), fill=255)
    glass.putalpha(mask.filter(ImageFilter.GaussianBlur(2)))
    glass.save(out)
    return str(out)


def _loop(own, colour: str, seed: int):
    """A loop drawn round a part as a hand draws one: a little uneven, its end running
    on past its start. A mark of attention, not a shape of the layout."""
    from manim import VMobject
    rng = np.random.default_rng(seed + 7)
    x, y = (own[0] + own[2]) / 2, (own[1] + own[3]) / 2
    across, up = (own[2] - own[0]) / 2 * 1.15 + 0.25, (own[3] - own[1]) / 2 * 1.15 + 0.2
    start = rng.uniform(0, 2 * np.pi)
    phase = rng.uniform(0, 2 * np.pi, 2)
    angles = np.linspace(start, start + 2 * np.pi * 1.12, 64)
    wobble = 1 + 0.04 * np.sin(2 * angles + phase[0]) + 0.025 * np.sin(3 * angles + phase[1])
    wobble += np.linspace(0, 0.06, len(angles))          # the second pass a little wider
    loop = VMobject(stroke_color=colour, stroke_width=6).set_points_smoothly(
        [[x + across * w * np.cos(a), y + up * w * np.sin(a), 0]
         for a, w in zip(angles, wobble, strict=True)])
    loop.attention = True
    return loop


def _cone(own, rim, colour: str):
    """A small ring on the part and two faint lines from it to the lens's rim: where
    the enlarged view comes from."""
    from manim import Circle, Line, VGroup
    centre = np.array([(own[0] + own[2]) / 2, (own[1] + own[3]) / 2, 0.0])
    radius = max(own[2] - own[0], own[3] - own[1]) / 2 + 0.12
    ring = Circle(radius=radius, color=colour, stroke_width=3).move_to(centre)
    far = rim.get_center()
    across = far - centre
    across = np.array([-across[1], across[0], 0.0]) / (np.linalg.norm(across) or 1.0)
    sides = [Line(centre + sign * across * radius, far + sign * across * rim.width / 2,
                  color=colour, stroke_width=2, stroke_opacity=0.6) for sign in (1, -1)]
    cone = VGroup(ring, *sides)
    for mark in cone.get_family():
        mark.attention = True
    return cone


BRIEF = load_brief()


def _typeface(look) -> str | None:
    """The deck's own body font when it is installed, else a clean sans: every word
    of v7 was drawn in Manim's default serif, the look's font never passed on."""
    try:
        import manimpango
        installed = set(manimpango.list_fonts())
    except Exception:              # no font list: Manim's own default
        return None
    return next((name for name in (look.get("body_font"), "Segoe UI", "Calibri",
                                   "Arial") if name and name in installed), None)


FONT = _typeface(BRIEF.look)
if FONT:
    Text.set_default(font=FONT)
    manim.MarkupText.set_default(font=FONT)
FRAME_WIDTH_UNITS = 14.222
FRAME_HEIGHT_UNITS = 8.0
# An outline is followed at most this many pixels between samples, so a 36 px line of
# words cannot fall between two of them (48 fixed samples left 30 px gaps on a long line).
SAMPLE_PX = 6.0
SMALLEST_SHAPE_PX = 40          # a dot or a marker is not a shape that collides
BACKGROUND_SHARE = 0.9          # a shape this much of the frame is a background
MOTION_SNAPSHOT_GAP = 0.25      # seconds: what each animation leaves, at most this often
_LINES: dict[tuple[int, bool], float] = {}


def _line_px(size: int, bold: bool = False) -> float:
    """How tall a line of type is at `size`, in pixels: measured on 'Hg' -- a word's own
    letters ('ocean' has no ascender) say nothing of the size it is set in."""
    if (size, bold) not in _LINES:
        line = Text("Hg", font_size=size, weight="BOLD" if bold else "NORMAL").height
        _LINES[(size, bold)] = line * BRIEF.height / FRAME_HEIGHT_UNITS
    return _LINES[(size, bold)]
BACKDROP_WASH = 0.28            # the page's colour over every painted backdrop
WORDS_WASH = 0.45               # and over that, under a shot carried by words


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
        self._panels: set[int] = set()        # words on their own tag or band
        self._snapshots: list[dict] = []
        self._decisions: list[dict] = []      # where each template put what it placed
        self._spoken = BRIEF.__dict__.get("words") or []
        self._flat = [(i, w) for i, timed in enumerate(self._spoken)
                      for w in _words(timed.get("text", ""))]
        self._narration = _words(BRIEF.narration)
        self._backdrop = self._background()
        if self._backdrop is not None:
            self.add(self._backdrop)

    @property
    def shown(self) -> list:
        """What is on screen, without the background under it: that is the frame's
        ground, not something laid out on it."""
        return [m for m in self.mobjects if m is not self._backdrop]

    def clear(self):
        """Everything off the screen but the background, which stays across shots."""
        super().clear()
        if self._backdrop is not None:
            self.add(self._backdrop)
        return self

    def _background(self):
        """The scene's background (`brief.background`): painted art, stretched to the
        frame, or a gradient -- split into coloured sections when asked. None when the
        scene has none or a person switched it off."""
        from manim import DOWN, RIGHT, Group, ImageMobject, Polygon, Rectangle, VGroup
        found = BRIEF.__dict__.get("background")
        if not found:
            return None
        width, height = FRAME_WIDTH_UNITS + 0.05, FRAME_HEIGHT_UNITS + 0.05
        if found.get("kind") == "image":
            layer = ImageMobject(found["path"])
            layer.stretch_to_fit_width(width).stretch_to_fit_height(height)
            # The ground, edge to edge: never shrunk into the margin like a picture
            # laid on it -- every painted backdrop of v7 sat inside a white border.
            layer.scenic = True
            # Under a soft wash of the page's own colour: a ground recedes behind the
            # words and pictures on it -- v7's busy rooms fought the text.
            wash = Rectangle(width=width, height=height, stroke_width=0)
            wash.set_fill(self.look["background"], opacity=BACKDROP_WASH)
            ground = Group(layer, wash).set_z_index(-100)
            ground.scenic = True
            return ground
        colours = list(found.get("colours") or []) or [self.look["background"]]
        base = Rectangle(width=width, height=height, stroke_width=0)
        base.set_fill(colours if len(colours) > 1 else colours[0], opacity=1)
        base.set_sheen_direction(RIGHT + DOWN)
        parts = [base]
        panel = found.get("panel") or colours[-1]
        half_w, half_h = width / 2, height / 2
        corners = {
            "left": [(-half_w, half_h), (-half_w / 3, half_h), (-half_w / 3, -half_h),
                     (-half_w, -half_h)],
            "right": [(half_w / 3, half_h), (half_w, half_h), (half_w, -half_h),
                      (half_w / 3, -half_h)],
            "top": [(-half_w, half_h), (half_w, half_h), (half_w, half_h / 2),
                    (-half_w, half_h / 2)],
            "bottom": [(-half_w, -half_h / 2), (half_w, -half_h / 2), (half_w, -half_h),
                       (-half_w, -half_h)],
            "diagonal": [(half_w * 0.2, half_h), (half_w, half_h), (half_w, -half_h),
                         (-half_w * 0.3, -half_h)],
        }.get(found.get("split") or "none")
        if corners:
            parts.append(Polygon(*[[x, y, 0] for x, y in corners], stroke_width=0)
                         .set_fill(panel, opacity=1))
        return VGroup(*parts).set_z_index(-100)

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
            # A painting shown edge to edge is the scene's ground: never shrunk into
            # the margin, never moved out of the way of words.
            if getattr(mobject, "scenic", False):
                continue
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
        words = {id(part) for top in self.shown for m in top.get_family()
                 if isinstance(m, TEXT_KINDS) for part in m.get_family()}
        traces = [_trace(m) for top in self.shown for m in top.get_family()
                  if id(m) not in skip and id(m) not in words and isinstance(m, VMobject)
                  and len(m.points) and _stroked(m)]
        return np.vstack(traces) if traces else np.zeros((0, 2))

    def _clear_of_words(self, mobject, own: set[int]) -> None:
        """Move `mobject` up or down to the nearest place where its words land
        neither on words already on screen, nor on a picture (whose own words
        cannot be seen from here), nor on a line, arrow or outline, staying
        inside the margin."""
        others = self._boxes(self.shown, own | self._leaving, solid=True)
        if not any(isinstance(m, manim.ImageMobject) for m in mobject.get_family()):
            others += [(m.get_left()[0], m.get_bottom()[1], m.get_right()[0], m.get_top()[1])
                       for top in self.shown for m in top.get_family()
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
        if isinstance(phrase, (int, float)):
            return float(phrase)              # the second itself, as the program writes it
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
        """The smallest font size whose line is as tall as the platforms allow
        (`smallest_text_px`, in pixels; larger for a classroom). It was taken as a
        font size, which drew every word about 60% larger than legibility needs."""
        floor = int(BRIEF.__dict__.get("smallest_text_px") or 36)
        return next((size for size in range(12, 96) if _line_px(size) >= floor), floor)

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
        # What the check measures it by: its size, and its height as set.
        mobject.kit_type = (size, bold, mobject.height)
        # Over painted art, a soft halo of the light ground under the letters: the
        # words stay readable over whatever part of the painting they cross.
        background = BRIEF.__dict__.get("background") or {}
        if background.get("kind") == "image" and on is None:
            mobject.set_stroke(self.look["background"], width=7, opacity=0.85, background=True)
        if at is not None:
            mobject.move_to([at[0], at[1], 0])
        # The colour asked for: Manim's get_color() reports the outline, not the fill.
        self._labels.append((mobject, text, on or self.look["background"], fill))
        return mobject

    # --- one type scale, one set of moves: every scene of a video alike ------------------

    # A title names the scene, it is not the scene: v7's 60 pt titles crowded the frame.
    TITLE_SIZE, HEADING_SIZE, LABEL_SIZE = 44, 36, 30
    _composing = False
    _fixed: dict | None = None       # the places the program gave this template
    _made: dict | None = None        # the places it used, recorded

    def _place(self, name: str, mobject, sized: bool = False):
        """Put `mobject` where the program says (`layout[name]`: its centre, and
        for a picture its width), or leave it where it was worked out -- and record
        where it is, so the program can say so."""
        if self._made is None:
            return mobject
        while name in self._made:
            name += "+"
        given = (self._fixed or {}).get(name)
        if given is not None:
            if sized and len(given) > 2 and mobject.width > 0:
                mobject.scale(float(given[2]) / mobject.width)
            mobject.move_to([float(given[0]), float(given[1]), 0])
        centre = mobject.get_center()
        self._made[name] = [round(float(centre[0]), 2), round(float(centre[1]), 2)] + (
            [round(float(mobject.width), 2)] if sized else [])
        return mobject

    def title(self, text: str):
        """The scene's title, always the same size, weight and place (top centre) --
        on a soft band over painted art, as every other title is."""
        if (BRIEF.__dict__.get("background") or {}).get("kind") == "image":
            return self._panel_title(text)
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

    def boxed(self, text: str, size: int = 30, color: str | None = None, pad: float = 0.25,
              at: tuple[float, float] | None = None, stroke: str | None = None,
              fill: str | None = None):
        """Words in a box sized to them, so they can never spill out of it. Filled
        with a tint of its outline's colour, so the box reads as a thing, and a line
        behind it is covered instead of running through."""
        from manim import RoundedRectangle, VGroup
        stroke = stroke or self.colour(0)
        # Light and soft-cornered, edged thinly in its colour: v7's heavy outlines on
        # tinted fills read as a slide's boxes.
        fill = fill or _mix(self._panel_fill(), stroke, 0.08)
        label = self.label(text, size=size, color=color, on=fill)
        box = RoundedRectangle(corner_radius=0.22, width=label.width + 2 * pad,
                               height=label.height + 2 * pad, stroke_color=stroke,
                               stroke_width=3, fill_color=fill, fill_opacity=1).move_to(label)
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
        image = ImageMobject(_softened(_trimmed(path), path)).set(height=height)
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

    @_recorded
    def flow(self, steps: list[str], y: float = -0.3, size: int = 30, gap: float = 0.9):
        """Steps in boxes joined by arrows, left to right -- top to bottom when they
        do not fit across. Has .boxes and .arrows (arrows[i] joins boxes[i] to [i+1])."""
        self._calm()
        from manim import DOWN, RIGHT, VGroup
        boxes = [self.boxed(text, size=size, stroke=self.colour(i))
                 for i, text in enumerate(steps)]
        group = VGroup(*boxes).arrange(RIGHT, buff=gap).move_to([0, y, 0])
        if group.width > 2 * self.SAFE_X:
            group.arrange(DOWN, buff=gap * 0.6).move_to([0, y, 0])
        self.safe(group)
        self._place("diagram", group)
        arrows = [self.connect(a, b, color=self.look["text"])
                  for a, b in zip(boxes, boxes[1:], strict=False)]
        whole = VGroup(*boxes, *arrows)
        whole.boxes, whole.arrows = boxes, arrows
        return whole

    @_recorded
    def hub(self, centre: str, around: list[str], y: float = -0.3, size: int = 30,
            gap: float = 1.2):
        """One idea in the middle and what hangs off it, in a column either side, each
        joined to the middle by a line from edge to edge. Has .centre, .items, .lines
        (lines[i] joins the centre to items[i])."""
        self._calm()
        from manim import DOWN, LEFT, RIGHT, Line, VGroup
        middle = self.boxed(self._broken(centre, 4.2, size + 4), size=size + 4,
                            stroke=self.colour(0), fill=self.tint(self.colour(0), 0.3))
        # Each item wrapped to the room its side has: set on one line, a wide hub was
        # shrunk to fit and its words went below the smallest readable size.
        room = (2 * self.SAFE_X - middle.width - 2 * gap) / 2 - 0.6
        items = [self.boxed(self._broken(text, max(2.0, room), size), size=size,
                            stroke=self.colour(i + 1))
                 for i, text in enumerate(around)]
        left = VGroup(*items[0::2]).arrange(DOWN, buff=0.5, aligned_edge=RIGHT)
        right = VGroup(*items[1::2]).arrange(DOWN, buff=0.5, aligned_edge=LEFT) \
            if len(items) > 1 else VGroup()
        left.next_to(middle, LEFT, buff=gap)
        sides = [left]
        if len(right):
            right.next_to(middle, RIGHT, buff=gap)
            sides.append(right)
        self._place("diagram", self.safe(VGroup(middle, *sides).move_to([0, y, 0])))
        lines = []
        for index, item in enumerate(items):
            start, end = ((middle.get_left(), item.get_right()) if index % 2 == 0
                          else (middle.get_right(), item.get_left()))
            lines.append(Line(start, end, buff=0.1, color=self.colour(index + 1),
                              stroke_width=4))
        whole = VGroup(middle, *items, *lines)
        whole.centre, whole.items, whole.lines = middle, items, lines
        return whole

    @_recorded
    def timeline(self, events: list[str], y: float = -0.4, size: int = 30):
        """Things in order on a line, a dot and a label each. Across the frame with
        labels above and below in turn; down its left side when they do not fit across.
        Has .spine, .dots, .labels."""
        self._calm()
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
            # Centred as a block: held to the left edge, it left most of the frame empty.
            column = VGroup(spine, *dots, *labels)
            column.shift(RIGHT * -column.get_center()[0])
        whole = VGroup(spine, *dots, *labels)
        self._place("diagram", self.safe(whole))
        whole.spine, whole.dots, whole.labels = spine, dots, labels
        return whole

    # --- shot templates: a whole scene from a few slots ---------------------------------
    # Each lays out, times and moves a complete scene that passes every check by
    # construction; the program only fills the slots and names the words each part
    # arrives on (`cue`: words from the narration). End the scene with self.finish().

    def _at_cue(self, cue: str | float | None) -> None:
        # Never later than a few seconds before the end: a closing point cued on the
        # narration's last words was still fading in as the scene ended.
        if cue:
            self.until(min(self.when(cue), BRIEF.seconds - 3.0))

    def _broken(self, text: str, width: float, size: int, bold: bool = False) -> str:
        """`text` with line breaks between words, so each line fits `width` at `size`,
        measured in the weight it is drawn in: bold is wider, and a heading measured
        in the regular weight ran across a compare's dividing line."""
        weight = "BOLD" if bold else "NORMAL"
        lines: list[str] = []
        for word in text.split() or [text]:
            trial = f"{lines[-1]} {word}" if lines else word
            if lines and Text(trial, font_size=size, weight=weight).width <= width:
                lines[-1] = trial
            else:
                lines.append(word)
        return "\n".join(lines)

    def _wrapped(self, text: str, width: float, size: int, **style) -> Text:
        """Words broken into lines that fit `width` (scene units) at `size`,
        measured -- between words only, never inside one ("Electroc/hemical"); a
        word wider than the line sets the type smaller, down to the smallest."""
        size = max(size, self.smallest_size())
        weight = "BOLD" if style.get("bold") else "NORMAL"
        widest = max(Text(word, font_size=size, weight=weight).width
                     for word in text.split() or [text])
        if widest > width:
            size = max(self.smallest_size(), int(size * width / widest))
        return self.label(self._broken(text, width, size, bool(style.get("bold"))),
                          size=size, **style)

    def _fit(self, path: str, width: float, height: float, at: tuple[float, float]):
        image = self.picture(path, height=1.0)
        image.scale(min(width / image.width, height / image.height))
        image.move_to([at[0], at[1], 0])
        return image

    # Six ways to point at a part, one chosen for each: v6 and v7 drew a dot, a long
    # line and a word to every part alike -- a cover's publisher included.
    POINTING = ("tag", "glow", "zoom", "lens", "sketch", "caption")
    LARGEST_PINNED = 0.15     # of the picture: a part larger -- a person -- is named, not pinned
    MOST_MARKS_SHOWN = 2      # tags, loops and lenses on screen at once

    def _style_of(self, style, box) -> str:
        """The style a callout is drawn in. A part that is most of a figure -- a
        person, a whole animal -- is named by a caption, never pinned with a dot or
        circled: a dot on a person's chest reads as a specimen pin."""
        style = style if style in self.POINTING else "tag"
        if box is None:
            return "caption" if style == "caption" else "tag"
        if (box[2] - box[0]) * (box[3] - box[1]) > self.LARGEST_PINNED and style != "glow":
            return "caption"
        return style

    @_composed
    def hero(self, picture: str, callouts: list, title: str = "", cue: str | None = None,
             moves: list | None = None):
        """One picture, large, and the parts the narration teaches pointed out on
        their words. `callouts` are (label, (x, y), cue, (left, top, right, bottom),
        style) -- place and box as fractions of the picture from its top left; box
        and style may be left off. A style is one of:
        tag -- a small tag beside the part, a short tick to it (naming a small part);
        glow -- the rest of the frame softens, a glow rings the part, its name in the
        caption ("look here" while it is spoken); zoom -- the view eases in on the
        part and back out (a detail too small to see whole); lens -- a round
        magnifier beside the part shows it enlarged (a tiny structure kept in its
        place); sketch -- a hand-drawn loop is drawn round it, its name beside (an
        informal "this one"); caption -- its name on a card at the foot of the frame,
        nothing laid on the picture (a person, a whole scene or era).
        A painting with its own setting fills the whole frame; a cut-out subject
        stands large on the scene's background. `moves` are ([(x, y), ...], cue): a
        pulse runs along those points of the picture on the cue -- a signal
        travelling, liquid carried."""
        from manim import Dot, Line
        callouts = [_entry(c, ("label", "point", "at", "part", "style")) for c in callouts]
        moves = [_entry(m, ("through", "at")) for m in (moves or [])]
        scenic = _scenic(picture)
        source = picture if scenic else _trimmed(picture)
        if not scenic:
            # Parts are located on the whole picture; the trimmed one is shown.
            callouts = [(text, _in_trimmed(picture, *xy), cue,
                         None if box is None else (*_in_trimmed(picture, *box[:2]),
                                                   *_in_trimmed(picture, *box[2:])), style)
                        for text, xy, cue, box, style in callouts]
            moves = [([_in_trimmed(picture, *xy) for xy in path], cue)
                     for path, cue in (moves or [])]
        # Every part the program names keeps its moment -- dropping some lost what the
        # narration taught; the frame stays calm because only MOST_MARKS_SHOWN are on
        # screen at once, the oldest going as the next comes.
        callouts = [(text, xy, cue, box, self._style_of(style, box))
                    for text, xy, cue, box, style in callouts]
        captioned = any(style in ("glow", "zoom", "caption") for *_, style in callouts)
        heading = self._place("title", self._panel_title(title)) if title else None
        top = (heading.get_bottom()[1] - 0.2) if heading is not None else self.SAFE_Y
        foot = -self.SAFE_Y + (1.05 if captioned else 0.0)
        if scenic:
            # The scene itself: edge to edge, as the painting was made -- never a
            # picture boxed inside the frame.
            image = manim.ImageMobject(source)
            image.scale(max(FRAME_WIDTH_UNITS / image.width, FRAME_HEIGHT_UNITS / image.height))
            image.move_to([0, 0, 0])
            image.scenic = True
        else:
            # Room at both sides for the tags: the picture is the scene, they serve it.
            image = self._fit(picture, 2 * self.SAFE_X - 2.4, top - foot,
                              (0.0, (top + foot) / 2))
        self._place("picture", image, sized=True)

        def at(fx: float, fy: float):
            return np.array([image.get_left()[0] + fx * image.width,
                             image.get_top()[1] - fy * image.height, 0.0])

        def frame_box(box):
            (x0, y1), (x1, y0) = at(box[0], box[1])[:2], at(box[2], box[3])[:2]
            return (x0, y0, x1, y1)

        if heading is not None and not scenic:
            self.play(self.reveal(heading))
        self._at_cue(cue)
        self.play(manim.FadeIn(image, scale=1.0 if scenic else 0.96, run_time=0.7))
        if heading is not None and scenic:
            self.play(self.reveal(heading))
        # A part the frame has cropped away is not pointed at: it would point at nothing.
        inside = [c for c in callouts if abs(at(*c[1])[0]) < self.SAFE_X - 0.2
                  and abs(at(*c[1])[1]) < self.SAFE_Y - 0.2]
        crowding = None if scenic else _drawn_share(source, image)
        points = [at(*c[1]) for c in inside]
        taken = [_box_of(heading)] if heading is not None else []
        if captioned:
            taken.append((-self.SAFE_X, -self.SAFE_Y, self.SAFE_X, -self.SAFE_Y + 1.05))
        marks = []
        for index, (text, _, part_cue, box, style) in enumerate(inside):
            colour = self.colour(index)
            point = points[index]
            own = frame_box(box) if box is not None else None
            others = [p for j, p in enumerate(points) if j != index]
            near = None if crowding is None else (lambda mine, own=own: crowding(mine, own))
            mark = {"style": style, "text": text, "colour": colour, "box": box, "own": own,
                    "cue": part_cue, "point": point}
            if style in ("tag", "sketch", "lens"):
                if style == "lens":
                    tag = self._lens(source, box, colour, text)
                else:
                    tag = self._pill(text, colour)
                # A small part keeps its tag off it; a loop or a lens is drawn round
                # the part, so the tag stands clear of the whole of it.
                small = own is not None and (box[2] - box[0]) * (box[3] - box[1]) < 0.1
                avoid = [own] if own is not None and (small or style != "tag") else []
                self._place_near(tag, point, image.get_center(), taken + avoid, others, near)
                self._place(f"{style}: {text}", tag)
                taken.append(_box_of(tag))
                mark["tag"] = tag
                if style == "tag":
                    mark["tick"] = Line(_edge(tag.box, point), point, buff=0.04,
                                        color=colour, stroke_width=3)
                    dot = Dot(point, radius=0.085, color=colour)
                    mark["dot"] = dot.set_stroke(self.look["background"], width=3,
                                                 background=True)
                elif style == "sketch":
                    mark["loop"] = _loop(own, colour, index)
                else:
                    mark["cone"] = _cone(own, tag.lens, colour)
            marks.append(mark)

        events = [(self.when(m["cue"] or ""), "mark", m) for m in marks]
        events += [(self.when(c or ""), "move", [at(*xy) for xy in path])
                   for path, c in (moves or []) if len(path) > 1]
        events.sort(key=lambda e: e[0])
        light, last, caption, passing, visible = None, None, None, False, []
        for number, (moment, kind, what) in enumerate(events):
            self.until(moment)
            if kind == "move":
                self._travel(what)
                continue
            style, colour = what["style"], what["colour"]
            following = events[number + 1][0] if number + 1 < len(events) else BRIEF.seconds
            # A caption naming a lit or near part leaves with it: v7's "heart" stayed
            # on while the light had moved on to the brain. One naming a person or a
            # scene stays until another takes its place.
            if passing and style in ("tag", "lens", "sketch"):
                self.play(manim.FadeOut(caption, run_time=0.3))
                caption, passing = None, False
            # Never more than a couple of marks on the picture: the oldest goes as a
            # new one comes -- v7 kept four tags and a caption on screen at once.
            marks = [what[k] for k in ("dot", "tick", "cone", "loop", "tag") if k in what]
            if marks and len(visible) >= self.MOST_MARKS_SHOWN:
                self.play(*[manim.FadeOut(m) for m in visible.pop(0)], run_time=0.3)
            if marks:
                visible.append(marks)
            if style == "tag":
                # A small part is lit as it is named; a large one is only tagged.
                box = what["box"]
                if box is not None and (box[2] - box[0]) * (box[3] - box[1]) < 0.45:
                    light = self._spotlight(image, source, what["box"], at, colour, light)
                    last = moment
                self.play(manim.FadeIn(what["dot"], scale=2.2, run_time=0.35),
                          self.draw(what["tick"], run_time=0.35),
                          self.reveal(what["tag"], run_time=0.45))
            elif style == "glow":
                light = self._spotlight(image, source, what["box"], at, colour, light)
                last = moment
                caption, passing = self._caption(what["text"], colour, caption), True
            elif style == "zoom":
                if light is not None:
                    self.play(*[manim.FadeOut(m) for m in light.values()], run_time=0.4)
                    light = None
                caption = self._caption(what["text"], colour, caption)
                self._zoom(image, what["own"], scenic, min(following, self.now + 4.5))
                self.play(manim.FadeOut(caption, run_time=0.3))
                caption, passing = None, False
            elif style == "lens":
                self.play(self.draw(what["cone"], run_time=0.5))
                self.play(manim.FadeIn(what["tag"], scale=0.6, run_time=0.6))
            elif style == "sketch":
                self.play(self.draw(what["loop"], run_time=0.7))
                self.play(self.reveal(what["tag"], run_time=0.4))
            else:
                caption, passing = self._caption(what["text"], colour, caption), False
        if light is not None:
            # The whole picture back, every part named, once the last has been seen.
            self.until(max(self.now, last + 2.0))
            leaving = list(light.values()) + ([caption] if passing else [])
            self.play(*[manim.FadeOut(m) for m in leaving], run_time=0.6)

    def _calm(self) -> None:
        """Before a shot carried by words -- steps, a comparison, a flow, a hub, a
        timeline -- a painted backdrop fades further back, so every word reads on a
        quiet ground. Once a shot: it goes with the shot when the frame is cleared."""
        from manim import Rectangle
        found = BRIEF.__dict__.get("background") or {}
        if found.get("kind") != "image" or any(getattr(m, "calm", False) for m in self.shown):
            return
        veil = Rectangle(width=FRAME_WIDTH_UNITS + 0.1, height=FRAME_HEIGHT_UNITS + 0.1)
        veil.set_fill(self.look["background"], opacity=WORDS_WASH).set_stroke(width=0)
        veil.calm = veil.attention = True
        # Under what is already on screen: laid over it, it greyed v9's diagram titles.
        above = list(self.shown)
        self.add(veil)
        self.bring_to_front(*above)
        self.play(manim.FadeIn(veil, run_time=0.4))

    def _panel_fill(self) -> str:
        """The ground of a tag, a band or a card: light, with the theme's words dark
        on it -- or deep, where the theme's words are light."""
        light = _mix("#ffffff", self.look["background"], 0.25)
        if _contrast(self.look["text"], light) >= 4.5:
            return light
        return _mix("#1f2430", self.look["background"], 0.25)

    def _caption(self, text: str, colour: str, before=None):
        """A name on a card at the foot of the frame, an accent bar at its side --
        nothing laid on the picture. One at a time: a new one takes the place of the
        last."""
        from manim import RoundedRectangle, VGroup
        fill = self._panel_fill()
        words = self._wrapped(text, 2 * self.SAFE_X - 2.0, self.LABEL_SIZE, bold=True,
                              on=fill)
        self._panels.add(id(words))
        card = RoundedRectangle(corner_radius=0.22, width=words.width + 0.95,
                                height=words.height + 0.4)
        card.set_fill(fill, opacity=0.93).set_stroke(width=0)
        bar = RoundedRectangle(corner_radius=0.05, width=0.1, height=card.height - 0.24)
        bar.set_fill(colour, opacity=1).set_stroke(width=0)
        words.move_to(card).shift([0.18, 0, 0])
        bar.move_to([card.get_left()[0] + 0.24, card.get_center()[1], 0])
        made = VGroup(card, bar, words)
        made.move_to([-self.SAFE_X + made.width / 2, -self.SAFE_Y + made.height / 2, 0])
        if before is None:
            self.play(manim.FadeIn(made, shift=manim.RIGHT * 0.3, run_time=0.45))
        else:
            self.play(manim.FadeOut(before, run_time=0.25),
                      manim.FadeIn(made, shift=manim.RIGHT * 0.3, run_time=0.45))
        return made

    def _zoom(self, image, own, scenic: bool, until: float) -> None:
        """The view eases in on a part until `until`, then back out: what was laid
        on the picture steps aside while it is near, and returns with it."""
        if own is None:
            return
        centre = np.array([(own[0] + own[2]) / 2, (own[1] + own[3]) / 2, 0.0])
        wide, high = max(0.2, own[2] - own[0]), max(0.2, own[3] - own[1])
        grown = min(2.6, FRAME_WIDTH_UNITS * 0.5 / wide, FRAME_HEIGHT_UNITS * 0.5 / high)
        if grown < 1.25:
            self.until(until)
            return
        # Scaled about the part, which stays put; then the part brought to the middle.
        target = -centre
        if scenic:
            # A painting edge to edge stays edge to edge: never pulled past its border.
            middle = centre * (1 - grown)
            half = np.array([image.width * grown / 2, image.height * grown / 2, 0.0])
            frame = np.array([FRAME_WIDTH_UNITS / 2, FRAME_HEIGHT_UNITS / 2, 0.0])
            target = np.clip(target, frame - half - middle, half - frame - middle)
        laid = [m for m in self.shown if m is not image
                and m not in self._panel_groups()]
        image.save_state()
        if laid:
            self.play(*[manim.FadeOut(m, run_time=0.3) for m in laid])
        self.play(image.animate.scale(grown, about_point=centre).shift(target),
                  run_time=1.2, rate_func=manim.smooth)
        self.until(max(self.now + 1.0, until - 1.2))
        self.play(manim.Restore(image), run_time=1.0, rate_func=manim.smooth)
        if laid:
            self.play(*[manim.FadeIn(m, run_time=0.3) for m in laid])

    def _panel_groups(self) -> list:
        """The title band and caption card on screen: they stay when the view moves."""
        return [m for m in self.shown
                if any(id(part) in self._panels for part in m.get_family())]

    def _lens(self, source: str, box, colour: str, text: str):
        """A round magnifier showing the part enlarged, its name under it. Has .box
        (for its pointer), .lens and .label."""
        from manim import Circle, Group, ImageMobject
        disc = ImageMobject(_round_crop(source, box, self._panel_fill())).set(height=2.3)
        rim = Circle(radius=1.15, color=colour, stroke_width=5).move_to(disc)
        rim.attention = True
        name = self._pill(text, colour)
        name.next_to(disc, manim.DOWN, buff=0.18)
        lens = Group(disc, rim, name)
        lens.box, lens.lens, lens.label = name.box, rim, name.label
        return lens

    def _pill(self, text: str, colour: str):
        """A name on a small rounded tag: light, edged in its part's colour, readable
        on any painting because it carries its own ground. Has .box and .label."""
        from manim import RoundedRectangle, VGroup
        fill = self._panel_fill()
        label = self._wrapped(text, 4.6, self.LABEL_SIZE - 2, color=self.look["text"], on=fill)
        self._panels.add(id(label))
        width, height = label.width + 0.44, label.height + 0.26
        box = RoundedRectangle(corner_radius=min(0.3, height / 2), width=width, height=height)
        box.set_fill(fill, opacity=0.95).set_stroke(colour, width=3).move_to(label)
        tag = VGroup(box, label)
        tag.box, tag.label = box, label
        return tag

    def _panel_title(self, text: str):
        """The scene's title on a soft light band at the top: over painted art the
        words carry their own ground, and never sit half on the picture."""
        from manim import RoundedRectangle, VGroup
        fill = self._panel_fill()
        # Smaller than a title on a plain ground: on a painting it names the scene,
        # it is not the scene -- v7's ran to two lines over a third of the frame.
        room = 2 * self.SAFE_X - 1.0
        size = next((s for s in range(self.HEADING_SIZE, 39, -2)
                     if Text(text, font_size=s, weight="BOLD").width <= room), self.HEADING_SIZE)
        words = self._wrapped(text, room, size, bold=True, on=fill)
        self._panels.add(id(words))
        band = RoundedRectangle(corner_radius=0.3, width=words.width + 0.8,
                                height=words.height + 0.36)
        band.set_fill(fill, opacity=0.9).set_stroke(width=0)
        heading = VGroup(band, words.move_to(band))
        heading.move_to([0, self.SAFE_Y - heading.height / 2, 0])
        return heading

    def _place_near(self, tag, point, centre, taken: list, others: list,
                    crowding=None) -> None:
        """Put `tag` close beside `point`, on the side away from the picture's middle
        first: inside the safe area, clear of every tag and title already placed, and
        off the other parts' points -- and, on a cut-out picture, on its empty ground
        rather than over what is drawn (`crowding(box)`, 0 to 1): v7's "Described by
        Broca" lay across his patient. The nearest free place wins; with none free,
        the one that overlaps least."""
        away = point - centre
        directions = sorted(
            [np.array(d, dtype=float) / np.linalg.norm(d) for d in
             ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1))],
            key=lambda d: -float(np.dot(d[:2], away[:2])))
        best, least = None, None
        for distance in (0.55, 0.9, 1.3, 1.8, 2.4, 3.0):
            for d in directions:
                reach = np.array([d[0] * (distance + tag.width / 2),
                                  d[1] * (distance * 0.75 + tag.height / 2), 0.0])
                tag.move_to(point + reach)
                mine = _box_of(tag)
                if (mine[0] < -self.SAFE_X or mine[2] > self.SAFE_X
                        or mine[1] < -self.SAFE_Y or mine[3] > self.SAFE_Y):
                    continue
                clash = sum(_overlap_area(mine, other, 0.15) for other in taken) + sum(
                    1.0 for p in others if mine[0] < p[0] < mine[2] and mine[1] < p[1] < mine[3])
                if crowding is not None:
                    # Over a drawn subject costs more than a longer tick: v7's tags
                    # covered the robot's face and the brain they named.
                    clash += 3 * max(0.0, crowding(mine) - 0.1)
                if clash == 0:
                    return
                if least is None or clash < least:
                    best, least = point + reach, clash
        tag.move_to(best if best is not None else point)
        self.safe(tag)

    def _spotlight(self, image, source: str, box, at, colour, light=None):
        """Attention moved to what is being said: a light veil softens the rest of
        the frame -- never darkens it -- the part named shows at full strength over
        it, cut from the same picture, and a soft glow rings it; from an earlier
        part, the light moves across."""
        from manim import Ellipse, ImageMobject, Rectangle
        from PIL import Image as _Image
        pad = 0.03
        left, top = max(0.0, box[0] - pad), max(0.0, box[1] - pad)
        right, bottom = min(1.0, box[2] + pad), min(1.0, box[3] + pad)
        out = Path(source).with_name(f"{Path(source).stem}-part-{left:.3f}-{top:.3f}-"
                                     f"{right:.3f}-{bottom:.3f}.png")
        if not out.exists():
            with _Image.open(source) as opened:
                width, height = opened.size
                opened.convert("RGBA").crop((round(left * width), round(top * height),
                                             round(right * width), round(bottom * height))
                                            ).save(out)
        corner_a, corner_b = at(left, top), at(right, bottom)
        part = ImageMobject(str(out))
        part.stretch_to_fit_width(max(0.05, corner_b[0] - corner_a[0]))
        part.stretch_to_fit_height(max(0.05, corner_a[1] - corner_b[1]))
        part.move_to([(corner_a[0] + corner_b[0]) / 2, (corner_a[1] + corner_b[1]) / 2, 0])
        part.scenic = True
        # Close round the part: a ring 1.2 times a tall part's size swallowed half
        # the table and ran through its own tag.
        ring = Ellipse(width=part.width * 1.06 + 0.3, height=part.height * 1.06 + 0.3)
        ring.move_to(part).set_fill(opacity=0).set_stroke(colour, width=4)
        glow = ring.copy().set_stroke(colour, width=18, opacity=0.22)
        # Marks of attention laid on the picture, not shapes of the layout.
        ring.attention = glow.attention = True
        # Laid in under everything already on the picture before it fades in: lifted
        # over them afterwards, the veil dimmed the title and caption as it came.
        above = [m for m in self.shown if m is not image]
        if light is None:
            veil = Rectangle(width=FRAME_WIDTH_UNITS + 0.1, height=FRAME_HEIGHT_UNITS + 0.1)
            # Light enough to keep the painting's colour: at 0.55 whole stretches
            # of v9 sat pale behind it.
            veil.set_fill(self.look["background"], opacity=0.4).set_stroke(width=0)
            veil.attention = True
            self.add(veil, part, glow, ring)
            self.bring_to_front(*above)
            self.play(manim.FadeIn(veil), manim.FadeIn(part), manim.FadeIn(glow),
                      self.draw(ring), run_time=0.6)
        else:
            veil = light["veil"]
            self.add(part)
            self.bring_to_front(*[m for m in above if m not in (light["part"], veil)])
            self.play(manim.FadeOut(light["part"]), manim.FadeIn(part),
                      manim.Transform(light["ring"], ring), manim.Transform(light["glow"], glow),
                      run_time=0.7)
            ring, glow = light["ring"], light["glow"]
        # Over the picture, under every tag, tick and dot already on it.
        self.bring_to_front(*[m for m in self.shown
                              if m not in (image, part, ring, glow, veil)])
        return {"veil": veil, "part": part, "ring": ring, "glow": glow}

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

    @_composed
    def steps(self, steps: list, title: str = ""):
        """Two to four steps in order -- an experiment, a process: `steps` are
        (label, picture or None, cue). Each arrives numbered, in its own panel,
        joined to the one before by an arrow."""
        self._calm()
        from manim import Circle, Group
        steps = [_entry(step, ("label", "picture", "at")) for step in steps]
        if title:
            self.play(self.reveal(self._place("title", self.title(title))))
        count = max(1, len(steps))
        width = (2 * self.SAFE_X - (count - 1) * 0.5) / count
        top = 2.45 if title else 3.2
        # A picture for every step stands over its own step; fewer than that, the
        # first stands once over them all -- one panel with a picture, the rest
        # empty, looked lopsided.
        each = all(picture for _, picture, _ in steps)
        shared = next((picture for _, picture, _ in steps if picture), None)
        if shared and not each:
            self.play(manim.FadeIn(self._place(
                "picture", self._fit(shared, 7.0, top + 0.6, (0, (top - 1.2) / 2 + 0.3)),
                sized=True), run_time=0.6))
        # With no picture the row stands mid-frame, not under an empty top half.
        badge_y = -1.55 if shared else 0.6
        panels = []
        for index, (text, picture, cue) in enumerate(steps):
            x = -self.SAFE_X + width / 2 + index * (width + 0.5)
            parts = []
            if picture and each:
                parts.append(self._place(f"step {index + 1} picture", self._fit(
                    picture, width - 0.2, top + 0.6, (x, (top - 1.2) / 2 + 0.3)), sized=True))
            colour = self.colour(index)
            badge = Circle(radius=0.34, color=colour, fill_color=self.tint(colour, 0.25),
                           fill_opacity=1, stroke_width=4).move_to([x, badge_y, 0])
            number = self.label(str(index + 1), size=self.LABEL_SIZE, on=self.tint(colour, 0.25),
                                bold=True).move_to(badge)
            words = self._wrapped(text, width - 0.1, self.LABEL_SIZE)
            words.next_to(badge, manim.DOWN, buff=0.3)
            self._place(f"step {index + 1}", Group(badge, number, words))
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
        [up to three short points], cue) on its own soft card, the two cards side by
        side and centred in the room under the title -- v7's hung from the top over
        a busy room, half the frame empty below them."""
        self._calm()
        from manim import Group, RoundedRectangle
        fill = self._panel_fill()
        left, right = (_entry(side, ("heading", "picture", "points", "at"))
                       for side in (left, right))
        heading_band = self._place("title", self._panel_title(title)) if title else None
        if heading_band is not None:
            self.play(self.reveal(heading_band))
        top = heading_band.get_bottom()[1] - 0.3 if heading_band is not None else self.SAFE_Y
        sides = []
        for side, (heading, picture, points, cue) in ((-1, left), (1, right)):
            colour = self.colour(0 if side < 0 else 1)
            # Words in an accent only where the accent reads; else in the ink.
            ink = colour if _contrast(colour, fill) >= 4.5 else self.look["text"]
            # Wrapped to its own card: a long heading ran across the dividing line.
            head = self._wrapped(heading, 5.4, self.HEADING_SIZE, bold=True, color=ink, on=fill)
            parts, y = [head], -head.height - 0.3
            head.move_to([0, -head.height / 2, 0])
            if picture:
                image = self._fit(picture, 5.2, 2.4, (0, y - 1.2))
                parts.append(image)
                y = image.get_bottom()[1] - 0.25
            for point in (points or [])[:3]:
                words = self._wrapped(point, 5.4, self.LABEL_SIZE, on=fill)
                words.move_to([0, y - words.height / 2, 0])
                y = words.get_bottom()[1] - 0.25
                parts.append(words)
            self._panels.update(id(m) for m in parts)
            sides.append((side, Group(*parts), cue))
        tallest = max(group.height for _, group, _ in sides)
        middle = (top - self.SAFE_Y) / 2
        cards = []
        for side, group, _ in sides:
            x = side * 3.3
            group.move_to([x, middle + tallest / 2 - group.height / 2, 0])
            card = RoundedRectangle(corner_radius=0.3, width=6.2, height=tallest + 0.8)
            card.set_fill(fill, opacity=0.9).set_stroke(width=0).move_to([x, middle, 0])
            self._place("left card" if side < 0 else "right card", Group(card, group))
            cards.append(card)
        # Each card with its own side, on its words: v9's second card stood empty
        # until they came.
        for card, (_, group, cue) in zip(cards, sides, strict=True):
            self._at_cue(cue)
            self.play(manim.FadeIn(card, scale=0.97, run_time=0.4),
                      *[self.reveal(part) for part in group])

    @_composed
    def person(self, picture: str, name: str, line: str, cue: str | None = None,
               line_cue: str | None = None):
        """A person: their portrait, their name, and one line on what they did."""
        portrait = self._place("picture", self._fit(picture, 5.2, 5.8, (-3.4, -0.2)), sized=True)
        named = self.label(name, size=self.TITLE_SIZE - 6, bold=True)
        named.move_to([0.3 + named.width / 2, 1.3, 0])
        self._place("name", self.safe(named))
        said = self._wrapped(line, 5.6, self.LABEL_SIZE)
        said.move_to([0.3 + said.width / 2, named.get_bottom()[1] - 0.45 - said.height / 2, 0])
        self._place("line", said)
        self._at_cue(cue)
        self.play(manim.FadeIn(portrait, run_time=0.6), self.reveal(named))
        self._at_cue(line_cue)
        self.play(self.reveal(said))

    @_composed
    def key_idea(self, statement: str, picture: str | None = None, cue: str | None = None):
        """One idea to remember, large, on a soft light card with an accent bar down
        its side -- readable on any background, where v7's words floated over the
        painting -- and a picture beside it when there is one."""
        from manim import RoundedRectangle, VGroup
        fill = self._panel_fill()
        if picture:
            image = self._place("picture", self._fit(picture, 5.6, 5.8, (3.4, -0.1)), sized=True)
            words, centre = self._wrapped(statement, 5.6, 42, on=fill), (-3.2, 0.2)
        else:
            image, words, centre = None, self._wrapped(statement, 10.4, 46, on=fill), (0, 0.3)
        self._panels.add(id(words))
        card = RoundedRectangle(corner_radius=0.3, width=words.width + 1.2,
                                height=words.height + 0.8)
        card.set_fill(fill, opacity=0.92).set_stroke(width=0)
        bar = RoundedRectangle(corner_radius=0.06, width=0.12, height=card.height - 0.4)
        bar.set_fill(self.colour(0), opacity=1).set_stroke(width=0)
        words.move_to(card).shift([0.15, 0, 0])
        bar.move_to([card.get_left()[0] + 0.35, card.get_center()[1], 0])
        self._place("card", self.safe(VGroup(card, bar, words).move_to([centre[0], centre[1], 0])))
        self._at_cue(cue)
        self.play(manim.FadeIn(card, scale=0.97, run_time=0.5),
                  *([manim.FadeIn(image, run_time=0.6)] if image else []))
        self.play(manim.GrowFromEdge(bar, manim.DOWN, run_time=0.4), self.reveal(words))

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
        lines = [_entry(line, ("text", "at")) for line in (lines or [])]
        if banner:
            image = self._fit(picture, 2 * self.SAFE_X - 0.6, 2.9, (0.0, 1.75))
            left, width, top = -self.SAFE_X + 0.2, 2 * self.SAFE_X - 0.4, \
                image.get_bottom()[1] - 0.35
        else:
            image = self._fit(picture, 5.4, 6.2, (3.25, -0.05))
            left, width, top = -self.SAFE_X + 0.1, 5.9, 2.3
        self._place("picture", image, sized=True)
        # On a soft card, as every title is: v8's opening title sat over the painted
        # lamp behind it.
        fill = self._panel_fill()
        left, width, top = left + 0.35, width - 0.7, top - 0.3
        heading = self._wrapped(title, width, self.TITLE_SIZE - 8, on=fill)
        heading.move_to([left + heading.width / 2, top - heading.height / 2, 0])
        rule = Line([left, heading.get_bottom()[1] - 0.25, 0],
                    [left + min(width, max(2.5, heading.width)), heading.get_bottom()[1] - 0.25, 0],
                    color=self.colour(0), stroke_width=6)
        placed, y, words_on_card = [], rule.get_center()[1] - 0.45, [heading]
        for index, (text, line_cue) in enumerate((lines or [])[:3]):
            words = self._wrapped(text, width - 0.6, self.LABEL_SIZE, on=fill)
            words.move_to([left + 0.55 + words.width / 2, y - words.height / 2, 0])
            dot = Dot([left + 0.2, words.get_top()[1] - 0.22, 0], radius=0.09,
                      color=self.colour(index + 1))
            placed.append((manim.VGroup(dot, words), line_cue))
            words_on_card.append(words)
            y = words.get_bottom()[1] - 0.35
        self._panels.update(id(words) for words in words_on_card)
        content = manim.VGroup(heading, rule, *[group for group, _ in placed])
        card = manim.RoundedRectangle(corner_radius=0.3, width=content.width + 0.7,
                                      height=content.height + 0.6)
        card.set_fill(fill, opacity=0.9).set_stroke(width=0).move_to(content)
        self._place("card", manim.VGroup(card, content))
        self._at_cue(cue)
        self.play(manim.FadeIn(image, scale=0.94, run_time=0.8), manim.FadeIn(card),
                  self.reveal(heading))
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
        for top in self.shown:
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
                size, bold, set_height = getattr(m, "kit_type", (0, False, 0.0))
                line = (_line_px(size, bold) * m.height / set_height if size and set_height
                        else (bottom - top_px) / lines)
                texts.append({"text": str(text), "box": [round(left), round(top_px),
                                                         round(right), round(bottom)],
                              "line_height": round(line),
                              "color": fill, "behind": behind,
                              "recorded": id(m) in recorded,
                              "panel": id(m) in self._panels})
        shapes, pictures, laid_on = [], [], []
        for top in self.shown:
            for m in top.get_family():
                if isinstance(m, ImageMobject):
                    left, top_px = _px(m.get_corner([-1, 1, 0]))
                    right, bottom = _px(m.get_corner([1, -1, 0]))
                    box = [round(left), round(top_px), round(right), round(bottom)]
                    pictures.append(box)
                    # A painting edge to edge is the ground the words stand on.
                    if not getattr(m, "scenic", False):
                        laid_on.append(box)
                # Its own outline: an arrow's shaft counts even though its tip is
                # a part of it.
                elif (isinstance(m, VMobject) and id(m) not in word_ids and len(m.points)
                      and not getattr(m, "attention", False)
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
            # picture's own labels, which nothing here can see. Words on their own
            # tag or band carry their ground with them.
            if not piece["panel"] and any(x0 < p[2] and p[0] < x1 and y0 < p[3] and p[1] < y1
                                          for p in laid_on):
                on_pictures.append(piece["text"][:40])
        collisions = self._collisions(drawn, texts)
        boxes = ([t["box"] for t in texts] + pictures
                 + [[p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()]
                    for _, p in drawn])
        extent = ([round(float(min(b[0] for b in boxes))), round(float(min(b[1] for b in boxes))),
                   round(float(max(b[2] for b in boxes))), round(float(max(b[3] for b in boxes)))]
                  if boxes else None)
        graphics = [top for top in self.shown
                    if not isinstance(top, text_kinds)
                    and any(id(m) not in word_ids and (isinstance(m, ImageMobject) or (
                        isinstance(m, VMobject) and len(m.points)
                        and (m.get_stroke_opacity() > 0.3 or m.get_fill_opacity() > 0.3)))
                            for m in top.get_family())]
        # The scene's own ground -- its backdrop, painted or a gradient, or a painting
        # edge to edge -- runs to the frame's edges by design.
        art = self._backdrop is not None or any(
            getattr(m, "scenic", False) for top in self.shown for m in top.get_family())
        self._snapshots.append({"at": round(self.now, 2), "beat": beat, "texts": texts,
                                "art": art,
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
    Path("decisions.json").write_text(json.dumps(scene._decisions, indent=1), encoding="utf-8")
    Path("layout.json").write_text(json.dumps({
        "renderer": "manim", "width": BRIEF.width, "height": BRIEF.height,
        "snapshots": scene._snapshots, "plays": scene._plays}, indent=1, ensure_ascii=False),
        encoding="utf-8")
