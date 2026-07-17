"""Deterministic campaign opening over the Campaign Library and research DAG.

``scaffold_campaign`` reserves identifiers and writes derived staging records.
``commit_campaign`` is the only canonical write path and preserves the DAG
service's preview -> stage -> explicit apply trust boundary.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from .dag_service import (
    DagError,
    apply_bundle,
    canonical_graph_for_diff,
    dag_root,
    load_graph,
    materialize_submission,
    repository_root,
    submit_bundle,
    validate_artifact,
    validate_graph,
)


CAMPAIGN_SCHEMA = "cella-start-campaign-v1"
CAMPAIGN_ID_RE = re.compile(r"CMP-(\d{4,})")
ARTIFACT_ID_RE = re.compile(r"CMA-(\d{6,})")


def campaign_library_root() -> Path:
    override = os.environ.get("CELLA_CAMPAIGN_ROOT")
    return Path(override).resolve() if override else repository_root() / "Campaign_Library"


def staging_root() -> Path:
    override = os.environ.get("CELLA_CAMPAIGN_STAGING")
    return Path(override).resolve() if override else campaign_library_root() / "_staging"


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DagError("CAMPAIGN_RECORD_MISSING", f"missing campaign record: {path}", path=str(path)) from exc
    except json.JSONDecodeError as exc:
        raise DagError("CAMPAIGN_INVALID_JSON", f"invalid JSON in {path}: {exc}", path=str(path)) from exc


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("wb", dir=path.parent, delete=False) as handle:
        handle.write(_json_bytes(value))
        temporary = Path(handle.name)
    temporary.replace(path)


def _slugify(value: str) -> str:
    value = value.replace("&", " and ").replace("-", "")
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return re.sub(r"_+", "_", value) or "unnamed_campaign"


def _node_suffix(slug: str) -> str:
    pieces = [piece for piece in slug.split("_") if piece]
    return "".join(piece[0] for piece in pieces) if len(pieces) > 1 else slug


def _family_map() -> dict[str, str]:
    record = _read_json(repository_root() / "Artifact_Schemas" / "CAMPAIGN_FAMILY_MAP.json")
    return record.get("families", {})


def resolve_registry_family(subject_family: str) -> str:
    mapping = _family_map()
    if subject_family not in mapping:
        raise DagError(
            "UNKNOWN_CAMPAIGN_FAMILY",
            f"no Campaign Library mapping exists for DAG subject family {subject_family!r}",
            available=sorted(mapping),
        )
    return mapping[subject_family]


def _all_sidecars() -> list[Path]:
    root = campaign_library_root()
    paths = list(root.glob("[0-9][0-9]_*/*/*.artifact.json"))
    paths.extend(staging_root().glob("*/campaign.artifact.json"))
    return sorted(set(path.resolve() for path in paths if path.is_file()))


def _campaign_assignments() -> dict[str, str]:
    assignments: dict[str, str] = {}
    registry = campaign_library_root() / "_catalogue" / "CAMPAIGN_REGISTRY.md"
    if registry.is_file():
        for line in registry.read_text(encoding="utf-8").splitlines():
            match = re.match(r"\|\s*(CMP-\d+)\s*\|\s*`([^`]+)`", line)
            if match:
                assignments[match.group(2)] = match.group(1)
    for family in campaign_library_root().glob("[0-9][0-9]_*"):
        if not family.is_dir():
            continue
        for path in family.glob("CMP-*__*"):
            match = re.fullmatch(r"(CMP-\d+)__(.+)", path.name)
            if match:
                assignments.setdefault(match.group(2), match.group(1))
    for manifest in staging_root().glob("*/manifest.json"):
        try:
            record = _read_json(manifest)
        except DagError:
            continue
        if record.get("campaign_slug") and record.get("campaign_id"):
            assignments.setdefault(record["campaign_slug"], record["campaign_id"])
    return assignments


def _resolve_campaign_id(slug: str) -> str:
    assignments = _campaign_assignments()
    if slug in assignments:
        return assignments[slug]
    used = [int(match.group(1)) for value in assignments.values() if (match := CAMPAIGN_ID_RE.fullmatch(value))]
    return f"CMP-{max(used, default=0) + 1:04d}"


def _ledger_artifacts() -> dict[str, str | None]:
    path = campaign_library_root() / "_catalogue" / "LEDGER.json"
    if not path.is_file():
        return {}
    return {
        item["artifact_id"]: item.get("campaign_id")
        for item in _read_json(path).get("artifacts", [])
        if ARTIFACT_ID_RE.fullmatch(str(item.get("artifact_id", "")))
    }


def _resolve_artifact_id(campaign_id: str, existing: dict | None, slug: str) -> str:
    ledger = _ledger_artifacts()
    candidates: list[str] = []
    if existing:
        candidates.extend([str(existing.get("artifact_id", "")), str(existing.get("extensions", {}).get("cma_id", ""))])
    for manifest in staging_root().glob("*/manifest.json"):
        try:
            record = _read_json(manifest)
        except DagError:
            continue
        if record.get("campaign_slug") == slug:
            candidates.append(str(record.get("artifact_id", "")))
    for candidate in candidates:
        if ARTIFACT_ID_RE.fullmatch(candidate) and ledger.get(candidate) in {None, campaign_id}:
            return candidate
    used = set(ledger)
    for sidecar_path in _all_sidecars():
        try:
            record = _read_json(sidecar_path)
        except DagError:
            continue
        for candidate in (record.get("artifact_id"), record.get("extensions", {}).get("cma_id")):
            if ARTIFACT_ID_RE.fullmatch(str(candidate or "")):
                used.add(str(candidate))
    numbers = [int(match.group(1)) for value in used if (match := ARTIFACT_ID_RE.fullmatch(value))]
    return f"CMA-{max(numbers, default=0) + 1:06d}"


def _normalise_claims(claims: list[dict]) -> list[dict]:
    output = []
    for claim in claims:
        item = copy.deepcopy(claim)
        item.setdefault("hypotheses", [])
        item.setdefault("scope", "campaign scope")
        item.setdefault("proof_ids", [])
        item.setdefault("evidence_ids", [])
        output.append(item)
    return output


def _normalise_impacts(impacts: list[dict], relations: list[dict]) -> list[dict]:
    output = []
    for impact in impacts:
        item = copy.deepcopy(impact)
        item.setdefault("kind", "reevaluate")
        item.setdefault("target_id", None)
        output.append({key: item[key] for key in ("kind", "target_id", "note")})
    if not output:
        for relation in relations:
            output.append({
                "kind": "reevaluate",
                "target_id": relation["target_id"],
                "note": f"Opening the campaign declares a {relation['relation']} relation to {relation['target_id']}.",
            })
    return output


def _normalise_relations(raw_relations: list[dict]) -> list[dict]:
    output = []
    for relation in raw_relations:
        target = relation.get("target_id", relation.get("target"))
        if not relation.get("relation") or not target:
            raise DagError("BAD_CAMPAIGN_RELATION", "each relation requires relation and target_id")
        output.append({
            "relation": str(relation["relation"]),
            "target_id": str(target),
            "basis": str(relation.get("basis") or "Declared campaign dependency."),
            **({"source_pointer": relation["source_pointer"]} if "source_pointer" in relation else {}),
        })
    return output


def _sidecar_record(*, existing: dict | None, campaign_id: str, artifact_id: str,
                    node_id: str, title: str, summary: str, subject_family: str,
                    registry_family: str, relations: list[dict]) -> dict:
    source = copy.deepcopy(existing or {})
    provenance = source.get("provenance") or {
        "authors": [], "created_utc": None, "origin_repository": "Cella Framework", "source_pointer": None,
    }
    external_ids = copy.deepcopy(source.get("external_ids", {}))
    external_ids["campaigns"] = sorted(set(external_ids.get("campaigns", []) + [campaign_id]))
    external_ids["campaign_artifacts"] = sorted(set(external_ids.get("campaign_artifacts", []) + [artifact_id]))
    extensions = copy.deepcopy(source.get("extensions", {}))
    extensions.update({
        "cma_id": artifact_id,
        "campaign_id": campaign_id,
        "registry_family": registry_family,
        "dag_node_id": node_id,
    })
    if not provenance.get("authors"):
        extensions["todos"] = sorted(set(extensions.get("todos", []) + ["provenance.authors"]))
    llm = copy.deepcopy(source.get("llm", {}))
    llm.setdefault("one_sentence_purpose", summary)
    llm.setdefault("key_terms", [piece for piece in _slugify(title).split("_") if len(piece) > 2])
    llm.setdefault("retrieval_questions", [f"What does campaign {campaign_id} investigate?"])
    llm.setdefault("context_priority", "high")
    llm.setdefault("context_role", "frontier")
    sidecar_relations = relations if relations else _normalise_relations(source.get("relations", []))
    return {
        "schema_version": 1,
        "artifact_id": artifact_id,
        "artifact_type": "campaign",
        "title": title,
        "summary": summary,
        "subject_families": [subject_family],
        "claim_status": source.get("claim_status"),
        "lifecycle_status": source.get("lifecycle_status", "active"),
        "provenance": provenance,
        "files": copy.deepcopy(source.get("files", [])),
        "claims": _normalise_claims(source.get("claims", [])),
        "relations": sidecar_relations,
        "external_ids": external_ids,
        "declared_impacts": _normalise_impacts(source.get("declared_impacts", []), relations),
        "llm": llm,
        "visual_hints": copy.deepcopy(source.get("visual_hints", {})),
        "extensions": extensions,
    }


def _graph_records(*, graph: dict, sidecar: dict, campaign_id: str, artifact_id: str,
                   node_id: str, title: str, summary: str, subject_family: str,
                   registry_family: str, final_pointer: str, relations: list[dict],
                   promote_tracked: list[str]) -> tuple[list[dict], list[dict]]:
    nodes_by_id = {node["id"]: node for node in graph["nodes"]}
    known = set(nodes_by_id)
    relation_names = set(json.loads((repository_root() / "Artifact_Schemas/RELATION_REGISTRY.json").read_text())["relations"])
    sidecar_digest = hashlib.sha256(_json_bytes(sidecar)).hexdigest()
    node = {
        "id": node_id,
        "label": title,
        "type": "campaign",
        "claim_status": None,
        "lifecycle_status": "active",
        "reachability": None,
        "tracked": True,
        "layer": "frontier",
        "summary": summary,
        "source_refs": [{"pointer": final_pointer, "sha256": sidecar_digest}],
        "external_ids": {
            "encyclopedia": [],
            "paper_artifacts": [],
            "campaigns": [campaign_id],
            "campaign_artifacts": [artifact_id],
            "reports": [],
            "evidence": [],
            "retirement_packages": [],
            "artifacts": [artifact_id],
        },
        "facets": {
            "subject_family": subject_family,
            "campaign_family": registry_family,
            "source_id": "campaign-openings-v1",
        },
        "visual_hints": sidecar.get("visual_hints", {}),
        "retrieval": {
            "key_terms": copy.deepcopy(sidecar["llm"]["key_terms"]),
            "retrieval_questions": copy.deepcopy(sidecar["llm"]["retrieval_questions"]),
            "context_priority": sidecar["llm"]["context_priority"],
            "context_role": sidecar["llm"]["context_role"],
        },
        "extensions": {"opened_by": CAMPAIGN_SCHEMA},
    }
    upsert_nodes = [node]
    for target in promote_tracked:
        if target not in nodes_by_id:
            raise DagError("CAMPAIGN_TARGET_NOT_FOUND", f"cannot promote unknown node {target!r}")
        promoted = copy.deepcopy(nodes_by_id[target])
        promoted["tracked"] = True
        promoted["layer"] = "frontier"
        promoted.setdefault("retrieval", {})["context_role"] = "frontier"
        promoted.setdefault("extensions", {})["promoted_by_campaign"] = campaign_id
        upsert_nodes.append(promoted)
    edges = []
    for relation in relations:
        source = str(relation.get("from_id") or node_id)
        target = str(relation["target_id"])
        if relation["relation"] not in relation_names:
            raise DagError("UNKNOWN_RELATION", f"campaign relation {relation['relation']!r} is not registered")
        if source not in known and source != node_id:
            raise DagError("CAMPAIGN_TARGET_NOT_FOUND", f"unknown relation source {source!r}")
        if target not in known and target != node_id:
            raise DagError("CAMPAIGN_TARGET_NOT_FOUND", f"unknown relation target {target!r}")
        edges.append({
            "id": f"e::{source}::{relation['relation']}::{target}",
            "from": source,
            "to": target,
            "relation": relation["relation"],
            "label": f"{source} {relation['relation']} {target}",
            "basis": relation.get("basis"),
            "source_refs": [],
            "facets": {"source_id": "campaign-openings-v1", "campaign_id": campaign_id},
            "extensions": {},
        })
    return upsert_nodes, edges


def scaffold_campaign(*, title: str, subject_family: str, summary: str,
                      relations: list[dict] | None = None,
                      promote_tracked: list[str] | None = None,
                      existing_sidecar: str | None = None) -> dict:
    existing_path = Path(existing_sidecar).resolve() if existing_sidecar else None
    existing = _read_json(existing_path) if existing_path else None
    title = title or str((existing or {}).get("title", ""))
    summary = summary or str((existing or {}).get("summary", ""))
    if not title or not summary:
        raise DagError("CAMPAIGN_INPUT_REQUIRED", "title and summary are required")
    slug = _slugify(title)
    if existing_path:
        folder_match = re.fullmatch(r"CMP-\d+__(.+)", existing_path.parent.name)
        if folder_match:
            # Existing Campaign Library folders are canonical spelling
            # authorities; do not reinterpret their editorial hyphen choices.
            slug = folder_match.group(1)
    campaign_id = _resolve_campaign_id(slug)
    artifact_id = _resolve_artifact_id(campaign_id, existing, slug)
    registry_family = resolve_registry_family(subject_family)
    node_id = f"DBP:campaign:{_node_suffix(slug)}"
    supplied_relations = copy.deepcopy(relations or [])
    if not supplied_relations and existing:
        supplied_relations = copy.deepcopy(existing.get("relations", []))
    normalised_relations = []
    for relation in supplied_relations:
        target = relation.get("target_id", relation.get("target"))
        normalised_relations.append({
            "relation": relation.get("relation"),
            "target_id": target,
            "basis": relation.get("basis") or "Declared campaign dependency.",
            **({"from_id": relation["from_id"]} if relation.get("from_id") else {}),
        })
    sidecar_relations = [relation for relation in normalised_relations if relation.get("from_id", node_id) == node_id]
    sidecar = _sidecar_record(
        existing=existing, campaign_id=campaign_id, artifact_id=artifact_id, node_id=node_id,
        title=title, summary=summary, subject_family=subject_family,
        registry_family=registry_family, relations=sidecar_relations,
    )
    relative_folder = Path(registry_family) / f"{campaign_id}__{slug}"
    sidecar_name = f"{campaign_id}__{slug}.artifact.json"
    final_path = campaign_library_root() / relative_folder / sidecar_name
    pointer = "cella:" + (Path("Campaign_Library") / relative_folder / sidecar_name).as_posix()
    graph = load_graph()
    upsert_nodes, upsert_edges = _graph_records(
        graph=graph, sidecar=sidecar, campaign_id=campaign_id, artifact_id=artifact_id,
        node_id=node_id, title=title, summary=summary, subject_family=subject_family,
        registry_family=registry_family, final_pointer=pointer,
        relations=normalised_relations, promote_tracked=list(promote_tracked or []),
    )
    submission = {
        "schema_version": 1,
        "submission_id": f"start-campaign-{campaign_id.lower()}",
        "base_revision": graph["revision"],
        "idempotency_key": f"start-campaign:{campaign_id}:{artifact_id}",
        "submitted_by": "cella.start_campaign",
        "summary": f"Open {campaign_id}: {title}",
        "artifacts": [sidecar],
        "graph_delta": {
            "upsert_nodes": upsert_nodes,
            "upsert_edges": upsert_edges,
            "retire_nodes": [],
            "remove_edges": [],
        },
        "declared_impacts": sidecar["declared_impacts"],
        "extensions": {"campaign_id": campaign_id, "artifact_id": artifact_id, "scaffold_schema": CAMPAIGN_SCHEMA},
    }
    stage = staging_root() / f"{campaign_id}__{slug}"
    if existing_path:
        _atomic_json(stage / "input.artifact.json", existing)
    _atomic_json(stage / "campaign.artifact.json", sidecar)
    _atomic_json(stage / "submission.json", submission)
    manifest = {
        "schema": CAMPAIGN_SCHEMA,
        "campaign_id": campaign_id,
        "artifact_id": artifact_id,
        "campaign_slug": slug,
        "node_id": node_id,
        "subject_family": subject_family,
        "registry_family": registry_family,
        "staging_dir": str(stage),
        "final_folder": str(final_path.parent),
        "final_sidecar": str(final_path),
        "source_existing_sidecar": str(existing_path) if existing_path else None,
        "base_revision": graph["revision"],
        "promote_tracked": list(promote_tracked or []),
    }
    _atomic_json(stage / "manifest.json", manifest)
    return {**manifest, "ok": True, "written": [str(stage / name) for name in ("manifest.json", "campaign.artifact.json", "submission.json")]}


def _refresh_submission(stage: Path, manifest: dict, sidecar: dict) -> dict:
    submission = _read_json(stage / "submission.json")
    graph = load_graph()
    submission["base_revision"] = graph["revision"]
    submission["artifacts"] = [sidecar]
    node_id = manifest["node_id"]
    digest = hashlib.sha256(_json_bytes(sidecar)).hexdigest()
    for node in submission["graph_delta"]["upsert_nodes"]:
        if node.get("id") == node_id:
            node.setdefault("external_ids", {})["artifacts"] = [manifest["artifact_id"]]
            node["source_refs"] = [{
                "pointer": "cella:" + Path(manifest["final_sidecar"]).relative_to(repository_root()).as_posix(),
                "sha256": digest,
            }]
    return submission


def _already_committed(manifest: dict, sidecar: dict) -> bool:
    graph = load_graph()
    node = next((item for item in graph["nodes"] if item["id"] == manifest["node_id"]), None)
    if not node or manifest["artifact_id"] not in node.get("external_ids", {}).get("artifacts", []):
        return False
    final = Path(manifest["final_sidecar"])
    return final.is_file() and final.read_bytes() == _json_bytes(sidecar)


def _overlay_path() -> Path:
    return repository_root() / "research/campaigns/Succession_Map/campaign-openings-v1.json"


def _source_registry_path() -> Path:
    return repository_root() / "DAG_Library/SOURCE_REGISTRY.json"


def _campaign_overlay(submission: dict, manifest: dict) -> dict:
    path = _overlay_path()
    record = _read_json(path) if path.is_file() else {
        "schema_version": 1,
        "graph_id": "cella-campaign-openings-v1",
        "authority_policy": "Campaign openings are admitted only after the rebuild-and-diff gate proves source persistence.",
        "generator": "cella.start_campaign",
        "nodes": [],
        "edges": [],
        "node_patches": [],
    }
    node_id = manifest["node_id"]
    campaign_node = next(node for node in submission["graph_delta"]["upsert_nodes"] if node["id"] == node_id)
    nodes = {node["id"]: node for node in record.get("nodes", [])}
    nodes[node_id] = copy.deepcopy(campaign_node)
    edges = {edge["id"]: edge for edge in record.get("edges", [])}
    for edge in submission["graph_delta"]["upsert_edges"]:
        edges[edge["id"]] = copy.deepcopy(edge)
    patches = {patch["id"]: patch for patch in record.get("node_patches", [])}
    for target in manifest.get("promote_tracked", []):
        patches[target] = {
            "id": target,
            "set": {"tracked": True, "layer": "frontier"},
            "merge": {
                "retrieval": {"context_role": "frontier"},
                "extensions": {"promoted_by_campaign": manifest["campaign_id"]},
            },
        }
    record["nodes"] = [nodes[key] for key in sorted(nodes)]
    record["edges"] = [edges[key] for key in sorted(edges)]
    record["node_patches"] = [patches[key] for key in sorted(patches)]
    return record


def _updated_source_registry(overlay: dict) -> dict:
    path = _source_registry_path()
    registry = _read_json(path)
    overlay_path = _overlay_path()
    pointer = "cella:" + overlay_path.relative_to(repository_root()).as_posix()
    entry = {
        "source_id": "campaign-openings-v1",
        "pointer": pointer,
        "sha256": hashlib.sha256(_json_bytes(overlay)).hexdigest(),
        "role": "campaign_opening_overlay",
    }
    sources = [source for source in registry.get("sources", []) if source.get("source_id") != entry["source_id"]]
    crosswalks = [source for source in sources if source.get("role") == "external_id_crosswalk"]
    sources = [source for source in sources if source.get("role") != "external_id_crosswalk"]
    registry["sources"] = sources + [entry] + crosswalks
    return registry


def _resolve_registered_pointer(pointer: str) -> Path:
    if pointer.startswith("cella:"):
        return repository_root() / pointer.split(":", 1)[1]
    if pointer.startswith("encyclopedia:"):
        encyclopedia = Path(os.environ.get("CELLA_ENCYCLOPEDIA_ROOT", "/home/wlloyd/Lloyd_Mathematics_Encyclopedia"))
        return encyclopedia / pointer.split(":", 1)[1]
    raise DagError("UNSUPPORTED_SOURCE_POINTER", f"cannot rebuild registered source pointer {pointer!r}")


def _rebuild_diff_gate(submission: dict, registry: dict, work: Path) -> dict:
    expected = materialize_submission(submission)
    rebuilt_path = work / "rebuilt.json"
    command = [sys.executable, str(repository_root() / "engine/tools/build_dag_library.py")]
    crosswalk = None
    for source in registry.get("sources", []):
        path = _resolve_registered_pointer(source["pointer"])
        if not path.is_file():
            raise DagError("REGISTERED_SOURCE_MISSING", f"registered DAG source is missing: {path}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != source["sha256"]:
            raise DagError(
                "REGISTERED_SOURCE_DIGEST_MISMATCH",
                f"registered DAG source digest drifted: {path}",
                expected=source["sha256"], actual=digest,
            )
        if source.get("role") == "external_id_crosswalk":
            crosswalk = path
        else:
            command.extend(["--source", f"{source['source_id']}={path}"])
    if crosswalk:
        command.extend(["--crosswalk", str(crosswalk)])
    command.extend(["--out", str(rebuilt_path)])
    build = subprocess.run(command, cwd=repository_root(), text=True, capture_output=True)
    if build.returncode != 0:
        raise DagError(
            "CAMPAIGN_REBUILD_FAILED",
            "registered-source rebuild failed",
            stdout=build.stdout[-8000:], stderr=build.stderr[-8000:],
        )
    rebuilt = _read_json(rebuilt_path)
    expected_path = work / "expected.canonical.json"
    rebuilt_canonical_path = work / "rebuilt.canonical.json"
    _atomic_json(expected_path, canonical_graph_for_diff(expected))
    _atomic_json(rebuilt_canonical_path, canonical_graph_for_diff(rebuilt))
    diff = subprocess.run(
        ["git", "diff", "--no-index", "--exit-code", "--", str(expected_path), str(rebuilt_canonical_path)],
        cwd=repository_root(), text=True, capture_output=True,
    )
    if diff.returncode not in {0, 1}:
        raise DagError("CAMPAIGN_DIFF_FAILED", "git diff could not compare canonical rebuilds", stderr=diff.stderr[-4000:])
    return {
        "ok": diff.returncode == 0,
        "builder_stdout": build.stdout[-4000:],
        "expected_canonical": str(expected_path),
        "rebuilt_canonical": str(rebuilt_canonical_path),
        "diff": (diff.stdout + diff.stderr)[-12000:],
    }


def _snapshot(paths: list[Path]) -> dict[Path, bytes | None]:
    return {path: path.read_bytes() if path.is_file() else None for path in paths}


def _restore(snapshot: dict[Path, bytes | None]) -> None:
    for path, content in snapshot.items():
        if content is None:
            if path.is_file() or path.is_symlink():
                path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("wb", dir=path.parent, delete=False) as handle:
            handle.write(content)
            temporary = Path(handle.name)
        temporary.replace(path)


def commit_campaign(staging_dir: str, *, confirm: bool = False) -> dict:
    stage = Path(staging_dir).resolve()
    manifest = _read_json(stage / "manifest.json")
    if manifest.get("schema") != CAMPAIGN_SCHEMA:
        raise DagError("BAD_CAMPAIGN_SCAFFOLD", "staging manifest does not use the start-campaign schema")
    sidecar = _read_json(stage / "campaign.artifact.json")
    artifact_validation = validate_artifact(sidecar, verify_files=True)
    if not artifact_validation["ok"]:
        return {"schema": CAMPAIGN_SCHEMA, "ok": False, "gate": "artifact_validation", "validation": artifact_validation}
    already_committed = _already_committed(manifest, sidecar)
    submission = _refresh_submission(stage, manifest, sidecar)
    preview = submit_bundle(submission, dry_run=True)
    if not preview.get("accepted"):
        return {"schema": CAMPAIGN_SCHEMA, "ok": False, "gate": "submission_preview", "preview": preview}
    if not confirm:
        return {
            "schema": CAMPAIGN_SCHEMA,
            "ok": False,
            "committed": False,
            "error": {"token": "CONFIRMATION_REQUIRED", "message": "campaign commit requires confirm=true"},
            "campaign_id": manifest["campaign_id"],
            "artifact_id": manifest["artifact_id"],
            "impact": preview.get("impact"),
            "changes": preview.get("changes"),
        }
    final_path = Path(manifest["final_sidecar"])
    overlay_path = _overlay_path()
    registry_path = _source_registry_path()
    safe_submission = re.sub(r"[^A-Za-z0-9_.-]+", "_", submission["submission_id"]).strip("._")
    mutation_paths = [
        final_path,
        overlay_path,
        registry_path,
        dag_root() / "canonical/theorem-dag.json",
        dag_root() / "submissions/pending" / f"{safe_submission}.json",
        dag_root() / "submissions/applied" / f"{safe_submission}.json",
        dag_root() / "receipts" / f"{safe_submission}.receipt.json",
    ]
    before = _snapshot(mutation_paths)
    try:
        _atomic_json(final_path, sidecar)
        overlay = _campaign_overlay(submission, manifest)
        _atomic_json(overlay_path, overlay)
        registry = _updated_source_registry(overlay)
        _atomic_json(registry_path, registry)
        with tempfile.TemporaryDirectory(prefix="cella-campaign-rebuild-") as temporary:
            rebuild_gate = _rebuild_diff_gate(submission, registry, Path(temporary))
            if not rebuild_gate["ok"]:
                _restore(before)
                return {
                    "schema": CAMPAIGN_SCHEMA,
                    "ok": False,
                    "committed": False,
                    "rolled_back": True,
                    "gate": "rebuild_git_diff",
                    "error": {"token": "CAMPAIGN_REBUILD_DIFF", "message": "campaign does not survive deterministic registered-source rebuild"},
                    "rebuild": rebuild_gate,
                }
        if already_committed:
            registry["canonical_revision"] = load_graph()["revision"]
            _atomic_json(registry_path, registry)
            return {
                "schema": CAMPAIGN_SCHEMA, "ok": True, "committed": True,
                "idempotent_replay": True, "campaign_id": manifest["campaign_id"],
                "artifact_id": manifest["artifact_id"], "node_id": manifest["node_id"],
                "rebuild_gate": {"ok": True, "diff": ""},
            }
        staged = submit_bundle(submission, dry_run=False)
        if not staged.get("staged"):
            raise DagError("CAMPAIGN_SUBMISSION_STAGE_FAILED", "campaign submission did not stage", result=staged)
        applied = apply_bundle(submission["submission_id"], confirm=True)
        graph_validation = validate_graph(load_graph(), verify_files=True)
        if not graph_validation["ok"]:
            raise DagError("POST_CAMPAIGN_GRAPH_INVALID", "campaign applied but the full graph failed validation", validation=graph_validation)
        registry["canonical_revision"] = applied["receipt"]["applied_revision"]
        _atomic_json(registry_path, registry)
        return {
            "schema": CAMPAIGN_SCHEMA,
            "ok": True,
            "committed": True,
            "idempotent_replay": False,
            "campaign_id": manifest["campaign_id"],
            "artifact_id": manifest["artifact_id"],
            "node_id": manifest["node_id"],
            "final_sidecar": str(final_path),
            "impact": preview.get("impact"),
            "receipt_path": applied["receipt_path"],
            "applied_revision": applied["receipt"]["applied_revision"],
            "graph_validation": graph_validation,
            "rebuild_gate": {"ok": True, "diff": "", "source": str(overlay_path)},
        }
    except Exception:
        _restore(before)
        raise
