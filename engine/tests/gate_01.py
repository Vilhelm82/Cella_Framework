"""Gate G0.1 — M-species composition on the rational-op class.

Certifies the implementation (src/cella/residue.py) against the facts the
campaign proved: composed M-residues reconstruct exactly on scalar and
matrix carriers, including multiplicative-defect chains (TC-P3a: additive
ledger, current-input residues), and floats are rejected at type level.

Run:  python tests/gate_01.py   (exit 0 iff the gate is closed)
"""

import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.residue import Account, Residue, madd, is_zero  # noqa: E402

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


# 1 — scalar chain: two lossy maps, composed account reconstructs
T = Q(1, 3)
v1 = Q(3333, 10000)                     # first lossy representation
r1 = Residue("M", T - v1)
v2 = Q(33, 100)                         # second map re-coarsens the CURRENT value
r2 = Residue("M", v1 - v2)
acc = Account().absorb(r1).absorb(r2)
check("G0.1 scalar chain reconstructs: v2 + m_total == T",
      v2 + acc.m_total == T)

# 2 — multiplicative-defect chain (TC-P3a as implementation behaviour)
T2, d1, d2 = Q(7, 3), Q(1, 100), Q(-1, 50)
w1 = T2 * (1 + d1)
w2 = w1 * (1 + d2)
acc2 = Account().absorb(Residue("M", T2 - w1)).absorb(Residue("M", w1 - w2))
check("G0.1 multiplicative chain: additive ledger exact (cross-term captured)",
      w2 + acc2.m_total == T2)
mut = (T2 - w1) + (-T2 * d2)            # original-truth mutant ledger
check("G0.1 original-truth mutant FAILS (misses T*d1*d2)",
      w2 + mut != T2 and (w2 + mut) - T2 == T2 * d1 * d2)

# 3 — matrix carrier: entrywise defects compose and reconstruct
M_true = ((Q(1, 3), Q(2, 7)), (Q(2, 7), Q(5, 11)))
M_obs = ((Q(3, 10), Q(2, 7)), (Q(2, 7), Q(9, 20)))
E1 = tuple(tuple(a - b for a, b in zip(ra, rb)) for ra, rb in zip(M_true, M_obs))
M_obs2 = ((Q(3, 10), Q(1, 4)), (Q(1, 4), Q(9, 20)))
E2 = tuple(tuple(a - b for a, b in zip(ra, rb)) for ra, rb in zip(M_obs, M_obs2))
accM = Account().absorb(Residue("M", E1)).absorb(Residue("M", E2))
check("G0.1 matrix carrier reconstructs entrywise",
      madd(M_obs2, accM.m_total) == M_true)

# 4 — Residue.compose agrees with Account composition
r12 = Residue("M", E1).compose(Residue("M", E2))
check("G0.1 Residue.compose == Account absorption (M)",
      r12.payload == accM.m_total)

# 5 — float rejection at every entry point
ok = True
for bad in (0.1, ((Q(1), 0.5),), (Q(1), float("nan"))):
    try:
        Residue("M", bad)
        ok = False
    except TypeError:
        pass
check("G0.1 float payloads rejected with TypeError (all shapes)", ok)

# 6 — zero detection on the module
check("G0.1 is_zero on nested carriers",
      is_zero(((Q(0), Q(0)), (Q(0), Q(0)))) and not is_zero(((Q(0), Q(1, 7)),)))

print()
if FAILS:
    print(f"GATE G0.1: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE G0.1: CLOSED — M-composition certified on scalar and matrix carriers.")
sys.exit(0)
