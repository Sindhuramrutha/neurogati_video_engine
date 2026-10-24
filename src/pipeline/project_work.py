"""Everything running for a project, and stopping all of it at once.

Deleting a project must work whatever is running in it: scenes being made, a
render, a queued job, and the ffmpeg, Manim and browser processes under them. Work
that kept going after its folder was erased would write files back into it.

Work announces itself with `working_on(slug)` (a thread, for as long as it runs) and
asks `stopped()` at its natural pauses. Processes it starts go through `run` (or are
`register`ed), so `stop_everything` can kill them. A stop is an epoch bump, not a
flag: work started afterwards, even in a new project with the same name, is not
told to stop by an old deletion.
"""

from __future__ import annotations

import contextvars
import subprocess
import sys
import threading
from collections.abc import Iterator
from contextlib import contextmanager

_lock = threading.Lock()
_epochs: dict[str, int] = {}
_processes: dict[str, set[subprocess.Popen]] = {}
_current: contextvars.ContextVar[tuple[str, int, str] | None] = contextvars.ContextVar(
    "project_work", default=None)


def _epoch(slug: str) -> int:
    with _lock:
        return _epochs.get(slug, 0)


def _identity(slug: str) -> str:
    """Which project lives under `slug` now: its project.json's creation time, or
    empty when there is none. A stop in another process cannot bump this one's
    epoch -- a project deleted on the page while a command-line run made its scenes
    was written back into existence -- so work also asks the folder itself."""
    from pipeline.core import projects_root
    from pipeline.storage.documents import read_json_object

    found = read_json_object(projects_root() / slug / "project.json", "project metadata")
    return str((found or {}).get("created") or "")


@contextmanager
def working_on(slug: str) -> Iterator[None]:
    """This thread is working for `slug` until the block ends."""
    token = _current.set((slug, _epoch(slug), _identity(slug)))
    try:
        yield
    finally:
        _current.reset(token)


def stopped() -> bool:
    """Has the project this thread works for been told to stop everything -- here,
    or by its deletion anywhere: its folder gone, or now another project's?"""
    current = _current.get()
    if current is None:
        return False
    slug, epoch, identity = current
    return _epoch(slug) != epoch or (bool(identity) and _identity(slug) != identity)


def kill_tree(pid: int) -> None:
    """End a process and everything it started."""
    import os
    import signal

    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)],
                       capture_output=True, check=False)
        return
    try:
        os.killpg(os.getpgid(pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


def register(process: subprocess.Popen) -> None:
    """A process this thread's project owns: `stop_everything` will kill it."""
    current = _current.get()
    if current is not None:
        with _lock:
            _processes.setdefault(current[0], set()).add(process)


def unregister(process: subprocess.Popen) -> None:
    with _lock:
        for processes in _processes.values():
            processes.discard(process)


def stop_everything(slug: str) -> int:
    """Tell all work for `slug` to stop at its next pause, and kill its processes
    now. Returns how many processes were killed."""
    with _lock:
        _epochs[slug] = _epochs.get(slug, 0) + 1
        doomed = list(_processes.pop(slug, ()))
    for process in doomed:
        kill_tree(process.pid)
    return len(doomed)


def run(command: list[str], *, timeout: float, input: str | None = None, cwd=None,
        env=None, check: bool = False) -> subprocess.CompletedProcess:
    """`subprocess.run` for a project's work: text in and out, killed on a timeout,
    and killable by `stop_everything`."""
    process = subprocess.Popen(
        command, cwd=cwd, env=env, text=True, encoding="utf-8", errors="replace",
        stdin=subprocess.PIPE if input is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        start_new_session=sys.platform != "win32")
    register(process)
    try:
        output, errors = process.communicate(input, timeout=timeout)
    except subprocess.TimeoutExpired:
        kill_tree(process.pid)
        process.communicate()
        raise
    finally:
        unregister(process)
    if check and process.returncode:
        raise subprocess.CalledProcessError(process.returncode, command, output, errors)
    return subprocess.CompletedProcess(command, process.returncode, output, errors)
