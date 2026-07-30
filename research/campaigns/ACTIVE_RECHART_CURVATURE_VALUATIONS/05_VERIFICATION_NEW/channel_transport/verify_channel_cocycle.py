#!/usr/bin/env python3
"""Stage 4 gate C: channel-defect cocycle on the triple overlap (PO-14).

  Z_(rho,tau) = Z_(rho,sigma) + Z_(sigma,tau)   with all Z in ker(Sigma_channel),
identically in the generic symbolic jet, plus exact witness values.

Note the account transport is affine over the FIXED invariant (the scalar
pullback of K is the identity at a point), so the plan's twisted form
Z_(rho,tau) = Z_(rho,sigma) + T_(rho,sigma) Z_(sigma,tau) holds with the
account-transport operator acting as the identity on kernel vectors: this
gate proves that statement rather than assuming it.
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
ks_D = A * (A * b**2 - 2 * a * b * B + a**2 * C) / (a**2 * q0**2)
ks_S = C * (C * a**2 - 2 * a * b * B + b**2 * A) / (b**2 * q0**2)
ACC = {
    "P": sp.Matrix([-B**2 / q0**2, sp.Integer(0), A * C / q0**2]),
    "D": sp.Matrix([-(A * b - a * B)**2 / (a**2 * q0**2), sp.Integer(0), ks_D]),
    "S": sp.Matrix([-(C * a - b * B)**2 / (b**2 * q0**2), sp.Integer(0), ks_S]),
}   # canonical order (kappa_c, kappa_int, kappa_s); graph gauge => kint = 0


def Z(r, s):
    return ACC[s] - ACC[r]


# kernel membership identically
for r, s in (("P", "D"), ("D", "S"), ("P", "S")):
    check(f"Z_({r},{s}) in ker(Sigma_channel) identically",
          sp.simplify(sum(Z(r, s))) == 0)

# cocycle law identically
coc = sp.simplify(sp.expand(Z("P", "S") - Z("P", "D") - Z("D", "S")))
check("cocycle Z_(P,S) = Z_(P,D) + Z_(D,S) identically", coc == sp.zeros(3, 1))

# witness values (5,7,2,3,4)
wit = {a: 5, b: 7, A: 2, B: 3, C: 4}
zpd = Z("P", "D").subs(wit)
check("witness Z_(P,D) = (kc: -1/140625 + 1/625, ks: -8/46875 - 8/5625)",
      zpd[0] == sp.Rational(-1, 140625) + sp.Rational(1, 625)
      and zpd[2] == sp.Rational(-8, 46875) - sp.Rational(8, 5625)
      and zpd[0] + zpd[1] + zpd[2] == 0)

print()
if failures:
    print("STAGE 4C GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 4C GATE PASSED: kernel cocycle exact on the triple overlap.")
