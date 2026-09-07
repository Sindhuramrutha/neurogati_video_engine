"""Highlight Planner agent: decides which real slide element to point at, and
when, as a slide's narration plays.

Split into an LLM "grounding" step and a pure-Python "formatting" step on
purpose. The LLM's only job is a closed-set choice -- which real shape_id,
from the list it's given, matches what the narration is currently saying --
never inventing a shape or a position. All of the actual geometry (the
manim_bbox each shape already carries, computed by utils/pptx_reader.py) is
known in advance, so turning a chosen shape_id into the literal Manim
instruction is deterministic formatting, not something worth spending an
LLM call to get right or wrong.
"""

import json

from pydantic import BaseModel

from state import WordTiming
from utils.llm import generate
from utils.pptx_reader import SlideContent

SYSTEM_PROMPT = """You are directing where a presenter's pointer moves across a slide while \
narrating it -- like a professor circling or pointing at part of their own slide as they \
talk about it.

You are given a slide's real elements (each with an id, a kind, and its text or a fallback \
label), the full narration for this slide, and word-level timing for that narration.

For each *distinct span* of narration that is clearly discussing one specific element on the \
slide, choose:
- Which element (by its exact id from the list given -- never invent an id that isn't in the \
list, and never invent an element that isn't there).
- When the highlight should start (a timestamp, in seconds, from the word timing -- the \
moment the narration starts discussing that element).
- What kind of highlight. Each element is given with its actual measured size and a size \
category -- use that number, not a guess from the label text, to decide:
  - "circle" -- the element's size category is "small, roughly square/round" (an icon, a \
number, a short label/name). Always prefer circle over box for these -- a circle around a \
small element looks deliberate, a box around it looks like a mistake.
  - "arrow" -- the element is "short, wide strip" sized AND positioned near an edge of the \
slide (its x or y range is close to the slide's outer bound), where pointing at it reads more \
naturally than outlining it.
  - "box" -- the element's size category is "large block" (a paragraph, a multi-line body of \
text, anything spanning most of the slide's width or height). Do not use "box" for anything \
marked "small, roughly square/round" -- that is always a circle.
  A slide with several small/short elements should end up using a real mix of circle and box, \
not box for everything -- check each element's given size category before choosing, every \
time, rather than defaulting to box.

Rules:
- Only highlight elements the narration is actually, specifically discussing at that moment -- \
not every element needs a highlight, and a purely decorative/background element (no \
meaningful text, not clearly what's being discussed) should usually be skipped entirely.
- Order every choice by timestamp, earliest first.
- CRITICAL -- never emit two beats in a row for the same shape_id with nothing else in \
between. If the narration keeps discussing the same element across several sentences, that is \
ONE beat starting when it's first mentioned, not several repeated beats re-triggering the same \
highlight -- a highlight re-appearing on the same spot over and over reads as flickering, not \
as one deliberate highlight. Only highlight the same shape_id again later if the narration \
moved on to something else in between and then genuinely comes back to it.
- Don't highlight so densely it never stops moving (a highlight should generally stay in place \
for at least a few seconds of narration), and don't leave a long stretch of narration about a \
specific visible element with no highlight at all.

Respond with ONLY a JSON array, no markdown fences, no commentary, in this exact shape:
[
  {"timestamp": 2.4, "shape_id": 5, "highlight": "box", "reason": "narration starts explaining this bullet"},
  ...
]
An empty array `[]` is a valid answer if nothing on the slide warrants a highlight.
"""


class HighlightBeat(BaseModel):
    timestamp: float
    shape_id: int
    highlight: str  # "box" | "circle" | "arrow"
    reason: str


def _timing_block(timestamps: list[WordTiming]) -> str:
    return "\n".join(f"{w.start:.2f}-{w.end:.2f}: {w.word}" for w in timestamps)


def _size_hint(bbox: tuple[float, float, float, float]) -> str:
    """A concrete, pre-computed size qualifier -- deliberately not left for the
    LLM to eyeball from label text alone, which in testing defaulted to "box"
    for everything regardless of actual size (even short 2-word labels).
    Giving it real numbers up front makes the circle/arrow/box choice a much
    more mechanical, reliable decision.
    """
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    area = width * height
    aspect = width / height if height else float("inf")
    if area < 1.2 and 0.4 <= aspect <= 2.5:
        return "small, roughly square/round"
    if height < 0.6:
        return "short, wide strip"
    return "large block"


def _shape_list_block(slide: SlideContent) -> str:
    lines = []
    for s in slide.shapes:
        label = s.text or s.alt_text or f"(unlabeled {s.kind})"
        width = s.manim_bbox[2] - s.manim_bbox[0]
        height = s.manim_bbox[3] - s.manim_bbox[1]
        size = _size_hint(s.manim_bbox)
        lines.append(
            f"- id={s.shape_id}, kind={s.kind}, size={width:.1f}x{height:.1f} units ({size}): {label!r}"
        )
    return "\n".join(lines) if lines else "(no elements with known positions on this slide)"


