"""Reviewing what extraction produced, and doing something about it.

Extraction is parsing, and parsing fails quietly: a picture comes out blank, a
diagram is stored as a 3-pixel rule, a chapter says "as Figure 2.1 shows" and no
figure was saved anywhere near it. Nothing downstream can tell -- the planner
sees a figure block, the renderer shows an empty rectangle, and the first person
to notice is whoever watches the finished video.

Two passes, in this order and deliberately separate:

1. **Checks.** Every extracted picture is opened and measured. Missing, corrupt,
   blank, tiny and hairline images are facts, not opinions, and they are found
   without a model, without a network, and identically every run.
2. **The Extraction agent.** What is left is a reading problem: a reference to a
   figure that was never extracted, a section that stops mid-sentence, text that
   came out garbled. That needs a reader, so the stage's own agent gets the
   extracted text, the figure inventory and the findings from pass 1.

A finding is a claim about a place in a document, so it carries that place. What
can be done about it lives here too: replace the picture with one you upload, or
say it is fine and stop being told.

Stored at `projects/<slug>/extraction/review.json`.
"""

from __future__ import annotations

import logging
import re
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

from pipeline.extraction import BlockKind, Extraction, ExtractionStore
from pipeline.storage.documents import JsonDocumentStore, new_identifier

logger = logging.getLogger(__name__)

# A picture smaller than this in either direction is a bullet, a rule or a
# spacer, not a diagram anyone meant to show.
SMALLEST_USEFUL_PIXELS = 32

# Wider than this against its height (or the reverse) and it is a divider line.
EXTREME_ASPECT_RATIO = 20

# How close to a single flat colour an image has to be before it is called
# blank. Measured on the greyscale range, so a white box with a faint watermark
# is still reported.
BLANK_TONAL_RANGE = 8

MAXIMUM_FINDINGS = 200
MAXIMUM_EXTRACTION_CHARACTERS_FOR_REVIEW = 40_000
MAXIMUM_FIGURES_LISTED_FOR_AGENT = 120

# "as Figure 2.1 shows", "see Fig. 4" -- a promise that a picture exists.
FIGURE_REFERENCE = re.compile(r"\b(?:fig|figure)s?\.?\s*(\d+(?:\.\d+)?)", re.IGNORECASE)


class FindingKind:
    PICTURE_MISSING = "picture_missing"
    PICTURE_UNREADABLE = "picture_unreadable"
    PICTURE_BLANK = "picture_blank"
    PICTURE_TINY = "picture_tiny"
    PICTURE_NOT_SAVED = "picture_not_saved"
    REFERENCE_WITHOUT_FIGURE = "reference_without_figure"
    EMPTY_DOCUMENT = "empty_document"
    READING_PROBLEM = "reading_problem"


class Finding(BaseModel):
    """Something wrong with what was extracted, and where it is.

    `block_id` is what makes a finding actionable rather than informative: it is
    the difference between "a figure is broken somewhere in chapter 2" and a
    button that replaces *this* picture.
    """

    id: str = Field(default_factory=new_identifier)
    kind: str = FindingKind.READING_PROBLEM
    severity: str = "warning"            # error | warning | note
    file_name: str = ""
    heading_path: list[str] = Field(default_factory=list)
    block_id: str = ""
    asset_path: str = ""
    what: str = ""
    suggestion: str = ""
    found_by: str = "checks"             # checks | agent

    @property
    def where(self) -> str:
        return " › ".join([self.file_name, *self.heading_path]) or self.file_name

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump() | {"where": self.where}


