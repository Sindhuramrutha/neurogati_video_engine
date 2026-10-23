"""One pace for every model call this server makes.

The provider allows a fixed number of requests a minute across the whole account
(TokenRouter: 15). Scene agents and their reviews would go over it within
seconds, and every call past the limit would fail. So each call takes a place in
a shared one-minute window before it is sent, waiting for a place when the
window is full: slower under load, never refused.

`LLM_REQUESTS_PER_MINUTE` sets the window (default 13, a little under 15). The
limit has changed under us before (30, then 15) and the app kept sending 28 a
minute into refusals, which risks the account. So a refusal is learned from: the
limit it states ("Maximum 15 requests within 1 minutes") becomes the pace for
every process, a little under it, and every process holds off for a whole
minute before sending again.

The window is shared by every process on this machine, through a small file:
the web app and a script making scenes at the same time each kept their own 28,
sent 56 between them, and the provider refused the rest.
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
from collections import deque

WINDOW_SECONDS = 60.0
DEFAULT_PER_MINUTE = 13
MARGIN = 2                     # requests a minute kept below a limit a refusal states
STATED = re.compile(r"maximum\s+(\d+)\s+requests?\s+(?:with)?in\s+(\d+)?\s*min", re.I)

_lock = threading.Lock()
_sent: deque[float] = deque()


def per_minute() -> int:
    try:
        set_here = max(1, int(os.environ.get("LLM_REQUESTS_PER_MINUTE", DEFAULT_PER_MINUTE)))
    except ValueError:
        set_here = DEFAULT_PER_MINUTE
    learned = _learned().get("per_minute")
    return min(set_here, learned) if isinstance(learned, int) and learned > 0 else set_here


def _limit_file():
    from pipeline.config import REPO_ROOT
    return REPO_ROOT / ".cache" / "llm-limit.json"


def _learned() -> dict:
    try:
        found = json.loads(_limit_file().read_text(encoding="utf-8"))
        return found if isinstance(found, dict) else {}
    except (OSError, ValueError):
        return {}


def refused(said: str, now: float | None = None) -> None:
    """The provider refused a request for its rate limit: every process holds off
    a whole window, and when the refusal states the limit, paces a little under it
    from now on."""
    from pipeline.storage.documents import write_text_atomically

    now = time.time() if now is None else now
    known = _learned()
    stated = STATED.search(said or "")
    if stated:
        minutes = max(1, int(stated.group(2) or 1))
        known["per_minute"] = max(1, int(stated.group(1)) // minutes - MARGIN)
    known["cool_until"] = now + WINDOW_SECONDS
    _limit_file().parent.mkdir(parents=True, exist_ok=True)
    write_text_atomically(_limit_file(), json.dumps(known))


def notice(response) -> None:
    """Every answer the provider sends: a rate-limit refusal slows every process."""
    if response.status_code == 429:
        response.read()
        refused(response.text)


def _cooling(now: float) -> float:
    """Seconds left before a refused provider may be asked again."""
    until = _learned().get("cool_until")
    return max(0.0, float(until) - now) if isinstance(until, (int, float)) else 0.0


def take_a_place(clock=time.monotonic, sleep=time.sleep) -> float:
    """Block until a request may be sent; return how long it waited."""
    waited = 0.0
    if clock is time.monotonic:          # the real clock: a refusal holds everyone off
        while (pause := _cooling(time.time())) > 0:
            sleep(pause)
            waited += pause
    while True:
        with _lock:
            now = clock()
            while _sent and now - _sent[0] >= WINDOW_SECONDS:
                _sent.popleft()
            if len(_sent) < per_minute():
                _sent.append(now)
                break
            pause = WINDOW_SECONDS - (now - _sent[0]) + 0.05
        sleep(pause)
        waited += pause
    if clock is time.monotonic:          # the real clock: share the window
        waited += _shared_place(sleep)
    return waited


def _shared_file():
    from pipeline.config import REPO_ROOT
    return REPO_ROOT / ".cache" / "llm-pace.json"


def _shared_place(sleep) -> float:
    """A place in the window every process shares. A lock file guards it; one
    left by a process that died is taken over after a few seconds."""
    path = _shared_file()
    lock = path.with_suffix(".lock")
    path.parent.mkdir(parents=True, exist_ok=True)
    waited = 0.0
    while True:
        try:
            handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > 5:
                    lock.unlink(missing_ok=True)
            except OSError:
                pass
            sleep(0.05)
            waited += 0.05
            continue
        try:
            now = time.time()
            try:
                sent = [t for t in json.loads(path.read_text(encoding="utf-8"))
                        if now - t < WINDOW_SECONDS]
            except (OSError, ValueError):
                sent = []
            if len(sent) < per_minute():
                path.write_text(json.dumps(sent + [now]), encoding="utf-8")
                return waited
            pause = WINDOW_SECONDS - (now - min(sent)) + 0.05
        finally:
            os.close(handle)
            lock.unlink(missing_ok=True)
        sleep(pause)
        waited += pause
