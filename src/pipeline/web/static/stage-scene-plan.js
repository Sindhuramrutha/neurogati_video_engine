/**
 * Scene Plan — four tabs, in the order the work happens.
 *
 * 1. Brief: what Extraction handed on, and the intent -- audience, learning
 *    objectives, key themes, video preferences.
 * 2. Outline: build it (follow the deck, draft with the agent, or by hand) and
 *    edit it. The agent only proposes; nothing changes until it is accepted.
 *    The plan is a lesson (`lesson_plan.py`): every section has a role, an
 *    Opening, Recap and Close wrap the body, time is shared from the target, and
 *    objective links and summaries are proposed, never imposed.
 * 3. Check: fixed rules over the plan, each pass / warn / fail with why.
 * 4. Final & transfer: later stages read the transferred plan
 *    (`plan_handoff.py`); a failing check blocks the transfer.
 *
 * Every pane is drawn and only the chosen one shown, so a tab change never
 * redraws the page or loses an edit in progress.
 *
 * The plan is the stage's output and is edited directly. It can also be drafted
 * by the Planning agent from the whole extraction; a draft is shown next to the
 * current plan and taken whole or section by section, never written over it.
 *
 * The bar at the top says where the plan stands against the extraction: nothing
 * extracted, a draft waiting, out of date, not linked, or matching. Before that
 * bar existed a plan could describe a chapter the extraction no longer held, and
 * nothing on the page could tell.
 *
 * Ordinary edits go through `editStageDocument`, which applies the change,
 * re-renders, persists, and rolls back on failure. Drafting, accepting and
 * confirming are single server operations and simply reload afterwards.
 */

import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, footerNav, icon, moveToNextLayerButton, notBuiltYet,
  projectApiPath, refreshProjectSummary, select, showStageNotice, stageHeader, stageNeighbours,
  whenItWas, wireGotoButtons,
} from "/static/ui-kit.js";

const PLAN_TABS = [
  ["brief", "Brief"], ["outline", "Outline"], ["check", "Check"], ["final", "Final & transfer"],
];

const currentPlanTab = () =>
  PLAN_TABS.some(([key]) => key === applicationState.planTab) ? applicationState.planTab : "brief";

/** View state only — it must not survive a reload or leak into the saved plan. */
const planViewState = {
  editingSectionId: null,
  editingSources: [],
  draggingSectionId: null,
  isDrafting: false,
  isActing: false,
  draftInstruction: "",
  // The approach being chosen, before it is built with. Null: what the plan has.
  approachKey: null,
  approachOptions: null,
  approachNotes: null,
};

const RENDERING_APPROACHES = [
  ["composition", "Composition", "Labelled diagrams, flows, comparisons"],
  ["plot", "Plot", "Real data on axes"],
  ["simulation", "Simulation", "A physical system in motion"],
  ["code", "Code", "Source code walked through"],
  ["still", "Still", "One frame that teaches the point"],
];
const approachLabel = key => RENDERING_APPROACHES.find(([k]) => k === key)?.[1] ?? "";

const FRAME_ROLES = ["opening", "recap", "close"];
const isFrame = section => FRAME_ROLES.includes(section.role);
const ROLE_NAMES = { opening: "Opening", teach: "Teach", story: "Story", recap: "Recap",
                     close: "Close" };
const FRAME_HELP = {
  opening: "A hook, then what the viewer will be able to do by the end — your objectives.",
  recap: "Back through each objective, one short beat each, from what the sections said.",
  close: "The one idea to keep, and something to think about next.",
};
const minutes = seconds => `${(seconds / 60).toFixed(1)} min`;

function formatDuration(totalSeconds) {
  if (totalSeconds < 60) return `~ ${totalSeconds} sec`;
  return `~ ${Math.round(totalSeconds / 60)} min`;
}

/** Where a section draws from, in the source's own terms: "Slide 3", or the
 *  heading path. The project has one source file, so its name is never needed. */
const referenceLabel = reference => reference.slide_number
  ? `Slide ${reference.slide_number}${reference.heading_path.length
      ? ` · ${reference.heading_path.at(-1)}` : ""}`
  : reference.heading_path.length ? reference.heading_path.join(" › ") : "The whole source";

