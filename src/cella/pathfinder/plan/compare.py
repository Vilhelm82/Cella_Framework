"""Deterministic route comparison with recorded loser evidence.

Order of the selection law (BUILD_SPEC §Selection law):
inadmissible candidates never reach this module; here the admitted frontier
is compared by invariant level, structural preference, Pareto burden
dominance, and a stable declared tie-break.  Every losing candidate receives
an explicit rejection record.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..api.contract import RouteCandidate


@dataclass(frozen=True, slots=True)
class RouteRejection:
    """Why one admitted candidate lost the comparison."""

    route_family: str
    stage: str  # pareto_dominated | invariant_level | structural_preference | burden_order | family_tie_break
    reason: str
    compared_to: str

    def __post_init__(self) -> None:
        if not all(
            value.strip() for value in (self.route_family, self.stage, self.reason, self.compared_to)
        ):
            raise ValueError("route rejection fields must be explicit")


def _selection_key(candidate: RouteCandidate) -> tuple[object, ...]:
    return (
        candidate.burden_vector.invariant_level,
        candidate.structural_preference_rank,
        candidate.burden_vector.as_tuple(),
        candidate.contract.route_family,
    )


def _loss_stage(winner: RouteCandidate, loser: RouteCandidate) -> tuple[str, str]:
    if loser.burden_vector.invariant_level > winner.burden_vector.invariant_level:
        return (
            "invariant_level",
            f"requires invariant level {loser.burden_vector.invariant_level} "
            f"above the sufficient level {winner.burden_vector.invariant_level}",
        )
    if loser.structural_preference_rank > winner.structural_preference_rank:
        return (
            "structural_preference",
            "a more direct structural route discharges the same target",
        )
    if loser.burden_vector.as_tuple() > winner.burden_vector.as_tuple():
        return (
            "burden_order",
            f"burden {loser.burden_vector.as_tuple()} exceeds {winner.burden_vector.as_tuple()} "
            "in the deterministic component order",
        )
    return (
        "family_tie_break",
        "identical burden; stable declared route-family tie-break applied",
    )


def compare_candidates(
    candidates: tuple[RouteCandidate, ...],
) -> tuple[RouteCandidate, tuple[RouteCandidate, ...], tuple[RouteRejection, ...]]:
    """(winner, pareto frontier, rejection records for every loser)."""

    if not candidates:
        raise ValueError("comparison requires at least one admitted candidate")
    rejections: list[RouteRejection] = []
    frontier: list[RouteCandidate] = []
    for candidate in candidates:
        dominator = next(
            (
                other
                for other in candidates
                if other is not candidate and other.burden_vector.dominates(candidate.burden_vector)
            ),
            None,
        )
        if dominator is None:
            frontier.append(candidate)
        else:
            rejections.append(
                RouteRejection(
                    route_family=candidate.contract.route_family,
                    stage="pareto_dominated",
                    reason=(
                        f"burden {candidate.burden_vector.as_tuple()} is Pareto-dominated by "
                        f"{dominator.burden_vector.as_tuple()}"
                    ),
                    compared_to=dominator.contract.route_family,
                )
            )
    winner = min(frontier, key=_selection_key)
    for candidate in frontier:
        if candidate is winner:
            continue
        stage, reason = _loss_stage(winner, candidate)
        rejections.append(
            RouteRejection(
                route_family=candidate.contract.route_family,
                stage=stage,
                reason=reason,
                compared_to=winner.contract.route_family,
            )
        )
    return winner, tuple(frontier), tuple(rejections)
