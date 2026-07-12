"""Measured structural burden used for Pareto comparison."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BurdenVector:
    invariant_level: int = 0
    global_expansion_rank: int = 0
    elimination_rank: int = 0
    exact_operation_count: int = 0
    scout_operation_count: int = 0
    expression_depth: int = 0

    def __post_init__(self) -> None:
        if any(value < 0 for value in self.as_tuple()):
            raise ValueError("burden components must be non-negative")

    def as_tuple(self) -> tuple[int, ...]:
        return (
            self.invariant_level,
            self.global_expansion_rank,
            self.elimination_rank,
            self.exact_operation_count,
            self.scout_operation_count,
            self.expression_depth,
        )

    def dominates(self, other: "BurdenVector") -> bool:
        left = self.as_tuple()
        right = other.as_tuple()
        return all(a <= b for a, b in zip(left, right)) and any(
            a < b for a, b in zip(left, right)
        )
