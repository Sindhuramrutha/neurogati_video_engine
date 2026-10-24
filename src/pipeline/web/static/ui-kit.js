/**
 * Shared UI state and primitives.
 *
 * Both the shell and each stage view import from here, so neither imports the
 * other and there is no cycle. Adding a stage view means adding one module that
 * imports this — not editing the shell.
 */

import {
  escapeHtml, hideNoticeIn, requestJsonFromApi, showNoticeIn,
} from "/static/shared-client.js";

export { escapeHtml };
export const select = selector => document.querySelector(selector);

/**
 * Everything the UI renders from.
 *
 * Deliberately one object rather than scattered module-level variables, so
 * "what can change, and who changes it" has a single answer. Stage views read
 * it freely and write only the fields they own.
 */
export const applicationState = {
  stageDefinitions: [],
  availableProjects: [],
  selectedProject: null,
  activeStageKey: "inputs",

  // Inputs
  isUploadInFlight: false,
  isDeleteInFlight: false,

  // Extraction workbench. Which file is previewed is a view concern and lives
  // here; which files are *extracted* is saved with the project on the server.
  previewFileName: null,
  extractingFileName: null,    // the one file being extracted, while it runs
  extractionSelection: [],     // the files ticked for the next extraction
  extractionTab: "extract",    // extract | review | final
  compareSplit: 32,            // % of the width the Preview column takes
  comparePaneHeight: null,     // px; null keeps the default height
  previewSlideIndex: null,     // the slide on screen in the Extraction preview
  finalFileName: null,
  stageSettings: {},           // stage key -> { values, options }
  isSavingSettings: false,

  // Planning. The plan is the stage's output, not a setting, so it is held
  // separately and written back whole.
  plan: null,

  // Which project the documents above were loaded for. Compared before every
  // save so a stale document cannot be written to a different project.
  documentsLoadedForSlug: null,

  // Scripting. Narration keyed by plan section id, plus
  // variables; the server returns it already audited against the plan.
  script: null,

  // Studio. Multi-track timeline in integer milliseconds.
  composition: null,

  // Reviewing. Comments, chapters and version history for the cut.
  review: null,

  // A preference, not project data: it says how you like to work.
};

/* ---- icons -------------------------------------------------------------- */

const ICON_PATHS = {
  inputs: `<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>`,
  extraction: `<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M9 13h6M9 17h4"/>`,
  assets: `<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.8"/><path d="m4 17 5-5 4 4 3-3 4 4"/>`,
  "scene-plan": `<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M8 2v4M16 2v4M3 10h18"/>`,
  "script-staging": `<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>`,
  generation: `<path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="3.5"/>`,
  studio: `<rect x="2" y="5" width="14" height="14" rx="2"/><path d="m22 8-6 4 6 4V8z"/>`,
  render: `<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m10 9 5 3-5 3V9z"/>`,
  export: `<path d="M12 3v12M8 11l4 4 4-4"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/>`,
  reviewing: `<path d="M9 11l3 3 8-8"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>`,
};

export const stageIcon = (stageKey, size = 17) =>
  `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
     ${ICON_PATHS[stageKey] ?? ICON_PATHS.inputs}</svg>`;

export const icon = (paths, size = 14, strokeWidth = 2) =>
  `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round">${paths}</svg>`;

export const ICON = {
  plus: `<path d="M12 5v14M5 12h14"/>`,
  arrowLeft: `<path d="M19 12H5M12 19l-7-7 7-7"/>`,
  arrowRight: `<path d="M5 12h14M12 5l7 7-7 7"/>`,
  check: `<path d="M4 12l5 5L20 6"/>`,
  alert: `<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/>`,
  gear: `<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9v.09"/>`,
  doc: `<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>`,
};

/* ---- formatting --------------------------------------------------------- */

export function formatFileSize(sizeInBytes) {
  if (sizeInBytes < 1024) return `${sizeInBytes} B`;
  if (sizeInBytes < 1024 * 1024) return `${Math.round(sizeInBytes / 1024)} KB`;
  return `${(sizeInBytes / (1024 * 1024)).toFixed(1)} MB`;
}

