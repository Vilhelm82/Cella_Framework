"""Truly minimal pathological ISCO formulation.

Lesson from the r_+^2 - 36 attempt: a cancellation alone is not enough --
the SIGNAL SCALING AFTER cancellation determines whether the form is
catastrophic.

For r_+ - 6 = sqrt(3)*sqrt(eps) (leading order):
  - O(eps) signal after cancellation -> catastrophic at eps ~ 1e-12
  - O(sqrt(eps)) signal -> still resolvable at eps ~ 1e-15

The minimal pathological path uses (12+eps)^2 - 144 = 24*eps + eps^2,
which is O(eps) and gets destroyed by float64 precision at small eps.
We then divide by sqrt(8) so the leading coefficient matches stable form.

Single cancellation site, single-line core, identical leading coefficient
to outer_stable.
"""

from __future__ import annotations

import math

from lloyd_v4.primitives.directional_alpha_probe import (
    DeclaredAlphaModel,
    directional_alpha_probe,
)


SQRT_8 = math.sqrt(8.0)


def outer_stable(eps: float) -> float:
    if eps <= 0:
        raise ValueError("eps must be positive")
    L = math.sqrt(12.0 + eps)
    return (eps + L * math.sqrt(eps)) / 2.0


def outer_pathological_minimal(eps: float) -> float:
    """r_+ - 6 via (12+eps)^2 - 144 cancellation, single step, no scaffolding.

    Mathematical identity (exact arithmetic):
        sqrt((12+eps)^2 - 144) / sqrt(8) = sqrt(24*eps + eps^2) / sqrt(8)
                                        = sqrt(3*eps + eps^2/8)
                                        ~= sqrt(3)*sqrt(eps)  for small eps

    Same leading coefficient (sqrt(3)) as the stable form.
    The (12+eps)^2 - 144 step is catastrophic: 144 + 24*eps - 144 isolates
    O(eps) signal from O(1) operands. Signal-to-precision ratio degrades
    linearly in eps and breaks down at eps ~ 1e-13.
    """
    if eps <= 0:
        raise ValueError("eps must be positive")
    twelve_plus_eps = 12.0 + eps
    diff = twelve_plus_eps * twelve_plus_eps - 144.0  # CANCELLATION
    if diff <= 0:
        return 0.0
    return math.sqrt(diff) / SQRT_8


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
    }


def main():
    print("=" * 88)
    print("Minimal pathological ISCO: (12+eps)^2 - 144, single cancellation")
    print("=" * 88)
    print()
    print("Sanity check: stable vs minimal pathological")
    print(f"{'eps':>12} {'stable g':>22} {'patho_min g':>22} {'rel_err':>12}")
    for eps in [1e-2, 1e-6, 1e-10, 1e-12, 1e-13, 1e-14, 1e-15]:
        gs = outer_stable(eps)
        gp = outer_pathological_minimal(eps)
        rel = abs(gp - gs) / max(abs(gs), 1e-300)
        print(f"{eps:>12.2e} {gs:>22.15e} {gp:>22.15e} {rel:>12.3e}")
    print()

    for label, obs in [("outer_stable", outer_stable), ("outer_pathological_minimal", outer_pathological_minimal)]:
        r = probe(label, obs)
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


if __name__ == "__main__":
    main()
