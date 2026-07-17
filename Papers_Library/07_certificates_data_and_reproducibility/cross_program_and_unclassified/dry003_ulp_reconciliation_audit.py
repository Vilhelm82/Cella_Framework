"""DRY-003 reconciliation audit: pre-Transplant-1 prerequisite for GAP-003.

Runs all known ULP implementations across the V4 codebase against a shared
test grid covering normal floats, subnormals (including smallest), and
non-finite values. Identifies divergences and recommends canonical
behaviour for the forthcoming typed_ulp primitive.

The audit reads each variant from its original site, runs it on the same
inputs, and reports differences. No source files are modified.

Per SUBSTRATE_CONSTRUCTION.md §5.1, the divergences are diagnostic: each
disagreement is either Mode 1 (a deeper primitive underneath) or Mode 2
(two operations sharing a name). The audit's job is to surface which mode
each divergence falls into.
"""

from __future__ import annotations

import math
import struct
import sys
from pathlib import Path
from typing import Callable

import numpy as np

# IEEE 754 float64 reference constants
SMALLEST_SUBNORMAL = 5e-324                       # 2^-1074
SMALLEST_NORMAL = 2.2250738585072014e-308          # 2^-1022
LARGEST_NORMAL = 1.7976931348623157e308            # (2-2^-52) * 2^1023


# ---------------------------------------------------------------------------
# Variant 1: unified_ulp from scratch/bacl_subnormal_audit.py
# ---------------------------------------------------------------------------

def _is_subnormal_v1(x: float) -> bool:
    return 0.0 < abs(x) < SMALLEST_NORMAL


def unified_ulp(x: float) -> float:
    """From scratch/bacl_subnormal_audit.py. Explicit subnormal branch."""
    if x == 0.0 or not math.isfinite(x):
        return SMALLEST_SUBNORMAL
    if _is_subnormal_v1(abs(x)):
        return SMALLEST_SUBNORMAL
    return math.ldexp(1.0, math.frexp(abs(x))[1] - 1 - 52)


# ---------------------------------------------------------------------------
# Variant 2: ulp_f64 from scratch/bacl_invariant_audit.py
# ---------------------------------------------------------------------------

def _floor_binade(x: float) -> int:
    if x == 0.0 or not math.isfinite(x):
        return -2000
    return math.frexp(abs(x))[1] - 1


def ulp_f64(x: float) -> float:
    """From scratch/bacl_invariant_audit.py. Floor via max() clamp."""
    if x == 0.0 or not math.isfinite(x):
        return 5e-324
    return math.ldexp(1.0, max(_floor_binade(x) - 52, -1074))


# ---------------------------------------------------------------------------
# Variant 3: _ulp from scratch/c2_lattice_substrate_derivation.py
# (also c2_lattice_sharpness_audit, c2_lattice_binade_danger_zone,
#  c2_theorem_scope_gate, blowup_exponent_v4_audit,
#  substrate_fingerprint_atlas_phase_beta)
# ---------------------------------------------------------------------------

def _ulp_c2(x: float) -> float:
    """From scratch/c2_lattice_substrate_derivation.py. Same algebra as ulp_f64."""
    if x == 0.0 or not math.isfinite(x):
        return 5e-324
    return math.ldexp(1.0, max(math.frexp(abs(x))[1] - 53, -1074))


# ---------------------------------------------------------------------------
# Variant 4: ulp_float64 from scratch/mcg_phase_1_g1_route_divergence.py
# (also mcg_gate_3_killswitch)
# ---------------------------------------------------------------------------

def ulp_float64_mcg(x: float) -> float:
    """From scratch/mcg_phase_1_g1_route_divergence.py. NO subnormal floor."""
    if x == 0.0:
        return math.ldexp(1.0, -1074)
    _, e = math.frexp(abs(x))
    return math.ldexp(1.0, e - 53)


# ---------------------------------------------------------------------------
# Variant 5: ulp_of_double from src/lloyd_v4/evals/multi_precision_four_form.py
# ---------------------------------------------------------------------------

def _bits_from_float(x: float) -> int:
    return struct.unpack(">Q", struct.pack(">d", x))[0]


def _float_from_bits(b: int) -> float:
    return struct.unpack(">d", struct.pack(">Q", b))[0]


def ulp_of_double(x: float) -> float:
    """From src/lloyd_v4/evals/multi_precision_four_form.py. NextAfter via bits."""
    absolute = abs(float(x))
    if absolute != absolute:
        return absolute
    if absolute == float("inf"):
        return absolute
    if absolute == 0.0:
        return _float_from_bits(1)
    bits = _bits_from_float(absolute)
    return _float_from_bits(bits + 1) - absolute


