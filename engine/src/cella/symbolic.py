"""Exact rational-function symbolic arm for Cella.

This module is deliberately smaller than a CAS. It owns a sparse
``Q[variables]`` polynomial representation, a rational-function layer over that
ring, and a restricted native front-end that compiles infix expressions directly
to Cella's exact term tables.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from fractions import Fraction
import keyword
from math import gcd
import re
from typing import Iterable

from .proofs import master_quadric_pole_law


_DECIMAL_LITERAL = re.compile(
    r"(?<![A-Za-z0-9_])(?:\d+\.\d*|\.\d+|\d+[eE][+-]?\d+)(?![A-Za-z0-9_])"
)


def _q(x) -> Fraction:
    if isinstance(x, bool):
        raise TypeError("booleans are not exact rationals")
    return Fraction(x)


def _z_or_q(x) -> Fraction:
    return _q(str(x).strip() if isinstance(x, str) else x)


def _check_symbol_name(name: str) -> None:
    if not name.isidentifier() or keyword.iskeyword(name) or name.startswith("_"):
        raise ValueError(f"invalid symbolic variable name {name!r}")


def _reject_decimal_literals(expression: str) -> None:
    match = _DECIMAL_LITERAL.search(expression)
    if match:
        raise ValueError(f"decimal literal {match.group(0)!r} is not exact; use an integer or rational string")


def _validate_variables(variables) -> tuple[str, ...]:
    out = tuple(str(v) for v in variables)
    if len(set(out)) != len(out):
        raise ValueError("variables must be distinct")
    for name in out:
        _check_symbol_name(name)
    return out


def _fraction_text(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b) if a and b else 0


def _common_content(polys: Iterable["Poly"]) -> Fraction:
    coeffs: list[Fraction] = []
    for poly in polys:
        coeffs.extend(poly.coefficients())
    if not coeffs:
        return Fraction(1)
    den_lcm = 1
    for coeff in coeffs:
        den_lcm = _lcm(den_lcm, coeff.denominator)
    int_gcd = 0
    for coeff in coeffs:
        int_gcd = gcd(int_gcd, abs(coeff.numerator * (den_lcm // coeff.denominator)))
    return Fraction(int_gcd, den_lcm) if int_gcd else Fraction(1)


def _term_sort(item: tuple[tuple[int, ...], Fraction]) -> tuple[int, tuple[int, ...]]:
    exp, _coeff = item
    return (sum(exp), exp)


@dataclass(frozen=True)
class Poly:
    """Sparse polynomial over Q in a fixed ordered variable tuple."""

    variables: tuple[str, ...]
    terms: tuple[tuple[tuple[int, ...], Fraction], ...]

    @staticmethod
    def from_terms(variables, items: Iterable[tuple[Iterable[int], Fraction]]) -> "Poly":
        variables = _validate_variables(variables)
        n = len(variables)
        merged: dict[tuple[int, ...], Fraction] = {}
        for exp_raw, coeff_raw in items:
            exp = tuple(int(e) for e in exp_raw)
            if len(exp) != n:
                raise ValueError("term exponent length does not match variables")
            if any(e < 0 for e in exp):
                raise ValueError("polynomial exponents must be nonnegative")
            coeff = _q(coeff_raw)
            if coeff:
                merged[exp] = merged.get(exp, Fraction(0)) + coeff
        merged = {exp: coeff for exp, coeff in merged.items() if coeff}
        return Poly(variables, tuple(sorted(merged.items(), key=_term_sort)))

    @staticmethod
    def zero(variables) -> "Poly":
        return Poly.from_terms(variables, ())

    @staticmethod
    def one(variables) -> "Poly":
        variables = _validate_variables(variables)
        return Poly.from_terms(variables, ((tuple([0] * len(variables)), Fraction(1)),))

    @staticmethod
    def constant(variables, value) -> "Poly":
        variables = _validate_variables(variables)
        value = _q(value)
        if value == 0:
            return Poly.zero(variables)
        return Poly.from_terms(variables, ((tuple([0] * len(variables)), value),))

    def _dict(self) -> dict[tuple[int, ...], Fraction]:
        return dict(self.terms)

    def _same_ring(self, other: "Poly") -> None:
        if self.variables != other.variables:
            raise ValueError("polynomials are in different variable rings")

    def coefficients(self) -> tuple[Fraction, ...]:
        return tuple(coeff for _exp, coeff in self.terms)

    def is_zero(self) -> bool:
        return not self.terms

    def is_one(self) -> bool:
        return self.terms == ((tuple([0] * len(self.variables)), Fraction(1)),)

    def is_constant(self) -> bool:
        return not self.terms or all(exp == tuple([0] * len(self.variables)) for exp, _ in self.terms)

    def constant_value(self) -> Fraction:
        if not self.terms:
            return Fraction(0)
        if not self.is_constant():
            raise ValueError("polynomial is not constant")
        return self.terms[0][1]

    def leading_coeff(self) -> Fraction:
        if not self.terms:
            return Fraction(0)
        return self.terms[-1][1]

    def scale(self, value) -> "Poly":
        value = _q(value)
        if value == 0 or self.is_zero():
            return Poly.zero(self.variables)
        return Poly.from_terms(self.variables, ((exp, coeff * value) for exp, coeff in self.terms))

    def __neg__(self) -> "Poly":
        return self.scale(-1)

    def __add__(self, other: "Poly") -> "Poly":
        self._same_ring(other)
        merged = self._dict()
        for exp, coeff in other.terms:
            merged[exp] = merged.get(exp, Fraction(0)) + coeff
        return Poly.from_terms(self.variables, merged.items())

    def __sub__(self, other: "Poly") -> "Poly":
        return self + (-other)

    def __mul__(self, other: "Poly") -> "Poly":
        self._same_ring(other)
        if self.is_zero() or other.is_zero():
            return Poly.zero(self.variables)
        merged: dict[tuple[int, ...], Fraction] = {}
        for e1, c1 in self.terms:
            for e2, c2 in other.terms:
                exp = tuple(a + b for a, b in zip(e1, e2))
                merged[exp] = merged.get(exp, Fraction(0)) + c1 * c2
        return Poly.from_terms(self.variables, merged.items())

    def pow(self, exponent: int) -> "Poly":
        exponent = int(exponent)
        if exponent < 0:
            raise ValueError("polynomial powers must be nonnegative")
        result = Poly.one(self.variables)
        base = self
        n = exponent
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1
        return result

    def term_record(self) -> list[list]:
        return [[_fraction_text(coeff), [str(e) for e in exp]] for exp, coeff in self.terms]

    def record(self) -> dict:
        return {
            "variables": list(self.variables),
            "terms": self.term_record(),
            "term_count": str(len(self.terms)),
            "is_zero": self.is_zero(),
            "text": self.text(),
        }

    def text(self) -> str:
        if self.is_zero():
            return "0"
        chunks = []
        for exp, coeff in self.terms:
            coeff_abs = abs(coeff)
            vars_text = []
            for name, power in zip(self.variables, exp):
                if power == 1:
                    vars_text.append(name)
                elif power > 1:
                    vars_text.append(f"{name}^{power}")
            mono = "*".join(vars_text)
            if mono:
                coeff_part = "" if coeff_abs == 1 else _fraction_text(coeff_abs) + "*"
                body = coeff_part + mono
            else:
                body = _fraction_text(coeff_abs)
            sign = "-" if coeff < 0 else "+"
            chunks.append((sign, body))
        first_sign, first_body = chunks[0]
        out = ("-" if first_sign == "-" else "") + first_body
        for sign, body in chunks[1:]:
            out += f" {sign} {body}"
        return out


@dataclass(frozen=True)
class Rat:
    """Rational function over a fixed sparse polynomial ring."""

    numerator: Poly
    denominator: Poly

    @staticmethod
    def const(variables, value) -> "Rat":
        variables = _validate_variables(variables)
        return Rat(Poly.constant(variables, value), Poly.one(variables)).normalized()

    @staticmethod
    def zero(variables) -> "Rat":
        return Rat.const(variables, 0)

    @staticmethod
    def one(variables) -> "Rat":
        return Rat.const(variables, 1)

    def _same_ring(self, other: "Rat") -> None:
        if self.numerator.variables != other.numerator.variables:
            raise ValueError("rational functions are in different variable rings")

    @property
    def variables(self) -> tuple[str, ...]:
        return self.numerator.variables

    def normalized(self) -> "Rat":
        if self.denominator.is_zero():
            raise ZeroDivisionError("rational-function denominator is zero")
        if self.numerator.is_zero():
            return Rat(Poly.zero(self.variables), Poly.one(self.variables))

        num = self.numerator
        den = self.denominator
        content = _common_content((num, den))
        if content not in (0, 1):
            num = num.scale(Fraction(1, 1) / content)
            den = den.scale(Fraction(1, 1) / content)

        if den.is_constant():
            c = den.constant_value()
            if c == 0:
                raise ZeroDivisionError("rational-function denominator is zero")
            num = num.scale(Fraction(1, 1) / c)
            den = Poly.one(num.variables)
        elif den.leading_coeff() < 0:
            num = -num
            den = -den
        return Rat(num, den)

    def is_zero(self) -> bool:
        return self.numerator.is_zero()

    def __neg__(self) -> "Rat":
        return Rat(-self.numerator, self.denominator).normalized()

    def __add__(self, other: "Rat") -> "Rat":
        self._same_ring(other)
        return Rat(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator,
        ).normalized()

    def __sub__(self, other: "Rat") -> "Rat":
        return self + (-other)

    def __mul__(self, other: "Rat") -> "Rat":
        self._same_ring(other)
        return Rat(self.numerator * other.numerator, self.denominator * other.denominator).normalized()

    def inverse(self) -> "Rat":
        if self.numerator.is_zero():
            raise ZeroDivisionError("division by zero rational function")
        return Rat(self.denominator, self.numerator).normalized()

    def __truediv__(self, other: "Rat") -> "Rat":
        return self * other.inverse()

    def pow(self, exponent: int) -> "Rat":
        exponent = int(exponent)
        if exponent == 0:
            return Rat.one(self.variables)
        if exponent < 0:
            return self.inverse().pow(-exponent)
        result = Rat.one(self.variables)
        base = self
        n = exponent
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1
        return result

    def record(self) -> dict:
        return {
            "variables": list(self.variables),
            "numerator": self.numerator.term_record(),
            "denominator": self.denominator.term_record(),
            "numerator_terms": str(len(self.numerator.terms)),
            "denominator_terms": str(len(self.denominator.terms)),
            "is_zero": self.is_zero(),
            "text": self.text(),
        }

    def text(self) -> str:
        if self.denominator.is_one():
            return self.numerator.text()
        num = self.numerator.text()
        if len(self.numerator.terms) > 1:
            num = f"({num})"
        return f"{num}/({self.denominator.text()})"


def _rat_variable(variables: tuple[str, ...], name: str) -> Rat:
    powers = [0] * len(variables)
    powers[variables.index(name)] = 1
    return Rat(Poly.from_terms(variables, ((tuple(powers), Fraction(1)),)), Poly.one(variables))


def _power_source(expression: str) -> str:
    return expression.replace("^", "**")


def _parse_native_ast(expression: str) -> ast.AST:
    try:
        return ast.parse(_power_source(expression), mode="eval").body
    except SyntaxError as exc:
        raise ValueError(f"could not parse symbolic expression: {exc}") from exc


def _reject_frontend_nodes(node: ast.AST) -> None:
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            raise ValueError("function calls are outside this exact rational-function arm")
        if isinstance(child, ast.Attribute):
            raise ValueError("attribute access is outside this exact rational-function arm")
        if isinstance(child, ast.Subscript):
            raise ValueError("subscript access is outside this exact rational-function arm")


def _unknown_names(node: ast.AST, variables: tuple[str, ...]) -> list[str]:
    allowed = set(variables)
    return sorted({child.id for child in ast.walk(node) if isinstance(child, ast.Name) and child.id not in allowed})


def _integer_exponent(node: ast.AST) -> int:
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return int(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _integer_exponent(node.operand)
        return -value if isinstance(node.op, ast.USub) else value
    raise ValueError("rational-function powers require integer literal exponents")


def _compile_rat_node(node: ast.AST, variables: tuple[str, ...]) -> Rat:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            raise ValueError("booleans are not exact rationals")
        if isinstance(node.value, int):
            return Rat.const(variables, node.value)
        raise ValueError("symbolic constants must be exact integers; use ratios such as 1/3")
    if isinstance(node, ast.Name):
        if node.id not in variables:
            raise ValueError(f"expression contains unknown symbols: {node.id}")
        return _rat_variable(variables, node.id)
    if isinstance(node, ast.UnaryOp):
        value = _compile_rat_node(node.operand, variables)
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return value
        raise ValueError(f"unsupported unary operator {type(node.op).__name__}")
    if isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Pow):
            return _compile_rat_node(node.left, variables).pow(_integer_exponent(node.right))
        left = _compile_rat_node(node.left, variables)
        right = _compile_rat_node(node.right, variables)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        raise ValueError(f"unsupported binary operator {type(node.op).__name__}")
    raise ValueError(f"unsupported symbolic expression node {type(node).__name__}")


def parse_rat(expression: str, variables) -> Rat:
    """Parse an exact rational function into Cella's sparse Q[variables] field."""
    expression = str(expression)
    _reject_decimal_literals(expression)
    variables = _validate_variables(variables)
    tree = _parse_native_ast(expression)
    _reject_frontend_nodes(tree)
    unknown = _unknown_names(tree, variables)
    if unknown:
        raise ValueError(f"expression contains unknown symbols: {', '.join(unknown)}")
    return _compile_rat_node(tree, variables).normalized()


