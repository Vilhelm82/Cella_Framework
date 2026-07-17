"""Tests for the typed_ulp primitive (GAP-003, IEEE 754 lattice geometry).

Reference: scratch/dry003_ulp_reconciliation_audit.py established the canonical
behaviour these tests enforce.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from lloyd_v4.core.protocols import validate_protocol
from lloyd_v4.core.status import (
    ConditioningStatus,
    ProtocolStatus,
    UlpStatus,
)
from lloyd_v4.primitives import (
    FINITE_TYPED_ULP_PROTOCOL,
    TYPED_ULP_PROTOCOL,
    TypedUlpValue,
    typed_ulp,
)


# IEEE 754 reference constants used in tests.
SMALLEST_SUBNORMAL = 5e-324                  # 2^-1074
SMALLEST_NORMAL = 2.2250738585072014e-308     # 2^-1022
LARGEST_NORMAL = 1.7976931348623157e308       # (2 - 2^-52) * 2^1023


# ---------------------------------------------------------------------------
# Normal-range branch
# ---------------------------------------------------------------------------


def test_ulp_at_one_is_machine_epsilon() -> None:
    """ulp(1.0) = 2^-52 (machine epsilon for float64, binade 0)."""
    r = typed_ulp(1.0)
    assert r.status is UlpStatus.ULP_NORMAL
    assert r.value.ulp == 2.0 ** -52
    assert r.value.binade == 0
    assert r.value.is_subnormal is False
    assert r.value.is_finite is True
    assert r.value.format == "float64"
    assert r.protocol is ProtocolStatus.OK
    assert r.refusal is None


def test_ulp_constant_within_a_binade() -> None:
    """Within [1.0, 2.0), every value shares ulp = 2^-52."""
    for x in (1.0, 1.25, 1.5, 1.99999, 1.9999999999999998):
        r = typed_ulp(x)
        assert r.status is UlpStatus.ULP_NORMAL
        assert r.value.ulp == 2.0 ** -52
        assert r.value.binade == 0


def test_ulp_doubles_across_binades() -> None:
    """ulp at 2.0 is twice ulp at 1.0 (binade 1 vs binade 0)."""
    r0 = typed_ulp(1.0)
    r1 = typed_ulp(2.0)
    assert r0.value.binade == 0
    assert r1.value.binade == 1
    assert r1.value.ulp == 2.0 * r0.value.ulp


def test_ulp_across_many_binades() -> None:
    """ulp at 2^k = 2^(k-52) across a spread of binades."""
    for k in (-100, -10, 0, 10, 100, 500, 1000):
        x = math.ldexp(1.0, k)
        r = typed_ulp(x)
        assert r.status is UlpStatus.ULP_NORMAL, f"k={k}"
        assert r.value.binade == k
        assert r.value.ulp == math.ldexp(1.0, k - 52)


def test_ulp_negative_input_uses_absolute_value() -> None:
    """ulp(-x) == ulp(x); the lattice spacing is sign-symmetric."""
    for x in (1.0, 1.5, 1e-100, 1e+100):
        assert typed_ulp(x).value.ulp == typed_ulp(-x).value.ulp


# ---------------------------------------------------------------------------
# Subnormal branch
# ---------------------------------------------------------------------------


def test_ulp_in_subnormal_region_is_smallest_subnormal() -> None:
    """All subnormals share the uniform spacing 2^-1074."""
    subnormals = [
        math.ldexp(1.0, -1023),
        math.ldexp(1.0, -1030),
        math.ldexp(1.0, -1050),
        math.ldexp(1.0, -1073),
        SMALLEST_SUBNORMAL,
        SMALLEST_NORMAL * 0.5,
    ]
    for x in subnormals:
        r = typed_ulp(x)
        assert r.status is UlpStatus.ULP_SUBNORMAL, f"x={x!r}"
        assert r.value.ulp == SMALLEST_SUBNORMAL
        assert r.value.is_subnormal is True


def test_smallest_normal_is_normal_not_subnormal() -> None:
    """The boundary case x == 2^-1022 sits in the normal range."""
    r = typed_ulp(SMALLEST_NORMAL)
    assert r.status is UlpStatus.ULP_NORMAL
    assert r.value.is_subnormal is False
    assert r.value.binade == -1022


def test_just_below_smallest_normal_is_subnormal() -> None:
    """Values strictly below 2^-1022 are subnormal."""
    r = typed_ulp(SMALLEST_NORMAL * 0.5)
    assert r.status is UlpStatus.ULP_SUBNORMAL
    assert r.value.is_subnormal is True


# ---------------------------------------------------------------------------
# Zero branch
# ---------------------------------------------------------------------------


def test_ulp_at_zero_returns_smallest_subnormal() -> None:
    """ulp(0) is defined as the limit of subnormal spacing toward zero."""
    r = typed_ulp(0.0)
    assert r.status is UlpStatus.ULP_ZERO
    assert r.value.ulp == SMALLEST_SUBNORMAL
    assert r.value.binade is None
    assert r.value.is_subnormal is False
    assert r.value.is_finite is True


def test_ulp_at_negative_zero_returns_smallest_subnormal() -> None:
    """ulp(-0.0) and ulp(+0.0) agree (both return 2^-1074)."""
    assert typed_ulp(-0.0).status is UlpStatus.ULP_ZERO
    assert typed_ulp(-0.0).value.ulp == typed_ulp(0.0).value.ulp


# ---------------------------------------------------------------------------
# At-edge branch
# ---------------------------------------------------------------------------


def test_largest_normal_is_at_edge() -> None:
    """At the top of the representable range, ulp is +inf (no next representable)."""
    r = typed_ulp(LARGEST_NORMAL)
    assert r.status is UlpStatus.ULP_AT_EDGE
    assert math.isinf(r.value.ulp)
    assert r.value.ulp > 0
    assert r.value.binade == 1023
    assert r.value.is_finite is True  # input is finite even though ulp is +inf
    assert r.protocol is ProtocolStatus.OK  # not a refusal — the result is honest
    assert r.refusal is None
    # Validity reflects "input defined, output not finite"
    assert r.validity.defined is True
    assert r.validity.finite is False
    assert r.validity.selectable is False


def test_ulp_at_edge_is_conditioning_singular() -> None:
    """Edge cases have SINGULAR conditioning (no local lattice geometry above)."""
    r = typed_ulp(LARGEST_NORMAL)
    assert r.conditioning.status is ConditioningStatus.SINGULAR


# ---------------------------------------------------------------------------
# Non-finite refusal branches
# ---------------------------------------------------------------------------


def test_positive_infinity_is_refused() -> None:
    """ULP of +inf is undefined; primitive refuses with typed reason."""
    r = typed_ulp(float("inf"))
    assert r.status is UlpStatus.ULP_NONFINITE_INF
    assert r.protocol is ProtocolStatus.SCALARIZATION_REFUSED
    assert r.refusal is not None
    assert "infinity" in r.refusal.reason.lower()
    assert r.value.is_finite is False
    assert r.validity.defined is False


def test_negative_infinity_is_refused() -> None:
    """Sign doesn't matter; -inf is also refused."""
    r = typed_ulp(float("-inf"))
    assert r.status is UlpStatus.ULP_NONFINITE_INF
    assert r.protocol is ProtocolStatus.SCALARIZATION_REFUSED
    assert r.refusal is not None
    assert r.refusal.details["input_value"] == "-inf"


