/**
 * Extraction stage — three tabs, in the order the work happens.
 *
 * 1. Extract: the project's one source file, and the one button that reads it.
 * 2. Review: each slide beside what was extracted from it, with the agent to
 *    review it slide by slide and change it. Only what was extracted.
 * 3. Final & transfer: everything extracted, and the one button that hands it
 *    to the next layer. Nothing reaches the Scene Plan until then, so a
 *    half-assembled collection is never planned from.
 *
 * Options are declared server-side and rendered generically here, so adding an
 * option is one entry in `stage_options.py` rather than a change in three places.
 */

import {
  openRawFile, releaseRawFile, renderRawFileShell, stepRawFile,
} from "/static/raw-file-viewer.js";
import { loadPicks, renderPicksCard, wirePicksCard } from "/static/extraction-picks.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, fileTypeBadge, footerNav, hideProgress, icon,
  moveToNextLayerButton, projectApiPath, refreshProjectSummary, select, showProgress,
  showStageNotice, stageHeader, stageNeighbours, whenItWas, wireGotoButtons,
} from "/static/ui-kit.js";

/** What the page was last drawn from. A view change -- a tab, a file, a view --
 *  redraws from this instead of fetching three documents again. */
let loaded = null;

async function loadExtractionPage(stage) {
  const [settings, extraction, review, picks] = await Promise.all([
    requestJsonFromApi(projectApiPath(`/settings/${stage.key}`)),
    requestJsonFromApi(projectApiPath("/extraction")).catch(extractionFailure => {
      console.error("extraction load failed", extractionFailure);
      return { documents: [], warnings: [], is_empty: true, audit: {}, freshness: {} };
    }),
    // A review of a previous run is worth showing straight away, and it is a
    // file read rather than any work.
    requestJsonFromApi(projectApiPath("/extraction/review")).catch(reviewFailure => {
      console.warn("extraction review load failed", reviewFailure);
      return null;
    }),
    loadPicks(),
  ]);
  return { slug: applicationState.selectedProject?.slug, settings, extraction, review, picks };
}

export async function renderExtractionStage(
  stage, navigateToStage, renderAgentStage, { refetch = true } = {},
) {
  const body = select("#stage-body");
  const source = applicationState.selectedProject?.source;
  const sources = source ? [source] : [];

  if (refetch || loaded?.slug !== applicationState.selectedProject?.slug) {
    body.innerHTML = `<div class="card muted">Loading options…</div>`;
    try {
      loaded = await loadExtractionPage(stage);
    } catch (settingsFailure) {
      console.error("settings load failed", settingsFailure);
      body.innerHTML = `<div class="card">
        <b>Could not load extraction options.</b>
        <p class="muted" style="margin:6px 0 0">${escapeHtml(settingsFailure.message)}</p>
      </div>`;
      return;
    }
  }
  const { settings, extraction, review, picks } = loaded;
  applicationState.stageSettings[stage.key] = settings;
  applicationState.extractionReview = review;

  applicationState.previewFileName = applicationState.selectedProject?.source?.name ?? null;

  body.innerHTML = `
    ${stageHeader("extraction", "Extraction", {
      agentButtonId: "extraction-agent-button",
    })}

    <div class="stage-content stage-content-bare">

      ${renderPicksCard(extraction, picks)}

      <div class="extraction-tabs">
        ${renderStageTabs()}

        <div class="x-tab-body" role="tabpanel">
          ${{
            extract: () => renderExtractTab(sources, extraction, settings),
            review: () => renderReviewTab(sources, extraction, review),
            final: () => renderFinalTab(stage, extraction),
          }[currentExtractionTab()]()}
        </div>
      </div>

      ${renderFooterNav(stage, extraction)}
    </div>`;

  wireExtractionStage(stage, navigateToStage, renderAgentStage);
}

/** Why an extracted file no longer matches its file or the options, or "". */
const STALE_REASONS = [
  ["removed", "file deleted"], ["changed", "file changed"], ["options_changed", "options changed"],
];

function staleReason(freshness, fileName) {
  return STALE_REASONS.find(([key]) => (freshness?.[key] ?? []).includes(fileName))?.[1] ?? "";
}

/** The open findings a review has, only for files in the collection and,
 *  given a file name, only for that file. */
function openFindings(review, extractedNames, fileName = "") {
  return (review?.findings ?? []).filter(finding => !finding.acknowledged
    && (!finding.file_name || extractedNames.has(finding.file_name))
    && (!fileName || finding.file_name === fileName));
}

function statusBadge(tone, text) {
  return `<span class="file-status ${tone}">${escapeHtml(text)}</span>`;
}

/** "342 blocks · 63 figures" for one extracted file. */
function documentSummary(document) {
  const figures = document.blocks.filter(block => block.kind === "figure").length;
  return [
    `${document.blocks.length} blocks`,
    figures ? `${figures} figures` : "",
  ].filter(Boolean).join(" · ");
}

/** Where the source stands, in one sentence: [tone, title, detail, button]. */
function sourceState(source, extraction) {
  if (!source) {
    return ["blocked", "No source file", "Add it on Inputs.", ""];
  }
  const document = extraction.documents.find(d => d.file_name === source.name);
  if (!document) {
    return extraction.documents.length
      ? ["stale", "The source was replaced",
         `${extraction.documents[0].file_name} was extracted. Extract the new file.`, "Extract"]
      : ["pending", "Not extracted yet", "Extract it to read what it says.", "Extract"];
  }
  const stale = staleReason(extraction.freshness, source.name);
  if (stale) {
    return ["stale", "Extract it again",
      stale === "options changed" ? "The options changed since it was extracted."
        : "The file changed since it was extracted.", "Extract again"];
  }
  return ["ready", "Extracted", documentSummary(document), "Extract again"];
}

function renderSourcePanel(source, extraction) {
  const [tone, title, detail, button] = sourceState(source, extraction);
  const busy = Boolean(applicationState.extractingFileName);
  return `
    <div class="panel x-source ${tone}">
      <div class="panel-head"><h3>Extract the source</h3></div>
      ${source ? "" : `<button class="btn" data-goto="inputs">Go to Inputs</button>`}
      <p class="x-source-state"><b>${escapeHtml(title)}</b> ${escapeHtml(detail)}</p>
      ${button ? `
        <button class="btn ${tone === "ready" ? "" : "btn-accent"} x-extract-button"
                id="extract-file-button" ${busy ? "disabled" : ""}>
          ${busy ? "Extracting…" : escapeHtml(button)}</button>` : ""}
      ${renderPdfLimitation(source)}
    </div>`;
}

/** Said plainly, and only when it applies.
 *
 *  The PDF reader takes text and nothing else: no headings, so a block's heading
 *  path is the page it sat on, and no figures. Every other stage is built on the
 *  promise that a claim can be traced back to a section, and for a PDF it can
 *  only be traced to "somewhere on page 7". The README admitted this and the
 *  page did not, which left the gap to be discovered rather than read.
 */
function renderPdfLimitation(source) {
  if ((source?.suffix || "").toLowerCase() !== ".pdf") return "";
  return `
    <p class="muted" style="font-size:12px;margin:8px 0 0;line-height:1.45">
      <b>PDF:</b> headings become page numbers and figures are not extracted —
      Word or PowerPoint keeps both. Scanned or handwritten pages are read only
      with handwriting recognition on.
    </p>`;
}

