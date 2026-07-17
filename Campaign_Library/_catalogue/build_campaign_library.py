#!/usr/bin/env python3
"""Build and verify the non-destructive, normalized Cella Campaign Library."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


CELLA = Path("/home/wlloyd/Cella Framework")
LLOYD = Path("/home/wlloyd/Lloyd_Engine_V4")
LIBRARY = CELLA / "Campaign_Library"
CATALOGUE = LIBRARY / "_catalogue"
PAPERS_LIBRARY = CELLA / "Papers_Library"
PAPERS_LEDGER = PAPERS_LIBRARY / "_catalogue/LEDGER.json"

SOURCE_ROOTS = (
    ("Cella Framework", "cella_research_campaign", CELLA / "research/campaigns"),
    ("Cella Framework", "cella_archived_campaign_output", CELLA / "archive/Reference_Material/campaign_outputs"),
    ("Lloyd_Engine_V4", "lloyd_research_campaign", LLOYD / "research/campaigns"),
)

SKIP_PARTS = {
    ".git", ".claude", ".venv", "node_modules", "__pycache__",
    ".pytest_cache", "Campaign_Library", "Papers_Library",
}
SKIP_PREFIXES = (".~lock.",)
TEXT_SUFFIXES = {
    ".md", ".txt", ".tex", ".html", ".py", ".m2", ".json", ".jsonl",
    ".csv", ".tsv", ".out", ".pin", ".sha", ".sha256", ".log", ".toml",
    ".yaml", ".yml", ".rst",
}
REFERENCE_SCAN_SUFFIXES = {
    ".md", ".txt", ".tex", ".html", ".py", ".m2", ".json", ".csv", ".tsv",
    ".toml", ".yaml", ".yml", ".rst",
}

FAMILY_RULES = (
    ("01_engine_substrate_and_continuation", (
        "cella_continuation_engine", "pathfinder_build", "the_engine",
        "dbp_engine_development", "difference_tower",
    )),
    ("03_curvature_shape_and_local_geometry", (
        "curvature", "lead7", "pfc_", "shape_witness", "shape_of_the_quiet",
        "deficit_engine", "flip_cartography",
    )),
    ("02_residue_role_channel_and_coupling", (
        "dbp_", "rolechspec", "three_channel", "g02_", "g10_", "g11_", "g12_",
        "coupling_holonomy", "cradle_arm", "bigraded_jet",
    )),
    ("04_arithmetic_precision_and_transfer", (
        "precision_flow", "exact_jet", "arith_", "pi_rotation",
    )),
    ("05_algebraic_branches_and_monodromy", (
        "monodromy", "root_closure", "cubic_role_branch",
    )),
    ("06_fault_semantics_and_transformations", ("the_warp", "the_weld")),
    ("07_cross_campaign_governance_and_tasking", ("cross_campaign_task_specs", "cross_campaign_root_material")),
)
DEFAULT_FAMILY = "08_cross_program_and_unclassified"

ROLE_FOLDERS = {
    "authority": "00_campaign_identity_and_authority",
    "index": "00_campaign_identity_and_authority",
    "brief": "01_scope_preregistration_and_design",
    "preregistration": "01_scope_preregistration_and_design",
    "design": "01_scope_preregistration_and_design",
    "prediction": "01_scope_preregistration_and_design",
    "method": "02_methods_software_and_protocols",
    "source": "02_methods_software_and_protocols",
    "test": "02_methods_software_and_protocols",
    "record": "03_evidence_records_and_certificates",
    "certificate": "03_evidence_records_and_certificates",
    "visualization": "03_evidence_records_and_certificates",
    "report": "04_analysis_and_reports",
    "audit": "04_analysis_and_reports",
    "claim": "05_claims_theorems_and_decisions",
    "closeout": "06_closeout_handoffs_and_successors",
    "handoff": "06_closeout_handoffs_and_successors",
    "manifest": "07_references_manifests_and_schemas",
    "schema": "07_references_manifests_and_schemas",
    "reference": "07_references_manifests_and_schemas",
    "archive": "08_historical_archives_and_superseded",
    "historical": "08_historical_archives_and_superseded",
    "other": "09_unclassified_campaign_material",
}

PATH_TOKEN_RE = re.compile(
    r"(?:/home/wlloyd/(?:Cella Framework|Lloyd_Engine_V4)/[^`\"'<>\n]+?"
    r"|(?:[A-Za-z0-9_.() +\-]+/)+[A-Za-z0-9_.() +\-]+?"
    r"|[A-Za-z0-9_.() +\-]+?)"
    r"\.(?:md|txt|tex|html|py|m2|json|jsonl|csv|tsv|out|pin|sha|sha256|log|toml|yaml|yml|rst|zip|png|svg|ms)",
    re.IGNORECASE,
)
SHA256_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", re.IGNORECASE)


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def slugify(value: str) -> str:
    value = value.replace("&", " and ")
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    value = re.sub(r"_+", "_", value)
    return value or "unnamed"


def repository_root(repository: str) -> Path:
    return CELLA if repository == "Cella Framework" else LLOYD


def authority_for(zone: str) -> str:
    return {
        "cella_research_campaign": "cella_research_reference_not_canon",
        "cella_archived_campaign_output": "cella_archived_reference",
        "lloyd_research_campaign": "lloyd_retirement_source",
    }[zone]


def eligible(path: Path) -> bool:
    return (
        path.is_file()
        and not path.is_symlink()
        and not path.name.startswith(SKIP_PREFIXES)
        and not any(part in SKIP_PARTS for part in path.parts)
        and path.suffix.lower() != ".pyc"
    )


def canonical_campaign(zone: str, relative: Path) -> tuple[str, str, Path]:
    parts = relative.parts
    if zone == "cella_archived_campaign_output":
        raw = parts[0]
        mapped = {
            "symbolic_rolechspec": "rolechspec_symbolic_proof_extraction",
            "precision_flow": "precision_flow",
            "three_channel_kg": "three_channel_kg",
        }.get(raw, slugify(raw))
        return mapped, raw, Path(*parts[1:])

    if len(parts) == 1:
        name = relative.name.lower()
        if "curvature_valence" in name:
            return "curvature_valence", relative.name, Path(relative.name)
        if "pathfinder" in name:
            return "pathfinder_build", relative.name, Path(relative.name)
        return "cross_campaign_root_material", relative.name, Path(relative.name)

    raw = parts[0]
    if raw == "RoleChSpec" and len(parts) >= 3:
        subcampaign = parts[1]
        subcampaign_slug = slugify(subcampaign)
        canonical = subcampaign_slug if subcampaign_slug.startswith("rolechspec_") else f"rolechspec_{subcampaign_slug}"
        return canonical, f"RoleChSpec/{subcampaign}", Path(*parts[2:])
    if raw == "_task_specs":
        return "cross_campaign_task_specs", raw, Path(*parts[1:])
    aliases = {
        "cv_curvature_valence": "curvature_valence",
    }
    return aliases.get(slugify(raw), slugify(raw)), raw, Path(*parts[1:])


def family_for(campaign_slug: str) -> tuple[str, str]:
    for family, tokens in FAMILY_RULES:
        matches = [token for token in tokens if token in campaign_slug]
        if matches:
            return family, "campaign token: " + ", ".join(matches)
    return DEFAULT_FAMILY, "no campaign-family token matched"


def document_role(path: Path, relative_campaign_path: Path, zone: str) -> tuple[str, str]:
    name = path.name.lower()
    probe = relative_campaign_path.as_posix().lower()
    suffix = path.suffix.lower()

    if any(token in probe for token in ("retired", "superseded", "older", "archive/", "historical")):
        return "historical", "explicit retired/superseded/archive marker"
    if suffix in {".zip", ".tar", ".gz"}:
        return "archive", "archive package format"
    if suffix in {".png", ".jpg", ".jpeg", ".svg"}:
        return "visualization", "visualization format"
    if suffix in {".py", ".m2", ".ms"}:
        if any(token in name for token in ("verify", "certificate", "cert_", "_cert", "digest")):
            return "certificate", "executable verifier/certificate source"
        if any(token in name for token in ("test", "battery", "mutant", "fixture")):
            return "test", "executable test/battery/mutant/fixture source"
        return "source", "executable/source format"
    if any(token in name for token in ("handoff", "successor", "queue")):
        return "handoff", "handoff/successor marker"
    if any(token in name for token in ("closeout", "campaign_close", "arm_close", "stage_a_close", "stage_b_close", "stage_c_close", "ledger_close", "final_report", "verdict", "decision_sheet", "disposition", "stage_a_complete", "resolved", "retired")) or name in {"close.md", "close_stage_a.md"}:
        return "closeout", "closeout/verdict/final-decision marker"
    if any(token in name for token in ("authority", "charter", "scope_lock", "baseline_lock", "campaign_layout")):
        return "authority", "authority/charter/scope-lock marker"
    if name.startswith("readme") or any(token in name for token in ("index", "catalogue")):
        return "index", "README/index/catalogue marker"
    if any(token in name for token in ("prereg", "predecl", "precommit")):
        return "preregistration", "preregistration/predeclaration marker"
    if "/research/campaigns/_task_specs/" in path.as_posix() or any(token in name for token in ("brief", "task_spec", "build_spec", "recon_spec", "codex_task", "agent_task")) or (name.startswith("campaign_") and "report" not in name and "close" not in name):
        return "brief", "brief/task/build-spec marker"
    if any(token in name for token in ("plan", "design", "template", "protocol", "contract", "roadmap", "specification", "draft")):
        return "design", "plan/design/protocol marker"
    if any(token in name for token in ("predict", "hypothesis", "conjecture", "stake")):
        return "prediction", "prediction/hypothesis marker"
    if any(token in name for token in ("audit", "review", "correction", "reconciliation", "classification", "adequacy_matrix", "refusal_matrix")):
        return "audit", "audit/review/correction marker"
    if any(token in name for token in ("theorem", "proof", "claim", "law", "lemma", "prohibition", "obstruction", "rule_ledger")):
        return "claim", "claim/theorem/proof marker"
    if "/reports/" in f"/{probe}" or any(token in name for token in ("report", "results", "result_", "outcome", "finding", "analysis", "investigation", "calibration", "reduction", "census", "standing", "summary", "addendum", "note", "formula", "normalization", "sweep", "grammar", "atlas", "attribution", "surprise_ledger", "gap_ledger")):
        return "report", "report/result/analysis marker"
    if "schema" in name:
        return "schema", "schema marker"
    if any(token in name for token in ("manifest", "inventory", "layout")):
        return "manifest", "manifest/inventory marker"
    if any(token in name for token in ("citation", "reference", "bibliography")):
        return "reference", "citation/reference marker"
    if suffix in {".pin", ".sha", ".sha256"} or any(token in name for token in ("certificate", "cert_", "_cert", "verify", "digest", "sha256", "freeze_pin", "hash_", "gate_artifact", "specdiff")):
        return "certificate", "certificate/verifier/digest marker or format"
    if any(token in name for token in ("test", "battery", "mutant", "fixture")):
        return "test", "test/battery/mutant/fixture marker"
    if suffix in {".jsonl", ".out", ".log"} or name == "log.md" or "/records/" in f"/{probe}" or any(token in name for token in ("record", "metric", "observation", "factor", "timeline", "bundle", "artifact", "raw_")):
        return "record", "record/log/raw-evidence marker or format"
    if any(token in name for token in ("method", "algorithm", "workflow")):
        return "method", "method/workflow marker"
    if suffix in {".json", ".csv", ".tsv", ".txt"}:
        return "record", "generic structured campaign record format"
    return "other", "no controlled document-role marker matched"


def phase_label(relative_campaign_path: Path) -> str:
    for part in relative_campaign_path.parts[:-1]:
        label = slugify(part)
        if label in {"records", "reports", "battery", "verify", "shared_schemas", "agent_tasks"}:
            continue
        if re.match(r"^(?:stage|facet|campaign|wave|probe|cce|wp)_?[0-9a-z]+", label):
            return label
        if re.match(r"^\d{2}_cce[0-9]+", label) or label in {"campaign_authority", "post8_universalization", "v2_floor_correction"}:
            return label
    return "campaign_wide"


def normalized_title(path: Path) -> str:
    stem = path.name[:-len(path.suffix)] if path.suffix else path.name
    return slugify(stem)


def discover() -> list[dict[str, object]]:
    origins: list[dict[str, object]] = []
    for repository, zone, root in SOURCE_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not eligible(path):
                continue
            relative_root = path.relative_to(root)
            campaign_slug, origin_label, relative_campaign = canonical_campaign(zone, relative_root)
            origins.append({
                "repository": repository,
                "source_zone": zone,
                "source_root": root.as_posix(),
                "path": path.relative_to(repository_root(repository)).as_posix(),
                "absolute_path": path.as_posix(),
                "origin_campaign_label": origin_label,
                "campaign_slug": campaign_slug,
                "relative_campaign_path": relative_campaign.as_posix(),
                "authority": authority_for(zone),
            })
    return origins


def origin_priority(origin: dict[str, object]) -> tuple[int, str]:
    priorities = {
        "cella_research_campaign": 0,
        "cella_archived_campaign_output": 1,
        "lloyd_research_campaign": 2,
    }
    return priorities[origin["source_zone"]], origin["path"]


def existing_campaign_ids() -> dict[str, str]:
    ledger = CATALOGUE / "LEDGER.json"
    if not ledger.is_file():
        return {}
    data = json.loads(ledger.read_text(encoding="utf-8"))
    return {campaign["campaign_slug"]: campaign["campaign_id"] for campaign in data.get("campaigns", [])}


def assign_campaign_ids(slugs: set[str]) -> dict[str, str]:
    assigned = {slug: campaign_id for slug, campaign_id in existing_campaign_ids().items() if slug in slugs}
    used = {int(campaign_id.split("-")[1]) for campaign_id in assigned.values()}
    next_id = max(used, default=0) + 1
    for slug in sorted(slugs):
        if slug in assigned:
            continue
        while next_id in used:
            next_id += 1
        assigned[slug] = f"CMP-{next_id:04d}"
        used.add(next_id)
        next_id += 1
    return assigned


def read_text(path: Path) -> str:
    if path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > 12 * 1024 * 1024:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def read_reference_text(path: Path) -> str:
    if path.suffix.lower() not in REFERENCE_SCAN_SUFFIXES or path.stat().st_size > 2 * 1024 * 1024:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def rewrite_risk_flags(repository: str, source_path: str) -> list[str]:
    lower = source_path.lower()
    name = Path(source_path).name.lower()
    suffix = Path(source_path).suffix.lower()
    flags = []
    if repository == "Cella Framework" and (source_path == "README.md" or lower.startswith(("state/", "docs/"))):
        flags.append("cella_canon_or_governance_adjacent")
    if any(token in name for token in ("manifest", "digest", "sha", "pin", "certificate")):
        flags.append("digest_or_manifest_bound")
    if suffix in {".py", ".m2", ".ms"}:
        flags.append("executable_source")
    if suffix in {".json", ".jsonl", ".csv", ".tsv", ".toml", ".yaml", ".yml"} or "schema" in name:
        flags.append("machine_readable_contract_or_record")
    if lower.startswith("archive/") or "/archive/" in lower:
        flags.append("archive_or_historical_reference")
    if not flags:
        flags.append("ordinary_prose")
    return flags


def load_paper_artifacts() -> dict[str, dict[str, object]]:
    if not PAPERS_LEDGER.is_file():
        return {}
    data = json.loads(PAPERS_LEDGER.read_text(encoding="utf-8"))
    return {artifact["sha256"]: artifact for artifact in data["artifacts"]}


def build_reference_impact(records: list[dict[str, object]], origins: list[dict[str, object]], campaign_ids: dict[str, str]) -> dict[str, object]:
    origin_by_absolute = {origin["absolute_path"]: origin for origin in origins}
    record_by_origin: dict[str, dict[str, object]] = {}
    exact_aliases: dict[tuple[str, str], list[tuple[dict[str, object], dict[str, object], str]]] = defaultdict(list)
    absolute_aliases: dict[str, list[tuple[dict[str, object], dict[str, object], str]]] = defaultdict(list)
    campaign_aliases: dict[tuple[str, str], list[tuple[dict[str, object], dict[str, object], str]]] = defaultdict(list)
    basename_aliases: dict[str, list[tuple[dict[str, object], dict[str, object], str]]] = defaultdict(list)

    for record in records:
        for origin in record["origins"]:
            record_by_origin[origin["absolute_path"]] = record
            exact_aliases[(origin["repository"], origin["path"])].append((record, origin, "repository_relative"))
            absolute_aliases[origin["absolute_path"]].append((record, origin, "absolute"))
            campaign_aliases[(origin["campaign_slug"], origin["relative_campaign_path"])].append((record, origin, "campaign_relative"))
            basename_aliases[Path(origin["path"]).name].append((record, origin, "unique_basename"))

    references: list[dict[str, object]] = []
    seen = set()
    scan_roots = (("Cella Framework", CELLA), ("Lloyd_Engine_V4", LLOYD))
    for repository, root in scan_roots:
        for source in root.rglob("*"):
            if not eligible(source) or source.suffix.lower() not in REFERENCE_SCAN_SUFFIXES:
                continue
            content = read_reference_text(source)
            if not content:
                continue
            source_origin = origin_by_absolute.get(source.as_posix())
            source_campaign = source_origin["campaign_slug"] if source_origin else None
            source_record = record_by_origin.get(source.as_posix())
            source_path = source.relative_to(root).as_posix()
            for line in content.splitlines():
                if len(line) > 12000 or "." not in line:
                    continue
                for match in PATH_TOKEN_RE.finditer(line):
                    raw_token = match.group(0)
                    token = raw_token.strip(" `\t\r\n\"'()[]{}:;,.")
                    candidates: list[tuple[dict[str, object], dict[str, object], str]] = []
                    candidates.extend(absolute_aliases.get(token, []))
                    candidates.extend(exact_aliases.get((repository, token), []))
                    candidates.extend(exact_aliases.get((repository, token.lstrip("./")), []))
                    if source_campaign:
                        candidates.extend(campaign_aliases.get((source_campaign, token.lstrip("./")), []))
                    basename = Path(token).name
                    if "/" not in token and len(basename_aliases.get(basename, [])) == 1:
                        candidates.extend(basename_aliases[basename])
                    for target_record, target_origin, resolution in candidates:
                        key = (repository, source_path, token, target_record["artifact_id"], target_origin["path"])
                        if key in seen:
                            continue
                        seen.add(key)
                        target_campaign = target_record["campaign_slug"]
                        if source_campaign == target_campaign:
                            scope = "same_campaign"
                        elif source_campaign:
                            scope = "cross_campaign"
                        else:
                            scope = "outside_campaign_tree"
                        references.append({
                            "source_repository": repository,
                            "source_path": source_path,
                            "source_campaign_id": campaign_ids.get(source_campaign),
                            "source_artifact_id": source_record["artifact_id"] if source_record else None,
                            "literal_token": token,
                            "resolution": resolution,
                            "scope": scope,
                            "rewrite_risk_flags": rewrite_risk_flags(repository, source_path),
                            "target_artifact_id": target_record["artifact_id"],
                            "target_campaign_id": target_record["campaign_id"],
                            "target_origin_repository": target_origin["repository"],
                            "target_origin_path": target_origin["path"],
                            "prospective_library_path": target_record["library_path"],
                        })

    inbound: dict[str, int] = Counter(reference["target_artifact_id"] for reference in references)
    outbound: dict[str, int] = Counter(reference["source_artifact_id"] for reference in references if reference["source_artifact_id"])
    for record in records:
        record["inbound_reference_count"] = inbound.get(record["artifact_id"], 0)
        record["outbound_reference_count"] = outbound.get(record["artifact_id"], 0)

    impacted_files = {(reference["source_repository"], reference["source_path"]) for reference in references}
    flags_by_file: dict[tuple[str, str], set[str]] = defaultdict(set)
    for reference in references:
        flags_by_file[(reference["source_repository"], reference["source_path"])].update(reference["rewrite_risk_flags"])
    return {
        "reference_count": len(references),
        "impacted_source_file_count": len(impacted_files),
        "impacted_source_files_by_repository": dict(sorted(Counter(repository for repository, _ in impacted_files).items())),
        "impacted_source_files_by_suffix": dict(sorted(Counter(Path(path).suffix.lower() or "none" for _, path in impacted_files).items())),
        "impacted_source_files_by_risk_flag": dict(sorted(Counter(flag for flags in flags_by_file.values() for flag in flags).items())),
        "scope_counts": dict(sorted(Counter(reference["scope"] for reference in references).items())),
        "resolution_counts": dict(sorted(Counter(reference["resolution"] for reference in references).items())),
        "references": references,
    }


def build(dry_run: bool) -> dict[str, object]:
    origins = discover()
    paper_artifacts_by_digest = load_paper_artifacts()
    campaign_slugs = {origin["campaign_slug"] for origin in origins}
    campaign_ids = assign_campaign_ids(campaign_slugs)

    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    digest_cache: dict[str, str] = {}
    for origin in origins:
        digest = sha256(Path(origin["absolute_path"]))
        digest_cache[origin["absolute_path"]] = digest
        grouped[(origin["campaign_slug"], digest)].append(origin)

    records: list[dict[str, object]] = []
    destination_claims: dict[str, str] = {}
    sorted_groups = sorted(grouped, key=lambda key: (campaign_ids[key[0]], origin_priority(min(grouped[key], key=origin_priority))))
    for number, (campaign_slug, digest) in enumerate(sorted_groups, start=1):
        group_origins = sorted(grouped[(campaign_slug, digest)], key=origin_priority)
        preferred = group_origins[0]
        source = Path(preferred["absolute_path"])
        relative_campaign = Path(preferred["relative_campaign_path"])
        role, role_basis = document_role(source, relative_campaign, preferred["source_zone"])
        family, family_basis = family_for(campaign_slug)
        campaign_id = campaign_ids[campaign_slug]
        phase = phase_label(relative_campaign)
        extension = source.suffix.lower()
        filename = f"{campaign_id}__ROLE-{role.upper()}__{normalized_title(source)}{extension}"
        relative_destination = Path(family) / f"{campaign_id}__{campaign_slug}" / ROLE_FOLDERS[role] / phase / filename
        destination_key = relative_destination.as_posix().lower()
        if destination_key in destination_claims and destination_claims[destination_key] != digest:
            filename = f"{campaign_id}__ROLE-{role.upper()}__{normalized_title(source)}__{digest[:8]}{extension}"
            relative_destination = Path(family) / f"{campaign_id}__{campaign_slug}" / ROLE_FOLDERS[role] / phase / filename
            destination_key = relative_destination.as_posix().lower()
        destination_claims[destination_key] = digest
        paper_artifact = paper_artifacts_by_digest.get(digest)
        if paper_artifact:
            paper_target = PAPERS_LIBRARY / paper_artifact["library_path"]
            if not paper_target.is_file() or sha256(paper_target) != digest:
                raise RuntimeError(f"Papers Library target does not match its ledger: {paper_target}")

        record = {
            "artifact_id": f"CMA-{number:06d}",
            "campaign_id": campaign_id,
            "campaign_slug": campaign_slug,
            "campaign_family": family,
            "document_role": role,
            "role_basis": role_basis,
            "family_basis": family_basis,
            "phase_label": phase,
            "normalized_filename": filename,
            "library_path": relative_destination.as_posix(),
            "sha256": digest,
            "bytes": source.stat().st_size,
            "format": extension.lstrip(".") or "none",
            "origins": group_origins,
            "mirror_count_within_campaign": len(group_origins),
            "embedded_sha256": [],
            "cross_campaign_mirror_artifact_ids": [],
            "storage_mode": "papers_library_symlink" if paper_artifact else "campaign_library_clone",
            "papers_artifact_id": paper_artifact["artifact_id"] if paper_artifact else None,
            "papers_category": paper_artifact["category"] if paper_artifact else None,
            "papers_subject_family": paper_artifact["subject_family"] if paper_artifact else None,
            "papers_library_path": paper_artifact["library_path"] if paper_artifact else None,
            "inbound_reference_count": 0,
            "outbound_reference_count": 0,
        }
        records.append(record)

    records_by_digest: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in records:
        records_by_digest[record["sha256"]].append(record)
    for digest_records in records_by_digest.values():
        if len({record["campaign_slug"] for record in digest_records}) <= 1:
            continue
        ids = [record["artifact_id"] for record in digest_records]
        for record in digest_records:
            record["cross_campaign_mirror_artifact_ids"] = [artifact_id for artifact_id in ids if artifact_id != record["artifact_id"]]

    digest_to_records = records_by_digest
    for record in records:
        embedded = set()
        for origin in record["origins"]:
            embedded.update(match.lower() for match in SHA256_RE.findall(read_text(Path(origin["absolute_path"]))))
        record["embedded_sha256"] = sorted(embedded)
        record["embedded_digest_matches"] = sorted({
            match["artifact_id"]
            for digest in embedded
            for match in digest_to_records.get(digest, [])
            if match["artifact_id"] != record["artifact_id"]
        })

    impact = build_reference_impact(records, origins, campaign_ids)

    aliases_by_campaign: dict[str, set[str]] = defaultdict(set)
    zones_by_campaign: dict[str, Counter] = defaultdict(Counter)
    artifact_count_by_campaign: Counter = Counter()
    origin_count_by_campaign: Counter = Counter()
    role_evidence_by_campaign: dict[str, Counter] = defaultdict(Counter)
    for record in records:
        artifact_count_by_campaign[record["campaign_slug"]] += 1
        origin_count_by_campaign[record["campaign_slug"]] += len(record["origins"])
        role_evidence_by_campaign[record["campaign_slug"]][record["document_role"]] += 1
        for origin in record["origins"]:
            aliases_by_campaign[record["campaign_slug"]].add(origin["origin_campaign_label"])
            zones_by_campaign[record["campaign_slug"]][origin["source_zone"]] += 1

    campaigns = []
    for slug in sorted(campaign_slugs, key=lambda item: campaign_ids[item]):
        family, family_basis = family_for(slug)
        campaigns.append({
            "campaign_id": campaign_ids[slug],
            "campaign_slug": slug,
            "campaign_family": family,
            "family_basis": family_basis,
            "status_label": "NOT_ADJUDICATED",
            "status_note": "documentary roles are inventoried; mathematical or operational status was not inferred",
            "origin_aliases": sorted(aliases_by_campaign[slug]),
            "source_zone_origin_counts": dict(sorted(zones_by_campaign[slug].items())),
            "artifact_count": artifact_count_by_campaign[slug],
            "origin_count": origin_count_by_campaign[slug],
            "document_role_counts": dict(sorted(role_evidence_by_campaign[slug].items())),
        })

    summary = {
        "schema_version": 1,
        "generated": datetime.now().astimezone().isoformat(timespec="seconds"),
        "mode": "dry_run" if dry_run else "applied",
        "source_policy": "non-destructive byte-identical clones; normalized library paths; source names and contents unchanged",
        "authority_policy": "STATE remains Cella canon; campaign documentary labels do not promote mathematical status",
        "reference_update_policy": "reference rewrites are scoped only and not executed in this stage",
        "campaign_count": len(campaigns),
        "artifact_count": len(records),
        "origin_count": len(origins),
        "global_unique_digest_count": len(records_by_digest),
        "exact_mirrors_collapsed_within_campaign": sum(record["mirror_count_within_campaign"] - 1 for record in records),
        "cross_campaign_mirror_record_count": sum(bool(record["cross_campaign_mirror_artifact_ids"]) for record in records),
        "papers_library_symlink_count": sum(record["storage_mode"] == "papers_library_symlink" for record in records),
        "papers_library_shared_bytes": sum(record["bytes"] for record in records if record["storage_mode"] == "papers_library_symlink"),
        "family_counts": dict(sorted(Counter(record["campaign_family"] for record in records).items())),
        "role_counts": dict(sorted(Counter(record["document_role"] for record in records).items())),
        "reference_impact_summary": {key: value for key, value in impact.items() if key != "references"},
        "campaigns": campaigns,
        "artifacts": records,
    }

    if not dry_run:
        expected = {record["library_path"] for record in records}
        for family in [rule[0] for rule in FAMILY_RULES] + [DEFAULT_FAMILY]:
            root = LIBRARY / family
            if not root.exists():
                continue
            for existing in root.rglob("*"):
                if existing.is_file() and existing.relative_to(LIBRARY).as_posix() not in expected:
                    existing.unlink()
            for directory in sorted((path for path in root.rglob("*") if path.is_dir()), reverse=True):
                if not any(directory.iterdir()):
                    directory.rmdir()
        for record in records:
            destination = LIBRARY / record["library_path"]
            source = Path(record["origins"][0]["absolute_path"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            if record["storage_mode"] == "papers_library_symlink":
                paper_target = PAPERS_LIBRARY / record["papers_library_path"]
                desired_target = Path(os.path.relpath(paper_target, start=destination.parent))
                if destination.is_symlink() and Path(os.readlink(destination)) != desired_target:
                    destination.unlink()
                elif destination.exists() and not destination.is_symlink():
                    destination.unlink()
                if not destination.is_symlink():
                    destination.symlink_to(desired_target)
            else:
                if destination.is_symlink():
                    destination.unlink()
                if destination.exists() and sha256(destination) != record["sha256"]:
                    raise RuntimeError(f"library collision with different content: {destination}")
                if not destination.exists():
                    shutil.copy2(source, destination)
        write_catalogue(summary, impact)
    return summary


def write_catalogue(summary: dict[str, object], impact: dict[str, object]) -> None:
    CATALOGUE.mkdir(parents=True, exist_ok=True)
    (CATALOGUE / "LEDGER.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (CATALOGUE / "REFERENCE_IMPACT.json").write_text(json.dumps(impact, indent=2) + "\n", encoding="utf-8")

    with (CATALOGUE / "LEDGER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow((
            "artifact_id", "campaign_id", "campaign_slug", "campaign_family", "document_role",
            "phase_label", "library_path", "sha256", "bytes", "origin_repository", "source_zone",
            "origin_campaign_label", "origin_path", "authority", "inbound_reference_count",
            "outbound_reference_count", "storage_mode", "papers_artifact_id", "papers_library_path",
        ))
        for record in summary["artifacts"]:
            for origin in record["origins"]:
                writer.writerow((
                    record["artifact_id"], record["campaign_id"], record["campaign_slug"],
                    record["campaign_family"], record["document_role"], record["phase_label"],
                    record["library_path"], record["sha256"], record["bytes"], origin["repository"],
                    origin["source_zone"], origin["origin_campaign_label"], origin["path"],
                    origin["authority"], record["inbound_reference_count"], record["outbound_reference_count"],
                    record["storage_mode"], record["papers_artifact_id"], record["papers_library_path"],
                ))

    with (CATALOGUE / "PATH_RENAME_MAP.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("campaign_id", "artifact_id", "origin_repository", "origin_path", "normalized_library_path", "sha256", "rewrite_status"))
        for record in summary["artifacts"]:
            for origin in record["origins"]:
                writer.writerow((
                    record["campaign_id"], record["artifact_id"], origin["repository"], origin["path"],
                    record["library_path"], record["sha256"], "NOT_EXECUTED_SCOPE_ONLY",
                ))

    terminology = """# Campaign Library terminology and labels

