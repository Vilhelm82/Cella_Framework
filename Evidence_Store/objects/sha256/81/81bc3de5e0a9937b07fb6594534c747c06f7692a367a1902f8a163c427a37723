#!/usr/bin/env python3
"""flagship_stageA_battery.py — SHAPE READOUT Stage A (quadratic layer).
Prereg: FLAGSHIP_STAGE_A_PREREG.md, pin d5e69a10fee4897d. role=probe.
FA.1 Molien a2; FA.2 FS indicators + trace Gram (CL-F1 certificates); FA.3/FA.4 conjugation
sweep (P-F2 sharp, sigma-tie per pair); FA.6 relabeling control; FA.5 P-F3 adaptive hunt.
Timings outside the blob. Exact Q on every verdict path.
"""
import sys, os, json, time, random
from fractions import Fraction as Fr
from itertools import combinations, permutations

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "portfolio", "campaigns", "the_engine", "stage_A"))
sys.path.insert(0, os.path.join(REPO, "evals", "dbp_involution"))
import engine_harness as EH
from rep_utils import specht_char_dict, specht_dim, cycle_type, partitions, class_rep, class_size
import sympy as sp

def hb(msg):
    import sys as _s; print("[hb]", msg, file=_s.stderr, flush=True)

def to_s(x):
    x = Fr(x); return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else f"{x.numerator}"

def det_frac(M):
    from math import lcm
    m = len(M); F = Fr(1); A = []
    for row in M:
        L = 1
        for x in row: L = lcm(L, Fr(x).denominator)
        F *= L
        A.append([int(Fr(x)*L) for x in row])
    sign, prev = 1, 1
    for k in range(m-1):
        if A[k][k] == 0:
            sw = next((r for r in range(k+1, m) if A[r][k] != 0), None)
            if sw is None: return Fr(0)
            A[k], A[sw] = A[sw], A[k]; sign = -sign
        for i in range(k+1, m):
            Aik = A[i][k]
            for j in range(k+1, m):
                A[i][j] = (A[i][j]*A[k][k] - Aik*A[k][j])//prev
            A[i][k] = 0
        prev = A[k][k]
    return Fr(sign*A[m-1][m-1], 1)/F


PREREG = os.path.join(HERE, "FLAGSHIP_STAGE_A_PREREG.md")
PIN = "d5e69a10fee4897d"
FA = {
 "FA.1": "FA.1: exact Molien on the pair module gives degree-2 invariant count a2 = 3 at n=5, n=6, and n=7.",
 "FA.2": "FA.2: Frobenius-Schur indicators equal +1 for lambda in {(n),(n-1,1),(n-2,2)} at n=5,6,7, and the trace Gram tr(P_X P_Y) = delta_XY * rank(P_X) holds exactly at n=5,6,7.",
 "FA.3": "FA.3: over the pinned conjugation sweep (seed 20260703, 40 pairs per n at n=5,6,7), every pair with delta_shape != 0 satisfies m2_shape(O1) != m2_shape(O2); a tie is recorded verbatim and routed as a mechanism-extraction lead, never silently widened.",
 "FA.4": "FA.4: on every sweep pair, Ehat_r(H1) = Ehat_r(H2) exactly for r=1..4 (the sigma-tie mechanism holds on the full sweep).",
 "FA.5": "FA.5: the P-F3 hunt follows the pinned adaptive protocol of section 5 and terminates in exactly one of WITNESS_FOUND, INCONCLUSIVE_BUDGET, or OBSTRUCTION_RECORDED; a found witness is certified by exact Ehat ties r=1..4, exact ties in all three m2's, O2 != O1, and pairwise-distinct g entries.",
 "FA.6": "FA.6: relabeling control \u2014 on one pinned pair per n, all Ehat_r and all three m2's are exactly invariant under the pinned relabeling pi_n.",
 "FA.7": "FA.7: witness_battery.py reproduces RECORDS_SHA256 39bed5552c805f4d via engine_harness certify on the primary substrate before Stage A is graded.",
}
PINS = {
 "portfolio/campaigns/shape_witness/BRIEF_v1_DRAFT.md": "3b3fca4292bc8aa7",
 "portfolio/campaigns/shape_witness/witness_battery.py": "abff00bd15d22c84",
 "portfolio/campaigns/shape_witness/WITNESS_PREDECL.md": "967c7909450ef944",
 "portfolio/campaigns/shape_witness/WALL_SCOUT_PREDECL.md": "b8d6c404131e7db7",
 "evals/dbp_involution/rep_utils.py": "0d838e5fd430461b",
 "portfolio/campaigns/the_engine/stage_A/engine_harness.py": "7f0e5e7e4f4d54a6",
 "portfolio/80_PROCESS_AMENDMENTS.md": "d03842f39c1e699b",
}

