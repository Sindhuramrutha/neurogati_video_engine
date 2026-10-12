"""Is this artifact still true of what it was built from?

Every stage here reads the stage before it, and none of them noticed when what
they read had changed underneath. A plan drafted from an extraction that has
since been re-run, narration written against a section someone has rewritten, a
timeline left over from an abandoned script -- each of those looks exactly like
current work, and each produced a finished-looking video that was wrong.

So the comparisons live together, in one module that owns no data and changes
nothing. Each one takes the two documents and returns what is out of step, in
words a person can act on; deciding what to do about it belongs to the stage.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from pipeline.composition import ClipKind, Composition
from pipeline.extraction import (
    Extraction,
)
from pipeline.planning import (
    Plan,
    PlanSection,
)
from pipeline.scripting import (
    Script,
)


def cut_freshness(plan: Plan, composition: Composition) -> dict[str, Any]:
    """Whether the timeline still describes the plan it was built from.

    Without this check a finished project can look finished while being wrong:
    a plan re-drafted from a different source document leaves the timeline and
    the chapters as the previous render made them, later renders refuse to
    rebuild them because they count as hand-edited, and Studio and Reviewing
    keep showing sections about electrodes for a video about neural networks.

    Matched on titles, because a clip records what it shows rather than which
    section produced it. That is a weaker link than an id and is the reason this
    reports "these do not appear in the plan" rather than claiming to know which
    section each clip came from.
    """
    scene_titles = [
        clip.text.strip() or clip.label.strip()
        for track in composition.tracks
        for clip in track.clips
        if clip.kind == ClipKind.SCENE
    ]
    planned_titles = {section.title.strip() for section in plan.sections if section.title.strip()}

    unknown = [title for title in scene_titles if title and title not in planned_titles]
    missing = [
        title for title in planned_titles
        if title not in set(scene_titles)
    ]

    warnings: list[str] = []
    if scene_titles and unknown:
        warnings.append(
            f"{len(unknown)} of {len(scene_titles)} section(s) in this timeline are not in "
            f"the plan any more — it was built from a different script. Rebuild it, or "
            f"re-render, before trusting the cut."
        )
    elif scene_titles and missing:
        warnings.append(
            f"{len(missing)} planned section(s) are missing from this timeline: "
            f"{', '.join(sorted(missing)[:3])}"
            f"{'…' if len(missing) > 3 else ''}."
        )

    return {
        "has_timeline": bool(scene_titles),
        "was_generated": bool(composition.generated_from_render_at),
        "section_count": len(scene_titles),
        "unknown_sections": unknown,
        "missing_sections": sorted(missing),
        "is_stale": bool(scene_titles and (unknown or missing)),
        "warnings": warnings,
    }

def source_outline(extraction: Extraction) -> list[dict[str, Any]]:
    """Every extracted document's headings: what a section can point at."""
    return [
        {
            "file_name": document.file_name,
            "words": document.word_count,
            "headings": document.heading_outline(),
        }
        for document in extraction.documents
    ]

def plan_freshness(plan: Plan, extraction: Extraction) -> dict[str, Any]:
    """Whether this plan still matches the extracted content it was made from.

    Three separate questions, because they need different answers:

    - **stale**: the extraction changed since the plan was drafted or confirmed.
      Something may be new, gone or reworded; the plan might still be fine.
    - **missing sources**: a section points at a location that is no longer in
      the extraction. That section is definitely teaching from nothing.
    - **unlinked**: a plan with sections and no record of what they are based
      on. A real plan was in exactly this state -- describing a chapter the
      extraction no longer held -- and nothing could notice.
    """
    current = extraction.content_fingerprint()
    is_linked = bool(plan.extraction_fingerprint)
    is_stale = is_linked and bool(current) and plan.extraction_fingerprint != current

    missing = []
    for section in plan.sections:
        gone = [
            reference.label for reference in section.sources
            if not extraction.has_location(reference.file_name, reference.heading_path)
        ]
        if gone:
            missing.append({"section_id": section.id, "title": section.title, "missing": gone})

    uses_sources = is_linked or any(section.sources for section in plan.sections)
    without_sources = [s.id for s in plan.sections if not s.sources] if uses_sources else []
    is_unlinked = bool(plan.sections) and not uses_sources and bool(extraction.documents)

    warnings = []
    if is_stale:
        warnings.append("the extraction has changed since this plan was drafted")
    if missing:
        warnings.append(
            f"{len(missing)} section(s) point at content that is no longer in the extraction"
        )
    if is_unlinked:
        warnings.append("this plan is not linked to the extracted content")

    return {
        "has_extraction": bool(extraction.documents),
        "extraction_fingerprint": current,
        "is_linked": is_linked,
        "is_stale": is_stale,
        "is_unlinked": is_unlinked,
        "sections_with_missing_sources": missing,
        "sections_without_sources": without_sources,
        "warnings": warnings,
    }

def _fingerprint(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]

def narration_fingerprints(section: PlanSection, extraction: Extraction) -> dict[str, str]:
    """What a section's narration is written against: the plan section's content
    and the text of the sources it covers.

    Length and presentation are left out on purpose. A new target duration or a
    different rendering approach does not make what was said wrong; a changed
    summary, different sources, or reworded source material might.
    """
    source_text = []
    for reference in section.sources:
        document = extraction.document(reference.file_name)
        source_text.append(document.text_under(reference.heading_path) if document else "")
    return {
        "plan": _fingerprint([
            section.title, section.summary,
            [[r.file_name, r.heading_path] for r in section.sources],
        ]),
        "source": _fingerprint(source_text),
    }

def narration_freshness(
    plan: Plan, script: Script, extraction: Extraction
) -> list[dict[str, Any]]:
    """Sections whose narration was written against something that has changed.

    Narration with no record of what it was written from is not judged: there is
    nothing to compare, and calling all of it out of date would be noise.
    """
    by_id = {s.section_id: s for s in script.section_scripts}
    found = []
    for section in plan.sections:
        written = by_id.get(section.id)
        if written is None or not written.body.strip() or not written.written_from:
            continue
        current = narration_fingerprints(section, extraction)
        reasons = []
        if written.written_from.get("plan") != current["plan"]:
            reasons.append("the plan section changed")
        if written.written_from.get("source") != current["source"]:
            reasons.append("its source content changed")
        if reasons:
            found.append({"section_id": section.id, "title": section.title, "reasons": reasons})
    return found
