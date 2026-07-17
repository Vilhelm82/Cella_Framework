"""Minimal typed selected skeleton used by post-CCE-8 reduction functors.

This module deliberately models only the common transport data.  It does not
assert equivalence of the unreduced realizations.
"""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import canonical_digest


@dataclass(frozen=True, slots=True)
class SelectedSkeletonObject:
    realization_id: str
    base_digest: str
    selected_divisor: str
    incidence_stratum: str
    selected_branch: str
    local_symmetry: str
    coefficient_domain: str
    orientation: int
    object_digest: str

    @classmethod
    def build(
        cls,
        *,
        realization_id: str,
        base_digest: str,
        selected_divisor: str,
        incidence_stratum: str,
        selected_branch: str,
        local_symmetry: str,
        coefficient_domain: str,
        orientation: int,
    ) -> "SelectedSkeletonObject":
        if orientation not in (-1, 1):
            raise ValueError("selected-skeleton orientation must be +1 or -1")
        unsigned = {
            "realization_id": realization_id,
            "base_digest": base_digest,
            "selected_divisor": selected_divisor,
            "incidence_stratum": incidence_stratum,
            "selected_branch": selected_branch,
            "local_symmetry": local_symmetry,
            "coefficient_domain": coefficient_domain,
            "orientation": orientation,
        }
        return cls(**unsigned, object_digest=canonical_digest(unsigned))


@dataclass(frozen=True, slots=True)
class SelectedSkeletonMorphism:
    source: SelectedSkeletonObject
    target: SelectedSkeletonObject
    monodromy_parity: int
    route_class: str
    morphism_digest: str

    @classmethod
    def build(
        cls,
        source: SelectedSkeletonObject,
        target: SelectedSkeletonObject,
        monodromy_parity: int,
        route_class: str,
    ) -> "SelectedSkeletonMorphism":
        if monodromy_parity not in (0, 1):
            raise ValueError("selected-skeleton monodromy parity must be zero or one")
        if source.base_digest != target.base_digest:
            raise ValueError("selected-skeleton morphisms require one parameter base")
        if source.realization_id != target.realization_id:
            raise ValueError("cross-realization arrows require a separately proved comparison functor")
        unsigned = {
            "source": source,
            "target": target,
            "monodromy_parity": monodromy_parity,
            "route_class": route_class,
        }
        return cls(**unsigned, morphism_digest=canonical_digest(unsigned))


def identity_skeleton_morphism(obj: SelectedSkeletonObject) -> SelectedSkeletonMorphism:
    return SelectedSkeletonMorphism.build(obj, obj, 0, "identity")


def compose_skeleton_morphisms(
    first: SelectedSkeletonMorphism,
    second: SelectedSkeletonMorphism,
) -> SelectedSkeletonMorphism:
    """Return second after first."""
    if first.target != second.source:
        raise ValueError("selected-skeleton morphisms are not composable")
    parity = first.monodromy_parity ^ second.monodromy_parity
    return SelectedSkeletonMorphism.build(
        first.source,
        second.target,
        parity,
        f"({first.route_class});({second.route_class})",
    )


__all__ = [
    "SelectedSkeletonMorphism",
    "SelectedSkeletonObject",
    "compose_skeleton_morphisms",
    "identity_skeleton_morphism",
]
