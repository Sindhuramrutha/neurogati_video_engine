/**
 * Scene Plan — the video's shape, agreed in a conversation (`plan_agent.py`).
 *
 * 1. Direction: say what the video should be, with the setup beside it (the
 *    length in your own words, how strictly the slides' order is kept, the
 *    audience, the language). The planning agent answers and proposes
 *    the shape: the length as it understood it, the sections (each a run of
 *    slides), their minutes and how many scenes each has. Agree to it, or reply
 *    with what to change. Only on agreement are the scenes written.
 * 2. Plan: what was agreed — sections and their scenes — editable by hand, with
 *    each section's pictures.
 * 3. Check: fixed rules; the slide order is held by code.
 * 4. Final & transfer.
 *
 * Every pane is drawn and only the chosen one shown, so a tab change never
 * redraws the page or loses an edit in progress.
 */

import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, footerNav, icon, moveToNextLayerButton,
  projectApiPath, refreshProjectSummary, select, showStageNotice, stageHeader, stageNeighbours,
  whenItWas, wireGotoButtons,
} from "/static/ui-kit.js";

const PLAN_TABS = [
  ["direction", "Direction"], ["plan", "Plan"], ["final", "Final & transfer"],
];
const currentPlanTab = () =>
  PLAN_TABS.some(([key]) => key === applicationState.planTab) ? applicationState.planTab
    : "direction";

/** View state only — never saved. */
const planViewState = {
  isThinking: false,      // a message or an agreement is with the agent
  isActing: false,
  draftMessage: "",
  editingSectionId: null,
  editingPictures: [],
  editingPicturesChosen: false,
};

/** A section about no slide -- an opening, a recap, whatever the agent decided --
 *  is written from the rest of the plan. There are no fixed kinds of section. */
const aboutNoSlide = section => !(section.sources ?? []).length;

const clock = seconds => seconds < 60 ? `${seconds} s`
  : `${Math.floor(seconds / 60)} min${seconds % 60 ? ` ${seconds % 60} s` : ""}`;

/** "4–9", or "4, 6, 7" when not one run. */
function unitsLabel(numbers) {
  if (!numbers.length) return "—";
  const run = numbers.every((n, i) => i === 0 || n === numbers[i - 1] + 1);
  return run && numbers.length > 1 ? `${numbers[0]}–${numbers.at(-1)}` : numbers.join(", ");
}

/** The units (slides, or parts) a saved section covers, by number, as the
 *  server matched them. */
const sectionUnits = (section, planning) => planning.section_units?.[section.id] ?? [];

/** "4-9, 12" → [4,5,6,7,8,9,12]; null when it cannot be read. */
function parseUnits(text) {
  const numbers = [];
  for (const part of text.split(",").map(p => p.trim()).filter(Boolean)) {
    const range = part.match(/^(\d+)\s*[-–]\s*(\d+)$/);
    if (range) {
      const [from, to] = [Number(range[1]), Number(range[2])];
      if (to < from || to - from > 200) return null;
      for (let n = from; n <= to; n += 1) numbers.push(n);
    } else if (/^\d+$/.test(part)) numbers.push(Number(part));
    else return null;
  }
  return numbers;
}

export async function renderScenePlanStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  if (!body.querySelector(".plan-tabs")) {
    body.innerHTML = `<div class="card muted">Loading plan…</div>`;
  }

  let plan;
  let settings;
  let planning;
  let handoff = { checks: [], failing: 0, warning: 0, has_transferred: false, pending: false };
  try {
    [plan, settings, planning, handoff] = await Promise.all([
      loadStageDocument("plan", "/plan"),
      requestJsonFromApi(projectApiPath(`/settings/${stage.key}`)),
      requestJsonFromApi(projectApiPath("/plan/planning")),
      requestJsonFromApi(projectApiPath("/plan/handoff")),
    ]);
    if (plan === null) return;
    applicationState.stageSettings[stage.key] = settings;
  } catch (loadFailure) {
    console.error("plan load failed", loadFailure);
    // A page newer than the server asks for routes the server does not have yet.
    const outdated = /not found/i.test(loadFailure.message);
    body.innerHTML = `<div class="card"><b>Could not load the plan.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}${outdated
        ? " — the server is running different code from this page. Stop it and start it again "
          + "(<code>uv run pipeline serve</code>), then reload." : ""}</p></div>`;
    return;
  }

  const tab = currentPlanTab();
  const pane = (key, content) =>
    `<section class="plan-pane" data-plan-pane="${key}" ${key === tab ? "" : "hidden"}>${content}</section>`;

  body.innerHTML = `
    ${stageHeader("scene-plan", "Scene Plan", { agentButtonId: "planning-agent-button" })}
    <div class="stage-content stage-content-bare">
      <div class="extraction-tabs plan-tabs">
        <nav class="x-tabs" role="tablist" aria-label="Scene Plan steps">
          ${PLAN_TABS.map(([key, label], index) => `
            <button role="tab" class="x-tab ${key === tab ? "on" : ""}" data-plan-tab="${key}"
                    aria-selected="${key === tab}">
              <span class="x-tab-number">${index + 1}</span>
              <b class="x-tab-label">${label}</b>
              ${key === "final" && handoff.failing ? `<span class="plan-tab-count fail">${handoff.failing}</span>` : ""}
            </button>`).join("")}
        </nav>
        <div class="x-tab-body" role="tabpanel">
          ${pane("direction", renderDirection(plan, planning, settings))}
          ${pane("plan", renderPlanTab(plan, planning))}
          ${pane("final", renderFinal(plan, handoff, stage, planning))}
        </div>
      </div>
      ${renderFooterNav(stage, handoff, tab)}
    </div>`;

  lastHandoff = handoff;
  currentNavigate = navigateToStage;
  wireScenePlanStage(stage, navigateToStage, renderAgentStage, planning);
  const thread = select(".plan-thread");
  if (thread) thread.scrollTop = thread.scrollHeight;
}