function renderOptionsPanel(settings) {
  const renderControl = option => {
    const currentValue = settings.values[option.key];

    if (option.kind === "choice") {
      const activeChoice = option.choices.find(choice => choice.value === currentValue);
      return `
        <div class="option">
          <label for="opt-${escapeHtml(option.key)}">${escapeHtml(option.label)}</label>
          <select id="opt-${escapeHtml(option.key)}" data-option="${escapeHtml(option.key)}">
            ${option.choices.map(choice => `
              <option value="${escapeHtml(choice.value)}"
                      ${choice.value === currentValue ? "selected" : ""}>
                ${escapeHtml(choice.label)}</option>`).join("")}
          </select>
          <p class="help">${escapeHtml(activeChoice?.help_text ?? option.help_text)}</p>
        </div>`;
    }

    return `
      <button class="toggle-row" data-option="${escapeHtml(option.key)}"
              role="checkbox" aria-checked="${currentValue}"
              title="${escapeHtml(option.help_text)}">
        <span class="checkbox ${currentValue ? "on" : ""}">${icon(ICON.check, 13, 3.5)}</span>
        <span class="toggle-label">${escapeHtml(option.label)}</span>
      </button>`;
  };

  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Extraction options</h3>
        <div class="spacer"></div>
        <span class="mono muted" id="settings-saved-hint"></span>
      </div>
      ${settings.options.map(renderControl).join("")}
    </div>`;
}

/** The previewed file's result in the collection, or a sentence saying why
 *  there is none. Only ever the file whose name is in the header. */
function previewedDocument(extraction, previewName) {
  const parsed = extraction.documents.find(d => d.file_name === previewName);
  if (parsed) return { parsed };

  const message = !previewName
    ? "No source file."
    : `<b>${escapeHtml(previewName)}</b> is not extracted yet.<br>
       Press <b>Extract</b> on the Extract tab to read it.`;
  return { empty: `<div class="preview-empty">${icon(ICON.doc, 34, 1.4)}<p>${message}</p></div>` };
}

/** Blocks carry the heading they sit under, so extracted text reads back with
 *  its structure rather than as a wall of paragraphs. */
function renderExtractedBlocks(
  extraction, fileName = applicationState.previewFileName, { head = true } = {},
) {
  const { parsed, empty } = previewedDocument(extraction, fileName);
  if (!parsed) return empty;

  const rows = renderBlockRows(parsed.blocks.slice(0, 400));
  const truncated = parsed.blocks.length > 400
    ? `<p class="muted" style="font-size:11.5px">showing the first 400 of ${
        parsed.blocks.length} blocks</p>`
    : "";

  return `<div class="x-doc">
    ${head ? `<div class="x-doc-head">${escapeHtml(parsed.file_name)} &middot; ${
      parsed.blocks.length} blocks${parsed.extraction_note
        ? ` &middot; ${escapeHtml(parsed.extraction_note)}` : ""}</div>` : ""}${rows}${truncated}</div>`;
}

const BLOCK_KINDS = {
  heading: "Heading", paragraph: "Text", list_item: "List item", table: "Table", figure: "Figure",
};

/** Every extracted block in the same box, labelled with what it is, so a page
 *  of them reads as a list of pieces rather than a wall of mixed styles. */
function renderBlockRows(blocks) {
  return blocks.map(block => {
    const body = block.kind === "figure" ? renderFigureBlock(block)
      : block.kind === "table" ? `<pre class="x-box-table">${escapeHtml(block.text)}</pre>`
      : `<p class="x-box-text">${escapeHtml(block.text)}</p>`;
    return `
      <div class="x-box ${escapeHtml(block.kind)}">
        <div class="x-box-kind">${BLOCK_KINDS[block.kind] ?? escapeHtml(block.kind)}${
          // Read off a page image by the vision model, not parsed from the file.
          block.transcribed ? `<span class="x-transcribed"
            title="Read from a page image by the vision model">transcribed</span>` : ""}</div>
        ${body}
      </div>`;
  }).join("");
}

/** What was extracted from what is on screen: for a deck, the slide showing
 *  in the preview beside it; for anything else, the whole file. */
function renderExtractionSide(extraction, fileName, slideIndex = 0) {
  const { parsed, empty } = previewedDocument(extraction, fileName);
  if (!parsed) return empty;
  if (!parsed.blocks.some(block => block.slide_number)) {
    return renderExtractedBlocks(extraction, fileName, { head: false });
  }
  const number = slideIndex + 1;
  const blocks = parsed.blocks.filter(block => block.slide_number === number);
  return `<div class="x-doc">
    ${renderSlideStructure(parsed, number)}
    ${blocks.length ? renderBlockRows(blocks)
      : `<p class="muted" style="margin:10px">Nothing was extracted from this slide.</p>`}
  </div>`;
}

const SHAPE_KINDS = {
  title: "title", text: "text", picture: "picture", table: "table", chart: "chart", other: "other",
};

function extractedAssetUrl(assetPath) {
  return projectApiPath(`/extraction/assets/${encodeURIComponent(assetPath.split("/").pop())}`);
}

/** The slide itself, as extraction recorded it: where each shape sits
 *  (Layout) and what is behind them (Background), in the same boxes as the
 *  content. Only for a deck read with those options on. */
function renderSlideStructure(parsed, number) {
  const slide = parsed.slides?.find(candidate => candidate.number === number);
  if (!slide) return "";

  const design = parsed.design ?? {};
  const ratio = design.slide_width_emu && design.slide_height_emu
    ? design.slide_width_emu / design.slide_height_emu : 16 / 9;
  const percent = fraction => `${(fraction * 100).toFixed(2)}%`;
  const shapes = [...(slide.shapes ?? [])].sort((a, b) => a.z - b.z);
  const counts = shapes.reduce((tally, shape) => {
    tally[shape.kind] = (tally[shape.kind] ?? 0) + 1;
    return tally;
  }, {});
  // A picture added after extraction has no slot on the original slide; a
  // replaced one took its predecessor's, and shows in the map.
  const placed = new Set(shapes.map(shape => shape.asset_path).filter(Boolean));
  const added = parsed.blocks.filter(block => block.slide_number === number
    && block.kind === "figure" && block.asset_path && !placed.has(block.asset_path)).length;

  const layout = shapes.length ? `
    <div class="x-box layout">
      <div class="x-box-kind">Layout${slide.layout_name
        ? `<span class="x-box-note">${escapeHtml(slide.layout_name)}</span>` : ""}</div>
      <div class="x-layout-map" style="aspect-ratio:${ratio.toFixed(4)}">
        ${shapes.map(shape => `
          <span class="x-layout-shape ${SHAPE_KINDS[shape.kind] ?? "other"}"
                title="${escapeHtml(shape.kind + (shape.text ? `: ${shape.text}` : ""))}"
                style="left:${percent(shape.left)};top:${percent(shape.top)};
                       width:${percent(shape.width)};height:${percent(shape.height)}">
            ${shape.asset_path
              ? `<img src="${extractedAssetUrl(shape.asset_path)}" alt="" loading="lazy">`
              : `<span>${escapeHtml(shape.text || shape.kind)}</span>`}
          </span>`).join("")}
      </div>
      <p class="x-box-caption">${shapes.length} shape${shapes.length === 1 ? "" : "s"}: ${
        Object.entries(counts).map(([kind, count]) =>
          `${count} ${escapeHtml(kind)}${count === 1 || kind === "text" ? "" : "s"}`).join(", ")}${
        added ? ` · ${added} added picture${added === 1 ? "" : "s"}, not placed on the slide` : ""}</p>
    </div>` : "";

  const background = slide.background;
  const isHex = value => /^#[0-9a-f]{6}$/i.test(value ?? "");
  const colour = isHex(background?.colour) ? background.colour : "";
  const stops = (background?.gradient ?? []).filter(isHex);
  const swatch = stops.length > 1 ? `linear-gradient(90deg, ${stops.join(", ")})` : colour;
  const from = background?.inherited_from;
  const backgroundBox = background && (colour || background.asset_path) ? `
    <div class="x-box background">
      <div class="x-box-kind">Background${from ? `<span class="x-box-note">${
        from === "slide" ? "set on this slide" : `from the ${escapeHtml(from)}`}</span>` : ""}</div>
      ${background.asset_path ? `<img class="x-background-image" loading="lazy"
          src="${extractedAssetUrl(background.asset_path)}" alt="Background of slide ${number}">` : ""}
      ${swatch && !background.asset_path ? `<p class="x-box-text"><span class="x-swatch${
        stops.length > 1 ? " wide" : ""}" style="background:${swatch}"></span>${
        stops.length > 1 ? `Gradient ${stops.join(" → ")}` : colour}</p>` : ""}
    </div>` : "";

  return layout + backgroundBox;
}

/** The Extraction column and the pager follow the slide the preview shows. */
document.addEventListener("deck-slide", event => {
  const { fileName, index, total } = event.detail;
  const pane = document.querySelector("[data-extraction-for]");
  if (!loaded || pane?.dataset.extractionFor !== fileName) return;
  applicationState.previewSlideIndex = index;
  pane.innerHTML = renderExtractionSide(loaded.extraction, fileName, index);
  pane.scrollTop = 0;

  const pager = document.querySelector("[data-pager-for]");
  if (!pager) return;
  pager.hidden = total < 2;
  pager.querySelector(".x-pager-count").textContent = `${index + 1} / ${total}`;
  pager.querySelector('[data-step="-1"]').disabled = index === 0;
  pager.querySelector('[data-step="1"]').disabled = index === total - 1;
});

/** Drag the boundary between Preview and Extraction, or focus it and use the
 *  arrow keys. The split is kept for the session, so it survives a redraw. */
function wireCompare() {
  document.querySelectorAll("[data-pager-for] [data-step]").forEach(button => {
    button.onclick = () => stepRawFile(applicationState.previewFileName, Number(button.dataset.step));
  });

  const compare = select(".x-compare");
  const divider = compare?.querySelector(".x-compare-divider");
  if (!divider) return;
  const setSplit = percent => {
    const split = Math.min(75, Math.max(30, percent));
    applicationState.compareSplit = split;
    compare.style.setProperty("--x-split", `${split}%`);
    divider.setAttribute("aria-valuenow", String(Math.round(split)));
  };

  divider.onpointerdown = down => {
    down.preventDefault();
    divider.setPointerCapture(down.pointerId);
    compare.classList.add("resizing");
    const move = event => {
      const box = compare.getBoundingClientRect();
      setSplit(((event.clientX - box.left) / box.width) * 100);
    };
    const stop = () => {
      compare.classList.remove("resizing");
      divider.removeEventListener("pointermove", move);
      divider.removeEventListener("pointerup", stop);
      divider.removeEventListener("pointercancel", stop);
    };
    divider.addEventListener("pointermove", move);
    divider.addEventListener("pointerup", stop);
    divider.addEventListener("pointercancel", stop);
  };
  divider.onkeydown = event => {
    const step = { ArrowLeft: -5, ArrowRight: 5 }[event.key];
    if (!step) return;
    event.preventDefault();
    setSplit(applicationState.compareSplit + step);
  };
}

/** Formats a browser cannot draw. Word and PowerPoint still embed old Windows
 *  metafiles, and an <img> pointed at one shows a broken-image icon that reads
 *  as a failed extraction when the figure was extracted fine. */
const FIGURES_BROWSERS_CANNOT_SHOW = new Set(["emf", "wmf", "tif", "tiff"]);

/** A figure the extraction pulled out, shown as the image itself. */
function renderFigureBlock(block) {
  const assetName = (block.asset_path || "").split("/").pop();
  const extension = assetName.split(".").pop().toLowerCase();

  if (!assetName) {
    return `<div class="x-block x-figure missing">
      <span class="x-figure-note">figure not stored</span>${escapeHtml(block.text)}</div>`;
  }

  const source = projectApiPath(`/extraction/assets/${encodeURIComponent(assetName)}`);
  const picture = FIGURES_BROWSERS_CANNOT_SHOW.has(extension)
    ? `<span class="x-figure-note">.${escapeHtml(extension)} — extracted, but browsers
         cannot draw this format. <a href="${source}" download>Download it</a>.</span>`
    : `<img src="${source}" alt="${escapeHtml(block.text)}" loading="lazy">`;

  return `<figure class="x-block x-figure">
    ${picture}
    <figcaption>${escapeHtml(block.text)}</figcaption>
  </figure>`;
}

function renderPreviewPanel(sources, extraction) {
  const previewFile = sources.find(file => file.name === applicationState.previewFileName);
  if (!previewFile) {
    return `
      <div class="panel preview-panel">
        <div class="preview-empty">${icon(ICON.doc, 34, 1.4)}
          <p>No file to show.<br>Add one on the Inputs stage.</p></div>
      </div>`;
  }

  const name = escapeHtml(previewFile.name);
  const split = applicationState.compareSplit;
  return `
    <div class="panel preview-panel">
      <div class="x-compare" style="--x-split:${split}%">
        <section class="x-compare-side">
          <h3 class="x-compare-title">Preview</h3>
          <div class="preview-stage raw">
            <div data-raw-host="${name}">
              <p class="muted" style="margin:0">Opening ${name}…</p>
            </div>
          </div>
        </section>
        <div class="x-compare-divider" role="separator" aria-orientation="vertical" tabindex="0"
             aria-label="Drag to resize the preview and the extraction"
             aria-valuemin="30" aria-valuemax="75" aria-valuenow="${Math.round(split)}"></div>
        <section class="x-compare-side">
          <h3 class="x-compare-title">Extraction</h3>
          <div class="preview-stage scrolls" data-extraction-for="${name}">
            ${renderExtractionSide(extraction, previewFile.name)}
          </div>
        </section>
      </div>
      <div class="x-pager" data-pager-for="${name}" hidden>
        <button class="x-pager-arrow" data-step="-1" title="Previous" aria-label="Previous">
          ${icon(`<path d="M15 18l-6-6 6-6"/>`, 22, 2.8)}</button>
        <span class="x-pager-count"></span>
        <button class="x-pager-arrow" data-step="1" title="Next" aria-label="Next">
          ${icon(`<path d="M9 18l6-6-6-6"/>`, 22, 2.8)}</button>
      </div>
      ${renderAgentPanel(extraction, previewFile.name)}
    </div>`;
}

/** The file itself, in the Preview tab: the same raw rendering as Inputs.
 *
 */
async function openPreviewedFile() {
  const host = document.querySelector("[data-raw-host]");
  if (!host) return;
  const fileName = host.dataset.rawHost;

  try {
    const preview = await requestJsonFromApi(
      projectApiPath(`/sources/${encodeURIComponent(fileName)}/preview`));
    // The stage may have been redrawn while this was loading.
    if (!host.isConnected) return;
    host.innerHTML = renderRawFileShell(fileName, preview);
    openRawFile(host, fileName, preview.viewer, { slideStrip: false });
  } catch (previewFailure) {
    console.error("preview failed", previewFailure);
    if (host.isConnected) {
      host.innerHTML = `<p class="muted" style="margin:0">Could not open this file —
        ${escapeHtml(previewFailure.message)}</p>`;
    }
  }
}

/* ---- the three tabs: Extract, Review, Final ---------------------------------
 *
 * One job per tab, in the order they happen. Extract reads files one at a time;
 * Review checks only what was extracted; Final shows everything that will be
 * handed on, and is the only place that hands it on.
 */

const EXTRACTION_TABS = ["extract", "review", "final"];

function currentExtractionTab() {
  return EXTRACTION_TABS.includes(applicationState.extractionTab)
    ? applicationState.extractionTab : "extract";
}

const TAB_LABELS = { extract: "Extract", review: "Review", final: "Final & transfer" };

function renderStageTabs() {
  const tab = currentExtractionTab();
  return `
    <nav class="x-tabs" role="tablist" aria-label="Extraction steps">
      ${EXTRACTION_TABS.map((key, index) => `
        <button role="tab" class="x-tab ${key === tab ? "on" : ""}"
                data-extraction-tab="${key}" aria-selected="${key === tab}">
          <span class="x-tab-number">${index + 1}</span>
          <b class="x-tab-label">${TAB_LABELS[key]}</b>
        </button>`).join("")}
    </nav>`;
}

function renderExtractTab(sources, extraction, settings) {
  return `
    <div class="workbench extraction-workbench">
      <div class="workbench-side">
        ${renderSourcePanel(applicationState.selectedProject?.source, extraction)}
        ${renderOptionsPanel(settings)}
      </div>
    </div>`;
}

/** The boundary under the files and options: dragged up, Preview / Extraction
 *  grows taller; down, shorter. The arrow keys do the same when it is focused.
 *  Kept for the session, so it survives a redraw. */
function wireRowDivider() {
  const workbench = select(".extraction-workbench");
  const divider = workbench?.querySelector(".x-row-divider");
  const pane = workbench?.querySelector(".preview-panel .preview-stage.scrolls");
  if (!divider || !pane) return;
  const setHeight = pixels => {
    const height = Math.round(Math.min(1600, Math.max(260, pixels)));
    applicationState.comparePaneHeight = height;
    workbench.style.setProperty("--x-pane-height", `${height}px`);
  };

  divider.onpointerdown = down => {
    down.preventDefault();
    divider.setPointerCapture(down.pointerId);
    workbench.classList.add("resizing");
    const startY = down.clientY;
    const startHeight = pane.getBoundingClientRect().height;
    const move = event => setHeight(startHeight + (startY - event.clientY));
    const stop = () => {
      workbench.classList.remove("resizing");
      divider.removeEventListener("pointermove", move);
      divider.removeEventListener("pointerup", stop);
      divider.removeEventListener("pointercancel", stop);
    };
    divider.addEventListener("pointermove", move);
    divider.addEventListener("pointerup", stop);
    divider.addEventListener("pointercancel", stop);
  };
  divider.onkeydown = event => {
    const step = { ArrowUp: 40, ArrowDown: -40 }[event.key];
    if (!step) return;
    event.preventDefault();
    setHeight(pane.getBoundingClientRect().height + step);
  };
}

function renderTabEmpty(message) {
  return `
    <div class="panel x-tab-empty">
      ${icon(ICON.doc, 34, 1.4)}
      <p>${message}</p>
      <button class="btn btn-accent" data-extraction-tab="extract">Go to Extract</button>
    </div>`;
}

/** Only what was extracted: one file at a time, slide by slide -- the slide,
 *  what was extracted from it, and the agent to review and change it. */
function renderReviewTab(sources, extraction, review) {
  const reviewSources = [{ name: extraction.documents[0]?.file_name, suffix: "" }];
  if (!extraction.documents.length) {
    return renderTabEmpty("Nothing to review yet.<br>Extract a file first, then check it here.");
  }
  // What was extracted is what is reviewed: after the source is replaced and
  // before it is extracted again, that is still the old file's result.
  const fileName = extraction.documents[0].file_name;
  applicationState.previewFileName = fileName;
  const names = extractedNames(extraction);
  const height = applicationState.comparePaneHeight;

  return `
    <div class="workbench extraction-workbench"${
      height ? ` style="--x-pane-height:${height}px"` : ""}>
      <div class="workbench-side">
        ${renderReviewPanel(review ?? { findings: [], reviewed_at: "" }, names,
          extraction.documents.find(d => d.file_name === fileName))}
      </div>
      <div class="x-row-divider" role="separator" aria-orientation="horizontal" tabindex="0"
           aria-label="Drag up for a taller preview and extraction, down for a shorter one"></div>
      ${renderPreviewPanel(reviewSources, extraction)}
    </div>`;
}

/** Everything that will be handed on, and the one button that hands it on. */
function renderFinalTab(stage, extraction) {
  const freshness = extraction.freshness ?? {};
  const documents = extraction.documents;
  const outOfDate = documents.map(d => d.file_name).filter(name => staleReason(freshness, name));
  const replaced = documents.length && applicationState.selectedProject?.source
    && documents[0].file_name !== applicationState.selectedProject.source.name;
  const pending = Boolean(freshness.pending_confirmation);
  const transferred = freshness.has_confirmed && !pending;
  const canTransfer = !outOfDate.length && !replaced
    && (documents.length ? pending : freshness.has_confirmed);

  const [tone, title, detail] = !documents.length
    ? ["blocked", "Nothing extracted yet",
       freshness.has_confirmed
         ? "Every file was removed. Transfer to clear what the next layer reads."
         : "Extract files on the Extract tab; they collect here."]
    : replaced
      ? ["stale", "The source was replaced",
         "Extract the new file on the Extract tab, then transfer it."]
    : outOfDate.length
      ? ["stale", "Extract it again",
         "It no longer matches the file or the options."]
      : transferred
        ? ["ready", "Transferred to the next layer",
           `The next layer has had exactly this since ${whenItWas(freshness.confirmed_at)}.`]
        : ["pending", "Ready to transfer",
           freshness.has_confirmed
             ? "This differs from what the next layer has. Transfer to hand it the changes."
             : "Nothing reaches the next layer until you transfer it."];

  const audit = extraction.audit ?? {};
  const totals = documents.length ? [
    documents[0].file_name, `${audit.block_count} blocks`,
    `${audit.figure_count ?? 0} figures`,
    `${extraction.total_word_count} words (~${extraction.estimated_narration_minutes} min narrated)`,
  ] : [];


  return `
    <div class="final-head ${tone}">
      <span class="run-icon">${icon(tone === "ready" ? ICON.check : ICON.alert, 18, 2.3)}</span>
      <span class="run-text">
        <b>${escapeHtml(title)}</b>
        <span>${escapeHtml(detail)}</span>
        ${totals.length ? `<span class="final-totals">${escapeHtml(totals.join(" · "))}</span>` : ""}
      </span>
      ${transferred && !canTransfer
        ? moveToNextLayerButton(stageNeighbours(stage).next, {
            carries: "The transferred extraction goes on: it is what every later stage reads.",
          })
        : `
        <button class="btn btn-accent btn-transfer" id="confirm-extraction-button"
                ${canTransfer ? "" : "disabled"}
                title="${canTransfer ? "Hand this to Assets & Design, the Scene Plan and every later stage"
                                     : "Nothing new to transfer"}">
          Transfer to the next layer ${icon(ICON.arrowRight)}
        </button>`}
    </div>

    ${documents.length ? `
      <div class="panel preview-panel x-final-text">
        <div class="preview-head"><h3>What the next layer receives</h3></div>
        <div class="preview-stage scrolls">
          ${renderExtractedBlocks(extraction, documents[0].file_name)}
        </div>
      </div>`
      : renderTabEmpty("Nothing is extracted yet.<br>Extract the source on the Extract tab.")}`;
}

function extractedNames(extraction) {
  return new Set(extraction.documents.map(d => d.file_name));
}

/** Clicks that only change what is on screen: [data- attribute, state field]. */
const VIEW_CHOICES = [
  ["extraction-tab", "extractionTab"],
];

function wireViewChoices(page) {
  for (const [attribute, field] of VIEW_CHOICES) {
    document.querySelectorAll(`[data-${attribute}]`).forEach(button => {
      button.onclick = async () => {
        applicationState[field] = button.getAttribute(`data-${attribute}`);
        // Pressed at the foot of the page, it lands you on the new tab's top.
        const fromFooter = Boolean(button.closest(".footer-nav"));
        await page.redraw();
        if (fromFooter) select(".x-tabs")?.scrollIntoView({ block: "start", behavior: "smooth" });
      };
    });
  }
}

/** The step after this tab: Extract leads to Review, Review to Final. Only the
 *  Final tab moves on to the next layer. */
const NEXT_TAB = { extract: ["review", "Review"], review: ["final", "Final & transfer"] };

function renderFooterNav(stage, extraction) {
  const freshness = extraction.freshness ?? {};
  const nextTab = NEXT_TAB[currentExtractionTab()];
  return footerNav(stage, {
    end: nextTab ? `
      <button class="btn btn-accent btn-move-next" data-extraction-tab="${nextTab[0]}">
        Move to ${nextTab[1]} ${icon(ICON.arrowRight)}
      </button>` : null,
    next: {
      carries: freshness.has_confirmed
        ? "The transferred extraction goes on: it is what every later stage reads."
        : "",
      warning: !freshness.has_confirmed
        ? "Nothing has been transferred yet, so the next layer has no extracted content "
          + "to work from. Transfer it on the Final & transfer tab first."
        : freshness.pending_confirmation
          ? "Your latest changes are not transferred yet — the next layer still reads the "
            + "last transferred version. Transfer on the Final & transfer tab to send them."
          : "",
    },
  });
}

function wireExtractionStage(stage, navigateToStage, renderAgentStage) {
  // Either kind of redraw replaces the preview, so a rendered deck in it is
  // released first rather than left as detached slides nobody can see.
  const draw = refetch => {
    releaseRawFile(applicationState.previewFileName);
    return renderExtractionStage(stage, navigateToStage, renderAgentStage, { refetch });
  };
  // `redraw` for a change of view, `refresh` for a change of data.
  const page = { redraw: () => draw(false), refresh: () => draw(true) };

  openPreviewedFile();
  wireCompare();
  wireAgentPanel();
  wireRowDivider();
  wireReviewPanel(page);
  wireCollection(page);
  wireViewChoices(page);
  wireGotoButtons(navigateToStage);
  wirePicksCard(page.refresh);

  // The AGENT.md is the real "settings" for this stage: it governs behaviour.
  select("#extraction-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-option]").forEach(control => {
    if (control.disabled) return;
    const optionKey = control.dataset.option;
    if (control.tagName === "SELECT") {
      control.onchange = () => persistOption(stage, optionKey, control.value, page);
    } else {
      control.onclick = () => {
        const currentValue = applicationState.stageSettings[stage.key].values[optionKey];
        persistOption(stage, optionKey, !currentValue, page);
      };
    }
  });
}

/* ---- what the extraction got wrong ---------------------------------------
 *
 * Extraction fails quietly: a diagram comes out blank, a picture is a 3-pixel
 * rule, a chapter promises "Figure 2.1" and nothing was saved. The checks find
 * that without a model. The rest is the agent's, one slide at a time with the
 * slide in view: its answers land in the chat below, to apply or discard.
 */

/** The slides of a deck, in order, or [0] for a document read as a whole. */
function slidesToReview(document) {
  const numbers = document.slides?.length
    ? document.slides.map(slide => slide.number)
    : document.blocks.map(block => block.slide_number).filter(Boolean);
  return numbers.length ? [...new Set(numbers)].sort((a, b) => a - b) : [0];
}

/** The review under way, if any: kept outside the page so a redraw can say so. */
let slideReview = null;

function renderReviewPanel(review, names, document) {
  const fileName = document.file_name;
  const open = openFindings(review, names, fileName);
  const tone = open.some(finding => finding.severity === "error") ? "bad"
    : open.length ? "warn" : "ok";
  const checks = !review.reviewed_at
    ? "Pictures and figure references not checked yet."
    : open.length
      ? `The checks found ${open.length} thing(s) to look at.`
      : "The checks found nothing wrong: every picture opened cleanly.";
  const slides = slidesToReview(document);
  const deck = slides[0] !== 0;

  return `
    <div class="panel review-panel ${tone}">
      <div class="panel-head">
        <h3>Review</h3>
      </div>

      <div class="review-actions">
        <button class="btn btn-accent" id="review-slides-button"
                title="The agent looks at each slide beside what was extracted from it, and proposes fixes. One model call per slide.">
          ${slideReview ? "Stop the review"
            : deck ? `Review all ${slides.length} slide${slides.length === 1 ? "" : "s"} with the agent`
            : "Review with the agent"}
        </button>
        <button class="btn" id="review-extraction-button"
                title="Opens every extracted picture and matches every figure reference. No model call.">
          ${review.reviewed_at ? "Check pictures again" : "Check pictures"}
        </button>
      </div>
      <p class="x-review-progress" hidden></p>
      <div class="x-review-slides" data-proposal-slides hidden></div>

      <p class="panel-sub">${escapeHtml(checks)}${
        review.is_stale ? " The extraction has changed since." : ""}</p>

      ${open.map(finding => `
        <div class="finding ${escapeHtml(finding.severity)}">
          ${finding.asset_path ? `
            <img class="finding-thumb" alt="" loading="lazy"
                 src="${projectApiPath(`/extraction/assets/${
                   encodeURIComponent(finding.asset_path.split("/").pop())}`)}">`
            : `<span class="finding-thumb empty">${icon(ICON.alert, 16, 2)}</span>`}
          <div class="finding-body">
            <b>${escapeHtml(finding.what)}</b>
            <span class="finding-where">${escapeHtml(finding.where)}${
              finding.found_by === "agent" ? " · found by the agent" : ""}</span>
            ${finding.suggestion
              ? `<span class="finding-suggestion">${escapeHtml(finding.suggestion)}</span>` : ""}
            <div class="finding-actions">
              ${finding.block_id ? `
                <label class="btn upload-replacement">
                  Upload a picture
                  <input type="file" accept="image/*" hidden
                         data-replace-figure="${escapeHtml(finding.block_id)}">
                </label>` : ""}
              ${finding.block_id ? `
                <button class="btn" data-draw-figure="${escapeHtml(finding.block_id)}"
                        title="Draw one from the surrounding text. It is recorded as
                               generated, not as the author's own figure.">
                  Draw a picture
                </button>` : ""}
              <button class="btn" data-acknowledge="${escapeHtml(finding.id)}">
                It is fine
              </button>
            </div>
          </div>
        </div>`).join("")}

    </div>`;
}

