"""Certified local-geometry and polynomial-proof primitives.

This is the first proof-kernel layer extracted from the verification scripts.
It intentionally covers narrow, repeated proof moves:

- local pole laws for parity-fixed and generic quadratic metric germs;
- master-quadric codimension-1 pole coefficients from exponent vectors;
- codimension-2 corner Newton/support vertices;
- exact symbolic-surface jets at rational points;
- sparse polynomial coefficient-positivity certificates after exact shifts;
- univariate Sturm positivity on an open ray.

The module uses only exact rational arithmetic. It is not a general CAS.
"""

from __future__ import annotations

from fractions import Fraction
import keyword
from math import comb
import re


def _q(x) -> Fraction:
    if isinstance(x, bool):
        raise TypeError("booleans are not exact rationals")
    return Fraction(x)


def _z(x) -> int:
    q = _q(x)
    if q.denominator != 1:
        raise ValueError(f"expected an integer, got {q}")
    return q.numerator


def _trim(poly: list[Fraction]) -> list[Fraction]:
    out = list(poly)
    while out and out[-1] == 0:
        out.pop()
    return out


def _degree(poly: list[Fraction]) -> int:
    return len(_trim(poly)) - 1


def _eval_poly(poly: list[Fraction], x: Fraction) -> Fraction:
    acc = Fraction(0)
    for coeff in reversed(poly):
        acc = acc * x + coeff
    return acc


def _derivative(poly: list[Fraction]) -> list[Fraction]:
    return _trim([poly[i] * i for i in range(1, len(poly))])


def _divmod_poly(num: list[Fraction], den: list[Fraction]) -> tuple[list[Fraction], list[Fraction]]:
    num = _trim(num)
    den = _trim(den)
    if not den:
        raise ZeroDivisionError("polynomial division by zero")
    if _degree(num) < _degree(den):
        return [], num
    q = [Fraction(0)] * (_degree(num) - _degree(den) + 1)
    r = num[:]
    den_deg = _degree(den)
    den_lead = den[-1]
    while _degree(r) >= den_deg and r:
        shift = _degree(r) - den_deg
        coeff = r[-1] / den_lead
        q[shift] = coeff
        for i, d in enumerate(den):
            r[i + shift] -= coeff * d
        r = _trim(r)
    return _trim(q), r


def _sign(x: Fraction) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def _variations(signs: list[int]) -> int:
    nz = [s for s in signs if s != 0]
    return sum(1 for a, b in zip(nz, nz[1:]) if a != b)


def _sturm_sequence(poly: list[Fraction]) -> list[list[Fraction]]:
    p0 = _trim(poly)
    if not p0:
        raise ValueError("zero polynomial has indeterminate sign")
    p1 = _derivative(p0)
    if not p1:
        return [p0]
    seq = [p0, p1]
    while seq[-1]:
        _, rem = _divmod_poly(seq[-2], seq[-1])
        if not rem:
            break
        seq.append([-c for c in rem])
    return seq


def _poly_from_terms(variables: tuple[str, ...], terms) -> dict[tuple[int, ...], Fraction]:
    n = len(variables)
    poly: dict[tuple[int, ...], Fraction] = {}
    for coeff, powers in terms:
        if len(powers) != n:
            raise ValueError("term exponent length does not match variables")
        exp = tuple(int(p) for p in powers)
        if any(p < 0 for p in exp):
            raise ValueError("polynomial exponents must be nonnegative")
        poly[exp] = poly.get(exp, Fraction(0)) + _q(coeff)
    return {k: v for k, v in poly.items() if v}


def _terms_from_poly(poly: dict[tuple[int, ...], Fraction]) -> tuple[tuple[Fraction, tuple[int, ...]], ...]:
    return tuple((coeff, exp) for exp, coeff in sorted(poly.items(), key=lambda item: (sum(item[0]), item[0])))


def _univariate_coeffs(variables: tuple[str, ...], terms) -> list[Fraction]:
    if len(variables) != 1:
        raise ValueError("Sturm certificates are univariate")
    poly = _poly_from_terms(variables, terms)
    degree = max((exp[0] for exp in poly), default=-1)
    coeffs = [Fraction(0)] * (degree + 1)
    for (power,), coeff in poly.items():
        coeffs[power] += coeff
    return _trim(coeffs)


