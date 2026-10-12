/**
 * The files themselves, drawn from their own bytes.
 *
 * Every format is shown raw: a deck, a PDF and a Word document rendered
 * client-side from the uploaded file, markdown and text as written. Nothing is
 * converted on the server and nothing derived is written to disk, because the
 * same raw file is what moves on to the later stages.
 *
 * Decks and PDFs are paged: a strip of thumbnails down the left moves through
 * them and, where a page allows it, deletes slides or pages from the file. A
 * page that shows a deck beside something else moves through it with its own
 * arrows instead, through `stepRawFile`. Either way the page on screen is
 * announced as a `deck-slide` event.
 *
 * A module of its own because two pages need it, and the stage modules cannot
 * import app.js without a cycle.
 */

import { requestBytesFromApi, requestJsonFromApi } from "/static/shared-client.js";
import { escapeHtml, icon, projectApiPath, showStageNotice } from "/static/ui-kit.js";

/** The frame for a file; `openRawFile` then fills it with the file itself.
 *  Just the file: its size is already on the row above it. `pdfPages` draws a
 *  PDF page by page with a strip, instead of in the browser's own viewer. */
export function renderRawFileShell(fileName, preview, { pdfPages = false } = {}) {
  const rawUrl = projectApiPath(`/sources/${encodeURIComponent(fileName)}`);

  if (preview.viewer === "pdf") {
    return pdfPages
      ? `<div class="slide-stage pdf-stage" data-pdf-for="${escapeHtml(fileName)}">
           <p class="muted" style="margin:0">Opening the PDF…</p>
         </div>`
      : `<iframe class="file-embed" src="${rawUrl}" title="${escapeHtml(fileName)}"></iframe>`;
  }

  if (preview.viewer === "slides") {
    return `<div class="slide-stage" data-slides-for="${escapeHtml(fileName)}">
              <p class="muted" style="margin:0">Opening the deck…</p>
            </div>`;
  }

  if (preview.viewer === "document") {
    return `<div class="doc-stage" data-document-for="${escapeHtml(fileName)}">
              <p class="muted" style="margin:0">Opening the document…</p>
            </div>`;
  }

  if (preview.viewer === "plain") {
    return `<pre class="file-text" data-plain-for="${escapeHtml(fileName)}"
              >Reading…</pre>`;
  }

  return `<p class="muted" style="margin:0">This type cannot be shown here.</p>`;
}

/** Draw the file itself, using whichever renderer suits it.
 *
 *  `editable`: a deck's slides or a PDF's pages can be deleted (Inputs).
 *  `slideStrip`: move through a deck by its thumbnails; off, the page moves
 *  through it with `stepRawFile`.
 */
export function openRawFile(panel, fileName, viewer, { editable = false, slideStrip = true } = {}) {
  const find = attribute => panel.querySelector(`[${attribute}="${CSS.escape(fileName)}"]`);
  if (viewer === "slides") {
    const stage = find("data-slides-for");
    if (stage) openDeck(fileName, stage, { editable, slideStrip });
  } else if (viewer === "pdf") {
    const stage = find("data-pdf-for");
    if (stage) openPdf(fileName, stage, { editable });
  } else if (viewer === "document") {
    const stage = find("data-document-for");
    if (stage) openDocument(fileName, stage);
  } else if (viewer === "plain") {
    const pre = find("data-plain-for");
    if (pre) openPlainText(fileName, pre);
  }
}

/** Files drawn page by page, so they can be let go of and stepped through. */
const openViewers = new Map();

/** Let go of a rendered deck or PDF. A 40-slide deck is a lot of DOM to keep in
 *  a panel nobody is looking at, and reopening re-renders it in a moment. */
export function releaseRawFile(fileName) {
  const viewer = openViewers.get(fileName);
  openViewers.delete(fileName);
  viewer?.release();
  return Boolean(viewer);
}

/** Move a paged file on or back, for a page with its own arrows. */
export function stepRawFile(fileName, delta) {
  openViewers.get(fileName)?.step(delta);
}

/** The stage inside a layout that has room for a strip, or not. Laid out
 *  before anything is measured, so the page is sized to the space it gets. */
function frameStage(stage, withStrip) {
  const layout = document.createElement("div");
  layout.className = withStrip ? "deck-layout" : "deck-layout deck-arrows";
  stage.before(layout);
  layout.append(stage);
  return layout;
}

