/**
 * Extraction stage — the run bar, then the workbench.
 *
 * The run bar (status and the Extract button) sits first, so the stage's one
 * action is always in view. Below it, files and options stack on the left and
 * the preview takes the remaining width. Options are declared server-side and
 * rendered generically here, so adding an option is one entry in
 * `stage_options.py` rather than a change in three places.
 */

import {
  openRawFile, releaseRawFile, renderRawFileShell,
} from "/static/raw-file-viewer.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, fileTypeBadge, formatFileSize, icon,
  notBuiltYet, projectApiPath, refreshProjectSummary, select, showStageNotice, sortedSources,
  stageIcon,
} from "/static/ui-kit.js";

/** The files extraction will read: every source except those left out.
 *
 *  Read from the project, not held in the page. The ticks used to live only in
 *  this tab's memory and the run ignored them -- unticking a file changed
 *  nothing, and a reload ticked it again.
 */
function includedSourceNames(sources, extraction) {
  const leftOut = new Set(extraction.freshness?.excluded ?? []);
  return new Set(sources.map(file => file.name).filter(name => !leftOut.has(name)));
}

export async function renderExtractionStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  const sources = sortedSources();

  body.innerHTML = `<div class="card muted">Loading options…</div>`;

  let settings;
  try {
    settings = await requestJsonFromApi(projectApiPath(`/settings/${stage.key}`));
    applicationState.stageSettings[stage.key] = settings;
  } catch (settingsFailure) {
    console.error("settings load failed", settingsFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load extraction options.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(settingsFailure.message)}</p>
    </div>`;
    return;
  }

  // Loaded here rather than lazily on the tab, so the run bar can say what
  // actually exists instead of claiming the stage is unimplemented.
  let extraction = { documents: [], warnings: [], is_empty: true, audit: {} };
  try {
    extraction = await requestJsonFromApi(projectApiPath("/extraction"));
  } catch (extractionFailure) {
    console.error("extraction load failed", extractionFailure);
  }

  const selected = includedSourceNames(sources, extraction);
  if (!applicationState.previewFileName && sources.length) {
    applicationState.previewFileName = sources[0].name;
  }

  body.innerHTML = `
    <div class="card">
      <div class="card-head">
        <span class="card-icon">${stageIcon("extraction", 21)}</span>
        <div>
          <h2>Extraction</h2>
          <p>Pull text and key information out of your documents.</p>
        </div>
        <button class="btn" id="extraction-agent-button">
          ${icon(ICON.gear, 14, 1.8)} Agent &amp; instructions
        </button>
      </div>

      ${renderRunBar(selected.size, sources.length, extraction)}

      <div class="workbench extraction-workbench">
        <div class="workbench-side">
          ${renderFilePanel(sources, selected, extraction)}
          ${renderOptionsPanel(settings)}
        </div>
        ${renderPreviewPanel(sources, extraction, selected)}
      </div>

      ${renderFooterNav(stage)}
    </div>`;

  wireExtractionStage(stage, sources, navigateToStage, renderAgentStage);
}

/** What one file's card says about it, from the server's view of the run.
 *
 *  Per file, because "which of my files made it in?" was answerable only by
 *  reading the run bar's sentence. Checked in the order that matters to someone
 *  deciding whether to re-run: a choice to leave it out first, then whether the
 *  current extraction actually contains it.
 */
function fileStatus(file, selected, extraction) {
  const freshness = extraction.freshness ?? {};
  const extracted = extraction.documents.find(d => d.file_name === file.name);

  if (!selected.has(file.name)) {
    return extracted
      ? { tone: "warn", text: "left out · still in the last run" }
      : { tone: "muted", text: "left out" };
  }
  if (!extracted) {
    // Before any run, nothing is behind; after one, a missing file is.
    return freshness.has_run
      ? { tone: "warn", text: "not extracted yet" }
      : { tone: "muted", text: "ready to extract" };
  }
  const figures = extracted.blocks.filter(block => block.kind === "figure").length;
  return {
    tone: "ok",
    text: `${extracted.blocks.length} blocks${figures ? ` · ${figures} figures` : ""}`,
  };
}

function renderFileStatus(file, selected, extraction) {
  const status = fileStatus(file, selected, extraction);
  return `<span class="file-status ${status.tone}"
                data-status-for="${escapeHtml(file.name)}">${escapeHtml(status.text)}</span>`;
}

function renderFilePanel(sources, selected, extraction) {
  return `
    <div class="panel">
      <div class="panel-head"><h3 id="files-to-process-heading">${
        filesToProcessHeading(selected.size, sources.length)}</h3></div>

      ${sources.length ? sources.map(file => `
        <button class="file-card ${applicationState.previewFileName === file.name ? "selected" : ""}
                       ${selected.has(file.name) ? "" : "left-out"}"
                data-preview="${escapeHtml(file.name)}" title="View ${escapeHtml(file.name)}"
                aria-current="${applicationState.previewFileName === file.name}">
          ${fileTypeBadge(file.suffix)}
          <span class="meta">
            <span class="name">${escapeHtml(file.name)}</span>
            <span class="sub">${formatFileSize(file.bytes)}</span>
            ${renderFileStatus(file, selected, extraction)}
          </span>
          <span class="checkbox ${selected.has(file.name) ? "on" : ""}"
                data-toggle-file="${escapeHtml(file.name)}" role="checkbox"
                aria-checked="${selected.has(file.name)}"
                title="${selected.has(file.name) ? "Included in extraction" : "Left out of extraction"}"
                aria-label="Include ${escapeHtml(file.name)}">
            ${icon(ICON.check, 11, 3.5)}
          </span>
        </button>`).join("")
        : `<p class="muted" style="font-size:12.5px;margin:0 0 10px">
             No sources yet. Add them on the Inputs stage.</p>`}

      <button class="btn" id="add-more-files-button"
              style="width:100%;justify-content:center;margin-top:10px">
        ${icon(ICON.plus)} Add more files
      </button>
    </div>`;
}

function renderOptionsPanel(settings) {
  // Built options first and in full; the ones nothing reads yet fold away. Four
  // disabled placeholders used to fill most of this panel and push the two
  // switches that do something into the middle of it.
  const built = settings.options.filter(option => option.implemented !== false);
  const planned = settings.options.filter(option => option.implemented === false);
  const renderControl = option => {
    const currentValue = settings.values[option.key];

    if (option.kind === "choice") {
      const activeChoice = option.choices.find(choice => choice.value === currentValue);
      const inert = option.implemented === false;
      return `
        <div class="option${inert ? " inert" : ""}">
          <label for="opt-${escapeHtml(option.key)}">${escapeHtml(option.label)}
            ${notBuiltYet(option)}</label>
          <select id="opt-${escapeHtml(option.key)}" data-option="${escapeHtml(option.key)}"
                  ${inert ? "disabled" : ""}>
            ${option.choices.map(choice => `
              <option value="${escapeHtml(choice.value)}"
                      ${choice.value === currentValue ? "selected" : ""}>
                ${escapeHtml(choice.label)}</option>`).join("")}
          </select>
          <p class="help">${escapeHtml(activeChoice?.help_text ?? option.help_text)}</p>
        </div>`;
    }

    const inert = option.implemented === false;
    return `
      <button class="toggle-row${inert ? " inert" : ""}" data-option="${escapeHtml(option.key)}"
              role="switch" aria-checked="${currentValue}" ${inert ? "disabled" : ""}
              title="${escapeHtml(option.help_text)}">
        <span class="switch ${currentValue && !inert ? "on" : ""}"></span>
        <span class="toggle-label">${escapeHtml(option.label)}</span>
        ${notBuiltYet(option)}
      </button>`;
  };

  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Extraction options</h3>
        <span class="info-dot"
              title="Saved with the project and used the next time this stage runs.">i</span>
        <div class="spacer"></div>
        <span class="mono muted" id="settings-saved-hint"></span>
      </div>
      ${built.map(renderControl).join("")}
      ${planned.length ? `
        <details class="planned-options">
          <summary>Planned options <span class="not-built">not built yet</span>
            <span class="count">${planned.length}</span></summary>
          ${planned.map(renderControl).join("")}
        </details>` : ""}
    </div>`;
}

