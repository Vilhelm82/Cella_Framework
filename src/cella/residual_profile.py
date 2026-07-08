"""Residual-shape profiler for Cella operation routing.

This module is intentionally small and dependency-free.  It is not a symbolic
CAS; it is a preflight layer that reads an arithmetic expression graph and
predicts where cancellation will dominate the operational burden.
"""

from __future__ import annotations

import ast
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable

from .probe_observers import sweep_signature_probe
from .slope_flow import residual_order_flow, residual_order_from_sweep_signature
from .typed_log_log_slope import fit_power_law_signed
from .typed_ulp import ulp_fraction

_MACHINE_EPSILON = 2.0 ** -52
# Subtraction condition number (|a|+|b|)/|a-b| at or above which the pre-read
# routes to the exact/rewrite path. This signal is scale-free, so it catches
# cancellation between operands that GROW with the sweep (e.g. sqrt(x+1)-sqrt(x)
# as x->inf), which the x=0 leading-constant test cannot see. Biased toward
# caution by design: it only promotes severity, never demotes, and is tunable.
_CONDITION_CATASTROPHIC = 1.0e4
_FUNCTIONS: dict[str, Callable[[float], float]] = {
    "sqrt": math.sqrt,
    "cos": math.cos,
    "sin": math.sin,
    "tan": math.tan,
    "acos": math.acos,
    "asin": math.asin,
    "atan": math.atan,
    "log": math.log,
    "exp": math.exp,
    "abs": abs,
}
_BUILTIN_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}


class UnsupportedExpression(ValueError):
    """Raised when the preflight grammar cannot represent the expression."""


@dataclass(frozen=True)
class Expr:
    def evaluate(self, env: dict[str, float]) -> float:
        raise NotImplementedError

    def render(self) -> str:
        raise NotImplementedError

    def structural_key(self):
        raise NotImplementedError


@dataclass(frozen=True)
class Constant(Expr):
    text: str
    value: float

    def evaluate(self, env: dict[str, float]) -> float:
        return self.value

    def render(self) -> str:
        return self.text

    def structural_key(self):
        return ("const", self.text)


@dataclass(frozen=True)
class Variable(Expr):
    name: str

    def evaluate(self, env: dict[str, float]) -> float:
        if self.name not in env:
            raise UnsupportedExpression(f"missing value for variable {self.name!r}")
        return env[self.name]

    def render(self) -> str:
        return self.name

    def structural_key(self):
        return ("var", self.name)


@dataclass(frozen=True)
class UnknownParameter(Expr):
    name: str

    def evaluate(self, env: dict[str, float]) -> float:
        raise UnsupportedExpression(f"unknown parameter {self.name!r}; provide constants to profile it")

    def render(self) -> str:
        return self.name

    def structural_key(self):
        return ("param", self.name)


@dataclass(frozen=True)
class Unary(Expr):
    op: str
    value: Expr

    def evaluate(self, env: dict[str, float]) -> float:
        v = self.value.evaluate(env)
        if self.op == "neg":
            return -v
        if self.op == "pos":
            return v
        if self.op not in _FUNCTIONS:
            raise UnsupportedExpression(f"unsupported unary operation {self.op!r}")
        return _FUNCTIONS[self.op](v)

    def render(self) -> str:
        if self.op == "neg":
            return f"(-{self.value.render()})"
        if self.op == "pos":
            return f"(+{self.value.render()})"
        return f"{self.op}({self.value.render()})"

    def structural_key(self):
        return ("unary", self.op, self.value.structural_key())


@dataclass(frozen=True)
class Binary(Expr):
    op: str
    left: Expr
    right: Expr

    def evaluate(self, env: dict[str, float]) -> float:
        a = self.left.evaluate(env)
        b = self.right.evaluate(env)
        if self.op == "add":
            return a + b
        if self.op == "sub":
            return a - b
        if self.op == "mul":
            return a * b
        if self.op == "div":
            return a / b
        if self.op == "pow":
            return a ** b
        raise UnsupportedExpression(f"unsupported binary operation {self.op!r}")

    def render(self) -> str:
        symbols = {
            "add": "+",
            "sub": "-",
            "mul": "*",
            "div": "/",
            "pow": "**",
        }
        return f"({self.left.render()} {symbols[self.op]} {self.right.render()})"

    def structural_key(self):
        return (self.op, self.left.structural_key(), self.right.structural_key())


