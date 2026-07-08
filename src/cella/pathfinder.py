"""Cella pathfinder route planning and conservative rewrite support."""

from __future__ import annotations

import ast

from .residual_profile import residual_profile


def route_plan(
    expression: str,
    sweep: dict,
    constants: dict | None = None,
    include_profile: bool = False,
    include_samples: bool = False,
) -> dict:
    try:
        profile = residual_profile(
            str(expression),
            sweep,
            constants=constants or {},
            include_samples=include_samples,
        )
    except Exception as exc:
        return {
            "expression": str(expression),
            "decision": "unsupported_shape",
            "why": f"Residual profile could not parse or probe the expression: {exc}",
            "operation_shape": None,
            "dominant_pattern": None,
            "exact_account_available": False,
            "blocking_inputs": {"unsupported": str(exc), "missing_constants": []},
            "next_tools": ["cella_help"],
            "route_confidence": "low",
            "profile_summary": {},
        }

    sites = list(profile.get("danger_sites", []))
    burden = dict(profile.get("predicted_burden_vector", {}))
    operation_shape = str(profile.get("operation_shape"))
    dominant = burden.get("dominant_pattern")
    missing = _missing_constants(sites)
    exact_account = _has_exact_account(sites)
    known_rewrite = _has_known_rewrite(str(expression), operation_shape, sites)

    if missing:
        decision = "needs_declared_constants"
        why = "At least one subtraction site contains an unknown symbolic parameter."
        next_tools = ["cella_route_plan"]
        confidence = "high"
    elif operation_shape == "no_subtraction":
        decision = "direct_ok"
        why = "No subtraction site was detected."
        next_tools = ["cella_symbolic_rational", "cella_arith_precision_budget"]
        confidence = "high"
    elif operation_shape == "self_cancellation":
        decision = "collapse_symbolically"
        why = "A structural x-x site can be collapsed before arithmetic."
        next_tools = ["cella_symbolic_rational", "cella_symbolic_equal"]
        confidence = "high"
    elif operation_shape == "catastrophic_cancellation" and known_rewrite:
        decision = "rewrite_candidate_needed"
        why = "Catastrophic same-leading-constant cancellation has at least one conservative rewrite family."
        next_tools = ["cella_rewrite_candidates", "cella_pathfinder_compare"]
        confidence = "high" if exact_account else "medium"
    elif operation_shape == "catastrophic_cancellation":
        decision = "precision_budget_needed"
        why = "Catastrophic cancellation was detected but no conservative rewrite family was found."
        next_tools = ["cella_arith_precision_budget", "cella_operand_residue_trace"]
        confidence = "medium"
    elif operation_shape == "benign_cancellation":
        decision = "direct_ok"
        why = "Cancellation opens with a benign fractional signal; monitor BACL/account burden."
        next_tools = ["cella_bacl_pair", "cella_operand_residue_trace"]
        confidence = "medium"
    elif operation_shape == "partly_unrecognised":
        decision = "unsupported_shape"
        why = "At least one subtraction site could not be classified."
        next_tools = ["cella_operand_residue_trace", "cella_help"]
        confidence = "low"
    else:
        decision = "direct_ok"
        why = "No high-risk cancellation route was detected."
        next_tools = ["cella_arith_precision_budget"]
        confidence = "medium"

    out = {
        "expression": str(expression),
        "decision": decision,
        "why": why,
        "operation_shape": operation_shape,
        "dominant_pattern": dominant,
        "exact_account_available": exact_account,
        "blocking_inputs": {"missing_constants": missing},
        "next_tools": next_tools,
        "route_confidence": confidence,
        "profile_summary": {
            "site_count": len(sites),
            "danger_sites": [
                {
                    "path": site.get("path"),
                    "pattern": site.get("pattern"),
                    "severity": site.get("severity"),
                    "signal_exponent": site.get("signal_exponent"),
                    "account_probe_status": site.get("account_probe_status"),
                }
                for site in sites
            ],
            "predicted_burden_vector": burden,
        },
    }
    if include_profile:
        out["profile"] = profile
    return out


