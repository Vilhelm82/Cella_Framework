"""Finite-algebra and factorization route providers (v1.3 Module A).

Two structure-first route families extracted from CELLA_ARCHITECTURE_v1.3.md
section 13: multiplication-matrix invariant derivation over a declared finite
quotient algebra (section 13.2/13.3) and factorization-shaped candidate
discovery with external irreducibility obligations (section 13.1, route ladder
Route E).  Both emit instructions only; execution and certificates are
external.
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
from ..scout.algebra import degree_balance_scout


def _is_nonempty_pairs(value: FrozenValue | None) -> bool:
    """A pairs tuple is opaque structured data; it must merely be nonempty."""

    return (
        isinstance(value, tuple)
        and bool(value)
        and all(
            isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str)
            for item in value
        )
    )


def _require_declared_characteristic(
    request: PathfinderRequest, route_family: str
) -> RecognitionOutcome | None:
    characteristic = lookup(request.mathematical_context, "characteristic")
    if not isinstance(characteristic, int) or isinstance(characteristic, bool):
        return refuse(
            route_family,
            "missing_characteristic",
            "The coefficient characteristic must be declared exactly.",
            "integer characteristic",
        )
    return None


def _require_shape_in(
    request: PathfinderRequest, route_family: str, accepted_shapes: tuple[str, ...]
) -> RecognitionOutcome | None:
    shape = lookup(request.mathematical_context, "problem_shape")
    if shape not in accepted_shapes:
        return refuse(
            route_family,
            "shape_mismatch",
            "The task does not declare an accepted problem shape for this family.",
            *accepted_shapes,
        )
    return None


# ---------------------------------------------------------------------------
# Family: finite_algebra_multiplication_matrix (v1.3 section 13.2, 13.3)
# ---------------------------------------------------------------------------

MULTIPLICATION_MATRIX_SHAPES = (
    "norm_trace_minimal_polynomial",
    "finite_algebra_operation",
)

SUPPORTED_INVARIANTS = ("norm", "trace", "minimal_polynomial")

MULTIPLICATION_MATRIX_CERTIFICATES = (
    Obligation(
        "multiplication-matrix-identity",
        "Each constructed matrix M_a acts on the declared quotient basis exactly as multiplication by a.",
        "exact-matrix-identity",
    ),
    Obligation(
        "resultant-charpoly-identity",
        "The emitted norm/trace/minimal polynomial satisfies its defining characteristic-polynomial or resultant identity, not merely a printed value.",
        "exact-polynomial-identity",
    ),
    Obligation(
        "degree-witness",
        "The multiplication-matrix dimension equals the declared quotient-algebra degree.",
        "exact-rank-count",
    ),
)

MULTIPLICATION_MATRIX_CONTRACT = RouteContract(
    route_family="finite_algebra_multiplication_matrix",
    accepted_problem_shape="norm_trace_minimal_polynomial|finite_algebra_operation",
    required_hypotheses=(
        "the quotient algebra is presented by an explicit finite presentation",
        "the coefficient characteristic is declared exactly",
        "the requested invariant is norm, trace, or minimal_polynomial",
        "trace/norm separability conclusions require an explicit separability hypothesis",
    ),
    required_evidence=("explicit quotient presentation", "declared requested invariant"),
    produced_obligations=(
        Obligation(
            "execute-multiplication-matrix-derivation",
            "Construct the multiplication matrices and emit the requested invariant presentation in host bindings.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "a non-separable algebra requires an explicit separability hypothesis before norm/trace conclusions",
        "a zero divisor discovered during matrix construction certifies the algebra is not a field and is recorded as a decomposition branch",
    ),
    execution_module="external.finite_algebra_executor",
    certificate_obligations=MULTIPLICATION_MATRIX_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#13.2",
        "CELLA_ARCHITECTURE_v1.3.md#13.3",
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md",
    ),
)


def recognize_finite_algebra_multiplication_matrix(
    request: PathfinderRequest,
) -> RecognitionOutcome:
    """Admit the multiplication-matrix invariant route conservatively."""

    family = MULTIPLICATION_MATRIX_CONTRACT.route_family
    outcome = (
        family_enabled(request, family)
        or _require_shape_in(request, family, MULTIPLICATION_MATRIX_SHAPES)
        or _require_declared_characteristic(request, family)
    )
    if outcome is not None:
        return outcome

    presentation = lookup(request.mathematical_context, "quotient_presentation")
    if not _is_nonempty_pairs(presentation):
        return refuse(
            family,
            "missing_quotient_presentation",
            "No explicit quotient-algebra presentation was declared.",
            "quotient_presentation with defining data (defining_polynomial/algebra_generators)",
        )

    requested_invariant = lookup(request.mathematical_context, "requested_invariant")
    if requested_invariant not in SUPPORTED_INVARIANTS:
        return refuse(
            family,
            "unsupported_invariant",
            "The requested invariant is not one this multiplication-matrix contract derives.",
            *SUPPORTED_INVARIANTS,
        )

    steps = (
        RouteStep(
            "construct-matrices",
            "construct_multiplication_matrices",
            ("quotient_presentation",),
            ("multiplication_matrices",),
        ),
        RouteStep(
            "derive-invariant",
            "derive_norm_trace_or_minimal_polynomial",
            ("multiplication_matrices",),
            ("derived_invariant",),
            freeze_mapping({"requested_invariant": requested_invariant}),
        ),
        RouteStep(
            "emit-invariant",
            "emit_invariant_presentation",
            ("derived_invariant",),
            ("host_invariant_presentation",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=MULTIPLICATION_MATRIX_CONTRACT,
        steps=steps,
        data_dependencies=("quotient_presentation", "requested_invariant"),
        required_intermediate_objects=("multiplication_matrices", "derived_invariant"),
        completion_condition="The external executor emits the requested invariant presentation in host bindings.",
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=3,
            scout_operation_count=0,
            expression_depth=2,
        ),
        structural_preference_rank=1,
    )


# ---------------------------------------------------------------------------
# Family: factorization_shaped (v1.3 section 13.1, route ladder Route E)
# ---------------------------------------------------------------------------

FACTORIZATION_SHAPES = ("factorization", "component_discovery")

FACTORIZATION_CERTIFICATES = (
    Obligation(
        "factor-product-identity",
        "The product of the emitted factors with multiplicities equals the target exactly, including content.",
        "exact-polynomial-identity",
    ),
    Obligation(
        "squarefree-multiplicity-witness",
        "The declared multiplicities agree with an exact squarefree decomposition of the target.",
        "exact-squarefree-decomposition",
    ),
    Obligation(
        "pairwise-coprimality",
        "The distinct factor candidates are pairwise coprime over the declared field.",
        "exact-gcd-witness",
    ),
    Obligation(
        "per-factor-irreducibility",
        "Each emitted factor carries a separate irreducibility witness over the declared field.",
        "exact-irreducibility-witness",
    ),
)

FACTORIZATION_CONTRACT = RouteContract(
    route_family="factorization_shaped",
    accepted_problem_shape="factorization|component_discovery",
    required_hypotheses=(
        "the coefficient characteristic is declared exactly",
        "the factor target is a declared bound polynomial/ideal generator",
        "modular factor patterns are scouting evidence only (Law 2: candidates never truth)",
        "irreducibility witnesses are separate obligations, never inferred from pattern agreement",
    ),
    required_evidence=("declared factor target", "exact degree bookkeeping for the target"),
    produced_obligations=(
        Obligation(
            "execute-factor-candidate-discovery",
            "Assemble factor candidates and emit them with per-factor irreducibility obligations in host bindings.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "an inseparable target in positive characteristic requires p-th-power extraction before squarefree decomposition",
        "modular pattern disagreement or recombination failure retries with a different scout; candidates are never emitted as truth",
    ),
    execution_module="external.factorization_executor",
    certificate_obligations=FACTORIZATION_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#13.1",
        "CELLA_ARCHITECTURE_v1.3.md#11.9",
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md",
    ),
)


def recognize_factorization_shaped(request: PathfinderRequest) -> RecognitionOutcome:
    """Admit factor-candidate discovery with external irreducibility burden."""

    family = FACTORIZATION_CONTRACT.route_family
    outcome = (
        family_enabled(request, family)
        or _require_shape_in(request, family, FACTORIZATION_SHAPES)
        or _require_declared_characteristic(request, family)
    )
    if outcome is not None:
        return outcome

    factor_target = lookup(request.mathematical_context, "factor_target")
    if not isinstance(factor_target, str) or not factor_target.strip():
        return refuse(
            family,
            "missing_factor_target",
            "No bound polynomial or ideal generator was named as the factor target.",
            "factor_target naming a declared generator",
        )

    evidence = evidence_by_family(request, "degree_balance")
    if evidence is None:
        problem = lower_request(request)
        scouted = degree_balance_scout(
            problem, request.analysis_budget, ideal_name=factor_target
        )
        evidence = dict(scouted.structural_fingerprint) if scouted is not None else None
    if evidence is None:
        return refuse(
            family,
            "evidence_unavailable",
            "Exact degree bookkeeping for the factor target could not be gathered.",
            "declared ring and factor-target generators admitting a bounded shadow",
        )

    steps = (
        RouteStep(
            "scout-factor-patterns",
            "modular_factor_pattern_scout",
            ("factor_target",),
            ("modular_factor_patterns",),
            freeze_mapping({"role": "scout_only", "verdict_bearing": False}),
        ),
        RouteStep(
            "assemble-candidates",
            "assemble_factor_candidates",
            ("modular_factor_patterns", "factor_target"),
            ("factor_candidates",),
        ),
        RouteStep(
            "emit-candidates",
            "emit_factor_candidates_with_irreducibility_obligations",
            ("factor_candidates",),
            ("host_factor_candidates",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=FACTORIZATION_CONTRACT,
        steps=steps,
        data_dependencies=("factor_target",),
        required_intermediate_objects=("modular_factor_patterns", "factor_candidates"),
        completion_condition="The external executor emits factor candidates with attached irreducibility obligations in host bindings.",
        burden_vector=BurdenVector(
            invariant_level=2,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=3,
            scout_operation_count=1,
            expression_depth=2,
        ),
        structural_preference_rank=2,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="finite_algebra_multiplication_matrix",
        contract=MULTIPLICATION_MATRIX_CONTRACT,
        recognizer=recognize_finite_algebra_multiplication_matrix,
        native_scouts=(),
        wrapper_capabilities=("quotient_algebra_presentation", "exact_linear_algebra"),
    ),
    RouteProvider(
        route_family="factorization_shaped",
        contract=FACTORIZATION_CONTRACT,
        recognizer=recognize_factorization_shaped,
        native_scouts=(degree_balance_scout,),
        wrapper_capabilities=("modular_factor_patterns", "exact_polynomial_arithmetic"),
    ),
)
