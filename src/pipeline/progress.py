"""How far a long job has got, for the page to show while it waits.

A render is one request that takes minutes, and a page that only says
"Rendering..." reads the same as a hang. The job reports each step here as it reaches it; the
page asks every second and fills a bar.

In memory, per project and job, and only while the job runs. It is a view of
work in progress, not a record: nothing is lost if the server restarts, because
the job it described has stopped too.
"""

from __future__ import annotations

import threading
import time
from typing import Any

_lock = threading.Lock()
_jobs: dict[tuple[str, str], dict[str, Any]] = {}


def report(slug: str, job: str, done: int, total: int, label: str = "") -> None:
    """The job has finished `done` of its `total` steps; `label` is the one now under way."""
    with _lock:
        entry = _jobs.setdefault((slug, job), {"started_at": time.time()})
        entry.update(done=done, total=total, label=label)


def claim(slug: str, job: str, label: str = "") -> bool:
    """Start reporting a job, unless it is already running. Checked and taken
    in one step, so two requests at once cannot both start it."""
    with _lock:
        if (slug, job) in _jobs:
            return False
        _jobs[(slug, job)] = {"started_at": time.time(), "done": 0, "total": 0, "label": label}
        return True


def finish(slug: str, job: str) -> None:
    with _lock:
        _jobs.pop((slug, job), None)


def running() -> list[dict[str, Any]]:
    """Every job running now, in any project, oldest first."""
    with _lock:
        entries = sorted(_jobs.items(), key=lambda item: item[1]["started_at"])
        return [
            {"slug": slug, "job": job, "done": entry["done"], "total": entry["total"],
             "label": entry["label"], "elapsed_seconds": round(time.time() - entry["started_at"])}
            for (slug, job), entry in entries
        ]


def read(slug: str, job: str) -> dict[str, Any]:
    with _lock:
        entry = _jobs.get((slug, job))
        if entry is None:
            return {"active": False, "done": 0, "total": 0, "label": "", "elapsed_seconds": 0}
        return {
            "active": True, "done": entry["done"], "total": entry["total"],
            "label": entry["label"],
            "elapsed_seconds": round(time.time() - entry["started_at"]),
        }
