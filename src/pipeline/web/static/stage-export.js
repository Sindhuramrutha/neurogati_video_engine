/**
 * Export — the video and everything that travels with it.
 *
 * The files are derived, so the interesting part of this page is not the list of
 * downloads: it is what is stopping the hand-over. A cut built from an abandoned
 * script, a section nobody narrated, a video file that is no longer on disk —
 * this is the last page on which any of those can still be caught.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, formatFileSize, icon, projectApiPath, select,
  showStageNotice, stageIcon,
} from "/static/ui-kit.js";

const KIND_LABELS = {
  video: "Video", subtitles: "Subtitles", transcript: "Transcript",
  chapters: "Chapters", description: "Description", audio: "Narration",
};

export async function renderExportStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  body.innerHTML = `<div class="card muted">Loading…</div>`;

  let manifest;
  try {
    manifest = await requestJsonFromApi(projectApiPath("/export"));
  } catch (loadFailure) {
    console.error("export load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load the export.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }
  applicationState.exportManifest = manifest;

  body.innerHTML = `
    <div class="card">
      <div class="card-head">
        <span class="card-icon">${stageIcon("export", 21)}</span>
        <div>
          <h2>Export</h2>
          <p>The video, its transcript, its chapters and a description — as files.</p>
        </div>
        <button class="btn" id="export-agent-button">
          ${icon(ICON.gear, 14, 1.8)} Agent &amp; instructions
        </button>
      </div>

      ${renderRunBar(manifest)}
      ${renderBlockers(manifest)}

      ${manifest.is_empty
        ? `<div class="empty">
             <h3>Nothing exported yet</h3>
             <p>Build the export to write the transcript, the chapter marks and the
                description beside the rendered video.</p>
           </div>`
        : renderFiles(manifest)}

      ${renderFooterNav(stage)}
    </div>`;

  wireExportStage(stage, navigateToStage, renderAgentStage);
}

function renderRunBar(manifest) {
  const blocked = manifest.blockers_now.length > 0;
  const tone = blocked ? "stale" : manifest.is_empty ? "blocked" : "ready";
  const built = manifest.built_at
    ? `Built ${escapeHtml(manifest.built_at.slice(0, 16).replace("T", " "))} UTC · `
      + `${manifest.file_count} file(s)`
    : "Nothing built yet.";

  return `
    <div class="run-bar ${tone}">
      <span class="run-icon">${icon(blocked ? ICON.alert : ICON.check, 17, 2.2)}</span>
      <span class="run-text">
        <b>${blocked
          ? `Not ready to hand over`
          : manifest.is_empty ? "Ready to build" : "Ready to hand over"}</b>
        <span>${built}</span>
      </span>
      <button class="btn btn-accent" id="build-export-button">
        ${manifest.is_empty ? "Build export" : "Build again"}
      </button>
    </div>`;
}

/** What is wrong, separated from what is merely worth knowing. */
function renderBlockers(manifest) {
  const blockers = manifest.blockers_now ?? [];
  const warnings = manifest.warnings_now ?? [];
  if (!blockers.length && !warnings.length) return "";

  return `
    ${blockers.length ? `
      <div class="notice bad" style="margin-bottom:12px">
        <b>${blockers.length} thing(s) would make this hand-over wrong:</b>
        <ul class="export-list">${blockers.map(b => `<li>${escapeHtml(b)}</li>`).join("")}</ul>
      </div>` : ""}
    ${warnings.length ? `
      <div class="notice warn" style="margin-bottom:14px">
        ${warnings.map(escapeHtml).join(" · ")}
      </div>` : ""}`;
}

function renderFiles(manifest) {
  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Files</h3>
        <div class="spacer"></div>
        ${manifest.duration_ms
          ? `<span class="plan-total">${Math.round(manifest.duration_ms / 60000)} min</span>` : ""}
      </div>
      ${manifest.files.map(file => `
        <div class="export-row">
          <span class="fact ${file.kind === "video" ? "ok" : "muted"}"
            >${escapeHtml(KIND_LABELS[file.kind] ?? file.kind)}</span>
          <span class="export-name">
            <b>${escapeHtml(file.name)}</b>
            <span>${escapeHtml(file.note)}</span>
          </span>
          <span class="mono muted">${formatFileSize(file.bytes)}</span>
          ${file.path.startsWith("export/")
            ? `<a class="btn" download
                  href="${projectApiPath(`/export/files/${encodeURIComponent(file.name)}`)}"
               >Download</a>`
            : `<a class="btn" download href="${projectApiPath("/output")}">Download</a>`}
        </div>`).join("")}
    </div>`;
}

function renderFooterNav(stage) {
  const { stageDefinitions } = applicationState;
  const index = stageDefinitions.findIndex(s => s.key === stage.key);
  const previous = stageDefinitions[index - 1];
  return `
    <div class="footer-nav">
      ${previous ? `<button class="btn" data-goto="${previous.key}">
        ${icon(ICON.arrowLeft)} Back to ${escapeHtml(previous.title)}</button>` : ""}
      <div class="spacer"></div>
    </div>`;
}

function wireExportStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderExportStage(stage, navigateToStage, renderAgentStage);

  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });
  select("#export-agent-button").onclick = () => renderAgentStage(stage);

  select("#build-export-button").onclick = async () => {
    const button = select("#build-export-button");
    button.disabled = true;
    button.textContent = "Building…";
    try {
      const built = await requestJsonFromApi(projectApiPath("/export"), { method: "POST" });
      applicationState.exportManifest = built;
      showStageNotice(built.blockers.length ? "warn" : "ok",
        built.blockers.length
          ? `Built, but ${built.blockers.length} thing(s) would make it wrong.`
          : `Built ${built.file_count} file(s).`);
    } catch (buildFailure) {
      console.error("building the export failed", buildFailure);
      showStageNotice("bad", buildFailure.message);
    }
    await rerender();
  };
}
