"""The things that can draw a scene, and what each of them can do.

One shot, several ways to make it. A labelled diagram can be a still drawn with
Pillow, the same diagram assembled a node at a time by Manim, or a full motion
graphic from a Motion Canvas scene -- and which of those is possible depends on
what is installed on the machine, not on what the project wants.

So a renderer declares itself the way a voice provider does: a key, what it can
draw, whether it is installed, and the command that installs it. The pipeline
asks for the best renderer that can draw a given scene and falls back to one that
can, saying which it used. A project renders on a bare checkout with Pillow and
ffmpeg; the same project renders with animation when Manim is there; nothing
silently produces less than it claimed.

Two capabilities matter and they are different:

- `stills` -- one frame, which the renderer above composites and moves a camera
  over. Everything can do this.
- `animated_diagram` -- a clip where the picture itself changes: an arrow drawn
  as it is described, a node appearing as it is named. This is the thing ffmpeg
  and Pillow cannot do, and the reason a second backend exists at all.

**And a renderer that can animate is asked *what* it can animate.** The first
version of this asked one question -- can you animate? -- and got one answer, so
a backend that drew boxes and arrows was treated as able to draw anything. There
are fourteen kinds of scene here (`SCENE_KINDS`), each declared per renderer and
each provable on its own: a machine whose Manim cannot typeset a formula can
still build every flow, plot and timeline in the video, and Generation is told
exactly that rather than being told "animation works" and finding out per scene.
"""

from __future__ import annotations

import importlib.util
import logging
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pipeline.rendering import FRAME_HEIGHT, FRAME_RATE, FRAME_WIDTH, RenderStyle

logger = logging.getLogger(__name__)

# A scene renderer that has not finished in this long has failed in a way that
# matters: a video is many scenes, and one that hangs takes the whole render.
RENDER_TIMEOUT_SECONDS = 240


class Capability:
    STILLS = "stills"
    ANIMATED_DIAGRAM = "animated_diagram"


# What the Motion Canvas scene in `renderers/revideo` implements. Fewer than
# Manim, and deliberately: it is here for the kinds a browser does better, not
# to reimplement a plotting library in TypeScript.
#
# `formula` is the one that matters. Revideo typesets with MathJax, in the page,
# so a machine with no TeX distribution still gets real mathematics -- Manim's
# `MathTex` needs `latex` on PATH and falls back to plain text without it. That
# is the whole argument for keeping a second backend alive.
REVIDEO_KINDS = ("flow", "compare", "stack", "cycle", "timeline", "counter",
                 "morph", "formula", "code")


def _why_it_failed(stderr: str) -> str:
    """The line of a renderer's output that says what went wrong.

    The last line is usually the version banner -- a failure reported as
    "Node.js v22.20.0" tells nobody anything -- so the first line that looks
    like an error wins, and the tail is the fallback.
    """
    lines = [line.strip() for line in (stderr or "").splitlines() if line.strip()]
    for line in lines:
        if any(marker in line for marker in
               ("Error:", "error:", "Exception", "Traceback", "TypeError", "failed")):
            return line[:240]
    return (lines[-1][:240] if lines else "")


# The shapes a piece of teaching takes, and what each one needs before it can be
# drawn. A kind is in this list because something in a real lecture looks like
# it, not because a renderer happens to have a class for it.
SCENE_KINDS: dict[str, str] = {
    "flow": "a sequence of steps, each leading to the next",
    "compare": "two or three things set against each other",
    "stack": "layers, one resting on another",
    "cycle": "a loop that returns to where it started",
    "tree": "a hierarchy branching from one root",
    "graph": "things connected to each other in no particular order",
    "plot": "a function of one variable, drawn as a curve",
    "bars": "stated quantities set beside each other",
    "timeline": "events in the order they happened",
    "table": "rows of values under headings",
    "counter": "one number moving from where it starts to where it ends",
    "formula": "an expression, written out and then rearranged",
    "figure": "the source's own picture, with this scene's labels beside it",
    "morph": "one thing becoming another",
    "code": "source code, read a line at a time",
}

