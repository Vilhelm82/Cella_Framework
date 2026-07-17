#!/usr/bin/env python3
"""t4_probe.py — T4 number-field probe. Predecl pin 38e823f5234dd5cc.
Extract algebraic points on slice-0/1 tie curves (plane t3=1), certify ties in Q[theta]/(m),
compute group-Jacobian kernel at each point. role=probe. Exact throughout.
"""
import sys, os, json, time, subprocess, hashlib
from fractions import Fraction as Fr
from math import lcm

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "portfolio", "campaigns", "the_engine", "stage_A"))
sys.path.insert(0, os.path.join(REPO, "evals", "dbp_involution"))
import engine_harness as EH
import hunt_v2_msolve as R
import sympy as sp

B = R.B
PREDECL = os.path.join(HERE, "T4_PROBE_PREDECL.md")
PIN = "e45bdde953f3a47e"
T4 = {
 "T4.1": "T4.1: for slices 0 and 1, the probe extracts an algebraic point on the tie curve via the pinned plane t3 = 1, certifies the actual ties (m2 triple and Ehat r=1..4) exactly in Q[theta]/(m), and verifies O2 != O1 in the field.",
 "T4.2": "T4.2: the probe computes the rank over the field of the 3x6 group-Jacobian dm2 = 2<P_X O2, O_of([H2,B])> across the six stabilizer basis directions at each certified point, and banks kernel = 6 - rank.",
 "T4.3": "T4.3: verdicts follow the frozen semantics: kernel 3 anywhere refutes T4 at that point; kernel >= 4 at both points yields T4 STRUCTURAL; any P2 failure is PIPELINE_DEFECT and halts; mixed outcomes are banked verbatim without promotion.",
}
PINS = {
 "portfolio/campaigns/shape_witness/hunt_v2_msolve.py": "520298bbd6534fb3",
 "portfolio/campaigns/shape_witness/flagship_stageA_battery.py": "81bc3de5e0a9937b",
 "portfolio/campaigns/shape_witness/HUNT_ADDENDUM_v2_3.md": "15f4ab251ce34645",
 "portfolio/campaigns/the_engine/stage_A/engine_harness.py": "7f0e5e7e4f4d54a6",
 "evals/dbp_involution/rep_utils.py": "0d838e5fd430461b",
}

def hb(m): print("[hb]", m, file=sys.stderr, flush=True)

# ---------------- number field F = Q[x]/(m), m monic irreducible ----------------
class NF:
    deg = None; red = None  # reduction table: x^(deg+k) as coeff vectors
    @classmethod
    def setup(cls, mco):  # mco: monic coeffs ascending, len deg+1
        cls.deg = len(mco) - 1
        cls.m = [Fr(c) for c in mco]
        cls.red = []
        cur = [-c for c in cls.m[:-1]]  # x^deg = cur
        cls.red.append(cur[:])
        for _ in range(cls.deg - 2):
            cur = [Fr(0)] + cur
            hi = cur.pop()  # coefficient of x^deg
            cur = [c + hi * r for c, r in zip(cur, cls.red[0])]
            cls.red.append(cur[:])
    def __init__(self, co):
        d = NF.deg
        co = list(co)
        if len(co) < d:
            co = co + [Fr(0)] * (d - len(co))
        self.c = co if len(co) == d else NF._reduce(co)
    @staticmethod
    def _reduce(co):
        d = NF.deg
        co = list(co)
        while len(co) > d:
            hi = co.pop()
            if hi != 0:
                r = NF.red[len(co) - d]
                for i in range(d):
                    co[i] += hi * r[i]
        return co + [Fr(0)] * (d - len(co))
    @staticmethod
    def const(q): return NF([Fr(q)])
    def __add__(s, o): return NF([a + b for a, b in zip(s.c, o.c)])
    def __sub__(s, o): return NF([a - b for a, b in zip(s.c, o.c)])
    def __neg__(s): return NF([-a for a in s.c])
    def __mul__(s, o):
        d = NF.deg
        out = [Fr(0)] * (2 * d - 1)
        for i, a in enumerate(s.c):
            if a == 0: continue
            for j, b in enumerate(o.c):
                if b != 0: out[i + j] += a * b
        return NF(NF._reduce(out))
    def is_zero(s): return all(x == 0 for x in s.c)
    def __eq__(s, o): return all(a == b for a, b in zip(s.c, o.c))
    def inv(s):
        # extended Euclid in Q[x]: a*s + b*m = 1
        a = s.c[:]; m = NF.m[:]
        r0, r1 = m, a + [Fr(0)]
        s0, s1 = [Fr(0)], [Fr(1)]
        def deg(p):
            k = len(p) - 1
            while k >= 0 and p[k] == 0: k -= 1
            return k
        def sub_scaled(p, q, c, sh):
            p = p[:] + [Fr(0)] * max(0, len(q) + sh - len(p))
            for i, x in enumerate(q):
                p[i + sh] -= c * x
            return p
        while deg(r1) > 0:
            while deg(r0) >= deg(r1):
                d0, d1 = deg(r0), deg(r1)
                c = r0[d0] / r1[d1]
                r0 = sub_scaled(r0, r1, c, d0 - d1)
                s0 = sub_scaled(s0, s1, c, d0 - d1)
            r0, r1, s0, s1 = r1, r0, s1, s0
        if deg(r1) != 0: raise ZeroDivisionError("non-invertible (m reducible?)")
        u = r1[deg(r1)]
        return NF([x / u for x in s1])
    def __truediv__(s, o): return s * o.inv()

