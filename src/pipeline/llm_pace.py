"""One pace for every model call this server makes.

The provider allows a fixed number of requests a minute across the whole account
(TokenRouter: 30). Scene agents and their reviews would go over it within
seconds, and every call past the limit would fail. So each call takes a place in
a shared one-minute window before it is sent, waiting for a place when the
window is full: slower under load, never refused.

`LLM_REQUESTS_PER_MINUTE` sets the window (default 28, a little under 30).
"""

from __future__ import annotations

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
                return waited
            pause = WINDOW_SECONDS - (now - _sent[0]) + 0.05
        sleep(pause)
        waited += pause
