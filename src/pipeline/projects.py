"""Projects — the unit of work. Everything starts with a project name.

Files are the source of truth (ADR 0005): a project is a directory, and its state is
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

        Inputs is special: it is 'ready' when at least one source exists, since there
        is no artifact to produce -- the files themselves are the output.
        """
        if stage is Stage.INPUTS:
            n = len(self.sources())
            return StageState(
                stage=stage,
                status="ready" if n else "empty",
                artifact="sources/" if n else None,
                detail=f"{n} file(s)" if n else "no sources yet",
            )

        d = self.stage_dir(stage)
        if not d.exists() or not any(d.iterdir()):
            return StageState(stage=stage, status="empty", artifact=None, detail="not run")
        files = [p for p in d.rglob("*") if p.is_file()]
        return StageState(
            stage=stage,
            status="ready",
            artifact=f"{stage.value}/",
            detail=f"{len(files)} file(s)",
        )

    def states(self) -> list[StageState]:
        return [self.stage_state(s.key) for s in STAGES]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "slug": self.slug,
            "created": self.created,
            "sources": self.sources(),
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
        return self._load(d) if d.is_dir() else None

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

    def delete(self, slug: str) -> bool:
        d = self.root / slug
        if not d.is_dir() or not (d / "project.json").exists():
            return False
        shutil.rmtree(d)
        return True