# What each kind cannot be drawn without. A spec that does not carry these is
# not drawable, and saying so here -- rather than finding out in a subprocess
# four seconds later -- is what stops a scene silently flattening.
NEEDS: dict[str, tuple[str, ...]] = {
    "flow": ("nodes",), "compare": ("nodes",), "stack": ("nodes",), "cycle": ("nodes",),
    "tree": ("nodes",), "graph": ("nodes",), "timeline": ("nodes",), "morph": ("nodes",),
    "table": ("nodes",),
    "plot": ("expression",),
    "bars": ("values",), "counter": ("values",),
    "formula": ("formula",),
    "figure": ("image",),
    "code": ("code",),
}



@dataclass(frozen=True)
class SceneRenderer:
    """One way of drawing a scene, and what it needs to be usable."""

    key: str
    label: str
    summary: str
    capabilities: tuple[str, ...]

    # Which of `SCENE_KINDS` this renderer says it can draw. Empty for a
    # renderer that only draws stills.
    kinds: tuple[str, ...] = ()

    # Roughly what one scene costs, measured. Used to choose between two
    # renderers that can both draw a kind, which is most of them.
    typical_seconds: int = 0

    required_module: str = ""          # a Python import that must succeed
    required_command: str = ""         # an executable that must be on PATH
    required_path: str = ""            # a folder, relative to the repo, that must exist
    install_command: str = ""

    def is_installed(self) -> bool:
        """Whether its parts are on the machine. Says nothing about whether it works."""
        from pipeline.config import REPO_ROOT

        if self.required_module and importlib.util.find_spec(self.required_module) is None:
            return False
        if self.required_command and not shutil.which(self.required_command):
            return False
        return not (self.required_path and not (REPO_ROOT / self.required_path).exists())

    def is_available(self) -> bool:
        """Installed, and not known to fail here.

        A renderer that failed its self-test is not used again until it passes
        one: picking it per scene would mean paying for a failed subprocess on
        every shot and flattening the diagram anyway.
        """
        if not self.is_installed():
            return False
        recorded = _self_test_results().get(self.key)
        return True if recorded is None else bool(recorded.get("ok"))

    def can(self, capability: str) -> bool:
        return capability in self.capabilities

    def can_draw(self, kind: str) -> bool:
        """Whether this renderer will actually draw this kind of scene here.

        Claimed, available, and not recorded as having failed at this kind. A
        kind nobody has probed is allowed: the alternative is refusing to
        animate anything until somebody runs fourteen probes, which would make
        the honest answer indistinguishable from the broken one.
        """
        if kind not in self.kinds or not self.is_available():
            return False
        recorded = (_self_test_results().get(self.key, {}).get("kinds") or {}).get(kind)
        return True if recorded is None else bool(recorded.get("ok"))

    def probe_command(self, kind: str) -> list[str]:
        """How to ask this renderer to draw the smallest real example of one kind.

        The example lives with the renderer that draws it -- each backend knows
        what a minimal scene of each kind looks like in its own terms, and a
        probe written here would be a second opinion about that.
        """
        import sys

        from pipeline.config import REPO_ROOT

        if self.key == "manim":
            return [sys.executable, str(REPO_ROOT / "renderers" / "manim_scenes.py"),
                    "--probe", kind]
        if self.key == "revideo":
            return ["node", "render.mjs", "--probe", kind]
        return []

    def to_dict(self) -> dict[str, Any]:
        recorded = _self_test_results().get(self.key) or {}
        return {
            "key": self.key,
            "label": self.label,
            "summary": self.summary,
            "capabilities": list(self.capabilities),
            "kinds": list(self.kinds),
            "drawable_kinds": [kind for kind in self.kinds if self.can_draw(kind)],
            "is_installed": self.is_installed(),
            "is_available": self.is_available(),
            "install_command": self.install_command,
            "self_test": {
                "checked": bool(recorded),
                "ok": bool(recorded.get("ok")),
                "detail": recorded.get("detail", ""),
                "checked_at": recorded.get("checked_at", ""),
                "kinds": recorded.get("kinds") or {},
            },
        }


