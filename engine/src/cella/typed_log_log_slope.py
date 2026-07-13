"""Cella-native log-log slope primitive.

This is the local Cella port of V4's ``typed_log_log_slope`` method: ordinary
least squares over log(f) -> log(|transfer|), with explicit refusal/degeneracy
status and fit diagnostics.  Cella adds signed coefficient recovery for
residual route assembly.
"""

from __future__ import annotations

from fractions import Fraction
import math


EXPONENT_CANDIDATES = (
    Fraction(0, 1),
    Fraction(1, 4),
    Fraction(1, 3),
    Fraction(1, 2),
    Fraction(2, 3),
    Fraction(3, 4),
    Fraction(1, 1),
    Fraction(4, 3),
    Fraction(3, 2),
    Fraction(5, 3),
    Fraction(2, 1),
    Fraction(5, 2),
    Fraction(3, 1),
    Fraction(4, 1),
)


def typed_log_log_slope(
    observations,
    *,
    expression_path: str = "ordinary_least_squares",
) -> dict:
    """Fit slope/intercept to ``(scale, transfer)`` observations.

    Observations may be pairs ``(f_value, transfer)`` or dictionaries with
    ``f_value``/``scale``/``sweep`` and ``transfer``/``value`` fields.
    """

    items = tuple(observations)
    pairs = tuple(pair for pair in (_usable_pair(item) for item in items) if pair is not None)
    n_input = len(items)
    n_used = len(pairs)
    if n_used < 3:
        return _slope_record(
            status="SLOPE_INSUFFICIENT_DATA",
            slope=None,
            intercept=None,
            r_squared=None,
            standard_error=None,
            n_input=n_input,
            n_used=n_used,
            log_f_min=None,
            log_f_max=None,
            residual_rms=None,
            residual_max_abs=None,
            residual_relative_rms=None,
            expression_path=expression_path,
        )

    log_f = tuple(math.log(f_value) for f_value, _transfer in pairs)
    log_t = tuple(math.log(abs(transfer)) for _f_value, transfer in pairs)
    log_f_min = min(log_f)
    log_f_max = max(log_f)
    if log_f_max - log_f_min == 0.0 or max(log_t) - min(log_t) == 0.0:
        return _slope_record(
            status="SLOPE_DEGENERATE_INPUT",
            slope=None,
            intercept=None,
            r_squared=None,
            standard_error=None,
            n_input=n_input,
            n_used=n_used,
            log_f_min=log_f_min,
            log_f_max=log_f_max,
            residual_rms=None,
            residual_max_abs=None,
            residual_relative_rms=None,
            expression_path=expression_path,
        )

    slope, intercept, r_squared, standard_error = _ordinary_least_squares(log_f, log_t)
    residual_rms, residual_max_abs, residual_relative_rms = _residual_stats(log_f, log_t, slope, intercept)
    return _slope_record(
        status="SLOPE_OBSERVED",
        slope=slope,
        intercept=intercept,
        r_squared=r_squared,
        standard_error=standard_error,
        n_input=n_input,
        n_used=n_used,
        log_f_min=log_f_min,
        log_f_max=log_f_max,
        residual_rms=residual_rms,
        residual_max_abs=residual_max_abs,
        residual_relative_rms=residual_relative_rms,
        expression_path=expression_path,
    )


