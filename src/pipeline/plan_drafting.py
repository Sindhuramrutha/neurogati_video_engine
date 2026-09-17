"""Drafting a plan from the whole extraction, in two passes.

The Planning agent used to be handed the extracted text cut off at 40,000
characters. Three short documents already came to 42,000, so it never saw the
last slides of the deck; a real course chapter or a fifty-slide deck would lose
most of its material, and the plan would quietly cover only the beginning.

So drafting now works the way a person plans a long source:

1. **Outline from every heading.** Each document's headings, with how many words
   sit under each, are small enough to show in full even for a long source. The
   agent groups them into sections in teaching order and says, for each section,
   exactly which locations it covers.
2. **Each section from its own text.** For every section, the agent is given the
   full text of the locations it covers -- and only those -- and writes the
   summary, chooses how it should be shown and why, and estimates its length.
   These run at the same time.

The result is a pending draft, never the plan: someone accepts it, in whole or
section by section, from the Planning page or through `accept_plan_draft`.
"""

from __future__ import annotations

import logging
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from pipeline.agent_runtime import build_system_prompt, resolve_agent
from pipeline.extraction import BlockKind, Extraction, ExtractionStore
from pipeline.llm import ModelCallFailed, ModelNotConfigured, complete_structured
from pipeline.operations import (
    OperationFailed,
    extraction_freshness,
    read_plan_draft,
    require_project,
)
from pipeline.planning import (
    LearningObjective,
    Plan,
    PlanDraftStore,
    PlanSection,
    PlanStore,
    RenderingApproach,
    SourceReference,
)
from pipeline.stages import Stage

logger = logging.getLogger(__name__)

# The heading outline of every document. Headings are short, so this holds a very
# large source; past it, the deepest heading levels are dropped first, and the
# draft says so.
MAXIMUM_OUTLINE_CHARACTERS = 60_000

# One section's own source text. A section normally covers a few headings; one
# that points at a whole book is cut here, and the draft says which.
MAXIMUM_SECTION_SOURCE_CHARACTERS = 24_000

MAXIMUM_DRAFTED_SECTIONS = 30
MAXIMUM_PARALLEL_SECTION_DRAFTS = 6

WORDS_PER_MINUTE_OF_NARRATION = 150


# --- what the model returns ----------------------------------------------------


class OutlineSection(BaseModel):
    title: str = Field(description="What this section teaches, as a short title.")
    source_ids: list[str] = Field(
        description="Ids of the outline entries this section covers, such as h12, or d2 "
                    "for a whole document."
    )
    estimated_seconds: int = Field(
        default=60, description="Spoken length, estimated from the words it covers."
    )
    objective_numbers: list[int] = Field(
        default_factory=list,
        description="Numbers of the learning objectives this section serves (1-based).",
    )


class DraftOutline(BaseModel):
    learning_objectives: list[str] = Field(
        description="What a viewer should be able to do afterwards, from the material only."
    )
    key_themes: list[str] = Field(
        default_factory=list, description="Three to six short phrases from the material."
    )
    sections: list[OutlineSection]


class SectionDetail(BaseModel):
    summary: str = Field(
        description="One or two sentences on what this section teaches, from its text only."
    )
    rendering_approach: RenderingApproach
    rendering_reason: str = Field(description="One sentence: why that approach.")
    estimated_seconds: int = Field(
        description="How long a faithful spoken treatment of this text takes."
    )


# --- the source, as the agent is shown it --------------------------------------


