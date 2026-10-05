"""Reviewing what extraction produced, and doing something about it.

Extraction is parsing, and parsing fails quietly: a picture comes out blank, a
diagram is stored as a 3-pixel rule, a chapter says "as Figure 2.1 shows" and no
figure was saved anywhere near it. Nothing downstream can tell -- the planner
sees a figure block, the renderer shows an empty rectangle, and the first person
to notice is whoever watches the finished video.

The checks here need no model: every extracted picture is opened and
measured, and every "see Figure 2.1" is matched to a figure. Missing, corrupt,
blank, tiny and hairline images are facts, not opinions, found identically
every run. Reading problems -- text in the wrong order, a garbled line, a
figure that is the wrong picture -- are the Extraction agent's, one slide at a
time with the slide in view (`extraction_slide_review`). It once read the
whole extraction in one reply, which ran out of room on any real deck.

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

from pipeline.config import get_settings
from pipeline.extraction import BlockKind, Extraction, ExtractionCollectionStore
from pipeline.figure_pictures import picture_context, picture_prompt, set_picture, store_picture
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

    By count, not all-or-nothing: skipping any document that extracted even one
    figure missed the case that actually happens -- a chapter of sixty that lost
    figure 63. A reference numbered past the figures there are catches both.
    """
    findings: list[Finding] = []

    for document in extraction.documents:
        if not document.blocks:
            findings.append(Finding(
                kind=FindingKind.EMPTY_DOCUMENT, severity="error",
                file_name=document.file_name,
                what="Nothing was extracted from this document.",
                suggestion="It may be a scanned file with no text layer. "
                           "Check it on Inputs.",
            ))
            continue

        figures = sum(1 for b in document.blocks if b.kind == BlockKind.FIGURE)
        referenced: dict[str, Any] = {}
        for block in document.blocks:
            if block.kind == BlockKind.FIGURE:
                continue
            # "2.1" is figure 1 of chapter 2: numbering restarts, so the tail counts.
            for number in FIGURE_REFERENCE.findall(block.text):
                if int(number.rsplit(".", 1)[-1]) > figures:
                    referenced.setdefault(number, block)

        for number, block in sorted(referenced.items())[:10]:
            findings.append(Finding(
                kind=FindingKind.REFERENCE_WITHOUT_FIGURE, severity="warning",
                file_name=document.file_name, heading_path=list(block.heading_path),
                block_id=block.id,
                what=f"The text refers to Figure {number}, but {figures} figure(s) "
                     f"were extracted from this document.",
                suggestion="Check whether the figures are images the reader could not "
                           "open, and upload them if the video needs them.",
            ))

    return findings


def run_checks(project_root: Path, extraction: Extraction) -> list[Finding]:
    """Everything findable without a model."""
    return inspect_pictures(project_root, extraction) + check_references(extraction)


# --- what a client calls ------------------------------------------------------------


def review_extraction(slug: str) -> dict[str, Any]:
    """Run the checks over the extraction, and save what they found."""
    from pipeline.operations import OperationFailed, require_project

    project = require_project(slug)
    extraction = ExtractionCollectionStore(project.root).load()
    if not extraction.documents:
        raise OperationFailed(
            f"{project.name} has nothing in its extraction collection yet. Extract a file first."
        )

    findings = run_checks(project.root, extraction)

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
        findings=findings,
        acknowledged=acknowledged,
    ))
    return saved.to_dict(extraction)


def read_extraction_review(slug: str) -> dict[str, Any]:
    """The last review, or an empty one. Says whether it is out of date."""
    from pipeline.operations import require_project

    project = require_project(slug)
    extraction = ExtractionCollectionStore(project.root).load()
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
    return saved.to_dict(ExtractionCollectionStore(project.root).load())


def _find_figure(extraction: Extraction, block_id: str):
    """The document a block is in, and the block."""
    from pipeline.operations import OperationFailed

    for document in extraction.documents:
        for block in document.blocks:
            if block.id == block_id:
                return document, block
    raise OperationFailed(f"This extraction has no block {block_id!r}.")


def replace_figure(
    slug: str, block_id: str, image_bytes: bytes, suffix: str, origin: str = "uploaded"
) -> dict[str, Any]:
    """Put a picture you supply where the extracted one should have been.

    The collection is edited, and later stages get the picture when it is next
    confirmed. The replacement is stored like any other asset, so it is pruned
    and addressed the same way -- and it survives until that file is extracted
    again, which overwrites it from the source. That is stated in the result
    rather than hidden.
    """
    from pipeline.operations import OperationFailed, present_artifact, require_project

    project = require_project(slug)
    store = ExtractionCollectionStore(project.root)
    extraction = store.load()

    document, target = _find_figure(extraction, block_id)
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

    stored = store_picture(project, image_bytes, suffix)
    # The figure and its place on the slide: one picture, recorded in both.
    set_picture(document, target, stored, origin)
    # Saving marks the collection changed: later stages get the picture on the
    # next transfer.
    saved = store.save(extraction)

    return present_artifact(project, "extraction", saved) | {
        "block_id": block_id,
        "asset_path": stored,
        "asset_origin": origin,
        "note": "Transfer again to hand this picture on; re-extracting replaces it.",
    }


# --- drawing a replacement ----------------------------------------------------------

def describe_figure_for_drawing(slug: str, block_id: str) -> dict[str, Any]:
    """What would be drawn, and from what, without drawing it.

    So the prompt can be shown before it is sent: a picture that will be stated
    as part of the source material should not be produced by a prompt nobody
    saw.
    """
    from pipeline.operations import OperationFailed, require_project

    project = require_project(slug)
    extraction = ExtractionCollectionStore(project.root).load()
    for document in extraction.documents:
        for block in document.blocks:
            if block.id == block_id:
                return {
                    "block_id": block_id,
                    "caption": block.text,
                    "file_name": document.file_name,
                    "heading_path": list(block.heading_path),
                    "context": picture_context(document, block),
                    "model": get_settings().image_llm[2],
                }
    raise OperationFailed(f"This extraction has no block {block_id!r}.")


def generate_figure(slug: str, block_id: str, instruction: str = "") -> dict[str, Any]:
    """Draw a replacement for a figure that did not extract, and put it in place.

    Recorded as generated, not quietly swapped in. Everything else in this
    pipeline comes from the source documents; a drawn picture is the one thing
    that does not, and the stage that shows it has to be able to say so.
    """
    from pipeline.llm import ModelCallFailed, ModelNotConfigured
    from pipeline.operations import OperationFailed, require_project

    described = describe_figure_for_drawing(slug, block_id)
    document, block = _find_figure(ExtractionCollectionStore(
        require_project(slug).root).load(), block_id)
    prompt = picture_prompt(
        document, block, described["caption"] or "an unnamed figure", instruction)

    from pipeline.llm import draw_image

    try:
        drawn = draw_image(prompt)
    except ModelNotConfigured as not_configured:
        raise OperationFailed(str(not_configured)) from not_configured
    except ModelCallFailed as call_failure:
        raise OperationFailed(f"The picture could not be drawn. {call_failure}") from call_failure

    saved = replace_figure(slug, block_id, drawn, ".png", origin="generated")
    return saved | {"prompt": prompt, "model": described["model"]}
