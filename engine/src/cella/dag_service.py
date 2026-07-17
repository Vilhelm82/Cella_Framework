"""Renderer-neutral, revisioned research-DAG service.

This module is organizational tooling, not a mathematical verdict path. It uses
only the standard library. DAG records stay inside ``DAG_Library``; a successful
apply additionally creates a path-scoped local Git commit for the declared source
files and transaction records. The canonical JSON graph is authoritative; MCP,
CLI, DOT, GraphML and Cytoscape are adapters over the same record.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
import tempfile
from collections import defaultdict, deque
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


SERVICE_SCHEMA = "cella-dag-service-v1"
GRAPH_DIRECTION = "from is the grammatical subject: from -relation-> to"
MAX_QUERY_LIMIT = 500


class DagError(ValueError):
    def __init__(self, token: str, message: str, **details):
        super().__init__(message)
        self.token = token
        self.message = message
        self.details = details

    def record(self) -> dict:
        return {
            "schema": SERVICE_SCHEMA,
            "ok": False,
            "error": {"token": self.token, "message": self.message},
            **self.details,
        }


def repository_root() -> Path:
    override = os.environ.get("CELLA_REPOSITORY_ROOT")
    return Path(override).resolve() if override else Path(__file__).resolve().parents[3]


def dag_root() -> Path:
    override = os.environ.get("CELLA_DAG_ROOT")
    return Path(override).resolve() if override else repository_root() / "DAG_Library"


def canonical_graph_path() -> Path:
    return dag_root() / "canonical" / "theorem-dag.json"


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DagError("DAG_NOT_INITIALIZED", f"missing DAG record: {path}", path=str(path)) from exc
    except json.JSONDecodeError as exc:
        raise DagError("INVALID_JSON", f"invalid JSON in {path}: {exc}", path=str(path)) from exc


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def object_digest(value) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def graph_revision(graph: dict) -> str:
    payload = copy.deepcopy(graph)
    payload.pop("revision", None)
    return f"sha256:{object_digest(payload)}"


def normalize_graph(graph: dict) -> dict:
    out = copy.deepcopy(graph)
    out.setdefault("schema_version", 1)
    out.setdefault("direction", GRAPH_DIRECTION)
    out.setdefault("authority_policy", "The DAG indexes provenance and declared relations; it does not promote documentary labels into mathematical authority.")
    out.setdefault("extensions", {})
    out["nodes"] = sorted(out.get("nodes", []), key=lambda node: node.get("id", ""))
    out["edges"] = sorted(out.get("edges", []), key=lambda edge: edge.get("id", ""))
    out["revision"] = graph_revision(out)
    return out


def canonical_graph_for_diff(graph: dict) -> dict:
    """Deterministic semantic graph form used by rebuild-survival gates.

    Build provenance and the revision digest are deliberately excluded: they
    describe how a graph was materialized, while this comparison proves that
    the complete node/edge content survives rebuilding from registered sources.
    """
    normalized = normalize_graph(graph)
    return {
        "schema_version": normalized["schema_version"],
        "graph_id": normalized["graph_id"],
        "direction": normalized["direction"],
        "authority_policy": normalized["authority_policy"],
        "nodes": normalized["nodes"],
        "edges": normalized["edges"],
    }


def load_graph() -> dict:
    return _read_json(canonical_graph_path())


def _registry() -> tuple[dict, dict]:
    base = repository_root() / "Artifact_Schemas"
    return _read_json(base / "SCHEMA_REGISTRY.json"), _read_json(base / "RELATION_REGISTRY.json")


def schema_record(name: str = "registry") -> dict:
    base = repository_root() / "Artifact_Schemas"
    routes = {
        "registry": base / "SCHEMA_REGISTRY.json",
        "relations": base / "RELATION_REGISTRY.json",
        "artifact": base / "schemas" / "artifact.schema.json",
        "dag": base / "schemas" / "dag.schema.json",
        "derived_view": base / "schemas" / "derived-view.schema.json",
        "submission": base / "schemas" / "submission.schema.json",
        "campaign_families": base / "CAMPAIGN_FAMILY_MAP.json",
    }
    key = str(name).strip().lower()
    if key not in routes:
        raise DagError("UNKNOWN_SCHEMA", f"unknown schema {name!r}", available=sorted(routes))
    return {
        "schema": SERVICE_SCHEMA,
        "ok": True,
        "name": key,
        "path": str(routes[key]),
        "document": _read_json(routes[key]),
    }


def _issue(token: str, location: str, message: str) -> dict:
    return {"token": token, "location": location, "message": message}


def _cycle_nodes(nodes: set[str], edges: list[dict]) -> list[str]:
    outgoing: dict[str, list[str]] = defaultdict(list)
    indegree = {node_id: 0 for node_id in nodes}
    for edge in edges:
        if edge.get("from") in nodes and edge.get("to") in nodes:
            outgoing[edge["from"]].append(edge["to"])
            indegree[edge["to"]] += 1
    queue = deque(sorted(node_id for node_id, degree in indegree.items() if degree == 0))
    seen: set[str] = set()
    while queue:
        node_id = queue.popleft()
        seen.add(node_id)
        for target in outgoing[node_id]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return sorted(nodes - seen)


def validate_graph(graph: dict | None = None, *, verify_files: bool = False) -> dict:
    graph = load_graph() if graph is None else graph
    schema_registry, relation_registry = _registry()
    errors: list[dict] = []
    warnings: list[dict] = []
    required_root = ("schema_version", "graph_id", "revision", "direction", "authority_policy", "nodes", "edges", "extensions")
    for key in required_root:
        if key not in graph:
            errors.append(_issue("MISSING_FIELD", key, f"required root field {key!r} is absent"))
    if graph.get("direction") != GRAPH_DIRECTION:
        errors.append(_issue("BAD_DIRECTION", "direction", f"direction must be {GRAPH_DIRECTION!r}"))
    if graph.get("revision") != graph_revision(graph):
        errors.append(_issue("REVISION_MISMATCH", "revision", "stored revision does not match canonical graph content"))

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    ids: set[str] = set()
    node_required = ("id", "label", "type", "claim_status", "lifecycle_status", "reachability", "tracked", "layer", "summary", "source_refs", "external_ids", "facets", "visual_hints", "retrieval", "extensions")
    allowed_types = set(schema_registry["artifact_types"])
    allowed_claims = set(schema_registry["claim_statuses"])
    allowed_lifecycle = set(schema_registry["lifecycle_statuses"])
    allowed_reachability = set(schema_registry["reachability_values"])
    repo = repository_root()
    for index, node in enumerate(nodes):
        location = f"nodes[{index}]"
        node_id = node.get("id")
        for key in node_required:
            if key not in node:
                errors.append(_issue("MISSING_FIELD", f"{location}.{key}", f"required node field {key!r} is absent"))
        if not isinstance(node_id, str) or not node_id:
            errors.append(_issue("BAD_NODE_ID", f"{location}.id", "node id must be a non-empty string"))
        elif node_id in ids:
            errors.append(_issue("DUPLICATE_NODE_ID", f"{location}.id", f"duplicate node id {node_id!r}"))
        else:
            ids.add(node_id)
        if node.get("type") not in allowed_types:
            errors.append(_issue("UNKNOWN_NODE_TYPE", f"{location}.type", f"unregistered node type {node.get('type')!r}"))
        if node.get("claim_status") is not None and node.get("claim_status") not in allowed_claims:
            errors.append(_issue("UNKNOWN_CLAIM_STATUS", f"{location}.claim_status", "claim status is not registered"))
        if node.get("lifecycle_status") is not None and node.get("lifecycle_status") not in allowed_lifecycle:
            errors.append(_issue("UNKNOWN_LIFECYCLE_STATUS", f"{location}.lifecycle_status", "lifecycle status is not registered"))
        if node.get("reachability") is not None and node.get("reachability") not in allowed_reachability:
            errors.append(_issue("UNKNOWN_REACHABILITY", f"{location}.reachability", "reachability is not registered"))
        retrieval = node.get("retrieval", {})
        for key in ("key_terms", "retrieval_questions", "context_priority", "context_role"):
            if key not in retrieval:
                errors.append(_issue("MISSING_RETRIEVAL_FIELD", f"{location}.retrieval.{key}", f"retrieval field {key!r} is required"))
        if retrieval.get("context_priority") not in {"low", "normal", "high", "critical"}:
            errors.append(_issue("BAD_CONTEXT_PRIORITY", f"{location}.retrieval.context_priority", "context priority is not registered"))
        if retrieval.get("context_role") not in {"core", "supporting", "historical", "frontier"}:
            errors.append(_issue("BAD_CONTEXT_ROLE", f"{location}.retrieval.context_role", "context role is not registered"))
        for namespace, values in node.get("external_ids", {}).items():
            if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
                errors.append(_issue("BAD_EXTERNAL_IDS", f"{location}.external_ids.{namespace}", "external id namespaces must contain arrays of strings"))
        for ref_index, ref in enumerate(node.get("source_refs", [])):
            pointer = ref.get("pointer") if isinstance(ref, dict) else None
            sha256 = ref.get("sha256") if isinstance(ref, dict) else None
            ref_loc = f"{location}.source_refs[{ref_index}]"
            if not pointer:
                errors.append(_issue("BAD_SOURCE_REF", ref_loc, "source reference requires a pointer"))
                continue
            if sha256 is not None and not re.fullmatch(r"[0-9a-f]{64}", str(sha256)):
                errors.append(_issue("BAD_SHA256", f"{ref_loc}.sha256", "sha256 must be 64 lowercase hexadecimal characters or null"))
            if verify_files and pointer.startswith("cella:"):
                file_path = pointer.split(":", 1)[1].split("#", 1)[0]
                resolved = repo / file_path
                if not resolved.is_file():
                    errors.append(_issue("SOURCE_MISSING", ref_loc, f"source file does not exist: {resolved}"))
                elif sha256 and hashlib.sha256(resolved.read_bytes()).hexdigest() != sha256:
                    errors.append(_issue("SOURCE_DIGEST_MISMATCH", ref_loc, f"source digest does not match: {resolved}"))
            if sha256 is None:
                warnings.append(_issue("UNBOUND_SOURCE", ref_loc, "source pointer has no content digest"))

    edge_ids: set[str] = set()
    triples: set[tuple[str, str, str]] = set()
    relation_records = relation_registry["relations"]
    acyclic_edges: list[dict] = []
    edge_required = ("id", "from", "to", "relation", "label", "basis", "source_refs", "facets", "extensions")
    for index, edge in enumerate(edges):
        location = f"edges[{index}]"
        for key in edge_required:
            if key not in edge:
                errors.append(_issue("MISSING_FIELD", f"{location}.{key}", f"required edge field {key!r} is absent"))
        edge_id = edge.get("id")
        if not edge_id:
            errors.append(_issue("BAD_EDGE_ID", f"{location}.id", "edge id must be a non-empty string"))
        elif edge_id in edge_ids:
            errors.append(_issue("DUPLICATE_EDGE_ID", f"{location}.id", f"duplicate edge id {edge_id!r}"))
        else:
            edge_ids.add(edge_id)
        if edge.get("from") not in ids or edge.get("to") not in ids:
            errors.append(_issue("DANGLING_EDGE", location, "edge endpoint is not a known node id"))
        if edge.get("from") == edge.get("to"):
            errors.append(_issue("SELF_EDGE", location, "self edges are not admitted"))
        relation = edge.get("relation")
        if relation not in relation_records:
            errors.append(_issue("UNKNOWN_RELATION", f"{location}.relation", f"unregistered relation {relation!r}"))
        elif relation_records[relation].get("acyclic"):
            acyclic_edges.append(edge)
        triple = (edge.get("from"), edge.get("to"), relation)
        if triple in triples:
            errors.append(_issue("DUPLICATE_EDGE", location, f"duplicate relation triple {triple!r}"))
        triples.add(triple)
        for ref_index, ref in enumerate(edge.get("source_refs", [])):
            pointer = ref.get("pointer") if isinstance(ref, dict) else None
            sha256 = ref.get("sha256") if isinstance(ref, dict) else None
            ref_loc = f"{location}.source_refs[{ref_index}]"
            if not pointer:
                errors.append(_issue("BAD_SOURCE_REF", ref_loc, "edge source reference requires a pointer"))
                continue
            if sha256 is not None and not re.fullmatch(r"[0-9a-f]{64}", str(sha256)):
                errors.append(_issue("BAD_SHA256", f"{ref_loc}.sha256", "sha256 must be 64 lowercase hexadecimal characters or null"))
            if verify_files and pointer.startswith("cella:"):
                file_path = pointer.split(":", 1)[1].split("#", 1)[0]
                resolved = repo / file_path
                if not resolved.is_file():
                    errors.append(_issue("SOURCE_MISSING", ref_loc, f"edge source file does not exist: {resolved}"))
                elif sha256 and hashlib.sha256(resolved.read_bytes()).hexdigest() != sha256:
                    errors.append(_issue("SOURCE_DIGEST_MISMATCH", ref_loc, f"edge source digest does not match: {resolved}"))
            if sha256 is None:
                warnings.append(_issue("UNBOUND_SOURCE", ref_loc, "edge source pointer has no content digest"))
    cycle = _cycle_nodes(ids, acyclic_edges)
    if cycle:
        errors.append(_issue("ACYCLIC_RELATION_CYCLE", "edges", f"acyclic relations contain a cycle through {cycle}"))
    return {
        "schema": SERVICE_SCHEMA,
        "ok": not errors,
        "graph_id": graph.get("graph_id"),
        "revision": graph.get("revision"),
        "counts": {"nodes": len(nodes), "edges": len(edges), "errors": len(errors), "warnings": len(warnings)},
        "errors": errors,
        "warnings": warnings,
    }


def validate_artifact(artifact: dict, *, verify_files: bool = False) -> dict:
    schema_registry, relation_registry = _registry()
    errors: list[dict] = []
    warnings: list[dict] = []
    required = ("schema_version", "artifact_id", "artifact_type", "title", "summary", "subject_families", "claim_status", "lifecycle_status", "files", "claims", "relations", "external_ids", "declared_impacts", "llm", "extensions")
    for key in required:
        if key not in artifact:
            errors.append(_issue("MISSING_FIELD", key, f"required artifact field {key!r} is absent"))
    if artifact.get("artifact_type") not in schema_registry["artifact_types"]:
        errors.append(_issue("UNKNOWN_ARTIFACT_TYPE", "artifact_type", "artifact type is not registered"))
    if artifact.get("claim_status") is not None and artifact.get("claim_status") not in schema_registry["claim_statuses"]:
        errors.append(_issue("UNKNOWN_CLAIM_STATUS", "claim_status", "claim status is not registered"))
    if artifact.get("lifecycle_status") not in schema_registry["lifecycle_statuses"]:
        errors.append(_issue("UNKNOWN_LIFECYCLE_STATUS", "lifecycle_status", "lifecycle status is not registered"))
    if artifact.get("artifact_type") == "theorem" and not artifact.get("claims"):
        errors.append(_issue("THEOREM_WITHOUT_CLAIM", "claims", "theorem artifacts require at least one exact claim"))
    for index, relation in enumerate(artifact.get("relations", [])):
        if relation.get("relation") not in relation_registry["relations"]:
            errors.append(_issue("UNKNOWN_RELATION", f"relations[{index}].relation", "relation is not registered"))
    base = repository_root()
    for index, file_record in enumerate(artifact.get("files", [])):
        digest = file_record.get("sha256", "")
        if not re.fullmatch(r"[0-9a-f]{64}", str(digest)):
            errors.append(_issue("BAD_SHA256", f"files[{index}].sha256", "file digest must be lowercase SHA-256"))
        if verify_files and file_record.get("path"):
            path = base / file_record["path"]
            if not path.is_file():
                errors.append(_issue("SOURCE_MISSING", f"files[{index}].path", f"file does not exist: {path}"))
            elif digest and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                errors.append(_issue("SOURCE_DIGEST_MISMATCH", f"files[{index}].sha256", f"digest does not match: {path}"))
    llm = artifact.get("llm", {})
    for key in ("one_sentence_purpose", "key_terms", "retrieval_questions", "context_priority", "context_role"):
        if key not in llm:
            errors.append(_issue("MISSING_LLM_FIELD", f"llm.{key}", f"LLM retrieval field {key!r} is required"))
    return {
        "schema": SERVICE_SCHEMA,
        "ok": not errors,
        "artifact_id": artifact.get("artifact_id"),
        "errors": errors,
        "warnings": warnings,
    }


def _node_index(graph: dict) -> dict[str, dict]:
    return {node["id"]: node for node in graph["nodes"]}


def dag_status() -> dict:
    graph = load_graph()
    validation = validate_graph(graph)
    type_counts: dict[str, int] = defaultdict(int)
    layer_counts: dict[str, int] = defaultdict(int)
    tracked = 0
    for node in graph["nodes"]:
        type_counts[node["type"]] += 1
        layer_counts[node["layer"]] += 1
        tracked += int(node["tracked"])
    return {
        "schema": SERVICE_SCHEMA,
        "ok": validation["ok"],
        "graph_id": graph["graph_id"],
        "revision": graph["revision"],
        "counts": {"nodes": len(graph["nodes"]), "edges": len(graph["edges"]), "tracked": tracked},
        "node_types": dict(sorted(type_counts.items())),
        "layers": dict(sorted(layer_counts.items())),
        "validation": validation["counts"],
        "paths": {"graph": str(canonical_graph_path()), "schemas": str(repository_root() / "Artifact_Schemas")},
    }


def get_node(node_id: str, *, direction: str = "both", depth: int = 1) -> dict:
    graph = load_graph()
    nodes = _node_index(graph)
    if node_id not in nodes:
        raise DagError("NODE_NOT_FOUND", f"unknown DAG node {node_id!r}", node_id=node_id)
    if direction not in {"in", "out", "both"}:
        raise DagError("BAD_DIRECTION", "direction must be in, out, or both")
    depth = max(0, min(int(depth), 5))
    frontier = {node_id}
    visited = {node_id}
    selected_edges: list[dict] = []
    for _ in range(depth):
        next_frontier: set[str] = set()
        for edge in graph["edges"]:
            take = False
            if direction in {"out", "both"} and edge["from"] in frontier:
                next_frontier.add(edge["to"]); take = True
            if direction in {"in", "both"} and edge["to"] in frontier:
                next_frontier.add(edge["from"]); take = True
            if take and edge not in selected_edges:
                selected_edges.append(edge)
        next_frontier -= visited
        visited |= next_frontier
        frontier = next_frontier
    return {
        "schema": SERVICE_SCHEMA,
        "ok": True,
        "graph_id": graph["graph_id"],
        "revision": graph["revision"],
        "node": nodes[node_id],
        "neighbors": [nodes[item] for item in sorted(visited - {node_id})],
        "edges": sorted(selected_edges, key=lambda edge: edge["id"]),
    }


TEXT_SUFFIXES = {".md", ".tex", ".txt", ".py", ".m2", ".json", ".jsonl", ".csv", ".tsv", ".out", ".pin", ".html"}
SOURCE_MAX_BYTES = 1_000_000


def _resolve_source_path(pointer: str) -> Path | None:
    """Resolve a 'cella:'/'encyclopedia:' pointer to a real file path, guarded to its repo root."""
    scheme, sep, rest = pointer.partition(":")
    if not sep:
        return None
    rest = rest.split("#", 1)[0]
    if scheme == "cella":
        base = repository_root()
    elif scheme == "encyclopedia":
        base = repository_root().parent / "Lloyd_Mathematics_Encyclopedia"
    else:
        return None
    base = base.resolve()
    candidate = (base / rest).resolve()
    if candidate != base and base not in candidate.parents:
        return None
    return candidate


def _source_connections(raw_pointer_base: str, file_sha: str | None, *, max_items: int = MAX_QUERY_LIMIT) -> dict:
    """Every node backed by the same file (matched by pointer base or content sha) plus incident edges."""
    graph = load_graph()
    backing: list[dict] = []
    backing_ids: set[str] = set()
    for node in graph["nodes"]:
        for ref in node.get("source_refs") or []:
            ref_pointer = (ref.get("pointer") or "").split("#", 1)[0]
            if ref_pointer == raw_pointer_base or (file_sha and ref.get("sha256") == file_sha):
                backing_ids.add(node["id"])
                backing.append({
                    "id": node["id"], "label": node["label"], "type": node["type"],
                    "claim_status": node["claim_status"], "lifecycle_status": node["lifecycle_status"],
                    "layer": node["layer"], "reachability": node["reachability"], "source_id": _node_source(node),
                })
                break
    edges = [
        {"id": edge["id"], "from": edge["from"], "to": edge["to"], "relation": edge["relation"], "label": edge.get("label")}
        for edge in graph["edges"] if edge["from"] in backing_ids or edge["to"] in backing_ids
    ]
    contained: set[str] = set()
    for node in graph["nodes"]:
        if node["id"] in backing_ids:
            contained |= set((node.get("external_ids") or {}).get("encyclopedia", []))
    relation_counts: dict[str, int] = {}
    for edge in edges:
        relation_counts[edge["relation"]] = relation_counts.get(edge["relation"], 0) + 1
    return {
        "counts": {"backing_nodes": len(backing), "incident_edges": len(edges), "contained_units": len(contained)},
        "backing_nodes": backing[:max_items],
        "incident_edges": edges[:max_items],
        "relation_counts": relation_counts,
        "contained_encyclopedia_ids": sorted(contained),
        "truncated": len(backing) > max_items or len(edges) > max_items,
    }


def fetch_source(pointer: str | None = None, node_id: str | None = None, *, max_bytes: int = SOURCE_MAX_BYTES, include_connections: bool = False) -> dict:
    """Return the full text of the file behind a pointer or a node's first source_ref.

    Read-only. Resolves 'cella:'/'encyclopedia:' pointers under their repo roots
    (path-traversal guarded), reports the live sha256 and whether it matches the
    node's declared digest, and declines to return binary payloads as text. When
    include_connections is true, also returns every node backed by the same file
    (matched by pointer base or content sha), the edges incident to that set, and
    the union of encyclopedia unit ids those nodes contain.
    """
    declared_sha = None
    if not pointer and node_id:
        node = _node_index(load_graph()).get(node_id)
        if node is None:
            raise DagError("UNKNOWN_NODE", f"no node with id {node_id!r}")
        refs = node.get("source_refs") or []
        if not refs or not refs[0].get("pointer"):
            raise DagError("NO_SOURCE", f"node {node_id!r} has no source_refs pointer")
        pointer = refs[0]["pointer"]
        declared_sha = refs[0].get("sha256")
    if not pointer:
        raise DagError("NO_POINTER", "provide a pointer or a node_id")
    anchor_line = None
    if "#" in pointer:
        frag = pointer.split("#", 1)[1]
        if frag[:1].upper() == "L" and frag[1:].isdigit():
            anchor_line = int(frag[1:])
    path = _resolve_source_path(pointer)
    if path is None:
        raise DagError("BAD_POINTER", f"pointer {pointer!r} does not resolve inside a known repository root")
    base = {"schema": SERVICE_SCHEMA, "pointer": pointer, "node_id": node_id, "anchor_line": anchor_line}
    if not path.is_file():
        return {**base, "ok": False, "exists": False, "error": {"token": "SOURCE_MISSING", "message": f"source file does not exist: {path}"}}
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    suffix = path.suffix.lower()
    try:
        resolved_path = str(path.relative_to(repository_root()))
    except ValueError:
        resolved_path = str(path)
    result = {
        **base, "ok": True, "exists": True, "resolved_path": resolved_path, "bytes": len(data),
        "sha256": digest, "declared_sha256": declared_sha,
        "sha256_matches_declared": (declared_sha is None or str(declared_sha) == digest),
        "is_text": suffix in TEXT_SUFFIXES, "truncated": False, "content": None,
    }
    if suffix not in TEXT_SUFFIXES:
        result["note"] = f"binary/non-text file ({suffix or 'no suffix'}); content not returned"
    elif len(data) > max_bytes:
        result["truncated"] = True
        result["content"] = data[:max_bytes].decode("utf-8", errors="replace")
    else:
        result["content"] = data.decode("utf-8", errors="replace")
    if include_connections:
        result["connections"] = _source_connections(pointer.split("#", 1)[0], digest)
    return result


def _node_source(node: dict) -> str | None:
    """Return the source_id a node was compiled from (facets, then extensions)."""
    facets = node.get("facets") or {}
    if facets.get("source_id"):
        return str(facets["source_id"])
    extensions = node.get("extensions") or {}
    return str(extensions["source_id"]) if extensions.get("source_id") else None


def query_nodes(filters: dict | None = None, *, edge_mode: str = "induced", limit: int = 100, cursor: int = 0) -> dict:
    graph = load_graph()
    filters = filters or {}
    if edge_mode not in {"none", "induced", "incident"}:
        raise DagError("BAD_EDGE_MODE", "edge_mode must be none, induced, or incident")
    limit = max(1, min(int(limit), MAX_QUERY_LIMIT))
    cursor = max(0, int(cursor))

    def values(key: str) -> set[str]:
        raw = filters.get(key, [])
        if isinstance(raw, str): raw = [raw]
        return {str(item) for item in raw}

    ids = values("ids"); types = values("types"); claims = values("claim_statuses")
    lifecycles = values("lifecycle_statuses"); layers = values("layers")
    reachability = values("reachability"); external_ids = values("external_ids")
    source_ids = values("source_ids"); edge_relations = values("edge_relations")
    cross_source = filters.get("cross_source")
    tracked = filters.get("tracked")
    text_query = str(filters.get("text", "")).strip().lower()
    matched: list[dict] = []
    for node in graph["nodes"]:
        if ids and node["id"] not in ids: continue
        if types and node["type"] not in types: continue
        if claims and str(node["claim_status"]) not in claims: continue
        if lifecycles and str(node["lifecycle_status"]) not in lifecycles: continue
        if layers and node["layer"] not in layers: continue
        if reachability and str(node["reachability"]) not in reachability: continue
        if source_ids and _node_source(node) not in source_ids: continue
        if tracked is not None and bool(node["tracked"]) != bool(tracked): continue
        flat_external = {item for group in node["external_ids"].values() for item in group}
        if external_ids and not (external_ids & flat_external): continue
        if text_query:
            haystack = " ".join([node["id"], node["label"], node["summary"], json.dumps(node["facets"], ensure_ascii=False), json.dumps(node["retrieval"], ensure_ascii=False)]).lower()
            if text_query not in haystack: continue
        matched.append(node)
    page = matched[cursor:cursor + limit]
    page_ids = {node["id"] for node in page}
    edges: list[dict] = []
    if edge_mode == "induced":
        edges = [edge for edge in graph["edges"] if edge["from"] in page_ids and edge["to"] in page_ids]
    elif edge_mode == "incident":
        edges = [edge for edge in graph["edges"] if edge["from"] in page_ids or edge["to"] in page_ids]
    if edge_relations:
        edges = [edge for edge in edges if edge["relation"] in edge_relations]
    if cross_source is not None:
        source_by_id = {node["id"]: _node_source(node) for node in graph["nodes"]}
        def _is_cross(edge: dict) -> bool:
            left = source_by_id.get(edge["from"]); right = source_by_id.get(edge["to"])
            return left is not None and right is not None and left != right
        edges = [edge for edge in edges if _is_cross(edge) == bool(cross_source)]
    next_cursor = cursor + len(page) if cursor + len(page) < len(matched) else None
    return {
        "schema": SERVICE_SCHEMA,
        "ok": True,
        "graph_id": graph["graph_id"],
        "revision": graph["revision"],
        "query": {"filters": filters, "edge_mode": edge_mode, "limit": limit, "cursor": cursor},
        "counts": {"matched": len(matched), "returned_nodes": len(page), "returned_edges": len(edges)},
        "next_cursor": next_cursor,
        "nodes": page,
        "edges": edges,
    }


def impact_analysis(changed_node_ids: list[str] | None = None, changed_source_sha256s: list[str] | None = None, *, max_depth: int = 8, _graph: dict | None = None) -> dict:
    graph = load_graph() if _graph is None else _graph
    _, relation_registry = _registry()
    nodes = _node_index(graph)
    seeds = set(changed_node_ids or [])
    digests = set(changed_source_sha256s or [])
    for node in graph["nodes"]:
        if any(ref.get("sha256") in digests for ref in node["source_refs"]):
            seeds.add(node["id"])
    unknown = sorted(seeds - set(nodes))
    if unknown:
        raise DagError("NODE_NOT_FOUND", "one or more changed nodes are unknown", unknown_node_ids=unknown)
    max_depth = max(0, min(int(max_depth), 32))
    reasons: dict[str, list[dict]] = {seed: [{"depth": 0, "reason": "direct change", "via": None}] for seed in seeds}
    queue = deque((seed, 0) for seed in sorted(seeds))
    while queue:
        current, depth = queue.popleft()
        if depth >= max_depth: continue
        for edge in graph["edges"]:
            policy = relation_registry["relations"][edge["relation"]]["impact"]
            candidates: list[tuple[str, str]] = []
            if edge["from"] == current and policy.get("from_to"):
                candidates.append((edge["to"], "from_to"))
            if edge["to"] == current and policy.get("to_from"):
                candidates.append((edge["from"], "to_from"))
            for candidate, traversal in candidates:
                record = {"depth": depth + 1, "reason": edge["relation"], "via": edge["id"], "traversal": traversal, "from_changed": current}
                if candidate not in reasons:
                    reasons[candidate] = [record]
                    queue.append((candidate, depth + 1))
                elif record not in reasons[candidate]:
                    reasons[candidate].append(record)
    affected_ids = sorted(set(reasons) - seeds)
    reevaluate_files = sorted({ref["pointer"] for node_id in affected_ids for ref in nodes[node_id]["source_refs"]})
    return {
        "schema": SERVICE_SCHEMA,
        "ok": True,
        "graph_id": graph["graph_id"],
        "revision": graph["revision"],
        "seeds": sorted(seeds),
        "affected_node_count": len(affected_ids),
        "affected_nodes": [{"id": node_id, "label": nodes[node_id]["label"], "reasons": reasons[node_id]} for node_id in affected_ids],
        "reevaluate_files": reevaluate_files,
        "scope_note": "This is the explicit relation closure. Undeclared semantic consequences still require review.",
    }


def _validate_submission(submission: dict, graph: dict) -> dict:
    errors: list[dict] = []
    required = ("schema_version", "submission_id", "base_revision", "idempotency_key", "submitted_by", "summary", "artifacts", "graph_delta", "declared_impacts", "extensions")
    for key in required:
        if key not in submission:
            errors.append(_issue("MISSING_FIELD", key, f"required submission field {key!r} is absent"))
    if submission.get("base_revision") != graph.get("revision"):
        errors.append(_issue("STALE_BASE_REVISION", "base_revision", "submission base revision does not match the current graph"))
    if len(str(submission.get("idempotency_key", ""))) < 8:
        errors.append(_issue("BAD_IDEMPOTENCY_KEY", "idempotency_key", "idempotency key must contain at least eight characters"))
    delta = submission.get("graph_delta", {})
    for key in ("upsert_nodes", "upsert_edges", "retire_nodes", "remove_edges"):
        if not isinstance(delta.get(key), list):
            errors.append(_issue("BAD_DELTA", f"graph_delta.{key}", f"{key} must be an array"))
    artifact_results = [validate_artifact(artifact) for artifact in submission.get("artifacts", [])]
    for index, result in enumerate(artifact_results):
        for issue in result["errors"]:
            errors.append(_issue(issue["token"], f"artifacts[{index}].{issue['location']}", issue["message"]))
    artifacts = submission.get("artifacts", [])
    artifact_ids = {artifact.get("artifact_id") for artifact in artifacts if artifact.get("artifact_id")}
    artifact_digests = {file_record.get("sha256") for artifact in artifacts for file_record in artifact.get("files", []) if file_record.get("sha256")}
    existing_nodes = _node_index(graph)
    known_digests = {
        ref.get("sha256")
        for record in list(graph.get("nodes", [])) + list(graph.get("edges", []))
        for ref in record.get("source_refs", [])
        if ref.get("sha256")
    }
    for index, node in enumerate(delta.get("upsert_nodes", [])):
        node_id = node.get("id")
        old_digests = {ref.get("sha256") for ref in existing_nodes.get(node_id, {}).get("source_refs", []) if ref.get("sha256")}
        new_digests = {ref.get("sha256") for ref in node.get("source_refs", []) if ref.get("sha256")}
        introduces_material = node_id not in existing_nodes or bool(new_digests - old_digests)
        linked_artifacts = set(node.get("external_ids", {}).get("artifacts", []))
        if introduces_material and not ((linked_artifacts & artifact_ids) or (new_digests & artifact_digests)):
            errors.append(_issue(
                "ARTIFACT_SIDECAR_REQUIRED",
                f"graph_delta.upsert_nodes[{index}]",
                "new nodes or source digests require a matching validated artifact sidecar by id or SHA-256",
            ))
    for index, edge in enumerate(delta.get("upsert_edges", [])):
        new_edge_digests = {ref.get("sha256") for ref in edge.get("source_refs", []) if ref.get("sha256")} - known_digests
        if new_edge_digests and not (new_edge_digests & artifact_digests):
            errors.append(_issue(
                "ARTIFACT_SIDECAR_REQUIRED",
                f"graph_delta.upsert_edges[{index}].source_refs",
                "new edge source digests require a matching artifact sidecar file digest",
            ))
    return {"ok": not errors, "errors": errors, "artifact_results": artifact_results}


def _apply_delta(graph: dict, delta: dict) -> tuple[dict, dict]:
    out = copy.deepcopy(graph)
    nodes = _node_index(out)
    edges = {edge["id"]: edge for edge in out["edges"]}
    changed_nodes: set[str] = set()
    changes = {"nodes_added": [], "nodes_updated": [], "nodes_retired": [], "edges_added": [], "edges_updated": [], "edges_removed": []}
    for node in delta.get("upsert_nodes", []):
        node_id = node.get("id")
        if not node_id:
            raise DagError("BAD_NODE_ID", "upsert node is missing id")
        bucket = "nodes_updated" if node_id in nodes else "nodes_added"
        nodes[node_id] = copy.deepcopy(node); changes[bucket].append(node_id); changed_nodes.add(node_id)
    for node_id in delta.get("retire_nodes", []):
        if node_id not in nodes:
            raise DagError("NODE_NOT_FOUND", f"cannot retire unknown node {node_id!r}")
        nodes[node_id]["lifecycle_status"] = "retired"
        changes["nodes_retired"].append(node_id); changed_nodes.add(node_id)
    for edge in delta.get("upsert_edges", []):
        edge_id = edge.get("id")
        if not edge_id:
            raise DagError("BAD_EDGE_ID", "upsert edge is missing id")
        bucket = "edges_updated" if edge_id in edges else "edges_added"
        edges[edge_id] = copy.deepcopy(edge); changes[bucket].append(edge_id)
        changed_nodes.update((edge.get("from"), edge.get("to")))
    for edge_id in delta.get("remove_edges", []):
        if edge_id not in edges:
            raise DagError("EDGE_NOT_FOUND", f"cannot remove unknown edge {edge_id!r}")
        edge = edges.pop(edge_id); changes["edges_removed"].append(edge_id)
        changed_nodes.update((edge["from"], edge["to"]))
    out["nodes"] = list(nodes.values()); out["edges"] = list(edges.values())
    return normalize_graph(out), {**changes, "changed_node_ids": sorted(item for item in changed_nodes if item)}


def preview_submission(submission: dict) -> dict:
    graph = load_graph()
    validation = _validate_submission(submission, graph)
    if not validation["ok"]:
        return {"schema": SERVICE_SCHEMA, "ok": False, "accepted": False, "validation": validation}
    try:
        proposed, changes = _apply_delta(graph, submission["graph_delta"])
    except DagError as exc:
        return exc.record()
    graph_validation = validate_graph(proposed)
    if not graph_validation["ok"]:
        return {"schema": SERVICE_SCHEMA, "ok": False, "accepted": False, "validation": validation, "graph_validation": graph_validation, "changes": changes}
    impact = impact_analysis(changes["changed_node_ids"], max_depth=8, _graph=proposed) if changes["changed_node_ids"] else {"affected_node_count": 0, "affected_nodes": [], "reevaluate_files": []}
    return {
        "schema": SERVICE_SCHEMA,
        "ok": True,
        "accepted": True,
        "submission_id": submission["submission_id"],
        "base_revision": graph["revision"],
        "proposed_revision": proposed["revision"],
        "submission_digest": f"sha256:{object_digest(submission)}",
        "changes": changes,
        "impact": impact,
        "validation": validation,
        "graph_validation": graph_validation,
    }


def materialize_submission(submission: dict) -> dict:
    """Return the fully validated graph a submission would produce, without writing."""
    graph = load_graph()
    validation = _validate_submission(submission, graph)
    if not validation["ok"]:
        raise DagError("SUBMISSION_REJECTED", "submission cannot be materialized", validation=validation)
    proposed, _ = _apply_delta(graph, submission["graph_delta"])
    graph_validation = validate_graph(proposed)
    if not graph_validation["ok"]:
        raise DagError("GRAPH_REJECTED", "materialized graph failed validation", validation=graph_validation)
    return proposed


def _safe_name(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value)).strip("._")
    if not safe:
        raise DagError("BAD_IDENTIFIER", "identifier does not contain a safe filename component")
    return safe[:128]


def _repository_relative_path(path: str | Path, root: Path) -> str:
    """Return a Git path without following symlinks or permitting root escape."""
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = Path(os.path.abspath(candidate))
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise DagError(
            "GIT_PATH_OUTSIDE_REPOSITORY",
            f"DAG publication path escapes the repository: {path}",
            path=str(path),
            repository_root=str(root),
        ) from exc
    if not candidate.exists() and not candidate.is_symlink():
        raise DagError(
            "GIT_PUBLICATION_PATH_MISSING",
            f"DAG publication path is missing: {relative.as_posix()}",
            path=relative.as_posix(),
        )
    return relative.as_posix()


def _submission_commit_paths(submission: dict, applied_path: Path, receipt_path: Path) -> list[str]:
    root = repository_root().resolve()
    candidates: list[str | Path] = [canonical_graph_path(), applied_path, receipt_path]
    for artifact in submission.get("artifacts", []):
        for file_record in artifact.get("files", []):
            if file_record.get("path"):
                candidates.append(file_record["path"])
    return sorted({_repository_relative_path(path, root) for path in candidates})


def _git_commit_applied_submission(submission: dict, applied_path: Path, receipt_path: Path) -> dict:
    """Commit only one applied submission's owned paths; never roll back DAG state."""
    root = repository_root().resolve()
    paths: list[str] = []
    try:
        paths = _submission_commit_paths(submission, applied_path, receipt_path)
        top_level = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if Path(top_level).resolve() != root:
            raise DagError(
                "GIT_REPOSITORY_MISMATCH",
                "configured Cella repository root is not the Git worktree root",
                repository_root=str(root),
                git_top_level=top_level,
            )
        subprocess.run(
            ["git", "-C", str(root), "add", "--", *paths],
            check=True,
            capture_output=True,
            text=True,
        )
        message = f"dag: apply {_safe_name(submission['submission_id'])}"
        subprocess.run(
            ["git", "-C", str(root), "commit", "--only", "-m", message, "--", *paths],
            check=True,
            capture_output=True,
            text=True,
        )
        commit = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        return {"ok": True, "status": "committed", "commit": commit, "paths": paths}
    except (DagError, OSError, subprocess.CalledProcessError) as exc:
        if isinstance(exc, subprocess.CalledProcessError):
            error = (exc.stderr or exc.stdout or str(exc)).strip()
        else:
            error = str(exc)
        return {
            "ok": False,
            "status": "git_publication_pending",
            "error": error,
            "paths": paths,
        }


