"""Regression test — Conjecture C subnormal sqrt (n=2), closed 2026-06-05 (HR121).

Guards the proven foundation claim: for ALL binary64 subnormal f, the correctly-rounded
sqrt round-trip is exact, i.e. sqrt(f)**2 == f, equivalently the residual
(sqrt(f)**2 - f) lies on the 2**-1074 lattice with integer multiple j = 0.

This closes the TASKS_TO_REVISIT R7 "proven-but-untested" gap for the subnormal-C result.
Stdlib only (the claim is pure IEEE-754); exact-rational check via fractions.Fraction.
Mechanism (HR121): the fixed 2**-1074 subnormal grid swallows the ~f*2**-52 back-squaring
error; the SAME correctly-rounded-sqrt mandate gives only ~50% round-trip exactness in the
normal range, so this is a genuine subnormal-regime fact, not a restatement of the mandate.
"""
import math
import struct
from fractions import Fraction

ULP_SUB = Fraction(1, 2 ** 1074)
SMALLEST_NORMAL = math.ldexp(1.0, -1022)


def _j(f):
    """Round-trip residual (sqrt(f)**2 - f) in units of 2**-1074, exact (must be 0)."""
    R = math.sqrt(f)
    V = R * R
    return (Fraction(V) - Fraction(f)) / ULP_SUB


def test_first_10000_smallest_subnormals_round_trip_exactly():
    for m in range(1, 10001):
        f = float(Fraction(m) / (1 << 1074))
        assert f < SMALLEST_NORMAL
        assert _j(f) == 0, f"subnormal m={m} not exact: j={_j(f)}"


def test_seam_top_subnormals_round_trip_exactly():
    top = 2 ** 52 - 1
    for k in range(top, top - 5000, -1):
        f = math.ldexp(float(k), -1074)
        assert f < SMALLEST_NORMAL
        assert _j(f) == 0, f"seam subnormal k={k} not exact: j={_j(f)}"


def test_strided_full_subnormal_range_round_trips_exactly():
    stride = (2 ** 52) // 20000
    for k in range(1, 2 ** 52, stride):
        f = math.ldexp(float(k), -1074)
        assert _j(f) == 0, f"strided subnormal k={k} not exact: j={_j(f)}"


def test_log_spaced_deep_subnormals_round_trip_exactly():
    for e in range(0, 52):
        f = math.ldexp(1.0, -1074 + e)
        assert f < SMALLEST_NORMAL
        assert _j(f) == 0, f"deep subnormal 2**{-1074 + e} not exact: j={_j(f)}"


def test_contrast_normal_range_round_trip_is_not_always_exact():
    """Sanity: the SAME mandate does NOT give round-trip exactness in the normal range
    (so the subnormal result is a real regime fact, not a tautology). At least one failure."""
    import random
    random.seed(0)
    fails = 0
    for _ in range(100000):
        exp = random.randint(1, 2046)
        man = random.getrandbits(52)
        x = struct.unpack(">d", struct.pack(">Q", (exp << 52) | man))[0]
        if math.isfinite(x) and x > 0 and math.sqrt(x) ** 2 != x:
            fails += 1
    assert fails > 0, "expected normal-range round-trip failures (mandate != round-trip exactness)"
