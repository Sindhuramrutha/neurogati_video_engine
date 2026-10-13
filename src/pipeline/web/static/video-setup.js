/**
 * Video setup — who the video is for, the voice, the music and where it will be
 * watched (`video_setup.py`). Mounted in the Scene Plan's setup, and its voice and
 * music on the Render page: one panel, saved as it changes, drawn and wired here.
 *
 * Every voice and every bed has a sample to hear before choosing; a bed can also be
 * heard under the chosen voice at the chosen intensity, mixed as the render mixes it.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import { escapeHtml, icon, projectApiPath, showStageNotice } from "/static/ui-kit.js";

const PARTS = ["learners", "voice", "music", "platforms"];

const ICONS = {
  learners: `<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/>
             <path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>`,
  voice: `<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>`,
  music: `<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>`,
  platforms: `<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>`,
  play: `<path d="M7 5l12 7-12 7z"/>`,
};

const PACE_LABELS = { slower: "Slower", normal: "Normal", faster: "Faster" };
const INTENSITY_LABELS = { whisper: "Whisper", soft: "Soft", present: "Present" };

const box = (key, title, body, note = "") => `
  <section class="setup-box vs-box vs-${key}">
    <div class="setup-box-head">
      <span class="setup-icon">${icon(ICONS[key], 16, 2)}</span>
      <b>${title}</b>
      ${note ? `<span class="muted setup-note">${note}</span>` : ""}
    </div>
    ${body}
  </section>`;

const playButton = (url, label) => `
  <button type="button" class="vs-play" data-vs-play="${escapeHtml(url)}"
          title="${escapeHtml(label)}" aria-label="${escapeHtml(label)}">${icon(ICONS.play, 14, 2)}</button>`;

function renderLearners({ setup, catalog }) {
  return box("learners", "Learners", `
    <p class="muted setup-hint">Choose everyone it is for; the script serves them all.</p>
    <div class="vs-chips">
      ${catalog.learners.map(learner => `
        <label class="vs-chip ${setup.learners.includes(learner.key) ? "on" : ""}"
               title="${escapeHtml(learner.guidance)}">
          <input type="checkbox" data-vs-learner="${escapeHtml(learner.key)}"
                 ${setup.learners.includes(learner.key) ? "checked" : ""}>
          ${escapeHtml(learner.label)}
        </label>`).join("")}
    </div>`);
}

function renderVoice({ setup, catalog }) {
  const groups = {};
  for (const voice of catalog.voices) (groups[voice.accent] ??= []).push(voice);
  return box("voice", "Voice", `
    <p class="muted setup-hint">Press ▶ to hear each one. Scenes and the render use the one chosen.</p>
    <div class="vs-voices">
      <label class="vs-option ${setup.voice ? "" : "on"}">
        <input type="radio" name="vs-voice" value="" ${setup.voice ? "" : "checked"}>
        <span>The language's default</span>
      </label>
      ${Object.entries(groups).map(([accent, voices]) => `
        <div class="vs-group"><span class="vs-group-name">${escapeHtml(accent)}</span>
          ${voices.map(voice => `
            <label class="vs-option ${setup.voice === voice.key ? "on" : ""}">
              <input type="radio" name="vs-voice" value="${escapeHtml(voice.key)}"
                     ${setup.voice === voice.key ? "checked" : ""}>
              <span>${escapeHtml(voice.name)} <span class="muted">· ${escapeHtml(voice.gender)}</span></span>
              ${playButton(`/api/voice-samples/${encodeURIComponent(voice.key)}?pace=${setup.pace}`,
                `Hear ${voice.name}`)}
            </label>`).join("")}
        </div>`).join("")}
    </div>
    <div class="vs-segment" role="radiogroup" aria-label="Pace">
      <span class="vs-segment-name">Pace</span>
      ${catalog.paces.map(pace => `
        <label class="${setup.pace === pace ? "on" : ""}">
          <input type="radio" name="vs-pace" value="${pace}" ${setup.pace === pace ? "checked" : ""}>
          ${PACE_LABELS[pace] ?? pace}</label>`).join("")}
    </div>
    ${renderSounds(setup)}`);
}

/** Names the voice says wrong, and how to spell them so it says them right. */
function renderSounds(setup) {
  const rows = [...Object.entries(setup.sounds ?? {}), ...(extraRows ? [["", ""]] : [])];
  return `
    <div class="vs-sounds">
      <span class="vs-group-name">Pronunciations</span>
      <p class="muted setup-hint">A name said wrong? Write how to say it; ▶ plays it in this
        voice. Subtitles keep the real spelling.</p>
      ${rows.map(([word, say]) => `
        <div class="vs-sound-row">
          <input data-vs-sound-word value="${escapeHtml(word)}" placeholder="Loewi"
                 aria-label="Written as">
          <span class="muted">say</span>
          <input data-vs-sound-say value="${escapeHtml(say)}" placeholder="Lervee"
                 aria-label="Said as">
          ${word ? playButton(projectApiPath(`/say?text=${encodeURIComponent(word)}`),
            `Hear ${word}`) : ""}
        </div>`).join("")}
      <div class="vs-actions">
        <button type="button" class="btn" data-vs-add-sound>+ Add a name</button>
        <button type="button" class="btn" data-vs-suggest>Suggest from the script
          <span class="fact warn">AI · 1 call</span></button>
      </div>
    </div>`;
}

