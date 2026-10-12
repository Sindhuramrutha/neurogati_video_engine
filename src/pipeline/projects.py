"""Projects — the unit of work. Everything starts with a project name.

Files are the source of truth: a project is a directory, and its state is
whatever is on disk. There is no database row that can disagree with it, and a project
is portable by copying the folder.
"""

from __future__ import annotations

import json
import logging
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from pipeline.sources import SUPPORTED_SOURCE_FILE_SUFFIXES
from pipeline.stages import STAGES, Stage
from pipeline.storage.documents import read_json_object, write_text_atomically
from pipeline.storage.layout import slugify

logger = logging.getLogger(__name__)

# Re-exported from pipeline.sources so "what counts as a source file?" has exactly
# one answer. Duplicating the set here is how the API and the UI end up disagreeing
# about which files are acceptable.
SOURCE_SUFFIXES = SUPPORTED_SOURCE_FILE_SUFFIXES

_KINDS = {".pptx": "deck", ".pdf": "PDF", ".docx": "Word document", ".md": "Markdown",
          ".txt": "text"}
_described: dict[tuple[str, int, int], dict] = {}


def describe_source(path: Path) -> dict:
    """What a source file is, and how much of it, without extracting it: a deck's
    slides, a PDF's pages, a document's words. Read once per version of the file."""
    import re
    import zipfile

    stat = path.stat()
    key = (str(path), stat.st_size, int(stat.st_mtime))
    if key in _described:
        return _described[key]
    suffix = path.suffix.lower()
    measure = ""
    try:
        if suffix == ".pptx":
            with zipfile.ZipFile(path) as deck:
                slides = [name for name in deck.namelist()
                          if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)]
            measure = f"{len(slides)} slide{'' if len(slides) == 1 else 's'}"
        elif suffix == ".pdf":
            from pypdf import PdfReader
            pages = len(PdfReader(str(path)).pages)
            measure = f"{pages} page{'' if pages == 1 else 's'}"
        elif suffix == ".docx":
            from docx import Document
            words = sum(len(p.text.split()) for p in Document(str(path)).paragraphs)
            measure = f"{words:,} words"
        elif suffix in (".md", ".txt"):
            words = len(path.read_text(encoding="utf-8", errors="replace").split())
            measure = f"{words:,} words"
    except Exception as unreadable:     # a file that cannot be read is said so, not raised
        logger.info("could not measure %s: %s", path.name, unreadable)
    described = {"kind": _KINDS.get(suffix, suffix.lstrip(".")), "measure": measure}
    _described[key] = described
    return described


@dataclass
class StageState:
    stage: Stage
    status: str  # "empty" | "ready" | "stale"
    artifact: str | None
    detail: str = ""


@dataclass
class Project:
    name: str
    slug: str
    root: Path
    created: str

    @property
    def sources_dir(self) -> Path:
        return self.root / "sources"

    def stage_dir(self, stage: Stage) -> Path:
        return self.root / stage.value

    @property
    def meta_path(self) -> Path:
        return self.root / "project.json"

    @property
    def source(self) -> dict | None:
        """The project's one source file, or None, with what it is in words: "deck",
        "5 slides". A project is made from exactly one file; should a folder from
        before that hold more, the first is it."""
        found = self.sources()
        if not found:
            return None
        return found[0] | describe_source(self.sources_dir / found[0]["name"])

    def sources(self) -> list[dict]:
        if not self.sources_dir.exists():
            return []
        return [
            {
                "name": p.name,
                "suffix": p.suffix.lower(),
                "bytes": p.stat().st_size,
                "supported": p.suffix.lower() in SOURCE_SUFFIXES,
            }
            for p in sorted(self.sources_dir.iterdir())
            if p.is_file()
        ]

    def stage_state(self, stage: Stage) -> StageState:
        """Derived from disk, never cached.

        Inputs is special: it is 'ready' once the source file exists, since there
        is no artifact to produce -- the file itself is the output.
        """
        if stage is Stage.INPUTS:
            source = self.source
            return StageState(
                stage=stage,
                status="ready" if source else "empty",
                artifact="sources/" if source else None,
                detail=source["name"] if source else "no source yet",
            )

        d = self.stage_dir(stage)
        if not d.exists() or not any(d.iterdir()):
            return StageState(stage=stage, status="empty", artifact=None, detail="not run")
        return StageState(
            stage=stage,
            status="ready",
            artifact=f"{stage.value}/",
            detail=_stage_detail(stage, d),
        )

    @staticmethod
    def _detail_for_reviewing(stage_directory: Path) -> str:
        """What Reviewing has, not how many files it left lying around.

        Counting files reported "96 file(s)" for one 8-minute video, because a
        render leaves a PNG per slide and an audio file per section in its
        working directory. A number that large reads as something being wrong,
        and it told the operator nothing they wanted to know.
        """
        renders = sorted((stage_directory / "output").glob("*.mp4"))
        if not renders:
            return "no render yet"
        newest = max(renders, key=lambda path: path.stat().st_mtime)
        return f"{len(renders)} render(s) - {newest.name}"

    def states(self) -> list[StageState]:
        return [self.stage_state(s.key) for s in STAGES]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "slug": self.slug,
            "created": self.created,
            "sources": self.sources(),
            "source": self.source,
            "stages": [
                {
                    "stage": s.stage.value,
                    "status": s.status,
                    "artifact": s.artifact,
                    "detail": s.detail,
                }
                for s in self.states()
            ],
        }