RENDERERS: tuple[SceneRenderer, ...] = (
    SceneRenderer(
        key="stills",
        label="Stills (Pillow + ffmpeg)",
        summary="Draws every scene as a frame and moves a camera over it. Always "
                "available; it is what the pipeline ships with.",
        capabilities=(Capability.STILLS,),
    ),
    SceneRenderer(
        key="manim",
        label="Manim (animated diagrams)",
        summary="Builds a scene a piece at a time -- steps arriving as they are "
                "named, a curve drawn as it is described, a number counting up. "
                "Every kind, in Python, with no browser.",
        capabilities=(Capability.STILLS, Capability.ANIMATED_DIAGRAM),
        kinds=tuple(SCENE_KINDS),
        typical_seconds=3,
        required_module="manim",
        install_command="uv sync --extra animation",
    ),
    SceneRenderer(
        key="revideo",
        label="Revideo / Motion Canvas",
        summary="A TypeScript scene renderer driven headlessly, with spring "
                "motion and typography Manim has no equivalent for. The "
                "heaviest of the three: Node, a package install and a browser.",
        capabilities=(Capability.STILLS, Capability.ANIMATED_DIAGRAM),
        kinds=REVIDEO_KINDS,
        # Forty seconds a scene against Manim's three: it starts a vite server
        # and a browser for every clip. Measured, not guessed.
        typical_seconds=40,
        required_command="node",
        required_path="renderers/revideo/node_modules",
        install_command="cd renderers/revideo && npm install",
    ),
)

BY_KEY: dict[str, SceneRenderer] = {renderer.key: renderer for renderer in RENDERERS}


def describe_scene_renderers() -> dict[str, Any]:
    """What can draw a scene here, and what is missing to do more.

    Shown rather than hidden: a project that renders flat because Manim is not
    installed should say so, with the one command that changes it.
    """
    available = [renderer for renderer in RENDERERS if renderer.is_available()]
    animating = [r for r in available if r.can(Capability.ANIMATED_DIAGRAM)]
    drawable = drawable_kinds()
    return {
        "renderers": [renderer.to_dict() for renderer in RENDERERS],
        "available": [renderer.key for renderer in available],
        "can_animate": bool(animating),
        "preferred_animator": animating[-1].key if animating else "",
        "kinds": [{"kind": kind, "describes": describes,
                   "is_drawable": kind in drawable,
                   "drawn_by": drawable.get(kind, "")}
                  for kind, describes in SCENE_KINDS.items()],
        "drawable_kinds": sorted(drawable),
        "has_latex": has_latex(),
    }


def drawable_kinds() -> dict[str, str]:
    """Every kind of scene that can actually be animated here, and by what.

    What Generation is allowed to ask for. Composing a formula scene on a
    machine that cannot draw one produces a still of a formula, which is worse
    than having composed a flow that would have moved.
    """
    found: dict[str, str] = {}
    for kind in SCENE_KINDS:
        chosen = renderer_for_kind(kind)
        if chosen is not None:
            found[kind] = chosen.key
    return found


def has_latex() -> bool:
    """Whether a TeX distribution is on PATH.

    Decides who draws a formula: Manim's `MathTex` needs one and reads as plain
    text without it, while Revideo typesets with MathJax in the page and needs
    nothing installed.
    """
    return bool(shutil.which("latex") or shutil.which("xelatex")
                or shutil.which("pdflatex"))


# Kinds where the slower renderer is chosen anyway, because it is doing
# something the faster one cannot -- with the condition under which that is
# true. Without an entry here, cost decides.
BETTER_DESPITE_COST: dict[str, tuple[str, Callable[[], bool]]] = {
    "formula": ("revideo", lambda: not has_latex()),
}


