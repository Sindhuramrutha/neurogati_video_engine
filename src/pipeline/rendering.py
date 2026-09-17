"""Rendering — plan plus script becomes an actual video file.

The stage that did not exist. Everything before this produced text; this produces
`reviewing/output/<slug>.mp4` and a matching `.srt`.

**Audio is the clock** ([ADR 0001](../../docs/decisions/0001-preserve-audio-first-timing.md)).
Each section's narration is synthesised first, its real duration is *measured*
from the file, and only then is the picture cut to fit. The alternative --
deciding the picture timing from the plan's estimated seconds and hoping the
voice matches -- is exactly how v1's animations drifted out of sync with the
narration, and no amount of prompting fixes a clock that guesses.

The visuals are deliberately plain: a title card per section, then the narration
as text slides. Not because plain is the goal, but because an honest plain
render beats a beautiful one that misrepresents the content. Diagrams come when
there is something that can draw them and check the result
([ADR 0007](../../docs/decisions/0007-revideo-as-rendering-target.md) is still
unbuilt).

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

logger = logging.getLogger(__name__)

FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080
FRAME_RATE = 30

# The stage colours the UI already uses, so a rendered video looks like it came
# from this app rather than from a generic slide tool.
BACKGROUND_COLOUR = (13, 15, 20)
SURFACE_COLOUR = (20, 23, 31)
TEXT_COLOUR = (232, 234, 240)
DIM_TEXT_COLOUR = (154, 163, 181)
ACCENT_COLOUR = (232, 121, 168)

# A title card needs long enough to read but not so long it stalls the video.
TITLE_CARD_MS = 2500

# Roughly how many characters of narration fit on one slide at this size.
CHARACTERS_PER_SLIDE = 260


class RenderFailed(Exception):
    """Rendering did not produce a video. Names the step that failed."""


@dataclass
class RenderedSection:
    section_id: str
    title: str
    narration: str
    audio_path: Path | None = None
    audio_duration_ms: int = 0
    start_ms: int = 0

    @property
    def total_ms(self) -> int:
        return TITLE_CARD_MS + self.audio_duration_ms


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


def _load_font(size: int, bold: bool = False):
    """A real font if one can be found, the bitmap default if not.

    Falling back rather than failing: a video with ugly text is worth more than
    no video, and the default font is legible even if it is not pretty.
    """
    from PIL import ImageFont

    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                continue

    logger.warning("no TrueType font found; falling back to the bitmap default")
    return ImageFont.load_default()


def _draw_frame(lines: list[str], subtitle: str, accent_text: str, font_size: int):
    """One 1920x1080 frame: an accent label, the body lines, and a footer."""
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (FRAME_WIDTH, FRAME_HEIGHT), BACKGROUND_COLOUR)
    draw = ImageDraw.Draw(image)

    # A surface panel so the text sits on something, matching the app's chrome.
    draw.rounded_rectangle(
        [(110, 110), (FRAME_WIDTH - 110, FRAME_HEIGHT - 110)],
        radius=28, fill=SURFACE_COLOUR,
    )
    draw.rectangle([(110, 110), (FRAME_WIDTH - 110, 118)], fill=ACCENT_COLOUR)

    if accent_text:
        draw.text((170, 170), accent_text.upper(), font=_load_font(30, bold=True),
                  fill=ACCENT_COLOUR)

    body_font = _load_font(font_size, bold=True)
    line_height = int(font_size * 1.45)
    total_height = line_height * len(lines)
    y = max(280, (FRAME_HEIGHT - total_height) // 2)

    for line in lines:
        draw.text((170, y), line, font=body_font, fill=TEXT_COLOUR)
        y += line_height

    if subtitle:
        draw.text((170, FRAME_HEIGHT - 190), subtitle, font=_load_font(26),
                  fill=DIM_TEXT_COLOUR)

    return image


# The whitespace after a sentence's closing punctuation, or after a closing
# quote or bracket that follows it. Only the whitespace is consumed: the
# punctuation and the quote stay with their sentence.
SENTENCE_BOUNDARY = re.compile(
    r"(?:(?<=[.!?\u2026])|(?<=[.!?\u2026][\"'\u201d\u2019)]))\s+"
)


def _slides_for_narration(narration: str) -> list[str]:
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
    slides: list[str] = []
    for paragraph in re.split(r"\n\s*\n", narration):
        flattened = " ".join(paragraph.split())
        if not flattened:
            continue
        current = ""
        for sentence in (s for s in SENTENCE_BOUNDARY.split(flattened) if s):
            candidate = f"{current} {sentence}".strip()
            if len(candidate) > CHARACTERS_PER_SLIDE and current:
                slides.append(_as_finished_sentence(current))
                current = sentence
            else:
                current = candidate
        if current:
            slides.append(_as_finished_sentence(current))
    return slides or [narration]


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

    @property
    def end_ms(self) -> int:
        return self.start_ms + self.duration_ms


def section_segments(section: RenderedSection) -> list[Segment]:
    """The title card, then the narration split into slides, exactly filling
    `section.total_ms`.

    Slides share the narration's *measured* duration in proportion to their
    text, using cumulative rounding so the pieces sum to the exact audio length
    -- no slide is lost to rounding and none overruns.
    """
    segments = [Segment("title", section.title, section.start_ms, TITLE_CARD_MS)]

    if not section.audio_duration_ms or not section.narration.strip():
        return segments

    slides = _slides_for_narration(section.narration)
    total_characters = sum(len(slide) for slide in slides) or 1
    narration_start_ms = section.start_ms + TITLE_CARD_MS

    characters_so_far = 0
    previous_boundary_ms = 0
    for slide in slides:
        characters_so_far += len(slide)
        boundary_ms = round(section.audio_duration_ms * characters_so_far / total_characters)
        segments.append(Segment(
            "slide", slide,
            narration_start_ms + previous_boundary_ms,
            boundary_ms - previous_boundary_ms,
        ))
        previous_boundary_ms = boundary_ms

    return segments


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


def render_sections(
    sections: list[RenderedSection],
    working_directory: Path,
    output_video_path: Path,
) -> None:
    """Draw every frame, cut each section to its exact length, and concatenate.

    One clip per section rather than one long filtergraph: a failure names the
    section that caused it.

    Three details carry the timing, and each fixes something that was wrong:

    - **Narration is delayed past the title card** (`adelay`), so the voice
      starts when the first slide appears -- it used to start under the title.
    - **Each clip is cut to exactly `total_ms`** with `-t`. `-shortest` did not
      cut the still-image stream, so sections overran and the drift compounded.
    - **Every clip has an audio stream**, silent if there is no narration.
      Concatenating with `-c copy` needs identical streams in every clip; one
      without audio produces a file whose sound stops partway through.
    """
    ffmpeg = require_ffmpeg()
    working_directory.mkdir(parents=True, exist_ok=True)
    clip_paths: list[Path] = []

    for index, section in enumerate(sections):
        frame_specs: list[tuple[Path, int]] = []

        for segment_index, segment in enumerate(section_segments(section)):
            frame_path = working_directory / f"s{index:02d}_{segment_index:02d}.png"
            if segment.kind == "title":
                image = _draw_frame(
                    textwrap.wrap(segment.text, width=34)[:4],
                    "", f"Section {index + 1}", 78,
                )
            else:
                image = _draw_frame(
                    textwrap.wrap(segment.text, width=52)[:9],
                    section.title, f"Section {index + 1}", 46,
                )
            image.save(frame_path)
            frame_specs.append((frame_path, segment.duration_ms))

        # An ffconcat list gives each still its own on-screen duration without
        # generating thousands of duplicate frames. ffconcat ignores the last
        # entry's duration unless the file is repeated; `-t` trims the excess.
        concat_list = working_directory / f"s{index:02d}_frames.txt"
        lines = []
        for frame_path, duration_ms in frame_specs:
            lines.append(f"file '{frame_path.as_posix()}'")
            lines.append(f"duration {duration_ms / 1000:.3f}")
        lines.append(f"file '{frame_specs[-1][0].as_posix()}'")
        concat_list.write_text("\n".join(lines), encoding="utf-8")

        has_narration = bool(section.audio_path and section.audio_path.exists())
        exact_seconds = f"{section.total_ms / 1000:.3f}"

        arguments = [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list)]
        if has_narration:
            arguments += ["-i", str(section.audio_path)]
            audio_filter = f"adelay={TITLE_CARD_MS}:all=1,apad"
        else:
            arguments += ["-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono"]
            audio_filter = "apad"

        clip_path = working_directory / f"s{index:02d}.mp4"
        arguments += [
            "-map", "0:v", "-map", "1:a",
            "-vf", f"scale={FRAME_WIDTH}:{FRAME_HEIGHT},format=yuv420p",
            "-af", audio_filter,
            "-r", str(FRAME_RATE), "-c:v", "libx264", "-preset", "veryfast",
            # One sample rate and layout for every clip, whatever the voice
            # provider produced, so the final copy-concat has matching streams.
            "-c:a", "aac", "-b:a", "160k", "-ar", "24000", "-ac", "1",
            "-t", exact_seconds,
            str(clip_path),
        ]

        _run_ffmpeg(arguments, f"rendering section {index + 1} ({section.title[:40]})")
        clip_paths.append(clip_path)

    joined_list = working_directory / "clips.txt"
    joined_list.write_text(
        "\n".join(f"file '{path.as_posix()}'" for path in clip_paths), encoding="utf-8"
    )

    output_video_path.parent.mkdir(parents=True, exist_ok=True)
    # +faststart moves the moov atom to the front. Without it the index sits at
    # the end of the file, so a browser must download all of it before the first
    # frame plays -- which looks exactly like a video that does not work.
    _run_ffmpeg(
        [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(joined_list),
         "-c", "copy", "-movflags", "+faststart", str(output_video_path)],
        "joining the sections",
    )
