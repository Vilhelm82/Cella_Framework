#!/usr/bin/env python3
"""screen_slices.py -- verified-prime rational-point screen for Rabinowitsch RURs.
Banked S-2026-07-05 (supersedes the ad-hoc screen4 scanner; same methodology).

Usage:  python3 screen_slices.py SLICE [SLICE ...]     # e.g. 3 4
        python3 screen_slices.py --selftest

Method (= rabinowitsch_records/screen4.log methodology):
  Parse /tmp/rab_s{s}.out ONCE with rur_tools.parse_stream_exact (validated
  tokenizer, exact ints). Extract dim, ideal_deg, lf, and w. Gates:
    P1 (structure): dim == 0, else ABORT slice (screen only sound for 0-dim).
    P2 (good prime, PER PRIME): lead(w) mod p != 0  [degree preserved].
        P2 GATES P3 -- no root count is computed or cited from a P2-fail prime.
    P3 (root count): #distinct roots of w in F_p = deg(gcd(x^p - x, w mod p)),
        powmod by hand-rolled square-and-multiply, gcd by Euclid-over-%
        (rur_tools.safe_gcd). Never nmod_poly.gcd().
  Certificate [PROVEN, rur_tools docstring]: rational root's denominator
  divides lead(w); P2 => the root reduces mod p; zero roots at one good
  prime => zero rational roots => zero rational tie points on the slice.
  Verdict: CERTIFIED_EMPTY if any good prime yields 0 roots; else OPEN
  (min good-prime count = upper bound on # rational points).
Primes: deterministic sympy nextprime chain from 576460752303424600, first 6,
  each asserted prime (composite-modulus defect rule: assert isprime, always).
Output is deterministic (no timestamps) for byte-stability x2 grading.
"""
import sys, hashlib
sys.path.insert(0, '/home/wlloyd/Lloyd_Engine_V4/portfolio/campaigns/shape_witness')
import rur_tools as RT
from sympy import isprime, nextprime
import flint

PRIME_SEED = 576460752303424600
N_PRIMES = 6

def prime_pool():
    ps, p = [], PRIME_SEED
    for _ in range(N_PRIMES):
        p = int(nextprime(p))
        assert isprime(p), "modulus not prime"
        ps.append(p)
    return ps

def pow_mod(base, e, mod, p):
    r = flint.nmod_poly([1], p)
    b = base % mod
    while e:
        if e & 1:
            r = (r * b) % mod
        b = (b * b) % mod
        e >>= 1
    return r

def count_roots(w_exact, p):
    """P2+P3 for one prime. Returns ('P2_FAIL', None) or ('OK', count)."""
    wl = [c % p for c in w_exact]
    if wl[-1] == 0:
        return ('P2_FAIL', None)
    wp = flint.nmod_poly(wl, p)
    x = flint.nmod_poly([0, 1], p)
    g = RT.safe_gcd(pow_mod(x, p, wp, p) - x, wp)
    return ('OK', g.degree())

def screen_slice(si, primes):
    path = '/tmp/rab_s%d.out' % si
    h = hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]
    parsed = RT.parse_stream_exact(path)
    dim = parsed[0]
    print("s%d out_sha16=%s dim=%d" % (si, h, dim))
    if dim != 0:
        print("s%d P1_FAIL: dim=%d != 0 -- SCREEN ABORTED FOR SLICE" % (si, dim))
        return
    B = RT.blocks_of(parsed)
    w = B["w"]
    print("s%d ideal_deg=%d deg_w=%d lf=%s vars=%s" %
          (si, B["ideal_deg"], len(w) - 1, B["lf"], B["vars"]))
    counts = []
    for p in primes:
        status, c = count_roots(w, p)
        if status == 'P2_FAIL':
            print("s%d p=%d: P2_FAIL (lead vanishes) -- excluded" % (si, p))
        else:
            print("s%d p=%d: roots %d" % (si, p, c))
            counts.append((p, c))
    zero = [p for (p, c) in counts if c == 0]
    if zero:
        print("s%d VERDICT: CERTIFIED_EMPTY (zero-root good prime %d)" % (si, zero[0]))
    elif counts:
        print("s%d VERDICT: OPEN (min good-prime count %d)" % (si, min(c for _, c in counts)))
    else:
        print("s%d VERDICT: NO_GOOD_PRIMES -- extend pool" % si)

def selftest():
    import ast
    s = "[0, [0, 4, 12, ['t1','t2','t3','y'], [0,0,0,1], [1, [[3, [-6, 11, -6, 1]], [1, [1]], [[[1, [0]], 1]]]]]]"
    a = RT._make_value(s, int)()
    b = ast.literal_eval(s)
    assert a == b, "exact parse != literal_eval"
    p = prime_pool()[0]
    w = [-6, 11, -6, 1]              # (x-1)(x-2)(x-3): expect 3 roots, all p
    st, c = count_roots(w, p)
    assert (st, c) == ('OK', 3), "cubic root count failed: %s %s" % (st, c)
    st, c = count_roots([0, 1], p)   # w = x: expect 1 root
    assert (st, c) == ('OK', 1), "linear root count failed"
    st, c = count_roots([1, p], p)   # lead == 0 mod p: expect P2_FAIL
    assert st == 'P2_FAIL', "P2 gate failed to fire"
    print("SELFTEST_PASS primes=%s" % prime_pool())

if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        selftest()
    else:
        primes = prime_pool()
        print("prime pool: %s" % primes)
        for a in sys.argv[1:]:
            screen_slice(int(a), primes)
        print("SCREEN_DONE slices=%s" % sys.argv[1:])