def outline_for_agent(
    extraction: Extraction,
) -> tuple[str, list[str], dict[str, SourceReference]]:
    """Every heading of every document, as the first pass reads it, and the ids
    that stand for them.

    Each entry has a short id -- `d1` for a whole document, `h12` for a heading
    and everything under it -- and the agent answers with ids. It used to answer
    by copying full heading paths back, which had two costs. Long paths repeated
    for every section filled a reasoning model's output budget, and a real draft
    was cut off mid-answer. And a copied path could be subtly wrong: one draft
    "tidied" a document's odd hierarchy, and the location no longer matched. An
    id either names a real place or it does not.
    """
    notes: list[str] = []
    index: dict[str, SourceReference] = {}
    entries: list[tuple[int, str]] = []   # (heading level, line)
    heading_number = 0

    for document_number, document in enumerate(extraction.documents, start=1):
        document_id = f"d{document_number}"
        index[document_id] = SourceReference(file_name=document.file_name, heading_path=[])
        entries.append((
            0, f"\n=== {document_id} · {document.file_name} ({document.word_count:,} words) ===",
        ))
        for heading in document.heading_outline():
            heading_number += 1
            heading_id = f"h{heading_number}"
            index[heading_id] = SourceReference(
                file_name=document.file_name, heading_path=heading["heading_path"]
            )
            indent = "  " * max(0, heading["level"] - 1)
            preview = _preview_for_generic_heading(document, heading["heading_path"])
            entries.append((
                heading["level"],
                f"{indent}- {heading_id} · {heading['heading_path'][-1]} · "
                f"{heading['words']:,} words{preview}",
            ))

    deepest = max((level for level, _ in entries), default=0)
    rendered = "\n".join(line for _, line in entries)
    while len(rendered) > MAXIMUM_OUTLINE_CHARACTERS and deepest > 1:
        entries = [(level, line) for level, line in entries if level < deepest]
        notes.append(
            f"The source has so many headings that level-{deepest} headings were left out "
            f"of the outline; sections still receive their full text."
        )
        deepest -= 1
        rendered = "\n".join(line for _, line in entries)

    return rendered, notes, index


GENERIC_HEADING = re.compile(r"^(slide|page)\s+\d+$", re.IGNORECASE)
PREVIEW_WORDS = 16


def _preview_for_generic_heading(document, heading_path: list[str]) -> str:
    """The opening words under a heading that says nothing on its own.

    A slide with no title is extracted as "Slide 12" and a PDF page as "Page 3".
    Shown only those, the agent could not tell what a deck was about, and left a
    whole forty-slide deck out of its plan. A few words of each such part fix
    that without sending the text itself, which the second pass does.
    """
    if not GENERIC_HEADING.match(heading_path[-1] if heading_path else ""):
        return ""
    words = " ".join(
        block.text for block in document.blocks_under(heading_path)
        if block.kind != BlockKind.HEADING
    ).split()
    if not words:
        return ""
    ellipsis = "…" if len(words) > PREVIEW_WORDS else ""
    return f' — "{" ".join(words[:PREVIEW_WORDS])}{ellipsis}"'


def resolve_source_ids(
    index: dict[str, SourceReference], source_ids: list[str]
) -> tuple[list[SourceReference], list[str]]:
    """The locations these ids stand for, and any ids that stand for nothing.

    References already covered by another in the same section -- a heading and
    each of its sub-headings, or a document and anything in it -- collapse to
    the covering one, so a section reads as the parts it really covers.
    """
    kept: list[SourceReference] = []
    unknown: list[str] = []
    for source_id in source_ids:
        reference = index.get(source_id.strip().lower())
        if reference is None:
            unknown.append(source_id)
        else:
            kept.append(reference)
    return _without_covered(kept), unknown


def _without_covered(references: list[SourceReference]) -> list[SourceReference]:
    unique: list[SourceReference] = []
    for reference in references:
        if reference not in unique:
            unique.append(reference)
    return [
        reference for reference in unique
        if not any(
            other is not reference
            and other.file_name == reference.file_name
            and len(other.heading_path) < len(reference.heading_path)
            and reference.heading_path[:len(other.heading_path)] == other.heading_path
            for other in unique
        )
    ]


def section_source_text(
    extraction: Extraction, references: list[SourceReference]
) -> tuple[str, bool]:
    """The full text of these locations, and whether it had to be cut."""
    parts = []
    for reference in references:
        document = extraction.document(reference.file_name)
        if document is None:
            continue
        parts.append(f"--- {reference.label} ---\n{document.text_under(reference.heading_path)}")
    text = "\n\n".join(parts)
    if len(text) > MAXIMUM_SECTION_SOURCE_CHARACTERS:
        return text[:MAXIMUM_SECTION_SOURCE_CHARACTERS], True
    return text, False


# --- the two passes -------------------------------------------------------------


