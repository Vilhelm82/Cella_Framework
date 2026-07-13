#!/usr/bin/env python3
"""stageB_battery.py -- FLAGSHIP STAGE B (SUCCESSION), PREREG_v2 battery.
role=probe. Gates: pin check (REFUSE_MISMATCH), clause check (CLAUSE_DRIFT),
PB.0 sanity (K-B0). Probe path: isotypic projection residual. Referee path
(independent): generator commutation [S_sigma, Q_nu] = 0. Must agree.
Exact arithmetic: fractions.Fraction throughout; sympy only for the n=3
symbolic identity gate. Deterministic. Run twice for byte-stability x2.
Usage: stageB_battery.py OUTPATH [--gates-only]
Defs first, dispatch last."""
import sys, os, json, hashlib, itertools
from fractions import Fraction as Fr
BASE = '/home/wlloyd/Lloyd_Engine_V4'
HERE = BASE + '/portfolio/campaigns/shape_witness/stage_B_succession'
sys.path.insert(0, BASE + '/evals/dbp_involution')
import rep_utils as RU

GRADER_CLAUSES = {
 "PB.0": "(i) in-battery symbolic gate: −q·e_2(PH_cP) ≡ Spec-§4 Δ_c at n=3, all g, all H_c; (ii) keystone: Δ_c^(3)=4, Q_ν = 2I−J exactly in ν-coords (both weights), (c_triv,c_std)=(−1,2); (iii) projector gates at n=4,5,6: ranks (1,n−1,n(n−3)/2), idempotent, orthogonal, sum = I on pair module",
 "PB.1": "for ≥1 weight cell: Q_ν(g) ∈ span_Q{P_triv,P_std,P_shape} EXACTLY (zero residual, exact ℚ) at ALL FOUR fixtures n4a,n4b,n5a,n5b ⟹ Δ_c^(n) = c_triv·m2_triv + c_std·m2_std + c_shape·m2_shape",
 "PB.2": "on surviving cell(s): coefficients g-INDEPENDENT (equal across the two g-fixtures at each n) AND the unique deg-≤2 polynomial in n through n=3,4,5 values RETRODICTS n=6 exactly (c_shape: linear through n=4,5, retrodicts n=6; n=3 unconstrained, shape dim 0). Ansatz ladder FROZEN: deg-≤2 polynomial only; no post-hoc function families",
}

def sha256_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def gate_pins_and_clauses():
    pins = {}
    for line in open(HERE + '/freeze_pins.sha256'):
        h, path = line.split()
        pins[path] = h
    for path, h in pins.items():
        full = BASE + '/' + path
        if sha256_file(full) != h:
            print("REFUSE_MISMATCH " + path); sys.exit(2)
    prereg = open(HERE + '/PREREG_v2.md', encoding='utf-8').read()
    for cid, clause in GRADER_CLAUSES.items():
        if clause not in prereg:
            print("CLAUSE_DRIFT " + cid); sys.exit(3)
    return pins

# ---------- exact linear algebra on Fractions ----------
def pairs_of(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]

def mat_mul(A, B):
    m, k, l = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(l)]
            for i in range(m)]

def mat_tr(A):
    return sum(A[i][i] for i in range(len(A)))

def sym_from_offdiag(n, h):
    M = [[Fr(0)] * n for _ in range(n)]
    for idx, (i, j) in enumerate(pairs_of(n)):
        M[i][j] = M[j][i] = Fr(h[idx])
    return M

def tangent_P(g):
    n = len(g)
    q = sum(x * x for x in g)
    return [[(Fr(1) if i == j else Fr(0)) - Fr(g[i] * g[j], q)
             for j in range(n)] for i in range(n)], q

def e2_form_value(P, q, n, h):
    A = mat_mul(mat_mul(P, sym_from_offdiag(n, h)), P)
    e2 = (mat_tr(A) ** 2 - mat_tr(mat_mul(A, A))) / 2
    return -q * e2   # Delta_c^(n) := -q * e_2(P Hc P)

def polarize_Q(P, q, n):
    N = n * (n - 1) // 2
    def f(v): return e2_form_value(P, q, n, v)
    diag = []
    for i in range(N):
        e = [Fr(0)] * N; e[i] = Fr(1)
        diag.append(f(e))
    Q = [[Fr(0)] * N for _ in range(N)]
    for i in range(N):
        Q[i][i] = diag[i]
        for j in range(i + 1, N):
            e = [Fr(0)] * N; e[i] = Fr(1); e[j] = Fr(1)
            Q[i][j] = Q[j][i] = (f(e) - diag[i] - diag[j]) / 2
    return Q