def test_nan_is_refused() -> None:
    """ULP of NaN is undefined; primitive refuses."""
    r = typed_ulp(float("nan"))
    assert r.status is UlpStatus.ULP_NONFINITE_NAN
    assert r.protocol is ProtocolStatus.SCALARIZATION_REFUSED
    assert r.refusal is not None
    assert "nan" in r.refusal.reason.lower()
    assert math.isnan(r.value.ulp)
    assert r.value.is_finite is False
    assert r.validity.defined is False


# ---------------------------------------------------------------------------
# Nextafter-reference cross-check (the canonical IEEE 754 definition)
# ---------------------------------------------------------------------------


def test_matches_nextafter_reference_across_grid() -> None:
    """For every finite non-edge x, typed_ulp(x).ulp == nextafter(|x|, +inf) - |x|."""
    import struct

    def reference_ulp(x: float) -> float:
        """Bit-manipulation nextafter for positive finite floats."""
        a = abs(x)
        bits = struct.unpack(">Q", struct.pack(">d", a))[0]
        return struct.unpack(">d", struct.pack(">Q", bits + 1))[0] - a

    grid = [
        1.0, 1.5, 2.0, 3.14159, 1e-5, 1e-100, 1e+100,
        SMALLEST_NORMAL, SMALLEST_NORMAL * 0.5, SMALLEST_SUBNORMAL,
        math.ldexp(1.0, -1050), math.ldexp(1.0, -500), math.ldexp(1.0, 500),
    ]
    for x in grid:
        if x == 0.0:
            continue
        r = typed_ulp(x)
        if r.status is UlpStatus.ULP_AT_EDGE:
            continue
        expected = reference_ulp(x)
        assert r.value.ulp == expected, f"x={x!r}: got {r.value.ulp}, expected {expected}"