async function runExtractionReview(page) {
  const button = select("#review-extraction-button");
  if (button) {
    button.disabled = true;
    button.textContent = "Checking…";
  }

  try {
    const review = await requestJsonFromApi(
      projectApiPath("/extraction/review"), { method: "POST" });
    applicationState.extractionReview = review;
    showStageNotice(review.error_count ? "warn" : "ok",
      review.open_count
        ? `${review.open_count} thing(s) to look at.`
        : "The checks found nothing wrong.");
  } catch (reviewFailure) {
    console.error("extraction review failed", reviewFailure);
    showStageNotice("bad", reviewFailure.message);
  } finally {
    await page.refresh();
  }
}

/** Walk the slides: one call each, so every answer is small and one slide
 *  that fails loses nothing else. Each answer lands in the chat as it comes;
 *  pressing the button again stops after the slide under way. */
async function runSlideReview(button) {
  if (slideReview) {
    slideReview.stopped = true;
    button.disabled = true;
    button.textContent = "Stopping after this slide…";
    return;
  }
  const fileName = applicationState.previewFileName;
  const document = loaded?.extraction.documents.find(d => d.file_name === fileName);
  if (!document) return;
  const slides = slidesToReview(document);
  const progress = select(".x-review-progress");
  const run = slideReview = { stopped: false };
  const failed = [];
  let conversationId = "";
  let reviewed = 0;
  button.textContent = "Stop the review";
  progress.hidden = false;

  for (const [index, number] of slides.entries()) {
    if (run.stopped || !progress.isConnected) break;
    progress.textContent = number
      ? `Reviewing slide ${number} (${index + 1} of ${slides.length})…` : "Reviewing…";
    showProgress({
      label: number ? `Agent reviewing slide ${number} of ${fileName}` : `Agent reviewing ${fileName}`,
      done: index, total: slides.length > 1 ? slides.length : 0,
    });
    try {
      const thread = await requestJsonFromApi(projectApiPath("/extraction/agent/review-slide"), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          file_name: fileName, slide_number: number, conversation_id: conversationId,
        }),
      });
      conversationId = thread.conversation_id;
      reviewed += 1;
      if (select(".x-agent")?.dataset.agentFor === fileName) showAgentThread(thread);
    } catch (failure) {
      console.error(`reviewing slide ${number} failed`, failure);
      failed.push(number ? `slide ${number} (${failure.message})` : failure.message);
    }
  }
  slideReview = null;
  hideProgress();
  if (!progress.isConnected) return;

  progress.textContent = (slides[0]
    ? `Reviewed ${reviewed} of ${slides.length} slides${run.stopped ? " — stopped" : ""}.`
    : reviewed ? "Reviewed." : "")
    + (failed.length ? ` Could not review ${failed.join("; ")}.` : "");
  button.disabled = false;
  button.textContent = slides[0]
    ? `Review all ${slides.length} slide${slides.length === 1 ? "" : "s"} with the agent`
    : "Review with the agent";
}

