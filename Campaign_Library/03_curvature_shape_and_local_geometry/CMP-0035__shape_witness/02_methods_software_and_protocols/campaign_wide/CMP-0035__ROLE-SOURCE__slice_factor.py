#!/usr/bin/env python3
"""slice_factor.py -- exact Z-factorization + split diagnostics for a
Rabinowitsch slice eliminant. Banked S-2026-07-05; generalizes s1_factor.py
(the slice-1 instance already ran byte-stable x2, summary sha 95376b40...,
factors sha16 5c5a6d02).

Usage: python3 slice_factor.py SLICE OUTPATH

Deterministic pipeline:
  1. parse /tmp/rab_s{SLICE}.out via rur_tools.parse_stream_exact; P1 gate dim==0.
  2. exact factorization of the eliminant w over Z (flint fmpz_poly.factor).
  3. report content, degree spectrum, multiplicities.
  4. rational-root verdict: any degree-1 factor => exact rational theta
     candidates listed (witness path); none => CERTIFIED rational-point-free
     (RUR bijection: rational tie point => rational value of separating
     form y => rational root of w => integer linear factor; see s1_factor.py
     docstring for the full argument).
  5. if the spectrum has exactly 2 factors: lead-equality and |const|-equality
     tests (the s1 anomaly: non-isomorphic factor fields, EQUAL 9694-digit
     leads -- norm-balance reading, [INTERPRETATION]).
  6. per-factor diagnostics over the standard verified-prime pool
     (= screen_slices.prime_pool, every modulus asserted prime): root counts,
     pairwise gcd degrees, full mod-p splitting types, pattern-equality flag
     (identical types at all good primes ~ isomorphic fields; one honest
     disagreement => non-isomorphic, modulo index divisibility caveat).
Writes summary -> OUTPATH, full factor coefficients -> OUTPATH + '.factors'
(sha16 of the factors file recorded in the summary). Run twice for x2.
"""
import sys, hashlib
sys.path.insert(0, '/home/wlloyd/Lloyd_Engine_V4/portfolio/campaigns/shape_witness')
import rur_tools as RT
import screen_slices as SS
import flint
from fractions import Fraction

def main():
    si, summary_path = int(sys.argv[1]), sys.argv[2]
    src = '/tmp/rab_s%d.out' % si
    h = hashlib.sha256(open(src, 'rb').read()).hexdigest()[:16]
    parsed = RT.parse_stream_exact(src)
    assert parsed[0] == 0, "P1_FAIL: dim != 0"
    B = RT.blocks_of(parsed)
    w = B["w"]
    out = ["s%d src_sha16=%s ideal_deg=%d deg_w=%d lf=%s" %
           (si, h, B["ideal_deg"], len(w) - 1, B["lf"])]
    content, parts = flint.fmpz_poly(w).factor()
    parts = sorted(parts, key=lambda t: (t[0].degree(), str(t[0])))
    degs = [q.degree() for q, _ in parts]
    out.append("content=%s n_factors=%d" % (content, len(parts)))
    out.append("degree_spectrum=%s" % degs)
    out.append("multiplicities=%s" % [e for _, e in parts])
    lin = [(q, e) for q, e in parts if q.degree() == 1]
    if not lin:
        out.append("VERDICT: NO_LINEAR_FACTOR => s%d CERTIFIED rational-point-free" % si)
    else:
        out.append("VERDICT: %d LINEAR FACTOR(S) -- rational theta candidates:" % len(lin))
        for q, e in lin:
            out.append("  theta = %s  (mult %d)" % (Fraction(-int(q[0]), int(q[1])), e))
    if len(parts) == 2:
        (q1, _), (q2, _) = parts
        out.append("lead_equal=%s" % (q1[q1.degree()] == q2[q2.degree()]))
        out.append("abs_const_equal=%s" % (abs(int(q1[0])) == abs(int(q2[0]))))

    primes = SS.prime_pool()
    out.append("prime_pool=%s" % primes)
    for p in primes:
        row, pats, reds = [], [], []
        for k, (q, _) in enumerate(parts):
            cs = [int(q[i]) for i in range(q.degree() + 1)]
            st, c = SS.count_roots(cs, p)
            if st == 'P2_FAIL':
                row.append("f%d:P2_FAIL" % k); pats.append(None); reds.append(None)
                continue
            row.append("f%d:%d" % (k, c))
            qp = flint.nmod_poly([x % p for x in cs], p)
            reds.append(qp)
            pats.append(sorted(g.degree() for g, _ in qp.factor()[1]))
        gcds = []
        for a in range(len(reds)):
            for b in range(a + 1, len(reds)):
                if reds[a] is not None and reds[b] is not None:
                    gcds.append(RT.safe_gcd(reds[a], reds[b]).degree())
        eq = all(pats[0] == pt for pt in pats[1:]) if pats and all(
            pt is not None for pt in pats) else 'NA'
        out.append("p=%d roots[%s] pairwise_gcd_degs=%s patterns_equal=%s" %
                   (p, " ".join(row), gcds, eq))
        for k, pt in enumerate(pats):
            if pt is not None:
                out.append("  p=%d f%d split_type=%s" % (p, k, pt))

    fac_path = summary_path + '.factors'
    with open(fac_path, 'w') as f:
        f.write("content=%s\n" % content)
        for q, e in parts:
            cs = [int(q[i]) for i in range(q.degree() + 1)]
            f.write("deg=%d mult=%d coeffs=%s\n" % (q.degree(), e, cs))
    fh = hashlib.sha256(open(fac_path, 'rb').read()).hexdigest()[:16]
    out.append("factors_file_sha16=%s" % fh)
    out.append("SLICEFAC_DONE s%d" % si)
    open(summary_path, 'w').write("\n".join(out) + "\n")
    print("\n".join(out))

if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    main()
