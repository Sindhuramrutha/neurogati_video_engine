/**
 * Extraction stage — the three-column workbench.
 *
 * Files to process | options | preview. Options are declared server-side and
 * rendered generically here, so adding an option is one entry in
 * `stage_options.py` rather than a change in three places.
 */

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
        ${renderPreviewPanel(sources)}
      </div>

      ${renderRunBar(selected.size, sources.length)}
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

function renderPreviewPanel(sources) {
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
        <span class="mono muted">${previewFile ? escapeHtml(previewFile.name) : "—"}</span>
      </div>

      <div class="preview-stage">
        <div class="preview-empty">
          ${icon(ICON.doc, 34, 1.4)}
          <p>${isPreviewTab
            ? "Document rendering is not built yet. This pane will show the selected page."
            : "Nothing extracted yet. Run the stage to see its text output here."}</p>
        </div>
      </div>
    </div>`;
}

function renderRunBar(selectedCount, totalCount) {
  const canRun = selectedCount > 0;
  const disabledReason = totalCount === 0
    ? "Add a source file first"
    : "Select at least one file";

  return `
    <div class="run-bar ${canRun ? "ready" : "blocked"}">
      <span class="run-icon">${icon(canRun ? ICON.check : ICON.alert, 17, canRun ? 2.4 : 2)}</span>
      <span class="run-text">
        <b>${canRun ? "Ready to extract" : "Nothing selected"}</b>
        <span>${canRun
          ? `${selectedCount} of ${totalCount} file(s) selected. Extraction is not implemented yet.`
          : escapeHtml(disabledReason) + "."}</span>
      </span>
      <button class="btn btn-accent" id="run-extraction-button" ${canRun ? "" : "disabled"}
              title="${canRun ? "Not implemented yet" : escapeHtml(disabledReason)}">
        Extract content
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
  const rerender = () => renderExtractionStage(stage, navigateToStage, renderAgentStage);

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
