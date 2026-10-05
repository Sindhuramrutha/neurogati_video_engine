# Plan: one source file per project

A working plan. Delete it when the work is done.

## The decision

A project has **exactly one source file**: a deck, a PDF, a Word document, a
Markdown or text file. That one file runs through every layer. There is no
choosing between files, no ticking, no per-file status, no "which deck"
anywhere.

| Question | Decided |
|---|---|
| A second file is uploaded | It **replaces** the first, after a confirmation that says what happens next |
| Work after Extraction when the file is replaced | **Kept, and flagged out of date** (the change flags already do this) |
| Inside the code | Records keep a file name, so nothing on disk breaks. Every multi-file path in the interface and the logic goes; a second file is refused at upload |
| A supporting reference file (deck + PDF) | Not built |

Every existing project already has at most one file, so none needs converting.

## The principle

**Name the source once, then stop talking about it.** Each layer shows the
source in one place: a strip under its header, "8. Chapter
Feeling-the-World.pptx · deck · 5 slides". Everywhere else a location is just
**"Slide 3"** or **"§ Methods"**, never "file.pptx › Slide 3".

---

## Work, layer by layer

### 1. Server: one source

- **Upload** takes one file. A request with more than one is refused, saying so.
  When the project already has a source, the upload must say `replace`; the old
  file is then removed and the new one kept. Without `replace` it is refused, so
  nothing is ever replaced by accident.
- **The project** has `source`: the one file, or none. `sources()` stays for code
  that lists files, and returns at most that one.
- **Extraction** runs on *the* source. The result *is* the extraction: a run
  replaces it whole, instead of adding to a collection. The old file's result
  cannot linger beside the new one.
- **Remove from the extraction** goes: there is nothing to remove one file from.
  Removing the source on Inputs empties the extraction too.
- **Freshness** becomes one answer: not extracted · extracted · extract again
  (file replaced, or options changed) · transferred.

### 2. Inputs

- **No file:** one drop zone, "Drop your source file here: a deck, PDF, Word,
  Markdown or text file". One file only: dropping two says so and takes none.
- **A file:** one card with its type, name, size, what it is (deck · N slides,
  or N pages) and three actions: **Preview**, **Replace**, **Remove**.
- **Replace** (or dropping a new file on the card) asks first: "Replace
  *old.pptx* with *new.pptx*? Extract it again; every later layer is marked out
  of date until it is redone or transferred as it stands."

### 3. Extraction

- **Extract tab:** no file list, no tick boxes, no "Extract N selected files".
  One card: the source, its state in a sentence, and one button: **Extract** /
  **Extract again** / **Extracted ✓**. The options sit beside it.
- **Review tab:** no "Extracted files" picker; the slide-by-slide review gets the
  full width.
- **Final & transfer:** no file list or per-file remove button. The header
  totals, then the extracted text.

### 4. The source strip, on every layer

Under each layer's header: the source's type badge, name, and what it is (deck ·
5 slides, 12 pages, 3,400 words). Shown from Extraction onward, once.

### 5. Assets & Design

- **Extracted assets:** the "Handed on by Extraction" file list goes (the source
  strip says it). No per-file boxes: the pictures are one grid, ordered by slide.
- **Look:** "Start from" is two choices: **the deck's styling** or **the
  renderer's own look**. No list of files.
- **Final:** pictures are named by slide only.

### 6. Scene Plan, Script & Staging, Generation, flags

- Plan: the Brief's document list goes; a section's source reads "Slide 3" or
  "§ Heading"; the section editor's source list has no file groups; the plan bar
  and draft panel stop counting documents.
- Generation: a slide shot reads "Slide 3", not "Slide 3 of deck.pptx".
- Change flags: "slide 4", not "slide 4 of deck.pptx". Replacing the file says
  "The source file was replaced".

### 7. Docs and tests

- Each SOP touched says one source; the system map says so as an invariant.
- Tests: one file per upload; replace needs `replace`; extraction replaces the
  result; old projects read unchanged; every page drawn with no file names in it
  except the strip.

## Order

1 → 2 → 3 → 4 → 5 → 6 → 7, each checked in a browser on a throwaway copy, and
the full suite green before the next.
