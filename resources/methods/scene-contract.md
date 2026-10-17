# The scene contract: what every scene must do

A scene is one folder. Its entry file is a program that draws the scene's clip,
in the renderer its spec names:

- `scene.py` (manim, matplotlib, pillow) -- run as
  `scene.py --brief brief.json --out render.mp4` in the scene folder;
- `scene.html` (web) -- recorded frame by frame in headless Chromium
  (`web-scenes.md`);
- `scene.tsx` (revideo) -- a Motion Canvas scene rendered by Revideo
  (`revideo-scenes.md`).

The rules below hold whatever the renderer; where a rule names a Manim helper,
the web kit has the same one (`kit.label`, `kit.picture`, `kit.when`).

## What the scene is

A teaching visual, synchronised to the narration. It is **not a slide** and
**never a paragraph on screen**. The narration is spoken; the picture shows the
idea being said, in deliberate beats, such as:

- a heading or concept introduced
- a progressive reveal, a diagram being built, arrows and flows
- a comparison
- a timeline whose stages appear and gain emphasis
- a chart that grows
- a highlight on the thing just named

Motion explains the current spoken idea; it never decorates.

## It must

1. **Write `render.mp4`**: H.264, exactly `brief.width` × `brief.height`, at
   `brief.fps`, with **no sound**.
2. **Last exactly `brief.seconds`**, the narration's *measured* length, within
   5%. With Manim, end with `self.finish()`.
3. **Put each beat on its words.** `brief.words` gives every spoken word's
   `start_ms`. With manimkit, `self.until(self.when("the exact words"))`.
4. **Keep text short and readable:**
   - at most 18 words in one label, and 25 on screen at once
   - lines at least 36 px tall
   - contrast of at least 4.5:1 against what is behind them
   - inside a 5% margin
   - never overlapping other text
5. **Never run a shape through words.** Put words in a box only with
   `self.boxed(...)` (sized to fit), join things only with `self.connect(a, b)`
   (edge to edge). No box edge, arrow, line or circle crosses text; it is checked.
6. **Label what stands for something.** Every node, dot, box or arrow that means
   something carries its few words. An unlabelled shape explains nothing; an empty
   box is a mistake. The main visual fills most of the frame.
7. **Ground every word and number.** On-screen text comes from `narration`,
   `on_screen` or `source_text`. Add no fact, number or label that is not there.
8. **Record its text.** With Manim, start with `from manimkit import *` (every
   Manim name and the kit), and make text with `self.label(...)`, so `layout.json`
   lists it for the checks. The kit fits anything with words inside the margin and
   moves words off words already on screen; use `self.row`/`self.column` to lay
   out several things at once. A web scene's text is measured from the page
   itself; use `kit.label(...)`, which keeps it inside the margin.
9. **Change visibly.** At least three distinct moments; a still frame fails.
   **Picture the idea, not the words.** At half the beats or more, at least two
   things on screen are not words: nodes, arrows, a timeline, shapes, a chart.
   Animated quotations are not a picture; a diagram of what they say is.
10. **Declare what it needs** at the very top of a `scene.py`:

       # /// script
       # requires-python = ">=3.11"
       # dependencies = ["manim>=0.19", "pillow"]
       # ///

11. **Record every outside resource** with `scenekit.fetch(url, name, licence,
   credit)`.

## Renderers

| Renderer | For | How |
| --- | --- | --- |
| `web` | Rich motion: morphs, motion paths, drawn strokes, zooms, data charts (D3), 3D (three.js) | `scene.html` with `webkit.js` and GSAP / D3 / three.js / anime.js (see `web-scenes.md`). |
| `revideo` | Polished, physical (spring) motion; typeset maths without TeX; code typed in | `scene.tsx`, a Motion Canvas scene in Revideo's form, with `./kit` (see `revideo-scenes.md`). |
| `manim` | Diagrams, labels, flows, timelines, transformations, technical explanation | `manimkit` (see `manimkit_example.py`). Place groups with `self.row(...)` / `self.column(...)`. There is no LaTeX: use `Text`, not `MathTex`. |
| `matplotlib` | Charts and plots that grow as they are explained | Write frames and encode with `scenekit.VideoWriter`. |
| `pillow` | Simple composed frames | `scenekit`. |

Choose whichever explains the idea best; nothing is the default.

## The brief

`brief.json` has:

- **What is said:** `narration`, `words` (each spoken word with `start_ms` and
  `duration_ms`), `seconds` (measured) and `time_range` (where the scene falls
  in its section).
- **What to show:** `on_screen` (the visual brief), `headline`, `section_title`
  and `how` (how the section is told).
- **The section around it:** `section_scenes` (every scene of the section, this
  one marked), so a scene can be one stage of a picture the section builds: draw
  all the stages, and emphasise this one.
- **What it is grounded in:** `source_text` (the section's slides).
- **What it may use:**
  - `assets.pictures`: the pictures offered, by index; `picture_catalogue` says
    what each is (where from, its role, whether it is the scene's own: `near`,
    which other scenes show it). A scene with pictures of its own **shows one**
    (`self.picture(path)`) and explains it on screen: labels joined to its parts,
    a highlight, a reveal
- **How it looks:** `look` (`background`, `panel`, `accent`, `text`, `dim`,
  `heading_font`, `body_font`). Use these colours so every scene belongs together.
- **The frame:** `width`, `height`, `fps`, `language`.
