/**
 * The files themselves, drawn from their own bytes.
 *
 * Every format is shown raw: a PDF in the browser's viewer, a deck and a Word
 * document rendered client-side from the uploaded file, markdown and text as
 * written. Nothing is converted on the server and nothing derived is written to
 * disk, because the same raw file is what moves on to the later stages.
 *
 * A module of its own because two pages need it. It used to live inside app.js,
 * which the stage modules cannot import without a cycle, so the Extraction
 * page's Preview tab said "Document rendering is not built yet" while Inputs,
 * one tab away, rendered the same file perfectly.
 */

import { requestBytesFromApi } from "/static/shared-client.js";
import { escapeHtml, formatFileSize, icon, projectApiPath } from "/static/ui-kit.js";

/** The frame around a file: what it is, and ways to open it outside the page.
 *  `openRawFile` then fills the body with the file itself. */
export function renderRawFileShell(fileName, preview) {
  const rawUrl = projectApiPath(`/sources/${encodeURIComponent(fileName)}`);
  const size = formatFileSize(preview.bytes);

  const header = (note) => `
    <div class="preview-meta">
      <span>${escapeHtml(note)}</span>
      <div class="spacer"></div>
      <a class="btn" href="${rawUrl}" target="_blank" rel="noopener">Open in a tab</a>
      <a class="btn" href="${rawUrl}" download>Download</a>
    </div>`;

  if (preview.viewer === "pdf") {
    return header(`${size} · shown by the browser's own PDF viewer`)
      + `<iframe class="file-embed" src="${rawUrl}" title="${escapeHtml(fileName)}"></iframe>`;
  }

  if (preview.viewer === "slides") {
    return header(`${size} · the deck itself`)
      + `<div class="slide-stage" data-slides-for="${escapeHtml(fileName)}">
           <p class="muted" style="margin:0">Opening the deck…</p>
         </div>`;
  }

  if (preview.viewer === "document") {
    return header(`${size} · the document itself`)
      + `<div class="doc-stage" data-document-for="${escapeHtml(fileName)}">
           <p class="muted" style="margin:0">Opening the document…</p>
         </div>`;
  }

  if (preview.viewer === "plain") {
    return header(`${size} · the file as written`)
      + `<pre class="file-text" data-plain-for="${escapeHtml(fileName)}"
           >Reading…</pre>`;
  }

  return header(`${size} · this type cannot be shown here`);
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
async function openDeck(fileName, stage) {
  // The same deck can be open on two stages; the older viewer goes first.
  releaseRawFile(fileName);
  try {
    const renderer = await loadSlideRenderer();
    const bytes = await requestBytesFromApi(
      projectApiPath(`/sources/${encodeURIComponent(fileName)}`));

    stage.innerHTML = "";
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

    fitStageToSlide(stage);
    stage.dataset.slideCount = String(previewer.slideCount ?? "");
    deckViewers.set(fileName, previewer);
    renderDeckControls(stage, previewer);
  } catch (deckFailure) {
    console.error("deck render failed", deckFailure);
    stage.innerHTML = `<p class="muted" style="margin:0">
      This deck could not be drawn — ${escapeHtml(deckFailure.message)}.
      Use <b>Open in a tab</b> or <b>Download</b> to view it.</p>`;
  }
}

/** Live viewers, so a collapsed preview can release its slides. */
const deckViewers = new Map();

/** Draw the file itself, using whichever renderer suits it.
 *
 *  Every branch here reads the same bytes the pipeline stores. Nothing is
 *  converted on the server and nothing derived is written to disk.
 */
export function openRawFile(panel, fileName, viewer) {
  if (viewer === "slides") {
    const stage = panel.querySelector(`[data-slides-for="${CSS.escape(fileName)}"]`);
    if (stage) openDeck(fileName, stage);
    return;
  }
  if (viewer === "document") {
    const stage = panel.querySelector(`[data-document-for="${CSS.escape(fileName)}"]`);
    if (stage) openDocument(fileName, stage);
    return;
  }
  if (viewer === "plain") {
    const pre = panel.querySelector(`[data-plain-for="${CSS.escape(fileName)}"]`);
    if (pre) openPlainText(fileName, pre);
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
      This document could not be drawn — ${escapeHtml(documentFailure.message)}.
      Use <b>Open in a tab</b> or <b>Download</b> to read it.</p>`;
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

  wrapper.style.height = `${slideHeight}px`;
  stage.style.height = `${slideHeight + 24}px`;
}

/** Our own transport for the deck.
 *
 *  The bundled one counts from zero -- "0/50" on the first slide -- and does not
 *  match anything else in this interface. These call the same methods and count
 *  the way people do.
 */
function renderDeckControls(stage, previewer) {
  const total = previewer.slideCount ?? 0;
  const bar = document.createElement("div");
  bar.className = "deck-controls";
  bar.innerHTML = `
    <button class="btn-icon" data-deck="previous" title="Previous slide"
            aria-label="Previous slide">${icon(`<path d="M15 18l-6-6 6-6"/>`, 16, 2.2)}</button>
    <span class="deck-count mono"></span>
    <button class="btn-icon" data-deck="next" title="Next slide"
            aria-label="Next slide">${icon(`<path d="M9 18l6-6-6-6"/>`, 16, 2.2)}</button>`;
  stage.after(bar);

  const counter = bar.querySelector(".deck-count");
  const update = () => {
    counter.textContent = `${(previewer.currentIndex ?? 0) + 1} / ${total}`;
    fitStageToSlide(stage);
  };

  bar.querySelector('[data-deck="previous"]').onclick = () => {
    previewer.renderPreSlide();
    update();
  };
  bar.querySelector('[data-deck="next"]').onclick = () => {
    previewer.renderNextSlide();
    update();
  };
  update();
}

/** Let go of a rendered deck. A 40-slide deck is a lot of DOM to keep in a
 *  panel nobody is looking at, and reopening re-renders it in a moment. */
export function releaseRawFile(fileName) {
  if (!deckViewers.has(fileName)) return false;
  deckViewers.get(fileName).destroy?.();
  deckViewers.delete(fileName);
  return true;
}
