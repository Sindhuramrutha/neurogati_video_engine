"""How one scene leads into the next: decided when the video is planned, held to when
it is written, and smoothed where sections meet.

v8's script, scene by scene, read well; where scenes met it did not. Scene 1 promised
"a question people have argued about for two thousand years" and scene 2 did not ask
it; scene 2 ended on "Where does thought live?" and scene 3 opened by asking it again;
"Chapter one of Demystifying the Brain" was announced afresh in the middle of the
video. Sections were planned, and drafted, each without the words of its neighbours.

- **Planned.** The shape, which sees the whole video, gives every section what it
  opens on and what it ends on; breaking a section into scenes gives every scene the
  same, and a pause after it (0 to 2 seconds) with its reason. A section's first and
  last scenes take the section's joins (`fit_joins`).
- **Written.** Each section is drafted to its scenes' joins (`scene_contracts`), told
  to name the course only where the video opens and closes.
- **Smoothed.** Sections are drafted side by side, so where they meet is read once all
  are written (`smooth_joins`): only the sentences at the join are rewritten, and only
  a small edit that brings in nothing the facts forbid is kept.
- **Checked.** `join_problems` finds, by code, a question or opening asked twice across
  a join, the course announced mid-video, and narration that describes the picture.
"""

from __future__ import annotations

import difflib
import re
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel, Field

SECTION_TURN_PAUSE = 1.0      # seconds after a section's last scene, unless planned more
SMALLEST_KEPT_LIKENESS = 0.6  # a smoothed scene is this like what was written, or not kept
MOST_PARALLEL_JOINS = 4

JOINS_RULE = (
    "Joins: the video must read as one continuous lesson. Each scene's opens_on takes up "
    "exactly what the scene before ends_on -- the first scene takes up the section's own "
    "opens_on, the last ends on the section's ends_on. A scene never asks again a question "
    "the scene before asked, never restarts a story already begun, and never promises "
    "what the next scene does not deliver. Give each scene the pause_after the moment "
    "needs, and why: 0 when the thought runs straight on, about 1 at a turn, up to 2 after "
    "a section's last scene, a question left to think about, or a reveal that should land."
)

SCRIPT_JOINS_RULE = (
    "Write every scene to its joins: its first sentences take up what the scene before "
    "ended on -- answer the question it posed, never ask it again; its last sentences "
    "hand the next scene what it opens on. Never repeat the sentence or the question the "
    "previous section ended with. Say which course and part this is, and what the viewer "
    "will learn, only in the video's first section and its last -- never re-announce it "
    "in between. Teach, never describe the picture: no 'this portrait is', 'this picture "
    "shows', 'here you can see'."
)


def section_joins_text(plan, section) -> str:
    """What breaking a section into scenes is told about where it sits."""
    index = next(i for i, s in enumerate(plan.sections) if s.id == section.id)
    before = plan.sections[index - 1] if index else None
    after = plan.sections[index + 1] if index + 1 < len(plan.sections) else None
    return "\n".join([
        "--- its joins ---",
        f"The section before ends on: {before.ends_on or before.summary}" if before
        else "This is the video's first section: it opens the video.",
        f"This section opens on: {section.opens_on or '(not said)'}",
        f"This section ends on: {section.ends_on or '(not said)'}",
        f"The section after opens on: {after.opens_on or after.summary}" if after
        else "This is the video's last section: it closes the video.",
    ])


def fit_joins(section, scenes: list) -> list:
    """A section's first scene opens on the section's opens_on, its last ends on its
    ends_on, and its last pauses at least a turn's breath."""
    if not scenes:
        return scenes
    if section.opens_on and not scenes[0].opens_on:
        scenes[0].opens_on = section.opens_on
    if section.ends_on and not scenes[-1].ends_on:
        scenes[-1].ends_on = section.ends_on
    if scenes[-1].pause_after < SECTION_TURN_PAUSE:
        scenes[-1].pause_after = SECTION_TURN_PAUSE
        scenes[-1].pause_why = scenes[-1].pause_why or "the section turns"
    return scenes


