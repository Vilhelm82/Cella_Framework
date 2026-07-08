#!/usr/bin/env python3
"""
Stage 3 certification script v2 — DBP dual third-kind period.

Changes vs the corrected draft (review of 2026-07-06):
  * G3 tautology rows REMOVED. Replaced by:
      G3a  symbolic signed residue gate: minimal_polynomial(P*Res_bare) == x - 4
           (carries the sign; no branch ambiguity; falls back to
           squared+sign+120-digit identity if minpoly is unavailable)
      G3b  curve-level residue antisymmetry: Res(-x0) == -Res(+x0), symbolic
      G3c  branch offsets recorded as DERIVED corollaries of G3a (not gates
           of the form X == X)
  * G9 is now a real control: true periods computed independently via
    Carlson elliprf and GATED against 2^(7/4)*K(k^2) and -2^(3/4)*K(k'^2),
    plus the rhombic pin Re(omega_2) == omega_1/2.
  * G5 states its honest scope: two-route certified only to the achieved
    G4 floor; single-route (regular interchange, dps-stable) beyond.

No naive ellippi(n>1, m) evaluation anywhere.
Dependencies: sympy, mpmath.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mpmath as mp
import sympy as sp


def exact_gate(report, name, actual, expected):
    actual_s = sp.simplify(actual)
    expected_s = sp.simplify(expected)
    diff_s = sp.simplify(actual_s - expected_s)
    passed = bool(diff_s == 0)
    report[name] = {
        "passed": passed,
        "actual_simplified": str(actual_s),
        "expected": str(expected_s),
        "difference_simplified": str(diff_s),
    }
    print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    return passed


def numeric_gate(report, name, actual_diff, tolerance, extra=None):
    passed = bool(actual_diff < tolerance)
    payload = {
        "passed": passed,
        "actual_diff": mp.nstr(actual_diff, 40),
        "tolerance": str(tolerance),
    }
    if extra:
        payload.update(extra)
    report[name] = payload
    print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    return passed


def phi_2(X, Y):
    return (X**3 + Y**3 - X**2 * Y**2
            + 1488 * X * Y * (X + Y)
            - 162000 * (X**2 + Y**2)
            + 40773375 * X * Y
            + 8748000000 * (X + Y)
            - 157464000000000)


def run(dps: int = 270, contour_height: str = "0.25",
        out_path: str = "stage3_report_v2.json"):
    report = {"stage_3a_exact": {}, "stage_3b_numerical": {}, "parameters": {}}

    print("==========================================================")
    print("  STAGE 3 v2: DBP DUAL THIRD-KIND PERIOD CERTIFICATION    ")
    print("==========================================================\n")

    s = sp.sqrt(2)
    n = (4 + 3 * s) / 8
    m = (2 + s) / 4
    P = -2 ** sp.Rational(7, 4) * (3 - 2 * s)

    x0_sq = sp.simplify(1 / n)
    y0_sq = sp.simplify((1 - x0_sq) * (1 - m * x0_sq))
    x0 = sp.sqrt(x0_sq)
    y0 = sp.sqrt(y0_sq)

    # Residues of the BARE differential dx/((1-n x^2) y) at x = +-x0:
    #   Res(x*) = 1 / ( d/dx[1 - n x^2]|_{x*} * y(x*) ) = 1 / (-2 n x* y0)
    res_plus = 1 / (-2 * n * x0 * y0)
    res_minus = 1 / (-2 * n * (-x0) * y0)
    weighted = P * res_plus

    res_bare_expected = -2 ** sp.Rational(1, 4) * (3 + 2 * s)

    print("--- [STAGE 3A] EXACT SYMBOLIC GATES ---")
    exact_gate(report["stage_3a_exact"], "G1_bare_residue_squared",
               sp.simplify(res_plus ** 2), sp.simplify(res_bare_expected ** 2))
    exact_gate(report["stage_3a_exact"], "G2_weighted_residue_squared",
               sp.simplify(weighted ** 2), 16)

    # G3a — SIGNED symbolic residue gate via minimal polynomial (no branch
    # ambiguity: minpoly of the actual radical expression, sign included).
    x_sym = sp.Symbol("x")
    try:
        mp_poly = sp.minimal_polynomial(weighted, x_sym)
        g3a_pass = bool(sp.expand(mp_poly - (x_sym - 4)) == 0)
        method = "minimal_polynomial"
        detail = str(mp_poly)
    except Exception as exc:  # fallback: squared gate + sign + high-prec identity
        sq_ok = bool(sp.simplify(weighted ** 2 - 16) == 0)
        num_ok = bool(abs(sp.N(weighted - 4, 120)) < sp.Float(10) ** -100)
        g3a_pass = sq_ok and num_ok
        method = f"fallback (minpoly failed: {exc})"
        detail = "squared identity + 120-digit numeric identity"
    report["stage_3a_exact"]["G3a_weighted_residue_equals_4_signed"] = {
        "passed": g3a_pass, "method": method, "detail": detail,
    }
    print(f"[{'PASS' if g3a_pass else 'FAIL'}] G3a_weighted_residue_equals_4_signed")

    # G3b — curve-level antisymmetry: residues at +-x0 cancel pairwise.
    exact_gate(report["stage_3a_exact"], "G3b_residue_antisymmetry",
               sp.simplify(res_plus + res_minus), 0)

    # G3c — branch offsets DERIVED from G3a (corollary record, not an X==X gate).
    report["stage_3a_exact"]["G3c_branch_offsets_derived"] = {
        "passed": g3a_pass,
        "one_sided_offset": "continuation - CPV = sign * i*pi * (P*Res_bare) = sign * 4*pi*i",
        "two_sided_jump": "between the two continuations: 2*pi*i * (P*Res_bare) = 8*pi*i",
        "derived_from": "G3a",
    }
    print(f"[{'PASS' if g3a_pass else 'FAIL'}] G3c_branch_offsets_derived")

    lam = (2 - s) / 4
    lam_dual = (2 + s) / 4
    j_lam = sp.simplify(256 * (1 - lam + lam ** 2) ** 3 / (lam ** 2 * (1 - lam) ** 2))
    exact_gate(report["stage_3a_exact"], "G6_lambda_product", lam * (1 - lam), sp.Rational(1, 8))
    exact_gate(report["stage_3a_exact"], "G6_lambda_dual_is_one_minus_lambda", lam_dual, 1 - lam)
    exact_gate(report["stage_3a_exact"], "G7_legendre_j", j_lam, sp.Integer(10976))
    exact_gate(report["stage_3a_exact"], "G8_phi2_isogeny", sp.Integer(phi_2(128, 10976)), sp.Integer(0))
    exact_gate(report["stage_3a_exact"], "G10_interchange_parameter_m_over_n", m / n, 2 * s - 2)
    exact_gate(report["stage_3a_exact"], "H1_x0_squared", x0_sq, 12 * s - 16)
    exact_gate(report["stage_3a_exact"], "H2_one_minus_x0_squared", 1 - x0_sq, (3 - 2 * s) ** 2)
    exact_gate(report["stage_3a_exact"], "H3_one_minus_m_x0_squared", 1 - m * x0_sq, 3 - 2 * s)
    exact_gate(report["stage_3a_exact"], "H4_n_times_unit", n * (3 - 2 * s), s / 8)

    report["parameters"] = {
        "n_dual": str(sp.simplify(n)),
        "m_dual_k_squared": str(sp.simplify(m)),
        "P_prefactor_on_Pi": str(sp.simplify(P)),
        "x0_squared": str(sp.simplify(x0_sq)),
        "res_bare_expected": str(sp.simplify(res_bare_expected)),
        "weighted_residue": "4 (signed, by G3a)",
        "lambda_primary": str(sp.simplify(lam)),
        "lambda_dual": str(sp.simplify(lam_dual)),
    }

    print(f"\n--- [STAGE 3B] HIGH-PRECISION NUMERICAL GATES (dps={dps}) ---")
    mp.mp.dps = dps

    s_num = mp.sqrt(2)
    m_num = (2 + s_num) / 4
    n_num = (4 + 3 * s_num) / 8
    q_num = 2 * s_num - 2
    K_num = mp.ellipk(m_num)

    cpv_pi_interchange = K_num - mp.ellippi(q_num, m_num)

    x0_num = 1 / mp.sqrt(n_num)
    h = mp.mpf(contour_height)

    def bare_integrand(z):
        return 1 / ((1 - n_num * z ** 2) * mp.sqrt((1 - z ** 2) * (1 - m_num * z ** 2)))

    contour_value_bare = mp.quad(bare_integrand, [0, x0_num - h * 1j, 1])
    cpv_pi_contour = mp.re(contour_value_bare)
    contour_imag_over_pi = mp.im(contour_value_bare) / mp.pi

    diff_cpv = abs(cpv_pi_interchange - cpv_pi_contour)
    numeric_gate(report["stage_3b_numerical"], "G4_two_route_CPV_Pi",
                 diff_cpv, mp.mpf("1e-130"),
                 {"cpv_pi_interchange": mp.nstr(cpv_pi_interchange, 180),
                  "cpv_pi_contour_real": mp.nstr(cpv_pi_contour, 180),
                  "contour_bare_imag_over_pi": mp.nstr(contour_imag_over_pi, 60),
                  "note": "independent routes; real part is CPV, imag records branch offset"})

    P_num = -(2 ** (mp.mpf(7) / 4)) * (3 - 2 * s_num)
    weighted_imag_over_pi = P_num * contour_imag_over_pi
    numeric_gate(report["stage_3b_numerical"], "G3_weighted_branch_offset_numeric",
                 abs(abs(weighted_imag_over_pi) - 4), mp.mpf("1e-120"),
                 {"weighted_imag_over_pi": mp.nstr(weighted_imag_over_pi, 60)})

    scale = -(2 ** (mp.mpf(7) / 4))
    dual_cpv = scale * ((3 - 2 * s_num) * cpv_pi_interchange - (2 - 2 * s_num) * K_num)
    certified_dual_cpv = mp.mpf(
        "-3.98800108597455809771976225753908737969412185555236029134797282037438204430"
        "1620084374998184536780571825905599613640469999524934769838194516297015969913"
        "667980232572633733216813738631005097537291913139724257892149600355947")
    g5_diff = abs(dual_cpv - certified_dual_cpv)
    numeric_gate(report["stage_3b_numerical"], "G5_certified_dual_CPV_pin",
                 g5_diff, mp.mpf("1e-170"),
                 {"dual_cpv": mp.nstr(dual_cpv, 220),
                  "pin_tail": "9694121855552360291",
                  "scope": ("two-route certified only to the G4 floor "
                            f"({mp.nstr(diff_cpv, 5)}); single-route (regular "
                            "interchange, dps-stable) beyond that")})

    # G9 — REAL period controls: true periods via Carlson RF, gated.
    w1_true_c = 4 * mp.elliprf(0, 1 - 1j, 1 + 1j)
    w2_true = 4 * mp.elliprf(1j - 1, 0, 2j)
    k_primary_sq = (2 - s_num) / 4
    omega1_claim = 2 ** (mp.mpf(7) / 4) * mp.ellipk(k_primary_sq)
    im_omega2_claim = -2 ** (mp.mpf(3) / 4) * K_num
    tol9 = mp.mpf(10) ** (-(dps - 40))
    numeric_gate(report["stage_3b_numerical"], "G9a_omega1_vs_2_74_Kprimary",
                 abs(w1_true_c.real - omega1_claim), tol9,
                 {"omega1_true": mp.nstr(w1_true_c.real, 60),
                  "omega1_imag_leak": mp.nstr(abs(w1_true_c.imag), 5)})
    numeric_gate(report["stage_3b_numerical"], "G9b_Im_omega2_vs_minus_2_34_Kdual",
                 abs(w2_true.imag - im_omega2_claim), tol9,
                 {"Im_omega2_true": mp.nstr(w2_true.imag, 60)})
    numeric_gate(report["stage_3b_numerical"], "G9c_rhombic_Re_omega2_is_half_omega1",
                 abs(w2_true.real - w1_true_c.real / 2), tol9,
                 {"Re_omega2_true": mp.nstr(w2_true.real, 60)})

    all_exact = all(v.get("passed") for v in report["stage_3a_exact"].values())
    all_num = all(v.get("passed") for v in report["stage_3b_numerical"].values())
    report["overall"] = {
        "passed": bool(all_exact and all_num),
        "exact_gates_passed": bool(all_exact),
        "numerical_gates_passed": bool(all_num),
        "note": ("v2: no tautology rows, no hardcoded PASS, no naive "
                 "ellippi(n>1,m) anywhere; period controls are real gates."),
    }
    print(f"\nOVERALL: {'PASS' if report['overall']['passed'] else 'FAIL'}")

    Path(out_path).write_text(json.dumps(report, indent=4), encoding="utf-8")
    print(f"Report saved to {out_path}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dps", type=int, default=270)
    parser.add_argument("--contour-height", default="0.25")
    parser.add_argument("--out", default="stage3_report_v2.json")
    args = parser.parse_args()
    run(dps=args.dps, contour_height=args.contour_height, out_path=args.out)
