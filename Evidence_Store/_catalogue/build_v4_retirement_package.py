#!/usr/bin/env python3
"""Build and verify the manifest-first Lloyd Engine V4 retirement package."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tarfile
import tempfile
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


CELLA = Path("/home/wlloyd/Cella Framework")
V4 = Path("/home/wlloyd/Lloyd_Engine_V4")
TARGET = CELLA / "V4_Retirement_Package"
EVIDENCE_LEDGER = CELLA / "Evidence_Store/_catalogue/OBJECT_LEDGER.json"
REPORTS_LEDGER = CELLA / "Reports_Library/_catalogue/LEDGER.json"

SNAPSHOT_NAME = "Lloyd_Engine_V4_non_git_cold_recovery.tar.gz"
SKIP_TOP = {".git"}

REPORT_CATEGORY_LABELS = {
    "01_campaign_and_stage_reports": "campaign_and_stage_reports",
    "02_verification_certification_and_release_receipts": "verification_certification_and_release_receipts",
    "03_audits_reviews_and_methodology": "audits_reviews_and_methodology",
    "04_exploratory_searches_and_negative_results": "exploratory_searches_and_negative_results",
    "05_machine_readouts_tables_and_supporting_data": "machine_readouts_tables_and_supporting_data",
    "06_historical_and_superseded_reports": "historical_and_superseded_reports",
}

DOC_GROUPS = {
    "agent_training": "governance_and_training",
    "governance": "governance_and_training",
    "superpowers": "governance_and_training",
    "architecture": "architecture_and_reference",
    "reference": "architecture_and_reference",
    "legacy": "legacy_documentation",
    "tools": "documentation_tools",
}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_digest(value: object) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def git_output(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=V4, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout


def inventory_source() -> list[dict[str, object]]:
    members: list[dict[str, object]] = []
    for root, dirs, files in os.walk(V4, topdown=True, followlinks=False):
        root_path = Path(root)
        if root_path == V4:
            dirs[:] = sorted(name for name in dirs if name not in SKIP_TOP)
        else:
            dirs.sort()
        files.sort()
        for name in files:
            path = root_path / name
            relative = path.relative_to(V4).as_posix()
            info = path.lstat()
            if stat.S_ISREG(info.st_mode):
                members.append({
                    "path": relative,
                    "file_type": "regular",
                    "sha256": sha256_file(path),
                    "bytes": info.st_size,
                    "mode": stat.S_IMODE(info.st_mode),
                })
            elif stat.S_ISLNK(info.st_mode):
                target = os.readlink(path)
                members.append({
                    "path": relative,
                    "file_type": "symlink",
                    "sha256": sha256_bytes(target.encode("utf-8")),
                    "bytes": len(target.encode("utf-8")),
                    "mode": stat.S_IMODE(info.st_mode),
                    "link_target": target,
                })
            else:
                raise RuntimeError(f"unsupported source member type: {path}")
    return sorted(members, key=lambda item: str(item["path"]))


def evidence_indexes() -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    ledger = json.loads(EVIDENCE_LEDGER.read_text(encoding="utf-8"))
    by_digest: dict[str, dict[str, object]] = {}
    by_v4_path: dict[str, dict[str, object]] = {}
    for obj in ledger["objects"]:
        by_digest[obj["sha256"]] = obj
        for origin in obj["origins"]:
            if origin.get("repository") == "Lloyd_Engine_V4" and origin.get("path"):
                by_v4_path[str(origin["path"])] = obj
    return by_digest, by_v4_path


def report_indexes() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    ledger = json.loads(REPORTS_LEDGER.read_text(encoding="utf-8"))
    path_to_categories: dict[str, set[str]] = defaultdict(set)
    path_to_report_ids: dict[str, set[str]] = defaultdict(set)
    for report in ledger["reports"]:
        for origin in report["origins"]:
            if origin.get("repository") == "Lloyd_Engine_V4":
                path = str(origin["path"])
                path_to_categories[path].add(str(report["category"]))
                path_to_report_ids[path].add(str(report["report_id"]))
    return path_to_categories, path_to_report_ids


def package_key(path: str, report_categories: dict[str, set[str]]) -> tuple[str, str] | None:
    parts = Path(path).parts
    if path.startswith("research/campaigns/") and len(parts) >= 4:
        return "campaigns", parts[2]
    if path.startswith("research/reports/"):
        categories = sorted(report_categories.get(path, {"05_machine_readouts_tables_and_supporting_data"}))
        category = categories[0]
        return "reports", REPORT_CATEGORY_LABELS[category]
    if path.startswith("research/verification/"):
        if path.startswith("research/verification/legacy_evals/"):
            return "verification", "legacy_evaluators"
        if Path(path).suffix.lower() in {".py", ".sh"}:
            return "verification", "verification_harnesses"
        return "verification", "verification_outputs"
    if path.startswith("archive/") and len(parts) >= 2:
        if len(parts) == 2:
            return None
        return "archaeology", parts[1]
    if path.startswith("engine/"):
        return "legacy_engine", "legacy_engine_source"
    if path.startswith("docs/") and len(parts) >= 2:
        if len(parts) == 2:
            return None
        return "documentation", DOC_GROUPS.get(parts[1], "cross_program_documentation")
    if path.startswith("research/paper/") or path.startswith("research/derivations/"):
        return "papers", "papers_and_derivations"
    return None


def enrich_members(source: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[tuple[str, str], list[dict[str, object]]]]:
    by_digest, by_v4_path = evidence_indexes()
    report_categories, report_ids = report_indexes()
    controls: list[dict[str, object]] = []
    packages: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for item in source:
        enriched = dict(item)
        digest = str(item["sha256"])
        path = str(item["path"])
        obj = by_v4_path.get(path) or by_digest.get(digest)
        enriched.update({
            "evidence_id": obj.get("evidence_id") if obj else None,
            "evidence_origin_bound": path in by_v4_path,
            "path_bound": bool(obj.get("path_bound")) if obj else False,
            "certificate_related": bool(obj.get("certificate_related")) if obj else False,
            "report_ids": sorted(report_ids.get(path, set())),
        })
        key = package_key(path, report_categories)
        if key is None:
            controls.append(enriched)
        else:
            packages[key].append(enriched)
    campaign_root = V4 / "research/campaigns"
    if campaign_root.exists():
        for path in sorted(campaign_root.iterdir()):
            if path.is_dir():
                packages.setdefault(("campaigns", path.name), [])
    return sorted(controls, key=lambda item: str(item["path"])), packages


def package_records(packages: dict[tuple[str, str], list[dict[str, object]]]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for index, ((family, label), members) in enumerate(sorted(packages.items()), 1):
        package_id = f"V4PKG-{index:04d}"
        ordered = sorted(members, key=lambda item: str(item["path"]))
        records.append({
            "package_id": package_id,
            "family": family,
            "label": label,
            "manifest_path": f"manifests/{family}/{package_id}__{label}.json",
            "member_count": len(ordered),
            "logical_bytes": sum(int(item["bytes"]) for item in ordered),
            "evidence_covered_count": sum(bool(item["evidence_id"]) for item in ordered),
            "evidence_origin_bound_count": sum(bool(item["evidence_origin_bound"]) for item in ordered),
            "path_bound_count": sum(bool(item["path_bound"]) for item in ordered),
            "certificate_related_count": sum(bool(item["certificate_related"]) for item in ordered),
            "member_tree_sha256": canonical_digest([
                [item["path"], item["sha256"], item["bytes"], item["mode"], item["file_type"]]
                for item in ordered
            ]),
            "members": ordered,
        })
    return records


def reflink_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["cp", "--reflink=always", "--preserve=mode,timestamps", source.as_posix(), target.as_posix()],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        shutil.copy2(source, target)


def write_controls(root: Path, controls: list[dict[str, object]]) -> list[dict[str, object]]:
    written: list[dict[str, object]] = []
    for item in controls:
        if item["file_type"] != "regular":
            continue
        source = V4 / str(item["path"])
        target = root / "controls" / str(item["path"])
        reflink_copy(source, target)
        target.chmod(0o444)
        written.append({**item, "control_copy_path": target.relative_to(root).as_posix()})
    return written


def normalized_tar_info(path: Path, arcname: str) -> tarfile.TarInfo:
    info = tarfile.TarInfo(arcname)
    stat_result = path.lstat()
    info.mode = stat.S_IMODE(stat_result.st_mode)
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    if path.is_symlink():
        info.type = tarfile.SYMTYPE
        info.linkname = os.readlink(path)
        info.size = 0
    elif path.is_dir():
        info.type = tarfile.DIRTYPE
        info.size = 0
    elif path.is_file():
        info.type = tarfile.REGTYPE
        info.size = stat_result.st_size
    else:
        raise RuntimeError(f"unsupported snapshot member: {path}")
    return info


def create_snapshot(target: Path) -> None:
    with target.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", compresslevel=1, fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                root_name = V4.name
                archive.addfile(normalized_tar_info(V4, root_name))
                for walk_root, dirs, files in os.walk(V4, topdown=True, followlinks=False):
                    walk_path = Path(walk_root)
                    if walk_path == V4:
                        dirs[:] = sorted(name for name in dirs if name not in SKIP_TOP)
                    else:
                        dirs.sort()
                    files.sort()
                    for name in dirs:
                        path = walk_path / name
                        arcname = f"{root_name}/{path.relative_to(V4).as_posix()}"
                        archive.addfile(normalized_tar_info(path, arcname))
                    for name in files:
                        path = walk_path / name
                        arcname = f"{root_name}/{path.relative_to(V4).as_posix()}"
                        info = normalized_tar_info(path, arcname)
                        if path.is_file() and not path.is_symlink():
                            with path.open("rb") as handle:
                                archive.addfile(info, handle)
                        else:
                            archive.addfile(info)


def verify_snapshot(snapshot: Path, source_members: list[dict[str, object]]) -> dict[str, object]:
    expected = {str(item["path"]): item for item in source_members}
    seen: set[str] = set()
    failures: list[str] = []
    with tarfile.open(snapshot, "r:gz") as archive:
        for member in archive:
            prefix = f"{V4.name}/"
            if not member.name.startswith(prefix) or member.isdir():
                continue
            relative = member.name[len(prefix):]
            item = expected.get(relative)
            if item is None:
                failures.append(f"unexpected:{relative}")
                continue
            seen.add(relative)
            if member.isfile():
                extracted = archive.extractfile(member)
                assert extracted is not None
                digest = hashlib.sha256()
                for block in iter(lambda: extracted.read(1024 * 1024), b""):
                    digest.update(block)
                if digest.hexdigest() != item["sha256"]:
                    failures.append(f"hash:{relative}")
            elif member.issym():
                if sha256_bytes(member.linkname.encode("utf-8")) != item["sha256"]:
                    failures.append(f"symlink:{relative}")
            else:
                failures.append(f"type:{relative}")
    for missing in sorted(set(expected) - seen):
        failures.append(f"missing:{missing}")
    return {
        "status": "PASS" if not failures else "FAIL",
        "member_count": len(seen),
        "expected_member_count": len(expected),
        "failures": failures,
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def generate_checksums(root: Path) -> int:
    files = sorted(path for path in root.rglob("*") if path.is_file() and path.name != "SHA256SUMS")
    with (root / "SHA256SUMS").open("w", encoding="utf-8") as handle:
        for path in files:
            handle.write(f"{sha256_file(path)}  {path.relative_to(root).as_posix()}\n")
    return len(files)


def build(*, apply: bool, replace: bool = False) -> dict[str, object]:
    source_before = inventory_source()
    controls, grouped = enrich_members(source_before)
    packages = package_records(grouped)
    source_bytes = sum(int(item["bytes"]) for item in source_before)
    summary = {
        "source_member_count": len(source_before),
        "source_bytes": source_bytes,
        "package_count": len(packages),
        "package_member_count": sum(int(pkg["member_count"]) for pkg in packages),
        "package_bytes": sum(int(pkg["logical_bytes"]) for pkg in packages),
        "control_member_count": len(controls),
        "control_bytes": sum(int(item["bytes"]) for item in controls),
        "evidence_covered_member_count": sum(bool(item["evidence_id"]) for pkg in packages for item in pkg["members"]),
        "evidence_origin_bound_member_count": sum(bool(item["evidence_origin_bound"]) for pkg in packages for item in pkg["members"]),
        "package_family_counts": dict(sorted(Counter(str(pkg["family"]) for pkg in packages).items())),
    }
    if not apply:
        return summary
    if TARGET.exists() and not replace:
        raise SystemExit(f"target already exists: {TARGET}")

    staging = Path(tempfile.mkdtemp(prefix=".V4_Retirement_Package.staging.", dir=CELLA))
    try:
        for package in packages:
            manifest_path = staging / str(package["manifest_path"])
            write_json(manifest_path, {
                "schema_version": 1,
                "authority": "historical V4 retirement reference; not current Cella authority",
                **package,
            })

        written_controls = write_controls(staging, controls)
        status_text = git_output("status", "--porcelain=v1", "--untracked-files=all")
        status_path = staging / "controls/SOURCE_GIT_STATUS.txt"
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status_path.write_text(status_text, encoding="utf-8")

        snapshot_path = staging / "cold_recovery" / SNAPSHOT_NAME
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        create_snapshot(snapshot_path)
        snapshot_verification = verify_snapshot(snapshot_path, source_before)
        if snapshot_verification["status"] != "PASS":
            raise RuntimeError(json.dumps(snapshot_verification, indent=2))

        source_after = inventory_source()
        if canonical_digest(source_before) != canonical_digest(source_after):
            raise RuntimeError("V4 source changed during snapshot construction")

        snapshot_record = {
            "path": snapshot_path.relative_to(staging).as_posix(),
            "sha256": sha256_file(snapshot_path),
            "bytes": snapshot_path.stat().st_size,
            "compression": "deterministic gzip level 1 over normalized PAX tar",
            "excluded": [".git/"],
            "source_tree_sha256": canonical_digest(source_before),
            "verification": snapshot_verification,
        }
        ledger = {
            "schema_version": 1,
            "generated": now_iso(),
            "mode": "manifest_first_with_single_cold_recovery_snapshot",
            "source_repository": V4.as_posix(),
            "source_git_head": git_output("rev-parse", "HEAD").strip(),
            "source_git_branch": git_output("branch", "--show-current").strip(),
            "source_git_status_sha256": sha256_bytes(status_text.encode("utf-8")),
            "authority_policy": "V4 packages are historical references; live Cella STATE and verification remain authoritative",
            **summary,
            "snapshot": snapshot_record,
            "controls": written_controls,
            "packages": [{key: value for key, value in pkg.items() if key != "members"} for pkg in packages],
        }
        write_json(staging / "PACKAGE_LEDGER.json", ledger)
        write_json(staging / "SNAPSHOT_MANIFEST.json", {"schema_version": 1, "source_tree_sha256": snapshot_record["source_tree_sha256"], "members": source_before})

        with (staging / "ORIGIN_PATH_MAP.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(("original_path", "disposition", "package_id", "sha256", "bytes", "evidence_id", "evidence_origin_bound", "path_bound", "certificate_related", "report_ids"))
            package_by_path = {
                str(item["path"]): (str(pkg["package_id"]), item)
                for pkg in packages for item in pkg["members"]
            }
            control_by_path = {str(item["path"]): item for item in written_controls}
            for item in source_before:
                path = str(item["path"])
                if path in package_by_path:
                    package_id, enriched = package_by_path[path]
                    disposition = "MANIFEST_PACKAGE_MEMBER"
                else:
                    package_id = ""
                    enriched = control_by_path.get(path, item)
                    disposition = "READABLE_CONTROL_COPY"
                writer.writerow((path, disposition, package_id, item["sha256"], item["bytes"], enriched.get("evidence_id"), enriched.get("evidence_origin_bound", False), enriched.get("path_bound", False), enriched.get("certificate_related", False), ";".join(enriched.get("report_ids", []))))

        readme = f"""# Lloyd Engine V4 retirement package

