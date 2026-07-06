"""Gate G0.2 — the two-species single account, as implemented.

Certifies src/cella/residue.py against the campaign's theorems by rebuilding
the certified facts THROUGH THE API: order-independence (Stage A), the
attribution fold and two-epoch law (Stage B / TC-P2), the asymmetry law and
the false-alarm/miss pair (TC-P1/P6), and owned holonomy (TC-P5). Geometry
helpers below are fresh code from the certified closed forms — Layer 1 does
not exist yet, so the test carries its own O and G.

Run:  python tests/gate_02.py   (exit 0 iff the gate is closed)
"""

import sys
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.residue import Account, Residue, is_zero, madd, msub  # noqa: E402

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


# --- fresh geometry helpers (certified closed forms; n = 3) ---
N = 3
g = (Q(3), Q(1), Q(2))


def Gm(base, a):
    return tuple(tuple(base[i] * a[j] + a[i] * base[j] for j in range(N))
                 for i in range(N))


def O(M, base=g):
    return tuple(M[i][j] - base[i] * M[j][j] / (2 * base[j])
                 - base[j] * M[i][i] / (2 * base[i])
                 for i in range(N) for j in range(i + 1, N))


H0 = ((Q(1), Q(2), Q(-1)), (Q(2), Q(3), Q(4)), (Q(-1), Q(4), Q(2)))
Es = [((Q(1), Q(0), Q(2)), (Q(0), Q(-1), Q(1)), (Q(2), Q(1), Q(3))),
      ((Q(0), Q(1, 2), Q(0)), (Q(1, 2), Q(2), Q(-1)), (Q(0), Q(-1), Q(0))),
      ((Q(-2), Q(1), Q(1)), (Q(1), Q(0), Q(0)), (Q(1), Q(0), Q(1)))]
As = [(Q(1), Q(0), Q(-1)), (Q(0), Q(2), Q(1)), (Q(-1, 2), Q(1), Q(0))]

# 1 — Stage A through the API: all 720 orderings, one account
ops = [Residue("M", E) for E in Es] + [Residue("R", a, base=g) for a in As]
accounts, finals = set(), set()
for perm in permutations(range(6)):
    H = H0
    acc = Account()
    for k in perm:
        r = ops[k]
        acc = acc.absorb(r)
        H = madd(H, r.payload if r.species == "M" else Gm(g, r.payload))
    accounts.add((acc.m_total, acc.r_epochs))
    finals.add(H)
check("G0.2 Stage-A via API: 720 orderings -> ONE account and ONE final",
      len(accounts) == 1 and len(finals) == 1)
acc = Account()
for r in ops:
    acc = acc.absorb(r)
Hf = next(iter(finals))
check("G0.2 reconstruction: O(H_final - m_total) == O(H0)",
      O(msub(Hf, acc.m_total)) == O(H0))
check("G0.2 R-ledger merged to a single epoch at fixed base",
      len(acc.r_epochs) == 1 and acc.r_epochs[0][0] == g
      and acc.r_epochs[0][1] == tuple(sum(a[i] for a in As) for i in range(N)))

# 2 — asymmetry law via API: d stays R (no damage reported)
d = (Q(1, 3), Q(-1, 2), Q(1))
a_exec = tuple(x + y for x, y in zip(As[0], d))
acc_d = Account().absorb(Residue("R", a_exec, base=g))
H_d = madd(H0, Gm(g, a_exec))
check("G0.2 asymmetry: defective direction -> M-ledger EMPTY, state intact",
      acc_d.m_total is None and O(H_d) == O(H0))

# 3 — Stage B via API: defective base, cross-term folded by criterion
e = (Q(1, 2), Q(1, 4), Q(-1, 3))
gp = tuple(g[i] + e[i] for i in range(N))
acc_b = Account().absorb(Residue("M", Es[0])) \
                 .absorb(Residue("R", As[0], base=gp))
H_b = madd(madd(H0, Es[0]), Gm(gp, As[0]))
acc_b = acc_b.fold_into_m(Gm(e, As[0]))          # the attribution move (F2/F3)
check("G0.2 Stage-B via API: fold(G_e(a)) -> exact state reconstruction",
      O(msub(H_b, acc_b.m_total)) == O(H0))
check("G0.2 Stage-B: R-ledger records intended parameters at the executed base",
      acc_b.r_epochs == ((gp, As[0]),))

# 4 — miss mutant via API: refusing the fold leaves real damage unclaimed
acc_miss = Account().absorb(Residue("M", Es[0])) \
                    .absorb(Residue("R", As[0], base=gp))
check("G0.2 miss mutant CAUGHT: without the fold, reconstruction fails",
      O(msub(H_b, acc_miss.m_total)) != O(H0))

# 5 — two-epoch law via API: distinct bases never merge
e2 = (Q(-1, 5), Q(1, 3), Q(1, 2))
gp2 = tuple(g[i] + e2[i] for i in range(N))
acc_2ep = Account().absorb(Residue("R", As[0], base=gp)) \
                   .absorb(Residue("R", As[1], base=gp2)) \
                   .absorb(Residue("R", As[2], base=gp2))
check("G0.2 two-epoch law: bases kept as ordered epochs, same-base merged",
      acc_2ep.r_epochs == ((gp, As[0]),
                           (gp2, tuple(x + y for x, y in zip(As[1], As[2])))))
try:
    Residue("R", As[0], base=gp).compose(Residue("R", As[1], base=gp2))
    boundary_guard = False
except ValueError:
    boundary_guard = True
check("G0.2 epoch boundary guard: cross-base R-composition refused", boundary_guard)

# 6 — owned holonomy via API (TC-P5 single slot; 1/10 + 2/10 forces the
# routes to disagree: fl(0.1)+fl(0.2) != fl(0.3))
t = Q(1, 10) + Q(2, 10)                           # a truth off the float lattice
va = float(Q(1, 10)) + float(Q(2, 10))            # route a: round parts, then add
ra = (Q(1, 10) - Q(float(Q(1, 10)))) + (Q(2, 10) - Q(float(Q(2, 10)))) \
     + (Q(float(Q(1, 10))) + Q(float(Q(2, 10))) - Q(va))
vb = float(t)                                     # route b: exact add, then round
rb = t - Q(vb)
A_a = Account().absorb(Residue("M", ra))
A_b = Account().absorb(Residue("M", rb))
check("G0.2 both routes reconstruct through the API",
      Q(va) + A_a.m_total == t and Q(vb) + A_b.m_total == t)
check("G0.2 owned holonomy: v_a - v_b == gap(A_a -> A_b) exactly",
      Q(va) - Q(vb) == A_a.holonomy_gap(A_b))
check("G0.2 holonomy witness nonzero (content, not vacuity)",
      Q(va) != Q(vb))

# 7 — ledger separation is structural
check("G0.2 no path mixes ledgers: M empty iff no M absorbed and no fold",
      Account().absorb(Residue("R", As[0], base=g)).m_total is None)

print()
if FAILS:
    print(f"GATE G0.2: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE G0.2: CLOSED — the two-species single account is implemented as "
      "certified: order-safe, attribution by criterion, epochs honest, "
      "holonomy owned.")
sys.exit(0)
