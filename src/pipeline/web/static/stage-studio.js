/**
 * Studio stage — preview, multi-track timeline, and clip properties.
 *
 * The composition is the artifact: tracks bottom-to-top, clips placed on an
 * absolute millisecond timeline. Everything here reads and writes that one
 * document, so a clip cannot exist on screen without existing in the file.
 *
 * The preview plays the timeline itself: press play and the playhead runs,
 * the frame at the playhead is drawn from the clips under it, and narration
 * clips play their audio. A rendered video is watched in Reviewing; this is
 * the editor's live view of what is on the timeline right now.
 */

import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, icon, projectApiPath, select,
  showStageNotice, stageIcon,
} from "/static/ui-kit.js";

/** View-only state. The playhead and selection are not part of the saved
 *  composition — reopening the stage should not restore a caret position. */
// Below this share of the timeline a clip is too few pixels wide to hit. The
// stylesheet widens these to a usable target; the cost is a few pixels of
// overlap with the clip after them, which is worth paying for a clip that can
// be selected.
const NARROWEST_CLICKABLE_PERCENT = 0.8;

const studioViewState = {
  selectedClipId: null,
  playheadMs: 0,
};

/** Playback is view state too: never saved, and it stops when you leave Studio
 *  or switch project. `audioElement` plays whichever narration clip is under
 *  the playhead. */
const playback = {
  isPlaying: false,
  frameRequest: 0,
  lastTickAt: 0,
  projectSlug: null,
  audioElement: null,
  audioClipId: null,
  lastFrameKey: "",
};

/** Width of the track headers: lanes (and the ruler) start this far in. */
const TRACK_HEAD_WIDTH_PX = 112;

const PLAY_ICON = `<path d="M5 3l14 9-14 9V3z"/>`;
const PAUSE_ICON = `<path d="M7 4h3v16H7zM14 4h3v16h-3z"/>`;

/** Clip colour by kind, so a glance at the timeline reads as structure rather
 *  than as a row of identical blocks. */
const CLIP_COLOURS = {
  video: "#2563eb",
  image: "#7c3aed",
  text: "#db2777",
  shape: "#0891b2",
  audio: "#059669",
  scene: "#ea580c",
};

const TRACK_KIND_LABELS = {
  video: "Video", text: "Text", graphics: "Graphics", audio: "Audio",
};

function formatTimecode(milliseconds) {
  const totalSeconds = Math.floor(milliseconds / 1000);
  const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, "0");
  const seconds = String(totalSeconds % 60).padStart(2, "0");
  const centiseconds = String(Math.floor((milliseconds % 1000) / 10)).padStart(2, "0");
  return `${minutes}:${seconds}.${centiseconds}`;
}

/** Always leave headroom past the last clip, so there is somewhere to drop the
 *  next one and the timeline does not collapse when empty. */
function visibleDurationMs(composition) {
  return Math.max(composition.duration_ms + 5000, 30000);
}

