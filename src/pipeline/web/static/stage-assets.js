/**
 * Assets & Design — four tabs, in the order the work happens.
 *
 * The layer is the inventory and the look. It shows what exists and where it
 * came from, and says everything it does to a picture; it does not judge one.
 *
 * 1. Extracted assets: what the last layer handed on, in a box per file; each
 *    picture with the slide it came from, and one action, Leave out. What
 *    gathering did to a picture (trimmed its border, flagged its crop) is said
 *    on its card, with why, when and how, and can be overruled.
 * 2. Brand assets: a watermark, a logo, an intro and an outro, placed and timed
 *    in an editor (`brand-editor.js`).
 * 3. Look: themes, colours, fonts and background art (`look-editor.js`).
 * 4. Final & transfer: the video as it will look, everything handed on stated,
 *    and the one button that hands it on.
 *
 * Nothing on this layer calls a model: the same pictures and the same choices
 * always give the same result (`assets_handoff.py`).
 */

import {
  renderBrand, renderBrandTimeline, renderFrameCanvas, wireBrandEditor,
} from "/static/brand-editor.js";
import { renderLook, wireLookEditor } from "/static/look-editor.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, footerNav, icon, moveToNextLayerButton, projectApiPath,
  refreshProjectSummary, select, showStageNotice, stageHeader, stageNeighbours, whenItWas,
  wireGotoButtons,
} from "/static/ui-kit.js";

const TABS = [
  ["extracted", "Extracted assets"], ["brand", "Brand assets"], ["look", "Look"],
  ["final", "Final & transfer"],
];

/** The file the video draws: the trimmed copy, unless the original was chosen. */
const pictureUrl = figure => figure.shown_path.startsWith("assets/prepared/")
  ? projectApiPath(`/assets/prepared/${encodeURIComponent(figure.shown_path.split("/").pop())}`)
  : projectApiPath(`/extraction/assets/${encodeURIComponent(figure.asset_path.split("/").pop())}`);

/** View state only: which picture's details are open. */
const view = { openPicture: null };

const currentTab = () =>
  TABS.some(([key]) => key === applicationState.assetsTab) ? applicationState.assetsTab : "extracted";