def nf_mat(rows): return [[x for x in r] for r in rows]
def nf_matmul(A, Bm, n):
    return [[sum((A[i][k] * Bm[k][j] for k in range(n)), NF.const(0)) for j in range(n)] for i in range(n)]
def nf_T(A): return [list(r) for r in zip(*A)]
def nf_inv(M, n):
    A = [[M[i][j] for j in range(n)] + [NF.const(i == j) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if not A[r][c].is_zero())
        A[c], A[p] = A[p], A[c]
        piv = A[c][c].inv()
        A[c] = [x * piv for x in A[c]]
        for r in range(n):
            if r != c and not A[r][c].is_zero():
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]
def nf_det(M, n):
    A = [row[:] for row in M]; det = NF.const(1)
    for c in range(n):
        p = next((r for r in range(c, n) if not A[r][c].is_zero()), None)
        if p is None: return NF.const(0)
        if p != c: A[c], A[p] = A[p], A[c]; det = -det
        det = det * A[c][c]
        piv = A[c][c].inv()
        for r in range(c + 1, n):
            if not A[r][c].is_zero():
                f = A[r][c] * piv
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return det
def nf_rank(M, rows, cols):
    A = [r[:] for r in M]; rk = 0
    for c in range(cols):
        p = next((r for r in range(rk, rows) if not A[r][c].is_zero()), None)
        if p is None: continue
        A[rk], A[p] = A[p], A[rk]
        piv = A[rk][c].inv()
        A[rk] = [x * piv for x in A[rk]]
        for r in range(rows):
            if r != rk and not A[r][c].is_zero():
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[rk])]
        rk += 1
        if rk == rows: break
    return rk

# ---------------- saturation (per HUNT v2.1/2.2, replicated) ----------------
def saturated_polys(si):
    polys = R.build_polys(si)[0]
    t1s, t2s, t3s = sp.symbols("t1 t2 t3")
    sl = B.SLATES[si]
    pu2 = [sp.Rational(x.numerator, x.denominator) for x in R.perp(sl[2])]
    pe_ = [sp.Rational(x.numerator, x.denominator) for x in R.perp(sl[4])]
    pv1_ = [sp.Rational(x.numerator, x.denominator) for x in R.perp(sl[1])]
    pv2_ = [sp.Rational(x.numerator, x.denominator) for x in R.perp(sl[3])]
    pu1 = [sp.Rational(x.numerator, x.denominator) for x in R.perp(sl[0])]
    U1 = [a + t1s * b for a, b in zip(pu1, pe_)]
    D1p = sp.Poly(sp.expand(1 + sum(x * x for x in U1) * sum(y * y for y in pv1_) - sum(x * y for x, y in zip(U1, pv1_)) ** 2), t1s, t2s, t3s)
    U2 = [a + t2s * b + t3s * c for a, b, c in zip(pu2, pe_, pv1_)]
    D2p = sp.Poly(sp.expand(1 + sum(x * x for x in U2) * sum(y * y for y in pv2_) - sum(x * y for x, y in zip(U2, pv2_)) ** 2), t1s, t2s, t3s)
    sat = []
    for cd in polys:
        P = sp.Poly(sum(sp.Rational(c.numerator, c.denominator) * t1s ** i * t2s ** j * t3s ** k for (i, j, k), c in cd.items()), t1s, t2s, t3s)
        for Dp in (D1p, D2p):
            while True:
                q, r = sp.div(P, Dp, domain="QQ")
                if r == 0 and not q.is_zero: P = sp.Poly(q, t1s, t2s, t3s)
                else: break
        sat.append({m: Fr(int(sp.numer(c)), int(sp.denom(c))) for m, c in zip(P.monoms(), P.coeffs())})
    return sat

