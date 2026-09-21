"""Rendering — plan plus script becomes an actual video file.

The stage that did not exist. Everything before this produced text; this produces
`reviewing/output/<slug>.mp4` and a matching `.srt`.

**Audio is the clock** ([ADR 0001](../../docs/decisions/0001-preserve-audio-first-timing.md)).
Each section's narration is synthesised first, its real duration is *measured*
from the file, and only then is the picture cut to fit. The alternative --
deciding the picture timing from the plan's estimated seconds and hoping the
voice matches -- is exactly how v1's animations drifted out of sync with the
narration, and no amount of prompting fixes a clock that guesses.

**The video is made of the source material, not of defaults.** A section shows
the pictures its own plan section draws on -- the diagrams from the deck or the
chapter, chosen on Assets & Design -- beside the words being spoken. When the
project follows the source's styling, the deck's background, its theme colours
and its fonts are what the frames are drawn with. Everything here comes from a
file somebody supplied: nothing is generated to fill a frame, and a section with
no picture gets text on the project's own background rather than a stock image.

**The narration is never on screen.** It is being spoken; printing it as well is
what made the output read as slides with a voice over them, and a viewer who is
reading has stopped listening. Each scene shows the headline and the two to four
labels Generation composed from its brief, and the labels appear one at a time,
on the word that names them.

**The picture changes per scene, not per sentence.** A scene whose narration
fills three slides is one continuous shot, so the camera move runs across the
whole of it, an animated diagram plays once instead of restarting, and one shot
dissolves into the next.

Animated scenes come from a scene renderer ([ADR 0007]
(../../docs/decisions/0007-revideo-as-rendering-target.md)) when one is
installed and its self-test passes; when none is, the same diagram is drawn as a
still from the same nodes and held.

ffmpeg does the muxing. It is an external process, so its failures are captured
and reported with the command that produced them rather than surfacing as a
generic non-zero exit.
"""

from __future__ import annotations

import logging
import re
import shutil
import subprocess
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

from pipeline.speech import WordTiming

logger = logging.getLogger(__name__)

FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080
FRAME_RATE = 30

# The stage colours the UI already uses, for a project that does not take its
# look from its source material.
BACKGROUND_COLOUR = (13, 15, 20)
SURFACE_COLOUR = (20, 23, 31)
TEXT_COLOUR = (232, 234, 240)
DIM_TEXT_COLOUR = (154, 163, 181)
ACCENT_COLOUR = (232, 121, 168)

# Where a picture sits on a slide, as fractions of the frame: the right half,
# inset. Fractions rather than pixels so the layout survives a frame size change.
PICTURE_BOX = (0.50, 0.17, 0.96, 0.86)
TEXT_BOX_WITH_PICTURE = (0.09, 0.20, 0.46, 0.86)


def _luminance(colour: tuple[int, int, int]) -> float:
    red, green, blue = colour
    return (0.2126 * red + 0.7152 * green + 0.0722 * blue) / 255


def _hex_to_rgb(value: str, fallback: tuple[int, int, int]) -> tuple[int, int, int]:
    text = (value or "").strip().lstrip("#")
    if len(text) != 6:
        return fallback
    try:
        return tuple(int(text[at:at + 2], 16) for at in (0, 2, 4))  # type: ignore[return-value]
    except ValueError:
        return fallback


@dataclass
class RenderStyle:
    """What the frames are drawn with.

    Built from the project's own material when it follows the source's styling,
    and from the app's colours when it does not. Text colour is not stored: it is
    decided from the background's luminance, because a deck with a white master
    and a deck with a black one both have to stay readable and neither knows
    about the other.
    """

    background_colour: tuple[int, int, int] = BACKGROUND_COLOUR
    surface_colour: tuple[int, int, int] = SURFACE_COLOUR
    accent_colour: tuple[int, int, int] = ACCENT_COLOUR
    background_image: Path | None = None
    heading_font: str = ""
    body_font: str = ""

    @property
    def is_light(self) -> bool:
        return _luminance(self.background_colour) > 0.55

    @property
    def text_colour(self) -> tuple[int, int, int]:
        return (26, 24, 22) if self.is_light else TEXT_COLOUR

    @property
    def dim_text_colour(self) -> tuple[int, int, int]:
        return (92, 86, 80) if self.is_light else DIM_TEXT_COLOUR

    @property
    def panel_colour(self) -> tuple[int, int, int]:
        """What a picture or a block of text sits on, so both stay legible over
        a background picture."""
        return (255, 255, 255) if self.is_light else self.surface_colour

    @classmethod
    def from_look(cls, look: dict, project_root: Path) -> RenderStyle:
        """The deck's own look. Anything missing keeps the app's default."""
        colours = look.get("colours") or {}
        background = _hex_to_rgb(
            look.get("background_colour") or colours.get("lt1", ""), BACKGROUND_COLOUR)
        accent = _hex_to_rgb(colours.get("accent1", ""), ACCENT_COLOUR)
        stored = look.get("background_asset_path") or ""
        picture = project_root / stored if stored else None
        return cls(
            background_colour=background,
            surface_colour=_hex_to_rgb(colours.get("lt2", ""), background),
            accent_colour=accent,
            background_image=picture if picture and picture.exists() else None,
            heading_font=look.get("heading_font", ""),
            body_font=look.get("body_font", ""),
        )


DEFAULT_STYLE = RenderStyle()

# The video opens on a title card. Sections do not. A card before every section
# was two and a half seconds of silence each time -- about seven per cent of a
# five-minute video spent waiting, for a name that is on the section's own
# frames anyway.
TITLE_CARD_MS = 1800

# A beat after the last word, so a cut does not clip the final syllable and the
# section does not end on the exact frame the voice stops.
SECTION_TAIL_MS = 250

# How long one shot dissolves into the next, and the shortest dissolve worth
# having: below this it is a flicker, so short shots are cut instead.
CROSS_FADE_MS = 400
SHORTEST_CROSS_FADE_MS = 90