def fit_power_law_signed(
    values: list[tuple[float, float]] | tuple[tuple[float, float], ...],
    *,
    forced_exponent: Fraction | str | None = None,
    exponent_source: str = "nearest_slope_candidate",
    expression_path: str = "cella_signed_power_law_fit",
) -> dict:
    """Fit ``y ~= c*x**p`` and preserve the sign of ``c``.

    This is the coefficient-estimation form of ``typed_log_log_slope``.  When
    ``forced_exponent`` is provided, the caller has already selected the order
    with a stronger method such as slope-flow; OLS is then only fit telemetry
    and coefficient evidence.
    """

    signed_usable = tuple(
        (float(x), float(y))
        for x, y in values
        if x > 0.0 and y != 0.0 and math.isfinite(x) and math.isfinite(y)
    )
    if not signed_usable:
        return _zero_power_fit(len(values), expression_path)

    slope_record = typed_log_log_slope(signed_usable, expression_path=expression_path)
    if slope_record["status"] == "SLOPE_OBSERVED":
        slope = float(slope_record["slope"])
        r2 = float(slope_record["r_squared"])
    else:
        slope = _fallback_slope(signed_usable)
        r2 = 1.0 if len(signed_usable) <= 2 else None

    if forced_exponent is None:
        exponent = _nearest_exponent(slope)
        exponent_source_used = exponent_source
    else:
        exponent = _parse_exponent(forced_exponent)
        exponent_source_used = exponent_source
    coeffs = [
        abs(y) / (x ** float(exponent))
        for x, y in signed_usable
        if x > 0.0 and math.isfinite(y)
    ]
    signed_coeffs = [
        y / (x ** float(exponent))
        for x, y in signed_usable
        if x > 0.0 and math.isfinite(y)
    ]
    coefficient = _median(coeffs) if coeffs else 0.0
    signed_coefficient = _median(signed_coeffs) if signed_coeffs else 0.0
    return {
        "signal_exponent": _fraction_text(exponent),
        "exponent_fraction": exponent,
        "coefficient": _snap_simple(coefficient),
        "signed_coefficient": _snap_simple(signed_coefficient),
        "r2": _snap_simple(r2) if r2 is not None else None,
        "slope_raw": _snap_simple(slope),
        "residual_rms": slope_record.get("residual_rms"),
        "residual_max_abs": slope_record.get("residual_max_abs"),
        "residual_relative_rms": slope_record.get("residual_relative_rms"),
        "fit_quality": {
            "status": slope_record["status"],
            "r2": _snap_simple(r2) if r2 is not None else None,
            "slope_raw": _snap_simple(slope),
            "residual_rms": slope_record.get("residual_rms"),
            "residual_max_abs": slope_record.get("residual_max_abs"),
            "residual_relative_rms": slope_record.get("residual_relative_rms"),
            "exponent_source": exponent_source_used,
            "forced_exponent": _fraction_text(exponent) if forced_exponent is not None else None,
            "intercept": _snap_simple(slope_record["intercept"]) if slope_record["intercept"] is not None else None,
            "standard_error": (
                _snap_simple(slope_record["standard_error"])
                if slope_record["standard_error"] is not None
                else None
            ),
            "n_input_observations": slope_record["n_input_observations"],
            "n_used": slope_record["n_used"],
            "log_f_min": slope_record["log_f_min"],
            "log_f_max": slope_record["log_f_max"],
            "expression_path": expression_path,
        },
    }


def _usable_pair(observation) -> tuple[float, float] | None:
    if isinstance(observation, dict):
        if "f_value" in observation:
            f_raw = observation["f_value"]
        elif "scale" in observation:
            f_raw = observation["scale"]
        else:
            f_raw = observation.get("sweep")
        if "transfer" in observation:
            t_raw = observation["transfer"]
        else:
            t_raw = observation.get("value")
    else:
        try:
            f_raw, t_raw = observation
        except (TypeError, ValueError):
            return None
    if isinstance(f_raw, bool) or isinstance(t_raw, bool):
        return None
    if not isinstance(f_raw, (int, float)) or not isinstance(t_raw, (int, float)):
        return None
    f_value = float(f_raw)
    transfer = float(t_raw)
    if not math.isfinite(f_value) or not math.isfinite(transfer):
        return None
    if f_value <= 0.0 or transfer == 0.0:
        return None
    return f_value, transfer


