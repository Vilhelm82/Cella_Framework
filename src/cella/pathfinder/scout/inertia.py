"""Exact rational inertia by congruence reduction (v1.3 §17.1).

Symmetric-form inertia over QQ using 1x1 and 2x2 pivots; a hyperbolic block
[[0,b],[b,0]] contributes one positive and one negative direction.  No
floating eigendecomposition is admitted.  Route evidence only.
"""

from __future__ import annotations

from fractions import Fraction

from ..ir.problem import NormalizedProblem
from ..ir.scope import AnalysisBudget
from ..ir.evidence import ScoutEvidence
from .protocol import scout_evidence


def congruence_inertia(
    matrix: tuple[tuple[Fraction, ...], ...],
) -> tuple[int, int, int]:
    """(positive, negative, nullity) of an exact symmetric matrix."""

    size = len(matrix)
    work = [[Fraction(entry) for entry in row] for row in matrix]
    for row in work:
        if len(row) != size:
            raise ValueError("inertia requires a square matrix")
    for i in range(size):
        for j in range(i):
            if work[i][j] != work[j][i]:
                raise ValueError("inertia requires an exactly symmetric matrix")

    positive = negative = nullity = 0
    index = 0
    active = list(range(size))
    while active:
        pivot_position = next(
            (k for k, row_index in enumerate(active) if work[row_index][row_index] != 0),
            None,
        )
        if pivot_position is not None:
            p = active.pop(pivot_position)
            pivot = work[p][p]
            if pivot > 0:
                positive += 1
            else:
                negative += 1
            for r in active:
                factor = work[r][p] / pivot
                for c in active:
                    work[r][c] -= factor * work[p][c]
                work[r][p] = Fraction(0)
                work[p][r] = Fraction(0)
            continue
        # No nonzero diagonal remains: look for a 2x2 hyperbolic pivot.
        off = next(
            (
                (a_pos, b_pos)
                for a_pos in range(len(active))
                for b_pos in range(a_pos + 1, len(active))
                if work[active[a_pos]][active[b_pos]] != 0
            ),
            None,
        )
        if off is None:
            nullity += len(active)
            break
        a_pos, b_pos = off
        a = active[a_pos]
        b = active[b_pos]
        pivot_value = work[a][b]
        # [[0,b],[b,0]] block: one positive, one negative direction.
        positive += 1
        negative += 1
        remaining = [r for r in active if r not in (a, b)]
        for r in remaining:
            # Eliminate row r against the 2x2 block [[0,v],[v,0]].
            alpha = work[r][b] / pivot_value
            beta = work[r][a] / pivot_value
            for c in remaining:
                work[r][c] -= alpha * work[a][c] + beta * work[b][c]
            work[r][a] = work[r][b] = Fraction(0)
            work[a][r] = work[b][r] = Fraction(0)
        active = remaining
        del index
    return positive, negative, nullity


def _matrix_from_context(problem: NormalizedProblem) -> tuple[tuple[Fraction, ...], ...] | None:
    raw = problem.context_value("symmetric_matrix")
    if not isinstance(raw, tuple):
        return None
    rows: list[tuple[Fraction, ...]] = []
    for row in raw:
        if not isinstance(row, tuple):
            return None
        entries: list[Fraction] = []
        for entry in row:
            if isinstance(entry, bool) or not isinstance(entry, (int, Fraction)):
                return None
            entries.append(Fraction(entry))
        rows.append(tuple(entries))
    if not rows or any(len(row) != len(rows) for row in rows):
        return None
    return tuple(rows)


def exact_inertia_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
) -> ScoutEvidence | None:
    matrix = _matrix_from_context(problem)
    if matrix is None:
        return None
    try:
        positive, negative, nullity = congruence_inertia(matrix)
    except ValueError:
        return None
    return scout_evidence(
        scout_family="exact_rational_inertia",
        problem=problem,
        fingerprint={
            "size": len(matrix),
            "positive": positive,
            "negative": negative,
            "nullity": nullity,
            "signature": positive - negative,
            "definite": nullity == 0 and (positive == len(matrix) or negative == len(matrix)),
        },
        trace=(f"congruence inertia ({positive},{negative},{nullity})",),
        stability="exact",
        scout_operations=len(matrix) ** 3,
    )
