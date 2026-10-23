/**
 * Reviewing stage — watch, comment, and decide whether it ships.
 *
 * The comment log is the point: it answers "what did we ask for, and did it get
 * done?". Each comment is timestamped, attributed, routed to the stage
 * that can fix it, and resolvable.
 */

import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, footerNav, icon, projectApiPath, select,
  showStageNotice, stageHeader, wireGotoButtons,
} from "/static/ui-kit.js";
import { addToRenderQueue } from "/static/render-dock.js";

/** Redraws Reviewing when its project's render finishes; replaced on each draw. */
let redrawWhenRendered = () => {};

const reviewViewState = {
  playheadMs: 0,
  isComposingComment: false,
};

/** Stages a comment can be routed to. Reviewing itself is excluded: routing a
 *  comment back to the stage it was raised in says nothing about who fixes it. */
const ROUTABLE_STAGES = ["extraction", "scene-plan", "script-staging", "studio"];

function formatTimecode(milliseconds) {
  const totalSeconds = Math.floor(milliseconds / 1000);
  return `${String(Math.floor(totalSeconds / 60)).padStart(2, "0")}:${
    String(totalSeconds % 60).padStart(2, "0")}`;
}

function relativeTime(isoTimestamp) {
  const elapsedMs = Date.now() - new Date(isoTimestamp).getTime();
  if (Number.isNaN(elapsedMs)) return "";
  const minutes = Math.round(elapsedMs / 60000);
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes} min ago`;
  const hours = Math.round(minutes / 60);
  if (hours < 24) return `${hours} hour${hours === 1 ? "" : "s"} ago`;
  return `${Math.round(hours / 24)} day(s) ago`;
}

const initialsOf = name =>
  (name || "?").trim().split(/\s+/).slice(0, 2).map(part => part[0]).join("").toUpperCase();

export async function renderReviewingStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  body.innerHTML = `<div class="card muted">Loading review…</div>`;

  let review;
  try {
    review = await loadStageDocument("review", "/review");
    if (review === null) return;
  } catch (loadFailure) {
    console.error("review load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load the review.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }

  body.innerHTML = `
    ${stageHeader("reviewing", "Reviewing", {
      agentButtonId: "reviewing-agent-button",
    })}

    <div class="card stage-content">

      ${renderReadinessCard(review)}
      ${renderSceneProblems(review.scene_problems)}

      <div class="review-grid">
        <div>
          ${renderPlayer(review)}
          ${renderTabs(review)}
        </div>
        <div>
          ${renderVersionPanel(review)}
          ${renderChapterPanel(review)}
        </div>
      </div>

      ${renderFooterNav(stage, review)}
    </div>`;

  wireReviewingStage(stage, navigateToStage, renderAgentStage);
}

/* ---- readiness ---------------------------------------------------------- */

/** Scenes by severity: their own checks still fail (a visible defect, it blocks the
 *  hand-over), or only the reviewer wants more (counted, not listed one by one). */
function renderSceneProblems(problems) {
  const failing = problems?.failing ?? [];
  const below = problems?.below_bar ?? [];
  if (!failing.length && !below.length) return "";
  return `
    ${failing.length ? `
      <div class="notice bad" style="margin:0 0 10px">
        <b>${failing.length} scene(s) in the video still fail their own checks:</b>
        <ul class="ready-checks">${failing.map(e => `<li>Scene ${e.scene}
          (${escapeHtml(e.section)}): ${escapeHtml(e.checks.join(", "))}</li>`).join("")}</ul>
        <button class="btn" id="remake-failing-button"
          data-visual-ids="${escapeHtml(failing.map(e => e.visual_id).join(","))}">
          Remake these ${failing.length} scene(s)</button>
      </div>` : ""}
    ${below.length ? `
      <div class="notice warn" style="margin:0 0 10px">
        ${below.length} scene(s) pass their checks but are below the reviewer's bar:
        scenes ${below.map(e => e.scene).join(", ")}. Open one on Generation to read what
        the reviewer wants.
      </div>` : ""}`;
}

function renderReadinessCard(review) {
  const openCount = review.audit.open_comment_count;
  const byStage = review.audit.by_stage;
  const failingScenes = review.scene_problems?.failing?.length ?? 0;
  const isReady = review.is_ready_to_export;
  // With no open comments, any warning left is an advisory -- a section far over
  // its planned length, versions that share one file. They do not block export,
  // but they are not "nothing", so the card shows no green tick over them.
  const warnings = review.warnings ?? [];
  const hasChecks = isReady && warnings.length > 0;

  // Where the open comments cluster is the useful signal: six routed to Script & Staging
  // means the script is the problem, not the timeline.
  const clusters = Object.entries(byStage)
    .sort((a, b) => b[1] - a[1])
    .map(([stageKey, count]) => `<span class="stage-chip ${
      stageKey === "unrouted" ? "unrouted" : ""}">${escapeHtml(stageKey)} ${count}</span>`)
    .join(" ");

  return `
    <div class="ready-card ${hasChecks ? "check" : isReady ? "ready" : "blocked"}">
      <span class="mark">${icon(isReady && !hasChecks ? ICON.check : ICON.alert, 17,
                                isReady && !hasChecks ? 2.4 : 2)}</span>
      <span class="text">
        <b>${!isReady
          ? (failingScenes ? `${failingScenes} scene(s) fail their own checks` : "")
            + (failingScenes && openCount ? " · " : "")
            + (openCount ? `${openCount} comment(s) still open` : "")
          : hasChecks
            ? `No open comments — ${warnings.length} thing${warnings.length === 1 ? "" : "s"} to check`
            : "Nothing outstanding"}</b>
        <span>${!isReady
          ? (openCount ? `Where the work is: ${clusters}` : "Listed below; export waits for them.")
          : hasChecks
            ? `<ul class="ready-checks">${warnings.map(w => `<li>${escapeHtml(w)}</li>`).join("")}</ul>`
            : review.versions.some(v => v.is_rendered)
              ? "No open feedback, and a render exists. Re-render to pick up any changes."
              : "No open feedback. Render the video to watch it here."}</span>
      </span>
      <button class="btn btn-accent" id="render-button"
              title="Add this project to the render queue, on the Render tab">
        Render video
      </button>
    </div>`;
}

