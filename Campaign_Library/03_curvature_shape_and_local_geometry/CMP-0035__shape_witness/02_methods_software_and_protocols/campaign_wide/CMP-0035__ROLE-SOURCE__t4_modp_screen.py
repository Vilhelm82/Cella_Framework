#!/usr/bin/env python3
"""t4_modp_screen.py — T4 probe mod-p screening layer (Amendment A2). Predecl pin ecd71cb22697b39a.
kernel_p = 3 at any good prime CERTIFIES kernel = 3 over Q(theta) [rank semicontinuity] => T4 REFUTED at point.
kernel_p = 4 at all primes => STRUCTURAL, exact run stays the certification tail."""
import sys, os, json, time, subprocess, hashlib
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "portfolio", "campaigns", "the_engine", "stage_A"))
sys.path.insert(0, os.path.join(REPO, "evals", "dbp_involution"))
import engine_harness as EH
import hunt_v2_msolve as R
import t4_probe as T
import sympy as sp
B = R.B

def hb(m): print("[hb]", m, file=sys.stderr, flush=True)

def pick_primes(mco_num, mco_den, k=5):
    """five smallest primes > 2^59 with m irreducible mod p and all denominators invertible"""
    x = sp.symbols("x")
    p = sp.nextprime(2**59)
    out = []
    while len(out) < k:
        if all(d % p != 0 for d in mco_den):
            mp = sp.Poly([ (n * pow(d, -1, p)) % p for n, d in zip(mco_num, mco_den)], x, modulus=p)
            try:
                if mp.degree() == len(mco_num) - 1 and len(sp.factor_list(mp.as_expr(), modulus=p)[1]) == 1:
                    out.append(p)
            except Exception:
                pass
        p = sp.nextprime(p)
    return out

class Fp:
    p = None; deg = None; red = None
    @classmethod
    def setup(cls, p, mco):  # mco monic ascending as Fr
        cls.p = p; cls.deg = len(mco) - 1
        m = [ (c.numerator * pow(c.denominator, -1, p)) % p for c in mco ]
        red = []
        cur = [(-c) % p for c in m[:-1]]
        red.append(cur[:])
        for _ in range(cls.deg - 2):
            cur = [0] + cur
            hi = cur.pop()
            cur = [ (c + hi * r) % p for c, r in zip(cur, red[0]) ]
            red.append(cur[:])
        cls.red = red
    def __init__(s, co):
        d, p = Fp.deg, Fp.p
        co = [c % p for c in co]
        while len(co) > d:
            hi = co.pop()
            if hi:
                r = Fp.red[len(co) - d]
                for i in range(d): co[i] = (co[i] + hi * r[i]) % p
        s.c = co + [0] * (d - len(co))
    @staticmethod
    def const(q):
        q = Fr(q)
        return Fp([ (q.numerator * pow(q.denominator, -1, Fp.p)) % Fp.p ])
    def __add__(s, o): return Fp([(a + b) for a, b in zip(s.c, o.c)])
    def __sub__(s, o): return Fp([(a - b) for a, b in zip(s.c, o.c)])
    def __neg__(s): return Fp([-a for a in s.c])
    def __mul__(s, o):
        d, p = Fp.deg, Fp.p
        out = [0] * (2 * d - 1)
        for i, a in enumerate(s.c):
            if a:
                for j, b in enumerate(o.c):
                    if b: out[i + j] = (out[i + j] + a * b) % p
        return Fp(out)
    def is_zero(s): return all(x == 0 for x in s.c)
    def __eq__(s, o): return s.c == o.c
    def inv(s):
        # Fermat in F_p[x]/(m): s^(p^deg - 2) too big; use extended Euclid over F_p
        p = Fp.p
        r0, r1 = [c for c in Fp._m_int()], s.c[:]
        s0, s1 = [0], [1]
        def deg(a):
            k = len(a) - 1
            while k >= 0 and a[k] == 0: k -= 1
            return k
        while deg(r1) > 0:
            while deg(r0) >= deg(r1) and deg(r1) >= 0:
                d0, d1 = deg(r0), deg(r1)
                c = (r0[d0] * pow(r1[d1], -1, p)) % p
                sh = d0 - d1
                r0 = r0 + [0] * max(0, len(r1) + sh - len(r0))
                for i, x in enumerate(r1): r0[i + sh] = (r0[i + sh] - c * x) % p
                s0 = s0 + [0] * max(0, len(s1) + sh - len(s0))
                for i, x in enumerate(s1): s0[i + sh] = (s0[i + sh] - c * x) % p
            r0, r1, s0, s1 = r1, r0, s1, s0
        u = r1[deg(r1)]
        ui = pow(u, -1, p)
        return Fp([(x * ui) % p for x in s1])
    def __truediv__(s, o): return s * o.inv()
    _mstash = None
    @classmethod
    def _m_int(cls): return cls._mstash

