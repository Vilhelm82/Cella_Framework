"""ISCO alpha-recovery probe -- extended, using task036 companion integration.

Same physics as isco_alpha_recovery_extended.py, but exercising the actual
task036 companion-call API: directional_alpha_probe(..., companion_sweep_signature=True)
returns an AlphaProbeObservation with companion_sweep_signature_{observation,status,trace_id}
populated. One call per observable instead of two.

OBSERVABLES (eps = L^2 - 12, M = 1):
  outer_deviation:  r_+ - 6  ~  sqrt(3) * sqrt(eps)
  inner_deviation:  6 - r_-  ~  sqrt(3) * sqrt(eps)
  orbit_splitting:  r_+ - r_-  ~  2*sqrt(3) * sqrt(eps)

Plus one deliberately pathological form to verify V4 catches catastrophic cancellation
via the joint evidence pattern (alpha_unstable_window + sweep_signature_cancellation_dominated).
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


# ---------------------------------------------------------------------------
# Outer deviation r_+ - 6
# ---------------------------------------------------------------------------

def outer_stable(eps: float) -> float:
    if eps <= 0:
        raise ValueError("eps must be positive")
    L = math.sqrt(12.0 + eps)
    return (eps + L * math.sqrt(eps)) / 2.0


def outer_naive(eps: float) -> float:
    if eps <= 0:
        raise ValueError("eps must be positive")
    L_sq = 12.0 + eps
    L = math.sqrt(L_sq)
    r_plus = (L_sq + L * math.sqrt(eps)) / 2.0
    return r_plus - 6.0


def outer_pathological(eps: float) -> float:
    """Computes sqrt(eps^2 + 12*eps) via (12+eps)^2 - 144 - eps^2 chain.
    The (12+eps)^2 - 144 step is catastrophic at small eps."""
    if eps <= 0:
        raise ValueError("eps must be positive")
    twelve_plus_eps = 12.0 + eps
    expanded = twelve_plus_eps * twelve_plus_eps
    expanded_minus_144 = expanded - 144.0  # cancellation
    inner = expanded_minus_144 - eps * eps
    inner_corrected = inner / 2.0
    if inner_corrected <= 0:
        return 0.0
    return (eps + math.sqrt(inner_corrected)) / 2.0


# ---------------------------------------------------------------------------
# Inner deviation 6 - r_-
# ---------------------------------------------------------------------------

def inner_stable(eps: float) -> float:
    if eps <= 0:
        raise ValueError("eps must be positive")
    L = math.sqrt(12.0 + eps)
    return (L * math.sqrt(eps) - eps) / 2.0


def inner_naive(eps: float) -> float:
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
    if eps <= 0:
        raise ValueError("eps must be positive")
    L = math.sqrt(12.0 + eps)
    return L * math.sqrt(eps)


def splitting_naive(eps: float) -> float:
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
    """Single alpha_probe call with companion=True; extract joint evidence from one result."""
    result = directional_alpha_probe(
        observable, EPS_GRID,
        probe_id=f"isco_{label}",
        function_label=f"isco_{label}",
        eta=ETA,
        declared_alpha_models=DECLARED_MODELS,
        expression_path=f"isco_{label}_chain",
        companion_sweep_signature=True,
    )
    a = result.value
    companion_obs = a.companion_sweep_signature_observation
    companion_status = a.companion_sweep_signature_status

    return {
        "label": label,
        "alpha_status": result.status.value,
        "observed_alpha": a.observed_alpha,
        "alpha_standard_error": a.standard_error,
        "alpha_r_squared": a.r_squared,
        "alpha_stability": a.alpha_stability_status.value,
        "alpha_window_span": a.alpha_window_span,
        "selected_model": a.selected_alpha_model,
        "n_alpha_observed": a.n_observed,
        "n_alpha_input": a.n_input_observations,
        "n_alpha_cancellation": a.n_cancellation_dominated,
        # Companion evidence from task036 integration
        "sweep_status": companion_status.value if companion_status else None,
        "sweep_cancellation_grade": companion_obs.cancellation_grade if companion_obs else None,
        "sweep_drop_rate": companion_obs.drop_rate if companion_obs else None,
        "sweep_r_squared": companion_obs.slope_observation.r_squared if companion_obs else None,
        "sweep_n_observed": companion_obs.n_observed if companion_obs else None,
        "sweep_trace_id": a.companion_sweep_signature_trace_id,
        "primary_trace_id": result.provenance.trace_id,
    }


def fmt_alpha(v: float | None) -> str:
    return f"{v:.6f}" if v is not None else "  None  "


def fmt_se(v: float | None) -> str:
    return f"{v:.2e}" if v is not None else "  None  "


def main() -> None:
    print("=" * 92)
    print("ISCO alpha-recovery via task036 companion integration")
    print("=" * 92)
    print(f"Grid: {N_POINTS} log-spaced points, eps in [{EPS_START:.0e}, {EPS_END:.0e}]")
    print(f"Eta:  {ETA:.0e}")
    print(f"Predicted alpha: 0.5 (saddle-node bifurcation)")
    print(f"Single API call per observable: directional_alpha_probe(..., companion_sweep_signature=True)")
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

    results = []
    print(f"{'observable':22s} {'alpha':>10s} {'se':>9s} {'alpha_status':30s} {'companion_status':35s}")
    print("-" * 110)
    for label, obs in observables:
        r = probe_one(label, obs)
        results.append(r)
        print(f"{label:22s} {fmt_alpha(r['observed_alpha']):>10s} "
              f"{fmt_se(r['alpha_standard_error']):>9s} "
              f"{r['alpha_status']:30s} {(r['sweep_status'] or 'None'):35s}")

    print()
    print("=" * 92)
    print("TRACE VERIFICATION")
    print("=" * 92)
    print("Companion trace IDs distinct from primary trace IDs:")
    for r in results[:3]:
        print(f"  {r['label']:22s}")
        print(f"    primary  : {r['primary_trace_id']}")
        print(f"    companion: {r['sweep_trace_id']}")
        print(f"    distinct : {r['primary_trace_id'] != r['sweep_trace_id']}")

    print()
    print("=" * 92)
    print("DETAILED")
    print("=" * 92)
    for r in results:
        print(f"\n  {r['label']}")
        print(f"    alpha           : {fmt_alpha(r['observed_alpha'])}  +- {fmt_se(r['alpha_standard_error'])}")
        print(f"    alpha status    : {r['alpha_status']}")
        print(f"    selected_model  : {r['selected_model']}")
        print(f"    nested_stability: {r['alpha_stability']}  (window span = {fmt_se(r['alpha_window_span'])})")
        scg = r['sweep_cancellation_grade']
        scg_s = f"{scg:.4f}" if scg is not None else "None"
        sdr = r['sweep_drop_rate']
        sdr_s = f"{sdr:.4f}" if sdr is not None else "None"
        print(f"    companion_status: {r['sweep_status']}")
        print(f"    cancel_grade    : {scg_s}    drop_rate: {sdr_s}")

    print()
    print("=" * 92)
    print("JOINT VERDICT (task036 patterns)")
    print("=" * 92)
    for r in results:
        alpha_s = r['alpha_status']
        sweep_s = r['sweep_status']
        if alpha_s in ('alpha_regular_integer', 'alpha_fractional_branch') and sweep_s == 'sweep_signature_clean':
            verdict = "WELL-CHARACTERIZED (alpha meaningful, formulation clean)"
        elif alpha_s == 'alpha_unstable_window' and sweep_s == 'sweep_signature_cancellation_dominated':
            verdict = "FORMULATION-BURDENED (instability is formulation, not structure)"
        elif alpha_s == 'alpha_unstable_window' and sweep_s == 'sweep_signature_clean':
            verdict = "STRUCTURALLY-UNSTABLE (or sub-threshold formulation)"
        elif alpha_s == 'alpha_cancellation_dominated' and sweep_s == 'sweep_signature_cancellation_dominated':
            verdict = "CONCURRENT CANCELLATION (both probes agree formulation rotten)"
        else:
            verdict = f"({alpha_s} + {sweep_s})"
        print(f"  {r['label']:22s} -> {verdict}")

    out_path = Path(__file__).parent / "isco_alpha_recovery_task036_results.json"
    with out_path.open("w") as fh:
        json.dump(
            {
                "config": {
                    "n_points": N_POINTS, "eps_start": EPS_START, "eps_end": EPS_END,
                    "eta": ETA, "predicted_alpha": 0.5, "predicted_coefficient": math.sqrt(3.0),
                    "api": "directional_alpha_probe(..., companion_sweep_signature=True)",
                    "grid": list(EPS_GRID),
                },
                "results": results,
            }, fh, indent=2,
        )
    print(f"\nResults: {out_path}")


if __name__ == "__main__":
    main()
