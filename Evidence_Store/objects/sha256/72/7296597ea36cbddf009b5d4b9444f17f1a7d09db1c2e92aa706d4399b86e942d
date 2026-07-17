#!/usr/bin/env python3
"""REALFIBER Probe-1 — exact local geometry of the real moment fiber at the cospectral pair.
Predecl pin 9f706c1a74a21317. Exact-Q on all verdict paths."""
import json, hashlib
from itertools import combinations
import sympy as sp

GRADER_CLAUSES = {
 "P-R1": "membership control — both charpolys equal `λ⁵ − 4λ³` exactly.",
 "P-R2": "`c(A₁) = c(A₂) = 3` (spectrum type (1,3,1)) ⟹ orbit-tangent dim 7 at both.",
 "P-R3": "rank ψ = **4 at the star, 3 at the cycle** (per pinned derivation).",
 "P-R4": "star = REGULAR point of μ|O_λ (local fiber dim 3); cycle = CRITICAL point (kernel-in-orbit dim 4 > 3).",
 "C-1": "ψ-rank = 4 at `RᵀA₁R` for a pinned rational Cayley R (generic non-fiber orbit point).",
}
pre = open("portfolio/campaigns/deficit_engine/REALFIBER_PREDECL.md", encoding="utf-8").read()
for k, cl in GRADER_CLAUSES.items():
    assert cl in pre, f"CLAUSE DRIFT on {k}: refuse to run"
assert hashlib.sha256(pre.encode()).hexdigest()[:16] == "9f706c1a74a21317", "PREDECL PIN MISMATCH"

m = 5
pairs = list(combinations(range(m), 2))
lam = sp.symbols('lam')

def adj(edges):
    W = sp.zeros(m)
    for (i, j) in edges: W[i, j] = W[j, i] = sp.Integer(1)
    return W
A1 = adj([(0,1),(0,2),(0,3),(0,4)])        # star K_{1,4}
A2 = adj([(0,1),(1,2),(2,3),(3,0)])        # C4 + isolated vertex 4

def psi_rank(W):
    cols = []
    for (a, b) in pairs:
        col = sp.zeros(m, 1)
        col[a, 0] = -2 * W[a, b]
        col[b, 0] =  2 * W[a, b]
        cols.append(col)
    return sp.Matrix.hstack(*cols).rank()

def commutant_dim(W):
    # A skew, [W,A]=0: unknowns = 10 pair coefficients
    x = sp.symbols('x0:10')
    A = sp.zeros(m)
    for k, (a, b) in enumerate(pairs):
        A[a, b] = x[k]; A[b, a] = -x[k]
    C = W * A - A * W
    eqs = [C[i, j] for i in range(m) for j in range(i, m)]
    M = sp.Matrix([[sp.diff(e, v) for v in x] for e in eqs])
    return 10 - M.rank()

cp1 = sp.expand(A1.charpoly(lam).as_expr())
cp2 = sp.expand(A2.charpoly(lam).as_expr())
target = sp.expand(lam**5 - 4*lam**3)
r1, r2 = psi_rank(A1), psi_rank(A2)
c1, c2 = commutant_dim(A1), commutant_dim(A2)
orbit_dim1, orbit_dim2 = 10 - c1, 10 - c2
ker_in_orbit_1 = orbit_dim1 - r1   # dim of D_W directions at the point
ker_in_orbit_2 = orbit_dim2 - r2
# C-1: generic orbit point via rational Cayley (u=(1,2,0,-1,1), skew A=uv^T-vu^T with v=(0,1,-1,2,0))
u = sp.Matrix([1, 2, 0, -1, 1]); v = sp.Matrix([0, 1, -1, 2, 0])
S = u * v.T - v * u.T
R = (sp.eye(m) - S) * (sp.eye(m) + S).inv()
Wg = (R.T * A1 * R).applyfunc(sp.nsimplify)
rg = psi_rank(Wg)

V = {}
V["P-R1"] = (sp.expand(cp1 - target) == 0 and sp.expand(cp2 - target) == 0)
V["P-R2"] = (c1 == 3 and c2 == 3 and orbit_dim1 == 7 and orbit_dim2 == 7)
V["P-R3"] = (r1 == 4 and r2 == 3)
V["P-R4"] = (r1 == 4 and ker_in_orbit_1 == 3 and r2 == 3 and ker_in_orbit_2 == 4)
V["C-1"] = (rg == 4)
rec = {"predecl_pin": "9f706c1a74a21317",
       "measured": {"rank_psi_star": int(r1), "rank_psi_cycle": int(r2),
                    "commutant_star": int(c1), "commutant_cycle": int(c2),
                    "orbit_dim": [int(orbit_dim1), int(orbit_dim2)],
                    "kernel_in_orbit": [int(ker_in_orbit_1), int(ker_in_orbit_2)],
                    "generic_orbit_point_rank": int(rg)},
       "verdicts": {k: bool(x) for k, x in V.items()}}
blob = json.dumps(rec, sort_keys=True, indent=1)
print(blob)
print("RECORDS_SHA256", hashlib.sha256(blob.encode()).hexdigest()[:16])
print("ALL_PASS" if all(V.values()) else "FAIL -> HALT PER KILL CONDITIONS")
