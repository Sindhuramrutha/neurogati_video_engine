"""Planning the video in a conversation with the planning agent.

1. **The shape.** The person writes what they want, with the setup beside it
   (the length in their own words, how strictly the slides' order is kept, the
   audience). The agent answers in words and proposes the shape: the length as
   it understood it, and each section -- its slides, its minutes, how many scenes.
   Code checks the slides' order and coverage; a shape that breaks them is sent
   back once with the exact problems.
2. **Agreement.** The person agrees to the shape, or replies with what to change
   and gets a revised one. Nothing changes the plan until they agree.
3. **The scenes.** On agreement, every section that is new or changed is broken
   into its agreed number of scenes, one model call per section. A section whose
   slides and scene count did not change keeps its scenes.

The thread is kept at `scene-plan/conversation.json`; the waiting proposal at
`drafts/plan.json`.
"""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from pipeline.agent_runtime import build_system_prompt, resolve_agent
from pipeline.core import OperationFailed, require_project
from pipeline.extraction import ExtractionStore
from pipeline.lesson_plan import plan_source, save_plan
from pipeline.llm import ModelCallFailed, ModelNotConfigured, complete_structured
from pipeline.plan_order import coverage_problems, order_problems
from pipeline.plan_units import (
    references_for,
    section_source_text,
    unit_numbers,
    unit_word,
    units_of,
)
from pipeline.planning import (
    SLIDE_ORDERS,
    Plan,
    PlanDraftStore,
    PlanLength,
    PlanScene,
    PlanSection,
    PlanStore,
)
from pipeline.stage_options import video_preferences
from pipeline.stages import Stage
from pipeline.storage.documents import read_json_object, write_text_atomically
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MOST_MESSAGES_SHOWN_TO_THE_AGENT = 30
MOST_PARALLEL_SCENE_CALLS = 6
LONGEST_MESSAGE = 4000


# --- what the model answers ----------------------------------------------------------


class ShapeSection(BaseModel):
    title: str = Field(description="What this section is about, as a short title.")
    units: list[int] = Field(
        default_factory=list,
        description="The numbers of the slides (or parts) it covers, in the order taught. "
                    "Empty for a section that is about no slide (an opening, a recap, or "
                    "anything else the video needs).")
    how: str = Field(description="In your own words, how this section should be told: its "
                                 "approach, voice and purpose in this video.")
    minutes: float = Field(description="How long the section runs.")
    scenes: int = Field(description="How many scenes it is made of.")
    summary: str = Field(description="One sentence: what the viewer gets from it.")


class LeftOut(BaseModel):
    unit: int
    why: str


class ShapeAnswer(BaseModel):
    reply: str = Field(description="To the person, in a few plain sentences: what you "
                                   "planned and why, and anything you need from them.")
    shortest_minutes: float = Field(description="The shortest length they would accept.")
    longest_minutes: float = Field(description="The longest length they would accept.")
    length_understood: str = Field(
        description="Their length request in one short sentence, as you understood it, "
                    "e.g. 'About 60 min. May run longer, not shorter.'")
    sections: list[ShapeSection]
    left_out: list[LeftOut] = Field(
        default_factory=list, description="Slides (or parts) deliberately not covered.")


class DetailedScene(BaseModel):
    does: str = Field(description="In one sentence: what this scene says and shows.")
    units: list[int] = Field(default_factory=list,
                             description="The slide numbers (or parts) it is about.")
    seconds: int


class SceneAnswer(BaseModel):
    scenes: list[DetailedScene]


# --- the thread --------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _thread_path(project):
    return artifact_path(project.root, Stage.SCENE_PLAN).with_name("conversation.json")


def read_thread(project) -> list[dict[str, Any]]:
    return (read_json_object(_thread_path(project), "planning conversation")
            or {}).get("messages", [])


def _add(project, messages: list[dict[str, Any]], role: str, text: str, **extra) -> None:
    """Add to the thread already read, and write it."""
    messages.append({"role": role, "text": text, "at": _now(), **extra})
    write_text_atomically(_thread_path(project), json.dumps(
        {"messages": messages}, indent=1, ensure_ascii=False))


# --- what the agent is shown -----------------------------------------------------------


def _setup_text(plan: Plan, preferences) -> str:
    return "\n".join([
        f"Length asked for: {plan.length_text or '(not given -- choose from the material)'}",
        f"Slide order: {SLIDE_ORDERS[plan.slide_order]}",
        f"Audience: {preferences.audience(plan.audience)}",
        f"Language: {preferences.language_name}",
    ])