export async function renderScenePlanStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  if (!body.querySelector(".plan-bar")) {
    body.innerHTML = `<div class="card muted">Loading plan…</div>`;
  }

  let plan;
  let settings;
  let draft = null;
  try {
    [plan, settings] = await Promise.all([
      loadStageDocument("plan", "/plan"),
      requestJsonFromApi(projectApiPath(`/settings/${stage.key}`)),
    ]);
    // loadStageDocument returns null when the project changed mid-request.
    if (plan === null) return;
    applicationState.stageSettings[stage.key] = settings;
    if (plan.has_pending_draft) {
      draft = await requestJsonFromApi(projectApiPath("/plan/draft"));
      if (!draft.is_pending) draft = null;
    }
  } catch (loadFailure) {
    console.error("plan load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load the plan.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }

  // Whether the sources are a deck, and whether the plan still follows it. Its
  // own request because a failure here should cost the slide controls and not
  // the page.
  let slides = null;
  let handoff = { checks: [], failing: 0, warning: 0, has_transferred: false, pending: false };
  try {
    [slides, handoff] = await Promise.all([
      requestJsonFromApi(projectApiPath("/plan/slide-coverage")),
      requestJsonFromApi(projectApiPath("/plan/handoff")),
    ]);
  } catch (coverageFailure) {
    console.error("slide coverage or hand-off load failed", coverageFailure);
  }
  const tab = currentPlanTab();
  const pane = (key, content) =>
    `<section class="plan-pane" data-plan-pane="${key}" ${key === tab ? "" : "hidden"}>${content}</section>`;

  // The bar already speaks for the plan's relationship to the extraction, so
  // the notice carries only the plan's own problems.
  const freshnessWarnings = new Set(plan.freshness?.warnings ?? []);
  const ownWarnings = plan.warnings.filter(warning => !freshnessWarnings.has(warning));

  body.innerHTML = `
    ${stageHeader("scene-plan", "Scene Plan", {
      agentButtonId: "planning-agent-button",
    })}

    <div class="stage-content stage-content-bare">
      <div class="extraction-tabs plan-tabs">
        <nav class="x-tabs" role="tablist" aria-label="Scene Plan steps">
          ${PLAN_TABS.map(([key, label], index) => `
            <button role="tab" class="x-tab ${key === tab ? "on" : ""}" data-plan-tab="${key}"
                    aria-selected="${key === tab}">
              <span class="x-tab-number">${index + 1}</span>
              <b class="x-tab-label">${label}</b>
              ${key === "check" && handoff.failing ? `<span class="plan-tab-count fail">${handoff.failing}</span>`
                : key === "check" && handoff.warning ? `<span class="plan-tab-count warn">${handoff.warning}</span>` : ""}
            </button>`).join("")}
        </nav>
        <div class="x-tab-body" role="tabpanel">
          ${pane("brief", renderBrief(plan, settings, slides))}
          ${pane("outline", `
            ${renderPlanBar(plan, slides)}
            ${ownWarnings.length ? `
              <div class="notice warn" style="margin-bottom:14px">
                ${ownWarnings.map(escapeHtml).join(" · ")}
              </div>` : ""}
            <div class="plan-grid">
              ${renderOutlinePanel(plan)}
              <div>${draft ? renderDraftPanel(draft, plan) : renderApproachPicker(plan)}</div>
            </div>`)}
          ${pane("check", renderChecks(handoff))}
          ${pane("final", renderFinal(plan, handoff, stage))}
        </div>
      </div>

      ${renderFooterNav(stage, handoff, tab)}
    </div>`;

  lastHandoff = handoff;
  currentNavigate = navigateToStage;
  currentAgentRenderer = renderAgentStage;
  wireScenePlanStage(stage, navigateToStage, renderAgentStage, draft);
}

/* ---- the plan against the extraction ------------------------------------ */

function renderPlanBar(plan, slides) {
  const freshness = plan.freshness ?? {};
  const slideCount = slides?.slide_count ?? 0;
  const documents = plan.source_outline ?? [];
  const headingCount = documents.reduce((sum, d) => sum + d.headings.length, 0);
  const missing = freshness.sections_with_missing_sources ?? [];
  const withoutSources = freshness.sections_without_sources ?? [];

  const bar = (tone, iconPaths, title, detail, actions = "") => `
    <div class="run-bar plan-bar ${tone}">
      <span class="run-icon">${icon(iconPaths, 17, 2.2)}</span>
      <span class="run-text"><b>${title}</b><span>${detail}</span></span>
      ${actions ? `<span class="plan-actions">${actions}</span>` : ""}
    </div>`;

  // Building is chosen in "How to build the outline", beside the plan.
  const draftControls = () => "";

  /**
   * Following the deck is a different kind of decision from drafting.
   *
   * A draft asks a model to group the material, which is right for a chapter or
   * a paper. A deck has already been divided and ordered by whoever made it, so
   * following it is mechanical: one section per slide, every slide, in order.
   * Offered wherever a draft is, because it is the better answer whenever the
   * source is a deck.
   */
  const deckButton = slideCount
    ? `<button class="btn" id="plan-from-slides-button"
               title="One section per slide, in the deck's order, every slide"
        >Follow the deck (${slideCount} slides)</button>`
    : "";
  const keepButton = `<button class="btn" id="confirm-plan-button"
      title="I have checked this plan against the current extraction">Keep plan as is</button>`;

  if (!freshness.has_extraction) {
    return bar("blocked", ICON.alert, "Nothing extracted yet",
      "A plan is drafted from what your documents say. Extract them first.",
      `<button class="btn btn-accent" data-goto="extraction">Go to Extraction</button>`);
  }

  if (planViewState.isDrafting) {
    return bar("working", ICON.doc, "Drafting from the source…",
      `Reading all ${headingCount} headings, then writing each section from its own text.
       This can take a minute or two; it is saved as a draft even if you leave this page.`);
  }

  const scope = `${headingCount} headings extracted`;

  if (plan.has_pending_draft) {
    return bar("pending", ICON.doc, "A drafted plan is waiting for review",
      "Accept all of it, add sections one by one, or discard it. Your plan is unchanged until you do.",
      draftControls("Redraft"));
  }

  if (!plan.sections.length) {
    return bar("ready", ICON.check, "No outline yet",
      `${escapeHtml(scope)}. Choose how to build it, on the right.`);
  }

  if (freshness.is_stale) {
    const extra = missing.length
      ? ` ${missing.length} section(s) point at content that is gone.` : "";
    return bar("stale", ICON.alert, "Out of date with your extraction",
      `The extracted content changed since this plan was drafted or checked.${extra}`,
      draftControls("Redraft") + keepButton);
  }

  if (freshness.is_unlinked) {
    return bar("stale", ICON.alert, "Not linked to your extraction",
      "Nothing records which extracted content each section covers, so this plan cannot be "
      + "checked against it.",
      draftControls("Draft from extraction") + keepButton);
  }

  if (missing.length) {
    return bar("stale", ICON.alert,
      `${missing.length} section(s) point at content that is no longer extracted`,
      escapeHtml(missing.map(m => m.title || "Untitled").join(" · ")),
      draftControls("Redraft"));
  }

  if (slides && slides.follows_the_deck) {
    return bar("ready", ICON.check,
      `Following the deck: all ${slides.slide_count} slides, in order`,
      `${slides.scene_count} scene(s) across ${slides.slide_count} slide(s)`
      + ` — ${slides.scenes_per_slide} per slide. Every slide is covered and none is`
      + ` out of order.`,
      draftControls("Redraft"));
  }
  if (slides && slides.warnings.length) {
    return bar("stale", ICON.alert, "This plan no longer follows the deck",
      slides.warnings.map(escapeHtml).join(" · "),
      draftControls("Redraft"));
  }

  const note = withoutSources.length
    ? `${withoutSources.length} section(s) have no source content recorded.`
    : escapeHtml(scope);
  return bar("ready", ICON.check, "Matches the current extraction", note, draftControls("Redraft"));
}

/* ---- outline ------------------------------------------------------------ */

function renderOutlinePanel(plan) {
  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Video outline</h3>
        <div class="spacer"></div>
        <span class="plan-total">${plan.sections.length} sections ·
          ${formatDuration(plan.total_estimated_seconds)}</span>
      </div>
      ${renderTimingStrip(plan)}
      ${renderLessonTools(plan)}
      <p class="panel-sub">Drag to reorder the body, or click a section to edit it. The
        Opening stays first; the Recap and Close stay last.</p>

      <div id="outline-list">
        ${plan.sections.length
          ? plan.sections.map((section, index) => renderOutlineRow(section, index, plan)).join("")
          : `<p class="muted" style="font-size:12.5px;margin:0 0 10px">
               No sections yet. Draft a plan from your extraction, or add one by hand.</p>`}
      </div>

      <button class="add-row" id="add-section-button">
        ${icon(ICON.plus)} Add new section
      </button>
    </div>`;
}

/** The plan as a timeline: each section's share of the video, coloured by role. */
function renderTimingStrip(plan) {
  const timing = plan.lesson?.timing;
  if (!plan.sections.length || !timing) return "";
  const tone = timing.is_stretched || timing.is_squeezed ? "warn" : "ok";
  const verdict = timing.is_stretched
    ? `That is stretched ×${timing.scale}, so the narration will pad. Choose a shorter target,
       or add material.`
    : timing.is_squeezed
      ? `That is squeezed ×${timing.scale}, so each section is cut hard. Choose a longer
         target, or split the video.`
      : timing.scale === 1 ? "It fits the target as it is."
        : `Shared out ×${timing.scale} to fit.`;
  return `
    <div class="plan-strip" role="img" aria-label="The video's sections, by length">
      ${plan.sections.map((section, index) => `
        <span class="plan-strip-cell role-${section.role}" style="flex:${Math.max(1, section.estimated_seconds)}"
              title="${index + 1}. ${escapeHtml(section.title || "Untitled")} · ${
                formatDuration(section.estimated_seconds)}"></span>`).join("")}
    </div>
    <p class="plan-strip-note ${tone}">The material needs about <b>${minutes(timing.needed_total)}</b>;
      the target is <b>${escapeHtml(timing.target_phrase)}</b>. ${verdict}</p>`;
}

/** What can be done to the plan as a whole: summaries and objective links. */
function renderLessonTools(plan) {
  const summaries = plan.lesson?.summaries ?? {};
  const proposals = Object.keys(summaries.proposals ?? {}).length;
  const suggestions = plan.lesson?.objective_suggestions ?? [];
  const tools = [];
  if (summaries.needing) {
    tools.push(`<button class="btn" id="write-summaries-button" data-everything="false">
      AI · write ${summaries.needing} summar${summaries.needing === 1 ? "y" : "ies"}
      <span class="fact warn">1 AI call</span></button>`);
  } else if (summaries.teaching_sections) {
    tools.push(`<button class="btn" id="write-summaries-button" data-everything="true">
      AI · rewrite all ${summaries.teaching_sections} summaries
      <span class="fact warn">1 AI call</span></button>`);
  }
  if (proposals) {
    tools.push(`<button class="btn btn-accent" id="accept-summaries-button">
      Use all ${proposals} proposed summar${proposals === 1 ? "y" : "ies"}</button>`,
      `<button class="btn" id="dismiss-summaries-button">Dismiss them</button>`);
  }
  if (suggestions.length) {
    tools.push(`<button class="btn" id="link-objectives-button">
      Link ${suggestions.length} suggested objective${suggestions.length === 1 ? "" : "s"}</button>`);
  }
  return tools.length ? `<div class="plan-tools">${tools.join("")}</div>` : "";
}

/** The numbers of the plan's learning objectives a section serves. */
function objectiveNumbersFor(section, plan) {
  return (section.objective_ids ?? [])
    .map(id => plan.learning_objectives.findIndex(o => o.id === id) + 1)
    .filter(number => number > 0);
}

function renderObjectiveFact(section, plan) {
  const numbers = objectiveNumbersFor(section, plan);
  return numbers.length
    ? `<div class="section-facts"><span class="fact" title="Learning objectives this section serves">
         objective${numbers.length === 1 ? "" : "s"} ${numbers.join(", ")}</span></div>`
    : "";
}

/** Small facts under a section: how it is shown, what it draws on, what it serves. */
function renderSectionFacts(section, plan, { missing = [] } = {}) {
  const usesSources = plan.freshness?.is_linked
    || plan.sections.some(s => (s.sources ?? []).length);
  const objectiveNumbers = objectiveNumbersFor(section, plan);
  const sources = section.sources ?? [];

  const facts = [];
  if (isFrame(section)) {
    facts.push(`<span class="fact muted" title="${escapeHtml(FRAME_HELP[section.role])}">
      written from the plan</span>`);
  }
  if (section.rendering_approach && !isFrame(section)) {
    facts.push(`<span class="fact approach ${escapeHtml(section.rendering_approach)}"
      title="${escapeHtml(section.rendering_reason || "")}">${
        escapeHtml(approachLabel(section.rendering_approach))}</span>`);
  }
  if (isFrame(section)) {
    // A frame section is written from the plan, so "no source" would be noise.
  } else if (sources.length) {
    facts.push(`<span class="fact" title="${escapeHtml(sources.map(referenceLabel).join("\n"))}">
      ${sources.length} source${sources.length === 1 ? "" : "s"}</span>`);
  } else if (usesSources) {
    facts.push(`<span class="fact muted">no source</span>`);
  }
  if (missing.length) {
    facts.push(`<span class="fact bad" title="${escapeHtml(missing.join("\n"))}">
      source missing</span>`);
  }
  if (objectiveNumbers.length) {
    facts.push(`<span class="fact" title="Learning objectives this section serves">
      objective${objectiveNumbers.length === 1 ? "" : "s"} ${objectiveNumbers.join(", ")}</span>`);
  }
  return facts.length ? `<div class="section-facts">${facts.join("")}</div>` : "";
}

function renderOutlineRow(section, index, plan) {
  if (planViewState.editingSectionId === section.id) {
    return renderSectionEditor(section, index, plan);
  }

  const isOddDuration = section.estimated_seconds < 10 || section.estimated_seconds > 600;
  const missing = (plan.freshness?.sections_with_missing_sources ?? [])
    .find(entry => entry.section_id === section.id)?.missing ?? [];

  const problem = plan.lesson?.summary_problems?.[section.id] ?? "";
  const proposal = plan.lesson?.summaries?.proposals?.[section.id];
  const suggestions = (plan.lesson?.objective_suggestions ?? [])
    .filter(suggestion => suggestion.section_id === section.id);
  const objectiveNumber = id => plan.learning_objectives.findIndex(o => o.id === id) + 1;
  const frame = isFrame(section);

  return `
    <div class="outline-row role-${section.role} ${missing.length ? "has-missing" : ""}"
         data-section="${section.id}" ${frame ? "" : `draggable="true"`}>
      <span class="grip" aria-hidden="true" ${frame ? "hidden" : ""}>
        ${icon(`<circle cx="9" cy="6" r="1.4"/><circle cx="9" cy="12" r="1.4"/>
                <circle cx="9" cy="18" r="1.4"/><circle cx="15" cy="6" r="1.4"/>
                <circle cx="15" cy="12" r="1.4"/><circle cx="15" cy="18" r="1.4"/>`, 15, 0)}
      </span>
      <span class="outline-num">${index + 1}</span>
      <div class="outline-body">
        <div class="title ${section.title ? "" : "untitled"}">
          <span class="role-chip role-${section.role}">${ROLE_NAMES[section.role] ?? "Teach"}</span>
          ${escapeHtml(section.title || "Untitled section")}</div>
        ${section.summary ? `<div class="summary ${problem ? "has-problem" : ""}">${
          escapeHtml(section.summary)}</div>` : ""}
        ${problem ? `<div class="summary-problem">Summary: ${escapeHtml(problem)}</div>` : ""}
        ${proposal ? `
          <div class="summary-proposal">
            <span class="fact warn">AI proposes</span>
            <span>${escapeHtml(proposal.summary)}</span>
            ${proposal.talks_about_source ? `<span class="fact bad">talks about the source</span>` : ""}
            <button class="btn" data-accept-summary="${section.id}">Use</button>
            <button class="btn" data-dismiss-summary="${section.id}">Dismiss</button>
          </div>` : ""}
        ${renderSectionFacts(section, plan, { missing })}
        ${suggestions.length ? `
          <div class="objective-suggestions">${suggestions.map(suggestion => `
            <button class="suggestion-chip" data-link-section="${section.id}"
                    data-link-objective="${suggestion.objective_id}"
                    title="Shares: ${escapeHtml(suggestion.words.join(", "))}">
              + objective ${objectiveNumber(suggestion.objective_id)}
              <span>${escapeHtml(suggestion.words.join(", "))}</span></button>`).join("")}
          </div>` : ""}
      </div>
      <span class="outline-duration ${isOddDuration ? "odd" : ""}"
            title="${section.pinned ? "Pinned: a length you set" : "Shared out from the target"}">
        ${section.pinned ? `<button class="pin-chip" data-unpin="${section.id}"
            title="Pinned. Click to let it follow the target again">pinned ×</button>` : ""}
        ${formatDuration(section.estimated_seconds)}</span>
      <button class="btn-icon" data-edit-section="${section.id}"
              title="Edit" aria-label="Edit ${escapeHtml(section.title || "section")}">
        ${icon(`<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/>`, 15, 1.8)}
      </button>
    </div>`;
}

function renderSectionEditor(section, index, plan) {
  const outline = plan.source_outline ?? [];
  const sourceOptions = outline.map(document => `
      <option value="${escapeHtml(JSON.stringify({ file_name: document.file_name, heading_path: [] }))}"
        >The whole source · ${document.words} words</option>
      ${document.headings.map(heading => `
        <option value="${escapeHtml(JSON.stringify({
          file_name: document.file_name, heading_path: heading.heading_path }))}"
          >${"  ".repeat(Math.max(0, heading.level - 1))}${
            escapeHtml(heading.heading_path.at(-1) ?? "")} · ${heading.words} words</option>`).join("")}
    `).join("");

  const frame = isFrame(section);
  return `
    <div class="outline-row editing" data-section="${section.id}">
      <span class="outline-num">${index + 1}</span>
      <div class="outline-edit">
        <input id="edit-title" value="${escapeHtml(section.title)}"
               placeholder="Section title" maxlength="120" aria-label="Section title">
        <textarea id="edit-summary" placeholder="In one line: what the viewer learns"
                  maxlength="400" aria-label="Section summary">${escapeHtml(section.summary)}</textarea>

        ${frame ? `<p class="muted edit-hint">${escapeHtml(FRAME_HELP[section.role])} Written
          from the plan, so it names no source.</p>` : `
        <div class="edit-field">
          <label>Its part in the lesson</label>
          <div class="seg" id="edit-role">
            ${["teach", "story"].map(role => `
              <button type="button" class="${section.role === role ? "on" : ""}" data-role="${role}">
                ${ROLE_NAMES[role]}</button>`).join("")}
          </div>
          <p class="muted edit-hint">Story: told first hand, in order, then what it shows.</p>
        </div>`}

        <div class="edit-field" ${frame ? "hidden" : ""}>
          <label for="edit-approach">How to show it</label>
          <div class="edit-pair">
            <select id="edit-approach">
              <option value="">Not chosen</option>
              ${RENDERING_APPROACHES.map(([key, label, hint]) => `
                <option value="${key}" ${section.rendering_approach === key ? "selected" : ""}
                  >${label} — ${hint}</option>`).join("")}
            </select>
            <input id="edit-reason" maxlength="240" placeholder="Why, in one sentence"
                   value="${escapeHtml(section.rendering_reason ?? "")}" aria-label="Why">
          </div>
        </div>

        <div class="edit-field" ${frame ? "hidden" : ""}>
          <label for="edit-add-source">Source content</label>
          <div id="edit-sources" class="source-chips"></div>
          ${outline.length
            ? `<select id="edit-add-source">
                 <option value="">Add extracted content…</option>${sourceOptions}
               </select>`
            : `<p class="muted edit-hint">Nothing extracted yet to point at.</p>`}
        </div>

        ${plan.learning_objectives.length && !frame ? `
          <div class="edit-field">
            <label>Learning objectives it serves</label>
            <div class="edit-objectives">
              ${plan.learning_objectives.map((objective, number) => `
                <label class="edit-objective">
                  <input type="checkbox" data-edit-objective-link="${objective.id}"
                         ${(section.objective_ids ?? []).includes(objective.id) ? "checked" : ""}>
                  <span><b>${number + 1}.</b> ${escapeHtml(objective.text)}</span>
                </label>`).join("")}
            </div>
          </div>` : ""}

        <div class="edit-row">
          <label for="edit-seconds">Seconds</label>
          <input id="edit-seconds" type="number" min="1" max="3600"
                 value="${section.estimated_seconds}" data-was="${section.estimated_seconds}">
          <label class="edit-pin"><input type="checkbox" id="edit-pinned"
            ${section.pinned ? "checked" : ""}> Pin this length</label>
          <div class="spacer" style="flex:1"></div>
          <button class="btn btn-accent" id="save-section-button">Done</button>
          ${frame ? "" : `<button class="btn-icon danger" id="delete-section-button"
                  title="Delete section" aria-label="Delete section">
            ${icon(`<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>`, 16, 1.8)}
          </button>`}
        </div>
      </div>
    </div>`;
}

/** The chosen sources, redrawn in place: re-rendering the stage would throw away
 *  a title or summary typed but not yet saved. */
function renderEditingSources() {
  const host = select("#edit-sources");
  if (!host) return;
  host.innerHTML = planViewState.editingSources.length
    ? planViewState.editingSources.map((reference, position) => `
        <span class="source-chip" title="${escapeHtml(referenceLabel(reference))}">
          ${escapeHtml(referenceLabel(reference))}
          <button type="button" data-remove-source="${position}"
                  aria-label="Remove this source">×</button>
        </span>`).join("")
    : `<span class="muted edit-hint">None yet.</span>`;

  host.querySelectorAll("[data-remove-source]").forEach(button => {
    button.onclick = () => {
      planViewState.editingSources.splice(Number(button.dataset.removeSource), 1);
      renderEditingSources();
    };
  });
}

/* ---- a drafted plan, next to the current one ----------------------------- */

function renderDraftPanel(draft, currentPlan) {
  const proposed = draft.plan;
  const accepted = new Set(draft.accepted_section_ids ?? []);
  const notes = draft.notes ?? [];
  const drafted = draft.created_at ? new Date(draft.created_at).toLocaleString() : "";

  return `
    <div class="panel draft-panel">
      <div class="panel-head">
        <h3>Proposed plan</h3>
        <div class="spacer"></div>
        <span class="plan-total">${proposed.sections.length} sections ·
          ${formatDuration(proposed.total_estimated_seconds)}</span>
      </div>
      <p class="panel-sub">
        Drafted by the ${escapeHtml(draft.agent ?? "Scene Plan")} agent from the source's
        ${draft.headings_read ?? 0} headings
        ${drafted ? `· ${escapeHtml(drafted)}` : ""}
        ${draft.instruction ? `· guidance: “${escapeHtml(draft.instruction)}”` : ""}
      </p>

      <div class="draft-actions">
        <button class="btn btn-accent" id="accept-draft-button">Accept all</button>
        <button class="btn" id="discard-draft-button">Discard</button>
      </div>

      ${draft.replaces_narrated_sections && currentPlan.sections.length ? `
        <div class="notice warn draft-notice">
          <b>Accept all</b> replaces your ${currentPlan.sections.length} current section(s).
          Narration already written for ${draft.replaces_narrated_sections} of them in
          Script &amp; Staging is kept, but no longer attached to a section.
          Use <b>Add to plan</b> to keep your sections and add these alongside.
        </div>` : ""}

      ${draft.is_behind_extraction ? `
        <div class="notice warn draft-notice">
          The extraction changed after this draft was made. Redraft to plan from what is
          extracted now.
        </div>` : ""}

      ${notes.length ? `
        <details class="draft-notes">
          <summary>Notes from drafting (${notes.length})</summary>
          <ul>${notes.map(note => `<li>${escapeHtml(note)}</li>`).join("")}</ul>
        </details>` : ""}

      ${proposed.learning_objectives.length ? `
        <div class="draft-objectives">
          <b>Learning objectives</b>
          <ol>${proposed.learning_objectives.map(o => `<li>${escapeHtml(o.text)}</li>`).join("")}</ol>
        </div>` : ""}

      ${proposed.key_themes.length ? `
        <div class="pill-row draft-themes">
          ${proposed.key_themes.map(theme => `<span class="pill theme">${escapeHtml(theme)}</span>`)
            .join("")}
        </div>` : ""}

      <div class="draft-sections">
        ${proposed.sections.map((section, index) => `
          <div class="draft-section ${accepted.has(section.id) ? "added" : ""}">
            <div class="draft-section-head">
              <span class="outline-num">${index + 1}</span>
              <b>${escapeHtml(section.title || "Untitled section")}</b>
              <div class="spacer"></div>
              <span class="outline-duration">${formatDuration(section.estimated_seconds)}</span>
            </div>
            ${section.summary ? `<p class="summary">${escapeHtml(section.summary)}</p>` : ""}
            ${section.rendering_approach ? `
              <p class="draft-approach">
                <span class="fact approach ${escapeHtml(section.rendering_approach)}">
                  ${escapeHtml(approachLabel(section.rendering_approach))}</span>
                ${escapeHtml(section.rendering_reason ?? "")}
              </p>` : ""}
            <div class="source-chips">
              ${(section.sources ?? []).map(reference => `
                <span class="source-chip">${escapeHtml(referenceLabel(reference))}</span>`).join("")
                || `<span class="fact bad">no source content</span>`}
            </div>
            ${renderObjectiveFact(section, proposed)}
            <div class="draft-section-actions">
              ${accepted.has(section.id)
                ? `<span class="fact ok">added to your plan</span>`
                : `<button class="btn" data-accept-section="${section.id}">Add to plan</button>`}
            </div>
          </div>`).join("")}
      </div>
    </div>`;
}

/* ---- side panels -------------------------------------------------------- */

function renderObjectivesPanel(plan) {
  const coverage = plan.objective_coverage ?? {};
  const isLinked = plan.sections.some(section => (section.objective_ids ?? []).length);
  const sectionNumber = id => plan.sections.findIndex(section => section.id === id) + 1;

  return `
    <div class="panel" style="margin-bottom:14px">
      <div class="panel-head">
        <h3>Learning objectives</h3>
        <div class="spacer"></div>
        <button class="btn-icon" id="add-objective-button"
                title="Add objective" aria-label="Add objective">${icon(ICON.plus, 15)}</button>
      </div>
      <p class="panel-sub">What should the viewer learn from this video?</p>

      ${plan.learning_objectives.length
        ? plan.learning_objectives.map((objective, number) => {
            const covering = (coverage[objective.id] ?? []).map(sectionNumber).filter(Boolean);
            const coverageChip = !isLinked || !objective.is_included ? ""
              : covering.length
                ? `<span class="fact ok" title="Sections that serve this objective">§ ${covering.join(", ")}</span>`
                : `<span class="fact warn">not covered</span>`;
            return `
          <div class="objective-row">
            <span class="checkbox ${objective.is_included ? "on" : ""}"
                  data-toggle-objective="${objective.id}" role="checkbox"
                  aria-checked="${objective.is_included}"
                  aria-label="Include this objective">
              ${icon(ICON.check, 11, 3.5)}
            </span>
            <span class="objective-number">${number + 1}</span>
            <span class="text ${objective.is_included ? "" : "off"}"
                  data-edit-objective="${objective.id}" title="Click to edit"
                  >${escapeHtml(objective.text || "(empty)")}</span>
            ${coverageChip}
            <button class="btn-icon danger" data-delete-objective="${objective.id}"
                    title="Remove" aria-label="Remove objective">
              ${icon(`<path d="M18 6 6 18M6 6l12 12"/>`, 14, 2)}
            </button>
          </div>`;
          }).join("")
        : `<p class="muted" style="font-size:12.5px;margin:0">
             None yet. These guide what Script &amp; Staging emphasises.</p>`}
    </div>`;
}

function renderFramePanel(plan) {
  const on = new Set(plan.lesson_frame ?? []);
  return `
    <div class="panel lesson-frame-panel" style="margin-bottom:14px">
      <div class="panel-head"><h3>The lesson frame</h3></div>
      <p class="panel-sub">Wrapped around the body so the video teaches, rather than starting
        cold on the first slide. Written from the plan, not the source.</p>
      ${FRAME_ROLES.map(part => `
        <button class="toggle-row" data-frame-part="${part}" role="checkbox"
                aria-checked="${on.has(part)}">
          <span class="checkbox ${on.has(part) ? "on" : ""}">${on.has(part) ? icon(ICON.check, 13, 3.5) : ""}</span>
          <span class="toggle-label"><b>${ROLE_NAMES[part]}</b> — ${escapeHtml(FRAME_HELP[part])}</span>
        </button>`).join("")}
    </div>`;
}

function renderAudiencePanel(plan) {
  return `
    <div class="panel" style="margin-bottom:14px">
      <div class="panel-head"><h3>Target audience</h3></div>
      <p class="panel-sub">Helps tailor the tone and depth.</p>
      <div class="pill-row">
        ${plan.audience_choices.map(audience => `
          <button class="pill ${audience === plan.selected_audience ? "on" : ""}"
                  data-audience="${escapeHtml(audience)}"
                  aria-pressed="${audience === plan.selected_audience}">
            ${escapeHtml(audience)}</button>`).join("")}
        <button class="pill ghost" id="add-audience-button">${icon(ICON.plus, 12)} Add</button>
      </div>
    </div>`;
}

function renderPreferencesPanel(settings) {
  return `
    <div class="panel" style="margin-bottom:14px">
      <div class="panel-head">
        <h3>Video preferences</h3>
        <div class="spacer"></div>
        <span class="mono muted" id="settings-saved-hint"></span>
      </div>
      ${settings.options.map(option => {
        const currentValue = settings.values[option.key];
        const activeChoice = option.choices.find(choice => choice.value === currentValue);
        const inert = option.implemented === false;
        return `
          <div class="option${inert ? " inert" : ""}">
            <label for="pref-${escapeHtml(option.key)}">${escapeHtml(option.label)}
              ${notBuiltYet(option)}</label>
            <select id="pref-${escapeHtml(option.key)}" data-option="${escapeHtml(option.key)}"
                    ${inert ? "disabled" : ""}>
              ${option.choices.map(choice => `
                <option value="${escapeHtml(choice.value)}"
                        ${choice.value === currentValue ? "selected" : ""}>
                  ${escapeHtml(choice.label)}</option>`).join("")}
            </select>
            ${activeChoice?.help_text
              ? `<p class="help">${escapeHtml(activeChoice.help_text)}</p>` : ""}
          </div>`;
      }).join("")}
    </div>`;
}

function renderThemesPanel(plan) {
  return `
    <div class="panel">
      <div class="panel-head">
        <h3>Key themes</h3>
        <div class="spacer"></div>
        <button class="btn-icon" id="add-theme-button"
                title="Add theme" aria-label="Add theme">${icon(ICON.plus, 15)}</button>
      </div>
      <p class="panel-sub">Proposed from the source when a plan is drafted, or add your own.</p>
      <div class="pill-row">
        ${plan.key_themes.length
          ? plan.key_themes.map(theme => `
            <button class="pill theme" data-remove-theme="${escapeHtml(theme)}"
                    title="Click to remove">${escapeHtml(theme)}</button>`).join("")
          : `<span class="muted" style="font-size:12.5px">None yet.</span>`}
      </div>
    </div>`;
}

/* ---- 1. Brief --------------------------------------------------------------- */

function renderBrief(plan, settings, slides) {
  const documents = plan.source_outline ?? [];
  return `
    <div class="plan-brief">
      ${documents.length ? "" : `
        <section class="panel">
          <p class="muted">Nothing has been transferred from Extraction yet. The plan is built
            from what the source says.</p>
          <button class="btn btn-accent" data-goto="extraction">Go to Extraction</button>
        </section>`}
      ${renderAudiencePanel(plan)}
      ${renderObjectivesPanel(plan)}
      ${renderFramePanel(plan)}
      ${renderThemesPanel(plan)}
      ${renderPreferencesPanel(settings)}
    </div>`;
}

/* ---- 2. Outline: how a plan can be built ------------------------------------ */

function chosenApproach(plan) {
  const view = plan.approach_choices;
  const key = planViewState.approachKey ?? view.chosen;
  return {
    approach: view.approaches.find(a => a.key === key && a.available)
      ?? view.approaches.find(a => a.available),
    options: { ...view.chosen_options, ...(planViewState.approachOptions ?? {}) },
    notes: planViewState.approachNotes ?? view.notes ?? "",
  };
}

function renderApproachPicker(plan) {
  const view = plan.approach_choices;
  if (!view) return "";
  const { approach, options, notes } = chosenApproach(plan);
  const buildLabel = approach.key === "follow-deck" ? "Follow the deck"
    : approach.key === "by-hand" ? "Build it by hand"
      : `Draft it: ${approach.name}`;
  return `
    <div class="panel plan-approach">
      <div class="panel-head"><h3>How to build the outline</h3></div>
      <p class="panel-sub">Choose an approach. One marked <b>AI</b> proposes a draft beside
        your plan, and nothing changes until you accept it.</p>
      ${view.approaches.map(a => `
        <button class="x-pick plan-approach-pick ${a.key === approach.key ? "on" : ""}"
                data-approach="${a.key}" ${a.available ? "" : "disabled"}>
          <span class="x-pick-name">${escapeHtml(a.name)}
            ${a.uses_ai ? `<span class="fact warn">AI</span>` : `<span class="fact muted">no AI</span>`}
            ${a.available ? "" : `<span class="fact muted">needs a deck</span>`}</span>
          <span class="plan-approach-does">${escapeHtml(a.does)}</span>
          <span class="plan-approach-when">Best when: ${escapeHtml(a.when)}</span>
        </button>`).join("")}

      ${view.options.filter(option => !option.for_ai || approach.uses_ai).map(option => `
        <div class="edit-field">
          <label>${escapeHtml(option.label)}</label>
          <div class="seg plan-approach-option">
            ${Object.entries(option.choices).map(([value, label]) => `
              <button class="${options[option.key] === value ? "on" : ""}"
                      data-approach-option="${option.key}" data-value="${value}"
                      data-saves="${option.for_ai ? "" : "now"}">${escapeHtml(label)}</button>`).join("")}
          </div>
        </div>`).join("")}

      ${approach.uses_ai ? `
        <div class="edit-field">
          <label for="approach-notes">Anything else the plan should do</label>
          <textarea id="approach-notes" maxlength="600"
            placeholder="In your own words. For example: keep Padma's story together, and spend longest on the neural architecture."
            >${escapeHtml(notes)}</textarea>
        </div>` : ""}

      <button class="btn btn-accent" id="build-outline-button">${escapeHtml(buildLabel)}
        ${approach.uses_ai ? `<span class="fact warn">AI</span>` : ""}</button>
    </div>`;
}

/* ---- 3. Check --------------------------------------------------------------- */

const CHECK_LABELS = { pass: "Pass", warn: "Warning", fail: "Fails", "n/a": "Not applicable" };

function renderChecks(handoff) {
  return `
    <section class="panel">
      <div class="panel-head"><h3>The checks the plan goes through</h3></div>
      <p class="panel-sub">Fixed rules over the plan, the extraction and the deck — no AI,
        the same plan always gets the same result. A failing check blocks the transfer;
        a warning is shown and allowed.</p>
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

/* ---- 4. Final & transfer ---------------------------------------------------- */

function renderFinal(plan, handoff, stage) {
  const [tone, title, detail] = !plan.sections.length
    ? ["blocked", "Nothing to transfer yet", "Build the outline first."]
    : handoff.failing
      ? ["stale", `${handoff.failing} check(s) fail`, "Fix them on the Check tab; then transfer."]
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
  const objectives = plan.learning_objectives.filter(o => o.is_included);

  return `
    <div class="final-head ${tone}">
      <span class="run-icon">${icon(tone === "ready" ? ICON.check : ICON.alert, 18, 2.3)}</span>
      <span class="run-text">
        <b>${escapeHtml(title)}</b>
        <span>${escapeHtml(detail)}</span>
        <span class="final-totals">${plan.sections.length} section(s) · ${
          formatDuration(plan.total_estimated_seconds)} · ${objectives.length} objective(s) · ${
          handoff.warning} warning(s)</span>
      </span>
      ${tone === "ready" ? moveToNextLayerButton(stageNeighbours(stage).next, {
          carries: "The transferred plan goes on to be scripted." })
        : `<button class="btn btn-accent btn-transfer" id="transfer-plan-button"
                   ${canTransfer ? "" : "disabled"}>
             Transfer to the next layer ${icon(ICON.arrowRight)}</button>`}
    </div>
    <div class="assets-final">
      <section class="panel">
        <div class="panel-head"><h3>The outline (${plan.sections.length})</h3></div>
        <ol class="plan-final-list">
          ${plan.sections.map(section => `
            <li><span class="role-chip role-${section.role}">${ROLE_NAMES[section.role] ?? ""}</span>
              <b>${escapeHtml(section.title || "Untitled section")}</b>
              <span>${formatDuration(section.estimated_seconds)}</span></li>`).join("")}
        </ol>
      </section>
      <section class="panel">
        <div class="panel-head"><h3>For whom, and to what end</h3></div>
        <p><b>Audience:</b> ${escapeHtml(plan.selected_audience || "not chosen")}</p>
        ${objectives.length ? `<ol class="plan-final-list">${objectives.map(o =>
          `<li>${escapeHtml(o.text)}</li>`).join("")}</ol>` : `<p class="muted">No objectives.</p>`}
      </section>
    </div>`;
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

/* ---- server actions ------------------------------------------------------ */

/** One call to the server, then a fresh render. Each of these changes more than
 *  one field, and the server decides the result, so there is nothing sensible to
 *  apply optimistically. */
async function runPlanAction({ path, method = "POST", body, pending, done, rerender }) {
  if (planViewState.isActing) {
    showStageNotice("warn", "Still working on the last action — try again in a moment.");
    return;
  }
  planViewState.isActing = true;
  if (pending) showStageNotice("ok", pending);
  try {
    await requestJsonFromApi(projectApiPath(path), {
      method,
      headers: { "Content-Type": "application/json" },
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

async function draftPlan(rerender) {
  if (planViewState.isDrafting) {
    showStageNotice("warn", "A draft is already being written.");
    return;
  }
  planViewState.draftInstruction = select("#draft-instruction")?.value.trim() ?? "";
  planViewState.isDrafting = true;
  await rerender();
  try {
    await requestJsonFromApi(projectApiPath("/plan/draft"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ instruction: planViewState.draftInstruction }),
    });
    planViewState.isDrafting = false;
    await rerender();
    showStageNotice("ok", "Draft ready. Review it next to your current plan.");
  } catch (draftFailure) {
    console.error("drafting failed", draftFailure);
    planViewState.isDrafting = false;
    await rerender();
    showStageNotice("bad", `Could not draft a plan — ${draftFailure.message}`);
  }
}

/* ---- wiring ------------------------------------------------------------- */

function wireScenePlanStage(stage, navigateToStage, renderAgentStage, draft) {
  const rerender = () => renderScenePlanStage(stage, navigateToStage, renderAgentStage);
  const change = applyEdit => editStageDocument({
    documentKind: "plan", apiPathSuffix: "/plan", applyEdit, rerender,
  });

  select("#planning-agent-button").onclick = () => renderAgentStage(stage);

  // Tabs: shown and hidden in place -- every pane is already drawn.
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
      // The footer's forward button follows the tab.
      rerenderFooter(stage, tab);
      if (button.closest(".footer-nav")) {
        select(".x-tabs")?.scrollIntoView({ block: "start", behavior: "smooth" });
      }
    };
  });

  const transferButton = select("#transfer-plan-button");
  if (transferButton && !transferButton.disabled) {
    transferButton.onclick = () => runPlanAction({
      path: "/plan/transfer", rerender,
      done: "Transferred: the stages after this read exactly this plan.",
    });
  }

  wireGotoButtons(navigateToStage);

  // --- the plan against the extraction ---
  const fromSlides = document.querySelector("#plan-from-slides-button");
  if (fromSlides) {
    fromSlides.onclick = async () => {
      fromSlides.disabled = true;
      fromSlides.textContent = "Following the deck…";
      try {
        const built = await requestJsonFromApi(
          projectApiPath("/plan/from-slides"), { method: "POST" });
        showStageNotice("ok",
          `${built.section_count} section(s) from ${built.slide_count} slide(s), in the`
          + ` deck's order.`);
        await refreshProjectSummary();
      } catch (slideFailure) {
        console.error("planning from slides failed", slideFailure);
        showStageNotice("bad", slideFailure.message);
      }
      await rerender();
    };
  }

  wireApproachPicker(change, rerender);

  const draftButton = select("#draft-plan-button");
  if (draftButton) draftButton.onclick = () => draftPlan(rerender);
  select("#draft-instruction")?.addEventListener("keydown", event => {
    if (event.key === "Enter") draftPlan(rerender);
  });

  const confirmButton = select("#confirm-plan-button");
  if (confirmButton) {
    confirmButton.onclick = () => runPlanAction({
      path: "/plan/confirm-extraction", rerender,
      done: "Recorded: this plan matches the current extraction.",
    });
  }

  // --- reviewing a draft ---
  if (draft) {
    select("#accept-draft-button").onclick = () => runPlanAction({
      path: "/plan/draft/accept", body: {}, rerender,
      done: "The drafted plan is now your plan.",
    });
    select("#discard-draft-button").onclick = () => runPlanAction({
      path: "/plan/draft", method: "DELETE", rerender, done: "Draft discarded.",
    });
    document.querySelectorAll("[data-accept-section]").forEach(button => {
      button.onclick = () => runPlanAction({
        path: "/plan/draft/accept", body: { section_ids: [button.dataset.acceptSection] },
        rerender, done: "Section added to your plan.",
      });
    });
  }

  // --- outline ---
  select("#add-section-button").onclick = () => change(plan => {
    const newSection = {
      id: newItemIdentifier(),
      title: "", summary: "", estimated_seconds: 60, role: "teach", pinned: false,
      summary_origin: "", sources: [], rendering_approach: "", rendering_reason: "",
      objective_ids: [],
    };
    const tail = plan.sections.findIndex(s => s.role === "recap" || s.role === "close");
    plan.sections.splice(tail < 0 ? plan.sections.length : tail, 0, newSection);
    planViewState.editingSectionId = newSection.id;
    planViewState.editingSources = [];
  });

  document.querySelectorAll("[data-edit-section]").forEach(button => {
    button.onclick = () => {
      const section = applicationState.plan.sections
        .find(s => s.id === button.dataset.editSection);
      planViewState.editingSectionId = button.dataset.editSection;
      planViewState.editingSources = structuredClone(section?.sources ?? []);
      rerender();
    };
  });

  const titleInput = select("#edit-title");
  if (titleInput) {
    titleInput.focus();
    titleInput.setSelectionRange(titleInput.value.length, titleInput.value.length);
    renderEditingSources();

    const addSource = select("#edit-add-source");
    if (addSource) {
      addSource.onchange = () => {
        if (!addSource.value) return;
        const reference = JSON.parse(addSource.value);
        const key = JSON.stringify(reference);
        if (!planViewState.editingSources.some(existing => JSON.stringify(existing) === key)) {
          planViewState.editingSources.push(reference);
        }
        addSource.value = "";
        renderEditingSources();
      };
    }

    const commitEdit = () => {
      const editingId = planViewState.editingSectionId;
      const before = applicationState.plan.sections.find(s => s.id === editingId) ?? {};
      const secondsInput = select("#edit-seconds");
      const seconds = Number(secondsInput.value) || 60;
      // Typing a length is setting one: it is pinned, and the rest rebalance.
      const pinned = select("#edit-pinned").checked
        || String(seconds) !== secondsInput.dataset.was;
      const summary = select("#edit-summary").value;
      const edited = {
        title: select("#edit-title").value,
        summary,
        summary_origin: summary.trim() !== (before.summary ?? "").trim() ? "you"
          : before.summary_origin ?? "",
        role: select("#edit-role .on")?.dataset.role ?? before.role ?? "teach",
        pinned,
        estimated_seconds: seconds,
        rendering_approach: select("#edit-approach").value,
        rendering_reason: select("#edit-reason").value,
        sources: structuredClone(planViewState.editingSources),
        objective_ids: [...document.querySelectorAll("[data-edit-objective-link]:checked")]
          .map(box => box.dataset.editObjectiveLink),
      };
      planViewState.editingSectionId = null;
      planViewState.editingSources = [];
      change(plan => {
        const section = plan.sections.find(s => s.id === editingId);
        if (section) Object.assign(section, edited);
      });
    };

    select("#save-section-button").onclick = commitEdit;
    document.querySelectorAll("#edit-role [data-role]").forEach(button => {
      button.onclick = () => {
        document.querySelectorAll("#edit-role [data-role]")
          .forEach(other => other.classList.toggle("on", other === button));
      };
    });
    // Enter commits from the title field; the summary is multi-line so Enter
    // there must insert a newline rather than close the editor.
    titleInput.addEventListener("keydown", event => {
      if (event.key === "Enter") { event.preventDefault(); commitEdit(); }
      if (event.key === "Escape") {
        planViewState.editingSectionId = null;
        planViewState.editingSources = [];
        rerender();
      }
    });

    const deleteButton = select("#delete-section-button");
    if (deleteButton) deleteButton.onclick = () => {
      const editingId = planViewState.editingSectionId;
      planViewState.editingSectionId = null;
      planViewState.editingSources = [];
      change(plan => {
        plan.sections = plan.sections.filter(s => s.id !== editingId);
      });
    };
  }

  wireOutlineDragAndDrop(change);
  wireLessonControls(stage, change, rerender);

  // The Brief's panels are always drawn now, draft or not.
  // --- objectives ---
  select("#add-objective-button").onclick = () => change(plan => {
    plan.learning_objectives.push({
      id: newItemIdentifier(),
      text: "New objective", is_included: true,
    });
  });

  document.querySelectorAll("[data-toggle-objective]").forEach(box => {
    box.onclick = () => change(plan => {
      const objective = plan.learning_objectives
        .find(o => o.id === box.dataset.toggleObjective);
      if (objective) objective.is_included = !objective.is_included;
    });
  });

  document.querySelectorAll("[data-edit-objective]").forEach(textNode => {
    textNode.onclick = () => promptInline(textNode, currentText =>
      change(plan => {
        const objective = plan.learning_objectives
          .find(o => o.id === textNode.dataset.editObjective);
        if (objective) objective.text = currentText;
      }));
  });

  document.querySelectorAll("[data-delete-objective]").forEach(button => {
    button.onclick = () => change(plan => {
      const removedId = button.dataset.deleteObjective;
      plan.learning_objectives = plan.learning_objectives.filter(o => o.id !== removedId);
      // The server drops dangling links too; doing it here keeps the page right
      // during the save instead of after it.
      plan.sections.forEach(section => {
        section.objective_ids = (section.objective_ids ?? []).filter(id => id !== removedId);
      });
    });
  });

  // --- audience ---
  document.querySelectorAll("[data-audience]").forEach(pill => {
    pill.onclick = () => change(plan => {
      plan.selected_audience = pill.dataset.audience;
    });
  });

  select("#add-audience-button").onclick = () => {
    const audience = window.prompt("Describe the audience");
    if (!audience?.trim()) return;
    change(plan => {
      const trimmed = audience.trim().slice(0, 80);
      if (!plan.audience_choices.includes(trimmed)) plan.audience_choices.push(trimmed);
      plan.selected_audience = trimmed;
    });
  };

  // --- themes ---
  select("#add-theme-button").onclick = () => {
    const theme = window.prompt("Add a key theme");
    if (!theme?.trim()) return;
    change(plan => {
      const trimmed = theme.trim().slice(0, 60);
      if (!plan.key_themes.includes(trimmed)) plan.key_themes.push(trimmed);
    });
  };

  document.querySelectorAll("[data-remove-theme]").forEach(pill => {
    pill.onclick = () => change(plan => {
      plan.key_themes = plan.key_themes.filter(t => t !== pill.dataset.removeTheme);
    });
  });

  // --- preferences ---
  document.querySelectorAll("[data-option]").forEach(control => {
    if (control.disabled) return;
    control.onchange = () => persistPreference(stage, control.dataset.option, control.value);
  });
}

function wireApproachPicker(change, rerender) {
  const keepNotes = () => {
    const notes = select("#approach-notes");
    if (notes) planViewState.approachNotes = notes.value;
  };
  document.querySelectorAll("[data-approach]").forEach(button => {
    button.onclick = () => {
      keepNotes();
      planViewState.approachKey = button.dataset.approach;
      rerender();
    };
  });
  document.querySelectorAll("[data-approach-option]").forEach(button => {
    button.onclick = () => {
      keepNotes();
      const key = button.dataset.approachOption;
      planViewState.approachOptions = { ...(planViewState.approachOptions ?? {}),
        [key]: button.dataset.value };
      // A choice about the plan as it is, not about a draft, is saved at once.
      if (button.dataset.saves === "now") {
        change(plan => {
          plan.approach_options = { ...(plan.approach_options ?? {}), [key]: button.dataset.value };
        });
      } else {
        rerender();
      }
    };
  });
  select("#approach-notes")?.addEventListener("input", keepNotes);

  const build = select("#build-outline-button");
  if (!build) return;
  build.onclick = async () => {
    keepNotes();
    const plan = applicationState.plan;
    const { approach, options, notes } = chosenApproach(plan);
    const body = plan.sections.filter(section => !isFrame(section));
    if (approach.key === "follow-deck" && body.length && !window.confirm(
        "Follow the deck? This replaces the outline with one section per slide. Narration "
        + "written for sections that go is kept, unattached.")) return;
    if (approach.uses_ai && !window.confirm(`Draft with “${approach.name}”?\n\nThis calls `
        + "the model: one call for the outline, then one per section. It makes a draft "
        + "beside your plan; nothing changes until you accept it.")) return;

    if (approach.uses_ai) {
      planViewState.isDrafting = true;
      await rerender();
    }
    try {
      const built = await requestJsonFromApi(projectApiPath("/plan/build"), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ approach: approach.key, options, notes }),
      });
      planViewState.approachKey = planViewState.approachOptions = planViewState.approachNotes = null;
      planViewState.isDrafting = false;
      await refreshProjectSummary();
      await rerender();
      showStageNotice("ok", built.made === "draft" ? "Draft ready. Review it beside your plan."
        : built.made === "plan" ? "The outline follows the deck, inside the lesson frame."
          : "Add sections with “Add new section”.");
    } catch (failure) {
      console.error("building the outline failed", failure);
      planViewState.isDrafting = false;
      await rerender();
      showStageNotice("bad", failure.message);
    }
  };
}

