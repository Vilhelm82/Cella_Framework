"""Kerr near-extremal alpha-recovery probe.

Tests V4's ability to distinguish DIFFERENT alpha exponents in adjacent GR
observables, all approaching the horizon r = 1 as the spin a -> 1 (extremal).

OBSERVABLES (M = 1, delta = 1 - a):
  isco_pro:   r_ISCO_prograde(a=1-delta) - 1            predicted alpha = 1/3
  photon_pro: r_photon_sphere_pro(a=1-delta) - 1         predicted alpha = 1/2
  horizon:    sqrt(1 - a^2) = sqrt(2*delta - delta^2)   predicted alpha = 1/2 (sanity)
  isco_retro_9: 9 - r_ISCO_retrograde(a=1-delta)        predicted alpha = ? (discovery)

Bardeen-Press-Teukolsky 1972:
  Z1 = 1 + (1 - a^2)^(1/3) * [(1+a)^(1/3) + (1-a)^(1/3)]
  Z2 = sqrt(3*a^2 + Z1^2)
  r_ISCO_pro = 3 + Z2 - sqrt((3-Z1)(3+Z1+2*Z2))
  r_ISCO_retro = 3 + Z2 + sqrt((3-Z1)(3+Z1+2*Z2))

Kerr photon sphere prograde:
  r_ph_pro = 2 * (1 + cos((2/3) * arccos(-a)))
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
# Kerr geodesic structure helpers (M = 1)
# ---------------------------------------------------------------------------

def kerr_z1(a: float) -> float:
    return 1.0 + (1.0 - a * a) ** (1.0 / 3.0) * (
        (1.0 + a) ** (1.0 / 3.0) + (1.0 - a) ** (1.0 / 3.0)
    )


def kerr_z2(a: float, z1: float) -> float:
    return math.sqrt(3.0 * a * a + z1 * z1)


def kerr_isco_prograde(a: float) -> float:
    """r_ISCO for prograde circular orbits, M = 1."""
    z1 = kerr_z1(a)
    z2 = kerr_z2(a, z1)
    return 3.0 + z2 - math.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))


def kerr_isco_retrograde(a: float) -> float:
    """r_ISCO for retrograde circular orbits, M = 1."""
    z1 = kerr_z1(a)
    z2 = kerr_z2(a, z1)
    return 3.0 + z2 + math.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))


def kerr_photon_prograde(a: float) -> float:
    """Prograde photon sphere radius, M = 1."""
    return 2.0 * (1.0 + math.cos((2.0 / 3.0) * math.acos(-a)))


def kerr_outer_horizon(a: float) -> float:
    """Outer event horizon radius, M = 1."""
    return 1.0 + math.sqrt(1.0 - a * a)


# ---------------------------------------------------------------------------
# Observables (sweep variable: delta = 1 - a)
# ---------------------------------------------------------------------------

def isco_pro_approach(delta: float) -> float:
    """g(delta) = r_ISCO_pro(1-delta) - 1.  Predicted alpha = 1/3."""
    if delta <= 0 or delta >= 2:
        raise ValueError("delta out of range")
    return kerr_isco_prograde(1.0 - delta) - 1.0


def photon_pro_approach(delta: float) -> float:
    """g(delta) = r_photon_pro(1-delta) - 1.  Predicted alpha = 1/2."""
    if delta <= 0 or delta >= 2:
        raise ValueError("delta out of range")
    return kerr_photon_prograde(1.0 - delta) - 1.0


def horizon_approach(delta: float) -> float:
    """g(delta) = sqrt(1 - (1-delta)^2).  Predicted alpha = 1/2."""
    if delta <= 0 or delta >= 2:
        raise ValueError("delta out of range")
    a = 1.0 - delta
    return math.sqrt(1.0 - a * a)


def isco_retro_distance(delta: float) -> float:
    """g(delta) = 9 - r_ISCO_retro(1-delta).  Predicted alpha = ? (discovery)."""
    if delta <= 0 or delta >= 2:
        raise ValueError("delta out of range")
    return 9.0 - kerr_isco_retrograde(1.0 - delta)


# ---------------------------------------------------------------------------
# Probe configuration
# ---------------------------------------------------------------------------

N_POINTS = 20
DELTA_START = 1e-2
DELTA_END = 1e-12

log_start = math.log10(DELTA_START)
log_end = math.log10(DELTA_END)
DELTA_GRID = tuple(
    10.0 ** (log_start + (log_end - log_start) * i / (N_POINTS - 1))
    for i in range(N_POINTS)
)

ETA = 1e-4

DECLARED_MODELS = (
    DeclaredAlphaModel(name="third_exponent",   alpha=1.0 / 3.0, band=0.04),
    DeclaredAlphaModel(name="half_exponent",    alpha=0.5,       band=0.04),
    DeclaredAlphaModel(name="two_thirds",       alpha=2.0 / 3.0, band=0.04),
    DeclaredAlphaModel(name="regular_linear",   alpha=1.0,       band=0.04),
)


def probe_one(label: str, observable: Callable[[float], float]) -> dict:
    result = directional_alpha_probe(
        observable, DELTA_GRID,
        probe_id=f"kerr_{label}",
        function_label=f"kerr_{label}",
        eta=ETA,
        declared_alpha_models=DECLARED_MODELS,
        expression_path=f"kerr_{label}_chain",
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
        "matching_models": list(a.matching_alpha_model_names),
        "n_alpha_observed": a.n_observed,
        "n_alpha_input": a.n_input_observations,
        "n_alpha_cancellation": a.n_cancellation_dominated,
        "sweep_status": companion_status.value if companion_status else None,
        "sweep_cancellation_grade": companion_obs.cancellation_grade if companion_obs else None,
        "sweep_drop_rate": companion_obs.drop_rate if companion_obs else None,
        "sweep_r_squared": companion_obs.slope_observation.r_squared if companion_obs else None,
        "sweep_n_observed": companion_obs.n_observed if companion_obs else None,
    }


def fmt_alpha(v: float | None) -> str:
    return f"{v:.6f}" if v is not None else "  None  "


def fmt_se(v: float | None) -> str:
    return f"{v:.2e}" if v is not None else "  None  "


def main() -> None:
    print("=" * 100)
    print("Kerr near-extremal alpha-recovery (four observables, three predicted alphas)")
    print("=" * 100)
    print(f"Grid: {N_POINTS} log-spaced points, delta = 1 - a in [{DELTA_START:.0e}, {DELTA_END:.0e}]")
    print(f"Eta:  {ETA:.0e}")
    print(f"Declared models: third_exponent (0.333), half_exponent (0.5), two_thirds (0.667), regular_linear (1.0)")
    print()

    # Sanity check at a few delta values
    print(f"{'delta':>14} {'isco_pro':>16} {'photon_pro':>16} {'horizon':>16} {'isco_retro_9':>16}")
    for delta in [1e-2, 1e-6, 1e-10, 1e-12]:
        try:
            v1 = isco_pro_approach(delta)
            v2 = photon_pro_approach(delta)
            v3 = horizon_approach(delta)
            v4 = isco_retro_distance(delta)
            print(f"{delta:>14.1e} {v1:>16.6e} {v2:>16.6e} {v3:>16.6e} {v4:>16.6e}")
        except Exception as exc:
            print(f"{delta:>14.1e}  exception: {exc}")
    print()

    # Show predicted coefficients
    print("Predicted leading-order coefficients (for log-log slope intercept comparison):")
    print(f"  isco_pro:    coefficient = 2^(2/3) = {2.0**(2.0/3.0):.6f}      ~> g = {2.0**(2.0/3.0):.4f} * delta^(1/3)")
    print(f"  photon_pro:  coefficient = 2*sqrt(6)/3 = {2.0*math.sqrt(6.0)/3.0:.6f}  ~> g = {2.0*math.sqrt(6.0)/3.0:.4f} * delta^(1/2)")
    print(f"  horizon:     coefficient = sqrt(2) = {math.sqrt(2.0):.6f}           ~> g = {math.sqrt(2.0):.4f} * delta^(1/2)")
    print(f"  isco_retro:  coefficient and alpha both unknown (discovery)")
    print()

    observables = [
        ("isco_pro",        isco_pro_approach),
        ("photon_pro",      photon_pro_approach),
        ("horizon",         horizon_approach),
        ("isco_retro_9",    isco_retro_distance),
    ]

    expected_alpha = {
        "isco_pro":     1.0 / 3.0,
        "photon_pro":   0.5,
        "horizon":      0.5,
        "isco_retro_9": None,
    }
    expected_model = {
        "isco_pro":     "third_exponent",
        "photon_pro":   "half_exponent",
        "horizon":      "half_exponent",
        "isco_retro_9": None,
    }

    results = []
    print(f"{'observable':18s} {'alpha':>10s} {'se':>9s} {'expected':>10s} {'selected_model':18s} {'sweep_status':30s}")
    print("-" * 105)
    for label, obs in observables:
        r = probe_one(label, obs)
        results.append(r)
        exp_str = f"{expected_alpha[label]:.4f}" if expected_alpha[label] is not None else "???"
        print(f"{label:18s} {fmt_alpha(r['observed_alpha']):>10s} "
              f"{fmt_se(r['alpha_standard_error']):>9s} "
              f"{exp_str:>10s} "
              f"{(r['selected_model'] or 'None'):18s} "
              f"{(r['sweep_status'] or 'None'):30s}")

    print()
    print("=" * 100)
    print("DETAILED")
    print("=" * 100)
    for r in results:
        print(f"\n  {r['label']}")
        print(f"    alpha           : {fmt_alpha(r['observed_alpha'])}  +- {fmt_se(r['alpha_standard_error'])}")
        print(f"    alpha status    : {r['alpha_status']}")
        print(f"    selected_model  : {r['selected_model']}")
        print(f"    matching_models : {r['matching_models']}")
        print(f"    nested_stability: {r['alpha_stability']}  (window span = {fmt_se(r['alpha_window_span'])})")
        if r['alpha_r_squared'] is not None:
            print(f"    r_squared       : {r['alpha_r_squared']:.6f}")
        print(f"    n_observed      : {r['n_alpha_observed']}/{r['n_alpha_input']}  (n_cancellation={r['n_alpha_cancellation']})")
        scg = r['sweep_cancellation_grade']
        scg_s = f"{scg:.4f}" if scg is not None else "None"
        sdr = r['sweep_drop_rate']
        sdr_s = f"{sdr:.4f}" if sdr is not None else "None"
        print(f"    companion       : {r['sweep_status']}  (cancel_grade={scg_s}, drop_rate={sdr_s})")

    print()
    print("=" * 100)
    print("DISTINGUISHABILITY VERDICT")
    print("=" * 100)
    correct_matches = 0
    for r in results:
        if expected_model[r['label']] is None:
            continue
        match = r['selected_model'] == expected_model[r['label']]
        correct_matches += int(match)
        verdict = "MATCH" if match else "MISMATCH"
        print(f"  {r['label']:18s} expected={expected_model[r['label']]:18s} observed={(r['selected_model'] or 'None'):18s} -> {verdict}")
    print(f"\n  Distinguishability score: {correct_matches}/3 known predictions matched")

    discovery = [r for r in results if r['label'] == 'isco_retro_9'][0]
    print(f"\n  Discovery angle (isco_retro_9):")
    print(f"    measured alpha = {fmt_alpha(discovery['observed_alpha'])} +- {fmt_se(discovery['alpha_standard_error'])}")
    print(f"    matched model  = {discovery['selected_model']}")

    out_path = Path(__file__).parent / "kerr_extremal_alpha_recovery_results.json"
    with out_path.open("w") as fh:
        json.dump(
            {
                "config": {
                    "n_points": N_POINTS, "delta_start": DELTA_START, "delta_end": DELTA_END,
                    "eta": ETA,
                    "predicted_alphas": {k: v for k, v in expected_alpha.items() if v is not None},
                    "grid": list(DELTA_GRID),
                },
                "results": results,
            }, fh, indent=2,
        )
    print(f"\nResults: {out_path}")


if __name__ == "__main__":
    main()
