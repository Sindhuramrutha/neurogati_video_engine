/**
 * Scripting stage — narration per plan section, plus scenarios and variables.
 *
 * The section list is the *plan's*, not a copy: bodies are keyed by
 * `PlanSection.id`, so renaming or reordering in Planning carries the narration
 * with it. Deleting a section leaves its text orphaned rather than destroyed, and
 * the server reports that so it is visible instead of silent.
 */

import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, icon, projectApiPath, select,
  showStageNotice, stageIcon,
} from "/static/ui-kit.js";

/** View-only state: which section is open, which pane is showing, and whether a
 *  save is in flight. None of it belongs in the saved script. */
const scriptViewState = {
  activeSectionId: null,
  editorTab: "script",
  pendingSaveTimer: null,
};

/** Typing saves on a debounce rather than per keystroke: a POST per character
 *  would be wasteful and would make every save a potential conflict with the
 *  next one. */
const SCRIPT_AUTOSAVE_DELAY_MS = 700;

export async function renderScriptingStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  body.innerHTML = `<div class="card muted">Loading script…</div>`;

  let script;
  try {
    script = await loadStageDocument("script", "/script");
    if (script === null) return;
  } catch (loadFailure) {
    console.error("script load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load the script.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }

  const sections = script.plan_sections;
  if (!sections.length) {
    body.innerHTML = `
      <div class="card">
        ${scriptingHeader(stage)}
        <div class="empty">
          <h3>No sections to write for</h3>
          <p>Scripting writes narration per plan section. Build the outline first.</p>
          <button class="btn btn-accent" data-goto="planning">
            ${icon(ICON.arrowLeft)} Go to Planning</button>
        </div>
      </div>`;
    wireNavigation(navigateToStage);
    select("#scripting-agent-button").onclick = () => renderAgentStage(stage);
    return;
  }

  // Keep the selection valid across a plan edit that removed the open section.
  if (!sections.some(section => section.id === scriptViewState.activeSectionId)) {
    scriptViewState.activeSectionId = sections[0].id;
  }

  body.innerHTML = `
    <div class="card">
      ${scriptingHeader(stage)}

      ${script.warnings.length ? `
        <div class="notice warn" style="margin-bottom:14px">
          ${script.warnings.map(escapeHtml).join(" · ")}
        </div>` : ""}

      <div class="script-grid">
        ${renderSectionList(script, sections)}
        ${renderEditor(script, sections)}
        <div>
          ${renderScenarioPanel(script)}
          ${renderVariablePanel(script)}
        </div>
      </div>

      ${renderFooterNav(stage, script)}
    </div>`;

  wireScriptingStage(stage, navigateToStage, renderAgentStage);
}

function scriptingHeader(stage) {
  return `
    <div class="card-head">
      <span class="card-icon">${stageIcon("scripting", 21)}</span>
      <div>
        <h2>Scripting</h2>
        <p>Write the narration for each section, and the scenarios it can be told in.</p>
      </div>
      <button class="btn" id="scripting-agent-button">
        ${icon(ICON.gear, 14, 1.8)} Agent &amp; instructions
      </button>
    </div>`;
}

/* ---- panels ------------------------------------------------------------- */

function renderSectionList(script, sections) {
  const writtenCount = sections.filter(
    section => (script.per_section[section.id]?.word_count ?? 0) > 0).length;

  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Sections</h3>
        <div class="spacer"></div>
        <span class="plan-total">${writtenCount}/${sections.length}</span>
      </div>
      <p class="panel-sub">From the plan. Edit the outline in Planning.</p>

      ${sections.map((section, index) => {
        const stats = script.per_section[section.id];
        const isWritten = (stats?.word_count ?? 0) > 0;
        return `
          <button class="section-row ${scriptViewState.activeSectionId === section.id ? "active" : ""}"
                  data-section="${section.id}">
            <span class="outline-num">${index + 1}</span>
            <span class="body">
              <span class="title ${section.title ? "" : "untitled"}"
                >${escapeHtml(section.title || "Untitled section")}</span>
              <span class="sub">${isWritten
                ? `${stats.word_count}w · ~${stats.estimated_seconds}s`
                : "not written"}</span>
            </span>
            <span class="written-dot ${isWritten ? "written" : ""}"
                  title="${isWritten ? "Has narration" : "No narration yet"}"></span>
          </button>`;
      }).join("")}
    </div>`;
}

function renderEditor(script, sections) {
  const activeSection = sections.find(s => s.id === scriptViewState.activeSectionId);
  const body = script.section_scripts
    .find(s => s.section_id === scriptViewState.activeSectionId)?.body ?? "";
  const isScriptTab = scriptViewState.editorTab === "script";
  const lineCount = body ? body.split("\n").length : 1;
  const stats = script.per_section[activeSection.id];

  return `
    <div class="panel editor-shell">
      <div class="editor-bar">
        <div class="seg">
          <button class="${isScriptTab ? "on" : ""}" data-editor-tab="script">Script</button>
          <button class="${isScriptTab ? "" : "on"}" data-editor-tab="preview">Preview</button>
        </div>
        <div class="spacer"></div>
        <span class="mono muted">${escapeHtml(activeSection.title || "Untitled section")}</span>
      </div>

      ${isScriptTab ? `
        <div class="editor-wrap">
          <div class="gutter" id="line-gutter">${
            Array.from({ length: lineCount }, (_, i) => i + 1).join("\n")}</div>
          <textarea class="script-body" id="script-body" spellcheck="true"
                    placeholder="Write the narration for this section.&#10;&#10;Use {{VARIABLE}} for values that change between runs."
                    aria-label="Narration for ${escapeHtml(activeSection.title || "this section")}"
                    >${escapeHtml(body)}</textarea>
        </div>`
        : `<div class="script-preview">${renderPreview(script, body)}</div>`}

      <div class="editor-foot">
        <span>Lines ${lineCount}</span>
        <span>Words ${stats?.word_count ?? 0}</span>
        <span>~${stats?.estimated_seconds ?? 0} sec</span>
        <div class="spacer"></div>
        <span id="script-save-hint"></span>
      </div>
    </div>`;
}

/** Substitute defined variables; leave unknown ones visible and highlighted.
 *  Silently blanking an undefined variable would hide the mistake until it
 *  reached narration. */
function renderPreview(script, body) {
  if (!body.trim()) {
    return `<span class="muted">Nothing written for this section yet.</span>`;
  }
  const values = Object.fromEntries(
    script.variables.filter(v => v.name).map(v => [v.name.toUpperCase(), v.value]));

  return escapeHtml(body).replace(/\{\{\s*([A-Za-z0-9_]+)\s*\}\}/g, (whole, name) => {
    const value = values[name.toUpperCase()];
    return value !== undefined
      ? escapeHtml(value)
      : `<span class="var-unresolved" title="Not defined">${escapeHtml(whole)}</span>`;
  });
}

function renderScenarioPanel(script) {
  return `
    <div class="panel" style="margin-bottom:14px">
      <div class="panel-head">
        <h3>Scenarios</h3>
        <div class="spacer"></div>
        <button class="btn-icon" id="add-scenario-button"
                title="Add scenario" aria-label="Add scenario">${icon(ICON.plus, 15)}</button>
      </div>
      <p class="panel-sub">The same content, told for a different viewer.</p>

      ${script.scenarios.length ? script.scenarios.map(scenario => `
        <div class="scenario-row ${scenario.id === script.active_scenario_id ? "active" : ""}"
             data-scenario="${scenario.id}" role="radio"
             aria-checked="${scenario.id === script.active_scenario_id}" tabindex="0">
          <span class="radio"></span>
          <span class="body">
            <span class="name">${escapeHtml(scenario.name || "Unnamed")}${
              scenario.id === script.active_scenario_id
                ? `<span class="badge-default">active</span>` : ""}</span>
            <span class="desc">${escapeHtml(scenario.description)}</span>
          </span>
          <button class="btn-icon danger" data-delete-scenario="${scenario.id}"
                  title="Remove" aria-label="Remove ${escapeHtml(scenario.name)}">
            ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 14)}
          </button>
        </div>`).join("")
        : `<p class="muted" style="font-size:12.5px;margin:0">None yet.</p>`}
    </div>`;
}

function renderVariablePanel(script) {
  const undefinedNames = new Set(script.audit.undefined_variables);

  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Script variables</h3>
        <span class="info-dot"
              title="Written as {{NAME}} in a script and replaced on output.">i</span>
        <div class="spacer"></div>
        <button class="btn-icon" id="add-variable-button"
                title="Add variable" aria-label="Add variable">${icon(ICON.plus, 15)}</button>
      </div>

      ${script.variables.length ? script.variables.map(variable => `
        <div class="variable-row ${variable.name && !/^[A-Z][A-Z0-9_]*$/.test(variable.name)
              ? "invalid" : ""}">
          <span class="var-name">{{${escapeHtml(variable.name || "?")}}}</span>
          <span class="var-value" data-edit-variable="${variable.id}"
                title="Click to edit">${escapeHtml(variable.value || "(empty)")}</span>
          <button class="btn-icon danger" data-delete-variable="${variable.id}"
                  title="Remove" aria-label="Remove variable">
            ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 14)}
          </button>
        </div>`).join("")
        : `<p class="muted" style="font-size:12.5px;margin:0">None defined.</p>`}

      ${undefinedNames.size ? `
        <p class="muted" style="font-size:11.5px;margin:9px 0 0;color:var(--warn)">
          Used but not defined: ${[...undefinedNames].map(escapeHtml).join(", ")}
        </p>` : ""}
    </div>`;
}

