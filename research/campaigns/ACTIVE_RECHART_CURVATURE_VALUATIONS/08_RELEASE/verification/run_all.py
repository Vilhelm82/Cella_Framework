#!/usr/bin/env python3
"""One-command verification entry point for the ACTIVE_RECHART_CURVATURE_VALUATIONS
release (plan Stage 9 requirement).

Runs every NEW falsification gate and the load-bearing packaged LEGACY
certificates. Exact arithmetic throughout; any failure exits nonzero.

    python3 08_RELEASE/verification/run_all.py [--quick]

--quick skips the slowest legacy certificates (test6/test9); the proof-bearing
new gates always run.
"""
import subprocess
import sys
import time
from pathlib import Path

CAMP = Path(__file__).resolve().parents[2]
NEW = CAMP / "05_VERIFICATION_NEW"
LEG = CAMP / "04_VERIFICATION_LEGACY"

NEW_GATES = [
    "role_cover_groupoid/verify_output_role_groupoid_r2.py",
    "role_cover_groupoid/verify_output_role_groupoid_r3.py",
    "role_cover_groupoid/verify_three_role_recovery.py",
    "channel_normalization/verify_sigma2_channel_split.py",
    "strict_descent_gate/verify_metric_rechart_defect_generic_n2.py",
    "strict_descent_gate/verify_metric_rechart_defect_exact_examples.py",
    "defect_cocycle/verify_defect_cocycle.py",
    "channel_transport/verify_channel_transport_generic_n2.py",
    "channel_transport/verify_output_role_quadruples.py",
    "channel_transport/verify_channel_cocycle.py",
    "channel_transport/verify_gauge_normal_form_all_dimensions.py",
    "off_diagonal_germs/verify_offdiag_frame_normal_form.py",
    "off_diagonal_germs/verify_inverse_metric_valuations.py",
    "off_diagonal_germs/verify_curvature_initial_form_random_exact.py",
    "off_diagonal_germs/find_offdiag_cancellation_counterexamples.py",
    "valuation_naturality/verify_principal_coefficient_rechart.py",
    "valuation_naturality/verify_defining_function_weight.py",
    "valuation_naturality/verify_weighted_jet_finiteness.py",
    "valuation_naturality/regress_variable_transverse_theorem.py",
    "regression/verify_diagonal_corner_recovery.py",
    "regression/verify_kn_replay.py",
]

LEGACY = [
    "local_curvature/pfc_test1_local_normal_forms.py",
    "local_curvature/pfc_test2_corner_valuation.py",
    "local_curvature/pfc_test3_vertex_rule.py",
    "local_curvature/lead7_test10_reflection_lemma.py",
    "kerr_newman/lead7_test4_masscharge_zeros.py",
]
LEGACY_SLOW = [
    "kerr_newman/lead7_test6_pole_coeffs_n3.py",
    "kerr_newman/lead7_test9_corner.py",
]


def run(base, rel):
    path = base / rel
    t0 = time.time()
    r = subprocess.run([sys.executable, path.name], cwd=str(path.parent),
                       capture_output=True, text=True, timeout=1800)
    dt = time.time() - t0
    ok = r.returncode == 0
    print(f"{'PASS' if ok else 'FAIL'}  [{dt:6.1f}s]  {rel}")
    if not ok:
        print(r.stdout[-3000:])
        print(r.stderr[-3000:])
    return ok


def main():
    quick = "--quick" in sys.argv
    fails = []
    print("== NEW falsification gates ==")
    for g in NEW_GATES:
        if not run(NEW, g):
            fails.append(g)
    print("== packaged LEGACY certificates ==")
    legacy = LEGACY + ([] if quick else LEGACY_SLOW)
    for g in legacy:
        if not run(LEG, g):
            fails.append(g)
    print()
    if fails:
        print("RELEASE VERIFICATION FAILED:", fails)
        return 1
    print(f"RELEASE VERIFICATION PASSED: {len(NEW_GATES)} new gates, "
          f"{len(legacy)} legacy certificates — all exact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
