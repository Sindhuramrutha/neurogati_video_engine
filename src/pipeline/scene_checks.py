"""The mechanical validation a scene program's clip goes through before it may be
used. Fixed rules; the same clip, layout and brief always give the same results.

- **Renderer**: the code uses the renderer its specification names (Manim,
  matplotlib, Pillow, the web kit, or a Revideo scene).
- **Duration**: the clip is within 5% of the narration's measured length.
- **Text** (from `layout.json`, which `manimkit` writes at every beat):
  - inside the frame with a 5% margin
  - no two pieces on screen at once overlapping, and none laid on a picture
  - contrast of at least 4.5:1 against what is behind it
  - lines at least 36 px tall at 1080p
  - never a paragraph: at most 18 words in one piece, 25 on screen at once
- **Shapes** (from `layout.json`): no outline crosses words, no box or circle
  runs through another, and at its fullest the scene spans a good part of the
  frame -- not one strip of it with the rest empty.
- **A picture of the idea**: at half the beats or more, at least two things on
  screen are not words (shapes, arrows, nodes, a timeline, a chart)
- **Grounding**: every number on screen is in the narration, brief or source,
  and most of the words of each piece are too.
- **Frames** (sampled from the clip): not blank, nothing cut at an edge, and at
  least three visibly different moments -- a scene is not a still slide. The
  sampled frames are kept in `frames/` for the visual review.
- **Motion that explains** (from `layout.json`): at least a few things
  transform, move, grow or are drawn -- not only faded in and out. Things
  coming on as they are named are what a scene is, so they never count against
  it.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from pipeline.plan_handoff import FAIL, NOT_APPLICABLE, PASS, WARN, _check
from pipeline.rendering import _hex_to_rgb
from pipeline.storage.documents import read_json_object

FLATTEST_FRAME = 3.0                # standard deviation of brightness, 0-255
POSTER_SAMPLE = 4                   # the frame at 85%, kept as the scene's poster
FRAME_SHARES = (0.05, 0.25, 0.45, 0.65, 0.85, 0.97)
# Animations that only show or hide something. Everything else -- transforming,
# moving, growing, drawing a shape, tracing, indicating -- explains by motion.
APPEAR_ONLY = {"FadeIn", "FadeOut", "Write", "Unwrite", "AddTextLetterByLetter",
               "RemoveTextLetterByLetter", "ShowIncreasingSubsets", "Wait", "Add", "Remove"}
LEAST_EXPLAINING_MOTIONS = 3

# The renderers a scene PROGRAM may name in its spec, and the import that proves it
# uses that renderer.
RENDERERS = {
    "manim": ("from manim", "import manim"),
    "matplotlib": ("matplotlib",),
    "pillow": ("from PIL", "import PIL", "scenekit"),
    "web": ("/kit/webkit.js",),
    "revideo": ("makeScene2D",),
}
UNWIRED_RENDERERS: dict[str, str] = {}

MOST_DURATION_DRIFT = 0.05
MARGIN = 0.05
LEAST_CONTRAST = 4.5
SMALLEST_LINE_PX = 36
MOST_WORDS_IN_A_PIECE = 18
MOST_WORDS_ON_SCREEN = 25
LEAST_GRAPHICS = 2              # non-text elements on screen at a beat
LEAST_PICTURED_SHARE = 0.5      # of the beats
LEAST_GROUNDED_SHARE = 0.6
LEAST_FILLED_HEIGHT = 0.4       # of the frame, at the scene's fullest moment
LEAST_FILLED_WIDTH = 0.5
LEAST_DISTINCT_MOMENTS = 3
# Mean absolute difference, 0-255. One new label on a 1080p frame moves the mean
# by about 1.5-2; a still frame by under 0.5.
DISTINCT_FRAME_DIFFERENCE = 1.2
MOST_EDGE_INK_SHARE = 0.02

_STOP = set("""about above after again also because been before being between both could
does doing down during each from have having here into itself just more most other over
same should some such than that their them then there these they this those through under
until very what when where which while will with would your yours you the and for are
but not can its it's our out who how why all any""".split())


def _hex(colour: str) -> tuple[int, int, int]:
    return _hex_to_rgb(colour.lstrip("#")[:6], (0, 0, 0))