function renderFooterNav(stage, script) {
  const { stageDefinitions } = applicationState;
  const stageIndex = stageDefinitions.findIndex(s => s.key === stage.key);
  const previousStage = stageDefinitions[stageIndex - 1];
  const nextStage = stageDefinitions[stageIndex + 1];
  const hasAnyNarration = script.total_word_count > 0;

  return `
    <div class="footer-nav">
      ${previousStage ? `
        <button class="btn" data-goto="${previousStage.key}">
          ${icon(ICON.arrowLeft)} Back to ${escapeHtml(previousStage.title)}
        </button>` : ""}
      <span class="plan-total" style="margin-left:14px">
        ${script.total_word_count} words · ~${Math.round(script.total_estimated_seconds / 60)} min
      </span>
      <div class="spacer"></div>
      ${nextStage ? `
        <button class="btn btn-accent" data-goto="${nextStage.key}"
                ${hasAnyNarration ? "" : "disabled"}
                title="${hasAnyNarration ? "" : "Write narration for at least one section"}">
          Next: ${escapeHtml(nextStage.title)} ${icon(ICON.arrowRight)}
        </button>` : ""}
    </div>`;
}

/* ---- persistence -------------------------------------------------------- */

function showSaveHint(text) {
  const hint = select("#script-save-hint");
  if (!hint) return;
  hint.textContent = text;
  setTimeout(() => { if (hint.isConnected) hint.textContent = ""; }, 1500);
}

