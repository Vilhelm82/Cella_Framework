#!/usr/bin/env python3
"""a6_sign_const_grade.py -- SPLIT_PROBE ADDENDUM A6 grader (SP.14/SP.15).
Reads banked factors files (anyrur_grade/slice_factor format), emits
per-system: content, per-factor sign(lead)/sign(const)/|const| square check,
product const square-class, and the even-degree norm sign read
sign(lead_i*const_i). Deterministic; run twice for byte-stability x2.
Usage: a6_sign_const_grade.py OUTPATH FILE1 FILE2 ...
Defs first, dispatch last (def-after-main rule)."""
import sys, hashlib, math, ast
sys.set_int_max_str_digits(0)

def is_sq(n):
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n

def parse(path):
    content = None
    facs = []
    for line in open(path):
        line = line.strip()
        if line.startswith("content="):
            content = int(line.split("=", 1)[1])
        elif line.startswith("deg="):
            head, coeffs = line.split(" coeffs=", 1)
            deg = int(head.split()[0].split("=")[1])
            mult = int(head.split()[1].split("=")[1])
            c = ast.literal_eval(coeffs)
            facs.append((deg, mult, int(c[0]), int(c[-1])))
    return content, facs

def main():
    outp = sys.argv[1]
    out = []
    for path in sys.argv[2:]:
        h = hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]
        content, facs = parse(path)
        name = path.split('/')[-1]
        ok = (len(facs) == 2 and
              all(d == 352 and m == 1 for d, m, _, _ in facs))
        out.append("system=%s sha16=%s content=%d sanity_2x352=%s" %
                   (name, h, content, ok))
        signs = []
        for i, (d, m, c0, cl) in enumerate(facs):
            sN = 1 if cl * c0 > 0 else -1
            signs.append(sN)
            out.append("  f%d: sign_lead=%+d sign_const=%+d "
                       "abs_const_digits=%d abs_const_square=%s "
                       "sign_leadxconst=%+d" %
                       (i + 1, 1 if cl > 0 else -1, 1 if c0 > 0 else -1,
                        len(str(abs(c0))), is_sq(abs(c0)), sN))
        if len(facs) == 2:
            p = facs[0][2] * facs[1][2]
            out.append("  const_product_abs_square=%s sign_const_product=%+d "
                       "sign_norm_product=%+d" %
                       (is_sq(abs(p)), 1 if p > 0 else -1, signs[0] * signs[1]))
    out.append("A6_DONE")
    open(outp, 'w').write("\n".join(out) + "\n")
    print("\n".join(out))

main()