def test_corrects_mcg_subnormal_underflow_bug() -> None:
    """DRY-003 finding: mcg_phase_1's ulp_float64 underflowed to 0 on subnormals.

    typed_ulp must NOT underflow: subnormals return 2^-1074 (the uniform
    subnormal spacing), never 0.0.
    """
    for k in (-1023, -1030, -1050, -1073, -1074):
        x = math.ldexp(1.0, k)
        if x == 0.0:
            continue
        r = typed_ulp(x)
        assert r.value.ulp > 0.0, f"subnormal 2^{k} must not underflow to 0"
        assert r.value.ulp == SMALLEST_SUBNORMAL


# ---------------------------------------------------------------------------
# Provenance and structural fields
# ---------------------------------------------------------------------------


def test_provenance_records_operation_id_and_input() -> None:
    r = typed_ulp(1.5)
    assert r.provenance.operation_id == "typed_ulp"
    assert r.provenance.inputs == (1.5,)
    assert r.provenance.parents == ()  # L1 primitive; no parent typed results
    assert r.provenance.precision == "float64"
    assert "1.5" in r.provenance.expression_path


def test_trace_id_is_deterministic_for_same_input() -> None:
    """Same input → same trace_id (used for replay and provenance equivalence)."""
    a = typed_ulp(1.0)
    b = typed_ulp(1.0)
    assert a.provenance.trace_id == b.provenance.trace_id


def test_trace_id_differs_for_different_inputs() -> None:
    a = typed_ulp(1.0)
    b = typed_ulp(2.0)
    assert a.provenance.trace_id != b.provenance.trace_id


# ---------------------------------------------------------------------------
# Protocol validation
# ---------------------------------------------------------------------------


def test_producer_protocol_validates() -> None:
    """Every produced status must be declared in TYPED_ULP_PROTOCOL.emitted_statuses."""
    for x in (1.0, 0.0, SMALLEST_SUBNORMAL, LARGEST_NORMAL, float("inf"), float("nan")):
        r = typed_ulp(x)
        assert r.status in TYPED_ULP_PROTOCOL.emitted_statuses, (
            f"produced undeclared status {r.status!r} for x={x!r}"
        )
    # Required producer fields are present on every result.
    sample = typed_ulp(1.0)
    for field in TYPED_ULP_PROTOCOL.required_fields:
        assert getattr(sample, field, None) is not None, f"missing producer field {field!r}"


def test_finite_consumer_protocol_accepts_finite_results() -> None:
    """Finite-only consumer accepts ULP_NORMAL/SUBNORMAL/ZERO."""
    for x in (1.0, 1e-100, SMALLEST_SUBNORMAL, 0.0):
        r = typed_ulp(x)
        verdict = validate_protocol(r, FINITE_TYPED_ULP_PROTOCOL)
        assert verdict.ok, f"finite-consumer should accept x={x!r}: {verdict}"


def test_finite_consumer_protocol_refuses_edge_and_nonfinite() -> None:
    """Finite-only consumer refuses ULP_AT_EDGE / ULP_NONFINITE_*."""
    for x in (LARGEST_NORMAL, float("inf"), float("nan")):
        r = typed_ulp(x)
        verdict = validate_protocol(r, FINITE_TYPED_ULP_PROTOCOL)
        assert not verdict.ok, f"finite-consumer should refuse x={x!r}"


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------


def test_result_serializes_to_json_safe_dict() -> None:
    r = typed_ulp(1.5)
    payload = r.to_json_safe()
    assert payload["space"] == "TypedUlp"
    assert payload["status"] == "ulp_normal"
    assert payload["value"]["ulp"] == 2.0 ** -52
    assert payload["value"]["binade"] == 0
    assert payload["value"]["is_subnormal"] is False
    assert payload["value"]["format"] == "float64"
    # Round-trip through JSON to confirm pure-stdlib JSON-safety
    json.dumps(payload)


def test_refusal_result_serializes_with_reason() -> None:
    r = typed_ulp(float("nan"))
    payload = r.to_json_safe()
    assert payload["status"] == "ulp_nonfinite_nan"
    assert payload["refusal"] is not None
    assert "nan" in payload["refusal"]["reason"].lower()
    json.dumps(payload)


