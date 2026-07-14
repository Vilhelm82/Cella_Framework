"""Exact provider for the six recertified DBP native evaluator requests."""

from __future__ import annotations

import hashlib
from importlib.resources import files
from fractions import Fraction

from cella.native_periods.schedule import admitted_m1_schedule

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.values import FrozenValue, freeze_mapping
from ..plan.admissibility import refuse
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider


ROUTE_FAMILY = "dbp_native_released_evaluation"
CORRIDOR_ROUTE_FAMILY = "dbp_exact_corridor_transport"
STATIC_SCHEDULE_DIGEST = "02241f86d41253a5af4f126aafbd1e1ab618de6faf924a38dd96326903857d41"
FAMILY_MANIFEST_DIGEST = "3f730d9537d7829f073d7e0c891aa21e30bb42e317f2a133cc1d74a93e7dc5f6"
ADMITTED_BITS = (192, 256, 384)
TARGETS = {
    "primary": {
        "kernel_id": "g_plus_v1",
        "path_digest": "35a3db5a24d6af74cd12bf5b06b403dfb69c43604655464f5201a5d764902570",
        "state_digest": "c462da0c7ff0efbc2a255994e69c4bc4b4a7000316d4378470007b4c3273c939",
        "coefficient_ring": "Z",
    },
    "dual_cpv": {
        "kernel_id": "g_minus_v1",
        "path_digest": "46981c5d8628fa70718f4fa5c01db19fa51987881d3aa50edd1b0ec00a63ea47",
        "state_digest": "1c76cfb309ed11e30738ca2e6ef1961bdf7770648dd20a4f3081f9c9cae658ac",
        "coefficient_ring": "Z[1/2,i]",
    },
}

CERTIFICATE_OBLIGATIONS = (
    Obligation("dbp-route-identity", "Replay the exact target, path, sheet and source ledger.", "exact-manifest"),
    Obligation("dbp-schedule-admission", "Replay the static schedule digest, schema, obligations and panel partition.", "exact-schedule"),
    Obligation("dbp-analytic-account", "Prove every panel radius and Cauchy remainder at execution time.", "certified-recurrence"),
    Obligation("dbp-arithmetic-account", "Replay the fixed-DAG arithmetic account.", "exact-account"),
    Obligation("dbp-envelope-link", "Link the verified legacy certificate into the CCE route/evaluation envelope.", "canonical-digest"),
)

DBP_NATIVE_CONTRACT = RouteContract(
    route_family=ROUTE_FAMILY,
    accepted_problem_shape="dbp_native_released_evaluation",
    required_hypotheses=(
        "adapter version is exactly 1.1",
        "target and requested precision belong to the recertified six-request domain",
        "family, path, selected state and coefficient ring match their exact digests",
        "packaged M1 schedule matches the PF-0 digest and admission rules",
    ),
    required_evidence=("schema-1.1 CCE-0 recertification lock",),
    produced_obligations=CERTIFICATE_OBLIGATIONS,
    discharged_obligations=(),
    exceptional_branches=(
        "larger or different precision requires a separately confirmed Pathfinder domain",
        "different path, sheet, state or ring requires a continuation-stage adapter",
    ),
    execution_module="cella.continuation.adapters.dbp_native_v1",
    certificate_obligations=CERTIFICATE_OBLIGATIONS,
    source_references=(
        "research/campaigns/CELLA_CONTINUATION_ENGINE/01_cce0_recertification/CCE_0_BASELINE_LOCK_v1.1.json",
        "research/campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_BUILD_SPEC_v1.0.md",
    ),
)

