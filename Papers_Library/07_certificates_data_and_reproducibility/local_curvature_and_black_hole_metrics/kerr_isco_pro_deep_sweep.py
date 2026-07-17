"""Deep sweep of Kerr ISCO_prograde near extremality.

Extends scratch/kerr_extremal_alpha_recovery.py's isco_pro probe to small
delta = 1 - a, to confirm that the recovered alpha converges to the
asymptotic prediction 1/3.

Precision consideration: at delta near 1e-16 or smaller, computing
  1 - a^2  via  1 - (1-delta)^2
loses precision because 1 - a^2 is below machine epsilon relative to 1.
We compute 1 - a^2 = 2*delta - delta^2 directly to maintain precision.

Two formulations are compared:
  isco_pro_naive  : direct BPT formula with 1 - (1-delta)**2
  isco_pro_stable : same formula but with 2*delta - delta**2 explicit
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from lloyd_v4.primitives.directional_alpha_probe import (
    DeclaredAlphaModel,
    directional_alpha_probe,
)


def kerr_z1_naive(a: float) -> float:
    """Z1 with 1 - a*a computation (precision loss for a near 1)."""
    one_minus_a2 = 1.0 - a * a
    return 1.0 + one_minus_a2 ** (1.0 / 3.0) * (
        (1.0 + a) ** (1.0 / 3.0) + (1.0 - a) ** (1.0 / 3.0)
    )


def kerr_z1_stable(a: float, delta: float) -> float:
    """Z1 with 1 - a^2 = 2*delta - delta^2 (precision preserved)."""
    one_minus_a2 = 2.0 * delta - delta * delta  # exact in float64 for delta in our range
    return 1.0 + one_minus_a2 ** (1.0 / 3.0) * (
        (1.0 + a) ** (1.0 / 3.0) + delta ** (1.0 / 3.0)
    )


def kerr_isco_pro_naive(a: float) -> float:
    z1 = kerr_z1_naive(a)
    z2 = math.sqrt(3.0 * a * a + z1 * z1)
    return 3.0 + z2 - math.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))


def kerr_isco_pro_stable(delta: float) -> float:
    """ISCO prograde with precision-preserving (1-a^2) computation."""
    a = 1.0 - delta
    z1 = kerr_z1_stable(a, delta)
    z2 = math.sqrt(3.0 * a * a + z1 * z1)
    return 3.0 + z2 - math.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))


def isco_pro_naive_obs(delta: float) -> float:
    if delta <= 0 or delta >= 2:
        raise ValueError("delta out of range")
    return kerr_isco_pro_naive(1.0 - delta) - 1.0


def isco_pro_stable_obs(delta: float) -> float:
    if delta <= 0 or delta >= 2:
        raise ValueError("delta out of range")
    return kerr_isco_pro_stable(delta) - 1.0


# Three sweep ranges to see asymptotic behaviour
SWEEPS = {
    "shallow": (1e-2, 1e-9, 20),    # original range
    "medium":  (1e-5, 1e-13, 25),   # deeper
    "deep":    (1e-8, 1e-18, 30),   # very deep -- tests precision limits
}

ETA = 1e-4

DECLARED_MODELS = (
    DeclaredAlphaModel(name="third_exponent", alpha=1.0 / 3.0, band=0.04),
    DeclaredAlphaModel(name="half_exponent",  alpha=0.5,       band=0.04),
    DeclaredAlphaModel(name="two_thirds",     alpha=2.0 / 3.0, band=0.04),
)


def build_grid(start: float, end: float, n: int) -> tuple[float, ...]:
    ls, le = math.log10(start), math.log10(end)
    return tuple(10.0 ** (ls + (le - ls) * i / (n - 1)) for i in range(n))


def probe(label: str, observable, grid: tuple[float, ...]) -> dict:
    r = directional_alpha_probe(
        observable, grid,
        probe_id=f"deep_{label}",
        function_label=f"deep_{label}",
        eta=ETA,
        declared_alpha_models=DECLARED_MODELS,
        expression_path=f"deep_{label}_chain",
        companion_sweep_signature=True,
    )
    a = r.value
    c_obs = a.companion_sweep_signature_observation
    c_st = a.companion_sweep_signature_status
    return {
        "label": label,
        "alpha_status": r.status.value,
        "observed_alpha": a.observed_alpha,
        "alpha_se": a.standard_error,
        "r_squared": a.r_squared,
        "stability": a.alpha_stability_status.value,
        "window_span": a.alpha_window_span,
        "selected_model": a.selected_alpha_model,
        "n_observed": a.n_observed,
        "n_input": a.n_input_observations,
        "sweep_status": c_st.value if c_st else None,
        "sweep_cancel": c_obs.cancellation_grade if c_obs else None,
        "sweep_drop": c_obs.drop_rate if c_obs else None,
    }


def main() -> None:
    print("=" * 95)
    print("Kerr ISCO_prograde deep sweep: testing asymptotic alpha -> 1/3")
    print("=" * 95)
    print(f"Predicted leading coefficient: 2^(2/3) = {2.0**(2.0/3.0):.6f}")
    print()

    # Sanity: compare naive vs stable formulations at small delta
    print("Naive vs stable observable values:")
    print(f"{'delta':>14} {'naive g':>22} {'stable g':>22} {'rel_diff':>12}")
    for delta in [1e-2, 1e-6, 1e-10, 1e-14, 1e-16, 1e-18]:
        try:
            gn = isco_pro_naive_obs(delta)
            gs = isco_pro_stable_obs(delta)
            rel = abs(gn - gs) / max(abs(gs), 1e-300)
            print(f"{delta:>14.2e} {gn:>22.12e} {gs:>22.12e} {rel:>12.3e}")
        except Exception as exc:
            print(f"{delta:>14.2e}  exception: {exc}")
    print()

    results = []
    for sweep_label, (start, end, n) in SWEEPS.items():
        grid = build_grid(start, end, n)
        print(f"\n--- {sweep_label} sweep: delta in [{start:.0e}, {end:.0e}], {n} points ---")
        for form_label, obs in [("naive", isco_pro_naive_obs), ("stable", isco_pro_stable_obs)]:
            label = f"{sweep_label}_{form_label}"
            r = probe(label, obs, grid)
            results.append(r)
            print(f"  {form_label:8s}: alpha = {r['observed_alpha']:.6f} +- {r['alpha_se']:.3e}  "
                  f"status={r['alpha_status']:30s}  sweep={r['sweep_status']}")
            print(f"            window_span={r['window_span']:.3e}  "
                  f"r_squared={r['r_squared']:.6f}  selected={r['selected_model']}")

    # Summary table
    print()
    print("=" * 95)
    print("ASYMPTOTIC TREND")
    print("=" * 95)
    print(f"  Predicted asymptote: alpha = 1/3 ~= 0.333333")
    print()
    print(f"  {'range':12s} {'form':8s} {'alpha':>10s} {'se':>10s} {'span':>10s} {'matched':12s}")
    for r in results:
        sweep_label, form_label = r['label'].rsplit('_', 1)
        match = "third" if r['selected_model'] == 'third_exponent' else (r['selected_model'] or "none")
        print(f"  {sweep_label:12s} {form_label:8s} {r['observed_alpha']:>10.6f} "
              f"{r['alpha_se']:>10.3e} {r['window_span']:>10.3e} {match:12s}")

    out_path = Path(__file__).parent / "kerr_isco_pro_deep_sweep_results.json"
    with out_path.open("w") as fh:
        json.dump({"results": results}, fh, indent=2)
    print(f"\nResults: {out_path}")


if __name__ == "__main__":
    main()
