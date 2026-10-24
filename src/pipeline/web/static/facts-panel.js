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
        <div class="fact" data-fact="${escapeHtml(claim.id)}" style="padding:8px 0;
             border-top:1px dashed #ccc">
          <div><span class="plan-check ${claim.status === "disputed" ? "fail" : "warn"}">
            ${claim.status === "disputed" ? "Slide may be wrong" : "Uncertain"}</span>
            <b>Slide ${claim.slide}:</b> ${escapeHtml(claim.says)}</div>
          ${claim.correct ? `<div class="muted">The checkers: ${escapeHtml(claim.correct)}</div>`
            : `<div class="muted">${escapeHtml(claim.why)}</div>`}
          <div style="display:flex;gap:8px;margin-top:6px;align-items:center">
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

/** A red badge on every page while any fact waits for a decision. */
export async function paintFactsBadge(tries = 0) {
  const head = document.querySelector(".stage-head");
  if (!head) {            // the page draws its header after the sidebar
    if (tries < 5) setTimeout(() => paintFactsBadge(tries + 1), 600);
    return;
  }
  head.querySelector(".facts-badge")?.remove();
  const facts = await loadFacts();
  if (!facts.open) return;
  const badge = document.createElement("span");
  badge.className = "facts-badge";
  badge.style.cssText = "background:#e8603c;color:#fff;border-radius:999px;padding:4px 12px;"
    + "font-weight:700;margin-left:auto;cursor:pointer";
  badge.textContent = `${facts.open} fact decision(s) open`;
  badge.title = "Decide them on Script & Staging, under Facts";
  badge.onclick = () => document.querySelector('.nav-item[data-stage="script-staging"]')?.click();
  head.insertBefore(badge, head.querySelector(".card-corner"));
}
