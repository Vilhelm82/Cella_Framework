from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable, Final, Sequence

from lloyd_v4.core.conditioning import Conditioning
from lloyd_v4.core.errors import ProtocolViolationError
from lloyd_v4.core.protocols import ConsumerProtocol, ProducerProtocol
from lloyd_v4.core.provenance import Provenance
from lloyd_v4.core.result import TypedResult
from lloyd_v4.core.serialization import to_json_safe
from lloyd_v4.core.status import ConditioningStatus, ProtocolStatus, SlopeStatus, SweepSignatureStatus, TransferStatus
from lloyd_v4.core.transitions import StatusTransitionRule
from lloyd_v4.core.validity import Validity
from lloyd_v4.primitives.typed_collection import typed_collection
from lloyd_v4.primitives.log64 import log64
from lloyd_v4.primitives.typed_finite_difference import typed_finite_difference
from lloyd_v4.primitives.typed_log_log_slope import LogLogSlopeObservation, LogLogSlopeResult, typed_log_log_slope


SWEEP_SIGNATURE_PROBE_SPACE: Final[str] = "SweepSignatureObservation"
CANCELLATION_GRADE_THRESHOLD: Final[float] = 0.70
DROP_RATE_THRESHOLD: Final[float] = 0.30
MIN_OBSERVATIONS_FOR_FIT: Final[int] = 3

SWEEP_SIGNATURE_STATUSES = frozenset(SweepSignatureStatus)

SWEEP_SIGNATURE_PROBE_PROTOCOL: Final[ProducerProtocol] = ProducerProtocol(
    name="sweep_signature_probe",
    emitted_statuses=SWEEP_SIGNATURE_STATUSES,
    required_fields=frozenset({"value", "status", "validity", "provenance"}),
    status_family=SweepSignatureStatus,
)

SWEEP_SIGNATURE_CONSUMER_PROTOCOL: Final[ConsumerProtocol] = ConsumerProtocol(
    name="sweep_signature_consumer",
    accepted_statuses=frozenset({SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN}),
    required_validity_fields=frozenset({"defined", "finite", "selectable"}),
    scalarization_allowed=False,
    status_family=SweepSignatureStatus,
    refused_statuses=SWEEP_SIGNATURE_STATUSES - frozenset({SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN}),
)

SWEEP_SIGNATURE_CONSUMER_TRANSITION_RULE: Final[StatusTransitionRule] = StatusTransitionRule(
    rule_id="sweep_signature_consumer_accepts_clean",
    input_status_family=SweepSignatureStatus,
    output_status_family=None,
    input_protocol_id=SWEEP_SIGNATURE_PROBE_PROTOCOL.name,
    output_protocol_id=SWEEP_SIGNATURE_CONSUMER_PROTOCOL.name,
    accepted_input_statuses=frozenset({SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN}),
    refused_input_statuses=SWEEP_SIGNATURE_STATUSES - frozenset({SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN}),
    mapped_statuses={},
    emitted_input_statuses=SWEEP_SIGNATURE_STATUSES,
    description="Default sweep-signature consumer accepts only clean sweep evidence.",
)


@dataclass(frozen=True, slots=True)
class SweepSignatureValue:
    cancellation_grade: float
    drop_rate: float
    slope_observation: LogLogSlopeObservation
    n_input: int
    n_observed: int
    n_dropped: int
    n_nonfinite: int
    n_domain_refused: int
    n_cancellation_dominated: int
    n_delta_indeterminate: int
    expression_path: str

    def to_json_safe(self) -> dict[str, Any]:
        return {
            "cancellation_grade": to_json_safe(self.cancellation_grade),
            "drop_rate": to_json_safe(self.drop_rate),
            "slope_observation": self.slope_observation.to_json_safe(),
            "n_input": self.n_input,
            "n_observed": self.n_observed,
            "n_dropped": self.n_dropped,
            "n_nonfinite": self.n_nonfinite,
            "n_domain_refused": self.n_domain_refused,
            "n_cancellation_dominated": self.n_cancellation_dominated,
            "n_delta_indeterminate": self.n_delta_indeterminate,
            "expression_path": self.expression_path,
        }


