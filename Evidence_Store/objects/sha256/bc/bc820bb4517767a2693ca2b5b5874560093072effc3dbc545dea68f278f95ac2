#!/usr/bin/env python3
"""m33d_build.py -- 3b.3-d battery (PREREG_3B3D). Rebuilds the M-B system
(regression-gated against the banked m33_mb.ms sha), adjoins u-generators
for dloc-D1 / dloc-D2 / control-E, runs pinned msolve, grades x2 with
banked anyrur_grade.py, writes flag files. Deterministic.
Usage: m33d_build.py MODE   (MODE in d1, d2, ectl, pd4)
Defs first, dispatch last."""
import sys, os, subprocess, hashlib
import sympy as sp
from math import lcm
HERE = os.path.dirname(os.path.abspath(__file__))
MSOLVE = os.path.expanduser("~/msolve_jll/bin/msolve")
MSOLVE_ENV = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser("~/msolve_jll/lib"))
MB_MS_SHA = "regression gate computed at runtime vs records/m33_mb.ms"

G4 = [3, 1, 2, 5]
H4 = [[2, 1, -1, 1], [1, 3, 2, -1], [-1, 2, 1, 2], [1, -1, 2, -2]]
S4 = {"u1": [1, 2, -1, 1], "v1": [2, -1, 1, -1], "u2": [1, -1, 2, 1],
      "v2": [-1, 1, 1, 2], "e": [1, 1, -2, 1]}

def perp(w, g):
    q = sum(x * x for x in g)
    c = sp.Rational(sum(a * b for a, b in zip(w, g)), q)
    return [sp.Rational(a) - c * b for a, b in zip(w, g)]

def skew(U, v, n):
    return sp.Matrix(n, n, lambda i, j: U[i] * v[j] - v[i] * U[j])

def cay_parts(U, v, n):
    A = skew(U, v, n)
    D = sp.expand(1 + sum(x * x for x in U) * sum(y * y for y in v)
                  - sum(x * y for x, y in zip(U, v)) ** 2)
    Rn = sp.expand((sp.eye(n) - A) * (sp.eye(n) + A).adjugate())
    return Rn, D

def O_of(Hm, g, n):
    prs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    return [sp.expand(Hm[i, j] - sp.Rational(g[i], 2 * g[j]) * Hm[j, j]
                      - sp.Rational(g[j], 2 * g[i]) * Hm[i, i])
            for (i, j) in prs]

def projectors_pair4():
    sys.path.insert(0, os.path.normpath(HERE + '/../../../../evals/dbp_involution'))
    import rep_utils as RU
    import itertools
    n = 4
    prs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    idx = {p: k for k, p in enumerate(prs)}
    N = len(prs)
    Ps = []
    for lam in ((4,), (3, 1), (2, 2)):
        d = RU.specht_dim(lam)
        P = sp.zeros(N, N)
        for p in itertools.permutations(range(n)):
            chi = RU.specht_char(lam, RU.cycle_type(p))
            if chi == 0: continue
            for k, (i, j) in enumerate(prs):
                a, b = p[i], p[j]
                P[idx[(min(a, b), max(a, b))], k] += chi
        Ps.append(P * sp.Rational(d, sp.factorial(n)))
    return Ps

def m2(vec, P):
    v = sp.Matrix(len(vec), 1, vec)
    return sp.expand((v.T * P * v)[0])

def gen_to_ms(expr, syms, names):
    P = sp.Poly(sp.expand(expr), *syms)
    L = 1
    for c in P.coeffs(): L = lcm(L, int(sp.Rational(c).q))
    terms = []
    for mono, c in zip(P.monoms(), P.coeffs()):
        ci = int(sp.Rational(c) * L)
        if ci == 0: continue
        m = "*".join("%s^%d" % (nm, e) for nm, e in zip(names, mono) if e) or "1"
        terms.append(("+" if ci > 0 and terms else "") + str(ci) + "*" + m)
    return "".join(terms)

def saturate(tie, Ds, syms):
    for D in Ds:
        while True:
            q, r = sp.div(tie, D, *syms)
            if sp.expand(r) == 0 and sp.expand(q) != 0:
                tie = sp.expand(q)
            else:
                break
    return tie

