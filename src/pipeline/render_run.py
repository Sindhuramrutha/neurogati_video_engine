"""Rendering: narration first, then everything that is measured from it.

Audio is the clock (ADR 0001). The narration is synthesised and measured, and
one timing function then drives the picture, the subtitles, the Studio timeline
and the chapter marks -- so the four cannot disagree. Everything this module
writes afterwards is derived from that one measurement.
"""

from __future__ import annotations

import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pipeline.core import OperationFailed, require_project
from pipeline.presentation import read_artifact
from pipeline.render_records import register_video_version, write_timeline_from_render
from pipeline.rendering import (
    RenderedSection,
    RenderFailed,
    RenderResult,
    render_sections,
    write_subtitles,
)
from pipeline.scripting import (
    ScriptStore,
)
from pipeline.speech import SpeechFailed, describe_voice_providers, synthesise_narration
from pipeline.stage_options import video_preferences


def list_voice_providers() -> dict[str, Any]:
    """Every text-to-speech option with its live availability."""
    return describe_voice_providers()


def pictures_for_sections(project, plan: dict) -> dict[str, list[Path]]:
    """Which of the source's pictures each plan section may show.

    A section records the content it covers -- a document and a heading within
    it -- and a picture records where it was extracted from. Matching the two is
    what makes a figure appear beside the words it belongs to instead of
    somewhere decorative.

    The Assets & Design library decides *which* pictures are worth showing;
    before it has been gathered, every extracted figure under the section's own
    headings is used. A section that records no source shows nothing rather than
    borrowing another section's diagrams.
    """
    from pipeline.assets import AssetLibraryStore
    from pipeline.extraction import BlockKind, ExtractionStore
    from pipeline.figure_prep import showable_path

    extraction = ExtractionStore(project.root).load()
    library = AssetLibraryStore(project.root).load()

    allowed: set[str] | None = None
    # The trimmed copy, where the library made one: a diagram with two inches of
    # slide background around it is drawn small on the frame, and the margin is
    # not part of the author's figure.
    prepared = {figure.asset_path: figure.prepared_path
                for figure in library.figures if figure.prepared_path}
    if library.figures:
        allowed = {figure.asset_path for figure in library.usable()}

    # Every figure, with where it came from, in extraction order.
    figures: list[tuple[str, tuple[str, ...], str]] = []
    for document in extraction.documents:
        for block in document.blocks:
            if block.kind != BlockKind.FIGURE or not block.asset_path:
                continue
            if allowed is not None and block.asset_path not in allowed:
                continue
            figures.append((document.file_name, tuple(block.heading_path), block.asset_path))

    chosen: dict[str, list[Path]] = {}
    for section in plan["sections"]:
        wanted: list[Path] = []
        for source in section.get("sources", []):
            file_name = source.get("file_name", "")
            heading = tuple(source.get("heading_path", []))
            for figure_file, figure_heading, asset_path in figures:
                if figure_file != file_name:
                    continue
                # The heading path is a location: a figure under a deeper
                # heading is inside the section, one above it is not.
                if figure_heading[:len(heading)] != heading:
                    continue
                path = showable_path(
                    project.root, asset_path, prepared.get(asset_path, ""))
                if path.exists() and path not in wanted:
                    wanted.append(path)
        chosen[section["id"]] = wanted
    return chosen



def shots_for_sections(project, plan: dict) -> dict[str, list]:
    """What Generation decided each scene shows, ready for the renderer.

    Empty when the stage has not run, and the renderer falls back to dealing the
    section's own pictures out slide by slide -- a project that never opens
    Generation still gets a video.
    """
    from pipeline.generation import VisualKind, VisualPlanStore
    from pipeline.rendering import Shot

    visuals = VisualPlanStore(project.root).load()
    if not visuals.visuals:
        return {}

    def file_at(relative: str) -> Path | None:
        if not relative:
            return None
        path = project.root / relative
        return path if path.exists() else None

    shots: dict[str, list] = {}
    for section in plan["sections"]:
        ordered = sorted(visuals.for_section(section["id"]), key=lambda v: v.scene_number)
        if not ordered:
            continue
        shots[section["id"]] = [
            Shot(
                picture=file_at(visual.asset_path),
                motion=visual.motion if visual.kind != VisualKind.TEXT else "hold",
                # An animated diagram replaces the still and its camera move.
                # The still stays on the visual, so a project whose animator is
                # gone renders the same scene held rather than not at all.
                clip=file_at(visual.clip_path),
                headline=visual.headline,
                points=list(visual.points),
                # A composed slide is already a finished frame.
                full_bleed=visual.kind == VisualKind.SLIDE,
            )
            for visual in ordered
        ]
    return shots


def render_style_for(project):
    """How the frames should be drawn: the source's look, or the app's own.

    Off unless the project asked for it on Assets & Design. A video that
    silently adopted a deck's brand colours would be making a decision that is
    not the renderer's to make.
    """
    from pipeline.assets import AssetLibraryStore
    from pipeline.rendering import DEFAULT_STYLE, RenderStyle

    library = AssetLibraryStore(project.root).load()
    if not library.look.use_source_styling:
        return DEFAULT_STYLE
    return RenderStyle.from_look(
        library.look.model_dump() | {"is_available": library.look.is_available},
        project.root,
    )


