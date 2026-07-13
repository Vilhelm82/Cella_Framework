"""Rational interval jets and certified high-order Taylor-panel bounds.

Jet coefficient k encloses f^(k)/k! throughout the input interval.  The
Taylor remainder therefore follows directly from the Lagrange theorem.
"""

from __future__ import annotations

from .exact_scalar import Interval, as_interval, sqrt_interval


class Jet:
    def __init__(self, coeffs, bits):
        # Outward dyadic normalization prevents exact-rational denominator
        # growth while preserving every enclosure invariant.
        self.c = tuple(as_interval(x).rounded(bits) for x in coeffs)
        self.bits = bits

    @property
    def order(self): return len(self.c) - 1

    @classmethod
    def const(cls, x, order, bits): return cls([x] + [0] * order, bits)

    @classmethod
    def variable(cls, interval, order, bits): return cls([interval, 1] + [0] * (order - 1), bits)

    def _jet(self, other): return other if isinstance(other, Jet) else Jet.const(other, self.order, self.bits)

    def __add__(self, other):
        other = self._jet(other)
        return Jet([a + b for a, b in zip(self.c, other.c)], self.bits)

    __radd__ = __add__
    def __neg__(self): return Jet([-x for x in self.c], self.bits)
    def __sub__(self, other): return self + (-self._jet(other))
    def __rsub__(self, other): return self._jet(other) - self

    def __mul__(self, other):
        other = self._jet(other)
        return Jet([sum((self.c[k] * other.c[n-k] for k in range(n+1)), Interval.point(0))
                    for n in range(self.order + 1)], self.bits)

    __rmul__ = __mul__

    def reciprocal(self):
        out = [self.c[0].reciprocal()]
        for n in range(1, self.order + 1):
            out.append(-sum((self.c[k] * out[n-k] for k in range(1, n+1)), Interval.point(0)) / self.c[0])
        return Jet(out, self.bits)

    def __truediv__(self, other): return self * self._jet(other).reciprocal()
    def __rtruediv__(self, other): return self._jet(other) / self

    def sqrt(self):
        out = [sqrt_interval(self.c[0], self.bits)]
        for n in range(1, self.order + 1):
            cross = sum((out[k] * out[n-k] for k in range(1, n)), Interval.point(0))
            out.append((self.c[n] - cross) / (2 * out[0]))
        return Jet(out, self.bits)


def kernel_jet(kernel_id: str, interval: Interval, order: int, bits: int) -> Jet:
    t = Jet.variable(interval, order, bits)
    w = 1 - t
    t2, w2 = t * t, w * w
    if kernel_id == "g_plus_v1":
        p = t2*t2 + 2*t2*w2 + 2*w2*w2
        return 16 * (t2 - 2*w2) / (t2 + 8*w2) / p.sqrt()
    if kernel_id == "g_minus_v1":
        delta = t2 - w2
        p = delta*delta + w2*w2
        root = p.sqrt()
        sqrt2 = Jet.const(sqrt_interval(Interval.point(2), bits), order, bits)
        return -16*t2 / (root * (t2 + 2*w2 + sqrt2*root))
    raise ValueError("unknown fixed DBP kernel")
