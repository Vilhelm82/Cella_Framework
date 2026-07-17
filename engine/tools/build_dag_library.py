#!/usr/bin/env python3
"""Compile the current DBP frontier source graph into the canonical DAG store."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "engine" / "src"))

from cella.dag_service import canonical_graph_path, normalize_graph, repository_root  # noqa: E402

REPO = repository_root()


CLAIM_MAP = {
    "proved": "proved",
    "measured": "demonstrated",
    "conjecture": "conjectured",
    "conjecture_label": "conjectured",
    "open": "open",
    "refuted": "refuted",
}
LIFECYCLE_MAP = {
    "released": "released",
    "released_incomplete": "released",
    "current": "active",
    "active": "active",
    "promoted": "active",
    "policy_gate": "active",
    "protected": "active",
    "conjecture": "draft",
    "conjecture_label": "draft",
    "open": "active",
    "refuted": "archived",
    "proved": "released",
    "measured": "released",
}


def read_json(path: Path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def external_indexes() -> tuple[dict[str, dict[str, list[str]]], dict[str, str]]:
    by_sha: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    papers = read_json(REPO / "Papers_Library/_catalogue/LEDGER.json", {"artifacts": []})
    for item in papers.get("artifacts", []):
        by_sha[item["sha256"]]["paper_artifacts"].append(item["artifact_id"])
    campaigns = read_json(REPO / "Campaign_Library/_catalogue/LEDGER.json", {"campaigns": [], "artifacts": []})
    for item in campaigns.get("artifacts", []):
        by_sha[item["sha256"]]["campaign_artifacts"].append(item["artifact_id"])
        if item.get("campaign_id"):
            by_sha[item["sha256"]]["campaigns"].append(item["campaign_id"])
    reports = read_json(REPO / "Reports_Library/_catalogue/LEDGER.json", {"reports": []})
    for item in reports.get("reports", []):
        by_sha[item["sha256"]]["reports"].append(item["report_id"])
    evidence = read_json(REPO / "Evidence_Store/_catalogue/OBJECT_LEDGER.json", {"objects": []})
    for item in evidence.get("objects", []):
        by_sha[item["sha256"]]["evidence"].append(item["evidence_id"])
    campaign_aliases: dict[str, str] = {}
    for campaign in campaigns.get("campaigns", []):
        for alias in campaign.get("origin_aliases", []):
            campaign_aliases[str(alias)] = campaign["campaign_id"]
    return by_sha, campaign_aliases


def source_ref(pointer: str | None, declared_sha: str | None) -> tuple[list[dict], str | None]:
    if not pointer:
        return [], None
    if not pointer.startswith("cella:"):
        return [{"pointer": pointer, "sha256": declared_sha}], declared_sha
    raw_path, marker, fragment = pointer.split(":", 1)[1].partition("#")
    path = REPO / raw_path
    if path.is_dir() and (path / "README.md").is_file():
        raw_path = f"{raw_path.rstrip('/')}/README.md"
        path = REPO / raw_path
    digest = sha256(path) if path.is_file() else declared_sha
    normalized_pointer = f"cella:{raw_path}" + (f"#{fragment}" if marker else "")
    return [{"pointer": normalized_pointer, "sha256": digest}], digest


EXTERNAL_NAMESPACE_MAP = {
    "PAP": "paper_artifacts",
    "CMP": "campaigns",
    "CMA": "campaign_artifacts",
    "RPT": "reports",
    "EVD": "evidence",
    "V4PKG": "retirement_packages",
}


def normalize_external_ids(raw_external: dict | None) -> dict[str, list[str]]:
    out = {"encyclopedia": [], "paper_artifacts": [], "campaigns": [], "campaign_artifacts": [], "reports": [], "evidence": [], "retirement_packages": []}
    for raw_namespace, raw_values in (raw_external or {}).items():
        namespace = EXTERNAL_NAMESPACE_MAP.get(raw_namespace, raw_namespace)
        values = raw_values if isinstance(raw_values, list) else [raw_values]
        out.setdefault(namespace, [])
        out[namespace] = sorted(set(out[namespace] + [str(value) for value in values if value not in (None, "")]))
    return out


def normalize_source_refs(raw_node: dict) -> tuple[list[dict], str | None]:
    if "source_refs" not in raw_node:
        return source_ref(raw_node.get("source_pointer"), raw_node.get("sha256"))
    refs: list[dict] = []
    first_digest = None
    for raw_ref in raw_node.get("source_refs", []):
        normalized, digest = source_ref(raw_ref.get("pointer"), raw_ref.get("sha256"))
        refs.extend(normalized)
        if first_digest is None:
            first_digest = digest
    return refs, first_digest


def encyclopedia_index(crosswalk: Path | None) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    by_sha: dict[str, set[str]] = defaultdict(set)
    by_pointer: dict[str, set[str]] = defaultdict(set)
    if crosswalk is None:
        return by_sha, by_pointer
    with crosswalk.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            identifier = row.get("encyclopedia_id")
            if not identifier:
                continue
            if row.get("sha256"):
                by_sha[row["sha256"]].add(identifier)
            for key in ("source_pointer", "target_pointer"):
                pointer = (row.get(key) or "").split("#", 1)[0]
                if pointer:
                    by_pointer[pointer].add(identifier)
    return by_sha, by_pointer


def compile_graph(source: Path, crosswalk: Path | None = None) -> dict:
    raw = read_json(source)
    by_sha, campaign_aliases = external_indexes()
    encyclopedia_by_sha, encyclopedia_by_pointer = encyclopedia_index(crosswalk)
    nodes = []
    standard_node_keys = {"id", "label", "type", "status", "claim_status", "lifecycle_status", "reachability", "tracked", "layer", "detail", "summary", "source_pointer", "sha256", "source_refs", "external_ids", "facets", "visual_hints", "retrieval", "extensions"}
    for raw_node in raw["nodes"]:
        legacy_status = raw_node.get("status")
        refs, digest = normalize_source_refs(raw_node)
        external = normalize_external_ids(raw_node.get("external_ids"))
        if digest in by_sha:
            for namespace, values in by_sha[digest].items():
                external[namespace] = sorted(set(external.get(namespace, []) + values))
        pointer = refs[0]["pointer"] if refs else ""
        pointer_base = pointer.split("#", 1)[0]
        external["encyclopedia"] = sorted(
            encyclopedia_by_sha.get(digest or "", set())
            | encyclopedia_by_pointer.get(pointer_base, set())
        )
        for alias, campaign_id in campaign_aliases.items():
            if f"/research/campaigns/{alias}/" in f"/{pointer.split(':', 1)[-1]}":
                external["campaigns"] = sorted(set(external["campaigns"] + [campaign_id]))
        facets = dict(raw_node.get("facets", {}))
        if raw_node.get("paper") is not None and "paper" not in facets:
            facets["paper"] = raw_node["paper"]
        if legacy_status in {"released_incomplete", "promoted", "policy_gate", "protected"}:
            facets["classification"] = legacy_status
        extensions = dict(raw_node.get("extensions", {}))
        extensions.update({key: value for key, value in raw_node.items() if key not in standard_node_keys})
        if legacy_status is not None:
            extensions["source_graph_status"] = legacy_status
        retrieval = dict(raw_node.get("retrieval", {}))
        retrieval.setdefault("key_terms", [])
        retrieval.setdefault("retrieval_questions", [])
        retrieval.setdefault("context_priority", "normal")
        retrieval.setdefault("context_role", "frontier" if raw_node.get("layer") == "frontier" else ("core" if raw_node.get("type") in {"theorem", "proof", "paper"} else "supporting"))
        nodes.append({
            "id": raw_node["id"],
            "label": raw_node["label"],
            "type": raw_node["type"],
            "claim_status": raw_node.get("claim_status", CLAIM_MAP.get(legacy_status)),
            "lifecycle_status": raw_node.get("lifecycle_status", LIFECYCLE_MAP.get(legacy_status)),
            "reachability": raw_node.get("reachability"),
            "tracked": bool(raw_node.get("tracked", False)),
            "layer": raw_node.get("layer", "unclassified"),
            "summary": raw_node.get("summary", raw_node.get("detail", "")),
            "source_refs": refs,
            "external_ids": external,
            "facets": facets,
            "visual_hints": raw_node.get("visual_hints", {}),
            "retrieval": retrieval,
            "extensions": extensions,
        })
    edges = []
    for raw_edge in raw["edges"]:
        identity = f"{raw_edge['from']}\0{raw_edge['relation']}\0{raw_edge['to']}"
        edge_id = raw_edge.get("id") or f"EDGE:{hashlib.sha256(identity.encode()).hexdigest()[:20]}"
        edge_source_refs = []
        for raw_ref in raw_edge.get("source_refs", []):
            normalized, _ = source_ref(raw_ref.get("pointer"), raw_ref.get("sha256"))
            edge_source_refs.extend(normalized)
        edges.append({
            "id": edge_id,
            "from": raw_edge["from"],
            "to": raw_edge["to"],
            "relation": raw_edge["relation"],
            "label": raw_edge.get("label"),
            "basis": raw_edge.get("basis"),
            "source_refs": edge_source_refs,
            "facets": raw_edge.get("facets", {}),
            "extensions": {**raw_edge.get("extensions", {}), **{key: value for key, value in raw_edge.items() if key not in {"id", "from", "to", "relation", "label", "basis", "source_refs", "facets", "extensions"}}},
        })
    compiled_from = [{"pointer": f"cella:{source.relative_to(REPO)}", "sha256": sha256(source), "role": "curated_frontier_overlay"}]
    if crosswalk is not None:
        compiled_from.append({"pointer": "encyclopedia:audit/DAG_CROSSWALK.csv", "sha256": sha256(crosswalk), "role": "external_id_crosswalk"})
    return normalize_graph({
        "schema_version": 1,
        "graph_id": raw.get("graph_id", "cella:theorem-succession-frontier"),
        "revision": "sha256:" + "0" * 64,
        "direction": "from is the grammatical subject: from -relation-> to",
        "authority_policy": raw.get("authority_policy", "The DAG indexes provenance and declared relations; live Cella STATE and rerunnable certificates remain authoritative."),
        "nodes": nodes,
        "edges": edges,
        "extensions": {
            **raw.get("extensions", {}),
            "compiled_from": compiled_from,
            "source_generator": raw.get("generator", raw.get("generated")),
            "source_reachability_legend": raw.get("reachability_legend", {}),
            "normalization": "Canonical fields were preserved; scalar external ids became arrays, directory pointers became README files, ledger/crosswalk ids were enriched, and legacy status was split without promoting authority."
        },
    })


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


DEFAULT_SOURCE = "dbp-frontier-v1=" + str(REPO / "research/campaigns/Succession_Map/DBP_FRONTIER_DAG_v1.0.json")


def parse_source(arg: str) -> tuple[str | None, Path]:
    """'source_id=path' -> (source_id, path); 'path' -> (None, path)."""
    head, sep, tail = arg.partition("=")
    if sep and "/" not in head and not head.endswith(".json"):
        return head, Path(tail)
    return None, Path(arg)


def source_id_for(path: Path, compiled: dict, explicit: str | None) -> str:
    if explicit:
        return explicit
    graph_id = str(compiled.get("graph_id") or "")
    if graph_id.startswith("cella-"):
        return graph_id[len("cella-"):] or path.stem
    return graph_id or path.stem


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile one or more registered source graphs into the canonical DAG as a tagged union.")
    parser.add_argument("--source", action="append", default=None, help="Repeatable. 'source_id=path' or 'path'. Defaults to the frontier overlay.")
    parser.add_argument("--crosswalk", type=Path, default=None, help="Optional encyclopedia DAG_CROSSWALK.csv used only for external ids.")
    parser.add_argument("--out", type=Path, default=None, help="Optional canonical output path (default: the live store; only the live store rewrites SOURCE_REGISTRY).")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    crosswalk = args.crosswalk.resolve() if args.crosswalk else None
    raw_sources = args.source or [DEFAULT_SOURCE]

    merged_nodes: dict[str, dict] = {}
    merged_edges: dict[str, dict] = {}
    node_collisions: list[str] = []
    edge_collisions: list[str] = []
    registry_sources: list[dict] = []
    graph_id = None
    legend: dict = {}
    generators: list = []
    node_patches: list[tuple[str, dict]] = []
    for raw in raw_sources:
        explicit_id, path = parse_source(raw)
        # Preserve the registered logical path. Reading still follows symlinks,
        # but provenance and isolation remain rooted in the selected repository.
        path = path.absolute()
        compiled = compile_graph(path, crosswalk)
        source_id = source_id_for(path, compiled, explicit_id)
        raw_document = read_json(path, {})
        node_patches.extend((source_id, patch) for patch in raw_document.get("node_patches", []))
        graph_id = graph_id or compiled.get("graph_id")
        legend = legend or compiled.get("extensions", {}).get("source_reachability_legend", {})
        generators.append({"source_id": source_id, "generator": compiled.get("extensions", {}).get("source_generator")})
        for node in compiled["nodes"]:
            node.setdefault("facets", {})["source_id"] = source_id
            if node["id"] in merged_nodes:
                node_collisions.append(node["id"]); continue
            merged_nodes[node["id"]] = node
        for edge in compiled["edges"]:
            edge.setdefault("facets", {})["source_id"] = source_id
            if edge["id"] in merged_edges:
                edge_collisions.append(edge["id"]); continue
            merged_edges[edge["id"]] = edge
        role = "curated_frontier_overlay" if source_id.startswith("dbp-frontier") else ("cross_source_bridge" if not compiled["nodes"] else "registered_source")
        registry_sources.append({"source_id": source_id, "pointer": f"cella:{path.relative_to(REPO)}", "sha256": sha256(path), "role": role})

    patch_errors: list[str] = []
    patchable = {
        "label", "type", "claim_status", "lifecycle_status", "reachability",
        "tracked", "layer", "summary", "source_refs", "external_ids",
        "facets", "visual_hints", "retrieval", "extensions",
    }
    for source_id, patch in node_patches:
        node_id = patch.get("id")
        if node_id not in merged_nodes:
            patch_errors.append(f"{source_id}: unknown patch node {node_id!r}")
            continue
        illegal = sorted(set(patch.get("set", {})) - patchable)
        illegal_merge = sorted(set(patch.get("merge", {})) - patchable)
        if illegal or illegal_merge:
            patch_errors.append(f"{source_id}: illegal patch keys for {node_id}: {illegal + illegal_merge}")
            continue
        node = merged_nodes[node_id]
        for key, value in patch.get("set", {}).items():
            node[key] = value
        for key, values in patch.get("merge", {}).items():
            if not isinstance(values, dict) or not isinstance(node.get(key), dict):
                patch_errors.append(f"{source_id}: merge patch {node_id}.{key} requires objects")
                continue
            node[key] = {**node[key], **values}
    if patch_errors:
        raise ValueError("registered node patch failure: " + "; ".join(patch_errors))

    compiled_from = [{"pointer": s["pointer"], "sha256": s["sha256"], "role": s["role"]} for s in registry_sources]
    if crosswalk is not None:
        compiled_from.append({"pointer": "encyclopedia:audit/DAG_CROSSWALK.csv", "sha256": sha256(crosswalk), "role": "external_id_crosswalk"})
    graph = normalize_graph({
        "schema_version": 1,
        "graph_id": graph_id or "cella:theorem-succession-frontier",
        "revision": "sha256:" + "0" * 64,
        "direction": "from is the grammatical subject: from -relation-> to",
        "authority_policy": "The DAG indexes provenance and declared relations; live Cella STATE and rerunnable certificates remain authoritative.",
        "nodes": list(merged_nodes.values()),
        "edges": list(merged_edges.values()),
        "extensions": {
            "compiled_from": compiled_from,
            "source_generators": generators,
            "source_reachability_legend": legend,
            "source_composition": {
                "sources": [s["source_id"] for s in registry_sources],
                "node_collisions": sorted(set(node_collisions)),
                "edge_collisions": sorted(set(edge_collisions)),
                "node_patches": [
                    {"source_id": source_id, "node_id": patch.get("id")}
                    for source_id, patch in node_patches
                ],
            },
            "normalization": "Tagged union of registered sources; every node/edge carries facets.source_id (view sources separately or compose via filters); scalar external ids became arrays, directory pointers became README files, ledger/crosswalk ids were enriched, and legacy status was split without promoting authority.",
        },
    })
    out_path = args.out.resolve() if args.out else canonical_graph_path()
    if not args.check:
        write_json(out_path, graph)
        if out_path == canonical_graph_path():
            sources = list(registry_sources)
            if crosswalk is not None:
                sources.append({"source_id": "encyclopedia-crosswalk-v1", "pointer": "encyclopedia:audit/DAG_CROSSWALK.csv", "sha256": sha256(crosswalk), "role": "external_id_crosswalk"})
            write_json(REPO / "DAG_Library/SOURCE_REGISTRY.json", {
                "schema_version": 1,
                "sources": sources,
                "canonical_graph": str(canonical_graph_path().relative_to(REPO)),
                "canonical_revision": graph["revision"],
            })
    print(json.dumps({
        "graph_id": graph["graph_id"], "revision": graph["revision"],
        "nodes": len(graph["nodes"]), "edges": len(graph["edges"]),
        "sources": [s["source_id"] for s in registry_sources],
        "collisions": {"nodes": len(set(node_collisions)), "edges": len(set(edge_collisions))},
        "node_patches": len(node_patches),
        "written": not args.check, "out": str(out_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