def _poly_cross_difference(left: Rat, right: Rat) -> Poly:
    left._same_ring(right)
    return left.numerator * right.denominator - right.numerator * left.denominator


def symbolic_rational(expression: str, variables) -> dict:
    rat = parse_rat(expression, variables)
    return {
        "variables": list(rat.variables),
        "expression": rat.record(),
        "method": "native_ast_to_cella_sparse_Q_polynomial_field",
        "verdict_path": "Cella sparse terms; no floats; no transcendental simplification",
    }


def symbolic_equal(left: str, right: str, variables) -> dict:
    variables = _validate_variables(variables)
    left_rat = parse_rat(left, variables)
    right_rat = parse_rat(right, variables)
    cross = _poly_cross_difference(left_rat, right_rat)
    return {
        "variables": list(variables),
        "equal": cross.is_zero(),
        "left": left_rat.record(),
        "right": right_rat.record(),
        "cross_difference": cross.record(),
        "method": "exact_cross_multiplication_in_Q_variables",
    }


def symbolic_pole_law(
    kind: str,
    variables,
    *,
    m=None,
    B=None,
    A=None,
    transverse_P0=None,
    transverse_P1=None,
    exponents=None,
) -> dict:
    """Symbolic rational-function pole laws over Q[variables]."""
    variables = _validate_variables(variables)
    if kind == "master_quadric":
        base = master_quadric_pole_law(exponents, 1)
        B_rat = parse_rat("1" if B is None else str(B), variables)
        coeff = Rat.const(variables, base["C_p"]) / B_rat
        out = {
            "kind": "master_quadric",
            "order": base["order"],
            "C_p": base["C_p"],
            "coefficient": coeff.record(),
            "coefficient_text": coeff.text(),
            "law": "R = C(p)/B * x^-(p0+2)",
            "formula": base["formula"],
        }
    elif kind == "parity_fixed":
        m_int = int(_q(m))
        if _q(m).denominator != 1:
            raise ValueError("m must be an integer")
        if m_int < 1:
            raise ValueError("m must be at least 1")
        B_rat = parse_rat(str(B), variables)
        C = Fraction(-m_int * (m_int + 5))
        coeff = Rat.const(variables, C) / B_rat
        out = {
            "kind": "parity_fixed",
            "order": Fraction(4),
            "C_p": C,
            "coefficient": coeff.record(),
            "coefficient_text": coeff.text(),
            "law": "R = -m(m+5)/B * x^-4",
        }
    elif kind == "generic_quadratic":
        A_rat = parse_rat(str(A), variables)
        p0 = [parse_rat(str(v), variables) for v in transverse_P0]
        p1 = [parse_rat(str(v), variables) for v in transverse_P1]
        if len(p0) != len(p1) or not p0:
            raise ValueError("transverse_P0 and transverse_P1 must have the same nonzero length")
        drift = Rat.zero(variables)
        for a, b in zip(p0, p1):
            drift = drift + (b / a)
        coeff = drift / A_rat
        out = {
            "kind": "generic_quadratic",
            "order": Fraction(3),
            "drift": drift.record(),
            "coefficient": coeff.record(),
            "coefficient_text": coeff.text(),
            "law": "R = (1/A) * sum(P_a1/P_a0) * x^-3 + O(x^-2)",
        }
    else:
        raise ValueError(f"unknown symbolic pole-law kind {kind!r}")
    out["variables"] = list(variables)
    out["domain_assumptions"] = [
        "declared symbols range over an exact rational-function field",
        "display strings are secondary; sparse terms are the certificate payload",
    ]
    if B is not None:
        out["domain_assumptions"].append("B denominator/unit is nonzero on the local chart")
    if A is not None:
        out["domain_assumptions"].append("A denominator/unit is nonzero on the local chart")
    return out


