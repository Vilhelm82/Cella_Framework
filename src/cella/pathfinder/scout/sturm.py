"""Exact Sturm-chain scout over rational-coefficient univariate polynomials.

Used by the sturm_escalation route family: sign-change counts of a Sturm
sequence at interval endpoints, entirely in Fraction arithmetic.
"""

from __future__ import annotations

from fractions import Fraction

from ..ir.problem import NormalizedProblem
from ..ir.scope import AnalysisBudget
from ..ir.evidence import ScoutEvidence
from .protocol import scout_evidence

Poly = tuple[Fraction, ...]  # ascending coefficients


def _normalize(poly: tuple[Fraction, ...]) -> Poly:
    coefficients = list(poly)
    while coefficients and coefficients[-1] == 0:
        coefficients.pop()
    return tuple(coefficients)


def _derivative(poly: Poly) -> Poly:
    if len(poly) <= 1:
        return ()
    return _normalize(tuple(poly[power] * power for power in range(1, len(poly))))


def _polynomial_mod(dividend: Poly, divisor: Poly) -> Poly:
    remainder = list(dividend)
    degree_divisor = len(divisor) - 1
    lead = divisor[-1]
    while len(remainder) - 1 >= degree_divisor and any(c != 0 for c in remainder):
        degree_remainder = len(remainder) - 1
        factor = remainder[-1] / lead
        shift = degree_remainder - degree_divisor
        for position, coefficient in enumerate(divisor):
            remainder[position + shift] -= factor * coefficient
        while remainder and remainder[-1] == 0:
            remainder.pop()
    return tuple(remainder)


def sturm_chain(poly: Poly) -> tuple[Poly, ...]:
    p0 = _normalize(poly)
    if len(p0) <= 1:
        return (p0,)
    chain: list[Poly] = [p0, _derivative(p0)]
    while len(chain[-1]) > 1 or (chain[-1] and chain[-1][0] != 0):
        remainder = _polynomial_mod(chain[-2], chain[-1])
        if not remainder:
            break
        chain.append(tuple(-c for c in remainder))
        if len(chain[-1]) == 1:
            break
    return tuple(chain)


def _evaluate(poly: Poly, point: Fraction) -> Fraction:
    total = Fraction(0)
    for coefficient in reversed(poly):
        total = total * point + coefficient
    return total


def _sign_at_infinity(poly: Poly, positive: bool) -> int:
    if not poly:
        return 0
    lead = poly[-1]
    degree = len(poly) - 1
    if positive or degree % 2 == 0:
        return 1 if lead > 0 else -1
    return -1 if lead > 0 else 1


def _sign_changes(signs: list[int]) -> int:
    filtered = [s for s in signs if s != 0]
    return sum(1 for a, b in zip(filtered, filtered[1:]) if a != b)


def sturm_root_count(
    poly: Poly,
    lower: Fraction | None,
    upper: Fraction | None,
) -> int:
    """Distinct real roots in (lower, upper]; None means the signed infinity."""

    chain = sturm_chain(poly)
    if lower is None:
        low_signs = [_sign_at_infinity(entry, positive=False) for entry in chain]
    else:
        low_signs = [1 if _evaluate(entry, lower) > 0 else -1 if _evaluate(entry, lower) < 0 else 0 for entry in chain]
    if upper is None:
        high_signs = [_sign_at_infinity(entry, positive=True) for entry in chain]
    else:
        high_signs = [1 if _evaluate(entry, upper) > 0 else -1 if _evaluate(entry, upper) < 0 else 0 for entry in chain]
    return _sign_changes(low_signs) - _sign_changes(high_signs)


def sturm_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
) -> ScoutEvidence | None:
    raw = problem.context_value("univariate_coefficients")
    if not isinstance(raw, tuple) or not raw:
        return None
    coefficients: list[Fraction] = []
    for entry in raw:
        if isinstance(entry, bool) or not isinstance(entry, (int, Fraction)):
            return None
        coefficients.append(Fraction(entry))
    poly = _normalize(tuple(coefficients))
    if len(poly) <= 1:
        return None
    bound_raw = problem.context_value("interval")
    lower: Fraction | None = None
    upper: Fraction | None = None
    if isinstance(bound_raw, tuple) and len(bound_raw) == 2:
        low, high = bound_raw
        lower = Fraction(low) if isinstance(low, (int, Fraction)) and not isinstance(low, bool) else None
        upper = Fraction(high) if isinstance(high, (int, Fraction)) and not isinstance(high, bool) else None
    count = sturm_root_count(poly, lower, upper)
    all_positive_coefficients = all(c >= 0 for c in poly) and poly[-1] > 0
    return scout_evidence(
        scout_family="sturm_chain",
        problem=problem,
        fingerprint={
            "degree": len(poly) - 1,
            "distinct_real_roots_in_interval": count,
            "interval": (
                str(lower) if lower is not None else "-infinity",
                str(upper) if upper is not None else "+infinity",
            ),
            "coefficient_positive": all_positive_coefficients,
        },
        trace=(f"Sturm count {count} on declared interval",),
        stability="exact",
        scout_operations=(len(poly) - 1) ** 2,
    )
