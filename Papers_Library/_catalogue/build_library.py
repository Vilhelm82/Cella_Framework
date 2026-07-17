#!/usr/bin/env python3
"""Build the non-destructive Cella Papers Library from both repository trees."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


CELLA = Path("/home/wlloyd/Cella Framework")
LLOYD = Path("/home/wlloyd/Lloyd_Engine_V4")
LIBRARY = CELLA / "Papers_Library"
CATALOGUE = LIBRARY / "_catalogue"

ALLOWED_SUFFIXES = {
    ".md", ".txt", ".tex", ".pdf", ".docx", ".html",
    ".py", ".m2", ".json", ".jsonl", ".csv", ".tsv",
    ".out", ".pin", ".zip", ".png", ".jpg", ".svg",
}

TEXT_SUFFIXES = {".md", ".txt", ".tex", ".html", ".py", ".m2", ".json", ".jsonl", ".csv", ".tsv", ".out", ".pin"}

SKIP_NAMES = {".~lock.patent_photonic_provisional_draft.docx#"}
SKIP_PARTS = {".git", ".claude", ".venv", "node_modules", "STATE", "__pycache__", ".pytest_cache", "Papers_Library"}

CATEGORIES = {
    "completed": "01_completed_papers",
    "theorem": "02_theorems_and_lemmas",
    "proof": "03_proofs_derivations_and_audits",
    "draft": "04_drafts_and_incomplete_papers",
    "companion": "05_expository_companions_and_research_maps",
    "hypothesis": "06_hypotheses_conjectures_and_research_programs",
    "certificate": "07_certificates_data_and_reproducibility",
    "patent": "08_patents_and_invention_disclosures",
    "historical": "09_historical_and_superseded_versions",
}

SUBJECT_RULES = (
    ("photonic_and_sensor_inventions", ("patent", "photonic", "sensor invention")),
    ("galois_horizon_and_kummer_covers", ("galois", "horizon", "kummer", "wreath", "quintic", "macaulay", "crown", "monodromy", "root_closure", "entropy", "abel_ruffini", "abel-ruffini", "total_reality", "generic_descent", "morse_lemma", "allk", "pointa", "emergence_ledger", "prior_art")),
    ("dbp_periods_landen_and_elliptic_structure", ("landen", "legendre", "relative_period", "relative period", "elliptic", "pinning", "periods_of_the_dbp")),
    ("precision_flow_and_transfer_functions", ("precision_flow", "precision flow", "transfer_function", "transfer-function", "algebraic branch points", "pred006")),
    ("local_curvature_and_black_hole_metrics", ("local_curvature", "local curvature", "lead7", "kerr", "newman", "black_hole", "black hole", "pfc_", "pole_orders", "masscharge", "curvature_valence", "/cv_", "kn_three_face", "collision_field")),
    ("dbp_role_channel_and_orbit_geometry", ("dbp", "role_channel", "role channel", "rolechspec", "orbit_calculus", "orbit calculus", "gauge_channel", "three_channel", "three channel", "self_glue", "curvature_role", "selected_quotient", "theorem_8_1", "canonical_invariant", "invariant_maximality", "role_singularity", "coupling_native_kg")),
    ("geometric_fault_localization_and_decomposition", ("mean curvature", "decomposition", "fault localization", "bilinear", "gradient_irreducibility", "gradient irreducibility", "monge", "two lights", "essential dimension", "alexandrov", "interaction curvature", "symmetric polynomial", "shape_witness", "deficit_engine", "cradle_arm", "rank_hc", "dual_confinement", "gradient_focusing", "taxonomy_of_distortion", "isotropy_locus")),
    ("cella_residue_and_coupling_theory", ("cella", "residue", "coupling_field", "coupling field", "invariant tower", "fault geometry", "arithmetic_track", "arith_i", "holonomy", "normal_form", "localization", "shape_moment", "transport_law", "numerator_tower", "open_pins")),
    ("general_relativity_and_gravity", ("general relativity", "gr_", "gr ", "photon sphere", "thermodynamic")),
)

PATH_RE = re.compile(
    r"(?:/home/wlloyd/(?:Cella Framework|Lloyd_Engine_V4)/[^`\"'<>\n]+?"
    r"|(?:[A-Za-z0-9_.() -]+/)+[A-Za-z0-9_.() -]+?)"
    r"\.(?:md|txt|tex|pdf|docx|html|py|m2|json|jsonl|csv|tsv|out|pin|zip)",
    re.IGNORECASE,
)
SHA256_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", re.IGNORECASE)


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def eligible(path: Path) -> bool:
    return (
        path.is_file()
        and not path.is_symlink()
        and path.name not in SKIP_NAMES
        and (path.suffix.lower() in ALLOWED_SUFFIXES or path.name.lower().endswith(".bak"))
        and not any(part in SKIP_PARTS for part in path.parts)
    )


def add_tree(target: set[Path], root: Path, predicate=None) -> None:
    if not root.exists():
        return
    for path in root.rglob("*"):
        if eligible(path) and (predicate is None or predicate(path)):
            target.add(path.resolve())


def keyword_candidate(path: Path) -> bool:
    text = path.as_posix().lower()
    words = (
        "paper", "theorem", "proof", "lemma", "derivation", "calculus",
        "galois", "kummer", "wreath", "horizon", "landen", "legendre",
        "curvature", "monodromy", "role", "channel", "dbp", "precision_flow",
        "transfer_function", "closeoff", "foundation", "certificate", "verify",
        "recert", "arith_i", "lead7", "review", "normal_form", "localization",
    )
    return any(word in text for word in words)


def paper_document_candidate(path: Path) -> bool:
    if path.suffix.lower() not in {".md", ".txt", ".html", ".tex", ".pdf", ".docx"}:
        return False
    name = path.name.lower().replace("-", "_")
    full = path.as_posix().lower()
    title_markers = (
        "paper", "whitepaper", "theorem", "proof", "lemma", "derivation",
        "conjecture", "hypothesis", "research_map", "research_log",
        "calc_log", "standing_results", "claim_ledger", "companion",
    )
    if any(marker in name for marker in title_markers):
        return True
    research_roles = (
        "report", "prereg", "brief", "handoff", "closeout", "close_",
        "manifest", "citations", "disposition", "formula", "axiom",
        "glossary", "historical_record", "roadmap", "revision_plan",
    )
    research_domains = (
        "paper", "theorem", "proof", "conjecture", "precision_flow",
        "transfer_function", "rolechspec", "shape_witness", "galois",
        "horizon", "kummer", "dbp", "curvature", "monodromy", "landen",
    )
    return any(role in name for role in research_roles) and any(domain in full for domain in research_domains)


def direct_support_reference(origin: Path, resolved: Path) -> bool:
    support_suffixes = {".py", ".m2", ".json", ".jsonl", ".csv", ".tsv", ".out", ".pin", ".zip", ".png", ".jpg", ".svg"}
    support_markers = ("certificate", "verify", "gate", "digest", "sha256", "pin", "output", "result", "fixture")
    return (
        resolved.parent == origin.parent
        or resolved.suffix.lower() in support_suffixes
        or any(marker in resolved.name.lower() for marker in support_markers)
    )


def discover() -> set[Path]:
    paths: set[Path] = set()

    # Primary paper and theorem corpora.
    for root in (
        CELLA / "research/paper",
        CELLA / "research/derivations",
        CELLA / "archive/Reference_Material/Theorems and Papers Library",
        CELLA / "archive/Reference_Material/papers",
        CELLA / "docs/files",
        CELLA / "docs/galois_horizon_cover_v1_0_publication_package",
        CELLA / "docs/m2_out_2026-07-10",
        CELLA / "docs/scripts",
        LLOYD / "research/paper",
        LLOYD / "research/derivations",
        LLOYD / "research/reports/lloyd_v4/transfer_function_paper_v5_revalidation",
        LLOYD / "research/reports/lloyd_v4/precision_flow",
        LLOYD / "archive/attic/paper_v5_work_2026-05-30",
    ):
        add_tree(paths, root)

    # Campaign-local theorem/proof corpora and their direct certificates.
    for root in (
        CELLA / "research/campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR",
        CELLA / "research/campaigns/CV_curvature_valence",
        CELLA / "research/campaigns/PFC_local_calculus",
        CELLA / "research/campaigns/LEAD7_dbp_metric",
    ):
        add_tree(paths, root)

    add_tree(
        paths,
        CELLA / "research/campaigns/CELLA_CONTINUATION_ENGINE",
        keyword_candidate,
    )
    add_tree(paths, CELLA / "research/reports", keyword_candidate)
    add_tree(paths, CELLA / "research/verification", keyword_candidate)
    add_tree(paths, CELLA / "lead7_test8_gate_dump")
    add_tree(paths, CELLA / "engine/tests", lambda path: path.name.startswith(("verify_", "gate_dbp_", "gate_legendre_")))
    add_tree(paths, CELLA, paper_document_candidate)
    add_tree(paths, LLOYD, paper_document_candidate)

    # Portable release artifacts adjacent to selected roots.
    for path in (
        CELLA / "docs/galois_horizon_cover_v1_0_publication_package.zip",
        CELLA / "docs/files/Archive.zip",
        CELLA / "docs/files/files.zip",
    ):
        if eligible(path):
            paths.add(path.resolve())

    # Pull in directly path-referenced certificate/support files without broadening
    # the library to unrelated engine or benchmark material.
    by_name, _ = all_repo_files()
    for _ in range(1):
        additions: set[Path] = set()
        for origin in paths:
            content = text_content(origin)
            if not content:
                continue
            for token in PATH_RE.findall(content):
                resolved = resolve_reference(token, origin, by_name)
                if resolved is not None and eligible(resolved) and direct_support_reference(origin, resolved):
                    additions.add(resolved)
        additions -= paths
        if not additions:
            break
        paths.update(additions)

    return paths


def repo_and_relative(path: Path) -> tuple[str, Path, Path]:
    if path.is_relative_to(CELLA):
        return "Cella Framework", CELLA, path.relative_to(CELLA)
    return "Lloyd_Engine_V4", LLOYD, path.relative_to(LLOYD)


def origin_priority(path: Path) -> tuple[int, int, str]:
    repo, _, relative = repo_and_relative(path)
    rel = relative.as_posix()
    rules = (
        "research/paper/",
        "docs/galois_horizon_cover_v1_0_publication_package/",
        "docs/files/",
        "research/derivations/",
        "research/campaigns/",
        "research/reports/",
        "archive/Reference_Material/papers/current/",
        "archive/Reference_Material/Theorems and Papers Library/",
        "archive/Reference_Material/papers/",
    )
    rank = next((index for index, prefix in enumerate(rules) if rel.startswith(prefix)), len(rules))
    if repo == "Lloyd_Engine_V4":
        rank += 20
    return rank, len(rel), rel


def subject(path: Path) -> tuple[str, str]:
    _, _, relative = repo_and_relative(path)
    probe = relative.as_posix().lower().replace("-", "_")
    for family, tokens in SUBJECT_RULES:
        hits = [token for token in tokens if token.replace("-", "_") in probe]
        if hits:
            return family, "path tokens: " + ", ".join(hits[:4])
    return "cross_program_and_unclassified", "no subject token rule matched"


def classify(path: Path) -> tuple[str, str, str]:
    lower = path.as_posix().lower()
    name = path.name.lower()
    suffix = path.suffix.lower()

    if "patent" in lower or re.match(r"lloyd-\d", name):
        return CATEGORIES["patent"], "patent_or_invention", "patent path or filing identifier"
    if any(token in lower for token in ("older_versions", ".bak", "pre_dichotomy", "archive/old_program_sources", "archive/attic", "archive/superseded_docs", "reference_material/audits")):
        return CATEGORIES["historical"], "historical_version", "archive/backup path marker"
    if suffix in {".py", ".m2", ".json", ".jsonl", ".csv", ".tsv", ".out", ".pin", ".zip", ".png", ".jpg", ".svg"} or any(
        token in name for token in ("certificate", "verify", "results", "output", "digest", "sha256", "pointa")
    ) or "/certificates/" in lower or "m2_out_" in lower or ".out." in name:
        return CATEGORIES["certificate"], "certificate_or_support", "executable/data/certificate format or filename"
    if any(token in lower for token in ("tier_3_hypotheses", "hypothesis", "conjecture", "engagement")):
        return CATEGORIES["hypothesis"], "hypothesis_or_conjecture", "hypothesis/conjecture path or title"
    if any(token in name for token in ("draft", "v0_", "brief", "skeleton", "plan", "strategy", "roadmap", "handoff", "kill_search", "publishing_runbook", "stage1", "stage2", "stage3")):
        return CATEGORIES["draft"], "draft_or_incomplete", "draft/version/plan marker"
    if any(token in name for token in ("proof", "derivation", "audit_report", "closeoff", "calculus_companion")):
        return CATEGORIES["proof"], "proof_derivation_or_audit", "proof/derivation/audit marker"
    if any(token in name for token in ("research_map", "research_log", "strategic_direction", "emergence_ledger", "prior_art", "companion", "narrative")):
        return CATEGORIES["companion"], "companion_or_research_map", "companion/map/ledger marker"
    if any(token in name for token in ("theorem", "lemma", "law", "correspondence", "prohibition", "confinement", "hierarchy", "irreducibility")) or "tier_1_proven" in lower or "tier_2_derived" in lower:
        return CATEGORIES["theorem"], "theorem_or_lemma", "theorem/lemma/law path or title"
    if suffix in {".pdf", ".tex", ".docx"} or "paper" in name or "complete_v" in name:
        return CATEGORIES["completed"], "paper_source_or_render", "paper format/title without draft marker"
    return CATEGORIES["companion"], "supporting_exposition", "documentary artifact without stronger status marker"


def safe_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._() +-]+", "_", name).strip()
    return cleaned or "artifact"


def text_content(path: Path) -> str:
    if path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > 5_000_000:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def all_repo_files() -> tuple[dict[str, list[Path]], dict[str, Path]]:
    by_name: dict[str, list[Path]] = defaultdict(list)
    by_absolute: dict[str, Path] = {}
    for root in (CELLA, LLOYD):
        for path in root.rglob("*"):
            if path.is_file() and not any(part in SKIP_PARTS for part in path.parts):
                resolved = path.resolve()
                by_name[path.name].append(resolved)
                by_absolute[resolved.as_posix()] = resolved
    return dict(by_name), by_absolute


def resolve_reference(token: str, origin: Path, by_name: dict[str, list[Path]]) -> Path | None:
    cleaned = token.strip("`'\"()[]{}.,;: ").replace("\\ ", " ")
    candidate = Path(cleaned)
    attempts = []
    if candidate.is_absolute():
        attempts.append(candidate)
    else:
        attempts.extend((origin.parent / candidate, CELLA / candidate, LLOYD / candidate))
    for attempt in attempts:
        try:
            resolved = attempt.resolve()
        except OSError:
            continue
        if resolved.is_file():
            return resolved
    matches = by_name.get(candidate.name, [])
    return matches[0] if len(matches) == 1 else None


def filename_tokens(path: str) -> set[str]:
    stop = {"the", "and", "for", "with", "from", "v1", "v2", "v0", "report", "paper", "theorem", "proof", "complete", "draft"}
    return {
        token for token in re.findall(r"[a-z0-9]+", Path(path).stem.lower())
        if len(token) >= 3 and token not in stop and not token.isdigit()
    }


def build(dry_run: bool) -> dict[str, object]:
    discovered = discover()
    grouped: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(discovered):
        grouped[sha256(path)].append(path)

    records = []
    destination_claims: dict[str, str] = {}
    hash_to_id: dict[str, str] = {}
    origin_to_id: dict[str, str] = {}

    for number, digest in enumerate(sorted(grouped, key=lambda item: origin_priority(min(grouped[item], key=origin_priority))), start=1):
        origins = sorted(grouped[digest], key=origin_priority)
        preferred = origins[0]
        category, role, category_basis = classify(preferred)
        family, subject_basis = subject(preferred)
        filename = safe_name(preferred.name)
        relative_destination = Path(category) / family / filename
        key = relative_destination.as_posix().lower()
        if key in destination_claims and destination_claims[key] != digest:
            filename = f"{Path(filename).stem}__{digest[:8]}{Path(filename).suffix}"
            relative_destination = Path(category) / family / filename
            key = relative_destination.as_posix().lower()
        destination_claims[key] = digest

        artifact_id = f"PAP-{number:04d}"
        hash_to_id[digest] = artifact_id
        origin_rows = []
        for origin in origins:
            repo, _, relative = repo_and_relative(origin)
            authority = "active_or_contextual_cella" if repo == "Cella Framework" and not relative.as_posix().startswith("archive/") else "historical_reference"
            if repo == "Lloyd_Engine_V4":
                authority = "retirement_source"
            origin_rows.append(
                {
                    "repository": repo,
                    "path": relative.as_posix(),
                    "absolute_path": origin.as_posix(),
                    "authority": authority,
                }
            )
            origin_to_id[origin.as_posix()] = artifact_id

        records.append(
            {
                "artifact_id": artifact_id,
                "title": preferred.stem,
                "category": category,
                "subject_family": family,
                "role": role,
                "library_path": relative_destination.as_posix(),
                "sha256": digest,
                "bytes": preferred.stat().st_size,
                "format": preferred.suffix.lower().lstrip(".") or "none",
                "classification_basis": category_basis,
                "subject_basis": subject_basis,
                "origins": origin_rows,
                "mirror_count": len(origin_rows),
                "embedded_sha256": [],
                "bindings": [],
            }
        )

    by_name, _ = all_repo_files()
    record_by_id = {record["artifact_id"]: record for record in records}

    # Explicit path and digest bindings mined from every origin text.
    for record in records:
        seen_bindings = set()
        embedded = set()
        for origin_row in record["origins"]:
            origin = Path(origin_row["absolute_path"])
            content = text_content(origin)
            if not content:
                continue
            embedded.update(match.lower() for match in SHA256_RE.findall(content))
            for token in PATH_RE.findall(content):
                resolved = resolve_reference(token, origin, by_name)
                if resolved is None:
                    continue
                target_id = origin_to_id.get(resolved.as_posix())
                target_record = record_by_id.get(target_id) if target_id else None
                lower_name = resolved.name.lower()
                relation = "path_reference"
                if any(word in lower_name for word in ("cert", "verify", "gate", "digest", "sha", "pin", "output", "result")):
                    relation = "certificate_or_digest_path"
                binding_key = (relation, resolved.as_posix(), target_id)
                if binding_key in seen_bindings:
                    continue
                seen_bindings.add(binding_key)
                repo, _, relative = repo_and_relative(resolved) if resolved.is_relative_to(CELLA) or resolved.is_relative_to(LLOYD) else ("external", resolved.parent, Path(resolved.name))
                record["bindings"].append(
                    {
                        "relation": relation,
                        "target_artifact_id": target_id,
                        "target_library_path": target_record["library_path"] if target_record else None,
                        "target_origin_repository": repo,
                        "target_origin_path": relative.as_posix(),
                        "evidence": f"literal path in {origin_row['repository']}:{origin_row['path']}",
                    }
                )
        record["embedded_sha256"] = sorted(embedded)
        for digest in sorted(embedded):
            target_id = hash_to_id.get(digest)
            if not target_id or target_id == record["artifact_id"]:
                continue
            target_record = record_by_id[target_id]
            record["bindings"].append(
                {
                    "relation": "embedded_digest_match",
                    "target_artifact_id": target_id,
                    "target_library_path": target_record["library_path"],
                    "target_origin_repository": None,
                    "target_origin_path": None,
                    "evidence": f"embedded SHA-256 {digest}",
                }
            )

    # Source/render pairing and conservative certificate-family inference.
    stem_groups: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    certificates_by_subject: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in records:
        stem_groups[(record["subject_family"], Path(record["library_path"]).stem.lower())].append(record)
        if record["category"] == CATEGORIES["certificate"]:
            certificates_by_subject[record["subject_family"]].append(record)

    for members in stem_groups.values():
        formats = {record["format"] for record in members}
        if len(members) < 2 or not ({"tex", "pdf"} <= formats or {"docx", "pdf"} <= formats):
            continue
        for source in members:
            for target in members:
                if source is target:
                    continue
                relation = "same_stem_source_render_pair"
                if not any(binding.get("target_artifact_id") == target["artifact_id"] and binding.get("relation") == relation for binding in source["bindings"]):
                    source["bindings"].append(
                        {
                            "relation": relation,
                            "target_artifact_id": target["artifact_id"],
                            "target_library_path": target["library_path"],
                            "target_origin_repository": None,
                            "target_origin_path": None,
                            "evidence": "same subject family and exact filename stem with source/render formats",
                        }
                    )

    for record in records:
        if record["category"] in {CATEGORIES["certificate"], CATEGORIES["historical"]}:
            continue
        source_tokens = filename_tokens(record["library_path"])
        if not source_tokens:
            continue
        candidates = []
        for certificate in certificates_by_subject.get(record["subject_family"], []):
            overlap = source_tokens & filename_tokens(certificate["library_path"])
            if len(overlap) >= 2:
                candidates.append((len(overlap), certificate, overlap))
        for _, certificate, overlap in sorted(candidates, key=lambda item: (-item[0], item[1]["artifact_id"]))[:8]:
            if any(binding.get("target_artifact_id") == certificate["artifact_id"] for binding in record["bindings"]):
                continue
            record["bindings"].append(
                {
                    "relation": "certificate_family_binding_inferred",
                    "target_artifact_id": certificate["artifact_id"],
                    "target_library_path": certificate["library_path"],
                    "target_origin_repository": None,
                    "target_origin_path": None,
                    "evidence": "shared subject plus filename tokens: " + ", ".join(sorted(overlap)),
                }
            )

    if not dry_run:
        expected = {record["library_path"] for record in records}
        for category in CATEGORIES.values():
            category_root = LIBRARY / category
            if not category_root.exists():
                continue
            for existing in category_root.rglob("*"):
                if existing.is_file() and existing.relative_to(LIBRARY).as_posix() not in expected:
                    existing.unlink()
            for directory in sorted((path for path in category_root.rglob("*") if path.is_dir()), reverse=True):
                if not any(directory.iterdir()):
                    directory.rmdir()
        for record in records:
            destination = LIBRARY / record["library_path"]
            source = Path(record["origins"][0]["absolute_path"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                if sha256(destination) != record["sha256"]:
                    raise RuntimeError(f"library collision with different content: {destination}")
            else:
                shutil.copy2(source, destination)

    summary = {
        "schema_version": 1,
        "generated": date.today().isoformat(),
        "mode": "dry_run" if dry_run else "applied",
        "source_policy": "non-destructive copies; originals unchanged",
        "artifact_count": len(records),
        "origin_count": sum(record["mirror_count"] for record in records),
        "exact_mirrors_collapsed": sum(record["mirror_count"] - 1 for record in records),
        "categories": dict(sorted(Counter(record["category"] for record in records).items())),
        "subjects": dict(sorted(Counter(record["subject_family"] for record in records).items())),
        "artifacts_with_bindings": sum(bool(record["bindings"] or record["embedded_sha256"]) for record in records),
        "artifacts": records,
    }

    if not dry_run:
        write_catalogue(summary)
    return summary


def write_catalogue(summary: dict[str, object]) -> None:
    CATALOGUE.mkdir(parents=True, exist_ok=True)
    (CATALOGUE / "LEDGER.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    with (CATALOGUE / "LEDGER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("artifact_id", "category", "subject_family", "role", "library_path", "sha256", "bytes", "mirror_count", "origin_repository", "origin_path", "binding_count", "embedded_sha256_count"))
        for record in summary["artifacts"]:
            for origin in record["origins"]:
                writer.writerow((
                    record["artifact_id"], record["category"], record["subject_family"], record["role"],
                    record["library_path"], record["sha256"], record["bytes"], record["mirror_count"],
                    origin["repository"], origin["path"], len(record["bindings"]), len(record["embedded_sha256"]),
                ))

    lines = [
        "# Papers Library origin and binding ledger",
        "",
        f"Generated: {summary['generated']}",
        "",
        f"- Unique library artifacts: **{summary['artifact_count']}**",
        f"- Original source paths represented: **{summary['origin_count']}**",
        f"- Exact mirror copies collapsed: **{summary['exact_mirrors_collapsed']}**",
        f"- Artifacts with path, certificate, render-pair, or embedded-digest bindings: **{summary['artifacts_with_bindings']}**",
        "",
        "The JSON ledger is authoritative for complete origin arrays and binding evidence.",
        "",
        "## Category and subject index",
        "",
        "| ID | Category | Subject | Library copy | Origins | Bindings | SHA-256 |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for record in summary["artifacts"]:
        lines.append(
            f"| {record['artifact_id']} | `{record['category']}` | `{record['subject_family']}` | `{record['library_path']}` | {record['mirror_count']} | {len(record['bindings']) + len(record['embedded_sha256'])} | `{record['sha256']}` |"
        )

    lines.extend(("", "## Bound artifacts", ""))
    for record in summary["artifacts"]:
        if not record["bindings"] and not record["embedded_sha256"]:
            continue
        lines.append(f"### {record['artifact_id']} — `{record['library_path']}`")
        lines.append("")
        for digest in record["embedded_sha256"]:
            lines.append(f"- embedded SHA-256: `{digest}`")
        for binding in record["bindings"]:
            target = binding["target_artifact_id"] or f"{binding['target_origin_repository']}:{binding['target_origin_path']}"
            lines.append(f"- `{binding['relation']}` → `{target}` — {binding['evidence']}")
        lines.append("")

    (CATALOGUE / "ORIGIN_AND_BINDING_LEDGER.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    readme = f"""# Cella Papers Library