@dataclass(frozen=True)
class Sweep:
    variable: str
    low: float
    high: float
    points: tuple[float, ...]


def residual_profile(
    expression: str,
    sweep: dict,
    n_samples: int = 9,
    constants: dict | None = None,
    include_samples: bool = False,
) -> dict:
    """Profile residual shape for a one-parameter expression graph."""

    parsed_sweep = _parse_sweep(sweep, n_samples)
    expr = _parse_expression(expression, parsed_sweep.variable, constants or {})
    sites = _collect_sites(expr, parsed_sweep, include_samples)
    burden = _burden_vector(sites)
    operation_shape = _operation_shape(sites)
    return {
        "expression": expression,
        "telemetry_role": "binary64 residual and floating-point noise are first-class probe data for route selection",
        "measured_artifact_contract": {
            "probe_precision": "python_float_binary64",
            "machine_epsilon": _MACHINE_EPSILON,
            "samples_included": bool(include_samples),
            "exact_account_probe": "auto_for_rational_arithmetic_subgraphs",
            "interpretation": "Measured probe samples expose operation texture; they do not replace final arithmetic evaluation.",
        },
        "sweep": {
            "variable": parsed_sweep.variable,
            "low": parsed_sweep.low,
            "high": parsed_sweep.high,
            "points": list(parsed_sweep.points),
        },
        "operation_shape": operation_shape,
        "predicted_burden_vector": burden,
        "danger_sites": sites,
        "recommended_process": _recommended_process(operation_shape, sites),
        "capabilities": [
            "static_subtraction_tree_scan",
            "structural_self_cancellation_detection",
            "same_leading_constant_cancellation_classification",
            "cheap_expression_graph_micro_probe_for_buried_constants",
            "fractional_signal_exponent_fit",
            "process_routing_into_cleanliness_and_arithmetic_tools",
        ],
        "gaps": [
            "one_sweep_variable_only",
            "unknown_symbolic_parameters_need_declared_constants_for_probe_classification",
            "no full asymptotic algebra yet for branch cuts, piecewise domains, or multivariate paths",
            "micro_probe_is_a_lightweight_shape_probe_not_a replacement_for_final_numeric_evaluation",
        ],
    }


def _parse_sweep(sweep: dict, n_samples: int) -> Sweep:
    if not isinstance(sweep, dict):
        raise ValueError("sweep must be a dictionary with variable, low, and high")
    variable = str(sweep.get("variable", "eps")).strip()
    if not variable.isidentifier():
        raise ValueError("sweep variable must be a valid identifier")
    if "points" in sweep:
        points = tuple(float(x) for x in sweep["points"])
        if not points:
            raise ValueError("sweep points must not be empty")
        low = min(points)
        high = max(points)
    else:
        low = float(sweep.get("low", "1e-12"))
        high = float(sweep.get("high", "1e-4"))
        count = max(3, int(n_samples))
        points = _logspace(low, high, count)
    if low <= 0 or high <= 0:
        raise ValueError("sweep low/high must be positive for residual exponent profiling")
    if high < low:
        raise ValueError("sweep high must be greater than or equal to low")
    if any(p <= 0 for p in points):
        raise ValueError("sweep points must be positive")
    return Sweep(variable=variable, low=low, high=high, points=tuple(points))


def _logspace(low: float, high: float, count: int) -> tuple[float, ...]:
    if count == 1:
        return (low,)
    log_low = math.log10(low)
    log_high = math.log10(high)
    return tuple(10.0 ** (log_low + (log_high - log_low) * i / (count - 1)) for i in range(count))


def _parse_expression(expression: str, sweep_variable: str, constants: dict) -> Expr:
    try:
        parsed = ast.parse(str(expression), mode="eval")
    except SyntaxError as exc:
        raise UnsupportedExpression(f"could not parse expression: {exc}") from exc
    const_values = dict(_BUILTIN_CONSTANTS)
    for key, value in constants.items():
        const_values[str(key)] = float(value)
    return _from_ast(parsed.body, sweep_variable, const_values)


