# Video quality plan

From "mid" to a video a learner would choose to watch: what quality means for
this product, where the output stands today (measured), why it falls short, and
the work that closes the gap, in order.

Written 13 Oct 2026, after two generation trials on slides 9–11 of
*Demystifying the Brain, Chapter 1* ("The Spark, the Physics, and the Chemical
Signal", 7 scenes, ~5 minutes).

---

## 1. What a good video is

A good explainer video does three things, and fails if it misses any one:

1. **It teaches.** A learner who has never met the topic can repeat the
   section's idea afterwards. Every picture on screen is *about* the sentence
   being spoken at that moment.
2. **It looks finished.** Nothing overlaps, nothing is cut off, nothing is
   crude. It looks like one designed course, not 60 scenes made by 60 different
   people.
3. **It can be trusted.** Every fact, name, date and drawing matches the source.
   A frog's heart is a frog's heart.

Everything below serves those three. When two goals conflict, the order is:
**correct > clear > finished > fast > cheap.**

---

## 2. Where the output stands (measured)

| | 10 Oct run (old code) | Trial 1 (13 Oct) | Trial 2 (13 Oct) |
|---|---|---|---|
| Scenes | 57 planned, 8 made | 7 | 7 |
| Rounds used per scene | median 6 of 6 | 6 of 6, every scene | 6 of 6, every scene |
| Passed every check | 6 of 8 (one visibly broken) | 3 of 7 | 2 of 7 |
| Reviewer called it "good" | — | 0 of 7 | 0 of 7 |
| Shows a slide picture | rarely | 7 of 7 (same one in each) | 7 of 7 (its own slide's) |
| Painted illustration | — | 0 | 4 of 7 |
| Time for 7 scenes | — | 13.4 min | 13.7 min |
| Model calls | ~6 + 1–2 vision per scene | 42 + 49 vision | 44 + 52 vision + 4 images |
| Prompt tokens | ~70k per scene | 665k | 654k |

**What got better** (seen in the frames): the script now teaches (questions,
defined terms, one idea per sentence, a takeaway); briefs say what to draw; the
deck's own look and pictures are used; the four painted illustrations (frog's
leg, Voltaic pile, two hearts in beakers, pipette) are far beyond shapes drawn
in code.

**What is still mid** (seen in the frames):

- Scenes without an illustration are stick lines and circles with labels
  crossed by lines.
- Labels float away from what they name; arrows start on their own labels.
- A painted illustration sits in a visible off-white panel on the white frame.
- An illustration was wrong (human hearts for frog hearts) and nothing caught it.
- No scene reached "good"; every scene spends all 6 rounds. The rounds go to
  fixing layout collisions, not to teaching.
- At this rate a 45-minute video is ~65 scenes, ~2 hours and ~6M prompt tokens.

---

## 3. Why it is mid: root causes

These are the causes behind the symptoms, most important first.

1. **Every scene is designed from scratch.** A model writes a fresh program for
   each scene and places every box, label and arrow by coordinates. There is no
   visual system, so 60 scenes are 60 one-offs. Free-form layout by a text model
   is what fails the checks over and over; rounds are spent on geometry.
2. **The model cannot draw.** Manim primitives give ellipses and stick figures.
   Painted illustrations fix this, but only where the script asks, and they are
   not checked.
3. **The expensive work happens before anyone looks.** A scene is written,
   rendered and refined six times before a person sees a single frame. A wrong
   direction (wrong picture, wrong layout idea) costs six rounds to discover.
4. **The quality judge is weak and late.** Fixed checks sample only the moments
   the scene pauses on. The vision reviewer judges everything at once, accepts
   cluttered frames, missed the wrong heart, and never says "good".
5. **The finish is thin.** One US voice with no pacing control, no pauses after
   key points, no music bed, no designed transitions between scenes, mono 24 kHz
   audio, sidecar-only captions.

The plan answers each one: a **design system and shot templates** (1),
**illustration as a first-class asset** (2), a **storyboard gate** before
animation (3), a **real quality judge** (4), and a **finishing pass** (5).

---

## 4. Product design approach

How a production studio would run this, translated into the pipeline.

- **Decide the look once, per course, before making anything.** A studio makes a
  *style frame*: palette, type, illustration style, layout grid. Everything after
  follows it. Here: the Look step produces a style guide that every scene reads.
- **Use a shot vocabulary, not a blank canvas.** Studios have 8–12 shot types
  they reuse with polish (hero illustration with callouts, A-vs-B comparison,
  step-by-step process, timeline, person intro...). Here: a library of tested
  scene templates; the model chooses one and fills its slots. Free-form code is
  the exception.
- **Storyboard before animation.** A storyboard frame costs seconds; an animated
  scene costs minutes. Here: one key frame per scene, approved by a person per
  section, before any scene is animated.
- **Pictures carry the idea; words label it.** At most five short labels, each
  touching what it names. If a frame would read the same as a slide, it is not
  finished.
- **Motion has meaning.** Every movement answers "what changed?": something is
  added, connected, compared, highlighted or transformed on the word that says
  so. No decoration.
- **Sound is half the video.** A clear, well-paced voice with breathing room is
  worth more than any visual polish.
- **Judge with a rubric, measure on a fixed test set.** Every change is checked
  on the same sections before and after. Quality is a number we track, not a
  feeling.

---

## 5. The quality rubric

Every scene is scored 1–5 on each line by the vision judge (and spot-checked by
a person). **Ship bar: no line below 3, and teaching + accuracy at 4 or more.**

| # | Dimension | 5 looks like | How it is measured |
|---|---|---|---|
| 1 | **Teaches the sentence** | The picture shows what is being said, when it is said | Judge, frames + narration with timings |
| 2 | **Accuracy** | Every drawn thing, label, name, date matches the source | Judge vs source text; illustration check at paint time |
| 3 | **Illustration** | A real, clear picture of the subject, in the course's style | Judge |
| 4 | **Composition** | One focal point, balanced, uses the frame, clear hierarchy | Fixed checks (fills, collide) + judge |
| 5 | **Typography & labels** | ≤5 labels, each next to what it names, readable, consistent sizes | Fixed checks (bounds, overlap, size, crossing) + judge |
| 6 | **Motion** | Builds on the words; things move, connect, compare | Fixed check (motion) + judge |
| 7 | **Consistency** | Same palette, type, illustration style as the rest of the video | Judge with the style frame beside it |
| 8 | **Voice & pacing** | Natural, clear, pauses after key points, names said right | Person (spot check) + pronunciation list |
| 9 | **Sync** | Each beat lands within ~0.3 s of its words | Word timings vs animation log |
| 10 | **Finish** | No artefacts, clean transitions, levelled audio, captions right | Fixed checks on the final render |

The judge returns scores *and* one concrete fix per line below 4. Scores are
recorded per scene, so a section's quality can be read at a glance on the
Generation page.

---

## 6. The work

Six workstreams, in the order they should land. Each item has a **done when**
line so it can be verified, not just merged.

### A. Fix what the trials exposed (next, ~1–2 days)

The five fixes already agreed, with how each is done and checked.

**A1. Check the whole animation, not only the pauses.**
Record what is on screen after every `play()`, not only at `until()`. Arrows
drawn and removed between beats are then checked too. Keep the snapshot cheap:
reuse the outline traces, skip snapshots closer than 0.25 s apart.
*Done when:* a test scene that flashes an arrow through a label between two
beats fails "No shape runs through words"; render time grows by under 10%.

**A2. Check each illustration once, when it is painted.**
One vision call compares the picture with what was asked ("two *frog* hearts in
beakers, the left one with its vagus nerve") and the narration. If it is wrong
(wrong subject, wrong species, impossible apparatus, any text in it), repaint
once with the judge's correction added to the prompt. Keep the verdict beside
the picture.
*Done when:* the trial 2 "human hearts" request is flagged and repainted; a
correct picture costs exactly one extra vision call.

**A3. Illustrate more freely.**
The script rule becomes: paint unless an offered slide picture already shows
the thing. Abstract ideas get a concrete picture too (a "law of specific
energies" becomes the same spark on two different nerves, one to the eye and one
to the ear). Cap: one illustration per scene.
*Done when:* on the test section, every scene has a picture (slide or painted)
as its main subject.

**A4. Blend the painted background into the frame.**
After painting, replace the near-background border region (flood from the
corners, tolerance ~12/255) with the exact frame colour, then soften the edge.
*Done when:* no visible panel edge on a white or dark frame (pixel check on the
border of the placed picture).

**A5. Labels next to what they name.**
A kit helper `self.callout(text, target_point, side)` places a label beside a
point on the picture with a short leader line that starts at the label's edge
and ends at the point — never starting inside the label, never crossing other
labels. Prompt rule: every label on a picture is a callout.
*Done when:* on the test section, no arrow starts on its own label and every
label is within ~150 px of its target.

### B. Art direction and a design system (~1 week)

The biggest single lever on "looks finished" and "consistent".

**B1. A style frame per project.** The Look step (Assets & Design) produces a
style guide the whole video uses:

- **Palette roles:** background, surface, ink, muted ink, 1 primary accent, 2
  secondary accents, 1 highlight — from the deck, checked for contrast and for
  colour-blind safety.
- **Type scale:** title 64, heading 48, label 36, caption 30 (px at 1080p), one
  font pair from the deck. Kit helpers use the scale; free sizes are not
  offered.
- **Layout grid:** 12 columns, 96 px margins, a fixed title zone, a fixed
  caption zone kept clear for subtitles.
- **Illustration style:** one written style ("flat, soft-shaded, rounded
  shapes, thin dark outlines, limited palette") plus one reference picture
  painted first and shown to the image model with every later request, so all
  illustrations look like one artist drew them.

The person sees and approves the style frame (one rendered sample frame) before
generation.
*Done when:* every illustration in the test section is visibly the same style;
the judge's consistency score averages 4 or more.

**B2. Motion grammar.** A short set of named moves with fixed timings, in the
kit: `reveal` (fade + 12 px rise, 0.4 s), `draw` (stroke, 0.6–1.0 s), `connect`
(grow arrow, 0.5 s), `focus` (dim the rest to 35%, scale target 1.06, 0.4 s),
`swap` (transform, 0.6 s), `count` (number roll). Easing is the same everywhere.
Scenes use these instead of hand-tuned animations.

### C. Shot templates (~1–2 weeks)

Replace "write a program from scratch" with "choose a shot, fill its slots".

**C1. The template library** (each a tested kit function with slots, layout and
motion built in, passing every check by construction):

| Shot | Use it for | Slots |
|---|---|---|
| Hero + callouts | A thing to look at (an apparatus, an organ, an experiment) | picture, up to 5 callouts with targets and timings |
| Experiment steps | Set-up → do → observe → conclude | picture per step or one picture with step states, step labels |
| A vs B | Two views, two results, before/after | two pictures or icons, two labels, the difference |
| Process / flow | Something causes something | 3–5 steps, connectors, optional picture per step |
| Timeline | Things in order | 3–7 events with dates/names, optional picture each |
| Person | Introduce a scientist | portrait (slide picture or painted), name, one-line contribution |
| Concept map | One idea and its parts | centre, up to 6 parts |
| Key idea | A takeaway or definition | one big statement, one supporting picture |
| Chart | Numbers from the source | data, axis labels, highlight |
| Section card | Opening a section | title, one picture, chapter number |

**C2. The scene model's job changes.** It picks a template, fills the slots
from the brief, and times the beats to the words. It writes free-form code only
when no template fits, and says why. Rounds then go to content, not geometry.

*Done when:* ≥80% of test scenes use a template; template scenes pass all
fixed checks in round 1; average rounds per scene falls from 6 to ≤3.

### D. Storyboard gate (~3–4 days)

**D1. A key frame per scene before animation.** For each scene: template,
picture (slide or painted), labels, laid out as a still. Cheap: no animation, no
refinement rounds, one render.

**D2. Approve per section.** The Generation page shows a section as a strip of
key frames with the narration under each. The person approves, or says what to
change for one frame ("use the Volta portrait", "show the frog leg larger").
Only approved storyboards are animated.

*Done when:* a whole section's storyboard is ready in under 2 minutes; changes
asked at the storyboard cost no animation rounds.

### E. Script and voice (~1 week)

**E1. Keep the new script rules** (taught to a first-time learner, briefs in a
fixed shape, scene lengths as targets) and add:

- **A fidelity pass:** one call compares each scene's narration with its source
  and lists any claim not supported (trial 1's "not a special animal
  electricity at all" was an inference).
- **A reading-level check:** average sentence length ≤ 18 words; every term the
  glossary lists is defined on first use.

**E2. Voice.**

- Choose the voice per course (accent, gender, pace); preview 3 voices on one
  paragraph before rendering. *Decision needed: US, British or Indian English?*
- Pronunciation list per project (Müller, Du Bois-Reymond, Loewi, Helmholtz,
  Galvani, vagus), applied by phoneme or respelling.
- Pauses: 0.4 s after a key sentence, 0.8 s between scenes, 1.2 s at a section
  change. Speaking rate ~150 words a minute, adjustable.

### F. Finishing: edit, sound, captions, delivery (~1 week)

**F1. Edit and pacing.**

- Scene-to-scene transitions follow meaning: a cut inside a topic, a short
  dissolve (0.4 s) at a topic change, the section card at a section change.
- Hold the last frame of a scene ~0.5 s before cutting, so a learner can read
  it.
- A small, persistent chapter indicator (section name, progress) in a corner.

**F2. Sound.**

- Final mix at 48 kHz stereo (today: 24 kHz mono), AAC 192 kbps.
- Loudness −16 LUFS integrated, −1.5 dBTP (kept from today), voice cleaned
  (high-pass ~80 Hz, gentle compression, de-ess).
- Optional music bed, very quiet (about −28 LUFS under the voice) and ducked
  further while the voice speaks; off by default. *Decision needed.*

**F3. Captions.**

- At most 42 characters a line, 2 lines, ≤ 17 characters a second, split on
  phrase boundaries, timed to word timings.
- Sidecar SRT/VTT always; burned-in optional for social cuts. *Decision needed.*

**F4. Delivery encode.** x264 `-crf 18 -preset slow` for the final (today:
default quality, `veryfast`), `+faststart`, chapter marks embedded, a thumbnail
from the section card.

### G. Quality judge and measurement (runs alongside everything above)

**G1. Rubric judge.** Replace the reviewer's yes/no with the rubric in section
5: scores per dimension, a fix for each low score, "good" meaning the ship bar is
met. The refinement loop then targets the lowest score first.

**G2. A fixed test set.** Three sections that stress different things: slides
9–11 (people and experiments), slides 15–16 (anatomy), slides 19–20
(behaviour, abstract ideas). Run after every workstream lands. Track: rubric
averages, % meeting the ship bar, rounds, minutes, tokens, images, and a human
1–5 rating of the finished section video.

**G3. Video-level review.** After the render, the judge watches the assembled
section (sampled frames across scene boundaries) for consistency, pacing and
continuity: the things no single scene can show.

---

## 7. Targets

| Measure | Today (trial 2) | After A | After A–D | After all |
|---|---|---|---|---|
| Scenes meeting the ship bar | 0 of 7 | 2–3 of 7 | 5 of 7 | ≥ 6 of 7 |
| Rounds per scene | 6 | 5 | ≤ 3 | ≤ 2.5 |
| Minutes per 7 scenes | 13.7 | ~13 | ~8 | ~7 |
| Prompt tokens per scene | ~93k | ~90k | ≤ 45k | ≤ 40k |
| Scenes with a real picture as subject | 7 of 7 (4 painted) | 7 of 7 | 7 of 7, one style | same |
| Human rating of the section video | — (est. 2/5) | 3/5 | 4/5 | 4.5/5 |

The cost targets come mostly from templates (fewer rounds) and the storyboard
gate (wrong directions caught before animation).

---

## 8. Order and timing

1. **A** (trial fixes): now. Re-run the test section to confirm.
2. **G1 + G2** (judge and test set): with A, so every later step is measured.
3. **B** (style frame) → **C** (templates): the core of "looks finished".
4. **D** (storyboard gate): once templates exist, a key frame is just a
   template's last frame.
5. **E** (script, voice) and **F** (finishing): in parallel with C/D; they do
   not depend on them.

Re-run the test set after each step; do not start the next until the numbers
moved.

---

## 9. Decisions needed

| Decision | Options | Recommendation |
|---|---|---|
| Narration accent | US / British / Indian English | Indian English (en-IN) if the learners are in India |
| Music bed | none / quiet ducked bed | none by default; a per-course switch |
| Captions | sidecar only / also burned-in | sidecar; burned-in only for social clips |
| Storyboard gate | required / optional | required for the first section of a course, optional after |
| Template coverage | strict (templates only) / templates first | templates first, free-form allowed with a reason |
| Illustration budget | per scene / per section cap | at most one per scene, reused across scenes where the same thing appears |

---

## 10. Risks

- **Painted pictures can be wrong.** Mitigated by A2 (check at paint time) and
  the accuracy line of the rubric; a person still approves the storyboard.
- **Templates can make videos look samey.** Mitigated by 10 shot types, the
  course's own pictures and illustrations, and per-template variation (layout
  mirroring, emphasis styles).
- **The judge is a model too.** Its scores are checked against human ratings
  on the test set; if they disagree, the rubric wording is tuned before trusting
  it.
- **Cost grows with images and judge calls.** Offset by fewer rounds; tracked on
  the test set.
