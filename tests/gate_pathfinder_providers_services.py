"""Gate the finite-extension, modular-Groebner and realization-poset providers."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.pathfinder import Obligation, PathfinderRequest
from cella.pathfinder.recognize.finite_extension import (
    PROVIDERS as FINITE_EXTENSION_PROVIDERS,
    recognize_factorization_shaped,
    recognize_finite_algebra_multiplication_matrix,
)
from cella.pathfinder.recognize.modular_groebner import (
    PROVIDERS as MODULAR_GROEBNER_PROVIDERS,
    recognize_modular_groebner_reconstruction,
)
from cella.pathfinder.recognize.realization import (
    PROVIDERS as REALIZATION_PROVIDERS,
    recognize_lazy_realization_poset,
)
from cella.pathfinder.serialize import canonical_json_bytes


FAILS: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


def build_request(
    request_id: str,
    family: str,
    base_context: dict[str, object],
    overrides: dict[str, object],
) -> PathfinderRequest:
    context = dict(base_context)
    context.update(overrides)
    return PathfinderRequest.create(
        request_id=request_id,
        target_obligation=Obligation(
            "route-target",
            "Return the selected computational route for the declared task.",
            "route-instructions",
        ),
        external_binding={"host_session": "m2:resident"},
        mathematical_context=context,
        available_route_families=(family, "generic_elimination"),
    )


def check_candidate_discipline(label: str, route: object) -> None:
    serialized = canonical_json_bytes(route)
    check(f"{label}: serialization is byte deterministic", serialized == canonical_json_bytes(route))
    check(f"{label}: no wall-clock prediction", b"predicted_duration" not in serialized)
    check(f"{label}: no final mathematical result field", b"final_result" not in serialized)


check(
    "providers tuples expose exactly the four assigned families",
    tuple(p.route_family for p in FINITE_EXTENSION_PROVIDERS) == ("finite_algebra_multiplication_matrix", "factorization_shaped")
    and tuple(p.route_family for p in MODULAR_GROEBNER_PROVIDERS) == ("modular_groebner_reconstruction",)
    and tuple(p.route_family for p in REALIZATION_PROVIDERS) == ("lazy_realization_poset",),
)


# --- finite_algebra_multiplication_matrix -----------------------------------

MULT_CONTEXT: dict[str, object] = {
    "problem_shape": "norm_trace_minimal_polynomial",
    "characteristic": 0,
    "quotient_presentation": {
        "defining_polynomial": "u**2-5",
        "algebra_generators": ("1", "u"),
    },
    "requested_invariant": "minimal_polynomial",
}


def mult_request(**overrides: object) -> PathfinderRequest:
    return build_request(
        "pf-finite-algebra-mult-matrix-v1",
        "finite_algebra_multiplication_matrix",
        MULT_CONTEXT,
        overrides,
    )


outcome = recognize_finite_algebra_multiplication_matrix(mult_request())
check("mult-matrix: positive fixture is admitted", outcome.candidate is not None)
assert outcome.candidate is not None
route = outcome.candidate.route
check(
    "mult-matrix: ordered operations match the contract route",
    tuple(step.operation for step in route.ordered_steps)
    == (
        "construct_multiplication_matrices",
        "derive_norm_trace_or_minimal_polynomial",
        "emit_invariant_presentation",
    ),
)
check(
    "mult-matrix: the requested invariant parametrizes the derivation step",
    dict(route.ordered_steps[1].parameters).get("requested_invariant") == "minimal_polynomial",
)
check(
    "mult-matrix: certificate obligations are present",
    {o.obligation_id for o in route.certificate_obligations}
    >= {"multiplication-matrix-identity", "resultant-charpoly-identity", "degree-witness"},
)
check(
    "mult-matrix: the second accepted shape is also admitted",
    recognize_finite_algebra_multiplication_matrix(
        mult_request(problem_shape="finite_algebra_operation")
    ).candidate
    is not None,
)
check_candidate_discipline("mult-matrix", route)

for label, changed, code in (
    (
        "mult-matrix: missing quotient presentation is refused",
        {"quotient_presentation": None},
        "missing_quotient_presentation",
    ),
    (
        "mult-matrix: wrong shape is refused",
        {"problem_shape": "factorization"},
        "shape_mismatch",
    ),
    (
        "mult-matrix: undeclared characteristic is refused",
        {"characteristic": None},
        "missing_characteristic",
    ),
    (
        "mult-matrix: unsupported invariant is not admitted",
        {"requested_invariant": "discriminant"},
        "unsupported_invariant",
    ),
):
    refused = recognize_finite_algebra_multiplication_matrix(mult_request(**changed))
    check(label, refused.refusal is not None and refused.refusal.code == code)


# --- factorization_shaped ----------------------------------------------------

FACTOR_CONTEXT: dict[str, object] = {
    "problem_shape": "factorization",
    "characteristic": 0,
    "factor_target": "quintic",
    "ring": {"variables": ("x",)},
    "ideals": {"quintic": ("x**5-4*x-2",)},
}


def factor_request(**overrides: object) -> PathfinderRequest:
    return build_request(
        "pf-factorization-shaped-v1",
        "factorization_shaped",
        FACTOR_CONTEXT,
        overrides,
    )


outcome = recognize_factorization_shaped(factor_request())
check("factorization: positive fixture is admitted", outcome.candidate is not None)
assert outcome.candidate is not None
route = outcome.candidate.route
check(
    "factorization: ordered operations match the contract route",
    tuple(step.operation for step in route.ordered_steps)
    == (
        "modular_factor_pattern_scout",
        "assemble_factor_candidates",
        "emit_factor_candidates_with_irreducibility_obligations",
    ),
)
check(
    "factorization: the pattern scout is marked non-verdict-bearing",
    dict(route.ordered_steps[0].parameters).get("verdict_bearing") is False,
)
check(
    "factorization: certificate obligations are present",
    {o.obligation_id for o in route.certificate_obligations}
    >= {
        "factor-product-identity",
        "squarefree-multiplicity-witness",
        "pairwise-coprimality",
        "per-factor-irreducibility",
    },
)
check(
    "factorization: burden and preference follow the ticket",
    outcome.candidate.burden_vector.invariant_level == 2
    and outcome.candidate.structural_preference_rank == 2,
)
check_candidate_discipline("factorization", route)

for label, changed, code in (
    (
        "factorization: missing factor target is refused",
        {"factor_target": None},
        "missing_factor_target",
    ),
    (
        "factorization: wrong shape is refused",
        {"problem_shape": "groebner_basis"},
        "shape_mismatch",
    ),
    (
        "factorization: ungatherable degree evidence is refused",
        {"ideals": None},
        "evidence_unavailable",
    ),
    (
        "factorization: undeclared characteristic is refused",
        {"characteristic": None},
        "missing_characteristic",
    ),
):
    refused = recognize_factorization_shaped(factor_request(**changed))
    check(label, refused.refusal is not None and refused.refusal.code == code)


# --- modular_groebner_reconstruction ------------------------------------------

GROEBNER_CONTEXT: dict[str, object] = {
    "problem_shape": "groebner_basis",
    "characteristic": 0,
    "host_supports_modular": True,
    "ring": {"variables": ("x", "y")},
    "ideals": {"target": ("x**2+y**2-1", "x*y-1")},
}


def groebner_request(**overrides: object) -> PathfinderRequest:
    return build_request(
        "pf-modular-groebner-v1",
        "modular_groebner_reconstruction",
        GROEBNER_CONTEXT,
        overrides,
    )


outcome = recognize_modular_groebner_reconstruction(groebner_request())
check("modular groebner: positive fixture is admitted", outcome.candidate is not None)
assert outcome.candidate is not None
route = outcome.candidate.route
check(
    "modular groebner: ordered operations mirror the section 10.1 flow",
    tuple(step.operation for step in route.ordered_steps)
    == (
        "clear_denominators_and_record_scaling",
        "select_admissible_primes",
        "run_parallel_modular_closure_scouts",
        "cluster_by_leading_ideal",
        "crt_accumulate_and_rationally_reconstruct",
        "emit_candidate_basis_with_certificate_obligations",
    ),
)
check(
    "modular groebner: prime selection declares its exclusions",
    dict(route.ordered_steps[1].parameters).get("exclusions")
    == (
        "primes_dividing_input_denominators",
        "primes_dividing_generator_contents",
        "primes_on_declared_bad_loci",
    ),
)
check(
    "modular groebner: modular scouts are marked non-verdict-bearing",
    dict(route.ordered_steps[2].parameters).get("verdict_bearing") is False,
)
check(
    "modular groebner: full certificate obligations are present",
    {o.obligation_id for o in route.certificate_obligations}
    >= {
        "groebner-containment-forward",
        "groebner-containment-reverse",
        "critical-pair-standard-representations",
        "basis-normalization-fingerprint",
    },
)
check(
    "modular groebner: unlucky primes are branch evidence, not user refusals",
    any("unlucky primes" in branch for branch in route.exceptional_branches),
)
check(
    "modular groebner: burden follows the ticket",
    outcome.candidate.burden_vector.invariant_level == 2
    and outcome.candidate.burden_vector.global_expansion_rank == 1
    and outcome.candidate.burden_vector.elimination_rank == 2
    and outcome.candidate.structural_preference_rank == 2,
)
check_candidate_discipline("modular groebner", route)

for label, changed, code in (
    (
        "modular groebner: nonzero characteristic is not admitted",
        {"characteristic": 7},
        "characteristic_not_zero",
    ),
    (
        "modular groebner: host without modular operations is not admitted",
        {"host_supports_modular": False},
        "host_lacks_modular_operations",
    ),
    (
        "modular groebner: wrong shape is refused",
        {"problem_shape": "realization_poset"},
        "shape_mismatch",
    ),
    (
        "modular groebner: missing target ideal is refused",
        {"ideals": None},
        "missing_target_ideal",
    ),
    (
        "modular groebner: undeclared characteristic is refused",
        {"characteristic": None},
        "missing_characteristic",
    ),
):
    refused = recognize_modular_groebner_reconstruction(groebner_request(**changed))
    check(label, refused.refusal is not None and refused.refusal.code == code)

check(
    "modular groebner: ideal-membership shape is also admitted",
    recognize_modular_groebner_reconstruction(
        groebner_request(problem_shape="ideal_membership")
    ).candidate
    is not None,
)


# --- lazy_realization_poset ----------------------------------------------------

POSET_CONTEXT: dict[str, object] = {
    "problem_shape": "realization_poset",
    "characteristic": 0,
    "realization_poset": {
        "requested_nodes": ("IR", "IZ", "Ceven+IZ", "IR+Ceven+IZ"),
    },
    "ideals": {
        "IX": ("w1**2-u-N1**2", "w1+w2+w3+w4-4*M"),
        "IZ": ("4*M-w1-w2-w3-w4", "N1**2+u-w1**2"),
    },
    "strata": (
        {"name": "generic_open", "condition": "2*M*P != 0", "status": "assumed"},
        {"name": "compactified_boundary", "condition": "M = 0", "status": "excluded"},
    ),
}


def poset_request(**overrides: object) -> PathfinderRequest:
    return build_request(
        "pf-lazy-realization-poset-v1",
        "lazy_realization_poset",
        POSET_CONTEXT,
        overrides,
    )


outcome = recognize_lazy_realization_poset(poset_request())
check("realization poset: positive fixture is admitted", outcome.candidate is not None)
assert outcome.candidate is not None
route = outcome.candidate.route
check(
    "realization poset: ordered operations match the lazy node/edge route",
    tuple(step.operation for step in route.ordered_steps)
    == (
        "order_requested_nodes_by_dependency",
        "derive_node_presentations",
        "attach_boundary_and_multiplicity_records",
        "emit_poset_node_and_edge_route",
    ),
)
check(
    "realization poset: presentations are lazy and content-addressed",
    dict(route.ordered_steps[1].parameters).get("evaluation") == "lazy"
    and dict(route.ordered_steps[1].parameters).get("saturation_policy")
    == "computed_once_content_addressed",
)
check(
    "realization poset: doubled nodes retain multiplicity",
    dict(route.ordered_steps[2].parameters).get("doubled_node_policy")
    == "record_multiplicity_never_reduce",
)
check(
    "realization poset: certificate obligations are present",
    {o.obligation_id for o in route.certificate_obligations}
    >= {
        "node-invariants-after-declared-saturation",
        "edge-witnesses",
        "multiplicity-retention-on-doubled-nodes",
        "boundary-task-retention",
    },
)
check(
    "realization poset: burden follows the ticket",
    outcome.candidate.burden_vector.invariant_level == 2
    and outcome.candidate.burden_vector.elimination_rank == 1
    and outcome.candidate.structural_preference_rank == 2,
)
check_candidate_discipline("realization poset", route)

for label, changed, code in (
    (
        "realization poset: empty requested nodes are not admitted",
        {"realization_poset": {"requested_nodes": ()}},
        "no_requested_nodes",
    ),
    (
        "realization poset: missing poset declaration is refused",
        {"realization_poset": None},
        "no_requested_nodes",
    ),
    (
        "realization poset: missing incidence presentation is refused",
        {"ideals": None},
        "missing_incidence_presentation",
    ),
    (
        "realization poset: wrong shape is refused",
        {"problem_shape": "groebner_basis"},
        "shape_mismatch",
    ),
    (
        "realization poset: node on an excluded stratum is refused",
        {
            "realization_poset": {
                "requested_nodes": ("IR", "compactified_boundary"),
            }
        },
        "poset_node_outside_declared_open",
    ),
    (
        "realization poset: characteristic two is refused",
        {"characteristic": 2},
        "characteristic_two",
    ),
):
    refused = recognize_lazy_realization_poset(poset_request(**changed))
    check(label, refused.refusal is not None and refused.refusal.code == code)


print()
if FAILS:
    print(f"GATE PATHFINDER PROVIDERS SERVICES: OPEN ({len(FAILS)} failing)")
    raise SystemExit(1)
print("GATE PATHFINDER PROVIDERS SERVICES: CLOSED")
