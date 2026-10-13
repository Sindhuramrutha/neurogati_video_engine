"""A scene is made by a short loop: write the program, render it, check and review
it, then fix a few lines (or the whole file). It finishes, or fails with a reason;
it never stops to ask."""

# ruff: noqa: F811
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

from pipeline import scene_agent, scene_maker
from pipeline.generation import VisualPlanStore
from pipeline.llm import ModelCallFailed, ModelOutputTruncated
from pipeline.scene_agent import agent_view
from pipeline.scene_checks import motion_check
from pipeline.scene_edit import apply_edits, parse_answer
from pipeline.scene_lab import scene_folder
from pipeline.scene_maker import make_scene
from pipeline.scene_review import Scores, Verdict
from tests.test_scene_lab import CRASHES, GOOD, project_root, scripted_project  # noqa: F401

pytestmark = pytest.mark.skipif(
    not (shutil.which("ffmpeg") and shutil.which("ffprobe")), reason="needs ffmpeg")

def scored(*, low: int = 5, **lines) -> Scores:
    """Every rubric line at `low`, with any named line set on its own."""
    return Scores(**(dict.fromkeys(Scores.model_fields, low) | lines))


GOOD_VERDICT = Verdict(scores=scored(), teaches=True, motion_explains=True, looks_finished=True)
BAD_VERDICT = Verdict(scores=scored(low=4, motion=2), teaches=True, motion_explains=False,
                      looks_finished=True, problems=["Labels only fade in and out."],
                      polish=["Larger title."])
SPEC = '```json\n{"renderer": "pillow", "approach": "A bar grows under the word touch."}\n```\n'


def whole(code):
    return SPEC + "```python\n" + code.strip("\n") + "\n```"


def edit(search, replace):
    return ("```edit\n<<<<<<< SEARCH\n" + search + "\n=======\n" + replace
            + "\n>>>>>>> REPLACE\n```")


class Model:
    """Answers each round from a list, and keeps the requests it was sent."""

    def __init__(self, *answers):
        self.answers, self.requests = list(answers), []

    def __call__(self, system_prompt, user_prompt, **kwargs):
        self.requests.append(user_prompt)
        answer = self.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer, {"prompt": 100, "completion": 20, "reasoning": 0}


def wired(monkeypatch, model, *verdicts):
    monkeypatch.setattr("pipeline.llm.complete_scene", model)
    queue = list(verdicts)
    monkeypatch.setattr("pipeline.scene_review.review_frames",
                        lambda folder, brief, question="": queue.pop(0))
    monkeypatch.setattr("pipeline.scene_review.look_at_picture",
                        lambda path, question: "a figure")
    monkeypatch.setattr(scene_maker, "RETRY_WAIT_SECONDS", 0)


# --- the loop ----------------------------------------------------------------------------


def test_a_scene_is_written_rendered_reviewed_and_done(project_root, monkeypatch):
    slug, project, visual = scripted_project("Loop")
    wired(monkeypatch, Model(whole(GOOD)), GOOD_VERDICT)

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert view["status"] == "done" and view["renders"] == 1 and view["calls"]["agent"] == 1
    assert view["summary"] == "A bar grows under the word touch."
    assert view["last_render"]["good"] and not view["remarks"]
    assert "question" not in view, "nothing waits on an answer"


def test_a_crash_is_fixed_with_a_few_line_edit(project_root, monkeypatch):
    slug, project, visual = scripted_project("Edit")
    model = Model(whole(CRASHES), edit(CRASHES.strip(), GOOD.strip("\n")))
    wired(monkeypatch, model, GOOD_VERDICT)

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert view["status"] == "done" and view["renders"] == 2
    assert "These checks FAIL" in model.requests[1] and "the scene went wrong" in model.requests[1]
    assert "```\nraise RuntimeError" in model.requests[1], "it is shown the file as it is"
    written = (scene_folder(project, visual) / "scene.py").read_text(encoding="utf-8")
    assert "RuntimeError" not in written and "Touch" in written, "the edit was applied"


def test_the_reviewers_notes_come_back_as_must_fix_and_polish(project_root, monkeypatch):
    slug, project, visual = scripted_project("Review")
    model = Model(whole(GOOD), whole(GOOD))
    wired(monkeypatch, model, BAD_VERDICT, GOOD_VERDICT)

    make_scene(slug, visual.id)

    assert "MUST FIX: Labels only fade in and out." in model.requests[1]
    assert "optional polish: Larger title." in model.requests[1]
    assert agent_view(slug, visual.id)["renders"] == 2