function wireReviewPanel(page) {
  const reviewButton = select("#review-extraction-button");
  if (reviewButton) reviewButton.onclick = () => runExtractionReview(page);

  const slidesButton = select("#review-slides-button");
  if (slidesButton) slidesButton.onclick = () => runSlideReview(slidesButton);

  document.querySelectorAll("[data-acknowledge]").forEach(button => {
    button.onclick = async () => {
      try {
        applicationState.extractionReview = await requestJsonFromApi(
          projectApiPath(`/extraction/findings/${
            encodeURIComponent(button.dataset.acknowledge)}/acknowledge`),
          { method: "POST" });
      } catch (acknowledgeFailure) {
        console.error("acknowledge failed", acknowledgeFailure);
        showStageNotice("bad", acknowledgeFailure.message);
        return;
      }
      await page.refresh();
    };
  });

  document.querySelectorAll("[data-draw-figure]").forEach(button => {
    button.onclick = async () => {
      const instruction = window.prompt(
        "Anything the picture must show? (optional) "
        + "It is drawn from the figure's caption and the text around it, and is "
        + "recorded as generated rather than as the author's own figure.", "");
      if (instruction === null) return;
      button.disabled = true;
      button.textContent = "Drawing…";
      try {
        const drawn = await requestJsonFromApi(
          projectApiPath(`/extraction/figures/${
            encodeURIComponent(button.dataset.drawFigure)}/draw`),
          {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ instruction }),
          });
        showStageNotice("ok", `Picture drawn by ${drawn.model} and marked as generated.`);
        await runExtractionReview(page);
      } catch (drawFailure) {
        console.error("drawing a figure failed", drawFailure);
        showStageNotice("bad", drawFailure.message);
        await page.refresh();
      }
    };
  });

  document.querySelectorAll("[data-replace-figure]").forEach(input => {
    input.onchange = async () => {
      const [chosen] = input.files ?? [];
      if (!chosen) return;
      const body = new FormData();
      body.append("file", chosen, chosen.name);
      try {
        await requestJsonFromApi(
          projectApiPath(`/extraction/figures/${
            encodeURIComponent(input.dataset.replaceFigure)}/picture`),
          { method: "POST", body });
        showStageNotice("ok",
          "Picture replaced. Transfer again from the Final tab to hand it to the next layer.");
        // The finding it fixes is only gone once the checks run again.
        await runExtractionReview(page);
      } catch (uploadFailure) {
        console.error("figure replacement failed", uploadFailure);
        showStageNotice("bad", uploadFailure.message);
        await page.refresh();
      }
    };
  });
}

