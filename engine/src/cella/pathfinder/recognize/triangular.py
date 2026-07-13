"""Triangular-tower route recognizers: substitution, domain tower, linear inverse.

Three route families over declared ideal presentations:

``direct_substitution`` (v1.3 route ladder Route A, §12.1): a triangular tower
whose every introduced variable is monic supports forward substitution with
substitution certificates instead of Groebner problems.

``triangular_domain_tower`` (v1.3 route ladder Route C, prime certificate
grade P2): the same tower order certifies primality when each step is monic
irreducible over the fraction field of the previous stage.  Irreducibility is
not checkable natively, so it is emitted as an external certificate
obligation with per-step witnesses.

``linear_inverse_ring_map`` (v1.3 prime certificate grade P1): a generator
linear in an eliminable fresh variable with unit leading coefficient yields an
explicit inverse ring map onto a smaller presentation.

Sources: CELLA_ARCHITECTURE_v1.3.md#11.9, #12.1 and
campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.2.
"""

from __future__ import annotations

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.expression import ExpressionShadowUnavailable
from ..ir.obligation import Obligation
from ..ir.polynomial import PolynomialShadow, shadow_polynomial
from ..ir.problem import lower_request
from ..ir.values import FrozenValue, freeze_mapping
from ..plan.admissibility import evidence_by_family, family_enabled, lookup, refuse
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider
from ..scout import fresh_variable_monic_scout, triangular_tower_scout


ACCEPTED_SHAPES = ("ideal_projection", "ideal_decomposition", "prime_certificate")
_SHAPE_LABEL = "|".join(ACCEPTED_SHAPES)

_FIELD_DOMAINS = ("QQ", "Q")


def _require_accepted_shape(request: PathfinderRequest, family: str) -> RecognitionOutcome | None:
    shape = lookup(request.mathematical_context, "problem_shape")
    if shape not in ACCEPTED_SHAPES:
        return refuse(
            family,
            "shape_mismatch",
            "The task does not declare a triangular-route problem shape.",
            *ACCEPTED_SHAPES,
        )
    return None


def _require_declared_characteristic(request: PathfinderRequest, family: str) -> RecognitionOutcome | None:
    """Any declared characteristic is admissible here; undeclared is not."""

    characteristic = lookup(request.mathematical_context, "characteristic")
    if not isinstance(characteristic, int) or isinstance(characteristic, bool):
        return refuse(
            family,
            "missing_characteristic",
            "The coefficient characteristic must be declared exactly.",
            "integer characteristic",
        )
    return None


def _tower_fingerprint(request: PathfinderRequest) -> dict[str, FrozenValue] | None:
    fingerprint = evidence_by_family(request, "triangular_tower")
    if fingerprint is not None:
        return fingerprint
    evidence = triangular_tower_scout(lower_request(request), request.analysis_budget)
    if evidence is None:
        return None
    return dict(evidence.structural_fingerprint)


def _tower_counts(fingerprint: dict[str, FrozenValue]) -> tuple[int, int, int] | None:
    """(generator_count, non_seed_step_count, monic_step_count) or None if malformed."""

    introduced = fingerprint.get("introduced_variables")
    monic = fingerprint.get("monic_step_count")
    generator_count = fingerprint.get("generator_count")
    if not isinstance(introduced, tuple) or not all(isinstance(item, str) for item in introduced):
        return None
    if not isinstance(monic, int) or isinstance(monic, bool):
        return None
    if not isinstance(generator_count, int) or isinstance(generator_count, bool):
        return None
    non_seed = sum(1 for variable in introduced if variable)
    return generator_count, non_seed, monic


# ---------------------------------------------------------------------------
# direct_substitution — Route A


DIRECT_SUBSTITUTION_CERTIFICATES = (
    Obligation(
        "substitution-ideal-equality",
        "Forward substitution along the declared tower order preserves the ideal exactly.",
        "exact-ideal-equality",
    ),
    Obligation(
        "tower-step-monic",
        "Each eliminated variable's defining generator is monic in that variable.",
        "exact-leading-coefficient",
    ),
)