# ---------------------------------------------------------------------------
# Reference variant: np.nextafter-based (IEEE 754 canonical)
# ---------------------------------------------------------------------------

def ulp_nextafter(x: float) -> float:
    """Canonical IEEE 754 ulp via np.nextafter on the lattice."""
    absolute = abs(float(x))
    if math.isnan(absolute):
        return float("nan")
    if math.isinf(absolute):
        return float("inf")
    if absolute == 0.0:
        return float(np.nextafter(0.0, 1.0))
    next_up = float(np.nextafter(absolute, float("inf")))
    return next_up - absolute


# ---------------------------------------------------------------------------
# Test grid
# ---------------------------------------------------------------------------

def build_test_grid() -> list[tuple[str, float]]:
    """Test points covering normal, subnormal, boundary, and non-finite values."""
    points: list[tuple[str, float]] = []

    # Normal floats across binades
    for k in [-1021, -1000, -500, -100, -10, -1, 0, 1, 10, 100, 500, 1000, 1023]:
        x = math.ldexp(1.0, k)
        points.append((f"normal_2^{k}", x))

    # A few normal floats with non-trivial mantissa
    points.append(("normal_1.5", 1.5))
    points.append(("normal_3.14159", 3.14159))
    points.append(("normal_1e-300", 1e-300))
    points.append(("normal_1e+300", 1e+300))

    # Smallest normal
    points.append(("smallest_normal", SMALLEST_NORMAL))
    points.append(("just_above_smallest_normal", SMALLEST_NORMAL * 1.5))

    # Subnormals
    for k in [-1023, -1030, -1050, -1070, -1073, -1074]:
        x = math.ldexp(1.0, k)
        # math.ldexp may produce 0 if k is too negative; check
        if x > 0.0:
            points.append((f"subnormal_2^{k}", x))
    # Smallest subnormal explicitly
    points.append(("smallest_subnormal", SMALLEST_SUBNORMAL))
    # A subnormal near the top of the subnormal range
    points.append(("subnormal_near_normal", SMALLEST_NORMAL * 0.5))

    # Boundary cases
    points.append(("zero", 0.0))
    points.append(("largest_normal", LARGEST_NORMAL))

    # Non-finite
    points.append(("positive_inf", float("inf")))
    points.append(("nan", float("nan")))

    return points


# ---------------------------------------------------------------------------
# Audit runner
# ---------------------------------------------------------------------------

VARIANTS: dict[str, Callable[[float], float]] = {
    "unified_ulp":      unified_ulp,
    "ulp_f64":          ulp_f64,
    "_ulp_c2":          _ulp_c2,
    "ulp_float64_mcg":  ulp_float64_mcg,
    "ulp_of_double":    ulp_of_double,
    "ulp_nextafter":    ulp_nextafter,
}


def safe_call(fn: Callable[[float], float], x: float) -> str:
    """Call fn(x) and return a string repr; capture exceptions."""
    try:
        result = fn(x)
        if math.isnan(result):
            return "NaN"
        if math.isinf(result):
            return ("+inf" if result > 0 else "-inf")
        return f"{result:.6e}"
    except Exception as e:
        return f"EXC: {type(e).__name__}"


def values_agree(a: str, b: str) -> bool:
    """Two string-rendered values agree if equal as strings or both NaN."""
    if a == b:
        return True
    # Allow NaN-NaN comparison
    if a == "NaN" and b == "NaN":
        return True
    return False


