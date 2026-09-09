/**
 * Reviewing stage — watch, comment, and decide whether it ships.
 *
 * The comment log is the point. v1's feedback was prose typed into a terminal and
 * gone with the scrollback, so nobody could answer "what did we ask for, and did
 * it get done?". Here each comment is timestamped, attributed, routed to the stage
 * that can fix it, and resolvable.
 */

import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, icon, projectApiPath, select,
  showStageNotice, stageIcon,
} from "/static/ui-kit.js";

const reviewViewState = {
  activeTab: "transcript",
  playheadMs: 0,
  isComposingComment: false,
};

/** Stages a comment can be routed to. Reviewing itself is excluded: routing a
 *  comment back to the stage it was raised in says nothing about who fixes it. */
const ROUTABLE_STAGES = ["extraction", "planning", "scripting", "studio"];

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
    <div class="card">
      <div class="card-head">
        <span class="card-icon">${stageIcon("reviewing", 21)}</span>
        <div>
          <h2>Reviewing</h2>
          <p>Watch, give feedback, and decide whether it ships.</p>
        </div>
        <button class="btn" id="reviewing-agent-button">
          ${icon(ICON.gear, 14, 1.8)} Agent &amp; instructions
        </button>
      </div>

      ${renderReadinessCard(review)}

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

function renderReadinessCard(review) {
  const openCount = review.audit.open_comment_count;
  const byStage = review.audit.by_stage;
  const isReady = review.is_ready_to_export;

  // Where the open comments cluster is the useful signal: six routed to Scripting
  // means the script is the problem, not the timeline.
  const clusters = Object.entries(byStage)
    .sort((a, b) => b[1] - a[1])
    .map(([stageKey, count]) => `<span class="stage-chip ${
      stageKey === "unrouted" ? "unrouted" : ""}">${escapeHtml(stageKey)} ${count}</span>`)
    .join(" ");

  return `
    <div class="ready-card ${isReady ? "ready" : "blocked"}">
      <span class="mark">${icon(isReady ? ICON.check : ICON.alert, 17, isReady ? 2.4 : 2)}</span>
      <span class="text">
        <b>${isReady ? "Nothing outstanding" : `${openCount} comment(s) still open`}</b>
        <span>${isReady
          ? "No open feedback. Export when a render exists."
          : `Where the work is: ${clusters}`}</span>
      </span>
      <button class="btn btn-accent" id="export-button" disabled
              title="Rendering is not built yet">
        Export final video
      </button>
    </div>`;
}

/* ---- player ------------------------------------------------------------- */

function renderPlayer(review) {
  const activeVersion = review.versions.find(v => v.id === review.active_version_id);

  return `
    <div class="panel" style="margin-bottom:14px">
      <div class="preview-frame">
        <div class="placeholder">
          ${icon(`<rect x="2" y="5" width="14" height="14" rx="2"/><path d="m22 8-6 4 6 4V8z"/>`,
                 40, 1.3)}
          <p>${activeVersion && activeVersion.is_rendered
            ? escapeHtml(activeVersion.label)
            : "No render yet.<br>Comments below can still be written against the plan and script."}</p>
        </div>
      </div>

      <div class="transport">
        <span class="time">${formatTimecode(reviewViewState.playheadMs)}</span>
        <div class="scrubber" id="review-scrubber">
          <div class="played" style="width:0%"></div>
          <div class="head" style="left:0%"></div>
        </div>
        <span class="mono muted">${review.versions.length} version(s)</span>
      </div>
    </div>`;
}

/* ---- tabs --------------------------------------------------------------- */

function renderTabs(review) {
  const openCount = review.audit.open_comment_count;
  const isTranscript = reviewViewState.activeTab === "transcript";

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

  let runningMs = 0;
  const rows = review.transcript.map(entry => {
    const section = review.plan_sections.find(s => s.id === entry.section_id);
    const stamp = formatTimecode(runningMs);
    runningMs += (section?.estimated_seconds ?? 0) * 1000;
    const hasBody = entry.body.trim().length > 0;

    return `
      <button class="transcript-row" data-jump="${runningMs}">
        <span class="stamp">${stamp}</span>
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
  const { stageDefinitions } = applicationState;
  const previousStage = stageDefinitions[
    stageDefinitions.findIndex(s => s.key === stage.key) - 1];

  return `
    <div class="footer-nav">
      ${previousStage ? `
        <button class="btn" data-goto="${previousStage.key}">
          ${icon(ICON.arrowLeft)} Back to ${escapeHtml(previousStage.title)}
        </button>` : ""}
      <span class="plan-total" style="margin-left:14px">
        ${review.comments.length} comment(s) · ${review.chapters.length} chapter(s)
      </span>
      <div class="spacer"></div>
      <span class="muted" style="font-size:12.5px">Last stage</span>
    </div>`;
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

  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });
  select("#reviewing-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-review-tab]").forEach(tab => {
    tab.onclick = () => {
      reviewViewState.activeTab = tab.dataset.reviewTab;
      rerender();
    };
  });

  document.querySelectorAll("[data-jump]").forEach(row => {
    row.onclick = () => {
      reviewViewState.playheadMs = Number(row.dataset.jump) || 0;
      rerender();
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
