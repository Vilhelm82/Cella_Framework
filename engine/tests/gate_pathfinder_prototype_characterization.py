"""Characterize the pre-package Pathfinder behavior before refactoring.

Authority: campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md, sections 5 and 13.1.

The named upload/pathfinder(1).py is absent from the workspace.  Git commit
a0beee8 preserves the earliest route_plan-only implementation; the live
src/cella/pathfinder.py plus the existing MCP gates are its tested behavioral
continuation.  This gate freezes the handoff-required public behavior without
claiming that the recovered Git blob is byte-identical to the missing upload.

Run: python tests/gate_pathfinder_prototype_characterization.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.pathfinder import pathfinder_compare, rewrite_candidates, route_plan


FAILS: list[str] = []
SWEEP = {"variable": "eps", "low": "1e-12", "high": "1e-4"}


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


def route(expression: str, constants: dict | None = None) -> dict:
    return route_plan(expression, SWEEP, constants=constants)


# Required route decisions.
decision_cases = (
    ("no subtraction -> direct_ok", "eps * eps", "direct_ok"),
    ("x-x -> collapse_symbolically", "eps - eps", "collapse_symbolically"),
    (
        "fully rewriteable catastrophic cancellation -> rewrite candidate",
        "(1 + eps) - 1",
        "rewrite_candidate_needed",
    ),
    (
        "partially rewriteable catastrophic cancellation -> precision budget",
        "(cos(eps) - 1) + ((1 + eps) - 1)",
        "precision_budget_needed",
    ),
    (
        "benign cancellation -> monitored direct route",
        "(1 + sqrt(eps)) - 1",
        "direct_ok",
    ),
    (
        "unknown symbolic constants -> needs declaration",
        "(A + eps) - A",
        "needs_declared_constants",
    ),
    ("unrecognized shape -> unsupported", "foo(eps)", "unsupported_shape"),
)

for label, expression, expected in decision_cases:
    check(label, route(expression)["decision"] == expected)

mixed = route("(cos(eps) - 1) + ((1 + eps) - 1)")
check(
    "partial rewrite coverage remains explicit",
    mixed["profile_summary"]["catastrophic_site_count"] == 2
    and mixed["profile_summary"]["rewriteable_catastrophic_site_count"] == 1
    and mixed["profile_summary"]["unresolved_catastrophic_site_count"] == 1,
)

unknown = route("(A + eps) - A")
check(
    "blocking input is structured rather than scraped by the caller",
    unknown["blocking_inputs"]["missing_constants"] == ["A"],
)

benign = route("(1 + sqrt(eps)) - 1")
check(
    "benign direct route retains monitoring tools",
    "cella_bacl_pair" in benign["next_tools"]
    and "cella_operand_residue_trace" in benign["next_tools"],
)


# Required conservative rewrite families.
rewrite_cases = (
    ("self_collapse", "eps - eps"),
    ("constant_offset_collapse", "(1 + eps) - 1"),
    ("scaled_constant_offset_collapse", "2 * (1 + eps) - 2"),
    ("difference_of_squares", "(a * a) - (b * b)"),
    ("sqrt_conjugate", "sqrt(1 + eps) - 1"),
    ("common_factor_extraction", "(a * c) - (b * c)"),
    ("three_term_regroup", "a + b + c"),
)

for family, expression in rewrite_cases:
    record = rewrite_candidates(expression, sweep=SWEEP)
    check(
        f"rewrite family remains conservative and available: {family}",
        any(candidate["family"] == family for candidate in record["candidates"]),
    )


# Required fingerprint distinctions.
fingerprinted = route("2 * (1 + eps) - 2")
fingerprint = fingerprinted["residual_fingerprint"]
required_fingerprint_fields = {
    "local_shape_class",
    "residual_order",
    "residual_order_evidence",
    "residual_scale_class",
    "account_closure_status",
    "burden_vector",
    "domain_refusal_stratum",
    "canonical_cross_form",
    "site_fingerprints",
}
check(
    "residual fingerprint retains every handoff-required axis",
    required_fingerprint_fields <= set(fingerprint),
)
check(
    "site fingerprint retains route-assembly classification",
    bool(fingerprint["site_fingerprints"])
    and fingerprint["site_fingerprints"][0]["route_assembly_class"]
    == "scaled_constant_offset_collapse",
)


# Required burden/Pareto comparator behavior.
comparison = pathfinder_compare(
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
check(
    "comparison preserves declared-grid equality and clean-form winner",
    comparison["winner"] in {"clean_absorb_first", "clean_absorb_commuted"}
    and comparison["equivalence_status"]
    == "verified_exact_real_equivalence_on_declared_grid"
    and comparison["burden_vectors"]["dirty_left_first"]["max_integer_residual"]
    == "1/2",
)
check(
    "comparison retains Pareto relations",
    bool(comparison["ranking"]["pareto_frontier"])
    and "dirty_left_first" in comparison["ranking"]["dominated_by"],
)


# Characterize deterministic output before typed-IR migration.
first = route("(1 + eps) - 1")
second = route("(1 + eps) - 1")
check(
    "same request produces byte-identical canonical JSON",
    json.dumps(first, sort_keys=True, separators=(",", ":"))
    == json.dumps(second, sort_keys=True, separators=(",", ":")),
)


print()
if FAILS:
    print(f"GATE PATHFINDER PROTOTYPE CHARACTERIZATION: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE PATHFINDER PROTOTYPE CHARACTERIZATION: CLOSED")
sys.exit(0)

