"""End-to-end isolated gate for deterministic campaign opening."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "engine" / "src"))

from cella.campaign_start import commit_campaign, scaffold_campaign  # noqa: E402
from cella.dag_service import DagError, load_graph, validate_graph  # noqa: E402


FAILS: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


with tempfile.TemporaryDirectory() as temporary:
    isolated = Path(temporary) / "Cella Framework"
    isolated.mkdir()
    shutil.copytree(REPO / "Artifact_Schemas", isolated / "Artifact_Schemas")
    (isolated / "DAG_Library/canonical").mkdir(parents=True)
    shutil.copy2(REPO / "DAG_Library/canonical/theorem-dag.json", isolated / "DAG_Library/canonical/theorem-dag.json")
    shutil.copy2(REPO / "DAG_Library/SOURCE_REGISTRY.json", isolated / "DAG_Library/SOURCE_REGISTRY.json")

    # Existing source files remain read-only symlinks; only the isolated DAG and
    # new campaign folder can be mutated by this acceptance gate.
    for source in REPO.iterdir():
        if source.name in {"Artifact_Schemas", "DAG_Library", "Campaign_Library", "research", ".git"}:
            continue
        (isolated / source.name).symlink_to(source, target_is_directory=source.is_dir())

    isolated_research = isolated / "research"
    isolated_research.mkdir()
    for source in (REPO / "research").iterdir():
        if source.name == "campaigns":
            continue
        (isolated_research / source.name).symlink_to(source, target_is_directory=source.is_dir())
    isolated_campaigns = isolated_research / "campaigns"
    isolated_campaigns.mkdir()
    for source in (REPO / "research/campaigns").iterdir():
        if source.name == "Succession_Map":
            continue
        (isolated_campaigns / source.name).symlink_to(source, target_is_directory=source.is_dir())

    # Source overlays are mutated by commit, so every registered research
    # source must be copied into the isolated repository rather than reached
    # through a top-level directory symlink.
    source_registry = json.loads((REPO / "DAG_Library/SOURCE_REGISTRY.json").read_text())
    for source in source_registry.get("sources", []):
        pointer = str(source.get("pointer", ""))
        if not pointer.startswith("cella:research/"):
            continue
        relative = Path(pointer.split(":", 1)[1])
        destination = isolated / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / relative, destination)
    campaign_root = isolated / "Campaign_Library"
    catalogue = campaign_root / "_catalogue"
    catalogue.mkdir(parents=True)
    for name in ("CAMPAIGN_REGISTRY.md", "LEDGER.json"):
        shutil.copy2(REPO / "Campaign_Library/_catalogue" / name, catalogue / name)
    for family in (REPO / "Campaign_Library").glob("[0-9][0-9]_*"):
        destination = campaign_root / family.name
        destination.mkdir()
        for campaign in family.iterdir():
            (destination / campaign.name).symlink_to(campaign, target_is_directory=campaign.is_dir())

    previous = {
        name: os.environ.get(name)
        for name in ("CELLA_REPOSITORY_ROOT", "CELLA_DAG_ROOT", "CELLA_CAMPAIGN_ROOT", "CELLA_CAMPAIGN_STAGING")
    }
    os.environ["CELLA_REPOSITORY_ROOT"] = str(isolated)
    os.environ.pop("CELLA_DAG_ROOT", None)
    os.environ.pop("CELLA_CAMPAIGN_ROOT", None)
    os.environ.pop("CELLA_CAMPAIGN_STAGING", None)
    try:
        scaffold = scaffold_campaign(
            title="Campaign Opening Gate",
            subject_family="cella_residue_and_coupling_theory",
            summary="Exercise deterministic campaign identifiers, sidecar binding, impact preview, and explicit apply.",
            relations=[
                {"relation": "depends_on", "target_id": "DBP:thm:r3_acfold", "basis": "Known theorem fixture."},
                {"relation": "opens_gap", "target_id": "U-1918", "basis": "Known open theorem fixture."},
                {"from_id": "U-1918", "relation": "depends_on", "target_id": "DBP:wall:V_faithful", "basis": "Known wall fixture."},
            ],
            promote_tracked=["U-1918"],
        )
        check("scaffold writes a stable staging bundle", scaffold["ok"] and Path(scaffold["staging_dir"]).is_dir())
        check("scaffold resolves distinct CMP and CMA namespaces", scaffold["campaign_id"].startswith("CMP-") and scaffold["artifact_id"].startswith("CMA-"))
        check("family mapping is explicit and correct", scaffold["registry_family"] == "02_residue_role_channel_and_coupling")
        submission = json.loads((Path(scaffold["staging_dir"]) / "submission.json").read_text())
        campaign_node = next(node for node in submission["graph_delta"]["upsert_nodes"] if node["id"] == scaffold["node_id"])
        check("new node carries the exact artifact sidecar binding", campaign_node["external_ids"]["artifacts"] == [scaffold["artifact_id"]])
        refused = commit_campaign(scaffold["staging_dir"], confirm=False)
        check("commit previews impact but refuses an unconfirmed write", not refused["ok"] and refused["error"]["token"] == "CONFIRMATION_REQUIRED" and refused["impact"] is not None)

        # Prove the failure path, not merely the happy path.  A label mutation
        # on the promoted existing node is intentionally absent from the
        # persistent overlay patch, so the semantic rebuild diff must catch it.
        submission_path = Path(scaffold["staging_dir"]) / "submission.json"
        clean_submission_bytes = submission_path.read_bytes()
        mismatched = json.loads(clean_submission_bytes)
        promoted_record = next(node for node in mismatched["graph_delta"]["upsert_nodes"] if node["id"] == "U-1918")
        promoted_record["label"] = "ROLLBACK GATE SENTINEL"
        submission_path.write_text(json.dumps(mismatched, indent=2) + "\n", encoding="utf-8")
        rollback_paths = [
            isolated / "DAG_Library/canonical/theorem-dag.json",
            isolated / "DAG_Library/SOURCE_REGISTRY.json",
            isolated / "research/campaigns/Succession_Map/campaign-openings-v1.json",
            Path(scaffold["final_sidecar"]),
        ]
        before_failure = {path: path.read_bytes() if path.is_file() else None for path in rollback_paths}
        rollback_result = commit_campaign(scaffold["staging_dir"], confirm=True)
        after_failure = {path: path.read_bytes() if path.is_file() else None for path in rollback_paths}
        check(
            "semantic rebuild difference is a hard commit failure",
            not rollback_result["ok"]
            and rollback_result.get("rolled_back") is True
            and rollback_result.get("gate") == "rebuild_git_diff",
        )
        check("failed commit restores every canonical mutation byte-for-byte", before_failure == after_failure)
        submission_path.write_bytes(clean_submission_bytes)

        try:
            committed = commit_campaign(scaffold["staging_dir"], confirm=True)
        except DagError as exc:
            print(json.dumps(exc.record(), indent=2))
            raise
        if not committed.get("ok"):
            print(json.dumps(committed, indent=2))
        check("confirmed commit admits campaign and emits a receipt", committed["ok"] and committed["committed"] and Path(committed["receipt_path"]).is_file())
        graph = load_graph()
        admitted = next((node for node in graph["nodes"] if node["id"] == scaffold["node_id"]), None)
        promoted = next(node for node in graph["nodes"] if node["id"] == "U-1918")
        check("campaign node is admitted with its binding", admitted is not None and scaffold["artifact_id"] in admitted["external_ids"]["artifacts"])
        check("declared tracked-frontier promotion is applied", promoted["tracked"] and promoted["layer"] == "frontier")
        check("whole post-commit graph validates with live source digests", validate_graph(graph, verify_files=True)["ok"])
        replay = commit_campaign(scaffold["staging_dir"], confirm=True)
        check("confirmed replay is idempotent", replay["ok"] and replay["idempotent_replay"])
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

if FAILS:
    print(f"CAMPAIGN START GATE: OPEN — {len(FAILS)} failure(s): {FAILS}")
    raise SystemExit(1)
print("CAMPAIGN START GATE: CLOSED")
