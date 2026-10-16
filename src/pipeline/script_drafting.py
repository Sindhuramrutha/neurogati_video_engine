"""Writing a plan section's narration, as scenes, with the agent.

Each scene is what is said and what is on screen while it is said. The Scripting
agent's instructions always asked for both -- and called a vague on-screen brief
"the single most direct cause of bad output downstream" -- but it could only ever
return one block of text, so the brief was never written.

What the agent is given, for one section:

- **the whole plan, compactly**, with this section marked, so it knows where it is;
- **this section's own plan**: summary, target length, how it will be shown and
  why, and the learning objectives it serves;
- **its neighbours**: the narration just before it, and what comes next, so a
  section opens where the last one left off instead of starting from nothing;
- **its source text in full** -- the content the plan section records -- rather
  than the whole extraction cut off at 40,000 characters.

A drafted section is saved, replacing only that section. "Draft all unwritten"
drafts every empty section at once and never touches narration already written.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from pydantic import BaseModel, Field

from pipeline.agent_runtime import (
    MAXIMUM_SOURCE_CHARACTERS,
    build_system_prompt,
    compact_plan_text,
    resolve_agent,
)
from pipeline.extraction import Extraction, ExtractionStore
from pipeline.llm import ModelCallFailed, ModelNotConfigured, complete_structured
from pipeline.narration_voice import VOICE_RULE
from pipeline.operations import (
    OperationFailed,
    _script_in_plan_order,
    narration_fingerprints,
    present_artifact,
    require_project,
)
from pipeline.plan_units import MAXIMUM_SECTION_SOURCE_CHARACTERS, section_source_text
from pipeline.planning import Plan, PlanSection
from pipeline.script_review import SLIDES_ARE_THE_DIRECTION
from pipeline.script_review import keep_to_slides as _keep_to_slides
from pipeline.scripting import (
    SCRIPT_WRITE,
    Script,
    ScriptScene,
    ScriptStore,
    SectionScript,
)
from pipeline.stage_options import video_preferences
from pipeline.stages import Stage

logger = logging.getLogger(__name__)

WORDS_PER_SECOND_OF_SPEECH = 150 / 60
MAXIMUM_PARALLEL_SECTION_DRAFTS = 6

# Enough of the previous section to continue from it; the opening of the next is
# only a hint of where this one must lead.
MAXIMUM_PREVIOUS_NARRATION_CHARACTERS = 3_000
MAXIMUM_NEXT_NARRATION_CHARACTERS = 800


# A section is every scene's narration and a full brief each, and the model's hidden
# reasoning spends from the same budget: 16,000 ran out at seven scenes.
SECTION_TOKENS = 65536


class DraftedScene(BaseModel):
    narration: str = Field(
        description="What is said aloud in this scene, written for the ear: short "
                    "sentences, no bullet points, headings, stage directions or markdown."
    )
    brief: str = Field(
        description="What is on screen while this narration plays, in the shape your "
                    "instructions give: PICTURE (the exact names of the deck's pictures "
                    "to show, the main one first, or none), DRAW (the real things, "
                    "named), LAYOUT, BEATS (\"exact words\" -> what appears or changes), "
                    "LABELS (at most five, from the narration), and -- only for what no "
                    "deck picture shows -- PHOTO (a real photograph, engraving or diagram "
                    "to find on the open web), ILLUSTRATE (what to paint) or ICON (up to "
                    "three simple icons). Never 'such as' or 'something like'."
    )


class DraftedSection(BaseModel):
    scenes: list[DraftedScene]


def draft_section(slug: str, section_id: str, instruction: str = "") -> dict[str, Any]:
    """Draft one section's scenes and save them, replacing that section only."""
    from pipeline.plan_handoff import plan_for_later_stages
    project = require_project(slug)
    plan = plan_for_later_stages(project)
    section = next((s for s in plan.sections if s.id == section_id), None)
    if section is None:
        listed = ", ".join(f"{s.id} ({s.title})" for s in plan.sections) or "none"
        raise OperationFailed(f"The plan has no section {section_id!r}. Sections: {listed}.")

    store = ScriptStore(project.root)
    script = store.load()
    extraction = ExtractionStore(project.root).load()
    agent = resolve_agent(project, Stage.SCRIPT_STAGING)

    try:
        written, notes = _write_section(
            agent, plan, script, extraction, section, instruction,
            video_preferences(project.root), section_pictures(project, plan))
    except ModelNotConfigured as not_configured:
        raise OperationFailed(str(not_configured)) from not_configured
    except ModelCallFailed as call_failure:
        raise OperationFailed(f"The model call failed. {call_failure}") from call_failure

    # Read again before saving: the model call takes a while, and anything saved
    # to other sections or the variables meanwhile must not be overwritten.
    latest = store.load()
    latest.section_scripts = [
        s for s in latest.section_scripts if s.section_id != section_id
    ] + [written]
    saved = store.save(_script_in_plan_order(project, latest))

    target_words = _target_words(section)
    return present_artifact(project, "script", saved) | {
        "stage": Stage.SCRIPT_STAGING.value,
        "agent": agent.name,
        "section_id": section_id,
        "section_title": section.title,
        "target_words": target_words,
        "written_words": written.word_count,
        "scene_count": len(written.scenes),
        "is_saved": True,
        "notes": notes,
    }


