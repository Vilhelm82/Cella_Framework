#!/usr/bin/env python3
"""split_probe.py -- Stage 1 battery for SPLIT_PROBE_PREDECL (S-2026-07-05).
Modes:
  stats    -- Q1 Frobenius statistics for all 16 factors over 120 primes.
              Grades SP.1/SP.2 (sanity, K-SP1 armed), SP.3 (parity match),
              SP.4 (lcm match), SP.5 (fixed-point variance, MEASURED).
  v3trace  -- Q3 3-adic trace of the actual pipeline objects per slice.
              Grades SP.6.
  selftest -- known-answer checks on small polynomials.
Deterministic output (no timestamps); run twice for byte-stability x2.
Factors are read from the banked rabinowitsch_records/s{si}_factors.txt.
Every modulus asserted prime (standing rule).
"""
import sys, ast, math
sys.set_int_max_str_digits(0)
BASE = '/home/wlloyd/Lloyd_Engine_V4/portfolio/campaigns/shape_witness'
sys.path.insert(0, BASE)
import flint
from sympy import isprime, nextprime

N_PRIMES = 120
PRIME_SEED = 576460752303424600
DEG = 352

def prime_chain(n, seed=PRIME_SEED):
    ps, p = [], seed
    for _ in range(n):
        p = int(nextprime(p)); assert isprime(p), "modulus not prime"
        ps.append(p)
    return ps

def load_factors(si):
    fs = []
    for line in open('%s/rabinowitsch_records/s%d_factors.txt' % (BASE, si)):
        if line.startswith('deg='):
            fs.append(ast.literal_eval(line.split('coeffs=')[1]))
    assert len(fs) == 2 and all(len(f) - 1 == DEG for f in fs)
    return fs

def frob_type(coeffs, p, deg=DEG):
    """Cycle type of Frobenius on the roots of coeffs mod p.
    Returns (status, type): status in OK / P2_FAIL / RAMIFIED."""
    wl = [c % p for c in coeffs]
    if wl[-1] == 0:
        return ('P2_FAIL', None)
    fac = flint.nmod_poly(wl, p).factor()[1]
    if any(e > 1 for _, e in fac):
        return ('RAMIFIED', None)
    t = sorted(q.degree() for q, _ in fac)
    assert sum(t) == deg, "SP.1 VIOLATION: type sums to %d" % sum(t)
    return ('OK', t)

def type_stats(t, deg=DEG):
    nroots = sum(1 for d in t if d == 1)
    parity = (deg - len(t)) % 2          # 0 = even permutation
    l = 1
    for d in t: l = math.lcm(l, d)
    return nroots, parity, l

def stats():
    primes = prime_chain(N_PRIMES)
    print("split_probe stats: %d primes, chain seed %d" % (N_PRIMES, PRIME_SEED))
    sp3_all, sp4_all = True, True
    for si in range(8):
        f1, f2 = load_factors(si)
        agg = [{'n': 0, 's': 0, 'ss': 0, 'odd': 0} for _ in range(2)]
        good = ram = p2f = pmatch = lmatch = 0
        mism = []
        for p in primes:
            r1, r2 = frob_type(f1, p), frob_type(f2, p)
            if 'P2_FAIL' in (r1[0], r2[0]): p2f += 1; continue
            if 'RAMIFIED' in (r1[0], r2[0]): ram += 1; continue
            good += 1
            st = [type_stats(r1[1]), type_stats(r2[1])]
            for k in range(2):
                nr, par, _ = st[k]
                agg[k]['n'] += 1; agg[k]['s'] += nr; agg[k]['ss'] += nr * nr
                agg[k]['odd'] += par
            if st[0][1] == st[1][1]: pmatch += 1
            else: mism.append(('par', p))
            if st[0][2] == st[1][2]: lmatch += 1
            else: mism.append(('lcm', p))
        means, varis = [], []
        for k in range(2):
            m = agg[k]['s'] / agg[k]['n']
            v = agg[k]['ss'] / agg[k]['n'] - m * m
            means.append(m); varis.append(v)
        print("s%d good=%d ram=%d p2fail=%d | mean_fp=(%.3f,%.3f) var_fp=(%.3f,%.3f) odd_frac=(%.3f,%.3f) | parity_match=%d/%d lcm_match=%d/%d" %
              (si, good, ram, p2f, means[0], means[1], varis[0], varis[1],
               agg[0]['odd'] / good, agg[1]['odd'] / good, pmatch, good, lmatch, good))
        if mism[:8]: print("s%d mismatches (first 8): %s" % (si, mism[:8]))
        if pmatch != good: sp3_all = False
        if lmatch != good: sp4_all = False
        if not (0.5 <= means[0] <= 1.5 and 0.5 <= means[1] <= 1.5):
            print("K-SP1 TRIP: s%d mean fixed points out of band" % si); sys.exit(2)
    print("SP.1 PASS (all types summed to %d; asserts silent)" % DEG)
    print("SP.2 PASS (all means in band)")
    print("SP.3 %s (parity match at every good prime, every slice)" % ("PASS" if sp3_all else "FAIL"))
    print("SP.4 %s (lcm match at every good prime, every slice)" % ("PASS" if sp4_all else "FAIL"))
    print("SP.5 MEASURED (variances above)")
    print("STATS_DONE")

def v3_of(fr):
    n, d = fr.numerator, fr.denominator
    k = 0
    while d % 3 == 0: d //= 3; k += 1
    m = 0
    while n and n % 3 == 0: n //= 3; m += 1
    return m - k

