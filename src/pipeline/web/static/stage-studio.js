/**
 * Studio stage — preview, multi-track timeline, and clip properties.
 *
 * The composition is the artifact: tracks bottom-to-top, clips placed on an
 * absolute millisecond timeline. Everything here reads and writes that one
 * document, so a clip cannot exist on screen without existing in the file.
 *
 * Rendering does not exist yet, and the preview says so rather than showing a
 * plausible-looking frame.
 */

import { editStageDocument, loadStageDocument, newItemIdentifier }
  from "/static/document-editing.js";
import {
  ICON, applicationState, escapeHtml, icon, projectApiPath, select,
  showStageNotice, stageIcon,
} from "/static/ui-kit.js";

/** View-only state. The playhead and selection are not part of the saved
 *  composition — reopening the stage should not restore a caret position. */
const studioViewState = {
  selectedClipId: null,
  playheadMs: 0,
};

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
        <button class="btn" id="studio-agent-button">
          ${icon(ICON.gear, 14, 1.8)} Agent &amp; instructions
        </button>
      </div>

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
  const totalMs = visibleDurationMs(composition);
  const playedFraction = totalMs ? (studioViewState.playheadMs / totalMs) * 100 : 0;

  return `
    <div class="panel">
      <div class="preview-frame">
        <div class="placeholder">
          ${icon(`<rect x="2" y="5" width="14" height="14" rx="2"/><path d="m22 8-6 4 6 4V8z"/>`,
                 40, 1.3)}
          <p>Rendering is not built yet.<br>
             The timeline below is real and saved.</p>
        </div>
      </div>

      <div class="transport">
        <button class="btn-icon" id="playhead-start" title="Go to start" aria-label="Go to start">
          ${icon(`<path d="M19 20 9 12l10-8v16zM5 19V5"/>`, 16, 1.8)}
        </button>
        <button class="btn-icon" disabled title="Playback needs a render"
                aria-label="Play (unavailable)">
          ${icon(`<path d="M5 3l14 9-14 9V3z"/>`, 16, 1.8)}
        </button>
        <button class="btn-icon" id="playhead-end" title="Go to end" aria-label="Go to end">
          ${icon(`<path d="M5 4l10 8-10 8V4zM19 5v14"/>`, 16, 1.8)}
        </button>
        <span class="time">${formatTimecode(studioViewState.playheadMs)}
          / ${formatTimecode(composition.duration_ms)}</span>
        <div class="scrubber" id="scrubber">
          <div class="played" style="width:${playedFraction}%"></div>
          <div class="head" style="left:${playedFraction}%"></div>
        </div>
        <span class="mono muted">${composition.frame_width}&times;${composition.frame_height}
          · ${composition.frame_rate}fps</span>
      </div>
    </div>`;
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
        <span class="time-readout">${formatTimecode(studioViewState.playheadMs)}</span>
      </div>

      <div class="ruler">
        ${Array.from({ length: tickCount }, (_, index) => {
          const atMs = (totalMs / (tickCount - 1)) * index;
          return `<span style="left:${(index / (tickCount - 1)) * 100}%"
                   >${formatTimecode(atMs)}</span>`;
        }).join("")}
      </div>

      <div style="position:relative">
        ${composition.tracks.map(track => renderTrack(track, composition, totalMs)).join("")}
        <div class="playhead" id="playhead"
             style="left:calc(112px + ${(studioViewState.playheadMs / totalMs) * 100}%
                    * (100% - 112px) / 100%)"></div>
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
          return `
            <div class="clip ${studioViewState.selectedClipId === clip.id ? "selected" : ""}
                        ${collidingIds.has(clip.id) ? "colliding" : ""}"
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
  const totalMs = visibleDurationMs(composition);

  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });
  select("#studio-agent-button").onclick = () => renderAgentStage(stage);

  // --- selection ---
  document.querySelectorAll("[data-clip]").forEach(clipElement => {
    clipElement.onclick = event => {
      event.stopPropagation();
      studioViewState.selectedClipId = clipElement.dataset.clip;
      rerender();
    };
  });

  // Clicking empty lane space clears the selection rather than leaving a stale
  // properties panel describing a clip you are no longer looking at.
  document.querySelectorAll("[data-track]").forEach(lane => {
    lane.onclick = () => {
      studioViewState.selectedClipId = null;
      rerender();
    };
  });

  // --- playhead ---
  const scrubber = select("#scrubber");
  if (scrubber) {
    scrubber.onclick = event => {
      const bounds = scrubber.getBoundingClientRect();
      const fraction = Math.min(1, Math.max(0, (event.clientX - bounds.left) / bounds.width));
      studioViewState.playheadMs = Math.round(fraction * totalMs);
      rerender();
    };
  }
  select("#playhead-start").onclick = () => {
    studioViewState.playheadMs = 0;
    rerender();
  };
  select("#playhead-end").onclick = () => {
    studioViewState.playheadMs = composition.duration_ms;
    rerender();
  };

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
