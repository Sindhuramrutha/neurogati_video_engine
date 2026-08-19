"""Generates a standalone ~10-second title/intro clip for one or more modules.

Not part of the regular chapter pipeline (run_chapter.py) -- a module intro
isn't sourced from an input document, it's a short hand-written title card
with narration, animated with the same Manim scene-generation machinery
regular scenes use (TTS -> alignment -> timed animation brief -> Manim code
-> render -> mux). Reuses agents/visual_render.py's "manim" renderer
directly so it gets the same retry/lint/duration-check loop for free.

Usage:
    python make_module_intros.py --project NPS
    python make_module_intros.py --project NPS --modules 2,6
"""

import argparse
from pathlib import Path

from agents.visual_render import RENDERERS
from state import Scene
from utils.audio_alignment import align
from utils.av_compose import compose_scene
from utils.storage import PROJECTS_DIR
from utils.tts import synthesize

# Each module's ~10-second script + a concrete (not vague) animation brief.
# Content is grounded in this project's own real section titles -- see
# projects/NPS/input_files/Module-*/ -- not invented.
MODULE_INTROS: dict[int, dict[str, str]] = {
    2: {
        "title": "The Neural Signal Acquisition Chain",
        "narration": (
            "Module Two: The Neural Signal Acquisition Chain. Learn how electrodes "
            "capture brain signals, how amplifiers and filters condition them, and "
            "how sampling turns them into digital data, safely and accurately. "
            "Let's get started!"
        ),
        "animation_description": (
            "A dynamic title card animation, not a static layout -- every element "
            "should enter with real motion. 'MODULE 2' flies in and settles at the "
            "top of the screen, then 'The Neural Signal Acquisition Chain' writes "
            "itself in below, letter by letter. As the narration says 'electrodes', "
            "an electrode shape grows in from nothing on the left; as it says "
            "'amplifiers and filters', an amplifier symbol slides in and connects "
            "to the electrode with an animated arrow that draws itself; as it says "
            "'sampling' and 'digital data', a discrete step-waveform/ADC icon "
            "builds in and connects with another drawn arrow, completing a left-to"
            "-right signal chain. Give the whole chain a subtle continuous pulse "
            "once assembled, not a frozen still frame. For the closing line 'Let's "
            "get started!', clear the chain diagram and have that phrase burst in "
            "large and bold at the center with a quick scale-up/flash entrance, "
            "held to the end."
        ),
    },
    5: {
        "title": "Filtering Neural Signals",
        "narration": (
            "Module Five: Filtering Neural Signals. Learn why signals need "
            "filtering, and how low-pass, high-pass, band-pass, and notch filters "
            "each clean unwanted noise from real neural data. Let's get started!"
        ),
        "animation_description": (
            "A dynamic title card animation with real motion throughout, not a "
            "static layout. 'MODULE 5' flies in and settles at the top, then "
            "'Filtering Neural Signals' writes itself in below, letter by letter. "
            "A visibly noisy, jagged waveform draws itself in on screen. As the "
            "narration names each filter, one labeled card at a time grows in "
            "along a row -- 'Low-Pass', 'High-Pass', 'Band-Pass', 'Notch' -- each "
            "one flashing/highlighting the instant it's named, previous cards "
            "staying visible and slightly dimmed. As the last card lands, animate "
            "the jagged waveform smoothly morphing (via a Transform, not a cut) "
            "into a clean, smooth version of itself. For the closing line 'Let's "
            "get started!', clear the diagram and have that phrase burst in large "
            "and bold at the center with a quick scale-up/flash entrance, held to "
            "the end."
        ),
    },
    6: {
        "title": "Time-Frequency Analysis",
        "narration": (
            "Module Six: Time-Frequency Analysis. Learn why neural signals change "
            "over time, how spectrograms and wavelets reveal that change, and how "
            "event-related potentials uncover hidden patterns. Let's get started!"
        ),
        "animation_description": (
            "A dynamic title card animation with real motion throughout, not a "
            "static layout. 'MODULE 6' flies in and settles at the top, then "
            "'Time-Frequency Analysis' writes itself in below, letter by letter. A "
            "wavy time-domain signal draws itself in on the left half of the "
            "screen, animating with a gentle continuous wiggle rather than sitting "
            "frozen. As the narration mentions 'spectrograms', a colorful "
            "spectrogram-style heatmap (rows of shifting color blocks building in "
            "one at a time) grows in on the right half, connected to the waveform "
            "by a drawn transform-style arrow. As it mentions 'event-related "
            "potentials', a small highlighted peak/spike pulses briefly within the "
            "waveform. For the closing line 'Let's get started!', clear the "
            "diagram and have that phrase burst in large and bold at the center "
            "with a quick scale-up/flash entrance, held to the end."
        ),
    },
    7: {
        "title": "Electroencephalography",
        "narration": (
            "Module Seven: Electroencephalography. Learn what EEG is, how "
            "electrodes record the brain's electrical activity from the scalp, "
            "and how to begin interpreting these signals. Let's get started!"
        ),
        "animation_description": (
            "A dynamic title card animation with real motion throughout, not a "
            "static layout. 'MODULE 7' flies in and settles at the top, then "
            "'Electroencephalography' writes itself in below, letter by letter. A "
            "stylized head/scalp outline draws itself in below the title. As the "
            "narration says 'electrodes', a handful of small electrode dots grow "
            "in one by one around the top of the head. As it says 'record the "
            "brain's electrical activity', a squiggly, irregular EEG-style "
            "waveform animates flowing continuously from one electrode across the "
            "lower part of the screen, as if being recorded live. For the closing "
            "line 'Let's get started!', clear the diagram and have that phrase "
            "burst in large and bold at the center with a quick scale-up/flash "
            "entrance, held to the end."
        ),
    },
}


def make_intro(project: str, module: int) -> Path:
    info = MODULE_INTROS[module]
    project_root = PROJECTS_DIR / project / "module_intros" / f"module-{module}-intro"
    project_root.mkdir(parents=True, exist_ok=True)

    scene = Scene(
        id=0,
        subtopic=f"Module {module} Introduction",
        narration=info["narration"],
        animation_description=info["animation_description"],
        scene_type="manim",
    )

    audio_path = project_root / "narration.wav"
    synthesize(scene.narration, audio_path)
    timestamps = align(audio_path)
    scene = scene.model_copy(update={"audio_path": str(audio_path), "timestamps": timestamps})

    print(f"  module {module}: narration synthesized ({len(timestamps)} words) -> rendering animation...")
    scene = RENDERERS["manim"](scene, project_root)

    if scene.render_status != "rendered":
        raise SystemExit(
            f"module {module}: render failed after {scene.render_attempts} attempt(s) -- "
            f"{scene.last_feedback}"
        )

    videos_dir = PROJECTS_DIR / project / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)
    out_path = videos_dir / f"module-{module}-intro.mp4"
    compose_scene(Path(scene.video_path), audio_path, out_path)
    print(f"  module {module}: done -> {out_path}")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", required=True, help="Project folder slug under projects/, e.g. NPS")
    parser.add_argument(
        "--modules", default=None,
        help=f"Comma-separated module numbers, e.g. 2,5,6,7 (default: all of {sorted(MODULE_INTROS)})",
    )
    args = parser.parse_args()

    modules = [int(m) for m in args.modules.split(",")] if args.modules else sorted(MODULE_INTROS)
    for m in modules:
        if m not in MODULE_INTROS:
            raise SystemExit(f"No intro script defined for module {m}. Defined: {sorted(MODULE_INTROS)}")

    for module in modules:
        make_intro(args.project, module)


if __name__ == "__main__":
    main()
