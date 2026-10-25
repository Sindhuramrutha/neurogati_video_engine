"""Scenes as shots: the model fills a template's slots; the program is written here.

Told to start from a template, the model still wrote every layout by hand -- 0
of 7 scenes in a measured run used one -- and every round went to the same
collisions. So it no longer writes the code for a template scene: it answers with
the shots, as data, and this writes the program that calls the kit's templates
(`manimkit`), which lay out, time and move a scene so it passes the checks by
construction. A scene the templates cannot express is still written by hand.

    {"renderer": "manim", "approach": "...", "shots": [
       {"template": "hero", "title": "Galvani's frog", "picture": 0, "when": "a dead frog",
        "callouts": [{"label": "Frog's leg", "at": [0.55, 0.40], "when": "leg kicked"}]}]}

A picture is an index into the brief's offered pictures. `when` is the narration
words a part arrives on. A scene has one to three shots; each after the first
begins on its own `when`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

TEMPLATES = ("hero", "steps", "compare", "person", "key_idea", "opener", "flow", "hub",
             "timeline")
MOST_SHOTS = 3
MOST_CALLOUT_WORDS = 4
# Each part keeps its moment; the kit shows two marks at a time, so more is not clutter.
MOST_CALLOUTS = 5
# The ways a callout points at its part (manimkit.hero): one chosen for each.
POINTING = ("tag", "glow", "zoom", "lens", "sketch", "caption")
MOST_IDEA_WORDS = 18            # more read as a paragraph on screen (the check allows 18)
# A label with one of these says something ("thought is segmented"); it names nothing.
STATING = {"is", "are", "was", "were", "be", "been", "has", "have", "had", "does", "did"}

GUIDE = """Shots (the preferred answer -- no code): a ```json block with "shots", a list of
one to three of these, each {"template": ..., then its slots}; "picture" is an index into
the brief's assets.pictures, "when" the exact narration words a part arrives on:
- hero: "title", "picture", "when", "callouts": [{"label", "part", "when", "style"}] (0 to
  5; as few as the teaching needs, every part the narration explains given its moment --
  two at most are on screen at once, the oldest going as the next comes) -- one picture
  large and the parts the narration TEACHES pointed out on their words
  (a label is a part's name, 1-4 words, never a statement). "part" is one of the
  picture's parts exactly as its description lists them: the pointer goes to where that
  part really is, and a callout naming no listed part is left out. "style" is how it is
  pointed out -- vary them through the video, choosing for the moment:
    "tag" -- a small tag beside the part, a short tick to it: naming one small thing.
    "glow" -- the rest of the frame softens and a glow rings the part, its name in a
      caption: "look here" while it is spoken.
    "zoom" -- the view eases in on the part and back out: a detail too small to see.
    "lens" -- a round magnifier beside the part shows it enlarged: a tiny structure
      (a synapse, a cell) kept in its place.
    "sketch" -- a hand-drawn loop round the part, its name beside: an informal "this one".
    "caption" -- its name on a card at the foot of the frame, nothing on the picture: a
      person, a whole scene, an era.
  What deserves pointing out: only what the narration explains at that moment -- never a
  book's publisher, author line or logo, never furniture or a background object, never a
  person's body unless the body is the lesson. A person is named with "caption", never
  pinned (the kit enforces it for any large figure). None at all is often best: a
  picture that already shows what is said needs no pointer. Optional "moves": [{"through": [2 to 6
  part names, in order], "when"}] -- a glowing pulse runs through those parts on the
  words: a signal down a nerve, current through a wire. Use it wherever the narration
  says something travels.
- steps: "title", "steps": [{"label", "picture" (or null), "when"}] -- 2 to 4 steps in order
- compare: "title", "left" and "right": {"heading", "picture" (or null), "points": [up to
  3 short], "when"}
- person: "picture", "name", "line", "when", "line_when"
- key_idea: "statement", "picture" (or null), "when"
- opener: "picture", "title", "when", "lines": [{"text", "when"}] (0 to 3 short) -- a topic
  opened, its context given or a section closed on a picture that SETS THE SCENE (the
  deck's own art, a cover, a portrait of the era): the picture large, slowly drawing
  nearer, the title and lines beside it. For a picture with role sets_scene.
- flow: "title", "steps": [{"label", "when"}] -- boxes joined by arrows
- hub: "title", "centre", "items": [{"label", "when"}] -- one idea and its parts
- timeline: "title", "events": [{"label", "when"}] -- things in order
Choosing: a thing that can be seen -- an experiment, an organ, an apparatus, a person -- is
shown in its picture (hero, steps with pictures, person, compare with pictures), never as
words in boxes; flow, hub and timeline are for ideas no picture shows; a scene that opens a
topic or gives its context can open on the deck's own art (opener). Narration that goes
in steps ("step two... then...") is steps, or one shot per step, not one still hero. Spread
the "when"s over the WHOLE narration: the frame must change on the later sentences too --
end on a key_idea when the narration ends on its point.
The brief's "direction" is the art director's plan for this scene -- its style, picture,
background, layout and motion; its picture and background are already made for you.
Follow it; depart from it only for a reason you give in "approach".
The scene's pictures are yours: look at what each shows, and use it, leave it out, or
have one painted -- add "paint": "one still picture, its subject and style exactly" to
the json, for one no offered picture shows, or for a better version of one that is not
right, saying what to change (up to three a scene). It is painted, checked and offered to
you as this scene's own picture -- far better than a scene of words alone.
Background: add "background" to the json -- {"kind": "image", "describe": "the art behind
the scene, filling the screen edge to edge: soft pastel botanical leaves at the edges, a
cosy illustrated bookshelf, warm paper with
a faint grid..."} or {"kind": "gradient", "colours": ["#hex", "#hex"], "split": "none" |
"left" | "right" | "top" | "bottom" | "diagonal", "panel": "#hex"} (a gradient split
into a coloured section). About seven scenes in ten get painted art and the rest a
gradient: the notes say how the video stands. Always light and pleasant, in colours that
suit each other -- artistic, a frame people want to look at, but calm and never overdone;
never a dark frame. Words on screen are not needed: a picture or a diagram can carry it.
Labels are a few words from the narration. A callout names a part the narration speaks of,
on the words that speak of it -- never one it does not (a desk, a pedestal, a head that
is only there): a label that teaches nothing is clutter, and none is better. The label
must be true of the very part it points at -- read the parts list before choosing -- and
name that part or what it is in this story, never an idea about the whole picture.
A picture whose catalogue entry has "main_of"
is another scene's subject: here it may only be small (steps, compare), never the picture
of a hero, person, opener or key_idea. A picture painted for this scene was made to be its
main picture: show it large. The brief's DRAW, LAYOUT and BEATS are direction -- what to
teach, on which words -- not a drawing to copy: a shot that teaches the same idea on the
same words fulfils them (ten stops on a road are a timeline of its main stops; a thought
coming apart is a hub, or the painting with its parts named). Write a program by hand
only when no shot can teach the idea -- hand-placed layouts are what fail the checks and
the reviewer most -- then send the file, and say why in "approach"."""


def _text(value: Any, where: str, required: bool = True) -> str:
    if value is None or str(value).strip() == "":
        if required:
            raise ValueError(f"{where} is missing")
        return ""
    return str(value).strip()[:120]


@dataclass(frozen=True)
class Pictures:
    """What the shots may use: how many pictures the brief offers, where each one's
    parts are (picture_parts), which are another scene's subject, and -- for the
    program to name them -- each one's file and what it shows (shot_values)."""
    count: int
    parts: dict[int, list] = field(default_factory=dict)
    taken: frozenset[int] = frozenset()
    files: tuple[str, ...] = ()
    about: tuple[str, ...] = ()


def _index(value: Any, pictures: Pictures, where: str, main: bool = False) -> int:
    try:
        index = int(value)
    except (TypeError, ValueError) as wrong:
        raise ValueError(f"{where}: a picture is an index into assets.pictures") from wrong
    if not 0 <= index < pictures.count:
        # A scene with no picture asked for one 23 times; it is told how to get one.
        raise ValueError(f"{where}: there is no picture {index} (the brief offers "
                         f"{pictures.count}). To show one, ask for it painted: add "
                         "\"paint\": \"the picture, its subject and style exactly\" to the "
                         "json, or use a shot without a picture")
    if main and index in pictures.taken:
        # The same picture scene after scene made the video look like one scene.
        raise ValueError(f"{where}: picture {index} is another scene's subject; here it may "
                         "only be small (steps, compare). Give this scene its own main "
                         "picture: another one; or ask for one painted -- add \"paint\": "
                         "\"the picture, its subject exactly\" to the json; or a diagram")
    return index


def _items(value: Any, where: str, least: int, most: int) -> list[dict]:
    if not isinstance(value, list) or not least <= len(value) <= most:
        raise ValueError(f"{where} must be a list of {least} to {most}")
    return [item if isinstance(item, dict) else {"label": item} for item in value]




LONGEST_STILL_SECONDS = 8.0     # of narration with nothing new arriving


def _cues(spec: dict) -> list[str]:
    """Every `when` in the shots: the words each part arrives on."""
    found: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ("when", "line_when", "begins") and isinstance(item, str):
                    found.append(item)
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(spec.get("shots") or [])
    return found


def uncovered(spec: dict, words: list[dict], seconds: float) -> str:
    """What to tell the model when its shots leave a long stretch of narration
    with nothing new on screen. A measured scene put every cue in the first half
    and stood still through "Nothing electrical had touched that heart..."; told
    only "keep things arriving", six rounds did not move it."""
    import re

    def norm(text: str) -> list[str]:
        return re.findall(r"[a-z0-9']+", text.lower())

    spoken = [(norm(w.get("text", "")), w.get("start_ms", 0) / 1000) for w in words]
    flat = [(word, at) for parts, at in spoken for word in parts]
    times = [0.0, seconds]
    for cue in _cues(spec):
        wanted = norm(cue)
        for start in range(len(flat) - len(wanted) + 1):
            if wanted and [w for w, _ in flat[start:start + len(wanted)]] == wanted:
                times.append(flat[start][1])
                break
    times.sort()
    gap, begins = max((b - a, a) for a, b in zip(times, times[1:], strict=False))
    if gap < max(LONGEST_STILL_SECONDS, 0.3 * seconds):
        return ""
    stretch = [w for w, at in flat if begins + 1.0 < at < begins + gap]
    if len(stretch) < 6:
        return ""
    said = " ".join(stretch[:30]) + (" ..." if len(stretch) > 30 else "")
    return (f"Nothing new arrives for {gap:.0f} s of the {seconds:.0f} s, from {begins:.0f} s: "
            f'while the narration says "{said}" the frame stands still. Give those words a '
            "shot that begins on them -- a key_idea with their point, or steps or compare -- "
            "or set later parts' \"when\" on them.")


def unheard(spec: dict, words: list[dict], narration: str = "") -> list[str]:
    """The "when"s that are not words the narration says. One not found was timed by
    a guess: two of three steps never came on screen before the scene moved on. The
    written narration counts too: the voice's timings spell a name as it is said
    ("Layvenhook"), and "Leeuwenhoek" was refused in every round."""
    if not words:                  # no timings yet: nothing to time the cues against
        return []
    said = [" " + " ".join(_norm(w.get("text", "")) for w in words) + " ",
            f" {_norm(narration)} "]
    return [cue for cue in _cues(spec)
            if _norm(cue) and not any(f" {_norm(cue)} " in text for text in said)]


def _norm(text: str) -> str:
    import re

    return " ".join(re.findall(r"[a-z0-9']+", text.lower()))


def _begins(shot: dict) -> str | None:
    """The words a shot begins on: its own "when", or its first part's. A steps or
    flow shot has its cues on its parts; without them the shot before it was cleared
    a second after it appeared, and the frame stood empty until the first part."""
    return shot.get("when") or shot.get("begins") or next(iter(_cues({"shots": [shot]})), None)


def is_shots(spec: dict) -> bool:
    return isinstance(spec.get("shots"), list) and bool(spec["shots"])
