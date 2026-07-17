#!/usr/bin/env python3
"""m33_build.py -- 3b.3 miniature builder + runner (PREREG_3B3, frozen).
Builds M-0 / M-A / M-B systems per the frozen construction, runs pinned
msolve, grades with banked anyrur_grade.py x2. Deterministic.
Usage: m33_build.py RUNG   (RUNG in m0, ma, mb)
Defs first, dispatch last."""
import sys, os, subprocess, hashlib
import sympy as sp
from math import lcm
HERE = os.path.dirname(os.path.abspath(__file__))
MSOLVE = os.path.expanduser("~/msolve_jll/bin/msolve")
MSOLVE_ENV = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser("~/msolve_jll/lib"))

G3 = [3, 1, 2]
H3 = [[2, 1, -1], [1, 3, 2], [-1, 2, 1]]
S3 = {"u1": [1, 2, -1], "v1": [2, -1, 1], "u2": [1, -1, 2],
      "v2": [-1, 1, 1], "e": [1, 1, -2]}
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
    Ddet = sp.expand((sp.eye(n) + A).det())
    assert sp.simplify(D - Ddet) == 0, "K-3B3-0 D closed form"
    Rn = sp.expand((sp.eye(n) - A) * (sp.eye(n) + A).adjugate())
    return Rn, D

def O_of(Hm, g, n):
    prs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    return [sp.expand(Hm[i, j] - sp.Rational(g[i], 2 * g[j]) * Hm[j, j]
                      - sp.Rational(g[j], 2 * g[i]) * Hm[i, i])
            for (i, j) in prs]

def projectors_pair(n):
    if n == 3:
        J = sp.ones(3, 3)
        return [J / 3, sp.eye(3) - J / 3]
    sys.path.insert(0, os.path.normpath(HERE + '/../../../../evals/dbp_involution'))
    import rep_utils as RU
    import itertools
    from fractions import Fraction as Fr
    prs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    idx = {p: k for k, p in enumerate(prs)}
    N = len(prs)
    Ps = []
    for lam in ((n,), (n - 1, 1), (n - 2, 2)):
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
    mults = []
    for D in Ds:
        m = 0
        while True:
            q, r = sp.div(tie, D, *syms)
            if sp.expand(r) == 0 and sp.expand(q) != 0:
                tie = sp.expand(q); m += 1
            else:
                break
        mults.append(m)
    return tie, mults

def build_rung(rung):
    if rung in ("m0", "ma"):
        n, g, H, S = 3, G3, H3, S3
    else:
        n, g, H, S = 4, G4, H4, S4
    pu1, pv1 = perp(S["u1"], g), perp(S["v1"], g)
    pu2, pv2, pe = perp(S["u2"], g), perp(S["v2"], g), perp(S["e"], g)
    t1, t2, t3, y = sp.symbols('t1 t2 t3 y')
    if rung == "m0":
        U1 = [a + t1 * b + t2 * c for a, b, c in zip(pu1, pe, pv2)]
        R1n, D1 = cay_parts(U1, pv1, n)
        Rn, Dall, ts = R1n, D1, (t1, t2)
    elif rung == "ma":
        U1 = [a + t1 * b for a, b in zip(pu1, pe)]
        U2 = [a + t2 * b for a, b in zip(pu2, pe)]
        R1n, D1 = cay_parts(U1, pv1, n)
        R2n, D2 = cay_parts(U2, pv2, n)
        Rn, Dall, ts = sp.expand(R1n * R2n), sp.expand(D1 * D2), (t1, t2)
    else:
        U1 = [a + t1 * b for a, b in zip(pu1, pe)]
        U2 = [a + t2 * b + t3 * c for a, b, c in zip(pu2, pe, pv1)]
        R1n, D1 = cay_parts(U1, pv1, n)
        R2n, D2 = cay_parts(U2, pv2, n)
        Rn, Dall, ts = sp.expand(R1n * R2n), sp.expand(D1 * D2), (t1, t2, t3)
    Hm = sp.Matrix(H)
    Hnum = sp.expand(Rn.T * Hm * Rn)      # denominator Dall^2
    Obase = O_of(Hm, g, n)
    Onum = O_of(Hnum, g, n)               # denominator Dall^2
    Ps = projectors_pair(n)
    Ds = [D1] if rung == "m0" else [D1, D2]
    ties, allmults = [], []
    for P in Ps:
        tie = sp.expand(m2(Onum, P) - m2(Obase, P) * Dall ** 4)
        tie, mults = saturate(tie, Ds, ts)
        assert sp.expand(tie) != 0, "K-3B3-0 tie vanished"
        ties.append(tie); allmults.append(mults)
    rab = y * Dall - 1
    names = [str(s) for s in ts] + ['y']
    gens = [gen_to_ms(t_, ts, names[:-1]) for t_ in ties] + \
           [gen_to_ms(rab, ts + (y,), names)]
    out = ",".join(names) + "\n0\n" + ",\n".join(gens) + "\n"
    path = '/tmp/m33_%s.ms' % rung
    open(path, 'w').write(out)
    print("WROTE %s (%d bytes) sat_mults=%s tie_degs=%s" %
          (path, len(out), allmults,
           [sp.Poly(t_, *ts).total_degree() for t_ in ties]))
    return path, ties, rab, ts, y, (D1, (D2 if rung != "m0" else None))

def main():
    rung = sys.argv[1]
    path, ties, rab, ts, y, Dpair = build_rung(rung)
    fout = '/tmp/m33_%s.out' % rung
    pr = subprocess.run([MSOLVE, "-P", "2", "-f", path, "-o", fout],
                        env=MSOLVE_ENV, capture_output=True, timeout=1800)
    print("msolve rc=%d" % pr.returncode)
    for i in (1, 2):
        gout = '/tmp/m33_%s_grade%d.out' % (rung, i)
        gr = subprocess.run(["python3", os.path.normpath(HERE + '/../anyrur_grade.py'),
                             fout, gout], capture_output=True, text=True)
        print(gr.stdout.strip() if gr.returncode == 0 else
              "GRADE_FAIL\n" + gr.stderr[-500:])
    h1 = hashlib.sha256(open('/tmp/m33_%s_grade1.out' % rung, 'rb').read()).hexdigest()
    h2 = hashlib.sha256(open('/tmp/m33_%s_grade2.out' % rung, 'rb').read()).hexdigest()
    print("GRADES_X2_IDENTICAL" if h1 == h2 else "GRADES_DIFFER", h1[:16])

main()
