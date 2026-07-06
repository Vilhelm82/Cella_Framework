"""Gate G0.3 — the exact number tower rung Q(sqrt(r)).

Certifies src/cella/qsqrt.py: exact field arithmetic at fixed radicand,
non-square/positivity guards, float exclusion from verdict paths, and the
parity-law retrodiction (sigma_1^2 rational at the keystone context q=14 —
a pinned prior claim tested fresh through this implementation).

Run:  python tests/gate_03.py   (exit 0 iff the gate is closed)
"""

import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.qsqrt import QSqrt  # noqa: E402

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


# 1 — construction guards
guards = []
for bad_r in (4, Q(9, 4), -2, 0, Q(16, 25)):
    try:
        QSqrt(1, 1, bad_r)
        guards.append(False)
    except ValueError:
        guards.append(True)
check("G0.3 square/nonpositive radicands rejected (5 cases)", all(guards))
floats_rejected = []
for args in ((0.5, 1, 14), (1, 0.5, 14), (1, 1, 14.0)):
    try:
        QSqrt(*args)
        floats_rejected.append(False)
    except TypeError:
        floats_rejected.append(True)
check("G0.3 float components rejected with TypeError", all(floats_rejected))

# 2 — exact field arithmetic at r = 14
x = QSqrt(Q(3, 7), Q(2, 5), 14)
y = QSqrt(Q(-1, 3), Q(1, 2), 14)
check("G0.3 multiplication exact (hand-computed pin, corrected in ink: "
      "a = -1/7 + 14/5 = 93/35)",
      x * y == QSqrt(Q(93, 35), Q(17, 210), 14))
check("G0.3 division inverts multiplication exactly", (x / y) * y == x)
check("G0.3 additive inverse collapses to rational zero", x + (-x) == Q(0))
check("G0.3 norm is multiplicative: N(xy) == N(x)N(y)",
      (x * y).norm() == x.norm() * y.norm())
check("G0.3 scalar coercion: (1/2) * x + x * (3/2) == 2x",
      Q(1, 2) * x + x * Q(3, 2) == x + x)

# 3 — parity-law retrodiction at the keystone context (q = 14):
#     sigma_1 = (6/49)*sqrt(14)  ==>  sigma_1^2 == 72/343, exactly rational
sigma1 = QSqrt(0, Q(6, 49), 14)
sq = sigma1 * sigma1
check("G0.3 parity retrodiction: sigma_1^2 == 72/343 (rational, exact)",
      sq.is_rational() and sq == Q(72, 343))
check("G0.3 to_fraction on the rational collapse", sq.to_fraction() == Q(72, 343))

# 4 — one sqrt per context: mixed radicands refused
try:
    _ = x + QSqrt(1, 1, 2)
    mixed = False
except TypeError:
    mixed = True
check("G0.3 mixed radicands refused (TypeError)", mixed)

# 5 — float exclusion from verdict paths
try:
    float(x)
    fl = False
except TypeError:
    fl = True
check("G0.3 __float__ raises; display path is explicit", fl
      and isinstance(x.to_float_display(), float))

# 6 — division by zero element
try:
    _ = x / QSqrt(0, 0, 14)
    dz = False
except ZeroDivisionError:
    dz = True
check("G0.3 division by zero QSqrt raises ZeroDivisionError", dz)

# 7 — honest rational collapse: equality and hash agree with Fraction
z = QSqrt(Q(5, 3), 0, 14)
check("G0.3 b == 0 equals and hashes as its Fraction",
      z == Q(5, 3) and hash(z) == hash(Q(5, 3))
      and QSqrt(Q(5, 3), 0, 14) == QSqrt(Q(5, 3), 0, 2))
try:
    x.to_fraction()
    tf = False
except ValueError:
    tf = True
check("G0.3 to_fraction refuses when irrational part nonzero", tf)

print()
if FAILS:
    print(f"GATE G0.3: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE G0.3: CLOSED — Q(sqrt(r)) exact, guarded, float-free on verdict paths.")
sys.exit(0)