/** What each file type wears: a colour, a label, and a glyph for the sheet.
 *
 *  The glyph is what makes the icon readable at a glance before the letters
 *  are: a pie chart is a deck, ruled lines are a document, a play triangle is
 *  video. Paths are drawn in a 24x24 box and placed on the sheet.
 */
const FILE_TYPES = {
  pdf:  { colour: "#FF5C5C", label: "PDF",
          glyph: `<path d="M5 4h9l5 5v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1z"/>
                  <path d="M8 13h8M8 17h5"/>` },
  doc:  { colour: "#4D96FF", label: "DOC",  glyph: `<path d="M5 6h14M5 11h14M5 16h9"/>` },
  docx: { colour: "#4D96FF", label: "DOCX", glyph: `<path d="M5 6h14M5 11h14M5 16h9"/>` },
  ppt:  { colour: "#FF8A5B", label: "PPT",
          glyph: `<circle cx="12" cy="12" r="8"/><path d="M12 4v8h8"/>` },
  pptx: { colour: "#FF8A5B", label: "PPTX",
          glyph: `<circle cx="12" cy="12" r="8"/><path d="M12 4v8h8"/>` },
  md:   { colour: "#B197FC", label: "MD",
          glyph: `<path d="M4 17V7l5 6 5-6v10"/><path d="M18 7v7m0 0 2.5-3M18 14l-2.5-3"/>` },
  txt:  { colour: "#FFD93D", label: "TXT", glyph: `<path d="M5 7h14M5 12h14M5 17h7"/>` },
  mp4:  { colour: "#38D89B", label: "MP4", glyph: `<path d="M9 6l10 6-10 6V6z"/>` },
  mov:  { colour: "#38D89B", label: "MOV", glyph: `<path d="M9 6l10 6-10 6V6z"/>` },
  mp3:  { colour: "#4ECDC4", label: "MP3",
          glyph: `<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>` },
  wav:  { colour: "#4ECDC4", label: "WAV",
          glyph: `<path d="M4 12h3l3-7 4 14 3-7h3"/>` },
  png:  { colour: "#A3E635", label: "PNG",
          glyph: `<rect x="4" y="5" width="16" height="14" rx="2"/><circle cx="9" cy="10" r="1.6"/><path d="m5 17 5-5 4 4 3-3 2 2"/>` },
  jpg:  { colour: "#A3E635", label: "JPG",
          glyph: `<rect x="4" y="5" width="16" height="14" rx="2"/><circle cx="9" cy="10" r="1.6"/><path d="m5 17 5-5 4 4 3-3 2 2"/>` },
};

const UNKNOWN_FILE_TYPE = {
  colour: "#C9C2BA", label: "FILE",
  glyph: `<path d="M12 7v6M12 17h.01"/>`,
};

/** A file icon: two stacked sheets, a coloured band across the foot, a glyph
 *  above it and the extension lettered on it.
 *
 *  Drawn rather than fetched. A 40px glyph is not worth a network dependency
 *  that breaks the app offline, and the instantly recognisable ones (Word,
 *  Acrobat) are trademarked artwork we should not ship. The stacked sheet and
 *  folded band are what make it read as a file; the colour and glyph say which.
 */