/* ---- viewing a deck ------------------------------------------------------ */

/** The renderer is 1.3 MB, so it is fetched the first time a deck is opened and
 *  never on a page that has none. */
let slideRendererPromise = null;
function loadSlideRenderer() {
  slideRendererPromise ??= new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "/static/vendor/pptx-preview.umd.js";
    script.onload = () => resolve(window.pptxPreview);
    script.onerror = () => reject(new Error("the slide renderer could not be loaded"));
    document.head.appendChild(script);
  });
  return slideRendererPromise;
}

/** Render the deck from its own bytes.
 *
 *  No conversion: the `.pptx` is fetched as it sits on disk and drawn by the
 *  browser. Nothing derived is written, and the file that goes on to the rest
 *  of the pipeline is the same file you are looking at.
 */
async function openDeck(fileName, stage, { editable = false, slideStrip = true } = {}) {
  // The same deck can be open on two stages; the older viewer goes first.
  releaseRawFile(fileName);
  try {
    const renderer = await loadSlideRenderer();
    const bytes = await requestBytesFromApi(
      projectApiPath(`/sources/${encodeURIComponent(fileName)}`));
    // The page may have been redrawn while a large deck was downloading; a
    // later open of the same deck is the one on screen, and this one must not
    // take its place.
    if (!stage.isConnected) return;

    stage.innerHTML = "";
    const layout = frameStage(stage, slideStrip);

    // Inside the padding, so the slide fits rather than forcing a horizontal
    // scrollbar for the last twenty pixels.
    const width = Math.max(320, Math.floor((stage.clientWidth || 880) - 24));

    // A generous height first, because the deck's shape is not known until it
    // is open: a 4:3 deck rendered into a 16:9 box loses its title and its
    // footer off the top and bottom, which is exactly what happened.
    const previewer = renderer.init(stage, {
      width, height: Math.round(width * 0.8), mode: "slide",
    });
    await previewer.preview(bytes);
    if (!stage.isConnected) {
      previewer.destroy?.();
      return;
    }
    fitStageToSlide(stage);
    const refit = keepDeckFitted(stage, width);

    const deck = previewer.pptx;
    const aspect = deck?.width && deck?.height ? deck.height / deck.width : 9 / 16;
    const pages = {
      layout, stage, fileName, editable, noun: "slide",
      total: previewer.slideCount ?? 0,
      thumbHeight: Math.round(THUMB_WIDTH * aspect),
      current: () => previewer.currentIndex ?? 0,
      show: index => {
        showSlide(previewer, index);
        fitStageToSlide(stage);
      },
      drawThumb: deckThumbnails(layout, previewer),
      reopen: () => openDeck(fileName, stage, { editable, slideStrip }),
    };
    const navigation = slideStrip ? renderPageStrip(pages) : announceOnly(pages);

    openViewers.set(fileName, {
      step: navigation.step,
      release: () => {
        refit.disconnect();
        navigation.release();
        previewer.destroy?.();
      },
    });
  } catch (deckFailure) {
    console.error("deck render failed", deckFailure);
    stage.innerHTML = `<p class="muted" style="margin:0">
      This deck could not be drawn — ${escapeHtml(deckFailure.message)}.</p>`;
  }
}

/** Jump the deck to one slide. The renderer only knows "next" and "previous",
 *  but those are just these three steps. */
function showSlide(previewer, index) {
  previewer.removeCurrentSlide();
  previewer.currentIndex = index;
  previewer.htmlRender.renderSlide(index);
  previewer.updatePagination?.();
}

/** Thumbnails of a deck, drawn from the deck already parsed for the main view:
 *  a second renderer borrows its parsed file rather than reading 100 MB again.
 *  It writes each slide into a container out of sight; every slide is moved
 *  into its thumbnail once drawn. */