def _has_exact_account(sites: list[dict]) -> bool:
    for site in sites:
        if site.get("account_probe_status") in ("exact_q_account", "structural_exact"):
            return True
        for sample in site.get("probe_samples", []):
            if sample.get("exact_account", {}).get("status") == "exact_q_account":
                return True
    return False


def _missing_constants(sites: list[dict]) -> list[str]:
    missing = set()
    marker = "unknown parameter "
    for site in sites:
        text = str(site.get("probe_error", ""))
        if marker in text:
            name = text.split(marker, 1)[1].split(";", 1)[0].strip().strip("'\"")
            if name:
                missing.add(name)
    return sorted(missing)


def _has_known_rewrite(
    expression: str, operation_shape: str, sites: list[dict]
) -> bool:
    if operation_shape == "self_cancellation":
        return True
    if operation_shape != "catastrophic_cancellation":
        return False
    try:
        root = ast.parse(str(expression), mode="eval").body
    except SyntaxError:
        return False
    for site in sites:
        if not _is_catastrophic_site(site):
            continue
        node = _node_at_profile_path(root, site.get("path"))
        if node is None or not _is_subtraction(node):
            continue
        if (
            _has_sqrt_conjugate_shape(node)
            or _has_difference_of_squares_shape(node)
            or _has_simple_constant_perturbation(node)
        ):
            return True
    return False


def _is_catastrophic_site(site: dict) -> bool:
    return (
        site.get("severity") == "catastrophic"
        or site.get("pattern") == "sterbenz_safe_catastrophic"
    )


def _is_subtraction(node: ast.AST) -> bool:
    return isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub)


def _node_at_profile_path(root: ast.AST, path: object) -> ast.AST | None:
    if not isinstance(path, str) or not path.startswith("root"):
        return None
    node = root
    for part in path.split(".")[1:]:
        if part == "left" and isinstance(node, ast.BinOp):
            node = node.left
        elif part == "right" and isinstance(node, ast.BinOp):
            node = node.right
        elif part == "arg":
            if isinstance(node, ast.UnaryOp):
                node = node.operand
            elif isinstance(node, ast.Call) and node.args:
                node = node.args[0]
            else:
                return None
        else:
            return None
    return node


def _has_simple_constant_perturbation(node: ast.AST) -> bool:
    if not _is_subtraction(node):
        return False
    if not _is_numeric_constant(node.right):
        return False
    if not isinstance(node.left, ast.BinOp) or not isinstance(node.left.op, ast.Add):
        return False
    return _same_constant(node.left.left, node.right) or _same_constant(
        node.left.right, node.right
    )


def _has_difference_of_squares_shape(node: ast.AST) -> bool:
    if not _is_subtraction(node):
        return False
    if not _is_nonnegative_numeric_constant(node.right):
        return False
    left = node.left
    if isinstance(left, ast.BinOp) and isinstance(left.op, ast.Mult):
        return ast.dump(left.left) == ast.dump(left.right)
    if isinstance(left, ast.BinOp) and isinstance(left.op, ast.Pow):
        return _constant_value(left.right) == 2
    return False


def _has_sqrt_conjugate_shape(node: ast.AST) -> bool:
    if not _is_subtraction(node):
        return False
    if not isinstance(node.left, ast.Call):
        return False
    if not isinstance(node.left.func, ast.Name) or node.left.func.id != "sqrt":
        return False
    return isinstance(node.right, ast.Constant) and node.right.value == 1


def _same_constant(left: ast.AST, right: ast.AST) -> bool:
    return _is_numeric_constant(left) and _constant_value(left) == _constant_value(right)


def _is_numeric_constant(node: ast.AST) -> bool:
    return _constant_value(node) is not None


def _is_nonnegative_numeric_constant(node: ast.AST) -> bool:
    value = _constant_value(node)
    return value is not None and value >= 0


def _constant_value(node: ast.AST) -> int | float | None:
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    ):
        return node.value
    return None
