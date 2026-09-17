/**
 * Planning stage — the video outline, and how it relates to the extracted content.
 *
 * The plan is the stage's output and is edited directly. It can also be drafted
 * by the Planning agent from the whole extraction; a draft is shown next to the
 * current plan and taken whole or section by section, never written over it.
 *
 * The bar at the top says where the plan stands against the extraction: nothing
 * extracted, a draft waiting, out of date, not linked, or matching. Before that
 * bar existed a plan could describe a chapter the extraction no longer held, and
 * nothing on the page could tell.
 *
 * Ordinary edits go through `editStageDocument`, which applies the change,
 * re-renders, persists, and rolls back on failure. Drafting, accepting and
 * confirming are single server operations and simply reload afterwards.
 */

import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, icon, notBuiltYet, projectApiPath,
  refreshProjectSummary, select,
  showStageNotice, stageIcon,
} from "/static/ui-kit.js";

/** View state only — it must not survive a reload or leak into the saved plan. */
const planViewState = {
  editingSectionId: null,
  editingSources: [],
  draggingSectionId: null,
  isDrafting: false,
  isActing: false,
  draftInstruction: "",
};

const RENDERING_APPROACHES = [
  ["composition", "Composition", "Labelled diagrams, flows, comparisons"],
  ["plot", "Plot", "Real data on axes"],
  ["simulation", "Simulation", "A physical system in motion"],
  ["code", "Code", "Source code walked through"],
  ["still", "Still", "One frame that teaches the point"],
];
const approachLabel = key => RENDERING_APPROACHES.find(([k]) => k === key)?.[1] ?? "";

function formatDuration(totalSeconds) {
  if (totalSeconds < 60) return `~ ${totalSeconds} sec`;
  return `~ ${Math.round(totalSeconds / 60)} min`;
}

const referenceLabel = reference =>
  [reference.file_name, ...reference.heading_path].join(" › ");

