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
import {
  openRawFile, releaseRawFile, renderRawFileShell,
} from "/static/raw-file-viewer.js";
import {
  renderModelMarkdown, requestJsonFromApi, showNoticeIn, uploadJsonToApi,
} from "/static/shared-client.js";
import { paintProjectPicker, startProjectPicker } from "/static/project-picker.js";
import {
  paintRenderNavBadge, renderRenderPage, startRenderDock,
} from "/static/render-dock.js";
import { renderAssetsStage } from "/static/stage-assets.js";
import { renderExportStage } from "/static/stage-export.js";
import { renderExtractionStage } from "/static/stage-extraction.js";
import { renderGenerationStage } from "/static/stage-generation.js";
import { renderScenePlanStage } from "/static/stage-scene-plan.js";
import { renderScriptStagingStage } from "/static/stage-script-staging.js";
import { renderReviewingStage } from "/static/stage-reviewing.js";
import { renderStudioStage } from "/static/stage-studio.js";
import {
  applicationState, clearProjectScopedState, escapeHtml, fileTypeBadge, footerNav,
  formatFileSize, icon, onProjectSummaryRefreshed, onUpstreamAction, paintUpstreamFlags,
  projectApiPath, refreshProjectSummary, refreshUpstream, select,
  showStageNotice, stageHeader, stageIcon, stageStateFor, whenItWas,
  wireGotoButtons,
} from "/static/ui-kit.js";

/* ---- boot --------------------------------------------------------------- */

/** Render is a page of its own, not a pipeline stage: it has a tab in the
 *  sidebar before Studio -- a render writes the timeline Studio shows -- but
 *  no step number and nothing to hand on. */
const RENDER_PAGE = { key: "render", title: "Render" };

function isKnownPage(key) {
  return key === RENDER_PAGE.key
    || applicationState.stageDefinitions.some(stage => stage.key === key);
}

