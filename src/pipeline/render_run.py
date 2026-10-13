"""Rendering: narration first, then everything that is measured from it.

Audio is the clock. The narration is synthesised and measured, and
one timing function then drives the picture, the subtitles, the Studio timeline
and the chapter marks -- so the four cannot disagree. Everything this module
writes afterwards is derived from that one measurement.
"""

from __future__ import annotations

import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pipeline import progress, project_work, upstream
from pipeline.core import OperationFailed, require_project
from pipeline.render_job import (
    JOB,
    UNFINISHED,
    RenderHalted,
    RenderJob,
    RenderJobStore,
    check_halt,
    clear_halt,
    cut_sections,
    fingerprint,
    job_view,
    join_clips,
    join_what_is_done,
    output_directory,
    remove_leftovers,
    save,
    working_directory,
)
from pipeline.render_job import (
    now as job_now,
)
from pipeline.render_records import register_video_version, write_timeline_from_render
from pipeline.rendering import (
    RenderedSection,
    RenderFailed,
    RenderResult,
    write_subtitles,
)
from pipeline.speech import (
    SpeechFailed,
    describe_voice_providers,
    load_word_timings,
    measure_audio_duration_ms,
    synthesise_narration,
)
from pipeline.stage_options import video_preferences


def list_voice_providers() -> dict[str, Any]:
    """Every text-to-speech option with its live availability."""
    return describe_voice_providers()


def pictures_for_sections(project, plan: dict) -> dict[str, list[Path]]:
    """The pictures each plan section shows: the ones the plan attached to it,
    from the Assets & Design transfer the plan carries (`plan_pictures.py`).

    Nothing here reads Assets & Design: what reaches the video is decided there,
    attached to sections in the plan, and handed on with it. A section with no
    pictures attached shows none rather than borrowing another section's.
    """
    from pipeline.figure_prep import showable_path
    from pipeline.plan_pictures import assets_for_later_stages, pictures_of
    from pipeline.planning import Plan

    library = assets_for_later_stages(project).library
    whole = Plan.model_validate({"sections": plan["sections"],
                                 "pictures_from": plan.get("pictures_from", "")})
    chosen: dict[str, list[Path]] = {}
    for section in whole.sections:
        wanted: list[Path] = []
        for figure in pictures_of(section, whole, library):
            # The trimmed copy, where the library made one: the margin around a
            # diagram is not part of the author's figure.
            path = showable_path(project.root, figure.asset_path,
                                 "" if figure.use_original else figure.prepared_path)
            if path.exists() and path not in wanted:
                wanted.append(path)
        chosen[section.id] = wanted
    return chosen



def shots_for_sections(project, plan: dict) -> dict[str, list]:
    """Each scene's program clip, ready for the renderer.

    Empty when the stage has not run, and the renderer falls back to dealing the
    section's own pictures out slide by slide -- a project that never opens
    Generation still gets a video.
    """
    from pipeline.generation_handoff import visuals_for_later_stages
    from pipeline.rendering import Shot

    # What Generation transferred, not what it is still making.
    visuals = visuals_for_later_stages(project)
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
                clip=file_at(visual.clip_path),
                headline=visual.headline,
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
    from pipeline.plan_pictures import assets_for_later_stages
    from pipeline.project_look import style_for
    from pipeline.rendering import DEFAULT_STYLE

    # The look the transferred plan carried on from Assets & Design.
    library = assets_for_later_stages(project).library
    if not library.look.use_source_styling:
        return DEFAULT_STYLE
    return style_for(library.look, project.root)


def render_video(
    slug: str, voice_provider: str = "", voice: str = "", resume: bool = False,
) -> dict[str, Any]:
    """Render the video as a job (`render_job`): one at a time, stopped at a
    section boundary when asked, and continued from where it stopped."""
    if not progress.claim(slug, JOB, "Starting the render"):
        raise OperationFailed(
            "A render of this project is already running. Halt it, or wait for it "
            "to finish -- two at once make both several times slower.")
    clear_halt(slug)
    try:
        with project_work.working_on(slug):
            return _render_video(slug, voice_provider, voice, resume)
    finally:
        clear_halt(slug)
        progress.finish(slug, JOB)


