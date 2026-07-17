#!/usr/bin/env python3
"""ROWB_MECH battery — graph-slice mechanism certification. Predecl pin 0c335fe2fa474d64.
Exact-Q on all verdict paths. role=probe; referee = exact rank / exact zero."""
import json, hashlib
from itertools import combinations
import sympy as sp

GRADER_CLAUSES = {
 "P1": "rank ψ_W = m−1 exactly at all four pinned points.",
 "P2": "dim D_W = (m−1)(m−2)/2 exactly (= 3 at m=4, 6 at m=5); mechanism: ker ψ_W ∩ commutant = 0 under G1.",
 "P3": "Jacobian(dΦ)·d = 0 exactly for every spanning vector d of D_W.",
 "P4": "dim D_W = dim ker dΦ (deficit recomputed in-battery, not imported), whence with P3: `ker dΦ = D_W` at the point. All four points.",
 "G1": "charpoly squarefree at every pinned point, exact gcd test",
}
pre = open("portfolio/campaigns/deficit_engine/ROWB_MECH_PREDECL.md", encoding="utf-8").read()
for k, cl in GRADER_CLAUSES.items():
    assert cl in pre, f"CLAUSE DRIFT on {k}: refuse to run"
assert hashlib.sha256(pre.encode()).hexdigest()[:16] == "0c335fe2fa474d64", "PREDECL PIN MISMATCH"

R = sp.Rational
lam = sp.symbols('lam')

def run_point(m, wvals):
    N = m * (m - 1) // 2
    pairs = list(combinations(range(m), 2))
    # pinned W
    W = sp.zeros(m)
    for k, (i, j) in enumerate(pairs):
        W[i, j] = W[j, i] = R(wvals[k])
    # G1: simple spectrum (squarefree charpoly)
    p = W.charpoly(lam).as_expr()
    g1 = sp.degree(sp.gcd(p, sp.diff(p, lam)), lam) == 0
    # psi_W matrix: rows = diagonal entries 0..m-1, cols = so(m) basis E_ab
    psi = sp.zeros(m, N)
    for c, (a, b) in enumerate(pairs):
        A = sp.zeros(m); A[a, b] = 1; A[b, a] = -1
        Bm = W * A - A * W
        for i in range(m):
            psi[i, c] = Bm[i, i]
    rank_psi = psi.rank()
    kerA = psi.nullspace()           # coeff vectors in the E_ab basis
    # D_W spanning vectors in pair coordinates of the zero-diagonal slice
    Dvecs = []
    for v in kerA:
        A = sp.zeros(m)
        for c, (a, b) in enumerate(pairs):
            A[a, b] += v[c]; A[b, a] -= v[c]
        Bm = W * A - A * W           # symmetric, zero diagonal on ker psi
        assert all(sp.simplify(Bm[i, i]) == 0 for i in range(m)), "kernel vector left the slice"
        Dvecs.append(sp.Matrix([Bm[i, j] for (i, j) in pairs]))
    dimD = sp.Matrix.hstack(*Dvecs).rank() if Dvecs else 0
    # summary Jacobian at the point (c2..cm on symbolic zero-diagonal slice)
    w = sp.symbols(f'w0:{N}')
    Ws = sp.zeros(m)
    for k, (i, j) in enumerate(pairs):
        Ws[i, j] = Ws[j, i] = w[k]
    cps = Ws.charpoly(lam).as_expr()
    Phi = [sp.expand(cps.coeff(lam, m - d)) for d in range(2, m + 1)]
    J = sp.Matrix([[sp.diff(f, v) for v in w] for f in Phi]).subs(dict(zip(w, [R(x) for x in wvals])))
    rank_J = sp.Matrix(J).rank()
    deficit = N - rank_J
    containment = all((sp.Matrix(J) * d).is_zero_matrix for d in Dvecs)
    return {"G1": bool(g1), "rank_psi": int(rank_psi), "dim_D": int(dimD),
            "rank_J": int(rank_J), "deficit": int(deficit), "containment": bool(containment)}

points = [(4, (1, 2, 3, 4, 5, 6)), (4, (2, 1, -1, 3, -2, 1)),
          (5, (1, -2, 3, 1, 2, -1, 4, -3, 1, 2)), (5, (2, 1, -1, 3, -2, 1, 1, 2, -1, 3))]
res = [dict(m=m, w=list(wv), **run_point(m, wv)) for m, wv in points]

V = {}
V["G1-all"] = all(r["G1"] for r in res)
V["P1"] = all(r["rank_psi"] == r["m"] - 1 for r in res)
V["P2"] = all(r["dim_D"] == (r["m"] - 1) * (r["m"] - 2) // 2 for r in res)
V["P3/C-1"] = all(r["containment"] for r in res)
V["P4"] = all(r["dim_D"] == r["deficit"] for r in res)
V["C-2"] = (res[0]["rank_psi"] == res[1]["rank_psi"] and res[2]["rank_psi"] == res[3]["rank_psi"])
rec = {"predecl_pin": "0c335fe2fa474d64", "points": res,
       "verdicts": {k: bool(v) for k, v in V.items()}}
blob = json.dumps(rec, sort_keys=True, indent=1)
print(blob)
print("RECORDS_SHA256", hashlib.sha256(blob.encode()).hexdigest()[:16])
print("ALL_PASS" if all(V.values()) else "FAIL -> HALT PER KILL CONDITIONS")
