#!/usr/bin/env python3
"""Build Cella's SHA-256 Evidence Store and symlinked Reports Library."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


CELLA = Path("/home/wlloyd/Cella Framework")
LLOYD = Path("/home/wlloyd/Lloyd_Engine_V4")
EVIDENCE = CELLA / "Evidence_Store"
OBJECTS = EVIDENCE / "objects" / "sha256"
EVIDENCE_CATALOGUE = EVIDENCE / "_catalogue"
REPORTS = CELLA / "Reports_Library"
REPORTS_CATALOGUE = REPORTS / "_catalogue"

CAMPAIGN_LEDGER = CELLA / "Campaign_Library/_catalogue/LEDGER.json"
PAPERS_LEDGER = CELLA / "Papers_Library/_catalogue/LEDGER.json"

SKIP_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}
REPORT_OUTPUT_SUFFIXES = {
    ".md", ".txt", ".json", ".jsonl", ".csv", ".tsv", ".html",
    ".pdf", ".npz", ".out", ".pin", ".zip", ".png", ".jpg", ".svg",
}
CAMPAIGN_REPORT_ROLES = {"report", "audit", "closeout", "claim", "certificate", "visualization"}
PAPER_REPORT_MARKERS = {
    "report", "audit", "review", "ledger", "receipt", "result", "summary",
    "closeout", "verdict", "certificate", "reproducibility",
}

REPORT_CATEGORIES = {
    "campaign": "01_campaign_and_stage_reports",
    "verification": "02_verification_certification_and_release_receipts",
    "audit": "03_audits_reviews_and_methodology",
    "exploratory": "04_exploratory_searches_and_negative_results",
    "data": "05_machine_readouts_tables_and_supporting_data",
    "historical": "06_historical_and_superseded_reports",
}

SUBJECT_RULES = (
    ("photonic_and_sensor_inventions", ("patent", "photonic", "sensor_invention")),
    ("galois_horizon_and_kummer_covers", ("galois", "horizon", "kummer", "wreath", "quintic", "macaulay", "crown", "monodromy", "root_closure", "abel_ruffini", "total_reality", "generic_descent", "morse_lemma")),
    ("dbp_periods_landen_and_elliptic_structure", ("landen", "legendre", "relative_period", "elliptic", "pinning", "periods_of_the_dbp")),
    ("precision_flow_and_transfer_functions", ("precision_flow", "transfer_function", "early_rounding", "rounding", "ulp", "subnormal", "sterbenz", "f1_f2", "operand_route", "q_source", "half_grid", "precision", "arith_i")),
    ("local_curvature_and_black_hole_metrics", ("local_curvature", "lead7", "kerr", "newman", "black_hole", "pfc_", "pole_orders", "masscharge", "curvature_valence", "schwarzschild", "kn_three_face", "collision_field")),
    ("dbp_role_channel_and_orbit_geometry", ("dbp", "role_channel", "rolechspec", "orbit_calculus", "gauge_channel", "three_channel", "self_glue", "curvature_role", "theorem_8_1", "canonical_invariant", "role_singularity", "coupling_native_kg")),
    ("geometric_fault_localization_and_decomposition", ("mean_curvature", "decomposition", "fault_localization", "bilinear", "gradient_irreducibility", "monge", "two_lights", "essential_dimension", "interaction_curvature", "shape_witness", "deficit_engine", "cradle_arm", "dual_confinement", "gradient_focusing", "shape_of_the_quiet")),
    ("cella_residue_and_coupling_theory", ("cella", "residue", "coupling_field", "invariant_tower", "fault_geometry", "arithmetic_track", "holonomy", "normal_form", "localization", "shape_moment", "transport_law", "numerator_tower", "pathfinder", "difference_tower", "the_engine")),
    ("general_relativity_and_gravity", ("general_relativity", "gr_", "photon_sphere", "thermodynamic")),
)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_slug(value: str) -> str:
    value = value.strip().lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value or "unclassified"


def safe_filename(value: str) -> str:
    path = Path(value)
    stem = re.sub(r"[^A-Za-z0-9._+-]+", "_", path.stem).strip("_") or "artifact"
    suffix = re.sub(r"[^A-Za-z0-9.]+", "", path.suffix)
    return stem + suffix


def repo_relative(path: Path) -> tuple[str, str]:
    resolved = path.resolve()
    if resolved.is_relative_to(CELLA):
        return "Cella Framework", resolved.relative_to(CELLA).as_posix()
    if resolved.is_relative_to(LLOYD):
        return "Lloyd_Engine_V4", resolved.relative_to(LLOYD).as_posix()
    return "external", resolved.as_posix()


def eligible(path: Path) -> bool:
    return path.is_file() and not any(part in SKIP_PARTS for part in path.parts)


def tree_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*") if eligible(path))


def normalize_probe(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower())


def subject_family(*values: str) -> tuple[str, str]:
    probe = normalize_probe("/".join(values))
    for family, tokens in SUBJECT_RULES:
        hits = [token for token in tokens if normalize_probe(token) in probe]
        if hits:
            return family, "tokens: " + ", ".join(hits[:4])
    return "cross_program_and_unclassified", "no subject token rule matched"


def origin_key(origin: dict[str, object]) -> str:
    return json.dumps(origin, sort_keys=True, separators=(",", ":"))


class Collector:
    def __init__(self) -> None:
        self.objects: dict[str, dict[str, object]] = {}
        self.hash_cache: dict[str, tuple[str, int]] = {}
        self.report_candidates: list[dict[str, object]] = []

    def file_identity(self, path: Path) -> tuple[Path, str, int]:
        physical = path.resolve(strict=True)
        key = physical.as_posix()
        if key not in self.hash_cache:
            self.hash_cache[key] = (sha256(physical), physical.stat().st_size)
        digest, size = self.hash_cache[key]
        return physical, digest, size

    def add(
        self,
        path: Path,
        *,
        origin: dict[str, object],
        binding: dict[str, object] | None = None,
        report: dict[str, object] | None = None,
    ) -> str:
        physical, digest, size = self.file_identity(path)
        record = self.objects.setdefault(
            digest,
            {
                "sha256": digest,
                "bytes": size,
                "physical_sources": [],
                "origins": {},
                "bindings": {},
            },
        )
        sources = record["physical_sources"]
        assert isinstance(sources, list)
        if physical.as_posix() not in sources:
            sources.append(physical.as_posix())
        origins = record["origins"]
        assert isinstance(origins, dict)
        origins[origin_key(origin)] = origin
        if binding:
            bindings = record["bindings"]
            assert isinstance(bindings, dict)
            bindings[origin_key(binding)] = binding
        if report is not None:
            self.report_candidates.append({**report, "sha256": digest, "bytes": size})
        return digest


def direct_origin(path: Path, zone: str, authority: str) -> dict[str, object]:
    repository, relative = repo_relative(path)
    return {
        "repository": repository,
        "path": relative,
        "absolute_path": path.resolve().as_posix(),
        "source_zone": zone,
        "authority": authority,
    }


def direct_report_candidate(path: Path, zone: str) -> dict[str, object]:
    repository, relative = repo_relative(path)
    return {
        "name": path.name,
        "repository": repository,
        "origin_path": relative,
        "source_zone": zone,
        "document_role": "report_tree" if zone == "research_reports" else "verification_output",
        "campaign_id": None,
        "campaign_slug": None,
        "paper_artifact_id": None,
    }


def ingest_direct_roots(collector: Collector) -> None:
    roots = (
        (CELLA / "research/reports", "research_reports", "live_cella_reference_not_canon"),
        (CELLA / "research/verification", "research_verification", "live_cella_verification_reference"),
        (LLOYD / "research/reports", "research_reports", "retiring_lloyd_reference"),
        (LLOYD / "research/verification", "research_verification", "retiring_lloyd_verification_reference"),
    )
    for root, zone, authority in roots:
        for path in tree_files(root):
            report = None
            if zone == "research_reports":
                report = direct_report_candidate(path, zone)
            elif path.suffix.lower() in REPORT_OUTPUT_SUFFIXES or "verdict" in path.name.lower():
                report = direct_report_candidate(path, zone)
            collector.add(path, origin=direct_origin(path, zone, authority), report=report)


def ingest_campaign_library(collector: Collector) -> None:
    data = json.loads(CAMPAIGN_LEDGER.read_text(encoding="utf-8"))
    for artifact in data["artifacts"]:
        path = CELLA / "Campaign_Library" / artifact["library_path"]
        if not path.exists():
            raise FileNotFoundError(path)
        library_origin = {
            "repository": "Cella Framework",
            "path": f"Campaign_Library/{artifact['library_path']}",
            "absolute_path": path.absolute().as_posix(),
            "source_zone": "campaign_library",
            "authority": "organized_reference_copy",
        }
        binding = {
            "system": "Campaign_Library",
            "artifact_id": artifact["artifact_id"],
            "campaign_id": artifact["campaign_id"],
            "campaign_slug": artifact["campaign_slug"],
            "document_role": artifact["document_role"],
            "inbound_reference_count": artifact.get("inbound_reference_count", 0),
            "embedded_digest_matches": artifact.get("embedded_digest_matches", []),
        }
        report = None
        if artifact["document_role"] in CAMPAIGN_REPORT_ROLES:
            report = {
                "name": Path(artifact["library_path"]).name,
                "repository": "Cella Framework",
                "origin_path": f"Campaign_Library/{artifact['library_path']}",
                "source_zone": "campaign_library",
                "document_role": artifact["document_role"],
                "campaign_id": artifact["campaign_id"],
                "campaign_slug": artifact["campaign_slug"],
                "campaign_family": artifact["campaign_family"],
                "paper_artifact_id": artifact.get("papers_artifact_id"),
            }
        digest = collector.add(path, origin=library_origin, binding=binding, report=report)
        record = collector.objects[digest]
        origins = record["origins"]
        assert isinstance(origins, dict)
        for source_origin in artifact.get("origins", []):
            normalized = {
                "repository": source_origin.get("repository"),
                "path": source_origin.get("path"),
                "absolute_path": source_origin.get("absolute_path"),
                "source_zone": source_origin.get("source_zone", "campaign_origin"),
                "authority": source_origin.get("authority", "source_reference"),
            }
            origins[origin_key(normalized)] = normalized


def ingest_papers_evidence(collector: Collector) -> None:
    data = json.loads(PAPERS_LEDGER.read_text(encoding="utf-8"))
    for artifact in data["artifacts"]:
        if artifact["category"] != "07_certificates_data_and_reproducibility":
            continue
        path = CELLA / "Papers_Library" / artifact["library_path"]
        if not path.exists():
            raise FileNotFoundError(path)
        binding = {
            "system": "Papers_Library",
            "artifact_id": artifact["artifact_id"],
            "category": artifact["category"],
            "subject_family": artifact["subject_family"],
            "binding_count": len(artifact.get("bindings", [])),
        }
        origin = {
            "repository": "Cella Framework",
            "path": f"Papers_Library/{artifact['library_path']}",
            "absolute_path": path.absolute().as_posix(),
            "source_zone": "papers_library",
            "authority": "organized_reference_copy",
        }
        name_probe = normalize_probe(Path(artifact["library_path"]).name)
        is_report = any(normalize_probe(marker) in name_probe for marker in PAPER_REPORT_MARKERS)
        report = None
        if is_report:
            report = {
                "name": Path(artifact["library_path"]).name,
                "repository": "Cella Framework",
                "origin_path": f"Papers_Library/{artifact['library_path']}",
                "source_zone": "papers_library",
                "document_role": "certificate_or_support",
                "campaign_id": None,
                "campaign_slug": None,
                "paper_artifact_id": artifact["artifact_id"],
                "declared_subject_family": artifact["subject_family"],
            }
        digest = collector.add(path, origin=origin, binding=binding, report=report)
        record = collector.objects[digest]
        origins = record["origins"]
        assert isinstance(origins, dict)
        for source_origin in artifact.get("origins", []):
            normalized = {
                "repository": source_origin.get("repository"),
                "path": source_origin.get("path"),
                "absolute_path": source_origin.get("absolute_path"),
                "source_zone": "paper_evidence_origin",
                "authority": source_origin.get("authority", "source_reference"),
            }
            origins[origin_key(normalized)] = normalized


def ingest_preservation_receipts(collector: Collector) -> None:
    root = CELLA / "archive/retired-worktrees"
    for path in tree_files(root):
        report = None
        if "receipt" in path.name.lower():
            report = direct_report_candidate(path, "retired_worktree_preservation")
            report["document_role"] = "preservation_receipt"
        collector.add(
            path,
            origin=direct_origin(path, "retired_worktree_preservation", "historical_preservation_evidence"),
            report=report,
        )


def classify_report(candidate: dict[str, object]) -> tuple[str, str, str]:
    raw_probe = str(candidate.get("origin_path", "")) + "/" + str(candidate.get("name", ""))
    raw_probe = raw_probe.replace("research/reports/", "research/").replace("Reports_Library/", "")
    probe = normalize_probe(raw_probe)
    probe_tokens = set(probe.split("_"))

    def marked(*markers: str) -> bool:
        for marker in markers:
            normalized = normalize_probe(marker)
            if "_" in normalized:
                if normalized in probe:
                    return True
            elif normalized in probe_tokens:
                return True
        return False

    role = str(candidate.get("document_role", ""))
    zone = str(candidate.get("source_zone", ""))
    if marked("archive", "historical", "superseded", "legacy", "older_version", "retired_worktree"):
        return REPORT_CATEGORIES["historical"], "historical_report", "historical/archive path marker"
    if role == "audit" or marked("audit", "review", "methodology", "capability_map", "risk_note"):
        return REPORT_CATEGORIES["audit"], "audit_review_or_methodology", "audit/review/methodology marker"
    if role == "certificate" or zone == "research_verification" or marked("certificate", "certification", "verification", "verify", "receipt", "release_report", "gate", "verdict", "revalidation", "retest"):
        return REPORT_CATEGORIES["verification"], "verification_or_certificate_report", "verification/certificate/receipt marker"
    if marked("scratch", "search", "discovery", "probe", "conjecture", "negative", "kill", "investigation", "exploratory", "candidate"):
        return REPORT_CATEGORIES["exploratory"], "exploratory_or_negative_result", "search/probe/investigation marker"
    if role in {"report", "closeout", "claim"} or marked("report", "closeout", "campaign_output", "stage", "session"):
        return REPORT_CATEGORIES["campaign"], "campaign_or_stage_report", "campaign/report/closeout marker"
    return REPORT_CATEGORIES["data"], "machine_readout_or_supporting_data", "data output without stronger report marker"


def report_bundle(candidate: dict[str, object]) -> str:
    if candidate.get("campaign_slug"):
        campaign_id = str(candidate.get("campaign_id") or "CMP")
        return safe_slug(f"{campaign_id}_{candidate['campaign_slug']}")
    path = Path(str(candidate.get("origin_path", "")))
    parts = list(path.parts)
    if "reports" in parts:
        index = parts.index("reports") + 1
        while index < len(parts) and parts[index] in {"lloyd_v4", "research"}:
            index += 1
        if index < len(parts) - 1:
            return safe_slug(parts[index])
    if "verification" in parts:
        index = parts.index("verification") + 1
        if index < len(parts) - 1:
            return safe_slug(parts[index])
        return "verification_root"
    if candidate.get("paper_artifact_id"):
        return safe_slug(f"paper_evidence_{candidate['paper_artifact_id']}")
    return safe_slug(path.parent.name or "cross_program")


def report_subject(candidate: dict[str, object]) -> tuple[str, str]:
    declared = candidate.get("declared_subject_family")
    if declared:
        return str(declared), "declared by Papers Library ledger"
    return subject_family(
        str(candidate.get("campaign_slug", "")),
        str(candidate.get("campaign_family", "")),
        str(candidate.get("origin_path", "")),
        str(candidate.get("name", "")),
    )


def copy_object(source: Path, target: Path) -> str:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["cp", "--reflink=always", "--preserve=mode,timestamps", source.as_posix(), target.as_posix()],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        method = "btrfs_reflink"
    except (OSError, subprocess.CalledProcessError):
        shutil.copy2(source, target)
        method = "independent_copy"
    target.chmod(0o444)
    return method


def write_evidence_catalogue(objects: list[dict[str, object]], summary: dict[str, object]) -> None:
    ledger = {"schema_version": 1, "generated": now_iso(), **summary, "objects": objects}
    (EVIDENCE_CATALOGUE / "OBJECT_LEDGER.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    with (EVIDENCE_CATALOGUE / "OBJECT_LEDGER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("evidence_id", "sha256", "bytes", "object_path", "origin_count", "binding_count", "repository", "origin_path", "source_zone", "authority"))
        for obj in objects:
            for origin in obj["origins"]:
                writer.writerow((obj["evidence_id"], obj["sha256"], obj["bytes"], obj["object_path"], len(obj["origins"]), len(obj["bindings"]), origin.get("repository"), origin.get("path"), origin.get("source_zone"), origin.get("authority")))

    lines = [
        "# Evidence Store object ledger",
        "",
        f"Generated: `{ledger['generated']}`",
        "",
        f"- Unique SHA-256 objects: **{summary['object_count']}**",
        f"- Recorded origins: **{summary['origin_count']}**",
        f"- Path/campaign/paper bindings: **{summary['binding_count']}**",
        f"- Objects with recorded path consequences: **{summary['path_bound_object_count']}**",
        f"- Certificate-related objects: **{summary['certificate_related_object_count']}**",
        f"- Unique object bytes: **{summary['unique_object_bytes']:,}**",
        f"- Logical origin bytes: **{summary['logical_origin_bytes']:,}**",
        f"- Exact-identity duplication collapsed: **{summary['deduplicated_logical_bytes']:,} bytes**",
        "",
        "Objects are immutable references, not current Cella authority. Exact identity is SHA-256 only.",
        "",
        "Run `sha256sum --check _catalogue/SHA256SUMS` from the Evidence Store root to verify every object.",
        "",
    ]
    (EVIDENCE_CATALOGUE / "ORIGIN_AND_BINDING_LEDGER.md").write_text("\n".join(lines), encoding="utf-8")
    with (EVIDENCE_CATALOGUE / "SHA256SUMS").open("w", encoding="utf-8") as handle:
        for obj in objects:
            handle.write(f"{obj['sha256']}  {obj['object_path']}\n")


def write_reports_catalogue(reports: list[dict[str, object]], summary: dict[str, object]) -> None:
    ledger = {"schema_version": 1, "generated": now_iso(), **summary, "reports": reports}
    (REPORTS_CATALOGUE / "LEDGER.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    with (REPORTS_CATALOGUE / "LEDGER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("report_id", "category", "subject_family", "bundle", "report_role", "library_path", "evidence_id", "sha256", "bytes", "origin_count", "campaign_ids", "paper_artifact_ids"))
        for report in reports:
            writer.writerow((report["report_id"], report["category"], report["subject_family"], report["bundle"], report["report_role"], report["library_path"], report["evidence_id"], report["sha256"], report["bytes"], len(report["origins"]), ";".join(report["campaign_ids"]), ";".join(report["paper_artifact_ids"])))
    lines = [
        "# Reports to evidence lineage",
        "",
        f"Generated: `{ledger['generated']}`",
        "",
        f"- Report entries: **{summary['report_count']}**",
        f"- Unique Evidence Store objects referenced: **{summary['unique_evidence_object_count']}**",
        f"- Relative symlinks: **{summary['relative_symlink_count']}**",
        "",
        "Every report file is a relative symlink to an immutable SHA-256 object. Multiple logical report contexts may intentionally reference the same object.",
        "",
        "| Category | Entries |",
        "|---|---:|",
    ]
    for category, count in summary["category_counts"].items():
        lines.append(f"| `{category}` | {count} |")
    lines.append("")
    (REPORTS_CATALOGUE / "REPORT_EVIDENCE_LINEAGE.md").write_text("\n".join(lines), encoding="utf-8")


def write_readmes(summary: dict[str, object], report_summary: dict[str, object]) -> None:
    evidence_readme = f"""# Evidence Store

