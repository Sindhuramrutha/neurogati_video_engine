/**
 * Script & Staging — three tabs, in the order the work happens.
 *
 * 1. Setup: what the Scene Plan handed on, the variables used
 *    across the script, and narration left over from sections the plan dropped.
 * 2. Write: each section's narration as scenes, beside what it was planned
 *    with. The Scripting agent (AI) only writes empty sections, or one you ask
 *    it to redraft.
 * 3. Check & transfer: the fixed rules over the script, each pass / warn / fail with
 *    why, and the transfer they guard -- later stages read the transferred script
 *    (`script_handoff.py`); a failing check blocks it. One tab: two read as one step.
 *
 * Every pane is drawn and only the chosen one shown, so a tab change never
 * redraws the page or loses typing.
 *
 * A scene is what is said and what is on screen while it is said. The section
 * list is the *plan's*: narration is keyed by `PlanSection.id`, so renaming or
 * reordering in the Scene Plan carries it along, and narration a plan no longer has is
 * shown -- to reattach or delete -- instead of only counted in a warning.
 *
 * Beside the editor sits everything the section was planned with: its summary,
 * target length, how it will be shown, its planned scenes and its source text, plus
 * any review comments sent back to Scripting for it. Narration written against a
 * plan section or source that has since changed is flagged there.
 */

import { loadFacts, renderFactsPanel, wireFactsPanel } from "/static/facts-panel.js";
import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, footerNav, icon, moveToNextLayerButton, projectApiPath,
  refreshProjectSummary, select, showStageNotice, stageHeader, stageNeighbours, whenItWas,
  wireGotoButtons,
} from "/static/ui-kit.js";

const SCRIPT_TABS = [
  ["setup", "Setup"], ["write", "Write"], ["final", "Check & transfer"],
];

const currentScriptTab = () =>
  // The Check tab became part of Check & transfer.
  SCRIPT_TABS.some(([key]) => key === applicationState.scriptTab)
    ? applicationState.scriptTab : applicationState.scriptTab === "check" ? "final" : "setup";

const CHECK_LABELS = { pass: "Pass", warn: "Warning", fail: "Fails", "n/a": "Not applicable" };

/** View-only state. None of it belongs in the saved script. */
const scriptViewState = {
  activeSectionId: null,
  pendingSaveTimer: null,
  savePromise: null,
  saveAgain: false,
  typedWhileSaving: false,
  draftingSectionId: null,
  isDraftingAll: false,
  draftInstruction: "",
};

/** Typing saves on a debounce rather than per keystroke: a POST per character
 *  would be wasteful and would make every save a potential conflict with the
 *  next one. */
const SCRIPT_AUTOSAVE_DELAY_MS = 700;
const WORDS_PER_SECOND = 150 / 60;

const isDrafting = () =>
  scriptViewState.isDraftingAll || scriptViewState.draftingSectionId !== null;