function deckThumbnails(layout, previewer) {
  const Renderer = previewer.htmlRender?.constructor;
  if (!Renderer || !previewer.pptx) return null;
  const scratch = document.createElement("div");
  scratch.className = "deck-strip-scratch";
  layout.append(scratch);

  const deck = previewer.pptx;
  const thumbHeight = Math.round(THUMB_WIDTH * (deck.height / deck.width || 9 / 16));
  const thumbnails = new Renderer(scratch, deck, {
    viewPort: { width: THUMB_WIDTH, height: thumbHeight }, mode: "list",
  });
  return (index, frame) => {
    thumbnails.renderSlide(index);
    const slide = scratch.querySelector(`.pptx-preview-slide-wrapper-${index}`);
    if (!slide) return;
    Object.assign(slide.style, { position: "relative", top: "0", left: "0", margin: "0" });
    frame.append(slide);
  };
}

/** Keep a deck the width of its column as the column changes -- dragging the
 *  boundary beside it, or resizing the window. The slide was drawn at one
 *  width; it is scaled to the new one rather than drawn again, which for a
 *  100 MB deck would mean reading the file again. */
function keepDeckFitted(stage, drawnWidth) {
  let lastWidth = stage.clientWidth;
  const watcher = new ResizeObserver(() => {
    const width = stage.clientWidth;
    if (!stage.isConnected || width === lastWidth) return;
    lastWidth = width;
    const wrapper = stage.querySelector(".pptx-preview-wrapper");
    if (!wrapper) return;
    wrapper.style.zoom = String(Math.max(0.3, (width - 24) / drawnWidth));
    fitStageToSlide(stage);
  });
  watcher.observe(stage);
  return watcher;
}

/* ---- viewing a PDF, page by page ------------------------------------------ */

/** pdf.js is fetched the first time a PDF is opened this way. */
let pdfLibraryPromise = null;
function loadPdfLibrary() {
  pdfLibraryPromise ??= import("/static/vendor/pdf.min.js").then(pdfjs => {
    pdfjs.GlobalWorkerOptions.workerSrc = "/static/vendor/pdf.worker.min.js";
    return pdfjs;
  });
  return pdfLibraryPromise;
}

/** A PDF as a deck is shown: its pages down the left, one at full width.
 *
 *  Drawn from its own bytes by pdf.js. The page is drawn again, sharp, when its
 *  column changes width; the thumbnails are drawn as they scroll into view.
 */
async function openPdf(fileName, stage, { editable = false } = {}) {
  releaseRawFile(fileName);
  try {
    const pdfjs = await loadPdfLibrary();
    const bytes = await requestBytesFromApi(
      projectApiPath(`/sources/${encodeURIComponent(fileName)}`));
    const pdf = await pdfjs.getDocument({ data: bytes }).promise;
    if (!stage.isConnected) {
      pdf.destroy();
      return;
    }

    stage.innerHTML = "";
    const layout = frameStage(stage, true);
    const canvas = document.createElement("canvas");
    canvas.className = "pdf-page";
    stage.append(canvas);

    let current = 0;
    let drawing = null;
    const drawPage = async index => {
      const page = await pdf.getPage(index + 1);
      const natural = page.getViewport({ scale: 1 });
      const scale = Math.max(240, stage.clientWidth - 24) / natural.width;
      const ratio = window.devicePixelRatio || 1;
      const viewport = page.getViewport({ scale: scale * ratio });
      drawing?.cancel();
      canvas.width = Math.floor(viewport.width);
      canvas.height = Math.floor(viewport.height);
      canvas.style.width = `${Math.floor(natural.width * scale)}px`;
      canvas.style.height = `${Math.floor(natural.height * scale)}px`;
      stage.style.height = `${Math.floor(natural.height * scale) + 24}px`;
      drawing = page.render({ canvasContext: canvas.getContext("2d"), viewport });
      try {
        await drawing.promise;
      } catch (renderFailure) {
        if (renderFailure?.name !== "RenderingCancelledException") throw renderFailure;
      }
    };
    await drawPage(0);

    const first = (await pdf.getPage(1)).getViewport({ scale: 1 });
    const navigation = renderPageStrip({
      layout, stage, fileName, editable, noun: "page",
      total: pdf.numPages,
      thumbHeight: Math.round(THUMB_WIDTH * first.height / first.width),
      current: () => current,
      show: index => {
        current = index;
        return drawPage(index);
      },
      drawThumb: async (index, frame) => {
        const page = await pdf.getPage(index + 1);
        const natural = page.getViewport({ scale: 1 });
        const ratio = window.devicePixelRatio || 1;
        const viewport = page.getViewport({ scale: (THUMB_WIDTH / natural.width) * ratio });
        const thumbnail = document.createElement("canvas");
        thumbnail.width = Math.floor(viewport.width);
        thumbnail.height = Math.floor(viewport.height);
        thumbnail.className = "pdf-thumb";
        await page.render({ canvasContext: thumbnail.getContext("2d"), viewport }).promise;
        frame.append(thumbnail);
      },
      reopen: () => openPdf(fileName, stage, { editable }),
    });

    let lastWidth = stage.clientWidth;
    const refit = new ResizeObserver(() => {
      if (!stage.isConnected || stage.clientWidth === lastWidth) return;
      lastWidth = stage.clientWidth;
      drawPage(current);
    });
    refit.observe(stage);

    openViewers.set(fileName, {
      step: navigation.step,
      release: () => {
        refit.disconnect();
        navigation.release();
        pdf.destroy();
      },
    });
  } catch (pdfFailure) {
    console.error("pdf render failed", pdfFailure);
    stage.innerHTML = `<p class="muted" style="margin:0">
      This PDF could not be drawn — ${escapeHtml(pdfFailure.message)}.</p>`;
  }
}