/* ---- 1. Direction: the conversation, and the setup beside it -------------------------- */

function renderDirection(plan, planning, settings) {
  const word = planning.unit_word;
  const nothing = !planning.units.length;
  return `
    <div class="plan-direction">
      <section class="panel plan-chat">
        <div class="panel-head"><h3>Plan the video with the planning agent</h3></div>
        ${nothing ? `<p class="muted">Nothing is extracted yet, so there is nothing to plan.
            <button class="btn" data-goto="extraction">Go to Extraction</button></p>` : ""}
        <div class="plan-thread">
          ${planning.messages.length ? planning.messages.map((message, index) =>
            renderMessage(message, index === lastProposalIndex(planning) ? planning : null, word)
          ).join("") : `
            <div class="plan-thread-empty">
              <b>Say what this video should be.</b>
              <span>For example: “One continuous lesson for nursing students. Keep Padma's
                story together as one section, and spend the most time on the neural
                architecture.” Set the length and the slide order on the right first.</span>
              <span>The agent proposes the shape — sections, minutes, scenes. Nothing is
                changed until you agree to it.</span>
            </div>`}
          ${planning.proposal && lastProposalIndex(planning) < 0
            ? renderProposal(planning, word) : ""}
          ${planViewState.isThinking ? `<div class="plan-msg agent thinking">
              <span class="plan-msg-who">Planning agent</span>Thinking…</div>` : ""}
        </div>
        <div class="plan-composer">
          <textarea id="plan-message" maxlength="4000" rows="3" ${nothing ? "disabled" : ""}
            placeholder="${planning.messages.length
              ? "Reply: what to change, or what to keep…" : "What should this video be?"}"
            >${escapeHtml(planViewState.draftMessage)}</textarea>
          <button class="btn btn-accent" id="send-plan-message"
                  ${nothing || planViewState.isThinking ? "disabled" : ""}>
            Plan scene <span class="fact warn">AI · 1–2 calls</span></button>
        </div>
        <p class="muted plan-composer-hint">Ctrl + Enter sends. Each message sends the setup, every
          ${word}'s title and size, the plan as it stands and this conversation.</p>
      </section>
      ${renderSetup(plan, planning, settings)}
    </div>`;
}

/** The thread entry the waiting proposal belongs to: the last agent reply. */
function lastProposalIndex(planning) {
  if (!planning.proposal) return -1;
  for (let i = planning.messages.length - 1; i >= 0; i -= 1) {
    if (planning.messages[i].role === "agent") {
      return planning.messages[i].proposal ? i : -1;
    }
  }
  return -1;
}

function renderMessage(message, withProposal, word) {
  const who = message.role === "you" ? "You" : "Planning agent";
  return `
    <div class="plan-msg ${message.role} ${message.failed ? "failed" : ""}">
      <span class="plan-msg-who">${who} · ${escapeHtml(whenItWas(message.at))}</span>
      ${escapeHtml(message.text)}
      ${withProposal ? renderProposal(withProposal, word) : ""}
    </div>`;
}

