"""Script & Staging, handed on: the checks the script must pass, and the
transferred copy every later stage reads.

The script is written against the *transferred* Scene Plan, section by section,
by hand or by accepting what the Scripting agent writes into an empty section.
Later stages -- the visuals, the render, the review, the export -- read one
script: the one that was **transferred**. A sentence being rewritten never
reaches a render half-finished.

Before the first transfer, later stages read the working script, as they
always did; from the first transfer on, only the transferred copy. The page
says which.

The checks are fixed rules over the script, the plan it is written against,
the extraction and the review; none calls a model. Two things block a transfer,
because each would be wrong in the video itself: a section with no narration
(a silent card), and a {{VARIABLE}} nobody defined (spoken as literal braces).
Everything else is a warning.

Stored at `scripting/script.transferred.json`.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from pipeline import upstream
from pipeline.core import OperationFailed, require_project
from pipeline.extraction import ExtractionStore
from pipeline.freshness import narration_freshness
from pipeline.plan_handoff import FAIL, NOT_APPLICABLE, PASS, WARN, plan_for_later_stages
from pipeline.plan_handoff import handoff_state as plan_handoff_state
from pipeline.scripting import OVER_BUDGET_TOLERANCE, Script, ScriptStore
from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore
from pipeline.storage.layout import artifact_path

# Narration under this share of its section's planned length is reported: a
# ten-word section planned for a minute is a different video from the plan.
UNDER_BUDGET_SHARE = 0.5


class TransferredScript(BaseModel):
    script: Script = Field(default_factory=Script)
    transferred_at: str = ""
    fingerprint: str = ""


class TransferredScriptStore(JsonDocumentStore[TransferredScript]):
    def __init__(self, project_root) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.SCRIPT_STAGING).with_name(
                "script.transferred.json"),
            model_type=TransferredScript, build_default=TransferredScript,
            description="transferred script",
        )


def fingerprint(script: Script) -> str:
    text = json.dumps(script.model_dump(mode="json"), sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:20]


def script_for_later_stages(project) -> Script:
    """The script every stage after Script & Staging reads: the transferred one,
    or -- before anything was ever transferred -- the working one."""
    transferred = TransferredScriptStore(project.root).load()
    if transferred.transferred_at:
        return transferred.script
    return ScriptStore(project.root).load()


def _check(key: str, name: str, rule: str, status: str, detail: str) -> dict[str, str]:
    return {"key": key, "name": name, "rule": rule, "status": status, "detail": detail}


def script_checks(project, script: Script) -> list[dict[str, str]]:
    """Every check the script goes through, in order, with what each found."""
    from pipeline.presentation import _open_comments_by_section

    plan = plan_for_later_stages(project)
    sections = plan.sections
    titles = {s.id: s.title or "Untitled" for s in sections}
    audit = script.audit([s.id for s in sections], {s.id: s.estimated_seconds for s in sections},
                         titles)
    by_id = {s.section_id: s for s in script.section_scripts}
    checks = []

    unwritten = audit["unwritten_section_ids"]
    checks.append(_check(
        "written", "Every section has narration", "Each planned section is written",
        NOT_APPLICABLE if not sections else FAIL if unwritten else PASS,
        f"Not written: {', '.join(titles[s] for s in unwritten[:6])}"
        + (f" and {len(unwritten) - 6} more" if len(unwritten) > 6 else "") + "."
        if unwritten else f"All {len(sections)} section(s) are written."
        if sections else "The Scene Plan has no sections yet."))

    checks.append(_check(
        "variables", "Variables defined", "Every {{NAME}} used is defined",
        FAIL if audit["undefined_variables"] else PASS,
        "Spoken as written, braces and all: " + ", ".join(audit["undefined_variables"])
        if audit["undefined_variables"] else "Every variable used is defined."))

    checks.append(_check(
        "variable-names", "Variable names", "Capitals, digits and _ only, starting with a letter",
        WARN if audit["invalid_variables"] else PASS,
        "Unusable: " + ", ".join(audit["invalid_variables"]) if audit["invalid_variables"]
        else "Every name is usable."))

    short = [s for s in sections if (w := by_id.get(s.id)) and w.body.strip()
             and w.estimated_seconds < s.estimated_seconds * UNDER_BUDGET_SHARE]
    over = audit["over_budget"]
    checks.append(_check(
        "section-lengths", "Section lengths",
        f"Each written section between {int(UNDER_BUDGET_SHARE * 100)}% and "
        f"{int(OVER_BUDGET_TOLERANCE * 100)}% of its planned length",
        WARN if over or short else PASS if sections else NOT_APPLICABLE,
        "; ".join([f"{o['title']}: ~{o['estimated_seconds']} s of {o['planned_seconds']} s"
                   for o in over[:4]]
                  + [f"{titles[s.id]}: ~{by_id[s.id].estimated_seconds} s of "
                     f"{s.estimated_seconds} s" for s in short[:4]])
        or "Every written section is close to its planned length."))

    length = plan.length
    spoken = sum(by_id[s.id].estimated_seconds for s in sections if s.id in by_id)
    checks.append(_check(
        "total", "Total length", "Within the length the plan agreed",
        NOT_APPLICABLE if not spoken or not length.is_known
        else PASS if length.shortest_seconds <= spoken <= length.longest_seconds else WARN,
        f"About {round(spoken / 60, 1)} min spoken. Agreed: {length.understood}"
        if length.is_known else "The plan has no agreed length."))

    stale = narration_freshness(plan, script, ExtractionStore(project.root).load())
    checks.append(_check(
        "up-to-date", "Up to date", "Written against the plan section and source as they are now",
        WARN if stale else PASS if sections else NOT_APPLICABLE,
        "; ".join(f"{titles.get(e['section_id'], '?')}: {' and '.join(e['reasons'])}"
                  for e in stale[:4]) or "Nothing changed under any narration."))

    bare = [s for s in sections if (w := by_id.get(s.id))
            and any(scene.narration.strip() and not scene.brief.strip() for scene in w.scenes)]
    checks.append(_check(
        "briefs", "On-screen briefs", "Every scene says what is shown while it is said",
        WARN if bare else PASS if sections else NOT_APPLICABLE,
        f"Scenes with no brief in: {', '.join(titles[s.id] for s in bare[:6])}."
        if bare else "Every scene has its brief."))

    from pipeline.narration_voice import reporting_phrases

    reporting = [(titles[s.id], found) for s in sections if (w := by_id.get(s.id))
                 for found in [reporting_phrases(w.body)] if found]
    checks.append(_check(
        "voice", "Teacher's voice",
        "The narrator teaches the viewer; it never talks about \"the chapter\", "
        "\"the book\", \"the author\" or \"the slide\"",
        WARN if reporting else PASS if sections else NOT_APPLICABLE,
        "; ".join(f"{title}: \u201c{found[0]}\u201d"
                  + (f" (+{len(found) - 1} more)" if len(found) > 1 else "")
                  for title, found in reporting[:4])
        + (" -- Rewrite these, or redraft the section." if reporting else "")
        if reporting else "Every section is told in the teacher's own voice."))

    claims = [f"“{titles.get(entry.section_id, 'Untitled')}” {claim}"
              for entry in script.section_scripts if entry.section_id in titles
              for claim in entry.unsupported]
    missing = [f"“{titles.get(entry.section_id, 'Untitled')}” {point}"
               for entry in script.section_scripts if entry.section_id in titles
               for point in entry.uncovered]
    checks.append(_check(
        "facts", "Follows the slides",
        "Every slide point covered; nothing that leads away from the slides or gets them "
        "wrong (checked, and revised by the agent, when it was drafted)",
        WARN if claims or missing else PASS,
        " ".join(part for part in (
            f"{len(missing)} slide point(s) not covered: " + "; ".join(missing[:3]) + "."
            if missing else "",
            f"{len(claims)} sentence(s) to look at: " + "; ".join(claims[:3]) + "."
            if claims else "") if part)
        + " -- Redraft the section, or edit it; keep what is right."
        if claims or missing else "Every slide point is covered, and nothing leads away."))

    conflicts = [f"“{titles.get(entry.section_id, 'Untitled')}” {item}"
                 for entry in script.section_scripts if entry.section_id in titles
                 for item in entry.slide_wrong]
    # Not a decision left open: the video never teaches a slide's error. The narration
    # says what is right, or leaves the doubtful detail out; one still repeating it is
    # a wrong claim, listed under "Follows the slides".
    checks.append(_check(
        "slides-wrong", "Slide errors not repeated",
        "Where a slide states something factually wrong, the video says what is right "
        "or leaves the detail out -- never the slide's error",
        PASS,
        f"{len(conflicts)} slide error(s) found, and not repeated: " + "; ".join(conflicts[:3])
        + (" ..." if len(conflicts) > 3 else "") if conflicts else "None found."))

    comments = _open_comments_by_section(project, plan, Stage.SCRIPT_STAGING)
    open_count = sum(len(found) for found in comments.values())
    checks.append(_check(
        "comments", "Review comments", "No open review comment sent back to Scripting",
        WARN if open_count else PASS,
        f"{open_count} open comment(s) to answer." if open_count else "None open."))

    orphaned = audit["orphaned_section_ids"]
    checks.append(_check(
        "unattached", "Unattached narration", "No narration left from sections the plan dropped",
        WARN if orphaned else PASS,
        f"{len(orphaned)} piece(s) of narration belong to no section. Attach or delete them "
        f"on the Setup tab." if orphaned else "None."))

    plan_state = plan_handoff_state(project)
    checks.append(_check(
        "plan", "Scene Plan transferred",
        "Written against a transferred plan with no changes waiting",
        WARN if not plan_state["has_transferred"] or plan_state["pending"] else PASS,
        "The Scene Plan has never been transferred." if not plan_state["has_transferred"]
        else "The Scene Plan has changes that are not transferred yet."
        if plan_state["pending"] else "Written against the transferred plan."))
    return checks


def handoff_state(project) -> dict[str, Any]:
    script = ScriptStore(project.root).load()
    transferred = TransferredScriptStore(project.root).load()
    checks = script_checks(project, script)
    return {
        "checks": checks,
        "failing": sum(1 for c in checks if c["status"] == FAIL),
        "warning": sum(1 for c in checks if c["status"] == WARN),
        "has_transferred": bool(transferred.transferred_at),
        "transferred_at": transferred.transferred_at,
        "pending": bool(script.section_scripts) and (
            fingerprint(script) != transferred.fingerprint
            or upstream.is_behind(project, "script-staging")),
    }


def read_script_handoff(slug: str) -> dict[str, Any]:
    return handoff_state(require_project(slug))


def transfer_script(slug: str) -> dict[str, Any]:
    """Hand the script as it stands to the next layer. Refused while a check fails."""
    project = require_project(slug)
    script = ScriptStore(project.root).load()
    failing = [c for c in script_checks(project, script) if c["status"] == FAIL]
    if failing:
        raise OperationFailed(
            "The script cannot be transferred while a check fails: "
            + "; ".join(f"{c['name']} -- {c['detail']}" for c in failing))
    TransferredScriptStore(project.root).save(TransferredScript(
        script=script, transferred_at=datetime.now(UTC).isoformat(timespec="seconds"),
        fingerprint=fingerprint(script)))
    upstream.record(project, "script-staging")
    return handoff_state(project)


def delete_unattached_narration(slug: str) -> dict[str, Any]:
    """Delete every piece of narration that belongs to no section of the plan."""
    project = require_project(slug)
    known = {section.id for section in plan_for_later_stages(project).sections}
    store = ScriptStore(project.root)
    script = store.load()
    kept = [s for s in script.section_scripts if s.section_id in known]
    removed = len(script.section_scripts) - len(kept)
    store.save(script.model_copy(update={"section_scripts": kept}))
    return {"removed": removed} | handoff_state(project)
