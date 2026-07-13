"""Cella-native slope-flow comparison.

Local Cella port of V4's ``branch/slope_flow.py`` method.  It compares
segment-by-segment log-magnitude slopes against declared slope models, so
Pathfinder residual-order readings are not reduced to one global OLS fit.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Any, Sequence


DEFAULT_SLOPE_MODEL_BAND = 0.05
RESIDUAL_ORDER_CANDIDATES = (
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


@dataclass(frozen=True, slots=True)
class SlopeFlowSample:
    control: int | float
    observable: int | float
    source_trace_id: str | None = None
    detection_trace_id: str | None = None
    detection_status: str | None = None

    def to_record(self) -> dict:
        return {
            "control": self.control,
            "observable": self.observable,
            "source_trace_id": self.source_trace_id,
            "detection_trace_id": self.detection_trace_id,
            "detection_status": self.detection_status,
        }


@dataclass(frozen=True, slots=True)
class SlopeFlowModel:
    name: str
    expected_slope: int | float

    def to_record(self) -> dict:
        return {
            "name": self.name,
            "expected_slope": float(self.expected_slope),
        }


def default_slope_models() -> tuple[SlopeFlowModel, ...]:
    return tuple(
        SlopeFlowModel(f"order_{_fraction_label(order)}", float(order))
        for order in RESIDUAL_ORDER_CANDIDATES
    )


def residual_order_derivative_models() -> tuple[SlopeFlowModel, ...]:
    """Models for finite-difference transfer slope = residual order - 1."""

    return tuple(
        SlopeFlowModel(f"order_{_fraction_label(order)}", float(order) - 1.0)
        for order in RESIDUAL_ORDER_CANDIDATES
    )


def compare_slope_flow_to_models(
    samples: Sequence[SlopeFlowSample | tuple[float, float] | dict],
    models: Sequence[SlopeFlowModel | tuple[str, float] | dict] = (),
    *,
    declared_model_band: float | None = None,
    comparison_kind: str = "direct_transfer",
) -> dict:
    band = _optional_nonnegative(declared_model_band, "declared_model_band")
    sample_tuple = tuple(_validate_sample(sample) for sample in samples)
    model_tuple = tuple(_validate_model(model) for model in models)
    usable = tuple(index for index, sample in enumerate(sample_tuple) if _is_loggable(sample))
    source_trace_ids = tuple(
        sample.source_trace_id for sample in sample_tuple if sample.source_trace_id is not None
    )

    if len(usable) < 2:
        return _slope_record(
            samples=sample_tuple,
            usable=usable,
            segments=(),
            models=model_tuple,
            residuals=(),
            band=band,
            selected=None,
            comparison_kind=comparison_kind,
            source_trace_ids=source_trace_ids,
            status="SLOPE_FLOW_INSUFFICIENT_SAMPLES",
        )

    segments = tuple(_segment(sample_tuple, left, right) for left, right in zip(usable, usable[1:]))
    if any(segment["slope"] is None for segment in segments):
        return _slope_record(
            samples=sample_tuple,
            usable=usable,
            segments=segments,
            models=model_tuple,
            residuals=(),
            band=band,
            selected=None,
            comparison_kind=comparison_kind,
            source_trace_ids=source_trace_ids,
            status="SLOPE_FLOW_INDETERMINATE",
        )

    residuals = tuple(_residual(model, segments, band) for model in model_tuple)
    selected = None
    if not model_tuple:
        status = "SLOPE_FLOW_OBSERVED"
    elif band is None:
        status = "SLOPE_MODEL_RESIDUALS"
    else:
        inside = [residual["model_name"] for residual in residuals if residual["within_declared_band"]]
        if len(inside) == 1:
            status = "SLOPE_MODEL_UNIQUE_MATCH"
            selected = inside[0]
        elif len(inside) > 1:
            status = "SLOPE_MODEL_AMBIGUOUS"
        else:
            status = "SLOPE_MODEL_NO_MATCH"

    return _slope_record(
        samples=sample_tuple,
        usable=usable,
        segments=segments,
        models=model_tuple,
        residuals=residuals,
        band=band,
        selected=selected,
        comparison_kind=comparison_kind,
        source_trace_ids=source_trace_ids,
        status=status,
    )


def residual_order_flow(
    observations: Sequence[tuple[float, float] | dict],
    *,
    declared_model_band: float = DEFAULT_SLOPE_MODEL_BAND,
    comparison_kind: str = "residual_order",
) -> dict:
    return compare_slope_flow_to_models(
        observations,
        default_slope_models(),
        declared_model_band=declared_model_band,
        comparison_kind=comparison_kind,
    )


def residual_order_from_sweep_signature(
    sweep_signature: dict,
    *,
    declared_model_band: float = DEFAULT_SLOPE_MODEL_BAND,
) -> dict:
    """Classify residual order from a sweep-signature transfer record.

    ``sweep_signature_probe`` observes finite-difference transfers.  If the
    residual behaves like ``C*x**p``, those transfer magnitudes behave like
    ``p*C*x**(p-1)``.  This helper compares the segment flow against models
    keyed by the original residual order ``p`` while using expected derivative
    slopes ``p-1``.
    """

    transfers = tuple(sweep_signature.get("transfers", ()))
    samples = tuple(
        (float(transfer["f"]), abs(float(transfer["transfer"])))
        for transfer in transfers
        if transfer.get("status") == "transfer_observed"
        and transfer.get("transfer") is not None
        and math.isfinite(float(transfer.get("f", 0.0)))
        and math.isfinite(float(transfer["transfer"]))
        and float(transfer.get("f", 0.0)) > 0.0
        and float(transfer["transfer"]) != 0.0
    )
    flow = compare_slope_flow_to_models(
        samples,
        residual_order_derivative_models(),
        declared_model_band=declared_model_band,
        comparison_kind="sweep_signature_residual_order",
    )
    flow["sweep_signature_status"] = sweep_signature.get("status")
    flow["sweep_cancellation_grade"] = sweep_signature.get("cancellation_grade")
    flow["sweep_drop_rate"] = sweep_signature.get("drop_rate")
    flow["sweep_slope_observation"] = sweep_signature.get("slope_observation")
    flow["order_source"] = "sweep_signature_probe_derivative_flow"
    flow["reported_order"] = flow.get("selected_order")
    return flow


def _segment(samples: tuple[SlopeFlowSample, ...], left_index: int, right_index: int) -> dict:
    left = samples[left_index]
    right = samples[right_index]
    delta_control = math.log(float(right.control)) - math.log(float(left.control))
    delta_observable = math.log(abs(float(right.observable))) - math.log(abs(float(left.observable)))
    if delta_control == 0.0 or not math.isfinite(delta_control) or not math.isfinite(delta_observable):
        slope = None
        refusal = "non_scalar_projective_slope"
    else:
        slope = delta_observable / delta_control
        refusal = None
    return {
        "left_index": left_index,
        "right_index": right_index,
        "delta_log_control": delta_control,
        "delta_log_observable": delta_observable,
        "projective_ratio": {
            "numerator": delta_observable,
            "denominator": delta_control,
        },
        "slope": slope,
        "refusal_reason": refusal,
    }


def _residual(model: SlopeFlowModel, segments: tuple[dict, ...], band: float | None) -> dict:
    segment_residuals = tuple(
        float(segment["slope"]) - float(model.expected_slope)
        for segment in segments
        if segment["slope"] is not None
    )
    max_abs = max((abs(value) for value in segment_residuals), default=None)
    within = None if band is None or max_abs is None else max_abs <= band
    return {
        "model_name": model.name,
        "expected_slope": float(model.expected_slope),
        "segment_residuals": list(segment_residuals),
        "max_abs_segment_residual": max_abs,
        "within_declared_band": within,
    }


def _slope_record(
    *,
    samples: tuple[SlopeFlowSample, ...],
    usable: tuple[int, ...],
    segments: tuple[dict, ...],
    models: tuple[SlopeFlowModel, ...],
    residuals: tuple[dict, ...],
    band: float | None,
    selected: str | None,
    comparison_kind: str,
    source_trace_ids: tuple[str, ...],
    status: str,
) -> dict:
    residuals_by_name = {record["model_name"]: record for record in residuals}
    slopes = [segment["slope"] for segment in segments if segment["slope"] is not None]
    return {
        "status": status,
        "samples": [sample.to_record() for sample in samples],
        "usable_sample_indices": list(usable),
        "segment_evidence": list(segments),
        "segment_slopes": slopes,
        "models": [model.to_record() for model in models],
        "model_residuals": list(residuals),
        "model_residuals_by_name": residuals_by_name,
        "declared_model_band": band,
        "selected_model_name": selected,
        "selected_order": _order_from_model_name(selected),
        "order_stability": _order_stability(status, slopes),
        "comparison_kind": comparison_kind,
        "source_trace_ids": list(source_trace_ids),
        "method": "slope_flow_segment_log_projective_model_comparison",
    }


def _order_stability(status: str, slopes: list[float]) -> str:
    if status == "SLOPE_MODEL_UNIQUE_MATCH":
        return "stable_model_match"
    if status == "SLOPE_MODEL_AMBIGUOUS":
        return "ambiguous_model_match"
    if status == "SLOPE_MODEL_NO_MATCH":
        return "model_mismatch"
    if status == "SLOPE_FLOW_OBSERVED" and slopes:
        spread = max(slopes) - min(slopes)
        return "stable_unmodelled" if abs(spread) <= DEFAULT_SLOPE_MODEL_BAND else "drifting_unmodelled"
    return "indeterminate"


def _order_from_model_name(name: str | None) -> str | None:
    if name is None:
        return None
    if not name.startswith("order_"):
        return None
    return name[len("order_"):]


def _is_loggable(sample: SlopeFlowSample) -> bool:
    return (
        float(sample.control) > 0.0
        and float(sample.observable) != 0.0
        and sample.detection_status in {None, "detected", "DETECTED"}
    )


def _validate_sample(sample: SlopeFlowSample | tuple[float, float] | dict) -> SlopeFlowSample:
    if isinstance(sample, SlopeFlowSample):
        out = sample
    elif isinstance(sample, dict):
        control = sample.get("control", sample.get("scale", sample.get("sweep")))
        observable = sample.get("observable", sample.get("transfer", sample.get("value")))
        out = SlopeFlowSample(
            control=control,
            observable=observable,
            source_trace_id=sample.get("source_trace_id"),
            detection_trace_id=sample.get("detection_trace_id"),
            detection_status=sample.get("detection_status"),
        )
    else:
        try:
            control, observable = sample
        except (TypeError, ValueError) as exc:
            raise ValueError("slope-flow samples must be sample objects, dicts, or pairs") from exc
        out = SlopeFlowSample(control, observable)
    _positive(out.control, "control")
    _finite(out.observable, "observable")
    return out


def _validate_model(model: SlopeFlowModel | tuple[str, float] | dict) -> SlopeFlowModel:
    if isinstance(model, SlopeFlowModel):
        out = model
    elif isinstance(model, dict):
        out = SlopeFlowModel(str(model["name"]), model["expected_slope"])
    else:
        try:
            name, expected = model
        except (TypeError, ValueError) as exc:
            raise ValueError("slope-flow models must be model objects, dicts, or pairs") from exc
        out = SlopeFlowModel(str(name), expected)
    _finite(out.expected_slope, "expected_slope")
    return out


def _finite(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise ValueError(f"{name} must be a finite scalar")
    return float(value)


def _positive(value: Any, name: str) -> float:
    number = _finite(value, name)
    if number <= 0.0:
        raise ValueError(f"{name} must be positive")
    return number


def _optional_nonnegative(value: Any | None, name: str) -> float | None:
    if value is None:
        return None
    number = _finite(value, name)
    if number < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return number


def _fraction_label(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"
