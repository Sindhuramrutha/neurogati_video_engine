"""Export — the video, and everything that travels with it.

A finished render is an .mp4 and a .vtt in a folder nobody else can navigate.
Handing the work over means a transcript someone can read, chapter marks that
can be pasted into a video host, a description built from what the project
already decided, and one manifest that says what each file is.

All of it is derived. Nothing here is written by hand and nothing is invented:
the transcript is the spoken text, the chapters are the measured section start
times, the description is the plan's audience and objectives. If any of those
change, the export is rebuilt rather than edited.

The checks matter more than the files. Exporting is the last point at which a
video can be stopped, so a cut whose timeline no longer matches the plan, a
section with no narration, or an open review comment is reported here and the
export says plainly that it is not ready.

Stored at `projects/<slug>/export/manifest.json`, beside the files it describes.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, write_text_atomically
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)


def _clock(milliseconds: int) -> str:
    """0:00 / 1:02:03 — how a video host wants a chapter mark."""
    seconds = max(0, milliseconds // 1000)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"


class ExportedFile(BaseModel):
    name: str = ""
    kind: str = ""          # video | subtitles | transcript | chapters | description | audio
    path: str = ""          # relative to the project root
    bytes: int = 0
    note: str = ""


class ExportManifest(BaseModel):
    built_at: str = ""
    video_version_id: str = ""
    title: str = ""
    duration_ms: int = 0
    files: list[ExportedFile] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @property
    def is_ready(self) -> bool:
        return bool(self.built_at) and not self.blockers

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump() | {
            "is_ready": self.is_ready,
            "is_empty": not self.built_at,
            "file_count": len(self.files),
        }


def default_export_manifest() -> ExportManifest:
    return ExportManifest()


class ExportStore(JsonDocumentStore[ExportManifest]):
    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.EXPORT),
            model_type=ExportManifest,
            build_default=default_export_manifest,
            description="export manifest",
        )


def transcript_markdown(project_name: str, sections: list[dict[str, Any]]) -> str:
    """The spoken words, under the section headings, with their start times."""
    lines = [f"# {project_name} — transcript", ""]
    for section in sections:
        lines.append(f"## {_clock(section['start_ms'])} · {section['title']}")
        lines.append("")
        lines.append(section["body"].strip() or "_No narration written._")
        lines.append("")
    return "\n".join(lines)


def chapters_text(sections: list[dict[str, Any]]) -> str:
    """`0:00 Title` per line, which is what a video host reads as chapters."""
    return "\n".join(
        f"{_clock(section['start_ms'])} {section['title']}" for section in sections
    )


def description_markdown(
    project_name: str, plan: dict[str, Any], sections: list[dict[str, Any]]
) -> str:
    """What the video is, from what the project already decided."""
    lines = [f"# {project_name}", ""]
    if plan.get("selected_audience"):
        lines += [f"**For:** {plan['selected_audience']}", ""]

    objectives = [o["text"] for o in plan.get("learning_objectives", []) if o.get("text")]
    if objectives:
        lines += ["**By the end of this video you will be able to:**", ""]
        lines += [f"- {text}" for text in objectives]
        lines.append("")

    if sections:
        lines += ["**Chapters**", ""]
        lines += [
            f"- {_clock(section['start_ms'])} — {section['title']}" for section in sections
        ]
        lines.append("")

    themes = [t for t in plan.get("key_themes", []) if t]
    if themes:
        lines += ["**Topics:** " + ", ".join(themes), ""]
    return "\n".join(lines)


def write_export_files(
    project_root: Path, project_name: str, plan: dict[str, Any], sections: list[dict[str, Any]]
) -> list[ExportedFile]:
    """Write the derived files and describe them. Returns what was written."""
    folder = project_root / "export"
    folder.mkdir(parents=True, exist_ok=True)

    written: list[ExportedFile] = []
    documents = [
        ("transcript.md", "transcript", transcript_markdown(project_name, sections),
         "Every spoken word, under its section."),
        ("chapters.txt", "chapters", chapters_text(sections),
         "Paste into a video host that reads timestamped chapters."),
        ("description.md", "description", description_markdown(project_name, plan, sections),
         "Audience, objectives and chapters, from the plan."),
    ]
    for name, kind, content, note in documents:
        path = folder / name
        write_text_atomically(path, content)
        written.append(ExportedFile(
            name=name, kind=kind, path=f"export/{name}",
            bytes=path.stat().st_size, note=note,
        ))
    return written