def _atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(payload); temp_path = Path(handle.name)
    temp_path.replace(path)


@contextmanager
def _store_lock():
    """Serialize staging/apply operations across MCP processes."""
    import fcntl
    lock_path = dag_root() / ".write.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def submit_bundle(submission: dict, *, dry_run: bool = True) -> dict:
    preview = preview_submission(submission)
    if not preview.get("accepted") or dry_run:
        return {**preview, "dry_run": True, "staged": False}
    with _store_lock():
        # Re-preview inside the lock so a concurrent apply cannot stale the bundle.
        preview = preview_submission(submission)
        if not preview.get("accepted"):
            return {**preview, "dry_run": False, "staged": False}
        pending = dag_root() / "submissions" / "pending" / f"{_safe_name(submission['submission_id'])}.json"
        if pending.exists():
            existing = _read_json(pending)
            if existing.get("idempotency_key") != submission.get("idempotency_key") or object_digest(existing) != object_digest(submission):
                raise DagError("SUBMISSION_COLLISION", "submission id already exists with different content", path=str(pending))
            return {**preview, "dry_run": False, "staged": True, "idempotent_replay": True, "pending_path": str(pending)}
        _atomic_json(pending, submission)
        return {**preview, "dry_run": False, "staged": True, "idempotent_replay": False, "pending_path": str(pending)}


