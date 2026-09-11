/**
 * Explainer Pipeline — application shell.
 *
 * Owns the chrome (topbar, sidebar, breadcrumb) and routes to a stage
 * view. Stage views live in their own modules and import shared state from
 * ui-kit.js, so this file never grows when a stage gains features.
 */

import {
  closeCredentialsPanel, isCredentialsPanelOpen, openCredentialsPanel,
} from "/static/credentials-panel.js";
import { requestJsonFromApi, showNoticeIn } from "/static/shared-client.js";
import { renderExtractionStage } from "/static/stage-extraction.js";
import { renderPlanningStage } from "/static/stage-planning.js";
import { renderScriptingStage } from "/static/stage-scripting.js";
import { renderReviewingStage } from "/static/stage-reviewing.js";
import { renderStudioStage } from "/static/stage-studio.js";
import {
  ICON, applicationState, clearProjectScopedState, escapeHtml, fileTypeBadge,
  formatFileSize, icon, projectApiPath, select, showStageNotice, sortedSources,
  stageIcon, stageStateFor,
} from "/static/ui-kit.js";

/* ---- boot --------------------------------------------------------------- */

async function boot() {
  select("#main-inner").innerHTML = `<div class="empty muted">Loading…</div>`;
  try {
    applicationState.stageDefinitions = await requestJsonFromApi("/api/stages");
    await refreshProjects();
    renderSidebar();
    renderMain();
  } catch (startupFailure) {
    console.error("startup failed", startupFailure);
    renderFatalStartupError(startupFailure);
  }
}

function renderFatalStartupError(startupFailure) {
  select("#sidebar").innerHTML = "";
  select("#main-inner").innerHTML = `
    <div class="empty">
      <h3>Could not start</h3>
      <p style="max-width:52ch;margin:0 auto 18px">${escapeHtml(startupFailure.message)}</p>
      <button class="btn btn-accent" id="retry-boot-button">Try again</button>
    </div>`;
  select("#retry-boot-button").onclick = boot;
}

async function refreshProjects() {
  applicationState.availableProjects = await requestJsonFromApi("/api/projects");
  const projectSelect = select("#project-select");
  const { availableProjects, selectedProject } = applicationState;

  projectSelect.innerHTML = availableProjects.length
    ? availableProjects.map(project =>
        `<option value="${escapeHtml(project.slug)}">${escapeHtml(project.name)}</option>`).join("")
    : `<option value="">No projects yet</option>`;

  const previouslySelectedSlug = selectedProject?.slug;

  if (availableProjects.length) {
    // Preserve the current selection across a refresh; fall back to the first
    // project only when the selected one is genuinely gone.
    applicationState.selectedProject =
      availableProjects.find(p => p.slug === previouslySelectedSlug) ?? availableProjects[0];
    projectSelect.value = applicationState.selectedProject.slug;
  } else {
    applicationState.selectedProject = null;
  }

  // A refresh that lands on a different project must not keep the old one's
  // documents -- the same corruption path as switching by hand.
  if (applicationState.selectedProject?.slug !== previouslySelectedSlug) {
    clearProjectScopedState();
  }
}

/** The single way to change stage. Stage views call this rather than reaching
 *  into the sidebar, so navigation stays one behaviour. */
function navigateToStage(stageKey) {
  applicationState.activeStageKey = stageKey;
  renderSidebar();
  renderMain();
}

/* ---- sidebar ------------------------------------------------------------ */

function renderSidebar() {
  const { stageDefinitions, activeStageKey } = applicationState;

  const navigationItems = stageDefinitions.map((stage, index) => {
    const state = stageStateFor(stage.key);
    const isActive = activeStageKey === stage.key;
    return `
      <button class="nav-item ${isActive ? "active" : ""}" data-stage="${stage.key}"
              ${isActive ? 'aria-current="page"' : ""}>
        <span class="nav-icon">${stageIcon(stage.key)}</span>
        <span class="nav-label">${escapeHtml(stage.title)}</span>
        <span class="nav-badge ${state.status === "ready" ? "done" : ""}">${index + 1}</span>
      </button>`;
  }).join("");

  select("#sidebar").innerHTML = navigationItems + `
    <div class="help-card">
      <h4>${icon(`<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>`, 15)}
        Need help?</h4>
      <p>Each stage is run by an agent whose instructions you can read and edit.</p>
    </div>`;

  document.querySelectorAll(".nav-item").forEach(item => {
    item.onclick = () => navigateToStage(item.dataset.stage);
  });
}

