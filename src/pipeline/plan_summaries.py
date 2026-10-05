"""AI · write summaries: one line per section, saying what the viewer learns.

The only AI on the Outline tab besides a full draft, and kept to that one job.
It never changes the plan: it writes *proposals*, shown under each section, and
a person accepts them one at a time or all at once. The page says how many
sections and how many model calls (one) before anything is sent.

Which sections it writes for is a fixed rule: every teaching section whose
summary is missing, a stand-in, source text, or talks about the source
(`lesson_plan.summary_problem`) -- or, when asked, every teaching section.

Proposals are kept at `drafts/summaries.json`, beside a pending plan draft, so a
reload does not throw away a paid call.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from pipeline.core import OperationFailed, require_project
from pipeline.extraction import ExtractionStore
from pipeline.llm import ModelCallFailed, ModelNotConfigured, complete_structured
from pipeline.narration_voice import reporting_phrases
from pipeline.planning import PlanStore
from pipeline.storage.documents import read_json_object, write_text_atomically

SOURCE_CHARACTERS_PER_SECTION = 1500
LONGEST_SUMMARY_WORDS = 30


class _Written(BaseModel):
    section_id: str
    summary: str


class _Batch(BaseModel):
    summaries: list[_Written] = Field(default_factory=list)


def _path(project):
    return project.root / "drafts" / "summaries.json"


def _load(project) -> dict[str, Any]:
    return read_json_object(_path(project), "summary proposals") or {"items": {}}


def _save(project, proposals: dict[str, Any]) -> None:
    path = _path(project)
    if not proposals["items"]:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    write_text_atomically(path, json.dumps(proposals, indent=2, ensure_ascii=False))


def _wanted(plan, everything: bool) -> list:
    from pipeline.lesson_plan import FRAME_ROLES, summary_problem

    body = [s for s in plan.sections if s.role not in FRAME_ROLES]
    return body if everything else [s for s in body if summary_problem(s)]


def summaries_view(project, plan) -> dict[str, Any]:
    """What the button will do, and what is waiting to be accepted."""
    items = _load(project)["items"]
    current = {s.id for s in plan.sections}
    return {
        "needing": len(_wanted(plan, False)),
        "teaching_sections": len(_wanted(plan, True)),
        "model_calls": 1,
        "proposals": {sid: item for sid, item in items.items() if sid in current},
    }


def propose_summaries(slug: str, everything: bool = False) -> dict[str, Any]:
    """One model call for every section that needs a summary. Saves proposals only."""
    from pipeline.plan_drafting import section_source_text

    project = require_project(slug)
    plan = PlanStore(project.root).load()
    sections = _wanted(plan, everything)
    if not sections:
        raise OperationFailed("Every teaching section already says what the viewer learns.")
    extraction = ExtractionStore(project.root).load()

    objectives = [o.text for o in plan.learning_objectives if o.is_included]
    parts = []
    for section in sections:
        text, _cut = section_source_text(extraction, section.sources)
        parts.append(f"[{section.id}] {section.title}\n"
                     f"{text[:SOURCE_CHARACTERS_PER_SECTION] or '(no source text)'}")
    system_prompt = (
        "You write the plan of an explainer video. For EACH section given, write one "
        f"sentence of at most {LONGEST_SUMMARY_WORDS} words saying what the viewer learns "
        "or experiences in it, stated plainly as the idea itself (\"How the brain builds "
        "a picture of the body from touch and movement.\"). Never describe the source: "
        "do not say \"the chapter\", \"this slide\", \"the author\", \"the text\" or "
        "\"explores\". Use only what the section's source text says. Return every "
        "section's id exactly as given."
    )
    user_prompt = (
        f"Audience: {plan.selected_audience or 'not chosen'}\n"
        f"Learning objectives:\n" + ("\n".join(f"- {o}" for o in objectives) or "(none)")
        + "\n\nSections:\n\n" + "\n\n".join(parts)
    )
    try:
        batch = complete_structured(_Batch, system_prompt, user_prompt)
    except (ModelCallFailed, ModelNotConfigured) as failure:
        raise OperationFailed(f"Could not write summaries: {failure}") from failure

    asked = {s.id: s for s in sections}
    proposals = _load(project)
    made_at = datetime.now(UTC).isoformat(timespec="seconds")
    for written in batch.summaries:
        section = asked.get(written.section_id)
        summary = " ".join(written.summary.split())
        if section is None or not summary:
            continue
        proposals["items"][section.id] = {
            "summary": summary, "was": section.summary, "made_at": made_at,
            # Said, not hidden: the model was told not to, and a person decides.
            "talks_about_source": bool(reporting_phrases(summary)),
        }
    _save(project, proposals)
    return summaries_view(project, plan)


def accept_summaries(slug: str, section_ids: list[str] | None = None) -> None:
    """Put proposals into the plan -- these, or all of them."""
    from pipeline.lesson_plan import save_plan

    project = require_project(slug)
    plan = PlanStore(project.root).load()
    proposals = _load(project)
    chosen = set(section_ids) if section_ids is not None else set(proposals["items"])
    for section in plan.sections:
        item = proposals["items"].get(section.id)
        if item and section.id in chosen:
            section.summary, section.summary_origin = item["summary"], "ai"
    save_plan(project, plan)
    proposals["items"] = {k: v for k, v in proposals["items"].items() if k not in chosen}
    _save(project, proposals)


def dismiss_summaries(slug: str, section_ids: list[str] | None = None) -> None:
    project = require_project(slug)
    proposals = _load(project)
    chosen = set(section_ids) if section_ids is not None else set(proposals["items"])
    proposals["items"] = {k: v for k, v in proposals["items"].items() if k not in chosen}
    _save(project, proposals)