DIRECT_SUBSTITUTION_CONTRACT = RouteContract(
    route_family="direct_substitution",
    accepted_problem_shape=_SHAPE_LABEL,
    required_hypotheses=(
        "the generators admit a triangular tower order",
        "every non-seed tower step is monic in its introduced variable",
        "the coefficient characteristic is declared exactly",
    ),
    required_evidence=("triangular_tower scout evidence with a complete monic tower",),
    produced_obligations=(
        Obligation(
            "execute-direct-substitution",
            "Substitute forward along the tower and emit the substituted presentation.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "a non-monic tower step blocks substitution and requires the domain-tower or elimination route",
        "generators outside a triangular order require another route family",
    ),
    execution_module="external.direct_substitution_executor",
    certificate_obligations=DIRECT_SUBSTITUTION_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#11.9",
        "CELLA_ARCHITECTURE_v1.3.md#12.1",
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.2",
    ),
)


def recognize_direct_substitution(request: PathfinderRequest) -> RecognitionOutcome:
    """Route A: substitution certificates, not Groebner problems (v1.3 §12.1)."""

    family = DIRECT_SUBSTITUTION_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _require_accepted_shape(request, family),
        _require_declared_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    fingerprint = _tower_fingerprint(request)
    if fingerprint is None:
        return refuse(
            family,
            "evidence_unavailable",
            "No triangular_tower evidence is available for the declared presentation.",
            "triangular_tower scout evidence",
        )
    if fingerprint.get("triangular") is not True:
        return refuse(
            family,
            "not_a_triangular_tower",
            "The generators do not admit an order introducing one fresh variable per step.",
            "complete triangular tower order",
        )
    counts = _tower_counts(fingerprint)
    if counts is None:
        return refuse(
            family,
            "evidence_unavailable",
            "The triangular_tower evidence does not carry usable step records.",
            "introduced_variables",
            "monic_step_count",
        )
    generator_count, non_seed, monic = counts
    if monic != non_seed:
        return refuse(
            family,
            "nonmonic_tower_step",
            "At least one introduced tower variable is not monic in its defining generator, so exact forward substitution is not available.",
            "every non-seed tower step monic in its introduced variable",
        )

    introduced = fingerprint.get("introduced_variables")
    steps = (
        RouteStep(
            "order-tower",
            "order_generators_by_tower",
            ("target_ideal",),
            ("ordered_tower_generators",),
            freeze_mapping(
                {
                    "tower_order": fingerprint.get("tower_order", ()),
                    "introduced_variables": introduced,
                }
            ),
        ),
        RouteStep(
            "substitute-forward",
            "substitute_forward",
            ("ordered_tower_generators",),
            ("substituted_presentation",),
            freeze_mapping(
                {"eliminated_variables": tuple(v for v in introduced if v)}  # type: ignore[union-attr]
            ),
        ),
        RouteStep(
            "emit-substituted",
            "emit_substituted_presentation",
            ("substituted_presentation",),
            ("host_substituted_presentation",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=DIRECT_SUBSTITUTION_CONTRACT,
        steps=steps,
        data_dependencies=("target_ideal",),
        required_intermediate_objects=("ordered_tower_generators", "substituted_presentation"),
        completion_condition="The external executor emits the substituted presentation in host bindings.",
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=generator_count,
            scout_operation_count=1,
            expression_depth=0,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# triangular_domain_tower — Route C / prime certificate grade P2


TRIANGULAR_DOMAIN_TOWER_CERTIFICATES = (
    Obligation(
        "tower-step-monic-irreducible",
        "Each non-seed tower step is monic and irreducible over the fraction field of the previous stage, witnessed per step externally.",
        "external-irreducibility-witness",
    ),
    Obligation(
        "tower-quotient-domain",
        "The full monic irreducible extension tower makes the quotient an integral domain, certifying the ideal prime.",
        "theorem-application",
    ),
)

TRIANGULAR_DOMAIN_TOWER_CONTRACT = RouteContract(
    route_family="triangular_domain_tower",
    accepted_problem_shape=_SHAPE_LABEL,
    required_hypotheses=(
        "the generators admit a triangular tower order",
        "each non-seed step is monic irreducible over the fraction field of the previous stage",
        "the coefficient characteristic is declared exactly",
    ),
    required_evidence=(
        "triangular_tower scout evidence with a complete tower order",
        "per-step external irreducibility witnesses",
    ),
    produced_obligations=(
        Obligation(
            "execute-domain-tower-certification",
            "Assemble the extension tower and emit the per-step domain certificate obligations.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "a reducible tower step splits the quotient; the decomposition route ladder continues at Route D or later",
        "irreducibility is never assumed: a missing witness leaves the primality obligation open",
    ),
    execution_module="external.domain_tower_certification_executor",
    certificate_obligations=TRIANGULAR_DOMAIN_TOWER_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#11.9",
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.2",
    ),
)


def recognize_triangular_domain_tower(request: PathfinderRequest) -> RecognitionOutcome:
    """Route C / P2: a monic irreducible tower certifies a domain quotient."""

    family = TRIANGULAR_DOMAIN_TOWER_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _require_accepted_shape(request, family),
        _require_declared_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    fingerprint = _tower_fingerprint(request)
    if fingerprint is None:
        return refuse(
            family,
            "evidence_unavailable",
            "No triangular_tower evidence is available for the declared presentation.",
            "triangular_tower scout evidence",
        )
    if fingerprint.get("triangular") is not True:
        return refuse(
            family,
            "not_a_triangular_tower",
            "The generators do not admit an order introducing one fresh variable per step.",
            "complete triangular tower order",
        )
    counts = _tower_counts(fingerprint)
    if counts is None:
        return refuse(
            family,
            "evidence_unavailable",
            "The triangular_tower evidence does not carry usable step records.",
            "introduced_variables",
            "monic_step_count",
        )
    generator_count, non_seed, monic = counts

    steps = (
        RouteStep(
            "order-tower",
            "order_generators_by_tower",
            ("target_ideal",),
            ("ordered_tower_generators",),
            freeze_mapping(
                {
                    "tower_order": fingerprint.get("tower_order", ()),
                    "introduced_variables": fingerprint.get("introduced_variables", ()),
                }
            ),
        ),
        RouteStep(
            "assemble-extension-tower",
            "assemble_fraction_field_extension_tower",
            ("ordered_tower_generators",),
            ("extension_tower",),
            freeze_mapping(
                {
                    "non_seed_step_count": non_seed,
                    "natively_monic_step_count": monic,
                }
            ),
        ),
        RouteStep(
            "emit-domain-obligations",
            "emit_domain_tower_certificate_obligations",
            ("extension_tower",),
            ("host_domain_tower_obligations",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=TRIANGULAR_DOMAIN_TOWER_CONTRACT,
        steps=steps,
        data_dependencies=("target_ideal",),
        required_intermediate_objects=("ordered_tower_generators", "extension_tower"),
        completion_condition="The external executor emits per-step monic-irreducibility obligations for the full tower.",
        burden_vector=BurdenVector(
            invariant_level=2,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=generator_count,
            scout_operation_count=1,
            expression_depth=0,
        ),
        structural_preference_rank=1,
    )


# ---------------------------------------------------------------------------
# linear_inverse_ring_map — prime certificate grade P1


LINEAR_INVERSE_RING_MAP_CERTIFICATES = (
    Obligation(
        "ring-map-isomorphism",
        "The constructed ring map and its inverse compose to the identity in both directions.",
        "explicit-ring-map",
    ),
    Obligation(
        "image-ideal-equality",
        "The image of the ideal under the isomorphism equals the declared target presentation.",
        "exact-ideal-equality",
    ),
)

LINEAR_INVERSE_RING_MAP_CONTRACT = RouteContract(
    route_family="linear_inverse_ring_map",
    accepted_problem_shape=_SHAPE_LABEL,
    required_hypotheses=(
        "at least one generator is linear in an eliminable fresh variable",
        "that linear generator has a unit leading coefficient in the eliminated variable",
        "the coefficient characteristic is declared exactly",
    ),
    required_evidence=("fresh_variable_monic scout evidence restricted to degree-1 steps",),
    produced_obligations=(
        Obligation(
            "execute-linear-inverse-ring-map",
            "Solve the linear generators, construct the inverse ring map, and emit the isomorphic presentation.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "a non-unit leading coefficient blocks the explicit solve over the declared coefficient ring",
        "higher-degree fresh variables belong to the substitution or domain-tower routes",
    ),
    execution_module="external.linear_inverse_ring_map_executor",
    certificate_obligations=LINEAR_INVERSE_RING_MAP_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#11.9",
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.2",
    ),
)


def recognize_linear_inverse_ring_map(request: PathfinderRequest) -> RecognitionOutcome:
    """P1: explicit linear elimination and inverse ring maps (v1.3 §11.9)."""

    family = LINEAR_INVERSE_RING_MAP_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _require_accepted_shape(request, family),
        _require_declared_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    fingerprint = evidence_by_family(request, "fresh_variable_monic")
    problem = lower_request(request)
    if fingerprint is None:
        evidence = fresh_variable_monic_scout(problem, request.analysis_budget)
        if evidence is None:
            return refuse(
                family,
                "evidence_unavailable",
                "No fresh_variable_monic evidence is available for the declared presentation.",
                "fresh_variable_monic scout evidence",
            )
        fingerprint = dict(evidence.structural_fingerprint)

    ideal = problem.ideal("target")
    if problem.ring is None or ideal is None:
        return refuse(
            family,
            "missing_ideal_declaration",
            "The request does not declare the ring and target ideal presentation needed for the degree-1 restriction.",
            "mathematical_context.ring",
            "mathematical_context.ideals.target",
        )
    try:
        shadows: tuple[PolynomialShadow, ...] = tuple(
            shadow_polynomial(
                generator,
                problem.ring.variables,
                max_nodes=request.analysis_budget.max_expression_nodes,
            )
            for generator in ideal.generators
        )
    except ExpressionShadowUnavailable:
        return refuse(
            family,
            "evidence_unavailable",
            "The generator shadows are unavailable within the declared analysis budget.",
            "bounded polynomial shadow",
        )

    fresh_variables = fingerprint.get("fresh_variables")
    sequence_order = fingerprint.get("sequence_order")
    if not isinstance(fresh_variables, tuple) or not isinstance(sequence_order, tuple):
        return refuse(
            family,
            "evidence_unavailable",
            "The fresh_variable_monic evidence does not carry usable step records.",
            "fresh_variables",
            "sequence_order",
        )
    domain = problem.ring.coefficient_domain
    field_coefficients = domain in _FIELD_DOMAINS or domain.startswith("GF(")

    linear_variables: list[str] = []
    linear_positions: list[int] = []
    for position, variable in zip(sequence_order, fresh_variables):
        if not isinstance(position, int) or isinstance(position, bool):
            continue
        if not isinstance(variable, str) or variable not in problem.ring.variables:
            continue
        if not 0 <= position < len(shadows):
            continue
        shadow = shadows[position]
        if shadow.degree_in(variable) != 1:
            continue
        if shadow.is_monic_in(variable) or (field_coefficients and shadow.has_unit_leading_in(variable)):
            linear_variables.append(variable)
            linear_positions.append(position)
    if not linear_variables:
        return refuse(
            family,
            "no_linear_eliminable_generator",
            "No generator is linear with unit leading coefficient in an eliminable fresh variable.",
            "a degree-1 fresh-variable generator with unit leading coefficient",
        )

    steps = (
        RouteStep(
            "solve-linear",
            "solve_linear_generators",
            ("target_ideal",),
            ("solved_linear_relations",),
            freeze_mapping(
                {
                    "eliminable_variables": tuple(linear_variables),
                    "generator_positions": tuple(linear_positions),
                }
            ),
        ),
        RouteStep(
            "construct-inverse",
            "construct_inverse_ring_map",
            ("solved_linear_relations",),
            ("inverse_ring_map",),
        ),
        RouteStep(
            "emit-isomorphic",
            "emit_isomorphic_presentation",
            ("inverse_ring_map", "target_ideal"),
            ("host_isomorphic_presentation",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=LINEAR_INVERSE_RING_MAP_CONTRACT,
        steps=steps,
        data_dependencies=("target_ideal",),
        required_intermediate_objects=("solved_linear_relations", "inverse_ring_map"),
        completion_condition="The external executor emits the isomorphic presentation and the explicit ring-map pair.",
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=len(linear_variables),
            scout_operation_count=1,
            expression_depth=0,
        ),
        structural_preference_rank=1,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="direct_substitution",
        contract=DIRECT_SUBSTITUTION_CONTRACT,
        recognizer=recognize_direct_substitution,
        native_scouts=(triangular_tower_scout,),
        wrapper_capabilities=("forward_substitution",),
    ),
    RouteProvider(
        route_family="triangular_domain_tower",
        contract=TRIANGULAR_DOMAIN_TOWER_CONTRACT,
        recognizer=recognize_triangular_domain_tower,
        native_scouts=(triangular_tower_scout,),
        wrapper_capabilities=("fraction_field_tower", "irreducibility_witness_ledger"),
    ),
    RouteProvider(
        route_family="linear_inverse_ring_map",
        contract=LINEAR_INVERSE_RING_MAP_CONTRACT,
        recognizer=recognize_linear_inverse_ring_map,
        native_scouts=(fresh_variable_monic_scout,),
        wrapper_capabilities=("linear_solve", "explicit_ring_map"),
    ),
)
