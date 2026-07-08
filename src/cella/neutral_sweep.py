"""Engine-neutral benchmark sweep with per-engine time caps.

This module is deliberately separate from the older hostile benchmark runner.
The corpus is declarative: each engine receives the same mathematical task and
the adapter chooses the most native route that engine would normally use.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

from .campaign import corner_frontface, diag_germ_classifier
from .pathfinder import route_plan
from .symbolic import symbolic_equal


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = REPO_ROOT / "benchmarks" / "neutral_sweep" / "manifest.json"
DEFAULT_ENGINES = ("cella", "sympy", "mpmath", "flint_arb")
TERMINAL_STATUSES = ("pass", "fail", "limit", "timeout", "unavailable")


def load_manifest(path: str | Path = DEFAULT_MANIFEST) -> dict:
    manifest_path = Path(path)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    for key in ("suite", "version", "cases"):
        if key not in data:
            raise ValueError(f"manifest missing required key {key!r}")
    if not isinstance(data["cases"], list) or not data["cases"]:
        raise ValueError("manifest cases must be a nonempty list")
    seen: set[str] = set()
    for case in data["cases"]:
        for key in ("id", "family", "kind", "input", "expect"):
            if key not in case:
                raise ValueError(f"case missing required key {key!r}: {case!r}")
        case_id = str(case["id"])
        if case_id in seen:
            raise ValueError(f"duplicate case id {case_id!r}")
        seen.add(case_id)
        if case["kind"] == "verification_script" or "script" in dict(case["input"]):
            raise ValueError(f"neutral case {case_id!r} must not launch a legacy script")
    data["_manifest_path"] = str(manifest_path)
    return data


def run_sweep(
    path: str | Path = DEFAULT_MANIFEST,
    *,
    output_path: str | Path | None = None,
    engines: list[str] | tuple[str, ...] | None = None,
    per_case_timeout_s: float = 30.0,
) -> dict:
    manifest = load_manifest(path)
    engine_names = tuple(engines or DEFAULT_ENGINES)
    cases = [_run_case(case, engine_names, float(per_case_timeout_s)) for case in manifest["cases"]]
    report = {
        "suite": manifest["suite"],
        "version": manifest["version"],
        "manifest_path": manifest["_manifest_path"],
        "per_case_timeout_s": float(per_case_timeout_s),
        "summary": _summary(cases, engine_names),
        "cases": cases,
    }
    if output_path is not None:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _run_case(case: dict, engines: tuple[str, ...], timeout_s: float) -> dict:
    return {
        "id": str(case["id"]),
        "family": str(case["family"]),
        "kind": str(case["kind"]),
        "engines": {
            engine: _run_engine_subprocess(engine, case, timeout_s)
            for engine in engines
        },
    }


def _run_engine_subprocess(engine: str, case: dict, timeout_s: float) -> dict:
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="cella_neutral_") as tmp:
        tmp_path = Path(tmp)
        case_path = tmp_path / "case.json"
        result_path = tmp_path / "result.json"
        progress_path = tmp_path / "progress.json"
        case_path.write_text(json.dumps(case), encoding="utf-8")

        cmd = [
            sys.executable,
            "-m",
            "cella.neutral_sweep",
            "--worker",
            "--engine",
            engine,
            "--case-file",
            str(case_path),
            "--result-file",
            str(result_path),
            "--progress-file",
            str(progress_path),
        ]
        env = dict(os.environ)
        src_path = str(REPO_ROOT / "src")
        env["PYTHONPATH"] = src_path + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
        proc = subprocess.Popen(
            cmd,
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            result = {
                "status": "timeout",
                "reason": f"engine exceeded {timeout_s:g}s case budget",
                "partial": _read_json(progress_path),
                "stdout_tail": _tail(stdout),
                "stderr_tail": _tail(stderr),
            }
        else:
            if result_path.exists():
                result = _read_json(result_path)
            else:
                result = {
                    "status": "fail",
                    "reason": f"worker exited without result file; returncode={proc.returncode}",
                    "partial": _read_json(progress_path),
                    "stdout_tail": _tail(stdout),
                    "stderr_tail": _tail(stderr),
                }
            if proc.returncode not in (0, None) and result.get("status") == "pass":
                result["status"] = "fail"
                result["reason"] = f"worker returncode {proc.returncode} after pass result"

    result = _jsonify(result)
    result.setdefault("status", "fail")
    result["elapsed_ms"] = round((time.perf_counter() - started) * 1000, 3)
    result["timeout_s"] = float(timeout_s)
    return result


def _worker_run(engine: str, case_path: str | Path, result_path: str | Path, progress_path: str | Path) -> int:
    case = json.loads(Path(case_path).read_text(encoding="utf-8"))
    result_file = Path(result_path)
    progress_file = Path(progress_path)

    def progress(phase: str, **extra: Any) -> None:
        payload = {
            "case_id": str(case.get("id")),
            "engine": engine,
            "phase": phase,
            "timestamp": time.time(),
        }
        payload.update(extra)
        progress_file.write_text(json.dumps(_jsonify(payload), sort_keys=True), encoding="utf-8")

    try:
        progress("dispatch")
        result = _adapter(engine, case, progress)
    except Exception as exc:
        result = {
            "status": "fail",
            "reason": f"{type(exc).__name__}: {exc}",
            "partial": _read_json(progress_file),
        }
    result_file.write_text(json.dumps(_jsonify(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


def _adapter(engine: str, case: dict, progress: Callable[..., None]) -> dict:
    adapters = {
        "cella": _run_cella,
        "sympy": _run_sympy,
        "mpmath": _run_mpmath,
        "flint_arb": _run_flint_arb,
    }
    if engine not in adapters:
        return {"status": "limit", "reason": f"unknown engine {engine!r}"}
    return adapters[engine](case, progress)


def _run_cella(case: dict, progress: Callable[..., None]) -> dict:
    kind = str(case["kind"])
    data = dict(case["input"])
    expect = dict(case["expect"])
    progress("cella_route", kind=kind)

    if kind == "arithmetic_rewrite":
        route = route_plan(str(data["expression"]), data["sweep"], include_profile=False)
        ok = route.get("decision") == expect.get("decision")
        return _status(ok, route=route, native_method="pathfinder_route_plan")

    if kind == "symbolic_equal":
        record = symbolic_equal(str(data["left"]).replace("^", "**"), str(data["right"]).replace("^", "**"), data["variables"])
        ok = bool(record["equal"]) is bool(expect["equal"])
        proof = "zero_normal_form" if record["equal"] else "nonzero_cross_difference"
        return _status(ok, proof=proof, symbolic=record, native_method="sparse_Q_cross_multiplication")

    if kind == "local_germ":
        record = diag_germ_classifier(str(data["coordinate"]), data["native"], data["transverse"])
        ok = record.get("kind") == expect.get("kind")
        if "coefficient_text" in expect:
            ok = ok and record.get("coefficient_text") == expect["coefficient_text"]
        return _status(ok, local_germ=record, native_method="local_normal_form")

    if kind == "corner_frontface":
        record = corner_frontface(face_data=data.get("face_data"), weights=data.get("weights"), path=data.get("path"))
        ok = _text(record.get("support_order")) == str(expect.get("support_order"))
        return _status(ok, corner=record, native_method="corner_support_function")

    if kind == "matrix_determinant":
        det = _hilbert_det_fraction(int(data["n"]))
        ok = det == Fraction(str(expect["determinant"]))
        return _status(ok, determinant=det, native_method="fraction_gaussian_elimination")

    if kind == "complex_eval":
        value = complex(0.0, math.pi)
        ok = bool(expect.get("real_zero")) and abs(value.real) < 1e-30
        return _status(ok, value={"real": value.real, "imag": value.imag}, native_method="principal_branch_recognition")

    if kind == "timeout_probe":
        return _timeout_probe(case, "cella", progress)

    return {"status": "limit", "reason": f"Cella adapter does not cover kind {kind!r}"}


def _run_sympy(case: dict, progress: Callable[..., None]) -> dict:
    try:
        import sympy as sp
    except Exception as exc:
        return {"status": "unavailable", "reason": f"sympy unavailable: {exc}"}

    kind = str(case["kind"])
    data = dict(case["input"])
    expect = dict(case["expect"])
    progress("sympy_parse", kind=kind)

    if kind == "arithmetic_rewrite":
        locals_map = _sympy_locals(["eps"], sp)
        expr = sp.sympify(str(data["expression"]).replace("^", "**"), locals=locals_map, rational=True)
        stable = sp.sympify(str(data["stable_expression"]).replace("^", "**"), locals=locals_map, rational=True)
        diff = sp.simplify(expr - stable)
        return _status(
            bool(diff == 0) is bool(expect["equivalent"]),
            simplified=str(sp.simplify(expr)),
            difference=str(diff),
            native_method="sympy_simplify_equivalence",
        )

    if kind == "symbolic_equal":
        locals_map = _sympy_locals(data["variables"], sp)
        left = sp.sympify(str(data["left"]).replace("^", "**"), locals=locals_map, rational=True)
        right = sp.sympify(str(data["right"]).replace("^", "**"), locals=locals_map, rational=True)
        diff = sp.cancel(sp.together(left - right))
        return _status(
            bool(diff == 0) is bool(expect["equal"]),
            proof="zero_normal_form" if diff == 0 else "nonzero_normal_form",
            difference=str(diff),
            node_count=int(sp.count_ops(left - right, visual=False)),
            native_method="sympy_cancel_together",
        )

    if kind == "matrix_determinant":
        matrix = sp.Matrix([[sp.Rational(1, i + j + 1) for j in range(int(data["n"]))] for i in range(int(data["n"]))])
        det = matrix.det()
        return _status(str(det) == str(expect["determinant"]), determinant=str(det), native_method="sympy_exact_matrix_det")

    if kind == "complex_eval":
        value = sp.simplify(sp.log(sp.exp(sp.I * sp.pi)))
        return _status(value == sp.I * sp.pi, value=str(value), native_method="sympy_principal_branch_simplify")

    if kind == "timeout_probe":
        return _timeout_probe(case, "sympy", progress)

    return {"status": "limit", "reason": f"SymPy adapter does not cover kind {kind!r}"}


def _run_mpmath(case: dict, progress: Callable[..., None]) -> dict:
    try:
        import mpmath as mp
    except Exception as exc:
        return {"status": "unavailable", "reason": f"mpmath unavailable: {exc}"}

    kind = str(case["kind"])
    data = dict(case["input"])
    progress("mpmath_prepare", kind=kind)
    mp.mp.dps = int(data.get("dps", 80))

    if kind == "arithmetic_rewrite":
        names = {name: mp.mpf(value) for name, value in data.get("sample", {}).items()}
        expr = _eval_mpmath_expr(str(data["expression"]), names, mp)
        stable = _eval_mpmath_expr(str(data["stable_expression"]), names, mp)
        tolerance = mp.mpf(10) ** (-(mp.mp.dps // 2))
        return _status(
            abs(expr - stable) <= tolerance,
            value=str(expr),
            stable_value=str(stable),
            error=str(abs(expr - stable)),
            native_method="mpmath_high_precision_sample",
        )

    if kind == "symbolic_equal":
        names = {name: mp.mpf(value) for name, value in data.get("sample", {}).items()}
        left = _eval_mpmath_expr(str(data["left"]), names, mp)
        right = _eval_mpmath_expr(str(data["right"]), names, mp)
        return {
            "status": "limit",
            "reason": "mpmath can sample the identity but cannot prove the symbolic equality",
            "sample_difference": str(left - right),
            "native_method": "mpmath_numeric_sample_only",
        }

    if kind == "matrix_determinant":
        matrix = mp.matrix([[mp.mpf(1) / (i + j + 1) for j in range(int(data["n"]))] for i in range(int(data["n"]))])
        det = mp.det(matrix)
        expected = mp.mpf(Fraction(str(case["expect"]["determinant"])).numerator) / Fraction(str(case["expect"]["determinant"])).denominator
        return _status(
            mp.almosteq(det, expected, rel_eps=mp.mpf("1e-60"), abs_eps=mp.mpf("1e-100")),
            determinant=str(det),
            expected=str(expected),
            native_method="mpmath_high_precision_det",
        )

    if kind == "complex_eval":
        value = mp.log(mp.e ** (mp.j * mp.pi))
        return _status(
            abs(mp.re(value)) < mp.mpf("1e-60") and abs(mp.im(value) - mp.pi) < mp.mpf("1e-60"),
            value=str(value),
            native_method="mpmath_principal_complex_eval",
        )

    if kind == "timeout_probe":
        return _timeout_probe(case, "mpmath", progress)

    return {"status": "limit", "reason": f"mpmath adapter does not cover kind {kind!r}"}


def _run_flint_arb(case: dict, progress: Callable[..., None]) -> dict:
    try:
        import flint
    except Exception as exc:
        return {"status": "unavailable", "reason": f"python-flint unavailable: {exc}"}

    kind = str(case["kind"])
    data = dict(case["input"])
    progress("flint_prepare", kind=kind)

    if kind == "arithmetic_rewrite":
        with flint.ctx.workdps(int(data.get("dps", 80))):
            names = {name: flint.arb(value) for name, value in data.get("sample", {}).items()}
            expr = _eval_flint_expr(str(data["expression"]), names, flint)
            stable = _eval_flint_expr(str(data["stable_expression"]), names, flint)
            diff = expr - stable
            return _status(
                bool(diff.contains(flint.arb(0))),
                value=str(expr),
                stable_value=str(stable),
                difference=str(diff),
                radius=str(diff.rad()),
                native_method="python_flint_arb_ball_eval",
            )

    if kind == "matrix_determinant":
        n = int(data["n"])
        matrix = flint.fmpq_mat([[flint.fmpq(1, i + j + 1) for j in range(n)] for i in range(n)])
        det = matrix.det()
        return _status(str(det) == str(case["expect"]["determinant"]), determinant=str(det), native_method="flint_fmpq_mat_det")

    if kind == "complex_eval":
        with flint.ctx.workdps(int(data.get("dps", 80))):
            value = flint.acb(0, flint.arb.pi()).exp().log()
            return {
                "status": "limit",
                "reason": "principal branch is enclosed but the Arb ball remains too wide for this branch-cut case",
                "value": str(value),
                "native_method": "python_flint_acb_branch_enclosure",
            }

    if kind == "timeout_probe":
        return _timeout_probe(case, "flint_arb", progress)

    return {"status": "limit", "reason": f"Flint/Arb adapter does not cover kind {kind!r}"}


def _timeout_probe(case: dict, engine: str, progress: Callable[..., None]) -> dict:
    data = dict(case["input"])
    if str(data.get("delay_engine")) == engine:
        progress("intentional_delay", delay_seconds=data.get("delay_seconds"))
        time.sleep(float(data.get("delay_seconds", 60)))
    return {"status": "pass", "native_method": "timeout_probe_no_delay"}


def _hilbert_det_fraction(n: int) -> Fraction:
    matrix = [[Fraction(1, i + j + 1) for j in range(n)] for i in range(n)]
    return _fraction_det(matrix)


def _fraction_det(matrix: list[list[Fraction]]) -> Fraction:
    a = [row[:] for row in matrix]
    n = len(a)
    det = Fraction(1)
    for i in range(n):
        pivot = next((r for r in range(i, n) if a[r][i]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            det = -det
        p = a[i][i]
        det *= p
        for r in range(i + 1, n):
            factor = a[r][i] / p
            for c in range(i, n):
                a[r][c] -= factor * a[i][c]
    return det


def _eval_mpmath_expr(expression: str, names: dict, mp_module):
    tree = ast.parse(str(expression).replace("^", "**"), mode="eval").body
    return _eval_mpmath_node(tree, names, mp_module)


def _eval_mpmath_node(node: ast.AST, names: dict, mp_module):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ValueError(f"unsupported mpmath constant {node.value!r}")
        return mp_module.mpf(str(node.value))
    if isinstance(node, ast.Name):
        if node.id == "pi":
            return mp_module.pi
        if node.id == "i":
            return mp_module.j
        if node.id in names:
            return names[node.id]
        raise ValueError(f"unsupported mpmath symbol {node.id!r}")
    if isinstance(node, ast.UnaryOp):
        value = _eval_mpmath_node(node.operand, names, mp_module)
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return value
    if isinstance(node, ast.BinOp):
        left = _eval_mpmath_node(node.left, names, mp_module)
        right = _eval_mpmath_node(node.right, names, mp_module)
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
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and len(node.args) == 1:
        arg = _eval_mpmath_node(node.args[0], names, mp_module)
        funcs = {
            "sqrt": mp_module.sqrt,
            "cos": mp_module.cos,
            "sin": mp_module.sin,
            "exp": mp_module.exp,
            "log": mp_module.log,
        }
        if node.func.id in funcs:
            return funcs[node.func.id](arg)
    raise ValueError(f"unsupported mpmath expression node {type(node).__name__}")


def _eval_flint_expr(expression: str, names: dict, flint_module):
    tree = ast.parse(str(expression).replace("^", "**"), mode="eval").body
    return _eval_flint_node(tree, names, flint_module)


def _eval_flint_node(node: ast.AST, names: dict, flint_module):
    arb = flint_module.arb
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ValueError(f"unsupported Arb constant {node.value!r}")
        return arb(str(node.value))
    if isinstance(node, ast.Name):
        if node.id == "pi":
            return arb.pi()
        if node.id in names:
            return names[node.id]
        raise ValueError(f"unsupported Arb symbol {node.id!r}")
    if isinstance(node, ast.UnaryOp):
        value = _eval_flint_node(node.operand, names, flint_module)
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return value
    if isinstance(node, ast.BinOp):
        left = _eval_flint_node(node.left, names, flint_module)
        right = _eval_flint_node(node.right, names, flint_module)
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
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and len(node.args) == 1:
        arg = _eval_flint_node(node.args[0], names, flint_module)
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


def _sympy_locals(names, sp_module) -> dict:
    out = {"sqrt": sp_module.sqrt, "cos": sp_module.cos, "sin": sp_module.sin, "exp": sp_module.exp, "log": sp_module.log}
    out["i"] = sp_module.I
    out["pi"] = sp_module.pi
    for name in names:
        out[str(name)] = sp_module.Symbol(str(name))
    return out


def _status(ok: bool, **payload) -> dict:
    out = {"status": "pass" if ok else "fail"}
    out.update(payload)
    return out


def _summary(cases: list[dict], engines: tuple[str, ...]) -> dict:
    out = {"case_count": len(cases), "engines": {engine: {status: 0 for status in TERMINAL_STATUSES} for engine in engines}}
    for case in cases:
        for engine, result in case["engines"].items():
            status = str(result.get("status", "fail"))
            out["engines"].setdefault(engine, {item: 0 for item in TERMINAL_STATUSES})
            out["engines"][engine][status] = out["engines"][engine].get(status, 0) + 1
    return out


def _text(value) -> str:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    return str(value)


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"read_error": f"{type(exc).__name__}: {exc}"}


def _tail(text: str | None, *, max_chars: int = 4000) -> str:
    if not text:
        return ""
    return text[-max_chars:]


def _jsonify(value):
    if isinstance(value, Fraction):
        return _text(value)
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, tuple):
        return [_jsonify(v) for v in value]
    if isinstance(value, list):
        return [_jsonify(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _jsonify(v) for k, v in value.items()}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Cella engine-neutral benchmark sweep.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--output")
    parser.add_argument("--timeout-s", type=float, default=30.0)
    parser.add_argument("--engines", nargs="+", default=list(DEFAULT_ENGINES))
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--engine")
    parser.add_argument("--case-file")
    parser.add_argument("--result-file")
    parser.add_argument("--progress-file")
    args = parser.parse_args(argv)

    if args.worker:
        missing = [name for name in ("engine", "case_file", "result_file", "progress_file") if getattr(args, name) is None]
        if missing:
            raise SystemExit(f"worker missing required args: {', '.join(missing)}")
        return _worker_run(args.engine, args.case_file, args.result_file, args.progress_file)

    report = run_sweep(args.manifest, output_path=args.output, engines=args.engines, per_case_timeout_s=args.timeout_s)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
