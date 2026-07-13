"""Cella-native IEEE 754 lattice geometry primitive.

This is the local Cella port of V4's ``typed_ulp`` method: same reference
computation, stripped of the V4 protocol/result stack.  It gives Cella one
canonical source for float lattice spacing instead of scattered ``math.ulp``
or hand-written ULP helpers.
"""

from __future__ import annotations

from fractions import Fraction
import math
import struct


FLOAT64_SMALLEST_SUBNORMAL = Fraction(1, 2**1074)
FLOAT64_SMALLEST_NORMAL = math.ldexp(1.0, -1022)
FLOAT32_SMALLEST_SUBNORMAL = Fraction(1, 2**149)
FLOAT32_SMALLEST_NORMAL = math.ldexp(1.0, -126)

_FLOAT64_MAX_BITS = 0x7FEFFFFFFFFFFFFF
_FLOAT32_MAX_BITS = 0x7F7FFFFF


def typed_ulp(x: float, *, precision: str = "float64") -> dict:
    """Return the local IEEE lattice spacing at ``x``.

    ``precision`` accepts ``float64``/``binary64`` and ``float32``/``binary32``.
    The returned record is JSON-ready, but the ULP is carried as exact rational
    text so callers can reconstruct it losslessly with ``Fraction(record["ulp"])``.
    """

    normalized = _normalize_precision(precision)
    if normalized == "float64":
        return _typed_ulp_float64(float(x))
    return _typed_ulp_float32(float(x))


def ulp_record(x: float, *, precision: str = "float64") -> dict:
    return typed_ulp(x, precision=precision)


def ulp_fraction(x: float, *, precision: str = "float64") -> Fraction:
    record = typed_ulp(x, precision=precision)
    if record["ulp"] is None:
        raise ValueError(f"ULP is undefined for {x!r} in {record['format']}")
    return Fraction(record["ulp"])


def _typed_ulp_float64(x_float: float) -> dict:
    if math.isnan(x_float):
        return _record(
            status="ULP_NONFINITE_NAN",
            input_value=x_float,
            ulp=None,
            binade=None,
            is_subnormal=False,
            is_finite=False,
            format_label="float64",
        )
    if math.isinf(x_float):
        return _record(
            status="ULP_NONFINITE_INF",
            input_value=x_float,
            ulp=None,
            binade=None,
            is_subnormal=False,
            is_finite=False,
            format_label="float64",
        )

    absolute = abs(x_float)
    if absolute == 0.0:
        return _record(
            status="ULP_ZERO",
            input_value=x_float,
            ulp=FLOAT64_SMALLEST_SUBNORMAL,
            binade=None,
            is_subnormal=False,
            is_finite=True,
            format_label="float64",
        )

    if _bits_from_float64(absolute) >= _FLOAT64_MAX_BITS:
        return _record(
            status="ULP_AT_EDGE",
            input_value=x_float,
            ulp=None,
            binade=None,
            is_subnormal=False,
            is_finite=True,
            format_label="float64",
        )

    _, exponent = math.frexp(absolute)
    binade = exponent - 1
    is_subnormal = absolute < FLOAT64_SMALLEST_NORMAL
    next_value = _next_representable_above_float64(absolute)
    ulp = Fraction.from_float(next_value) - Fraction.from_float(absolute)
    return _record(
        status="ULP_SUBNORMAL" if is_subnormal else "ULP_NORMAL",
        input_value=x_float,
        ulp=ulp,
        binade=binade,
        is_subnormal=is_subnormal,
        is_finite=True,
        format_label="float64",
    )


