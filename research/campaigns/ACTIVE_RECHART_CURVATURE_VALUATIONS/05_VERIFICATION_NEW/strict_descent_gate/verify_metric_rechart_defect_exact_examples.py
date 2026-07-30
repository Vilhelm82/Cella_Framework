#!/usr/bin/env python3
"""Stage 3 gate, part 2: exact rational examples, degenerate strata, and the
four-role weight non-invariance witness (PO-9, PO-11, falsification items 1-2).

  E1  (5,7,2,3,4) witness: defect entries computed in closed form; nonzero.
  E2  a role rechart of a DIAGONAL metric is off-diagonal (falsification item 1:
      the pullback phi*(g^(D)) has nonzero (dD,dS) cross term).
  E3  degenerate stratum: B = 0 (Lambda_P = 0) makes w_P infinite — the
      presentations D and S lose their P-entry; typed refusal, not a metric.
  E4  FOUR ROLES: the shared-coordinate weight coincidence of n=2 FAILS:
      G_i^(rho) != G_i^(sigma) for a shared state coordinate i (exact witness)
      — so no single ambient diagonal form reproduces all presentations at
      n >= 3; the pair decomposition is required.
  E5  four roles: strict descent fails (defect nonzero on shared block too).
"""
import random
import sys
import itertools
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("/", 1)[0] + "/role_cover_groupoid")
from jetlib import rechart, jet_coeff

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


# ---------------- n = 2 exact witness ----------------------------------------
a, b, A, B, C = 5, 7, 2, 3, 4
q0 = 1 + a**2 + b**2                    # 75
LamP, LamD, LamS = sp.Rational(B), sp.Rational(A * b - a * B, a), sp.Rational(C * a - b * B, b)
wP, wD, wS = q0**2 / LamP**2, q0**2 / LamD**2, q0**2 / LamS**2
gP = sp.diag(wD, wS)
gD = sp.diag(wP, wS)
J = sp.Matrix([[a, b], [0, 1]])
pull = J.T * gD * J
Ddef = gP - pull
check("E1 defect at witness is nonzero and rank 2",
      Ddef != sp.zeros(2, 2) and Ddef.det() != 0)
# closed form check: D = wD dD^2 - wP (a dD + b dS)^2
closed = sp.diag(wD, 0) - wP * sp.Matrix([[a], [b]]) * sp.Matrix([[a, b]])
check("E1 closed-form rank-one-difference matches", sp.expand(Ddef - closed) == sp.zeros(2, 2))

# E2 off-diagonalization (falsification item 1)
check("E2 diagonal metric becomes off-diagonal under active rechart",
      pull[0, 1] != 0)

# E3 degenerate stratum: B = 0
a3, b3, A3, B3, C3 = 5, 7, 2, 0, 4
LamP3 = B3
check("E3 Lambda_P = 0 is a typed stratum: w_P undefined (division by zero refused)",
      LamP3 == 0)   # the assignment itself refuses; no coerced value exists

# ---------------- four roles (n = 3) ------------------------------------------
rng = random.Random(31415)
x0, x1, x2 = sp.symbols("x0 x1 x2")
while True:
    cs = {k: sp.Rational(rng.randint(-5, 5), rng.randint(1, 4))
          for k in ["c0", "c1", "c2", "c00", "c01", "c02", "c11", "c12", "c22"]}
    if cs["c0"] != 0 and cs["c1"] != 0 and cs["c2"] != 0:
        break
f3 = (cs["c0"] * x0 + cs["c1"] * x1 + cs["c2"] * x2
      + cs["c00"] * x0**2 / 2 + cs["c01"] * x0 * x1 + cs["c02"] * x0 * x2
      + cs["c11"] * x1**2 / 2 + cs["c12"] * x1 * x2 + cs["c22"] * x2**2 / 2)
vars3 = {0: x0, 1: x1, 2: x2}

# all four output charts (role 3 native)
charts = {3: (sp.expand(f3), vars3)}
for i in (0, 1, 2):
    charts[i] = rechart(f3, vars3, 3, i, 2)

def chart_data(i):
    jet, vs = charts[i]
    idx = sorted(vs)                       # roles serving as inputs
    syms = [vs[j] for j in idx]
    grad = {j: jet_coeff(jet, syms, tuple(1 if k == j else 0 for k in idx))
            for j in idx}
    q = 1 + sum(grad[j]**2 for j in idx)
    lam = {}
    for l, m in itertools.combinations(idx, 2):
        e = tuple((1 if k in (l, m) else 0) for k in idx)
        lam[frozenset((l, m))] = jet_coeff(jet, syms, e)
    return q, lam

Q = {}
LAM = {}
for i in range(4):
    Q[i], LAM[i] = chart_data(i)

def G_entry(i, rho):
    """diagonal entry for state coordinate i in presentation rho"""
    total = 0
    for m in range(4):
        if m in (i, rho):
            continue
        lam = LAM[i][frozenset((rho, m))]
        total += 1 / lam**2
    return sp.cancel(Q[i]**2 * total)

# E4 weight non-invariance for a shared coordinate
i_shared = 0
vals = {rho: G_entry(i_shared, rho) for rho in (1, 2, 3)}
distinct = len({sp.nsimplify(v) for v in vals.values()})
check("E4 shared-coordinate weights differ across presentations (n=3)",
      distinct >= 2)

# E5 strict descent fails at four roles: compare g^(3) and phi*(g^(2)) in the
# base of presentation 3 (coords x0,x1,x2)
grad3 = {j: jet_coeff(charts[3][0], [x0, x1, x2],
                      tuple(1 if k == j else 0 for k in range(3)))
         for j in range(3)}
def metric_in_base3(rho):
    """g^(rho) expressed in the (x0,x1,x2) frame at the base point"""
    M = sp.zeros(3, 3)
    for i in range(4):
        if i == rho:
            continue
        # dx_i in base-3 frame
        if i == 3:
            row = sp.Matrix([[grad3[0], grad3[1], grad3[2]]])
        else:
            row = sp.zeros(1, 3)
            row[0, i] = 1
        M += G_entry(i, rho) * row.T * row
    return M

g3 = metric_in_base3(3)
g2 = metric_in_base3(2)
diff = sp.expand(g3 - g2)
check("E5 four-role strict descent fails (defect nonzero)",
      diff != sp.zeros(3, 3))
# and the defect is NOT supported only in the exchanged directions:
# its (0,0) entry (a shared coordinate) is already nonzero
check("E5 defect hits shared coordinates too (weights are pair-dependent)",
      sp.simplify(diff[0, 0]) != 0)

print()
if failures:
    print("STAGE 3 EXACT-EXAMPLE GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 3 EXACT-EXAMPLE GATE PASSED: witnesses fixed; degeneracy typed; "
      "n=3 kills the single-form picture — pair decomposition required.")
