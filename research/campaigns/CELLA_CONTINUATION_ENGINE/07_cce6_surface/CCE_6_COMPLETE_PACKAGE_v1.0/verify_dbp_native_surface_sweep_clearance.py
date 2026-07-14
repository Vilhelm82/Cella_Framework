#!/usr/bin/env python3
"""Independent exact replay for the CCE-6 native surface-clearance theorem.

The verifier uses only the Python standard library.  It checks source and
nested-certificate bindings, replays the polynomial identities in
Q[rho,sigma,V,T,Xi,H]/(rho^2-1-sigma^2), and recomputes every rational
lower-bound transfer appearing in the certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, Mapping, Tuple


Monomial = Tuple[int, int, int, int, int, int]
Polynomial = Dict[Monomial, Fraction]
ZERO_MONOMIAL: Monomial = (0, 0, 0, 0, 0, 0)


def clean(poly: Mapping[Monomial, Fraction]) -> Polynomial:
    return {m: c for m, c in poly.items() if c}


def const(value: int | Fraction) -> Polynomial:
    value = Fraction(value)
    return {} if not value else {ZERO_MONOMIAL: value}


def variable(index: int) -> Polynomial:
    exponent = [0] * 6
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def add(left: Mapping[Monomial, Fraction], right: Mapping[Monomial, Fraction]) -> Polynomial:
    out: Polynomial = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Fraction(0)) + coefficient
    return clean(out)


def neg(poly: Mapping[Monomial, Fraction]) -> Polynomial:
    return {m: -c for m, c in poly.items()}


def sub(left: Mapping[Monomial, Fraction], right: Mapping[Monomial, Fraction]) -> Polynomial:
    return add(left, neg(right))


def mul(left: Mapping[Monomial, Fraction], right: Mapping[Monomial, Fraction]) -> Polynomial:
    out: Polynomial = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(a + b for a, b in zip(lm, rm))
            out[monomial] = out.get(monomial, Fraction(0)) + lc * rc
    return clean(out)


def power(poly: Mapping[Monomial, Fraction], exponent: int) -> Polynomial:
    if exponent < 0:
        raise ValueError("negative polynomial exponent")
    out = const(1)
    base = dict(poly)
    while exponent:
        if exponent & 1:
            out = mul(out, base)
        base = mul(base, base)
        exponent >>= 1
    return out


def scale(poly: Mapping[Monomial, Fraction], scalar: int | Fraction) -> Polynomial:
    scalar = Fraction(scalar)
    return clean({m: scalar * c for m, c in poly.items()})


def reduce_cover(poly: Mapping[Monomial, Fraction]) -> Polynomial:
    """Reduce rho^2 to 1+sigma^2 until rho degree is at most one."""

    pending = list(poly.items())
    out: Polynomial = {}
    while pending:
        monomial, coefficient = pending.pop()
        if not coefficient:
            continue
        rho_degree = monomial[0]
        if rho_degree < 2:
            out[monomial] = out.get(monomial, Fraction(0)) + coefficient
            continue
        base = list(monomial)
        base[0] -= 2
        pending.append((tuple(base), coefficient))
        sigma_term = list(base)
        sigma_term[1] += 2
        pending.append((tuple(sigma_term), coefficient))
    return clean(out)


def equal_cover(left: Mapping[Monomial, Fraction], right: Mapping[Monomial, Fraction]) -> bool:
    return not reduce_cover(sub(left, right))


def substitute(poly: Mapping[Monomial, Fraction], index: int, replacement: Mapping[Monomial, Fraction]) -> Polynomial:
    out: Polynomial = {}
    for monomial, coefficient in poly.items():
        exponent = monomial[index]
        residual = list(monomial)
        residual[index] = 0
        term = {tuple(residual): coefficient}
        out = add(out, mul(term, power(replacement, exponent)))
    return reduce_cover(out)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def find_one(root: Path, candidates: Iterable[str]) -> Path:
    for candidate in candidates:
        path = root / candidate
        if path.is_file():
            return path
    raise FileNotFoundError("none of the source candidates exists: " + ", ".join(candidates))


class Replay:
    def __init__(self) -> None:
        self.assertions = 0

    def check(self, condition: bool, label: str) -> None:
        if not condition:
            raise AssertionError(label)
        self.assertions += 1

    def poly(self, left: Polynomial, right: Polynomial, label: str) -> None:
        self.check(equal_cover(left, right), label)


def replay(root: Path, certificate_path: Path) -> Tuple[int, str]:
    cert = json.loads(certificate_path.read_text(encoding="utf-8"))
    r = Replay()

    r.check(cert["schema_id"] == "cella.cce6.native_surface_sweep_clearance_certificate", "schema id")
    r.check(cert["schema_version"] == "1.0", "schema version")
    r.check(cert["verdict"] == "PROVED", "verdict")
    r.check(cert["claim_scope"] == "two_exact_dbp_corridors_on_native_surface_image", "claim scope")
    r.check(cert["scope_ceiling"] == "S_Z^nat=image(L_Z); no whole-surface claim", "scope ceiling")

    source_candidates = {
        "cce2_stage_report_json_sha256": [
            "upload/CCE_2_STAGE_REPORT_v1.0.json",
            "research/campaigns/CELLA_CONTINUATION_ENGINE/03_cce2_corridors/CCE_2_STAGE_REPORT_v1.0.json",
        ],
        "cce2_route_digests_json_sha256": [
            "upload/DBP_EXACT_CORRIDOR_ROUTE_DIGESTS_v1.0.json",
            "research/campaigns/CELLA_CONTINUATION_ENGINE/03_cce2_corridors/DBP_EXACT_CORRIDOR_ROUTE_DIGESTS_v1.0.json",
        ],
        "cce2_clearance_bundle_json_sha256": [
            "upload/DBP_EXACT_CORRIDOR_CLEARANCE_CERTIFICATES_v1.0.json",
            "research/campaigns/CELLA_CONTINUATION_ENGINE/03_cce2_corridors/DBP_EXACT_CORRIDOR_CLEARANCE_CERTIFICATES_v1.0.json",
        ],
        "stage2_surface_source_sha256": [
            "DBP_DUAL_SURFACE_CYCLE_STAGE2_v0.1.md",
            "research/paper/Theorems/DBP/technical_supplements/DBP_DUAL_SURFACE_CYCLE_STAGE2_v0.1.md",
        ],
        "stage3_surface_source_sha256": [
            "DBP_DUAL_SURFACE_CYCLE_STAGE3_v0.1.md",
            "research/paper/Theorems/DBP/technical_supplements/DBP_DUAL_SURFACE_CYCLE_STAGE3_v0.1.md",
        ],
        "paper_iii_source_sha256": [
            "DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md",
            "research/paper/Theorems/DBP/DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md",
        ],
        "existing_work_extraction_report_sha256": [
            "upload/CCE_5_8_EXISTING_WORK_SUPPORT_AND_EXTRACTION_REPORT_v1.0.md",
            "research/campaigns/CELLA_CONTINUATION_ENGINE/00_campaign_authority/CCE_5_8_EXISTING_WORK_SUPPORT_AND_EXTRACTION_REPORT_v1.0.md",
        ],
    }
    for key, candidates in source_candidates.items():
        source = find_one(root, candidates)
        r.check(sha256(source) == cert["source_bindings"][key], "source binding: " + key)

    theorem = find_one(root, [
        cert["theorem_artifact"]["path"],
        "research/campaigns/CELLA_CONTINUATION_ENGINE/07_cce6_surface/CCE_6_COMPLETE_PACKAGE_v1.0/"
        + cert["theorem_artifact"]["path"],
    ])
    r.check(sha256(theorem) == cert["theorem_artifact"]["sha256"], "theorem binding")

    clearance_path = find_one(root, source_candidates["cce2_clearance_bundle_json_sha256"])
    clearance = json.loads(clearance_path.read_text(encoding="utf-8"))
    for arm in ("upper", "lower"):
        nested = cert["nested_corridor_certificates"][arm]
        source_cert = clearance["certificates"][arm]
        r.check(source_cert["route_manifest"]["route_id"] == nested["route_id"], arm + " route id")
        r.check(source_cert["route_manifest_digest"] == nested["route_manifest_digest"], arm + " route digest")
        r.check(canonical_digest(source_cert) == nested["clearance_certificate_digest"], arm + " clearance digest")
        tube = source_cert["tube_bounds"]

        def tube_fraction(key: str) -> Fraction:
            value = tube[key]
            return Fraction(int(value["numerator"]), int(value["denominator"]))

        published_separations = {
            "m": Fraction(1, 512),
            "one_minus_m": Fraction(1, 512),
            "x_p": Fraction(2, 5),
            "x_p_minus_one": Fraction(1, 320),
            "x_p_minus_m": Fraction(1, 163840),
            "y_p_squared": Fraction(1, 131072000),
        }
        for key, expected in published_separations.items():
            r.check(tube_fraction(key) == expected, arm + " marked-section bound: " + key)

    rho, sigma, V, T, Xi, H = (variable(i) for i in range(6))
    one = const(1)
    two = const(2)
    A = add(rho, one)
    B = sub(rho, one)
    Delta1 = sub(mul(A, T), mul(B, V))
    Delta2 = sub(mul(power(A, 2), T), mul(power(B, 2), V))

    r.poly(sub(A, B), two, "A-B=2")
    r.poly(add(A, B), scale(rho, 2), "A+B=2rho")
    r.poly(mul(A, B), power(sigma, 2), "AB=sigma^2")

    angular_sum = add(scale(V, 2), mul(A, sub(T, V)))
    r.poly(angular_sum, Delta1, "angular C^2+S^2 numerator")

    norm = add(mul(Delta2, power(Xi, 2)), scale(mul(mul(A, T), power(H, 2)), 2))
    linear_resultant_factor = sub(scale(mul(A, T), 2), Delta2)
    r.poly(linear_resultant_factor, neg(mul(B, Delta1)), "resultant linear factor")
    resultant = power(linear_resultant_factor, 2)
    r.poly(resultant, mul(power(B, 2), power(Delta1, 2)), "cleared norm-polar resultant")

    r.poly(
        sub(scale(mul(B, V), 2), Delta2),
        neg(mul(A, Delta1)),
        "x-1 divisor identity",
    )
    r.poly(
        sub(scale(mul(rho, V), 4), Delta2),
        mul(power(A, 2), sub(V, T)),
        "x-m divisor identity",
    )
    r.poly(
        add(mul(power(B, 2), V), Delta2),
        mul(power(A, 2), T),
        "x-xp divisor identity",
    )

    zero = const(0)
    delta1_v0 = substitute(Delta1, 2, zero)
    delta2_v0 = substitute(Delta2, 2, zero)
    norm_v0 = substitute(norm, 2, zero)
    r.poly(delta1_v0, mul(A, T), "V=0 Delta1")
    r.poly(delta2_v0, mul(power(A, 2), T), "V=0 Delta2")
    r.poly(norm_v0, mul(mul(A, T), add(mul(A, power(Xi, 2)), scale(power(H, 2), 2))), "V=0 norm")
    r.poly(
        substitute(mul(power(B, 2), power(Delta1, 2)), 2, zero),
        mul(mul(power(A, 2), power(B, 2)), power(T, 2)),
        "V=0 resultant",
    )

    delta1_vt = substitute(Delta1, 2, T)
    delta2_vt = substitute(Delta2, 2, T)
    norm_vt = substitute(norm, 2, T)
    r.poly(delta1_vt, scale(T, 2), "V=T Delta1")
    r.poly(delta2_vt, scale(mul(rho, T), 4), "V=T Delta2")
    r.poly(norm_vt, scale(mul(T, add(scale(mul(rho, power(Xi, 2)), 2), mul(A, power(H, 2)))), 2), "V=T norm")
    r.poly(
        substitute(mul(power(B, 2), power(Delta1, 2)), 2, T),
        scale(mul(power(B, 2), power(T, 2)), 4),
        "V=T resultant",
    )

    r.poly(substitute(norm, 5, zero), mul(Delta2, power(Xi, 2)), "norm at H=0")
    polar_fibre = add(power(Xi, 2), power(H, 2))
    r.poly(substitute(polar_fibre, 5, zero), power(Xi, 2), "polar at H=0")

    bounds = cert["corridor_tube_bounds"]
    sigma_lower = Fraction(bounds["abs_sigma_lower"])
    rho_lower = Fraction(bounds["abs_rho_lower"])
    A_upper = Fraction(bounds["abs_A_upper"])
    c_lower = Fraction(bounds["abs_c_lower"])
    r.check(sigma_lower * sigma_lower / 4 == Fraction(bounds["derived_abs_ab_lower"]), "ab lower bound")
    r.check(Fraction(2, 1) / A_upper == Fraction(bounds["derived_abs_one_minus_c_lower"]), "1-c lower bound")
    r.check(2 * rho_lower / A_upper == Fraction(bounds["derived_abs_one_plus_c_lower"]), "1+c lower bound")
    serialized_separations = {
        "abs_m_lower": Fraction(1, 512),
        "abs_one_minus_m_lower": Fraction(1, 512),
        "abs_x_p_lower": Fraction(2, 5),
        "abs_x_p_minus_one_lower": Fraction(1, 320),
        "abs_x_p_minus_m_lower": Fraction(1, 163840),
        "abs_y_p_squared_lower": Fraction(1, 131072000),
    }
    for key, expected in serialized_separations.items():
        r.check(Fraction(bounds[key]) == expected, "serialized marked-section bound: " + key)

    c_upper = 1 / Fraction(bounds["abs_inverse_c_lower"])
    norm_p1_upper = 1 + c_upper
    norm_p2_upper = 1 + c_upper * c_upper
    pairwise_lower = (
        Fraction(bounds["abs_c_lower"])
        * Fraction(bounds["derived_abs_one_minus_c_lower"])
        / (norm_p1_upper * norm_p2_upper)
    )
    exclusion_radius = pairwise_lower / 4
    contract = cert["refined_curve_clearance_contract"]
    r.check(norm_p1_upper == 321, "P1 norm upper")
    r.check(norm_p2_upper == 102401, "P2 norm upper")
    r.check(pairwise_lower == Fraction(1, 26296576800), "minimum pairwise chordal separation")
    r.check(exclusion_radius == Fraction(1, 105186307200), "uniform exclusion radius")
    r.check(Fraction(contract["minimum_pairwise_separation_lower"]) == pairwise_lower, "serialized pairwise separation")
    r.check(Fraction(contract["uniform_exclusion_radius"]) == exclusion_radius, "serialized exclusion radius")
    r.check(Fraction(contract["primary_track_clearance_lower"]) == Fraction(1, 25), "primary track clearance")
    other_pairwise_bounds = {
        "fixed-point pairs": Fraction(1, 2),
        "P0-P1": Fraction(1, 321),
        "P0-P2": Fraction(1, 102401),
        "Pinfinity-P1": Fraction(bounds["abs_c_lower"]) / norm_p1_upper,
        "Pinfinity-P2": Fraction(bounds["abs_c_lower"]) ** 2 / norm_p2_upper,
        "Pm-P1": Fraction(bounds["derived_abs_one_minus_c_lower"]) / (2 * norm_p1_upper),
        "Pm-P2": (
            Fraction(bounds["derived_abs_one_minus_c_lower"])
            * Fraction(bounds["derived_abs_one_plus_c_lower"])
            / (2 * norm_p2_upper)
        ),
    }
    for label, lower in other_pairwise_bounds.items():
        r.check(lower >= pairwise_lower, label + " separation dominates minimum")

    one_minus_c = Fraction(bounds["derived_abs_one_minus_c_lower"])
    one_plus_c = Fraction(bounds["derived_abs_one_plus_c_lower"])
    q = cert["quantitative_transfer"]
    r.check(4 * one_minus_c == Fraction(8, 5), "general discriminant coefficient")
    r.check(c_lower * c_lower == Fraction(1, 102400), "general resultant coefficient")
    r.check(one_minus_c == Fraction(2, 5), "constant coefficient bound")
    r.check(one_minus_c * one_plus_c == Fraction(2, 25), "V=T D2 coefficient")
    r.check(4 * one_minus_c * one_minus_c * one_plus_c == Fraction(16, 125), "V=T discriminant coefficient")
    r.check(c_lower * c_lower * one_minus_c * one_minus_c == Fraction(1, 640000), "V=T resultant coefficient")

    expected_quantitative = {
        "released_route_epsilon_infinity": "1/105186307200",
        "released_route_epsilon_1": "1/105186307200",
        "released_route_epsilon_2": "1/105186307200",
        "abs_norm_discriminant_lower": "(8/5)*epsilon_infinity*epsilon_2",
        "abs_norm_polar_resultant_lower": "epsilon_1^2/102400",
        "abs_norm_constant_coefficient_lower": "(2/5)*epsilon_infinity",
        "abs_norm_leading_coefficient_lower": "epsilon_2",
        "face_V0_abs_D1_lower": "epsilon_infinity",
        "face_V0_abs_D2_lower": "epsilon_infinity",
        "face_V0_abs_discriminant_lower": "(8/5)*epsilon_infinity^2",
        "face_V0_abs_resultant_lower": "epsilon_infinity^2/102400",
        "face_VT_abs_D1_lower": "(2/5)*epsilon_infinity",
        "face_VT_abs_D2_lower": "(2/25)*epsilon_infinity",
        "face_VT_abs_discriminant_lower": "(16/125)*epsilon_infinity^2",
        "face_VT_abs_resultant_lower": "epsilon_infinity^2/640000",
    }
    r.check(q == expected_quantitative, "serialized quantitative ledger")

    r.check(cert["collision_identities"]["norm_polar_resultant_primitive"] == "c^2*D1^2", "primitive resultant ledger")
    r.check(cert["collision_identities"]["norm_discriminant_primitive"] == "-4*(1-c)*T*D2", "primitive discriminant ledger")
    r.check(cert["curve_divisor_reduction"]["divisor_map"]["T=0"] == "x=x_p", "polar curve map")
    r.check(cert["curve_divisor_reduction"]["divisor_map"]["D1=0"] == "x=1", "D1 curve map")
    r.check(cert["curve_divisor_reduction"]["divisor_map"]["D2=0"] == "x=infinity", "D2 curve map")
    r.check(cert["retired_blocker"].startswith("SurfaceSweepClearanceUnproved"), "blocker retirement")
    r.check("OutsideNativeSurfaceImage" in cert["retained_refusals"], "native-image refusal retained")
    r.check("WholeSurfaceScopeUnproved" in cert["retained_refusals"], "whole-surface refusal retained")
    r.check("SurfaceRouteAdmissibilityMissing" in cert["retained_refusals"], "arbitrary-route refusal retained")

    return r.assertions, canonical_digest(cert)


def main() -> None:
    parser = argparse.ArgumentParser()
    repository_root = next(
        (parent for parent in Path(__file__).resolve().parents if (parent / "engine/src").is_dir()),
        Path(__file__).resolve().parent,
    )
    parser.add_argument("--root", type=Path, default=repository_root)
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).resolve().with_name(
            "DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_CERTIFICATE_v1.0.json"
        ),
    )
    args = parser.parse_args()
    assertions, digest = replay(args.root.resolve(), args.certificate.resolve())
    print(f"CCE-6 native surface-clearance replay: {assertions} assertions passed")
    print(f"canonical certificate digest: {digest}")


if __name__ == "__main__":
    main()
