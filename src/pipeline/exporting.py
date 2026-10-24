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

import json
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
    kind: str = ""  # video | subtitles | transcript | chapters | description | credits | audio
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
    # How many of the deck's pictures the video shows, and the outside pictures it
    # credits.
    deck_pictures: dict[str, Any] = Field(default_factory=dict)
    credits: list[dict[str, Any]] = Field(default_factory=list)
    # Built as a draft: scenes whose own checks still fail were accepted, on purpose.
    draft: bool = False

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


def credits_markdown(project_name: str, credits: list[dict[str, Any]]) -> str:
    """Every picture from outside the deck, with what its licence asks: the work,
    its author, where it is, and the licence."""
    lines = [f"# {project_name} — picture credits", "",
             "Pictures from outside the course's deck, each under a licence that allows "
             "commercial use.", ""]
    for entry in credits:
        title = entry.get("title") or entry.get("file", "")
        page = entry.get("page", "")
        licence = entry.get("licence", "")
        lines.append(f"- {f'[{title}]({page})' if page else title}"
                     f" — {entry.get('author') or 'unknown author'}"
                     f", {entry.get('source', '')}"
                     + (f", {licence}" if licence else "")
                     + (f" ({entry['licence_url']})" if entry.get("licence_url") else ""))
    return "\n".join(lines) + "\n"