export async function renderStudioStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  body.innerHTML = `<div class="card muted">Loading timeline…</div>`;

  let composition;
  try {
    composition = await loadStageDocument("composition", "/composition");
    if (composition === null) return;
  } catch (loadFailure) {
    console.error("composition load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load the timeline.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }

  body.innerHTML = `
    <div class="card">
      <div class="card-head">
        <span class="card-icon">${stageIcon("studio", 21)}</span>
        <div>
          <h2>Studio</h2>
          <p>Compose the video: media, timeline, layers and rendering.</p>
        </div>
        <button class="btn" id="studio-render-button"
                title="Synthesise narration and render the video">
          ${icon(`<path d="M5 3l14 9-14 9V3z"/>`, 13, 1.8)} Render video
        </button>
        <button class="btn" id="studio-agent-button">
          ${icon(ICON.gear, 14, 1.8)} Agent &amp; instructions
        </button>
      </div>

      ${renderCutFreshness(composition)}

      ${composition.warnings.length ? `
        <div class="notice warn" style="margin-bottom:14px">
          ${composition.warnings.map(escapeHtml).join(" · ")}
        </div>` : ""}

      <div class="studio-top">
        ${renderPreview(composition)}
        ${renderProperties(composition)}
      </div>

      ${renderTimeline(composition)}
      ${renderFooterNav(stage, composition)}
    </div>`;

  wireStudioStage(stage, navigateToStage, renderAgentStage);
}

/* ---- preview ------------------------------------------------------------ */

function renderPreview(composition) {
  const contentMs = composition.duration_ms;
  const hasContent = contentMs > 0;
  const playedFraction = hasContent
    ? Math.min(1, studioViewState.playheadMs / contentMs) * 100 : 0;

  return `
    <div class="panel">
      <div class="preview-frame">
        <div class="studio-stage" id="studio-stage">
          ${renderStageFrame(composition, studioViewState.playheadMs)}
        </div>
      </div>

      <div class="transport">
        <button class="btn-icon" id="playhead-start" title="Go to start (Home)"
                aria-label="Go to start">
          ${icon(`<path d="M19 20 9 12l10-8v16zM5 19V5"/>`, 16, 1.8)}
        </button>
        <button class="btn-icon" id="play-toggle" ${hasContent ? "" : "disabled"}
                title="${hasContent ? "Play / pause (Space)" : "Nothing on the timeline to play"}"
                aria-label="${playback.isPlaying ? "Pause" : "Play"}">
          ${icon(playback.isPlaying ? PAUSE_ICON : PLAY_ICON, 16, 1.8)}
        </button>
        <button class="btn-icon" id="playhead-end" title="Go to end (End)" aria-label="Go to end">
          ${icon(`<path d="M5 4l10 8-10 8V4zM19 5v14"/>`, 16, 1.8)}
        </button>
        <span class="time" id="preview-time">${formatTimecode(studioViewState.playheadMs)}
          / ${formatTimecode(contentMs)}</span>
        <div class="scrubber" id="scrubber" title="Click or drag to seek">
          <div class="played" style="width:${playedFraction}%"></div>
          <div class="head" style="left:${playedFraction}%"></div>
        </div>
        <span class="mono muted">${composition.frame_width}&times;${composition.frame_height}
          · ${composition.frame_rate}fps</span>
      </div>
    </div>`;
}

/* ---- live frame --------------------------------------------------------- */

function activeLayersAt(composition, atMs) {
  const layers = [];
  composition.tracks.forEach((track, trackIndex) => {
    if (!track.is_visible) return;
    const clip = track.clips.find(c => atMs >= c.start_ms && atMs < c.start_ms + c.duration_ms);
    if (clip) layers.push({ track, clip, trackIndex });
  });
  return layers;
}

/** The frame at `atMs`, drawn from the clips under the playhead.
 *
 *  Tracks composite bottom-to-top, exactly as the list reads: a title card on
 *  the video track sits under a text clip on the text track. Audio draws
 *  nothing, but says what is playing, so a silent-looking frame is not
 *  mistaken for a broken one.
 */
function renderStageFrame(composition, atMs) {
  const layers = activeLayersAt(composition, atMs);
  const visual = layers.filter(layer => layer.track.kind !== "audio");
  const narration = layers.find(layer => layer.track.kind === "audio");

  const drawn = visual.map(({ track, clip, trackIndex }) => {
    const words = escapeHtml(clip.text || clip.label || "");
    if (clip.kind === "scene") {
      return `<div class="stage-layer stage-title" style="z-index:${trackIndex}">
                <span class="stage-kicker">${escapeHtml(track.label || "Scene")}</span>
                <h2>${words || "Untitled scene"}</h2>
              </div>`;
    }
    if (clip.kind === "text") {
      return `<div class="stage-layer stage-text" style="z-index:${trackIndex}">
                <p>${words || `<span class="muted">Empty text clip</span>`}</p>
              </div>`;
    }
    return `<div class="stage-layer stage-block" style="z-index:${trackIndex};
                 --clip-bg:${CLIP_COLOURS[clip.kind] ?? "#475569"}">
              <span>${escapeHtml(clip.label || clip.kind)}</span>
              <small>${escapeHtml(clip.kind)} clip · no media preview</small>
            </div>`;
  }).join("");

  const empty = visual.length ? "" : `
    <div class="stage-empty">
      ${composition.duration_ms
        ? `Nothing on screen at ${formatTimecode(atMs)}`
        : "The timeline is empty. Render a video, or add a clip with +."}
    </div>`;

  const audioBadge = narration ? `
    <span class="stage-audio-badge">
      ${icon(`<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>`, 12, 2)}
      ${escapeHtml(narration.clip.label || "Audio")}
    </span>` : "";

  return drawn + empty + audioBadge;
}

/* ---- playback ----------------------------------------------------------- */

/** Where the playhead line sits for `atMs`.
 *
 *  This used to be `calc(112px + X% * (100% - 112px) / 100%)`, which is not
 *  valid CSS: calc cannot multiply two percentages or divide by one. The browser
 *  discarded the whole rule, so the playhead never moved however the state
 *  changed. Multiplying by a plain number is valid.
 */
function playheadLeft(atMs, composition) {
  const fraction = Math.min(1, Math.max(0, atMs / visibleDurationMs(composition)));
  return `calc(${TRACK_HEAD_WIDTH_PX}px + (100% - ${TRACK_HEAD_WIDTH_PX}px) * ${fraction.toFixed(5)})`;
}

/** Update everything that shows the playhead, in place.
 *
 *  Not a re-render: re-rendering Studio refetches the composition, which is far
 *  too slow to do sixty times a second and would flash the page on every frame.
 */
function updatePlaybackDom() {
  const composition = applicationState.composition;
  if (!composition) return;
  const atMs = studioViewState.playheadMs;

  const stageElement = document.getElementById("studio-stage");
  if (stageElement) {
    // Redraw the frame only when the set of clips under the playhead changes.
    const frameKey = activeLayersAt(composition, atMs).map(l => l.clip.id).join("|")
      + (composition.duration_ms ? "" : "empty");
    if (frameKey !== playback.lastFrameKey || !stageElement.childElementCount) {
      stageElement.innerHTML = renderStageFrame(composition, atMs);
      playback.lastFrameKey = frameKey;
    }
  }

  const previewTime = document.getElementById("preview-time");
  if (previewTime) {
    previewTime.textContent =
      `${formatTimecode(atMs)} / ${formatTimecode(composition.duration_ms)}`;
  }

  const contentFraction = composition.duration_ms
    ? Math.min(1, atMs / composition.duration_ms) * 100 : 0;
  const played = document.querySelector("#scrubber .played");
  const head = document.querySelector("#scrubber .head");
  if (played) played.style.width = `${contentFraction}%`;
  if (head) head.style.left = `${contentFraction}%`;

  const playheadLine = document.getElementById("playhead");
  if (playheadLine) playheadLine.style.left = playheadLeft(atMs, composition);

  const timelineTime = document.getElementById("timeline-time");
  if (timelineTime) timelineTime.textContent = formatTimecode(atMs);

  const toggle = document.getElementById("play-toggle");
  if (toggle) {
    toggle.innerHTML = icon(playback.isPlaying ? PAUSE_ICON : PLAY_ICON, 16, 1.8);
    toggle.setAttribute("aria-label", playback.isPlaying ? "Pause" : "Play");
  }
}

function narrationClipAt(composition, atMs) {
  return activeLayersAt(composition, atMs)
    .find(layer => layer.track.kind === "audio" && layer.clip.asset_id)?.clip ?? null;
}

/** Keep the narration audio matched to the playhead.
 *
 *  `force` is for seeks: move the audio to the new position even if it is the
 *  same clip. Without it a seek inside a narration clip would keep talking from
 *  where it was.
 */
function syncNarration(force) {
  const composition = applicationState.composition;
  if (!composition) return;

  const audio = playback.audioElement ??= createNarrationElement();
  const clip = narrationClipAt(composition, studioViewState.playheadMs);

  if (!playback.isPlaying || !clip) {
    if (!audio.paused) audio.pause();
    if (!clip) playback.audioClipId = null;
    return;
  }

  const offsetSeconds = () =>
    Math.max(0, (studioViewState.playheadMs - clip.start_ms + (clip.source_in_ms ?? 0)) / 1000);

  if (playback.audioClipId !== clip.id) {
    playback.audioClipId = clip.id;
    audio.src = projectApiPath(`/narration/${encodeURIComponent(clip.asset_id)}`);
    audio.addEventListener("loadedmetadata", () => {
      audio.currentTime = offsetSeconds();
    }, { once: true });
    audio.play().catch(playFailure => reportNarrationFailure(playFailure));
    return;
  }

  if (force && audio.readyState >= 1) audio.currentTime = offsetSeconds();
  if (audio.paused && !audio.ended) {
    audio.play().catch(playFailure => reportNarrationFailure(playFailure));
  }
}

function createNarrationElement() {
  const audio = new Audio();
  audio.preload = "auto";
  audio.addEventListener("error", () => reportNarrationFailure(audio.error));
  return audio;
}

let narrationFailureReported = false;
function reportNarrationFailure(failure) {
  // An interrupted play() (the next seek arrived first) is normal, not a fault.
  if (failure?.name === "AbortError") return;
  console.error("narration playback failed", failure);
  if (narrationFailureReported) return;
  narrationFailureReported = true;
  showStageNotice("warn",
    "The narration audio could not be played, so playback continues silently. "
    + "Re-rendering the video recreates the audio files.");
}

/** While narration is audible, the audio decides where the playhead is.
 *
 *  ADR 0001 again: audio is the clock. Advancing by wall-clock time alone lets
 *  the picture drift from the voice after a stall or a slow load.
 */
function narrationClockMs(composition) {
  const audio = playback.audioElement;
  if (!audio || audio.paused || audio.ended || audio.readyState < 2) return null;
  const clip = composition.tracks.flatMap(t => t.clips)
    .find(c => c.id === playback.audioClipId);
  if (!clip) return null;
  return clip.start_ms + audio.currentTime * 1000 - (clip.source_in_ms ?? 0);
}

function tick(now) {
  if (!playback.isPlaying) return;

  const composition = applicationState.composition;
  const leftStudio = applicationState.activeStageKey !== "studio";
  const switchedProject = applicationState.selectedProject?.slug !== playback.projectSlug;
  if (!composition || leftStudio || switchedProject) {
    stopPlayback();
    return;
  }

  const elapsedMs = now - playback.lastTickAt;
  playback.lastTickAt = now;
  studioViewState.playheadMs = narrationClockMs(composition)
    ?? studioViewState.playheadMs + elapsedMs;

  if (studioViewState.playheadMs >= composition.duration_ms) {
    studioViewState.playheadMs = composition.duration_ms;
    stopPlayback();
    return;
  }

  syncNarration(false);
  updatePlaybackDom();
  playback.frameRequest = requestAnimationFrame(tick);
}

function startPlayback() {
  const composition = applicationState.composition;
  if (!composition?.duration_ms) return;

  if (studioViewState.playheadMs >= composition.duration_ms) studioViewState.playheadMs = 0;
  playback.isPlaying = true;
  playback.projectSlug = applicationState.selectedProject?.slug ?? null;
  playback.lastTickAt = performance.now();
  syncNarration(true);
  updatePlaybackDom();
  cancelAnimationFrame(playback.frameRequest);
  playback.frameRequest = requestAnimationFrame(tick);
}

function stopPlayback() {
  playback.isPlaying = false;
  cancelAnimationFrame(playback.frameRequest);
  playback.audioElement?.pause();
  updatePlaybackDom();
}

function togglePlayback() {
  if (playback.isPlaying) stopPlayback();
  else startPlayback();
}

function seekTo(targetMs) {
  const composition = applicationState.composition;
  if (!composition) return;
  studioViewState.playheadMs = Math.round(
    Math.min(Math.max(targetMs, 0), visibleDurationMs(composition)));
  playback.lastTickAt = performance.now();
  if (playback.isPlaying && studioViewState.playheadMs >= composition.duration_ms) {
    stopPlayback();
    return;
  }
  syncNarration(true);
  updatePlaybackDom();
}

/** Milliseconds for a pointer position over the lanes or the ruler.
 *
 *  Measured against a real lane rather than recomputed from CSS, so the time
 *  under the cursor is the time that lands, whatever the layout does.
 */
function msFromTimelinePointer(event) {
  const lane = document.querySelector(".track-lane");
  const composition = applicationState.composition;
  if (!lane || !composition) return studioViewState.playheadMs;
  const bounds = lane.getBoundingClientRect();
  const fraction = Math.min(1, Math.max(0, (event.clientX - bounds.left) / bounds.width));
  return fraction * visibleDurationMs(composition);
}

function msFromScrubberPointer(event, scrubber) {
  const composition = applicationState.composition;
  const bounds = scrubber.getBoundingClientRect();
  const fraction = Math.min(1, Math.max(0, (event.clientX - bounds.left) / bounds.width));
  return fraction * (composition.duration_ms || visibleDurationMs(composition));
}

/** Click to jump, drag to scrub. */
function wireScrubbing(element, msFromEvent) {
  if (!element) return;
  element.onpointerdown = event => {
    if (event.button !== 0) return;
    element.setPointerCapture(event.pointerId);
    seekTo(msFromEvent(event));
    element.onpointermove = moveEvent => seekTo(msFromEvent(moveEvent));
  };
  const endScrub = event => {
    element.onpointermove = null;
    if (element.hasPointerCapture?.(event.pointerId)) {
      element.releasePointerCapture(event.pointerId);
    }
  };
  element.onpointerup = endScrub;
  element.onpointercancel = endScrub;
}

let studioKeyboardWired = false;
/** Space plays and pauses, Home and End jump, arrows step a second (Shift: five).
 *
 *  Ignored while typing, and ignored when a button has focus: the browser
 *  already presses a focused button on Space, and handling it here as well
 *  would toggle twice and appear to do nothing.
 */
function wireStudioKeyboard() {
  if (studioKeyboardWired) return;
  studioKeyboardWired = true;

  document.addEventListener("keydown", event => {
    if (applicationState.activeStageKey !== "studio") return;
    if (!document.getElementById("studio-stage")) return;
    const target = event.target;
    if (target.closest?.("input, textarea, select, button, [contenteditable]")) return;

    const composition = applicationState.composition;
    const stepMs = event.shiftKey ? 5000 : 1000;
    const actions = {
      " ": togglePlayback,
      Home: () => seekTo(0),
      End: () => seekTo(composition?.duration_ms ?? 0),
      ArrowLeft: () => seekTo(studioViewState.playheadMs - stepMs),
      ArrowRight: () => seekTo(studioViewState.playheadMs + stepMs),
    };
    const action = actions[event.key];
    if (!action) return;
    event.preventDefault();
    action();
  });
}

/* ---- properties --------------------------------------------------------- */

function findClip(composition, clipId) {
  for (const track of composition.tracks) {
    const clip = track.clips.find(c => c.id === clipId);
    if (clip) return { clip, track };
  }
  return null;
}

function renderProperties(composition) {
  const found = findClip(composition, studioViewState.selectedClipId);

  if (!found) {
    return `
      <div class="panel">
        <div class="panel-head"><h3>Properties</h3></div>
        <p class="muted" style="font-size:12.5px;margin:0">
          Select a clip on the timeline to edit it.</p>
      </div>`;
  }

  const { clip, track } = found;
  return `
    <div class="panel">
      <div class="panel-head">
        <h3>${escapeHtml(TRACK_KIND_LABELS[track.kind] ?? "Clip")} clip</h3>
        <div class="spacer"></div>
        <button class="btn-icon danger" id="delete-clip-button"
                title="Delete clip" aria-label="Delete clip">
          ${icon(`<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>`, 15, 1.8)}
        </button>
      </div>

      <div class="prop-group">
        <label for="clip-label">Label</label>
        <div class="prop-row">
          <input id="clip-label" value="${escapeHtml(clip.label)}" maxlength="80">
        </div>
      </div>

      ${clip.kind === "text" ? `
        <div class="prop-group">
          <label for="clip-text">Text</label>
          <textarea class="prop-text" id="clip-text"
                    placeholder="On-screen text">${escapeHtml(clip.text)}</textarea>
        </div>` : ""}

      <div class="prop-group">
        <label>Timing (milliseconds)</label>
        <div class="prop-row">
          <input id="clip-start" type="number" min="0" step="100"
                 value="${clip.start_ms}" aria-label="Start">
          <input id="clip-duration" type="number" min="100" step="100"
                 value="${clip.duration_ms}" aria-label="Duration">
        </div>
        <p class="help">Start ${formatTimecode(clip.start_ms)} ·
          ends ${formatTimecode(clip.start_ms + clip.duration_ms)}</p>
      </div>

      <div class="prop-group">
        <label for="clip-kind">Kind</label>
        <div class="prop-row">
          <select id="clip-kind">
            ${["video", "image", "text", "shape", "audio", "scene"].map(kind => `
              <option value="${kind}" ${kind === clip.kind ? "selected" : ""}>
                ${kind}</option>`).join("")}
          </select>
        </div>
      </div>
    </div>`;
}

/* ---- timeline ----------------------------------------------------------- */

/** Whether this timeline still describes the plan it was built from.
 *
 *  Without this the page cannot tell: clips carry what they show, not which
 *  section produced them, so a timeline left over from an abandoned script
 *  looks exactly like a current one -- which is how a finished-looking project
 *  came to hold five sections about electrodes for a video about neural
 *  networks.
 */
function renderCutFreshness(composition) {
  const freshness = composition.freshness;
  if (!freshness?.is_stale) return "";

  const unknown = freshness.unknown_sections ?? [];
  return `
    <div class="notice bad stale-cut">
      <div>
        <b>This timeline was built from a different script.</b>
        ${unknown.length
          ? `${unknown.length} of its ${freshness.section_count} section(s) are not in the
             plan any more: ${escapeHtml(unknown.slice(0, 3).join(" · "))}${
               unknown.length > 3 ? " …" : ""}.`
          : `${freshness.missing_sections.length} planned section(s) are missing from it.`}
        Rendering leaves it alone because it counts as edited by hand.
      </div>
      <button class="btn" id="clear-timeline-button">Empty it and rebuild on the next render</button>
    </div>`;
}

function renderTimeline(composition) {
  const totalMs = visibleDurationMs(composition);
  const tickCount = 7;

  return `
    <div class="timeline">
      <div class="timeline-bar">
        <button class="btn-icon" id="add-clip-button" title="Add a clip to the selected track">
          ${icon(ICON.plus, 16)}
        </button>
        <button class="btn-icon" id="split-clip-button"
                title="Split the selected clip at the playhead">
          ${icon(`<path d="M12 3v18M6 8l-3 4 3 4M18 8l3 4-3 4"/>`, 16, 1.7)}
        </button>
        <span class="time-readout" id="timeline-time">${formatTimecode(studioViewState.playheadMs)}</span>
      </div>

      <div class="ruler" id="timeline-ruler" title="Click or drag to seek">
        ${Array.from({ length: tickCount }, (_, index) => {
          const atMs = (totalMs / (tickCount - 1)) * index;
          return `<span style="left:${(index / (tickCount - 1)) * 100}%"
                   >${formatTimecode(atMs)}</span>`;
        }).join("")}
      </div>

      <div style="position:relative">
        ${composition.tracks.map(track => renderTrack(track, composition, totalMs)).join("")}
        <div class="playhead" id="playhead"
             style="left:${playheadLeft(studioViewState.playheadMs, composition)}"></div>
      </div>
    </div>`;
}

function renderTrack(track, composition, totalMs) {
  const collidingIds = new Set(composition.audit.overlapping_clips[track.id] ?? []);

  return `
    <div class="track-row">
      <div class="track-head">
        <span class="track-label">${escapeHtml(track.label || track.kind)}</span>
        <button class="btn-icon ${track.is_visible ? "" : "off"}"
                data-toggle-visible="${track.id}"
                title="${track.is_visible ? "Hide track" : "Show track"}"
                aria-label="${track.is_visible ? "Hide track" : "Show track"}">
          ${icon(track.is_visible
            ? `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>`
            : `<path d="M17.9 17.9A10.1 10.1 0 0 1 12 20C5 20 1 12 1 12a18.5 18.5 0 0 1 5.1-5.9M23 12s-4 8-11 8"/><path d="M1 1l22 22"/>`,
            14, 1.6)}
        </button>
        <button class="btn-icon ${track.is_locked ? "" : "off"}"
                data-toggle-lock="${track.id}"
                title="${track.is_locked ? "Unlock track" : "Lock track"}"
                aria-label="${track.is_locked ? "Unlock track" : "Lock track"}">
          ${icon(track.is_locked
            ? `<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>`
            : `<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>`,
            14, 1.6)}
        </button>
      </div>

      <div class="track-lane ${track.is_locked ? "locked" : ""}" data-track="${track.id}">
        ${track.clips.map(clip => {
          const leftPercent = (clip.start_ms / totalMs) * 100;
          const widthPercent = (clip.duration_ms / totalMs) * 100;
          const label = clip.label || clip.text || clip.kind;
          // A clip's width is its share of the whole video, so on a 21-minute
          // timeline a 1.8-second title card is under two pixels wide: its
          // neighbour takes every click aimed at it, and it cannot be selected
          // at all. Marked here so the stylesheet can give it a reachable
          // width and put it above the clip beside it.
          const isNarrow = widthPercent < NARROWEST_CLICKABLE_PERCENT;
          return `
            <div class="clip ${studioViewState.selectedClipId === clip.id ? "selected" : ""}
                        ${collidingIds.has(clip.id) ? "colliding" : ""}
                        ${isNarrow ? "narrow" : ""}"
                 data-clip="${clip.id}"
                 style="left:${leftPercent}%;width:${widthPercent}%;
                        --clip-bg:${CLIP_COLOURS[clip.kind] ?? "#475569"}"
                 title="${escapeHtml(label)} · ${formatTimecode(clip.start_ms)}
                        → ${formatTimecode(clip.start_ms + clip.duration_ms)}">
              <span class="clip-label">${escapeHtml(label)}</span>
            </div>`;
        }).join("")}
      </div>
    </div>`;
}

function renderFooterNav(stage, composition) {
  const { stageDefinitions } = applicationState;
  const stageIndex = stageDefinitions.findIndex(s => s.key === stage.key);
  const previousStage = stageDefinitions[stageIndex - 1];
  const nextStage = stageDefinitions[stageIndex + 1];
  const hasClips = composition.clip_count > 0;

  return `
    <div class="footer-nav">
      ${previousStage ? `
        <button class="btn" data-goto="${previousStage.key}">
          ${icon(ICON.arrowLeft)} Back to ${escapeHtml(previousStage.title)}
        </button>` : ""}
      <span class="plan-total" style="margin-left:14px">
        ${composition.clip_count} clip(s) · ${formatTimecode(composition.duration_ms)}
      </span>
      <div class="spacer"></div>
      ${nextStage ? `
        <button class="btn btn-accent" data-goto="${nextStage.key}"
                ${hasClips ? "" : "disabled"}
                title="${hasClips ? "" : "Add at least one clip first"}">
          Next: ${escapeHtml(nextStage.title)} ${icon(ICON.arrowRight)}
        </button>` : ""}
    </div>`;
}

/* ---- persistence -------------------------------------------------------- */

/* ---- wiring ------------------------------------------------------------- */

function wireStudioStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderStudioStage(stage, navigateToStage, renderAgentStage);
  const change = applyEdit => editStageDocument({
    documentKind: "composition", apiPathSuffix: "/composition", applyEdit, rerender,
  });
  const composition = applicationState.composition;

  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });

  const clearButton = select("#clear-timeline-button");
  if (clearButton) {
    clearButton.onclick = async () => {
      if (!window.confirm(
        "Empty this timeline? Its clips are from a script that is no longer current, "
        + "and the next render will build it again.")) return;
      try {
        applicationState.composition = await requestJsonFromApi(
          projectApiPath("/composition/clear"), { method: "POST" });
        showStageNotice("ok", "Timeline emptied. Render again to rebuild it.");
      } catch (clearFailure) {
        console.error("clearing the timeline failed", clearFailure);
        showStageNotice("bad", clearFailure.message);
      }
      await rerender();
    };
  }
  select("#studio-agent-button").onclick = () => renderAgentStage(stage);

  const studioRenderButton = select("#studio-render-button");
  if (studioRenderButton) {
    studioRenderButton.onclick = () => renderFromStudio(studioRenderButton, navigateToStage);
  }

  // --- selection: clicking a clip selects it and moves the playhead there ---
  document.querySelectorAll("[data-clip]").forEach(clipElement => {
    clipElement.onclick = event => {
      event.stopPropagation();
      // Clamped into the clip. Short clips are drawn wider than their duration
      // so they can be grabbed -- a 2.5s title card on an 8-minute timeline is
      // ~5px of real time -- so the raw pointer position can map past the
      // clip's end, and the preview then showed the next clip, not this one.
      const clickedClip = composition.tracks.flatMap(t => t.clips)
        .find(c => c.id === clipElement.dataset.clip);
      // Inside the clip's real time range: land where clicked. Outside it (the
      // drawn-wider part of a short clip): land at its start, so pressing play
      // shows the whole clip rather than its last millisecond.
      const pointerMs = msFromTimelinePointer(event);
      const isWithinClip = clickedClip
        && pointerMs >= clickedClip.start_ms
        && pointerMs < clickedClip.start_ms + clickedClip.duration_ms;
      seekTo(!clickedClip || isWithinClip ? pointerMs : clickedClip.start_ms);
      if (studioViewState.selectedClipId !== clipElement.dataset.clip) {
        studioViewState.selectedClipId = clipElement.dataset.clip;
        rerender();
      }
    };
  });

  // Clicking empty lane space moves the playhead there, and clears the
  // selection rather than leaving a properties panel describing a clip you are
  // no longer looking at.
  document.querySelectorAll("[data-track]").forEach(lane => {
    lane.onclick = event => {
      seekTo(msFromTimelinePointer(event));
      if (studioViewState.selectedClipId) {
        studioViewState.selectedClipId = null;
        rerender();
      }
    };
  });

  // --- playback and seeking ---
  select("#play-toggle").onclick = togglePlayback;
  select("#playhead-start").onclick = () => seekTo(0);
  select("#playhead-end").onclick = () => seekTo(composition.duration_ms);
  const scrubber = select("#scrubber");
  wireScrubbing(scrubber, event => msFromScrubberPointer(event, scrubber));
  wireScrubbing(select("#timeline-ruler"), msFromTimelinePointer);
  wireStudioKeyboard();
  playback.lastFrameKey = "";

  // --- track controls ---
  document.querySelectorAll("[data-toggle-visible]").forEach(button => {
    button.onclick = event => {
      event.stopPropagation();
      change(comp => {
        const track = comp.tracks.find(t => t.id === button.dataset.toggleVisible);
        if (track) track.is_visible = !track.is_visible;
      });
    };
  });

  document.querySelectorAll("[data-toggle-lock]").forEach(button => {
    button.onclick = event => {
      event.stopPropagation();
      change(comp => {
        const track = comp.tracks.find(t => t.id === button.dataset.toggleLock);
        if (track) track.is_locked = !track.is_locked;
      });
    };
  });

  // --- timeline actions ---
  select("#add-clip-button").onclick = () => {
    const selected = findClip(composition, studioViewState.selectedClipId);
    // Add to the selected clip's track, or the first unlocked track.
    const targetTrack = selected?.track
      ?? composition.tracks.find(track => !track.is_locked);
    if (!targetTrack) {
      showStageNotice("warn", "Every track is locked. Unlock one to add a clip.");
      return;
    }
    change(comp => {
      const track = comp.tracks.find(t => t.id === targetTrack.id);
      const startMs = studioViewState.playheadMs;
      const kindByTrack = { video: "video", text: "text", graphics: "shape", audio: "audio" };
      track.clips.push({
        id: newItemIdentifier(),
        kind: kindByTrack[track.kind] ?? "text",
        label: "New clip", start_ms: startMs, duration_ms: 3000,
        asset_id: null, text: "", source_in_ms: 0,
      });
    });
  };

  select("#split-clip-button").onclick = () => {
    const selected = findClip(composition, studioViewState.selectedClipId);
    if (!selected) {
      showStageNotice("warn", "Select a clip to split.");
      return;
    }
    const { clip } = selected;
    const splitAt = studioViewState.playheadMs;
    // A split outside the clip, or too close to an edge to leave two grabbable
    // pieces, would produce a clip that cannot be selected or deleted.
    if (splitAt <= clip.start_ms + 100 || splitAt >= clip.start_ms + clip.duration_ms - 100) {
      showStageNotice("warn", "Move the playhead inside the clip to split it.");
      return;
    }
    change(comp => {
      const track = comp.tracks.find(t => t.clips.some(c => c.id === clip.id));
      const original = track.clips.find(c => c.id === clip.id);
      const secondDuration = original.start_ms + original.duration_ms - splitAt;
      original.duration_ms = splitAt - original.start_ms;
      track.clips.push({
        ...original,
        id: newItemIdentifier(),
        start_ms: splitAt,
        duration_ms: secondDuration,
      });
    });
  };

  wireProperties(change);
}

