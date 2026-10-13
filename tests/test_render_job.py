"""A render as a job: one at a time, halted with what it made, and resumed.

ffmpeg and the voice are replaced with fakes that write small files, so these
exercise the job -- what is kept, reused and refused -- not the encoder.
"""

import pytest

from pipeline import operations, progress, render_job, render_run
from pipeline.operations import OperationFailed
from pipeline.planning import Plan, PlanSection, PlanStore
from pipeline.render_job import RenderJobStore, job_view
from pipeline.scripting import Script, ScriptScene, ScriptStore, SectionScript
from pipeline.speech import SpeechResult


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def three_sections(name="Job"):
    slug = operations.create_project(name)["slug"]
    project = operations.require_project(slug)
    PlanStore(project.root).save(Plan(sections=[
        PlanSection(id=f"s{n}", title=f"Part {n}", estimated_seconds=10) for n in range(3)]))
    ScriptStore(project.root).save(Script(section_scripts=[
        SectionScript(section_id=f"s{n}", scenes=[ScriptScene(narration=f"Part {n} words.")])
        for n in range(3)]))
    return slug, project


@pytest.fixture
def fakes(monkeypatch):
    """Counts what was actually made, and can halt after a given section clip."""
    made = {"spoken": [], "cut": [], "halt_after_cut": None, "slug": ""}

    def speak(text, path, provider, voice):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"mp3")
        made["spoken"].append(path.name)
        return SpeechResult(audio_path=path, duration_ms=2_000, provider_key=provider,
                            voice=voice)

    def cut(ffmpeg, section, shots, durations, fade_ms, index, working):
        clip = working / f"s{index:02d}.mp4"
        clip.write_bytes(b"clip")
        made["cut"].append(index)
        if made["halt_after_cut"] == index:
            render_job.request_halt(made["slug"])
        return clip

    def join(ffmpeg, clips, working, output, music=(None, 0.0)):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"".join(clip.read_bytes() for clip in clips))

    monkeypatch.setattr(render_run, "synthesise_narration", speak)
    monkeypatch.setattr(render_run, "measure_audio_duration_ms", lambda path: 2_000)
    monkeypatch.setattr(render_run, "describe_voice_providers",
                        lambda: {"recommended": "silent"})
    monkeypatch.setattr(render_run, "write_subtitles", lambda sections, path: None)
    monkeypatch.setattr(render_run, "write_timeline_from_render", lambda *a, **k: "")
    monkeypatch.setattr(render_run, "register_video_version", lambda *a, **k: "")
    monkeypatch.setattr(render_job, "require_ffmpeg", lambda: "ffmpeg")
    monkeypatch.setattr(render_job, "_encode_shot", lambda *a, **k: a[4] / f"{k['name']}.mp4")
    monkeypatch.setattr(render_job, "_cut_section", cut)
    monkeypatch.setattr(render_job, "_join_and_level", join)
    return made


def test_a_halted_render_keeps_what_it_made_and_joins_it_for_watching(project_root, fakes):
    slug, project = three_sections()
    fakes.update(slug=slug, halt_after_cut=0)

    result = render_run.render_video(slug)

    assert result["halted"] is True
    job = result["job"]
    assert job["status"] == "halted" and job["spoken"] == 3 and job["cut"] == 1
    assert job["can_resume"] is True
    assert job["partial_video"].endswith("-so-far.mp4")
    assert (project.root / "reviewing" / "output" / job["partial_video"]).read_bytes() == b"clip"
    assert not progress.read(slug, "render")["active"], "a halted render is not running"


def test_continuing_reuses_every_narration_and_clip_already_made(project_root, fakes):
    slug, project = three_sections("Resume")
    fakes.update(slug=slug, halt_after_cut=1)
    halted = render_run.render_video(slug)["job"]
    fakes.update(spoken=[], cut=[], halt_after_cut=None)

    render_run.render_video(slug, resume=True)

    assert fakes["spoken"] == [], "narration already made is not paid for again"
    assert fakes["cut"] == [2], "only the section not yet drawn is drawn"
    record = RenderJobStore(project.root).load()
    assert record.status == "done" and record.render_id == halted["render_id"]
    assert (project.root / "reviewing" / "output" / f"{slug}-{halted['render_id']}.mp4").exists()
    assert not (project.root / "reviewing" / "output" / halted["partial_video"]).exists()
    assert not render_job.working_directory(project, halted["render_id"]).exists()


