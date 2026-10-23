/**
 * Pictures for the video — on the Extraction page.
 *
 * A video's pictures are made for it by the image model. From the deck, only the
 * two or three a person picks here are used, each under the name they give it;
 * no other extracted picture needs reviewing.
 */

import { requestJsonFromApi } from "/static/shared-client.js";
import { escapeHtml, projectApiPath, select, showStageNotice } from "/static/ui-kit.js";

/** Every extracted figure that has a stored image, once. */
function figuresOf(extraction) {
  const seen = new Set();
  const figures = [];
  for (const document of extraction?.documents ?? []) {
    for (const block of document.blocks ?? []) {
      if (block.kind !== "figure" || !block.asset_path || seen.has(block.asset_path)) continue;
      seen.add(block.asset_path);
      figures.push(block);
    }
  }
  return figures;
}

export async function loadPicks() {
  return requestJsonFromApi(projectApiPath("/chosen-pictures"))
    .catch(() => ({ chosen: [], most: 3 }));
}

export function renderPicksCard(extraction, picks) {
  const figures = figuresOf(extraction);
  if (!figures.length) return "";
  const named = Object.fromEntries((picks.chosen ?? []).map(p => [p.asset_path, p.name]));
  const count = Object.keys(named).length;
  return `
    <details class="card" id="picks-card" style="margin-bottom:12px" ${count ? "" : "open"}>
      <summary><b>Pictures for the video</b> — ${count} of ${picks.most} chosen</summary>
      <p class="muted" style="margin:6px 0 10px">The video's pictures are made for it.
        Pick up to ${picks.most} from the deck that it must show, and name each; no other
        picture needs reviewing.</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px">
        ${figures.map(block => {
          const file = block.asset_path.split("/").pop();
          const name = named[block.asset_path];
          return `
            <div class="pick ${name ? "chosen" : ""}" data-pick="${escapeHtml(block.asset_path)}"
                 style="border:2px solid ${name ? "var(--accent, #2bb673)" : "transparent"};
                        border-radius:10px;padding:6px">
              <img src="${projectApiPath(`/extraction/assets/${encodeURIComponent(file)}`)}"
                   alt="" loading="lazy" style="width:100%;height:110px;object-fit:contain">
              <input class="pick-name" placeholder="Name it to use it"
                     value="${escapeHtml(name ?? "")}" style="width:100%;margin-top:6px">
              <div style="display:flex;gap:6px;margin-top:6px">
                <button class="btn pick-use">${name ? "Rename" : "Use in video"}</button>
                ${name ? `<button class="btn pick-drop">Let go</button>` : ""}
              </div>
            </div>`;
        }).join("")}
      </div>
    </details>`;
}

export function wirePicksCard(refresh) {
  const card = select("#picks-card");
  if (!card) return;
  const send = async (assetPath, name, keep) => {
    try {
      await requestJsonFromApi(projectApiPath("/chosen-pictures"), {
        method: "PUT", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ asset_path: assetPath, name, keep }),
      });
      await refresh();
    } catch (pickFailure) {
      showStageNotice("bad", pickFailure.message);
    }
  };
  card.querySelectorAll("[data-pick]").forEach(tile => {
    const assetPath = tile.dataset.pick;
    tile.querySelector(".pick-use").onclick = () =>
      send(assetPath, tile.querySelector(".pick-name").value, true);
    const drop = tile.querySelector(".pick-drop");
    if (drop) drop.onclick = () => send(assetPath, "", false);
  });
}