/* ---- the collection: extract one file, remove one, confirm all ----------- */

/** Re-read the extraction after a setting changes, which can make the source
 *  need extracting again, and redraw just the source panel -- redrawing the
 *  stage would re-render a 50 MB deck in the preview for one switch. */
async function refreshCollection() {
  let extraction;
  try {
    extraction = await requestJsonFromApi(projectApiPath("/extraction"));
  } catch (refreshFailure) {
    console.error("collection refresh failed", refreshFailure);
    return;
  }
  if (loaded) loaded.extraction = extraction;
  const panel = document.querySelector(".x-source");
  if (panel) {
    panel.outerHTML = renderSourcePanel(applicationState.selectedProject?.source, extraction);
    wireExtractButton(currentPage);
  }
}

let currentPage = null;

function wireCollection(page) {
  currentPage = page;
  wireExtractButton(page);
  const confirmButton = select("#confirm-extraction-button");
  if (confirmButton && !confirmButton.disabled) {
    confirmButton.onclick = () => confirmCollection(confirmButton, page);
  }
}

function wireExtractButton(page) {
  const button = select("#extract-file-button");
  if (button && !button.disabled) button.onclick = () => extractSource(button, page);
}

/** Read the source file, then show what came out. */
async function extractSource(button, page) {
  const source = applicationState.selectedProject?.source;
  if (applicationState.extractingFileName || !source) return;
  applicationState.extractingFileName = source.name;
  showProgress({ label: `Extracting ${source.name}` });
  button.disabled = true;
  button.textContent = "Extracting…";
  try {
    const result = await requestJsonFromApi(projectApiPath("/extraction/run"), {
      method: "POST", headers: { "Content-Type": "application/json" }, body: "{}",
    });
    const done = result.extracted;
    // Land on what came out: running a stage and seeing no change is the most
    // confusing possible outcome.
    applicationState.extractionTab = "review";
    showStageNotice(done.warnings.length ? "warn" : "ok",
      `Extracted ${done.word_count} words, ${done.block_count} blocks. Review it here, then `
      + `transfer it from Final.${done.warnings.length ? ` ${done.warnings.join(" ")}` : ""}`);
  } catch (runFailure) {
    console.error("extraction failed", runFailure);
    showStageNotice("bad", `Could not extract ${source.name} — ${runFailure.message}`);
  } finally {
    applicationState.extractingFileName = null;
    hideProgress();
  }
  await Promise.all([refreshProjectSummary(), page.refresh()]);
}