def _contrast(first: str, second: str) -> float:
    from pipeline.project_look import contrast

    return contrast(_hex(first), _hex(second))


def _vocabulary(*texts: str) -> set[str]:
    found = set()
    for text in texts:
        for word in re.findall(r"[a-z0-9]+", text.lower()):
            found.add(word[:5] if word.isalpha() else word)
    return found


def _content_words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower())
            if (w.isdigit() or len(w) >= 4) and w not in _STOP]


# --- the code and its length --------------------------------------------------------------


def renderer_check(code: str, renderer: str) -> dict[str, str]:
    rule = "The code imports the renderer its specification names"
    if renderer in UNWIRED_RENDERERS:
        return _check("renderer", "Renderer is wired", rule, FAIL, UNWIRED_RENDERERS[renderer])
    markers = RENDERERS.get(renderer)
    if markers is None:
        return _check("renderer", "Renderer is wired", rule, FAIL,
                      f"“{renderer or 'none'}” is not a renderer here: "
                      + ", ".join(RENDERERS) + ".")
    found = any(marker in code for marker in markers)
    return _check("renderer", "Renderer is wired", rule, PASS if found else FAIL,
                  f"It imports {renderer}." if found
                  else f"The specification says {renderer}, but the code does not import it.")


def duration_check(clip_seconds: float, narration_seconds: float) -> dict[str, str]:
    drift = abs(clip_seconds - narration_seconds) / narration_seconds if narration_seconds else 1
    return _check(
        "duration", "Length matches the narration",
        f"Within {MOST_DURATION_DRIFT:.0%} of the narration's measured length",
        PASS if drift <= MOST_DURATION_DRIFT else FAIL,
        f"{clip_seconds:.2f} s of picture for {narration_seconds:.2f} s of narration "
        f"({drift:.1%} apart).")


# --- the text, from layout.json -------------------------------------------------------------


def _overlap(a: list[int], b: list[int]) -> bool:
    return min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])


