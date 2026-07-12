"""Non-verdict-bearing route-discovery evidence."""

from __future__ import annotations

from dataclasses import dataclass

from .burden import BurdenVector
from .scope import Scope
from .values import FrozenValue


@dataclass(frozen=True, slots=True)
class ScoutEvidence:
    scout_family: str
    scope: Scope
    structural_fingerprint: tuple[tuple[str, FrozenValue], ...]
    actual_trace: tuple[str, ...]
    burden_vector: BurdenVector
    stability: str
    unresolved_inputs: tuple[str, ...] = ()
    retained_artifact_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.scout_family.strip() or not self.stability.strip():
            raise ValueError("scout family and stability must be explicit")
        if self.stability not in {"exact", "stable", "conditional", "unstable"}:
            raise ValueError(f"unknown scout stability: {self.stability}")
