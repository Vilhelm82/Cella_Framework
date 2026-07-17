#!/usr/bin/env python3
"""anyrur_grade.py SRC OUTPATH -- factorization + split/lead-law grading for
an arbitrary RUR file (SPLIT_PROBE A1: grades SP.7' on sform outputs and
SP.10 on the s8 output; same logic as slice_factor.py, path-general).
Prints: header data, degree spectrum, multiplicities, rational-root verdict,
lead-equality, |const|-equality, lead(w) perfect-square check, factor sha.
Deterministic; run twice for byte-stability x2.
"""
import sys, hashlib, math
sys.set_int_max_str_digits(0)
sys.path.insert(0, '/home/wlloyd/Lloyd_Engine_V4/portfolio/campaigns/shape_witness')
import rur_tools as RT
import flint
from fractions import Fraction

def main():
    src, outp = sys.argv[1], sys.argv[2]
    h = hashlib.sha256(open(src, 'rb').read()).hexdigest()[:16]
    parsed = RT.parse_stream_exact(src)
    assert parsed[0] == 0, "P1_FAIL: dim != 0"
    B = RT.blocks_of(parsed)
    w = B["w"]
    out = ["src=%s sha16=%s ideal_deg=%d deg_w=%d lf=%s" %
           (src, h, B["ideal_deg"], len(w) - 1, B["lf"])]
    lw = w[-1]
    r = math.isqrt(abs(lw))
    out.append("lead_w_digits=%d lead_w_perfect_square=%s" %
               (len(str(abs(lw))), r * r == abs(lw) and lw > 0))

    content, parts = flint.fmpz_poly(w).factor()
    parts = sorted(parts, key=lambda t: (t[0].degree(), str(t[0])))
    degs = [q.degree() for q, _ in parts]
    out.append("content=%s n_factors=%d degree_spectrum=%s multiplicities=%s" %
               (content, len(parts), degs, [e for _, e in parts]))
    lin = [(q, e) for q, e in parts if q.degree() == 1]
    if not lin:
        out.append("VERDICT: NO_LINEAR_FACTOR => rational-point-free")
    else:
        out.append("VERDICT: %d LINEAR FACTOR(S):" % len(lin))
        for q, e in lin:
            out.append("  theta = %s (mult %d)" % (Fraction(-int(q[0]), int(q[1])), e))
    if len(parts) == 2:
        (q1, _), (q2, _) = parts
        l1, l2 = int(q1[q1.degree()]), int(q2[q2.degree()])
        g = math.gcd(l1, l2)
        out.append("lead_equal=%s abs_const_equal=%s reduced_lead_ratio=%d/%d" %
                   (l1 == l2, abs(int(q1[0])) == abs(int(q2[0])),
                    abs(l1 // g), abs(l2 // g)))
    fac_path = outp + '.factors'
    with open(fac_path, 'w') as f:
        f.write("content=%s\n" % content)
        for q, e in parts:
            f.write("deg=%d mult=%d coeffs=%s\n" %
                    (q.degree(), e, [int(q[i]) for i in range(q.degree() + 1)]))
    out.append("factors_file_sha16=%s" %
               hashlib.sha256(open(fac_path, 'rb').read()).hexdigest()[:16])
    out.append("ANYRUR_DONE")
    open(outp, 'w').write("\n".join(out) + "\n")
    print("\n".join(out))

if __name__ == '__main__':
    main()