def renderer_for_kind(kind: str, preferred: str = "") -> SceneRenderer | None:
    """The renderer that will draw this kind of scene, or None if nothing can.

    The cheap one wins wherever both can draw the kind, because that is nearly
    all of them and the difference is a minute against a quarter of an hour on a
    twenty-scene video. The exception is a kind where the expensive renderer is
    doing something the cheap one cannot -- a formula on a machine with no TeX
    distribution -- and that exception names its own condition rather than being
    a standing preference.
    """
    if preferred and (chosen := BY_KEY.get(preferred)) and chosen.can_draw(kind):
        return chosen

    usable = [renderer for renderer in RENDERERS if renderer.can_draw(kind)]
    if not usable:
        return None

    better, when = BETTER_DESPITE_COST.get(kind, ("", None))
    if better and when and when():
        for renderer in usable:
            if renderer.key == better:
                return renderer
    return min(usable, key=lambda renderer: renderer.typical_seconds)


def renderer_for(capability: str, preferred: str = "") -> SceneRenderer | None:
    """The renderer that will actually be used for this kind of scene.

    Later in `RENDERERS` wins, because the list is ordered by what each can do:
    a machine with Revideo installed asked for an animated diagram should get
    Revideo, and one with neither should get None rather than a still pretending
    to be an animation.
    """
    if preferred and (chosen := BY_KEY.get(preferred)) and chosen.is_available() \
            and chosen.can(capability):
        return chosen
    usable = [r for r in RENDERERS if r.is_available() and r.can(capability)]
    return usable[-1] if usable else None


@dataclass(frozen=True)
class Ran:
    """What a renderer subprocess did: its output, and whether it finished."""

    code: int
    out: str
    err: str
    timed_out: bool = False


def run_bounded(
    command: list[str], seconds: int, cwd: Path | None = None, text_in: str = ""
) -> Ran:
    """Run a renderer and come back, whatever it does.

    `subprocess.run(timeout=...)` is not enough here. It kills the process it
    started and then waits for the pipes to close -- and these processes start
    others: Revideo starts a vite server and a Chrome, Manim starts ffmpeg. A
    surviving grandchild holds the pipe open, so the call that was supposed to
    time out blocks instead, and a renderer that hung would hang the render.

    So the whole tree is killed, not the child: `taskkill /T` on Windows, the
    process group on everything else. Nothing here is allowed to cost more than
    `seconds`, because a video is many scenes and one of them must not take all
    of them.
    """
    import sys

    flags = subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
    started = subprocess.Popen(
        command, cwd=cwd, text=True,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        creationflags=flags,
        start_new_session=sys.platform != "win32",
    )
    try:
        out, err = started.communicate(text_in, timeout=seconds)
        return Ran(started.returncode, out or "", err or "")
    except subprocess.TimeoutExpired:
        _kill_tree(started.pid)
        try:
            out, err = started.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            # The pipes are still held by something that outlived the kill.
            # Reporting the timeout is worth more than waiting for it.
            out, err = "", ""
        logger.warning("%s did not finish in %ss", command[0], seconds)
        return Ran(-1, out or "", err or "", timed_out=True)


