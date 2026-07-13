"""Normalization-aware cover route-family providers.

Three route families from the horizon wreath corpus:

- ``normalization_aware_cover`` — model the incidence cover first and read
  ramification from the relative Jacobian determinant modulo the incidence
  ideal; the eliminant discriminant is PROHIBITED as a ramification decider
  (it overcounts projected sheet crossings, certified on the N = (8,8,12,20)
  slice).
- ``structured_incidence_projection`` — one structured prolongation plus its
  G-orbit supplies d parity rows (full matrix = B (x) I_d); admissibility rests
  on the five-point geometric verification package, not on a discriminant.
- ``generic_open_boundary_split`` — the boundary disposition table splits the
  declared boundaries into unramified relation / unramified crossing / colored
  inertia tasks, one retained task per boundary.

Route instructions and certificate obligations only; no execution.
"""

from __future__ import annotations

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.problem import lower_request
from ..ir.values import FrozenValue, freeze_mapping
from ..plan.admissibility import (
    evidence_by_family,
    family_enabled,
    lookup,
    refuse,
    require_odd_characteristic,
)
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider
from ..scout.algebra import sign_orbit_scout
from ..scout.kummer import parity_matrix_scout


def _accept_shape(
    request: PathfinderRequest,
    route_family: str,
    accepted_shapes: tuple[str, ...],
) -> RecognitionOutcome | None:
    shape = lookup(request.mathematical_context, "problem_shape")
    if shape not in accepted_shapes:
        return refuse(
            route_family,
            "shape_mismatch",
            "The task does not declare one of the accepted problem shapes: "
            + ", ".join(repr(item) for item in accepted_shapes)
            + ".",
            *accepted_shapes,
        )
    return None


def _is_exact_int(value: FrozenValue | None) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _parity_fingerprint(request: PathfinderRequest) -> dict[str, FrozenValue] | None:
    supplied = evidence_by_family(request, "kummer_parity_matrix")
    if supplied is not None:
        return supplied
    evidence = parity_matrix_scout(lower_request(request), request.analysis_budget)
    if evidence is None:
        return None
    return dict(evidence.structural_fingerprint)


# ---------------------------------------------------------------------------
# normalization_aware_cover
# ---------------------------------------------------------------------------

_NORMALIZATION_SHAPES = ("cover_ramification", "branch_image")

NORMALIZATION_COVER_CERTIFICATES = (
    Obligation(
        "incidence-codimension",
        "The incidence ideal has the expected codimension on the ambient model "
        "(codim 5 on the horizon fixture IX = (w_i^2 - u - N_i^2, Sigma w_i - 4M)).",
        "exact-codimension",
    ),
    Obligation(
        "relative-jacobian-identity",
        "The relative Jacobian determinant identity holds modulo the incidence ideal "
        "(on the horizon fixture: ramDet = 8*e3(w) mod IX).",
        "exact-polynomial-remainder",
    ),
    Obligation(
        "branch-image-from-ir-only",
        "The branch image is computed from the relative ramification ideal "
        "IR = IX + (ramDet) alone, never from the eliminant discriminant. Certified "
        "overcount instance: on the slice N = (8,8,12,20) the eliminant discriminant "
        "contains the true factors PLUS the spurious unramified-crossing factors "
        "m^10*(m-2)^2*(m+2)^2*(m^2-12)^2*(3*m^2-68)^2*(3*m^2+64)^2.",
        "exact-ideal-membership",
    ),
)

