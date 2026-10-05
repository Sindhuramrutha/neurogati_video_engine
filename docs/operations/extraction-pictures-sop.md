# SOP: changing a picture in the extraction

How a figure's picture is replaced, redrawn, edited or added during Extraction,
and what must be true afterwards. The code is `src/pipeline/figure_pictures.py`.
Every path below goes through it, and a new path must too.

## The paths

| Path | Where | Action |
|---|---|---|
| Upload a picture | Review tab, on a finding | replace |
| Draw a picture | Review tab, on a finding | redraw |
| Agent: `redraw_image` | Review tab chat | redraw |
| Agent: `edit_image` | Review tab chat | edit |
| Agent: `add_image` | Review tab chat | add |

## Choose the action

1. **The slide already has a picture that should be different** (a placeholder,
   a broken, blank or wrong picture): **redraw** it, or **edit** it to keep most
   of it. The new picture takes the old one's place on the slide.
2. **The slide has no picture for this**: **add**. The new figure goes after the
   block you name, and the Layout box notes "N added picture(s), not placed on
   the slide", because the original slide has no slot for it.
3. **You have the right picture as a file**: **upload**.

The agent is instructed to follow 1 and 2. If it proposes an add where a
redraw was meant, discard the proposal and ask it to redraw that figure.

## What the image model is sent

Built by `picture_prompt`, for every draw:

- **What to draw**: the figure's caption, or the add's instruction.
- **The instruction**, if any.
- **The slide's text, for understanding only.** For a deck this is that slide's
  headings, paragraphs and list items. For a document it is the blocks around
  the figure. Speaker notes are never sent.
- **The shape**: landscape, portrait or square, from the slot the picture fills
  on the slide.
- **The no-text rule**: the picture only; no slide, title bar, heading,
  paragraph, caption, quote or sentence from the text. No words at all unless
  the instruction asks for labels, and then one to three words each. Nothing
  invented.
- **The style** (flat, plain white background, high contrast), unless the
  instruction asks for another.

An edit is sent the picture plus the instruction and "keep everything else;
add no title, caption or text".

## What changes

`set_picture`, in one save:

- The figure's picture becomes the new one.
- The layout shape on the same slide that showed the old picture shows the new
  one, so the Layout box and every later stage agree.
- The figure is marked `generated` (drawn or edited by a model) or `uploaded`.
  It is never passed off as the author's own.

## Checks after a change

- [ ] The Figure box shows the new picture, with **no slide text drawn in it**.
- [ ] The Layout box shows it in the old picture's place (redraw, edit, upload),
      or reports it as added (add).
- [ ] Wrong? Press **Undo** on that proposal (agent changes), or ask for a
      redraw with a clearer instruction. Undo restores the figure and the layout.
- [ ] Then **Final & transfer → Transfer**. Nothing reaches later stages until
      you do.

## Things to know

- **Extracting the file again replaces every picture from the source**,
  including drawn and uploaded ones. Redo the picture changes after a
  re-extract, or don't re-extract that file.
- Each draw or edit is one paid image-model call, made only when you press
  **Apply** (agent) or **Draw a picture** (Review). A proposal costs nothing
  until it is applied.
- A picture drawn before this procedure existed (2026-09-27) may contain slide
  text. Redraw it.
