"""Gate the engine-neutral benchmark sweep.

Run:  PYTHONPATH=src python tests/gate_neutral_sweep.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FAILS: list[str] = []


def check(name: str, ok: bool) -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


try:
    from cella.neutral_sweep import DEFAULT_MANIFEST, load_manifest, run_sweep
except Exception as exc:
    print(f"GATE NEUTRAL SWEEP: OPEN - import failed: {exc}")
    sys.exit(1)


manifest = load_manifest(DEFAULT_MANIFEST)
case_ids = {case["id"] for case in manifest["cases"]}
families = {case["family"] for case in manifest["cases"]}

check(
    "NS1 default corpus contains broad engine-neutral families",
    {
        "arithmetic_cancellation",
        "symbolic_rational",
        "polynomial_identity",
        "local_geometry",
        "linear_algebra",
        "complex_branch",
    }
    <= families
    and len(case_ids) >= 8,
)

check(
    "NS2 corpus is declarative rather than a legacy script launcher",
    all(case["kind"] != "verification_script" for case in manifest["cases"])
    and all("script" not in case.get("input", {}) for case in manifest["cases"]),
)

with tempfile.TemporaryDirectory() as tmp:
    report_path = Path(tmp) / "neutral-report.json"
    report = run_sweep(
        DEFAULT_MANIFEST,
        output_path=report_path,
        engines=["cella", "sympy", "mpmath", "flint_arb"],
        per_case_timeout_s=3.0,
    )
    persisted = json.loads(report_path.read_text(encoding="utf-8"))

check(
    "NS3 sweep writes one result bundle per neutral case",
    persisted["summary"]["case_count"] == len(manifest["cases"])
    and len(persisted["cases"]) == len(manifest["cases"])
    and persisted["summary"] == report["summary"],
)

check(
    "NS4 every engine result records bounded runtime telemetry",
    all(
        "elapsed_ms" in result
        and "status" in result
        and result.get("timeout_s") == 3.0
        for case in report["cases"]
        for result in case["engines"].values()
    ),
)

cancellation = next(case for case in report["cases"] if case["id"] == "cancel_sqrt_conjugate")
check(
    "NS5 cancellation case is solved by at least two native engines",
    sum(1 for result in cancellation["engines"].values() if result["status"] == "pass") >= 2,
)

poly = next(case for case in report["cases"] if case["id"] == "poly_sophie_germain")
check(
    "NS6 polynomial identity case exposes exact proof records",
    poly["engines"]["cella"]["status"] == "pass"
    and poly["engines"]["sympy"]["status"] == "pass"
    and poly["engines"]["cella"].get("proof") == "zero_normal_form",
)

timeout_case = next(case for case in report["cases"] if case["id"] == "timeout_progress_probe")
check(
    "NS7 per-engine timeout dumps partial progress and moves on",
    timeout_case["engines"]["sympy"]["status"] == "timeout"
    and timeout_case["engines"]["sympy"]["partial"].get("phase") == "intentional_delay"
    and timeout_case["engines"]["sympy"]["partial"].get("case_id") == "timeout_progress_probe"
    and timeout_case["engines"]["cella"]["status"] == "pass",
)

check(
    "NS8 report classifies pass/fail/limit/timeout counts by engine",
    report["summary"]["engines"]["cella"]["pass"] >= 6
    and report["summary"]["engines"]["sympy"]["timeout"] >= 1
    and "flint_arb" in report["summary"]["engines"],
)

print()
if FAILS:
    print(f"GATE NEUTRAL SWEEP: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE NEUTRAL SWEEP: CLOSED - engine-neutral benchmark sweep is bounded and reportable.")
sys.exit(0)
