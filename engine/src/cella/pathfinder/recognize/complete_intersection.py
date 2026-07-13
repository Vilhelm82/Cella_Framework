"""Complete-intersection route recognizers: regular sequence and degree balance.

``regular_sequence_complete_intersection`` (v1.3 §11.7, route ladder Route B):
a certified fresh-variable monic regular sequence makes the ideal a complete
intersection — codimension equals the generator count, the quotient is
Cohen-Macaulay, and there are no embedded associated primes.  The
``ring_safe_monic`` witness holds over any coefficient ring; the
``field_unit_leading_only`` witness is admissible only when the coefficient
domain is a field.  Candidate primality, Jacobian gates, and degree balance
remain external certificate obligations.

``degree_balance_closure`` (v1.3 §12.2 with the §11.7 degree-balance step):
once regularity is certified, the complete-intersection degree is the product
of the generators' weighted degrees.  When the declared candidate component
degrees sum exactly to that product, no minimal component is missing; a
mismatch is a mathematical refusal, not an implementation gap.

Sources: CELLA_ARCHITECTURE_v1.3.md#11.7, #11.8, #11.9, #12.2 and
campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.2.
"""

from __future__ import annotations

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.problem import lower_request
from ..ir.values import FrozenValue, freeze_mapping
from ..plan.admissibility import evidence_by_family, family_enabled, lookup, refuse
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider
from ..scout import degree_balance_scout, fresh_variable_monic_scout


ACCEPTED_SHAPES = (
    "ideal_decomposition",
    "component_certification",
    "dimension_degree_certification",
)
_SHAPE_LABEL = "|".join(ACCEPTED_SHAPES)

_FIELD_DOMAINS = ("QQ", "Q")


def _require_accepted_shape(request: PathfinderRequest, family: str) -> RecognitionOutcome | None:
    shape = lookup(request.mathematical_context, "problem_shape")
    if shape not in ACCEPTED_SHAPES:
        return refuse(
            family,
            "shape_mismatch",
            "The task does not declare a complete-intersection certification shape.",
            *ACCEPTED_SHAPES,
        )
    return None


def _fresh_monic_fingerprint(request: PathfinderRequest) -> dict[str, FrozenValue] | None:
    fingerprint = evidence_by_family(request, "fresh_variable_monic")
    if fingerprint is not None:
        return fingerprint
    evidence = fresh_variable_monic_scout(lower_request(request), request.analysis_budget)
    if evidence is None:
        return None
    return dict(evidence.structural_fingerprint)


def _is_field_domain(request: PathfinderRequest) -> bool:
    problem = lower_request(request)
    if problem.ring is None:
        return False
    domain = problem.ring.coefficient_domain
    return domain in _FIELD_DOMAINS or domain.startswith("GF(")


# ---------------------------------------------------------------------------
# regular_sequence_complete_intersection — Route B


REGULAR_SEQUENCE_CI_CERTIFICATES = (
    Obligation(
        "ci-height-equals-generators",
        "height(I) equals the generator count of the certified regular sequence.",
        "exact-height-witness",
    ),
    Obligation(
        "ci-candidate-primality",
        "Each candidate component ideal is prime.",
        "external-primality-certificate",
    ),
    Obligation(
        "ci-jacobian-minor",
        "A codimension-sized Jacobian minor is nonzero on each candidate component.",
        "exact-jacobian-witness",
    ),
    Obligation(
        "ci-degree-balance",
        "deg(I) equals the sum of the candidate component degrees in one declared DegreeSpec.",
        "exact-degree-balance",
    ),
)

REGULAR_SEQUENCE_CI_CONTRACT = RouteContract(
    route_family="regular_sequence_complete_intersection",
    accepted_problem_shape=_SHAPE_LABEL,
    required_hypotheses=(
        "the generators form a certified fresh-variable regular sequence",
        "a unit-leading-only certificate requires the coefficient domain to be a field",
        "every degree below is bound to one declared DegreeSpec",
    ),
    required_evidence=("fresh_variable_monic scout evidence with regular_sequence_certified",),
    produced_obligations=(
        Obligation(
            "execute-ci-certification",
            "Derive the complete-intersection invariants and emit the CI certificate obligations.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "saturation may destroy the displayed complete-intersection presentation; re-certify after localization (v1.3 §11.8)",
        "input without a certified regular sequence is refused, never assumed regular",
    ),
    execution_module="external.complete_intersection_certification_executor",
    certificate_obligations=REGULAR_SEQUENCE_CI_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#11.7",
        "CELLA_ARCHITECTURE_v1.3.md#11.8",
        "CELLA_ARCHITECTURE_v1.3.md#11.9",
        "research/campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.2",
    ),
)


