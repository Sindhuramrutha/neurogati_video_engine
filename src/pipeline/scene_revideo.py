"""A Revideo / Motion Canvas scene an agent wrote: `scene.tsx`, rendered by the
same headless renderer the diagram kinds use (`renderers/revideo/render.mjs`).

The scene is compiled inside `renderers/revideo` -- in a working folder of its
own under `agent/` -- because that is where its packages resolve: a `.tsx` in the
project folder could not import `@revideo/2d`. The working folder gets the
scene's own `.ts`/`.tsx` files, a project file, a tsconfig (without one, JSX
compiles to `React.createElement` and the page dies with "Navigating frame was
detached"), copies of the pictures its brief offers, and `kit.ts`:

    import {brief, look, seconds, pictures, when, until, finish} from './kit';

    export default makeScene2D(function* (view) {
      view.add(<Txt ref={title} text="Body image" fill={look.text} fontSize={64} />);
      yield* until(when('sensors'));       // the moment the word is spoken
      ...
      yield* finish();                     // ends at exactly brief.seconds
    });

Revideo does not report its text or its kinds of motion, so a revideo scene's
text and motion are judged from its frames by the visual review, and the text
checks say so (a warning) rather than pretending to have measured.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Any

from pipeline import project_work
from pipeline.config import REPO_ROOT

RENDERER = REPO_ROOT / "renderers" / "revideo"
ENTRY = "scene.tsx"
COPIED = {".ts", ".tsx", ".css"}

KIT = """import {useThread, waitFor} from '@revideo/core';

export const brief: any = __BRIEF__;
export const look: Record<string, string> = brief.look ?? {};
export const seconds: number = brief.seconds;
export const width: number = brief.width;
export const height: number = brief.height;
/** The pictures the brief offers, as URLs an <Img src=...> can load. */
export const pictures: string[] = __PICTURES__;
export const font: string = `${look.body_font || 'Segoe UI'}, Arial, sans-serif`;

/** The project's font for every text in the scene: call it first. (Not the
 *  view's fill -- that is the background; give each Txt fill={look.text}.) */
export function prepare(view: any) {
  view.fontFamily(font);
}

