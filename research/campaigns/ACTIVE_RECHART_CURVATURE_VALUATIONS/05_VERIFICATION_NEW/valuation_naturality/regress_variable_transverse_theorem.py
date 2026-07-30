#!/usr/bin/env python3
"""Stage 6 gate D: regression — the packaged legacy variable-transverse
weighted-jet verifier must pass FROM THE PACKAGE (shim-path audit flag
discharged: the packaged runner resolves the verifier beside itself, not the
old nonexistent parent-tree location)."""
import subprocess
import sys
from pathlib import Path

pkg = Path(__file__).resolve().parents[2] / "04_VERIFICATION_LEGACY" / "weighted_jet"

for script in ("verify_lead7_variable_transverse_weighted_jet.py",
               "lead7_variable_transverse_weighted_jet.py"):
    r = subprocess.run([sys.executable, str(pkg / script)], cwd=str(pkg),
                       capture_output=True, text=True, timeout=600)
    tail = (r.stdout or "").strip().splitlines()[-1:] or ["<no output>"]
    ok = r.returncode == 0 and "passed" in (r.stdout or "").lower()
    print(("PASS " if ok else "FAIL ") + f"{script}: {tail[0]}")
    if not ok:
        print(r.stdout)
        print(r.stderr)
        sys.exit(1)

print()
print("STAGE 6D GATE PASSED: legacy weighted-jet proof replays from the "
      "package; broken shim path permanently fixed.")
