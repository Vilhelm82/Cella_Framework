"""Signed-contact structural projection recognizer.

This module emits instructions only.  M2 execution and exact ideal checks live
in the external benchmark/execution adapter.
"""

from __future__ import annotations

from ..api.contract import (
    RecognitionOutcome,
    RecognitionRefusal,
    RouteCandidate,
    RouteContract,
)
from ..api.request import PathfinderRequest
from ..api.route import ComputationalRoute, RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.values import FrozenValue, freeze_mapping


CONTACT_CERTIFICATES = (
    Obligation(
        "contact-incidence-membership",
        "The declared signed-contact substitutions satisfy every incidence generator.",
        "exact-ideal-membership",
    ),
    Obligation(
        "restricted-generator-identity",
        "The target generator plus 16*J^2 vanishes modulo the even contact ideal.",
        "exact-polynomial-remainder",
    ),
    Obligation(
        "structural-upstairs-equality",
        "The original sliced upstairs ideal equals the structural sliced presentation.",
        "exact-ideal-equality",
    ),
    Obligation(
        "base-image-equivalence",
        "The structurally produced base ideal equals the baseline eliminated ideal.",
        "exact-ideal-equality",
    ),
    Obligation(
        "multiplicity-retention",
        "The executor retains J^2 and does not replace it by the reduced support J.",
        "scheme-structure",
    ),
)

CONTACT_RESTRICTION_CONTRACT = RouteContract(
    route_family="contact_restriction",
    accepted_problem_shape="signed_contact_projection",
    required_hypotheses=(
        "sign_product = +1",
        "characteristic != 2",
        "the wrapper declares an exact slice",
        "the target generator has the declared delta binding",
    ),
    required_evidence=("explicit contact substitutions", "linear contact wall"),
    produced_obligations=(
        Obligation(
            "execute-contact-restriction",
            "Execute the signed-contact restriction and emit the requested host base image.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "odd sign product uses a different restricted generator",
        "characteristic two invalidates division/scaling assumptions",
        "nonlinear or incomplete contact walls require another route",
    ),
    execution_module="external.contact_restriction_executor",
    certificate_obligations=CONTACT_CERTIFICATES,
    source_references=(
        "CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1.0.md#12.1",
        "CELLA_ARCHITECTURE_v1.3.md",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#16.3",
    ),
)


def _lookup(items: tuple[tuple[str, FrozenValue], ...], key: str) -> FrozenValue | None:
    for item_key, value in items:
        if item_key == key:
            return value
    return None


def _refuse(code: str, reason: str, *requirements: str) -> RecognitionOutcome:
    return RecognitionOutcome(
        refusal=RecognitionRefusal(
            route_family=CONTACT_RESTRICTION_CONTRACT.route_family,
            code=code,
            reason=reason,
            unmet_requirements=tuple(requirements),
        )
    )


def recognize_contact_restriction(request: PathfinderRequest) -> RecognitionOutcome:
    """Recognize the first even-contact projection fixture conservatively."""

    family = CONTACT_RESTRICTION_CONTRACT.route_family
    if family not in request.available_route_families:
        return _refuse("route_not_enabled", "The wrapper did not enable this route family.", family)

    shape = _lookup(request.mathematical_context, "problem_shape")
    if shape != CONTACT_RESTRICTION_CONTRACT.accepted_problem_shape:
        return _refuse(
            "shape_mismatch",
            "The task is not a declared signed-contact projection.",
            CONTACT_RESTRICTION_CONTRACT.accepted_problem_shape,
        )

    sign_product = _lookup(request.mathematical_context, "sign_product")
    if sign_product != 1:
        return _refuse(
            "unsupported_sign_product",
            "The initial route is valid only on an even signed contact.",
            "sign_product = +1",
        )

    characteristic = _lookup(request.mathematical_context, "characteristic")
    if not isinstance(characteristic, int) or isinstance(characteristic, bool):
        return _refuse(
            "missing_characteristic",
            "The coefficient characteristic must be declared exactly.",
            "integer characteristic",
        )
    if characteristic == 2:
        return _refuse(
            "characteristic_two",
            "The restricted-generator scaling is not admissible in characteristic two.",
            "characteristic != 2",
        )

    target_generator = _lookup(request.mathematical_context, "target_generator")
    if target_generator != "delta":
        return _refuse(
            "target_generator_mismatch",
            "The first contract recognizes only the declared delta generator.",
            "target_generator = delta",
        )

    exact_slice = _lookup(request.mathematical_context, "exact_slice")
    required_slice_keys = ("N1", "N2", "N3", "N4")
    if not isinstance(exact_slice, tuple):
        return _refuse("missing_exact_slice", "No canonical exact slice was supplied.", *required_slice_keys)
    slice_items = dict(exact_slice)
    missing = tuple(key for key in required_slice_keys if key not in slice_items)
    if missing:
        return _refuse("incomplete_exact_slice", "The exact slice is incomplete.", *missing)
    if any(not isinstance(slice_items[key], int) or isinstance(slice_items[key], bool) for key in required_slice_keys):
        return _refuse(
            "nonintegral_fixture_slice",
            "The initial fixture requires exact integral slice assignments.",
            *required_slice_keys,
        )

    steps = (
        RouteStep(
            "contact-substitute",
            "apply_signed_contact_substitutions",
            ("incidence_ideal", "contact_component"),
            ("restricted_incidence", "restricted_target_generator"),
            freeze_mapping({"sign_product": 1}),
        ),
        RouteStep(
            "reduce-target",
            "reduce_bound_generator_on_contact",
            ("restricted_target_generator",),
            ("multiplicity_generator",),
            freeze_mapping({"identity": "delta|contact = -16*J^2", "retain_power": 2}),
        ),
        RouteStep(
            "apply-slice",
            "apply_exact_slice_assignments",
            ("restricted_incidence", "multiplicity_generator"),
            ("sliced_contact_system",),
            freeze_mapping({"assignments": slice_items}),
        ),
        RouteStep(
            "solve-wall",
            "solve_linear_contact_wall",
            ("sliced_contact_system",),
            ("base_image_presentation",),
            freeze_mapping({"wall": "4*M = N1+N2+N3+N4"}),
        ),
        RouteStep(
            "emit-host-route",
            "emit_base_image_in_external_bindings",
            ("base_image_presentation",),
            ("host_base_image",),
        ),
    )

    route = ComputationalRoute(
        request_id=request.request_id,
        target_obligation=request.target_obligation,
        route_family=family,
        ordered_steps=steps,
        data_dependencies=("incidence_ideal", "contact_component", "target_generator", "exact_slice"),
        external_binding=request.external_binding,
        required_intermediate_objects=(
            "restricted_incidence",
            "restricted_target_generator",
            "multiplicity_generator",
            "sliced_contact_system",
            "base_image_presentation",
        ),
        required_hypotheses=CONTACT_RESTRICTION_CONTRACT.required_hypotheses,
        certificate_obligations=CONTACT_CERTIFICATES,
        exceptional_branches=CONTACT_RESTRICTION_CONTRACT.exceptional_branches,
        completion_condition="The external executor emits the requested base image in host bindings.",
        supporting_scout_evidence=request.supplied_scout_evidence,
    )
    return RecognitionOutcome(
        candidate=RouteCandidate(
            contract=CONTACT_RESTRICTION_CONTRACT,
            route=route,
            burden_vector=BurdenVector(
                invariant_level=1,
                global_expansion_rank=0,
                elimination_rank=0,
                exact_operation_count=4,
                scout_operation_count=0,
                expression_depth=2,
            ),
            structural_preference_rank=0,
        )
    )
