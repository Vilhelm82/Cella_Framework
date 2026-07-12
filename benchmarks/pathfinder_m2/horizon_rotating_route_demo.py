"""Durable route-demo: Pathfinder vs the horizon_rotating wreath-engine job.

Drives three routes end-to-end from the wreath-engine module and writes every
artifact into ``benchmarks/results/HORIZON_ROTATING_ROUTE_ONLY/``:

  route1_contact_orbit.m2 / .out.txt      signed_contact_orbit_projection (M2)
  route2_iz_primeness.m2 / .out.txt       kummer_finite_extension_primeness (M2)
  route3_wreath_closure.route.json        rotating_three_channel_wreath_closure
  SUMMARY.json                            module hash, per-route timing, certs
  REPORT.md                               human-readable summary

Usage:
    python benchmarks/pathfinder_m2/horizon_rotating_route_demo.py            # certified
    python benchmarks/pathfinder_m2/horizon_rotating_route_demo.py --route-only

Reference: wreath-engine verify job_20260711T033436, 961.3 s, 53 gates certified.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools" / "pathfinder_m2"))
sys.path.insert(0, str(ROOT / "tools" / "wreath_engine"))

from wreath_engine.spec import validate

from cella.pathfinder import Obligation, PathfinderRequest, plan_request
from cella.pathfinder.serialize import canonical_json_bytes
from cella_pathfinder_m2.execute import run_m2_script
from cella_pathfinder_m2.model import M2ContactOrbitTask, M2DifferenceIdealPrimenessTask
from cella_pathfinder_m2.wrapper import lift_route, lower_any_task

MODULE = ROOT / "tools" / "wreath_engine" / "examples" / "horizon_rotating.json"
MODEL = ROOT / "docs" / "files" / "horizon_wreath_inertia_model.m2"
OUT_DIR = ROOT / "benchmarks" / "results" / "HORIZON_ROTATING_ROUTE_DEMO"
REFERENCE_JOB = "job_20260711T033436_b19195"
REFERENCE_SECONDS = 961.3


def _cert_closed(stdout: str) -> bool:
    return "PATHFINDER_M2_CERTIFICATE=CLOSED" in stdout


def run(certified: bool) -> dict:
    spec = validate(json.loads(MODULE.read_text()))
    degree = spec.base_cover.degree
    channels = tuple(c.name for c in spec.channels)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mode = "certified" if certified else "route-only"

    routes: list[dict] = []
    started = time.perf_counter()

    # ---- Route 1: complete signed-contact orbit (M2) ----------------------
    orbit_outcome = plan_request(lower_any_task(M2ContactOrbitTask(
        request_id=f"{spec.name}-contact-orbit", model_path=MODEL)))
    assert orbit_outcome.route is not None
    orbit_lift = lift_route(orbit_outcome.route, certified=certified)
    (OUT_DIR / "route1_contact_orbit.m2").write_text(orbit_lift.script)
    t_before = time.perf_counter()
    orbit_exec = run_m2_script(
        orbit_lift.script, script_path=OUT_DIR / "route1_contact_orbit.m2",
        result_markers=("PATHFINDER_M2_RESULT_BEGIN", "PATHFINDER_M2_RESULT_END"))
    orbit_seconds = time.perf_counter() - t_before
    (OUT_DIR / "route1_contact_orbit.out.txt").write_text(orbit_exec.stdout)
    routes.append({
        "index": 1,
        "route_family": orbit_outcome.route.route_family,
        "executor": "macaulay2",
        "ordered_operations": [s.operation for s in orbit_outcome.route.ordered_steps],
        "walls_emitted": orbit_exec.stdout.count("matrix"),
        "certificate_obligations": list(orbit_lift.certificate_obligation_ids),
        "certificate_status": "closed" if _cert_closed(orbit_exec.stdout) else (
            "bypassed" if not certified else "FAILED"),
        "wall_seconds": round(orbit_seconds, 4),
        "script": "route1_contact_orbit.m2",
        "transcript": "route1_contact_orbit.out.txt",
    })

    # ---- Route 2: delta_private primeness through Kummer P4 (M2) -----------
    primeness_outcome = plan_request(lower_any_task(M2DifferenceIdealPrimenessTask(
        request_id=f"{spec.name}-delta-private-primeness", model_path=MODEL)))
    assert primeness_outcome.route is not None, primeness_outcome.refusal
    primeness_lift = lift_route(primeness_outcome.route, certified=certified)
    (OUT_DIR / "route2_iz_primeness.m2").write_text(primeness_lift.script)
    t_before = time.perf_counter()
    primeness_exec = run_m2_script(
        primeness_lift.script, script_path=OUT_DIR / "route2_iz_primeness.m2",
        result_markers=("PATHFINDER_M2_RESULT_BEGIN", "PATHFINDER_M2_RESULT_END"))
    primeness_seconds = time.perf_counter() - t_before
    (OUT_DIR / "route2_iz_primeness.out.txt").write_text(primeness_exec.stdout)
    routes.append({
        "index": 2,
        "route_family": primeness_outcome.route.route_family,
        "executor": "macaulay2",
        "ordered_operations": [s.operation for s in primeness_outcome.route.ordered_steps],
        "generators_returned": list(primeness_exec.canonical_generators),
        "avoids_generic_decomposition": "primaryDecomposition" not in primeness_lift.script,
        "certificate_obligations": list(primeness_lift.certificate_obligation_ids),
        "certificate_status": "closed" if _cert_closed(primeness_exec.stdout) else (
            "bypassed" if not certified else "FAILED"),
        "wall_seconds": round(primeness_seconds, 4),
        "script": "route2_iz_primeness.m2",
        "transcript": "route2_iz_primeness.out.txt",
    })

    # ---- Route 3: rotating wreath closure, planned from module rows --------
    width = len(channels) * degree
    parity_rows: list[tuple[int, ...]] = []
    for divisor in spec.divisors:
        for sheet in range(degree):
            row = [0] * width
            for channel_index, bit in enumerate(divisor.claimed_parity_row):
                if bit % 2:
                    row[channel_index * degree + sheet] = 1
            parity_rows.append(tuple(row))
    t_before = time.perf_counter()
    closure_outcome = plan_request(PathfinderRequest.create(
        request_id=f"{spec.name}-wreath-closure",
        target_obligation=Obligation(
            "rotating-wreath-closure",
            "Certify the augmented rotating closure group C_2^3 wr S_5.",
            "exact-group-certificate"),
        external_binding={"module": str(MODULE)},
        mathematical_context={
            "problem_shape": "rotating_wreath_closure",
            "characteristic": 0,
            "closure_scope": "augmented",
            "banked_base_group": spec.base_cover.group.name,
            "base_group_order": spec.base_cover.group.order,
            "primitivity_certificate": True,
            "standing_nonvanishing": True,
            "cover": {
                "degree": degree, "channels": channels,
                "base_group": spec.base_cover.group.name,
                "parity_rows": tuple(parity_rows),
            },
        },
        available_route_families=("rotating_three_channel_wreath_closure",)))
    closure_seconds = time.perf_counter() - t_before
    assert closure_outcome.route is not None, closure_outcome.refusal
    (OUT_DIR / "route3_wreath_closure.route.json").write_bytes(
        canonical_json_bytes(closure_outcome.route))
    closure_parameters: dict = {}
    for step in closure_outcome.route.ordered_steps:
        closure_parameters.update({k: v for k, v in step.parameters})
    routes.append({
        "index": 3,
        "route_family": closure_outcome.route.route_family,
        "executor": "native (no M2); group obligations belong to the wreath engine",
        "ordered_operations": [s.operation for s in closure_outcome.route.ordered_steps],
        "parity_matrix": f"{len(parity_rows)}x{width} from claimed_parity_rows",
        "f2_rank_discharged_in_core": closure_parameters.get("f2_rank"),
        "closure_group": "C_2^3 wr S_5",
        "closure_order": 3932160,
        "external_obligations": [o.obligation_id for o in closure_outcome.route.certificate_obligations],
        "certificate_status": "f2_rank discharged in-core; group obligations external",
        "wall_seconds": round(closure_seconds, 6),
        "route": "route3_wreath_closure.route.json",
    })

    total_seconds = time.perf_counter() - started
    m2_routes = [r for r in routes if r["executor"] == "macaulay2"]
    all_m2_closed = all(r["certificate_status"] == "closed" for r in m2_routes)

    summary = {
        "module": spec.name,
        "module_source": str(MODULE.relative_to(ROOT)),
        "module_content_hash": spec.content_hash(),
        "delivery_mode": mode,
        "cover_degree": degree,
        "channels": list(channels),
        "base_group": {"name": spec.base_cover.group.name, "order": spec.base_cover.group.order},
        "routes": routes,
        "total_wall_seconds": round(total_seconds, 4),
        "m2_certificate_replay": "all_closed" if all_m2_closed else (
            "bypassed" if not certified else "INCOMPLETE"),
        "reference_verify_job": REFERENCE_JOB,
        "reference_verify_seconds": REFERENCE_SECONDS,
        "reference_verify_gates": 53,
        "coverage_note": (
            "Routes cover the 16 contact walls, the delta_private primeness, and the "
            "rotating wreath-closure claim. The verify job's per-channel charpoly and "
            "structural gates are NOT covered by these routes."
        ),
    }
    (OUT_DIR / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT_DIR / "REPORT.md").write_text(_report(summary))
    return summary


def _report(summary: dict) -> str:
    rows = "\n".join(
        f"| {r['index']} | `{r['route_family']}` | {r['executor'].split(';')[0]} | "
        f"{r['wall_seconds']} s | {r['certificate_status']} |"
        for r in summary["routes"]
    )
    return f"""# Horizon-rotating Pathfinder route demo