def _units_text(units) -> str:
    return "\n".join(f"{u.number}. {u.title} -- {u.words} words"
                     + (f", {u.pictures} picture(s)" if u.pictures else "") for u in units)


def _current_shape_text(plan: Plan, units) -> str:
    if not plan.sections:
        return "(no plan yet)"
    lines = []
    for s in plan.sections:
        numbers = unit_numbers(s, units)
        lines.append(f"- {s.title} units {numbers or '-'}, "
                     f"{round(s.estimated_seconds / 60, 1)} min, {len(s.scenes)} scenes")
    return "\n".join(lines)


def _shape_prompts(project, plan: Plan, units, thread: list[dict[str, Any]],
                   problems: list[str]) -> tuple[str, str]:
    agent = resolve_agent(project, Stage.SCENE_PLAN)
    system_prompt = (
        f"{build_system_prompt(agent)}\n\n---\n"
        "Plan the whole video's SHAPE with the person, from their direction. Decide how "
        "long it runs (within the length they asked for), how many sections, which "
        "slides (or parts) each section covers -- one, or a run of several -- and how many "
        "scenes each section has. A scene is one beat on screen, usually 20 to 60 seconds. "
        "Sections are as many and as long as the material and the length call for. "
        "Keep the slide order exactly as the setup says. Cover every slide, or list it "
        "under left_out with why. You may add sections that are about no slide -- an "
        "opening, a recap, a close, or anything else this video needs -- with no units; "
        "decide them and name them yourself. For every section, say in your own words how "
        "it should be told. Never plan material that is not in the list. Reply to the "
        "person briefly and plainly."
    )
    conversation = "\n".join(f"{m['role'].upper()}: {m['text']}"
                             for m in thread[-MOST_MESSAGES_SHOWN_TO_THE_AGENT:])
    user_prompt = "\n\n".join(part for part in [
        f"--- setup ---\n{_setup_text(plan, video_preferences(project.root))}",
        f"--- the source, in order ---\n{_units_text(units)}",
        f"--- the plan as it stands ---\n{_current_shape_text(plan, units)}",
        f"--- the conversation ---\n{conversation}",
        ("--- your last answer broke these rules; answer again without breaking them ---\n"
         + "\n".join(f"- {p}" for p in problems)) if problems else "",
    ] if part)
    return system_prompt, user_prompt


def _shape_problems(answer: ShapeAnswer, plan: Plan, all_units: list[int]) -> list[str]:
    body = [(s.title, s.units) for s in answer.sections if s.units]
    left_out = {item.unit: item.why for item in answer.left_out}
    return (order_problems(body, plan.slide_order)
            + coverage_problems(body, all_units, left_out))


# --- the person's actions ----------------------------------------------------------------


def set_setup(slug: str, changes: dict[str, Any]) -> Plan:
    """The length in their words, the slide order and the audience."""
    project = require_project(slug)
    plan = PlanStore(project.root).load()
    for key in ("length_text", "slide_order", "audience"):
        if key in changes:
            setattr(plan, key, str(changes[key] or ""))
    return PlanStore(project.root).save(Plan.model_validate(plan.model_dump()))


def send_message(slug: str, text: str) -> dict[str, Any]:
    """Say something to the planning agent; it answers with a proposed shape.
    One model call, and one more only if the first breaks the order rules."""
    project = require_project(slug)
    text = text.strip()[:LONGEST_MESSAGE]
    if not text:
        raise OperationFailed("Write what you want first.")
    extraction = ExtractionStore(project.root).load()
    units = units_of(extraction)
    if not units:
        raise OperationFailed("Nothing is extracted yet, so there is nothing to plan.")
    plan = PlanStore(project.root).load()
    thread = read_thread(project)
    _add(project, thread, "you", text)

    all_units = [u.number for u in units]
    problems: list[str] = []
    calls = 0
    for _attempt in range(2):
        system_prompt, user_prompt = _shape_prompts(project, plan, units, thread, problems)
        try:
            answer = complete_structured(ShapeAnswer, system_prompt, user_prompt)
        except (ModelNotConfigured, ModelCallFailed) as failure:
            _add(project, thread, "agent", f"I could not answer: {failure}", failed=True)
            raise OperationFailed(f"The planning agent could not answer. {failure}") from failure
        calls += 1
        problems = _shape_problems(answer, plan, all_units)
        if not problems:
            break

    proposal = {
        "made_at": _now(), "calls": calls, "reply": answer.reply,
        "length": PlanLength(shortest_seconds=round(answer.shortest_minutes * 60),
                             longest_seconds=round(answer.longest_minutes * 60),
                             understood=answer.length_understood).model_dump(),
        "sections": [s.model_dump() for s in answer.sections],
        "left_out": {str(item.unit): item.why for item in answer.left_out},
        "problems": problems,
        "extraction_fingerprint": extraction.content_fingerprint(),
    }
    PlanDraftStore(project.root).save(proposal)
    _add(project, thread, "agent", answer.reply, proposal=True)
    return planning_view(project, units=units, plan=plan, thread=thread, proposal=proposal)


