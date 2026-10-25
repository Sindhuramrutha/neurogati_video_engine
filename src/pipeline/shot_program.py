"""The program written from a scene's shots, with every value in it.

`scene_shots` checks the shots; this writes the program that calls the kit's
templates (`manimkit`): the pictures it shows named at its top, each part's moment
as the second it is spoken (`shot_values`), and -- once a render has recorded them
(`decisions.json`) -- the place of every picture, title, tag and card, so nothing
about where or when is left outside the file. A table above each shot lists its
moments with the words spoken then.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pipeline.picture_parts import anchor, region
from pipeline.program_layout import _laid_out, _one_line
from pipeline.scene_shots import (
    MOST_CALLOUT_WORDS,
    MOST_CALLOUTS,
    MOST_IDEA_WORDS,
    MOST_SHOTS,
    POINTING,
    STATING,
    TEMPLATES,
    Pictures,
    _begins,
    _index,
    _items,
    _text,
)
from pipeline.shot_values import Timing, picture_names, second


@dataclass
class _Writing:
    """One program being written: its pictures (and the ones it uses), its timing,
    and the moments of the shot being written, for the table above it."""
    pictures: Pictures
    timing: Timing | None
    names: list[str]
    used: set[int] = field(default_factory=set)
    moments: list[tuple[float | None, str, str]] = field(default_factory=list)

    def picture(self, index: int) -> str:
        self.used.add(index)
        return self.names[index] if self.pictures.files else f"P[{index}]"

    def cue(self, value: Any, what: str, entry: bool = False) -> str:
        """A cue as the program writes it: the second it is spoken, or -- when that
        cannot be known here -- its words, for the kit to find."""
        words = str(value).strip() if value else ""
        at = second(words, self.timing, entry) if words else None
        self.moments.append((at, what, words))
        return repr(at) if at is not None else (repr(words) if words else "None")


def _picture(value: Any, writing: _Writing, where: str, required: bool = False,
             main: bool = False) -> str:
    if value is None or value == "":
        if required:
            raise ValueError(f"{where} needs a picture, and none is given")
        return "None"
    return writing.picture(_index(value, writing.pictures, where, main))


def _call(name: str, *args: str, **kwargs: str) -> str:
    return f"{name}({', '.join([*args, *(f'{k}={v}' for k, v in kwargs.items())])})"


def _places(layout: dict | None) -> dict[str, str]:
    """`layout=` for a template: where the kit put each of its parts, as numbers."""
    if not layout:
        return {}
    shown = ", ".join(f"{name!r}: ({', '.join(f'{v:g}' for v in value)})"
                      for name, value in layout.items())
    return {"layout": "{" + shown + "}"}


# What arrives first in each template, for the table of moments.
ARRIVES = {"hero": "the picture", "opener": "the picture and title", "person": "the portrait",
           "key_idea": "the idea's card", "steps": "the title", "compare": "the title",
           "flow": "the title", "hub": "the title", "timeline": "the title"}


def _shot_code(shot: dict, writing: _Writing, at: int, layout: dict | None) -> list[str]:
    template = shot.get("template")
    where = f"shot {at + 1} ({template})"
    # A scene opens on its picture at once: a first shot waiting for its words
    # left the screen blank until the narration reached "Galen".
    first = ARRIVES.get(str(template), "the shot")
    if at == 0:
        writing.moments.append((0.0, first, "at once"))
        opening = "None"
    else:
        opening = writing.cue(shot.get("when"), first, entry=True)
    title = repr(_text(shot.get("title"), f"{where} title", required=False))
    places = _places(layout)
    if template == "hero":
        index = _index(shot.get("picture"), writing.pictures, where, main=True)
        found = writing.pictures.parts.get(index, [])
        callouts = []
        for c in _items(shot.get("callouts", []), f"{where} callouts", 0, MOST_CALLOUTS):
            label = _text(c.get("label"), f"{where} callout label")
            if (len(label.split()) > MOST_CALLOUT_WORDS or label.rstrip().endswith((".", "!"))
                    or STATING.intersection(label.lower().split())):
                # "It was electrical" pointed at an engraving names nothing in it.
                raise ValueError(f"{where} callout {label!r} is a statement: a callout names "
                                 f"a part of the picture in 1 to {MOST_CALLOUT_WORDS} words "
                                 "('Frog's leg'); put a statement in a key_idea shot")
            style = str(c.get("style") or "tag").strip().lower()
            if style not in POINTING:
                raise ValueError(f"{where} callout {label!r}: style is one of "
                                 f"{', '.join(POINTING)}")
            box = region(found, str(c.get("part") or label))
            if box is not None:       # no part surely there: no pointer at all
                left, top, right, bottom = box
                callouts.append(_call(
                    "dict", label=repr(label),
                    point=f"({(left + right) / 2:.2f}, {(top + bottom) / 2:.2f})",
                    at=writing.cue(c.get("when"), f'{style} "{label}"'),
                    part=f"({left:.2f}, {top:.2f}, {right:.2f}, {bottom:.2f})",
                    style=repr(style)))
        moves = []
        for move in _items(shot.get("moves", []), f"{where} moves", 0, 3):
            through = [anchor(found, str(name)) for name in move.get("through") or []]
            if 2 <= len(through) <= 6 and all(through):
                moves.append(_call(
                    "dict", through="[" + ", ".join(f"({x:.2f}, {y:.2f})" for x, y in through)
                    + "]", at=writing.cue(move.get("when"), "a pulse along the picture")))
        extra = {"moves": f"[{', '.join(moves)}]"} if moves else {}
        return [_call("self.hero", writing.picture(index), f"[{', '.join(callouts)}]",
                      title=title, cue=opening, **extra, **places)]
    if template == "steps":
        steps = []
        for number, step in enumerate(_items(shot.get("steps"), f"{where} steps", 2, 4)):
            label = _text(step.get("label"), f"{where} step label")
            steps.append(_call("dict", label=repr(label),
                               picture=_picture(step.get("picture"), writing, where),
                               at=writing.cue(step.get("when"), f"step {number + 1}",
                                              entry=True)))
        return [_call("self.steps", f"[{', '.join(steps)}]", title=title, **places)]
    if template == "compare":
        sides = []
        for name in ("left", "right"):
            side = shot.get(name)
            if not isinstance(side, dict):
                raise ValueError(f"{where} needs '{name}'")
            points = [repr(_text(p, f"{where} {name} point"))
                      for p in (side.get("points") or [])[:3]]
            sides.append(_call(
                "dict", heading=repr(_text(side.get("heading"), f"{where} {name} heading")),
                picture=_picture(side.get("picture"), writing, where),
                points=f"[{', '.join(points)}]",
                at=writing.cue(side.get("when"), f"the {name} card", entry=True)))
        return [_call("self.compare", *sides, title=title, **places)]
    if template == "person":
        return [_call("self.person",
                      _picture(shot.get("picture"), writing, where, True, main=True),
                      repr(_text(shot.get("name"), f"{where} name")),
                      repr(_text(shot.get("line"), f"{where} line")), cue=opening,
                      line_cue=writing.cue(shot.get("line_when"), "the line", entry=True),
                      **places)]
    if template == "key_idea":
        statement = _text(shot.get("statement"), f"{where} statement")
        if len(statement.split()) > MOST_IDEA_WORDS:
            raise ValueError(f"{where} statement has {len(statement.split())} words: one "
                             f"point to remember is at most {MOST_IDEA_WORDS} -- the narration "
                             "says the rest")
        return [_call("self.key_idea", repr(statement),
                      _picture(shot.get("picture"), writing, where, main=True),
                      cue=opening, **places)]
    if template == "opener":
        lines = [_call("dict", text=repr(text), at=writing.cue(item.get("when"), f'"{text}"'))
                 for item in _items(shot.get("lines", []), f"{where} lines", 0, 3)
                 for text in [_text(item.get("text") or item.get("label"), f"{where} line")]]
        return [_call("self.opener", _picture(shot.get("picture"), writing, where, True,
                                              main=True),
                      repr(_text(shot.get("title"), f"{where} title")),
                      f"[{', '.join(lines)}]", cue=opening, **places)]
    if template in ("flow", "hub", "timeline"):
        return _diagram_code(template, shot, where, title, writing, places)
    raise ValueError(f"{where}: template must be one of {', '.join(TEMPLATES)}")


def _wait(cue: str) -> str:
    """Waiting for a moment: a second, or -- untimed here -- the words for the kit."""
    return f"self.until({cue})" if cue[:1].isdigit() else f"self._at_cue({cue})"


def _diagram_code(template: str, shot: dict, where: str, title: str, writing: _Writing,
                  places: dict[str, str]) -> list[str]:
    key = {"flow": "steps", "hub": "items", "timeline": "events"}[template]
    items = _items(shot.get(key), f"{where} {key}", 2, 6)
    labels = [_text(i.get("label"), f"{where} label") for i in items]
    whens = [writing.cue(i.get("when"), f'"{label}"', entry=True)
             for i, label in zip(items, labels, strict=True)]
    listed = f"[{', '.join(repr(label) for label in labels)}]"
    lines = []
    if title != repr(""):
        lines.append(f"self.play(self.reveal(self.title({title})))")
    if template == "flow":
        lines += [f"d = {_call('self.flow', listed, **places)}"]
        for number, when in enumerate(whens):
            lines.append(_wait(when))
            grow = f", self.grow(d.arrows[{number - 1}])" if number else ""
            lines.append(f"self.play(self.reveal(d.boxes[{number}]){grow})")
    elif template == "hub":
        centre = _text(shot.get("centre"), f"{where} centre")
        lines += [f"d = {_call('self.hub', repr(centre), listed, **places)}",
                  "self.play(self.reveal(d.centre))"]
        for number, when in enumerate(whens):
            lines += [_wait(when),
                      f"self.play(self.grow(d.lines[{number}]), self.reveal(d.items[{number}]))"]
    else:
        # The whole line, every stop faint, from the start: v8's showed one dot on an
        # empty line for most of its scene. Each stop lights on its words.
        lines += [f"d = {_call('self.timeline', listed, **places)}",
                  "[dot.set_opacity(0.3) for dot in d.dots]",
                  "self.play(self.draw(d.spine), *[FadeIn(dot) for dot in d.dots])"]
        for number, when in enumerate(whens):
            lines += [_wait(when),
                      f"self.play(d.dots[{number}].animate.set_opacity(1).scale(1.3), "
                      f"self.reveal(d.labels[{number}]))"]
    return lines


def program_for(spec: dict, pictures: int | Pictures, timing: Timing | None = None,
                layouts: list[dict] | None = None) -> str:
    """The scene program for these shots, or a ValueError saying what is wrong
    with them, for the model to correct. `pictures` is how many the brief offers, or
    a `Pictures` -- with their files, the program names them at its top. With
    `timing` every cue is written as its second; with `layouts` (the kit's
    decisions.json from a render) every place the kit chose is written too."""
    if isinstance(pictures, int):
        pictures = Pictures(pictures)
    shots = spec["shots"]
    if len(shots) > MOST_SHOTS:
        raise ValueError(f"a scene has at most {MOST_SHOTS} shots")
    writing = _Writing(pictures, timing, picture_names(pictures.files, pictures.about))
    body: list[str] = [] if pictures.files else [
        "P = self.brief.assets.pictures  # the pictures the brief offers"]
    for at, shot in enumerate(shots):
        if not isinstance(shot, dict):
            raise ValueError(f"shot {at + 1} must be an object")
        writing.moments = []
        begins = _begins(shot)
        lines = []
        if at:
            moment = writing.cue(begins, "", entry=True)
            lines += [_wait(moment) + (f'  # "{_one_line(begins, 50)}"'
                                       if moment[:1].isdigit() else ""),
                      "self.play(*[FadeOut(m) for m in self.shown], run_time=0.4)",
                      "self.clear()"]
            writing.moments = []
        layout = (layouts[at]["layout"] if layouts and at < len(layouts)
                  and layouts[at].get("call") == shot.get("template") else None)
        lines += _shot_code(shot, writing, at, layout)
        body += ["" if body else None, f"# Shot {at + 1}: {shot.get('template') or 'shot'}",
                 *_moment_table(writing.moments), *lines]
    body += ["", "self.finish()"]
    indented = "\n".join(_laid_out(line, 8) if line else ""
                         for line in body if line is not None)
    constants = "".join(
        f"{writing.names[index]} = {pictures.files[index]!r}"
        + (f"  # {_one_line(pictures.about[index], 70)}" if index < len(pictures.about)
           and pictures.about[index] else "") + "\n"
        for index in sorted(writing.used)) if pictures.files else ""
    return ("# /// script\n# requires-python = \">=3.11\"\n"
            "# dependencies = [\"manim>=0.19\", \"pillow\"]\n# ///\n"
            "# Written from the scene's shots by scene_shots.py. Edited and saved by hand,\n"
            "# it is the scene's program until the scene is made again.\n"
            "#\n"
            "# Times are seconds into the scene, the words spoken then beside them. Places\n"
            "# (`layout`) are the centre of each part in scene units -- the frame is 14.2\n"
            "# wide and 8 high, (0, 0) its middle, y upward -- and, for a picture, its width.\n"
            "# A place left out is worked out by the kit (manimkit.py).\n"
            "from manimkit import *\n\n"
            + (f"# The pictures it shows: in the scene's folder, unless a full path is given.\n"
               f"{constants}" if constants else "")
            + "\n\nclass TheScene(ExplainerScene):\n    def construct(self):\n"
            f"{indented}\n\n\nrun(TheScene)\n")


def _moment_table(moments: list[tuple[float | None, str, str]]) -> list[str]:
    """`#   12.40 s  tag "Cortex"   "the outer layer"` for each moment of a shot."""
    ordered = sorted(moments, key=lambda m: (m[0] is None, m[0] or 0.0))
    return [f"#   {'' if at is None else f'{at:.2f} s':>8}  {what:<28} "
            + (f'"{_one_line(words, 48)}"' if words and words != "at once" else words)
            for at, what, words in ordered]
