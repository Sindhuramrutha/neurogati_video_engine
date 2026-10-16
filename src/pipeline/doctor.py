"""Before a job spends anything: is everything it needs here and working?

Demo 001 met, one after another, a missing folder, a voice service that would
not answer, and a machine so short of memory that ffmpeg could not open its
encoder and Manim could not allocate. Each was found by the job that hit it,
minutes or hours in. The doctor asks first.

- **Quick checks** (well under a second): the tools on PATH, free disk where
  projects and working files go, free memory, and that both can be written.
  Run before every render and before scenes are made; a job does not start
  when one fails, and says what to do.
- **Deep checks** (`pipeline doctor --deep`, or `GET /api/doctor?deep=1`): a real
  one-second encode, the scene environment (Manim importable through uv), and
  one small call each to the model, the vision model and the voice.

Working files go where `config.use_work_dir` puts them (`.cache/tmp`, or
`PIPELINE_TEMP`); the doctor only checks that folder.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from pipeline.config import get_settings
from pipeline.core import OperationFailed, projects_root

PASS, WARN, FAIL = "pass", "warn", "fail"
DISK_FAIL_GB, DISK_WARN_GB = 2.0, 8.0
MEMORY_FAIL_GB, MEMORY_WARN_GB = 1.0, 3.0


def _check(key: str, name: str, status: str, detail: str, fix: str = "") -> dict[str, str]:
    return {"key": key, "name": name, "status": status, "detail": detail,
            "fix": fix if status != PASS else ""}


def _grade(value: float, fail_below: float, warn_below: float) -> str:
    return FAIL if value < fail_below else WARN if value < warn_below else PASS


def _answers(key: str, name: str, call: Callable[[], str], fix: str) -> dict[str, str]:
    """One call to an outside service: PASS with what it said, or FAIL with why."""
    try:
        return _check(key, name, PASS, call())
    except Exception as failure:
        return _check(key, name, FAIL, str(failure)[:300], fix)


class _Ping(BaseModel):
    ok: bool


def _probe(suffix: str) -> Path:
    return get_settings().work_dir / f"doctor-{os.getpid()}{suffix}"


# --- quick checks --------------------------------------------------------------------------

def _tools() -> list[dict[str, str]]:
    found = []
    for tool, why in (("ffmpeg", "renders and joins every video"),
                      ("ffprobe", "measures audio and video"),
                      ("uv", "runs each scene program in its own environment")):
        where = shutil.which(tool)
        found.append(_check(f"tool-{tool}", f"{tool} is installed",
                            PASS if where else FAIL,
                            where or f"Not found on PATH; it {why}.",
                            f"Install {tool} and make sure it is on PATH, then restart."))
    return found


def _disk(label: str, folder: Path) -> dict[str, str]:
    free = shutil.disk_usage(folder).free / 1e9
    return _check(f"disk-{label}", f"Free disk for {label}",
                  _grade(free, DISK_FAIL_GB, DISK_WARN_GB),
                  f"{free:.1f} GB free at {folder.anchor or folder}.",
                  f"Free space on that drive (at least {DISK_WARN_GB:.0f} GB): a full drive "
                  "stops renders mid-way, and on Windows it also starves memory.")


def _available_memory_gb() -> float | None:
    """Memory a new allocation can get: on Windows the commit still available
    (what 'Memory allocation failed' ran out of), elsewhere MemAvailable."""
    if sys.platform == "win32":
        import ctypes

        class Status(ctypes.Structure):
            _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong),
                        ("total_phys", ctypes.c_ulonglong), ("avail_phys", ctypes.c_ulonglong),
                        ("total_page", ctypes.c_ulonglong), ("avail_page", ctypes.c_ulonglong),
                        ("total_virtual", ctypes.c_ulonglong),
                        ("avail_virtual", ctypes.c_ulonglong),
                        ("avail_extended", ctypes.c_ulonglong)]
        status = Status()
        status.length = ctypes.sizeof(Status)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return None
        return status.avail_page / 1e9
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) / 1e6
    except OSError:
        return None
    return None


def _memory() -> dict[str, str]:
    free = _available_memory_gb()
    if free is None:
        return _check("memory", "Free memory", WARN, "Could not be measured on this system.")
    return _check("memory", "Free memory", _grade(free, MEMORY_FAIL_GB, MEMORY_WARN_GB),
                  f"{free:.1f} GB available.",
                  "Close other programs (browsers, editors) or free space on the system "
                  "drive; renders and scene programs fail to allocate below about 1 GB.")


def _writable(label: str, folder: Path) -> dict[str, str]:
    try:
        folder.mkdir(parents=True, exist_ok=True)
        probe = folder / f".doctor-{os.getpid()}"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return _check(f"write-{label}", f"Can write {label}", PASS, str(folder))
    except OSError as refused:
        return _check(f"write-{label}", f"Can write {label}", FAIL, f"{folder}: {refused}",
                      "Check the folder's permissions, or that the drive is not full.")


def quick() -> list[dict[str, str]]:
    folders = {"projects": projects_root(), "working files": get_settings().work_dir}
    written = [_writable(label, folder) for label, folder in folders.items()]
    # Measured only where the folder exists; a folder that cannot be made already fails.
    disks = [_disk(label, folder) for label, folder in folders.items() if folder.is_dir()]
    return [*_tools(), *disks, _memory(), *written]


# --- deep checks ---------------------------------------------------------------------------

def _encode() -> dict[str, str]:
    from pipeline.rendering import FRAME_HEIGHT, FRAME_RATE, FRAME_WIDTH, WORKING_VIDEO

    key, name = "encode", "A 1080p video can be encoded"
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return _check(key, name, FAIL, "ffmpeg is missing.")
    target = _probe(".mp4")
    done = subprocess.run([ffmpeg, "-v", "error", "-y", "-f", "lavfi", "-i",
                           f"color=c=blue:s={FRAME_WIDTH}x{FRAME_HEIGHT}:d=1:r={FRAME_RATE}",
                           *WORKING_VIDEO, "-pix_fmt", "yuv420p", str(target)],
                          capture_output=True, text=True, timeout=120)
    ok = done.returncode == 0 and target.exists() and target.stat().st_size > 0
    target.unlink(missing_ok=True)
    return _check(key, name, PASS if ok else FAIL,
                  "Encoded one second." if ok else (done.stderr or "no output")[-300:],
                  "Usually memory: close programs and try again.")


SCENE_PROBE = ('# /// script\n# requires-python = ">=3.11"\n'
               '# dependencies = ["manim>=0.19", "pillow<13"]\n# ///\n'
               "import manim\nprint(manim.__version__)\n")


def _scene_environment() -> dict[str, str]:
    from pipeline.scene_lab import _command

    key, name = "scenes", "Scene programs can run (Manim through uv)"
    if not shutil.which("uv"):
        return _check(key, name, FAIL, "uv is missing.")
    folder = _probe("-scene")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "scene.py").write_text(SCENE_PROBE, encoding="utf-8")
    try:
        # The command a real scene runs with, so the probe passes and fails as scenes do.
        done = subprocess.run(_command(folder), cwd=folder, capture_output=True, text=True,
                              timeout=600)
    except subprocess.TimeoutExpired:
        return _check(key, name, FAIL, "uv took over 10 minutes.",
                      "Check the network (uv downloads Manim once), then try again.")
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    ok = done.returncode == 0
    return _check(key, name, PASS if ok else FAIL,
                  f"Manim {done.stdout.strip()}" if ok else (done.stderr or "")[-300:],
                  "Run `uv run --script` on a scene by hand to see the error.")


def _text_model() -> dict[str, str]:
    from pipeline import llm

    model = get_settings().ir_llm[2]

    def ask() -> str:
        llm.complete_structured(_Ping, "Answer with ok true.", "Are you there?",
                                max_tokens=2000)
        return f"{model} answered."

    return _answers("model", "The writing model answers", ask,
                    "Check the key and the provider's status page.")


def _vision_model() -> dict[str, str]:
    import io

    from PIL import Image

    from pipeline import llm

    model = get_settings().vision_model

    def ask() -> str:
        buffer = io.BytesIO()
        Image.new("RGB", (64, 64), (40, 90, 200)).save(buffer, format="JPEG")
        llm.complete_structured_with_images(_Ping, "Answer with ok true.",
                                            "Is there a picture?",
                                            [("probe.jpg", buffer.getvalue())],
                                            max_tokens=llm.VISION_TOKENS)
        return f"{model} answered."

    return _answers("vision", "The vision model answers", ask,
                    "Check VISION_MODEL and the key.")


def _voice() -> dict[str, str]:
    from pipeline.speech import describe_voice_providers, synthesise_narration

    key, name = "voice", "The narration voice answers"
    voice = describe_voice_providers()["recommended"]   # the one a render would use
    if voice == "silent":
        return _check(key, name, WARN, "No voice is ready; renders would be silent.",
                      "Run `pipeline voices` to see what each voice needs.")
    target = _probe(".mp3")

    def speak() -> str:
        started = time.monotonic()
        try:
            synthesise_narration("This is a test of the narration voice.", target, voice, "")
        finally:
            target.unlink(missing_ok=True)
        return f"{voice} spoke a sentence in {time.monotonic() - started:.1f} s."

    return _answers(key, name, speak, "Check the network; renders wait and resume by "
                    "themselves if it comes back.")


def deep() -> list[dict[str, str]]:
    with ThreadPoolExecutor() as pool:
        # The services answer side by side; the encode and Manim stay one at a time,
        # because both need the memory a short machine does not have twice.
        calls = [pool.submit(check) for check in (_text_model, _vision_model, _voice)]
        local = [_encode(), _scene_environment()]
        return [*quick(), *local, *(call.result() for call in calls)]


# --- for clients and jobs ------------------------------------------------------------------

def check_readiness(deep_checks: bool = False) -> dict[str, Any]:
    """The doctor's answer, for every client: the worst status and every check."""
    checks = deep() if deep_checks else quick()
    worst = next((s for s in (FAIL, WARN) if any(c["status"] == s for c in checks)), PASS)
    return {"status": worst, "checks": checks}


class NotReady(OperationFailed):
    """A quick check failed. Said like any refusal (an OperationFailed), but
    transient: memory and disk can be freed, and a render waiting on it resumes
    by itself (render_queue)."""

    transient = True


def require_ready(job: str) -> list[dict[str, str]]:
    """Run the quick checks before `job`; raise NotReady naming every failure and
    its fix. Returns the checks (warnings included) when the job may start."""
    checks = quick()
    failing = [c for c in checks if c["status"] == FAIL]
    if failing:
        raise NotReady(f"{job} cannot start yet: " + " ".join(
            f"{c['name']}: {c['detail']} {c['fix']}".strip() for c in failing))
    return checks
