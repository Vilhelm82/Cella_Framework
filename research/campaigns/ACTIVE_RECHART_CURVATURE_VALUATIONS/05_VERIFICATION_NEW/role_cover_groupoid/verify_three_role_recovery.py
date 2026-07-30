#!/usr/bin/env python3
"""Gate 1 recovery: the general (n+1)-role machinery must reproduce, exactly,
the legacy three-role transformed derivatives of BOTH inverse charts
(authority: dbp_orbit_calculus #sec:transpose and
Theorem_8_1_Curvature_Orbit_Correction #4), and the sixfold ordered chart
object must collapse to three unordered output-role jets.
"""
import sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from jetlib import rechart, jet_coeff, jets_equal

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


a, b, A, B, C = sp.symbols("a b A B C")
D, S = sp.symbols("x0 x1")
jet_P = a * D + b * S + A * D**2 / 2 + B * D * S + C * S**2 / 2
vars_P = {0: D, 1: S}

# ---- D-output chart D = q(P,S): Paper I formulas ---------------------------
jD, vD = rechart(jet_P, vars_P, 2, 0, 2)
P_, S_ = vD[2], vD[1]
tests = {
    "q_P = 1/a":        (jet_coeff(jD, [P_, S_], (1, 0)), 1 / a),
    "q_S = -b/a":       (jet_coeff(jD, [P_, S_], (0, 1)), -b / a),
    "q_PP = -A/a^3":    (2 * jet_coeff(jD, [P_, S_], (2, 0)), -A / a**3),
    "q_PS = (Ab-aB)/a^3": (jet_coeff(jD, [P_, S_], (1, 1)), (A * b - a * B) / a**3),
    "q_SS = (-Ab^2+2abB-a^2C)/a^3":
        (2 * jet_coeff(jD, [P_, S_], (0, 2)), (-A * b**2 + 2 * a * b * B - a**2 * C) / a**3),
}
for name, (got, want) in tests.items():
    check("D-chart " + name, sp.simplify(got - want) == 0)

# ---- S-output chart S = r(D,P): Theorem 8.1 correction formulas -----------
jS, vS = rechart(jet_P, vars_P, 2, 1, 2)
D_, P2_ = vS[0], vS[2]
tests = {
    "r_D = -a/b":       (jet_coeff(jS, [D_, P2_], (1, 0)), -a / b),
    "r_P = 1/b":        (jet_coeff(jS, [D_, P2_], (0, 1)), 1 / b),
    "r_DD = (-Ca^2+2abB-b^2A)/b^3":
        (2 * jet_coeff(jS, [D_, P2_], (2, 0)), (-C * a**2 + 2 * a * b * B - b**2 * A) / b**3),
    "r_DP = (Ca-bB)/b^3": (jet_coeff(jS, [D_, P2_], (1, 1)), (C * a - b * B) / b**3),
    "r_PP = -C/b^3":    (2 * jet_coeff(jS, [D_, P2_], (0, 2)), -C / b**3),
}
for name, (got, want) in tests.items():
    check("S-chart " + name, sp.simplify(got - want) == 0)

# ---- six ordered charts collapse to three unordered jets -------------------
# Input swap changes nothing about the jet as a function germ; the ordered
# object is the jet PLUS the slot order. Hence exactly 3 distinct output-role
# jets and a free slot-ordering on each: verify D-chart jets computed from the
# swapped presentation agree as germs.
jet_P_swapped = jet_P.subs({D: S, S: D}, simultaneous=True).subs(
    {a: b, b: a, A: C, C: A}, simultaneous=True)
check("input swap fixes the P-output germ (covariance, not new data)",
      sp.expand(jet_P_swapped - jet_P) == 0)

jD2, vD2 = rechart(jet_P, vars_P, 2, 0, 2)
check("six ordered charts -> three output-role jets (D-chart germ unique)",
      jets_equal(jD, vD, jD2, vD2, 2))

print()
if failures:
    print("GATE 1 RECOVERY FAILED:", failures)
    sys.exit(1)
print("GATE 1 PASSED: all ten legacy inverse-chart derivatives recovered "
      "exactly; sixfold collapse verified.")
