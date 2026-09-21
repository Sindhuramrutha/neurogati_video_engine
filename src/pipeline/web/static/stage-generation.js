/**
 * Generation — what each scene shows, what it says on screen, and how it moves.
 *
 * One card per scene, in the order they are spoken, each showing the picture
 * that will actually be on screen and the few words that will be on it. That is
 * the point of the page: the brief was a sentence nobody could check, and a
 * thumbnail with its headline is a claim you can see.
 *
 * The narration is deliberately not shown as on-screen text anywhere here. It
 * is what the scene *says*; the headline and labels are what it *shows*, and the
 * whole stage exists to keep those two apart.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import {
  ICON, applicationState, escapeHtml, icon, projectApiPath, refreshProjectSummary, select,
  showStageNotice, stageIcon,
} from "/static/ui-kit.js";

const generationViewState = {
  filter: "all",   // all | needs-building | from-source | diagrams | generated | words
};

const FILTERS = [
  ["all", "Every scene"],
  ["needs-building", "Not made yet"],
  ["slides", "Slides"],
  ["from-source", "From the source"],
  ["diagrams", "Diagrams"],
  ["generated", "Drawn"],
  ["words", "Words only"],
];

const KIND_LABELS = {
  slide: "The deck's slide",
  source_picture: "From the source",
  chart: "Chart",
  diagram: "Diagram",
  generated_image: "Drawn",
  text: "Words only",
};

/** The shapes a scene can be drawn as, in the words a person would use. */
const DIAGRAM_LABELS = {
  flow: "a sequence",
  compare: "a comparison",
  stack: "layers",
  cycle: "a loop",
  tree: "a hierarchy",
  graph: "a network",
  plot: "a curve",
  bars: "bars",
  timeline: "a timeline",
  table: "a table",
  counter: "a counting number",
  formula: "a formula",
  figure: "the source's own figure",
  morph: "one thing becoming another",
  code: "code",
};

const MOTION_LABELS = {
  hold: "Still",
  push_in: "Push in",
  pull_back: "Pull back",
  pan_right: "Pan right",
  pan_left: "Pan left",
};

const matches = visual => ({
  all: true,
  "needs-building": !visual.is_built || visual.is_stale,
  slides: visual.kind === "slide",
  "from-source": visual.kind === "source_picture",
  diagrams: visual.kind === "diagram",
  generated: visual.kind === "generated_image" || visual.kind === "chart",
  words: visual.kind === "text",
}[generationViewState.filter]);

/**
 * Assets live in three places, and a thumbnail has to come from the same file
 * the video will draw.
 *
 * `generation/` is what this stage made. `assets/prepared/` is a source figure
 * with its slide background trimmed off, which is what the renderer uses --
 * pointing a thumbnail at the untrimmed original instead showed a picture the
 * render would not use, and pointing it at the extraction folder 404s.
 */
const pictureUrl = assetPath => {
  const name = encodeURIComponent(assetPath.split("/").pop());
  if (assetPath.startsWith("generation/slides/")) {
    return projectApiPath(`/visuals/slides/${name}`);
  }
  if (assetPath.startsWith("generation/")) {
    return projectApiPath(`/visuals/assets/${name}`);
  }
  if (assetPath.startsWith("assets/prepared/")) {
    return projectApiPath(`/assets/prepared/${name}`);
  }
  return projectApiPath(`/extraction/assets/${name}`);
};

export async function renderGenerationStage(stage, navigateToStage, renderAgentStage) {
  const body = select("#stage-body");
  body.innerHTML = `<div class="card muted">Loading the shots…</div>`;

  let visuals;
  try {
    visuals = await requestJsonFromApi(projectApiPath("/visuals"));
  } catch (loadFailure) {
    console.error("visuals load failed", loadFailure);
    body.innerHTML = `<div class="card">
      <b>Could not load what each scene shows.</b>
      <p class="muted" style="margin:6px 0 0">${escapeHtml(loadFailure.message)}</p>
    </div>`;
    return;
  }
  applicationState.sceneVisuals = visuals;

  // What can be animated here is a property of the machine, not of the project,
  // so it is loaded separately and a failure to read it costs the panel and not
  // the page.
  let renderers = null;
  try {
    renderers = await requestJsonFromApi("/api/scene-renderers");
  } catch (rendererFailure) {
    console.error("scene renderers load failed", rendererFailure);
  }

  const shown = visuals.visuals.filter(matches);

  body.innerHTML = `
    <div class="card">
      <div class="card-head">
        <span class="card-icon">${stageIcon("generation", 21)}</span>
        <div>
          <h2>Generation</h2>
          <p>Make what each scene shows, and decide how the camera moves over it.</p>
        </div>
        <button class="btn" id="generation-agent-button">
          ${icon(ICON.gear, 14, 1.8)} Agent &amp; instructions
        </button>
      </div>

      ${renderRunBar(visuals)}

      ${renderRendererPanel(renderers)}

      ${visuals.warnings.length ? `
        <div class="notice warn" style="margin-bottom:12px">
          ${visuals.warnings.map(escapeHtml).join(" · ")}
        </div>` : ""}
      ${visuals.notes.length ? `
        <p class="muted edit-hint" style="margin-bottom:12px">
          ${visuals.notes.map(escapeHtml).join(" · ")}</p>` : ""}

      ${visuals.is_empty
        ? `<div class="empty">
             <h3>No scenes yet</h3>
             <p>Write the narration as scenes on Script &amp; Staging, then decide
                what each one shows.</p>
             <button class="btn btn-accent" data-goto="script-staging">
               ${icon(ICON.arrowLeft)} Go to Script &amp; Staging</button>
           </div>`
        : `${renderFilters(visuals)}
           <div class="shot-grid">${shown.map(renderShot).join("")}</div>
           ${shown.length ? "" : `<p class="muted edit-hint">Nothing matches this filter.</p>`}`}

      ${renderFooterNav(stage)}
    </div>`;

  wireGenerationStage(stage, navigateToStage, renderAgentStage);
}

