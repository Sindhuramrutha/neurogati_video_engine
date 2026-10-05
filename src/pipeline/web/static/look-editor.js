/**
 * The Look tab: how the video's own frames are coloured and set.
 *
 * Built for choosing, not for reading a palette file: a preview that is always
 * in view, ready-made themes to start from, three colours with plain names and
 * a real colour picker, a line saying how well the text reads, font dropdowns
 * with a sample, and the deck's background art shown as it would really be
 * drawn. Its controls are deliberately quieter than the rest of the app.
 *
 * Every control changes the render (`project_look.py`): none is decoration, and
 * the preview's colours come from the renderer's own style.
 */

import { ICON, escapeHtml, icon, projectApiPath } from "/static/ui-kit.js";

const COLOUR_ABOUT = {
  background: "Behind everything on the frame.",
  panels: "The box that text and pictures sit on.",
  accent: "The bar above a heading, and highlights.",
};
const PALETTE_NAMES = { dk1: "Dark 1", lt1: "Light 1", dk2: "Dark 2", lt2: "Light 2",
                        hlink: "Link", folHlink: "Visited link" };
const paletteName = key => PALETTE_NAMES[key] ?? key.replace(/^accent(\d)$/, "Accent $1");
const WASHES = [
  ["as_written", "As PowerPoint shows it", "The deck's pale sheet stays over its art."],
  ["inverted", "Art at full strength", "The sheet is read as see-through. Dark text may sit on dark art."],
  ["ignored", "No sheet", "The sheet is left off; only the art is drawn."],
];
const artUrl = path => projectApiPath(`/extraction/assets/${encodeURIComponent(path.split("/").pop())}`);
const swatchesOf = colours => Object.entries(colours ?? {})
  .filter(([, value]) => String(value).startsWith("#"));

/** A small frame drawn in four colours: the unit every theme card and the preview share. */
const miniFrame = ({ background, panel, accent, text }) => `
  <span class="lp-mini" style="background:${background}">
    <span class="lp-mini-panel" style="background:${panel}">
      <i style="background:${accent}"></i><b style="color:${text}">Aa</b>
    </span>
  </span>`;

