/**
 * Brand assets: the four slots, and an editor for where and when they appear.
 *
 * - The canvas is a lesson frame in the project's look. The logo and watermark
 *   on it are the very images the render lays on (`brand_overlay.py`), at the
 *   place the render puts them, so what is dragged here is what is rendered.
 * - Everything a person can set has a control and a number beside it: position,
 *   size, opacity, corners, shadow, when it shows, fades; and for the intro and
 *   outro, what is trimmed and how long they cross-fade with the lesson.
 * - Every change saves at once. Nothing reaches a render until the layer is
 *   transferred, as with everything else here.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import { ICON, escapeHtml, icon, projectApiPath, showStageNotice } from "/static/ui-kit.js";

export const brandEditorState = { selected: "logo" };

const OVERLAYS = [["logo", "Logo"], ["watermark", "Watermark"]];
const SAFE_MARGIN = 0.05;
const NOMINAL_LESSON_SECONDS = 60;
const SHOW_LABELS = { whole: "The whole lesson", first: "The first…", last: "The last…",
                      range: "From… to…" };

const brandFileUrl = file => projectApiPath(
  `/assets/brand-files/${encodeURIComponent(file.path.split("/").pop())}`);
const overlayUrl = overlay => projectApiPath(
  `/assets/brand-overlays/${encodeURIComponent(overlay.file)}`);
const asPercent = (share, digits = 0) => `${(share * 100).toFixed(digits)}%`;
const seconds = value => `${Number(value).toFixed(1)} s`;

/* ---- the lesson frame, with the overlays on it ------------------------------------ */

/**
 * A 16:9 lesson frame in the project's look, with the logo and watermark where
 * the render puts them. `editable` makes them draggable and shows the guides.
 */
