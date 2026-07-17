import math

import pytest

from lloyd_v4.core.errors import ProtocolViolationError
from lloyd_v4.core.status import SlopeStatus, SweepSignatureStatus, TransferStatus
from lloyd_v4.observers import (
    CANCELLATION_GRADE_THRESHOLD,
    DROP_RATE_THRESHOLD,
    MIN_OBSERVATIONS_FOR_FIT,
    sweep_signature_probe,
)
from lloyd_v4.observers.sweep_signature_probe import _classify_signature
from lloyd_v4.primitives.typed_log_log_slope import LogLogSlopeObservation
from lloyd_v4.observers.sweep_signature_probe import SweepSignatureValue


F_VALUES = tuple(10.0 ** (-1.0 + (-8.0 / 7.0) * index) for index in range(8))
ETA = 3e-7


def _f1(r: float, b: float, m: float) -> float:
    return b * (r - 2.0 * m) - r**3


def _f2(r: float, b: float, m: float) -> float:
    return b * r - 3.0 * r**3


def _naive_observable(form, direction: tuple[float, float, float]):
    point = (3.0, 27.0, 1.0)

    def observable(f: float) -> float:
        return form(
            point[0] + f * direction[0],
            point[1] + f * direction[1],
            point[2] + f * direction[2],
        )

    return observable