def _render_video(slug: str, voice_provider: str, voice: str, resume: bool) -> dict[str, Any]:
    """Turn the plan and script into an actual video file.

    The order matters and is the point: **narration first, then picture.** Each
    section is synthesised, its real duration measured from the audio file, and
    only then is the picture cut to fit. Deciding the picture from
    the plan's estimated seconds and hoping the voice matches is how animation
    drifts out of sync with narration.

    Writes into `reviewing/output/`, registers the result as a version on the
    review, and returns where the file landed -- or, halted, what it had made.
    """
    project = require_project(slug)

    from pipeline.plan_handoff import plan_for_later_stages

    plan = plan_for_later_stages(project).model_dump(mode="json")
    if not plan["sections"]:
        raise OperationFailed(
            f"{project.name} has no plan sections yet, so there is nothing to render."
        )
    # Every scene is a program that passed its checks and was approved. Nothing
    # falls back to a still with the voice over it.
    from pipeline.generation_handoff import visuals_for_later_stages
    from pipeline.scene_approval import render_blockers
    blockers = render_blockers(visuals_for_later_stages(project).visuals)
    if blockers:
        raise OperationFailed(
            f"{len(blockers)} scene(s) cannot be rendered yet: " + "; ".join(blockers[:8])
            + ("; …" if len(blockers) > 8 else "")
            + ". Make, check and approve each scene's program on Generation, then transfer.")

    # The spoken text, variables filled in. The raw body would let "{{COURSE}}" reach
    # the voice, the subtitles and the Studio timeline while the review transcript
    # showed the substituted value.
    from pipeline.script_handoff import script_for_later_stages
    script_document = script_for_later_stages(project)
    undefined_variables = script_document.audit(
        [section["id"] for section in plan["sections"]]
    )["undefined_variables"]

    store = RenderJobStore(project.root)
    previous = store.load()
    if resume and not voice_provider:
        # Continued in the voice it started in: a different one would be both a
        # changed render and two voices in one video.
        voice_provider, voice = previous.voice_provider, voice or previous.voice
    chosen_provider = voice_provider or describe_voice_providers()["recommended"]
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

    section_pictures = pictures_for_sections(project, plan)
    section_shots = shots_for_sections(project, plan)
    style = render_style_for(project)
    from pipeline.plan_pictures import assets_for_later_stages
    brand = assets_for_later_stages(project).brand
    narrations = [script_document.spoken_text(s["id"]).strip() for s in plan["sections"]]
    made_from = fingerprint(plan["sections"], narrations, chosen_provider, voice,
                            section_pictures, section_shots, style,
                            *([brand.model_dump()] if not brand.is_empty else []))

    if resume:
        job = _job_to_resume(project, previous, made_from)
    else:
        # A fresh start replaces an unfinished render rather than keeping both.
        if previous.status in UNFINISHED:
            remove_leftovers(project, previous)
        # Every render gets its own identity, so a second render never overwrites an
        # earlier cut. Milliseconds, so two renders a second apart do not share one.
        job = RenderJob(
            render_id=datetime.now(UTC).strftime("%Y%m%d-%H%M%S-%f")[:-3],
            started_at=job_now(), fingerprint=made_from, voice_provider=chosen_provider,
            voice=voice, section_count=len(plan["sections"]),
        )
    job.status, job.message = "running", ""
    render_id = job.render_id
    count = job.section_count

    audio_directory = output_directory(project) / "audio"
    working = working_directory(project, render_id)
    video_path = output_directory(project) / f"{project.slug}-{render_id}.mp4"
    subtitle_path = output_directory(project) / f"{project.slug}-{render_id}.srt"
    sections: list[RenderedSection] = []
    # The lesson starts after the intro, so the subtitles, the timeline and the
    # chapters are measured on the video as it plays.
    cursor_ms = brand.lesson_starts_at_ms

    def before_picture(index: int) -> None:
        check_halt(slug)
        save(project, job, f"Drawing section {index + 1} of {count}: {sections[index].title}")

    def after_picture(index: int) -> None:
        job.cut = max(job.cut, index + 1)
        save(project, job, f"Drew section {index + 1} of {count}")

    try:
        for index, plan_section in enumerate(plan["sections"]):
            check_halt(slug)
            save(project, job, f"Speaking section {index + 1} of {count}: {plan_section['title']}")
            section = RenderedSection(
                section_id=plan_section["id"],
                title=plan_section["title"],
                narration=narrations[index],
                start_ms=cursor_ms,
                pictures=section_pictures.get(plan_section["id"], []),
                shots=section_shots.get(plan_section["id"], []),
                # Only the video's opening holds a title card. Every other section
                # starts speaking at once -- a card before each of them was 2.5
                # seconds of silence a section, and nothing was said in any of it.
                is_opening=index == 0,
            )
            if not section.narration:
                # A section with no narration still gets a card, so the gap is
                # visible in the video rather than silently skipped.
                warnings.append(f"{plan_section['title']!r} has no narration; card only")
                section.audio_duration_ms = 0
            else:
                # Named per render: an earlier timeline still points at its own
                # narration by file name, and reusing the name would swap the
                # audio under it. A resumed render reuses its own, unpaid for.
                audio_path = audio_directory / f"section-{index:02d}-{render_id}.mp3"
                _speak(section, audio_path, reuse=index < job.spoken,
                       provider=chosen_provider, voice=voice)
            sections.append(section)
            cursor_ms += section.total_ms
            job.spoken = max(job.spoken, index + 1)

        clips = cut_sections(sections, working, style=style, reuse=job.cut,
                             before=before_picture, after=after_picture)
        check_halt(slug)
        save(project, job, "Joining the sections into one video")
        join_clips(clips, working, video_path, project.root)
        if not brand.is_empty:
            from pipeline.render_brand import apply_brand
            save(project, job, "Putting on the brand assets")
            apply_brand(brand, project.root, video_path, working)
        write_subtitles(sections, subtitle_path)
    except RenderHalted as halt:
        if halt.discard:
            remove_leftovers(project, job)
            store.save(RenderJob())
            return {"halted": True, "discarded": True, "job": job_view(slug)}
        return _halted(project, job)
    except (RenderFailed, OperationFailed) as failure:
        # Kept, not cleaned: what was made is what a continue starts from.
        # Discarding the render removes it.
        job.status, job.message = "failed", str(failure)
        save(project, job)
        raise OperationFailed(str(failure)) from failure

    # Finished: the working files are intermediates, a frame and a clip per
    # shot, and a long video makes hundreds of megabytes of them.
    shutil.rmtree(working, ignore_errors=True)
    if job.partial_video:
        (project.root / job.partial_video).unlink(missing_ok=True)
    job.status, job.partial_video = "done", ""
    save(project, job)
    upstream.record(project, "render")

    result = RenderResult(
        video_path=video_path,
        subtitle_path=subtitle_path,
        duration_ms=brand.total_ms(cursor_ms - brand.lesson_starts_at_ms),
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


def _job_to_resume(project, previous: RenderJob, made_from: str) -> RenderJob:
    """The stopped render to continue, if it can be continued."""
    if previous.status not in UNFINISHED or not previous.render_id \
            or not working_directory(project, previous.render_id).exists():
        raise OperationFailed("There is no stopped render to continue. Start a new one.")
    if previous.fingerprint != made_from:
        raise OperationFailed(
            "The plan, script, voice or pictures changed since that render stopped, "
            "so continuing it would mix two versions in one video. Start over instead.")
    if previous.partial_video:
        (project.root / previous.partial_video).unlink(missing_ok=True)
        previous.partial_video = ""
    return previous


def _speak(section: RenderedSection, audio_path, *, reuse: bool, provider: str,
           voice: str) -> None:
    """Give a section its narration: the one already made, or a new one."""
    if reuse and audio_path.exists():
        section.audio_path = audio_path
        section.audio_duration_ms = measure_audio_duration_ms(audio_path)
        section.words = load_word_timings(audio_path)
        return
    try:
        spoken = synthesise_narration(section.narration, audio_path, provider, voice)
    except SpeechFailed as speech_failure:
        raise OperationFailed(str(speech_failure)) from speech_failure
    section.audio_path = spoken.audio_path
    section.audio_duration_ms = spoken.duration_ms
    # Where every word landed, when the voice said. The cuts and the labels
    # are timed from these rather than from a share of the characters.
    section.words = spoken.words


def _halted(project, job: RenderJob) -> dict[str, Any]:
    """Stopped on request: join what is finished so it can be watched."""
    job.status = "halted"
    save(project, job)
    progress.report(project.slug, JOB, 0, 0, "Halting: joining what is done so far")
    try:
        job.partial_video = join_what_is_done(project, job)
    except RenderFailed as join_failure:
        job.message = f"What was done could not be joined for watching: {join_failure}"
    save(project, job)
    return {"halted": True, "job": job_view(project.slug)}
