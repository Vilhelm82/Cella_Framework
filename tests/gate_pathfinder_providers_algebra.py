"""Gate the corpus-derived algebra route providers.

Covers, for every registered family: a positive fixture with the expected
ordered operations, a missing-hypothesis refusal, a wrong-shape refusal, a
mutation fixture that must not be admitted, and the presence of certificate
obligations on the admitted route.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.pathfinder import Obligation, PathfinderRequest
from cella.pathfinder.recognize.complete_intersection import (
    recognize_degree_balance_closure,
    recognize_regular_sequence_complete_intersection,
)
from cella.pathfinder.recognize.complete_intersection import PROVIDERS as CI_PROVIDERS
from cella.pathfinder.recognize.elimination import (
    recognize_generic_elimination,
    recognize_localization_boundary_split,
    recognize_ordinary_host_computation,
)
from cella.pathfinder.recognize.elimination import PROVIDERS as ELIMINATION_PROVIDERS
from cella.pathfinder.recognize.rewrite import recognize_symbolic_collapse_rewrite
from cella.pathfinder.recognize.rewrite import PROVIDERS as REWRITE_PROVIDERS
from cella.pathfinder.recognize.triangular import (
    recognize_direct_substitution,
    recognize_linear_inverse_ring_map,
    recognize_triangular_domain_tower,
)
from cella.pathfinder.recognize.triangular import PROVIDERS as TRIANGULAR_PROVIDERS
from cella.pathfinder.serialize import canonical_json_bytes


FAILS: list[str] = []

ALL_FAMILIES = (
    "symbolic_collapse_rewrite",
    "direct_substitution",
    "triangular_domain_tower",
    "linear_inverse_ring_map",
    "regular_sequence_complete_intersection",
    "degree_balance_closure",
    "generic_elimination",
    "localization_boundary_split",
    "ordinary_host_computation",
)


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


def make_request(context: dict, binding: dict | None = None) -> PathfinderRequest:
    return PathfinderRequest.create(
        request_id="providers-algebra-gate-v1",
        target_obligation=Obligation(
            "target-task",
            "Discharge the declared task through an admissible route.",
            "exact",
        ),
        external_binding=binding if binding is not None else {"target_ideal": "host:I"},
        mathematical_context=context,
        available_route_families=ALL_FAMILIES,
    )


def ops(outcome) -> tuple[str, ...]:
    assert outcome.candidate is not None
    return tuple(step.operation for step in outcome.candidate.route.ordered_steps)


def refused(outcome, code: str) -> bool:
    return outcome.refusal is not None and outcome.refusal.code == code


def has_obligation(outcome, obligation_id: str) -> bool:
    assert outcome.candidate is not None
    return any(
        obligation.obligation_id == obligation_id
        for obligation in outcome.candidate.route.certificate_obligations
    )


# ---------------------------------------------------------------------------
# symbolic_collapse_rewrite

print("-- symbolic_collapse_rewrite --")

rewrite_positive = recognize_symbolic_collapse_rewrite(
    make_request({"problem_shape": "scalar_expression", "expression": "(a+b)-(a+b)"})
)
check("rewrite: self-cancellation fixture admitted", rewrite_positive.candidate is not None)
check(
    "rewrite: ordered operations",
    rewrite_positive.candidate is not None
    and ops(rewrite_positive)
    == (
        "classify_cancellation_sites",
        "apply_conservative_rewrites",
        "emit_rewritten_expression_in_external_bindings",
    ),
)
check(
    "rewrite: per-site families recorded on the rewrite step",
    rewrite_positive.candidate is not None
    and "site_rewrite_families"
    in dict(rewrite_positive.candidate.route.ordered_steps[1].parameters),
)
check(
    "rewrite: exact-identity certificate obligation present",
    rewrite_positive.candidate is not None
    and has_obligation(rewrite_positive, "rewrite-exact-identity"),
)
check(
    "rewrite: missing expression refused as no_expression",
    refused(
        recognize_symbolic_collapse_rewrite(make_request({"problem_shape": "scalar_expression"})),
        "no_expression",
    ),
)
check(
    "rewrite: wrong shape refused",
    refused(
        recognize_symbolic_collapse_rewrite(
            make_request({"problem_shape": "ideal_projection", "expression": "(a+b)-(a+b)"})
        ),
        "shape_mismatch",
    ),
)
check(
    "rewrite: unresolved cancellation refused mathematically",
    refused(
        recognize_symbolic_collapse_rewrite(
            make_request({"problem_shape": "scalar_expression", "expression": "a - b"})
        ),
        "unsupported_expression_shape",
    ),
)
check(
    "rewrite: no subtraction refused as nothing-to-collapse",
    refused(
        recognize_symbolic_collapse_rewrite(
            make_request({"problem_shape": "scalar_expression", "expression": "a + b"})
        ),
        "no_cancellation_to_collapse",
    ),
)

# ---------------------------------------------------------------------------
# triangular fixtures

print("-- direct_substitution --")

MONIC_TOWER = ("t**2 - 4", "x**2 - t", "y - t*x")
NONMONIC_TOWER = ("t**2 - 4", "2*x**2 - t", "y - t*x")


def tower_context(generators: tuple[str, ...], shape: str = "ideal_decomposition", **extra) -> dict:
    context = {
        "problem_shape": shape,
        "characteristic": 0,
        "ring": {"variables": ("t", "x", "y", "z"), "coefficients": "QQ", "characteristic": 0},
        "ideals": {"target": generators},
    }
    context.update(extra)
    return context


substitution_positive = recognize_direct_substitution(make_request(tower_context(MONIC_TOWER)))
check("substitution: monic tower admitted", substitution_positive.candidate is not None)
check(
    "substitution: ordered operations",
    substitution_positive.candidate is not None
    and ops(substitution_positive)
    == ("order_generators_by_tower", "substitute_forward", "emit_substituted_presentation"),
)
check(
    "substitution: ideal-equality certificate obligation present",
    substitution_positive.candidate is not None
    and has_obligation(substitution_positive, "substitution-ideal-equality"),
)
check(
    "substitution: missing characteristic refused",
    refused(
        recognize_direct_substitution(
            make_request({k: v for k, v in tower_context(MONIC_TOWER).items() if k != "characteristic"})
        ),
        "missing_characteristic",
    ),
)
check(
    "substitution: wrong shape refused",
    refused(
        recognize_direct_substitution(
            make_request(tower_context(MONIC_TOWER, shape="scalar_expression"))
        ),
        "shape_mismatch",
    ),
)
check(
    "substitution: non-monic tower mutation refused",
    refused(
        recognize_direct_substitution(make_request(tower_context(NONMONIC_TOWER))),
        "nonmonic_tower_step",
    ),
)

print("-- triangular_domain_tower --")

domain_tower_positive = recognize_triangular_domain_tower(make_request(tower_context(MONIC_TOWER)))
check("domain tower: triangular tower admitted", domain_tower_positive.candidate is not None)
check(
    "domain tower: ordered operations",
    domain_tower_positive.candidate is not None
    and ops(domain_tower_positive)
    == (
        "order_generators_by_tower",
        "assemble_fraction_field_extension_tower",
        "emit_domain_tower_certificate_obligations",
    ),
)
check(
    "domain tower: external irreducibility obligation present",
    domain_tower_positive.candidate is not None
    and has_obligation(domain_tower_positive, "tower-step-monic-irreducible"),
)
check(
    "domain tower: missing characteristic refused",
    refused(
        recognize_triangular_domain_tower(
            make_request({k: v for k, v in tower_context(MONIC_TOWER).items() if k != "characteristic"})
        ),
        "missing_characteristic",
    ),
)
check(
    "domain tower: wrong shape refused",
    refused(
        recognize_triangular_domain_tower(
            make_request(tower_context(MONIC_TOWER, shape="scalar_expression"))
        ),
        "shape_mismatch",
    ),
)
non_triangular_context = {
    "problem_shape": "prime_certificate",
    "characteristic": 0,
    "ring": {"variables": ("x", "y", "z", "w"), "coefficients": "QQ", "characteristic": 0},
    "ideals": {"target": ("x*y - 1", "z*w - 1")},
}
check(
    "domain tower: non-triangular mutation refused",
    refused(
        recognize_triangular_domain_tower(make_request(non_triangular_context)),
        "not_a_triangular_tower",
    ),
)

print("-- linear_inverse_ring_map --")

LINEAR_GENERATORS = ("x - t**2", "y**2 - t")
NONLINEAR_GENERATORS = ("x**2 - t", "y**2 - t - 1")

linear_positive = recognize_linear_inverse_ring_map(
    make_request(tower_context(LINEAR_GENERATORS, shape="prime_certificate"))
)
check("linear inverse: degree-1 fresh generator admitted", linear_positive.candidate is not None)
check(
    "linear inverse: ordered operations",
    linear_positive.candidate is not None
    and ops(linear_positive)
    == ("solve_linear_generators", "construct_inverse_ring_map", "emit_isomorphic_presentation"),
)
check(
    "linear inverse: eliminated variable recorded",
    linear_positive.candidate is not None
    and "x"
    in dict(linear_positive.candidate.route.ordered_steps[0].parameters)["eliminable_variables"],
)
check(
    "linear inverse: isomorphism certificate obligation present",
    linear_positive.candidate is not None
    and has_obligation(linear_positive, "ring-map-isomorphism"),
)
check(
    "linear inverse: missing characteristic refused",
    refused(
        recognize_linear_inverse_ring_map(
            make_request(
                {k: v for k, v in tower_context(LINEAR_GENERATORS).items() if k != "characteristic"}
            )
        ),
        "missing_characteristic",
    ),
)
check(
    "linear inverse: wrong shape refused",
    refused(
        recognize_linear_inverse_ring_map(
            make_request(tower_context(LINEAR_GENERATORS, shape="scalar_expression"))
        ),
        "shape_mismatch",
    ),
)
check(
    "linear inverse: no-linear-generator mutation refused",
    refused(
        recognize_linear_inverse_ring_map(make_request(tower_context(NONLINEAR_GENERATORS))),
        "no_linear_eliminable_generator",
    ),
)

# ---------------------------------------------------------------------------
# complete intersection fixtures

print("-- regular_sequence_complete_intersection --")

CI_GENERATORS = ("x**2 - t", "y**2 - t - 1", "z - t**2")
NON_REGULAR_GENERATORS = ("x*y - 1", "x*z - 1")


def ci_context(generators: tuple[str, ...], shape: str = "ideal_decomposition", **extra) -> dict:
    context = {
        "problem_shape": shape,
        "characteristic": 0,
        "ring": {"variables": ("t", "x", "y", "z"), "coefficients": "QQ", "characteristic": 0},
        "ideals": {"target": generators},
    }
    context.update(extra)
    return context


ci_positive = recognize_regular_sequence_complete_intersection(make_request(ci_context(CI_GENERATORS)))
check("regular sequence CI: certified sequence admitted", ci_positive.candidate is not None)
check(
    "regular sequence CI: ordered operations",
    ci_positive.candidate is not None
    and ops(ci_positive)
    == (
        "certify_fresh_variable_regular_sequence",
        "derive_complete_intersection_invariants",
        "emit_ci_certificate_obligations",
    ),
)
check(
    "regular sequence CI: ring-safe monic certificate kind",
    ci_positive.candidate is not None
    and dict(ci_positive.candidate.route.ordered_steps[0].parameters)["certificate_kind"]
    == "ring_safe_monic",
)
check(
    "regular sequence CI: codimension equals generator count",
    ci_positive.candidate is not None
    and dict(ci_positive.candidate.route.ordered_steps[1].parameters)["codimension"] == 3,
)
for obligation_id in (
    "ci-height-equals-generators",
    "ci-candidate-primality",
    "ci-jacobian-minor",
    "ci-degree-balance",
):
    check(
        f"regular sequence CI: obligation {obligation_id} present",
        ci_positive.candidate is not None and has_obligation(ci_positive, obligation_id),
    )
unit_leading = recognize_regular_sequence_complete_intersection(
    make_request(ci_context(("2*x**2 - t", "y**2 - t")))
)
check(
    "regular sequence CI: unit-leading sequence admitted over the field",
    unit_leading.candidate is not None
    and dict(unit_leading.candidate.route.ordered_steps[0].parameters)["certificate_kind"]
    == "field_unit_leading",
)
check(
    "regular sequence CI: undeclared presentation refused",
    refused(
        recognize_regular_sequence_complete_intersection(
            make_request({"problem_shape": "ideal_decomposition", "characteristic": 0})
        ),
        "evidence_unavailable",
    ),
)
check(
    "regular sequence CI: wrong shape refused",
    refused(
        recognize_regular_sequence_complete_intersection(
            make_request(ci_context(CI_GENERATORS, shape="scalar_expression"))
        ),
        "shape_mismatch",
    ),
)
non_regular_context = {
    "problem_shape": "ideal_decomposition",
    "characteristic": 0,
    "ring": {"variables": ("x", "y", "z"), "coefficients": "QQ", "characteristic": 0},
    "ideals": {"target": NON_REGULAR_GENERATORS},
}
check(
    "regular sequence CI: non-certified mutation refused",
    refused(
        recognize_regular_sequence_complete_intersection(make_request(non_regular_context)),
        "not_a_certified_regular_sequence",
    ),
)

print("-- degree_balance_closure --")

balanced_context = ci_context(CI_GENERATORS, candidate_component_degrees=(4, 4))
balance_positive = recognize_degree_balance_closure(make_request(balanced_context))
check("degree balance: balanced candidates admitted", balance_positive.candidate is not None)
check(
    "degree balance: ordered operations",
    balance_positive.candidate is not None
    and ops(balance_positive)
    == (
        "certify_regular_sequence",
        "compute_weighted_ci_degree",
        "compare_component_degree_sum",
        "emit_minimal_prime_closure_obligations",
    ),
)
check(
    "degree balance: exact CI product recorded",
    balance_positive.candidate is not None
    and dict(balance_positive.candidate.route.ordered_steps[1].parameters)[
        "complete_intersection_degree"
    ]
    == 8,
)
check(
    "degree balance: closure primality obligation present",
    balance_positive.candidate is not None
    and has_obligation(balance_positive, "closure-candidate-primality"),
)
check(
    "degree balance: missing candidate degrees refused",
    refused(
        recognize_degree_balance_closure(make_request(ci_context(CI_GENERATORS))),
        "missing_candidate_component_degrees",
    ),
)
check(
    "degree balance: wrong shape refused",
    refused(
        recognize_degree_balance_closure(
            make_request(
                ci_context(CI_GENERATORS, shape="scalar_expression", candidate_component_degrees=(4, 4))
            )
        ),
        "shape_mismatch",
    ),
)
check(
    "degree balance: degree-sum mismatch mutation refused",
    refused(
        recognize_degree_balance_closure(
            make_request(ci_context(CI_GENERATORS, candidate_component_degrees=(4, 3)))
        ),
        "degree_balance_failed",
    ),
)

# ---------------------------------------------------------------------------
# elimination fixtures

print("-- generic_elimination --")

elimination_context = {
    "problem_shape": "ideal_projection",
    "characteristic": 0,
    "sheet_variables": ("w1", "w2"),
    "generic_denominator": "N1*N2",
}
elimination_positive = recognize_generic_elimination(make_request(elimination_context))
check("generic elimination: declared projection admitted", elimination_positive.candidate is not None)
check(
    "generic elimination: ordered operations",
    elimination_positive.candidate is not None
    and ops(elimination_positive)
    == (
        "saturate_by_declared_denominator",
        "eliminate_sheet_variables",
        "emit_eliminated_ideal_in_external_bindings",
    ),
)
check(
    "generic elimination: comparison-candidate burden declared",
    elimination_positive.candidate is not None
    and elimination_positive.candidate.burden_vector.as_tuple() == (2, 2, 3, 2, 0, 0)
    and elimination_positive.candidate.structural_preference_rank == 3,
)
check(
    "generic elimination: projection-closure obligation present",
    elimination_positive.candidate is not None
    and has_obligation(elimination_positive, "elimination-projection-closure"),
)
check(
    "generic elimination: sheet variables accepted from external binding",
    recognize_generic_elimination(
        make_request(
            {"problem_shape": "ideal_elimination", "characteristic": 0},
            binding={"target_ideal": "host:I", "sheet_variables": "host:sheetVars"},
        )
    ).candidate
    is not None,
)
check(
    "generic elimination: missing characteristic refused",
    refused(
        recognize_generic_elimination(
            make_request({"problem_shape": "ideal_projection", "sheet_variables": ("w1",)})
        ),
        "missing_characteristic",
    ),
)
check(
    "generic elimination: wrong shape refused",
    refused(
        recognize_generic_elimination(
            make_request(
                {"problem_shape": "scalar_expression", "characteristic": 0, "sheet_variables": ("w1",)}
            )
        ),
        "shape_mismatch",
    ),
)
check(
    "generic elimination: missing sheet variables mutation refused",
    refused(
        recognize_generic_elimination(
            make_request({"problem_shape": "ideal_projection", "characteristic": 0})
        ),
        "missing_sheet_variables",
    ),
)

print("-- localization_boundary_split --")

split_context = {
    "problem_shape": "generic_open_restriction",
    "characteristic": 0,
    "strata": (
        {"name": "U_f", "condition": "f != 0", "status": "assumed"},
        {"name": "Z_g", "condition": "g = 0", "status": "excluded"},
    ),
}
split_positive = recognize_localization_boundary_split(make_request(split_context))
check("boundary split: declared strata admitted", split_positive.candidate is not None)
check(
    "boundary split: ordered operations",
    split_positive.candidate is not None
    and ops(split_positive)
    == ("saturate_to_open", "record_excluded_boundary_tasks", "emit_open_restriction"),
)
check(
    "boundary split: every boundary retained as a task",
    split_positive.candidate is not None
    and dict(split_positive.candidate.route.ordered_steps[1].parameters)["task_count"] == 2
    and ("excluded", "Z_g", "g = 0")
    in dict(split_positive.candidate.route.ordered_steps[1].parameters)["boundary_tasks"],
)
check(
    "boundary split: saturation-witness obligation present",
    split_positive.candidate is not None and has_obligation(split_positive, "saturation-witness"),
)
check(
    "boundary split: missing open declaration refused",
    refused(
        recognize_localization_boundary_split(
            make_request({"problem_shape": "generic_open_restriction", "characteristic": 0})
        ),
        "missing_open_stratum_declaration",
    ),
)
check(
    "boundary split: wrong shape refused",
    refused(
        recognize_localization_boundary_split(
            make_request({"problem_shape": "ideal_projection", "characteristic": 0})
        ),
        "shape_mismatch",
    ),
)
malformed_strata_context = {
    "problem_shape": "generic_open_restriction",
    "characteristic": 0,
    "strata": ({"name": "U_f"},),
}
check(
    "boundary split: malformed strata mutation refused",
    refused(
        recognize_localization_boundary_split(make_request(malformed_strata_context)),
        "missing_open_stratum_declaration",
    ),
)

print("-- ordinary_host_computation --")

host_positive = recognize_ordinary_host_computation(
    make_request({"problem_shape": "ideal_decomposition", "host_default_route": "host_default_elimination"})
)
check("host default: declared default admitted", host_positive.candidate is not None)
check(
    "host default: ordered operations",
    host_positive.candidate is not None
    and ops(host_positive)
    == ("execute_host_default_route", "emit_host_result_in_external_bindings"),
)
check(
    "host default: highest burden and last preference rank",
    host_positive.candidate is not None
    and host_positive.candidate.burden_vector.invariant_level == 3
    and host_positive.candidate.burden_vector.global_expansion_rank == 3
    and host_positive.candidate.burden_vector.elimination_rank == 3
    and host_positive.candidate.structural_preference_rank == 4,
)
check(
    "host default: admitted for any declared shape",
    recognize_ordinary_host_computation(
        make_request({"problem_shape": "scalar_expression", "host_default_route": "host_default_evaluate"})
    ).candidate
    is not None,
)
check(
    "host default: result-identity obligation present",
    host_positive.candidate is not None
    and has_obligation(host_positive, "host-default-result-identity"),
)
check(
    "host default: missing declaration refused",
    refused(
        recognize_ordinary_host_computation(make_request({"problem_shape": "ideal_decomposition"})),
        "missing_host_default_declaration",
    ),
)
check(
    "host default: empty declaration refused",
    refused(
        recognize_ordinary_host_computation(
            make_request({"problem_shape": "ideal_decomposition", "host_default_route": " "})
        ),
        "missing_host_default_declaration",
    ),
)
check(
    "host default: non-string declaration mutation refused",
    refused(
        recognize_ordinary_host_computation(
            make_request({"problem_shape": "ideal_decomposition", "host_default_route": 7})
        ),
        "missing_host_default_declaration",
    ),
)

# ---------------------------------------------------------------------------
# provider tuples, determinism, and boundary invariants

print("-- provider tuples and boundary invariants --")

provider_families = tuple(
    provider.route_family
    for providers in (REWRITE_PROVIDERS, TRIANGULAR_PROVIDERS, CI_PROVIDERS, ELIMINATION_PROVIDERS)
    for provider in providers
)
check("providers: all nine families registered", provider_families == ALL_FAMILIES)
check(
    "providers: contracts match their families",
    all(
        provider.contract.route_family == provider.route_family
        for providers in (REWRITE_PROVIDERS, TRIANGULAR_PROVIDERS, CI_PROVIDERS, ELIMINATION_PROVIDERS)
        for provider in providers
    ),
)
check(
    "providers: every contract cites at least one source",
    all(
        provider.contract.source_references
        for providers in (REWRITE_PROVIDERS, TRIANGULAR_PROVIDERS, CI_PROVIDERS, ELIMINATION_PROVIDERS)
        for provider in providers
    ),
)

serialized = canonical_json_bytes(substitution_positive.candidate.route)
check(
    "routes: serialization is byte deterministic",
    serialized == canonical_json_bytes(recognize_direct_substitution(make_request(tower_context(MONIC_TOWER))).candidate.route),
)
check("routes: no wall-clock prediction emitted", b"predicted_duration" not in serialized)
check("routes: no final mathematical result emitted", b"final_result" not in serialized)

not_enabled = PathfinderRequest.create(
    request_id="providers-algebra-gate-v1",
    target_obligation=Obligation("target-task", "Discharge the declared task.", "exact"),
    external_binding={"target_ideal": "host:I"},
    mathematical_context={"problem_shape": "ideal_decomposition", "characteristic": 0},
    available_route_families=("contact_restriction",),
)
check(
    "routes: disabled family refused as route_not_enabled",
    refused(recognize_direct_substitution(not_enabled), "route_not_enabled"),
)


print()
if FAILS:
    print(f"GATE PATHFINDER PROVIDERS ALGEBRA: OPEN ({len(FAILS)} failing)")
    raise SystemExit(1)
print("GATE PATHFINDER PROVIDERS ALGEBRA: CLOSED")