function wireProperties(change) {
  const clipId = studioViewState.selectedClipId;
  if (!clipId) return;

  const applyToSelectedClip = mutateClip => change(comp => {
    for (const track of comp.tracks) {
      const clip = track.clips.find(c => c.id === clipId);
      if (clip) { mutateClip(clip); return; }
    }
  });

  const label = select("#clip-label");
  if (label) label.onchange = () => applyToSelectedClip(clip => { clip.label = label.value; });

  const text = select("#clip-text");
  if (text) text.onchange = () => applyToSelectedClip(clip => { clip.text = text.value; });

  const start = select("#clip-start");
  if (start) start.onchange = () =>
    applyToSelectedClip(clip => { clip.start_ms = Number(start.value) || 0; });

  const duration = select("#clip-duration");
  if (duration) duration.onchange = () =>
    applyToSelectedClip(clip => { clip.duration_ms = Number(duration.value) || 100; });

  const kind = select("#clip-kind");
  if (kind) kind.onchange = () => applyToSelectedClip(clip => { clip.kind = kind.value; });

  const deleteButton = select("#delete-clip-button");
  if (deleteButton) deleteButton.onclick = () => {
    studioViewState.selectedClipId = null;
    change(comp => {
      for (const track of comp.tracks) {
        track.clips = track.clips.filter(c => c.id !== clipId);
      }
    });
  };
}


