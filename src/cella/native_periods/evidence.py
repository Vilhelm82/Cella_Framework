"""Repository-local exact theorem and release-evidence adapters.

These adapters do not participate in numerical certification.  They expose the
fixed Landen--trace verifier and the immutable release-report receipt without
changing either the DBP evaluator or its certificates.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


_ROOT = Path(__file__).resolve().parents[3]
_CAMPAIGN = _ROOT / "campaigns" / "DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR"


def verify_landen_trace_theorem() -> dict:
    """Run the fixed exact v1.1 theorem verifier in a clean child process."""
    script = _CAMPAIGN / "verify_dbp_landen_trace_theorem_v1_1.py"
    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(_CAMPAIGN),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    stdout = completed.stdout
    stderr = completed.stderr
    return {
        "theorem": "DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1",
        "verifier": str(script.relative_to(_ROOT)),
        "clean_child_process": True,
        "exit_code": completed.returncode,
        "passed": completed.returncode == 0
        and "All exact gates passed." in stdout
        and "All v1.1 extension gates passed." in stdout,
        "exact_gate_count": sum(
            line.startswith("PASS  ") for line in stdout.splitlines()
        ),
        "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
        "stderr_empty": not stderr,
        "certified_identity": (
            "omega_epsilon + T_epsilon^*omega_epsilon = "
            "phi_epsilon^*(iota_epsilon^(-1)*Theta)"
        ),
        "pushforward_identity": (
            "(phi_epsilon)_*omega_epsilon = iota_epsilon^(-1)*Theta"
        ),
        "theta": "8*(X-3)/(X+7)*dX/Y on E128",
        "scope_boundary": (
            "Does not derive omega_epsilon from the DBP surface curvature two-form."
        ),
    }


def release_report_receipt() -> dict:
    """Return a compact receipt for the stored v1.0 release campaign."""
    path = _CAMPAIGN / "DBP_NATIVE_EVALUATOR_RELEASE_REPORT_v1.0.json"
    raw = path.read_bytes()
    report = json.loads(raw)
    replay = report["certificate_replay"]
    dependency = report["production_dependency_audit"]
    referee = report["arb_referee"]
    return {
        "report": str(path.relative_to(_ROOT)),
        "report_sha256": hashlib.sha256(raw).hexdigest(),
        "schema_id": report["schema_id"],
        "schema_version": report["schema_version"],
        "campaign_date": report["date"],
        "verdict": report["verdict"],
        "stored_receipt_only": True,
        "certificate_replay": {
            "clean_processes": replay["clean_processes"],
            "byte_identical": replay["byte_identical"],
            "canonical_bundle_sha256": replay["canonical_bundle_sha256"],
        },
        "refusal_campaign_passed": report["refusal_campaign"]["passed"],
        "forbidden_dependency_hits": dependency["forbidden_import_or_call_hits"],
        "arb_referee": {
            "certifying_path": referee["certifying_path"],
            "primary_contains_referee": referee["primary"]["native_384_bracket_contains_ball"],
            "dual_cpv_contains_referee": referee["dual_cpv"]["native_384_bracket_contains_ball"],
        },
        "remaining_boundaries": report["remaining_boundaries"],
    }
