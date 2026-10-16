"""Run the quality test set: one section of a deck through the whole pipeline, then
a report of how good the scenes came out and what they cost.

    uv run python tools/quality_run.py --section spark
    uv run python tools/quality_run.py --section all

Each run makes a fresh project (named for the section and the time), so runs are
compared side by side in the app and on disk. The report is written beside the
project: projects/<slug>/quality-report.md, with a contact sheet of every scene's
poster (quality-sheet.png).

Every step is the app's own function. Only the plan is shaped here -- one section,
its slides, its length and scene count -- instead of by the planning conversation,
so the same section is planned the same way each run and runs can be compared.

See docs/plans/video-quality-plan.md, section 6 G2.
"""

from __future__ import annotations

import argparse
import json
import shutil
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST_SET = json.loads((Path(__file__).with_name("quality_set.json")).read_text(encoding="utf-8"))


def say(*parts) -> None:
    print(datetime.now().strftime("%H:%M:%S"), *parts, flush=True)


def build(section: dict) -> str:
    """A project for this one section, planned and scripted, ready to generate."""
    from pipeline import operations
    from pipeline.assets_handoff import confirm_assets
    from pipeline.core import require_project
    from pipeline.extraction import ExtractionStore
    from pipeline.lesson_plan import save_plan
    from pipeline.plan_agent import write_scenes
    from pipeline.plan_handoff import read_plan_handoff, transfer_plan
    from pipeline.plan_units import references_for, units_of
    from pipeline.planning import PlanLength, PlanSection, PlanStore
    from pipeline.script_drafting import draft_section
    from pipeline.script_handoff import read_script_handoff, transfer_script
    from pipeline.sources import sanitize_source_file_name

    deck = (ROOT / section["deck"]).resolve()
    name = f"Quality {section['key']} {datetime.now():%m-%d %H%M}"
    slug = operations.create_project(name)["slug"]
    project = require_project(slug)
    project.sources_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(deck, project.sources_dir / sanitize_source_file_name(deck.name))
    operations.run_extraction(slug)
    operations.confirm_extraction(slug)
    say("pictures gathered:", len(operations.refresh_asset_library(slug)["figures"]))
    confirm_assets(slug)

    extraction = ExtractionStore(project.root).load()
    units = units_of(extraction)
    seconds, slides = section["seconds"], section["slides"]
    plan = PlanStore(project.root).load()
    plan.length = PlanLength(shortest_seconds=seconds - 30, longest_seconds=seconds + 30,
                             understood=f"About {round(seconds / 60)} minutes.")
    plan.audience = section.get("audience", "")
    plan.slides_left_out = {u.number: "Quality run: only this section is made."
                            for u in units if u.number not in slides}
    planned = PlanSection(title=section["title"], summary=section["summary"],
                          how=section["how"], sources=references_for(slides, units),
                          estimated_seconds=seconds)
    plan.sections = [planned]
    plan.shape_agreed_at = datetime.now().isoformat()
    plan.extraction_fingerprint = extraction.content_fingerprint()
    write_scenes(project, plan, {planned.id: section["scenes"]}, extraction, units, [])
    plan = save_plan(project, plan)
    failing = [c for c in read_plan_handoff(slug)["checks"] if c["status"] == "fail"]
    if failing:
        raise SystemExit(f"plan checks fail: {failing}")
    transfer_plan(slug)
    draft_section(slug, planned.id)
    failing = [c for c in read_script_handoff(slug)["checks"] if c["status"] == "fail"]
    if failing:
        raise SystemExit(f"script checks fail: {failing}")
    transfer_script(slug)
    operations.plan_visuals(slug)
    say("built", slug)
    return slug


def generate(slug: str) -> float:
    from pipeline import scene_agent
    from pipeline.core import require_project
    from pipeline.generation import VisualPlanStore

    visuals = VisualPlanStore(require_project(slug).root).load().visuals
    started = time.time()
    scene_agent.start(slug, [v.id for v in visuals])
    while True:
        time.sleep(20)
        view = scene_agent.queue_view(slug)
        if not view["working"] and not view["queued"]:
            break
    return (time.time() - started) / 60


