#!/usr/bin/env python3
"""Stage 5 gate B: inverse-metric and determinant valuations for the framed
class (PO-19), with the noncancellation stratum named and a jump witness.

  I1  det g = z^(sum p_i) * unit,  unit|_D = (det E|_D)^2 * prod h_i|_D != 0
      (exact, symbolic 3x3)
  I2  inverse valuation law: ord_z (g^{-1})_{ij} >= -max_k p_k, with equality
      on the noncancellation stratum  E^{-1}_{i k*} E^{-1}_{j k*} |_D != 0
      (k* the index of the maximal exponent); random exact 3x3 members
  I3  JUMP WITNESS (falsification item 4, inside the class): an E with
      E^{-1}_{i k*}|_D = 0 shifts the naive inverse valuation on entry (i,i)
      while det g keeps its rigid valuation.
"""
import random
import sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from curvlib import leading_laurent

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


z = sp.Symbol("z", positive=True)

# ---- I1 symbolic 3x3 ---------------------------------------------------------
E = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"e{i}{j}"))
h = [sp.Symbol(f"h{i}", nonzero=True) for i in range(3)]
p = [3, 1, 0]
D = sp.diag(*[z**p[i] * h[i] for i in range(3)])
g = E.T * D * E
detg = sp.factor(g.det())
check("I1 det g = z^(p0+p1+p2) (det E)^2 h0 h1 h2 exactly",
      sp.simplify(detg - z**sum(p) * (E.det())**2 * h[0] * h[1] * h[2]) == 0)

# ---- I2 random exact members ---------------------------------------------------
rng = random.Random(555)


def rand_unit_matrix():
    while True:
        M0 = sp.Matrix(3, 3, lambda i, j: sp.Rational(rng.randint(-3, 3), rng.randint(1, 3)))
        if M0.det() != 0:
            break
    M1 = sp.Matrix(3, 3, lambda i, j: sp.Rational(rng.randint(-2, 2), rng.randint(1, 3)))
    return M0 + z * M1


ok_bound = ok_generic = True
for trial in range(4):
    Ex = rand_unit_matrix()
    hx = [sp.Rational(rng.randint(1, 5), rng.randint(1, 3)) + z * rng.randint(-2, 2)
          for _ in range(3)]
    px = sorted(rng.sample(range(0, 5), 3), reverse=True)
    Dx = sp.diag(*[z**px[i] * hx[i] for i in range(3)])
    gx = Ex.T * Dx * Ex
    ginv = gx.inv()
    kstar = px.index(max(px))
    Einv0 = Ex.inv().subs(z, 0)
    for i in range(3):
        for j in range(i, 3):
            entry = sp.cancel(ginv[i, j])
            if entry == 0:
                continue
            o, c = leading_laurent(entry, z)
            if o < -max(px):
                ok_bound = False
            noncancel = Einv0[i, kstar] * Einv0[j, kstar] != 0
            if noncancel and o != -max(px):
                ok_generic = False
check("I2 inverse valuation bound ord >= -max p on all random members", ok_bound)
check("I2 equality on the noncancellation stratum (E^-1 leading entries nonzero)",
      ok_generic)

# ---- I3 jump witness ------------------------------------------------------------
# choose E so that (E^{-1})_{2,0}|_D = 0: then entry (2,2) of g^{-1} misses the
# dominant z^{-p0} channel and its valuation jumps upward.
Ei = sp.Matrix([[1, 0, 2], [0, 1, 0], [0, 0, 1]])   # E^{-1} has (2,0) entry 0
Ew = Ei.inv()                                        # class member frame
hw = [sp.Integer(1), sp.Integer(1), sp.Integer(1)]
pw = [4, 1, 0]
Dw = sp.diag(*[z**pw[i] * hw[i] for i in range(3)])
gw = Ew.T * Dw * Ew
ginvw = gw.inv()
o22, _ = leading_laurent(sp.cancel(ginvw[2, 2]), z)
o00, _ = leading_laurent(sp.cancel(ginvw[0, 0]), z)
odet, _ = leading_laurent(gw.det(), z)
check("I3 dominant entry (0,0) achieves ord = -4", o00 == -4)
check("I3 entry (2,2) JUMPS above the naive -4 bound (cancellation stratum)",
      o22 > -4)
check("I3 determinant valuation stays rigid at +5 despite the jump", odet == 5)
print(f"      (witness: ord g^-1_(0,0) = {o00}, ord g^-1_(2,2) = {o22}, ord det = {odet})")

print()
if failures:
    print("STAGE 5B GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 5B GATE PASSED: inverse/determinant valuation laws exact; "
      "cancellation stratum named algebraically and witnessed.")
