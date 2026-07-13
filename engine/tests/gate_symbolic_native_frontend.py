"""Gate native symbolic front-end.

This gate pins the replacement for the temporary SymPy parser bridge:
symbolic expressions are parsed with Cella's own restricted AST compiler and
compiled directly to Poly/Rat.

Run:  python tests/gate_symbolic_native_frontend.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


try:
    import cella.symbolic as symbolic
except Exception as exc:
    print(f"GATE SYMBOLIC NATIVE FRONTEND: OPEN - import failed: {exc}")
    sys.exit(1)


check("N1 importing cella.symbolic does not import sympy", "sympy" not in sys.modules)

rat = symbolic.parse_rat("(-14)/(S*(16*pi*S + 1)**2)", ["S", "Q", "pi"])
round_trip = symbolic.parse_rat(rat.text(), ["S", "Q", "pi"])
cross = symbolic._poly_cross_difference(rat, round_trip)
check(
    "N2 native front-end compiles exact rational expression and round-trips Cella caret text",
    rat.denominator.terms
    == (
        ((1, 0, 0), symbolic.Fraction(1)),
        ((2, 0, 1), symbolic.Fraction(32)),
        ((3, 0, 2), symbolic.Fraction(256)),
    )
    and cross.is_zero(),
)
check("N2b parsing symbolic rational expressions does not import sympy", "sympy" not in sys.modules)

negative_power = symbolic.parse_rat("(1 + x)^-2", ["x"])
same_negative_power = symbolic.parse_rat("1/(1 + x)**2", ["x"])
check(
    "N3 native front-end accepts integer negative powers as rational functions",
    symbolic._poly_cross_difference(negative_power, same_negative_power).is_zero(),
)

try:
    symbolic.parse_rat("B + 0.1", ["B"])
    decimal_rejected = False
except ValueError as exc:
    decimal_rejected = "decimal literal" in str(exc)
check("N4 native front-end rejects decimal literals structurally", decimal_rejected)

try:
    symbolic.parse_rat("sqrt(B)", ["B"])
    function_rejected = False
except ValueError as exc:
    function_rejected = "function calls" in str(exc)
check("N5 native front-end rejects function calls structurally", function_rejected)

try:
    symbolic.parse_rat("B + C", ["B"])
    unknown_rejected = False
except ValueError as exc:
    unknown_rejected = "unknown symbols: C" in str(exc)
check("N6 native front-end reports undeclared symbols without error-string scraping", unknown_rejected)

try:
    symbolic.parse_rat("B**C", ["B", "C"])
    symbolic_exponent_rejected = False
except ValueError as exc:
    symbolic_exponent_rejected = "integer literal exponents" in str(exc)
check("N7 native front-end rejects symbolic powers before term construction", symbolic_exponent_rejected)

print()
if FAILS:
    print(f"GATE SYMBOLIC NATIVE FRONTEND: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE SYMBOLIC NATIVE FRONTEND: CLOSED - symbolic parser is native.")
sys.exit(0)