/* ---- wiring ------------------------------------------------------------- */

function wireNavigation(navigateToStage) {
  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });
}

function wireScriptingStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderScriptingStage(stage, navigateToStage, renderAgentStage);
  const change = (applyEdit, options = {}) => editStageDocument({
    documentKind: "script", apiPathSuffix: "/script", applyEdit, rerender,
    ...options,
  });

  wireNavigation(navigateToStage);
  select("#scripting-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-section]").forEach(row => {
    row.onclick = () => {
      flushPendingSave();
      scriptViewState.activeSectionId = row.dataset.section;
      rerender();
    };
  });

  document.querySelectorAll("[data-editor-tab]").forEach(tab => {
    tab.onclick = () => {
      flushPendingSave();
      scriptViewState.editorTab = tab.dataset.editorTab;
      rerender();
    };
  });

  wireEditor(change);
  wireScenarios(change);
  wireVariables(change);
}

function wireEditor(change) {
  const editor = select("#script-body");
  if (!editor) return;

  const gutter = select("#line-gutter");

  const scheduleSave = () => {
    clearTimeout(scriptViewState.pendingSaveTimer);
    scriptViewState.pendingSaveTimer = setTimeout(() => {
      const currentText = editor.value;
      const sectionId = scriptViewState.activeSectionId;
      // silent: re-rendering mid-typing would move the caret to the end.
      change(script => {
        const existing = script.section_scripts.find(s => s.section_id === sectionId);
        if (existing) existing.body = currentText;
        else script.section_scripts.push({ section_id: sectionId, body: currentText });
      }, { silent: true, onSaved: saved => { showSaveHint("saved"); return saved; } });
    }, SCRIPT_AUTOSAVE_DELAY_MS);
  };

  editor.addEventListener("input", () => {
    // Gutter is updated directly rather than by re-render, for the same reason.
    const lineCount = editor.value.split("\n").length;
    gutter.textContent = Array.from({ length: lineCount }, (_, i) => i + 1).join("\n");
    scheduleSave();
  });

  // Keep the gutter aligned when the textarea scrolls independently.
  editor.addEventListener("scroll", () => { gutter.scrollTop = editor.scrollTop; });

  editor.addEventListener("blur", flushPendingSave);
}

