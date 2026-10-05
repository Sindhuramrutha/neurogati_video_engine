"""The plan as a lesson: roles, the frame around the body, time, and objectives.

A plan built from a deck used to be the deck: one section per slide, starting
cold on slide 1, each section as long as its slide was wordy. Nothing opened the
lesson, nothing brought it back together, and the learning objectives were
decoration -- no section served one, and the check that would have said so
skipped itself.

This module turns the plan into a lesson, by fixed rules only:

- **Roles.** Every section is an *opening*, *teach*, *story*, *recap* or *close*.
  The role tells the Scripting agent what the section is for (`ROLE_GUIDE`).
- **The lesson frame.** An Opening (a hook, then what the viewer will learn),
  a Recap (one beat per learning objective) and a Close wrap the body. Each can
  be switched off. Frame sections have fixed ids, so their narration stays
  attached, and they are written from the plan itself rather than the source.
- **Time.** The body's lengths are shared out from the target duration, in
  proportion to how much each section has to teach: its words, and extra for
  each picture it must explain. A length a person set is pinned and kept; the
  rest rebalance. The material is never stretched past the target's upper end
  or squeezed below its lower one, and how far it had to move is reported.
- **Objectives.** Links from sections to objectives are *suggested* by the
  words they share, and a person accepts them. The suggestion names the words.

`shape_plan` applies all of it and runs on every save, so the same plan, the
same extraction and the same target always give the same shape.
"""

from __future__ import annotations

import re
from typing import Any

from pipeline.planning import LESSON_FRAME_PARTS, Plan, PlanSection

FRAME_ROLES = ("opening", "recap", "close")
BODY_ROLES = ("teach", "story")

FRAME_IDS = {"opening": "frame-opening", "recap": "frame-recap", "close": "frame-close"}
FRAME_DEFAULTS = {
    "opening": ("Opening", "Why this matters, and what you will be able to do by the end."),
    "recap": ("Recap", "Back through what you learned, one objective at a time."),
    "close": ("Close", "The one idea to keep, and something to think about next."),
}
OPENING_SECONDS = 25
CLOSE_SECONDS = 15
RECAP_SECONDS_PER_OBJECTIVE = 10

# How long a body section needs, before the target is applied.
SECONDS_PER_WORD = 60 / 150
SECONDS_PER_PICTURE = 12
SHORTEST_BODY_SECONDS = 20
SHORTEST_ANY_SECONDS = 10
# Past these the material is being padded or cut hard; the Check tab says so.
MOST_STRETCH = 1.5
MOST_SQUEEZE = 0.6

ROLE_GUIDE = {
    "opening": "This is the opening of the video. Start with a hook -- a question, a "
               "surprising fact or a moment from the material -- then tell the viewer "
               "plainly what they will be able to do by the end: the learning objectives "
               "below, in your own words. Do not teach the content yet.",
    "teach": "",
    "story": "This section is a story or a case. Tell it yourself, first hand and in "
             "order, then say in one sentence what it shows the viewer.",
    "recap": "This is the recap. Walk back through each learning objective below, in "
             "order, one short beat each: say what the viewer now knows, in plain words, "
             "using what the sections actually said. Add no new facts.",
    "close": "This is the close of the video. End warmly: the one idea to keep, and a "
             "question or next step to think about. Add no new facts. Keep it short.",
}

ROLE_NAMES = {"opening": "Opening", "teach": "Teach", "story": "Story",
              "recap": "Recap", "close": "Close"}


# --- the frame -------------------------------------------------------------------------


def _frame_section(part: str, existing: dict[str, PlanSection]) -> PlanSection:
    kept = existing.get(FRAME_IDS[part])
    if kept is not None:
        return kept
    title, summary = FRAME_DEFAULTS[part]
    return PlanSection(id=FRAME_IDS[part], role=part, title=title, summary=summary,
                       summary_origin="rule")


def apply_frame(plan: Plan) -> None:
    """Opening first, then the body in its own order, then Recap and Close."""
    by_id = {section.id: section for section in plan.sections}
    body = [s for s in plan.sections if s.role not in FRAME_ROLES]
    frame = {part: _frame_section(part, by_id) for part in plan.lesson_frame}
    included = [o.id for o in plan.learning_objectives if o.is_included]
    for part, section in frame.items():
        section.role = part
        section.sources = []
        section.rendering_approach = ""
        # The opening promises the objectives and the recap returns to each.
        section.objective_ids = included if part in ("opening", "recap") else []
    plan.sections = ([frame["opening"]] if "opening" in frame else []) + body + [
        frame[part] for part in ("recap", "close") if part in frame]


