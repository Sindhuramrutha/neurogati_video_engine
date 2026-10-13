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

from typing import Any

TEMPLATES = ("hero", "steps", "compare", "person", "key_idea", "flow", "hub", "timeline")
MOST_SHOTS = 3
MOST_CALLOUT_WORDS = 4
# A label with one of these says something ("thought is segmented"); it names nothing.
STATING = {"is", "are", "was", "were", "be", "been", "has", "have", "had", "does", "did"}

GUIDE = """Shots (the preferred answer -- no code): a ```json block with "shots", a list of
one to three of these, each {"template": ..., then its slots}; "picture" is an index into
the brief's assets.pictures, "when" the exact narration words a part arrives on:
- hero: "title", "picture", "when", "callouts": [{"label", "at": [x, y], "when"}] -- one
  picture large and its parts named (a label is a part's name, 1-4 words, never a
  statement); at = the part's place as fractions of the picture
  from its top left, from the picture's description. Optional "moves": [{"along": [[x, y],
  ...2 to 8 points on the picture], "when"}] -- a glowing pulse runs along that path on
  the words: a signal down a nerve, current through a wire, liquid carried across. Use it
  wherever the narration says something travels; no need to write the scene by hand.
- steps: "title", "steps": [{"label", "picture" (or null), "when"}] -- 2 to 4 steps in order
- compare: "title", "left" and "right": {"heading", "picture" (or null), "points": [up to
  3 short], "when"}
- person: "picture", "name", "line", "when", "line_when"
- key_idea: "statement", "picture" (or null), "when"
- flow: "title", "steps": [{"label", "when"}] -- boxes joined by arrows
- hub: "title", "centre", "items": [{"label", "when"}] -- one idea and its parts
- timeline: "title", "events": [{"label", "when"}] -- things in order
Choosing: a thing that can be seen -- an experiment, an organ, an apparatus, a person -- is
shown in its picture (hero, steps with pictures, person, compare with pictures), never as
words in boxes; flow, hub and timeline are for ideas no picture shows. Narration that goes
in steps ("step two... then...") is steps, or one shot per step, not one still hero. Spread
the "when"s over the WHOLE narration: the frame must change on the later sentences too --
end on a key_idea when the narration ends on its point.
Labels are a few words from the narration. Write a program by hand only when no shot can
show the idea: then send the file, and say why in "approach"."""


def _text(value: Any, where: str, required: bool = True) -> str:
    if value is None or str(value).strip() == "":
        if required:
            raise ValueError(f"{where} is missing")
        return ""
    return str(value).strip()[:120]


def _picture(value: Any, pictures: int, where: str, required: bool = False) -> str:
    if value is None or value == "":
        if required:
            raise ValueError(f"{where} needs a picture, and none is given")
        return "None"
    try:
        index = int(value)
    except (TypeError, ValueError) as wrong:
        raise ValueError(f"{where}: a picture is an index into assets.pictures") from wrong
    if not 0 <= index < pictures:
        raise ValueError(f"{where}: there is no picture {index} (the brief offers {pictures})")
    return f"P[{index}]"


def _when(value: Any) -> str:
    return repr(str(value).strip()) if value else "None"


def _items(value: Any, where: str, least: int, most: int) -> list[dict]:
    if not isinstance(value, list) or not least <= len(value) <= most:
        raise ValueError(f"{where} must be a list of {least} to {most}")
    return [item if isinstance(item, dict) else {"label": item} for item in value]