/** A .docx drawn from its own bytes: styles, headings, tables and images. */
async function openDocument(fileName, stage) {
  try {
    const renderer = await loadDocumentRenderer();
    const bytes = await requestBytesFromApi(
      projectApiPath(`/sources/${encodeURIComponent(fileName)}`));
    stage.innerHTML = "";
    await renderer.renderAsync(bytes, stage, null, {
      className: "docx", inWrapper: true, ignoreWidth: false,
      breakPages: true, experimental: true,
    });
    fitDocumentToWidth(stage);
  } catch (documentFailure) {
    console.error("document render failed", documentFailure);
    stage.innerHTML = `<p class="muted" style="margin:0">
      This document could not be drawn — ${escapeHtml(documentFailure.message)}.</p>`;
  }
}

/** Scale a rendered Word document down to the width it has been given.
 *
 *  The renderer draws pages at their real width, about 816 pixels. In a narrower
 *  panel the page was centred and overflowed on both sides, and the left margin
 *  -- where every line begins -- could not be scrolled to. Scaling keeps the
 *  page's own layout, which is the point of showing the file rather than text.
 *  Refitted when the panel changes size, and never enlarged past real size.
 */
function fitDocumentToWidth(stage) {
  const wrapper = stage.querySelector(".docx-wrapper");
  if (!wrapper) return;

  const fit = () => {
    wrapper.style.zoom = "1";
    // The widest page plus the wrapper's padding -- not `scrollWidth`. The pages
    // are centred, so they overflow on both sides, and scrollWidth only counts
    // overflow to the right: it reported 680 pixels for a page needing 830, and
    // the scaled page was still cut off on the left.
    const padding = getComputedStyle(wrapper);
    const natural = Math.max(0, ...[...wrapper.children].map(page => page.offsetWidth))
      + parseFloat(padding.paddingLeft) + parseFloat(padding.paddingRight);
    const available = stage.clientWidth;
    if (natural > 0 && available > 0 && natural > available) {
      wrapper.style.zoom = String(Math.max(0.35, available / natural));
    }
  };
  fit();
  new ResizeObserver(() => { if (stage.isConnected) fit(); }).observe(stage);
}

/** Markdown and plain text are already text: show the bytes, not a reading of
 *  them. */
async function openPlainText(fileName, pre) {
  try {
    const bytes = await requestBytesFromApi(
      projectApiPath(`/sources/${encodeURIComponent(fileName)}`));
    pre.textContent = new TextDecoder("utf-8").decode(bytes);
  } catch (textFailure) {
    console.error("text read failed", textFailure);
    pre.textContent = `Could not read this file — ${textFailure.message}`;
  }
}

/** jszip first: docx-preview expects it as a global. */
let documentRendererPromise = null;
function documentScript(source) {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = source;
    script.onload = resolve;
    script.onerror = () => reject(new Error(`could not load ${source}`));
    document.head.appendChild(script);
  });
}
function loadDocumentRenderer() {
  documentRendererPromise ??= (async () => {
    if (!window.JSZip) await documentScript("/static/vendor/jszip.min.js");
    if (!window.docx) await documentScript("/static/vendor/docx-preview.min.js");
    return window.docx;
  })();
  return documentRendererPromise;
}


