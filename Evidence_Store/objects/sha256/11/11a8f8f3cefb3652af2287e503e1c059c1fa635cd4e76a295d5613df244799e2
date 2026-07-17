#!/usr/bin/env python3
"""pi_stage0.py -- pi-rotation boundary chassis Stage 0 (PI_STAGE0_PREDECL).
Family: A(t1,t2,t3) = cay(pu1 + t1*pe, pv1) * R_plane(p, q),
        p = pu2 + t2*pe, q = pv2 + t3*pv1  (all vectors perp'd SLATES[0]).
R_plane = I - 2*(qq*pp^T - pq*(pq^T+qp^T) + pp*qq^T)/G2 (Gram reflection).
PI.1 (A^T A = I, A g = g, exact) asserted at EVERY evaluation point.
Modes: smoke | build  (build emits /tmp/pirot_s0.ms, Rabinowitsch y*D1*G2-1)
"""
import sys
from fractions import Fraction as Fr
from math import lcm
BASE = '/home/wlloyd/Lloyd_Engine_V4/portfolio/campaigns/shape_witness'
sys.path.insert(0, BASE)
import hunt_v2_msolve as R
import flagship_stageA_battery as B
import stage2_build as S2
import sympy as sp

def gram_reflect(p, q, n):
    pp = sum(x * x for x in p); qq = sum(x * x for x in q)
    pq = sum(x * y for x, y in zip(p, q))
    G2 = pp * qq - pq * pq
    assert G2 != 0, "degenerate plane"
    Rm = [[Fr(i == j) - 2 * (qq * p[i] * p[j] - pq * (p[i] * q[j] + q[i] * p[j])
          + pp * q[i] * q[j]) / G2 for j in range(n)] for i in range(n)]
    return Rm, G2

def family():
    sl = B.SLATES[0]
    pu1, pv1, pu2, pv2, pe = (R.perp(w) for w in sl)
    vecs = (list(pu1), list(pv1), list(pu2), list(pv2), list(pe))
    pu1, pv1, pu2, pv2, pe = vecs
    n, g = R.n, R.g
    def evalpt(t1, t2, t3):
        U1 = [a + t1 * b for a, b in zip(pu1, pe)]
        C = B.cayley(U1, pv1, g, n)
        p = [a + t2 * b for a, b in zip(pu2, pe)]
        q = [a + t3 * b for a, b in zip(pv2, pv1)]
        Rm, G2 = gram_reflect(p, q, n)
        A = B.matmul(C, Rm, n)
        At = B.matT(A)
        AtA = B.matmul(At, A, n)
        assert all(AtA[i][j] == Fr(i == j) for i in range(n) for j in range(n)), "PI.1 orth FAIL"
        assert all(sum(A[i][k] * g[k] for k in range(n)) == g[i] for i in range(n)), "PI.1 g-fix FAIL"
        H2 = B.matmul(At, B.matmul(R.H, A, n), n)
        mm = B.m2s(B.O_of(H2, g, R.PAIRS), R.Ps, R.N)
        return mm, G2
    def D1f(t1):
        U1 = [a + t1 * b for a, b in zip(pu1, pe)]
        return 1 + sum(x * x for x in U1) * sum(y * y for y in pv1) \
               - sum(x * y for x, y in zip(U1, pv1)) ** 2
    def G2f(t2, t3):
        p = [a + t2 * b for a, b in zip(pu2, pe)]
        q = [a + t3 * b for a, b in zip(pv2, pv1)]
        pp = sum(x * x for x in p); qq = sum(x * x for x in q)
        pq = sum(x * y for x, y in zip(p, q))
        return pp * qq - pq * pq
    return evalpt, D1f, G2f, vecs

def build():
    evalpt, D1f, G2f, vecs = family()
    K, D = 8, 19
    xs = [Fr(k) for k in range(-(D // 2), D - D // 2)]
    grid = {}
    for a1 in xs:
        for a2 in xs:
            for a3 in xs:
                mm, _ = evalpt(a1, a2, a3)
                w = D1f(a1) ** K * G2f(a2, a3) ** K
                grid[(a1, a2, a3)] = [(mm[X] - R.M_T[X]) * w for X in range(3)]
    polys = []
    for X in range(3):
        c3 = {}
        for a1 in xs:
            for a2 in xs:
                co = B.interp_1d(xs, [grid[(a1, a2, a3)][X] for a3 in xs])
                for k3, c in enumerate(co): c3.setdefault(k3, {})[(a1, a2)] = c
        cdict = {}
        for k3, tbl in c3.items():
            c2 = {}
            for a1 in xs:
                co = B.interp_1d(xs, [tbl.get((a1, a2), Fr(0)) for a2 in xs])
                for k2, c in enumerate(co): c2.setdefault(k2, {})[a1] = c
            for k2, tb1 in c2.items():
                co = B.interp_1d(xs, [tb1.get(a1, Fr(0)) for a1 in xs])
                for k1, c in enumerate(co):
                    if c != 0: cdict[(k1, k2, k3)] = c
        import random as _r
        rr = _r.Random(7100 + X)
        for _ in range(3):
            pt = tuple(Fr(rr.randint(8, 12), rr.choice([1, 3])) for _ in range(3))
            mm, _ = evalpt(*pt)
            direct = (mm[X] - R.M_T[X]) * D1f(pt[0]) ** K * G2f(pt[1], pt[2]) ** K
            val = sum(c * pt[0] ** i * pt[1] ** j * pt[2] ** k for (i, j, k), c in cdict.items())
            if val != direct: raise RuntimeError("self-check failed X=%d" % X)
        polys.append(cdict)
    return polys, vecs

def emit():
    polys, vecs = build()
    pu1, pv1, pu2, pv2, pe = [[sp.Rational(x.numerator, x.denominator) for x in v] for v in vecs]
    t1s, t2s, t3s, ys = sp.symbols('t1 t2 t3 y')
    U1 = [a + t1s * b for a, b in zip(pu1, pe)]
    D1 = sp.expand(1 + sum(x * x for x in U1) * sum(y * y for y in pv1)
                   - sum(x * y for x, y in zip(U1, pv1)) ** 2)
    p = [a + t2s * b for a, b in zip(pu2, pe)]
    q = [a + t3s * b for a, b in zip(pv2, pv1)]
    G2 = sp.expand(sum(x * x for x in p) * sum(y * y for y in q)
                   - sum(x * y for x, y in zip(p, q)) ** 2)
    rab = S2.gen_to_ms(ys * D1 * G2 - 1, (t1s, t2s, t3s, ys), ('t1', 't2', 't3', 'y'))
    out = "t1,t2,t3,y\n0\n" + ",\n".join([R.poly_to_ms(pd) for pd in polys] + [rab]) + "\n"
    open('/tmp/pirot_s0.ms', 'w').write(out)
    print("WROTE /tmp/pirot_s0.ms (%d bytes) PI.1_ALL_SILENT" % len(out))

def smoke():
    evalpt, D1f, G2f, _ = family()
    for pt in ((Fr(1), Fr(1), Fr(1)), (Fr(2), Fr(-1), Fr(3)), (Fr(1, 3), Fr(5), Fr(-2))):
        mm, G2 = evalpt(*pt)
        assert G2 != 0 and D1f(pt[0]) != 0
        print("smoke %s: mm=%s G2=%s  PI.1_SILENT" % (pt, [str(x)[:12] for x in mm], str(G2)[:16]))
    print("SMOKE_PASS")

if __name__ == '__main__':
    if sys.argv[1] == 'smoke': smoke()
    elif sys.argv[1] == 'build': emit()
