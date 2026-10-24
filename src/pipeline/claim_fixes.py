"""A sentence the fact check found wrong is corrected, not only reported.

Drafting checks every section against its slides and the fact ledger, and revises;
what is still wrong after that was listed as a warning and left in the script. v8
and v9 both reached the video saying Helmholtz "used electromagnetic wave theory" --
caught, warned, fixed by hand each time. Once the script is drafted, each claim
still said is corrected here: only its sentence, to what is right (or with the
doubtful detail left out), and only an edit that removes the sentence, stays small
and brings in nothing the facts forbid is kept. The claim is then cleared.
"""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel, Field

MOST_PARALLEL_FIXES = 4
_CLAIM = re.compile(r"scene (\d+): (?:says )?'(.+?)' -- (.+)", re.DOTALL)


class Corrected(BaseModel):
    narration: str = Field(description="The scene's narration with only the wrong sentence "
                                       "corrected; every other word as it was.")


def _parse(claim: str) -> tuple[int, str, str] | None:
    found = _CLAIM.search(claim)
    return (int(found.group(1)), found.group(2), found.group(3)) if found else None


def fix_claims(slug: str) -> list[str]:
    """Correct every claim still said in the script. Returns notes of what changed."""
    from pipeline.core import require_project
    from pipeline.fact_ledger import broken, forbidden_for
    from pipeline.llm import ModelCallFailed, ModelNotConfigured, complete_structured
    from pipeline.planning import PlanStore
    from pipeline.scene_joins import close_enough
    from pipeline.scripting import ScriptStore

    project = require_project(slug)
    plan, store = PlanStore(project.root).load(), ScriptStore(project.root)
    script = store.load()
    titles = {section.id: section.title for section in plan.sections}
    sections = {section.id: section for section in plan.sections}
    work = []           # (section script, scene, quoted sentence, why, claim)
    for written in script.section_scripts:
        for claim in written.unsupported:
            parsed = _parse(claim)
            if parsed is None:
                continue
            number, quoted, why = parsed
            if 1 <= number <= len(written.scenes) and \
                    quoted.lower() in written.scenes[number - 1].narration.lower():
                work.append((written, written.scenes[number - 1], quoted, why, claim))
    if not work:
        return []
    system = ("You correct one sentence of a narrated lesson that a fact check found wrong. "
              "Rewrite only that sentence so it says what is right -- or leaves the doubtful "
              "detail out -- in the same voice, about the same length. Keep every other word "
              "of the narration exactly as it is.")

    def correct(item) -> Corrected | None:
        _written, scene, quoted, why, _claim = item
        try:
            return complete_structured(Corrected, system, "\n\n".join([
                f"--- the narration ---\n{scene.narration}",
                f"--- the wrong sentence ---\n{quoted}",
                f"--- what is right ---\n{why}"]))
        except (ModelCallFailed, ModelNotConfigured):
            return None

    with ThreadPoolExecutor(max_workers=MOST_PARALLEL_FIXES) as pool:
        answers = list(pool.map(correct, work))
    notes = []
    for (written, scene, quoted, _why, claim), answer in zip(work, answers, strict=True):
        if answer is None:
            continue
        new = answer.narration.strip()
        section = sections.get(written.section_id)
        forbidden = forbidden_for(project, section) if section else []
        if quoted.lower() not in new.lower() and close_enough(scene.narration, new) \
                and not broken([type(scene)(narration=new, brief="")], forbidden):
            scene.narration = new
            written.unsupported = [c for c in written.unsupported if c != claim]
            notes.append(f"Corrected in “{titles.get(written.section_id, '?')}”: "
                         f"“{quoted[:80]}”.")
    if notes:
        script.section_scripts = [type(s).model_validate(s.model_dump())   # body follows
                                  for s in script.section_scripts]
        store.save(script)
    return notes
