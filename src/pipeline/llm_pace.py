"""One pace for every model call this server makes.

The provider allows a fixed number of requests a minute across the whole account
(TokenRouter: 30). Scene agents and their reviews would go over it within
seconds, and every call past the limit would fail. So each call takes a place in
a shared one-minute window before it is sent, waiting for a place when the
window is full: slower under load, never refused.

`LLM_REQUESTS_PER_MINUTE` sets the window (default 28, a little under 30).

The window is shared by every process on this machine, through a small file:
the web app and a script making scenes at the same time each kept their own 28,
sent 56 between them, and the provider refused the rest.
"""

from __future__ import annotations

import json
import os
import threading
import time
from collections import deque

WINDOW_SECONDS = 60.0
DEFAULT_PER_MINUTE = 28

_lock = threading.Lock()
_sent: deque[float] = deque()


def per_minute() -> int:
    try:
        return max(1, int(os.environ.get("LLM_REQUESTS_PER_MINUTE", DEFAULT_PER_MINUTE)))
    except ValueError:
        return DEFAULT_PER_MINUTE


def take_a_place(clock=time.monotonic, sleep=time.sleep) -> float:
    """Block until a request may be sent; return how long it waited."""
    waited = 0.0
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
