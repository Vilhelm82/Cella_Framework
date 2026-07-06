"""The exact number tower, rung 1: Q(sqrt(r)).

Admission A-003 (ESTABLISHED — the parity law is the optimality proof:
even-order invariants are rational, odd-order carry exactly one square
root, so two rungs cover the entire invariant tower).

Contract
--------
- QSqrt(a, b, r) represents a + b*sqrt(r), a and b exact rationals, r a
  POSITIVE NON-SQUARE rational (verified at construction — a square or
  nonpositive radicand is a ValueError; the value would be rational or
  complex, i.e. a different type).
- Arithmetic is exact and closed within a FIXED radicand. Mixing radicands
  is a TypeError: the parity law supplies one sqrt per context (q = g.g on
  a surface); cross-radicand identification (sqrt(8) = 2*sqrt(2)) is a
  Layer-1 normalization duty, deliberately not guessed at here.
- No float on any verdict path: float components are TypeErrors and
  __float__ raises. Display conversion exists ONLY as to_float_display(),
  named to be un-mistakable.
- b == 0 collapses honestly: equality and hashing agree with Fraction.
"""

from __future__ import annotations

import math
from fractions import Fraction

_EXACT = (Fraction, int)


def _is_square_rational(r: Fraction) -> bool:
    p, q = r.numerator, r.denominator     # lowest terms, q > 0
    sp_, sq_ = math.isqrt(p), math.isqrt(q)
    return sp_ * sp_ == p and sq_ * sq_ == q


class QSqrt:
    """a + b*sqrt(r), exact, fixed radicand."""

    __slots__ = ("_a", "_b", "_r")

    def __init__(self, a, b, r):
        for name, x in (("a", a), ("b", b), ("r", r)):
            if isinstance(x, (float, complex)):
                raise TypeError(f"{name} is {type(x).__name__}: floats are "
                                "forbidden on verdict paths (exact tower only)")
            if not isinstance(x, _EXACT):
                raise TypeError(f"{name} must be Fraction or int")
        r = Fraction(r)
        if r <= 0:
            raise ValueError("radicand must be positive (nonpositive radicand "
                             "is a different type, not a QSqrt)")
        if _is_square_rational(r):
            raise ValueError(f"radicand {r} is a rational square — the value "
                             "is rational; use Fraction, not QSqrt")
        object.__setattr__(self, "_a", Fraction(a))
        object.__setattr__(self, "_b", Fraction(b))
        object.__setattr__(self, "_r", r)

    def __setattr__(self, *_):
        raise AttributeError("QSqrt is immutable")

    # --- accessors -------------------------------------------------------
    @property
    def a(self) -> Fraction:
        return self._a

    @property
    def b(self) -> Fraction:
        return self._b

    @property
    def r(self) -> Fraction:
        return self._r

    def is_rational(self) -> bool:
        return self._b == 0

    def to_fraction(self) -> Fraction:
        if self._b != 0:
            raise ValueError("not rational: irrational part is nonzero")
        return self._a

    def norm(self) -> Fraction:
        """Field norm N(a + b*sqrt(r)) = a^2 - b^2 r  (multiplicative)."""
        return self._a * self._a - self._b * self._b * self._r

    # --- coercion helpers --------------------------------------------------
    def _lift(self, other):
        if isinstance(other, QSqrt):
            if other._r != self._r:
                raise TypeError(f"mixed radicands sqrt({self._r}) vs "
                                f"sqrt({other._r}): one sqrt per context "
                                "(parity law); normalize at Layer 1")
            return other
        if isinstance(other, _EXACT):
            return QSqrt(other, 0, self._r)
        if isinstance(other, (float, complex)):
            raise TypeError("float operand on a verdict path")
        return None

    # --- arithmetic --------------------------------------------------------
    def __add__(self, other):
        o = self._lift(other)
        if o is None:
            return NotImplemented
        return QSqrt(self._a + o._a, self._b + o._b, self._r)

    __radd__ = __add__

    def __neg__(self):
        return QSqrt(-self._a, -self._b, self._r)

    def __sub__(self, other):
        o = self._lift(other)
        if o is None:
            return NotImplemented
        return QSqrt(self._a - o._a, self._b - o._b, self._r)

    def __rsub__(self, other):
        o = self._lift(other)
        if o is None:
            return NotImplemented
        return o - self

    def __mul__(self, other):
        o = self._lift(other)
        if o is None:
            return NotImplemented
        return QSqrt(self._a * o._a + self._b * o._b * self._r,
                     self._a * o._b + self._b * o._a, self._r)

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = self._lift(other)
        if o is None:
            return NotImplemented
        n = o.norm()
        if n == 0:
            # norm zero forces a = b = 0 (r is non-square), i.e. division by zero
            raise ZeroDivisionError("division by zero QSqrt")
        conj = QSqrt(o._a, -o._b, self._r)
        num = self * conj
        return QSqrt(num._a / n, num._b / n, self._r)

    def __rtruediv__(self, other):
        o = self._lift(other)
        if o is None:
            return NotImplemented
        return o / self

    # --- comparisons / hashing ----------------------------------------------
    def __eq__(self, other):
        if isinstance(other, QSqrt):
            if self._r != other._r:
                return self._b == 0 and other._b == 0 and self._a == other._a
            return self._a == other._a and self._b == other._b
        if isinstance(other, _EXACT):
            return self._b == 0 and self._a == Fraction(other)
        return NotImplemented

    def __hash__(self):
        if self._b == 0:
            return hash(self._a)
        return hash((self._a, self._b, self._r))

    # --- display only ---------------------------------------------------------
    def __float__(self):
        raise TypeError("no float on verdict paths — use to_float_display() "
                        "(display only, lossy by declaration)")

    def to_float_display(self) -> float:
        """LOSSY, display path only. Never verdict-bearing."""
        return float(self._a) + float(self._b) * math.sqrt(float(self._r))

    def __repr__(self):
        return f"QSqrt({self._a!r}, {self._b!r}, r={self._r!r})"