This is Cella's immutable, content-addressed evidence layer.

- Address: `SHA-256`
- Object layout: `objects/sha256/<first-two-hex>/<full-digest>`
- Unique objects: **{summary['object_count']}**
- Recorded origins: **{summary['origin_count']}**
- Storage: independent Btrfs reflinks where supported; ordinary copies otherwise

An object records bytes and provenance. It does **not** promote a historical result, campaign conclusion, certificate, or report into current Cella authority. Current claims remain governed by `STATE/`, `BOOT.md`, `ADMISSIONS.md`, and live verification.

Human-readable report paths live in `../Reports_Library` and resolve here through relative symlinks. See `_catalogue/OBJECT_LEDGER.json` for machine-readable origins and bindings.
"""
    reports_readme = f"""# Reports Library

This is the human-readable report view over `../Evidence_Store`.

- Report entries: **{report_summary['report_count']}**
- Unique evidence objects referenced: **{report_summary['unique_evidence_object_count']}**
- Storage mode: relative symlinks; report bytes are not duplicated

The tree separates campaign reports, verification/certification receipts, audits, exploratory results, machine readouts, and historical material. Subject families follow the terminology already used by the Papers and Campaign libraries.

Reports and receipts are references, not automatic proof or current authority. See `_catalogue/LEDGER.json` and `_catalogue/REPORT_EVIDENCE_LINEAGE.md` for provenance.
"""
    (EVIDENCE / "README.md").write_text(evidence_readme, encoding="utf-8")
    (REPORTS / "README.md").write_text(reports_readme, encoding="utf-8")


def build(*, apply: bool, replace: bool) -> dict[str, object]:
    collector = Collector()
    ingest_direct_roots(collector)
    ingest_campaign_library(collector)
    ingest_papers_evidence(collector)
    ingest_preservation_receipts(collector)

    digest_to_id = {digest: f"EVD-{index:06d}" for index, digest in enumerate(sorted(collector.objects), 1)}
    origin_count = sum(len(record["origins"]) for record in collector.objects.values())
    binding_count = sum(len(record["bindings"]) for record in collector.objects.values())
    unique_bytes = sum(int(record["bytes"]) for record in collector.objects.values())
    logical_bytes = sum(int(record["bytes"]) * len(record["origins"]) for record in collector.objects.values())
    source_zones = Counter(
        str(origin.get("source_zone", "unknown"))
        for record in collector.objects.values()
        for origin in record["origins"].values()
    )
    repositories = Counter(
        str(origin.get("repository", "unknown"))
        for record in collector.objects.values()
        for origin in record["origins"].values()
    )
    binding_systems = Counter(
        str(binding.get("system", "unknown"))
        for record in collector.objects.values()
        for binding in record["bindings"].values()
    )

    summary: dict[str, object] = {
        "source_policy": "non-destructive ingestion from both repositories and existing Papers/Campaign ledgers",
        "identity_policy": "exact SHA-256 identity only",
        "authority_policy": "stored evidence is reference material, not current Cella authority",
        "object_count": len(collector.objects),
        "origin_count": origin_count,
        "binding_count": binding_count,
        "unique_object_bytes": unique_bytes,
        "logical_origin_bytes": logical_bytes,
        "deduplicated_logical_bytes": logical_bytes - unique_bytes,
        "source_zone_origin_counts": dict(sorted(source_zones.items())),
        "repository_origin_counts": dict(sorted(repositories.items())),
        "binding_system_counts": dict(sorted(binding_systems.items())),
    }

    logical_reports: dict[tuple[str, str, str, str], list[dict[str, object]]] = defaultdict(list)
    for candidate in collector.report_candidates:
        category, role, basis = classify_report(candidate)
        subject, subject_basis = report_subject(candidate)
        bundle = report_bundle(candidate)
        logical_reports[(str(candidate["sha256"]), category, subject, bundle)].append(
            {**candidate, "category": category, "report_role": role, "classification_basis": basis, "subject_family": subject, "subject_basis": subject_basis, "bundle": bundle}
        )

    report_summary: dict[str, object] = {
        "report_count": len(logical_reports),
        "unique_evidence_object_count": len({key[0] for key in logical_reports}),
        "relative_symlink_count": len(logical_reports),
        "category_counts": dict(sorted(Counter(key[1] for key in logical_reports).items())),
    }

    if not apply:
        return {"evidence": summary, "reports": report_summary}

    if OBJECTS.exists() or REPORTS.exists():
        if not replace:
            raise SystemExit("Evidence objects or Reports_Library already exist; rerun with --replace after review")
        if OBJECTS.exists():
            shutil.rmtree(OBJECTS)
        if REPORTS.exists():
            shutil.rmtree(REPORTS)
    OBJECTS.mkdir(parents=True, exist_ok=True)
    EVIDENCE_CATALOGUE.mkdir(parents=True, exist_ok=True)
    REPORTS_CATALOGUE.mkdir(parents=True, exist_ok=True)

    object_records: list[dict[str, object]] = []
    storage_methods: Counter[str] = Counter()
    for digest in sorted(collector.objects):
        source_record = collector.objects[digest]
        source = Path(sorted(source_record["physical_sources"])[0])
        relative = Path("objects") / "sha256" / digest[:2] / digest
        target = EVIDENCE / relative
        method = copy_object(source, target)
        storage_methods[method] += 1
        if sha256(target) != digest:
            raise RuntimeError(f"object hash mismatch after copy: {target}")
        object_records.append(
            {
                "evidence_id": digest_to_id[digest],
                "sha256": digest,
                "bytes": source_record["bytes"],
                "object_path": relative.as_posix(),
                "storage_method": method,
                "path_bound": any(
                    int(binding.get("inbound_reference_count", 0) or 0) > 0
                    or int(binding.get("binding_count", 0) or 0) > 0
                    for binding in source_record["bindings"].values()
                ),
                "certificate_related": any(
                    binding.get("document_role") == "certificate"
                    or binding.get("category") == "07_certificates_data_and_reproducibility"
                    for binding in source_record["bindings"].values()
                ),
                "origins": sorted(source_record["origins"].values(), key=origin_key),
                "bindings": sorted(source_record["bindings"].values(), key=origin_key),
            }
        )
    summary["storage_method_counts"] = dict(sorted(storage_methods.items()))
    summary["path_bound_object_count"] = sum(bool(obj["path_bound"]) for obj in object_records)
    summary["certificate_related_object_count"] = sum(bool(obj["certificate_related"]) for obj in object_records)
    write_evidence_catalogue(object_records, summary)

    report_records: list[dict[str, object]] = []
    occupied: set[str] = set()
    sorted_groups = sorted(logical_reports.items(), key=lambda item: (item[0][1], item[0][2], item[0][3], item[0][0]))
    for index, ((digest, category, subject, bundle), candidates) in enumerate(sorted_groups, 1):
        report_id = f"RPT-{index:06d}"
        primary = sorted(candidates, key=lambda item: (item["repository"] != "Cella Framework", len(str(item["origin_path"])), str(item["origin_path"])))[0]
        filename = f"{report_id}__{safe_filename(str(primary['name']))}"
        relative = Path(category) / subject / bundle / filename
        if relative.as_posix() in occupied:
            relative = relative.with_name(f"{relative.stem}__{digest[:8]}{relative.suffix}")
        occupied.add(relative.as_posix())
        link = REPORTS / relative
        link.parent.mkdir(parents=True, exist_ok=True)
        object_path = EVIDENCE / "objects" / "sha256" / digest[:2] / digest
        link.symlink_to(os.path.relpath(object_path, start=link.parent))
        origins = sorted(
            {
                (str(item["repository"]), str(item["origin_path"]), str(item["source_zone"]))
                for item in candidates
            }
        )
        report_records.append(
            {
                "report_id": report_id,
                "category": category,
                "subject_family": subject,
                "subject_basis": primary["subject_basis"],
                "bundle": bundle,
                "report_role": primary["report_role"],
                "classification_basis": primary["classification_basis"],
                "library_path": relative.as_posix(),
                "evidence_id": digest_to_id[digest],
                "evidence_object_path": f"../Evidence_Store/objects/sha256/{digest[:2]}/{digest}",
                "sha256": digest,
                "bytes": primary["bytes"],
                "origins": [
                    {"repository": repository, "path": path, "source_zone": zone}
                    for repository, path, zone in origins
                ],
                "campaign_ids": sorted({str(item["campaign_id"]) for item in candidates if item.get("campaign_id")}),
                "paper_artifact_ids": sorted({str(item["paper_artifact_id"]) for item in candidates if item.get("paper_artifact_id")}),
            }
        )
    write_reports_catalogue(report_records, report_summary)
    write_readmes(summary, report_summary)
    return {"evidence": summary, "reports": report_summary}


def verify_generated() -> dict[str, object]:
    if not (EVIDENCE_CATALOGUE / "OBJECT_LEDGER.json").exists():
        raise SystemExit("Evidence Store ledger is missing")
    if not (REPORTS_CATALOGUE / "LEDGER.json").exists():
        raise SystemExit("Reports Library ledger is missing")

    evidence_ledger = json.loads((EVIDENCE_CATALOGUE / "OBJECT_LEDGER.json").read_text(encoding="utf-8"))
    report_ledger = json.loads((REPORTS_CATALOGUE / "LEDGER.json").read_text(encoding="utf-8"))
    object_failures: list[str] = []
    for obj in evidence_ledger["objects"]:
        path = EVIDENCE / obj["object_path"]
        if not path.is_file():
            object_failures.append(f"missing:{obj['object_path']}")
        elif path.name != obj["sha256"]:
            object_failures.append(f"misaddressed:{obj['object_path']}")
        elif sha256(path) != obj["sha256"]:
            object_failures.append(f"hash:{obj['object_path']}")

    link_failures: list[str] = []
    absolute_links = 0
    for report in report_ledger["reports"]:
        link = REPORTS / report["library_path"]
        if not link.is_symlink():
            link_failures.append(f"not_symlink:{report['library_path']}")
            continue
        target_text = os.readlink(link)
        if os.path.isabs(target_text):
            absolute_links += 1
        resolved = link.resolve(strict=False)
        expected = (EVIDENCE / "objects" / "sha256" / report["sha256"][:2] / report["sha256"]).resolve()
        if not resolved.is_file():
            link_failures.append(f"broken:{report['library_path']}")
        elif resolved != expected:
            link_failures.append(f"target:{report['library_path']}")

    collector = Collector()
    ingest_direct_roots(collector)
    ingest_campaign_library(collector)
    ingest_papers_evidence(collector)
    ingest_preservation_receipts(collector)
    source_digests = set(collector.objects)
    ledger_digests = {str(obj["sha256"]) for obj in evidence_ledger["objects"]}
    missing_source_digests = sorted(source_digests - ledger_digests)
    unexpected_ledger_digests = sorted(ledger_digests - source_digests)

    result = {
        "status": "PASS" if not (object_failures or link_failures or absolute_links or missing_source_digests or unexpected_ledger_digests) else "FAIL",
        "objects_checked": len(evidence_ledger["objects"]),
        "object_failures": object_failures,
        "report_links_checked": len(report_ledger["reports"]),
        "link_failures": link_failures,
        "absolute_symlink_count": absolute_links,
        "source_digest_count": len(source_digests),
        "missing_source_digests": missing_source_digests,
        "unexpected_ledger_digests": unexpected_ledger_digests,
    }
    if result["status"] != "PASS":
        raise SystemExit(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write the two libraries")
    parser.add_argument("--replace", action="store_true", help="replace generated object/report trees")
    parser.add_argument("--verify", action="store_true", help="verify objects, links, and source coverage")
    args = parser.parse_args()
    result = verify_generated() if args.verify else build(apply=args.apply, replace=args.replace)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
