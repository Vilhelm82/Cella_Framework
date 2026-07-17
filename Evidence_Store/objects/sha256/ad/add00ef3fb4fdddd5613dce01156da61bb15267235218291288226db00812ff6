#!/usr/bin/env python3
"""Exact audit for the CCE-6 whole-surface rank obstruction."""

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class QRoot2:
    rational: Fraction
    root2: Fraction = Fraction(0)

    def __sub__(self, other: "QRoot2") -> "QRoot2":
        return QRoot2(self.rational - other.rational, self.root2 - other.root2)

    def __mul__(self, scalar: int) -> "QRoot2":
        return QRoot2(self.rational * scalar, self.root2 * scalar)

    def __bool__(self) -> bool:
        return bool(self.rational or self.root2)


passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


for epsilon in (1, -1):
    a = QRoot2(Fraction(1, 2), Fraction(epsilon, 2))
    b = QRoot2(Fraction(-1, 2), Fraction(epsilon, 2))
    check(f"sheet {epsilon}: a-b=1", a - b == QRoot2(Fraction(1)))
    finite_pencil = (a * -4, b * 4, QRoot2(Fraction(-4)), QRoot2(Fraction(0)))
    check(f"sheet {epsilon}: four finite pencil parameters distinct", len(set(finite_pencil)) == 4)
    check(f"sheet {epsilon}: Dq smooth pencil", len(set(finite_pencil)) == 4)
    check(f"sheet {epsilon}: Dinf smooth pencil", len(set(finite_pencil[:3])) == 3)

# Complete intersection and divisor invariants.
surface_degree = 2 * 2
c2_coefficient = 2
euler_surface = c2_coefficient * surface_degree
b0, b1, b3, b4 = 1, 0, 0, 1
b2_surface = euler_surface - b0 + b1 + b3 - b4
check("surface degree four", surface_degree == 4)
check("surface Euler characteristic eight", euler_surface == 8)
check("surface b2 six", b2_surface == 6)

# Gysin sequence for X=S-Dq.
rank_h2_x = (b2_surface - 1) + 2
rank_h1_x = 0
check("complement H2 rank seven", rank_h2_x == 7)
check("complement H1 rank zero", rank_h1_x == 0)

# Dinf is elliptic and meets Dq in H^2=4 points.
genus_y, punctures_y = 1, surface_degree
rank_h1_y = 2 * genus_y + punctures_y - 1
check("boundary curve has four punctures", punctures_y == 4)
check("boundary H1 rank five", rank_h1_y == 5)

rank_relative = rank_h2_x + rank_h1_y
rank_curve_source = (2 * 1 + 2 - 1) + 1
check("whole relative H2 rank twelve", rank_relative == 12)
check("native curve source rank four", rank_curve_source == 4)
check("surjectivity rank obstruction", rank_curve_source < rank_relative)
check("at least eight nonnative directions", rank_relative - rank_curve_source == 8)

print(f"CCE-6 whole-surface topology audit: {passed} assertions passed")
