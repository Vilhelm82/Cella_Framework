"""Higher-radical α-family probe — V4-disciplined exploratory test.

Pre-registration (binding before measurement):
- For n ∈ {2, 3, 4, 5, 6, 7, 8}:
  - Run directional_alpha_probe with observable = lambda f: f**(1/n)
  - Compute mpmath oracle α at 50 dps for the same sweep
- Sweep: 12 f_values logarithmically spaced from 1e-2 down to 1e-9.
- eta: 1e-6 (primitive default).
- declared_alpha_models: empty (agnostic).
- Expected emit (paper prediction): observed_alpha ≈ 1/n for each n.

Falsifiability:
- observed_alpha materially ≠ 1/n for any n
- status not alpha_fractional_branch (e.g. alpha_regular_integer hit at n=1)
- stability != stable for any n
- mpmath oracle disagrees with 1/n

Cross-n questions:
- Does the V4-chain bias (observed_alpha - 1/n) scale monotonically with n?
- Does n=2 behave differently from n≥3 (mandated vs non-mandated)?
- Where do the routing precision floors set in vs n?
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from mpmath import mp, mpf, power, log, sqrt as mpsqrt

ROOT = Path("/home/william_lloydlt/projects/V4/Lloyd_Engine_V4")
sys.path.insert(0, str(ROOT / "src"))

from lloyd_v4.primitives.directional_alpha_probe import directional_alpha_probe


def mpmath_oracle_alpha(n: int, f_values: list[float], eta: float, dps: int = 50) -> dict:
    """Compute α via the same log-log-slope chain at high precision."""
    mp.dps = dps
    one_over_n = mpf(1) / mpf(n)

    f_mp = [mpf(f) for f in f_values]
    eta_mp = mpf(eta)
    delta_mp = [eta_mp * f for f in f_mp]

    transfers_mp = []
    for f, delta in zip(f_mp, delta_mp):
        g_at_f = power(f, one_over_n)
        g_at_f_plus = power(f + delta, one_over_n)
        t = (g_at_f_plus - g_at_f) / delta
        transfers_mp.append(t)

    log_f = [log(f) for f in f_mp]
    log_t = [log(abs(t)) for t in transfers_mp]

    n_pts = mpf(len(log_f))
    mean_x = sum(log_f) / n_pts
    mean_y = sum(log_t) / n_pts
    sxx = sum((x - mean_x) ** 2 for x in log_f)
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_f, log_t))
    slope_mp = sxy / sxx
    alpha_mp = slope_mp + mpf(1)
    delta_from_truth = alpha_mp - one_over_n
    return {
        "alpha_mpmath": alpha_mp,
        "delta_from_1_over_n": delta_from_truth,
    }


def main() -> None:
    f_values = [10.0 ** (-2.0 - (7.0 / 11.0) * i) for i in range(12)]
    eta = 1e-6

    n_values = [2, 3, 4, 5, 6, 7, 8]

    print("=" * 100)
    print("Higher-radical α-family probe")
    print("=" * 100)
    print(f"f sweep: 12 points log-spaced from 1e-2 to 1e-9")
    print(f"eta = {eta}, observable = lambda f: f**(1/n) via Python ** operator")
    print()

    results = []
    for n in n_values:
        observable = (lambda nn: lambda f: f ** (1.0 / nn))(n)
        v4_result = directional_alpha_probe(
            observable=observable,
            f_values=f_values,
            probe_id=f"radical_family_n_{n}_001",
            function_label=f"python_pow_1_over_{n}",
            eta=eta,
        )
        oracle = mpmath_oracle_alpha(n, f_values, eta)
        results.append({
            "n": n,
            "v4_alpha": v4_result.value.observed_alpha,
            "v4_status": v4_result.status.value,
            "v4_stability": v4_result.value.alpha_stability_status.value,
            "v4_window_span": v4_result.value.alpha_window_span,
            "v4_standard_error": v4_result.value.standard_error,
            "oracle_alpha": float(oracle["alpha_mpmath"]),
            "oracle_alpha_mp": oracle["alpha_mpmath"],
            "oracle_delta_from_truth": oracle["delta_from_1_over_n"],
            "n_observed": v4_result.value.n_observed,
            "n_input": v4_result.value.n_input_observations,
        })

    # --- Summary table ---
    print(f"{'n':>3}  {'1/n':>20}  {'V4 obs_alpha':>22}  {'oracle α (50dps)':>22}  "
          f"{'V4 − 1/n':>14}  {'oracle − 1/n':>14}")
    print("-" * 110)
    for r in results:
        truth = 1.0 / r["n"]
        v4_bias = r["v4_alpha"] - truth if r["v4_alpha"] is not None else None
        oracle_bias = float(r["oracle_delta_from_truth"])
        v4_bias_str = f"{v4_bias:+.3e}" if v4_bias is not None else "N/A"
        print(f"{r['n']:>3}  {truth:>20.16f}  {r['v4_alpha']!r:>22}  "
              f"{r['oracle_alpha']:>22.16f}  {v4_bias_str:>14}  {oracle_bias:>+14.3e}")

    print()
    print(f"{'n':>3}  {'V4 status':>30}  {'stability':>10}  {'window_span':>14}  "
          f"{'std_err':>14}  {'n_obs/n_in':>10}")
    print("-" * 110)
    for r in results:
        n_str = f"{r['n_observed']}/{r['n_input']}"
        print(f"{r['n']:>3}  {r['v4_status']:>30s}  {r['v4_stability']:>10s}  "
              f"{r['v4_window_span']:>14.3e}  {r['v4_standard_error']:>14.3e}  "
              f"{n_str:>10s}")

    print()
    print("=" * 100)
    print("V4-bias-from-truth vs n")
    print("=" * 100)
    print(f"{'n':>3}  {'V4 bias':>14}  {'mandate?':>10}")
    for r in results:
        truth = 1.0 / r["n"]
        v4_bias = r["v4_alpha"] - truth if r["v4_alpha"] is not None else None
        mandate = "IEEE-yes" if r["n"] == 2 else "IEEE-no"
        v4_bias_str = f"{v4_bias:+.3e}" if v4_bias is not None else "N/A"
        print(f"{r['n']:>3}  {v4_bias_str:>14}  {mandate:>10}")


if __name__ == "__main__":
    main()
