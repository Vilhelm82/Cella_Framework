"""Typed route returned by Pathfinder."""

from __future__ import annotations

from dataclasses import dataclass

from ..ir.evidence import ScoutEvidence
from ..ir.obligation import Obligation
from ..ir.values import FrozenValue


@dataclass(frozen=True, slots=True)
class RouteStep:
    step_id: str
    operation: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    parameters: tuple[tuple[str, FrozenValue], ...] = ()

    def __post_init__(self) -> None:
        if not self.step_id.strip() or not self.operation.strip():
            raise ValueError("route step id and operation must be non-empty")


@dataclass(frozen=True, slots=True)
class ComputationalRoute:
    """Instructions for an external executor, never a mathematical result."""

    request_id: str
    target_obligation: Obligation
    route_family: str
    ordered_steps: tuple[RouteStep, ...]
    data_dependencies: tuple[str, ...]
    external_binding: tuple[tuple[str, FrozenValue], ...]
    required_intermediate_objects: tuple[str, ...]
    required_hypotheses: tuple[str, ...]
    certificate_obligations: tuple[Obligation, ...]
    exceptional_branches: tuple[str, ...]
    completion_condition: str
    supporting_scout_evidence: tuple[ScoutEvidence, ...] = ()

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.route_family.strip():
            raise ValueError("request id and route family must be non-empty")
        if not self.ordered_steps:
            raise ValueError("a computational route must contain at least one step")
        if not self.completion_condition.strip():
            raise ValueError("completion condition must be explicit")
        ids = tuple(step.step_id for step in self.ordered_steps)
        if len(set(ids)) != len(ids):
            raise ValueError("route step ids must be unique")