def _from_ast(node: ast.AST, sweep_variable: str, constants: dict[str, float]) -> Expr:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return Constant(_constant_text(node.value), float(node.value))
    if isinstance(node, ast.Name):
        if node.id == sweep_variable:
            return Variable(node.id)
        if node.id in constants:
            return Constant(node.id, float(constants[node.id]))
        return UnknownParameter(node.id)
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return Unary("neg", _from_ast(node.operand, sweep_variable, constants))
        if isinstance(node.op, ast.UAdd):
            return Unary("pos", _from_ast(node.operand, sweep_variable, constants))
    if isinstance(node, ast.BinOp):
        op = _binop_name(node.op)
        return Binary(
            op,
            _from_ast(node.left, sweep_variable, constants),
            _from_ast(node.right, sweep_variable, constants),
        )
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise UnsupportedExpression("only direct function calls are supported")
        if len(node.args) != 1 or node.keywords:
            raise UnsupportedExpression("only one-argument function calls are supported")
        name = node.func.id
        if name not in _FUNCTIONS:
            raise UnsupportedExpression(f"unsupported function {name!r}")
        return Unary(name, _from_ast(node.args[0], sweep_variable, constants))
    raise UnsupportedExpression(f"unsupported expression node {type(node).__name__}")


def _binop_name(op: ast.operator) -> str:
    if isinstance(op, ast.Add):
        return "add"
    if isinstance(op, ast.Sub):
        return "sub"
    if isinstance(op, ast.Mult):
        return "mul"
    if isinstance(op, ast.Div):
        return "div"
    if isinstance(op, ast.Pow):
        return "pow"
    raise UnsupportedExpression(f"unsupported binary operator {type(op).__name__}")


def _constant_text(value: int | float) -> str:
    if isinstance(value, int):
        return str(value)
    if math.isfinite(value) and abs(value - round(value)) <= 0.0:
        return str(int(round(value)))
    return _format_float(float(value))


def _collect_sites(expr: Expr, sweep: Sweep, include_samples: bool) -> list[dict]:
    sites: list[dict] = []

    def walk(node: Expr, path: str):
        if isinstance(node, Binary):
            if node.op == "sub":
                sites.append(_classify_subtraction(node, path, sweep, include_samples))
            walk(node.left, f"{path}.left")
            walk(node.right, f"{path}.right")
        elif isinstance(node, Unary):
            walk(node.value, f"{path}.arg")

    walk(expr, "root")
    return sites


def _unknown_parameters(expr: Expr) -> list[str]:
    out = set()

    def walk(node: Expr):
        if isinstance(node, UnknownParameter):
            out.add(node.name)
        elif isinstance(node, Unary):
            walk(node.value)
        elif isinstance(node, Binary):
            walk(node.left)
            walk(node.right)

    walk(expr)
    return sorted(out)


