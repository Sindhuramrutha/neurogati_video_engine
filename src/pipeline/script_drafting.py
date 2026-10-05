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
from pipeline.plan_drafting import MAXIMUM_SECTION_SOURCE_CHARACTERS, section_source_text
from pipeline.planning import Plan, PlanSection
from pipeline.scripting import Script, ScriptScene, ScriptStore, SectionScript
from pipeline.stage_options import video_preferences
from pipeline.stages import Stage

logger = logging.getLogger(__name__)

WORDS_PER_SECOND_OF_SPEECH = 150 / 60
MAXIMUM_PARALLEL_SECTION_DRAFTS = 6

# Enough of the previous section to continue from it; the opening of the next is
# only a hint of where this one must lead.
MAXIMUM_PREVIOUS_NARRATION_CHARACTERS = 3_000
MAXIMUM_NEXT_NARRATION_CHARACTERS = 800


class DraftedScene(BaseModel):
    narration: str = Field(
        description="What is said aloud in this scene, written for the ear: short "
                    "sentences, no bullet points, headings, stage directions or markdown."
    )
    brief: str = Field(
        description="Exactly what is on screen while this narration plays: the real "
                    "values, labels and terms from the source. Never 'such as' or "
                    "'something like'. If there is no real data, say which generic "
                    "marks to show."
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

    def draft(section: PlanSection):
        try:
            return section, *_write_section(
                agent, plan, script, extraction, section, instruction, preferences, pictures)
        except (ModelCallFailed, ModelNotConfigured) as failure:
            logger.warning("drafting %s failed: %s", section.title, failure)
            return section, None, [f'"{section.title}" could not be drafted: {failure}']

    workers = min(MAXIMUM_PARALLEL_SECTION_DRAFTS, len(unwritten))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(draft, unwritten))

    store = ScriptStore(project.root)
    latest = store.load()
    notes: list[str] = []
    drafted_ids: list[str] = []
    for section, written, section_notes in results:
        notes.extend(section_notes)
        if written is None:
            continue
        if latest.body_for(section.id).strip():
            notes.append(f'"{section.title}" was written while drafting; it was kept as it is.')
            continue
        latest.section_scripts = [
            s for s in latest.section_scripts if s.section_id != section.id
        ] + [written]
        drafted_ids.append(section.id)

    if not drafted_ids and all(written is None for _, written, _ in results):
        raise OperationFailed("No section could be drafted. " + " ".join(notes))

    saved = store.save(_script_in_plan_order(project, latest))
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

    system_prompt = (
        f"{build_system_prompt(agent)}\n\n"
        f"---\nWrite ONE plan section as a sequence of scenes. Each scene has "
        f"`narration`, spoken aloud and written for the ear, of about 15 to 45 "
        f"seconds (roughly 40 to 110 words), and `brief`, exactly what is on "
        f"screen while that narration plays, following your instructions on "
        f"briefs. About {target_words} words of narration in total, to fill about "
        f"{section.estimated_seconds} seconds. Every fact must come from the "
        f"source material provided; do not add examples, numbers or analogies "
        f"that are not in it. Open where the previous section left off.\n\n"
        f"{VOICE_RULE}\n"
        f"Tone: {preferences.tone_sentence}\n"
        f"Write the narration, and every brief, in {preferences.language_name}. "
        f"Keep technical terms and proper nouns in the form the source uses, "
        f"even where the rest of the sentence is not in English."
    )

    from pipeline.lesson_plan import FRAME_ROLES, frame_source

    if section.role in FRAME_ROLES:
        # Written from the plan -- and the recap and close from what the body
        # said -- not from a source: an opening that re-read the source taught.
        source, source_note = frame_source(plan, script, section), ""
    else:
        source, source_note = _source_for(extraction, section)
    if source_note:
        notes.append(f'"{section.title}": {source_note}')

    user_prompt = "\n\n".join(part for part in (
        f"Audience: {plan.selected_audience or 'not chosen'}"
        + (f"\nInstruction: {instruction.strip()}" if instruction.strip() else ""),
        f"--- the whole plan ---\n{compact_plan_text(plan, marked_section_id=section.id)}",
        "--- the section you are writing ---\n" + _section_brief(
            plan, section, target_words, (pictures or {}).get(section.id, [])),
        _neighbours(plan, script, section),
        f"--- source material for this section ---\n{source}",
    ) if part)

    drafted = complete_structured(DraftedSection, system_prompt, user_prompt)
    scenes = [
        ScriptScene(narration=scene.narration.strip(), brief=scene.brief.strip())
        for scene in drafted.scenes if scene.narration.strip()
    ]
    if not scenes:
        raise ModelCallFailed("The agent returned no narration for this section.")

    written = SectionScript(section_id=section.id, scenes=scenes)
    written.written_from = narration_fingerprints(section, extraction)
    return written, notes


def section_pictures(project, plan: Plan) -> dict[str, list[str]]:
    """Each section's pictures, as the plan attached them, named for the agent:
    the script is written knowing what the section will show."""
    from pipeline.plan_pictures import assets_for_later_stages, pictures_of

    library = assets_for_later_stages(project).library
    return {section.id: [figure.name + (f" -- {figure.caption}" if figure.caption
                                        and figure.caption not in figure.name else "")
                         for figure in pictures_of(section, plan, library)]
            for section in plan.sections}


def _section_brief(plan: Plan, section: PlanSection, target_words: int,
                   pictures: list[str] | None = None) -> str:
    from pipeline.lesson_plan import ROLE_GUIDE, summary_problem

    objectives = {o.id: o.text for o in plan.learning_objectives if o.is_included}
    served = [objectives[oid] for oid in section.objective_ids if oid in objectives]
    # A stand-in or raw source text is not a summary, and passing it on as one
    # told the agent to read the slide out.
    summary = section.summary if not summary_problem(section) else ""
    lines = [
        f"Title: {section.title}",
        f"Summary: {summary or '(none given)'}",
        f"Target: about {section.estimated_seconds} seconds, about {target_words} words",
    ]
    if section.rendering_approach:
        lines.append(f"Shown as: {section.rendering_approach}"
                     + (f" -- {section.rendering_reason}" if section.rendering_reason else ""))
    if served:
        lines.append("Learning objectives it serves:\n" + "\n".join(f"- {o}" for o in served))
    if ROLE_GUIDE.get(section.role):
        lines.append(f"Its part in the lesson: {ROLE_GUIDE[section.role]}")
    if pictures:
        lines.append("Pictures from the source this section shows (a scene may be built "
                     "around one; describe no picture that is not listed):\n"
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
