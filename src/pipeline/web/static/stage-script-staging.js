/**
 * Scripting stage — each plan section's narration, written as scenes.
 *
 * A scene is what is said and what is on screen while it is said. The section
 * list is the *plan's*: narration is keyed by `PlanSection.id`, so renaming or
 * reordering in Planning carries it along, and narration a plan no longer has is
 * shown -- to reattach or delete -- instead of only counted in a warning.
 *
 * Beside the editor sits everything the section was planned with: its summary,
 * target length, how it will be shown, its objectives and its source text, plus
 * any review comments sent back to Scripting for it. Narration written against a
 * plan section or source that has since changed is flagged there.
 */

import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, icon, projectApiPath, refreshProjectSummary, select,
  showStageNotice, stageIcon,
} from "/static/ui-kit.js";

/** View-only state. None of it belongs in the saved script. */
const scriptViewState = {
  activeSectionId: null,
  editorTab: "script",
  pendingSaveTimer: null,
  savePromise: null,
  saveAgain: false,
  typedWhileSaving: false,
  draftingSectionId: null,
  isDraftingAll: false,
  draftInstruction: "",
  sourceShownFor: null,
  sourceCache: {},
};

/** Typing saves on a debounce rather than per keystroke: a POST per character
 *  would be wasteful and would make every save a potential conflict with the
 *  next one. */
const SCRIPT_AUTOSAVE_DELAY_MS = 700;
const WORDS_PER_SECOND = 150 / 60;

const APPROACH_LABELS = {
  composition: "Composition", plot: "Plot", simulation: "Simulation",
  code: "Code", still: "Still",
};

const isDrafting = () =>
  scriptViewState.isDraftingAll || scriptViewState.draftingSectionId !== null;

const countWords = text => (text.trim() ? text.trim().split(/\s+/).length : 0);
const secondsFor = words => Math.round(words / WORDS_PER_SECOND);
const formatClock = milliseconds => {
  const seconds = Math.round(milliseconds / 1000);
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
};
const referenceLabel = reference =>
  [reference.file_name, ...reference.heading_path].join(" › ");

export async function renderScriptStagingStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  if (!body.querySelector(".script-grid")) {
    body.innerHTML = `<div class="card muted">Loading script…</div>`;
  }

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
        ${scriptingHeader()}
        <div class="empty">
          <h3>No sections to write for</h3>
          <p>Narration is written per planned section. Build the scene plan first.</p>
          <button class="btn btn-accent" data-goto="scene-plan">
            ${icon(ICON.arrowLeft)} Go to the Scene Plan</button>
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

  // Stranded and out-of-date narration have their own places on the page; the
  // notice keeps the rest.
  const shownElsewhere = /belong to sections no longer in the plan|were written against an earlier/;
  const warnings = script.warnings.filter(warning => !shownElsewhere.test(warning));

  body.innerHTML = `
    <div class="card">
      ${scriptingHeader()}
      ${renderDraftBar(script, sections)}

      ${warnings.length ? `
        <div class="notice warn" style="margin-bottom:14px">
          ${warnings.map(escapeHtml).join(" · ")}
        </div>` : ""}

      ${renderStrandedNarration(script, sections)}

      <div class="script-grid">
        ${renderSectionList(script, sections)}
        ${renderEditor(script, sections)}
        <div>
          ${renderSectionContext(script, sections)}
          ${renderScenarioPanel(script)}
          ${renderVariablePanel(script)}
        </div>
      </div>

      ${renderFooterNav(stage, script)}
    </div>`;

  wireScriptingStage(stage, navigateToStage, renderAgentStage);
}

function scriptingHeader() {
  return `
    <div class="card-head">
      <span class="card-icon">${stageIcon("script-staging", 21)}</span>
      <div>
        <h2>Script &amp; Staging</h2>
        <p>Write each section as scenes: what is said, and what is on screen.</p>
      </div>
      <button class="btn" id="scripting-agent-button">
        ${icon(ICON.gear, 14, 1.8)} Agent &amp; instructions
      </button>
    </div>`;
}

/* ---- drafting ------------------------------------------------------------ */

