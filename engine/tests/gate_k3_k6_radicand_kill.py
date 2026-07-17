"""Gate the exact k=3/k=6 canonical-radicand kill test."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "research/evidence/arithmetic_horizon_variation/k3_k6_radicand_kill_v1"
VERIFY = PACKAGE / "verify_k3_k6_radicand_kill.py"
CERTIFICATE = PACKAGE / "certificates/k3_k6_radicand_kill.json"
REPORT = PACKAGE / "reports/K3_K6_RADICAND_KILL_TEST_v1.0.md"

missing = [
    str(path.relative_to(ROOT))
    for path in (VERIFY, CERTIFICATE, REPORT)
    if not path.is_file()
]
if missing:
    raise AssertionError(f"k=3/k=6 radicand package is incomplete: {missing}")

result = subprocess.run(
    [sys.executable, str(VERIFY)],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
if result.returncode:
    raise AssertionError(result.stdout + result.stderr)

certificate = json.loads(CERTIFICATE.read_text())
expected = {
    "3": {
        "delta_k": 4,
        "alpha": "e3(w)+u*e1(w)",
        "beta": "e2(w)+u",
        "square_class_rank": 8,
        "normal_closure_group": "C2^2 wr S4",
    },
    "6": {
        "delta_k": 22,
        "alpha": "e6(w)+u*e4(w)+u^2*e2(w)+u^3",
        "beta": "e5(w)+u*e3(w)+u^2*e1(w)",
        "square_class_rank": 44,
        "normal_closure_group": "C2^2 wr S22",
    },
}
for k, wanted in expected.items():
    case = certificate["cases"][k]
    for key, value in wanted.items():
        if case[key] != value:
            raise AssertionError(f"k={k} {key}: expected {value!r}, got {case[key]!r}")
    if case["sheet_level_B"] != [[1, 0], [1, 1]]:
        raise AssertionError(f"k={k} lost the parity-separating contact matrix")

if certificate["verdict"] != "SURVIVES_K3_AND_K6":
    raise AssertionError("the kill-test verdict is not pinned")
if certificate["scope"]["arbitrary_k_theorem_claimed"] is not False:
    raise AssertionError("two probes must not be serialized as an arbitrary-k theorem")

print(result.stdout.strip())