This is a non-destructive, digest-addressed library assembled from the active Cella
repository and the retired Lloyd Engine V4 tree. Originals remain in place.

The library contains **{summary['artifact_count']} unique artifacts** representing
**{summary['origin_count']} original paths**. Exact mirrors are stored once and every
origin is retained in `_catalogue/LEDGER.json`.

## Categories

| Directory | Meaning |
|---|---|
| `01_completed_papers/` | Paper sources and rendered papers without draft markers |
| `02_theorems_and_lemmas/` | Theorem, lemma, law, correspondence, and derived-result statements |
| `03_proofs_derivations_and_audits/` | Proofs, derivations, closeoffs, and claim-level audits |
| `04_drafts_and_incomplete_papers/` | Drafts, staged manuscripts, briefs, plans, and unfinished publication work |
| `05_expository_companions_and_research_maps/` | Companions, maps, ledgers, logs, and explanatory notes |
| `06_hypotheses_conjectures_and_research_programs/` | Explicit hypotheses, conjectures, and open research programmes |
| `07_certificates_data_and_reproducibility/` | Verifiers, scripts, outputs, digests, packages, and certificate data |
| `08_patents_and_invention_disclosures/` | Patent filings, provisional drafts, and invention material |
| `09_historical_and_superseded_versions/` | Backups and explicitly older program-source versions |