**Module:** `{summary['module']}` (content hash `{summary['module_content_hash']}`)
**Source:** `{summary['module_source']}`
**Delivery mode:** `{summary['delivery_mode']}`
**Base group:** {summary['base_group']['name']} (order {summary['base_group']['order']}), cover degree {summary['cover_degree']}

## Routes planned from the module, executed end-to-end

| # | Route family | Executor | Wall time | Certificate |
|---|---|---|---:|---|
{rows}

**Total wall time:** {summary['total_wall_seconds']} s
**M2 certificate replay:** {summary['m2_certificate_replay']}

## Reference

Wreath-engine verify job `{summary['reference_verify_job']}`: **{summary['reference_verify_seconds']} s**,
{summary['reference_verify_gates']} gates, certified.

{summary['coverage_note']}

## Artifacts in this directory

- `route1_contact_orbit.m2` / `.out.txt` — the emitted M2 script and its full transcript
- `route2_iz_primeness.m2` / `.out.txt` — the Kummer primeness route and its transcript
- `route3_wreath_closure.route.json` — the native wreath-closure `ComputationalRoute` (canonical serialization)
- `SUMMARY.json` — machine-readable per-route timings, certificate status, and coverage
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--route-only", action="store_true",
                        help="Bypass certified delivery for the M2 routes.")
    args = parser.parse_args()
    summary = run(certified=not args.route_only)
    print(str(OUT_DIR / "SUMMARY.json"))
    print(str(OUT_DIR / "REPORT.md"))
    print(f"delivery_mode={summary['delivery_mode']}  "
          f"total={summary['total_wall_seconds']}s  "
          f"m2_replay={summary['m2_certificate_replay']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