export function fileTypeBadge(suffix) {
  const extension = (suffix || "").replace(".", "").toLowerCase();
  const type = FILE_TYPES[extension] ?? UNKNOWN_FILE_TYPE;
  const label = extension ? extension.toUpperCase().slice(0, 4) : type.label;
  const letterSize = label.length >= 4 ? 7.6 : label.length === 3 ? 8.8 : 10;

  return `<span class="file-badge" title="${escapeHtml(label)} file">
    <svg viewBox="0 0 44 52" width="34" height="40" aria-hidden="true"
         stroke="#14110F" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round">
      <!-- the sheet behind, so a file reads as a stack of pages -->
      <rect x="13" y="3" width="28" height="40" rx="5" fill="#E7EBF2"/>
      <!-- the sheet in front -->
      <rect x="3" y="9" width="28" height="40" rx="5" fill="#F8F9FC"/>
      <!-- the glyph, drawn in a 24x24 box and set into the white area -->
      <g transform="translate(9 13) scale(0.55)" fill="none" stroke="#14110F"
         stroke-width="3.4">${type.glyph}</g>
      <!-- the colour band across the foot, carrying the letters -->
      <path d="M3 33h28v11a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5z" fill="${type.colour}"/>
      <text x="17" y="45" text-anchor="middle" fill="#14110F" stroke="none"
            font-family="system-ui, sans-serif" font-size="${letterSize}"
            font-weight="800" letter-spacing=".2">${escapeHtml(label)}</text>
    </svg>
  </span>`;
}

/* ---- derived reads ------------------------------------------------------ */

export function stageStateFor(stageKey) {
  if (!applicationState.selectedProject) return { status: "empty", detail: "" };
  return applicationState.selectedProject.stages.find(s => s.stage === stageKey)
    ?? { status: "empty", detail: "" };
}

/** How long a notice stays, by tone, before it goes by itself. A long message
 *  gets longer, so the rejected-file list in a warning can still be read. */
const NOTICE_MILLISECONDS = { ok: 4000, warn: 8000, bad: 12000 };
let stageNoticeTimer = null;

/** A toast over the page, not a bar in it, so it never pushes the stage down.
 *  It floats, leaves on its own, and a click sends it away sooner. */
export function showStageNotice(tone, message) {
  const host = select("#stage-notice");
  showNoticeIn(host, tone, message);
  if (!host) return;

  host.onclick = () => hideNoticeIn(host);
  clearTimeout(stageNoticeTimer);
  const lasts = Math.max(NOTICE_MILLISECONDS[tone] ?? 6000, message.length * 60);
  stageNoticeTimer = setTimeout(() => hideNoticeIn(host), lasts);
}

export const projectApiPath = suffix =>
  `/api/projects/${applicationState.selectedProject.slug}${suffix}`;

/**
 * Re-read the selected project's summary: its stage statuses and their details.
 *
 * The chrome renders from `selectedProject.stages`, loaded when the project was
 * opened. Without this, every stage chip stated the project as it was on
 * arrival -- "1 of 4 sections written" after drafting the other three -- until
 * the page was reloaded.
 *
 * The shell registers what to redraw, so stage views say what changed and stay
 * out of the chrome.
 */
let redrawChrome = null;

export function onProjectSummaryRefreshed(callback) {
  redrawChrome = callback;
}

export async function refreshProjectSummary() {
  const slugAtRequestTime = applicationState.selectedProject?.slug;
  if (!slugAtRequestTime) return;

  let summary;
  try {
    summary = await requestJsonFromApi(`/api/projects/${slugAtRequestTime}`);
  } catch (refreshFailure) {
    // The stage's own work succeeded; a stale chip is not worth an error.
    console.warn("could not refresh the project summary", refreshFailure);
    return;
  }
  if (applicationState.selectedProject?.slug !== slugAtRequestTime) return;

  applicationState.selectedProject = summary;
  const listed = applicationState.availableProjects
    .findIndex(project => project.slug === slugAtRequestTime);
  if (listed !== -1) applicationState.availableProjects[listed] = summary;
  redrawChrome?.();
  await refreshUpstream();
}

/* ---- when an earlier layer changed -----------------------------------------
 *
 * Every transfer records what it was built from. When an earlier layer is
 * transferred again, each layer after it is flagged: red in the sidebar, and a
 * banner under its header that names what is new, changed or gone and offers to
 * redo the layer for the new input. `stageHeader` draws the banner, so it is on
 * every layer without each page knowing about it.
 */
const UPSTREAM_REDO = {
  assets: "Gather again",
  "scene-plan": "Tell the planner what changed",
  "script-staging": "Go to the sections to redraft",
  generation: "Set up the scenes again",
  render: "Render again",
};

