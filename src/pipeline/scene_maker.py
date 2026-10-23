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

import json
import logging
from pathlib import Path
from typing import Any

from pipeline import project_work
from pipeline.core import require_project
from pipeline.generation import VisualPlanStore
from pipeline.llm import ModelCallFailed, ModelNotConfigured, ModelOutputTruncated
from pipeline.scene_backgrounds import choose as choose_background
from pipeline.scene_edit import apply_edits, parse_answer
from pipeline.scene_kept import (
    adopt,
    drop_kept,
    failing_checks,
    has_clip,
    keep_best,
    mark_below_bar,
    passes_as_written,
    rank,
    restore_best,
)
from pipeline.scene_lab import _visual, run_scene, scene_folder, write_brief
from pipeline.scene_pictures import PAINTED, paint_asked
from pipeline.scene_pictures import prepare as prepare_pictures
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
from pipeline.scene_shots import Pictures, is_shots, program_for, uncovered, unheard
from pipeline.scene_state import STOP, add_event, doing, load_state, save_state

logger = logging.getLogger(__name__)

MOST_ROUNDS = 6           # refining until the reviewer calls it good takes rounds
# A scene stops when two rounds in a row do not beat its best: a ladder of 14 rounds made
# the kept version in 2 Chapter 1 scenes of 21. It starts over only when far off.
STALLED_ROUNDS = 2
FAR_SCORE = 2.0
ESCALATIONS = ("fresh",)
ESCALATION_ROUNDS = 4
ESCALATION_NOTE = (
    "The rounds so far did not reach the bar, so this is a fresh start, not a fix: "
    "write a new program that shows the idea with a different shot -- a different "
    "composition, a different way of moving, another picture of the mechanism. Do not "
    "rebuild the last version.")
# Written by hand and failing the checks twice, a scene is answered with shots (which pass
# them by construction): 9 of 11 Chapter 1 scenes that ended failing were hand-written.
HAND_FAILURES = 2
SHOTS_ONLY = ("Programs written by hand failed the checks twice here: answer with shots only "
              "now, no code -- the shots that teach the idea best; the brief is direction.")
ASKS_PER_ROUND = 3        # an unusable answer is asked again, without a render
SEND_IT = ("Now send it, exactly as the answer format says: the ```json block with the "
           "shots -- or, only if no shot can show the idea, the json block and the "
           "complete file. No plan and no explanation outside the blocks.")
ROUND_TOKENS = 65536      # as long as the model will write: what the provider accepts
CALL_ATTEMPTS = 6         # a failed model call is tried again, waiting longer each time
MODEL_GIVE_UP_SECONDS = 1800


# --- the loop --------------------------------------------------------------------------------


class _GaveUp(Exception):
    """The model cannot be reached: the scene stops, and says why."""


def _ask(system: str, user: str, folder: Path, state: dict[str, Any],
         then: tuple = ()) -> str | None:
    """One model call, waited out through a blip (resilience.py: jittered backoff,
    the provider's Retry-After, a circuit shared by every process; up to half an
    hour before the scene stops). None if the answer was cut off."""
    from pipeline.llm import complete_scene
    from pipeline.resilience import ServiceUnavailable, call

    def attempt() -> tuple[str, dict[str, int]]:
        return complete_scene(system, user, max_tokens=ROUND_TOKENS, then=then)

    def said(failure: BaseException, pause: float) -> None:
        add_event(state, "retry", f"The model could not answer ({failure}); trying again "
                  f"in {pause:.0f} s.")
        save_state(folder, state)

    try:
        text, used = call("model", attempt, attempts=CALL_ATTEMPTS, base_seconds=10,
                          longest_wait=300, give_up_after=MODEL_GIVE_UP_SECONDS,
                          on_retry=said)
    except ModelOutputTruncated:
        return None
    except (ModelNotConfigured, ModelCallFailed, ServiceUnavailable) as failure:
        raise _GaveUp(str(failure)) from failure
    state["calls"]["agent"] += 1
    state["tokens"]["prompt"] += used["prompt"]
    state["tokens"]["completion"] += used["completion"]
    return text


