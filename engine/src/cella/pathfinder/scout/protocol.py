"""Scout protocol: cheap internal probes producing serializable evidence."""

from __future__ import annotations

from typing import Callable, Mapping

from ..ir.burden import BurdenVector
from ..ir.evidence import ScoutEvidence
from ..ir.problem import NormalizedProblem
from ..ir.scope import AnalysisBudget, Scope
from ..ir.values import freeze_mapping

Scout = Callable[[NormalizedProblem, AnalysisBudget], ScoutEvidence | None]


def scout_evidence(
    *,
    scout_family: str,
    problem: NormalizedProblem,
    fingerprint: Mapping[str, object],
    trace: tuple[str, ...],
    stability: str,
    scout_operations: int,
    unresolved_inputs: tuple[str, ...] = (),
) -> ScoutEvidence:
    """Uniform evidence constructor so every scout serializes identically."""

    return ScoutEvidence(
        scout_family=scout_family,
        scope=Scope(
            object_family=problem.problem_shape or "undeclared",
            coefficient_domain=problem.ring.coefficient_domain if problem.ring else "undeclared",
            characteristic=problem.characteristic,
        ),
        structural_fingerprint=freeze_mapping(dict(fingerprint)),
        actual_trace=trace,
        burden_vector=BurdenVector(scout_operation_count=max(1, scout_operations)),
        stability=stability,
    )


def run_scouts(
    scouts: tuple[Scout, ...],
    problem: NormalizedProblem,
    budget: AnalysisBudget,
) -> tuple[ScoutEvidence, ...]:
    """Run each scout once; unavailable evidence is skipped, never fabricated."""

    collected: list[ScoutEvidence] = []
    for scout in scouts:
        evidence = scout(problem, budget)
        if evidence is not None:
            collected.append(evidence)
    return tuple(collected)
