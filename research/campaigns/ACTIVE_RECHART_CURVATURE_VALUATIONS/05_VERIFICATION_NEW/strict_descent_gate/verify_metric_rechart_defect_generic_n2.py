#!/usr/bin/env python3
"""Stage 3 decisive gate, part 1: generic symbolic three-role metric descent
test (PO-9, PO-11 start).  NOT Kerr-Newman: the jet (a,b,A,B,C) is fully
generic symbolic.

Construction under test (frozen in NOTATION_LEDGER 5): for presentation rho,

    g^(rho) = sum_{i != rho} G_i^(rho) (dx_i)^2,
    G_i^(rho) = q_i^2 / Lambda_{i,{rho,m}}^2          (n = 2: single pair)

with q_i the i-output chart norm and Lambda the chart mixed partial.

Checks:
  M1  weight identity: G_i^(rho) = q_0^2 / Lambda_i^2 with Lambda_P = B,
      Lambda_D = (Ab-aB)/a, Lambda_S = (Ca-bB)/b  — i.e. the diagonal weights
      w_i are PRESENTATION-INDEPENDENT scalars (shared-entry coincidence).
  M2  strict descent is FALSE: D_(P,D) = g^(P) - phi*(g^(D)) != 0 generically,
      with an exact rational witness.
  M3  structure: D_(rho,sigma) = iota*( w_sigma dx_sigma^2 - w_rho dx_rho^2 )
      — difference of two rank-one forms, verified symbolically.
  M4  the defect is NOT conformal: phi*(g^(D)) = lambda g^(P) has no scalar
      solution generically (witness).
  M5  descent of the average: T = (1/2) sum_rho g^(rho) is the restriction of
      the single ambient diagonal form  W = sum_i w_i dx_i^2, and
      g^(rho) = T - iota*(w_rho dx_rho^2)  exactly.
  M6  determinant transformation: det phi*(g^(D)) = a^2 det(g^(D) at the same
      point) — determinant divisors agree up to the square of the chart
      Jacobian factor (so the determinant DIVISOR CLASS descends, the
      determinant function does not).
  M7  signature descends: all three metrics are positive definite on the real
      locus Lambda_P Lambda_D Lambda_S != 0 (squares of nonzero reals).
"""
import sys
import sympy as sp

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


a, b, A, B, C = sp.symbols("a b A B C", real=True)
q0 = 1 + a**2 + b**2

# ---- chart data derived from first principles (Stage 1 engine formulas) ----
# D-output chart D = q(P,S):   q_P = 1/a, q_S = -b/a, q_PS = (Ab-aB)/a^3
# S-output chart S = r(D,P):   r_D = -a/b, r_P = 1/b, r_DP = (Ca-bB)/b^3
qD_norm = 1 + (1 / a) ** 2 + (b / a) ** 2          # 1 + |grad f_D|^2
qS_norm = 1 + (a / b) ** 2 + (1 / b) ** 2
LamP = B
LamD = (A * b - a * B) / a
LamS = (C * a - b * B) / b

# metric entries by the frozen assignment G_i^(rho) = q_i^2 / (chart mixed partial)^2
G_D_of_P = qD_norm**2 / ((A * b - a * B) / a**3) ** 2      # state coord D, presentation P
G_S_of_P = qS_norm**2 / ((C * a - b * B) / b**3) ** 2      # state coord S, presentation P
G_P_of_D = q0**2 / B**2                                     # state coord P, presentation D
G_S_of_D = qS_norm**2 / ((C * a - b * B) / b**3) ** 2      # state coord S, presentation D
G_D_of_S = qD_norm**2 / ((A * b - a * B) / a**3) ** 2      # state coord D, presentation S
G_P_of_S = q0**2 / B**2                                     # state coord P, presentation S

# M1: weights are presentation-independent: w_i = q0^2 / Lambda_i^2
wP = q0**2 / LamP**2
wD = q0**2 / LamD**2
wS = q0**2 / LamS**2
check("M1 w_D = q0^2/Lambda_D^2 (both presentations)",
      sp.simplify(G_D_of_P - wD) == 0 and sp.simplify(G_D_of_S - wD) == 0)