def make_scene(slug: str, visual_id: str, *, instruction: str = "",
               fresh: bool = False) -> None:
    """Make (or change) one scene until it is good, or the rounds are used."""
    with project_work.working_on(slug):
        _make_scene(slug, visual_id, instruction, fresh)


def _make_scene(slug: str, visual_id: str, instruction: str, fresh: bool) -> None:
    from pipeline.storyboard import note_for

    project = require_project(slug)
    visual = _visual(VisualPlanStore(project.root).load(), visual_id)
    instruction = instruction or note_for(project, visual_id)   # the storyboard card's note
    folder = scene_folder(project, visual, create=True)
    (folder / STOP).unlink(missing_ok=True)
    state = load_state(folder)
    state.update(status="working", error="", summary="", remarks=[], renders=0,
                 calls={"agent": 0, "vision": 0}, tokens={"prompt": 0, "completion": 0},
                 last_render=None)
    add_event(state, "start", instruction or ("Started again." if fresh else "Started."))

    renderers = available_renderers()
    brief = write_brief(project, visual)
    # Made once, before the first round: a painting (checked) or icons the script asked for.
    doing(folder, state, "Making the pictures the deck does not have")
    brief = prepare_pictures(project, visual, brief, state)
    renderer, entry = entry_of(folder)
    code = "" if fresh or not (folder / entry).exists() else \
        (folder / entry).read_text(encoding="utf-8")
    spec = {} if not code else _spec_of(folder)
    # The best so far: the scene as it is counts, when its clip was made for this brief.
    best = None
    drop_kept(folder)
    if code and passes_as_written(project, visual) and has_clip(folder):
        failing = [c["name"] for c in failing_checks(folder)]
        keep_best(folder)
        best = {"rank": rank(not failing, failing), "spec": dict(spec), "entry": entry,
                "renderer": renderer, "feedback": "",
                "last_render": {"passed": not failing, "good": False, "reviewed": False,
                                "failing": failing, "problems": [], "polish": []}}
    met, climbed, best_on_disk, stalled = False, 0, True, 0
    hand_failed, shots_only = 0, False
    try:
        doing(folder, state, "Looking at the slide's pictures")
        notes, parts = picture_notes(brief, folder.parent, state)
        system = system_prompt(project, renderers)
        earlier = earlier_scenes(project, visual)
        feedback = ""

        number, rounds = 0, MOST_ROUNDS
        while True:
            number += 1
            if project_work.stopped():
                return           # the project is being deleted: touch nothing more
            if (folder / STOP).exists():
                state["status"] = "stopped"
                add_event(state, "stopped", "Stopped by the person.")
                break
            if number > rounds:
                near = best is not None and best["rank"][0] == 1 and best["rank"][2] >= FAR_SCORE
                if climbed == len(ESCALATIONS) or near:
                    break                     # no better to be had this way: the best is used
                # Far off the bar: not more of the same, a different approach.
                climbed, rounds, stalled = climbed + 1, number - 1 + ESCALATION_ROUNDS, 0
                still = (best or {}).get("feedback") or feedback
                code, spec = "", {}
                feedback = ESCALATION_NOTE + (f"\nWhat the best version still needed:\n"
                                              f"{still}" if still else "")
                add_event(state, "escalate", f"Still far off the bar after {number - 1} rounds: "
                          f"starting over with a different shot ({ESCALATION_ROUNDS} more "
                          "rounds).")
            doing(folder, state, f"{'Fixing' if code else 'Writing'} the scene "
                  f"(round {number} of up to {rounds})")
            written = _written(system, brief, notes, earlier, entry, code, feedback,
                               instruction if number == 1 else "", renderers, spec,
                               folder, state, parts, shots_only)
            if project_work.stopped():
                return
            if written is None:
                continue                      # nothing usable after asking again
            code, spec, renderer, entry, rewrote = written
            painted = paint_asked(project, visual, folder, spec, brief, state)
            if painted is not None:           # asked for a picture: answered with it
                brief, (notes, parts) = painted, picture_notes(painted, folder.parent, state)
                code, spec, feedback = "", {}, PAINTED
                continue
            brief = choose_background(project, visual, folder, spec, brief, state) or brief
            (folder / entry).write_text(code, encoding="utf-8")
            add_event(state, "write", f"{'Rewrote' if rewrote else 'Edited'} {entry} "
                      f"({renderer}): {spec.get('approach', '')}")

            doing(folder, state, f"Rendering with {renderer}, checking, reviewing the frames")
            result = render_round(slug, visual_id, folder, renderer, spec, state, brief)
            if project_work.stopped():
                return
            state["last_render"] = {k: result[k] for k in
                                    ("passed", "good", "reviewed", "failing", "problems",
                                     "polish", "scores", "score")}
            feedback = "\n\n".join(part for part in (
                result["feedback"], _still_stretch(folder, brief, spec)) if part)
            if not result["passed"] and not is_shots(spec):
                hand_failed += 1
                if hand_failed >= HAND_FAILURES and not shots_only:
                    shots_only = True
                    add_event(state, "note", "Written by hand, it failed the checks twice: "
                              "from now on it is answered with shots.")
            if shots_only:
                feedback = SHOTS_ONLY + "\n\n" + feedback
            add_event(state, "render", f"Round {number}: " + (
                "good" if result["good"] else "passed its checks" if result["passed"]
                else f"{len(result['failing'])} check(s) fail: " + "; ".join(result["failing"])))
            # Done when the reviewer calls it good. A pass with nothing it MUST change
            # ends it too: polish alone does not earn another round.
            if result["good"] or (result["passed"] and not result["problems"]):
                best, met = None, True        # this one is the scene: nothing to go back to
                break

            # Otherwise it is refined, and a refinement is kept only when it is better:
            # after a pass, the reviewer is the judge of better.
            this = (rank(result["passed"], result["failing"], result["good"],
                         len(result["problems"]), result["score"])
                    if has_clip(folder) else None)
            if this is not None and (best is None or this > best["rank"]
                                     or (this == best["rank"] and not result["passed"])):
                keep_best(folder)
                if not result["passed"]:
                    adopt(slug, visual_id)
                best = {"rank": this, "spec": dict(spec), "entry": entry,
                        "renderer": renderer, "feedback": feedback,
                        "last_render": state["last_render"]}
                best_on_disk, stalled = True, 0
                continue
            # Not better than the best. Twice in a row, once the best passes its checks,
            # and this approach is spent: more rounds of it were thrown away.
            stalled += 1
            if best is not None and best["rank"][0] == 1 and stalled >= STALLED_ROUNDS:
                rounds = number
            if best is not None and climbed:
                # A fresh approach is refined on its own terms, not undone back to the
                # old one; the best stays kept and comes back if nothing beats it.
                best_on_disk = False
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
    if best is not None and not best_on_disk:
        code, spec = restore_best(slug, visual_id), dict(best["spec"])
        state["last_render"] = best["last_render"]
        add_event(state, "note", "Nothing after it beat the best version; it is back.")
    stood_in = False
    if state["status"] != "stopped" and not (state.get("last_render") or {}).get("passed") \
            and best is None and not has_clip(folder):
        _stand_in(slug, visual_id, folder, brief, state)
        stood_in = True
    elif best is not None and best["rank"][0] == 0:
        adopt(slug, visual_id)                # the best one made, with its problems named
    _conclude(state, spec, has_clip(folder))
    if not met and state["status"] == "done":
        why = _below_bar(state, stood_in)
        mark_below_bar(slug, visual_id, why)
        state["below_bar"] = why
        add_event(state, "note", f"Used below the quality bar: {why}")
    save_state(folder, state)