function renderRunBar(visuals) {
  const audit = visuals.audit;
  const missing = visuals.visuals.filter(v => !v.is_built || v.is_stale).length;
  const tone = visuals.is_empty ? "blocked" : missing ? "stale" : "ready";

  return `
    <div class="run-bar ${tone}">
      <span class="run-icon">${icon(missing ? ICON.alert : ICON.check, 17, 2.2)}</span>
      <span class="run-text">
        <b>${visuals.is_empty
          ? "Nothing planned yet"
          : missing
            ? `${missing} of ${audit.scene_count} scene(s) still need a picture`
            : `All ${audit.scene_count} scenes have something to show`}</b>
        <span>${visuals.is_empty
          ? "Decide what every scene shows. This calls no model."
          : [
              audit.slides ? `${audit.slides} from the deck's own slides` : "",
              audit.from_source ? `${audit.from_source} from the source` : "",
              audit.charts ? `${audit.charts} chart(s)` : "",
              audit.diagrams ? `${audit.diagrams} diagram(s), ${audit.animated ?? 0} animated` : "",
              audit.generated ? `${audit.generated} drawn` : "",
              audit.words_only ? `${audit.words_only} words only` : "",
            ].filter(Boolean).join(" · ")}</span>
      </span>
      <span class="plan-actions">
        <button class="btn" id="plan-visuals-button">
          ${visuals.is_empty ? "Decide what to show" : "Decide again"}
        </button>
        <button class="btn btn-accent" id="build-visuals-button"
                ${visuals.is_empty ? "disabled" : ""}>
          ${missing ? "Make what is missing" : "Make again"}
        </button>
      </span>
    </div>`;
}

/**
 * What can draw a scene on this machine, and what is missing to do more.
 *
 * Shown rather than hidden. A project whose diagrams come out as stills because
 * nothing is installed should say so, with the one command that changes it --
 * and a renderer that is installed but fails here should say *that*, because the
 * two look identical in the finished video.
 */
function renderRendererPanel(renderers) {
  if (!renderers) return "";

  const drawable = renderers.drawable_kinds ?? [];
  const total = (renderers.kinds ?? []).length;
  const animators = (renderers.renderers ?? []).filter(
    renderer => (renderer.capabilities ?? []).includes("animated_diagram"));

  return `
    <details class="renderer-panel ${drawable.length ? "" : "flat"}">
      <summary>
        <span class="renderer-state">${drawable.length
          ? `${drawable.length} of ${total} scene kinds can be animated`
          : "Nothing here can animate a scene"}</span>
        <span class="muted">${drawable.length
          ? `drawn by ${escapeHtml([...new Set((renderers.kinds ?? [])
              .map(kind => kind.drawn_by).filter(Boolean))].join(", "))}`
          : "diagrams will be drawn as stills and held"}</span>
      </summary>

      <div class="renderer-list">
        ${animators.map(renderer => `
          <div class="renderer-row ${renderer.is_available ? "ok" : "off"}">
            <div class="renderer-head">
              <b>${escapeHtml(renderer.label)}</b>
              <span class="fact ${renderer.is_available ? "ok"
                : renderer.is_installed ? "bad" : "muted"}">${
                renderer.is_available ? "working"
                  : renderer.is_installed ? "installed, not working" : "not installed"}</span>
              <div class="spacer"></div>
              ${renderer.is_installed ? `
                <button class="btn" data-verify="${escapeHtml(renderer.key)}">
                  Verify ${escapeHtml(renderer.kinds.length)} kinds</button>` : ""}
            </div>
            <p class="muted">${escapeHtml(renderer.summary)}</p>
            ${renderer.is_installed ? "" : `
              <p class="renderer-install">Install with
                <code>${escapeHtml(renderer.install_command)}</code></p>`}
            ${renderer.self_test.checked && renderer.self_test.detail ? `
              <p class="renderer-detail">${escapeHtml(renderer.self_test.detail)}</p>` : ""}
            ${renderer.is_installed ? `
              <div class="renderer-kinds">
                ${renderer.kinds.map(kind => {
                  const proved = renderer.self_test.kinds?.[kind];
                  const state = !proved ? "unproved" : proved.ok ? "ok" : "bad";
                  const why = !proved ? "not verified yet"
                    : proved.ok ? "verified" : proved.detail;
                  return `<span class="kind ${state}" title="${escapeHtml(why)}"
                    >${escapeHtml(kind)}</span>`;
                }).join("")}
              </div>` : ""}
          </div>`).join("")}
      </div>

      <div class="renderer-kinds-all">
        ${(renderers.kinds ?? []).map(kind => `
          <span class="kind ${kind.is_drawable ? "ok" : "off"}"
                title="${escapeHtml(kind.describes)}${kind.drawn_by
                  ? ` — drawn by ${kind.drawn_by}` : " — nothing here draws this"}"
            >${escapeHtml(kind.kind)}</span>`).join("")}
      </div>
    </details>`;
}

function renderFilters(visuals) {
  const counts = {
    all: visuals.visuals.length,
    "needs-building": visuals.visuals.filter(v => !v.is_built || v.is_stale).length,
    slides: visuals.audit.slides ?? 0,
    "from-source": visuals.audit.from_source,
    diagrams: visuals.audit.diagrams ?? 0,
    generated: visuals.audit.generated + visuals.audit.charts,
    words: visuals.audit.words_only,
  };
  return `
    <div class="seg asset-filters">
      ${FILTERS.map(([key, label]) => `
        <button class="${generationViewState.filter === key ? "on" : ""}" data-filter="${key}">
          ${escapeHtml(label)} <span class="mono">${counts[key] ?? 0}</span>
        </button>`).join("")}
    </div>`;
}

function renderShot(visual) {
  return `
    <div class="shot-card ${visual.is_stale ? "is-stale" : ""} ${visual.is_built ? "" : "unbuilt"}"
         data-visual="${escapeHtml(visual.id)}">
      <div class="shot-head">
        <span class="outline-num">${visual.scene_number}</span>
        <span class="fact ${visual.kind === "source_picture" ? "ok" : "muted"}"
          >${escapeHtml(KIND_LABELS[visual.kind] ?? visual.kind)}</span>
        <div class="spacer"></div>
        ${visual.is_stale ? `<span class="fact warn">scene rewritten</span>` : ""}
        ${visual.is_built ? "" : `<span class="fact bad">not made</span>`}
      </div>
      <span class="shot-section">${escapeHtml(visual.section_title)}</span>

      <div class="shot-frame">
        ${visual.asset_path
          ? `<img alt="" loading="lazy" src="${pictureUrl(visual.asset_path)}">`
          : `<span class="shot-words">${escapeHtml(
               visual.headline || "Nothing composed yet")}</span>`}
        ${visual.clip_path
          ? `<span class="shot-animated">animated by ${escapeHtml(visual.drawn_by)}</span>`
          : ""}
        <span class="shot-motion">${escapeHtml(MOTION_LABELS[visual.motion] ?? visual.motion)}</span>
      </div>

      <div class="shot-reads">
        <b class="shot-headline">${escapeHtml(visual.headline || "No headline yet")}</b>
        ${(visual.points ?? []).length
          ? `<ul class="shot-points">${visual.points.map(
               point => `<li>${escapeHtml(point)}</li>`).join("")}</ul>`
          : `<span class="muted">${visual.kind === "slide"
               ? `Slide ${visual.slide_number} of the deck, shown as its author made it.`
               : "No labels — the picture carries this one."}</span>`}
        ${visual.diagram
          ? `<span class="shot-diagram">Drawn as ${escapeHtml(
               DIAGRAM_LABELS[visual.diagram.kind] ?? visual.diagram.kind)}:
               ${escapeHtml((visual.diagram.nodes ?? []).join(" → "))}</span>`
          : ""}
      </div>

      <details class="shot-brief-detail">
        <summary>What the script asked for</summary>
        <p>${escapeHtml(visual.brief || "Nothing was written for this scene.")}</p>
      </details>
      ${visual.note ? `<span class="shot-note">${escapeHtml(visual.note)}</span>` : ""}

      <div class="shot-actions">
        <select data-kind-for="${escapeHtml(visual.id)}" aria-label="What this scene shows">
          ${Object.entries(KIND_LABELS).map(([key, label]) => `
            <option value="${key}" ${visual.kind === key ? "selected" : ""}
              >${escapeHtml(label)}</option>`).join("")}
        </select>
        <select data-motion-for="${escapeHtml(visual.id)}" aria-label="How the camera moves">
          ${Object.entries(MOTION_LABELS).map(([key, label]) => `
            <option value="${key}" ${visual.motion === key ? "selected" : ""}
              >${escapeHtml(label)}</option>`).join("")}
        </select>
      </div>

      ${visual.prompt ? `
        <details class="shot-prompt">
          <summary>What was asked for</summary>
          <pre>${escapeHtml(visual.prompt)}</pre>
        </details>` : ""}
    </div>`;
}

function renderFooterNav(stage) {
  const { stageDefinitions } = applicationState;
  const index = stageDefinitions.findIndex(s => s.key === stage.key);
  const previous = stageDefinitions[index - 1];
  const next = stageDefinitions[index + 1];
  return `
    <div class="footer-nav">
      ${previous ? `<button class="btn" data-goto="${previous.key}">
        ${icon(ICON.arrowLeft)} Back to ${escapeHtml(previous.title)}</button>` : ""}
      <div class="spacer"></div>
      ${next ? `<button class="btn btn-accent" data-goto="${next.key}">
        Next: ${escapeHtml(next.title)} ${icon(ICON.arrowRight)}</button>` : ""}
    </div>`;
}

function wireGenerationStage(stage, navigateToStage, renderAgentStage) {
  const rerender = () => renderGenerationStage(stage, navigateToStage, renderAgentStage);

  document.querySelectorAll("[data-goto]").forEach(button => {
    button.onclick = () => navigateToStage(button.dataset.goto);
  });
  select("#generation-agent-button").onclick = () => renderAgentStage(stage);

  document.querySelectorAll("[data-filter]").forEach(button => {
    button.onclick = () => {
      generationViewState.filter = button.dataset.filter;
      rerender();
    };
  });

  select("#plan-visuals-button").onclick = async () => {
    const button = select("#plan-visuals-button");
    button.disabled = true;
    button.textContent = "Deciding…";
    try {
      const planned = await requestJsonFromApi(
        projectApiPath("/visuals/plan"), { method: "POST" });
      showStageNotice("ok", `${planned.audit.scene_count} scene(s) planned.`);
      await refreshProjectSummary();
    } catch (planFailure) {
      console.error("planning visuals failed", planFailure);
      showStageNotice("bad", planFailure.message);
    }
    await rerender();
  };

  const build = select("#build-visuals-button");
  if (build) {
    build.onclick = async () => {
      build.disabled = true;
      build.textContent = "Making…";
      try {
        const built = await requestJsonFromApi(projectApiPath("/visuals/build"), {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ rebuild: false }),
        });
        showStageNotice(built.notes.length ? "warn" : "ok",
          `${built.built_ids.length} picture(s) made.`
          + (built.notes.length ? ` ${built.notes.join(" ")}` : ""));
        await refreshProjectSummary();
      } catch (buildFailure) {
        console.error("building visuals failed", buildFailure);
        showStageNotice("bad", buildFailure.message);
      }
      await rerender();
    };
  }

  document.querySelectorAll("[data-verify]").forEach(button => {
    button.onclick = async () => {
      const key = button.dataset.verify;
      button.disabled = true;
      button.textContent = "Drawing…";
      try {
        const proved = await requestJsonFromApi(
          `/api/scene-renderers/${encodeURIComponent(key)}/verify`, {method: "POST"});
        showStageNotice(proved.ok ? "ok" : "bad",
          proved.ok
            ? `${key}: ${proved.drawable.length} kind(s) drawn in ${proved.seconds}s.`
              + (proved.detail ? ` ${proved.detail}` : "")
            : `${key} could not draw anything. ${proved.detail}`);
      } catch (verifyFailure) {
        console.error("verifying a renderer failed", verifyFailure);
        showStageNotice("bad", verifyFailure.message);
      }
      await rerender();
    };
  });

  document.querySelectorAll("[data-kind-for]").forEach(picker => {
    picker.onchange = () => change(picker.dataset.kindFor, { kind: picker.value }, rerender);
  });
  document.querySelectorAll("[data-motion-for]").forEach(picker => {
    picker.onchange = () => change(picker.dataset.motionFor, { motion: picker.value }, rerender);
  });
}

async function change(visualId, body, rerender) {
  try {
    applicationState.sceneVisuals = await requestJsonFromApi(
      projectApiPath(`/visuals/${encodeURIComponent(visualId)}`), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
  } catch (changeFailure) {
    console.error("changing the shot failed", changeFailure);
    showStageNotice("bad", changeFailure.message);
  }
  await rerender();
}