function wireLessonControls(stage, change, rerender) {
  document.querySelectorAll("[data-frame-part]").forEach(button => {
    button.onclick = () => {
      const on = new Set(applicationState.plan.lesson_frame ?? []);
      const part = button.dataset.framePart;
      if (on.has(part)) on.delete(part); else on.add(part);
      runPlanAction({ path: "/plan/lesson-frame", body: { parts: [...on] }, rerender,
        done: on.has(part) ? `${ROLE_NAMES[part]} added.` : `${ROLE_NAMES[part]} switched off.` });
    };
  });

  const writeButton = select("#write-summaries-button");
  if (writeButton) {
    writeButton.onclick = () => {
      const everything = writeButton.dataset.everything === "true";
      const summaries = applicationState.plan.lesson?.summaries ?? {};
      const count = everything ? summaries.teaching_sections : summaries.needing;
      if (!window.confirm(`Ask the model for ${count} one-line summar${count === 1 ? "y" : "ies"}?`
          + "\n\nOne AI call. Nothing in the plan changes until you use them.")) return;
      runPlanAction({ path: "/plan/summaries", body: { everything }, rerender,
        pending: "Writing summaries…", done: "Summaries proposed. Use or dismiss each one." });
    };
  }
  const acceptAll = select("#accept-summaries-button");
  if (acceptAll) acceptAll.onclick = () => runPlanAction({
    path: "/plan/summaries/accept", body: {}, rerender, done: "Summaries are in the plan." });
  const dismissAll = select("#dismiss-summaries-button");
  if (dismissAll) dismissAll.onclick = () => runPlanAction({
    path: "/plan/summaries/dismiss", body: {}, rerender, done: "Proposals dismissed." });
  document.querySelectorAll("[data-accept-summary]").forEach(button => {
    button.onclick = () => runPlanAction({ path: "/plan/summaries/accept",
      body: { section_ids: [button.dataset.acceptSummary] }, rerender });
  });
  document.querySelectorAll("[data-dismiss-summary]").forEach(button => {
    button.onclick = () => runPlanAction({ path: "/plan/summaries/dismiss",
      body: { section_ids: [button.dataset.dismissSummary] }, rerender });
  });

  const link = (plan, sectionId, objectiveId) => {
    const section = plan.sections.find(s => s.id === sectionId);
    if (section && !section.objective_ids.includes(objectiveId)) section.objective_ids.push(objectiveId);
  };
  document.querySelectorAll("[data-link-section]").forEach(chip => {
    chip.onclick = () => change(plan =>
      link(plan, chip.dataset.linkSection, chip.dataset.linkObjective));
  });
  const linkAll = select("#link-objectives-button");
  if (linkAll) linkAll.onclick = () => {
    const suggestions = applicationState.plan.lesson?.objective_suggestions ?? [];
    change(plan => suggestions.forEach(s => link(plan, s.section_id, s.objective_id)));
  };

  document.querySelectorAll("[data-unpin]").forEach(button => {
    button.onclick = event => {
      event.stopPropagation();
      change(plan => {
        const section = plan.sections.find(s => s.id === button.dataset.unpin);
        if (section) section.pinned = false;
      });
    };
  });
}