function renderPreview(page, chosen) {
  const preview = page.look_preview;
  const reads = preview.readability;
  return `
    <aside class="lp-preview">
      <h4>Preview</h4>
      <div class="look-frame" style="background:${preview.background}">
        ${preview.art ? `<img class="look-frame-art" alt="" src="${artUrl(preview.art)}">` : ""}
        <div class="look-frame-panel" style="background:${preview.panel}">
          <span class="look-frame-bar" style="background:${preview.accent}"></span>
          <b style="color:${preview.text};font-family:'${escapeHtml(preview.heading_font || "inherit")}'">
            How we feel the world</b>
          <span style="color:${preview.dim};font-family:'${escapeHtml(preview.body_font || "inherit")}'">
            Touch, sight and sound reach the brain as signals.</span>
        </div>
      </div>
      <p class="lp-caption">${chosen ? "The source's own styling."
        : "The renderer's own look."} The frame as the render draws it.</p>
      <div class="lp-reads ${reads.text_is_readable ? "good" : "poor"}">
        ${icon(reads.text_is_readable ? ICON.check : ICON.alert, 15, 2.4)}
        <span><b>Text on its panel: ${reads.text_on_panel} : 1.</b>
          ${reads.text_is_readable ? "Easy to read."
            : `Hard to read. It needs at least ${reads.needed} : 1. Pick a panel colour further from the text.`}
          <small>The text is ${preview.text === "#1a1816" ? "dark" : "light"} because the
            background is ${preview.text === "#1a1816" ? "light" : "dark"}; the render picks it.</small>
        </span>
      </div>
      ${reads.accent_is_visible ? "" : `<div class="lp-reads poor">${icon(ICON.alert, 15, 2.4)}
        <span><b>The accent is nearly the background's colour</b>, so its bar will not show.</span></div>`}
    </aside>`;
}

function renderColour(role, page) {
  const look = page.look;
  const choice = look.choices?.[role.key] ?? "";
  const colour = page.look_preview.chosen[role.key];
  const custom = choice.startsWith("#");
  const from = !choice ? "The deck's own" : custom ? "Your colour" : paletteName(choice);
  return `
    <details class="lp-colour" data-role="${role.key}">
      <summary>
        <span class="lp-well" style="background:${colour}"></span>
        <span class="lp-colour-name"><b>${escapeHtml(role.name)}</b>
          <small>${escapeHtml(COLOUR_ABOUT[role.key])}</small></span>
        <span class="lp-colour-value">${escapeHtml(from)}<code>${escapeHtml(colour.toUpperCase())}</code></span>
        <span class="lp-chevron">${icon(`<path d="m6 9 6 6 6-6"/>`, 15, 2.2)}</span>
      </summary>
      <div class="lp-colour-body">
        <div>
          <h5>From this deck</h5>
          <div class="lp-swatches">
            ${swatchesOf(look.colours).map(([key, value]) => `
              <button class="lp-swatch ${choice === key ? "on" : ""}" data-look-role="${role.key}"
                      data-value="${escapeHtml(key)}" style="background:${escapeHtml(value)}"
                      title="${escapeHtml(paletteName(key))} · ${escapeHtml(value)}"
                      aria-label="${escapeHtml(paletteName(key))} ${escapeHtml(value)}"></button>`).join("")}
          </div>
        </div>
        <div>
          <h5>Any colour</h5>
          <div class="lp-custom">
            <input type="color" value="${colour}" data-look-colour="${role.key}" aria-label="Pick a colour">
            <input type="text" value="${colour.toUpperCase()}" maxlength="7" spellcheck="false"
                   data-look-hex="${role.key}" aria-label="Hex colour">
          </div>
        </div>
        <button class="lp-reset" data-look-role="${role.key}" data-value="" ${choice ? "" : "disabled"}>
          Reset to the deck's own</button>
      </div>
    </details>`;
}

function renderFont(role, page) {
  const look = page.look;
  const choice = look.choices?.[role.key] ?? "";
  const own = role.key === "heading_font" ? "heading" : "body";
  const other = own === "heading" ? "body" : "heading";
  const names = { heading: look.heading_font, body: look.body_font };
  const options = [
    ["", `${names[own] || "The renderer's font"} (the deck's ${own} font)`],
    ...(names[other] && names[other] !== names[own]
      ? [[other, `${names[other]} (the deck's ${other} font)`]] : []),
    ["renderer", "The renderer's font"],
  ];
  const drawn = page.look_preview[role.key];
  return `
    <label class="lp-font">
      <span><b>${escapeHtml(role.name)}</b></span>
      <select data-look-font="${role.key}">
        ${options.map(([value, label]) => `
          <option value="${value}" ${(choice === own ? "" : choice) === value ? "selected" : ""}>
            ${escapeHtml(label)}</option>`).join("")}
      </select>
      <span class="lp-sample" style="font-family:'${escapeHtml(drawn || "inherit")}'">
        ${role.key === "heading_font" ? "How we feel the world" : "Touch, sight and sound reach the brain as signals."}
      </span>
    </label>`;
}

