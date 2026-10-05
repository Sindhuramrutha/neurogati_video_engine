# The scene contract: what every scene.py must do

A scene is one folder. Its `scene.py` draws the scene's clip. It is run as:

    scene.py --brief brief.json --out render.mp4

with the scene folder as the working directory.

## It must

1. **Write `render.mp4`**: H.264, exactly `brief.width` × `brief.height`, at
   `brief.fps`, with **no sound**. The narration is added by the render.
2. **Last about `brief.seconds`.** Shorter is held on its last frame; longer is
   cut off, so never run over.
3. **Show something.** A frame that is one flat colour fails the check.
4. **Keep everything inside the frame**, with a margin of at least 5% on every
   side. Nothing the viewer must read may touch an edge.
5. **Not print the narration.** It is being spoken. Show the few words of
   `brief.on_screen` and `brief.headline`, and the picture of the idea.
6. **Declare what it needs** at the very top, so it runs anywhere:

       # /// script
       # requires-python = ">=3.11"
       # dependencies = ["pillow", "numpy"]
       # ///

7. **Record every outside resource.** Use `scenekit.fetch(url, name, licence,
   credit)`. It saves the file in `assets/` and writes `sources.json`. Only use
   resources whose licence allows it (public domain, CC0, CC BY, MIT, OFL…).

## It may

- Use any library it declares: Manim, matplotlib, numpy, svg tools, anything.
- Use `scenekit` and anything else in `resources/code` (already importable).
- Use the files in `resources/assets`, at the path in the `SCENE_RESOURCES`
  environment variable.
- Use the project's own pictures, listed in `brief.pictures`, and the deck's
  slide in `brief.slide_image`.

## The brief

`brief.json` has: `narration`, `on_screen`, `headline`, `section_title`, `role`,
`scene_number`, `seconds`, `width`, `height`, `fps`, `language`, `pictures`,
`slide_image`, and `look` (`background`, `panel`, `accent`, `text`, `dim`,
`heading_font`, `body_font`). Use the look's colours so every scene of the video
belongs together.