let extraRows = false;

function musicSampleUrl(setup, music, underVoice) {
  const query = new URLSearchParams({ music, intensity: setup.intensity });
  if (underVoice) {
    query.set("voice", setup.voice || "en-IN-NeerjaNeural");
    query.set("pace", setup.pace);
  }
  return projectApiPath(`/music-sample?${query}`);
}

function renderMusic({ setup, catalog }) {
  const chosen = setup.music !== "none";
  return box("music", "Music", `
    <p class="muted setup-hint">Under the voice, quieter still while it speaks. ▶ plays the music
      alone; the button below plays it under the voice.</p>
    <div class="vs-voices">
      <label class="vs-option ${chosen ? "" : "on"}">
        <input type="radio" name="vs-music" value="none" ${chosen ? "" : "checked"}>
        <span>No music</span>
      </label>
      ${catalog.music.map(track => `
        <label class="vs-option ${setup.music === track.key ? "on" : ""}">
          <input type="radio" name="vs-music" value="${escapeHtml(track.key)}"
                 ${setup.music === track.key ? "checked" : ""}>
          <span>${escapeHtml(track.label)}</span>
          ${playButton(musicSampleUrl(setup, track.key, false), `Hear ${track.label}`)}
        </label>`).join("")}
    </div>
    <div class="vs-segment" role="radiogroup" aria-label="Intensity">
      <span class="vs-segment-name">Intensity</span>
      ${catalog.intensities.map(level => `
        <label class="${setup.intensity === level ? "on" : ""}">
          <input type="radio" name="vs-intensity" value="${level}"
                 ${setup.intensity === level ? "checked" : ""}>
          ${INTENSITY_LABELS[level] ?? level}</label>`).join("")}
    </div>
    <div class="vs-actions">
      <button type="button" class="btn" ${chosen ? "" : "disabled"}
              data-vs-play="${chosen ? escapeHtml(musicSampleUrl(setup, setup.music, true)) : ""}">
        ${icon(ICONS.play, 14, 2)} Hear it under the voice</button>
      <label class="btn vs-upload">Upload a track…
        <input type="file" accept=".mp3,.wav,.m4a,.ogg,.flac" data-vs-upload hidden></label>
    </div>
    <p class="muted setup-hint">Upload only music you have the rights to use.</p>`);
}

function renderPlatforms({ setup, catalog }) {
  return box("platforms", "Where it will be watched", `
    <div class="vs-list">
      ${catalog.platforms.map(platform => `
        <label class="vs-option ${setup.platforms.includes(platform.key) ? "on" : ""}">
          <input type="checkbox" data-vs-platform="${escapeHtml(platform.key)}"
                 ${setup.platforms.includes(platform.key) ? "checked" : ""}>
          <span>${escapeHtml(platform.label)}</span>
        </label>`).join("")}
    </div>`);
}

const RENDERERS = {
  learners: renderLearners, voice: renderVoice, music: renderMusic, platforms: renderPlatforms,
};

/** Draw the setup into `container` and keep it there: it redraws itself after
 *  every change, so the page around it is never redrawn for a setting. */
