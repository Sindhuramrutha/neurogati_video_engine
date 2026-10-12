/**
 * The Render page: its own tab in the sidebar, before Studio.
 *
 * Rendering is minutes of work a section, so it is not a button that says
 * "Rendering..." (or, after a redraw, "Render video" again while three renders
 * run unseen). Modelled on an editor's Deliver page:
 *
 * - A bar: what is rendering, how far it has got, how long it has taken and
 *   roughly how long is left, with Pause and Delete.
 * - The render settings on the left (the voice) with "Add to render queue",
 *   and the queue on the right: every job with its status and what can be
 *   done to it -- reorder, pause, resume, retry, delete, watch.
 * - The sidebar's Render tab carries the state from any page: the percentage
 *   while one renders, how many wait, or "!" for one paused or failed.
 *
 * The queue is the server's (`/api/render-queue`); this only shows it and
 * asks it to act. A reload loses nothing: the job carries on, and the panel
 * finds it again.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import {
  applicationState, escapeHtml, select, showStageNotice, stageHeader,
} from "/static/ui-kit.js";

const FAST_POLL_MS = 1500;
const SLOW_POLL_MS = 5000;

let view = { jobs: [], paused: false, activity: [] };
let voices = null;
let chosenProvider = "";
let firstLook = true;
let pollTimer = null;
const finishedSeen = new Set();
// Set by the app: open Studio on a project and play one rendered file there.
let openInStudio = () => {};

const STATUS_LABELS = {
  rendering: "Rendering", queued: "Waiting", paused: "Paused", failed: "Failed", done: "Finished",
};

function clock(seconds) {
  const total = Math.max(0, Math.round(seconds));
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const rest = String(total % 60).padStart(2, "0");
  return hours ? `${hours}:${String(minutes).padStart(2, "0")}:${rest}` : `${minutes}:${rest}`;
}

/** Percent done, and a rough time left once enough is done to judge by. */
function measure(progress) {
  if (!progress?.active || !progress.total) {
    return { percent: null, left: "", elapsed: progress?.elapsed_seconds ?? 0 };
  }
  const fraction = Math.min(1, progress.done / progress.total);
  const left = fraction >= 0.05
    ? `~${clock((progress.elapsed_seconds * (1 - fraction)) / fraction)} left` : "estimating…";
  return { percent: Math.round(fraction * 100), left, elapsed: progress.elapsed_seconds };
}

function track(percent) {
  const known = percent !== null;
  return `
    <div class="stage-progress-track ${known ? "" : "unknown"}">
      <div class="stage-progress-fill" style="width:${known ? percent : 100}%"></div>
    </div>`;
}

/* ---- the bar -------------------------------------------------------------- */

function renderBar() {
  const rendering = view.jobs.find(job => job.status === "rendering");
  const count = status => view.jobs.filter(job => job.status === status).length;
  const chips = ["queued", "paused", "failed", "done"]
    .filter(status => count(status))
    .map(status => `<span class="rd-chip ${status}">${count(status)} ${
      STATUS_LABELS[status].toLowerCase()}</span>`).join("");

  let now;
  if (rendering) {
    const { percent, left, elapsed } = measure(rendering.progress);
    now = `
      <div class="rd-now">
        <div class="rd-now-text">
          <span>${escapeHtml(rendering.progress?.label || "Starting…")}</span>
        </div>
        ${track(percent)}
      </div>
      <span class="rd-numbers">${percent !== null ? `${percent}% · ` : ""}${clock(elapsed)}${
        left ? ` · ${left}` : ""}</span>
      <button class="btn" data-rd="pause" data-id="${rendering.id}"
              title="Stop after the section under way, keeping everything made so far">Pause</button>
      <button class="btn danger" data-rd="delete" data-id="${rendering.id}"
              title="Stop after the section under way and delete what it made">Delete</button>`;
  } else {
    const activity = view.activity[0];
    now = `<span class="rd-idle">${activity
      ? `${escapeHtml(activity.label || activity.job)}…`
      : view.paused ? "Queue on hold — nothing new starts."
      : count("queued") ? "Starting the next job…" : "Nothing rendering."}</span>`;
  }

  return `
    <div class="rd-bar">
      <b class="rd-title">Render queue</b>
      ${view.paused ? `<span class="rd-chip held">on hold</span>` : ""}
      ${chips}
      ${now}
    </div>`;
}

/* ---- the open panel ------------------------------------------------------- */

