"""Rendering — plan plus script becomes an actual video file.

Writes `reviewing/output/<slug>.mp4` and a matching `.srt`/`.vtt`.

**Audio is the clock.** Each section's narration is synthesised first, its real
duration is *measured* from the file, and only then is the picture cut to fit.
Deciding the picture timing from the plan's estimated seconds and hoping the
voice matches is how animation drifts out of sync with narration, and no amount
of prompting fixes a clock that guesses.

**Every scene is a program's clip.** Generation makes one approved clip per
scene; the render lays them end to end under the narration, a title card in
front of each section. A project that never opened Generation still gets a
video: a section shows the pictures its own plan section draws on (chosen on
Assets & Design) beside the words being spoken, drawn with the source's own
styling when the project asked for it. Nothing is generated to fill a frame; a
section with no picture gets text on the project's own background.

**The narration is never on screen.** It is being spoken; printing it as well
reads as slides with a voice over them. A scene shows its headline.

**The picture changes per scene, not per sentence.** A scene whose narration
fills three slides is one continuous shot, a clip plays once instead of
restarting, and one shot dissolves into the next.

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

from pipeline import project_work
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

# How many characters of narration one subtitle cue holds: about two lines,
# which can be read in the seconds it is on screen. A sentence longer than this
# is still one cue: cutting mid-clause reads worse than a long line.
CHARACTERS_PER_CUE = 90


class RenderFailed(Exception):
    """Rendering did not produce a video. Names the step that failed."""


@dataclass
class Shot:
    """One scene's picture, or the clip a program drew for it.

    A scene, not a slide: one scene's narration may fill three slides, and all
    three are the same shot, so a clip plays through once instead of restarting.
    """

    picture: Path | None = None

    # The clip a scene program rendered. It replaces the still: a clip already
    # carries its own words and motion.
    clip: Path | None = None

    # The scene's headline, drawn over the still of a scene that has no clip.
    headline: str = ""


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
    """Where the headline sits on the frame."""

    heading_font: object
    headline_rows: tuple[tuple[str, int, int], ...]


def _words_layout(
    headline: str, style: RenderStyle, showing_picture: bool, is_title: bool,
) -> WordsLayout:
    headline_size = 82 if is_title else (56 if showing_picture else 68)
    wrap_at = 20 if showing_picture else 30

    if showing_picture:
        left = int(TEXT_BOX_WITH_PICTURE[0] * FRAME_WIDTH)
        top = int(TEXT_BOX_WITH_PICTURE[1] * FRAME_HEIGHT)
        bottom = int(TEXT_BOX_WITH_PICTURE[3] * FRAME_HEIGHT)
    else:
        left, top, bottom = 200, 300, FRAME_HEIGHT - 240

    lines = textwrap.wrap(headline, width=wrap_at)[:3] or [headline]
    line_height = int(headline_size * 1.22)
    y = max(top, (top + bottom - line_height * len(lines)) // 2)

    return WordsLayout(
        heading_font=_load_font(headline_size, bold=True, family=style.heading_font),
        headline_rows=tuple(
            (line, left, y + index * line_height) for index, line in enumerate(lines)),
    )


def _draw_frame(
    headline: str,
    footer: str,
    accent_text: str,
    style: RenderStyle = DEFAULT_STYLE,
    picture: Path | None = None,
    is_title: bool = False,
):
    """One 1920x1080 frame: the background, the scene's picture, and its headline.

    **Not the narration.** It is being spoken; printing it as well is what made
    this read as slides with a voice over them. A headline of a few words is what
    somebody can take in while listening to something else.
    """
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), style.background_colour)
    _paste_background(image, style)
    draw = ImageDraw.Draw(image)

    showing_picture = False
    if _readable_picture(picture):
        showing_picture = _paste_picture(image, draw, picture, style)

    if not showing_picture:
        # No picture: the words sit on a panel.
        draw.rounded_rectangle(
            [(110, 110), (FRAME_WIDTH - 110, FRAME_HEIGHT - 110)],
            radius=28, fill=style.panel_colour,
        )
        draw.rectangle([(110, 110), (FRAME_WIDTH - 110, 118)], fill=style.accent_colour)

    layout = _words_layout(headline, style, showing_picture, is_title)
    text_left = layout.headline_rows[0][1]

    if accent_text:
        draw.text((text_left, int(0.09 * FRAME_HEIGHT)), accent_text.upper(),
                  font=_load_font(30, bold=True, family=style.heading_font),
                  fill=style.accent_colour)

    for line, left, top in layout.headline_rows:
        draw.text((left, top), line, font=layout.heading_font, fill=style.text_colour)

    if footer:
        draw.text((text_left, FRAME_HEIGHT - 190), footer,
                  font=_load_font(26, family=style.body_font), fill=style.dim_text_colour)

    return image


# The whitespace after a sentence's closing punctuation, or after a closing
# quote or bracket that follows it. Only the whitespace is consumed: the
# punctuation and the quote stay with their sentence.
SENTENCE_BOUNDARY = re.compile(
    r"(?:(?<=[.!?\u2026])|(?<=[.!?\u2026][\"'\u201d\u2019)]))\s+"
)


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
            if len(candidate) > CHARACTERS_PER_CUE and current:
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
    scene whose narration fills three cues is one continuous shot, not three
    stills restarting (the carousel one level down): a clip plays once rather
    than three times.
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


def write_subtitles(sections: list[RenderedSection], path: Path) -> None:
    """One cue per sentence or two, from the same segments the picture is cut to."""
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
        project_work.run(arguments, check=True, timeout=1800)
    except subprocess.CalledProcessError as failure:
        # The last lines of stderr say what ffmpeg actually objected to; the exit
        # code alone says nothing anyone can act on.
        tail = "\n".join((failure.stderr or "").strip().splitlines()[-6:])
        raise RenderFailed(f"ffmpeg failed while {step}:\n{tail}") from failure
    except subprocess.TimeoutExpired as timeout:
        raise RenderFailed(f"ffmpeg timed out while {step}") from timeout


def _shot_for(section: RenderedSection, segment: Segment) -> Shot:
    """What is on screen for this slide.

    Generation decides per scene. Without it, the section's own pictures are
    dealt out slide by slide.
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
        return Shot(picture=section.pictures[0])
    index = max(0, segment.scene_index) % len(section.pictures)
    return Shot(picture=section.pictures[index])


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

    A clip plays and then holds its last frame (`tpad`) rather than looping: a
    scene that finished assembling should stay assembled while the narration
    talks about it, not start over.
    """
    if shot.clip is not None and shot.clip.exists():
        return (
            ["-i", str(shot.clip)],
            f"scale={FRAME_WIDTH}:{FRAME_HEIGHT}:force_original_aspect_ratio=decrease,"
            f"pad={FRAME_WIDTH}:{FRAME_HEIGHT}:-1:-1:color=black,fps={FRAME_RATE},"
            f"tpad=stop_mode=clone:stop_duration={length_ms / 1000:.3f}",
        )
    return (["-loop", "1", "-i", str(frame_path)],
            f"scale={FRAME_WIDTH}:{FRAME_HEIGHT},fps={FRAME_RATE}")


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
    """One scene: its frame (or clip) and the fades at the ends of the video."""
    shot = _shot_for(section, window.segments[0])
    is_title = window.kind == "title"
    headline = section.title if is_title else (shot.headline or section.title)

    frame_path = working_directory / f"{name}.png"
    _draw_frame(
        headline, "" if is_title else section.title, kicker, style,
        picture=None if shot.clip is not None else shot.picture, is_title=is_title,
    ).save(frame_path)

    inputs, chain = _shot_source(shot, frame_path, length_ms)
    shot_path = working_directory / f"{name}.mp4"
    arguments = [
        ffmpeg, "-y", *inputs,
        "-filter_complex", _shot_filter(chain, length_ms, opens_the_video, closes_the_video),
        "-map", "[out]",
        "-t", f"{length_ms / 1000:.3f}",
        "-r", str(FRAME_RATE), "-c:v", "libx264", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", str(shot_path),
    ]
    _run_ffmpeg(arguments, f"drawing {step}")
    return shot_path


def _shot_filter(
    chain: str, length_ms: int, opens_the_video: bool, closes_the_video: bool,
) -> str:
    """The filter graph for one shot: its sizing chain and the fades."""
    finish = ["format=yuv420p"]
    if opens_the_video:
        finish.insert(0, "fade=t=in:st=0:d=0.6")
    if closes_the_video:
        finish.insert(0, f"fade=t=out:st={max(0.0, length_ms / 1000 - 0.8):.3f}:d=0.8")
    return f"[0:v]{chain},{','.join(finish)}[out]"


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