let upstreamActionHandler = null;
/** The shell says what Redo and Transfer as it stands do; this file cannot navigate. */
export function onUpstreamAction(handler) { upstreamActionHandler = handler; }

export async function refreshUpstream() {
  const slug = applicationState.selectedProject?.slug;
  if (!slug) return;
  try {
    const state = await requestJsonFromApi(`/api/projects/${slug}/upstream`);
    if (applicationState.selectedProject?.slug !== slug) return;
    applicationState.upstream = state;
  } catch (failure) {
    console.warn("could not read what changed upstream", failure);
    return;
  }
  paintUpstreamFlags();
}

function upstreamBanner(stageKey) {
  const flag = applicationState.upstream?.[stageKey];
  if (!flag?.flagged) return "";
  const parts = (change, kind, word) => change.counts[kind] ? `
    <span class="upstream-parts"><b>${change.counts[kind]} ${word}:</b>
      ${change[kind].map(escapeHtml).join(" · ")}${
        change.counts[kind] > change[kind].length ? " …" : ""}</span>` : "";
  const direct = flag.changes.map(change => `
    <p><b>${escapeHtml(change.name)} was transferred again</b> (${escapeHtml(whenItWas(change.at))}).
      This layer was built from the transfer before it.</p>
    ${parts(change, "changed", "changed")}${parts(change, "added", "new")}${
      parts(change, "removed", "removed")}`).join("");
  const behind = flag.behind.length ? `
    <p><b>${flag.behind.map(escapeHtml).join(" and ")}</b>
      ${flag.behind.length === 1 ? "is" : "are"} out of date, so this layer is too.
      Bring ${flag.behind.length === 1 ? "it" : "them"} up to date first.</p>` : "";
  return `
    <div class="upstream-flag" role="alert">
      <span class="upstream-flag-mark">${icon(ICON.alert, 18, 2.4)} Out of date</span>
      <div class="upstream-flag-text">${direct}${behind}</div>
      ${flag.changes.length ? `
        <div class="upstream-flag-actions">
          <button class="btn btn-accent" data-upstream-redo="${stageKey}">${UPSTREAM_REDO[stageKey]}</button>
          ${stageKey === "render" ? "" : `<button class="btn" data-upstream-keep="${stageKey}"
            title="This layer still holds: hand it on again as it is">Transfer as it stands</button>`}
        </div>` : ""}
    </div>`;
}

/** Fill every banner on the page, and mark the flagged layers in the sidebar. */
export function paintUpstreamFlags() {
  document.querySelectorAll("[data-upstream-for]").forEach(host => {
    host.innerHTML = upstreamBanner(host.dataset.upstreamFor);
  });
  document.querySelectorAll(".nav-item[data-stage]").forEach(item => {
    const flagged = Boolean(applicationState.upstream?.[item.dataset.stage]?.flagged);
    item.classList.toggle("flagged", flagged);
    item.title = flagged ? "Out of date: an earlier layer was transferred again" : "";
  });
}

document.addEventListener("click", event => {
  const redo = event.target.closest?.("[data-upstream-redo]");
  const keep = event.target.closest?.("[data-upstream-keep]");
  if (redo) upstreamActionHandler?.(redo.dataset.upstreamRedo, "redo");
  if (keep) upstreamActionHandler?.(keep.dataset.upstreamKeep, "keep");
});

/**
 * Every field in `applicationState` scoped to one project.
 *
 * Listed once, here, so a new per-project document cannot be added to the state
 * object and then forgotten when the project changes.
 */
/**
 * Which tab each layer is on, kept per project in this browser so a refresh
 * comes back to the same tab. Each page checks the value against its own tabs
 * and falls back to its first, so a tab that no longer exists is harmless.
 */