def scene_contracts(section) -> str:
    """Each planned scene's joins, for drafting the section."""
    lines = [f"The section opens on: {section.opens_on}" if section.opens_on else "",
             f"The section ends on: {section.ends_on}" if section.ends_on else ""]
    lines += [f"Scene {number}: opens on {scene.opens_on or '(the thread before)'}; "
              f"ends on {scene.ends_on or '(what the next takes up)'}"
              for number, scene in enumerate(section.scenes, start=1)
              if scene.opens_on or scene.ends_on]
    return "\n".join(line for line in lines if line)


def where_it_sits(plan, section) -> str:
    """Whether a section may say which course and part the video is."""
    index = next(i for i, s in enumerate(plan.sections) if s.id == section.id)
    if index == 0:
        return "This section opens the video: say which course and part it is, and what "\
               "the viewer will come away with."
    if index == len(plan.sections) - 1:
        return "This section closes the video: you may name the course and part as you "\
               "sum up."
    return "This section is in the middle of the video: never announce the course or the "\
           "part again -- carry straight on from the section before."


# --- found by code ------------------------------------------------------------------------

_SENTENCE = re.compile(r"(?<=[.!?])\s+")
_DESCRIBES_PICTURE = re.compile(
    r"\b(?:this|the) (?:portrait|picture|image|illustration|drawing) (?:is|shows)\b"
    r"|\bhere you can see\b|\bas you can see (?:here|in this)\b", re.IGNORECASE)
_OPENERS = re.compile(r"^(?:now,? )?(?:let's|let us) (?:begin|start)\b", re.IGNORECASE)


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in _SENTENCE.split(text.strip()) if part.strip()]