def master_quadric_pole_law(exponents, B=Fraction(1)) -> dict:
    """Codimension-1 monomial metric pole law from an exponent vector.

    For ``g_xx = B x^p0`` and ``g_aa = A_a x^pa`` with constant leading units,
    the scalar curvature has leading monomial

        R = C(p)/B * x^-(p0+2).

    The transverse amplitudes ``A_a`` cancel. This is the codim-1 master law
    behind the parity-fixed face: p0=2 and pa=-2 gives C(p)=-m(m+5).
    """
    exponents = tuple(_q(p) for p in exponents)
    B = _q(B)
    if len(exponents) < 2:
        raise ValueError("master_quadric needs [radial_exponent, transverse_exponents...]")
    if B == 0:
        raise ValueError("B must be nonzero")
    p0, transverse = exponents[0], exponents[1:]
    if p0 == -2:
        raise ValueError("radial exponent p0=-2 is the logarithmic-distance case, not this pole law")

    s1 = sum(transverse, Fraction(0))
    diag = sum(p * p for p in transverse)
    pair = sum(transverse[i] * transverse[j] for i in range(len(transverse))
               for j in range(i + 1, len(transverse)))
    C_p = -Fraction(1, 2) * (diag + pair - (p0 + 2) * s1)
    return {
        "kind": "master_quadric",
        "coordinate": "x",
        "radial_exponent": p0,
        "transverse_exponents": transverse,
        "order": p0 + 2,
        "C_p": C_p,
        "B": B,
        "coefficient": C_p / B,
        "law": "R = C(p)/B * x^-(p0+2)",
        "formula": "C(p)=-1/2*(sum p_a^2 + sum_{a<b} p_a p_b - (p0+2)*sum p_a)",
    }


def local_pole_law(kind: str, **kwargs) -> dict:
    """Return an exact local pole-law certificate value."""
    if kind == "master_quadric":
        return master_quadric_pole_law(kwargs["exponents"], kwargs.get("B", Fraction(1)))
    if kind == "parity_fixed":
        m = _z(kwargs["m"])
        B = _q(kwargs["B"])
        if m < 1:
            raise ValueError("m must be at least 1")
        if B <= 0:
            raise ValueError("B must be positive for the parity-fixed law")
        c = Fraction(-m * (m + 5), 1) / B
        return {
            "kind": "parity_fixed",
            "coordinate": "x",
            "order": Fraction(4),
            "coefficient": c,
            "law": "R = -m(m+5)/B * x^-4",
            "intrinsic_distance": {
                "power": Fraction(2),
                "coefficient": Fraction(-m * (m + 5), 4),
            },
        }
    if kind == "generic_quadratic":
        A = _q(kwargs["A"])
        p0 = tuple(_q(x) for x in kwargs["transverse_P0"])
        p1 = tuple(_q(x) for x in kwargs["transverse_P1"])
        if A == 0:
            raise ValueError("A must be nonzero")
        if len(p0) != len(p1) or not p0:
            raise ValueError("transverse_P0 and transverse_P1 must have the same nonzero length")
        if any(x == 0 for x in p0):
            raise ValueError("transverse_P0 entries must be nonzero")
        drift = sum(b / a for a, b in zip(p0, p1))
        return {
            "kind": "generic_quadratic",
            "coordinate": "x",
            "order": Fraction(3),
            "coefficient": drift / A,
            "drift": drift,
            "law": "R = (1/A) * sum(P_a1/P_a0) * x^-3 + O(x^-2)",
        }
    raise ValueError(f"unknown pole-law kind {kind!r}")


def _check_symbol_name(name: str) -> None:
    if not name.isidentifier() or keyword.iskeyword(name) or name.startswith("_"):
        raise ValueError(f"invalid symbolic variable name {name!r}")


_DECIMAL_LITERAL = re.compile(
    r"(?<![A-Za-z0-9_])(?:\d+\.\d*|\.\d+|\d+[eE][+-]?\d+)(?![A-Za-z0-9_])"
)


