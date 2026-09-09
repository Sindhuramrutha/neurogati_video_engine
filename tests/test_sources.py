"""Source-file admission tests.

The traversal cases are regression tests for a verified arbitrary-file-write: before
`pipeline.sources` existed, the upload route joined the raw multipart filename onto
the project directory, and a filename of `../../../ESCAPED.txt` demonstrably wrote
outside the project.
"""

import pytest

from pipeline.sources import (
    MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES,
    AcceptedSourceFile,
    SourceFileRejected,
    reduce_to_bare_file_name,
    sanitize_source_file_name,
    validate_uploaded_source_file,
)

# --- path traversal ----------------------------------------------------------


@pytest.mark.parametrize(
    "hostile_file_name",
    [
        "../../../ESCAPED.txt",
        "..\\..\\..\\ESCAPED.txt",
        "../../ESCAPED.md",
        "/etc/passwd.txt",
        "C:\\Windows\\System32\\evil.txt",
        "subdir/../../../ESCAPED.pdf",
        "....//....//ESCAPED.md",
    ],
)
def test_traversal_attempts_never_escape_the_destination(hostile_file_name, tmp_path):
    destination = tmp_path / "sources"
    destination.mkdir()

    try:
        accepted = validate_uploaded_source_file(
            original_file_name=hostile_file_name,
            file_content=b"content",
            destination_directory=destination,
        )
    except SourceFileRejected:
        return  # refusing outright is an acceptable outcome

    written_path = (destination / accepted.safe_file_name).resolve()
    assert written_path.is_relative_to(destination.resolve()), (
        f"{hostile_file_name!r} resolved to {written_path}, outside {destination}"
    )
    assert "/" not in accepted.safe_file_name
    assert "\\" not in accepted.safe_file_name


def test_null_bytes_are_stripped_from_file_names():
    assert "\x00" not in reduce_to_bare_file_name("evil\x00.md")


# --- type and size -----------------------------------------------------------


@pytest.mark.parametrize(
    "unsupported_file_name", ["clip.mp4", "archive.zip", "script.exe", "noextension"]
)
def test_unsupported_types_are_rejected_with_a_usable_reason(
    unsupported_file_name, tmp_path
):
    with pytest.raises(SourceFileRejected) as rejection:
        validate_uploaded_source_file(unsupported_file_name, b"x", tmp_path)
    # The message must name what IS allowed, not merely what was refused.
    assert "supported types" in str(rejection.value).lower()


def test_oversized_uploads_are_rejected_before_any_write(tmp_path):
    oversized_content = b"x" * (MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES + 1)
    with pytest.raises(SourceFileRejected) as rejection:
        validate_uploaded_source_file("big.pdf", oversized_content, tmp_path)
    assert "limit" in str(rejection.value).lower()
    assert not any(tmp_path.iterdir())


def test_empty_uploads_are_rejected(tmp_path):
    """A zero-byte file passes every other check and then fails deep inside
    extraction, where the cause is no longer obvious."""
    with pytest.raises(SourceFileRejected):
        validate_uploaded_source_file("empty.md", b"", tmp_path)


def test_missing_file_name_is_rejected(tmp_path):
    with pytest.raises(SourceFileRejected):
        validate_uploaded_source_file("", b"content", tmp_path)


# --- sanitisation ------------------------------------------------------------


def test_ordinary_file_names_survive_untouched(tmp_path):
    accepted = validate_uploaded_source_file("Chapter 1.docx", b"x", tmp_path)
    assert accepted.safe_file_name == "Chapter 1.docx"
    assert accepted.was_renamed is False


def test_renaming_is_reported_so_it_is_never_a_silent_surprise(tmp_path):
    accepted = validate_uploaded_source_file("we:rd*name?.md", b"x", tmp_path)
    assert accepted.was_renamed is True
    assert accepted.original_file_name == "we:rd*name?.md"
    assert ":" not in accepted.safe_file_name


def test_windows_reserved_names_are_made_creatable():
    """CON.txt cannot be created on Windows; the resulting OSError is opaque."""
    assert sanitize_source_file_name("CON.md") != "CON.md"
    assert sanitize_source_file_name("con.md").lower().startswith("con_file")


def test_absurdly_long_names_are_truncated_but_keep_their_suffix():
    safe = sanitize_source_file_name("a" * 400 + ".pdf")
    assert len(safe) <= 120
    assert safe.endswith(".pdf")


def test_a_name_of_only_punctuation_still_yields_a_usable_file(tmp_path):
    accepted = validate_uploaded_source_file("***.md", b"x", tmp_path)
    assert accepted.safe_file_name.endswith(".md")
    assert len(accepted.safe_file_name) > len(".md")


def test_accepted_result_reports_size_and_suffix(tmp_path):
    accepted = validate_uploaded_source_file("notes.MD", b"12345", tmp_path)
    assert isinstance(accepted, AcceptedSourceFile)
    assert accepted.size_in_bytes == 5
    assert accepted.suffix == ".md"  # normalised, so downstream can compare directly
