#!/usr/bin/env python3
"""m33_reads.py -- 3b.3 M4 reads on the M-B factors file: const/lead square
classes (norm law) + f(z^2) irreducibility per component (pointwise-h).
Deterministic; run twice for x2. Usage: m33_reads.py FACTORS_FILE OUTPATH"""
import sys, math, ast, hashlib
sys.path.insert(0, '/home/wlloyd/Lloyd_Engine_V4/portfolio/campaigns/shape_witness')
import flint

def sq(n):
    n = abs(n); r = math.isqrt(n); return r * r == n

def main():
    src, outp = sys.argv[1], sys.argv[2]
    h = hashlib.sha256(open(src, 'rb').read()).hexdigest()[:16]
    facs = []
    for line in open(src):
        line = line.strip()
        if line.startswith('deg='):
            facs.append(ast.literal_eval(line.split(' coeffs=', 1)[1]))
    out = ["src=%s sha16=%s n_factors=%d" % (src, h, len(facs))]
    P = L = 1
    for c in facs:
        P *= int(c[0]); L *= int(c[-1])
    out.append("abs_const_w_square=%s sign_const=%+d abs_lead_w_square=%s "
               "sign_lead=%+d norm_class_trivial_pos=%s" %
               (sq(P), 1 if P > 0 else -1, sq(L), 1 if L > 0 else -1,
                sq(P * L) and P * L > 0))
    out.append("per_factor_const_sq=%s" % [sq(int(c[0])) for c in facs])
    out.append("per_factor_lead_sq=%s" % [sq(int(c[-1])) for c in facs])
    for c in facs:
        deg = len(c) - 1
        cz2 = []
        for x in c:
            cz2.extend([int(x), 0])
        f = flint.fmpz_poly(cz2[:-1])
        _, parts = f.factor()
        degs = sorted(q.degree() for q, e in parts)
        out.append("fz2 deg=%d -> %s %s" %
                   (deg, degs, "SPLITS(h exists)" if len(degs) > 1
                    else "irreducible(theta not square)"))
    out.append("M33_READS_DONE")
    open(outp, 'w').write("\n".join(out) + "\n")
    print("\n".join(out))

main()
