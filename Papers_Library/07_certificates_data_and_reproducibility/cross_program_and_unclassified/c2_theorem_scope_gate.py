"""
c2 Theorem Scope Gate Audit.

Verifies that actual campaign fixtures (the ones whose c2 lattice property
the proven theorem is supposed to cover) keep f_float in the normal range
where Conjecture C is proven, specifically f_float >= 2^(-1021).

This is the gate that must pass before the c2 lattice theorem can be
promoted from "conditional on C" to "unconditional", and even then only
with the explicit-bound qualifier.

The user's critique (2026-05-18): the proof's mechanism is scaling
invariance; that mechanism dies in subnormal. The campaign's trajectory
(v5–v9 fold-readback, c2 sharpness sweeps) heads toward small f. Verify-
don't-assume that actual fixtures stay above the proven floor.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from lloyd_v4.primitives import typed_ulp


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "Build_Docs" / "Reports" / "c2_theorem_scope_gate"
ARTIFACT = REPORT_DIR / "artifact.json"

# Theorem's proven domain: f_float >= 2^(-1021) (the smallest normal-range
# odd-k binade for which Conjecture C was verified).
THEOREM_FLOOR = math.ldexp(1.0, -1021)


# ---------------------------------------------------------------------------
# Sweep specifications matching actual campaigns
# ---------------------------------------------------------------------------


def _ulp_f64(x: float) -> float:
    """ULP via the ``typed_ulp`` substrate primitive (GAP-003, precision='float64').

    Migrated from inline IEEE 754 ULP helper as part of the DRY-003 substrate
    consolidation. Byte-compatible with the original on finite normal inputs.
    """
    return float(typed_ulp(x, precision="float64").value.ulp)


def _binade_index(x: float) -> int:
    if x == 0.0 or not math.isfinite(x):
        return -2000
    return math.frexp(x)[1] - 1


def _is_subnormal(x: float) -> bool:
    return 0.0 < abs(x) < math.ldexp(1.0, -1022)


# ---------------------------------------------------------------------------
# Fixture-specific f_float computations
# ---------------------------------------------------------------------------


def _f_float_SR(beta: float) -> float:
    return 1.0 - beta * beta


def _f_float_Schwarzschild(r: float) -> float:
    return 1.0 - 2.0 / r


def _f_float_PureAlgebraic(x: float) -> float:
    return 1.0 - x


def _f_float_CubeRoot(x: float) -> float:
    return 1.0 - x


# ---------------------------------------------------------------------------
# Sweep grids matching each known campaign
# ---------------------------------------------------------------------------


def _campaign_grids() -> dict:
    """Return parameter grids for each known campaign × fixture combination.
    Matches what c2_lattice_sharpness_audit.py, v11 densified grid, and
    Test A actually used.
    """
    grids = {}

    # c2 sharpness audit (full natural range, 10K pts)
    grids["c2_sharpness_SR"] = np.linspace(1e-3, 1.0 - 1e-3, 10000)
    grids["c2_sharpness_Schwarzschild"] = np.geomspace(2.001, 1e6, 10000)
    grids["c2_sharpness_PureAlgebraic"] = np.linspace(1e-3, 1.0 - 1e-3, 10000)
    grids["c2_sharpness_CubeRoot"] = np.linspace(1e-3, 1.0 - 1e-3, 10000)

    # v11 fold-readback densified grid (SR near β=1)
    # Reconstruct from scratch/run_foldreadback_probe0_v11_genuine_separation.py
    # densified_sr_grid(): base + extras at 1 - 10^(-2 - k*0.1) for k=1..29
    base = np.linspace(0.001, 0.9999, 137)  # rough approximation of beta_grid
    extras = []
    for k in range(1, 30):
        one_minus_beta = 10.0 ** (-2.0 - k * 0.1)
        beta_val = 1.0 - one_minus_beta
        if 0.99 <= beta_val < 1.0:
            extras.append(beta_val)
    grids["v11_densified_SR"] = np.array(sorted(set(list(base) + extras)))

    # c2 substrate derivation (dense logarithmic grid)
    grids["c2_substrate_SR"] = np.linspace(1e-3, 1.0 / math.sqrt(2.0), 5000)
    grids["c2_substrate_Schwarzschild"] = np.linspace(4.0, 100.0, 5000)
    grids["c2_substrate_PureAlgebraic"] = np.linspace(1e-3, 0.5, 5000)
    grids["c2_substrate_CubeRoot"] = np.linspace(1e-3, 0.5, 5000)

    # Test A region (Sterbenz region per fixture, 4 fixtures, ~70 pts each)
    # Use rougher reconstructions
    grids["test_a_SR"] = np.linspace(0.01, 1.0 / math.sqrt(2.0), 100)
    grids["test_a_Schwarzschild"] = np.linspace(4.0, 50.0, 100)
    grids["test_a_PureAlgebraic"] = np.linspace(0.01, 0.5, 100)
    grids["test_a_CubeRoot"] = np.linspace(0.01, 0.5, 100)

    # Hypothetical "deep cancellation" — push β very close to 1 to see what
    # the campaign's natural trajectory CAN reach.
    grids["deep_SR_near_1"] = np.array(
        [1.0 - math.ldexp(1.0, -e) for e in range(1, 53) if 1.0 - math.ldexp(1.0, -e) > 0]
    )
    return grids


# ---------------------------------------------------------------------------
# Fixture-specific f_float minima
# ---------------------------------------------------------------------------


def _fixture_for_grid(grid_name: str):
    if grid_name.endswith("_SR") or "SR_near" in grid_name:
        return _f_float_SR
    if grid_name.endswith("_Schwarzschild"):
        return _f_float_Schwarzschild
    if grid_name.endswith("_PureAlgebraic"):
        return _f_float_PureAlgebraic
    if grid_name.endswith("_CubeRoot"):
        return _f_float_CubeRoot
    return None


def _audit_grid(grid_name: str, grid: np.ndarray) -> dict:
    f_func = _fixture_for_grid(grid_name)
    if f_func is None:
        return {"error": f"unknown fixture for grid {grid_name}"}
    f_values = [f_func(float(x)) for x in grid]
    f_values_pos = [f for f in f_values if f > 0]
    if not f_values_pos:
        return {"grid": grid_name, "no_positive_f": True}
    f_min = min(f_values_pos)
    f_max = max(f_values_pos)
    # Where is f_min relative to the theorem floor?
    f_min_binade = _binade_index(f_min)
    f_min_is_subnormal = _is_subnormal(f_min)
    f_min_geq_floor = f_min >= THEOREM_FLOOR
    margin_log2 = (math.log2(f_min) - math.log2(THEOREM_FLOOR)) if f_min > 0 else None
    # Find the smallest few f values
    f_sorted = sorted(f_values_pos)[:5]
    return {
        "grid": grid_name,
        "grid_size": len(grid),
        "n_positive_f": len(f_values_pos),
        "f_min": float(f_min),
        "f_max": float(f_max),
        "f_min_binade_k": int(f_min_binade),
        "f_min_is_subnormal": bool(f_min_is_subnormal),
        "f_min_geq_floor_2_to_neg_1021": bool(f_min_geq_floor),
        "margin_log2": float(margin_log2) if margin_log2 is not None else None,
        "smallest_5_f_values": [float(x) for x in f_sorted],
    }


# ---------------------------------------------------------------------------
# Theoretical reachability — how small can f_float get in principle?
# ---------------------------------------------------------------------------


def _theoretical_reachability_per_fixture() -> dict:
    """For each fixture form, compute the minimum f_float reachable given
    float64 precision limits (not just our sweep ranges)."""
    # For SR: f = 1 - β². The smallest f > 0 is when β² is just below 1.
    # Smallest β² below 1 in float64: 1 - ulp(1) = 1 - 2^(-52). So min f = 2^(-52).
    # But β² is a computation: β² for β just below 1 rounds to 1 - 2^(-52) or further.
    # In practice: min β² in float64 just-below-1 is 1 - 2^(-52); min f = 2^(-52).
    sr_min_f = math.ldexp(1.0, -52)  # 2^(-52)

    # For Schwarzschild: f = 1 - 2/r. For r very large, 2/r → 0, f → 1. For r just above 2,
    # 2/r just below 1. Min f when 2/r = nextafter(1, 0) = 1 - 2^(-53). So min f = 2^(-53).
    schw_min_f = math.ldexp(1.0, -53)

    # For pure_algebraic / cube_root: f = 1 - x. Min f = ulp(1) = 2^(-52)
    pa_min_f = math.ldexp(1.0, -52)

    return {
        "SR_theoretical_min_f": sr_min_f,
        "Schwarzschild_theoretical_min_f": schw_min_f,
        "PureAlgebraic_theoretical_min_f": pa_min_f,
        "CubeRoot_theoretical_min_f": pa_min_f,
        "all_theoretical_min_geq_floor": all(
            v >= THEOREM_FLOOR
            for v in [sr_min_f, schw_min_f, pa_min_f]
        ),
        "theorem_floor": THEOREM_FLOOR,
        "theorem_floor_binade_k": _binade_index(THEOREM_FLOOR),
    }


# ---------------------------------------------------------------------------
# Run gate
# ---------------------------------------------------------------------------


def run_gate() -> dict:
    grids = _campaign_grids()
    per_grid_results = {}
    any_subnormal = False
    any_below_floor = False
    min_margin_log2 = float("inf")
    for grid_name, grid in grids.items():
        r = _audit_grid(grid_name, grid)
        per_grid_results[grid_name] = r
        if r.get("f_min_is_subnormal"):
            any_subnormal = True
        if not r.get("f_min_geq_floor_2_to_neg_1021", True):
            any_below_floor = True
        if r.get("margin_log2") is not None:
            min_margin_log2 = min(min_margin_log2, r["margin_log2"])

    theoretical = _theoretical_reachability_per_fixture()

    if any_below_floor:
        gate_verdict = "GATE_FAILS_C_subnormal_required"
    elif any_subnormal:
        gate_verdict = "GATE_FAILS_subnormal_observed"
    else:
        gate_verdict = "GATE_PASSES_actual_fixtures_in_normal_range"

    return {
        "audit_name": "c2_theorem_scope_gate",
        "purpose": "Verify campaign fixtures stay above proven floor f_float >= 2^(-1021) before promoting theorem to unconditional",
        "theorem_floor": THEOREM_FLOOR,
        "theorem_floor_binade_k": _binade_index(THEOREM_FLOOR),
        "per_grid_results": per_grid_results,
        "theoretical_reachability_per_fixture": theoretical,
        "gate_summary": {
            "any_subnormal_observed": any_subnormal,
            "any_below_floor": any_below_floor,
            "min_margin_log2_above_floor": min_margin_log2,
            "verdict": gate_verdict,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(ARTIFACT))
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    data = run_gate()
    Path(args.output).write_text(json.dumps(data, indent=2, sort_keys=True))
    print(f"scope-gate artifact written to {args.output}")
    print(f"  theorem floor: f_float >= 2^({_binade_index(THEOREM_FLOOR)}) = {THEOREM_FLOOR:.4e}")
    print()
    print(f"  Per-grid f_min:")
    for grid, r in data["per_grid_results"].items():
        marker = "✓" if r.get("f_min_geq_floor_2_to_neg_1021") else "✗"
        margin = r.get("margin_log2")
        margin_str = f"margin = {margin:.1f} binades above floor" if margin is not None else "n/a"
        sub_marker = " ← SUBNORMAL!" if r.get("f_min_is_subnormal") else ""
        print(
            f"    {marker} {grid:35} f_min = 2^{r.get('f_min_binade_k', 'n/a'):>5} = {r.get('f_min', 0):.4e} ({margin_str}){sub_marker}"
        )
    print()
    print(f"  Theoretical reachability per fixture (float64 limits):")
    t = data["theoretical_reachability_per_fixture"]
    for k in ("SR", "Schwarzschild", "PureAlgebraic", "CubeRoot"):
        key = f"{k}_theoretical_min_f"
        v = t[key]
        print(f"    {k:20} theoretical min f = 2^{_binade_index(v):>5} = {v:.4e}")
    print(f"    All theoretical mins ≥ floor? {t['all_theoretical_min_geq_floor']}")
    print()
    print(f"  Gate verdict: {data['gate_summary']['verdict']}")
    print(f"  Minimum margin above floor: {data['gate_summary']['min_margin_log2_above_floor']:.1f} binades")


if __name__ == "__main__":
    main()
