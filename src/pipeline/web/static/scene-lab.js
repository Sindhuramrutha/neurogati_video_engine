/**
 * Scripted scenes on the Generation page: a folder and a `scene.py` per scene.
 *
 * - The bar on the Make tab says how many scripted scenes are waiting, and what
 *   writing them will cost, before anything is sent.
 * - The scene panel is the scene's folder on screen: its clip, the fixed checks
 *   it went through, the script (editable, runnable), what it printed, the
 *   brief it was given and every outside resource it used.
 * - The resource library on the Setup tab is what the agent is shown each time
 *   it writes a scene; adding a file there is how it learns a technique.
 *
 * Every scene is made by its agent, on the server (`scene_agent.py`): it writes,
 * renders, looks at its own frames and improves the scene until the checks pass
 * and the review says it teaches. Nothing waits on a question. Its steps and a
 * Stop button are on the scene panel; the
 * page refreshes itself while agents work. A clip that fails a check is never used.
 */

import { mountCodeEditor } from "/static/code-editor.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, hideProgress, icon, projectApiPath, refreshProjectSummary,
  showProgress, showStageNotice,
} from "/static/ui-kit.js";

export const sceneLabState = {
  openId: null, navigate: null, agents: null, poll: null,
  sectionOpen: {},      // section id -> what the person chose; absent: the default
  drafts: {},           // scene id -> its script as edited and not yet saved
  editor: null,         // the open scene's code editor
};

const AGENT_LABELS = {
  idle: "Not started", queued: "Queued", working: "Being made", done: "Made",
  stopped: "Stopped", failed: "Could not be made",
  interrupted: "Interrupted (the app restarted) — Make the missing resumes it",
};

/** Every scene's agent at a glance (for the bar and the cards). */
export async function loadAgents() {
  try {
    sceneLabState.agents = await requestJsonFromApi(projectApiPath("/scene-agents"));
  } catch (failure) {
    console.error("could not read the scene agents", failure);
    sceneLabState.agents = null;
  }
  return sceneLabState.agents;
}

export const agentOf = visualId =>
  sceneLabState.agents?.scenes?.find(scene => scene.id === visualId) ?? null;

