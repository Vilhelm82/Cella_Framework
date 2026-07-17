#!/usr/bin/env python3
"""
FOUR-CHARGE CROWN TEST -- Galois machinery on the Cvetic-Youm four-charge class
================================================================================
Date: 2026-07-09.  Requires sympy.  Run: python3 four_charge_crown.py

QUESTION: does the two-sheet Galois machinery, applied to the four-charge
rotating black hole (the string-exact object, Strominger-Vafa lineage),
reproduce the integer product  S_L^2 - S_R^2 ~ N1 N2 N3 N4  -- and what happens
to the cover degree over the physical charges?

PARAMETRIC FAMILY [Cvetic-Youm class; reconstructed form, DOUBLE-ANCHORED]:
  boosts d_i, mass parameter m, rotation a:
    M   = (m/4) sum_i cosh 2d_i
    Q_i = (m/4) sinh 2d_i            (write s_i=sinh d_i, c_i=cosh d_i)
    N_i := 4 Q_i = m sinh 2d_i       (the quantized-charge normalization)
    J   = a m (prod c_i - prod s_i)
    S_+- = 2 pi m [ m(Pc+Ps) +- sqrt(m^2-a^2) (Pc-Ps) ],  Pc=prod c, Ps=prod s
ANCHORS (self-validation; if either fails the run is VOID):
  A1  all boosts -> 0  reproduces tonight's verified KERR quadratic.
  A2  equal boosts     reproduces tonight's verified KN quadratic with Q = sum Q_i.
"""
import sympy as sp
from sympy import Rational as R

m, a, pi, u = sp.symbols('m a pi u', positive=True)
s = list(sp.symbols('s1:5', positive=True))
c = list(sp.symbols('c1:5', positive=True))
Pc, Ps = sp.prod(c), sp.prod(s)

M  = (m/4)*sum(ci**2 + si**2 for ci, si in zip(c, s))     # (m/4) sum cosh2d
Q  = [(m/2)*si*ci for si, ci in zip(s, c)]                 # (m/4) sinh2d
N  = [4*q for q in Q]
J  = m*a*(Pc - Ps)
sq = sp.sqrt(m**2 - a**2)
Spl = 2*pi*m*(m*(Pc+Ps) + sq*(Pc-Ps))
Smi = 2*pi*m*(m*(Pc+Ps) - sq*(Pc-Ps))
e1, e2 = sp.expand(Spl + Smi), sp.expand(Spl*Smi)
SL, SR = sp.simplify((Spl+Smi)/2), sp.simplify((Spl-Smi)/2)

print("="*72)
print("ANCHORS (void the run if False)")
print("="*72)
kerr = {**{si: 0 for si in s}, **{ci: 1 for ci in c}}
A1a = sp.simplify(e1.subs(kerr) - 4*pi*m**2) == 0                 # 2pi(2M^2), M=m
A1b = sp.simplify(e2.subs(kerr) - 4*pi**2*a**2*m**2) == 0         # 4 pi^2 J^2, J=am
print("A1 Kerr limit:  e1 -> 4 pi m^2 :", A1a, "   e2 -> 4 pi^2 (am)^2 :", A1b)

seq, ceq = sp.symbols('s c', positive=True)
eqsub = {**{si: seq for si in s}, **{ci: ceq for ci in c}}
QK, MK = sum(Q).subs(eqsub), M.subs(eqsub)
d1 = sp.expand(e1.subs(eqsub) - 2*pi*(2*MK**2 - QK**2))
d1 = sp.expand(d1.subs(ceq**2, 1+seq**2)); d1 = sp.expand(d1.subs(ceq**2, 1+seq**2))
JK = J.subs(eqsub)
d2 = sp.expand(e2.subs(eqsub) - pi**2*(4*JK**2 + QK**4))
d2 = sp.expand(d2.subs(ceq**2, 1+seq**2)); d2 = sp.expand(d2.subs(ceq**2, 1+seq**2))
A2a, A2b = sp.simplify(d1) == 0, sp.simplify(d2) == 0
print("A2 KN diagonal: e1 == 2 pi(2M^2-Q^2) :", A2a, "   e2 == pi^2(4J^2+Q^4) :", A2b)