This package replaces a loose-file retirement strategy with **{summary['package_count']} deterministic package manifests**, readable control copies, and one verified non-Git cold-recovery snapshot.

- Source members: **{summary['source_member_count']}**
- Manifest-packaged members: **{summary['package_member_count']}**
- Individually readable controls: **{summary['control_member_count']}**
- Members already represented in the Evidence Store: **{summary['evidence_covered_member_count']}**
- Cold snapshot: `{snapshot_record['path']}`
- Snapshot SHA-256: `{snapshot_record['sha256']}`

Package manifests do not duplicate their member payloads. They bind original V4 paths to SHA-256 identities, Evidence Store IDs where available, report IDs, path consequences, and certificate status. The cold snapshot is the single physical reconstruction fallback and preserves the exact non-Git V4 tree as built.

Nothing here promotes V4 results into current Cella authority. Consult `PACKAGE_LEDGER.json`, `ORIGIN_PATH_MAP.csv`, and `SHA256SUMS` before any source retirement.
"""
        (staging / "README.md").write_text(readme, encoding="utf-8")
        gate = f"""# Retirement gate

Status: **PACKAGE BUILT; SOURCE DELETION NOT PERFORMED**

- Package manifests: {summary['package_count']}
- Packaged source members: {summary['package_member_count']}
- Readable control members: {summary['control_member_count']}
- Snapshot verification: {snapshot_verification['status']}
- Source changed during build: no

