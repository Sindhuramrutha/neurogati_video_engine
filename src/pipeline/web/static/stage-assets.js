/**
 * Assets & Design — which pictures the video may show, and how it should look.
 *
 * Extraction produces every picture in the sources and knows nothing about which
 * ones matter; a deck of sixty-three yields perhaps fifteen worth showing. The
 * decision is made here, once, and kept: it is keyed by the stored picture, so
 * re-running extraction does not throw it away.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, icon, projectApiPath, refreshProjectSummary, select,
  showStageNotice, stageIcon,
} from "/static/ui-kit.js";

const assetsViewState = {
  filter: "all",      // all | usable | skipped | decoration | generated
};

const FILTERS = [
  ["all", "Everything"],
  ["usable", "Would be shown"],
  ["skipped", "Skipped"],
  ["decoration", "Decoration"],
  ["generated", "Not from the source"],
];

const matchesFilter = figure => ({
  all: true,
  usable: figure.use === "use" || (figure.use === "undecided" && !figure.is_decoration),
  skipped: figure.use === "skip",
  decoration: figure.is_decoration,
  generated: figure.origin !== "source",
}[assetsViewState.filter]);

const pictureUrl = assetPath =>
  projectApiPath(`/extraction/assets/${encodeURIComponent(assetPath.split("/").pop())}`);

export async function renderAssetsStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  body.innerHTML = `<div class="card muted">Loading the library…</div>`;

  let library;
  try {
    library = await requestJsonFromApi(projectApiPath("/assets"));
  } catch (loadFailure) {
    console.error("asset library load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load the asset library.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }
  applicationState.assetLibrary = library;

  const shown = library.figures.filter(matchesFilter);

  body.innerHTML = `
    <div class="card">
      <div class="card-head">
        <span class="card-icon">${stageIcon("assets", 21)}</span>
        <div>
          <h2>Assets &amp; Design</h2>
          <p>Choose what the video may show, and whether it follows the source's look.</p>
        </div>
        <button class="btn" id="assets-agent-button">
          ${icon(ICON.gear, 14, 1.8)} Agent &amp; instructions
        </button>
      </div>

      ${renderRunBar(library)}

      ${library.warnings.length ? `
        <div class="notice warn" style="margin-bottom:14px">
          ${library.warnings.map(escapeHtml).join(" · ")}
        </div>` : ""}

      <div class="assets-grid">
        <div>
          ${renderFilters(library)}
          ${library.figures.length
            ? `<div class="figure-grid">${shown.map(renderFigure).join("")}</div>`
            : `<div class="empty">
                 <h3>No pictures yet</h3>
                 <p>Gather them from the extraction to decide what the video can show.</p>
               </div>`}
          ${library.figures.length && !shown.length
            ? `<p class="muted edit-hint">Nothing matches this filter.</p>` : ""}
        </div>
        ${renderLookPanel(library.look)}
      </div>

      ${renderFooterNav(stage)}
    </div>`;

  wireAssetsStage(stage, navigateToStage, renderAgentStage);
}

function renderRunBar(library) {
  const audit = library.audit;
  const tone = library.is_empty ? "blocked" : "ready";
  return `
    <div class="run-bar ${tone}">
      <span class="run-icon">${icon(library.is_empty ? ICON.alert : ICON.check, 17, 2.2)}</span>
      <span class="run-text">
        <b>${library.is_empty ? "Nothing gathered yet" : `${audit.figure_count} picture(s)`}</b>
        <span>${library.is_empty
          ? "Gather the pictures the extraction found."
          : `${audit.usable_count} would be shown · ${audit.chosen_count} chosen · `
            + `${audit.skipped_count} skipped · ${audit.decoration_count} look like decoration`
            + (audit.generated_count ? ` · ${audit.generated_count} drawn` : "")
            + (audit.uploaded_count ? ` · ${audit.uploaded_count} uploaded` : "")}</span>
      </span>
      <button class="btn btn-accent" id="refresh-assets-button">
        ${library.is_empty ? "Gather pictures" : "Gather again"}
      </button>
    </div>`;
}

function renderFilters(library) {
  const counts = {
    all: library.figures.length,
    usable: library.audit.usable_count,
    skipped: library.audit.skipped_count,
    decoration: library.audit.decoration_count,
    generated: library.audit.generated_count + library.audit.uploaded_count,
  };
  return `
    <div class="seg asset-filters">
      ${FILTERS.map(([key, label]) => `
        <button class="${assetsViewState.filter === key ? "on" : ""}" data-filter="${key}">
          ${escapeHtml(label)} <span class="mono">${counts[key] ?? 0}</span>
        </button>`).join("")}
    </div>`;
}

function renderFigure(figure) {
  const decided = figure.use === "use" ? "chosen" : figure.use === "skip" ? "skipped" : "";
  return `
    <div class="figure-card ${decided} ${figure.in_extraction ? "" : "gone"}"
         data-figure="${escapeHtml(figure.id)}">
      <img class="figure-thumb" alt="" loading="lazy" src="${pictureUrl(figure.asset_path)}">
      <div class="figure-body">
        <b>${escapeHtml(figure.caption || "Untitled picture")}</b>
        <span class="figure-where">${escapeHtml(figure.where)}</span>
        <div class="figure-facts">
          ${figure.width ? `<span class="fact muted">${figure.width}×${figure.height}</span>` : ""}
          ${figure.origin !== "source"
            ? `<span class="fact warn">${escapeHtml(figure.origin)}</span>` : ""}
          ${figure.is_decoration ? `<span class="fact muted">decoration</span>` : ""}
          ${figure.in_extraction ? "" : `<span class="fact bad">no longer extracted</span>`}
        </div>
        ${figure.note ? `<span class="figure-note">${escapeHtml(figure.note)}</span>` : ""}
      </div>
      <div class="figure-actions">
        <button class="btn ${figure.use === "use" ? "btn-accent" : ""}"
                data-use="use" data-for="${escapeHtml(figure.id)}">Use</button>
        <button class="btn ${figure.use === "skip" ? "btn-accent" : ""}"
                data-use="skip" data-for="${escapeHtml(figure.id)}">Skip</button>
        <button class="btn-icon" data-note-for="${escapeHtml(figure.id)}"
                title="Say why" aria-label="Say why">
          ${icon(`<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>`, 14, 1.8)}
        </button>
      </div>
    </div>`;
}

/** The source deck's own look, and whether the video should wear it. */
function renderLookPanel(look) {
  const swatches = Object.entries(look.colours ?? {})
    .filter(([, value]) => String(value).startsWith("#"))
    .slice(0, 10);

  return `
    <div class="panel look-panel">
      <div class="panel-head"><h3>The look</h3></div>
      ${look.is_available
        ? `<p class="panel-sub">From ${escapeHtml(look.from_file)}${
             look.theme_name ? ` · ${escapeHtml(look.theme_name)}` : ""}</p>

           <label class="toggle-row look-toggle">
             <span class="checkbox ${look.use_source_styling ? "on" : ""}" id="use-styling-toggle"
                   role="checkbox" aria-checked="${look.use_source_styling}">
               ${icon(ICON.check, 11, 3.5)}
             </span>
             <span>
               <b>Follow the source's styling</b>
               <span class="hint">Its colours, fonts and slide proportions, rather than
                 the renderer's defaults.</span>
             </span>
           </label>

           <dl class="context-facts look-facts">
             ${look.aspect_ratio ? `<dt>Shape</dt><dd>${escapeHtml(look.aspect_ratio)}</dd>` : ""}
             ${look.heading_font ? `<dt>Headings</dt><dd>${escapeHtml(look.heading_font)}</dd>` : ""}
             ${look.body_font ? `<dt>Body</dt><dd>${escapeHtml(look.body_font)}</dd>` : ""}
             ${look.background_colour
               ? `<dt>Behind</dt><dd><span class="swatch"
                    style="background:${escapeHtml(look.background_colour)}"></span>
                    ${escapeHtml(look.background_colour)}</dd>` : ""}
           </dl>

           ${swatches.length ? `
             <div class="swatches">
               ${swatches.map(([name, value]) => `
                 <span class="swatch-chip" title="${escapeHtml(name)} ${escapeHtml(value)}">
                   <span class="swatch" style="background:${escapeHtml(value)}"></span>
                   ${escapeHtml(name)}
                 </span>`).join("")}
             </div>` : ""}

           ${look.background_asset_path ? `
             <div class="look-background">
               <span class="scene-label">Background picture</span>
               <img alt="" loading="lazy" src="${pictureUrl(look.background_asset_path)}">
             </div>` : ""}`
        : `<p class="muted edit-hint">No styling was extracted. Switch on
             <b>Extract styling</b> on Extraction and run it again to read a deck's
             colours and fonts.</p>`}
    </div>`;
}