/* ---- main --------------------------------------------------------------- */

function renderMain() {
  const container = select("#main-inner");

  if (!applicationState.selectedProject) {
    container.innerHTML = `
      <div class="empty">
        <h3>No project yet</h3>
        <p>Everything starts with a project name.</p>
        <button class="btn btn-accent" id="create-first-project-button">Create a project</button>
      </div>`;
    select("#create-first-project-button").onclick = beginNewProject;
    return;
  }

  const stage = applicationState.stageDefinitions
    .find(s => s.key === applicationState.activeStageKey);
  const state = stageStateFor(stage.key);

  container.innerHTML = `
    ${renderBreadcrumb(state)}
    <div class="notice" id="stage-notice" hidden></div>
    <div id="stage-body"></div>`;

  // Stage views own their own rendering; the shell only routes. Adding a stage
  // view means one more line here and one more module.
  const stageRenderers = {
    inputs: () => renderInputsStage(stage),
    extraction: () => renderExtractionStage(stage, navigateToStage, renderAgentStage),
    planning: () => renderPlanningStage(stage, navigateToStage, renderAgentStage),
    scripting: () => renderScriptingStage(stage, navigateToStage, renderAgentStage),
    studio: () => renderStudioStage(stage, navigateToStage, renderAgentStage),
    reviewing: () => renderReviewingStage(stage, navigateToStage, renderAgentStage),
  };
  (stageRenderers[stage.key] ?? (() => renderAgentStage(stage)))();
}

function renderBreadcrumb(state) {
  return `
    <div class="breadcrumb">
      <span>Project</span><span>&rsaquo;</span>
      <span class="current">${escapeHtml(applicationState.selectedProject.name)}</span>
      <div class="spacer"></div>
      <span class="status-pill">
        <span class="dot ${state.status === "ready" ? "ready" : ""}"></span>
        ${escapeHtml(state.detail || state.status)}
      </span>
    </div>`;
}

/* ---- inputs stage ------------------------------------------------------- */

function renderInputsStage(stage) {
  const sources = sortedSources();

  select("#stage-body").innerHTML = `
    <div class="card">
      <div class="card-head">
        <span class="card-icon">${stageIcon("inputs", 21)}</span>
        <div>
          <h2>${escapeHtml(stage.title)}</h2>
          <p>Source documents for this project.</p>
        </div>
        <span class="card-note">PDF &middot; MD &middot; DOCX &middot; PPTX &middot; TXT</span>
      </div>

      <div class="dropzone" id="dropzone">
        <div class="cloud">${icon(
          `<path d="M16 16l-4-4-4 4M12 12v9"/>
           <path d="M20.4 14.5A5 5 0 0 0 18 5a7 7 0 0 0-13.3 2A4.5 4.5 0 0 0 5 16"/>`, 38, 1.5)}
        </div>
        <div class="lead">Drag and drop your files here</div>
        <div class="or">or</div>
        <button class="btn btn-accent" id="choose-files-button">
          ${icon(`<path d="M12 19V5M5 12l7-7 7 7"/>`)} Choose files
        </button>
        <input type="file" id="file-picker" multiple hidden
               accept=".pdf,.md,.txt,.docx,.pptx">
      </div>

      <div class="list-head">
        <h3>Uploaded files (${sources.length})</h3>
        <div class="sort">
          <label for="sort-select">Sort by</label>
          <select id="sort-select">
            <option value="name-asc">Name (A–Z)</option>
            <option value="name-desc">Name (Z–A)</option>
            <option value="size-desc">Size (largest)</option>
            <option value="type-asc">Type</option>
          </select>
        </div>
      </div>

      ${sources.length ? sources.map(file => `
        <div class="file-row">
          ${fileTypeBadge(file.suffix)}
          <span class="file-name" title="${escapeHtml(file.name)}">${escapeHtml(file.name)}</span>
          ${file.supported ? "" : `<span class="chip">unsupported</span>`}
          <span class="file-size">${formatFileSize(file.bytes)}</span>
          <span class="file-actions">
            <button class="btn-icon danger" data-delete="${escapeHtml(file.name)}"
                    aria-label="Delete ${escapeHtml(file.name)}" title="Delete">
              ${icon(`<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>`, 16, 1.8)}
            </button>
          </span>
        </div>`).join("")
        : `<div class="empty" style="padding:26px">
             <p class="muted" style="margin:0">No files yet — add one to begin.</p>
           </div>`}

      ${renderInputsFooter(stage, sources.length)}
    </div>`;

  wireInputsStage(stage);
}

