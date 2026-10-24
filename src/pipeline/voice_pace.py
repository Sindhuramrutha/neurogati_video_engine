"""How fast each voice really speaks, learned from every scene it speaks.

A script is drafted to a length in words. v9's was drafted at 150 words a minute and
spoken by en-IN-NeerjaNeural at about 140: 38 minutes on paper, 41 in the video, past
the 40 the person asked for. Every scene's narration is spoken once to be measured
(`scene_program.measure_narration`); each time, its words and seconds are added to
that voice's tally here, and drafting and the length checks use the voice's own pace
once enough of it is heard -- the assumed 150 until then.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

ASSUMED_WORDS_PER_MINUTE = 150
LEAST_MINUTES_HEARD = 3          # before a voice's own pace is trusted
SLOWEST, FASTEST = 90, 200       # words a minute: a measurement outside is not believed
_LOCK = threading.Lock()


def _path() -> Path:
    from pipeline.config import REPO_ROOT

    return REPO_ROOT / ".cache" / "voice-pace.json"


def _read() -> dict:
    try:
        found = json.loads(_path().read_text(encoding="utf-8"))
        return found if isinstance(found, dict) else {}
    except (OSError, ValueError):
        return {}


def record(voice: str, words: int, milliseconds: int) -> None:
    """Add one spoken scene to its voice's tally."""
    from pipeline.storage.documents import write_text_atomically

    if not voice or words <= 0 or milliseconds <= 0:
        return
    with _LOCK:
        tally = _read()
        heard = tally.get("voices", {}).get(voice, {"words": 0, "ms": 0})
        tally.setdefault("voices", {})[voice] = {"words": heard["words"] + words,
                                                 "ms": heard["ms"] + milliseconds}
        tally["last"] = voice
        _path().parent.mkdir(parents=True, exist_ok=True)
        write_text_atomically(_path(), json.dumps(tally, indent=1))


def words_per_minute(voice: str | None = None) -> float:
    """The voice's own pace, once enough is heard -- of the voice heard last when none
    is named -- else the assumed one."""
    tally = _read()
    heard = tally.get("voices", {}).get(voice or tally.get("last", ""), {})
    minutes = heard.get("ms", 0) / 60000
    if minutes < LEAST_MINUTES_HEARD:
        return ASSUMED_WORDS_PER_MINUTE
    pace = heard["words"] / minutes
    return pace if SLOWEST <= pace <= FASTEST else ASSUMED_WORDS_PER_MINUTE


def for_project(project) -> float:
    """The pace of the voice this project speaks in."""
    from pipeline.scene_program import _voice

    return words_per_minute(_voice(project)[1])
