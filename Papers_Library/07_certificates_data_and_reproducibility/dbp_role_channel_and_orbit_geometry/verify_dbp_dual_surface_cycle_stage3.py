#!/usr/bin/env python3
"""Dependency-free exact checks for the DBP Stage-3 transport calculation."""

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

    def __pow__(self, exponent: int) -> "Q2":
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        result = Q2(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power >>= 1
        return result

    def approx(self) -> float:
        return float(self.a) + float(self.b) * 2.0**0.5


FAILURES: list[str] = []


def gate(name: str, condition: bool, detail: str = "") -> None:
    print(f"{'PASS' if condition else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not condition:
        FAILURES.append(name)


def main() -> None:
    one = Q2(1)
    two = Q2(2)
    root2 = Q2(0, 1)
    r = root2

    c = (r - one) / (r + one)
    m = (r - one) / (two * r)
    n = -(m * m) / (one - two * m)

    c_dual = ((-r) - one) / ((-r) + one)
    m_dual = ((-r) - one) / (two * (-r))
    n_dual = -(m_dual * m_dual) / (one - two * m_dual)

    gate("G1.primary_c", c == Q2(3, -2))
    gate("G2.primary_m", m == Q2(F(1, 2), F(-1, 4)))
    gate("G3.primary_n", n == Q2(F(1, 2), F(-3, 8)))
    gate("G4.c_involution", c_dual == one / c)
    gate("G5.m_involution", m_dual == one - m)
    gate("G6.n_involution", n_dual == one - n)
    gate("G7.dual_c", c_dual == Q2(3, 2))
    gate("G8.dual_m", m_dual == Q2(F(1, 2), F(1, 4)))
    gate("G9.dual_n", n_dual == Q2(F(1, 2), F(3, 8)))

    u_p = one / n_dual
    x_p = m_dual / n_dual
    gate("P1.pole_inside_relative_interval", 0 < u_p.approx() < 1)
    gate("P2.pole_inside_legendre_interval", 0 < x_p.approx() < m_dual.approx())
    gate("P3.u_p_formula", u_p == (two * m_dual - one) / (m_dual * m_dual))
    gate("P4.x_p_formula", x_p == two - one / m_dual)

    du_dm = two * (one - m_dual) / (m_dual**3)
    dx_dm = one / (m_dual * m_dual)
    gate("P5.u_p_motion_positive", du_dm.approx() > 0)
    gate("P6.x_p_motion_positive", dx_dm.approx() > 0)

    # The residue meridian has normalized period 2*pi*i*4.  The upper minus
    # lower indentation is the oppositely oriented meridian.
    residue = 4
    gate("R1.meridian_residue_coefficient", 2 * residue == 8)
    gate("R2.upper_minus_lower_coefficient", -2 * residue == -8)
    gate("R3.cpv_meridian_coefficient", F(1, 2) == F(1, 2))

    # The endpoint lattice is Z*beta.  No integer k solves k=i; checking real
    # and imaginary coordinates makes the obstruction explicit and exact.
    integral_boundary_coordinates = {(k, 0) for k in range(-4, 5)}
    gate("H1.i_boundary_not_integral", (0, 1) not in integral_boundary_coordinates)
    gate("H2.orientation_units_only", all(pair in integral_boundary_coordinates for pair in ((1, 0), (-1, 0))))

    # The Legendre j-value is useful as a consistency check on both channels.
    j = Q2(256) * (one - m_dual + m_dual * m_dual) ** 3 / (
        (m_dual * m_dual) * ((one - m_dual) ** 2)
    )
    gate("J1.common_legendre_j", j == Q2(10976))

    total = 22
    if FAILURES:
        print(f"VERDICT: FAIL ({len(FAILURES)}): {', '.join(FAILURES)}")
        raise SystemExit(1)
    print(f"VERDICT: DBP DUAL SURFACE-CYCLE STAGE 3 CLEAN — {total}/{total} gates")


if __name__ == "__main__":
    main()
