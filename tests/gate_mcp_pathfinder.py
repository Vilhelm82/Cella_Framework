"""Gate MCP pathfinder route planning.

Run:  python tests/gate_mcp_pathfinder.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


try:
    from cella.mcp_server import (
        CellaRouter,
        TOOL_GROUPS,
        TOOL_NAMES,
        call_cella_help,
        call_pathfinder_compare,
        call_route_plan,
        call_rewrite_candidates,
    )
except Exception as exc:
    print(f"GATE MCP PATHFINDER: OPEN - import failed: {exc}")
    sys.exit(1)


def route(expression, constants=None):
    return call_route_plan(
        expression=expression,
        sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
        constants=constants,
    )


linear = route("(1 + eps) - 1")
check("PTH1 catastrophic same-leading-constant expression requests rewrite candidates",
      linear["ok"]
      and linear["value"]["decision"] == "rewrite_candidate_needed"
      and linear["value"]["operation_shape"] == "catastrophic_cancellation"
      and linear["value"]["exact_account_available"] is True
      and "cella_rewrite_candidates" in linear["value"]["next_tools"])
linear_fp = linear["value"].get("residual_fingerprint", {})
check("PTH1b route plan promotes the residual fingerprint as the primary routing record",
      linear["ok"]
      and linear_fp.get("fingerprint_id") == (
          "rfp:v1:same_leading_constant_catastrophic_rewriteable:"
          "order=1:account=all_exact_q_account:route=rewrite_candidate_needed"
      )
      and linear_fp.get("local_shape_class") == "same_leading_constant_catastrophic_rewriteable"
      and linear_fp.get("residual_order") == "1"
      and linear_fp.get("residual_scale_class") == "same_leading_constant"
      and linear_fp.get("account_closure_status") == "all_exact_q_account"
      and linear_fp.get("required_route") == "rewrite_candidate_needed"
      and linear_fp.get("burden_vector", {}).get("catastrophic_sites") == 1
      and linear_fp.get("source_expression_role") == "debug_metadata"
      and linear_fp.get("engine_stack", {}).get("visibility") == "internal_background_engine"
      and "sweep_signature_probe" in linear_fp.get("engine_stack", {}).get("source_methods", []))
linear_order = linear_fp.get("residual_order_evidence", {})
check("PTH1c residual_order is measured by copied V4 slope-flow evidence",
      linear["ok"]
      and linear_order.get("status") == "SLOPE_MODEL_UNIQUE_MATCH"
      and linear_order.get("selected_model_name") == "order_1"
      and linear_order.get("order_stability") == "stable_model_match"
      and len(linear_order.get("segment_evidence", [])) >= 2)

self_cancel = route("eps - eps")
check("PTH2 structural self-cancellation routes to symbolic collapse",
      self_cancel["ok"]
      and self_cancel["value"]["decision"] == "collapse_symbolically"
      and self_cancel["value"]["route_confidence"] == "high"
      and "cella_symbolic_rational" in self_cancel["value"]["next_tools"])
self_fp = self_cancel["value"].get("residual_fingerprint", {})
check("PTH2b structural zero has a fingerprint before symbolic verification",
      self_cancel["ok"]
      and self_fp.get("local_shape_class") == "structural_zero_self_cancellation"
      and self_fp.get("residual_order") == "zero"
      and self_fp.get("account_closure_status") == "structural_exact"
      and self_fp.get("required_route") == "collapse_symbolically")

unknown = route("(A + eps) - A")
check("PTH3 missing constants are surfaced as blocking inputs",
      unknown["ok"]
      and unknown["value"]["decision"] == "needs_declared_constants"
      and "A" in unknown["value"]["blocking_inputs"]["missing_constants"])
unknown_fp = unknown["value"].get("residual_fingerprint", {})
check("PTH3b undeclared constants become a fingerprint stratum, not scraped prose",
      unknown["ok"]
      and unknown_fp.get("local_shape_class") == "parameter_blocked_residual_texture"
      and unknown_fp.get("domain_refusal_stratum") == "unknown_parameters:A"
      and unknown_fp.get("required_route") == "needs_declared_constants")

scaled_offset = route("2 * (1 + eps) - 2")
scaled_fp = scaled_offset["value"].get("residual_fingerprint", {})
check("PTH3c scaled offset collapse shares the canonical cross-form fingerprint",
      scaled_offset["ok"]
      and scaled_offset["value"]["decision"] == "rewrite_candidate_needed"
      and scaled_fp.get("canonical_cross_form", {}).get("canonical_fingerprint_id")
      == linear_fp.get("canonical_cross_form", {}).get("canonical_fingerprint_id")
      and scaled_fp.get("canonical_cross_form", {}).get("canonical_shape_class")
      == "same_leading_constant_catastrophic"
      and scaled_fp.get("source_expression") == "2 * (1 + eps) - 2")

linear_site = linear_fp.get("site_fingerprints", [{}])[0]
scaled_site = scaled_fp.get("site_fingerprints", [{}])[0]
scaled_canon = scaled_fp.get("canonical_cross_form", {})
check("PTH3e canonical cross-form preserves V4 route-substrate guardrails",
      scaled_offset["ok"]
      and abs(linear_site.get("signal_coefficient", 0.0) - 1.0) < 1e-6
      and abs(scaled_site.get("signal_coefficient", 0.0) - 2.0) < 1e-6
      and linear_site.get("scale_evidence", {}).get("left_leading_constant") == 1.0
      and scaled_site.get("scale_evidence", {}).get("left_leading_constant") == 2.0
      and linear_site.get("route_assembly_class") == "constant_offset_collapse"
      and scaled_site.get("route_assembly_class") == "scaled_constant_offset_collapse"
      and linear_site.get("predicted_precision_crossing_epsilon") is not None
      and scaled_site.get("predicted_precision_crossing_epsilon") is not None
      and scaled_canon.get("canonicalization_level") == "residual_texture_not_algebraic_identity"
      and "signal_coefficient" in scaled_canon.get("noncanonical_axes", [])
      and "route_assembly" in scaled_canon.get("noncanonical_axes", [])
      and "natural_ulp_scale" in scaled_canon.get("noncanonical_axes", [])
      and "common_mode_roundoff" in scaled_canon.get("noncanonical_axes", []))

scaled_candidates = call_rewrite_candidates(
    expression="2 * (1 + eps) - 2",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
check("PTH3d scaled offset collapse emits a residual-carrier rewrite candidate",
      scaled_candidates["ok"]
      and any(c["family"] == "scaled_constant_offset_collapse"
              and "eps" in c["expression"]
              for c in scaled_candidates["value"]["candidates"]))

benign = route("(1 + sqrt(eps)) - 1")
check("PTH4 benign cancellation remains direct but asks for BACL monitoring",
      benign["ok"]
      and benign["value"]["decision"] == "direct_ok"
      and benign["value"]["dominant_pattern"] == "sterbenz_safe_benign"
      and "cella_bacl_pair" in benign["value"]["next_tools"])

precision = route("cos(eps) - 1")
check("PTH5 catastrophic site without known rewrite routes to precision budgeting",
      precision["ok"]
      and precision["value"]["decision"] == "precision_budget_needed"
      and precision["value"]["profile_summary"]["unresolved_catastrophic_site_count"] == 1
      and "cella_arith_precision_budget" in precision["value"]["next_tools"])

mixed = route("(cos(eps) - 1) + ((1 + eps) - 1)")
check("PTH6 mixed catastrophic sites keep unresolved precision-budget route",
      mixed["ok"]
      and mixed["value"]["decision"] == "precision_budget_needed"
      and mixed["value"]["profile_summary"]["catastrophic_site_count"] == 2
      and mixed["value"]["profile_summary"]["rewriteable_catastrophic_site_count"] == 1
      and mixed["value"]["profile_summary"]["unresolved_catastrophic_site_count"] == 1)

offset = call_rewrite_candidates(
    expression="(1 + eps) - 1",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
check("PTH7 constant-offset collapse exposes the residual carrier directly",
      offset["ok"]
      and any(c["family"] == "constant_offset_collapse" and c["expression"] == "eps"
              for c in offset["value"]["candidates"]))

conjugate = call_rewrite_candidates(
    expression="sqrt(1 + eps) - 1",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
check("PTH8 conjugate template is generated for sqrt(1+eps)-1",
      conjugate["ok"]
      and any(c["family"] == "sqrt_conjugate" for c in conjugate["value"]["candidates"])
      and any("sqrt" in c["expression"] and "/" in c["expression"]
              for c in conjugate["value"]["candidates"]))

square = call_rewrite_candidates(
    expression="((12 + eps) * (12 + eps)) - 144",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
square_route = route("((12 + eps) * (12 + eps)) - 144")
square_site = square_route["value"]["residual_fingerprint"]["site_fingerprints"][0]
check("PTH9 square-minus-constant emits a difference-of-squares candidate",
      square["ok"]
      and any(c["family"] == "difference_of_squares" for c in square["value"]["candidates"])
      and square["value"]["requires_ranking"] is True
      and square_site.get("route_assembly_class") == "scaled_constant_offset_collapse")

symbolic_square = call_rewrite_candidates(
    expression="(a * a) - (b * b)",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
check("PTH10 symbolic a^2-b^2 emits a general difference-of-squares candidate",
      symbolic_square["ok"]
      and any(c["family"] == "difference_of_squares"
              and "(a)" in c["expression"]
              and "(b)" in c["expression"]
              for c in symbolic_square["value"]["candidates"]))

self_candidates = call_rewrite_candidates(
    expression="eps - eps",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
check("PTH11 self-cancellation emits zero candidate",
      self_candidates["ok"]
      and self_candidates["value"]["candidates"][0]["expression"] == "0"
      and self_candidates["value"]["candidates"][0]["family"] == "self_collapse")

comparison = call_pathfinder_compare(
    variables=["small", "big", "neg_big"],
    forms=[
        {"name": "dirty_left_first", "expression": "(small + big) + neg_big"},
        {"name": "clean_absorb_first", "expression": "small + (big + neg_big)"},
        {"name": "clean_absorb_commuted", "expression": "(big + neg_big) + small"},
    ],
    grid={
        "small": ["0x1.0000000000001p+0"],
        "big": ["0x1p+1"],
        "neg_big": ["-0x1p+1"],
    },
)
check("PTH12 pathfinder compare ranks declared equivalent forms by BACL/refinery burden",
      comparison["ok"]
      and comparison["value"]["winner"] in ["clean_absorb_first", "clean_absorb_commuted"]
      and comparison["value"]["equivalence_status"] == "verified_exact_real_equivalence_on_declared_grid"
      and comparison["value"]["burden_vectors"]["dirty_left_first"]["max_integer_residual"] == "1/2")

router = CellaRouter(default_profile="clean")
router_route = router.call(
    "route_plan",
    {"expression": "(1 + eps) - 1", "sweep": {"variable": "eps", "low": "1e-12", "high": "1e-4"}},
)
check("PTH13 route planning is internal engine API, not a public router profile tool",
      not router_route["ok"]
      and router_route["error"]["token"] == "UNKNOWN_TOOL"
      and route("(1 + eps) - 1")["value"]["decision"] == "rewrite_candidate_needed")

help_record = call_cella_help("cella_route_plan")
check("PTH14 help documents route-plan result reading",
      help_record["ok"]
      and "residual_fingerprint is the primary record" in help_record["value"]["tool"]["read_result"]
      and "decision" in help_record["value"]["tool"]["read_result"]
      and "next_tools" in help_record["value"]["tool"]["read_result"])

generic_conjugate_route = route("sqrt(1 + eps + eps*eps) - 1")
generic_conjugate = call_rewrite_candidates(
    expression="sqrt(1 + eps + eps*eps) - 1",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
check("PTH15 route promise matches generic sqrt conjugate candidate generation",
      generic_conjugate_route["ok"]
      and generic_conjugate_route["value"]["decision"] == "rewrite_candidate_needed"
      and generic_conjugate["ok"]
      and any(c["family"] == "sqrt_conjugate"
              for c in generic_conjugate["value"]["candidates"]))

right_conjugate_route = route("1 - sqrt(1 - eps)")
right_conjugate = call_rewrite_candidates(
    expression="1 - sqrt(1 - eps)",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
check("PTH16 reverse sqrt conjugate template is routed and generated",
      right_conjugate_route["ok"]
      and right_conjugate_route["value"]["decision"] == "rewrite_candidate_needed"
      and right_conjugate["ok"]
      and any(c["family"] == "sqrt_conjugate"
              for c in right_conjugate["value"]["candidates"]))

try:
    non_equivalent = call_pathfinder_compare(
        variables=["x"],
        forms=[
            {"name": "x", "expression": "x"},
            {"name": "x_plus_one", "expression": "x + 1"},
        ],
        grid={"x": ["0x1p+0"]},
    )
except Exception as exc:
    non_equivalent = {"ok": False, "exception_type": type(exc).__name__, "refusal": None}
check("PTH17 non-equivalent compare returns a refusal instead of leaking an exception",
      non_equivalent["ok"] is False
      and non_equivalent.get("exception_type") is None
      and non_equivalent["refusal"]["token"] == "INDETERMINATE"
      and non_equivalent["refusal"]["stratum"] == "non_equivalent_declared_grid")

print()
if FAILS:
    print(f"GATE MCP PATHFINDER: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP PATHFINDER: CLOSED - route planner, rewrite candidates, and comparison are internal engine APIs.")
sys.exit(0)