function renderInputsFooter(stage, sourceCount) {
  const nextStage = applicationState.stageDefinitions[
    applicationState.stageDefinitions.findIndex(s => s.key === stage.key) + 1];
  if (!nextStage) return "";

  return `
    <div class="footer-nav">
      <div class="spacer"></div>
      <button class="btn btn-accent" data-goto="${nextStage.key}"
              ${sourceCount ? "" : "disabled"}
              title="${sourceCount ? "" : "Add at least one source file first"}">
        Next: ${escapeHtml(nextStage.title)} ${icon(ICON.arrowRight)}
      </button>
    </div>`;
}

function wireInputsStage(stage) {
  const dropzone = select("#dropzone");
  const filePicker = select("#file-picker");

  select("#choose-files-button").onclick = () => filePicker.click();
  filePicker.onchange = () => {
    uploadSourceFiles(stage, filePicker.files);
    filePicker.value = "";  // allow re-selecting the same file after a delete
  };

  dropzone.addEventListener("dragover", event => {
    event.preventDefault();
    dropzone.classList.add("over");
  });
  dropzone.addEventListener("dragleave", () => dropzone.classList.remove("over"));
  dropzone.addEventListener("drop", event => {
    event.preventDefault();
    dropzone.classList.remove("over");
    uploadSourceFiles(stage, event.dataTransfer.files);
  });

  select("#sort-select").value = applicationState.sourceSortOrder;
  select("#sort-select").onchange = event => {
    applicationState.sourceSortOrder = event.target.value;
    renderInputsStage(stage);
  };

  document.querySelectorAll("[data-delete]").forEach(button => {
    button.onclick = () => deleteSourceFile(stage, button.dataset.delete);
  });

  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });
}

async function uploadSourceFiles(stage, fileList) {
  if (!fileList?.length) return;
  if (applicationState.isUploadInFlight) {
    // Dropping a second batch mid-upload would race two responses to overwrite
    // `selectedProject`. Refusing silently would look like the drop missed.
    showStageNotice("warn", "An upload is already running — wait for it to finish.");
    return;
  }
  applicationState.isUploadInFlight = true;

  const dropzone = select("#dropzone");
  dropzone?.classList.add("busy");

  try {
    const formData = new FormData();
    [...fileList].forEach((file, index) => formData.append(`file${index}`, file));

    const uploadResult = await requestJsonFromApi(
      projectApiPath("/sources"), { method: "POST", body: formData });

    applicationState.selectedProject = uploadResult.project;
    // New files default into the selection on the next stage.
    applicationState.selectedSourceNames = null;
    renderSidebar();
    renderMain();
    reportUploadOutcome(uploadResult);
  } catch (uploadFailure) {
    console.error("upload failed", uploadFailure);
    showStageNotice("bad", `Upload failed — ${uploadFailure.message}`);
  } finally {
    applicationState.isUploadInFlight = false;
    dropzone?.classList.remove("busy");
  }
}

function reportUploadOutcome({ accepted = [], rejected = [] }) {
  // Partial success is a real outcome. Reporting "3 added" while silently
  // dropping a fourth file is the kind of quiet lie that erodes trust.
  const renamedFiles = accepted.filter(file => file.was_renamed);
  const messageParts = [];

  if (accepted.length) messageParts.push(`${accepted.length} added`);
  if (renamedFiles.length) messageParts.push(`${renamedFiles.length} renamed to a safe filename`);
  if (rejected.length) {
    const details = rejected.map(file => `${file.file_name} — ${file.reason}`).join("; ");
    messageParts.push(`${rejected.length} rejected (${details})`);
  }
  if (!messageParts.length) return;

  showStageNotice(rejected.length ? "warn" : "ok", messageParts.join(" · "));
}