def symbolic_gauge_carrier(variables, g, H) -> dict:
    """Compute O_ij over Q[variables] for a symbolic exact 2-jet."""
    variables = _validate_variables(variables)
    g_rat = [parse_rat(str(v), variables) for v in g]
    H_rat = [[parse_rat(str(v), variables) for v in row] for row in H]
    n = len(g_rat)
    if n == 0:
        raise ValueError("at least one gradient component is required")
    if len(H_rat) != n or any(len(row) != n for row in H_rat):
        raise ValueError("H must be an n by n matrix")

    two = Rat.const(variables, 2)
    zero = Rat.zero(variables)
    O: dict[tuple[int, int], Rat] = {}
    for i in range(n):
        for j in range(i + 1, n):
            O[(i, j)] = (
                H_rat[i][j]
                - (g_rat[i] * H_rat[j][j]) / (two * g_rat[j])
                - (g_rat[j] * H_rat[i][i]) / (two * g_rat[i])
            )

    normal = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(zero.record())
            else:
                row.append(O[(min(i, j), max(i, j))].record())
        normal.append(row)

    return {
        "variables": list(variables),
        "dimension": str(n),
        "pairs": [f"O{i + 1}{j + 1}" for i, j in O],
        "O": {f"O{i + 1}{j + 1}": value.record() for (i, j), value in O.items()},
        "normal_form": normal,
        "formula": "O_ij = H_ij - g_i*H_jj/(2*g_j) - g_j*H_ii/(2*g_i)",
        "domain_assumptions": [f"g{i + 1} != 0" for i in range(n)],
        "method": "exact_sparse_Q_symbolic_carrier",
    }


