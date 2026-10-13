"""Video setup: the learners, the voice, the music and the platforms a person
chooses, and where each one reaches the video."""
# ruff: noqa: F811

import json
import shutil
import subprocess

import pytest

from pipeline import operations, video_setup
from pipeline.core import OperationFailed, require_project
from pipeline.stage_options import video_preferences
from tests.test_operations_and_clients import project_root  # noqa: F401


def test_several_learners_are_joined_into_one_audience(project_root):
    slug = operations.create_project("Learners")["slug"]
    video_setup.save(slug, {"learners": ["school", "teachers", "nobody"]})

    preferences = video_preferences(require_project(slug).root)
    audience = preferences.audience("Students in Hyderabad")

    assert audience.startswith("Students in Hyderabad")
    assert "School students (class 9-12)" in audience and "Teachers" in audience
    assert "one new term at a time" in audience, "each brings what it needs"
    assert "Serve all of them at once" in audience
    assert "nobody" not in json.dumps(video_setup.read(slug)["setup"]), "unknown is dropped"


def test_the_voice_chosen_is_the_one_scenes_and_the_render_speak_with(project_root):
    slug = operations.create_project("Voice")["slug"]
    root = require_project(slug).root
    assert video_preferences(root).voice_for("edge") == "en-US-AriaNeural", "the default"

    video_setup.save(slug, {"voice": "en-IN-NeerjaNeural", "pace": "slower"})

    assert video_preferences(root).voice_for("edge") == "en-IN-NeerjaNeural@-10%"
    video_setup.save(slug, {"voice": "hi-IN-SwaraNeural"})
    assert video_preferences(root).voice_for("edge") == "en-US-AriaNeural", \
        "a Hindi voice does not read an English video"


def test_classroom_projection_makes_every_text_larger(project_root):
    slug = operations.create_project("Classroom")["slug"]
    root = require_project(slug).root
    assert video_setup.platform_needs(root)["smallest_text_px"] == 36
    video_setup.save(slug, {"platforms": ["website", "classroom"]})
    assert video_setup.platform_needs(root)["smallest_text_px"] == 44


def test_music_is_a_built_in_bed_or_a_track_the_person_uploads(project_root):
    slug = operations.create_project("Music")["slug"]
    root = require_project(slug).root
    assert video_setup.music_for(root) == (None, 0.0), "none by default"

    with pytest.raises(OperationFailed, match="not a music file"):
        video_setup.add_music(slug, "notes.txt", b"words")
    with pytest.raises(OperationFailed, match="not in this project's music"):
        video_setup.save(slug, {"music": "upload:missing.mp3"})

    catalog = video_setup.add_music(slug, "Our theme.mp3", b"ID3 not really music")
    assert any(m["key"] == "upload:Our-theme.mp3" or m["key"].startswith("upload:Our")
               for m in catalog["catalog"]["music"])
    video_setup.save(slug, {"music": "built-in:calm", "intensity": "whisper"})
    bed, level = video_setup.music_for(root)
    assert bed is not None and bed.name == "calm.wav" and level == -30.0


@pytest.mark.skipif(not shutil.which("ffprobe"), reason="needs ffmpeg")
def test_a_render_lays_the_bed_under_the_voice_in_stereo(project_root):
    """The soundtrack was 24 kHz mono: a bed lost its width and the voice its air."""
    slug = operations.create_project("Bed Under")["slug"]
    operations.add_plan_section(slug, title="Only section", estimated_seconds=30)
    section = operations.read_artifact(slug, "plan")["sections"][0]
    operations.write_section_script(slug, section["id"], "One sentence. Two sentences.")
    video_setup.save(slug, {"music": "built-in:warm", "intensity": "soft"})

    result = operations.render_video(slug, voice_provider="silent")

    video = require_project(slug).root / result["video_path"]
    probe = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=sample_rate,channels", "-of", "json", str(video)],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    assert probe["sample_rate"] == "48000" and probe["channels"] == 2


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="needs ffmpeg")
def test_for_youtube_the_export_has_a_thumbnail_and_srt_subtitles(project_root):
    from pipeline.exporting import build_export

    slug = operations.create_project("For YouTube")["slug"]
    operations.add_plan_section(slug, title="Only section", estimated_seconds=30)
    section = operations.read_artifact(slug, "plan")["sections"][0]
    operations.write_section_script(slug, section["id"], "One sentence. Two sentences.")
    operations.render_video(slug, voice_provider="silent")
    assert not any(f["kind"] == "thumbnail" for f in build_export(slug)["files"])

    video_setup.save(slug, {"platforms": ["website", "youtube"]})
    files = build_export(slug)["files"]

    assert any(f["kind"] == "thumbnail" for f in files)
    assert any(f["name"].endswith(".srt") for f in files)
