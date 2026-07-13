"""Gate the hostile Pathfinder benchmark campaign.

Run:  PYTHONPATH=src python tests/gate_pathfinder_hostile_benchmark.py
Skip: PYTHONPATH=src python tests/gate_pathfinder_hostile_benchmark.py --skip-hostile
   or CELLA_SKIP_HOSTILE_BENCHMARK=1 with the normal command.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

if "--skip-hostile" in sys.argv or os.environ.get("CELLA_SKIP_HOSTILE_BENCHMARK") == "1":
    print("GATE PATHFINDER HOSTILE BENCHMARK: SKIPPED - explicit skip flag set.")
    sys.exit(0)

FAILS: list[str] = []


def check(name: str, ok: bool) -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


try:
    from cella.hostile_benchmark import DEFAULT_MANIFEST, load_manifest, run_manifest
except Exception as exc:
    print(f"GATE PATHFINDER HOSTILE BENCHMARK: OPEN - import failed: {exc}")
    sys.exit(1)


manifest = load_manifest(DEFAULT_MANIFEST)
case_ids = {case["id"] for case in manifest["cases"]}
families = {case["family"] for case in manifest["cases"]}

check(
    "HB1 manifest contains the required hostile families",
    {
        "arithmetic_cancellation",
        "symbolic_swell",
        "local_geometry",
        "dbp_channel",
        "period_residue",
    } <= families
    and len(case_ids) >= 10,
)

check(
    "HB2 manifest includes concrete regression handles from the design",
    {
        "arith_constant_offset",
        "arith_sqrt_conjugate",
        "arith_unresolved_cos",
        "symbolic_rational_normal_form",
        "pfc_parity_fixed",
        "pfc_corner_wedge",
        "dbp_stage_c_channel_predicate",
        "dbp_regular_gi_zero",
        "dbp_n5_carrier_required",
        "period_residue_lane_reserved",
        "hog_lead7_reflection_coefficients",
        "hog_lead7_schwarzschild_corner",
        "hog_pfc_vertex_rule",
    } <= case_ids,
)

with tempfile.TemporaryDirectory() as tmp:
    out_path = Path(tmp) / "hostile-report.json"
    report = run_manifest(DEFAULT_MANIFEST, out_path)
    persisted = json.loads(out_path.read_text(encoding="utf-8"))

check(
    "HB3 runner writes a report with one result bundle per case",
    persisted["summary"]["case_count"] == len(manifest["cases"])
    and len(persisted["cases"]) == len(manifest["cases"])
    and persisted["summary"] == report["summary"],
)

pathfinder_results = {
    case["id"]: case["engines"]["cella_pathfinder"]
    for case in report["cases"]
}

check(
    "HB4 Pathfinder wins the arithmetic route cases by early process selection",
    pathfinder_results["arith_constant_offset"]["status"] == "pass"
    and pathfinder_results["arith_constant_offset"]["route"]["decision"] == "rewrite_candidate_needed"
    and pathfinder_results["arith_sqrt_conjugate"]["route"]["decision"] == "rewrite_candidate_needed",
)

check(
    "HB5 Pathfinder records unresolved precision instead of inventing a rewrite",
    pathfinder_results["arith_unresolved_cos"]["status"] == "pass"
    and pathfinder_results["arith_unresolved_cos"]["route"]["decision"] == "precision_budget_needed",
)

check(
    "HB6 Pathfinder routes local geometry by normal form, not global expansion",
    pathfinder_results["pfc_parity_fixed"]["status"] == "pass"
    and pathfinder_results["pfc_parity_fixed"]["local_germ"]["kind"] == "parity_fixed"
    and pathfinder_results["pfc_corner_wedge"]["corner"]["support_order"] == "2",
)

check(
    "HB7 Pathfinder keeps the c001/DBP channel semantics intact",
    pathfinder_results["dbp_stage_c_channel_predicate"]["status"] == "pass"
    and pathfinder_results["dbp_stage_c_channel_predicate"]["overlay"]["channel_predicate"] == "delta_kappa_c"
    and pathfinder_results["dbp_regular_gi_zero"]["overlay"]["regularity_status"] == "regular"
    and pathfinder_results["dbp_n5_carrier_required"]["overlay"]["shape_resolution"] == "carrier_required",
)

check(
    "HB8 period/residue lane is explicitly reserved as a current limit",
    pathfinder_results["period_residue_lane_reserved"]["status"] == "limit"
    and "period/residue" in pathfinder_results["period_residue_lane_reserved"]["reason"],
)

check(
    "HB9 conventional baseline records are present without being strawmen",
    all("sympy_naive" in case["engines"] for case in report["cases"])
    and all("mpmath_naive" in case["engines"] for case in report["cases"])
    and all("flint_arb" in case["engines"] for case in report["cases"]),
)

arb_results = {
    case["id"]: case["engines"]["flint_arb"]
    for case in report["cases"]
}

check(
    "HB10 Arb baseline evaluates arithmetic cases with interval telemetry",
    arb_results["arith_constant_offset"]["status"] == "pass"
    and arb_results["arith_sqrt_conjugate"]["status"] == "pass"
    and arb_results["arith_unresolved_cos"]["status"] == "pass"
    and arb_results["arith_constant_offset"]["backend"] == "python-flint arb"
    and arb_results["arith_constant_offset"]["sample_eps"] == "1e-12"
    and "radius" in arb_results["arith_constant_offset"]
    and arb_results["arith_unresolved_cos"]["operation"] == "cos_minus_one",
)

hog_results = {
    case["id"]: case["engines"]["cella_pathfinder"]
    for case in report["cases"]
    if case["family"] == "computational_hog"
}

check(
    "HB11 Tier 2 computational hog scripts close through the benchmark runner",
    {"hog_lead7_reflection_coefficients", "hog_lead7_schwarzschild_corner", "hog_pfc_vertex_rule"} <= set(hog_results)
    and hog_results.get("hog_lead7_reflection_coefficients", {}).get("status") == "pass"
    and "LEAD-7 TEST 6 CLEAN" in hog_results.get("hog_lead7_reflection_coefficients", {}).get("verdict", "")
    and hog_results.get("hog_lead7_schwarzschild_corner", {}).get("status") == "pass"
    and "LEAD-7 TEST 9 CLEAN" in hog_results.get("hog_lead7_schwarzschild_corner", {}).get("verdict", "")
    and hog_results.get("hog_pfc_vertex_rule", {}).get("status") == "pass"
    and "PFC-4 vertex rule PROVEN" in hog_results.get("hog_pfc_vertex_rule", {}).get("verdict", "")
    and hog_results.get("hog_lead7_reflection_coefficients", {}).get("script_elapsed_ms", 0) > 1000,
)

print()
if FAILS:
    print(f"GATE PATHFINDER HOSTILE BENCHMARK: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE PATHFINDER HOSTILE BENCHMARK: CLOSED - hostile benchmark MVP runs and records limits.")
sys.exit(0)