# ---------- shared exact machinery (witness pattern) ----------
def pairs_of(n): return list(combinations(range(n), 2))
def idx_of(P): return {p: k for k, p in enumerate(P)}

def pair_perm(p, PAIRS, IDX): return [IDX[tuple(sorted((p[i], p[j])))] for (i, j) in PAIRS]

def projectors(n, PAIRS, IDX):
    N = len(PAIRS); lams = [(n,), (n-1, 1), (n-2, 2)]
    chis = [specht_char_dict(l) for l in lams]; dims = [specht_dim(l) for l in lams]
    f = 1
    for k in range(2, n+1): f *= k
    Ps = [[[Fr(0)]*N for _ in range(N)] for _ in lams]
    for p in permutations(range(n)):
        ct = cycle_type(p); pi = pair_perm(p, PAIRS, IDX)
        cs = [Fr(dims[a]*int(chis[a][ct]), f) for a in range(3)]
        for k in range(N):
            d = pi[k]
            for a in range(3): Ps[a][d][k] += cs[a]
    return Ps

def matmul(A, B, n):
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def matT(A): return [list(r) for r in zip(*A)]

def frac_inv(M, n):
    A = [[Fr(M[i][j]) for j in range(n)] + [Fr(i == j) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]

def cayley(u, v, g, n):
    A = [[u[i]*v[j] - v[i]*u[j] for j in range(n)] for i in range(n)]
    I = [[Fr(i == j) for j in range(n)] for i in range(n)]
    ImA = [[I[i][j]-A[i][j] for j in range(n)] for i in range(n)]
    IpA = [[I[i][j]+A[i][j] for j in range(n)] for i in range(n)]
    R = matmul(ImA, frac_inv(IpA, n), n)
    RtR = matmul(matT(R), R, n)
    assert all(RtR[i][j] == Fr(i == j) for i in range(n) for j in range(n))
    assert all(sum(R[i][k]*g[k] for k in range(n)) == g[i] for i in range(n))
    return R

def O_of(H, g, PAIRS):
    return [H[i][j] - g[i]*H[j][j]/(2*g[j]) - g[j]*H[i][i]/(2*g[i]) for (i, j) in PAIRS]

def Ehat(H, g, n, r):
    tot = Fr(0)
    for I in combinations(range(n), r+1):
        M = [[Fr(0)]*(r+2) for _ in range(r+2)]
        for a, i in enumerate(I):
            M[0][a+1] = M[a+1][0] = Fr(g[i])
            for b, j in enumerate(I): M[a+1][b+1] = Fr(H[i][j])
        tot += det_frac(M)
    return (-1)**(r+1)*tot

def m2s(O, Ps, N):
    out = []
    for P in Ps:
        PO = [sum(P[i][k]*O[k] for k in range(N)) for i in range(N)]
        out.append(sum(PO[i]*O[i] for i in range(N)))
    return out  # [triv, std, shape]

def proj_vec(O, P, N): return [sum(P[i][k]*O[k] for k in range(N)) for i in range(N)]

# ---------- FA.1: Molien a2 ----------
def molien_a2(n, PAIRS, IDX):
    t = sp.symbols("t"); f = 1
    for k in range(2, n+1): f *= k
    tot = sp.Integer(0)
    for mu in partitions(n):
        pi = pair_perm(class_rep(mu, n), PAIRS, IDX)
        seen, den = [False]*len(pi), sp.Integer(1)
        for s in range(len(pi)):
            if not seen[s]:
                L, c = 0, s
                while not seen[c]: seen[c] = True; c = pi[c]; L += 1
                den *= (1 - t**L)
        tot += sp.Rational(class_size(mu, n))/den
    ser = sp.series(tot/f, t, 0, 3).removeO().expand()
    return int(ser.coeff(t, 2))

# ---------- FA.2: FS indicators + trace Gram ----------
def fs_and_gram(n, Ps):
    f = 1
    for k in range(2, n+1): f *= k
    lams = [(n,), (n-1, 1), (n-2, 2)]
    chis = [specht_char_dict(l) for l in lams]
    fs = []
    for chi in chis:
        s = 0
        for p in permutations(range(n)):
            q = tuple(p[p[i]] for i in range(len(p)))
            s += int(chi[cycle_type(q)])
        fs.append(Fr(s, f))
    N = len(Ps[0]); gram, ranks = [], [1, n-1, n*(n-3)//2]
    ok = True
    for a in range(3):
        row = []
        for b in range(3):
            tr = sum(sum(Ps[a][i][k]*Ps[b][k][i] for k in range(N)) for i in range(N))
            row.append(tr)
            ok = ok and (tr == (Fr(ranks[a]) if a == b else Fr(0)))
        gram.append([str(x) for x in row])
    return [str(x) for x in fs], gram, ok and all(x == Fr(1) for x in fs)

# ---------- FA.3/FA.4: sweep ----------
POOL = [Fr(k) for k in range(1, 24)] + [Fr(3,2), Fr(5,2), Fr(7,2), Fr(9,2), Fr(11,2)]
def rand_perp(rng, g, n):
    while True:
        u = [Fr(rng.randint(-3, 3)) for _ in range(n)]
        gg = sum(x*x for x in g); ug = sum(a*b for a, b in zip(u, g))
        u = [a - ug*b/gg for a, b in zip(u, g)]
        if any(x != 0 for x in u): return u

def draw_pair_sample(rng, g_n, PAIRS, n):
    g = rng.sample(POOL, n)
    offd = [Fr(rng.choice([x for x in range(-5, 6) if x != 0]), rng.choice([1, 2, 3])) for _ in PAIRS]
    diag = [Fr(rng.choice([x for x in range(-5, 6) if x != 0]), rng.choice([1, 2, 3])) for _ in range(n)]
    vecs = [rand_perp(rng, g, n) for _ in range(4)]
    return {"g": g, "offd": offd, "diag": diag, "vecs": vecs, "n": n}

_G = {}
def _init_pool(Ps_by_n, pairs_by_n):
    _G["P"], _G["PR"] = Ps_by_n, pairs_by_n

def sweep_worker(task):
    n, g, offd, diag, vecs = task["n"], task["g"], task["offd"], task["diag"], task["vecs"]
    Ps = _G["P"][n]; PAIRS = _G["PR"][n][0]; N = len(PAIRS)
    H1 = [[Fr(0)]*n for _ in range(n)]
    for (i, j), v in zip(PAIRS, offd): H1[i][j] = H1[j][i] = v
    for i in range(n): H1[i][i] = diag[i]
    A = matmul(cayley(vecs[0], vecs[1], g, n), cayley(vecs[2], vecs[3], g, n), n)
    H2 = matmul(matT(A), matmul(H1, A, n), n)
    O1, O2 = O_of(H1, g, PAIRS), O_of(H2, g, PAIRS)
    etie = all(Ehat(H1, g, n, r) == Ehat(H2, g, n, r) for r in (1, 2, 3, 4))
    d = [a-b for a, b in zip(proj_vec(O1, Ps[2], N), proj_vec(O2, Ps[2], N))]
    dz = all(x == 0 for x in d)
    m1, m2_ = m2s(O1, Ps, N), m2s(O2, Ps, N)
    return {"etie": etie, "delta_shape_zero": dz, "m2_shape_tie": m1[2] == m2_[2],
            "m2_triv_tie": m1[0] == m2_[0], "m2_std_tie": m1[1] == m2_[1]}

def grade_sweep(recs):
    sep = all((r["delta_shape_zero"] or not r["m2_shape_tie"]) for r in recs)
    return {"pairs": len(recs), "all_sigma_tied": all(r["etie"] for r in recs),
            "nonzero_delta": sum(0 if r["delta_shape_zero"] else 1 for r in recs),
            "FA3_separation": sep,
            "ties_on_nonzero_delta": [i for i, r in enumerate(recs) if (not r["delta_shape_zero"]) and r["m2_shape_tie"]],
            "auto_tie_rate_triv": sum(1 for r in recs if r["m2_triv_tie"]),
            "auto_tie_rate_std": sum(1 for r in recs if r["m2_std_tie"])}

# ---------- FA.6: relabeling control ----------
def relabel_control(n, Ps, PAIRS, IDX, rng):
    N = len(PAIRS)
    g = rng.sample(POOL, n)
    H = [[Fr(0)]*n for _ in range(n)]
    for (i, j) in PAIRS: H[i][j] = H[j][i] = Fr(rng.choice([x for x in range(-5, 6) if x != 0]), rng.choice([1, 2, 3]))
    for i in range(n): H[i][i] = Fr(rng.choice([x for x in range(-5, 6) if x != 0]), rng.choice([1, 2, 3]))
    pi = tuple(list(range(1, n)) + [0])  # pinned n-cycle
    gp = [g[pi[i]] for i in range(n)]
    Hp = [[H[pi[i]][pi[j]] for j in range(n)] for i in range(n)]
    ok = all(Ehat(H, g, n, r) == Ehat(Hp, gp, n, r) for r in (1, 2, 3, 4))
    ok = ok and (m2s(O_of(H, g, PAIRS), Ps, N) == m2s(O_of(Hp, gp, PAIRS), Ps, N))
    return bool(ok)

# ---------- FA.5: the hunt ----------
SLATES = [  # 8 pinned integer slates (u1, v1, u2, v2, e) pre-projection
 ((1,0,-1,2,0),(0,1,1,-1,1),(2,-1,0,1,-1),(1,1,-2,0,1),(0,2,-1,-1,1)),
 ((2,1,0,-1,1),(1,-1,2,0,-2),(0,1,-1,1,2),(2,0,1,-2,0),(1,-2,0,1,1)),
 ((1,2,-2,0,1),(0,-1,1,2,-1),(1,0,2,-1,-2),(0,2,1,1,-1),(2,-1,1,0,-2)),
 ((0,1,2,-1,-2),(2,0,-1,1,1),(1,-2,1,0,2),(0,1,-1,2,-1),(1,1,0,-2,2)),
 ((2,-1,1,-1,0),(1,1,-2,1,-1),(0,2,1,-2,1),(1,0,-1,1,2),(2,1,-1,0,-1)),
 ((1,-1,0,2,-2),(0,2,-1,-1,1),(2,1,1,0,-1),(1,-1,2,-2,0),(0,1,1,1,-2)),
 ((0,2,-2,1,0),(1,0,1,-1,2),(1,2,0,-2,1),(2,-1,-1,1,0),(1,0,2,0,-1)),
 ((2,0,-1,2,-1),(0,1,2,-2,1),(1,1,-1,0,-2),(0,-2,1,1,1),(2,2,0,-1,-1)),
]

def dotf(a, b): return sum(x*y for x, y in zip(a, b))

def interp_1d(xs, ys):
    # exact Lagrange -> coefficient list (Fractions), ascending degree
    m = len(xs); coef = [Fr(0)]*m
    for i in range(m):
        # basis poly prod_{j!=i} (x - xj)/(xi - xj), accumulate ys[i]*basis
        num = [Fr(1)]; den = Fr(1)
        for j in range(m):
            if j == i: continue
            num = [ (num[k-1] if k > 0 else Fr(0)) - xs[j]*(num[k] if k < len(num) else Fr(0)) for k in range(len(num)+1) ]
            den *= (xs[i]-xs[j])
        w = ys[i]/den
        for k in range(len(num)): coef[k] += w*num[k]
    while len(coef) > 1 and coef[-1] == 0: coef.pop()
    return coef

ELIM_SRC = r"""
import sys, json
from fractions import Fraction as Fr
import sympy as sp
t1, t2, t3 = sp.symbols('t1 t2 t3')
data = json.load(sys.stdin)
polys = []
for d in data['polys']:
    e = sp.Integer(0)
    for mono, c in d.items():
        i, j, k = map(int, mono.split(','))
        e += sp.Rational(c) * t1**i * t2**j * t3**k
    polys.append(sp.expand(e))
sols = []
try:
    G = sp.groebner(polys, t1, t2, t3, order='lex', domain='QQ')
    uni = [g for g in G.exprs if g.free_symbols <= {t3}]
    cand3 = set()
    for u in uni:
        cand3 |= set(sp.roots(sp.Poly(u, t3), filter='Q').keys())
    for a3 in cand3:
        two = [sp.expand(p.subs(t3, a3)) for p in polys]
        r = sp.resultant(two[0], two[2], t2) if not two[0].free_symbols <= {t1} else two[0]
        c1 = set(sp.roots(sp.Poly(r, t1), filter='Q').keys()) if r.free_symbols else set()
        if not c1:
            r2 = sp.resultant(two[1], two[2], t2)
            c1 = set(sp.roots(sp.Poly(r2, t1), filter='Q').keys()) if r2.free_symbols else set()
        for a1 in c1:
            one = [sp.expand(p.subs({t3: a3, t1: a1})) for p in two]
            g2 = sp.gcd(sp.Poly(one[0], t2), sp.gcd(sp.Poly(one[1], t2), sp.Poly(one[2], t2)))
            for a2 in sp.roots(g2, filter='Q'):
                if all(p.subs({t1: a1, t2: a2, t3: a3}) == 0 for p in polys):
                    sols.append([str(a1), str(a2), str(a3)])
except Exception as ex:
    print(json.dumps({'error': str(ex)[:150]})); sys.exit(0)
print(json.dumps({'sols': sols}))
"""

def hunt_slice(args):
    si, branch_u, Ps5, PAIRS5 = args
    import time as _t
    n, N = 5, 10
    g = [Fr(x) for x in (1, 2, 3, 5, 7)]
    H = [[Fr(0)]*n for _ in range(n)]
    offd = [Fr(x) for x in (1, -2, 3, 1, 2, -1, 4, -3, 1, 2)]
    for (i, j), v in zip(PAIRS5, offd): H[i][j] = H[j][i] = v
    O1 = O_of(H, g, PAIRS5); m_t = m2s(O1, Ps5, N)
    E1 = [Ehat(H, g, n, r) for r in (1, 2, 3, 4)]
    t = sp.symbols("t"); gg = sum(x*x for x in g)
    def perp(w):
        wg = sum(sp.Rational(a)*b for a, b in zip(w, g)); return [sp.Rational(a) - wg*sp.Rational(b)/gg for a, b in zip(w, g)]
    def cay_sym(u, v):
        Aa = sp.Matrix(n, n, lambda i, j: u[i]*v[j]-v[i]*u[j])
        return (sp.eye(n)-Aa)*(sp.eye(n)+Aa).inv()
    def to_fr(x):
        xr = sp.Rational(sp.nsimplify(x)); return Fr(int(xr.p), int(xr.q))
    def certify_at(H2s, sm):
        H2 = [[to_fr(H2s[i, j].subs(sm)) for j in range(n)] for i in range(n)]
        O2 = O_of(H2, g, PAIRS5); mm = m2s(O2, Ps5, N)
        E2 = [Ehat(H2, g, n, r) for r in (1, 2, 3, 4)]
        return ((mm == m_t) and (E2 == E1) and (O2 != O1)), O2, mm, E2
    def m2_sym(O2s, P):
        PO = [sum(sp.Rational(P[i][k])*O2s[k] for k in range(N)) for i in range(N)]
        return sum(PO[i]*O2s[i] for i in range(N))
    def O_sym(H2s):
        gs = [sp.Rational(x) for x in g]
        return [H2s[i, j] - gs[i]*H2s[j, j]/(2*gs[j]) - gs[j]*H2s[i, i]/(2*gs[i]) for (i, j) in PAIRS5]
    Hs = sp.Matrix(n, n, lambda i, j: sp.Rational(H[i][j]))
    u1, v1, u2, v2, e = SLATES[si]
    t0 = _t.time(); trace = []
    try:
        if branch_u:
            U1 = [a + t*b for a, b in zip(perp(u1), perp(e))]
            R = cay_sym(U1, perp(v1))*cay_sym(perp(u2), perp(v2))
            H2s = R.T*Hs*R
            f = sp.together(m2_sym(O_sym(H2s), Ps5[2]) - sp.Rational(m_t[2]))
            roots = [r for r in sp.roots(sp.Poly(sp.numer(f), t), filter="Q") if r != 0]
            for r0 in roots:
                cert, O2, mm, E2 = certify_at(H2s, {t: r0})
                trace.append({"root": str(r0), "certified": bool(cert)})
                if cert:
                    return {"slice": si, "witness": {"branch": "U", "t": str(r0),
                            "g": [to_s(x) for x in g], "H1_offd": [to_s(x) for x in offd],
                            "O2": [to_s(x) for x in O2], "m2_tied": [to_s(x) for x in mm],
                            "Ehat_tied": [to_s(x) for x in E2]}, "trace": trace}
            trace.append({"branch": "U", "roots": len(roots)})
        else:
            import subprocess, json as _json
            pu1, pv1, pu2, pv2, pe = ([Fr(x.p, x.q) for x in perp(w)] for w in (u1, v1, u2, v2, e))
            def evalpt(a1, a2, a3):
                U1 = [x + a1*y for x, y in zip(pu1, pe)]
                U2 = [x + a2*y + a3*z for x, y, z in zip(pu2, pe, pv1)]
                A = matmul(cayley(U1, pv1, g, n), cayley(U2, pv2, g, n), n)
                H2 = matmul(matT(A), matmul(H, A, n), n)
                return H2, m2s(O_of(H2, g, PAIRS5), Ps5, N)
            def D1f(a1):
                U1 = [x + a1*y for x, y in zip(pu1, pe)]
                return 1 + dotf(U1, U1)*dotf(pv1, pv1) - dotf(U1, pv1)**2
            def D2f(a2, a3):
                U2 = [x + a2*y + a3*z for x, y, z in zip(pu2, pe, pv1)]
                return 1 + dotf(U2, U2)*dotf(pv2, pv2) - dotf(U2, pv2)**2
            # G0: free coordinate-line and diagonal pre-hunts (univariate, cheap)
            def line_hunt(paramize, tag):
                K = 6; xs = [Fr(k) for k in range(-(2*K), 2*K+1)]
                ys = [[], [], []]
                for x in xs:
                    a = paramize(x); _, mm = evalpt(*a)
                    w = D1f(a[0])**K * D2f(a[1], a[2])**K
                    for X in range(3): ys[X].append((mm[X]-m_t[X])*w)
                roots = None
                for X in range(3):
                    co = interp_1d(xs, ys[X])
                    p = sp.Poly([sp.Rational(c.numerator, c.denominator) for c in reversed(co)], sp.symbols("s"))
                    rs = set(r for r in sp.roots(p, filter="Q") if r != 0)
                    roots = rs if roots is None else (roots & rs)
                    if not roots: return []
                out = []
                for r0 in roots:
                    a = paramize(Fr(int(sp.numer(r0)), int(sp.denom(r0))))
                    H2, mm = evalpt(*a)
                    if mm == m_t:
                        O2 = O_of(H2, g, PAIRS5); E2 = [Ehat(H2, g, n, r) for r in (1, 2, 3, 4)]
                        if E2 == E1 and O2 != O1:
                            out.append((a, H2, O2, mm, E2, tag))
                return out
            for tag, pz in (("a1_axis", lambda s: (s, Fr(0), Fr(0))), ("a2_axis", lambda s: (Fr(0), s, Fr(0))),
                            ("a3_axis", lambda s: (Fr(0), Fr(0), s)), ("diagonal", lambda s: (s, s, s))):
                for (a, H2, O2, mm, E2, tg) in line_hunt(pz, tag):
                    trace.append({"line_hit": tg, "a": [to_s(x) for x in a]})
                    return {"slice": si, "witness": {"branch": "G0-"+tg, "t": [to_s(x) for x in a],
                            "g": [to_s(x) for x in g], "H1_offd": [to_s(x) for x in offd],
                            "O2": [to_s(x) for x in O2], "m2_tied": [to_s(x) for x in mm],
                            "Ehat_tied": [to_s(x) for x in E2]}, "trace": trace}
            hb(f"slice {si}: G0 lines empty {round(_t.time()-t0,1)}s")
            if _t.time()-t0 > 600: return {"slice": si, "aborted_600s": "G0", "trace": trace}
            # G1: trivariate interpolation on tensor grid, self-checked, then capped elimination
            K, D = 6, 15
            xs = [Fr(k) for k in range(-(D//2), D - D//2)]
            grid = {}
            for a1 in xs:
                for a2 in xs:
                    for a3 in xs:
                        _, mm = evalpt(a1, a2, a3)
                        w = D1f(a1)**K * D2f(a2, a3)**K
                        grid[(a1, a2, a3)] = [(mm[X]-m_t[X])*w for X in range(3)]
                if _t.time()-t0 > 550: return {"slice": si, "aborted_600s": "G1-grid", "trace": trace}
            hb(f"slice {si}: grid {D}^3 done {round(_t.time()-t0,1)}s")
            polys = []
            for X in range(3):
                c3 = {}
                for a1 in xs:
                    for a2 in xs:
                        co = interp_1d(xs, [grid[(a1, a2, a3)][X] for a3 in xs])
                        for k3, c in enumerate(co): c3.setdefault(k3, {})[(a1, a2)] = c
                cdict = {}
                for k3, tbl in c3.items():
                    c2 = {}
                    for a1 in xs:
                        co = interp_1d(xs, [tbl.get((a1, a2), Fr(0)) for a2 in xs])
                        for k2, c in enumerate(co): c2.setdefault(k2, {})[a1] = c
                    for k2, tb1 in c2.items():
                        co = interp_1d(xs, [tb1.get(a1, Fr(0)) for a1 in xs])
                        for k1, c in enumerate(co):
                            if c != 0: cdict[(k1, k2, k3)] = c
                # self-check at 3 fresh rational points
                import random as _r; rr = _r.Random(1000+si)
                for _ in range(3):
                    p = tuple(Fr(rr.randint(8, 12), rr.choice([1, 3])) for _ in range(3))
                    _, mm = evalpt(*p)
                    direct = (mm[X]-m_t[X])*D1f(p[0])**K*D2f(p[1], p[2])**K
                    val = sum(c*p[0]**i*p[1]**j*p[2]**k for (i, j, k), c in cdict.items())
                    if val != direct: raise RuntimeError(f"interp self-check failed X={X}")
                polys.append({f"{i},{j},{k}": f"{c.numerator}/{c.denominator}" for (i, j, k), c in cdict.items()})
            hb(f"slice {si}: interp+selfcheck done {round(_t.time()-t0,1)}s")
            budget = max(30, int(600-(_t.time()-t0)))
            try:
                pr = subprocess.run([sys.executable, "-c", ELIM_SRC], input=_json.dumps({"polys": polys}),
                                    capture_output=True, text=True, timeout=budget)
                res = _json.loads(pr.stdout.strip() or "{}")
            except subprocess.TimeoutExpired:
                return {"slice": si, "aborted_600s": "elimination", "trace": trace}
            if "error" in res: trace.append({"elim_error": res["error"]})
            for a1s, a2s, a3s in res.get("sols", []):
                a = tuple(Fr(x) for x in (a1s, a2s, a3s))
                if a == (0, 0, 0): continue
                H2, mm = evalpt(*a)
                if mm != m_t: continue
                O2 = O_of(H2, g, PAIRS5); E2 = [Ehat(H2, g, n, r) for r in (1, 2, 3, 4)]
                cert = (E2 == E1) and (O2 != O1)
                trace.append({"sol": [a1s, a2s, a3s], "certified": bool(cert)})
                if cert:
                    return {"slice": si, "witness": {"branch": "G1", "t": [a1s, a2s, a3s],
                            "g": [to_s(x) for x in g], "H1_offd": [to_s(x) for x in offd],
                            "O2": [to_s(x) for x in O2], "m2_tied": [to_s(x) for x in mm],
                            "Ehat_tied": [to_s(x) for x in E2]}, "trace": trace}
            trace.append({"branch": "G1", "sols": len(res.get("sols", [])), "wall_s": round(_t.time()-t0, 1)})
    except Exception as ex:
        trace.append({"error": str(ex)[:120]})
    return {"slice": si, "done_s": round(_t.time()-t0, 1), "trace": trace}

def hunt(Ps5, PAIRS5, IDX5, branch_u, pool=None):
    args = [(si, branch_u, Ps5, PAIRS5) for si in range(len(SLATES))]
    results = pool.map(hunt_slice, args) if pool else [hunt_slice(a) for a in args]
    results.sort(key=lambda r: r["slice"])
    for r in results:
        if "witness" in r:
            return {"outcome": "WITNESS_FOUND", **r["witness"], "slice": r["slice"],
                    "trace": [x for rr in results for x in rr.get("trace", [])]}
    return {"outcome": "INCONCLUSIVE_BUDGET", "branch_u": branch_u,
            "trace": [{"slice": rr["slice"], **({k: v for k, v in rr.items() if k not in ("slice", "trace")})} for rr in results]}

def main():
    import multiprocessing as mp, os as _os
    EH.clause_gate(PREREG, FA, PIN); EH.pin_gate(PINS)
    print("GATES_GREEN prereg_pin", PIN, "content_pins", len(PINS))
    cores = _os.cpu_count() or 1
    hb(f"cores={cores}")
    blob, tm = {}, {}
    rng = random.Random(20260703)
    P_by_n, PR_by_n = {}, {}
    for n in (5, 6, 7):
        PAIRS = pairs_of(n); IDX = idx_of(PAIRS)
        t0 = time.perf_counter(); Ps = projectors(n, PAIRS, IDX)
        P_by_n[n], PR_by_n[n] = Ps, (PAIRS, IDX)
        a2 = molien_a2(n, PAIRS, IDX)
        fs, gram, fa2ok = fs_and_gram(n, Ps)
        blob[f"n{n}"] = {"a2": a2, "fs_indicators": fs, "trace_gram": gram, "fa2_ok": fa2ok}
        tm[f"n{n}_cert"] = round(time.perf_counter()-t0, 2)
        hb(f"n{n} certificates done {tm[f'n{n}_cert']}s a2={a2}")
    # pre-draw ALL sweep + relabel randomness in pinned order (seed 20260703, one stream)
    tasks, relabel_samples = [], {}
    for n in (5, 6, 7):
        PAIRS, IDX = PR_by_n[n]
        for k in range(40):
            tasks.append(draw_pair_sample(rng, None, PAIRS, n))
        g = rng.sample(POOL, n)
        offd = [Fr(rng.choice([x for x in range(-5, 6) if x != 0]), rng.choice([1, 2, 3])) for _ in PAIRS]
        diag = [Fr(rng.choice([x for x in range(-5, 6) if x != 0]), rng.choice([1, 2, 3])) for _ in range(n)]
        relabel_samples[n] = (g, offd, diag)
    pool = mp.Pool(min(cores, 14), initializer=_init_pool, initargs=(P_by_n, PR_by_n)) if cores > 1 else None
    if pool is None: _init_pool(P_by_n, PR_by_n)
    t0 = time.perf_counter()
    recs = pool.map(sweep_worker, tasks, chunksize=4) if pool else [sweep_worker(x) for x in tasks]
    tm["sweep_all"] = round(time.perf_counter()-t0, 2)
    hb(f"sweep 120 pairs done {tm['sweep_all']}s")
    for a, n in enumerate((5, 6, 7)):
        blob[f"n{n}"]["sweep"] = grade_sweep(recs[a*40:(a+1)*40])
    # FA.6 relabeling control per n (deterministic pinned samples)
    for n in (5, 6, 7):
        PAIRS, IDX = PR_by_n[n]; N = len(PAIRS); Ps = P_by_n[n]
        g, offd, diag = relabel_samples[n]
        H = [[Fr(0)]*n for _ in range(n)]
        for (i, j), v in zip(PAIRS, offd): H[i][j] = H[j][i] = v
        for i in range(n): H[i][i] = diag[i]
        pi = tuple(list(range(1, n)) + [0])
        gp = [g[pi[i]] for i in range(n)]
        Hp = [[H[pi[i]][pi[j]] for j in range(n)] for i in range(n)]
        ok = all(Ehat(H, g, n, r) == Ehat(Hp, gp, n, r) for r in (1, 2, 3, 4))
        ok = ok and (m2s(O_of(H, g, PAIRS), Ps, N) == m2s(O_of(Hp, gp, PAIRS), Ps, N))
        blob[f"n{n}"]["relabel_control"] = bool(ok)
    s5 = blob["n5"]["sweep"]
    branch_u = (s5["auto_tie_rate_triv"] == s5["pairs"] and s5["auto_tie_rate_std"] == s5["pairs"])
    blob["hunt_branch"] = "U" if branch_u else "G"
    hb(f"hunt branch {blob['hunt_branch']} (auto-tie triv {s5['auto_tie_rate_triv']}/40 std {s5['auto_tie_rate_std']}/40)")
    t0 = time.perf_counter()
    PAIRS5, IDX5 = PR_by_n[5]
    blob["hunt"] = hunt(P_by_n[5], PAIRS5, IDX5, branch_u, pool=pool)
    tm["hunt"] = round(time.perf_counter()-t0, 2)
    hb(f"hunt done {tm['hunt']}s outcome {blob['hunt']['outcome']}")
    if pool: pool.close(); pool.join()
    out = json.dumps(blob, sort_keys=True, indent=1)
    print(out)
    print("RECORDS_SHA256", EH.records_sha(out))
    print("TIMINGS_JSON", json.dumps(tm, sort_keys=True))
    print("STAGE_A_COMPLETE")

if __name__ == "__main__":
    main()