/** Redraw only the footer, for a tab change. */
let lastHandoff = null;

function rerenderFooter(stage, tab) {
  const footer = select(".stage-content > .footer-nav");
  if (!footer || !lastHandoff) return;
  footer.outerHTML = renderFooterNav(stage, lastHandoff, tab);
  wireGotoButtons(currentNavigate);
  document.querySelectorAll(".footer-nav [data-plan-tab]").forEach(button => {
    button.onclick = () => select(`.plan-tabs [data-plan-tab="${button.dataset.planTab}"]`)?.click();
  });
}

let currentNavigate = () => {};
let currentAgentRenderer = () => {};

/** Swap a label for an input in place, commit on blur or Enter. Avoids a modal
 *  for what is a one-field edit. */
function promptInline(textNode, commit) {
  const input = document.createElement("input");
  input.className = "text-input";
  input.value = textNode.textContent.trim() === "(empty)" ? "" : textNode.textContent.trim();
  input.maxLength = 200;
  textNode.replaceWith(input);
  input.focus();
  input.select();

  let hasCommitted = false;
  const finish = shouldCommit => {
    if (hasCommitted) return;      // blur fires after Enter; commit once
    hasCommitted = true;
    if (shouldCommit) commit(input.value.trim());
    else input.replaceWith(textNode);
  };

  input.addEventListener("keydown", event => {
    if (event.key === "Enter") finish(true);
    if (event.key === "Escape") finish(false);
  });
  input.addEventListener("blur", () => finish(true));
}

