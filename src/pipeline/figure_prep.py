"""Figure hygiene — making an extracted picture fit to show, or saying it is not.

A picture pulled out of a deck is not a figure. It is whatever rectangle the
file happened to store: a diagram with two inches of slide background around it,
a screenshot cropped through its own caption, a gradient strip that was a
divider rule, a 1200x40 sliver of a table. Put on a frame at full size, the
first wastes most of the screen, the second shows half a sentence, and the last
two show nothing at all.

Nothing looked. The library measured width and height and called anything under
64 pixels decoration; everything else went on the frame as it came out of the
file.

This module opens each one and decides three things:

- **Trim.** The uniform border around the picture is measured and removed, and
  the trimmed copy is kept beside the original under a name derived from its
  content. The original is never touched: the trim is a guess about framing, and
  a guess that overwrites the source is not reversible.
- **Reject.** Blank, near-blank, a sliver, or too small to read once trimmed --
  these are not proposed for use. Somebody can still choose one; the flag says
  what is wrong with it, not what they are allowed to do.
- **Flag.** Ink running off an edge usually means the crop went through
  something -- a caption, an axis, the bottom row of a table. It is a guess, so
  it is only ever a flag: a diagram drawn with a full-bleed border looks exactly
  the same to this and is perfectly fine to show.
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

# How far a pixel may be from the border colour and still count as border. Decks
# compress their images, so a "uniform" white margin is never exactly one value.
UNIFORM_TOLERANCE = 14

# Below this, once trimmed, there is nothing left to read on a 1920-wide frame.
SMALLEST_PREPARED_PIXELS = 120

# Thinner than this and it is a rule, a banner or a sliver of a table.
WIDEST_USABLE_RATIO = 8.0

# The whole picture within this much of one tone: a fill, a gradient, a blank.
FLATTEST_USABLE_RANGE = 12

# The outer band where ink means the crop probably went through something, and
# how much ink in it counts as running off the edge.
EDGE_BAND_FRACTION = 0.02
EDGE_INK_FRACTION = 0.10

# Trimming less than this is not worth a second file on disk.
SMALLEST_WORTHWHILE_TRIM = 0.03

PREPARED_DIRECTORY = "assets/prepared"


class FigureFlag:
    """What is wrong with a picture, in the words the UI shows."""

    TRIMMED = "trimmed"
    BLANK = "blank"
    SLIVER = "sliver"
    TINY = "tiny"
    CUT_OFF = "cut_off"
    UNREADABLE = "unreadable"


# The flags that mean "do not put this on a frame unless somebody says to". A
# cut-off picture is not here: it is a guess, and a wrong guess that silently
# drops the author's own diagram is worse than a caption with its feet cut off.
DISQUALIFYING = frozenset({
    FigureFlag.BLANK, FigureFlag.SLIVER, FigureFlag.TINY, FigureFlag.UNREADABLE})

WHY = {
    FigureFlag.TRIMMED: "Trimmed: it had a uniform border around it.",
    FigureFlag.BLANK: "Nothing in it: one flat tone from edge to edge.",
    FigureFlag.SLIVER: "A sliver, not a figure -- far wider than it is tall, or the reverse.",
    FigureFlag.TINY: "Too small to read once its border was trimmed.",
    FigureFlag.CUT_OFF: "Ink runs off an edge, so the crop may have cut through a caption.",
    FigureFlag.UNREADABLE: "The file could not be opened.",
}


@dataclass(frozen=True)
class PreparedFigure:
    """What was found in one picture, and the copy that is fit to show."""

    # The size of the file as it was stored, and the size of what is actually
    # shown once the margin is off. Both, because they answer different
    # questions: the first is what the deck contained, the second is what a
    # frame has to fit.
    width: int = 0
    height: int = 0
    prepared_width: int = 0
    prepared_height: int = 0

    prepared_path: str = ""          # relative to the project root; empty if untrimmed
    trimmed_fraction: float = 0.0
    flags: list[str] = field(default_factory=list)

    @property
    def is_usable(self) -> bool:
        return not DISQUALIFYING.intersection(self.flags)

    @property
    def why(self) -> str:
        return " ".join(WHY[flag] for flag in self.flags if flag in WHY)


def prepare_figure(project_root: Path, asset_path: str) -> PreparedFigure:
    """Open one stored picture, trim it, and say what is wrong with it.

    Never raises. A picture that cannot be opened is a finding, not an error:
    that is exactly what this is looking for.
    """
    from PIL import Image

    source = project_root / asset_path
    try:
        with Image.open(source) as opened:
            opened.load()
            picture = opened.convert("RGBA")
    except Exception as unreadable:      # Pillow raises a wide variety here
        logger.warning("figure unreadable (%s): %s", asset_path, unreadable)
        return PreparedFigure(flags=[FigureFlag.UNREADABLE])

    width, height = picture.size
    mask = _ink_mask(picture)
    box = mask.getbbox()
    flags: list[str] = []

    if box is None:
        return PreparedFigure(width=width, height=height, flags=[FigureFlag.BLANK])

    trimmed = picture.crop(box)
    kept = (trimmed.width * trimmed.height) / max(1, width * height)
    trimmed_fraction = round(1 - kept, 3)

    prepared_path = ""
    if trimmed_fraction >= SMALLEST_WORTHWHILE_TRIM:
        prepared_path = _write_prepared(project_root, source, trimmed)
        if prepared_path:
            flags.append(FigureFlag.TRIMMED)

    shown = trimmed
    if min(shown.width, shown.height) < SMALLEST_PREPARED_PIXELS:
        flags.append(FigureFlag.TINY)
    longest = max(shown.width, shown.height) / max(1, min(shown.width, shown.height))
    if longest > WIDEST_USABLE_RATIO:
        flags.append(FigureFlag.SLIVER)
    if _tonal_range(shown) <= FLATTEST_USABLE_RANGE:
        flags.append(FigureFlag.BLANK)
    elif _runs_off_an_edge(picture, mask):
        # Asked of the picture as it was stored, not of the trimmed copy: after
        # trimming, every figure's ink is at the edge by construction, so a
        # diagram drawn inside a box would flag every time and the flag would
        # mean nothing. Ink at the *original* edge is the signal -- there was no
        # margin there, because something was cut through.
        flags.append(FigureFlag.CUT_OFF)

    return PreparedFigure(
        width=width, height=height,
        prepared_width=shown.width, prepared_height=shown.height,
        prepared_path=prepared_path, trimmed_fraction=trimmed_fraction,
        flags=flags,
    )


def showable_path(project_root: Path, asset_path: str, prepared_path: str) -> Path:
    """The file a frame should actually draw: the prepared copy if there is one."""
    if prepared_path:
        prepared = project_root / prepared_path
        if prepared.exists():
            return prepared
    return project_root / asset_path


# --- looking at the pixels ----------------------------------------------------------


def _ink_mask(picture):
    """Everything that is not the border, as a black-and-white mask.

    The border colour is taken from the corners rather than assumed to be white:
    a dark-themed deck's figures come out on a dark background, and trimming
    those against white removes nothing at all.
    """
    from PIL import Image, ImageChops

    alpha = picture.getchannel("A")
    if alpha.getextrema()[0] < 250:
        # Transparent margins say where the picture ends better than any colour
        # comparison can.
        return alpha.point(lambda value: 255 if value > 8 else 0)

    flat = picture.convert("RGB")
    border = _commonest_border_colour(flat)
    difference = ImageChops.difference(flat, Image.new("RGB", flat.size, border))
    return difference.convert("L").point(
        lambda value: 255 if value > UNIFORM_TOLERANCE else 0)


def _commonest_border_colour(flat) -> tuple[int, int, int]:
    """The colour of the outermost ring of pixels, by majority.

    The whole ring rather than the four corners: a screenshot cropped through a
    dark caption has two white corners and two black ones, and on that tie the
    trim was as likely to decide the picture was black-bordered and cut the
    content away instead of the margin.
    """
    from collections import Counter

    width, height = flat.size
    ring = [
        *flat.crop((0, 0, width, 1)).getdata(),
        *flat.crop((0, height - 1, width, height)).getdata(),
        *flat.crop((0, 0, 1, height)).getdata(),
        *flat.crop((width - 1, 0, width, height)).getdata(),
    ]
    return Counter(ring).most_common(1)[0][0] if ring else (255, 255, 255)


def _tonal_range(picture) -> int:
    from PIL import ImageStat

    darkest, lightest = ImageStat.Stat(picture.convert("L")).extrema[0]
    return lightest - darkest


def _runs_off_an_edge(picture, mask) -> bool:
    """Whether ink reaches an edge densely enough to look like a cut.

    Density, not presence: one antialiased pixel touching the border happens in
    most diagrams. A tenth of an edge band covered is a line, a caption or a
    table row going over the side.
    """
    width, height = mask.size
    band = max(1, int(min(width, height) * EDGE_BAND_FRACTION))

    edges = [
        mask.crop((0, 0, width, band)),
        mask.crop((0, height - band, width, height)),
        mask.crop((0, 0, band, height)),
        mask.crop((width - band, 0, width, height)),
    ]
    for edge in edges:
        pixels = edge.width * edge.height
        if not pixels:
            continue
        inked = sum(edge.point(lambda value: 1 if value else 0)
                    .getdata())  # noqa: PD011 - a PIL image, not a dataframe
        if inked / pixels >= EDGE_INK_FRACTION:
            return True
    return False


def _write_prepared(project_root: Path, source: Path, trimmed) -> str:
    """Save the trimmed copy under a name derived from what is in it.

    Content-addressed so re-running extraction does not pile up copies of the
    same picture, and so a picture that changed gets a new file rather than a
    stale one under the old name.
    """
    from PIL import Image

    flattened = trimmed
    if flattened.mode == "RGBA":
        backing = Image.new("RGBA", flattened.size, (255, 255, 255, 0))
        flattened = Image.alpha_composite(backing, flattened)

    digest = hashlib.sha256(
        f"{source.name}|{flattened.size}|{flattened.tobytes()[:4096].hex()}".encode()
    ).hexdigest()[:16]
    directory = project_root / PREPARED_DIRECTORY
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{source.stem}-{digest}.png"

    if not path.exists():
        try:
            flattened.save(path)
        except OSError as unwritable:
            logger.warning("could not write the trimmed copy of %s: %s", source.name, unwritable)
            return ""
    return f"{PREPARED_DIRECTORY}/{path.name}"