function renderProposal(planning, word) {
  const proposal = planning.proposal;
  const sections = proposal.sections;
  const minutes = sections.reduce((sum, s) => sum + s.minutes, 0);
  const scenes = sections.reduce((sum, s) => sum + Math.max(1, s.scenes), 0);
  const leftOut = Object.entries(proposal.left_out ?? {});
  const problems = proposal.problems ?? [];
  return `
    <div class="plan-proposal">
      <div class="plan-proposal-head">
        <b>Proposed shape</b>
        <span>${Math.round(minutes * 10) / 10} min · ${sections.length} sections · ${scenes} scenes</span>
      </div>
      <p class="plan-understood"><b>Length, as understood:</b>
        ${escapeHtml(proposal.length.understood)}</p>
      <table class="plan-shape">
        <thead><tr><th>#</th><th>Section</th><th>${word === "slide" ? "Slides" : "Parts"}</th>
          <th>Minutes</th><th>Scenes</th></tr></thead>
        <tbody>${sections.map((section, index) => `
          <tr>
            <td>${index + 1}</td>
            <td><b>${escapeHtml(section.title)}</b>
              <span class="plan-shape-summary">${escapeHtml(section.summary)}</span>
              ${section.how ? `<span class="plan-shape-how">${escapeHtml(section.how)}</span>` : ""}</td>
            <td>${unitsLabel(section.units)}</td>
            <td>${Math.round(section.minutes * 10) / 10}</td>
            <td>${Math.max(1, section.scenes)}</td>
          </tr>`).join("")}</tbody>
      </table>
      ${leftOut.length ? `<p class="plan-left-out"><b>Left out on purpose:</b> ${leftOut.map(
        ([unit, why]) => `${word} ${escapeHtml(unit)} (${escapeHtml(why)})`).join("; ")}</p>` : ""}
      ${problems.length ? `<div class="plan-problems"><b>This shape breaks the rules you set,
          so it cannot be agreed to.</b> Reply with what to fix.
          <ul>${problems.map(p => `<li>${escapeHtml(p)}</li>`).join("")}</ul></div>` : ""}
      <div class="plan-proposal-actions">
        <button class="btn btn-accent" id="agree-shape" ${problems.length
          || planViewState.isThinking ? "disabled" : ""}>Agree to this shape
          ${planning.agree_calls ? `<span class="fact warn">AI · ${planning.agree_calls}
            call${planning.agree_calls === 1 ? "" : "s"} for the scenes</span>`
            : `<span class="fact muted">no AI: the scenes are kept</span>`}</button>
        <button class="btn" id="discard-shape">Discard</button>
        <span class="muted">Or reply below with what to change.</span>
      </div>
    </div>`;
}

/** The setup's icons, one per box. */
const SETUP_ICONS = {
  setup: `<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/>
          <circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>`,
  length: `<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>`,
  order: `<path d="M4 6h10M4 12h10M4 18h10M18 4v16M15 17l3 3 3-3"/>`,
  audience: `<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/>
             <path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>`,
  language: `<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>`,
};

/** One setup field in its own box: an icon, its name, then the control. */
const setupBox = (key, label, body, { forId = "", note = "" } = {}) => `
  <section class="setup-box setup-${key}">
    <div class="setup-box-head">
      <span class="setup-icon">${icon(SETUP_ICONS[key], 16, 2)}</span>
      ${forId ? `<label for="${forId}">${label}</label>` : `<b>${label}</b>`}
      ${note ? `<span class="muted setup-note">${note}</span>` : ""}
    </div>
    ${body}
  </section>`;

function renderSetup(plan, planning, settings) {
  const language = settings.options.find(option => option.key === "language");
  return `
    <aside class="plan-setup">
      <section class="setup-box setup-title">
        <div class="setup-box-head">
          <span class="setup-icon">${icon(SETUP_ICONS.setup, 16, 2)}</span>
          <b>Setup</b>
        </div>
        <p class="muted setup-hint">Sent with every message. Saved as you change it.</p>
      </section>

      ${setupBox("length", "Length, in your words", `
        <input id="setup-length" maxlength="300" value="${escapeHtml(plan.length_text)}"
               placeholder="e.g. about 1 hr, longer if needed, never shorter">
        ${plan.length?.understood ? `<p class="muted setup-hint">Agreed as:
          ${escapeHtml(plan.length.understood)}</p>` : ""}`, { forId: "setup-length" })}

      ${setupBox("order", planning.unit_word === "slide" ? "Slide order" : "Order of the source", `
        <div class="plan-order-picks">
          ${Object.entries(planning.slide_orders).map(([key, text]) => `
            <label class="plan-order-pick ${plan.slide_order === key ? "on" : ""}">
              <input type="radio" name="slide-order" value="${key}"
                     ${plan.slide_order === key ? "checked" : ""}>
              <span>${escapeHtml(text)}</span>
            </label>`).join("")}
        </div>`)}

      ${setupBox("audience", "Audience", `
        <input id="setup-audience" maxlength="300" value="${escapeHtml(plan.audience)}"
               placeholder="Who is watching, if it matters">`,
        { forId: "setup-audience", note: "optional" })}

      ${language ? setupBox("language", "Language", `
        <select id="setup-language">
          ${language.choices.map(choice => `<option value="${escapeHtml(choice.value)}"
            ${settings.values.language === choice.value ? "selected" : ""}>${
            escapeHtml(choice.label)}</option>`).join("")}
        </select>`, { forId: "setup-language" }) : ""}

    </aside>`;
}

/* ---- 2. Plan: sections and their scenes ------------------------------------------------- */