/** Commit a debounced edit immediately.
 *
 *  Called before any navigation away from the editor. Without it, switching
 *  section within the debounce window would discard the last keystrokes — the
 *  quiet data loss that is hardest to notice. */
function flushPendingSave() {
  if (!scriptViewState.pendingSaveTimer) return;
  clearTimeout(scriptViewState.pendingSaveTimer);
  scriptViewState.pendingSaveTimer = null;

  const editor = select("#script-body");
  if (!editor) return;

  const currentText = editor.value;
  const sectionId = scriptViewState.activeSectionId;
  const script = applicationState.script;
  const existing = script.section_scripts.find(s => s.section_id === sectionId);
  if (existing) existing.body = currentText;
  else script.section_scripts.push({ section_id: sectionId, body: currentText });

  requestJsonFromApi(projectApiPath("/script"), {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(script),
  }).catch(saveFailure => {
    console.error("flush save failed", saveFailure);
    showStageNotice("bad", `Could not save the last edit — ${saveFailure.message}`);
  });
}

function wireScenarios(change) {
  document.querySelectorAll("[data-scenario]").forEach(row => {
    const activate = () => change(script => {
      script.active_scenario_id = row.dataset.scenario;
    });
    row.onclick = event => {
      if (event.target.closest("[data-delete-scenario]")) return;
      activate();
    };
    row.onkeydown = event => {
      if (event.key === "Enter" || event.key === " ") { event.preventDefault(); activate(); }
    };
  });

  document.querySelectorAll("[data-delete-scenario]").forEach(button => {
    button.onclick = event => {
      event.stopPropagation();
      change(script => {
        script.scenarios = script.scenarios
          .filter(s => s.id !== button.dataset.deleteScenario);
        // Never leave the active scenario pointing at something deleted.
        if (script.active_scenario_id === button.dataset.deleteScenario) {
          script.active_scenario_id = script.scenarios[0]?.id ?? null;
        }
      });
    };
  });

  select("#add-scenario-button").onclick = () => {
    const name = window.prompt("Scenario name");
    if (!name?.trim()) return;
    change(script => {
      script.scenarios.push({
        id: newItemIdentifier(),
        name: name.trim(), description: "",
      });
    });
  };
}

function wireVariables(change) {
  select("#add-variable-button").onclick = () => {
    const name = window.prompt("Variable name (e.g. TOPIC)");
    if (!name?.trim()) return;
    const value = window.prompt(`Value for {{${name.trim().toUpperCase()}}}`) ?? "";
    change(script => {
      script.variables.push({
        id: newItemIdentifier(),
        name: name.trim(), value,
      });
    });
  };

  document.querySelectorAll("[data-edit-variable]").forEach(valueNode => {
    valueNode.onclick = () => {
      const variable = applicationState.script.variables
        .find(v => v.id === valueNode.dataset.editVariable);
      const next = window.prompt(`Value for {{${variable.name}}}`, variable.value);
      if (next === null) return;
      change(script => {
        const target = script.variables.find(v => v.id === valueNode.dataset.editVariable);
        if (target) target.value = next;
      });
    };
  });

  document.querySelectorAll("[data-delete-variable]").forEach(button => {
    button.onclick = () => change(script => {
      script.variables = script.variables
        .filter(v => v.id !== button.dataset.deleteVariable);
    });
  });
}