class ExtractionReview(BaseModel):
    reviewed_at: str = ""
    # What was reviewed. A review of an extraction that has since been re-run is
    # stale, and saying so is better than showing findings about content that no
    # longer exists.
    content_fingerprint: str = ""
    asked_the_agent: bool = False
    findings: list[Finding] = Field(default_factory=list)
    acknowledged: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @field_validator("findings")
    @classmethod
    def _cap_findings(cls, value: list[Finding]) -> list[Finding]:
        return value[:MAXIMUM_FINDINGS]

    def open_findings(self) -> list[Finding]:
        return [f for f in self.findings if f.id not in set(self.acknowledged)]

    def to_dict(self, extraction: Extraction | None = None) -> dict[str, Any]:
        acknowledged = set(self.acknowledged)
        stale = bool(
            extraction is not None
            and self.content_fingerprint
            and extraction.content_fingerprint() != self.content_fingerprint
        )
        open_findings = [f for f in self.findings if f.id not in acknowledged]
        return {
            "reviewed_at": self.reviewed_at,
            "asked_the_agent": self.asked_the_agent,
            "is_stale": stale,
            "notes": self.notes,
            "open_count": len(open_findings),
            "error_count": sum(1 for f in open_findings if f.severity == "error"),
            "findings": [
                f.to_dict() | {"acknowledged": f.id in acknowledged} for f in self.findings
            ],
        }


def default_extraction_review() -> ExtractionReview:
    return ExtractionReview()


class ExtractionReviewStore(JsonDocumentStore[ExtractionReview]):
    """Persistence for the extraction review, beside the content it is about."""

    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=project_root / "extraction" / "review.json",
            model_type=ExtractionReview,
            build_default=default_extraction_review,
            description="extraction review",
        )


# --- pass one: the pictures themselves ----------------------------------------------


def _describe_picture(path: Path) -> dict[str, Any]:
    """Open a stored picture and measure it. Never raises.

    A corrupt file is exactly what this is looking for, so a failure to read one
    is a result rather than an error.
    """
    from PIL import Image, ImageStat

    try:
        with Image.open(path) as picture:
            picture.load()
            width, height = picture.size
            greyscale = picture.convert("L")
            extrema = ImageStat.Stat(greyscale).extrema[0]
    except Exception as unreadable:      # Pillow raises a wide variety here
        return {"readable": False, "why": f"{type(unreadable).__name__}: {unreadable}"}

    return {
        "readable": True,
        "width": width,
        "height": height,
        "tonal_range": extrema[1] - extrema[0],
    }


def inspect_pictures(project_root: Path, extraction: Extraction) -> list[Finding]:
    """Every extracted picture, opened and measured."""
    findings: list[Finding] = []

    for document in extraction.documents:
        for block in document.blocks:
            if block.kind != BlockKind.FIGURE:
                continue

            common = {
                "file_name": document.file_name,
                "heading_path": list(block.heading_path),
                "block_id": block.id,
                "asset_path": block.asset_path,
            }

            if not block.asset_path:
                findings.append(Finding(
                    kind=FindingKind.PICTURE_NOT_SAVED, severity="warning", **common,
                    what=f"{block.text or 'A figure'} is recorded, but no picture was saved.",
                    suggestion="Switch on Extract images and run extraction again, or "
                               "upload the picture yourself.",
                ))
                continue

            path = project_root / block.asset_path
            if not path.exists():
                findings.append(Finding(
                    kind=FindingKind.PICTURE_MISSING, severity="error", **common,
                    what=f"The file for {block.text or 'this figure'} is not on disk.",
                    suggestion="Run extraction again, or upload a replacement.",
                ))
                continue

            measured = _describe_picture(path)
            if not measured["readable"]:
                findings.append(Finding(
                    kind=FindingKind.PICTURE_UNREADABLE, severity="error", **common,
                    what=f"{block.text or 'This figure'} is not a readable image "
                         f"({measured['why']}).",
                    suggestion="Upload a replacement, or take a screenshot of it "
                               "from the source document.",
                ))
                continue

            width, height = measured["width"], measured["height"]
            if width < SMALLEST_USEFUL_PIXELS or height < SMALLEST_USEFUL_PIXELS:
                findings.append(Finding(
                    kind=FindingKind.PICTURE_TINY, severity="note", **common,
                    what=f"{block.text or 'This figure'} is only {width}×{height} pixels — "
                         f"probably a bullet or a rule rather than a diagram.",
                    suggestion="Ignore it if it is decoration; upload the real picture "
                               "if a diagram was meant to be here.",
                ))
                continue

            longest, shortest = max(width, height), min(width, height)
            if shortest and longest / shortest > EXTREME_ASPECT_RATIO:
                findings.append(Finding(
                    kind=FindingKind.PICTURE_TINY, severity="note", **common,
                    what=f"{block.text or 'This figure'} is {width}×{height} — a line, "
                         f"by its proportions.",
                    suggestion="Ignore it if it is a divider.",
                ))
                continue

            if measured["tonal_range"] <= BLANK_TONAL_RANGE:
                findings.append(Finding(
                    kind=FindingKind.PICTURE_BLANK, severity="error", **common,
                    what=f"{block.text or 'This figure'} came out blank — "
                         f"{width}×{height} of a single flat colour.",
                    suggestion="Upload a replacement: a blank picture in the video is "
                               "worse than no picture.",
                ))

    return findings