def report(slug: str, minutes: float) -> Path:
    """The report: every scene's rubric, rounds and cost, the totals, the sheet."""
    from pipeline.core import require_project
    from pipeline.scene_pictures import deck_usage

    project = require_project(slug)
    root = project.root
    usage = deck_usage(project)
    rows, totals = [], {"prompt": 0, "completion": 0, "agent": 0, "vision": 0, "image": 0}
    ships, scores_seen, rounds = 0, [], []
    posters, templates = [], []
    for folder in sorted((root / "generation" / "scenes").glob("[0-9]*")):
        state = json.loads((folder / "agent.json").read_text(encoding="utf-8"))
        last = state.get("last_render") or {}
        scores = last.get("scores") or {}
        totals["prompt"] += state["tokens"]["prompt"]
        totals["completion"] += state["tokens"]["completion"]
        for kind in ("agent", "vision", "image"):
            totals[kind] += state["calls"].get(kind, 0)
        rounds.append(state["renders"])
        if scores:
            scores_seen.append(scores)
        ships += bool(last.get("good"))
        entry = folder / "scene.py"
        program = entry.read_text(encoding="utf-8") if entry.exists() else ""
        template = next((name for name in TEMPLATES if f"self.{name}(" in program), "by hand")
        templates.append(template)
        rows.append(
            f"| {folder.name[:3]} | {template} | {state['renders']} | "
            f"{'yes' if last.get('passed') else 'no'} | {'yes' if last.get('good') else 'no'} | "
            + " | ".join(str(scores.get(k, "-")) for k in RUBRIC)
            + f" | {', '.join(last.get('failing') or []) or '-'} |")
        if (folder / "poster.png").exists():
            posters.append(folder / "poster.png")
    count = len(rounds) or 1
    averages = {k: round(sum(s[k] for s in scores_seen) / len(scores_seen), 2)
                for k in RUBRIC} if scores_seen else {}
    sheet = _contact_sheet(posters, root / "quality-sheet.png")
    lines = [
        f"# Quality run: {slug}", "",
        f"{count} scenes · {minutes:.1f} min · meets the ship bar: {ships} of {count} · "
        f"rounds per scene {sum(rounds) / count:.1f}", "",
        f"Tokens: {totals['prompt']:,} prompt, {totals['completion']:,} completion. "
        f"Calls: {totals['agent']} agent, {totals['vision']} vision, {totals['image']} image.",
        "", "Rubric averages (scenes the reviewer scored): "
        + (", ".join(f"{k} {v}" for k, v in averages.items()) or "none scored"), "",
        f"Templates: {sum(t != 'by hand' for t in templates)} of {count} scenes.", "",
        f"Deck pictures shown: {usage['shown']} of {usage['deck_pictures']}"
        + (" (not shown: " + ", ".join(p["name"] for p in usage["not_shown"][:8])
           + ("..." if len(usage["not_shown"]) > 8 else "") + ")"
           if usage["not_shown"] else ""), "",
        "| Scene | Shot | Rounds | Checks pass | Ship bar | " + " | ".join(RUBRIC) + " | Failing |",
        "|---|---|---|---|---|" + "---|" * len(RUBRIC) + "---|", *rows, "",
        f"![contact sheet]({sheet.name})" if sheet else "",
    ]
    path = root / "quality-report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    (root / "quality-report.json").write_text(json.dumps({
        "slug": slug, "minutes": minutes, "scenes": count, "ships": ships,
        "rounds_per_scene": sum(rounds) / count, "averages": averages, "totals": totals,
        "templates": templates,
        "deck_pictures": {"deck": usage["deck_pictures"], "shown": usage["shown"]}},
        indent=1), encoding="utf-8")
    return path


TEMPLATES = ("hero", "steps", "compare", "person", "key_idea", "opener", "flow", "hub",
             "timeline")
RUBRIC = ("teaches", "accuracy", "illustration", "composition", "labels", "motion", "finish")


def _contact_sheet(posters: list[Path], target: Path) -> Path | None:
    from PIL import Image

    if not posters:
        return None
    width, height, columns = 640, 360, 3
    rows = (len(posters) + columns - 1) // columns
    sheet = Image.new("RGB", (width * columns, height * rows), (40, 40, 40))
    for index, poster in enumerate(posters):
        with Image.open(poster) as image:
            sheet.paste(image.convert("RGB").resize((width, height)),
                        ((index % columns) * width, (index // columns) * height))
    sheet.save(target)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--section", default="spark",
                        help="a key from quality_set.json, or 'all'")
    chosen = parser.parse_args().section
    sections = TEST_SET if chosen == "all" else [s for s in TEST_SET if s["key"] == chosen]
    if not sections:
        raise SystemExit(f"no section {chosen!r}: {[s['key'] for s in TEST_SET]}")
    for section in sections:
        slug = build(section)
        minutes = generate(slug)
        say("report:", report(slug, minutes))


if __name__ == "__main__":
    main()
