#!/usr/bin/env python3
"""bprime_battery.py -- STAGE B' DIRECTION-LAW PROBE, PREREG_BPRIME battery.
role=probe. W = W-prod only (W-sum retired at Stage B close, see preamble).
Probe path: symbolic identities (sympy cancel == 0). Referee path
(independent): exact-Fraction numeric evaluation at fresh fixtures; must
agree. Deterministic; run twice for byte-stability x2.
Usage: bprime_battery.py OUTPATH [--gates-only]
Defs first, dispatch last."""
import sys, os, json, hashlib, itertools
from fractions import Fraction as Fr
from math import factorial
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(HERE + '/../../../../evals/dbp_involution'))
import rep_utils as RU

GRADER_CLAUSES = {
 "PBp.0": "regression: recomputed Q_ν and shadow coefficients at the six Stage-B (n,g) fixtures match the pinned Stage-B run-1 records exactly; projector gates n=4,5,6",
 "PBp.1": "SYMBOLIC in g at n=4: (n−2)·c_std(g) + 2·c_triv(g) ≡ 0 AND (n−2)·c_shape(g) + n·c_triv(g) ≡ 0 as exact rational-function identities (c_X = tr(Q_ν P_X)/tr(P_X)) — equivalently shadow(Q_ν) = s(g)·((n−2)I − A_1)",
 "PBp.1b": "same two identities SYMBOLIC at n=5",
 "PBp.2": "direction (−(n−2) : 2 : n) at NINE fresh g-fixtures (3 per n ∈ {4,5,6}), exact ℚ",
 "PBp.3": "scalar s(g) := −c_triv(g)/(n−2): (a) staked: s is a symmetric rational function of g, homogeneous of degree 6−2n; (b) measurement: record s(g) in factored form at n=4 (and n=5 if PBp.1b lands)",
 "PBp.4": "residual R(g) = Q_ν − s·Q_univ: record rank(R) and isotypic block support (P_X R P_Y norms²) at all 15 fixtures",
}

def sha256_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def gate_pins_and_clauses():
    pins = {}
    for line in open(HERE + '/freeze_pins_bprime.sha256'):
        h, path = line.split()
        pins[path] = h
    for path, h in pins.items():
        full = os.path.normpath(os.path.join(HERE, path))
        if sha256_file(full) != h:
            print("REFUSE_MISMATCH " + path); sys.exit(2)
    prereg = open(HERE + '/PREREG_BPRIME.md', encoding='utf-8').read()
    for cid, clause in GRADER_CLAUSES.items():
        if clause not in prereg:
            print("CLAUSE_DRIFT " + cid); sys.exit(3)
    return pins

# ---------- exact Fraction pipeline (as Stage B, W-prod only) ----------
def pairs_of(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]

def mat_mul(A, B):
    k, l = len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(l)]
            for i in range(len(A))]

def mat_tr(A):
    return sum(A[i][i] for i in range(len(A)))

def sym_from_offdiag(n, h):
    M = [[Fr(0)] * n for _ in range(n)]
    for idx, (i, j) in enumerate(pairs_of(n)):
        M[i][j] = M[j][i] = Fr(h[idx])
    return M

def tangent_P(g):
    n = len(g); q = sum(x * x for x in g)
    return [[(Fr(1) if i == j else Fr(0)) - Fr(g[i] * g[j], q)
             for j in range(n)] for i in range(n)], q

def e2_form_value(P, q, n, h):
    A = mat_mul(mat_mul(P, sym_from_offdiag(n, h)), P)
    return -q * ((mat_tr(A) ** 2 - mat_tr(mat_mul(A, A))) / 2)

def polarize_Q(P, q, n):
    N = n * (n - 1) // 2
    def f(v): return e2_form_value(P, q, n, v)
    diag = []
    for i in range(N):
        e = [Fr(0)] * N; e[i] = Fr(1); diag.append(f(e))
    Q = [[Fr(0)] * N for _ in range(N)]
    for i in range(N):
        Q[i][i] = diag[i]
        for j in range(i + 1, N):
            e = [Fr(0)] * N; e[i] = Fr(1); e[j] = Fr(1)
            Q[i][j] = Q[j][i] = (f(e) - diag[i] - diag[j]) / 2
    return Q

def w_prod(n, g):
    out = []
    for (i, j) in pairs_of(n):
        w = 1
        for k in range(n):
            if k not in (i, j): w *= g[k]
        out.append(Fr(w))
    return out

def q_nu(Q, W):
    N = len(W)
    return [[Q[i][j] / (W[i] * W[j]) for j in range(N)] for i in range(N)]

def pair_perm_matrix(n, p):
    prs = pairs_of(n); idx = {pr: k for k, pr in enumerate(prs)}
    N = len(prs)
    M = [[Fr(0)] * N for _ in range(N)]
    for k, (i, j) in enumerate(prs):
        a, b = p[i], p[j]
        M[idx[(min(a, b), max(a, b))]][k] = Fr(1)
    return M