CORRIDOR_ROUTES = {
    "dbp_corridor_upper_qi_v1": {
        "route_manifest_digest": "63e19e63181d9573590d2ff4825787c95f4ecc1b99da8d510df370b7ccfaa62d",
        "vertices_digest": "5ecf7206162d574c926947852ec2aaa710926f45f6c287846523f28e7fe34c25",
        "selected_state_digest": "d933ac4b9ba1c74709f9082a071c8dd04f2cadb22a2b07e0a5f07c465cc66adb",
        "clearance_certificate_digest": "c4c9fae572cd9ca02ffdc493389c738731a961df9e7593b0be72382bf8e2240a",
        "free_group_word": "a_+",
        "windings": (("sigma_zero", 0), ("plus_i", 1), ("minus_i", 0)),
        "target": "[delta_-^up] mod Z[A]+Z[B]",
    },
    "dbp_corridor_lower_qi_v1": {
        "route_manifest_digest": "6216ca406c364cf382baabb7f6ea112ed095ce2393ac9d63f06636d5157565b5",
        "vertices_digest": "bc06c45e2a779d911cd562784e9ba8bc098ee76b766d3235abe8d4ba723f2a0d",
        "selected_state_digest": "0e80d13849c17e2394ba932107f03048dabe9c682f3961dbf4a09f3791b40232",
        "clearance_certificate_digest": "9cf591af652d6c9e7e5609f8641ef00b78c6c8e7434d8d2be0ae6291fbff0217",
        "free_group_word": "a_-^(-1)",
        "windings": (("sigma_zero", 0), ("plus_i", 0), ("minus_i", -1)),
        "target": "[delta_-^down] mod Z[A]+Z[B]",
    },
}

DBP_CORRIDOR_CONTRACT = RouteContract(
    route_family=CORRIDOR_ROUTE_FAMILY,
    accepted_problem_shape="dbp_exact_corridor_transport",
    required_hypotheses=(
        "route is one of the two theorem-bound Q(i) polygons",
        "family, divisor, route, state and theorem digests match",
        "exact structural word, winding vector, sheets and tube radius match",
        "scope is curve-only and excludes surface clearance",
    ),
    required_evidence=("CCE-2R exact positive-clearance theorem",),
    produced_obligations=(
        Obligation("corridor-identity", "Replay vertices, structural word and Stage-3 corridor identity.", "exact-Q(i)-manifest"),
        Obligation("corridor-clearance", "Replay base, tube, curve divisor and pole separation.", "exact-rational-bounds"),
        Obligation("corridor-lift", "Replay overlap chain and odd deck parity.", "algebraic-isolators"),
        Obligation("corridor-lateral", "Replay the exact return-stem sign and quotient class.", "algebraic-sign"),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "any changed vertex or orientation restarts theorem identity",
        "surface observables require CCE-6 surface clearance",
    ),
    execution_module="cella.continuation.corridors",
    certificate_obligations=(),
    source_references=(
        "research/campaigns/CELLA_CONTINUATION_ENGINE/03_cce2_corridors/DBP_EXACT_CORRIDOR_POSITIVE_CLEARANCE_THEOREM_v1.0.md",
        "research/campaigns/CELLA_CONTINUATION_ENGINE/03_cce2_corridors/DBP_EXACT_CORRIDOR_DIVISOR_REDUCTION_v1.0.md",
        "research/campaigns/CELLA_CONTINUATION_ENGINE/03_cce2_corridors/DBP_CORRIDOR_LATERAL_CALIBRATION_v1.0.md",
    ),
)


def _lookup(items: tuple[tuple[str, FrozenValue], ...], key: str) -> FrozenValue | None:
    return next((value for item_key, value in items if item_key == key), None)


def _reject(code: str, reason: str, *requirements: str) -> RecognitionOutcome:
    return refuse(ROUTE_FAMILY, code, reason, *requirements)