const pictureUrl = picture => picture.shown_path.startsWith("assets/prepared/")
  ? projectApiPath(`/assets/prepared/${encodeURIComponent(picture.shown_path.split("/").pop())}`)
  : projectApiPath(`/extraction/assets/${encodeURIComponent(picture.path.split("/").pop())}`);
const offeredPicture = (plan, path) => (plan.pictures?.offered ?? []).find(p => p.path === path);

function renderPlanTab(plan, planning) {
  if (!plan.sections.length) {
    return `<section class="panel"><p class="muted" style="margin:0">Nothing is agreed yet.
      Plan the video on the Direction tab; the shape you agree to appears here, with its
      scenes.</p>
      <button class="btn btn-accent" data-plan-tab="direction" style="margin-top:10px">
        Go to Direction ${icon(ICON.arrowRight)}</button></section>`;
  }
  const word = planning.unit_word === "slide" ? "Slides" : "Parts";
  return `
    ${plan.pictures?.has_assets ? "" : `<div class="pictures-notice">
      <b>Assets & Design is not transferred yet.</b> The plan carries its pictures, brand kit
      and look to every later layer, so the plan cannot be transferred until it is.
      <button class="btn" data-goto="assets">Go to Assets & Design</button></div>`}
    <div class="plan-summary-bar">
      <b>${clock(plan.total_estimated_seconds)}</b> · ${plan.sections.length} sections ·
      ${plan.scene_count} scenes
      ${plan.length?.understood ? `<span class="muted">— agreed: ${
        escapeHtml(plan.length.understood)}</span>` : ""}
    </div>
    <div class="plan-sections">
      ${plan.sections.map((section, index) =>
        renderSection(section, index, plan, planning, word)).join("")}
    </div>
    <button class="add-row" id="add-section-button">${icon(ICON.plus)} Add a section by hand</button>`;
}

function renderSection(section, index, plan, planning, word) {
  const editing = planViewState.editingSectionId === section.id;
  const units = sectionUnits(section, planning);
  return `
    <section class="panel plan-section" data-section="${section.id}">
      <div class="plan-section-head">
        <span class="outline-num">${index + 1}</span>
        <b class="plan-section-title">${escapeHtml(section.title || "Untitled section")}</b>
        <span class="fact">${aboutNoSlide(section) ? "about no slide · written from the rest of the plan"
          : `${word} ${unitsLabel(units)}`}</span>
        <span class="fact">${clock(section.estimated_seconds)} · ${section.scenes.length} scene${
          section.scenes.length === 1 ? "" : "s"}</span>
        <button class="btn" data-edit-section="${section.id}">${editing ? "Close" : "Edit"}</button>
      </div>
      ${section.summary ? `<p class="plan-section-summary">${escapeHtml(section.summary)}</p>` : ""}
      ${section.how ? `<p class="plan-section-how"><b>How it is told:</b> ${escapeHtml(section.how)}</p>` : ""}
      ${editing ? renderSectionEditor(section, units, word) : ""}
      ${renderSectionPictures(section, plan)}
      <table class="plan-scenes">
        <thead><tr><th>#</th><th>What the scene says and shows</th><th>${word}</th>
          <th>Seconds</th><th></th></tr></thead>
        <tbody>
          ${section.scenes.map((scene, n) => `
            <tr data-scene="${scene.id}">
              <td>${n + 1}</td>
              <td><textarea class="scene-does" rows="2" maxlength="400"
                    data-scene-field="does">${escapeHtml(scene.does)}</textarea></td>
              <td><input class="scene-units" data-scene-field="slides"
                    value="${escapeHtml(unitsLabel(scene.slides ?? []).replace("—", ""))}"></td>
              <td><input class="scene-seconds" type="number" min="3" max="900"
                    data-scene-field="seconds" value="${scene.seconds}"></td>
              <td class="plan-scene-actions">
                <button class="btn-icon" data-scene-move="-1" title="Move up" ${n ? "" : "disabled"}
                  aria-label="Move up">↑</button>
                <button class="btn-icon" data-scene-move="1" title="Move down"
                  ${n < section.scenes.length - 1 ? "" : "disabled"} aria-label="Move down">↓</button>
                <button class="btn-icon danger" data-scene-remove title="Remove this scene"
                  aria-label="Remove this scene">×</button>
              </td>
            </tr>`).join("")}
        </tbody>
      </table>
      <button class="btn plan-add-scene" data-add-scene="${section.id}">${icon(ICON.plus)} Add a scene</button>
    </section>`;
}

