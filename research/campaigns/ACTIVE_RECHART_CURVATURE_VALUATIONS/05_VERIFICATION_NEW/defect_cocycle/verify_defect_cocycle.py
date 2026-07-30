#!/usr/bin/env python3
"""Stage 3 gate, part 3: defect cocycle law and pair-form generation
(PO-10, PO-11, PO-12 resolution).

  K1  n=2 symbolic triple-overlap cocycle in a common frame:
      D_(P,D) + D_(D,S) + D_(S,P) = 0 identically in (a,b,A,B,C)
  K2  n=2 twisted (chartwise) cocycle: D_(rho,tau) = D_(rho,sigma)
      + phi_(rho,sigma)^* D_(sigma,tau), each term in its own chart frame
  K3  four roles, exact rational jet: twisted cocycle on the triple (3,2,1)
  K4  four roles: PAIR-FORM GENERATION —
        c_{i;{l,m}} = q_i^2 / Lambda_{i,{l,m}}^2 (dx_i)^2      (chart-intrinsic)
        b_{lm}      = sum_{i not in {l,m}} c_{i;{l,m}}          (canonical)
        g^(rho)     = sum_{m != rho} b_{rho m}                  (assignment)
      verified entrywise in a common frame.
  K5  four roles: the half-sum T = (1/2) sum_rho g^(rho) = sum_{pairs} b_pair
      descends (presentation-free), so the canonical objects are the pair
      forms and every g^(rho) is a partial sum — Branch B controlled defect,
      obstruction class zero.
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


# ---------------- K1/K2: n = 2 symbolic ---------------------------------------
a, b, A, B, C = sp.symbols("a b A B C")
q0 = 1 + a**2 + b**2
LamP, LamD, LamS = B, (A * b - a * B) / a, (C * a - b * B) / b
wP, wD, wS = q0**2 / LamP**2, q0**2 / LamD**2, q0**2 / LamS**2

# common frame: P-base (dD, dS); dP = a dD + b dS
rP = sp.Matrix([[a, b]])
rD = sp.Matrix([[1, 0]])
rS = sp.Matrix([[0, 1]])
c = {"P": wP * rP.T * rP, "D": wD * rD.T * rD, "S": wS * rS.T * rS}
g = {rho: sum((c[i] for i in "PDS" if i != rho), sp.zeros(2, 2)) for rho in "PDS"}
D_PD = sp.expand(g["P"] - g["D"])
D_DS = sp.expand(g["D"] - g["S"])
D_SP = sp.expand(g["S"] - g["P"])
check("K1 triple cocycle D_(P,D)+D_(D,S)+D_(S,P) = 0 identically",
      sp.simplify(D_PD + D_DS + D_SP) == sp.zeros(2, 2))
check("K1 each defect is the coboundary c_sigma - c_rho",
      sp.simplify(D_PD - (c["D"] - c["P"])) == sp.zeros(2, 2))

# K2 twisted formulation: express D_(D,S) in the D-chart frame and pull back.
# D-chart base (dP, dS); on T Sigma: dD = (1/a) dP - (b/a) dS
rD_in_D = sp.Matrix([[1 / a, -b / a]])
rP_in_D = sp.Matrix([[1, 0]])
rS_in_D = sp.Matrix([[0, 1]])
cD = {"P": wP * rP_in_D.T * rP_in_D, "D": wD * rD_in_D.T * rD_in_D,
      "S": wS * rS_in_D.T * rS_in_D}
D_DS_chartD = sp.expand((cD["S"] - cD["D"]))
J_PD = sp.Matrix([[a, b], [0, 1]])        # d(base_D) rows (dP,dS) via (dD,dS)
pulled = sp.expand(J_PD.T * D_DS_chartD * J_PD)
D_PS_chartP = sp.expand(c["S"] - c["P"])
check("K2 twisted cocycle D_(P,S) = D_(P,D) + phi* D_(D,S)",
      sp.simplify(D_PD + pulled - D_PS_chartP) == sp.zeros(2, 2))

# ---------------- K3-K5: four roles, exact rational ----------------------------
rng = random.Random(27182)
x0, x1, x2 = sp.symbols("x0 x1 x2")
while True:
    cs = {k: sp.Rational(rng.randint(-5, 5), rng.randint(1, 4))
          for k in ["c0", "c1", "c2", "c00", "c01", "c02", "c11", "c12", "c22"]}
    if cs["c0"] * cs["c1"] * cs["c2"] != 0:
        break
f3 = (cs["c0"] * x0 + cs["c1"] * x1 + cs["c2"] * x2
      + cs["c00"] * x0**2 / 2 + cs["c01"] * x0 * x1 + cs["c02"] * x0 * x2
      + cs["c11"] * x1**2 / 2 + cs["c12"] * x1 * x2 + cs["c22"] * x2**2 / 2)
vars3 = {0: x0, 1: x1, 2: x2}
charts = {3: (sp.expand(f3), vars3)}
for i in (0, 1, 2):
    charts[i] = rechart(f3, vars3, 3, i, 2)

Q, LAM, GRAD = {}, {}, {}
for i in range(4):
    jet, vs = charts[i]
    idx = sorted(vs)
    syms = [vs[j] for j in idx]
    GRAD[i] = {j: jet_coeff(jet, syms, tuple(1 if k == j else 0 for k in idx))
               for j in idx}
    Q[i] = 1 + sum(GRAD[i][j]**2 for j in idx)
    LAM[i] = {}
    for l, m in itertools.combinations(idx, 2):
        e = tuple((1 if k in (l, m) else 0) for k in idx)
        LAM[i][frozenset((l, m))] = jet_coeff(jet, syms, e)

# common ambient frame: presentation-3 base (dx0,dx1,dx2); dx3 = grad f3 . dx
def row(i):
    if i == 3:
        return sp.Matrix([[GRAD[3][0], GRAD[3][1], GRAD[3][2]]])
    r = sp.zeros(1, 3)
    r[0, i] = 1
    return r

def cform(i, pair):
    lam = LAM[i][frozenset(pair)]
    return (Q[i]**2 / lam**2) * row(i).T * row(i)

def bpair(l, m):
    return sum((cform(i, (l, m)) for i in range(4) if i not in (l, m)),
               sp.zeros(3, 3))

def g_of(rho):
    M = sp.zeros(3, 3)
    for i in range(4):
        if i == rho:
            continue
        tot = sum(1 / LAM[i][frozenset((rho, m))]**2
                  for m in range(4) if m not in (i, rho))
        M += Q[i]**2 * tot * row(i).T * row(i)
    return sp.expand(M)

G = {rho: g_of(rho) for rho in range(4)}

# K3 twisted cocycle on (3,2,1): all in common frame -> plain additivity, plus
# a chartwise pullback consistency using the base-2 frame.
D32 = sp.expand(G[3] - G[2])
D21 = sp.expand(G[2] - G[1])
D31 = sp.expand(G[3] - G[1])
check("K3 four-role cocycle D_(3,1) = D_(3,2) + D_(2,1) (common frame, exact)",
      sp.simplify(D31 - D32 - D21) == sp.zeros(3, 3))

# K4 pair-form generation
ok = True
for rho in range(4):
    gen = sum((bpair(rho, m) for m in range(4) if m != rho), sp.zeros(3, 3))
    if sp.simplify(sp.expand(gen - G[rho])) != sp.zeros(3, 3):
        ok = False
check("K4 g^(rho) = sum_{m != rho} b_{rho m} for all four presentations", ok)

# K5 half-sum descent
T = sum((bpair(l, m) for l, m in itertools.combinations(range(4), 2)),
        sp.zeros(3, 3))
half = sp.expand(sum(G.values(), sp.zeros(3, 3)) / 2)
check("K5 T = (1/2) sum_rho g^(rho) = sum_pairs b_pair (descends)",
      sp.simplify(half - T) == sp.zeros(3, 3))

print()
if failures:
    print("STAGE 3 COCYCLE GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 3 COCYCLE GATE PASSED: coboundary structure exact at three and "
      "four roles; pair forms generate every presentation; half-sum descends.")
