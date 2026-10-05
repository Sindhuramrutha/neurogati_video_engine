# Plan: Assets & Design, six changes

A working plan. Delete it when the work is done.

Source: six annotated screenshots and four answered questions (30 Sept 2026).

## The principle behind all six

This layer had drifted into **deciding** things (will show / won't show) and
into **doing** things without saying so (trimming, flagging). Its job is
narrower and clearer:

> **Assets & Design is the inventory and the look.** It shows what exists and
> where it came from, lets you set aside what you don't want, and sets how the
> video looks. It says everything it does to a picture. It does not judge.

Every change below follows from that. Two rules hold throughout:

1. **Nothing happens to an asset without the page saying what, why, and how to
   undo it.**
2. **No AI on this layer.** The same inputs always give the same result.

## Decisions taken (from your answers)

| # | Question | Answer |
|---|---|---|
| 1 | What a picture card does | Shows the picture, its slide number and slide name. One action: **Leave out**. No verdict of any kind on this tab. |
| 2 | How far "skip the brutalism" goes | Only the **Look tab's controls**. The rest of the app keeps its style. |
| 3 | Brand freedom | All four: drag to place and slider to size; opacity, shadow, rounded corners; when it appears; intro/outro trims and fades. |
| 4 | Final view | A strip: Intro → a lesson frame → Outro. |

## One consequence to be aware of

Removing the verdict from this tab means the *fitness* rules (too small, blank,
a sliver) no longer decide anything here. They do not disappear: a 20 px bullet
must still never fill a frame. They move to where a picture is actually chosen
for a scene, **Generation**, whose rule becomes "a picture from the section's
source that is large and clear enough to fill a frame". Generation's Setup tab
lists any handed-on picture that is not, and why. So:

- Assets & Design: every picture is listed and handed on unless you leave it out.
- Generation: decides which picture a scene shows, and says which it cannot use.

---

## Work, in order

### 1. Picture cards: show, don't judge

**Now:** "Will show", a reason line, Use / Skip / Back to the rules.

**After:**

- Title: **Slide 2 · Padma's Story: A Promising Beginning** (slide number and
  slide name, from the extraction). For a document that is not a deck: the
  heading it sits under.
- Under it: the picture's own caption, when it has a real one.
- Facts: its size in pixels.
- One action: **Leave out** ↔ **Put back**. A left-out card is dimmed and says
  "Left out". Nothing else is decided.
- Removed: the verdict, the reason line, Use, Skip, Back to the rules.

**Data:** each picture records `slide_number` and `slide_title` when gathered.
"Included" means "not left out". Old Use/Skip choices are read as: Skip = left
out, anything else = included.

### 2. Each file is a box that opens and closes

- One bordered box per source file. Its header row: file name, "3 pictures",
  "1 left out", and a chevron.
- Click the header to fold or unfold. Open by default; the choice is remembered
  per file for the project.
- The pictures sit inside the box, so which file owns which assets is visible
  at a glance.

### 3. Trimmed and "check the crop": say why, when, how

**Now:** two unexplained chips.

**After:** each becomes a plain sentence on the card with **See why**, which
opens the picture's details in place:

- **Border trimmed**
  - *What:* the original and the trimmed copy side by side, with both sizes.
  - *Why:* the picture had a plain border taking N% of its area; on a frame
    that border is wasted screen.
  - *When:* on gathering, when the border is more than 3% of the picture.
  - *How:* the border colour is read from the edges and cut away. The original
    is never changed.
  - *Your choice:* **Use the trimmed copy** / **Use the original**. Saved per
    picture; the render and scripted scenes honour it.
- **Check the crop**
  - *What:* the picture with the edges where ink touches marked.
  - *Why:* ink in the outer 2% of a picture usually means the crop cut through
    a caption, an axis or a table row.
  - *When:* on gathering, when more than 10% of an edge band is ink.
  - *How:* nothing was changed. It is a prompt to look.
  - *Your choice:* **It looks right** (clears the flag for this picture), or
    **Leave out**, or fix the picture in Extraction.