/* ---- player ------------------------------------------------------------- */

function renderPlayer(review) {
  const activeVersion = review.versions.find(v => v.id === review.active_version_id)
    ?? review.versions.findLast(v => v.is_rendered);

  // A real player once a render exists. The <video> element owns its own
  // transport, so the fake scrubber below it is dropped rather than left to
  // disagree with the thing actually playing.
  if (activeVersion?.is_rendered) {
    const fileName = activeVersion.file_path.split(/[\\/]/).pop();
    const videoUrl = projectApiPath(`/output/${encodeURIComponent(fileName)}`);
    // .vtt for the <track>; a browser will not load .srt. The .srt is still
    // produced and offered as a download for editors that expect it.
    const stem = fileName.replace(/\.mp4$/i, "");
    const captionsUrl = projectApiPath(`/output/${encodeURIComponent(stem + ".vtt")}`);
    const subtitleUrl = projectApiPath(`/output/${encodeURIComponent(stem + ".srt")}`);

    return `
      <div class="panel" style="margin-bottom:14px">
        <video class="review-video" controls preload="metadata" src="${videoUrl}"
               crossorigin="anonymous">
          <track kind="subtitles" label="English" srclang="en" src="${captionsUrl}" default>
          Your browser cannot play this file.
        </video>
        <div class="transport">
          <span class="time">${formatTimecode(activeVersion.duration_ms)}</span>
          <span class="mono muted">${escapeHtml(activeVersion.label)}</span>
          <div class="spacer"></div>
          <a class="btn" href="${videoUrl}" download>Download .mp4</a>
          <a class="btn" href="${subtitleUrl}" download>.srt</a>
        </div>
      </div>`;
  }

  return `
    <div class="panel" style="margin-bottom:14px">
      <div class="preview-frame">
        <div class="placeholder">
          ${icon(`<rect x="2" y="5" width="14" height="14" rx="2"/><path d="m22 8-6 4 6 4V8z"/>`,
                 40, 1.3)}
          <p>No render yet.<br>Use <b>Render video</b> above to make one.</p>
        </div>
      </div>
      <div class="transport">
        <span class="mono muted">${review.versions.length} version(s)</span>
      </div>
    </div>`;
}

