"""Cache-isolated benchmark for the complete signed-contact projection route."""

from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from .contact_orbit_benchmark import (
    _bootstrap_ci,
    _marker,
    _plan,
    _run_script,
    _sign_test_two_sided,
    _stats,
)
from .model import M2ContactOrbitTask


@dataclass(frozen=True, slots=True)
class IsolatedPair:
    trial: int
    order: str
    baseline_marginal_seconds: float
    pathfinder_execution_seconds: float
    pathfinder_certificate_seconds: float
    wrapper_lowering_seconds: float
    pathfinder_analysis_seconds: float
    wrapper_lifting_seconds: float
    pathfinder_marginal_total_seconds: float
    marginal_difference_seconds: float
    marginal_speedup_ratio: float
    baseline_cold_wall_seconds: float
    pathfinder_cold_wall_seconds: float
    cold_difference_seconds: float
    cold_speedup_ratio: float
    baseline_peak_rss_kb: int
    pathfinder_peak_rss_kb: int


def _baseline_script(model: Path) -> str:
    return f'''-- Cache-isolated generic route for all sixteen contact images.
load "{model}";
baselineTimed = elapsedTiming apply(epsilons, eps ->
    projectToBase(contactIdeal eps + ideal(0_S))
    );
baselineImages = baselineTimed#1;
expectedWalls = apply(epsilons, eps -> trim ideal(wallPolynomial eps));
assert(#baselineImages == 16);
assert(all(16, k -> trim(baselineImages#k) == trim(expectedWalls#k)));
print("CONTACT_BASELINE_ELAPSED_SECONDS=" | toString(baselineTimed#0));
print "CONTACT_BASELINE_EXACTNESS=CLOSED";
'''


def _version() -> str:
    result = subprocess.run(["M2", "--version"], capture_output=True, text=True, check=False)
    return (result.stdout or result.stderr).strip()


def _stratum(records: list[IsolatedPair], order: str) -> dict[str, object]:
    selected = [record for record in records if record.order == order]
    return {
        "count": len(selected),
        "marginal_difference_seconds": _stats([record.marginal_difference_seconds for record in selected]),
        "marginal_speedup_ratio": _stats([record.marginal_speedup_ratio for record in selected]),
        "cold_difference_seconds": _stats([record.cold_difference_seconds for record in selected]),
        "cold_speedup_ratio": _stats([record.cold_speedup_ratio for record in selected]),
    }


