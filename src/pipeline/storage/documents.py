"""Durable JSON document persistence — one implementation, one behaviour.

Four stage artifacts (plan, script, composition, review) plus project metadata and
stage settings all need the same three properties:

1. **Atomic writes.** Temp file then rename, so an interrupted write never leaves a
   truncated file that the reader then rejects — which surfaces as the document
   silently vanishing from the UI.
2. **Never destructive on a bad parse.** A corrupt file may hold hours of someone's
   writing. Return a default so the UI still renders, log loudly so the operator
   knows, and leave the file exactly where it is for manual recovery.
3. **Validation on read.** The stored shape is coerced through the model, so a file
   hand-edited or written by an older version cannot reach the rest of the system
   as an unexpected shape.

Before this module those three behaviours were reimplemented six times. They agreed
today only because they were written in one sitting; the next one added under time
pressure would have been the odd one out, and the divergence would be invisible
until something went wrong.
"""

from __future__ import annotations

import json
import logging
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

logger = logging.getLogger(__name__)

DocumentModel = TypeVar("DocumentModel", bound=BaseModel)

TEMPORARY_WRITE_SUFFIX = ".tmp"


def new_identifier() -> str:
    """Stable short id for list items.

    Twelve hex characters: enough that a collision within one document is not a
    practical concern, short enough to read in a JSON file while debugging.

    Items need ids at all so reordering, editing and deleting address the right row
    even while titles are duplicated or blank mid-edit.
    """
    return uuid.uuid4().hex[:12]


def write_text_atomically(destination_path: Path, text: str) -> None:
    """Write via a temporary file and rename.

    The rename is what makes it atomic: a reader either sees the whole previous
    file or the whole new one, never a half-written middle.
    """
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = destination_path.with_name(
        destination_path.name + TEMPORARY_WRITE_SUFFIX)
    temporary_path.write_text(text, encoding="utf-8")
    temporary_path.replace(destination_path)


def read_json_object(source_path: Path, description: str) -> dict | None:
    """Read a JSON object, or None if it cannot be used.

    Distinguishes three cases deliberately:

    - **missing** — silent. "Not created yet" is a normal state, not an error.
    - **unreadable or malformed** — logged at ERROR. The caller falls back to a
      default, and without a log the operator would only see settings that keep
      reverting for no visible reason.
    - **valid JSON but not an object** — also logged. A bare list or string would
      otherwise fail much later inside model validation, far from the file that
      caused it.
    """
    if not source_path.exists():
        return None

    try:
        parsed = json.loads(source_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as unreadable:
        logger.error(
            "%s at %s is unreadable (%s); using defaults and leaving the file "
            "untouched for recovery", description, source_path, unreadable,
        )
        return None

    if not isinstance(parsed, dict):
        logger.error(
            "%s at %s is valid JSON but not an object; using defaults",
            description, source_path,
        )
        return None

    return parsed


class JsonDocumentStore[DocumentModel: BaseModel]:
    """Loads and saves one validated document at one path.

    Generic over the model so each stage keeps its own typed artifact while sharing
    the durability behaviour. A stage that needs different persistence should say so
    explicitly rather than quietly reimplementing this.
    """

    def __init__(
        self,
        document_path: Path,
        model_type: type[DocumentModel],
        build_default: Callable[[], DocumentModel],
        description: str,
    ) -> None:
        self.document_path = document_path
        self.model_type = model_type
        self.build_default = build_default
        self.description = description

    def load(self) -> DocumentModel:
        raw_document = read_json_object(self.document_path, self.description)
        if raw_document is None:
            return self.build_default()

        try:
            return self.model_type.model_validate(raw_document)
        except ValueError as invalid_shape:
            # The file parsed as JSON but does not fit the model -- typically an
            # older schema or a hand edit. Same rule as an unreadable file: never
            # overwrite, always report.
            logger.error(
                "%s at %s does not match its expected shape (%s); using defaults "
                "and leaving the file untouched for recovery",
                self.description, self.document_path, invalid_shape,
            )
            return self.build_default()

    def save(self, document: DocumentModel) -> DocumentModel:
        write_text_atomically(self.document_path, document.model_dump_json(indent=2))
        return document