async function deleteSourceFile(stage, fileName) {
  if (applicationState.isDeleteInFlight) {
    showStageNotice("warn", "Still removing the last file — try again in a moment.");
    return;
  }
  applicationState.isDeleteInFlight = true;
  try {
    const deleteResult = await requestJsonFromApi(
      projectApiPath(`/sources/${encodeURIComponent(fileName)}`), { method: "DELETE" });

    applicationState.selectedProject = deleteResult.project;
    // A deleted file must not linger in the extraction selection or preview.
    applicationState.selectedSourceNames?.delete(fileName);
    if (applicationState.previewFileName === fileName) {
      applicationState.previewFileName = null;
    }
    renderSidebar();
    renderMain();
    showStageNotice("ok", `Removed ${fileName}.`);
  } catch (deleteFailure) {
    console.error("delete failed", deleteFailure);
    showStageNotice("bad", `Could not remove ${fileName} — ${deleteFailure.message}`);
  } finally {
    applicationState.isDeleteInFlight = false;
  }
}

/* ---- agent stages ------------------------------------------------------- */

async function renderAgentStage(stage) {
  const body = select("#stage-body");

  if (!stage.has_agent) {
    body.innerHTML = `<div class="card muted">No agent — file handling only.</div>`;
    return;
  }

  body.innerHTML = `<div class="card muted">Loading agent…</div>`;

  let agent;
  try {
    agent = await requestJsonFromApi(projectApiPath(`/agent/${stage.key}`));
  } catch (loadFailure) {
    console.error("agent load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load this agent.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }

  body.innerHTML = `
    <div class="card">
      <div class="card-head">
        <span class="card-icon">${stageIcon(stage.key, 21)}</span>
        <div>
          <h2>${escapeHtml(stage.title)}</h2>
          <p>${escapeHtml(agent.role)}</p>
        </div>
        <span class="card-note">${escapeHtml(stage.produces)}</span>
      </div>

      <h3 class="section">Tools it can operate — ${agent.tools.length}</h3>
      <div class="tool-grid">${agent.tools.map(tool => `
        <div class="tool">
          <b>${escapeHtml(tool.name)}</b><span class="kind">${escapeHtml(tool.kind)}</span>
          <p>${escapeHtml(tool.summary)}</p>
        </div>`).join("")}</div>

      ${agent.unknown_tools.length ? `
        <div class="notice bad" style="margin-top:12px">
          Unknown tools declared: ${agent.unknown_tools.map(escapeHtml).join(", ")} —
          not in the catalogue, likely a typo.
        </div>` : ""}

      ${agent.resources.length ? `
        <h3 class="section">External resources</h3>
        <div class="tool-grid">${agent.resources.map(resource => `
          <div class="tool">
            <b>${escapeHtml(resource.name)}</b><span class="kind">${escapeHtml(resource.kind)}</span>
            <p>${escapeHtml(resource.summary)}<br>licence: ${escapeHtml(resource.licence)}${
              resource.requires_key ? " &middot; needs API key" : ""}</p>
          </div>`).join("")}</div>` : ""}

      <h3 class="section">AGENT.md</h3>
      <div class="agent-bar">
        <span class="chip ${agent.source === "project" ? "accent" : ""}">${escapeHtml(agent.source)}</span>
        <span class="mono muted">${escapeHtml(agent.path)}</span>
        <div class="spacer"></div>
        <button class="btn btn-accent" id="save-agent-button">Save to project</button>
      </div>
      ${agent.invalidates.length ? `
        <p class="muted" style="font-size:12.5px;margin:0 0 9px">
          Editing invalidates: ${agent.invalidates.map(s =>
            `<span class="chip">${escapeHtml(s)}</span>`).join(" ")}
        </p>` : ""}
      <textarea class="agent-body" id="agent-body" spellcheck="false">${escapeHtml(agent.body)}</textarea>

      <p class="muted" style="font-size:12.5px;margin:12px 0 0">
        This text is the agent's system prompt. Planning and Scripting run it
        against a model today; the other stages read it but do not call one yet.
      </p>
    </div>`;

  wireAgentSave(stage);
}

function wireAgentSave(stage) {
  const saveButton = select("#save-agent-button");
  saveButton.onclick = async () => {
    // Disabled for the duration: a second click would issue a concurrent write
    // to the same AGENT.md, where last-writer-wins is arbitrary.
    saveButton.disabled = true;
    const idleLabel = saveButton.textContent;
    saveButton.textContent = "Saving…";
    try {
      await requestJsonFromApi(projectApiPath(`/agent/${stage.key}`), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ body: select("#agent-body").value }),
      });
      await renderAgentStage(stage);
      showStageNotice("ok", `${stage.title} agent saved to this project.`);
    } catch (saveFailure) {
      console.error("agent save failed", saveFailure);
      // The edit is still in the textarea; say so, because losing a long edit to
      // a transient failure is the worst outcome here.
      saveButton.disabled = false;
      saveButton.textContent = idleLabel;
      showStageNotice("bad",
        `Could not save — ${saveFailure.message}. Your edit is still here; try again.`);
    }
  };
}

