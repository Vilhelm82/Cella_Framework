"""
Conjecture C — Definition-Grounded Audit.

Re-establishes Conjecture C's load-bearing empirical step (R = R_above(m)
for every odd k in normal range) by deriving R_above(m) from the
round-to-nearest-even definition applied to mpmath's exact sqrt, rather
than asserting it via bit pattern + libm cross-check.

The original conjecture_c_proof_audit used:
  R = math.sqrt(2^k)                              # libm call
  R_above_predicted = bit-pattern construction    # hardcoded mantissa
  assert R == R_above_predicted                   # libm cross-check

This version uses:
  exact_sqrt = mpmath.sqrt(mpmath.power(2, k))    # exact in mpmath
  R_RN_definition = RN_even_of_mpmath(exact_sqrt) # RN-even from definition
  R_RN_definition is the proof's R_above(m)       # grounded in RN-even
  cross-check: R_RN_definition == math.sqrt(2^k)  # IEEE conformance check

The proof's R_above(m) is now derived from the RN-even definition; the
libm comparison becomes a separate sanity check, not part of the proof.

User direction (2026-05-18): grounding the proof requires RN-even from
definition, not libm assertion.
"""
from __future__ import annotations

import argparse
import json
import math
import struct
import sys
from pathlib import Path

import mpmath

mpmath.mp.dps = 100  # high-precision oracle


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "Build_Docs" / "Reports" / "conjecture_c_proof_audit"
ARTIFACT = REPORT_DIR / "definition_grounded_artifact.json"


# ---------------------------------------------------------------------------
# RN-even, derived purely from the definition
# ---------------------------------------------------------------------------


def RN_even_of_mpmath_to_float64(x_mp: mpmath.mpf) -> float:
    """Round a high-precision mpmath value to IEEE 754 float64 using
    round-to-nearest-ties-to-even, derived purely from the definition.

    Definition: the result is the float64 closest to x. If x is exactly
    midway between two adjacent float64 values, the result is the one
    with even mantissa LSB.

    Returns a Python float (which is float64 on standard CPython).
    """
    if x_mp == 0:
        return 0.0
    if x_mp < 0:
        return -RN_even_of_mpmath_to_float64(-x_mp)

    # Find binade: k such that x ∈ [2^k, 2^(k+1))
    # Use mpmath.frexp: x = m * 2^e with m ∈ [0.5, 1), so binade = e - 1
    m_frac, e = mpmath.frexp(x_mp)
    k = int(e) - 1

    if k < -1022 or k > 1023:
        raise ValueError(f"value outside float64 normal range, binade k={k}")

    # Floats in binade [2^k, 2^(k+1)) are M · 2^(k-52) for M ∈ [2^52, 2^53)
    # (53-bit precision: implicit leading 1 bit + 52 explicit mantissa bits)
    ulp = mpmath.power(2, k - 52)
    M_real = x_mp / ulp  # M_real ∈ [2^52, 2^53)

    # Two adjacent integers M_lo, M_hi bracketing M_real
    M_lo = int(mpmath.floor(M_real))
    M_hi = M_lo + 1

    # Distances from M_real to M_lo and M_hi
    distance_lo = M_real - mpmath.mpf(M_lo)  # ∈ [0, 1)
    distance_hi = mpmath.mpf(1) - distance_lo  # ∈ (0, 1]

    # Apply RN-even
    if distance_lo < distance_hi:
        M_chosen = M_lo
    elif distance_lo > distance_hi:
        M_chosen = M_hi
    else:
        # Exact tie (distance == 1/2): round to even mantissa LSB
        if M_lo % 2 == 0:
            M_chosen = M_lo
        else:
            M_chosen = M_hi

    # Boundary case: if M_chosen rounds up to 2^53, the value is at the
    # next binade boundary (= 2^(k+1)), and the float representation
    # shifts to that binade with mantissa 2^52.
    if M_chosen == 2 ** 53:
        k_actual = k + 1
        M_actual = 2 ** 52
    else:
        k_actual = k
        M_actual = M_chosen

    # Construct the float64 bit pattern directly to avoid float() routine ambiguity
    if k_actual > 1023:
        raise ValueError("overflow into infinity")
    mantissa_bits = M_actual - 2 ** 52  # 52-bit explicit mantissa
    biased_exp = k_actual + 1023
    bits = (biased_exp << 52) | mantissa_bits
    return struct.unpack(">d", bits.to_bytes(8, byteorder="big"))[0]


# ---------------------------------------------------------------------------
# Definition-grounded R_above(m) for each odd k
# ---------------------------------------------------------------------------


def R_above_from_definition(k: int) -> float:
    """Compute R_above(m) for k = 2m+1 by:
    1. Computing exact sqrt(2^k) in mpmath at 100 dps
    2. Applying RN-even from definition

    Returns a float64 value. This is the proof's R_above, grounded
    in the RN-even definition, NOT via libm.
    """
    assert k % 2 != 0, f"R_above defined only for odd k; got k={k}"
    f_mp = mpmath.power(2, k)
    exact_sqrt = mpmath.sqrt(f_mp)
    R_RN = RN_even_of_mpmath_to_float64(exact_sqrt)
    return R_RN


