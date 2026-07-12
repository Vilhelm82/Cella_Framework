"""Unit gate for every Pathfinder kernel component (IR, scouts, comparison)."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FAILS: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


# --- expression IR ---------------------------------------------------------
from cella.pathfinder.ir.expression import (
    ExpressionShadowUnavailable,
    expression_depth,
    node_count,
    parse_expression,
    subtraction_sites,
    variables_used,
)

tree = parse_expression("(1 + x) - 1")
check("expression IR parses and finds one subtraction site", len(subtraction_sites(tree)) == 1)
check("expression IR reports variables deterministically", variables_used(tree) == ("x",))
check("expression IR depth/count are positive", expression_depth(tree) >= 2 and node_count(tree) >= 3)
try:
    parse_expression("x +", max_nodes=10)
    check("unparseable expression raises shadow-unavailable", False)
except ExpressionShadowUnavailable:
    check("unparseable expression raises shadow-unavailable", True)
try:
    parse_expression("x " + "+ x" * 50, max_nodes=10)
    check("node budget is enforced", False)
except ExpressionShadowUnavailable:
    check("node budget is enforced", True)

# --- polynomial shadow -----------------------------------------------------
from cella.pathfinder.ir.polynomial import shadow_polynomial

variables = ("M", "N1", "u", "w1")
quadric = shadow_polynomial("w1**2 - u - N1**2", variables)
check("shadow expands exact sparse terms", quadric.total_degree() == 2)
check("fresh-variable monic detection (ring-safe)", quadric.is_monic_in("w1"))
check("mixed leading coefficient is not monic", not shadow_polynomial("u*w1 + M", variables).is_monic_in("u"))
check(
    "field-unit leading is distinguished from ring-safe monic",
    shadow_polynomial("w1 - 4*M", variables).has_unit_leading_in("M")
    and not shadow_polynomial("w1 - 4*M", variables).is_monic_in("M"),
)
check(
    "weighted degree respects declared weights",
    shadow_polynomial("u**2 + M", ("M", "u")).weighted_degree((1, 2)) == 4,
)
try:
    shadow_polynomial("q + 1", variables)
    check("undeclared variable is refused by the shadow", False)
except ExpressionShadowUnavailable:
    check("undeclared variable is refused by the shadow", True)

# --- F2 --------------------------------------------------------------------
from cella.pathfinder.scout.f2 import f2_kernel_basis, f2_orbit_rank, f2_rank

identity5 = tuple(tuple(1 if i == j else 0 for j in range(5)) for i in range(5))
static_rows = tuple(tuple(list(identity5[i]) + [0] * 5) for i in range(5)) + tuple(
    tuple(list(identity5[i]) + list(identity5[i])) for i in range(5)
)
check("static parity matrix has F2 rank 10", f2_rank(static_rows) == 10)
kernel = f2_kernel_basis(((1, 1, 0), (0, 1, 1)))
check("F2 kernel basis is exact", kernel == ((1, 1, 1),))
check("orbit rank multiplies by cover degree", f2_orbit_rank(((1, 0), (1, 1)), 5) == 10)

# --- congruence inertia ----------------------------------------------------
from cella.pathfinder.scout.inertia import congruence_inertia

check(
    "hyperbolic block contributes (1,1,0)",
    congruence_inertia(((Fraction(0), Fraction(2)), (Fraction(2), Fraction(0)))) == (1, 1, 0),
)
two_i_minus_j = tuple(
    tuple(Fraction(2 if i == j else 0) - 1 for j in range(3)) for i in range(3)
)
check("2I-J has Lorentzian signature (2,1)", congruence_inertia(two_i_minus_j) == (2, 1, 0))

# --- Sturm -----------------------------------------------------------------
from cella.pathfinder.scout.sturm import sturm_root_count

lead7_gate_poly = tuple(Fraction(c) for c in (8, 15, -7, -15, 5, 2))
check(
    "lead7 Sturm gate: H~ has no roots in (1, +inf)",
    sturm_root_count(lead7_gate_poly, Fraction(1), None) == 0,
)
check(
    "x^2-2 has exactly two real roots",
    sturm_root_count((Fraction(-2), Fraction(0), Fraction(1)), None, None) == 2,
)

# --- Newton corner ---------------------------------------------------------
from cella.pathfinder.scout.newton import support_function, vertex_coefficient

check("KN corner vertex coefficient A = -84", vertex_coefficient(-6, 2, -2) == -84)
kn_vertices = ((-4, 2), (2, -4))
check(
    "KN balanced-diagonal support is 2",
    support_function(kn_vertices, (Fraction(1), Fraction(1))) == 2,
)

# --- problem lowering + hashing -------------------------------------------
from cella.pathfinder import Obligation, PathfinderRequest
from cella.pathfinder.ir.problem import lower_request, stable_problem_hash


def build_request(**context_overrides: object) -> PathfinderRequest:
    context: dict[str, object] = {
        "problem_shape": "ideal_decomposition",
        "characteristic": 0,
        "ring": {"variables": ("M", "N1", "u", "w1"), "weights": (1, 1, 2, 1)},
        "ideals": {"target": ("w1**2 - u - N1**2", "w1 - 4*M")},
    }
    context.update(context_overrides)
    return PathfinderRequest.create(
        request_id="kernel-unit",
        target_obligation=Obligation("o", "statement", "warrant"),
        external_binding={"host": "opaque"},
        mathematical_context=context,
        available_route_families=("contact_restriction",),
    )


problem = lower_request(build_request())
check("lowering exposes the declared ring", problem.ring is not None and problem.ring.weights == (1, 1, 2, 1))
check("lowering exposes named ideals", problem.ideal("target") is not None)
check(
    "problem hash is stable across identical requests",
    stable_problem_hash(problem) == stable_problem_hash(lower_request(build_request())),
)
check(
    "problem hash distinguishes different declarations",
    stable_problem_hash(problem) != stable_problem_hash(lower_request(build_request(characteristic=7))),
)

# --- fingerprint engine ----------------------------------------------------
from cella.pathfinder.ir.fingerprint import fingerprint_problem
from cella.pathfinder.ir.scope import AnalysisBudget
from cella.pathfinder.scout import fresh_variable_monic_scout

budget = AnalysisBudget()
evidence = fresh_variable_monic_scout(problem, budget)
assert evidence is not None
fp1 = fingerprint_problem(problem, (evidence,))
fp2 = fingerprint_problem(problem, (evidence,))
check("fingerprint is deterministic", fp1 == fp2)
check("fingerprint records scout provenance", "fresh_variable_monic" in fp1.provenance)
check("fingerprint id is versioned", fp1.fingerprint_id.startswith("sfp:v1:"))
ci = dict(fp1.complete_intersection_indicators)
check("fingerprint carries CI indicators from evidence", "regular_sequence_certified" in ci)

# --- comparison and loser records ------------------------------------------
from cella.pathfinder.api.contract import RouteCandidate, RouteContract
from cella.pathfinder.api.route import ComputationalRoute, RouteStep
from cella.pathfinder.ir.burden import BurdenVector
from cella.pathfinder.plan.compare import compare_candidates


def make_candidate(family: str, level: int, rank: int, exact_ops: int) -> RouteCandidate:
    contract = RouteContract(
        route_family=family,
        accepted_problem_shape="shape",
        required_hypotheses=("h",),
        required_evidence=("e",),
        produced_obligations=(Obligation("p", "s", "w"),),
        discharged_obligations=(),
        exceptional_branches=("b",),
        execution_module="external.test",
        certificate_obligations=(Obligation("c", "s", "w"),),
        source_references=("test",),
    )
    route = ComputationalRoute(
        request_id="cmp",
        target_obligation=Obligation("o", "s", "w"),
        route_family=family,
        ordered_steps=(RouteStep("s1", "op", ("i",), ("o",)),),
        data_dependencies=("i",),
        external_binding=(),
        required_intermediate_objects=(),
        required_hypotheses=("h",),
        certificate_obligations=(Obligation("c", "s", "w"),),
        exceptional_branches=("b",),
        completion_condition="done",
    )
    return RouteCandidate(
        contract=contract,
        route=route,
        burden_vector=BurdenVector(invariant_level=level, exact_operation_count=exact_ops),
        structural_preference_rank=rank,
    )


structural = make_candidate("structural", 1, 0, 4)
generic = make_candidate("generic", 2, 3, 2)
dominated = make_candidate("dominated", 1, 0, 9)
winner, frontier, rejections = compare_candidates((structural, generic, dominated))
check("lowest sufficient invariant level wins", winner.contract.route_family == "structural")
check("dominated candidate is recorded with its dominator", any(
    r.route_family == "dominated" and r.stage == "pareto_dominated" for r in rejections
))
check("every loser receives a rejection record", {r.route_family for r in rejections} == {"generic", "dominated"})
check(
    "invariant-level loss is named",
    any(r.route_family == "generic" and r.stage == "invariant_level" for r in rejections),
)

# --- planning outcome surface ----------------------------------------------
from cella.pathfinder import plan_request

outcome = plan_request(
    PathfinderRequest.create(
        request_id="m2-even-contact-delta-slice-a-v1",
        target_obligation=Obligation("base-image", "Compute the sliced base image.", "exact-scheme"),
        external_binding={"incidence_ideal": "m2:IX"},
        mathematical_context={
            "problem_shape": "signed_contact_projection",
            "sign_product": 1,
            "characteristic": 0,
            "target_generator": "delta",
            "exact_slice": {"N1": 4, "N2": 8, "N3": 12, "N4": 20},
        },
        available_route_families=("contact_restriction",),
    )
)
check("plan_request returns the selected route", outcome.route is not None)
check("plan_request attaches a structural fingerprint", outcome.structural_fingerprint is not None)
check("no losers means no rejection records", outcome.rejected_alternatives == ())


print()
if FAILS:
    print(f"GATE PATHFINDER KERNEL UNITS: OPEN ({len(FAILS)} failing)")
    raise SystemExit(1)
print("GATE PATHFINDER KERNEL UNITS: CLOSED")
