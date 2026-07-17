#!/usr/bin/env python3
"""Deficit Engine wave-0 calibration battery. Predecl pin c6fd7018a4602209.
Exact-Q on all verdict paths. role=probe; referee = exact rank / exact polynomial identity."""
import sys, json, hashlib
from itertools import combinations
import sympy as sp

GRADER_CLAUSES = {
 "P-A1": "rank dΦ_σ = 4 exactly at O* and O**; deficit = 6.",
 "P-A2": "the 6 tangent vectors δO_k span dim 6 exactly AND Jacobian·δO_k = 0 exactly for all k",
 "P-B1": "c₁ ≡ 0 identically; rank dΦ = m−1 exactly at the pinned points; deficits 3 (m=4) and 6 (m=5).",
 "P-B2": "the cospectral pair has exactly equal char polys in ℤ[λ] AND distinct S₅-orbits",
 "C-1": "Φ_id = the coordinate functions themselves (m=4 graph row) must give rank 6, deficit 0.",
 "C-2": "Row-A rank identical at O* and O** (genericity ×2).",
}
pre = open("portfolio/campaigns/deficit_engine/WAVE0_PREDECL.md", encoding="utf-8").read()
for k, cl in GRADER_CLAUSES.items():
    assert cl in pre, f"CLAUSE DRIFT on {k}: refuse to run"
assert hashlib.sha256(pre.encode()).hexdigest()[:16] == "c6fd7018a4602209", "PREDECL PIN MISMATCH"

R = sp.Rational
# ---------- ROW A ----------
n = 5
g = [R(x) for x in (1, 2, 3, 5, 7)]
PAIRS = list(combinations(range(n), 2))
o = sp.symbols('o0:10')
def M_of(vec):
    H = sp.zeros(n)
    for k, (i, j) in enumerate(PAIRS):
        H[i, j] = H[j, i] = vec[k]
    return H
H = M_of(o)
def Ehat_expr(H, r):
    tot = sp.Integer(0)
    for I in combinations(range(n), r + 1):
        m = sp.zeros(r + 2)
        for a, i in enumerate(I):
            m[0, a+1] = m[a+1, 0] = g[i]
            for b, j in enumerate(I):
                m[a+1, b+1] = H[i, j]
        tot += m.det()
    return sp.expand((-1) ** (r + 1) * tot)
Phi = [Ehat_expr(H, r) for r in (1, 2, 3, 4)]
Jac = sp.Matrix([[sp.diff(f, v) for v in o] for f in Phi])
Ostar  = [R(x) for x in (1, -2, 3, 1, 2, -1, 4, -3, 1, 2)]
Ostar2 = [R(x) for x in (2, 1, -1, 3, -2, 1, 1, 2, -1, 3)]
def rank_at(P):
    return sp.Matrix(Jac.subs(dict(zip(o, P)))).rank()
rA1, rA2 = rank_at(Ostar), rank_at(Ostar2)
# hidden-group tangents: so(4)_g basis via pairs of a g-perp basis
gperp = []
for i in range(1, n):  # v_i = g_i e_0 − g_0 e_i  ⟂ g
    v = [R(0)] * n; v[0] = g[i]; v[i] = -g[0]; gperp.append(sp.Matrix(v))
As = []
for (a, b) in combinations(range(4), 2):
    u, v = gperp[a], gperp[b]
    As.append(u * v.T - v * u.T)
assert all((A * sp.Matrix(g)).is_zero_matrix for A in As) and len(As) == 6
Hstar = M_of(Ostar)
def O_of_matrix(Hm):
    return [Hm[i, j] - g[i]*Hm[j, j]/(2*g[j]) - g[j]*Hm[i, i]/(2*g[i]) for (i, j) in PAIRS]
Tvecs = []
for A in As:
    dH = Hstar * A - A * Hstar          # infinitesimal conjugation [H, A]
    Tvecs.append(sp.Matrix(O_of_matrix(dH)))
Tmat = sp.Matrix.hstack(*Tvecs)
span_dim = Tmat.rank()
Jstar = sp.Matrix(Jac.subs(dict(zip(o, Ostar))))
containment = all((Jstar * t).is_zero_matrix for t in Tvecs)

# ---------- ROW B ----------
def graph_row(m, wvals):
    N = m * (m - 1) // 2
    w = sp.symbols(f'w0:{N}')
    W = sp.zeros(m)
    for k, (i, j) in enumerate(combinations(range(m), 2)):
        W[i, j] = W[j, i] = w[k]
    lam = sp.symbols('lam')
    cp = W.charpoly(lam).as_expr()
    coeffs = [sp.expand(cp.coeff(lam, m - d)) for d in range(1, m + 1)]  # c1..cm signs folded in
    c1_zero = sp.simplify(coeffs[0]) == 0
    Phi = coeffs[1:]  # nonconstant summary c2..cm
    J = sp.Matrix([[sp.diff(f, v) for v in w] for f in Phi])
    pt = dict(zip(w, [R(x) for x in wvals]))
    return c1_zero, sp.Matrix(J.subs(pt)).rank(), N
c1z4, rB4, N4 = graph_row(4, (1, 2, 3, 4, 5, 6))
c1z5, rB5, N5 = graph_row(5, (1, -2, 3, 1, 2, -1, 4, -3, 1, 2))
# C-1: identity summary at m=4
w4 = sp.symbols('w0:6')
Jid = sp.Matrix([[sp.diff(f, v) for v in w4] for f in list(w4)])
rank_id = Jid.rank()
# P-B2: imported cospectral witness at m=5 (0/1 weights)
def adj(edges, m=5):
    W = sp.zeros(m)
    for (i, j) in edges: W[i, j] = W[j, i] = 1
    return W
K14 = adj([(0,1),(0,2),(0,3),(0,4)])
C4K1 = adj([(0,1),(1,2),(2,3),(3,0)])
lam = sp.symbols('lam')
cp_equal = sp.expand(K14.charpoly(lam).as_expr() - C4K1.charpoly(lam).as_expr()) == 0
deg = lambda W: tuple(sorted([sum(W[i, j] for j in range(5)) for i in range(5)], reverse=True))
orbits_distinct = deg(K14) != deg(C4K1)

V = {}
V["P-A1"] = (rA1 == 4 and rA2 == 4)
V["P-A2"] = (span_dim == 6 and containment)
V["P-B1"] = (c1z4 and c1z5 and rB4 == 3 and rB5 == 4)
V["P-B2"] = (cp_equal and orbits_distinct)
V["C-1"] = (rank_id == 6)
V["C-2"] = (rA1 == rA2)
rec = {"predecl_pin": "c6fd7018a4602209",
       "verdicts": {k: bool(v) for k, v in V.items()},
       "measured": {"rankA_Ostar": int(rA1), "rankA_Ostar2": int(rA2),
                    "deficit_A": 10 - int(rA1), "tangent_span": int(span_dim),
                    "containment_exact": bool(containment),
                    "rank_B_m4": int(rB4),
                    "rank_B_m5": int(rB5), "deficit_B_m5": N5 - int(rB5),
                    "cospectral_charpoly_equal": bool(cp_equal),
                    "degseq": [[int(x) for x in deg(K14)], [int(x) for x in deg(C4K1)]]}}
rec["measured"]["deficit_B_m4"] = N4 - int(rB4)
blob = json.dumps(rec, sort_keys=True, indent=1)
print(blob)
print("RECORDS_SHA256", hashlib.sha256(blob.encode()).hexdigest()[:16])
print("ALL_PASS" if all(V.values()) else "FAIL -> HALT PER KILL CONDITIONS")