# ---------- isotypic projectors on the pair module ----------
def pair_perm_matrix(n, p):
    prs = pairs_of(n); idx = {pr: k for k, pr in enumerate(prs)}
    N = len(prs)
    M = [[Fr(0)] * N for _ in range(N)]
    for k, (i, j) in enumerate(prs):
        a, b = p[i], p[j]
        M[idx[(min(a, b), max(a, b))]][k] = Fr(1)
    return M

def projectors(n):
    from math import factorial
    lams = [(n,), (n - 1, 1)] + ([(n - 2, 2)] if n >= 4 else [])
    Ps = []
    N = n * (n - 1) // 2
    perms = list(itertools.permutations(range(n)))
    mats = [(p, pair_perm_matrix(n, p)) for p in perms]
    for lam in lams:
        d = RU.specht_dim(lam)
        P = [[Fr(0)] * N for _ in range(N)]
        for p, M in mats:
            chi = RU.specht_char(lam, RU.cycle_type(p))
            if chi == 0: continue
            for i in range(N):
                Mi = M[i]
                for j in range(N):
                    if Mi[j]: P[i][j] += chi * Mi[j]
        c = Fr(d, factorial(n))
        Ps.append([[c * P[i][j] for j in range(N)] for i in range(N)])
    return Ps

