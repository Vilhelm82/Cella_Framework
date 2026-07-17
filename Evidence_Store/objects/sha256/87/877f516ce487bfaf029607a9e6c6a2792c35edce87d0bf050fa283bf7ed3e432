#!/usr/bin/env python3
"""s1_factor.py -- exact Z-factorization of the slice-1 Rabinowitsch eliminant.
Banked S-2026-07-05. The decisive slice-1 move per HANDOFF_S2026-07-03.

Certificate logic [PROVEN modulo the RUR contract]:
  msolve's RUR for a 0-dim radical ideal is a bijection solutions <-> roots
  of the squarefree eliminant w, with theta = value of the separating linear
  form (here lf = y). A rational tie point P => theta = y(P) rational
  => w has a rational root => (after content strip) a degree-1 factor in Z[x].
  Contrapositive: NO degree-1 factor in the exact factorization
  => slice 1 CERTIFIED rational-point-free.
  If degree-1 factors DO appear: each gives an exact rational theta; the RUR
  coordinate formula x_i = -v_i(theta)/(den_i * w'(theta)) reconstructs an
  exact QQ candidate point -- the witness path. (Reconstruction + exact tie
  verification is a FOLLOW-UP step, not performed here.)
Either way the irreducible factor degrees expose the field structure of the
tie points (which number fields the 704 solutions live in).

Output: argv[1] = summary path (degree spectrum, multiplicities, rational
roots in full). Full factor coefficients -> same path + '.factors' (large).
Deterministic; run twice for byte-stability x2.
"""
import sys, hashlib
sys.path.insert(0, '/home/wlloyd/Lloyd_Engine_V4/portfolio/campaigns/shape_witness')
import rur_tools as RT
import flint
from fractions import Fraction

def main():
    summary_path = sys.argv[1]
    src = '/tmp/rab_s1.out'
    h = hashlib.sha256(open(src, 'rb').read()).hexdigest()[:16]
    parsed = RT.parse_stream_exact(src)
    dim = parsed[0]
    assert dim == 0, "P1_FAIL: dim != 0"
    B = RT.blocks_of(parsed)
    w = B["w"]
    out = ["s1 src_sha16=%s ideal_deg=%d deg_w=%d lf=%s" %
           (h, B["ideal_deg"], len(w) - 1, B["lf"])]
    P = flint.fmpz_poly(w)
    content, parts = P.factor()
    degs = sorted(q.degree() for q, _ in parts)
    out.append("content=%s n_factors=%d" % (content, len(parts)))
    out.append("degree_spectrum=%s" % degs)
    out.append("multiplicities=%s" % sorted(e for _, e in parts))
    lin = [(q, e) for q, e in parts if q.degree() == 1]
    if not lin:
        out.append("VERDICT: NO_LINEAR_FACTOR => s1 CERTIFIED rational-point-free")
    else:
        out.append("VERDICT: %d LINEAR FACTOR(S) -- rational theta candidates:" % len(lin))
        for q, e in lin:
            a, b = int(q[0]), int(q[1])
            out.append("  theta = %s  (mult %d)" % (Fraction(-a, b), e))

    fac_path = summary_path + '.factors'
    with open(fac_path, 'w') as f:
        f.write("content=%s\n" % content)
        for q, e in sorted(parts, key=lambda t: t[0].degree()):
            cs = [int(q[i]) for i in range(q.degree() + 1)]
            f.write("deg=%d mult=%d coeffs=%s\n" % (q.degree(), e, cs))
    fh = hashlib.sha256(open(fac_path, 'rb').read()).hexdigest()[:16]
    out.append("factors_file_sha16=%s" % fh)
    out.append("S1FAC_DONE")
    open(summary_path, 'w').write("\n".join(out) + "\n")
    print("\n".join(out))

if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    main()