# --- time --------------------------------------------------------------------------------


def _measure(extraction, reference) -> tuple[int, int]:
    """Words and pictures at one source location."""
    document = extraction.document(reference.file_name) if extraction else None
    if document is None:
        return 0, 0
    if reference.slide_number:
        blocks = [b for b in document.blocks if b.slide_number == reference.slide_number]
    else:
        blocks = document.blocks_under(reference.heading_path)
    words = sum(len(b.text.split()) for b in blocks if b.kind not in ("heading", "figure"))
    return words, sum(1 for b in blocks if b.kind == "figure")


def needed_seconds(section: PlanSection, extraction, objective_count: int,
                   pictures_attached: bool = False) -> int:
    """How long a section needs on its own merits, before the target is applied.
    Once pictures are attached, it is the section's own pictures that take time."""
    if section.role == "opening":
        return OPENING_SECONDS
    if section.role == "close":
        return CLOSE_SECONDS
    if section.role == "recap":
        return max(20, min(90, 8 + RECAP_SECONDS_PER_OBJECTIVE * objective_count))
    if not section.sources:
        return section.estimated_seconds     # nothing to measure: a person's estimate
    words = pictures = 0
    for reference in section.sources:
        more_words, more_pictures = _measure(extraction, reference)
        words, pictures = words + more_words, pictures + more_pictures
    return max(SHORTEST_BODY_SECONDS,
               round(words * SECONDS_PER_WORD + (len(section.picture_paths) if pictures_attached
                                                  else pictures) * SECONDS_PER_PICTURE))


def timing(plan: Plan, extraction, target_range: tuple[int, int]) -> dict[str, Any]:
    """Each section's length under the target, and how far the material moved."""
    objectives = sum(1 for o in plan.learning_objectives if o.is_included)
    needed = {s.id: needed_seconds(s, extraction, objectives, bool(plan.pictures_from))
              for s in plan.sections}
    fixed = {s.id: (s.estimated_seconds if s.pinned else needed[s.id])
             for s in plan.sections if s.pinned or s.role in FRAME_ROLES}
    flexible = [s for s in plan.sections if s.id not in fixed]
    flexible_need = sum(needed[s.id] for s in flexible)
    natural_total = sum(fixed.values()) + flexible_need
    shortest, longest = target_range
    target = min(max(natural_total, shortest), longest)

    scale = 1.0
    if flexible_need:
        scale = max(0.0, target - sum(fixed.values())) / flexible_need
    seconds = dict(fixed) | {
        s.id: max(SHORTEST_ANY_SECONDS, round(needed[s.id] * scale)) for s in flexible}
    return {
        "seconds": seconds,
        "needed_total": natural_total,
        "target": target,
        "target_range": [shortest, longest],
        "scale": round(scale, 2),
        "is_stretched": scale > MOST_STRETCH,
        "is_squeezed": 0 < scale < MOST_SQUEEZE,
    }


# --- objectives ---------------------------------------------------------------------------

_STOP_WORDS = set("""
about above after again against also because been before being below between both
could does doing down during each from further have having into itself just more most
other over same should some such than that their them then there these they this those
through under until very what when where which while will with would your yours what
explain describe summarise summarize understand relate know learn identify discuss
outline define show tell viewer viewers able using used make made like
""".split())


def _words(text: str) -> set[str]:
    found = set()
    for word in re.findall(r"[a-z]{4,}", text.lower()):
        if word in _STOP_WORDS:
            continue
        found.add(word[:-1] if word.endswith("s") and not word.endswith("ss") else word)
    return found


def objective_suggestions(plan: Plan, extraction) -> list[dict[str, Any]]:
    """Links worth making: a section and an objective that share words.

    Two or more shared words suggest a link; so does one, when that section is
    the objective's best match. Frame sections are linked by the frame itself.
    """
    body = [s for s in plan.sections if s.role not in FRAME_ROLES]
    texts = {}
    for section in body:
        source = " ".join(" ".join(r.heading_path) for r in section.sources)
        under = ""
        if extraction is not None:
            for reference in section.sources:
                document = extraction.document(reference.file_name)
                if document is not None and not reference.slide_number:
                    under += " " + document.text_under(reference.heading_path)[:1500]
                elif document is not None:
                    under += " " + " ".join(
                        b.text for b in document.blocks
                        if b.slide_number == reference.slide_number)[:1500]
        texts[section.id] = _words(f"{section.title} {section.summary} {source} {under}")

    found = []
    for objective in plan.learning_objectives:
        if not objective.is_included:
            continue
        wanted = _words(objective.text)
        scored = sorted(((len(wanted & texts[s.id]), index, s) for index, s in enumerate(body)),
                        key=lambda item: (-item[0], item[1]))
        best = scored[0][0] if scored else 0
        for score, _index, section in scored:
            if objective.id in section.objective_ids or score == 0:
                continue
            if score >= 2 or score == best:
                found.append({"section_id": section.id, "objective_id": objective.id,
                              "words": sorted(wanted & texts[section.id])[:6]})
    return found