/** Blocks carry the heading they sit under, so extracted text reads back with
 *  its structure rather than as a wall of paragraphs. */
function renderExtractedBlocks(extraction, selected) {
  const previewName = applicationState.previewFileName;
  // Only ever the file whose name is in the header. Falling back to the first
  // extracted document put a deck's 408 blocks under a Word document's name
  // whenever the Word document had been left out.
  const parsed = extraction.documents.find(d => d.file_name === previewName);

  if (!parsed) {
    const message = !previewName
      ? "No file selected."
      : !selected.has(previewName)
        ? `<b>${escapeHtml(previewName)}</b> is left out of extraction.<br>
           Tick it in the file list to include it in the next run.`
        : extraction.is_empty
          ? "Nothing extracted yet.<br>Extract to see what is inside your documents."
          : `<b>${escapeHtml(previewName)}</b> has not been extracted yet.<br>
             Re-extract to see what is inside it.`;
    return `<div class="preview-empty">${icon(ICON.doc, 34, 1.4)}<p>${message}</p></div>`;
  }

  const rows = parsed.blocks.slice(0, 400).map(block => {
    if (block.kind === "heading") {
      return `<div class="x-block x-heading" style="--depth:${block.level}">${
        escapeHtml(block.text)}</div>`;
    }
    if (block.kind === "table") {
      return `<pre class="x-block x-table">${escapeHtml(block.text)}</pre>`;
    }
    if (block.kind === "list_item") {
      return `<div class="x-block x-list">${escapeHtml(block.text)}</div>`;
    }
    if (block.kind === "figure") return renderFigureBlock(block);
    return `<div class="x-block">${escapeHtml(block.text)}</div>`;
  }).join("");

  const truncated = parsed.blocks.length > 400
    ? `<p class="muted" style="font-size:11.5px">showing the first 400 of ${
        parsed.blocks.length} blocks</p>`
    : "";

  return `<div class="x-doc">
    <div class="x-doc-head">${escapeHtml(parsed.file_name)} &middot; ${
      parsed.blocks.length} blocks</div>${rows}${truncated}</div>`;
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

function renderPreviewPanel(sources, extraction, selected) {
  const previewFile = sources.find(file => file.name === applicationState.previewFileName);
  const isPreviewTab = applicationState.previewTab === "preview";

  return `
    <div class="panel preview-panel">
      <div class="preview-head">
        <div class="seg">
          <button class="${isPreviewTab ? "on" : ""}" data-preview-tab="preview">Preview</button>
          <button class="${isPreviewTab ? "" : "on"}" data-preview-tab="text">Extracted text</button>
        </div>
        <div class="spacer"></div>
        <span class="mono muted" title="${previewFile ? escapeHtml(previewFile.name) : ""}"
              >${previewFile ? escapeHtml(previewFile.name) : "—"}</span>
      </div>

      <div class="preview-stage${isPreviewTab ? " raw" : " scrolls"}">
        ${!isPreviewTab
          ? renderExtractedBlocks(extraction, selected)
          : previewFile
            ? `<div data-raw-host="${escapeHtml(previewFile.name)}">
                 <p class="muted" style="margin:0">Opening ${escapeHtml(previewFile.name)}…</p>
               </div>`
            : `<div class="preview-empty">
                 ${icon(ICON.doc, 34, 1.4)}
                 <p>No file to show.<br>Add one on the Inputs stage.</p>
               </div>`}
      </div>
    </div>`;
}

/** The file itself, in the Preview tab: the same raw rendering as Inputs.
 *
 *  This tab used to say "Document rendering is not built yet" while the Inputs
 *  stage, one click away, drew the same deck slide by slide.
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
    openRawFile(host, fileName, preview.viewer);
  } catch (previewFailure) {
    console.error("preview failed", previewFailure);
    if (host.isConnected) {
      host.innerHTML = `<p class="muted" style="margin:0">Could not open this file —
        ${escapeHtml(previewFailure.message)}</p>`;
    }
  }
}

function renderRunBar(selectedCount, totalCount, extraction) {
  const canRun = selectedCount > 0;
  const hasExtracted = !extraction.is_empty;
  const freshness = extraction.freshness ?? {};

  // Out of date beats "Extracted": a green tick over content that is missing a
  // whole document is how that gap went unnoticed until an agent reported it.
  if (hasExtracted && freshness.is_stale) {
    const missing = freshness.added ?? [];
    const gone = freshness.removed ?? [];
    const changed = (freshness.options_changed ?? []).map(key => key.replaceAll("_", " "));
    const unticked = freshness.newly_excluded ?? [];
    const detail = [
      missing.length ? `not extracted: ${missing.join(", ")}` : "",
      unticked.length ? `left out since the last run: ${unticked.join(", ")}` : "",
      gone.length ? `no longer in the project: ${gone.join(", ")}` : "",
      changed.length ? `options changed since the last run: ${changed.join(", ")}` : "",
    ].filter(Boolean).join(" · ");

    return `
      <div class="run-bar stale">
        <span class="run-icon">${icon(ICON.alert, 17, 2.2)}</span>
        <span class="run-text">
          <b>Out of date with your files</b>
          <span>${escapeHtml(detail)}. Re-extract so later stages see them.</span>
        </span>
        <button class="btn btn-accent" id="run-extraction-button" ${canRun ? "" : "disabled"}
                title="Parse every source document again">Re-extract</button>
      </div>`;
  }

  const disabledReason = totalCount === 0
    ? "Add a source file first"
    : "Select at least one file";

  const summary = hasExtracted
    ? `${extraction.audit.document_count} document(s) - ${extraction.audit.block_count} blocks`
      + ` - ${extraction.audit.figure_count ?? 0} figures`
      // Stated when there is something to state: an option that captured
      // nothing looks exactly like one that was never switched on.
      + (extraction.audit.slide_layout_count
        ? ` - layout for ${extraction.audit.slide_layout_count} slide(s)` : "")
      + (extraction.audit.themed_document_names?.length
        ? ` - ${extraction.audit.themed_document_names.length} deck design(s)` : "")
      + (totalCount > selectedCount ? ` - ${totalCount - selectedCount} left out` : "")
      + ` - ${extraction.total_word_count} words (~${
          extraction.estimated_narration_minutes} min narrated)`
    : `${selectedCount} of ${totalCount} file(s) selected.`;

  return `
    <div class="run-bar ${canRun || hasExtracted ? "ready" : "blocked"}">
      <span class="run-icon">${icon(canRun || hasExtracted ? ICON.check : ICON.alert, 17,
                                    canRun || hasExtracted ? 2.4 : 2)}</span>
      <span class="run-text">
        <b>${hasExtracted ? "Extracted" : canRun ? "Ready to extract" : "Nothing selected"}</b>
        <span>${canRun || hasExtracted
          ? escapeHtml(summary)
          : escapeHtml(disabledReason) + "."}</span>
      </span>
      ${extraction.warnings?.length
        ? `<span class="stage-chip unrouted">${escapeHtml(extraction.warnings[0])}</span>`
        : ""}
      <button class="btn btn-accent" id="run-extraction-button" ${canRun ? "" : "disabled"}
              title="${canRun ? "Parse every source document" : escapeHtml(disabledReason)}">
        ${hasExtracted ? "Re-extract" : "Extract content"}
      </button>
    </div>`;
}


function renderFooterNav(stage) {
  const { stageDefinitions } = applicationState;
  const stageIndex = stageDefinitions.findIndex(s => s.key === stage.key);
  const previousStage = stageDefinitions[stageIndex - 1];
  const nextStage = stageDefinitions[stageIndex + 1];

  return `
    <div class="footer-nav">
      ${previousStage ? `
        <button class="btn" data-goto="${previousStage.key}">
          ${icon(ICON.arrowLeft)} Back to ${escapeHtml(previousStage.title)}
        </button>` : ""}
      <div class="spacer"></div>
      ${nextStage ? `
        <button class="btn btn-accent" data-goto="${nextStage.key}">
          Next: ${escapeHtml(nextStage.title)} ${icon(ICON.arrowRight)}
        </button>` : ""}
    </div>`;
}

function wireExtractionStage(stage, sources, navigateToStage, renderAgentStage) {
  // A redraw replaces the preview, so a rendered deck in it is released first
  // rather than left as detached slides nobody can see.
  const rerender = () => {
    releaseRawFile(applicationState.previewFileName);
    return renderExtractionStage(stage, navigateToStage, renderAgentStage);
  };

  openPreviewedFile();

  document.querySelectorAll("[data-preview]").forEach(card => {
    card.onclick = event => {
      // The checkbox lives inside the card; clicking it must not also change
      // which file is previewed.
      if (event.target.closest("[data-toggle-file]")) return;
      applicationState.previewFileName = card.dataset.preview;
      rerender();
    };
  });

  document.querySelectorAll("[data-toggle-file]").forEach(checkbox => {
    checkbox.onclick = event => {
      event.stopPropagation();
      toggleFileInclusion(checkbox, rerender);
    };
  });

  document.querySelectorAll("[data-preview-tab]").forEach(tab => {
    tab.onclick = () => {
      applicationState.previewTab = tab.dataset.previewTab;
      rerender();
    };
  });

  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });

  select("#add-more-files-button").onclick = () => navigateToStage("inputs");

  const runButton = select("#run-extraction-button");
  if (runButton && !runButton.disabled) {
    runButton.onclick = () => runExtraction(runButton, rerender);
  }

  // The AGENT.md is the real "settings" for this stage: it governs behaviour.
  select("#extraction-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-option]").forEach(control => {
    if (control.disabled) return;
    const optionKey = control.dataset.option;
    if (control.tagName === "SELECT") {
      control.onchange = () => persistOption(stage, optionKey, control.value, rerender);
    } else {
      control.onclick = () => {
        const currentValue = applicationState.stageSettings[stage.key].values[optionKey];
        persistOption(stage, optionKey, !currentValue, rerender);
      };
    }
  });
}

/** Redraw the run bar from the server's current view of the extraction. */
async function refreshRunBar(rerender) {
  const bar = document.querySelector(".run-bar");
  if (!bar) return;

  let extraction;
  try {
    extraction = await requestJsonFromApi(projectApiPath("/extraction"));
  } catch (refreshFailure) {
    console.error("run bar refresh failed", refreshFailure);
    return;
  }
  if (!bar.isConnected) return;

  const sources = sortedSources();
  const included = includedSourceNames(sources, extraction);
  bar.outerHTML = renderRunBar(included.size, sources.length, extraction);

  const heading = select("#files-to-process-heading");
  if (heading) heading.textContent = filesToProcessHeading(included.size, sources.length);

  for (const file of sources) {
    const badge = document.querySelector(`[data-status-for="${CSS.escape(file.name)}"]`);
    if (badge) badge.outerHTML = renderFileStatus(file, included, extraction);
  }

  const runButton = select("#run-extraction-button");
  if (runButton && !runButton.disabled) {
    runButton.onclick = () => runExtraction(runButton, rerender);
  }
}

function filesToProcessHeading(includedCount, totalCount) {
  return includedCount === totalCount
    ? `Files to process (${totalCount})`
    : `Files to process (${includedCount} of ${totalCount})`;
}

/** Tick or untick a file for extraction, saved with the project.
 *
 *  The tick moves at once; the run bar is then redrawn from the server, which is
 *  what decides whether the extraction still matches. Unticking a file that was
 *  extracted makes it out of date -- later stages are still reading it -- while
 *  a file that was never extracted can be left out without any warning at all.
 */
async function toggleFileInclusion(checkbox, rerender) {
  if (applicationState.isSavingSettings) {
    showStageNotice("warn", "Still saving the last change — try again in a moment.");
    return;
  }
  applicationState.isSavingSettings = true;

  const include = !checkbox.classList.contains("on");
  showFileIncluded(checkbox, include);
  const excluded = [...document.querySelectorAll("[data-toggle-file]")]
    .filter(box => !box.classList.contains("on"))
    .map(box => box.dataset.toggleFile);

  try {
    await requestJsonFromApi(projectApiPath("/extraction/sources"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ excluded }),
    });
    await refreshRunBar(rerender);
  } catch (saveFailure) {
    console.error("file selection save failed", saveFailure);
    showFileIncluded(checkbox, !include);
    showStageNotice("bad", `Could not save that choice — ${saveFailure.message}`);
  } finally {
    applicationState.isSavingSettings = false;
  }
}

