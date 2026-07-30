#!/usr/bin/env python3
"""Stage 6 gate B: defining-function gauge and intrinsic (gauge-free)
packaging of the singularity rates (PO-22 completion, Theorem 6.4 replay).

  Q1  divisor-order invariance under a FULL unit change of defining function
      z = (v0(y) + v1(y) z') z' — order fixed, coefficient scales by v0^-k
      only (v1 invisible at the principal layer): parity and generic faces.
  Q2  intrinsic proper-distance gauges (no defining function at all):
        parity face:  lim R d^2   = -m(m+5)/4        (m = 1: -3/2)
        generic face: lim R d^3/2 = Theta A^-1/4 / 2^(3/2)
      verified exactly on symbolic models.
"""
import sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("/", 1)[0] + "/off_diagonal_germs")
from curvlib import scalar_curvature, leading_laurent

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


z, y = sp.symbols("z y", positive=True)
zp = sp.Symbol("zp", positive=True)
B0, A1c, P0c, P1c, A2c = sp.symbols("B0 A1 P0 P1 A2", positive=True)
v0, v1 = sp.symbols("v0 v1", nonzero=True)

# ---- Q1 full unit change ------------------------------------------------------
for name, g0, kk, cexp in (
    ("parity k=4", sp.diag(B0 * z**2, A1c / z**2), 4, -6 / B0),
    ("generic k=3", sp.diag(A2c * z**2, P0c + P1c * z), 3, P1c / (P0c * A2c)),
):
    sub = {z: (v0 + v1 * zp) * zp}
    dz = sp.diff(sub[z], zp)
    J = sp.Matrix([[dz, 0], [0, 1]])
    gn = J.T * g0.subs(sub) * J
    Rn = scalar_curvature(gn, [zp, y])
    o, c = leading_laurent(Rn, zp)
    check(f"Q1 {name}: order invariant under full unit change", o == -kk)
    check(f"Q1 {name}: coefficient = base * v0^-{kk}, v1 invisible",
          sp.simplify(c - cexp / v0**kk) == 0)

# ---- Q2 intrinsic rates ---------------------------------------------------------
# parity m=1: d = (sqrt(B)/2) z^2 + O(z^4); R d^2 -> -6/4 = -3/2
g_par = sp.diag(B0 * z**2, A1c / z**2)
R_par = sp.cancel(scalar_curvature(g_par, [z, y]))
d_par = sp.sqrt(B0) / 2 * z**2
lim_par = sp.limit(sp.simplify(R_par * d_par**2), z, 0)
check("Q2 parity intrinsic rate: lim R d^2 = -3/2 (= -m(m+5)/4, m=1)",
      lim_par == sp.Rational(-3, 2))

# generic m=1: Theta = P1/P0; d = (sqrt(A2)/2) z^2 + O(z^3); R d^(3/2) -> Theta A2^(-1/4)/2^(3/2)
g_gen = sp.diag(A2c * z**2, P0c + P1c * z)
R_gen = sp.cancel(scalar_curvature(g_gen, [z, y]))
d_gen = sp.sqrt(A2c) / 2 * z**2
lim_gen = sp.limit(sp.simplify(R_gen * d_gen ** sp.Rational(3, 2)), z, 0)
target = (P1c / P0c) * A2c ** sp.Rational(-1, 4) / 2 ** sp.Rational(3, 2)
check("Q2 generic intrinsic rate: lim R d^(3/2) = Theta A^(-1/4)/2^(3/2)",
      sp.simplify(lim_gen - target) == 0)

print()
if failures:
    print("STAGE 6B GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 6B GATE PASSED: defining-function freedom fully quotiented; "
      "intrinsic singularity rates recovered exactly.")