This library normalizes documentary organization only. It does not promote a campaign,
claim, theorem, result, or certificate into Cella canon. `STATE/` remains authoritative.

## Campaign identifiers

- `CMP-####` is a stable library identifier assigned to one canonical campaign slug.
- Original campaign names are aliases retained in the registry and artifact ledger.
- Campaign status is `NOT_ADJUDICATED`; filenames are not evidence of truth or completion.

## Filename grammar

`CMP-####__ROLE-<CONTROLLED_ROLE>__<normalized_original_title>.<extension>`

Campaign-only artifacts are byte-identical clones. When an identical SHA-256 already
exists in `Papers_Library`, the normalized campaign path is a relative symlink to that
paper artifact. The separate trees remain visible while the bytes are stored once.

## Controlled document roles

| Role | Meaning |
|---|---|
| `authority` | charter, authority source, scope lock, or baseline lock |
| `index` | README, index, or catalogue |
| `brief` | campaign/task/build brief or specification |
| `preregistration` | preregistration, predeclaration, or precommitment |
| `design` | plan, protocol, contract, template, or design |
| `prediction` | explicit hypothesis, conjecture, prediction, or stake |
| `method` | methodological or workflow document |
| `source` | executable campaign source |
| `test` | battery, test, mutant, or fixture |
| `record` | raw record, log, observation, factor, or timeline |
| `certificate` | verifier, pin, digest, or certificate |
| `visualization` | campaign plot or diagram |
| `report` | analysis, report, result, census, or gap ledger |
| `audit` | audit, review, correction, reconciliation, or adequacy matrix |
| `claim` | claim ledger, theorem, proof, lemma, or law |
| `closeout` | close, closeout, final report, verdict, or decision sheet |
| `handoff` | handoff, successor, or queued continuation |
| `manifest` | manifest, inventory, or layout |
| `schema` | schema or data contract |
| `reference` | citations, bibliography, or reference values |
| `archive` | packaged archive |
| `historical` | explicitly retired, superseded, old, or historical material |
| `other` | campaign material with no reliable controlled-role marker |