const REMEMBERED_TABS = {
  assetsTab: "extracted",      // extracted | brand | look | final
  planTab: "direction",        // direction | plan | final
  scriptTab: "setup",          // setup | write | final (check & transfer)
  generationTab: "setup",      // setup | make | final
  extractionTab: "extract",
  reviewTab: "transcript",     // Reviewing: transcript | comments
  scriptEditorTab: "script",   // Script & Staging's writing pane: script | preview
};
const tabsStorageKey = () => `pipeline.tabs.${applicationState.selectedProject?.slug ?? ""}`;
const readRememberedTabs = () => {
  try { return JSON.parse(localStorage.getItem(tabsStorageKey()) ?? "{}") ?? {}; } catch { return {}; }
};
const chosenTabs = {};   // this page load's choices; null until one is made
for (const [key, fallback] of Object.entries(REMEMBERED_TABS)) {
  Object.defineProperty(applicationState, key, {
    enumerable: true,
    get: () => chosenTabs[key] ?? readRememberedTabs()[key] ?? fallback,
    set: value => {
      chosenTabs[key] = value;
      if (value === null || !applicationState.selectedProject) return;
      try {
        localStorage.setItem(tabsStorageKey(), JSON.stringify({ ...readRememberedTabs(), [key]: value }));
      } catch { /* private mode: the tab is kept for this page load only */ }
    },
  });
}

const PROJECT_SCOPED_STATE_DEFAULTS = {
  previewFileName: null,
  // null: back to what this browser remembers for the project (REMEMBERED_TABS).
  assetsTab: null,
  planTab: null,
  scriptTab: null,
  generationTab: null,
  reviewTab: null,
  scriptEditorTab: null,
  // A rendered video Studio is showing instead of its timeline: { slug, file }.
  studioWatch: null,
  extractionTab: null,
  extractionSelection: [],
  finalFileName: null,
  stageSettings: {},
  plan: null,
  script: null,

  // Assets & Design, Generation and Export, all per project.
  assetLibrary: null,
  sceneVisuals: null,
  exportManifest: null,
  composition: null,
  review: null,

  // For each layer: what changed before it since it was handed on (`upstream.py`).
  upstream: null,

  // The Orchestrator's thread is about one project's work, so it must not
  // follow you into another project.
  agentConversationId: null,
  agentConversations: [],

  // What the last extraction review found, for the panel on that page.
  extractionReview: null,
};

/**
 * Discard everything belonging to the previously selected project.
 *
 * Not cosmetic. Before this existed, switching project left `plan`, `script`,
 * `composition` and `review` holding the *previous* project's documents while
 * `projectApiPath` already resolved to the new one — so a save issued before the
 * new document loaded wrote project A's plan into project B. Stale-looking data
 * was the visible symptom; cross-project corruption was the real one.
 *
 * Must be called on every path that changes `selectedProject`.
 */
export function clearProjectScopedState() {
  Object.assign(applicationState, structuredClone(PROJECT_SCOPED_STATE_DEFAULTS));
}

/* ---- what each stage is for, behind an (i) beside its title ---------------
 *
 * The one-line description under every title said too little to help and took
 * a line on every page. It lives here instead, longer, and appears on hover or
 * keyboard focus. Written per stage so the header code stays one call.
 */