function renderFooterNav(stage) {
  const { stageDefinitions } = applicationState;
  const index = stageDefinitions.findIndex(s => s.key === stage.key);
  const previous = stageDefinitions[index - 1];
  const next = stageDefinitions[index + 1];
  return `
    <div class="footer-nav">
      ${previous ? `<button class="btn" data-goto="${previous.key}">
        ${icon(ICON.arrowLeft)} Back to ${escapeHtml(previous.title)}</button>` : ""}
      <div class="spacer"></div>
      ${next ? `<button class="btn btn-accent" data-goto="${next.key}">
        Next: ${escapeHtml(next.title)} ${icon(ICON.arrowRight)}</button>` : ""}
    </div>`;
}

function wireAssetsStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderAssetsStage(stage, navigateToStage, renderAgentStage);

  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });
  select("#assets-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-filter]").forEach(button => {
    button.onclick = () => {
      assetsViewState.filter = button.dataset.filter;
      rerender();
    };
  });

  select("#refresh-assets-button").onclick = async () => {
    const button = select("#refresh-assets-button");
    button.disabled = true;
    button.textContent = "Gathering…";
    try {
      applicationState.assetLibrary = await requestJsonFromApi(
        projectApiPath("/assets/refresh"), { method: "POST" });
      showStageNotice("ok",
        `${applicationState.assetLibrary.audit.figure_count} picture(s) gathered.`);
      await refreshProjectSummary();
    } catch (refreshFailure) {
      console.error("gathering assets failed", refreshFailure);
      showStageNotice("bad", refreshFailure.message);
    }
    await rerender();
  };

  document.querySelectorAll("[data-use]").forEach(button => {
    button.onclick = () => decide(button.dataset.for, button.dataset.use, undefined, rerender);
  });

  document.querySelectorAll("[data-note-for]").forEach(button => {
    button.onclick = () => {
      const figure = applicationState.assetLibrary.figures
        .find(f => f.id === button.dataset.noteFor);
      const note = window.prompt("Why? (one line)", figure?.note ?? "");
      if (note === null) return;
      decide(button.dataset.noteFor, figure?.use ?? "undecided", note, rerender);
    };
  });

  const toggle = select("#use-styling-toggle");
  if (toggle) {
    toggle.onclick = async () => {
      const wanted = !toggle.classList.contains("on");
      try {
        applicationState.assetLibrary = await requestJsonFromApi(
          projectApiPath("/assets/look"), {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ use_source_styling: wanted }),
          });
      } catch (lookFailure) {
        console.error("setting the look failed", lookFailure);
        showStageNotice("bad", lookFailure.message);
      }
      await rerender();
    };
  }
}

/** A decision is one click, so it saves immediately rather than collecting edits. */
async function decide(figureId, use, note, rerender) {
  try {
    applicationState.assetLibrary = await requestJsonFromApi(
      projectApiPath(`/assets/figures/${encodeURIComponent(figureId)}`), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(note === undefined ? { use } : { use, note }),
      });
  } catch (decisionFailure) {
    console.error("saving the decision failed", decisionFailure);
    showStageNotice("bad", decisionFailure.message);
  }
  await rerender();
}
