"""Structural expression scout: cancellation shape and rewrite coverage.

This is the typed, purely syntactic port of the legacy prototype's route
classification.  It inspects subtraction sites and conservative rewrite
families without floating-point probing; numeric residual telemetry stays in
the legacy compatibility surface.
"""

from __future__ import annotations

from ..ir.expression import (
    ExpressionNode,
    ExpressionShadowUnavailable,
    expression_depth,
    node_count,
    parse_expression,
    structurally_equal,
    subtraction_sites,
)
from ..ir.problem import NormalizedProblem
from ..ir.scope import AnalysisBudget
from ..ir.evidence import ScoutEvidence
from .protocol import scout_evidence

REWRITE_FAMILIES = (
    "self_collapse",
    "constant_offset_collapse",
    "scaled_constant_offset_collapse",
    "difference_of_squares",
    "sqrt_conjugate",
    "common_factor_extraction",
)


def _is_square(node: ExpressionNode) -> ExpressionNode | None:
    if node.kind == "mul" and structurally_equal(node.children[0], node.children[1]):
        return node.children[0]
    if node.kind == "pow" and node.children[1].kind == "const" and node.children[1].constant == 2:
        return node.children[0]
    return None


def _rewrite_families_at(site: ExpressionNode) -> tuple[str, ...]:
    left, right = site.children
    families: list[str] = []
    if structurally_equal(left, right):
        families.append("self_collapse")
    if left.kind == "add" and any(structurally_equal(child, right) for child in left.children):
        families.append("constant_offset_collapse")
    if left.kind == "mul" and right.kind in {"const", "mul"}:
        families.append("scaled_constant_offset_collapse")
    if _is_square(left) is not None and (_is_square(right) is not None or right.kind == "const"):
        families.append("difference_of_squares")
    if (left.kind == "call" and left.name == "sqrt" and right.kind == "const") or (
        right.kind == "call" and right.name == "sqrt" and left.kind == "const"
    ):
        families.append("sqrt_conjugate")
    if left.kind == "mul" and right.kind == "mul":
        for left_factor in left.children:
            if any(structurally_equal(left_factor, right_factor) for right_factor in right.children):
                families.append("common_factor_extraction")
                break
    return tuple(families)


def expression_shape_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
) -> ScoutEvidence | None:
    if problem.expression is None:
        return None
    try:
        tree = parse_expression(problem.expression, max_nodes=budget.max_expression_nodes)
    except ExpressionShadowUnavailable as exc:
        return scout_evidence(
            scout_family="expression_shape",
            problem=problem,
            fingerprint={
                "shape": "unsupported",
                "reason": str(exc),
                "subtraction_site_count": 0,
            },
            trace=(f"expression shadow unavailable: {exc}",),
            stability="unstable",
            scout_operations=1,
        )
    sites = subtraction_sites(tree)
    site_families = {path: _rewrite_families_at(site) for path, site in sites}
    self_collapse_count = sum(1 for families in site_families.values() if "self_collapse" in families)
    rewriteable = sum(1 for families in site_families.values() if families)
    if not sites:
        shape = "no_subtraction"
    elif self_collapse_count == len(sites):
        shape = "self_cancellation"
    elif rewriteable == len(sites):
        shape = "cancellation_fully_rewriteable"
    elif rewriteable:
        shape = "cancellation_partly_rewriteable"
    else:
        shape = "cancellation_unresolved"
    return scout_evidence(
        scout_family="expression_shape",
        problem=problem,
        fingerprint={
            "shape": shape,
            "subtraction_site_count": len(sites),
            "rewriteable_site_count": rewriteable,
            "self_collapse_site_count": self_collapse_count,
            "site_rewrite_families": tuple(
                (path, families) for path, families in sorted(site_families.items())
            ),
            "node_count": node_count(tree),
            "expression_depth": expression_depth(tree),
        },
        trace=(f"{len(sites)} subtraction sites; {rewriteable} rewriteable",),
        stability="exact",
        scout_operations=node_count(tree),
    )
