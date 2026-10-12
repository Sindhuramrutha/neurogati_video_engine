"""scenekit -- the small toolkit every scene script can import.

Reading the brief, drawing frames with Pillow, writing them to a video, easing,
and fetching an outside resource while recording where it came from. A scene
script does not have to use any of it: it may use Manim, matplotlib or anything
else it declares. This is what is always here.

Needs: pillow (and ffmpeg on PATH). List "pillow" in the script's dependencies.

    from scenekit import load_brief, VideoWriter, canvas, font, wrap, ease

    brief = load_brief()
    with VideoWriter(brief) as video:
        for n in range(brief.frames):
            t = n / max(1, brief.frames - 1)          # 0..1 through the scene
            image, draw = canvas(brief)
            draw.text((160, 200), brief.headline, font=font(brief, 84, bold=True),
                      fill=brief.look["text"])
            video.write(image)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import urllib.request
from pathlib import Path


class _Facts(dict):
    """A dict whose keys also read as attributes: `brief.assets.pictures` and
    `brief.assets["pictures"]` are the same thing."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as missing:
            raise AttributeError(name) from missing


class Brief:
    """What the scene is told: `brief.json`, with attribute access.

    narration, on_screen, headline, seconds, width, height, fps, frames, look
    (background, panel, accent, text, dim, heading_font, body_font), pictures,
    slide_image, section_title, role, language -- and `out`, where to write.
    """

    def __init__(self, data: dict, out: Path) -> None:
        self.__dict__.update({key: _Facts(value) if isinstance(value, dict) else value
                              for key, value in data.items()})
        self.out = out
        self.frames = max(1, round(self.seconds * self.fps))


def load_brief() -> Brief:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", default="brief.json")
    parser.add_argument("--out", default="render.mp4")
    arguments = parser.parse_args()
    data = json.loads(Path(arguments.brief).read_text(encoding="utf-8"))
    return Brief(data, Path(arguments.out))


# --- drawing -------------------------------------------------------------------------


def canvas(brief: Brief, colour: str | None = None):
    """A blank frame in the project's background colour, and something to draw with."""
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (brief.width, brief.height), colour or brief.look["background"])
    return image, ImageDraw.Draw(image)


_FONT_FILES = {
    False: ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf", "Helvetica.ttc"],
    True: ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf", "Helvetica.ttc"],
}


def font(brief: Brief, size: int, bold: bool = False):
    """The project's font at this size, or the nearest one this machine has."""
    from PIL import ImageFont

    family = brief.look.get("heading_font" if bold else "body_font") or ""
    named = [f"{family.lower().replace(' ', '')}{'bd' if bold else ''}.ttf"] if family else []
    for name in [*named, *_FONT_FILES[bold]]:
        for folder in ("", "C:/Windows/Fonts/", "/usr/share/fonts/truetype/dejavu/",
                       "/System/Library/Fonts/"):
            try:
                return ImageFont.truetype(folder + name, size)
            except OSError:
                continue
    return ImageFont.load_default(size)


def wrap(draw, text: str, the_font, width: int) -> list[str]:
    """`text` broken into lines no wider than `width` pixels."""
    lines, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if draw.textlength(candidate, font=the_font) <= width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    return [*lines, line] if line else lines


def ease(t: float) -> float:
    """0..1 in, 0..1 out, starting and stopping gently."""
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def between(t: float, start: float, end: float) -> float:
    """How far `t` is through the window start..end, eased: 0 before, 1 after."""
    return ease((t - start) / (end - start)) if end > start else float(t >= end)


# --- writing the video ----------------------------------------------------------------


class VideoWriter:
    """Frames in, an .mp4 out: H.264, the brief's size and frame rate, no sound."""

    def __init__(self, brief: Brief) -> None:
        self.brief = brief
        self.process = subprocess.Popen(
            ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-s", f"{brief.width}x{brief.height}", "-r", str(brief.fps), "-i", "-",
             "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(brief.out)],
            stdin=subprocess.PIPE)

    def write(self, image) -> None:
        if image.size != (self.brief.width, self.brief.height) or image.mode != "RGB":
            image = image.convert("RGB").resize((self.brief.width, self.brief.height))
        self.process.stdin.write(image.tobytes())

    def __enter__(self) -> VideoWriter:
        return self

    def __exit__(self, *_error) -> None:
        self.process.stdin.close()
        if self.process.wait() != 0:
            raise RuntimeError("ffmpeg could not write the video")


# --- outside resources ------------------------------------------------------------------


def fetch(url: str, name: str, licence: str, credit: str) -> Path:
    """Download an open resource into `assets/`, and record where it came from.

    `licence` and `credit` are required: a scene may use what others made only
    when it says whose it is and on what terms. They are written to
    `sources.json`, which the checks read and the page shows.
    """
    if not licence.strip() or not credit.strip():
        raise ValueError("fetch() needs the resource's licence and who to credit")
    target = Path("assets") / Path(name).name
    target.parent.mkdir(exist_ok=True)
    if not target.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "scenekit"})
        with urllib.request.urlopen(request, timeout=60) as response:
            target.write_bytes(response.read())
    record = Path("sources.json")
    sources = json.loads(record.read_text(encoding="utf-8")) if record.exists() else []
    if not any(entry["file"] == target.as_posix() for entry in sources):
        sources.append({"file": target.as_posix(), "url": url, "licence": licence,
                        "credit": credit})
        record.write_text(json.dumps(sources, indent=2), encoding="utf-8")
    return target