def render_video(
    slug: str, voice_provider: str = "", voice: str = ""
) -> dict[str, Any]:
    """Turn the plan and script into an actual video file.

    The order matters and is the point: **narration first, then picture.** Each
    section is synthesised, its real duration measured from the audio file, and
    only then is the picture cut to fit ([ADR 0001]). Deciding the picture from
    the plan's estimated seconds and hoping the voice matches is precisely how
    v1's animation drifted out of sync with its narration.

    Writes into `reviewing/output/`, registers the result as a version on the
    review, and returns where the file landed.
    """
    project = require_project(slug)

    plan = read_artifact(slug, "plan")
    if not plan["sections"]:
        raise OperationFailed(
            f"{project.name} has no plan sections yet, so there is nothing to render."
        )

    # The spoken text, variables filled in. The render used to take the raw body,
    # so "{{COURSE}}" reached the voice, the subtitles and the Studio timeline
    # while the review transcript showed the substituted value.
    script_document = ScriptStore(project.root).load()
    undefined_variables = script_document.audit(
        [section["id"] for section in plan["sections"]]
    )["undefined_variables"]

    chosen_provider = voice_provider or describe_voice_providers()["recommended"]


    # Every render gets its own identity. All renders used to write
    # `<slug>.mp4`, and each review version stored that one path -- so a second
    # render overwrote every earlier cut, and picking an old version in the UI
    # played the newest file. A "version" that is not immutable is not a version.
    #
    # Milliseconds, not seconds: at one-second resolution two renders started in
    # the same second shared an id, which put both cuts at the same `.mp4` path
    # and reintroduced exactly the overwrite this id exists to prevent. Short
    # projects on the silent provider render in well under a second.
    render_id = datetime.now(UTC).strftime("%Y%m%d-%H%M%S-%f")[:-3]

    output_directory = project.root / "reviewing" / "output"
    audio_directory = output_directory / "audio"
    working_directory = output_directory / "frames" / render_id

    section_pictures = pictures_for_sections(project, plan)
    section_shots = shots_for_sections(project, plan)
    style = render_style_for(project)

    sections: list[RenderedSection] = []
    warnings: list[str] = [
        f"{{{{{name}}}}} is not defined, so it is spoken as written"
        for name in undefined_variables
    ]

    # The narration was written in the project's language, so it has to be spoken
    # in it. An English voice reading Hindi is not an accent -- it is unusable
    # audio, and nothing would have said so.
    preferences = video_preferences(project.root)
    if not voice:
        voice = preferences.voice_for(chosen_provider)
    if preferences.language != "en" and not voice:
        warnings.append(
            f"The narration is written in {preferences.language_name}, but the "
            f"{chosen_provider} provider has no voice for it here, so it will be "
            f"spoken by that provider's default voice."
        )
    cursor_ms = 0

    for index, plan_section in enumerate(plan["sections"]):
        narration = script_document.spoken_text(plan_section["id"]).strip()
        section = RenderedSection(
            section_id=plan_section["id"],
            title=plan_section["title"],
            narration=narration,
            start_ms=cursor_ms,
            pictures=section_pictures.get(plan_section["id"], []),
            shots=section_shots.get(plan_section["id"], []),
            # Only the video's opening holds a title card. Every other section
            # starts speaking at once -- a card before each of them was 2.5
            # seconds of silence a section, and nothing was said in any of it.
            is_opening=index == 0,
        )

        if not narration:
            # A section with no narration still gets a card, so the gap is
            # visible in the video rather than silently skipped.
            warnings.append(f"{plan_section['title']!r} has no narration; card only")
            section.audio_duration_ms = 0
        else:
            # Named per render too: an earlier timeline still points at its own
            # narration by file name, and reusing the name would silently swap
            # the audio under it.
            audio_path = audio_directory / f"section-{index:02d}-{render_id}.mp3"
            try:
                spoken = synthesise_narration(
                    narration, audio_path, chosen_provider, voice
                )
                section.audio_path = spoken.audio_path
                section.audio_duration_ms = spoken.duration_ms
                # Where every word landed, when the voice said. The cuts and the
                # labels are timed from these rather than from a share of the
                # characters.
                section.words = spoken.words
            except SpeechFailed as speech_failure:
                raise OperationFailed(str(speech_failure)) from speech_failure

        sections.append(section)
        cursor_ms += section.total_ms

    video_path = output_directory / f"{project.slug}-{render_id}.mp4"
    subtitle_path = output_directory / f"{project.slug}-{render_id}.srt"

    try:
        render_sections(sections, working_directory, video_path, style)
        write_subtitles(sections, subtitle_path)
    except RenderFailed as render_failure:
        raise OperationFailed(str(render_failure)) from render_failure
    finally:
        # Cleaned whether or not it worked. These are intermediates -- a frame
        # and a clip per shot, plus the joined cut -- and a long video makes
        # hundreds of megabytes of them. Cleaning only on success meant a failed
        # render left all of it behind, so the next attempt had less room than
        # the one that just ran out of disk.
        shutil.rmtree(working_directory, ignore_errors=True)

    result = RenderResult(
        video_path=video_path,
        subtitle_path=subtitle_path,
        duration_ms=cursor_ms,
        provider_key=chosen_provider,
        voice=voice,
        sections=sections,
        warnings=warnings,
    )

    # The timeline first: the review's chapters are derived from the same
    # measured sections, and registering the version first meant chapters were
    # seeded before any measured data existed -- so they came from the plan's
    # estimates and pointed at 60s in a 15s video.
    timeline_note = write_timeline_from_render(project, sections, render_id)
    if timeline_note:
        result.warnings.append(timeline_note)

    chapter_note = register_video_version(project, result, render_id)
    if chapter_note:
        result.warnings.append(chapter_note)

    return result.to_dict()
