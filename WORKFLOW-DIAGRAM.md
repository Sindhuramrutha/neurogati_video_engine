# Workflow diagram

How a project moves from one source file to a finished video: what each layer
takes in, what it does, and what it hands on. This is a working draft, written
to be edited into the project's direction.

**How to read it**

- A box is a layer. Inside it are the actions it takes, in order, and at its
  foot what it hands on.
- **(AI)** marks an action that calls a model. Everything else is a fixed rule
  or a person's choice.
- A thick arrow is a **transfer**, labelled with what is handed on. A layer
  reads only what was transferred, never what is still being worked on.
- The two boxes at the foot run across every layer: change flags going down,
  and feedback going back.

```mermaid
flowchart TD
    %% ---------------------------------------------------------------- the layers

    subgraph INPUTS["1 · Inputs"]
        direction TB
        I1["Upload ONE source file<br/>deck · PDF · Word · Markdown · text"]
        I2["Preview it · Replace it · Remove it"]
        I3[/"sources/ — the one file"/]
        I1 --> I2 --> I3
    end

    subgraph EXTRACTION["2 · Extraction"]
        direction TB
        E1["Extract: read text, headings, tables, figures,<br/>slide layout, backgrounds, styling<br/>handwriting OCR is optional (AI)"]
        E2["Review slide by slide<br/>fixed picture checks<br/>agent proposes fixes (AI) — you apply or discard"]
        E3[/"Transfer → the extraction"/]
        E1 --> E2 --> E3
    end

    subgraph ASSETS["3 · Assets & Design"]
        direction TB
        A1["Extracted assets: gather every picture by slide<br/>trim plain borders · flag cut crops<br/>you leave out what you don't want"]
        A2["Brand assets: watermark · logo · intro · outro<br/>placed, sized, timed, trimmed, cross-faded"]
        A3["Look: the deck's styling or the renderer's own<br/>theme · colours · fonts · background art"]
        A4[/"Transfer → pictures · brand kit · look"/]
        A1 --> A2 --> A3 --> A4
    end

    subgraph PLAN["4 · Scene Plan"]
        direction TB
        P1["Brief: audience · learning objectives<br/>lesson frame · target length · tone · language"]
        P2["Build the outline by an approach<br/>follow the deck (rule) · group into ideas ·<br/>story first · concept first · question led (AI draft)"]
        P3["Shape the lesson: Opening · Teach · Story · Recap · Close<br/>time shared from the target · objective links suggested<br/>one-line summaries (AI, proposals)"]
        P4["Fixed checks"]
        P5[/"Transfer → the plan"/]
        P1 --> P2 --> P3 --> P4 --> P5
    end

    subgraph SCRIPT["5 · Script & Staging"]
        direction TB
        S1["Write each section as scenes (AI)<br/>narration in the teacher's own voice<br/>+ what is on screen while it is said"]
        S2["Edit by hand · redraft a section (AI)"]
        S3["Fixed checks: every section written,<br/>length fits, teacher's voice, variables"]
        S4[/"Transfer → the script"/]
        S1 --> S2 --> S3 --> S4
    end

    subgraph GENERATION["6 · Generation"]
        direction TB
        G1["Decide each scene's shot by fixed rules<br/>the deck's slide › a source picture › a chart ›<br/>a drawn picture (AI) › words on screen"]
        G2["Or a scripted scene: the agent writes scene.py (AI)<br/>it is run, and 8 fixed checks decide if its clip is used"]
        G3["Make: on-screen words (AI) · pictures · diagrams · charts"]
        G4["Fixed checks"]
        G5[/"Transfer → frozen shots"/]
        G1 --> G2 --> G3 --> G4 --> G5
    end

    subgraph RENDER["7 · Render"]
        direction TB
        R1["Speak the narration (text-to-speech)<br/>the audio is the clock"]
        R2["Cut every shot to its narration · join the sections<br/>subtitles · timeline · chapters"]
        R3["Brand pass: logo · watermark · intro · outro"]
        R4["A queue: halt · continue · discard"]
        R5[/"A video version: .mp4 + subtitles"/]
        R1 --> R2 --> R3 --> R4 --> R5
    end

    subgraph STUDIO["8 · Studio"]
        direction TB
        T1["The timeline the render built<br/>viewer · inspector · tracks"]
        T2["Edit clips by hand · render again"]
        T1 --> T2
    end

    subgraph REVIEW["9 · Reviewing"]
        direction TB
        V1["Watch each version · chapters · transcript"]
        V2["Comment at a moment<br/>each comment is routed to the layer that can fix it"]
        V1 --> V2
    end

    subgraph EXPORT["10 · Export"]
        direction TB
        X1["The video and what travels with it<br/>transcript · chapters · subtitles · description"]
        X2[/"export/ — files to hand over"/]
        X1 --> X2
    end

    %% ------------------------------------------------- the spine, in the app's order
    %% A thick arrow is a transfer: the next layer reads only what was handed on.
    INPUTS == "the source file" ==> EXTRACTION
    EXTRACTION == "the extraction" ==> ASSETS
    ASSETS ~~~ PLAN
    EXTRACTION == "the extraction" ==> PLAN
    PLAN == "the plan" ==> SCRIPT
    SCRIPT == "the script" ==> GENERATION
    ASSETS == "pictures · brand kit · look" ==> GENERATION
    GENERATION == "frozen shots · the script" ==> RENDER
    RENDER == "a video version" ==> STUDIO
    RENDER == "a video version" ==> REVIEW
    RENDER == "a video version" ==> EXPORT

    %% ------------------------------------------- what runs across every layer
    subgraph ACROSS["Across every layer"]
        direction TB
        FLAGS{{"Change flags<br/>when a layer is transferred again,<br/>every layer after it is marked out of date<br/>and names the slides or sections that changed"}}
        BACK{{"Feedback<br/>a review comment is routed back<br/>to the layer that can fix it ·<br/>Studio edits go back to Render"}}
    end
    EXPORT ~~~ ACROSS

    %% ---------------------------------------------------------------- colours
    classDef ai fill:#FFF4C9,stroke:#9A5B00,color:#1A1816
    classDef out fill:#D7F7EA,stroke:#0F7A4F,color:#1A1816
    classDef flag fill:#FFE0E0,stroke:#D92D20,color:#1A1816
    class E2,P2,P3,S1,S2,G2,G3 ai
    class I3,E3,A4,P5,S4,G5,R5,X2 out
    class FLAGS,BACK flag
```

