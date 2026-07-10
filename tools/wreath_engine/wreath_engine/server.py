"""MCP server: the validated boundary in front of the Macaulay2 authority.

Tools mirror the design doc. Results are envelopes with
status in {certified, claimed, refuted, exploratory, error}; "certified" is
only ever returned when the mathematical gates ran in M2 and the
script+output certificate pair is on disk under runs/.
"""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from . import jobs, m2gen, m2run, m2session, pipeline, report, spec as spec_mod

mcp = FastMCP("wreath-engine")

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def _load(spec: dict | None, spec_path: str | None) -> spec_mod.ProblemSpec | dict:
    try:
        if spec is not None:
            return spec_mod.validate(spec)
        if spec_path is not None:
            return spec_mod.load(spec_path)
    except (spec_mod.SpecError, OSError, json.JSONDecodeError) as exc:
        return {"status": "error", "error": str(exc)}
    return {"status": "error",
            "error": "provide either spec (object) or spec_path (string); "
                     f"example specs live in {EXAMPLES}"}


@mcp.tool()
def analyze_kummer_module(spec: dict | None = None,
                          spec_path: str | None = None) -> dict:
    """Validate a problem spec and compute the F2 bookkeeping from the CLAIMED
    parity rows: sheet-level matrix B, its rank and kernel, the orbit matrix
    rank, and the candidate wreath closure. No Macaulay2 runs, so the result
    is at best status 'claimed'. Rank-deficient B returns the kernel basis
    (the square-class relation module)."""
    ps = _load(spec, spec_path)
    if isinstance(ps, dict):
        return ps
    return pipeline.analyze_kummer_module(ps)


@mcp.tool()
def verify_valuation_matrix(spec: dict | None = None,
                            spec_path: str | None = None,
                            timeout_seconds: float = 3600.0) -> dict:
    """Certify the parity matrix in Macaulay2: for every divisor, check
    prime-upstairs, unramifiedness, regularity, on-sheet valuation parity
    (bounded symbolic powers), off-sheet evenness (norm valuation equals
    on-sheet order), and the expected wall image. All-pass promotes the spec's
    matrix to 'certified'; any failure returns 'refuted' with the failed
    gates. Certificates (script + verbatim output) land under runs/.
    For long verifications use start_verification instead."""
    ps = _load(spec, spec_path)
    if isinstance(ps, dict):
        return ps
    return pipeline.verify_valuation_matrix(ps, timeout=timeout_seconds)


@mcp.tool()
def compute_wreath_lift(spec: dict | None = None,
                        spec_path: str | None = None) -> dict:
    """Combine the latest verification certificate for this spec (matched by
    content hash) with the F2 facts: Kummer rank, [H:K], and the wreath
    closure C_2^s wr G with its order — 'certified' only when a verification
    run certified the matrix, 'refuted' with the kernel if rank fails."""
    ps = _load(spec, spec_path)
    if isinstance(ps, dict):
        return ps
    return pipeline.compute_wreath_lift(ps)


@mcp.tool()
def classify_inertia(spec: dict | None = None,
                     spec_path: str | None = None) -> dict:
    """Colored inertia table (theorem section 7): per divisor, the Kummer sign
    vector (its parity row, acting as the tame inertia involution on the
    channel square roots) paired with base cycle data from the spec."""
    ps = _load(spec, spec_path)
    if isinstance(ps, dict):
        return ps
    return pipeline.classify_inertia(ps)


@mcp.tool()
def realize_branch_poset(spec: dict | None = None,
                         spec_path: str | None = None,
                         include_decompositions: bool = False,
                         timeout_seconds: float = 3600.0) -> dict:
    """Run the generated realization pipeline in Macaulay2: structural
    assertions, contact-wall images, the incidence table (codim, degree,
    generic-saturation emptiness for IR, divisors, channel divisors and their
    meets), and exact rational slices. include_decompositions adds
    minimalPrimes/primaryDecomposition of every channel divisor (slow — use
    start_realization for that)."""
    ps = _load(spec, spec_path)
    if isinstance(ps, dict):
        return ps
    return pipeline.realize_branch_poset(
        ps, include_decompositions=include_decompositions,
        timeout=timeout_seconds)


