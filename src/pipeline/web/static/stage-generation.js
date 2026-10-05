/**
 * Generation — five tabs, in the order the work happens.
 *
 * 1. Setup: what came in (the transferred script and assets), what this machine
 *    can draw, and the rules that decide each scene's shot.
 * 2. Decide: what every scene shows and how it moves. Fixed rules, no model;
 *    change any scene by hand.
 * 3. Make: produce it. Says in advance which scenes will call a model (the
 *    words on screen, drawn pictures) and which are made by local code.
 * 4. Check: fixed rules over the shots, each pass / warn / fail with why.
 * 5. Final & transfer: the render reads the transferred shots, frozen so that
 *    making a scene again cannot change them (`generation_handoff.py`).
 *
 * One card per scene, in the order they are spoken, each showing the picture
 * that will actually be on screen and the few words that will be on it. That is
 * the point of the page: the brief was a sentence nobody could check, and a
 * thumbnail with its headline is a claim you can see.
 *
 * The narration is deliberately not shown as on-screen text anywhere here. It
 * is what the scene *says*; the headline and labels are what it *shows*, and the
 * whole stage exists to keep those two apart.
 */

import {
  loadOpenScene, markOneScripted, renderResourceLibrary, renderScenePanel, renderScriptedBar,
  sceneLabState, scenePosterUrl, wireSceneLab,
} from "/static/scene-lab.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, footerNav, hideProgress, icon, moveToNextLayerButton,
  projectApiPath, refreshProjectSummary, select, showProgress, showStageNotice, stageHeader,
  stageNeighbours, whenItWas, wireGotoButtons,
} from "/static/ui-kit.js";

const GENERATION_TABS = [
  ["setup", "Setup"], ["decide", "Decide"], ["make", "Make"], ["check", "Check"],
  ["final", "Final & transfer"],
];

const currentGenerationTab = () =>
  GENERATION_TABS.some(([key]) => key === applicationState.generationTab)
    ? applicationState.generationTab : "setup";

const CHECK_LABELS = { pass: "Pass", warn: "Warning", fail: "Fails", "n/a": "Not applicable" };

const generationViewState = {
  filter: "all",   // all | needs-building | from-source | diagrams | generated | words
};

const FILTERS = [
  ["all", "Every scene"],
  ["needs-building", "Not made yet"],
  ["slides", "Slides"],
  ["from-source", "From the source"],
  ["diagrams", "Diagrams"],
  ["generated", "Drawn"],
  ["scripted", "Scripted"],
  ["words", "Words only"],
];

const KIND_LABELS = {
  slide: "The deck's slide",
  source_picture: "From the source",
  chart: "Chart",
  diagram: "Diagram",
  generated_image: "Drawn",
  text: "Words only",
  scripted: "A scripted scene",
};

/** The shapes a scene can be drawn as, in the words a person would use. */
const DIAGRAM_LABELS = {
  flow: "a sequence",
  compare: "a comparison",
  stack: "layers",
  cycle: "a loop",
  tree: "a hierarchy",
  graph: "a network",
  plot: "a curve",
  bars: "bars",
  timeline: "a timeline",
  table: "a table",
  counter: "a counting number",
  formula: "a formula",
  figure: "the source's own figure",
  morph: "one thing becoming another",
  code: "code",
};

const MOTION_LABELS = {
  hold: "Still",
  push_in: "Push in",
  pull_back: "Pull back",
  pan_right: "Pan right",
  pan_left: "Pan left",
};

const matches = visual => ({
  all: true,
  "needs-building": !visual.is_built || visual.is_stale,
  slides: visual.kind === "slide",
  "from-source": visual.kind === "source_picture",
  diagrams: visual.kind === "diagram",
  generated: visual.kind === "generated_image" || visual.kind === "chart",
  scripted: visual.kind === "scripted",
  words: visual.kind === "text",
}[generationViewState.filter]);

/**
 * Assets live in three places, and a thumbnail has to come from the same file
 * the video will draw.
 *
 * `generation/` is what this stage made. `assets/prepared/` is a source figure
 * with its slide background trimmed off, which is what the renderer uses --
 * pointing a thumbnail at the untrimmed original instead showed a picture the
 * render would not use, and pointing it at the extraction folder 404s.
 */