## Lifecycle folders

The numbered role folders encode documentary function, not chronology or claim status.
Stage/facet/CCE labels are normalized as a subordinate `phase_label`; unscoped material
uses `campaign_wide`.

## Campaign-to-paper lineage

An exact digest match to `Papers_Library` creates a mechanical lineage edge recorded in
`CAMPAIGN_PAPER_LINEAGE.json` and `.md`. This proves artifact identity and production
context; it does not by itself prove the mathematical claim inside the artifact.
"""
    (CATALOGUE / "TERMINOLOGY.md").write_text(terminology, encoding="utf-8")

    registry_lines = [
        "# Campaign registry", "",
        "All status labels are deliberately `NOT_ADJUDICATED`.", "",
        "| ID | Canonical campaign | Family | Artifacts | Origins | Origin aliases |",
        "|---|---|---|---:|---:|---|",
    ]
    for campaign in summary["campaigns"]:
        registry_lines.append(
            f"| {campaign['campaign_id']} | `{campaign['campaign_slug']}` | `{campaign['campaign_family']}` | "
            f"{campaign['artifact_count']} | {campaign['origin_count']} | " + ", ".join(f"`{alias}`" for alias in campaign["origin_aliases"]) + " |"
        )
    (CATALOGUE / "CAMPAIGN_REGISTRY.md").write_text("\n".join(registry_lines) + "\n", encoding="utf-8")

    lineage_edges = [
        {
            "campaign_id": record["campaign_id"],
            "campaign_slug": record["campaign_slug"],
            "campaign_artifact_id": record["artifact_id"],
            "campaign_library_path": record["library_path"],
            "papers_artifact_id": record["papers_artifact_id"],
            "papers_category": record["papers_category"],
            "papers_subject_family": record["papers_subject_family"],
            "papers_library_path": record["papers_library_path"],
            "sha256": record["sha256"],
            "relation": "byte_identical_campaign_product",
        }
        for record in summary["artifacts"]
        if record["storage_mode"] == "papers_library_symlink"
    ]
    lineage = {
        "schema_version": 1,
        "edge_count": len(lineage_edges),
        "relation_semantics": "exact SHA-256 identity links a campaign artifact to its single stored Papers Library copy",
        "edges": lineage_edges,
    }
    (CATALOGUE / "CAMPAIGN_PAPER_LINEAGE.json").write_text(json.dumps(lineage, indent=2) + "\n", encoding="utf-8")
    lineage_lines = [
        "# Campaign to paper and theorem lineage", "",
        "Each edge below is backed by an exact SHA-256 match and implemented as a relative symlink.",
        "The edge records production context and byte identity; it does not promote claim status.", "",
        "| Campaign | Campaign artifact | Papers role | Papers artifact | Subject |",
        "|---|---|---|---|---|",
    ]
    for edge in lineage_edges:
        lineage_lines.append(
            f"| {edge['campaign_id']} `{edge['campaign_slug']}` | `{edge['campaign_artifact_id']}` | "
            f"`{edge['papers_category']}` | `{edge['papers_artifact_id']}` | `{edge['papers_subject_family']}` |"
        )
    (CATALOGUE / "CAMPAIGN_PAPER_LINEAGE.md").write_text("\n".join(lineage_lines) + "\n", encoding="utf-8")

    impact_lines = [
        "# Prospective reference-update scope", "",
        "No source references were rewritten in this stage.", "",
        f"- Detected reference records: **{impact['reference_count']}**",
        f"- Source files potentially affected: **{impact['impacted_source_file_count']}**",
        "- Scope counts: " + ", ".join(f"`{key}`={value}" for key, value in impact["scope_counts"].items()),
        "- Resolution counts: " + ", ".join(f"`{key}`={value}" for key, value in impact["resolution_counts"].items()),
        "- Source repositories: " + ", ".join(f"`{key}`={value}" for key, value in impact["impacted_source_files_by_repository"].items()),
        "- Risk flags by unique source file: " + ", ".join(f"`{key}`={value}" for key, value in impact["impacted_source_files_by_risk_flag"].items()),
        "", "## Interpretation", "",
        "A later rewrite stage must decide whether references should target normalized library paths,",
        "whether source campaign trees will themselves be renamed, and how executable imports and",
        "digest-bound manifests will be regenerated. This report scopes that work; it authorizes none of it.",
        "", "## Recommended execution split", "",
        "1. Rewrite same-campaign ordinary prose and validate local links.",
        "2. Review cross-campaign references campaign-by-campaign against the lineage ledger.",
        "3. Handle executable and machine-readable references with import/schema checks.",
        "4. Regenerate and re-verify every digest-, pin-, certificate-, or manifest-bound artifact.",
        "5. Review Cella canon/governance-adjacent references manually; never bulk-promote campaign status.",
        "", "The complete occurrence-level record is `REFERENCE_IMPACT.json` and the one-row-per-origin",
        "mapping is `PATH_RENAME_MAP.csv`.",
    ]
    (CATALOGUE / "REFERENCE_UPDATE_SCOPE.md").write_text("\n".join(impact_lines) + "\n", encoding="utf-8")

    readme = f"""# Cella Campaign Library

