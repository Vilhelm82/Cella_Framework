"""Cella-native constructive elementary functions.

Local Cella port of the V4 certified-precision-spine observer family:
``typed_refine``, ``log_eval``, ``exp_eval``, ``pi_eval``, and the typed
elementary wrappers built from exact rational enclosures.  This module is
deliberately self-contained: no libm transcendental calls, no mpmath, no
SymPy, no runtime dependency on V4.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from fractions import Fraction
from typing import Callable, Protocol


class EvalDomainRefusal(ValueError):
    """Raised when a constructive evaluator refuses an input domain."""


class LogDomainError(EvalDomainRefusal):
    pass


class AsinDomainError(EvalDomainRefusal):
    pass


class AcosDomainError(EvalDomainRefusal):
    pass


class PowDomainError(EvalDomainRefusal):
    pass


class TanPoleRefusal(EvalDomainRefusal):
    pass


class RefineStatus(StrEnum):
    REFINED_CORRECTLY_ROUNDED = "refined_correctly_rounded"
    REFINED_BUDGET_EXCEEDED = "refined_budget_exceeded"
    REFINED_DOMAIN_REFUSED = "refined_domain_refused"


@dataclass(frozen=True, slots=True)
class RationalEnclosure:
    lo: Fraction
    hi: Fraction

    @property
    def width(self) -> Fraction:
        return self.hi - self.lo

    def to_record(self) -> dict:
        return {
            "lo": _fraction_text(self.lo),
            "hi": _fraction_text(self.hi),
            "width": _fraction_text(self.width),
        }

    def __getitem__(self, key: str):
        return self.to_record()[key]


class _Enclosure(Protocol):
    @property
    def lo(self) -> Fraction: ...

    @property
    def hi(self) -> Fraction: ...


_INITIAL_HEADROOM = 2
_ONE_THIRD = Fraction(1, 3)
_TWO = Fraction(2)
_POLE_SEPARATION_CEILING = 2048


def typed_refine(
    eval_atom: Callable[[Fraction, int], _Enclosure],
    x,
    required_precision: int,
    *,
    ceiling: int | None = None,
) -> dict:
    """Decide the correctly rounded p-bit value of ``eval_atom(x)`` or refuse."""

    if required_precision <= 0:
        raise ValueError("required_precision must be positive")
    x_q = _fraction_input(x)
    p = int(required_precision)
    cap = bundschuh_ceiling(p) if ceiling is None else int(ceiling)
    working_bits = p + _INITIAL_HEADROOM
    iterations = 0
    while True:
        iterations += 1
        try:
            enclosure = eval_atom(x_q, working_bits)
        except EvalDomainRefusal:
            return _refine_record(
                RefineStatus.REFINED_DOMAIN_REFUSED,
                None,
                working_bits,
                iterations,
            )

        rounded_lo = round_to_p_bits(enclosure.lo, p)
        rounded_hi = round_to_p_bits(enclosure.hi, p)
        if rounded_lo == rounded_hi:
            return _refine_record(
                RefineStatus.REFINED_CORRECTLY_ROUNDED,
                rounded_lo,
                working_bits,
                iterations,
            )

        if working_bits >= cap:
            return _refine_record(
                RefineStatus.REFINED_BUDGET_EXCEEDED,
                None,
                working_bits,
                iterations,
            )
        working_bits = min(working_bits * 2, cap)


def bundschuh_ceiling(required_precision: int) -> int:
    return max(64, int(required_precision) * int(required_precision))


def round_to_p_bits(value: Fraction, p: int) -> Fraction:
    if p <= 0:
        raise ValueError("p must be positive")
    value = Fraction(value)
    if value == 0:
        return Fraction(0)
    sign = 1 if value > 0 else -1
    absolute = value if value > 0 else -value
    exponent = _floor_log2(absolute)
    shift = exponent - (p - 1)
    scaled = absolute / (1 << shift) if shift >= 0 else absolute * (1 << -shift)
    rounded = _round_half_to_even(scaled)
    if shift >= 0:
        return Fraction(sign * rounded * (1 << shift))
    return Fraction(sign * rounded, 1 << -shift)


def log_eval(x, working_bits: int) -> RationalEnclosure:
    x_q = _fraction_input(x)
    if x_q <= 0:
        raise LogDomainError(f"log_eval domain: x must be > 0, got {x_q}")
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")

    target = Fraction(1, 1 << int(working_bits))
    exponent, mantissa = _binade_reduce(x_q)
    z = (mantissa - 1) / (mantissa + 1)
    log_mant = _two_atanh_enclosure(z, target / 2)
    if exponent == 0:
        return log_mant

    log2_budget = (target / 2) / abs(exponent)
    log2 = _two_atanh_enclosure(_ONE_THIRD, log2_budget)
    if exponent > 0:
        return RationalEnclosure(log_mant.lo + exponent * log2.lo, log_mant.hi + exponent * log2.hi)
    return RationalEnclosure(log_mant.lo + exponent * log2.hi, log_mant.hi + exponent * log2.lo)


def exp_eval(x, working_bits: int) -> RationalEnclosure:
    x_q = _fraction_input(x)
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")

    target = Fraction(1, 1 << int(working_bits))
    if x_q >= 0:
        return _exp_nonnegative(x_q, target)
    positive = _exp_nonnegative(-x_q, target)
    return RationalEnclosure(1 / positive.hi, 1 / positive.lo)


def pi_eval(working_bits: int) -> RationalEnclosure:
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")
    target = Fraction(1, 1 << int(working_bits))
    a5 = _arctan_recip(5, target / 32)
    a239 = _arctan_recip(239, target / 8)
    return RationalEnclosure(16 * a5.lo - 4 * a239.hi, 16 * a5.hi - 4 * a239.lo)


def sin_eval(x, working_bits: int) -> RationalEnclosure:
    x_q = _fraction_input(x)
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")
    target = Fraction(1, 1 << int(working_bits))
    internal = int(working_bits) + 16
    while True:
        pi_enc = pi_eval(internal)
        two_pi_lo = 2 * pi_enc.lo
        two_pi_hi = 2 * pi_enc.hi
        delta = two_pi_hi - two_pi_lo
        approx = (two_pi_lo + two_pi_hi) / 2
        k = round(x_q / approx)
        reduction_error = abs(k) * delta
        if 4 * reduction_error <= target:
            r = x_q - k * two_pi_lo
            core = _sin_taylor(r, target / 2)
            return RationalEnclosure(core.lo - reduction_error, core.hi + reduction_error)
        internal *= 2


def cos_eval(x, working_bits: int) -> RationalEnclosure:
    x_q = _fraction_input(x)
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")
    target = Fraction(1, 1 << int(working_bits))
    internal = int(working_bits) + 16
    while True:
        pi_enc = pi_eval(internal)
        two_pi_lo = 2 * pi_enc.lo
        two_pi_hi = 2 * pi_enc.hi
        delta = two_pi_hi - two_pi_lo
        approx = (two_pi_lo + two_pi_hi) / 2
        k = round(x_q / approx)
        reduction_error = abs(k) * delta
        if 4 * reduction_error <= target:
            r = x_q - k * two_pi_lo
            core = _cos_taylor(r, target / 2)
            return RationalEnclosure(core.lo - reduction_error, core.hi + reduction_error)
        internal *= 2


def asin_eval(x, working_bits: int) -> RationalEnclosure:
    x_q = _fraction_input(x)
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")
    if x_q < -1 or x_q > 1:
        raise AsinDomainError(f"asin domain: |x| must be <= 1, got {x_q}")
    target = Fraction(1, 1 << int(working_bits))
    negate = x_q < 0
    abs_x = -x_q if negate else x_q
    if abs_x == 1:
        pi_enc = pi_eval(working_bits)
        lo, hi = pi_enc.lo / 2, pi_enc.hi / 2
        return RationalEnclosure(-hi, -lo) if negate else RationalEnclosure(lo, hi)

    abs_x_squared = abs_x * abs_x
    one_minus = 1 - abs_x_squared
    partial = Fraction(0)
    term = abs_x
    k = 0
    while True:
        partial += term
        next_term = term * (2 * k + 1) ** 2 * abs_x_squared / (2 * (k + 1) * (2 * k + 3))
        tail_bound = next_term / one_minus
        if tail_bound <= target:
            core = RationalEnclosure(partial, partial + tail_bound)
            return RationalEnclosure(-core.hi, -core.lo) if negate else core
        term = next_term
        k += 1


def acos_eval(x, working_bits: int) -> RationalEnclosure:
    x_q = _fraction_input(x)
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")
    if x_q < -1 or x_q > 1:
        raise AcosDomainError(f"acos domain: |x| must be <= 1, got {x_q}")
    if x_q == 1:
        return RationalEnclosure(Fraction(0), Fraction(0))
    target = Fraction(1, 1 << int(working_bits))
    internal = int(working_bits) + 8
    while True:
        asin_enc = asin_eval(x_q, internal)
        pi_enc = pi_eval(internal)
        lo = pi_enc.lo / 2 - asin_enc.hi
        hi = pi_enc.hi / 2 - asin_enc.lo
        if hi - lo <= target:
            return RationalEnclosure(lo, hi)
        internal *= 2


def atan_eval(x, working_bits: int) -> RationalEnclosure:
    x_q = _fraction_input(x)
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")
    target = Fraction(1, 1 << int(working_bits))
    negate = x_q < 0
    abs_x = -x_q if negate else x_q
    if abs_x <= 1:
        core = _atan_series(abs_x, target)
        return RationalEnclosure(-core.hi, -core.lo) if negate else core

    inner = _atan_series(1 / abs_x, target / 2)
    internal = int(working_bits) + 16
    while True:
        pi_enc = pi_eval(internal)
        lo = pi_enc.lo / 2 - inner.hi
        hi = pi_enc.hi / 2 - inner.lo
        if hi - lo <= target:
            return RationalEnclosure(-hi, -lo) if negate else RationalEnclosure(lo, hi)
        internal *= 2


def tan_eval(x, working_bits: int) -> RationalEnclosure:
    x_q = _fraction_input(x)
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")
    target = Fraction(1, 1 << int(working_bits))
    internal = int(working_bits) + 12
    while True:
        sine = sin_eval(x_q, internal)
        cosine = cos_eval(x_q, internal)
        if cosine.lo <= 0 <= cosine.hi:
            if internal >= _POLE_SEPARATION_CEILING:
                raise TanPoleRefusal(f"tan: x={x_q} too close to a pole to separate cos from zero")
            internal *= 2
            continue
        corners = (
            sine.lo / cosine.lo,
            sine.lo / cosine.hi,
            sine.hi / cosine.lo,
            sine.hi / cosine.hi,
        )
        lo, hi = min(corners), max(corners)
        if hi - lo <= target:
            return RationalEnclosure(lo, hi)
        internal *= 2


def log2_eval(x, working_bits: int) -> RationalEnclosure:
    x_q = _fraction_input(x)
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")
    target = Fraction(1, 1 << int(working_bits))
    internal = int(working_bits) + 8
    while True:
        numerator = log_eval(x_q, internal)
        denominator = log_eval(_TWO, internal)
        corners = (
            numerator.lo / denominator.lo,
            numerator.lo / denominator.hi,
            numerator.hi / denominator.lo,
            numerator.hi / denominator.hi,
        )
        lo, hi = min(corners), max(corners)
        if hi - lo <= target:
            return RationalEnclosure(lo, hi)
        internal *= 2


def pow_eval(x, y, working_bits: int) -> RationalEnclosure:
    x_q = _fraction_input(x)
    y_q = _fraction_input(y)
    if x_q <= 0:
        raise PowDomainError(f"pow_eval domain: base x must be > 0, got {x_q}")
    if working_bits <= 0:
        raise ValueError("working_bits must be positive")

    target = Fraction(1, 1 << int(working_bits))
    internal = int(working_bits) + 8
    while True:
        log_x = log_eval(x_q, internal)
        if y_q >= 0:
            lower, upper = y_q * log_x.lo, y_q * log_x.hi
        else:
            lower, upper = y_q * log_x.hi, y_q * log_x.lo
        lo = exp_eval(lower, internal).lo
        hi = exp_eval(upper, internal).hi
        if hi - lo <= target:
            return RationalEnclosure(lo, hi)
        internal *= 2


def typed_log(x, required_precision: int) -> dict:
    return typed_refine(log_eval, x, required_precision)


def typed_exp(x, required_precision: int) -> dict:
    return typed_refine(exp_eval, x, required_precision)


def typed_log2(x, required_precision: int) -> dict:
    return typed_refine(log2_eval, x, required_precision)


def typed_sin(x, required_precision: int) -> dict:
    return typed_refine(sin_eval, x, required_precision)


def typed_cos(x, required_precision: int) -> dict:
    return typed_refine(cos_eval, x, required_precision)


def typed_asin(x, required_precision: int) -> dict:
    return typed_refine(asin_eval, x, required_precision)


def typed_acos(x, required_precision: int) -> dict:
    return typed_refine(acos_eval, x, required_precision)


def typed_atan(x, required_precision: int) -> dict:
    return typed_refine(atan_eval, x, required_precision)


def typed_tan(x, required_precision: int) -> dict:
    return typed_refine(tan_eval, x, required_precision)


def typed_pow(x, y, required_precision: int) -> dict:
    return typed_refine(lambda base, bits: pow_eval(base, y, bits), x, required_precision)


def _refine_record(status: RefineStatus, value: Fraction | None, working_bits: int, iterations: int) -> dict:
    return {
        "status": status,
        "value": None if value is None else _fraction_text(value),
        "working_bits": str(working_bits),
        "iterations": str(iterations),
        "method": "typed_refine_exact_rational_enclosure",
    }


def _binade_reduce(x: Fraction) -> tuple[int, Fraction]:
    e = x.numerator.bit_length() - x.denominator.bit_length() - 1

    def scaled(exp: int) -> Fraction:
        if exp >= 0:
            return Fraction(x.numerator, x.denominator << exp)
        return Fraction(x.numerator << -exp, x.denominator)

    mant = scaled(e)
    while mant >= 2:
        e += 1
        mant = scaled(e)
    while mant < 1:
        e -= 1
        mant = scaled(e)
    return e, mant


def _two_atanh_enclosure(z: Fraction, width_budget: Fraction) -> RationalEnclosure:
    if z == 0:
        return RationalEnclosure(Fraction(0), Fraction(0))
    one_minus_z2 = 1 - z * z
    partial = Fraction(0)
    j = 0
    while True:
        partial += 2 * z ** (2 * j + 1) / (2 * j + 1)
        tail_bound = 2 * z ** (2 * j + 3) / ((2 * j + 3) * one_minus_z2)
        if tail_bound <= width_budget:
            return RationalEnclosure(partial, partial + tail_bound)
        j += 1


def _exp_nonnegative(x: Fraction, width_budget: Fraction) -> RationalEnclosure:
    partial = Fraction(0)
    term = Fraction(1)
    m = 0
    while True:
        partial += term
        next_term = term * x / (m + 1)
        if m + 2 > x:
            tail_bound = next_term / (1 - x / (m + 2))
            if tail_bound <= width_budget:
                return RationalEnclosure(partial, partial + tail_bound)
        term = next_term
        m += 1


def _arctan_recip(m: int, width_budget: Fraction) -> RationalEnclosure:
    partial = Fraction(0)
    k = 0
    while True:
        sign = 1 if k % 2 == 0 else -1
        partial += Fraction(sign, (2 * k + 1) * m ** (2 * k + 1))
        next_mag = Fraction(1, (2 * (k + 1) + 1) * m ** (2 * (k + 1) + 1))
        if next_mag <= width_budget:
            if (k + 1) % 2 == 0:
                return RationalEnclosure(partial, partial + next_mag)
            return RationalEnclosure(partial - next_mag, partial)
        k += 1


def _sin_taylor(r: Fraction, width_budget: Fraction) -> RationalEnclosure:
    r = Fraction(r)
    abs_r = -r if r < 0 else r
    negate = r < 0
    r_squared = r * r
    partial = Fraction(0)
    magnitude = abs_r
    k = 0
    while True:
        partial += (1 if k % 2 == 0 else -1) * magnitude
        next_magnitude = magnitude * r_squared / ((2 * k + 2) * (2 * k + 3))
        if next_magnitude <= magnitude and next_magnitude <= width_budget:
            if (k + 1) % 2 == 0:
                lo, hi = partial, partial + next_magnitude
            else:
                lo, hi = partial - next_magnitude, partial
            return RationalEnclosure(-hi, -lo) if negate else RationalEnclosure(lo, hi)
        magnitude = next_magnitude
        k += 1


def _cos_taylor(r: Fraction, width_budget: Fraction) -> RationalEnclosure:
    r_squared = r * r
    partial = Fraction(0)
    magnitude = Fraction(1)
    k = 0
    while True:
        partial += (1 if k % 2 == 0 else -1) * magnitude
        next_magnitude = magnitude * r_squared / ((2 * k + 1) * (2 * k + 2))
        if next_magnitude <= magnitude and next_magnitude <= width_budget:
            if (k + 1) % 2 == 0:
                return RationalEnclosure(partial, partial + next_magnitude)
            return RationalEnclosure(partial - next_magnitude, partial)
        magnitude = next_magnitude
        k += 1


def _atan_series(y: Fraction, width_budget: Fraction) -> RationalEnclosure:
    y_squared = y * y
    partial = Fraction(0)
    magnitude = y
    k = 0
    while True:
        partial += (1 if k % 2 == 0 else -1) * magnitude
        next_magnitude = magnitude * y_squared * (2 * k + 1) / (2 * k + 3)
        if next_magnitude <= magnitude and next_magnitude <= width_budget:
            if (k + 1) % 2 == 0:
                return RationalEnclosure(partial, partial + next_magnitude)
            return RationalEnclosure(partial - next_magnitude, partial)
        magnitude = next_magnitude
        k += 1


def _floor_log2(a: Fraction) -> int:
    e = a.numerator.bit_length() - a.denominator.bit_length() - 1

    def pow2(exp: int) -> Fraction:
        return Fraction(1 << exp) if exp >= 0 else Fraction(1, 1 << -exp)

    while pow2(e) > a:
        e -= 1
    while pow2(e + 1) <= a:
        e += 1
    return e


def _round_half_to_even(s: Fraction) -> int:
    floor_part = s.numerator // s.denominator
    remainder = s - floor_part
    half = Fraction(1, 2)
    if remainder < half:
        return floor_part
    if remainder > half:
        return floor_part + 1
    return floor_part if floor_part % 2 == 0 else floor_part + 1


def _fraction_input(value) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("booleans are not rational inputs")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        return Fraction.from_float(value)
    if isinstance(value, str):
        return Fraction(value.strip())
    return Fraction(value)


def _fraction_text(value: Fraction) -> str:
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"