def _kill_tree(pid: int) -> None:
    import os
    import signal
    import sys

    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)],
                       capture_output=True, check=False)
        return
    try:
        os.killpg(os.getpgid(pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


def _as_hex(colour: tuple[int, int, int]) -> str:
    """A style colour the way a renderer's own configuration spells one."""
    red, green, blue = colour
    return f"#{red:02X}{green:02X}{blue:02X}"


# --- what a renderer is asked to draw -----------------------------------------------


@dataclass
class DiagramSpec:
    """A scene as data, not as a picture of one.

    Every label, number, edge and term here came from the source material, so
    whatever draws it cannot invent one: a renderer that receives three nodes
    draws three nodes. That is the difference between this and asking an image
    model for "a diagram of the acquisition chain", which produces something
    plausible and unverifiable.

    One dataclass for fourteen kinds rather than fourteen classes, because it is
    a message to a subprocess: what every field means is set by `kind`, and
    `NEEDS` says which ones that kind cannot do without.
    """

    kind: str = "flow"
    caption: str = ""

    # Boxes, steps, vertices, events, or `a|b` rows for a table.
    nodes: list[str] = field(default_factory=list)
    # Pairs of node positions, for a tree or a network.
    edges: list[list[int]] = field(default_factory=list)
    # Headings: column names, axis names, the one note under a morph.
    labels: list[str] = field(default_factory=list)

    # Quantities, for bars and for a counter's start and end.
    values: list[float] = field(default_factory=list)
    # A function of x, and the span to draw it over.
    expression: str = ""
    x_range: list[float] = field(default_factory=list)

    # An expression and the steps it is rearranged into.
    formula: str = ""
    steps: list[str] = field(default_factory=list)

    # An absolute path to the source's own picture, for `figure`.
    image: str = ""

    # Source code, and what language to highlight it as.
    code: str = ""
    language: str = ""

    @property
    def is_drawable(self) -> bool:
        """Whether this kind has what that kind needs."""
        if self.kind not in SCENE_KINDS:
            return False
        for needed in NEEDS.get(self.kind, ()):
            value = getattr(self, needed)
            if needed == "nodes" and len(value) < (1 if self.kind == "table" else 2):
                return False
            if needed == "values" and len(value) < (2 if self.kind == "counter" else 1):
                return False
            if not value:
                return False
        return True

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind, "caption": self.caption,
            "nodes": list(self.nodes), "edges": [list(edge) for edge in self.edges],
            "labels": list(self.labels), "values": [float(v) for v in self.values],
            "expression": self.expression, "x_range": [float(x) for x in self.x_range],
            "formula": self.formula, "steps": list(self.steps), "image": self.image,
            "code": self.code, "language": self.language,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any] | None) -> DiagramSpec | None:
        if not raw:
            return None

        def texts(key: str) -> list[str]:
            return [str(item).strip() for item in raw.get(key) or [] if str(item).strip()]

        def numbers(key: str) -> list[float]:
            found = []
            for item in raw.get(key) or []:
                try:
                    found.append(float(item))
                except (TypeError, ValueError):
                    continue
            return found

        edges = []
        for pair in raw.get("edges") or []:
            try:
                first, second = int(pair[0]), int(pair[1])
            except (TypeError, ValueError, IndexError):
                continue
            edges.append([first, second])

        spec = cls(
            kind=str(raw.get("kind") or "flow").strip().lower(),
            caption=str(raw.get("caption") or ""),
            nodes=texts("nodes"), edges=edges, labels=texts("labels"),
            values=numbers("values"), expression=str(raw.get("expression") or ""),
            x_range=numbers("x_range"), formula=str(raw.get("formula") or ""),
            steps=texts("steps"), image=str(raw.get("image") or ""),
            code=str(raw.get("code") or ""), language=str(raw.get("language") or ""),
        )
        return spec if spec.is_drawable else None


def render_animated_diagram(
    spec: DiagramSpec,
    output_path: Path,
    duration_ms: int,
    style: RenderStyle,
    preferred: str = "",
) -> tuple[Path | None, str]:
    """Draw the scene as a clip. Returns the clip and which renderer made it.

    Never raises: a scene that cannot be animated falls back to the still the
    caller already knows how to draw, and the reason is returned so the render
    can report it rather than quietly flattening.
    """
    renderer = renderer_for_kind(spec.kind, preferred)
    if renderer is None:
        return None, f"nothing installed here can animate a {spec.kind} scene"

    try:
        if renderer.key == "manim":
            return _render_with_manim(spec, output_path, duration_ms, style), "manim"
        if renderer.key == "revideo":
            return _render_with_revideo(spec, output_path, duration_ms, style), "revideo"
    except Exception as failure:      # a backend failing must not stop a video
        logger.warning("%s could not draw the scene: %s", renderer.key, failure)
        return None, f"{renderer.key} failed: {_why_it_failed(str(failure))}"
    return None, f"{renderer.key} cannot animate a scene"