const STAGE_INFO = {
  inputs: {
    summary: "The one source file this video is made from.",
    points: [
      "One file per project: a PowerPoint deck, PDF, Word, Markdown or plain-text file. It runs through every layer.",
      "It is kept exactly as uploaded; open Preview to look at it.",
      "Replace it to use another file: the work after Extraction is kept and marked out of date until it is redone.",
      "Next, Extraction reads it.",
    ],
  },
  extraction: {
    summary: "Pull the text and figures out of the source.",
    points: [
      "Extract: read the source, with the options beside it. Extracting again replaces the result.",
      "Review: each slide beside what was extracted from it. The agent reviews every "
        + "slide and proposes fixes, and you can ask it for more changes, or new pictures.",
      "Final & transfer: see everything extracted, then transfer it to the next layer.",
      "Nothing reaches later stages until it is transferred.",
    ],
  },
  assets: {
    summary: "The inventory and the look: what exists, your brand assets, and how the video's frames look.",
    points: [
      "Extracted assets: every picture, in a box per file, with the slide it came from. Leave out what you "
        + "don't want. Nothing is judged here; the Scene Plan attaches pictures to sections.",
      "Brand assets: watermark, logo, intro and outro. Drag to place; set size, opacity, corners, shadow, "
        + "when it appears, trims and cross-fades. The preview is the image the render lays on.",
      "Look: a theme, three colours, fonts and the deck's background art, with a live preview and a "
        + "readability check.",
      "Final & transfer: the video as it will look, and everything handed on, stated. It goes to the "
        + "Scene Plan, which carries it to every later layer. No AI on this layer.",
    ],
  },
  "scene-plan": {
    summary: "Agree the video's shape with the planning agent: its length, sections and scenes.",
    points: [
      "Direction: say what the video should be, with the length in your own words and how strictly "
        + "the slides' order is kept. The agent (AI) proposes the shape; you agree, or reply with "
        + "what to change. Only then are the scenes written.",
      "Plan: what was agreed -- sections, each a run of slides, and their scenes -- editable by "
        + "hand, with each section's pictures.",
      "Final & transfer: lists anything that blocks the transfer -- a broken strict slide order, a "
        + "section with no scenes, Assets & Design not transferred. Later stages read only the "
        + "transferred plan, with its scenes and the pictures, brand kit and look it carries.",
    ],
  },
  "script-staging": {
    summary: "Write each planned section as scenes.",
    points: [
      "Setup: the sections the Scene Plan handed on, variables, and leftover narration.",
      "Write: each section as scenes — what is said and what is shown. The agent (AI) only drafts what you ask.",
      "Check & transfer: fixed rules -- an unwritten section or an undefined {{VARIABLE}} "
        + "blocks the transfer; once transferred, later stages read only the transferred script.",
    ],
  },
  generation: {
    summary: "Make what each scene shows.",
    points: [
      "Setup: what came in, what this machine can draw, and the rules that decide each shot.",
      "Decide: what every scene shows and how it moves — fixed rules, no model; change any by hand.",
      "Make: produce it; says first which scenes call a model (on-screen words, drawn pictures, scene scripts).",
      "A scripted scene is drawn by its own Python script, in its own folder; fixed checks decide whether its clip is used.",
      "Check, then Final & transfer: the render reads the transferred shots, frozen.",
    ],
  },
  studio: {
    summary: "Compose and render the video.",
    points: [
      "Arrange media on the timeline, in layers.",
      "Pick the voice that reads the narration.",
      "Render video adds the project to the Render queue, where it is made.",
    ],
  },
  render: {
    summary: "Make the videos: a queue of renders, one at a time.",
    points: [
      "Choose the voice, then add the project to the queue.",
      "Renders run one after another on the server; reloading the page stops nothing.",
      "Pause keeps everything made so far — resume carries on from there.",
      "Delete stops a render and removes what it made; finished videos are never deleted.",
    ],
  },
  reviewing: {
    summary: "Watch the video and decide whether it ships.",
    points: [
      "Play it back and leave comments at the moment they are about.",
      "Check the chapters.",
      "Anything that needs changing goes back to the stage that made it.",
    ],
  },
  export: {
    summary: "Take the finished video away as files.",
    points: [
      "The video itself, its transcript, its chapters and a description.",
      "Each is a file you can download and publish.",
    ],
  },
};

/** An (i) beside a stage title that explains the stage on hover or focus.
 *  `summaryOverride` replaces the summary, for pages that describe themselves
 *  (an agent states its own role). */
function stageInfoButton(stageKey, summaryOverride = "") {
  const info = STAGE_INFO[stageKey] ?? { summary: "", points: [] };
  const summary = summaryOverride || info.summary;
  const id = `stage-info-${stageKey}`;
  return `
    <span class="stage-info">
      <button class="stage-info-button" type="button" aria-describedby="${id}"
              aria-label="About this stage">i</button>
      <span class="stage-info-pop" role="tooltip" id="${id}">
        <b>${escapeHtml(summary)}</b>
        ${info.points.length ? `<ul>${info.points.map(point =>
          `<li>${escapeHtml(point)}</li>`).join("")}</ul>` : ""}
      </span>
    </span>`;
}

