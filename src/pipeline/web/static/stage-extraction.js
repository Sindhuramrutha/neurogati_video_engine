/**
 * Extraction stage — the three-column workbench.
 *
 * Files to process | options | preview. Options are declared server-side and
 * rendered generically here, so adding an option is one entry in
 * `stage_options.py` rather than a change in three places.
 */

import {
  openRawFile, releaseRawFile, renderRawFileShell,
} from "/static/raw-file-viewer.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, fileTypeBadge, formatFileSize, icon,
  projectApiPath, select, showStageNotice, sortedSources, stageIcon,
} from "/static/ui-kit.js";

/** Default to everything selected. An explicit empty Set is a real state and
 *  must not be confused with "not chosen yet", which is why null is used for
 *  the latter rather than an empty collection. */
function selectedSourceNames(sources) {
  if (applicationState.selectedSourceNames === null) {
    return new Set(sources.map(file => file.name));
  }
  return applicationState.selectedSourceNames;
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

  const selected = selectedSourceNames(sources);
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

      <div class="workbench">
        ${renderFilePanel(sources, selected)}
        ${renderOptionsPanel(settings)}
        ${renderPreviewPanel(sources, extraction)}
      </div>

      ${renderRunBar(selected.size, sources.length, extraction)}
      ${renderFooterNav(stage)}
    </div>`;

  wireExtractionStage(stage, sources, navigateToStage, renderAgentStage);
}

function renderFilePanel(sources, selected) {
  return `
    <div class="panel">
      <div class="panel-head"><h3>Files to process (${sources.length})</h3></div>

      ${sources.length ? sources.map(file => `
        <button class="file-card ${applicationState.previewFileName === file.name ? "selected" : ""}"
                data-preview="${escapeHtml(file.name)}">
          ${fileTypeBadge(file.suffix)}
          <span class="meta">
            <span class="name">${escapeHtml(file.name)}</span>
            <span class="sub">${formatFileSize(file.bytes)}</span>
          </span>
          <span class="checkbox ${selected.has(file.name) ? "on" : ""}"
                data-toggle-file="${escapeHtml(file.name)}" role="checkbox"
                aria-checked="${selected.has(file.name)}"
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
  const controls = settings.options.map(option => {
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
              role="switch" aria-checked="${currentValue}"
              title="${escapeHtml(option.help_text)}">
        <span class="switch ${currentValue ? "on" : ""}"></span>
        <span class="toggle-label">${escapeHtml(option.label)}</span>
      </button>`;
  }).join("");

  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Extraction options</h3>
        <span class="info-dot"
              title="Saved with the project and used the next time this stage runs.">i</span>
        <div class="spacer"></div>
        <span class="mono muted" id="settings-saved-hint"></span>
      </div>
      ${controls}
    </div>`;
}

/** Blocks carry the heading they sit under, so extracted text reads back with
 *  its structure rather than as a wall of paragraphs. */
function renderExtractedBlocks(extraction) {
  const previewName = applicationState.previewFileName;
  const parsed = extraction.documents.find(d => d.file_name === previewName)
    ?? extraction.documents[0];

  if (!parsed) {
    return `<div class="preview-empty">
      ${icon(ICON.doc, 34, 1.4)}
      <p>Nothing extracted yet.<br>Run the stage to parse your documents.</p>
    </div>`;
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

function renderPreviewPanel(sources, extraction) {
  const previewFile = sources.find(file => file.name === applicationState.previewFileName);
  const isPreviewTab = applicationState.previewTab === "preview";

  return `
    <div class="panel">
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
          ? renderExtractedBlocks(extraction)
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
    const detail = [
      missing.length ? `not extracted: ${missing.join(", ")}` : "",
      gone.length ? `no longer in the project: ${gone.join(", ")}` : "",
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
      const fileName = checkbox.dataset.toggleFile;
      const selected = new Set(selectedSourceNames(sources));
      if (selected.has(fileName)) selected.delete(fileName);
      else selected.add(fileName);
      applicationState.selectedSourceNames = selected;
      rerender();
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
  settings.values[optionKey] = newValue;
  await rerender();

  try {
    const savedSettings = await requestJsonFromApi(
      projectApiPath(`/settings/${stage.key}`),
      {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ values: settings.values }),
      });
    applicationState.stageSettings[stage.key] = savedSettings;

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
