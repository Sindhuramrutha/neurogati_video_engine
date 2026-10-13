"""Text to speech — declared providers, one contract, swap without touching callers.

A single hardcoded engine fails without a GPU (minutes per scene) or offline
(nothing at all), and changing it means editing the audio code. A provider is a
**declaration** — like tools and stage options — and
the renderer only ever calls `synthesise_narration`.

Every provider answers the same three questions before it is offered:

- **Is it installed?** A provider whose package is missing is listed with the
  exact install command, not hidden. An option that silently disappears is how
  someone concludes the app is broken.
- **Does it need a key?** Named as an environment variable, resolved through
  `config`/`credentials` like every other secret. No provider reads a key from
  an argument.
- **Where does the compute happen?** Local providers cost time and disk; network
  providers cost a round trip and send your script to a third party. That is a
  real decision and the UI should state it rather than bury it.

`SILENT` exists on purpose: it writes silence of the right duration, so the whole
render path can be exercised with zero dependencies and no network. A renderer
that can only be tested with a working TTS is a renderer nobody tests.
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import threading
import wave
from dataclasses import dataclass
from importlib.util import find_spec
from pathlib import Path

logger = logging.getLogger(__name__)

# 24 kHz mono is what most neural TTS emits; resampling once here keeps every
# provider's output muxable without a per-provider special case.
SAMPLE_RATE_HZ = 24000

# Used by SILENT and as the fallback estimate when a provider cannot report
# duration. Matches the rate the rest of the pipeline assumes.
WORDS_PER_MINUTE_OF_NARRATION = 150


class SpeechFailed(Exception):
    """Synthesis did not produce audio. Names the provider and the reason.
    `transient` False: trying again will not help (resilience.classify)."""

    def __init__(self, message: str, transient: bool | None = None) -> None:
        super().__init__(message)
        self.transient = transient


@dataclass(frozen=True)
class VoiceProvider:
    """One way to turn text into speech.

    Declared here and rendered generically, so adding a provider is one entry
    plus one function -- no UI change, no new route, no branching in the renderer.
    """

    key: str
    label: str
    # "local" burns your CPU/GPU and works offline. "network" sends the narration
    # text to a third party. "none" produces silence.
    compute: str
    summary: str
    # The package that must be importable, if any.
    required_module: str | None = None
    # The command that installs it, shown verbatim when it is missing.
    install_command: str = ""
    # Environment variable holding the key, if the provider needs one.
    required_key_name: str | None = None
    default_voice: str = ""
    voice_examples: tuple[str, ...] = ()

    def is_installed(self) -> bool:
        return self.required_module is None or find_spec(self.required_module) is not None

    def has_key(self) -> bool:
        if self.required_key_name is None:
            return True
        return bool(os.environ.get(self.required_key_name) or _key_from_settings(
            self.required_key_name))

    def is_available(self) -> bool:
        return self.is_installed() and self.has_key()

    def unavailable_reason(self) -> str:
        if not self.is_installed():
            return f"not installed - run: {self.install_command}"
        if not self.has_key():
            return f"needs {self.required_key_name}, set it in the API keys panel"
        return ""

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "label": self.label,
            "compute": self.compute,
            "summary": self.summary,
            "install_command": self.install_command,
            "required_key_name": self.required_key_name,
            "default_voice": self.default_voice,
            "voice_examples": list(self.voice_examples),
            "is_installed": self.is_installed(),
            "is_available": self.is_available(),
            "unavailable_reason": self.unavailable_reason(),
        }


def _key_from_settings(name: str) -> str:
    """Read a provider key through the same path as every other secret."""
    from pipeline.credentials import read_environment_file

    return read_environment_file().get(name, "")


VOICE_PROVIDERS: tuple[VoiceProvider, ...] = (
    VoiceProvider(
        key="silent",
        label="Silent (no voice)",
        compute="none",
        summary="Writes silence of the estimated duration. Renders a video with "
                "no narration - useful for checking timing and layout, and for "
                "testing the render path with nothing installed.",
    ),
    VoiceProvider(
        key="edge",
        label="Edge TTS (Microsoft neural)",
        compute="network",
        summary="Free neural voices over the network, no account and no key. "
                "Good quality and fast. Sends the narration text to Microsoft.",
        required_module="edge_tts",
        install_command="uv add edge-tts",
        default_voice="en-US-AriaNeural",
        voice_examples=(
            "en-US-AriaNeural", "en-US-GuyNeural", "en-GB-SoniaNeural",
            "en-IN-NeerjaNeural", "en-IN-PrabhatNeural",
        ),
    ),
    VoiceProvider(
        key="kokoro",
        label="Kokoro (local)",
        compute="local",
        summary="Runs entirely on your machine, no network. Pulls "
                "roughly 1-2 GB of ML dependencies and is slow without a GPU.",
        required_module="kokoro",
        install_command="uv sync --extra audio",
        default_voice="af_heart",
        voice_examples=("af_heart", "af_bella", "am_michael", "bf_emma"),
    ),
    VoiceProvider(
        key="piper",
        label="Piper (local, fast)",
        compute="local",
        summary="Small local neural TTS that runs well on CPU. Much lighter than "
                "Kokoro; voices are downloaded per model.",
        required_module="piper",
        install_command="uv add piper-tts",
        default_voice="en_US-amy-medium",
        voice_examples=("en_US-amy-medium", "en_US-ryan-high", "en_GB-alba-medium"),
    ),
    VoiceProvider(
        key="huggingface_local",
        label="Hugging Face (local model)",
        compute="local",
        summary="Any TTS model from the Hub, run locally through transformers. "
                "Slow to start (the model downloads once) but fully offline after.",
        required_module="transformers",
        install_command="uv add transformers torch",
        default_voice="facebook/mms-tts-eng",
        voice_examples=(
            "facebook/mms-tts-eng", "microsoft/speecht5_tts", "suno/bark-small",
        ),
    ),
    VoiceProvider(
        key="huggingface_api",
        label="Hugging Face (Inference API)",
        compute="network",
        summary="The same Hub models, run on Hugging Face's servers. No local "
                "compute and no model download; needs a token.",
        required_module="httpx",
        install_command="uv add httpx",
        required_key_name="HUGGINGFACE_API_KEY",
        default_voice="facebook/mms-tts-eng",
        voice_examples=("facebook/mms-tts-eng", "suno/bark-small"),
    ),
    VoiceProvider(
        key="openai_compatible",
        label="OpenAI-compatible /audio/speech",
        compute="network",
        summary="Any provider exposing OpenAI's speech endpoint - OpenAI itself, "
                "or a gateway. Uses TTS_BASE_URL and TTS_API_KEY so it can point "
                "somewhere other than your text model.",
        required_module="httpx",
        install_command="uv add httpx",
        required_key_name="TTS_API_KEY",
        default_voice="alloy",
        voice_examples=("alloy", "echo", "fable", "onyx", "nova", "shimmer"),
    ),
    VoiceProvider(
        key="elevenlabs",
        label="ElevenLabs",
        compute="network",
        summary="High-quality commercial voices. Needs an account and a key; "
                "billed per character.",
        required_module="httpx",
        install_command="uv add httpx",
        required_key_name="ELEVENLABS_API_KEY",
        default_voice="21m00Tcm4TlvDq8ikWAM",
        voice_examples=("21m00Tcm4TlvDq8ikWAM", "AZnzlk1XvdvUeBnXmlld"),
    ),
)

PROVIDERS_BY_KEY: dict[str, VoiceProvider] = {p.key: p for p in VOICE_PROVIDERS}


def describe_voice_providers() -> dict:
    """Every provider with its live availability, for a UI or an agent to choose from."""
    providers = [provider.to_dict() for provider in VOICE_PROVIDERS]
    ready = [p["key"] for p in providers if p["is_available"]]
    return {
        "providers": providers,
        "available": ready,
        # Prefer a real voice over silence when one is actually usable.
        "recommended": next((key for key in ready if key != "silent"), "silent"),
    }


def resolve_provider(provider_key: str) -> VoiceProvider:
    provider = PROVIDERS_BY_KEY.get(provider_key)
    if provider is None:
        raise SpeechFailed(
            f"No voice provider {provider_key!r}. "
            f"Choose one of: {', '.join(PROVIDERS_BY_KEY)}."
        )
    return provider


@dataclass(frozen=True)
class WordTiming:
    """When one word is spoken, from the voice itself.

    Not an estimate. A provider that reports word boundaries is telling the
    renderer exactly where every word lands in the file it just produced, which
    is the difference between a slide that changes on a word and one that
    changes on a share of the characters.
    """

    text: str
    start_ms: int
    duration_ms: int

    @property
    def end_ms(self) -> int:
        return self.start_ms + self.duration_ms

    def to_dict(self) -> dict:
        return {"text": self.text, "start_ms": self.start_ms,
                "duration_ms": self.duration_ms}


@dataclass(frozen=True)
class SpeechResult:
    audio_path: Path
    duration_ms: int
    provider_key: str
    voice: str

    # Empty for every provider that does not report them, which is most of
    # them; the renderer falls back to splitting by text length.
    words: tuple[WordTiming, ...] = ()


def word_timings_path(audio_path: Path) -> Path:
    return audio_path.with_suffix(audio_path.suffix + ".words.json")


def save_word_timings(audio_path: Path, words: tuple[WordTiming, ...]) -> None:
    """Keep the timings beside the audio they describe.

    Beside it rather than in the render result because the audio outlives the
    render: a later cut, or the Studio timeline, can read where the words fell
    without paying for the voice again.
    """
    if not words:
        return
    import json

    word_timings_path(audio_path).write_text(
        json.dumps([word.to_dict() for word in words]), encoding="utf-8")


def load_word_timings(audio_path: Path) -> tuple[WordTiming, ...]:
    import json

    path = word_timings_path(audio_path)
    if not path.exists():
        return ()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as unreadable:
        logger.warning("word timings for %s could not be read: %s", audio_path.name, unreadable)
        return ()
    return tuple(
        WordTiming(text=str(entry.get("text", "")),
                   start_ms=int(entry.get("start_ms", 0)),
                   duration_ms=int(entry.get("duration_ms", 0)))
        for entry in raw if isinstance(entry, dict)
    )


def _write_silence(output_path: Path, duration_ms: int) -> None:
    """A real, playable wav of the right length.

    Silence rather than a zero-byte file: ffmpeg must be able to mux it, and a
    missing stream fails differently from a quiet one.
    """
    frame_count = int(SAMPLE_RATE_HZ * duration_ms / 1000)
    with wave.open(str(output_path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE_HZ)
        handle.writeframes(b"\x00\x00" * frame_count)


def measure_audio_duration_ms(path: Path) -> int:
    """Measured, never estimated.

    Audio is the clock. Guessing a duration from the word count is how
    animation drifts out of sync with narration, so the real file is measured
    even though every provider claims a length.
    """
    probe = shutil.which("ffprobe")
    if probe:
        try:
            output = subprocess.run(
                [probe, "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                capture_output=True, text=True, timeout=60, check=True,
            ).stdout.strip()
            return int(float(output) * 1000)
        except (subprocess.SubprocessError, ValueError) as probe_failure:
            logger.warning("ffprobe could not measure %s: %s", path.name, probe_failure)

    try:
        with wave.open(str(path), "rb") as handle:
            return int(handle.getnframes() / handle.getframerate() * 1000)
    except (wave.Error, OSError) as wave_failure:
        raise SpeechFailed(
            f"Could not measure the duration of {path.name}: {wave_failure}"
        ) from wave_failure


def estimate_duration_ms(text: str) -> int:
    words = max(1, len(text.split()))
    return int(words / WORDS_PER_MINUTE_OF_NARRATION * 60_000)


# --- the backends -----------------------------------------------------------
#
# Each writes audio to `output_path` and returns nothing. Failures raise
# SpeechFailed with the provider named, so a caller never has to guess which of
# eight providers produced a traceback.


EDGE_GIVE_UP_SECONDS = 900      # then the job waits and resumes by itself
_EDGE_TURN = threading.Lock()


def _speak_silent(text: str, output_path: Path, voice: str) -> None:
    _write_silence(output_path, estimate_duration_ms(text))


def _speak_edge(text: str, output_path: Path, voice: str) -> list[WordTiming]:
    """edge-tts, streamed rather than saved, to keep the word boundaries.

    `Communicate.save` writes the audio and throws the `WordBoundary` events
    away. Streaming costs nothing extra -- the events arrive on the same
    connection as the audio -- and they are the only exact timing anything in
    this pipeline has ever had.
    """
    import asyncio

    import edge_tts

    words: list[WordTiming] = []
    voice, rate = ((voice or "en-US-AriaNeural") + "@+0%").split("@")[:2]  # pace: "v@-10%"

    async def run() -> None:
        # Asked for explicitly: the default is sentence boundaries, which are
        # too coarse to put a label on the word it names. An edge-tts
        # without the argument still speaks; it just reports nothing.
        try:
            communicate = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
        except TypeError:
            communicate = edge_tts.Communicate(text, voice, rate=rate)
        with open(output_path, "wb") as handle:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    handle.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    # Reported in 100-nanosecond ticks, the way Windows speech
                    # has always counted.
                    words.append(WordTiming(
                        text=str(chunk.get("text", "")),
                        start_ms=int(chunk["offset"]) // 10_000,
                        duration_ms=int(chunk["duration"]) // 10_000,
                    ))

    # The free service drops a request now and then ("NoAudioReceived") and
    # throttles bursts; the same words a moment later speak fine. Through the
    # gate (resilience.py): retried with jittered backoff for up to 15 minutes,
    # one request at a time, and a circuit shared with every other process.
    from pipeline.resilience import call

    def attempt() -> list[WordTiming]:
        words.clear()
        with _EDGE_TURN:
            asyncio.run(run())
        if not output_path.exists() or output_path.stat().st_size == 0:
            raise ConnectionError("no audio came back")
        return list(words)

    return call("edge-tts", attempt, attempts=10, base_seconds=3, longest_wait=180,
                give_up_after=EDGE_GIVE_UP_SECONDS)


def _speak_kokoro(text: str, output_path: Path, voice: str) -> None:
    import numpy
    import soundfile
    from kokoro import KPipeline

    pipeline = KPipeline(lang_code="a")
    chunks = [audio for _, _, audio in pipeline(text, voice=voice or "af_heart")]
    if not chunks:
        raise SpeechFailed("kokoro produced no audio for that text")
    soundfile.write(str(output_path), numpy.concatenate(chunks), 24000)


def _speak_piper(text: str, output_path: Path, voice: str) -> None:
    from piper import PiperVoice

    loaded = PiperVoice.load(voice or "en_US-amy-medium")
    with wave.open(str(output_path), "wb") as handle:
        loaded.synthesize(text, handle)


def _speak_huggingface_local(text: str, output_path: Path, voice: str) -> None:
    import numpy
    import soundfile
    from transformers import pipeline as hf_pipeline

    synthesiser = hf_pipeline("text-to-speech", model=voice or "facebook/mms-tts-eng")
    result = synthesiser(text)
    soundfile.write(
        str(output_path),
        numpy.asarray(result["audio"]).squeeze(),
        int(result["sampling_rate"]),
    )


def _post_audio(service: str, url: str, headers: dict, body: dict, output_path: Path) -> None:
    """One request to a voice service, through the gate: a 429, a 5xx or a dropped
    connection is tried again with backoff; a refused key is said at once."""
    import httpx

    from pipeline.resilience import call

    def attempt() -> bytes:
        response = httpx.post(url, headers=headers, json=body, timeout=180)
        response.raise_for_status()
        return response.content

    try:
        output_path.write_bytes(call(service, attempt, attempts=5, give_up_after=600))
    except httpx.HTTPStatusError as refused:
        raise SpeechFailed(f"{service} returned {refused.response.status_code}: "
                           f"{refused.response.text[:200]}") from refused


def _speak_huggingface_api(text: str, output_path: Path, voice: str) -> None:
    model = voice or "facebook/mms-tts-eng"
    token = os.environ.get("HUGGINGFACE_API_KEY") or _key_from_settings("HUGGINGFACE_API_KEY")
    _post_audio("huggingface", f"https://api-inference.huggingface.co/models/{model}",
                {"Authorization": f"Bearer {token}"}, {"inputs": text}, output_path)


def _speak_openai_compatible(text: str, output_path: Path, voice: str) -> None:
    base_url = (
        os.environ.get("TTS_BASE_URL")
        or _key_from_settings("TTS_BASE_URL")
        or "https://api.openai.com/v1"
    ).rstrip("/")
    token = os.environ.get("TTS_API_KEY") or _key_from_settings("TTS_API_KEY")
    model = os.environ.get("TTS_MODEL") or _key_from_settings("TTS_MODEL") or "tts-1"
    _post_audio("tts-api", f"{base_url}/audio/speech", {"Authorization": f"Bearer {token}"},
                {"model": model, "voice": voice or "alloy", "input": text}, output_path)


def _speak_elevenlabs(text: str, output_path: Path, voice: str) -> None:
    token = os.environ.get("ELEVENLABS_API_KEY") or _key_from_settings("ELEVENLABS_API_KEY")
    _post_audio("elevenlabs",
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice or '21m00Tcm4TlvDq8ikWAM'}",
                {"xi-api-key": token, "Content-Type": "application/json"},
                {"text": text, "model_id": "eleven_multilingual_v2"}, output_path)


BACKENDS = {
    "silent": _speak_silent,
    "edge": _speak_edge,
    "kokoro": _speak_kokoro,
    "piper": _speak_piper,
    "huggingface_local": _speak_huggingface_local,
    "huggingface_api": _speak_huggingface_api,
    "openai_compatible": _speak_openai_compatible,
    "elevenlabs": _speak_elevenlabs,
}


def synthesise_narration(
    text: str, output_path: Path, provider_key: str = "silent", voice: str = ""
) -> SpeechResult:
    """Speak `text` into `output_path`. The only entry point callers use.

    The returned duration is **measured from the file**, not estimated from the
    text -- audio is the clock, and a clock that guesses is not one.
    """
    provider = resolve_provider(provider_key)

    if not provider.is_available():
        raise SpeechFailed(f"{provider.label} is not usable: {provider.unavailable_reason()}",
                           transient=False)

    if not text.strip():
        raise SpeechFailed("There is nothing to speak - the narration is empty.",
                           transient=False)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    backend = BACKENDS[provider.key]

    try:
        spoken_words = backend(text, output_path, voice or provider.default_voice) or ()
    except SpeechFailed:
        raise
    except Exception as synthesis_failure:
        raise SpeechFailed(
            f"{provider.label} failed: {type(synthesis_failure).__name__}: "
            f"{synthesis_failure}"
        ) from synthesis_failure

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise SpeechFailed(f"{provider.label} produced no audio file.")

    words = tuple(spoken_words)
    save_word_timings(output_path, words)
    return SpeechResult(
        audio_path=output_path,
        duration_ms=measure_audio_duration_ms(output_path),
        provider_key=provider.key,
        voice=voice or provider.default_voice,
        words=words,
    )