def _shot_code(shot: dict, pictures: int, at: int) -> list[str]:
    template = shot.get("template")
    # A scene opens on its picture at once: a first shot waiting for its words
    # left the screen blank until the narration reached "Galen".
    opening = "None" if at == 0 else _when(shot.get("when"))
    where = f"shot {at + 1} ({template})"
    title = repr(_text(shot.get("title"), f"{where} title", required=False))
    if template == "hero":
        callouts = []
        for number, c in enumerate(_items(shot.get("callouts", []), f"{where} callouts", 1, 5)):
            point = c.get("at")
            if not (isinstance(point, list) and len(point) == 2):
                raise ValueError(f"{where} callout {number + 1}: 'at' must be [x, y]")
            x, y = (min(1.0, max(0.0, float(v))) for v in point)
            label = _text(c.get("label"), f"{where} callout label")
            if (len(label.split()) > MOST_CALLOUT_WORDS or label.rstrip().endswith((".", "!"))
                    or STATING.intersection(label.lower().split())):
                # "It was electrical" pointed at an engraving names nothing in it.
                raise ValueError(f"{where} callout {label!r} is a statement: a callout names "
                                 f"a part of the picture in 1 to {MOST_CALLOUT_WORDS} words "
                                 "('Frog's leg'); put a statement in a key_idea shot")
            callouts.append(f"({label!r}, "
                            f"({x:.2f}, {y:.2f}), {_when(c.get('when'))})")
        moves = []
        for number, move in enumerate(_items(shot.get("moves", []), f"{where} moves", 0, 3)):
            along = move.get("along")
            if not (isinstance(along, list) and 2 <= len(along) <= 8
                    and all(isinstance(p, list) and len(p) == 2 for p in along)):
                raise ValueError(f"{where} move {number + 1}: 'along' must be 2 to 8 [x, y] "
                                 "points on the picture")
            points = ", ".join(f"({min(1.0, max(0.0, float(x))):.2f}, "
                               f"{min(1.0, max(0.0, float(y))):.2f})" for x, y in along)
            moves.append(f"([{points}], {_when(move.get('when'))})")
        return [f"self.hero({_picture(shot.get('picture'), pictures, where, True)}, "
                f"[{', '.join(callouts)}], title={title}, cue={opening}"
                + (f", moves=[{', '.join(moves)}]" if moves else "") + ")"]
    if template == "steps":
        steps = [f"({_text(s.get('label'), f'{where} step label')!r}, "
                 f"{_picture(s.get('picture'), pictures, where)}, {_when(s.get('when'))})"
                 for s in _items(shot.get("steps"), f"{where} steps", 2, 4)]
        return [f"self.steps([{', '.join(steps)}], title={title})"]
    if template == "compare":
        sides = []
        for name in ("left", "right"):
            side = shot.get(name)
            if not isinstance(side, dict):
                raise ValueError(f"{where} needs '{name}'")
            points = [repr(_text(p, f"{where} {name} point"))
                      for p in (side.get("points") or [])[:3]]
            sides.append(f"({_text(side.get('heading'), f'{where} {name} heading')!r}, "
                         f"{_picture(side.get('picture'), pictures, where)}, "
                         f"[{', '.join(points)}], {_when(side.get('when'))})")
        return [f"self.compare({sides[0]}, {sides[1]}, title={title})"]
    if template == "person":
        return [f"self.person({_picture(shot.get('picture'), pictures, where, True)}, "
                f"{_text(shot.get('name'), f'{where} name')!r}, "
                f"{_text(shot.get('line'), f'{where} line')!r}, cue={opening}, "
                f"line_cue={_when(shot.get('line_when'))})"]
    if template == "key_idea":
        return [f"self.key_idea({_text(shot.get('statement'), f'{where} statement')!r}, "
                f"{_picture(shot.get('picture'), pictures, where)}, "
                f"cue={opening})"]
    if template in ("flow", "hub", "timeline"):
        return _diagram_code(template, shot, where, title)
    raise ValueError(f"{where}: template must be one of {', '.join(TEMPLATES)}")


def _diagram_code(template: str, shot: dict, where: str, title: str) -> list[str]:
    key = {"flow": "steps", "hub": "items", "timeline": "events"}[template]
    items = _items(shot.get(key), f"{where} {key}", 2, 6)
    labels = [repr(_text(i.get("label"), f"{where} label")) for i in items]
    whens = [_when(i.get("when")) for i in items]
    lines = []
    if title != repr(""):
        lines.append(f"self.play(self.reveal(self.title({title})))")
    if template == "flow":
        lines += [f"d = self.flow([{', '.join(labels)}])"]
        for number, when in enumerate(whens):
            lines.append(f"self._at_cue({when})")
            grow = f", self.grow(d.arrows[{number - 1}])" if number else ""
            lines.append(f"self.play(self.reveal(d.boxes[{number}]){grow})")
    elif template == "hub":
        centre = _text(shot.get("centre"), f"{where} centre")
        lines += [f"d = self.hub({centre!r}, [{', '.join(labels)}])",
                  "self.play(self.reveal(d.centre))"]
        for number, when in enumerate(whens):
            lines += [f"self._at_cue({when})",
                      f"self.play(self.grow(d.lines[{number}]), self.reveal(d.items[{number}]))"]
    else:
        lines += [f"d = self.timeline([{', '.join(labels)}])", "self.play(self.draw(d.spine))"]
        for number, when in enumerate(whens):
            lines += [f"self._at_cue({when})",
                      f"self.play(self.reveal(d.dots[{number}]), self.reveal(d.labels[{number}]))"]
    return lines


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


def is_shots(spec: dict) -> bool:
    return isinstance(spec.get("shots"), list) and bool(spec["shots"])


def program_for(spec: dict, pictures: int) -> str:
    """The scene program for these shots, or a ValueError saying what is wrong
    with them, for the model to correct."""
    shots = spec["shots"]
    if len(shots) > MOST_SHOTS:
        raise ValueError(f"a scene has at most {MOST_SHOTS} shots")
    body: list[str] = ["P = self.brief.assets.pictures"]
    for at, shot in enumerate(shots):
        if not isinstance(shot, dict):
            raise ValueError(f"shot {at + 1} must be an object")
        if at:
            body += [f"self._at_cue({_when(shot.get('when') or shot.get('begins'))})",
                     "self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)",
                     "self.clear()"]
        body += _shot_code(shot, pictures, at)
    body.append("self.finish()")
    indented = "\n".join("        " + line for line in body)
    return ("# /// script\n# requires-python = \">=3.11\"\n"
            "# dependencies = [\"manim>=0.19\", \"pillow\"]\n# ///\n"
            "# Written from the scene's shots (scene_shots.py): edit the shots, not this.\n"
            "from manimkit import *\n\n\n"
            "class TheScene(ExplainerScene):\n    def construct(self):\n"
            f"{indented}\n\n\nrun(TheScene)\n")