SweepSignatureResult = TypedResult[SweepSignatureValue, SweepSignatureStatus]


def sweep_signature_probe(
    observable: Callable[[float], float],
    f_values: Sequence[float],
    *,
    eta: float,
    function_label: str,
    probe_id: str,
    precision: str = "raw_python",
    backend: str = "python",
    device: str = "cpu",
    measurement_resolution: Any | None = None,
    expression_path: str = "sweep_signature_probe",
) -> SweepSignatureResult:
    f_tuple = _validate_inputs(observable, f_values, eta, function_label, probe_id)
    delta_values = tuple(eta * f_value for f_value in f_tuple)
    transfers = tuple(
        typed_finite_difference(
            observable,
            f_value,
            delta_value,
            function_label=function_label,
            precision=precision,
            backend=backend,
            device=device,
            measurement_resolution=measurement_resolution,
            expression_path="forward_difference",
        )
        for f_value, delta_value in zip(f_tuple, delta_values)
    )
    counts = _transfer_counts(transfers)
    n_input = len(transfers)
    n_observed = counts[TransferStatus.TRANSFER_OBSERVED]
    n_dropped = n_input - n_observed
    drop_rate = n_dropped / n_input

    slope_result: LogLogSlopeResult | None
    if counts[TransferStatus.TRANSFER_NON_FINITE] == n_input or counts[TransferStatus.TRANSFER_DOMAIN_REFUSED] == n_input:
        slope_result = None
        slope_observation = _empty_slope_observation(n_input, 0, expression_path)
    else:
        slope_result = typed_log_log_slope(
            typed_collection(transfers),
            precision=precision,
            backend=backend,
            device=device,
            measurement_resolution=measurement_resolution,
            expression_path="ordinary_least_squares",
        )
        slope_observation = _regularized_slope_observation(slope_result, transfers, drop_rate)

    cancellation_grade = _cancellation_grade(slope_observation.r_squared)
    value = SweepSignatureValue(
        cancellation_grade=cancellation_grade,
        drop_rate=drop_rate,
        slope_observation=slope_observation,
        n_input=n_input,
        n_observed=n_observed,
        n_dropped=n_dropped,
        n_nonfinite=counts[TransferStatus.TRANSFER_NON_FINITE],
        n_domain_refused=counts[TransferStatus.TRANSFER_DOMAIN_REFUSED],
        n_cancellation_dominated=counts[TransferStatus.TRANSFER_CANCELLATION_DOMINATED],
        n_delta_indeterminate=counts[TransferStatus.TRANSFER_DELTA_INDETERMINATE],
        expression_path=expression_path,
    )
    status = _classify_signature(value, None if slope_result is None else slope_result.status, counts)

    parent_ids = tuple(transfer.provenance.trace_id for transfer in transfers)
    if slope_result is not None:
        parent_ids = parent_ids + (slope_result.provenance.trace_id,)

    return TypedResult(
        value=value,
        space=SWEEP_SIGNATURE_PROBE_SPACE,
        status=status,
        validity=_validity_for_status(status),
        conditioning=_conditioning_for_status(status, value),
        provenance=Provenance(
            operation_id="sweep_signature_probe",
            expression_path=expression_path,
            precision=precision,
            backend=backend,
            device=device,
            measurement_resolution=measurement_resolution,
            inputs=(probe_id, function_label, _f_grid_descriptor(f_tuple), eta),
            parents=parent_ids,
        ),
        protocol=ProtocolStatus.OK,
    )


