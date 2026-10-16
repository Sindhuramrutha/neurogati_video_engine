/**
 * Generation — three tabs, in the order the work happens.
 *
 * 1. Setup: what came in (the transferred script and assets) and the resource
 *    library the scene agents draw on.
 * 2. Make: one scene program per scene of the script. Each is written, run and
 *    checked, then watched and approved -- one by one, or every passed one at once.
 * 3. Final & transfer: the checks, each pass / warn / fail with why, and the
 *    transfer. The render reads the transferred scenes, frozen so that making a
 *    scene again cannot change them (`generation_handoff.py`).
 *
 * One card per scene, in the order they are spoken, each showing the frame
 * that will be on screen and the words the scene was briefed with. A brief was
 * a sentence nobody could check; a poster frame is a claim you can see.
 */

import { mountStoryboard, mountStoryboardGate } from "/static/storyboard.js";
import {
  agentOf, keepWatching, loadAgents, loadOpenScene, renderResourceLibrary,
  renderScenePanel, renderSceneSections, renderSceneStatus, renderScriptedBar, sceneLabState,
  scenePosterUrl, wireSceneLab,
} from "/static/scene-lab.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, footerNav, icon, moveToNextLayerButton,
  projectApiPath, refreshProjectSummary, select, showStageNotice, stageHeader,
  stageNeighbours, whenItWas, wireGotoButtons,
} from "/static/ui-kit.js";

const GENERATION_TABS = [
  ["setup", "Setup"], ["storyboard", "Storyboard"], ["make", "Make"],
  ["final", "Final & transfer"],
];

const currentGenerationTab = () =>
  GENERATION_TABS.some(([key]) => key === applicationState.generationTab)
    ? applicationState.generationTab : "setup";

const CHECK_LABELS = { pass: "Pass", warn: "Warning", fail: "Fails", "n/a": "Not applicable" };

/** A scene's poster frame: the one picture the page shows for it. */
const posterOf = visual => scenePosterUrl(visual);