/** Size the stage to whatever shape this deck actually is.
 *
 *  A deck can be 4:3 or 16:9 and the renderer honours the file, so the
 *  container has to follow the slide rather than the other way round.
 */
function fitStageToSlide(stage) {
  const wrapper = stage.querySelector(".pptx-preview-wrapper");
  const slide = stage.querySelector(".pptx-preview-slide-wrapper");
  if (!wrapper || !slide) return;

  // The renderer places the slide absolutely and offsets it down inside whatever
  // height it was handed -- a height that can only ever be a guess, because the
  // deck's own shape is not known until it has been parsed. Pinning the slide to
  // the top removes that offset instead of measuring around it: measuring from
  // the wrapper's top to the slide's bottom kept the empty band and merely moved
  // it inside the border, which is how 128 pixels of nothing survived above
  // every slide.
  slide.style.top = "0px";

  const slideHeight = Math.ceil(slide.getBoundingClientRect().height);
  if (slideHeight <= 0) return;

  // Measured on screen, so after any scaling; the wrapper's own height is set
  // before it, so it is divided back out.
  const zoom = parseFloat(wrapper.style.zoom) || 1;
  wrapper.style.height = `${slideHeight / zoom}px`;
  stage.style.height = `${slideHeight + 24}px`;
}

/* ---- moving through pages -------------------------------------------------- */

const THUMB_WIDTH = 150;
const TRASH_ICON = '<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>';

/** Say which page is on screen, so a page beside the file can follow it. */
function announce(fileName, index, total) {
  document.dispatchEvent(new CustomEvent("deck-slide", { detail: { fileName, index, total } }));
}

/** No strip: the page moves through the file with its own arrows. */
function announceOnly({ layout, stage, fileName, total, current, show }) {
  announce(fileName, current(), total);
  return {
    release: () => layout.isConnected && layout.replaceWith(stage),
    step: async delta => {
      const index = Math.min(total - 1, Math.max(0, current() + delta));
      if (index === current()) return;
      await show(index);
      announce(fileName, index, total);
    },
  };
}

/** Every page, small, down the left of the file -- as PowerPoint shows a deck --
 *  and the way to move through it. The same strip for a deck's slides and a
 *  PDF's pages; `noun` says which.
 *
 *  Thumbnails are drawn only as they scroll into view, so an 80-page file does
 *  not render 80 pages before the first one can be seen.
 *
 *  Where the file is `editable`, every page has a delete button. Deleting only
 *  marks it; nothing leaves the file until Save, which asks first.
 */
