"""What a render writes down: the Studio timeline, the version and its chapters.

Separate from making the video because it is a different kind of work. Rendering
turns a script into pixels; this turns the same measured sections into the
records that everything downstream reads -- the timeline somebody edits, the
version a comment is made against, the chapters a viewer navigates by.

All three come from the sections the renderer measured, never from the plan's
estimates, and each refuses to overwrite work somebody did by hand.
"""

from __future__ import annotations

from datetime import UTC, datetime

from pipeline.composition import Clip, ClipKind, CompositionStore
from pipeline.projects import Project
from pipeline.rendering import RenderedSection, RenderResult
from pipeline.review import ReviewStore


def write_timeline_from_render(
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

    from pipeline.composition import TrackKind, default_composition
    from pipeline.rendering import _shot_for, section_segments, shot_windows

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
        # One video clip per shot -- what is actually on screen, for as long as
        # it is on screen. A clip per section title described the render the
        # renderer used to make, not this one.
        for window in shot_windows(section):
            shot = _shot_for(section, window.segments[0])
            # Numbered, and never the section title repeated. A section of
            # seven scenes produced seven clips all reading "The McCulloch-Pitts
            # Neuron", each truncated at this width to the same single
            # character -- so the track carried no information at all. The
            # number leads because it is the part that still distinguishes them
            # once the text is cut off.
            label = section.title if window.kind == "title" else (
                f"{window.scene_index + 1}. {shot.headline}" if shot.headline
                else f"{window.scene_index + 1}. {section.title}")
            tracks_by_kind[TrackKind.VIDEO].clips.append(Clip(
                kind=ClipKind.SCENE, label=label[:80],
                # `text` stays the section's title, because that is what a
                # chapter is named after and what the preview shows behind the
                # frame. `label` is what this one clip is, which is a scene.
                text=section.title,
                start_ms=window.start_ms, duration_ms=window.duration_ms,
                section_id=section.section_id,
            ))
        for segment in section_segments(section):
            if segment.kind == "slide":
                tracks_by_kind[TrackKind.TEXT].clips.append(Clip(
                    kind=ClipKind.TEXT, label=segment.text[:40], text=segment.text,
                    start_ms=segment.start_ms, duration_ms=segment.duration_ms,
                    section_id=section.section_id,
                ))

        if section.audio_path and section.audio_duration_ms:
            tracks_by_kind[TrackKind.AUDIO].clips.append(Clip(
                kind=ClipKind.AUDIO,
                label=f"Narration - {section.title[:40]}",
                # The file name only: the studio serves narration from the render's
                # audio directory and never accepts a path.
                asset_id=section.audio_path.name,
                # Where the voice actually starts: after this section's own card,
                # which most sections no longer have.
                start_ms=section.start_ms + section.title_card_ms,
                duration_ms=section.audio_duration_ms,
                section_id=section.section_id,
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

def register_video_version(
    project: Project, result: RenderResult, render_id: str = ""
) -> str:
    """Record the render as a version on the review.

    So a comment can always say which cut it was made against -- the reason
    `VideoVersion` existed before anything could produce one.
    """

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