GR_CASES = (
    ("stable", "F1_along_r", lambda f: -9.0 * f**2 - f**3, SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("stable", "F1_along_B", lambda f: f, SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("stable", "F1_along_M", lambda f: -54.0 * f, SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("stable", "F2_along_r", lambda f: -54.0 * f - 27.0 * f**2 - 3.0 * f**3, SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("stable", "F2_along_B", lambda f: 3.0 * f, SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("stable", "F2_along_M", lambda f: 0.0, SweepSignatureStatus.SWEEP_SIGNATURE_DEGENERATE_INPUT),
    ("stable", "F1_along_tangent", lambda f: -27.0 * f**2 - 27.0 * f**3, SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("stable", "F2_along_tangent", lambda f: -81.0 * f**2 - 81.0 * f**3, SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("naive", "F1_along_r", _naive_observable(_f1, (1.0, 0.0, 0.0)), SweepSignatureStatus.SWEEP_SIGNATURE_CANCELLATION_DOMINATED),
    ("naive", "F1_along_B", _naive_observable(_f1, (0.0, 1.0, 0.0)), SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("naive", "F1_along_M", _naive_observable(_f1, (0.0, 0.0, 1.0)), SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("naive", "F2_along_r", _naive_observable(_f2, (1.0, 0.0, 0.0)), SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("naive", "F2_along_B", _naive_observable(_f2, (0.0, 1.0, 0.0)), SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN),
    ("naive", "F2_along_M", _naive_observable(_f2, (0.0, 0.0, 1.0)), SweepSignatureStatus.SWEEP_SIGNATURE_DEGENERATE_INPUT),
    ("naive", "F1_along_tangent", _naive_observable(_f1, (3.0, 54.0, 1.0)), SweepSignatureStatus.SWEEP_SIGNATURE_CANCELLATION_DOMINATED),
    ("naive", "F2_along_tangent", _naive_observable(_f2, (3.0, 54.0, 1.0)), SweepSignatureStatus.SWEEP_SIGNATURE_CANCELLATION_DOMINATED),
)


@pytest.mark.parametrize(("form_kind", "label", "observable", "expected"), GR_CASES)
def test_gr_photon_sphere_calibration_cases(form_kind, label, observable, expected) -> None:
    result = sweep_signature_probe(
        observable,
        F_VALUES,
        eta=ETA,
        function_label=f"{form_kind}_{label}",
        probe_id=f"{form_kind}_{label}",
    )

    assert result.status is expected
    assert result.value.n_input == len(F_VALUES)
    assert result.value.drop_rate <= 1.0


def test_gr_calibration_partition_counts() -> None:
    statuses = [
        sweep_signature_probe(
            observable,
            F_VALUES,
            eta=ETA,
            function_label=f"{form_kind}_{label}",
            probe_id=f"{form_kind}_{label}",
        ).status
        for form_kind, label, observable, _expected in GR_CASES
    ]

    assert statuses.count(SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN) == 11
    assert statuses.count(SweepSignatureStatus.SWEEP_SIGNATURE_CANCELLATION_DOMINATED) == 3
    assert statuses.count(SweepSignatureStatus.SWEEP_SIGNATURE_DEGENERATE_INPUT) == 2


def test_f1_along_b_naive_is_sub_limit_clean() -> None:
    result = sweep_signature_probe(
        _naive_observable(_f1, (0.0, 1.0, 0.0)),
        F_VALUES,
        eta=ETA,
        function_label="naive_F1_along_B",
        probe_id="naive_F1_along_B",
    )

    assert result.status is SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN
    assert result.value.cancellation_grade < CANCELLATION_GRADE_THRESHOLD
    assert result.value.drop_rate < DROP_RATE_THRESHOLD


def test_high_drop_rate_with_mixed_finite_nonfinite_cells() -> None:
    result = sweep_signature_probe(
        lambda f: f * f if f >= 0.03 else math.inf,
        (1.0, 0.3, 0.1, 0.03, 0.01, 0.003),
        eta=ETA,
        function_label="mixed_nonfinite",
        probe_id="mixed_nonfinite",
    )

    assert result.status is SweepSignatureStatus.SWEEP_SIGNATURE_HIGH_DROP_RATE
    assert result.value.drop_rate > DROP_RATE_THRESHOLD
    assert result.value.n_nonfinite == 2
    assert result.value.n_observed >= MIN_OBSERVATIONS_FOR_FIT


def test_nonfinite_every_cell() -> None:
    result = sweep_signature_probe(lambda f: math.inf, F_VALUES, eta=ETA, function_label="inf", probe_id="inf")

    assert result.status is SweepSignatureStatus.SWEEP_SIGNATURE_NONFINITE
    assert result.value.n_nonfinite == len(F_VALUES)
    assert result.value.slope_observation.n_used == 0


def test_domain_refused_every_cell() -> None:
    def raises(_f: float) -> float:
        raise ValueError("outside")

    result = sweep_signature_probe(raises, F_VALUES, eta=ETA, function_label="raises", probe_id="raises")

    assert result.status is SweepSignatureStatus.SWEEP_SIGNATURE_DOMAIN_REFUSED
    assert result.value.n_domain_refused == len(F_VALUES)
    assert result.value.slope_observation.n_used == 0


def test_insufficient_data_fewer_than_three_cells() -> None:
    result = sweep_signature_probe(lambda f: f * f, F_VALUES[:2], eta=ETA, function_label="two", probe_id="two")

    assert result.status is SweepSignatureStatus.SWEEP_SIGNATURE_INSUFFICIENT_DATA
    assert result.value.n_observed == 2
    assert result.value.slope_observation.n_used == 2


def test_constant_zero_observable_is_degenerate_input() -> None:
    result = sweep_signature_probe(lambda f: 0.0, F_VALUES, eta=ETA, function_label="zero", probe_id="zero")

    assert result.status is SweepSignatureStatus.SWEEP_SIGNATURE_DEGENERATE_INPUT
    assert result.value.n_observed == len(F_VALUES)
    assert result.value.slope_observation.n_used == 0


def test_input_validation_raises() -> None:
    with pytest.raises(ProtocolViolationError):
        sweep_signature_probe(42, F_VALUES, eta=ETA, function_label="x", probe_id="x")
    with pytest.raises(ProtocolViolationError):
        sweep_signature_probe(lambda f: f, (), eta=ETA, function_label="x", probe_id="x")
    with pytest.raises(ProtocolViolationError):
        sweep_signature_probe(lambda f: f, (-1.0,), eta=ETA, function_label="x", probe_id="x")
    with pytest.raises(ProtocolViolationError):
        sweep_signature_probe(lambda f: f, F_VALUES, eta=0.0, function_label="x", probe_id="x")
    with pytest.raises(ProtocolViolationError):
        sweep_signature_probe(lambda f: f, F_VALUES, eta=ETA, function_label="", probe_id="x")
    with pytest.raises(ProtocolViolationError):
        sweep_signature_probe(lambda f: f, F_VALUES, eta=ETA, function_label="x", probe_id="")


def test_cancellation_grade_boundary_cases() -> None:
    above = _fake_value(r_squared=1.0 - CANCELLATION_GRADE_THRESHOLD - 1e-12)
    exact = _fake_value(r_squared=1.0 - CANCELLATION_GRADE_THRESHOLD)
    below = _fake_value(r_squared=1.0 - CANCELLATION_GRADE_THRESHOLD + 1e-12)
    counts = {status: 0 for status in TransferStatus}
    counts[TransferStatus.TRANSFER_OBSERVED] = above.n_input

    assert _classify_signature(above, SlopeStatus.SLOPE_OBSERVED, counts) is SweepSignatureStatus.SWEEP_SIGNATURE_CANCELLATION_DOMINATED
    assert _classify_signature(exact, SlopeStatus.SLOPE_OBSERVED, counts) is SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN
    assert _classify_signature(below, SlopeStatus.SLOPE_OBSERVED, counts) is SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN


def _fake_value(r_squared: float) -> SweepSignatureValue:
    return SweepSignatureValue(
        cancellation_grade=1.0 - r_squared,
        drop_rate=0.0,
        slope_observation=LogLogSlopeObservation(
            slope=1.0,
            intercept=0.0,
            r_squared=r_squared,
            standard_error=0.0,
            n_input_observations=5,
            n_used=5,
            log_f_min=-5.0,
            log_f_max=-1.0,
            expression_path="boundary",
        ),
        n_input=5,
        n_observed=5,
        n_dropped=0,
        n_nonfinite=0,
        n_domain_refused=0,
        n_cancellation_dominated=0,
        n_delta_indeterminate=0,
        expression_path="boundary",
    )
