"""Whether a plan keeps the slides' order -- held by code, not by trusting a model.

The person chooses how strictly the deck's order is kept (`SLIDE_ORDERS`):

- **strict**: each section is an unbroken run of slides, ascending, and the runs
  follow one another through the deck. Slide 10's topic can never come first.
- **nearly**: sections follow the deck by their first slide; inside a section
  the slides may be in any order. No slide is used twice.
- **loose**: no slide is used twice; the order is a guide.
- **free**: only that every slide named exists.

Under every rule, a slide the plan does not cover must be left out on purpose,
with a reason, or it is reported. The same plan always gives the same problems.
"""

from __future__ import annotations

from typing import Any


def _runs(slides: list[int]) -> bool:
    return slides == list(range(slides[0], slides[0] + len(slides))) if slides else True


def order_problems(sections: list[tuple[str, list[int]]], rule: str) -> list[str]:
    """`sections` is each body section's title and slides, in the plan's order."""
    problems: list[str] = []
    seen: dict[int, str] = {}
    for title, slides in sections:
        for slide in slides:
            if slide in seen and rule != "free":
                problems.append(f"slide {slide} is in both “{seen[slide]}” and “{title}”")
            seen.setdefault(slide, title)
    if rule == "strict":
        for title, slides in sections:
            if not _runs(slides):
                problems.append(f"“{title}” is not one unbroken run of slides, in order "
                                f"({', '.join(map(str, slides))})")
    if rule in ("strict", "nearly"):
        firsts = [(min(slides), title) for title, slides in sections if slides]
        for (was, before), (now, after) in zip(firsts, firsts[1:], strict=False):
            if now < was:
                problems.append(f"“{after}” (from slide {now}) comes after “{before}” "
                                f"(from slide {was}), against the deck's order")
    return problems


def coverage_problems(sections: list[tuple[str, list[int]]], all_slides: list[int],
                      left_out: dict[int, str]) -> list[str]:
    """Slides no section covers and that were not left out on purpose, and slides
    named that the deck does not have."""
    covered = {slide for _title, slides in sections for slide in slides}
    known = set(all_slides)
    problems = [f"slide {slide} is not in the deck"
                for slide in sorted(covered - known)]
    missing = [slide for slide in all_slides if slide not in covered and slide not in left_out]
    if missing:
        problems.append(
            f"{len(missing)} slide(s) are not covered and not left out on purpose: "
            + ", ".join(map(str, missing[:20])) + ("…" if len(missing) > 20 else ""))
    return problems


def plan_order_report(plan, units) -> dict[str, Any]:
    """The order and coverage problems of a saved plan's body sections."""
    from pipeline.plan_units import unit_numbers

    body = [(s.title or "Untitled", unit_numbers(s, units)) for s in plan.sections
            if s.sources]
    return {
        "rule": plan.slide_order,
        "order": order_problems(body, plan.slide_order),
        "coverage": coverage_problems(body, [u.number for u in units], plan.slides_left_out),
    }
