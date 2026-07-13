"""Uniform route/candidate assembly for provider recognizers."""

from __future__ import annotations

from ..api.contract import RecognitionOutcome, RouteCandidate, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import ComputationalRoute, RouteStep
from ..ir.burden import BurdenVector


def assemble_candidate(
    *,
    request: PathfinderRequest,
    contract: RouteContract,
    steps: tuple[RouteStep, ...],
    data_dependencies: tuple[str, ...],
    required_intermediate_objects: tuple[str, ...],
    completion_condition: str,
    burden_vector: BurdenVector,
    structural_preference_rank: int,
) -> RecognitionOutcome:
    """Build the admitted candidate with the contract's declared obligations."""

    route = ComputationalRoute(
        request_id=request.request_id,
        target_obligation=request.target_obligation,
        route_family=contract.route_family,
        ordered_steps=steps,
        data_dependencies=data_dependencies,
        external_binding=request.external_binding,
        required_intermediate_objects=required_intermediate_objects,
        required_hypotheses=contract.required_hypotheses,
        certificate_obligations=contract.certificate_obligations,
        exceptional_branches=contract.exceptional_branches,
        completion_condition=completion_condition,
        supporting_scout_evidence=request.supplied_scout_evidence,
    )
    return RecognitionOutcome(
        candidate=RouteCandidate(
            contract=contract,
            route=route,
            burden_vector=burden_vector,
            structural_preference_rank=structural_preference_rank,
        )
    )