@mcp.tool()
def suggest_parity_rows(spec: dict | None = None,
                        spec_path: str | None = None,
                        divisor_gens: list[str] | None = None,
                        timeout_seconds: float = 600.0) -> dict:
    """EXPLORATORY (never certifies): probe a candidate divisor's valuation
    parities on every component it decomposes into. Use to find divisors
    worth adding to the spec; then run verify_valuation_matrix. Runs in a
    persistent M2 session for responsiveness, falling back to batch."""
    ps = _load(spec, spec_path)
    if isinstance(ps, dict):
        return ps
    if not divisor_gens:
        return {"status": "error", "error": "divisor_gens required"}
    try:
        script = m2gen.generate_explore_parity(ps, divisor_gens)
        results = m2session.shared_session().run(script, timeout=timeout_seconds)
        return {
            "status": "exploratory",
            "candidate_gens": divisor_gens,
            "components": [r for r in results if "parity_row" in r],
            "channel_order": [c.name for c in ps.channels],
            "warnings": ["exploratory only — parity rows here certify nothing"],
        }
    except m2run.M2Error:
        return pipeline.suggest_parity_rows(ps, divisor_gens,
                                            timeout=timeout_seconds)


@mcp.tool()
def inspect_certificate(run_id: str | None = None) -> dict:
    """List runs (no run_id) or return one run's artifact index and stored
    result envelope. Never recomputes anything."""
    return pipeline.inspect_certificate(run_id)


@mcp.tool()
def render_report(spec: dict | None = None,
                  spec_path: str | None = None) -> dict:
    """Assemble the markdown certificate report for a spec from its latest
    verification and realization runs."""
    ps = _load(spec, spec_path)
    if isinstance(ps, dict):
        return ps
    verify_env = pipeline.latest_result(ps, "verify")
    realize_env = pipeline.latest_result(ps, "realize")
    lift_env = pipeline.compute_wreath_lift(ps)
    inertia_env = pipeline.classify_inertia(ps)
    return {"status": lift_env.get("status", "claimed"),
            "markdown": report.render(ps, verify_env, lift_env,
                                      inertia_env, realize_env)}


@mcp.tool()
def start_verification(spec: dict | None = None,
                       spec_path: str | None = None,
                       timeout_seconds: float = 7200.0) -> dict:
    """Async verify_valuation_matrix for long runs (e.g. private divisors
    whose primality check takes minutes). Returns a job_id; poll with
    get_job_status, collect with get_job_result."""
    ps = _load(spec, spec_path)
    if isinstance(ps, dict):
        return ps
    return jobs.start_job(ps, "verify", timeout=timeout_seconds)


@mcp.tool()
def start_realization(spec: dict | None = None,
                      spec_path: str | None = None,
                      include_decompositions: bool = True,
                      timeout_seconds: float = 7200.0) -> dict:
    """Async realize_branch_poset, by default including the slow
    decomposition stage. Returns a job_id."""
    ps = _load(spec, spec_path)
    if isinstance(ps, dict):
        return ps
    kind = "realize_full" if include_decompositions else "realize"
    return jobs.start_job(ps, kind, timeout=timeout_seconds)


@mcp.tool()
def get_job_status(job_id: str) -> dict:
    """State of an async job: running | done | failed | cancelled."""
    return jobs.job_status(job_id)


@mcp.tool()
def get_job_result(job_id: str) -> dict:
    """Result envelope of a finished async job."""
    return jobs.job_result(job_id)


@mcp.tool()
def cancel_job(job_id: str) -> dict:
    """Cancel a running job (SIGTERM then SIGKILL to the process group)."""
    return jobs.cancel_job(job_id)


@mcp.tool()
def list_jobs() -> dict:
    """All known async jobs with their states."""
    return jobs.list_jobs()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
