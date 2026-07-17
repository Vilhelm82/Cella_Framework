"""Gate for the independently reconstructed AHV-1 k=4 evidence package."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "research/evidence/arithmetic_horizon_variation/ahv1_k4_clean_v1"
VERIFY = PACKAGE / "verify_ahv1_k4_clean.py"


required = (
    PACKAGE / "certificates/topological_control.json",
    PACKAGE / "certificates/decoration_live.json",
    PACKAGE / "matrices/control_chain_matrices.json",
    PACKAGE / "matrices/control_thimbles.json",
    PACKAGE / "matrices/decoration_chain_matrices.json",
    PACKAGE / "matrices/decoration_thimbles.json",
    PACKAGE / "matrices/decoration_kummer_parity.json",
    PACKAGE / "reports/AHV1_K4_CLEAN_EXECUTION_v1.0.md",
)

missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
if missing:
    raise AssertionError(f"clean AHV-1 package is incomplete: {missing}")

result = subprocess.run(
    [sys.executable, str(VERIFY)],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
if result.returncode:
    raise AssertionError(result.stdout + result.stderr)

summary = json.loads((PACKAGE / "certificates/decoration_live.json").read_text())
if summary["kummer"]["normalization"] != "gamma_R9=2*(e4(w)+u*e2(w)+u^2+P)":
    raise AssertionError("noncanonical gamma normalization entered the clean certificate")
if summary["kummer"].get("alpha") != "e4(w)+u*e2(w)+u^2":
    raise AssertionError("the global alpha identity is missing from the clean certificate")
if summary["kummer"].get("beta") != "e3(w)+u*e1(w)":
    raise AssertionError("the global beta identity is missing from the clean certificate")
if summary["scope"]["closes_all_k_IV3"] is not False:
    raise AssertionError("instance evidence must not close the all-k IV3 gap")

print(result.stdout.strip())