Non-destructive campaign library assembled from Cella and Lloyd Engine V4 campaign
trees. The library contains **{summary['campaign_count']} campaigns**, **{summary['artifact_count']}
campaign artifacts**, and **{summary['origin_count']} source paths**.

Every campaign-only clone is byte-identical to its recorded origin. Exact overlaps with
`Papers_Library` are relative symlinks, preserving separate campaign and paper trees while
storing the bytes once. Folder names, campaign IDs, role folders, phase labels, and
filenames are normalized under `_catalogue/TERMINOLOGY.md`. Source files and source
references were not renamed or edited.

## Catalogue

- `_catalogue/CAMPAIGN_REGISTRY.md` — campaign IDs, aliases, families, and counts.
- `_catalogue/CAMPAIGN_PAPER_LINEAGE.md` — campaign-to-paper/theorem identity edges.
- `_catalogue/CAMPAIGN_PAPER_LINEAGE.json` — machine-readable lineage and symlink map.
- `_catalogue/DEDUPLICATION_SWEEP.md` — exact-identity deduplication result and exclusions.
- `_catalogue/DEDUPLICATION_SWEEP.json` — machine-readable deduplication receipt.
- `_catalogue/TERMINOLOGY.md` — controlled folder and filename vocabulary.
- `_catalogue/LEDGER.json` — authoritative artifact, origin, digest, and mirror ledger.
- `_catalogue/LEDGER.csv` — one row per origin path.
- `_catalogue/PATH_RENAME_MAP.csv` — original-to-normalized mapping; rewrite status remains scope-only.
- `_catalogue/REFERENCE_UPDATE_SCOPE.md` — human scope assessment for a later rewrite stage.
- `_catalogue/REFERENCE_IMPACT.json` — occurrence-level reference impact data.
- `_catalogue/build_campaign_library.py` — reproducible builder and verifier.

