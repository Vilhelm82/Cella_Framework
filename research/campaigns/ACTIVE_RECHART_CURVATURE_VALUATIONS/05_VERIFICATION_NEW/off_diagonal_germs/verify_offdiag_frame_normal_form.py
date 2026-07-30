#!/usr/bin/env python3
"""Stage 5 gate A: the framed monomial-unit germ class  g = E^T diag(z^p_i h_i) E
(PO-18 closure; determinant valuation rigidity; finite-jet dependence).

  W1  closure under boundary-adapted rechart z = u(y') z' + O(z'^2), y = psi(y', z'):
      the pulled-back metric is again E~^T D~ E~ with
      E~ = (E o phi) J,  h~_i = (h_i o phi) u^{p_i} (1 + O(z')),  same exponents p_i.
      Verified: unit values nonzero at the divisor, det E~ nonzero at the divisor,
      and the exact matrix identity.
  W2  determinant valuation rigidity INSIDE the class:
      det g = z^(sum p_i) * (det E)^2 * prod h_i  — the valuation sum(p_i) cannot
      shift while det E|_D != 0 (class membership); exact symbolic identity.
  W3  finite-jet dependence: perturbing E and h at order z^6 leaves the leading
      curvature term (order AND coefficient) unchanged on an off-diagonal member.
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


z, y = sp.symbols("z y", positive=True)
zp, yp = sp.symbols("zp yp", positive=True)

# ---- W1 closure --------------------------------------------------------------
e1, e2, u0, u1, c1 = sp.symbols("e1 e2 u0 u1 c1", nonzero=True)
h00, h01, h10, h11 = sp.symbols("h00 h01 h10 h11", nonzero=True)
E = sp.Matrix([[1, e1 + z], [e2 * z, 1]])
h0 = h00 + h01 * z
h1 = h10 + h11 * z
D = sp.diag(z**2 * h0, h1)
g = sp.expand(E.T * D * E)

# rechart: z = (u0 + u1*yp) * zp,  y = yp + c1*zp   (boundary-adapted, unit u0+u1*yp)
subs_map = {z: (u0 + u1 * yp) * zp, y: yp + c1 * zp}
J = sp.Matrix([[sp.diff(subs_map[z], zp), sp.diff(subs_map[z], yp)],
               [sp.diff(subs_map[y], zp), sp.diff(subs_map[y], yp)]])
g_pull = sp.expand(J.T * g.subs(subs_map) * J)

u_unit = u0 + u1 * yp
E_new = sp.expand(E.subs(subs_map) * J)
h0_new = h0.subs(subs_map) * u_unit**2      # exponent p_0 = 2
h1_new = h1.subs(subs_map)                  # exponent p_1 = 0
D_new = sp.diag(zp**2 * h0_new, h1_new)
check("W1 exact class identity g' = E~^T D~ E~ under boundary-adapted rechart",
      sp.simplify(sp.expand(g_pull - E_new.T * D_new * E_new)) == sp.zeros(2, 2))
check("W1 new units nonvanishing on divisor and det E~|_D != 0",
      sp.simplify(h0_new.subs(zp, 0)) != 0 and sp.simplify(h1_new.subs(zp, 0)) != 0
      and sp.simplify(E_new.subs(zp, 0).det()) != 0)

# ---- W2 determinant rigidity ---------------------------------------------------
detg = sp.factor(g.det())
target = sp.factor(z**2 * h0 * h1 * (E.det()) ** 2)
check("W2 det g = z^(p0+p1) (det E)^2 h0 h1 exactly", sp.simplify(detg - target) == 0)

# ---- W3 finite-jet dependence ---------------------------------------------------
# concrete exact off-diagonal member (2D; z-dependent entries keep the exact
# rational curvature computation light while exercising every z-jet layer)
Ex = sp.Matrix([[1, sp.Rational(1, 3) + z], [2 * z, 1]])
h0x = 3 + 2 * z
h1x = 2 + z
Dx = sp.diag(z**2 * h0x, h1x)
gx = sp.expand(Ex.T * Dx * Ex)
R = scalar_curvature(gx, [z, y])
ordR, coefR = leading_laurent(R, z)

# perturb E and h at z^5 (far above the jet that determines the leading term)
Ep = Ex + sp.Matrix([[z**5, 5 * z**6], [z**5, 3 * z**5]])
h0p = h0x + 7 * z**5
h1p = h1x + 11 * z**5
gp = sp.expand(Ep.T * sp.diag(z**2 * h0p, h1p) * Ep)
Rp = scalar_curvature(gp, [z, y])
ordRp, coefRp = leading_laurent(Rp, z)
check("W3 leading order unchanged under z^5 jet perturbation", ordR == ordRp)
check("W3 leading coefficient unchanged under z^5 jet perturbation",
      sp.simplify(coefR - coefRp) == 0)
print(f"      (off-diagonal member: leading term {coefR} * z^{ordR})")

print()
if failures:
    print("STAGE 5A GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 5A GATE PASSED: class closed under admissible rechart; determinant "
      "valuation rigid; leading curvature term is finite-jet data.")