/* ---- tabs --------------------------------------------------------------- */

function renderTabs(review) {
  const openCount = review.audit.open_comment_count;
  const isTranscript = applicationState.reviewTab === "transcript";

  return `
    <div class="panel">
      <div class="preview-head">
        <div class="seg">
          <button class="${isTranscript ? "on" : ""}" data-review-tab="transcript">Transcript</button>
          <button class="${isTranscript ? "" : "on"}" data-review-tab="comments">
            Comments${review.comments.length ? ` (${review.comments.length})` : ""}</button>
        </div>
        <div class="spacer"></div>
        ${openCount ? `<span class="stage-chip unrouted">${openCount} open</span>` : ""}
      </div>

      ${isTranscript ? renderTranscript(review) : renderComments(review)}
    </div>`;
}

function renderTranscript(review) {
  if (!review.transcript.length) {
    return `<p class="muted" style="font-size:12.5px;margin:0">
      No sections yet. The transcript follows the plan and script.</p>`;
  }

  const rows = review.transcript.map(entry => {
    // The server measures these against the render; the page must not recompute
    // them from the plan's estimates, which is how they came to be minutes out.
    const startMs = entry.start_ms ?? 0;
    const hasBody = entry.body.trim().length > 0;

    return `
      <button class="transcript-row" data-jump="${startMs}">
        <span class="stamp">${formatTimecode(startMs)}</span>
        <span class="line ${hasBody ? "" : "empty"}">
          ${hasBody
            ? escapeHtml(entry.body.slice(0, 220)) + (entry.body.length > 220 ? "…" : "")
            : `${escapeHtml(entry.title || "Untitled section")} — not written yet`}
        </span>
      </button>`;
  }).join("");

  return `<div class="transcript-list">${rows}</div>
    <p class="muted" style="font-size:11.5px;margin:10px 0 0">
      Timings are estimates from the plan. A render will replace them with measured ones.
    </p>`;
}

function renderComments(review) {
  return `
    ${renderCommentForm()}
    ${review.comments.length
      ? review.comments.map(renderComment).join("")
      : `<p class="muted" style="font-size:12.5px;margin:0">No feedback yet.</p>`}`;
}

function renderCommentForm() {
  if (!reviewViewState.isComposingComment) {
    return `<button class="add-row" id="start-comment-button" style="margin-bottom:14px">
      ${icon(ICON.plus)} Add a comment</button>`;
  }

  return `
    <div class="comment-form">
      <textarea id="comment-body" placeholder="What needs to change?"
                aria-label="Comment"></textarea>
      <div class="row">
        <input id="comment-author" placeholder="Your name" maxlength="80"
               value="${escapeHtml(localStorage.getItem("reviewerName") ?? "")}">
        <input id="comment-at" type="number" min="0" step="1000"
               value="${reviewViewState.playheadMs}" style="width:110px"
               aria-label="Timecode in milliseconds">
        <select id="comment-stage" aria-label="Route to stage">
          <option value="">Route to…</option>
          ${ROUTABLE_STAGES.map(stageKey =>
            `<option value="${stageKey}">${stageKey}</option>`).join("")}
        </select>
        <div class="spacer" style="flex:1"></div>
        <button class="btn" id="cancel-comment-button">Cancel</button>
        <button class="btn btn-accent" id="submit-comment-button">Comment</button>
      </div>
    </div>`;
}