def test_out_of_rounds_with_passing_checks_it_is_made_with_the_remarks(project_root,
                                                                       monkeypatch):
    slug, project, visual = scripted_project("Remarks")
    monkeypatch.setattr(scene_maker, "MOST_ROUNDS", 2)
    wired(monkeypatch, Model(whole(GOOD), whole(GOOD)), BAD_VERDICT, BAD_VERDICT)

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert view["status"] == "done", "the clip passed every check"
    assert "Labels only fade in and out." in view["remarks"], "what is left is reported"


def test_out_of_rounds_with_nothing_drawn_a_plain_stand_in_is_made_and_nothing_asked(
        project_root, monkeypatch):
    slug, project, visual = scripted_project("Fails")
    monkeypatch.setattr(scene_maker, "MOST_ROUNDS", 2)
    wired(monkeypatch, Model(whole(CRASHES), whole(CRASHES)))

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert view["status"] == "done", "a scene always ends with a clip"
    assert any("plain stand-in" in e["text"] for e in view["events"])
    assert any("The program ran" in e["text"] for e in view["events"] if e["kind"] == "render")
    assert "question" not in view


def test_with_no_clip_at_all_the_scene_is_failed_not_done(project_root, monkeypatch):
    """The stand-in can fail too. A scene with nothing to show is not "done"."""
    slug, project, visual = scripted_project("No clip")
    monkeypatch.setattr(scene_maker, "MOST_ROUNDS", 2)
    monkeypatch.setattr(scene_maker, "_stand_in", lambda *args: None)
    wired(monkeypatch, Model(whole(CRASHES), whole(CRASHES)))

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert view["status"] == "failed" and "The program ran" in view["error"]


def test_a_pass_with_only_polish_left_ends_the_scene(project_root, monkeypatch):
    """Rounds spent on polish broke scenes that already worked: a pass is the end
    unless the reviewer names something that must change."""
    slug, project, visual = scripted_project("Polish")
    polish_only = Verdict(scores=scored(low=4, finish=3), teaches=True, motion_explains=True,
                          looks_finished=False, polish=["A warmer accent."])
    model = Model(whole(GOOD), whole(GOOD))
    wired(monkeypatch, model, polish_only)

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert view["status"] == "done" and view["renders"] == 1 and len(model.requests) == 1
    assert "A warmer accent." in view["remarks"]


def test_an_unusable_answer_is_asked_again_with_what_the_render_found(project_root,
                                                                      monkeypatch):
    """A re-ask that said only "your answer could not be used" had the model fix
    its format and forget what was wrong with the scene."""
    slug, project, visual = scripted_project("Re-ask")
    only_a_plan = '```json\n{"renderer": "pillow", "approach": "A bar."}\n```'
    model = Model(whole(CRASHES), only_a_plan, whole(GOOD))
    wired(monkeypatch, model, GOOD_VERDICT)

    make_scene(slug, visual.id)

    asked_again = model.requests[2]
    assert "could not be used" in asked_again
    assert "These checks FAIL" in asked_again and "the scene went wrong" in asked_again
    assert agent_view(slug, visual.id)["renders"] == 2, "the unusable answer cost no render"


def test_a_change_that_breaks_a_passing_scene_is_undone_and_it_ends_made(project_root,
                                                                         monkeypatch):
    """Scene 002 of a real run passed in round 4, broke in round 5, and the passing
    clip was gone. Once a version passes, nothing worse replaces it."""
    slug, project, visual = scripted_project("Kept")
    monkeypatch.setattr(scene_maker, "MOST_ROUNDS", 3)
    model = Model(whole(GOOD), whole(CRASHES), whole(CRASHES))
    wired(monkeypatch, model, BAD_VERDICT)

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert view["status"] == "done", "the version that passed is what is left"
    folder = scene_folder(project, visual)
    assert "RuntimeError" not in (folder / "scene.py").read_text(encoding="utf-8")
    assert (folder / "render.mp4").exists() and (folder / "preview.mp4").exists()
    recorded = next(v for v in VisualPlanStore(project.root).load().visuals if v.id == visual.id)
    assert recorded.clip_path, "the clip is the scene's again"
    assert len(model.requests) == 3, "it keeps refining while the reviewer has a must-fix"
    assert "MUST FIX: Labels only fade in and out." in model.requests[1]
    told = model.requests[2]
    assert "did not make it better" in told and "The program ran" in told
    assert "MUST FIX: Labels only fade in and out." in told, "still asked for it"
    assert "```\nraise RuntimeError" not in told, "shown the kept file"
    assert any("back to the best version" in e["text"] for e in view["events"])