def main() -> None:
    print("=" * 110)
    print("DRY-003 reconciliation audit: ULP implementations across V4 codebase")
    print("=" * 110)
    print()
    print(f"Variants under test: {len(VARIANTS)}")
    for name in VARIANTS:
        print(f"  - {name}")
    print()

    grid = build_test_grid()
    print(f"Test grid: {len(grid)} points")
    print()

    # Run each variant on each grid point
    results: dict[str, list[str]] = {name: [] for name in VARIANTS}
    for label, x in grid:
        for name, fn in VARIANTS.items():
            results[name].append(safe_call(fn, x))

    # Print the table
    name_w = max(len(n) for n in VARIANTS) + 2
    label_w = max(len(lab) for lab, _ in grid) + 2
    val_w = 14
    print(f"{'point':<{label_w}}", end="")
    for name in VARIANTS:
        print(f"{name:<{val_w + 2}}", end="")
    print()
    print("-" * (label_w + len(VARIANTS) * (val_w + 2)))

    divergences: list[tuple[str, dict[str, str]]] = []
    for i, (label, x) in enumerate(grid):
        row_vals = {name: results[name][i] for name in VARIANTS}
        print(f"{label:<{label_w}}", end="")
        for name in VARIANTS:
            print(f"{row_vals[name]:<{val_w + 2}}", end="")
        print()

        # Check for divergence (any pair disagrees)
        all_agree = True
        ref = list(row_vals.values())[0]
        for v in row_vals.values():
            if not values_agree(v, ref):
                all_agree = False
                break
        if not all_agree:
            divergences.append((label, row_vals))

    print()
    print("=" * 110)
    print(f"DIVERGENCES: {len(divergences)} of {len(grid)} test points show disagreement")
    print("=" * 110)
    print()
    for label, row_vals in divergences:
        # Group variants by their value
        by_value: dict[str, list[str]] = {}
        for name, val in row_vals.items():
            by_value.setdefault(val, []).append(name)
        print(f"  {label}:")
        for val, names in by_value.items():
            print(f"    {val:>14} : {', '.join(names)}")
        print()

    # Classify divergences against the canonical np.nextafter reference
    print("=" * 110)
    print("DIVERGENCE FROM CANONICAL (ulp_nextafter)")
    print("=" * 110)
    print()
    print("For each non-reference variant, count points where it disagrees with ulp_nextafter:")
    print()
    for name in VARIANTS:
        if name == "ulp_nextafter":
            continue
        disagreements = []
        for i, (label, _) in enumerate(grid):
            if not values_agree(results[name][i], results["ulp_nextafter"][i]):
                disagreements.append((label, results[name][i], results["ulp_nextafter"][i]))
        print(f"  {name}: {len(disagreements)} disagreements")
        for label, v, ref in disagreements:
            print(f"    {label:<32s} got {v:<14s} expected {ref}")
        print()

    print("=" * 110)
    print("RECOMMENDED CANONICAL BEHAVIOUR")
    print("=" * 110)
    print("""
For typed_ulp(x: float, format: 'float64') -> TypedUlpResult:

  Status family:
    ulp_normal          x is finite, |x| >= 2^-1022      -> 2^(binade(|x|) - 52)
    ulp_subnormal       0 < |x| < 2^-1022                -> 2^-1074  (subnormal spacing is uniform)
    ulp_zero            x == 0                            -> 2^-1074  (limit of subnormal spacing)
    ulp_nonfinite_inf   |x| == inf                       -> typed refusal; ULP of inf is undefined
    ulp_nonfinite_nan   x is NaN                         -> typed refusal; ULP of NaN is undefined

  Reference implementation: np.nextafter(|x|, +inf) - |x| for finite x.

  Justification:
    1. nextafter is the IEEE 754 canonical "distance to next representable", which is the
       mathematical definition of ULP. It produces 2^-1074 for subnormal-range inputs naturally.
    2. Returning NaN/inf for non-finite inputs (as ulp_of_double does) is more semantically
       honest than returning 5e-324 (as ulp_f64 does); but the typed primitive should refuse
       with a status rather than propagate NaN, per Axiom 4 (multi-field validity).
    3. The mcg_phase_1 variant's underflow behaviour on subnormals is wrong and should not
       become canonical.
    4. unified_ulp's treatment of non-finite as 2^-1074 conflates 'tiny' with 'undefined'.
       Axiom 6 (zero must be measured) forbids this kind of false equivalence.

Sites to update (after the typed primitive lands):
  scratch/bacl_subnormal_audit.py:51  unified_ulp        -> use typed_ulp
  scratch/bacl_invariant_audit.py:44  ulp_f64            -> use typed_ulp
  scratch/c2_lattice_*.py             _ulp_f64 / _ulp    -> use typed_ulp
  scratch/c2_theorem_scope_gate.py:42 _ulp_f64           -> use typed_ulp
  scratch/mcg_phase_1_g1_*.py:75      ulp_float64        -> use typed_ulp (CORRECTS subnormal underflow bug)
  scratch/mcg_gate_3_killswitch.py:51 ulp_float64        -> use typed_ulp (same correction)
  scratch/blowup_exponent_v4_audit.py:196 _ulp           -> use typed_ulp
  scratch/substrate_fingerprint_atlas_phase_beta.py:100 _ulp -> use typed_ulp
  src/lloyd_v4/evals/scale_invariant_signature.py:96     -> use typed_ulp(format='float32')
  src/lloyd_v4/evals/multi_precision_four_form.py:65     -> use typed_ulp
""")


if __name__ == "__main__":
    main()