function wireOutlineDragAndDrop(change) {
  const rows = document.querySelectorAll(".outline-row[draggable]");

  rows.forEach(row => {
    row.addEventListener("dragstart", event => {
      planViewState.draggingSectionId = row.dataset.section;
      row.classList.add("dragging");
      event.dataTransfer.effectAllowed = "move";
      // Firefox refuses to start a drag unless data is set.
      event.dataTransfer.setData("text/plain", row.dataset.section);
    });

    row.addEventListener("dragend", () => {
      planViewState.draggingSectionId = null;
      document.querySelectorAll(".outline-row")
        .forEach(other => other.classList.remove("dragging", "drop-target"));
    });

    row.addEventListener("dragover", event => {
      event.preventDefault();
      if (row.dataset.section !== planViewState.draggingSectionId) {
        row.classList.add("drop-target");
      }
    });

    row.addEventListener("dragleave", () => row.classList.remove("drop-target"));

    row.addEventListener("drop", event => {
      event.preventDefault();
      const draggedId = planViewState.draggingSectionId;
      const targetId = row.dataset.section;
      if (!draggedId || draggedId === targetId) return;
      // The frame stays at the edges; the server would put it back anyway.
      if (!row.hasAttribute("draggable")) return;

      change(plan => {
        const fromIndex = plan.sections.findIndex(s => s.id === draggedId);
        const toIndex = plan.sections.findIndex(s => s.id === targetId);
        if (fromIndex < 0 || toIndex < 0) return;
        const [moved] = plan.sections.splice(fromIndex, 1);
        plan.sections.splice(toIndex, 0, moved);
      });
    });
  });
}