export function renderFrameCanvas(page, { editable = false } = {}) {
  const preview = page.look_preview;
  const { overlays } = page.brand;
  const art = preview.art ? projectApiPath(`/extraction/assets/${encodeURIComponent(
    preview.art.split("/").pop())}`) : "";
  return `
    <div class="brand-canvas ${editable ? "editable" : ""}" style="background:${preview.background}">
      ${art ? `<img class="look-frame-art" alt="" src="${art}">` : ""}
      <div class="look-frame-panel" style="background:${preview.panel}">
        <span class="look-frame-bar" style="background:${preview.accent}"></span>
        <b style="color:${preview.text};font-family:'${escapeHtml(preview.heading_font || "inherit")}'">
          How we feel the world</b>
        <span style="color:${preview.dim};font-family:'${escapeHtml(preview.body_font || "inherit")}'">
          Touch, sight and sound reach the brain as signals.</span>
      </div>
      ${editable ? `<div class="brand-safe" title="The safe margin: 5% in from every edge"></div>` : ""}
      ${["watermark", "logo"].filter(slot => overlays[slot]).map(slot => `
        <img class="brand-overlay ${editable && brandEditorState.selected === slot ? "selected" : ""}"
             data-overlay="${slot}" alt="${slot}" draggable="false" src="${overlayUrl(overlays[slot])}"
             style="left:${asPercent(overlays[slot].left, 3)};top:${asPercent(overlays[slot].top, 3)};
                    width:${asPercent(overlays[slot].width, 3)}">`).join("")}
    </div>`;
}

/* ---- the slots ----------------------------------------------------------------------- */

function renderSlot(slot, page) {
  const { kit, timing, limits } = page.brand;
  const file = kit[slot.key];
  const isVideo = slot.kind === "video";
  const accept = isVideo ? ".mp4,.mov,.webm,.mkv,.m4v" : ".png,.jpg,.jpeg,.webp";
  const preview = !file ? `<div class="brand-empty">${icon(ICON.doc, 28, 1.4)}</div>`
    : isVideo ? `<video class="brand-preview" controls preload="metadata" src="${brandFileUrl(file)}"></video>`
      : `<img class="brand-preview" alt="" src="${brandFileUrl(file)}">`;
  const facts = !file ? "Not set"
    : isVideo ? `${seconds(file.duration_ms / 1000)} · ${file.width}×${file.height}`
        + (file.has_audio ? " · with sound" : " · silent")
      : `${file.width}×${file.height} px`;

  let edit = "";
  if (file && isVideo) {
    const key = `${slot.key}_edit`;
    const values = kit[key];
    const whole = file.duration_ms / 1000;
    const runs = timing[`${slot.key}_seconds`];
    const row = (field, label, max, help) => `
      <label class="brand-row">
        <span>${label}</span>
        <input type="range" min="0" max="${max}" step="0.1" value="${values[field]}"
               data-brand-edit="${key}" data-field="${field}">
        <input type="number" min="0" max="${max}" step="0.1" value="${values[field]}"
               data-brand-edit="${key}" data-field="${field}" aria-label="${label}, seconds">
        <em>s</em>
        ${help ? `<small>${help}</small>` : ""}
      </label>`;
    edit = `
      <div class="brand-clip-edit">
        ${row("trim_start", "Cut from the start", Math.max(0, whole - 0.5).toFixed(1))}
        ${row("trim_end", "Cut from the end", Math.max(0, whole - 0.5).toFixed(1))}
        ${row("fade", slot.key === "intro" ? "Cross-fade into the lesson" : "Cross-fade from the lesson",
              limits.cross_fade[1], timing[`${slot.key}_overlap`] < values.fade
                ? `Only ${seconds(timing[`${slot.key}_overlap`])} is used: a cross-fade is never more than half the clip.` : "")}
        <p class="brand-runs">Runs <b>${seconds(runs)}</b> of its ${seconds(whole)}.</p>
      </div>`;
  }

  return `
    <section class="panel brand-slot ${file ? "set" : ""}">
      <div class="panel-head"><h3>${escapeHtml(slot.name)}</h3></div>
      <p class="panel-sub">${escapeHtml(slot.does)}</p>
      ${preview}
      <p class="brand-facts">${file ? `<b>${escapeHtml(file.file_name)}</b> · ` : ""}${escapeHtml(facts)}</p>
      ${edit}
      <div class="assets-actions">
        <label class="btn ${file ? "" : "btn-accent"}">${file ? "Replace" : "Upload"}
          <input type="file" hidden accept="${accept}" data-brand-upload="${slot.key}"></label>
        ${file ? `<button class="btn" data-brand-remove="${slot.key}">Remove</button>` : ""}
      </div>
    </section>`;
}

/* ---- the controls for the selected overlay ---------------------------------------- */

function renderOverlayControls(page) {
  const { kit, limits, overlays, shows } = page.brand;
  const present = OVERLAYS.filter(([slot]) => kit[slot]);
  if (!present.length) {
    return `<p class="muted">Upload a logo or a watermark above to place it on the frame.</p>`;
  }
  if (!kit[brandEditorState.selected]) brandEditorState.selected = present[0][0];
  const slot = brandEditorState.selected;
  const key = `${slot}_place`;
  const place = kit[key];

  const slider = (field, label, [low, high], help = "") => `
    <label class="brand-row">
      <span>${label}</span>
      <input type="range" min="${low * 100}" max="${high * 100}" step="1"
             value="${Math.round(place[field] * 100)}" data-brand-place="${key}" data-field="${field}"
             data-scale="100">
      <output>${Math.round(place[field] * 100)}%</output>
      ${help ? `<small>${help}</small>` : ""}
    </label>`;
  const number = (field, label, max) => `
    <label class="brand-inline">${label}
      <input type="number" min="0" max="${max}" step="0.5" value="${place[field]}"
             data-brand-place="${key}" data-field="${field}"> s</label>`;

  return `
    <div class="seg brand-which">
      ${present.map(([name, label]) => `
        <button class="${name === slot ? "on" : ""}" data-select-overlay="${name}">${label}</button>`).join("")}
    </div>

    <h4 class="brand-group">Where</h4>
    <div class="brand-where">
      <div class="brand-snap" role="group" aria-label="Snap to a place">
        ${["top", "middle", "bottom"].flatMap(row => ["left", "centre", "right"].map(column => `
          <button data-snap="${row}-${column}" title="${row} ${column}" aria-label="${row} ${column}"></button>`)).join("")}
      </div>
      <div class="brand-xy">
        <label class="brand-inline">Across
          <input type="number" min="0" max="100" step="0.5" value="${(place.x * 100).toFixed(1)}"
                 data-brand-place="${key}" data-field="x" data-scale="100"> %</label>
        <label class="brand-inline">Down
          <input type="number" min="0" max="100" step="0.5" value="${(place.y * 100).toFixed(1)}"
                 data-brand-place="${key}" data-field="y" data-scale="100"> %</label>
        <small>Its centre, from the frame's top left. Or drag it on the frame.</small>
      </div>
    </div>

    <h4 class="brand-group">How it looks</h4>
    ${slider("width", "Size", limits.width, "of the frame's width")}
    ${softNote(kit[slot], overlays[slot])}
    ${slider("opacity", "Opacity", limits.opacity)}
    ${slider("radius", "Rounded corners", limits.radius)}
    ${slider("shadow", "Shadow", limits.shadow)}

    <h4 class="brand-group">When it appears</h4>
    <div class="seg brand-show">
      ${shows.map(show => `
        <button class="${place.show === show ? "on" : ""}" data-brand-show="${key}" data-value="${show}">
          ${SHOW_LABELS[show]}</button>`).join("")}
    </div>
    <div class="brand-when">
      ${place.show === "first" || place.show === "last" ? number("seconds", place.show === "first"
          ? "The first" : "The last", limits.seconds[1]) : ""}
      ${place.show === "range" ? number("start", "From", 3600) + number("end", "to", 3600)
          + `<small>Seconds from the start of the lesson.</small>` : ""}
      ${number("fade_in", "Fade in", limits.fade[1])}
      ${number("fade_out", "Fade out", limits.fade[1])}
    </div>`;
}

/** Said when the file is smaller than it is drawn: a stretched logo looks soft. */
function softNote(file, overlay) {
  if (!file || !overlay) return "";
  const drawn = Math.round(overlay.inner_width * 1920);
  return drawn > file.width * 1.25 ? `
    <p class="brand-soft">${icon(ICON.alert, 14, 2.2)} Drawn ${drawn} px wide from a file that is
      ${file.width} px wide, so it is stretched and will look soft in the video. Upload a larger
      file (at least ${drawn} px wide), or make it smaller.</p>` : "";
}

/* ---- the timeline --------------------------------------------------------------------- */

function windowOf(place, lesson) {
  if (place.show === "first") return [0, Math.min(place.seconds, lesson)];
  if (place.show === "last") return [Math.max(0, lesson - place.seconds), lesson];
  if (place.show === "range") return [Math.min(place.start, lesson), Math.min(place.end, lesson)];
  return [0, lesson];
}

export function renderBrandTimeline(page) {
  const { kit, timing } = page.brand;
  const lesson = NOMINAL_LESSON_SECONDS;
  const intro = kit.intro ? timing.intro_seconds : 0;
  const outro = kit.outro ? timing.outro_seconds : 0;
  const total = intro + lesson + outro;
  const share = value => `${(value / total * 100).toFixed(2)}%`;
  const bar = (slot, label) => {
    if (!kit[slot]) return "";
    const [start, end] = windowOf(kit[`${slot}_place`], lesson);
    return `
      <div class="brand-track"><span class="brand-track-name">${label}</span>
        <div class="brand-track-lane">
          <span class="brand-track-bar ${slot}" style="left:${share(intro + start)};width:${share(end - start)}"
                title="${label}: ${seconds(start)} to ${seconds(end)} of the lesson"></span>
        </div></div>`;
  };
  return `
    <div class="brand-timeline">
      <div class="brand-track"><span class="brand-track-name">Video</span>
        <div class="brand-track-lane brand-segments">
          ${intro ? `<span class="segment intro" style="width:${share(intro)}">Intro ${seconds(intro)}</span>` : ""}
          <span class="segment lesson" style="width:${share(lesson)}">Lesson</span>
          ${outro ? `<span class="segment outro" style="width:${share(outro)}">Outro ${seconds(outro)}</span>` : ""}
        </div></div>
      ${bar("logo", "Logo")}${bar("watermark", "Watermark")}
      <p class="panel-sub">Drawn for a lesson of one minute. The real length comes from the
        narration.${timing.intro_overlap ? ` The intro and the lesson share ${seconds(timing.intro_overlap)} of cross-fade.` : ""}${
        timing.outro_overlap ? ` The lesson and the outro share ${seconds(timing.outro_overlap)}.` : ""}
        The logo and watermark sit on the lesson only.</p>
    </div>`;
}

/* ---- the tab ------------------------------------------------------------------------------ */

export function renderBrand(page) {
  const { slots } = page.brand;
  return `
    <div class="brand-grid">${slots.map(slot => renderSlot(slot, page)).join("")}</div>
    <div class="brand-editor">
      <section class="panel">
        <div class="panel-head"><h3>On the lesson frame</h3></div>
        <p class="panel-sub">Drag the logo or the watermark to place it. The dashed line is the
          safe margin. What you see here is the image the render lays on, where it lays it.</p>
        ${renderFrameCanvas(page, { editable: true })}
        ${renderBrandTimeline(page)}
      </section>
      <section class="panel brand-controls">
        <div class="panel-head"><h3>Place and style</h3></div>
        ${renderOverlayControls(page)}
      </section>
    </div>`;
}

/* ---- acting --------------------------------------------------------------------------------- */

export function wireBrandEditor(redraw, page) {
  const save = async options => {
    try {
      await requestJsonFromApi(projectApiPath("/assets/brand-options"), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(options),
      });
    } catch (failure) {
      console.error("saving the brand assets failed", failure);
      showStageNotice("bad", failure.message);
    }
    await redraw();
  };
  const valueOf = input => Number(input.value) / Number(input.dataset.scale || 1);

  document.querySelectorAll("[data-select-overlay]").forEach(button => {
    button.onclick = () => { brandEditorState.selected = button.dataset.selectOverlay; redraw(); };
  });

  // Sliders and number fields: the number beside a slider follows it as it
  // moves; the change is saved when it is let go.
  document.querySelectorAll("[data-brand-place], [data-brand-edit]").forEach(input => {
    const key = input.dataset.brandPlace ?? input.dataset.brandEdit;
    input.oninput = () => {
      const output = input.parentElement.querySelector("output");
      if (output) output.textContent = `${Math.round(Number(input.value))}%`;
      const twin = [...input.parentElement.querySelectorAll("input")].find(other => other !== input);
      if (twin) twin.value = input.value;
    };
    input.onchange = () => save({ [key]: { [input.dataset.field]: valueOf(input) } });
  });
  document.querySelectorAll("[data-brand-show]").forEach(button => {
    button.onclick = () => save({ [button.dataset.brandShow]: { show: button.dataset.value } });
  });

  const canvas = document.querySelector(".brand-canvas.editable");
  const { overlays } = page.brand;

  // The 3×3 grid puts the picture just inside the safe margin.
  document.querySelectorAll("[data-snap]").forEach(button => {
    button.onclick = () => {
      const slot = brandEditorState.selected;
      const box = overlays[slot];
      if (!box) return;
      const [row, column] = button.dataset.snap.split("-");
      const x = { left: SAFE_MARGIN + box.inner_width / 2, centre: 0.5,
                  right: 1 - SAFE_MARGIN - box.inner_width / 2 }[column];
      const y = { top: SAFE_MARGIN + box.inner_height / 2, middle: 0.5,
                  bottom: 1 - SAFE_MARGIN - box.inner_height / 2 }[row];
      save({ [`${slot}_place`]: { x, y } });
    };
  });

  if (!canvas) return;
  canvas.querySelectorAll("[data-overlay]").forEach(element => {
    element.onpointerdown = down => {
      down.preventDefault();
      const slot = element.dataset.overlay;
      const frame = canvas.getBoundingClientRect();
      const start = element.getBoundingClientRect();
      const grab = { x: down.clientX - start.left, y: down.clientY - start.top };
      let moved = false;
      element.setPointerCapture(down.pointerId);
      element.classList.add("dragging");

      element.onpointermove = move => {
        moved = true;
        element.style.left = `${(move.clientX - grab.x - frame.left) / frame.width * 100}%`;
        element.style.top = `${(move.clientY - grab.y - frame.top) / frame.height * 100}%`;
      };
      element.onpointerup = () => {
        element.onpointermove = element.onpointerup = null;
        element.classList.remove("dragging");
        brandEditorState.selected = slot;
        if (!moved) return redraw();
        const now = element.getBoundingClientRect();
        // Its centre, as a share of the frame: what a placement stores.
        return save({ [`${slot}_place`]: {
          x: (now.left + now.width / 2 - frame.left) / frame.width,
          y: (now.top + now.height / 2 - frame.top) / frame.height,
        } });
      };
    };
  });
}
