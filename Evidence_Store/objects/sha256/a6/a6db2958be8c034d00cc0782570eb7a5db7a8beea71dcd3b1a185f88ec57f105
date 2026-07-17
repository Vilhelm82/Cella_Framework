"""
Test A: Cross-fixture refinery audit.

For each of 4 fixtures (Schwarzschild, SR, pure-algebraic, cube-root):
- Compute c1 = (R^n) - 1 + x_term  [Sterbenz-blessed]
- Compute c2 = (R^n) + (x_term - 1)  [reassociated]
- Across Sterbenz-applicable region (R^n >= 1/2)
- Classify lattice character (integer / half-integer / quarter-integer / irregular)
- Verdict: does c2 dominate c1 on lattice class per fixture?

Preregistry: Build_Docs/Reports/task032_cross_fixture_refinery_audit/preregistry.md
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "src")

from lloyd_v4.evals.sr_four_form import beta_grid as sr_beta_grid
from lloyd_v4.evals.pure_algebraic_four_form import x_grid as pa_x_grid
from lloyd_v4.evals.schwarzschild_four_form import sweep_r_values
from lloyd_v4.evals.multi_precision_four_form import ulp_of_double


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "Build_Docs" / "Reports" / "task032_cross_fixture_refinery_audit"
ARTIFACT = REPORT_DIR / "artifact.json"


# Fixture definitions: each returns (native_grid, sterbenz_predicate, x_term_func, R_func, n)
def fixture_schwarzschild():
    def x_term(r): return 2.0 / r
    def R_func(r): return (1.0 - 2.0 / r) ** 0.5
    return {
        "name": "schwarzschild",
        "native_var": "r",
        "grid": sweep_r_values(),
        "sterbenz_predicate": lambda r: r >= 4.0,
        "boundary": "r >= 4 (Sterbenz: R^2 = 1 - 2/r >= 1/2)",
        "x_term": x_term,
        "R_func": R_func,
        "f_func": lambda r: 1.0 - 2.0 / r,
        "n": 2,
    }


def fixture_sr():
    def x_term(beta): return beta * beta
    def R_func(beta): return (1.0 - beta * beta) ** 0.5
    return {
        "name": "sr",
        "native_var": "beta",
        "grid": sr_beta_grid(),
        "sterbenz_predicate": lambda beta: beta <= 1.0 / math.sqrt(2.0),
        "boundary": "beta <= 1/sqrt(2) (Sterbenz: R^2 = 1 - beta^2 >= 1/2)",
        "x_term": x_term,
        "R_func": R_func,
        "f_func": lambda beta: 1.0 - beta * beta,
        "n": 2,
    }


def fixture_pure_algebraic():
    def x_term(x): return float(x)
    def R_func(x): return (1.0 - float(x)) ** 0.5
    return {
        "name": "pure_algebraic",
        "native_var": "x",
        "grid": pa_x_grid(),
        "sterbenz_predicate": lambda x: x <= 0.5,
        "boundary": "x <= 0.5 (Sterbenz: R^2 = 1 - x >= 1/2)",
        "x_term": x_term,
        "R_func": R_func,
        "f_func": lambda x: 1.0 - float(x),
        "n": 2,
    }


def fixture_cube_root():
    def x_term(x): return float(x)
    def R_func(x):
        # Use np.cbrt to match V4's cube-root computation
        import numpy as np
        return float(np.cbrt(1.0 - float(x)))
    return {
        "name": "cube_root",
        "native_var": "x",
        "grid": pa_x_grid(),
        "sterbenz_predicate": lambda x: x <= 0.5,
        "boundary": "x <= 0.5 (Sterbenz: R^3 = 1 - x >= 1/2)",
        "x_term": x_term,
        "R_func": R_func,
        "f_func": lambda x: 1.0 - float(x),
        "n": 3,
    }


def compute_candidates(fixture, var_value):
    """Compute c1 and c2 for one fixture at one grid point."""
    R = fixture["R_func"](var_value)
    xt = fixture["x_term"](var_value)
    n = fixture["n"]

    # R^n via repeated multiplication (matches the audit's "R*R" pattern)
    R_n = R
    for _ in range(n - 1):
        R_n = R_n * R

    c1 = R_n - 1.0 + xt
    c2 = R_n + (xt - 1.0)
    return c1, c2, R_n, xt


def classify_lattice(levels):
    """Classify lattice character from list of lattice levels."""
    nonzero_levels = [L for L in levels if L != 0.0]
    if not nonzero_levels:
        return {
            "class": "silent",
            "nonzero_count": 0,
            "unique_levels": [],
            "fractional_parts": [],
            "max_abs_level": 0.0,
        }

    # Fractional parts (always in [0, 1))
    fractional_parts = sorted({(L - math.floor(L)) for L in nonzero_levels})
    # Normalize to canonical fractions
    canonical_fracs = []
    for fp in fractional_parts:
        # Round to nearest 0.25 increment for classification
        for candidate in (0.0, 0.25, 0.5, 0.75):
            if abs(fp - candidate) < 1e-9 or abs(fp - 1.0 - candidate) < 1e-9:
                canonical_fracs.append(candidate)
                break
        else:
            # Doesn't match standard fractional pattern
            canonical_fracs.append(fp)

    canonical_set = sorted(set(canonical_fracs))

    if canonical_set == [0.0]:
        klass = "integer"
    elif set(canonical_set).issubset({0.0, 0.5}) and 0.5 in canonical_set:
        klass = "half_integer"
    elif set(canonical_set).issubset({0.0, 0.25, 0.5, 0.75}) and (0.25 in canonical_set or 0.75 in canonical_set):
        klass = "quarter_integer"
    else:
        klass = "irregular"

    return {
        "class": klass,
        "nonzero_count": len(nonzero_levels),
        "unique_levels": sorted(set(nonzero_levels)),
        "fractional_parts": canonical_set,
        "max_abs_level": max(abs(L) for L in nonzero_levels),
    }


LATTICE_ORDER = {"integer": 0, "half_integer": 1, "quarter_integer": 2, "irregular": 3, "silent": -1}


def audit_fixture(fixture):
    """Run the c1 vs c2 lattice-class audit on one fixture."""
    grid = fixture["grid"]
    sterbenz_grid = [v for v in grid if fixture["sterbenz_predicate"](v)]

    records = []
    c1_levels = []
    c2_levels = []
    for v in sterbenz_grid:
        c1, c2, R_n, xt = compute_candidates(fixture, v)
        f = fixture["f_func"](v)
        unit = ulp_of_double(f) if f != 0.0 else 0.0
        L1 = c1 / unit if unit != 0.0 else 0.0
        L2 = c2 / unit if unit != 0.0 else 0.0
        records.append({
            "native_value": float(v),
            "f": f,
            "ulp_f": unit,
            "c1_residual": c1,
            "c2_residual": c2,
            "c1_lattice_level": L1,
            "c2_lattice_level": L2,
        })
        c1_levels.append(L1)
        c2_levels.append(L2)

    c1_classification = classify_lattice(c1_levels)
    c2_classification = classify_lattice(c2_levels)

    # Dominance verdict
    c1_rank = LATTICE_ORDER[c1_classification["class"]]
    c2_rank = LATTICE_ORDER[c2_classification["class"]]
    if c2_classification["class"] == "silent" or c1_classification["class"] == "silent":
        dominance = "either_silent"
    elif c2_rank < c1_rank:
        dominance = "c2_dominates_c1_on_lattice"
    elif c1_rank < c2_rank:
        dominance = "c1_dominates_c2_on_lattice"
    else:
        dominance = "tied_on_lattice"

    return {
        "fixture_name": fixture["name"],
        "native_var": fixture["native_var"],
        "sterbenz_region_predicate": fixture["boundary"],
        "n_radical": fixture["n"],
        "sterbenz_region_grid_size": len(sterbenz_grid),
        "c1_classification": c1_classification,
        "c2_classification": c2_classification,
        "dominance_verdict": dominance,
        "records_sample": records[:5] + records[-5:] if len(records) > 10 else records,
    }


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    fixtures = [
        fixture_schwarzschild(),
        fixture_sr(),
        fixture_pure_algebraic(),
        fixture_cube_root(),
    ]
    results = [audit_fixture(f) for f in fixtures]

    # Strong-prediction verdict
    all_c2_integer = all(r["c2_classification"]["class"] == "integer" for r in results)
    all_c1_nonzero_nonint = all(
        r["c1_classification"]["class"] in ("half_integer", "quarter_integer")
        for r in results
    )
    all_c2_dominates = all(r["dominance_verdict"] == "c2_dominates_c1_on_lattice" for r in results)
    strong_prediction_held = all_c2_integer and all_c1_nonzero_nonint and all_c2_dominates

    artifact = {
        "audit_name": "task032_cross_fixture_refinery_audit",
        "preregistry": "Build_Docs/Reports/task032_cross_fixture_refinery_audit/preregistry.md",
        "frozen_prediction": "strong: c2 integer lattice in all 4 fixtures, c1 non-integer in all 4, c2 dominates c1 on lattice class everywhere",
        "strong_prediction_held": strong_prediction_held,
        "per_fixture_results": results,
        "summary_table": [
            {
                "fixture": r["fixture_name"],
                "n_grid": r["sterbenz_region_grid_size"],
                "c1_lattice_class": r["c1_classification"]["class"],
                "c1_nonzero_count": r["c1_classification"]["nonzero_count"],
                "c1_fracs": r["c1_classification"]["fractional_parts"],
                "c2_lattice_class": r["c2_classification"]["class"],
                "c2_nonzero_count": r["c2_classification"]["nonzero_count"],
                "c2_fracs": r["c2_classification"]["fractional_parts"],
                "verdict": r["dominance_verdict"],
            }
            for r in results
        ],
    }

    ARTIFACT.write_text(json.dumps(artifact, default=float, indent=2, sort_keys=True))
    print(f"Artifact written to {ARTIFACT}")
    print()
    print(f"=== Per-fixture summary ===")
    print(f"{'fixture':<18} {'n_grid':<8} {'c1_class':<18} {'c1_nz':<6} {'c2_class':<18} {'c2_nz':<6} {'verdict':<30}")
    print("-" * 110)
    for row in artifact["summary_table"]:
        print(f"{row['fixture']:<18} {row['n_grid']:<8} {row['c1_lattice_class']:<18} {row['c1_nonzero_count']:<6} {row['c2_lattice_class']:<18} {row['c2_nonzero_count']:<6} {row['verdict']:<30}")
    print()
    print(f"=== Strong prediction held? {strong_prediction_held} ===")
    if not strong_prediction_held:
        print(f"  c2 integer in all: {all_c2_integer}")
        print(f"  c1 non-int in all: {all_c1_nonzero_nonint}")
        print(f"  c2 dominates everywhere: {all_c2_dominates}")


if __name__ == "__main__":
    main()
