#!/usr/bin/env python3
"""PO-1..PO-4 falsification gate at jet order r=2.

Checks, in exact arithmetic:
  G1  identity law           T_(rho,rho) = id
  G2  inverse law            T_(sigma,rho) T_(rho,sigma) = id      (3 and 4 roles)
  G3  triple composition     T_(sigma,tau) T_(rho,sigma) = T_(rho,tau)
  G4  S3 relations at n=2:   s^2 = t^2 = e, (st)^3 = e  on the generic symbolic 2-jet
  G5  denominator locus:     order-2 rechart coefficients have denominator a^3 exactly
  G6  active/passive separation: passive input swap fixes the channel tuple,
      active transposition changes the jet (generic witness)
  G7  singular stratum typing: a = 0 raises a typed refusal, never a coerced value

Exit code 0 iff every gate passes.
"""
import random
import sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from jetlib import (rechart, generic_jet, random_rational_jet, jets_equal,
                    jet_coeff, truncate)

R = 2
failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


# ---------------------------------------------------------------- G1/G4/G5: generic symbolic, 3 roles
# roles: 0 = D, 1 = S, 2 = P ; start with P-output chart P = f(D,S)
a, b, A, B, C = sp.symbols("a b A B C")
D, S = sp.symbols("x0 x1")
jet_P = a * D + b * S + sp.Rational(1, 2) * A * D**2 + B * D * S + sp.Rational(1, 2) * C * S**2
vars_P = {0: D, 1: S}

# G1 identity
j_id, v_id = rechart(jet_P, vars_P, 2, 2, R)
check("G1 identity T_(P,P)=id", sp.expand(j_id - jet_P) == 0)

# active transposition t = (D P): rechart to the D-output chart
jet_D, vars_D = rechart(jet_P, vars_P, 2, 0, R)
# expected exact second-order transposition from Paper I (authority: dbp_orbit_calculus #sec:transpose)
P_, S_ = vars_D[2], vars_D[1]
expected_D = (P_ / a - b / a * S_
              - A / a**3 * P_**2 / 2 + (A * b - a * B) / a**3 * P_ * S_
              + (-A * b**2 + 2 * a * b * B - a**2 * C) / a**3 * S_**2 / 2)
check("Gate1 D-chart jet matches Paper I t-formulas exactly",
      sp.simplify(sp.expand(jet_D - expected_D)) == 0)

# G2 inverse: back to P-output
jet_P2, vars_P2 = rechart(jet_D, vars_D, 0, 2, R)
check("G2 t^2 = e (P->D->P restores the generic 2-jet)",
      jets_equal(jet_P, vars_P, jet_P2, vars_P2, R))

# G4 (st)^3 = e on the generic symbolic jet.
# Ordered chart state: (jet, vars, out, slots=[first input role, second input role]).
# s = passive swap of the two input SLOTS (jet unchanged as a polynomial);
# t = active transposition of the output with the FIRST input slot.
cur_jet, cur_vars, cur_out, slots = jet_P, vars_P, 2, [0, 1]
for _ in range(3):
    slots = [slots[1], slots[0]]                                   # s
    tgt = slots[0]                                                 # t
    cur_jet, cur_vars = rechart(cur_jet, cur_vars, cur_out, tgt, R)
    cur_out, slots = tgt, [cur_out, slots[1]]
# after 3 iterations of (s then t) starting from P|D,S we must be back at P|D,S
check("G4 (st)^3 = e on generic symbolic 2-jet",
      cur_out == 2 and slots == [0, 1]
      and jets_equal(jet_P, vars_P, cur_jet, cur_vars, R))


def input_swap(jet, variables):
    """passive relabelling s = (D S): swap role indices 0 and 1 (for G6)."""
    v0, v1 = variables[0], variables[1]
    tmp = sp.Symbol("tmp_swap")
    jet2 = jet.subs(v0, tmp).subs(v1, v0).subs(tmp, v1)
    return sp.expand(jet2), dict(variables)

# G5 denominator locus: all order-2 coefficients of jet_D over a^3 exactly
ok5 = True
for exps, mono in [((2, 0), "PP"), ((1, 1), "PS"), ((0, 2), "SS")]:
    coeff = jet_coeff(jet_D, [vars_D[2], vars_D[1]], exps)
    denom = sp.denom(sp.together(sp.cancel(coeff)))
    # denominator must be a^3 up to a rational combinatorial constant
    ratio = sp.simplify(denom / a**3)
    if not ratio.is_Rational or ratio == 0:
        ok5 = False
check("G5 order-2 denominators are exactly a^3 (localized rational closure)", ok5)

# ---------------------------------------------------------------- G2/G3: 4 roles, random exact jets
rng = random.Random(20260730)
ok2 = ok3 = True
for trial in range(4):
    jet0, vars0 = random_rational_jet(4, 3, R, rng)     # roles 0..3, output 3
    # inverse law on a random pair
    j1, v1 = rechart(jet0, vars0, 3, 1, R)
    j0b, v0b = rechart(j1, v1, 1, 3, R)
    if not jets_equal(jet0, vars0, j0b, v0b, R):
        ok2 = False
    # triple composition 3 -> 0 -> 2  vs  3 -> 2
    ja, va = rechart(jet0, vars0, 3, 0, R)
    jab, vab = rechart(ja, va, 0, 2, R)
    jc, vc = rechart(jet0, vars0, 3, 2, R)
    if not jets_equal(jab, vab, jc, vc, R):
        ok3 = False
check("G2 inverse law, 4 roles, random exact jets", ok2)
check("G3 exact overlap composition T_(s,t)T_(r,s)=T_(r,t), 4 roles", ok3)

# ---------------------------------------------------------------- G6 active/passive separation
subs_num = {a: 5, b: 7, A: 2, B: 3, C: 4}
jet_num = jet_P.subs(subs_num)
js, vs = input_swap(jet_num, vars_P)
# passive swap: jet coefficients permute but the SET of channel data is fixed;
# active transposition genuinely changes the numbers:
jd, vd = rechart(jet_num, vars_P, 2, 0, R)
A_D = 2 * jet_coeff(jd, [vd[2], vd[1]], (2, 0))
check("G6 active rechart changes the second jet (A -> -A/a^3 = -2/125)",
      sp.Rational(-2, 125) == sp.nsimplify(A_D) and jet_coeff(js, [vs[0], vs[1]], (2, 0)) * 2 == 4)

# ---------------------------------------------------------------- G7 singular stratum typing
jet_sing = 0 * D + 1 * S + sp.Rational(1, 2) * D**2   # df/dD = 0 at base point
try:
    rechart(jet_sing, {0: D, 1: S}, 2, 0, R)
    check("G7 singular stratum raises typed refusal", False)
except ZeroDivisionError:
    check("G7 singular stratum raises typed refusal", True)

print()
if failures:
    print("GATE r=2 FAILED:", failures)
    sys.exit(1)
print("GATE r=2 PASSED: identity, inverse, composition, S3, denominators, "
      "active/passive separation, singular typing — all exact.")