/* ---- project creation --------------------------------------------------- */

function beginNewProject() {
  // An inline form rather than window.prompt(): prompt() is unstyleable, blocks
  // the page, and leaves nowhere to explain why a name was refused.
  select("#main-inner").innerHTML = `
    <div class="empty">
      <h3>Name the project</h3>
      <div class="name-form">
        <input id="new-project-name" placeholder="e.g. Demystifying the Brain"
               autocomplete="off" maxlength="120" aria-label="Project name">
        <button class="btn btn-accent" id="confirm-new-project-button">Create</button>
        <button class="btn" id="cancel-new-project-button">Cancel</button>
      </div>
      <div class="notice bad" id="new-project-error" hidden></div>
    </div>`;

  const nameInput = select("#new-project-name");
  const confirmButton = select("#confirm-new-project-button");
  nameInput.focus();

  const cancel = () => { renderSidebar(); renderMain(); };
  select("#cancel-new-project-button").onclick = cancel;
  nameInput.addEventListener("keydown", event => {
    if (event.key === "Enter") confirmButton.click();
    if (event.key === "Escape") cancel();
  });

  confirmButton.onclick = async () => {
    const projectName = nameInput.value.trim();
    if (!projectName) {
      showNoticeIn(select("#new-project-error"), "bad", "A project needs a name.");
      nameInput.focus();
      return;
    }
    confirmButton.disabled = true;
    confirmButton.textContent = "Creating…";
    try {
      applicationState.selectedProject = await requestJsonFromApi("/api/projects", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: projectName }),
      });
      await refreshProjects();
      select("#project-select").value = applicationState.selectedProject.slug;
      navigateToStage("inputs");
    } catch (createFailure) {
      console.error("project create failed", createFailure);
      confirmButton.disabled = false;
      confirmButton.textContent = "Create";
      showNoticeIn(select("#new-project-error"), "bad", createFailure.message);
      nameInput.focus();
    }
  };
}

/* ---- chrome ------------------------------------------------------------- */

select("#new-project-button").onclick = beginNewProject;

select("#project-select").onchange = event => {
  const chosenProject = applicationState.availableProjects
    .find(project => project.slug === event.target.value) ?? null;
  if (chosenProject?.slug === applicationState.selectedProject?.slug) return;

  applicationState.selectedProject = chosenProject;
  // Everything loaded for the previous project is now wrong, and leaving it in
  // place would let a save write one project's document into another.
  clearProjectScopedState();
  renderSidebar();
  renderMain();
};

const drawer = select("#drawer");
select("#toggle-drawer-button").onclick = () => drawer.classList.toggle("open");
select("#close-drawer-button").onclick = () => drawer.classList.remove("open");

// Both panels slide in from the same edge, so opening one closes the other
// rather than stacking them on top of each other.
select("#open-credentials-button").onclick = () => {
  drawer.classList.remove("open");
  openCredentialsPanel();
};
select("#close-credentials-button").onclick = closeCredentialsPanel;

select("#drawer-send-button").onclick = () => {
  const input = select("#drawer-input");
  const messageText = input.value.trim();
  if (!messageText) return;

  const log = select("#drawer-log");
  log.insertAdjacentHTML("beforeend", `<div class="msg mine">${escapeHtml(messageText)}</div>`);
  log.insertAdjacentHTML("beforeend", `<div class="msg muted">
    No model wired up yet — this is the surface only. Context would be:
    <b>${escapeHtml(applicationState.selectedProject?.name ?? "no project")}</b> /
    <b>${escapeHtml(applicationState.activeStageKey)}</b>.</div>`);
  input.value = "";
  log.scrollTop = log.scrollHeight;
};

select("#drawer-input").addEventListener("keydown", event => {
  if (event.key === "Enter") select("#drawer-send-button").click();
});

document.addEventListener("keydown", event => {
  if (event.key !== "Escape") return;
  if (isCredentialsPanelOpen()) closeCredentialsPanel();
  else if (drawer.classList.contains("open")) drawer.classList.remove("open");
});

boot();