function renderDraftBar(script, sections) {
  const unwritten = sections.filter(s => !(script.per_section[s.id]?.word_count > 0));
  const plannedSeconds = sections.reduce((sum, s) => sum + s.estimated_seconds, 0);
  const bar = (tone, iconPaths, title, detail, actions = "") => `
    <div class="run-bar plan-bar ${tone}">
      <span class="run-icon">${icon(iconPaths, 17, 2.2)}</span>
      <span class="run-text"><b>${title}</b><span>${detail}</span></span>
      ${actions ? `<span class="plan-actions">${actions}</span>` : ""}
    </div>`;

  if (scriptViewState.isDraftingAll) {
    return bar("working", ICON.doc, `Drafting ${unwritten.length} section(s) at once…`,
      "Each is written from its own source text, as scenes with on-screen briefs. "
      + "This can take a minute or two; editing is paused until they are saved.");
  }
  if (unwritten.length) {
    return bar("ready", ICON.doc,
      `${unwritten.length} of ${sections.length} section(s) have no narration`,
      `About ${Math.round(plannedSeconds / 60)} min planned. Drafting never replaces narration
       that is already written.`,
      `<input id="draft-instruction" class="draft-instruction" maxlength="300"
              placeholder="Guidance for every section (optional)"
              value="${escapeHtml(scriptViewState.draftInstruction)}"
              aria-label="Guidance for the drafts">
       <button class="btn btn-accent" id="draft-unwritten-button"
               ${isDrafting() ? "disabled" : ""}>Draft all unwritten</button>`);
  }
  return bar("ready", ICON.check, `All ${sections.length} sections have narration`,
    `~${Math.round(script.total_estimated_seconds / 60)} min spoken, `
    + `~${Math.round(plannedSeconds / 60)} min planned.`);
}

/* ---- narration no section points at --------------------------------------- */

function renderStrandedNarration(script, sections) {
  if (!script.orphaned?.length) return "";
  const writtenIds = new Set(sections
    .filter(s => script.per_section[s.id]?.word_count > 0).map(s => s.id));

  return `
    <div class="panel stranded-panel">
      <div class="panel-head">
        <h3>Narration not attached to any section (${script.orphaned.length})</h3>
      </div>
      <p class="panel-sub">Written for sections the plan no longer has. Attach it to a
        section to use it, or delete it.</p>
      ${script.orphaned.map(entry => `
        <div class="stranded-row">
          <div class="stranded-text">
            <b>${entry.word_count} words · ${entry.scene_count} scene(s)</b>
            <span>${escapeHtml(entry.preview)}${entry.preview.length >= 160 ? "…" : ""}</span>
          </div>
          <select data-attach-orphan="${escapeHtml(entry.section_id)}"
                  aria-label="Attach this narration to a section">
            <option value="">Attach to…</option>
            ${sections.map((section, index) => `
              <option value="${section.id}">${index + 1}. ${escapeHtml(section.title)}${
                writtenIds.has(section.id) ? " (replaces its narration)" : ""}</option>`).join("")}
          </select>
          <button class="btn-icon danger" data-delete-orphan="${escapeHtml(entry.section_id)}"
                  title="Delete this narration" aria-label="Delete this narration">
            ${icon(`<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>`, 15, 1.8)}
          </button>
        </div>`).join("")}
    </div>`;
}

/* ---- section list ---------------------------------------------------------- */

