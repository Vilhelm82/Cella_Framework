"""Modular Groebner reconstruction route provider (v1.3 section 10, Route F).

The modular flow is a QQ technique: modular closure scouts, leading-ideal
clustering, CRT accumulation and rational reconstruction produce a candidate
basis only.  Cross-prime agreement is reconnaissance, not certification; the
full Groebner certificate (v1.3 section 10.3) is discharged externally by
canonical exact replay.  Pathfinder emits the instructions and obligations,
never the basis.
"""

from __future__ import annotations

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.problem import lower_request
from ..ir.values import freeze_mapping
from ..plan.admissibility import family_enabled, lookup, refuse
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider


MODULAR_GROEBNER_SHAPES = ("groebner_basis", "ideal_membership", "ideal_equality")

MODULAR_GROEBNER_CERTIFICATES = (
    Obligation(
        "groebner-containment-forward",
        "An explicit multiplier matrix U witnesses G = U*F, proving <G> is contained in <F>.",
        "exact-multiplier-matrix",
    ),
    Obligation(
        "groebner-containment-reverse",
        "An explicit multiplier matrix V witnesses F = V*G, proving <F> is contained in <G>.",
        "exact-multiplier-matrix",
    ),
    Obligation(
        "critical-pair-standard-representations",
        "Every required critical pair S(g_i,g_j) carries a standard representation with the strict leading-monomial bound.",
        "exact-standard-representation",
    ),
    Obligation(
        "basis-normalization-fingerprint",
        "Canonical replay verifies G is monic and interreduced and that the ring and monomial-order fingerprints match the claim.",
        "exact-canonical-replay",
    ),
)

MODULAR_GROEBNER_CONTRACT = RouteContract(
    route_family="modular_groebner_reconstruction",
    accepted_problem_shape="groebner_basis|ideal_membership|ideal_equality",
    required_hypotheses=(
        "characteristic 0 (the modular reconstruction lane is a QQ technique)",
        "the target ideal is declared with explicit generators",
        "the host exposes modular reduction, GF(p) closure scouts, CRT and rational reconstruction",
        "cross-prime agreement is reconnaissance, not certification",
        "the declared monomial order is admissible",
    ),
    required_evidence=("declared target ideal generators", "host modular capability declaration"),
    produced_obligations=(
        Obligation(
            "execute-modular-reconstruction",
            "Run the modular scout flow and emit a candidate basis with its full certificate obligations in host bindings.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "unlucky primes are discarded with recorded prime-event evidence, never surfaced as user refusals",
        "rational-reconstruction ambiguity retries with additional admissible primes",
        "a failed candidate basis is classified and retried; it is never emitted as truth",
    ),
    execution_module="external.modular_groebner_executor",
    certificate_obligations=MODULAR_GROEBNER_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#10.1",
        "CELLA_ARCHITECTURE_v1.3.md#10.2",
        "CELLA_ARCHITECTURE_v1.3.md#10.3",
        "CELLA_ARCHITECTURE_v1.3.md#11.9",
    ),
)

PRIME_EXCLUSIONS = (
    "primes_dividing_input_denominators",
    "primes_dividing_generator_contents",
    "primes_on_declared_bad_loci",
)


def recognize_modular_groebner_reconstruction(
    request: PathfinderRequest,
) -> RecognitionOutcome:
    """Admit the modular reconstruction flow only where it is a theorem-true lane."""

    family = MODULAR_GROEBNER_CONTRACT.route_family
    outcome = family_enabled(request, family)
    if outcome is not None:
        return outcome

    shape = lookup(request.mathematical_context, "problem_shape")
    if shape not in MODULAR_GROEBNER_SHAPES:
        return refuse(
            family,
            "shape_mismatch",
            "The task does not declare a Groebner-basis-shaped problem.",
            *MODULAR_GROEBNER_SHAPES,
        )

    characteristic = lookup(request.mathematical_context, "characteristic")
    if not isinstance(characteristic, int) or isinstance(characteristic, bool):
        return refuse(
            family,
            "missing_characteristic",
            "The coefficient characteristic must be declared exactly.",
            "integer characteristic",
        )
    if characteristic != 0:
        return refuse(
            family,
            "characteristic_not_zero",
            "Modular reconstruction lifts GF(p) images back to QQ; in nonzero characteristic there is no reconstruction target.",
            "characteristic = 0",
        )

    if lookup(request.mathematical_context, "host_supports_modular") is not True:
        return refuse(
            family,
            "host_lacks_modular_operations",
            "The host did not advertise the modular operations this route instructs it to run.",
            "host_supports_modular = True",
        )

    problem = lower_request(request)
    if problem.ideal("target") is None:
        return refuse(
            family,
            "missing_target_ideal",
            "No target ideal with explicit generators was declared.",
            "ideals.target with generator strings",
        )

    steps = (
        RouteStep(
            "clear-denominators",
            "clear_denominators_and_record_scaling",
            ("target_ideal",),
            ("primitive_integer_generators", "scaling_record"),
        ),
        RouteStep(
            "select-primes",
            "select_admissible_primes",
            ("primitive_integer_generators",),
            ("admissible_primes",),
            freeze_mapping({"exclusions": PRIME_EXCLUSIONS}),
        ),
        RouteStep(
            "modular-scouts",
            "run_parallel_modular_closure_scouts",
            ("primitive_integer_generators", "admissible_primes"),
            ("modular_bases",),
            freeze_mapping({"role": "scout_only", "verdict_bearing": False}),
        ),
        RouteStep(
            "cluster-leading-ideals",
            "cluster_by_leading_ideal",
            ("modular_bases",),
            ("modular_clusters",),
        ),
        RouteStep(
            "crt-reconstruct",
            "crt_accumulate_and_rationally_reconstruct",
            ("modular_clusters", "scaling_record"),
            ("rational_candidate_basis",),
        ),
        RouteStep(
            "emit-candidate-basis",
            "emit_candidate_basis_with_certificate_obligations",
            ("rational_candidate_basis",),
            ("host_candidate_basis",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=MODULAR_GROEBNER_CONTRACT,
        steps=steps,
        data_dependencies=("target_ideal", "declared_monomial_order"),
        required_intermediate_objects=(
            "primitive_integer_generators",
            "scaling_record",
            "admissible_primes",
            "modular_bases",
            "modular_clusters",
            "rational_candidate_basis",
        ),
        completion_condition="The external executor emits the candidate basis with its full Groebner certificate obligations in host bindings.",
        burden_vector=BurdenVector(
            invariant_level=2,
            global_expansion_rank=1,
            elimination_rank=2,
            exact_operation_count=6,
            scout_operation_count=0,
            expression_depth=2,
        ),
        structural_preference_rank=2,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="modular_groebner_reconstruction",
        contract=MODULAR_GROEBNER_CONTRACT,
        recognizer=recognize_modular_groebner_reconstruction,
        native_scouts=(),
        wrapper_capabilities=(
            "modular_reduction",
            "gfp_groebner_scouts",
            "crt_rational_reconstruction",
        ),
    ),
)
