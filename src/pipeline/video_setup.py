"""Video setup: who the video is for, the voice that speaks it, the music under it,
and where it will be watched -- chosen once per project, on the Scene Plan's setup.

- **Learners**, several at once. Each brings its own teaching guidance, and the
  ones chosen are joined into one description that the planner, the script
  writer, the scene maker and the reviewer all read (`audience_text`).
- **Voice** and its pace, with a sample of each to hear before choosing. The voice
  chosen here is the one scenes are measured with and the render speaks with, so
  the two can never differ.
- **Music**: none, a built-in bed (made here, in code, so it is free to use), or a
  track the person uploads; how loud it sits under the voice; a sample of it alone
  and under the chosen voice.
- **Platforms**: the website, YouTube, a classroom projector. Each changes what
  the video and its hand-over need (`platform_needs`).

Kept at projects/<slug>/settings/video.json.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

from pipeline.config import REPO_ROOT
from pipeline.core import OperationFailed, require_project
from pipeline.storage.documents import read_json_object, write_text_atomically

CACHE = REPO_ROOT / ".cache"
SAMPLE_RATE = 48000
MUSIC_SUFFIXES = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}
LARGEST_MUSIC_BYTES = 40 * 1024 * 1024


@dataclass(frozen=True)
class Learners:
    key: str
    label: str
    guidance: str


LEARNERS = (
    Learners("school", "School students (class 9-12)",
             "Everyday words; one new term at a time, always explained; short sentences; "
             "examples from daily life."),
    Learners("college", "College students",
             "Standard terms, each defined once; explain why as well as what; connect each "
             "idea to the one before."),
    Learners("advanced", "Postgraduates and researchers",
             "Precise terms and a brisker pace; name methods and evidence; little "
             "repetition."),
    Learners("teachers", "Teachers",
             "A clear structure a teacher could reuse in class; say each section's key "
             "takeaway plainly."),
    Learners("health", "Medical and health learners",
             "Connect ideas to the body and to what a clinician would see, where the "
             "source does."),
    Learners("engineering", "Engineering and computing learners",
             "Connect ideas to signals, systems and computation, where the source does."),
    Learners("general", "Curious general audience",
             "Story-led and warm; no background assumed; everyday comparisons."),
)


@dataclass(frozen=True)
class Voice:
    key: str            # the Edge voice
    name: str
    accent: str
    gender: str
    language: str


VOICES = (
    Voice("en-IN-NeerjaNeural", "Neerja", "Indian English", "female", "en"),
    Voice("en-IN-PrabhatNeural", "Prabhat", "Indian English", "male", "en"),
    Voice("en-US-AvaNeural", "Ava", "US English", "female", "en"),
    Voice("en-US-AndrewNeural", "Andrew", "US English", "male", "en"),
    Voice("en-US-AriaNeural", "Aria", "US English", "female", "en"),
    Voice("en-GB-SoniaNeural", "Sonia", "British English", "female", "en"),
    Voice("en-GB-RyanNeural", "Ryan", "British English", "male", "en"),
    Voice("hi-IN-SwaraNeural", "Swara", "Hindi", "female", "hi"),
    Voice("hi-IN-MadhurNeural", "Madhur", "Hindi", "male", "hi"),
    Voice("te-IN-ShrutiNeural", "Shruti", "Telugu", "female", "te"),
    Voice("te-IN-MohanNeural", "Mohan", "Telugu", "male", "te"),
)
PACES = {"slower": "-10%", "normal": "+0%", "faster": "+10%"}
SAMPLE_WORDS = {
    "en": "Hello, I'll be your guide through this lesson. By the eighteenth century, "
          "scientists began to realise that life was not only chemical. It was also "
          "electrical.",
    "hi": "नमस्ते, इस पाठ में मैं आपकी मार्गदर्शक रहूँगी। अठारहवीं सदी तक वैज्ञानिक समझने "
          "लगे थे कि जीवन केवल रासायनिक नहीं, बल्कि विद्युत भी है।",
    "te": "నమస్కారం, ఈ పాఠంలో నేను మీకు మార్గదర్శిగా ఉంటాను. పద్దెనిమిదవ శతాబ్దానికి, జీవం "
          "రసాయనికమే కాదు, విద్యుత్ కూడా అని శాస్త్రవేత్తలు గ్రహించడం మొదలుపెట్టారు.",
}

# How loud the bed sits under the voice, before it ducks further while the voice speaks.
INTENSITIES = {"whisper": -30.0, "soft": -24.0, "present": -18.0}
BUILT_IN_MUSIC = {
    "calm": "Calm pad: slow, soft chords",
    "focus": "Gentle pulse: a quiet, steady arpeggio",
    "warm": "Warm keys: soft piano-like chords",
}
PLATFORMS = {
    "website": "Your website or LMS: subtitles as a file the player loads (WebVTT).",
    "youtube": "YouTube: chapter marks, a description and a thumbnail to upload with it.",
    "classroom": "Classroom projection: larger text everywhere, so the back row can read.",
}


class VideoSetup(BaseModel):
    learners: list[str] = Field(default_factory=list)
    voice: str = ""                 # empty: the language's default voice
    pace: str = "normal"
    music: str = "none"             # none | built-in:<key> | upload:<file name>
    intensity: str = "soft"
    platforms: list[str] = Field(default_factory=lambda: ["website"])
    # A name the voice says wrong, and how to spell it so it says it right.
    sounds: dict[str, str] = Field(default_factory=dict)

    @field_validator("sounds")
    @classmethod
    def _tidy_sounds(cls, value: dict[str, str]) -> dict[str, str]:
        tidy = {str(k).strip()[:60]: str(v).strip()[:80] for k, v in value.items()}
        return dict(list({k: v for k, v in tidy.items() if k and v}.items())[:200])

    @field_validator("learners")
    @classmethod
    def _known_learners(cls, value: list[str]) -> list[str]:
        known = {learner.key for learner in LEARNERS}
        return list(dict.fromkeys(v for v in value if v in known))

    @field_validator("platforms")
    @classmethod
    def _known_platforms(cls, value: list[str]) -> list[str]:
        return list(dict.fromkeys(v for v in value if v in PLATFORMS))

    @field_validator("pace")
    @classmethod
    def _known_pace(cls, value: str) -> str:
        return value if value in PACES else "normal"

    @field_validator("intensity")
    @classmethod
    def _known_intensity(cls, value: str) -> str:
        return value if value in INTENSITIES else "soft"

    @field_validator("voice")
    @classmethod
    def _known_voice(cls, value: str) -> str:
        return value if value in {v.key for v in VOICES} else ""


def _path(project_root: Path) -> Path:
    return project_root / "settings" / "video.json"


def load(project_root: Path) -> VideoSetup:
    saved = read_json_object(_path(project_root), "video setup") or {}
    return VideoSetup.model_validate(saved)


def save(slug: str, changes: dict[str, Any]) -> dict[str, Any]:
    project = require_project(slug)
    setup = VideoSetup.model_validate(load(project.root).model_dump() | changes)
    if setup.music.startswith("upload:") and not _upload(project.root, setup.music[7:]):
        raise OperationFailed("That music file is not in this project's music.")
    write_text_atomically(_path(project.root), setup.model_dump_json(indent=1))
    return read(slug)


def read(slug: str) -> dict[str, Any]:
    """The setup, and everything the page offers to choose from."""
    from pipeline.stage_options import StageSettingsStore
    from pipeline.stages import Stage

    project = require_project(slug)
    setup = load(project.root)
    language = str(StageSettingsStore(project.root).load(Stage.SCENE_PLAN).values.get(
        "language", "en"))
    return {"setup": setup.model_dump(), "language": language, "catalog": {
        "learners": [vars(learner) for learner in LEARNERS],
        # Only voices that speak the video's language: a Telugu voice cannot read English.
        "voices": [vars(voice) for voice in VOICES if voice.language == language],
        "paces": list(PACES),
        "intensities": list(INTENSITIES),
        "music": [{"key": f"built-in:{key}", "label": label} for key, label
                  in BUILT_IN_MUSIC.items()]
        + [{"key": f"upload:{path.name}", "label": f"Your track: {path.name}"}
           for path in _uploads(project.root)],
        "platforms": [{"key": key, "label": text} for key, text in PLATFORMS.items()],
    }}


# --- what the rest of the pipeline reads ------------------------------------------------


def audience_text(project_root: Path, written: str = "") -> str:
    """The learners chosen, joined into one description, with what each needs --
    and the person's own words, when there are any."""
    chosen = [learner for learner in LEARNERS if learner.key in load(project_root).learners]
    parts = [written.strip()] if written.strip() else []
    if chosen:
        parts.append("For: " + "; ".join(learner.label for learner in chosen) + ".")
        parts += [f"- {learner.label}: {learner.guidance}" for learner in chosen]
        if len(chosen) > 1:
            parts.append("Serve all of them at once: the simplest wording that is still "
                         "precise, every term defined, the depth the most advanced needs.")
    return "\n".join(parts)