def _payload_for(
    spec: DiagramSpec, output_path: Path, duration_ms: int, style: RenderStyle,
    frame_rate_key: str = "frame_rate",
) -> dict[str, Any]:
    return spec.to_dict() | {
        "seconds": max(1.5, duration_ms / 1000),
        "width": FRAME_WIDTH,
        "height": FRAME_HEIGHT,
        frame_rate_key: FRAME_RATE,
        "background": _as_hex(style.background_colour),
        "accent": _as_hex(style.accent_colour),
        "text": _as_hex(style.text_colour),
        "dim": _as_hex(style.dim_text_colour),
        "output": str(output_path),
    }


def _render_with_manim(
    spec: DiagramSpec, output_path: Path, duration_ms: int, style: RenderStyle
) -> Path:
    """Manim builds the scene a piece at a time, in the order it is described.

    Run in a subprocess rather than imported here. Manim configures itself
    globally -- media directory, quality, logging -- and doing that inside the
    web process would leak those settings into every later render.
    """
    import json
    import sys

    from pipeline.config import REPO_ROOT

    script = REPO_ROOT / "renderers" / "manim_scenes.py"
    ran = run_bounded(
        [sys.executable, str(script)], RENDER_TIMEOUT_SECONDS,
        text_in=json.dumps(_payload_for(spec, output_path, duration_ms, style)),
    )
    if ran.timed_out:
        raise RuntimeError(f"manim did not finish in {RENDER_TIMEOUT_SECONDS}s")
    if ran.code != 0 or not output_path.exists():
        raise RuntimeError(_why_it_failed(ran.err) or "manim produced no clip")
    return output_path


def _render_with_revideo(
    spec: DiagramSpec, output_path: Path, duration_ms: int, style: RenderStyle
) -> Path:
    """Motion Canvas, rendered headlessly through the project in `renderers/revideo`."""
    import json

    from pipeline.config import REPO_ROOT

    project = REPO_ROOT / "renderers" / "revideo"
    ran = run_bounded(
        ["node", "render.mjs"], RENDER_TIMEOUT_SECONDS, cwd=project,
        text_in=json.dumps(
            _payload_for(spec, output_path, duration_ms, style, "frameRate")),
    )
    if ran.timed_out:
        raise RuntimeError(f"revideo did not finish in {RENDER_TIMEOUT_SECONDS}s")
    if ran.code != 0 or not output_path.exists():
        raise RuntimeError(_why_it_failed(ran.err) or "revideo produced no clip")
    return output_path


# --- proving a renderer works here --------------------------------------------------

# Installed is not the same as working. Revideo installs cleanly and then fails
# to drive its headless browser on some machines; a registry that called that
# "available" would pick it for every scene, fail every time, and quietly flatten
# every diagram. So a renderer that claims to animate has to prove it once, and
# the answer is remembered.
SELF_TEST_FILE = "renderers/.self-test.json"

# How long one kind's probe may take: the same budget a real render gets. A
# probe draws two seconds at a quarter frame rate, so it should be far quicker
# -- but a renderer condemned by a *tighter* bound than the one it will actually
# run under would be recorded as unable to draw something it can. The bound is
# there to stop a hang, not to rank renderers by speed; `typical_seconds` does
# that.
PROBE_TIMEOUT_SECONDS = RENDER_TIMEOUT_SECONDS


def _self_test_results() -> dict[str, Any]:
    from pipeline.config import REPO_ROOT
    from pipeline.storage.documents import read_json_object

    return read_json_object(REPO_ROOT / SELF_TEST_FILE, "renderer self-tests") or {}