def _classify_subtraction(node: Binary, path: str, sweep: Sweep, include_samples: bool) -> dict:
    left_text = node.left.render()
    right_text = node.right.render()
    unknown_parameters = sorted(
        set(_unknown_parameters(node.left)) | set(_unknown_parameters(node.right))
    )
    if node.left.structural_key() == node.right.structural_key():
        return {
            "path": path,
            "operator": "sub",
            "left": left_text,
            "right": right_text,
            "unknown_parameters": unknown_parameters,
            "pattern": "self_cancellation",
            "severity": "structural_zero",
            "probe_used": False,
            "left_leading_constant": None,
            "right_leading_constant": None,
            "leading_constant_gap": 0.0,
            "signal_exponent": "zero",
            "signal_coefficient": 0.0,
            "predicted_precision_crossing_epsilon": None,
            "sterbenz_window": True,
            "fit_quality": {"r2": 1.0, "slope_raw": 0.0},
            "residual_order_evidence": {
                "status": "STRUCTURAL_ZERO",
                "selected_model_name": "order_0",
                "selected_order": "zero",
                "order_stability": "structural_exact",
                "segment_evidence": [],
                "comparison_kind": "residual_order",
            },
            "account_probe_status": "structural_exact",
            "route_hint": "collapse_symbolically_before_arithmetic",
        }

    probe = _probe_subtraction(node, sweep)
    if not probe["ok"]:
        return {
            "path": path,
            "operator": "sub",
            "left": left_text,
            "right": right_text,
            "unknown_parameters": unknown_parameters,
            "pattern": "unrecognised",
            "severity": "needs_empirical_refinery",
            "probe_used": True,
            "probe_error": probe["error"],
            "left_leading_constant": None,
            "right_leading_constant": None,
            "leading_constant_gap": None,
            "signal_exponent": None,
            "signal_coefficient": None,
            "predicted_precision_crossing_epsilon": None,
            "sterbenz_window": None,
            "fit_quality": {"r2": None, "slope_raw": None},
            "residual_order_evidence": {
                "status": "SLOPE_FLOW_UNAVAILABLE",
                "selected_model_name": None,
                "selected_order": None,
                "order_stability": "indeterminate",
                "segment_evidence": [],
                "comparison_kind": "residual_order",
            },
            "account_probe_status": "unavailable",
            "route_hint": "run_operand_residue_trace_or_declare_constants",
        }

    left_constant = probe["left_constant"]
    right_constant = probe["right_constant"]
    gap = abs(left_constant - right_constant)
    same_constant = _close(left_constant, right_constant)
    signal_exponent = probe["signal_exponent"]
    exponent_fraction = probe["exponent_fraction"]
    coefficient = probe["coefficient"]
    leading_scale = max(abs(left_constant), abs(right_constant))
    sterbenz_window = _sterbenz_window(left_constant, right_constant)

    if same_constant and leading_scale > 0.0:
        if float(exponent_fraction) >= 0.95:
            pattern = "sterbenz_safe_catastrophic"
            severity = "catastrophic"
            route_hint = "rewrite_before_binary64_or_raise_precision_budget"
        else:
            pattern = "sterbenz_safe_benign"
            severity = "benign"
            route_hint = "direct_route_is_probably_clean_enough_with_bacl_monitor"
    elif same_constant:
        pattern = "zero_base_cancellation"
        severity = "algebraic_simplification"
        route_hint = "simplify_zero_base_terms_before_numeric_routing"
    else:
        pattern = "non_cancelling_subtraction"
        severity = "low"
        route_hint = "ordinary_subtraction_route"

    # Scale-free cancellation guard. The leading-constant test above is anchored
    # at the sweep variable = 0 and cannot see cancellation between operands that
    # grow with the sweep (e.g. sqrt(x+1)-sqrt(x) or sqrt(x*x+1)-x as x->inf).
    # The subtraction condition number, read from the sampled sweep, catches it
    # at any scale. This block only PROMOTES a low call to catastrophic
    # (never demotes), so it cannot create a new under-call; at worst it
    # over-refers to the exact path, which is the safe direction for a pre-read.
    # Restricted to the "low"/non_cancelling class (operands with DIFFERENT
    # leading constants at the x=0 anchor), which is exactly where the
    # growing-operand blind spot lives. The deliberate "benign" partial-
    # cancellation class (same leading constant, residual exponent < 0.95, e.g.
    # (1+sqrt(eps))-1) already routes direct-with-BACL-monitoring and is left to
    # that policy on purpose, not silently overridden here.
    max_condition = probe.get("max_condition_number", 0.0)
    if severity == "low" and max_condition >= _CONDITION_CATASTROPHIC:
        pattern = "sterbenz_safe_catastrophic"
        severity = "catastrophic"
        route_hint = "rewrite_before_binary64_or_raise_precision_budget"

    site = {
        "path": path,
        "operator": "sub",
        "left": left_text,
        "right": right_text,
        "unknown_parameters": unknown_parameters,
        "pattern": pattern,
        "severity": severity,
        "probe_used": True,
        "left_leading_constant": left_constant,
        "right_leading_constant": right_constant,
        "leading_constant_gap": gap,
        "signal_exponent": signal_exponent,
        "signal_coefficient": coefficient,
        "signal_signed_coefficient": probe["signed_coefficient"],
        "residual_order_evidence": probe["residual_order_evidence"],
        "operand_perturbation": probe["operand_perturbation"],
        "predicted_precision_crossing_epsilon": _crossing_epsilon(
            leading_scale,
            coefficient,
            exponent_fraction,
            same_constant,
        ),
        "sterbenz_window": sterbenz_window,
        "fit_quality": probe["fit_quality"],
        "account_probe_status": probe["account_status"],
        "route_hint": route_hint,
    }
    if include_samples:
        site["probe_samples"] = probe["samples"]
    return site


