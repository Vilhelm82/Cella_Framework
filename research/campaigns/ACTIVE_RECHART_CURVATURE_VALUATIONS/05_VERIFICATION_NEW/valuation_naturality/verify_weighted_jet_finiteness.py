#!/usr/bin/env python3
"""Stage 6 gate C: finite weighted-jet determination and transverse-derivative
exclusion, with ARBITRARY symbolic function coefficients (PO-24, PO-25).

This is an INDEPENDENT replay of the LEAD-7 variable-transverse theorem with
a different engine (direct Christoffel/Ricci on function-coefficient metrics
via curvlib), not the packaged Laurent-jet verifier.

  J1  generic face, m = 2, all coefficients arbitrary functions of y:
        R = (P1/P0 + R1/R0)/A2 * z^-3 + O(z^-2)
      leading coefficient contains NO derivative of any coefficient function
      and does not see A3, P2, R2.
  J2  reflection face, m = 2, arbitrary functions of y:
        R = -14/B * z^-4 + O(z^-2)
      independent of B4, C10, C20 and of the transverse amplitudes C1, C2;
      no transverse derivatives at leading order.
"""
import sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("/", 1)[0] + "/off_diagonal_germs")
from curvlib import scalar_curvature, diagonal_scalar_curvature, leading_laurent

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


z, y, w = sp.symbols("z y w", positive=True)
A2f, A3f, P0f, P1f, P2f, R0f, R1f, R2f = [
    sp.Function(n)(y) for n in ("A2", "A3", "P0", "P1", "P2", "R0", "R1", "R2")]

# ---- J0 engine cross-check --------------------------------------------------------
g0 = [z**2 * (3 + z), 2 + z + y, 1 + 2 * z]
check("J0 directional-channel formula == tensor engine (Lame identity, exact)",
      sp.simplify(sp.together(scalar_curvature(sp.diag(*g0), [z, y, w])
                              - diagonal_scalar_curvature(g0, [z, y, w]))) == 0)

# ---- J1 generic face ------------------------------------------------------------
g = [A2f * z**2 + A3f * z**3,
     P0f + P1f * z + P2f * z**2,
     R0f + R1f * z + R2f * z**2]
R = diagonal_scalar_curvature(g, [z, y, w])
o, c = leading_laurent(R, z)
target = (P1f / P0f + R1f / R0f) / A2f
check("J1 generic: order exactly 3", o == -3)
check("J1 generic: coefficient = (P1/P0 + R1/R0)/A2 exactly",
      sp.simplify(c - target) == 0)
check("J1 generic: no transverse derivatives, no A3/P2/R2 in the coefficient",
      not any(isinstance(a, sp.Derivative) for a in sp.preorder_traversal(c))
      and all(f not in c.free_symbols | set(c.atoms(sp.Function))
              for f in (A3f, P2f, R2f)))

# ---- J2 reflection face -----------------------------------------------------------
Bf, B4f, C1f, C2f, C10f, C20f = [
    sp.Function(n)(y) for n in ("B", "B4", "C1", "C2", "C10", "C20")]
g2 = [Bf * z**2 + B4f * z**4,
      C1f / z**2 + C10f,
      C2f / z**2 + C20f]
R2m = diagonal_scalar_curvature(g2, [z, y, w])
o2, c2 = leading_laurent(R2m, z)
check("J2 reflection: order exactly 4", o2 == -4)
check("J2 reflection: coefficient = -14/B exactly (amplitudes drop out)",
      sp.simplify(c2 + 14 / Bf) == 0)
check("J2 reflection: no transverse derivatives, no B4/C10/C20 at leading order",
      not any(isinstance(a, sp.Derivative) for a in sp.preorder_traversal(c2))
      and all(f not in set(c2.atoms(sp.Function))
              for f in (B4f, C10f, C20f, C1f, C2f)))

print()
if failures:
    print("STAGE 6C GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 6C GATE PASSED: finite weighted-jet determination and "
      "transverse-derivative exclusion replayed with an independent engine.")