export async function renderPlanningStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  if (!body.querySelector(".plan-bar")) {
    body.innerHTML = `<div class="card muted">Loading plan…</div>`;
  }

  let plan;
  let settings;
  let draft = null;
  try {
    [plan, settings] = await Promise.all([
      loadStageDocument("plan", "/plan"),
      requestJsonFromApi(projectApiPath(`/settings/${stage.key}`)),
    ]);
    // loadStageDocument returns null when the project changed mid-request.
    if (plan === null) return;
    applicationState.stageSettings[stage.key] = settings;
    if (plan.has_pending_draft) {
      draft = await requestJsonFromApi(projectApiPath("/plan/draft"));
      if (!draft.is_pending) draft = null;
    }
  } catch (loadFailure) {
    console.error("plan load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load the plan.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }

  // The bar already speaks for the plan's relationship to the extraction, so
  // the notice carries only the plan's own problems.
  const freshnessWarnings = new Set(plan.freshness?.warnings ?? []);
  const ownWarnings = plan.warnings.filter(warning => !freshnessWarnings.has(warning));

  body.innerHTML = `
    <div class="card">
      <div class="card-head">
        <span class="card-icon">${stageIcon("planning", 21)}</span>
        <div>
          <h2>Planning</h2>
          <p>Turn extracted content into a clear structure for your video.</p>
        </div>
        <button class="btn" id="planning-agent-button">
          ${icon(ICON.gear, 14, 1.8)} Agent &amp; instructions
        </button>
      </div>

      ${renderPlanBar(plan)}

      ${ownWarnings.length ? `
        <div class="notice warn" style="margin-bottom:14px">
          ${ownWarnings.map(escapeHtml).join(" · ")}
        </div>` : ""}

      <div class="plan-grid">
        ${renderOutlinePanel(plan)}
        <div>
          ${draft
            ? renderDraftPanel(draft, plan)
            : `${renderObjectivesPanel(plan)}
               ${renderAudiencePanel(plan)}
               ${renderPreferencesPanel(settings)}
               ${renderThemesPanel(plan)}`}
        </div>
      </div>

      ${renderFooterNav(stage)}
    </div>`;

  wirePlanningStage(stage, navigateToStage, renderAgentStage, draft);
}

/* ---- the plan against the extraction ------------------------------------ */

function renderPlanBar(plan) {
  const freshness = plan.freshness ?? {};
  const documents = plan.source_outline ?? [];
  const headingCount = documents.reduce((sum, d) => sum + d.headings.length, 0);
  const missing = freshness.sections_with_missing_sources ?? [];
  const withoutSources = freshness.sections_without_sources ?? [];

  const bar = (tone, iconPaths, title, detail, actions = "") => `
    <div class="run-bar plan-bar ${tone}">
      <span class="run-icon">${icon(iconPaths, 17, 2.2)}</span>
      <span class="run-text"><b>${title}</b><span>${detail}</span></span>
      ${actions ? `<span class="plan-actions">${actions}</span>` : ""}
    </div>`;

  const draftControls = label => `
    <input id="draft-instruction" class="draft-instruction" maxlength="300"
           placeholder="Guidance for the draft (optional)"
           value="${escapeHtml(planViewState.draftInstruction)}"
           aria-label="Guidance for the draft">
    <button class="btn btn-accent" id="draft-plan-button">${label}</button>`;
  const keepButton = `<button class="btn" id="confirm-plan-button"
      title="I have checked this plan against the current extraction">Keep plan as is</button>`;

  if (!freshness.has_extraction) {
    return bar("blocked", ICON.alert, "Nothing extracted yet",
      "A plan is drafted from what your documents say. Extract them first.",
      `<button class="btn btn-accent" data-goto="extraction">Go to Extraction</button>`);
  }

  if (planViewState.isDrafting) {
    return bar("working", ICON.doc, `Drafting from ${documents.length} document(s)…`,
      `Reading all ${headingCount} headings, then writing each section from its own text.
       This can take a minute or two; it is saved as a draft even if you leave this page.`);
  }

  const scope = `${documents.length} document(s) · ${headingCount} headings extracted`;

  if (plan.has_pending_draft) {
    return bar("pending", ICON.doc, "A drafted plan is waiting for review",
      "Accept all of it, add sections one by one, or discard it. Your plan is unchanged until you do.",
      draftControls("Redraft"));
  }

  if (!plan.sections.length) {
    return bar("ready", ICON.check, "Draft a plan from your extraction",
      escapeHtml(scope), draftControls("Draft plan"));
  }

  if (freshness.is_stale) {
    const extra = missing.length
      ? ` ${missing.length} section(s) point at content that is gone.` : "";
    return bar("stale", ICON.alert, "Out of date with your extraction",
      `The extracted content changed since this plan was drafted or checked.${extra}`,
      draftControls("Redraft") + keepButton);
  }

  if (freshness.is_unlinked) {
    return bar("stale", ICON.alert, "Not linked to your extraction",
      "Nothing records which extracted content each section covers, so this plan cannot be "
      + "checked against it.",
      draftControls("Draft from extraction") + keepButton);
  }

  if (missing.length) {
    return bar("stale", ICON.alert,
      `${missing.length} section(s) point at content that is no longer extracted`,
      escapeHtml(missing.map(m => m.title || "Untitled").join(" · ")),
      draftControls("Redraft"));
  }

  const note = withoutSources.length
    ? `${withoutSources.length} section(s) have no source content recorded.`
    : escapeHtml(scope);
  return bar("ready", ICON.check, "Matches the current extraction", note, draftControls("Redraft"));
}

/* ---- outline ------------------------------------------------------------ */

function renderOutlinePanel(plan) {
  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Video outline</h3>
        <div class="spacer"></div>
        <span class="plan-total">${plan.sections.length} sections ·
          ${formatDuration(plan.total_estimated_seconds)}</span>
      </div>
      <p class="panel-sub">Drag to reorder, or click a section to edit it.</p>

      <div id="outline-list">
        ${plan.sections.length
          ? plan.sections.map((section, index) => renderOutlineRow(section, index, plan)).join("")
          : `<p class="muted" style="font-size:12.5px;margin:0 0 10px">
               No sections yet. Draft a plan from your extraction, or add one by hand.</p>`}
      </div>

      <button class="add-row" id="add-section-button">
        ${icon(ICON.plus)} Add new section
      </button>
    </div>`;
}

/** The numbers of the plan's learning objectives a section serves. */
function objectiveNumbersFor(section, plan) {
  return (section.objective_ids ?? [])
    .map(id => plan.learning_objectives.findIndex(o => o.id === id) + 1)
    .filter(number => number > 0);
}

function renderObjectiveFact(section, plan) {
  const numbers = objectiveNumbersFor(section, plan);
  return numbers.length
    ? `<div class="section-facts"><span class="fact" title="Learning objectives this section serves">
         objective${numbers.length === 1 ? "" : "s"} ${numbers.join(", ")}</span></div>`
    : "";
}

/** Small facts under a section: how it is shown, what it draws on, what it serves. */
function renderSectionFacts(section, plan, { missing = [] } = {}) {
  const usesSources = plan.freshness?.is_linked
    || plan.sections.some(s => (s.sources ?? []).length);
  const objectiveNumbers = objectiveNumbersFor(section, plan);
  const sources = section.sources ?? [];

  const facts = [];
  if (section.rendering_approach) {
    facts.push(`<span class="fact approach ${escapeHtml(section.rendering_approach)}"
      title="${escapeHtml(section.rendering_reason || "")}">${
        escapeHtml(approachLabel(section.rendering_approach))}</span>`);
  }
  if (sources.length) {
    facts.push(`<span class="fact" title="${escapeHtml(sources.map(referenceLabel).join("\n"))}">
      ${sources.length} source${sources.length === 1 ? "" : "s"}</span>`);
  } else if (usesSources) {
    facts.push(`<span class="fact muted">no source</span>`);
  }
  if (missing.length) {
    facts.push(`<span class="fact bad" title="${escapeHtml(missing.join("\n"))}">
      source missing</span>`);
  }
  if (objectiveNumbers.length) {
    facts.push(`<span class="fact" title="Learning objectives this section serves">
      objective${objectiveNumbers.length === 1 ? "" : "s"} ${objectiveNumbers.join(", ")}</span>`);
  }
  return facts.length ? `<div class="section-facts">${facts.join("")}</div>` : "";
}

function renderOutlineRow(section, index, plan) {
  if (planViewState.editingSectionId === section.id) {
    return renderSectionEditor(section, index, plan);
  }

  const isOddDuration = section.estimated_seconds < 10 || section.estimated_seconds > 600;
  const missing = (plan.freshness?.sections_with_missing_sources ?? [])
    .find(entry => entry.section_id === section.id)?.missing ?? [];

  return `
    <div class="outline-row ${missing.length ? "has-missing" : ""}" data-section="${section.id}"
         draggable="true">
      <span class="grip" aria-hidden="true">
        ${icon(`<circle cx="9" cy="6" r="1.4"/><circle cx="9" cy="12" r="1.4"/>
                <circle cx="9" cy="18" r="1.4"/><circle cx="15" cy="6" r="1.4"/>
                <circle cx="15" cy="12" r="1.4"/><circle cx="15" cy="18" r="1.4"/>`, 15, 0)}
      </span>
      <span class="outline-num">${index + 1}</span>
      <div class="outline-body">
        <div class="title ${section.title ? "" : "untitled"}">
          ${escapeHtml(section.title || "Untitled section")}</div>
        ${section.summary
          ? `<div class="summary">${escapeHtml(section.summary)}</div>` : ""}
        ${renderSectionFacts(section, plan, { missing })}
      </div>
      <span class="outline-duration ${isOddDuration ? "odd" : ""}"
            title="${isOddDuration ? "Unusual length for one section" : ""}">
        ${formatDuration(section.estimated_seconds)}</span>
      <button class="btn-icon" data-edit-section="${section.id}"
              title="Edit" aria-label="Edit ${escapeHtml(section.title || "section")}">
        ${icon(`<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/>`, 15, 1.8)}
      </button>
    </div>`;
}

function renderSectionEditor(section, index, plan) {
  const outline = plan.source_outline ?? [];
  const sourceOptions = outline.map(document => `
    <optgroup label="${escapeHtml(document.file_name)}">
      <option value="${escapeHtml(JSON.stringify({ file_name: document.file_name, heading_path: [] }))}"
        >Whole document · ${document.words} words</option>
      ${document.headings.map(heading => `
        <option value="${escapeHtml(JSON.stringify({
          file_name: document.file_name, heading_path: heading.heading_path }))}"
          >${"  ".repeat(Math.max(0, heading.level - 1))}${
            escapeHtml(heading.heading_path.at(-1) ?? "")} · ${heading.words} words</option>`).join("")}
    </optgroup>`).join("");

  return `
    <div class="outline-row editing" data-section="${section.id}">
      <span class="outline-num">${index + 1}</span>
      <div class="outline-edit">
        <input id="edit-title" value="${escapeHtml(section.title)}"
               placeholder="Section title" maxlength="120" aria-label="Section title">
        <textarea id="edit-summary" placeholder="What this section covers"
                  maxlength="400" aria-label="Section summary">${escapeHtml(section.summary)}</textarea>

        <div class="edit-field">
          <label for="edit-approach">How to show it</label>
          <div class="edit-pair">
            <select id="edit-approach">
              <option value="">Not chosen</option>
              ${RENDERING_APPROACHES.map(([key, label, hint]) => `
                <option value="${key}" ${section.rendering_approach === key ? "selected" : ""}
                  >${label} — ${hint}</option>`).join("")}
            </select>
            <input id="edit-reason" maxlength="240" placeholder="Why, in one sentence"
                   value="${escapeHtml(section.rendering_reason ?? "")}" aria-label="Why">
          </div>
        </div>

        <div class="edit-field">
          <label for="edit-add-source">Source content</label>
          <div id="edit-sources" class="source-chips"></div>
          ${outline.length
            ? `<select id="edit-add-source">
                 <option value="">Add extracted content…</option>${sourceOptions}
               </select>`
            : `<p class="muted edit-hint">Nothing extracted yet to point at.</p>`}
        </div>

        ${plan.learning_objectives.length ? `
          <div class="edit-field">
            <label>Learning objectives it serves</label>
            <div class="edit-objectives">
              ${plan.learning_objectives.map((objective, number) => `
                <label class="edit-objective">
                  <input type="checkbox" data-edit-objective-link="${objective.id}"
                         ${(section.objective_ids ?? []).includes(objective.id) ? "checked" : ""}>
                  <span><b>${number + 1}.</b> ${escapeHtml(objective.text)}</span>
                </label>`).join("")}
            </div>
          </div>` : ""}

        <div class="edit-row">
          <label for="edit-seconds">Seconds</label>
          <input id="edit-seconds" type="number" min="1" max="3600"
                 value="${section.estimated_seconds}">
          <div class="spacer" style="flex:1"></div>
          <button class="btn btn-accent" id="save-section-button">Done</button>
          <button class="btn-icon danger" id="delete-section-button"
                  title="Delete section" aria-label="Delete section">
            ${icon(`<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>`, 16, 1.8)}
          </button>
        </div>
      </div>
    </div>`;
}

/** The chosen sources, redrawn in place: re-rendering the stage would throw away
 *  a title or summary typed but not yet saved. */
function renderEditingSources() {
  const host = select("#edit-sources");
  if (!host) return;
  host.innerHTML = planViewState.editingSources.length
    ? planViewState.editingSources.map((reference, position) => `
        <span class="source-chip" title="${escapeHtml(referenceLabel(reference))}">
          ${escapeHtml(referenceLabel(reference))}
          <button type="button" data-remove-source="${position}"
                  aria-label="Remove this source">×</button>
        </span>`).join("")
    : `<span class="muted edit-hint">None yet.</span>`;

  host.querySelectorAll("[data-remove-source]").forEach(button => {
    button.onclick = () => {
      planViewState.editingSources.splice(Number(button.dataset.removeSource), 1);
      renderEditingSources();
    };
  });
}

/* ---- a drafted plan, next to the current one ----------------------------- */

function renderDraftPanel(draft, currentPlan) {
  const proposed = draft.plan;
  const accepted = new Set(draft.accepted_section_ids ?? []);
  const notes = draft.notes ?? [];
  const drafted = draft.created_at ? new Date(draft.created_at).toLocaleString() : "";

  return `
    <div class="panel draft-panel">
      <div class="panel-head">
        <h3>Proposed plan</h3>
        <div class="spacer"></div>
        <span class="plan-total">${proposed.sections.length} sections ·
          ${formatDuration(proposed.total_estimated_seconds)}</span>
      </div>
      <p class="panel-sub">
        Drafted by the ${escapeHtml(draft.agent ?? "Planning")} agent from
        ${(draft.documents_read ?? []).length} document(s) and ${draft.headings_read ?? 0} headings
        ${drafted ? `· ${escapeHtml(drafted)}` : ""}
        ${draft.instruction ? `· guidance: “${escapeHtml(draft.instruction)}”` : ""}
      </p>

      <div class="draft-actions">
        <button class="btn btn-accent" id="accept-draft-button">Accept all</button>
        <button class="btn" id="discard-draft-button">Discard</button>
      </div>

      ${draft.replaces_narrated_sections && currentPlan.sections.length ? `
        <div class="notice warn draft-notice">
          <b>Accept all</b> replaces your ${currentPlan.sections.length} current section(s).
          Narration already written for ${draft.replaces_narrated_sections} of them in
          Scripting is kept, but no longer attached to a section.
          Use <b>Add to plan</b> to keep your sections and add these alongside.
        </div>` : ""}

      ${draft.is_behind_extraction ? `
        <div class="notice warn draft-notice">
          The extraction changed after this draft was made. Redraft to plan from what is
          extracted now.
        </div>` : ""}

      ${notes.length ? `
        <details class="draft-notes">
          <summary>Notes from drafting (${notes.length})</summary>
          <ul>${notes.map(note => `<li>${escapeHtml(note)}</li>`).join("")}</ul>
        </details>` : ""}

      ${proposed.learning_objectives.length ? `
        <div class="draft-objectives">
          <b>Learning objectives</b>
          <ol>${proposed.learning_objectives.map(o => `<li>${escapeHtml(o.text)}</li>`).join("")}</ol>
        </div>` : ""}

      ${proposed.key_themes.length ? `
        <div class="pill-row draft-themes">
          ${proposed.key_themes.map(theme => `<span class="pill theme">${escapeHtml(theme)}</span>`)
            .join("")}
        </div>` : ""}

      <div class="draft-sections">
        ${proposed.sections.map((section, index) => `
          <div class="draft-section ${accepted.has(section.id) ? "added" : ""}">
            <div class="draft-section-head">
              <span class="outline-num">${index + 1}</span>
              <b>${escapeHtml(section.title || "Untitled section")}</b>
              <div class="spacer"></div>
              <span class="outline-duration">${formatDuration(section.estimated_seconds)}</span>
            </div>
            ${section.summary ? `<p class="summary">${escapeHtml(section.summary)}</p>` : ""}
            ${section.rendering_approach ? `
              <p class="draft-approach">
                <span class="fact approach ${escapeHtml(section.rendering_approach)}">
                  ${escapeHtml(approachLabel(section.rendering_approach))}</span>
                ${escapeHtml(section.rendering_reason ?? "")}
              </p>` : ""}
            <div class="source-chips">
              ${(section.sources ?? []).map(reference => `
                <span class="source-chip">${escapeHtml(referenceLabel(reference))}</span>`).join("")
                || `<span class="fact bad">no source content</span>`}
            </div>
            ${renderObjectiveFact(section, proposed)}
            <div class="draft-section-actions">
              ${accepted.has(section.id)
                ? `<span class="fact ok">added to your plan</span>`
                : `<button class="btn" data-accept-section="${section.id}">Add to plan</button>`}
            </div>
          </div>`).join("")}
      </div>
    </div>`;
}

/* ---- side panels -------------------------------------------------------- */

function renderObjectivesPanel(plan) {
  const coverage = plan.objective_coverage ?? {};
  const isLinked = plan.sections.some(section => (section.objective_ids ?? []).length);
  const sectionNumber = id => plan.sections.findIndex(section => section.id === id) + 1;

  return `
    <div class="panel" style="margin-bottom:14px">
      <div class="panel-head">
        <h3>Learning objectives</h3>
        <div class="spacer"></div>
        <button class="btn-icon" id="add-objective-button"
                title="Add objective" aria-label="Add objective">${icon(ICON.plus, 15)}</button>
      </div>
      <p class="panel-sub">What should the viewer learn from this video?</p>

      ${plan.learning_objectives.length
        ? plan.learning_objectives.map((objective, number) => {
            const covering = (coverage[objective.id] ?? []).map(sectionNumber).filter(Boolean);
            const coverageChip = !isLinked || !objective.is_included ? ""
              : covering.length
                ? `<span class="fact ok" title="Sections that serve this objective">§ ${covering.join(", ")}</span>`
                : `<span class="fact warn">not covered</span>`;
            return `
          <div class="objective-row">
            <span class="checkbox ${objective.is_included ? "on" : ""}"
                  data-toggle-objective="${objective.id}" role="checkbox"
                  aria-checked="${objective.is_included}"
                  aria-label="Include this objective">
              ${icon(ICON.check, 11, 3.5)}
            </span>
            <span class="objective-number">${number + 1}</span>
            <span class="text ${objective.is_included ? "" : "off"}"
                  data-edit-objective="${objective.id}" title="Click to edit"
                  >${escapeHtml(objective.text || "(empty)")}</span>
            ${coverageChip}
            <button class="btn-icon danger" data-delete-objective="${objective.id}"
                    title="Remove" aria-label="Remove objective">
              ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 14, 2)}
            </button>
          </div>`;
          }).join("")
        : `<p class="muted" style="font-size:12.5px;margin:0">
             None yet. These guide what Scripting emphasises.</p>`}
    </div>`;
}

function renderAudiencePanel(plan) {
  return `
    <div class="panel" style="margin-bottom:14px">
      <div class="panel-head"><h3>Target audience</h3></div>
      <p class="panel-sub">Helps tailor the tone and depth.</p>
      <div class="pill-row">
        ${plan.audience_choices.map(audience => `
          <button class="pill ${audience === plan.selected_audience ? "on" : ""}"
                  data-audience="${escapeHtml(audience)}"
                  aria-pressed="${audience === plan.selected_audience}">
            ${escapeHtml(audience)}</button>`).join("")}
        <button class="pill ghost" id="add-audience-button">${icon(ICON.plus, 12)} Add</button>
      </div>
    </div>`;
}

function renderPreferencesPanel(settings) {
  return `
    <div class="panel" style="margin-bottom:14px">
      <div class="panel-head">
        <h3>Video preferences</h3>
        <div class="spacer"></div>
        <span class="mono muted" id="settings-saved-hint"></span>
      </div>
      ${settings.options.map(option => {
        const currentValue = settings.values[option.key];
        const activeChoice = option.choices.find(choice => choice.value === currentValue);
        const inert = option.implemented === false;
        return `
          <div class="option${inert ? " inert" : ""}">
            <label for="pref-${escapeHtml(option.key)}">${escapeHtml(option.label)}
              ${notBuiltYet(option)}</label>
            <select id="pref-${escapeHtml(option.key)}" data-option="${escapeHtml(option.key)}"
                    ${inert ? "disabled" : ""}>
              ${option.choices.map(choice => `
                <option value="${escapeHtml(choice.value)}"
                        ${choice.value === currentValue ? "selected" : ""}>
                  ${escapeHtml(choice.label)}</option>`).join("")}
            </select>
            ${activeChoice?.help_text
              ? `<p class="help">${escapeHtml(activeChoice.help_text)}</p>` : ""}
          </div>`;
      }).join("")}
    </div>`;
}

function renderThemesPanel(plan) {
  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Key themes</h3>
        <div class="spacer"></div>
        <button class="btn-icon" id="add-theme-button"
                title="Add theme" aria-label="Add theme">${icon(ICON.plus, 15)}</button>
      </div>
      <p class="panel-sub">Proposed from the source when a plan is drafted, or add your own.</p>
      <div class="pill-row">
        ${plan.key_themes.length
          ? plan.key_themes.map(theme => `
            <button class="pill theme" data-remove-theme="${escapeHtml(theme)}"
                    title="Click to remove">${escapeHtml(theme)}</button>`).join("")
          : `<span class="muted" style="font-size:12.5px">None yet.</span>`}
      </div>
    </div>`;
}

function renderFooterNav(stage) {
  const { stageDefinitions } = applicationState;
  const stageIndex = stageDefinitions.findIndex(s => s.key === stage.key);
  const previousStage = stageDefinitions[stageIndex - 1];
  const nextStage = stageDefinitions[stageIndex + 1];
  const hasSections = (applicationState.plan?.sections ?? []).length > 0;

  return `
    <div class="footer-nav">
      ${previousStage ? `
        <button class="btn" data-goto="${previousStage.key}">
          ${icon(ICON.arrowLeft)} Back to ${escapeHtml(previousStage.title)}
        </button>` : ""}
      <div class="spacer"></div>
      ${nextStage ? `
        <button class="btn btn-accent" data-goto="${nextStage.key}"
                ${hasSections ? "" : "disabled"}
                title="${hasSections ? "" : "Add at least one section first"}">
          Next: ${escapeHtml(nextStage.title)} ${icon(ICON.arrowRight)}
        </button>` : ""}
    </div>`;
}

/* ---- server actions ------------------------------------------------------ */

/** One call to the server, then a fresh render. Each of these changes more than
 *  one field, and the server decides the result, so there is nothing sensible to
 *  apply optimistically. */
async function runPlanAction({ path, method = "POST", body, pending, done, rerender }) {
  if (planViewState.isActing) {
    showStageNotice("warn", "Still working on the last action — try again in a moment.");
    return;
  }
  planViewState.isActing = true;
  if (pending) showStageNotice("ok", pending);
  try {
    await requestJsonFromApi(projectApiPath(path), {
      method,
      headers: { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    await refreshProjectSummary();
    await rerender();
    if (done) showStageNotice("ok", done);
  } catch (actionFailure) {
    console.error("plan action failed", path, actionFailure);
    showStageNotice("bad", actionFailure.message);
  } finally {
    planViewState.isActing = false;
  }
}

async function draftPlan(rerender) {
  if (planViewState.isDrafting) {
    showStageNotice("warn", "A draft is already being written.");
    return;
  }
  planViewState.draftInstruction = select("#draft-instruction")?.value.trim() ?? "";
  planViewState.isDrafting = true;
  await rerender();
  try {
    await requestJsonFromApi(projectApiPath("/plan/draft"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ instruction: planViewState.draftInstruction }),
    });
    planViewState.isDrafting = false;
    await rerender();
    showStageNotice("ok", "Draft ready. Review it next to your current plan.");
  } catch (draftFailure) {
    console.error("drafting failed", draftFailure);
    planViewState.isDrafting = false;
    await rerender();
    showStageNotice("bad", `Could not draft a plan — ${draftFailure.message}`);
  }
}

/* ---- wiring ------------------------------------------------------------- */

function wirePlanningStage(stage, navigateToStage, renderAgentStage, draft) {
  const rerender = () => renderPlanningStage(stage, navigateToStage, renderAgentStage);
  const change = applyEdit => editStageDocument({
    documentKind: "plan", apiPathSuffix: "/plan", applyEdit, rerender,
  });

  select("#planning-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });

  // --- the plan against the extraction ---
  const draftButton = select("#draft-plan-button");
  if (draftButton) draftButton.onclick = () => draftPlan(rerender);
  select("#draft-instruction")?.addEventListener("keydown", event => {
    if (event.key === "Enter") draftPlan(rerender);
  });

  const confirmButton = select("#confirm-plan-button");
  if (confirmButton) {
    confirmButton.onclick = () => runPlanAction({
      path: "/plan/confirm-extraction", rerender,
      done: "Recorded: this plan matches the current extraction.",
    });
  }

  // --- reviewing a draft ---
  if (draft) {
    select("#accept-draft-button").onclick = () => runPlanAction({
      path: "/plan/draft/accept", body: {}, rerender,
      done: "The drafted plan is now your plan.",
    });
    select("#discard-draft-button").onclick = () => runPlanAction({
      path: "/plan/draft", method: "DELETE", rerender, done: "Draft discarded.",
    });
    document.querySelectorAll("[data-accept-section]").forEach(button => {
      button.onclick = () => runPlanAction({
        path: "/plan/draft/accept", body: { section_ids: [button.dataset.acceptSection] },
        rerender, done: "Section added to your plan.",
      });
    });
  }

  // --- outline ---
  select("#add-section-button").onclick = () => change(plan => {
    const newSection = {
      id: newItemIdentifier(),
      title: "", summary: "", estimated_seconds: 60,
      sources: [], rendering_approach: "", rendering_reason: "", objective_ids: [],
    };
    plan.sections.push(newSection);
    planViewState.editingSectionId = newSection.id;
    planViewState.editingSources = [];
  });

  document.querySelectorAll("[data-edit-section]").forEach(button => {
    button.onclick = () => {
      const section = applicationState.plan.sections
        .find(s => s.id === button.dataset.editSection);
      planViewState.editingSectionId = button.dataset.editSection;
      planViewState.editingSources = structuredClone(section?.sources ?? []);
      rerender();
    };
  });

  const titleInput = select("#edit-title");
  if (titleInput) {
    titleInput.focus();
    titleInput.setSelectionRange(titleInput.value.length, titleInput.value.length);
    renderEditingSources();

    const addSource = select("#edit-add-source");
    if (addSource) {
      addSource.onchange = () => {
        if (!addSource.value) return;
        const reference = JSON.parse(addSource.value);
        const key = JSON.stringify(reference);
        if (!planViewState.editingSources.some(existing => JSON.stringify(existing) === key)) {
          planViewState.editingSources.push(reference);
        }
        addSource.value = "";
        renderEditingSources();
      };
    }

    const commitEdit = () => {
      const editingId = planViewState.editingSectionId;
      const edited = {
        title: select("#edit-title").value,
        summary: select("#edit-summary").value,
        estimated_seconds: Number(select("#edit-seconds").value) || 60,
        rendering_approach: select("#edit-approach").value,
        rendering_reason: select("#edit-reason").value,
        sources: structuredClone(planViewState.editingSources),
        objective_ids: [...document.querySelectorAll("[data-edit-objective-link]:checked")]
          .map(box => box.dataset.editObjectiveLink),
      };
      planViewState.editingSectionId = null;
      planViewState.editingSources = [];
      change(plan => {
        const section = plan.sections.find(s => s.id === editingId);
        if (section) Object.assign(section, edited);
      });
    };

    select("#save-section-button").onclick = commitEdit;
    // Enter commits from the title field; the summary is multi-line so Enter
    // there must insert a newline rather than close the editor.
    titleInput.addEventListener("keydown", event => {
      if (event.key === "Enter") { event.preventDefault(); commitEdit(); }
      if (event.key === "Escape") {
        planViewState.editingSectionId = null;
        planViewState.editingSources = [];
        rerender();
      }
    });

    select("#delete-section-button").onclick = () => {
      const editingId = planViewState.editingSectionId;
      planViewState.editingSectionId = null;
      planViewState.editingSources = [];
      change(plan => {
        plan.sections = plan.sections.filter(s => s.id !== editingId);
      });
    };
  }

  wireOutlineDragAndDrop(change);

  // The side panels are replaced by the draft while one is under review.
  if (draft) return;

  // --- objectives ---
  select("#add-objective-button").onclick = () => change(plan => {
    plan.learning_objectives.push({
      id: newItemIdentifier(),
      text: "New objective", is_included: true,
    });
  });

  document.querySelectorAll("[data-toggle-objective]").forEach(box => {
    box.onclick = () => change(plan => {
      const objective = plan.learning_objectives
        .find(o => o.id === box.dataset.toggleObjective);
      if (objective) objective.is_included = !objective.is_included;
    });
  });

  document.querySelectorAll("[data-edit-objective]").forEach(textNode => {
    textNode.onclick = () => promptInline(textNode, currentText =>
      change(plan => {
        const objective = plan.learning_objectives
          .find(o => o.id === textNode.dataset.editObjective);
        if (objective) objective.text = currentText;
      }));
  });

  document.querySelectorAll("[data-delete-objective]").forEach(button => {
    button.onclick = () => change(plan => {
      const removedId = button.dataset.deleteObjective;
      plan.learning_objectives = plan.learning_objectives.filter(o => o.id !== removedId);
      // The server drops dangling links too; doing it here keeps the page right
      // during the save instead of after it.
      plan.sections.forEach(section => {
        section.objective_ids = (section.objective_ids ?? []).filter(id => id !== removedId);
      });
    });
  });

  // --- audience ---
  document.querySelectorAll("[data-audience]").forEach(pill => {
    pill.onclick = () => change(plan => {
      plan.selected_audience = pill.dataset.audience;
    });
  });

  select("#add-audience-button").onclick = () => {
    const audience = window.prompt("Describe the audience");
    if (!audience?.trim()) return;
    change(plan => {
      const trimmed = audience.trim().slice(0, 80);
      if (!plan.audience_choices.includes(trimmed)) plan.audience_choices.push(trimmed);
      plan.selected_audience = trimmed;
    });
  };

  // --- themes ---
  select("#add-theme-button").onclick = () => {
    const theme = window.prompt("Add a key theme");
    if (!theme?.trim()) return;
    change(plan => {
      const trimmed = theme.trim().slice(0, 60);
      if (!plan.key_themes.includes(trimmed)) plan.key_themes.push(trimmed);
    });
  };

  document.querySelectorAll("[data-remove-theme]").forEach(pill => {
    pill.onclick = () => change(plan => {
      plan.key_themes = plan.key_themes.filter(t => t !== pill.dataset.removeTheme);
    });
  });

  // --- preferences ---
  document.querySelectorAll("[data-option]").forEach(control => {
    if (control.disabled) return;
    control.onchange = () => persistPreference(stage, control.dataset.option, control.value);
  });
}

/** Swap a label for an input in place, commit on blur or Enter. Avoids a modal
 *  for what is a one-field edit. */
function promptInline(textNode, commit) {
  const input = document.createElement("input");
  input.className = "text-input";
  input.value = textNode.textContent.trim() === "(empty)" ? "" : textNode.textContent.trim();
  input.maxLength = 200;
  textNode.replaceWith(input);
  input.focus();
  input.select();

  let hasCommitted = false;
  const finish = shouldCommit => {
    if (hasCommitted) return;      // blur fires after Enter; commit once
    hasCommitted = true;
    if (shouldCommit) commit(input.value.trim());
    else input.replaceWith(textNode);
  };

  input.addEventListener("keydown", event => {
    if (event.key === "Enter") finish(true);
    if (event.key === "Escape") finish(false);
  });
  input.addEventListener("blur", () => finish(true));
}

function wireOutlineDragAndDrop(change) {
  const rows = document.querySelectorAll(".outline-row[draggable]");

  rows.forEach(row => {
    row.addEventListener("dragstart", event => {
      planViewState.draggingSectionId = row.dataset.section;
      row.classList.add("dragging");
      event.dataTransfer.effectAllowed = "move";
      // Firefox refuses to start a drag unless data is set.
      event.dataTransfer.setData("text/plain", row.dataset.section);
    });

    row.addEventListener("dragend", () => {
      planViewState.draggingSectionId = null;
      document.querySelectorAll(".outline-row")
        .forEach(other => other.classList.remove("dragging", "drop-target"));
    });

    row.addEventListener("dragover", event => {
      event.preventDefault();
      if (row.dataset.section !== planViewState.draggingSectionId) {
        row.classList.add("drop-target");
      }
    });

    row.addEventListener("dragleave", () => row.classList.remove("drop-target"));

    row.addEventListener("drop", event => {
      event.preventDefault();
      const draggedId = planViewState.draggingSectionId;
      const targetId = row.dataset.section;
      if (!draggedId || draggedId === targetId) return;

      change(plan => {
        const fromIndex = plan.sections.findIndex(s => s.id === draggedId);
        const toIndex = plan.sections.findIndex(s => s.id === targetId);
        if (fromIndex < 0 || toIndex < 0) return;
        const [moved] = plan.sections.splice(fromIndex, 1);
        plan.sections.splice(toIndex, 0, moved);
      });
    });
  });
}

async function persistPreference(stage, optionKey, newValue) {
  // A control that silently does nothing reads as broken. Say why instead
  // of dropping the interaction.
  if (applicationState.isSavingSettings) {
    showStageNotice("warn", "Still saving the last change — try again in a moment.");
    return;
  }
  applicationState.isSavingSettings = true;

  const settings = applicationState.stageSettings[stage.key];
  const previousValue = settings.values[optionKey];
  settings.values[optionKey] = newValue;

  try {
    applicationState.stageSettings[stage.key] = await requestJsonFromApi(
      projectApiPath(`/settings/${stage.key}`),
      {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ values: settings.values }),
      });
    const savedHint = select("#settings-saved-hint");
    if (savedHint) {
      savedHint.textContent = "saved";
      setTimeout(() => { if (savedHint.isConnected) savedHint.textContent = ""; }, 1600);
    }
  } catch (saveFailure) {
    console.error("preference save failed", saveFailure);
    settings.values[optionKey] = previousValue;
    showStageNotice("bad", `Could not save that preference — ${saveFailure.message}`);
  } finally {
    applicationState.isSavingSettings = false;
  }
}
