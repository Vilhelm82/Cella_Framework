# Claude Code Task 1 of 3 — V4 Historical Record

**Date:** 2026-05-30
**Mode:** READ-ONLY over results. Produces ONE new file: `Build_Docs/HISTORICAL_RECORD.md`. No derivations, no edits to src/evals/Reports, no deletions, no moves.
**Sequence:** Task 1 of 3. It produces the context that task 2 (Build_Docs cleanup) and task 3 (project index) depend on. Run it first.
**Not a drift audit.** Plain table. No north-star / flipbook framing, no LaTeX, no new theorems.

---

## Goal
A single canonical cross-reference of what the project has actually established, so any session can see — without hunting through 80+ report folders — which results are proven, partial, refuted, open, or superseded, and where each lives.

## Deliverable — `Build_Docs/HISTORICAL_RECORD.md`
One row per established result or task outcome. A table, not an essay.

Columns: `Result / claim (one line)` | `Status` | `Where it lives (exact path)` | `Date` | `Supersedes / superseded-by` | `Scope / caveat`
Status vocabulary: `PROVEN` | `PARTIAL` | `REFUTED` | `OPEN` | `SUPERSEDED`.

## Sources to read and reconcile, in order
1. `Build_Docs/Reports/_audit/01..15_*.md` — arc bodies already name results, locations, and partial/refuted nuance. Mine first.
2. Every `Build_Docs/Reports/*/closeout.md` (~20) — authoritative closed results.
3. Report `.md` in the ~60 folders with no `closeout.md` — record the real file (e.g. `task034_*_summary.md`).
4. `Build_Docs/LIVE_CAMPAIGNS_LEDGER.md` — "Recently closed", "Open questions", "Obs 1-7".
5. `Build_Docs/Agent_tasks/*.md` — what each task set out to do.
6. `../Docs/session_handoff_*.md` — session-level outcomes.

## Reconciliation rules (follow exactly)
- Ledger says "Closed" but an arc body says "partial" -> record `PARTIAL`, cite both, note the discrepancy.
- Conflict by date -> later supersedes earlier; link both directions. Claims in `transfer_function_exponent_family_v4.tex` (2026-05-14) are SUPERSEDED by the 2026-05-18 `c2_lattice_substrate_derivation`, `conjecture_c_proof_audit`, `c2_theorem_scope_gate` closeouts — flag every such case.
- Every row cites a real path. If a result lives only in memory or only in the `.tex`, it does not go in until a file backs it.
- One line per result. Do NOT restate or reconstruct proofs. This is an index.

## Hard guarantees
- READ-ONLY. The only new file is `Build_Docs/HISTORICAL_RECORD.md`. No other edits, deletions, or moves.
- NEVER re-derive, re-run, or re-verify. If a result looks unproven, mark `OPEN`; do not try to close it.
- No drift framing, no LaTeX, no new theorems. Plain table.
- If scope grows beyond this one file, STOP and report.

## Hand-off
This file is the context for task 2 (Build_Docs cleanup): it tells that task which results are load-bearing, hence which design/authority docs are current vs superseded. Do not start task 2 until this exists.
