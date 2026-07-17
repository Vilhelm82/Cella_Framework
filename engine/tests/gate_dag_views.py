"""Gate revision-bound CPU/CUDA derived views and content-addressed storage."""
from __future__ import annotations

import json
import os
import copy
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "engine" / "src"))

from cella.dag_service import load_graph, normalize_graph, schema_record
from cella.dag_views import (
    compute_view,
    get_view,
    list_views,
    validate_view,
    view_capabilities,
)


FAILS = []


def check(name, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


capabilities = view_capabilities()
check("CPU backend is always available", capabilities["backends"]["cpu"]["available"])
check("derived-view JSON schema is registered", schema_record("derived_view")["document"]["title"].startswith("Cella revision-bound"))

_live = load_graph()
layered_a = compute_view("layered", "auto")
layered_b = compute_view("layered", "auto")
view = layered_a["view"]
check("layered view covers the live canonical selection", layered_a["counts"] == {"nodes": len(_live["nodes"]), "edges": len(_live["edges"])})
check("derived view validates against its graph revision", validate_view(view, current_revision=view["graph_revision"])["ok"])
check("deterministic content digest excludes generation time", view["content_digest"] == layered_b["view"]["content_digest"])
check("layout state is revision-bound", view["graph_revision"].startswith("sha256:"))
check("stale derived views are explicitly flagged", validate_view(view, current_revision="sha256:" + "0" * 64)["stale"])

spring_cpu = compute_view("spring", "cpu", parameters={"seed": 17, "iterations": 5})
check("CPU spring adapter emits one position per node", len(spring_cpu["view"]["geometry"]["node_positions"]) == len(_live["nodes"]))

if capabilities["backends"]["cuda"]["available"]:
    spring_cuda = compute_view("spring", "cuda", parameters={"seed": 17, "iterations": 5})
    check("CUDA adapter resolves to the declared GPU backend", spring_cuda["view"]["compute"]["backend_resolved"] == "cuda")
    check("CUDA adapter records the physical device", "NVIDIA" in spring_cuda["view"]["compute"]["device"])

with tempfile.TemporaryDirectory() as temp:
    previous = os.environ.get("CELLA_DAG_VIEW_ROOT")
    os.environ["CELLA_DAG_VIEW_ROOT"] = temp
    try:
        stored = compute_view("layered", "cpu", write=True)
        path = Path(stored["path"])
        check("view write is content-addressed", path.name == stored["view"]["content_digest"][7:] + ".view.json")
        check("stored view is valid JSON", json.loads(path.read_text())["view_id"] == stored["view"]["view_id"])
        listing = list_views()
        check("stored view is discoverable", listing["count"] == 1 and listing["views"][0]["view_id"] == stored["view"]["view_id"])
        fetched = get_view(stored["view"]["view_id"])
        check("stored view is retrievable by stable id", fetched["validation"]["ok"] and not fetched["validation"]["stale"])
    finally:
        if previous is None:
            os.environ.pop("CELLA_DAG_VIEW_ROOT", None)
        else:
            os.environ["CELLA_DAG_VIEW_ROOT"] = previous

with tempfile.TemporaryDirectory() as temp:
    previous_root = os.environ.get("CELLA_DAG_ROOT")
    root = Path(temp) / "DAG_Library"
    (root / "canonical").mkdir(parents=True)
    template = load_graph()["nodes"][0]
    nodes = []
    for index in range(1915):
        node = copy.deepcopy(template)
        node["id"] = f"SYNTH:unit:{index:04d}"
        node["label"] = f"Synthetic encyclopedia unit {index:04d}"
        node["summary"] = "Synthetic encyclopedia pagination gate."
        node["source_refs"] = []
        nodes.append(node)
    large_graph = normalize_graph({
        "schema_version": 1,
        "graph_id": "cella-encyclopedia-scale-gate",
        "direction": "from is the grammatical subject: from -relation-> to",
        "authority_policy": "Synthetic renderer-capacity gate only.",
        "nodes": nodes,
        "edges": [],
        "extensions": {},
    })
    (root / "canonical/theorem-dag.json").write_text(json.dumps(large_graph))
    os.environ["CELLA_DAG_ROOT"] = str(root)
    try:
        paged = compute_view("layered", "auto", {"text": "Synthetic encyclopedia"})
        check("internal view selection pages beyond the 500-node MCP boundary", paged["counts"]["nodes"] == 1915)
        accelerated = compute_view("spring", "auto", parameters={"iterations": 1})
        expected_backend = "cuda" if capabilities["backends"]["cuda"]["available"] else "cpu"
        check("encyclopedia-scale auto backend selects the available accelerated route", accelerated["view"]["compute"]["backend_resolved"] == expected_backend)
    finally:
        if previous_root is None:
            os.environ.pop("CELLA_DAG_ROOT", None)
        else:
            os.environ["CELLA_DAG_ROOT"] = previous_root

if FAILS:
    print(f"DAG VIEW GATE: OPEN — {len(FAILS)} failure(s): {FAILS}")
    raise SystemExit(1)
print("DAG VIEW GATE: CLOSED")
