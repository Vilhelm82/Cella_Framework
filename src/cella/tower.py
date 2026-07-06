"""The invariant tower — gate G1.1.

sigma_r, r = 1..n-1: elementary symmetric functions of the principal
curvatures of the level hypersurface, computed exactly from the jet.

Definition (the sign is part of the convention, pinned in the G1.1 prereg):

    A       = P H P ,   P = I - g g^T / q ,   q = g.g
    c_r     = e_r(A)    (principal-minor sums; A g = 0)
    sigma_r = (-1)^r c_r / q^(r/2)      (shape operator S = -(1/sqrt q) A|_T)

Parity law, enforced at the TYPE level (A-003):
    even r  -> Fraction
    odd  r  -> QSqrt(0, b, q), b = -c_r / q^((r+1)/2); collapses to Fraction
               exactly when b == 0 or q is a rational square.

Gauge invariance is identical, not numerical: P annihilates g, so the gauge
image g a^T + a g^T dies under conjugation by P — A never sees the gauge.

Chart/regularity distinction (pinned, G1.1 PREREG P3): the tower requires
only g != 0. Component-zero gradients refuse the CARRIER (no output chart,
`ROLE_CHART_UNAVAILABLE`) but not the tower — invariants need no chart.

Certified: tests/gate_11.py against campaigns/G11_invariant_tower/PREREG.md.
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import combinations

from .cell import Cell
from .jet import ConstraintBlock
from .qsqrt import QSqrt
from .refusal import Refusal

TIER_TOWER = ("tier: local; codim-1; orders 1..n-1; parity-typed "
              "(even Q, odd Q(sqrt q))")


def _is_square_rational(r: Fraction) -> bool:
    p, q = r.numerator, r.denominator
    sp, sq = math.isqrt(p), math.isqrt(q)
    return sp * sp == p and sq * sq == q


def _det(M):
    n = len(M)
    if n == 0:
        return Fraction(1)
    if n == 1:
        return M[0][0]
    total = Fraction(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += (-1) ** j * M[0][j] * _det(minor)
    return total


def _principal_minor_sum(A, r):
    n = len(A)
    return sum(_det([[A[i][j] for j in S] for i in S])
               for S in combinations(range(n), r))


def sigma_tower(block: ConstraintBlock) -> Cell:
    """The exact tower (sigma_1, ..., sigma_{n-1}) as a Cell.

    Refusals: CODIM_UNSUPPORTED for blocks of length > 1;
    SINGULAR_GRADIENT for g = 0. Nothing else refuses — see the
    chart/regularity note in the module docstring."""
    if not isinstance(block, ConstraintBlock):
        raise TypeError("sigma_tower takes a ConstraintBlock")
    if len(block) > 1:
        return Cell(None, Refusal(
            "CODIM_UNSUPPORTED",
            f"constraint system of {len(block)} constraints (codimension >= 2)"))
    jet = block.jets[0]
    g, H, n = jet.g, jet.h, jet.n
    q = sum(x * x for x in g)
    if q == 0:
        return Cell(None, Refusal(
            "SINGULAR_GRADIENT",
            "vanishing gradient: no surface direction at the base point"))
    q = Fraction(q)
    # A = P H P, exact
    P = tuple(tuple((Fraction(1) if i == j else Fraction(0))
                    - Fraction(g[i] * g[j]) / q for j in range(n))
              for i in range(n))
    PH = tuple(tuple(sum(P[i][k] * H[k][l] for k in range(n))
                     for l in range(n)) for i in range(n))
    A = tuple(tuple(sum(PH[i][k] * P[k][j] for k in range(n))
                    for j in range(n)) for i in range(n))
    sigmas = []
    for r in range(1, n):
        c = _principal_minor_sum(A, r)
        if r % 2 == 0:
            sigmas.append(c / q ** (r // 2))
        else:
            b = -c / q ** ((r + 1) // 2)
            if b == 0:
                sigmas.append(Fraction(0))
            elif _is_square_rational(q):
                sp = Fraction(math.isqrt(q.numerator), math.isqrt(q.denominator))
                sigmas.append(b * sp)
            else:
                sigmas.append(QSqrt(0, b, q))
    value = tuple(sigmas)
    return Cell(value, tuple(Fraction(0) for _ in value))
