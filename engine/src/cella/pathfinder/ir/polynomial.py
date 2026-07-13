"""Bounded sparse polynomial shadow used only for route discovery.

Generators arrive as strings from the wrapper.  This module expands them into
exact sparse form so scouts can inspect monic/triangular/degree structure.
The shadow is budget-bounded; exceeding the budget makes evidence unavailable
rather than producing an error verdict.  It is never a public algebra service.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .expression import (
    ExpressionNode,
    ExpressionShadowUnavailable,
    parse_expression,
)

Monomial = tuple[int, ...]
SparsePolynomial = dict[Monomial, Fraction]

DEFAULT_TERM_BUDGET = 4096


@dataclass(frozen=True, slots=True)
class PolynomialShadow:
    """Exact sparse view of one generator over the declared variables."""

    source: str
    variables: tuple[str, ...]
    terms: tuple[tuple[Monomial, Fraction], ...]

    def support(self) -> tuple[Monomial, ...]:
        return tuple(monomial for monomial, _ in self.terms)

    def variables_used(self) -> tuple[str, ...]:
        used = [
            self.variables[index]
            for index in range(len(self.variables))
            if any(monomial[index] for monomial, _ in self.terms)
        ]
        return tuple(used)

    def total_degree(self) -> int:
        if not self.terms:
            return 0
        return max(sum(monomial) for monomial, _ in self.terms)

    def weighted_degree(self, weights: tuple[int, ...]) -> int:
        if len(weights) != len(self.variables):
            raise ValueError("weight vector length must match the variable list")
        if not self.terms:
            return 0
        return max(
            sum(exponent * weight for exponent, weight in zip(monomial, weights))
            for monomial, _ in self.terms
        )

    def degree_in(self, variable: str) -> int:
        index = self.variables.index(variable)
        if not self.terms:
            return 0
        return max(monomial[index] for monomial, _ in self.terms)

    def _pure_leading_coefficient(self, variable: str) -> Fraction | None:
        """The leading coefficient in the variable when it is a pure constant."""

        index = self.variables.index(variable)
        degree = self.degree_in(variable)
        if degree == 0:
            return None
        leading = [
            (monomial, coefficient)
            for monomial, coefficient in self.terms
            if monomial[index] == degree
        ]
        if len(leading) != 1:
            return None
        monomial, coefficient = leading[0]
        pure = all(exponent == 0 for position, exponent in enumerate(monomial) if position != index)
        return coefficient if pure else None

    def is_monic_in(self, variable: str) -> bool:
        """True when the highest power of the variable has coefficient +-1 and
        involves no other variable (v1.3 §11.7 fresh-variable pattern; safe
        over any coefficient ring)."""

        coefficient = self._pure_leading_coefficient(variable)
        return coefficient in (Fraction(1), Fraction(-1))

    def has_unit_leading_in(self, variable: str) -> bool:
        """True when the leading coefficient in the variable is a pure nonzero
        constant — a unit over a coefficient field, but not over every ring."""

        coefficient = self._pure_leading_coefficient(variable)
        return coefficient is not None and coefficient != 0

    def is_linear(self) -> bool:
        return self.total_degree() <= 1

    def constant_term(self) -> Fraction:
        zero = tuple(0 for _ in self.variables)
        for monomial, coefficient in self.terms:
            if monomial == zero:
                return coefficient
        return Fraction(0)


def shadow_polynomial(
    source: str,
    variables: tuple[str, ...],
    *,
    term_budget: int = DEFAULT_TERM_BUDGET,
    max_nodes: int = 100_000,
) -> PolynomialShadow:
    """Expand a generator string into exact sparse form within the budget."""

    tree = parse_expression(source, max_nodes=max_nodes)
    index = {name: position for position, name in enumerate(variables)}
    poly = _expand(tree, index, len(variables), term_budget)
    terms = tuple(sorted(poly.items(), key=lambda item: item[0], reverse=True))
    return PolynomialShadow(source=str(source), variables=variables, terms=terms)


def _expand(
    node: ExpressionNode,
    index: dict[str, int],
    width: int,
    term_budget: int,
) -> SparsePolynomial:
    if node.kind == "const":
        assert node.constant is not None
        return {} if node.constant == 0 else {tuple(0 for _ in range(width)): node.constant}
    if node.kind == "var":
        position = index.get(str(node.name))
        if position is None:
            raise ExpressionShadowUnavailable(f"undeclared variable in generator: {node.name}")
        monomial = tuple(1 if slot == position else 0 for slot in range(width))
        return {monomial: Fraction(1)}
    if node.kind == "neg":
        return {m: -c for m, c in _expand(node.children[0], index, width, term_budget).items()}
    if node.kind == "add" or node.kind == "sub":
        left = _expand(node.children[0], index, width, term_budget)
        right = _expand(node.children[1], index, width, term_budget)
        sign = Fraction(1) if node.kind == "add" else Fraction(-1)
        out = dict(left)
        for monomial, coefficient in right.items():
            merged = out.get(monomial, Fraction(0)) + sign * coefficient
            if merged == 0:
                out.pop(monomial, None)
            else:
                out[monomial] = merged
        _check_budget(out, term_budget)
        return out
    if node.kind == "mul":
        left = _expand(node.children[0], index, width, term_budget)
        right = _expand(node.children[1], index, width, term_budget)
        return _multiply(left, right, term_budget)
    if node.kind == "div":
        left = _expand(node.children[0], index, width, term_budget)
        right = _expand(node.children[1], index, width, term_budget)
        divisor = _constant_of(right, width)
        if divisor is None or divisor == 0:
            raise ExpressionShadowUnavailable("nonconstant or zero divisor in generator shadow")
        return {m: c / divisor for m, c in left.items()}
    if node.kind == "pow":
        base = _expand(node.children[0], index, width, term_budget)
        exponent_poly = _expand(node.children[1], index, width, term_budget)
        exponent = _constant_of(exponent_poly, width)
        if exponent is None or exponent.denominator != 1 or exponent < 0:
            raise ExpressionShadowUnavailable("only non-negative integer powers are shadowable")
        result: SparsePolynomial = {tuple(0 for _ in range(width)): Fraction(1)}
        for _ in range(int(exponent)):
            result = _multiply(result, base, term_budget)
        return result
    raise ExpressionShadowUnavailable(f"generator contains an unshadowable node: {node.kind}")


def _multiply(left: SparsePolynomial, right: SparsePolynomial, term_budget: int) -> SparsePolynomial:
    out: SparsePolynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            merged = out.get(monomial, Fraction(0)) + left_coefficient * right_coefficient
            if merged == 0:
                out.pop(monomial, None)
            else:
                out[monomial] = merged
        _check_budget(out, term_budget)
    return out


def _check_budget(poly: SparsePolynomial, term_budget: int) -> None:
    if len(poly) > term_budget:
        raise ExpressionShadowUnavailable("polynomial shadow exceeds the analysis term budget")


def _constant_of(poly: SparsePolynomial, width: int) -> Fraction | None:
    zero = tuple(0 for _ in range(width))
    if not poly:
        return Fraction(0)
    if set(poly) == {zero}:
        return poly[zero]
    return None