def test_a_refinement_the_reviewer_likes_less_does_not_replace_the_kept_one(project_root,
                                                                           monkeypatch):
    """Two passing versions used to tie, and the newer always won: round 4 of a
    real scene replaced one the reviewer had fewer complaints about."""
    slug, project, visual = scripted_project("Liked less")
    monkeypatch.setattr(scene_maker, "MOST_ROUNDS", 3)
    worse = Verdict(scores=scored(low=3, illustration=1, motion=1), teaches=False,
                    motion_explains=False, looks_finished=True,
                    problems=["Only words in boxes.", "Nothing moves."])
    model = Model(whole(GOOD), whole(GOOD.replace("Touch", "Touching")), whole(GOOD))
    wired(monkeypatch, model, BAD_VERDICT, worse, GOOD_VERDICT)

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert any("Round 2 was no better" in e["text"] for e in view["events"])
    assert "did not make it better" in model.requests[2]
    assert "Touching" not in model.requests[2], "it is shown the version the reviewer preferred"
    assert view["status"] == "done" and view["last_render"]["good"]


def test_an_edit_that_matches_nothing_is_sent_back_not_guessed(project_root, monkeypatch):
    slug, project, visual = scripted_project("Bad edit")
    model = Model(whole(CRASHES), edit("no such line", "x"), whole(GOOD))
    wired(monkeypatch, model, GOOD_VERDICT)

    make_scene(slug, visual.id)

    assert "could not be used: edit 1" in model.requests[2]
    assert "not in the file as written" in model.requests[2]
    assert agent_view(slug, visual.id)["status"] == "done"


def test_a_cut_off_answer_is_asked_again_for_less(project_root, monkeypatch):
    slug, project, visual = scripted_project("Cut off")
    model = Model(ModelOutputTruncated("cut off"), whole(GOOD))
    wired(monkeypatch, model, GOOD_VERDICT)

    make_scene(slug, visual.id)

    assert "cut off at the length limit" in model.requests[1]
    assert agent_view(slug, visual.id)["status"] == "done"


def test_a_model_call_that_fails_once_is_tried_again(project_root, monkeypatch):
    slug, project, visual = scripted_project("Blip")
    wired(monkeypatch, Model(ModelCallFailed("rate limited"), whole(GOOD)), GOOD_VERDICT)

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert view["status"] == "done" and any(e["kind"] == "retry" for e in view["events"])


def test_a_model_that_keeps_failing_ends_the_scene_with_the_reason(project_root, monkeypatch):
    slug, project, visual = scripted_project("Down")
    wired(monkeypatch, Model(*[ModelCallFailed("the provider is down")] * 5))

    make_scene(slug, visual.id)

    view = agent_view(slug, visual.id)
    assert "provider is down" in view["error"]
    assert any("plain stand-in" in e["text"] for e in view["events"]), \
        "with no model, a stand-in is drawn without one"


def test_a_later_scene_is_told_what_the_ones_before_it_did(project_root, monkeypatch):
    slug, project, visual = scripted_project("Continuity")
    first = VisualPlanStore(project.root).load().visuals[0]
    model = Model(whole(GOOD), whole(GOOD))
    wired(monkeypatch, model, GOOD_VERDICT, GOOD_VERDICT)

    make_scene(slug, first.id)
    make_scene(slug, visual.id)

    assert "A bar grows under the word touch." in model.requests[1]
    assert "stay consistent" in model.requests[1] and "stay consistent" not in model.requests[0]


def test_a_picture_is_described_once_and_kept(tmp_path, monkeypatch):
    picture = tmp_path / "figure.png"
    picture.write_bytes(b"x")
    seen = []
    monkeypatch.setattr("pipeline.scene_review.look_at_picture",
                        lambda path, question: seen.append(path) or "a labelled brain")
    brief = {"assets": {"pictures": [str(picture)]}}
    state = {"calls": {"agent": 0, "vision": 0}}

    first = scene_maker.picture_notes(brief, tmp_path, state)
    second = scene_maker.picture_notes(brief, tmp_path, state)

    assert "pictures[0] (figure.png): a labelled brain" in first and first == second
    assert len(seen) == 1 and state["calls"]["vision"] == 1


def test_the_instructions_are_the_agent_file_and_never_ask(project_root):
    slug, project, visual = scripted_project("Prompt")

    prompt = scene_maker.system_prompt(project, ["web", "manim"])

    assert "None of them are executable" not in prompt, "a false footer for a scene maker"
    assert "Never ask a question" in prompt and "one screen" in prompt


# --- the answer and its edits ---------------------------------------------------------------


