"""Release gate for the separate native Legendre K/E enclosure module."""

from __future__ import annotations

import ast
from fractions import Fraction
from pathlib import Path

from cella.native_periods import (LegendreKEResult, PeriodRefusal,
    legendre_e_enclose, legendre_k_enclose, legendre_ke_enclose,
    legendre_pinning_register)
from cella.periods import legendre_ke_numerical_realization
from cella.qsqrt import QSqrt
from cella.typed_elementary import pi_eval, round_to_p_bits


passed = 0
def check(label, condition):
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


def interval(result):
    b = result.dyadic_bracket
    return (Fraction(b.lower_numerator, 1 << b.denominator_exponent),
            Fraction(b.upper_numerator, 1 << b.denominator_exponent))


def pin_interval(record, key):
    return Fraction(record[key]["lo"]), Fraction(record[key]["hi"])


# Rational parameters and correct endpoint behavior.
for m in (Fraction(0), Fraction(1, 3), Fraction(1, 2), Fraction(3, 4)):
    for atom, evaluator in (("K", legendre_k_enclose), ("E", legendre_e_enclose)):
        result = evaluator(m, 48)
        check("rational parameter accepted", isinstance(result, LegendreKEResult))
        check("requested width met", result.dyadic_bracket.width_bits >= 48)
        check("pinning register closed", result.pinning_register["contains"] is True)
        check("exact recurrence recorded", result.series_ledger["coefficient_recurrences"][0].startswith("C_0=1"))
        check("no external dependency recorded", result.certificate_record["external_numerical_dependencies"] == [])

k0 = legendre_k_enclose(Fraction(0), 80)
e0 = legendre_e_enclose(Fraction(0), 80)
pi = pi_eval(160)
w0 = (pi.lo/2, pi.hi/2)
for result in (k0, e0):
    lo, hi = interval(result)
    check("m=0 encloses pi/2", lo <= w0[0] <= w0[1] <= hi)
    check("m=0 uses endpoint pinning register", result.pinning_register["mode"] == "m=0_endpoint_limit")

# Both exact DBP complementary parameters in Q(sqrt(2)).
m_plus = QSqrt(Fraction(1, 2), Fraction(-1, 4), Fraction(2))
m_minus = QSqrt(Fraction(1, 2), Fraction(1, 4), Fraction(2))
dbp = {}
for label, m in (("plus", m_plus), ("minus", m_minus)):
    for atom, evaluator in (("K", legendre_k_enclose), ("E", legendre_e_enclose)):
        result = evaluator(m, 96)
        dbp[(label, atom)] = result
        check("DBP quadratic parameter accepted", isinstance(result, LegendreKEResult))
        check("DBP partial remains exact QSqrt", result.series_ledger["exact_partial_sum"]["type"] == "QSqrt")
        check("DBP pinning closes", result.pinning_register["contains"] is True)
        check("complement transported exactly", result.pinning_register["complement"] == (
            {"type": "QSqrt", "a": "1/2", "b": "1/4" if label == "plus" else "-1/4", "r": "2"}))

# Precision nesting and correct rounding by independent higher enclosure.
for atom, evaluator in (("K", legendre_k_enclose), ("E", legendre_e_enclose)):
    low = evaluator(Fraction(1, 3), 40)
    high = evaluator(Fraction(1, 3), 96)
    llo, lhi = interval(low); hlo, hhi = interval(high)
    check("precision brackets nest", llo <= hlo <= hhi <= lhi)
    check("higher endpoints round identically", round_to_p_bits(hlo, 40) == round_to_p_bits(hhi, 40))
    check("correct rounded value returned", Fraction(low.rounded_value) == round_to_p_bits(hlo, 40))

# Structural owner adapter delegates without changing the atom record owner.
adapted = legendre_ke_numerical_realization("K", Fraction(1, 3), 40)
direct = legendre_ke_enclose("K", Fraction(1, 3), 40)
check("periods adapter registers numerical realization", adapted.certificate_digest == direct.certificate_digest)

# Pinning interval contains the separately generated native pi/2 interval.
pin = legendre_pinning_register(Fraction(1, 3), 80)
left_lo, left_hi = pin_interval(pin, "left")
right_lo, right_hi = pin_interval(pin, "right_pi_over_2")
check("pinning left contains native pi/2", left_lo <= right_lo <= right_hi <= left_hi)
check("coefficient mutant bites", legendre_pinning_register(Fraction(1, 3), 80, _mutation="coefficient")["contains"] is False)
check("complement mutant bites", legendre_pinning_register(Fraction(1, 3), 80, _mutation="complement")["contains"] is False)

# Typed real-stratum and request refusals.
for m in (Fraction(-1, 10), Fraction(1), Fraction(11, 10)):
    refusal = legendre_k_enclose(m, 40)
    check("domain refusal", isinstance(refusal, PeriodRefusal) and refusal.token == "domain_separation_failed")
check("float parameter refuses", isinstance(legendre_k_enclose(0.5, 40), PeriodRefusal))
check("integer parameter refuses", isinstance(legendre_k_enclose(0, 40), PeriodRefusal))
check("invalid precision refuses", isinstance(legendre_k_enclose(Fraction(1, 2), 0), PeriodRefusal))
check("unsupported atom refuses", legendre_ke_enclose("Pi", Fraction(1, 2), 40).token == "unsupported_differential")

# Static production dependency audit: imports and call sites only.
source = Path("src/cella/native_periods/legendre_ke.py").read_text()
tree = ast.parse(source)
forbidden = ("mpmath", "sympy", "scipy", "flint", "arb", "sage", "agm", "carlson", "ellip")
hits = []
for node in ast.walk(tree):
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        text = ast.unparse(node).lower()
        if any(name in text for name in forbidden): hits.append((node.lineno, text))
    if isinstance(node, ast.Call):
        text = ast.unparse(node.func).lower()
        if any(name in text for name in forbidden): hits.append((node.lineno, text))
check("no external numerical dependencies", not hits)

print(f"Native Legendre K/E enclosure: {passed} assertions passed")