/** The hand-off: later stages read this collection from now on. *//** The hand-off: later stages read this collection from now on. */
async function confirmCollection(button, page) {
  button.disabled = true;
  button.textContent = "Transferring…";
  try {
    const confirmed = await requestJsonFromApi(
      projectApiPath("/extraction/confirm"), { method: "POST" });
    showStageNotice("ok",
      `Transferred to the next layer: ${confirmed.total_word_count} words.`);
  } catch (confirmFailure) {
    console.error("confirming the collection failed", confirmFailure);
    showStageNotice("bad", confirmFailure.message);
  }
  await Promise.all([refreshProjectSummary(), page.refresh()]);
}

/** Move one control to a value without redrawing anything else. */
function showOptionValue(optionKey, value) {
  const control = document.querySelector(`[data-option="${CSS.escape(optionKey)}"]`);
  if (!control) return;
  if (control.tagName === "SELECT") {
    control.value = value;
    return;
  }
  control.setAttribute("aria-checked", String(Boolean(value)));
  control.querySelector(".checkbox")?.classList.toggle("on", Boolean(value));
}

async function persistOption(stage, optionKey, newValue, page) {
  // A control that silently does nothing reads as broken. Say why instead
  // of dropping the interaction.
  if (applicationState.isSavingSettings) {
    showStageNotice("warn", "Still saving the last change — try again in a moment.");
    return;
  }
  applicationState.isSavingSettings = true;

  const settings = applicationState.stageSettings[stage.key];
  const previousValue = settings.values[optionKey];

  // Optimistic: the control moves immediately and reverts if the write fails.
  // A toggle that lags behind the pointer feels broken even when it works.
  //
  // In place, not by redrawing the stage. A redraw re-reads the settings from
  // the server, and running before the save is sent would fetch the old value
  // and put the switch straight back.
  settings.values[optionKey] = newValue;
  showOptionValue(optionKey, newValue);

  try {
    const savedSettings = await requestJsonFromApi(
      projectApiPath(`/settings/${stage.key}`),
      {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ values: settings.values }),
      });
    applicationState.stageSettings[stage.key] = savedSettings;

    // Now the save has landed, ask again whether the extraction still matches:
    // a changed option can make it out of date. Only the run bar is redrawn --
    // redrawing the stage would re-download and re-render a 50 MB deck sitting
    // in the Preview tab for the sake of one switch.
    await refreshCollection();

    const savedHint = select("#settings-saved-hint");
    if (savedHint) {
      savedHint.textContent = "saved";
      setTimeout(() => {
        if (savedHint.isConnected) savedHint.textContent = "";
      }, 1600);
    }
  } catch (saveFailure) {
    console.error("settings save failed", saveFailure);
    settings.values[optionKey] = previousValue;
    await page.refresh();
    showStageNotice("bad", `Could not save that setting — ${saveFailure.message}`);
  } finally {
    applicationState.isSavingSettings = false;
  }
}