def apply_bundle(submission_id: str, *, confirm: bool = False) -> dict:
    if not confirm:
        raise DagError("CONFIRMATION_REQUIRED", "apply requires confirm=true; preview or stage the submission first")
    with _store_lock():
        pending = dag_root() / "submissions" / "pending" / f"{_safe_name(submission_id)}.json"
        submission = _read_json(pending)
        graph = load_graph()
        validation = _validate_submission(submission, graph)
        if not validation["ok"]:
            raise DagError("SUBMISSION_REJECTED", "pending submission is no longer applicable", validation=validation)
        proposed, changes = _apply_delta(graph, submission["graph_delta"])
        graph_validation = validate_graph(proposed)
        if not graph_validation["ok"]:
            raise DagError("GRAPH_REJECTED", "proposed graph failed validation", validation=graph_validation)
        _atomic_json(canonical_graph_path(), proposed)
        applied_dir = dag_root() / "submissions" / "applied"
        applied_dir.mkdir(parents=True, exist_ok=True)
        applied_path = applied_dir / pending.name
        pending.replace(applied_path)
        receipt = {
            "schema": SERVICE_SCHEMA,
            "submission_id": submission_id,
            "idempotency_key": submission["idempotency_key"],
            "submission_digest": f"sha256:{object_digest(submission)}",
            "base_revision": graph["revision"],
            "applied_revision": proposed["revision"],
            "applied_utc": datetime.now(timezone.utc).isoformat(),
            "changes": changes,
            "applied_submission_path": str(applied_path),
        }
        receipt_path = dag_root() / "receipts" / f"{_safe_name(submission_id)}.receipt.json"
        _atomic_json(receipt_path, receipt)
        git_commit = _git_commit_applied_submission(submission, applied_path, receipt_path)
        return {
            "schema": SERVICE_SCHEMA,
            "ok": True,
            "applied": True,
            "receipt": receipt,
            "receipt_path": str(receipt_path),
            "git_commit": git_commit,
        }


