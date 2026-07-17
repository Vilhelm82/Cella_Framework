"""ISCO alpha-recovery probe -- extended.

Three observables, three forms each, probing the alpha = 1/2 prediction of
the Schwarzschild ISCO saddle-node bifurcation.

OBSERVABLES (eps = L^2 - 12, M = 1):
  outer_deviation:  r_+ - 6  ~  sqrt(3) * sqrt(eps)
  inner_deviation:  6 - r_-  ~  sqrt(3) * sqrt(eps)
  orbit_splitting:  r_+ - r_-  ~  2*sqrt(3) * sqrt(eps)

FORMS:
  stable: algebraically reduced, no spurious subtractions.
  naive:  compute r_+ or r_- first, then subtract the reference.
  pathological: deliberately introduce a catastrophic-cancellation chain
                via the quartic form  r^4 - L^2*r^3 + 3*L^2*r^2 vanishing
                at the orbit -- evaluated at r = 6 + g, then divided through.

  The pathological form is a stress test: we expect alpha_probe + sweep
  to register catastrophic cancellation, NOT to recover alpha = 0.5
  cleanly. If V4 catches it, that's a positive result.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Callable

from lloyd_v4.primitives.directional_alpha_probe import (
    DeclaredAlphaModel,
    directional_alpha_probe,
)
from lloyd_v4.primitives.sweep_signature_probe import sweep_signature_probe


# ---------------------------------------------------------------------------
# Outer deviation r_+ - 6
# ---------------------------------------------------------------------------

def outer_stable(eps: float) -> float:
    """r_+ - 6 via algebraic simplification."""
    if eps <= 0:
        raise ValueError("eps must be positive")
    L = math.sqrt(12.0 + eps)
    return (eps + L * math.sqrt(eps)) / 2.0


def outer_naive(eps: float) -> float:
    """r_+ - 6 via direct r_+ computation."""
    if eps <= 0:
        raise ValueError("eps must be positive")
    L_sq = 12.0 + eps
    L = math.sqrt(L_sq)
    r_plus = (L_sq + L * math.sqrt(eps)) / 2.0
    return r_plus - 6.0


def outer_pathological(eps: float) -> float:
    """r_+ - 6 via deliberately catastrophic-cancellation chain.

    Strategy: evaluate the orbit polynomial P(r) = r^2 - L^2*r + 3*L^2
    at r = 6 + g and at r = 6, then solve for g via the linear correction:

        P(6 + g) ~= P(6) + P'(6) * g
        =>   g  ~= -P(6) / P'(6)

    This produces a cancellation between two large quantities P(6+g)
    and P(6) when g is small. The actual orbit is at g_true = r_+ - 6,
    so this should recover g_true to leading order for small eps,
    but with floor-of-cancellation precision.

    P(r) = r^2 - L^2*r + 3*L^2
    P(6) = 36 - 6*L^2 + 3*L^2 = 36 - 3*L^2 = 36 - 3*(12+eps) = -3*eps
    P'(r) = 2r - L^2
    P'(6) = 12 - L^2 = -eps

    So the linear estimate gives:
        g_lin = -P(6) / P'(6) = 3*eps / eps = 3  (NOT the right answer)

    The linear estimate fails because both numerator and denominator vanish
    at ISCO; the proper recovery needs the second derivative. To get the
    leading sqrt(eps) we need:

        P(6 + g) = P(6) + P'(6)*g + 0.5*P''(6)*g^2
                 = -3*eps - eps*g + 0.5*2*g^2
                 = -3*eps - eps*g + g^2

    Setting = 0:  g^2 - eps*g - 3*eps = 0
                   g = (eps + sqrt(eps^2 + 12*eps)) / 2

    For small eps:  g ~= sqrt(12*eps)/2 = sqrt(3) * sqrt(eps).  Correct.

    The PATHOLOGICAL evaluation: compute eps^2 + 12*eps, take its sqrt,
    add eps, divide by 2. The eps^2 + 12*eps subexpression has clean
    sum for small eps, but if we instead compute it as
    (12 + eps)*eps - 12*eps + 12*eps with rearrangement, we get
    cancellation.

    We use:  inner = (12.0 * eps + eps * eps + (eps - eps)) -- which
    after the spurious zero subtraction still yields the right value
    in infinite precision but is unstable.

    Actually let's be more direct: compute eps^2 + 12*eps as
    ((12 + eps)*(12 + eps) - 144 - eps*eps) / 1 == 24*eps + 2*eps^2 - eps^2
    which involves catastrophic cancellation of the 144 term.
    """
    if eps <= 0:
        raise ValueError("eps must be positive")
    # Compute eps^2 + 12*eps via catastrophic-cancellation chain.
    # eps^2 + 12*eps == (12 + eps)^2 - 144 - eps^2
    # The (12 + eps)^2 - 144 has cancellation for small eps.
    twelve_plus_eps = 12.0 + eps
    expanded = twelve_plus_eps * twelve_plus_eps  # ~144 + 24*eps + eps^2
    expanded_minus_144 = expanded - 144.0  # CANCELLATION: ~24*eps + eps^2
    inner = expanded_minus_144 - eps * eps  # ~24*eps; we want eps^2 + 12*eps, not 24*eps
    # Wait -- this gives us 24*eps + eps^2 - eps^2 = 24*eps. We want eps^2 + 12*eps.
    # Correct it: divide by 2.
    inner_corrected = inner / 2.0  # ~12*eps + eps^2/2, off by eps^2/2 from true value
    # For small eps, eps^2/2 is negligible vs 12*eps; leading behaviour correct.
    # The PATHOLOGY is the (expanded - 144) catastrophic cancellation at the inner step.
    if inner_corrected <= 0:
        # If catastrophic cancellation flips sign or zeros it out, return 0 -> dropout
        return 0.0
    return (eps + math.sqrt(inner_corrected)) / 2.0


# ---------------------------------------------------------------------------
# Inner deviation 6 - r_-
# ---------------------------------------------------------------------------

def inner_stable(eps: float) -> float:
    """6 - r_- via algebraic simplification.

    r_- = (L^2 - L*sqrt(eps)) / 2,  L = sqrt(12 + eps)
    6 - r_- = 6 - (L^2 - L*sqrt(eps))/2 = (12 - L^2 + L*sqrt(eps))/2
            = (-eps + L*sqrt(eps))/2 = (L*sqrt(eps) - eps)/2

    For small eps:  6 - r_- ~ sqrt(3) * sqrt(eps).
    """
    if eps <= 0:
        raise ValueError("eps must be positive")
    L = math.sqrt(12.0 + eps)
    return (L * math.sqrt(eps) - eps) / 2.0


def inner_naive(eps: float) -> float:
    """6 - r_- via direct r_- computation."""
    if eps <= 0:
        raise ValueError("eps must be positive")
    L_sq = 12.0 + eps
    L = math.sqrt(L_sq)
    r_minus = (L_sq - L * math.sqrt(eps)) / 2.0
    return 6.0 - r_minus


# ---------------------------------------------------------------------------
# Orbit splitting r_+ - r_-
# ---------------------------------------------------------------------------

def splitting_stable(eps: float) -> float:
    """r_+ - r_- = L*sqrt(eps) exactly."""
    if eps <= 0:
        raise ValueError("eps must be positive")
    L = math.sqrt(12.0 + eps)
    return L * math.sqrt(eps)


def splitting_naive(eps: float) -> float:
    """r_+ - r_- via difference of both orbits computed separately."""
    if eps <= 0:
        raise ValueError("eps must be positive")
    L_sq = 12.0 + eps
    L = math.sqrt(L_sq)
    r_plus = (L_sq + L * math.sqrt(eps)) / 2.0
    r_minus = (L_sq - L * math.sqrt(eps)) / 2.0
    return r_plus - r_minus


# ---------------------------------------------------------------------------
# Probe configuration
# ---------------------------------------------------------------------------

N_POINTS = 20
EPS_START = 1e-2
EPS_END = 1e-15

log_start = math.log10(EPS_START)
log_end = math.log10(EPS_END)
EPS_GRID = tuple(
    10.0 ** (log_start + (log_end - log_start) * i / (N_POINTS - 1))
    for i in range(N_POINTS)
)

ETA = 1e-4

DECLARED_MODELS = (
    DeclaredAlphaModel(name="isco_half_exponent", alpha=0.5, band=0.05),
    DeclaredAlphaModel(name="regular_linear", alpha=1.0, band=0.05),
    DeclaredAlphaModel(name="constant", alpha=0.0, band=0.05),
)


def probe_one(label: str, observable: Callable[[float], float]) -> dict:
    """Run alpha_probe + sweep_signature_probe; return summary dict."""
    alpha_result = directional_alpha_probe(
        observable, EPS_GRID,
        probe_id=f"isco_{label}_alpha",
        function_label=f"isco_{label}",
        eta=ETA,
        declared_alpha_models=DECLARED_MODELS,
        expression_path=f"isco_{label}_chain",
    )
    sweep_result = sweep_signature_probe(
        observable, EPS_GRID,
        probe_id=f"isco_{label}_sweep",
        function_label=f"isco_{label}",
        eta=ETA,
    )

    a = alpha_result.value
    s = sweep_result.value if sweep_result.value is not None else None

    return {
        "label": label,
        "alpha_status": alpha_result.status.value,
        "observed_alpha": a.observed_alpha,
        "alpha_standard_error": a.standard_error,
        "alpha_r_squared": a.r_squared,
        "alpha_stability": a.alpha_stability_status.value,
        "alpha_window_span": a.alpha_window_span,
        "selected_model": a.selected_alpha_model,
        "n_alpha_observed": a.n_observed,
        "n_alpha_input": a.n_input_observations,
        "n_alpha_cancellation": a.n_cancellation_dominated,
        "sweep_status": sweep_result.status.value,
        "sweep_cancellation_grade": s.cancellation_grade if s else None,
        "sweep_drop_rate": s.drop_rate if s else None,
        "sweep_r_squared": s.slope_observation.r_squared if s else None,
        "sweep_n_observed": s.n_observed if s else None,
        "sweep_n_dropped": s.n_dropped if s else None,
    }


def fmt_alpha(v: float | None) -> str:
    return f"{v:.6f}" if v is not None else "  None  "


def fmt_se(v: float | None) -> str:
    return f"{v:.2e}" if v is not None else "  None  "


def main() -> None:
    print("=" * 88)
    print("ISCO alpha-recovery -- extended (3 observables x 3 forms)")
    print("=" * 88)
    print(f"Grid: {N_POINTS} log-spaced points, eps in [{EPS_START:.0e}, {EPS_END:.0e}]")
    print(f"Eta:  {ETA:.0e}")
    print(f"Predicted alpha: 0.5 (saddle-node bifurcation, coefficient sqrt(3) ~ 1.7321)")
    print()

    observables = [
        ("outer_stable",        outer_stable),
        ("outer_naive",         outer_naive),
        ("outer_pathological",  outer_pathological),
        ("inner_stable",        inner_stable),
        ("inner_naive",         inner_naive),
        ("splitting_stable",    splitting_stable),
        ("splitting_naive",     splitting_naive),
    ]

    # Sanity check at a few eps values
    print(f"{'eps':>14} {'outer_stable':>16} {'outer_naive':>16} {'outer_path':>16}")
    for eps in [1e-2, 1e-6, 1e-10, 1e-13]:
        try:
            os = outer_stable(eps)
            on = outer_naive(eps)
            op = outer_pathological(eps)
            print(f"{eps:>14.1e} {os:>16.6e} {on:>16.6e} {op:>16.6e}")
        except Exception as exc:
            print(f"{eps:>14.1e}  exception: {exc}")
    print()

    # Run all probes
    results = []
    print(f"{'observable':22s} {'alpha':>10s} {'se':>9s} {'status':30s} {'sweep_status':30s}")
    print("-" * 105)
    for label, obs in observables:
        r = probe_one(label, obs)
        results.append(r)
        print(f"{label:22s} {fmt_alpha(r['observed_alpha']):>10s} "
              f"{fmt_se(r['alpha_standard_error']):>9s} "
              f"{r['alpha_status']:30s} {r['sweep_status']:30s}")

    print()
    print("=" * 88)
    print("DETAILED")
    print("=" * 88)
    for r in results:
        print(f"\n  {r['label']}")
        print(f"    alpha           : {fmt_alpha(r['observed_alpha'])}  +- {fmt_se(r['alpha_standard_error'])}")
        print(f"    alpha status    : {r['alpha_status']}")
        print(f"    selected_model  : {r['selected_model']}")
        print(f"    nested_stability: {r['alpha_stability']}  (window span = {fmt_se(r['alpha_window_span'])})")
        print(f"    r_squared       : {r['alpha_r_squared']:.6f}" if r['alpha_r_squared'] is not None else "    r_squared       : None")
        print(f"    n_observed      : {r['n_alpha_observed']}/{r['n_alpha_input']}  (n_cancellation={r['n_alpha_cancellation']})")
        scg = r['sweep_cancellation_grade']
        scg_s = f"{scg:.4f}" if scg is not None else "None"
        sdr = r['sweep_drop_rate']
        sdr_s = f"{sdr:.4f}" if sdr is not None else "None"
        print(f"    sweep status    : {r['sweep_status']}")
        print(f"    sweep cancel    : {scg_s}    drop_rate: {sdr_s}    n_obs: {r['sweep_n_observed']}")

    # Joint summary
    print()
    print("=" * 88)
    print("JOINT VERDICT")
    print("=" * 88)
    matching_count = sum(1 for r in results if r['selected_model'] == 'isco_half_exponent')
    print(f"  observables matching isco_half_exponent: {matching_count}/{len(results)}")
    print(f"  expected: 6/7 (all stable + naive forms; pathological should fail)")

    out_path = Path(__file__).parent / "isco_alpha_recovery_extended_results.json"
    with out_path.open("w") as fh:
        json.dump(
            {
                "config": {
                    "n_points": N_POINTS, "eps_start": EPS_START, "eps_end": EPS_END,
                    "eta": ETA, "predicted_alpha": 0.5, "predicted_coefficient": math.sqrt(3.0),
                    "grid": list(EPS_GRID),
                },
                "results": results,
            }, fh, indent=2,
        )
    print(f"\nResults: {out_path}")


if __name__ == "__main__":
    main()