## The rules every layer keeps

| Rule | What it means |
|---|---|
| One source file | A project is made from one file. It runs through every layer. Replacing it keeps later work and flags it out of date. |
| Transfer to hand on | A layer's work reaches the next layer only when it is transferred. A failing check blocks the transfer. |
| AI proposes, a person decides | Every AI action produces a proposal or a draft, said in advance with how many model calls it costs. Nothing changes until it is accepted. |
| Fixed checks | Each layer's checks are fixed rules: the same work always gets the same results. |
| Audio is the clock | The render measures the spoken narration and cuts every picture, subtitle and chapter to it. |
| Nothing hidden | What a layer did to anything (trimmed a picture, flagged a crop, skipped a scene) is said on the page, with why. |

## Where each layer's work is kept

| Layer | Working copy | What it transfers |
|---|---|---|
| Inputs | `sources/` | — |
| Extraction | `extraction/collection.json` | `extraction/content.json` |
| Assets & Design | `assets/library.json`, `brand.json` | `assets/library.confirmed.json` |
| Scene Plan | `scene-plan/plan.json` | `scene-plan/plan.transferred.json` (after the first transfer) |
| Script & Staging | `script-staging/script.json` | `script-staging/script.transferred.json` (after the first transfer) |
| Generation | `generation/visuals.json`, `generation/scenes/` | `generation/visuals.transferred.json` (after the first transfer) |
| Render | `reviewing/output/render-job.json` | a video version in `reviewing/output/` |
| Studio | `studio/composition.json` | — |
| Reviewing | `reviewing/review.json` | — |
| Export | — | `export/manifest.json` |
