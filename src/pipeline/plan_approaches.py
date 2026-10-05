"""How to build the outline: a choice of approach, a few options, and your own words.

There used to be one rule (a section per slide) and one open-ended draft. How a
lesson is put together is a teaching decision, so it is a choice here, made
before anything is built:

- **Follow the deck** and **By hand** use no AI.
- The rest steer the Scene Plan agent's draft with a fixed instruction for that
  approach, the options, and whatever the person adds. The result is a draft
  beside the plan, accepted whole or section by section, as always.

The instruction an approach sends is composed here from fixed text, so the same
choice always sends the same words. What was chosen is kept on the plan.
"""

from __future__ import annotations

from typing import Any

from pipeline.core import OperationFailed, require_project

APPROACHES = [
    {"key": "follow-deck", "name": "Follow the deck", "uses_ai": False, "needs_deck": True,
     "does": "One section per slide, every slide, in the deck's order.",
     "when": "The deck is already a good lesson."},
    {"key": "group-ideas", "name": "Group into ideas", "uses_ai": True, "needs_deck": False,
     "does": "Neighbouring slides or headings that make one idea become one section. "
             "Nothing is reordered or skipped.",
     "when": "The deck spreads one idea over several slides.",
     "instruction": "Group neighbouring parts that make ONE idea into one section. Keep the "
                    "source's own order exactly: never reorder, and never skip a part that "
                    "teaches something. A section may cover several slides or headings."},
    {"key": "story-first", "name": "Story first", "uses_ai": True, "needs_deck": False,
     "does": "Opens on the story or case in the material, told in order, then explains "
             "what lies behind it.",
     "when": "The material has a person, a case or an event.",
     "instruction": "Lead with the story or case in the material: tell it first, in the "
                    "order it happened, in sections whose role is story. Only then explain "
                    "the ideas behind it, in sections whose role is teach, each tied back "
                    "to the story."},
    {"key": "concept-first", "name": "Concept first", "uses_ai": True, "needs_deck": False,
     "does": "Builds the ideas from the simplest up, then shows them at work in the "
             "examples.",
     "when": "The viewer needs the basics before the examples make sense.",
     "instruction": "Build the ideas from the simplest to the hardest, each section resting "
                    "on the one before. Put the examples, cases and stories after the idea "
                    "they show, in sections whose role is story."},
    {"key": "question-led", "name": "Question led", "uses_ai": True, "needs_deck": False,
     "does": "Every section answers one question the viewer would ask, in the order "
             "they would ask it.",
     "when": "The topic is best learnt by asking why and how.",
     "instruction": "Make every section answer ONE question a curious viewer would ask, in "
                    "the order they would ask it. Write each section's title as that "
                    "question."},
    {"key": "by-hand", "name": "By hand", "uses_ai": False, "needs_deck": False,
     "does": "You add each section and write it.",
     "when": "You already know the structure."},
]

OPTIONS = [
    {"key": "sections", "label": "How many sections", "for_ai": True, "default": "auto",
     "choices": {"auto": "Let the material decide", "few": "A few (3 to 5)",
                 "some": "Some (6 to 9)", "many": "Many (10 or more)"},
     "instruction": {"few": "Use 3 to 5 sections.", "some": "Use 6 to 9 sections.",
                     "many": "Use 10 or more sections, each on one small idea."}},
    {"key": "longest", "label": "Longest section", "for_ai": True, "default": "120",
     "choices": {"60": "1 minute", "90": "1.5 minutes", "120": "2 minutes", "180": "3 minutes"},
     "instruction": {k: f"No section should run longer than {k} seconds; split one that would."
                     for k in ("60", "90", "120", "180")}},
    {"key": "merged", "label": "A section covering several slides shows", "for_ai": False,
     "default": "each",
     "choices": {"each": "Each slide in turn, as the narration moves",
                 "first": "Only its first slide"}},
]
LONGEST_NOTES = 600


def approach_view(plan, has_deck: bool) -> dict[str, Any]:
    """The choices the page offers, and what this plan was last built with."""
    chosen = {o["key"]: plan.approach_options.get(o["key"], o["default"]) for o in OPTIONS}
    return {
        "approaches": [{k: v for k, v in a.items() if k != "instruction"}
                       | {"available": has_deck or not a["needs_deck"]} for a in APPROACHES],
        "options": [{k: v for k, v in o.items() if k != "instruction"} for o in OPTIONS],
        "chosen": plan.approach or ("follow-deck" if has_deck else "group-ideas"),
        "chosen_options": chosen,
        "notes": plan.approach_notes,
    }


def instruction_for(approach: str, options: dict[str, str], notes: str) -> str:
    """Exactly what an approach sends to the agent."""
    found = next((a for a in APPROACHES if a["key"] == approach), None)
    if found is None or not found["uses_ai"]:
        return ""
    parts = [found["instruction"]]
    for option in OPTIONS:
        line = option.get("instruction", {}).get(options.get(option["key"], option["default"]))
        if line:
            parts.append(line)
    if notes.strip():
        parts.append(f"From the person planning this video: {notes.strip()[:LONGEST_NOTES]}")
    return " ".join(parts)


def _attach_slides(extraction, sections: list[dict[str, Any]]) -> None:
    """A drafted section names a deck's headings; say which slides those are, so
    the video can show them. A slide is given to the first section that names it."""
    taken: set[tuple[str, int]] = set()
    for section in sections:
        for source in section.get("sources", []):
            document = extraction.document(source.get("file_name", ""))
            if document is None or source.get("slide_number"):
                continue
            for block in document.blocks:
                key = (document.file_name, block.slide_number)
                if (block.kind == "heading" and block.slide_number and key not in taken
                        and block.heading_path == source.get("heading_path")):
                    source["slide_number"] = block.slide_number
                    taken.add(key)
                    break


def build_outline(slug: str, approach: str, options: dict[str, str], notes: str) -> dict[str, Any]:
    """Build with the chosen approach. Returns what was made: a plan, or a draft."""
    from pipeline.extraction import ExtractionStore
    from pipeline.planning import PlanDraftStore, PlanStore

    found = next((a for a in APPROACHES if a["key"] == approach), None)
    if found is None:
        raise OperationFailed(f"{approach!r} is not a planning approach.")
    cleaned = {}
    for option in OPTIONS:
        value = options.get(option["key"], option["default"])
        if value not in option["choices"]:
            raise OperationFailed(f"{option['label']} cannot be {value!r}.")
        cleaned[option["key"]] = value

    project = require_project(slug)
    store = PlanStore(project.root)
    plan = store.load()
    plan.approach, plan.approach_options = approach, cleaned
    plan.approach_notes = notes.strip()[:LONGEST_NOTES]
    store.save(plan)

    if approach == "by-hand":
        return {"made": "nothing"}
    if approach == "follow-deck":
        from pipeline.slide_plan import plan_from_slides
        plan_from_slides(slug)
        return {"made": "plan"}

    from pipeline.plan_drafting import draft_plan
    draft_plan(slug, instruction_for(approach, cleaned, notes))
    drafts = PlanDraftStore(project.root)
    draft = drafts.load()
    if draft:
        _attach_slides(ExtractionStore(project.root).load(), draft["plan"]["sections"])
        drafts.save(draft | {"approach": found["name"]})
    return {"made": "draft"}