export async function renderGenerationStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  if (!body.querySelector(".generation-tabs")) {
    body.innerHTML = `<div class="card muted">Loading the scenes…</div>`;
  }

  let visuals;
  let handoff;
  try {
    [visuals, handoff] = await Promise.all([
      requestJsonFromApi(projectApiPath("/visuals")),
      requestJsonFromApi(projectApiPath("/visuals/handoff")),
    ]);
  } catch (loadFailure) {
    console.error("visuals load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load the scenes.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }
  applicationState.sceneVisuals = visuals;

  // The resource library is the machine's; the open scene is one scene's folder. Either failing costs its panel, not the page.
  let resources = null;
  try {
    resources = await requestJsonFromApi("/api/resources");
  } catch (resourceFailure) {
    console.error("resource library load failed", resourceFailure);
  }
  const [openScene] = await Promise.all([loadOpenScene(), loadAgents()]);

  const tab = currentGenerationTab();
  const content = {
    setup: () => renderSetup(handoff) + renderResourceLibrary(resources),
    storyboard: () => `<div id="storyboard-mount"><div class="card muted">Loading the
      storyboard…</div></div>`,
    make: () => `<div id="storyboard-gate"></div>` + renderMake(visuals, handoff, openScene),
    final: () => renderGenerationFinal(visuals, handoff, stage),
  }[tab]();

  body.innerHTML = `
    ${stageHeader("generation", "Generation", { agentButtonId: "generation-agent-button" })}
    <div class="stage-content stage-content-bare">
      <div class="extraction-tabs plan-tabs generation-tabs">
        <nav class="x-tabs" role="tablist" aria-label="Generation steps">
          ${GENERATION_TABS.map(([key, label], index) => `
            <button role="tab" class="x-tab ${key === tab ? "on" : ""}" data-generation-tab="${key}"
                    aria-selected="${key === tab}">
              <span class="x-tab-number">${index + 1}</span>
              <b class="x-tab-label">${label}</b>
              ${key === "final" && handoff.failing ? `<span class="plan-tab-count fail">${handoff.failing}</span>`
                : key === "final" && handoff.warning ? `<span class="plan-tab-count warn">${handoff.warning}</span>` : ""}
            </button>`).join("")}
        </nav>
        <div class="x-tab-body" role="tabpanel">${content}</div>
      </div>
      ${renderGenerationFooter(stage, handoff, tab)}
    </div>`;

  wireGenerationStage(stage, navigateToStage, renderAgentStage);
  sceneLabState.navigate = navigateToStage;
  const again = () => renderGenerationStage(stage, navigateToStage, renderAgentStage);
  wireSceneLab(again, visuals);
  keepWatching(again);
  mountStoryboard(select("#storyboard-mount"));
  mountStoryboardGate(select("#storyboard-gate"), () => {
    applicationState.generationTab = "storyboard";
    again();
  });
}

/* ---- 1. Setup ---------------------------------------------------------------- */

function renderSetup(handoff) {
  const inputs = handoff.checks.filter(check => check.key === "script" || check.key === "assets");
  return `
    <div class="plan-brief">
      <section class="panel">
        <div class="panel-head"><h3>What came in</h3></div>
        <p class="panel-sub">Scenes are made from the transferred script (each scene's
          on-screen brief) and the pictures Assets &amp; Design transferred.</p>
        ${inputs.map(check => `
          <div class="assets-source-row">
            <span class="x-pick-name">${escapeHtml(check.name)}</span>
            <span class="plan-check ${check.status}">${CHECK_LABELS[check.status]}</span>
          </div>
          <p class="panel-sub">${escapeHtml(check.detail)}</p>`).join("")}
        ${renderPicturesHandedOn(handoff.pictures)}
      </section>
    </div>`;
}

/** The deck's pictures the plan carried, and how many of them the video shows.
 *  Every scene is offered every one, nearest first; the agent decides. */
function renderPicturesHandedOn(pictures) {
  if (!pictures || !pictures.handed_on) return "";
  const missing = pictures.not_shown || [];
  const measured = pictures.measured || [];
  return `
    <div class="assets-source-row">
      <span class="x-pick-name">The deck's pictures in the video</span>
      <span class="file-status">${pictures.shown} of ${pictures.handed_on} shown in some scene</span>
    </div>
    <p class="panel-sub">Every scene is offered every picture the plan carried, its own
      slide's first, with what each is; the scene agent decides what to show. Leave a
      picture out on Assets &amp; Design to keep it out of the video.</p>
    ${missing.length ? `
      <p class="panel-sub">Not in any scene yet:</p>
      <ul class="generation-unfit">${missing.map(picture => `
        <li><b>${escapeHtml(picture.name)}</b></li>`).join("")}</ul>` : ""}
    ${measured.length ? `
      <p class="panel-sub">Measured, and told to the agent (not refused):</p>
      <ul class="generation-unfit">${measured.map(picture => `
        <li><b>${escapeHtml(picture.name)}</b>: ${escapeHtml(picture.why)}</li>`).join("")}</ul>`
      : ""}`;
}

/* ---- 2. Make ---------------------------------------------------------------------- */

function renderMake(visuals, handoff, openScene) {
  if (visuals.is_empty) {
    return `<div class="empty"><h3>No scenes yet</h3>
      <p>Set up one scene program per scene of the transferred script. No model is called.</p>
      <button class="btn btn-accent" id="plan-visuals-button">Set up the scenes from the script</button>
      <button class="btn" data-goto="script-staging">
        ${icon(ICON.arrowLeft)} Go to Script &amp; Staging</button></div>`;
  }
  const preview = handoff.make_preview;
  return `
    ${renderScriptedBar(preview)}
    ${renderSceneStatus(visuals.visuals)}
    ${renderScenePanel(openScene)}
    ${visuals.notes.length ? `<p class="muted edit-hint">${visuals.notes.map(escapeHtml).join(" · ")}</p>` : ""}
    ${renderSceneSections(visuals.visuals, renderShot)}`;
}

/* the checks, shown on Final & transfer */

function renderGenerationChecks(handoff) {
  return `
    <section class="panel">
      <div class="panel-head"><h3>The checks before transfer</h3></div>
      <p class="panel-sub">Fixed rules over the scenes, the script and the assets. A failing
        check blocks the transfer; a warning is shown and allowed.</p>
      <table class="assets-rule-table plan-checks">
        <thead><tr><th>Result</th><th>Check</th><th>Rule</th><th>Found</th></tr></thead>
        <tbody>
          ${handoff.checks.map(check => `
            <tr>
              <td><span class="plan-check ${check.status === "n/a" ? "na" : check.status}">${
                CHECK_LABELS[check.status] ?? check.status}</span></td>
              <td><b>${escapeHtml(check.name)}</b></td>
              <td>${escapeHtml(check.rule)}</td>
              <td>${escapeHtml(check.detail)}</td>
            </tr>`).join("")}
        </tbody>
      </table>
    </section>`;
}

/* ---- 3. Final & transfer ------------------------------------------------------------- */

function renderGenerationFinal(visuals, handoff, stage) {
  const [tone, title, detail] = visuals.is_empty
    ? ["blocked", "Nothing to transfer yet", "Set up the scenes on the Make tab first."]
    : handoff.failing
      ? ["stale", `${handoff.failing} check(s) fail`, "Fix them (listed below), then transfer."]
      : !handoff.has_transferred
        ? ["pending", "Ready to transfer",
           "Nothing has been transferred yet, so the render reads the working scenes."]
        : handoff.pending
          ? ["pending", "Ready to transfer",
             "This differs from what the render has. Transfer to hand it the changes."]
          : ["ready", "Transferred to the next layer",
             `The render has had exactly these scenes since ${whenItWas(handoff.transferred_at)}.`];
  const canTransfer = !visuals.is_empty && !handoff.failing
    && (handoff.pending || !handoff.has_transferred);
  const audit = visuals.audit;
  return `
    <div class="final-head ${tone}">
      <span class="run-icon">${icon(tone === "ready" ? ICON.check : ICON.alert, 18, 2.3)}</span>
      <span class="run-text">
        <b>${escapeHtml(title)}</b>
        <span>${escapeHtml(detail)}</span>
        <span class="final-totals">${audit.scene_count} scene(s) · ${audit.built_count} made ·
          ${audit.approved_count} approved · ${handoff.warning} warning(s)</span>
      </span>
      ${tone === "ready" ? moveToNextLayerButton(stageNeighbours(stage).next, {
          carries: "The transferred scenes go on to the render." })
        : `<button class="btn btn-accent btn-transfer" id="transfer-generation-button"
                   ${canTransfer ? "" : "disabled"}>
             Transfer to the next layer ${icon(ICON.arrowRight)}</button>`}
    </div>
    <p class="panel-sub">A transfer freezes every file it points at, so making a scene
      again afterwards cannot change what the render shows until you transfer again.</p>
    <div class="assets-final-strip generation-final-strip">
      ${visuals.visuals.map(visual => visual.asset_path
        ? `<img alt="" loading="lazy" title="${escapeHtml(visual.section_title)} · scene ${visual.scene_number}"
               src="${posterOf(visual)}">`
        : `<span class="generation-words-thumb" title="Not made yet">${escapeHtml(
            visual.headline || "—")}</span>`).join("")}
    </div>
    ${renderGenerationChecks(handoff)}`;
}

function renderGenerationFooter(stage, handoff, tab) {
  const at = GENERATION_TABS.findIndex(([key]) => key === tab);
  const next = GENERATION_TABS[at + 1];
  return footerNav(stage, {
    end: next ? `
      <button class="btn btn-accent btn-move-next" data-generation-tab="${next[0]}">
        Move to ${next[1]} ${icon(ICON.arrowRight)}</button>` : null,
    next: {
      carries: handoff.has_transferred ? "The transferred scenes go on to the render." : "",
      warning: !handoff.has_transferred
        ? "The scenes have never been transferred: the render reads the working scenes until "
          + "you transfer them on the Final & transfer tab."
        : handoff.pending
          ? "Your latest changes are not transferred — the render still uses the last "
            + "transferred scenes."
          : "",
    },
  });
}

function agentChip(visual) {
  const agent = agentOf(visual.id);
  if (!agent || agent.status === "idle") return "";
  const tone = agent.status === "done" ? "ok"
    : ["failed", "stopped", "interrupted"].includes(agent.status) ? "bad" : "muted";
  const label = { queued: "queued", working: "being made", done: "made", stopped: "stopped",
    failed: "could not be made", interrupted: "interrupted" }[agent.status];
  return `<span class="fact ${tone}">${escapeHtml(label ?? agent.status)}</span>`;
}

/** For a scene its agent is on: what it is doing now, and how much of its
 *  render budget it has used (a scene can finish well before the budget). */
function agentProgress(visual) {
  const agent = agentOf(visual.id);
  if (!agent || !["working", "queued"].includes(agent.status)) return "";
  if (agent.status === "queued") {
    return `<div class="shot-progress queued"><span>Queued — starts when one of the
      scenes being made finishes</span></div>`;
  }
  const share = Math.min(100, Math.round(100 * agent.renders_used / agent.most_renders));
  return `
    <div class="shot-progress">
      <span class="shot-progress-doing">${escapeHtml(agent.doing || "Starting")}…</span>
      <div class="shot-progress-bar" title="${agent.renders_used} of up to ${agent.most_renders} renders">
        <i style="width:${share}%"></i></div>
      <span class="muted">Round ${agent.renders_used} of up to ${agent.most_renders}</span>
    </div>`;
}

function renderShot(visual) {
  return `
    <div class="shot-card ${visual.is_stale ? "is-stale" : ""} ${visual.is_built ? "" : "unbuilt"}"
         data-visual="${escapeHtml(visual.id)}">
      <div class="shot-head">
        <span class="outline-num">${visual.scene_number}</span>
        <div class="spacer"></div>
        ${visual.is_stale ? `<span class="fact warn">scene rewritten</span>` : ""}
        ${agentChip(visual)}
        ${visual.is_built ? "" : `<span class="fact bad">not made</span>`}
      </div>
      <span class="shot-section">${escapeHtml(visual.section_title)}</span>
      ${agentProgress(visual)}

      <div class="shot-frame">
        ${visual.asset_path
          ? `<img alt="" loading="lazy" src="${posterOf(visual)}">`
          : `<span class="shot-words">${escapeHtml(visual.headline || "Not made yet")}</span>`}
        ${visual.clip_path
          ? `<span class="shot-animated">drawn by ${escapeHtml(visual.drawn_by)}</span>`
          : ""}
      </div>

      <!-- What the script asked for, and the scene's note (a failing check's whole
           detail), are read in the scene itself, behind "Open the scene": on the
           card they ran to a dozen lines. -->

      <button class="btn btn-accent shot-open"
          data-open-scene="${escapeHtml(visual.id)}">Open the scene</button>
    </div>`;
}

function wireGenerationStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderGenerationStage(stage, navigateToStage, renderAgentStage);

  wireGotoButtons(navigateToStage);
  select("#generation-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-generation-tab]").forEach(button => {
    button.onclick = async () => {
      applicationState.generationTab = button.dataset.generationTab;
      const fromFooter = Boolean(button.closest(".footer-nav"));
      await rerender();
      if (fromFooter) select(".x-tabs")?.scrollIntoView({ block: "start", behavior: "smooth" });
    };
  });

  const planButton = select("#plan-visuals-button");
  if (planButton) {
    planButton.onclick = async () => {
      planButton.disabled = true;
      planButton.textContent = "Reading the script…";
      const before = new Map((applicationState.sceneVisuals?.visuals ?? [])
        .map(visual => [visual.id, visual.brief_fingerprint]));
      try {
        const planned = await requestJsonFromApi(projectApiPath("/visuals/plan"), { method: "POST" });
        const after = planned.visuals;
        const added = after.filter(visual => !before.has(visual.id)).length;
        const removed = [...before.keys()].filter(id => !after.some(v => v.id === id)).length;
        const rewritten = after.filter(visual => before.has(visual.id)
          && before.get(visual.id) !== visual.brief_fingerprint).length;
        const kept = after.length - added - rewritten;
        showStageNotice("ok", added || removed || rewritten
          ? `Set up again from the script: ${added} new, ${rewritten} rewritten (to make again),`
            + ` ${removed} removed, ${kept} unchanged.`
          : `The script has not changed: all ${after.length} scenes are as they were.`);
        await refreshProjectSummary();
      } catch (planFailure) {
        console.error("deciding visuals failed", planFailure);
        showStageNotice("bad", planFailure.message);
      }
      await rerender();
    };
  }

  const rebuild = select("#rebuild-visuals-button");
  if (rebuild) rebuild.onclick = async () => {
    const count = applicationState.sceneVisuals?.visuals?.length ?? 0;
    if (!window.confirm(`Make all ${count} scenes again?\n\nEvery scene's agent starts from a `
        + "fresh conversation and writes, renders and improves its scene until it is good — "
        + "paid model calls for every scene, including the ones already made and approved. "
        + "A scene's approval is withdrawn when it is rendered again.")) return;
    rebuild.disabled = true;
    try {
      const started = await requestJsonFromApi(projectApiPath("/scene-agents"), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ everything: true }),
      });
      showStageNotice("ok", `${started.started.length} scene agent(s) started again, start to end.`);
    } catch (failure) {
      showStageNotice("bad", failure.message);
    }
    await rerender();
  };

  const transfer = select("#transfer-generation-button");
  if (transfer && !transfer.disabled) {
    transfer.onclick = async () => {
      transfer.disabled = true;
      try {
        await requestJsonFromApi(projectApiPath("/visuals/transfer"), { method: "POST" });
        showStageNotice("ok", "Transferred: the render uses exactly these scenes, frozen.");
        await refreshProjectSummary();
      } catch (transferFailure) {
        console.error("transferring the scenes failed", transferFailure);
        showStageNotice("bad", transferFailure.message);
      }
      await rerender();
    };
  }

}
