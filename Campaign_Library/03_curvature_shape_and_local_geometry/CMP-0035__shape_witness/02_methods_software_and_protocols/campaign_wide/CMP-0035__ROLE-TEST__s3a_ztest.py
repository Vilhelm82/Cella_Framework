#!/usr/bin/env python3
"""s3a_ztest.py -- SPLIT_PROBE Stage 3a battery (predecl A2).
Modes:
  ztest      -- SP.11: for slices 1 and 8, factor f_i(z^2) over Z for both
                components. IRREDUCIBLE deg 704 <=> theta not a square in K_i
                (no h on that component). REDUCIBLE 352+352 <=> sqrt(theta)
                in K_i (h exists there).
  constclass -- SP.12: for slices 0..8, is const(f1)*const(f2) a perfect
                square (up to sign)? Fixes the Q*/(Q*)^2 class of N(D1*D2).
Deterministic; run twice for byte-stability x2.
"""
import sys, ast, math
sys.set_int_max_str_digits(0)
BASE = '/home/wlloyd/Lloyd_Engine_V4/portfolio/campaigns/shape_witness'
import flint

def load(si):
    fs = []
    for line in open('%s/rabinowitsch_records/s%d_factors.txt' % (BASE, si)):
        if line.startswith('deg='):
            fs.append(ast.literal_eval(line.split('coeffs=')[1]))
    assert len(fs) == 2 and all(len(f) == 353 for f in fs)
    return fs

def zsquare(f):
    g = [0] * (2 * len(f) - 1)
    for k, a in enumerate(f):
        g[2 * k] = a
    return g

def ztest():
    hold = True
    for si in (1, 8):
        for k, f in enumerate(load(si)):
            g = zsquare(f)
            assert len(g) - 1 == 704
            content, parts = flint.fmpz_poly(g).factor()
            degs = sorted(q.degree() for q, _ in parts)
            verdict = "IRREDUCIBLE_704 (theta NOT square in K)" if degs == [704] \
                else "REDUCIBLE %s (sqrt(theta) IN K -- h exists on component)" % degs
            if degs != [704]: hold = False
            print("s%d f%d: f(z^2) -> %s" % (si, k + 1, verdict))
    print("SP.11 %s (prediction: irreducible everywhere)" % ("HOLDS" if hold else "FAILS"))
    print("ZTEST_DONE")

def constclass():
    for si in range(9):
        f1, f2 = load(si)
        c = abs(f1[0] * f2[0])
        r = math.isqrt(c)
        print("s%d: |const(f1)*const(f2)| perfect_square=%s (digits %d)" %
              (si, r * r == c, len(str(c))))
    print("CONSTCLASS_DONE")

if __name__ == '__main__':
    if sys.argv[1] == 'ztest': ztest()
    elif sys.argv[1] == 'constclass': constclass()