def draft_unwritten_sections(slug: str, instruction: str = "") -> dict[str, Any]:
    """Draft every section with no narration, at the same time, and save them.

    Narration already written is never replaced, including anything typed while
    the drafts were being written: the script is read again before saving, and a
    section that gained words in the meantime keeps them.
    """
    from pipeline.plan_handoff import plan_for_later_stages
    project = require_project(slug)
    plan = plan_for_later_stages(project)
    script = ScriptStore(project.root).load()
    unwritten = [s for s in plan.sections if not script.body_for(s.id).strip()]
    if not unwritten:
        raise OperationFailed("Every section already has narration.")

    extraction = ExtractionStore(project.root).load()
    agent = resolve_agent(project, Stage.SCRIPT_STAGING)
    preferences = video_preferences(project.root)
    pictures = section_pictures(project, plan)

    store = ScriptStore(project.root)
    drafted_ids: list[str] = []

    def draft(section: PlanSection) -> list[str]:
        """One section, saved the moment it is written: a run stopped later keeps
        every section already drafted (it once saved nothing until all finished).
        Any error stays with its section; the others go on."""
        try:
            written, section_notes = _write_section(
                agent, plan, script, extraction, section, instruction, preferences, pictures)
        except Exception as failure:          # one section's error, never the run's
            logger.warning("drafting %s failed: %s", section.title, failure, exc_info=True)
            return [f'"{section.title}" could not be drafted: {failure}']
        with SCRIPT_WRITE:
            latest = store.load()
            if latest.body_for(section.id).strip():
                return [*section_notes,
                        f'"{section.title}" was written while drafting; it was kept as it is.']
            latest.section_scripts = [
                s for s in latest.section_scripts if s.section_id != section.id] + [written]
            store.save(_script_in_plan_order(project, latest))
            drafted_ids.append(section.id)
        return section_notes

    workers = min(MAXIMUM_PARALLEL_SECTION_DRAFTS, len(unwritten))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        notes = [note for found in pool.map(draft, unwritten) for note in found]

    if not drafted_ids:
        raise OperationFailed("No section could be drafted. " + " ".join(notes))

    saved = store.load()
    return present_artifact(project, "script", saved) | {
        "drafted_section_ids": drafted_ids,
        "notes": notes,
    }


# --- one section --------------------------------------------------------------------


def _target_words(section: PlanSection) -> int:
    return max(20, int(section.estimated_seconds * WORDS_PER_SECOND_OF_SPEECH))