def symbolic_channel_sum(variables, channels: dict, expected_total=None) -> dict:
    """Sum symbolic channel expressions and optionally certify a target total."""
    variables = _validate_variables(variables)
    parsed = {str(label): parse_rat(str(expr), variables) for label, expr in channels.items()}
    total = Rat.zero(variables)
    for value in parsed.values():
        total = total + value
    out = {
        "variables": list(variables),
        "channels": {label: value.record() for label, value in parsed.items()},
        "sum": total.record(),
        "method": "exact_sparse_Q_channel_sum",
    }
    if expected_total is not None:
        expected = parse_rat(str(expected_total), variables)
        cross = _poly_cross_difference(total, expected)
        out["expected_total"] = expected.record()
        out["sum_equals_expected"] = cross.is_zero()
        out["cross_difference"] = cross.record()
    return out


def _term_from_json(item) -> tuple[str, str, tuple[Fraction, ...]]:
    if isinstance(item, dict):
        label = str(item.get("label", f"T{item}"))
        coefficient = str(item.get("coefficient", "1"))
        powers = item["powers"]
    else:
        label, coefficient, powers = item
        label = str(label)
        coefficient = str(coefficient)
    return label, coefficient, tuple(_z_or_q(p) for p in powers)


def symbolic_valuation(coordinates, terms, path: dict | None = None, parameters=None) -> dict:
    """Newton/support valuation for symbolic monomial terms.

    Coefficients live in Q[parameters]. Exponent vectors live on ``coordinates``.
    Nonzero symbolic coefficients are treated as chart units and reported as
    deletion walls, not silently assumed globally nonzero.
    """
    coordinates = _validate_variables(coordinates)
    parameters = _validate_variables(parameters or ())
    parsed_terms = []
    for raw in terms:
        label, coeff_expr, powers = _term_from_json(raw)
        if len(powers) != len(coordinates):
            raise ValueError("term exponent length does not match coordinates")
        coeff = parse_rat(coeff_expr, parameters)
        polar = any(p < 0 for p in powers)
        coeff_zero = coeff.is_zero()
        parsed_terms.append({
            "label": label,
            "coefficient": coeff,
            "powers": powers,
            "polar": polar,
            "coefficient_zero": coeff_zero,
            "active": polar and not coeff_zero,
        })

    out_terms = []
    deletion_walls = []
    domain_walls = []
    for item in parsed_terms:
        record = {
            "label": item["label"],
            "powers": item["powers"],
            "coefficient": item["coefficient"].record(),
            "coefficient_zero": item["coefficient_zero"],
            "polar": item["polar"],
            "active": item["active"],
        }
        if item["active"] and not item["coefficient"].numerator.is_constant():
            deletion_walls.append({
                "label": item["label"],
                "wall": f"{item['coefficient'].numerator.text()} = 0",
                "effect": "deletes this polar vertex from the leading support",
            })
        if item["active"] and not item["coefficient"].denominator.is_one():
            domain_walls.append({
                "label": item["label"],
                "wall": f"{item['coefficient'].denominator.text()} != 0",
                "effect": "keeps the rational coefficient chart defined",
            })
        out_terms.append(record)

    out = {
        "coordinates": list(coordinates),
        "parameters": list(parameters),
        "terms": out_terms,
        "active_terms": [item["label"] for item in parsed_terms if item["active"]],
        "deletion_walls": deletion_walls,
        "domain_walls": domain_walls,
        "method": "symbolic_newton_support_with_exact_unit_coefficients",
    }

    if path is not None:
        path_q = {str(k): _z_or_q(v) for k, v in path.items()}
        missing = set(coordinates) - set(path_q)
        if missing:
            raise ValueError(f"path is missing coordinate weights: {sorted(missing)}")
        support_orders = {}
        for item in parsed_terms:
            if not item["active"]:
                continue
            strength = -sum(power * path_q[name] for name, power in zip(coordinates, item["powers"]))
            support_orders[item["label"]] = strength
        support_order = max(support_orders.values()) if support_orders else None
        leading = [label for label, order in support_orders.items() if order == support_order]
        out["path"] = path_q
        out["support_orders"] = support_orders
        out["support_order"] = support_order
        out["leading_terms"] = leading
    return out