def write_export_files(
    project_root: Path, project_name: str, plan: dict[str, Any], sections: list[dict[str, Any]],
    credits: list[dict[str, Any]] | None = None, corrections: str = "",
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
    if credits:
        documents.append(("credits.md", "credits", credits_markdown(project_name, credits),
                          "The pictures from outside the deck, with the credit each "
                          "licence asks for: put it in the video's description."))
    if corrections:
        documents.append(("corrections.md", "corrections", corrections,
                          "What the slides may have wrong, and what the video says: for "
                          "the course team, to put the deck right."))
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

def scene_problems(project: Project) -> dict[str, list[dict[str, Any]]]:
    """The scenes in the video that are below the bar, by how bad.

    `failing`: its own fixed checks still fail -- text over text, a blank frame, a
    shape through words. The video has a visible defect there.
    `below_bar`: every check passes, and the reviewer still wants changes.
    """
    from pipeline.generation import VisualPlanStore
    from pipeline.scene_kept import failing_checks
    from pipeline.scene_program import scene_folder

    failing, below = [], []
    for number, visual in enumerate(VisualPlanStore(project.root).load().visuals, start=1):
        if not visual.clip_path:
            continue
        folder = scene_folder(project, visual)
        checks = [c.get("name", "") for c in failing_checks(folder)] if folder else []
        entry = {"scene": number, "visual_id": visual.id, "section": visual.section_title,
                 "checks": checks, "why": visual.below_bar}
        if checks:
            failing.append(entry)
        elif visual.below_bar:
            below.append(entry)
    return {"failing": failing, "below_bar": below}


def _scene_list(entries: list[dict[str, Any]], with_checks: bool) -> str:
    shown = [f"scene {e['scene']} ({e['section']}"
             + (f": {', '.join(e['checks'])}" if with_checks else "") + ")"
             for e in entries[:6]]
    return "; ".join(shown) + (f"; and {len(entries) - 6} more" if len(entries) > 6 else "")


def export_readiness(project: Project, usage: dict[str, Any] | None = None,
                     draft: bool = False, problems: dict[str, list] | None = None
                     ) -> tuple[list[str], list[str]]:
    """What stops this project being handed over, and what merely ought to be known.

    Blockers are the things that make the files wrong: no plan, no narration, no
    render, a cut built from a script that is no longer current -- and a scene in
    the video whose own checks still fail, a visible defect, unless the export is
    built as a draft on purpose. Everything else is a warning, because "one comment
    is still open" or "the reviewer wants a better layout" is a judgement and this
    stage does not get to make it.
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
    problems = problems or scene_problems(project)
    if problems["failing"]:
        said = (f"{len(problems['failing'])} scene(s) in the video still fail their own "
                f"checks: {_scene_list(problems['failing'], True)}. "
                "Remake them on Generation")
        if draft:
            warnings.append(f"Accepted as a draft: {said}.")
        else:
            blockers.append(f"{said}, or build the export as a draft.")
    from pipeline.fact_ledger import open_count

    if open_count(project):
        warnings.append(f"{open_count(project)} fact(s) the slides may have wrong are not "
                        "decided: the video keeps them general. Decide them on Script & "
                        "Staging, under Facts.")
    if problems["below_bar"]:
        warnings.append(f"{len(problems['below_bar'])} scene(s) pass their checks but are "
                        f"below the reviewer's bar: {_scene_list(problems['below_bar'], False)}.")
    from pipeline.scene_pictures import deck_usage

    usage = usage or deck_usage(project)
    if usage["not_shown"] and usage["shown"]:
        names = ", ".join(p["name"] for p in usage["not_shown"][:4])
        more = "..." if len(usage["not_shown"]) > 4 else ""
        warnings.append(f"{len(usage['not_shown'])} of the deck's {usage['deck_pictures']} "
                        f"pictures appear in no scene: {names}{more}.")
    stranded = script.audit([s.id for s in plan.sections])["orphaned_section_ids"]
    if stranded:
        warnings.append(
            f"{len(stranded)} piece(s) of narration are not attached to any section."
        )
    return blockers, warnings

def build_export(slug: str, draft: bool = False) -> dict[str, Any]:
    """Write the transcript, chapters and description, and list what is ready.

    Refuses nothing: a project with problems still gets its manifest, with the
    problems named in it. Withholding the files would not make the video better,
    and someone checking what is wrong needs the transcript to do it. Scenes whose
    own checks still fail make it not ready, unless it is built as a `draft`: then
    they are accepted, and the manifest says so.
    """
    from pipeline.plan_handoff import plan_for_later_stages
    project = require_project(slug)
    plan = plan_for_later_stages(project)
    from pipeline.script_handoff import script_for_later_stages
    script = script_for_later_stages(project)
    review = ReviewStore(project.root).load()

    from pipeline.scene_pictures import deck_usage

    usage = deck_usage(project)
    problems = scene_problems(project)
    draft = draft and bool(problems["failing"])
    blockers, warnings = export_readiness(project, usage, draft, problems)
    sections = _export_sections(project, plan, script)
    credits = outside_credits(project)
    from pipeline.fact_ledger import corrections_markdown

    files = write_export_files(project.root, project.name, plan.to_dict(), sections, credits,
                               corrections_markdown(project))

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
        deck_pictures={"deck": usage["deck_pictures"], "shown": usage["shown"],
                       "not_shown": [p["name"] for p in usage["not_shown"]]},
        credits=credits,
        draft=draft,
    )
    return ExportStore(project.root).save(manifest).to_dict() | {"scene_problems": problems}

def read_export(slug: str) -> dict[str, Any]:
    """The last export, with today's blockers rather than the ones it was built with."""
    project = require_project(slug)
    manifest = ExportStore(project.root).load()
    problems = scene_problems(project)
    blockers, warnings = export_readiness(project, draft=manifest.draft, problems=problems)
    return manifest.to_dict() | {
        "blockers_now": blockers,
        "warnings_now": warnings,
        "is_ready_now": not blockers,
        "scene_problems": problems,
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


def outside_credits(project) -> list[dict[str, Any]]:
    """Every outside picture any scene keeps, with its credit, for Export."""
    from pipeline.generation import VisualPlanStore
    from pipeline.scene_program import scene_folder

    found: dict[str, dict[str, Any]] = {}
    for visual in VisualPlanStore(project.root).load().visuals:
        folder = scene_folder(project, visual)
        record = folder / "sources.json" if folder else None
        if record is None or not record.exists():
            continue
        try:
            entries = json.loads(record.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for entry in entries:
            key = entry.get("page") or entry.get("title") or entry.get("file", "")
            found.setdefault(key, entry)
    return list(found.values())