NORMALIZATION_COVER_CONTRACT = RouteContract(
    route_family="normalization_aware_cover",
    accepted_problem_shape="cover_ramification",
    required_hypotheses=(
        "the eliminant discriminant must not be used to decide ramification "
        "(it overcounts projected sheet crossings)",
        "the cover is modeled by its incidence presentation upstairs; ramification is "
        "read from the relative Jacobian determinant modulo the incidence ideal",
        "decomposition happens upstairs BEFORE projection to the base",
        "generic saturation is admissible only away from the boundary strata under study",
    ),
    required_evidence=(
        "a declared incidence (or target) ideal presentation",
        "a declared ambient ring with exact characteristic",
    ),
    produced_obligations=(
        Obligation(
            "certify-branch-image",
            "Certify the codimension and relative-Jacobian identities; the branch image "
            "emitted from IR is then the true relative ramification image of the cover.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "M = 0 needs boundary-specific saturation: generic saturation deletes the "
        "stratum under study",
        "P = 0 needs boundary-specific saturation",
        "N_a^2 = N_b^2 needs boundary-specific saturation (it is a projected crossing)",
    ),
    execution_module="external.normalization_cover_executor",
    certificate_obligations=NORMALIZATION_COVER_CERTIFICATES,
    source_references=(
        "docs/files/MACAULAY2_REALIZATION_POSET_WORKFLOW_2026-07-10.md",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#16",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#12.2",
    ),
)


def recognize_normalization_aware_cover(request: PathfinderRequest) -> RecognitionOutcome:
    family = NORMALIZATION_COVER_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _accept_shape(request, family, _NORMALIZATION_SHAPES),
    ):
        if gate is not None:
            return gate

    characteristic = lookup(request.mathematical_context, "characteristic")
    if not _is_exact_int(characteristic):
        return refuse(
            family,
            "missing_characteristic",
            "The coefficient characteristic must be declared exactly.",
            "integer characteristic",
        )

    problem = lower_request(request)
    if problem.ring is None:
        return refuse(
            family,
            "missing_ring_declaration",
            "No ambient ring was declared; the incidence model needs explicit variables.",
            "ring declaration",
        )
    incidence = problem.ideal("incidence") or problem.ideal("target")
    if incidence is None:
        return refuse(
            family,
            "missing_incidence_presentation",
            "No incidence presentation was declared; without the upstairs incidence "
            "ideal the only available decider is the eliminant discriminant, which is "
            "prohibited because it overcounts projected sheet crossings.",
            "ideal named 'incidence' (or 'target')",
        )

    steps = (
        RouteStep(
            "build-incidence",
            "build_incidence_model",
            ("incidence_generators",),
            ("incidence_model",),
            freeze_mapping(
                {"ideal": incidence.name, "generator_count": len(incidence.generators)}
            ),
        ),
        RouteStep(
            "relative-ramification",
            "derive_relative_ramification_from_jacobian",
            ("incidence_model",),
            ("relative_ramification_ideal",),
            freeze_mapping(
                {
                    "determinant": "relative_jacobian_determinant",
                    "horizon_fixture_identity": "ramDet = 8*e3(w) mod IX",
                }
            ),
        ),
        RouteStep(
            "decompose-upstairs",
            "decompose_upstairs_before_projection",
            ("relative_ramification_ideal",),
            ("upstairs_components",),
        ),
        RouteStep(
            "emit-branch-image",
            "emit_branch_image_route",
            ("upstairs_components",),
            ("branch_image_route",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=NORMALIZATION_COVER_CONTRACT,
        steps=steps,
        data_dependencies=("incidence_generators", "ring_declaration"),
        required_intermediate_objects=(
            "incidence_model",
            "relative_ramification_ideal",
            "upstairs_components",
        ),
        completion_condition=(
            "The external executor emits the branch image from the relative ramification "
            "ideal, decomposed upstairs before projection, with the eliminant discriminant "
            "never consulted for a ramification decision."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=4,
            scout_operation_count=0,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# structured_incidence_projection  (Thm 5.1 + geometric package)
# ---------------------------------------------------------------------------

_STRUCTURED_SHAPES = ("structured_projection", "square_class_rank")

_GEOMETRIC_PACKAGE_CHECKLIST = (
    "the base divisor is not a discriminant component",
    "the base divisor is unramified in E/F at the generic point",
    "exactly one conjugate sheet has odd valuation",
    "off-sheet valuations are even",
    "the radicands are regular on the normalized localized model",
)

STRUCTURED_PROJECTION_CERTIFICATES = (
    Obligation(
        "not-discriminant-component",
        "The selected base divisor is not a component of the discriminant.",
        "exact-divisor-membership",
    ),
    Obligation(
        "generic-point-unramified",
        "The base divisor is unramified in E/F at its generic point.",
        "exact-ramification",
    ),
    Obligation(
        "single-odd-sheet",
        "Exactly one conjugate sheet carries an odd valuation at the structured divisor.",
        "exact-valuation",
    ),
    Obligation(
        "off-sheet-even",
        "All off-sheet valuations at the structured divisor are even.",
        "exact-valuation",
    ),
    Obligation(
        "radicand-regularity",
        "All radicands are regular on the normalized localized model at the divisor.",
        "exact-regularity",
    ),
)

STRUCTURED_PROJECTION_CONTRACT = RouteContract(
    route_family="structured_incidence_projection",
    accepted_problem_shape="structured_projection",
    required_hypotheses=(
        "characteristic != 2",
        "the base group acts transitively on the sheets (declared certificate)",
        "the parity rows have the structured shape: v^(q)(r_alpha,j) = b_{q,alpha} if "
        "j = i_q else 0, so the full matrix is B (x) I_d and a single s x s check suffices",
        "the five-point geometric package certifies each structured row",
        "the G-orbit of one structured prolongation supplies all d rows",
    ),
    required_evidence=(
        "kummer_parity_matrix evidence with kronecker_structured_shape true and "
        "full column rank",
        "declared base-group transitivity",
    ),
    produced_obligations=(
        Obligation(
            "certify-structured-projection",
            "Certify the five-point geometric package at the selected divisors; B "
            "invertibility over F2 then certifies maximality of all sd square classes.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "the selected base divisor IS a discriminant component: the package fails and "
        "another divisor must be selected",
        "sub-balance walls are excluded (non-transverse contact)",
    ),
    execution_module="external.structured_projection_executor",
    certificate_obligations=STRUCTURED_PROJECTION_CERTIFICATES,
    source_references=(
        "docs/files/KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md#5",
        "docs/files/MACAULAY2_REALIZATION_POSET_WORKFLOW_2026-07-10.md#4",
    ),
)


def recognize_structured_incidence_projection(request: PathfinderRequest) -> RecognitionOutcome:
    family = STRUCTURED_PROJECTION_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _accept_shape(request, family, _STRUCTURED_SHAPES),
        require_odd_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    if lookup(request.mathematical_context, "base_group_transitive") is not True:
        return refuse(
            family,
            "missing_transitivity",
            "The orbit-transport step needs the base group to act transitively on the "
            "sheets (the G-orbit of one prolongation must supply all d rows); "
            "transitivity is not declared.",
            "base_group_transitive",
        )

    fingerprint = _parity_fingerprint(request)
    if fingerprint is None:
        return refuse(
            family,
            "missing_parity_rows",
            "No structured parity rows were declared for the projection.",
            "cover declaration with parity_rows",
        )
    if fingerprint.get("kronecker_structured_shape") is not True:
        return refuse(
            family,
            "not_structured_shape",
            "The declared parity rows do not have the Kronecker structured shape "
            "(column count = channels x degree), so the single s x s sheet-level check "
            "of Thm 5.1 does not apply.",
            "column_count = channel_count * cover_degree",
        )
    rank = fingerprint.get("f2_rank")
    columns = fingerprint.get("column_count")
    degree = fingerprint.get("cover_degree")
    if not _is_exact_int(rank) or not _is_exact_int(columns) or not _is_exact_int(degree):
        return refuse(
            family,
            "malformed_parity_evidence",
            "The parity-matrix evidence does not carry exact integer rank, column count, "
            "and cover degree.",
            "f2_rank",
            "column_count",
            "cover_degree",
        )
    if fingerprint.get("full_column_rank") is not True:
        return refuse(
            family,
            "parity_rank_inconclusive",
            f"The structured rows have F2 rank {rank} over {columns} columns; the "
            "maximality criterion is SILENT here — a deficient rank does NOT disprove "
            "independence of the projected square classes.",
            "full F2 column rank of the structured matrix",
        )

    steps = (
        RouteStep(
            "select-divisors",
            "select_structured_base_divisors",
            ("cover_declaration",),
            ("structured_base_divisors",),
        ),
        RouteStep(
            "verify-package",
            "verify_geometric_package",
            ("structured_base_divisors",),
            ("geometric_package_certificate",),
            freeze_mapping({"checklist": _GEOMETRIC_PACKAGE_CHECKLIST}),
        ),
        RouteStep(
            "orbit-transport",
            "orbit_transport_rows",
            ("geometric_package_certificate",),
            ("transported_rows",),
            freeze_mapping(
                {
                    "degree": degree,
                    "principle": "the G-orbit of one structured prolongation supplies d rows",
                }
            ),
        ),
        RouteStep(
            "emit-obligations",
            "emit_structured_projection_obligations",
            ("transported_rows",),
            ("structured_projection_route",),
            freeze_mapping({"sheet_structure": "B (x) I_d"}),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=STRUCTURED_PROJECTION_CONTRACT,
        steps=steps,
        data_dependencies=("cover_declaration", "base_group_transitive"),
        required_intermediate_objects=(
            "structured_base_divisors",
            "geometric_package_certificate",
            "transported_rows",
        ),
        completion_condition=(
            "The external certifier verifies the five-point geometric package at each "
            "selected divisor; sheet-level invertibility then certifies maximality."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=4,
            scout_operation_count=1,
            expression_depth=1,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# generic_open_boundary_split
# ---------------------------------------------------------------------------

_BOUNDARY_DISPOSITION_TABLE = (
    ("J = 0", "unramified Kummer relation divisor: v_J(u_i) = v_J(gamma_i) = "
     "v_J(delta_i) = 0 with delta_i(0) = gamma_i - 4P != 0, yet the fiber square-class "
     "rank drops ([delta_0] = [u][gamma])"),
    ("J = infinity", "unramified even pole: v_t(delta) = -2"),
    ("N_a = 0", "unramified axial collapse: u_i = (gamma_i/(2*beta_i))^2; static rank "
     "2 -> 1, augmented 3 -> <= 2, ordered scope not forced"),
    ("N_a^2 = N_b^2", "unramified crossing of normalized sheets (not ramification)"),
    ("sub-balance Sigma eps_i/N_i = 0", "colored C_4 inertia (except the even "
     "ordered-horizon case, which stays C_2); owned by the inertia family"),
    ("M = 0", "unramified chart boundary"),
    ("weighted infinity", "unramified: under weights M = N = 1, J = u = 2, "
     "gamma = delta = 4 all poles are even"),
)

BOUNDARY_SPLIT_CERTIFICATES = (
    Obligation(
        "boundary-valuation-parity",
        "The valuation parity of every declared radicand is verified at each declared "
        "boundary on the normalized model.",
        "exact-valuation",
    ),
    Obligation(
        "even-pole-at-infinity",
        "The even-pole checks hold at J = infinity and at the weighted infinity.",
        "exact-valuation",
    ),
    Obligation(
        "sub-balance-deferred",
        "The sub-balance stratum's colored inertia is classified by the inertia "
        "stratification family, not by this split.",
        "route-delegation",
    ),
)

BOUNDARY_SPLIT_CONTRACT = RouteContract(
    route_family="generic_open_boundary_split",
    accepted_problem_shape="boundary_stratification",
    required_hypotheses=(
        "characteristic != 2",
        "valuation parity per boundary splits the declared boundaries into "
        "{unramified relation | unramified crossing | colored inertia}",
        "J = 0 is a Kummer RELATION divisor, not ramification",
        "each boundary keeps its own saturation discipline (no generic saturation while "
        "studying that boundary)",
    ),
    required_evidence=(
        "declared cover parity data or declared boundary strata",
    ),
    produced_obligations=(
        Obligation(
            "certify-boundary-dispositions",
            "Certify the valuation-parity reading at each declared boundary; the "
            "disposition table then splits the boundary set into retained tasks.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "the reciprocal sub-balance Sigma eps_i/N_i = 0 is the one boundary with "
        "genuine (colored C_4) inertia",
    ),
    execution_module="external.boundary_split_executor",
    certificate_obligations=BOUNDARY_SPLIT_CERTIFICATES,
    source_references=(
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#11",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#12.6",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#15",
    ),
)


def recognize_generic_open_boundary_split(request: PathfinderRequest) -> RecognitionOutcome:
    family = BOUNDARY_SPLIT_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _accept_shape(request, family, ("boundary_stratification",)),
        require_odd_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    problem = lower_request(request)
    has_parity = problem.cover is not None and bool(problem.cover.parity_rows)
    has_strata = bool(problem.strata)
    if not has_parity and not has_strata:
        return refuse(
            family,
            "missing_boundary_declarations",
            "Neither cover parity data nor declared boundary strata are present; the "
            "boundary split has nothing to classify.",
            "cover.parity_rows or declared strata",
        )

    steps = (
        RouteStep(
            "classify-boundaries",
            "classify_declared_boundaries",
            ("boundary_declarations",),
            ("boundary_classification",),
            freeze_mapping({"disposition_table": _BOUNDARY_DISPOSITION_TABLE}),
        ),
        RouteStep(
            "split-tasks",
            "split_boundary_tasks",
            ("boundary_classification",),
            ("boundary_tasks",),
            freeze_mapping({"policy": "one retained task per declared boundary"}),
        ),
        RouteStep(
            "emit-route",
            "emit_boundary_disposition_route",
            ("boundary_tasks",),
            ("boundary_disposition_route",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=BOUNDARY_SPLIT_CONTRACT,
        steps=steps,
        data_dependencies=("boundary_declarations",),
        required_intermediate_objects=("boundary_classification", "boundary_tasks"),
        completion_condition=(
            "The external executor verifies the valuation-parity disposition at each "
            "declared boundary and emits one retained task per boundary."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=3,
            scout_operation_count=1,
            expression_depth=1,
        ),
        structural_preference_rank=0,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="normalization_aware_cover",
        contract=NORMALIZATION_COVER_CONTRACT,
        recognizer=recognize_normalization_aware_cover,
        native_scouts=(),
        wrapper_capabilities=("incidence_model_construction", "jacobian_determinant"),
    ),
    RouteProvider(
        route_family="structured_incidence_projection",
        contract=STRUCTURED_PROJECTION_CONTRACT,
        recognizer=recognize_structured_incidence_projection,
        native_scouts=(parity_matrix_scout,),
        wrapper_capabilities=("structured_divisor_selection", "orbit_transport"),
    ),
    RouteProvider(
        route_family="generic_open_boundary_split",
        contract=BOUNDARY_SPLIT_CONTRACT,
        recognizer=recognize_generic_open_boundary_split,
        native_scouts=(parity_matrix_scout, sign_orbit_scout),
        wrapper_capabilities=("boundary_classification",),
    ),
)
