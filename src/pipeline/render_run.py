"""Rendering: narration first, then everything that is measured from it.

Audio is the clock (ADR 0001). The narration is synthesised and measured, and
one timing function then drives the picture, the subtitles, the Studio timeline
and the chapter marks -- so the four cannot disagree. Everything this module
writes afterwards is derived from that one measurement.
"""

from __future__ import annotations

import shutil
from datetime import UTC, datetime
from typing import Any

from pipeline.composition import Clip, ClipKind, CompositionStore
from pipeline.core import OperationFailed, require_project
from pipeline.presentation import read_artifact
from pipeline.projects import Project
from pipeline.rendering import (
    TITLE_CARD_MS,
    RenderedSection,
    RenderFailed,
    RenderResult,
    render_sections,
    write_subtitles,
)
from pipeline.review import (
    ReviewStore,
)
from pipeline.scripting import (
    ScriptStore,
)
from pipeline.speech import SpeechFailed, describe_voice_providers, synthesise_narration


def list_voice_providers() -> dict[str, Any]:
    """Every text-to-speech option with its live availability."""
    return describe_voice_providers()

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

    sections: list[RenderedSection] = []
    warnings: list[str] = [
        f"{{{{{name}}}}} is not defined, so it is spoken as written"
        for name in undefined_variables
    ]
    cursor_ms = 0

    for index, plan_section in enumerate(plan["sections"]):
        narration = script_document.spoken_text(plan_section["id"]).strip()
        section = RenderedSection(
            section_id=plan_section["id"],
            title=plan_section["title"],
            narration=narration,
            start_ms=cursor_ms,
        )

        if not narration:
            # A section with no narration still gets its title card, so the gap
            # is visible in the video rather than silently skipped.
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
            except SpeechFailed as speech_failure:
                raise OperationFailed(str(speech_failure)) from speech_failure

        sections.append(section)
        cursor_ms += section.total_ms

    video_path = output_directory / f"{project.slug}-{render_id}.mp4"
    subtitle_path = output_directory / f"{project.slug}-{render_id}.srt"

    try:
        render_sections(sections, working_directory, video_path)
        write_subtitles(sections, subtitle_path)
    except RenderFailed as render_failure:
        raise OperationFailed(str(render_failure)) from render_failure

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
    timeline_note = _write_timeline_from_render(project, sections, render_id)
    if timeline_note:
        result.warnings.append(timeline_note)

    chapter_note = _register_video_version(project, result, render_id)
    if chapter_note:
        result.warnings.append(chapter_note)

    # The frames are intermediates; only the video, its audio and its subtitles
    # are worth keeping per render.
    shutil.rmtree(working_directory, ignore_errors=True)
    return result.to_dict()

def _write_timeline_from_render(
    project: Project, sections: list[RenderedSection], render_id: str = ""
) -> str:
    """Put the render's structure on the Studio timeline, from the same segments
    the video was cut to -- so what Studio shows is what the file contains.

    Title cards go on the video track, narration slides on the text track, and
    each section's narration audio on the audio track at its real, measured
    offset. Returns a note when it deliberately does nothing.

    **Never over hand-made clips.** It replaces a timeline only when it is empty
    or was written by an earlier render. Anything else is someone's editing, and
    replacing it to display the renderer's output would destroy their work.
    """
    from datetime import UTC, datetime

    from pipeline.composition import TrackKind, default_composition
    from pipeline.rendering import section_segments

    store = CompositionStore(project.root)
    existing = store.load()
    existing_clip_count = sum(len(track.clips) for track in existing.tracks)

    if existing_clip_count:
        was_generated = bool(existing.generated_from_render_at)
        # The fingerprint is what makes this safe. An edit round-trips the whole
        # document through the API, marker included, so the marker alone said
        # "generated" for a timeline the user had just edited by hand.
        is_untouched = existing.generated_fingerprint == existing.fingerprint()

        if was_generated and not existing.generated_fingerprint:
            # Written by a version that recorded no fingerprint, so whether it
            # has since been edited is unknowable. Left alone, and said plainly:
            # telling someone they made edits they did not make is its own bug.
            return (
                "The Studio timeline was built by an earlier version that kept no "
                "record of its contents, so it was left as it is. Delete its clips "
                "to have a render rebuild it."
            )

        if not (was_generated and is_untouched):
            return (
                "The Studio timeline has your own edits, so it was not replaced "
                "with the render's structure. Delete the clips to have a render "
                "rebuild it."
            )

    composition = default_composition()
    tracks_by_kind = {track.kind: track for track in composition.tracks}

    for section in sections:
        for segment in section_segments(section):
            if segment.kind == "title":
                tracks_by_kind[TrackKind.VIDEO].clips.append(Clip(
                    kind=ClipKind.SCENE, label=segment.text[:80], text=segment.text,
                    start_ms=segment.start_ms, duration_ms=segment.duration_ms,
                ))
            else:
                tracks_by_kind[TrackKind.TEXT].clips.append(Clip(
                    kind=ClipKind.TEXT, label=segment.text[:40], text=segment.text,
                    start_ms=segment.start_ms, duration_ms=segment.duration_ms,
                ))

        if section.audio_path and section.audio_duration_ms:
            tracks_by_kind[TrackKind.AUDIO].clips.append(Clip(
                kind=ClipKind.AUDIO,
                label=f"Narration - {section.title[:40]}",
                # The file name only: the studio serves narration from the render's
                # audio directory and never accepts a path.
                asset_id=section.audio_path.name,
                start_ms=section.start_ms + TITLE_CARD_MS,
                duration_ms=section.audio_duration_ms,
            ))

    composition.generated_from_render_at = (
        render_id or datetime.now(UTC).isoformat(timespec="seconds")
    )
    composition.generated_fingerprint = composition.fingerprint()
    store.save(composition)
    return ""

def chapters_from_sections(sections: list[RenderedSection]) -> list:
    """Chapter marks straight from the rendered sections.

    Measured, and independent of anything else having been written yet -- which
    is the point: deriving them from the timeline meant the first render seeded
    chapters before the timeline existed and silently fell back to the plan's
    estimates.
    """
    from pipeline.review import Chapter

    return [
        Chapter(title=section.title, start_ms=section.start_ms) for section in sections
    ]

def _register_video_version(
    project: Project, result: RenderResult, render_id: str = ""
) -> str:
    """Record the render as a version on the review.

    So a comment can always say which cut it was made against -- the reason
    `VideoVersion` existed before anything could produce one.
    """
    from datetime import UTC, datetime

    from pipeline.review import VideoVersion

    store = ReviewStore(project.root)
    review = store.load()
    version = VideoVersion(
        label=f"Render {datetime.now(UTC).strftime('%Y-%m-%d %H:%M')}",
        notes=f"{result.provider_key} voice, {len(result.sections)} section(s)",
        duration_ms=result.duration_ms,
        file_path=str(result.video_path),
    )
    review.versions.append(version)
    review.active_version_id = version.id

    measured = chapters_from_sections(result.sections)
    was_generated = bool(review.chapters_generated_from_render_at)
    note = ""

    if not review.chapters or was_generated:
        # Ours to correct: either there are none, or the last render wrote them
        # and nobody has edited them since (an edit clears the marker).
        review.chapters = measured
        review.chapters_generated_from_render_at = (
            render_id or datetime.now(UTC).isoformat(timespec="seconds")
        )
    elif [c.start_ms for c in review.chapters] != [c.start_ms for c in measured]:
        note = (
            "Your chapter marks do not match this render. Use Rebuild chapters "
            "to move them to the new timings."
        )

    store.save(review)
    return note