def _probe_subtraction(node: Binary, sweep: Sweep) -> dict:
    try:
        left_constant = _leading_constant(node.left, sweep)
        right_constant = _leading_constant(node.right, sweep)
        diff_values = []
        left_offsets = []
        right_offsets = []
        samples = []
        account_count = 0
        for point in sweep.points:
            env = {sweep.variable: point}
            left_value = node.left.evaluate(env)
            right_value = node.right.evaluate(env)
            diff = left_value - right_value
            if math.isfinite(diff):
                diff_values.append((point, diff))
            left_offset = left_value - left_constant
            right_offset = right_value - right_constant
            if math.isfinite(left_offset):
                left_offsets.append((point, left_offset))
            if math.isfinite(right_offset):
                right_offsets.append((point, right_offset))
            if math.isfinite(left_value) and math.isfinite(right_value) and math.isfinite(diff):
                sample = {
                    "sweep": point,
                    "left": left_value,
                    "right": right_value,
                    "difference": diff,
                    "abs_difference": abs(diff),
                }
                account = _exact_sample_account(node.left, node.right, sweep.variable, point, diff)
                if account is not None:
                    sample["exact_account"] = account
                    account_count += 1
                samples.append(sample)
        # Scale-free cancellation signal: the subtraction condition number
        # (|a|+|b|)/|a-b| over the sampled sweep. Large values mean the result
        # is a small difference of comparatively large operands, i.e. digits are
        # lost to cancellation regardless of where the operands sit at x=0.
        condition_numbers = []
        for _s in samples:
            _mag = abs(_s["left"]) + abs(_s["right"])
            _den = abs(_s["difference"])
            if _mag > 0.0:
                condition_numbers.append(_mag / _den if _den > 0.0 else 1.0e300)
        max_condition = max(condition_numbers) if condition_numbers else 0.0
        diff_observable = lambda x: node.left.evaluate({sweep.variable: x}) - node.right.evaluate({sweep.variable: x})
        left_observable = lambda x: node.left.evaluate({sweep.variable: x}) - left_constant
        right_observable = lambda x: node.right.evaluate({sweep.variable: x}) - right_constant
        fit = _sweep_power_profile(diff_values, diff_observable, sweep, "difference")
        left_fit = _sweep_power_profile(left_offsets, left_observable, sweep, "left_operand_perturbation")
        right_fit = _sweep_power_profile(right_offsets, right_observable, sweep, "right_operand_perturbation")
        return {
            "ok": True,
            "left_constant": left_constant,
            "right_constant": right_constant,
            "max_condition_number": max_condition,
            "samples": samples,
            "account_status": "exact_q_account" if samples and account_count == len(samples) else "float_telemetry_only",
            "residual_order_evidence": fit["residual_order_evidence"],
            "operand_perturbation": {
                "left": _perturbation_record(left_fit),
                "right": _perturbation_record(right_fit),
                "difference": _perturbation_record(fit),
            },
            **fit,
        }
    except (ArithmeticError, OverflowError, ValueError, UnsupportedExpression) as exc:
        return {"ok": False, "error": str(exc)}


def _exact_sample_account(left: Expr, right: Expr, sweep_variable: str, point: float, diff_float: float) -> dict | None:
    env = {sweep_variable: Fraction.from_float(point)}
    left_exact = _exact_arithmetic_value(left, env)
    right_exact = _exact_arithmetic_value(right, env)
    if left_exact is None or right_exact is None:
        return None
    difference_exact = left_exact - right_exact
    rounded_difference = Fraction.from_float(diff_float)
    residue = difference_exact - rounded_difference
    ulp = ulp_fraction(diff_float)
    residue_ulps = None if ulp == 0 else residue / ulp
    return {
        "status": "exact_q_account",
        "value_plus_account_equals_true_q": True,
        "left_exact": _fraction_text(left_exact),
        "right_exact": _fraction_text(right_exact),
        "difference_exact": _fraction_text(difference_exact),
        "rounded_difference": _fraction_text(rounded_difference),
        "rounding_residue": _fraction_text(residue),
        "rounding_residue_ulps": None if residue_ulps is None else _fraction_text(residue_ulps),
        "account_law": "rounded_difference + rounding_residue == difference_exact",
    }