async function persistPreference(stage, optionKey, newValue) {
  // A control that silently does nothing reads as broken. Say why instead
  // of dropping the interaction.
  if (applicationState.isSavingSettings) {
    showStageNotice("warn", "Still saving the last change — try again in a moment.");
    return;
  }
  applicationState.isSavingSettings = true;

  const settings = applicationState.stageSettings[stage.key];
  const previousValue = settings.values[optionKey];
  settings.values[optionKey] = newValue;

  try {
    applicationState.stageSettings[stage.key] = await requestJsonFromApi(
      projectApiPath(`/settings/${stage.key}`),
      {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ values: settings.values }),
      });
    if (optionKey === "target_duration") {
      await requestJsonFromApi(projectApiPath("/plan/reshape"), { method: "POST" });
      await renderScenePlanStage(stage, currentNavigate, currentAgentRenderer);
      showStageNotice("ok", "The time is shared out again for the new target.");
    }
    const savedHint = select("#settings-saved-hint");
    if (savedHint) {
      savedHint.textContent = "saved";
      setTimeout(() => { if (savedHint.isConnected) savedHint.textContent = ""; }, 1600);
    }
  } catch (saveFailure) {
    console.error("preference save failed", saveFailure);
    settings.values[optionKey] = previousValue;
    showStageNotice("bad", `Could not save that preference — ${saveFailure.message}`);
  } finally {
    applicationState.isSavingSettings = false;
  }
}
