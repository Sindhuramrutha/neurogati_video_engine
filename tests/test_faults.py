"""Fault injection: each way Demo 001 stopped or degraded, made to happen again.

The run (21 slides, 43 scenes) met nine failures (docs/plans/robustness-plan.md).
Every one has a test that makes it happen and checks the job survives it:

- Edge "NoAudioReceived" stopped the run: test_resilience (edge speech is asked
  again); below, a queued render outlives a voice that drops.
- 429 from the provider: test_scene_agent (the request window is shared by every
  process); below, a scene rides out a 429 storm.
- Script drafting stalled for 75 minutes: test_resilience (backoff stops at the
  last attempt).
- A vision answer was cut off: test_resilience (a cut-off answer is not retried);
  below, a scene whose review is cut off is still made.
- The first render failed on an untested path: test_smoke (deck to export, with
  the real narration and ffmpeg paths a first render takes).
- A crashed scene showed "working" forever: test_scene_agent (a scene that stops
  on an error is failed with its reason).
- A narration failure killed a scene before round 1: below, a scene that cannot
  start is failed, with why.
- Badges and covers became scene pictures: test_scene_layout (deck pictures are
  vetted).
- Most scenes ended below the quality bar: test_scene_agent (the quality ladder).
"""
# ruff: noqa: F811

import shutil

import pytest

from pipeline import render_queue
from pipeline.llm import ModelOutputTruncated
from pipeline.scene_agent import agent_view
from pipeline.scene_maker import make_scene
from tests.test_render_job import fakes, project_root, three_sections  # noqa: F401
from tests.test_render_queue import statuses, wait_for
from tests.test_scene_agent import GOOD_VERDICT, Model, whole, wired
from tests.test_scene_lab import GOOD, scripted_project

needs_ffmpeg = pytest.mark.skipif(
    not (shutil.which("ffmpeg") and shutil.which("ffprobe")), reason="needs ffmpeg")


class NoAudioReceived(Exception):
    """What edge-tts raises when the free service drops a request."""


class RateLimited(Exception):
    """What the provider's client raises on a 429."""

    status_code = 429


@needs_ffmpeg
def test_a_scene_rides_out_a_429_storm(project_root, monkeypatch):
    slug, project, visual = scripted_project("Storm")
    model = Model(RateLimited("slow down"), RateLimited("slow down"), whole(GOOD))
    wired(monkeypatch, model, GOOD_VERDICT)

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert view["status"] == "done"
    assert sum(e["kind"] == "retry" for e in view["events"]) == 2


@needs_ffmpeg
def test_a_scene_whose_review_is_cut_off_is_still_made(project_root, monkeypatch):
    slug, project, visual = scripted_project("Cut off")
    wired(monkeypatch, Model(whole(GOOD)))

    def cut_off(folder, brief, question=""):
        raise ModelOutputTruncated("the answer stopped at the token limit")

    monkeypatch.setattr("pipeline.scene_review.review_frames", cut_off)

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert view["status"] == "done", "every check passed; only the review is missing"
    assert not view["last_render"]["reviewed"]


def test_a_queued_render_outlives_a_voice_that_drops(project_root, fakes, monkeypatch):
    """Edge dropped requests mid-run and one failure stopped the whole job."""
    from pipeline.speech import SpeechFailed

    slug, _ = three_sections("Dropped")
    real_speak = __import__("pipeline.narration_audio", fromlist=["x"]).speak_scenes
    dropped = []

    def drops_twice(*args, **kwargs):
        if len(dropped) < 2:
            dropped.append(1)
            # As Edge does it: the pipeline's error, caused by the service's.
            raise SpeechFailed("The narration could not be spoken") from NoAudioReceived(
                "No audio was received")
        return real_speak(*args, **kwargs)

    monkeypatch.setattr("pipeline.narration_audio.speak_scenes", drops_twice)
    monkeypatch.setattr(render_queue, "FIRST_WAIT_SECONDS", 0)

    render_queue.add_job(slug, "silent")
    view = wait_for(lambda v: statuses(v) == ["done"], seconds=30)

    assert len(dropped) == 2, "it waited twice and carried on, not failed"
    assert view["jobs"][0]["video_file"]


def test_a_scene_that_cannot_start_is_failed_with_why(project_root, monkeypatch):
    """Measuring the narration sat outside the scene's handling: a voice failure
    killed the scene before round 1 and left it 'working'."""
    from pipeline import scene_agent
    from pipeline.scene_lab import scene_folder
    from pipeline.scene_state import load_state

    slug, project, visual = scripted_project("No start")

    def cannot_speak(*args, **kwargs):
        raise RuntimeError("the narration could not be measured")

    monkeypatch.setattr("pipeline.scene_maker.write_brief", cannot_speak)
    scene_agent._running.add((slug, visual.id))
    scene_agent._run_safely(slug, visual.id, "", False)

    state = load_state(scene_folder(project, visual, create=True))
    assert state["status"] == "failed" and "could not be measured" in state["error"]


def test_a_clip_held_open_by_a_player_does_not_end_the_scene(tmp_path, monkeypatch):
    """Demo 003: scene 15's last clip was open in the page playing it; replacing it
    raised PermissionError and the scene ended. Now it is waited out, and if it stays
    open the round fails with the reason and the next round tries again."""
    from pathlib import Path as _Path

    from pipeline import scene_lab, scene_program

    clip = tmp_path / "render.mp4"
    clip.write_bytes(b"clip")
    tries = []

    def held(self, missing_ok=False):
        tries.append(1)
        if len(tries) < 3:
            raise PermissionError("in use")
        original(self, missing_ok=missing_ok)

    original = _Path.unlink
    monkeypatch.setattr(_Path, "unlink", held)
    assert scene_program._clear_last_clip(clip, sleep=lambda s: None)
    assert len(tries) == 3 and not clip.exists()

    monkeypatch.setattr(_Path, "unlink", lambda self, missing_ok=False: (_ for _ in ()).throw(
        PermissionError("in use")))
    assert not scene_program._clear_last_clip(clip, sleep=lambda s: None)
    monkeypatch.setattr(scene_lab, "_clear_last_clip", lambda clip: False)
    ran = scene_lab.run_script(tmp_path)
    assert ran["code"] == 1 and "open in another program" in ran["log"]