function renderComment(comment) {
  return `
    <div class="comment ${comment.status}">
      <span class="avatar">${escapeHtml(initialsOf(comment.author))}</span>
      <div class="content">
        <div class="meta">
          <span class="who">${escapeHtml(comment.author)}</span>
          <span class="when">${escapeHtml(relativeTime(comment.created_at))}</span>
          <span class="stamp-chip">${formatTimecode(comment.at_ms)}</span>
          <span class="stage-chip ${comment.routed_to_stage ? "" : "unrouted"}">
            ${escapeHtml(comment.routed_to_stage ?? "unrouted")}</span>
          ${comment.status !== "open"
            ? `<span class="stamp-chip">${escapeHtml(comment.status)}</span>` : ""}
        </div>
        <div class="body">${escapeHtml(comment.body)}</div>
        ${comment.status === "open" ? `
          <div class="actions">
            <button class="btn" data-address="${comment.id}"
                    style="padding:4px 10px;font-size:12px">Mark addressed</button>
            <button class="btn" data-decline="${comment.id}"
                    style="padding:4px 10px;font-size:12px">Decline</button>
            ${comment.routed_to_stage
              ? `<button class="btn" data-goto="${comment.routed_to_stage}"
                     style="padding:4px 10px;font-size:12px">
                   Go to ${escapeHtml(comment.routed_to_stage)}</button>` : ""}
          </div>` : `
          <div class="actions">
            <button class="btn" data-reopen="${comment.id}"
                    style="padding:4px 10px;font-size:12px">Reopen</button>
          </div>`}
      </div>
      <button class="btn-icon danger" data-delete-comment="${comment.id}"
              title="Delete comment" aria-label="Delete comment">
        ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 14)}
      </button>
    </div>`;
}

/* ---- side panels -------------------------------------------------------- */

function renderVersionPanel(review) {
  return `
    <div class="panel" style="margin-bottom:14px">
      <div class="panel-head">
        <h3>Versions</h3>
        <div class="spacer"></div>
        <button class="btn-icon" id="add-version-button"
                title="Record a version" aria-label="Record a version">${icon(ICON.plus, 15)}</button>
      </div>
      <p class="panel-sub">Which cut a comment was made against.</p>

      ${review.versions.length ? review.versions.map(version => `
        <button class="version-row ${version.id === review.active_version_id ? "active" : ""}"
                data-version="${version.id}">
          <span class="vlabel">${escapeHtml(version.label || "Untitled")}</span>
          <span class="vwhen">${escapeHtml(relativeTime(version.created_at))}</span>
          ${version.is_rendered ? "" : `<span class="stamp-chip">no file</span>`}
        </button>`).join("")
        : `<p class="muted" style="font-size:12.5px;margin:0">
             None recorded. Rendering will add these automatically.</p>`}
    </div>`;
}