def _reject_decimal_literals(expression: str) -> None:
    match = _DECIMAL_LITERAL.search(expression)
    if match:
        raise ValueError(f"decimal literal {match.group(0)!r} is not exact; use an integer or rational string")


def _sympy_rational_to_fraction(value) -> Fraction:
    import sympy as sp

    value = sp.cancel(sp.simplify(value))
    if value.is_Rational:
        return Fraction(int(value.p), int(value.q))
    raise ValueError(f"symbolic value is not rational: {value}")


def surface_jet(expression: str, variables, point, require_on_surface: bool = True) -> dict:
    """Differentiate a symbolic implicit surface and return its exact rational 2-jet."""
    import sympy as sp

    expression = str(expression)
    _reject_decimal_literals(expression)
    variables = tuple(str(v) for v in variables)
    if not variables:
        raise ValueError("at least one variable is required")
    if len(set(variables)) != len(variables):
        raise ValueError("variables must be distinct")
    for name in variables:
        _check_symbol_name(name)

    point = tuple(_q(v) for v in point)
    if len(point) != len(variables):
        raise ValueError("point length does not match variables")

    symbols = tuple(sp.Symbol(name) for name in variables)
    local_dict = {name: sym for name, sym in zip(variables, symbols)}
    expr = sp.sympify(expression, locals=local_dict, rational=True)
    unknown = expr.free_symbols - set(symbols)
    if unknown:
        names = ", ".join(sorted(str(s) for s in unknown))
        raise ValueError(f"expression contains unknown symbols: {names}")
    if expr.atoms(sp.Float):
        raise ValueError("surface expression contains decimal floats; use exact rationals")

    subs = {sym: sp.Rational(v.numerator, v.denominator) for sym, v in zip(symbols, point)}
    surface_value = _sympy_rational_to_fraction(expr.subs(subs))
    on_surface = surface_value == 0
    if require_on_surface and not on_surface:
        raise ValueError(f"point is not on the surface: F(point)={surface_value}")

    gradient = tuple(_sympy_rational_to_fraction(sp.diff(expr, sym).subs(subs)) for sym in symbols)
    hessian = tuple(
        tuple(_sympy_rational_to_fraction(sp.diff(expr, si, sj).subs(subs)) for sj in symbols)
        for si in symbols
    )
    return {
        "expression": str(expr),
        "variables": variables,
        "point": point,
        "surface_value": surface_value,
        "on_surface": on_surface,
        "gradient": gradient,
        "hessian": hessian,
        "jet": {
            "point": point,
            "g": gradient,
            "H": hessian,
        },
        "method": "sympy_exact_differentiate_then_rationalize",
    }


def corner_newton(weights: dict, path: dict | None = None) -> dict:
    """Codimension-2 corner vertex/support certificate from monomial weights."""
    p0 = _z(weights["p0"])
    q0 = _z(weights["q0"])
    p1 = _z(weights["p1"])
    q1 = _z(weights["q1"])
    p2 = _z(weights["p2"])
    q2 = _z(weights["q2"])

    A = Fraction(-p0 * p0 + p0 * p1 - p0 * p2 + 2 * p0 + p1 * p2 - p2 * p2 + 2 * p2)
    B = Fraction(-q0 * q0 - q0 * q1 + q0 * q2 + 2 * q0 - q1 * q1 + q1 * q2 + 2 * q1)
    vertices = {
        "V1": {"exponent": (Fraction(-(p1 + 2)), Fraction(-q1)), "coefficient": A},
        "V2": {"exponent": (Fraction(-p2), Fraction(-(q2 + 2))), "coefficient": B},
        # The exact coefficient of V0 depends on the spectator s-jet. The
        # weight certificate can still decide whether the vertex is polar.
        "V0": {"exponent": (Fraction(-p0), Fraction(-q0)), "coefficient": None},
    }
    for item in vertices.values():
        u, v = item["exponent"]
        item["polar"] = (u < 0 or v < 0)
        item["active"] = item["polar"] and item["coefficient"] != 0

    active = {k: v for k, v in vertices.items() if v["active"]}
    out = {
        "weights": {k: Fraction(v) for k, v in weights.items()},
        "vertices": vertices,
        "active_vertices": tuple(active.keys()),
        "face_data": {
            "p_x": Fraction(p1 + 2),
            "p_y": Fraction(q2 + 2),
            "r_x": Fraction(-p2),
            "r_y": Fraction(-q1),
        },
    }
    if path is not None:
        ax = _q(path["ax"])
        ay = _q(path["ay"])
        orders = {}
        for name, item in active.items():
            u, v = item["exponent"]
            orders[name] = -(u * ax + v * ay)
        out["path"] = {"ax": ax, "ay": ay}
        out["support_terms"] = orders
        out["support_order"] = max(orders.values()) if orders else None
    return out


