"""A whole deck made into a finished video, every stage as the app runs it.

    uv run python -u tools/demo_run.py --name "Demo 001" --deck "<path to .pptx>"

Each stage is the app's own operation, so the project shows its progress in the
app as it goes, and can be picked up there at any stage. The render goes through
the running app's queue (http://127.0.0.1:8000), so it is the app's worker that
renders. Run again with --slug to carry on a project from where it stopped.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

APP = "http://127.0.0.1:8000"
SETUP = {
    "learners": ["general"],
    "voice": "en-US-AndrewNeural",
    "pace": "normal",
    "music": "built-in:calm",
    "intensity": "soft",
    "platforms": ["website", "youtube"],
}
ASK = ("Make the whole chapter into one video at full length: every slide's ideas taught "
       "in order, none skipped or rushed, about {minutes} minutes in all. Group the slides "
       "into sections of two or three slides that belong together, each told as a story "
       "with the people, the experiment and what it proved. Leave out only a slide that "
       "says nothing of its own (a bare title slide), and say why.")


def say(*parts) -> None:
    print(datetime.now().strftime("%H:%M:%S"), *parts, flush=True)


def _checks(view: dict) -> list[dict]:
    return [c for c in view["checks"] if c["status"] == "fail"]


def build(name: str, deck: Path, minutes: int, voice: str = "", length: str = "",
          learners: list[str] | None = None, picks: list[str] | None = None) -> str:
    from pipeline import operations, plan_agent, video_setup
    from pipeline.assets_handoff import confirm_assets
    from pipeline.core import require_project
    from pipeline.sources import sanitize_source_file_name

    slug = operations.create_project(name)["slug"]
    project = require_project(slug)
    say("project", slug)
    project.sources_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(deck, project.sources_dir / sanitize_source_file_name(deck.name))
    operations.run_extraction(slug)
    operations.confirm_extraction(slug)
    # The deck pictures the video must show, chosen by file name ("<file>=<name>"),
    # as a person chooses them on the Extraction page; nothing else from the deck.
    from pipeline import chosen_pictures
    for pick in picks or []:
        file_name, _, picture_name = pick.partition("=")
        chosen_pictures.choose(slug, f"extraction/assets/{file_name.strip()}",
                               picture_name.strip())
        say("chose", file_name, "as", picture_name)
    library = operations.refresh_asset_library(slug)
    say("pictures:", library["audit"]["usable_count"], "usable of", len(library["figures"]))
    confirm_assets(slug)
    video_setup.save(slug, SETUP | ({"voice": voice} if voice else {})
                     | ({"learners": learners} if learners else {}))

    audience = ("; ".join(g.label for g in video_setup.LEARNERS if g.key in learners)
                if learners else "Curious learners new to neuroscience")
    plan_agent.set_setup(slug, {"length_text": length or f"About {minutes} minutes",
                                "audience": audience})
    view = plan_agent.send_message(slug, ASK.format(minutes=minutes))
    for _ in range(2):
        proposal = view.get("proposal") or {}
        if not proposal.get("problems"):
            break
        view = plan_agent.send_message(slug, "Fix these first: "
                                       + "; ".join(proposal["problems"]))
    plan_agent.agree(slug)
    return slug


def script(slug: str) -> None:
    from pipeline.plan_handoff import read_plan_handoff, transfer_plan
    from pipeline.script_drafting import draft_unwritten_sections
    from pipeline.script_handoff import read_script_handoff, transfer_script

    failing = _checks(read_plan_handoff(slug))
    if failing:
        raise SystemExit(f"plan checks fail: {json.dumps(failing, indent=1)}")
    transfer_plan(slug)
    say("plan transferred; drafting the script")
    for attempt in range(3):
        result = draft_unwritten_sections(slug)
        say("drafted:", {k: v for k, v in result.items() if k != "script"})
        if not _unwritten(slug):
            break
        say("sections still unwritten; drafting again", attempt + 1)
    failing = _checks(read_script_handoff(slug))
    if failing:
        raise SystemExit(f"script checks fail: {json.dumps(failing, indent=1)}")
    transfer_script(slug)


def _unwritten(slug: str) -> list[str]:
    from pipeline.core import require_project
    from pipeline.planning import PlanStore
    from pipeline.scripting import ScriptStore

    project = require_project(slug)
    written = {s.section_id for s in ScriptStore(project.root).load().section_scripts
               if s.scenes}
    return [s.id for s in PlanStore(project.root).load().sections if s.id not in written]


def prepare(slug: str) -> None:
    from pipeline import operations, storyboard, video_setup

    try:
        video_setup.suggest_pronunciations(slug)
        say("pronunciations:", video_setup.load(_root(slug)).sounds)
    except Exception as failure:          # a nicety; the video is made without it
        say("pronunciations skipped:", failure)
    operations.plan_visuals(slug)
    board = storyboard.read(slug)
    first = board["sections"][0]["id"]
    storyboard.prepare(slug, first)
    storyboard.approve(slug, first)
    say("storyboard of the first section prepared and approved")


def _root(slug: str) -> Path:
    from pipeline.core import require_project
    return require_project(slug).root


def generate(slug: str) -> None:
    from pipeline import scene_agent
    from pipeline.core import require_project
    from pipeline.generation import VisualPlanStore
    from pipeline.scene_lab import scene_folder, write_brief

    project = require_project(slug)
    visuals = VisualPlanStore(project.root).load().visuals
    # A finished scene is kept, unless a picture it was offered is no longer
    # offered (left out on Assets & Design since): that one is made again.
    todo, again = [], []
    for visual in visuals:
        folder = scene_folder(project, visual, create=True)
        state_path, brief_path = folder / "agent.json", folder / "brief.json"
        done = state_path.exists() and json.loads(
            state_path.read_text(encoding="utf-8")).get("status") == "done"
        before = set(json.loads(brief_path.read_text(encoding="utf-8"))["pictures"]) \
            if brief_path.exists() else set()
        after = set(write_brief(project, visual)["pictures"])
        if done and before - after:
            again.append(visual.id)
        elif not done:
            todo.append(visual.id)
    say("making", len(todo), "scenes;", len(again), "made again without pictures no "
        "longer offered;", len(visuals) - len(todo) - len(again), "kept")
    if again:
        scene_agent.start(slug, again, fresh=True)
    scene_agent.start(slug, todo)
    last = None
    while True:
        time.sleep(30)
        view = scene_agent.queue_view(slug)
        now = (view["working"], view["queued"])     # counts
        if now != last:
            say("scenes working", now[0], "queued", now[1])
            last = now
        if not view["working"] and not view["queued"]:
            break


def _call(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(APP + path, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=120) as answer:
        return json.loads(answer.read() or b"{}")


def render(slug: str) -> None:
    from pipeline import video_setup
    from pipeline.scene_approval import approve_passed

    # The render takes approved scenes only; here every scene that passed its
    # checks is approved, as the person would on the Make tab.
    say("approved:", approve_passed(slug))
    voice = video_setup.edge_voice(_root(slug), "en")
    before = {j["id"] for j in _call("GET", "/api/render-queue")["jobs"]}
    _call("POST", "/api/render-queue", {"slug": slug, "voice_provider": "edge",
                                        "voice": voice})
    say("render queued with", voice)
    while True:
        time.sleep(30)
        # The job just queued: the first one for the project was an earlier render,
        # long done, and was reported as this one.
        job = next(j for j in _call("GET", "/api/render-queue")["jobs"]
                   if j["slug"] == slug and j["id"] not in before)
        if job["status"] in ("done", "failed", "paused"):
            say("render", job["status"], job.get("message", ""), job.get("video_file", ""))
            if job["status"] != "done":
                raise SystemExit("render did not finish")
            return


def export(slug: str) -> None:
    result = _call("POST", f"/api/projects/{slug}/export", {})
    say("export:", json.dumps(result)[:1500])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--name", default="Demo 001")
    parser.add_argument("--deck", default=str(
        ROOT.parents[1] / "contents" / "01-DEMYSTIFYING THE BRAIN"
        / "Demystifying-the-Brain  Chapter 1.pptx"))
    parser.add_argument("--minutes", type=int, default=32)
    parser.add_argument("--length", default="",
                        help='the length in words, e.g. "35 min or more, never shorter"')
    parser.add_argument("--voice", default="",
                        help="an Edge voice the app offers, e.g. en-IN-NeerjaNeural")
    parser.add_argument("--learners", default="",
                        help='learner keys, comma separated, or "all"')
    parser.add_argument("--pick", action="append", default=[],
                        help='a deck picture the video must show: "<file>=<name>"')
    parser.add_argument("--until", default="export",
                        choices=("script", "prepare", "generate", "render", "export"),
                        help="stop after this step")
    parser.add_argument("--slug", default="", help="carry on this project")
    parser.add_argument("--from", dest="start", default="script",
                        choices=("script", "prepare", "generate", "render", "export"))
    chosen = parser.parse_args()
    steps = ("script", "prepare", "generate", "render", "export")
    learners = ([key for key in ("school", "college", "advanced", "teachers", "health",
                                 "engineering", "general")]
                if chosen.learners == "all"
                else [k.strip() for k in chosen.learners.split(",") if k.strip()])
    if chosen.slug:
        slug, todo = chosen.slug, steps[steps.index(chosen.start):]
    else:
        slug = build(chosen.name, Path(chosen.deck), chosen.minutes, chosen.voice,
                     chosen.length, learners, chosen.pick)
        todo = steps
    todo = todo[:todo.index(chosen.until) + 1] if chosen.until in todo else todo
    for step in todo:
        say("--", step)
        globals()[step](slug)
    say("finished", slug)


if __name__ == "__main__":
    main()