def _filtered_graph(filters: dict | None) -> dict:
    graph = load_graph()
    if not filters:
        return graph
    result = query_nodes(filters, edge_mode="induced", limit=MAX_QUERY_LIMIT, cursor=0)
    if result["counts"]["matched"] > MAX_QUERY_LIMIT:
        raise DagError("EXPORT_FILTER_TOO_BROAD", f"filtered export exceeds {MAX_QUERY_LIMIT} nodes; refine filters")
    out = copy.deepcopy(graph); out["nodes"] = result["nodes"]; out["edges"] = result["edges"]
    return normalize_graph(out)


def _dot(graph: dict) -> str:
    def quoted(value) -> str:
        return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'
    lines = ["digraph theorem_dag {", "  rankdir=LR;", "  graph [overlap=false];", "  node [shape=box];"]
    for node in graph["nodes"]:
        lines.append(f"  {quoted(node['id'])} [label={quoted(node['label'])}];")
    for edge in graph["edges"]:
        lines.append(f"  {quoted(edge['from'])} -> {quoted(edge['to'])} [label={quoted(edge['relation'])}, id={quoted(edge['id'])}];")
    lines.append("}")
    return "\n".join(lines) + "\n"


def _graphml(graph: dict) -> str:
    lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>", '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">', '  <key id="label" for="all" attr.name="label" attr.type="string"/>', '  <key id="type" for="node" attr.name="type" attr.type="string"/>', '  <key id="relation" for="edge" attr.name="relation" attr.type="string"/>', f'  <graph id="{xml_escape(graph["graph_id"])}" edgedefault="directed">']
    for node in graph["nodes"]:
        lines.append(f'    <node id="{xml_escape(node["id"])}"><data key="label">{xml_escape(node["label"])}</data><data key="type">{xml_escape(node["type"])}</data></node>')
    for edge in graph["edges"]:
        lines.append(f'    <edge id="{xml_escape(edge["id"])}" source="{xml_escape(edge["from"])}" target="{xml_escape(edge["to"])}"><data key="relation">{xml_escape(edge["relation"])}</data></edge>')
    lines.extend(["  </graph>", "</graphml>"])
    return "\n".join(lines) + "\n"