def _write_section(
    agent,
    plan: Plan,
    script: Script,
    extraction: Extraction,
    section: PlanSection,
    instruction: str,
    preferences,
    pictures: dict[str, list[str]] | None = None,
) -> tuple[SectionScript, list[str]]:
    """Ask for this section's scenes. Returns the section, unsaved, and any notes."""
    notes: list[str] = []
    target_words = _target_words(section)

    # The plan decided the scenes: how many, what each does, how long. The
    # script writes into exactly those.
    planned = section.scenes
    shape = (
        f"Write exactly {len(planned)} scenes, in this order -- the plan decided them; "
        f"do not add, drop, merge or split any. Each scene's seconds are a target at "
        f"about {round(WORDS_PER_SECOND_OF_SPEECH * 60)} words a minute, not a quota: say "
        f"what the material supports, shorter is fine, and never pad or repeat."
        if planned else
        "Write it as a sequence of scenes of about 15 to 45 seconds (roughly 40 to 110 "
        "words) each."
    )
    system_prompt = (
        f"{build_system_prompt(agent)}\n\n"
        f"---\nWrite ONE plan section. Each scene has `narration`, spoken aloud and "
        f"written for the ear, and `brief`, exactly what is on screen while that "
        f"narration plays, following your instructions on briefs. {shape} "
        f"Up to about {target_words} words of narration in total, for about "
        f"{section.estimated_seconds} seconds. {SLIDES_ARE_THE_DIRECTION} Teach it to "
        f"a learner meeting it for the first time, following your instructions on "
        f"narration. Open where the previous section left off.\n\n"
        f"{VOICE_RULE}\n"
        f"Tone: {preferences.tone_sentence}\n"
        f"Write the narration, and every brief, in {preferences.language_name}. "
        f"Keep technical terms and proper nouns in the form the source uses, "
        f"even where the rest of the sentence is not in English."
    )

    from pipeline.lesson_plan import plan_source

    if not section.sources:
        # Written from the plan -- and the recap and close from what the body
        # said -- not from a source: an opening that re-read the source taught.
        source, source_note = plan_source(plan, script, section), ""
    else:
        source, source_note = _source_for(extraction, section)
    if source_note:
        notes.append(f'"{section.title}": {source_note}')

    user_prompt = "\n\n".join(part for part in (
        f"Audience: {preferences.audience(plan.audience)}"
        + (f"\nInstruction: {instruction.strip()}" if instruction.strip() else ""),
        f"--- the whole plan ---\n{compact_plan_text(plan, marked_section_id=section.id)}",
        "--- the section you are writing ---\n" + _section_brief(
            plan, section, target_words, (pictures or {}).get(section.id, [])),
        _neighbours(plan, script, section),
        f"--- source material for this section ---\n{source}",
    ) if part)

    drafted = complete_structured(DraftedSection, system_prompt, user_prompt,
                                  max_tokens=SECTION_TOKENS)
    written_scenes = [scene for scene in drafted.scenes if scene.narration.strip()]
    if not written_scenes:
        raise ModelCallFailed("The agent returned no narration for this section.")
    if planned:
        # Kept to the plan's scenes and their ids, so every later layer -- one
        # scene.py per scene -- lines up with what was agreed.
        if len(written_scenes) != len(planned):
            notes.append(f'"{section.title}": the agent wrote {len(written_scenes)} scenes '
                         f"for {len(planned)} planned; matched in order.")
        scenes = [ScriptScene(id=plan_scene.id, narration=scene.narration.strip(),
                              brief=scene.brief.strip())
                  for plan_scene, scene in zip(planned, written_scenes, strict=False)]
    else:
        scenes = [ScriptScene(narration=scene.narration.strip(), brief=scene.brief.strip())
                  for scene in written_scenes]

    scenes, unsupported, uncovered = _keep_to_slides(
        system_prompt, source, scenes, notes, section.title)
    written = SectionScript(section_id=section.id, scenes=scenes)
    written.written_from = narration_fingerprints(section, extraction)
    written.unsupported, written.uncovered = unsupported, uncovered
    return written, notes


