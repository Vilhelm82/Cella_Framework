"""Admissibility-first, burden/Pareto route selection.

plan_request lowers the request once, runs the enabled providers' native
scouts to enrich the evidence, invokes each recognizer, and compares the
admitted candidates deterministically.  Every losing candidate receives an
explicit rejection record; nothing here executes host mathematics.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from ..api.contract import RecognitionRefusal, RouteCandidate
from ..api.request import PathfinderRequest
from ..api.route import ComputationalRoute
from ..ir.evidence import ScoutEvidence
from ..ir.fingerprint import StructuralFingerprint, fingerprint_problem
from ..ir.problem import lower_request
from ..scout.protocol import run_scouts
from .compare import RouteRejection, compare_candidates
from .registry import PROVIDERS


@dataclass(frozen=True, slots=True)
class PlanningRefusal:
    code: str
    reason: str
    recognizer_refusals: tuple[RecognitionRefusal, ...]
    unregistered_route_families: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PlanningOutcome:
    route: ComputationalRoute | None
    selected_candidate: RouteCandidate | None
    pareto_frontier: tuple[str, ...]
    recognizer_refusals: tuple[RecognitionRefusal, ...]
    refusal: PlanningRefusal | None = None
    rejected_alternatives: tuple[RouteRejection, ...] = ()
    structural_fingerprint: StructuralFingerprint | None = None
    gathered_scout_evidence: tuple[ScoutEvidence, ...] = ()

    def __post_init__(self) -> None:
        selected = self.route is not None and self.selected_candidate is not None
        if selected == (self.refusal is not None):
            raise ValueError("planning outcome must contain either a selected route or a refusal")


def plan_request(request: PathfinderRequest) -> PlanningOutcome:
    """Discover and select a route without invoking any execution module."""

    problem = lower_request(request)

    # Run each enabled provider's native scouts once (deduplicated).
    seen_scouts: set[int] = set()
    gathered: list[ScoutEvidence] = []
    for family in request.available_route_families:
        provider = PROVIDERS.get(family)
        if provider is None:
            continue
        fresh_scouts = tuple(
            scout for scout in provider.native_scouts if id(scout) not in seen_scouts
        )
        seen_scouts.update(id(scout) for scout in fresh_scouts)
        gathered.extend(run_scouts(fresh_scouts, problem, request.analysis_budget))

    enriched_request = (
        replace(
            request,
            supplied_scout_evidence=request.supplied_scout_evidence + tuple(gathered),
        )
        if gathered
        else request
    )
    fingerprint = fingerprint_problem(problem, enriched_request.supplied_scout_evidence)

    candidates: list[RouteCandidate] = []
    refusals: list[RecognitionRefusal] = []
    unregistered: list[str] = []

    for family in request.available_route_families:
        provider = PROVIDERS.get(family)
        if provider is None:
            unregistered.append(family)
            continue
        outcome = provider.recognizer(enriched_request)
        if outcome.candidate is not None:
            candidates.append(outcome.candidate)
        else:
            assert outcome.refusal is not None
            refusals.append(outcome.refusal)
        if len(candidates) >= request.analysis_budget.max_candidates:
            break

    if not candidates:
        refusal = PlanningRefusal(
            code="no_admissible_route",
            reason="No registered recognizer admitted the request.",
            recognizer_refusals=tuple(refusals),
            unregistered_route_families=tuple(unregistered),
        )
        return PlanningOutcome(
            None,
            None,
            (),
            tuple(refusals),
            refusal,
            structural_fingerprint=fingerprint,
            gathered_scout_evidence=tuple(gathered),
        )

    selected, frontier, rejections = compare_candidates(tuple(candidates))
    return PlanningOutcome(
        route=selected.route,
        selected_candidate=selected,
        pareto_frontier=tuple(sorted(candidate.route.route_family for candidate in frontier)),
        recognizer_refusals=tuple(refusals),
        rejected_alternatives=rejections,
        structural_fingerprint=fingerprint,
        gathered_scout_evidence=tuple(gathered),
    )
