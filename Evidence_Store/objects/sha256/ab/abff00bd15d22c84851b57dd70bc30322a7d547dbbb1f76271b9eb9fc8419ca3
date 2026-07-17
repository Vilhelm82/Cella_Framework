#!/usr/bin/env python3
"""shape_witness battery — n=5 sigma-blind shape witness. Predecl pin 967c7909450ef944.
Exact-Q only on verdict paths. role=probe; referee = exact rational equality (independent
charpoly route cross-checks the bordered route)."""
import sys, json, hashlib
from fractions import Fraction as Fr
sys.path.insert(0, "evals/dbp_involution")
from rep_utils import specht_char_dict, specht_dim, conjugacy_classes, cycle_type
from itertools import combinations, permutations
import sympy as sp

GRADER_CLAUSES = {
 "P-W1": "Ê_r(H1) = Ê_r(H2) exactly, r = 1..4. [forced by mechanism if mechanism holds]",
 "P-W2": "charpoly(P·H1·P) = charpoly(P·H2·P) exactly in ℚ[z] (q cleared). [forced]",
 "P-W3": "δ = π_shape(O(H1)) − π_shape(O(H2)) ≠ 0 exactly. [expected, not forced]",
 "P-W4": "m2_shape(O1) ≠ m2_shape(O2). [expected; fallback m3_shape; only-triv/std ⟹ PARTIAL]",
 "C-1": "identity pair → everything equal.",
 "C-2": "gauge pair (H1 vs H1+gbᵀ+bgᵀ) → Ê_r equal, O equal, shape equal.",
 "C-3": "perturbed pair → some Ê_r differs (detector non-vacuous).",
}
# gate: clauses must appear verbatim in the frozen predecl
pre = open("portfolio/campaigns/shape_witness/WITNESS_PREDECL.md", encoding="utf-8").read()
for k, cl in GRADER_CLAUSES.items():
    assert cl in pre, f"CLAUSE DRIFT on {k}: refuse to run"
assert hashlib.sha256(pre.encode()).hexdigest()[:16] == "967c7909450ef944", "PREDECL PIN MISMATCH"

n = 5
g = [Fr(x) for x in (1, 2, 3, 5, 7)]
PAIRS = list(combinations(range(n), 2))  # lex
offd = [Fr(x) for x in (1, -2, 3, 1, 2, -1, 4, -3, 1, 2)]

def sym_from_pairs(vec, diag=None):
    M = [[Fr(0)] * n for _ in range(n)]
    for (i, j), v in zip(PAIRS, vec):
        M[i][j] = M[j][i] = v
    if diag:
        for i in range(n): M[i][i] = diag[i]
    return M

H1 = sym_from_pairs(offd)

def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def matT(A): return [list(r) for r in zip(*A)]
def cayley(u, v):
    u = [Fr(x) for x in u]; v = [Fr(x) for x in v]
    assert sum(a*b for a, b in zip(u, g)) == 0 and sum(a*b for a, b in zip(v, g)) == 0
    A = [[u[i]*v[j] - v[i]*u[j] for j in range(n)] for i in range(n)]
    I = [[Fr(i == j) for j in range(n)] for i in range(n)]
    ImA = [[I[i][j] - A[i][j] for j in range(n)] for i in range(n)]
    IpA = sp.Matrix([[I[i][j] + A[i][j] for j in range(n)] for i in range(n)])
    Rinv = IpA.inv()
    R = [[Fr(sp.nsimplify(sum(ImA[i][k] * Rinv[k, j] for k in range(n)))) for j in range(n)] for i in range(n)]
    # exactness gates: orthogonal + fixes g
    RT = matT(R); RtR = matmul(RT, R)
    assert all(RtR[i][j] == Fr(i == j) for i in range(n) for j in range(n)), "R not orthogonal"
    assert all(sum(R[i][k] * g[k] for k in range(n)) == g[i] for i in range(n)), "Rg != g"
    return R

def conj(H, R):
    return matmul(matT(R), matmul(H, R))

def O_of(H):
    return [H[i][j] - g[i]*H[j][j]/(2*g[j]) - g[j]*H[i][i]/(2*g[i]) for (i, j) in PAIRS]

def Ehat(H, r):  # bordered-minor sum, Extension §1 at t=u=1
    tot = Fr(0)
    for I in combinations(range(n), r + 1):
        m = sp.zeros(r + 2)
        for a, i in enumerate(I):
            m[0, a+1] = m[a+1, 0] = sp.Rational(g[i])
            for b, j in enumerate(I):
                m[a+1, b+1] = sp.Rational(H[i][j])
        tot += Fr(sp.Rational(m.det()))
    return (-1) ** (r + 1) * tot

def tang_charpoly(H):  # q-cleared charpoly of P H P, P = I - g g^T/q
    q = sum(x*x for x in g)
    Pm = sp.eye(n) - sp.Matrix([[sp.Rational(g[i]*g[j]) for j in range(n)] for i in range(n)]) / sp.Rational(q)
    Hm = sp.Matrix([[sp.Rational(H[i][j]) for j in range(n)] for i in range(n)])
    z = sp.symbols('z')
    return sp.expand((Pm * Hm * Pm).charpoly(z).as_expr())

