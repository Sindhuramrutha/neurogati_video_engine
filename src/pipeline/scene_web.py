"""A web page as a scene: `scene.html`, animated with GSAP / D3 / three.js /
anime.js through `resources/code/webkit.js`, recorded frame by frame.

Headless Chromium (Playwright) opens the page at a private address that only
this recorder answers: the scene's own files, the animation libraries installed
under `renderers/web/node_modules`, the kit, and the pictures its brief offers.
Every other request -- the internet included -- is refused, so a scene renders
the same offline as online and cannot reach anything else.

Time is driven, not waited for: for each frame the recorder calls the page's
`seek(t)` and takes a screenshot, and ffmpeg encodes the frames at the brief's
rate -- so the clip is exactly the narration's length however slow the page is.
At every second the page reports what is on screen (`layout.json`), so the same
text checks apply as to a Manim scene, and its timelines report their kinds of
motion for the motion check.
"""

from __future__ import annotations

import json
import mimetypes
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from pipeline import project_work
from pipeline.config import REPO_ROOT

HOST = "http://scene.local"
ENTRY = "scene.html"
LIBRARIES = REPO_ROOT / "renderers" / "web" / "node_modules"
KIT = REPO_ROOT / "resources" / "code" / "webkit.js"
LIBRARY_FILES = {
    "gsap.js": "gsap/dist/gsap.min.js",
    "d3.js": "d3/dist/d3.min.js",
    "anime.js": "animejs/lib/anime.min.js",
    "three.js": "three/build/three.module.min.js",
}
GSAP_PLUGINS = {"MotionPathPlugin", "MorphSVGPlugin", "DrawSVGPlugin", "SplitText",
                "TextPlugin", "Flip", "CustomEase"}
SNAPSHOT_EVERY_SECONDS = 1.0
READY_TIMEOUT_MS = 30000


def is_installed() -> bool:
    return all((LIBRARIES / path).exists() for path in LIBRARY_FILES.values())


def _library(path: str) -> Path | None:
    name = path.removeprefix("/lib/")
    if name in LIBRARY_FILES:
        return LIBRARIES / LIBRARY_FILES[name]
    if name.startswith("gsap/") and Path(name).stem in GSAP_PLUGINS:
        return LIBRARIES / "gsap" / "dist" / f"{Path(name).stem}.min.js"
    return None


def _answer(folder: Path, brief: dict[str, Any], url: str) -> Path | None:
    """The one file a request may have, or None (refused)."""
    parsed = urlparse(url)
    if f"{parsed.scheme}://{parsed.netloc}" != HOST:
        return None
    path = unquote(parsed.path)
    if path.startswith("/lib/"):
        return _library(path)
    if path == "/kit/webkit.js":
        return KIT
    if path == "/picture":
        wanted = parse_qs(parsed.query).get("path", [""])[0]
        offered = {*brief.get("assets", {}).get("pictures", []), brief.get("slide_image", "")}
        return Path(wanted) if wanted and wanted in offered else None
    target = (folder / path.lstrip("/")).resolve()
    return target if target.is_relative_to(folder.resolve()) and target.is_file() else None


def render_web(folder: Path, brief: dict[str, Any], seconds_limit: int) -> dict[str, Any]:
    """Record scene.html to render.mp4 and write layout.json; report like a script run."""
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright

    started = time.monotonic()
    log: list[str] = []
    (folder / "render.mp4").unlink(missing_ok=True)
    if not is_installed():
        return {"code": 1, "timed_out": False, "log": "The web animation libraries are not "
                "installed: run `npm install` in renderers/web."}
    ffmpeg = shutil.which("ffmpeg")
    fps, width, height = brief["fps"], brief["width"], brief["height"]
    frames = max(1, round(brief["seconds"] * fps))

    def route(handle) -> None:
        found = _answer(folder, brief, handle.request.url)
        if found is None or not found.exists():
            log.append(f"refused: {handle.request.url}")
            handle.abort()
            return
        kind = mimetypes.guess_type(found.name)[0] or "application/octet-stream"
        if found.suffix in (".js", ".mjs"):
            kind = "text/javascript"
        handle.fulfill(status=200, body=found.read_bytes(), content_type=kind)

    encoder = subprocess.Popen(
        [ffmpeg, "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(fps), "-i", "-",
         "-c:v", "libx264", "-threads", "4", "-pix_fmt", "yuv420p", "-r", str(fps),
         str(folder / "render.mp4")],
        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    project_work.register(encoder)
    snapshots, plays, code, timed_out = [], None, 0, False
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": width, "height": height},
                                    device_scale_factor=1)
            page.on("console", lambda m: log.append(f"console.{m.type}: {m.text}"))
            page.on("pageerror", lambda e: log.append(f"page error: {e}"))
            page.route("**/*", route)
            page.goto(f"{HOST}/{ENTRY}")
            page.wait_for_function("window.__kitReady === true", timeout=READY_TIMEOUT_MS)
            next_snapshot = 0.0
            for index in range(frames):
                if project_work.stopped():
                    code = 1
                    log.append("Stopped: the project is being deleted.")
                    break
                if time.monotonic() - started > seconds_limit:
                    timed_out, code = True, 1
                    break
                at = index / fps
                page.evaluate("t => window.__kit.seek(t)", at)
                encoder.stdin.write(page.screenshot(type="jpeg", quality=92))
                if at >= next_snapshot:
                    snapshots.append(page.evaluate("t => window.__kit.snapshot(t)", at))
                    next_snapshot += SNAPSHOT_EVERY_SECONDS
            plays = page.evaluate("window.__kit.motions()")
            browser.close()
    except (PlaywrightError, OSError) as broke:
        code = 1
        log.append(f"{type(broke).__name__}: {str(broke).splitlines()[0][:400]}")
    finally:
        encoder.stdin.close()
        problem = encoder.stderr.read().decode(errors="replace")
        encoder.wait(timeout=120)
        if problem.strip():
            log.append(f"ffmpeg: {problem.strip()[:400]}")
    (folder / "layout.json").write_text(json.dumps(
        {"renderer": "web", "width": width, "height": height, "snapshots": snapshots,
         "plays": plays}, indent=1, ensure_ascii=False), encoding="utf-8")
    if any(line.startswith("page error") for line in log):
        code = code or 1
    text = "\n".join(log)
    if timed_out:
        text += f"\n\nStopped: it did not finish in {seconds_limit} seconds."
    return {"code": code, "timed_out": timed_out, "log": text}