def build_mb_core():
    n, g, H, S = 4, G4, H4, S4
    t1, t2, t3, y, u = sp.symbols('t1 t2 t3 y u')
    pu1, pv1 = perp(S["u1"], g), perp(S["v1"], g)
    pu2, pv2, pe = perp(S["u2"], g), perp(S["v2"], g), perp(S["e"], g)
    U1 = [a + t1 * b for a, b in zip(pu1, pe)]
    U2 = [a + t2 * b + t3 * c for a, b, c in zip(pu2, pe, pv1)]
    R1n, D1 = cay_parts(U1, pv1, n)
    R2n, D2 = cay_parts(U2, pv2, n)
    Rn, Dall = sp.expand(R1n * R2n), sp.expand(D1 * D2)
    Hm = sp.Matrix(H)
    Hnum = sp.expand(Rn.T * Hm * Rn)
    Obase, Onum = O_of(Hm, g, n), O_of(Hnum, g, n)
    ts = (t1, t2, t3)
    ties = []
    for P in projectors_pair4():
        tie = sp.expand(m2(Onum, P) - m2(Obase, P) * Dall ** 4)
        ties.append(saturate(tie, [D1, D2], ts))
    rab = y * Dall - 1
    # regression gate: rebuilt base .ms must equal the banked one
    names = ['t1', 't2', 't3', 'y']
    gens = [gen_to_ms(t_, ts, names[:-1]) for t_ in ties] + \
           [gen_to_ms(rab, ts + (y,), names)]
    out = ",".join(names) + "\n0\n" + ",\n".join(gens) + "\n"
    got = hashlib.sha256(out.encode()).hexdigest()
    want = hashlib.sha256(open(HERE + '/records/m33_mb.ms', 'rb').read()).hexdigest()
    assert got == want, "K-3B3D-0 REGRESSION: rebuilt M-B .ms != banked"
    return ties, rab, ts, y, u, D1, D2, U1

def main():
    mode = sys.argv[1]
    ties, rab, ts, y, u, D1, D2, U1 = build_mb_core()
    print("REGRESSION_GATE_OK")
    if mode == "pd4":
        # Pfister-shape identity: D = 1 + sum of Plucker minors^2, symbolic in t1
        n = 4
        g = G4
        pv1 = perp(S4["v1"], g)
        pluck = [U1[k] * pv1[l] - U1[l] * pv1[k]
                 for k in range(n) for l in range(k + 1, n)]
        lhs = sp.expand(D1 - 1 - sum(p * p for p in pluck))
        print("PD4_IDENTITY_HOLDS" if lhs == 0 else "PD4_IDENTITY_FAILS")
        return
    if mode == "d1":
        ugen = u * D1 - 1
    elif mode == "d2":
        ugen = u * D2 - 1
    else:
        E = sp.expand(2 + sum(x * x for x in U1))
        ugen = u * E - 1
    names = ['t1', 't2', 't3', 'y', 'u']
    gens = [gen_to_ms(t_, ts, names[:3]) for t_ in ties] + \
           [gen_to_ms(rab, ts + (y,), names[:4]),
            gen_to_ms(ugen, ts + (u,), names[:3] + ['u'])]
    out = ",".join(names) + "\n0\n" + ",\n".join(gens) + "\n"
    path = '/tmp/m33d_%s.ms' % mode
    open(path, 'w').write(out)
    print("WROTE %s (%d bytes)" % (path, len(out)))
    fout = '/tmp/m33d_%s.out' % mode
    pr = subprocess.run([MSOLVE, "-P", "2", "-f", path, "-o", fout],
                        env=MSOLVE_ENV, capture_output=True, timeout=1800)
    print("msolve rc=%d" % pr.returncode)
    for i in (1, 2):
        gout = '/tmp/m33d_%s_grade%d.out' % (mode, i)
        subprocess.run(["python3", os.path.normpath(HERE + '/../anyrur_grade.py'),
                        fout, gout], capture_output=True, text=True)
    h1 = hashlib.sha256(open('/tmp/m33d_%s_grade1.out' % mode, 'rb').read()).hexdigest()
    h2 = hashlib.sha256(open('/tmp/m33d_%s_grade2.out' % mode, 'rb').read()).hexdigest()
    open('/tmp/m33d_%s.flag' % mode, 'w').write(
        "DONE x2=%s\n" % (h1 == h2))
    print("FLAG WRITTEN", h1 == h2)

if __name__ == "__main__":
    main()