/* ---- the Extraction agent: a conversation beside the blocks --------------
 *
 * Ask for a change -- merge these, reorder that, rewrite a heading, redraw or
 * edit a picture -- and the agent replies with a proposal. Nothing changes
 * until Apply; the last applied proposal can be undone.
 */

function renderAgentPanel(extraction, fileName) {
  const extracted = extraction.documents.some(d => d.file_name === fileName);
  return `
    <section class="x-agent" data-agent-for="${escapeHtml(fileName)}">
      <div class="x-agent-head">
        <h3 class="x-compare-title">Extraction agent</h3>
        <div class="spacer"></div>
        ${extracted ? `
          <div class="x-agent-history" hidden>
            <button class="btn" data-agent-history aria-expanded="false" aria-haspopup="true">
              History</button>
            <div class="x-agent-history-menu" hidden></div>
          </div>
          <button class="btn" data-agent-new>New chat</button>` : ""}
      </div>
      ${extracted ? `
        <div class="x-agent-log" aria-live="polite">
          <p class="muted x-agent-empty">Loading the conversation…</p>
        </div>
        <form class="x-agent-ask">
          <textarea rows="2" maxlength="2000" aria-label="Message to the extraction agent"
            placeholder="Ask to rewrite, merge, reorder or delete blocks, or to redraw, edit or add a picture…"
          ></textarea>
          <button class="btn btn-accent" type="submit">Send</button>
        </form>`
        : `<p class="muted x-agent-empty">Extract this file to work on it with the agent.</p>`}
    </section>`;
}

const TRASH_ICON = '<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>';

/** A click anywhere outside the History menu closes it. One listener for the
 *  page, not one per redraw. */
document.addEventListener("click", event => {
  if (event.target.closest(".x-agent-history")) return;
  document.querySelectorAll(".x-agent-history-menu:not([hidden])").forEach(menu => {
    menu.hidden = true;
    menu.parentElement.querySelector("[data-agent-history]")?.setAttribute("aria-expanded", "false");
  });
});

const AGENT_STATUS = {
  applied: "Applied", discarded: "Discarded", undone: "Undone",
};

function renderAgentTurn(turn, thread) {
  if (turn.role === "person") {
    return `
      <div class="x-agent-turn person">
        ${turn.slide_number ? `<span class="x-agent-slide">slide ${turn.slide_number}</span>` : ""}
        <p>${escapeHtml(turn.text)}</p>
      </div>`;
  }
  const changes = turn.summaries.map((summary, index) => `
    <li><b>${escapeHtml(summary)}</b>${turn.changes[index]?.reason
      ? `<span>${escapeHtml(turn.changes[index].reason)}</span>` : ""}</li>`).join("");
  const actions = turn.status === "proposed" ? `
      <div class="x-agent-actions">
        <button class="btn btn-accent" data-agent-apply="${turn.id}">Apply changes</button>
        <button class="btn" data-agent-discard="${turn.id}">Discard</button>
      </div>`
    : turn.status ? `
      <div class="x-agent-actions">
        <span class="x-agent-status ${turn.status}">${AGENT_STATUS[turn.status] ?? turn.status}</span>
        ${undoneTogether(thread).at(-1) === turn.id
          ? `<button class="btn" data-agent-undo="${turn.id}">${undoneTogether(thread).length > 1
              ? `Undo all ${undoneTogether(thread).length}` : "Undo"}</button>` : ""}
      </div>` : "";
  return `
    <div class="x-agent-turn agent">
      ${turn.looked_at ? `<span class="x-agent-looked">Looked at ${escapeHtml(turn.looked_at)}</span>` : ""}
      <p>${escapeHtml(turn.text)}</p>
      ${changes ? `<ol class="x-agent-changes">${changes}</ol>` : ""}
      ${turn.notes.map(note => `<p class="x-agent-note">${escapeHtml(note)}</p>`).join("")}
      ${actions}
    </div>`;
}

/** The proposals the next Undo puts back: one, or every one "Apply all" applied. */
const undoneTogether = thread => (thread.undo_turn_id || "").split(",").filter(Boolean);

/** Picture changes call the image model: said before "Apply all" runs. */
const PICTURE_ACTIONS = new Set(["redraw_image", "edit_image", "add_image"]);

/** Set by the agent panel, which owns the requests; the chips call it. */
let applyAllWaiting = null;
/** While "Apply all" runs, its button counts down and cannot start a second run. */
let applyingAll = false;

/** The conversation on screen, so a message goes on in the one being read. */
let agentConversationId = "";

/** The thread on screen, for "Apply all" to walk its waiting proposals. */
let currentThread = { turns: [] };

function showAgentThread(thread) {
  const log = select(".x-agent-log");
  if (!log) return;
  agentConversationId = thread.conversation_id;
  currentThread = thread;

  const history = select(".x-agent-history");
  if (history) {
    history.hidden = !thread.conversations.length;
    history.querySelector(".x-agent-history-menu").innerHTML = thread.conversations.map(chat => `
      <div class="x-agent-history-row${chat.id === thread.conversation_id ? " on" : ""}">
        <button class="x-agent-history-open" data-open-chat="${chat.id}">
          <b>${escapeHtml(chat.title)}</b>
          <span>${chat.started_at ? escapeHtml(whenItWas(chat.started_at)) : ""}${
            chat.turn_count ? ` · ${chat.turn_count} message${chat.turn_count === 1 ? "" : "s"}` : ""}</span>
        </button>
        <button class="x-agent-history-delete" data-delete-chat="${chat.id}"
                title="Delete this chat" aria-label="Delete the chat “${escapeHtml(chat.title)}”">
          ${icon(TRASH_ICON, 15, 2)}</button>
      </div>`).join("");
  }
  showProposalSlides(thread);
  log.innerHTML = thread.turns.length
    ? thread.turns.map(turn => renderAgentTurn(turn, thread)).join("")
    : `<p class="muted x-agent-empty">Review every slide with the agent above, or ask it to
         change what was extracted: rewrite, merge, reorder or delete blocks, or redraw, edit or
         add a picture. It proposes; you apply.</p>`;
  log.scrollTop = log.scrollHeight;
}