# ---------------- probe per slice ----------------
def probe_slice(si):
    out = {"slice": si}
    sat = saturated_polys(si)
    hb(f"slice {si}: saturated system ready")
    fin, fout = f"/tmp/t4_s{si}.ms", f"/tmp/t4_s{si}.out"
    open(fin, "w").write("t1,t2,t3\n0\n" + ",\n".join(R.poly_to_ms(p) for p in sat) + ",\n1*t3-1\n")
    subprocess.run([R.MSOLVE, "-P", "2", "-f", fin, "-o", fout], env=R.MSOLVE_ENV, capture_output=True, timeout=600)
    r = R.parse_rur(open(fout).read())
    assert r["kind"] == "rur", f"section not 0-dim: {r}"
    t = sp.symbols("t")
    w = sp.Poly(list(reversed(r["w"])), t)
    facs = [sp.Poly(f, t) for f, mult in sp.factor_list(w.as_expr())[1]]
    facs = [f for f in facs if not (f.degree() == 1 and f.eval(0) == 0)]
    # rational root shortcut = witness path
    lin = [f for f in facs if f.degree() == 1]
    facs.sort(key=lambda f: f.degree())
    mpoly = facs[0]
    out["w_degree"] = w.degree(); out["m_degree"] = mpoly.degree()
    out["linear_factors"] = len(lin)
    mon = mpoly.monic()
    mco = [sp.Rational(c) for c in reversed(mon.all_coeffs())]
    NF.setup([Fr(int(sp.numer(c)), int(sp.denom(c))) for c in mco])
    hb(f"slice {si}: field deg {NF.deg} set up (w deg {w.degree()}, {len(facs)} nontrivial factors)")
    # coordinates in F
    theta = NF([Fr(0), Fr(1)])
    def poly_at_theta(coeffs_ascending):
        acc, p = NF.const(0), NF.const(1)
        for c in coeffs_ascending:
            acc = acc + NF.const(sp.Rational(c)) * p
            p = p * theta
        return acc
    dtheta = poly_at_theta(r["d"])
    dinv = dtheta.inv()
    coords = [(-poly_at_theta(v)) * dinv for v in r["vs"]]
    if len(coords) > 3:
        coords = coords[:3]
    if len(coords) == 2:
        csum = NF.const(0)
        for c, x in zip(r["lf"][:-1], coords):
            csum = csum + NF.const(sp.Rational(c)) * x
        last = (theta - csum) * NF.const(sp.Rational(1, r["lf"][-1])) if r["lf"][-1] != 0 else theta
        coords = coords + [last]
    a1, a2, a3 = coords
    out["t3_is_1"] = bool(a3 == NF.const(1))
    assert out["t3_is_1"], "validity gate: t3 != 1"
    def _pw(a):
        o = [NF.const(1)]
        for _ in range(20): o.append(o[-1] * a)
        return o
    _P = (_pw(a1), _pw(a2), _pw(a3))
    for _cd in sat:
        _acc = NF.const(0)
        for (_i, _j, _k), _c in _cd.items(): _acc = _acc + NF.const(_c) * _P[0][_i] * _P[1][_j] * _P[2][_k]
        assert _acc.is_zero(), "validity gate: sat != 0"
    # field pipeline
    n, N = 5, 10
    g = [Fr(x) for x in (1, 2, 3, 5, 7)]
    Hq = R.H
    sl = B.SLATES[si]
    pu1, pv1, pu2, pv2, pe = ([NF.const(x) for x in R.perp(wv)] for wv in sl)
    U1 = [x + a1 * y for x, y in zip(pu1, pe)]
    U2 = [x + a2 * y + a3 * z for x, y, z in zip(pu2, pe, pv1)]
    def cay_F(U, V):
        S = [[U[i] * V[j] - V[i] * U[j] for j in range(n)] for i in range(n)]
        IpS = [[S[i][j] + NF.const(i == j) for j in range(n)] for i in range(n)]
        ImS = [[NF.const(i == j) - S[i][j] for j in range(n)] for i in range(n)]
        C = nf_matmul(ImS, nf_inv(IpS, n), n)
        return C
    t0 = time.time()
    A = nf_matmul(cay_F(U1, pv1), cay_F(U2, pv2), n)
    HF = [[NF.const(Hq[i][j]) for j in range(n)] for i in range(n)]
    H2 = nf_matmul(nf_T(A), nf_matmul(HF, A, n), n)
    hb(f"slice {si}: A, H2 in F done {round(time.time()-t0,1)}s")
    gF = [NF.const(x) for x in g]
    def O_of_F(Hm):
        return [Hm[i][j] - NF.const(Fr(g[i], 1)) * Hm[j][j] * NF.const(Fr(1, 2) / g[j]) - NF.const(Fr(g[j], 1)) * Hm[i][i] * NF.const(Fr(1, 2) / g[i]) for (i, j) in R.PAIRS]
    O2 = O_of_F(H2)
    O1F = [NF.const(x) for x in R.O_of(Hq, g, R.PAIRS)]
    m2F = []
    for P in R.Ps:
        PO = [sum((NF.const(P[i][k]) * O2[k] for k in range(N)), NF.const(0)) for i in range(N)]
        m2F.append(sum((PO[i] * O2[i] for i in range(N)), NF.const(0)))
    m2_ok = all(m2F[X] == NF.const(R.M_T[X]) for X in range(3))
    def Ehat_F(Hm, rr):
        from itertools import combinations
        tot = NF.const(0)
        for I in combinations(range(n), rr + 1):
            M = [[NF.const(0)] * (rr + 2) for _ in range(rr + 2)]
            for ai, i in enumerate(I):
                M[0][ai + 1] = M[ai + 1][0] = NF.const(g[i])
                for bi, j in enumerate(I):
                    M[ai + 1][bi + 1] = Hm[i][j]
            tot = tot + nf_det(M, rr + 2)
        return tot if (rr + 1) % 2 == 0 else -tot
    e_ok = all(Ehat_F(H2, rr) == NF.const(R.E1[rr - 1]) for rr in (1, 2, 3, 4))
    o_neq = any(not (O2[k] == O1F[k]) for k in range(N))
    out["P2"] = {"m2_tie": bool(m2_ok), "ehat_tie": bool(e_ok), "O2_neq_O1": bool(o_neq)}
    hb(f"slice {si}: P2 {out['P2']} {round(time.time()-t0,1)}s")
    if not (m2_ok and e_ok and o_neq):
        out["verdict"] = "PIPELINE_DEFECT"
        return out
    # P3: group-Jacobian via [H2, B]
    gg = sum(x * x for x in g)
    basis = []
    for i in range(4):
        w0 = [Fr(k == i) - g[i] * g[k] / gg for k in range(n)]
        for u in basis:
            uw = sum(a * b for a, b in zip(u, w0)); uu = sum(a * a for a in u)
            w0 = [a - uw * b / uu for a, b in zip(w0, u)]
        basis.append(w0)
    from itertools import combinations as comb2
    rows = []
    for ai, bi in comb2(range(4), 2):
        u, v = basis[ai], basis[bi]
        Bm = [[NF.const(u[i] * v[j] - v[i] * u[j]) for j in range(n)] for i in range(n)]
        HB = nf_matmul(H2, Bm, n); BH = nf_matmul(Bm, H2, n)
        dH2 = [[HB[i][j] - BH[i][j] for j in range(n)] for i in range(n)]
        dO = O_of_F(dH2)
        col = []
        for X in range(3):
            PO = [sum((NF.const(R.Ps[X][i][k]) * O2[k] for k in range(N)), NF.const(0)) for i in range(N)]
            col.append(sum((PO[i] * dO[i] for i in range(N)), NF.const(0)) * NF.const(2))
        rows.append(col)
    J = [[rows[c][X] for c in range(6)] for X in range(3)]  # 3x6
    rk = nf_rank(J, 3, 6)
    out["rank"] = rk; out["kernel"] = 6 - rk
    hb(f"slice {si}: P3 rank {rk} kernel {6-rk} {round(time.time()-t0,1)}s")
    return out