def recognize_regular_sequence_complete_intersection(
    request: PathfinderRequest,
) -> RecognitionOutcome:
    """Route B: fresh-variable monic regular sequence to CI invariants (v1.3 §11.7)."""

    family = REGULAR_SEQUENCE_CI_CONTRACT.route_family
    for gate in (family_enabled(request, family), _require_accepted_shape(request, family)):
        if gate is not None:
            return gate

    fingerprint = _fresh_monic_fingerprint(request)
    if fingerprint is None:
        return refuse(
            family,
            "evidence_unavailable",
            "No fresh_variable_monic evidence is available for the declared presentation.",
            "fresh_variable_monic scout evidence",
        )
    if fingerprint.get("regular_sequence_certified") is not True:
        return refuse(
            family,
            "not_a_certified_regular_sequence",
            "The generators do not carry a certified fresh-variable regular-sequence witness.",
            "regular_sequence_certified = True",
        )
    ring_safe = fingerprint.get("ring_safe_monic") is True
    field_only = fingerprint.get("field_unit_leading_only") is True
    if not ring_safe:
        if not field_only:
            return refuse(
                family,
                "not_a_certified_regular_sequence",
                "The evidence certifies neither a ring-safe monic nor a field unit-leading sequence.",
                "ring_safe_monic or field_unit_leading_only",
            )
        if not _is_field_domain(request):
            return refuse(
                family,
                "unit_leading_requires_field",
                "A unit-leading-only regular-sequence witness is admissible only over a coefficient field.",
                "field coefficient domain",
            )
    certificate_kind = "ring_safe_monic" if ring_safe else "field_unit_leading"

    generator_count = fingerprint.get("generator_count")
    if not isinstance(generator_count, int) or isinstance(generator_count, bool) or generator_count <= 0:
        return refuse(
            family,
            "evidence_unavailable",
            "The fresh_variable_monic evidence does not carry a usable generator count.",
            "generator_count",
        )

    steps = (
        RouteStep(
            "certify-regular-sequence",
            "certify_fresh_variable_regular_sequence",
            ("target_ideal",),
            ("regular_sequence_certificate",),
            freeze_mapping(
                {
                    "certificate_kind": certificate_kind,
                    "fresh_variables": fingerprint.get("fresh_variables", ()),
                    "sequence_order": fingerprint.get("sequence_order", ()),
                }
            ),
        ),
        RouteStep(
            "derive-ci-invariants",
            "derive_complete_intersection_invariants",
            ("regular_sequence_certificate",),
            ("complete_intersection_invariants",),
            freeze_mapping(
                {
                    "codimension": generator_count,
                    "conclusions": (
                        "complete_intersection",
                        "cohen_macaulay",
                        "no_embedded_primes",
                    ),
                }
            ),
        ),
        RouteStep(
            "emit-ci-obligations",
            "emit_ci_certificate_obligations",
            ("complete_intersection_invariants",),
            ("host_ci_certificate_obligations",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=REGULAR_SEQUENCE_CI_CONTRACT,
        steps=steps,
        data_dependencies=("target_ideal",),
        required_intermediate_objects=(
            "regular_sequence_certificate",
            "complete_intersection_invariants",
        ),
        completion_condition="The external executor emits the CI invariants and the external certificate obligations.",
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=generator_count,
            scout_operation_count=1,
            expression_depth=0,
        ),
        structural_preference_rank=1,
    )


# ---------------------------------------------------------------------------
# degree_balance_closure — CI degree route


DEGREE_BALANCE_CLOSURE_CERTIFICATES = (
    Obligation(
        "closure-candidate-primality",
        "Each declared candidate component ideal is prime.",
        "external-primality-certificate",
    ),
    Obligation(
        "closure-ideal-containment",
        "The ideal is contained in each declared candidate component.",
        "exact-ideal-membership",
    ),
    Obligation(
        "closure-jacobian-gate",
        "A codimension-sized Jacobian minor is nonzero on each candidate component.",
        "exact-jacobian-witness",
    ),
    Obligation(
        "closure-component-degrees",
        "Each candidate component has exactly its declared degree under the declared DegreeSpec.",
        "exact-degree-witness",
    ),
)

DEGREE_BALANCE_CLOSURE_CONTRACT = RouteContract(
    route_family="degree_balance_closure",
    accepted_problem_shape=_SHAPE_LABEL,
    required_hypotheses=(
        "the generators form a certified fresh-variable regular sequence",
        "the candidate component degrees are declared under the same DegreeSpec as the CI product",
        "the candidate component degree sum equals the complete-intersection degree exactly",
    ),
    required_evidence=(
        "fresh_variable_monic scout evidence with regular_sequence_certified",
        "degree_balance scout evidence with the exact weighted CI product",
        "declared candidate_component_degrees",
    ),
    produced_obligations=(
        Obligation(
            "execute-minimal-prime-closure",
            "Emit the minimal-prime closure obligations for the balanced candidate set.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "a degree-sum mismatch means a minimal component is missing or a declared degree is wrong; the route refuses",
        "saturation invalidates the displayed CI degree; re-certify after localization (v1.3 §11.8)",
    ),
    execution_module="external.degree_balance_closure_executor",
    certificate_obligations=DEGREE_BALANCE_CLOSURE_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#12.2",
        "CELLA_ARCHITECTURE_v1.3.md#11.7",
        "research/campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.2",
    ),
)


def recognize_degree_balance_closure(request: PathfinderRequest) -> RecognitionOutcome:
    """CI degree route: candidate degree sum must equal the CI product (v1.3 §12.2)."""

    family = DEGREE_BALANCE_CLOSURE_CONTRACT.route_family
    for gate in (family_enabled(request, family), _require_accepted_shape(request, family)):
        if gate is not None:
            return gate

    fresh = _fresh_monic_fingerprint(request)
    if fresh is None:
        return refuse(
            family,
            "evidence_unavailable",
            "No fresh_variable_monic evidence is available for the declared presentation.",
            "fresh_variable_monic scout evidence",
        )
    if fresh.get("regular_sequence_certified") is not True:
        return refuse(
            family,
            "not_a_certified_regular_sequence",
            "The degree-balance route requires a certified regular sequence before any degree is meaningful.",
            "regular_sequence_certified = True",
        )

    balance = evidence_by_family(request, "degree_balance")
    if balance is None:
        evidence = degree_balance_scout(lower_request(request), request.analysis_budget)
        if evidence is None:
            return refuse(
                family,
                "evidence_unavailable",
                "No degree_balance evidence is available for the declared presentation.",
                "degree_balance scout evidence",
            )
        balance = dict(evidence.structural_fingerprint)
    ci_degree = balance.get("complete_intersection_degree")
    if not isinstance(ci_degree, int) or isinstance(ci_degree, bool) or ci_degree <= 0:
        return refuse(
            family,
            "evidence_unavailable",
            "The degree_balance evidence does not carry an exact complete-intersection degree.",
            "complete_intersection_degree",
        )

    candidates = lookup(request.mathematical_context, "candidate_component_degrees")
    if (
        not isinstance(candidates, tuple)
        or not candidates
        or not all(isinstance(d, int) and not isinstance(d, bool) and d > 0 for d in candidates)
    ):
        return refuse(
            family,
            "missing_candidate_component_degrees",
            "The request must declare the candidate component degrees as a tuple of positive integers.",
            "mathematical_context.candidate_component_degrees",
        )
    degree_sum = sum(candidates)  # type: ignore[arg-type]
    if degree_sum != ci_degree:
        return refuse(
            family,
            "degree_balance_failed",
            f"The candidate component degrees sum to {degree_sum} but the complete-intersection degree is {ci_degree}; a minimal component is missing or a declared degree is wrong.",
            "sum(candidate_component_degrees) = complete_intersection_degree",
        )

    steps = (
        RouteStep(
            "certify-regular-sequence",
            "certify_regular_sequence",
            ("target_ideal",),
            ("regular_sequence_certificate",),
            freeze_mapping(
                {
                    "fresh_variables": fresh.get("fresh_variables", ()),
                    "sequence_order": fresh.get("sequence_order", ()),
                }
            ),
        ),
        RouteStep(
            "compute-ci-degree",
            "compute_weighted_ci_degree",
            ("regular_sequence_certificate",),
            ("complete_intersection_degree",),
            freeze_mapping(
                {
                    "weighted_degrees": balance.get("weighted_degrees", ()),
                    "weights": balance.get("weights", ()),
                    "complete_intersection_degree": ci_degree,
                }
            ),
        ),
        RouteStep(
            "compare-degree-sum",
            "compare_component_degree_sum",
            ("complete_intersection_degree",),
            ("degree_balance_record",),
            freeze_mapping(
                {
                    "candidate_component_degrees": candidates,
                    "candidate_degree_sum": degree_sum,
                    "balanced": True,
                }
            ),
        ),
        RouteStep(
            "emit-closure-obligations",
            "emit_minimal_prime_closure_obligations",
            ("degree_balance_record",),
            ("host_minimal_prime_closure_obligations",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=DEGREE_BALANCE_CLOSURE_CONTRACT,
        steps=steps,
        data_dependencies=("target_ideal", "candidate_component_degrees"),
        required_intermediate_objects=(
            "regular_sequence_certificate",
            "complete_intersection_degree",
            "degree_balance_record",
        ),
        completion_condition="The external executor emits the minimal-prime closure obligations for every balanced candidate.",
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=len(candidates),
            scout_operation_count=2,
            expression_depth=0,
        ),
        structural_preference_rank=1,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="regular_sequence_complete_intersection",
        contract=REGULAR_SEQUENCE_CI_CONTRACT,
        recognizer=recognize_regular_sequence_complete_intersection,
        native_scouts=(fresh_variable_monic_scout,),
        wrapper_capabilities=("regular_sequence_certification",),
    ),
    RouteProvider(
        route_family="degree_balance_closure",
        contract=DEGREE_BALANCE_CLOSURE_CONTRACT,
        recognizer=recognize_degree_balance_closure,
        native_scouts=(fresh_variable_monic_scout, degree_balance_scout),
        wrapper_capabilities=("regular_sequence_certification", "weighted_degree_bookkeeping"),
    ),
)