def _markdown(report: dict[str, object]) -> str:
    marginal = report["marginal_summary"]  # type: ignore[index]
    cold = report["cold_summary"]  # type: ignore[index]
    strata = report["order_stratified_summary"]  # type: ignore[index]
    return f'''# Pathfinder benchmark: 16 signed-contact projections, cache-isolated

**Workload:** recorded stage-2 corpus deliverable  
**Host:** {report["host_version"]}  
**Design:** {report["trials"]} paired trials; each route in a separate fresh M2 process; order alternated  
**Warm-up:** one excluded process per route  
**Outliers removed:** none  
**Exact baseline result:** `closed`  
**Independent Pathfinder certificate:** `closed`

## Marginal route cost

Internal M2 elapsed timings exclude process startup and model loading. Pathfinder total includes wrapper lowering, core recognition/selection, route lifting, direct wall construction, and independent triangular-presentation replay.

| Measurement | Median | 95% paired-bootstrap interval |
|---|---:|---:|
| Generic elimination | {marginal["baseline_seconds"]["median"]:.6f}s | — |
| Pathfinder including certificate | {marginal["pathfinder_total_seconds"]["median"]:.6f}s | — |
| Time saved | {marginal["difference_seconds"]["median"]:.6f}s | [{marginal["difference_median_95_ci"][0]:.6f}, {marginal["difference_median_95_ci"][1]:.6f}]s |
| Speedup | {marginal["speedup_ratio"]["median"]:.3f}x | [{marginal["speedup_median_95_ci"][0]:.3f}, {marginal["speedup_median_95_ci"][1]:.3f}]x |

Pathfinder was faster in **{marginal["pathfinder_faster_pairs"]}/{report["trials"]}** isolated pairs; exact two-sided sign-test `p={marginal["sign_test_p_value"]:.3g}`.

## Cold end-to-end cost

Cold totals include separate M2 startup/model loading. Pathfinder also includes its Python wrapper/core overhead and external certificate replay.

| Measurement | Generic | Pathfinder |
|---|---:|---:|
| Median wall time | {cold["baseline_wall_seconds"]["median"]:.6f}s | {cold["pathfinder_wall_seconds"]["median"]:.6f}s |
| Median peak RSS | {cold["baseline_peak_rss_kb"]["median"]:.0f} KiB | {cold["pathfinder_peak_rss_kb"]["median"]:.0f} KiB |

Cold paired median speedup: **{cold["speedup_ratio"]["median"]:.4f}x**, 95% interval [{cold["speedup_median_95_ci"][0]:.4f}, {cold["speedup_median_95_ci"][1]:.4f}]x. Pathfinder was faster cold in **{cold["pathfinder_faster_pairs"]}/{report["trials"]}** pairs.

## Order-stratified check

| Stratum | Pairs | Marginal median speedup | Cold median speedup |
|---|---:|---:|---:|
| Baseline process first | {strata["baseline-first"]["count"]} | {strata["baseline-first"]["marginal_speedup_ratio"]["median"]:.3f}x | {strata["baseline-first"]["cold_speedup_ratio"]["median"]:.4f}x |
| Pathfinder process first | {strata["pathfinder-first"]["count"]} | {strata["pathfinder-first"]["marginal_speedup_ratio"]["median"]:.3f}x | {strata["pathfinder-first"]["cold_speedup_ratio"]["median"]:.4f}x |

The separate-process design prevents one route from populating Gröbner caches used by the other. Order strata remain visible to expose thermal or system-drift effects.
'''


