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
 * Writing is AI (up to a fixed number of calls per scene); running and checking
 * are not. A clip that fails a check is never used (`scene_lab.py`).
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, escapeHtml, hideProgress, icon, projectApiPath, refreshProjectSummary,
  showProgress, showStageNotice,
} from "/static/ui-kit.js";

export const sceneLabState = { openId: null };

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
  if (!preview.scripted) return "";
  const waiting = preview.scripted_waiting;
  return `
    <div class="run-bar ${waiting ? "stale" : "ready"} scripted-bar">
      <span class="run-icon">${icon(waiting ? ICON.alert : ICON.check, 17, 2.2)}</span>
      <span class="run-text">
        <b>${preview.scripted} scripted scene(s)${waiting ? `, ${waiting} without a clip that passed` : ""}</b>
        <span>${waiting
          ? `Each is written by the agent, run, checked, and fixed if a check fails: at most
             ${preview.script_calls_at_most} model call(s) for these ${waiting}.`
          : "Each has a clip that passed its checks. Open one to watch it, or to change its script."}</span>
      </span>
      ${waiting ? `<span class="plan-actions">
        <button class="btn btn-accent" id="write-scripts-button">
          Write the ${waiting} missing script(s) <span class="fact warn">AI</span></button>
      </span>` : ""}
    </div>`;
}

/* ---- the scene panel ------------------------------------------------------------ */