def test_a_whole_file_and_a_spec_are_read_from_an_answer():
    answer = parse_answer(whole("print('a')"))
    assert answer.spec["renderer"] == "pillow" and answer.code == "print('a')\n"


def test_edits_are_read_and_applied_ignoring_trailing_spaces():
    answer = parse_answer(edit("x = 1  \ny = 2", "x = 10\ny = 20"))
    assert apply_edits("a\nx = 1\ny = 2   \nb", answer.edits) == "a\nx = 10\ny = 20\nb"


def test_an_edit_must_find_its_lines_exactly_once():
    with pytest.raises(ValueError, match="not in the file as written"):
        apply_edits("a\nb", [("c", "d")])
    with pytest.raises(ValueError, match="2 times"):
        apply_edits("a\nb\na", [("a", "z")])


def test_an_answer_with_nothing_usable_is_refused_with_a_reason():
    with pytest.raises(ValueError, match="no shots, no complete file and no"):
        parse_answer("Sure, here you go.")
    with pytest.raises(ValueError, match="not valid JSON"):
        parse_answer("```json\n{oops\n```\n```python\nx = 1\n```")


# --- checks, status, stopping, pace ------------------------------------------------------------


def test_motion_that_only_fades_fails_and_motion_that_explains_passes():
    fades = {"plays": [["FadeIn"], ["FadeIn", "FadeOut"], ["Write"], ["Wait"]]}
    explains = {"plays": [["FadeIn"], ["GrowArrow"], ["ReplacementTransform"], ["Move"],
                          ["FadeOut"]]}
    assert motion_check(fades)["status"] == "fail"
    assert motion_check(explains)["status"] == "pass"
    assert motion_check({"snapshots": []})["status"] == "n/a", "renderer without a record"


def test_bringing_many_things_on_as_they_are_named_does_not_fail_motion():
    """Scene 003 of a real run: 9 real motions among 22 entrances failed a share rule
    and drove the model to shrink its labels to make 'motion'."""
    plays = {"plays": [["FadeIn"]] * 22 + [["GrowArrow"], ["Move"], ["Create"]] * 3}
    assert motion_check(plays)["status"] == "pass"
    assert ".scale" not in motion_check({"plays": [["FadeIn"]]})["detail"]


def test_a_scene_left_working_by_a_restart_is_shown_as_interrupted():
    from pipeline.scene_agent import _shown_status

    assert _shown_status("p", "v", "working") == "interrupted", "no thread runs it any more"
    assert _shown_status("p", "v", "queued") == "interrupted"
    assert _shown_status("p", "v", "done") == "done"


def test_model_calls_wait_for_a_place_in_the_provider_s_limit(monkeypatch):
    from pipeline import llm_pace

    monkeypatch.setenv("LLM_REQUESTS_PER_MINUTE", "3")
    monkeypatch.setattr(llm_pace, "_sent", llm_pace.deque())
    now = [100.0]

    def sleep(seconds):
        now[0] += seconds

    waits = [llm_pace.take_a_place(clock=lambda: now[0], sleep=sleep) for _ in range(4)]
    assert waits[:3] == [0, 0, 0], "three fit in the minute"
    assert waits[3] > 59, "the fourth waits for the window, rather than being refused"


def test_stop_all_drops_the_queue_and_stops_the_working_ones(project_root, monkeypatch):
    slug, project, _visual = scripted_project("Stop all")
    release, started = threading.Event(), threading.Event()

    def slow(slug, visual_id, **kwargs):
        started.set()
        release.wait(10)

    # One place only: the first scene works, the second waits in the queue.
    monkeypatch.setattr(scene_agent, "_pool", ThreadPoolExecutor(max_workers=1))
    monkeypatch.setattr(scene_agent, "make_scene", slow)
    ids = [v.id for v in VisualPlanStore(project.root).load().visuals]
    scene_agent.start(slug, ids)
    assert started.wait(5)

    done = scene_agent.stop_all(slug)
    release.set()

    assert done["stopped"] == 2
    queued = agent_view(slug, ids[1])
    assert queued["status"] == "stopped" and not queued["running"], "dropped before it started"
    first = VisualPlanStore(project.root).load().visuals[0]
    assert (scene_folder(project, first) / scene_agent.STOP).exists(), \
        "the working one is told to stop after its round"


def test_the_model_is_shown_the_kits_real_api_not_left_to_guess():
    api = scene_maker.kit_api(["manim", "web", "pillow"])

    assert "class ExplainerScene" in api and ".picture(path: str" in api
    assert "self.brief.assets.pictures[0]" in api, "how to use a slide picture"
    assert "Kit.load()" in api and "kit.picture" in api, "the web kit's own header"
    assert "VideoWriter" in api, "scenekit, for matplotlib and pillow"