Before deleting V4 source paths, commit or externally back up this directory, verify `SHA256SUMS`, preserve Git history separately, and update live path consumers to resolve through `ORIGIN_PATH_MAP.csv`.
"""
        (staging / "RETIREMENT_GATE.md").write_text(gate, encoding="utf-8")
        checksum_count = generate_checksums(staging)
        if TARGET.exists():
            backup = CELLA / f".V4_Retirement_Package.previous.{os.getpid()}"
            os.replace(TARGET, backup)
            try:
                os.replace(staging, TARGET)
            except Exception:
                os.replace(backup, TARGET)
                raise
            shutil.rmtree(backup)
        else:
            os.replace(staging, TARGET)
        return {**summary, "snapshot": snapshot_record, "checksum_file_count": checksum_count, "target": TARGET.as_posix()}
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def verify() -> dict[str, object]:
    ledger = json.loads((TARGET / "PACKAGE_LEDGER.json").read_text(encoding="utf-8"))
    snapshot_manifest = json.loads((TARGET / "SNAPSHOT_MANIFEST.json").read_text(encoding="utf-8"))
    failures: list[str] = []

    for package in ledger["packages"]:
        path = TARGET / package["manifest_path"]
        if not path.is_file():
            failures.append(f"missing_manifest:{package['manifest_path']}")
            continue
        manifest = json.loads(path.read_text(encoding="utf-8"))
        calculated = canonical_digest([
            [item["path"], item["sha256"], item["bytes"], item["mode"], item["file_type"]]
            for item in manifest["members"]
        ])
        if calculated != package["member_tree_sha256"]:
            failures.append(f"manifest_tree:{package['package_id']}")

    for control in ledger["controls"]:
        path = TARGET / control["control_copy_path"]
        if not path.is_file() or sha256_file(path) != control["sha256"]:
            failures.append(f"control:{control['path']}")

    snapshot = TARGET / ledger["snapshot"]["path"]
    if not snapshot.is_file() or sha256_file(snapshot) != ledger["snapshot"]["sha256"]:
        failures.append("snapshot_checksum")
        snapshot_result = {"status": "FAIL", "failures": ["snapshot_checksum"]}
    else:
        snapshot_result = verify_snapshot(snapshot, snapshot_manifest["members"])
        if snapshot_result["status"] != "PASS":
            failures.extend(snapshot_result["failures"])

    checksum_failures: list[str] = []
    for line in (TARGET / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        path = TARGET / relative
        if not path.is_file() or sha256_file(path) != expected:
            checksum_failures.append(relative)
    failures.extend(f"checksum:{path}" for path in checksum_failures)
    result = {
        "status": "PASS" if not failures else "FAIL",
        "package_count": len(ledger["packages"]),
        "manifest_member_count": sum(int(pkg["member_count"]) for pkg in ledger["packages"]),
        "control_count": len(ledger["controls"]),
        "snapshot": snapshot_result,
        "checksum_entries_checked": len((TARGET / "SHA256SUMS").read_text(encoding="utf-8").splitlines()),
        "failures": failures,
    }
    if failures:
        raise SystemExit(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = verify() if args.verify else build(apply=args.apply, replace=args.replace)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
