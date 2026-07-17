"""Qt bridge over the renderer-neutral Cella DAG and derived-view services."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from PySide6.QtCore import QObject, Property, QUrl, Signal, Slot
from PySide6.QtGui import QColor, QDesktopServices

from cella.dag_service import DagError, _resolve_source_path, impact_analysis, load_graph, query_nodes
from cella.dag_views import compute_view, view_capabilities


NODE_COLOURS = {
    "theorem": "#61d6a8",
    "proof": "#7bc7ff",
    "draft": "#ffcf6e",
    "paper": "#b99cff",
    "campaign": "#ff8c6b",
    "report": "#8fa7c2",
    "evidence": "#e8a7d7",
    "certificate": "#9ce36f",
    "gap": "#ff657a",
    "erratum_or_supersession": "#ff9d55",
    "retirement_package": "#9a9da8",
    "object": "#4fd0c4",
    "definition": "#d9b55f",
    "formula": "#d98cc0",
}

PREFS_PATH = Path.home() / ".config" / "cella_graph_workbench" / "workbench_prefs.json"


class WorkbenchBridge(QObject):
    graphChanged = Signal()
    selectionChanged = Signal()
    statusChanged = Signal()
    busyChanged = Signal()
    sourcesChanged = Signal()
    colorsChanged = Signal()
    bundleChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._graph = load_graph()
        self._nodes: list[dict] = []
        self._edges: list[dict] = []
        self._selected: dict = {}
        self._status = "Loading canonical graph"
        self._busy = False
        self._filters: dict = {}
        self._layout = "layered"
        self._backend = "auto"
        self._positions: dict[str, dict] = {}
        self._affected: set[str] = set()
        self._last_view: dict | None = None
        self._capabilities = view_capabilities()
        self._types = sorted({node["type"] for node in self._graph["nodes"]})
        self._lifecycles = sorted({str(node["lifecycle_status"]) for node in self._graph["nodes"] if node["lifecycle_status"] is not None})
        node_src = Counter((n.get("facets") or {}).get("source_id") for n in self._graph["nodes"])
        edge_src = Counter((e.get("facets") or {}).get("source_id") for e in self._graph["edges"])
        node_src.pop(None, None)
        edge_src.pop(None, None)
        self._src_nodes = dict(node_src)
        self._src_edges = dict(edge_src)
        self._source_ids = sorted(set(node_src) | set(edge_src))
        self._enabled_sources = set(self._source_ids)
        self._cluster_key = "facets.subject"
        self._cluster_keys = self._enumerate_cluster_keys()
        self._colour_overrides = self._load_colour_overrides()
        self._focus_active = False
        self._bundle_strength = 0.0
        self._recompute(write=False)

    def _apply_bundling(self):
        """FDEB-lite: mean-shift compatible edges' control points into cables."""
        beta = self._bundle_strength
        if beta <= 0.01 or len(self._edges) < 4 or len(self._edges) > 6000:
            return
        try:
            import numpy as np
        except Exception:
            return
        edges = self._edges
        p0 = np.array([[e["x1"], e["y1"]] for e in edges], dtype=np.float32)
        p1 = np.array([[e["x2"], e["y2"]] for e in edges], dtype=np.float32)
        direction = p1 - p0
        length = np.clip(np.linalg.norm(direction, axis=1, keepdims=True), 1e-6, None)
        unit = direction / length
        mid = 0.5 * (p0 + p1)
        angle_compat = np.abs(unit @ unit.T) ** 2                 # parallel edges bundle
        gap = mid[:, None, :] - mid[None, :, :]
        dist2 = (gap * gap).sum(axis=2)
        scale = float(np.median(length)) * 0.5 + 1e-6
        proximity = np.exp(-dist2 / (2.0 * scale * scale))        # nearby edges bundle
        compat = (angle_compat * proximity).astype(np.float32)
        np.fill_diagonal(compat, 0.0)
        weights = compat / (compat.sum(axis=1, keepdims=True) + 1e-9)
        segments = 6
        ts = np.linspace(0.0, 1.0, segments + 2, dtype=np.float32)[1:-1]
        ctrl = np.stack([p0 + t * (p1 - p0) for t in ts])         # (segments, E, 2)
        for _ in range(3):
            for k in range(segments):
                target = weights @ ctrl[k]
                straight = p0 + ts[k] * (p1 - p0)
                ctrl[k] = (1.0 - beta) * straight + beta * (0.5 * ctrl[k] + 0.5 * target)
        # Smooth the bundled control polyline into a Catmull-Rom spline so cables curve, not kink.
        full = np.concatenate([p0[None], ctrl, p1[None]], axis=0)  # (M, E, 2)
        # Laplacian smoothing along the edge diffuses out kinks (endpoints pinned).
        for _ in range(8):
            full[1:-1] = 0.5 * full[1:-1] + 0.25 * full[:-2] + 0.25 * full[2:]
        full = np.transpose(full, (1, 0, 2))  # (E, M, 2)
        padded = np.concatenate([full[:, :1], full, full[:, -1:]], axis=1)
        samples = 3
        seg_count = full.shape[1] - 1
        curve = []
        for seg in range(seg_count):
            a, b, c, d = padded[:, seg], padded[:, seg + 1], padded[:, seg + 2], padded[:, seg + 3]
            for s in range(samples):
                t = s / samples
                t2 = t * t
                t3 = t2 * t
                curve.append(0.5 * (2.0 * b + (-a + c) * t
                                    + (2.0 * a - 5.0 * b + 4.0 * c - d) * t2
                                    + (-a + 3.0 * b - 3.0 * c + d) * t3))
        curve.append(full[:, -1])
        smooth = np.stack(curve, axis=1)  # (E, S, 2)
        for i, edge in enumerate(edges):
            flat = []
            for point in smooth[i]:
                flat.extend((float(point[0]), float(point[1])))
            edge["path"] = flat

    def _load_colour_overrides(self) -> dict:
        try:
            if PREFS_PATH.exists():
                data = json.loads(PREFS_PATH.read_text())
                return {str(k): str(v) for k, v in (data.get("colors") or {}).items() if isinstance(v, str)}
        except Exception:
            pass
        return {}

    def _save_prefs(self) -> None:
        try:
            PREFS_PATH.parent.mkdir(parents=True, exist_ok=True)
            PREFS_PATH.write_text(json.dumps({"colors": self._colour_overrides}, indent=2))
        except Exception:
            pass

    def _type_colour(self, node_type: str) -> str:
        return self._colour_overrides.get(node_type) or NODE_COLOURS.get(node_type, "#9ba7b4")

    def _enumerate_cluster_keys(self) -> list[dict]:
        nodes = self._graph["nodes"]
        total = max(len(nodes), 1)
        facet_keys: set[str] = set()
        for node in nodes:
            facet_keys.update((node.get("facets") or {}).keys())
        candidates = [(key, False) for key in ("type", "layer", "claim_status", "lifecycle_status", "reachability", "tracked")]
        candidates += [(key, True) for key in sorted(facet_keys)]
        entries: list[dict] = []
        for key, is_facet in candidates:
            values: set[str] = set()
            coverage = 0
            for node in nodes:
                raw = (node.get("facets") or {}).get(key) if is_facet else node.get(key)
                if raw is not None:
                    coverage += 1
                    values.add(str(raw))
            groups = len(values)
            if not 2 <= groups <= 50:
                continue
            full_key = f"facets.{key}" if is_facet else key
            entries.append({
                "key": full_key,
                "groups": groups,
                "coverage": coverage,
                "label": f"{full_key} · {groups} groups · {round(100 * coverage / total)}%",
            })
        entries.sort(key=lambda item: (-item["coverage"], item["key"]))
        return entries

    @Property("QVariantList", notify=graphChanged)
    def nodes(self):
        return self._nodes

    @Property("QVariantList", notify=graphChanged)
    def edges(self):
        return self._edges

    @Property("QVariantMap", notify=selectionChanged)
    def selectedNode(self):
        return self._selected

    @Property(str, notify=statusChanged)
    def statusText(self):
        return self._status

    @Property(bool, notify=busyChanged)
    def busy(self):
        return self._busy

    @Property(str, constant=True)
    def graphRevision(self):
        return self._graph["revision"]

    @Property("QVariantList", constant=True)
    def artifactTypes(self):
        return ["All types", *self._types]

    @Property("QVariantList", constant=True)
    def lifecycleStatuses(self):
        return ["All lifecycle", *self._lifecycles]

    @Property("QVariantList", notify=sourcesChanged)
    def sourceList(self):
        items = []
        for sid in self._source_ids:
            parts = []
            nodes = self._src_nodes.get(sid, 0)
            edges = self._src_edges.get(sid, 0)
            if nodes:
                parts.append(f"{nodes} nodes")
            if edges:
                parts.append(f"{edges} edges")
            items.append({"id": sid, "label": f"{sid} · " + " · ".join(parts), "enabled": sid in self._enabled_sources})
        return items

    @Property("QVariantList", constant=True)
    def layoutNames(self):
        return list(self._capabilities["layouts"].keys())

    @Property("QVariantList", constant=True)
    def clusterKeys(self):
        return self._cluster_keys

    @Property("QVariantList", notify=colorsChanged)
    def typeColours(self):
        return [{"type": node_type, "colour": self._type_colour(node_type)} for node_type in self._types]

    @Property(str, constant=True)
    def cudaLabel(self):
        cuda = self._capabilities["backends"]["cuda"]
        return cuda["device"] if cuda["available"] else "CUDA unavailable"

    @Property(bool, constant=True)
    def cudaAvailable(self):
        return bool(self._capabilities["backends"]["cuda"]["available"])

    def _set_busy(self, value: bool):
        if self._busy != value:
            self._busy = value
            self.busyChanged.emit()

    def _set_status(self, value: str):
        self._status = value
        self.statusChanged.emit()

    def _display_node(self, node: dict) -> dict:
        position = self._positions.get(node["id"], {"x": 0.5, "y": 0.5})
        return {
            "id": node["id"],
            "label": node["label"],
            "type": node["type"],
            "lifecycle": node["lifecycle_status"] or "none",
            "claim": node["claim_status"] or "none",
            "reachability": node["reachability"] or "none",
            "tracked": node["tracked"],
            "x": position["x"],
            "y": position["y"],
            "colour": self._type_colour(node["type"]),
            "affected": node["id"] in self._affected,
        }

    def _refresh_models(self):
        if not self._filters:
            visible_nodes = self._graph["nodes"]
        else:
            visible_nodes = []
            cursor = 0
            while True:
                page = query_nodes(self._filters, edge_mode="none", limit=500, cursor=cursor)
                visible_nodes.extend(page["nodes"])
                if page["next_cursor"] is None:
                    break
                cursor = page["next_cursor"]
        all_on = len(self._enabled_sources) == len(self._source_ids)
        if not all_on:
            visible_nodes = [n for n in visible_nodes if (n.get("facets") or {}).get("source_id") in self._enabled_sources]
        focus_id = self._selected.get("id") if self._focus_active else None
        if focus_id is not None and any(node["id"] == focus_id for node in visible_nodes):
            neighbours = {focus_id}
            for edge in self._graph["edges"]:
                if not all_on and (edge.get("facets") or {}).get("source_id") not in self._enabled_sources:
                    continue
                if edge["from"] == focus_id:
                    neighbours.add(edge["to"])
                elif edge["to"] == focus_id:
                    neighbours.add(edge["from"])
            visible_nodes = [node for node in visible_nodes if node["id"] in neighbours]
        else:
            focus_id = None
        visible = {node["id"] for node in visible_nodes}
        node_colour = {node["id"]: self._type_colour(node["type"]) for node in visible_nodes}
        self._nodes = [self._display_node(node) for node in visible_nodes]
        self._edges = []
        for edge in self._graph["edges"]:
            if edge["from"] not in visible or edge["to"] not in visible:
                continue
            if not all_on and (edge.get("facets") or {}).get("source_id") not in self._enabled_sources:
                continue
            if focus_id is not None and focus_id != edge["from"] and focus_id != edge["to"]:
                continue
            source = self._positions.get(edge["from"], {"x": 0.5, "y": 0.5})
            target = self._positions.get(edge["to"], {"x": 0.5, "y": 0.5})
            self._edges.append({
                "id": edge["id"],
                "from": edge["from"],
                "to": edge["to"],
                "relation": edge["relation"],
                "x1": source["x"], "y1": source["y"],
                "x2": target["x"], "y2": target["y"],
                "colour1": node_colour.get(edge["from"], "#40505f"),
                "colour2": node_colour.get(edge["to"], "#40505f"),
                "affected": edge["from"] in self._affected or edge["to"] in self._affected,
            })
        self._apply_bundling()
        self.graphChanged.emit()

    def _recompute(self, *, write: bool):
        self._set_busy(True)
        try:
            result = compute_view(
                self._layout,
                self._backend,
                self._filters,
                {"seed": 17, "iterations": 180, "cluster_key": self._cluster_key},
                write=write,
            )
            self._last_view = result
            self._positions = {item["id"]: item for item in result["view"]["geometry"]["node_positions"]}
            self._refresh_models()
            compute = result["view"]["compute"]
            suffix = f" · saved {Path(result['path']).name}" if result["path"] else ""
            self._set_status(
                f"{result['counts']['nodes']} nodes · {result['counts']['edges']} edges · "
                f"{compute['algorithm']} on {compute['backend_resolved']} ({compute['device']}){suffix}"
            )
        except DagError as exc:
            self._set_status(f"{exc.token}: {exc.message}")
        except Exception as exc:
            self._set_status(f"WORKBENCH_ERROR: {type(exc).__name__}: {exc}")
        finally:
            self._set_busy(False)

    @Slot(str, str, str)
    def applyFilters(self, text: str, artifact_type: str, lifecycle: str):
        filters: dict = {}
        if text.strip():
            filters["text"] = text.strip()
        if artifact_type and artifact_type != "All types":
            filters["types"] = [artifact_type]
        if lifecycle and lifecycle != "All lifecycle":
            filters["lifecycle_statuses"] = [lifecycle]
        self._filters = filters
        self._affected.clear()
        self._recompute(write=False)

    @Slot(str, bool)
    def setSourceEnabled(self, source_id: str, enabled: bool):
        if enabled:
            self._enabled_sources.add(source_id)
        else:
            self._enabled_sources.discard(source_id)
        self.sourcesChanged.emit()
        self._refresh_models()

    @Slot(bool)
    def setAllSources(self, enabled: bool):
        self._enabled_sources = set(self._source_ids) if enabled else set()
        self.sourcesChanged.emit()
        self._refresh_models()

    @Slot(str, QColor)
    def setTypeColour(self, node_type: str, colour: QColor):
        self._colour_overrides[node_type] = colour.name()
        self._save_prefs()
        self.colorsChanged.emit()
        self._refresh_models()

    @Slot()
    def resetColours(self):
        self._colour_overrides = {}
        self._save_prefs()
        self.colorsChanged.emit()
        self._refresh_models()

    @Slot(bool)
    def setFocusEdges(self, enabled: bool):
        self._focus_active = bool(enabled)
        self._refresh_models()

    @Property(float, notify=bundleChanged)
    def bundleStrength(self):
        return self._bundle_strength

    @Slot(float)
    def setBundleStrength(self, value: float):
        self._bundle_strength = max(0.0, min(1.0, float(value)))
        self.bundleChanged.emit()
        self._refresh_models()

    @Slot(str, str, bool, str)
    def computeLayout(self, algorithm: str, backend: str, save: bool = False, cluster_key: str = ""):
        self._layout = algorithm.lower()
        self._backend = backend.lower()
        if cluster_key:
            self._cluster_key = cluster_key
        self._recompute(write=save)

    @Slot(str)
    def selectNode(self, node_id: str):
        node = next((item for item in self._graph["nodes"] if item["id"] == node_id), None)
        if node is None:
            self._set_status(f"NODE_NOT_FOUND: {node_id}")
            return
        source_lines = [
            f"{ref['pointer']}\nsha256:{ref['sha256']}" if ref.get("sha256") else ref["pointer"]
            for ref in node["source_refs"]
        ]
        external_lines = [
            f"{namespace}: {', '.join(values)}"
            for namespace, values in node["external_ids"].items() if values
        ]
        self._selected = {
            **node,
            "source_text": "\n\n".join(source_lines) or "No source pointers",
            "external_text": "\n".join(external_lines) or "No external identifiers",
            "retrieval_text": json.dumps(node["retrieval"], indent=2, ensure_ascii=False),
        }
        self.selectionChanged.emit()
        if self._focus_active:
            self._refresh_models()
        self._set_status(f"Selected {node['id']}")

    @Slot()
    def impactSelected(self):
        node_id = self._selected.get("id")
        if not node_id:
            self._set_status("Select a node before requesting impact closure")
            return
        try:
            impact = impact_analysis([node_id])
            self._affected = {node_id, *(item["id"] for item in impact["affected_nodes"])}
            self._refresh_models()
            self._set_status(
                f"Impact closure: {impact['affected_node_count']} downstream nodes · "
                f"{len(impact['reevaluate_files'])} source files flagged"
            )
        except DagError as exc:
            self._set_status(f"{exc.token}: {exc.message}")

    @Slot()
    def clearImpact(self):
        self._affected.clear()
        self._refresh_models()
        self._set_status("Impact highlighting cleared")

    @Slot()
    def revealSource(self):
        node_id = self._selected.get("id")
        if not node_id:
            self._set_status("Select a node before revealing its source")
            return
        refs = self._selected.get("source_refs") or []
        pointer = refs[0].get("pointer") if refs else None
        if not pointer:
            self._set_status("Selected node has no source pointer")
            return
        path = _resolve_source_path(pointer)
        if path is None:
            self._set_status(f"UNRESOLVED_SOURCE: {pointer}")
            return
        folder = path if path.is_dir() else path.parent
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))
        self._set_status(f"Revealed {folder}")