def text_checks(layout: dict | None, brief: dict[str, Any]) -> list[dict[str, str]]:
    if not layout or not layout.get("snapshots"):
        detail = "This renderer does not record its text, so its text is not checked."
        if layout is None and brief.get("renderer") == "manim":
            return [_check("layout", "Text is recorded", "manimkit writes layout.json",
                           FAIL, "There is no layout.json: build the scene with manimkit.")]
        return [_check("layout", "Text is recorded", "manimkit writes layout.json",
                       WARN, detail)]
    width, height = brief["width"], brief["height"]
    left, top = width * MARGIN, height * MARGIN
    right, bottom = width * (1 - MARGIN), height * (1 - MARGIN)
    vocabulary = _vocabulary(brief.get("narration", ""), brief.get("on_screen", ""),
                             brief.get("source_text", ""), brief.get("section_title", ""),
                             brief.get("headline", ""))
    outside, overlaps, faint, small, paragraphs, ungrounded = [], [], [], [], [], []
    # Larger for a classroom projector (Video setup's platforms).
    smallest = int(brief.get("smallest_text_px") or SMALLEST_LINE_PX)
    seen: set[str] = set()
    for snapshot in layout["snapshots"]:
        texts = snapshot["texts"]
        at = f"at {snapshot['at']} s"
        if sum(len(t["text"].split()) for t in texts) > MOST_WORDS_ON_SCREEN:
            paragraphs.append(f"{sum(len(t['text'].split()) for t in texts)} words on screen {at}")
        overlaps += [f"“{text}” on the slide's picture {at}, over what is drawn there: put "
                     "it beside the picture and point to it"
                     for text in snapshot.get("on_pictures", [])]
        for index, piece in enumerate(texts):
            name, (x0, y0, x1, y1) = piece["text"][:40], piece["box"]
            if x0 < left or y0 < top or x1 > right or y1 > bottom:
                outside.append(f"“{name}” {at}")
            for other in texts[index + 1:]:
                if _overlap(piece["box"], other["box"]):
                    overlaps.append(f"“{name}” and “{other['text'][:40]}” {at}")
            ratio = _contrast(piece["color"], piece["behind"])
            if ratio < LEAST_CONTRAST:
                faint.append(f"“{name}” ({ratio}:1)")
            if piece["line_height"] < smallest:
                small.append(f"“{name}” ({piece['line_height']} px)")
            if len(piece["text"].split()) > MOST_WORDS_IN_A_PIECE:
                paragraphs.append(f"“{name}…” is {len(piece['text'].split())} words")
            if piece["text"] in seen:
                continue
            seen.add(piece["text"])
            words = _content_words(piece["text"])
            numbers = [w for w in words if w.isdigit() and w not in vocabulary]
            grounded = [w for w in words if (w if w.isdigit() else w[:5]) in vocabulary]
            if numbers or (len(words) >= 2 and len(grounded) / len(words) < LEAST_GROUNDED_SHARE):
                ungrounded.append(f"“{name}”" + (f" (number {', '.join(numbers)})"
                                                 if numbers else ""))

    snapshots = layout["snapshots"]
    # The beats are the moments the scene rests on; what animations leave between
    # them is checked for collisions and crossings, not counted as beats.
    beats = [s for s in snapshots if s.get("beat", True)] or snapshots
    pictured = sum(1 for s in beats if s.get("graphics", 0) >= LEAST_GRAPHICS)
    share = pictured / len(beats)
    words_only = [f"{s['at']} s" for s in beats if s.get("graphics", 0) < LEAST_GRAPHICS]

    def result(key, name, rule, found):
        return _check(key, name, rule, FAIL if found else PASS,
                      "; ".join(dict.fromkeys(found))[:400] if found else "None found.")

    return [
        result("bounds", "Text inside the frame", "Every piece of text keeps a 5% margin",
               outside),
        result("overlap", "No overlapping text",
               "No two pieces on screen at once overlap, and none lies on a picture", overlaps),
        result("contrast", "Text is high contrast",
               f"At least {LEAST_CONTRAST}:1 against what is behind it", faint),
        _legible(small, smallest),
        result("paragraphs", "No paragraph on screen",
               f"At most {MOST_WORDS_IN_A_PIECE} words in one piece and "
               f"{MOST_WORDS_ON_SCREEN} on screen at once", paragraphs),
        result("grounded", "On-screen text is grounded",
               "Every number, and most words, come from the narration, brief or source",
               ungrounded),
        result("crossing", "No shape runs through words",
               "No outline -- a box edge, an arrow, a line, a circle -- passes through text; "
               "words in a box fit inside it",
               [f"a {c['shape']} through “{c['text']}” at {s['at']} s"
                for s in snapshots for c in s.get("crossings", [])]),
        *shape_checks(snapshots, width, height),
        _pictures_check(snapshots, brief),
        _check("pictured", "It pictures the idea, not only words",
               f"At {LEAST_PICTURED_SHARE:.0%} of the beats or more, at least "
               f"{LEAST_GRAPHICS} things on screen are not words",
               PASS if share >= LEAST_PICTURED_SHARE else FAIL,
               f"{pictured} of {len(beats)} beats show a picture of the idea."
               + ("" if share >= LEAST_PICTURED_SHARE else
                  " Only words on screen at " + ", ".join(words_only[:8]) + ": put the "
                  "idea's shape there too (a box, an arrow, a node, a timeline, the "
                  "slide's picture), and keep it on screen while the words change.")),
    ]