def main():
    EH.clause_gate(PREDECL, T4, PIN)
    EH.pin_gate(PINS)
    got = hashlib.sha256(open(R.MSOLVE, "rb").read()).hexdigest()[:16]
    assert got == R.MSOLVE_PIN, "engine pin"
    print("GATES_GREEN predecl_pin", PIN)
    blob, tm = {}, {}
    for si in (0, 1):
        t0 = time.perf_counter()
        blob[f"s{si}"] = probe_slice(si)
        tm[f"s{si}"] = round(time.perf_counter() - t0, 1)
    ks = [blob[f"s{si}"].get("kernel") for si in (0, 1)]
    vs = [blob[f"s{si}"].get("verdict") for si in (0, 1)]
    if "PIPELINE_DEFECT" in vs: blob["verdict"] = "PIPELINE_DEFECT"
    elif any(k == 3 for k in ks): blob["verdict"] = "T4_REFUTED_AT_POINT"
    elif all(k is not None and k >= 4 for k in ks): blob["verdict"] = "T4_STRUCTURAL"
    else: blob["verdict"] = "MIXED"
    out = json.dumps(blob, sort_keys=True, indent=1)
    print(out)
    print("RECORDS_SHA256", EH.records_sha(out))
    print("TIMINGS_JSON", json.dumps(tm, sort_keys=True))
    print("T4_PROBE_COMPLETE")

if __name__ == "__main__":
    main()
