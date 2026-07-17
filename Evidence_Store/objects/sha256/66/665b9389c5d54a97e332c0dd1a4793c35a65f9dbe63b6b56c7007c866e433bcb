"""Deterministic certified dyadic-panel integration."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

from .exact_scalar import Interval
from .exact_scalar import dyadic_ceil
from .jet_bound import kernel_jet
from .schedule import admitted_m1_schedule
from .algebraic_series import integrate_recurrence_panel


@dataclass(frozen=True, slots=True)
class IntegralCertificate:
    enclosure: Interval
    rule: str
    panels: int
    order: int
    working_bits: int
    remainder_bound: Fraction


@lru_cache(maxsize=16)
def integrate_certified(kernel_id: str, target_bits: int) -> IntegralCertificate:
    # M0 retains the prescribed fourth-derivative Simpson theorem.  M1 uses
    # the spec-permitted faster Taylor rule with an explicit Lagrange bound.
    # The Simpson implementation is retained and directly exercised as the
    # prescribed M0 proof kernel.  API precision requests use the faster rule
    # once fourth-order panel growth ceases to be practical.
    if target_bits <= 12:
        return _adaptive_simpson(kernel_id, target_bits)
    if target_bits > 12:
        schedule = admitted_m1_schedule(kernel_id)
        panels = schedule["panels"]
        total = Interval.point(0)
        remainder = Fraction(0)
        max_order = 0
        max_work = 0
        for item in schedule["panel_schedules"]:
            i = item["panel"]
            # The frozen schedule is the M1 floor.  For M2 requests, raise
            # only the recurrence order using a rational lower bound for
            # log2(radius_multiplier).  The ensuing complex-disk and Cauchy
            # checks remain the admission proof; this is merely a deterministic
            # requested-precision budget, not Pathfinder evidence.
            log2_lower = {
                2: Fraction(1), 3: Fraction(3, 2), 4: Fraction(2),
                6: Fraction(5, 2), 8: Fraction(3),
            }[item["radius_multiplier"]]
            required_order = (Fraction(target_bits + 24, 1) / log2_lower)
            required_order = (required_order.numerator + required_order.denominator - 1) // required_order.denominator
            order = max(item["order"], required_order)
            work = target_bits + item["guard_bits"]
            panel, tail = integrate_recurrence_panel(
                kernel_id, Fraction(i, panels), Fraction(i+1, panels),
                order, work, item["radius_multiplier"],
            )
            total += panel
            remainder += tail
            max_order, max_work = max(max_order, order), max(max_work, work)
        if total.hi-total.lo > Fraction(1, 1 << (target_bits+4)):
            raise ArithmeticError("frozen M1 recurrence schedule missed its certified width")
        return IntegralCertificate(total, "fixed_algebraic_recurrence_cauchy", panels, max_order, max_work,
                                   dyadic_ceil(remainder, max_work))
    else:
        order = max(24, min(48, target_bits // 2))
        panels = 16
        work = target_bits + 90
    while True:
        total = Interval.point(0)
        remainder = Fraction(0)
        for i in range(panels):
            a, b = Fraction(i, panels), Fraction(i + 1, panels)
            c, h = (a + b) / 2, (b - a) / 2
            point_jet = kernel_jet(kernel_id, Interval.point(c), order, work)
            panel = Interval.point(0)
            for k in range(0, order + 1, 2):
                panel += point_jet.c[k] * (2 * h ** (k + 1) / (k + 1))
            bound_jet = kernel_jet(kernel_id, Interval(a, b), order + 1, work)
            rem = 2 * h ** (order + 2) * bound_jet.c[order + 1].abs_bound()
            total += panel + Interval(-rem, rem)
            remainder += rem
        if total.hi - total.lo <= Fraction(1, 1 << (target_bits + 4)):
            return IntegralCertificate(total, "certified_taylor_interval_jet", panels, order, work, remainder)
        panels *= 2
        if panels > 256:
            raise ArithmeticError("Taylor remainder budget did not close")


def _adaptive_simpson(kernel_id: str, target_bits: int) -> IntegralCertificate:
    work = target_bits + 80
    panels = 64
    while True:
        total = Interval.point(0)
        remainder = Fraction(0)
        h = Fraction(1, panels)
        for i in range(panels):
            a, b = i*h, (i+1)*h
            m = (a+b)/2
            fa = kernel_jet(kernel_id, Interval.point(a), 0, work).c[0]
            fm = kernel_jet(kernel_id, Interval.point(m), 0, work).c[0]
            fb = kernel_jet(kernel_id, Interval.point(b), 0, work).c[0]
            panel = (fa + 4*fm + fb) * (h/6)
            fourth = kernel_jet(kernel_id, Interval(a, b), 4, work).c[4].abs_bound() * 24
            rem = h**5 * fourth / 2880
            total += panel + Interval(-rem, rem)
            remainder += rem
        if total.hi-total.lo <= Fraction(1, 1 << (target_bits + 4)):
            return IntegralCertificate(total, "composite_simpson_fourth_derivative", panels, 4, work, remainder)
        panels *= 2
        if panels > (1 << 20):
            raise ArithmeticError("Simpson remainder budget did not close")
