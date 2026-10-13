"""One gate for every call to a service outside this machine.

Outside services fail as a matter of course: Microsoft's free voice drops a
request in a burst ("NoAudioReceived"), the model provider refuses past 30 a
minute, a request stalls. Each of these once stopped a whole video. Through this
gate a call is

- **retried** with exponential backoff and full jitter (so many waiting calls do
  not come back at the same moment), honouring a `Retry-After` the service sent;
- **classed**: *transient* (it may work later: throttled, timed out, the
  connection dropped, a 5xx) or *permanent* (a bad key, a bad request, a bug).
  A permanent failure is not retried; it is raised at once, to be said plainly;
- **behind a circuit breaker** per service, shared by every process on this
  machine (a small file in `.cache/breakers`). After repeated transient
  failures the breaker opens: callers wait for the service to come back rather
  than each trying, failing and giving up. One trial call then closes it again.

When the attempts run out on a transient failure, `ServiceUnavailable` is raised:
the work that called it is stopped *for now*, and the job around it (a render, a
scene) waits and resumes by itself.
"""

from __future__ import annotations

import json
import logging
import os
import random
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


TRANSIENT, PERMANENT = "transient", "permanent"
OPEN_AFTER = 5                 # transient failures in a row before the breaker opens
FIRST_COOL_SECONDS = 30.0      # how long it stays open the first time; doubles
LONGEST_COOL_SECONDS = 900.0
LOCK_STALE_SECONDS = 5.0


def _SLEEP(seconds: float) -> None:          # one name for tests to make waits instant
    time.sleep(seconds)


class ServiceUnavailable(Exception):
    """A service could not be reached for now, after every attempt. Transient by
    definition: whatever needed it should wait and try again later."""

    transient = True

    def __init__(self, service: str, cause: BaseException | str) -> None:
        self.service = service
        super().__init__(f"{service} is not answering for now ({_short(cause)}). "
                         "It will be tried again.")


def _short(cause: BaseException | str) -> str:
    text = cause if isinstance(cause, str) else (f"{type(cause).__name__}: {cause}"
                                                 if str(cause) else type(cause).__name__)
    return text.strip().splitlines()[0][:200] if text.strip() else "no answer"


# --- what kind of failure ------------------------------------------------------------------

_TRANSIENT_NAMES = {
    # openai / httpx / aiohttp / edge-tts, by name so none is a hard import here
    "RateLimitError", "APITimeoutError", "APIConnectionError", "InternalServerError",
    "TimeoutException", "ConnectTimeout", "ReadTimeout", "WriteTimeout", "PoolTimeout",
    "ConnectError", "ReadError", "WriteError", "RemoteProtocolError", "NetworkError",
    "ClientConnectionError", "ClientConnectorError", "ServerDisconnectedError",
    "ClientOSError", "ClientPayloadError", "WSServerHandshakeError", "WebSocketError",
    "NoAudioReceived", "UnexpectedResponse", "UnknownResponse",
    "TimeoutError", "ConnectionError", "ConnectionResetError", "ConnectionAbortedError",
    "BrokenPipeError", "IncompleteRead",
}
_PERMANENT_NAMES = {
    "AuthenticationError", "PermissionDeniedError", "BadRequestError", "NotFoundError",
    "UnprocessableEntityError", "ModelNotConfigured", "ValueError", "TypeError",
    "KeyError", "AttributeError", "NotImplementedError", "FileNotFoundError",
}


def _chain(failure: BaseException) -> list[BaseException]:
    seen, found = set(), []
    cause: BaseException | None = failure
    while cause is not None and id(cause) not in seen:
        seen.add(id(cause))
        found.append(cause)
        cause = cause.__cause__ or cause.__context__
    return found


def _status(failure: BaseException) -> int | None:
    for attribute in ("status_code", "status"):
        value = getattr(failure, attribute, None)
        if isinstance(value, int):
            return value
    response = getattr(failure, "response", None)
    value = getattr(response, "status_code", None)
    return value if isinstance(value, int) else None


def _kind(cause: BaseException) -> str | None:
    """What this one error says about itself, or None when it says nothing."""
    said = getattr(cause, "transient", None)          # an error may say what it is
    if isinstance(said, bool):
        return TRANSIENT if said else PERMANENT
    status = _status(cause)
    if status is not None:
        if status in (408, 409, 425, 429) or status >= 500:
            return TRANSIENT
        if 400 <= status < 500:
            return PERMANENT
    names = {kind.__name__ for kind in type(cause).__mro__}
    if names & _TRANSIENT_NAMES:
        return TRANSIENT
    if names & _PERMANENT_NAMES:
        return PERMANENT
    return None