def _stage_detail(stage: Stage, stage_directory: Path) -> str:
    """One line saying what a finished stage produced."""
    if stage is Stage.REVIEWING:
        return Project._detail_for_reviewing(stage_directory)
    if stage is Stage.EXTRACTION:
        detail = _detail_for_extraction(stage_directory)
        if detail:
            return detail
    if stage is Stage.SCENE_PLAN:
        detail = _detail_for_planning(stage_directory)
        if detail:
            return detail
    if stage is Stage.SCRIPT_STAGING:
        detail = _detail_for_scripting(stage_directory)
        if detail:
            return detail
    files = [path for path in stage_directory.rglob("*") if path.is_file()]
    return f"{len(files)} file(s)"


def _detail_for_scripting(stage_directory: Path) -> str:
    """Sections written out of the plan's sections, and the spoken length."""
    import json

    try:
        script = json.loads((stage_directory / "script.json").read_text(encoding="utf-8"))
        plan = json.loads(
            (stage_directory.parent / "scene-plan" / "plan.json").read_text(encoding="utf-8")
        )
    except (OSError, ValueError):
        return ""

    section_ids = {s.get("id") for s in plan.get("sections", [])}
    written = [
        s for s in script.get("section_scripts", [])
        if s.get("section_id") in section_ids and (s.get("body") or "").strip()
    ]
    words = sum(len((s.get("body") or "").split()) for s in written)
    seconds = round(words / 150 * 60)
    length = f"~{round(seconds / 60)} min" if seconds >= 60 else f"~{seconds} sec"
    return f"{len(written)} of {len(section_ids)} sections written · {length}"