# --- isotypic projectors on the 10-dim pair module (S5), from rep_utils characters ---
def pair_perm_matrix(p):  # p: tuple perm of range(n)
    M = [[Fr(0)] * 10 for _ in range(10)]
    idx = {fr: k for k, fr in enumerate(PAIRS)}
    for k, (i, j) in enumerate(PAIRS):
        a, b = p[i], p[j]
        M[idx[(min(a, b), max(a, b))]][k] = Fr(1)
    return M

def projector(lam):
    chi = specht_char_dict(lam)  # class -> char value
    d = specht_dim(lam)
    P = [[Fr(0)] * 10 for _ in range(10)]
    for p in permutations(range(n)):
        c = Fr(int(chi[cycle_type(p)]))
        if c == 0: continue
        M = pair_perm_matrix(p)
        for i in range(10):
            for j in range(10):
                P[i][j] += c * M[i][j]
    f = Fr(d, 120)
    return [[f * P[i][j] for j in range(10)] for i in range(10)]

P_triv, P_std, P_shape = projector((5,)), projector((4, 1)), projector((3, 2))
def rank10(P): return sp.Matrix([[sp.Rational(x) for x in row] for row in P]).rank()
def apply10(P, v): return [sum(P[i][j] * v[j] for j in range(10)) for i in range(10)]
assert (rank10(P_triv), rank10(P_std), rank10(P_shape)) == (1, 4, 5), "projector rank gate"
for P in (P_triv, P_std, P_shape):
    PP = [[sum(P[i][k]*P[k][j] for k in range(10)) for j in range(10)] for i in range(10)]
    assert PP == P, "idempotency gate"
S = [[P_triv[i][j] + P_std[i][j] + P_shape[i][j] for j in range(10)] for i in range(10)]
assert all(S[i][j] == Fr(i == j) for i in range(10) for j in range(10)), "partition-of-identity gate"

def m2(v): return sum(x*x for x in v)
def m3_shape(v):
    M = sym_from_pairs(v)
    M3 = matmul(M, matmul(M, M))
    return sum(M3[i][i] for i in range(n))

def readings(H):
    O = O_of(H)
    sh, st, tv = apply10(P_shape, O), apply10(P_std, O), apply10(P_triv, O)
    return {"E": [Ehat(H, r) for r in (1, 2, 3, 4)], "cp": tang_charpoly(H), "O": O,
            "shape": sh, "m2_shape": m2(sh), "m3_shape": m3_shape(sh),
            "m2_std": m2(st), "m2_triv": m2(tv)}

R = cayley((2, -1, 0, 0, 0), (3, 0, -1, 0, 0))
H2 = conj(H1, R)
b = [Fr(x) for x in (1, -1, 2, 0, 1)]
Hg = [[H1[i][j] + g[i]*b[j] + b[i]*g[j] for j in range(n)] for i in range(n)]
Hp = [row[:] for row in H1]; Hp[0][1] += 1; Hp[1][0] += 1

r1, r2, rg, rp = readings(H1), readings(H2), readings(Hg), readings(Hp)
V = {}
V["C-1"] = (readings(H1)["E"] == r1["E"] and readings(H1)["shape"] == r1["shape"])
V["C-2"] = (rg["E"] == r1["E"] and rg["O"] == r1["O"] and rg["shape"] == r1["shape"])
V["C-3"] = (rp["E"] != r1["E"])
V["P-W1"] = (r1["E"] == r2["E"])
V["P-W2"] = (sp.expand(r1["cp"] - r2["cp"]) == 0)
delta = [a - b_ for a, b_ in zip(r1["shape"], r2["shape"])]
V["P-W3"] = any(x != 0 for x in delta)
sep_primary = (r1["m2_shape"] != r2["m2_shape"])
sep_secondary = (r1["m3_shape"] != r2["m3_shape"])
V["P-W4"] = sep_primary or sep_secondary
rec = {"predecl_pin": "967c7909450ef944",
       "verdicts": {k: bool(v) for k, v in V.items()},
       "sep": {"primary_m2_shape": bool(sep_primary), "secondary_m3_shape": bool(sep_secondary)},
       "values": {"E_r(H1)": [str(x) for x in r1["E"]],
                  "m2_shape": [str(r1["m2_shape"]), str(r2["m2_shape"])],
                  "m3_shape": [str(r1["m3_shape"]), str(r2["m3_shape"])],
                  "m2_std": [str(r1["m2_std"]), str(r2["m2_std"])],
                  "m2_triv": [str(r1["m2_triv"]), str(r2["m2_triv"])],
                  "delta_shape_nonzero_coords": sum(1 for x in delta if x != 0)}}
blob = json.dumps(rec, sort_keys=True, indent=1)
print(blob)
print("RECORDS_SHA256", hashlib.sha256(blob.encode()).hexdigest()[:16])
print("ALL_PASS" if all(V.values()) else "FAIL -> HALT PER KILL CONDITIONS")
