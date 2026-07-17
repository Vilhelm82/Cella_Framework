# Research evidence inventory

This is the primary evaluation surface for material that may be consolidated into
reports or selectively re-derived in Cella.

| Directory | Contents | Suggested treatment |
|---|---|---|
| `campaigns/` | Campaign preregistrations, records, manifests, results, and task specifications | Evaluate by campaign; extract exact claims, scope, and strongest certificate |
| `verification/` | Persistent evals, exploratory scripts, scratch probes, and gate demonstrations | Classify as clean, partial, broken, or report-only before reuse |
| `reports/` | V4 reports, audit trails, and captured outputs | Preferred source for report consolidation; cross-check against raw campaign records |
| `paper/` | Paper sources and publication planning artifacts | Treat claims as secondary until matched to reports or fresh verification |
| `derivations/` | Theorem notes paired with computational probes | Candidate derivations; review assumptions and source version before promotion |

Recommended evaluation order:

1. Read the origin corrections ledger at `archive/pre-canon/portfolio/20_SUPERSEDED_AND_CORRECTIONS.md`.
2. Select a campaign family and identify its final report, frozen manifest, raw record, and verifier.
3. Compare duplicate or superseded versions by content hash and scope.
4. Produce one consolidated report with explicit source paths and exclusions.
5. Admit or reimplement only after Cella-side re-verification.