def _ordinary_least_squares(
    x_values: tuple[float, ...],
    y_values: tuple[float, ...],
) -> tuple[float, float, float, float]:
    n = len(x_values)
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n
    sxx = sum((x - mean_x) ** 2 for x in x_values)
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
    slope = 0.0 if sxx == 0.0 else sxy / sxx
    intercept = mean_y - slope * mean_x
    residuals = tuple(y - (slope * x + intercept) for x, y in zip(x_values, y_values))
    ss_res = sum(residual * residual for residual in residuals)
    ss_tot = sum((y - mean_y) ** 2 for y in y_values)
    r_squared = 1.0 if ss_tot == 0.0 else 1.0 - ss_res / ss_tot
    standard_error = 0.0 if sxx == 0.0 else math.sqrt(max(0.0, ss_res / (n - 2) / sxx))
    return slope, intercept, max(0.0, min(1.0, r_squared)), standard_error


def _residual_stats(
    x_values: tuple[float, ...],
    y_values: tuple[float, ...],
    slope: float,
    intercept: float,
) -> tuple[float, float, float]:
    residuals = tuple(y - (slope * x + intercept) for x, y in zip(x_values, y_values))
    rms = math.sqrt(sum(r * r for r in residuals) / len(residuals)) if residuals else 0.0
    max_abs = max((abs(r) for r in residuals), default=0.0)
    scale = max((abs(y) for y in y_values), default=0.0)
    relative = 0.0 if scale == 0.0 else rms / scale
    return _snap_simple(rms), _snap_simple(max_abs), _snap_simple(relative)


def _slope_record(
    *,
    status: str,
    slope: float | None,
    intercept: float | None,
    r_squared: float | None,
    standard_error: float | None,
    n_input: int,
    n_used: int,
    log_f_min: float | None,
    log_f_max: float | None,
    residual_rms: float | None,
    residual_max_abs: float | None,
    residual_relative_rms: float | None,
    expression_path: str,
) -> dict:
    return {
        "status": status,
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_squared,
        "standard_error": standard_error,
        "n_input_observations": n_input,
        "n_used": n_used,
        "log_f_min": log_f_min,
        "log_f_max": log_f_max,
        "residual_rms": residual_rms,
        "residual_max_abs": residual_max_abs,
        "residual_relative_rms": residual_relative_rms,
        "expression_path": expression_path,
        "method": "typed_log_log_slope_ordinary_least_squares",
    }


def _zero_power_fit(n_input: int, expression_path: str) -> dict:
    return {
        "signal_exponent": "zero",
        "exponent_fraction": Fraction(0, 1),
        "coefficient": 0.0,
        "signed_coefficient": 0.0,
        "r2": 1.0,
        "slope_raw": 0.0,
        "residual_rms": 0.0,
        "residual_max_abs": 0.0,
        "residual_relative_rms": 0.0,
        "fit_quality": {
            "status": "SLOPE_ZERO_TRANSFER",
            "r2": 1.0,
            "slope_raw": 0.0,
            "residual_rms": 0.0,
            "residual_max_abs": 0.0,
            "residual_relative_rms": 0.0,
            "intercept": None,
            "exponent_source": "zero_transfer",
            "forced_exponent": None,
            "standard_error": None,
            "n_input_observations": n_input,
            "n_used": 0,
            "log_f_min": None,
            "log_f_max": None,
            "expression_path": expression_path,
        },
    }


def _fallback_slope(values: tuple[tuple[float, float], ...]) -> float:
    if len(values) < 2:
        return 0.0
    first_x, first_y = values[0]
    last_x, last_y = values[-1]
    if first_x <= 0.0 or last_x <= 0.0 or first_y == 0.0 or last_y == 0.0:
        return 0.0
    denom = math.log(last_x) - math.log(first_x)
    if denom == 0.0:
        return 0.0
    return (math.log(abs(last_y)) - math.log(abs(first_y))) / denom


def _parse_exponent(value: Fraction | str) -> Fraction:
    if isinstance(value, Fraction):
        return value
    text = str(value)
    if text == "zero":
        return Fraction(0, 1)
    return Fraction(text)


def _nearest_exponent(slope: float) -> Fraction:
    if not math.isfinite(slope):
        return Fraction(0, 1)
    return min(EXPONENT_CANDIDATES, key=lambda candidate: abs(float(candidate) - slope))


def _median(values: list[float]) -> float:
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


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
