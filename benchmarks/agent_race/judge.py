"""Judge agent-race solver reports against a minimal answer key.

The answer key is intentionally only ``{case_id: answer_string}``. Comparison
policy lives here because the paper defines output type and precision while the
key remains a blind oracle, not a derivation guide.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_ANSWER_KEY = ROOT / "answer_key.json"

POLICY = {
    "P001": {"mode": "exact_text"},
    "P002": {"mode": "exact_text"},
    "P003": {"mode": "rational"},
    "P004": {"mode": "decimal_abs", "tol": "1e-80"},
    "P005": {"mode": "complex_rect", "tol": "1e-70"},
    "P006": {"mode": "exact_expr"},
    "P007": {"mode": "exact_expr"},
    "P008": {"mode": "decimal_abs", "tol": "1e-60"},
    "P009": {"mode": "complex_rect", "tol": "1e-70"},
    "P010": {"mode": "rational"},
}

TERMINAL_STATUSES = ("correct", "incorrect", "missing", "not_judged")


def load_answer_key(path: str | Path = DEFAULT_ANSWER_KEY) -> dict[str, str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not data:
        raise ValueError("answer key must be a nonempty object")
    bad = [key for key, value in data.items() if not isinstance(key, str) or not isinstance(value, str)]
    if bad:
        raise ValueError(f"answer key values must be strings only: {bad}")
    return data


def judge_report(report_path: str | Path, *, answer_key_path: str | Path = DEFAULT_ANSWER_KEY) -> dict:
    answer_key = load_answer_key(answer_key_path)
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    cases_in = report.get("cases", [])
    if not isinstance(cases_in, list):
        raise ValueError("report cases must be a list")

    submitted = {str(item.get("case_id")): item for item in cases_in if isinstance(item, dict)}
    judged_cases = []
    summary = {status: 0 for status in TERMINAL_STATUSES}
    native_ms_total = 0.0
    filler_ms_total = 0.0
    instrumentation_missing = 0

    for case_id in sorted(answer_key):
        item = submitted.get(case_id)
        if item is None:
            judged = {
                "case_id": case_id,
                "judgement": "missing",
                "reason": "case was not present in report",
            }
            summary["missing"] += 1
            judged_cases.append(judged)
            continue

        status = str(item.get("status", "fail"))
        answer = str(item.get("answer", ""))
        native_ms, filler_ms, instrumentation_ok = _timing_split(item)
        if instrumentation_ok:
            native_ms_total += native_ms
            filler_ms_total += filler_ms
        else:
            instrumentation_missing += 1
        judged = {
            "case_id": case_id,
            "status": status,
            "answer": answer,
            "elapsed_ms": item.get("elapsed_ms"),
            "native_ms": native_ms,
            "filler_ms": filler_ms,
            "filler_percent": _percent(filler_ms, native_ms + filler_ms),
            "native_steps": item.get("native_steps", []),
            "filler_steps": item.get("filler_steps", []),
            "instrumentation_ok": instrumentation_ok,
            "method": item.get("method"),
            "working_precision": item.get("working_precision"),
        }
        if status != "pass":
            judged["judgement"] = "not_judged"
            judged["reason"] = f"status is {status!r}, not 'pass'"
            summary["not_judged"] += 1
        else:
            ok, reason = compare(case_id, answer, answer_key[case_id])
            judged["judgement"] = "correct" if ok else "incorrect"
            judged["reason"] = reason
            summary["correct" if ok else "incorrect"] += 1
        judged_cases.append({k: v for k, v in judged.items() if v is not None})

    summary["native_ms"] = _round_ms(native_ms_total)
    summary["filler_ms"] = _round_ms(filler_ms_total)
    summary["filler_percent"] = _percent(filler_ms_total, native_ms_total + filler_ms_total)
    summary["instrumentation_missing"] = instrumentation_missing
    return {
        "engine": report.get("engine"),
        "summary": summary,
        "cases": judged_cases,
    }


def compare(case_id: str, answer: str, expected: str) -> tuple[bool, str]:
    policy = POLICY.get(case_id, {"mode": "exact_text"})
    mode = policy["mode"]
    if mode == "exact_text":
        return _norm_text(answer) == _norm_text(expected), f"exact text comparison for {case_id}"
    if mode == "exact_expr":
        return _norm_expr(answer) == _norm_expr(expected), f"exact expression comparison for {case_id}"
    if mode == "rational":
        try:
            return Fraction(answer) == Fraction(expected), f"exact rational comparison for {case_id}"
        except (ValueError, ZeroDivisionError) as exc:
            return False, f"invalid rational answer: {exc}"
    if mode == "decimal_abs":
        tol = Decimal(policy["tol"])
        try:
            with localcontext() as ctx:
                ctx.prec = 160
                return abs(Decimal(answer) - Decimal(expected)) <= tol, f"decimal abs tolerance {tol}"
        except InvalidOperation as exc:
            return False, f"invalid decimal answer: {exc}"
    if mode == "complex_rect":
        tol = Decimal(policy["tol"])
        try:
            ar, ai = _parse_complex_rect(answer)
            er, ei = _parse_complex_rect(expected)
            with localcontext() as ctx:
                ctx.prec = 160
                ok = abs(ar - er) <= tol and abs(ai - ei) <= tol
            return ok, f"complex rectangular abs tolerance {tol}"
        except (InvalidOperation, ValueError) as exc:
            return False, f"invalid complex answer: {exc}"
    return False, f"unknown comparison mode {mode!r}"


def _norm_text(value: str) -> str:
    return "".join(str(value).split())


def _norm_expr(value: str) -> str:
    text = _norm_text(value)
    text = text.replace("**", "^")
    return text


def _parse_complex_rect(value: str) -> tuple[Decimal, Decimal]:
    text = "".join(str(value).strip().lower().replace("j", "i").split())
    if not text:
        raise ValueError("empty complex value")
    if not text.endswith("i"):
        return Decimal(text), Decimal(0)
    body = text[:-1]
    split_at = -1
    for idx in range(1, len(body)):
        if body[idx] in "+-":
            split_at = idx
    if split_at == -1:
        real = Decimal(0)
        imag_text = body
    else:
        real = Decimal(body[:split_at])
        imag_text = body[split_at:]
    if imag_text in ("+", ""):
        imag = Decimal(1)
    elif imag_text == "-":
        imag = Decimal(-1)
    else:
        imag = Decimal(imag_text)
    return real, imag


def _timing_split(item: dict[str, Any]) -> tuple[float, float, bool]:
    try:
        native = float(item["native_ms"])
        filler = float(item["filler_ms"])
    except (KeyError, TypeError, ValueError):
        return 0.0, 0.0, False
    if native < 0 or filler < 0:
        return 0.0, 0.0, False
    return _round_ms(native), _round_ms(filler), True


def _round_ms(value: float) -> float:
    return round(float(value), 6)


def _percent(part: float, total: float) -> float:
    if total <= 0:
        return 0.0
    return round((float(part) / float(total)) * 100.0, 6)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Judge an agent-race solver report.")
    parser.add_argument("--report", required=True)
    parser.add_argument("--answer-key", default=str(DEFAULT_ANSWER_KEY))
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)

    judged = judge_report(args.report, answer_key_path=args.answer_key)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(judged, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(judged["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
