"""Cube-root α-at-branch — mpmath confirmation oracle.

Pre-registration (binding before measurement):
- Pipeline: compute g(f) = f^(1/3) and the forward finite-difference transfer
  T(f) = (g(f+δf) - g(f)) / δf at each f_value, then fit the log-log slope of |T|
  vs f, ALL IN mpmath AT 50-DIGIT PRECISION.
- f_values: same 12-point sweep as cbrt_alpha_probe.py (1e-2 down to 1e-9).
- eta: 1e-6 (matches primitive default).
- Goal: produce an α reading whose measurement chain does NOT share float64's u_p,
  so it can serve as the ground-truth reference for the +2.05e-11 difference
  observed between Python's ** and numpy's cbrt at float64.

This is NOT a V4 typed emit — it's a confirmation oracle (CLAUDE.md §4 / §5 V3-isolation
principle applied to mpmath: confirmation oracle, never a design source for substrate).

The two earlier float64 readings to compare against:
  Python f**(1/3):  observed_alpha = 0.3333333333377432
  numpy.cbrt(f):    observed_alpha = 0.3333333333582371
  delta:            +2.05e-11
"""
from __future__ import annotations

from mpmath import mp, mpf, power, log, sqrt
import math


def main() -> None:
    # Set mpmath to 50 decimal digits — well above float64's ~15-17 decimal digits
    mp.dps = 50

    # Same sweep as cbrt_alpha_probe.py
    f_values_float = [10.0 ** (-2.0 - (7.0 / 11.0) * i) for i in range(12)]

    eta_float = 1e-6

    print("=" * 78)
    print("cube-root α-at-branch — mpmath oracle (50 dps)")
    print("=" * 78)
    print(f"mpmath precision: mp.dps = {mp.dps}")
    print(f"f_values sweep: {len(f_values_float)} points, log-spaced 1e-2 → 1e-9")
    print(f"eta: {eta_float}")
    print()

    # --- Compute transfers entirely in mpmath ---
    f_mp = [mpf(f) for f in f_values_float]
    eta_mp = mpf(eta_float)
    delta_mp = [eta_mp * f for f in f_mp]

    one_third = mpf(1) / mpf(3)

    transfers_mp = []
    for f, delta in zip(f_mp, delta_mp):
        g_at_f = power(f, one_third)
        g_at_f_plus = power(f + delta, one_third)
        t = (g_at_f_plus - g_at_f) / delta
        transfers_mp.append(t)

    # --- Log-log fit IN mpmath ---
    log_f = [log(f) for f in f_mp]
    log_t = [log(abs(t)) for t in transfers_mp]

    n = len(log_f)
    n_mp = mpf(n)
    mean_x = sum(log_f) / n_mp
    mean_y = sum(log_t) / n_mp

    sxx = sum((x - mean_x) ** 2 for x in log_f)
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_f, log_t))
    slope_mp = sxy / sxx

    # Compute residuals and R^2 in mpmath
    intercept_mp = mean_y - slope_mp * mean_x
    residuals = [y - (slope_mp * x + intercept_mp) for x, y in zip(log_f, log_t)]
    ss_res = sum(r * r for r in residuals)
    ss_tot = sum((y - mean_y) ** 2 for y in log_t)
    r_squared_mp = mpf(1) if ss_tot == 0 else mpf(1) - ss_res / ss_tot
    standard_error_mp = sqrt(ss_res / mpf(n - 2) / sxx)

    alpha_mp = slope_mp + mpf(1)

    # --- Report ---
    print("--- mpmath high-precision pipeline result ---")
    print(f"  observed_slope (mpmath, full precision):")
    print(f"    {mp.nstr(slope_mp, 30)}")
    print(f"  observed_alpha (mpmath, full precision):")
    print(f"    {mp.nstr(alpha_mp, 30)}")
    print(f"  delta from exact 1/3:")
    delta_from_third = alpha_mp - one_third
    print(f"    {mp.nstr(delta_from_third, 15)}")
    print(f"  r_squared (mpmath):       {mp.nstr(r_squared_mp, 30)}")
    print(f"  standard_error (mpmath):  {mp.nstr(standard_error_mp, 15)}")
    print()

    # --- Comparison against earlier float64 readings ---
    print("--- comparison against earlier float64 readings ---")
    alpha_python_pow = 0.3333333333377432
    alpha_numpy_cbrt = 0.3333333333582371
    alpha_oracle_float = float(alpha_mp)

    print(f"  Python f**(1/3) float64 reading:  {alpha_python_pow!r}")
    print(f"  numpy.cbrt(f)    float64 reading: {alpha_numpy_cbrt!r}")
    print(f"  mpmath 50dps oracle reading:      {alpha_oracle_float!r}  (cast from {mp.nstr(alpha_mp, 18)})")
    print()
    print(f"  Python    vs oracle delta: {alpha_python_pow - alpha_oracle_float:+.3e}")
    print(f"  numpy.cbrt vs oracle delta: {alpha_numpy_cbrt - alpha_oracle_float:+.3e}")
    print(f"  Python vs numpy.cbrt:       {alpha_python_pow - alpha_numpy_cbrt:+.3e}")
    print()

    # --- Per-point transfer comparison (cast mpmath to float vs Python pow) ---
    print("--- per-point transfer comparison: mpmath-cast vs Python ** ---")
    print(f"{'f':>14}  {'T_mpmath_cast':>22}  {'T_python_pow':>22}  {'delta':>12}")
    print("-" * 78)
    for f_float, t_mp in zip(f_values_float, transfers_mp):
        t_mp_cast = float(t_mp)
        # Recompute the Python ** transfer the same way the V4 primitive would
        delta = eta_float * f_float
        g_python_at_f = f_float ** (1.0 / 3.0)
        g_python_at_fp = (f_float + delta) ** (1.0 / 3.0)
        t_python = (g_python_at_fp - g_python_at_f) / delta
        delta_t = t_python - t_mp_cast
        print(f"{f_float:14.3e}  {t_mp_cast:22.16e}  {t_python:22.16e}  {delta_t:+12.3e}")
    print()

    # --- Saturation check: what does the fit say at f → 0+? ---
    # If we restricted to only the smallest f_values, does alpha tighten further?
    print("--- saturation check: alpha from windowed fits, smallest-f subset ---")
    for k in (12, 10, 8, 6, 4):
        sub_log_f = log_f[-k:]
        sub_log_t = log_t[-k:]
        n_k = mpf(len(sub_log_f))
        mx = sum(sub_log_f) / n_k
        my = sum(sub_log_t) / n_k
        sxx_k = sum((x - mx) ** 2 for x in sub_log_f)
        sxy_k = sum((x - mx) * (y - my) for x, y in zip(sub_log_f, sub_log_t))
        slope_k = sxy_k / sxx_k
        alpha_k = slope_k + mpf(1)
        delta_k = alpha_k - one_third
        print(f"  k={k:2d} (last {k} probes, smallest f): "
              f"alpha = {mp.nstr(alpha_k, 18)}, delta from 1/3 = {mp.nstr(delta_k, 8)}")


if __name__ == "__main__":
    main()