/** "Changes waiting on slides 2 · 5 · 9", each a button that shows the slide. */
function showProposalSlides(thread) {
  const box = select("[data-proposal-slides]");
  if (!box) return;
  const proposed = thread.turns.filter(turn => turn.status === "proposed");
  const waiting = [...new Set(proposed.filter(turn => turn.slide_number)
    .map(turn => turn.slide_number))].sort((a, b) => a - b);
  const pictures = proposed.filter(turn =>
    turn.changes.some(change => PICTURE_ACTIONS.has(change.action))).length;
  box.hidden = !waiting.length;
  box.innerHTML = waiting.length ? `
    <span>Changes waiting on slide${waiting.length === 1 ? "" : "s"}</span>
    ${waiting.map(number => `
      <button class="x-slide-chip" data-show-slide="${number}"
              title="Show slide ${number}">${number}</button>`).join("")}
    ${applyingAll ? `<button class="btn x-apply-all" disabled>Applying… ${proposed.length} left</button>`
      : proposed.length > 1 ? `<button class="btn btn-accent x-apply-all" data-apply-all
        data-count="${proposed.length}" data-pictures="${pictures}"
        title="Apply every waiting change, slide by slide. One Undo puts them all back.">
        Apply all ${proposed.length} changes</button>` : ""}` : "";
  box.onclick = event => {
    const all = event.target.closest("[data-apply-all]");
    if (all) {
      applyAllWaiting?.(all);
      return;
    }
    const chip = event.target.closest("[data-show-slide]");
    if (!chip) return;
    const fileName = applicationState.previewFileName;
    stepRawFile(fileName, Number(chip.dataset.showSlide) - 1 - (applicationState.previewSlideIndex ?? 0));
    select(".x-compare")?.scrollIntoView({ block: "start", behavior: "smooth" });
  };
}

/** The slide the agent should look at: the one on screen, for a deck. */
function agentSlideNumber(fileName) {
  const document = loaded?.extraction.documents.find(d => d.file_name === fileName);
  const onSlides = document?.blocks.some(block => block.slide_number);
  return onSlides ? (applicationState.previewSlideIndex ?? 0) + 1 : 0;
}

/** After an apply or an undo: the extraction changed, so the column is drawn
 *  from the new one without refetching anything. */
function showChangedExtraction(extraction, fileName) {
  if (loaded) loaded.extraction = extraction;
  const pane = document.querySelector("[data-extraction-for]");
  if (pane?.dataset.extractionFor === fileName) {
    pane.innerHTML = renderExtractionSide(extraction, fileName, applicationState.previewSlideIndex ?? 0);
  }
  refreshProjectSummary();
}

function wireAgentPanel() {
  const panel = select(".x-agent");
  const fileName = panel?.dataset.agentFor;
  const form = panel?.querySelector(".x-agent-ask");
  if (!form) return;

  const path = `/extraction/agent`;
  const post = (url, body) => requestJsonFromApi(projectApiPath(url), {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ file_name: fileName, ...body }),
  });
  const busy = (button, label, work) => async () => {
    const original = button.textContent;
    button.disabled = true;
    button.textContent = label;
    try {
      await work();
    } catch (failure) {
      console.error("extraction agent failed", failure);
      showStageNotice("bad", failure.message);
      button.disabled = false;
      button.textContent = original;
    }
  };

  applyAllWaiting = button => {
    const count = Number(button.dataset.count);
    const pictures = Number(button.dataset.pictures);
    if (!window.confirm(`Apply all ${count} waiting changes, slide by slide?\n\n`
        + (pictures ? `${pictures} of them redraw, edit or add a picture: each of those is `
          + "a paid call to the image model.\n\n" : "")
        + "One Undo puts every one of them back.")) return;
    // One by one, so each slide's chip goes as its change lands; each apply names
    // the batch so far, so one Undo still puts every one of them back.
    busy(button, "Applying…", async () => {
      const waiting = currentThread.turns.filter(turn => turn.status === "proposed");
      applyingAll = true;
      let batch = "";
      let applied = 0;
      for (const turn of waiting) {
        showProgress({ label: `Applying the changes on slide ${turn.slide_number || "?"}`,
          done: applied, total: waiting.length });
        try {
          const result = await post(`${path}/${turn.id}/apply`, { continues: batch });
          batch = result.thread.undo_turn_id;
          applied += 1;
          showAgentThread(result.thread);
          showChangedExtraction(result.extraction, fileName);
        } catch (failure) {
          applyingAll = false;
          showAgentThread(currentThread);
          hideProgress();
          showStageNotice("warn", `${applied} applied; stopped at slide ${turn.slide_number || "?"}:`
            + ` ${failure.message} ${waiting.length - applied} still waiting.`);
          return;
        }
      }
      applyingAll = false;
      showAgentThread(currentThread);
      hideProgress();
      showStageNotice("ok", `All ${applied} changes applied. Transfer again to hand them to the `
        + "next layer.");
    })();
  };

  requestJsonFromApi(projectApiPath(`${path}?file_name=${encodeURIComponent(fileName)}`))
    .then(showAgentThread)
    .catch(failure => {
      console.error("agent conversation load failed", failure);
      panel.querySelector(".x-agent-log").innerHTML =
        `<p class="muted x-agent-empty">Could not load the conversation — ${escapeHtml(failure.message)}</p>`;
    });

  const newChat = panel.querySelector("[data-agent-new]");
  newChat.onclick = busy(newChat, "Starting…", async () => {
    showAgentThread(await post(`${path}/new`, {}));
    newChat.disabled = false;
    newChat.textContent = "New chat";
    textarea.focus();
  });
  // History: every chat about this file, to reopen one or delete it.
  const toggle = panel.querySelector("[data-agent-history]");
  const menu = panel.querySelector(".x-agent-history-menu");
  const showMenu = open => {
    menu.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
  };
  toggle.onclick = () => showMenu(menu.hidden);
  menu.onclick = async event => {
    const open = event.target.closest("[data-open-chat]");
    const remove = event.target.closest("[data-delete-chat]");
    try {
      if (open) {
        showMenu(false);
        showAgentThread(await requestJsonFromApi(projectApiPath(
          `${path}?file_name=${encodeURIComponent(fileName)}`
          + `&conversation_id=${encodeURIComponent(open.dataset.openChat)}`)));
      } else if (remove) {
        if (!window.confirm("Delete this chat? Any changes it applied stay applied.")) return;
        showAgentThread(await requestJsonFromApi(projectApiPath(
          `${path}/conversations/${encodeURIComponent(remove.dataset.deleteChat)}`
          + `?file_name=${encodeURIComponent(fileName)}`), { method: "DELETE" }));
      }
    } catch (failure) {
      console.error("chat history failed", failure);
      showStageNotice("bad", failure.message);
    }
  };

  const textarea = form.querySelector("textarea");
  const send = form.querySelector('button[type="submit"]');
  form.onsubmit = event => {
    event.preventDefault();
    const message = textarea.value.trim();
    if (!message) return;
    busy(send, "Thinking…", async () => {
      showAgentThread(await post(path, {
        message, slide_number: agentSlideNumber(fileName), conversation_id: agentConversationId,
      }));
      textarea.value = "";
      send.disabled = false;
      send.textContent = "Send";
    })();
  };
  textarea.onkeydown = event => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      form.requestSubmit();
    }
  };

  // The log is redrawn after every step, so its buttons are handled by
  // delegation rather than wired one by one.
  panel.querySelector(".x-agent-log").onclick = event => {
    const apply = event.target.closest("[data-agent-apply]");
    const discard = event.target.closest("[data-agent-discard]");
    const undo = event.target.closest("[data-agent-undo]");
    if (apply) {
      busy(apply, "Applying…", async () => {
        const result = await post(`${path}/${apply.dataset.agentApply}/apply`, {});
        showAgentThread(result.thread);
        showChangedExtraction(result.extraction, fileName);
        showStageNotice("ok", "Changes applied. Transfer again to hand them to the next layer.");
      })();
    } else if (discard) {
      busy(discard, "Discarding…", async () => {
        showAgentThread((await post(`${path}/${discard.dataset.agentDiscard}/discard`, {})).thread);
      })();
    } else if (undo) {
      busy(undo, "Undoing…", async () => {
        const result = await post(`${path}/undo`, {});
        showAgentThread(result.thread);
        showChangedExtraction(result.extraction, fileName);
        showStageNotice("ok", "Undone: those blocks are back as they were.");
      })();
    }
  };
}
