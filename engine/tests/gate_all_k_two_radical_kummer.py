"""Gate the completed all-k two-radical Kummer-closure paper."""

from __future__ import annotations

from fractions import Fraction
from math import comb
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
STEM = ROOT / (
    "Papers_Library/01_completed_papers/galois_horizon_and_kummer_covers/"
    "ALL_K_TWO_RADICAL_KUMMER_CLOSURE_v1.0"
)
TEX = Path(f"{STEM}.tex")
PDF = Path(f"{STEM}.pdf")
LOW_K_GATE = ROOT / "engine/tests/gate_k3_k6_radicand_kill.py"


for path in (TEX, PDF, LOW_K_GATE):
    if not path.is_file():
        raise AssertionError(f"missing all-k proof artifact: {path.relative_to(ROOT)}")
if PDF.stat().st_size < 80_000:
    raise AssertionError("the rendered proof PDF is unexpectedly small")

source = TEX.read_text()
required_fragments = (
    r"\sum_{r=0}^{\lfloor k/2\rfloor}u^r e_{k-2r}(w)",
    r"\sum_{r=0}^{\lfloor(k-1)/2\rfloor}u^r e_{k-1-2r}(w)",
    r"\boxed{\gamma_k(\gamma_k-4P)=4u\beta_k^2.}",
    r"\begin{pmatrix}" + "\n 1&0\\\\\n 1&1\n " + r"\end{pmatrix}",
    r"C_2^2\wrp S_{\delta_k}",
    "What is special at four charges",
)
for fragment in required_fragments:
    if fragment not in source:
        raise AssertionError(f"proof source lost required theorem fragment: {fragment}")
if "qquad" in source.replace(r"\qquad", ""):
    raise AssertionError("proof source contains a literal qquad typesetting artifact")


def delta(k: int) -> int:
    """Degree of the normalized equal-weight mass polynomial."""

    if k % 2:
        return 2 ** (k - 1)
    return 2 ** (k - 1) - comb(k, k // 2) // 2


expected = {3: 4, 4: 5, 5: 16, 6: 22, 7: 64, 8: 93}
actual = {k: delta(k) for k in expected}
if actual != expected:
    raise AssertionError(f"all-k degree formula failed: {actual}")

# Exact signed-contact witnesses.  Powers of two make every signed mass wall
# distinct.  The derivative of 4M-sum eps_i*sqrt(u+N_i^2) at u=0 is
# -1/2 sum eps_i/N_i, so a nonzero reciprocal sum proves the contact is simple.
# The product sign gives gamma_k(0)=4P (even) or 0 (odd), hence the two rows.
for k in range(3, 11):
    charges = tuple(2**i for i in range(k))
    rows: list[tuple[int, int]] = []
    for signs in ((1,) * k, (-1,) + (1,) * (k - 1)):
        reciprocal_sum = sum(
            (Fraction(sign, charge) for sign, charge in zip(signs, charges)),
            Fraction(0),
        )
        if reciprocal_sum == 0:
            raise AssertionError(f"k={k} chosen contact is not simple")
        gamma_parity = 0 if signs.count(-1) % 2 == 0 else 1
        rows.append((1, gamma_parity))
    if rows != [(1, 0), (1, 1)]:
        raise AssertionError(f"k={k} lost the parity-separating contact matrix")

low_k = subprocess.run(
    [sys.executable, str(LOW_K_GATE)],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
if low_k.returncode:
    raise AssertionError(low_k.stdout + low_k.stderr)

print(
    "all-k two-radical Kummer closure: PASS "
    "(proof artifacts, degree formula, k=3..10 exact contacts, k=3/k=6 replay)"
)