const countWords = text => (text.trim() ? text.trim().split(/\s+/).length : 0);
const secondsFor = words => Math.round(words / WORDS_PER_SECOND);
const formatClock = milliseconds => {
  const seconds = Math.round(milliseconds / 1000);
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
};
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
      ${scriptingHeader()}
      <div class="card stage-content">
        <div class="empty">
          <h3>No sections to write for</h3>
          <p>Narration is written per planned section. Build the scene plan first.</p>
          <button class="btn btn-accent" data-goto="scene-plan">
            ${icon(ICON.arrowLeft)} Go to the Scene Plan</button>
        </div>
      </div>`;
    wireGotoButtons(navigateToStage);
    select("#scripting-agent-button").onclick = () => renderAgentStage(stage);
    return;
  }

  // Keep the selection valid across a plan edit that removed the open section.
  if (!sections.some(section => section.id === scriptViewState.activeSectionId)) {
    scriptViewState.activeSectionId = sections[0].id;
  }

  let handoff = { checks: [], failing: 0, warning: 0, has_transferred: false, pending: false };
  try {
    handoff = await requestJsonFromApi(projectApiPath("/script/handoff"));
  } catch (handoffFailure) {
    console.error("script hand-off load failed", handoffFailure);
  }
  const facts = await loadFacts();
  const tab = currentScriptTab();
  const pane = (key, content) =>
    `<section class="plan-pane" data-script-pane="${key}" ${key === tab ? "" : "hidden"}>${content}</section>`;

  body.innerHTML = `
    ${scriptingHeader()}
    <div class="stage-content stage-content-bare">
      ${renderFactsPanel(facts)}
      <div class="extraction-tabs plan-tabs script-tabs">
        <nav class="x-tabs" role="tablist" aria-label="Script & Staging steps">
          ${SCRIPT_TABS.map(([key, label], index) => `
            <button role="tab" class="x-tab ${key === tab ? "on" : ""}" data-script-tab="${key}"
                    aria-selected="${key === tab}">
              <span class="x-tab-number">${index + 1}</span>
              <b class="x-tab-label">${label}</b>
              ${key === "final" && handoff.failing ? `<span class="plan-tab-count fail">${handoff.failing}</span>`
                : key === "final" && handoff.warning ? `<span class="plan-tab-count warn">${handoff.warning}</span>` : ""}
              ${key === "setup" && script.orphaned?.length ? `<span class="plan-tab-count warn"
                  title="Narration left over from earlier plans">${script.orphaned.length}</span>` : ""}
            </button>`).join("")}
        </nav>
        <div class="x-tab-body" role="tabpanel">
          ${pane("setup", renderSetup(script, sections))}
          ${pane("write", `
            ${renderDraftBar(script, sections)}
            <div class="script-grid">
              ${renderSectionList(script, sections)}
              ${renderEditor(script, sections)}
            </div>`)}
          ${pane("final", renderScriptFinal(script, sections, handoff, stage)
            + renderScriptChecks(handoff))}
        </div>
      </div>
      ${renderFooterNav(stage, script, handoff, tab)}
    </div>`;

  lastScriptHandoff = handoff;
  wireScriptingStage(stage, navigateToStage, renderAgentStage);
}

/* ---- 1. Setup ---------------------------------------------------------------- */

function renderSetup(script, sections) {
  const planned = sections.reduce((sum, s) => sum + s.estimated_seconds, 0);
  return `
    <div class="plan-brief">
      <section class="panel">
        <div class="panel-head"><h3>Handed on by the Scene Plan</h3></div>
        <p class="panel-sub">${sections.length} section(s), about ${Math.round(planned / 60)} min
          planned${script.audience ? `, for ${escapeHtml(script.audience)}` : ""}.
          Narration is written for these sections and their planned scenes, and only these.</p>
        <ol class="plan-final-list">
          ${sections.map(section => `<li><b>${escapeHtml(section.title || "Untitled section")}</b>
            <span>${section.estimated_seconds} s · ${(section.scenes ?? []).length} scene(s)</span>
            </li>`).join("")}
        </ol>
      </section>
      <div>
        ${renderVariablePanel(script)}
      </div>
    </div>
    ${renderStrandedNarration(script, sections)}`;
}

/* ---- 3. Check ---------------------------------------------------------------- */

function renderScriptChecks(handoff) {
  return `
    <section class="panel">
      <div class="panel-head"><h3>The checks the script goes through</h3></div>
      <p class="panel-sub">Fixed rules over the script, its plan, the extraction and the
        review — no AI, the same script always gets the same result. A failing check
        blocks the transfer; a warning is shown and allowed.</p>
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

/* ---- 4. Final & transfer ----------------------------------------------------- */

function renderScriptFinal(script, sections, handoff, stage) {
  const written = sections.filter(s => script.per_section[s.id]?.word_count > 0);
  const [tone, title, detail] = !written.length
    ? ["blocked", "Nothing to transfer yet", "Write the narration on the Write tab."]
    : handoff.failing
      ? ["stale", `${handoff.failing} check(s) fail`, "Fix them (see the checks below), then transfer."]
      : !handoff.has_transferred
        ? ["pending", "Ready to transfer",
           "Nothing has been transferred yet, so later stages read your working script."]
        : handoff.pending
          ? ["pending", "Ready to transfer",
             "This differs from what the next layer has. Transfer to hand it the changes."]
          : ["ready", "Transferred to the next layer",
             `The next layer has had exactly this since ${whenItWas(handoff.transferred_at)}.`];
  const canTransfer = written.length && !handoff.failing
    && (handoff.pending || !handoff.has_transferred);

  return `
    <div class="final-head ${tone}">
      <span class="run-icon">${icon(tone === "ready" ? ICON.check : ICON.alert, 18, 2.3)}</span>
      <span class="run-text">
        <b>${escapeHtml(title)}</b>
        <span>${escapeHtml(detail)}</span>
        <span class="final-totals">${written.length} of ${sections.length} section(s) written ·
          ${script.total_word_count} words · ~${Math.round(script.total_estimated_seconds / 60)} min ·
          ${handoff.warning} warning(s)</span>
      </span>
      ${tone === "ready" ? moveToNextLayerButton(stageNeighbours(stage).next, {
          carries: "The transferred narration and its scenes go on." })
        : `<button class="btn btn-accent btn-transfer" id="transfer-script-button"
                   ${canTransfer ? "" : "disabled"}>
             Transfer to the next layer ${icon(ICON.arrowRight)}</button>`}
    </div>
    <section class="panel">
      <div class="panel-head"><h3>The narration, section by section</h3></div>
      <ol class="plan-final-list">
        ${sections.map(section => {
          const stats = script.per_section[section.id];
          return `<li><b>${escapeHtml(section.title || "Untitled section")}</b>
            <span>${stats?.word_count
              ? `${stats.word_count} words · ~${stats.estimated_seconds} s of ${section.estimated_seconds} s · ${stats.scene_count} scene(s)`
              : "not written"}</span></li>`;
        }).join("")}
      </ol>
    </section>`;
}