def test_edge_result_serializes_inf_value() -> None:
    """At-edge result has ulp=+inf; JSON-safe form should preserve this."""
    r = typed_ulp(LARGEST_NORMAL)
    payload = r.to_json_safe()
    assert payload["status"] == "ulp_at_edge"
    # to_json_safe may represent +inf as the string "Infinity" or similar;
    # either way, the round-trip should not raise.
    json_dump = json.dumps(payload, default=str)
    assert "ulp_at_edge" in json_dump


# ===========================================================================
# Float32 precision path (GAP-003 extension)
#
# These tests exercise typed_ulp(x, precision="float32") in parallel to the
# float64 tests above. Reference: IEEE 754 binary32 (23 mantissa bits, smallest
# subnormal 2^-149, smallest normal 2^-126).
# ===========================================================================


# IEEE 754 binary32 reference constants
F32_SMALLEST_SUBNORMAL = 2.0 ** -149
F32_SMALLEST_NORMAL = 2.0 ** -126
F32_LARGEST_NORMAL = 3.4028234663852886e38


def test_float32_at_one_is_machine_epsilon() -> None:
    """ulp(1.0, precision='float32') = 2^-23 (binary32 machine epsilon)."""
    r = typed_ulp(1.0, precision="float32")
    assert r.status is UlpStatus.ULP_NORMAL
    assert r.value.ulp == 2.0 ** -23
    assert r.value.binade == 0
    assert r.value.is_subnormal is False
    assert r.value.is_finite is True
    assert r.value.format == "float32"
    assert r.protocol is ProtocolStatus.OK
    assert r.refusal is None


def test_float32_constant_within_a_binade() -> None:
    """Within [1.0, 2.0), every float32-representable value shares ulp = 2^-23."""
    for x in (1.0, 1.25, 1.5, 1.875):
        r = typed_ulp(x, precision="float32")
        assert r.status is UlpStatus.ULP_NORMAL
        assert r.value.ulp == 2.0 ** -23
        assert r.value.binade == 0


def test_float32_doubles_across_binades() -> None:
    """ulp at 2.0 in float32 is twice ulp at 1.0."""
    r0 = typed_ulp(1.0, precision="float32")
    r1 = typed_ulp(2.0, precision="float32")
    assert r0.value.binade == 0
    assert r1.value.binade == 1
    assert r1.value.ulp == 2.0 * r0.value.ulp


def test_float32_subnormal_region_uniform_spacing() -> None:
    """All float32 subnormals share spacing 2^-149."""
    for k in (-127, -130, -140, -148, -149):
        x = math.ldexp(1.0, k)
        r = typed_ulp(x, precision="float32")
        assert r.status is UlpStatus.ULP_SUBNORMAL, f"k={k}: status={r.status}"
        assert r.value.ulp == F32_SMALLEST_SUBNORMAL
        assert r.value.is_subnormal is True
        assert r.value.format == "float32"


def test_float32_smallest_normal_is_normal() -> None:
    """Boundary 2^-126 sits in the float32 normal range."""
    r = typed_ulp(F32_SMALLEST_NORMAL, precision="float32")
    assert r.status is UlpStatus.ULP_NORMAL
    assert r.value.is_subnormal is False
    assert r.value.binade == -126


def test_float32_at_zero_returns_smallest_subnormal() -> None:
    """ulp(0.0, precision='float32') = 2^-149."""
    r = typed_ulp(0.0, precision="float32")
    assert r.status is UlpStatus.ULP_ZERO
    assert r.value.ulp == F32_SMALLEST_SUBNORMAL
    assert r.value.binade is None
    assert r.value.format == "float32"


def test_float32_largest_normal_is_at_edge() -> None:
    """Largest float32 normal: ulp is +inf (no next representable above)."""
    r = typed_ulp(F32_LARGEST_NORMAL, precision="float32")
    assert r.status is UlpStatus.ULP_AT_EDGE
    assert math.isinf(r.value.ulp) and r.value.ulp > 0
    assert r.value.binade == 127
    assert r.value.format == "float32"


def test_float32_overflow_input_routed_to_nonfinite_inf() -> None:
    """A float64 input above float32 range rounds to +/-inf in float32; refuse."""
    for x in (1e+39, 1e+50, 1e+100):
        r = typed_ulp(x, precision="float32")
        assert r.status is UlpStatus.ULP_NONFINITE_INF, f"x={x!r}: {r.status}"
        assert r.protocol is ProtocolStatus.SCALARIZATION_REFUSED
        assert r.refusal is not None
        # Refusal should record the original float64 input for traceability
        assert "original_float64" in r.refusal.details