export function renderLook(page) {
  const look = page.look;
  const { sources, colour_roles: colourRoles, font_roles: fontRoles } = page.look_options;
  const following = look.use_source_styling ? look.from_file : "";
  const chosen = sources.find(source => source.from_file === following);
  const themes = page.look_preview.themes ?? [];

  const source = (key, name, detail, colours) => `
    <button class="lp-source ${following === key ? "on" : ""}" data-look-source="${escapeHtml(key)}">
      <span class="lp-radio"></span>
      <span class="lp-source-text"><b>${escapeHtml(name)}</b><small>${escapeHtml(detail)}</small></span>
      ${colours ? `<span class="lp-strip">${swatchesOf(colours).slice(0, 8).map(([, value]) =>
        `<i style="background:${escapeHtml(value)}"></i>`).join("")}</span>` : ""}
    </button>`;

  return `
    <div class="look-pro">
      <div class="lp-main">
        <section class="lp-section">
          <h4>Start from</h4>
          <p>How the video's own frames look. Slides of the deck are always shown as their
            author made them, whatever is chosen here.</p>
          ${sources.slice(0, 1).map(item => source(item.from_file, "The source's own styling",
            [item.theme_name, item.heading_font, item.aspect_ratio].filter(Boolean).join(" · "),
            item.colours)).join("")}
          ${source("", "The renderer's own look", "Dark and neutral, the same for every video.")}
          ${sources.length ? "" : `<p class="lp-note">The source has no styling to follow: it
            is not a deck, or <b>Extract styling</b> was off. Switch it on on Extraction, extract
            and transfer again.</p>`}
        </section>

        ${chosen ? `
          <section class="lp-section">
            <h4>Theme</h4>
            <p>A starting point, made from this deck's own colours. Change any colour below.</p>
            <div class="lp-themes">
              ${themes.map(theme => `
                <button class="lp-theme ${theme.is_current ? "on" : ""}" data-look-theme="${theme.key}">
                  ${miniFrame(theme)}
                  <b>${escapeHtml(theme.name)}</b><small>${escapeHtml(theme.about)}</small>
                </button>`).join("")}
              ${themes.some(theme => theme.is_current) ? "" : `
                <span class="lp-theme on custom">${miniFrame(page.look_preview)}
                  <b>Your own</b><small>The colours you set below.</small></span>`}
            </div>
          </section>

          <section class="lp-section">
            <h4>Colours</h4>
            <p>Click a colour to change it.</p>
            ${colourRoles.map(role => renderColour(role, page)).join("")}
          </section>

          <section class="lp-section">
            <h4>Fonts</h4>
            ${fontRoles.map(role => renderFont(role, page)).join("")}
            <p class="lp-note">A font the computer rendering the video does not have is
              replaced by the nearest one it has.</p>
          </section>

          ${look.background_asset_path ? `
            <section class="lp-section">
              <h4>Background art</h4>
              <label class="lp-switch">
                <input type="checkbox" data-look-art ${look.background_art ? "checked" : ""}>
                <span class="lp-switch-track"></span>
                <span><b>Draw the deck's background art</b> behind the video's own frames</span>
              </label>
              <p>Many decks lay a near-opaque sheet over their art, and the file does not say
                how it is meant to look. This is the deck's first slide, drawn each way. It
                applies wherever a slide of the deck is shown.</p>
              <div class="lp-washes">
                ${WASHES.map(([key, name, about]) => `
                  <button class="lp-wash ${look.slide_wash === key ? "on" : ""}" data-wash="${key}">
                    <img alt="" loading="lazy" src="${projectApiPath(`/assets/wash-preview/${key}`)}">
                    <b>${name}</b><small>${about}</small>
                  </button>`).join("")}
              </div>
            </section>` : ""}`
          : `<p class="lp-note">Pick a file above to use its colours and fonts, and to adjust them.</p>`}
      </div>
      ${renderPreview(page, chosen)}
    </div>`;
}

/** `act(button, path, body)` is the page's one way of saving and redrawing. */
export function wireLookEditor(act) {
  const choose = (element, body) => act(element, "/assets/look-choice", body);

  document.querySelectorAll("[data-look-source]").forEach(button => {
    button.onclick = () => choose(button, { from_file: button.dataset.lookSource });
  });
  document.querySelectorAll("button[data-look-theme]").forEach(button => {
    button.onclick = () => choose(button, { theme: button.dataset.lookTheme });
  });
  document.querySelectorAll("[data-look-role]").forEach(button => {
    button.onclick = () => choose(button, { role: button.dataset.lookRole, value: button.dataset.value });
  });
  document.querySelectorAll("[data-look-colour]").forEach(input => {
    input.onchange = () => choose(input, { role: input.dataset.lookColour, value: input.value });
  });
  document.querySelectorAll("[data-look-hex]").forEach(input => {
    input.onchange = () => {
      const value = input.value.trim().startsWith("#") ? input.value.trim() : `#${input.value.trim()}`;
      if (!/^#[0-9a-fA-F]{6}$/.test(value)) {
        input.classList.add("invalid");
        input.title = "A colour is # and six of 0-9 or A-F, like #4472C4.";
        return;
      }
      choose(input, { role: input.dataset.lookHex, value });
    };
  });
  document.querySelectorAll("[data-look-font]").forEach(picker => {
    picker.onchange = () => choose(picker, { role: picker.dataset.lookFont, value: picker.value });
  });
  document.querySelectorAll("[data-look-art]").forEach(box => {
    box.onchange = () => choose(box, { background_art: box.checked });
  });
  // Keep the colour being worked on open across the redraw a change causes.
  document.querySelectorAll("details.lp-colour").forEach(panel => {
    if (panel.dataset.role === openColour) panel.open = true;
    panel.addEventListener("toggle", () => {
      if (panel.open) openColour = panel.dataset.role;
      else if (openColour === panel.dataset.role) openColour = null;
    });
  });
}

let openColour = null;
