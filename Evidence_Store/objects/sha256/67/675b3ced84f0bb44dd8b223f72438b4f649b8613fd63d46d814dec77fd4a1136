#!/usr/bin/env python3
"""
ABEL-RUFFINI FOR BLACK HOLES -- the mod-p computation
=====================================================
Date: 2026-07-09.  Requires sympy, mpmath.  Run: python3 abel_ruffini_black_holes.py

CLAIM UNDER TEST: over the physical field Q(M, Q_1..Q_4), the seed mass-square
u = m^2 of the four-charge (Cvetic-Youm class) black hole -- defined by
        4M = sum_i sqrt(u + 16 Q_i^2)
-- has a degree-5 minimal polynomial with Galois group S_5. If so, by
Abel-Ruffini the mass fiber admits NO closed-form radical expression in the
physical variables, and the 25-year-old parametric (cosh/sinh) dictionary was
never a convention: it was a necessity.

CERTIFICATION LOGIC (airtight direction only):
  * The norm polynomial N(u) = prod over all 16 sign patterns of
    (4M - sum_i eps_i sqrt(u + a_i)), a_i = 16 Q_i^2, is a degree-5 polynomial.
  * Specialization: Gal(specialized) <= Gal(generic). Contrapositive: generic
    solvable => every good specialization solvable. ONE specialization with
    Gal = S_5 (non-solvable) => generic group is non-solvable (indeed = S_5).
  * Dedekind: for p not dividing disc or lc, the factorization degree pattern
    of N mod p is a cycle type of some Frobenius element of Gal.
  * Among TRANSITIVE quintic groups {C5, D5, F20, A5, S5}: a pattern
    {1,1,1,2} (transposition) or {2,3} (order-6 element) occurs ONLY in S5.
    So: irreducible over Q  +  one such prime witness  =>  Gal = S_5.

Charges are chosen DIRECTLY (generic rationals), never via the boost
parametrization -- so the physical root does not split off artificially.
Physical existence: the all-plus branch has a real root iff M > sum|Q_i|
(the BPS-type bound); it is UNIQUE (the branch sum is monotone in m).
"""
import sympy as sp
import mpmath as mp
from sympy import Rational as R

u, x, w = sp.symbols('u x w')