async function boot() {
  select("#main-inner").innerHTML = `<div class="empty muted">Loading…</div>`;
  try {
    applicationState.stageDefinitions = await requestJsonFromApi("/api/stages");
    await refreshProjects();

    // A stage named in the path opens; anything unrecognised falls back to the
    // first stage, and the address is corrected by replacement so the back
    // button is not filled with a place nobody chose.
    const { stageKey } = readAddress();
    const known = isKnownPage(stageKey);
    applicationState.activeStageKey =
      known ? stageKey : applicationState.stageDefinitions[0]?.key;
    writeAddress({ replace: true });

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

const LAST_PROJECT_STORAGE_KEY = "explainer-pipeline:last-project";

/* ---- addresses ----------------------------------------------------------
 *
 * A stage is a place, so it has an address: `/scene-plan/<project>`. The path is
 * the truth on load and is kept in step on every change, which is what makes a
 * reload land where you were and a pasted link open what the sender was looking
 * at.
 */

/** What the current path is asking for. Empty fields mean "no preference". */
function readAddress() {
  const [stageKey = "", projectSlug = ""] = window.location.pathname
    .split("/").filter(Boolean).map(decodeURIComponent);
  return { stageKey, projectSlug };
}

/** Put the address in the bar without reloading.
 *
 *  `replace` is for corrections -- landing on a default, or a stage that does
 *  not exist -- so the back button is not filled with places nobody chose.
 */
function writeAddress({ replace = false } = {}) {
  const { selectedProject, activeStageKey } = applicationState;
  if (!selectedProject || !activeStageKey) return;

  const path = `/${encodeURIComponent(activeStageKey)}`
    + `/${encodeURIComponent(selectedProject.slug)}`;
  if (window.location.pathname === path) return;

  const title = `${selectedProject.name} · ${activeStageKey}`;
  if (replace) window.history.replaceState({}, title, path);
  else window.history.pushState({}, title, path);
}

function rememberSelectedProject(slug) {
  try { localStorage.setItem(LAST_PROJECT_STORAGE_KEY, slug); }
  catch { /* storage unavailable: the choice just won't survive a reload */ }
}

function recallSelectedProject() {
  try { return localStorage.getItem(LAST_PROJECT_STORAGE_KEY); }
  catch { return null; }
}

/** Which project to open when nothing is selected yet.
 *
 *  Not simply the first alphabetically: after a reload that would always land
 *  on the same old project, whatever was being worked on.
 *  Now: the one they last had open, else the newest.
 */
function chooseProjectToOpen(availableProjects) {
  const remembered = availableProjects.find(p => p.slug === recallSelectedProject());
  if (remembered) return remembered;
  return [...availableProjects].sort(
    (a, b) => String(b.created ?? "").localeCompare(String(a.created ?? "")))[0];
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
    // The address wins on a fresh load: someone who pasted a link asked for that
    // project, whatever this browser had open last.
    const addressed = availableProjects.find(p => p.slug === readAddress().projectSlug);
    applicationState.selectedProject =
      addressed
      ?? availableProjects.find(p => p.slug === previouslySelectedSlug)
      ?? chooseProjectToOpen(availableProjects);
    projectSelect.value = applicationState.selectedProject.slug;
    rememberSelectedProject(applicationState.selectedProject.slug);
  } else {
    applicationState.selectedProject = null;
  }

  // A refresh that lands on a different project must not keep the old one's
  // documents -- the same corruption path as switching by hand.
  if (applicationState.selectedProject?.slug !== previouslySelectedSlug) {
    clearProjectScopedState();
    resetConversationPanel();
  }
}

/** Redraw the chrome when a stage changes what the project's status says.
 *  Only the chrome: the stage view owns its own body and redraws itself. */
onProjectSummaryRefreshed(() => renderSidebar());

/** The single way to change stage. Stage views call this rather than reaching
 *  into the sidebar, so navigation stays one behaviour. */
function navigateToStage(stageKey, { replaceAddress = false } = {}) {
  applicationState.activeStageKey = stageKey;
  writeAddress({ replace: replaceAddress });
  renderSidebar();
  renderMain();
}

/**
 * What the banner's two buttons do, per layer. Redo is the rule-based part
 * where there is one (gather again; re-sync a deck plan, keeping its edits) and
 * otherwise the tab where the work is redone. Either way the layer is then
 * transferred again, which is what clears its flag.
 */
const UPSTREAM_TABS = {
  assets: ["assetsTab", "extracted"],
  "scene-plan": ["planTab", "direction"],
  "script-staging": ["scriptTab", "write"],
  generation: ["generationTab", "make"],
};

onUpstreamAction(async (layer, action) => {
  let notice = null;
  if (action === "redo") {
    try {
      if (layer === "assets") {
        await requestJsonFromApi(projectApiPath("/assets/refresh"), { method: "POST" });
        notice = ["ok", "Gathered again from the new extraction. Your Use and Skip are kept."];
      }
      if (layer === "scene-plan") {
        notice = ["ok", "Tell the planning agent what changed in the source; it proposes a "
          + "revised shape, and sections that did not change keep their scenes."];
      }
    } catch (failure) {
      notice = ["warn", `${failure.message} Redo this layer by hand, then transfer.`];
    }
  }
  const [tabKey, redoTab] = UPSTREAM_TABS[layer] ?? [];
  if (tabKey) applicationState[tabKey] = action === "redo" ? redoTab : "final";
  navigateToStage(layer === "render" ? RENDER_PAGE.key : layer);
  await refreshProjectSummary();
  if (notice) showStageNotice(...notice);
});

/* ---- sidebar ------------------------------------------------------------ */

function renderSidebar() {
  const { stageDefinitions, activeStageKey } = applicationState;

  const navigationItems = stageDefinitions.map((stage, index) => {
    const state = stageStateFor(stage.key);
    const isActive = activeStageKey === stage.key;
    return `${stage.key === "studio" ? renderTab() : ""}
      <button class="nav-item ${isActive ? "active" : ""}" data-stage="${stage.key}"
              ${isActive ? 'aria-current="page"' : ""}>
        <span class="nav-icon">${stageIcon(stage.key)}</span>
        <span class="nav-label">${escapeHtml(stage.title)}</span>
        <span class="nav-badge ${state.status === "ready" ? "done" : ""}">${index + 1}</span>
      </button>`;
  }).join("");

  select("#sidebar").innerHTML = navigationItems;
  paintRenderNavBadge();
  paintUpstreamFlags();

  document.querySelectorAll(".nav-item").forEach(item => {
    item.onclick = () => navigateToStage(item.dataset.stage);
  });
}

function renderTab() {
  const isActive = applicationState.activeStageKey === RENDER_PAGE.key;
  return `
      <button class="nav-item nav-page ${isActive ? "active" : ""}" data-stage="${RENDER_PAGE.key}"
              ${isActive ? 'aria-current="page"' : ""}>
        <span class="nav-icon">${stageIcon(RENDER_PAGE.key)}</span>
        <span class="nav-label">${RENDER_PAGE.title}</span>
        <span class="nav-badge render-badge" id="render-nav-badge" hidden></span>
      </button>`;
}

/* ---- main --------------------------------------------------------------- */

function renderMain() {
  paintProjectPicker();
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

  const stage = applicationState.activeStageKey === RENDER_PAGE.key ? RENDER_PAGE
    : applicationState.stageDefinitions.find(s => s.key === applicationState.activeStageKey);

  container.innerHTML = `
    <div class="notice" id="stage-notice" role="status" aria-live="polite"
         title="Click to dismiss" hidden></div>
    <div id="stage-body" data-stage="${stage.key}"></div>`;

  // Every page render asks what changed upstream: the flags are painted when the
  // answer arrives, and a stage that draws later reads them from the state.
  refreshUpstream();

  // Stage views own their own rendering; the shell only routes. Adding a stage
  // view means one more line here and one more module.
  const stageRenderers = {
    inputs: () => renderInputsStage(stage),
    extraction: () => renderExtractionStage(stage, navigateToStage, renderAgentStage),
    assets: () => renderAssetsStage(stage, navigateToStage, renderAgentStage),
    "scene-plan": () => renderScenePlanStage(stage, navigateToStage, renderAgentStage),
    "script-staging": () => renderScriptStagingStage(stage, navigateToStage, renderAgentStage),
    generation: () => renderGenerationStage(stage, navigateToStage, renderAgentStage),
    studio: () => renderStudioStage(stage, navigateToStage, renderAgentStage),
    reviewing: () => renderReviewingStage(stage, navigateToStage, renderAgentStage),
    export: () => renderExportStage(stage, navigateToStage, renderAgentStage),
    render: () => renderRenderPage(stage),
  };
  (stageRenderers[stage.key] ?? (() => renderAgentStage(stage)))();
}

/* ---- inputs stage ------------------------------------------------------- */

/**
 * A project is made from one source file, and that file runs through every
 * layer. So this page is one drop zone until there is a file, and one card once
 * there is: preview it, replace it, or remove it. Replacing asks first, and says
 * what happens to the work after it.
 */
const SOURCE_TYPES = ".pdf,.md,.txt,.docx,.pptx";

function renderInputsStage(stage) {
  const source = applicationState.selectedProject?.source ?? null;

  select("#stage-body").innerHTML = `
    ${stageHeader("inputs", stage.title, {
      actions: `
        <span class="supported-types" title="Supported source documents">
          ${["pdf", "md", "docx", "pptx", "txt"].map(fileTypeBadge).join("")}
        </span>`,
    })}

    <div class="card stage-content">
      ${source ? `
        <div class="source-card" id="source-card">
          <div class="source-card-row">
            ${fileTypeBadge(source.suffix)}
            <div class="source-card-name">
              <b title="${escapeHtml(source.name)}">${escapeHtml(source.name)}</b>
              <span>${escapeHtml([source.kind, source.measure, formatFileSize(source.bytes)]
                .filter(Boolean).join(" · "))}</span>
            </div>
            <button class="btn" data-preview="${escapeHtml(source.name)}" aria-expanded="false">
              ${icon(`<path d="M6 9l6 6 6-6"/>`, 15, 2.2)} Preview</button>
            <button class="btn" id="replace-source-button">Replace</button>
            <button class="btn-icon danger" id="remove-source-button"
                    title="Remove the source" aria-label="Remove ${escapeHtml(source.name)}">
              ${icon(`<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>`, 16, 1.8)}
            </button>
          </div>
          <div class="file-preview" data-preview-for="${escapeHtml(source.name)}" hidden></div>
          <p class="source-card-note">This file runs through every layer. To use another,
            replace it (or drop the new file here): the work after Extraction is kept and
            marked out of date until it is redone.</p>
        </div>`
        : `
        <div class="dropzone" id="dropzone">
          <div class="cloud">${icon(
            `<path d="M16 16l-4-4-4 4M12 12v9"/>
             <path d="M20.4 14.5A5 5 0 0 0 18 5a7 7 0 0 0-13.3 2A4.5 4.5 0 0 0 5 16"/>`, 38, 1.5)}
          </div>
          <div class="lead">Drop your source file here</div>
          <div class="or">A deck, PDF, Word, Markdown or text file. One file: it runs through
            every layer.</div>
          <button class="btn btn-accent" id="choose-files-button">
            ${icon(`<path d="M12 19V5M5 12l7-7 7 7"/>`)} Choose a file
          </button>
        </div>`}
      <input type="file" id="file-picker" hidden accept="${SOURCE_TYPES}">

      ${renderInputsFooter(stage, source)}
    </div>`;

  wireInputsStage(stage, source);
}

function renderInputsFooter(stage, source) {
  return footerNav(stage, {
    next: {
      disabled: !source,
      disabledReason: "Add the source file first",
      carries: source ? `${source.name} goes on to be extracted.` : "",
    },
  });
}

function wireInputsStage(stage, source) {
  const filePicker = select("#file-picker");
  filePicker.onchange = () => {
    useSourceFile(stage, filePicker.files);
    filePicker.value = "";  // allow choosing the same file again
  };
  const choose = select("#choose-files-button");
  if (choose) choose.onclick = () => filePicker.click();
  const replace = select("#replace-source-button");
  if (replace) replace.onclick = () => filePicker.click();
  const remove = select("#remove-source-button");
  if (remove) remove.onclick = () => deleteSourceFile(stage, source.name);

  // The drop zone takes a first file; the card takes a replacement.
  const target = select("#dropzone") ?? select("#source-card");
  target.addEventListener("dragover", event => {
    event.preventDefault();
    target.classList.add("over");
  });
  target.addEventListener("dragleave", () => target.classList.remove("over"));
  target.addEventListener("drop", event => {
    event.preventDefault();
    target.classList.remove("over");
    useSourceFile(stage, event.dataTransfer.files);
  });

  document.querySelectorAll("[data-preview]").forEach(button => {
    button.onclick = () => toggleSourcePreview(button);
  });
  wireGotoButtons(navigateToStage);
}

/** Use this file as the project's source: the first one, or a replacement. */
async function useSourceFile(stage, fileList) {
  if (!fileList?.length) return;
  if (fileList.length > 1) {
    showStageNotice("warn", `A project has one source file. ${fileList.length} were dropped; `
      + "drop just the one this video is made from.");
    return;
  }
  if (applicationState.isUploadInFlight) {
    showStageNotice("warn", "An upload is already running — wait for it to finish.");
    return;
  }
  const file = fileList[0];
  const current = applicationState.selectedProject?.source;
  if (current && !window.confirm(`Replace ${current.name} with ${file.name}?\n\n`
      + "Extract the new file next. Every layer after Extraction keeps its work and is "
      + "marked out of date until it is redone, or transferred as it stands.")) return;

  applicationState.isUploadInFlight = true;
  const host = select("#dropzone") ?? select("#source-card");
  const lead = host?.querySelector(".lead, .source-card-name span");
  const leadText = lead?.textContent;
  host?.classList.add("busy");
  try {
    const formData = new FormData();
    formData.append("file", file);
    // A large deck takes minutes to send: say how far it has got. Past 100% the
    // server is still checking and saving.
    const result = await uploadJsonToApi(
      projectApiPath(`/sources${current ? "?replace=true" : ""}`), formData, fraction => {
        if (lead) lead.textContent = fraction < 1 ? `Uploading… ${Math.floor(fraction * 100)}%` : "Saving…";
      });
    applicationState.selectedProject = result.project;
    applicationState.previewFileName = null;
    renderSidebar();
    renderMain();
    showStageNotice(result.replaced ? "warn" : "ok", result.replaced
      ? `${result.accepted.file_name} replaced ${result.replaced}. Extract it next; the layers `
        + "after Extraction are marked out of date."
      : `${result.accepted.file_name} is the source. Extract it next.`
        + (result.accepted.was_renamed ? " (Its name was made safe for a file name.)" : ""));
  } catch (uploadFailure) {
    console.error("upload failed", uploadFailure);
    showStageNotice("bad", uploadFailure.message);
  } finally {
    applicationState.isUploadInFlight = false;
    host?.classList.remove("busy");
    if (lead && lead.isConnected) lead.textContent = leadText;
  }
}

async function deleteSourceFile(stage, fileName) {
  if (!window.confirm(`Remove ${fileName}?\n\nThe project has no source until you add one. `
      + "What was extracted and transferred stays where it is.")) return;
  if (applicationState.isDeleteInFlight) {
    showStageNotice("warn", "Still removing the last file — try again in a moment.");
    return;
  }
  applicationState.isDeleteInFlight = true;
  try {
    const deleteResult = await requestJsonFromApi(
      projectApiPath(`/sources/${encodeURIComponent(fileName)}`), { method: "DELETE" });
    applicationState.selectedProject = deleteResult.project;
    applicationState.previewFileName = null;
    renderSidebar();
    renderMain();
    showStageNotice("ok", `Removed ${fileName}. Add the source file to go on.`);
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
    ${stageHeader(stage.key, stage.title, {
      actions: `<span class="card-note">${escapeHtml(stage.produces)}</span>`,
      infoSummary: agent.role,
    })}

    <div class="card stage-content">

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
        This text is the agent's system prompt. Scene Plan and Script & Staging run it
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
  if (chosenProject) rememberSelectedProject(chosenProject.slug);
  writeAddress();
  // Everything loaded for the previous project is now wrong, and leaving it in
  // place would let a save write one project's document into another. The
  // Orchestrator's thread goes with it: it is about the other project's work.
  clearProjectScopedState();
  resetConversationPanel();
  renderSidebar();
  renderMain();
};

const drawer = select("#drawer");
select("#toggle-drawer-button").onclick = () => {
  const opening = !drawer.classList.contains("open");
  drawer.classList.toggle("open");
  // The thread is in `applicationState`, so it survives the panel closing; what
  // may have changed while it was shut is the list of threads.
  if (opening) refreshConversationList();
};
select("#close-drawer-button").onclick = () => drawer.classList.remove("open");

// Both panels slide in from the same edge, so opening one closes the other
// rather than stacking them on top of each other.
select("#open-credentials-button").onclick = () => {
  drawer.classList.remove("open");
  openCredentialsPanel();
};
select("#close-credentials-button").onclick = closeCredentialsPanel;

startRenderDock({
  // Watch on the Render tab: that project's Studio, playing the rendered file.
  watch: (slug, file, label) => {
    if (slug !== applicationState.selectedProject?.slug) {
      const chooser = select("#project-select");
      chooser.value = slug;
      chooser.dispatchEvent(new Event("change"));
    }
    applicationState.studioWatch = { slug, file, label };
    navigateToStage("studio");
  },
});
startProjectPicker({
  // The deleted project may have been the open one: the list is re-read, and
  // it chooses another and clears what was loaded for the old one.
  onDeleted: async () => {
    await refreshProjects();
    writeAddress();
    renderSidebar();
    renderMain();
  },
});

/** Ask the orchestrator — the master agent, not the stage you happen to be on.
 *
 *  A person asking a question should not have to know which stage owns the
 *  answer, or navigate to it first, so the question goes to the master agent.
 *
 *  The orchestrator sits above every stage. It decides which stage agents to
 *  put to work, runs several of them at once, and answers from what they send
 *  back. The reply lists everyone it consulted, so an answer can be checked
 *  against the agents that produced it.
 */
async function askTheAgent() {
  const input = select("#drawer-input");
  const question = input.value.trim();
  if (!question) return;

  const log = select("#drawer-log");
  const project = applicationState.selectedProject;

  if (!project) {
    log.insertAdjacentHTML("beforeend",
      `<div class="msg muted">Open a project first — the agent answers about one.</div>`);
    return;
  }

  select("#drawer-intro")?.remove();
  hideConversationList();

  log.insertAdjacentHTML("beforeend", `<div class="msg mine">${escapeHtml(question)}</div>`);
  input.value = "";

  // It may run several agents in sequence, so it says what it is doing rather
  // than leaving a still spinner for a minute.
  const working = document.createElement("div");
  working.className = "msg muted";
  working.innerHTML = `<span class="working-dot"></span>Orchestrator is deciding
    which agents to put to work…`;
  log.appendChild(working);
  log.scrollTop = log.scrollHeight;

  const sendButton = select("#drawer-send-button");
  sendButton.disabled = true;

  try {
    const reply = await requestJsonFromApi(projectApiPath("/orchestrator/ask"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      // The thread this question belongs to, so the agent is told what was
      // already said. Empty means "start a new one", and the reply says which.
      body: JSON.stringify({
        question, conversation_id: applicationState.agentConversationId ?? "",
      }),
    });
    working.remove();
    applicationState.agentConversationId = reply.conversation_id;
    log.insertAdjacentHTML("beforeend", renderOrchestratorReply(reply));
    wireConsultedAgents(log);
    refreshConversationList();
  } catch (askFailure) {
    console.error("orchestrator ask failed", askFailure);
    working.remove();
    log.insertAdjacentHTML("beforeend", `<div class="msg bad">
      ${escapeHtml(askFailure.message)}</div>`);
  } finally {
    sendButton.disabled = false;
    log.scrollTop = log.scrollHeight;
  }
}

/** The answer, plus who was actually asked to produce it.
 *
 *  Showing the consultations is not decoration. An orchestrator that summarises
 *  five agents is a layer between you and the thing that knows, and without the
 *  originals there is no way to tell a real finding from a confident paraphrase.
 */
function renderOrchestratorReply(reply) {
  const consulted = reply.consulted ?? [];
  const readNames = reply.artifacts_read ?? [];

  const worked = consulted.length
    ? `<div class="consulted">
         ${consulted.map(one => `
           <button class="agent-chip${one.ok ? "" : " failed"}"
                   data-consulted="${escapeHtml(one.stage)}"
                   title="What the ${escapeHtml(one.agent)} agent said">
             ${escapeHtml(one.agent)}
           </button>`).join("")}
         ${readNames.map(name =>
           `<span class="artifact-chip">${escapeHtml(name)}.json</span>`).join("")}
       </div>`
    : "";

  const transcripts = consulted.map(one => `
    <div class="consulted-answer" data-answer-for="${escapeHtml(one.stage)}" hidden>
      <span class="msg-who">${escapeHtml(one.agent)} was asked</span>
      <p class="consulted-question">${escapeHtml(one.question)}</p>
      <div class="answer-body">${renderModelMarkdown(one.answer)}</div>
    </div>`).join("");

  return `
    <div class="msg">
      <span class="msg-who">${escapeHtml(reply.agent)} ·
        ${escapeHtml(reply.agent_source)} instructions${
          consulted.length ? ` · ${consulted.length} agent${consulted.length === 1 ? "" : "s"} consulted` : ""
        }</span>
      <div class="answer-body">${renderModelMarkdown(reply.answer)}</div>
      ${worked}
      ${transcripts}
    </div>`;
}

/** Each consulted agent's own words, on demand. */
function wireConsultedAgents(log) {
  log.querySelectorAll("[data-consulted]").forEach(chip => {
    if (chip.dataset.wired) return;
    chip.dataset.wired = "true";
    chip.onclick = () => {
      const panel = chip.closest(".msg")
        .querySelector(`[data-answer-for="${CSS.escape(chip.dataset.consulted)}"]`);
      if (!panel) return;
      panel.hidden = !panel.hidden;
      chip.classList.toggle("open", !panel.hidden);
    };
  });
}

/* ---- conversations with the Orchestrator -------------------------------- */

/**
 * The panel keeps threads, rather than one exchange that dies with the drawer.
 *
 * Closing the panel keeps the conversation: it is written down, and the agent is
 * told what was already said.
 */
const INTRO_MESSAGE = `
  <div class="msg muted" id="drawer-intro">
    This is the <b>Orchestrator</b> — the master agent, above every stage.
    Ask it anything about this project from any tab; it works out which stage
    agents can answer, puts several of them to work at once, and replies from
    what they send back.
    <br><br>Every reply lists the agents it consulted, and you can open any of
    them to read what that agent actually said. It never writes to the project.
  </div>`;

/** Timestamps are stored in UTC; a list that says 08:27 for something you asked
 *  at 13:57 reads as the wrong conversation. */
function resetConversationPanel() {
  applicationState.agentConversationId = null;
  select("#drawer-log").innerHTML = INTRO_MESSAGE;
  hideConversationList();
}

function startNewConversation() {
  resetConversationPanel();
  select("#drawer-input").focus();
}

function hideConversationList() {
  select("#conversation-list").hidden = true;
  select("#conversation-history-button").setAttribute("aria-expanded", "false");
}

async function refreshConversationList() {
  if (!applicationState.selectedProject) return;
  try {
    const listed = await requestJsonFromApi(projectApiPath("/conversations"));
    applicationState.agentConversations = listed.conversations;
  } catch (listFailure) {
    console.warn("could not list conversations", listFailure);
    return;
  }
  if (!select("#conversation-list").hidden) renderConversationList();
}

function renderConversationList() {
  const list = select("#conversation-list");
  const conversations = applicationState.agentConversations ?? [];

  list.innerHTML = conversations.length
    ? conversations.map(conversation => `
        <div class="conversation-row ${
          conversation.id === applicationState.agentConversationId ? "active" : ""}">
          <button class="conversation-open" data-conversation="${escapeHtml(conversation.id)}">
            <span class="conversation-title">${escapeHtml(conversation.title)}</span>
            <span class="conversation-meta">${conversation.turn_count} message${
              conversation.turn_count === 1 ? "" : "s"} · ${
              escapeHtml(whenItWas(conversation.updated_at))}</span>
          </button>
          <button class="btn-icon danger" data-forget-conversation="${escapeHtml(conversation.id)}"
                  title="Delete this conversation" aria-label="Delete this conversation">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
          </button>
        </div>`).join("")
    : `<p class="muted conversation-empty">No earlier conversations for this project.</p>`;

  list.querySelectorAll("[data-conversation]").forEach(button => {
    button.onclick = () => openConversation(button.dataset.conversation);
  });
  list.querySelectorAll("[data-forget-conversation]").forEach(button => {
    button.onclick = async () => {
      if (!window.confirm("Delete this conversation? The project itself is untouched.")) return;
      const conversationId = button.dataset.forgetConversation;
      try {
        const left = await requestJsonFromApi(
          projectApiPath(`/conversations/${encodeURIComponent(conversationId)}`),
          { method: "DELETE" });
        applicationState.agentConversations = left.conversations;
      } catch (forgetFailure) {
        console.error("could not delete the conversation", forgetFailure);
        return;
      }
      if (applicationState.agentConversationId === conversationId) startNewConversation();
      renderConversationList();
    };
  });
}

/** Reopen a thread and show it as it was, so it can be continued. */
async function openConversation(conversationId) {
  const log = select("#drawer-log");
  log.innerHTML = `<div class="msg muted">Opening…</div>`;
  hideConversationList();

  let conversation;
  try {
    conversation = await requestJsonFromApi(
      projectApiPath(`/conversations/${encodeURIComponent(conversationId)}`));
  } catch (openFailure) {
    console.error("could not open the conversation", openFailure);
    log.innerHTML = `<div class="msg bad">${escapeHtml(openFailure.message)}</div>`;
    return;
  }

  applicationState.agentConversationId = conversation.id;
  log.innerHTML = conversation.turns.map(turn => `
    <div class="msg mine">${escapeHtml(turn.question)}</div>
    ${renderOrchestratorReply({
      agent: "Orchestrator", agent_source: "default", answer: turn.answer,
      consulted: turn.consulted, artifacts_read: turn.artifacts_read,
    })}`).join("");
  wireConsultedAgents(log);
  log.scrollTop = log.scrollHeight;
}

select("#new-conversation-button").onclick = startNewConversation;

select("#conversation-history-button").onclick = async () => {
  const list = select("#conversation-list");
  const showing = list.hidden;
  select("#conversation-history-button").setAttribute("aria-expanded", String(showing));
  list.hidden = !showing;
  if (!showing) return;
  list.innerHTML = `<p class="muted conversation-empty">Loading…</p>`;
  await refreshConversationList();
  renderConversationList();
};

select("#drawer-send-button").onclick = askTheAgent;

select("#drawer-input").addEventListener("keydown", event => {
  if (event.key === "Enter") select("#drawer-send-button").click();
});

document.addEventListener("keydown", event => {
  if (event.key !== "Escape") return;
  if (isCredentialsPanelOpen()) closeCredentialsPanel();
  else if (drawer.classList.contains("open")) drawer.classList.remove("open");
});

boot();


/** Expand a file row to show the file itself.
 *
 *  Opened on first expand and then kept, so collapsing and reopening a document
 *  does not draw it again -- except a deck, which is released on collapse
 *  because its rendered slides are the heaviest thing on the page.
 */
async function toggleSourcePreview(button) {
  const fileName = button.dataset.preview;
  const panel = document.querySelector(`[data-preview-for="${CSS.escape(fileName)}"]`);
  if (!panel) return;

  const isOpening = panel.hidden;
  panel.hidden = !isOpening;

  if (!isOpening && releaseRawFile(fileName)) panel.dataset.loaded = "";
  button.setAttribute("aria-expanded", String(isOpening));
  button.classList.toggle("open", isOpening);

  if (!isOpening || panel.dataset.loaded === "true") return;

  panel.innerHTML = `<p class="muted" style="margin:0">Reading ${escapeHtml(fileName)}…</p>`;

  try {
    const preview = await requestJsonFromApi(
      projectApiPath(`/sources/${encodeURIComponent(fileName)}/preview`));
    panel.innerHTML = renderRawFileShell(fileName, preview, { pdfPages: true });
    panel.dataset.loaded = "true";
    openRawFile(panel, fileName, preview.viewer, { editable: true });
  } catch (previewFailure) {
    console.error("preview failed", previewFailure);
    panel.innerHTML = `<p class="muted" style="margin:0">
      Could not read this file — ${escapeHtml(previewFailure.message)}</p>`;
  }
}

/** A saved deck is a smaller file: its row and the project's figures say so. */
document.addEventListener("deck-edited", async event => {
  await refreshProjectSummary();
  if (applicationState.activeStageKey === "inputs") renderMain();
});

/** The back button moves through the stages you visited.
 *
 *  Without this, pushing an address on every navigation would give a back
 *  button that changes the bar and nothing else -- worse than no routing at
 *  all, because the page would then disagree with its own URL.
 */
window.addEventListener("popstate", async () => {
  const { stageKey, projectSlug } = readAddress();

  const wantedProject = applicationState.availableProjects
    .find(project => project.slug === projectSlug);
  if (wantedProject && wantedProject.slug !== applicationState.selectedProject?.slug) {
    applicationState.selectedProject = wantedProject;
    rememberSelectedProject(wantedProject.slug);
    select("#project-select").value = wantedProject.slug;
    clearProjectScopedState();
    resetConversationPanel();
  }

  if (isKnownPage(stageKey)) applicationState.activeStageKey = stageKey;

  renderSidebar();
  renderMain();
});