def _detail_for_planning(stage_directory: Path) -> str:
    """Sections and running time, from the plan -- not "1 file(s)", which was
    true of every plan ever made and said nothing about any of them."""
    import json

    try:
        plan = json.loads((stage_directory / "plan.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""

    sections = plan.get("sections", [])
    seconds = sum(int(s.get("estimated_seconds") or 0) for s in sections)
    length = f"~{round(seconds / 60)} min" if seconds >= 60 else f"~{seconds} sec"
    return f"{len(sections)} section{'' if len(sections) == 1 else 's'} · {length}"


def _detail_for_extraction(stage_directory: Path) -> str:
    """Documents and figures, read from the artifact rather than counted on disk.

    Counting files stopped meaning anything once figures were extracted: a
    three-document project read "55 file(s)", which is 54 images and one JSON
    file and says nothing about what was extracted.
    """
    import json

    content = stage_directory / "content.json"
    try:
        documents = json.loads(content.read_text(encoding="utf-8")).get("documents", [])
    except (OSError, ValueError):
        return ""

    figures = sum(
        1 for document in documents for block in document.get("blocks", [])
        if block.get("kind") == "figure"
    )
    parts = [f"{len(documents)} document{'' if len(documents) == 1 else 's'}"]
    if figures:
        parts.append(f"{figures} figure{'' if figures == 1 else 's'}")
    return " · ".join(parts)


class ProjectStore:
    def __init__(self, projects_dir: Path) -> None:
        self.root = projects_dir
        self.root.mkdir(parents=True, exist_ok=True)

    def _load(self, project_directory: Path) -> Project | None:
        """Read one project, or None if this directory is not a project.

        A missing project.json means "not a project" and is silent by design --
        stray directories under projects/ are not errors.

        A *corrupt* project.json is different: the project exists but cannot be
        read, and returning None silently made it disappear from the UI with no
        indication anything was wrong. That is logged loudly, because a vanished
        project is the kind of thing a user reports as "it deleted my work".
        """
        metadata_path = project_directory / "project.json"
        if not metadata_path.exists():
            return None   # not a project directory; silent by design

        # read_json_object logs an unreadable or non-object file loudly. A project
        # that silently disappears reads to a user as "it deleted my work".
        raw_metadata = read_json_object(
            metadata_path, f"project metadata for {project_directory.name}")
        if raw_metadata is None:
            return None

        return Project(
            name=str(raw_metadata.get("name") or project_directory.name),
            slug=project_directory.name,
            root=project_directory,
            created=str(raw_metadata.get("created") or ""),
        )

    def list(self) -> list[Project]:
        out = []
        for d in sorted(self.root.iterdir()) if self.root.exists() else []:
            if d.is_dir() and (p := self._load(d)):
                out.append(p)
        return out

    def get(self, slug: str) -> Project | None:
        d = self.root / slug
        if not d.is_dir():
            return None
        return self._load(d)

    def delete(self, slug: str) -> bool:
        """Erase a project and everything in it, for good -- False if `slug` is not
        a project folder. There is no trash and no way back: the page says so before
        it asks."""
        import os
        import shutil
        import stat
        import time

        project_directory = self.root / slug
        if not (project_directory / "project.json").is_file():
            return False

        def writable_then_retry(remove, path, _error):
            # Windows will not remove a read-only file: make it writable and go on.
            os.chmod(path, stat.S_IWRITE)
            remove(path)

        for attempt in range(1, 7):
            try:
                shutil.rmtree(project_directory, onexc=writable_then_retry)
                return True
            except OSError:
                # A process that was just killed may hold a file for a moment.
                if attempt == 6:
                    raise
                time.sleep(0.5)
        return True

    def create(self, name: str) -> Project:
        """Create a project directory, or fail without leaving a half-built one.

        Three problems the obvious version has:

        1. **Check-then-create is a race.** `if d.exists()` followed by `mkdir`
           lets two concurrent creates both pass the check; the loser then raised
           a raw FileExistsError, which surfaced as a 500 rather than the intended
           "already exists" 400. `mkdir(exist_ok=False)` makes the filesystem the
           arbiter, and its failure is translated here.
        2. **A partial create wedges the slug.** If the metadata write failed after
           the directories were made, `_load` returned None so the project was
           invisible in listings, while `create` refused to remake it. The
           directory is removed on failure instead.
        3. **The metadata write was not atomic**, unlike `Manifest.save`. Two
           standards for the same concern in one codebase is how the weaker one
           gets copied into the next module.
        """
        project_slug = slugify(name)
        project_directory = self.root / project_slug

        try:
            project_directory.mkdir(parents=True, exist_ok=False)
        except FileExistsError as already_exists:
            raise ValueError(
                f"a project already uses the folder name {project_slug!r}"
            ) from already_exists

        try:
            (project_directory / "sources").mkdir()
            for stage_specification in STAGES:
                if stage_specification.key is not Stage.INPUTS:
                    (project_directory / stage_specification.key.value).mkdir()

            created_timestamp = datetime.now(UTC).isoformat(timespec="seconds")
            self._write_project_metadata_atomically(
                project_directory, {"name": name, "created": created_timestamp}
            )
        except OSError:
            # Never leave a directory that listings skip but creation refuses.
            shutil.rmtree(project_directory, ignore_errors=True)
            raise

        return Project(
            name=name, slug=project_slug, root=project_directory,
            created=created_timestamp,
        )

    @staticmethod
    def _write_project_metadata_atomically(
        project_directory: Path, metadata: dict
    ) -> None:
        """Durability behaviour is shared -- see storage/documents.py."""
        write_text_atomically(
            project_directory / "project.json", json.dumps(metadata, indent=2))