function renderSettings() {
  const project = applicationState.selectedProject;
  const providers = voices?.providers ?? [];
  chosenProvider ||= voices?.recommended ?? "";
  return `
    <section class="rd-settings">
      <h4>Render settings</h4>
      <label>Project
        <input type="text" value="${escapeHtml(project?.name ?? "No project selected")}" disabled>
      </label>
      <label>Voice
        <select data-rd-voice ${providers.length ? "" : "disabled"}>
          ${providers.map(provider => `
            <option value="${escapeHtml(provider.key)}" ${provider.key === chosenProvider ? "selected" : ""}
                    ${provider.is_available ? "" : "disabled"}>
              ${escapeHtml(provider.label)}${provider.is_available ? "" : " — unavailable"}</option>`).join("")}
        </select>
      </label>
      <p class="rd-hint">1920×1080 · 30 fps · MP4 (H.264, AAC)</p>
      <button class="btn btn-accent" data-rd="add" ${project ? "" : "disabled"}>
        Add to render queue</button>
      <div class="rd-queue-actions">
        <button class="btn" data-rd="hold">${view.paused ? "Release queue" : "Hold queue"}</button>
        <button class="btn" data-rd="clear" ${view.jobs.some(job => job.status === "done") ? "" : "disabled"}>
          Clear finished</button>
      </div>
    </section>`;
}

function jobDetail(job, index) {
  const sections = job.sections;
  const made = sections?.count
    ? `Narration ${sections.spoken}/${sections.count} · pictures ${sections.cut}/${sections.count}` : "";
  if (job.status === "rendering") {
    const { percent, left, elapsed } = measure(job.progress);
    return `
      <p class="rd-line">${escapeHtml(job.progress?.label || "Starting…")}</p>
      ${track(percent)}
      <p class="rd-line muted">${percent !== null ? `${percent}% · ` : ""}${clock(elapsed)} elapsed${
        left ? ` · ${left}` : ""}</p>`;
  }
  if (job.status === "queued") {
    const ahead = view.jobs.slice(0, index).filter(other =>
      other.status === "queued" || other.status === "rendering").length;
    return `<p class="rd-line muted">${ahead ? `${ahead} job(s) ahead of it` : "Next up"}${
      job.continues ? " · continues from where it stopped" : ""}</p>`;
  }
  if (job.status === "paused" || job.status === "failed") {
    return `
      ${made ? `<p class="rd-line">${made}</p>` : ""}
      ${job.message ? `<p class="rd-line ${job.status === "failed" ? "bad" : "muted"}">${
        escapeHtml(job.message)}</p>` : ""}
      ${job.partial_video ? `<button class="btn" data-rd="watch" data-slug="${escapeHtml(job.slug)}"
          data-file="${escapeHtml(job.partial_video)}"
          data-label="What was done before it paused: sections 1–${sections?.cut ?? "?"}">
          ▶ Watch what's done (sections 1–${sections?.cut ?? "?"})</button>` : ""}`;
  }
  return `
    <p class="rd-line">Finished in ${clock(job.render_seconds)} · video ${clock(job.duration_ms / 1000)}</p>
    ${job.message ? `<p class="rd-line muted">${escapeHtml(job.message)}</p>` : ""}`;
}

function jobActions(job) {
  const button = (action, label, extra = "") =>
    `<button class="btn ${extra}" data-rd="${action}" data-id="${job.id}">${label}</button>`;
  return {
    rendering: button("pause", "Pause") + button("delete", "Delete", "danger"),
    queued: button("up", "↑", "rd-small") + button("down", "↓", "rd-small")
      + button("pause", "Hold") + button("delete", "Delete", "danger"),
    paused: button("resume", "Resume", "btn-accent") + button("delete", "Delete", "danger"),
    failed: button("resume", "Retry", "btn-accent") + button("delete", "Delete", "danger"),
    done: (job.video_file ? `<button class="btn btn-accent" data-rd="watch"
             data-slug="${escapeHtml(job.slug)}" data-file="${escapeHtml(job.video_file)}"
             title="Play it in Studio">Watch in Studio</button>` : "") + button("delete", "Remove"),
  }[job.status] ?? "";
}

function renderQueue() {
  return `
    <section class="rd-jobs">
      <h4>Queue (${view.jobs.length})</h4>
      ${view.jobs.length ? view.jobs.map((job, index) => `
        <article class="rd-job ${escapeHtml(job.status)}">
          <div class="rd-job-head">
            <span class="rd-job-number">Job ${index + 1}</span>
            <b>${escapeHtml(job.project)}</b>
            <span class="rd-chip ${escapeHtml(job.status)}">${STATUS_LABELS[job.status] ?? job.status}</span>
          </div>
          ${jobDetail(job, index)}
          <div class="rd-job-actions">${jobActions(job)}</div>
        </article>`).join("")
        : `<p class="muted rd-empty">No renders yet. Choose the settings and add this project.</p>`}
    </section>`;
}

/* ---- drawing, polling and acting ------------------------------------------ */

const dock = () => select("#render-dock");

/** The Render page: the header, then the queue's bar, settings and jobs. */
export function renderRenderPage(stage) {
  select("#stage-body").innerHTML = `
    ${stageHeader("render", stage.title)}
    <section class="render-dock" id="render-dock" aria-label="Render queue">
      <div class="rd-bar-slot">${renderBar()}</div>
      <div class="rd-body">${renderSettings() + renderQueue()}</div>
    </section>`;
  ensureVoices().then(paint);
  poll();
}

