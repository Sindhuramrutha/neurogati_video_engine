"""Source-file admission tests.

The traversal cases are regression tests for a verified arbitrary-file-write: before
`pipeline.sources` existed, the upload route joined the raw multipart filename onto
the project directory, and a filename of `../../../ESCAPED.txt` demonstrably wrote
outside the project.
"""

import io

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
    accepted = validate_uploaded_source_file("Chapter 1.docx", b"PK\x03\x04x", tmp_path)
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


# --- large uploads ----------------------------------------------------------


class _Stream:
    """A minimal stand-in for an upload part: `read(size)` and nothing else."""

    def __init__(self, payload: bytes):
        self._buffer = io.BytesIO(payload)

    async def read(self, size: int = -1) -> bytes:
        return self._buffer.read(size)


async def test_a_large_file_is_streamed_to_disk(tmp_path):
    """The whole point: the file must never sit in memory in one piece.

    Reading the part first meant a 300 MB deck cost 300 MB of RAM before a byte
    was written. Here it arrives in blocks.
    """
    from pipeline.sources import UPLOAD_CHUNK_SIZE_IN_BYTES, store_uploaded_source_file

    payload = b"PK\x03\x04" + b"x" * (UPLOAD_CHUNK_SIZE_IN_BYTES * 3 + 17)
    accepted = await store_uploaded_source_file("big.pptx", _Stream(payload), tmp_path)

    assert accepted.size_in_bytes == len(payload)
    assert (tmp_path / "big.pptx").read_bytes() == payload


async def test_an_oversized_upload_is_abandoned_without_filling_the_disk(tmp_path, monkeypatch):
    """It must stop at the limit, not after writing the whole thing."""
    import pipeline.sources as sources

    monkeypatch.setattr(sources, "MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES", 4096)
    monkeypatch.setattr(sources, "UPLOAD_CHUNK_SIZE_IN_BYTES", 1024)

    with pytest.raises(sources.SourceFileRejected) as rejection:
        await sources.store_uploaded_source_file(
            "huge.pdf", _Stream(b"%PDF" + b"y" * 40_000), tmp_path
        )

    assert "larger than" in rejection.value.reason
    assert list(tmp_path.iterdir()) == [], "an abandoned upload must leave nothing behind"


async def test_an_interrupted_upload_leaves_no_half_file(tmp_path):
    """A partial file in sources/ looks like a real document to every later
    stage, so the write goes to a temporary name and is renamed only once
    complete."""
    from pipeline.sources import store_uploaded_source_file

    class _Failing:
        def __init__(self):
            self._sent = False

        async def read(self, size: int = -1) -> bytes:
            if self._sent:
                raise ConnectionResetError("the client went away")
            self._sent = True
            return b"PK\x03\x04" + b"z" * 2048

    with pytest.raises(ConnectionResetError):
        await store_uploaded_source_file("dropped.docx", _Failing(), tmp_path)

    assert list(tmp_path.iterdir()) == [], "a dropped upload must leave nothing behind"


async def test_the_wrong_type_is_refused_before_any_bytes_are_read(tmp_path):
    """A 300 MB file with an unsupported extension should not be transferred at
    all before being refused."""
    from pipeline.sources import SourceFileRejected, store_uploaded_source_file

    class _NeverRead:
        async def read(self, size: int = -1) -> bytes:
            raise AssertionError("the body was read before the name was checked")

    with pytest.raises(SourceFileRejected) as rejection:
        await store_uploaded_source_file("movie.mkv", _NeverRead(), tmp_path)

    assert ".mkv" in rejection.value.reason


async def test_an_empty_upload_is_refused(tmp_path):
    from pipeline.sources import SourceFileRejected, store_uploaded_source_file

    with pytest.raises(SourceFileRejected) as rejection:
        await store_uploaded_source_file("nothing.txt", _Stream(b""), tmp_path)

    assert "empty" in rejection.value.reason
    assert list(tmp_path.iterdir()) == []


# --- contents and identity ---------------------------------------------------


@pytest.mark.parametrize("file_name, content", [
    ("chapter.docx", b"%PDF-1.7 a PDF wearing a Word extension"),
    ("deck.pptx", b"%PDF-1.4"),
    ("notes.pdf", b"PK\x03\x04 a zip wearing a PDF extension"),
    ("notes.md", b"PK\x03\x04\x00\x00 binary"),
])
async def test_contents_that_contradict_the_extension_are_refused(file_name, content, tmp_path):
    """Passed by name, the file used to fail minutes later inside extraction
    with an error about zip archives."""
    from pipeline.sources import store_uploaded_source_file

    with pytest.raises(SourceFileRejected) as rejection:
        await store_uploaded_source_file(file_name, _Stream(content), tmp_path)

    assert file_name.rsplit(".", 1)[1] in rejection.value.reason
    assert list(tmp_path.iterdir()) == [], "a refused upload must leave nothing behind"


def test_the_same_check_applies_when_the_bytes_are_already_in_hand(tmp_path):
    with pytest.raises(SourceFileRejected):
        validate_uploaded_source_file("chapter.docx", b"%PDF-1.7", tmp_path)


async def test_a_pdf_header_after_leading_junk_is_still_a_pdf(tmp_path):
    from pipeline.sources import store_uploaded_source_file

    accepted = await store_uploaded_source_file(
        "scan.pdf", _Stream(b"\r\n\xef\xbb\xbf%PDF-1.5 body"), tmp_path)
    assert accepted.suffix == ".pdf"


async def test_a_second_upload_under_the_same_name_is_reported_as_a_replacement(tmp_path):
    """Two different files can sanitise to one name -- "Chapter 4: Networks" and
    "Chapter 4_ Networks" -- and the loser used to vanish with an "accepted"."""
    from pipeline.sources import store_uploaded_source_file

    first = await store_uploaded_source_file(
        "Chapter 4: Networks.md", _Stream(b"first"), tmp_path)
    second = await store_uploaded_source_file(
        "Chapter 4_ Networks.md", _Stream(b"second"), tmp_path)

    assert first.safe_file_name == second.safe_file_name
    assert first.was_replaced is False
    assert second.was_replaced is True
    assert (tmp_path / second.safe_file_name).read_bytes() == b"second"


def test_the_request_limit_is_not_the_framework_default():
    """Litestar's default is 10 MB, which refused one ordinary 50-slide deck
    with "Request Entity Too Large" before any check in this codebase ran."""
    from pipeline.sources import (
        MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES,
        MAXIMUM_UPLOAD_REQUEST_SIZE_IN_BYTES,
    )
    from pipeline.web.app import create_app

    app = create_app()
    assert app.request_max_body_size == MAXIMUM_UPLOAD_REQUEST_SIZE_IN_BYTES
    assert app.request_max_body_size >= MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES, (
        "a single file at the per-file limit must fit inside one request"
    )
    assert MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES >= 256 * 1024 * 1024, (
        "a 50-slide deck with images is routinely over 100 MB"
    )
