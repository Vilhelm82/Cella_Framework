"""Wrapper-neutral Pathfinder request."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from ..ir.evidence import ScoutEvidence
from ..ir.obligation import Obligation
from ..ir.scope import AnalysisBudget
from ..ir.values import FrozenValue, freeze_mapping


@dataclass(frozen=True, slots=True)
class PathfinderRequest:
    """A route-analysis request; host bindings remain opaque values."""

    request_id: str
    target_obligation: Obligation
    external_binding: tuple[tuple[str, FrozenValue], ...]
    mathematical_context: tuple[tuple[str, FrozenValue], ...]
    available_route_families: tuple[str, ...]
    supplied_scout_evidence: tuple[ScoutEvidence, ...] = ()
    already_discharged_obligations: tuple[str, ...] = ()
    analysis_budget: AnalysisBudget = field(default_factory=AnalysisBudget)

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id must be non-empty")
        if not self.available_route_families:
            raise ValueError("at least one route family must be available")
        if len(set(self.available_route_families)) != len(self.available_route_families):
            raise ValueError("available route families must be unique")

    @classmethod
    def create(
        cls,
        *,
        request_id: str,
        target_obligation: Obligation,
        external_binding: Mapping[str, object],
        mathematical_context: Mapping[str, object],
        available_route_families: tuple[str, ...],
        supplied_scout_evidence: tuple[ScoutEvidence, ...] = (),
        already_discharged_obligations: tuple[str, ...] = (),
        analysis_budget: AnalysisBudget | None = None,
    ) -> "PathfinderRequest":
        return cls(
            request_id=request_id,
            target_obligation=target_obligation,
            external_binding=freeze_mapping(external_binding),
            mathematical_context=freeze_mapping(mathematical_context),
            available_route_families=available_route_families,
            supplied_scout_evidence=supplied_scout_evidence,
            already_discharged_obligations=already_discharged_obligations,
            analysis_budget=analysis_budget or AnalysisBudget(),
        )
