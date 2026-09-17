/**
 * Optimistic document editing — one implementation for every stage artifact.
 *
 * Planning, Scripting, Studio and Reviewing each edit a whole document and write
 * it back. All four implemented the same optimistic-with-rollback dance
 * separately, which meant four slightly different failure behaviours waiting to
 * diverge further.
 *
 * The contract:
 *
 * - Apply the change locally first, so the UI never lags the pointer.
 * - Persist. On failure, restore the previous document and say so.
 * - Refuse to persist a document loaded for a *different* project — the stale-state
 *   write that could put one project's plan into another.
 * - Never silently drop a user action: a rejected edit reports why.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import {
  applicationState, projectApiPath, refreshProjectSummary, showStageNotice,
} from "/static/ui-kit.js";

/** Short id for a new list item. One definition; it was previously inlined as
 *  `crypto.randomUUID().replace(...)` in nine places. */
export function newItemIdentifier() {
  return crypto.randomUUID().replace(/-/g, "").slice(0, 12);
}

/**
 * A save already running for this document.
 *
 * Keyed by document kind rather than a shared flag, so saving a plan cannot block
 * an unrelated review edit.
 */
const inFlightSavesByDocumentKind = new Set();

/**
 * Persist an edit to a whole-document artifact.
 *
 * @param {object} options
 * @param {string} options.documentKind      "plan" | "script" | "composition" | "review"
 * @param {string} options.apiPathSuffix     e.g. "/plan"
 * @param {Function} options.applyEdit       mutates the in-memory document
 * @param {Function} options.rerender        re-renders the stage view
 * @param {Function} [options.buildPayload]  narrows what is sent; defaults to the whole document
 * @param {Function} [options.onSaved]       receives the server's response
 * @param {boolean} [options.silent]         skip the optimistic re-render (used while typing,
 *                                           where a re-render would move the caret)
 */
export async function editStageDocument({
  documentKind,
  apiPathSuffix,
  applyEdit,
  rerender,
  buildPayload = document => document,
  onSaved = null,
  silent = false,
}) {
  // A second save of the same document while one is in flight would race, and
  // last-writer-wins would be arbitrary. Say so rather than dropping the click:
  // a button that silently does nothing reads as broken.
  if (inFlightSavesByDocumentKind.has(documentKind)) {
    showStageNotice("warn", "Still saving the last change — try again in a moment.");
    return;
  }

  const projectSlugAtEditTime = applicationState.selectedProject?.slug;
  if (!projectSlugAtEditTime) {
    showStageNotice("bad", "No project selected.");
    return;
  }

  inFlightSavesByDocumentKind.add(documentKind);

  const documentBeforeEdit = structuredClone(applicationState[documentKind]);
  applyEdit(applicationState[documentKind]);

  // The body is fixed *here*, straight after the edit and before any redraw.
  // Every stage's render loads its document from the server, and the payload
  // used to be built after the optimistic redraw -- from a document that redraw
  // had just replaced with the unedited server copy. So every click-edit on
  // Planning, Scripting, Studio and Reviewing was sent back unchanged and
  // silently lost: choosing an audience, a scenario, hiding a track. Only typing
  // survived, because it saves without redrawing.
  const payload = JSON.stringify(buildPayload(structuredClone(applicationState[documentKind])));

  if (!silent) await rerender();

  try {
    const savedDocument = await requestJsonFromApi(projectApiPath(apiPathSuffix), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: payload,
    });

    // The project can be switched while a request is in flight. Applying this
    // response would overwrite the newly selected project's document with the
    // previous one's server state.
    if (applicationState.selectedProject?.slug !== projectSlugAtEditTime) {
      console.warn(
        `discarded a ${documentKind} save response for ${projectSlugAtEditTime}: ` +
        `the selected project changed while it was in flight`);
      return;
    }

    applicationState[documentKind] = onSaved
      ? onSaved(savedDocument, documentBeforeEdit)
      : savedDocument;

    // What the document now says about its stage -- how much is written, whether
    // it is ready -- is shown in the chrome, which would otherwise keep the
    // answer it had when the project was opened. Skipped while typing: that
    // saves every second, and the chip can wait for the next click.
    if (!silent) await refreshProjectSummary();
  } catch (saveFailure) {
    console.error(`${documentKind} save failed`, saveFailure);
    if (applicationState.selectedProject?.slug === projectSlugAtEditTime) {
      applicationState[documentKind] = documentBeforeEdit;
      showStageNotice("bad", `Could not save — ${saveFailure.message}`);
    }
  } finally {
    inFlightSavesByDocumentKind.delete(documentKind);
    if (applicationState.selectedProject?.slug === projectSlugAtEditTime) {
      await rerender();
    }
  }
}

/**
 * Load a stage document, refusing to apply a response that arrived after the
 * project changed.
 *
 * Returns the document, or null when the load failed or is no longer relevant —
 * callers render their own error state, because what a failed load should look
 * like differs per stage.
 */
export async function loadStageDocument(documentKind, apiPathSuffix) {
  const projectSlugAtRequestTime = applicationState.selectedProject?.slug;
  if (!projectSlugAtRequestTime) return null;

  // While a save of this document is in flight, the edited copy in memory is the
  // truth, and the server still holds the old one. Fetching here would redraw
  // the page back to its state before the click until the save came back.
  if (inFlightSavesByDocumentKind.has(documentKind)
      && applicationState[documentKind]
      && applicationState.documentsLoadedForSlug === projectSlugAtRequestTime) {
    return applicationState[documentKind];
  }

  const loadedDocument = await requestJsonFromApi(projectApiPath(apiPathSuffix));

  if (applicationState.selectedProject?.slug !== projectSlugAtRequestTime) {
    console.warn(
      `discarded a ${documentKind} load for ${projectSlugAtRequestTime}: ` +
      `the selected project changed while it was in flight`);
    return null;
  }

  applicationState[documentKind] = loadedDocument;
  applicationState.documentsLoadedForSlug = projectSlugAtRequestTime;
  return loadedDocument;
}