export async function renderAssetsStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  body.innerHTML = `<div class="card muted">Loading the library…</div>`;

  let page;
  try {
    page = await requestJsonFromApi(projectApiPath("/assets"));
  } catch (loadFailure) {
    console.error("asset library load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load the asset library.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }
  applicationState.assetLibrary = page;
  const tab = currentTab();

  body.innerHTML = `
    ${stageHeader("assets", "Assets & Design", { agentButtonId: "assets-agent-button" })}

    <div class="stage-content stage-content-bare">
      <div class="extraction-tabs assets-tabs">
        <nav class="x-tabs" role="tablist" aria-label="Assets & Design steps">
          ${TABS.map(([key, label], index) => `
            <button role="tab" class="x-tab ${key === tab ? "on" : ""}" data-assets-tab="${key}"
                    aria-selected="${key === tab}">
              <span class="x-tab-number">${index + 1}</span>
              <b class="x-tab-label">${label}</b>
            </button>`).join("")}
        </nav>
        <div class="x-tab-body" role="tabpanel">
          ${{ extracted: renderExtracted, brand: renderBrand, look: renderLook,
              final: () => renderFinal(page, stage) }[tab](page)}
        </div>
      </div>
      ${renderFooter(stage, page, tab)}
    </div>`;

  wire(stage, navigateToStage, renderAgentStage);
}

/* ---- 1. Extracted assets --------------------------------------------------- */

function renderExtracted(page) {
  return renderGather(page) + renderPictures(page);
}

function renderGather(page) {
  const { source, audit, handoff } = page;
  const libraryState = page.is_empty ? ["blocked", "Not gathered yet",
    "Gather the pictures the last transfer contains."]
    : handoff.in_step ? ["ok", "In step with the last transfer",
      `${audit.figure_count} picture(s): ${audit.handed_on_count} handed on`
      + (audit.left_out_count ? `, ${audit.left_out_count} left out.` : ".")]
      : ["warn", "Out of step", "Extraction was transferred again since this was gathered."];

  const transferred = source.files.length > 0;
  return `
    <div class="assets-gather">
      <section class="panel assets-library ${transferred ? libraryState[0] : "blocked"}">
        <div class="panel-head"><h3>The pictures in the source</h3></div>
        ${transferred ? `
          <p class="assets-state"><b>${libraryState[1]}</b><span>${libraryState[2]}</span></p>
          <p class="panel-sub">From the extraction transferred
            ${escapeHtml(whenItWas(source.transferred_at))}.</p>`
          : `<p class="assets-state"><b>Nothing transferred yet</b><span>Extract the source and
               transfer it; its pictures are gathered here.</span></p>
             <button class="btn btn-accent" data-goto="extraction">Go to Extraction</button>`}
        ${page.gone_figures.length ? `<p class="panel-sub">Not in the last transfer, so not
          handed on (your choices are kept in case ${page.gone_figures.length === 1 ? "it comes" : "they come"} back):
          ${page.gone_figures.map(gone => `<b>${escapeHtml(gone)}</b>`).join(", ")}.</p>` : ""}
        <div class="assets-actions">
          <button class="btn btn-accent" data-assets-action="gather" ${source.files.length ? "" : "disabled"}>
            ${page.is_empty ? "Gather pictures" : "Gather again"}</button>
          <button class="btn" data-assets-action="clear" ${page.is_empty && !audit.gone_count ? "disabled" : ""}
                  title="Empty the library: every picture, and what you left out">
            Clear everything</button>
        </div>
      </section>
    </div>`;
}

const originalUrl = figure =>
  projectApiPath(`/extraction/assets/${encodeURIComponent(figure.asset_path.split("/").pop())}`);
const trimmedUrl = figure =>
  projectApiPath(`/assets/prepared/${encodeURIComponent(figure.prepared_path.split("/").pop())}`);
const percent = share => `${Math.round(share * 100)}%`;
/** "the top edge", "the top and left edges", "every edge". */
const edgeWords = edges => !edges?.length ? "an edge"
  : edges.length === 4 ? "every edge"
    : `the ${edges.join(" and ")} edge${edges.length === 1 ? "" : "s"}`;

/** Where a picture came from, in the words a person uses. */
const pictureOrigin = figure => figure.slide_number
  ? `Slide ${figure.slide_number}${figure.slide_title ? ` · ${figure.slide_title}` : ""}`
  : (figure.heading_path.at(-1) ?? figure.file_name);

/**
 * The source's pictures, in its own order: slide by slide for a deck. This tab
 * lists what exists and where it came from; it decides nothing. The one thing a
 * person can do to a picture here is leave it out.
 */
function renderPictures(page) {
  if (!page.figures.length) return "";
  const order = figure => [figure.slide_number || Infinity, page.figures.indexOf(figure)];
  const pictures = [...page.figures].sort((a, b) => {
    const [slideA, atA] = order(a);
    const [slideB, atB] = order(b);
    return slideA - slideB || atA - atB;
  });
  const leftOut = pictures.filter(figure => figure.is_left_out).length;
  return `
    <section class="asset-pictures">
      <h3 class="asset-pictures-head">${pictures.length} picture${pictures.length === 1 ? "" : "s"}${
        leftOut ? ` <span class="file-status left-out">${leftOut} left out</span>` : ""}</h3>
      <div class="figure-grid">${pictures.map(figure => renderFigure(figure, page)).join("")}</div>
    </section>`;
}

function renderFigure(figure, page) {
  const id = escapeHtml(figure.id);
  const open = view.openPicture === figure.id;
  const trimmed = Boolean(figure.prepared_path);
  return `
    <div class="figure-card ${figure.is_left_out ? "left-out" : ""} ${open ? "open" : ""}" data-picture="${id}">
      <img class="figure-thumb" alt="" loading="lazy" src="${pictureUrl(figure)}">
      <div class="figure-body">
        <b>${escapeHtml(pictureOrigin(figure))}</b>
        ${figure.own_caption ? `<span class="figure-caption">${escapeHtml(figure.own_caption)}</span>` : ""}
        <span class="figure-size">${figure.width} × ${figure.height} px${
          figure.origin !== "source" ? ` · ${escapeHtml(figure.origin)}` : ""}</span>
        ${trimmed ? `
          <button class="figure-note-line" data-open-picture="${id}">
            ${figure.use_original
              ? "A plain border was found; you chose to keep the original."
              : `Its plain border was trimmed (${percent(figure.trimmed_fraction)} of the picture).`}
            <u>${open ? "Hide" : "See why"}</u></button>` : ""}
        ${figure.flags.includes("cut_off") ? `
          <button class="figure-note-line ${figure.needs_crop_check ? "asks" : ""}" data-open-picture="${id}">
            ${figure.needs_crop_check
              ? `Check the crop: the picture touches ${escapeHtml(edgeWords(figure.cut_edges))}.`
              : "Crop checked: you said it looks right."}
            <u>${open ? "Hide" : "See why"}</u></button>` : ""}
        ${figure.is_left_out ? `<span class="figure-left-out">Left out: not handed on.</span>` : ""}
      </div>
      <div class="figure-actions">
        <button class="btn" data-leave-out="${id}" data-value="${figure.is_left_out ? "false" : "true"}">
          ${figure.is_left_out ? "Put back" : "Leave out"}</button>
      </div>
      ${open ? renderPictureDetails(figure, page) : ""}
    </div>`;
}

/** What gathering did to this picture, why, when and how, and the person's say. */
function renderPictureDetails(figure, page) {
  const rules = page.picture_rules;
  const id = escapeHtml(figure.id);
  const trim = figure.prepared_path ? `
    <div class="picture-detail">
      <h4>The border was trimmed</h4>
      <div class="picture-compare">
        <figure class="${figure.use_original ? "in-use" : ""}"><img alt="" src="${originalUrl(figure)}">
          <figcaption><b>Original</b> ${figure.width} × ${figure.height} px${
            figure.use_original ? " · in use" : ""}</figcaption></figure>
        <figure class="${figure.use_original ? "" : "in-use"}"><img alt="" src="${trimmedUrl(figure)}">
          <figcaption><b>Trimmed</b> ${figure.prepared_width} × ${figure.prepared_height} px${
            figure.use_original ? "" : " · in use"}</figcaption></figure>
      </div>
      <dl class="picture-why">
        <dt>Why</dt><dd>${percent(figure.trimmed_fraction)} of this picture was a plain border.
          On a video frame that border is wasted screen, and the picture itself is drawn smaller.</dd>
        <dt>When</dt><dd>When pictures are gathered, for any picture whose plain border is more
          than ${percent(rules.trim_at)} of it.</dd>
        <dt>How</dt><dd>The border's colour is read from the picture's edges and cut away. The
          original file is never changed; the trimmed copy is kept beside it.</dd>
      </dl>
      <div class="seg">
        <button class="${figure.use_original ? "" : "on"}" data-use-original="${id}" data-value="false">
          Use the trimmed copy</button>
        <button class="${figure.use_original ? "on" : ""}" data-use-original="${id}" data-value="true">
          Use the original</button>
      </div>
    </div>` : "";

  const edges = figure.cut_edges ?? [];
  const crop = figure.flags.includes("cut_off") ? `
    <div class="picture-detail">
      <h4>Check the crop</h4>
      <div class="picture-crop ${edges.map(edge => `cut-${edge}`).join(" ")}">
        <img alt="" src="${originalUrl(figure)}"></div>
      <p class="picture-crop-key">The red line marks where the picture touches
        <b>${escapeHtml(edgeWords(edges))}</b>.${edges.length === 4 ? ` Touching all four is
        what a picture that simply fills its frame looks like, and is usually fine.` : ""}</p>
      <dl class="picture-why">
        <dt>Why</dt><dd>When a lot of a picture touches its own edge, the crop has usually cut
          through something: a caption, an axis, the last row of a table.</dd>
        <dt>When</dt><dd>When pictures are gathered: if more than ${percent(rules.edge_ink)} of the
          outer ${percent(rules.edge_band)} of an edge is not background.</dd>
        <dt>How</dt><dd>Nothing was changed. This is only a prompt to look. A picture drawn
          right up to its edge on purpose looks the same to this check, and is fine.</dd>
      </dl>
      <div class="assets-actions">
        ${figure.crop_checked
          ? `<button class="btn" data-crop-checked="${id}" data-value="false">Ask me again</button>`
          : `<button class="btn btn-accent" data-crop-checked="${id}" data-value="true">It looks right</button>`}
        <span class="muted">If something is cut, leave it out, or replace the picture on Extraction.</span>
      </div>
    </div>` : "";
  return `<div class="picture-details">${trim}${crop}</div>`;
}

/* ---- 4. Final & transfer -------------------------------------------------- */

function renderFinal(page, stage) {
  const { handoff, look, look_preview: preview } = page;
  const { kit, timing } = page.brand;
  const handedOn = page.figures.filter(figure => !figure.is_left_out);
  const leftOut = page.figures.filter(figure => figure.is_left_out);
  const brandNames = page.brand.slots.filter(slot => kit[slot.key]).map(slot => slot.name);
  const [tone, title, detail] = page.is_empty && !look.is_available && !brandNames.length
    ? ["blocked", "Nothing to transfer yet", "Gather the pictures on the Extracted assets tab."]
    : !page.is_empty && !handoff.in_step
      ? ["stale", "Gather again first", "Extraction was transferred again since this was gathered."]
      : handoff.pending
        ? ["pending", "Ready to transfer", handoff.has_confirmed
            ? "This differs from what the next layer has. Transfer to hand it the changes."
            : "Nothing reaches the next layer until you transfer it."]
        : ["ready", "Transferred to the next layer",
           `The next layer has had exactly this since ${whenItWas(handoff.confirmed_at)}.`];
  const canTransfer = (handoff.in_step || page.is_empty) && handoff.pending;
  const s = value => `${Number(value).toFixed(1)} s`;

  // Each part of the look and the kit, said in a sentence: nothing handed on is
  // left for the reader to work out.
  const when = place => ({
    whole: "for the whole lesson",
    first: `for the first ${s(place.seconds)}`,
    last: `for the last ${s(place.seconds)}`,
    range: `from ${s(place.start)} to ${s(place.end)} of the lesson`,
  }[place.show]) + (place.fade_in ? `, fading in over ${s(place.fade_in)}` : "")
    + (place.fade_out ? `, fading out over ${s(place.fade_out)}` : "");
  const overlayLine = (slot, name) => kit[slot] ? `
    <li><b>${name}</b> (${escapeHtml(kit[slot].file_name)}): ${Math.round(kit[`${slot}_place`].width * 100)}% of
      the frame wide, ${Math.round(kit[`${slot}_place`].opacity * 100)}% opaque, on screen
      ${when(kit[`${slot}_place`])}.</li>` : "";
  const clipLine = (slot, name) => {
    if (!kit[slot]) return "";
    const edit = kit[`${slot}_edit`];
    const cuts = [edit.trim_start ? `${s(edit.trim_start)} cut from its start` : "",
                  edit.trim_end ? `${s(edit.trim_end)} cut from its end` : ""].filter(Boolean);
    const overlap = timing[`${slot}_overlap`];
    return `<li><b>${name}</b> (${escapeHtml(kit[slot].file_name)}): runs ${s(timing[`${slot}_seconds`])}${
      cuts.length ? `, with ${cuts.join(" and ")}` : ""}; ${overlap
        ? `cross-fades with the lesson for ${s(overlap)}` : "cuts straight to the lesson"}.</li>`;
  };
  const clipCard = (slot, name) => {
    if (!kit[slot]) return "";
    const edit = kit[`${slot}_edit`];
    const from = edit.trim_start;
    const to = from + timing[`${slot}_seconds`];
    const url = projectApiPath(`/assets/brand-files/${encodeURIComponent(kit[slot].path.split("/").pop())}`);
    return `
      <figure class="final-part">
        <video controls preload="metadata" src="${url}#t=${from.toFixed(2)},${to.toFixed(2)}"></video>
        <figcaption><b>${name}</b> ${s(timing[`${slot}_seconds`])}</figcaption>
      </figure>`;
  };
  // How a clip meets the lesson: a cut, or a cross-fade of so many seconds.
  const join = slot => !kit[slot] ? "" : `
    <span class="final-join">${timing[`${slot}_overlap`]
      ? `fade ${s(timing[`${slot}_overlap`])}` : "cut"}</span>`;
  const chosen = preview.chosen;

  return `
    <div class="final-head ${tone}">
      <span class="run-icon">${icon(tone === "ready" ? ICON.check : ICON.alert, 18, 2.3)}</span>
      <span class="run-text">
        <b>${escapeHtml(title)}</b>
        <span>${escapeHtml(detail)}</span>
        <span class="final-totals">${handedOn.length} of ${page.figures.length} picture(s) handed on ·
          ${look.use_source_styling ? "the source's styling" : "the renderer's default look"} ·
          ${brandNames.length ? escapeHtml(brandNames.join(", ")) : "no brand assets"}</span>
      </span>
      ${tone === "ready" ? moveToNextLayerButton(stageNeighbours(stage).next, {
          carries: "The transferred pictures and look go on." })
        : `<button class="btn btn-accent btn-transfer" data-assets-action="confirm"
                   ${canTransfer ? "" : "disabled"}>
             Transfer to the next layer ${icon(ICON.arrowRight)}</button>`}
    </div>

    <section class="panel final-video">
      <div class="panel-head"><h3>The video, as it will look</h3></div>
      <p class="panel-sub">Left to right, as it plays. The middle frame is a sample of the lesson
        in your look, with the logo and watermark where and as the render draws them.</p>
      <div class="final-strip">
        ${clipCard("intro", "Intro")}${join("intro")}
        <figure class="final-part final-lesson">
          ${renderFrameCanvas(page)}
          <figcaption><b>The lesson</b> its length comes from the narration</figcaption>
        </figure>
        ${join("outro")}${clipCard("outro", "Outro")}
      </div>
    </section>

    <div class="assets-final">
      <section class="panel">
        <div class="panel-head"><h3>Pictures handed on (${handedOn.length})</h3></div>
        ${handedOn.length ? `<div class="assets-final-strip">${handedOn.map(figure => `
            <figure><img alt="" loading="lazy" src="${pictureUrl(figure)}">
              <figcaption>${escapeHtml(pictureOrigin(figure))}${
                figure.use_original ? " · original" : figure.prepared_path ? " · trimmed" : ""}</figcaption>
            </figure>`).join("")}</div>`
          : `<p class="muted">None: every picture is left out, or none was gathered.</p>`}
        ${leftOut.length ? `<p class="final-left-out"><b>Left out (${leftOut.length}), not handed on:</b>
          ${leftOut.map(figure => escapeHtml(pictureOrigin(figure))).join(" · ")}.</p>` : ""}
      </section>

      <section class="panel">
        <div class="panel-head"><h3>The look</h3></div>
        <p>${look.use_source_styling
          ? "The source's own styling."
          : "The renderer's own look: dark and neutral."}</p>
        <ul class="final-list">
          ${Object.entries({ Background: chosen.background, Panels: chosen.panels, Accent: chosen.accent })
            .map(([name, colour]) => `<li><span class="swatch" style="background:${colour}"></span>
              <b>${name}</b> <code>${colour.toUpperCase()}</code></li>`).join("")}
          <li><b>Headings</b> ${escapeHtml(preview.heading_font || "the renderer's font")}</li>
          <li><b>Body text</b> ${escapeHtml(preview.body_font || "the renderer's font")}</li>
          <li><b>Text reads at</b> ${preview.readability.text_on_panel} : 1${
            preview.readability.text_is_readable ? "" : " — hard to read"}</li>
          ${look.background_asset_path ? `<li><b>Background art</b> ${look.background_art && look.use_source_styling
            ? "drawn behind the frames" : "not drawn behind the frames"}; on the deck's slides:
            ${escapeHtml((page.slide_washes[look.slide_wash] ?? "").split(":")[0].toLowerCase())}.</li>` : ""}
        </ul>
      </section>

      <section class="panel" style="grid-column:1 / -1">
        <div class="panel-head"><h3>Brand assets</h3></div>
        ${brandNames.length ? `<ul class="final-list">
            ${overlayLine("logo", "Logo")}${overlayLine("watermark", "Watermark")}
            ${clipLine("intro", "Intro")}${clipLine("outro", "Outro")}
          </ul>
          ${renderBrandTimeline(page)}` : `<p class="muted">None.</p>`}
      </section>
    </div>`;
}

/* ---- the footer ------------------------------------------------------------ */

function renderFooter(stage, page, tab) {
  const at = TABS.findIndex(([key]) => key === tab);
  const next = TABS[at + 1];
  const { handoff } = page;
  return footerNav(stage, {
    end: next ? `
      <button class="btn btn-accent btn-move-next" data-assets-tab="${next[0]}">
        Move to ${next[1]} ${icon(ICON.arrowRight)}</button>` : null,
    next: {
      carries: handoff.has_confirmed ? "The transferred pictures and look go on." : "",
      warning: !handoff.has_confirmed
        ? "Nothing has been transferred yet. Transfer on the Final & transfer tab first."
        : handoff.pending
          ? "Your latest changes are not transferred — the next layer still reads the last "
            + "transferred version."
          : "",
    },
  });
}

/* ---- acting ---------------------------------------------------------------- */

function wire(stage, navigateToStage, renderAgentStage) {
  const redraw = () => renderAssetsStage(stage, navigateToStage, renderAgentStage);
  const act = async (button, path, body, done) => {
    button.disabled = true;
    try {
      await requestJsonFromApi(projectApiPath(path), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body ?? {}),
      });
      if (done) showStageNotice("ok", done);
      await refreshProjectSummary();
    } catch (failure) {
      console.error("assets action failed", failure);
      showStageNotice("bad", failure.message);
    }
    await redraw();
  };

  wireGotoButtons(navigateToStage);
  select("#assets-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-assets-tab]").forEach(button => {
    button.onclick = async () => {
      applicationState.assetsTab = button.dataset.assetsTab;
      const fromFooter = Boolean(button.closest(".footer-nav"));
      await redraw();
      if (fromFooter) select(".x-tabs")?.scrollIntoView({ block: "start", behavior: "smooth" });
    };
  });

  document.querySelectorAll("[data-assets-action]").forEach(button => {
    const action = button.dataset.assetsAction;
    button.onclick = () => {
      if (action === "gather") return act(button, "/assets/refresh", null, "Gathered.");
      if (action === "clear") {
        if (!window.confirm("Clear everything? Every picture is removed, along with what you "
            + "left out and your trim and crop choices. The library stays empty until you gather "
            + "again.")) return undefined;
        return act(button, "/assets/refresh?clear=true", null, "Cleared.");
      }
      if (action === "styling") {
        const wanted = button.getAttribute("aria-checked") !== "true";
        return act(button, "/assets/look", { use_source_styling: wanted });
      }
      if (action === "confirm") {
        return act(button, "/assets/confirm", null,
          "Transferred: the next layer reads exactly these pictures and this look.");
      }
      return undefined;
    };
  });
  document.querySelectorAll("[data-brand-upload]").forEach(input => {
    input.onchange = async () => {
      const file = input.files[0];
      if (!file) return;
      const form = new FormData();
      form.append("file", file);
      showStageNotice("ok", `Uploading ${file.name}…`);
      try {
        await requestJsonFromApi(projectApiPath(`/assets/brand/${input.dataset.brandUpload}`),
          { method: "POST", body: form });
        showStageNotice("ok", `${file.name} added.`);
      } catch (failure) {
        console.error("brand upload failed", failure);
        showStageNotice("bad", failure.message);
      }
      await redraw();
    };
  });
  document.querySelectorAll("[data-brand-remove]").forEach(button => {
    button.onclick = async () => {
      button.disabled = true;
      try {
        await requestJsonFromApi(projectApiPath(`/assets/brand/${button.dataset.brandRemove}`),
          { method: "DELETE" });
      } catch (failure) {
        showStageNotice("bad", failure.message);
      }
      await redraw();
    };
  });
  wireBrandEditor(redraw, applicationState.assetLibrary);
  wireLookEditor(act);
  document.querySelectorAll("[data-wash]").forEach(button => {
    button.onclick = () => act(button, "/assets/wash", { wash: button.dataset.wash });
  });
  const picture = (selector, key, field) =>
    document.querySelectorAll(selector).forEach(button => {
      button.onclick = () => act(button, `/assets/pictures/${encodeURIComponent(button.dataset[key])}`,
        { [field]: button.dataset.value === "true" });
    });
  picture("[data-leave-out]", "leaveOut", "left_out");
  picture("[data-use-original]", "useOriginal", "use_original");
  picture("[data-crop-checked]", "cropChecked", "crop_checked");

  document.querySelectorAll("[data-open-picture]").forEach(button => {
    button.onclick = () => {
      view.openPicture = view.openPicture === button.dataset.openPicture
        ? null : button.dataset.openPicture;
      redraw();
    };
  });
}
