"""Paired marginal and cold end-to-end benchmark for all 16 contact walls."""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import random
import re
import statistics
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from cella.pathfinder import plan_request

from .model import M2ContactOrbitTask
from .wrapper import lift_route, lower_contact_orbit_task


@dataclass(frozen=True, slots=True)
class PairedTrial:
    trial: int
    order: str
    baseline_elapsed_seconds: float
    pathfinder_execution_elapsed_seconds: float
    certificate_elapsed_seconds: float
    wrapper_lowering_seconds: float
    pathfinder_analysis_seconds: float
    wrapper_lifting_seconds: float
    pathfinder_marginal_total_seconds: float
    paired_difference_seconds: float
    paired_speedup_ratio: float
    process_wall_seconds: float
    process_peak_rss_kb: int


@dataclass(frozen=True, slots=True)
class ColdTrial:
    trial: int
    baseline_wall_seconds: float
    baseline_peak_rss_kb: int
    pathfinder_wall_seconds: float
    pathfinder_peak_rss_kb: int
    wrapper_core_seconds: float


def _marker(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}=(.+)$", text, re.MULTILINE)
    if match is None:
        raise RuntimeError(f"missing benchmark marker {name}")
    return match.group(1).strip()


def _run_script(script: str, path: Path) -> tuple[str, float, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(script)
    started = time.perf_counter()
    completed = subprocess.run(
        ["/usr/bin/time", "-f", "CONTACT_BENCH_RSS_KB=%M", "M2", "--script", str(path)],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "LC_ALL": "C"},
    )
    wall = time.perf_counter() - started
    if completed.returncode:
        raise RuntimeError(f"M2 failed for {path}\n{completed.stdout}\n{completed.stderr}")
    return completed.stdout, wall, int(_marker(completed.stderr, "CONTACT_BENCH_RSS_KB"))


def _plan(task: M2ContactOrbitTask) -> tuple[object, float, float, float]:
    started = time.perf_counter()
    request = lower_contact_orbit_task(task)
    lower = time.perf_counter() - started
    started = time.perf_counter()
    outcome = plan_request(request)
    analysis = time.perf_counter() - started
    if outcome.route is None:
        raise RuntimeError(f"Pathfinder refused proper benchmark: {outcome.refusal}")
    started = time.perf_counter()
    lifted = lift_route(outcome.route)
    lifting = time.perf_counter() - started
    if lifted.route_family != "signed_contact_orbit_projection":
        raise RuntimeError(f"wrong selected route: {lifted.route_family}")
    return lifted, lower, analysis, lifting


def _paired_script(model: Path, structural_first: bool) -> str:
    baseline = '''baselineTimed = elapsedTiming apply(epsilons, eps ->
    projectToBase(contactIdeal eps + ideal(0_S))
    );
baselineImages = baselineTimed#1;
'''
    structural = '''structuralTimed = elapsedTiming apply(epsilons, eps ->
    trim ideal(wallPolynomial eps)
    );
structuralImages = structuralTimed#1;

certificateTimed = elapsedTiming all(epsilons, eps ->
    trim(contactIdeal eps + ideal(0_S)) == trim ideal(
        u,
        w1-eps#0*N1,
        w2-eps#1*N2,
        w3-eps#2*N3,
        w4-eps#3*N4,
        wallPolynomial eps
        )
    );
assert(certificateTimed#1);
'''
    operations = structural + baseline if structural_first else baseline + structural
    return f'''-- Paired 16-contact benchmark; model startup is outside marginal timings.
load "{model}";
{operations}
assert(all(16, k -> trim(baselineImages#k) == trim(structuralImages#k)));
assert(#structuralImages == 16);
print("CONTACT_BASELINE_ELAPSED_SECONDS=" | toString(baselineTimed#0));
print("CONTACT_STRUCTURAL_ELAPSED_SECONDS=" | toString(structuralTimed#0));
print("CONTACT_CERTIFICATE_ELAPSED_SECONDS=" | toString(certificateTimed#0));
print "CONTACT_EQUIVALENCE=CLOSED";
'''


def _baseline_cold_script(model: Path) -> str:
    return f'''load "{model}";
contactImages = apply(epsilons, eps -> projectToBase(contactIdeal eps + ideal(0_S)));
print "CONTACT_COLD_BASELINE_RESULT=CLOSED";
'''