def _norm(sentence: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", sentence.lower()).strip()


def join_problems(plan, script) -> list[tuple[str, str]]:
    """(scene id, what is wrong) at each join and in each scene, found by code."""
    sections = {s.section_id: s for s in script.section_scripts}
    ordered = [(section, scene) for section in plan.sections
               if (written := sections.get(section.id))
               for scene in written.scenes if scene.narration.strip()]
    middle = {s.id for s in plan.sections[1:-1]}
    names = [n for n in (plan.course, plan.this_video) if n and len(n) > 3]
    found: list[tuple[str, str]] = []
    for (_, before), (_, after) in zip(ordered, ordered[1:], strict=False):
        end, start = _sentences(before.narration)[-2:], _sentences(after.narration)[:2]
        asked = {_norm(s) for s in end if s.endswith("?")}
        if any(_norm(s) in asked for s in start if s.endswith("?")) or any(
                difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio() > 0.8
                for a in end for b in start):
            found.append((after.id, "opens by repeating what the scene before ended on"))
        if start and _OPENERS.match(start[0]) and any(_OPENERS.match(s) for s in end):
            found.append((after.id, "begins again what the scene before just began"))
    for section, scene in ordered:
        if section.id in middle and any(
                re.search(rf"\b{re.escape(name)}\b", scene.narration, re.IGNORECASE)
                for name in names):
            found.append((scene.id, "announces the course or part in the middle of the video"))
        if _DESCRIBES_PICTURE.search(scene.narration):
            found.append((scene.id, "describes the picture instead of teaching"))
    return found


# --- smoothed once all is written -------------------------------------------------------------


class JoinFix(BaseModel):
    before: str = Field(description="The earlier scene's narration, its last sentences "
                                    "changed only if the join needs it.")
    after: str = Field(description="The later scene's narration, its first sentences "
                                   "changed only if the join needs it.")


def close_enough(old: str, new: str) -> bool:
    return (bool(new.strip())
            and difflib.SequenceMatcher(None, old, new).ratio() >= SMALLEST_KEPT_LIKENESS
            and 0.75 <= len(new) / max(1, len(old)) <= 1.25)


def smooth_joins(slug: str, identity: str = "") -> list[str]:
    """Read every join between sections, and every join the code found wrong, and
    rewrite only the sentences at it. Returns notes of what changed."""
    from pipeline.core import require_project
    from pipeline.fact_ledger import broken, forbidden_for
    from pipeline.llm import ModelCallFailed, ModelNotConfigured, complete_structured
    from pipeline.planning import PlanStore
    from pipeline.scripting import ScriptStore

    project = require_project(slug)
    plan, store = PlanStore(project.root).load(), ScriptStore(project.root)
    script = store.load()
    by_section = {s.section_id: s for s in script.section_scripts}
    plan_scenes = {scene.id: scene for section in plan.sections for scene in section.scenes}
    pairs = []          # (section of the later scene, earlier scene, later scene)
    flat = [(section, scene) for section in plan.sections
            if (written := by_section.get(section.id)) for scene in written.scenes]
    flagged = {scene_id for scene_id, _ in join_problems(plan, script)}
    for (first_section, before), (section, after) in zip(flat, flat[1:], strict=False):
        if first_section.id != section.id or after.id in flagged:
            pairs.append((section, before, after))
    if not pairs:
        return []
    problems = dict(join_problems(plan, script))
    system = ("You smooth the join between two scenes of a narrated lesson so it reads as "
              "one continuous teacher speaking. " + SCRIPT_JOINS_RULE + " Change only the "
              "earlier scene's last one or two sentences and the later scene's first one or "
              "two; keep every other word, every fact and the length. If the join already "
              "reads well, return both unchanged.")

    def propose(pair) -> JoinFix | None:
        section, before, after = pair
        planned_before, planned_after = plan_scenes.get(before.id), plan_scenes.get(after.id)
        prompt = "\n\n".join(part for part in (
            identity and f"--- what this video is ---\n{identity}",
            f"Where the later scene sits: {where_it_sits(plan, section)}",
            f"The earlier scene should end on: {planned_before.ends_on}"
            if planned_before and planned_before.ends_on else "",
            f"The later scene should open on: {planned_after.opens_on}"
            if planned_after and planned_after.opens_on else "",
            f"Found wrong here: {problems[after.id]}" if after.id in problems else "",
            f"--- the earlier scene ---\n{before.narration}",
            f"--- the later scene ---\n{after.narration}",
        ) if part)
        try:
            return complete_structured(JoinFix, system, prompt)
        except (ModelCallFailed, ModelNotConfigured):
            return None

    # Asked side by side; kept one by one -- two joins can share a scene, and a scene
    # already rewritten at one join is not rewritten again at the next.
    with ThreadPoolExecutor(max_workers=MOST_PARALLEL_JOINS) as pool:
        answers = list(pool.map(propose, pairs))
    notes, changed = [], set()
    for (section, before, after), answer in zip(pairs, answers, strict=True):
        if answer is None:
            continue
        forbidden = forbidden_for(project, section)
        kept = []
        for scene, new in ((before, answer.before.strip()), (after, answer.after.strip())):
            if scene.id not in changed and new != scene.narration.strip() \
                    and close_enough(scene.narration, new) \
                    and not broken([type(scene)(narration=new, brief="")], forbidden):
                scene.narration = new
                changed.add(scene.id)
                kept.append(scene.id)
        if kept:
            notes.append(f"Smoothed the join into “{section.title}”.")
    if notes:
        script.section_scripts = [type(s).model_validate(s.model_dump())   # body follows
                                  for s in script.section_scripts]
        store.save(script)
    return notes


def pauses_ms(plan, section_id: str) -> list[int]:
    """The planned pause after each of a section's scenes, in milliseconds."""
    section = next((s for s in plan.sections if s.id == section_id), None)
    return [round(scene.pause_after * 1000) for scene in section.scenes] if section else []
