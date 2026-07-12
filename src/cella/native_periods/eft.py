"""Exact replay identities for binary64 readings and local EFT defects."""

from __future__ import annotations

import struct
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import sqrt


def float_fraction(x: float) -> Fraction:
    n, d = x.as_integer_ratio()
    return Fraction(n, d)


@dataclass(frozen=True, slots=True)
class BinaryReading:
    format: str
    sign: int
    exponent: int
    significand: int
    raw_bits: str

    @classmethod
    def from_float(cls, x: float):
        bits = struct.unpack(">Q", struct.pack(">d", x))[0]
        sign = -1 if bits >> 63 else 1
        raw_exp = (bits >> 52) & 0x7FF
        frac = bits & ((1 << 52) - 1)
        exponent = -1074 if raw_exp == 0 else raw_exp - 1023 - 52
        significand = frac if raw_exp == 0 else frac | (1 << 52)
        return cls("binary64", sign, exponent, significand, f"{bits:016x}")

    def exact(self):
        if self.significand == 0:
            return Fraction(0)
        return Fraction(self.sign * self.significand * (1 << self.exponent)) if self.exponent >= 0 else Fraction(self.sign * self.significand, 1 << -self.exponent)

    def to_record(self):
        return asdict(self)


def two_sum(a: float, b: float):
    s = a + b
    e = float_fraction(a) + float_fraction(b) - float_fraction(s)
    return s, e


def two_prod(a: float, b: float):
    p = a * b
    e = float_fraction(a) * float_fraction(b) - float_fraction(p)
    return p, e


def division_defect(a: float, b: float):
    q = a / b
    r = float_fraction(a) - float_fraction(q) * float_fraction(b)
    return q, r


def sqrt_defect(a: float):
    q = sqrt(a)
    d = float_fraction(a) - float_fraction(q) ** 2
    return q, d


def normalize_expansion(values):
    total = sum((float_fraction(v) if isinstance(v, float) else Fraction(v) for v in values), Fraction())
    limbs = []
    residual = total
    for _ in range(8):
        limb = float(residual)
        if limb == 0.0:
            break
        limbs.append(limb)
        residual -= float_fraction(limb)
    return tuple(limbs), residual