MAX_JSON_ATTEMPTS = 3


def plan_highlights(slide: SlideContent, narration: str, timestamps: list[WordTiming]) -> list[HighlightBeat]:
    valid_ids = {s.shape_id for s in slide.shapes}
    if not valid_ids:
        return []

    prompt = (
        f"Slide elements:\n{_shape_list_block(slide)}\n\n"
        f"Narration:\n{narration}\n\n"
        f"Word-level timing:\n{_timing_block(timestamps)}"
    )

    last_error = None
    for _ in range(MAX_JSON_ATTEMPTS):
        raw = generate(system=SYSTEM_PROMPT, prompt=prompt, max_tokens=2048)
        try:
            data = json.loads(raw)
            beats = [HighlightBeat(**item) for item in data]
        except (json.JSONDecodeError, TypeError) as exc:
            last_error = exc
            continue

        # Mirrors utils/manim_lint.py's asset-key check, but at planning time: never
        # trust the model's shape_id claim, verify it against the real list ourselves.
        beats = [b for b in beats if b.shape_id in valid_ids]
        beats.sort(key=lambda b: b.timestamp)
        return beats

    raise last_error


def render_prompt_from_highlights(
    slide: SlideContent, beats: list[HighlightBeat], background_asset_key: str, total_duration: float
) -> str:
    shapes_by_id = {s.shape_id: s for s in slide.shapes}

    lines = [
        f"1. 0.00-{total_duration:.2f}: Display the slide background image via "
        f"ImageMobject(ASSET_PATHS['{background_asset_key}']), scaled to fill the frame width "
        f"and centered. This is the ONLY content on screen unless a beat below says otherwise "
        f"-- never add, remove, redraw, resize, or reposition the slide image itself at any "
        f"point in this scene. Keep it static and fully visible for the entire scene duration."
    ]

    for i, beat in enumerate(beats):
        shape = shapes_by_id.get(beat.shape_id)
        if shape is None:
            continue
        x_min, y_min, x_max, y_max = shape.manim_bbox
        label = shape.text or shape.alt_text or f"element {shape.shape_id}"
        end = beats[i + 1].timestamp if i + 1 < len(beats) else total_duration

        pad = 0.12  # small margin so the highlight doesn't hug the text with zero breathing room
        if beat.highlight == "circle":
            cx, cy = (x_min + x_max) / 2, (y_min + y_max) / 2
            ew, eh = (x_max - x_min) + 2 * pad, (y_max - y_min) + 2 * pad
            action = (
                f"Construct `Ellipse(width={ew:.2f}, height={eh:.2f}, color=YELLOW, "
                f"stroke_width=5, fill_opacity=0)` and `.move_to(np.array([{cx:.2f}, {cy:.2f}, "
                f"0]))` -- a single, complete, closed oval outline that fully encloses the "
                f"element with a small even margin on every side. This must be the actual "
                f"`Ellipse` mobject, not an `Arc`, not a partial curve, and not "
                f"`Create`/`DrawBorderThenFill` cut off partway -- animate it in with "
                f"`Create(ellipse)` played to full completion so the closed oval is entirely "
                f"visible, not a swoosh or incomplete arc."
            )
        elif beat.highlight == "arrow":
            cx, cy = (x_min + x_max) / 2, (y_min + y_max) / 2
            # Point in from whichever side of the frame has more open space, so the arrow's
            # tail doesn't overlap the slide content it isn't highlighting.
            from_below = cy > 0
            tail = (cx, cy - 1.4, 0) if from_below else (cx, cy + 1.4, 0)
            action = (
                f"Construct `Arrow(start=np.array({tail!r}), end=np.array([{cx:.2f}, {cy:.2f}, "
                f"0]), color=YELLOW, stroke_width=6, buff=0.1)` -- a single arrow with a clear "
                f"visible tip, pointing directly at that point from outside the element, "
                f"animated in with `Create(arrow)` or `GrowArrow(arrow)`."
            )
        else:
            w, h = (x_max - x_min) + 2 * pad, (y_max - y_min) + 2 * pad
            cx, cy = (x_min + x_max) / 2, (y_min + y_max) / 2
            action = (
                f"Construct `Rectangle(width={w:.2f}, height={h:.2f}, color=YELLOW, "
                f"stroke_width=5, fill_opacity=0)` and `.move_to(np.array([{cx:.2f}, {cy:.2f}, "
                f"0]))` -- a single complete rectangle outline fully enclosing the element with "
                f"a small even margin on every side, animated in with `Create(rectangle)` "
                f"played to full completion."
            )

        lines.append(
            f"{i + 2}. {beat.timestamp:.2f}-{end:.2f}: {action} This corresponds to "
            f"{label!r} on the slide -- {beat.reason}. Fade this highlight out at the end of "
            f"this beat (before the next beat's highlight, if any, appears); do not leave "
            f"multiple highlights on screen at once."
        )

    return "\n".join(lines)
