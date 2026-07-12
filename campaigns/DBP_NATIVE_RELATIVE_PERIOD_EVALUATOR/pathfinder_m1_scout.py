"""Compile-time Pathfinder scout for the M1 static execution schedule.

This program ranks only already-admissible executor schedules.  Its evidence is
deliberately not imported by the native evaluator and is never a certificate.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from cella.pathfinder import (BurdenVector, ComputationalRoute, Obligation,
                              RouteCandidate, RouteContract, RouteStep)
from cella.pathfinder.plan.compare import compare_candidates


TARGET_BITS = 150
OBLIGATIONS = (
    Obligation("dbp-domain", "Executor re-proves exact radicand and denominator separation.", "theorem"),
    Obligation("dbp-radius", "Executor re-proves the admitted complex analytic disk radius.", "theorem"),
    Obligation("dbp-account", "Executor closes every fixed-DAG arithmetic account.", "identity"),
    Obligation("dbp-remainder", "Executor proves the algebraic-recurrence Cauchy remainder.", "theorem"),
)


def candidate(name: str, plus_segments, minus_segments, form: str) -> RouteCandidate:
    family = f"dbp_recurrence_{name}_{form}"
    contract = RouteContract(
        family, "fixed smooth E128 DBP algebraic kernel", (), (), OBLIGATIONS, (), (),
        "cella.native_periods.quadrature", OBLIGATIONS,
        ("DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_BUILD_SPEC_v1.0.md section 9",),
    )
    route = ComputationalRoute(
        "dbp-m1-autotune", OBLIGATIONS[-1], family,
        (RouteStep("execute", "fixed_algebraic_recurrence_cauchy", ("compiled_kernel",), ("dyadic_bracket",),
                   (("plus_segments", plus_segments), ("minus_segments", minus_segments),
                    ("kernel_form", form))),),
        ("compiled_kernel",), (), ("algebraic_recurrence_coefficients", "panel_remainder_ledger"), (), OBLIGATIONS, (),
        "The native executor independently discharges every emitted obligation.",
    )
    operations = sum(count*order*order for count, order, radius in plus_segments+minus_segments)
    operations *= 9 if form == "factored" else 12
    # Predicted width is scout evidence only; underpredicted candidates are not
    # admitted to comparison.
    return RouteCandidate(contract, route, BurdenVector(
        invariant_level=1, exact_operation_count=operations,
        scout_operation_count=4, expression_depth=8 if form == "factored" else 11,
    ), 0 if form == "factored" else 1)


def main():
    selected_plus = ((32, 88, 6),)
    selected_minus = ((9,70,8),(3,80,6),(3,104,4),(5,128,3),
                      (3,104,4),(3,80,6),(6,70,8))
    raw = [
        candidate("segmented_p32", selected_plus, selected_minus, "factored"),
        candidate("uniform_p32", ((32,128,3),), ((32,128,3),), "factored"),
        candidate("uniform_p64", ((64,104,4),), ((64,104,4),), "factored"),
        candidate("segmented_p32", selected_plus, selected_minus, "expanded"),
    ]
    # The executor later verifies these predictions; they only bound the scout
    # search and never constitute admission or certificate evidence.
    winner, frontier, rejected = compare_candidates(tuple(raw))
    params = dict(winner.route.ordered_steps[0].parameters)
    report = {
        "status": "compile_time_scout_only", "target_bits": TARGET_BITS,
        "selected_family": winner.contract.route_family, "selected_parameters": params,
        "exact_obligations": [asdict(o) for o in OBLIGATIONS],
        "frontier": [c.contract.route_family for c in frontier],
        "rejections": [asdict(r) for r in rejected],
        "warning": "Pathfinder predictions are non-verdict-bearing and never enter the evaluator certificate.",
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