def shape_checks(snapshots: list[dict], width: int, height: int) -> list[dict[str, str]]:
    """What the text checks cannot see: boxes laid over boxes, and a diagram that
    keeps to one strip of the frame. A scene passed every other check with both."""
    rule = ("No box, circle or other outline runs through another one, and no line or "
            "arrow runs through a box -- it stops at the edge")
    if not any("collisions" in s for s in snapshots):
        collide = _check("collide", "No shapes collide", rule, NOT_APPLICABLE,
                         "This renderer does not record its shapes.")
    else:
        found = [f"the {c['a']} and the {c['b']} at {s['at']} s"
                 for s in snapshots for c in s.get("collisions", [])]
        collide = _check("collide", "No shapes collide", rule, FAIL if found else PASS,
                         "; ".join(dict.fromkeys(found))[:400] + ". Lay them out apart -- "
                         "self.row/column/flow/hub/timeline place them so they cannot meet."
                         if found else "None found.")
    rule = (f"At its fullest, what is on screen spans at least {LEAST_FILLED_HEIGHT:.0%} of "
            f"the frame's height and {LEAST_FILLED_WIDTH:.0%} of its width")
    extents = [s["extent"] for s in snapshots if s.get("extent")]
    if not any("extent" in s for s in snapshots):
        return [collide, _check("fills", "The frame is used", rule, NOT_APPLICABLE,
                                "This renderer does not record where things are.")]
    tall = max(((e[3] - e[1]) / height for e in extents), default=0.0)
    wide = max(((e[2] - e[0]) / width for e in extents), default=0.0)
    used = tall >= LEAST_FILLED_HEIGHT and wide >= LEAST_FILLED_WIDTH
    return [collide, _check(
        "fills", "The frame is used", rule, PASS if used else FAIL,
        f"At most {tall:.0%} of the height and {wide:.0%} of the width is used."
        + ("" if used else " The diagram sits in one strip with the rest of the frame "
           "empty: make it bigger and spread it over the frame -- larger shapes, more "
           "space between them, or the slide's picture beside it."))]


def _legible(small: list[str], smallest: int = SMALLEST_LINE_PX) -> dict[str, str]:
    rule = f"Lines at least {smallest} px tall at 1080p"
    if not small:
        return _check("legible", "Text is large enough", rule, PASS, "None found.")
    return _check("legible", "Text is large enough", rule, FAIL,
                  "; ".join(dict.fromkeys(small))[:400] + f". A label of size {smallest} "
                  "or more "
                  "is large enough as made: these were shrunk afterwards, by .scale() on "
                  "them or a group holding them, or by row/column/safe fitting too much "
                  "into the frame. Keep the size: take older things off screen, or give "
                  "the words fewer, shorter pieces, instead of scaling down.")


def _pictures_check(snapshots: list[dict], brief: dict[str, Any]) -> dict[str, str]:
    """A section whose slides have pictures shows them: the slide's own figure,
    explained on screen, not left out for shapes drawn from nothing."""
    offered = (brief.get("assets") or {}).get("pictures") or []
    shown = any(s.get("pictures") for s in snapshots)
    if not offered:
        return _check("pictures", "Uses the slide's pictures",
                      "Shows a picture from its section's slides, when there is one",
                      NOT_APPLICABLE, "Its section has no pictures.")
    return _check("pictures", "Uses the slide's pictures",
                  "Shows a picture from its section's slides, when there is one",
                  PASS if shown else FAIL,
                  "It shows one of them." if shown else
                  f"Its section has {len(offered)} picture(s), and it shows none.")


# --- the frames ---------------------------------------------------------------------------


def _frame(video: Path, at: float, target: Path):
    from PIL import Image

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return None
    subprocess.run([ffmpeg, "-y", "-v", "error", "-ss", f"{at:.2f}", "-i", str(video),
                    "-frames:v", "1", str(target)], capture_output=True, check=False, timeout=60)
    if not target.exists():
        return None
    with Image.open(target) as image:
        return image.convert("RGB").copy()


