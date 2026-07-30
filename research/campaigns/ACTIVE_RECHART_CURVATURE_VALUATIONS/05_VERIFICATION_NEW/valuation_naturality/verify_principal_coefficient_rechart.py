#!/usr/bin/env python3
"""Stage 6 gate A: pole-order invariance and the weight-k principal
coefficient law (PO-22, PO-23).

Convention (frozen ledger 6): if z' = u(y) z + O(z^2) with u|_D != 0 and
R = c(y) z^-k + O(z^-k+1), then c'(y) = u(y)^k c(y): the principal
coefficient is a section of the k-th power of the conormal dual, not a scalar.

  P1  parity face (k = 4, m = 1): rechart z = c(y) z' + k2(y) z'^2 replays
      Paper II Prop 6.3 exactly:
        R = -6/(B c^4) z'^-4 + 24 k2/(B c^5) z'^-3 + O(z'^-2)
      i.e. weight-4 coefficient law + parity-breaking odd term iff k2 != 0.
  P2  generic face (k = 3): under z = c(y) z', the coefficient transforms
      with weight 3: c' = (P1/P0)/A2 * c(y)^-3  (= u^3 c with u = 1/c).
  P3  only u|_D enters: adding the O(z^2) term k2(y) z'^2 leaves the
      PRINCIPAL coefficient unchanged (it feeds strictly higher orders).
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
c0, k2 = sp.symbols("c0 k2", nonzero=True)

# ---- P1 parity face, m = 1 ----------------------------------------------------
g_par = sp.diag(B0 * z**2, A1c / z**2)
sub = {z: c0 * zp + k2 * zp**2}
J = sp.Matrix([[sp.diff(sub[z], zp), 0], [0, 1]])
g_new = J.T * g_par.subs(sub) * J
Rn = sp.cancel(scalar_curvature(g_new, [zp, y]))
o4, c4 = leading_laurent(Rn, zp)
check("P1 recharted parity face keeps pole order 4", o4 == -4)
check("P1 weight-4 law: c' = -6/(B c0^4) exactly",
      sp.simplify(c4 + 6 / (B0 * c0**4)) == 0)
# next Laurent layer: subtract leading and re-extract
Rsub = sp.cancel(sp.together(Rn - c4 * zp**-4))
o3, c3 = leading_laurent(Rsub, zp)
check("P1 odd term 24 k2/(B c0^5) z'^-3 appears iff k2 != 0 (Prop 6.3 replay)",
      o3 == -3 and sp.simplify(c3 - 24 * k2 / (B0 * c0**5)) == 0)

# ---- P2 generic face, weight 3 --------------------------------------------------
g_gen = sp.diag(A2c * z**2, P0c + P1c * z)
subs2 = {z: c0 * zp}
J2 = sp.Matrix([[c0, 0], [0, 1]])
g2 = J2.T * g_gen.subs(subs2) * J2
R2 = scalar_curvature(g2, [zp, y])
og, cg = leading_laurent(R2, zp)
check("P2 generic face keeps pole order 3", og == -3)
check("P2 weight-3 law: c' = (P1/P0)/A2 * c0^-3 exactly",
      sp.simplify(cg - P1c / (P0c * A2c * c0**3)) == 0)

# ---- P3 principal coefficient sees only u|_D --------------------------------------
sub3 = {z: c0 * zp + k2 * zp**2}
J3 = sp.Matrix([[sp.diff(sub3[z], zp), 0], [0, 1]])
g3 = J3.T * g_gen.subs(sub3) * J3
R3 = scalar_curvature(g3, [zp, y])
og3, cg3 = leading_laurent(R3, zp)
check("P3 O(z^2) rechart term does not touch the principal coefficient",
      og3 == -3 and sp.simplify(cg3 - cg) == 0)

print()
if failures:
    print("STAGE 6A GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 6A GATE PASSED: pole order natural; principal coefficient is a "
      "weight-k conormal datum; only u|_D enters.")
