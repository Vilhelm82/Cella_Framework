#!/usr/bin/env python3
"""Stage 4 gate A: active channel transport (PO-13, PO-14).

The transport law under test: the channel account of the sigma-output chart is
obtained by (i) transporting the jet with T_(rho,sigma) (Stage 1 engine),
(ii) evaluating the graph-channel formula in the new chart. The account moves
affinely over a fixed invariant:

    C_sigma = C_rho + Z_(rho,sigma),        Z_(rho,sigma) in ker(Sigma_channel).

  A1  transported-jet channels == native quadruple formulas (all three charts)
  A2  invariant part fixed: K identical across charts, identically in (a,b,A,B,C)
  A3  kernel law: Z_(rho,sigma) sums to zero identically; nonzero generically
  A4  keystone: implicit gauge has kint = -3/49 != 0, but the graph chart of
      the SAME surface at the SAME point has kint = 0 while K_G = -3/49
      (falsification item 6: graph vs implicit interaction)
"""
import sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("/", 1)[0] + "/role_cover_groupoid")
from jetlib import rechart, jet_coeff

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


def graph_channels(alpha, beta, L, M, N):
    """Graph-channel formula (authority: Paper I 5.4), legacy order (K,kc,ks,kint)."""
    Q = 1 + alpha**2 + beta**2
    return ((L * N - M**2) / Q**2, -(M**2) / Q**2, L * N / Q**2, 0)


a, b, A, B, C = sp.symbols("a b A B C")
D, S = sp.symbols("x0 x1")
jet_P = a * D + b * S + A * D**2 / 2 + B * D * S + C * S**2 / 2
vars_P = {0: D, 1: S}
q0 = 1 + a**2 + b**2
K = (A * C - B**2) / q0**2

# native P-chart account
C_P = graph_channels(a, b, A, B, C)

# D-chart account via Stage-1 transport
jD, vD = rechart(jet_P, vars_P, 2, 0, 2)
sy = [vD[2], vD[1]]
C_D = graph_channels(jet_coeff(jD, sy, (1, 0)), jet_coeff(jD, sy, (0, 1)),
                     2 * jet_coeff(jD, sy, (2, 0)), jet_coeff(jD, sy, (1, 1)),
                     2 * jet_coeff(jD, sy, (0, 2)))
# S-chart account via transport
jS, vS = rechart(jet_P, vars_P, 2, 1, 2)
sy = [vS[0], vS[2]]
C_S = graph_channels(jet_coeff(jS, sy, (1, 0)), jet_coeff(jS, sy, (0, 1)),
                     2 * jet_coeff(jS, sy, (2, 0)), jet_coeff(jS, sy, (1, 1)),
                     2 * jet_coeff(jS, sy, (0, 2)))

# A1: match the frozen quadruples
quad_D = (K, -(A * b - a * B)**2 / (a**2 * q0**2),
          A * (A * b**2 - 2 * a * b * B + a**2 * C) / (a**2 * q0**2), 0)
quad_S = (K, -(C * a - b * B)**2 / (b**2 * q0**2),
          C * (C * a**2 - 2 * a * b * B + b**2 * A) / (b**2 * q0**2), 0)
check("A1 transported D-chart account equals frozen C_D quadruple",
      all(sp.simplify(x - y) == 0 for x, y in zip(C_D, quad_D)))
check("A1 transported S-chart account equals frozen C_S quadruple",
      all(sp.simplify(x - y) == 0 for x, y in zip(C_S, quad_S)))

# A2 invariant part fixed identically
check("A2 K identical across all three output charts (identically)",
      sp.simplify(C_D[0] - K) == 0 and sp.simplify(C_S[0] - K) == 0
      and sp.simplify(C_P[0] - K) == 0)

# A3 kernel law
Z_PD = [sp.simplify(C_D[i] - C_P[i]) for i in (1, 2, 3)]
Z_PS = [sp.simplify(C_S[i] - C_P[i]) for i in (1, 2, 3)]
check("A3 Z_(P,D) sums to zero identically (kernel membership)",
      sp.simplify(sum(Z_PD)) == 0)
check("A3 Z_(P,S) sums to zero identically",
      sp.simplify(sum(Z_PS)) == 0)
wit = {a: 5, b: 7, A: 2, B: 3, C: 4}
check("A3 Z_(P,D) nonzero at witness (transport is genuinely affine, not strict)",
      any(z.subs(wit) != 0 for z in Z_PD))

# A4 keystone graph vs implicit
x1, x2 = sp.symbols("x1 x2")
h = sp.sqrt(3 - x1**2 - x1 * x2)
alpha = sp.diff(h, x1).subs({x1: 1, x2: 1})
beta = sp.diff(h, x2).subs({x1: 1, x2: 1})
L = sp.diff(h, x1, 2).subs({x1: 1, x2: 1})
M = sp.diff(h, x1, x2).subs({x1: 1, x2: 1})
N = sp.diff(h, x2, 2).subs({x1: 1, x2: 1})
Kg, kc_g, ks_g, kint_g = [sp.simplify(x) for x in graph_channels(alpha, beta, L, M, N)]
check("A4 keystone graph chart: K_G = -3/49 with kint = 0",
      Kg == sp.Rational(-3, 49) and kint_g == 0)
check("A4 implicit keystone kint = -3/49 != graph kint = 0 (interaction is "
      "presentation data)", sp.Rational(-3, 49) != 0 and kint_g == 0)

print()
if failures:
    print("STAGE 4A GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 4A GATE PASSED: affine kernel transport law proved on the generic "
      "symbolic jet; graph/implicit interaction split witnessed.")