def discard_proposal(slug: str) -> dict[str, Any]:
    project = require_project(slug)
    if PlanDraftStore(project.root).clear():
        _add(project, read_thread(project), "you", "(Discarded the proposed shape.)")
    return planning_view(project)


def _reuse(old: list[PlanSection], proposed: ShapeSection,
           units) -> tuple[PlanSection | None, bool]:
    """The existing section this proposed one is -- the same slides, or for a
    section about no slide the same title -- and whether it keeps its scenes.
    It does only when nothing they were written from changed: the same number of
    scenes, the same length, and the same direction (how it is told, and what it
    is about). Otherwise its scenes are written again."""
    for section in old:
        same = unit_numbers(section, units) == proposed.units if proposed.units else (
            not section.sources and section.title.strip().lower()
            == proposed.title.strip().lower())
        if same:
            unchanged = (len(section.scenes) == max(1, proposed.scenes)
                         and section.estimated_seconds == round(proposed.minutes * 60)
                         and section.how.strip() == proposed.how.strip()
                         and section.summary.strip() == proposed.summary.strip())
            return section, unchanged
    return None, False


def agree(slug: str) -> dict[str, Any]:
    """Make the proposed shape the plan, then write the scenes it needs."""
    project = require_project(slug)
    proposal = PlanDraftStore(project.root).load()
    if not proposal:
        raise OperationFailed("There is no proposed shape to agree to.")
    if proposal.get("problems"):
        raise OperationFailed("This shape breaks the slide order or leaves slides out "
                              "without saying why. Reply with what to fix first.")
    extraction = ExtractionStore(project.root).load()
    if proposal.get("extraction_fingerprint") != extraction.content_fingerprint():
        raise OperationFailed("The source was extracted again after this shape was "
                              "proposed, so its slide numbers may not mean the same "
                              "slides. Ask the planning agent again.")
    units = units_of(extraction)
    plan = PlanStore(project.root).load()
    sections, needs_scenes = [], {}
    for proposed in (ShapeSection.model_validate(s) for s in proposal["sections"]):
        numbers = proposed.units
        kept, keeps_scenes = _reuse(plan.sections, proposed, units)
        section = PlanSection(
            id=kept.id if kept else PlanSection().id,
            title=proposed.title, how=proposed.how, summary=proposed.summary,
            sources=references_for(numbers, units),
            estimated_seconds=round(proposed.minutes * 60),
            picture_paths=kept.picture_paths if kept else [],
            pictures_chosen=kept.pictures_chosen if kept else False)
        if keeps_scenes:
            section.scenes = kept.scenes
        else:
            needs_scenes[section.id] = max(1, proposed.scenes)
        sections.append(section)
    plan.sections = sections
    plan.length = PlanLength.model_validate(proposal["length"])
    plan.slides_left_out = {int(k): v for k, v in proposal.get("left_out", {}).items()}
    plan.shape_agreed_at = _now()
    plan.extraction_fingerprint = proposal.get("extraction_fingerprint", "")
    PlanDraftStore(project.root).clear()
    thread = read_thread(project)
    _add(project, thread, "you", "(Agreed to the shape.)")

    notes = write_scenes(project, plan, needs_scenes, extraction, units, thread)
    plan = save_plan(project, plan)
    written = len(needs_scenes) - len(notes)
    _add(project, thread, "agent", f"Scenes written for {written} section(s)."
         + (" " + " ".join(notes) if notes else "")
         + " Edit anything on the Plan tab, or tell me what to change.")
    return planning_view(project, units=units, plan=plan, thread=thread, proposal=None)


# --- the scenes --------------------------------------------------------------------------


