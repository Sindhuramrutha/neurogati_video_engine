"""The project's source file: one per project, uploaded, replaced or removed.

A project is made from exactly one file -- a deck, a PDF, a Word document, a
Markdown or text file -- and that file runs through every layer. So an upload
carries one file, and a project that already has one only takes another when
the request says `replace`: nothing is ever replaced by accident.

Replacing the file leaves the work after Extraction where it is. Extraction
reads the new file, and every later layer is flagged out of date (`upstream.py`)
until it is redone, or transferred as it stands.
"""

from __future__ import annotations

import logging
from typing import Annotated, Any

from litestar import delete, post
from litestar.di import NamedDependency
from litestar.enums import RequestEncodingType
from litestar.exceptions import ClientException, NotFoundException
from litestar.params import Body, FromPath

from pipeline.extraction import ExtractionCollectionStore
from pipeline.sources import (
    SourceFileRejected,
    reduce_to_bare_file_name,
    store_uploaded_source_file,
)
from pipeline.web.routes_project import ProjectService

logger = logging.getLogger(__name__)


@post("/api/projects/{slug:str}/sources")
async def upload_source(
    slug: FromPath[str],
    projects: NamedDependency[ProjectService],
    data: Annotated[dict[str, Any], Body(media_type=RequestEncodingType.MULTI_PART)],
    replace: bool = False,
) -> dict[str, Any]:
    """Store the project's source file, or replace it when `replace` is set."""
    project = projects.require(slug)
    parts = [part for part in data.values() if hasattr(part, "read")]
    if not parts:
        raise ClientException(detail="No file was found in the upload.")
    if len(parts) > 1:
        raise ClientException(
            detail=f"A project has one source file; {len(parts)} were sent. Upload one: a "
                   f"deck, a PDF, a Word, Markdown or text file.")

    previous = [source["name"] for source in project.sources()]
    if previous and not replace:
        raise ClientException(
            detail=f"This project's source is {previous[0]}. Replace it to use another file.")

    upload = parts[0]
    staging = project.root / ".incoming"
    try:
        # Stored beside the project first: a file that is refused leaves the
        # current source exactly as it was.
        accepted = await store_uploaded_source_file(
            original_file_name=getattr(upload, "filename", "") or "",
            upload_stream=upload, destination_directory=staging)
    except SourceFileRejected as rejection:
        logger.info("rejected source upload for project %s: %s", slug, rejection)
        raise ClientException(
            detail=f"{rejection.original_file_name} was not used: {rejection.reason}.") \
            from rejection

    project.sources_dir.mkdir(parents=True, exist_ok=True)
    for name in previous:
        (project.sources_dir / name).unlink(missing_ok=True)
    (staging / accepted.safe_file_name).replace(project.sources_dir / accepted.safe_file_name)
    staging.rmdir()
    logger.info("source for project %s is now %s (%s bytes)%s", slug,
                accepted.safe_file_name, accepted.size_in_bytes,
                f", replacing {previous[0]}" if previous else "")
    return {
        "accepted": accepted.to_dict(),
        "replaced": previous[0] if previous else "",
        "project": project.to_dict(),
    }


@delete("/api/projects/{slug:str}/sources/{file_name:str}", status_code=200)
async def delete_source(
    slug: FromPath[str], file_name: FromPath[str], projects: NamedDependency[ProjectService],
) -> dict[str, Any]:
    """Remove the project's source file.

    The name arrives from the URL, so it is reduced to a bare name and checked to
    be inside the sources folder: a crafted request cannot delete anything else.
    The extraction made from it stays until Extraction is run on a new file, and
    whatever was transferred stays with the later layers.
    """
    project = projects.require(slug)
    bare_file_name = reduce_to_bare_file_name(file_name)
    target_path = (project.sources_dir / bare_file_name).resolve()
    if not target_path.is_relative_to(project.sources_dir.resolve()):
        logger.warning("refused delete outside sources dir for project %s: %r", slug, file_name)
        raise ClientException(detail="that filename is not valid")
    if not target_path.is_file():
        raise NotFoundException(detail=f"no such source file: {bare_file_name}")
    try:
        target_path.unlink()
    except OSError as delete_failure:
        logger.warning("failed deleting %s from project %s: %s", bare_file_name, slug,
                       delete_failure)
        raise ClientException(detail="could not delete that file") from delete_failure

    collection = ExtractionCollectionStore(project.root).load()
    return {
        "deleted": bare_file_name,
        "was_in_extraction": any(d.file_name == bare_file_name for d in collection.documents),
        "project": project.to_dict(),
    }


SOURCE_ROUTES = [upload_source, delete_source]