function renderChapterPanel(review) {
  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Chapters</h3>
        <div class="spacer"></div>
        <button class="btn-icon" id="seed-chapters-button"
                title="Rebuild from the plan (replaces existing)"
                aria-label="Rebuild chapters from the plan">
          ${icon(`<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>`, 15, 1.7)}
        </button>
        <button class="btn-icon" id="add-chapter-button"
                title="Add chapter" aria-label="Add chapter">${icon(ICON.plus, 15)}</button>
      </div>

      ${review.chapters.length ? review.chapters.map((chapter, index) => `
        <div class="chapter-row">
          <span class="idx">${index + 1}</span>
          <span class="title ${chapter.title ? "" : "untitled"}"
                data-edit-chapter="${chapter.id}" title="Click to rename"
                >${escapeHtml(chapter.title || "Untitled")}</span>
          <span class="vwhen">${formatTimecode(chapter.start_ms)}</span>
          <button class="btn-icon danger" data-delete-chapter="${chapter.id}"
                  title="Remove" aria-label="Remove chapter">
            ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 13)}
          </button>
        </div>`).join("")
        : `<p class="muted" style="font-size:12.5px;margin:0">
             None yet. Seed them from the plan with the refresh button.</p>`}
    </div>`;
}

function renderFooterNav(stage, review) {
  return footerNav(stage, {
    middle: `
      <span class="plan-total" style="margin-left:14px">
        ${review.comments.length} comment(s) · ${review.chapters.length} chapter(s)
      </span>`,
    end: `<span class="muted" style="font-size:12.5px">Last stage</span>`,
  });
}

/* ---- persistence -------------------------------------------------------- */

/* ---- wiring ------------------------------------------------------------- */

function wireReviewingStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderReviewingStage(stage, navigateToStage, renderAgentStage);
  // The GET assembles transcript and plan_sections that the POST response omits;
  // onSaved keeps them so the panes do not blank until the next full load.
  const change = applyEdit => editStageDocument({
    documentKind: "review", apiPathSuffix: "/review", applyEdit, rerender,
    buildPayload: review => ({
      comments: review.comments, chapters: review.chapters,
      versions: review.versions, active_version_id: review.active_version_id,
    }),
    onSaved: (saved, before) => ({
      ...saved, transcript: before.transcript, plan_sections: before.plan_sections,
    }),
  });

  wireGotoButtons(navigateToStage);
  select("#reviewing-agent-button").onclick = () => renderAgentStage(stage);

  // Remakes the failing scenes from the start -- the button used to only open
  // Generation, and read as broken -- then shows them being made there.
  const remakeButton = select("#remake-failing-button");
  if (remakeButton) remakeButton.onclick = async () => {
    remakeButton.disabled = true;
    try {
      await requestJsonFromApi(projectApiPath("/scene-agents"), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ visual_ids: remakeButton.dataset.visualIds.split(","),
                               fresh: true }),
      });
      navigateToStage("generation");
    } catch (remakeFailure) {
      remakeButton.disabled = false;
      showStageNotice("bad", `Could not start the remake — ${remakeFailure.message}`);
    }
  };

  // Into the render queue at the bottom of the page; when this project's
  // render finishes there, this page redraws to play it.
  const renderButton = select("#render-button");
  if (renderButton) renderButton.onclick = () => addToRenderQueue(() => navigateToStage("render"));
  window.removeEventListener("render-finished", redrawWhenRendered);
  redrawWhenRendered = event => {
    if (event.detail.slug === applicationState.selectedProject?.slug
        && select("#render-button")?.isConnected) rerender();
  };
  window.addEventListener("render-finished", redrawWhenRendered);

  document.querySelectorAll("[data-review-tab]").forEach(tab => {
    tab.onclick = () => {
      applicationState.reviewTab = tab.dataset.reviewTab;
      rerender();
    };
  });

  // Clicking a line seeks the video, which has its own transport.
  document.querySelectorAll("[data-jump]").forEach(row => {
    row.onclick = () => {
      const atMs = Number(row.dataset.jump) || 0;
      reviewViewState.playheadMs = atMs;
      const player = document.querySelector("video.review-video");
      if (!player) return;
      player.currentTime = atMs / 1000;
      player.play().catch(playFailure => console.warn("could not play", playFailure));
    };
  });

  wireCommentForm(change, rerender);
  wireCommentActions(change);
  wireChapters(change, rerender);
  wireVersions(change);
}

function wireCommentForm(change, rerender) {
  const startButton = select("#start-comment-button");
  if (startButton) {
    startButton.onclick = () => {
      reviewViewState.isComposingComment = true;
      rerender();
    };
    return;
  }

  const cancelButton = select("#cancel-comment-button");
  if (cancelButton) {
    cancelButton.onclick = () => {
      reviewViewState.isComposingComment = false;
      rerender();
    };
  }

  const bodyField = select("#comment-body");
  bodyField?.focus();

  const submitButton = select("#submit-comment-button");
  if (!submitButton) return;

  submitButton.onclick = () => {
    const commentBody = select("#comment-body").value.trim();
    if (!commentBody) {
      showStageNotice("warn", "A comment needs some text.");
      select("#comment-body").focus();
      return;
    }
    const author = select("#comment-author").value.trim() || "Anonymous";
    // Remembered per browser so a reviewer does not retype their name each time.
    try { localStorage.setItem("reviewerName", author); } catch { /* private mode */ }

    const routedStage = select("#comment-stage").value || null;
    const atMs = Number(select("#comment-at").value) || 0;

    reviewViewState.isComposingComment = false;
    change(review => {
      review.comments.unshift({
        id: newItemIdentifier(),
        author, body: commentBody, at_ms: atMs,
        created_at: new Date().toISOString(),
        status: "open", routed_to_stage: routedStage, resolution_note: "",
      });
    });
  };
}

function wireCommentActions(change) {
  const setStatus = (commentId, status) => change(review => {
    const comment = review.comments.find(c => c.id === commentId);
    if (comment) comment.status = status;
  });

  document.querySelectorAll("[data-address]").forEach(button => {
    button.onclick = () => setStatus(button.dataset.address, "addressed");
  });
  document.querySelectorAll("[data-decline]").forEach(button => {
    button.onclick = () => setStatus(button.dataset.decline, "declined");
  });
  document.querySelectorAll("[data-reopen]").forEach(button => {
    button.onclick = () => setStatus(button.dataset.reopen, "open");
  });

  document.querySelectorAll("[data-delete-comment]").forEach(button => {
    button.onclick = () => {
      // Deleting is destructive and unlike resolving cannot be undone from the UI.
      if (!window.confirm("Delete this comment permanently?")) return;
      change(review => {
        review.comments = review.comments
          .filter(c => c.id !== button.dataset.deleteComment);
      });
    };
  });
}

function wireChapters(change, rerender) {
  select("#add-chapter-button").onclick = () => {
    const title = window.prompt("Chapter title");
    if (!title?.trim()) return;
    change(review => {
      review.chapters.push({
        id: newItemIdentifier(),
        title: title.trim(), start_ms: reviewViewState.playheadMs,
      });
    });
  };

  select("#seed-chapters-button").onclick = async () => {
    // Destructive: it replaces hand-edited titles, so it asks first.
    if (!window.confirm("Rebuild chapters from the plan? This replaces the current ones."))
      return;
    try {
      const rebuilt = await requestJsonFromApi(
        projectApiPath("/review/seed-chapters"), { method: "POST" });
      applicationState.review = {
        ...rebuilt,
        transcript: applicationState.review.transcript,
        plan_sections: applicationState.review.plan_sections,
      };
      await rerender();
      showStageNotice("ok", `Rebuilt ${rebuilt.chapters.length} chapter(s) from the plan.`);
    } catch (seedFailure) {
      console.error("seed chapters failed", seedFailure);
      showStageNotice("bad", `Could not rebuild chapters — ${seedFailure.message}`);
    }
  };

  document.querySelectorAll("[data-edit-chapter]").forEach(titleNode => {
    titleNode.onclick = () => {
      const chapter = applicationState.review.chapters
        .find(c => c.id === titleNode.dataset.editChapter);
      const next = window.prompt("Chapter title", chapter.title);
      if (next === null) return;
      change(review => {
        const target = review.chapters.find(c => c.id === titleNode.dataset.editChapter);
        if (target) target.title = next.trim();
      });
    };
  });

  document.querySelectorAll("[data-delete-chapter]").forEach(button => {
    button.onclick = () => change(review => {
      review.chapters = review.chapters
        .filter(c => c.id !== button.dataset.deleteChapter);
    });
  });
}

function wireVersions(change) {
  select("#add-version-button").onclick = () => {
    const label = window.prompt("Version label (e.g. v1)");
    if (!label?.trim()) return;
    change(review => {
      const version = {
        id: newItemIdentifier(),
        label: label.trim(), created_at: new Date().toISOString(),
        notes: "", duration_ms: 0, file_path: null,
      };
      review.versions.unshift(version);
      review.active_version_id = version.id;
    });
  };

  document.querySelectorAll("[data-version]").forEach(row => {
    row.onclick = () => change(review => {
      review.active_version_id = row.dataset.version;
    });
  });
}
