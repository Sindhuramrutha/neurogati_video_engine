"""Source-file admission — the single owner of "may this file enter a project?"

Every source document entering the system passes through
`validate_uploaded_source_file`. Nothing else is permitted to decide whether an
upload is acceptable, so the answer cannot drift between the API, the CLI, and a
future importer.

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
   extraction error.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath

SUPPORTED_SOURCE_FILE_SUFFIXES: frozenset[str] = frozenset(
    {".pdf", ".md", ".txt", ".docx", ".pptx"}
)

MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES: int = 64 * 1024 * 1024  # 64 MB
MAXIMUM_SOURCE_FILE_NAME_LENGTH: int = 120

# Windows reserves these regardless of extension; a file named CON.txt cannot be
# created and the resulting OSError is opaque.
WINDOWS_RESERVED_FILE_STEMS: frozenset[str] = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{digit}" for digit in range(1, 10)}
    | {f"LPT{digit}" for digit in range(1, 10)}
)

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
    report both so a silently renamed file is never a surprise.
    """

    original_file_name: str
    safe_file_name: str
    size_in_bytes: int
    suffix: str

    @property
    def was_renamed(self) -> bool:
        return self.original_file_name != self.safe_file_name


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


def validate_uploaded_source_file(
    original_file_name: str,
    file_content: bytes,
    destination_directory: Path,
) -> AcceptedSourceFile:
    """The only sanctioned way to admit a source file.

    Raises `SourceFileRejected` with a user-facing reason; never writes anything.
    The caller writes to `destination_directory / result.safe_file_name`.
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

    if len(file_content) == 0:
        raise SourceFileRejected(original_file_name, "the file is empty")

    if len(file_content) > MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES:
        limit_in_megabytes = MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES // (1024 * 1024)
        actual_in_megabytes = len(file_content) / (1024 * 1024)
        raise SourceFileRejected(
            original_file_name,
            f"the file is {actual_in_megabytes:.1f} MB, over the "
            f"{limit_in_megabytes} MB limit",
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

    return AcceptedSourceFile(
        original_file_name=original_file_name,
        safe_file_name=safe_file_name,
        size_in_bytes=len(file_content),
        suffix=suffix,
    )