function showFileIncluded(checkbox, included) {
  checkbox.classList.toggle("on", included);
  checkbox.setAttribute("aria-checked", String(included));
  checkbox.title = included ? "Included in extraction" : "Left out of extraction";
  checkbox.closest(".file-card")?.classList.toggle("left-out", !included);
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
  control.querySelector(".switch")?.classList.toggle("on", Boolean(value));
}

async function persistOption(stage, optionKey, newValue, rerender) {
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
  // the server, and it used to run *before* the save was sent -- so it fetched
  // the old value and put the switch straight back. Every toggle here looked
  // dead while quietly saving.
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
    await refreshRunBar(rerender);

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
    await rerender();
    showStageNotice("bad", `Could not save that setting — ${saveFailure.message}`);
  } finally {
    applicationState.isSavingSettings = false;
  }
}


/** Parse every source document, then show what came out.
 *
 *  Extraction runs synchronously server-side and takes real time on a large PDF,
 *  so the button says what it is doing rather than going inert: a control that
 *  looks frozen is indistinguishable from one that is broken.
 */
async function runExtraction(button, rerender) {
  const originalLabel = button.textContent;
  button.disabled = true;
  button.textContent = "Extracting...";

  try {
    const result = await requestJsonFromApi(
      projectApiPath("/extraction/run"), { method: "POST" });

    // Land on the tab that shows the result. Running a stage and seeing no
    // visible change is the most confusing possible outcome.
    applicationState.previewTab = "text";
    await refreshProjectSummary();
    await rerender();

    showStageNotice(
      result.warnings.length ? "warn" : "ok",
      result.warnings.length
        ? result.warnings.join(" - ")
        : `Extracted ${result.total_word_count} words from ${
            result.audit.document_count} document(s).`);
  } catch (runFailure) {
    console.error("extraction run failed", runFailure);
    button.disabled = false;
    button.textContent = originalLabel;
    showStageNotice("bad", `Extraction failed - ${runFailure.message}`);
  }
}