def mat_rank(A):
    M = [row[:] for row in A]; n, m = len(M), len(M[0]); r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = Fr(1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(n):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r

def gate_projectors(n, Ps):
    N = n * (n - 1) // 2
    want = (1, n - 1, n * (n - 3) // 2)
    assert tuple(mat_rank(P) for P in Ps) == want, "K-B0 projector rank"
    for P in Ps:
        assert mat_mul(P, P) == P, "K-B0 idempotency"
    for a in range(3):
        for b in range(a + 1, 3):
            Z = mat_mul(Ps[a], Ps[b])
            assert all(x == 0 for row in Z for x in row), "K-B0 orthogonality"
    I = [[Fr(int(i == j)) for j in range(N)] for i in range(N)]
    S = [[Ps[0][i][j] + Ps[1][i][j] + Ps[2][i][j] for j in range(N)]
         for i in range(N)]
    assert S == I, "K-B0 partition of identity"

def weights(n, g, kind):
    out = []
    for (i, j) in pairs_of(n):
        rest = [g[k] for k in range(n) if k not in (i, j)]
        if kind == 'W-prod':
            w = 1
            for x in rest: w *= x
        else:
            w = sum(rest)
        out.append(Fr(w))
    return out

def q_nu(Q, W):
    N = len(W)
    return [[Q[i][j] / (W[i] * W[j]) for j in range(N)] for i in range(N)]

def span_decompose(Q, Ps):
    cs, R = [], [row[:] for row in Q]
    for P in Ps:
        num = mat_tr(mat_mul(Q, P)); den = mat_tr(P)
        c = num / den; cs.append(c)
        for i in range(len(R)):
            for j in range(len(R)):
                R[i][j] -= c * P[i][j]
    zero = all(x == 0 for row in R for x in row)
    return cs, zero

def commutant_check(n, Q):
    gens = [tuple([1, 0] + list(range(2, n))),
            tuple(list(range(1, n)) + [0])]
    for p in gens:
        S = pair_perm_matrix(n, p)
        if mat_mul(S, Q) != mat_mul(Q, S):
            return False
    return True

def pb0_symbolic_gate():
    import sympy as sp
    g1, g2, g3, a, b, c = sp.symbols('g1 g2 g3 a b c')
    g = sp.Matrix([g1, g2, g3]); q = (g.T * g)[0]
    Hc = sp.Matrix([[0, a, b], [a, 0, c], [b, c, 0]])
    P = sp.eye(3) - g * g.T / q
    A = P * Hc * P
    e2 = ((A.trace()) ** 2 - (A * A).trace()) / 2
    Dc = (g1**2*c**2 + g2**2*b**2 + g3**2*a**2
          - 2*g1*g2*b*c - 2*g1*g3*a*c - 2*g2*g3*a*b)
    return sp.simplify(sp.simplify(-q * e2) - Dc) == 0

def pb0_keystone(fx):
    g = fx['g']; h = [Fr(x) for x in fx['Hc_offdiag']]
    P, q = tangent_P(g)
    assert q == 14, "K-B0 keystone q"
    val = e2_form_value(P, q, 3, h)
    assert val == 4, "K-B0 keystone Delta_c != 4"
    Q = polarize_Q(P, q, 3)
    ok = {}
    for kind in ('W-prod', 'W-sum'):
        W = weights(3, g, kind)
        Qn = q_nu(Q, W)
        twoIJ = [[Fr(2) if i == j else Fr(0) for j in range(3)]
                 for i in range(3)]
        for i in range(3):
            for j in range(3): twoIJ[i][j] -= 1
        ok[kind] = (Qn == twoIJ)
        assert Qn == twoIJ, "K-B0 keystone Q_nu != 2I-J (" + kind + ")"
        Ps3 = projectors(3)
        c_t = mat_tr(mat_mul(Qn, Ps3[0])) / mat_tr(Ps3[0])
        c_s = mat_tr(mat_mul(Qn, Ps3[1])) / mat_tr(Ps3[1])
        assert (c_t, c_s) == (Fr(-1), Fr(2)), "K-B0 keystone coeffs"
    return True

def lagrange_eval(pts, x):
    tot = Fr(0)
    for i, (xi, yi) in enumerate(pts):
        term = yi
        for j, (xj, _) in enumerate(pts):
            if i != j:
                term *= Fr(x - xj, xi - xj)
        tot += term
    return tot

def main():
    outp = sys.argv[1]
    gates_only = '--gates-only' in sys.argv
    pins = gate_pins_and_clauses()
    fx = json.load(open(HERE + '/fixtures_stageB.json'))
    rows = []
    led = {"role": "probe", "prereg": "PREREG_v2.md",
           "prereg_sha256": pins['portfolio/campaigns/shape_witness/'
                                'stage_B_succession/PREREG_v2.md'],
           "battery_sha256": sha256_file(os.path.abspath(__file__))}
    assert pb0_symbolic_gate(), "K-B0 symbolic identity"
    assert pb0_keystone(fx['keystone_n3']), "K-B0 keystone"
    Pcache = {}
    for n in (4, 5, 6):
        Pcache[n] = projectors(n)
        gate_projectors(n, Pcache[n])
    rows.append({"row": "PB0", "symbolic_identity": True, "keystone": True,
                 "projector_gates": [4, 5, 6], "pass": True})
    if gates_only:
        print("GATES_ONLY_OK"); return
    cells = {}
    for f in fx['fixtures']:
        n, g, h = f['n'], f['g'], [Fr(x) for x in f['Hc_offdiag']]
        P, q = tangent_P(g)
        Q = polarize_Q(P, q, n)
        for kind in ('W-prod', 'W-sum'):
            Qn = q_nu(Q, weights(n, g, kind))
            cs, zero = span_decompose(Qn, Pcache[n])
            comm = commutant_check(n, Qn)
            assert zero == comm, "probe/referee disagree"
            cells.setdefault(kind, {})[f['id']] = (cs, zero)
            rows.append({"row": "PB1", "fixture": f['id'], "n": n,
                         "weight": kind, "residual_zero": zero,
                         "referee_commutant": comm,
                         "c": [str(c) for c in cs]})
    verdicts = {}
    pb1_cells = {}
    for kind in ('W-prod', 'W-sum'):
        ok = all(cells[kind][i][1] for i in ('n4a', 'n4b', 'n5a', 'n5b'))
        pb1_cells[kind] = ok
    verdicts['PB.1'] = {"pass": any(pb1_cells.values()), "cells": pb1_cells}

    pb2 = {}
    for kind in ('W-prod', 'W-sum'):
        if not pb1_cells[kind]:
            pb2[kind] = {"pass": False, "reason": "cell failed PB.1"}
            continue
        gind = all(cells[kind][a][0] == cells[kind][b][0]
                   for a, b in (('n4a', 'n4b'), ('n5a', 'n5b'),
                                ('n6a', 'n6b')))
        entry = {"g_independent": gind}
        if gind:
            c4, c5 = cells[kind]['n4a'][0], cells[kind]['n5a'][0]
            c6 = cells[kind]['n6a'][0]
            fits = []
            for k, n3val in ((0, Fr(-1)), (1, Fr(2))):
                pred = lagrange_eval([(3, n3val), (4, c4[k]), (5, c5[k])], 6)
                fits.append(pred == c6[k])
            pred_sh = lagrange_eval([(4, c4[2]), (5, c5[2])], 6)
            fits.append(pred_sh == c6[2])
            entry["n6_retrodicted"] = fits
            entry["pass"] = all(fits)
            entry["c_n4"] = [str(x) for x in c4]
            entry["c_n5"] = [str(x) for x in c5]
            entry["c_n6"] = [str(x) for x in c6]
        else:
            entry["pass"] = False
        pb2[kind] = entry
    verdicts['PB.2'] = pb2
    verdicts['PB.0'] = {"pass": True}
    rows.append({"row": "VERDICTS", "verdicts": verdicts, "ledger": led})
    with open(outp, 'w') as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(json.dumps(verdicts, sort_keys=True, indent=1))
    print("STAGEB_DONE")

main()