## Authority boundary

This is a documentary library. Cella `STATE/` remains canon. Campaign names such as
`PROVEN`, `CERTIFIED`, `FINAL`, or `CLOSE` are origin claims and are not promoted by
their placement here.
"""
    (LIBRARY / "README.md").write_text(readme, encoding="utf-8")


def verify_library() -> dict[str, object]:
    ledger_path = CATALOGUE / "LEDGER.json"
    if not ledger_path.is_file():
        raise SystemExit(f"missing ledger: {ledger_path}")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    impact = json.loads((CATALOGUE / "REFERENCE_IMPACT.json").read_text(encoding="utf-8"))
    lineage = json.loads((CATALOGUE / "CAMPAIGN_PAPER_LINEAGE.json").read_text(encoding="utf-8"))
    paper_artifacts = load_paper_artifacts()
    errors: list[str] = []
    ids = {record["artifact_id"] for record in ledger["artifacts"]}
    campaign_ids = {campaign["campaign_id"] for campaign in ledger["campaigns"]}
    if len(ids) != len(ledger["artifacts"]):
        errors.append("artifact IDs are not unique")
    if len(campaign_ids) != len(ledger["campaigns"]):
        errors.append("campaign IDs are not unique")

    origin_count = 0
    symlink_count = 0
    clone_count = 0
    for record in ledger["artifacts"]:
        destination = LIBRARY / record["library_path"]
        if not destination.is_file():
            errors.append(f"missing library clone: {record['library_path']}")
            continue
        if destination.stat().st_size != record["bytes"] or sha256(destination) != record["sha256"]:
            errors.append(f"library clone mismatch: {record['library_path']}")
        if record["storage_mode"] == "papers_library_symlink":
            symlink_count += 1
            paper_artifact = paper_artifacts.get(record["sha256"])
            paper_target = PAPERS_LIBRARY / record["papers_library_path"]
            if not destination.is_symlink():
                errors.append(f"expected Papers Library symlink: {record['library_path']}")
            elif destination.resolve() != paper_target.resolve():
                errors.append(f"symlink target mismatch: {record['library_path']}")
            if not paper_artifact or paper_artifact["artifact_id"] != record["papers_artifact_id"]:
                errors.append(f"Papers Library lineage mismatch: {record['artifact_id']}")
        else:
            clone_count += 1
            if destination.is_symlink():
                errors.append(f"unexpected symlink for campaign-only artifact: {record['library_path']}")
        expected_prefix = Path(record["campaign_family"]) / f"{record['campaign_id']}__{record['campaign_slug']}" / ROLE_FOLDERS[record["document_role"]] / record["phase_label"]
        if not Path(record["library_path"]).is_relative_to(expected_prefix):
            errors.append(f"taxonomy mismatch: {record['library_path']}")
        expected_name = re.compile(rf"^{re.escape(record['campaign_id'])}__ROLE-{record['document_role'].upper()}__[a-z0-9_]+(?:__[0-9a-f]{{8}})?(?:\.[a-z0-9]+)?$")
        if not expected_name.match(record["normalized_filename"]):
            errors.append(f"filename grammar mismatch: {record['normalized_filename']}")
        for origin in record["origins"]:
            origin_count += 1
            source = Path(origin["absolute_path"])
            if not source.is_file():
                errors.append(f"missing source origin: {source}")
                continue
            if source.stat().st_size != record["bytes"] or sha256(source) != record["sha256"]:
                errors.append(f"source origin mismatch: {source}")
            if source.stat().st_dev == destination.stat().st_dev and source.stat().st_ino == destination.stat().st_ino:
                errors.append(f"clone is not independent: {source}")
        for artifact_id in record["cross_campaign_mirror_artifact_ids"] + record["embedded_digest_matches"]:
            if artifact_id not in ids:
                errors.append(f"unknown artifact binding {artifact_id} from {record['artifact_id']}")

    if len(ledger["artifacts"]) != ledger["artifact_count"]:
        errors.append("artifact count disagrees with ledger")
    if origin_count != ledger["origin_count"]:
        errors.append("origin count disagrees with ledger")
    if len(ledger["campaigns"]) != ledger["campaign_count"]:
        errors.append("campaign count disagrees with ledger")
    if impact["reference_count"] != len(impact["references"]):
        errors.append("reference-impact count disagrees with records")
    for reference in impact["references"]:
        if reference["target_artifact_id"] not in ids:
            errors.append(f"unknown reference target: {reference['target_artifact_id']}")
    if lineage["edge_count"] != len(lineage["edges"]) or lineage["edge_count"] != symlink_count:
        errors.append("campaign-paper lineage count disagrees with symlink records")
    lineage_campaign_artifacts = {edge["campaign_artifact_id"] for edge in lineage["edges"]}
    expected_lineage_artifacts = {record["artifact_id"] for record in ledger["artifacts"] if record["storage_mode"] == "papers_library_symlink"}
    if lineage_campaign_artifacts != expected_lineage_artifacts:
        errors.append("campaign-paper lineage edge set disagrees with ledger")

    current = discover()
    recorded_origins = {
        (origin["repository"], origin["path"], record["sha256"])
        for record in ledger["artifacts"]
        for origin in record["origins"]
    }
    current_origins = {
        (origin["repository"], origin["path"], sha256(Path(origin["absolute_path"])))
        for origin in current
    }
    if recorded_origins != current_origins:
        errors.append("source campaign inventory has drifted since generation")

    with (CATALOGUE / "LEDGER.csv").open(newline="", encoding="utf-8") as handle:
        csv_rows = sum(1 for _ in csv.DictReader(handle))
    if csv_rows != origin_count:
        errors.append("CSV origin count disagrees with JSON ledger")

    report = {
        "status": "pass" if not errors else "fail",
        "campaigns_verified": len(ledger["campaigns"]),
        "artifact_paths_verified": len(ledger["artifacts"]),
        "campaign_only_clones_verified": clone_count,
        "papers_library_symlinks_verified": symlink_count,
        "origin_paths_verified": origin_count,
        "reference_impact_records_verified": len(impact["references"]),
        "independent_copy_check": "pass" if not any("not independent" in error for error in errors) else "fail",
        "inventory_drift_check": "pass" if "source campaign inventory has drifted since generation" not in errors else "fail",
        "errors": errors,
    }
    if errors:
        print(json.dumps(report, indent=2))
        raise SystemExit(1)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--apply", action="store_true", help="clone campaign artifacts and write catalogues")
    actions.add_argument("--verify", action="store_true", help="verify clones, origins, taxonomy, and impact records")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify_library(), indent=2))
        return
    summary = build(dry_run=not args.apply)
    keys = (
        "mode", "campaign_count", "artifact_count", "origin_count",
        "global_unique_digest_count", "exact_mirrors_collapsed_within_campaign",
        "cross_campaign_mirror_record_count", "papers_library_symlink_count",
        "papers_library_shared_bytes", "family_counts", "role_counts",
        "reference_impact_summary",
    )
    print(json.dumps({key: summary[key] for key in keys}, indent=2))


if __name__ == "__main__":
    main()
