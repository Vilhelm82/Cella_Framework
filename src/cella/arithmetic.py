"""Arithmetic certification helpers for Cella MCP.

This module is intentionally a certification harness, not a replacement
arbitrary-precision library. Numerical routines are admissible only when paired
with exact branch/residue gates or independent route comparisons.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction

import mpmath as mp
import sympy as sp


def _sympify(expr):
    return sp.sympify(str(expr), locals={"sqrt": sp.sqrt, "pi": sp.pi, "I": sp.I})


def _mp(expr):
    return mp.mpf(str(sp.N(_sympify(expr), mp.mp.dps + 20)))


def _sym_text(expr) -> str:
    return str(sp.simplify(expr))


def _digits_from_diff(diff) -> int:
    diff = mp.mpf(diff)
    if diff == 0:
        return 999
    if diff >= 1:
        return 0
    return max(0, int(mp.floor(-mp.log10(diff))))


def _floor_log2(a: Fraction) -> int:
    e = a.numerator.bit_length() - a.denominator.bit_length() - 1

    def pow2(exp: int) -> Fraction:
        return Fraction(1 << exp) if exp >= 0 else Fraction(1, 1 << -exp)

    while pow2(e) > a:
        e -= 1
    while pow2(e + 1) <= a:
        e += 1
    return e


def _round_half_to_even(s: Fraction) -> int:
    floor_part = s.numerator // s.denominator
    remainder = s - floor_part
    if remainder < Fraction(1, 2):
        return floor_part
    if remainder > Fraction(1, 2):
        return floor_part + 1
    return floor_part if floor_part % 2 == 0 else floor_part + 1


def round_to_p_bits(value, p: int) -> Fraction:
    value = Fraction(value)
    if p <= 0:
        raise ValueError("required_bits must be positive")
    if value == 0:
        return Fraction(0)
    sign = 1 if value > 0 else -1
    a = value if value > 0 else -value
    e = _floor_log2(a)
    shift = e - (p - 1)
    scaled = a / (1 << shift) if shift >= 0 else a * (1 << -shift)
    n = _round_half_to_even(scaled)
    if shift >= 0:
        return Fraction(sign * n * (1 << shift))
    return Fraction(sign * n, 1 << -shift)


def arith_refine(required_bits: int, enclosures: list, ceiling: int | None = None) -> dict:
    """Resolve a sequence of rational enclosures by endpoint rounding agreement."""
    if required_bits <= 0:
        raise ValueError("required_bits must be positive")
    attempts = []
    for index, item in enumerate(enclosures, start=1):
        lo = Fraction(str(item["lo"]))
        hi = Fraction(str(item["hi"]))
        if lo > hi:
            raise ValueError("enclosure lower endpoint exceeds upper endpoint")
        working_bits = int(item.get("working_bits", 0))
        rounded_lo = round_to_p_bits(lo, required_bits)
        rounded_hi = round_to_p_bits(hi, required_bits)
        attempts.append({
            "iteration": index,
            "working_bits": working_bits,
            "rounded_lo": rounded_lo,
            "rounded_hi": rounded_hi,
            "resolved": rounded_lo == rounded_hi,
        })
        if rounded_lo == rounded_hi:
            return {
                "status": "refined_correctly_rounded",
                "value": rounded_lo,
                "working_bits": working_bits,
                "iterations": index,
                "attempts": attempts,
            }
        if ceiling is not None and working_bits >= int(ceiling):
            break
    return {
        "status": "refined_budget_exceeded",
        "value": None,
        "working_bits": attempts[-1]["working_bits"] if attempts else 0,
        "iterations": len(attempts),
        "attempts": attempts,
    }


def arith_precision_budget(
    output_bits: int,
    path_losses: list | None = None,
    format_bits: int = 53,
    atoms: list | None = None,
) -> dict:
    losses = [int(v) for v in (path_losses or [])]
    floor = int(output_bits) + sum(losses)
    atom_records = []
    overall = "proven"
    for atom in atoms or []:
        atom_format = int(atom.get("format_bits", format_bits))
        kind = str(atom.get("kind", "finite_exact_algebraic"))
        budget_bits = atom.get("budget_bits")
        if kind == "construct_to_tolerance":
            atom_floor = floor
            verdict = "proven" if budget_bits is not None and int(budget_bits) >= atom_floor else "eval"
        else:
            atom_floor = floor
            verdict = "proven" if atom_floor <= atom_format else "unmeetable"
        if verdict == "unmeetable":
            overall = "unmeetable"
        elif verdict == "eval" and overall != "unmeetable":
            overall = "eval"
        atom_records.append({
            "name": str(atom.get("name", "atom")),
            "kind": kind,
            "floor": atom_floor,
            "format_bits": atom_format,
            "budget_bits": None if budget_bits is None else int(budget_bits),
            "verdict": verdict,
        })
    if floor > int(format_bits):
        overall = "unmeetable"
    return {
        "output_bits": int(output_bits),
        "path_losses": losses,
        "composition_floor": floor,
        "format_bits": int(format_bits),
        "overall_verdict": overall,
        "atoms": atom_records,
    }


def elliptic_legendre_reduce(m, n) -> dict:
    m_s = sp.simplify(_sympify(m))
    n_s = sp.simplify(_sympify(n))
    singular = bool(sp.N(n_s) > 1)
    record = {
        "m": _sym_text(m_s),
        "n": _sym_text(n_s),
        "singular_third_kind": singular,
        "naive_ellippi_allowed": not singular,
    }
    if singular:
        q = sp.simplify(m_s / n_s)
        record.update({
            "regular_parameter_q": _sym_text(q),
            "identity": "PV Pi(n; m) = K(m) - Pi(q; m), q = m/n; use K(m) - Pi(q; m)",
            "reason": "n > 1 puts the pole on the real integration path; direct ellippi is not a certification route.",
        })
    else:
        record.update({
            "regular_parameter_q": _sym_text(n_s),
            "identity": "Pi(n; m) is regular for this declared branch.",
            "reason": "No real-path pole detected from n.",
        })
    return record


def residue_branch_gate(m, n, prefactor) -> dict:
    m_s = sp.simplify(_sympify(m))
    n_s = sp.simplify(_sympify(n))
    p_s = sp.simplify(_sympify(prefactor))
    x = sp.Symbol("x")
    x0_sq = sp.simplify(1 / n_s)
    y0_sq = sp.simplify((1 - x0_sq) * (1 - m_s * x0_sq))
    x0 = sp.sqrt(x0_sq)
    y0 = sp.sqrt(y0_sq)
    res_plus = sp.simplify(1 / (-2 * n_s * x0 * y0))
    res_minus = sp.simplify(1 / (-2 * n_s * (-x0) * y0))
    weighted = sp.simplify(p_s * res_plus)
    minpoly = sp.minimal_polynomial(weighted, x)
    weighted_is_four = bool(sp.expand(minpoly - (x - 4)) == 0)
    return {
        "m": _sym_text(m_s),
        "n": _sym_text(n_s),
        "x0_squared": _sym_text(x0_sq),
        "bare_residue_plus": _sym_text(res_plus),
        "bare_residue_minus": _sym_text(res_minus),
        "residue_antisymmetry": _sym_text(res_plus + res_minus),
        "weighted_residue": "4" if weighted_is_four else _sym_text(weighted),
        "weighted_residue_minpoly": str(minpoly),
        "one_sided_offset": "+/-4*pi*i" if weighted_is_four else f"+/-pi*i*({_sym_text(weighted)})",
        "two_sided_jump": "8*pi*i" if weighted_is_four else f"2*pi*i*({_sym_text(weighted)})",
    }


def third_kind_cpv(
    m,
    n,
    scale,
    weight_pi,
    weight_k,
    dps: int = 90,
    tolerance="1e-35",
    contour_height="0.25",
) -> dict:
    mp.mp.dps = int(dps)
    m_num = _mp(m)
    n_num = _mp(n)
    scale_num = _mp(scale)
    w_pi = _mp(weight_pi)
    w_k = _mp(weight_k)
    tol = mp.mpf(str(tolerance))
    K_num = mp.ellipk(m_num)
    if n_num > 1:
        q_num = m_num / n_num
        cpv_interchange = K_num - mp.ellippi(q_num, m_num)
        naive_used = False
    else:
        q_num = n_num
        cpv_interchange = mp.ellippi(n_num, m_num)
        naive_used = True

    x0_num = 1 / mp.sqrt(n_num)
    h = mp.mpf(str(contour_height))

    def bare_integrand(z):
        return 1 / ((1 - n_num * z ** 2) * mp.sqrt((1 - z ** 2) * (1 - m_num * z ** 2)))

    contour_value = mp.quad(bare_integrand, [0, x0_num - h * 1j, 1])
    cpv_contour = mp.re(contour_value)
    diff = abs(cpv_interchange - cpv_contour)
    constant = scale_num * (w_pi * cpv_interchange - w_k * K_num)
    weighted_imag_over_pi = scale_num * w_pi * (mp.im(contour_value) / mp.pi)
    return {
        "m": mp.nstr(m_num, 60),
        "n": mp.nstr(n_num, 60),
        "q": mp.nstr(q_num, 60),
        "naive_ellippi_used": naive_used,
        "routes_agree": bool(diff < tol),
        "route_difference": mp.nstr(diff, 80),
        "achieved_decimal_digits": _digits_from_diff(diff),
        "cpv_interchange": mp.nstr(cpv_interchange, 80),
        "cpv_contour_real": mp.nstr(cpv_contour, 80),
        "constant": mp.nstr(constant, 80),
        "branch_offset_weighted_over_pi": mp.nstr(weighted_imag_over_pi, 60),
        "branch_offset_weighted_over_pi_abs": mp.nstr(abs(weighted_imag_over_pi), 60),
        "scope": "CPV certified to the independent-route agreement floor.",
    }


def carlson_period_referee(m_primary, m_dual, dps: int = 90) -> dict:
    mp.mp.dps = int(dps)
    m_p = _mp(m_primary)
    m_d = _mp(m_dual)
    w1_true = 4 * mp.elliprf(0, 1 - 1j, 1 + 1j)
    w2_true = 4 * mp.elliprf(1j - 1, 0, 2j)
    omega1_claim = 2 ** (mp.mpf(7) / 4) * mp.ellipk(m_p)
    im_omega2_claim = -2 ** (mp.mpf(3) / 4) * mp.ellipk(m_d)
    d1 = abs(mp.re(w1_true) - omega1_claim)
    d2 = abs(mp.im(w2_true) - im_omega2_claim)
    d3 = abs(mp.re(w2_true) - mp.re(w1_true) / 2)
    return {
        "omega1_diff": mp.nstr(d1, 80),
        "im_omega2_diff": mp.nstr(d2, 80),
        "rhombic_diff": mp.nstr(d3, 80),
        "omega1_digits": _digits_from_diff(d1),
        "im_omega2_digits": _digits_from_diff(d2),
        "rhombic_digits": _digits_from_diff(d3),
        "all_gates_passed": d1 < mp.mpf(10) ** (-(int(dps) - 30))
        and d2 < mp.mpf(10) ** (-(int(dps) - 30))
        and d3 < mp.mpf(10) ** (-(int(dps) - 30)),
    }


def two_route_compare(route_a, route_b, requested_digits: int) -> dict:
    mp.mp.dps = max(80, int(requested_digits) + 30)
    a = mp.mpf(str(route_a))
    b = mp.mpf(str(route_b))
    diff = abs(a - b)
    digits = _digits_from_diff(diff)
    return {
        "route_a": mp.nstr(a, 80),
        "route_b": mp.nstr(b, 80),
        "difference": mp.nstr(diff, 80),
        "achieved_decimal_digits": digits,
        "requested_digits": int(requested_digits),
        "certified_to_requested": digits >= int(requested_digits),
        "scope": "Agreement certificate only; it does not prove the common value without route independence.",
    }


def _phi2(X, Y):
    return (
        X**3 + Y**3 - X**2 * Y**2
        + 1488 * X * Y * (X + Y)
        - 162000 * (X**2 + Y**2)
        + 40773375 * X * Y
        + 8748000000 * (X + Y)
        - 157464000000000
    )


def period_curve_invariants(lambda_value, partner_j=None) -> dict:
    lam = sp.simplify(_sympify(lambda_value))
    j = sp.simplify(256 * (1 - lam + lam**2) ** 3 / (lam**2 * (1 - lam) ** 2))
    record = {
        "lambda": _sym_text(lam),
        "lambda_product": _sym_text(lam * (1 - lam)),
        "lambda_dual": _sym_text(1 - lam),
        "j": _sym_text(j),
    }
    if partner_j is not None:
        partner = sp.simplify(_sympify(partner_j))
        phi = sp.simplify(_phi2(partner, j))
        record.update({
            "partner_j": _sym_text(partner),
            "phi2_partner": _sym_text(phi),
            "phi2_partner_zero": bool(phi == 0),
        })
    return record


def pslq_field_referee(value, basis: list, max_coeff: int = 10) -> dict:
    val = sp.simplify(_sympify(value))
    basis_s = [sp.simplify(_sympify(v)) for v in basis]
    bound = int(max_coeff)
    for coeffs in itertools.product(range(-bound, bound + 1), repeat=len(basis_s)):
        candidate = sp.simplify(sum(c * b for c, b in zip(coeffs, basis_s)))
        if sp.simplify(candidate - val) == 0:
            return {
                "relation_found": True,
                "coefficients": [str(sp.Integer(c)) for c in coeffs],
                "basis": [_sym_text(v) for v in basis_s],
                "value": _sym_text(val),
                "max_coeff": bound,
                "scope": "bounded-search",
            }
    return {
        "relation_found": False,
        "coefficients": None,
        "basis": [_sym_text(v) for v in basis_s],
        "value": _sym_text(val),
        "max_coeff": bound,
        "scope": "bounded-search",
        "warning": "No bounded relation found; this is not a proof of independence.",
    }


def arith_constant_pin(
    name: str,
    value: str,
    certified_digits: int,
    route_agreement_digits: int,
    branch_convention: str,
    exact_gates: list | None = None,
) -> dict:
    gates = [str(g) for g in (exact_gates or [])]
    status = "certified" if int(route_agreement_digits) >= int(certified_digits) else "insufficient_route_agreement"
    record = {
        "name": str(name),
        "value": str(value),
        "certified_digits": int(certified_digits),
        "route_agreement_digits": int(route_agreement_digits),
        "branch_convention": str(branch_convention),
        "exact_gates": gates,
        "status": status,
    }
    digest_payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    record["digest"] = hashlib.sha256(digest_payload).hexdigest()[:16]
    return record