const words = (text: string) => (String(text).toLowerCase().match(/[a-z0-9']+/g) ?? []);
const spoken: [number, string][] = [];
(brief.words ?? []).forEach((w: any, i: number) => words(w.text).forEach(p => spoken.push([i, p])));

/** The second these words start being spoken. */
export function when(phrase: string, fallback?: number): number {
  const wanted = words(phrase);
  for (let s = 0; s + wanted.length <= spoken.length; s++) {
    if (wanted.every((w, k) => spoken[s + k][1] === w)) {
      return brief.words[spoken[s][0]].start_ms / 1000;
    }
  }
  if (fallback !== undefined) return fallback;
  const said = words(brief.narration ?? '');
  for (let s = 0; s + wanted.length <= said.length; s++) {
    if (wanted.every((w, k) => said[s + k] === w)) return seconds * s / Math.max(1, said.length);
  }
  return 0;
}

/** Wait until `t` seconds into the scene. */
export function* until(t: number) {
  const now = useThread().time();
  if (t > now) yield* waitFor(t - now);
}

/** End at exactly the narration's length. */
export function* finish() {
  yield* until(seconds);
}
"""

PROJECT = """import {makeProject} from '@revideo/core';
import scene from './scene';

declare const PIPELINE_FRAME: {width: number; height: number; rate: number};
const frame = typeof PIPELINE_FRAME === 'undefined' ? {width: 1920, height: 1080, rate: 30}
  : PIPELINE_FRAME;

export default makeProject({
  name: 'agent-scene',
  scenes: [scene],
  settings: {
    shared: {background: __BACKGROUND__, range: [0, Infinity],
             size: {x: frame.width, y: frame.height}},
    preview: {fps: frame.rate, resolutionScale: 1},
    rendering: {exporter: {name: '@revideo/core/wasm'}, fps: frame.rate, resolutionScale: 1,
                colorSpace: 'srgb'},
  },
});
"""

PRAGMA = "/** @jsxImportSource @revideo/2d/lib */"
# Revideo's makeScene2D takes a name first; Motion Canvas's does not. A scene
# written the Motion Canvas way fails deep in the renderer with "Cannot read
# properties of undefined (reading 'name')", so the name is put in for it.
UNNAMED_SCENE = re.compile(r"makeScene2D\(\s*(function|\()")


def _chromium() -> str:
    """The Chromium Playwright installed: Puppeteer is pointed at it rather than at
    the exact Chrome build it was released with, which is often not on the machine."""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            return playwright.chromium.executable_path
    except Exception:
        return ""


def is_installed() -> bool:
    return bool(shutil.which("node")) and (RENDERER / "node_modules" / "@revideo").exists()


def _working_folder(folder: Path, brief: dict[str, Any]) -> tuple[Path, str]:
    name = uuid.uuid4().hex[:12]
    working = RENDERER / "agent" / name
    (working / "pictures").mkdir(parents=True)
    for path in folder.iterdir():
        if path.is_file() and path.suffix in COPIED:
            shutil.copy(path, working / path.name)
    scene = working / ENTRY
    code = scene.read_text(encoding="utf-8")
    code = UNNAMED_SCENE.sub(lambda found: f"makeScene2D('scene', {found.group(1)}", code)
    if "@jsxImportSource" not in code:
        code = f"{PRAGMA}\n{code}"
    scene.write_text(code, encoding="utf-8")
    urls = []
    for index, picture in enumerate(brief.get("assets", {}).get("pictures", [])):
        source = Path(picture)
        if source.exists():
            shutil.copy(source, working / "pictures" / f"{index}{source.suffix}")
            urls.append(f"/agent/{name}/pictures/{index}{source.suffix}")
    (working / "kit.ts").write_text(
        KIT.replace("__BRIEF__", json.dumps(brief, ensure_ascii=False))
           .replace("__PICTURES__", json.dumps(urls)), encoding="utf-8")
    (working / "project.ts").write_text(PROJECT.replace(
        "__BACKGROUND__", json.dumps(brief.get("look", {}).get("background", "#0D0F14"))),
        encoding="utf-8")
    config = json.loads((RENDERER / "tsconfig.json").read_text(encoding="utf-8"))
    config.pop("//", None)
    config["include"] = ["*.ts", "*.tsx"]
    (working / "tsconfig.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    return working, name


def render_revideo(folder: Path, brief: dict[str, Any], seconds_limit: int) -> dict[str, Any]:
    """Render scene.tsx to render.mp4; report like a script run."""
    from pipeline.scene_lab import SCENE_ENVIRONMENT

    (folder / "render.mp4").unlink(missing_ok=True)
    if not is_installed():
        return {"code": 1, "timed_out": False, "log": "Revideo is not installed: run "
                "`npm install` in renderers/revideo (Node is needed)."}
    working, name = _working_folder(folder, brief)
    spec = {"project": f"./agent/{name}/project.ts", "seconds": brief["seconds"],
            "width": brief["width"], "height": brief["height"], "frameRate": brief["fps"],
            "output": str(folder / "render.mp4"),
            "timeoutMs": max(60, seconds_limit - 30) * 1000, "gpu": True}
    environment = {k: v for k, v in os.environ.items() if k.upper() in SCENE_ENVIRONMENT}
    chromium = os.environ.get("PUPPETEER_EXECUTABLE_PATH") or _chromium()
    if chromium:
        environment["PUPPETEER_EXECUTABLE_PATH"] = chromium
    try:
        done = project_work.run(
            [shutil.which("node"), "render.mjs"], cwd=RENDERER, input=json.dumps(spec),
            timeout=seconds_limit, env=environment)
        log = (done.stdout + "\n" + done.stderr).strip()
        code, timed_out = done.returncode, False
    except subprocess.TimeoutExpired:
        log, code, timed_out = f"Stopped: it did not finish in {seconds_limit} seconds.", 1, True
    finally:
        shutil.rmtree(working, ignore_errors=True)
    if code == 0 and not (folder / "render.mp4").exists():
        code = 1
        log += "\nThe renderer finished but wrote no clip."
    return {"code": code, "timed_out": timed_out, "log": log}