function renderSectionEditor(section, units, word) {
  return `
    <div class="plan-section-editor">
      <div class="edit-field"><label for="edit-title">Title</label>
        <input id="edit-title" maxlength="120" value="${escapeHtml(section.title)}"></div>
      <div class="edit-field"><label for="edit-summary">Summary</label>
        <textarea id="edit-summary" maxlength="400" rows="2">${escapeHtml(section.summary)}</textarea></div>
      <div class="edit-field"><label for="edit-how">How it is told</label>
        <textarea id="edit-how" maxlength="400" rows="2">${escapeHtml(section.how ?? "")}</textarea></div>
        <div class="edit-field"><label for="edit-units">${word}</label>
          <input id="edit-units" value="${escapeHtml(unitsLabel(units).replace("—", ""))}"
                 placeholder="e.g. 4–9">
          <p class="muted edit-hint">A run like 4–9, or a list like 4, 6. Empty: about no
            slide, written from the rest of the plan.</p></div>
        <div class="edit-field"><label>Pictures it shows</label>
          <p class="muted edit-hint" id="edit-pictures-rule"></p>
          <div id="edit-pictures" class="picture-picker"></div></div>
      <div class="edit-row">
        <button class="btn btn-accent" id="save-section-button">Save</button>
        <button class="btn danger" id="delete-section-button">Delete section</button>
      </div>
    </div>`;
}