def export_graph(format: str = "node_edge_json", filters: dict | None = None, *, write: bool = False, include_data: bool = False) -> dict:
    graph = _filtered_graph(filters)
    fmt = str(format).strip().lower().replace("-", "_")
    if fmt == "canonical_json":
        payload = json.dumps(graph, indent=2, ensure_ascii=False) + "\n"; suffix = "json"
    elif fmt == "node_edge_json":
        payload = json.dumps({"nodes": graph["nodes"], "edges": graph["edges"]}, indent=2, ensure_ascii=False) + "\n"; suffix = "json"
    elif fmt == "cytoscape_json":
        payload = json.dumps({"elements": {"nodes": [{"data": node} for node in graph["nodes"]], "edges": [{"data": edge} for edge in graph["edges"]]}}, indent=2, ensure_ascii=False) + "\n"; suffix = "cytoscape.json"
    elif fmt == "dot":
        payload = _dot(graph); suffix = "dot"
    elif fmt == "graphml":
        payload = _graphml(graph); suffix = "graphml"
    else:
        raise DagError("UNKNOWN_EXPORT_FORMAT", f"unknown DAG export format {format!r}", available=["canonical_json", "node_edge_json", "cytoscape_json", "dot", "graphml"])
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    path = None
    if write:
        export_dir = dag_root() / "exports"; export_dir.mkdir(parents=True, exist_ok=True)
        path = export_dir / f"{_safe_name(graph['graph_id'])}__{fmt}__{graph['revision'][7:19]}.{suffix}"
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=export_dir, delete=False) as handle:
            handle.write(payload); temp_path = Path(handle.name)
        temp_path.replace(path)
    return {
        "schema": SERVICE_SCHEMA,
        "ok": True,
        "format": fmt,
        "graph_id": graph["graph_id"],
        "graph_revision": graph["revision"],
        "counts": {"nodes": len(graph["nodes"]), "edges": len(graph["edges"])},
        "sha256": digest,
        "bytes": len(payload.encode("utf-8")),
        "written": bool(write),
        "path": str(path) if path else None,
        "data": payload if include_data else None,
    }