def run_screen(si, primes_wanted=5):
    out = {"slice": si}
    sat = T.saturated_polys(si)
    fin, fout = f"/tmp/t4m_s{si}.ms", f"/tmp/t4m_s{si}.out"
    open(fin, "w").write("t1,t2,t3\n0\n" + ",\n".join(R.poly_to_ms(p) for p in sat) + ",\n1*t3-1\n")
    subprocess.run([R.MSOLVE, "-P", "2", "-f", fin, "-o", fout], env=R.MSOLVE_ENV, capture_output=True, timeout=600)
    r = R.parse_rur(open(fout).read())
    t = sp.symbols("t")
    w = sp.Poly(list(reversed(r["w"])), t)
    facs = [sp.Poly(f, t) for f, m_ in sp.factor_list(w.as_expr())[1] if not (sp.Poly(f, t).degree() == 1 and sp.Poly(f, t).eval(0) == 0)]
    facs.sort(key=lambda f: f.degree())
    mon = facs[0].monic()
    mco = [sp.Rational(c) for c in reversed(mon.all_coeffs())]
    mco_fr = [Fr(int(sp.numer(c)), int(sp.denom(c))) for c in mco]
    out["m_degree"] = len(mco_fr) - 1
    primes = pick_primes([c.numerator for c in mco_fr], [c.denominator for c in mco_fr], primes_wanted)
    out["primes"] = [str(p) for p in primes]
    n, N = 5, 10
    g = [Fr(x) for x in (1, 2, 3, 5, 7)]
    per_prime = {}
    for p in primes:
        t0 = time.time()
        try:
            Fp._mstash = [ (c.numerator * pow(c.denominator, -1, p)) % p for c in mco_fr ]
            Fp.setup(p, mco_fr)
            theta = Fp([0, 1])
            def pat(co):
                acc, pw = Fp.const(0), Fp.const(1)
                for c in co:
                    cf = Fr(sp.Rational(c))
                    acc = acc + Fp.const(cf) * pw
                    pw = pw * theta
                return acc
            dinv = pat(r["d"]).inv()
            coords = [(-pat(v)) * dinv for v in r["vs"]]
            if len(coords) > 3: coords = coords[:3]
            a1, a2, a3 = coords
            assert a3 == Fp.const(1), "validity gate: t3 != 1"
            def _pw(a):
                out = [Fp.const(1)]
                for _ in range(20): out.append(out[-1] * a)
                return out
            _P = (_pw(a1), _pw(a2), _pw(a3))
            for _cd in sat:
                _acc = Fp.const(0)
                for (_i, _j, _k), _c in _cd.items(): _acc = _acc + Fp.const(_c) * _P[0][_i] * _P[1][_j] * _P[2][_k]
                assert _acc.is_zero(), "validity gate: sat != 0"
            sl = B.SLATES[si]
            pu1, pv1, pu2, pv2, pe = ([Fp.const(x) for x in R.perp(wv)] for wv in sl)
            U1 = [x + a1 * y for x, y in zip(pu1, pe)]
            U2 = [x + a2 * y + a3 * z for x, y, z in zip(pu2, pe, pv1)]
            def cay(U, V):
                S = [[U[i] * V[j] - V[i] * U[j] for j in range(n)] for i in range(n)]
                IpS = [[S[i][j] + Fp.const(i == j) for j in range(n)] for i in range(n)]
                ImS = [[Fp.const(i == j) - S[i][j] for j in range(n)] for i in range(n)]
                # inverse via Gaussian over Fp-field elements
                A = [[IpS[i][j] for j in range(n)] + [Fp.const(i == j) for j in range(n)] for i in range(n)]
                for c in range(n):
                    pr = next(rr for rr in range(c, n) if not A[rr][c].is_zero())
                    A[c], A[pr] = A[pr], A[c]
                    piv = A[c][c].inv()
                    A[c] = [x * piv for x in A[c]]
                    for rr in range(n):
                        if rr != c and not A[rr][c].is_zero():
                            f = A[rr][c]
                            A[rr] = [a - f * b for a, b in zip(A[rr], A[c])]
                inv = [row[n:] for row in A]
                return [[sum((ImS[i][k] * inv[k][j] for k in range(n)), Fp.const(0)) for j in range(n)] for i in range(n)]
            def mm(Am, Bm): return [[sum((Am[i][k] * Bm[k][j] for k in range(n)), Fp.const(0)) for j in range(n)] for i in range(n)]
            A = mm(cay(U1, pv1), cay(U2, pv2))
            HF = [[Fp.const(R.H[i][j]) for j in range(n)] for i in range(n)]
            H2 = mm([list(rw) for rw in zip(*A)], mm(HF, A))
            def O_of(Hm):
                return [Hm[i][j] - Fp.const(Fr(g[i]) / (2 * g[j])) * Hm[j][j] - Fp.const(Fr(g[j]) / (2 * g[i])) * Hm[i][i] for (i, j) in R.PAIRS]
            O2 = O_of(H2)
            m2 = []
            for P in R.Ps:
                PO = [sum((Fp.const(P[i][k]) * O2[k] for k in range(N)), Fp.const(0)) for i in range(N)]
                m2.append(sum((PO[i] * O2[i] for i in range(N)), Fp.const(0)))
            ties = all(m2[X] == Fp.const(R.M_T[X]) for X in range(3))
            from itertools import combinations as cb
            def EhatF(rr_):
                tot = Fp.const(0)
                for I in cb(range(n), rr_ + 1):
                    M = [[Fp.const(0)] * (rr_ + 2) for _ in range(rr_ + 2)]
                    for ai, i in enumerate(I):
                        M[0][ai + 1] = M[ai + 1][0] = Fp.const(g[i])
                        for bi, j in enumerate(I): M[ai + 1][bi + 1] = H2[i][j]
                    # det via Gaussian
                    Am = [row[:] for row in M]; det = Fp.const(1); m_ = rr_ + 2
                    ok = True
                    for c in range(m_):
                        pr = next((x for x in range(c, m_) if not Am[x][c].is_zero()), None)
                        if pr is None: det = Fp.const(0); ok = False; break
                        if pr != c: Am[c], Am[pr] = Am[pr], Am[c]; det = -det
                        det = det * Am[c][c]; piv = Am[c][c].inv()
                        for x in range(c + 1, m_):
                            if not Am[x][c].is_zero():
                                f = Am[x][c] * piv
                                Am[x] = [aa - f * bb for aa, bb in zip(Am[x], Am[c])]
                    tot = tot + det
                return tot if (rr_ + 1) % 2 == 0 else -tot
            eties = all(EhatF(rr_) == Fp.const(R.E1[rr_ - 1]) for rr_ in (1, 2, 3, 4))
            gg = sum(x * x for x in g)
            basis = []
            for i in range(4):
                w0 = [Fr(k == i) - g[i] * g[k] / gg for k in range(n)]
                for u in basis:
                    uw = sum(a * b for a, b in zip(u, w0)); uu = sum(a * a for a in u)
                    w0 = [a - uw * b / uu for a, b in zip(w0, u)]
                basis.append(w0)
            rows = []
            for ai, bi in cb(range(4), 2):
                u, v = basis[ai], basis[bi]
                Bm = [[Fp.const(u[i] * v[j] - v[i] * u[j]) for j in range(n)] for i in range(n)]
                HB = mm(H2, Bm); BH = mm(Bm, H2)
                dO = O_of([[HB[i][j] - BH[i][j] for j in range(n)] for i in range(n)])
                col = []
                for X in range(3):
                    PO = [sum((Fp.const(R.Ps[X][i][k]) * O2[k] for k in range(N)), Fp.const(0)) for i in range(N)]
                    col.append(sum((PO[i] * dO[i] for i in range(N)), Fp.const(0)))
                rows.append(col)
            J = [[rows[c][X] for c in range(6)] for X in range(3)]
            rk = 0
            Am = [r_[:] for r_ in J]
            for c in range(6):
                pr = next((x for x in range(rk, 3) if not Am[x][c].is_zero()), None)
                if pr is None: continue
                Am[rk], Am[pr] = Am[pr], Am[rk]
                piv = Am[rk][c].inv()
                Am[rk] = [x * piv for x in Am[rk]]
                for x in range(3):
                    if x != rk and not Am[x][c].is_zero():
                        f = Am[x][c]
                        Am[x] = [a - f * b for a, b in zip(Am[x], Am[rk])]
                rk += 1
                if rk == 3: break
            rec_p = {"ties_mod_p": bool(ties), "ehat_mod_p": bool(eties), "wall_s": round(time.time() - t0, 2)}
            if ties and eties:
                rec_p["rank"] = rk; rec_p["kernel"] = 6 - rk
            else:
                rec_p["point_invalid"] = True
            per_prime[str(p)] = rec_p
            hb(f"slice {si} p={p}: ties {ties} ehat {eties} rank {rk} kernel {6-rk} ({round(time.time()-t0,1)}s)")
        except Exception as ex:
            per_prime[str(p)] = {"error": str(ex)[:120]}
    out["per_prime"] = {k: {kk: vv for kk, vv in v.items() if kk != "wall_s"} for k, v in per_prime.items()}
    ks = [v.get("kernel") for v in per_prime.values() if "kernel" in v]
    out["min_kernel"] = min(ks) if ks else None
    return out

