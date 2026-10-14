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
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from pipeline.composition import CompositionStore
from pipeline.core import require_project
from pipeline.freshness import cut_freshness
from pipeline.planning import Plan
from pipeline.presentation import section_start_times
from pipeline.projects import Project
from pipeline.review import CommentStatus, ReviewStore
from pipeline.scripting import Script
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
    if plan.get("audience"):
        lines += [f"**For:** {plan['audience']}", ""]

    if sections:
        lines += ["**Chapters**", ""]
        lines += [
            f"- {_clock(section['start_ms'])} — {section['title']}" for section in sections
        ]
        lines.append("")
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


# --- what a client calls -----------------------------------------------------


def _export_sections(project: Project, plan: Plan, script: Script) -> list[dict[str, Any]]:
    starts = section_start_times(project, plan)
    return [
        {
            "id": section.id,
            "title": section.title,
            "body": script.spoken_text(section.id),
            "start_ms": start_ms,
        }
        for section, start_ms in zip(plan.sections, starts, strict=False)
    ]

def export_readiness(project: Project) -> tuple[list[str], list[str]]:
    """What stops this project being handed over, and what merely ought to be known.

    Blockers are the things that make the files wrong: no plan, no narration, no
    render, or a cut built from a script that is no longer current. Everything
    else is a warning, because "one comment is still open" is a judgement and
    this stage does not get to make it.
    """
    from pipeline.plan_handoff import plan_for_later_stages
    plan = plan_for_later_stages(project)
    from pipeline.script_handoff import script_for_later_stages
    script = script_for_later_stages(project)
    review = ReviewStore(project.root).load()
    composition = CompositionStore(project.root).load()

    blockers: list[str] = []
    warnings: list[str] = []

    if not plan.sections:
        blockers.append("The plan has no sections.")
    unwritten = [s.title for s in plan.sections if not script.body_for(s.id).strip()]
    if unwritten:
        shown = ", ".join(unwritten[:3])
        more = "..." if len(unwritten) > 3 else ""
        blockers.append(f"{len(unwritten)} section(s) have no narration: {shown}{more}.")
    if not review.versions:
        blockers.append("Nothing has been rendered yet.")

    blockers.extend(cut_freshness(plan, composition)["warnings"])

    open_comments = [
        comment for comment in review.comments
        if comment.status == CommentStatus.OPEN
    ]
    if open_comments:
        warnings.append(f"{len(open_comments)} review comment(s) are still open.")
    from pipeline.generation import VisualPlanStore

    for visual in VisualPlanStore(project.root).load().visuals:
        if visual.below_bar and visual.clip_path:
            warnings.append(f"Scene {visual.scene_number or ''} of \"{visual.section_title}\" "
                            f"is used below the quality bar: {visual.below_bar}")
    stranded = script.audit([s.id for s in plan.sections])["orphaned_section_ids"]
    if stranded:
        warnings.append(
            f"{len(stranded)} piece(s) of narration are not attached to any section."
        )
    return blockers, warnings

def build_export(slug: str) -> dict[str, Any]:
    """Write the transcript, chapters and description, and list what is ready.

    Refuses nothing: a project with problems still gets its manifest, with the
    problems named in it. Withholding the files would not make the video better,
    and someone checking what is wrong needs the transcript to do it.
    """
    from pipeline.plan_handoff import plan_for_later_stages
    project = require_project(slug)
    plan = plan_for_later_stages(project)
    from pipeline.script_handoff import script_for_later_stages
    script = script_for_later_stages(project)
    review = ReviewStore(project.root).load()

    blockers, warnings = export_readiness(project)
    sections = _export_sections(project, plan, script)
    files = write_export_files(project.root, project.name, plan.to_dict(), sections)

    version = next(
        (v for v in review.versions if v.id == review.active_version_id),
        review.versions[-1] if review.versions else None,
    )
    if version is not None:
        video = Path(version.file_path)
        if video.exists():
            files.append(ExportedFile(
                name=video.name, kind="video",
                path=str(video.relative_to(project.root)).replace("\\", "/"),
                bytes=video.stat().st_size,
                note=version.label or "The rendered video.",
            ))
            for subtitle in sorted(video.parent.glob(video.stem + "*.vtt")):
                files.append(ExportedFile(
                    name=subtitle.name, kind="subtitles",
                    path=str(subtitle.relative_to(project.root)).replace("\\", "/"),
                    bytes=subtitle.stat().st_size,
                    note="Subtitles, timed to the narration.",
                ))
            files += _youtube_files(project, video, version.duration_ms)
        else:
            blockers.append(f"The rendered video is missing from disk: {video.name}")

    manifest = ExportManifest(
        built_at=datetime.now(UTC).isoformat(timespec="seconds"),
        video_version_id=version.id if version else "",
        title=project.name,
        duration_ms=version.duration_ms if version else 0,
        files=files,
        blockers=blockers,
        warnings=warnings,
    )
    return ExportStore(project.root).save(manifest).to_dict()

def read_export(slug: str) -> dict[str, Any]:
    """The last export, with today's blockers rather than the ones it was built with."""
    project = require_project(slug)
    manifest = ExportStore(project.root).load()
    blockers, warnings = export_readiness(project)
    return manifest.to_dict() | {
        "blockers_now": blockers,
        "warnings_now": warnings,
        "is_ready_now": not blockers,
    }


def _youtube_files(project: Project, video: Path, duration_ms: int) -> list[ExportedFile]:
    """When the video is going to YouTube (Video setup): a thumbnail with its title,
    and the subtitles in the format YouTube asks for (SRT)."""
    from pipeline.thumbnail import make_thumbnail
    from pipeline.video_setup import platform_needs

    if not platform_needs(project.root)["youtube"]:
        return []
    files = []
    target = project.root / "export" / "thumbnail.png"
    if make_thumbnail(video, project.name, target, duration_ms / 1000):
        files.append(ExportedFile(name=target.name, kind="thumbnail", path="export/thumbnail.png",
                                  bytes=target.stat().st_size,
                                  note="For YouTube: a moment of the video with its title."))
    for subtitle in sorted(video.parent.glob(video.stem + "*.srt")):
        files.append(ExportedFile(
            name=subtitle.name, kind="subtitles",
            path=str(subtitle.relative_to(project.root)).replace("\\", "/"),
            bytes=subtitle.stat().st_size, note="Subtitles for YouTube (SRT)."))
    return files
