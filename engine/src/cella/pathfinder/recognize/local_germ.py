"""Local-geometry germ route-family providers.

Families: ``local_metric_germ``, ``parity_fixed_face``, ``extremal_face``,
``newton_wedge_corner``.

Recognition works on 2-3 term exact Laurent germ data instead of a global
curvature expansion.  All context numbers are int/Fraction (no floats; bool is
not a number).  Leading-coefficient values computed below (for example
-m*(m+5)/B) are route evidence and replay parameters, never the host
deliverable: the executor still produces and certifies the pole law itself.
"""

from __future__ import annotations

from fractions import Fraction

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.problem import lower_request
from ..ir.values import FrozenValue, freeze_mapping
from ..plan.admissibility import evidence_by_family, family_enabled, lookup, refuse, require_shape
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider
from ..scout.newton import newton_corner_scout
from ..scout.sturm import sturm_scout


def _rational(value: FrozenValue | None) -> Fraction | None:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        return None
    return Fraction(value)


def _rational_tuple(
    value: FrozenValue | None,
    expected_length: int | None = None,
) -> tuple[Fraction, ...] | None:
    if not isinstance(value, tuple) or not value:
        return None
    if expected_length is not None and len(value) != expected_length:
        return None
    entries: list[Fraction] = []
    for entry in value:
        rational = _rational(entry)
        if rational is None:
            return None
        entries.append(rational)
    return tuple(entries)


# ---------------------------------------------------------------------------
# local_metric_germ
# ---------------------------------------------------------------------------

LOCAL_GERM_CERTIFICATES = (
    Obligation(
        "a2-taylor-identity",
        "A2 equals the delta^2 Taylor coefficient of the collapsing component exactly.",
        "exact-identity-replay",
    ),
    Obligation(
        "first-principles-ricci-match",
        "The order-3 pole law matches a first-principles Ricci computation on the germ.",
        "external-replay",
    ),
    Obligation(
        "germ-shape-hypotheses",
        "The metric is diagonal, exactly one native component collapses quadratically, and the "
        "transverse channels are finite and nonzero.",
        "hypothesis-audit",
    ),
)

