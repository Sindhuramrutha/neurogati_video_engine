/**
 * API keys panel — set the provider credentials the agents will use.
 *
 * The whole point of this surface is that it handles a secret it never receives.
 * The server sends a mask (`••••••••SioV`) and a status; the input for a stored
 * key starts empty and only travels in one direction. So there is no state here
 * holding a key, nothing to leak through devtools, and nothing cached in the page
 * between opens — reopening the panel re-reads the status from the server.
 *
 * Fields are declared server-side in credentials.py and rendered generically,
 * the same way stage options are: adding a provider changes one Python tuple and
 * nothing in this file.
 */

import { hideNoticeIn, requestJsonFromApi, showNoticeIn } from "/static/shared-client.js";
import { ICON, escapeHtml, icon, select } from "/static/ui-kit.js";

/** Server status for each field, refreshed on every open. Holds masks, never
 *  values — see the module note above. */
let credentialStatus = null;
let isSavingCredentials = false;

const panel = () => select("#credentials-panel");
const noticeHost = () => select("#credentials-notice");

export async function openCredentialsPanel() {
  panel().classList.add("open");
  select("#credentials-body").innerHTML = `<p class="muted" style="margin:0">Loading…</p>`;
  hideNoticeIn(noticeHost());

  try {
    credentialStatus = await requestJsonFromApi("/api/credentials");
  } catch (loadFailure) {
    console.error("credentials load failed", loadFailure);
    select("#credentials-body").innerHTML = `
      <p class="muted" style="margin:0">Could not load credential status.<br>
      ${escapeHtml(loadFailure.message)}</p>`;
    return;
  }

  renderCredentialFields();
}

export function closeCredentialsPanel() {
  panel().classList.remove("open");
  // Drop the status rather than keeping it for the next open: it is server
  // truth with a short shelf life, and a stale "key is set" badge is worse than
  // a moment of loading.
  credentialStatus = null;
}

export const isCredentialsPanelOpen = () => panel().classList.contains("open");

/* ---- rendering ----------------------------------------------------------- */

function renderCredentialFields() {
  const { fields, warnings, environment_file, is_gitignored } = credentialStatus;

  const groups = [...new Set(fields.map(field => field.group))];
  const groupMarkup = groups.map(group => `
    <div class="cred-group">
      <h4>${escapeHtml(group)}</h4>
      ${fields.filter(field => field.group === group).map(renderField).join("")}
    </div>`).join("");

  select("#credentials-body").innerHTML = `
    ${warnings.map(warning => `
      <div class="notice warn" style="margin-bottom:12px">${escapeHtml(warning)}</div>`).join("")}

    ${groupMarkup}

    <div class="cred-footer">
      <p>
        ${icon(ICON.check, 12, 2.4)}
        Stored server-side in <code>${escapeHtml(environment_file)}</code>.
        Keys are never sent to this page — only a mask.
      </p>
      ${is_gitignored
        ? `<p>${icon(ICON.check, 12, 2.4)} That file is gitignored, so it cannot be committed.</p>`
        : `<p class="danger-text">${icon(ICON.alert, 12, 2)}
             <b>That file is not gitignored.</b> Add <code>.env</code> to
             <code>.gitignore</code> before saving a real key.</p>`}
      <p>${icon(ICON.alert, 12, 2)}
         Agents are not wired to a model yet, so nothing uses these keys so far.</p>
    </div>`;

  select("#credentials-save-button").onclick = saveCredentials;
  for (const button of document.querySelectorAll("[data-clear-credential]")) {
    button.onclick = () => clearOneCredential(button.dataset.clearCredential);
  }
}

function renderField(field) {
  const inputId = `credential-${field.name}`;

  // A field set in the real environment cannot be changed from here: pydantic
  // reads it ahead of the file, so accepting an edit would store a value that
  // never takes effect. Better to disable it and say why.
  if (!field.is_editable) {
    return `
      <div class="cred-field">
        <label>${escapeHtml(field.label)}
          <span class="cred-badge env">shell environment</span></label>
        <input value="${escapeHtml(field.display_value)}" disabled>
        <p class="help">Set outside this app, which takes precedence. Unset it in
           your shell to manage it here.</p>
      </div>`;
  }

  const statusBadge = field.is_set
    ? `<span class="cred-badge set">set</span>`
    : `<span class="cred-badge unset">not set</span>`;

  if (field.is_secret) {
    return `
      <div class="cred-field">
        <label for="${inputId}">${escapeHtml(field.label)} ${statusBadge}</label>
        ${field.is_set ? `
          <div class="cred-current">
            <code>${escapeHtml(field.display_value)}</code>
            <button class="btn-icon danger" data-clear-credential="${escapeHtml(field.name)}"
                    title="Remove this key" aria-label="Remove this key">
              ${icon(`<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>`, 14, 1.8)}
            </button>
          </div>` : ""}
        <input id="${inputId}" type="password" autocomplete="off" spellcheck="false"
               data-credential="${escapeHtml(field.name)}" data-secret="true"
               placeholder="${escapeHtml(field.is_set ? "Enter a new key to replace it" : field.placeholder)}">
        <p class="help">${escapeHtml(field.help ?? "")}</p>
      </div>`;
  }

  return `
    <div class="cred-field">
      <label for="${inputId}">${escapeHtml(field.label)}</label>
      <input id="${inputId}" type="text" autocomplete="off" spellcheck="false"
             data-credential="${escapeHtml(field.name)}"
             value="${escapeHtml(field.display_value)}"
             placeholder="${escapeHtml(field.placeholder)}">
      <p class="help">${escapeHtml(field.help ?? "")}</p>
    </div>`;
}

/* ---- saving -------------------------------------------------------------- */

/** Collect only what the user actually supplied.
 *
 *  A blank secret input means "leave it alone", not "clear it" — the input for a
 *  stored key is always empty, so treating blank as a clear would wipe the key
 *  every time someone saved a change to the model name. Clearing is a separate,
 *  explicit button. */
function collectSubmittedValues() {
  const values = {};
  for (const input of document.querySelectorAll("[data-credential]")) {
    const isSecret = input.dataset.secret === "true";
    const value = input.value.trim();
    if (isSecret && !value) continue;
    values[input.dataset.credential] = value;
  }
  return values;
}

async function submitCredentialValues(values, successMessage) {
  if (isSavingCredentials) {
    showNoticeIn(noticeHost(), "warn", "Still saving the last change — try again in a moment.");
    return;
  }
  isSavingCredentials = true;

  const saveButton = select("#credentials-save-button");
  const originalLabel = saveButton.textContent;
  saveButton.disabled = true;
  saveButton.textContent = "Saving…";

  try {
    credentialStatus = await requestJsonFromApi("/api/credentials", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ values }),
    });
    renderCredentialFields();
    showNoticeIn(noticeHost(), "ok", successMessage);
  } catch (saveFailure) {
    console.error("credentials save failed", saveFailure);
    showNoticeIn(noticeHost(), "bad", `Could not save: ${saveFailure.message}`);
  } finally {
    isSavingCredentials = false;
    const button = select("#credentials-save-button");
    if (button) {
      button.disabled = false;
      button.textContent = originalLabel;
    }
  }
}

function saveCredentials() {
  const values = collectSubmittedValues();
  if (Object.keys(values).length === 0) {
    showNoticeIn(noticeHost(), "warn", "Nothing to save — no field was changed.");
    return;
  }
  return submitCredentialValues(values, "Saved. Agents will use these once they are wired to a model.");
}

function clearOneCredential(fieldName) {
  return submitCredentialValues({ [fieldName]: "" }, `Removed ${fieldName}.`);
}