def norm_poly(M0, Qs):
    """N(u) = prod_{eps in {+-1}^4} (4M - sum_i eps_i w_i),  w_i^2 = u + 16 Q_i^2.
    Built by conjugate doubling; exact rationals throughout."""
    a = [16*q**2 for q in Qs]
    p = x                                   # roots so far: {0}
    for ak in a:
        q2 = sp.expand(p.subs(x, x - w) * p.subs(x, x + w))
        P2 = sp.Poly(q2, w)
        deg = P2.degree()
        coeffs = P2.all_coeffs()            # descending in w
        expr = 0
        for i, cf in enumerate(coeffs):
            k = deg - i
            if sp.expand(cf) == 0:
                continue
            assert k % 2 == 0, "odd power survived -- construction error"
            expr += sp.expand(cf) * (u + ak)**(k // 2)
        p = sp.expand(expr)
    N = sp.expand(p.subs(x, 4*M0))
    return sp.Poly(N, u)


def analyse(tag, M0, Qs, primes):
    print("=" * 74)
    print(f"POINT {tag}:  M = {M0},  Q = {tuple(Qs)}")
    bps = sum(abs(q) for q in Qs)
    print(f"  BPS margin: M - sum|Q_i| = {sp.nsimplify(M0 - bps)}  (> 0 required)")
    N = norm_poly(M0, Qs)
    print(f"  degree of N(u): {N.degree()}")
    _, Nz = N.clear_denoms()
    Nz = sp.Poly(Nz.as_expr(), u).primitive()[1]
    sep = sp.gcd(Nz.as_expr(), sp.diff(Nz.as_expr(), u))
    print(f"  separable: {sp.degree(sep, u) == 0}")
    fl = sp.factor_list(Nz.as_expr())[1]
    degs = sorted(sp.degree(f, u) for f, m_ in fl for _ in range(m_))
    irred = degs == [5]
    print(f"  factorization over Q (degrees): {degs}   irreducible: {irred}")

    # physical root: unique real solution of the all-plus branch
    a = [16*q**2 for q in Qs]
    mp.mp.dps = 40
    af = [mp.mpf(int(sp.nsimplify(ai * 10**12))) / mp.mpf(10**12) for ai in
          [sp.nsimplify(ai) for ai in a]]
    Mf = mp.mpf(int(sp.nsimplify(M0 * 10**12))) / mp.mpf(10**12)
    g = lambda m: sum(mp.sqrt(m**2 + ai) for ai in af) - 4*Mf
    mstar = mp.findroot(g, 4*Mf)
    ustar = mstar**2
    Nf = sp.lambdify(u, Nz.as_expr(), 'mpmath')
    scale = max(abs(c) for c in Nz.all_coeffs())
    resid = abs(Nf(ustar)) / (mp.mpf(int(scale)) * max(1, ustar)**5)
    print(f"  physical root u* = m^2 = {mp.nstr(ustar, 12)}   "
          f"N(u*)/scale = {mp.nstr(resid, 3)}  (~0 => u* is a root of the quintic)")
    nreal = sp.count_roots(Nz)
    print(f"  real roots of the quintic: {nreal}")

    D = sp.discriminant(Nz.as_expr(), u)
    lc = Nz.all_coeffs()[0]
    witness_S5, saw_5cycle, table = None, False, []
    for p_ in primes:
        if D % p_ == 0 or lc % p_ == 0:
            continue
        try:
            flp = sp.Poly(Nz.as_expr(), u, modulus=p_).factor_list()[1]
        except Exception:
            continue
        pat = sorted(sp.degree(f.as_expr(), u) for f, m_ in flp for _ in range(m_))
        table.append((p_, pat))
        if pat == [5]:
            saw_5cycle = True
        if pat in ([1, 1, 1, 2], [2, 3]) and witness_S5 is None:
            witness_S5 = (p_, pat)
    print("  Frobenius cycle types (Dedekind):")
    for p_, pat in table:
        mark = "  <-- S5 witness" if pat in ([1, 1, 1, 2], [2, 3]) else \
               ("  (5-cycle)" if pat == [5] else "")
        print(f"     p = {p_:3d}: {pat}{mark}")
    verdict = irred and witness_S5 is not None
    print(f"  VERDICT at this point: "
          f"{'Gal = S_5 (non-solvable)' if verdict else 'S_5 not certified here'}"
          + (f"   [witness p = {witness_S5[0]}, type {witness_S5[1]};"
         f" 5-cycles seen: {saw_5cycle}]" if verdict else ""))
    return verdict


PRIMES = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

points = [
    ("A (generic rationals)", R(3),  [R(1, 3), R(1, 2), R(2, 5), R(3, 7)]),
    ("B (integer string charges)", R(15), [R(1), R(2), R(3), R(5)]),
    ("C (generic rationals)", R(2),  [R(2, 7), R(5, 9), R(1, 4), R(4, 11)]),
]

wins = [analyse(t, M0, Q, PRIMES) for (t, M0, Q) in points]

print("=" * 74)
print("CONCLUSION")
print("=" * 74)
if any(wins):
    print("""At least one good rational specialization has Galois group S_5.
By the specialization principle (generic solvable => all specializations
solvable), the GENERIC Galois group of the mass fiber over Q(M, Q_1..Q_4)
is therefore non-solvable -- and, being a transitive subgroup of S_5
containing S_5 witnesses, it IS S_5.

THEOREM (Abel-Ruffini for the four-charge black hole).  The seed mass-square
m^2 of the non-extremal four-charge black hole is a degree-5 algebraic
function of the physical mass and charges with Galois group S_5. There is NO
closed-form radical expression for m^2 -- hence none for the parametric
dictionary as written -- in the physical variables. The 25 years of
cosh/sinh parametrization were forced: the inversion is Abel-Ruffini
obstructed.

Counterpoint (the night's split, now arithmetic): the Galois-INVARIANT
sector escapes the obstruction entirely -- e2 = S+S- = pi^2(4J^2 + N1N2N3N4)
is rational (degree 1) in the charges. Everything the invariant ring keeps
is rational; everything it discards lives under S_5.

Scope: (i) statement is about inverting the parametrization (the mass
fiber); whether S+- admits some radical expression NOT factoring through m
is a separate open question. (ii) Parametric family attribution + literature
pin owed. (iii) Witnesses reproducible from this script alone.""")
else:
    print("""No S_5 witness found at the sampled points. Report the observed
factorization patterns honestly and investigate the hidden structure --
a generic factorization would itself be a discovery (a rational invariant
nobody has named).""")
