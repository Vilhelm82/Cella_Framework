"""Shared admissibility helpers for route-family recognizers.

Recognizers refuse for mathematically explicit reasons, never for missing
implementation.  These helpers keep refusal records uniform across the
provider registry.
"""

from __future__ import annotations

from ..api.contract import RecognitionOutcome, RecognitionRefusal
from ..api.request import PathfinderRequest
from ..ir.values import FrozenValue


def lookup(items: tuple[tuple[str, FrozenValue], ...], key: str) -> FrozenValue | None:
    return next((value for item_key, value in items if item_key == key), None)


def refuse(
    route_family: str,
    code: str,
    reason: str,
    *requirements: str,
) -> RecognitionOutcome:
    return RecognitionOutcome(
        refusal=RecognitionRefusal(
            route_family=route_family,
            code=code,
            reason=reason,
            unmet_requirements=tuple(requirements),
        )
    )


def family_enabled(request: PathfinderRequest, route_family: str) -> RecognitionOutcome | None:
    if route_family not in request.available_route_families:
        return refuse(
            route_family,
            "route_not_enabled",
            "The wrapper did not enable this route family.",
            route_family,
        )
    return None


def require_shape(
    request: PathfinderRequest,
    route_family: str,
    accepted_shape: str,
) -> RecognitionOutcome | None:
    shape = lookup(request.mathematical_context, "problem_shape")
    if shape != accepted_shape:
        return refuse(
            route_family,
            "shape_mismatch",
            f"The task does not declare problem shape {accepted_shape!r}.",
            accepted_shape,
        )
    return None


def require_odd_characteristic(
    request: PathfinderRequest,
    route_family: str,
) -> RecognitionOutcome | None:
    """Characteristic must be declared exactly and must not be two."""

    characteristic = lookup(request.mathematical_context, "characteristic")
    if not isinstance(characteristic, int) or isinstance(characteristic, bool):
        return refuse(
            route_family,
            "missing_characteristic",
            "The coefficient characteristic must be declared exactly.",
            "integer characteristic",
        )
    if characteristic == 2:
        return refuse(
            route_family,
            "characteristic_two",
            "This route family is not admissible in characteristic two.",
            "characteristic != 2",
        )
    return None


def evidence_by_family(
    request: PathfinderRequest,
    scout_family: str,
) -> dict[str, FrozenValue] | None:
    for item in request.supplied_scout_evidence:
        if item.scout_family == scout_family:
            return dict(item.structural_fingerprint)
    return None