/** Render, then send the user to Reviewing where the player is.
 *
 *  Rendering from Studio but watching in Reviewing would otherwise leave someone
 *  staring at a placeholder wondering whether it worked.
 */
async function renderFromStudio(button, navigateToStage) {
  const originalLabel = button.textContent;
  button.disabled = true;
  button.textContent = "Rendering...";

  let voiceProvider = "";
  try {
    voiceProvider = (await requestJsonFromApi("/api/voices")).recommended;
  } catch (voicesFailure) {
    console.error("could not list voices", voicesFailure);
  }

  showStageNotice("warn",
    `Rendering with the ${voiceProvider || "default"} voice. One synthesis call `
    + "per section, then ffmpeg - this takes a few minutes.");

  try {
    const result = await requestJsonFromApi(projectApiPath("/render"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ voice_provider: voiceProvider, voice: "" }),
    });
    showStageNotice("ok",
      `Rendered ${result.section_count} section(s), ${
        Math.round(result.duration_ms / 1000)}s. Opening Reviewing to watch it.`);
    navigateToStage("reviewing");
  } catch (renderFailure) {
    console.error("render failed", renderFailure);
    button.disabled = false;
    button.textContent = originalLabel;
    showStageNotice("bad", `Render failed - ${renderFailure.message}`);
  }
}