function renderSectionList(script, sections) {
  const writtenCount = sections.filter(s => script.per_section[s.id]?.word_count > 0).length;
  const stale = new Set((script.out_of_date ?? []).map(entry => entry.section_id));

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
        const comments = (script.comments_by_section?.[section.id] ?? []).length;
        const measured = script.measured_seconds?.[section.id];
        const over = isWritten && stats.estimated_seconds > section.estimated_seconds * 1.25;
        return `
          <button class="section-row ${scriptViewState.activeSectionId === section.id ? "active" : ""}"
                  data-section="${section.id}">
            <span class="outline-num">${index + 1}</span>
            <span class="body">
              <span class="title ${section.title ? "" : "untitled"}"
                    title="${escapeHtml(section.title)}"
                >${escapeHtml(section.title || "Untitled section")}</span>
              <span class="sub ${over ? "over" : ""}">${isWritten
                ? `~${stats.estimated_seconds}s of ${section.estimated_seconds}s`
                : `not written · ${section.estimated_seconds}s planned`}</span>
              ${stale.has(section.id) || comments || measured ? `
                <span class="section-flags">
                  ${stale.has(section.id) ? `<span class="fact warn">out of date</span>` : ""}
                  ${comments ? `<span class="fact bad">${comments} comment${comments === 1 ? "" : "s"}</span>` : ""}
                  ${measured ? `<span class="fact" title="Measured in the last render">${measured}s spoken</span>` : ""}
                </span>` : ""}
            </span>
            <span class="written-dot ${isWritten ? "written" : ""}"
                  title="${isWritten ? "Has narration" : "No narration yet"}"></span>
          </button>`;
      }).join("")}
    </div>`;
}

/* ---- the editor ------------------------------------------------------------- */

function activeSectionScript(script) {
  return script.section_scripts.find(s => s.section_id === scriptViewState.activeSectionId);
}

function renderEditor(script, sections) {
  const section = sections.find(s => s.id === scriptViewState.activeSectionId);
  const written = activeSectionScript(script);
  const scenes = written?.scenes ?? [];
  const isScriptTab = scriptViewState.editorTab === "script";
  const isDraftingThis = scriptViewState.draftingSectionId === section.id;
  const words = countWords(scenes.map(scene => scene.narration).join(" "));

  return `
    <div class="panel editor-shell">
      <div class="editor-bar">
        <div class="seg">
          <button class="${isScriptTab ? "on" : ""}" data-editor-tab="script">Scenes</button>
          <button class="${isScriptTab ? "" : "on"}" data-editor-tab="preview">Preview</button>
        </div>
        <div class="spacer"></div>
        <button class="btn ${words ? "" : "btn-accent"}" id="draft-section-button"
                ${isDrafting() ? "disabled" : ""}>
          ${isDraftingThis ? "Drafting…" : words ? "Redraft this section" : "Draft this section"}
        </button>
      </div>

      ${isDraftingThis ? `
        <div class="notice ok" style="margin-bottom:10px">
          Writing “${escapeHtml(section.title)}” from its source text… Editing is paused
          until it is saved.
        </div>` : ""}

      ${isScriptTab ? renderScenes(scenes) : renderPreview(script, scenes)}

      <div class="editor-foot">
        <span id="section-word-count">Words ${words}</span>
        <span id="section-length" class="${secondsFor(words) > section.estimated_seconds * 1.25 ? "over" : ""}"
          >~${secondsFor(words)}s of ${section.estimated_seconds}s planned</span>
        <span>${scenes.length} scene${scenes.length === 1 ? "" : "s"}</span>
        <div class="spacer"></div>
        <span id="script-save-hint"></span>
      </div>
    </div>`;
}

function renderScenes(scenes) {
  // While a draft is written on the server, the page's copy of the script is
  // out of date: a save from it would put the old narration back over the draft.
  const locked = isDrafting() ? "disabled" : "";
  if (!scenes.length) {
    return `
      <div class="scenes-empty">
        <p>No narration yet. Draft this section from its source text, or add a scene and
           write it yourself.</p>
        <button class="add-row" data-add-scene ${locked}>${icon(ICON.plus)} Add a scene</button>
      </div>`;
  }

  return `
    <div class="scene-list">
      ${scenes.map((scene, index) => `
        <div class="scene-card" data-scene-card="${index}">
          <div class="scene-head">
            <span class="outline-num">${index + 1}</span>
            <b>Scene ${index + 1}</b>
            <span class="mono muted scene-length" data-scene-length="${index}"
              >~${secondsFor(countWords(scene.narration))}s</span>
            <div class="spacer"></div>
            <button class="btn-icon" data-move-scene="${index}" data-direction="-1"
                    ${index === 0 ? "disabled" : locked} title="Move up" aria-label="Move scene up">
              ${icon(`<path d="M18 15l-6-6-6 6"/>`, 14, 2.2)}</button>
            <button class="btn-icon" data-move-scene="${index}" data-direction="1"
                    ${index === scenes.length - 1 ? "disabled" : locked} title="Move down"
                    aria-label="Move scene down">
              ${icon(`<path d="M6 9l6 6 6-6"/>`, 14, 2.2)}</button>
            <button class="btn-icon danger" data-delete-scene="${index}" ${locked}
                    title="Delete scene" aria-label="Delete scene">
              ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 14, 2)}</button>
          </div>
          <label class="scene-label" for="scene-narration-${index}">Said</label>
          <textarea id="scene-narration-${index}" class="scene-narration" spellcheck="true"
                    data-scene-field="narration" data-scene-index="${index}" ${locked ? "readonly" : ""}
                    placeholder="What is said aloud. Use {{VARIABLE}} for values that change."
                    >${escapeHtml(scene.narration)}</textarea>
          <label class="scene-label" for="scene-brief-${index}">On screen</label>
          <textarea id="scene-brief-${index}" class="scene-brief" spellcheck="true"
                    data-scene-field="brief" data-scene-index="${index}" ${locked ? "readonly" : ""}
                    placeholder="Exactly what is shown: the real values and labels from the source."
                    >${escapeHtml(scene.brief)}</textarea>
        </div>`).join("")}
      <button class="add-row" data-add-scene ${locked}>${icon(ICON.plus)} Add a scene</button>
    </div>`;
}

/** What is spoken, variables filled in exactly as the render fills them, with
 *  unknown ones left visible and highlighted. */
function renderPreview(script, scenes) {
  if (!scenes.some(scene => scene.narration.trim())) {
    return `<div class="script-preview"><span class="muted">Nothing written for this section yet.</span></div>`;
  }
  const values = Object.fromEntries(
    script.variables.filter(v => v.name).map(v => [v.name.toUpperCase(), v.value]));
  const fill = text => escapeHtml(text).replace(/\{\{\s*([A-Za-z0-9_]+)\s*\}\}/g, (whole, name) => {
    const value = values[name.toUpperCase()];
    return value !== undefined
      ? escapeHtml(value)
      : `<span class="var-unresolved" title="Not defined: spoken as written">${escapeHtml(whole)}</span>`;
  });

  return `
    <div class="script-preview scene-preview">
      ${scenes.map((scene, index) => `
        <div class="preview-scene">
          <span class="scene-label">Scene ${index + 1}</span>
          <p>${fill(scene.narration)}</p>
          ${scene.brief ? `<div class="preview-brief"><b>On screen:</b> ${escapeHtml(scene.brief)}</div>` : ""}
        </div>`).join("")}
    </div>`;
}

/* ---- what the section was planned with -------------------------------------- */

function renderSectionContext(script, sections) {
  const section = sections.find(s => s.id === scriptViewState.activeSectionId);
  const objectives = Object.fromEntries((script.plan_objectives ?? []).map(o => [o.id, o.text]));
  const served = (section.objective_ids ?? []).map(id => objectives[id]).filter(Boolean);
  const stale = (script.out_of_date ?? []).find(entry => entry.section_id === section.id);
  const comments = script.comments_by_section?.[section.id] ?? [];
  const source = scriptViewState.sourceShownFor === section.id
    ? scriptViewState.sourceCache[section.id] : null;

  return `
    <div class="panel section-context" style="margin-bottom:14px">
      <div class="panel-head"><h3>This section</h3></div>

      ${stale ? `
        <div class="notice warn context-notice">
          <b>Out of date:</b> ${escapeHtml(stale.reasons.join(" and "))} since this was written.
          <button class="btn" id="confirm-narration-button">Keep narration as is</button>
        </div>` : ""}

      ${comments.length ? `
        <div class="context-comments">
          <b>Review comments for Scripting</b>
          ${comments.map(comment => `
            <div class="context-comment">
              <span class="mono">${formatClock(comment.at_ms)}</span>
              <span><b>${escapeHtml(comment.author)}:</b> ${escapeHtml(comment.body)}</span>
            </div>`).join("")}
        </div>` : ""}

      <p class="context-summary">${escapeHtml(section.summary || "No summary in the plan.")}</p>
      <dl class="context-facts">
        <dt>Target</dt><dd>~${section.estimated_seconds}s
          (about ${Math.round(section.estimated_seconds * WORDS_PER_SECOND)} words)</dd>
        ${section.rendering_approach ? `
          <dt>Shown as</dt><dd><span class="fact approach ${escapeHtml(section.rendering_approach)}"
            >${escapeHtml(APPROACH_LABELS[section.rendering_approach] ?? section.rendering_approach)}</span>
            ${escapeHtml(section.rendering_reason ?? "")}</dd>` : ""}
        ${served.length ? `
          <dt>Objectives</dt><dd><ul>${served.map(o => `<li>${escapeHtml(o)}</li>`).join("")}</ul></dd>` : ""}
        ${script.selected_audience ? `
          <dt>Audience</dt><dd>${escapeHtml(script.selected_audience)}</dd>` : ""}
      </dl>

      <div class="context-sources">
        <b>Source content</b>
        ${(section.sources ?? []).length
          ? `<div class="source-chips">${section.sources.map(r =>
              `<span class="source-chip">${escapeHtml(referenceLabel(r))}</span>`).join("")}</div>
             <button class="btn" id="toggle-source-button">
               ${source ? "Hide source text" : "Show source text"}</button>`
          : `<p class="muted edit-hint">The plan records no source for this section. Drafting
               reads the whole extraction instead.</p>`}
        ${source ? `
          <div class="source-text">
            ${source.parts.map(part => `
              <div class="source-part">
                <span class="scene-label">${escapeHtml(part.label)}</span>
                <pre>${escapeHtml(part.text)}</pre>
              </div>`).join("")}
            ${source.missing.length ? `<p class="fact bad">No longer extracted:
              ${source.missing.map(escapeHtml).join("; ")}</p>` : ""}
          </div>` : ""}
      </div>
    </div>`;
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
              title="Written as {{NAME}} in a script and filled in wherever it is spoken or shown.">i</span>
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
          Used but not defined, so spoken as written: ${[...undefinedNames].map(escapeHtml).join(", ")}
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

/** The active section's entry, created if the section has none yet. */
function ensureSectionScript(script, sectionId) {
  let entry = script.section_scripts.find(s => s.section_id === sectionId);
  if (!entry) {
    entry = { section_id: sectionId, body: "", scenes: [], written_from: {} };
    script.section_scripts.push(entry);
  }
  return entry;
}

/**
 * What a save sends: the scenes, never the `body` derived from them.
 *
 * `SectionScript.body` is rebuilt from the scenes when the script is saved, and
 * a section that arrives with a body and no scenes is migrated the other way --
 * that is how scripts written before scenes existed are read. Sending the page's
 * copy of `body` made deleting the *last* scene do nothing: the payload said no
 * scenes and still carried the old body, so the server helpfully turned that
 * body back into a scene.
 */
const scriptPayload = script => ({
  ...script,
  section_scripts: script.section_scripts.map(({ body, ...rest }) => rest),
});

/* ---- wiring ------------------------------------------------------------- */

function wireNavigation(navigateToStage) {
  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });
}

function wireScriptingStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderScriptStagingStage(stage, navigateToStage, renderAgentStage);
  const change = async applyEdit => {
    await flushPendingSave();
    if (isDrafting()) {
      showStageNotice("warn", "Editing is paused until the draft is saved.");
      return;
    }
    await editStageDocument({
      documentKind: "script", apiPathSuffix: "/script", applyEdit, rerender,
      buildPayload: scriptPayload,
    });
  };

  wireNavigation(navigateToStage);
  select("#scripting-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-section]").forEach(row => {
    row.onclick = async () => {
      await flushPendingSave();
      scriptViewState.activeSectionId = row.dataset.section;
      rerender();
    };
  });

  document.querySelectorAll("[data-editor-tab]").forEach(tab => {
    tab.onclick = async () => {
      await flushPendingSave();
      scriptViewState.editorTab = tab.dataset.editorTab;
      rerender();
    };
  });

  wireDrafting(rerender);
  wireScenes(change);
  wireSectionContext(rerender);
  wireStrandedNarration(change);
  wireScenarios(change);
  wireVariables(change);
}

async function runScriptAction({ path, body, method = "POST", done, rerender }) {
  await flushPendingSave();
  let result = null;
  try {
    result = await requestJsonFromApi(projectApiPath(path), {
      method,
      headers: { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch (actionFailure) {
    console.error("script action failed", path, actionFailure);
    showStageNotice("bad", actionFailure.message);
  }
  await refreshProjectSummary();
  await rerender();
  if (result && done) showStageNotice("ok", done);
  return result;
}

function wireDrafting(rerender) {
  const instruction = select("#draft-instruction");
  if (instruction) {
    instruction.oninput = () => { scriptViewState.draftInstruction = instruction.value; };
  }

  const draftAll = select("#draft-unwritten-button");
  if (draftAll) {
    draftAll.onclick = async () => {
      await flushPendingSave();
      scriptViewState.draftInstruction = select("#draft-instruction")?.value.trim() ?? "";
      scriptViewState.isDraftingAll = true;
      await rerender();
      let result = null;
      try {
        result = await requestJsonFromApi(projectApiPath("/script/draft-unwritten"), {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ instruction: scriptViewState.draftInstruction }),
        });
      } catch (draftFailure) {
        console.error("draft all failed", draftFailure);
        showStageNotice("bad", `Could not draft — ${draftFailure.message}`);
      } finally {
        scriptViewState.isDraftingAll = false;
        await refreshProjectSummary();
        await rerender();
      }
      if (result) {
        const drafted = result.drafted_section_ids.length;
        showStageNotice(result.notes.length ? "warn" : "ok",
          `Drafted ${drafted} section(s).${result.notes.length ? " " + result.notes.join(" ") : ""}`);
      }
    };
  }

  const draftOne = select("#draft-section-button");
  if (draftOne) {
    draftOne.onclick = async () => {
      await flushPendingSave();
      const sectionId = scriptViewState.activeSectionId;
      const written = activeSectionScript(applicationState.script);
      if (written?.scenes?.some(scene => scene.narration.trim() || scene.brief.trim())
          && !window.confirm("Redraft this section? Its current scenes will be replaced.")) {
        return;
      }
      scriptViewState.draftingSectionId = sectionId;
      await rerender();
      let result = null;
      try {
        result = await requestJsonFromApi(projectApiPath("/script/draft"), {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ section_id: sectionId, instruction: "" }),
        });
      } catch (draftFailure) {
        console.error("section draft failed", draftFailure);
        showStageNotice("bad", `Could not draft this section — ${draftFailure.message}`);
      } finally {
        scriptViewState.draftingSectionId = null;
        await refreshProjectSummary();
        await rerender();
      }
      if (result) {
        showStageNotice(result.notes?.length ? "warn" : "ok",
          `Drafted ${result.scene_count} scene(s), ${result.written_words} words.`
          + (result.notes?.length ? " " + result.notes.join(" ") : ""));
      }
    };
  }
}

function wireScenes(change) {
  const sectionId = scriptViewState.activeSectionId;

  document.querySelectorAll("[data-scene-field]").forEach(field => {
    field.addEventListener("input", () => {
      // Memory is updated at once and the save debounced. Re-rendering while
      // typing would move the caret, so the counts are updated in place.
      const entry = ensureSectionScript(applicationState.script, sectionId);
      const scene = entry.scenes[Number(field.dataset.sceneIndex)];
      if (!scene) return;
      scene[field.dataset.sceneField] = field.value;
      if (scriptViewState.savePromise) scriptViewState.typedWhileSaving = true;
      refreshCounts(entry);
      scheduleSave();
    });
    field.addEventListener("blur", () => { flushPendingSave(); });
  });

  document.querySelectorAll("[data-add-scene]").forEach(button => {
    button.onclick = () => {
      change(script => {
        ensureSectionScript(script, sectionId).scenes.push({
          id: newItemIdentifier(), narration: "", brief: "",
        });
      });
    };
  });

  document.querySelectorAll("[data-move-scene]").forEach(button => {
    button.onclick = () => {
      const from = Number(button.dataset.moveScene);
      const to = from + Number(button.dataset.direction);
      change(script => {
        const scenes = ensureSectionScript(script, sectionId).scenes;
        if (to < 0 || to >= scenes.length) return;
        [scenes[from], scenes[to]] = [scenes[to], scenes[from]];
      });
    };
  });

  document.querySelectorAll("[data-delete-scene]").forEach(button => {
    button.onclick = () => {
      const index = Number(button.dataset.deleteScene);
      const scene = ensureSectionScript(applicationState.script, sectionId).scenes[index];
      if ((scene?.narration.trim() || scene?.brief.trim())
          && !window.confirm("Delete this scene and its text?")) {
        return;
      }
      change(script => {
        ensureSectionScript(script, sectionId).scenes.splice(index, 1);
      });
    };
  });
}

function refreshCounts(entry) {
  const words = countWords(entry.scenes.map(scene => scene.narration).join(" "));
  const counter = select("#section-word-count");
  if (counter) counter.textContent = `Words ${words}`;
  const section = applicationState.script.plan_sections
    .find(s => s.id === scriptViewState.activeSectionId);
  const length = select("#section-length");
  if (length && section) {
    length.textContent = `~${secondsFor(words)}s of ${section.estimated_seconds}s planned`;
    length.classList.toggle("over", secondsFor(words) > section.estimated_seconds * 1.25);
  }
  entry.scenes.forEach((scene, index) => {
    const label = document.querySelector(`[data-scene-length="${index}"]`);
    if (label) label.textContent = `~${secondsFor(countWords(scene.narration))}s`;
  });
}

/** Save what has been typed, without redrawing.
 *
 *  A redraw would move the caret, so this passes no redraw at all. If more is
 *  typed while the save is on its way, the page's copy is kept rather than
 *  replaced by the server's reply, and saved again. */
function saveTyping() {
  if (scriptViewState.savePromise) {
    scriptViewState.saveAgain = true;
    return scriptViewState.savePromise;
  }
  scriptViewState.savePromise = (async () => {
    try {
      do {
        scriptViewState.saveAgain = false;
        scriptViewState.typedWhileSaving = false;
        await editStageDocument({
          documentKind: "script", apiPathSuffix: "/script", silent: true,
          applyEdit: () => {}, rerender: async () => {}, buildPayload: scriptPayload,
          onSaved: saved => {
            if (scriptViewState.typedWhileSaving) return applicationState.script;
            showSaveHint("saved");
            return saved;
          },
        });
      } while (scriptViewState.saveAgain);
    } finally {
      scriptViewState.savePromise = null;
    }
  })();
  return scriptViewState.savePromise;
}

function scheduleSave() {
  clearTimeout(scriptViewState.pendingSaveTimer);
  scriptViewState.pendingSaveTimer = setTimeout(() => {
    scriptViewState.pendingSaveTimer = null;
    saveTyping();
  }, SCRIPT_AUTOSAVE_DELAY_MS);
}

/** Save typing still waiting on its debounce, and wait until it is saved.
 *
 *  Awaited before anything that redraws or changes the script another way. A
 *  redraw loads the script from the server, so without this, switching section
 *  within the debounce window would discard the last keystrokes -- the quiet
 *  data loss that is hardest to notice. */
async function flushPendingSave() {
  if (scriptViewState.pendingSaveTimer) {
    clearTimeout(scriptViewState.pendingSaveTimer);
    scriptViewState.pendingSaveTimer = null;
    saveTyping();
  }
  if (scriptViewState.savePromise) await scriptViewState.savePromise;
}

function wireSectionContext(rerender) {
  const sectionId = scriptViewState.activeSectionId;

  const toggle = select("#toggle-source-button");
  if (toggle) {
    toggle.onclick = async () => {
      if (scriptViewState.sourceShownFor === sectionId) {
        scriptViewState.sourceShownFor = null;
        await rerender();
        return;
      }
      if (!scriptViewState.sourceCache[sectionId]) {
        try {
          scriptViewState.sourceCache[sectionId] = await requestJsonFromApi(
            projectApiPath(`/script/sections/${encodeURIComponent(sectionId)}/source`));
        } catch (sourceFailure) {
          showStageNotice("bad", `Could not load the source — ${sourceFailure.message}`);
          return;
        }
      }
      scriptViewState.sourceShownFor = sectionId;
      await rerender();
    };
  }

  const keep = select("#confirm-narration-button");
  if (keep) {
    keep.onclick = () => runScriptAction({
      path: `/script/sections/${encodeURIComponent(sectionId)}/confirm`, rerender,
      done: "Recorded: this narration still matches its section and source.",
    });
  }
}

function wireStrandedNarration(change) {
  document.querySelectorAll("[data-attach-orphan]").forEach(picker => {
    picker.onchange = () => {
      const targetId = picker.value;
      if (!targetId) return;
      const script = applicationState.script;
      const targetHasNarration = script.section_scripts
        .some(s => s.section_id === targetId && s.body?.trim());
      if (targetHasNarration
          && !window.confirm("That section already has narration. Replace it with this?")) {
        picker.value = "";
        return;
      }
      scriptViewState.activeSectionId = targetId;
      change(edited => {
        edited.section_scripts = edited.section_scripts.filter(s => s.section_id !== targetId);
        const orphan = edited.section_scripts
          .find(s => s.section_id === picker.dataset.attachOrphan);
        if (orphan) orphan.section_id = targetId;
      });
    };
  });

  document.querySelectorAll("[data-delete-orphan]").forEach(button => {
    button.onclick = () => {
      if (!window.confirm("Delete this narration? It is not attached to any section.")) return;
      change(script => {
        script.section_scripts = script.section_scripts
          .filter(s => s.section_id !== button.dataset.deleteOrphan);
      });
    };
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
