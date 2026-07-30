#!/usr/bin/env python3
"""Stage 5 gate C: curvature initial forms for the framed class (PO-20).

  V0  harness validation: unit 2-sphere R=+2; flat R^3 R=0; pure parity model
      R = -m(m+5)/B z^-4 exactly for m=1 (2D) and m=2 (3D)
  V1  finite candidate support: on random exact class members the curvature
      pole order obeys  ord_z R >= 2(min p - max p) - 2  (crude universal
      bound), and the leading term is an exact rational Laurent datum
  V2  E = I reduction: the diagonal member reproduces the generic order-3 law
      R = (1/A2)(P1/P0) z^-3 + O(z^-2)  (m = 1 transverse direction)
  V3  rechart-pullback member: pulling a diagonal normal form back through a
      genuine boundary-adapted diffeo keeps the pole order (order 3), i.e. the
      class contains off-diagonal presentations of the diagonal laws with the
      SAME valuation (seed of Stage 6 naturality)
"""
import random
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

# ---- V0 harness validation ----------------------------------------------------
th, ph = sp.symbols("theta phi", positive=True)
g_sphere = sp.diag(1, sp.sin(th) ** 2)
R_sph = sp.simplify(scalar_curvature(g_sphere, [th, ph]))
check("V0 unit two-sphere R = +2 (frozen sign convention)", R_sph == 2)

g_flat = sp.diag(1, 1, 1)
check("V0 flat R^3 has R = 0", scalar_curvature(g_flat, [z, y, w]) == 0)

Bsym = sp.Symbol("B", positive=True)
A1 = sp.Symbol("A1", positive=True)
g_par1 = sp.diag(Bsym * z**2, A1 / z**2)
R1 = sp.cancel(scalar_curvature(g_par1, [z, y]))
check("V0 pure parity m=1: R = -6/(B z^4) exactly",
      sp.simplify(R1 + 6 / (Bsym * z**4)) == 0)

A2s = sp.Symbol("A2", positive=True)
g_par2 = sp.diag(Bsym * z**2, A1 / z**2, A2s / z**2)
R2 = sp.cancel(scalar_curvature(g_par2, [z, y, w]))
check("V0 pure parity m=2: R = -14/(B z^4) exactly, amplitudes drop out",
      sp.simplify(R2 + 14 / (Bsym * z**4)) == 0)

# ---- V1 random exact members ----------------------------------------------------
rng = random.Random(777)
ok_bound = True
results = []
for trial in range(3):
    while True:
        E0 = sp.Matrix(2, 2, lambda i, j: sp.Rational(rng.randint(-2, 2), rng.randint(1, 2)))
        if E0.det() != 0:
            break
    E1 = sp.Matrix(2, 2, lambda i, j: sp.Rational(rng.randint(-1, 1), rng.randint(1, 2)))
    Ex = E0 + z * E1
    px = [rng.choice([2, 3]), rng.choice([-2, -1, 0])]
    hx = [sp.Rational(rng.randint(1, 4), rng.randint(1, 2)) + z * rng.randint(0, 2)
          for _ in range(2)]
    gx = Ex.T * sp.diag(z**px[0] * hx[0], z**px[1] * hx[1]) * Ex
    R = scalar_curvature(gx, [z, y])
    if R == 0:
        continue
    o, c = leading_laurent(R, z)
    bound = 2 * (min(px) - max(px)) - 2
    results.append((px, o, c))
    if o < bound:
        ok_bound = False
check("V1 universal bound ord R >= 2(min p - max p) - 2 on all members", ok_bound)
for px, o, c in results:
    print(f"      (p = {px}: leading term {c} * z^{o})")

# ---- V2 E = I generic collapse reduction -----------------------------------------
A2c, P0, P1 = sp.symbols("A2 P0 P1", positive=True)
g_gen = sp.diag(A2c * z**2, P0 + P1 * z)
Rg = scalar_curvature(g_gen, [z, y])
og, cg = leading_laurent(Rg, z)
check("V2 diagonal generic collapse: order exactly 3", og == -3)
check("V2 leading coefficient = (P1/P0)/A2 exactly",
      sp.simplify(cg - P1 / (P0 * A2c)) == 0)

# ---- V3 rechart pullback keeps the valuation --------------------------------------
# diagonal normal form in (zp, yp); rechart z = zp*(1 + yp), y = yp + zp^2
zp, yp = sp.symbols("zp yp", positive=True)
gdiag = sp.diag(3 * z**2, 2 + z + y)
sub = {z: zp * (1 + yp), y: yp + zp**2}
J = sp.Matrix([[sp.diff(sub[z], zp), sp.diff(sub[z], yp)],
               [sp.diff(sub[y], zp), sp.diff(sub[y], yp)]])
gpull = J.T * gdiag.subs(sub) * J
check("V3 pulled-back metric is genuinely off-diagonal", sp.simplify(gpull[0, 1]) != 0)
Rd = scalar_curvature(gdiag, [z, y])
Rp = scalar_curvature(gpull, [zp, yp])
od, cd = leading_laurent(Rd.subs(y, sp.Rational(1, 3)), z)
op, cp = leading_laurent(Rp.subs(yp, sp.Rational(1, 3)), zp)
check("V3 pole order invariant under boundary-adapted rechart (3 = 3)",
      od == op == -3)
print(f"      (native coeff {cd}, recharted coeff {cp} at y = 1/3)")

print()
if failures:
    print("STAGE 5C GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 5C GATE PASSED: harness validated; finite support bound holds; "
      "diagonal law recovered at E = I; rechart pullback preserves order.")
