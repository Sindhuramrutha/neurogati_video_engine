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
            # A stand-in until a summary is written: the slide's own text is the
            # section's source, not a line about what the viewer learns.
            summary=slide["title"], summary_origin="rule",
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

    from pipeline.lesson_plan import save_plan
    from pipeline.planning import LESSON_FRAME_PARTS

    saved = save_plan(project, Plan(
        sections=sections,
        lesson_frame=previous.lesson_frame if previous.sections else LESSON_FRAME_PARTS,
        approach=previous.approach, approach_options=previous.approach_options,
        approach_notes=previous.approach_notes,
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
        "section_count": len(sections),
        "coverage": coverage,
    }


def resync_plan_with_deck(slug: str) -> dict[str, Any]:
    """Bring a deck-following plan back in step with the deck, keeping its edits.

    A section whose slide is still there is kept exactly as it is: its title,
    summary, role, links and pin. A new slide gets a new section where the deck
    has it; a section whose slides are all gone is removed. Sections that follow
    no slide (the lesson frame, anything added by hand) stay where they were.
    The same plan and deck always give the same result.
    """
    from pipeline.core import OperationFailed, require_project
    from pipeline.extraction import ExtractionStore
    from pipeline.lesson_plan import save_plan
    from pipeline.planning import PlanSection, PlanStore, SourceReference
    from pipeline.presentation import present_artifact

    project = require_project(slug)
    extraction = ExtractionStore(project.root).load()
    slides = {(s["file_name"], s["number"]): s for s in slides_in(extraction)}
    if not slides:
        raise OperationFailed("The extraction has no slides to re-sync with.")
    plan = PlanStore(project.root).load()

    covered, kept, removed = set(), [], []
    for section in plan.sections:
        on_slides = [r for r in section.sources if r.slide_number]
        if not on_slides:
            kept.append(section)
            continue
        section.sources = [r for r in section.sources
                           if not r.slide_number or (r.file_name, r.slide_number) in slides]
        if any(r.slide_number for r in section.sources):
            covered.update((r.file_name, r.slide_number) for r in section.sources)
            kept.append(section)
        else:
            removed.append(section.title or "Untitled")

    added = []
    for key, slide in slides.items():
        if key in covered:
            continue
        new = PlanSection(
            id=f"slide-{slide['number']:03d}", title=slide["title"], summary=slide["title"],
            summary_origin="rule", rendering_approach="slide",
            rendering_reason="This section is a slide of the source deck and is shown as "
                             "that slide.",
            sources=[SourceReference(file_name=slide["file_name"],
                                     heading_path=[slide["title"]],
                                     slide_number=slide["number"])])
        # After the last kept section that covers an earlier slide of the same deck.
        at = 0
        for index, section in enumerate(kept):
            if any(r.file_name == key[0] and 0 < r.slide_number < key[1]
                   for r in section.sources):
                at = index + 1
        kept.insert(at, new)
        added.append(new.title)

    plan.sections = kept
    plan.extraction_fingerprint = extraction.content_fingerprint()
    saved = save_plan(project, plan)
    return present_artifact(project, "plan", saved) | {
        "resync": {"added": added, "removed": removed}}


def _seconds_for(text: str) -> int:
    words = len(text.split())
    return int(max(SHORTEST_SLIDE_SECONDS,
                   min(LONGEST_SLIDE_SECONDS, words * SECONDS_PER_WORD)))


def slides_of(section) -> list[int]:
    numbers: list[int] = []
    for source in section.sources:
        if source.slide_number and source.slide_number not in numbers:
            numbers.append(source.slide_number)
    return numbers


def slide_for_scene(section, scene_index: int, scene_count: int, merged: str = "each") -> int:
    """Which slide a scene shows. A section of several slides moves through them
    in order as its scenes go, evenly; or stays on the first, when that is chosen."""
    numbers = slides_of(section)
    if not numbers:
        return 0
    if merged == "first" or scene_count <= 0:
        return numbers[0]
    return numbers[min(len(numbers) - 1, scene_index * len(numbers) // scene_count)]


def scene_slide(plan, section, scene_index: int, scene_count: int) -> int:
    """`slide_for_scene`, with the plan's own choice for sections of several slides."""
    return slide_for_scene(section, scene_index, scene_count,
                           plan.approach_options.get("merged", "each"))


def coverage_of(slides: list[dict[str, Any]], sections: list) -> dict[str, Any]:
    """Whether the plan still covers every slide, in the deck's order."""
    wanted = [slide["number"] for slide in slides]
    covered: list[int] = []
    for section in sections:
        # Every slide a section covers: one made of several slides covers them all.
        covered.extend(slides_of(section))

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
        if not slides_of(section):
            continue        # the lesson frame, or a section of another source
        entry = next((e for e in script.section_scripts if e.section_id == section.id), None)
        count = max(1, len(entry.scenes) if entry else 0)
        merged = plan.approach_options.get("merged", "each")
        scene_slides.extend(slide_for_scene(section, i, count, merged) for i in range(count))

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
    unseen = [s["number"] for s in slides if s["number"] not in set(scene_slides)
              and s["number"] not in coverage["missing_slides"]]
    if unseen:
        warnings.append(
            f"{len(unseen)} slide(s) get no scene of their own, so they are never shown: "
            f"{', '.join(map(str, unseen[:8]))}. Write more scenes for their section."
        )

    return coverage | {
        "scene_count": len(scene_slides),
        "scenes_per_slide": round(len(scene_slides) / len(slides), 2) if slides else 0,
        "follows_the_deck": coverage["is_complete"] and not unseen,
        "warnings": warnings,
    }