def _even(seconds: list[int], total: int) -> list[int]:
    """Scale to add up to `total`, keeping their proportions."""
    if not seconds or not sum(seconds):
        return [max(3, total // max(1, len(seconds)))] * len(seconds)
    scaled = [max(3, round(s * total / sum(seconds))) for s in seconds]
    scaled[-1] = max(3, scaled[-1] + total - sum(scaled))
    return scaled


def write_scenes(project, plan: Plan, wanted: dict[str, int], extraction, units,
                 thread: list[dict[str, Any]]) -> list[str]:
    """Break each section in `wanted` into that many scenes. One call per section."""
    if not wanted:
        return []
    agent = resolve_agent(project, Stage.SCENE_PLAN)
    direction = "\n".join(m["text"] for m in thread if m["role"] == "you")
    language = video_preferences(project.root).language_name
    system_prompt = (
        f"{build_system_prompt(agent)}\n\n---\n"
        "Break ONE section of the agreed plan into exactly the number of scenes asked "
        "for. A scene is one beat on screen. For each, say in one sentence what it says "
        "and shows, which of the section's slides it is about, and its seconds; together "
        "they fill the section's time. Keep the slides' order. Use only the material given."
    )

    def detail(section: PlanSection) -> str | None:
        count = wanted[section.id]
        own = unit_numbers(section, units)
        if not section.sources:
            material, cut = plan_source(plan, None, section), False
        else:
            material, cut = section_source_text(extraction, section.sources)
        user_prompt = "\n\n".join([
            f"The person's direction:\n{direction or '(none)'}",
            f"Audience: {video_preferences(project.root).audience(plan.audience)}\n"
            f"Language: {language}",
            f"Section: {section.title} -- {section.summary}\n"
            f"How it is told: {section.how or '(not said)'}",
            f"It runs {section.estimated_seconds} seconds in exactly {count} scenes. "
            f"Its slides: {own or 'none'}.",
            f"--- its material ---\n{material}",
        ])
        try:
            answer = complete_structured(SceneAnswer, system_prompt, user_prompt)
        except (ModelNotConfigured, ModelCallFailed) as failure:
            logger.warning("scenes for %s failed: %s", section.title, failure)
            return f"“{section.title}” could not be broken into scenes: {failure}."
        scenes = answer.scenes[:count]
        seconds = _even([s.seconds for s in scenes], section.estimated_seconds)
        section.scenes = [PlanScene(does=s.does, seconds=t,
                                    slides=[n for n in s.units if n in own])
                          for s, t in zip(scenes, seconds, strict=True)]
        note = f"“{section.title}” got {len(scenes)} of {count} scenes." \
            if len(scenes) < count else None
        return note or (f"“{section.title}”: its material was cut to fit." if cut else None)

    targets = [s for s in plan.sections if s.id in wanted]
    with ThreadPoolExecutor(max_workers=min(MOST_PARALLEL_SCENE_CALLS, len(targets))) as pool:
        notes = [note for note in pool.map(detail, targets) if note]
    return notes


# --- what the page shows -------------------------------------------------------------------


_UNREAD = object()


def planning_view(project, *, units=None, plan: Plan | None = None,
                  thread: list[dict[str, Any]] | None = None,
                  proposal: Any = _UNREAD) -> dict[str, Any]:
    """The thread, the waiting proposal, what agreeing would cost, and the units
    each section covers. Whatever the caller already loaded is passed in."""
    if proposal is _UNREAD:
        proposal = PlanDraftStore(project.root).load()
    if proposal and "sections" not in proposal:
        proposal = None          # a draft from before plans were made this way
    units = units if units is not None else units_of(ExtractionStore(project.root).load())
    plan = plan or PlanStore(project.root).load()
    scene_calls = sum(
        not _reuse(plan.sections, ShapeSection.model_validate(raw), units)[1]
        for raw in (proposal or {}).get("sections", []))
    return {
        "messages": thread if thread is not None else read_thread(project),
        "proposal": proposal,
        "agree_calls": scene_calls,
        "section_units": {s.id: unit_numbers(s, units) for s in plan.sections},
        "units": [{"number": u.number, "title": u.title, "words": u.words,
                   "reference": u.reference.model_dump()} for u in units],
        "unit_word": unit_word(units),
        "slide_orders": SLIDE_ORDERS,
    }


def read_planning(slug: str) -> dict[str, Any]:
    return planning_view(require_project(slug))
