"""Revision-bound derived views for the Cella research DAG.

The canonical DAG remains authoritative.  This module computes disposable,
content-addressed geometry records that renderers may consume without placing
layout state in the graph itself.  CPU support is always available; optional
CUDA implementations are selected behind the same record contract.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import math
import os
import tempfile
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .dag_service import DagError, dag_root, load_graph, object_digest, query_nodes


VIEW_SCHEMA = "cella-derived-view-v1"
VIEW_SCHEMA_VERSION = 1
LAYOUT_ALGORITHMS = ("layered", "spring", "forceatlas2", "radial", "clustered", "circular")
DETERMINISTIC_LAYOUTS = ("layered", "radial", "clustered", "circular")
BACKENDS = ("auto", "cpu", "cuda")
MAX_VIEW_NODES = 100_000


def derived_view_root() -> Path:
    override = os.environ.get("CELLA_DAG_VIEW_ROOT")
    return Path(override).resolve() if override else dag_root() / "derived_views"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def _cuda_status() -> dict:
    record = {
        "available": False,
        "implementation": None,
        "device": None,
        "reason": "PyTorch is not installed",
    }
    if not _module_available("torch"):
        return record
    try:
        import torch

        if not torch.cuda.is_available():
            record["reason"] = "PyTorch is installed but CUDA is unavailable"
            return record
        record.update(
            available=True,
            implementation="torch-cuda-force-v1",
            device=torch.cuda.get_device_name(0),
            reason=None,
        )
    except Exception as exc:  # optional capability probe must remain safe
        record["reason"] = f"CUDA probe failed: {type(exc).__name__}: {exc}"
    return record


def view_capabilities() -> dict:
    cuda = _cuda_status()
    return {
        "schema": VIEW_SCHEMA,
        "ok": True,
        "layouts": {
            "layered": {
                "dimensions": [2],
                "backends": ["cpu"],
                "deterministic": True,
                "purpose": "Readable directed succession/dependency ranks.",
            },
            "spring": {
                "dimensions": [2],
                "backends": ["cpu"] + (["cuda"] if cuda["available"] else []),
                "deterministic_with_seed": True,
                "purpose": "Exploratory force-directed topology.",
            },
            "forceatlas2": {
                "dimensions": [2],
                "backends": ["cpu"] + (["cuda"] if cuda["available"] else []),
                "deterministic_with_seed": True,
                "purpose": "Community-separating force layout: pulls clusters apart into a galaxy of islands.",
            },
            "radial": {
                "dimensions": [2],
                "backends": ["cpu"],
                "deterministic": True,
                "purpose": "Concentric rings by proof status: proven core, frontier on the rim.",
            },
            "clustered": {
                "dimensions": [2],
                "backends": ["cpu"],
                "deterministic": True,
                "parameters": {"cluster_key": "node field or facets.<key> to group by (default facets.subject)"},
                "purpose": "Territory map: nodes grouped into regions by a chosen categorical key.",
            },
            "circular": {
                "dimensions": [2],
                "backends": ["cpu"],
                "deterministic": True,
                "purpose": "All nodes on one ring, ordered by type then id; edges chord across.",
            },
        },
        "backends": {
            "cpu": {
                "available": True,
                "networkx": _module_available("networkx"),
                "implementation": "networkx-spring" if _module_available("networkx") else "cella-layered-stdlib-v1",
            },
            "cuda": cuda,
        },
        "renderer_contract": {
            "authoritative_input": "canonical DAG JSON",
            "derived_output": "revision-bound view JSON",
            "high_volume_transport": "shared memory or CUDA-graphics interoperability; not MCP JSON",
        },
    }


def _selected_graph(filters: dict | None) -> dict:
    graph = load_graph()
    if not filters:
        return graph
    selected_nodes: list[dict] = []
    cursor = 0
    while True:
        page = query_nodes(filters, edge_mode="none", limit=500, cursor=cursor)
        selected_nodes.extend(page["nodes"])
        if len(selected_nodes) > MAX_VIEW_NODES:
            raise DagError("VIEW_FILTER_TOO_BROAD", f"view selection exceeds {MAX_VIEW_NODES} nodes")
        if page["next_cursor"] is None:
            break
        cursor = page["next_cursor"]
    selected_ids = {node["id"] for node in selected_nodes}
    return {
        **{key: value for key, value in graph.items() if key not in {"nodes", "edges"}},
        "nodes": selected_nodes,
        "edges": [
            edge for edge in graph["edges"]
            if edge["from"] in selected_ids and edge["to"] in selected_ids
        ],
    }


def _normalise_positions(positions: dict[str, tuple[float, float]]) -> list[dict]:
    if not positions:
        return []
    xs = [point[0] for point in positions.values()]
    ys = [point[1] for point in positions.values()]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    dx = x1 - x0 or 1.0
    dy = y1 - y0 or 1.0
    return [
        {
            "id": node_id,
            "x": round((positions[node_id][0] - x0) / dx, 8),
            "y": round((positions[node_id][1] - y0) / dy, 8),
        }
        for node_id in sorted(positions)
    ]


def _layered_layout(graph: dict, _parameters: dict) -> tuple[list[dict], dict]:
    node_ids = sorted(node["id"] for node in graph["nodes"])
    outgoing: dict[str, list[str]] = defaultdict(list)
    indegree = {node_id: 0 for node_id in node_ids}
    for edge in graph["edges"]:
        if edge["from"] in indegree and edge["to"] in indegree:
            outgoing[edge["from"]].append(edge["to"])
            indegree[edge["to"]] += 1
    rank = {node_id: 0 for node_id in node_ids}
    queue = deque(sorted(node_id for node_id, degree in indegree.items() if degree == 0))
    visited: set[str] = set()
    while queue:
        node_id = queue.popleft()
        visited.add(node_id)
        for target in sorted(outgoing[node_id]):
            rank[target] = max(rank[target], rank[node_id] + 1)
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    # Cyclic/non-succession relations are kept visible in a final stable rank.
    unresolved = sorted(set(node_ids) - visited)
    cycle_rank = max(rank.values(), default=0) + (1 if visited and unresolved else 0)
    for node_id in unresolved:
        rank[node_id] = cycle_rank
    groups: dict[int, list[str]] = defaultdict(list)
    for node_id in node_ids:
        groups[rank[node_id]].append(node_id)
    positions: dict[str, tuple[float, float]] = {}
    for x_index, rank_value in enumerate(sorted(groups)):
        members = groups[rank_value]
        for y_index, node_id in enumerate(members):
            positions[node_id] = (float(x_index), float(y_index) - (len(members) - 1) / 2.0)
    return _normalise_positions(positions), {
        "implementation": "cella-layered-stdlib-v1",
        "device": "CPU",
        "cycle_bucket_nodes": unresolved,
    }


def _cluster_value(node: dict, key: str) -> str | None:
    if key.startswith("facets."):
        raw = (node.get("facets") or {}).get(key[len("facets."):])
    else:
        raw = node.get(key)
    return None if raw is None else str(raw)


def _radial_layout(graph: dict, _parameters: dict) -> tuple[list[dict], dict]:
    tier = {"machine-verified": 0, "proved": 0, "demonstrated": 1, "conjectured": 1}
    rings: dict[int, list[str]] = defaultdict(list)
    for node in graph["nodes"]:
        rings[tier.get(node.get("claim_status"), 2)].append(node["id"])
    radii = {0: 0.16, 1: 0.55, 2: 1.0}
    positions: dict[str, tuple[float, float]] = {}
    for ring, members in rings.items():
        members.sort()
        radius = radii.get(ring, 1.0)
        count = len(members)
        for i, node_id in enumerate(members):
            angle = 2.0 * math.pi * i / max(count, 1)
            positions[node_id] = (radius * math.cos(angle), radius * math.sin(angle))
    return _normalise_positions(positions), {
        "implementation": "cella-radial-stdlib-v1",
        "device": "CPU",
        "rings": {str(ring): len(members) for ring, members in sorted(rings.items())},
    }


def _clustered_layout(graph: dict, parameters: dict) -> tuple[list[dict], dict]:
    key = str(parameters.get("cluster_key") or "facets.subject")
    groups: dict[str, list[str]] = defaultdict(list)
    for node in graph["nodes"]:
        groups[_cluster_value(node, key) or "(unset)"].append(node["id"])
    names = sorted(groups)
    total = max(len(names), 1)
    node_count = max(len(graph["nodes"]), 1)
    positions: dict[str, tuple[float, float]] = {}
    for group_index, name in enumerate(names):
        members = sorted(groups[name])
        angle = 2.0 * math.pi * group_index / total
        centre_x, centre_y = math.cos(angle), math.sin(angle)
        span = 0.30 * math.sqrt(len(members) / node_count)
        for member_index, node_id in enumerate(members):
            radius = span * math.sqrt(member_index / max(len(members), 1))
            spiral = member_index * 2.399963229728653  # golden angle
            positions[node_id] = (centre_x + radius * math.cos(spiral), centre_y + radius * math.sin(spiral))
    return _normalise_positions(positions), {
        "implementation": "cella-clustered-stdlib-v1",
        "device": "CPU",
        "cluster_key": key,
        "clusters": {name: len(members) for name, members in sorted(groups.items())},
    }


def _circular_layout(graph: dict, _parameters: dict) -> tuple[list[dict], dict]:
    ordered = sorted(graph["nodes"], key=lambda node: (str(node.get("type")), node["id"]))
    count = len(ordered)
    positions: dict[str, tuple[float, float]] = {}
    for index, node in enumerate(ordered):
        angle = 2.0 * math.pi * index / max(count, 1)
        positions[node["id"]] = (math.cos(angle), math.sin(angle))
    return _normalise_positions(positions), {
        "implementation": "cella-circular-stdlib-v1",
        "device": "CPU",
    }


def _spring_cpu_layout(graph: dict, parameters: dict) -> tuple[list[dict], dict]:
    if not _module_available("networkx"):
        raise DagError("BACKEND_UNAVAILABLE", "spring/cpu requires NetworkX")
    import networkx as nx

    nx_graph = nx.DiGraph()
    nx_graph.add_nodes_from(node["id"] for node in graph["nodes"])
    nx_graph.add_edges_from((edge["from"], edge["to"]) for edge in graph["edges"])
    seed = int(parameters.get("seed", 17))
    iterations = max(1, min(int(parameters.get("iterations", 100)), 2000))
    k = parameters.get("k")
    k = float(k) if k is not None else None
    raw = nx.spring_layout(nx_graph, seed=seed, iterations=iterations, k=k, dim=2)
    positions = {node_id: (float(point[0]), float(point[1])) for node_id, point in raw.items()}
    return _normalise_positions(positions), {
        "implementation": f"networkx-{nx.__version__}-spring",
        "device": "CPU",
    }


def _spring_cuda_layout(graph: dict, parameters: dict) -> tuple[list[dict], dict]:
    cuda = _cuda_status()
    if not cuda["available"]:
        raise DagError("BACKEND_UNAVAILABLE", cuda["reason"] or "CUDA is unavailable")
    import torch

    node_ids = sorted(node["id"] for node in graph["nodes"])
    count = len(node_ids)
    if not count:
        return [], {"implementation": cuda["implementation"], "device": cuda["device"]}
    index = {node_id: i for i, node_id in enumerate(node_ids)}
    seed = int(parameters.get("seed", 17))
    iterations = max(1, min(int(parameters.get("iterations", 200)), 5000))
    generator = torch.Generator(device="cuda").manual_seed(seed)
    angles = torch.linspace(0.0, 2.0 * math.pi, count + 1, device="cuda")[:-1]
    positions = torch.stack((torch.cos(angles), torch.sin(angles)), dim=1)
    positions += 0.025 * torch.randn((count, 2), generator=generator, device="cuda")
    if graph["edges"]:
        sources = torch.tensor([index[edge["from"]] for edge in graph["edges"]], device="cuda", dtype=torch.long)
        targets = torch.tensor([index[edge["to"]] for edge in graph["edges"]], device="cuda", dtype=torch.long)
    else:
        sources = targets = torch.empty(0, device="cuda", dtype=torch.long)
    ideal = float(parameters.get("ideal_distance", max(0.08, 1.0 / math.sqrt(count))))
    step = float(parameters.get("step", 0.035))
    for iteration in range(iterations):
        delta = positions[:, None, :] - positions[None, :, :]
        distance2 = delta.square().sum(dim=2).clamp_min(1e-4)
        repulsion = (delta / distance2[:, :, None]).sum(dim=1) * (ideal * ideal)
        attraction = torch.zeros_like(positions)
        if sources.numel():
            edge_delta = positions[sources] - positions[targets]
            edge_distance = edge_delta.norm(dim=1, keepdim=True).clamp_min(1e-4)
            force = edge_delta * edge_distance / max(ideal, 1e-4)
            attraction.index_add_(0, sources, -force)
            attraction.index_add_(0, targets, force)
        cooling = 1.0 - (iteration / max(iterations, 1)) * 0.9
        velocity = (repulsion + attraction).clamp(-10.0, 10.0)
        positions += step * cooling * velocity
        positions -= positions.mean(dim=0, keepdim=True)
    host = positions.detach().cpu().tolist()
    result = {node_id: (float(host[i][0]), float(host[i][1])) for i, node_id in enumerate(node_ids)}
    return _normalise_positions(result), {
        "implementation": cuda["implementation"],
        "device": cuda["device"],
        "precision": "float32",
    }


def _forceatlas2_cuda_layout(graph: dict, parameters: dict) -> tuple[list[dict], dict]:
    cuda = _cuda_status()
    if not cuda["available"]:
        raise DagError("BACKEND_UNAVAILABLE", cuda["reason"] or "CUDA is unavailable")
    import torch

    node_ids = sorted(node["id"] for node in graph["nodes"])
    count = len(node_ids)
    if not count:
        return [], {"implementation": "torch-cuda-forceatlas2-v1", "device": cuda["device"]}
    index = {node_id: i for i, node_id in enumerate(node_ids)}
    seed = int(parameters.get("seed", 17))
    iterations = max(1, min(int(parameters.get("iterations", 400)), 5000))
    generator = torch.Generator(device="cuda").manual_seed(seed)
    angles = torch.linspace(0.0, 2.0 * math.pi, count + 1, device="cuda")[:-1]
    positions = torch.stack((torch.cos(angles), torch.sin(angles)), dim=1)
    positions += 0.05 * torch.randn((count, 2), generator=generator, device="cuda")
    deg = torch.zeros(count, device="cuda")
    if graph["edges"]:
        sources = torch.tensor([index[edge["from"]] for edge in graph["edges"]], device="cuda", dtype=torch.long)
        targets = torch.tensor([index[edge["to"]] for edge in graph["edges"]], device="cuda", dtype=torch.long)
        deg.index_add_(0, sources, torch.ones(sources.shape[0], device="cuda"))
        deg.index_add_(0, targets, torch.ones(targets.shape[0], device="cuda"))
    else:
        sources = targets = torch.empty(0, device="cuda", dtype=torch.long)
    mass = deg + 1.0  # FA2 "mass": hubs repel and are pulled to centre more strongly
    k_repulsion = float(parameters.get("repulsion", 0.02))
    gravity = float(parameters.get("gravity", 0.08))
    step = float(parameters.get("step", 0.02))
    for iteration in range(iterations):
        delta = positions[:, None, :] - positions[None, :, :]
        distance2 = delta.square().sum(dim=2).clamp_min(1e-4)
        mass_factor = mass[:, None] * mass[None, :]
        repulsion = (delta * (mass_factor / distance2)[:, :, None]).sum(dim=1) * k_repulsion
        attraction = torch.zeros_like(positions)
        if sources.numel():
            edge_delta = positions[sources] - positions[targets]
            edge_distance = edge_delta.norm(dim=1, keepdim=True).clamp_min(1e-4)
            # LinLog attraction: weak (logarithmic) pull keeps communities apart.
            force = edge_delta * (torch.log1p(edge_distance) / edge_distance)
            attraction.index_add_(0, sources, -force)
            attraction.index_add_(0, targets, force)
        gravity_force = -positions * (mass[:, None] * gravity)
        cooling = 1.0 - (iteration / max(iterations, 1)) * 0.9
        velocity = (repulsion + attraction + gravity_force).clamp(-10.0, 10.0)
        positions += step * cooling * velocity
        positions -= positions.mean(dim=0, keepdim=True)
    host = positions.detach().cpu().tolist()
    result = {node_id: (float(host[i][0]), float(host[i][1])) for i, node_id in enumerate(node_ids)}
    return _normalise_positions(result), {
        "implementation": "torch-cuda-forceatlas2-v1",
        "device": cuda["device"],
        "precision": "float32",
    }


def _forceatlas2_cpu_layout(graph: dict, parameters: dict) -> tuple[list[dict], dict]:
    if not _module_available("numpy"):
        raise DagError("BACKEND_UNAVAILABLE", "forceatlas2/cpu requires NumPy")
    import numpy as np

    node_ids = sorted(node["id"] for node in graph["nodes"])
    count = len(node_ids)
    if not count:
        return [], {"implementation": "numpy-forceatlas2-v1", "device": "CPU"}
    index = {node_id: i for i, node_id in enumerate(node_ids)}
    seed = int(parameters.get("seed", 17))
    iterations = max(1, min(int(parameters.get("iterations", 250)), 800))
    rng = np.random.default_rng(seed)
    angles = np.linspace(0.0, 2.0 * math.pi, count, endpoint=False)
    pos = np.stack([np.cos(angles), np.sin(angles)], axis=1) + 0.05 * rng.standard_normal((count, 2))
    deg = np.zeros(count)
    if graph["edges"]:
        src = np.array([index[edge["from"]] for edge in graph["edges"]], dtype=np.int64)
        tgt = np.array([index[edge["to"]] for edge in graph["edges"]], dtype=np.int64)
        np.add.at(deg, src, 1.0)
        np.add.at(deg, tgt, 1.0)
    else:
        src = tgt = np.empty(0, dtype=np.int64)
    mass = deg + 1.0
    k_repulsion = float(parameters.get("repulsion", 0.02))
    gravity = float(parameters.get("gravity", 0.08))
    step = float(parameters.get("step", 0.02))
    for iteration in range(iterations):
        delta = pos[:, None, :] - pos[None, :, :]
        distance2 = np.clip((delta * delta).sum(axis=2), 1e-4, None)
        mass_factor = mass[:, None] * mass[None, :]
        repulsion = (delta * (mass_factor / distance2)[:, :, None]).sum(axis=1) * k_repulsion
        attraction = np.zeros_like(pos)
        if src.size:
            edge_delta = pos[src] - pos[tgt]
            edge_distance = np.clip(np.linalg.norm(edge_delta, axis=1, keepdims=True), 1e-4, None)
            force = edge_delta * (np.log1p(edge_distance) / edge_distance)
            np.add.at(attraction, src, -force)
            np.add.at(attraction, tgt, force)
        gravity_force = -pos * (mass[:, None] * gravity)
        cooling = 1.0 - (iteration / max(iterations, 1)) * 0.9
        velocity = np.clip(repulsion + attraction + gravity_force, -10.0, 10.0)
        pos += step * cooling * velocity
        pos -= pos.mean(axis=0, keepdims=True)
    result = {node_id: (float(pos[i][0]), float(pos[i][1])) for i, node_id in enumerate(node_ids)}
    return _normalise_positions(result), {
        "implementation": "numpy-forceatlas2-v1",
        "device": "CPU",
    }


def _resolve_backend(algorithm: str, requested: str, node_count: int, parameters: dict) -> str:
    if requested not in BACKENDS:
        raise DagError("UNKNOWN_VIEW_BACKEND", f"unknown view backend {requested!r}", available=list(BACKENDS))
    if algorithm in DETERMINISTIC_LAYOUTS:
        if requested == "cuda":
            raise DagError("UNSUPPORTED_LAYOUT_BACKEND", f"{algorithm} layout is deterministic CPU work and has no CUDA implementation")
        return "cpu"
    if requested == "auto":
        threshold = max(1, int(parameters.get("cuda_min_nodes", 1000)))
        return "cuda" if node_count >= threshold and _cuda_status()["available"] else "cpu"
    return requested


def _digest_payload(view: dict) -> dict:
    payload = copy.deepcopy(view)
    payload.pop("view_id", None)
    payload.pop("content_digest", None)
    payload.pop("created_at", None)
    return payload


def view_digest(view: dict) -> str:
    return f"sha256:{object_digest(_digest_payload(view))}"


def validate_view(view: dict, *, current_revision: str | None = None) -> dict:
    errors: list[dict] = []
    required = (
        "schema_version", "view_id", "graph_id", "graph_revision", "created_at",
        "selection", "compute", "geometry", "styles", "provenance",
        "content_digest", "extensions",
    )
    for key in required:
        if key not in view:
            errors.append({"token": "MISSING_FIELD", "location": key, "message": f"missing {key}"})
    if view.get("schema_version") != VIEW_SCHEMA_VERSION:
        errors.append({"token": "BAD_SCHEMA_VERSION", "location": "schema_version", "message": "expected version 1"})
    if view.get("content_digest") and view.get("content_digest") != view_digest(view):
        errors.append({"token": "VIEW_DIGEST_MISMATCH", "location": "content_digest", "message": "derived view digest does not match content"})
    positions = view.get("geometry", {}).get("node_positions", [])
    ids = [position.get("id") for position in positions]
    if len(ids) != len(set(ids)):
        errors.append({"token": "DUPLICATE_VIEW_NODE", "location": "geometry.node_positions", "message": "node positions must be unique"})
    stale = bool(current_revision and view.get("graph_revision") != current_revision)
    return {
        "schema": VIEW_SCHEMA,
        "ok": not errors,
        "view_id": view.get("view_id"),
        "errors": errors,
        "stale": stale,
        "current_graph_revision": current_revision,
    }


def compute_view(
    algorithm: str = "layered",
    backend: str = "auto",
    filters: dict | None = None,
    parameters: dict | None = None,
    *,
    write: bool = False,
) -> dict:
    algorithm = str(algorithm).strip().lower().replace("-", "_")
    backend = str(backend).strip().lower()
    if algorithm not in LAYOUT_ALGORITHMS:
        raise DagError("UNKNOWN_LAYOUT", f"unknown layout {algorithm!r}", available=list(LAYOUT_ALGORITHMS))
    parameters = copy.deepcopy(parameters or {})
    graph = _selected_graph(filters)
    resolved = _resolve_backend(algorithm, backend, len(graph["nodes"]), parameters)
    if algorithm == "layered":
        positions, implementation = _layered_layout(graph, parameters)
    elif algorithm == "radial":
        positions, implementation = _radial_layout(graph, parameters)
    elif algorithm == "clustered":
        positions, implementation = _clustered_layout(graph, parameters)
    elif algorithm == "circular":
        positions, implementation = _circular_layout(graph, parameters)
    elif algorithm == "forceatlas2":
        positions, implementation = (_forceatlas2_cuda_layout(graph, parameters) if resolved == "cuda"
                                     else _forceatlas2_cpu_layout(graph, parameters))
    elif resolved == "cuda":
        positions, implementation = _spring_cuda_layout(graph, parameters)
    else:
        positions, implementation = _spring_cpu_layout(graph, parameters)
    view: dict[str, Any] = {
        "schema_version": VIEW_SCHEMA_VERSION,
        "view_id": "pending",
        "graph_id": graph["graph_id"],
        "graph_revision": graph["revision"],
        "created_at": _utc_now(),
        "selection": {
            "filters": copy.deepcopy(filters or {}),
            "node_ids": sorted(node["id"] for node in graph["nodes"]),
            "edge_ids": sorted(edge["id"] for edge in graph["edges"]),
        },
        "compute": {
            "algorithm": algorithm,
            "backend_requested": backend,
            "backend_resolved": resolved,
            "parameters": parameters,
            **implementation,
        },
        "geometry": {
            "dimensions": 2,
            "coordinate_space": "normalised-unit-square",
            "node_positions": positions,
            "edge_routes": [],
        },
        "styles": {"node_scalars": {}, "node_groups": {}, "extensions": {}},
        "provenance": {
            "generator": VIEW_SCHEMA,
            "canonical_graph_path": str(dag_root() / "canonical" / "theorem-dag.json"),
            "authority": "derived-nonauthoritative",
        },
        "content_digest": "pending",
        "extensions": {},
    }
    digest = view_digest(view)
    view["content_digest"] = digest
    view["view_id"] = f"{graph['graph_id']}:view:{digest[7:23]}"
    validation = validate_view(view, current_revision=graph["revision"])
    if not validation["ok"]:
        raise DagError("INVALID_DERIVED_VIEW", "computed view failed validation", validation=validation)
    path = None
    if write:
        directory = derived_view_root() / graph["revision"][7:23]
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{digest[7:]}.view.json"
        if not path.exists():
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=directory, delete=False) as handle:
                json.dump(view, handle, indent=2, ensure_ascii=False)
                handle.write("\n")
                temp_path = Path(handle.name)
            temp_path.replace(path)
    return {
        "schema": VIEW_SCHEMA,
        "ok": True,
        "view": view,
        "written": bool(write),
        "path": str(path) if path else None,
        "counts": {"nodes": len(graph["nodes"]), "edges": len(graph["edges"])},
    }


def list_views(*, include_stale: bool = True) -> dict:
    graph = load_graph()
    records: list[dict] = []
    root = derived_view_root()
    for path in sorted(root.glob("*/*.view.json")) if root.exists() else []:
        try:
            view = json.loads(path.read_text(encoding="utf-8"))
            validation = validate_view(view, current_revision=graph["revision"])
        except (OSError, json.JSONDecodeError) as exc:
            records.append({"path": str(path), "ok": False, "error": str(exc)})
            continue
        if include_stale or not validation["stale"]:
            records.append({
                "path": str(path),
                "ok": validation["ok"],
                "stale": validation["stale"],
                "view_id": view.get("view_id"),
                "content_digest": view.get("content_digest"),
                "graph_revision": view.get("graph_revision"),
                "algorithm": view.get("compute", {}).get("algorithm"),
                "backend": view.get("compute", {}).get("backend_resolved"),
                "counts": {
                    "nodes": len(view.get("selection", {}).get("node_ids", [])),
                    "edges": len(view.get("selection", {}).get("edge_ids", [])),
                },
            })
    return {
        "schema": VIEW_SCHEMA,
        "ok": True,
        "current_graph_revision": graph["revision"],
        "count": len(records),
        "views": records,
    }


def get_view(identifier: str) -> dict:
    identifier = str(identifier).strip()
    graph = load_graph()
    matches: list[Path] = []
    root = derived_view_root()
    if root.exists():
        for path in root.glob("*/*.view.json"):
            if identifier in {path.name, path.stem, path.name.split(".", 1)[0]}:
                matches.append(path)
                continue
            try:
                candidate = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if identifier in {candidate.get("view_id"), candidate.get("content_digest")}:
                matches.append(path)
    if not matches:
        raise DagError("VIEW_NOT_FOUND", f"unknown derived view {identifier!r}")
    if len(matches) > 1:
        raise DagError("AMBIGUOUS_VIEW", f"derived view identifier {identifier!r} is ambiguous")
    path = matches[0]
    view = json.loads(path.read_text(encoding="utf-8"))
    return {
        "schema": VIEW_SCHEMA,
        "ok": True,
        "path": str(path),
        "view": view,
        "validation": validate_view(view, current_revision=graph["revision"]),
    }