/** The sidebar tab's badge: the state of the queue, seen from any page. */
export function paintRenderNavBadge() {
  const badge = select("#render-nav-badge");
  if (!badge) return;
  const rendering = view.jobs.find(job => job.status === "rendering");
  const waiting = view.jobs.filter(job => job.status === "queued").length;
  const stuck = view.jobs.some(job => job.status === "paused" || job.status === "failed");
  const { percent } = measure(rendering?.progress);
  badge.textContent = rendering ? (percent !== null ? `${percent}%` : "…")
    : waiting ? String(waiting) : stuck ? "!" : "";
  badge.hidden = !badge.textContent;
  badge.className = `nav-badge render-badge ${rendering ? "rendering" : stuck ? "stuck" : ""}`;
  badge.title = rendering ? `Rendering ${rendering.project}`
    : waiting ? `${waiting} waiting` : stuck ? "A render is paused or failed" : "";
}

function paint() {
  paintRenderNavBadge();
  const root = dock();
  if (!root) return;
  root.querySelector(".rd-bar-slot").innerHTML = renderBar();
  // Not while the voice list is in use: a repaint would close it.
  if (document.activeElement?.closest?.(".rd-body select") == null) {
    root.querySelector(".rd-body").innerHTML = renderSettings() + renderQueue();
  }
}

function announce(previous) {
  const rendering = view.jobs.find(job => job.status === "rendering");
  if (firstLook && rendering) {
    showStageNotice("ok", `A render of ${rendering.project} is running on the server — `
      + "reloading the page did not stop it. Follow it on the Render tab.");
  }
  for (const job of view.jobs) {
    const was = previous.jobs.find(other => other.id === job.id)?.status;
    if (job.status === "done" && was && was !== "done" && !finishedSeen.has(job.id)) {
      finishedSeen.add(job.id);
      showStageNotice("ok", `Render finished: ${job.project}. Watch it from the Render tab, `
        + "or in Reviewing.");
      window.dispatchEvent(new CustomEvent("render-finished", { detail: { slug: job.slug } }));
    }
    if (job.status === "failed" && was === "rendering") {
      showStageNotice("bad", `Render failed: ${job.project} — ${job.message}`);
    }
  }
  firstLook = false;
}

async function poll() {
  clearTimeout(pollTimer);
  const previous = view;
  try {
    view = await requestJsonFromApi("/api/render-queue");
    announce(previous);
    paint();
  } catch (pollFailure) {
    console.warn("render queue poll failed", pollFailure);
  }
  const busy = view.jobs.some(job => job.status === "rendering" || job.status === "queued");
  pollTimer = setTimeout(poll, busy ? FAST_POLL_MS : SLOW_POLL_MS);
}

async function send(path, body) {
  view = await requestJsonFromApi(`/api/render-queue${path}`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body ?? {}),
  });
  paint();
  poll();
}

/** Put the project on screen in the queue with the chosen voice; `show`
 *  then opens the Render tab, where it can be followed. */
export async function addToRenderQueue(show = null) {
  const project = applicationState.selectedProject;
  if (!project) return;
  try {
    await ensureVoices();
    await send("", { slug: project.slug, voice_provider: chosenProvider });
    showStageNotice("ok", `${project.name} is in the render queue.`);
  } catch (failure) {
    console.error("adding to the render queue failed", failure);
    showStageNotice("bad", failure.message);
  }
  show?.();
}

async function ensureVoices() {
  if (voices) return;
  try {
    voices = await requestJsonFromApi("/api/voices");
  } catch (voicesFailure) {
    console.warn("could not list voices", voicesFailure);
    voices = { providers: [], recommended: "" };
  }
}

async function act(action, id, button) {
  if (action === "watch") {
    return openInStudio(button.dataset.slug, button.dataset.file, button.dataset.label ?? "");
  }
  const confirmations = {
    delete: view.jobs.find(job => job.id === id)?.status === "done"
      ? "" : "Delete this job and everything it has made so far?",
  };
  if (confirmations[action] && !window.confirm(confirmations[action])) return;
  if (action === "add") return addToRenderQueue();
  if (action === "hold") return send("/hold", { paused: !view.paused });
  if (action === "clear") return send("/clear-finished");
  if (action === "up" || action === "down") {
    return send(`/${encodeURIComponent(id)}/move?step=${action === "up" ? -1 : 1}`);
  }
  await send(`/${encodeURIComponent(id)}/${action}`);
  if (action === "pause") {
    showStageNotice("ok", "Pausing after the section under way. Everything made so far is kept.");
  }
}

export function startRenderDock({ watch } = {}) {
  if (watch) openInStudio = watch;
  // Delegated from the document: the page is drawn again on every visit.
  document.addEventListener("click", async event => {
    const button = event.target.closest("#render-dock [data-rd]");
    if (!button) return;
    button.disabled = true;
    try {
      await act(button.dataset.rd, button.dataset.id, button);
    } catch (failure) {
      console.error("render queue action failed", failure);
      showStageNotice("bad", failure.message);
    } finally {
      if (button.isConnected) button.disabled = false;
    }
  });
  document.addEventListener("change", event => {
    if (event.target.matches("[data-rd-voice]")) chosenProvider = event.target.value;
  });
  poll();
}
