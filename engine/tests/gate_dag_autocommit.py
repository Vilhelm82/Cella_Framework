"""Gate scoped Git durability for successfully applied DAG submissions."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "engine" / "src"))

from cella.dag_service import (  # noqa: E402
    GRAPH_DIRECTION,
    apply_bundle,
    load_graph,
    normalize_graph,
    submit_bundle,
)


FAILS: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


with tempfile.TemporaryDirectory() as temp:
    root = Path(temp) / "repo"
    dag = root / "DAG_Library"
    (dag / "canonical").mkdir(parents=True)
    shutil.copytree(REPO / "Artifact_Schemas", root / "Artifact_Schemas")
    graph = normalize_graph({
        "schema_version": 1,
        "graph_id": "auto-commit-gate",
        "direction": GRAPH_DIRECTION,
        "authority_policy": "Gate fixture: the DAG indexes claims and does not prove them.",
        "nodes": [],
        "edges": [],
        "extensions": {},
    })
    (dag / "canonical" / "theorem-dag.json").write_text(
        json.dumps(graph, indent=2) + "\n", encoding="utf-8"
    )
    (root / ".gitignore").write_text("DAG_Library/.write.lock\n", encoding="utf-8")

    git(root, "init", "-b", "main")
    git(root, "config", "user.name", "DAG Gate")
    git(root, "config", "user.email", "dag-gate@example.invalid")
    git(root, "add", "Artifact_Schemas", "DAG_Library/canonical/theorem-dag.json", ".gitignore")
    git(root, "commit", "-m", "gate baseline")
    baseline = git(root, "rev-parse", "HEAD")

    source = root / "papers" / "new-result.md"
    source.parent.mkdir(parents=True)
    source.write_text("# New result\n\nCertified gate fixture.\n", encoding="utf-8")
    source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    (root / "scratch.txt").write_text("must remain untracked\n", encoding="utf-8")
    (root / "unrelated-staged.txt").write_text("must remain staged\n", encoding="utf-8")
    git(root, "add", "unrelated-staged.txt")

    previous_root = os.environ.get("CELLA_REPOSITORY_ROOT")
    previous_dag = os.environ.get("CELLA_DAG_ROOT")
    os.environ["CELLA_REPOSITORY_ROOT"] = str(root)
    os.environ["CELLA_DAG_ROOT"] = str(dag)
    try:
        live = load_graph()
        artifact_id = "TEST:auto-commit"
        node = {
            "id": "TEST:report:auto-commit",
            "label": "Auto-commit gate node",
            "type": "report",
            "claim_status": None,
            "lifecycle_status": "draft",
            "reachability": None,
            "tracked": False,
            "layer": "test",
            "summary": "Temporary gate record for scoped Git durability.",
            "source_refs": [{
                "pointer": "cella:papers/new-result.md",
                "sha256": source_sha,
            }],
            "external_ids": {"artifacts": [artifact_id]},
            "facets": {},
            "visual_hints": {},
            "retrieval": {
                "key_terms": ["auto-commit"],
                "retrieval_questions": [],
                "context_priority": "low",
                "context_role": "supporting",
            },
            "extensions": {},
        }
        submission = {
            "schema_version": 1,
            "submission_id": "gate-auto-commit",
            "base_revision": live["revision"],
            "idempotency_key": "gate-auto-commit-0001",
            "submitted_by": "gate_dag_autocommit",
            "summary": "Exercise scoped Git durability after a valid DAG apply.",
            "artifacts": [{
                "schema_version": 1,
                "artifact_id": artifact_id,
                "artifact_type": "report",
                "title": "Auto-commit gate artifact",
                "summary": "Temporary artifact used by the scoped Git durability gate.",
                "subject_families": ["schema_test"],
                "claim_status": None,
                "lifecycle_status": "draft",
                "files": [{
                    "role": "paper",
                    "path": "papers/new-result.md",
                    "sha256": source_sha,
                    "media_type": "text/markdown",
                }],
                "claims": [],
                "relations": [],
                "external_ids": {},
                "declared_impacts": [],
                "llm": {
                    "one_sentence_purpose": "Exercise scoped Git durability.",
                    "key_terms": ["gate"],
                    "retrieval_questions": [],
                    "context_priority": "low",
                    "context_role": "supporting",
                },
                "extensions": {},
            }],
            "graph_delta": {
                "upsert_nodes": [node],
                "upsert_edges": [],
                "retire_nodes": [],
                "remove_edges": [],
            },
            "declared_impacts": [],
            "extensions": {},
        }
        staged = submit_bundle(submission, dry_run=False)
        check("valid submission stages", staged["staged"])
        applied = apply_bundle("gate-auto-commit", confirm=True)
        git_record = applied.get("git_commit", {})
        check("apply reports a successful Git commit", git_record.get("status") == "committed")
        check("apply exposes the committed revision", git_record.get("commit") == git(root, "rev-parse", "HEAD"))
        check("auto-commit advances HEAD", git(root, "rev-parse", "HEAD") != baseline)

        committed = set(filter(None, git(root, "show", "--name-only", "--pretty=format:", "HEAD").splitlines()))
        expected = {
            "papers/new-result.md",
            "DAG_Library/canonical/theorem-dag.json",
            "DAG_Library/submissions/applied/gate-auto-commit.json",
            "DAG_Library/receipts/gate-auto-commit.receipt.json",
        }
        check("commit contains exactly the DAG-owned paths", committed == expected)
        check("unrelated staged file remains staged", git(root, "diff", "--cached", "--name-only") == "unrelated-staged.txt")
        check("unrelated untracked file remains untracked", "?? scratch.txt" in git(root, "status", "--short").splitlines())
    finally:
        if previous_root is None:
            os.environ.pop("CELLA_REPOSITORY_ROOT", None)
        else:
            os.environ["CELLA_REPOSITORY_ROOT"] = previous_root
        if previous_dag is None:
            os.environ.pop("CELLA_DAG_ROOT", None)
        else:
            os.environ["CELLA_DAG_ROOT"] = previous_dag

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp) / "not-a-git-repository"
    dag = root / "DAG_Library"
    (dag / "canonical").mkdir(parents=True)
    shutil.copytree(REPO / "Artifact_Schemas", root / "Artifact_Schemas")
    graph = normalize_graph({
        "schema_version": 1,
        "graph_id": "auto-commit-pending-gate",
        "direction": GRAPH_DIRECTION,
        "authority_policy": "Gate fixture: the DAG indexes claims and does not prove them.",
        "nodes": [],
        "edges": [],
        "extensions": {},
    })
    (dag / "canonical" / "theorem-dag.json").write_text(
        json.dumps(graph, indent=2) + "\n", encoding="utf-8"
    )
    previous_root = os.environ.get("CELLA_REPOSITORY_ROOT")
    previous_dag = os.environ.get("CELLA_DAG_ROOT")
    os.environ["CELLA_REPOSITORY_ROOT"] = str(root)
    os.environ["CELLA_DAG_ROOT"] = str(dag)
    try:
        live = load_graph()
        artifact_id = "TEST:auto-commit-pending"
        submission = {
            "schema_version": 1,
            "submission_id": "gate-auto-commit-pending",
            "base_revision": live["revision"],
            "idempotency_key": "gate-auto-commit-pending-0001",
            "submitted_by": "gate_dag_autocommit",
            "summary": "Prove Git failure remains recoverable after a valid apply.",
            "artifacts": [{
                "schema_version": 1,
                "artifact_id": artifact_id,
                "artifact_type": "report",
                "title": "Auto-commit pending gate artifact",
                "summary": "Temporary artifact used by the Git failure-semantics gate.",
                "subject_families": ["schema_test"],
                "claim_status": None,
                "lifecycle_status": "draft",
                "files": [],
                "claims": [],
                "relations": [],
                "external_ids": {},
                "declared_impacts": [],
                "llm": {
                    "one_sentence_purpose": "Exercise recoverable Git publication failure.",
                    "key_terms": ["gate"],
                    "retrieval_questions": [],
                    "context_priority": "low",
                    "context_role": "supporting",
                },
                "extensions": {},
            }],
            "graph_delta": {
                "upsert_nodes": [{
                    "id": "TEST:report:auto-commit-pending",
                    "label": "Auto-commit pending gate node",
                    "type": "report",
                    "claim_status": None,
                    "lifecycle_status": "draft",
                    "reachability": None,
                    "tracked": False,
                    "layer": "test",
                    "summary": "Temporary gate record for recoverable Git failure.",
                    "source_refs": [],
                    "external_ids": {"artifacts": [artifact_id]},
                    "facets": {},
                    "visual_hints": {},
                    "retrieval": {
                        "key_terms": ["auto-commit"],
                        "retrieval_questions": [],
                        "context_priority": "low",
                        "context_role": "supporting",
                    },
                    "extensions": {},
                }],
                "upsert_edges": [],
                "retire_nodes": [],
                "remove_edges": [],
            },
            "declared_impacts": [],
            "extensions": {},
        }
        staged = submit_bundle(submission, dry_run=False)
        check("pending-state submission stages", staged["staged"])
        applied = apply_bundle("gate-auto-commit-pending", confirm=True)
        check("Git failure does not roll back the DAG apply", applied["applied"] and len(load_graph()["nodes"]) == 1)
        check("Git failure returns publication pending", applied["git_commit"]["status"] == "git_publication_pending")
        check("pending result names the intended DAG records", len(applied["git_commit"]["paths"]) == 3)
        check("receipt survives Git publication failure", Path(applied["receipt_path"]).is_file())
    finally:
        if previous_root is None:
            os.environ.pop("CELLA_REPOSITORY_ROOT", None)
        else:
            os.environ["CELLA_REPOSITORY_ROOT"] = previous_root
        if previous_dag is None:
            os.environ.pop("CELLA_DAG_ROOT", None)
        else:
            os.environ["CELLA_DAG_ROOT"] = previous_dag

if FAILS:
    print(f"DAG AUTO-COMMIT GATE: OPEN — {len(FAILS)} failure(s): {FAILS}")
    raise SystemExit(1)
print("DAG AUTO-COMMIT GATE: CLOSED")