/* ---- moving on: "Move to next layer", confirmed first ---------------------
 *
 * Every stage ends in the same button, and moving on is a deliberate step: a
 * dialog says where you are going and what goes with you, and nothing happens
 * until you confirm. The pages still save as you work -- this confirms the
 * move, it does not save anything.
 */

/** The footer button that moves to the next stage after a confirmation.
 *  `carries` is one sentence on what goes on with you; `warning` is shown in
 *  the dialog when something is not ready (it does not block the move). */
export function moveToNextLayerButton(nextStage, {
  disabled = false, disabledReason = "", carries = "", warning = "",
} = {}) {
  if (!nextStage) return "";
  return `
    <button class="btn btn-accent btn-move-next" data-goto="${escapeHtml(nextStage.key)}"
            data-move-next="${escapeHtml(nextStage.title)}"
            data-move-carries="${escapeHtml(carries)}"
            data-move-warning="${escapeHtml(warning)}"
            ${disabled ? "disabled" : ""}
            title="${escapeHtml(disabled ? disabledReason : `Move on to ${nextStage.title}`)}">
      Move to next layer ${icon(ICON.arrowRight)}
    </button>`;
}

/** A brutalist confirmation dialog. Resolves true on confirm, false otherwise. */
function confirmMoveToNextLayer({ nextTitle, carries = "", warning = "" }) {
  return new Promise(resolve => {
    const dialog = document.createElement("dialog");
    dialog.className = "move-dialog";
    dialog.setAttribute("aria-labelledby", "move-dialog-title");
    dialog.innerHTML = `
      <form method="dialog">
        <h3 id="move-dialog-title">Move to the next layer?</h3>
        <p class="move-dialog-where">Next: <b>${escapeHtml(nextTitle)}</b></p>
        ${carries ? `<p>${escapeHtml(carries)}</p>` : ""}
        ${warning ? `<p class="move-dialog-warning">${icon(ICON.alert, 16, 2.2)}
                     <span>${escapeHtml(warning)}</span></p>` : ""}
        <div class="move-dialog-actions">
          <button class="btn" value="cancel">Stay here</button>
          <button class="btn btn-accent" value="confirm" autofocus>
            Move to ${escapeHtml(nextTitle)} ${icon(ICON.arrowRight)}
          </button>
        </div>
      </form>`;
    document.body.append(dialog);
    dialog.addEventListener("close", () => {
      resolve(dialog.returnValue === "confirm");
      dialog.remove();
    });
    // A click on the backdrop is a "stay here".
    dialog.addEventListener("click", event => {
      if (event.target === dialog) dialog.close("cancel");
    });
    dialog.showModal();
  });
}

/** Wire every [data-goto] on the page: a "Move to next layer" button asks
 *  first, any other goto (Back, Go to ...) moves straight away. */
export function wireGotoButtons(navigateToStage) {
  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = async () => {
      if (button.dataset.moveNext) {
        const confirmed = await confirmMoveToNextLayer({
          nextTitle: button.dataset.moveNext,
          carries: button.dataset.moveCarries,
          warning: button.dataset.moveWarning,
        });
        if (!confirmed) return;
      }
      navigateToStage(button.dataset.goto);
    };
  });
}

/* ---- the page frame every stage shares ------------------------------------ */

/** The stage before and after this one, either possibly undefined. */
export function stageNeighbours(stage) {
  const { stageDefinitions } = applicationState;
  const index = stageDefinitions.findIndex(s => s.key === stage.key);
  return { previous: stageDefinitions[index - 1], next: stageDefinitions[index + 1] };
}

/** The purple header box: icon, title, the (i) and, on the right, whatever the
 *  page adds -- then the gear that opens its agent, when it has one. */
