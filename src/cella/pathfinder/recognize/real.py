"""Exact-real route-family providers (invariant floor, Sturm, pencils, inertia).

Families: ``invariant_floor_real``, ``sturm_escalation``,
``matrix_pencil_selection``, ``exact_rational_inertia``.

Invariant-floor doctrine (CELLA_ARCHITECTURE_v1.3 SS16): discharge a claim at
the lowest sufficient exact invariant level.  Coefficient data (traces,
elementary symmetric functions, determinants, characteristic-polynomial
coefficients) precede root isolation; spectrum access is an escalation only
when the claim concerns roots, their order, or their selection as such.

All numbers are int/Fraction (bool is not a number; no floats).  Inertia
triples and Sturm counts recorded below come from native scouts and are route
evidence for external replay; the certified host classification remains
external.
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
from ..scout.inertia import exact_inertia_scout
from ..scout.regularity import regularity_scout
from ..scout.sturm import sturm_scout


def _rational(value: FrozenValue | None) -> Fraction | None:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        return None
    return Fraction(value)


# ---------------------------------------------------------------------------
# invariant_floor_real
# ---------------------------------------------------------------------------

INVARIANT_FLOOR_CERTIFICATES = (
    Obligation(
        "observation-family-adequacy",
        "Law 15: the chosen observation family is adequate for the declared claim level; "
        "coefficient invariants discharge coefficient claims, and root claims carry an explicit "
        "escalation.",
        "hypothesis-audit",
    ),
)

INVARIANT_FLOOR_CONTRACT = RouteContract(
    route_family="invariant_floor_real",
    accepted_problem_shape="real_decision",
    required_hypotheses=(
        "the claim level is declared: coefficient, root_order, or root_selection",
        "coefficient invariants precede root isolation (invariant-floor doctrine)",
    ),
    required_evidence=("declared claim level",),
    produced_obligations=(
        Obligation(
            "execute-invariant-floor-decision",
            "Discharge the real decision at the lowest sufficient exact invariant level.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "root_order and root_selection claims escalate to sturm_escalation by declared route",
        "transcendental pins are outside the native exact-rational scope",
    ),
    execution_module="external.invariant_floor_real_executor",
    certificate_obligations=INVARIANT_FLOOR_CERTIFICATES,
    source_references=("CELLA_ARCHITECTURE_v1.3.md#16",),
)

_CLAIM_LEVELS = ("coefficient", "root_order", "root_selection")

_COEFFICIENT_FLOOR = (
    "traces, elementary symmetric functions, determinants, charpoly coefficients precede root "
    "isolation"
)


def recognize_invariant_floor_real(request: PathfinderRequest) -> RecognitionOutcome:
    family = INVARIANT_FLOOR_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, INVARIANT_FLOOR_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    claim_level = lookup(request.mathematical_context, "claim_level")
    if claim_level not in _CLAIM_LEVELS:
        return refuse(
            family,
            "unknown_claim_level",
            "The claim level must be one of coefficient, root_order, root_selection.",
            "claim_level in {coefficient, root_order, root_selection}",
        )

    if claim_level == "coefficient":
        steps = (
            RouteStep(
                "check-coefficient-invariants",
                "check_coefficient_invariants",
                ("real_decision_claim",),
                ("coefficient_invariant_report",),
                freeze_mapping({"invariant_floor": _COEFFICIENT_FLOOR}),
            ),
            RouteStep(
                "emit-coefficient-floor",
                "emit_coefficient_floor_route",
                ("coefficient_invariant_report",),
                ("host_coefficient_floor_decision",),
                freeze_mapping({"claim_level": "coefficient"}),
            ),
        )
        intermediates = ("coefficient_invariant_report",)
        completion = (
            "The external executor discharges the coefficient-level claim from coefficient "
            "invariants alone in host bindings."
        )
    else:
        steps = (
            RouteStep(
                "certify-floor-insufficiency",
                "certify_floor_insufficiency",
                ("real_decision_claim",),
                ("floor_insufficiency_certificate",),
                freeze_mapping(
                    {
                        "claim_level": claim_level,
                        "reason": "the claim concerns roots as such; coefficient invariants are "
                        "below the required floor",
                    }
                ),
            ),
            RouteStep(
                "escalate-to-root-isolation",
                "escalate_to_root_isolation",
                ("floor_insufficiency_certificate",),
                ("root_isolation_escalation",),
                freeze_mapping({"next_route_family": "sturm_escalation"}),
            ),
            RouteStep(
                "emit-escalation",
                "emit_escalation_route",
                ("root_isolation_escalation",),
                ("host_escalation_declaration",),
            ),
        )
        intermediates = ("floor_insufficiency_certificate", "root_isolation_escalation")
        completion = (
            "The external executor records the certified escalation to root isolation "
            "(sturm_escalation) in host bindings."
        )

    return assemble_candidate(
        request=request,
        contract=INVARIANT_FLOOR_CONTRACT,
        steps=steps,
        data_dependencies=("claim_level",),
        required_intermediate_objects=intermediates,
        completion_condition=completion,
        burden_vector=BurdenVector(
            invariant_level=0 if claim_level == "coefficient" else 1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=2,
            scout_operation_count=1,
            expression_depth=1,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# sturm_escalation
# ---------------------------------------------------------------------------

STURM_CERTIFICATES = (
    Obligation(
        "sturm-chain-replay",
        "The Sturm chain construction replays exactly over rational coefficients.",
        "exact-sturm-replay",
    ),
    Obligation(
        "endpoint-sign-evaluations",
        "Endpoint sign evaluations of every chain member are exact rational computations.",
        "exact-rational",
    ),
)

STURM_CONTRACT = RouteContract(
    route_family="sturm_escalation",
    accepted_problem_shape="real_root_count",
    required_hypotheses=(
        "univariate polynomial with exact rational coefficients, degree >= 1",
        "Sturm counts distinct roots in the half-open interval (a, b]",
    ),
    required_evidence=("sturm_chain scout evidence",),
    produced_obligations=(
        Obligation(
            "execute-sturm-root-count",
            "Certify the distinct real-root count on the declared interval by Sturm-chain replay.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "roots at the declared endpoints: Sturm counts the half-open interval (a, b]",
        "non-squarefree input counts distinct roots only",
    ),
    execution_module="external.sturm_escalation_executor",
    certificate_obligations=STURM_CERTIFICATES,
    source_references=(
        "paper/lead7_kn_n3_dbp_metric.tex#sec:gate",
        "CELLA_ARCHITECTURE_v1.3.md#16",
    ),
)


def recognize_sturm_escalation(request: PathfinderRequest) -> RecognitionOutcome:
    family = STURM_CONTRACT.route_family
    gate = family_enabled(request, family)
    if gate is not None:
        return gate

    shape = lookup(request.mathematical_context, "problem_shape")
    escalated_decision = (
        shape == "real_decision"
        and lookup(request.mathematical_context, "claim_level") == "root_order"
    )
    if shape != STURM_CONTRACT.accepted_problem_shape and not escalated_decision:
        return refuse(
            family,
            "shape_mismatch",
            "The task is neither a real_root_count nor a real_decision at claim level root_order.",
            "real_root_count",
            "real_decision with claim_level = root_order",
        )

    evidence = evidence_by_family(request, "sturm_chain")
    if evidence is None:
        result = sturm_scout(lower_request(request), request.analysis_budget)
        if result is None:
            return refuse(
                family,
                "missing_polynomial",
                "univariate_coefficients must be a non-empty tuple of exact int/Fraction values "
                "of degree >= 1.",
                "exact rational univariate_coefficients, degree >= 1",
            )
        evidence = dict(result.structural_fingerprint)

    steps = (
        RouteStep(
            "build-chain",
            "build_sturm_chain",
            ("univariate_coefficients",),
            ("sturm_chain",),
            freeze_mapping({"degree": evidence.get("degree")}),
        ),
        RouteStep(
            "count-sign-changes",
            "count_sign_changes_on_interval",
            ("sturm_chain",),
            ("interval_root_count",),
            freeze_mapping(
                {
                    "degree": evidence.get("degree"),
                    "distinct_real_roots_in_interval": evidence.get(
                        "distinct_real_roots_in_interval"
                    ),
                    "interval": evidence.get("interval"),
                    "count_convention": "distinct roots in the half-open interval (a, b]",
                }
            ),
        ),
        RouteStep(
            "emit-root-count",
            "emit_root_count_route",
            ("interval_root_count",),
            ("host_root_count_certificate",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=STURM_CONTRACT,
        steps=steps,
        data_dependencies=("univariate_coefficients", "interval"),
        required_intermediate_objects=("sturm_chain", "interval_root_count"),
        completion_condition=(
            "The external executor certifies the distinct real-root count by replaying the Sturm "
            "chain in host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=2,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=3,
            scout_operation_count=2,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# matrix_pencil_selection
# ---------------------------------------------------------------------------

PENCIL_CERTIFICATES = (
    Obligation(
        "complementarity-law",
        "The selected member retains the boundary orders 3/4/4 (complementarity law).",
        "exact-identity-replay",
    ),
    Obligation(
        "interior-regularity-witness",
        "The selected member has no interior role-role isotropy zero.",
        "exact-rational",
    ),
    Obligation(
        "positive-definiteness-witness",
        "The selected member carries an exact positive-definiteness witness (congruence inertia).",
        "exact-identity-replay",
    ),
)

PENCIL_CONTRACT = RouteContract(
    route_family="matrix_pencil_selection",
    accepted_problem_shape="pencil_selection",
    required_hypotheses=(
        "a declared finite pencil of candidate members",
        "per-member interior-regularity and positive-definiteness declarations",
        "exact definiteness evidence (congruence inertia, no floating eigendecomposition)",
        "exactly one member is both positive-definite and interior-regular",
    ),
    required_evidence=("pencil member declarations", "exact_rational_inertia or declared definiteness evidence"),
    produced_obligations=(
        Obligation(
            "execute-pencil-selection",
            "Certify the unique admissible pencil member and emit its selection witnesses.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "members with interior isotropy zeros acquire spurious interior poles and are rejected",
        "members losing definiteness are rejected",
    ),
    execution_module="external.matrix_pencil_selection_executor",
    certificate_obligations=PENCIL_CERTIFICATES,
    source_references=(
        "paper/lead7_kn_n3_dbp_metric.tex#sec:gate",
        "CELLA_ARCHITECTURE_v1.3.md#16",
    ),
)


def _bool_tuple(value: FrozenValue | None, expected_length: int) -> tuple[bool, ...] | None:
    if not isinstance(value, tuple) or len(value) != expected_length:
        return None
    if any(not isinstance(entry, bool) for entry in value):
        return None
    return tuple(bool(entry) for entry in value)


def recognize_matrix_pencil_selection(request: PathfinderRequest) -> RecognitionOutcome:
    family = PENCIL_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, PENCIL_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    members = lookup(request.mathematical_context, "pencil_members")
    if not isinstance(members, tuple) or not members:
        return refuse(
            family,
            "malformed_pencil_declaration",
            "pencil_members must be a non-empty tuple of member labels.",
            "non-empty pencil_members tuple",
        )
    interior_regular = _bool_tuple(
        lookup(request.mathematical_context, "member_interior_regular"), len(members)
    )
    positive_definite = _bool_tuple(
        lookup(request.mathematical_context, "member_positive_definite"), len(members)
    )
    if interior_regular is None or positive_definite is None:
        return refuse(
            family,
            "malformed_pencil_declaration",
            "member_interior_regular and member_positive_definite must be boolean tuples of the "
            "same length as pencil_members.",
            "boolean member declarations matching pencil_members",
        )

    definiteness_evidence: FrozenValue = None
    if lookup(request.mathematical_context, "symmetric_matrix") is not None:
        inertia = evidence_by_family(request, "exact_rational_inertia")
        if inertia is None:
            result = exact_inertia_scout(lower_request(request), request.analysis_budget)
            inertia = dict(result.structural_fingerprint) if result is not None else None
        if inertia is None:
            return refuse(
                family,
                "missing_definiteness_evidence",
                "The declared symmetric matrix did not yield exact congruence-inertia evidence.",
                "exact symmetric rational matrix",
            )
        definiteness_evidence = tuple(sorted(inertia.items()))
    elif lookup(request.mathematical_context, "definiteness_evidence") is not None:
        definiteness_evidence = lookup(request.mathematical_context, "definiteness_evidence")
    else:
        return refuse(
            family,
            "missing_definiteness_evidence",
            "Pencil selection requires definiteness_evidence or a symmetric matrix for exact "
            "congruence inertia.",
            "definiteness_evidence or symmetric_matrix",
        )

    admissible = tuple(
        index
        for index in range(len(members))
        if interior_regular[index] and positive_definite[index]
    )
    if len(admissible) != 1:
        return refuse(
            family,
            "selection_not_unique",
            f"{len(admissible)} pencil members are both positive-definite and interior-regular; "
            "the selection law requires exactly one.",
            "exactly one admissible pencil member",
        )
    selected = members[admissible[0]]

    steps = (
        RouteStep(
            "evaluate-definiteness",
            "evaluate_member_definiteness",
            ("pencil_members",),
            ("member_definiteness_table",),
            freeze_mapping(
                {
                    "member_positive_definite": positive_definite,
                    "definiteness_evidence": definiteness_evidence,
                }
            ),
        ),
        RouteStep(
            "exclude-isotropy-poles",
            "exclude_interior_isotropy_poles",
            ("member_definiteness_table",),
            ("interior_regular_members",),
            freeze_mapping({"member_interior_regular": interior_regular}),
        ),
        RouteStep(
            "select-member",
            "select_unique_admissible_member",
            ("interior_regular_members",),
            ("selected_pencil_member",),
            freeze_mapping({"selected_member": selected}),
        ),
        RouteStep(
            "emit-selection",
            "emit_pencil_selection_route",
            ("selected_pencil_member",),
            ("host_pencil_selection_certificate",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=PENCIL_CONTRACT,
        steps=steps,
        data_dependencies=(
            "pencil_members",
            "member_interior_regular",
            "member_positive_definite",
        ),
        required_intermediate_objects=(
            "member_definiteness_table",
            "interior_regular_members",
            "selected_pencil_member",
        ),
        completion_condition=(
            "The external executor certifies the unique admissible pencil member in host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=len(members) + 1,
            scout_operation_count=2,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# exact_rational_inertia
# ---------------------------------------------------------------------------

INERTIA_CERTIFICATES = (
    Obligation(
        "sylvester-law-replay",
        "Sylvester's law of inertia replays on the congruence block-diagonal form exactly.",
        "exact-identity-replay",
    ),
    Obligation(
        "monomial-partition-cross-check",
        "Where the bordered-Hessian context applies, det(H_b) = Delta_c + Delta_s + Delta_m "
        "cross-checks the channel classification.",
        "exact-identity-replay",
    ),
)

INERTIA_CONTRACT = RouteContract(
    route_family="exact_rational_inertia",
    accepted_problem_shape="symmetric_inertia",
    required_hypotheses=(
        "exact square symmetric rational matrix",
        "q != 0 whenever a gradient stratum is declared (use q, never |g|)",
        "the kappa_s channel does not obey the naive mirror formula (H_s is not traceless)",
    ),
    required_evidence=("exact_rational_inertia scout evidence",),
    produced_obligations=(
        Obligation(
            "execute-inertia-classification",
            "Certify INERTIA_CERTIFIED_WITH_NULLITY(rank, signature, nullity) by congruence replay.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "HIGHER_JET_REQUIRED_FOR_CLASSIFICATION along quadratic null directions (nullity > 0); "
        "the certified inertia remains valid and further classification is external",
    ),
    execution_module="external.exact_rational_inertia_executor",
    certificate_obligations=INERTIA_CERTIFICATES,
    source_references=(
        "Reference_Material/papers/current/Three_Channel_KG_Strong_Spec.md",
        "CELLA_ARCHITECTURE_v1.3.md#17.1",
    ),
)


def recognize_exact_rational_inertia(request: PathfinderRequest) -> RecognitionOutcome:
    family = INERTIA_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, INERTIA_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    # q-regularity: a declared singular gradient stratum refuses, never returns 0.
    if lookup(request.mathematical_context, "gradient") is not None:
        regularity = evidence_by_family(request, "dbp_regularity")
        if regularity is None:
            result = regularity_scout(lower_request(request), request.analysis_budget)
            regularity = dict(result.structural_fingerprint) if result is not None else None
        if regularity is None:
            return refuse(
                family,
                "non_rational_input",
                "The declared gradient must be a non-empty tuple of exact int/Fraction values.",
                "exact rational gradient",
            )
        q = _rational(regularity.get("q"))
        if q is not None and q == 0:
            return refuse(
                family,
                "singular_stratum_q_zero",
                "q = g^T g = 0 is the singular stratum: refuse, do not return 0.",
                "q != 0",
            )

    evidence = evidence_by_family(request, "exact_rational_inertia")
    if evidence is None:
        result = exact_inertia_scout(lower_request(request), request.analysis_budget)
        if result is None:
            return refuse(
                family,
                "missing_symmetric_matrix",
                "symmetric_matrix must be an exactly symmetric square tuple-of-tuples of "
                "int/Fraction values.",
                "exact square symmetric rational matrix",
            )
        evidence = dict(result.structural_fingerprint)

    positive = evidence.get("positive")
    negative = evidence.get("negative")
    nullity = evidence.get("nullity")
    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in (positive, negative, nullity)
    ):
        return refuse(
            family,
            "missing_symmetric_matrix",
            "The inertia evidence does not carry an exact (positive, negative, nullity) triple.",
            "exact congruence-inertia triple",
        )
    rank = positive + negative
    signature = positive - negative

    steps = (
        RouteStep(
            "congruence-reduce",
            "congruence_pivot_reduction",
            ("symmetric_matrix",),
            ("congruence_block_diagonal",),
            freeze_mapping(
                {
                    "positive": positive,
                    "negative": negative,
                    "nullity": nullity,
                    "pivot_rule": "1x1 and 2x2 hyperbolic pivots; no floating eigendecomposition",
                    "hyperbolic_block": "[[0,b],[b,0]] contributes one positive and one negative "
                    "direction",
                }
            ),
        ),
        RouteStep(
            "emit-inertia",
            "emit_inertia_classification",
            ("congruence_block_diagonal",),
            ("host_inertia_classification",),
            freeze_mapping(
                {
                    "classification": (
                        f"INERTIA_CERTIFIED_WITH_NULLITY(rank={rank}, signature={signature}, "
                        f"nullity={nullity})"
                    ),
                }
            ),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=INERTIA_CONTRACT,
        steps=steps,
        data_dependencies=("symmetric_matrix",),
        required_intermediate_objects=("congruence_block_diagonal",),
        completion_condition=(
            "The external executor certifies the inertia classification by congruence replay in "
            "host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=rank + nullity + 1,
            scout_operation_count=2,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


PROVIDERS = (
    RouteProvider(
        route_family="invariant_floor_real",
        contract=INVARIANT_FLOOR_CONTRACT,
        recognizer=recognize_invariant_floor_real,
        native_scouts=(),
        wrapper_capabilities=("coefficient_invariant_readout",),
    ),
    RouteProvider(
        route_family="sturm_escalation",
        contract=STURM_CONTRACT,
        recognizer=recognize_sturm_escalation,
        native_scouts=(sturm_scout,),
        wrapper_capabilities=("sturm_chain_replay",),
    ),
    RouteProvider(
        route_family="matrix_pencil_selection",
        contract=PENCIL_CONTRACT,
        recognizer=recognize_matrix_pencil_selection,
        native_scouts=(exact_inertia_scout,),
        wrapper_capabilities=("pencil_member_evaluation", "congruence_inertia"),
    ),
    RouteProvider(
        route_family="exact_rational_inertia",
        contract=INERTIA_CONTRACT,
        recognizer=recognize_exact_rational_inertia,
        native_scouts=(exact_inertia_scout, regularity_scout),
        wrapper_capabilities=("congruence_inertia",),
    ),
)