# --- summaries -----------------------------------------------------------------------------

LONGEST_SUMMARY_CHARACTERS = 220


def summary_problem(section: PlanSection) -> str:
    """Why a summary does not yet say what the viewer learns, or "" if it does."""
    from pipeline.narration_voice import reporting_phrases

    summary = section.summary.strip()
    if not summary:
        return "no summary"
    if section.role in FRAME_ROLES:
        return ""
    if section.summary_origin == "rule" or summary == section.title.strip():
        return "a stand-in (the title)"
    if "\n" in summary or len(summary) > LONGEST_SUMMARY_CHARACTERS:
        return "source text, not a summary"
    if reporting_phrases(summary):
        return "talks about the source"
    return ""


# --- applying it -----------------------------------------------------------------------------


def shape_plan(project, plan: Plan) -> Plan:
    """The frame, the pictures, then the time. Deterministic: run on every save."""
    from pipeline.extraction import ExtractionStore
    from pipeline.plan_pictures import attach_pictures
    from pipeline.stage_options import video_preferences

    apply_frame(plan)
    attach_pictures(project, plan)
    extraction = ExtractionStore(project.root).load()
    shares = timing(plan, extraction, video_preferences(project.root).target_seconds)
    for section in plan.sections:
        section.estimated_seconds = shares["seconds"][section.id]
    return plan


def save_plan(project, plan: Plan) -> Plan:
    from pipeline.planning import PlanStore

    return PlanStore(project.root).save(shape_plan(project, plan))


def lesson_view(project, plan: Plan) -> dict[str, Any]:
    """What the Scene Plan page shows about the plan as a lesson."""
    from pipeline.extraction import ExtractionStore
    from pipeline.plan_summaries import summaries_view
    from pipeline.stage_options import video_preferences

    extraction = ExtractionStore(project.root).load()
    preferences = video_preferences(project.root)
    shares = timing(plan, extraction, preferences.target_seconds)
    return {
        "frame_parts": LESSON_FRAME_PARTS,
        "role_names": ROLE_NAMES,
        "timing": {k: v for k, v in shares.items() if k != "seconds"}
        | {"target_phrase": preferences.target_phrase},
        "objective_suggestions": objective_suggestions(plan, extraction),
        "summary_problems": {s.id: problem for s in plan.sections
                             if (problem := summary_problem(s))},
        "summaries": summaries_view(project, plan),
    }


def set_lesson_frame(slug: str, parts: list[str]) -> Plan:
    from pipeline.core import require_project
    from pipeline.planning import PlanStore

    project = require_project(slug)
    plan = PlanStore(project.root).load()
    plan.lesson_frame = [part for part in LESSON_FRAME_PARTS if part in parts]
    return save_plan(project, plan)


def reshape(slug: str) -> Plan:
    """Apply the rules again, after something outside the plan changed (the target)."""
    from pipeline.core import require_project
    from pipeline.planning import PlanStore

    project = require_project(slug)
    return save_plan(project, PlanStore(project.root).load())


# --- what the Scripting agent is given for a frame section -----------------------------------


def frame_source(plan: Plan, script, section: PlanSection) -> str:
    """A frame section is written from the plan, and the recap and close from what
    the body actually said."""
    objectives = [o.text for o in plan.learning_objectives if o.is_included]
    lines = ["Learning objectives, in order:",
             *([f"{number}. {text}" for number, text in enumerate(objectives, 1)]
               or ["(none)"]),
             "", "The lesson's sections:"]
    for body in (s for s in plan.sections if s.role not in FRAME_ROLES):
        lines.append(f"- {body.title}: {body.summary}")
        if section.role in ("recap", "close") and script is not None:
            spoken = script.spoken_text(body.id).strip()
            if spoken:
                lines.append(f"  What it said: {spoken[:600]}")
    return "\n".join(lines)