const pictureUrl = assetPath => {
  const name = encodeURIComponent(assetPath.split("/").pop());
  if (assetPath.startsWith("generation/slides/")) {
    return projectApiPath(`/visuals/slides/${name}`);
  }
  if (assetPath.startsWith("generation/")) {
    return projectApiPath(`/visuals/assets/${name}`);
  }
  if (assetPath.startsWith("assets/prepared/")) {
    return projectApiPath(`/assets/prepared/${name}`);
  }
  return projectApiPath(`/extraction/assets/${name}`);
};

export async function renderGenerationStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  if (!body.querySelector(".generation-tabs")) {
    body.innerHTML = `<div class="card muted">Loading the shots…</div>`;
  }

  let visuals;
  let handoff;
  try {
    [visuals, handoff] = await Promise.all([
      requestJsonFromApi(projectApiPath("/visuals")),
      requestJsonFromApi(projectApiPath("/visuals/handoff")),
    ]);
  } catch (loadFailure) {
    console.error("visuals load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load what each scene shows.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }
  applicationState.sceneVisuals = visuals;

  // What can be animated here is a property of the machine, not of the project,
  // so a failure to read it costs the panel and not the page.
  let renderers = null;
  try {
    renderers = await requestJsonFromApi("/api/scene-renderers");
  } catch (rendererFailure) {
    console.error("scene renderers load failed", rendererFailure);
  }

  // The resource library is the machine's, like the renderers; the open scene is
  // one scene's folder. Either failing costs its panel, not the page.
  let resources = null;
  try {
    resources = await requestJsonFromApi("/api/resources");
  } catch (resourceFailure) {
    console.error("resource library load failed", resourceFailure);
  }
  const openScene = await loadOpenScene();

  const tab = currentGenerationTab();
  const content = {
    setup: () => renderSetup(visuals, handoff, renderers) + renderResourceLibrary(resources),
    decide: () => renderDecide(visuals),
    make: () => renderMake(visuals, handoff, openScene),
    check: () => renderGenerationChecks(handoff),
    final: () => renderGenerationFinal(visuals, handoff, stage),
  }[tab]();

  body.innerHTML = `
    ${stageHeader("generation", "Generation", { agentButtonId: "generation-agent-button" })}
    <div class="stage-content stage-content-bare">
      <div class="extraction-tabs plan-tabs generation-tabs">
        <nav class="x-tabs" role="tablist" aria-label="Generation steps">
          ${GENERATION_TABS.map(([key, label], index) => `
            <button role="tab" class="x-tab ${key === tab ? "on" : ""}" data-generation-tab="${key}"
                    aria-selected="${key === tab}">
              <span class="x-tab-number">${index + 1}</span>
              <b class="x-tab-label">${label}</b>
              ${key === "check" && handoff.failing ? `<span class="plan-tab-count fail">${handoff.failing}</span>`
                : key === "check" && handoff.warning ? `<span class="plan-tab-count warn">${handoff.warning}</span>` : ""}
            </button>`).join("")}
        </nav>
        <div class="x-tab-body" role="tabpanel">${content}</div>
      </div>
      ${renderGenerationFooter(stage, handoff, tab)}
    </div>`;

  wireGenerationStage(stage, navigateToStage, renderAgentStage);
  wireSceneLab(() => renderGenerationStage(stage, navigateToStage, renderAgentStage), visuals);
}

/* ---- 1. Setup ---------------------------------------------------------------- */

function renderSetup(visuals, handoff, renderers) {
  const inputs = handoff.checks.filter(check => check.key === "script" || check.key === "assets");
  return `
    <div class="plan-brief">
      <section class="panel">
        <div class="panel-head"><h3>What came in</h3></div>
        <p class="panel-sub">Shots are decided from the transferred script (each scene's
          on-screen brief) and the pictures Assets &amp; Design transferred.</p>
        ${inputs.map(check => `
          <div class="assets-source-row">
            <span class="x-pick-name">${escapeHtml(check.name)}</span>
            <span class="plan-check ${check.status}">${CHECK_LABELS[check.status]}</span>
          </div>
          <p class="panel-sub">${escapeHtml(check.detail)}</p>`).join("")}
        ${renderPicturesHandedOn(handoff.pictures)}
      </section>
      <section class="panel">
        <div class="panel-head"><h3>How each scene's shot is decided</h3></div>
        <p class="panel-sub">The first that applies, in this order. The same script and
          pictures always give the same decisions.</p>
        <table class="assets-rule-table">
          <thead><tr><th>#</th><th>Shot</th><th>When</th><th>Made by</th></tr></thead>
          <tbody>
            ${handoff.rules.map((rule, index) => `
              <tr><td>${index + 1}</td><td><b>${escapeHtml(rule.name)}</b></td>
                <td>${escapeHtml(rule.when)}</td>
                <td>${rule.made_by.startsWith("AI") ? `<span class="fact warn">${escapeHtml(rule.made_by)}</span>`
                  : escapeHtml(rule.made_by)}</td></tr>`).join("")}
          </tbody>
        </table>
        <p class="assets-guarantee">A diagram can replace words or a drawn picture when the
          scene describes a sequence or a comparison — it is drawn from the scene's own
          terms, never from a model's impression.</p>
      </section>
    </div>
    <section class="panel" style="margin-top:16px">
      <div class="panel-head"><h3>What this machine can draw</h3></div>
      ${renderRendererPanel(renderers) || `<p class="muted">Could not read the renderers.</p>`}
    </section>`;
}

/** Which handed-on pictures can be a scene's picture. Judged here, where a
 *  picture is chosen for a scene; Assets & Design lists them and judges none. */
function renderPicturesHandedOn(pictures) {
  if (!pictures || !pictures.handed_on) return "";
  const cannot = pictures.cannot_fill_a_frame;
  return `
    <div class="assets-source-row">
      <span class="x-pick-name">Pictures handed on</span>
      <span class="file-status">${pictures.usable} of ${pictures.handed_on} can be a scene's picture</span>
    </div>
    ${cannot.length ? `
      <p class="panel-sub">A scene's picture has to be large and clear enough to fill a frame.
        ${cannot.length === 1 ? "This one is not" : `These ${cannot.length} are not`}, so no rule
        picks ${cannot.length === 1 ? "it" : "them"}:</p>
      <ul class="generation-unfit">${cannot.map(picture => `
        <li><b>${escapeHtml(picture.name)}</b>: ${escapeHtml(picture.why)}</li>`).join("")}</ul>`
      : `<p class="panel-sub">Every one is large and clear enough to fill a frame.</p>`}`;
}

/* ---- 2. Decide ------------------------------------------------------------------ */

function renderDecide(visuals) {
  const audit = visuals.audit;
  return `
    <div class="run-bar ${visuals.is_empty ? "blocked" : "ready"}">
      <span class="run-icon">${icon(visuals.is_empty ? ICON.alert : ICON.check, 17, 2.2)}</span>
      <span class="run-text">
        <b>${visuals.is_empty ? "Nothing decided yet" : `${audit.scene_count} scene(s) decided`}</b>
        <span>${visuals.is_empty ? "Decide what every scene shows. No model is called."
          : [audit.slides ? `${audit.slides} slide(s)` : "",
             audit.from_source ? `${audit.from_source} from the source` : "",
             audit.charts ? `${audit.charts} chart(s)` : "",
             audit.diagrams ? `${audit.diagrams} diagram(s)` : "",
             audit.generated ? `${audit.generated} to be drawn (AI)` : "",
             audit.words_only ? `${audit.words_only} words only` : ""].filter(Boolean).join(" · ")}</span>
      </span>
      <span class="plan-actions">
        <button class="btn btn-accent" id="plan-visuals-button"
                title="Apply the rules on the Setup tab to every scene. Scenes already decided and unchanged keep their shot.">
          ${visuals.is_empty ? "Decide what to show" : "Decide again"}</button>
        ${visuals.is_empty ? "" : `<button class="btn" id="script-every-scene-button"
            title="Every scene drawn by its own Python script, written by the agent">
          Script every scene</button>`}
      </span>
    </div>
    ${visuals.is_empty ? `
      <div class="empty">
        <h3>No scenes yet</h3>
        <p>Write the narration as scenes on Script &amp; Staging and transfer it, then
           decide what each one shows.</p>
        <button class="btn btn-accent" data-goto="script-staging">
          ${icon(ICON.arrowLeft)} Go to Script &amp; Staging</button>
      </div>` : `
      <section class="panel">
        <table class="assets-rule-table generation-decisions">
          <thead><tr><th>Scene</th><th>Shows</th><th>Why</th><th>Camera</th></tr></thead>
          <tbody>
            ${visuals.visuals.map(visual => `
              <tr>
                <td><b>${escapeHtml(visual.section_title)}</b> · scene ${visual.scene_number}
                  <div class="muted generation-brief">${escapeHtml(visual.brief || "No brief.")}</div></td>
                <td><select data-kind-for="${escapeHtml(visual.id)}" aria-label="What this scene shows">
                  ${Object.entries(KIND_LABELS).map(([key, label]) => `
                    <option value="${key}" ${visual.kind === key ? "selected" : ""}>${escapeHtml(label)}${
                      key === "generated_image" || key === "scripted" ? " (AI)" : ""}</option>`).join("")}
                </select></td>
                <td>${escapeHtml(visual.note || (visual.kind === "source_picture"
                  ? "A picture from this section's own source." : visual.kind === "generated_image"
                  ? "Nothing in the source for it; an image model will draw the brief." : ""))}</td>
                <td><select data-motion-for="${escapeHtml(visual.id)}" aria-label="How the camera moves">
                  ${Object.entries(MOTION_LABELS).map(([key, label]) => `
                    <option value="${key}" ${visual.motion === key ? "selected" : ""}>${escapeHtml(label)}</option>`).join("")}
                </select></td>
              </tr>`).join("")}
          </tbody>
        </table>
      </section>`}`;
}

/* ---- 3. Make ---------------------------------------------------------------------- */

function renderMake(visuals, handoff, openScene) {
  if (visuals.is_empty) {
    return `<div class="empty"><h3>Nothing to make yet</h3>
      <p>Decide what every scene shows first.</p>
      <button class="btn btn-accent" data-generation-tab="decide">Go to Decide</button></div>`;
  }
  const preview = handoff.make_preview;
  const shown = visuals.visuals.filter(matches);
  const line = (count, text, ai = false) => count
    ? `<li>${ai ? `<span class="fact warn">AI</span> ` : ""}${count} ${text}</li>` : "";
  return `
    <div class="run-bar ${preview.to_make ? "stale" : "ready"}">
      <span class="run-icon">${icon(preview.to_make ? ICON.alert : ICON.check, 17, 2.2)}</span>
      <span class="run-text">
        <b>${preview.to_make ? `${preview.to_make} scene(s) to make` : "Every scene is made"}</b>
        <span>${preview.to_make ? "What making will do, before anything is made or paid for:"
          : "Make again only after changing a scene or a decision."}</span>
        ${preview.to_make ? `<ul class="generation-preview">
          ${line(preview.ai_words, "scene(s) get their on-screen words composed by a model", true)}
          ${line(preview.ai_pictures, "picture(s) drawn by the image model", true)}
          ${line(preview.slides, "slide(s) composed from the deck")}
          ${line(preview.source_pictures, "picture(s) from the source prepared")}
          ${line(preview.charts, "chart(s) drawn from stated numbers")}
          ${line(preview.diagrams, "diagram(s) drawn locally")}
        </ul>` : ""}
      </span>
      <span class="plan-actions">
        <button class="btn btn-accent" id="build-visuals-button" ${preview.to_make ? "" : "disabled"}>
          Make what is missing</button>
        <button class="btn" id="rebuild-visuals-button"
                title="Make every scene again, including the ones already made">Make everything again</button>
      </span>
    </div>
    ${renderScriptedBar(preview)}
    ${renderScenePanel(openScene)}
    ${visuals.notes.length ? `<p class="muted edit-hint">${visuals.notes.map(escapeHtml).join(" · ")}</p>` : ""}
    ${renderFilters(visuals)}
    <div class="shot-grid">${shown.map(renderShot).join("")}</div>
    ${shown.length ? "" : `<p class="muted edit-hint">Nothing matches this filter.</p>`}`;
}

/* ---- 4. Check ---------------------------------------------------------------------- */

function renderGenerationChecks(handoff) {
  return `
    <section class="panel">
      <div class="panel-head"><h3>The checks the shots go through</h3></div>
      <p class="panel-sub">Fixed rules over the shots, the script and the assets. A failing
        check blocks the transfer; a warning is shown and allowed.</p>
      <table class="assets-rule-table plan-checks">
        <thead><tr><th>Result</th><th>Check</th><th>Rule</th><th>Found</th></tr></thead>
        <tbody>
          ${handoff.checks.map(check => `
            <tr>
              <td><span class="plan-check ${check.status === "n/a" ? "na" : check.status}">${
                CHECK_LABELS[check.status] ?? check.status}</span></td>
              <td><b>${escapeHtml(check.name)}</b></td>
              <td>${escapeHtml(check.rule)}</td>
              <td>${escapeHtml(check.detail)}</td>
            </tr>`).join("")}
        </tbody>
      </table>
    </section>`;
}

/* ---- 5. Final & transfer ------------------------------------------------------------- */

function renderGenerationFinal(visuals, handoff, stage) {
  const [tone, title, detail] = visuals.is_empty
    ? ["blocked", "Nothing to transfer yet", "Decide and make the shots first."]
    : handoff.failing
      ? ["stale", `${handoff.failing} check(s) fail`, "Fix them (see the Check tab), then transfer."]
      : !handoff.has_transferred
        ? ["pending", "Ready to transfer",
           "Nothing has been transferred yet, so the render reads the working shots."]
        : handoff.pending
          ? ["pending", "Ready to transfer",
             "This differs from what the render has. Transfer to hand it the changes."]
          : ["ready", "Transferred to the next layer",
             `The render has had exactly these shots since ${whenItWas(handoff.transferred_at)}.`];
  const canTransfer = !visuals.is_empty && !handoff.failing
    && (handoff.pending || !handoff.has_transferred);
  const audit = visuals.audit;
  return `
    <div class="final-head ${tone}">
      <span class="run-icon">${icon(tone === "ready" ? ICON.check : ICON.alert, 18, 2.3)}</span>
      <span class="run-text">
        <b>${escapeHtml(title)}</b>
        <span>${escapeHtml(detail)}</span>
        <span class="final-totals">${audit.scene_count} shot(s) · ${audit.generated} drawn by AI ·
          ${audit.moving} moving · ${handoff.warning} warning(s)</span>
      </span>
      ${tone === "ready" ? moveToNextLayerButton(stageNeighbours(stage).next, {
          carries: "The transferred shots go on to the render." })
        : `<button class="btn btn-accent btn-transfer" id="transfer-generation-button"
                   ${canTransfer ? "" : "disabled"}>
             Transfer to the next layer ${icon(ICON.arrowRight)}</button>`}
    </div>
    <p class="panel-sub">A transfer freezes every picture it points at, so making a scene
      again afterwards cannot change what the render shows until you transfer again.</p>
    <div class="assets-final-strip generation-final-strip">
      ${visuals.visuals.map(visual => visual.asset_path
        ? `<img alt="" loading="lazy" title="${escapeHtml(visual.section_title)} · scene ${visual.scene_number}"
               src="${pictureUrl(visual.asset_path)}">`
        : `<span class="generation-words-thumb" title="Words only">${escapeHtml(
            visual.headline || "—")}</span>`).join("")}
    </div>`;
}

function renderGenerationFooter(stage, handoff, tab) {
  const at = GENERATION_TABS.findIndex(([key]) => key === tab);
  const next = GENERATION_TABS[at + 1];
  return footerNav(stage, {
    end: next ? `
      <button class="btn btn-accent btn-move-next" data-generation-tab="${next[0]}">
        Move to ${next[1]} ${icon(ICON.arrowRight)}</button>` : null,
    next: {
      carries: handoff.has_transferred ? "The transferred shots go on to the render." : "",
      warning: !handoff.has_transferred
        ? "The shots have never been transferred: the render reads the working shots until "
          + "you transfer them on the Final & transfer tab."
        : handoff.pending
          ? "Your latest changes are not transferred — the render still uses the last "
            + "transferred shots."
          : "",
    },
  });
}

/**
 * What can draw a scene on this machine, and what is missing to do more.
 *
 * Shown rather than hidden. A project whose diagrams come out as stills because
 * nothing is installed should say so, with the one command that changes it --
 * and a renderer that is installed but fails here should say *that*, because the
 * two look identical in the finished video.
 */
function renderRendererPanel(renderers) {
  if (!renderers) return "";

  const drawable = renderers.drawable_kinds ?? [];
  const total = (renderers.kinds ?? []).length;
  const animators = (renderers.renderers ?? []).filter(
    renderer => (renderer.capabilities ?? []).includes("animated_diagram"));

  return `
    <details class="renderer-panel ${drawable.length ? "" : "flat"}">
      <summary>
        <span class="renderer-state">${drawable.length
          ? `${drawable.length} of ${total} scene kinds can be animated`
          : "Nothing here can animate a scene"}</span>
        <span class="muted">${drawable.length
          ? `drawn by ${escapeHtml([...new Set((renderers.kinds ?? [])
              .map(kind => kind.drawn_by).filter(Boolean))].join(", "))}`
          : "diagrams will be drawn as stills and held"}</span>
      </summary>

      <div class="renderer-list">
        ${animators.map(renderer => `
          <div class="renderer-row ${renderer.is_available ? "ok" : "off"}">
            <div class="renderer-head">
              <b>${escapeHtml(renderer.label)}</b>
              <span class="fact ${renderer.is_available ? "ok"
                : renderer.is_installed ? "bad" : "muted"}">${
                renderer.is_available ? "working"
                  : renderer.is_installed ? "installed, not working" : "not installed"}</span>
              <div class="spacer"></div>
              ${renderer.is_installed ? `
                <button class="btn" data-verify="${escapeHtml(renderer.key)}">
                  Verify ${escapeHtml(renderer.kinds.length)} kinds</button>` : ""}
            </div>
            <p class="muted">${escapeHtml(renderer.summary)}</p>
            ${renderer.is_installed ? "" : `
              <p class="renderer-install">Install with
                <code>${escapeHtml(renderer.install_command)}</code></p>`}
            ${renderer.self_test.checked && renderer.self_test.detail ? `
              <p class="renderer-detail">${escapeHtml(renderer.self_test.detail)}</p>` : ""}
            ${renderer.is_installed ? `
              <div class="renderer-kinds">
                ${renderer.kinds.map(kind => {
                  const proved = renderer.self_test.kinds?.[kind];
                  const state = !proved ? "unproved" : proved.ok ? "ok" : "bad";
                  const why = !proved ? "not verified yet"
                    : proved.ok ? "verified" : proved.detail;
                  return `<span class="kind ${state}" title="${escapeHtml(why)}"
                    >${escapeHtml(kind)}</span>`;
                }).join("")}
              </div>` : ""}
          </div>`).join("")}
      </div>

      <div class="renderer-kinds-all">
        ${(renderers.kinds ?? []).map(kind => `
          <span class="kind ${kind.is_drawable ? "ok" : "off"}"
                title="${escapeHtml(kind.describes)}${kind.drawn_by
                  ? ` — drawn by ${kind.drawn_by}` : " — nothing here draws this"}"
            >${escapeHtml(kind.kind)}</span>`).join("")}
      </div>
    </details>`;
}