def recognize_dbp_native_released(request: PathfinderRequest) -> RecognitionOutcome:
    if ROUTE_FAMILY not in request.available_route_families:
        return _reject("route_not_enabled", "The wrapper did not enable the DBP native route.", ROUTE_FAMILY)
    if _lookup(request.mathematical_context, "problem_shape") != DBP_NATIVE_CONTRACT.accepted_problem_shape:
        return _reject("shape_mismatch", "The request is not a DBP native released evaluation.", DBP_NATIVE_CONTRACT.accepted_problem_shape)
    if _lookup(request.mathematical_context, "adapter_id") != "cella.continuation.adapters.dbp_native_v1":
        return _reject("unsupported_adapter", "Adapter identity is outside the confirmed scope.", "dbp_native_v1")
    if _lookup(request.mathematical_context, "adapter_version") != "1.1":
        return _reject("unsupported_adapter", "Adapter version is outside the confirmed scope.", "1.1")

    target_name = _lookup(request.mathematical_context, "target")
    if not isinstance(target_name, str) or target_name not in TARGETS:
        return _reject("unsupported_path", "Target is outside the released DBP pair.", "primary or dual_cpv")
    target = TARGETS[target_name]
    requested_bits = _lookup(request.mathematical_context, "requested_bits")
    if isinstance(requested_bits, bool) or requested_bits not in ADMITTED_BITS:
        return _reject("unsupported_path", "Precision is outside the recertified six-request domain.", "192, 256, or 384")

    expected = (
        ("family_manifest_digest", FAMILY_MANIFEST_DIGEST),
        ("exact_path_digest", target["path_digest"]),
        ("selected_state_digest", target["state_digest"]),
        ("coefficient_ring", target["coefficient_ring"]),
    )
    for key, value in expected:
        if _lookup(request.mathematical_context, key) != value:
            return _reject("route_identity_failed", f"{key} does not match the confirmed manifest.", key)

    schedule_bytes = files("cella.native_periods").joinpath("m1_schedule.json").read_bytes()
    if hashlib.sha256(schedule_bytes).hexdigest() != STATIC_SCHEDULE_DIGEST:
        return _reject("route_identity_failed", "Packaged M1 schedule digest changed.", "static schedule digest")
    schedule = admitted_m1_schedule(str(target["kernel_id"]))

    steps = (
        RouteStep(
            "bind-source",
            "bind_exact_dbp_native_source",
            ("continuation_request",),
            ("bound_native_request",),
            freeze_mapping({"target": target_name, "requested_bits": requested_bits}),
        ),
        RouteStep(
            "admit-schedule",
            "admit_static_recurrence_schedule",
            ("bound_native_request", "m1_schedule"),
            ("admitted_schedule",),
            freeze_mapping({
                "kernel_id": target["kernel_id"],
                "panels": schedule["panels"],
                "schedule_digest": STATIC_SCHEDULE_DIGEST,
            }),
        ),
        RouteStep(
            "execute-native",
            "execute_native_evaluator_with_runtime_proofs",
            ("bound_native_request", "admitted_schedule"),
            ("legacy_result", "legacy_certificate"),
        ),
        RouteStep(
            "verify-native",
            "verify_native_certificate",
            ("legacy_certificate",),
            ("verified_legacy_certificate",),
        ),
        RouteStep(
            "assemble-cce-envelope",
            "assemble_cce_route_and_evaluation_certificates",
            ("bound_native_request", "admitted_schedule", "verified_legacy_certificate"),
            ("certified_result",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=DBP_NATIVE_CONTRACT,
        steps=steps,
        data_dependencies=("continuation_request", "m1_schedule"),
        required_intermediate_objects=(
            "bound_native_request",
            "admitted_schedule",
            "legacy_result",
            "verified_legacy_certificate",
        ),
        completion_condition="The CCE envelope links a verified recertified legacy certificate to the exact Pathfinder route.",
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=5,
            scout_operation_count=0,
            expression_depth=1,
        ),
        structural_preference_rank=0,
    )


def recognize_dbp_exact_corridor(request: PathfinderRequest) -> RecognitionOutcome:
    def reject(code: str, reason: str, *requirements: str) -> RecognitionOutcome:
        return refuse(CORRIDOR_ROUTE_FAMILY, code, reason, *requirements)

    if CORRIDOR_ROUTE_FAMILY not in request.available_route_families:
        return reject("route_not_enabled", "The exact DBP corridor route was not enabled.", CORRIDOR_ROUTE_FAMILY)
    if _lookup(request.mathematical_context, "problem_shape") != DBP_CORRIDOR_CONTRACT.accepted_problem_shape:
        return reject("shape_mismatch", "The request is not an exact DBP corridor transport.", DBP_CORRIDOR_CONTRACT.accepted_problem_shape)
    route_id = _lookup(request.mathematical_context, "route_id")
    if not isinstance(route_id, str) or route_id not in CORRIDOR_ROUTES:
        return reject("unsupported_path", "Route is outside the theorem-bound pair.", "exact upper or lower corridor")
    route = CORRIDOR_ROUTES[route_id]
    fixed = {
        "adapter_id": "cella.continuation.adapters.dbp_exact_corridor_v1",
        "adapter_version": "1.0",
        "family_manifest_digest": "0bbc80b08d721dc0dc0c7e430720a8943522f7d01d4ea52c59f9f71e08d2864a",
        "divisor_manifest_digest": "cf893db1c6c2718a614dfdf519e220cbb3b7312aff62130c608ddd7598c1c93a",
        "theorem_digest": "bfb0dc4c4678803cc46e791cbe60e87736ea41ce14db157e8fb1726e28b671fe",
        "coefficient_ring": "Z",
        "surface_scope": "curve_only",
        "initial_sheet": "rho=+sqrt(2)",
        "terminal_sheet": "rho=-sqrt(2)",
        "tube_radius": Fraction(1, 8),
    }
    route_fixed = {key: route[key] for key in (
        "route_manifest_digest", "vertices_digest", "selected_state_digest",
        "clearance_certificate_digest", "free_group_word", "windings",
    )}
    for key, expected in {**fixed, **route_fixed}.items():
        if _lookup(request.mathematical_context, key) != expected:
            code = {
                "theorem_digest": "route_theorem_digest_mismatch",
                "divisor_manifest_digest": "divisor_manifest_digest_mismatch",
                "surface_scope": "surface_scope_requested_without_surface_clearance",
            }.get(key, "route_identity_failed")
            return reject(code, f"{key} does not match the exact corridor certificate.", key)
    steps = (
        RouteStep("bind-exact-corridor", "bind_theorem_route_and_divisor_manifests", ("continuation_request",), ("bound_corridor",), freeze_mapping({"route_id": route_id, "vertices_digest": route["vertices_digest"]})),
        RouteStep("replay-clearance", "replay_exact_corridor_clearance_and_lift", ("bound_corridor",), ("verified_corridor",), freeze_mapping({"clearance_certificate_digest": route["clearance_certificate_digest"], "tube_radius": Fraction(1, 8)})),
        RouteStep("select-relative-class", "apply_return_stem_lateral_calibration", ("verified_corridor",), ("certified_relative_transport",), freeze_mapping({"target": route["target"]})),
    )
    return assemble_candidate(
        request=request,
        contract=DBP_CORRIDOR_CONTRACT,
        steps=steps,
        data_dependencies=("continuation_request",),
        required_intermediate_objects=("bound_corridor", "verified_corridor"),
        completion_condition="The exact curve corridor, lift and lateral quotient class replay with all bound digests.",
        burden_vector=BurdenVector(invariant_level=2, exact_operation_count=3, scout_operation_count=0, expression_depth=2),
        structural_preference_rank=0,
    )


PROVIDERS = (
    RouteProvider(
        route_family=ROUTE_FAMILY,
        contract=DBP_NATIVE_CONTRACT,
        recognizer=recognize_dbp_native_released,
        native_scouts=(),
        wrapper_capabilities=("native_dbp_evaluation", "legacy_certificate_replay"),
    ),
    RouteProvider(
        route_family=CORRIDOR_ROUTE_FAMILY,
        contract=DBP_CORRIDOR_CONTRACT,
        recognizer=recognize_dbp_exact_corridor,
        native_scouts=(),
        wrapper_capabilities=("exact_dbp_corridor_transport", "curve_clearance_replay"),
    ),
)