def section_pictures(project, plan: Plan) -> dict[str, list[str]]:
    """Each section's pictures, as the plan attached them, named for the agent with
    what each is and what it is good for (described once, `scene_vetting`): the
    script is written knowing what the section will show."""
    from pipeline.plan_pictures import assets_for_later_stages, pictures_of
    from pipeline.scene_program import SCENES
    from pipeline.scene_vetting import ROLES, notes

    library = assets_for_later_stages(project).library
    attached = {section.id: pictures_of(section, plan, library) for section in plan.sections}
    described = notes(project.root / SCENES, sorted({
        str(project.root / figure.shown_path) for figures in attached.values()
        for figure in figures if (project.root / figure.shown_path).exists()}))

    def line(figure) -> str:
        note = described.get(str(project.root / figure.shown_path), {})
        parts = [figure.name + (f" -- {figure.caption}" if figure.caption
                                and figure.caption not in figure.name else "")]
        if note.get("what"):
            parts.append(f"what it is: {note['what']}")
        if note.get("role") in ROLES:
            parts.append(ROLES[note["role"]])
        if figure.why_not_a_frame:
            parts.append(f"measured: {figure.why_not_a_frame}")
        return " | ".join(parts)

    return {section_id: [line(figure) for figure in figures]
            for section_id, figures in attached.items()}


def _section_brief(plan: Plan, section: PlanSection, target_words: int,
                   pictures: list[str] | None = None) -> str:
    lines = [
        f"Title: {section.title}",
        f"Summary: {section.summary or '(none given)'}",
        f"Target: about {section.estimated_seconds} seconds, about {target_words} words",
    ]
    if section.scenes:
        lines.append("Its scenes, as planned:\n" + "\n".join(
            f"{number}. (~{scene.seconds} s"
            + (f", slide {', '.join(map(str, scene.slides))}" if scene.slides else "")
            + f") {scene.does}" for number, scene in enumerate(section.scenes, start=1)))
    if section.how:
        lines.append(f"How it is told: {section.how}")
    if pictures:
        lines.append("Pictures from the deck for this section -- give each one that fits a "
                     "place: the subject of a scene when it shows what is said, or behind a "
                     "topic's opening when it is the deck's art (name them on PICTURE; "
                     "describe no deck picture that is not listed):\n"
                     + "\n".join(f"- {name}" for name in pictures))
    return "\n".join(lines)


def _neighbours(plan: Plan, script: Script, section: PlanSection) -> str:
    index = next(i for i, s in enumerate(plan.sections) if s.id == section.id)
    parts = []

    if index > 0:
        previous = plan.sections[index - 1]
        spoken = script.spoken_text(previous.id).strip()
        parts.append(
            f'--- the section before: "{previous.title}" ---\n'
            + (_tail(spoken, MAXIMUM_PREVIOUS_NARRATION_CHARACTERS) if spoken
               else f"(not written yet; its plan summary: {previous.summary or 'none'})")
        )
    else:
        parts.append("--- this is the first section of the video ---")

    if index + 1 < len(plan.sections):
        following = plan.sections[index + 1]
        spoken = script.spoken_text(following.id).strip()
        parts.append(
            f'--- the section after: "{following.title}" ---\n'
            f"Plan summary: {following.summary or 'none'}"
            + (f"\nIt opens: {spoken[:MAXIMUM_NEXT_NARRATION_CHARACTERS]}" if spoken else "")
        )
    else:
        parts.append("--- this is the last section of the video ---")

    return "\n\n".join(parts)


def _tail(text: str, limit: int) -> str:
    return text if len(text) <= limit else "..." + text[-limit:]


def _source_for(extraction: Extraction, section: PlanSection) -> tuple[str, str]:
    """This section's own source text, or -- only when it records none -- the
    extraction, which is then cut to what fits. Returns (text, note)."""
    if section.sources:
        text, was_cut = section_source_text(extraction, section.sources)
        if not text.strip():
            return ("(the content this section records is no longer in the extraction)",
                    "its recorded source content is not in the extraction")
        if was_cut:
            return (text + "\n\n... (longer than shown; use only the above)",
                    f"its source is longer than {MAXIMUM_SECTION_SOURCE_CHARACTERS:,} "
                    f"characters; the agent read the first part")
        return text, ""

    markdown = extraction.as_markdown()
    if not markdown.strip():
        return "(nothing has been extracted)", "nothing is extracted to write from"
    if len(markdown) > MAXIMUM_SOURCE_CHARACTERS:
        markdown = markdown[:MAXIMUM_SOURCE_CHARACTERS] + "\n\n... (truncated)"
        return markdown, ("it records no sources, so the agent read the extraction up to "
                          f"{MAXIMUM_SOURCE_CHARACTERS:,} characters")
    return markdown, "it records no sources, so the agent read the whole extraction"
