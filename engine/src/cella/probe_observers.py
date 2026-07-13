"""Cella-native probe observers copied from V4 observer methods.

This module ports the useful mechanics of V4's finite-difference,
sweep-signature, directional-alpha, and alpha-jet observers into Cella's
lightweight local style.  It keeps floating telemetry as measured data, while
using the copied ``typed_log_log_slope`` primitive for fit diagnostics.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Callable, Sequence

from .typed_log_log_slope import typed_log_log_slope


CANCELLATION_GRADE_THRESHOLD = 0.70
DROP_RATE_THRESHOLD = 0.30
MIN_OBSERVATIONS_FOR_FIT = 3
K_BOUNDARY = 2.0
K_DRIFT = 2.0
ALPHA_NUMERIC_FLOOR = 1.0e-9
DEFAULT_ALPHA_MATERIALITY = 0.05
MIN_WINDOW_POINTS = 3
MIN_WINDOW_COUNT = 3


@dataclass(frozen=True, slots=True)
class DeclaredAlphaModel:
    name: str
    alpha: float
    band: float

    def to_record(self) -> dict:
        return {"name": self.name, "alpha": float(self.alpha), "band": float(self.band)}


def typed_finite_difference(
    g_callable: Callable[[float], float],
    f: float,
    delta_f: float,
    *,
    function_label: str,
    precision: str = "raw_python",
    expression_path: str = "forward_difference",
) -> dict:
    _validate_fd_inputs(g_callable, f, delta_f, function_label)
    precision_floor = _precision_floor(precision)
    if delta_f == 0:
        return _transfer_record(
            "transfer_delta_indeterminate",
            None,
            None,
            None,
            None,
            None,
            f,
            delta_f,
            function_label,
            expression_path,
            ("delta_f_is_zero",),
        )

    g_f = None
    g_f_plus = None
    try:
        raw_g_f = g_callable(float(f))
        if not _is_numeric(raw_g_f):
            return _transfer_record("transfer_domain_refused", None, None, None, None, None, f, delta_f, function_label, expression_path, (f"non_numeric_return:g_at_f:{type(raw_g_f).__name__}",))
        g_f = float(raw_g_f)
        raw_g_f_plus = g_callable(float(f) + float(delta_f))
        if not _is_numeric(raw_g_f_plus):
            return _transfer_record("transfer_domain_refused", None, g_f, None, None, None, f, delta_f, function_label, expression_path, (f"non_numeric_return:g_at_f_plus_delta:{type(raw_g_f_plus).__name__}",))
        g_f_plus = float(raw_g_f_plus)
    except Exception as exc:
        return _transfer_record("transfer_domain_refused", None, g_f, g_f_plus, None, None, f, delta_f, function_label, expression_path, (f"exception:{type(exc).__name__}",))

    delta_g = g_f_plus - g_f
    transfer = delta_g / float(delta_f)
    if not math.isfinite(g_f):
        return _transfer_record("transfer_non_finite", transfer, g_f, g_f_plus, delta_g, None, f, delta_f, function_label, expression_path, ("nonfinite:g_at_f",))
    if not math.isfinite(g_f_plus):
        return _transfer_record("transfer_non_finite", transfer, g_f, g_f_plus, delta_g, None, f, delta_f, function_label, expression_path, ("nonfinite:g_at_f_plus_delta",))
    if not math.isfinite(transfer):
        return _transfer_record("transfer_non_finite", transfer, g_f, g_f_plus, delta_g, None, f, delta_f, function_label, expression_path, ("nonfinite:transfer",))

    max_g = max(abs(g_f), abs(g_f_plus))
    cancellation_ratio = None if max_g == 0.0 else abs(delta_g) / max_g
    if cancellation_ratio is not None and cancellation_ratio < precision_floor:
        return _transfer_record(
            "transfer_cancellation_dominated",
            transfer,
            g_f,
            g_f_plus,
            delta_g,
            cancellation_ratio,
            f,
            delta_f,
            function_label,
            expression_path,
            (f"cancellation_ratio={cancellation_ratio:.3e}", f"precision_floor={precision_floor:.3e}"),
        )

    return _transfer_record(
        "transfer_observed",
        transfer,
        g_f,
        g_f_plus,
        delta_g,
        cancellation_ratio,
        f,
        delta_f,
        function_label,
        expression_path,
        (),
    )


def sweep_signature_probe(
    observable: Callable[[float], float],
    f_values: Sequence[float],
    *,
    eta: float,
    function_label: str,
    probe_id: str,
    precision: str = "raw_python",
    expression_path: str = "sweep_signature_probe",
) -> dict:
    f_tuple = _validate_sweep_inputs(observable, f_values, eta, function_label, probe_id)
    delta_values = tuple(float(eta) * f for f in f_tuple)
    transfers = tuple(
        typed_finite_difference(
            observable,
            f,
            delta,
            function_label=function_label,
            precision=precision,
            expression_path="forward_difference",
        )
        for f, delta in zip(f_tuple, delta_values)
    )
    counts = _transfer_counts(transfers)
    observed_pairs = _observed_pairs(transfers)
    slope = typed_log_log_slope(observed_pairs, expression_path="ordinary_least_squares")
    slope = _regularized_slope_observation(slope, transfers)
    n_input = len(transfers)
    n_observed = counts["transfer_observed"]
    n_dropped = n_input - n_observed
    drop_rate = n_dropped / n_input if n_input else 1.0
    cancellation_grade = _cancellation_grade(slope.get("r_squared"))
    status = _classify_sweep_signature(counts, n_input, n_observed, drop_rate, cancellation_grade, slope)
    return {
        "status": status,
        "probe_id": probe_id,
        "function_label": function_label,
        "f_values": list(f_tuple),
        "delta_values": list(delta_values),
        "eta": float(eta),
        "transfers": list(transfers),
        "slope_observation": slope,
        "residual_rms": slope.get("residual_rms"),
        "residual_max_abs": slope.get("residual_max_abs"),
        "residual_relative_rms": slope.get("residual_relative_rms"),
        "cancellation_grade": cancellation_grade,
        "drop_rate": drop_rate,
        "n_input": n_input,
        "n_observed": n_observed,
        "n_dropped": n_dropped,
        "n_nonfinite": counts["transfer_non_finite"],
        "n_domain_refused": counts["transfer_domain_refused"],
        "n_cancellation_dominated": counts["transfer_cancellation_dominated"],
        "n_delta_indeterminate": counts["transfer_delta_indeterminate"],
        "expression_path": expression_path,
        "method": "sweep_signature_probe_forward_difference_log_log_slope",
    }


def directional_alpha_probe(
    observable: Callable[[float], float],
    f_values: Sequence[float],
    *,
    probe_id: str,
    function_label: str,
    eta: float = 1.0e-6,
    declared_alpha_models: Sequence[DeclaredAlphaModel] = (),
    declared_alpha_band: float | None = None,
    companion_sweep_signature: bool = False,
    precision: str = "raw_python",
    expression_path: str = "log_log_slope_fit",
) -> dict:
    f_tuple, models = _validate_alpha_inputs(observable, f_values, eta, probe_id, function_label, declared_alpha_models, declared_alpha_band)
    companion = None
    if companion_sweep_signature:
        companion = sweep_signature_probe(
            observable,
            f_tuple,
            eta=eta,
            function_label=function_label,
            probe_id=f"{probe_id}_companion_sweep_signature",
            precision=precision,
            expression_path="sweep_signature_companion",
        )

    delta_values = tuple(float(eta) * f for f in f_tuple)
    transfers = tuple(
        typed_finite_difference(
            observable,
            f,
            delta,
            function_label=function_label,
            precision=precision,
            expression_path="forward_difference",
        )
        for f, delta in zip(f_tuple, delta_values)
    )
    counts = _transfer_counts(transfers)
    if counts["transfer_observed"] < 3:
        status = _low_alpha_observation_status(counts, len(transfers))
        return _alpha_record(
            status,
            probe_id,
            function_label,
            f_tuple,
            delta_values,
            eta,
            transfers,
            None,
            None,
            None,
            None,
            None,
            None,
            _untested_nested_evidence(),
            counts,
            models,
            declared_alpha_band,
            None,
            (),
            expression_path,
            companion,
        )

    slope = typed_log_log_slope(_observed_pairs(transfers), expression_path="ordinary_least_squares")
    if slope["status"] == "SLOPE_INSUFFICIENT_DATA":
        status = "alpha_insufficient_data"
    elif slope["status"] == "SLOPE_DEGENERATE_INPUT":
        status = "alpha_indeterminate"
    elif not _finite_slope_value(slope.get("slope"), slope.get("intercept")):
        status = "alpha_nonfinite"
    else:
        observed_alpha = float(slope["slope"]) + 1.0
        nested = _nested_window_evidence(transfers, declared_alpha_band)
        if _is_zero_boundary(observed_alpha, slope.get("standard_error")):
            status, selected, matching = "alpha_zero_boundary", None, ()
        elif nested["alpha_stability_status"] == "unstable":
            status, selected, matching = "alpha_unstable_window", None, ()
        else:
            status, selected, matching = _classify_alpha(observed_alpha, models, declared_alpha_band)
        return _alpha_record(
            status,
            probe_id,
            function_label,
            f_tuple,
            delta_values,
            eta,
            transfers,
            slope,
            slope.get("slope"),
            observed_alpha,
            slope.get("r_squared"),
            slope.get("standard_error"),
            slope.get("log_f_min"),
            slope.get("log_f_max"),
            nested,
            counts,
            models,
            declared_alpha_band,
            selected,
            matching,
            expression_path,
            companion,
        )

    return _alpha_record(
        status,
        probe_id,
        function_label,
        f_tuple,
        delta_values,
        eta,
        transfers,
        slope,
        slope.get("slope"),
        None if slope.get("slope") is None else slope.get("slope") + 1.0,
        slope.get("r_squared"),
        slope.get("standard_error"),
        slope.get("log_f_min"),
        slope.get("log_f_max"),
        _untested_nested_evidence(),
        counts,
        models,
        declared_alpha_band,
        None,
        (),
        expression_path,
        companion,
    )


def scalar_alpha_jet_bundle(
    func: Callable[[float], float],
    x0: float,
    h_values: Sequence[float],
    *,
    probe_id: str,
    function_label: str,
    eta: float = 1.0e-6,
    declared_alpha_models: Sequence[DeclaredAlphaModel] = (),
    declared_alpha_band: float | None = None,
    precision: str = "raw_python",
    expression_path: str = "scalar_alpha_jet_local_probe",
) -> dict:
    point, h_tuple, models = _validate_jet_inputs(func, x0, h_values, eta, probe_id, function_label, declared_alpha_models, declared_alpha_band)
    try:
        f_at_x0 = float(func(point))
    except Exception as exc:
        return _jet_record("scalar_jet_domain_refused", point, None, probe_id, function_label, h_tuple, eta, None, None, None, None, None, None, models, declared_alpha_band, None, (), expression_path, f"f(x0) raised {type(exc).__name__}")
    if not math.isfinite(f_at_x0):
        return _jet_record("scalar_jet_nonfinite", point, f_at_x0, probe_id, function_label, h_tuple, eta, None, None, None, None, None, None, models, declared_alpha_band, None, (), expression_path, "f(x0) was nonfinite")

    def local(h: float) -> float:
        return func(point + h) - f_at_x0

    alpha = directional_alpha_probe(
        local,
        h_tuple,
        probe_id=f"{probe_id}__x0_{point!r}",
        function_label=f"{function_label}__local_at_{point!r}",
        eta=eta,
        declared_alpha_models=models,
        declared_alpha_band=declared_alpha_band,
        precision=precision,
        expression_path="log_log_slope_fit",
    )
    derivative = None
    derivative_h = None
    for h in sorted(set(h_tuple)):
        transfer = typed_finite_difference(local, h, eta * h, function_label=function_label, precision=precision)
        if transfer["status"] == "transfer_observed":
            derivative = transfer["transfer"]
            derivative_h = h
            break
    return _jet_record(
        _scalar_status_from_alpha(alpha["status"]),
        point,
        f_at_x0,
        probe_id,
        function_label,
        h_tuple,
        eta,
        alpha,
        alpha.get("observed_slope"),
        alpha.get("observed_alpha"),
        alpha.get("status"),
        derivative,
        derivative_h,
        models,
        declared_alpha_band,
        alpha.get("selected_alpha_model"),
        tuple(alpha.get("matching_alpha_model_names", [])),
        expression_path,
        f"alpha_status={alpha['status']}",
    )


def singular_alpha_jet_bundle(
    func: Callable[[float], float],
    x0: float,
    h_values: Sequence[float],
    *,
    probe_id: str,
    function_label: str,
    eta: float = 1.0e-6,
    declared_alpha_models: Sequence[DeclaredAlphaModel] = (),
    declared_alpha_band: float | None = None,
    precision: str = "raw_python",
    expression_path: str = "singular_alpha_jet_singular_probe",
) -> dict:
    point, h_tuple, models = _validate_jet_inputs(func, x0, h_values, eta, probe_id, function_label, declared_alpha_models, declared_alpha_band)

    def singular(h: float) -> float:
        return func(point + h)

    alpha = directional_alpha_probe(
        singular,
        h_tuple,
        probe_id=f"{probe_id}__x0_{point!r}",
        function_label=f"{function_label}__singular_at_{point!r}",
        eta=eta,
        declared_alpha_models=models,
        declared_alpha_band=declared_alpha_band,
        precision=precision,
        expression_path="log_log_slope_fit",
    )
    return {
        "status": _singular_status_from_alpha(alpha["status"]),
        "point": point,
        "probe_id": probe_id,
        "function_label": function_label,
        "h_values": list(h_tuple),
        "eta": float(eta),
        "alpha_probe_observation": alpha,
        "observed_slope": alpha.get("observed_slope"),
        "observed_alpha": alpha.get("observed_alpha"),
        "alpha_status": alpha.get("status"),
        "declared_alpha_models": [model.to_record() for model in models],
        "declared_alpha_band": declared_alpha_band,
        "selected_alpha_model": alpha.get("selected_alpha_model"),
        "matching_alpha_model_names": list(alpha.get("matching_alpha_model_names", [])),
        "expression_path": expression_path,
        "method": "singular_alpha_jet_bundle_directional_alpha_probe",
    }


def _transfer_record(status: str, transfer, g_f, g_f_plus, delta_g, cancellation_ratio, f, delta_f, function_label, expression_path, notes) -> dict:
    return {
        "status": status,
        "transfer": transfer,
        "g_at_f": g_f,
        "g_at_f_plus_delta": g_f_plus,
        "delta_g": delta_g,
        "cancellation_ratio": cancellation_ratio,
        "f": float(f),
        "delta_f": float(delta_f),
        "function_label": function_label,
        "expression_path": expression_path,
        "notes": list(notes),
        "method": "typed_finite_difference_forward_transfer",
    }


def _alpha_record(status, probe_id, function_label, f_values, delta_values, eta, transfers, slope, observed_slope, observed_alpha, r_squared, standard_error, log_f_min, log_f_max, nested, counts, models, declared_alpha_band, selected, matching, expression_path, companion) -> dict:
    return {
        "status": status,
        "probe_id": probe_id,
        "function_label": function_label,
        "f_values": list(f_values),
        "delta_values": list(delta_values),
        "eta": float(eta),
        "transfers": list(transfers),
        "slope_observation": slope,
        "observed_slope": observed_slope,
        "observed_alpha": observed_alpha,
        "r_squared": r_squared,
        "standard_error": standard_error,
        "log_f_min": log_f_min,
        "log_f_max": log_f_max,
        **nested,
        "n_input_observations": len(transfers),
        "n_observed": counts["transfer_observed"],
        "n_cancellation_dominated": counts["transfer_cancellation_dominated"],
        "n_non_finite": counts["transfer_non_finite"],
        "n_domain_refused": counts["transfer_domain_refused"],
        "n_delta_indeterminate": counts["transfer_delta_indeterminate"],
        "declared_alpha_models": [model.to_record() for model in models],
        "declared_alpha_band": declared_alpha_band,
        "selected_alpha_model": selected,
        "matching_alpha_model_names": list(matching),
        "expression_path": expression_path,
        "companion_sweep_signature": companion,
        "method": "directional_alpha_probe_forward_difference_log_log_slope",
    }


def _jet_record(status, point, f_value, probe_id, function_label, h_values, eta, alpha, observed_slope, observed_alpha, alpha_status, derivative, derivative_h, models, declared_alpha_band, selected, matching, expression_path, reason) -> dict:
    return {
        "status": status,
        "point": point,
        "f_value": f_value,
        "probe_id": probe_id,
        "function_label": function_label,
        "h_values": list(h_values),
        "eta": float(eta),
        "alpha_probe_observation": alpha,
        "observed_slope": observed_slope,
        "observed_alpha": observed_alpha,
        "alpha_status": alpha_status,
        "derivative_at_point": derivative,
        "derivative_h": derivative_h,
        "declared_alpha_models": [model.to_record() for model in models],
        "declared_alpha_band": declared_alpha_band,
        "selected_alpha_model": selected,
        "matching_alpha_model_names": list(matching),
        "expression_path": expression_path,
        "reason": reason,
        "method": "scalar_alpha_jet_bundle_directional_alpha_probe",
    }


def _observed_pairs(transfers: Sequence[dict]) -> tuple[tuple[float, float], ...]:
    return tuple(
        (float(t["f"]), float(t["transfer"]))
        for t in transfers
        if t.get("status") == "transfer_observed"
        and t.get("transfer") is not None
        and math.isfinite(float(t["transfer"]))
        and float(t["transfer"]) != 0.0
    )


def _transfer_counts(transfers: Sequence[dict]) -> dict[str, int]:
    statuses = (
        "transfer_observed",
        "transfer_cancellation_dominated",
        "transfer_non_finite",
        "transfer_domain_refused",
        "transfer_delta_indeterminate",
    )
    return {status: sum(1 for transfer in transfers if transfer.get("status") == status) for status in statuses}


def _regularized_slope_observation(slope: dict, transfers: Sequence[dict]) -> dict:
    if not transfers or any(t.get("status") != "transfer_observed" for t in transfers):
        return slope
    logs = [math.log(abs(float(t["transfer"]))) for t in transfers if t.get("transfer")]
    if not logs or max(logs) - min(logs) > CANCELLATION_GRADE_THRESHOLD:
        return slope
    if slope["status"] == "SLOPE_OBSERVED" and slope.get("slope") is not None and abs(slope["slope"]) <= CANCELLATION_GRADE_THRESHOLD:
        out = dict(slope)
        out.update({"slope": 0.0, "r_squared": 1.0, "standard_error": 0.0})
        return out
    return slope


def _nested_window_evidence(transfers: Sequence[dict], declared_alpha_band: float | None) -> dict:
    pairs = tuple(sorted(_observed_pairs(transfers), key=lambda pair: pair[0], reverse=True))
    max_window_count = len(pairs) - MIN_WINDOW_POINTS + 1
    if max_window_count < MIN_WINDOW_COUNT:
        return _untested_nested_evidence()
    fits = []
    for drop_count in range(max_window_count):
        fit = _fit_window(pairs[drop_count:])
        if fit is not None:
            fits.append(fit)
    if len(fits) < MIN_WINDOW_COUNT:
        return _untested_nested_evidence()
    min_fit = min(fits, key=lambda fit: fit["observed_alpha"])
    max_fit = max(fits, key=lambda fit: fit["observed_alpha"])
    alpha_span = max_fit["observed_alpha"] - min_fit["observed_alpha"]
    propagated = math.sqrt(min_fit["alpha_standard_error"] ** 2 + max_fit["alpha_standard_error"] ** 2)
    materiality = declared_alpha_band if declared_alpha_band is not None else DEFAULT_ALPHA_MATERIALITY
    stability = "unstable" if alpha_span > materiality and alpha_span > K_DRIFT * propagated else "stable"
    return {
        "nested_window_fits": fits,
        "alpha_window_min": min_fit["observed_alpha"],
        "alpha_window_max": max_fit["observed_alpha"],
        "alpha_window_span": alpha_span,
        "propagated_window_error": propagated,
        "alpha_stability_status": stability,
    }


def _fit_window(pairs: tuple[tuple[float, float], ...]) -> dict | None:
    if len(pairs) < MIN_WINDOW_POINTS:
        return None
    fit = typed_log_log_slope(pairs, expression_path="nested_window")
    if fit["status"] != "SLOPE_OBSERVED":
        return None
    return {
        "h_start": min(h for h, _ in pairs),
        "h_end": max(h for h, _ in pairs),
        "h_count": len(pairs),
        "observed_slope": fit["slope"],
        "observed_alpha": fit["slope"] + 1.0,
        "slope_standard_error": fit["standard_error"],
        "alpha_standard_error": fit["standard_error"],
        "r_squared": fit["r_squared"],
    }


def _untested_nested_evidence() -> dict:
    return {
        "nested_window_fits": None,
        "alpha_window_min": None,
        "alpha_window_max": None,
        "alpha_window_span": None,
        "propagated_window_error": None,
        "alpha_stability_status": "not_tested",
    }


def _classify_sweep_signature(counts, n_input, n_observed, drop_rate, cancellation_grade, slope) -> str:
    if counts["transfer_non_finite"] == n_input:
        return "sweep_signature_nonfinite"
    if counts["transfer_domain_refused"] == n_input:
        return "sweep_signature_domain_refused"
    if slope["status"] == "SLOPE_INSUFFICIENT_DATA" or n_observed < MIN_OBSERVATIONS_FOR_FIT:
        return "sweep_signature_insufficient_data"
    if slope["status"] == "SLOPE_DEGENERATE_INPUT" and slope.get("r_squared") is None:
        return "sweep_signature_degenerate_input"
    if cancellation_grade > CANCELLATION_GRADE_THRESHOLD:
        return "sweep_signature_cancellation_dominated"
    if drop_rate > DROP_RATE_THRESHOLD:
        return "sweep_signature_high_drop_rate"
    return "sweep_signature_clean"


def _classify_alpha(observed_alpha: float, models: tuple[DeclaredAlphaModel, ...], declared_alpha_band: float | None) -> tuple[str, str | None, tuple[str, ...]]:
    if not math.isfinite(observed_alpha):
        return "alpha_nonfinite", None, ()
    if models:
        matching = tuple(model for model in models if abs(observed_alpha - model.alpha) <= model.band)
        names = tuple(model.name for model in matching)
        if len(matching) > 1:
            return "alpha_model_ambiguous", None, names
        if not matching:
            return "alpha_model_no_match", None, ()
        matched = matching[0]
        if matched.alpha < 0:
            return "alpha_negative_singularity", matched.name, names
        if _is_close_to_positive_integer(matched.alpha, matched.band):
            return "alpha_regular_integer", matched.name, names
        return "alpha_fractional_branch", matched.name, names
    if observed_alpha < 0:
        return "alpha_negative_singularity", None, ()
    if declared_alpha_band is not None and _is_close_to_positive_integer(observed_alpha, declared_alpha_band):
        return "alpha_regular_integer", None, ()
    return "alpha_fractional_branch", None, ()


def _scalar_status_from_alpha(status: str) -> str:
    return {
        "alpha_regular_integer": "scalar_jet_regular_integer_alpha",
        "alpha_fractional_branch": "scalar_jet_fractional_alpha_branch",
        "alpha_negative_singularity": "scalar_jet_negative_alpha_singularity",
        "alpha_model_ambiguous": "scalar_jet_alpha_model_refused",
        "alpha_model_no_match": "scalar_jet_alpha_model_refused",
        "alpha_cancellation_dominated": "scalar_jet_alpha_cancellation_dominated",
        "alpha_insufficient_data": "scalar_jet_alpha_indeterminate",
        "alpha_indeterminate": "scalar_jet_alpha_indeterminate",
        "alpha_zero_boundary": "scalar_jet_alpha_zero_boundary",
        "alpha_unstable_window": "scalar_jet_alpha_unstable_window",
        "alpha_domain_refused": "scalar_jet_domain_refused",
        "alpha_nonfinite": "scalar_jet_nonfinite",
    }.get(status, "scalar_jet_protocol_refused")


def _singular_status_from_alpha(status: str) -> str:
    return {
        "alpha_regular_integer": "singular_jet_regular_integer_alpha",
        "alpha_fractional_branch": "singular_jet_fractional_alpha_branch",
        "alpha_negative_singularity": "singular_jet_negative_alpha_singularity",
        "alpha_model_ambiguous": "singular_jet_alpha_model_refused",
        "alpha_model_no_match": "singular_jet_alpha_model_refused",
        "alpha_cancellation_dominated": "singular_jet_alpha_cancellation_dominated",
        "alpha_insufficient_data": "singular_jet_alpha_indeterminate",
        "alpha_indeterminate": "singular_jet_alpha_indeterminate",
        "alpha_zero_boundary": "singular_jet_alpha_zero_boundary",
        "alpha_unstable_window": "singular_jet_alpha_unstable_window",
        "alpha_domain_refused": "singular_jet_domain_refused",
        "alpha_nonfinite": "singular_jet_nonfinite",
    }.get(status, "singular_jet_protocol_refused")


def _low_alpha_observation_status(counts: dict[str, int], total: int) -> str:
    majority = total // 2 + 1
    if counts["transfer_cancellation_dominated"] >= majority:
        return "alpha_cancellation_dominated"
    if counts["transfer_domain_refused"] >= majority:
        return "alpha_domain_refused"
    if counts["transfer_non_finite"] >= majority:
        return "alpha_nonfinite"
    return "alpha_insufficient_data"


def _cancellation_grade(r_squared: float | None) -> float:
    if r_squared is None or not math.isfinite(r_squared):
        return 0.0
    return 1.0 - r_squared


def _finite_slope_value(slope: float | None, intercept: float | None) -> bool:
    return slope is not None and intercept is not None and math.isfinite(slope) and math.isfinite(intercept)


def _alpha_boundary_envelope(standard_error: float | None) -> float:
    if standard_error is None or not math.isfinite(standard_error):
        return ALPHA_NUMERIC_FLOOR
    return max(K_BOUNDARY * standard_error, ALPHA_NUMERIC_FLOOR)


def _is_zero_boundary(observed_alpha: float, standard_error: float | None) -> bool:
    return abs(observed_alpha) <= _alpha_boundary_envelope(standard_error)


def _is_close_to_positive_integer(alpha: float, band: float) -> bool:
    if alpha <= 0:
        return False
    nearest = round(alpha)
    if nearest < 1:
        return False
    return abs(alpha - nearest) <= band


def _validate_fd_inputs(g_callable, f, delta_f, function_label) -> None:
    if not callable(g_callable):
        raise ValueError("g_callable must be callable")
    if isinstance(f, bool) or not isinstance(f, (int, float)) or not math.isfinite(float(f)):
        raise ValueError("f must be a finite real scalar")
    if isinstance(delta_f, bool) or not isinstance(delta_f, (int, float)) or not math.isfinite(float(delta_f)):
        raise ValueError("delta_f must be a finite real scalar")
    if not isinstance(function_label, str) or function_label == "":
        raise ValueError("function_label must be a non-empty string")


def _validate_sweep_inputs(observable, f_values, eta, function_label, probe_id) -> tuple[float, ...]:
    if not callable(observable):
        raise ValueError("observable must be callable")
    if not isinstance(function_label, str) or function_label == "":
        raise ValueError("function_label must be a non-empty string")
    if not isinstance(probe_id, str) or probe_id == "":
        raise ValueError("probe_id must be a non-empty string")
    if isinstance(eta, bool) or not isinstance(eta, (int, float)) or not math.isfinite(float(eta)) or float(eta) == 0.0:
        raise ValueError("eta must be a finite non-zero real scalar")
    f_tuple = tuple(float(value) for value in f_values)
    if not f_tuple or any(not math.isfinite(value) or value <= 0.0 for value in f_tuple):
        raise ValueError("f_values must contain finite positive scalars")
    return f_tuple


def _validate_alpha_inputs(observable, f_values, eta, probe_id, function_label, declared_alpha_models, declared_alpha_band) -> tuple[tuple[float, ...], tuple[DeclaredAlphaModel, ...]]:
    f_tuple = _validate_sweep_inputs(observable, f_values, eta, function_label, probe_id)
    models = _validate_alpha_models(declared_alpha_models, declared_alpha_band)
    return f_tuple, models


def _validate_jet_inputs(func, x0, h_values, eta, probe_id, function_label, declared_alpha_models, declared_alpha_band) -> tuple[float, tuple[float, ...], tuple[DeclaredAlphaModel, ...]]:
    if not callable(func):
        raise ValueError("func must be callable")
    if isinstance(x0, bool) or not isinstance(x0, (int, float)) or not math.isfinite(float(x0)):
        raise ValueError("x0 must be a finite real scalar")
    h_tuple = _validate_sweep_inputs(func, h_values, eta, function_label, probe_id)
    models = _validate_alpha_models(declared_alpha_models, declared_alpha_band)
    return float(x0), h_tuple, models


def _validate_alpha_models(models, declared_alpha_band) -> tuple[DeclaredAlphaModel, ...]:
    if declared_alpha_band is not None and (
        isinstance(declared_alpha_band, bool)
        or not isinstance(declared_alpha_band, (int, float))
        or not math.isfinite(float(declared_alpha_band))
        or float(declared_alpha_band) <= 0.0
    ):
        raise ValueError("declared_alpha_band must be finite and positive")
    out = tuple(models)
    names = set()
    for model in out:
        if not isinstance(model, DeclaredAlphaModel):
            raise ValueError("declared_alpha_models must contain DeclaredAlphaModel instances")
        if not model.name or model.name in names:
            raise ValueError("declared alpha model names must be non-empty and unique")
        names.add(model.name)
        if not math.isfinite(model.alpha) or not math.isfinite(model.band) or model.band <= 0.0:
            raise ValueError("declared alpha model alpha and band must be finite, with positive band")
    return out


def _precision_floor(precision: str) -> float:
    if precision == "raw_python":
        return 2.0**-52
    raise ValueError(f"unsupported precision {precision!r}; raw_python is currently supported")


def _is_numeric(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float))