function renderSectionPictures(section, plan) {
  if (!plan.pictures?.has_assets || aboutNoSlide(section)) return "";
  const pictures = (section.picture_paths ?? []).map(path => offeredPicture(plan, path))
    .filter(Boolean);
  if (!pictures.length) {
    return `<div class="section-pictures"><span class="fact muted">no pictures${
      section.pictures_chosen ? " · chosen" : ""}</span></div>`;
  }
  return `
    <div class="section-pictures" title="${escapeHtml(pictures.map(p => p.name).join("\n"))}">
      ${pictures.slice(0, 8).map(p => `<img alt="${escapeHtml(p.name)}" loading="lazy" src="${
        pictureUrl(p)}">`).join("")}
      ${pictures.length > 8 ? `<span class="more">+${pictures.length - 8}</span>` : ""}
      <span class="fact ${section.pictures_chosen ? "" : "muted"}">${pictures.length}
        picture${pictures.length === 1 ? "" : "s"} · ${section.pictures_chosen ? "chosen" : "by rule"}</span>
    </div>`;
}

function renderEditingPictures() {
  const host = select("#edit-pictures");
  if (!host) return;
  const plan = applicationState.plan;
  const attached = new Set(planViewState.editingPictures);
  const offered = plan.pictures?.offered ?? [];
  select("#edit-pictures-rule").innerHTML = planViewState.editingPicturesChosen
    ? `Chosen by you: the section keeps exactly these.
       <button type="button" class="btn" id="pictures-by-rule">Back to the rule</button>`
    : `By rule: every picture from this section's own ${escapeHtml("slides")} that can fill a
       frame. Click a picture to choose them yourself.`;
  host.innerHTML = offered.length ? offered.map(picture => `
      <button type="button" class="picture-tile ${attached.has(picture.path) ? "on" : ""}"
              data-picture="${escapeHtml(picture.path)}" ${picture.can_attach ? "" : "disabled"}
              aria-pressed="${attached.has(picture.path)}"
              title="${escapeHtml(picture.can_attach ? picture.name : `${picture.name}: ${picture.why_not}`)}">
        <img alt="" loading="lazy" src="${pictureUrl(picture)}">
        <span>${escapeHtml(picture.name)}</span>
        ${picture.can_attach
          ? `<b class="tile-state">${attached.has(picture.path) ? "✓ Attached" : "Not attached"}</b>`
          : `<em>${escapeHtml(picture.why_not)}</em>`}
      </button>`).join("")
    : `<span class="muted edit-hint">Assets & Design handed on no pictures.</span>`;

  host.querySelectorAll("[data-picture]").forEach(button => {
    button.onclick = () => {
      const now = new Set(planViewState.editingPictures);
      const path = button.dataset.picture;
      now.has(path) ? now.delete(path) : now.add(path);
      planViewState.editingPictures = offered.map(p => p.path).filter(p => now.has(p));
      planViewState.editingPicturesChosen = true;
      renderEditingPictures();
    };
  });
  const byRule = select("#pictures-by-rule");
  if (byRule) byRule.onclick = () => {
    planViewState.editingPicturesChosen = false;
    planViewState.editingPictures =
      [...(plan.pictures?.by_rule?.[planViewState.editingSectionId] ?? [])];
    renderEditingPictures();
  };
}

/* ---- 4. Final & transfer ---------------------------------------------------------------- */

/** Only what is wrong: the checks still decide whether the plan can be handed
 *  on, and a passing one has nothing to say. */
function renderProblems(handoff) {
  const problems = handoff.checks.filter(c => c.status === "fail" || c.status === "warn");
  if (!problems.length) return "";
  return `
    <section class="panel plan-problems-list">
      ${problems.map(check => `
        <div class="plan-problem ${check.status}">
          <span class="plan-check ${check.status}">${check.status === "fail" ? "Blocks" : "Note"}</span>
          <span><b>${escapeHtml(check.name)}</b> — ${escapeHtml(check.detail)}</span>
        </div>`).join("")}
    </section>`;
}

function renderFinal(plan, handoff, stage, planning) {
  const [tone, title, detail] = !plan.sections.length
    ? ["blocked", "Nothing to transfer yet", "Agree to a shape on the Direction tab first."]
    : handoff.failing
      ? ["stale", `${handoff.failing} problem(s) block the transfer`, "Fix what is listed below; then transfer."]
      : !handoff.has_transferred
        ? ["pending", "Ready to transfer",
           "Nothing has been transferred yet, so later stages read your working plan."]
        : handoff.pending
          ? ["pending", "Ready to transfer",
             "This differs from what the next layer has. Transfer to hand it the changes."]
          : ["ready", "Transferred to the next layer",
             `The next layer has had exactly this since ${whenItWas(handoff.transferred_at)}.`];
  const canTransfer = plan.sections.length && !handoff.failing
    && (handoff.pending || !handoff.has_transferred);
  const word = planning.unit_word === "slide" ? "slides" : "parts";
  return `
    <div class="final-head ${tone}">
      <span class="run-icon">${icon(tone === "ready" ? ICON.check : ICON.alert, 18, 2.3)}</span>
      <span class="run-text">
        <b>${escapeHtml(title)}</b>
        <span>${escapeHtml(detail)}</span>
        <span class="final-totals">${plan.sections.length} section(s) · ${plan.scene_count} scene(s) ·
          ${clock(plan.total_estimated_seconds)}</span>
      </span>
      ${tone === "ready" ? moveToNextLayerButton(stageNeighbours(stage).next, {
          carries: "The plan, its scenes, and the pictures, brand kit and look go on." })
        : `<button class="btn btn-accent btn-transfer" id="transfer-plan-button"
                   ${canTransfer ? "" : "disabled"}>
             Transfer to the next layer ${icon(ICON.arrowRight)}</button>`}
    </div>
    ${renderProblems(handoff)}
    <section class="panel">
      <div class="panel-head"><h3>What is handed on</h3></div>
      <p><b>Length:</b> ${escapeHtml(plan.length?.understood || "not agreed")} ·
        <b>Order:</b> ${escapeHtml(planning.slide_orders[plan.slide_order] ?? "")} ·
        <b>Audience:</b> ${escapeHtml(plan.audience || "not stated")}</p>
      <ol class="plan-final-list">
        ${plan.sections.map(section => `
          <li><b>${escapeHtml(section.title || "Untitled section")}</b>
            <span>${aboutNoSlide(section) ? "" : `${word} ${unitsLabel(sectionUnits(section, planning))} · `}${
              section.scenes.length} scenes · ${clock(section.estimated_seconds)}</span></li>`).join("")}
      </ol>
    </section>`;
}

function renderFooterNav(stage, handoff, tab) {
  const at = PLAN_TABS.findIndex(([key]) => key === tab);
  const next = PLAN_TABS[at + 1];
  return footerNav(stage, {
    end: next ? `
      <button class="btn btn-accent btn-move-next" data-plan-tab="${next[0]}">
        Move to ${next[1]} ${icon(ICON.arrowRight)}</button>` : null,
    next: {
      carries: handoff.has_transferred ? "The transferred plan goes on to be scripted." : "",
      warning: !handoff.has_transferred
        ? "The plan has never been transferred: later stages read your working plan until "
          + "you transfer it on the Final & transfer tab."
        : handoff.pending
          ? "Your latest changes are not transferred — later stages still read the last "
            + "transferred plan."
          : "",
    },
  });
}

/* ---- server actions ---------------------------------------------------------------------- */

async function runPlanAction({ path, method = "POST", body, done, rerender }) {
  if (planViewState.isActing) {
    showStageNotice("warn", "Still working on the last action — try again in a moment.");
    return;
  }
  planViewState.isActing = true;
  try {
    await requestJsonFromApi(projectApiPath(path), {
      method, headers: { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    await refreshProjectSummary();
    await rerender();
    if (done) showStageNotice("ok", done);
  } catch (actionFailure) {
    console.error("plan action failed", path, actionFailure);
    showStageNotice("bad", actionFailure.message);
  } finally {
    planViewState.isActing = false;
  }
}

/** A call to the agent: shown as thinking in the thread until it answers. */
async function askTheAgent(path, rerender, done) {
  if (planViewState.isThinking) return;
  planViewState.isThinking = true;
  await rerender();
  try {
    await requestJsonFromApi(projectApiPath(path), {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: path.endsWith("/message")
        ? JSON.stringify({ text: planViewState.draftMessage }) : "{}",
    });
    if (path.endsWith("/message")) planViewState.draftMessage = "";
    planViewState.isThinking = false;
    await refreshProjectSummary();
    await rerender();
    showStageNotice("ok", done);
  } catch (failure) {
    console.error("planning agent failed", failure);
    planViewState.isThinking = false;
    await rerender();
    showStageNotice("bad", failure.message);
  }
}

/* ---- wiring ------------------------------------------------------------------------------ */

let lastHandoff = null;
let currentNavigate = () => {};

function rerenderFooter(stage, tab) {
  const footer = select(".stage-content > .footer-nav");
  if (!footer || !lastHandoff) return;
  footer.outerHTML = renderFooterNav(stage, lastHandoff, tab);
  wireGotoButtons(currentNavigate);
  document.querySelectorAll(".footer-nav [data-plan-tab]").forEach(button => {
    button.onclick = () => select(`.plan-tabs [data-plan-tab="${button.dataset.planTab}"]`)?.click();
  });
}

function wireScenePlanStage(stage, navigateToStage, renderAgentStage, planning) {
  const rerender = () => renderScenePlanStage(stage, navigateToStage, renderAgentStage);
  const change = applyEdit => editStageDocument({
    documentKind: "plan", apiPathSuffix: "/plan", applyEdit, rerender,
  });

  select("#planning-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-plan-tab]").forEach(button => {
    button.onclick = () => {
      const tab = button.dataset.planTab;
      applicationState.planTab = tab;
      document.querySelectorAll("[data-plan-pane]").forEach(pane => {
        pane.hidden = pane.dataset.planPane !== tab;
      });
      document.querySelectorAll(".plan-tabs .x-tab").forEach(tabButton => {
        const on = tabButton.dataset.planTab === tab;
        tabButton.classList.toggle("on", on);
        tabButton.setAttribute("aria-selected", String(on));
      });
      rerenderFooter(stage, tab);
      if (tab === "plan") fitSceneBoxes();
      if (!button.closest(".x-tabs")) {
        select(".x-tabs")?.scrollIntoView({ block: "start", behavior: "smooth" });
      }
    };
  });
  wireGotoButtons(navigateToStage);

  const transferButton = select("#transfer-plan-button");
  if (transferButton && !transferButton.disabled) {
    transferButton.onclick = () => runPlanAction({
      path: "/plan/transfer", rerender,
      done: "Transferred: the stages after this read exactly this plan.",
    });
  }

  wireDirection(rerender, planning);
  wirePlan(change, rerender, planning);
}

function wireDirection(rerender, planning) {
  const message = select("#plan-message");
  const send = select("#send-plan-message");
  if (message) {
    message.addEventListener("input", () => { planViewState.draftMessage = message.value; });
    message.addEventListener("keydown", event => {
      if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) send?.click();
    });
  }
  if (send) send.onclick = () => {
    planViewState.draftMessage = message.value.trim();
    if (!planViewState.draftMessage) {
      showStageNotice("warn", "Write what you want first.");
      return;
    }
    askTheAgent("/plan/message", rerender, "The planning agent answered. Read its shape below.");
  };

  const agreeButton = select("#agree-shape");
  if (agreeButton) agreeButton.onclick = () => {
    const calls = planning.agree_calls;
    if (calls && !window.confirm(`Agree to this shape?\n\nIt becomes the plan, and the scenes `
        + `of ${calls} section(s) are written: ${calls} AI call(s). Sections whose slides and `
        + "scene count did not change keep their scenes.")) return;
    askTheAgent("/plan/agree", rerender, "Agreed. The plan and its scenes are on the Plan tab.");
  };
  const discard = select("#discard-shape");
  if (discard) discard.onclick = () => runPlanAction({
    path: "/plan/proposal", method: "DELETE", rerender, done: "Proposal discarded.",
  });

  // The setup saves as it changes.
  const saveSetup = changes => runPlanAction({ path: "/plan/setup", body: changes, rerender });
  const length = select("#setup-length");
  if (length) length.onchange = () => saveSetup({ length_text: length.value });
  const audience = select("#setup-audience");
  if (audience) audience.onchange = () => saveSetup({ audience: audience.value });
  document.querySelectorAll("[name=slide-order]").forEach(radio => {
    radio.onchange = () => saveSetup({ slide_order: radio.value });
  });
  const languageSelect = select("#setup-language");
  if (languageSelect) languageSelect.onchange = async () => {
    const settings = applicationState.stageSettings["scene-plan"];
    try {
      applicationState.stageSettings["scene-plan"] = await requestJsonFromApi(
        projectApiPath("/settings/scene-plan"), {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ values: { ...settings.values, language: languageSelect.value } }),
        });
      showStageNotice("ok", "Language saved.");
    } catch (failure) {
      showStageNotice("bad", `Could not save the language — ${failure.message}`);
    }
  };
}

/** A scene's text box is as tall as its text, so nothing is cut off. Measured
 *  only while visible: a hidden tab has no height to measure. */
function fitSceneBoxes(only = null) {
  const boxes = only ? [only] : document.querySelectorAll(".plan-scenes textarea");
  boxes.forEach(box => {
    if (!box.offsetParent) return;
    box.style.height = "auto";
    box.style.height = `${box.scrollHeight + 2}px`;
  });
}

function wirePlan(change, rerender, planning) {
  const sectionOf = (plan, element) =>
    plan.sections.find(s => s.id === element.closest("[data-section]").dataset.section);

  document.querySelectorAll("[data-edit-section]").forEach(button => {
    button.onclick = () => {
      const id = button.dataset.editSection;
      const section = applicationState.plan.sections.find(s => s.id === id);
      planViewState.editingSectionId = planViewState.editingSectionId === id ? null : id;
      planViewState.editingPictures = [...(section?.picture_paths ?? [])];
      planViewState.editingPicturesChosen = Boolean(section?.pictures_chosen);
      rerender();
    };
  });
  renderEditingPictures();

  const save = select("#save-section-button");
  if (save) save.onclick = () => {
    const id = planViewState.editingSectionId;
    const unitsInput = select("#edit-units");
    let sources = null;
    if (unitsInput) {
      const numbers = parseUnits(unitsInput.value);
      const known = new Map(planning.units.map(u => [u.number, u.reference]));
      if (numbers === null || numbers.some(n => !known.has(n))) {
        showStageNotice("warn", `“${unitsInput.value}” names a ${planning.unit_word} that is not `
          + "in the source. Use numbers like 4–9 or 4, 6.");
        return;
      }
      sources = numbers.map(n => structuredClone(known.get(n)));
    }
    const edited = {
      title: select("#edit-title").value, summary: select("#edit-summary").value,
      how: select("#edit-how").value,
      ...(sources ? { sources } : {}),
      picture_paths: [...planViewState.editingPictures],
      pictures_chosen: planViewState.editingPicturesChosen,
    };
    planViewState.editingSectionId = null;
    change(plan => Object.assign(plan.sections.find(s => s.id === id) ?? {}, edited));
  };
  const remove = select("#delete-section-button");
  if (remove) remove.onclick = () => {
    const id = planViewState.editingSectionId;
    if (!window.confirm("Delete this section and its scenes?")) return;
    planViewState.editingSectionId = null;
    change(plan => { plan.sections = plan.sections.filter(s => s.id !== id); });
  };

  fitSceneBoxes();
  document.querySelectorAll(".plan-scenes textarea").forEach(box => {
    box.addEventListener("input", () => fitSceneBoxes(box));
  });

  // Scenes: edited in place, saved on change.
  document.querySelectorAll("[data-scene-field]").forEach(input => {
    input.onchange = () => {
      const sceneId = input.closest("[data-scene]").dataset.scene;
      const field = input.dataset.sceneField;
      let value = input.value;
      if (field === "seconds") value = Math.max(3, Math.min(900, Number(value) || 30));
      if (field === "slides") {
        value = parseUnits(value || "");
        if (value === null) {
          showStageNotice("warn", "Use numbers like 4–5 or 4, 6.");
          return;
        }
      }
      change(plan => {
        const scene = sectionOf(plan, input).scenes.find(s => s.id === sceneId);
        if (scene) scene[field] = value;
      });
    };
  });
  document.querySelectorAll("[data-scene-move]").forEach(button => {
    button.onclick = () => {
      const sceneId = button.closest("[data-scene]").dataset.scene;
      change(plan => {
        const scenes = sectionOf(plan, button).scenes;
        const at = scenes.findIndex(s => s.id === sceneId);
        const to = at + Number(button.dataset.sceneMove);
        if (at < 0 || to < 0 || to >= scenes.length) return;
        [scenes[at], scenes[to]] = [scenes[to], scenes[at]];
      });
    };
  });
  document.querySelectorAll("[data-scene-remove]").forEach(button => {
    button.onclick = () => {
      const sceneId = button.closest("[data-scene]").dataset.scene;
      change(plan => {
        const section = sectionOf(plan, button);
        section.scenes = section.scenes.filter(s => s.id !== sceneId);
      });
    };
  });
  document.querySelectorAll("[data-add-scene]").forEach(button => {
    button.onclick = () => change(plan => {
      sectionOf(plan, button).scenes.push(
        { id: newItemIdentifier(), does: "", slides: [], seconds: 30 });
    });
  });

  const add = select("#add-section-button");
  if (add) add.onclick = () => {
    const id = newItemIdentifier();
    planViewState.editingSectionId = id;
    planViewState.editingPictures = [];
    planViewState.editingPicturesChosen = false;
    change(plan => {
      plan.sections.push({
        id, title: "New section", summary: "", how: "", estimated_seconds: 30,
        sources: [], picture_paths: [],
        pictures_chosen: false,
        scenes: [{ id: newItemIdentifier(), does: "", slides: [], seconds: 30 }],
      });
    });
  };
}