def _stats(values: list[float]) -> dict[str, float]:
    ordered = sorted(values)
    return {
        "minimum": ordered[0],
        "q1": statistics.median(ordered[: len(ordered) // 2]),
        "median": statistics.median(ordered),
        "q3": statistics.median(ordered[(len(ordered) + 1) // 2 :]),
        "maximum": ordered[-1],
        "mad": statistics.median(abs(value - statistics.median(ordered)) for value in ordered),
    }


def _bootstrap_ci(values: list[float], *, samples: int = 10_000) -> tuple[float, float]:
    rng = random.Random(0xCE11A)
    medians = sorted(
        statistics.median(rng.choices(values, k=len(values)))
        for _ in range(samples)
    )
    return medians[int(0.025 * samples)], medians[int(0.975 * samples)]


def _sign_test_two_sided(positive: int, total: int) -> float:
    smaller = min(positive, total - positive)
    tail = sum(math.comb(total, k) for k in range(smaller + 1)) / (2**total)
    return min(1.0, 2 * tail)


def _m2_version() -> str:
    result = subprocess.run(["M2", "--version"], capture_output=True, text=True, check=False)
    return (result.stdout or result.stderr).strip()


def _markdown(report: dict[str, object]) -> str:
    marginal = report["marginal_summary"]  # type: ignore[index]
    cold = report["cold_end_to_end_summary"]  # type: ignore[index]
    return f'''# Proper Pathfinder benchmark: all 16 signed-contact projections

**Workload:** recorded stage-2 corpus deliverable, all sixteen contact-image ideals  
**Host:** {report["host_version"]}  
**Design:** {report["paired_trials"]} paired, order-balanced, fresh-process trials after two excluded warm-ups  
**Outliers removed:** none  
**Exact equivalence:** `{report["result_equivalence_status"]}`  
**External certificate:** `{report["certificate_status"]}`

## Marginal algorithm result

Model loading and process startup occur before both in-process timers. Pathfinder marginal total includes Python lowering, core analysis/selection, route lifting, direct wall construction, and independent triangular-ideal certificate replay.

| Measurement | Median | 95% bootstrap CI |
|---|---:|---:|
| Generic elimination | {marginal["baseline_seconds"]["median"]:.6f}s | — |
| Pathfinder including certificate | {marginal["pathfinder_total_seconds"]["median"]:.6f}s | — |
| Paired time saved | {marginal["paired_difference_seconds"]["median"]:.6f}s | [{marginal["paired_difference_median_95_ci"][0]:.6f}, {marginal["paired_difference_median_95_ci"][1]:.6f}]s |
| Paired speedup | {marginal["paired_speedup_ratio"]["median"]:.3f}x | [{marginal["paired_speedup_median_95_ci"][0]:.3f}, {marginal["paired_speedup_median_95_ci"][1]:.3f}]x |

Pathfinder was faster in **{marginal["pathfinder_faster_pairs"]}/{report["paired_trials"]}** pairs; exact two-sided sign-test `p={marginal["sign_test_p_value"]:.3g}`.

## Cold end-to-end result

These trials include Python wrapper/core work, M2 startup, model loading, execution, and Pathfinder certificate replay.

| Route | Median wall time | Median peak RSS |
|---|---:|---:|
| Generic elimination | {cold["baseline_wall_seconds"]["median"]:.6f}s | {cold["baseline_peak_rss_kb"]["median"]:.0f} KiB |
| Wrapped Pathfinder | {cold["pathfinder_wall_seconds"]["median"]:.6f}s | {cold["pathfinder_peak_rss_kb"]["median"]:.0f} KiB |

Cold median ratio: **{cold["median_speedup_ratio"]:.4f}x**. The marginal benchmark answers whether the route is computationally better; the cold benchmark answers whether one isolated invocation amortizes M2 startup.

## Interpretation

`{report["interpretation"]}`
'''


def run(root: Path, paired_trials: int, cold_trials: int) -> dict[str, object]:
    model = root / "docs" / "files" / "horizon_wreath_inertia_model.m2"
    task = M2ContactOrbitTask("m2-all-signed-contact-walls-v1", model)
    runs = root / "benchmarks" / "results" / "contact_orbit_runs"
    runs.mkdir(parents=True, exist_ok=True)

    # Two excluded warm-ups, one in each operation order.
    for index, structural_first in enumerate((False, True), 1):
        _plan(task)
        _run_script(_paired_script(model, structural_first), runs / f"warmup_{index}.m2")

    paired: list[PairedTrial] = []
    for trial in range(1, paired_trials + 1):
        _, lower, analysis, lifting = _plan(task)
        structural_first = trial % 2 == 0
        output, process_wall, peak_rss = _run_script(
            _paired_script(model, structural_first),
            runs / f"paired_{trial:02d}.m2",
        )
        if _marker(output, "CONTACT_EQUIVALENCE") != "CLOSED":
            raise RuntimeError("paired exact equivalence did not close")
        baseline = float(_marker(output, "CONTACT_BASELINE_ELAPSED_SECONDS"))
        structural = float(_marker(output, "CONTACT_STRUCTURAL_ELAPSED_SECONDS"))
        certificate = float(_marker(output, "CONTACT_CERTIFICATE_ELAPSED_SECONDS"))
        pathfinder_total = lower + analysis + lifting + structural + certificate
        paired.append(
            PairedTrial(
                trial,
                "pathfinder-first" if structural_first else "baseline-first",
                baseline,
                structural,
                certificate,
                lower,
                analysis,
                lifting,
                pathfinder_total,
                baseline - pathfinder_total,
                baseline / pathfinder_total,
                process_wall,
                peak_rss,
            )
        )

    # Cold trials are separate processes per route; one excluded warm-up each.
    lifted, _, _, _ = _plan(task)
    _run_script(_baseline_cold_script(model), runs / "cold_warmup_baseline.m2")
    _run_script(lifted.script, runs / "cold_warmup_pathfinder.m2")
    cold: list[ColdTrial] = []
    for trial in range(1, cold_trials + 1):
        _, lower, analysis, lifting = _plan(task)
        core = lower + analysis + lifting
        if trial % 2:
            _, baseline_wall, baseline_rss = _run_script(
                _baseline_cold_script(model), runs / f"cold_{trial:02d}_baseline.m2"
            )
            output, path_wall, path_rss = _run_script(
                lifted.script, runs / f"cold_{trial:02d}_pathfinder.m2"
            )
        else:
            output, path_wall, path_rss = _run_script(
                lifted.script, runs / f"cold_{trial:02d}_pathfinder.m2"
            )
            _, baseline_wall, baseline_rss = _run_script(
                _baseline_cold_script(model), runs / f"cold_{trial:02d}_baseline.m2"
            )
        if _marker(output, "PATHFINDER_M2_CERTIFICATE") != "CLOSED":
            raise RuntimeError("cold Pathfinder certificate did not close")
        cold.append(ColdTrial(trial, baseline_wall, baseline_rss, path_wall + core, path_rss, core))

    differences = [item.paired_difference_seconds for item in paired]
    ratios = [item.paired_speedup_ratio for item in paired]
    faster = sum(value > 0 for value in differences)
    baseline_cold = [item.baseline_wall_seconds for item in cold]
    pathfinder_cold = [item.pathfinder_wall_seconds for item in cold]
    report: dict[str, object] = {
        "benchmark_id": task.request_id,
        "source_workload": "docs/m2_out_2026-07-10/stage2_contact_walls.m2",
        "source_theorem": "CELLA_ARCHITECTURE_v1.3.md structure-first route table",
        "host_version": _m2_version(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "logical_cpu_count": os.cpu_count(),
        "load_average_at_report": os.getloadavg(),
        "paired_trials": paired_trials,
        "cold_trials_per_route": cold_trials,
        "warmup_policy": "two excluded paired warm-ups, one per order; one excluded cold warm-up per route",
        "order_policy": "alternating baseline-first and Pathfinder-first; no outlier removal",
        "mathematical_target": "all sixteen exact signed-contact image ideals",
        "baseline_route": "sixteen generic eliminate(contactIdeal(eps), sheetVars) calls",
        "pathfinder_route": "one triangular substitution law transported over the complete sign orbit",
        "marginal_summary": {
            "baseline_seconds": _stats([item.baseline_elapsed_seconds for item in paired]),
            "pathfinder_execution_seconds": _stats([item.pathfinder_execution_elapsed_seconds for item in paired]),
            "certificate_seconds": _stats([item.certificate_elapsed_seconds for item in paired]),
            "wrapper_lowering_seconds": _stats([item.wrapper_lowering_seconds for item in paired]),
            "pathfinder_analysis_seconds": _stats([item.pathfinder_analysis_seconds for item in paired]),
            "wrapper_lifting_seconds": _stats([item.wrapper_lifting_seconds for item in paired]),
            "pathfinder_total_seconds": _stats([item.pathfinder_marginal_total_seconds for item in paired]),
            "paired_difference_seconds": _stats(differences),
            "paired_difference_median_95_ci": _bootstrap_ci(differences),
            "paired_speedup_ratio": _stats(ratios),
            "paired_speedup_median_95_ci": _bootstrap_ci(ratios),
            "pathfinder_faster_pairs": faster,
            "sign_test_p_value": _sign_test_two_sided(faster, paired_trials),
        },
        "cold_end_to_end_summary": {
            "baseline_wall_seconds": _stats(baseline_cold),
            "pathfinder_wall_seconds": _stats(pathfinder_cold),
            "baseline_peak_rss_kb": _stats([float(item.baseline_peak_rss_kb) for item in cold]),
            "pathfinder_peak_rss_kb": _stats([float(item.pathfinder_peak_rss_kb) for item in cold]),
            "median_speedup_ratio": statistics.median(baseline_cold) / statistics.median(pathfinder_cold),
        },
        "result_equivalence_status": "exact-ideal-equality-all-16",
        "certificate_status": "independent-triangular-presentation-replay-closed",
        "interpretation": (
            "The structural route is admitted and benchmarked as a genuine algorithmic improvement only if "
            "the paired median difference and its 95% interval are positive. Cold-start performance is reported "
            "separately and is not allowed to erase or fabricate the marginal result."
        ),
        "paired_trial_records": [asdict(item) for item in paired],
        "cold_trial_records": [asdict(item) for item in cold],
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--paired-trials", type=int, default=30)
    parser.add_argument("--cold-trials", type=int, default=7)
    args = parser.parse_args()
    if args.paired_trials < 20 or args.cold_trials < 7:
        parser.error("proper campaign requires at least 20 paired and 7 cold trials")
    report = run(args.root.resolve(), args.paired_trials, args.cold_trials)
    results = args.root / "benchmarks" / "results"
    json_path = results / "CONTACT_ORBIT_BENCHMARK.json"
    markdown_path = results / "CONTACT_ORBIT_BENCHMARK.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    markdown_path.write_text(_markdown(report))
    print(markdown_path)
    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