def check_references(extraction: Extraction) -> list[Finding]:
    """Text that promises a figure the extraction does not have.

    Scoped per document: "Figure 2.1" in a chapter with no extracted figures at
    all is a strong signal, while the same phrase in a document full of figures
    usually just refers to one of them.
    """
    findings: list[Finding] = []

    for document in extraction.documents:
        figures = [b for b in document.blocks if b.kind == BlockKind.FIGURE]
        if figures:
            continue

        referenced: dict[str, Any] = {}
        for block in document.blocks:
            if block.kind == BlockKind.FIGURE:
                continue
            for number in FIGURE_REFERENCE.findall(block.text):
                referenced.setdefault(number, block)

        for number, block in sorted(referenced.items())[:10]:
            findings.append(Finding(
                kind=FindingKind.REFERENCE_WITHOUT_FIGURE, severity="warning",
                file_name=document.file_name, heading_path=list(block.heading_path),
                block_id=block.id,
                what=f"The text refers to Figure {number}, but no figure was extracted "
                     f"from this document at all.",
                suggestion="Check whether the figures are images the reader could not "
                           "open, and upload them if the video needs them.",
            ))

    for document in extraction.documents:
        if not document.blocks:
            findings.append(Finding(
                kind=FindingKind.EMPTY_DOCUMENT, severity="error",
                file_name=document.file_name,
                what="Nothing was extracted from this document.",
                suggestion="It may be a scanned file with no text layer. "
                           "Check it on Inputs.",
            ))

    return findings


def run_checks(project_root: Path, extraction: Extraction) -> list[Finding]:
    """Everything findable without a model."""
    return inspect_pictures(project_root, extraction) + check_references(extraction)


# --- pass two: the stage's own agent ------------------------------------------------


class AgentFinding(BaseModel):
    file_name: str = Field(default="", description="The document the problem is in.")
    heading: str = Field(
        default="", description="The heading it is under, copied exactly from the text."
    )
    what: str = Field(description="What is wrong, in one sentence.")
    suggestion: str = Field(default="", description="What the person should do about it.")
    severity: str = Field(
        default="warning", description="error, warning or note."
    )


class ExtractionReviewReport(BaseModel):
    findings: list[AgentFinding] = Field(
        default_factory=list,
        description="Problems in what was extracted. Empty if the extraction reads cleanly.",
    )
    notes: list[str] = Field(
        default_factory=list, description="Anything worth saying that is not a problem."
    )


