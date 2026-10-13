"""A thumbnail for YouTube: a moment of the video with its title, readable at the
size a thumbnail is seen -- a phone's list of results, a few centimetres wide.

The frame is taken a fifth of the way in (past any intro, into the first teaching
scene), shrunk to 1280x720, and the title set large and bold on a dark band
across its lower third, so it reads on any picture.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from pipeline.config import REPO_ROOT

SIZE = (1280, 720)
FONT = REPO_ROOT / "assets" / "fonts" / "Outfit[wght].ttf"
FRAME_SHARE = 0.2
LONGEST_LINE = 30             # characters: two lines, so the band leaves the picture seen


def _lines(title: str) -> list[str]:
    words, lines = title.split(), [""]
    for word in words:
        if lines[-1] and len(lines[-1]) + 1 + len(word) > LONGEST_LINE:
            lines.append(word)
        else:
            lines[-1] = f"{lines[-1]} {word}".strip()
    return lines[:3]


def make_thumbnail(video: Path, title: str, target: Path, seconds: float) -> Path | None:
    """Write the thumbnail; None when there is no ffmpeg or no frame to take."""
    from PIL import Image, ImageDraw, ImageFont

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg or not video.exists():
        return None
    frame = target.with_suffix(".frame.png")
    subprocess.run([ffmpeg, "-y", "-v", "error", "-ss", f"{max(0.0, seconds * FRAME_SHARE):.2f}",
                    "-i", str(video), "-frames:v", "1", str(frame)],
                   capture_output=True, stdin=subprocess.DEVNULL, timeout=60, check=False)
    if not frame.exists():
        return None
    with Image.open(frame) as opened:
        image = opened.convert("RGB").resize(SIZE)
    frame.unlink(missing_ok=True)

    lines = _lines(title)
    band_top = SIZE[1] - 56 - 80 * len(lines)
    shade = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    ImageDraw.Draw(shade).rectangle([0, band_top, SIZE[0], SIZE[1]], fill=(10, 12, 20, 200))
    image = Image.alpha_composite(image.convert("RGBA"), shade).convert("RGB")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(str(FONT), 72)
        font.set_variation_by_axes([800])
    except (OSError, ValueError, AttributeError):
        font = ImageFont.load_default(size=72)
    for index, line in enumerate(lines):
        draw.text((56, band_top + 24 + index * 80), line, font=font, fill=(255, 255, 255))
    image.save(target)
    return target
