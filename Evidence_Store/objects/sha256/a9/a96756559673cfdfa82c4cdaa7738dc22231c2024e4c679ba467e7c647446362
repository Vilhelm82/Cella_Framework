#!/usr/bin/env python3
"""stage2_build.py -- builds the two Stage-2 .ms systems (SPLIT_PROBE A1).
Modes:
  sform SI  -> /tmp/sform_s{SI}.ms : Rabinowitsch system + variable s with
               generator s - (3*t1 + 5*t2 + 7*t3), s LAST in variable order
               (msolve's separating preference). Tests SP.7' (lead-squareness
               under a generic separating element).
  s8        -> /tmp/rab_s8.ms : fresh slate = SLATES[0] with u1[0] += 1/7,
               appended as index 8; full Rabinowitsch build. Tests SP.10
               (slate-genericity of the split + lead laws).
Deterministic output; the .ms file sha is the pin for each system.
"""
import sys
from fractions import Fraction as Fr
BASE = '/home/wlloyd/Lloyd_Engine_V4/portfolio/campaigns/shape_witness'
sys.path.insert(0, BASE)
import hunt_v2_msolve as R
import t4_probe as T
import sympy as sp
from math import lcm

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

def D_polys(si, t1s, t2s, t3s):
    sl = R.B.SLATES[si]
    pv = [[sp.Rational(x.numerator, x.denominator) for x in R.perp(w)] for w in sl]
    pu1, pv1, pu2, pv2, pe_ = pv
    U1 = [a + t1s * b for a, b in zip(pu1, pe_)]
    U2 = [a + t2s * b + t3s * c for a, b, c in zip(pu2, pe_, pv1)]
    D1 = sp.expand(1 + sum(x * x for x in U1) * sum(y * y for y in pv1) - sum(x * y for x, y in zip(U1, pv1)) ** 2)
    D2 = sp.expand(1 + sum(x * x for x in U2) * sum(y * y for y in pv2) - sum(x * y for x, y in zip(U2, pv2)) ** 2)
    return D1, D2

def sat_strings(si):
    return [R.poly_to_ms(p) for p in T.saturated_polys(si)]

def build_sform(si):
    t1s, t2s, t3s, ys, ss = sp.symbols('t1 t2 t3 y s')
    D1, D2 = D_polys(si, t1s, t2s, t3s)
    rab = gen_to_ms(ys * D1 * D2 - 1, (t1s, t2s, t3s, ys), ('t1', 't2', 't3', 'y'))
    sgen = "s-3*t1-5*t2-7*t3"
    out = "t1,t2,t3,y,s\n0\n" + ",\n".join(sat_strings(si) + [rab, sgen]) + "\n"
    open('/tmp/sform_s%d.ms' % si, 'w').write(out)
    print("WROTE /tmp/sform_s%d.ms (%d bytes)" % (si, len(out)))

def build_s8():
    sl0 = R.B.SLATES[0]
    slate8 = [list(v) for v in sl0]
    slate8[0][0] = Fr(slate8[0][0]) + Fr(1, 7)
    R.B.SLATES.append(slate8)
    assert len(R.B.SLATES) == 9
    t1s, t2s, t3s, ys = sp.symbols('t1 t2 t3 y')
    D1, D2 = D_polys(8, t1s, t2s, t3s)
    rab = gen_to_ms(ys * D1 * D2 - 1, (t1s, t2s, t3s, ys), ('t1', 't2', 't3', 'y'))
    out = "t1,t2,t3,y\n0\n" + ",\n".join(sat_strings(8) + [rab]) + "\n"
    open('/tmp/rab_s8.ms', 'w').write(out)
    print("WROTE /tmp/rab_s8.ms (%d bytes)" % len(out))

def build_dloc(si, which):
    """3b.2 (predecl A4): adjoin u = 1/D_{which} on the honest Rabinowitsch
    scheme; u LAST so msolve separates by it. Grades N(D_which) square-class."""
    t1s, t2s, t3s, ys, us = sp.symbols('t1 t2 t3 y u')
    D1, D2 = D_polys(si, t1s, t2s, t3s)
    rab = gen_to_ms(ys * D1 * D2 - 1, (t1s, t2s, t3s, ys), ('t1', 't2', 't3', 'y'))
    D = D1 if which == 1 else D2
    uloc = gen_to_ms(us * D - 1, (t1s, t2s, t3s, us), ('t1', 't2', 't3', 'u'))
    out = "t1,t2,t3,y,u\n0\n" + ",\n".join(sat_strings(si) + [rab, uloc]) + "\n"
    open('/tmp/dloc_s%d_D%d.ms' % (si, which), 'w').write(out)
    print("WROTE /tmp/dloc_s%d_D%d.ms (%d bytes)" % (si, which, len(out)))

if __name__ == "__main__":
    if sys.argv[1] == "sform": build_sform(int(sys.argv[2]))
    elif sys.argv[1] == "s8": build_s8()
    elif sys.argv[1] == "dloc": build_dloc(int(sys.argv[2]), int(sys.argv[3]))