def _figure_inventory(project_root: Path, extraction: Extraction) -> str:
    """What pictures exist, with their measurements, for the agent to reason about."""
    lines: list[str] = []
    for document in extraction.documents:
        for block in document.blocks:
            if block.kind != BlockKind.FIGURE or len(lines) >= MAXIMUM_FIGURES_LISTED_FOR_AGENT:
                continue
            location = " › ".join(block.heading_path) or "(no heading)"
            if not block.asset_path:
                lines.append(f"- {block.text or 'figure'} [{location}] — no picture saved")
                continue
            measured = _describe_picture(project_root / block.asset_path)
            size = (f"{measured['width']}×{measured['height']}"
                    if measured["readable"] else "unreadable")
            lines.append(f"- {block.text or 'figure'} [{location}] — {size}")
    return "\n".join(lines) or "(no figures were extracted)"


def ask_the_agent(
    project, extraction: Extraction, found: list[Finding]
) -> ExtractionReviewReport:
    """Have the Extraction agent read what was extracted and say what is wrong."""
    from pipeline.agent_runtime import build_system_prompt, resolve_agent
    from pipeline.llm import complete_structured
    from pipeline.stages import Stage

    agent = resolve_agent(project, Stage.EXTRACTION)
    system_prompt = build_system_prompt(agent) + (
        "\n\nYou are reviewing an extraction you have already produced. Report only "
        "problems you can point at in the text below: a section that stops "
        "mid-sentence, words that came out garbled or run together, a table that "
        "lost its shape, a reference to a figure or appendix that is not here, "
        "content that is obviously missing. Quote the heading each problem is "
        "under, exactly as it appears. Do not summarise the content, do not "
        "suggest improvements to the source material, and report nothing you "
        "cannot point at."
    )

    already = "\n".join(f"- {finding.where}: {finding.what}" for finding in found)
    user_prompt = "\n\n".join(part for part in [
        f"--- figures extracted ---\n{_figure_inventory(project.root, extraction)}",
        f"--- problems already found by the automatic checks ---\n{already}"
        if already else "",
        f"--- the extracted content ---\n"
        f"{extraction.as_markdown()[:MAXIMUM_EXTRACTION_CHARACTERS_FOR_REVIEW]}",
    ] if part)

    return complete_structured(ExtractionReviewReport, system_prompt, user_prompt)


def _heading_path_for(extraction: Extraction, file_name: str, heading: str) -> list[str]:
    """Turn the agent's quoted heading back into a real location.

    The agent answers with a heading it read; a finding needs the path the rest
    of the pipeline uses. An unmatched heading is not discarded -- the finding is
    still true, it just points at the document.
    """
    wanted = heading.strip().lower()
    if not wanted:
        return []
    for document in extraction.documents:
        if file_name and document.file_name != file_name:
            continue
        for block in document.blocks:
            if block.kind == BlockKind.HEADING and block.text.strip().lower() == wanted:
                return list(block.heading_path)
    return []


# --- what a client calls ------------------------------------------------------------


def review_extraction(slug: str, ask_agent: bool = True) -> dict[str, Any]:
    """Check the extraction, optionally have its agent read it, and save the result.

    The checks always run. The agent is best-effort: a review that reported
    nothing because the model was unreachable would be worse than one that
    reports the broken pictures and says the reading pass did not happen.
    """
    from pipeline.llm import ModelCallFailed, ModelNotConfigured
    from pipeline.operations import OperationFailed, require_project

    project = require_project(slug)
    extraction = ExtractionStore(project.root).load()
    if not extraction.documents:
        raise OperationFailed(
            f"{project.name} has nothing extracted yet. Run extraction first."
        )

    findings = run_checks(project.root, extraction)
    notes: list[str] = []
    asked = False

    if ask_agent:
        try:
            report = ask_the_agent(project, extraction, findings)
            asked = True
            notes.extend(report.notes)
            for found in report.findings:
                findings.append(Finding(
                    kind=FindingKind.READING_PROBLEM,
                    severity=found.severity if found.severity in
                    {"error", "warning", "note"} else "warning",
                    file_name=found.file_name,
                    heading_path=_heading_path_for(
                        extraction, found.file_name, found.heading),
                    what=found.what,
                    suggestion=found.suggestion,
                    found_by="agent",
                ))
        except ModelNotConfigured as not_configured:
            notes.append(f"The agent did not read it: {not_configured}")
        except ModelCallFailed as call_failure:
            logger.warning("the extraction agent could not review: %s", call_failure)
            notes.append(f"The agent did not read it: {call_failure}")

    store = ExtractionReviewStore(project.root)
    previous = store.load()
    # Acknowledgements survive a re-review by what they were about, not by id:
    # every run makes new ids, and forgetting them would re-raise everything the
    # person has already looked at and dismissed.
    dismissed = {
        (f.kind, f.block_id, f.what) for f in previous.findings
        if f.id in set(previous.acknowledged)
    }
    acknowledged = [
        f.id for f in findings if (f.kind, f.block_id, f.what) in dismissed
    ]

    saved = store.save(ExtractionReview(
        reviewed_at=datetime.now(UTC).isoformat(timespec="seconds"),
        content_fingerprint=extraction.content_fingerprint(),
        asked_the_agent=asked,
        findings=findings,
        acknowledged=acknowledged,
        notes=notes,
    ))
    return saved.to_dict(extraction)