def _exact_arithmetic_value(expr: Expr, env: dict[str, Fraction]) -> Fraction | None:
    if isinstance(expr, Constant):
        return Fraction.from_float(expr.value)
    if isinstance(expr, Variable):
        return env.get(expr.name)
    if isinstance(expr, UnknownParameter):
        return None
    if isinstance(expr, Unary):
        child = _exact_arithmetic_value(expr.value, env)
        if child is None:
            return None
        if expr.op == "neg":
            return -child
        if expr.op == "pos":
            return child
        return None
    if isinstance(expr, Binary):
        left = _exact_arithmetic_value(expr.left, env)
        right = _exact_arithmetic_value(expr.right, env)
        if left is None or right is None:
            return None
        if expr.op == "add":
            return left + right
        if expr.op == "sub":
            return left - right
        if expr.op == "mul":
            return left * right
        if expr.op == "div":
            if right == 0:
                return None
            return left / right
        if expr.op == "pow":
            if right.denominator != 1:
                return None
            exponent = int(right)
            if abs(exponent) > 64:
                return None
            return left ** exponent
    return None


def _leading_constant(expr: Expr, sweep: Sweep) -> float:
    try:
        value = expr.evaluate({sweep.variable: 0.0})
        if math.isfinite(value):
            return _snap_simple(value)
    except (ArithmeticError, OverflowError, ValueError, UnsupportedExpression):
        pass

    tiny = max(min(sweep.points) * 1.0e-6, 1.0e-300)
    value = expr.evaluate({sweep.variable: tiny})
    if not math.isfinite(value):
        raise ValueError("leading constant probe was not finite")
    return _snap_simple(value)


def _sweep_power_profile(
    values: list[tuple[float, float]],
    observable: Callable[[float], float],
    sweep: Sweep,
    label: str,
) -> dict:
    if _all_observed_values_zero(values):
        return _zero_power_profile(values, sweep, label)

    sweep_signature = sweep_signature_probe(
        observable,
        sweep.points,
        eta=1.0e-3,
        function_label=label,
        probe_id=f"residual_profile_{label}",
    )
    order_evidence = residual_order_from_sweep_signature(sweep_signature)
    selected_order = order_evidence.get("selected_order")
    exponent_source = order_evidence.get("order_source", "sweep_signature_probe_derivative_flow")
    if selected_order is None:
        fallback = _direct_residual_order_evidence(values)
        selected_order = fallback.get("selected_order") or fallback.get("reported_order")
        if selected_order is not None:
            derivative_evidence = order_evidence
            order_evidence = dict(fallback)
            order_evidence["sweep_signature_derivative_flow"] = derivative_evidence
            order_evidence["sweep_signature_status"] = sweep_signature.get("status")
            order_evidence["sweep_cancellation_grade"] = sweep_signature.get("cancellation_grade")
            order_evidence["sweep_drop_rate"] = sweep_signature.get("drop_rate")
        else:
            order_evidence["direct_value_flow_fallback"] = fallback
        order_evidence["reported_order"] = selected_order
        exponent_source = "direct_residual_slope_flow_fallback"
    if selected_order is None:
        return _indeterminate_power_profile(values, sweep_signature, order_evidence, label)

    fit = fit_power_law_signed(
        values,
        forced_exponent=selected_order,
        exponent_source=exponent_source,
    )
    fit["signal_exponent"] = selected_order
    fit["exponent_fraction"] = _order_fraction(selected_order)
    fit["sweep_signature_evidence"] = sweep_signature
    fit["residual_order_evidence"] = order_evidence
    fit["fit_quality"]["residual_order_source"] = exponent_source
    return fit


def _direct_residual_order_evidence(values: list[tuple[float, float]]) -> dict:
    observations = [
        (x, abs(y))
        for x, y in values
        if x > 0.0 and y != 0.0 and math.isfinite(x) and math.isfinite(y)
    ]
    evidence = residual_order_flow(observations)
    evidence["reported_order"] = evidence.get("selected_order")
    evidence["order_source"] = "direct_residual_slope_flow_fallback"
    return evidence


def _all_observed_values_zero(values: list[tuple[float, float]]) -> bool:
    finite = [y for _x, y in values if math.isfinite(y)]
    return bool(finite) and all(y == 0.0 for y in finite)


