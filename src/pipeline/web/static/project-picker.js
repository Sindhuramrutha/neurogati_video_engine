/**
 * The project picker: a menu of projects, each with a dustbin on its right.
 *
 * A native <select> cannot hold a button in an option, so this draws the menu
 * itself. The hidden <select id="project-select"> stays the record of which
 * project is chosen -- the rest of the app reads and sets it -- and choosing
 * here sets it and fires its `change`, exactly as picking from it did.
 *
 * Deleting erases the project's folder on the server, for good: there is no
 * trash and no way back, and the page says so before it asks. It always works:
 * whatever is running in the project is stopped first, on the server.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import { escapeHtml, icon, select, showStageNotice } from "/static/ui-kit.js";

const TRASH_ICON = '<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>';

const menu = () => select("#project-menu");
const toggle = () => select("#project-picker-button");

function showMenu(open) {
  menu().hidden = !open;
  toggle().setAttribute("aria-expanded", String(open));
  if (open) paintMenu();
}

function paintMenu() {
  const chooser = select("#project-select");
  const projects = [...chooser.options].filter(option => option.value);
  menu().innerHTML = projects.length ? projects.map(option => `
    <div class="project-row ${option.value === chooser.value ? "on" : ""}" role="option"
         aria-selected="${option.value === chooser.value}">
      <button class="project-row-name" data-pick="${escapeHtml(option.value)}">
        ${escapeHtml(option.textContent)}</button>
      <button class="project-row-trash" data-trash="${escapeHtml(option.value)}"
              title="Delete ${escapeHtml(option.textContent)}"
              aria-label="Delete the project ${escapeHtml(option.textContent)}">
        ${icon(TRASH_ICON, 16, 2)}</button>
    </div>`).join("")
    : `<p class="project-menu-empty">No projects yet.</p>`;
}

/** The button's label follows whatever the hidden select says is chosen. */
export function paintProjectPicker() {
  const chooser = select("#project-select");
  const label = select("#project-picker-name");
  if (!chooser || !label) return;
  label.textContent = chooser.selectedOptions[0]?.textContent || "No projects yet";
  if (!menu().hidden) paintMenu();
}

async function deleteProject(slug, name, onDeleted) {
  if (!window.confirm(`Delete the project “${name}” for good?\n\nIts folder and everything `
      + "in it is erased. There is no trash and no way to get it back.")) return;
  try {
    await requestJsonFromApi(`/api/projects/${encodeURIComponent(slug)}`, { method: "DELETE" });
    showStageNotice("ok", `Deleted “${name}”, for good.`);
    await onDeleted(slug);
  } catch (failure) {
    console.error("deleting the project failed", failure);
    showStageNotice("bad", failure.message);
  }
  paintProjectPicker();
}

/** `onDeleted(slug)` refreshes the project list and redraws the page. */
export function startProjectPicker({ onDeleted }) {
  toggle().onclick = () => showMenu(menu().hidden);
  menu().onclick = event => {
    const pick = event.target.closest("[data-pick]");
    const trash = event.target.closest("[data-trash]");
    if (pick) {
      showMenu(false);
      const chooser = select("#project-select");
      if (chooser.value === pick.dataset.pick) return;
      chooser.value = pick.dataset.pick;
      chooser.dispatchEvent(new Event("change"));
      paintProjectPicker();
    } else if (trash) {
      const name = trash.closest(".project-row").querySelector(".project-row-name").textContent.trim();
      deleteProject(trash.dataset.trash, name, onDeleted);
    }
  };
  document.addEventListener("click", event => {
    if (!menu().hidden && !event.target.closest("#project-picker")) showMenu(false);
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && !menu().hidden) showMenu(false);
  });
}