def _validate_inputs(
    observable: Callable[[float], float],
    f_values: Sequence[float],
    eta: float,
    function_label: str,
    probe_id: str,
) -> tuple[float, ...]:
    if not callable(observable):
        raise ProtocolViolationError("observable must be callable")
    if not isinstance(function_label, str) or function_label == "":
        raise ProtocolViolationError("function_label must be a non-empty string")
    if not isinstance(probe_id, str) or probe_id == "":
        raise ProtocolViolationError("probe_id must be a non-empty string")
    if isinstance(eta, bool) or not isinstance(eta, int | float) or not math.isfinite(eta) or eta == 0:
        raise ProtocolViolationError("eta must be a finite non-zero real scalar")
    try:
        f_tuple = tuple(f_values)
    except TypeError as exc:
        raise ProtocolViolationError("f_values must be a sequence of finite positive real scalars") from exc
    if not f_tuple:
        raise ProtocolViolationError("f_values must not be empty")
    for value in f_tuple:
        if isinstance(value, bool) or not isinstance(value, int | float) or not math.isfinite(value) or value <= 0:
            raise ProtocolViolationError("f_values must contain only finite positive real scalars")
    return tuple(float(value) for value in f_tuple)


def _transfer_counts(transfers: tuple[TypedResult, ...]) -> dict[TransferStatus, int]:
    return {status: sum(1 for transfer in transfers if transfer.status is status) for status in TransferStatus}


def _regularized_slope_observation(
    slope_result: LogLogSlopeResult,
    transfers: tuple[TypedResult, ...],
    drop_rate: float,
) -> LogLogSlopeObservation:
    if not _all_observed_nonzero(transfers) or drop_rate != 0.0:
        return slope_result.value
    log_span = _nonzero_transfer_log_span(transfers)
    if log_span is None or log_span > CANCELLATION_GRADE_THRESHOLD:
        return slope_result.value
    if slope_result.status is SlopeStatus.SLOPE_OBSERVED and slope_result.value.slope is not None:
        if abs(slope_result.value.slope) > CANCELLATION_GRADE_THRESHOLD:
            return slope_result.value
        return LogLogSlopeObservation(
            slope=0.0,
            intercept=slope_result.value.intercept,
            r_squared=1.0,
            standard_error=0.0,
            n_input_observations=slope_result.value.n_input_observations,
            n_used=slope_result.value.n_used,
            log_f_min=slope_result.value.log_f_min,
            log_f_max=slope_result.value.log_f_max,
            expression_path=slope_result.value.expression_path,
        )
    if slope_result.status is SlopeStatus.SLOPE_DEGENERATE_INPUT:
        return LogLogSlopeObservation(
            slope=0.0,
            intercept=_mean_nonzero_log_transfer(transfers),
            r_squared=1.0,
            standard_error=0.0,
            n_input_observations=slope_result.value.n_input_observations,
            n_used=slope_result.value.n_used,
            log_f_min=slope_result.value.log_f_min,
            log_f_max=slope_result.value.log_f_max,
            expression_path=slope_result.value.expression_path,
        )
    return slope_result.value


def _classify_signature(
    value: SweepSignatureValue,
    slope_status: SlopeStatus | None,
    counts: dict[TransferStatus, int],
) -> SweepSignatureStatus:
    if counts[TransferStatus.TRANSFER_NON_FINITE] == value.n_input:
        return SweepSignatureStatus.SWEEP_SIGNATURE_NONFINITE
    if counts[TransferStatus.TRANSFER_DOMAIN_REFUSED] == value.n_input:
        return SweepSignatureStatus.SWEEP_SIGNATURE_DOMAIN_REFUSED
    if value.n_observed > 0 and value.n_observed == value.n_input and value.slope_observation.n_used == 0:
        return SweepSignatureStatus.SWEEP_SIGNATURE_DEGENERATE_INPUT
    if slope_status is SlopeStatus.SLOPE_DEGENERATE_INPUT and value.slope_observation.r_squared is None:
        return SweepSignatureStatus.SWEEP_SIGNATURE_DEGENERATE_INPUT
    if slope_status is SlopeStatus.SLOPE_INSUFFICIENT_DATA or value.n_observed < MIN_OBSERVATIONS_FOR_FIT:
        return SweepSignatureStatus.SWEEP_SIGNATURE_INSUFFICIENT_DATA
    if value.cancellation_grade > CANCELLATION_GRADE_THRESHOLD:
        return SweepSignatureStatus.SWEEP_SIGNATURE_CANCELLATION_DOMINATED
    if value.drop_rate > DROP_RATE_THRESHOLD:
        return SweepSignatureStatus.SWEEP_SIGNATURE_HIGH_DROP_RATE
    return SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN


