"""What this video is: the course it belongs to, which part of it, and what it teaches.

Every agent that shapes the video is told this before anything else. Without it the
planner saw only a list of slide titles, left the deck's title slide out as "a title
page", and a whole video was planned and narrated without once saying it belongs to
its course or what the viewer will come away with.

  COURSE       the course's name -- by default the title slide's heading.
  THIS VIDEO   which part of the course it is -- by default the deck's file name
               without the course's own words ("Chapter 1").
  TEACHES      what the viewer will come away knowing, in a sentence or two, written
               by the planner with the shape and agreed with it.

Course and This video are the person's, on Scene Plan's setup, filled in from the deck
until they change them. The pictures the person chose on Extraction are listed with
them: each must appear in the video, wherever its slide is or is not taught.
"""

from __future__ import annotations

import re
from pathlib import PurePath

LONGEST_TITLE_SLIDE = 600


def _first_slide_blocks(extraction):
    for document in getattr(extraction, "documents", []) or []:
        blocks = [b for b in document.blocks if (b.slide_number or 0) <= 1]
        return document, blocks or list(document.blocks[:6])
    return None, []


def title_slide_text(extraction) -> str:
    """What the deck's first slide says, word for word (no picture captions)."""
    _document, blocks = _first_slide_blocks(extraction)
    words = [b.text.strip() for b in blocks if b.kind != "figure" and b.text.strip()]
    return " | ".join(dict.fromkeys(words))[:LONGEST_TITLE_SLIDE]


def _plain(text: str) -> str:
    return re.sub(r"[\s_\-]+", " ", text).strip()


def deck_defaults(extraction) -> tuple[str, str]:
    """(course, this video) as the deck states them: the title slide's heading, and
    the file name without the course's words."""
    document, blocks = _first_slide_blocks(extraction)
    if document is None:
        return "", ""
    headings = [b.text.strip() for b in blocks if b.kind == "heading" and b.text.strip()]
    course = headings[0] if headings else ""
    stem = _plain(PurePath(document.file_name).stem)
    this_video = stem
    if course and _plain(course).lower() in stem.lower():
        start = stem.lower().index(_plain(course).lower())
        this_video = _plain(stem[:start] + stem[start + len(_plain(course)):]).strip(" :|")
    return course, this_video or stem


def fill_defaults(plan, extraction) -> bool:
    """Fill an empty Course / This video from the deck. True if anything changed."""
    course, this_video = deck_defaults(extraction)
    changed = False
    if not plan.course and course:
        plan.course, changed = course, True
    if not plan.this_video and this_video:
        plan.this_video, changed = this_video, True
    return changed


def chosen_pictures(project, extraction) -> list[dict[str, object]]:
    """The pictures the person chose: path, their name for it, and its slide."""
    from pipeline.chosen_pictures import chosen

    slides = {}
    for document in getattr(extraction, "documents", []) or []:
        for block in document.blocks:
            if block.asset_path:
                slides.setdefault(block.asset_path, block.slide_number or 0)
    return [{"path": path, "name": name, "slide": slides.get(path, 0)}
            for path, name in chosen(project).items()]


def identity_text(project, plan, extraction) -> str:
    """The block every shaping agent reads first."""
    lines = [
        f"Course: {plan.course or '(not given)'}",
        f"This video: {plan.this_video or '(not given)'}",
    ]
    title = title_slide_text(extraction)
    if title:
        lines.append(f"The deck's title slide says: {title}")
    if plan.teaches:
        lines.append(f"What the viewer will come away with (agreed with the plan): {plan.teaches}")
    picks = chosen_pictures(project, extraction)
    if picks:
        lines.append("Pictures the person chose -- every one must appear in the video:")
        lines += [f"- “{p['name']}” (slide {p['slide'] or '?'})" for p in picks]
    return "\n".join(lines)
