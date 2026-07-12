"""Exact proof scalars and canonical dyadic interval arithmetic."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


def q(value) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("boolean is not an exact scalar")
    return value if isinstance(value, Fraction) else Fraction(value)


def floor_fraction(x: Fraction) -> int:
    return x.numerator // x.denominator


def ceil_fraction(x: Fraction) -> int:
    return -floor_fraction(-x)


def dyadic_floor(x: Fraction, bits: int) -> Fraction:
    return Fraction(floor_fraction(q(x) * (1 << bits)), 1 << bits)


def dyadic_ceil(x: Fraction, bits: int) -> Fraction:
    return Fraction(ceil_fraction(q(x) * (1 << bits)), 1 << bits)


@dataclass(frozen=True, slots=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self):
        object.__setattr__(self, "lo", q(self.lo))
        object.__setattr__(self, "hi", q(self.hi))
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @classmethod
    def point(cls, value) -> "Interval":
        value = q(value)
        return cls(value, value)

    def __add__(self, other):
        other = as_interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_interval(other))

    def __rsub__(self, other):
        return as_interval(other) - self

    def __mul__(self, other):
        other = as_interval(other)
        products = (self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi)
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def reciprocal(self):
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        return Interval(1 / self.hi, 1 / self.lo) if self.lo > 0 else Interval(1 / self.hi, 1 / self.lo)

    def __truediv__(self, other):
        return self * as_interval(other).reciprocal()

    def __rtruediv__(self, other):
        return as_interval(other) / self

    def abs_bound(self) -> Fraction:
        return max(abs(self.lo), abs(self.hi))

    def rounded(self, bits: int) -> "Interval":
        return Interval(dyadic_floor(self.lo, bits), dyadic_ceil(self.hi, bits))


def as_interval(value) -> Interval:
    return value if isinstance(value, Interval) else Interval.point(value)


def sqrt_interval(value: Interval, bits: int) -> Interval:
    """Outward dyadic square-root enclosure proved by integer squaring."""
    value = as_interval(value)
    if value.lo < 0:
        raise ValueError("negative square-root interval")
    scale = 1 << (2 * bits)

    def lower(x: Fraction) -> Fraction:
        n = (x.numerator * scale) // x.denominator
        r = isqrt(n)
        while Fraction((r + 1) * (r + 1), scale) <= x:
            r += 1
        while Fraction(r * r, scale) > x:
            r -= 1
        return Fraction(r, 1 << bits)

    def upper(x: Fraction) -> Fraction:
        lo = lower(x)
        return lo if lo * lo == x else lo + Fraction(1, 1 << bits)

    return Interval(lower(value.lo), upper(value.hi))


@dataclass(frozen=True, slots=True)
class QS2:
    a: Fraction
    b: Fraction

    def __init__(self, a=0, b=0):
        object.__setattr__(self, "a", q(a))
        object.__setattr__(self, "b", q(b))

    def to_record(self):
        return {"type": "QS2", "a": fraction_text(self.a), "b": fraction_text(self.b)}


def fraction_text(x: Fraction) -> str:
    x = q(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
