#!/usr/bin/env python3
"""m33d_pd1.py -- PD.1: subset-square relations among the four component
norm classes c_i = class(lead_i * const_i) of the banked M-B factors.
(Squarefree parts of ~5000-digit integers are infeasible; the exact,
computable mechanism data = which subset products are squares, + small-prime
valuations mod 2 up to 10^6.) Deterministic; run twice for x2.
Usage: m33d_pd1.py FACTORS OUTPATH"""
import sys, math, ast, hashlib, itertools

def sq(n):
    n = abs(n); r = math.isqrt(n); return r * r == n

def main():
    src, outp = sys.argv[1], sys.argv[2]
    h = hashlib.sha256(open(src, 'rb').read()).hexdigest()[:16]
    vals, degs = [], []
    for line in open(src):
        line = line.strip()
        if line.startswith('deg='):
            c = ast.literal_eval(line.split(' coeffs=', 1)[1])
            vals.append(int(c[0]) * int(c[-1]))
            degs.append(len(c) - 1)
    out = ["src sha16=%s degs=%s" % (h, degs)]
    out.append("signs=%s" % [1 if v > 0 else -1 for v in vals])
    for r in range(1, len(vals) + 1):
        for S in itertools.combinations(range(len(vals)), r):
            p = 1
            for i in S: p *= vals[i]
            if sq(p) and p > 0:
                out.append("SQUARE_SUBSET %s (degs %s)" %
                           (list(S), [degs[i] for i in S]))
    smalls = {}
    for i, v in enumerate(vals):
        vp = {}
        m = abs(v)
        for p in range(2, 1000000):
            if p * p > m and m > 1: break
            e = 0
            while m % p == 0: m //= p; e += 1
            if e % 2: vp[p] = e
        smalls[i] = vp
        out.append("comp%d deg=%d odd-val small primes: %s%s" %
                   (i, degs[i], sorted(vp), " (large cofactor)" if m > 1 else ""))
    out.append("PD1_DONE")
    open(outp, 'w').write("\n".join(out) + "\n")
    print("\n".join(out))

main()
