"""Hostile benchmark harness for the internal Cella Pathfinder thesis.

This is deliberately not an MCP tool. It is a repo-local campaign runner that
compares Cella's internal route choices against direct Cella and conventional
baselines on a frozen manifest.
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from .campaign import corner_frontface, diag_germ_classifier
from .pathfinder import route_plan
from .residual_profile import residual_profile
from .symbolic import symbolic_rational


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MANIFEST = REPO_ROOT / "benchmarks" / "pathfinder_hostile" / "manifest.json"


def load_manifest(path: str | Path = DEFAULT_MANIFEST) -> dict:
    manifest_path = Path(path)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    for key in ("campaign", "version", "cases"):
        if key not in data:
            raise ValueError(f"manifest missing required key {key!r}")
    if not isinstance(data["cases"], list) or not data["cases"]:
        raise ValueError("manifest cases must be a nonempty list")
    seen = set()
    for case in data["cases"]:
        for key in ("id", "family", "kind", "input", "expect"):
            if key not in case:
                raise ValueError(f"case missing required key {key!r}: {case!r}")
        case_id = str(case["id"])
        if case_id in seen:
            raise ValueError(f"duplicate case id {case_id!r}")
        seen.add(case_id)
    data["_manifest_path"] = str(manifest_path)
    return data


def run_manifest(path: str | Path = DEFAULT_MANIFEST, output_path: str | Path | None = None) -> dict:
    manifest = load_manifest(path)
    cases = []
    for case in manifest["cases"]:
        cases.append(_run_case(case))
    report = {
        "campaign": manifest["campaign"],
        "version": manifest["version"],
        "manifest_path": manifest["_manifest_path"],
        "summary": _summary(cases),
        "cases": cases,
    }
    if output_path is not None:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _run_case(case: dict) -> dict:
    engines = {
        "cella_pathfinder": _timed(lambda: run_cella_pathfinder(case)),
        "cella_direct": _timed(lambda: run_cella_direct(case)),
        "sympy_naive": _timed(lambda: run_sympy_naive(case)),
        "mpmath_naive": _timed(lambda: run_mpmath_naive(case)),
        "flint_arb": _timed(lambda: run_flint_arb(case)),
    }
    return {
        "id": str(case["id"]),
        "family": str(case["family"]),
        "kind": str(case["kind"]),
        "source": str(case.get("source", "")),
        "engines": engines,
    }


def _timed(fn) -> dict:
    start = time.perf_counter()
    try:
        result = fn()
    except Exception as exc:
        result = {
            "status": "fail",
            "reason": f"{type(exc).__name__}: {exc}",
        }
    elapsed_ms = round((time.perf_counter() - start) * 1000, 3)
    result = _jsonify(result)
    result["elapsed_ms"] = elapsed_ms
    return result


def run_cella_pathfinder(case: dict) -> dict:
    kind = str(case["kind"])
    data = dict(case["input"])
    expect = dict(case.get("expect", {}))

    if kind == "route_expression":
        route = route_plan(
            str(data["expression"]),
            data["sweep"],
            constants=data.get("constants", {}),
        )
        return _status(
            route.get("decision") == expect.get("decision"),
            route=route,
            reason=f"expected decision {expect.get('decision')!r}",
        )

    if kind == "symbolic_rational":
        record = symbolic_rational(str(data["expression"]), data["variables"])
        return _status(
            record.get("method") == expect.get("method"),
            symbolic=record,
            route={
                "decision": "symbolic_normal_form",
                "why": "Use Cella sparse rational-function records instead of expanded global algebra.",
            },
        )

    if kind == "local_germ":
        record = diag_germ_classifier(str(data["coordinate"]), data["native"], data["transverse"])
        ok = record.get("kind") == expect.get("kind")
        if "coefficient_text" in expect:
            ok = ok and record.get("coefficient_text") == expect["coefficient_text"]
        if "order" in expect:
            ok = ok and _text(record.get("order")) == str(expect["order"])
        return _status(ok, local_germ=record)

    if kind == "corner_frontface":
        record = corner_frontface(
            face_data=data.get("face_data"),
            weights=data.get("weights"),
            path=data.get("path"),
        )
        ok = _text(record.get("support_order")) == str(expect.get("support_order"))
        return _status(ok, corner=record)

    if kind == "dbp_overlay":
        route = route_plan(
            "eps",
            {"variable": "eps", "low": "1e-12", "high": "1e-4"},
            domain=data["domain"],
            geometry=data["geometry"],
        )
        overlay = route.get("geometry_overlay", {})
        ok = True
        for key, expected in expect.items():
            if key == "q":
                ok = ok and overlay.get("regularity", {}).get("q") == expected
            else:
                ok = ok and overlay.get(key) == expected
        return _status(ok, overlay=overlay, route=route)

    if kind == "reserved_limit":
        return {
            "status": "limit",
            "reason": str(data.get("reason", "period/residue lane is reserved for a future deterministic fixture")),
        }

    if kind == "verification_script":
        return _run_verification_script(data, expect)

    return {"status": "limit", "reason": f"no Pathfinder adapter for case kind {kind!r}"}


def run_cella_direct(case: dict) -> dict:
    kind = str(case["kind"])
    data = dict(case["input"])

    if kind == "route_expression":
        profile = residual_profile(
            str(data["expression"]),
            data["sweep"],
            constants=data.get("constants", {}),
        )
        return {
            "status": "pass",
            "operation_shape": profile.get("operation_shape"),
            "note": "Direct profile has telemetry but no higher Pathfinder route contract.",
        }

    if kind == "symbolic_rational":
        return {"status": "pass", "symbolic": symbolic_rational(str(data["expression"]), data["variables"])}

    if kind == "local_germ":
        return {
            "status": "pass",
            "local_germ": diag_germ_classifier(str(data["coordinate"]), data["native"], data["transverse"]),
        }

    if kind == "corner_frontface":
        return {
            "status": "pass",
            "corner": corner_frontface(
                face_data=data.get("face_data"),
                weights=data.get("weights"),
                path=data.get("path"),
            ),
        }

    if kind in {"dbp_overlay", "reserved_limit", "verification_script"}:
        return {
            "status": "limit",
            "reason": "Direct Cella primitive path has no internal Pathfinder overlay for this case.",
        }

    return {"status": "limit", "reason": f"no direct Cella adapter for case kind {kind!r}"}


def run_sympy_naive(case: dict) -> dict:
    try:
        import sympy as sp
    except Exception as exc:
        return {"status": "unavailable", "reason": f"sympy unavailable: {exc}"}

    kind = str(case["kind"])
    data = dict(case["input"])
    if kind not in {"route_expression", "symbolic_rational"}:
        return {"status": "limit", "reason": f"SymPy naive baseline is not applicable to {kind}"}
    expr_text = str(data["expression"]).replace("^", "**")
    eps = sp.Symbol("eps")
    locals_map = {"eps": eps, "sqrt": sp.sqrt, "cos": sp.cos}
    for name in data.get("variables", []):
        locals_map[str(name)] = sp.Symbol(str(name))
    expr = sp.sympify(expr_text, locals=locals_map, rational=True)
    simplified = sp.simplify(expr)
    return {
        "status": "pass",
        "node_count": int(sp.count_ops(expr, visual=False)),
        "simplified_node_count": int(sp.count_ops(simplified, visual=False)),
        "simplified": str(simplified),
        "note": "Naive SymPy parse/simplify baseline; no Pathfinder route telemetry.",
    }


def run_mpmath_naive(case: dict) -> dict:
    try:
        import mpmath as mp
    except Exception as exc:
        return {"status": "unavailable", "reason": f"mpmath unavailable: {exc}"}

    kind = str(case["kind"])
    data = dict(case["input"])
    if kind != "route_expression":
        return {"status": "limit", "reason": f"mpmath naive baseline is not applicable to {kind}"}
    env = {
        "__builtins__": {},
        "eps": mp.mpf("1e-12"),
        "sqrt": mp.sqrt,
        "cos": mp.cos,
    }
    value = eval(str(data["expression"]), env, {})
    return {
        "status": "pass",
        "sample_eps": "1e-12",
        "value": str(value),
        "note": "Direct mpmath numeric sample; no route or rewrite decision.",
    }


def run_flint_arb(case: dict) -> dict:
    try:
        import flint
    except Exception as exc:
        return {"status": "unavailable", "reason": f"python-flint unavailable: {exc}"}

    kind = str(case["kind"])
    data = dict(case["input"])
    if kind != "route_expression":
        return {"status": "limit", "reason": f"Arb baseline is not applicable to {kind} in this MVP"}

    sample_eps = str(data.get("sample_eps", data.get("sweep", {}).get("low", "1e-12")))
    with flint.ctx.workdps(int(data.get("arb_dps", 80))):
        eps = flint.arb(sample_eps)
        result = _eval_arb_expr(str(data["expression"]), {"eps": eps}, flint)
        zero = flint.arb(0)
        return {
            "status": "pass",
            "backend": "python-flint arb",
            "operation": _arb_operation_label(str(data["expression"])),
            "sample_eps": sample_eps,
            "precision_dps": int(data.get("arb_dps", 80)),
            "value": str(result),
            "lower": str(result.lower()),
            "upper": str(result.upper()),
            "radius": str(result.rad()),
            "bits": result.bits(),
            "rel_accuracy_bits": result.rel_accuracy_bits(),
            "contains_zero": bool(result.contains(zero)),
            "note": "Arb ball evaluation baseline; no Pathfinder route or rewrite decision.",
        }


def _eval_arb_expr(expression: str, names: dict, flint_module):
    tree = ast.parse(str(expression), mode="eval").body
    return _eval_arb_node(tree, names, flint_module)


def _eval_arb_node(node: ast.AST, names: dict, flint_module):
    arb = flint_module.arb
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ValueError(f"unsupported Arb constant {node.value!r}")
        return arb(str(node.value))
    if isinstance(node, ast.Name):
        if node.id not in names:
            raise ValueError(f"unsupported Arb symbol {node.id!r}")
        return names[node.id]
    if isinstance(node, ast.UnaryOp):
        value = _eval_arb_node(node.operand, names, flint_module)
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return value
        raise ValueError(f"unsupported Arb unary operator {type(node.op).__name__}")
    if isinstance(node, ast.BinOp):
        left = _eval_arb_node(node.left, names, flint_module)
        right = _eval_arb_node(node.right, names, flint_module)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left ** right
        raise ValueError(f"unsupported Arb binary operator {type(node.op).__name__}")
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and len(node.args) == 1:
        arg = _eval_arb_node(node.args[0], names, flint_module)
        if node.func.id == "sqrt":
            return arg.sqrt()
        if node.func.id == "cos":
            return arg.cos()
        if node.func.id == "sin":
            return arg.sin()
        if node.func.id == "exp":
            return arg.exp()
        if node.func.id == "log":
            return arg.log()
    raise ValueError(f"unsupported Arb expression node {type(node).__name__}")


def _arb_operation_label(expression: str) -> str:
    compact = str(expression).replace(" ", "")
    if compact == "(1+eps)-1":
        return "constant_offset_collapse"
    if compact == "sqrt(1+eps)-1":
        return "sqrt_minus_one"
    if compact == "cos(eps)-1":
        return "cos_minus_one"
    return "arb_expression"


def _run_verification_script(data: dict, expect: dict) -> dict:
    script = REPO_ROOT / str(data["script"])
    if not script.exists():
        return {"status": "fail", "reason": f"script does not exist: {script}"}
    cmd = [sys.executable, str(script)] + [str(arg) for arg in data.get("args", [])]
    timeout = float(data.get("timeout_seconds", 300))
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
        return {
            "status": "fail",
            "reason": f"verification script timed out after {timeout:g}s",
            "command": cmd,
            "script_elapsed_ms": elapsed_ms,
            "stdout_tail": _tail(exc.stdout or ""),
            "stderr_tail": _tail(exc.stderr or ""),
        }

    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    expected_returncode = int(expect.get("returncode", 0))
    token = str(expect.get("stdout_contains", ""))
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    ok = completed.returncode == expected_returncode and (not token or token in stdout)
    out = {
        "status": "pass" if ok else "fail",
        "command": cmd,
        "returncode": completed.returncode,
        "expected_returncode": expected_returncode,
        "stdout_contains": token,
        "verdict": _extract_verdict(stdout),
        "script_elapsed_ms": elapsed_ms,
        "stdout_tail": _tail(stdout),
        "stderr_tail": _tail(stderr),
    }
    if not ok:
        out["reason"] = "return code or stdout verdict token mismatch"
    return out


def _extract_verdict(stdout: str) -> str:
    verdicts = [line.strip() for line in stdout.splitlines() if line.strip().startswith("VERDICT:")]
    return verdicts[-1] if verdicts else ""


def _tail(text: str, max_lines: int = 24, max_chars: int = 8000) -> str:
    lines = str(text).splitlines()
    tail = "\n".join(lines[-max_lines:])
    if len(tail) > max_chars:
        return tail[-max_chars:]
    return tail


def _status(ok: bool, reason: str = "expectation mismatch", **payload) -> dict:
    out = {"status": "pass" if ok else "fail"}
    if not ok:
        out["reason"] = reason
    out.update(payload)
    return out


def _summary(cases: list[dict]) -> dict:
    counts: dict[str, dict[str, int]] = {}
    totals: dict[str, int] = {}
    for case in cases:
        for engine, result in case["engines"].items():
            status = str(result.get("status", "unknown"))
            counts.setdefault(engine, {})
            counts[engine][status] = counts[engine].get(status, 0) + 1
            totals[status] = totals.get(status, 0) + 1
    return {
        "case_count": len(cases),
        "engine_status_counts": counts,
        "total_status_counts": totals,
    }


def _jsonify(value: Any) -> Any:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return value
    if isinstance(value, Fraction):
        return _text(value)
    if isinstance(value, tuple):
        return [_jsonify(v) for v in value]
    if isinstance(value, list):
        return [_jsonify(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _jsonify(v) for k, v in value.items()}
    return str(value)


def _text(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return str(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Cella Pathfinder hostile benchmark campaign.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--output", default="reports/pathfinder_hostile/mvp-report.json")
    args = parser.parse_args(argv)
    report = run_manifest(args.manifest, args.output)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    print(f"report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
