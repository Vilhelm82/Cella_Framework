"""Bounded native expression IR used only for route discovery.

This is an internal exact shadow: it exists so scouts and fingerprints can
inspect structure.  It is not a public mathematics service and never produces
a verdict about the host's deliverable.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from fractions import Fraction


class ExpressionShadowUnavailable(Exception):
    """The expression cannot be shadowed within the declared analysis budget."""


@dataclass(frozen=True, slots=True)
class ExpressionNode:
    """One canonical expression node; children are structural, not evaluated."""

    kind: str  # const | var | add | sub | mul | div | pow | neg | call
    constant: Fraction | None = None
    name: str | None = None
    children: tuple["ExpressionNode", ...] = ()

    def __post_init__(self) -> None:
        if self.kind == "const" and self.constant is None:
            raise ValueError("constant nodes require an exact rational value")
        if self.kind in {"var", "call"} and not (self.name or "").strip():
            raise ValueError("variable and call nodes require a name")


_BINARY_KINDS = {
    ast.Add: "add",
    ast.Sub: "sub",
    ast.Mult: "mul",
    ast.Div: "div",
    ast.Pow: "pow",
}


def parse_expression(expression: str, *, max_nodes: int = 100_000) -> ExpressionNode:
    """Parse a Python-syntax scalar expression into the canonical shadow."""

    try:
        tree = ast.parse(str(expression), mode="eval").body
    except SyntaxError as exc:
        raise ExpressionShadowUnavailable(f"unparseable expression: {exc}") from exc
    counter = {"nodes": 0}
    return _lower(tree, counter, max_nodes)


def _lower(node: ast.AST, counter: dict[str, int], max_nodes: int) -> ExpressionNode:
    counter["nodes"] += 1
    if counter["nodes"] > max_nodes:
        raise ExpressionShadowUnavailable("expression exceeds the analysis-node budget")
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ExpressionShadowUnavailable(f"unsupported constant: {node.value!r}")
        return ExpressionNode("const", constant=Fraction(str(node.value)))
    if isinstance(node, ast.Name):
        return ExpressionNode("var", name=node.id)
    if isinstance(node, ast.UnaryOp):
        child = _lower(node.operand, counter, max_nodes)
        if isinstance(node.op, ast.USub):
            return ExpressionNode("neg", children=(child,))
        if isinstance(node.op, ast.UAdd):
            return child
        raise ExpressionShadowUnavailable("unsupported unary operator")
    if isinstance(node, ast.BinOp):
        kind = _BINARY_KINDS.get(type(node.op))
        if kind is None:
            raise ExpressionShadowUnavailable("unsupported binary operator")
        return ExpressionNode(
            kind,
            children=(
                _lower(node.left, counter, max_nodes),
                _lower(node.right, counter, max_nodes),
            ),
        )
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return ExpressionNode(
            "call",
            name=node.func.id,
            children=tuple(_lower(arg, counter, max_nodes) for arg in node.args),
        )
    raise ExpressionShadowUnavailable(f"unsupported expression node: {type(node).__name__}")


def canonical_text(node: ExpressionNode) -> str:
    """Deterministic textual form used only for hashing and provenance."""

    if node.kind == "const":
        return str(node.constant)
    if node.kind == "var":
        return str(node.name)
    if node.kind == "neg":
        return f"(-{canonical_text(node.children[0])})"
    if node.kind == "call":
        return f"{node.name}({','.join(canonical_text(child) for child in node.children)})"
    symbol = {"add": "+", "sub": "-", "mul": "*", "div": "/", "pow": "^"}[node.kind]
    return "(" + symbol.join(canonical_text(child) for child in node.children) + ")"


def node_count(node: ExpressionNode) -> int:
    return 1 + sum(node_count(child) for child in node.children)


def expression_depth(node: ExpressionNode) -> int:
    if not node.children:
        return 1
    return 1 + max(expression_depth(child) for child in node.children)


def variables_used(node: ExpressionNode) -> tuple[str, ...]:
    names: set[str] = set()

    def visit(item: ExpressionNode) -> None:
        if item.kind == "var":
            names.add(str(item.name))
        for child in item.children:
            visit(child)

    visit(node)
    return tuple(sorted(names))


def subtraction_sites(node: ExpressionNode) -> tuple[tuple[str, ExpressionNode], ...]:
    """Every subtraction node with its canonical path (root.left.right...)."""

    sites: list[tuple[str, ExpressionNode]] = []

    def visit(item: ExpressionNode, path: str) -> None:
        if item.kind == "sub":
            sites.append((path, item))
        labels = _child_labels(item)
        for label, child in zip(labels, item.children):
            visit(child, f"{path}.{label}")

    visit(node, "root")
    return tuple(sites)


def _child_labels(node: ExpressionNode) -> tuple[str, ...]:
    if node.kind in {"add", "sub", "mul", "div", "pow"}:
        return ("left", "right")
    if node.kind == "neg":
        return ("arg",)
    if node.kind == "call":
        return tuple("arg" for _ in node.children)
    return ()


def structurally_equal(left: ExpressionNode, right: ExpressionNode) -> bool:
    return canonical_text(left) == canonical_text(right)
