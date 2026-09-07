"""Turns a PowerPoint deck into a narrated, highlight-annotated video --
each slide shown as-is, with narration audio and animated highlights
(box/circle/arrow) pointing at whatever's currently being discussed.

Not part of the regular chapter pipeline (run_chapter.py) -- a slide deck
isn't sourced from a document to be planned into scenes, it already has
its own fixed structure (one slide = one scene). This wires together,
unchanged: utils/pptx_rasterize.py + utils/pptx_reader.py (ingestion),
agents/slide_narrator.py (narration fallback), utils/tts.py +
utils/audio_alignment.py (voice + timing), agents/highlight_planner.py
(what to point at and when), agents/visual_render.py's RENDERERS["manim"]
(rendering, with its existing retry/lint/duration-check loop), and
utils/av_compose.py + utils/stitch.py + utils/subtitles.py (muxing and
final assembly) -- all imported and used exactly as the rest of the
pipeline already does.

State is saved after every single slide, not once at the end of the whole
run -- a hard lesson from the regular chapter pipeline, where a single
end-of-batch save meant an interrupted run could lose every already-
rendered scene's progress. That mistake isn't repeated here.

Usage:
    python pptx_deck_pipeline.py --project NPS --pptx "Demystifying-the-Brain Chapter 1.pptx"
    python pptx_deck_pipeline.py --project NPS --pptx deck.pptx --slides 1,2,3
"""

import argparse
import json
import shutil
from pathlib import Path
from typing import Optional

from agents.highlight_planner import plan_highlights, render_prompt_from_highlights
from agents.slide_narrator import auto_narrate_slide
from agents.visual_render import RENDERERS
from state import Scene
from utils.asset_library import list_image_assets, register_asset, unregister_asset
from utils.audio_alignment import align
from utils.av_compose import compose_scene
from utils.ffmpeg_utils import duration_seconds
from utils.pptx_rasterize import export_slides_to_png
from utils.pptx_reader import SlideContent, read_deck
from utils.storage import PROJECTS_DIR, slugify
from utils.stitch import stitch_clips
from utils.subtitles import build_srt


def _asset_key(deck_slug: str, slide_index: int) -> str:
    return f"pptx_{deck_slug}_slide_{slide_index:02d}"


def _sweep_stale_assets(deck_slug: str) -> None:
    """Removes any leftover temp asset from a previous run that crashed hard
    enough to skip its own `finally` cleanup (e.g. a killed process). Safe to
    call every run -- a no-op when nothing's left over.
    """
    prefix = f"pptx_{deck_slug}_slide_"
    for key in list(list_image_assets()):
        if key.startswith(prefix):
            unregister_asset(key)


def _load_scenes(state_path: Path) -> Optional[list[Scene]]:
    if not state_path.exists():
        return None
    return [Scene(**s) for s in json.loads(state_path.read_text(encoding="utf-8"))]


def _save_scenes(state_path: Path, scenes: list[Scene]) -> None:
    state_path.write_text(
        json.dumps([s.model_dump() for s in scenes], indent=2), encoding="utf-8"
    )


def _resolve_narration(deck_dir: Path, descriptions_dir: Optional[Path], slide: SlideContent) -> str:
    if descriptions_dir is not None:
        desc_path = descriptions_dir / f"slide_{slide.index:02d}.txt"
        if desc_path.exists():
            text = desc_path.read_text(encoding="utf-8").strip()
            if text:
                return text
    return auto_narrate_slide(slide)


def process_slide(
    slide: SlideContent,
    deck_dir: Path,
    deck_slug: str,
    slide_png: Path,
    descriptions_dir: Optional[Path],
    existing: Optional[Scene],
) -> Scene:
    scene_id = slide.index
    print(f"  slide {scene_id}:")

    if existing is not None and existing.render_status == "rendered" and existing.composed_path:
        print("    already composed, skipping")
        return existing

    scene = existing or Scene(
        id=scene_id, subtopic=f"Slide {scene_id}", narration="",
        animation_description="(unused -- render_prompt set directly)", scene_type="manim",
    )

    if not scene.narration:
        scene = scene.model_copy(
            update={"narration": _resolve_narration(deck_dir, descriptions_dir, slide)}
        )
        print(f"    narration ready ({len(scene.narration)} chars)")

    if not scene.audio_path or not Path(scene.audio_path).exists():
        audio_path = deck_dir / "audio" / f"slide_{scene_id:02d}.wav"
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        from utils.tts import synthesize
        synthesize(scene.narration, audio_path)
        timestamps = align(audio_path)
        transcripts_dir = deck_dir / "transcripts"
        transcripts_dir.mkdir(parents=True, exist_ok=True)
        (transcripts_dir / f"slide_{scene_id:02d}.txt").write_text(scene.narration, encoding="utf-8")
        scene = scene.model_copy(update={"audio_path": str(audio_path), "timestamps": timestamps})
        print(f"    audio ready ({duration_seconds(audio_path):.2f}s, {len(timestamps)} words)")

    asset_key = _asset_key(deck_slug, scene_id)

    if not scene.render_prompt:
        highlight_plans_dir = deck_dir / "highlight_plans"
        highlight_plans_dir.mkdir(parents=True, exist_ok=True)
        beats = plan_highlights(slide, scene.narration, scene.timestamps)
        (highlight_plans_dir / f"slide_{scene_id:02d}.json").write_text(
            json.dumps([b.model_dump() for b in beats], indent=2), encoding="utf-8"
        )
        total_duration = duration_seconds(Path(scene.audio_path))
        render_prompt = render_prompt_from_highlights(slide, beats, asset_key, total_duration)
        prompts_dir = deck_dir / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / f"slide_{scene_id:02d}_prompt.txt").write_text(render_prompt, encoding="utf-8")
        scene = scene.model_copy(update={"render_prompt": render_prompt})
        print(f"    highlight plan ready ({len(beats)} beats)")

    if scene.render_status != "rendered":
        register_asset(asset_key, slide_png, "image", f"PPTX pipeline temp slide background -- {deck_slug} slide {scene_id}")
        try:
            scene = RENDERERS["manim"](scene, deck_dir)
        finally:
            unregister_asset(asset_key)
        if scene.render_status == "rendered":
            silent_copy = deck_dir / "rendered_video" / f"slide_{scene_id:02d}_silent.mp4"
            silent_copy.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(scene.video_path, silent_copy)
            print(f"    rendered -> {silent_copy}")
        else:
            print(f"    RENDER FAILED: {scene.last_feedback}")
            return scene

    if not scene.composed_path:
        out_path = deck_dir / "rendered_video" / f"slide_{scene_id:02d}_with_audio.mp4"
        compose_scene(Path(scene.video_path), Path(scene.audio_path), out_path)
        scene = scene.model_copy(update={"composed_path": str(out_path)})
        print(f"    composed -> {out_path}")

    return scene