def shifted_polynomial_certificate(variables, terms, shifts=None) -> dict:
    """Coefficient-positivity certificate after exact affine shifts."""
    variables = tuple(str(v) for v in variables)
    shifts = shifts or {}
    new_variables = tuple(str(shifts[v]["new"]) if v in shifts else v for v in variables)
    if len(set(new_variables)) != len(new_variables):
        raise ValueError("shifted variables must remain distinct")
    new_index = {v: i for i, v in enumerate(new_variables)}

    out: dict[tuple[int, ...], Fraction] = {}
    for coeff0, powers in terms:
        coeff0 = _q(coeff0)
        if len(powers) != len(variables):
            raise ValueError("term exponent length does not match variables")
        term_poly = {tuple([0] * len(new_variables)): coeff0}
        for old_var, exp_raw in zip(variables, powers):
            exp = int(exp_raw)
            if exp < 0:
                raise ValueError("polynomial exponents must be nonnegative")
            idx = new_index[str(shifts[old_var]["new"])] if old_var in shifts else new_index[old_var]
            offset = _q(shifts[old_var]["offset"]) if old_var in shifts else Fraction(0)
            factor = []
            for k in range(exp + 1):
                powers_new = [0] * len(new_variables)
                powers_new[idx] = k
                factor.append((tuple(powers_new), Fraction(comb(exp, k)) * offset ** (exp - k)))
            next_poly: dict[tuple[int, ...], Fraction] = {}
            for e1, c1 in term_poly.items():
                for e2, c2 in factor:
                    exp_new = tuple(a + b for a, b in zip(e1, e2))
                    next_poly[exp_new] = next_poly.get(exp_new, Fraction(0)) + c1 * c2
            term_poly = {k: v for k, v in next_poly.items() if v}
        for exp, coeff in term_poly.items():
            out[exp] = out.get(exp, Fraction(0)) + coeff

    out = {k: v for k, v in out.items() if v}
    coeffs = tuple(out.values())
    nonnegative = bool(coeffs) and all(c >= 0 for c in coeffs)
    positive = nonnegative and any(c > 0 for c in coeffs)
    return {
        "variables": new_variables,
        "terms": _terms_from_poly(out),
        "coefficient_nonnegative": nonnegative,
        "positive": positive,
        "method": "coefficient_nonnegative_on_positive_orthant",
    }


def sturm_positive_on_open_ray(variable: str, terms, lower) -> dict:
    """Prove a univariate polynomial has positive sign on (lower, infinity)."""
    lower = _q(lower)
    coeffs = _univariate_coeffs((variable,), terms)
    seq = _sturm_sequence(coeffs)
    lower_signs = [_sign(_eval_poly(p, lower)) for p in seq]
    infinity_signs = [_sign(p[-1]) for p in seq]
    root_count = _variations(lower_signs) - _variations(infinity_signs)
    sample = lower + 1
    sample_value = _eval_poly(coeffs, sample)
    positive = root_count == 0 and sample_value > 0
    return {
        "variable": variable,
        "lower": lower,
        "root_count": Fraction(root_count),
        "sample": sample,
        "sample_value": sample_value,
        "positive": positive,
        "degree": Fraction(_degree(coeffs)),
        "sturm_lengths": tuple(Fraction(len(p)) for p in seq),
    }
