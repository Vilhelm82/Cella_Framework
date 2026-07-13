"""Exact theorem-directed compiler for the two admitted E128 paths."""

from __future__ import annotations

from dataclasses import asdict

from .records import (CompiledKernel, CurveRecord, DifferentialRecord, DUAL_PATH,
                      PRIMARY_PATH, PeriodRefusal, SourceRecord)


PLUS_EXPRESSION = "16*(t^2 - 2*w^2)/(t^2 + 8*w^2)/sqrt(P_plus)"
MINUS_EXPRESSION = "-16*t^2/(sqrt(P_minus)*(t^2 + 2*w^2 + sqrt(2)*sqrt(P_minus)))"


def canonical_source(path=PRIMARY_PATH) -> SourceRecord:
    return SourceRecord(path=path)


def compile_dbp_theta(source: SourceRecord):
    if source.curve != CurveRecord():
        return _refuse("unsupported_curve", "curve_gate", "curve coefficients or factorization differ")
    if source.differential != DifferentialRecord():
        return _refuse("unsupported_differential", "differential_gate", "Theta does not match exactly")
    if source.path.prescription == "one_sided" and source.path.sheet is None:
        return _refuse("cpv_side_not_declared", "path_gate", "one-sided continuation requires side and branch")
    if source.path.sheet is None:
        return _refuse("sheet_not_declared", "path_gate", "a physical sheet is mandatory")
    if source.path == PRIMARY_PATH:
        return CompiledKernel(
            "dbp_theta_primary_v1", "g_plus_v1",
            "P_plus = t^4 + 2*t^2*w^2 + 2*w^4", PLUS_EXPRESSION,
            ("P_plus >= 1/8", "t^2 + 8*w^2 >= 8/9"),
            {"curve": asdict(source.curve), "differential": asdict(source.differential),
             "path": asdict(source.path), "pole_crossings": []},
        )
    if source.path == DUAL_PATH:
        ledger = {
            "curve": asdict(source.curve), "differential": asdict(source.differential),
            "path": asdict(source.path), "source_pole": ["-7", "20*i"],
            "residue_of_minus_i_Theta": "4", "z_pole": "2*sqrt(2)",
            "polar_kernel": "16*sqrt(2)/(z^2-8)",
            "polar_primitive": "4*log(abs((z-2*sqrt(2))/(z+2*sqrt(2))))",
            "polar_kernel_cpv": "0", "rationalizing_identity": "A^2 - 2*P_minus = -t^2*D",
            "runtime_cpv": False,
        }
        return CompiledKernel(
            "dbp_theta_dual_cpv_v1", "g_minus_v1",
            "P_minus = (t^2-w^2)^2 + w^4", MINUS_EXPRESSION,
            ("P_minus >= 1/64", "t^2 + 2*w^2 >= 2/3"), ledger,
        )
    return _refuse("unsupported_relative_path", "path_gate", "path, orientation, sheet, or prescription differs")


def _refuse(token, stage, detail):
    return PeriodRefusal(token, stage, detail, detail)