def draft_plan(slug: str, instruction: str = "") -> dict[str, Any]:
    """Draft a plan from the whole extraction and keep it as a pending draft.

    Never touches the plan. Raises when nothing is extracted or no model is set
    up; a failure in one section's second pass is reported in the draft's notes
    and that section keeps what the outline gave it, rather than losing the rest.
    """
    project = require_project(slug)
    extraction = ExtractionStore(project.root).load()
    if not extraction.documents:
        raise OperationFailed(
            f"{project.name} has nothing extracted yet. Extract the source documents first; "
            f"a plan is drafted from what they say."
        )

    agent = resolve_agent(project, Stage.SCENE_PLAN)
    current_plan = PlanStore(project.root).load()
    audience = current_plan.selected_audience or "a general audience"
    notes: list[str] = []

    if extraction_freshness(project)["is_stale"]:
        notes.append(
            "The extraction is out of date with your files; this draft is based on what "
            "was last extracted."
        )

    outline_text, outline_notes, source_index = outline_for_agent(extraction)
    notes.extend(outline_notes)

    try:
        outline = _outline_pass(agent, audience, instruction, outline_text)
    except ModelNotConfigured as not_configured:
        raise OperationFailed(str(not_configured)) from not_configured
    except ModelCallFailed as call_failure:
        if "max_tokens" in str(call_failure):
            # Said in terms someone can act on, not as the library's exception.
            raise OperationFailed(
                "The outline was too long for one model response. Try guidance asking "
                "for fewer, broader sections, or leave some files out of extraction."
            ) from call_failure
        message = f"The model call failed while outlining. {call_failure}"
        raise OperationFailed(message) from call_failure

    objectives = [
        LearningObjective(text=text) for text in outline.learning_objectives if text.strip()
    ]

    sections: list[PlanSection] = []
    for proposed in outline.sections[:MAXIMUM_DRAFTED_SECTIONS]:
        references, unknown = resolve_source_ids(source_index, proposed.source_ids)
        if unknown:
            notes.append(
                f"\"{proposed.title}\": ignored {len(unknown)} source id(s) that are not in "
                f"the outline ({', '.join(unknown[:5])})."
            )
        sections.append(PlanSection(
            title=proposed.title,
            estimated_seconds=proposed.estimated_seconds,
            sources=references,
            objective_ids=[
                objectives[number - 1].id for number in proposed.objective_numbers
                if 1 <= number <= len(objectives)
            ],
        ))
    if len(outline.sections) > MAXIMUM_DRAFTED_SECTIONS:
        notes.append(
            f"The outline proposed {len(outline.sections)} sections; the first "
            f"{MAXIMUM_DRAFTED_SECTIONS} were kept."
        )

    _detail_pass(agent, audience, instruction, extraction, sections, objectives, notes)
    notes.extend(_uncovered_parts(extraction, sections))

    plan = Plan(
        sections=sections,
        learning_objectives=objectives,
        audience_choices=current_plan.audience_choices,
        selected_audience=current_plan.selected_audience,
        key_themes=[theme.strip() for theme in outline.key_themes if theme.strip()][:8],
    )

    PlanDraftStore(project.root).save({
        "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "instruction": instruction,
        "agent": agent.name,
        "agent_source": agent.source,
        "extraction_fingerprint": extraction.content_fingerprint(),
        "documents_read": [document.file_name for document in extraction.documents],
        "headings_read": sum(len(d.heading_outline()) for d in extraction.documents),
        "notes": notes,
        "accepted_section_ids": [],
        "plan": plan.model_dump(mode="json"),
    })
    return read_plan_draft(slug)