def R_above_squared_strictly_above_2k(k: int, R_above: float) -> tuple[bool, str]:
    """Check whether R_above² > 2^k strictly, using mpmath.
    Returns (verdict, mpmath difference as string)."""
    R_hp = mpmath.mpf(R_above)
    R_squared_hp = R_hp * R_hp
    f_hp = mpmath.power(2, k)
    diff = R_squared_hp - f_hp
    return (diff > 0, str(diff))


# ---------------------------------------------------------------------------
# Audit: verify R_above_from_definition agrees with bit-pattern construction
# and with libm — both as cross-checks, not as proof steps
# ---------------------------------------------------------------------------


def _bit_pattern_R_above(k: int) -> float:
    """The original audit's bit-pattern construction (libm-derived).
    Used here for cross-check only."""
    m = (k - 1) // 2
    mantissa_52 = 0x6a09e667f3bcd
    bits = ((m + 1023) << 52) | mantissa_52
    return struct.unpack(">d", bits.to_bytes(8, byteorder="big"))[0]


def audit_one_k(k: int) -> dict:
    """Audit one odd k value: derive R_above from definition, verify R² > 2^k,
    cross-check libm and bit-pattern construction."""
    R_definition = R_above_from_definition(k)
    R_libm = math.sqrt(math.ldexp(1.0, k))
    R_bitpattern = _bit_pattern_R_above(k)

    R_squared_above, diff_str = R_above_squared_strictly_above_2k(k, R_definition)
    libm_matches_definition = (R_libm == R_definition)
    bitpattern_matches_definition = (R_bitpattern == R_definition)

    return {
        "k": k,
        "R_definition_grounded": R_definition,
        "R_libm": R_libm,
        "R_bitpattern": R_bitpattern,
        "libm_matches_definition": bool(libm_matches_definition),
        "bitpattern_matches_definition": bool(bitpattern_matches_definition),
        "R_squared_strictly_above_2k": bool(R_squared_above),
        "R_squared_minus_2k_mpmath": diff_str,
    }


def run_audit() -> dict:
    odd_k_values = list(range(-1021, 1023, 2))
    records = []
    libm_mismatches = 0
    bitpattern_mismatches = 0
    R_squared_failures = 0
    for k in odd_k_values:
        r = audit_one_k(k)
        records.append(r)
        if not r["libm_matches_definition"]:
            libm_mismatches += 1
        if not r["bitpattern_matches_definition"]:
            bitpattern_mismatches += 1
        if not r["R_squared_strictly_above_2k"]:
            R_squared_failures += 1

    return {
        "audit_name": "conjecture_c_definition_grounded_audit",
        "purpose": (
            "Re-establish Conjecture C's load-bearing empirical step "
            "(R = R_above(m) for every odd k) by deriving R_above from "
            "the RN-even definition applied to mpmath exact sqrt, rather "
            "than asserting it via bit pattern + libm cross-check. "
            "Per user direction (2026-05-18), this grounds the proof in "
            "the RN-even definition; libm cross-check becomes a separate "
            "IEEE conformance sanity check, not part of the proof."
        ),
        "n_odd_k_values_tested": len(odd_k_values),
        "k_range": [odd_k_values[0], odd_k_values[-1]],
        "libm_mismatches_count": libm_mismatches,
        "bitpattern_mismatches_count": bitpattern_mismatches,
        "R_squared_strictly_above_failures_count": R_squared_failures,
        "all_libm_match_definition": libm_mismatches == 0,
        "all_bitpattern_match_definition": bitpattern_mismatches == 0,
        "all_R_squared_strictly_above_2k": R_squared_failures == 0,
        "first_3_records": records[:3],
        "last_3_records": records[-3:],
        "verdict": (
            "Proof_grounded_in_RN_even_definition"
            if (R_squared_failures == 0)
            else "Proof_still_libm_dependent"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(ARTIFACT))
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    data = run_audit()
    Path(args.output).write_text(json.dumps(data, indent=2, sort_keys=True))
    print(f"definition-grounded audit artifact written to {args.output}")
    print(f"  verdict: {data['verdict']}")
    print(f"  n_odd_k_values_tested: {data['n_odd_k_values_tested']}")
    print(f"  k range: {data['k_range']}")
    print(f"  libm matches definition (all 1022 cases): {data['all_libm_match_definition']}")
    print(f"  bit-pattern matches definition (all 1022): {data['all_bitpattern_match_definition']}")
    print(f"  R² > 2^k strict (all 1022): {data['all_R_squared_strictly_above_2k']}")
    print(f"  libm mismatches: {data['libm_mismatches_count']}")
    print(f"  bit-pattern mismatches: {data['bitpattern_mismatches_count']}")
    print(f"  R² failures: {data['R_squared_strictly_above_failures_count']}")
    print()
    print(f"  Sample first record:")
    r0 = data["first_3_records"][0]
    print(f"    k={r0['k']}")
    print(f"    R_definition_grounded = {r0['R_definition_grounded']!r}")
    print(f"    R_libm                = {r0['R_libm']!r}")
    print(f"    R² − 2^k (mpmath)     = {r0['R_squared_minus_2k_mpmath']}")


if __name__ == "__main__":
    main()
