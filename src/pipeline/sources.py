"""Source-file admission — the single owner of "may this file enter a project?"

Every source document entering the system passes through
`store_uploaded_source_file`. Nothing else is permitted to decide whether an
upload is acceptable, so the answer cannot drift between the API, the CLI, and
any other entry.

Validation happens at the boundary, before a single byte is written, so a bad
upload fails at the point it arrives rather than several stages later inside an
extraction agent that has no idea where the file came from.

What this guards against, in order of severity:

1. **Path traversal.** `sources_dir / upload.filename` with a filename of
   `../../../ESCAPED.txt` writes outside the project entirely -- verified
   reproducible before this module existed. Filenames are reduced to a bare name
   and re-checked against the destination directory afterwards.
2. **Unbounded writes.** The upload is read fully into memory, so a large file is
   both a disk and a memory problem.
3. **Unsupported types.** The UI advertises PDF/MD/TXT/DOCX/PPTX; without a check
   the API accepts anything, and the failure surfaces much later as a confusing
   extraction error. The extension alone is not enough -- a PDF renamed to
   `.docx` passed it -- so the first bytes are checked against the format too.
4. **Silent replacement.** A second upload under a name already in the project
   replaces the first. That is how a corrected deck gets back in, so it is
   allowed, but it is reported: two different files can also sanitise to the
   same name, and the one that loses should never vanish unannounced.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from pipeline.storage.documents import new_identifier

SUPPORTED_SOURCE_FILE_SUFFIXES: frozenset[str] = frozenset(
    {".pdf", ".md", ".txt", ".docx", ".pptx"}
)

# A 50-slide deck with images and embedded media is routinely 100-300 MB, and
# a scanned PDF can be larger still. 64 MB refused ordinary course material.
MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES: int = 512 * 1024 * 1024  # 512 MB

# What one request may carry in total: several files can be dropped at once.
# Litestar's own default is 10 MB, which rejected a single real deck with
# "Request Entity Too Large" *before* any of the checks in this module ran --
# the size limit that mattered was one nobody here had chosen.
MAXIMUM_UPLOAD_REQUEST_SIZE_IN_BYTES: int = 2 * 1024 * 1024 * 1024  # 2 GB

# Streamed in blocks so a large file never sits in memory in full.
UPLOAD_CHUNK_SIZE_IN_BYTES: int = 1024 * 1024
MAXIMUM_SOURCE_FILE_NAME_LENGTH: int = 120

# Windows reserves these regardless of extension; a file named CON.txt cannot be
# created and the resulting OSError is opaque.
WINDOWS_RESERVED_FILE_STEMS: frozenset[str] = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{digit}" for digit in range(1, 10)}
    | {f"LPT{digit}" for digit in range(1, 10)}
)

# What each format's bytes open with. OOXML is a zip archive; a PDF header may
# sit after a little leading junk, which readers tolerate, so it is looked for
# within the first kilobyte rather than at offset 0.
_ZIP_SIGNATURE = b"PK\x03\x04"
_PDF_SIGNATURE = b"%PDF"
_PDF_HEADER_WINDOW = 1024
_BINARY_SIGNATURES = {".pdf": "a PDF", ".docx": "a Word document", ".pptx": "a PowerPoint deck"}

_UNSAFE_FILE_NAME_CHARACTERS = re.compile(r"[^A-Za-z0-9._ -]+")
_REPEATED_SEPARATORS = re.compile(r"[-_ ]{2,}")


class SourceFileRejected(ValueError):
    """Raised when an upload must not be written.

    Carries a message written for the person who uploaded the file, not for a log:
    it names the file and says what to do about it.
    """

    def __init__(self, original_file_name: str, reason: str) -> None:
        self.original_file_name = original_file_name
        self.reason = reason
        super().__init__(f"{original_file_name!r} was rejected: {reason}")


@dataclass(frozen=True)
class AcceptedSourceFile:
    """An upload that passed every check, with the name it will be stored under.

    `safe_file_name` may differ from `original_file_name` -- the caller should
    report both so a silently renamed file is never a surprise. `was_replaced`
    says a file of that name was already there and has been overwritten.
    """

    original_file_name: str
    safe_file_name: str
    size_in_bytes: int
    suffix: str
    was_replaced: bool = False

    @property
    def was_renamed(self) -> bool:
        return self.original_file_name != self.safe_file_name

    def to_dict(self) -> dict[str, Any]:
        """What the upload response reports for this file."""
        return {
            "file_name": self.safe_file_name,
            "original_file_name": self.original_file_name,
            "was_renamed": self.was_renamed,
            "was_replaced": self.was_replaced,
            "size_in_bytes": self.size_in_bytes,
        }


def reduce_to_bare_file_name(candidate_file_name: str) -> str:
    """Strip every directory component, from either path convention.

    A browser normally sends a bare name, but the multipart filename is entirely
    attacker-controlled and may contain POSIX separators, Windows separators, or
    both. `PurePosixPath` alone would treat `..\\..\\x.txt` as a single filename on
    Linux, so both conventions are applied.
    """
    without_null_bytes = candidate_file_name.replace("\x00", "")
    posix_name = PurePosixPath(without_null_bytes).name
    windows_name = PureWindowsPath(posix_name).name
    return windows_name


def sanitize_source_file_name(original_file_name: str) -> str:
    """Produce a filename safe to join onto a directory path.

    Deliberately conservative: unusual characters become underscores rather than
    being dropped, so two different uploads do not collapse into one name as
    easily.
    """
    bare_name = reduce_to_bare_file_name(original_file_name).strip()
    normalised = unicodedata.normalize("NFKC", bare_name)

    suffix = Path(normalised).suffix.lower()
    stem = Path(normalised).stem

    cleaned_stem = _UNSAFE_FILE_NAME_CHARACTERS.sub("_", stem).strip(" .")
    cleaned_stem = _REPEATED_SEPARATORS.sub(lambda m: m.group(0)[0], cleaned_stem)

    if not cleaned_stem:
        cleaned_stem = "source"
    if cleaned_stem.upper() in WINDOWS_RESERVED_FILE_STEMS:
        cleaned_stem = f"{cleaned_stem}_file"

    # Leave room for the suffix within the overall length budget.
    allowed_stem_length = MAXIMUM_SOURCE_FILE_NAME_LENGTH - len(suffix)
    cleaned_stem = cleaned_stem[:allowed_stem_length] or "source"

    return f"{cleaned_stem}{suffix}"


def check_source_file_name(
    original_file_name: str, destination_directory: Path
) -> str:
    """Everything that can be decided from the name alone, before any bytes.

    Split out so a 300 MB file with the wrong extension is refused immediately
    rather than after it has been read.
    """
    if not original_file_name or not original_file_name.strip():
        raise SourceFileRejected("(unnamed)", "the upload had no filename")

    safe_file_name = sanitize_source_file_name(original_file_name)
    suffix = Path(safe_file_name).suffix.lower()

    if suffix not in SUPPORTED_SOURCE_FILE_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_SOURCE_FILE_SUFFIXES))
        raise SourceFileRejected(
            original_file_name,
            f"{suffix or 'files without an extension'} is not supported. "
            f"Supported types: {supported}",
        )

    # Belt and braces: sanitisation should already have made traversal impossible,
    # but the destination is re-checked so a future change to the sanitiser cannot
    # silently reintroduce an arbitrary file write.
    resolved_destination = (destination_directory / safe_file_name).resolve()
    resolved_directory = destination_directory.resolve()
    if not resolved_destination.is_relative_to(resolved_directory):
        raise SourceFileRejected(
            original_file_name, "the filename resolves outside the project"
        )

    return safe_file_name


def describe_size_limit() -> str:
    return f"{MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES // (1024 * 1024)} MB"


def check_source_file_content(original_file_name: str, suffix: str, head: bytes) -> None:
    """Refuse a file whose first bytes contradict its extension.

    A PDF renamed to `.docx` passes every name check and then fails inside
    extraction, several stages and minutes later, with an error about zip
    archives -- the confusing failure this module exists to prevent, arriving by
    a different door. The signature is in the first chunk, so it costs nothing.
    """
    if suffix not in _BINARY_SIGNATURES:
        # Markdown and text are read as UTF-8; a NUL byte means a binary file
        # with a text extension, which would extract to noise.
        if b"\x00" in head:
            raise SourceFileRejected(
                original_file_name,
                f"the file is named {suffix} but is not plain text",
            )
        return

    if suffix == ".pdf":
        matches = _PDF_SIGNATURE in head[:_PDF_HEADER_WINDOW]
    else:
        matches = head.startswith(_ZIP_SIGNATURE)
    if not matches:
        raise SourceFileRejected(
            original_file_name,
            f"the file is named {suffix} but its contents are not "
            f"{_BINARY_SIGNATURES[suffix]}. Check it opens, then save it again "
            f"in that format.",
        )


async def store_uploaded_source_file(
    original_file_name: str,
    upload_stream: Any,
    destination_directory: Path,
) -> AcceptedSourceFile:
    """Stream an upload to disk, enforcing the size cap as it goes.

    Reading a whole file into memory to measure it means a 300 MB deck costs
    300 MB of RAM before a single byte is written, and several at once multiply
    that. Here the file is copied in blocks and abandoned the moment it crosses
    the limit -- so an oversized upload costs the limit, not the file.

    Written to a temporary name and renamed once complete, so an interrupted
    upload never leaves a half-file sitting in `sources/` looking like a real
    document.
    """
    safe_file_name = check_source_file_name(original_file_name, destination_directory)
    destination_directory.mkdir(parents=True, exist_ok=True)

    suffix = Path(safe_file_name).suffix.lower()
    final_path = destination_directory / safe_file_name
    temporary_path = final_path.with_name(f"{safe_file_name}.{new_identifier()}.part")

    bytes_written = 0
    try:
        with temporary_path.open("wb") as destination:
            while True:
                chunk = await upload_stream.read(UPLOAD_CHUNK_SIZE_IN_BYTES)
                if not chunk:
                    break
                if not bytes_written:
                    check_source_file_content(original_file_name, suffix, chunk)
                bytes_written += len(chunk)
                if bytes_written > MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES:
                    raise SourceFileRejected(
                        original_file_name,
                        f"the file is larger than the {describe_size_limit()} limit",
                    )
                destination.write(chunk)

        if bytes_written == 0:
            raise SourceFileRejected(original_file_name, "the file is empty")

        was_replaced = final_path.exists()
        temporary_path.replace(final_path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise

    return AcceptedSourceFile(
        original_file_name=original_file_name,
        safe_file_name=safe_file_name,
        size_in_bytes=bytes_written,
        suffix=suffix,
        was_replaced=was_replaced,
    )