def _zero_power_profile(values: list[tuple[float, float]], sweep: Sweep, label: str) -> dict:
    sweep_signature = {
        "status": "sweep_signature_zero_observable",
        "cancellation_grade": 0.0,
        "drop_rate": 0.0,
        "n_input": len(sweep.points),
        "n_observed": 0,
        "transfers": [],
        "slope_observation": {
            "status": "SLOPE_ZERO_TRANSFER",
            "slope": None,
            "intercept": None,
            "r_squared": 1.0,
            "standard_error": None,
            "n_input_observations": len(values),
            "n_used": 0,
            "expression_path": f"residual_profile_{label}_zero_observable",
        },
    }
    order_evidence = {
        "status": "SLOPE_ZERO_TRANSFER",
        "selected_model_name": "order_0",
        "selected_order": "zero",
        "reported_order": "zero",
        "order_stability": "structural_stationary",
        "segment_evidence": [],
        "comparison_kind": "residual_order",
        "order_source": "zero_observable",
    }
    fit = fit_power_law_signed(values, expression_path=f"residual_profile_{label}_zero_observable")
    fit["signal_exponent"] = "zero"
    fit["exponent_fraction"] = Fraction(0, 1)
    fit["sweep_signature_evidence"] = sweep_signature
    fit["residual_order_evidence"] = order_evidence
    fit["fit_quality"]["residual_order_source"] = "zero_observable"
    return fit


def _indeterminate_power_profile(
    values: list[tuple[float, float]],
    sweep_signature: dict,
    order_evidence: dict,
    label: str,
) -> dict:
    fit = fit_power_law_signed(
        values,
        forced_exponent=Fraction(0, 1),
        exponent_source="indeterminate_residual_order_default_zero",
    )
    fit["signal_exponent"] = None
    fit["exponent_fraction"] = None
    fit["sweep_signature_evidence"] = sweep_signature
    fit["residual_order_evidence"] = order_evidence
    fit["fit_quality"]["residual_order_source"] = "indeterminate_residual_order_default_zero"
    fit["fit_quality"]["expression_path"] = f"residual_profile_{label}_indeterminate"
    return fit


def _perturbation_record(fit: dict) -> dict:
    return {
        "exponent": fit.get("signal_exponent"),
        "coefficient": fit.get("coefficient"),
        "signed_coefficient": fit.get("signed_coefficient"),
        "sweep_signature": {
            "status": (fit.get("sweep_signature_evidence") or {}).get("status"),
            "cancellation_grade": (fit.get("sweep_signature_evidence") or {}).get("cancellation_grade"),
            "drop_rate": (fit.get("sweep_signature_evidence") or {}).get("drop_rate"),
            "residual_rms": (fit.get("sweep_signature_evidence") or {}).get("residual_rms"),
            "residual_max_abs": (fit.get("sweep_signature_evidence") or {}).get("residual_max_abs"),
            "residual_relative_rms": (fit.get("sweep_signature_evidence") or {}).get("residual_relative_rms"),
        },
        "residual_order_evidence": fit.get("residual_order_evidence"),
        "fit_quality": fit.get("fit_quality", {"r2": fit.get("r2"), "slope_raw": fit.get("slope_raw")}),
    }


def _order_fraction(value: str | Fraction) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if value == "zero":
        return Fraction(0, 1)
    return Fraction(str(value))


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= 1.0e-9 * max(1.0, abs(a), abs(b))


def _sterbenz_window(a: float, b: float) -> bool:
    aa = abs(a)
    bb = abs(b)
    if aa == 0.0 and bb == 0.0:
        return True
    if aa == 0.0 or bb == 0.0:
        return False
    ratio = aa / bb
    return 0.5 <= ratio <= 2.0


def _crossing_epsilon(scale: float, coefficient: float, exponent: Fraction, same_constant: bool) -> str | None:
    if not same_constant or coefficient <= 0.0 or exponent <= 0:
        return None
    crossing = ((_MACHINE_EPSILON * max(scale, 1.0)) / coefficient) ** (1.0 / float(exponent))
    if not math.isfinite(crossing):
        return None
    return crossing


