/**
 * The storyboard (`storyboard.py`): a card per scene — its picture, its first words,
 * what will be drawn and labelled — painted, noted and approved before any scene is
 * animated. The first section's approval opens Making; it sets the style.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import { escapeHtml, projectApiPath, showStageNotice } from "/static/ui-kit.js";

const BRIEF_NAMES = { draw: "Drawn", labels: "Labels", picture: "Slide picture",
  illustrate: "Painted" };

function renderCard(card) {
  const picture = card.picture
    ? `<img src="${escapeHtml(projectApiPath(`/${card.picture}`))}" alt="" loading="lazy">`
    : `<div class="sb-no-picture">No picture yet</div>`;
  return `
    <article class="sb-card" data-sb-card="${escapeHtml(card.visual_id)}">
      <div class="sb-picture">${picture}
        <span class="sb-number">${card.number}</span>
        ${card.picture_kind === "painted" ? `<span class="sb-kind">painted</span>`
          : card.picture_kind === "slide" ? `<span class="sb-kind">slide</span>` : ""}
      </div>
      <p class="sb-says">“${escapeHtml(card.says)}…”</p>
      <dl class="sb-brief">${Object.entries(card.brief).filter(([key]) => key !== "illustrate")
        .map(([key, value]) => `<dt>${BRIEF_NAMES[key] ?? key}</dt><dd>${escapeHtml(value)}</dd>`)
        .join("")}</dl>
      <textarea rows="2" data-sb-note placeholder="A note for this scene — e.g. show the leg larger"
        >${escapeHtml(card.note)}</textarea>
      ${card.picture_kind === "painted" ? `<button type="button" class="btn sb-repaint"
          data-sb-repaint>Paint again with the note <span class="fact warn">AI · 1 image</span>
          </button>` : ""}
    </article>`;
}

// Sections opened or closed by hand stay so through the page's own redraws.
const sectionOpen = {};

/** A section is a row: its title, scenes and approval; opened, its cards. One that
 *  still needs approving opens by default, so what is asked is never hidden. */
function renderSection(section) {
  const status = section.approved ? `<span class="plan-check pass">Approved</span>`
    : section.required ? `<span class="plan-check warn">Required before making scenes</span>`
      : `<span class="plan-check n/a">Optional</span>`;
  const open = sectionOpen[section.id] ?? (section.required && !section.approved);
  return `
    <details class="panel sb-section" data-sb-section="${escapeHtml(section.id)}" ${open ? "open" : ""}>
      <summary class="sb-row">
        <h3>${escapeHtml(section.title)}</h3>
        <span class="muted">${section.cards.length} scene(s)${section.prepared ? "" : " · not prepared"}</span>
        <span class="spacer"></span>${status}
      </summary>
      ${section.prepared ? `<div class="sb-grid">${section.cards.map(renderCard).join("")}</div>`
        : `<p class="panel-sub">${section.cards.length} scene(s). Preparing paints each scene's
            picture in the project's style and lays out what it will show.</p>`}
      <div class="vs-actions">
        <button type="button" class="btn ${section.prepared ? "" : "btn-accent"}" data-sb-prepare>
          ${section.prepared ? "Prepare again" : "Prepare storyboard"}
          <span class="fact warn">AI · up to ${section.cards.length} image(s)</span></button>
        ${section.prepared ? `<button type="button" class="btn ${section.approved ? "" : "btn-accent"}"
            data-sb-approve="${section.approved ? "0" : "1"}">
            ${section.approved ? "Withdraw approval" : "Approve this storyboard"}</button>` : ""}
      </div>
    </details>`;
}

/** The Storyboard tab, drawn into `container` and redrawn after every action. */
export async function mountStoryboard(container) {
  if (!container) return;
  let board;
  const call = async (path, body, busy, done) => {
    if (busy) {
      busy.disabled = true;
      busy.textContent = "Working…";
    }
    try {
      board = await requestJsonFromApi(projectApiPath(`/storyboard${path}`), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (done) showStageNotice("ok", done);
    } catch (failure) {
      showStageNotice("bad", failure.message);
    }
    draw();
  };
  const draw = () => {
    container.innerHTML = `
      <p class="panel-sub sb-intro">A card per scene: its picture, what it says, what will be
        drawn. Leave a note on any card — it is the scene's instruction when it is made. The
        first section's storyboard must be approved before scenes are made: it sets the style
        every scene follows.</p>
      ${board.sections.map(renderSection).join("")}`;
    container.querySelectorAll("[data-sb-section]").forEach(element => {
      const sectionId = element.dataset.sbSection;
      element.addEventListener("toggle", () => { sectionOpen[sectionId] = element.open; });
      const prepare = element.querySelector("[data-sb-prepare]");
      prepare.onclick = () => call("/prepare", { section_id: sectionId }, prepare,
        "Storyboard prepared. Look at every card, leave notes, then approve.");
      const approve = element.querySelector("[data-sb-approve]");
      if (approve) approve.onclick = () => call("/approve",
        { section_id: sectionId, approved: approve.dataset.sbApprove === "1" }, approve,
        approve.dataset.sbApprove === "1" ? "Approved." : "Approval withdrawn.");
    });
    container.querySelectorAll("[data-sb-card]").forEach(card => {
      const visualId = card.dataset.sbCard;
      const note = card.querySelector("[data-sb-note]");
      note.onchange = () => call("/note", { visual_id: visualId, note: note.value }, null,
        "Note saved.");
      const repaint = card.querySelector("[data-sb-repaint]");
      if (repaint) repaint.onclick = () => call("/repaint", { visual_id: visualId }, repaint,
        "Painted again.");
    });
  };
  try {
    board = await requestJsonFromApi(projectApiPath("/storyboard"));
  } catch (failure) {
    container.innerHTML = `<p class="muted">The storyboard could not be loaded — ${
      escapeHtml(failure.message)}</p>`;
    return;
  }
  draw();
}

/** On the Make tab: why scenes cannot be made yet, while they cannot. */
export async function mountStoryboardGate(container, openStoryboard) {
  if (!container) return;
  try {
    const board = await requestJsonFromApi(projectApiPath("/storyboard"));
    if (!board.gate) return;
    container.innerHTML = `<div class="card sb-gate"><b>Storyboard first.</b>
      ${escapeHtml(board.gate)} <button type="button" class="btn btn-accent" data-sb-open>
      Open the storyboard</button></div>`;
    container.querySelector("[data-sb-open]").onclick = openStoryboard;
  } catch (failure) {
    console.warn("storyboard gate could not be read", failure);
  }
}