def edge_voice(project_root: Path, language: str) -> str:
    """The voice chosen for this language, with its pace (`voice@rate`), or empty
    when none is chosen for it."""
    setup = load(project_root)
    voice = next((v for v in VOICES if v.key == setup.voice and v.language == language), None)
    if voice is None:
        return ""
    rate = PACES[setup.pace]
    return voice.key if rate == "+0%" else f"{voice.key}@{rate}"


def pronunciations(project_root: Path) -> dict[str, str]:
    return load(project_root).sounds


class Suggested(BaseModel):
    words: list[dict[str, str]] = Field(
        default_factory=list,
        description="Each a name or term a text-to-speech voice is likely to say wrong: "
                    "{\"word\": as written, \"say\": a plain respelling that makes the "
                    "voice say it right, e.g. \"Loewi\" -> \"Lervee\"}.")


def suggest_pronunciations(slug: str) -> dict[str, Any]:
    """Read the script once and propose respellings for the names and terms a
    voice is likely to say wrong (AI, one call). Kept beside the person's own;
    a word they already set is never changed."""
    from pipeline.llm import ModelCallFailed, ModelNotConfigured, complete_structured
    from pipeline.script_handoff import script_for_later_stages
    from pipeline.stage_options import video_preferences

    project = require_project(slug)
    script = script_for_later_stages(project)
    spoken = "\n\n".join(script.spoken_text(entry.section_id)
                         for entry in script.section_scripts)[:20000]
    if not spoken.strip():
        raise OperationFailed("There is no script yet to find names in.")
    preferences = video_preferences(project.root)
    try:
        answer = _ask_for_sounds(complete_structured, preferences, spoken)
    except (ModelCallFailed, ModelNotConfigured) as failure:
        raise OperationFailed(f"The model could not suggest them: {failure}") from failure
    setup = load(project.root)
    for item in answer.words:
        word, say = str(item.get("word", "")).strip(), str(item.get("say", "")).strip()
        if word and say and word not in setup.sounds:
            setup.sounds[word] = say
    return save(slug, {"sounds": setup.sounds})