def projectors(n):
    lams = [(n,), (n - 1, 1)] + ([(n - 2, 2)] if n >= 4 else [])
    Ps, N = [], n * (n - 1) // 2
    mats = [(p, pair_perm_matrix(n, p))
            for p in itertools.permutations(range(n))]
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
        inv = Fr(1) / M[r][c]; M[r] = [x * inv for x in M[r]]
        for i in range(n):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r

def gate_projectors(n, Ps):
    N = n * (n - 1) // 2
    assert tuple(mat_rank(P) for P in Ps) == (1, n - 1, n * (n - 3) // 2)
    for P in Ps: assert mat_mul(P, P) == P
    for a in range(3):
        for b in range(a + 1, 3):
            assert all(x == 0 for r_ in mat_mul(Ps[a], Ps[b]) for x in r_)
    I = [[Fr(int(i == j)) for j in range(N)] for i in range(N)]
    assert [[sum(P[i][j] for P in Ps) for j in range(N)]
            for i in range(N)] == I

def shadow(Qn, Ps):
    return [mat_tr(mat_mul(Qn, P)) / mat_tr(P) for P in Ps]

def johnson_A1(n):
    prs = pairs_of(n); N = len(prs)
    return [[Fr(1 if len(set(prs[i]) & set(prs[j])) == 1 else 0)
             for j in range(N)] for i in range(N)]

def q_univ(n):
    A1 = johnson_A1(n); N = len(A1)
    return [[(Fr(n - 2) if i == j else Fr(0)) - A1[i][j]
             for j in range(N)] for i in range(N)]

def numeric_cell(n, g, Ps):
    P, q = tangent_P(g)
    Qn = q_nu(polarize_Q(P, q, n), w_prod(n, g))
    cs = shadow(Qn, Ps)
    i1 = (n - 2) * cs[1] + 2 * cs[0]
    i2 = (n - 2) * cs[2] + n * cs[0]
    return Qn, cs, (i1 == 0 and i2 == 0 and cs[0] != 0)

def residual_row(n, g, Qn, cs, Ps, fid):
    s = -cs[0] / Fr(n - 2)
    QU = q_univ(n); N = len(QU)
    R = [[Qn[i][j] - s * QU[i][j] for j in range(N)] for i in range(N)]
    blocks = {}
    names = ('t', 's', 'sh')
    for a in range(3):
        for b in range(3):
            B = mat_mul(mat_mul(Ps[a], R), Ps[b])
            n2 = sum(x * x for row in B for x in row)
            blocks[names[a] + names[b]] = str(n2)
    return {"row": "PBp4", "fixture": fid, "n": n, "s": str(s),
            "rank_R": mat_rank(R), "block_norms2": blocks}

# ---------- symbolic path (probe): sympy over Q(g) ----------
def symbolic_block(n, Ps):
    import sympy as sp
    gs = sp.symbols('g0:%d' % n, positive=True)
    q = sum(x * x for x in gs)
    B = sp.Matrix([[q * (1 if i == j else 0) - gs[i] * gs[j]
                    for j in range(n)] for i in range(n)])
    prs = pairs_of(n); N = len(prs)
    def f_e2p(v):
        M = sp.zeros(n, n)
        for idx, (i, j) in enumerate(prs):
            if v[idx]:
                M[i, j] = M[j, i] = v[idx]
        A = B * M * B
        return sp.expand((A.trace() ** 2 - (A * A).trace()) / 2)
    diag = []
    for i in range(N):
        v = [0] * N; v[i] = 1; diag.append(f_e2p(v))
    Qp = [[None] * N for _ in range(N)]
    for i in range(N):
        Qp[i][i] = diag[i]
        for j in range(i + 1, N):
            v = [0] * N; v[i] = 1; v[j] = 1
            Qp[i][j] = Qp[j][i] = sp.expand((f_e2p(v) - diag[i] - diag[j]) / 2)
    W = []
    for (i, j) in prs:
        w = sp.Integer(1)
        for k in range(n):
            if k not in (i, j): w *= gs[k]
        W.append(w)
    S = []
    for P in Ps:
        tot = sp.Integer(0)
        for e in range(N):
            for f in range(N):
                if P[f][e] != 0 and Qp[e][f] != 0:
                    tot += sp.Rational(P[f][e].numerator,
                                       P[f][e].denominator) \
                           * Qp[e][f] / (W[e] * W[f])
        S.append(sp.together(tot))
    trs = [sp.Rational(mat_tr(P).numerator, mat_tr(P).denominator)
           for P in Ps]
    I1 = sp.cancel((n - 2) * S[1] / trs[1] + 2 * S[0] / trs[0])
    I2 = sp.cancel((n - 2) * S[2] / trs[2] + n * S[0] / trs[0])
    ok = (I1 == 0 and I2 == 0)
    # scalar s(g) = -c_triv/(n-2); c_triv = (-1/q^3) S_triv/tr ⟹
    s_expr = sp.cancel(S[0] / (q ** 3 * trs[0] * (n - 2)))
    t = sp.symbols('t', positive=True)
    hom = sp.cancel(s_expr.subs({gi: t * gi for gi in gs}) / s_expr)
    hom_ok = sp.simplify(hom - t ** (6 - 2 * n)) == 0
    swap = {gs[0]: gs[1], gs[1]: gs[0]}
    cyc = {gs[i]: gs[(i + 1) % n] for i in range(n)}
    sym_ok = (sp.cancel(s_expr.subs(swap, simultaneous=True) - s_expr) == 0
              and sp.cancel(s_expr.subs(cyc, simultaneous=True) - s_expr) == 0)
    return ok, hom_ok, sym_ok, str(sp.factor(s_expr))

def main():
    outp = sys.argv[1]
    gates_only = '--gates-only' in sys.argv
    pins = gate_pins_and_clauses()
    fxB = json.load(open(HERE + '/fixtures_stageB.json'))
    fxP = json.load(open(HERE + '/fixtures_bprime.json'))
    rows, led = [], {"role": "probe", "prereg": "PREREG_BPRIME.md",
                     "battery_sha256": sha256_file(os.path.abspath(__file__))}
    Pc = {n: projectors(n) for n in (4, 5, 6)}
    for n in (4, 5, 6): gate_projectors(n, Pc[n])
    # PBp.0 regression vs pinned Stage-B run-1 records (W-prod rows)
    rec = {}
    for line in open(HERE + '/records/stageB_records_run1.jsonl'):
        r = json.loads(line)
        if r.get('row') == 'PB1' and r['weight'] == 'W-prod':
            rec[r['fixture']] = r['c']
    reg_ok = True
    cellsB = {}
    for f in fxB['fixtures']:
        n, g = f['n'], f['g']
        Qn, cs, _ = numeric_cell(n, g, Pc[n])
        cellsB[f['id']] = (n, g, Qn, cs)
        if [str(c) for c in cs] != rec[f['id']]:
            reg_ok = False
    rows.append({"row": "PBp0", "regression_match": reg_ok,
                 "projector_gates": [4, 5, 6], "pass": reg_ok})
    assert reg_ok, "K-Bp0 regression mismatch"
    if gates_only:
        print("GATES_ONLY_OK"); return
    # PBp.2 numeric fresh fixtures (also referee data for PBp.1)
    fresh_ok, cellsP = True, {}
    for f in fxP['fresh_g']:
        n, g = f['n'], f['g']
        Qn, cs, ok = numeric_cell(n, g, Pc[n])
        cellsP[f['id']] = (n, g, Qn, cs)
        fresh_ok = fresh_ok and ok
        rows.append({"row": "PBp2", "fixture": f['id'], "n": n,
                     "direction_ok": ok, "c": [str(c) for c in cs]})
    # PBp.1 / PBp.1b symbolic + PBp.3 symbolic
    sym = {}
    for n in (4, 5):
        ok, hom_ok, sym_ok, s_fac = symbolic_block(n, Pc[n])
        sym[n] = {"identities": ok, "s_homog_6_minus_2n": hom_ok,
                  "s_symmetric": sym_ok, "s_factored": s_fac}
        rows.append({"row": "PBp1" if n == 4 else "PBp1b", "n": n,
                     "symbolic_identities": ok, "s_homogeneous": hom_ok,
                     "s_symmetric": sym_ok, "s_factored": s_fac})
    # referee agreement: symbolic zero must match numeric zero at fresh g's
    agree = (sym[4]["identities"] and fresh_ok) or \
            (not sym[4]["identities"] and not fresh_ok)
    rows.append({"row": "REFEREE", "symbolic_vs_numeric_agree": agree})
    # PBp.4 residual measurements at all 15 fixtures
    for fid in sorted(cellsB) + sorted(cellsP):
        src = cellsB if fid in cellsB else cellsP
        n, g, Qn, cs = src[fid]
        rows.append(residual_row(n, g, Qn, cs, Pc[n], fid))
    verdicts = {
        "PBp.0": {"pass": True},
        "PBp.1": {"pass": sym[4]["identities"]},
        "PBp.1b": {"pass": sym[5]["identities"]},
        "PBp.2": {"pass": fresh_ok},
        "PBp.3a": {"pass": sym[4]["s_homog_6_minus_2n"] and
                           sym[4]["s_symmetric"] and
                           sym[5]["s_homog_6_minus_2n"] and
                           sym[5]["s_symmetric"]},
        "referee_agree": agree,
    }
    rows.append({"row": "VERDICTS", "verdicts": verdicts, "ledger": led,
                 "pins": pins})
    with open(outp, 'w') as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(json.dumps(verdicts, sort_keys=True, indent=1))
    print("BPRIME_DONE")

main()
