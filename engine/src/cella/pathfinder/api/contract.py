"""Route-family contract and recognition outcome types."""

from __future__ import annotations

from dataclasses import dataclass

from .route import ComputationalRoute
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation


@dataclass(frozen=True, slots=True)
class RouteContract:
    route_family: str
    accepted_problem_shape: str
    required_hypotheses: tuple[str, ...]
    required_evidence: tuple[str, ...]
    produced_obligations: tuple[Obligation, ...]
    discharged_obligations: tuple[str, ...]
    exceptional_branches: tuple[str, ...]
    execution_module: str
    certificate_obligations: tuple[Obligation, ...]
    source_references: tuple[str, ...]

    def __post_init__(self) -> None:
        required = (
            self.route_family,
            self.accepted_problem_shape,
            self.execution_module,
        )
        if not all(value.strip() for value in required):
            raise ValueError("route contract identity and execution module must be explicit")
        if not self.source_references:
            raise ValueError("a route contract must cite at least one source")


@dataclass(frozen=True, slots=True)
class RouteCandidate:
    contract: RouteContract
    route: ComputationalRoute
    burden_vector: BurdenVector
    structural_preference_rank: int

    def __post_init__(self) -> None:
        if self.contract.route_family != self.route.route_family:
            raise ValueError("route candidate family does not match its contract")
        if self.structural_preference_rank < 0:
            raise ValueError("structural preference rank must be non-negative")


@dataclass(frozen=True, slots=True)
class RecognitionRefusal:
    route_family: str
    code: str
    reason: str
    unmet_requirements: tuple[str, ...]

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.route_family, self.code, self.reason)):
            raise ValueError("recognition refusal fields must be explicit")


@dataclass(frozen=True, slots=True)
class RecognitionOutcome:
    candidate: RouteCandidate | None = None
    refusal: RecognitionRefusal | None = None

    def __post_init__(self) -> None:
        if (self.candidate is None) == (self.refusal is None):
            raise ValueError("recognition outcome requires exactly one of candidate or refusal")