function renderFilters(visuals) {
  const counts = {
    all: visuals.visuals.length,
    "needs-building": visuals.visuals.filter(v => !v.is_built || v.is_stale).length,
    slides: visuals.audit.slides ?? 0,
    "from-source": visuals.audit.from_source,
    diagrams: visuals.audit.diagrams ?? 0,
    generated: visuals.audit.generated + visuals.audit.charts,
    scripted: visuals.visuals.filter(v => v.kind === "scripted").length,
    words: visuals.audit.words_only,
  };
  return `
    <div class="seg asset-filters">
      ${FILTERS.map(([key, label]) => `
        <button class="${generationViewState.filter === key ? "on" : ""}" data-filter="${key}">
          ${escapeHtml(label)} <span class="mono">${counts[key] ?? 0}</span>
        </button>`).join("")}
    </div>`;
}

function renderShot(visual) {
  return `
    <div class="shot-card ${visual.is_stale ? "is-stale" : ""} ${visual.is_built ? "" : "unbuilt"}"
         data-visual="${escapeHtml(visual.id)}">
      <div class="shot-head">
        <span class="outline-num">${visual.scene_number}</span>
        <span class="fact ${visual.kind === "source_picture" ? "ok" : "muted"}"
          >${escapeHtml(KIND_LABELS[visual.kind] ?? visual.kind)}</span>
        <div class="spacer"></div>
        ${visual.is_stale ? `<span class="fact warn">scene rewritten</span>` : ""}
        ${visual.is_built ? "" : `<span class="fact bad">not made</span>`}
      </div>
      <span class="shot-section">${escapeHtml(visual.section_title)}</span>

      <div class="shot-frame">
        ${visual.asset_path
          ? `<img alt="" loading="lazy" src="${visual.kind === "scripted"
               ? scenePosterUrl(visual) : pictureUrl(visual.asset_path)}">`
          : `<span class="shot-words">${escapeHtml(
               visual.headline || "Nothing composed yet")}</span>`}
        ${visual.clip_path
          ? `<span class="shot-animated">animated by ${escapeHtml(visual.drawn_by)}</span>`
          : ""}
        <span class="shot-motion">${escapeHtml(MOTION_LABELS[visual.motion] ?? visual.motion)}</span>
      </div>

      <div class="shot-reads">
        <b class="shot-headline">${escapeHtml(visual.headline || "No headline yet")}</b>
        ${(visual.points ?? []).length
          ? `<ul class="shot-points">${visual.points.map(
               point => `<li>${escapeHtml(point)}</li>`).join("")}</ul>`
          : `<span class="muted">${visual.kind === "slide"
               ? `Slide ${visual.slide_number} of the deck, shown as its author made it.`
               : "No labels — the picture carries this one."}</span>`}
        ${visual.diagram
          ? `<span class="shot-diagram">Drawn as ${escapeHtml(
               DIAGRAM_LABELS[visual.diagram.kind] ?? visual.diagram.kind)}:
               ${escapeHtml((visual.diagram.nodes ?? []).join(" → "))}</span>`
          : ""}
      </div>

      <details class="shot-brief-detail">
        <summary>What the script asked for</summary>
        <p>${escapeHtml(visual.brief || "Nothing was written for this scene.")}</p>
      </details>
      ${visual.note ? `<span class="shot-note">${escapeHtml(visual.note)}</span>` : ""}

      ${visual.kind === "scripted" ? `<button class="btn btn-accent shot-open"
          data-open-scene="${escapeHtml(visual.id)}">${visual.is_built ? "Open the scene"
            : "Write its script"}</button>` : ""}
      <div class="shot-actions">
        <select data-kind-for="${escapeHtml(visual.id)}" aria-label="What this scene shows">
          ${Object.entries(KIND_LABELS).map(([key, label]) => `
            <option value="${key}" ${visual.kind === key ? "selected" : ""}
              >${escapeHtml(label)}</option>`).join("")}
        </select>
        <select data-motion-for="${escapeHtml(visual.id)}" aria-label="How the camera moves">
          ${Object.entries(MOTION_LABELS).map(([key, label]) => `
            <option value="${key}" ${visual.motion === key ? "selected" : ""}
              >${escapeHtml(label)}</option>`).join("")}
        </select>
      </div>

      ${visual.prompt ? `
        <details class="shot-prompt">
          <summary>What was asked for</summary>
          <pre>${escapeHtml(visual.prompt)}</pre>
        </details>` : ""}
    </div>`;
}

function wireGenerationStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderGenerationStage(stage, navigateToStage, renderAgentStage);

  wireGotoButtons(navigateToStage);
  select("#generation-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-generation-tab]").forEach(button => {
    button.onclick = async () => {
      applicationState.generationTab = button.dataset.generationTab;
      const fromFooter = Boolean(button.closest(".footer-nav"));
      await rerender();
      if (fromFooter) select(".x-tabs")?.scrollIntoView({ block: "start", behavior: "smooth" });
    };
  });
  document.querySelectorAll("[data-filter]").forEach(button => {
    button.onclick = () => {
      generationViewState.filter = button.dataset.filter;
      rerender();
    };
  });

  const planButton = select("#plan-visuals-button");
  if (planButton) {
    planButton.onclick = async () => {
      planButton.disabled = true;
      planButton.textContent = "Deciding…";
      try {
        const planned = await requestJsonFromApi(projectApiPath("/visuals/plan"), { method: "POST" });
        showStageNotice("ok", `${planned.audit.scene_count} scene(s) decided.`);
        await refreshProjectSummary();
      } catch (planFailure) {
        console.error("deciding visuals failed", planFailure);
        showStageNotice("bad", planFailure.message);
      }
      await rerender();
    };
  }

  const make = async (button, rebuild) => {
    if (rebuild && !window.confirm("Make every scene again? Scenes already made are made "
        + "again too, and model calls are made for them.")) return;
    button.disabled = true;
    button.textContent = "Making…";
    showProgress({ label: rebuild ? "Making every scene again" : "Making what is missing" });
    try {
      const built = await requestJsonFromApi(projectApiPath("/visuals/build"), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rebuild }),
      });
      showStageNotice(built.notes.length ? "warn" : "ok",
        `${built.built_ids.length} scene(s) made.` + (built.notes.length ? ` ${built.notes.join(" ")}` : ""));
      await refreshProjectSummary();
    } catch (buildFailure) {
      console.error("making visuals failed", buildFailure);
      showStageNotice("bad", buildFailure.message);
    } finally {
      hideProgress();
    }
    await rerender();
  };
  const build = select("#build-visuals-button");
  if (build && !build.disabled) build.onclick = () => make(build, false);
  const rebuild = select("#rebuild-visuals-button");
  if (rebuild) rebuild.onclick = () => make(rebuild, true);

  const transfer = select("#transfer-generation-button");
  if (transfer && !transfer.disabled) {
    transfer.onclick = async () => {
      transfer.disabled = true;
      try {
        await requestJsonFromApi(projectApiPath("/visuals/transfer"), { method: "POST" });
        showStageNotice("ok", "Transferred: the render uses exactly these shots, frozen.");
        await refreshProjectSummary();
      } catch (transferFailure) {
        console.error("transferring the shots failed", transferFailure);
        showStageNotice("bad", transferFailure.message);
      }
      await rerender();
    };
  }

  document.querySelectorAll("[data-verify]").forEach(button => {
    button.onclick = async () => {
      const key = button.dataset.verify;
      button.disabled = true;
      button.textContent = "Drawing…";
      try {
        const proved = await requestJsonFromApi(
          `/api/scene-renderers/${encodeURIComponent(key)}/verify`, { method: "POST" });
        showStageNotice(proved.ok ? "ok" : "bad",
          proved.ok
            ? `${key}: ${proved.drawable.length} kind(s) drawn in ${proved.seconds}s.`
              + (proved.detail ? ` ${proved.detail}` : "")
            : `${key} could not draw anything. ${proved.detail}`);
      } catch (verifyFailure) {
        console.error("verifying a renderer failed", verifyFailure);
        showStageNotice("bad", verifyFailure.message);
      }
      await rerender();
    };
  });

  document.querySelectorAll("[data-kind-for]").forEach(picker => {
    picker.onchange = async () => {
      if (picker.value !== "scripted") {
        if (sceneLabState.openId === picker.dataset.kindFor) sceneLabState.openId = null;
        return change(picker.dataset.kindFor, { kind: picker.value }, rerender);
      }
      // A scripted scene has its own path: it waits for a script, and opens on
      // the Make tab where that script is written.
      try {
        await markOneScripted(picker.dataset.kindFor);
        applicationState.generationTab = "make";
      } catch (markFailure) {
        showStageNotice("bad", markFailure.message);
      }
      return rerender();
    };
  });
  document.querySelectorAll("[data-motion-for]").forEach(picker => {
    picker.onchange = () => change(picker.dataset.motionFor, { motion: picker.value }, rerender);
  });
}

async function change(visualId, body, rerender) {
  try {
    applicationState.sceneVisuals = await requestJsonFromApi(
      projectApiPath(`/visuals/${encodeURIComponent(visualId)}`), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
  } catch (changeFailure) {
    console.error("changing the shot failed", changeFailure);
    showStageNotice("bad", changeFailure.message);
  }
  await rerender();
}
