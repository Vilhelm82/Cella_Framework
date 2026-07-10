"""High-level orchestration: the tool semantics shared by CLI and MCP server.

Every function returns a result envelope dict:
  status: certified | claimed | refuted | exploratory | error
plus tool-specific fields. Fields that don't apply are omitted.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import f2, m2gen, m2run
from .spec import ProblemSpec

ENGINE_VERSION = "0.1.0"


def _b_matrix(ps: ProblemSpec) -> list[list[int]]:
    return [list(d.claimed_parity_row) for d in ps.divisors]


def _wreath_facts(ps: ProblemSpec, certified: bool) -> dict:
    b = _b_matrix(ps)
    rank_b = f2.rank(b)
    s, d = ps.s, ps.d
    maximal = rank_b == s and len(b) >= s
    facts = {
        "base_group": ps.base_cover.group.name,
        "degree": d,
        "channels": s,
        "valuation_matrix": b,
        "sheet_matrix_rank": rank_b,
        "orbit_matrix_rank": f2.orbit_rank(b, d) if maximal else rank_b * d,
        "maximal_rank": maximal,
    }
    if maximal:
        facts.update({
            "kummer_rank": s * d,
            "index_H_over_K": f"2^{s}",
            "index_L_over_E": f"2^{s * d}",
            "closure_group": f"C_2^{s} wr {ps.base_cover.group.name}",
            "closure_order": (2 ** (s * d)) * ps.base_cover.group.order,
        })
    else:
        kernel = f2.kernel_basis(b)
        facts.update({
            "kummer_rank_upper_bound": rank_b * d,
            "kernel_basis": kernel,
            "kernel_note": "nonzero kernel = explicit square-class relation "
                           "module among the channels at the chosen divisors "
                           "(theorem report section 8); the wreath conclusion "
                           "cannot be promoted",
        })
    facts["status"] = ("certified" if certified and maximal else
                       "refuted" if certified and not maximal else
                       "claimed")
    return facts


def analyze_kummer_module(ps: ProblemSpec) -> dict:
    """F2 bookkeeping only — no M2, so at best status 'claimed'."""
    facts = _wreath_facts(ps, certified=False)
    facts["status"] = "claimed"
    facts["warnings"] = [
        "parity rows are as claimed in the spec; run verify_valuation_matrix "
        "to certify them"
    ]
    return facts


def _gate_verdicts(results: list[dict]) -> tuple[bool, list[dict], list[str]]:
    """(all_passed, gate list, warnings) from parsed M2 result blocks."""
    gates, warnings = [], []
    all_passed = True
    for r in results:
        if r.get("kind") in ("structural", "charpoly", "gate"):
            entry = {k: v for k, v in r.items() if k != "kind"}
            entry["kind"] = r["kind"]
            gates.append(entry)
            if r.get("bound_hit"):
                warnings.append(
                    f"symbolic-power bound hit at divisor {r.get('divisor')} "
                    f"channel {r.get('channel')} — raise the order bound or use a slice"
                )
                all_passed = False
            if r.get("pass") is False:
                all_passed = False
    return all_passed, gates, warnings


def verify_valuation_matrix(ps: ProblemSpec, root: Path | None = None,
                            timeout: float = m2run.DEFAULT_TIMEOUT) -> dict:
    """The certified core: run the generated checklist script in M2."""
    run_dir = m2run.new_run_dir(ps, "verify", root)
    try:
        m2res = m2run.run_script(m2gen.generate_verify(ps), run_dir, "verify", timeout)
    except m2run.M2Error as exc:
        envelope = {
            "status": "error", "error": str(exc), "log_tail": exc.log_tail,
            "run_id": run_dir.name,
            "certificate_files": [str(p) for p in sorted(run_dir.iterdir())],
        }
        _persist(run_dir, envelope)
        return envelope
    all_passed, gates, warnings = _gate_verdicts(m2res.results)
    failed = [g for g in gates if g.get("pass") is False]
    envelope = _wreath_facts(ps, certified=all_passed)
    if not all_passed:
        envelope["status"] = "refuted"
        envelope["failed_gates"] = failed
    envelope.update({
        "run_id": run_dir.name,
        "gates": gates,
        "elapsed_seconds": round(m2res.elapsed, 1),
        "certificate_files": [str(m2res.script_path), str(m2res.output_path)],
        "warnings": warnings,
    })
    _persist(run_dir, envelope)
    return envelope


def compute_wreath_lift(ps: ProblemSpec, root: Path | None = None) -> dict:
    """Combine the latest verification certificate with the F2 facts."""
    prior = latest_result(ps, "verify", root)
    if prior is None or prior.get("status") == "error":
        env = _wreath_facts(ps, certified=False)
        env["status"] = "claimed"
        env["warnings"] = ["no verification certificate found for this spec "
                           "(matching by content hash); run verify_valuation_matrix"]
        return env
    env = _wreath_facts(ps, certified=(prior["status"] == "certified"))
    env["verified_by_run"] = prior.get("run_id")
    if prior["status"] == "refuted":
        env["status"] = "refuted"
        env["failed_gates"] = prior.get("failed_gates", [])
    env["certificate_files"] = prior.get("certificate_files", [])
    return env


def classify_inertia(ps: ProblemSpec, root: Path | None = None) -> dict:
    """Colored inertia table from the verified parity rows (theorem section 7):
    each divisor's row, viewed in W-dual, is the tame inertia generator; the
    colored class pairs the sign vector with the base cycle data."""
    prior = latest_result(ps, "verify", root)
    certified = prior is not None and prior.get("status") == "certified"
    cycles = {c.get("divisor"): c.get("cycles", "trivial")
              for c in ps.base_cycle_data if isinstance(c, dict)}
    table = []
    for dv in ps.divisors:
        row = list(dv.claimed_parity_row)
        table.append({
            "divisor": dv.name,
            "type": dv.type,
            "sign_vector": row,
            "kummer_inertia_order": 2 if any(row) else 1,
            "base_cycles": cycles.get(dv.name, "trivial"),
            "action": " ".join(
                f"sqrt({ch.name})->{'-' if row[i] else '+'}sqrt({ch.name})"
                for i, ch in enumerate(ps.channels)
            ),
        })
    return {
        "status": "certified" if certified else "claimed",
        "inertia_table": table,
        "verified_by_run": prior.get("run_id") if prior else None,
        "warnings": [] if certified else [
            "table reflects claimed parity rows; certify with verify_valuation_matrix"
        ],
    }


def realize_branch_poset(ps: ProblemSpec, root: Path | None = None,
                         include_decompositions: bool = False,
                         timeout: float = m2run.DEFAULT_TIMEOUT) -> dict:
    run_dir = m2run.new_run_dir(ps, "realize", root)
    try:
        fast = m2run.run_script(m2gen.generate_realize_fast(ps), run_dir,
                                "realize_fast", timeout)
        results = list(fast.results)
        files = [str(fast.script_path), str(fast.output_path)]
        if include_decompositions:
            dec = m2run.run_script(m2gen.generate_realize_decomp(ps), run_dir,
                                   "realize_decomp", timeout)
            results += dec.results
            files += [str(dec.script_path), str(dec.output_path)]
    except m2run.M2Error as exc:
        envelope = {"status": "error", "error": str(exc),
                    "log_tail": exc.log_tail, "run_id": run_dir.name}
        _persist(run_dir, envelope)
        return envelope
    walls = [r for r in results if r.get("stage") == "contact_wall"]
    table = [r for r in results if r.get("stage") == "incidence_table"]
    slices = [r for r in results if r.get("stage", "").startswith("slice_")]
    decomp = [r for r in results if r.get("stage", "").startswith("channel_")]
    structural = [r for r in results if r.get("kind") == "structural"]
    ok = all(r.get("pass") is not False for r in walls + structural)
    envelope = {
        "status": "certified" if ok else "refuted",
        "run_id": run_dir.name,
        "structural": structural,
        "contact_walls": walls,
        "incidence_table": table,
        "slices": slices,
        "decompositions": decomp,
        "certificate_files": files,
        "warnings": [] if include_decompositions else
            ["decomposition stage skipped (include_decompositions=false); "
             "primality of channel divisors not checked in this run"],
    }
    _persist(run_dir, envelope)
    return envelope


def suggest_parity_rows(ps: ProblemSpec, divisor_gens: list[str],
                        root: Path | None = None,
                        timeout: float = m2run.DEFAULT_TIMEOUT) -> dict:
    run_dir = m2run.new_run_dir(ps, "explore", root)
    try:
        m2res = m2run.run_script(
            m2gen.generate_explore_parity(ps, divisor_gens), run_dir,
            "explore", timeout)
    except m2run.M2Error as exc:
        return {"status": "error", "error": str(exc), "log_tail": exc.log_tail}
    components = [r for r in m2res.results if "parity_row" in r]
    envelope = {
        "status": "exploratory",
        "run_id": run_dir.name,
        "candidate_gens": divisor_gens,
        "components": components,
        "channel_order": [c.name for c in ps.channels],
        "warnings": ["exploratory only — parity rows here certify nothing; "
                     "add the divisor to the spec and run verify_valuation_matrix"],
    }
    _persist(run_dir, envelope)
    return envelope


def inspect_certificate(run_id: str | None = None, root: Path | None = None) -> dict:
    rr = m2run.runs_root(str(root) if root else None)
    if run_id is None:
        runs = sorted(p.name for p in rr.iterdir() if p.is_dir())
        return {"status": "certified", "runs": runs}
    run_dir = rr / run_id
    if not run_dir.is_dir():
        return {"status": "error", "error": f"no run named {run_id}"}
    files = {p.name: p.stat().st_size for p in sorted(run_dir.iterdir())}
    result = {}
    result_file = run_dir / "result.json"
    if result_file.exists():
        result = json.loads(result_file.read_text())
    return {"status": "certified", "run_id": run_id, "files": files,
            "result": result}


def latest_result(ps: ProblemSpec, purpose: str, root: Path | None = None) -> dict | None:
    rr = m2run.runs_root(str(root) if root else None)
    suffix = f"_{ps.name}_{purpose}_{ps.content_hash()}"
    candidates = sorted(p for p in rr.iterdir()
                        if p.is_dir() and p.name.endswith(suffix))
    for run_dir in reversed(candidates):
        result_file = run_dir / "result.json"
        if result_file.exists():
            return json.loads(result_file.read_text())
    return None


def _persist(run_dir: Path, envelope: dict) -> None:
    (run_dir / "result.json").write_text(json.dumps(envelope, indent=2))
