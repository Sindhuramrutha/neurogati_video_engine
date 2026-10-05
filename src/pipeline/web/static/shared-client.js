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
/** The same contract as `requestJsonFromApi`, for responses that are not JSON.
 *
 *  Binary needs its own door: a deck is fetched as bytes so the browser can
 *  render the raw `.pptx`, and forcing that through the JSON helper would mean
 *  either parsing bytes as JSON or letting callers reach for `fetch` directly --
 *  and the moment one caller does, nobody checks status codes again.
 */
export async function requestBytesFromApi(path, requestOptions) {
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
    throw new ApiRequestFailed(
      `${response.status} ${response.statusText}`, { statusCode: response.status });
  }

  return response.arrayBuffer();
}

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
 * `requestJsonFromApi` for a POST whose body takes a while to send.
 *
 * fetch reports no upload progress, so a 300 MB deck sat behind a dimmed
 * dropzone for minutes with no sign it was moving. XMLHttpRequest does; the
 * contract is otherwise identical -- parsed JSON, or an ApiRequestFailed.
 * `onProgress` receives a fraction from 0 to 1.
 */
export function uploadJsonToApi(path, body, onProgress) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest();
    request.open("POST", path);

    request.upload.onprogress = event => {
      if (event.lengthComputable) onProgress?.(event.loaded / event.total);
    };
    request.onerror = () => reject(new ApiRequestFailed(
      navigator.onLine === false
        ? "You appear to be offline."
        : "Could not reach the server. Is it still running?",
      { isNetworkFailure: true },
    ));
    request.onload = () => {
      let parsed = null;
      try {
        parsed = request.responseText ? JSON.parse(request.responseText) : null;
      } catch {
        // Handled below: an error status reports its own text, a 2xx is a server bug.
      }
      if (request.status < 200 || request.status >= 300) {
        reject(new ApiRequestFailed(
          parsed?.detail || `${request.status} ${request.statusText}`,
          { statusCode: request.status },
        ));
      } else if (parsed === null && request.status !== 204) {
        reject(new ApiRequestFailed("The server returned a malformed response."));
      } else {
        resolve(parsed);
      }
    };

    request.send(body);
  });
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

/** The small slice of markdown a model actually writes back, as safe HTML.
 *
 *  Model answers arrive as markdown — `**bold**`, `##` headings, `-` lists —
 *  and showing them raw put literal asterisks and hashes in front of the user
 *  on every reply. A full markdown library is 40 KB to render five constructs,
 *  and every one of them would still need escaping.
 *
 *  **Escaping happens first, on the whole string, before any tag is added.**
 *  That ordering is the safety property: by the time this inserts `<b>`, there
 *  is no `<` left in the text that could have come from the model, so a reply
 *  quoting HTML is displayed rather than run.
 */
export function renderModelMarkdown(text) {
  const inline = (fragment) => fragment
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/(^|[\s(])\*([^*\n]+?)\*(?=[\s).,;:!?]|$)/g, "$1<i>$2</i>")
    .replace(/`([^`\n]+?)`/g, "<code>$1</code>");

  const blocks = [];
  let listItems = [];

  const closeList = () => {
    if (!listItems.length) return;
    blocks.push(`<ul>${listItems.map(item => `<li>${item}</li>`).join("")}</ul>`);
    listItems = [];
  };

  for (const rawLine of escapeHtml(text).split("\n")) {
    const line = rawLine.trim();

    if (!line) { closeList(); continue; }

    const heading = line.match(/^(#{1,6})\s+(.*)$/);
    if (heading) {
      closeList();
      // Levels are flattened to one weight: these sit inside a chat bubble, and
      // an <h2> styled like a page title would shout over the answer.
      blocks.push(`<p class="answer-heading">${inline(heading[2])}</p>`);
      continue;
    }

    if (/^[-*+]\s+/.test(line)) { listItems.push(inline(line.slice(2))); continue; }
    if (/^\d+[.)]\s+/.test(line)) {
      listItems.push(inline(line.replace(/^\d+[.)]\s+/, "")));
      continue;
    }
    if (/^-{3,}$/.test(line)) { closeList(); blocks.push("<hr>"); continue; }

    closeList();
    blocks.push(`<p>${inline(line)}</p>`);
  }
  closeList();

  return blocks.join("");
}
