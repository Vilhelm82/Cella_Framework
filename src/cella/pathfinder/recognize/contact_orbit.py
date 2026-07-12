"""Recognizer for projecting the complete signed-contact orbit."""

from __future__ import annotations

from ..api.contract import RecognitionOutcome, RecognitionRefusal, RouteCandidate, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import ComputationalRoute, RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.values import FrozenValue, freeze_mapping


ORBIT_CERTIFICATES = (
    Obligation(
        "contact-triangular-presentation",
        "Each signed-contact ideal equals its explicit triangular presentation with one linear wall.",
        "exact-ideal-equality",
    ),
    Obligation(
        "contact-orbit-completeness",
        "The emitted sign orbit contains every element of {+1,-1}^4 exactly once.",
        "finite-exact-enumeration",
    ),
    Obligation(
        "contact-image-contraction",
        "Each triangular contact presentation contracts to its declared linear base wall.",
        "explicit-ring-map",
    ),
)

CONTACT_ORBIT_CONTRACT = RouteContract(
    route_family="signed_contact_orbit_projection",
    accepted_problem_shape="complete_signed_contact_projection",
    required_hypotheses=(
        "characteristic != 2",
        "four signed sheet variables",
        "the complete 16-element sign orbit is requested",
        "each contact component is given by explicit signed substitutions",
    ),
    required_evidence=("signed substitution family", "linear incidence wall"),
    produced_obligations=(
        Obligation(
            "execute-contact-orbit-projection",
            "Emit all sixteen signed contact walls in host bindings.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "characteristic two collapses the sign orbit",
        "partial sign sets require an explicitly declared subset route",
        "nonlinear incidence walls require generic projection",
    ),
    execution_module="external.signed_contact_orbit_executor",
    certificate_obligations=ORBIT_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#structure-first-route-table",
        "CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1.0.md#structure-first-route-table",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#16",
    ),
)


def _lookup(items: tuple[tuple[str, FrozenValue], ...], key: str) -> FrozenValue | None:
    return next((value for item_key, value in items if item_key == key), None)


def _refuse(code: str, reason: str, *requirements: str) -> RecognitionOutcome:
    return RecognitionOutcome(
        refusal=RecognitionRefusal(
            CONTACT_ORBIT_CONTRACT.route_family,
            code,
            reason,
            tuple(requirements),
        )
    )


def recognize_contact_orbit(request: PathfinderRequest) -> RecognitionOutcome:
    family = CONTACT_ORBIT_CONTRACT.route_family
    if family not in request.available_route_families:
        return _refuse("route_not_enabled", "The wrapper did not enable this route family.", family)
    if _lookup(request.mathematical_context, "problem_shape") != CONTACT_ORBIT_CONTRACT.accepted_problem_shape:
        return _refuse("shape_mismatch", "The task is not a complete signed-contact projection.")
    characteristic = _lookup(request.mathematical_context, "characteristic")
    if not isinstance(characteristic, int) or isinstance(characteristic, bool):
        return _refuse("missing_characteristic", "The coefficient characteristic is not exact.")
    if characteristic == 2:
        return _refuse("characteristic_two", "The signed orbit collapses in characteristic two.")
    if _lookup(request.mathematical_context, "sign_dimension") != 4:
        return _refuse("unsupported_sign_dimension", "The first orbit contract is four-dimensional.")
    if _lookup(request.mathematical_context, "sign_vector_count") != 16:
        return _refuse("incomplete_sign_orbit", "The request does not declare all sixteen sign vectors.")

    route = ComputationalRoute(
        request_id=request.request_id,
        target_obligation=request.target_obligation,
        route_family=family,
        ordered_steps=(
            RouteStep(
                "derive-representative",
                "derive_triangular_contact_presentation",
                ("incidence_ideal", "contact_substitution_family"),
                ("representative_contact_presentation", "representative_wall"),
            ),
            RouteStep(
                "enumerate-orbit",
                "enumerate_complete_sign_orbit",
                ("representative_contact_presentation",),
                ("signed_contact_presentations",),
                freeze_mapping({"dimension": 4, "expected_count": 16}),
            ),
            RouteStep(
                "transport-wall",
                "transport_linear_wall_over_sign_orbit",
                ("representative_wall", "signed_contact_presentations"),
                ("signed_contact_walls",),
                freeze_mapping({"wall_template": "4*M-s1*N1-s2*N2-s3*N3-s4*N4"}),
            ),
            RouteStep(
                "emit-host-route",
                "emit_contact_walls_in_external_bindings",
                ("signed_contact_walls",),
                ("host_contact_images",),
            ),
        ),
        data_dependencies=("incidence_ideal", "contact_substitution_family", "base_variables"),
        external_binding=request.external_binding,
        required_intermediate_objects=(
            "representative_contact_presentation",
            "representative_wall",
            "signed_contact_presentations",
            "signed_contact_walls",
        ),
        required_hypotheses=CONTACT_ORBIT_CONTRACT.required_hypotheses,
        certificate_obligations=ORBIT_CERTIFICATES,
        exceptional_branches=CONTACT_ORBIT_CONTRACT.exceptional_branches,
        completion_condition="The external executor emits all sixteen linear contact-image ideals.",
        supporting_scout_evidence=request.supplied_scout_evidence,
    )
    return RecognitionOutcome(
        candidate=RouteCandidate(
            CONTACT_ORBIT_CONTRACT,
            route,
            BurdenVector(
                invariant_level=1,
                global_expansion_rank=0,
                elimination_rank=0,
                exact_operation_count=16,
                scout_operation_count=1,
                expression_depth=2,
            ),
            0,
        )
    )
