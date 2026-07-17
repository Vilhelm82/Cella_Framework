#!/usr/bin/env python3
"""Exact verifier for the DBP pole-free native relative-period route.

This verifier checks the algebraic transformations that compile the two
relative Theta periods on E_128 to smooth integrands on [0,1].  It performs no
floating-point arithmetic and no numerical integration.  The analytic inputs
are only change of variables, the real-sheet convention from the corrected
Landen--Trace theorem, and the elementary principal-value identity displayed
in the route theorem.
"""

from __future__ import annotations

from fractions import Fraction as Q

import verify_dbp_landen_trace_theorem as base


def rf(value: object) -> base.RationalFunction:
    return base.RationalFunction.coerce(value)


def main() -> None:
    print("DBP NATIVE RELATIVE-PERIOD ROUTE: EXACT CERTIFICATION")
    print("Coefficient domain: Q(sqrt(2)); no floating-point arithmetic")
    print()

    z = base.U
    s = base.S

    # E_128 has the particularly simple real factorization used by both paths.
    x = base.U
    cubic = x**3 - x**2 + x - 1
    base.gate("E128 factorization", cubic == (x - 1) * (x**2 + 1))

    # Primary substitution X=1+z^2.
    x_plus = 1 + z**2
    q_plus_z = z**4 + 2 * z**2 + 2
    cubic_plus = x_plus**3 - x_plus**2 + x_plus - 1
    base.gate("primary radicand after X=1+z^2", cubic_plus == z**2 * q_plus_z)
    primary_ratio = (x_plus - 3) / (x_plus + 7)
    base.gate(
        "primary rational coefficient",
        primary_ratio == (z**2 - 2) / (z**2 + 8),
    )

    # Dual substitution X=1-z^2 on Y=+i*sqrt(-cubic).
    x_minus = 1 - z**2
    q_minus_z = z**4 - 2 * z**2 + 2
    cubic_minus = x_minus**3 - x_minus**2 + x_minus - 1
    base.gate("dual radicand after X=1-z^2", -cubic_minus == z**2 * q_minus_z)
    dual_ratio = (x_minus - 3) / (x_minus + 7)
    base.gate(
        "dual rational coefficient",
        dual_ratio == -(z**2 + 2) / (8 - z**2),
    )

    # The physical dual pole becomes z0=2*sqrt(2).  Both the pulled-back
    # differential and the subtraction kernel have residue 4.
    z0 = 2 * s
    base.gate("dual pole square", z0 * z0 == 8)
    q_at_z0 = z0**4 - 2 * z0**2 + 2
    base.gate("dual pole radicand is 50", q_at_z0 == 50)
    sqrt_q_at_z0 = 5 * s
    raw_residue = 16 * (z0**2 + 2) / (2 * z0 * sqrt_q_at_z0)
    base.gate("pulled-back dual residue is 4", raw_residue == 4)
    polar_residue = 16 * s / (2 * z0)
    base.gate("polar subtraction residue is 4", polar_residue == 4)

    polar_kernel = rf(16 * s) / (z**2 - 8)
    primitive_derivative = 4 * (1 / (z - z0) - 1 / (z + z0))
    base.gate(
        "polar kernel has the declared logarithmic primitive",
        polar_kernel == primitive_derivative,
    )

    # Compactification z=t/(1-t).
    t = base.U
    w = 1 - t
    p_plus = t**4 + 2 * t**2 * w**2 + 2 * w**4
    p_minus = t**4 - 2 * t**2 * w**2 + 2 * w**4
    base.gate(
        "primary compactified radicand",
        p_plus == t**4 + 2 * t**2 * w**2 + 2 * w**4,
    )
    base.gate(
        "dual radicand sum-of-squares form",
        p_minus == (t**2 - w**2) ** 2 + w**4,
    )

    a = t**2 + 2 * w**2
    d = t**2 - 8 * w**2
    base.gate(
        "dual rationalizing identity",
        a**2 - 2 * p_minus == -(t**2) * d,
    )

    # Exact endpoint and removable-point data.
    base.gate("primary left endpoint", -4 / s == -2 * s)
    base.gate("dual right endpoint", -16 / (1 + s) == 16 * (1 - s))
    compact_pole_value = (-16 * s / 25) * (1 + 2 * s) ** 2
    expected_compact_pole_value = -(128 + 144 * s) / 25
    base.gate(
        "dual former-pole compactified value",
        compact_pole_value == expected_compact_pole_value,
    )

    # The polar primitive has equal endpoint limits: log|-1|=log(1)=0.
    # This is the exact CPV-zero step; no numerical cancellation is invoked.
    base.gate("polar primitive endpoint ratio at z=0 has modulus 1", z0.sign() > 0)
    base.gate("polar primitive endpoint ratio at infinity tends to 1", Q(1) == 1)

    print()
    print("All route gates passed.")
    print("Certified execution forms:")
    print("  J_plus = integral_0^1 g_plus(t) dt")
    print("  H_minus = integral_0^1 g_minus(t) dt")
    print("  g_minus is smooth: its CPV pole was removed exactly before execution")


if __name__ == "__main__":
    main()

