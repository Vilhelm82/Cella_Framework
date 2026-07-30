#!/usr/bin/env python3
"""Stage 7 gate: the diagonal and corner calculus as STRICT corollaries of the
framed class at E = I (Gate 7).

  G7.1  master quadric: for pure monomial single-face germs
        g = diag(x^p0, x^p1, ..., x^pm),  R = C(p) x^-(p0+2)  EXACTLY,
        for a battery of exponent vectors in dimensions 2,3,4 — including the
        scalar-flat locus p_alpha = 4/(m+1) (C = 0, R == 0)
  G7.2  closed corner formula (Thm 7.4): symbolic exponents + unit functions
        h_i(s): R equals the three-term formula with A (7.3), B (7.4), L_s (7.5)
  G7.3  Example 8.1: R = -6 x^-4 - 6 y^-4 exactly; weighted valuation along
        x = rho eps^a, y = eps^b gives kappa = max(4a, 4b) with front
        coefficient -6(rho^-4 + 1)
  G7.4  KN corner sector exponents: A = -84, B = -12, vertices (-4,2), (2,-4),
        Newton wedge m(a) = max(4a-2, 4-2a)
  G7.5  pure parity models m = 1..4: R = -m(m+5)/B x^-4 exactly
"""
import sys
import itertools
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("/", 1)[0] + "/off_diagonal_germs")
from curvlib import diagonal_scalar_curvature

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


x = sp.Symbol("x", positive=True)


def master_quadric(p):
    p0, rest = p[0], p[1:]
    return -sp.Rational(1, 2) * (sum(q**2 for q in rest)
                                 + sum(a * b for a, b in itertools.combinations(rest, 2))
                                 - (p0 + 2) * sum(rest))


# ---- G7.1 --------------------------------------------------------------------
ok = True
battery = [(2, -2), (2, -2, -2), (2, -2, -2, -2), (3, 1), (0, 2), (2, 0, 1),
           (4, -1, 2), (0, sp.Rational(4, 2)), (0, 2, 2), (0, sp.Rational(4, 3), sp.Rational(4, 3))]
for p in battery:
    m = len(p) - 1
    coords = [x] + [sp.Symbol(f"y{i}", positive=True) for i in range(m)]
    entries = [x**p[0]] + [x**p[i + 1] for i in range(m)]
    R = sp.cancel(sp.together(diagonal_scalar_curvature(entries, coords)))
    want = master_quadric(list(p)) * x**(-(p[0] + 2))
    if sp.simplify(R - want) != 0:
        ok = False
        print(f"      mismatch at p = {p}: got {R}, want {want}")
check("G7.1 master quadric exact for pure monomials, dims 2-4, incl. scalar-flat locus", ok)

# ---- G7.2 closed corner formula -----------------------------------------------
s, yv = sp.symbols("s y", positive=True)
p0, q0, p1, q1, p2, q2 = sp.symbols("p0 q0 p1 q1 p2 q2")
h0, h1, h2 = [sp.Function(f"h{i}")(s) for i in range(3)]
entries = [h0 * x**p0 * yv**q0, h1 * x**p1 * yv**q1, h2 * x**p2 * yv**q2]
R = diagonal_scalar_curvature(entries, [s, x, yv])
Acoef = -p0**2 + p0 * p1 - p0 * p2 + 2 * p0 + p1 * p2 - p2**2 + 2 * p2
Bcoef = -q0**2 + q0 * q2 - q0 * q1 + 2 * q0 + q2 * q1 - q1**2 + 2 * q1
a0, a1, a2 = sp.sqrt(h0), sp.sqrt(h1), sp.sqrt(h2)
l0, l1, l2 = [sp.diff(ai, s) / ai for ai in (a0, a1, a2)]
Ls = -2 / h0 * (sp.diff(a1, s, 2) / a1 + sp.diff(a2, s, 2) / a2
                - l0 * (l1 + l2) + l1 * l2)
Rformula = (Acoef / (2 * h1) * x**(-(p1 + 2)) * yv**(-q1)
            + Bcoef / (2 * h2) * x**(-p2) * yv**(-(q2 + 2))
            + Ls * x**(-p0) * yv**(-q0))
check("G7.2 closed three-dimensional corner formula (7.2)-(7.5) exact, symbolic",
      sp.simplify(sp.together(R - Rformula)) == 0)

# ---- G7.3 Example 8.1 -----------------------------------------------------------
yv2 = sp.Symbol("y2", positive=True)
g81 = [x**-2 * yv2**-2, x**2, yv2**2]
R81 = sp.cancel(sp.together(diagonal_scalar_curvature(g81, [s, x, yv2])))
check("G7.3 Example 8.1: R = -6 x^-4 - 6 y^-4 exactly",
      sp.simplify(R81 + 6 / x**4 + 6 / yv2**4) == 0)
rho, eps, aw = sp.symbols("rho epsilon a", positive=True)
Rpath = R81.subs({x: rho * eps**aw, yv2: eps})
check("G7.3 weighted valuation: front -6(rho^-4 + 1) on the balanced face a=1",
      sp.simplify(Rpath.subs(aw, 1) * eps**4 + 6 * (rho**-4 + 1)) == 0)

# ---- G7.4 KN corner sector --------------------------------------------------------
pv = {p0: -6, q0: 0, p1: 2, q1: -2, p2: -2, q2: 2}
Akn = Acoef.subs(pv)
Bkn = Bcoef.subs(pv)
check("G7.4 KN sector raw master coefficients A = -84, B = -12",
      Akn == -84 and Bkn == -12)
V1 = (-(pv[p1] + 2), -pv[q1])
V2 = (-pv[p2], -(pv[q2] + 2))
check("G7.4 vertices V_x = (-4, 2), V_y = (2, -4)", V1 == (-4, 2) and V2 == (2, -4))
avar = sp.Symbol("a", positive=True)
wedge = sp.Max(-(V1[0] * avar + V1[1]), -(V2[0] * avar + V2[1]))
check("G7.4 Newton wedge m(a) = max(4a-2, 4-2a)",
      sp.simplify(wedge - sp.Max(4 * avar - 2, 4 - 2 * avar)) == 0)

# ---- G7.5 pure parity all m -------------------------------------------------------
Bs = sp.Symbol("B", positive=True)
ok = True
for m in (1, 2, 3, 4):
    coords = [x] + [sp.Symbol(f"t{i}", positive=True) for i in range(m)]
    As = [sp.Symbol(f"Amp{i}", positive=True) for i in range(m)]
    entries = [Bs * x**2] + [As[i] / x**2 for i in range(m)]
    Rm = sp.cancel(sp.together(diagonal_scalar_curvature(entries, coords)))
    if sp.simplify(Rm + m * (m + 5) / (Bs * x**4)) != 0:
        ok = False
check("G7.5 pure parity R = -m(m+5)/B x^-4 exactly for m = 1,2,3,4", ok)

print()
if failures:
    print("STAGE 7 GATE FAILED:", failures)
    sys.exit(1)
print("GATE 7 PASSED: master quadric, corner formula, Example 8.1, KN sector, "
      "parity family — all strict corollaries at E = I, all exact.")
