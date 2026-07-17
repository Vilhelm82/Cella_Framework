"""Gate the renderer-neutral DAG service and transactional mutation boundary."""
from __future__ import annotations

import copy
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "engine" / "src"))

from cella.dag_mcp_server import DAG_TOOL_NAMES, tool_callable_map
from cella.dag_service import (
    apply_bundle,
    dag_status,
    export_graph,
    impact_analysis,
    load_graph,
    submit_bundle,
    validate_graph,
)


FAILS = []


def check(name, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


live = load_graph()
validation = validate_graph(live, verify_files=True)
check("canonical graph validates with all source digests", validation["ok"] and validation["counts"]["warnings"] == 0)
_source_counts: dict = {}
for _node in live["nodes"]:
    _sid = (_node.get("facets") or {}).get("source_id")
    _source_counts[_sid] = _source_counts.get(_sid, 0) + 1
check("multi-source union carries the 88-node frontier + the encyclopedia substrate",
      _source_counts.get("dbp-frontier-v1") == 88 and _source_counts.get("encyclopedia-units-v1") == 1915)

dependency = next(edge for edge in live["edges"] if edge["relation"] == "depends_on")
impact = impact_analysis([dependency["to"]], max_depth=1)
check("dependency target change flags its dependent source", dependency["from"] in {node["id"] for node in impact["affected_nodes"]})

dot = export_graph("dot", include_data=True)
graphml = export_graph("graphml", include_data=True)
cytoscape = export_graph("cytoscape_json", include_data=True)
check("DOT export is generated from canonical graph", dot["ok"] and dot["data"].startswith("digraph theorem_dag"))
check("GraphML export is generated from canonical graph", graphml["ok"] and "<graphml" in graphml["data"])
check("Cytoscape export is valid JSON", "elements" in json.loads(cytoscape["data"]))

expected_tools = {
    "cella_dag_status", "cella_dag_schema", "cella_dag_get", "cella_dag_source", "cella_dag_query",
    "cella_dag_validate", "cella_dag_impact", "cella_dag_submit",
    "cella_dag_apply", "cella_dag_export",
    "cella_dag_view_capabilities", "cella_dag_view_compute",
    "cella_dag_view_list", "cella_dag_view_get",
    "cella_campaign_scaffold", "cella_campaign_commit",
}
check("standalone MCP surface exposes the full DAG workflow", set(DAG_TOOL_NAMES) == expected_tools == set(tool_callable_map()))

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp) / "DAG_Library"
    (root / "canonical").mkdir(parents=True)
    shutil.copy2(REPO / "DAG_Library/canonical/theorem-dag.json", root / "canonical/theorem-dag.json")
    previous = os.environ.get("CELLA_DAG_ROOT")
    os.environ["CELLA_DAG_ROOT"] = str(root)
    try:
        graph = load_graph()
        base_count = len(graph["nodes"])
        new_node = {
            "id": "TEST:report:transaction",
            "label": "Transactional DAG gate node",
            "type": "report",
            "claim_status": None,
            "lifecycle_status": "draft",
            "reachability": None,
            "tracked": False,
            "layer": "test",
            "summary": "Temporary gate record.",
            "source_refs": [],
            "external_ids": {"artifacts": ["TEST:report:transaction"]},
            "facets": {},
            "visual_hints": {},
            "retrieval": {"key_terms": ["transaction"], "retrieval_questions": [], "context_priority": "low", "context_role": "supporting"},
            "extensions": {},
        }
        submission = {
            "schema_version": 1,
            "submission_id": "gate-transaction",
            "base_revision": graph["revision"],
            "idempotency_key": "gate-transaction-0001",
            "submitted_by": "gate_dag_service",
            "summary": "Exercise preview, stage and explicit apply.",
            "artifacts": [{
                "schema_version": 1,
                "artifact_id": "TEST:report:transaction",
                "artifact_type": "report",
                "title": "Transactional DAG gate artifact",
                "summary": "Temporary valid sidecar used by the mutation gate.",
                "subject_families": ["schema_test"],
                "claim_status": None,
                "lifecycle_status": "draft",
                "files": [],
                "claims": [],
                "relations": [],
                "external_ids": {},
                "declared_impacts": [],
                "llm": {"one_sentence_purpose": "Exercise sidecar-bound graph admission.", "key_terms": ["gate"], "retrieval_questions": [], "context_priority": "low", "context_role": "supporting"},
                "extensions": {},
            }],
            "graph_delta": {"upsert_nodes": [new_node], "upsert_edges": [], "retire_nodes": [], "remove_edges": []},
            "declared_impacts": [],
            "extensions": {},
        }
        missing_sidecar = dict(submission)
        missing_sidecar["artifacts"] = []
        refused = submit_bundle(missing_sidecar, dry_run=True)
        check("new material is refused without a matching artifact sidecar", not refused["accepted"] and any(issue["token"] == "ARTIFACT_SIDECAR_REQUIRED" for issue in refused["validation"]["errors"]))
        unbound = copy.deepcopy(submission)
        unbound["graph_delta"]["upsert_nodes"][0]["external_ids"] = {}
        unbound_result = submit_bundle(unbound, dry_run=True)
        check("node id equality no longer substitutes for explicit artifact binding", not unbound_result["accepted"] and any(issue["token"] == "ARTIFACT_SIDECAR_REQUIRED" for issue in unbound_result["validation"]["errors"]))
        preview = submit_bundle(submission, dry_run=True)
        check("write path defaults to dry-run preview", preview["accepted"] and preview["dry_run"] and not preview["staged"])
        staged = submit_bundle(submission, dry_run=False)
        check("accepted bundle stages without mutating canonical graph", staged["staged"] and len(load_graph()["nodes"]) == base_count)
        applied = apply_bundle("gate-transaction", confirm=True)
        check("explicit apply mutates graph and emits receipt", applied["applied"] and len(load_graph()["nodes"]) == base_count + 1 and Path(applied["receipt_path"]).is_file())
        check("detached test DAG reports Git publication pending", applied["git_commit"]["status"] == "git_publication_pending")
        stale = submit_bundle(submission, dry_run=True)
        check("optimistic revision rejects stale submissions", not stale["accepted"] and any(issue["token"] == "STALE_BASE_REVISION" for issue in stale["validation"]["errors"]))
        check("post-apply graph still validates", dag_status()["ok"])
    finally:
        if previous is None:
            os.environ.pop("CELLA_DAG_ROOT", None)
        else:
            os.environ["CELLA_DAG_ROOT"] = previous

if FAILS:
    print(f"DAG SERVICE GATE: OPEN — {len(FAILS)} failure(s): {FAILS}")
    raise SystemExit(1)
print("DAG SERVICE GATE: CLOSED")
