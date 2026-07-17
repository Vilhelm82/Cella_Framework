"""Cleaner pathological formulation for the ISCO outer-deviation observable.

The original outer_pathological in isco_alpha_recovery_extended.py used a
two-cancellation chain via ((12+eps)^2 - 144 - eps^2)/2.  Pedagogically
elaborate.

This script tests a simpler pathological form using the difference-of-squares
identity:
    r_+ - 6 = (r_+^2 - 36) / (r_+ + 6)

In exact arithmetic this equals the stable form (eps + L*sqrt(eps))/2.
In float64 it introduces exactly ONE catastrophic cancellation at the
r_+^2 - 36 step, where two large nearly-equal numbers are subtracted.

Same true answer as the stable form (~sqrt(3)*sqrt(eps) for small eps,
so alpha = 1/2).  Same predicted failure mode (alpha_unstable_window +
sweep_signature_cancellation_dominated).  Cleaner to explain.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from lloyd_v4.primitives.directional_alpha_probe import (
    DeclaredAlphaModel,
    directional_alpha_probe,
)


def outer_stable(eps: float) -> float:
    if eps <= 0:
        raise ValueError("eps must be positive")
    L = math.sqrt(12.0 + eps)
    return (eps + L * math.sqrt(eps)) / 2.0


def outer_pathological_clean(eps: float) -> float:
    """r_+ - 6 via r_+^2 - 36 path.  One catastrophic cancellation."""
    if eps <= 0:
        raise ValueError("eps must be positive")
    L_sq = 12.0 + eps
    L = math.sqrt(L_sq)
    r_plus = (L_sq + L * math.sqrt(eps)) / 2.0
    return (r_plus * r_plus - 36.0) / (r_plus + 6.0)


# -- numerical comparison --------------------------------------------------

def trace_comparison() -> None:
    print("Comparison: stable vs pathological_clean")
    print(f"{'eps':>12} {'stable g':>22} {'patho_clean g':>22} {'rel_err':>12}")
    for eps in [1e-2, 1e-6, 1e-10, 1e-12, 1e-14, 1e-15]:
        gs = outer_stable(eps)
        gp = outer_pathological_clean(eps)
        rel = abs(gp - gs) / max(abs(gs), 1e-300)
        print(f"{eps:>12.2e} {gs:>22.15e} {gp:>22.15e} {rel:>12.3e}")
    print()


# -- V4 probe --------------------------------------------------------------

N_POINTS = 20
EPS_START = 1e-2
EPS_END = 1e-15
ETA = 1e-4

log_start = math.log10(EPS_START)
log_end = math.log10(EPS_END)
EPS_GRID = tuple(
    10.0 ** (log_start + (log_end - log_start) * i / (N_POINTS - 1))
    for i in range(N_POINTS)
)

DECLARED_MODELS = (
    DeclaredAlphaModel(name="isco_half_exponent", alpha=0.5, band=0.05),
    DeclaredAlphaModel(name="regular_linear", alpha=1.0, band=0.05),
)


def probe(label, observable):
    r = directional_alpha_probe(
        observable, EPS_GRID,
        probe_id=label, function_label=label,
        eta=ETA, declared_alpha_models=DECLARED_MODELS,
        expression_path=f"{label}_chain",
        companion_sweep_signature=True,
    )
    a = r.value
    c = a.companion_sweep_signature_observation
    cs = a.companion_sweep_signature_status
    return {
        "label": label,
        "alpha_status": r.status.value,
        "observed_alpha": a.observed_alpha,
        "alpha_se": a.standard_error,
        "r_squared": a.r_squared,
        "stability": a.alpha_stability_status.value,
        "window_span": a.alpha_window_span,
        "selected_model": a.selected_alpha_model,
        "sweep_status": cs.value if cs else None,
        "sweep_cancel": c.cancellation_grade if c else None,
        "sweep_drop": c.drop_rate if c else None,
    }


def main():
    print("=" * 88)
    print("Cleaner pathological ISCO formulation: r_+^2 - 36 cancellation path")
    print("=" * 88)
    print()
    trace_comparison()

    results = []
    for label, obs in [("outer_stable", outer_stable), ("outer_pathological_clean", outer_pathological_clean)]:
        r = probe(label, obs)
        results.append(r)
        print(f"  {label}")
        print(f"    alpha           : {r['observed_alpha']:.6f}  +- {r['alpha_se']:.3e}")
        print(f"    alpha status    : {r['alpha_status']}")
        print(f"    selected_model  : {r['selected_model']}")
        print(f"    stability       : {r['stability']}  (window span = {r['window_span']:.3e})")
        if r['r_squared'] is not None:
            print(f"    r_squared       : {r['r_squared']:.6f}")
        sc = r['sweep_cancel']
        sc_s = f"{sc:.4f}" if sc is not None else "None"
        print(f"    sweep status    : {r['sweep_status']}  (cancel_grade={sc_s})")
        print()

    out_path = Path(__file__).parent / "isco_pathological_cleaner_results.json"
    with out_path.open("w") as fh:
        json.dump({"results": results}, fh, indent=2)
    print(f"Results: {out_path}")


if __name__ == "__main__":
    main()
