"""Cube-root α-at-branch probe — V4-disciplined exploratory test.

Pre-registration (binding before measurement):
- Probes: two runs of directional_alpha_probe, identical except observable callable.
- Synthetic observable: lambda f: f**(1/3)   (Python float64 ** operator)
- Fixture observable:   lambda f: float(np.cbrt(f))   (numpy cbrt, matches R_of_x routing in evals/cbrt_four_form.py)
- f_values: 12 points logarithmically spaced from f = 1e-2 down to f = 1e-9 (approaching 0+ from above).
- eta: 1e-6 (primitive default).
- declared_alpha_models: empty.
- declared_alpha_band: None.

Expected emit (paper prediction, transfer_function_exponent_family_v4.tex):
  observed_alpha ≈ 1/3
  status = alpha_fractional_branch
  alpha_stability_status = stable (if nested-window check passes)

Falsifiability — any of the following would surprise:
  - observed_alpha materially ≠ 1/3
  - status != alpha_fractional_branch
  - stability != stable
  - refusal status emitted
  - the two observables behaving differently from each other

NOT scratch arithmetic. The primitive (directional_alpha_probe) is the V4 typed primitive;
this script only sets up the inputs and prints the outputs.
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
    # Sweep: 12 points logarithmically spaced from f=1e-2 down to f=1e-9
    f_values = [10.0 ** (-2.0 - (7.0 / 11.0) * i) for i in range(12)]

    print("=" * 78)
    print("cube-root α-at-branch probe — V4-disciplined")
    print("=" * 78)
    print(f"f_values sweep ({len(f_values)} points, log-spaced):")
    for i, f in enumerate(f_values):
        print(f"  [{i:2d}] f = {f:.3e}")
    print()

    # --- Test 1: synthetic observable (Python float64 ** operator) ---
    print("-" * 78)
    print("TEST 1: synthetic observable  g(f) = f**(1/3)  (Python ** operator)")
    print("-" * 78)
    result_synthetic = directional_alpha_probe(
        observable=lambda f: f ** (1.0 / 3.0),
        f_values=f_values,
        probe_id="cbrt_alpha_synthetic_001",
        function_label="synthetic_cbrt_python_pow",
        eta=1e-6,
    )
    report_result(result_synthetic)
    print()

    # --- Test 2: fixture observable (numpy cbrt, matches R_of_x routing) ---
    print("-" * 78)
    print("TEST 2: fixture observable  g(f) = float(np.cbrt(f))  (numpy cbrt routing)")
    print("-" * 78)
    result_fixture = directional_alpha_probe(
        observable=lambda f: float(np.cbrt(f)),
        f_values=f_values,
        probe_id="cbrt_alpha_fixture_001",
        function_label="fixture_numpy_cbrt",
        eta=1e-6,
    )
    report_result(result_fixture)
    print()

    # --- Cross-comparison ---
    print("=" * 78)
    print("cross-comparison")
    print("=" * 78)
    obs_syn = result_synthetic.value.observed_alpha
    obs_fix = result_fixture.value.observed_alpha
    if obs_syn is not None and obs_fix is not None:
        delta = obs_fix - obs_syn
        print(f"  synthetic observed_alpha = {obs_syn!r}")
        print(f"  fixture   observed_alpha = {obs_fix!r}")
        print(f"  delta (fixture - synthetic) = {delta:+.3e}")
    else:
        print(f"  synthetic observed_alpha = {obs_syn!r}")
        print(f"  fixture   observed_alpha = {obs_fix!r}")
    print(f"  synthetic status = {result_synthetic.status.value}")
    print(f"  fixture   status = {result_fixture.status.value}")
    print(f"  synthetic alpha_stability_status = {result_synthetic.value.alpha_stability_status.value}")
    print(f"  fixture   alpha_stability_status = {result_fixture.value.alpha_stability_status.value}")


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