LOCAL_GERM_CONTRACT = RouteContract(
    route_family="local_metric_germ",
    accepted_problem_shape="local_pole_order",
    required_hypotheses=(
        "diagonal metric germ",
        "single native coordinate collapses quadratically (A2 != 0)",
        "transverse channels finite and nonzero (every P0 != 0)",
        "parity broken at first order (some P1 != 0)",
    ),
    required_evidence=("exact collapse coefficients", "exact transverse channel pairs"),
    produced_obligations=(
        Obligation(
            "execute-local-pole-law",
            "Certify the order-3 pole and its leading coefficient from the declared germ.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "divergent transverse channels leave this family; the face belongs to parity_fixed_face",
        "the leading coefficient is independent of A3 and higher collapse coefficients",
    ),
    execution_module="external.local_metric_germ_executor",
    certificate_obligations=LOCAL_GERM_CERTIFICATES,
    source_references=(
        "paper/lead7_kn_n3_dbp_metric.tex#sec:gate",
        "paper/pfc_normal_forms.tex#thm:pure",
        "CELLA_ARCHITECTURE_v1.3.md#17.1",
    ),
)


def recognize_local_metric_germ(request: PathfinderRequest) -> RecognitionOutcome:
    family = LOCAL_GERM_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, LOCAL_GERM_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    collapse = _rational_tuple(lookup(request.mathematical_context, "collapse_coefficients"))
    if collapse is None:
        return refuse(
            family,
            "non_rational_input",
            "collapse_coefficients must be a non-empty tuple (A2, A3, ...) of exact int/Fraction values.",
            "exact rational collapse coefficients",
        )
    if collapse[0] == 0:
        return refuse(
            family,
            "degenerate_collapse",
            "A2 = 0: the native component does not collapse quadratically.",
            "A2 != 0",
        )

    raw_channels = lookup(request.mathematical_context, "transverse_channels")
    if not isinstance(raw_channels, tuple) or not raw_channels:
        return refuse(
            family,
            "non_rational_input",
            "transverse_channels must be a non-empty tuple of exact (P0, P1) pairs.",
            "exact rational transverse channels",
        )
    channels: list[tuple[Fraction, Fraction]] = []
    for entry in raw_channels:
        pair = _rational_tuple(entry, 2)
        if pair is None:
            return refuse(
                family,
                "non_rational_input",
                "Every transverse channel must be an exact (P0, P1) pair of int/Fraction values.",
                "exact rational transverse channels",
            )
        channels.append((pair[0], pair[1]))
    if any(p0 == 0 for p0, _ in channels):
        return refuse(
            family,
            "transverse_channel_vanishes",
            "A transverse channel has P0 = 0: the channel is not finite and nonzero at the face.",
            "every P0 != 0",
        )
    if all(p1 == 0 for _, p1 in channels):
        return refuse(
            family,
            "parity_fixed_escalation",
            "Every P1 = 0: the x^-3 term vanishes identically; the even germ belongs to the "
            "parity_fixed_face family.",
            "some P1 != 0",
        )

    a2 = collapse[0]
    coefficient = sum((p1 / p0 for p0, p1 in channels), Fraction(0)) / a2

    steps = (
        RouteStep(
            "read-germ",
            "read_local_germ",
            ("metric_germ",),
            ("local_laurent_germ",),
            freeze_mapping(
                {
                    "collapse_coefficients": collapse,
                    "transverse_channels": tuple(channels),
                }
            ),
        ),
        RouteStep(
            "compute-pole-law",
            "compute_generic_pole_law",
            ("local_laurent_germ",),
            ("generic_pole_law",),
            freeze_mapping(
                {
                    "pole_order": 3,
                    "coefficient_formula": "(1/A2) * sum(P1/P0)",
                    "leading_coefficient": coefficient,
                    "independent_of": "A3 and higher collapse coefficients",
                }
            ),
        ),
        RouteStep(
            "emit-pole-order",
            "emit_pole_order_route",
            ("generic_pole_law",),
            ("host_pole_order_certificate",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=LOCAL_GERM_CONTRACT,
        steps=steps,
        data_dependencies=("collapse_coefficients", "transverse_channels"),
        required_intermediate_objects=("local_laurent_germ", "generic_pole_law"),
        completion_condition=(
            "The external executor certifies the order-3 pole law in host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=len(channels) + 1,
            scout_operation_count=1,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# parity_fixed_face
# ---------------------------------------------------------------------------

PARITY_FACE_CERTIFICATES = (
    Obligation(
        "warped-product-reduction",
        "The even germ reduces to the warped-product normal form exactly.",
        "exact-identity-replay",
    ),
    Obligation(
        "first-principles-ricci-low-m",
        "First-principles Ricci computations for m = 1, 2, 3 replay the -m(m+5)/B law.",
        "external-replay",
    ),
    Obligation(
        "transverse-collapse-hypothesis",
        "The transverse channels genuinely collapse: the x^-2 poles are present in the germ.",
        "hypothesis-audit",
    ),
)

PARITY_FACE_CONTRACT = RouteContract(
    route_family="parity_fixed_face",
    accepted_problem_shape="local_pole_order",
    required_hypotheses=(
        "metric germ even in the collapsing variable",
        "fibre dimension m >= 1",
        "radial coefficient B != 0",
        "transverse channels genuinely collapse (x^-2 poles present)",
    ),
    required_evidence=("declared even germ parity", "exact fibre dimension and radial coefficient"),
    produced_obligations=(
        Obligation(
            "execute-parity-fixed-face",
            "Certify the order-4 pole with universal coefficient -m(m+5)/B on the reflection face.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "corners where two order-4 faces meet belong to newton_wedge_corner",
        "the coefficient can vanish to second order at corner loci",
    ),
    execution_module="external.parity_fixed_face_executor",
    certificate_obligations=PARITY_FACE_CERTIFICATES,
    source_references=(
        "paper/pfc_normal_forms.tex#thm:pure",
        "paper/lead7_kn_n3_dbp_metric.tex#sec:gate",
        "CELLA_ARCHITECTURE_v1.3.md#17.1",
    ),
)


def recognize_parity_fixed_face(request: PathfinderRequest) -> RecognitionOutcome:
    family = PARITY_FACE_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, PARITY_FACE_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    parity = lookup(request.mathematical_context, "germ_parity")
    if parity != "even":
        return refuse(
            family,
            "germ_parity_not_even",
            "This face route requires an exactly even metric germ; odd first-order drift belongs "
            "to local_metric_germ.",
            "germ_parity = even",
        )

    fibre = lookup(request.mathematical_context, "fibre_dimension")
    if isinstance(fibre, bool) or not isinstance(fibre, int) or fibre < 0:
        return refuse(
            family,
            "missing_fibre_dimension",
            "The fibre dimension m must be declared as a non-negative integer.",
            "integer fibre_dimension m >= 1",
        )
    if fibre == 0:
        return refuse(
            family,
            "flat_no_pole",
            "m = 0 is the flat case: there is no pole to certify.",
            "fibre_dimension m >= 1",
        )

    radial = _rational(lookup(request.mathematical_context, "radial_coefficient"))
    if radial is None:
        return refuse(
            family,
            "non_rational_input",
            "The radial coefficient B must be an exact int/Fraction value.",
            "exact rational radial_coefficient",
        )
    if radial == 0:
        return refuse(
            family,
            "degenerate_radial_coefficient",
            "B = 0 degenerates the radial normal form.",
            "radial_coefficient B != 0",
        )

    coefficient = Fraction(-fibre * (fibre + 5), 1) / radial

    steps = (
        RouteStep(
            "verify-parity",
            "verify_even_parity_germ",
            ("metric_germ",),
            ("even_parity_germ",),
            freeze_mapping({"parity": "even", "absent_term": "x^-3 (excluded by parity)"}),
        ),
        RouteStep(
            "apply-normal-form",
            "apply_parity_fixed_normal_form",
            ("even_parity_germ",),
            ("reflection_face_law",),
            freeze_mapping(
                {
                    "law": "R = -m(m+5)/B * x^-4",
                    "pole_order": 4,
                    "fibre_dimension": fibre,
                    "leading_coefficient": coefficient,
                    "coefficient_decomposition": "m(m+5) = 6m + m(m-1)",
                    "decomposition_terms": (6 * fibre, fibre * (fibre - 1)),
                }
            ),
        ),
        RouteStep(
            "emit-reflection-face",
            "emit_reflection_face_route",
            ("reflection_face_law",),
            ("host_reflection_face_certificate",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=PARITY_FACE_CONTRACT,
        steps=steps,
        data_dependencies=("germ_parity", "fibre_dimension", "radial_coefficient"),
        required_intermediate_objects=("even_parity_germ", "reflection_face_law"),
        completion_condition=(
            "The external executor certifies the order-4 reflection-face pole law in host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=3,
            scout_operation_count=1,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# extremal_face
# ---------------------------------------------------------------------------

EXTREMAL_FACE_CERTIFICATES = (
    Obligation(
        "a2-delta-squared-identity",
        "A2 equals the delta^2 coefficient [(4U + U_J^2 + U_Q^2)^2/(4U) * (1/U_J^2 + 1/U_Q^2)] at "
        "the extremal edge exactly.",
        "exact-identity-replay",
    ),
    Obligation(
        "sturm-negativity-gate",
        "The lead7_test8 Sturm-based gate certifies the sign of the transverse log-derivative on "
        "the open edge.",
        "exact-sturm-replay",
    ),
    Obligation(
        "denominator-positivity-factorization",
        "The denominator factors into coefficient-positive terms after t = 1 + r substitution.",
        "exact-identity-replay",
    ),
)

EXTREMAL_FACE_CONTRACT = RouteContract(
    route_family="extremal_face",
    accepted_problem_shape="extremal_edge_pole",
    required_hypotheses=(
        "outer physical wedge: S, J, Q > 0 and U_S > 0",
        "only the native S-component collapses at the extremal edge",
        "A2 > 0 (exact positive collapse coefficient)",
        "transverse log-derivative d/dS log(G_J*G_Q) nonzero at the edge",
    ),
    required_evidence=("declared wedge membership", "exact A2 and transverse log-derivative"),
    produced_obligations=(
        Obligation(
            "execute-extremal-edge-pole",
            "Certify the order-3 pole and its rational coefficient on the open extremal edge.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "corners S = pi*Q^2 and S = 2*pi*J leave the open edge",
        "the inner branch U_S < 0 is outside the physical wedge",
    ),
    execution_module="external.extremal_face_executor",
    certificate_obligations=EXTREMAL_FACE_CERTIFICATES,
    source_references=(
        "paper/lead7_kn_n3_dbp_metric.tex#sec:gate",
        "CELLA_ARCHITECTURE_v1.3.md#16",
    ),
)


def recognize_extremal_face(request: PathfinderRequest) -> RecognitionOutcome:
    family = EXTREMAL_FACE_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, EXTREMAL_FACE_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    if lookup(request.mathematical_context, "wedge_membership") is not True:
        return refuse(
            family,
            "outside_physical_wedge",
            "The point is not declared inside the outer physical wedge (U_S > 0).",
            "wedge_membership = True",
        )

    a2 = _rational(lookup(request.mathematical_context, "collapse_coefficient_A2"))
    if a2 is None:
        return refuse(
            family,
            "non_rational_input",
            "collapse_coefficient_A2 must be an exact int/Fraction value.",
            "exact rational collapse_coefficient_A2",
        )
    if a2 <= 0:
        return refuse(
            family,
            "nonpositive_A2",
            "A2 <= 0 contradicts the sum-of-positives factorization at the extremal edge.",
            "collapse_coefficient_A2 > 0",
        )

    log_derivative = _rational(lookup(request.mathematical_context, "transverse_log_derivative"))
    if log_derivative is None:
        return refuse(
            family,
            "non_rational_input",
            "transverse_log_derivative must be an exact int/Fraction value.",
            "exact rational transverse_log_derivative",
        )
    if log_derivative == 0:
        return refuse(
            family,
            "degenerate_transverse_derivative",
            "d/dS log(G_J*G_Q) = 0 at the edge: the sign gate degenerates; the locus belongs to "
            "the corner stratum (newton_wedge_corner).",
            "transverse_log_derivative != 0",
        )

    extremal_value = log_derivative / a2

    steps = (
        RouteStep(
            "restrict-edge",
            "restrict_to_extremal_edge",
            ("wedge_point",),
            ("extremal_edge_point",),
            freeze_mapping(
                {
                    "edge": "S_ext = pi*sqrt(4*J^2 + Q^4)",
                    "wedge": "S, J, Q > 0 and U_S > 0",
                }
            ),
        ),
        RouteStep(
            "read-collapse-germ",
            "read_generic_collapse_germ",
            ("extremal_edge_point",),
            ("extremal_collapse_germ",),
            freeze_mapping(
                {
                    "pole_order": 3,
                    "coefficient_formula": "R_ext = (1/A2) * d/dS log(G_J*G_Q)",
                    "leading_coefficient": extremal_value,
                    "transverse_log_derivative_sign": "negative" if log_derivative < 0 else "positive",
                }
            ),
        ),
        RouteStep(
            "gate-sign",
            "gate_sign_by_sturm",
            ("extremal_collapse_germ",),
            ("edge_sign_certificate",),
            freeze_mapping(
                {
                    "certificate_id": "lead7_test8",
                    "sturm_certificates": (
                        "H~(t) = 2t^5 + 5t^4 - 15t^3 - 7t^2 + 15t + 8 > 0 on [1, infinity)",
                        "9F + G > 0 on [1, infinity)",
                    ),
                    "assembly": "pi^2*F + G = (pi^2 - 9)*F + (9F + G) > 0 using pi^2 > 9",
                }
            ),
        ),
        RouteStep(
            "emit-extremal-pole",
            "emit_extremal_pole_route",
            ("edge_sign_certificate",),
            ("host_extremal_pole_certificate",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=EXTREMAL_FACE_CONTRACT,
        steps=steps,
        data_dependencies=(
            "wedge_membership",
            "collapse_coefficient_A2",
            "transverse_log_derivative",
        ),
        required_intermediate_objects=(
            "extremal_edge_point",
            "extremal_collapse_germ",
            "edge_sign_certificate",
        ),
        completion_condition=(
            "The external executor certifies the order-3 extremal-edge pole law in host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=4,
            scout_operation_count=2,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# newton_wedge_corner
# ---------------------------------------------------------------------------

NEWTON_CORNER_CERTIFICATES = (
    Obligation(
        "vertex-coefficient-closed-form",
        "The vertex coefficients follow the closed form A = -p0^2 + p0*p1 - p0*p2 + 2*p0 + p1*p2 "
        "- p2^2 + 2*p2 (and its q-mirror) exactly.",
        "exact-identity-replay",
    ),
    Obligation(
        "unit-factor-invariance",
        "The corner order is invariant under unit factors h_i(s) in the face data.",
        "exact-identity-replay",
    ),
    Obligation(
        "synthetic-corner-replays",
        "Synthetic corner fixtures replay the support-function order along declared directions.",
        "external-replay",
    ),
)

NEWTON_CORNER_CONTRACT = RouteContract(
    route_family="newton_wedge_corner",
    accepted_problem_shape="corner_pole_order",
    required_hypotheses=(
        "two parity variables vanish together at the corner",
        "single-face data known on both incident faces",
        "the corner value is NOT the superposition of the two face laws (mixed excess certified)",
    ),
    required_evidence=("newton_corner scout evidence", "integer corner exponent pairs"),
    produced_obligations=(
        Obligation(
            "execute-corner-order",
            "Certify the corner pole order via the polar Newton support function.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "facet-parallel directions: the front-face coefficient is unresolved (open)",
        "vertex cancellation when a vertex coefficient vanishes",
        "codimension >= 3 corners are outside this contract",
    ),
    execution_module="external.newton_wedge_corner_executor",
    certificate_obligations=NEWTON_CORNER_CERTIFICATES,
    source_references=(
        "paper/pfc_normal_forms.tex#thm:pure",
        "paper/lead7_kn_n3_dbp_metric.tex#sec:gate",
        "CELLA_ARCHITECTURE_v1.3.md#17.1",
    ),
)


def recognize_newton_wedge_corner(request: PathfinderRequest) -> RecognitionOutcome:
    family = NEWTON_CORNER_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, NEWTON_CORNER_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    evidence = evidence_by_family(request, "newton_corner")
    if evidence is None:
        result = newton_corner_scout(lower_request(request), request.analysis_budget)
        if result is None:
            return refuse(
                family,
                "missing_corner_exponents",
                "corner_exponents must be a tuple of three integer (p, q) pairs and no "
                "newton_corner evidence was supplied.",
                "corner_exponents: three integer (p, q) pairs",
            )
        evidence = dict(result.structural_fingerprint)

    steps = (
        RouteStep(
            "build-polar-vertices",
            "build_polar_newton_vertices",
            ("corner_exponents",),
            ("polar_newton_vertices",),
            freeze_mapping(
                {
                    "exponent_pairs": evidence.get("exponent_pairs"),
                    "polar_vertices": evidence.get("polar_vertices"),
                    "vertex_coefficient_a": evidence.get("vertex_coefficient_a"),
                    "vertex_coefficient_b": evidence.get("vertex_coefficient_b"),
                    "vertex_cancellation": evidence.get("vertex_cancellation"),
                }
            ),
        ),
        RouteStep(
            "evaluate-support",
            "evaluate_support_function",
            ("polar_newton_vertices",),
            ("corner_support_values",),
            freeze_mapping(
                {
                    "support_function": "m(a) = max over polar vertices v of -<a, v>",
                    "support_balanced_diagonal": evidence.get("support_balanced_diagonal"),
                    "support_axis_x": evidence.get("support_axis_x"),
                    "support_axis_y": evidence.get("support_axis_y"),
                }
            ),
        ),
        RouteStep(
            "emit-corner-order",
            "emit_corner_order_route",
            ("corner_support_values",),
            ("host_corner_order_certificate",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=NEWTON_CORNER_CONTRACT,
        steps=steps,
        data_dependencies=("corner_exponents",),
        required_intermediate_objects=("polar_newton_vertices", "corner_support_values"),
        completion_condition=(
            "The external executor certifies the corner pole order along the declared directions "
            "in host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=3,
            scout_operation_count=3,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


PROVIDERS = (
    RouteProvider(
        route_family="local_metric_germ",
        contract=LOCAL_GERM_CONTRACT,
        recognizer=recognize_local_metric_germ,
        native_scouts=(),
        wrapper_capabilities=("laurent_germ_readout",),
    ),
    RouteProvider(
        route_family="parity_fixed_face",
        contract=PARITY_FACE_CONTRACT,
        recognizer=recognize_parity_fixed_face,
        native_scouts=(),
        wrapper_capabilities=("parity_normal_form",),
    ),
    RouteProvider(
        route_family="extremal_face",
        contract=EXTREMAL_FACE_CONTRACT,
        recognizer=recognize_extremal_face,
        native_scouts=(sturm_scout,),
        wrapper_capabilities=("edge_restriction", "sturm_sign_gate"),
    ),
    RouteProvider(
        route_family="newton_wedge_corner",
        contract=NEWTON_CORNER_CONTRACT,
        recognizer=recognize_newton_wedge_corner,
        native_scouts=(newton_corner_scout,),
        wrapper_capabilities=("polar_vertex_construction", "support_function_evaluation"),
    ),
)
