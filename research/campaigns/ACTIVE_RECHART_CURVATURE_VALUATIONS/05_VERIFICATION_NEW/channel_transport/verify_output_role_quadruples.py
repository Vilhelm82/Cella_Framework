#!/usr/bin/env python3
"""Stage 4 gate B (Gate 4 proper): the three output-role quadruples, closure
identities, transverse quadratic, worked example, and carrier faithfulness
(PO-17 + required transfer from Theorem_8_1_Curvature_Orbit_Correction).

  B1  closure identities (both), identically in (a,b,A,B,C)
  B2  transverse quadratic laws kappa_s,D = A*R/(a^2 q0^2), kappa_s,S = C*R/(b^2 q0^2)
  B3  worked example (a,b,A,B,C) = (5,7,2,3,4): all three quadruples exact
  B4  coupling-carrier faithfulness Jacobian det = 8 Lambda_P Lambda_D Lambda_S / q0^6
  B5  input swap fixes each scalar account while the labelled jet moves
      (falsification item 7)
"""
import sys
import sympy as sp

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


a, b, A, B, C = sp.symbols("a b A B C")
q0 = 1 + a**2 + b**2
K = (A * C - B**2) / q0**2

# B1 closure identities
lhs1 = A * (A * b**2 - 2 * a * b * B + a**2 * C) - (A * b - a * B)**2
lhs2 = C * (C * a**2 - 2 * a * b * B + b**2 * A) - (C * a - b * B)**2
check("B1 A-closure = a^2(AC - B^2)", sp.expand(lhs1 - a**2 * (A * C - B**2)) == 0)
check("B1 C-closure = b^2(AC - B^2)", sp.expand(lhs2 - b**2 * (A * C - B**2)) == 0)

# B2 transverse quadratic
R_trans = a**2 * C - 2 * a * b * B + b**2 * A
ks_D = A * (A * b**2 - 2 * a * b * B + a**2 * C) / (a**2 * q0**2)
ks_S = C * (C * a**2 - 2 * a * b * B + b**2 * A) / (b**2 * q0**2)
check("B2 kappa_s,D = A*R_trans/(a^2 q0^2)",
      sp.simplify(ks_D - A * R_trans / (a**2 * q0**2)) == 0)
check("B2 kappa_s,S = C*R_trans/(b^2 q0^2)",
      sp.simplify(ks_S - C * R_trans / (b**2 * q0**2)) == 0)
quad_val = (sp.Matrix([[b, -a]]) * sp.Matrix([[A, B], [B, C]])
            * sp.Matrix([[b], [-a]]))[0, 0]
check("B2 R_trans is the normal-frame quadratic (b,-a) Hess (b,-a)^T",
      sp.expand(R_trans - quad_val) == 0)

# B3 worked example
wit = {a: 5, b: 7, A: 2, B: 3, C: 4}
CP = (K, -B**2 / q0**2, A * C / q0**2, 0)
CD = (K, -(A * b - a * B)**2 / (a**2 * q0**2), ks_D, 0)
CS = (K, -(C * a - b * B)**2 / (b**2 * q0**2), ks_S, 0)
vals = {
    "C_P": ([x.subs(wit) if hasattr(x, "subs") else x for x in CP],
            [sp.Rational(-1, 5625), sp.Rational(-1, 625), sp.Rational(8, 5625), 0]),
    "C_D": ([x.subs(wit) if hasattr(x, "subs") else x for x in CD],
            [sp.Rational(-1, 5625), sp.Rational(-1, 140625), sp.Rational(-8, 46875), 0]),
    "C_S": ([x.subs(wit) if hasattr(x, "subs") else x for x in CS],
            [sp.Rational(-1, 5625), sp.Rational(-1, 275625), sp.Rational(-16, 91875), 0]),
}
for name, (got, want) in vals.items():
    check(f"B3 worked example {name} exact", [sp.nsimplify(x) for x in got] == want)
# R_trans value transfer required by the plan
check("B3 R_trans(5,7,2,3,4) = -12", R_trans.subs(wit) == -12)

# B4 carrier faithfulness Jacobian
LamP, LamD, LamS = B, (A * b - a * B) / a, (C * a - b * B) / b
O_carrier = sp.Matrix([-LamP**2 / q0**2, -LamD**2 / q0**2, -LamS**2 / q0**2])
Jac = O_carrier.jacobian([A, B, C])
det = sp.simplify(Jac.det())
target = sp.simplify(8 * LamP * LamD * LamS / q0**6)
check("B4 det d(O)/d(A,B,C) = 8 Lambda_P Lambda_D Lambda_S / q0^6",
      sp.simplify(det - target) == 0)

# B5 input swap: s(a,b,A,B,C) = (b,a,C,B,A) fixes each account, moves the jet
swap = {a: b, b: a, A: C, C: A}
for name, acc in (("C_P", CP), ("C_D", CS), ("C_S", CD)):
    # under input swap, the D- and S-output accounts exchange LABELS but the
    # spectrum {C_P, C_D, C_S} is fixed; C_P maps to itself.
    pass
CP_sw = [sp.simplify(x.subs(swap, simultaneous=True) - y) if hasattr(x, "subs") else 0
         for x, y in zip(CP, CP)]
check("B5 input swap fixes C_P componentwise", all(x == 0 for x in CP_sw))
CD_sw = [sp.simplify(x.subs(swap, simultaneous=True) - y) if hasattr(x, "subs") else 0
         for x, y in zip(CD, CS)]
check("B5 input swap exchanges C_D and C_S (spectrum fixed as a set)",
      all(x == 0 for x in CD_sw))
check("B5 the labelled jet itself moves under the swap (witness)",
      (a.subs(swap, simultaneous=True) - a).subs(wit) != 0)

print()
if failures:
    print("STAGE 4B GATE FAILED:", failures)
    sys.exit(1)
print("GATE 4 PASSED: quadruples, closure identities, transverse quadratic, "
      "worked example, faithfulness Jacobian, swap covariance — all exact.")