def _cancellation_grade(r_squared: float | None) -> float:
    if r_squared is None or not math.isfinite(r_squared):
        return 0.0
    return 1.0 - r_squared


def _all_observed_nonzero(transfers: tuple[TypedResult, ...]) -> bool:
    if not transfers:
        return False
    for transfer in transfers:
        if transfer.status is not TransferStatus.TRANSFER_OBSERVED:
            return False
        transfer_value = transfer.value.transfer
        if not isinstance(transfer_value, int | float) or isinstance(transfer_value, bool):
            return False
        if not math.isfinite(float(transfer_value)) or float(transfer_value) == 0.0:
            return False
    return True


def _nonzero_transfer_log_span(transfers: tuple[TypedResult, ...]) -> float | None:
    logs = []
    for transfer in transfers:
        transfer_value = transfer.value.transfer
        if not isinstance(transfer_value, int | float) or isinstance(transfer_value, bool):
            return None
        transfer_float = float(transfer_value)
        if not math.isfinite(transfer_float) or transfer_float == 0.0:
            return None
        logs.append(log64(abs(transfer_float)))
    if not logs:
        return None
    return max(logs) - min(logs)


def _mean_nonzero_log_transfer(transfers: tuple[TypedResult, ...]) -> float | None:
    logs = []
    for transfer in transfers:
        transfer_value = transfer.value.transfer
        if isinstance(transfer_value, int | float) and not isinstance(transfer_value, bool) and math.isfinite(float(transfer_value)) and float(transfer_value) != 0.0:
            logs.append(log64(abs(float(transfer_value))))
    if not logs:
        return None
    return sum(logs) / len(logs)


def _empty_slope_observation(n_input: int, n_used: int, expression_path: str) -> LogLogSlopeObservation:
    return LogLogSlopeObservation(
        slope=None,
        intercept=None,
        r_squared=None,
        standard_error=None,
        n_input_observations=n_input,
        n_used=n_used,
        log_f_min=None,
        log_f_max=None,
        expression_path=expression_path,
    )


def _f_grid_descriptor(f_values: tuple[float, ...]) -> dict[str, Any]:
    return {
        "count": len(f_values),
        "first": f_values[0],
        "last": f_values[-1],
        "min": min(f_values),
        "max": max(f_values),
        "strictly_decreasing": all(left > right for left, right in zip(f_values, f_values[1:])),
        "strictly_increasing": all(left < right for left, right in zip(f_values, f_values[1:])),
    }


def _validity_for_status(status: SweepSignatureStatus) -> Validity:
    if status is SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN:
        return Validity(defined=True, finite=True, selectable=True, advanceable=True, observable=True)
    if status in {
        SweepSignatureStatus.SWEEP_SIGNATURE_CANCELLATION_DOMINATED,
        SweepSignatureStatus.SWEEP_SIGNATURE_HIGH_DROP_RATE,
        SweepSignatureStatus.SWEEP_SIGNATURE_DEGENERATE_INPUT,
        SweepSignatureStatus.SWEEP_SIGNATURE_INSUFFICIENT_DATA,
    }:
        return Validity(defined=True, finite=True, selectable=False, advanceable=False, observable=True)
    if status is SweepSignatureStatus.SWEEP_SIGNATURE_NONFINITE:
        return Validity(defined=True, finite=False, selectable=False, advanceable=False, observable=True)
    return Validity(defined=False, finite=False, selectable=False, advanceable=False, observable=True)


def _conditioning_for_status(status: SweepSignatureStatus, value: SweepSignatureValue) -> Conditioning:
    notes = (
        f"cancellation_grade={value.cancellation_grade:.6g}",
        f"drop_rate={value.drop_rate:.6g}",
        f"n_observed={value.n_observed}/{value.n_input}",
    )
    if status is SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN:
        return Conditioning(status=ConditioningStatus.WELL_CONDITIONED, notes=notes)
    return Conditioning(status=ConditioningStatus.WARNING, notes=notes)