Within every category, artifacts are grouped by subject family. Placement describes
the artifact's documentary role, not Cella canonical status or mathematical validity.

## Ledgers

- `_catalogue/LEDGER.json` — complete machine-readable record.
- `_catalogue/LEDGER.csv` — one row per origin path.
- `_catalogue/ORIGIN_AND_BINDING_LEDGER.md` — human index and digest/certificate bindings.
- `_catalogue/build_library.py` — reproducible builder.
"""
    (LIBRARY / "README.md").write_text(readme, encoding="utf-8")


def verify_library() -> dict[str, object]:
    ledger_path = CATALOGUE / "LEDGER.json"
    retirement_path = CATALOGUE / "RETIREMENT_DELETION_RECEIPT.json"
    errors: list[str] = []
    if not ledger_path.is_file():
        raise SystemExit(f"missing ledger: {ledger_path}")

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    records = ledger["artifacts"]
    retired_entries = []
    if retirement_path.is_file():
        retired_entries = json.loads(retirement_path.read_text(encoding="utf-8"))["deletions"]
    retired = {(entry["repository"], entry["origin_path"]): entry for entry in retired_entries}
    ids = {record["artifact_id"] for record in records}
    if len(ids) != len(records):
        errors.append("artifact IDs are not unique")

    origin_rows = 0
    live_origin_rows = 0
    retired_origin_rows = 0
    for record in records:
        destination = LIBRARY / record["library_path"]
        if not destination.is_file():
            errors.append(f"missing library copy: {record['library_path']}")
            continue
        if destination.stat().st_size != record["bytes"]:
            errors.append(f"library size mismatch: {record['library_path']}")
        if sha256(destination) != record["sha256"]:
            errors.append(f"library digest mismatch: {record['library_path']}")
        expected_prefix = Path(record["category"]) / record["subject_family"]
        if not Path(record["library_path"]).is_relative_to(expected_prefix):
            errors.append(f"taxonomy mismatch: {record['library_path']}")

        for origin in record["origins"]:
            origin_rows += 1
            source = Path(origin["absolute_path"])
            retirement = retired.get((origin["repository"], origin["path"]))
            if not source.is_file():
                if retirement is None:
                    errors.append(f"missing origin: {source}")
                elif retirement["artifact_id"] != record["artifact_id"] or retirement["sha256"] != record["sha256"] or retirement["bytes"] != record["bytes"] or retirement["library_path"] != record["library_path"]:
                    errors.append(f"retirement receipt disagrees with ledger: {source}")
                else:
                    retired_origin_rows += 1
                continue
            if retirement is not None:
                errors.append(f"retired origin still exists: {source}")
                continue
            live_origin_rows += 1
            if source.stat().st_size != record["bytes"] or sha256(source) != record["sha256"]:
                errors.append(f"origin no longer matches recorded copy: {source}")
            if source.stat().st_dev == destination.stat().st_dev and source.stat().st_ino == destination.stat().st_ino:
                errors.append(f"library copy is not independent of origin: {source}")

        for binding in record["bindings"]:
            target_id = binding["target_artifact_id"]
            if target_id and target_id not in ids:
                errors.append(f"unknown binding target {target_id} from {record['artifact_id']}")
            elif target_id:
                target = next(item for item in records if item["artifact_id"] == target_id)
                if binding["target_library_path"] != target["library_path"]:
                    errors.append(f"binding path disagrees with target {target_id} from {record['artifact_id']}")
            elif binding["target_origin_repository"] in {"Cella Framework", "Lloyd_Engine_V4"}:
                root = CELLA if binding["target_origin_repository"] == "Cella Framework" else LLOYD
                if not (root / binding["target_origin_path"]).is_file():
                    errors.append(f"missing external binding target from {record['artifact_id']}: {root / binding['target_origin_path']}")

    if len(records) != ledger["artifact_count"]:
        errors.append("artifact count disagrees with ledger summary")
    if origin_rows != ledger["origin_count"]:
        errors.append("origin count disagrees with ledger summary")
    if origin_rows - len(records) != ledger["exact_mirrors_collapsed"]:
        errors.append("mirror-collapse count disagrees with ledger summary")
    if retired_origin_rows != len(retired):
        errors.append("retirement receipt contains an origin absent from the ledger")

    with (CATALOGUE / "LEDGER.csv").open(newline="", encoding="utf-8") as handle:
        csv_rows = sum(1 for _ in csv.DictReader(handle))
    if csv_rows != origin_rows:
        errors.append("CSV origin-row count disagrees with JSON ledger")

    current = build(dry_run=True)
    recorded_origins = {
        (origin["repository"], origin["path"], record["sha256"])
        for record in records
        for origin in record["origins"]
        if (origin["repository"], origin["path"]) not in retired
    }
    current_origins = {
        (origin["repository"], origin["path"], record["sha256"])
        for record in current["artifacts"]
        for origin in record["origins"]
    }
    if recorded_origins != current_origins:
        errors.append("source inventory has drifted since the ledger was generated")

    report = {
        "status": "pass" if not errors else "fail",
        "artifact_copies_verified": len(records),
        "origin_paths_recorded": origin_rows,
        "live_origin_paths_verified": live_origin_rows,
        "retired_origin_paths_verified": retired_origin_rows,
        "binding_targets_verified": sum(len(record["bindings"]) for record in records),
        "independent_copy_check": "pass" if not any("not independent" in error for error in errors) else "fail",
        "inventory_drift_check": "pass" if "source inventory has drifted since the ledger was generated" not in errors else "fail",
        "errors": errors,
    }
    if errors:
        print(json.dumps(report, indent=2))
        raise SystemExit(1)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--apply", action="store_true", help="copy artifacts and write ledgers")
    action.add_argument("--verify", action="store_true", help="verify all copies, origins, ledgers, and bindings")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify_library(), indent=2))
        return
    summary = build(dry_run=not args.apply)
    print(json.dumps({key: summary[key] for key in ("mode", "artifact_count", "origin_count", "exact_mirrors_collapsed", "categories", "subjects", "artifacts_with_bindings")}, indent=2))


if __name__ == "__main__":
    main()