def _typed_ulp_float32(x_float: float) -> dict:
    if math.isnan(x_float):
        return _record(
            status="ULP_NONFINITE_NAN",
            input_value=x_float,
            ulp=None,
            binade=None,
            is_subnormal=False,
            is_finite=False,
            format_label="float32",
        )

    x_f32 = _round_to_float32(x_float)
    if math.isinf(x_f32):
        return _record(
            status="ULP_NONFINITE_INF",
            input_value=x_float,
            ulp=None,
            binade=None,
            is_subnormal=False,
            is_finite=False,
            format_label="float32",
            observed_value=x_f32,
        )

    absolute = abs(x_f32)
    if absolute == 0.0:
        return _record(
            status="ULP_ZERO",
            input_value=x_float,
            ulp=FLOAT32_SMALLEST_SUBNORMAL,
            binade=None,
            is_subnormal=False,
            is_finite=True,
            format_label="float32",
            observed_value=x_f32,
        )

    if _bits_from_float32(absolute) >= _FLOAT32_MAX_BITS:
        return _record(
            status="ULP_AT_EDGE",
            input_value=x_float,
            ulp=None,
            binade=None,
            is_subnormal=False,
            is_finite=True,
            format_label="float32",
            observed_value=x_f32,
        )

    _, exponent = math.frexp(absolute)
    binade = exponent - 1
    is_subnormal = absolute < FLOAT32_SMALLEST_NORMAL
    next_value = _next_representable_above_float32(absolute)
    ulp = Fraction.from_float(next_value) - Fraction.from_float(absolute)
    return _record(
        status="ULP_SUBNORMAL" if is_subnormal else "ULP_NORMAL",
        input_value=x_float,
        ulp=ulp,
        binade=binade,
        is_subnormal=is_subnormal,
        is_finite=True,
        format_label="float32",
        observed_value=x_f32,
    )


def _record(
    *,
    status: str,
    input_value: float,
    ulp: Fraction | None,
    binade: int | None,
    is_subnormal: bool,
    is_finite: bool,
    format_label: str,
    observed_value: float | None = None,
) -> dict:
    ulp_text = None if ulp is None else _fraction_text(ulp)
    observed = input_value if observed_value is None else observed_value
    return {
        "status": status,
        "input": _float_record(input_value),
        "observed": _float_record(observed),
        "ulp": ulp_text,
        "binade": None if binade is None else str(binade),
        "binade_int": binade,
        "is_subnormal": is_subnormal,
        "is_finite": is_finite,
        "format": format_label,
        "method": "typed_ulp_next_representable_ieee754",
        "value": {
            "ulp": ulp_text,
            "input_value": _float_text(input_value),
            "observed_value": _float_text(observed),
            "binade": binade,
            "is_subnormal": is_subnormal,
            "is_finite": is_finite,
            "format": format_label,
        },
    }


def _normalize_precision(precision: str) -> str:
    key = str(precision).strip().lower()
    if key in {"float64", "binary64"}:
        return "float64"
    if key in {"float32", "binary32"}:
        return "float32"
    raise ValueError("typed_ulp precision must be float64/binary64 or float32/binary32")


def _bits_from_float64(x: float) -> int:
    return struct.unpack(">Q", struct.pack(">d", x))[0]


def _float64_from_bits(bits: int) -> float:
    return struct.unpack(">d", struct.pack(">Q", bits & 0xFFFFFFFFFFFFFFFF))[0]


def _next_representable_above_float64(x_positive_finite: float) -> float:
    return _float64_from_bits(_bits_from_float64(x_positive_finite) + 1)


def _round_to_float32(x: float) -> float:
    try:
        return struct.unpack(">f", struct.pack(">f", x))[0]
    except OverflowError:
        return float("inf") if x > 0 else float("-inf")


def _bits_from_float32(x_as_float32: float) -> int:
    return struct.unpack(">L", struct.pack(">f", x_as_float32))[0]


def _float32_from_bits(bits: int) -> float:
    return struct.unpack(">f", struct.pack(">L", bits & 0xFFFFFFFF))[0]


def _next_representable_above_float32(x_positive_finite_f32: float) -> float:
    return _float32_from_bits(_bits_from_float32(x_positive_finite_f32) + 1)


def _float_record(value: float) -> dict:
    return {
        "hex": value.hex(),
        "fraction": None if not math.isfinite(value) else _fraction_text(Fraction.from_float(value)),
    }


def _float_text(value: float) -> str:
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "inf" if value > 0 else "-inf"
    return value.hex()


def _fraction_text(value: Fraction) -> str:
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"
