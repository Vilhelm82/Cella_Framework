#!/usr/bin/env python3
"""Stage 5 gate D: constructed counterexamples (falsification programme items
4, 5; PO-21 strata).

  X1  leading-coefficient cancellation ON the nominal generic stratum
      (falsification item 5): generic quadratic collapse with
      P1/P0 + R1/R0 = 0 drops the order below 3 — "order three with zero
      coefficient" is falsified as a reporting style.
  X2  frame activity: an E-dressing with no coordinate-change origin changes
      the curvature valuation relative to its diagonal core (E is NOT
      removable; the class is genuinely larger than recharted diagonals).
  X3  degenerate stratum bookkeeping: the X1 drop lands exactly one layer
      down (order 2), witnessing the cancellation hierarchy's "inspect the
      next layer" rule rather than an informal exception.
"""
import sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from curvlib import scalar_curvature, leading_laurent

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


z, y, w = sp.symbols("z y w", positive=True)

# ---- X1/X3 cancellation on the nominal generic stratum -------------------------
# m = 2 transverse: P-drift +2/P0=1, R-drift -2/R0=1  =>  sum of drifts zero
g_cancel = sp.diag(5 * z**2, 1 + 2 * z + 3 * z**2, 1 - 2 * z)
Rc = scalar_curvature(g_cancel, [z, y, w])
oc, cc = leading_laurent(Rc, z)
check("X1 drift-balanced generic collapse drops below order 3", oc > -3)
check("X3 the drop lands exactly at order 2 (next layer, not an exception)",
      oc == -2 and cc != 0)
print(f"      (cancellation witness: leading term {cc} * z^{oc})")

# control: unbalanced drifts give order 3
g_ctrl = sp.diag(5 * z**2, 1 + 2 * z, 1 + 2 * z)
octl, cctl = leading_laurent(scalar_curvature(g_ctrl, [z, y, w]), z)
check("X1 control: unbalanced drifts keep exact order 3 with coeff (1/A2)*sum",
      octl == -3 and sp.simplify(cctl - sp.Rational(4, 5)) == 0)

# ---- X2 frame activity -----------------------------------------------------------
# diagonal core: flat after substitution (z^2 dz^2 + dy^2)
g_core = sp.diag(z**2, sp.Integer(1))
R_core = scalar_curvature(g_core, [z, y])
check("X2 diagonal core is flat (R = 0)", sp.simplify(R_core) == 0)
# dress with a z-dependent shear frame (no diffeo origin):
Esh = sp.Matrix([[1, z], [0, 1]])
g_dress = sp.expand(Esh.T * g_core * Esh)
R_dress = sp.cancel(scalar_curvature(g_dress, [z, y]))
od, cd = leading_laurent(R_dress, z) if R_dress != 0 else (None, 0)
check("X2 shear-dressed member is NOT flat — frame E is curvature-active",
      R_dress != 0)
print(f"      (dressed curvature leading term: {cd} * z^{od})")

print()
if failures:
    print("STAGE 5D GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 5D GATE PASSED: cancellation strata witnessed and typed; "
      "frame activity proved — E-dressing is genuinely new geometry.")