def main():
    EH.clause_gate(T.PREDECL, T.T4, "ecd71cb22697b39a")
    EH.pin_gate(T.PINS)
    print("GATES_GREEN predecl_pin ecd71cb22697b39a (A2)")
    blob = {}
    for si in (0, 1):
        blob[f"s{si}"] = run_screen(si)
    mins = [blob[f"s{si}"]["min_kernel"] for si in (0, 1)]
    anyinvalid = any("point_invalid" in v for si in (0, 1) for v in blob[f"s{si}"]["per_prime"].values())
    if anyinvalid: blob["verdict"] = "POINT_INVALID (P2 failed at some prime; no kernel semantics)"
    elif any(k == 3 for k in mins): blob["verdict"] = "T4_REFUTED_CERTIFIED (kernel=3 mod p => kernel=3 exactly)"
    elif all(k == 4 for k in mins): blob["verdict"] = "T4_STRUCTURAL_MODP (kernel<=4 certified; =4 pending exact tail)"
    else: blob["verdict"] = f"MODP_MIXED {mins}"
    out = json.dumps(blob, sort_keys=True, indent=1)
    print(out)
    print("RECORDS_SHA256", EH.records_sha(out))
    print("T4_MODP_COMPLETE")

if __name__ == "__main__":
    main()