def _outline_pass(agent, audience: str, instruction: str, outline_text: str) -> DraftOutline:
    system_prompt = (
        f"{build_system_prompt(agent)}\n\n"
        f"---\nThis is the first of two passes: the OUTLINE only.\n"
        f"You are shown every heading of every source document, with how many words "
        f"sit under each. Group the parts into sections in teaching order. For each "
        f"section give a title saying what it teaches, the outline entries it covers "
        f"as their ids (d1 is a whole document; h12 is a heading and everything under "
        f"it -- prefer the highest heading that covers what you mean), a spoken "
        f"length estimated from those words at about {WORDS_PER_MINUTE_OF_NARRATION} "
        f"words a minute, and which learning objectives it serves.\n"
        f"Also give the learning objectives -- what a viewer should be able to do "
        f"afterwards -- and three to six key themes, all from the material only.\n"
        f"Cover every part that teaches something. Leave out title slides, contents "
        f"pages, reference lists and acknowledgements. Never invent a section for "
        f"material that is not listed. A later pass writes each section's summary "
        f"from its full text, so do not summarise here."
    )
    instruction_line = f"Instruction: {instruction.strip()}\n" if instruction.strip() else ""
    user_prompt = f"Audience: {audience}\n{instruction_line}\nSource outline:{outline_text}"
    return complete_structured(DraftOutline, system_prompt, user_prompt)


def _detail_pass(
    agent,
    audience: str,
    instruction: str,
    extraction: Extraction,
    sections: list[PlanSection],
    objectives: list[LearningObjective],
    notes: list[str],
) -> None:
    """Fill in each section from its own text, several at once."""
    system_prompt = (
        f"{build_system_prompt(agent)}\n\n"
        f"---\nThis is the second pass: ONE section, with the full text it covers.\n"
        f"Write a one- or two-sentence summary of what it teaches, from this text "
        f"only. Choose how it should be shown -- composition, plot, simulation, code "
        f"or still -- and give one sentence of why. Estimate how long a faithful "
        f"spoken treatment of this text takes, in seconds."
    )
    instruction_line = (
        f"Instruction for the whole plan: {instruction.strip()}\n" if instruction.strip() else ""
    )
    numbered_objectives = "\n".join(
        f"{number}. {objective.text}" for number, objective in enumerate(objectives, start=1)
    ) or "(none)"

    def detail(section: PlanSection) -> str | None:
        if not section.sources:
            return f"\"{section.title}\" has no source locations, so it was not detailed."
        text, was_cut = section_source_text(extraction, section.sources)
        user_prompt = (
            f"Audience: {audience}\n"
            f"{instruction_line}"
            f"Learning objectives of the plan:\n{numbered_objectives}\n\n"
            f"Section: {section.title}\n\n"
            f"Source text for this section:\n{text}"
        )
        try:
            result = complete_structured(SectionDetail, system_prompt, user_prompt)
        except (ModelCallFailed, ModelNotConfigured) as failure:
            logger.warning("section detail failed for %s: %s", section.title, failure)
            return f"\"{section.title}\" could not be detailed: {failure}"

        section.summary = result.summary
        section.rendering_approach = result.rendering_approach.value
        section.rendering_reason = result.rendering_reason
        section.estimated_seconds = result.estimated_seconds
        if was_cut:
            return (
                f"\"{section.title}\" covers more than "
                f"{MAXIMUM_SECTION_SOURCE_CHARACTERS:,} characters; its detail was written "
                f"from the first part. Consider splitting it."
            )
        return None

    if not sections:
        return
    workers = min(MAXIMUM_PARALLEL_SECTION_DRAFTS, len(sections))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for note in pool.map(detail, sections):
            if note:
                notes.append(note)

    # Validators run on construction, not on assignment: re-validate so a
    # clamped duration or an over-long reason is stored the way the plan expects.
    for index, section in enumerate(sections):
        sections[index] = PlanSection.model_validate(section.model_dump())


def _uncovered_parts(extraction: Extraction, sections: list[PlanSection]) -> list[str]:
    """Top-level parts no section points into -- said, so a gap is a choice."""
    covered = [
        (reference.file_name, reference.heading_path)
        for section in sections for reference in section.sources
    ]
    uncovered = []
    for document in extraction.documents:
        top_levels = {
            tuple(heading["heading_path"][:1])
            for heading in document.heading_outline() if heading["heading_path"]
        }
        for top in sorted(top_levels):
            is_covered = any(
                file_name == document.file_name
                and (list(top) == path[:1] or not path)
                for file_name, path in covered
            )
            if not is_covered:
                uncovered.append(f"{document.file_name} › {top[0]}")
    if not uncovered:
        return []
    shown = "; ".join(uncovered[:6]) + ("; …" if len(uncovered) > 6 else "")
    return [f"{len(uncovered)} part(s) of the source are not covered by any section: {shown}"]