function renderPageStrip({
  layout, stage, fileName, total, thumbHeight, noun, current, show, drawThumb, editable, reopen,
}) {
  const unwrap = () => layout.isConnected && layout.replaceWith(stage);
  if (total < 2) {
    announce(fileName, 0, total);
    return { release: unwrap, step: () => {} };
  }
  const Noun = noun[0].toUpperCase() + noun.slice(1);
  const plural = count => `${count} ${noun}${count === 1 ? "" : "s"}`;

  const rail = document.createElement("div");
  rail.className = `deck-strip${editable ? " editable" : ""}`;
  rail.setAttribute("role", "listbox");
  rail.setAttribute("aria-label", `${Noun}s`);
  rail.style.setProperty("--thumb-height", `${thumbHeight}px`);
  rail.innerHTML = Array.from({ length: total }, (_, index) => `
    <div class="deck-thumb" data-thumb="${index}">
      <button class="deck-thumb-pick" data-slide="${index}" role="option"
              aria-selected="false" title="${Noun} ${index + 1}">
        <span class="deck-thumb-number">${index + 1}</span>
        <span class="deck-thumb-frame"></span>
      </button>
      ${editable ? `
        <button class="deck-thumb-delete" data-delete-slide="${index}"
                title="Delete ${noun} ${index + 1}" aria-label="Delete ${noun} ${index + 1}">
          ${icon(TRASH_ICON, 14, 2)}
        </button>` : ""}
    </div>`).join("");
  layout.prepend(rail);

  const editBar = document.createElement("div");
  editBar.className = "deck-edit-bar";
  editBar.hidden = true;
  layout.before(editBar);

  const watcher = drawThumb && new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      watcher.unobserve(entry.target);
      const index = Number(entry.target.dataset.slide);
      Promise.resolve()
        .then(() => drawThumb(index, entry.target.querySelector(".deck-thumb-frame")))
        .catch(thumbnailFailure => {
          // A page that cannot be drawn small keeps its number; the file itself
          // is unaffected.
          console.warn(`${noun} ${index + 1} thumbnail failed`, thumbnailFailure);
        });
    }
  }, { root: rail, rootMargin: "240px 0px" });
  if (watcher) rail.querySelectorAll(".deck-thumb-pick").forEach(pick => watcher.observe(pick));

  const thumb = index => rail.querySelector(`[data-thumb="${index}"]`);

  const highlight = () => {
    const index = current();
    rail.style.height = stage.style.height;
    rail.querySelectorAll(".deck-thumb").forEach(item => {
      const on = Number(item.dataset.thumb) === index;
      item.classList.toggle("on", on);
      item.querySelector(".deck-thumb-pick").setAttribute("aria-selected", String(on));
      if (on) item.scrollIntoView({ block: "nearest" });
    });
    announce(fileName, index, total);
  };
  const go = async index => {
    await show(index);
    highlight();
  };

  // --- deleting ---
  const marked = new Set();

  const renderEditBar = () => {
    editBar.hidden = !marked.size;
    editBar.innerHTML = `
      <span class="deck-edit-note">${plural(marked.size)} marked for deletion</span>
      <div class="spacer"></div>
      <button class="btn" data-deck-edit="cancel">Cancel</button>
      <button class="btn btn-accent" data-deck-edit="save" ${marked.size ? "" : "disabled"}>
        Save changes</button>`;
  };

  const toggleMark = index => {
    if (marked.has(index)) marked.delete(index);
    else marked.add(index);
    const isMarked = marked.has(index);
    const item = thumb(index);
    item.classList.toggle("marked", isMarked);
    const button = item.querySelector(".deck-thumb-delete");
    button.title = `${isMarked ? "Keep" : "Delete"} ${noun} ${index + 1}`;
    button.setAttribute("aria-label", button.title);
    button.innerHTML = isMarked
      ? icon(`<path d="M3 12a9 9 0 1 0 3-6.7L3 8M3 3v5h5"/>`, 13, 2.6)
      : icon(TRASH_ICON, 14, 2);
    renderEditBar();
  };

  const save = async button => {
    const numbers = [...marked].sort((a, b) => a - b).map(index => index + 1);
    if (!window.confirm(`Delete ${plural(numbers.length)} from ${fileName}? `
      + "This changes the file itself and cannot be undone.")) return;

    button.disabled = true;
    button.textContent = "Saving…";
    try {
      const saved = await requestJsonFromApi(
        projectApiPath(`/sources/${encodeURIComponent(fileName)}/pages/delete`), {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ pages: numbers }),
        });
      showStageNotice("ok",
        `Deleted ${plural(saved.deleted)} from ${fileName}; ${saved.remaining} left. `
        + "Extract it again so later stages see the change.");
      document.dispatchEvent(new CustomEvent("deck-edited", { detail: saved }));
      // It is a different file now: draw it again from its new bytes.
      reopen();
    } catch (saveFailure) {
      console.error(`${noun} deletion failed`, saveFailure);
      showStageNotice("bad", `Could not save ${fileName} — ${saveFailure.message}`);
      button.disabled = false;
      button.textContent = "Save changes";
    }
  };

  rail.onclick = event => {
    const remove = event.target.closest("[data-delete-slide]");
    if (remove) {
      toggleMark(Number(remove.dataset.deleteSlide));
      return;
    }
    const pick = event.target.closest("[data-slide]");
    if (pick) go(Number(pick.dataset.slide));
  };

  editBar.onclick = event => {
    const action = event.target.closest("[data-deck-edit]");
    if (action?.dataset.deckEdit === "cancel") [...marked].forEach(toggleMark);
    if (action?.dataset.deckEdit === "save") save(action);
  };

  highlight();

  return {
    step: delta => go(Math.min(total - 1, Math.max(0, current() + delta))),
    release: () => {
      watcher?.disconnect();
      editBar.remove();
      rail.remove();
      unwrap();
    },
  };
}
