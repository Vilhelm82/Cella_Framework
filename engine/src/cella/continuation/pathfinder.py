"""PF-0-scoped constructor for the six recertified DBP native requests.

This is deliberately not a general route finder.  It turns one member of the
finite recertified request domain into the exact schedule that the legacy
executor independently re-proves panel by panel.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
from pathlib import Path

from cella.pathfinder import Obligation, PathfinderRequest, plan_request
from cella.pathfinder.recognize.dbp_native import CORRIDOR_ROUTE_FAMILY, ROUTE_FAMILY
from cella.pathfinder.serialize import canonical_json_bytes as pathfinder_canonical_bytes
from cella.native_periods.schedule import admitted_m1_schedule

from .canonical import canonical_digest
from .corridors import CORRIDORS, exact_certificate_digest, verify_manifest
from .model import (
    CoefficientRing,
    CorridorContinuationRequest,
    CorridorPathfinderPlan,
    ContinuationRequest,
    PathfinderPlan,
    Refusal,
    UnsupportedRequest,
)


PATHFINDER_VERSION = "cella.pathfinder.typed_core.dbp_native.v1"
ADMITTED_DOMAIN_ID = "cella.cce.dbp_native.schema_1_1.released_six.v1"
ADAPTER_ID = "cella.continuation.adapters.dbp_native_v1"
ADAPTER_VERSION = "1.1"
STATIC_SCHEDULE_DIGEST = "02241f86d41253a5af4f126aafbd1e1ab618de6faf924a38dd96326903857d41"
PF0_CONFIRMATION_DIGEST = "304fccce5ed1206f23969952634d10b250d8d4d7a7a955971afa8018c2372008"
PF0_V1_SOURCE_DIGEST = "0fd5afbb455fc5b142165a0f30692b54786f2f391fbc973cb1ec2cab3139bee5"
CORRIDOR_PATHFINDER_VERSION = "cella.pathfinder.typed_core.dbp_exact_corridor.v1"
CORRIDOR_ADAPTER_ID = "cella.continuation.adapters.dbp_exact_corridor_v1"
CORRIDOR_ADAPTER_VERSION = "1.0"
CORRIDOR_DIVISOR_MANIFEST_DIGEST = "cf893db1c6c2718a614dfdf519e220cbb3b7312aff62130c608ddd7598c1c93a"
CORRIDOR_THEOREM_DIGEST = "bfb0dc4c4678803cc46e791cbe60e87736ea41ce14db157e8fb1726e28b671fe"
CORRIDOR_FAMILY_MANIFEST_DIGEST = canonical_digest({
    "family": "DBP shear-cover exact curve corridor transport",
    "cover": "rho^2=1+sigma^2",
    "base": "C minus {0,+i,-i}",
    "source_class": "delta_+",
    "quotient": "relative homology modulo Z[A]+Z[B]",
})

FAMILY_MANIFEST = {
    "family": "DBP fixed E128 native relative-period evaluator",
    "curve": "Y^2=(X-1)(X^2+1)",
    "differential": "Theta=8*(X-3)/(X+7)*dX/Y",
    "certificate_schema": "1.1",
    "targets": ("primary", "dual_cpv"),
}
FAMILY_MANIFEST_DIGEST = canonical_digest(FAMILY_MANIFEST)

_TARGETS = {
    "primary": {
        "kernel_id": "g_plus_v1",
        "path": "X=1 to X=+infinity; increasing_X; Y>0 for X>1; ordinary",
        "state": "primary selected relative path",
        "ring": CoefficientRing.Z,
    },
    "dual_cpv": {
        "kernel_id": "g_minus_v1",
        "path": "X=1 to X=-infinity; decreasing_X; upper physical sheet; real CPV",
        "state": "dual CPV midpoint with i-normalization",
        "ring": CoefficientRing.Z_HALF_I,
    },
}
ADMITTED_BITS = (192, 256, 384)
ADMITTED_REQUESTS = tuple(
    (target, bits) for bits in ADMITTED_BITS for target in ("primary", "dual_cpv")
)


def exact_path_digest(target: str) -> str:
    return canonical_digest({"target": target, "path": _TARGETS[target]["path"]})


def selected_state_digest(target: str) -> str:
    return canonical_digest({"target": target, "state": _TARGETS[target]["state"]})


def released_request(target: str, requested_bits: int) -> ContinuationRequest:
    if target not in _TARGETS:
        raise ValueError(f"unknown released DBP target {target!r}")
    return ContinuationRequest(
        request_id=f"dbp-native-{target}-{requested_bits}",
        adapter_id=ADAPTER_ID,
        adapter_version=ADAPTER_VERSION,
        target=target,
        requested_bits=requested_bits,
        family_manifest_digest=FAMILY_MANIFEST_DIGEST,
        exact_path_digest=exact_path_digest(target),
        selected_state_digest=selected_state_digest(target),
        coefficient_ring=_TARGETS[target]["ring"],
    )


def _unsupported(
    request: ContinuationRequest,
    code: str,
    obligation: str,
    detail: str,
) -> UnsupportedRequest:
    return UnsupportedRequest(
        request,
        Refusal(
            code=code,
            failed_obligation=obligation,
            source_location="cella.continuation.pathfinder.construct_plan",
            larger_budget_may_help=False,
            new_theorem_or_adapter_required=True,
            detail=detail,
        ),
    )


def construct_plan(
    request: ContinuationRequest,
) -> PathfinderPlan | UnsupportedRequest:
    pf_request = PathfinderRequest.create(
        request_id=request.request_id,
        target_obligation=Obligation(
            "cce-certified-result",
            "Produce the recertified DBP result with a CCE route/evaluation envelope.",
            "exact-manifest-and-replay",
        ),
        external_binding={
            "continuation_request": request.request_id,
            "m1_schedule": "package:cella.native_periods/m1_schedule.json",
        },
        mathematical_context={
            "problem_shape": "dbp_native_released_evaluation",
            "adapter_id": request.adapter_id,
            "adapter_version": request.adapter_version,
            "target": request.target,
            "requested_bits": request.requested_bits,
            "family_manifest_digest": request.family_manifest_digest,
            "exact_path_digest": request.exact_path_digest,
            "selected_state_digest": request.selected_state_digest,
            "coefficient_ring": request.coefficient_ring.value,
        },
        available_route_families=(ROUTE_FAMILY,),
    )
    outcome = plan_request(pf_request)
    if outcome.route is None:
        refusal = outcome.recognizer_refusals[0] if outcome.recognizer_refusals else None
        return _unsupported(
            request,
            refusal.code if refusal is not None else "unsupported_path",
            refusal.unmet_requirements[0] if refusal is not None and refusal.unmet_requirements else "pathfinder_admission",
            refusal.reason if refusal is not None else "Pathfinder found no admitted route",
        )

    target = _TARGETS.get(request.target)
    if target is None:
        return _unsupported(request, "unsupported_path", "route_identity", "target is outside the released DBP pair")
    schedule = admitted_m1_schedule(str(target["kernel_id"]))
    panel_schedule: list[tuple[int, int, int, int]] = []
    for item in schedule["panel_schedules"]:
        log2_lower = {
            2: Fraction(1),
            3: Fraction(3, 2),
            4: Fraction(2),
            6: Fraction(5, 2),
            8: Fraction(3),
        }[item["radius_multiplier"]]
        quotient = Fraction(request.requested_bits + 24, 1) / log2_lower
        required_order = (
            quotient.numerator + quotient.denominator - 1
        ) // quotient.denominator
        order = max(item["order"], required_order)
        work_bits = request.requested_bits + item["guard_bits"]
        panel_schedule.append(
            (item["panel"], order, work_bits, item["radius_multiplier"])
        )

    canonical_route = pathfinder_canonical_bytes(outcome.route)
    # CCE-1 is a frozen PF-0 certificate domain.  Its historical source closure
    # remains bound by the recorded digest even as later route families are
    # added to the registry; CCE-2 binds the new live closure independently.
    source_digest = PF0_V1_SOURCE_DIGEST
    unsigned = {
        "schema_id": "cella.continuation.pathfinder_plan",
        "pathfinder_version": PATHFINDER_VERSION,
        "pathfinder_source_digest": source_digest,
        "admitted_domain_id": ADMITTED_DOMAIN_ID,
        "request_digest": canonical_digest(request),
        "target": request.target,
        "requested_bits": request.requested_bits,
        "kernel_id": target["kernel_id"],
        "static_schedule_digest": STATIC_SCHEDULE_DIGEST,
        "canonical_route_json": canonical_route.decode("utf-8"),
        "computational_route_digest": hashlib.sha256(canonical_route).hexdigest(),
        "panel_schedule": tuple(panel_schedule),
        "constructor_invariants": (
            "typed Cella Pathfinder provider admits exact adapter, family, path, state, ring, target and precision",
            "static schedule schema and obligation tuple admitted",
            "panel schedule is an exact ordered partition of 0..31",
            "orders and working precision are deterministic rational functions of the request",
            "executor independently re-proves domain, radii, account and remainder",
        ),
        "numeric_representation": "integers and exact Fractions only; no binary floating point",
    }
    return PathfinderPlan(**unsigned, plan_digest=canonical_digest(unsigned))


def plan_fits_budget(request: ContinuationRequest, plan: PathfinderPlan) -> bool:
    """Adequacy check kept separate from constructor validity."""

    return (
        len(plan.panel_schedule) <= request.proof_budget.max_steps
        and max(item[1] for item in plan.panel_schedule)
        <= request.proof_budget.max_recurrence_order
        and max(item[2] for item in plan.panel_schedule)
        <= request.proof_budget.max_work_bits
    )


def released_corridor_request(route: str) -> CorridorContinuationRequest:
    if route not in CORRIDORS:
        raise ValueError(f"unknown exact DBP corridor {route!r}")
    manifest = CORRIDORS[route]
    return CorridorContinuationRequest(
        request_id=f"dbp-exact-corridor-{route}",
        adapter_id=CORRIDOR_ADAPTER_ID,
        adapter_version=CORRIDOR_ADAPTER_VERSION,
        route_id=manifest.route_id,
        family_manifest_digest=CORRIDOR_FAMILY_MANIFEST_DIGEST,
        divisor_manifest_digest=CORRIDOR_DIVISOR_MANIFEST_DIGEST,
        route_manifest_digest=manifest.digest,
        theorem_digest=CORRIDOR_THEOREM_DIGEST,
        selected_state_digest=canonical_digest({
            "source": manifest.selected_source_class,
            "target": manifest.selected_target_quotient_class,
            "compact_correction": manifest.unresolved_compact_correction,
        }),
        coefficient_ring=CoefficientRing.Z,
        surface_scope="curve_only",
    )


def _live_pathfinder_source_digest() -> str:
    pathfinder_root = Path(__file__).parents[1] / "pathfinder"
    return canonical_digest(tuple(
        (str(path.relative_to(Path(__file__).parents[2])), hashlib.sha256(path.read_bytes()).hexdigest())
        for path in sorted(pathfinder_root.rglob("*.py"))
    ))


def construct_corridor_plan(request: CorridorContinuationRequest) -> CorridorPathfinderPlan | Refusal:
    manifest = next((item for item in CORRIDORS.values() if item.route_id == request.route_id), None)
    if manifest is None:
        return Refusal("unsupported_path", "route_identity", "cella.continuation.pathfinder.construct_corridor_plan", False, True, "route is outside the exact upper/lower corridor pair")
    try:
        verify_manifest(manifest)
    except ValueError as exc:
        return Refusal(str(exc), "exact_corridor_manifest", "cella.continuation.corridors.verify_manifest", False, True, "exact corridor theorem replay failed")
    pf_request = PathfinderRequest.create(
        request_id=request.request_id,
        target_obligation=Obligation("cce2-exact-corridor", "Construct the theorem-bound DBP corridor transport plan.", "exact-rational-replay"),
        external_binding={"continuation_request": request.request_id},
        mathematical_context={
            "problem_shape": "dbp_exact_corridor_transport",
            "adapter_id": request.adapter_id,
            "adapter_version": request.adapter_version,
            "route_id": request.route_id,
            "family_manifest_digest": request.family_manifest_digest,
            "divisor_manifest_digest": request.divisor_manifest_digest,
            "route_manifest_digest": request.route_manifest_digest,
            "theorem_digest": request.theorem_digest,
            "selected_state_digest": request.selected_state_digest,
            "coefficient_ring": request.coefficient_ring.value,
            "surface_scope": request.surface_scope,
            "vertices_digest": canonical_digest(manifest.vertices),
            "free_group_word": manifest.free_group_word,
            "windings": manifest.windings,
            "initial_sheet": manifest.initial_sheet,
            "terminal_sheet": manifest.terminal_sheet,
            "tube_radius": manifest.tube_radius,
            "clearance_certificate_digest": exact_certificate_digest(manifest),
        },
        available_route_families=(CORRIDOR_ROUTE_FAMILY,),
    )
    outcome = plan_request(pf_request)
    if outcome.route is None:
        refusal = outcome.recognizer_refusals[0] if outcome.recognizer_refusals else None
        return Refusal(refusal.code if refusal else "unsupported_path", (refusal.unmet_requirements[0] if refusal and refusal.unmet_requirements else "pathfinder_admission"), "cella.continuation.pathfinder.construct_corridor_plan", False, True, refusal.reason if refusal else "Pathfinder found no exact corridor route")
    canonical_route = pathfinder_canonical_bytes(outcome.route)
    provider_path = Path(__file__).parents[1] / "pathfinder/recognize/dbp_native.py"
    unsigned = {
        "schema_id": "cella.continuation.corridor_pathfinder_plan",
        "pathfinder_version": CORRIDOR_PATHFINDER_VERSION,
        "pathfinder_source_digest": _live_pathfinder_source_digest(),
        "provider_source_digest": hashlib.sha256(provider_path.read_bytes()).hexdigest(),
        "pf0_confirmation_digest": PF0_CONFIRMATION_DIGEST,
        "request_digest": canonical_digest(request),
        "route_id": request.route_id,
        "canonical_route_json": canonical_route.decode("utf-8"),
        "computational_route_digest": hashlib.sha256(canonical_route).hexdigest(),
        "constructor_invariants": (
            "exact Q(i) vertices and structural free-group word replayed",
            "positive rational route and radius-1/8 tube clearance replayed",
            "unique path lift and odd deck parity replayed without nearest-root selection",
            "curve divisor, lateral class, theorem and production source digests bound",
            "surface scope explicitly refused",
        ),
    }
    return CorridorPathfinderPlan(**unsigned, plan_digest=canonical_digest(unsigned))
