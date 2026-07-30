#!/usr/bin/env python3
"""PO-2/PO-3 falsification gate at jet order r=3, plus the CCE-8 finite-tower
naturality replay.

  H1  inverse law at r=3 on the generic symbolic three-role 3-jet
  H2  composition law at r=3, 4 roles, random exact jets
  H3  denominator locus at order 3 is a^5 (up to rational constants)
  H4  finite-tower naturality: truncating a 3-jet transport to order 2 equals
      transporting the truncated 2-jet  (tau_{3,2} t = t tau_{3,2}), generic
  H5  order-d inverse coefficients depend on no input coefficient above degree d
      (triangularity of the inverse recurrence)

Exit code 0 iff every gate passes.
"""
import random
import sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from jetlib import rechart, random_rational_jet, jets_equal, jet_coeff, truncate

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


# generic symbolic three-role 3-jet of the P-output chart
a, b, A, B, C = sp.symbols("a b A B C")
F30, F21, F12, F03 = sp.symbols("F30 F21 F12 F03")
D, S = sp.symbols("x0 x1")
jet3 = (a * D + b * S + A * D**2 / 2 + B * D * S + C * S**2 / 2
        + F30 * D**3 / 6 + F21 * D**2 * S / 2 + F12 * D * S**2 / 2 + F03 * S**3 / 6)
vars_P = {0: D, 1: S}

# H1 inverse law at r=3
jD, vD = rechart(jet3, vars_P, 2, 0, 3)
jP2, vP2 = rechart(jD, vD, 0, 2, 3)
check("H1 t^2 = e at r=3 on generic symbolic 3-jet",
      jets_equal(jet3, vars_P, jP2, vP2, 3))

# H2 composition at r=3, 4 roles, random exact jets
rng = random.Random(97)
ok = True
for _ in range(3):
    j0, v0 = random_rational_jet(4, 0, 3, rng)
    ja, va = rechart(j0, v0, 0, 1, 3)
    jab, vab = rechart(ja, va, 1, 2, 3)
    jc, vc = rechart(j0, v0, 0, 2, 3)
    if not jets_equal(jab, vab, jc, vc, 3):
        ok = False
check("H2 composition T_(1,2)T_(0,1) = T_(0,2) at r=3, 4 roles", ok)

# H3 denominator power at order 3 is a^5
ok = True
for exps in [(3, 0), (2, 1), (1, 2), (0, 3)]:
    c = jet_coeff(jD, [vD[2], vD[1]], exps)
    denom = sp.denom(sp.together(sp.cancel(c)))
    ratio = sp.simplify(denom / a**5)
    if not ratio.is_Rational or ratio == 0:
        ok = False
check("H3 order-3 denominators are exactly a^5", ok)

# H4 finite-tower naturality (CCE-8 replay): tau_{3,2}(t f) = t tau_{3,2}(f)
lhs = truncate(jD, [vD[2], vD[1]], 2)
jet2 = truncate(jet3, [D, S], 2)
rhs, vrhs = rechart(jet2, vars_P, 2, 0, 2)
check("H4 truncation commutes with active transposition (CCE-8 naturality)",
      jets_equal(lhs, vD, rhs, vrhs, 2))

# H5 triangularity: order-2 coefficients of the inverse never see F30..F03
ok = True
for exps in [(2, 0), (1, 1), (0, 2)]:
    c = jet_coeff(jD, [vD[2], vD[1]], exps)
    if any(s in c.free_symbols for s in (F30, F21, F12, F03)):
        ok = False
check("H5 inverse degree-d coefficients use no input coefficient above degree d", ok)

print()
if failures:
    print("GATE r=3 FAILED:", failures)
    sys.exit(1)
print("GATE r=3 PASSED: inverse, composition, a^5 denominators, finite-tower "
      "naturality, triangular dependence — all exact.")