# Roughly how many characters of narration fit in one subtitle cue.
CHARACTERS_PER_SLIDE = 260


class RenderFailed(Exception):
    """Rendering did not produce a video. Names the step that failed."""


@dataclass
class Shot:
    """One scene's picture and how the camera moves over it.

    A scene, not a slide: one scene's narration may fill three slides, and all
    three are the same shot -- the camera keeps moving across them instead of
    restarting, which is the difference between a film and a carousel.
    """

    picture: Path | None = None
    motion: str = "hold"

    # A clip that animates this scene, when a renderer that can animate drew
    # one. It replaces the still and its camera move: the diagram is already
    # moving, and panning across an animation is two motions competing.
    clip: Path | None = None

    # What the viewer reads while this scene is spoken. Never the narration.
    headline: str = ""
    points: list[str] = field(default_factory=list)

    # A finished frame -- the source's own slide, composed as its author
    # designed it. Drawn edge to edge with nothing over it: it already has its
    # heading, its body text and its artwork exactly where they belong, and
    # anything this renderer adds is drawn on top of somebody's layout.
    full_bleed: bool = False


@dataclass
class RenderedSection:
    section_id: str
    title: str
    narration: str
    audio_path: Path | None = None
    audio_duration_ms: int = 0
    start_ms: int = 0

    # The source's own pictures for this section, in the order they were
    # extracted. Used when Generation has decided nothing: the slides take one
    # each and start again when they run out.
    pictures: list[Path] = field(default_factory=list)

    # What Generation decided, one shot per scene: the picture and how the
    # camera moves over it. This is what makes a video rather than a slideshow,
    # so it wins over `pictures` whenever it exists.
    shots: list[Shot] = field(default_factory=list)

    # Where every word of this section's narration falls, when the voice
    # reported it. The slides then break on a word rather than on a share of
    # the characters, and a label appears as it is said.
    words: tuple[WordTiming, ...] = ()

    # Only the first section opens the video, and only it gets a title card.
    is_opening: bool = False

    @property
    def title_card_ms(self) -> int:
        """How long this section holds a card before its narration starts.

        Only where a card earns the silence: the opening of the video, and a
        section with nothing to say -- whose gap should be visible rather than
        skipped.
        """
        if self.is_opening or not self.audio_duration_ms or not self.narration.strip():
            return TITLE_CARD_MS
        return 0

    @property
    def total_ms(self) -> int:
        if not self.audio_duration_ms:
            return self.title_card_ms
        return self.title_card_ms + self.audio_duration_ms + SECTION_TAIL_MS


@dataclass
class RenderResult:
    video_path: Path
    subtitle_path: Path
    duration_ms: int
    provider_key: str
    voice: str
    sections: list[RenderedSection] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "video_path": str(self.video_path),
            "video_file_name": self.video_path.name,
            "subtitle_path": str(self.subtitle_path),
            "duration_ms": self.duration_ms,
            "voice_provider": self.provider_key,
            "voice": self.voice,
            "section_count": len(self.sections),
            "sections": [
                {
                    "section_id": s.section_id,
                    "title": s.title,
                    "start_ms": s.start_ms,
                    "duration_ms": s.total_ms,
                }
                for s in self.sections
            ],
            "warnings": self.warnings,
        }


def require_ffmpeg() -> str:
    path = shutil.which("ffmpeg")
    if not path:
        raise RenderFailed(
            "ffmpeg is not on PATH. Install it (winget install Gyan.FFmpeg) and "
            "reopen the terminal so the new PATH is picked up."
        )
    return path


def _font_file_candidates(family: str, bold: bool) -> list[str]:
    """File names a font family is likely to be installed under.

    A theme names its fonts the way a person does -- "Calibri Light" -- and the
    files are named the way a foundry does: `calibril.ttf`. Guessing a few
    spellings finds the real font on a machine that has it and costs nothing on
    one that does not.
    """
    compact = family.lower().replace(" ", "").replace("-", "")
    first = family.lower().split()[0] if family.split() else ""
    suffixes = ("bd", "b") if bold else ("",)
    names = []
    for stem in (compact, first):
        if not stem:
            continue
        names.extend(f"{stem}{suffix}.ttf" for suffix in suffixes)
        names.append(f"{stem}.ttf")
    return names


def _load_font(size: int, bold: bool = False, family: str = ""):
    """A real font if one can be found, the bitmap default if not.

    Falling back rather than failing: a video with plainer text is worth more
    than no video, and a theme naming a font nobody has installed is ordinary.
    """
    from PIL import ImageFont

    named = []
    if family:
        for name in _font_file_candidates(family, bold):
            named.append(f"C:/Windows/Fonts/{name}")
            named.append(f"/usr/share/fonts/truetype/{name}")
            named.append(name)      # Pillow also searches the system font path.

    fallbacks = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in [*named, *fallbacks]:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue

    logger.warning("no TrueType font found; falling back to the bitmap default")
    return ImageFont.load_default()


def _paste_background(image, style: RenderStyle) -> None:
    """The deck's background picture, filled to the frame and calmed down.

    Covered rather than stretched, because a background squashed to a different
    aspect is the most obvious way a video says it was made by a machine. The
    veil over it is what keeps the words readable: a photographic background and
    body text cannot share the same contrast range.
    """
    from PIL import Image

    if style.background_image is None or not style.background_image.exists():
        return
    try:
        with Image.open(style.background_image) as picture:
            filled = picture.convert("RGB")
    except Exception as unreadable:      # a broken file must not stop a render
        logger.warning("background picture skipped: %s", unreadable)
        return

    scale = max(FRAME_WIDTH / filled.width, FRAME_HEIGHT / filled.height)
    resized = filled.resize(
        (max(1, round(filled.width * scale)), max(1, round(filled.height * scale))),
        Image.LANCZOS,
    )
    left = (resized.width - FRAME_WIDTH) // 2
    top = (resized.height - FRAME_HEIGHT) // 2
    image.paste(resized.crop((left, top, left + FRAME_WIDTH, top + FRAME_HEIGHT)), (0, 0))

    veil = Image.new("RGBA", (FRAME_WIDTH, FRAME_HEIGHT),
                     (*style.background_colour, 170))
    image.paste(Image.alpha_composite(image.convert("RGBA"), veil).convert("RGB"), (0, 0))


