"""When a layer changes, every layer after it says so.

Each layer hands its work on with a transfer. A later layer built from that
transfer is only right while the transfer stands: re-transfer the extraction
with a slide changed, and the plan, the script, the shots and the render are all
now about something that is no longer what was extracted. Nothing used to say
so, layer by layer; a person had to remember.

So every transfer records what it was **built from** -- a small snapshot of each
earlier layer it reads, part by part (each slide, each section, each scene, each
picture). When an earlier layer is transferred again, the layers after it are
flagged, and the flag names exactly which parts are new, changed or gone. A
layer further down is flagged too, because what it was built on is now behind.

The flag clears when the layer is transferred again -- after redoing it for the
new input, or as it stands, which is a person saying it still holds.

All of it is comparison of fingerprints: the same transfers always give the same
flags. Stored at `handoffs.json` in the project.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from pipeline.storage.documents import read_json_object, write_text_atomically

# In the order the work flows. What each reads directly. Nothing after Scene Plan
# reads Assets & Design: the plan carries its pictures, brand kit and look on.
READS = {
    "assets": ["extraction"],
    "scene-plan": ["extraction", "assets"],
    "script-staging": ["scene-plan", "extraction"],
    "generation": ["script-staging", "scene-plan"],
    "render": ["generation", "script-staging", "scene-plan"],
}
ORDER = ["extraction", "assets", "scene-plan", "script-staging", "generation", "render"]
NAMES = {"extraction": "Extraction", "assets": "Assets & Design", "scene-plan": "Scene Plan",
         "script-staging": "Script & Staging", "generation": "Generation", "render": "Render"}
MOST_PARTS_NAMED = 8


def _hash(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _snapshot(fingerprint: str, at: str, parts: dict[str, list[str]],
              digest: str = "") -> dict[str, Any]:
    """`digest` is the layer's own digest of what it transferred: equal digests
    mean the same content, however its parts are described here."""
    return {"fingerprint": fingerprint, "at": at, "parts": parts, "digest": digest}


# --- what each layer last handed on, part by part --------------------------------------


def _extraction(project) -> dict[str, Any] | None:
    from pipeline.extraction import ExtractionStore

    extraction = ExtractionStore(project.root).load()
    if not extraction.documents:
        return None
    # Keyed by place, not by file: a project has one source, so a replaced file
    # shows as the slides that differ rather than as everything gone and new.
    parts: dict[str, list[str]] = {"~source": [
        "the source file", _hash([d.file_name for d in extraction.documents])]}
    for document in extraction.documents:
        groups: dict[str, tuple[str, list]] = {}
        for block in document.blocks:
            if block.slide_number:
                key = f"slide{block.slide_number:04d}"
                label = f"slide {block.slide_number}"
            else:
                top = block.heading_path[0] if block.heading_path else "(before any heading)"
                key, label = f"#{top}", f"“{top}”"
            groups.setdefault(key, (label, []))[1].append(
                [str(block.kind), block.text, block.asset_path])
        for key, (label, content) in groups.items():
            parts[key] = [label, _hash(content)]
    return _snapshot(_hash(parts), extraction.confirmed_at or extraction.extracted_at, parts,
                     extraction.content_fingerprint())


def _assets(project) -> dict[str, Any] | None:
    from pipeline.assets_handoff import ConfirmedAssetStore

    confirmed = ConfirmedAssetStore(project.root).load()
    if not confirmed.confirmed_at:
        return None
    parts = {f.asset_path: [f.caption or "a picture", _hash([f.use, f.shown_path])]
             for f in confirmed.library.handed_on()}
    parts["~look"] = ["the look", _hash(confirmed.library.look.model_dump())]
    parts["~brand"] = ["the brand assets", _hash(confirmed.brand.model_dump())]
    return _snapshot(_hash(parts), confirmed.confirmed_at, parts, confirmed.fingerprint)


def _plan(project) -> dict[str, Any] | None:
    from pipeline.plan_handoff import TransferredPlanStore

    transferred = TransferredPlanStore(project.root).load()
    if not transferred.transferred_at:
        return None
    plan = transferred.plan
    parts = {s.id: [f"section “{s.title or 'Untitled'}”", _hash(s.model_dump(mode="json"))]
             for s in plan.sections}
    parts["~brief"] = ["the brief (audience and objectives)", _hash([
        plan.selected_audience, [o.model_dump() for o in plan.learning_objectives]])]
    if transferred.assets is not None:
        parts["~assets"] = ["the pictures, brand kit and look it carries",
                            transferred.assets.fingerprint]
    return _snapshot(_hash(parts), transferred.transferred_at, parts, transferred.fingerprint)


def _script(project) -> dict[str, Any] | None:
    from pipeline.plan_handoff import plan_for_later_stages
    from pipeline.script_handoff import TransferredScriptStore

    transferred = TransferredScriptStore(project.root).load()
    if not transferred.transferred_at:
        return None
    titles = {s.id: s.title for s in plan_for_later_stages(project).sections}
    parts = {
        entry.section_id: [
            f"the narration of “{titles.get(entry.section_id, entry.section_id)}”",
            _hash([[scene.narration, scene.brief] for scene in entry.scenes])]
        for entry in transferred.script.section_scripts}
    return _snapshot(_hash(parts), transferred.transferred_at, parts, transferred.fingerprint)


def _generation(project) -> dict[str, Any] | None:
    from pipeline.generation_handoff import TransferredVisualStore

    transferred = TransferredVisualStore(project.root).load()
    if not transferred.transferred_at:
        return None
    parts = {
        v.scene_id or v.id: [
            f"the shot for “{v.section_title}” scene {v.scene_number}",
            _hash(v.model_dump(mode="json", exclude={"built_at", "id"}))]
        for v in transferred.visuals.visuals}
    return _snapshot(_hash(parts), transferred.transferred_at, parts, transferred.fingerprint)


_SNAPSHOTS = {"extraction": _extraction, "assets": _assets, "scene-plan": _plan,
              "script-staging": _script, "generation": _generation}


def _has_output(project, layer: str) -> bool:
    if layer == "render":
        from pipeline.render_job import RenderJobStore
        return RenderJobStore(project.root).load().status == "done"
    return _SNAPSHOTS[layer](project) is not None


# --- the record ---------------------------------------------------------------------------


def _path(project):
    return project.root / "handoffs.json"


def _load(project) -> dict[str, Any]:
    return read_json_object(_path(project), "hand-off record") or {}


def record(project, layer: str) -> None:
    """Note what `layer` is being handed on from. Called by its transfer."""
    records = _load(project)
    records[layer] = {reads: _SNAPSHOTS[reads](project) for reads in READS.get(layer, [])}
    write_text_atomically(_path(project), json.dumps(records, indent=1, ensure_ascii=False))


def _difference(was: dict[str, Any], now: dict[str, Any]) -> dict[str, list[str]]:
    before, after = was.get("parts", {}), now.get("parts", {})
    return {
        "added": [after[k][0] for k in after if k not in before],
        "removed": [before[k][0] for k in before if k not in after],
        "changed": [after[k][0] for k in after if k in before and before[k][1] != after[k][1]],
    }


def upstream_state(project) -> dict[str, Any]:
    """For each layer: what changed before it since it was handed on."""
    records = _load(project)
    current = {layer: make(project) for layer, make in _SNAPSHOTS.items()}
    state: dict[str, Any] = {}
    adopted = False

    for layer in ORDER[1:]:
        if not _has_output(project, layer):
            state[layer] = {"flagged": False, "changes": [], "behind": [],
                            "name": NAMES[layer]}
            continue
        extraction_was = (records.get(layer) or {}).get("extraction")
        if layer not in records or (extraction_was and "~source" not in extraction_was["parts"]):
            # Handed on before this record existed -- or recorded when its parts
            # were keyed by file name, before a project had one source: taken as
            # in step, once, as it stands, so an older project is not flagged for
            # changes nobody made.
            records[layer] = {reads: current[reads] for reads in READS[layer]}
            adopted = True
        changes = []
        for reads in READS[layer]:
            was, now = records[layer].get(reads), current[reads]
            if not was or not now or was["fingerprint"] == now["fingerprint"]:
                continue
            same = (was["digest"] == now["digest"]) if was.get("digest") and now.get("digest") \
                else bool(was.get("at")) and was["at"] == now["at"]
            if same:
                # The same transfer, described differently: the app learned to
                # record something new about it. Only new content is a change.
                records[layer][reads] = now
                adopted = True
                continue
            difference = _difference(was, now)
            changes.append({
                "layer": reads, "name": NAMES[reads], "at": now["at"], "was_at": was["at"],
                **{kind: labels[:MOST_PARTS_NAMED] for kind, labels in difference.items()},
                "counts": {kind: len(labels) for kind, labels in difference.items()},
            })
        behind = [NAMES[reads] for reads in READS[layer]
                  if state.get(reads, {}).get("flagged")]
        state[layer] = {"flagged": bool(changes or behind), "changes": changes,
                        "behind": behind, "name": NAMES[layer]}

    if adopted:
        write_text_atomically(_path(project), json.dumps(records, indent=1, ensure_ascii=False))
    return state


def is_behind(project, layer: str) -> bool:
    """Whether what `layer` reads directly has been handed on again since."""
    return bool(upstream_state(project).get(layer, {}).get("changes"))
