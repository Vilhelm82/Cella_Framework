"""Fixed algebraic Taylor recurrences and analytic Cauchy tail witnesses."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .exact_scalar import Interval, sqrt_interval


def _zero(n): return [Interval.point(0) for _ in range(n)]


def _add(a, b):
    n = max(len(a), len(b)); out = _zero(n)
    for i in range(n):
        out[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
    return out


def _scale(a, s): return [x*s for x in a]


def _mul(a, b, n, bits):
    return [sum((a[k]*b[i-k] for k in range(i+1) if k < len(a) and i-k < len(b)), Interval.point(0)).rounded(bits)
            for i in range(n)]


def _sqrt_series(a, n, bits):
    y = [sqrt_interval(a[0], bits)]
    for i in range(1, n):
        cross = sum((y[k]*y[i-k] for k in range(1, i)), Interval.point(0))
        ai = a[i] if i < len(a) else Interval.point(0)
        y.append(((ai-cross)/(2*y[0])).rounded(bits))
    return y


def _divide_series(a, b, n, bits):
    q = [(a[0]/b[0]).rounded(bits)]
    for i in range(1, n):
        used = sum((b[k]*q[i-k] for k in range(1, i+1) if k < len(b)), Interval.point(0))
        ai = a[i] if i < len(a) else Interval.point(0)
        q.append(((ai-used)/b[0]).rounded(bits))
    return q


def kernel_coefficients(kernel_id: str, center: Fraction, order: int, bits: int):
    """Coefficients through order, generated only by the fixed DAG recurrences."""
    n = order + 1
    t = [Interval.point(center), Interval.point(1)] + _zero(n-2)
    w = [Interval.point(1-center), Interval.point(-1)] + _zero(n-2)
    t2, w2 = _mul(t, t, n, bits), _mul(w, w, n, bits)
    if kernel_id == "g_plus_v1":
        p = _add(_add(_mul(t2, t2, n, bits), _scale(_mul(t2, w2, n, bits), 2)),
                 _scale(_mul(w2, w2, n, bits), 2))
        root = _sqrt_series(p, n, bits)
        numerator = _scale(_add(t2, _scale(w2, -2)), 16)
        denominator = _mul(_add(t2, _scale(w2, 8)), root, n, bits)
    elif kernel_id == "g_minus_v1":
        delta = _add(t2, _scale(w2, -1))
        p = _add(_mul(delta, delta, n, bits), _mul(w2, w2, n, bits))
        root = _sqrt_series(p, n, bits)
        sqrt2 = sqrt_interval(Interval.point(2), bits)
        inner = _add(_add(t2, _scale(w2, 2)), _scale(root, sqrt2))
        numerator = _scale(t2, -16)
        denominator = _mul(root, inner, n, bits)
    else:
        raise ValueError("unknown fixed kernel")
    return _divide_series(numerator, denominator, n, bits)


@dataclass(frozen=True, slots=True)
class Rect:
    re: Interval
    im: Interval

    def __add__(self, other):
        other = rect(other); return Rect(self.re+other.re, self.im+other.im)
    __radd__ = __add__
    def __neg__(self): return Rect(-self.re, -self.im)
    def __sub__(self, other): return self + (-rect(other))
    def __rsub__(self, other): return rect(other)-self
    def __mul__(self, other):
        other = rect(other)
        return Rect(self.re*other.re-self.im*other.im, self.re*other.im+self.im*other.re)
    __rmul__ = __mul__
    def abs_upper(self):
        # |z| <= |Re z|+|Im z|, deliberately rational.
        return self.re.abs_bound()+self.im.abs_bound()


def rect(x):
    return x if isinstance(x, Rect) else Rect(Interval.point(x), Interval.point(0))


def analytic_majorant(kernel_id: str, center: Fraction, radius: Fraction, bits: int) -> Fraction:
    """Prove analytic separation on a complex disk via its enclosing rectangle."""
    z = Rect(Interval(center-radius, center+radius), Interval(-radius, radius))
    w = 1-z; t2, w2 = z*z, w*w
    if kernel_id == "g_plus_v1":
        p = t2*t2 + 2*t2*w2 + 2*w2*w2
        q = t2 + 8*w2
        if p.re.lo <= 0 or q.re.lo <= 0:
            raise ValueError("primary analytic disk separation failed")
        root_lower = sqrt_interval(Interval.point(p.re.lo), bits).lo
        return 16*(t2-2*w2).abs_upper()/(q.re.lo*root_lower)
    if kernel_id == "g_minus_v1":
        delta = t2-w2
        p = delta*delta+w2*w2
        a = t2+2*w2
        if p.re.lo <= 0 or a.re.lo <= 0:
            raise ValueError("dual analytic disk separation failed")
        root_lower = sqrt_interval(Interval.point(p.re.lo), bits).lo
        # The principal sqrt has positive real part because Re(P)>0; hence
        # Re(a+sqrt(2)*sqrt(P)) >= Re(a).
        return 16*t2.abs_upper()/(root_lower*a.re.lo)
    raise ValueError("unknown fixed kernel")


def integrate_recurrence_panel(kernel_id: str, a: Fraction, b: Fraction,
                               order: int, bits: int, radius_multiplier: int):
    center, h = (a+b)/2, (b-a)/2
    radius = radius_multiplier*h
    coeff = kernel_coefficients(kernel_id, center, order, bits)
    value = Interval.point(0)
    for k in range(0, order+1, 2):
        value += coeff[k] * (2*h**(k+1)/(k+1))
    majorant = analytic_majorant(kernel_id, center, radius, bits)
    ratio = h/radius
    tail = 2*h*majorant*ratio**(order+1)/(1-ratio)
    return value + Interval(-tail, tail), tail
