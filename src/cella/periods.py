"""Cella-native certified period/residue spike.

This module is not a numeric period evaluator. It records the exact structural
data that should come before numerical evaluation: elliptic quartic identity,
third-kind pole residues, branch-jump coefficients, exact K/Pi normal forms,
and the gaps that still need another spike.

The first spike is intentionally rational-only. That is a feature, not an
accident: it lets the kernel prove what it owns without leaning on SymPy or
mpmath while we identify the next native layer to build.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

from .qsqrt import QSqrt


def _q(x) -> Fraction:
    if isinstance(x, bool):
        raise TypeError("booleans are not exact period scalars")
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(x.strip())
    raise TypeError(f"expected exact integer or rational string, got {type(x).__name__}")


def _fmt(x) -> str:
    x = _q(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def _fmt_factor(value: Fraction) -> str:
    text = _fmt(value)
    return text if value.denominator == 1 else f"({text})"


def _square_part_and_free(n: int) -> tuple[int, int]:
    if n <= 0:
        raise ValueError("square decomposition needs a positive integer")
    square = 1
    free = 1
    d = 2
    while d * d <= n:
        exponent = 0
        while n % d == 0:
            n //= d
            exponent += 1
        if exponent:
            square *= d ** (exponent // 2)
            if exponent % 2:
                free *= d
        d += 1 if d == 2 else 2
    if n > 1:
        free *= n
    return square, free


def _sqrt_q(value: Fraction):
    value = _q(value)
    if value < 0:
        raise ValueError("complex square roots are outside this rational spike")
    if value == 0:
        return Fraction(0)
    sn, rn = _square_part_and_free(value.numerator)
    sd, rd = _square_part_and_free(value.denominator)
    coefficient = Fraction(sn, sd * rd)
    radicand = Fraction(rn * rd)
    root = isqrt(radicand.numerator)
    if radicand.denominator == 1 and root * root == radicand.numerator:
        return coefficient * root
    return QSqrt(0, coefficient, radicand)


def _scale_value(value, scale: Fraction):
    scale = _q(scale)
    if isinstance(value, QSqrt):
        return value * scale
    return _q(value) * scale


def _neg_value(value):
    if isinstance(value, QSqrt):
        return -value
    return -_q(value)


def _add_coeffs(out: dict[str, Fraction], atom: str, coeff) -> None:
    coeff = _q(coeff)
    if coeff == 0:
        return
    out[atom] = out.get(atom, Fraction(0)) + coeff
    if out[atom] == 0:
        del out[atom]


def _curve_m(curve: dict | None = None, m=None) -> Fraction:
    if curve is not None:
        if str(curve.get("kind", "legendre_even")) != "legendre_even":
            raise ValueError("this spike only supports curve kind 'legendre_even'")
        return _q(curve["m"])
    return _q(m)


def _curve_id(m: Fraction) -> str:
    return f"legendre_even:m={_fmt(m)}"


def _basis_atom_k(m: Fraction) -> str:
    return f"K({_fmt(m)})"


def _basis_atom_pi(q: Fraction, m: Fraction) -> str:
    return f"Pi({_fmt(q)};{_fmt(m)})"


def _sorted_basis_terms(terms: dict[str, Fraction]) -> dict[str, Fraction]:
    return {atom: terms[atom] for atom in sorted(terms)}


def period_quartic(kind: str, m) -> dict:
    """Return a native exact Legendre even quartic record."""
    if str(kind) != "legendre_even":
        raise ValueError("this spike only supports kind='legendre_even'")
    m_q = _q(m)
    if m_q in (0, 1):
        raise ValueError("m=0 or m=1 degenerates the quartic")
    branch_square = Fraction(1, 1) / m_q
    j = 256 * (1 - m_q + m_q * m_q) ** 3 / (m_q * m_q * (1 - m_q) ** 2)
    return {
        "kind": "legendre_even",
        "curve_id": _curve_id(m_q),
        "m": m_q,
        "equation": f"y^2 = (1 - x^2)*(1 - {_fmt_factor(m_q)}*x^2)",
        "expanded_coefficients": {
            "x^0": Fraction(1),
            "x^2": -(1 + m_q),
            "x^4": m_q,
        },
        "branch_squares": (Fraction(1), branch_square),
        "branch_points": ("+1", "-1", f"+sqrt({_fmt(branch_square)})", f"-sqrt({_fmt(branch_square)})"),
        "j_invariant": j,
        "discriminant_factor": m_q * m_q * (1 - m_q) ** 2,
        "method": "cella_native_exact_quartic_record",
        "gaps": (
            _gap("general_algebraic_number_field"),
            _gap("certified_numeric_evaluation"),
        ),
    }


def third_kind_residue(curve: dict, n, prefactor) -> dict:
    """Exact residue ledger for p dx / ((1-n*x^2)*y) on a Legendre quartic."""
    m_q = _curve_m(curve)
    n_q = _q(n)
    p_q = _q(prefactor)
    if n_q == 0:
        raise ValueError("n must be nonzero")
    x0_sq = Fraction(1) / n_q
    y0_sq = (1 - x0_sq) * (1 - m_q * x0_sq)
    if y0_sq == 0:
        raise ValueError("third-kind pole collides with a branch point")
    residue_square = p_q * p_q * n_q / (4 * (n_q - 1) * (n_q - m_q))
    magnitude = _sqrt_q(residue_square)
    positive_x_residue = _scale_value(magnitude, -1 if p_q >= 0 else 1)
    negative_x_residue = _neg_value(positive_x_residue)
    two_sided = _scale_value(positive_x_residue, 2)
    return {
        "curve_id": _curve_id(m_q),
        "differential": "prefactor*dx/((1 - n*x^2)*y)",
        "prefactor": p_q,
        "n": n_q,
        "x0_squared": x0_sq,
        "y0_squared": y0_sq,
        "residue_square": residue_square,
        "positive_x_residue": positive_x_residue,
        "negative_x_residue": negative_x_residue,
        "residue_antisymmetry": positive_x_residue == _neg_value(negative_x_residue),
        "one_sided_offset_over_pi_i": positive_x_residue,
        "two_sided_jump_over_pi_i": two_sided,
        "branch_convention": "canonical positive local square roots; positive-x pole residue carries the denominator derivative sign",
        "method": "cella_native_third_kind_residue_ledger",
        "gaps": (
            _gap("general_algebraic_number_field"),
            _gap("general_rational_differential_reduction"),
        ),
    }


def period_normal_form(
    kind: str,
    curve: dict,
    n=None,
    scale=1,
    weight_pi=1,
    weight_k=0,
    basis_terms: list | None = None,
    residue_jumps: list | None = None,
) -> dict:
    """Build an exact structural period normal form."""
    m_q = _curve_m(curve)
    terms: dict[str, Fraction] = {}
    regular_q = None
    route_identity = None
    if kind == "third_kind_cpv":
        n_q = _q(n)
        scale_q = _q(scale)
        wpi_q = _q(weight_pi)
        wk_q = _q(weight_k)
        if n_q > 1:
            regular_q = m_q / n_q
            _add_coeffs(terms, _basis_atom_k(m_q), scale_q * (wpi_q - wk_q))
            _add_coeffs(terms, _basis_atom_pi(regular_q, m_q), -scale_q * wpi_q)
            route_identity = "CPV Pi(n;m)=K(m)-Pi(m/n;m)"
        else:
            regular_q = n_q
            _add_coeffs(terms, _basis_atom_k(m_q), -scale_q * wk_q)
            _add_coeffs(terms, _basis_atom_pi(n_q, m_q), scale_q * wpi_q)
            route_identity = "regular Pi(n;m)"
    elif kind == "declared_basis":
        for item in basis_terms or []:
            _add_coeffs(terms, str(item["atom"]), _q(item["coefficient"]))
        route_identity = "declared exact period basis"
    else:
        raise ValueError("normal-form kind must be 'third_kind_cpv' or 'declared_basis'")

    return {
        "kind": "period_normal_form",
        "curve_id": _curve_id(m_q),
        "basis_terms": _sorted_basis_terms(terms),
        "residue_jumps": tuple(residue_jumps or ()),
        "regular_parameter_q": regular_q,
        "route_identity": route_identity,
        "numeric_evaluation": None,
        "method": "cella_native_period_basis_record",
        "gaps": (
            _gap("certified_numeric_evaluation"),
            _gap("general_rational_differential_reduction"),
        ),
    }


def _parse_basis_terms(record: dict) -> dict[str, Fraction]:
    return {str(atom): _q(coeff) for atom, coeff in record.get("basis_terms", {}).items()}


def period_route_compare(route_a: dict, route_b: dict) -> dict:
    """Compare two normal forms by exact structural basis difference."""
    curve_a = str(route_a.get("curve_id"))
    curve_b = str(route_b.get("curve_id"))
    if curve_a != curve_b:
        return {
            "equivalent": False,
            "curve_a": curve_a,
            "curve_b": curve_b,
            "difference_terms": {},
            "first_gap": {
                "gap": "curve_mismatch",
                "status": "open",
                "why": "normal forms live on different curve records",
                "next_spike": "curve_isomorphism_and_pullback_normalizer",
            },
            "method": "exact_period_normal_form_difference",
        }
    a_terms = _parse_basis_terms(route_a)
    b_terms = _parse_basis_terms(route_b)
    diff: dict[str, Fraction] = {}
    for atom in sorted(set(a_terms) | set(b_terms)):
        value = a_terms.get(atom, Fraction(0)) - b_terms.get(atom, Fraction(0))
        if value:
            diff[atom] = value
    equivalent = not diff and tuple(route_a.get("residue_jumps", ())) == tuple(route_b.get("residue_jumps", ()))
    return {
        "equivalent": equivalent,
        "curve_id": curve_a,
        "difference_terms": diff,
        "residue_jumps_match": tuple(route_a.get("residue_jumps", ())) == tuple(route_b.get("residue_jumps", ())),
        "first_gap": None if equivalent else {
            "gap": "period_basis_mismatch",
            "status": "open",
            "why": "the exact period-basis coefficients do not cancel",
            "next_spike": "differential_reduction_or_cycle_normalization_before_numeric_comparison",
        },
        "method": "exact_period_normal_form_difference",
    }


def e128_relative_path_record(target: str):
    """Narrow adapter to the certified E128 relative-path owner.

    Formal Legendre normal forms remain owned here; numeric execution remains
    isolated in ``cella.native_periods``.
    """
    from .native_periods.api import TARGETS
    from .native_periods.dbp_theta_route import canonical_source, compile_dbp_theta

    if target not in TARGETS:
        raise ValueError("unsupported E128 relative-period target")
    path = TARGETS[target][0]
    return compile_dbp_theta(canonical_source(path))


def legendre_ke_numerical_realization(atom: str, m, required_bits: int, certificate: bool = True):
    """Adapter from structural K/E atoms to their separate native realization."""
    from .native_periods.legendre_ke import legendre_ke_enclose

    return legendre_ke_enclose(atom, m, required_bits, certificate)


_GAPS = {
    "certified_numeric_evaluation": {
        "why": "period atoms are structurally certified but not enclosed by a native evaluator",
        "next_spike": "native_enclosure_evaluator_for_K_Pi_and_branch_jumps",
    },
    "general_algebraic_number_field": {
        "why": "this spike accepts rational parameters only; dual constants need exact algebraic fields such as Q(sqrt(2))",
        "next_spike": "Cella algebraic-number field parser and minimal-polynomial comparison",
    },
    "general_rational_differential_reduction": {
        "why": "only Legendre third-kind CPV templates are reduced; arbitrary rational differentials are not yet cohomology-reduced",
        "next_spike": "Hermite_style_reduction_of_rational_differentials_on_quartics",
    },
    "raw_bordered_hessian_surface_route": {
        "why": "the raw K_G surface integral is not yet transformed into a curve/differential/cycle record",
        "next_spike": "bordered_hessian_surface_integral_to_period_atom_compiler",
    },
}


def _gap(name: str) -> dict:
    item = _GAPS[name]
    return {
        "gap": name,
        "status": "open",
        "why": item["why"],
        "next_spike": item["next_spike"],
    }


def period_gap_report(scope: str = "elliptic_quartic_spike") -> dict:
    """Return the explicit remaining gaps for the native period spike."""
    return {
        "scope": str(scope),
        "gaps": tuple(_gap(name) for name in (
            "certified_numeric_evaluation",
            "general_algebraic_number_field",
            "general_rational_differential_reduction",
            "raw_bordered_hessian_surface_route",
        )),
        "method": "cella_native_gap_inventory",
    }
