"""The sole value-enclosure materialization boundary."""

from __future__ import annotations

from fractions import Fraction

from .exact_scalar import Interval, ceil_fraction, floor_fraction
from .records import DyadicBracket


def materialize(enclosure: Interval, target_bits: int) -> DyadicBracket:
    exponent = target_bits + (64 if target_bits >= 150 else 16)
    scale = 1 << exponent
    lo = floor_fraction(enclosure.lo * scale)
    hi = ceil_fraction(enclosure.hi * scale)
    gap = max(1, hi-lo)
    width_bits = exponent - (gap - 1).bit_length()
    rounded = round((enclosure.lo + enclosure.hi) * (1 << (target_bits-1)) / 2)
    return DyadicBracket(lo, hi, exponent, width_bits, target_bits)


def decimal_render(enclosure: Interval, digits: int) -> str:
    mid = (enclosure.lo + enclosure.hi) / 2
    sign = "-" if mid < 0 else ""
    mid = abs(mid)
    integer = mid.numerator // mid.denominator
    remainder = mid - integer
    out = []
    for _ in range(digits):
        remainder *= 10
        d = remainder.numerator // remainder.denominator
        out.append(str(d))
        remainder -= d
    return f"{sign}{integer}." + "".join(out)
