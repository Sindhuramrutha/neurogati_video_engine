/**
 * Shared UI state and primitives.
 *
 * Both the shell and each stage view import from here, so neither imports the
 * other and there is no cycle. Adding a stage view means adding one module that
 * imports this — not editing the shell.
 */

import { escapeHtml, showNoticeIn } from "/static/shared-client.js";

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
  sourceSortOrder: "name-asc",
  isUploadInFlight: false,
  isDeleteInFlight: false,

  // Extraction workbench. Selection is per-session rather than persisted:
  // which files you are looking at is a view concern, unlike the saved options.
  selectedSourceNames: null,   // null means "all"; an empty Set means "none"
  previewFileName: null,
  previewTab: "preview",
  stageSettings: {},           // stage key -> { values, options }
  isSavingSettings: false,

  // Planning. The plan is the stage's output, not a setting, so it is held
  // separately and written back whole.
  plan: null,

  // Which project the documents above were loaded for. Compared before every
  // save so a stale document cannot be written to a different project.
  documentsLoadedForSlug: null,

  // Scripting. Narration keyed by plan section id, plus scenarios and
  // variables; the server returns it already audited against the plan.
  script: null,

  // Studio. Multi-track timeline in integer milliseconds.
  composition: null,

  // Reviewing. Comments, chapters and version history for the cut.
  review: null,
};

/* ---- icons -------------------------------------------------------------- */

const ICON_PATHS = {
  inputs: `<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>`,
  extraction: `<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M9 13h6M9 17h4"/>`,
  planning: `<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M8 2v4M16 2v4M3 10h18"/>`,
  scripting: `<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>`,
  studio: `<rect x="2" y="5" width="14" height="14" rx="2"/><path d="m22 8-6 4 6 4V8z"/>`,
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

/** Badge colour per file type, so a source list is scannable by shape as well
 *  as by name. */
export function fileTypeBadge(suffix) {
  const extension = (suffix || "").replace(".", "").toLowerCase();
  const colourVariable = ["pdf", "md", "docx", "pptx"].includes(extension)
    ? `var(--${extension})` : "var(--txt)";
  return `<span class="file-badge" style="--badge:${colourVariable}"
    >${escapeHtml(extension.toUpperCase().slice(0, 4) || "?")}</span>`;
}

/* ---- derived reads ------------------------------------------------------ */

export function stageStateFor(stageKey) {
  if (!applicationState.selectedProject) return { status: "empty", detail: "" };
  return applicationState.selectedProject.stages.find(s => s.stage === stageKey)
    ?? { status: "empty", detail: "" };
}

export function sortedSources() {
  const sources = [...(applicationState.selectedProject?.sources ?? [])];
  const comparators = {
    "name-asc": (a, b) => a.name.localeCompare(b.name),
    "name-desc": (a, b) => b.name.localeCompare(a.name),
    "size-desc": (a, b) => b.bytes - a.bytes,
    "type-asc": (a, b) => a.suffix.localeCompare(b.suffix) || a.name.localeCompare(b.name),
  };
  return sources.sort(comparators[applicationState.sourceSortOrder] ?? comparators["name-asc"]);
}

export function showStageNotice(tone, message) {
  showNoticeIn(select("#stage-notice"), tone, message);
}

export const projectApiPath = suffix =>
  `/api/projects/${applicationState.selectedProject.slug}${suffix}`;

/**
 * Every field in `applicationState` scoped to one project.
 *
 * Listed once, here, so a new per-project document cannot be added to the state
 * object and then forgotten when the project changes.
 */
const PROJECT_SCOPED_STATE_DEFAULTS = {
  selectedSourceNames: null,
  previewFileName: null,
  previewTab: "preview",
  stageSettings: {},
  plan: null,
  script: null,
  composition: null,
  review: null,
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

/**
 * True when a per-project document in state belongs to the project currently
 * selected. Stage views call this before persisting, so a save cannot be issued
 * against a document loaded for a different project.
 */
export function isDocumentLoadedForCurrentProject(loadedForSlug) {
  return loadedForSlug === applicationState.selectedProject?.slug;
}
