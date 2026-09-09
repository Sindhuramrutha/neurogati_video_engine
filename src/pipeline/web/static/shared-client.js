/**
 * Shared browser-side contract for talking to the pipeline API.
 *
 * One definition means HTTP failure behaves identically everywhere, and there is
 * one place to change it. This exists because an earlier page made raw fetch
 * calls and checked none of them: a failed POST advanced the UI exactly as a
 * successful one did, losing the write silently.
 */

/**
 * Escapes the five characters that can break out of element content or a quoted
 * attribute value.
 *
 * The earlier per-page versions escaped only & < >, which was safe by accident:
 * every interpolated value happened to be server-sanitised. Relying on that is a
 * latent injection waiting for the first unsanitised field.
 */
export function escapeHtml(value) {
  return String(value ?? "").replace(
    /[&<>"']/g,
    character => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[character]),
  );
}

/**
 * Thrown for every failed API interaction.
 *
 * `isNetworkFailure` separates "the server could not be reached" from "the server
 * answered with an error". They need different wording, and only the former is
 * worth offering an automatic retry for.
 */
export class ApiRequestFailed extends Error {
  constructor(message, { statusCode = null, isNetworkFailure = false } = {}) {
    super(message);
    this.name = "ApiRequestFailed";
    this.statusCode = statusCode;
    this.isNetworkFailure = isNetworkFailure;
  }
}

/**
 * The only sanctioned way for a page to call the API.
 *
 * Always either returns parsed JSON (or null for 204), or throws
 * ApiRequestFailed. It never returns a partially-successful value, so a caller
 * cannot accidentally treat a failure as data.
 */
export async function requestJsonFromApi(path, requestOptions) {
  let response;
  try {
    response = await fetch(path, requestOptions);
  } catch {
    throw new ApiRequestFailed(
      navigator.onLine === false
        ? "You appear to be offline."
        : "Could not reach the server. Is it still running?",
      { isNetworkFailure: true },
    );
  }

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new ApiRequestFailed(
      errorBody.detail || `${response.status} ${response.statusText}`,
      { statusCode: response.status },
    );
  }

  if (response.status === 204) return null;

  try {
    return await response.json();
  } catch {
    // A 2xx carrying malformed JSON is a server bug. Naming it here stops a
    // SyntaxError surfacing later from somewhere unrelated.
    throw new ApiRequestFailed("The server returned a malformed response.");
  }
}

/**
 * Renders a transient message into a host element.
 *
 * Kept here so both pages report success, partial success and failure the same
 * way rather than one using alert() and the other using nothing.
 */
export function showNoticeIn(hostElement, tone, message) {
  if (!hostElement) return;
  hostElement.className = `notice ${tone}`;
  hostElement.textContent = message;
  hostElement.hidden = false;
}

export function hideNoticeIn(hostElement) {
  if (hostElement) hostElement.hidden = true;
}
