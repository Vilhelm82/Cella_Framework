#!/usr/bin/env python3
"""Exact extension verifier for DBP Landen--Trace Theorem v1.1.

This script runs the v1.0 trace/isogeny verifier and then checks the corrected
anti-translation closure:

* the exact anti-invariant rational coefficient;
* its complete-interval reduction (no incomplete amplitude);
* the logarithmic derivative identity;
* the algebraic normalizations giving residues 4i and 4;
* the endpoint data that give -4*pi in the primary channel and CPV 0 in
  the dual channel.

No floating-point arithmetic or external package is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q

import verify_dbp_landen_trace_theorem as base


@dataclass(frozen=True)
class QTI:
    """Element of Q(t,i), t^4=2 and i^2=-1, in the basis t^k i^j."""

    coeffs: tuple[Q, Q, Q, Q, Q, Q, Q, Q]

    @staticmethod
    def zero() -> "QTI":
        return QTI((Q(0),) * 8)

    @staticmethod
    def rational(value: int | Q) -> "QTI":
        data = [Q(0)] * 8
        data[0] = Q(value)
        return QTI(tuple(data))

    @staticmethod
    def basis(t_power: int, i_power: int, coeff: int | Q = 1) -> "QTI":
        t_factor, t_remainder = divmod(t_power, 4)
        i_factor, i_remainder = divmod(i_power, 2)
        scale = Q(coeff) * (Q(2) ** t_factor) * ((-1) ** i_factor)
        data = [Q(0)] * 8
        data[4 * i_remainder + t_remainder] = scale
        return QTI(tuple(data))

    @staticmethod
    def from_qs2(value: base.QS2) -> "QTI":
        return QTI.rational(value.a) + QTI.basis(2, 0, value.b)

    def __add__(self, other: object) -> "QTI":
        if not isinstance(other, QTI):
            other = QTI.rational(other)  # type: ignore[arg-type]
        return QTI(tuple(a + b for a, b in zip(self.coeffs, other.coeffs)))

    __radd__ = __add__

    def __neg__(self) -> "QTI":
        return QTI(tuple(-x for x in self.coeffs))

    def __sub__(self, other: object) -> "QTI":
        return self + (-other)  # type: ignore[operator]

    def __rsub__(self, other: object) -> "QTI":
        return QTI.rational(other) - self  # type: ignore[arg-type]

    def __mul__(self, other: object) -> "QTI":
        if not isinstance(other, QTI):
            other = QTI.rational(other)  # type: ignore[arg-type]
        out = [Q(0)] * 8
        for left_i, left_coeff in enumerate(self.coeffs):
            if left_coeff == 0:
                continue
            left_ip, left_tp = divmod(left_i, 4)
            for right_i, right_coeff in enumerate(other.coeffs):
                if right_coeff == 0:
                    continue
                right_ip, right_tp = divmod(right_i, 4)
                t_factor, t_remainder = divmod(left_tp + right_tp, 4)
                i_factor, i_remainder = divmod(left_ip + right_ip, 2)
                scale = (Q(2) ** t_factor) * ((-1) ** i_factor)
                index = 4 * i_remainder + t_remainder
                out[index] += left_coeff * right_coeff * scale
        return QTI(tuple(out))

    __rmul__ = __mul__

    def __truediv__(self, scalar: int | Q) -> "QTI":
        scalar = Q(scalar)
        return QTI(tuple(x / scalar for x in self.coeffs))

    def __pow__(self, exponent: int) -> "QTI":
        if exponent < 0:
            raise ValueError("negative QTI power is not needed")
        result = QTI.rational(1)
        base_value = self
        power = exponent
        while power:
            if power & 1:
                result = result * base_value
            base_value = base_value * base_value
            power >>= 1
        return result


T = QTI.basis(1, 0)
II = QTI.basis(0, 1)


def rat(value: object) -> base.RationalFunction:
    return base.RationalFunction.coerce(value)


def verify_anti_channel(epsilon: int) -> None:
    label = "primary" if epsilon == 1 else "dual"
    m = (2 - epsilon * base.S) / 4
    m_bar = 1 - m
    n = (4 - epsilon * 3 * base.S) / 8
    A = 3 + epsilon * 2 * base.S
    B = 2 + epsilon * 2 * base.S
    a = 2 * m - 1
    b = base.QS2(Q(-1, 8))
    d = m * (1 - n)
    c = m / (m - n)

    base.gate(f"{label}: n=-m^2/(1-2m)", n == -(m * m) / (1 - 2 * m))
    base.gate(f"{label}: A*m=1-m", A * m == m_bar)
    base.gate(f"{label}: d/(m-n)=1-m", d / (m - n) == m_bar)
    base.gate(f"{label}: A*m/d=4*epsilon*s", A * m / d == 4 * epsilon * base.S)

    def F(argument: base.RationalFunction) -> base.RationalFunction:
        return rat(A * m) / (rat(d) - argument * n) - B

    translated_u = rat(b) / base.U
    anti_f = F(base.U) - F(translated_u)
    expected_anti_f = (
        rat(A * m * n)
        * (base.U - translated_u)
        / ((rat(d) - base.U * n) * (rat(d) - translated_u * n))
    )
    base.gate(f"{label}: explicit anti-invariant coefficient", anti_f == expected_anti_f)

    # Pull both terms back to the original complete parameter z=r^2.
    z = base.U
    u_of_z = (z - 1) * m
    original_in_z = rat(A) / (1 - z * n) - B
    translated_in_z = rat(A * c) * (1 - z) / (1 - z * m_bar) - B
    base.gate(
        f"{label}: translated coefficient remains on complete interval",
        F(rat(b) / u_of_z) == translated_in_z,
    )
    complete_decomposition = rat(A) * (
        rat(1) / (1 - z * n)
        - c / m_bar
        + rat(c * m / m_bar) / (1 - z * m_bar)
    )
    base.gate(
        f"{label}: complete K/Pi partial-fraction reduction",
        F(u_of_z) - F(rat(b) / u_of_z) == complete_decomposition,
    )

    # Algebra behind d log((y-ell*u)/(y+ell*u)).
    u0 = d / n
    u1 = b / u0
    z0 = u0 + a + b / u0
    curve = base.U**3 + base.U**2 * a + base.U * b
    curve_derivative = 3 * base.U**2 + base.U * (2 * a) + b
    base.gate(
        f"{label}: logarithmic numerator identity",
        base.U * curve_derivative - 2 * curve == base.U * (base.U**2 - b),
    )
    base.gate(
        f"{label}: logarithmic denominator factorization",
        curve - base.U**2 * z0
        == base.U * (base.U - u0) * (base.U - u1),
    )
    expected_kernel = (
        (base.U**2 - b)
        / ((base.U - u0) * (base.U - u1))
        * (-(A * m / d))
    )
    base.gate(f"{label}: anti coefficient is a dlog kernel", anti_f == expected_kernel)

    # Exact algebraic slope and residue normalization.
    if epsilon == 1:
        ell = -2 * II * T
        residue = 4 * II
    else:
        ell = -2 * T
        residue = QTI.rational(4)
    base.gate(f"{label}: ell^2 equals pole z-coordinate", ell**2 == QTI.from_qs2(z0))
    rhs = (T**7) * QTI.from_qs2(A * m / d) / 2
    base.gate(f"{label}: dlog residue normalization", residue * ell == rhs)

    # Endpoint values are f(-m,0)=-1 and lim_{u->0-} f=1.
    base.gate(f"{label}: initial logarithmic endpoint is -1", m.sign() > 0)
    base.gate(f"{label}: terminal logarithmic endpoint is 1", b.sign() < 0)


def main() -> None:
    base.main()
    print()
    print("DBP LANDEN--TRACE v1.1: ANTI-TRANSLATION CLOSURE")
    verify_anti_channel(+1)
    verify_anti_channel(-1)
    print()
    print("All v1.1 extension gates passed.")
    print("Certified analytic endpoint consequences:")
    print("  primary: integral(alpha_+) = 4*i*(i*pi) = -4*pi")
    print("  dual CPV: integral(alpha_-) = 0")
    print("  dual one-sided values: integral(alpha_-) in { -4*pi*i, +4*pi*i }")


if __name__ == "__main__":
    main()
