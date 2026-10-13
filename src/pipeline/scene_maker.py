"""Making one scene: write it, render it, review it, fix it -- and nothing else.

    write the program  ->  render + fixed checks  ->  review its frames  ->  edit it
          ^                                                                    |
          +--------------------------------------------------------------------+

Each round is one model call, asked afresh: the model is given the scene's brief,
the file as it is now and what the last render found -- not a conversation to
remember. It answers with a few-line edit, or the whole file, as long as it needs.

At most `MOST_ROUNDS` renders. The scene is done when every check passes and the
reviewer calls it good, or has nothing it must fix (polish alone does not earn a
round). Until then it is refined, and a refinement is kept only when it is
better: after a pass, by the reviewer's judgement, not merely by being newer.

A scene always ends with a clip. The best version so far is kept (`scene_kept`):
a round that comes out worse is undone back to it, and the model is told what its
change broke. When the rounds run out, the scene keeps that best version, with
any failing checks named for the person to judge. If no round drew anything --
every program crashed, or the model could not be reached -- a plain stand-in is
drawn without a model (`scene_fallback`).

An answer that cannot be used (an edit whose lines are not in the file, a cut-off
reply) is asked again at once, without spending a render.

Earlier scenes of the video are summarised in a line each, so a later scene
stays consistent with them; the slide's pictures are described once and kept.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from pipeline import project_work
from pipeline.core import require_project
from pipeline.generation import VisualPlanStore
from pipeline.llm import ModelCallFailed, ModelNotConfigured, ModelOutputTruncated
from pipeline.scene_edit import apply_edits, parse_answer
from pipeline.scene_illustration import paint as paint_illustration
from pipeline.scene_illustration import wanted as wanted_illustration
from pipeline.scene_kept import (
    adopt,
    drop_kept,
    failing_checks,
    has_clip,
    keep_best,
    passes_as_written,
    rank,
    restore_best,
)
from pipeline.scene_lab import _visual, run_scene, scene_folder, write_brief
from pipeline.scene_program import ENTRY_FILES, entry_of
from pipeline.scene_prompt import (  # noqa: F401 -- kit_api, compact: read through here
    available_renderers,
    compact,
    earlier_scenes,
    kit_api,
    picture_notes,
    request,
    system_prompt,
)
from pipeline.scene_round import render_round
from pipeline.scene_state import STOP, add_event, doing, load_state, save_state

logger = logging.getLogger(__name__)

MOST_ROUNDS = 6           # refining until the reviewer calls it good takes rounds
ASKS_PER_ROUND = 3        # an unusable answer is asked again, without a render
# As long as the model will write: 65,536 tokens is what the provider accepts.
ROUND_TOKENS = 65536
CALL_RETRIES = 3          # a failed model call is tried again, waiting longer each time
RETRY_WAIT_SECONDS = 20


# --- the loop --------------------------------------------------------------------------------


class _GaveUp(Exception):
    """The model cannot be reached: the scene stops, and says why."""


def _ask(system: str, user: str, folder: Path, state: dict[str, Any]) -> str | None:
    """One model call, waited out through a blip. None if the answer was cut off."""
    from pipeline.llm import complete_scene

    for attempt in range(1, CALL_RETRIES + 2):
        try:
            text, used = complete_scene(system, user, max_tokens=ROUND_TOKENS)
        except ModelOutputTruncated:
            return None
        except ModelNotConfigured as failure:
            raise _GaveUp(str(failure)) from failure
        except ModelCallFailed as failure:
            if attempt > CALL_RETRIES:
                raise _GaveUp(str(failure)) from failure
            add_event(state, "retry", f"The model could not answer ({failure}); trying again.")
            save_state(folder, state)
            time.sleep(RETRY_WAIT_SECONDS * attempt)
            continue
        state["calls"]["agent"] += 1
        state["tokens"]["prompt"] += used["prompt"]
        state["tokens"]["completion"] += used["completion"]
        return text
    return None


def make_scene(slug: str, visual_id: str, *, instruction: str = "",
               fresh: bool = False) -> None:
    """Make (or change) one scene until it is good, or the rounds are used."""
    with project_work.working_on(slug):
        _make_scene(slug, visual_id, instruction, fresh)


def _make_scene(slug: str, visual_id: str, instruction: str, fresh: bool) -> None:
    project = require_project(slug)
    visual = _visual(VisualPlanStore(project.root).load(), visual_id)
    folder = scene_folder(project, visual, create=True)
    (folder / STOP).unlink(missing_ok=True)
    state = load_state(folder)
    state.update(status="working", error="", summary="", remarks=[], renders=0,
                 calls={"agent": 0, "vision": 0}, tokens={"prompt": 0, "completion": 0},
                 last_render=None)
    add_event(state, "start", instruction or ("Started again." if fresh else "Started."))

    renderers = available_renderers()
    brief = write_brief(project, visual)
    # Painted once, before the first round, when the script asked for a picture
    # no slide has; the brief then offers it first.
    if wanted_illustration(brief["on_screen"]):
        doing(folder, state, "Painting the scene's illustration")
        if paint_illustration(folder, brief["on_screen"], brief["look"], state,
                              brief["narration"]):
            brief = write_brief(project, visual)
    renderer, entry = entry_of(folder)
    code = "" if fresh or not (folder / entry).exists() else \
        (folder / entry).read_text(encoding="utf-8")
    spec = {} if not code else _spec_of(folder)
    # The best version so far. The scene as it is now counts, when it has a clip
    # made for this brief: a change asked for must not lose it.
    best = None
    drop_kept(folder)
    if code and passes_as_written(project, visual) and has_clip(folder):
        failing = [c["name"] for c in failing_checks(folder)]
        keep_best(folder)
        best = {"rank": rank(not failing, failing), "spec": dict(spec), "entry": entry,
                "renderer": renderer, "feedback": "",
                "last_render": {"passed": not failing, "good": False, "reviewed": False,
                                "failing": failing, "problems": [], "polish": []}}
    try:
        doing(folder, state, "Looking at the slide's pictures")
        notes = picture_notes(brief, folder.parent, state)
        system = system_prompt(project, renderers)
        earlier = earlier_scenes(project, visual)
        feedback = ""

        for number in range(1, MOST_ROUNDS + 1):
            if project_work.stopped():
                return           # the project is being deleted: touch nothing more
            if (folder / STOP).exists():
                state["status"] = "stopped"
                add_event(state, "stopped", "Stopped by the person.")
                break
            doing(folder, state, f"{'Fixing' if code else 'Writing'} the scene "
                  f"(round {number} of up to {MOST_ROUNDS})")
            written = _written(system, brief, notes, earlier, entry, code, feedback,
                               instruction if number == 1 else "", renderers, spec,
                               folder, state)
            if project_work.stopped():
                return
            if written is None:
                continue                      # nothing usable after asking again
            code, spec, renderer, entry, rewrote = written
            (folder / entry).write_text(code, encoding="utf-8")
            add_event(state, "write", f"{'Rewrote' if rewrote else 'Edited'} {entry} "
                      f"({renderer}): {spec.get('approach', '')}")

            doing(folder, state, f"Rendering with {renderer}, checking, reviewing the frames")
            result = render_round(slug, visual_id, folder, renderer, spec, state)
            if project_work.stopped():
                return
            state["last_render"] = {k: result[k] for k in
                                    ("passed", "good", "reviewed", "failing", "problems",
                                     "polish")}
            feedback = result["feedback"]
            add_event(state, "render", f"Round {number}: " + (
                "good" if result["good"] else "passed its checks" if result["passed"]
                else f"{len(result['failing'])} check(s) fail: " + "; ".join(result["failing"])))
            # Done when the reviewer calls it good. A pass with nothing it MUST change
            # ends it too: polish alone does not earn another round.
            if result["good"] or (result["passed"] and not result["problems"]):
                best = None                   # this one is the scene: nothing to go back to
                break

            # Otherwise it is refined, and a refinement is kept only when it is better:
            # after a pass, the reviewer is the judge of better.
            this = (rank(result["passed"], result["failing"], result["good"],
                         len(result["problems"])) if has_clip(folder) else None)
            if this is not None and (best is None or this > best["rank"]
                                     or (this == best["rank"] and not result["passed"])):
                keep_best(folder)
                if not result["passed"]:
                    adopt(slug, visual_id)
                best = {"rank": this, "spec": dict(spec), "entry": entry,
                        "renderer": renderer, "feedback": feedback,
                        "last_render": state["last_render"]}
            elif best is not None:
                code, spec = restore_best(slug, visual_id), dict(best["spec"])
                entry, renderer = best["entry"], best["renderer"]
                state["last_render"] = best["last_render"]
                feedback = (
                    f"Your last change did not make it better:\n{feedback}\n\nIt was undone: "
                    "the file below is the best version so far. "
                    + (f"What it still needs:\n{best['feedback']}\n" if best["feedback"]
                       else "")
                    + "Make that change another way, without breaking what works.")
                add_event(state, "note", f"Round {number} was no better ("
                          + (", ".join(result["failing"]) or "the reviewer's view")
                          + "); back to the best version.")
    except _GaveUp as failure:
        add_event(state, "note", f"The model could not be reached: {failure}")
        state["error"] = str(failure)
    if state["status"] != "stopped" and not (state.get("last_render") or {}).get("passed") \
            and best is None and not has_clip(folder):
        _stand_in(slug, visual_id, folder, brief, state)
    elif best is not None and best["rank"][0] == 0:
        adopt(slug, visual_id)                # the best one made, with its problems named
    _conclude(state, spec, has_clip(folder))
    save_state(folder, state)


def _written(system, brief, notes, earlier, entry, code, feedback, instruction, renderers,
             spec, folder, state):
    """The program the model writes this round, asked again at once when its answer
    cannot be used -- an edit that matches nothing is not worth a render. None if no
    answer could be used."""
    # What the last render found stays in every ask: a re-ask that said only "your
    # answer could not be used" had the model fix the format and forget the scene.
    found, note = feedback, ""
    for _ in range(ASKS_PER_ROUND):
        feedback = "\n\n".join(part for part in (note, found) if part)
        text = _ask(system, request(brief, notes, earlier, entry, code, feedback,
                                    instruction, renderers), folder, state)
        if text is None:
            note = ("Your last answer was cut off at the length limit. Send the "
                    "complete file, written more compactly.")
            add_event(state, "note", "Its answer was cut off; asking again.")
            continue
        try:
            answer = parse_answer(text)
            merged = {**spec, **answer.spec}
            renderer = str(merged.get("renderer", "")).strip().lower()
            if renderer not in renderers:
                raise ValueError(f"the renderer must be one of {', '.join(renderers)}"
                                 + (f", not {renderer!r}" if renderer else ""))
            written = answer.code if answer.code else apply_edits(code, answer.edits)
        except ValueError as unusable:
            note = (f"Your last answer could not be used: {unusable}. Send the "
                    "complete file this time, in the fenced blocks described below.")
            add_event(state, "note", f"Its answer could not be used ({unusable}); asking "
                      "again for the whole file.")
            continue
        return written, merged, renderer, ENTRY_FILES[renderer], bool(answer.code)
    return None


def _stand_in(slug: str, visual_id: str, folder: Path, brief: dict[str, Any],
              state: dict[str, Any]) -> None:
    """No round drew anything: draw the plain stand-in, without a model."""
    from pipeline.scene_fallback import FALLBACK_NOTE, fallback_program
    from pipeline.scene_program import save_spec

    doing(folder, state, "Drawing a plain stand-in")
    spec = {"renderer": "manim", "approach": FALLBACK_NOTE}
    (folder / "scene.py").write_text(fallback_program(brief, folder), encoding="utf-8")
    save_spec(folder, spec | {"entry": "scene.py"})
    state["renders"] += 1
    run_scene(slug, visual_id)
    failing = [c["name"] for c in failing_checks(folder)]
    if has_clip(folder):
        adopt(slug, visual_id)
    state["last_render"] = {"passed": not failing, "good": False, "reviewed": False,
                            "failing": failing, "problems": [], "polish": []}
    add_event(state, "note", "No round drew a clip, so a plain stand-in was drawn: "
              + FALLBACK_NOTE)


def _spec_of(folder: Path) -> dict[str, Any]:
    from pipeline.storage.documents import read_json_object

    return read_json_object(folder / "spec.json", "scene spec") or {}


def _conclude(state: dict[str, Any], spec: dict[str, Any], clip: bool = True) -> None:
    """How the making ended, in plain words. Nothing is asked, and a scene is
    always made: with every check passing, or with the failing ones named."""
    if state["status"] == "stopped":
        return
    last = state["last_render"] or {}
    failing = last.get("failing") or []
    if not clip:
        # Not even the stand-in drew anything: there is no scene to call done.
        state.update(status="failed", failing=failing, error=state.get("error") or (
            "No clip could be made" + (f": {', '.join(failing)}." if failing else ".")))
        add_event(state, "failed", state["error"])
        return
    state.update(status="done", summary=str(spec.get("approach", "")),
                 remarks=(last.get("problems") or []) + (last.get("polish") or []),
                 failing=failing)
    if not failing:
        add_event(state, "done", "Every check passed"
                  + ("." if last.get("good") else "; the reviewer still has remarks."))
    else:
        add_event(state, "done", f"Made, with {len(failing)} check(s) failing: "
                  f"{', '.join(failing)}. Watch it: approve it as it is, or say what to "
                  "change.")