export function renderScenePanel(scene) {
  if (!scene) return "";
  const { visual, checks } = scene;
  const failing = checks.filter(check => check.status === "fail").length;
  const state = !scene.code ? ["blocked", "No script yet"]
    : !checks.length ? ["pending", "Not run yet"]
      : failing ? ["stale", `${failing} check(s) fail: this clip is not used`]
        : ["ready", "Passed its checks: this clip is what the scene shows"];
  return `
    <section class="panel scene-panel" data-scene="${escapeHtml(visual.id)}">
      <div class="panel-head">
        <h3>${escapeHtml(visual.section_title)} · scene ${visual.scene_number}</h3>
        <div class="spacer"></div>
        <button class="btn" id="close-scene-button">Close</button>
      </div>
      <p class="panel-sub mono">${escapeHtml(scene.folder || "No folder yet: it is made with the first script.")}</p>
      <div class="final-head ${state[0]} scene-state"><span class="run-text"><b>${state[1]}</b>
        <span>${escapeHtml(visual.note || "")}</span></span></div>

      <div class="scene-grid">
        <div>
          ${scene.has_clip
            ? `<video class="scene-clip" controls muted preload="metadata"
                 src="${sceneFileUrl(visual.id, "render.mp4", scene.checked_at)}"></video>`
            : `<div class="scene-clip scene-clip-empty">No clip yet</div>`}
          <p class="panel-sub">Silent on purpose: the narration is added by the render. About
            ${escapeHtml(String(scene.brief.seconds ?? "?"))} s, to fit what is said.</p>
          ${checks.length ? `
            <table class="assets-rule-table plan-checks scene-checks">
              <tbody>${checks.map(check => `
                <tr><td><span class="plan-check ${check.status}">${CHECK_LABELS[check.status]}</span></td>
                  <td><b>${escapeHtml(check.name)}</b><br><span class="muted">${escapeHtml(check.detail)}</span></td>
                </tr>`).join("")}</tbody>
            </table>` : ""}
          ${scene.sources.length ? `
            <div class="scene-sources"><b>Outside resources it used</b>
              ${scene.sources.map(source => `
                <div><a href="${escapeHtml(source.url)}" target="_blank" rel="noopener">${
                  escapeHtml(source.file)}</a> · ${escapeHtml(source.licence)} · ${escapeHtml(source.credit)}</div>`).join("")}
            </div>` : ""}
        </div>

        <div>
          <details class="scene-brief">
            <summary>What the script is told (brief.json)</summary>
            <p><b>Said:</b> ${escapeHtml(scene.brief.narration ?? visual.narration_preview)}</p>
            <p><b>On screen:</b> ${escapeHtml(scene.brief.on_screen ?? visual.brief)}</p>
          </details>
          <label class="scene-label" for="scene-code">scene.py</label>
          <textarea id="scene-code" class="scene-code" spellcheck="false"
            placeholder="No script yet. Have the agent write one, or write it here.">${escapeHtml(scene.code)}</textarea>
          <div class="scene-actions">
            <button class="btn btn-accent" id="run-scene-button" ${scene.code ? "" : "disabled"}>
              Save and run</button>
            <input id="scene-instruction" maxlength="400"
                   placeholder="What to change, in your own words (optional)">
            <button class="btn" id="write-scene-button">
              ${scene.code ? "Rewrite it" : "Write it"} <span class="fact warn">AI · up to ${scene.maximum_attempts}</span></button>
          </div>
          ${scene.log ? `<details class="scene-log"><summary>What it printed (log.txt)</summary>
            <pre>${escapeHtml(scene.log)}</pre></details>` : ""}
        </div>
      </div>
    </section>`;
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
  document.querySelectorAll("[data-open-scene]").forEach(button => {
    button.onclick = async () => {
      sceneLabState.openId = button.dataset.openScene;
      await rerender();
      document.querySelector(".scene-panel")?.scrollIntoView({ block: "start", behavior: "smooth" });
    };
  });
  const close = document.querySelector("#close-scene-button");
  if (close) close.onclick = () => { sceneLabState.openId = null; rerender(); };

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

  const run = document.querySelector("#run-scene-button");
  if (run) run.onclick = () => busy(run, "Running the scene's script",
    () => post(`/scenes/${encodeURIComponent(openId)}/run`,
      { code: document.querySelector("#scene-code").value }));
  document.querySelector("#scene-code")?.addEventListener("input", event => {
    if (run) run.disabled = !event.target.value.trim();
  });

  const write = document.querySelector("#write-scene-button");
  if (write) write.onclick = () => {
    const instruction = document.querySelector("#scene-instruction").value.trim();
    if (!window.confirm("Have the agent write this scene's script?\n\nUp to 3 model calls: "
        + "it writes, the script is run and checked, and it fixes what failed. "
        + "The script there now is replaced.")) return undefined;
    return busy(write, "Writing, running and checking the scene",
      () => post(`/scenes/${encodeURIComponent(openId)}/write`, { instruction }));
  };

  const writeAll = document.querySelector("#write-scripts-button");
  if (writeAll) writeAll.onclick = async () => {
    const waiting = visuals.visuals.filter(v => v.kind === "scripted" && (!v.is_built || v.is_stale));
    if (!window.confirm(`Write ${waiting.length} scene script(s)?\n\nAt most `
        + `${waiting.length * 3} model calls. Each scene is written, run and checked in turn; `
        + "you can leave this page and the ones already done are kept.")) return;
    writeAll.disabled = true;
    let passed = 0;
    for (const [index, visual] of waiting.entries()) {
      showProgress({ label: `Writing scene scripts: ${visual.section_title}`,
        done: index, total: waiting.length });
      try {
        const scene = await post(`/scenes/${encodeURIComponent(visual.id)}/write`, {});
        if (!scene.checks.some(check => check.status === "fail")) passed += 1;
      } catch (failure) {
        console.error("writing a scene failed", visual.id, failure);
        showStageNotice("bad", `${visual.section_title}: ${failure.message}`);
        break;
      }
    }
    hideProgress();
    await refreshProjectSummary();
    await rerender();
    showStageNotice(passed === waiting.length ? "ok" : "warn",
      `${passed} of ${waiting.length} scene(s) passed their checks.`
      + (passed === waiting.length ? "" : " Open the others to see what failed."));
  };

  const markAll = document.querySelector("#script-every-scene-button");
  if (markAll) markAll.onclick = async () => {
    if (!window.confirm("Make every scene a scripted scene?\n\nNothing is written yet: each "
        + "scene waits for its script, which you write from the Make tab. Pictures already "
        + "made for these scenes are no longer used.")) return;
    try {
      const marked = await post("/scenes/mark", {});
      showStageNotice("ok", `${marked.changed} scene(s) are now scripted scenes, waiting for their scripts.`);
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

/** Choosing "A scripted scene" in a kind picker goes to its own endpoint. */
export async function markOneScripted(visualId) {
  await post("/scenes/mark", { visual_ids: [visualId] });
  sceneLabState.openId = visualId;
}
