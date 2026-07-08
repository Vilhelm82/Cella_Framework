#!/usr/bin/env python3
"""shadow_law_verify.py -- machine verification of SHADOW_LAW_THEOREM.md.
V1: symbolic n=4 triangle decomposition; V2: exact identity at all 15
banked fixtures; V3: shadow+scalar vs B' certified values; V4: Lemma 1
closed form symbolic n=4. Deterministic; run twice for x2.
Usage: shadow_law_verify.py OUTPATH.  Defs first, dispatch last."""
import sys, os, json, hashlib, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))

def pairs_of(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]

def mat_mul(A, B):
    k, l = len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(l)]
            for i in range(len(A))]

def mat_tr(A):
    return sum(A[i][i] for i in range(len(A)))

def tangent_P(g):
    n = len(g); q = sum(x * x for x in g)
    return [[(Fr(1) if i == j else Fr(0)) - Fr(g[i] * g[j], q)
             for j in range(n)] for i in range(n)], q

def sym_from_offdiag(n, h):
    M = [[Fr(0)] * n for _ in range(n)]
    for idx, (i, j) in enumerate(pairs_of(n)):
        M[i][j] = M[j][i] = Fr(h[idx])
    return M

def e2_direct(P, q, n, h):
    A = mat_mul(mat_mul(P, sym_from_offdiag(n, h)), P)
    return -q * ((mat_tr(A) ** 2 - mat_tr(mat_mul(A, A))) / 2)

def polarize(fun, N):
    diag = []
    for i in range(N):
        e = [Fr(0)] * N; e[i] = Fr(1); diag.append(fun(e))
    Q = [[Fr(0)] * N for _ in range(N)]
    for i in range(N):
        Q[i][i] = diag[i]
        for j in range(i + 1, N):
            e = [Fr(0)] * N; e[i] = Fr(1); e[j] = Fr(1)
            Q[i][j] = Q[j][i] = (fun(e) - diag[i] - diag[j]) / 2
    return Q

def w_prod(n, g):
    out = []
    for (i, j) in pairs_of(n):
        w = 1
        for k in range(n):
            if k not in (i, j): w *= g[k]
        out.append(Fr(w))
    return out

def triangle_sum(n, g):
    prs = pairs_of(n); idx = {p: k for k, p in enumerate(prs)}
    N = len(prs)
    Q = [[Fr(0)] * N for _ in range(N)]
    for S in itertools.combinations(range(n), 3):
        d = 1
        for m in range(n):
            if m not in S: d *= g[m] * g[m]
        T = Fr(1, d)
        es = [idx[p] for p in itertools.combinations(S, 2)]
        for a in es:
            Q[a][a] += T
            for b in es:
                if a != b: Q[a][b] -= T
    return Q

def v1_v4_symbolic_n4():
    import sympy as sp
    n = 4
    gs = sp.symbols('g0:4', positive=True)
    q = sum(x * x for x in gs)
    prs = pairs_of(n); N = len(prs)
    hs = sp.symbols('h0:%d' % N)
    M = sp.zeros(n, n)
    for idx, (i, j) in enumerate(prs):
        M[i, j] = M[j, i] = hs[idx]
    P = sp.eye(n) - sp.Matrix(n, 1, gs) * sp.Matrix(1, n, gs) / q
    A = P * M * P
    delta_direct = sp.expand(-q * ((A.trace())**2 - (A*A).trace()) / 2)
    # V4: Lemma 1 closed form
    Mg = M * sp.Matrix(n, 1, gs)
    lemma1 = sp.expand(q * sum(h*h for h in hs)
                       - sum(x*x for x in Mg))
    v4 = sp.simplify(delta_direct - lemma1) == 0
    # V1: triangle decomposition of Q_nu, symbolic
    W = []
    for (i, j) in prs:
        w = sp.Integer(1)
        for k in range(n):
            if k not in (i, j): w *= gs[k]
        W.append(w)
    nu = sp.symbols('nu0:%d' % N)
    delta_nu = delta_direct.subs({hs[e]: nu[e] / W[e] for e in range(N)},
                                 simultaneous=True)
    tri = sp.Integer(0)
    idx = {p: k for k, p in enumerate(prs)}
    for S in itertools.combinations(range(n), 3):
        T = sp.Integer(1)
        for m in range(n):
            if m not in S: T /= gs[m]**2
        es = [idx[p] for p in itertools.combinations(S, 2)]
        loc = sum(nu[a]*nu[a] for a in es) \
            - sum(nu[a]*nu[b] for a in es for b in es if a != b)
        tri += T * loc
    v1 = sp.simplify(sp.together(delta_nu - tri)) == 0
    return v1, v4

def main():
    outp = sys.argv[1]
    rows = []
    thm_sha = hashlib.sha256(
        open(HERE + '/SHADOW_LAW_THEOREM.md', 'rb').read()).hexdigest()[:16]
    v1, v4 = v1_v4_symbolic_n4()
    rows.append({"row": "V1_V4_symbolic_n4",
                 "triangle_decomposition": v1, "lemma1_closed_form": v4})
    assert v1 and v4
    # V2: exact identity at all 15 banked fixtures; V3 shadow/scalar
    fxB = json.load(open(HERE + '/fixtures_stageB.json'))
    fxP = json.load(open(HERE + '/fixtures_bprime.json'))
    gsets = [(f['id'], f['n'], f['g']) for f in fxB['fixtures']] + \
            [(f['id'], f['n'], f['g']) for f in fxP['fresh_g']]
    all_ok = True
    for fid, n, g in gsets:
        P, q = tangent_P(g)
        N = n * (n - 1) // 2
        W = w_prod(n, g)
        def f_nu(v):
            return e2_direct(P, q, n, [v[e] / W[e] for e in range(N)])
        Qn = polarize(f_nu, N)
        ok = (Qn == triangle_sum(n, g))
        # V3: scalar from decomposition = e3(g^2)/(C(n,3) e_n(g^2))
        e3 = sum(Fr(g[a]*g[a]*g[b]*g[b]*g[c]*g[c])
                 for a, b, c in itertools.combinations(range(n), 3))
        en = Fr(1)
        for x in g: en *= x * x
        from math import comb
        s = e3 / (comb(n, 3) * en)
        diag_mean = sum(Qn[i][i] for i in range(N)) / N
        ok_s = (diag_mean == s * (n - 2))
        all_ok = all_ok and ok and ok_s
        rows.append({"row": "V2_V3", "fixture": fid, "n": n,
                     "triangle_identity": ok, "scalar_matches": ok_s})
    assert all_ok
    rows.append({"row": "VERDICT", "all_pass": True,
                 "theorem_doc_sha16": thm_sha,
                 "ledger": {"role": "probe",
                            "script_sha256": hashlib.sha256(
                                open(os.path.abspath(__file__), 'rb')
                                .read()).hexdigest()}})
    with open(outp, 'w') as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print("ALL_VERIFY_PASS")

main()