def _burden_vector(sites: list[dict]) -> dict:
    counts = {
        "subtraction_sites": len(sites),
        "self_cancellation_sites": 0,
        "catastrophic_sites": 0,
        "benign_sites": 0,
        "unrecognised_sites": 0,
        "ordinary_sites": 0,
        "micro_probe_sites": 0,
    }
    crossings = []
    constants = []
    for site in sites:
        pattern = site["pattern"]
        if site.get("probe_used"):
            counts["micro_probe_sites"] += 1
        if pattern == "self_cancellation":
            counts["self_cancellation_sites"] += 1
        elif pattern == "sterbenz_safe_catastrophic":
            counts["catastrophic_sites"] += 1
        elif pattern in ("sterbenz_safe_benign", "zero_base_cancellation"):
            counts["benign_sites"] += 1
        elif pattern == "unrecognised":
            counts["unrecognised_sites"] += 1
        else:
            counts["ordinary_sites"] += 1
        if site.get("predicted_precision_crossing_epsilon"):
            crossings.append(float(site["predicted_precision_crossing_epsilon"]))
        for key in ("left_leading_constant", "right_leading_constant"):
            if site.get(key) is not None:
                constants.append(abs(float(site[key])))
    dominant = "none"
    if counts["catastrophic_sites"]:
        dominant = "sterbenz_safe_catastrophic"
    elif counts["benign_sites"]:
        dominant = "sterbenz_safe_benign"
    elif counts["self_cancellation_sites"]:
        dominant = "self_cancellation"
    elif counts["ordinary_sites"]:
        dominant = "non_cancelling_subtraction"
    elif counts["unrecognised_sites"]:
        dominant = "unrecognised"
    return {
        **counts,
        "dominant_pattern": dominant,
        "min_predicted_crossing_epsilon": min(crossings) if crossings else None,
        "largest_leading_constant": max(constants) if constants else None,
    }


def _operation_shape(sites: list[dict]) -> str:
    if not sites:
        return "no_subtraction"
    patterns = {site["pattern"] for site in sites}
    if "sterbenz_safe_catastrophic" in patterns:
        return "catastrophic_cancellation"
    if patterns == {"self_cancellation"}:
        return "self_cancellation"
    if "unrecognised" in patterns:
        return "partly_unrecognised"
    if patterns <= {"sterbenz_safe_benign", "zero_base_cancellation", "self_cancellation"}:
        return "benign_cancellation"
    return "ordinary_subtraction"


def _recommended_process(operation_shape: str, sites: list[dict]) -> dict:
    if operation_shape == "no_subtraction":
        return {
            "primary": "direct_or_symbolic_sparse",
            "reason": "No subtraction site was present in the expression tree.",
            "next_tools": ["cella_symbolic_rational", "cella_arith_precision_budget"],
        }
    if operation_shape == "self_cancellation":
        return {
            "primary": "collapse_symbolically",
            "reason": "A structural x-x term can be eliminated before arithmetic.",
            "next_tools": ["cella_symbolic_equal", "cella_symbolic_rational"],
        }
    if operation_shape == "catastrophic_cancellation":
        return {
            "primary": "rewrite_before_evaluation",
            "reason": "A same-leading-constant subtraction exposes a linear-or-worse residual near the sweep endpoint.",
            "next_tools": ["cella_cleanliness_rank", "cella_bacl_dial", "cella_operand_residue_trace"],
            "route_hints": [site["route_hint"] for site in sites if site["severity"] == "catastrophic"],
        }
    if operation_shape == "benign_cancellation":
        return {
            "primary": "direct_with_bacl_monitor",
            "reason": "Same-leading-constant subtraction exists, but the residual opens with a fractional/benign exponent.",
            "next_tools": ["cella_bacl_pair", "cella_operand_residue_trace"],
        }
    if operation_shape == "partly_unrecognised":
        return {
            "primary": "declare_constants_or_empirical_refinery",
            "reason": "At least one subtraction site could not be probed from the declared expression graph.",
            "next_tools": ["cella_operand_residue_trace", "cella_refinery_compare"],
        }
    return {
        "primary": "ordinary_subtraction_route",
        "reason": "Subtractions do not share a leading constant at the declared sweep endpoint.",
        "next_tools": ["cella_arith_precision_budget"],
    }


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _snap_simple(value: float) -> float:
    if not math.isfinite(value):
        return value
    nearest = round(value)
    if abs(value - nearest) <= 1.0e-10 * max(1.0, abs(value)):
        return float(nearest)
    return value


def _format_float(value: float) -> str:
    if not math.isfinite(value):
        return str(value)
    value = _snap_simple(value)
    if abs(value - round(value)) <= 0.0:
        return str(int(round(value)))
    text = f"{value:.17g}"
    if "e" in text:
        mantissa, exponent = text.split("e", 1)
        return f"{mantissa}e{int(exponent):+d}"
    return text
