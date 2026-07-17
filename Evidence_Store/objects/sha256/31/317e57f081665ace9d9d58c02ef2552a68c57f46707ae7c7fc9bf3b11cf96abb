"""Square-root α-at-branch probe — V4-disciplined exploratory test.

Pre-registration (binding before measurement):
- Probes: three runs of directional_alpha_probe, identical except observable callable.
  - Python `**(1/2)`:  lambda f: f**(1/2)         (Python float64 ** operator;
                                                   identical to pure_algebraic R_of_x)
  - math.sqrt:         lambda f: math.sqrt(f)     (math.sqrt routing)
  - numpy.sqrt:        lambda f: float(np.sqrt(f)) (numpy.sqrt routing)
- f_values: same 12-point logarithmic sweep as cube-root probe (1e-2 down to 1e-9).
- eta: 1e-6 (primitive default).
- declared_alpha_models: empty (agnostic).
- declared_alpha_band: None.

Expected emit (paper prediction):
  observed_alpha ≈ 1/2
  status = alpha_fractional_branch
  alpha_stability_status = stable (if nested-window check passes)

Falsifiability — any of the following would surprise:
  - observed_alpha materially ≠ 1/2
  - status != alpha_fractional_branch
  - stability != stable
  - refusal status emitted
  - the three observables behaving outside the precision floor of the V4 chain

Test of interest beyond the basic α=1/2 confirmation:
  - Does the b_k routing asymmetry (~5.6× numpy/python observed in cube-root)
    hold for sqrt? Or is the asymmetry pattern radical-specific?
  - With three routings instead of two, we get a 3-point routing comparison
    rather than a 2-point comparison — potentially revealing whether b_k
    scales differently across math vs numpy implementations.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

# Add V4 src to path
ROOT = Path("/home/william_lloydlt/projects/V4/Lloyd_Engine_V4")
sys.path.insert(0, str(ROOT / "src"))

from lloyd_v4.primitives.directional_alpha_probe import directional_alpha_probe


def main() -> None:
    # Same sweep as cbrt_alpha_probe.py
    f_values = [10.0 ** (-2.0 - (7.0 / 11.0) * i) for i in range(12)]

    print("=" * 78)
    print("square-root α-at-branch probe — V4-disciplined")
    print("=" * 78)
    print(f"f_values sweep ({len(f_values)} points, log-spaced):")
    for i, f in enumerate(f_values):
        print(f"  [{i:2d}] f = {f:.3e}")
    print()

    # --- Test 1: Python ** operator ---
    print("-" * 78)
    print("TEST 1: synthetic observable  g(f) = f**(1/2)  (Python ** operator)")
    print("        identical to pure_algebraic R_of_x routing")
    print("-" * 78)
    result_python = directional_alpha_probe(
        observable=lambda f: f ** (1.0 / 2.0),
        f_values=f_values,
        probe_id="sqrt_alpha_python_pow_001",
        function_label="synthetic_sqrt_python_pow",
        eta=1e-6,
    )
    report_result(result_python)
    print()

    # --- Test 2: math.sqrt routing ---
    print("-" * 78)
    print("TEST 2: math.sqrt routing  g(f) = math.sqrt(f)")
    print("-" * 78)
    result_math = directional_alpha_probe(
        observable=lambda f: math.sqrt(f),
        f_values=f_values,
        probe_id="sqrt_alpha_math_sqrt_001",
        function_label="math_sqrt",
        eta=1e-6,
    )
    report_result(result_math)
    print()

    # --- Test 3: numpy.sqrt routing ---
    print("-" * 78)
    print("TEST 3: numpy.sqrt routing  g(f) = float(np.sqrt(f))")
    print("-" * 78)
    result_numpy = directional_alpha_probe(
        observable=lambda f: float(np.sqrt(f)),
        f_values=f_values,
        probe_id="sqrt_alpha_numpy_sqrt_001",
        function_label="numpy_sqrt",
        eta=1e-6,
    )
    report_result(result_numpy)
    print()

    # --- Cross-comparison ---
    print("=" * 78)
    print("cross-comparison")
    print("=" * 78)
    obs_py = result_python.value.observed_alpha
    obs_ma = result_math.value.observed_alpha
    obs_np = result_numpy.value.observed_alpha
    half = 0.5

    print(f"  Python **(1/2)  observed_alpha = {obs_py!r}")
    print(f"  math.sqrt       observed_alpha = {obs_ma!r}")
    print(f"  numpy.sqrt      observed_alpha = {obs_np!r}")
    print()
    if all(o is not None for o in (obs_py, obs_ma, obs_np)):
        print(f"  Python  delta from 1/2  = {obs_py - half:+.3e}")
        print(f"  math    delta from 1/2  = {obs_ma - half:+.3e}")
        print(f"  numpy   delta from 1/2  = {obs_np - half:+.3e}")
        print()
        print(f"  math vs Python         = {obs_ma - obs_py:+.3e}")
        print(f"  numpy vs Python        = {obs_np - obs_py:+.3e}")
        print(f"  numpy vs math          = {obs_np - obs_ma:+.3e}")
        print()
        # b_k ratio: how does each routing's bias from 1/2 compare?
        # (Using absolute distance to handle either-sign biases)
        d_py = abs(obs_py - half)
        d_ma = abs(obs_ma - half)
        d_np = abs(obs_np - half)
        if d_py > 0:
            print(f"  math/Python  bias-magnitude ratio  = {d_ma/d_py:.2f}")
            print(f"  numpy/Python bias-magnitude ratio  = {d_np/d_py:.2f}")
        if d_ma > 0:
            print(f"  numpy/math   bias-magnitude ratio  = {d_np/d_ma:.2f}")
    print()
    print(f"  Python status  = {result_python.status.value}")
    print(f"  math   status  = {result_math.status.value}")
    print(f"  numpy  status  = {result_numpy.status.value}")
    print()
    print(f"  Python stability  = {result_python.value.alpha_stability_status.value}")
    print(f"  math   stability  = {result_math.value.alpha_stability_status.value}")
    print(f"  numpy  stability  = {result_numpy.value.alpha_stability_status.value}")
    print()
    print(f"  Python window_span  = {result_python.value.alpha_window_span!r}")
    print(f"  math   window_span  = {result_math.value.alpha_window_span!r}")
    print(f"  numpy  window_span  = {result_numpy.value.alpha_window_span!r}")
    print()
    print(f"  Python propagated_window_error  = {result_python.value.propagated_window_error!r}")
    print(f"  math   propagated_window_error  = {result_math.value.propagated_window_error!r}")
    print(f"  numpy  propagated_window_error  = {result_numpy.value.propagated_window_error!r}")


def report_result(result) -> None:
    v = result.value
    print(f"  status                   = {result.status.value}")
    print(f"  observed_alpha           = {v.observed_alpha!r}")
    print(f"  observed_slope           = {v.observed_slope!r}")
    print(f"  r_squared                = {v.r_squared!r}")
    print(f"  standard_error           = {v.standard_error!r}")
    print(f"  alpha_stability_status   = {v.alpha_stability_status.value}")
    print(f"  alpha_window_min/max     = {v.alpha_window_min!r}, {v.alpha_window_max!r}")
    print(f"  alpha_window_span        = {v.alpha_window_span!r}")
    print(f"  propagated_window_error  = {v.propagated_window_error!r}")
    print(f"  n_observed / n_input     = {v.n_observed} / {v.n_input_observations}")
    print(f"  n_cancellation_dominated = {v.n_cancellation_dominated}")
    print(f"  n_domain_refused         = {v.n_domain_refused}")
    print(f"  n_non_finite             = {v.n_non_finite}")
    print(f"  validity.selectable      = {result.validity.selectable}")


if __name__ == "__main__":
    main()
