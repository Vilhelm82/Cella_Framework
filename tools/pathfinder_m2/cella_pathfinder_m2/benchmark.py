"""End-to-end benchmark campaign for the first M2 Pathfinder fixture."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from cella.pathfinder import plan_request

from .execute import M2Execution, run_m2_script
from .model import M2ContactProjectionTask
from .wrapper import lift_route, lower_task


@dataclass(frozen=True, slots=True)
class BaselineTrial:
    trial: int
    total_wall_ns: int
    peak_rss_kb: int
    canonical_generators: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PathfinderTrial:
    trial: int
    lowering_ns: int
    analysis_ns: int
    lifting_ns: int
    host_execution_and_certificate_wall_ns: int
    total_wall_ns: int
    execution_cpu_seconds: float
    certificate_cpu_seconds: float
    peak_rss_kb: int
    canonical_generators: tuple[str, ...]
    certificate_status: str


def _baseline_script(task: M2ContactProjectionTask) -> str:
    terms = ", ".join(f"{name}-{value}" for name, value in task.slice_assignments)
    return f'''-- Historical generic baseline for {task.request_id}.
load "{task.model_path}";
sliceA = ideal({terms});
baseline = trim eliminate(
    saturate({task.contact_component} + {task.rotating_ideal} + sliceA, ideal(M)),
    sheetVars
    );
print "PATHFINDER_M2_BASELINE_BEGIN";
print toString gens baseline;
print "PATHFINDER_M2_BASELINE_END";
'''


def _run_baseline(task: M2ContactProjectionTask, path: Path, trial: int) -> BaselineTrial:
    result = run_m2_script(
        _baseline_script(task),
        script_path=path,
        result_markers=("PATHFINDER_M2_BASELINE_BEGIN", "PATHFINDER_M2_BASELINE_END"),
    )
    return BaselineTrial(trial, result.wall_ns, result.peak_rss_kb, result.canonical_generators)


def _run_pathfinder(
    task: M2ContactProjectionTask, path: Path, trial: int, *, certified: bool = True
) -> tuple[PathfinderTrial, bytes]:
    total_started = time.perf_counter_ns()
    started = time.perf_counter_ns()
    request = lower_task(task)
    lowering_ns = time.perf_counter_ns() - started

    started = time.perf_counter_ns()
    outcome = plan_request(request)
    analysis_ns = time.perf_counter_ns() - started
    if outcome.route is None:
        assert outcome.refusal is not None
        raise RuntimeError(f"Pathfinder refused benchmark fixture: {outcome.refusal}")

    started = time.perf_counter_ns()
    lifted = lift_route(outcome.route, certified=certified)
    lifting_ns = time.perf_counter_ns() - started

    execution = run_m2_script(
        lifted.script,
        script_path=path,
        result_markers=("PATHFINDER_M2_RESULT_BEGIN", "PATHFINDER_M2_RESULT_END"),
    )
    total_wall_ns = time.perf_counter_ns() - total_started
    if execution.execution_cpu_seconds is None:
        raise RuntimeError("lifted route omitted internal execution timing")
    if certified:
        if execution.certificate_cpu_seconds is None:
            raise RuntimeError("lifted route omitted certificate timing")
        if execution.certificate_status is None:
            raise RuntimeError("lifted route omitted certificate status")
        certificate_cpu_seconds = execution.certificate_cpu_seconds
        certificate_status = execution.certificate_status
    else:
        # Route-only mode: certified delivery is intentionally bypassed, so the
        # script emits no certificate timing or status.
        certificate_cpu_seconds = 0.0
        certificate_status = "SKIPPED"
    return (
        PathfinderTrial(
            trial=trial,
            lowering_ns=lowering_ns,
            analysis_ns=analysis_ns,
            lifting_ns=lifting_ns,
            host_execution_and_certificate_wall_ns=execution.wall_ns,
            total_wall_ns=total_wall_ns,
            execution_cpu_seconds=execution.execution_cpu_seconds,
            certificate_cpu_seconds=certificate_cpu_seconds,
            peak_rss_kb=execution.peak_rss_kb,
            canonical_generators=execution.canonical_generators,
            certificate_status=certificate_status,
        ),
        lifted.canonical_route,
    )


def _integer_stats(values: list[int]) -> dict[str, int]:
    return {
        "minimum": min(values),
        "median": int(statistics.median(values)),
        "maximum": max(values),
    }


def _float_stats(values: list[float]) -> dict[str, float]:
    return {
        "minimum": min(values),
        "median": statistics.median(values),
        "maximum": max(values),
    }


def _m2_version() -> str:
    completed = subprocess.run(["M2", "--version"], capture_output=True, text=True, check=False)
    return (completed.stdout or completed.stderr).strip()


def _markdown(report: dict[str, object]) -> str:
    timing = report["timing_summary"]  # type: ignore[index]
    baseline = timing["baseline_total_wall_ns"]  # type: ignore[index]
    pathfinder = timing["pathfinder_total_wall_ns"]  # type: ignore[index]
    gate = report["release_gate"]  # type: ignore[index]
    return f'''# First M2 Pathfinder benchmark report

**Benchmark:** `{report["benchmark_id"]}`  
**Host:** {report["host_version"]}  
**Trials:** one excluded warm-up plus {report["measured_trials_per_route"]} cold processes per route  
**Result equivalence:** `{report["result_equivalence_status"]}`  
**Certificate:** `{report["certificate_status"]}`  
**Release timing gate:** `{"CLOSED" if gate["closed"] else "OPEN"}`

## Result

Both paths returned the canonical generators:

```text
{report["canonical_generators"]}
```

The structural route retained `J^2`; external replay also verified that `J` is not in the resulting ideal.

## Wall-clock measurements

| Route | Minimum | Median | Maximum | Peak RSS median |
|---|---:|---:|---:|---:|
| Generic saturation/elimination | {baseline["minimum"] / 1e9:.6f}s | {baseline["median"] / 1e9:.6f}s | {baseline["maximum"] / 1e9:.6f}s | {timing["baseline_peak_rss_kb"]["median"]} KiB |
| Wrapped Pathfinder structural route | {pathfinder["minimum"] / 1e9:.6f}s | {pathfinder["median"] / 1e9:.6f}s | {pathfinder["maximum"] / 1e9:.6f}s | {timing["pathfinder_peak_rss_kb"]["median"]} KiB |

Median speedup ratio `T_baseline / T_pathfinder`: **{report["speedup_ratio"]:.6f}x**.

Pathfinder total time includes lowering, core analysis/selection, route lifting, M2 process startup and model loading, selected-route execution, and external certificate replay. M2 execution and certificate CPU telemetry are recorded separately in the JSON report; the complete combined host-process wall time is used in `T_total`.

## Gate decision

`{gate["reason"]}`

No fabricated duration estimate participates in route selection. These are measurements taken after exact route admission and replay.
'''


def run_campaign(root: Path, trials: int, *, certified: bool = True) -> dict[str, object]:
    task = M2ContactProjectionTask(
        request_id="m2-even-contact-delta-slice-a-v1",
        model_path=root / "docs" / "files" / "horizon_wreath_inertia_model.m2",
        slice_assignments=(("N1", 4), ("N2", 8), ("N3", 12), ("N4", 20)),
    )
    run_dir = root / "benchmarks" / "results" / "pathfinder_m2_runs"
    run_dir.mkdir(parents=True, exist_ok=True)

    # Warm-up is intentionally excluded.
    _run_baseline(task, run_dir / "warmup_baseline.m2", 0)
    _run_pathfinder(task, run_dir / "warmup_pathfinder.m2", 0, certified=certified)

    baseline_trials: list[BaselineTrial] = []
    pathfinder_trials: list[PathfinderTrial] = []
    canonical_route = b""
    for trial in range(1, trials + 1):
        if trial % 2:
            baseline_trials.append(_run_baseline(task, run_dir / f"trial_{trial:02d}_baseline.m2", trial))
            pathfinder, canonical_route = _run_pathfinder(
                task, run_dir / f"trial_{trial:02d}_pathfinder.m2", trial, certified=certified
            )
        else:
            pathfinder, canonical_route = _run_pathfinder(
                task, run_dir / f"trial_{trial:02d}_pathfinder.m2", trial, certified=certified
            )
            baseline_trials.append(_run_baseline(task, run_dir / f"trial_{trial:02d}_baseline.m2", trial))
        pathfinder_trials.append(pathfinder)

    baseline_results = {trial.canonical_generators for trial in baseline_trials}
    pathfinder_results = {trial.canonical_generators for trial in pathfinder_trials}
    equivalent = len(baseline_results) == 1 and baseline_results == pathfinder_results
    certificates_closed = all(trial.certificate_status == "CLOSED" for trial in pathfinder_trials)
    baseline_wall = [trial.total_wall_ns for trial in baseline_trials]
    pathfinder_wall = [trial.total_wall_ns for trial in pathfinder_trials]
    baseline_median = statistics.median(baseline_wall)
    pathfinder_median = statistics.median(pathfinder_wall)
    speedup = baseline_median / pathfinder_median
    if not certified:
        # Route-only mode delivers an uncertified result, so the release gate is
        # not evaluated regardless of timing; correctness equivalence still is.
        release_closed = False
        reason = (
            "Route-only mode: certified delivery bypassed, so the release gate is not evaluated. "
            + (
                "Exact result equivalence with the baseline still held."
                if equivalent
                else "Result equivalence with the baseline FAILED."
            )
        )
    else:
        release_closed = equivalent and certificates_closed and pathfinder_median < baseline_median
        reason = (
            "Exact equivalence and external certificates passed; wrapped Pathfinder median is below baseline."
            if release_closed
            else "Correctness passed, but the wrapped Pathfinder median is not below baseline; no speedup is claimed."
        )

    generators = next(iter(pathfinder_results)) if pathfinder_results else ()
    report: dict[str, object] = {
        "benchmark_id": task.request_id,
        "source_document": "benchmarks/FIRST_M2_FIXTURE.md",
        "host_version": _m2_version(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "logical_cpu_count": os.cpu_count(),
        "cold_warm_policy": "one excluded warm-up per route; every measured trial is a separate cold M2 process",
        "measured_trials_per_route": trials,
        "mathematical_target": "exact even-contact/difference-divisor sliced base-image ideal with doubled J node",
        "baseline_route": "saturate(Ceven + IZ + sliceA, ideal(M)); eliminate sheetVars",
        "pathfinder_route": "contact_restriction",
        "delivery_mode": "certified" if certified else "route-only",
        "route_evidence": {
            "sign_product": 1,
            "characteristic": 0,
            "restricted_generator_identity": "delta|Ceven = -16*J^2",
            "canonical_route_sha256": hashlib.sha256(canonical_route).hexdigest(),
        },
        "canonical_generators": list(generators),
        "timing_summary": {
            "baseline_total_wall_ns": _integer_stats(baseline_wall),
            "pathfinder_wrapper_lowering_ns": _integer_stats([trial.lowering_ns for trial in pathfinder_trials]),
            "pathfinder_analysis_ns": _integer_stats([trial.analysis_ns for trial in pathfinder_trials]),
            "pathfinder_wrapper_lifting_ns": _integer_stats([trial.lifting_ns for trial in pathfinder_trials]),
            "pathfinder_host_execution_and_certificate_wall_ns": _integer_stats(
                [trial.host_execution_and_certificate_wall_ns for trial in pathfinder_trials]
            ),
            "pathfinder_execution_cpu_seconds": _float_stats(
                [trial.execution_cpu_seconds for trial in pathfinder_trials]
            ),
            "pathfinder_certificate_cpu_seconds": _float_stats(
                [trial.certificate_cpu_seconds for trial in pathfinder_trials]
            ),
            "pathfinder_total_wall_ns": _integer_stats(pathfinder_wall),
            "baseline_peak_rss_kb": _integer_stats([trial.peak_rss_kb for trial in baseline_trials]),
            "pathfinder_peak_rss_kb": _integer_stats([trial.peak_rss_kb for trial in pathfinder_trials]),
        },
        "speedup_ratio": speedup,
        "result_equivalence_status": "exact-generator-equivalence" if equivalent else "FAILED",
        "certificate_status": (
            "route-only-bypassed"
            if not certified
            else "external-replay-closed"
            if certificates_closed
            else "FAILED"
        ),
        "release_gate": {"closed": release_closed, "reason": reason},
        "baseline_trials": [asdict(trial) for trial in baseline_trials],
        "pathfinder_trials": [asdict(trial) for trial in pathfinder_trials],
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--trials", type=int, default=7)
    parser.add_argument(
        "--route-only",
        action="store_true",
        help="Bypass certified delivery: lift and run only the route's execution block, "
        "skip the external certificate replay, and do not evaluate the release gate.",
    )
    args = parser.parse_args()
    certified = not args.route_only
    minimum_trials = 1 if args.route_only else 7
    if args.trials < minimum_trials:
        parser.error(
            "route-only runs require at least one measured trial"
            if args.route_only
            else "the release campaign requires at least seven measured trials"
        )
    report = run_campaign(args.root.resolve(), args.trials, certified=certified)
    results = args.root / "benchmarks" / "results"
    results.mkdir(parents=True, exist_ok=True)
    # Route-only runs are uncertified and must not overwrite the certified release report.
    stem = "FIRST_M2_REPORT" if certified else "FIRST_M2_REPORT_ROUTE_ONLY"
    json_path = results / f"{stem}.json"
    markdown_path = results / f"{stem}.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    markdown_path.write_text(_markdown(report))
    print(markdown_path)
    print(json_path)
    print("DELIVERY_MODE=" + str(report["delivery_mode"]))  # type: ignore[index]
    print("RELEASE_GATE=" + ("CLOSED" if report["release_gate"]["closed"] else "OPEN"))  # type: ignore[index]
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
