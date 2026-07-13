"""Newton-polytope corner scout (pfc thm:vertex / lead7 prop:corner).

From integer face exponents the scout builds the polar Newton vertices and
the support function m(a) = max over vertices of the polar pairing.  The
vertex-coefficient closed forms A(p0,p1,p2), B(q0,q1,q2) decide whether a
vertex is present; a vanishing coefficient is a declared cancellation.
"""

from __future__ import annotations

from fractions import Fraction

from ..ir.problem import NormalizedProblem
from ..ir.scope import AnalysisBudget
from ..ir.evidence import ScoutEvidence
from .protocol import scout_evidence


def vertex_coefficient(p0: int, p1: int, p2: int) -> int:
    """A(p0,p1,p2) = -p0^2 + p0*p1 - p0*p2 + 2*p0 + p1*p2 - p2^2 + 2*p2."""

    return -p0 * p0 + p0 * p1 - p0 * p2 + 2 * p0 + p1 * p2 - p2 * p2 + 2 * p2


def support_function(vertices: tuple[tuple[int, int], ...], direction: tuple[Fraction, Fraction]) -> Fraction:
    """m(a) = max_v ( -<a, v> ) over the polar vertices."""

    if not vertices:
        return Fraction(0)
    ax, ay = direction
    return max(-(ax * vx + ay * vy) for vx, vy in vertices)


def newton_corner_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
) -> ScoutEvidence | None:
    raw = problem.context_value("corner_exponents")
    if not isinstance(raw, tuple) or len(raw) != 3:
        return None
    pairs: list[tuple[int, int]] = []
    for entry in raw:
        if (
            not isinstance(entry, tuple)
            or len(entry) != 2
            or any(isinstance(v, bool) or not isinstance(v, int) for v in entry)
        ):
            return None
        pairs.append((int(entry[0]), int(entry[1])))
    (p0, q0), (p1, q1), (p2, q2) = pairs
    coefficient_a = vertex_coefficient(p0, p1, p2)
    coefficient_b = vertex_coefficient(q0, q2, q1)
    vertices: list[tuple[int, int]] = []
    if coefficient_a != 0:
        vertices.append((-(p1 + 2), -q1))
    if coefficient_b != 0:
        vertices.append((-p2, -(q2 + 2)))
    if p0 > 0 or q0 > 0:
        vertices.append((-p0, -q0))
    balanced = support_function(tuple(vertices), (Fraction(1), Fraction(1)))
    axis_x = support_function(tuple(vertices), (Fraction(1), Fraction(0)))
    axis_y = support_function(tuple(vertices), (Fraction(0), Fraction(1)))
    return scout_evidence(
        scout_family="newton_corner",
        problem=problem,
        fingerprint={
            "exponent_pairs": tuple(pairs),
            "vertex_coefficient_a": coefficient_a,
            "vertex_coefficient_b": coefficient_b,
            "polar_vertices": tuple(vertices),
            "support_balanced_diagonal": balanced,
            "support_axis_x": axis_x,
            "support_axis_y": axis_y,
            "vertex_cancellation": coefficient_a == 0 or coefficient_b == 0,
        },
        trace=(f"polar vertices {tuple(vertices)}; balanced support {balanced}",),
        stability="exact",
        scout_operations=len(pairs) * 3,
    )