def _paste_picture(image, draw, picture_path: Path, style: RenderStyle) -> bool:
    """One of the source's own pictures, fitted into the right of the frame.

    Contained, never cropped and never enlarged past its own size: these are
    diagrams with labels on them, and a diagram that has been zoomed to fill a
    box is a diagram nobody can read. Returns whether anything was drawn, so the
    text can take the whole frame when it was not.
    """
    from PIL import Image

    try:
        with Image.open(picture_path) as opened:
            picture = opened.convert("RGBA")
    except Exception as unreadable:
        logger.warning("picture skipped (%s): %s", picture_path.name, unreadable)
        return False

    left, top, right, bottom = (
        int(PICTURE_BOX[0] * FRAME_WIDTH), int(PICTURE_BOX[1] * FRAME_HEIGHT),
        int(PICTURE_BOX[2] * FRAME_WIDTH), int(PICTURE_BOX[3] * FRAME_HEIGHT),
    )
    box_width, box_height = right - left, bottom - top
    scale = min(box_width / picture.width, box_height / picture.height)
    width = max(1, round(picture.width * scale))
    height = max(1, round(picture.height * scale))
    fitted = picture.resize((width, height), Image.LANCZOS)

    # A card behind it: most extracted diagrams have transparent or white
    # backgrounds, and either one disappears on a dark frame.
    pad = 18
    card = [
        (left + (box_width - width) // 2 - pad, top + (box_height - height) // 2 - pad),
        (left + (box_width - width) // 2 + width + pad,
         top + (box_height - height) // 2 + height + pad),
    ]
    draw.rounded_rectangle(card, radius=18, fill=(255, 255, 255))
    image.paste(fitted, (card[0][0] + pad, card[0][1] + pad), fitted)
    return True


def _readable_picture(picture: Path | None) -> bool:
    """Whether there is a picture that can actually be opened.

    Asked before drawing rather than discovered during it, because a label
    overlaid later has to land in the same place as the headline underneath it,
    and the layout depends on whether the frame has a picture in it.
    """
    from PIL import Image

    if picture is None or not picture.exists():
        return False
    try:
        with Image.open(picture) as opened:
            opened.verify()
        return True
    except Exception as unreadable:      # a broken file must not stop a render
        logger.warning("picture skipped (%s): %s", picture.name, unreadable)
        return False


@dataclass(frozen=True)
class WordsLayout:
    """Where the headline and each label sit on the frame.

    One layout, used both to draw a frame and to draw the transparent layer a
    label arrives on, so a label that appears eight seconds in lands on exactly
    the pixel it would have occupied had it been there from the start.
    """

    heading_font: object
    headline_rows: tuple[tuple[str, int, int], ...]
    point_font: object
    # Each label as the rows it wrapped to, and where the first row sits.
    point_rows: tuple[tuple[tuple[str, ...], int, int], ...]
    point_size: int


def _words_layout(
    headline: str, points: list[str], style: RenderStyle,
    showing_picture: bool, is_title: bool,
) -> WordsLayout:
    headline_size = 82 if is_title else (56 if showing_picture else 68)
    point_size = 34 if showing_picture else 40
    wrap_at = 20 if showing_picture else 30

    if showing_picture:
        left = int(TEXT_BOX_WITH_PICTURE[0] * FRAME_WIDTH)
        top = int(TEXT_BOX_WITH_PICTURE[1] * FRAME_HEIGHT)
        bottom = int(TEXT_BOX_WITH_PICTURE[3] * FRAME_HEIGHT)
    else:
        left, top, bottom = 200, 300, FRAME_HEIGHT - 240

    lines = textwrap.wrap(headline, width=wrap_at)[:3] or [headline]
    line_height = int(headline_size * 1.22)

    # A label wraps rather than running off the side of the frame. "1000 times
    # smaller than the chest ECG" is a real label from real source material, and
    # it was being cut off mid-word at the edge.
    point_wrap = 26 if showing_picture else 44
    wrapped = [textwrap.wrap(point, width=point_wrap)[:2] or [point] for point in points]

    gap = 56 if points else 0
    point_gap = int(point_size * 0.9)
    block = (line_height * len(lines) + gap
             + sum(len(rows) * int(point_size * 1.35) + point_gap for rows in wrapped))
    y = max(top, (top + bottom - block) // 2)

    headline_rows = tuple(
        (line, left, y + index * line_height) for index, line in enumerate(lines))

    point_rows = []
    at = y + line_height * len(lines) + gap
    for rows in wrapped:
        point_rows.append((tuple(rows), left, at))
        at += len(rows) * int(point_size * 1.35) + point_gap

    return WordsLayout(
        heading_font=_load_font(headline_size, bold=True, family=style.heading_font),
        headline_rows=headline_rows,
        point_font=_load_font(point_size, family=style.body_font),
        point_rows=tuple(point_rows),
        point_size=point_size,
    )


def _draw_point(draw, layout: WordsLayout, index: int, style: RenderStyle) -> None:
    """One label, wrapped, with an accent rule where a bullet would be."""
    rows, left, top = layout.point_rows[index]
    middle = top + layout.point_size // 2
    draw.rounded_rectangle(
        [(left, middle - 4), (left + 26, middle + 4)], radius=4, fill=style.accent_colour)
    for at, row in enumerate(rows):
        draw.text((left + 52, top + at * int(layout.point_size * 1.35)), row,
                  font=layout.point_font, fill=style.text_colour)


def _fill_frame(picture: Path, style: RenderStyle = DEFAULT_STYLE):
    """A finished frame, drawn edge to edge.

    Contained rather than cropped: a slide composed at the video's own shape
    lands exactly, and one from a 4:3 deck is letterboxed on the project's own
    background rather than having its edges cut off. Losing a centimetre of
    somebody's layout to fill a frame is not a trade worth making.
    """
    from PIL import Image

    frame = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), style.background_colour)
    with Image.open(picture) as opened:
        slide = opened.convert("RGB")
    scale = min(FRAME_WIDTH / slide.width, FRAME_HEIGHT / slide.height)
    fitted = slide.resize(
        (max(1, round(slide.width * scale)), max(1, round(slide.height * scale))),
        Image.LANCZOS,
    )
    frame.paste(fitted, ((FRAME_WIDTH - fitted.width) // 2,
                         (FRAME_HEIGHT - fitted.height) // 2))
    return frame


def _draw_frame(
    headline: str,
    points: list[str],
    footer: str,
    accent_text: str,
    style: RenderStyle = DEFAULT_STYLE,
    picture: Path | None = None,
    is_title: bool = False,
    revealed: int = 0,
):
    """One 1920x1080 frame: the background, the scene's picture, and the few
    words the viewer reads.

    **Not the narration.** It is being spoken; printing it as well is what made
    this read as slides with a voice over them. A headline of a few words and up
    to four labels is what somebody can take in while listening to something
    else -- and every one of them came from the scene's brief, so what is on
    screen is what the script asked for rather than a transcript of it.

    `revealed` is how many labels are already on the frame. The rest arrive as
    overlays timed to the voice, so the base frame is drawn with none.
    """
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), style.background_colour)
    _paste_background(image, style)
    draw = ImageDraw.Draw(image)

    showing_picture = False
    if _readable_picture(picture):
        showing_picture = _paste_picture(image, draw, picture, style)

    if not showing_picture:
        # No picture: the words sit on a panel, as they always did.
        draw.rounded_rectangle(
            [(110, 110), (FRAME_WIDTH - 110, FRAME_HEIGHT - 110)],
            radius=28, fill=style.panel_colour,
        )
        draw.rectangle([(110, 110), (FRAME_WIDTH - 110, 118)], fill=style.accent_colour)

    layout = _words_layout(headline, points, style, showing_picture, is_title)
    text_left = layout.headline_rows[0][1]

    if accent_text:
        draw.text((text_left, int(0.09 * FRAME_HEIGHT)), accent_text.upper(),
                  font=_load_font(30, bold=True, family=style.heading_font),
                  fill=style.accent_colour)

    for line, left, top in layout.headline_rows:
        draw.text((left, top), line, font=layout.heading_font, fill=style.text_colour)

    for index in range(min(revealed, len(layout.point_rows))):
        _draw_point(draw, layout, index, style)

    if footer:
        draw.text((text_left, FRAME_HEIGHT - 190), footer,
                  font=_load_font(26, family=style.body_font), fill=style.dim_text_colour)

    return image


def _draw_point_layer(
    headline: str, points: list[str], index: int, style: RenderStyle,
    showing_picture: bool, path: Path,
) -> None:
    """One label alone, on transparent, ready to be overlaid when it is said.

    A layer per label rather than a frame per state: the shot is encoded once,
    so the camera keeps moving while the labels arrive, and a four-label scene
    costs four small PNGs instead of four more encodes.
    """
    from PIL import Image, ImageDraw

    layer = Image.new("RGBA", (FRAME_WIDTH, FRAME_HEIGHT), (0, 0, 0, 0))
    layout = _words_layout(headline, points, style, showing_picture, is_title=False)
    _draw_point(ImageDraw.Draw(layer), layout, index, style)
    path.parent.mkdir(parents=True, exist_ok=True)
    layer.save(path)


# The whitespace after a sentence's closing punctuation, or after a closing
# quote or bracket that follows it. Only the whitespace is consumed: the
# punctuation and the quote stay with their sentence.
SENTENCE_BOUNDARY = re.compile(
    r"(?:(?<=[.!?\u2026])|(?<=[.!?\u2026][\"'\u201d\u2019)]))\s+"
)


def _slides_for_narration(narration: str) -> list[str]:
    """Kept for callers that only want the words; see `_slides_with_scenes`."""
    return [text for text, _scene in _slides_with_scenes(narration)]


def _slides_with_scenes(narration: str) -> list[tuple[str, int]]:
    """Split narration into slide-sized chunks, breaking on sentences.

    Sentence boundaries rather than a fixed character count: a slide that cuts
    mid-clause is harder to read than one that is slightly too long.
    """
    # Split *after* the punctuation, keeping it. Splitting on ". " consumed the
    # full stop, and rejoining with a space ran every sentence on a slide into
    # the next: "only a few microvolts Filters remove unwanted noise An
    # analog-to-digital converter..." -- on screen, in the subtitles and in the
    # Studio timeline. Only the last sentence of a slide got a period back, and
    # a question at the end of a slide became "Why?.".
    #
    # Blank lines split first: a script's scenes are joined by one, so a slide
    # never runs across the end of one scene into the next.
    slides: list[tuple[str, int]] = []
    for scene_index, paragraph in enumerate(re.split(r"\n\s*\n", narration)):
        flattened = " ".join(paragraph.split())
        if not flattened:
            continue
        current = ""
        for sentence in (s for s in SENTENCE_BOUNDARY.split(flattened) if s):
            candidate = f"{current} {sentence}".strip()
            if len(candidate) > CHARACTERS_PER_SLIDE and current:
                slides.append((_as_finished_sentence(current), scene_index))
                current = sentence
            else:
                current = candidate
        if current:
            slides.append((_as_finished_sentence(current), scene_index))
    return slides or [(narration, 0)]


def _as_finished_sentence(text: str) -> str:
    """A slide ends like a sentence: its own punctuation if it has some."""
    unquoted = text.rstrip("\"'\u201d\u2019)")
    return text if unquoted.endswith((".", "!", "?", "\u2026")) else text + "."


def _format_timestamp(milliseconds: int) -> str:
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


@dataclass(frozen=True)
class Segment:
    """One thing on screen: a title card or a slide of narration text.

    **Every timing in a render comes from `section_segments`.** The picture, the
    subtitles and the Studio timeline all read these, so they cannot disagree.

    They did. The frames split narration time evenly across slides while the
    subtitles split it by text length; the narration was muxed under the title
    card while the subtitles assumed it started after; and `-shortest` failed to
    cut the image stream, so each section ran 2-6 seconds long and the error
    compounded to ~20 seconds by the end. Three formulas for one clock.
    """

    kind: str          # "title" or "slide"
    text: str
    start_ms: int      # from the start of the whole video
    duration_ms: int

    # Which scene's words these are, so the picture on screen is the one that
    # scene asked for. -1 on a title card, which belongs to no scene.
    scene_index: int = -1

    @property
    def end_ms(self) -> int:
        return self.start_ms + self.duration_ms


def section_segments(section: RenderedSection) -> list[Segment]:
    """The title card, if this section has one, then the narration in cues,
    exactly filling `section.total_ms`.

    Where the cues break is decided by the voice when the voice said: a provider
    that reports word boundaries is telling us exactly where every word landed
    in the file it produced, so a cue can change on a word instead of on a share
    of the characters. Without them the split is proportional to the text, which
    is what this had before and is still the fallback.
    """
    segments: list[Segment] = []
    if section.title_card_ms:
        segments.append(
            Segment("title", section.title, section.start_ms, section.title_card_ms))

    if not section.audio_duration_ms or not section.narration.strip():
        return segments

    slides = _slides_with_scenes(section.narration)
    boundaries = _slide_boundaries(slides, section.words, section.audio_duration_ms)
    narration_start_ms = section.start_ms + section.title_card_ms

    previous_boundary_ms = 0
    for (text, scene_index), boundary_ms in zip(slides, boundaries, strict=True):
        segments.append(Segment(
            "slide", text,
            narration_start_ms + previous_boundary_ms,
            boundary_ms - previous_boundary_ms,
            scene_index,
        ))
        previous_boundary_ms = boundary_ms

    return segments


def _slide_boundaries(
    slides: list[tuple[str, int]], words: tuple[WordTiming, ...], audio_duration_ms: int
) -> list[int]:
    """Where each cue ends, in milliseconds from the first spoken word.

    The last one is the whole spoken length plus the tail, always: the clock has
    to close exactly on the section, whichever way the boundaries were found.
    """
    total_ms = audio_duration_ms + SECTION_TAIL_MS
    word_counts = [len(text.split()) for text, _scene in slides]

    # Only trust the timings when there are about as many of them as there are
    # words. A provider that splits differently -- or a narration with numerals
    # and abbreviations in it -- would otherwise slide every cue along by the
    # difference, which is worse than not using them.
    spoken = sum(word_counts)
    if words and abs(len(words) - spoken) <= max(2, spoken // 10):
        boundaries: list[int] = []
        cursor = 0
        for count in word_counts:
            cursor += count
            boundaries.append(total_ms if cursor >= len(words) else words[cursor].start_ms)
        boundaries[-1] = total_ms
        if all(later > earlier
               for earlier, later in zip([0, *boundaries], boundaries, strict=False)):
            return boundaries
        logger.warning("word timings were not in order; splitting by text length instead")

    characters = [len(text) for text, _scene in slides]
    all_characters = sum(characters) or 1
    boundaries = []
    so_far = 0
    for count in characters:
        so_far += count
        boundaries.append(round(total_ms * so_far / all_characters))
    boundaries[-1] = total_ms
    return boundaries


@dataclass(frozen=True)
class ShotWindow:
    """Consecutive segments that share one picture: a title card, or one scene.

    The picture changes when the *scene* changes, not when the text does. A
    scene whose narration fills three cues used to be three stills with the
    camera restarting on each, which is the carousel one level down; as one
    window it is one continuous shot, an animated diagram plays once rather than
    three times, and the labels build across the whole of it.
    """

    kind: str                # "title" or "scene"
    scene_index: int
    start_ms: int
    duration_ms: int
    segments: tuple[Segment, ...]

    @property
    def end_ms(self) -> int:
        return self.start_ms + self.duration_ms


def shot_windows(section: RenderedSection) -> list[ShotWindow]:
    """The section's segments grouped into the shots that will be encoded."""
    windows: list[ShotWindow] = []
    for segment in section_segments(section):
        if segment.kind == "title":
            windows.append(ShotWindow(
                "title", -1, segment.start_ms, segment.duration_ms, (segment,)))
            continue
        previous = windows[-1] if windows else None
        if (previous is not None and previous.kind == "scene"
                and previous.scene_index == segment.scene_index):
            windows[-1] = ShotWindow(
                "scene", previous.scene_index, previous.start_ms,
                previous.duration_ms + segment.duration_ms,
                (*previous.segments, segment),
            )
        else:
            windows.append(ShotWindow(
                "scene", segment.scene_index, segment.start_ms,
                segment.duration_ms, (segment,)))
    return windows


# A word worth matching a label against: long enough that finding it in the
# narration means something. "the" matches everywhere and says nothing.
SHORTEST_MATCHABLE_WORD = 4

# A label appears a little before the word is finished being said, so it is
# already there as the ear arrives at it.
REVEAL_LEAD_MS = 120

# Two labels landing within this of each other read as one flicker.
SHORTEST_GAP_BETWEEN_REVEALS_MS = 200


def _key_word(text: str) -> str:
    """The word in a label worth looking for in the narration."""
    words = [
        "".join(character for character in word if character.isalnum()).lower()
        for word in text.split()
    ]
    long_enough = [word for word in words if len(word) >= SHORTEST_MATCHABLE_WORD]
    return max(long_enough, key=len) if long_enough else ""


def reveal_times(section: RenderedSection, window: ShotWindow, points: list[str]) -> list[int]:
    """When each label appears, in milliseconds from the start of its shot.

    On the word that names it, when the voice reported its timings and that word
    is spoken in this scene: the label lands as it is said, which is the only
    reason to have word timings at all. Otherwise the labels are spread across
    the first part of the shot -- still better than four appearing at once,
    which is a slide.
    """
    if not points:
        return []

    narration_start_ms = section.start_ms + section.title_card_ms
    window_start_ms = window.start_ms - narration_start_ms
    window_end_ms = window_start_ms + window.duration_ms

    found_times: list[int] = []
    cursor = 0
    for index, point in enumerate(points):
        at_ms = None
        key = _key_word(point)
        if key and section.words:
            for position in range(cursor, len(section.words)):
                word = section.words[position]
                if word.start_ms < window_start_ms or word.start_ms >= window_end_ms:
                    continue
                spoken = _key_word(word.text)
                if spoken and (spoken == key or spoken.startswith(key) or key.startswith(spoken)):
                    at_ms = word.start_ms - window_start_ms - REVEAL_LEAD_MS
                    cursor = position + 1
                    break
        if at_ms is None:
            share = (index + 1) / (len(points) + 1)
            at_ms = int(window.duration_ms * share * 0.75)
        found_times.append(max(0, min(at_ms, max(0, window.duration_ms - 500))))

    # Never out of order, whatever the matching found: a label that appears
    # above one already on screen reads as a glitch even when each landed on its
    # own word.
    ordered: list[int] = []
    for at_ms in found_times:
        floor = ordered[-1] + SHORTEST_GAP_BETWEEN_REVEALS_MS if ordered else 0
        ordered.append(max(at_ms, floor))
    return ordered


def write_subtitles(sections: list[RenderedSection], path: Path) -> None:
    """One cue per slide, from the same segments the picture is cut to."""
    entries: list[str] = []
    index = 1

    for section in sections:
        for segment in section_segments(section):
            if segment.kind != "slide":
                continue
            entries.append(
                f"{index}\n"
                f"{_format_timestamp(segment.start_ms)} --> "
                f"{_format_timestamp(segment.end_ms)}\n"
                f"{segment.text}\n"
            )
            index += 1

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(entries), encoding="utf-8")

    # A browser <track> only accepts WebVTT -- SRT silently fails to load,
    # which looks like broken subtitles rather than the wrong format. The two
    # differ by a header and a decimal separator, so both are written: VTT for
    # the player, SRT for every editor that expects it.
    vtt_path = path.with_suffix(".vtt")
    vtt_path.write_text(
        "WEBVTT\n\n" + "\n".join(entries).replace(",", "."), encoding="utf-8"
    )


def _run_ffmpeg(arguments: list[str], step: str) -> None:
    try:
        subprocess.run(arguments, capture_output=True, text=True, check=True, timeout=1800)
    except subprocess.CalledProcessError as failure:
        # The last lines of stderr say what ffmpeg actually objected to; the exit
        # code alone says nothing anyone can act on.
        tail = "\n".join((failure.stderr or "").strip().splitlines()[-6:])
        raise RenderFailed(f"ffmpeg failed while {step}:\n{tail}") from failure
    except subprocess.TimeoutExpired as timeout:
        raise RenderFailed(f"ffmpeg timed out while {step}") from timeout



def _motion_filter(motion: str, duration_ms: int) -> str:
    """The camera move, as an ffmpeg filter over a still.

    `zoompan` rather than a frame sequence: a ten-second shot at thirty frames a
    second is three hundred 1920x1080 PNGs, and a six-minute video would be
    several gigabytes of intermediates to say "the picture drifts slowly left".
    ffmpeg does the same thing from one still and never writes them down.

    The move is slow on purpose -- about four per cent of the frame over the
    whole shot. Anything faster reads as a screensaver and pulls attention off
    the narration, which is the opposite of what a diagram is for.
    """
    frames = max(1, round(duration_ms / 1000 * FRAME_RATE))
    common = f"d={frames}:s={FRAME_WIDTH}x{FRAME_HEIGHT}:fps={FRAME_RATE}"
    # zoompan samples from the scaled input, so the still is enlarged first:
    # zooming a 1920-wide frame directly is what makes a pan look like a
    # slideshow of blurred crops.
    scaled = f"scale={FRAME_WIDTH * 2}:-1"
    centre = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    middle = "y='ih/2-(ih/zoom/2)'"
    drift = 0.04

    moves = {
        "push_in": f"zoompan=z='min(1+{drift}*on/{frames},1.5)':{centre}:{common}",
        "pull_back": f"zoompan=z='max(1+{drift}-{drift}*on/{frames},1.0)':{centre}:{common}",
        "pan_right": f"zoompan=z='1.06':x='(iw-iw/zoom)*on/{frames}':{middle}:{common}",
        "pan_left": f"zoompan=z='1.06':x='(iw-iw/zoom)*(1-on/{frames})':{middle}:{common}",
    }
    return f"{scaled},{moves.get(motion, f'zoompan=z=1:{centre}:{common}')}"


def _shot_for(section: RenderedSection, segment: Segment) -> Shot:
    """What is on screen for this slide.

    Generation decides per scene. Without it, the section's own pictures are
    dealt out slide by slide, which is what the renderer did before there was a
    stage to decide anything.
    """
    if section.shots:
        if segment.kind == "title":
            return section.shots[0]
        if 0 <= segment.scene_index < len(section.shots):
            return section.shots[segment.scene_index]
        return section.shots[-1]

    if not section.pictures:
        return Shot()
    if segment.kind == "title":
        return Shot(picture=section.pictures[0], motion="hold")
    index = max(0, segment.scene_index) % len(section.pictures)
    return Shot(picture=section.pictures[index], motion="hold")


def _cross_fade_ms(durations: list[int]) -> int:
    """How long one shot dissolves into the next, for this section.

    Shortened to fit the shortest shot, and dropped entirely when that would
    make it a flicker: a dissolve that takes as long as the shot it is leaving
    is not a transition, it is a blur.
    """
    if len(durations) < 2:
        return 0
    fade_ms = min(CROSS_FADE_MS, min(durations) // 3)
    return fade_ms if fade_ms >= SHORTEST_CROSS_FADE_MS else 0


def _shot_source(
    shot: Shot, frame_path: Path, length_ms: int
) -> tuple[list[str], str]:
    """How this shot's picture enters ffmpeg, and the filter that sizes it.

    An animated clip plays and then holds its last frame (`tpad`) rather than
    looping: a diagram that finished assembling should stay assembled while the
    narration talks about it, not start over.
    """
    if shot.clip is not None and shot.clip.exists():
        return (
            ["-i", str(shot.clip)],
            f"scale={FRAME_WIDTH}:{FRAME_HEIGHT}:force_original_aspect_ratio=decrease,"
            f"pad={FRAME_WIDTH}:{FRAME_HEIGHT}:-1:-1:color=black,fps={FRAME_RATE},"
            f"tpad=stop_mode=clone:stop_duration={length_ms / 1000:.3f}",
        )
    return (["-loop", "1", "-i", str(frame_path)], _motion_filter(shot.motion, length_ms))


def render_sections(
    sections: list[RenderedSection],
    working_directory: Path,
    output_video_path: Path,
    style: RenderStyle = DEFAULT_STYLE,
) -> None:
    """Draw every shot, cut each section to its exact length, and join them.

    One encode per *scene*, not per sentence: the camera move runs across the
    whole scene, an animated diagram plays once, and the scene's labels arrive
    on top of the moving picture as they are spoken. Encoding a frame per label
    would restart the motion on every one of them.

    Four details carry the timing, and each fixes something that was wrong:

    - **Only the opening section waits for a title card.** A card before every
      section was 2.5 seconds of silence each time, which on a five-minute video
      is most of a section spent reading a name that is on the frames anyway.
    - **Each clip is cut to exactly `total_ms`** with `-t`. `-shortest` did not
      cut the still-image stream, so sections overran and the drift compounded.
    - **Shots are cross-faded, and the fade is paid for.** Every shot is encoded
      a fade longer than its slot, and each dissolve starts a fade early, so the
      section still lands on exactly the length the clock says.
    - **Every clip has an audio stream**, silent if there is no narration.
      Concatenating with `-c copy` needs identical streams in every clip; one
      without audio produces a file whose sound stops partway through.
    """
    ffmpeg = require_ffmpeg()
    working_directory.mkdir(parents=True, exist_ok=True)
    clip_paths: list[Path] = []
    last_section = len(sections) - 1

    for index, section in enumerate(sections):
        windows = shot_windows(section)
        if not windows:
            continue
        durations = [window.duration_ms for window in windows]
        fade_ms = _cross_fade_ms(durations)

        shot_paths = [
            _encode_shot(
                ffmpeg, section, window, style, working_directory,
                name=f"s{index:02d}_{at:02d}",
                kicker=f"Section {index + 1}",
                length_ms=window.duration_ms + fade_ms,
                step=f"section {index + 1}, shot {at + 1} of {len(windows)}",
                opens_the_video=index == 0 and at == 0,
                closes_the_video=index == last_section and at == len(windows) - 1,
            )
            for at, window in enumerate(windows)
        ]
        clip_paths.append(_cut_section(
            ffmpeg, section, shot_paths, durations, fade_ms, index, working_directory))

    _join_and_level(ffmpeg, clip_paths, working_directory, output_video_path)


def _encode_shot(
    ffmpeg: str,
    section: RenderedSection,
    window: ShotWindow,
    style: RenderStyle,
    working_directory: Path,
    *,
    name: str,
    kicker: str,
    length_ms: int,
    step: str,
    opens_the_video: bool = False,
    closes_the_video: bool = False,
) -> Path:
    """One scene: its frame, its camera move, and its labels arriving on top.

    The labels are overlaid rather than drawn into the frame, each switched on
    with `enable` at the moment its word is said, so the whole shot is one
    encode and the motion never restarts.
    """
    shot = _shot_for(section, window.segments[0])
    is_title = window.kind == "title"
    headline = section.title if is_title else (shot.headline or section.title)

    # A clip and a composed slide both carry their own words: the renderer that
    # drew one was given this scene's headline and labels, so overlaying them
    # again prints each of them twice, over the top of what already shows them.
    carries_its_own_words = (
        (shot.clip is not None and shot.clip.exists())
        or (shot.full_bleed and _readable_picture(shot.picture))
    )
    points = [] if is_title or carries_its_own_words else list(shot.points)
    showing_picture = _readable_picture(shot.picture) and not carries_its_own_words

    frame_path = working_directory / f"{name}.png"
    if shot.full_bleed and _readable_picture(shot.picture):
        # Nothing of ours on it. Not a headline, not a kicker, not a footer:
        # this is the author's slide and every mark we add is over their design.
        _fill_frame(shot.picture, style).save(frame_path)
    else:
        _draw_frame(
            headline, points, "" if is_title else section.title, kicker, style,
            picture=None if shot.clip is not None else shot.picture,
            is_title=is_title, revealed=0,
        ).save(frame_path)

    layer_paths: list[Path] = []
    for at, _point in enumerate(points):
        layer_path = working_directory / f"{name}_p{at}.png"
        _draw_point_layer(headline, points, at, style, showing_picture, layer_path)
        layer_paths.append(layer_path)

    inputs, chain = _shot_source(shot, frame_path, length_ms)
    arguments = [ffmpeg, "-y", *inputs]
    for layer_path in layer_paths:
        arguments += ["-i", str(layer_path)]

    shot_path = working_directory / f"{name}.mp4"
    arguments += [
        "-filter_complex", ";".join(_shot_filters(
            chain, layer_paths, reveal_times(section, window, points),
            length_ms, opens_the_video, closes_the_video)),
        "-map", "[out]",
        "-t", f"{length_ms / 1000:.3f}",
        "-r", str(FRAME_RATE), "-c:v", "libx264", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", str(shot_path),
    ]
    _run_ffmpeg(arguments, f"drawing {step}")
    return shot_path


def _shot_filters(
    chain: str,
    layer_paths: list[Path],
    reveals: list[int],
    length_ms: int,
    opens_the_video: bool,
    closes_the_video: bool,
) -> list[str]:
    """The filter graph for one shot: the move, the reveals, and the fades."""
    steps = [f"[0:v]{chain}[v0]"]
    for at, (_layer, at_ms) in enumerate(zip(layer_paths, reveals, strict=True)):
        steps.append(
            f"[v{at}][{at + 1}:v]overlay=enable='gte(t,{at_ms / 1000:.2f})'[v{at + 1}]"
        )

    finish = ["format=yuv420p"]
    if opens_the_video:
        finish.insert(0, "fade=t=in:st=0:d=0.6")
    if closes_the_video:
        finish.insert(0, f"fade=t=out:st={max(0.0, length_ms / 1000 - 0.8):.3f}:d=0.8")
    steps.append(f"[v{len(layer_paths)}]{','.join(finish)}[out]")
    return steps


def _cut_section(
    ffmpeg: str,
    section: RenderedSection,
    shot_paths: list[Path],
    durations: list[int],
    fade_ms: int,
    index: int,
    working_directory: Path,
) -> Path:
    """One section's shots, dissolved together, under its narration.

    Cut to exactly `total_ms`: `-shortest` does not cut a still-image stream, so
    sections overran and the drift compounded down the video.
    """
    dissolving = bool(fade_ms) and len(shot_paths) > 1
    arguments = [ffmpeg, "-y"]

    if dissolving:
        for shot_path in shot_paths:
            arguments += ["-i", str(shot_path)]
        audio_index = len(shot_paths)
    else:
        concat_list = working_directory / f"s{index:02d}_shots.txt"
        concat_list.write_text(
            "\n".join(f"file '{path.as_posix()}'" for path in shot_paths),
            encoding="utf-8")
        arguments += ["-f", "concat", "-safe", "0", "-i", str(concat_list)]
        audio_index = 1

    if section.audio_path and section.audio_path.exists():
        arguments += ["-i", str(section.audio_path)]
        # The voice starts when the title card ends -- and where there is no
        # card, it starts at once, which is the silence this removed.
        audio_filter = (f"adelay={section.title_card_ms}:all=1,apad"
                        if section.title_card_ms else "apad")
    else:
        arguments += ["-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono"]
        audio_filter = "apad"

    if dissolving:
        arguments += [
            "-filter_complex", ";".join(_dissolve_filters(shot_paths, durations, fade_ms)),
            "-map", "[vout]",
        ]
    else:
        arguments += [
            "-map", "0:v",
            "-vf", f"scale={FRAME_WIDTH}:{FRAME_HEIGHT},format=yuv420p",
        ]

    clip_path = working_directory / f"s{index:02d}.mp4"
    arguments += [
        "-map", f"{audio_index}:a", "-af", audio_filter,
        "-r", str(FRAME_RATE), "-c:v", "libx264", "-preset", "veryfast",
        # One sample rate and layout for every clip, whatever the voice provider
        # produced, so the final copy-concat has matching streams.
        "-c:a", "aac", "-b:a", "160k", "-ar", "24000", "-ac", "1",
        "-t", f"{section.total_ms / 1000:.3f}",
        str(clip_path),
    ]
    _run_ffmpeg(arguments, f"cutting section {index + 1} ({section.title[:40]})")
    return clip_path


def _dissolve_filters(
    shot_paths: list[Path], durations: list[int], fade_ms: int
) -> list[str]:
    """Chained cross-fades that still land on the section's exact length.

    Each dissolve starts a fade *early* and every shot was encoded a fade longer
    than its slot, so the overlap is paid for out of the tail rather than taken
    out of the clock.
    """
    steps = []
    current = "0:v"
    offset_ms = 0
    for at in range(1, len(shot_paths)):
        offset_ms += durations[at - 1]
        steps.append(
            f"[{current}][{at}:v]xfade=transition=fade:"
            f"duration={fade_ms / 1000:.3f}:"
            f"offset={(offset_ms - fade_ms) / 1000:.3f}[x{at}]"
        )
        current = f"x{at}"
    steps.append(f"[{current}]scale={FRAME_WIDTH}:{FRAME_HEIGHT},format=yuv420p[vout]")
    return steps


def _join_and_level(
    ffmpeg: str, clip_paths: list[Path], working_directory: Path, output_video_path: Path
) -> None:
    """Concatenate the sections, then level the whole soundtrack once.

    One loudness pass over the finished audio, not one per section: levelling
    each section on its own makes every section internally consistent and each
    one a different loudness, which is the thing a viewer actually notices. The
    video is copied, so this costs a pass over the file and no quality.

    `+faststart` moves the moov atom to the front. Without it the index sits at
    the end of the file, so a browser must download all of it before the first
    frame plays -- which looks exactly like a video that does not work.
    """
    joined_list = working_directory / "clips.txt"
    joined_list.write_text(
        "\n".join(f"file '{path.as_posix()}'" for path in clip_paths), encoding="utf-8"
    )

    joined_path = working_directory / "joined.mp4"
    _run_ffmpeg(
        [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(joined_list),
         "-c", "copy", str(joined_path)],
        "joining the sections",
    )

    output_video_path.parent.mkdir(parents=True, exist_ok=True)
    _run_ffmpeg(
        [ffmpeg, "-y", "-i", str(joined_path), "-c:v", "copy",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:a", "aac", "-b:a", "160k", "-ar", "24000", "-ac", "1",
         "-movflags", "+faststart", str(output_video_path)],
        "levelling the audio",
    )
