"""Where the pictures pulled out of a document are stored.

Kept apart from the readers: storage is the one side effect extraction has, and
the readers stay pure functions of their file when no sink is given.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

# Extracted figures are a copy of the pictures inside the source files, so a
# picture-heavy deck can approach the size of the deck itself. This is a ceiling
# against the pathological case -- a folder of large decks quietly filling the
# disk -- not a target; normal documents land far below it.
MAXIMUM_EXTRACTED_ASSET_BYTES = 512 * 1024 * 1024


class AssetSink:
    """Somewhere to put the images pulled out of a document.

    Content-addressed by digest, so a logo repeated on forty slides is stored
    once rather than forty times -- which on a real 80 MB deck is the difference
    between a few megabytes of assets and most of the deck copied out again.

    Passed in rather than derived inside the readers so a reader stays a pure
    function of its file when nobody wants the images: `read_docx(path)` with no
    sink extracts text and writes nothing, which is what the tests and the
    preview path want.
    """

    def __init__(self, directory: Path, relative_to: Path | None = None) -> None:
        self.directory = directory
        self.relative_to = relative_to
        self.written: dict[str, str] = {}
        self.bytes_written = 0
        self.skipped_for_size = 0

    def store(self, blob: bytes, suffix: str) -> str:
        digest = hashlib.sha256(blob).hexdigest()[:16]
        if digest in self.written:
            return self.written[digest]

        if self.bytes_written + len(blob) > MAXIMUM_EXTRACTED_ASSET_BYTES:
            # Reported rather than raised: losing the last few figures of a very
            # large deck is a much smaller problem than failing the extraction
            # and keeping none of its text.
            self.skipped_for_size += 1
            return ""

        self.directory.mkdir(parents=True, exist_ok=True)
        destination = self.directory / f"{digest}{suffix.lower()}"
        if not destination.exists():
            destination.write_bytes(blob)

        stored = str(
            destination.relative_to(self.relative_to) if self.relative_to else destination
        ).replace("\\", "/")
        self.written[digest] = stored
        self.bytes_written += len(blob)
        return stored

    def prune_unreferenced(self, referenced: set[str]) -> int:
        """Delete stored figures nothing refers to. Returns how many went.

        `referenced` is every asset path still in use -- by the collection and by
        the confirmed extraction, since one file is extracted at a time and the
        others' figures must survive it. Called only after the new extraction is
        safely saved. Without it, removing a picture-heavy deck from a project
        left most of its size behind in `extraction/assets/` for good.
        """
        if not self.directory.exists():
            return 0
        kept = {Path(stored).name for stored in referenced}
        removed = 0
        for candidate in self.directory.iterdir():
            if candidate.is_file() and candidate.name not in kept:
                candidate.unlink()
                removed += 1
        return removed