def frame_checks(video: Path, seconds: float, background: str, folder: Path) -> list[dict]:
    from PIL import ImageChops, ImageStat

    kept = folder / "frames"
    shutil.rmtree(kept, ignore_errors=True)
    kept.mkdir(parents=True, exist_ok=True)
    frames = []
    for index, share in enumerate(FRAME_SHARES):
        target = kept / f"frame-{index}.png"
        frames.append(_frame(video, seconds * share, target))
        if index == POSTER_SAMPLE and target.exists():
            shutil.copy(target, folder / "poster.png")
    frames = [f for f in frames if f is not None]
    if not frames:
        return [_check("frames", "Frames can be read", "Sampled frames open", FAIL,
                       "No frame could be read from the clip.")]

    blank = [i for i, f in enumerate(frames)
             if ImageStat.Stat(f.convert("L")).stddev[0] < FLATTEST_FRAME]
    distinct, last = 1, frames[0]
    changes = []
    for frame in frames[1:]:
        difference = ImageStat.Stat(ImageChops.difference(frame, last).convert("L")).mean[0]
        changes.append(round(difference, 1))
        if difference > DISTINCT_FRAME_DIFFERENCE:
            distinct, last = distinct + 1, frame

    back = _hex(background)
    edge_ink = 0.0
    for frame in frames:
        width, height = frame.size
        border = [frame.getpixel((x, y)) for x in range(0, width, 8) for y in (1, height - 2)]
        border += [frame.getpixel((x, y)) for y in range(0, height, 8) for x in (1, width - 2)]
        ink = sum(1 for p in border if sum(abs(a - b) for a, b in zip(p, back, strict=False)) > 60)
        edge_ink = max(edge_ink, ink / len(border))

    return [
        _check("not-blank", "No blank frame", "No sampled frame is one flat colour",
               FAIL if blank else PASS,
               f"{len(blank)} of {len(frames)} sampled frames are blank." if blank
               else f"{len(frames)} frames sampled, none blank."),
        _check("edges", "Nothing cut at the edge",
               f"Under {MOST_EDGE_INK_SHARE:.0%} of the outermost pixels differ from the "
               "background", FAIL if edge_ink > MOST_EDGE_INK_SHARE else PASS,
               f"{edge_ink:.1%} of the edge is drawn on."),
        _check("moments", "It explains in steps, not a still",
               f"At least {LEAST_DISTINCT_MOMENTS} visibly different moments",
               FAIL if distinct < LEAST_DISTINCT_MOMENTS else PASS,
               f"{distinct} distinct moment(s) in {len(frames)} samples taken evenly "
               f"through the scene (change since the last distinct one: {changes}). "
               + ("" if distinct >= LEAST_DISTINCT_MOMENTS else
                  "The screen barely changes for long stretches: keep new things arriving, "
                  "moving or leaving through the WHOLE scene, on the words as they come, "
                  "not only near the start.")),
    ]


def motion_check(layout: dict | None) -> dict[str, str]:
    """Not only "things in, things out": some of what happens must transform,
    move, grow or draw. A count, not a share: bringing each thing on as it is
    named is what a scene does, and more of that must never fail it."""
    rule = (f"At least {LEAST_EXPLAINING_MOTIONS} animations transform, move, grow or draw "
            "-- not only fade or write in and out")
    plays = (layout or {}).get("plays")
    if plays is None:
        return _check("motion", "Motion explains", rule, NOT_APPLICABLE,
                      "This renderer does not record its animations.")
    motions = [name for play in plays for name in play if name not in ("Wait",)]
    explaining = [name for name in motions if name not in APPEAR_ONLY]
    good = len(explaining) >= LEAST_EXPLAINING_MOTIONS
    kinds = ", ".join(sorted(set(explaining))[:6]) or "none"
    return _check("motion", "Motion explains", rule, PASS if good else FAIL,
                  f"{len(explaining)} of {len(motions)} animations explain by motion "
                  f"({kinds}). " + ("" if good else
                  "Only fading and writing things in and out does not: make things MOVE or "
                  "CHANGE -- one thing transforming into another, an arrow growing from one "
                  "idea to the next, an element moving to where it is compared, a dot "
                  "travelling along a path (Manim: ReplacementTransform, GrowArrow, "
                  ".animate.shift, MoveAlongPath, Indicate; web: gsap x/y/morph; see "
                  "motion.md). Never shrink something with words in it to make motion: "
                  "its words become too small to read."))


def program_checks(folder: Path, brief: dict[str, Any], clip_seconds: float) -> list[dict]:
    """Every program check, from what is in the scene's folder."""
    from pipeline.scene_program import entry_of

    renderer, entry = entry_of(folder)
    code = (folder / entry).read_text(encoding="utf-8") if (folder / entry).exists() else ""
    checks = [renderer_check(code, renderer),
              duration_check(clip_seconds, brief["seconds"])]
    layout = read_json_object(folder / "layout.json", "scene layout")
    checks += text_checks(layout, brief | {"renderer": renderer})
    checks.append(motion_check(layout))
    checks += frame_checks(folder / "render.mp4", clip_seconds,
                           brief["look"]["background"], folder)
    return checks