def _ask_for_sounds(complete_structured, preferences, spoken: str) -> Suggested:
    return complete_structured(
        Suggested,
        "You prepare narration for a text-to-speech voice. List only the names and "
        "terms in the text that such a voice is likely to mispronounce -- foreign "
        "names, unusual scientific terms -- each with a respelling the voice will read "
        "correctly as ordinary words: lowercase except where a name starts, no "
        "hyphenated syllables, no capitals for stress, no phonetic symbols "
        "(\"Loewi\" -> \"Lervee\", \"Galvani\" -> \"Galvahnee\"). Give each name on its "
        "own, not with the first name that comes before it. Leave out common words and "
        "words a voice already says well.",
        f"Voice language: {preferences.language_name}\n\n{spoken}",
        # A reasoning model spends from the same budget: 8,000 ran out on one section.
        max_tokens=65536)


def platform_needs(project_root: Path) -> dict[str, Any]:
    platforms = set(load(project_root).platforms)
    return {"smallest_text_px": 44 if "classroom" in platforms else 36,
            "youtube": "youtube" in platforms, "website": "website" in platforms}


def music_for(project_root: Path) -> tuple[Path | None, float]:
    """The bed to lay under the narration, and its level in dB, or (None, 0)."""
    setup = load(project_root)
    if setup.music.startswith("built-in:") and setup.music[9:] in BUILT_IN_MUSIC:
        return built_in_bed(setup.music[9:]), INTENSITIES[setup.intensity]
    if setup.music.startswith("upload:"):
        path = _upload(project_root, setup.music[7:])
        return (path, INTENSITIES[setup.intensity]) if path else (None, 0.0)
    return None, 0.0


# --- music ------------------------------------------------------------------------------


def _uploads(project_root: Path) -> list[Path]:
    folder = project_root / "music"
    return sorted(p for p in folder.glob("*") if p.suffix.lower() in MUSIC_SUFFIXES) \
        if folder.is_dir() else []


def _upload(project_root: Path, name: str) -> Path | None:
    return next((p for p in _uploads(project_root) if p.name == name), None)