/** While any agent works, look again in a few seconds -- never while you type. */
export function keepWatching(rerender) {
  clearTimeout(sceneLabState.poll);
  if (!sceneLabState.agents?.running) return;
  sceneLabState.poll = setTimeout(() => {
    const typing = ["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName);
    if (typing) keepWatching(rerender);
    else rerender();
  }, 4000);
}

const CHECK_LABELS = { pass: "Pass", warn: "Warning", fail: "Fails" };
const RESOURCE_KINDS = [
  ["code", "Code", "Python the scripts can import", ".py"],
  ["methods", "Methods", "How-to notes and worked examples the agent reads", ".md,.py,.txt"],
  ["assets", "Assets", "Pictures, icons, fonts and data the scripts can use",
   ".png,.jpg,.jpeg,.webp,.svg,.gif,.ttf,.otf,.json,.csv,.mp3,.wav"],
];

const sceneFileUrl = (visualId, name, stamp = "") =>
  projectApiPath(`/scenes/${encodeURIComponent(visualId)}/files/${name}`)
  + (stamp ? `?v=${encodeURIComponent(stamp)}` : "");

export const scenePosterUrl = visual => sceneFileUrl(visual.id, "poster.png", visual.built_at);

/** Fetch the open scene's folder, if one is open. */
export async function loadOpenScene() {
  if (!sceneLabState.openId) return null;
  try {
    return await requestJsonFromApi(
      projectApiPath(`/scenes/${encodeURIComponent(sceneLabState.openId)}`));
  } catch (failure) {
    console.error("could not read the scene", failure);
    sceneLabState.openId = null;
    return null;
  }
}

/* ---- the bar on the Make tab ------------------------------------------------- */

export function renderScriptedBar(preview) {
  if (!preview.scenes) return "";
  const agents = sceneLabState.agents
    ?? { running: 0, working: 0, queued: 0, interrupted: 0, failed: 0, scenes: [] };
  const missing = preview.waiting;
  const passed = preview.passed;
  const toApprove = passed - preview.approved;
  const busy = agents.running > 0;
  const line = busy
    ? `${agents.working} being made, ${agents.queued} queued (${agents.at_once} at a time, in
       order, on the server). You can leave this page.`
    : agents.interrupted
      ? `${agents.interrupted} were interrupted by a restart: making the missing scenes resumes them.`
      : missing ? "Each missing scene is made by its own agent, which keeps improving it until it is good."
        : toApprove ? "Watch a scene's preview, then approve it — or approve every passed one at once."
          : "Every scene passed and is approved: the render uses their clips.";
  return `
    <div class="run-bar ${!missing && !toApprove ? "ready" : "stale"} scripted-bar">
      <span class="run-text">
        <b>${preview.scenes} scenes: ${passed} passed, ${missing} still to make</b>
        <span>${line}</span>
      </span>
      <span class="plan-actions">
        ${missing && !busy ? `<button class="btn btn-accent" id="make-scenes-button">
          Make the ${missing} missing <span class="fact warn">AI</span></button>` : ""}
        ${toApprove ? `<button class="btn ${missing ? "" : "btn-accent"}"
            id="approve-passed-button" data-count="${toApprove}">
            Approve ${toApprove} passed</button>` : ""}
        ${busy ? `<button class="btn" id="stop-all-button"
            title="Working agents stop after the step they are on; the queue is dropped. Nothing is deleted.">
            Stop all</button>` : ""}
        <button class="btn" id="plan-visuals-button"
                title="Read the transferred script again: new scenes are added, gone ones removed, unchanged ones keep their programs. No model is called.">
          Set up again</button>
        <button class="btn" id="rebuild-visuals-button"
                title="Every scene's agent starts again from a fresh conversation">
          Remake all <span class="fact warn">AI</span></button>
      </span>
    </div>`;
}

/* ---- every scene at a glance -------------------------------------------------------- */

// In the order a scene goes through them; what its agent is doing now comes first.
const SCENE_STATES = [
  ["approved", "Approved"],
  ["passed", "Passed, to watch"],
  ["working", "Being made"],
  ["queued", "Queued"],
  ["stopped", "Stopped or failed"],
  ["waiting", "Not started"],
];

function sceneState(visual) {
  const status = agentOf(visual.id)?.status;
  if (status === "working" || status === "queued") return status;
  if (visual.approved_at) return "approved";
  if (visual.clip_path) return "passed";
  if (["failed", "stopped", "interrupted"].includes(status)) return "stopped";
  return "waiting";
}

/** The scenes in rows, one collapsible row per section of the video. A row shows its
 *  title, how many of its scenes are where, and a dot for each scene; it is open when
 *  a scene in it is being made, unless the person opened or closed it themselves. */
export function renderSceneSections(visuals, renderCard) {
  const sections = [];
  for (const visual of visuals) {
    let section = sections.at(-1);
    if (!section || section.id !== visual.section_id) {
      section = { id: visual.section_id, title: visual.section_title, scenes: [] };
      sections.push(section);
    }
    section.scenes.push(visual);
  }
  return sections.map(section => {
    const states = section.scenes.map(sceneState);
    const counts = SCENE_STATES
      .map(([key, label]) => [label, states.filter(state => state === key).length])
      .filter(([, count]) => count);
    const byDefault = sections.length === 1 || states.includes("working");
    const open = sceneLabState.sectionOpen[section.id] ?? byDefault;
    return `
      <details class="scene-section" data-section="${escapeHtml(section.id)}"
               data-default="${byDefault ? "open" : "closed"}" ${open ? "open" : ""}>
        <summary>
          <span class="scene-section-title">${escapeHtml(section.title || "Untitled section")}</span>
          <span class="scene-section-dots">${states.map(state => `
            <i class="scene-status-dot ${state}"></i>`).join("")}</span>
          <span class="muted">${section.scenes.length} scene(s) ·
            ${counts.map(([label, count]) => `${count} ${label.toLowerCase()}`).join(" · ")}</span>
        </summary>
        <div class="shot-grid">${section.scenes.map(renderCard).join("")}</div>
      </details>`;
  }).join("");
}

/** One bar across all the scenes, coloured by where each one is, with the counts. */
export function renderSceneStatus(visuals) {
  if (!visuals.length) return "";
  const counts = Object.fromEntries(SCENE_STATES.map(([key]) => [key, 0]));
  visuals.forEach(visual => { counts[sceneState(visual)] += 1; });
  const shown = SCENE_STATES.filter(([key]) => counts[key]);
  return `
    <div class="scene-status" aria-label="Where every scene is">
      <div class="scene-status-bar">
        ${shown.map(([key, label]) => `
          <span class="scene-status-part ${key}" style="flex:${counts[key]}"
                title="${escapeHtml(label)}: ${counts[key]}"></span>`).join("")}
      </div>
      <div class="scene-status-key">
        ${shown.map(([key, label]) => `
          <span><i class="scene-status-dot ${key}"></i>${escapeHtml(label)}
            <b>${counts[key]}</b></span>`).join("")}
        <span class="muted">of ${visuals.length} scene(s)</span>
      </div>
    </div>`;
}

/* ---- the scene panel ------------------------------------------------------------ */

/** What the agent is doing now, and the box to ask it for a change: always in view. */
function renderAgentControls(scene) {
  const agent = scene.agent ?? { status: "idle", events: [], remarks: [] };
  const busy = agent.running || ["queued", "working"].includes(agent.status);
  return `
    <div class="scene-agent ${escapeHtml(agent.status)}">
      <div class="scene-agent-head">
        <b>${escapeHtml(AGENT_LABELS[agent.status] ?? agent.status)}</b>
        ${busy && agent.doing ? `<span class="muted">${escapeHtml(agent.doing)}…</span>` : ""}
        <div class="spacer"></div>
        ${busy ? `<button class="btn" id="stop-agent-button">Stop</button>` : ""}
      </div>
      ${agent.status === "failed" ? `<p class="panel-sub">${escapeHtml(agent.error)}</p>` : ""}
      ${renderChat(agent)}
      ${!busy ? `
        <div class="scene-actions">
          <input id="scene-instruction" maxlength="600"
                 placeholder="${scene.code ? "What to change, in your own words" : "Anything it should know (optional)"}">
          <button class="btn ${scene.code ? "" : "btn-accent"}" id="agent-scene-button">
            ${scene.code ? "Change it" : "Make it"} <span class="fact warn">AI</span></button>
        </div>` : ""}
    </div>`;
}

const CHAT_WHEN = at => (at ? new Date(at).toLocaleString([], {
  day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }) : "");

/** Every ask of this scene and how it ended, oldest first, like a chat. */
function renderChat(agent) {
  const turns = agent.conversation ?? [];
  if (!turns.length) return "";
  const last = turns.length - 1;
  return `
    <div class="scene-chat" id="scene-chat">${turns.map((turn, index) => `
      <div class="chat-turn asked">${turn.asked
        ? escapeHtml(turn.asked) : "<i>Make it</i>"}<span class="chat-when">${
        escapeHtml(CHAT_WHEN(turn.at))}</span></div>
      <div class="chat-turn answer ${escapeHtml(turn.status)}">${turn.answer
        ? escapeHtml(turn.answer) : `<i>${agent.running
          ? `${escapeHtml(agent.doing || "Working on it")}…` : "Interrupted before it finished."}</i>`}${
        index === last && turn.status === "done" && agent.summary
          ? `

<b>It made:</b> ${escapeHtml(agent.summary)}` : ""}${turn.ended_at
        ? `<span class="chat-when">${escapeHtml(CHAT_WHEN(turn.ended_at))}</span>` : ""}</div>`).join("")}
    </div>`;
}

/** The scene's script, in a real editor: edited by hand, saved and run from here. */
function renderCodeEditor(scene) {
  const draft = sceneLabState.drafts[scene.visual.id];
  const code = draft ?? scene.code;
  return `
    <div class="scene-code-wrap" id="scene-code-wrap">
      <div class="scene-code-bar">
        <label class="scene-label" for="scene-code">${escapeHtml(scene.entry)}</label>
        <span class="fact warn" id="code-unsaved" ${draft === undefined ? "hidden" : ""}>
          Unsaved changes</span>
        <div class="spacer"></div>
        <span class="muted code-keys">Ctrl+S save and run · Ctrl+F find · Ctrl+/ comment</span>
        <button class="btn" id="code-revert-button" ${draft === undefined ? "hidden" : ""}>
          Undo my changes</button>
        <button class="btn" id="code-full-button">Full screen</button>
        <button class="btn btn-accent" id="run-scene-button" ${code.trim() ? "" : "disabled"}>
          Save and run</button>
      </div>
      <textarea id="scene-code" class="scene-code" spellcheck="false"
        placeholder="No script yet. Have the agent write one, or write it here.">${escapeHtml(code)}</textarea>
      <textarea id="scene-code-saved" hidden>${escapeHtml(scene.code)}</textarea>
      <p class="panel-sub">Saved edits are this scene's program until it is made again: asking
        the agent to change it, or remaking it, writes it afresh from its shots.</p>
    </div>`;
}

/** What the agent made and how: its record, read when wanted. */
function renderAgentRecord(scene) {
  const agent = scene.agent ?? { status: "idle", events: [], remarks: [] };
  const busy = agent.running || ["queued", "working"].includes(agent.status);
  const tokens = (agent.tokens?.prompt ?? 0) + (agent.tokens?.completion ?? 0);
  return `
    <p class="panel-sub">${agent.renders} render(s) · ${agent.calls?.agent ?? 0} write and
      ${agent.calls?.vision ?? 0} review call(s) · ${tokens.toLocaleString()} tokens this run</p>
    ${agent.status === "done" && agent.summary ? `
      <p class="panel-sub"><b>It made:</b> ${escapeHtml(agent.summary)}</p>` : ""}
    ${agent.remarks?.length ? `
      <div class="agent-remarks"><b>The reviewer's remarks</b>
        <ul>${agent.remarks.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul></div>` : ""}
    ${agent.events.length ? `
      <details class="agent-steps" ${busy ? "open" : ""}>
        <summary>What it did (${agent.events.length} step(s))</summary>
        <ol>${agent.events.slice().reverse().map(event => `
          <li><span class="agent-step-kind">${escapeHtml(event.kind.replaceAll("_", " "))}</span>
            ${escapeHtml(event.text)}</li>`).join("")}</ol>
      </details>` : ""}`;
}

/**
 * The open scene, in the side panel: its video, whether it passed, the box to ask
 * for a change and its background switch in view; everything else -- the reviewer's
 * remarks, the agent's steps, its checks, its program -- folded under Details.
 */
export function renderScenePanel(scene) {
  if (!scene) return "";
  const { visual, checks } = scene;
  const failing = checks.filter(check => check.status === "fail").length;
  const state = !scene.code ? ["blocked", "No program yet"]
    : !checks.length ? ["pending", "Not run yet"]
      : failing ? ["stale", `${failing} check(s) fail: this scene cannot be rendered`]
        : visual.approved_at ? ["ready", "Approved: the render uses this program's clip"]
          : ["pending", "Passed every check: watch the preview, then approve it"];
  const spec = scene.spec ?? {};
  const range = scene.brief.time_range;
  return `
    <section class="panel scene-panel" data-scene="${escapeHtml(visual.id)}">
      <div class="scene-panel-head">
        <button class="btn btn-icon-text" id="previous-scene-button" title="The scene before (←)"
                aria-label="Previous scene">← Previous</button>
        <div>
          <h3>${escapeHtml(visual.section_title)} · scene ${visual.scene_number}</h3>
          <p class="mono">${escapeHtml(scene.folder || "No folder yet: it is made with the first script.")}</p>
        </div>
        <div class="spacer"></div>
        <button class="btn btn-icon-text" id="next-scene-button" title="The scene after (→)"
                aria-label="Next scene">Next →</button>
        <button class="btn" id="close-scene-button">Close</button>
      </div>
      <div class="scene-player">
          ${scene.has_preview
            ? `<video class="scene-clip" controls preload="metadata"
                 src="${sceneFileUrl(visual.id, "preview.mp4", scene.checked_at)}"></video>`
            : scene.has_clip
              ? `<video class="scene-clip" controls muted preload="metadata"
                   src="${sceneFileUrl(visual.id, "render.mp4", scene.checked_at)}"></video>
                 <p class="panel-sub">Its clip, silent: it did not pass, so it has no preview.</p>`
              : `<div class="scene-clip scene-clip-empty">No clip yet</div>`}
      </div>
      <div class="final-head ${state[0]} scene-state"><span class="run-text"><b>${state[1]}</b>
        <span>${escapeHtml(visual.note || "")}</span></span>
        ${!failing && checks.length && scene.has_clip ? `
          <button class="btn ${visual.approved_at ? "" : "btn-accent"}" id="approve-scene-button"
                  data-approved="${visual.approved_at ? "1" : ""}">
            ${visual.approved_at ? "Withdraw approval" : "Approve this scene"}</button>` : ""}
        ${scene.has_preview ? `<button class="btn" id="studio-scene-button">Play in Studio</button>` : ""}
      </div>

      ${renderAgentControls(scene)}
      ${scene.background?.kind ? `
        <div class="bg-toggle-row">
          <span class="bg-toggle-label">Background</span>
          <div class="pill-toggle" role="radiogroup" aria-label="The scene's background">
            ${[[true, "With background"], [false, "Plain"]].map(([on, label]) =>
              on === Boolean(scene.background.on)
                ? `<button class="pill-option on" role="radio" aria-checked="true" disabled>${label}</button>`
                : `<button class="pill-option" role="radio" aria-checked="false"
                     id="background-scene-button" data-on="${scene.background.on ? "1" : ""}">${label}</button>`
            ).join("")}
          </div>
        </div>` : ""}

      <details class="scene-code-row" ${sceneLabState.codeOpen ? "open" : ""}>
        <summary>Code — ${escapeHtml(scene.entry)}, the scene's Python program${
          sceneLabState.drafts[visual.id] !== undefined ? " · unsaved changes" : ""}</summary>
        ${renderCodeEditor(scene)}
      </details>

      <details class="scene-details" ${sceneLabState.detailsOpen ? "open" : ""}>
        <summary>Details — the reviewer's remarks, its steps, checks and log</summary>
        ${renderAgentRecord(scene)}
        <dl class="scene-spec">
          <dt>Renderer</dt><dd>${escapeHtml(spec.renderer || "not chosen yet")}${
            spec.approach ? ` — ${escapeHtml(spec.approach)}` : ""}</dd>
          <dt>Narration</dt><dd>${scene.brief.narration_measured
            ? `${scene.brief.seconds} s, measured from its voice` : "not measured yet"}${range
            ? ` · ${range.start}–${range.end} s into its section${range.earlier_scenes_measured
              ? "" : " (earlier scenes estimated)"}` : ""}</dd>
          <dt>Source assets</dt><dd>${(spec.assets_used ?? []).length
            ? spec.assets_used.map(a => escapeHtml(a.split(/[\\/]/).pop())).join(", ")
            : "none used"}${scene.brief.assets?.pictures?.length
            ? ` · ${scene.brief.assets.pictures.length} approved picture(s) offered` : ""}</dd>
          ${scene.background?.kind ? `<dt>Background</dt><dd>${scene.background.kind === "image"
            ? `Painted: ${escapeHtml(scene.background.describe)}`
            : `Gradient: ${escapeHtml((scene.background.colours ?? []).join(", "))}`}</dd>` : ""}
        </dl>
        ${(spec.beats ?? []).length ? `
          <details class="scene-beats"><summary>Its ${spec.beats.length} visual beats</summary>
            <ol>${spec.beats.map(beat => `<li><b>“${escapeHtml(beat.when_said)}”</b> — ${
              escapeHtml(beat.shows)}</li>`).join("")}</ol>
          </details>` : ""}
        ${checks.length ? `
          <table class="assets-rule-table plan-checks scene-checks">
            <tbody>${checks.map(check => `
              <tr><td><span class="plan-check ${check.status}">${CHECK_LABELS[check.status]}</span></td>
                <td><b>${escapeHtml(check.name)}</b><br><span class="muted">${escapeHtml(check.detail)}</span></td>
              </tr>`).join("")}</tbody>
          </table>` : ""}
        <details class="scene-brief">
          <summary>What the script is told (brief.json)</summary>
          <p><b>Said:</b> ${escapeHtml(scene.brief.narration ?? visual.narration_preview)}</p>
          <p><b>On screen:</b> ${escapeHtml(scene.brief.on_screen ?? visual.brief)}</p>
        </details>
        ${scene.log ? `<details class="scene-log"><summary>What it printed (log.txt)</summary>
          <pre>${escapeHtml(scene.log)}</pre></details>` : ""}
      </details>
    </section>`;
}

/** The editor's buttons, and the draft kept while it is not saved. */
function wireCodeEditor(openId, busy) {
  sceneLabState.editor = null;
  const area = document.querySelector("#scene-code");
  const run = document.querySelector("#run-scene-button");
  if (!area || !run) return;
  sceneLabState.savedCode = document.querySelector("#scene-code-saved")?.value ?? "";
  const codeNow = () => sceneLabState.editor?.getValue() ?? area.value;
  const changed = text => {
    if (sceneLabState.openId !== openId) return;
    if (text === sceneLabState.savedCode) delete sceneLabState.drafts[openId];
    else sceneLabState.drafts[openId] = text;
    const unsaved = sceneLabState.drafts[openId] !== undefined;
    document.querySelector("#code-unsaved")?.toggleAttribute("hidden", !unsaved);
    document.querySelector("#code-revert-button")?.toggleAttribute("hidden", !unsaved);
    run.disabled = !text.trim();
  };
  const save = () => {
    if (run.disabled) return;
    fullScreen(false);
    busy(run, "Saving and running the scene's script", async () => {
      const scene = await post(`/scenes/${encodeURIComponent(openId)}/run`, { code: codeNow() });
      delete sceneLabState.drafts[openId];        // saved: the file is the code now
      return scene;
    });
  };
  const wrap = document.querySelector("#scene-code-wrap");
  const full = document.querySelector("#code-full-button");
  const fullScreen = on => {
    wrap?.classList.toggle("full", on);
    if (full) full.textContent = on ? "Exit full screen" : "Full screen";
    sceneLabState.editor?.refresh();
    if (on) sceneLabState.editor?.focus();
  };
  sceneLabState.fullScreen = fullScreen;
  if (full) full.onclick = () => fullScreen(!wrap.classList.contains("full"));
  run.onclick = save;
  area.addEventListener("input", () => changed(area.value));   // until the editor loads
  document.querySelector("#code-revert-button").onclick = () => {
    delete sceneLabState.drafts[openId];
    if (sceneLabState.editor) sceneLabState.editor.setValue(sceneLabState.savedCode ?? "");
    else area.value = sceneLabState.savedCode ?? "";
    changed(codeNow());
  };
  mountCodeEditor(area, { onChange: changed, onSave: save })
    .then(editor => { if (editor) sceneLabState.editor = editor; })
    .catch(failure => console.error(failure));      // the plain box still works
}

/* ---- the resource library ------------------------------------------------------- */

export function renderResourceLibrary(resources) {
  if (!resources) return "";
  return `
    <section class="panel resource-library" style="margin-top:16px">
      <div class="panel-head"><h3>The resource library</h3></div>
      <p class="panel-sub">What every scene script can draw on. The agent is shown this each
        time it writes a scene, so a file added here is something it can use next time.</p>
      <div class="resource-kinds">
        ${RESOURCE_KINDS.map(([kind, name, does, accept]) => `
          <div class="resource-kind">
            <b>${name}</b><span class="muted">${does}</span>
            ${(resources[kind] ?? []).map(entry => `
              <div class="resource-row">
                <span class="x-pick-name">${escapeHtml(entry.name)}</span>
                <span class="muted">${escapeHtml(entry.about)}</span>
                <button class="btn-icon danger" data-remove-resource="${kind}"
                        data-name="${escapeHtml(entry.name)}" title="Remove" aria-label="Remove">
                  ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 13, 2)}</button>
              </div>`).join("") || `<span class="muted">Nothing yet.</span>`}
            <label class="btn">Add<input type="file" hidden accept="${accept}"
              data-add-resource="${kind}"></label>
          </div>`).join("")}
      </div>
      <p class="scene-warning">${icon(ICON.alert, 15, 2.2)} A scene script is a program. It
        runs on this computer with your permissions, in its scene's folder, with a time limit,
        and it may download open resources, which it records with their licence. Read a
        script before trusting it with anything that matters.</p>
    </section>`;
}

/* ---- acting ------------------------------------------------------------------------ */

const post = (path, body) => requestJsonFromApi(projectApiPath(path), {
  method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body ?? {}),
});

const summarise = scene => {
  const failing = scene.checks.filter(check => check.status === "fail");
  return failing.length
    ? ["warn", `It ran, and fails ${failing.length} check(s): ${failing[0].name} — ${failing[0].detail}`]
    : ["ok", "It ran and passed its checks. The clip is what this scene shows."];
};

export function wireSceneLab(rerender, visuals) {
  // A section opened or closed by hand stays so through the page's own refreshes.
  document.querySelectorAll("details.scene-section").forEach(row => {
    row.addEventListener("toggle", () => {
      const byDefault = row.dataset.default === "open";
      if (row.open === byDefault && !(row.dataset.section in sceneLabState.sectionOpen)) return;
      sceneLabState.sectionOpen[row.dataset.section] = row.open;
    });
  });

  document.querySelectorAll("[data-open-scene]").forEach(button => {
    button.onclick = async () => {
      sceneLabState.openId = button.dataset.openScene;
      await rerender();      // it opens in the side panel, the list staying where it was
    };
  });
  const closeScene = () => { sceneLabState.openId = null; rerender(); };
  // Previous and next: the scenes in the video's order, one step either way.
  const order = (visuals?.visuals ?? []).map(visual => visual.id);
  const at = order.indexOf(sceneLabState.openId);
  const step = async by => {
    const next = order[at + by];
    if (!next) return;
    sceneLabState.openId = next;
    await rerender();
  };
  const previous = document.querySelector("#previous-scene-button");
  const following = document.querySelector("#next-scene-button");
  if (previous) { previous.disabled = at <= 0; previous.onclick = () => step(-1); }
  if (following) { following.disabled = at < 0 || at >= order.length - 1; following.onclick = () => step(1); }
  sceneLabState.step = step;
  const chat = document.getElementById("scene-chat");
  if (chat) chat.scrollTop = chat.scrollHeight;          // the latest turn, as a chat opens
  const details = document.querySelector(".scene-details");
  if (details) details.addEventListener("toggle", () => {
    sceneLabState.detailsOpen = details.open;
    sceneLabState.editor?.refresh();           // drawn while folded, it has no size yet
  });
  const codeRow = document.querySelector(".scene-code-row");
  if (codeRow) codeRow.addEventListener("toggle", () => {
    sceneLabState.codeOpen = codeRow.open;
    sceneLabState.editor?.refresh();
  });
  const close = document.querySelector("#close-scene-button");
  if (close) close.onclick = closeScene;
  const backdrop = document.querySelector("#scene-drawer-backdrop");
  if (backdrop) backdrop.onclick = closeScene;
  sceneLabState.close = closeScene;
  if (!sceneLabState.escapes) {           // one listener for the page's life
    sceneLabState.escapes = true;
    document.addEventListener("keydown", event => {
      if (!sceneLabState.openId) return;
      const wrap = document.querySelector("#scene-code-wrap");
      if (event.key === "Escape" && wrap?.classList.contains("full")) {
        sceneLabState.fullScreen?.(false);        // out of full screen, not out of the scene
        return;
      }
      if (event.key === "Escape" && event.target.closest?.(".CodeMirror, .CodeMirror-dialog")) return;
      if (event.key === "Escape") sceneLabState.close?.();
      // The arrows step through the scenes, but never while typing.
      const typing = ["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName);
      if (!typing && event.key === "ArrowLeft") sceneLabState.step?.(-1);
      if (!typing && event.key === "ArrowRight") sceneLabState.step?.(1);
    });
  }

  const openId = sceneLabState.openId;
  const busy = async (button, label, work) => {
    button.disabled = true;
    showProgress({ label });
    try {
      const scene = await work();
      if (scene?.checks) showStageNotice(...summarise(scene));
      await refreshProjectSummary();
    } catch (failure) {
      console.error("scene action failed", failure);
      showStageNotice("bad", failure.message);
    } finally {
      hideProgress();
    }
    await rerender();
  };

  const approve = document.querySelector("#approve-scene-button");
  if (approve) approve.onclick = () => busy(approve,
    approve.dataset.approved ? "Withdrawing the approval" : "Approving the scene",
    () => post(`/scenes/${encodeURIComponent(openId)}/approve`,
      { approved: !approve.dataset.approved }));

  const studio = document.querySelector("#studio-scene-button");
  if (studio) studio.onclick = () => {
    applicationState.studioWatch = {
      slug: applicationState.selectedProject?.slug, kind: "scene",
      url: sceneFileUrl(openId, "preview.mp4", String(Date.now())),
      label: document.querySelector(".scene-panel h3")?.textContent ?? "Scene preview",
    };
    sceneLabState.navigate?.("studio");
  };

  // The scene is drawn again, with its background or without it.
  const background = document.querySelector("#background-scene-button");
  if (background) background.onclick = () => busy(background,
    background.dataset.on ? "Drawing the scene without its background"
      : "Drawing the scene with its background",
    () => post(`/scenes/${encodeURIComponent(openId)}/background`,
      { on: !background.dataset.on }));

  wireCodeEditor(openId, busy);

  const startAgents = async (button, body, notice) => {
    button.disabled = true;
    try {
      await post("/scene-agents", body);
      showStageNotice("ok", notice);
    } catch (failure) {
      showStageNotice("bad", failure.message);
    }
    await loadAgents();
    await rerender();
  };

  const agentScene = document.querySelector("#agent-scene-button");
  if (agentScene) agentScene.onclick = () => {
    const instruction = document.querySelector("#scene-instruction").value.trim();
    if (!window.confirm("Make this scene?\n\nIt is written, rendered, checked, reviewed and "
        + "fixed, for up to 6 rounds — paid model calls.")) return undefined;
    return startAgents(agentScene, { visual_ids: [openId], instruction },
      "It is being made on the server. Its steps appear here as it goes.");
  };

  const stop = document.querySelector("#stop-agent-button");
  if (stop) stop.onclick = async () => {
    stop.disabled = true;
    await post(`/scenes/${encodeURIComponent(openId)}/agent/stop`, {});
    showStageNotice("ok", "It stops after the step it is on.");
    await loadAgents();
    await rerender();
  };

  const makeAll = document.querySelector("#make-scenes-button");
  if (makeAll) makeAll.onclick = () => {
    const waiting = visuals.visuals.filter(v => !v.clip_path);
    if (!window.confirm(`Make ${waiting.length} scene(s)?\n\nEach is written, rendered, checked, `
        + "reviewed by looking at its frames, and fixed — up to 6 rounds, in the video's "
        + "order, a few at a time, on the server. Paid model calls. You can leave this page; "
        + "nothing will stop to ask you.")) return undefined;
    return startAgents(makeAll, {}, `${waiting.length} scene(s) are being made on the server.`);
  };

  const stopAll = document.querySelector("#stop-all-button");
  if (stopAll) stopAll.onclick = async () => {
    stopAll.disabled = true;
    try {
      const done = await post("/scene-agents/stop", {});
      showStageNotice("ok", `${done.stopped} scene agent(s) stopped: the queue is dropped and `
        + "working ones stop after the step they are on. Nothing was deleted; Make the missing "
        + "resumes them.");
    } catch (failure) {
      showStageNotice("bad", failure.message);
    }
    await loadAgents();
    await rerender();
  };

  const approveAll = document.querySelector("#approve-passed-button");
  if (approveAll) approveAll.onclick = async () => {
    const count = approveAll.dataset.count;
    if (!window.confirm(`Approve ${count} scene(s) whose programs passed every check?\n\n`
        + "The render will use their clips as they are. Approving here does not mean you "
        + "watched them: open any scene to watch its preview, and withdraw its approval "
        + "there if it is not right.")) return;
    approveAll.disabled = true;
    try {
      const done = await post("/scenes/approve-passed", {});
      showStageNotice(done.not_passed ? "warn" : "ok", `${done.approved} scene(s) approved.`
        + (done.not_passed ? ` ${done.not_passed} have no clip that passed, so are not.` : ""));
    } catch (failure) {
      showStageNotice("bad", failure.message);
    }
    await refreshProjectSummary();
    await rerender();
  };

  document.querySelectorAll("[data-add-resource]").forEach(input => {
    input.onchange = async () => {
      const file = input.files[0];
      if (!file) return;
      const form = new FormData();
      form.append("file", file);
      try {
        await requestJsonFromApi(`/api/resources/${input.dataset.addResource}`,
          { method: "POST", body: form });
        showStageNotice("ok", `${file.name} is in the library. The agent sees it from the next scene it writes.`);
      } catch (failure) {
        showStageNotice("bad", failure.message);
      }
      await rerender();
    };
  });
  document.querySelectorAll("[data-remove-resource]").forEach(button => {
    button.onclick = async () => {
      if (!window.confirm(`Remove ${button.dataset.name} from the library? Scripts that use it will stop working.`)) return;
      try {
        await requestJsonFromApi(
          `/api/resources/${button.dataset.removeResource}/${encodeURIComponent(button.dataset.name)}`,
          { method: "DELETE" });
      } catch (failure) {
        showStageNotice("bad", failure.message);
      }
      await rerender();
    };
  });
}
