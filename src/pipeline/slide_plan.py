"""Building a video's spine from a deck's own slides.

The normal path asks a model to group the source material into sections, which
is right for a chapter or a paper: the shape of the video is a judgement about
the content. A deck is different. Somebody already decided the order and the
divisions, slide by slide, and a video made from it that reorders or skips is
worse than one that follows.

So this builds the plan mechanically: **one section per slide, in the deck's
order, every slide**. No model call, nothing to review, nothing that can
silently drop slide 23.

Scenes may outnumber slides -- a dense slide is narrated in two or three beats
and Script & Staging decides how many -- but the order is fixed and the coverage
is total. `slide_coverage` checks exactly that and is meant to be run after
every stage that could disturb it.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Roughly how long a slide's narration runs, from how much is written on it.
# Floor and ceiling because a title slide still needs a beat and a wall of text
# should be split by the script rather than narrated for two minutes.
SECONDS_PER_WORD = 60 / 150
SHORTEST_SLIDE_SECONDS = 10
LONGEST_SLIDE_SECONDS = 75

# What a section's summary shows of the slide it covers.
MAXIMUM_SUMMARY_CHARACTERS = 300


def slides_in(extraction, file_name: str = "") -> list[dict[str, Any]]:
    """Every slide of every deck in the extraction, in order.

    Keyed on the slide number the blocks carry, not on their heading text: two
    slides titled the same are two slides, and the title is all a heading path
    records for a deck.
    """
    found: list[dict[str, Any]] = []
    for document in extraction.documents:
        if file_name and document.file_name != file_name:
            continue
        numbers = sorted({
            block.slide_number for block in document.blocks if block.slide_number
        })
        for number in numbers:
            blocks = [b for b in document.blocks if b.slide_number == number]
            heading = next((b.text for b in blocks if b.kind == "heading"), "")
            words = [b.text for b in blocks if b.kind != "heading" and b.text.strip()]
            found.append({
                "file_name": document.file_name,
                "number": number,
                "title": heading or f"Slide {number}",
                "text": "\n".join(words),
                "figure_count": sum(1 for b in blocks if b.kind == "figure"),
            })
    return found


def plan_from_slides(slug: str, file_name: str = "") -> dict[str, Any]:
    """Replace the plan with one section per slide, in the deck's order.

    Deliberately destructive and never automatic: it throws away whatever
    sectioning was there, because its whole purpose is to impose the deck's
    order rather than negotiate with another one.
    """
    from pipeline.core import OperationFailed, require_project
    from pipeline.extraction import ExtractionStore
    from pipeline.planning import Plan, PlanSection, PlanStore, SourceReference
    from pipeline.presentation import present_artifact

    project = require_project(slug)
    extraction = ExtractionStore(project.root).load()
    if not extraction.documents:
        raise OperationFailed(
            f"{project.name} has nothing extracted yet, so there are no slides to "
            f"follow. Run extraction first."
        )

    slides = slides_in(extraction, file_name)
    if not slides:
        named = ", ".join(d.file_name for d in extraction.documents) or "none"
        raise OperationFailed(
            "No slides were found in this project's extraction. This needs a "
            "PowerPoint source extracted with slide numbers; the documents here "
            f"are: {named}."
        )

    store = PlanStore(project.root)
    previous = store.load()

    sections = [
        PlanSection(
            id=f"slide-{slide['number']:03d}",
            title=slide["title"],
            summary=slide["text"][:MAXIMUM_SUMMARY_CHARACTERS],
            estimated_seconds=_seconds_for(slide["text"]),
            rendering_approach="slide",
            rendering_reason="This section is a slide of the source deck and is "
                             "shown as that slide.",
            sources=[SourceReference(
                file_name=slide["file_name"],
                heading_path=[slide["title"]],
                slide_number=slide["number"],
            )],
        )
        for slide in slides
    ]

    saved = store.save(Plan(
        sections=sections,
        # Kept, because they are decisions about the video rather than about the
        # sectioning: an audience, its objectives and the themes outlive a
        # re-plan that only imposes the deck's order.
        selected_audience=previous.selected_audience,
        audience_choices=previous.audience_choices,
        learning_objectives=previous.learning_objectives,
        key_themes=previous.key_themes,
        extraction_fingerprint=previous.extraction_fingerprint,
    ))
    coverage = coverage_of(slides, saved.sections)
    return present_artifact(project, "plan", saved) | {
        "slide_count": len(slides),
        "section_count": len(saved.sections),
        "coverage": coverage,
    }


def _seconds_for(text: str) -> int:
    words = len(text.split())
    return int(max(SHORTEST_SLIDE_SECONDS,
                   min(LONGEST_SLIDE_SECONDS, words * SECONDS_PER_WORD)))


def coverage_of(slides: list[dict[str, Any]], sections: list) -> dict[str, Any]:
    """Whether the plan still covers every slide, in the deck's order."""
    wanted = [slide["number"] for slide in slides]
    covered: list[int] = []
    for section in sections:
        for source in section.sources:
            if source.slide_number:
                covered.append(source.slide_number)
                break

    missing = [number for number in wanted if number not in set(covered)]
    in_order = covered == sorted(covered)
    return {
        "slide_count": len(wanted),
        "covered_count": len(set(covered)),
        "missing_slides": missing,
        "is_in_order": in_order,
        "is_complete": not missing and in_order,
    }


def slide_coverage(slug: str) -> dict[str, Any]:
    """Does the video still follow the deck -- every slide, in order?

    Reported rather than assumed. A model that re-plans, a hand edit that
    deletes a section, or a reordered outline all break the guarantee silently,
    and the whole point of the slide-driven spine is that it cannot be broken
    without somebody being told.
    """
    from pipeline.core import require_project
    from pipeline.extraction import ExtractionStore
    from pipeline.planning import PlanStore
    from pipeline.scripting import ScriptStore

    project = require_project(slug)
    extraction = ExtractionStore(project.root).load()
    plan = PlanStore(project.root).load()
    script = ScriptStore(project.root).load()

    slides = slides_in(extraction)
    coverage = coverage_of(slides, plan.sections)

    # Scenes may outnumber slides; they may never be fewer, and the slide they
    # belong to may never go backwards.
    scene_slides: list[int] = []
    for section in plan.sections:
        number = next((s.slide_number for s in section.sources if s.slide_number), 0)
        entry = next((e for e in script.section_scripts if e.section_id == section.id), None)
        scene_slides.extend([number] * max(1, len(entry.scenes) if entry else 0))

    warnings: list[str] = []
    if coverage["missing_slides"]:
        shown = ", ".join(str(n) for n in coverage["missing_slides"][:8])
        warnings.append(
            f"{len(coverage['missing_slides'])} slide(s) are not covered by any "
            f"section: {shown}. Rebuild the plan from the slides."
        )
    if not coverage["is_in_order"]:
        warnings.append(
            "The sections no longer follow the deck's slide order. Rebuild the "
            "plan from the slides, or reorder them."
        )
    if slides and len(scene_slides) < len(slides):
        warnings.append(
            f"{len(scene_slides)} scene(s) for {len(slides)} slide(s): every slide "
            f"needs at least one. Draft the unwritten sections."
        )

    return coverage | {
        "scene_count": len(scene_slides),
        "scenes_per_slide": round(len(scene_slides) / len(slides), 2) if slides else 0,
        "follows_the_deck": coverage["is_complete"] and len(scene_slides) >= len(slides),
        "warnings": warnings,
    }
