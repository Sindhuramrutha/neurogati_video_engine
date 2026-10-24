/**
 * Facts — on Script & Staging, and a badge on every page while any is open.
 *
 * Every claim the deck makes is checked by two models (`fact_ledger.py`). Where a
 * slide is wrong, or the checkers disagree, a person decides: keep it as the slide
 * says, or as the fact is. Until then the video states neither, and it stays here,
 * highlighted, until it is decided.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import { escapeHtml, projectApiPath, select, showStageNotice } from "/static/ui-kit.js";

export async function loadFacts() {
  return requestJsonFromApi(projectApiPath("/facts"))
    .catch(() => ({ claims: [], open: 0, counts: {}, built_at: "" }));
}

export function renderFactsPanel(facts) {
  const needing = facts.claims.filter(c => c.status === "disputed" || c.status === "uncertain");
  const decided = needing.filter(c => c.decision);
  return `
    <details class="card" id="facts-panel" style="margin-bottom:12px;${facts.open
      ? "border:3px solid #e8603c" : ""}" ${facts.open ? "open" : ""}>
      <summary><b>Facts</b> —
        ${facts.built_at ? `${facts.counts.verified ?? 0} verified,
          ${facts.counts.disputed ?? 0} the slides may have wrong,
          ${facts.counts.uncertain ?? 0} uncertain
          ${facts.open ? `· <b style="color:#c4401f">${facts.open} to decide</b>` : ""}`
          : "not checked yet"}</summary>
      <p class="muted" style="margin:6px 0 10px">Every claim the slides make is checked by
        two models. Where a slide may be wrong, choose what the video says; until you do,
        it states neither, keeping the point general.</p>
      ${facts.built_at ? "" : `<button class="btn btn-accent" id="build-facts-button">
        Check the slides' facts</button>`}
      ${needing.map(claim => `
        <div class="fact-row" data-fact="${escapeHtml(claim.id)}" style="display:grid;
             grid-template-columns:minmax(0,1fr) auto;gap:14px;align-items:start;
             padding:10px 0;border-top:1px dashed #ccc;white-space:normal">
          <div style="overflow-wrap:anywhere">
            <span class="plan-check ${claim.status === "disputed" ? "fail" : "warn"}">
              ${claim.status === "disputed" ? "Slide may be wrong" : "Uncertain"}</span>
            <b>Slide ${claim.slide}:</b> ${escapeHtml(claim.says)}
            <div class="muted" style="margin-top:4px">${claim.correct
              ? `The checkers: ${escapeHtml(claim.correct)}` : escapeHtml(claim.why)}</div>
          </div>
          <div style="display:flex;flex-direction:column;gap:6px;min-width:170px">
            <button class="btn ${claim.decision === "slide" ? "btn-accent" : ""}"
                    data-decide="slide">Keep it as in the slide</button>
            <button class="btn ${claim.decision === "fact" ? "btn-accent" : ""}"
                    data-decide="fact">${claim.status === "disputed" ? "Use the fact"
                      : "Keep it general"}</button>
            ${claim.decision ? `<button class="btn" data-decide="">Undecide</button>` : ""}
          </div>
        </div>`).join("")}
      ${decided.length ? `<div style="margin-top:10px">
        <button class="btn btn-accent" id="apply-facts-button">
          Write the sections these decisions touch again</button></div>` : ""}
    </details>`;
}

export function wireFactsPanel(refresh) {
  const send = async (call, label) => {
    try {
      await call();
      await refresh();
      paintFactsBadge();
    } catch (failure) {
      showStageNotice("bad", `${label} — ${failure.message}`);
    }
  };
  select("#build-facts-button")?.addEventListener("click", event => {
    event.target.disabled = true;
    event.target.textContent = "Checking every claim with two models…";
    send(() => requestJsonFromApi(projectApiPath("/facts/build"), { method: "POST" }),
      "Could not check the facts");
  });
  select("#apply-facts-button")?.addEventListener("click", event => {
    event.target.disabled = true;
    event.target.textContent = "Writing those sections again…";
    send(() => requestJsonFromApi(projectApiPath("/facts/apply"), { method: "POST" }),
      "Could not write them again");
  });
  document.querySelectorAll("[data-fact] [data-decide]").forEach(button => {
    button.onclick = () => send(() => requestJsonFromApi(
      projectApiPath(`/facts/${encodeURIComponent(button.closest("[data-fact]").dataset.fact)}`),
      { method: "PUT", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ decision: button.dataset.decide }) }), "Could not decide");
  });
}

/** A red badge on every page while any fact waits for a decision. A page draws its
 *  header when it likes and draws it again after an action, so the badge is put
 *  back whenever a header appears without it, from the count last fetched. */
let openFacts = 0;

export async function paintFactsBadge() {
  openFacts = (await loadFacts()).open ?? 0;
  placeFactsBadge();
}

function placeFactsBadge() {
  const head = document.querySelector(".stage-head");
  if (!head) return;
  const badge = head.querySelector(".facts-badge");
  if (!openFacts) {
    badge?.remove();
    return;
  }
  const text = `${openFacts} fact decision(s) open`;
  if (badge) {
    if (badge.textContent !== text) badge.textContent = text;
    return;
  }
  const made = document.createElement("span");
  made.className = "facts-badge";
  made.style.cssText = "background:#e8603c;color:#fff;border-radius:999px;padding:4px 12px;"
    + "font-weight:700;margin-left:auto;margin-right:10px;cursor:pointer;white-space:nowrap";
  made.textContent = text;
  made.title = "Decide them on Script & Staging, under Facts";
  made.onclick = () => document.querySelector('.nav-item[data-stage="script-staging"]')?.click();
  head.insertBefore(made, head.querySelector(".card-corner"));
}

new MutationObserver(placeFactsBadge).observe(document.body, { childList: true, subtree: true });
