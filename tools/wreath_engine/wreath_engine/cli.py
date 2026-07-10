"""Human CLI: drive the pipeline without MCP.

  wreath-engine analyze  <spec.json>
  wreath-engine verify   <spec.json> [--timeout N]
  wreath-engine lift     <spec.json>
  wreath-engine inertia  <spec.json>
  wreath-engine realize  <spec.json> [--decomp] [--timeout N]
  wreath-engine explore  <spec.json> --gens "g1; g2; ..."
  wreath-engine report   <spec.json>
  wreath-engine inspect  [run_id]
  wreath-engine jobs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import jobs, pipeline, report, spec as spec_mod


def _print(env: dict) -> int:
    json.dump(env, sys.stdout, indent=2, default=str)
    print()
    return 0 if env.get("status") not in ("error", "refuted") else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="wreath-engine")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("analyze", "verify", "lift", "inertia", "realize",
                 "explore", "report"):
        p = sub.add_parser(name)
        p.add_argument("spec")
        p.add_argument("--timeout", type=float, default=3600.0)
        if name == "realize":
            p.add_argument("--decomp", action="store_true")
        if name == "explore":
            p.add_argument("--gens", required=True,
                           help="candidate divisor generators, ';'-separated")
    p = sub.add_parser("inspect")
    p.add_argument("run_id", nargs="?")
    sub.add_parser("jobs")
    args = ap.parse_args(argv)

    if args.cmd == "inspect":
        return _print(pipeline.inspect_certificate(args.run_id))
    if args.cmd == "jobs":
        return _print(jobs.list_jobs())

    try:
        ps = spec_mod.load(args.spec)
    except spec_mod.SpecError as exc:
        return _print({"status": "error", "error": str(exc)})

    if args.cmd == "analyze":
        return _print(pipeline.analyze_kummer_module(ps))
    if args.cmd == "verify":
        env = pipeline.verify_valuation_matrix(ps, timeout=args.timeout)
        _write_report(ps, env)
        return _print(env)
    if args.cmd == "lift":
        return _print(pipeline.compute_wreath_lift(ps))
    if args.cmd == "inertia":
        return _print(pipeline.classify_inertia(ps))
    if args.cmd == "realize":
        env = pipeline.realize_branch_poset(
            ps, include_decompositions=args.decomp, timeout=args.timeout)
        return _print(env)
    if args.cmd == "explore":
        gens = [g.strip() for g in args.gens.split(";") if g.strip()]
        return _print(pipeline.suggest_parity_rows(ps, gens, timeout=args.timeout))
    if args.cmd == "report":
        verify_env = pipeline.latest_result(ps, "verify")
        realize_env = pipeline.latest_result(ps, "realize")
        lift_env = pipeline.compute_wreath_lift(ps)
        inertia_env = pipeline.classify_inertia(ps)
        print(report.render(ps, verify_env, lift_env, inertia_env, realize_env))
        return 0
    return 2


def _write_report(ps, verify_env: dict) -> None:
    run_id = verify_env.get("run_id")
    if not run_id:
        return
    run_dir = Path(verify_env["certificate_files"][0]).parent if \
        verify_env.get("certificate_files") else None
    if run_dir and run_dir.is_dir():
        lift_env = pipeline.compute_wreath_lift(ps)
        inertia_env = pipeline.classify_inertia(ps)
        (run_dir / "report.md").write_text(
            report.render(ps, verify_env, lift_env, inertia_env))


if __name__ == "__main__":
    sys.exit(main())