def _remember_self_test(
    key: str, ok: bool, detail: str, kinds: dict[str, Any] | None = None
) -> None:
    import json
    from datetime import UTC, datetime

    from pipeline.config import REPO_ROOT
    from pipeline.storage.documents import write_text_atomically

    results = _self_test_results()
    previous = results.get(key) or {}
    results[key] = {
        "ok": ok,
        "detail": detail,
        "checked_at": datetime.now(UTC).isoformat(timespec="seconds"),
        # Merged rather than replaced: verifying one kind must not forget what
        # is known about the other thirteen.
        "kinds": (previous.get("kinds") or {}) | (kinds or {}),
    }
    write_text_atomically(REPO_ROOT / SELF_TEST_FILE, json.dumps(results, indent=2))


def _probe_one(renderer: SceneRenderer, kind: str) -> tuple[bool, str]:
    """Draw the smallest real example of one kind. Returns (ok, why not)."""
    command = renderer.probe_command(kind)
    if not command:
        return False, "this renderer has no probe"
    try:
        ran = run_bounded(command, PROBE_TIMEOUT_SECONDS, cwd=_probe_directory(renderer))
    except OSError as unusable:
        return False, str(unusable)[:200]

    if ran.timed_out:
        return False, f"did not finish in {PROBE_TIMEOUT_SECONDS}s"
    said = ran.out.strip().splitlines()
    if ran.code == 0 and said and said[-1].strip() == "ok":
        return True, ""
    return False, (_why_it_failed(ran.err)
                   or (said[-1][:200] if said else f"exit {ran.code}"))


def _probe_directory(renderer: SceneRenderer) -> Path | None:
    from pipeline.config import REPO_ROOT

    if renderer.key == "revideo":
        return REPO_ROOT / "renderers" / "revideo"
    return REPO_ROOT


def verify_scene_renderer(key: str, kind: str = "") -> dict[str, Any]:
    """Actually draw with it, and remember what worked.

    With no kind, every kind it claims -- which is slow and is meant to be: it
    is the difference between a page that says "animation is available" and one
    that says which eleven of fourteen kinds this machine can really draw. With
    a kind, just that one, so a fix can be rechecked in seconds.
    """
    import time

    renderer = BY_KEY.get(key)
    if renderer is None:
        return {"key": key, "ok": False, "detail": "no such renderer"}
    if not renderer.is_installed():
        return {"key": key, "ok": False, "detail": "not installed"}
    if not renderer.can(Capability.ANIMATED_DIAGRAM):
        _remember_self_test(key, True, "draws stills, which needs no proving")
        return {"key": key, "ok": True, "detail": "stills only", "kinds": {}}

    wanted = [kind] if kind else list(renderer.kinds)
    unknown = [one for one in wanted if one not in renderer.kinds]
    if unknown:
        return {"key": key, "ok": False,
                "detail": f"{renderer.label} does not claim to draw {unknown[0]!r}"}

    started = time.time()
    results: dict[str, Any] = {}
    for one in wanted:
        ok, detail = _probe_one(renderer, one)
        results[one] = {"ok": ok, "detail": detail}

    # The renderer works if it can draw anything at all. One kind failing is a
    # gap in the repertoire; every kind failing is a broken backend, and the
    # difference decides whether Generation may use it.
    passed = [one for one, result in results.items() if result["ok"]]
    failed = [one for one, result in results.items() if not result["ok"]]
    if kind and not passed:
        # Verifying one kind must not condemn the whole renderer: everything
        # else may still work, and the recorded per-kind result is the answer.
        was = _self_test_results().get(key) or {}
        overall_ok = bool(was.get("ok", True))
        detail = was.get("detail", "")
    else:
        overall_ok = bool(passed)
        detail = ("" if not failed else
                  f"{len(failed)} of {len(wanted)} kinds could not be drawn: "
                  f"{', '.join(failed[:4])}")

    _remember_self_test(key, overall_ok, detail, results)
    return {
        "key": key,
        "ok": overall_ok,
        "detail": detail,
        "kinds": results,
        "drawable": sorted(passed),
        "seconds": round(time.time() - started, 1),
    }