def v3trace():
    import hunt_v2_msolve as R
    import t4_probe as T
    import sympy as sp
    from fractions import Fraction as Fr
    from math import lcm
    t1s, t2s, t3s, ys = sp.symbols('t1 t2 t3 y')
    gvec = R.g
    GG = sum(Fr(a) * Fr(a) for a in gvec)
    print("v3(GG) = %d   (GG = |g|^2)" % v3_of(GG))
    flagged = []
    for si in range(8):
        sl = R.B.SLATES[si]
        pv = [[Fr(x.numerator, x.denominator) for x in R.perp(w)] for w in sl]
        perp_v3 = [v3_of(x) for w in pv for x in w if x != 0]
        pu1, pv1, pu2, pv2, pe_ = [[sp.Rational(x) for x in w] for w in pv]
        U1 = [a + t1s * b for a, b in zip(pu1, pe_)]
        U2 = [a + t2s * b + t3s * c for a, b, c in zip(pu2, pe_, pv1)]
        D1 = sp.expand(1 + sum(x * x for x in U1) * sum(y * y for y in pv1) - sum(x * y for x, y in zip(U1, pv1)) ** 2)
        D2 = sp.expand(1 + sum(x * x for x in U2) * sum(y * y for y in pv2) - sum(x * y for x, y in zip(U2, pv2)) ** 2)
        dco = [Fr(c.p, c.q) for c in sp.Poly(D1, t1s, t2s, t3s).coeffs()] + \
              [Fr(c.p, c.q) for c in sp.Poly(D2, t1s, t2s, t3s).coeffs()]
        d_v3 = [v3_of(x) for x in dco if x != 0]
        sat = T.saturated_polys(si)
        Ls = []
        for P in sat:
            L = 1
            for c in P.values(): L = lcm(L, int(sp.Rational(c).q))
            Ls.append(v3_of(Fr(L)))
        rabL = 1
        for c in sp.Poly(sp.expand(ys * D1 * D2 - 1), t1s, t2s, t3s, ys).coeffs():
            rabL = lcm(rabL, sp.Rational(c).q)
        anyv3 = (min(perp_v3) != 0 or max(perp_v3) != 0 or min(d_v3) != 0 or
                 max(d_v3) != 0 or any(Ls) or v3_of(Fr(rabL)) != 0)
        if anyv3: flagged.append(si)
        print("s%d: perp v3 range [%d,%d] | D-coeff v3 range [%d,%d] | sat clearing v3 %s | rab clearing v3 %d" %
              (si, min(perp_v3), max(perp_v3), min(d_v3), max(d_v3), Ls, v3_of(Fr(rabL))))
    print("SP.6 %s (flagged slices = %s; prediction {3,4})" %
          ("PASS" if flagged == [3, 4] else "FAIL", flagged))
    print("V3TRACE_DONE")

def selftest():
    assert prime_chain(3, seed=10) == [11, 13, 17]
    st, t = frob_type([-6, 11, -6, 1], 13, deg=3)     # (x-1)(x-2)(x-3)
    assert (st, t) == ('OK', [1, 1, 1]), (st, t)
    assert type_stats(t, deg=3) == (3, 0, 1)
    st, t = frob_type([1, 0, 1], 13, deg=2)           # x^2+1, 13 = 1 mod 4
    assert (st, t) == ('OK', [1, 1]), (st, t)
    st, t = frob_type([1, 0, 1], 19, deg=2)           # 19 = 3 mod 4 -> inert
    assert (st, t) == ('OK', [2]), (st, t)
    assert type_stats(t, deg=2) == (0, 1, 2)          # 0 roots, ODD, lcm 2
    st, t = frob_type([1, 13], 13, deg=1)             # lead kills mod 13
    assert st == 'P2_FAIL'
    st, t = frob_type([1, 2, 1], 13, deg=2)           # (x+1)^2 ramified
    assert st == 'RAMIFIED'
    print("SELFTEST_PASS")

def crosscheck():
    """SP.8 + SP.9: lcm-collision within-slice pairs vs cross-slice baseline;
    joint parity 2x2 per slice. Same 120-prime chain as stats."""
    primes = prime_chain(N_PRIMES)
    lcms, pars = {}, {}
    for si in range(8):
        f1, f2 = load_factors(si)
        for k, f in ((0, f1), (1, f2)):
            L, P = [], []
            for p in primes:
                st, t = frob_type(f, p)
                if st != 'OK':
                    L.append(None); P.append(None); continue
                _, par, l = type_stats(t)
                L.append(l); P.append(par)
            lcms[(si, k)] = L; pars[(si, k)] = P
    keys = sorted(lcms)
    win_hit = win_tot = x_hit = x_tot = 0
    for a in range(len(keys)):
        for b in range(a + 1, len(keys)):
            ka, kb = keys[a], keys[b]
            hits = tot = 0
            for x, y in zip(lcms[ka], lcms[kb]):
                if x is None or y is None: continue
                tot += 1; hits += (x == y)
            if ka[0] == kb[0]: win_hit += hits; win_tot += tot
            else: x_hit += hits; x_tot += tot
    print("SP.8: within-slice lcm collisions %d/%d (rate %.5f) | cross-slice %d/%d (rate %.5f)" %
          (win_hit, win_tot, win_hit / win_tot, x_hit, x_tot, x_hit / x_tot))
    for si in range(8):
        c = [[0, 0], [0, 0]]
        for x, y in zip(pars[(si, 0)], pars[(si, 1)]):
            if x is None or y is None: continue
            c[x][y] += 1
        print("SP.9 s%d joint parity [ee,eo;oe,oo] = [%d,%d;%d,%d]" %
              (si, c[0][0], c[0][1], c[1][0], c[1][1]))
    print("CROSSCHECK_DONE")

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stats': stats()
    elif mode == 'v3trace': v3trace()
    elif mode == 'crosscheck': crosscheck()
    elif mode == 'selftest': selftest()
    else: raise SystemExit("mode?")
