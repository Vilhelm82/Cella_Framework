"""Explicit scope and bounded-analysis controls."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Scope:
    object_family: str
    coefficient_domain: str
    characteristic: int | None
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.object_family.strip() or not self.coefficient_domain.strip():
            raise ValueError("scope object family and coefficient domain must be non-empty")
        if self.characteristic is not None and self.characteristic < 0:
            raise ValueError("characteristic must be non-negative or None")


@dataclass(frozen=True, slots=True)
class AnalysisBudget:
    max_scout_steps: int = 10_000
    max_candidates: int = 64
    max_expression_nodes: int = 100_000

    def __post_init__(self) -> None:
        if min(self.max_scout_steps, self.max_candidates, self.max_expression_nodes) <= 0:
            raise ValueError("analysis budget limits must be positive")