export function stageHeader(stageKey, title, {
  actions = "", agentButtonId = "", infoSummary = "",
} = {}) {
  return `
    <div class="card-head stage-head">
      <span class="card-icon">${stageIcon(stageKey, 21)}</span>
      <div class="stage-title">
        <h2>${escapeHtml(title)}</h2>
        ${stageInfoButton(stageKey, infoSummary)}
      </div>
      ${actions}
      ${agentButtonId ? `
        <button class="btn btn-square card-corner" id="${agentButtonId}"
                title="Agent &amp; instructions" aria-label="Agent and instructions">
          ${icon(ICON.gear, 18, 1.8)}
        </button>` : ""}
    </div>
    <div class="stage-progress" aria-live="polite" ${progressState ? "" : "hidden"}>
      ${progressMarkup()}</div>
    <div data-upstream-for="${stageKey}">${upstreamBanner(stageKey)}</div>`;
}

/* ---- the progress bar under the stage header --------------------------------
 *
 * For long work the page itself steps through -- extracting several files, the
 * agent reviewing slide after slide -- in the strip under the purple header,
 * where the eye already is. It says what is under way, how far it has got and
 * for how long. Renders run on the server and have their own panel along the
 * bottom (`render-dock.js`). Kept outside the page, so it survives a redraw;
 * `stageHeader` draws it.
 */

let progressState = null;  // { label, done, total, startedAt }
let progressClock = null;

function progressMarkup() {
  if (!progressState) return "";
  const { label, done, total, startedAt } = progressState;
  const known = total > 0;
  const shown = Math.min(done, total);
  const percent = known ? Math.round((100 * shown) / total) : 0;
  const seconds = Math.max(0, Math.round((Date.now() - startedAt) / 1000));
  const elapsed = `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
  return `
    <div class="stage-progress-text">
      <b>${escapeHtml(label)}</b>
      <span>${known ? `${shown} / ${total} · ${percent}% · ` : ""}${elapsed}</span>
    </div>
    <div class="stage-progress-track ${known ? "" : "unknown"}" role="progressbar"
         aria-label="${escapeHtml(label)}" aria-valuemin="0" aria-valuemax="100"
         ${known ? `aria-valuenow="${percent}"` : ""}>
      <div class="stage-progress-fill" style="width:${known ? percent : 100}%"></div>
    </div>`;
}

function paintProgress() {
  const bar = document.querySelector(".stage-progress");
  if (!bar) return;
  bar.hidden = !progressState;
  bar.innerHTML = progressMarkup();
}

/** Show or move the bar. `total` 0 means the steps are not known yet: the bar
 *  runs striped instead of filling. */
export function showProgress({ label, done = 0, total = 0 }) {
  progressState = { label, done, total, startedAt: progressState?.startedAt ?? Date.now() };
  paintProgress();
  progressClock ??= setInterval(paintProgress, 1000);
}

export function hideProgress() {
  progressState = null;
  clearInterval(progressClock);
  progressClock = null;
  paintProgress();
}

/** The footer: Back, anything the page puts in the middle, and the confirmed
 *  "Move to next layer" (see `moveToNextLayerButton` for `next`'s options).
 *  `end` takes the forward button's place, for a page that should not have one. */
export function footerNav(stage, { middle = "", next = {}, end = null } = {}) {
  const { previous, next: nextStage } = stageNeighbours(stage);
  return `
    <div class="footer-nav">
      ${previous ? `
        <button class="btn" data-goto="${previous.key}">
          ${icon(ICON.arrowLeft)} Back to ${escapeHtml(previous.title)}
        </button>` : ""}
      ${middle}
      <div class="spacer"></div>
      ${end ?? moveToNextLayerButton(nextStage, next)}
    </div>`;
}

/** "14:05" today, "3 Sep, 14:05" otherwise; the raw text if it is not a date. */
export function whenItWas(isoTimestamp) {
  if (!isoTimestamp) return "";
  const when = new Date(isoTimestamp);
  if (Number.isNaN(when.getTime())) return isoTimestamp.slice(0, 16).replace("T", " ");
  const today = new Date().toDateString() === when.toDateString();
  return when.toLocaleString(undefined, today
    ? { hour: "2-digit", minute: "2-digit" }
    : { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
}
