/**
 * Planning stage — the video outline and everything that shapes it.
 *
 * Unlike Extraction, this stage's *output* is edited directly: the plan is the
 * artifact. An agent will also be able to generate one, and both paths write the
 * same document, so there is never a generated plan and an edited plan that drift.
 *
 * Every mutation goes through `mutatePlan`, which applies the change locally,
 * re-renders, then persists — and rolls back on failure. That keeps optimistic
 * editing in one place rather than repeated per control.
 */

import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, icon, projectApiPath, select,
  showStageNotice, stageIcon,
} from "/static/ui-kit.js";

/** Which section is open for editing, and which is mid-drag. View state only —
 *  it must not survive a reload or leak into the saved plan. */
const planViewState = {
  editingSectionId: null,
  draggingSectionId: null,
};

function formatDuration(totalSeconds) {
  if (totalSeconds < 60) return `~ ${totalSeconds} sec`;
  const minutes = Math.round(totalSeconds / 60);
  return `~ ${minutes} min`;
}

export async function renderPlanningStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  body.innerHTML = `<div class="card muted">Loading plan…</div>`;

  let plan;
  let settings;
  try {
    [plan, settings] = await Promise.all([
      loadStageDocument("plan", "/plan"),
      requestJsonFromApi(projectApiPath(`/settings/${stage.key}`)),
    ]);
    // loadStageDocument returns null when the project changed mid-request.
    if (plan === null) return;
    applicationState.stageSettings[stage.key] = settings;
  } catch (loadFailure) {
    console.error("plan load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load the plan.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }

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

      ${plan.warnings.length ? `
        <div class="notice warn" style="margin-bottom:14px">
          ${plan.warnings.map(escapeHtml).join(" · ")}
        </div>` : ""}

      <div class="plan-grid">
        ${renderOutlinePanel(plan)}
        <div>
          ${renderObjectivesPanel(plan)}
          ${renderAudiencePanel(plan)}
          ${renderPreferencesPanel(settings)}
          ${renderThemesPanel(plan)}
        </div>
      </div>

      ${renderFooterNav(stage)}
    </div>`;

  wirePlanningStage(stage, navigateToStage, renderAgentStage);
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
          ? plan.sections.map((section, index) => renderOutlineRow(section, index)).join("")
          : `<p class="muted" style="font-size:12.5px;margin:0 0 10px">
               No sections yet. Add one, or let the agent draft an outline.</p>`}
      </div>

      <button class="add-row" id="add-section-button">
        ${icon(ICON.plus)} Add new section
      </button>
    </div>`;
}

function renderOutlineRow(section, index) {
  if (planViewState.editingSectionId === section.id) {
    return `
      <div class="outline-row editing" data-section="${section.id}">
        <span class="outline-num">${index + 1}</span>
        <div class="outline-edit">
          <input id="edit-title" value="${escapeHtml(section.title)}"
                 placeholder="Section title" maxlength="120" aria-label="Section title">
          <textarea id="edit-summary" placeholder="What this section covers"
                    maxlength="400" aria-label="Section summary">${escapeHtml(section.summary)}</textarea>
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

  const isOddDuration = section.estimated_seconds < 10 || section.estimated_seconds > 600;

  return `
    <div class="outline-row" data-section="${section.id}" draggable="true">
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

/* ---- side panels -------------------------------------------------------- */

function renderObjectivesPanel(plan) {
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
        ? plan.learning_objectives.map(objective => `
          <div class="objective-row">
            <span class="checkbox ${objective.is_included ? "on" : ""}"
                  data-toggle-objective="${objective.id}" role="checkbox"
                  aria-checked="${objective.is_included}"
                  aria-label="Include this objective">
              ${icon(ICON.check, 11, 3.5)}
            </span>
            <span class="text ${objective.is_included ? "" : "off"}"
                  data-edit-objective="${objective.id}" title="Click to edit"
                  >${escapeHtml(objective.text || "(empty)")}</span>
            <button class="btn-icon danger" data-delete-objective="${objective.id}"
                    title="Remove" aria-label="Remove objective">
              ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 14, 2)}
            </button>
          </div>`).join("")
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
        return `
          <div class="option">
            <label for="pref-${escapeHtml(option.key)}">${escapeHtml(option.label)}</label>
            <select id="pref-${escapeHtml(option.key)}" data-option="${escapeHtml(option.key)}">
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
      <p class="panel-sub">Extraction will fill these in; add your own meanwhile.</p>
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

/* ---- mutation ----------------------------------------------------------- */

/* ---- wiring ------------------------------------------------------------- */

function wirePlanningStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderPlanningStage(stage, navigateToStage, renderAgentStage);
  const change = applyEdit => editStageDocument({
    documentKind: "plan", apiPathSuffix: "/plan", applyEdit, rerender,
  });

  select("#planning-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });

  // --- outline ---
  select("#add-section-button").onclick = () => change(plan => {
    const newSection = {
      id: newItemIdentifier(),
      title: "", summary: "", estimated_seconds: 60,
    };
    plan.sections.push(newSection);
    planViewState.editingSectionId = newSection.id;
  });

  document.querySelectorAll("[data-edit-section]").forEach(button => {
    button.onclick = () => {
      planViewState.editingSectionId = button.dataset.editSection;
      rerender();
    };
  });

  const titleInput = select("#edit-title");
  if (titleInput) {
    titleInput.focus();
    titleInput.setSelectionRange(titleInput.value.length, titleInput.value.length);

    const commitEdit = () => {
      const editingId = planViewState.editingSectionId;
      const title = select("#edit-title").value;
      const summary = select("#edit-summary").value;
      const seconds = Number(select("#edit-seconds").value) || 60;
      planViewState.editingSectionId = null;
      change(plan => {
        const section = plan.sections.find(s => s.id === editingId);
        if (section) Object.assign(section, {
          title, summary, estimated_seconds: seconds,
        });
      });
    };

    select("#save-section-button").onclick = commitEdit;
    // Enter commits from the title field; the summary is multi-line so Enter
    // there must insert a newline rather than close the editor.
    titleInput.addEventListener("keydown", event => {
      if (event.key === "Enter") { event.preventDefault(); commitEdit(); }
      if (event.key === "Escape") { planViewState.editingSectionId = null; rerender(); }
    });

    select("#delete-section-button").onclick = () => {
      const editingId = planViewState.editingSectionId;
      planViewState.editingSectionId = null;
      change(plan => {
        plan.sections = plan.sections.filter(s => s.id !== editingId);
      });
    };
  }

  wireOutlineDragAndDrop(change);

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
      plan.learning_objectives = plan.learning_objectives
        .filter(o => o.id !== button.dataset.deleteObjective);
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
