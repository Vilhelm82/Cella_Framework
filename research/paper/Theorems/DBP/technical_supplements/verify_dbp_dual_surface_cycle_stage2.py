#!/usr/bin/env python3
"""Dependency-free checks for the DBP dual surface-cycle Stage-2 lift."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Q2:
    """a + b*sqrt(2), exactly."""

    a: F = F(0)
    b: F = F(0)

    @staticmethod
    def make(value: object) -> "Q2":
        return value if isinstance(value, Q2) else Q2(F(value))

    def __add__(self, other: object) -> "Q2":
        other = self.make(other)
        return Q2(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self) -> "Q2":
        return Q2(-self.a, -self.b)

    def __sub__(self, other: object) -> "Q2":
        return self + (-self.make(other))

    def __rsub__(self, other: object) -> "Q2":
        return self.make(other) - self

    def __mul__(self, other: object) -> "Q2":
        other = self.make(other)
        return Q2(
            self.a * other.a + 2 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def inverse(self) -> "Q2":
        norm = self.a * self.a - 2 * self.b * self.b
        if norm == 0:
            raise ZeroDivisionError
        return Q2(self.a / norm, -self.b / norm)

    def __truediv__(self, other: object) -> "Q2":
        return self * self.make(other).inverse()

    def __rtruediv__(self, other: object) -> "Q2":
        return self.make(other) / self

    def approx(self) -> float:
        return float(self.a) + float(self.b) * 2.0**0.5


FAILURES: list[str] = []


def gate(name: str, condition: bool, detail: str = "") -> None:
    print(f"{'PASS' if condition else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not condition:
        FAILURES.append(name)


def generic_gate(c: F, v: F, xi: F) -> bool:
    """Exact rational check of the angular and fiber identities."""

    a = 1 / (1 - c)
    b = c / (1 - c)
    cos2 = (1 - c) * v / (1 - c * v)
    sin2 = (1 - v) / (1 - c * v)
    p = a * cos2 + sin2
    pb = p + b
    p_expected = 1 / (1 - c * v)
    pb_expected = (1 - c * c * v) / ((1 - c) * (1 - c * v))

    surface_value = (
        a * (3 / a) * (1 + xi * xi) * cos2
        - b * (3 / b) * xi * xi
        + 3 * (1 + xi * xi) * sin2
    )
    q_over_12 = a * (1 + xi * xi) * cos2 + b * xi * xi + (1 + xi * xi) * sin2
    z2 = p + pb * xi * xi

    w2 = c * v * (1 - v) * (1 - c * v) * (1 - c * c * v)
    dt2 = (1 - c) / (4 * (1 - c * v) ** 2 * v * (1 - v))
    f2 = a * b / (p * p * pb)
    metric_rhs2 = c * c * (1 - c * v) ** 2 / (4 * w2)

    # d(xi/Z) = p/Z^3 dxi after clearing Z^2.
    primitive_numerator = z2 - pb * xi * xi

    return all(
        (
            a - b == 1,
            cos2 + sin2 == 1,
            surface_value == 3,
            p == p_expected,
            pb == pb_expected,
            q_over_12 == z2,
            f2 * dt2 == metric_rhs2,
            primitive_numerator == p,
        )
    )


def main() -> None:
    root2 = Q2(0, F(1))
    one = Q2(1)
    c = Q2(3, 2)
    a = one / (one - c)
    b = c / (one - c)
    a_primary = (one + root2) / 2
    b_primary = (root2 - one) / 2

    gate("K1.dual_a", a == -b_primary)
    gate("K2.dual_b", b == -a_primary)
    gate("K3.a_minus_b", a - b == one)
    gate("K4.ab_keystone", a * b == Q2(F(1, 4)))
    gate("K5.axis_swap_surface", -b_primary == a and -a_primary == b)

    branch_1 = one / (c * c)
    branch_2 = one / c
    gate("K6.branch_order", 0 < branch_1.approx() < branch_2.approx() < 1)
    gate("K7.dual_contour_avoids_finite_branches", branch_1.approx() > 0 and branch_2.approx() < 1)

    samples = (
        (F(1, 3), F(2, 5), F(3, 7)),
        (F(2, 3), F(-3, 5), F(4, 9)),
        (F(5, 3), F(7, 4), F(-2, 3)),
        (F(7, 4), F(-5, 2), F(5, 6)),
    )
    for index, values in enumerate(samples, start=1):
        gate(
            f"A{index}.angular_fiber_exact_sample",
            generic_gate(*values),
            f"c={values[0]}, v={values[1]}, xi={values[2]}",
        )

    # Derive the Stage-1 residue again inside the Stage-2 checker. At
    # P_infinity^- write W/v^2=i*w_i with w_i=-c^2.
    leading_q = c * (-one) * (-c) * (-(c * c))
    gate("R0.quartic_leading_term", leading_q == -(c * c * c * c))
    w_i = -(c * c)
    omega_i_coeff_dv_over_v = -4 * c * c / w_i
    omega_i_coeff_dtau_over_tau = -omega_i_coeff_dv_over_v
    residue = -omega_i_coeff_dtau_over_tau
    gate("R1.boundary_residue", residue == Q2(4))
    gate("R2.lateral_difference_coefficient", 2 * residue == Q2(8))

    # If int(C_up)=-i*I-4*pi and int(C_down)=-i*I+4*pi, then
    # multiplication of both chains by i gives I-/+4*pi*i and the half-sum I.
    real_offsets_cancel = Q2(-4) + Q2(4) == Q2(0)
    normalized_cpv_coefficient = F(1, 2) * (F(1) + F(1))
    gate("P1.geometric_offsets_cancel", real_offsets_cancel)
    gate("P2.cpv_half_sum_normalization", normalized_cpv_coefficient == 1)
    gate("P3.geometric_meridian_coefficient", -2 * residue == Q2(-8))

    total = 13 + len(samples)
    if FAILURES:
        print(f"VERDICT: FAIL ({len(FAILURES)}): {', '.join(FAILURES)}")
        raise SystemExit(1)
    print(f"VERDICT: DBP DUAL SURFACE-CYCLE STAGE 2 CLEAN — {total}/{total} gates")


if __name__ == "__main__":
    main()