def run(project: str, pptx_filename: str, descriptions_folder: Optional[str], dpi: int, slide_filter: Optional[list[int]]) -> None:
    project_dir = PROJECTS_DIR / project
    pptx_path = project_dir / "input_files" / pptx_filename
    if not pptx_path.exists():
        raise SystemExit(f"No input file at {pptx_path}")

    deck_slug = slugify(pptx_path.stem)
    deck_dir = project_dir / deck_slug
    deck_dir.mkdir(parents=True, exist_ok=True)
    state_path = deck_dir / "state.json"

    descriptions_dir = None
    if descriptions_folder:
        candidate = project_dir / "input_files" / descriptions_folder
        if candidate.exists():
            descriptions_dir = candidate

    print(f"Deck: {deck_slug}  (input: {pptx_filename})")
    _sweep_stale_assets(deck_slug)

    slides = read_deck(pptx_path)
    slides_data_dir = deck_dir / "slides_data"
    slides_data_dir.mkdir(parents=True, exist_ok=True)
    for slide in slides:
        (slides_data_dir / f"slide_{slide.index:02d}.json").write_text(
            slide.model_dump_json(indent=2), encoding="utf-8"
        )

    slides_raw_dir = deck_dir / "slides_raw"
    expected_pngs = [slides_raw_dir / f"slide_{s.index:02d}.png" for s in slides]
    if not all(p.exists() for p in expected_pngs):
        print(f"Rasterizing {len(slides)} slides...")
        export_slides_to_png(pptx_path, slides_raw_dir, dpi=dpi)
    else:
        print("Slides already rasterized, reusing.")

    existing_scenes = _load_scenes(state_path)
    existing_by_id = {s.id: s for s in existing_scenes} if existing_scenes else {}

    targets = slides if slide_filter is None else [s for s in slides if s.index in slide_filter]
    updated = dict(existing_by_id)
    for slide in targets:
        slide_png = slides_raw_dir / f"slide_{slide.index:02d}.png"
        scene = process_slide(slide, deck_dir, deck_slug, slide_png, descriptions_dir, existing_by_id.get(slide.index))
        updated[slide.index] = scene
        # Saved after every slide, not once at the end -- see module docstring.
        _save_scenes(state_path, [updated[s.index] for s in slides if s.index in updated])

    all_scenes = [updated[s.index] for s in slides if s.index in updated]
    composed = [s for s in all_scenes if s.composed_path]
    print(f"\n{len(composed)}/{len(slides)} slides composed.")

    if slide_filter is not None:
        print("(processed a subset -- run with no --slides once every slide is ready, to stitch the final video)")
        return

    if len(composed) < len(slides):
        print("Not every slide is composed yet -- fix the failing ones, then re-run.")
        return

    videos_dir = project_dir / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)
    clip_paths = [s.composed_path for s in all_scenes]
    final_path = stitch_clips(clip_paths, videos_dir / f"{deck_slug}.mp4")
    srt_text = build_srt(all_scenes)
    (videos_dir / f"{deck_slug}.srt").write_text(srt_text, encoding="utf-8")
    print(f"Final video -> {final_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", required=True, help="Project folder slug under projects/, e.g. NPS")
    parser.add_argument("--pptx", required=True, help="Filename under projects/<project>/input_files/")
    parser.add_argument(
        "--descriptions", default=None,
        help="Folder name under input_files/ with optional slide_NN.txt narration overrides "
             "(default: <pptx-stem>_descriptions if it exists)",
    )
    parser.add_argument("--dpi", type=int, default=200, help="Slide rasterization resolution")
    parser.add_argument("--slides", default=None, help="Comma-separated slide numbers (default: all)")
    args = parser.parse_args()

    descriptions_folder = args.descriptions or f"{Path(args.pptx).stem}_descriptions"
    slide_filter = [int(s) for s in args.slides.split(",")] if args.slides else None

    run(args.project, args.pptx, descriptions_folder, args.dpi, slide_filter)


if __name__ == "__main__":
    main()
