"""DBP regularity scout: q = g^T g over exact rationals.

Refuse-only-when-q-is-zero is the corpus regularity rule; a single vanishing
gradient component is not singular when q != 0.
"""

from __future__ import annotations

from fractions import Fraction

from ..ir.problem import NormalizedProblem
from ..ir.scope import AnalysisBudget
from ..ir.evidence import ScoutEvidence
from .protocol import scout_evidence


def regularity_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
) -> ScoutEvidence | None:
    raw = problem.context_value("gradient")
    if not isinstance(raw, tuple) or not raw:
        return None
    gradient: list[Fraction] = []
    for entry in raw:
        if isinstance(entry, bool) or not isinstance(entry, (int, Fraction)):
            return None
        gradient.append(Fraction(entry))
    q = sum(value * value for value in gradient)
    return scout_evidence(
        scout_family="dbp_regularity",
        problem=problem,
        fingerprint={
            "dimension": len(gradient),
            "q": q,
            "regular": q != 0,
            "zero_components": tuple(index for index, value in enumerate(gradient) if value == 0),
            "all_components_nonzero": all(value != 0 for value in gradient),
        },
        trace=(f"q = g^T g = {q}",),
        stability="exact",
        scout_operations=len(gradient),
    )