def add_music(slug: str, file_name: str, data: bytes) -> dict[str, Any]:
    """Keep an uploaded track in the project's music. The person says it is theirs
    to use: nothing here can know a track's licence."""
    from pipeline.sources import sanitize_source_file_name

    project = require_project(slug)
    name = sanitize_source_file_name(file_name)
    if Path(name).suffix.lower() not in MUSIC_SUFFIXES:
        raise OperationFailed(f"{file_name} is not a music file: use "
                              + ", ".join(sorted(MUSIC_SUFFIXES)) + ".")
    if len(data) > LARGEST_MUSIC_BYTES:
        raise OperationFailed("That track is larger than 40 MB.")
    folder = project.root / "music"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_bytes(data)
    return read(slug)


def built_in_bed(key: str) -> Path:
    """A built-in bed, made once here in code and kept: free to use, made by no one
    else. A seamless 32-second loop the render repeats under the whole video."""
    from pipeline.music_beds import make_bed

    target = CACHE / "music" / f"{key}.wav"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        make_bed(key, target, SAMPLE_RATE)
    return target


def music_track(project_root: Path, key: str) -> Path:
    if key.startswith("built-in:") and key[9:] in BUILT_IN_MUSIC:
        return built_in_bed(key[9:])
    path = _upload(project_root, key[7:]) if key.startswith("upload:") else None
    if path is None:
        raise OperationFailed(f"No music {key!r}.")
    return path


# --- samples to listen to ---------------------------------------------------------------


def voice_sample(voice_key: str, pace: str = "normal") -> Path:
    """A few seconds of this voice at this pace, spoken once and kept."""
    from pipeline.speech import SpeechFailed, synthesise_narration

    voice = next((v for v in VOICES if v.key == voice_key), None)
    if voice is None:
        raise OperationFailed(f"No voice {voice_key!r}.")
    rate = PACES.get(pace, "+0%")
    target = CACHE / "voices" / f"{voice.key}{rate.replace('%', 'pc')}.mp3"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        spoken = voice.key if rate == "+0%" else f"{voice.key}@{rate}"
        try:
            synthesise_narration(SAMPLE_WORDS[voice.language], target, "edge", spoken)
        except SpeechFailed as failure:
            raise OperationFailed(f"The sample could not be spoken: {failure}") from failure
    return target


def music_sample(project_root: Path, music_key: str, intensity: str,
                 voice_key: str = "", pace: str = "normal") -> Path:
    """The bed alone (no voice), or under the chosen voice at this intensity, as
    the render will mix it: 20 seconds, made once and kept."""
    from pipeline.audio_mix import mix_under_voice

    bed = music_track(project_root, music_key)
    level = INTENSITIES.get(intensity, INTENSITIES["soft"])
    key = hashlib.sha256(f"{bed}|{bed.stat().st_mtime}|{level}|{voice_key}|{pace}".encode()
                         ).hexdigest()[:16]
    target = CACHE / "previews" / f"{key}.mp3"
    if target.exists():
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise OperationFailed("ffmpeg is needed to play music samples.")
    if voice_key:
        mix_under_voice(voice_sample(voice_key, pace), bed, level, target, seconds=20,
                        lead_in=2.0)
    else:
        subprocess.run([ffmpeg, "-y", "-v", "error", "-stream_loop", "-1", "-i", str(bed),
                        "-t", "20", "-af", "afade=t=in:d=1,afade=t=out:st=18:d=2",
                        "-c:a", "libmp3lame", "-b:a", "160k", str(target)],
                       check=True, capture_output=True, stdin=subprocess.DEVNULL, timeout=60)
    return target


def say_sample(project_root: Path, text: str) -> Path:
    """`text` in the project's voice, with its pronunciations: to hear whether a
    respelling works before a whole video is spoken with it. Kept once made."""
    from pipeline.narration_audio import speak
    from pipeline.speech import SpeechFailed
    from pipeline.stage_options import video_preferences

    text = " ".join(text.split())[:200]
    if not text:
        raise OperationFailed("There is nothing to say.")
    voice = video_preferences(project_root).voice_for("edge")
    sounds = pronunciations(project_root)
    key = hashlib.sha256(f"{voice}|{sorted(sounds.items())}|{text}".encode()).hexdigest()[:16]
    target = CACHE / "said" / f"{key}.mp3"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            speak(text, target, "edge", voice, sounds)
        except SpeechFailed as failure:
            raise OperationFailed(f"It could not be spoken: {failure}") from failure
    return target