def run(root: Path, trials: int) -> dict[str, object]:
    model = root / "docs" / "files" / "horizon_wreath_inertia_model.m2"
    task = M2ContactOrbitTask("m2-all-signed-contact-walls-v2-isolated", model)
    runs = root / "benchmarks" / "results" / "contact_orbit_isolated_runs"
    runs.mkdir(parents=True, exist_ok=True)

    lifted, _, _, _ = _plan(task)
    _run_script(_baseline_script(model), runs / "warmup_baseline.m2")
    _run_script(lifted.script, runs / "warmup_pathfinder.m2")

    records: list[IsolatedPair] = []
    for trial in range(1, trials + 1):
        lifted, lower, analysis, lifting = _plan(task)
        pathfinder_first = trial % 2 == 0
        if pathfinder_first:
            path_output, path_wall, path_rss = _run_script(
                lifted.script, runs / f"trial_{trial:02d}_pathfinder.m2"
            )
            baseline_output, baseline_wall, baseline_rss = _run_script(
                _baseline_script(model), runs / f"trial_{trial:02d}_baseline.m2"
            )
        else:
            baseline_output, baseline_wall, baseline_rss = _run_script(
                _baseline_script(model), runs / f"trial_{trial:02d}_baseline.m2"
            )
            path_output, path_wall, path_rss = _run_script(
                lifted.script, runs / f"trial_{trial:02d}_pathfinder.m2"
            )
        if _marker(baseline_output, "CONTACT_BASELINE_EXACTNESS") != "CLOSED":
            raise RuntimeError("isolated baseline exactness failed")
        if _marker(path_output, "PATHFINDER_M2_CERTIFICATE") != "CLOSED":
            raise RuntimeError("isolated Pathfinder certificate failed")

        baseline = float(_marker(baseline_output, "CONTACT_BASELINE_ELAPSED_SECONDS"))
        execution = float(_marker(path_output, "PATHFINDER_M2_EXEC_ELAPSED_SECONDS"))
        certificate = float(_marker(path_output, "PATHFINDER_M2_CERT_ELAPSED_SECONDS"))
        core = lower + analysis + lifting
        pathfinder_marginal = core + execution + certificate
        pathfinder_cold = core + path_wall
        records.append(
            IsolatedPair(
                trial,
                "pathfinder-first" if pathfinder_first else "baseline-first",
                baseline,
                execution,
                certificate,
                lower,
                analysis,
                lifting,
                pathfinder_marginal,
                baseline - pathfinder_marginal,
                baseline / pathfinder_marginal,
                baseline_wall,
                pathfinder_cold,
                baseline_wall - pathfinder_cold,
                baseline_wall / pathfinder_cold,
                baseline_rss,
                path_rss,
            )
        )

    marginal_differences = [record.marginal_difference_seconds for record in records]
    marginal_ratios = [record.marginal_speedup_ratio for record in records]
    cold_differences = [record.cold_difference_seconds for record in records]
    cold_ratios = [record.cold_speedup_ratio for record in records]
    marginal_faster = sum(value > 0 for value in marginal_differences)
    cold_faster = sum(value > 0 for value in cold_differences)
    return {
        "benchmark_id": task.request_id,
        "source_workload": "docs/m2_out_2026-07-10/stage2_contact_walls.m2",
        "host_version": _version(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "logical_cpu_count": os.cpu_count(),
        "load_average_at_report": os.getloadavg(),
        "trials": trials,
        "warmup_policy": "one excluded fresh-process warm-up per route",
        "order_policy": "alternating separate-process order; no outlier removal",
        "result_equivalence_status": "both routes independently equal all sixteen declared wall ideals",
        "certificate_status": "Pathfinder triangular-presentation replay closed in every trial",
        "marginal_summary": {
            "baseline_seconds": _stats([record.baseline_marginal_seconds for record in records]),
            "pathfinder_execution_seconds": _stats([record.pathfinder_execution_seconds for record in records]),
            "pathfinder_certificate_seconds": _stats([record.pathfinder_certificate_seconds for record in records]),
            "pathfinder_total_seconds": _stats([record.pathfinder_marginal_total_seconds for record in records]),
            "difference_seconds": _stats(marginal_differences),
            "difference_median_95_ci": _bootstrap_ci(marginal_differences),
            "speedup_ratio": _stats(marginal_ratios),
            "speedup_median_95_ci": _bootstrap_ci(marginal_ratios),
            "pathfinder_faster_pairs": marginal_faster,
            "sign_test_p_value": _sign_test_two_sided(marginal_faster, trials),
        },
        "cold_summary": {
            "baseline_wall_seconds": _stats([record.baseline_cold_wall_seconds for record in records]),
            "pathfinder_wall_seconds": _stats([record.pathfinder_cold_wall_seconds for record in records]),
            "difference_seconds": _stats(cold_differences),
            "difference_median_95_ci": _bootstrap_ci(cold_differences),
            "speedup_ratio": _stats(cold_ratios),
            "speedup_median_95_ci": _bootstrap_ci(cold_ratios),
            "pathfinder_faster_pairs": cold_faster,
            "sign_test_p_value": _sign_test_two_sided(cold_faster, trials),
            "baseline_peak_rss_kb": _stats([float(record.baseline_peak_rss_kb) for record in records]),
            "pathfinder_peak_rss_kb": _stats([float(record.pathfinder_peak_rss_kb) for record in records]),
        },
        "order_stratified_summary": {
            "baseline-first": _stratum(records, "baseline-first"),
            "pathfinder-first": _stratum(records, "pathfinder-first"),
        },
        "trial_records": [asdict(record) for record in records],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--trials", type=int, default=30)
    args = parser.parse_args()
    if args.trials < 20:
        parser.error("cache-isolated campaign requires at least 20 pairs")
    report = run(args.root.resolve(), args.trials)
    results = args.root / "benchmarks" / "results"
    json_path = results / "CONTACT_ORBIT_ISOLATED_BENCHMARK.json"
    markdown_path = results / "CONTACT_ORBIT_ISOLATED_BENCHMARK.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    markdown_path.write_text(_markdown(report))
    print(markdown_path)
    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
