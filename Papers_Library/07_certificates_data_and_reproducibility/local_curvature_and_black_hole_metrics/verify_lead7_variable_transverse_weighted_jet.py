#!/usr/bin/env python3
"""Weighted-local-jet proof of the two LEAD-7 transverse Laurent laws.

This verifier never forms the global scalar-curvature rational expression.
It works in a finite Laurent jet ring in the collapsing variable x, while the
coefficients remain arbitrary symbolic functions of the transverse variables
y and z.  Only exponents capable of feeding the requested x^-3 or x^-4
coefficient are retained through Christoffel and Ricci assembly.

Valuation logic
---------------

Generic face:
    v_x(g_xx, g_yy, g_zz) = (2, 0, 0).
    The only x^-3 scalar-curvature terms are
    E_x P_x/(2 E^2 P) and E_x R_x/(2 E^2 R).
    Transverse differentiation preserves x-valuation, so every term carrying
    a y/z derivative has valuation at least -2.

Reflection face:
    v_x(g_xx, g_yy, g_zz) = (2, -2, -2).
    The x^-4 coefficient is determined entirely by the leading monomials.
    Corrections B4, C10, C20 begin two valuation steps later; transverse
    derivatives cannot lower x-valuation and therefore cannot enter x^-4.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


LO = -8
HI = 8


@dataclass(frozen=True)
class Jet:
    """Finite Laurent jet sum_k coefficient[k] x^k on [LO, HI]."""

    coefficients: dict[int, sp.Expr]

    def __post_init__(self) -> None:
        cleaned = {
            exponent: coefficient
            for exponent, coefficient in self.coefficients.items()
            if LO <= exponent <= HI and coefficient != 0
        }
        object.__setattr__(self, "coefficients", cleaned)

    @staticmethod
    def zero() -> "Jet":
        return Jet({})

    @staticmethod
    def monomial(coefficient: sp.Expr, exponent: int) -> "Jet":
        return Jet({exponent: coefficient})

    def coefficient(self, exponent: int) -> sp.Expr:
        return self.coefficients.get(exponent, sp.Integer(0))

    def __add__(self, other: "Jet") -> "Jet":
        out = dict(self.coefficients)
        for exponent, coefficient in other.coefficients.items():
            out[exponent] = out.get(exponent, sp.Integer(0)) + coefficient
        return Jet(out)

    def __neg__(self) -> "Jet":
        return Jet({exponent: -coefficient for exponent, coefficient in self.coefficients.items()})

    def __sub__(self, other: "Jet") -> "Jet":
        return self + (-other)

    def __mul__(self, other: "Jet") -> "Jet":
        out: dict[int, sp.Expr] = {}
        for left_exponent, left_coefficient in self.coefficients.items():
            for right_exponent, right_coefficient in other.coefficients.items():
                exponent = left_exponent + right_exponent
                if LO <= exponent <= HI:
                    out[exponent] = out.get(exponent, sp.Integer(0)) + left_coefficient * right_coefficient
        return Jet(out)

    def scale(self, scalar: sp.Expr) -> "Jet":
        return Jet({exponent: scalar * coefficient for exponent, coefficient in self.coefficients.items()})

    def diff(self, coordinate: int, y: sp.Symbol, z: sp.Symbol) -> "Jet":
        if coordinate == 0:
            return Jet({exponent - 1: exponent * coefficient for exponent, coefficient in self.coefficients.items()})
        variable = y if coordinate == 1 else z
        return Jet({exponent: sp.diff(coefficient, variable) for exponent, coefficient in self.coefficients.items()})

    def inverse(self) -> "Jet":
        if not self.coefficients:
            raise ZeroDivisionError("zero Laurent jet")
        valuation = min(self.coefficients)
        leading = self.coefficient(valuation)
        first_inverse_exponent = -valuation
        count = HI - first_inverse_exponent
        inverse_unit: list[sp.Expr] = [sp.Integer(1) / leading]
        for degree in range(1, count + 1):
            convolution = sum(
                self.coefficient(valuation + index) * inverse_unit[degree - index]
                for index in range(1, degree + 1)
            )
            inverse_unit.append(-convolution / leading)
        return Jet({first_inverse_exponent + degree: coefficient for degree, coefficient in enumerate(inverse_unit)})


def series(*terms: tuple[sp.Expr, int]) -> Jet:
    return Jet({exponent: coefficient for coefficient, exponent in terms})


def scalar_curvature_jet(diagonal: tuple[Jet, Jet, Jet], y: sp.Symbol, z: sp.Symbol) -> Jet:
    """Assemble only finite Laurent jets of Gamma, Ricci, and scalar curvature."""

    dimension = 3
    inverse = tuple(entry.inverse() for entry in diagonal)
    gamma = [[[Jet.zero() for _ in range(dimension)] for _ in range(dimension)] for _ in range(dimension)]

    for upper in range(dimension):
        for left in range(dimension):
            for right in range(dimension):
                bracket = Jet.zero()
                if upper == left:
                    bracket = bracket + diagonal[upper].diff(right, y, z)
                if upper == right:
                    bracket = bracket + diagonal[upper].diff(left, y, z)
                if left == right:
                    bracket = bracket - diagonal[left].diff(upper, y, z)
                gamma[upper][left][right] = (inverse[upper] * bracket).scale(sp.Rational(1, 2))

    scalar = Jet.zero()
    for index in range(dimension):
        ricci = Jet.zero()
        for upper in range(dimension):
            ricci = ricci + gamma[upper][index][index].diff(upper, y, z)
            ricci = ricci - gamma[upper][index][upper].diff(index, y, z)
            for contracted in range(dimension):
                ricci = ricci + gamma[upper][upper][contracted] * gamma[contracted][index][index]
                ricci = ricci - gamma[upper][index][contracted] * gamma[contracted][index][upper]
        scalar = scalar + inverse[index] * ricci
    return scalar


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print(f"PASS  {label}")


def main() -> None:
    y, z = sp.symbols("y z", real=True)

    A2 = sp.Function("A2")(y, z)
    A3 = sp.Function("A3")(y, z)
    P0 = sp.Function("P0")(y, z)
    P1 = sp.Function("P1")(y, z)
    P2 = sp.Function("P2")(y, z)
    R0 = sp.Function("R0")(y, z)
    R1 = sp.Function("R1")(y, z)
    R2 = sp.Function("R2")(y, z)

    generic_metric = (
        series((A2, 2), (A3, 3)),
        series((P0, 0), (P1, 1), (P2, 2)),
        series((R0, 0), (R1, 1), (R2, 2)),
    )
    generic = scalar_curvature_jet(generic_metric, y, z)
    generic_lead = sp.factor(generic.coefficient(-3))
    generic_expected = (P1 / P0 + R1 / R0) / A2
    check("generic x^-3 coefficient", sp.cancel(generic_lead - generic_expected) == 0)
    check("generic x^-3 has no transverse derivatives", not generic_lead.has(sp.Derivative))
    check("generic terms below x^-3 absent", all(generic.coefficient(power) == 0 for power in range(LO, -3)))

    B = sp.Function("B")(y, z)
    B4 = sp.Function("B4")(y, z)
    C1 = sp.Function("C1")(y, z)
    C10 = sp.Function("C10")(y, z)
    C2 = sp.Function("C2")(y, z)
    C20 = sp.Function("C20")(y, z)

    reflection_metric = (
        series((B, 2), (B4, 4)),
        series((C1, -2), (C10, 0)),
        series((C2, -2), (C20, 0)),
    )
    reflection = scalar_curvature_jet(reflection_metric, y, z)
    reflection_lead = sp.factor(reflection.coefficient(-4))
    check("reflection x^-4 coefficient", sp.cancel(reflection_lead + 14 / B) == 0)
    check("reflection x^-4 has no transverse derivatives", not reflection_lead.has(sp.Derivative))
    check("reflection terms below x^-4 absent", all(reflection.coefficient(power) == 0 for power in range(LO, -4)))

    print("generic coefficient:", generic_lead)
    print("reflection coefficient:", reflection_lead)
    print("LEAD7 weighted-local-jet audit: 6 assertions passed")


if __name__ == "__main__":
    main()
