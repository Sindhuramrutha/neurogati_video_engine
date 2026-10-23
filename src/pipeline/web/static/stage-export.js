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
  ICON, applicationState, escapeHtml, footerNav, formatFileSize, icon, projectApiPath,
  select, showStageNotice, stageHeader, wireGotoButtons,
} from "/static/ui-kit.js";

let finishPoll = null;

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
  const finish = await requestJsonFromApi(projectApiPath("/finish"))
    .catch(() => ({ state: "idle" }));
  applicationState.finishing = finish;

  body.innerHTML = `
    ${stageHeader("export", "Export", {
      agentButtonId: "export-agent-button",
    })}

    <div class="card stage-content">

      ${renderFinishBar(finish)}
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

/** Finishing the video in one go, on the server: the scenes still missing or
 *  failing their checks, the render, the export -- with the step it is on. */
function renderFinishBar(finish) {
  const ended = { done: "Finished", blocked: "Finished, not ready", failed: "Stopped" };
  return `
    <div class="run-bar ${finish.running ? "stale" : finish.state === "done" ? "ready" : ""}"
         style="margin-bottom:12px">
      <span class="run-text">
        <b>${finish.running ? "Finishing the video…" : ended[finish.state] ?? "Finish the video"}</b>
        <span>${escapeHtml(finish.running || ended[finish.state] ? finish.step ?? ""
          : "Makes the scenes still missing, remakes those failing their checks, "
            + "renders and builds the export.")}</span>
      </span>
      ${finish.running ? "" : `
        <button class="btn btn-accent" id="finish-video-button">Finish the video</button>`}
    </div>`;
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
          : manifest.is_empty ? "Ready to build"
            : manifest.draft ? "Built as a draft" : "Ready to hand over"}</b>
        <span>${built}${manifest.draft
          ? " · scenes with failing checks were accepted on purpose" : ""}</span>
      </span>
      <button class="btn btn-accent" id="build-export-button">
        ${manifest.is_empty ? "Build export" : "Build again"}
      </button>
      ${(manifest.scene_problems?.failing ?? []).length && !manifest.draft ? `
        <button class="btn" id="build-draft-button"
                title="Accept the scenes whose own checks still fail, and mark it a draft">
          Build as a draft anyway</button>` : ""}
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
            : `<a class="btn" download
                  href="${projectApiPath(`/output/${encodeURIComponent(file.name)}`)}"
               >Download</a>`}
        </div>`).join("")}
    </div>`;
}

function renderFooterNav(stage) {
  return footerNav(stage);
}

function wireExportStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderExportStage(stage, navigateToStage, renderAgentStage);

  wireGotoButtons(navigateToStage);
  select("#export-agent-button").onclick = () => renderAgentStage(stage);

  const finishButton = select("#finish-video-button");
  if (finishButton) finishButton.onclick = async () => {
    finishButton.disabled = true;
    try {
      await requestJsonFromApi(projectApiPath("/finish"), { method: "POST" });
    } catch (finishFailure) {
      showStageNotice("bad", `Could not start finishing — ${finishFailure.message}`);
    }
    await rerender();
  };
  // While it finishes, the page follows it.
  clearTimeout(finishPoll);
  if (applicationState.finishing?.running) {
    finishPoll = setTimeout(() => {
      if (select("#export-agent-button")?.isConnected) rerender();
    }, 15000);
  }

  const draftButton = select("#build-draft-button");
  if (draftButton) {
    draftButton.onclick = async () => {
      const count = applicationState.exportManifest?.scene_problems?.failing?.length ?? 0;
      if (!window.confirm(`Build the export as a draft, with ${count} scene(s) whose own `
          + "checks still fail? The manifest will say it is a draft.")) return;
      try {
        applicationState.exportManifest = await requestJsonFromApi(
          projectApiPath("/export?draft=true"), { method: "POST" });
        showStageNotice("warn", `Built as a draft, with ${count} scene(s) accepted as they are.`);
      } catch (buildFailure) {
        console.error("building the draft export failed", buildFailure);
        showStageNotice("bad", buildFailure.message);
      }
      await rerender();
    };
  }

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