def test_an_unclosed_block_and_unfenced_edits_are_still_read():
    unclosed = parse_answer('```json\n{"renderer": "web"}\n```\n```html\n<p>hi</p>')
    assert unclosed.spec["renderer"] == "web" and unclosed.code == "<p>hi</p>\n"

    bare = parse_answer("Here is the fix:\n<<<<<<< SEARCH\na\n=======\nb\n>>>>>>> REPLACE")
    assert bare.edits == [("a", "b")]


def test_the_motion_check_says_how_to_fix_it():
    detail = motion_check({"plays": [["FadeIn"], ["FadeOut"], ["Write"]]})["detail"]
    assert "MOVE or CHANGE" in detail and "ReplacementTransform" in detail


def test_only_a_few_renders_run_at_once():
    from pipeline import scene_round

    assert scene_round._render_slots._value >= 1


def test_deleting_a_project_stops_the_scenes_being_made_in_it(project_root, monkeypatch):
    import time

    from pipeline import project_work
    from pipeline.web.routes_project_admin import stop_and_wait

    slug, project, _visual = scripted_project("Doomed")
    started, ended = threading.Event(), threading.Event()

    def working_until_stopped(slug, visual_id, **kwargs):
        with project_work.working_on(slug):
            started.set()
            while not project_work.stopped():
                time.sleep(0.05)
        ended.set()

    monkeypatch.setattr(scene_agent, "make_scene", working_until_stopped)
    scene_agent.start(slug, [v.id for v in VisualPlanStore(project.root).load().visuals])
    assert started.wait(5) and scene_agent.is_working(slug)

    stop_and_wait(slug)

    assert ended.wait(5), "the work noticed it was stopped"
    assert not scene_agent.is_working(slug)


def test_the_reviewer_scores_a_rubric_and_good_means_the_ship_bar():
    """Yes/no passed cluttered frames and never once said "good". The bar: no line
    below 3, teaching and accuracy at 4 or more."""
    ships = Verdict(scores=scored(low=3, teaches=4, accuracy=4), teaches=True,
                    motion_explains=True, looks_finished=True)
    weak = Verdict(scores=scored(low=4, illustration=2), teaches=True,
                   motion_explains=True, looks_finished=True)
    assert ships.good and not weak.good
    assert weak.scores.weakest()[0] == ("illustration", 2)
    assert scored(teaches=9).teaches == 5, "out of range is clamped, not refused"


def test_a_storyboard_note_reaches_the_scene_as_what_the_person_asked_for(project_root,
                                                                         monkeypatch):
    from pipeline import storyboard

    slug, project, visual = scripted_project("Storyboard note")
    storyboard.set_note(slug, visual.id, "Show the frog's leg larger")
    model = Model(whole(GOOD))
    wired(monkeypatch, model, GOOD_VERDICT)

    make_scene(slug, visual.id)

    assert "What the person asked for" in model.requests[0]
    assert "Show the frog's leg larger" in model.requests[0]


def test_a_scene_answered_with_shots_has_its_program_written_for_it(project_root,
                                                                    monkeypatch):
    """Told to use the templates, the model still wrote every layout by hand. Now
    it may answer with the shots alone, and the program is written from them."""
    from pipeline import scene_maker as maker
    from pipeline.scene_lab import write_brief

    slug, project, visual = scripted_project("Shots")
    brief = write_brief(project, visual)
    shots = ('```json\n{"approach": "steps", "shots": [{"template": "flow", "title": '
             '"Touch", "steps": [{"label": "Touch", "when": "touch"}, {"label": '
             '"Movement", "when": "movement"}]}]}\n```')
    monkeypatch.setattr(maker, "_ask", lambda *args: shots)
    state = {"calls": {"agent": 0, "vision": 0}, "events": []}

    written = maker._written("system", brief, "", "", "scene.py", "", "", "", ["manim"],
                             {}, scene_folder(project, visual, create=True), state)

    code, spec, renderer, entry, rewrote = written
    assert renderer == "manim" and entry == "scene.py" and rewrote
    assert "self.flow(['Touch', 'Movement'])" in code and spec["shots"][0]["template"] == "flow"

    wrong = shots.replace('"flow"', '"montage"')
    monkeypatch.setattr(maker, "_ask", lambda *args: wrong)
    assert maker._written("system", brief, "", "", "scene.py", "", "", "", ["manim"], {},
                          scene_folder(project, visual), state) is None
    assert any("template must be one of" in e["text"] for e in state["events"])