def _below_bar(state: dict[str, Any], stood_in: bool) -> str:
    """What the scene still lacks, in a line, for the person deciding on it."""
    if stood_in:
        return "no round drew a clip, so it is a plain stand-in."
    last = state.get("last_render") or {}
    failing, problems = last.get("failing") or [], last.get("problems") or []
    if failing:
        return f"{len(failing)} check(s) still fail: {', '.join(failing)}."
    if problems:
        return "the reviewer still wants: " + "; ".join(str(p) for p in problems[:3]) + "."
    return "the reviewer did not call it good."


def _written(system, brief, notes, earlier, entry, code, feedback, instruction, renderers,
             spec, folder, state, parts=None, shots_only=False):
    """The program the model writes this round, asked again at once when its answer
    cannot be used -- an edit that matches nothing is not worth a render. None if no
    answer could be used."""
    # What the last render found stays in every ask (a bare re-ask forgot the scene).
    found, note, then = feedback, "", ()
    for _ in range(ASKS_PER_ROUND):
        feedback = "\n\n".join(part for part in (note, found) if part)
        text = _ask(system, request(brief, notes, earlier, entry, code, feedback,
                                    instruction, renderers, spec.get("shots")), folder, state,
                    then)
        then = ()
        if text is None:
            note = ("Your last answer was cut off at the length limit. Send the "
                    "complete file, written more compactly.")
            add_event(state, "note", "Its answer was cut off; asking again.")
            continue
        try:
            answer = parse_answer(text)
            merged = {**spec, **answer.spec}
            if not answer.code and not answer.edits and is_shots(answer.spec):
                missing = unheard(answer.spec, brief.get("words") or [], brief["narration"])
                if missing:
                    raise ValueError(
                        "these \"when\"s are not words the narration says, so they cannot "
                        "be timed: " + "; ".join(f'"{cue}"' for cue in missing[:5])
                        + ". Copy each one exactly from the narration's words.")
                # The shots, as data: the program is written from them (scene_shots).
                renderer = "manim"
                merged = {**merged, "renderer": renderer}
                pictures = Pictures(
                    len((brief.get("assets") or {}).get("pictures") or []), parts or {},
                    frozenset(e["index"] for e in brief.get("picture_catalogue") or []
                              if e.get("main_of")))
                return (program_for(answer.spec, pictures), merged, renderer,
                        ENTRY_FILES[renderer], True)
            if shots_only:
                raise ValueError(SHOTS_ONLY)
            renderer = str(merged.get("renderer", "")).strip().lower()
            if renderer not in renderers:
                raise ValueError(f"the renderer must be one of {', '.join(renderers)}"
                                 + (f", not {renderer!r}" if renderer else ""))
            written = answer.code if answer.code else apply_edits(code, answer.edits)
        except ValueError as unusable:
            if "```" not in text:
                # Most unusable answers were a plan with nothing after it: the model
                # is asked, in the same conversation, for what it planned.
                then = ({"role": "assistant", "content": text},
                        {"role": "user", "content": SEND_IT})
                note = ""
                add_event(state, "note", "Its answer was a plan with no shots or file; "
                          "asked for them.")
                continue
            note = (f"Your last answer could not be used: {unusable}. Correct it and send "
                    "it again, in the fenced blocks described below.")
            add_event(state, "note", f"Its answer could not be used ({unusable}); asking "
                      "again for the whole file.")
            continue
        return written, merged, renderer, ENTRY_FILES[renderer], bool(answer.code)
    return None


def _still_stretch(folder: Path, brief: dict[str, Any], spec: dict[str, Any]) -> str:
    """For shots: the narration a long still stretch leaves unshown, quoted."""
    timings = folder / "narration.mp3.words.json"
    if not is_shots(spec) or not timings.exists():
        return ""
    try:
        words = json.loads(timings.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    return uncovered(spec, words, float(brief.get("seconds") or 0))


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
