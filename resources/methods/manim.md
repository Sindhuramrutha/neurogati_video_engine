# Using Manim in a scene

Good for: equations that build up, graphs, geometric constructions, transforms.

Declare it, and render straight to the file the contract asks for:

    # /// script
    # requires-python = ">=3.11"
    # dependencies = ["manim", "pillow"]
    # ///
    import shutil
    from pathlib import Path
    from manim import Scene, Text, Write, config, tempconfig
    from scenekit import load_brief

    brief = load_brief()

    class TheScene(Scene):
        def construct(self):
            title = Text(brief.headline, color=brief.look["text"]).scale(0.9)
            writing = min(2, brief.seconds / 3)
            self.play(Write(title), run_time=writing)
            self.wait(max(0.1, brief.seconds - writing))   # the two add up to the scene

    with tempconfig({"pixel_width": brief.width, "pixel_height": brief.height,
                     "frame_rate": brief.fps, "background_color": brief.look["background"],
                     "media_dir": "manim_media", "output_file": "scene",
                     "disable_caching": True, "verbosity": "ERROR"}):
        scene = TheScene()
        scene.render()
        shutil.copy(scene.renderer.file_writer.movie_file_path, brief.out)

## Know before you use it

- **The total of every `run_time` and `wait` must be about `brief.seconds`.**
  Add them up before writing the scene.
- **`MathTex` and `Tex` need LaTeX installed.** Most machines do not have it.
  Use `Text` unless the brief says LaTeX is available, or draw a formula with
  `Text` and Unicode (x², √, ∑, ∫, →).
- Manim's frame is 14.2 units wide and 8 tall. Keep everything within ±6.4 by
  ±3.6 so nothing touches an edge.
- The first run downloads Manim, which takes a few minutes.
- Manim prints warnings and progress bars as it works. They are not errors.