export async function mountVideoSetup(container, { parts = PARTS } = {}) {
  if (!container) return;
  let data;
  try {
    data = await requestJsonFromApi(projectApiPath("/video-setup"));
  } catch (failure) {
    container.innerHTML = `<p class="muted">Video setup could not be loaded — ${
      escapeHtml(failure.message)}</p>`;
    return;
  }
  const draw = () => {
    container.innerHTML = parts.map(part => RENDERERS[part](data)).join("")
      + `<audio class="vs-player" preload="none"></audio>`;
    wire();
  };
  const save = async changes => {
    try {
      data = await requestJsonFromApi(projectApiPath("/video-setup"), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(changes),
      });
      draw();
      showStageNotice("ok", "Video setup saved.");
    } catch (failure) {
      showStageNotice("bad", `Could not save the video setup — ${failure.message}`);
      draw();
    }
  };
  const wire = () => {
    const player = container.querySelector(".vs-player");
    container.querySelectorAll("[data-vs-play]").forEach(button => {
      button.onclick = event => {
        event.preventDefault();
        const url = button.dataset.vsPlay;
        if (!url) return;
        if (player.dataset.playing === url && !player.paused) {
          player.pause();
          return;
        }
        container.querySelectorAll(".vs-play.busy").forEach(b => b.classList.remove("busy"));
        button.classList.add("busy");
        player.src = url;
        player.dataset.playing = url;
        player.play().catch(failure => showStageNotice("bad",
          `The sample could not be played — ${failure.message}`));
      };
    });
    if (player) {
      player.onplaying = () => container.querySelectorAll(".vs-play.busy")
        .forEach(b => b.classList.remove("busy"));
      player.onerror = () => {
        container.querySelectorAll(".vs-play.busy").forEach(b => b.classList.remove("busy"));
        showStageNotice("bad", "The sample could not be made. A voice sample needs the "
          + "internet the first time; music samples need ffmpeg.");
      };
    }
    container.querySelectorAll("[data-vs-learner]").forEach(box => {
      box.onchange = () => save({ learners: [...container.querySelectorAll(
        "[data-vs-learner]:checked")].map(b => b.dataset.vsLearner) });
    });
    container.querySelectorAll("[data-vs-platform]").forEach(box => {
      box.onchange = () => save({ platforms: [...container.querySelectorAll(
        "[data-vs-platform]:checked")].map(b => b.dataset.vsPlatform) });
    });
    for (const [name, key] of [["vs-voice", "voice"], ["vs-pace", "pace"],
      ["vs-music", "music"], ["vs-intensity", "intensity"]]) {
      container.querySelectorAll(`[name=${name}]`).forEach(radio => {
        radio.onchange = () => save({ [key]: radio.value });
      });
    }
    const saveSounds = () => {
      const sounds = {};
      container.querySelectorAll(".vs-sound-row").forEach(row => {
        const word = row.querySelector("[data-vs-sound-word]").value.trim();
        const say = row.querySelector("[data-vs-sound-say]").value.trim();
        if (word && say) sounds[word] = say;
      });
      extraRows = false;
      save({ sounds });
    };
    container.querySelectorAll("[data-vs-sound-word], [data-vs-sound-say]").forEach(input => {
      input.onchange = saveSounds;
    });
    const add = container.querySelector("[data-vs-add-sound]");
    if (add) add.onclick = () => { extraRows = true; draw(); };
    const suggest = container.querySelector("[data-vs-suggest]");
    if (suggest) suggest.onclick = async () => {
      suggest.disabled = true;
      suggest.textContent = "Reading the script…";
      try {
        data = await requestJsonFromApi(projectApiPath("/video-setup/suggest-pronunciations"),
          { method: "POST" });
        showStageNotice("ok", "Pronunciations suggested. Play each one to check it.");
      } catch (failure) {
        showStageNotice("bad", `Could not suggest pronunciations — ${failure.message}`);
      }
      draw();
    };
    const upload = container.querySelector("[data-vs-upload]");
    if (upload) upload.onchange = async () => {
      const file = upload.files?.[0];
      if (!file) return;
      const form = new FormData();
      form.append("file", file);
      try {
        data = await requestJsonFromApi(projectApiPath("/music"), { method: "POST", body: form });
        draw();
        showStageNotice("ok", `${file.name} added to this project's music.`);
      } catch (failure) {
        showStageNotice("bad", `Could not add the track — ${failure.message}`);
      }
    };
  };
  draw();
}