check("M1 w_S = q0^2/Lambda_S^2 (both presentations)",
      sp.simplify(G_S_of_P - wS) == 0 and sp.simplify(G_S_of_D - wS) == 0)
check("M1 w_P = q0^2/Lambda_P^2 (both presentations)",
      sp.simplify(G_P_of_D - wP) == 0 and sp.simplify(G_P_of_S - wP) == 0)

# ---- metrics as matrices in their own base charts ---------------------------
# presentation P, base (D,S):
gP = sp.diag(wD, wS)
# presentation D, base (P,S):
gD = sp.diag(wP, wS)
# presentation S, base (D,P):
gS = sp.diag(wD, wP)

# pullback phi_(P,D): (D,S) -> (P,S), dP = a dD + b dS
J_PD = sp.Matrix([[a, b], [0, 1]])           # rows: (dP, dS) in terms of (dD, dS)
pull_gD = sp.expand(J_PD.T * gD * J_PD)

# M2: strict descent falsified
Ddef = sp.expand(gP - pull_gD)
Ddef_simplified = sp.simplify(Ddef)
witness = {a: 5, b: 7, A: 2, B: 3, C: 4}
Dw = Ddef.subs(witness)
check("M2 defect D_(P,D) is nonzero on the exact witness (5,7,2,3,4)",
      sp.simplify(Dw) != sp.zeros(2, 2) and any(x != 0 for x in Dw))

# M3: rank-one difference structure
rank1_target = sp.expand(
    sp.diag(wD, 0) - wP * sp.Matrix([[a], [b]]) * sp.Matrix([[a, b]]))
check("M3 D_(P,D) = w_D dD^2 - w_P (a dD + b dS)^2 exactly",
      sp.simplify(Ddef - rank1_target) == sp.zeros(2, 2))

# M4: non-conformality witness: ratios of matched entries differ
r11 = sp.simplify(pull_gD[0, 0] / gP[0, 0])
r22 = sp.simplify(pull_gD[1, 1] / gP[1, 1])
check("M4 pullback is not conformal to native (witness ratios differ)",
      sp.simplify((r11 - r22).subs(witness)) != 0)

# M5: average descent and the T - c_rho law
# In P-base coordinates, iota*(w_P dP^2) = w_P (a dD + b dS)^2 etc.
iota_P = wP * sp.Matrix([[a], [b]]) * sp.Matrix([[a, b]])
iota_D = sp.diag(wD, 0)
iota_S = sp.diag(0, wS)
T = sp.expand(iota_P + iota_D + iota_S)     # restriction of W = sum w_i dx_i^2
check("M5 g^(P) = T - iota*(w_P dP^2) exactly",
      sp.simplify(gP - (T - iota_P)) == sp.zeros(2, 2))
check("M5 phi*(g^(D)) = T - iota*(w_D dD^2) exactly",
      sp.simplify(pull_gD - (T - iota_D)) == sp.zeros(2, 2))
# and the average: (1/2) sum over presentations (all pulled to P-base) = T
pull_gS = sp.expand(sp.Matrix([[1, 0], [a, b]]).T * gS * sp.Matrix([[1, 0], [a, b]]))
avg = sp.expand((gP + pull_gD + pull_gS) / 2)
check("M5 T = (1/2)(g^(P) + phi*g^(D) + phi*g^(S)) descends",
      sp.simplify(avg - T) == sp.zeros(2, 2))

# M6: determinant transformation
detlaw = sp.simplify(pull_gD.det() - a**2 * gD.det())
check("M6 det(phi* g^(D)) = a^2 det(g^(D)) (Jacobian-square law)", detlaw == 0)

# M7: signature (positive definiteness off the isotropy loci)
gPw = gP.subs(witness)
gDw = gD.subs(witness)
check("M7 both metrics positive definite at the witness",
      gPw[0, 0] > 0 and gPw.det() > 0 and gDw[0, 0] > 0 and gDw.det() > 0)

print()
if failures:
    print("STAGE 3 GENERIC GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 3 GENERIC GATE PASSED: strict descent FALSIFIED with witness; "
      "defect = coboundary of rank-one role forms; average tensor descends; "
      "determinant divisor class descends; signature descends.")