def read_extraction_review(slug: str) -> dict[str, Any]:
    """The last review, or an empty one. Says whether it is out of date."""
    from pipeline.operations import require_project

    project = require_project(slug)
    extraction = ExtractionStore(project.root).load()
    return ExtractionReviewStore(project.root).load().to_dict(extraction)


def acknowledge_finding(slug: str, finding_id: str) -> dict[str, Any]:
    """Mark one finding as looked at, so it stops being reported."""
    from pipeline.operations import OperationFailed, require_project

    project = require_project(slug)
    store = ExtractionReviewStore(project.root)
    review = store.load()
    if not any(finding.id == finding_id for finding in review.findings):
        raise OperationFailed(f"This review has no finding {finding_id!r}.")

    if finding_id not in review.acknowledged:
        review.acknowledged = [*review.acknowledged, finding_id]
    saved = store.save(review)
    return saved.to_dict(ExtractionStore(project.root).load())


def replace_figure(slug: str, block_id: str, image_bytes: bytes, suffix: str) -> dict[str, Any]:
    """Put a picture you supply where the extracted one should have been.

    The extraction itself is edited, because that is what every later stage
    reads. The replacement is stored like any other asset, so it is pruned and
    addressed the same way -- and it survives until the next extraction run,
    which will overwrite it from the source. That is stated in the result rather
    than hidden.
    """
    from pipeline.extraction import AssetSink
    from pipeline.operations import OperationFailed, present_artifact, require_project

    project = require_project(slug)
    store = ExtractionStore(project.root)
    extraction = store.load()

    target = None
    for document in extraction.documents:
        for block in document.blocks:
            if block.id == block_id:
                target = block
                break
    if target is None:
        raise OperationFailed(f"This extraction has no block {block_id!r}.")
    if target.kind != BlockKind.FIGURE:
        raise OperationFailed(f"Block {block_id!r} is a {target.kind}, not a figure.")

    if not image_bytes:
        raise OperationFailed("That file is empty.")

    # Checked before it is stored: accepting a file that cannot be opened would
    # replace one broken picture with another and report success.
    from PIL import Image

    try:
        with Image.open(BytesIO(image_bytes)) as picture:
            picture.verify()
    except Exception as unreadable:
        raise OperationFailed(
            f"That file is not an image the pipeline can read "
            f"({type(unreadable).__name__})."
        ) from unreadable

    sink = AssetSink(project.root / "extraction" / "assets", relative_to=project.root)
    stored = sink.store(image_bytes, suffix if suffix.startswith(".") else f".{suffix}")
    if not stored:
        raise OperationFailed("The picture could not be stored.")

    target.asset_path = stored
    saved = store.save(extraction)

    return present_artifact(project, "extraction", saved) | {
        "block_id": block_id,
        "asset_path": stored,
        "note": "Running extraction again will replace this picture with the "
                "one in the source document.",
    }
