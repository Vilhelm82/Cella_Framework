"""BACL/refinery cleanliness diagnostics for Cella.

This module synthesizes the V4 BACL, early-absorption, refinery-burden, and
upsilon-lane ideas into a small MCP-suitable core. It is intentionally not a
CAS. It evaluates a restricted arithmetic expression tree using binary64
operations, while carrying the exact rational value of every binary64 operand
and intermediate.

The result is an operational-algebra diagnostic:

* BACL pair checks expose whether an additive/subtractive pair sits on the
  clean integer lattice of the coarser operand.
* Operand traces expose exact per-operation rounding residue.
* Burden vectors rank algebraically equivalent forms by lattice cleanliness
  before local roundoff size.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import math
from typing import Iterable

from .typed_ulp import ulp_fraction as _typed_ulp_fraction
from .typed_ulp import ulp_record as _typed_ulp_record

_LATTICE_RANK = {
    "integer_lattice": 0,
    "off_integer_lattice": 1,
    "non_integer_lattice": 1,
    "no_additive_lattice": 2,
    "unknown_lattice": 3,
}

_DEFAULT_COMPARE_DIMENSIONS = (
    "lattice_class",
    "max_integer_residual",
    "operation_chain_depth",
)


def _fraction_text(value: Fraction) -> str:
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _fraction_from_record(value) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("booleans are not burden scalars")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, str):
        return Fraction(value.strip())
    raise TypeError(f"expected exact burden scalar, got {type(value).__name__}")


def _looks_hex_float(text: str) -> bool:
    s = text.strip().lower()
    return s.startswith("0x") or s.startswith("+0x") or s.startswith("-0x")


def parse_binary64(value) -> float:
    """Parse a user-declared binary64 input.

    Strings may be Python hex floats, decimal floats, integers, or rational
    strings. Decimal strings are accepted here because these are operational
    IEEE diagnostics; the parsed binary64 is always reported back by hex and
    exact Fraction so the declaration is reproducible.
    """
    if isinstance(value, bool):
        raise TypeError("booleans are not binary64 inputs")
    if isinstance(value, float):
        out = value
    elif isinstance(value, int):
        out = float(value)
    elif isinstance(value, str):
        s = value.strip()
        if not s:
            raise ValueError("empty binary64 input")
        if _looks_hex_float(s):
            out = float.fromhex(s)
        elif "/" in s:
            out = float(Fraction(s))
        else:
            out = float(s)
    else:
        raise TypeError(f"expected binary64 scalar, got {type(value).__name__}")
    return float(out)


def _float_record(value: float) -> dict:
    return {
        "hex": value.hex(),
        "fraction": _fraction_text(Fraction.from_float(value)),
    }


def _ulp_record(value: float) -> dict:
    return _typed_ulp_record(value, precision="float64")


def _ulp_fraction(value: float) -> Fraction:
    return _typed_ulp_fraction(value, precision="float64")


def _nearest_integer_residual(value: Fraction) -> tuple[int, Fraction]:
    floor = value.numerator // value.denominator
    candidates = (floor, floor + 1)
    nearest = min(candidates, key=lambda n: (abs(value - n), abs(n)))
    return nearest, abs(value - nearest)


def _bacl_pair_from_floats(a: float, b: float) -> dict:
    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError("BACL requires finite binary64 inputs")
    qa = Fraction.from_float(a)
    qb = Fraction.from_float(b)
    ulp_a = _ulp_fraction(a)
    ulp_b = _ulp_fraction(b)
    lattice_index = (qa - qb) / ulp_b
    nearest, integer_residual = _nearest_integer_residual(lattice_index)
    lattice_class = "integer_lattice" if integer_residual == 0 else "off_integer_lattice"
    theorem_hypothesis = ulp_a >= ulp_b
    return {
        "precision": "binary64",
        "a": _float_record(a),
        "b": _float_record(b),
        "ulp_a": _fraction_text(ulp_a),
        "ulp_b": _fraction_text(ulp_b),
        "delta": _fraction_text(qa - qb),
        "lattice_index": _fraction_text(lattice_index),
        "nearest_integer": str(nearest),
        "integer_residual": _fraction_text(integer_residual),
        "lattice_class": lattice_class,
        "theorem_hypothesis": theorem_hypothesis,
        "theorem_protected": theorem_hypothesis and lattice_class == "integer_lattice",
        "method": "BACL_binary64_integer_lattice_index",
    }


def bacl_pair(a, b, precision: str = "binary64") -> dict:
    if precision != "binary64":
        raise ValueError("only precision='binary64' is currently supported")
    return _bacl_pair_from_floats(parse_binary64(a), parse_binary64(b))


@dataclass(frozen=True)
class _NodeValue:
    text: str
    float_value: float
    exact_value: Fraction
    depth: int


@dataclass(frozen=True)
class _EntryBuild:
    record: dict
    rounding_abs_ulps: Fraction
    bacl_integer_residual: Fraction | None


def _residue_in_ulps(residue: Fraction, result: float) -> Fraction:
    return residue / _ulp_fraction(result)


def _operation_entry(
    op_index: int,
    op: str,
    left: _NodeValue,
    right: _NodeValue,
    result_float: float,
    result_exact: Fraction,
) -> _EntryBuild:
    if not math.isfinite(result_float):
        raise ValueError(f"{op} produced a non-finite binary64 result")
    rounded_q = Fraction.from_float(result_float)
    residue = result_exact - rounded_q
    residual_ulps = _residue_in_ulps(residue, result_float)
    _nearest, rounding_integer_residual = _nearest_integer_residual(residual_ulps)

    bacl = None
    bacl_residual = None
    if op == "add":
        bacl = _bacl_pair_from_floats(left.float_value, -right.float_value)
        bacl_residual = Fraction(bacl["integer_residual"])
    elif op == "sub":
        bacl = _bacl_pair_from_floats(left.float_value, right.float_value)
        bacl_residual = Fraction(bacl["integer_residual"])

    record = {
        "op_index": str(op_index),
        "op": op,
        "expression": f"({left.text} {op} {right.text})",
        "left": _float_record(left.float_value),
        "right": _float_record(right.float_value),
        "result": _float_record(result_float),
        "exact_result": _fraction_text(result_exact),
        "rounded_result": _fraction_text(rounded_q),
        "rounding_residual": _fraction_text(residue),
        "rounding_residual_ulps": _fraction_text(residual_ulps),
        "rounding_integer_residual": _fraction_text(rounding_integer_residual),
        "bacl_pair": bacl,
    }
    return _EntryBuild(
        record=record,
        rounding_abs_ulps=abs(residual_ulps),
        bacl_integer_residual=bacl_residual,
    )


def _validate_variables(variables: Iterable[str]) -> tuple[str, ...]:
    out = tuple(str(v) for v in variables)
    if len(set(out)) != len(out):
        raise ValueError("variables must be distinct")
    for name in out:
        if not name.isidentifier() or name.startswith("_"):
            raise ValueError(f"invalid variable name {name!r}")
    return out


def _constant_node(value) -> _NodeValue:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"unsupported expression constant {value!r}")
    f = float(value)
    if not math.isfinite(f):
        raise ValueError("expression constants must be finite")
    return _NodeValue(text=repr(value), float_value=f, exact_value=Fraction.from_float(f), depth=0)


def _eval_node(node: ast.AST, env: dict[str, _NodeValue], entries: list[_EntryBuild]) -> _NodeValue:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, env, entries)
    if isinstance(node, ast.Name):
        if node.id not in env:
            raise ValueError(f"unknown variable {node.id!r}")
        return env[node.id]
    if isinstance(node, ast.Constant):
        return _constant_node(node.value)
    if isinstance(node, ast.UnaryOp):
        child = _eval_node(node.operand, env, entries)
        if isinstance(node.op, ast.UAdd):
            return child
        if isinstance(node.op, ast.USub):
            return _NodeValue(
                text=f"-({child.text})",
                float_value=-child.float_value,
                exact_value=-child.exact_value,
                depth=child.depth,
            )
        raise ValueError("unsupported unary operator")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, env, entries)
        right = _eval_node(node.right, env, entries)
        if isinstance(node.op, ast.Add):
            op = "add"
            result_float = left.float_value + right.float_value
            result_exact = left.exact_value + right.exact_value
        elif isinstance(node.op, ast.Sub):
            op = "sub"
            result_float = left.float_value - right.float_value
            result_exact = left.exact_value - right.exact_value
        elif isinstance(node.op, ast.Mult):
            op = "mul"
            result_float = left.float_value * right.float_value
            result_exact = left.exact_value * right.exact_value
        elif isinstance(node.op, ast.Div):
            op = "div"
            if right.float_value == 0.0 or right.exact_value == 0:
                raise ZeroDivisionError("division by zero in operand trace")
            result_float = left.float_value / right.float_value
            result_exact = left.exact_value / right.exact_value
        elif isinstance(node.op, ast.Pow):
            if right.exact_value.denominator != 1:
                raise ValueError("only integer powers are supported")
            exponent = int(right.exact_value)
            if abs(exponent) > 64:
                raise ValueError("integer power magnitude is capped at 64 for trace readability")
            op = "pow"
            result_float = left.float_value ** exponent
            result_exact = left.exact_value ** exponent
        else:
            raise ValueError("unsupported binary operator")
        idx = len(entries)
        entries.append(_operation_entry(idx, op, left, right, result_float, result_exact))
        try:
            text = ast.unparse(node)
        except Exception:  # pragma: no cover - fallback for older runtimes
            text = entries[-1].record["expression"]
        return _NodeValue(text=text, float_value=result_float, exact_value=result_exact, depth=max(left.depth, right.depth) + 1)
    raise ValueError(f"unsupported expression node {type(node).__name__}")


def _coerce_values(variables: tuple[str, ...], values) -> dict[str, _NodeValue]:
    if isinstance(values, dict):
        missing = [v for v in variables if v not in values]
        if missing:
            raise ValueError(f"missing values for variables {missing}")
        raw = {v: values[v] for v in variables}
    else:
        if len(values) != len(variables):
            raise ValueError("values length must match variables")
        raw = dict(zip(variables, values))
    out = {}
    for name, declared in raw.items():
        f = parse_binary64(declared)
        if not math.isfinite(f):
            raise ValueError(f"{name} is not finite")
        out[name] = _NodeValue(
            text=name,
            float_value=f,
            exact_value=Fraction.from_float(f),
            depth=0,
        )
    return out


def operand_residue_trace(expression: str, variables, values, precision: str = "binary64") -> dict:
    if precision != "binary64":
        raise ValueError("only precision='binary64' is currently supported")
    vars_tuple = _validate_variables(variables)
    entries: list[_EntryBuild] = []
    env = _coerce_values(vars_tuple, values)
    tree = ast.parse(str(expression), mode="eval")
    root = _eval_node(tree, env, entries)

    rounded_final = Fraction.from_float(root.float_value)
    final_residue = root.exact_value - rounded_final
    final_residue_ulps = _residue_in_ulps(final_residue, root.float_value)
    final_abs_ulps = abs(final_residue_ulps)

    bacl_residuals = [e.bacl_integer_residual for e in entries if e.bacl_integer_residual is not None]
    max_bacl = max(bacl_residuals, default=Fraction(0))
    off_lattice_ops = sum(1 for r in bacl_residuals if r != 0)
    max_rounding = max([e.rounding_abs_ulps for e in entries] + [final_abs_ulps], default=Fraction(0))
    lattice_class = "integer_lattice" if max_bacl == 0 else "off_integer_lattice"
    if not bacl_residuals:
        lattice_class = "no_additive_lattice"

    return {
        "expression": str(expression),
        "precision": precision,
        "variables": list(vars_tuple),
        "inputs": {name: _float_record(env[name].float_value) for name in vars_tuple},
        "result": _float_record(root.float_value),
        "exact_result": _fraction_text(root.exact_value),
        "rounded_result": _fraction_text(rounded_final),
        "global_rounding_residual": _fraction_text(final_residue),
        "global_rounding_residual_ulps": _fraction_text(final_residue_ulps),
        "operation_chain_depth": str(len(entries)),
        "entries": [e.record for e in entries],
        "diagnostics": {
            "lattice_class": lattice_class,
            "additive_ops": str(len(bacl_residuals)),
            "off_lattice_additive_ops": str(off_lattice_ops),
            "max_bacl_integer_residual": _fraction_text(max_bacl),
            "rounding_residual_max_ulp": _fraction_text(max_rounding),
            "final_rounding_residual_abs_ulp": _fraction_text(final_abs_ulps),
            "coverage_class": "exact_rational_binary64_ops",
        },
    }


def _rank_for_dimension(dimension: str, value):
    if dimension == "lattice_class":
        return _LATTICE_RANK.get(str(value), 3)
    if dimension in {
        "max_integer_residual",
        "operation_chain_depth",
        "rounding_residual_max_ulp",
        "final_rounding_residual_abs_ulp",
        "b_k_point_estimate",
    }:
        return _fraction_from_record(value)
    if dimension == "calibration_zero_preserved":
        return 0 if bool(value) else 1
    return str(value)


def _compare_dimension(dimension: str, reference_value, candidate_value) -> str:
    ref_rank = _rank_for_dimension(dimension, reference_value)
    cand_rank = _rank_for_dimension(dimension, candidate_value)
    if type(ref_rank) is not type(cand_rank):
        return "indeterminate"
    if cand_rank < ref_rank:
        return "candidate_better"
    if cand_rank > ref_rank:
        return "candidate_worse"
    return "tied"


def _default_dimensions(reference_burden: dict, candidate_burden: dict) -> list[str]:
    out = [d for d in _DEFAULT_COMPARE_DIMENSIONS if d in reference_burden and d in candidate_burden]
    extras = sorted(
        d for d in set(reference_burden) & set(candidate_burden)
        if d not in out and d in {"rounding_residual_max_ulp", "final_rounding_residual_abs_ulp"}
    )
    return out + extras


def refinery_compare(reference: dict, candidate: dict, dimensions: list[str] | None = None) -> dict:
    ref_geometry = dict(reference.get("geometry", {}))
    cand_geometry = dict(candidate.get("geometry", {}))
    ref_burden = dict(reference.get("burden", {}))
    cand_burden = dict(candidate.get("burden", {}))
    dims = [str(d) for d in (dimensions or _default_dimensions(ref_burden, cand_burden))]
    missing = [d for d in dims if d not in ref_burden or d not in cand_burden]
    if missing:
        raise ValueError(f"missing burden dimensions {missing}")

    admissible = ref_geometry == cand_geometry
    dimension_results = {
        dim: _compare_dimension(dim, ref_burden[dim], cand_burden[dim])
        for dim in dims
    }
    any_better = any(v == "candidate_better" for v in dimension_results.values())
    any_worse = any(v == "candidate_worse" for v in dimension_results.values())
    any_indeterminate = any(v == "indeterminate" for v in dimension_results.values())

    if not admissible:
        decision = "rejected"
        reason = "geometry_admissibility_failed"
    elif any_indeterminate:
        decision = "indeterminate"
        reason = "at_least_one_dimension_indeterminate"
    elif any_worse:
        decision = "rejected"
        reason = "candidate_regresses_at_least_one_dimension"
    elif any_better:
        decision = "accepted"
        reason = "same_geometry_componentwise_lower_burden"
    else:
        decision = "tied"
        reason = "same_geometry_equal_burden"

    return {
        "reference_name": str(reference.get("name", "reference")),
        "candidate_name": str(candidate.get("name", "candidate")),
        "admissible": admissible,
        "dimensions": dims,
        "dimension_results": dimension_results,
        "decision": decision,
        "decision_reason": reason,
        "reference_burden": ref_burden,
        "candidate_burden": cand_burden,
    }


def _grid_samples(variables: tuple[str, ...], grid: dict) -> list[dict]:
    axes = []
    for name in variables:
        if name not in grid:
            raise ValueError(f"grid missing variable {name!r}")
        values = grid[name]
        if isinstance(values, (str, int, float)):
            values = [values]
        if not values:
            raise ValueError(f"grid variable {name!r} has no samples")
        axes.append(list(values))
    return [dict(zip(variables, sample)) for sample in product(*axes)]


def _aggregate_form(expression: str, variables: tuple[str, ...], samples: list[dict]) -> tuple[dict, list[dict]]:
    traces = [operand_residue_trace(expression, variables, sample) for sample in samples]
    exact_results = {trace["exact_result"] for trace in traces}
    max_integer = max(Fraction(t["diagnostics"]["max_bacl_integer_residual"]) for t in traces)
    max_rounding = max(Fraction(t["diagnostics"]["rounding_residual_max_ulp"]) for t in traces)
    max_final = max(Fraction(t["diagnostics"]["final_rounding_residual_abs_ulp"]) for t in traces)
    depth = max(int(t["operation_chain_depth"]) for t in traces)
    off_samples = sum(1 for t in traces if Fraction(t["diagnostics"]["max_bacl_integer_residual"]) != 0)
    mean_final = sum(Fraction(t["diagnostics"]["final_rounding_residual_abs_ulp"]) for t in traces) / len(traces)
    burden = {
        "lattice_class": "integer_lattice" if max_integer == 0 else "off_integer_lattice",
        "max_integer_residual": _fraction_text(max_integer),
        "operation_chain_depth": str(depth),
        "rounding_residual_max_ulp": _fraction_text(max_rounding),
        "final_rounding_residual_abs_ulp": _fraction_text(max_final),
        "b_k_point_estimate": _fraction_text(mean_final),
        "off_lattice_samples": f"{off_samples}/{len(traces)}",
        "sample_count": str(len(traces)),
        "exact_result_classes": str(len(exact_results)),
    }
    return burden, traces


def _dial_sort_key(name: str, burden: dict) -> tuple:
    return (
        _LATTICE_RANK.get(burden["lattice_class"], 3),
        Fraction(burden["max_integer_residual"]),
        Fraction(burden["operation_chain_depth"]),
        Fraction(burden["rounding_residual_max_ulp"]),
        name,
    )


def cleanliness_rank(
    variables,
    forms: list[dict],
    grid: dict,
    dimensions: list[str] | None = None,
) -> dict:
    vars_tuple = _validate_variables(variables)
    samples = _grid_samples(vars_tuple, grid)
    if not forms:
        raise ValueError("at least one form is required")

    burden_vectors = {}
    trace_examples = {}
    traces_by_form = {}
    geometry = {"variables": list(vars_tuple), "grid_sample_count": str(len(samples))}
    for form in forms:
        name = str(form["name"])
        expression = str(form["expression"])
        if name in burden_vectors:
            raise ValueError(f"duplicate form name {name!r}")
        burden, traces = _aggregate_form(expression, vars_tuple, samples)
        burden_vectors[name] = burden
        trace_examples[name] = traces[0]
        traces_by_form[name] = traces

    equivalence_failures = []
    for sample_index in range(len(samples)):
        exact_by_form = {
            name: traces_by_form[name][sample_index]["exact_result"]
            for name in burden_vectors
        }
        if len(set(exact_by_form.values())) != 1:
            equivalence_failures.append({
                "sample_index": str(sample_index),
                "sample": {
                    var: _float_record(parse_binary64(samples[sample_index][var]))
                    for var in vars_tuple
                },
                "exact_results": exact_by_form,
            })
    if equivalence_failures:
        raise ValueError(
            "forms are not exact-real equivalent on the declared grid; "
            f"first failure: {equivalence_failures[0]}"
        )

    dominated = {name: [] for name in burden_vectors}
    dominated_by = {name: [] for name in burden_vectors}
    comparisons = {}
    names = list(burden_vectors)
    for candidate_name in names:
        for reference_name in names:
            if candidate_name == reference_name:
                continue
            comparison = refinery_compare(
                {
                    "name": reference_name,
                    "geometry": geometry,
                    "burden": burden_vectors[reference_name],
                },
                {
                    "name": candidate_name,
                    "geometry": geometry,
                    "burden": burden_vectors[candidate_name],
                },
                dimensions=dimensions,
            )
            comparisons[f"{candidate_name}__vs__{reference_name}"] = comparison
            if comparison["decision"] == "accepted":
                dominated[candidate_name].append(reference_name)
                dominated_by[reference_name].append(candidate_name)

    frontier = [name for name in names if not dominated_by[name]]
    dial_origin = min(names, key=lambda n: _dial_sort_key(n, burden_vectors[n]))
    return {
        "variables": list(vars_tuple),
        "forms": [{"name": str(f["name"]), "expression": str(f["expression"])} for f in forms],
        "burden_vectors": burden_vectors,
        "pareto_frontier": frontier,
        "dominated": dominated,
        "dominated_by": dominated_by,
        "pairwise_comparisons": comparisons,
        "dial_origin": dial_origin,
        "dial_origin_burden": burden_vectors[dial_origin],
        "sample_equivalence": "verified_exact_real_equivalence_on_declared_grid",
        "trace_examples": trace_examples,
        "method": "BACL_lattice_burden_plus_componentwise_refinery",
    }


def bacl_dial(variables, terms: list[dict], grid: dict, dimensions: list[str] | None = None) -> dict:
    if len(terms) != 3:
        raise ValueError("bacl_dial currently requires exactly three terms")
    generated = []
    pair_by_name = {}
    for i, j in ((0, 1), (0, 2), (1, 2)):
        k = ({0, 1, 2} - {i, j}).pop()
        first = terms[i]
        second = terms[j]
        last = terms[k]
        labels = [str(first["label"]), str(second["label"])]
        name = f"pair_{labels[0]}_{labels[1]}_then_{last['label']}"
        expression = f"(({first['expression']}) + ({second['expression']})) + ({last['expression']})"
        generated.append({"name": name, "expression": expression, "first_pair": labels})
        pair_by_name[name] = labels
    ranking = cleanliness_rank(variables, generated, grid, dimensions=dimensions)
    origin = ranking["dial_origin"]
    return {
        "generated_forms": generated,
        "dial_origin": origin,
        "dial_origin_pair": pair_by_name[origin],
        "ranking": ranking,
        "method": "three_term_pair_first_BACL_absorption_dial",
    }