function scriptingHeader() {
  return stageHeader("script-staging", "Script & Staging",
                     { agentButtonId: "scripting-agent-button" });
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
       <span class="fact warn" title="Written by the Scripting agent: a model">AI</span>
       <button class="btn btn-accent" id="draft-unwritten-button"
               title="The Scripting agent writes every empty section; written ones are never touched"
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
        <h3>Narration from earlier plans (${script.orphaned.length})</h3>
        <div class="spacer"></div>
        <button class="btn danger" id="delete-unattached-button"
                title="Delete every piece of narration that belongs to no section">
          Delete all ${script.orphaned.length}</button>
      </div>
      <p class="panel-sub">Written for sections the plan no longer has. It is not in the video.
        Attach a piece to a section to use it, or delete it.</p>
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

/**
 * The plan owns the scenes: a section's script scenes are its planned scenes, in
 * order, by id. Narration written before the plan had scenes is matched to them
 * in order; anything beyond them is shown as not in the plan.
 */
function alignToPlan(script, section) {
  const planned = section?.scenes ?? [];
  if (!planned.length) return;
  const entry = ensureSectionScript(script, section.id);
  const ids = new Set(planned.map(p => p.id));
  if (!entry.scenes.some(scene => ids.has(scene.id))) {
    entry.scenes.forEach((scene, index) => { if (planned[index]) scene.id = planned[index].id; });
  }
  const byId = new Map(entry.scenes.map(scene => [scene.id, scene]));
  entry.scenes = [
    ...planned.map(p => byId.get(p.id) ?? { id: p.id, narration: "", brief: "" }),
    ...entry.scenes.filter(scene => !ids.has(scene.id)),
  ];
}

function renderEditor(script, sections) {
  const section = sections.find(s => s.id === scriptViewState.activeSectionId);
  alignToPlan(script, section);
  const written = activeSectionScript(script);
  const scenes = written?.scenes ?? [];
  const isScriptTab = applicationState.scriptEditorTab === "script";
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
                title="The Scripting agent (AI) writes this section from its source text"
                ${isDrafting() ? "disabled" : ""}>
          ${isDraftingThis ? "Drafting…" : words ? "Redraft this section (AI)" : "Draft this section (AI)"}
        </button>
      </div>

      ${renderSectionNotices(script, section)}

      ${isDraftingThis ? `
        <div class="notice ok" style="margin-bottom:10px">
          Writing “${escapeHtml(section.title)}” from its source text… Editing is paused
          until it is saved.
        </div>` : ""}

      ${isScriptTab ? renderScenes(scenes, section.scenes ?? []) : renderPreview(script, scenes)}

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

function renderScenes(scenes, planned = []) {
  // While a draft is written on the server, the page's copy of the script is
  // out of date: a save from it would put the old narration back over the draft.
  const locked = isDrafting() ? "disabled" : "";
  if (!scenes.length && !planned.length) {
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
              >~${secondsFor(countWords(scene.narration))}s${
                planned[index] ? ` of ${planned[index].seconds}s planned` : ""}</span>
            <div class="spacer"></div>
            ${planned.length ? (index >= planned.length ? `
              <span class="fact bad">not in the plan</span>
              <button class="btn-icon danger" data-delete-scene="${index}" ${locked}
                      title="Delete scene" aria-label="Delete scene">
                ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 14, 2)}</button>` : "") : `
            <button class="btn-icon" data-move-scene="${index}" data-direction="-1"
                    ${index === 0 ? "disabled" : locked} title="Move up" aria-label="Move scene up">
              ${icon(`<path d="M18 15l-6-6-6 6"/>`, 14, 2.2)}</button>
            <button class="btn-icon" data-move-scene="${index}" data-direction="1"
                    ${index === scenes.length - 1 ? "disabled" : locked} title="Move down"
                    aria-label="Move scene down">
              ${icon(`<path d="M6 9l6 6 6-6"/>`, 14, 2.2)}</button>
            <button class="btn-icon danger" data-delete-scene="${index}" ${locked}
                    title="Delete scene" aria-label="Delete scene">
              ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 14, 2)}</button>`}
          </div>
          ${planned[index] ? `<p class="scene-planned"><b>Planned:</b> ${escapeHtml(planned[index].does)}${
            (planned[index].slides ?? []).length ? ` · slide ${planned[index].slides.join(", ")}` : ""}</p>` : ""}
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
      ${planned.length ? `<p class="muted scene-planned-note">The scenes are decided on the Scene
          Plan: add, remove or reorder them there.</p>`
        : `<button class="add-row" data-add-scene ${locked}>${icon(ICON.plus)} Add a scene</button>`}
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

/* ---- what needs the writer's attention on this section --------------------- */

/** Shown in the editor only when there is something: narration that is out of
 *  date with its plan, and review comments addressed to Scripting. */
function renderSectionNotices(script, section) {
  const stale = (script.out_of_date ?? []).find(entry => entry.section_id === section.id);
  const comments = script.comments_by_section?.[section.id] ?? [];
  return `
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
      </div>` : ""}`;
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

function renderFooterNav(stage, script, handoff, tab) {
  const at = SCRIPT_TABS.findIndex(([key]) => key === tab);
  const next = SCRIPT_TABS[at + 1];
  return footerNav(stage, {
    middle: `
      <span class="plan-total" style="margin-left:14px">
        ${script.total_word_count} words · ~${Math.round(script.total_estimated_seconds / 60)} min
      </span>`,
    end: next ? `
      <button class="btn btn-accent btn-move-next" data-script-tab="${next[0]}">
        Move to ${next[1]} ${icon(ICON.arrowRight)}</button>` : null,
    next: {
      carries: handoff.has_transferred ? "The transferred narration and its scenes go on." : "",
      warning: !handoff.has_transferred
        ? "The script has never been transferred: later stages read your working script "
          + "until you transfer it on the Final & transfer tab."
        : handoff.pending
          ? "Your latest changes are not transferred — later stages still read the last "
            + "transferred script."
          : "",
    },
  });
}

/** Redraw only the footer, for a tab change. */
let lastScriptHandoff = null;

let redrawScript = async () => {};

function showScriptTab(tab, stage, navigateToStage) {
  applicationState.scriptTab = tab;
  // Typing saves quietly, without a redraw; the checks and the summary are
  // drawn fresh, so they never describe the script as it was before it.
  if (tab === "final") {
    flushPendingSave().then(() => redrawScript());
    return;
  }
  document.querySelectorAll("[data-script-pane]").forEach(pane => {
    pane.hidden = pane.dataset.scriptPane !== tab;
  });
  document.querySelectorAll(".script-tabs .x-tab").forEach(tabButton => {
    const on = tabButton.dataset.scriptTab === tab;
    tabButton.classList.toggle("on", on);
    tabButton.setAttribute("aria-selected", String(on));
  });
  const footer = select(".stage-content > .footer-nav");
  if (footer && lastScriptHandoff) {
    footer.outerHTML = renderFooterNav(stage, applicationState.script, lastScriptHandoff, tab);
    wireGotoButtons(navigateToStage);
    document.querySelectorAll(".footer-nav [data-script-tab]").forEach(button => {
      button.onclick = () => {
        showScriptTab(button.dataset.scriptTab, stage, navigateToStage);
        select(".x-tabs")?.scrollIntoView({ block: "start", behavior: "smooth" });
      };
    });
  }
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

function wireScriptingStage(stage, navigateToStage, renderAgentStage) {
  wireFactsPanel(() => renderScriptStagingStage(stage, navigateToStage, renderAgentStage));
  const rerender = () => renderScriptStagingStage(stage, navigateToStage, renderAgentStage);
  redrawScript = rerender;
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

  wireGotoButtons(navigateToStage);
  select("#scripting-agent-button").onclick = () => renderAgentStage(stage);

  // Tabs: shown and hidden in place -- every pane is already drawn.
  document.querySelectorAll("[data-script-tab]").forEach(button => {
    button.onclick = async () => {
      await flushPendingSave();
      showScriptTab(button.dataset.scriptTab, stage, navigateToStage);
      if (button.closest(".footer-nav")) {
        select(".x-tabs")?.scrollIntoView({ block: "start", behavior: "smooth" });
      }
    };
  });

  const transferButton = select("#transfer-script-button");
  if (transferButton && !transferButton.disabled) {
    transferButton.onclick = () => runScriptAction({
      path: "/script/transfer", rerender,
      done: "Transferred: the stages after this read exactly this script.",
    });
  }

  const clearLeftovers = select("#delete-unattached-button");
  if (clearLeftovers) {
    clearLeftovers.onclick = () => {
      const count = applicationState.script.orphaned?.length ?? 0;
      if (!window.confirm(`Delete all ${count} piece(s) of narration that belong to no section? `
          + "This cannot be undone.")) return;
      runScriptAction({
        path: "/script/unattached/delete", rerender,
        done: `Deleted ${count} piece(s) of leftover narration.`,
      });
    };
  }

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
      applicationState.scriptEditorTab = tab.dataset.editorTab;
      rerender();
    };
  });

  wireDrafting(rerender);
  wireScenes(change);
  wireSectionContext(rerender);
  wireStrandedNarration(change);
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