**Data:** per picture `use_original` and `crop_checked`.

### 4. Brand assets: a real editor

**Now:** four corners, three sizes, three opacities.

**After:** a canvas editor.

- **The canvas:** a 16:9 lesson frame drawn with the project's look, with a
  sample headline so you place things against real content. A dashed 5% safe
  margin.
- **Drag** the logo or the watermark anywhere on it. A 3×3 snap grid and exact
  X / Y fields for precision.
- **Per item (logo, watermark):**
  - Size: 2–60% of the frame's width.
  - Opacity: 5–100%.
  - Rounded corners: 0–50%.
  - Shadow: 0–100%.
  - When it appears: the whole lesson · the first N seconds · the last N
    seconds · from–to. Fade in and fade out, in seconds.
- **Intro and outro:**
  - Trim the start and the end, with the resulting length shown.
  - Cross-fade into / out of the lesson, 0–2 seconds.
- **A timeline** under the canvas: Intro | Lesson | Outro, with a bar for when
  the logo and the watermark are on screen.
- Every change saves at once and is part of the next transfer.

**Render:** the logo and watermark are prepared once as finished images (size,
corners, opacity, shadow) and laid on by ffmpeg at their position and times.
Trims and cross-fades are applied when the intro and outro are joined.
Subtitles, the timeline and chapters are offset by the intro's real length
(after trim, minus the cross-fade). All fixed arithmetic.

**Old projects:** the corner / size / opacity choices are converted to the
equivalent position, size and opacity, so nothing moves.

### 5. The Look tab: controls a person can use

**Now:** three grids of 13 swatches named `dk1`, `lt2`, `accent4`.

**After** (softer controls, this tab only):

- **Preview on the right**, always in view, redrawn on every change.
- **Themes:** three or four ready-made starting points built from the chosen
  deck's own palette (Deck's own · Light · Dark · Accent-led), each a small
  preview card. One click.
- **Colours:** three rows with plain names and one line each of what they are:
  *Background* (behind everything), *Panels* (what text and pictures sit on),
  *Accent* (the bar and highlights). Each is a colour well showing the colour
  and its hex. Clicking it offers the deck's colours as swatches, **any colour**
  through a picker or a hex field, and **Reset**.
- **Readability:** the text colour the render will use, and its contrast
  against the background as a ratio, with a warning under 4.5:1.
- **Fonts:** two dropdowns, each option shown by name, with a sample line set
  in the chosen font.
- **Background art:** a switch, then three picture cards showing each reading
  of the deck's sheet, instead of three paragraphs.

**Data:** a colour choice may now be any hex, not only a palette name.

### 6. Final & transfer: the video as it will look

- **A strip:** Intro (playable, trimmed length) → **the lesson frame** with the
  look, the logo and the watermark exactly as placed → Outro (playable).
  Cross-fades and the times the logo and watermark appear are written under it.
- **Pictures handed on (N)** as thumbnails, and **Left out (M)** by name.
- The look and the brand assets, each stated in a sentence.
- Nothing about what is handed on is left unsaid.

---

## How each step is checked

- Backend: a test for every rule and every conversion (old choices → new), and
  a real ffmpeg run for the brand pass with placement, timing, trim and fade.
- Page: each step walked through in a browser on a throwaway copy, with a
  screenshot looked at before moving on.
- The full suite passes before the next step starts.
- The SOP (`docs/operations/assets-and-design-sop.md`) is updated with each
  step, not at the end.

## Files

| Area | Files |
|---|---|
| Pictures | `assets.py`, `figure_prep.py`, `assets_handoff.py`, `stage-assets.js`, `assets.css` |
| Fitness moves to Generation | `generation.py`, `generation_handoff.py`, `stage-generation.js` |
| Brand | `brand_kit.py`, `render_brand.py`, `render_run.py`, new `brand-editor.js` |
| Look | `project_look.py`, new `look-editor.js`, `assets.css` |
| Final | `stage-assets.js` |