def classify(failure: BaseException) -> str:
    """Transient or permanent. The root cause decides first: "the narration could
    not be spoken" raised from a dropped connection is transient; the same words
    raised as a deliberate refusal (no cause) are permanent. Unknown: transient,
    since the job around it waits and tries again a bounded number of times."""
    for cause in reversed(_chain(failure)):
        kind = _kind(cause)
        if kind is not None:
            return kind
    return TRANSIENT


def retry_after(failure: BaseException) -> float | None:
    """Seconds the service asked us to wait, when it said."""
    for cause in _chain(failure):
        headers = getattr(getattr(cause, "response", None), "headers", None)
        if not headers:
            continue
        value = headers.get("retry-after") or headers.get("Retry-After")
        try:
            return max(0.0, min(float(value), LONGEST_COOL_SECONDS)) if value else None
        except (TypeError, ValueError):
            return None
    return None


# --- the breaker, shared by every process ----------------------------------------------------

def _breakers() -> Path:
    from pipeline.config import REPO_ROOT
    return REPO_ROOT / ".cache" / "breakers"


def _locked(path: Path, change: Callable[[dict[str, Any]], dict[str, Any] | None],
            sleep: Callable[[float], None] = time.sleep) -> dict[str, Any]:
    """Read, change and write one breaker's file under a lock file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix(".lock")
    while True:
        try:
            handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > LOCK_STALE_SECONDS:
                    lock.unlink(missing_ok=True)
            except OSError:
                pass
            sleep(0.02)
    try:
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            state = {}
        changed = change(state)
        if changed is not None:
            path.write_text(json.dumps(changed), encoding="utf-8")
            return changed
        return state
    finally:
        os.close(handle)
        lock.unlink(missing_ok=True)


def breaker_state(service: str) -> dict[str, Any]:
    return _locked(_breakers() / f"{service}.json", lambda state: None)


def _record(service: str, ok: bool) -> None:
    def change(state: dict[str, Any]) -> dict[str, Any]:
        if ok:
            return {"failures": 0, "open_until": 0.0, "cool": 0.0}
        failures = int(state.get("failures", 0)) + 1
        cool = float(state.get("cool", 0.0))
        open_until = float(state.get("open_until", 0.0))
        if failures >= OPEN_AFTER:
            cool = min(LONGEST_COOL_SECONDS, cool * 2 if cool else FIRST_COOL_SECONDS)
            open_until = time.time() + cool
            logger.warning("%s: circuit open for %.0f s after %d failures",
                           service, cool, failures)
            failures = OPEN_AFTER - 1        # one trial call after the cool-off
        return {"failures": failures, "open_until": open_until, "cool": cool}
    _locked(_breakers() / f"{service}.json", change)


def _wait_while_open(service: str, deadline: float,
                     sleep: Callable[[float], None]) -> None:
    while True:
        until = float(breaker_state(service).get("open_until", 0.0))
        now = time.time()
        if until <= now:
            return
        if until > deadline:
            raise ServiceUnavailable(service, "it has been failing; waiting for it to recover")
        sleep(min(until - now, 30.0))


# --- the call ------------------------------------------------------------------------------

def call[T](service: str, attempt: Callable[[], T], *, attempts: int = 6,
         base_seconds: float = 2.0, longest_wait: float = 120.0,
         give_up_after: float = 900.0, sleep: Callable[[float], None] | None = None,
         on_retry: Callable[[BaseException, float], None] | None = None) -> T:
    """`attempt()` through the gate. Returns its result; raises a permanent
    failure as it came, or `ServiceUnavailable` once the attempts (or
    `give_up_after` seconds) are spent on transient ones."""
    sleep = sleep or (lambda seconds: _SLEEP(seconds))
    deadline = time.time() + give_up_after
    last: BaseException | None = None
    for number in range(attempts):
        _wait_while_open(service, deadline, sleep)
        try:
            result = attempt()
        except Exception as failure:          # classified below; nothing is swallowed
            if classify(failure) == PERMANENT:
                raise
            last = failure
            _record(service, ok=False)
            asked = retry_after(failure)
            pause = asked if asked is not None else random.uniform(
                0, min(longest_wait, base_seconds * 2 ** number))
            if number == attempts - 1 or time.time() + pause > deadline:
                break
            logger.info("%s: %s; trying again in %.1f s", service, _short(failure), pause)
            if on_retry:
                on_retry(failure, pause)
            sleep(pause)
            continue
        _record(service, ok=True)
        return result
    raise ServiceUnavailable(service, last or "no answer") from last


def is_transient(failure: BaseException) -> bool:
    return classify(failure) == TRANSIENT