print()
print("="*72)
print("THE PRODUCT (unconditional algebra -- no hyperbolic constraint needed)")
print("="*72)
prod_ok = sp.simplify(sp.expand(e2 - pi**2*(4*J**2 + sp.prod(N)))) == 0
print("e2 = S+S-  ==  pi^2 ( 4 J^2  +  N1 N2 N3 N4 )   :", prod_ok)
print("   -> EXACT four-charge generalization of tonight's KN quadratic:")
print("      KN  e2 = pi^2(4J^2 + Q^4)   with   Q^4  ->  N1 N2 N3 N4.")
print("   -> mass enters ONLY through N_i and J: the invariant is the")
print("      quantized charge product. Level matching = e2 lattice.")

print()
print("extremal chirality  a->m:  S_R -> 0 :", sp.simplify(SR.subs(a, m)) == 0)
print("static split: S_L = 2 pi m^2 (Pc+Ps), S_R = 2 pi m^2 (Pc-Ps)",
      "(cosh/sinh microstate split):",
      sp.simplify(SL.subs(a,0) - 2*pi*m**2*(Pc+Ps)) == 0,
      sp.simplify(SR.subs(a,0) - 2*pi*m**2*(Pc-Ps)) == 0)

print()
print("="*72)
print("COVER DEGREE over the PHYSICAL charges (the wreath question)")
print("="*72)
print("Over Q(M, Q_i):  m obeys  4M = sum_i sqrt(m^2 + 16 Q_i^2)  (4 radicals).")
print("Eliminate at an exact rational point and count the fiber:")
sv = [R(3,4), R(5,12), R(8,15), R(20,21)]
cv = [R(5,4), R(13,12), R(17,15), R(29,21)]
m0 = R(2)
Q0 = [m0/2*sv[i]*cv[i] for i in range(4)]
M0 = (m0/4)*sum(cv[i]**2 + sv[i]**2 for i in range(4))
w2, w3, w4 = sp.symbols('w2 w3 w4')
f  = sp.expand((4*M0 - w2 - w3 - w4)**2 - (u + 16*Q0[0]**2))
r2 = sp.resultant(f,  w2**2 - (u + 16*Q0[1]**2), w2)
r3 = sp.resultant(r2, w3**2 - (u + 16*Q0[2]**2), w3)
r4 = sp.resultant(r3, w4**2 - (u + 16*Q0[3]**2), w4)
P  = sp.Poly(sp.expand(r4), u)
print("elimination polynomial degree in u=m^2 :", P.degree())
print("physical point u=4 is a root           :", P.eval(4) == 0)
roots = sp.real_roots(P.as_expr(), u)
pos = [r for r in roots if r.is_positive]
print("positive real roots (fiber over (M,Q)) :", len(pos))
print("  -> fiber > 1  <=>  the entropy cover over Q(M,Q_1..Q_4) has degree > 2:")
print("     the two-sheet Z/2 is the BOTTOM of a tower; radicals indexed per")
print("     charge, permuted when charges coincide -- imprimitive/wreath class.")
print("     The self-glue monodromy machinery ACTIVATES here (follow-on campaign:")
print("     compute the actual Galois/monodromy group of this cover).")
print()
print("CORRECTION (logged): last turn's guess that a single charge conjugation")
print("realizes the sheet swap DIES on inspection -- charge sign flips move the")
print("BASE POINT (they act on (e1,e2) parameters); the deck swap remains")
print("sqrt(disc) -> -sqrt(disc). The interplay of (Z/2)^4 charge conjugations")
print("with the deck Z/2 belongs to the group computation above.")
