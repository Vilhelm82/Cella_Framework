"""Certified native Legendre K/E enclosures on the real stratum 0 <= m < 1.

This module is deliberately separate from the fixed DBP relative-period
evaluator.  It realizes only the first- and second-kind Legendre atoms and the
complementary pinning register; Pi, descent, and field normalization are out of
scope.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction

from cella.qsqrt import QSqrt
from cella.typed_elementary import pi_eval, round_to_p_bits

from .certificate import canon, digest
from .exact_scalar import (Interval, dyadic_ceil, dyadic_floor, fraction_text,
                           sqrt_interval)
from .records import DyadicBracket, PeriodRefusal
from .terminal import materialize


@dataclass(frozen=True, slots=True)
class LegendreKEResult:
    atom: str
    parameter: dict
    required_bits: int
    dyadic_bracket: DyadicBracket
    rounded_value: str
    series_ledger: dict
    pinning_register: dict
    certificate_digest: str
    certificate_record: dict | None

    def to_record(self):
        return asdict(self)


def _sign(x: Fraction | QSqrt) -> int:
    """Exact sign in one declared real quadratic field."""
    if isinstance(x, Fraction):
        return (x > 0) - (x < 0)
    a, b, r = x.a, x.b, x.r
    if b == 0:
        return (a > 0) - (a < 0)
    if b > 0:
        if a >= 0:
            return 1
        return 1 if b*b*r > a*a else -1
    if a <= 0:
        return -1
    return 1 if a*a > b*b*r else -1


def _parameter(value):
    if isinstance(value, Fraction):
        return value
    if isinstance(value, QSqrt):
        return value
    raise TypeError("Legendre m must be Fraction or QSqrt")


def _field_record(value: Fraction | QSqrt) -> dict:
    if isinstance(value, Fraction):
        return {"type": "Q", "value": fraction_text(value)}
    return {
        "type": "QSqrt", "a": fraction_text(value.a),
        "b": fraction_text(value.b), "r": fraction_text(value.r),
    }


def _field_interval(value: Fraction | QSqrt, bits: int) -> Interval:
    """The only field-to-rational conversion used by the value path."""
    if isinstance(value, Fraction):
        return Interval.point(value)
    root = sqrt_interval(Interval.point(value.r), bits)
    if value.b >= 0:
        return Interval(value.a + value.b*root.lo, value.a + value.b*root.hi)
    return Interval(value.a + value.b*root.hi, value.a + value.b*root.lo)


def _domain(m: Fraction | QSqrt) -> bool:
    return _sign(m) >= 0 and _sign(1-m) > 0


def _tail_order(m: Fraction | QSqrt, proof_bits: int) -> tuple[int, Fraction]:
    if _sign(m) == 0:
        return 0, Fraction(0)
    m_hi = _field_interval(m, proof_bits + 24).hi
    if not 0 < m_hi < 1:
        raise ArithmeticError("failed to separate m from 1 in the real embedding")
    target = Fraction(1, 1 << (proof_bits + 16))
    power = m_hi
    order = 0
    tail = power / (1-m_hi)
    while tail > target:
        power *= m_hi
        order += 1
        tail = power / (1-m_hi)
        if order > 250_000:
            raise ArithmeticError("series term budget exhausted near m=1")
    return order, tail


def _normalized_pair(m: Fraction | QSqrt, order: int, mutation: str | None = None):
    """Exact partial sums for K/W0 and E/W0 in the parameter field."""
    one = m*0 + 1
    k_sum = one
    e_sum = one
    power = one
    c = Fraction(1)
    b = Fraction(1)
    for index in range(1, order + 1):
        c *= Fraction(2*index-1, 2*index)
        b *= Fraction(2*index-3, 2*index)
        power *= m
        k_coeff = c*c
        e_coeff = b*c
        if mutation == "coefficient" and index == 1:
            e_coeff += Fraction(1, 16)
        k_sum += k_coeff*power
        e_sum += e_coeff*power
    return k_sum, e_sum


def _terminal_pair(m: Fraction | QSqrt, proof_bits: int, mutation: str | None = None):
    order, tail = _tail_order(m, proof_bits)
    k_partial, e_partial = _normalized_pair(m, order, mutation=mutation)
    k_read = _field_interval(k_partial, proof_bits + 32)
    e_read = _field_interval(e_partial, proof_bits + 32)
    # K has a positive tail; all E coefficients after the constant are
    # negative on 0 <= m < 1.
    k_norm = Interval(k_read.lo, k_read.hi + tail)
    e_norm = Interval(e_read.lo - tail, e_read.hi)
    w0_raw = pi_eval(proof_bits + 48)
    w0 = Interval(w0_raw.lo/2, w0_raw.hi/2)
    return {
        "K": k_norm*w0,
        "E": e_norm*w0,
        "K_normalized": k_norm,
        "E_normalized": e_norm,
        "order": order,
        "tail_bound": tail,
        "K_partial": k_partial,
        "E_partial": e_partial,
        "w0": w0,
    }


def _pinning_register(m: Fraction | QSqrt, proof_bits: int, mutation: str | None = None) -> dict:
    right_raw = pi_eval(proof_bits + 88)
    right = Interval(right_raw.lo/2, right_raw.hi/2)
    if _sign(m) == 0:
        # Endpoint limit: (E-K)K~ vanishes, E~=E(1)=1, K(0)=W0.
        left_raw = pi_eval(proof_bits + 64)
        left = Interval(left_raw.lo/2, left_raw.hi/2)
        closed = left.lo <= right.lo and left.hi >= right.hi
        return {
            "identity": "E(m)*K(1-m)+E(1-m)*K(m)-K(m)*K(1-m)=pi/2",
            "mode": "m=0_endpoint_limit", "left": _interval_record(left, proof_bits + 32),
            "right_pi_over_2": _interval_record(right, proof_bits + 32), "contains": closed,
            "endpoint_obligations": ["E(1)=1", "K(0)=W0", "(E-K)*K_complement tends to 0"],
        }
    complement = m if mutation == "complement" else 1-m
    direct = _terminal_pair(m, proof_bits, mutation="coefficient" if mutation == "coefficient" else None)
    dual = _terminal_pair(complement, proof_bits)
    left = direct["E"]*dual["K"] + dual["E"]*direct["K"] - direct["K"]*dual["K"]
    closed = left.lo <= right.lo and left.hi >= right.hi
    return {
        "identity": "E(m)*K(1-m)+E(1-m)*K(m)-K(m)*K(1-m)=pi/2",
        "mode": "complementary_series", "complement": _field_record(complement),
        "left": _interval_record(left, proof_bits + 32),
        "right_pi_over_2": _interval_record(right, proof_bits + 32),
        "contains": closed, "direct_order": direct["order"], "complement_order": dual["order"],
    }


def legendre_pinning_register(m, required_bits: int, *, _mutation: str | None = None):
    try:
        m = _parameter(m)
    except TypeError as exc:
        return PeriodRefusal("route_identity_failed", "legendre_parameter", str(exc), "Fraction or QSqrt parameter")
    if isinstance(required_bits, bool) or not isinstance(required_bits, int) or required_bits <= 0:
        return PeriodRefusal("precision_budget_exhausted", "legendre_precision", "required_bits must be positive", "positive precision")
    if not _domain(m):
        return PeriodRefusal("domain_separation_failed", "legendre_domain", "certified stratum is 0 <= m < 1", "real Legendre stratum")
    try:
        return _pinning_register(m, required_bits + 24, mutation=_mutation)
    except ArithmeticError as exc:
        return PeriodRefusal("precision_budget_exhausted", "legendre_series", str(exc), "series tail budget")


def cella_arith_refine(required_bits: int, enclosures: list[dict]) -> dict:
    """Pure exact endpoint-refinement contract used by cella_arith_refine."""
    attempts = []
    for item in enclosures:
        lo, hi = Fraction(item["lo"]), Fraction(item["hi"])
        rounded_lo = round_to_p_bits(lo, required_bits)
        rounded_hi = round_to_p_bits(hi, required_bits)
        attempts.append({
            "working_bits": item["working_bits"],
            "rounded_lo": fraction_text(rounded_lo),
            "rounded_hi": fraction_text(rounded_hi),
            "resolved": rounded_lo == rounded_hi,
        })
        if rounded_lo == rounded_hi:
            return {"status": "refined_correctly_rounded", "value": rounded_lo, "attempts": attempts}
    return {"status": "refined_budget_exceeded", "value": None, "attempts": attempts}


def legendre_ke_enclose(atom: str, m, required_bits: int, certificate: bool = True):
    atom = str(atom).upper()
    if atom not in {"K", "E"}:
        return PeriodRefusal("unsupported_differential", "legendre_atom", "atom must be K or E", "first- or second-kind atom")
    try:
        m = _parameter(m)
    except TypeError as exc:
        return PeriodRefusal("route_identity_failed", "legendre_parameter", str(exc), "Fraction or QSqrt parameter")
    if isinstance(required_bits, bool) or not isinstance(required_bits, int) or required_bits <= 0:
        return PeriodRefusal("precision_budget_exhausted", "legendre_precision", "required_bits must be positive", "positive precision")
    if not isinstance(certificate, bool):
        return PeriodRefusal("route_identity_failed", "legendre_request", "certificate must be boolean", "request contract")
    if not _domain(m):
        return PeriodRefusal("domain_separation_failed", "legendre_domain", "certified stratum is 0 <= m < 1", "real Legendre stratum")

    attempts = []
    work = required_bits + 24
    pair = None
    pinning = None
    refine = None
    for _ in range(6):
        try:
            pair = _terminal_pair(m, work)
            pinning = _pinning_register(m, work)
        except ArithmeticError as exc:
            return PeriodRefusal("precision_budget_exhausted", "legendre_series", str(exc), "series tail budget")
        value = pair[atom]
        attempts.append({"working_bits": work, "lo": value.lo, "hi": value.hi})
        refine = cella_arith_refine(required_bits, attempts)
        if refine["status"] == "refined_correctly_rounded" and pinning["contains"]:
            break
        work *= 2
    else:
        token = "account_not_closed" if pinning is not None and not pinning["contains"] else "precision_budget_exhausted"
        return PeriodRefusal(token, "legendre_refine", "rounding or pinning did not close", "correct rounding and complementary pinning")

    value = pair[atom]
    bracket = materialize(value, required_bits)
    series = {
        "coefficient_recurrences": [
            "C_0=1; C_k=C_(k-1)*(2k-1)/(2k)",
            "B_0=1; B_k=B_(k-1)*(2k-3)/(2k)",
        ],
        "normalized_series": {
            "K": "sum C_k^2*m^k", "E": "sum B_k*C_k*m^k",
        },
        "order": pair["order"],
        "tail_bound": fraction_text(dyadic_ceil(pair["tail_bound"], work + 32)),
        "tail_sign": "positive" if atom == "K" else "negative_one_sided",
        "exact_partial_sum": _exact_field_record(pair[f"{atom}_partial"]),
        "terminal_field_conversion_bits": work + 32,
        "refinement_method": "cella_arith_refine",
        "refinement": canon(refine),
    }
    record = {
        "schema_id": "cella.native_periods.legendre_ke.certificate",
        "schema_version": "1.0", "atom": atom, "parameter": _field_record(m),
        "required_bits": required_bits, "stratum": "0<=m<1",
        "series_ledger": series, "w0_source": {
            "atom": "pi/2", "implementation": "cella.typed_elementary.pi_eval",
            "method": "native_machin_arctan_rational_enclosure",
        },
        "pinning_register": pinning, "dyadic_bracket": bracket.to_record(),
        "external_numerical_dependencies": [],
    }
    certificate_digest = digest(record)
    canonical_record = {**canon(record), "certificate_digest": certificate_digest}
    return LegendreKEResult(
        atom, _field_record(m), required_bits, bracket,
        fraction_text(refine["value"]), series, pinning,
        certificate_digest, canonical_record if certificate else None,
    )


def legendre_k_enclose(m, required_bits: int, certificate: bool = True):
    return legendre_ke_enclose("K", m, required_bits, certificate)


def legendre_e_enclose(m, required_bits: int, certificate: bool = True):
    return legendre_ke_enclose("E", m, required_bits, certificate)


def _interval_record(value: Interval, bits: int) -> dict:
    return {
        "lo": fraction_text(dyadic_floor(value.lo, bits)),
        "hi": fraction_text(dyadic_ceil(value.hi, bits)),
    }


def _rational_hex(value: Fraction) -> dict:
    return {
        "numerator_hex": ("-" if value.numerator < 0 else "") + format(abs(value.numerator), "x"),
        "denominator_hex": format(value.denominator, "x"),
    }


def _exact_field_record(value: Fraction | QSqrt) -> dict:
    """Unbounded exact encoding that avoids decimal digit conversion limits."""
    if isinstance(value, Fraction):
        return {"type": "Q", "encoding": "hex_rational", "value": _rational_hex(value)}
    return {
        "type": "QSqrt", "encoding": "hex_rational_components",
        "a": _rational_hex(value.a), "b": _rational_hex(value.b),
        "r": _rational_hex(value.r),
    }