def test_continuing_after_the_script_changed_is_refused(project_root, fakes):
    """It would put two versions of the narration in one video."""
    slug, project = three_sections("Changed")
    fakes.update(slug=slug, halt_after_cut=0)
    render_run.render_video(slug)
    script = ScriptStore(project.root).load()
    script.section_scripts[2].scenes[0].narration = "Different words now."
    ScriptStore(project.root).save(script)

    with pytest.raises(OperationFailed, match="changed since"):
        render_run.render_video(slug, resume=True)


def test_a_second_render_is_refused_while_one_runs(project_root, fakes):
    slug, _ = three_sections("Twice")
    assert progress.claim(slug, "render")
    try:
        with pytest.raises(OperationFailed, match="already running"):
            render_run.render_video(slug)
    finally:
        progress.finish(slug, "render")


def test_a_render_left_running_by_a_stopped_server_is_offered_to_continue(project_root, fakes):
    slug, project = three_sections("Interrupted")
    fakes.update(slug=slug, halt_after_cut=0)
    render_run.render_video(slug)
    record = RenderJobStore(project.root).load()
    record.status = "running"                 # what a killed server leaves behind
    RenderJobStore(project.root).save(record)

    view = job_view(slug)
    assert view["status"] == "interrupted" and view["can_resume"] is True


def test_starting_over_throws_the_stopped_render_away(project_root, fakes):
    slug, project = three_sections("Over")
    fakes.update(slug=slug, halt_after_cut=0)
    first = render_run.render_video(slug)["job"]
    fakes.update(halt_after_cut=None)

    render_run.render_video(slug)

    assert not render_job.working_directory(project, first["render_id"]).exists()
    assert RenderJobStore(project.root).load().render_id != first["render_id"]


def test_discarding_removes_the_working_files_and_the_preview(project_root, fakes):
    slug, project = three_sections("Discard")
    fakes.update(slug=slug, halt_after_cut=0)
    halted = render_run.render_video(slug)["job"]

    view = render_job.discard(slug)

    assert view["status"] == "" and view["can_resume"] is False
    assert not render_job.working_directory(project, halted["render_id"]).exists()
    assert not (project.root / "reviewing" / "output" / halted["partial_video"]).exists()


def test_halting_with_nothing_running_is_refused(project_root):
    slug, _ = three_sections("Idle")
    with pytest.raises(OperationFailed, match="No render"):
        render_job.request_halt(slug)


def test_stop_and_delete_throws_the_render_away(project_root, fakes, monkeypatch):
    slug, project = three_sections("Delete")
    fakes.update(slug=slug)

    def cut_then_delete(ffmpeg, section, shots, durations, fade_ms, index, working):
        clip = working / f"s{index:02d}.mp4"
        clip.write_bytes(b"clip")
        render_job.request_halt(slug, discard=True)
        return clip

    monkeypatch.setattr(render_job, "_cut_section", cut_then_delete)
    result = render_run.render_video(slug)

    assert result["discarded"] is True and result["job"]["status"] == ""
    output = project.root / "reviewing" / "output"
    assert not list((output / "frames").glob("*")), "no working files left"
    assert not list((output / "audio").glob("*")), "nor the narration it made"


def test_continuing_uses_the_voice_the_render_started_in(project_root, fakes):
    """The Continue button sends no voice; the default one is a different voice,
    which made every continue look like a changed render and be refused."""
    slug, project = three_sections("Voice")
    fakes.update(slug=slug, halt_after_cut=0)
    render_run.render_video(slug, voice_provider="another-voice")
    fakes.update(halt_after_cut=None)

    render_run.render_video(slug, resume=True)

    record = RenderJobStore(project.root).load()
    assert record.status == "done" and record.voice_provider == "another-voice"