def test_float32_input_rounded_to_float32_first() -> None:
    """Float32 path rounds the input to float32 representation first. 0.1 is
    not exactly representable in float32; its float32 approximation has a
    different binade ulp than the float64 approximation would."""
    r32 = typed_ulp(0.1, precision="float32")
    r64 = typed_ulp(0.1, precision="float64")
    # 0.1 in float32 sits in [2^-4, 2^-3); ulp = 2^-27
    assert r32.value.ulp == 2.0 ** -27
    # 0.1 in float64 sits in [2^-4, 2^-3); ulp = 2^-56
    assert r64.value.ulp == 2.0 ** -56
    assert r32.value.ulp > r64.value.ulp


def test_float32_negative_inputs_use_absolute_value() -> None:
    """ulp(-x, precision='float32') == ulp(x, precision='float32')."""
    for x in (1.0, 1e-10, 1e+10):
        a = typed_ulp(x, precision="float32").value.ulp
        b = typed_ulp(-x, precision="float32").value.ulp
        assert a == b


def test_float32_nan_refused() -> None:
    """ULP of NaN in float32 is refused (parallel to float64)."""
    r = typed_ulp(float("nan"), precision="float32")
    assert r.status is UlpStatus.ULP_NONFINITE_NAN
    assert r.protocol is ProtocolStatus.SCALARIZATION_REFUSED
    assert r.refusal is not None
    assert r.refusal.details.get("format") == "float32"


def test_float32_infinity_refused() -> None:
    """ULP of +/-inf in float32 is refused."""
    for x in (float("inf"), float("-inf")):
        r = typed_ulp(x, precision="float32")
        assert r.status is UlpStatus.ULP_NONFINITE_INF
        assert r.protocol is ProtocolStatus.SCALARIZATION_REFUSED


def test_float32_provenance_records_precision() -> None:
    """Provenance.precision and expression_path reflect the float32 path."""
    r = typed_ulp(1.0, precision="float32")
    assert r.provenance.precision == "float32"
    assert "float32" in r.provenance.expression_path
    assert r.provenance.operation_id == "typed_ulp"
    assert r.provenance.parents == ()


def test_dispatcher_default_is_float64() -> None:
    """Calling typed_ulp(x) with no precision kwarg uses the float64 path."""
    r = typed_ulp(1.0)
    assert r.value.format == "float64"
    assert r.value.ulp == 2.0 ** -52
    assert r.provenance.precision == "float64"


def test_dispatcher_rejects_unknown_precision() -> None:
    """Unknown precision strings raise ValueError."""
    for bad in ("float128", "bfloat16", "double", "", "FLOAT64"):
        with pytest.raises(ValueError, match="unsupported precision"):
            typed_ulp(1.0, precision=bad)


def test_dispatcher_format_kwarg_no_longer_accepted() -> None:
    """Regression test: the kwarg was renamed format -> precision. The old
    name must not silently accept (avoid two parallel APIs)."""
    with pytest.raises(TypeError):
        typed_ulp(1.0, format="float32")


def test_float32_and_float64_paths_disagree_when_lattice_differs() -> None:
    """For values where the two lattices have different spacing, the typed
    results must reflect that difference (not silently collapse)."""
    # 1.0 is exactly representable in both formats; ulp differs by ~2^29
    r32 = typed_ulp(1.0, precision="float32")
    r64 = typed_ulp(1.0, precision="float64")
    assert r32.value.ulp > r64.value.ulp
    assert r32.value.format != r64.value.format
    # Provenance trace_id should differ since precision is in the trace seed
    assert r32.provenance.trace_id != r64.provenance.trace_id


def test_float32_consumer_protocol_still_accepts_subnormal() -> None:
    """FINITE_TYPED_ULP_PROTOCOL is precision-agnostic; it accepts float32
    subnormal results the same way it accepts float64 ones."""
    r = typed_ulp(F32_SMALLEST_SUBNORMAL, precision="float32")
    verdict = validate_protocol(r, FINITE_TYPED_ULP_PROTOCOL)
    assert verdict.ok


def test_float32_result_serializes_to_json_safe() -> None:
    r = typed_ulp(1.0, precision="float32")
    payload = r.to_json_safe()
    assert payload["value"]["format"] == "float32"
    assert payload["value"]["ulp"] == 2.0 ** -23
    assert payload["provenance"]["precision"] == "float32"
    json.dumps(payload)
