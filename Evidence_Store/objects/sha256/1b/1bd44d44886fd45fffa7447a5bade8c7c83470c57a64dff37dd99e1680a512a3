# Claude Code Task 2 of 3 — Build_Docs Cleanup (debloat)

**Date:** 2026-05-30
**Mode:** Proposal-first, then reversible execution behind an approval gate. No hard deletes, ever.
**Sequence:** Run AFTER task 1 (`HISTORICAL_RECORD.md` must exist) and BEFORE task 3. Task 1's record is the authority for what is superseded. Task 3's index is written against the docs that survive this cleanup.
**Scope = the docs set, NOT the results set.** Operates on the design / architecture / rules / authority documents — the files that stipulate how V4 works — not on the results record (task 1). Build_Docs currently holds ~497 files; reduce the active doc surface to a lean canonical set.

---

## Goal
Cut the doc bloat so a new session faces a handful of canonical, current docs instead of hundreds. Reduction is by ARCHIVING (reversible), never deletion.

## Step 1 — Inventory + classify
Read every Build_Docs doc that is NOT a report (`Reports/`) and NOT a task spec (`Agent_tasks/`). Discover the full set; known members: `Architecture/AXIOMS.md`, `Architecture/VERA_REFERENCE_LEDGER.md`, `V4_GLOSSARY.md`, `LIVE_CAMPAIGNS_LEDGER.md`, `LAYER_MANIFEST*`, `where_i_got_stuck.md`, `transfer_function_exponent_family_v4.tex`, `session_handoff.md`, the repo `README.md`, and the parent `CLAUDE.md`.
Classify each against `HISTORICAL_RECORD.md`:
- `CANONICAL` — current source of truth.
- `LIVING` — must stay active and current (ledger, glossary; the index once task 3 builds it).
- `SUPERSEDED` — older version of a canonical doc, or a claim the record marks superseded (e.g. the `.tex`).
- `SCRATCH` — exploratory; keep but archive.
- `ORPHAN` — nothing references it.
- `DUPLICATE` — content-near-duplicate of another (name its twin).

## Step 2 — Propose the reduction (move nothing yet)
Produce `Build_Docs/CLEANUP_PLAN.md`: the full classified inventory + a concrete move-list. Everything not `CANONICAL`/`LIVING` -> `Build_Docs/_archive/`. For any `SUPERSEDED` authority doc (the `.tex` especially), state what supersedes it and where. You may *propose* content merges in the plan, but do not perform them in this task.

## Step 3 — Approval gate
Present `CLEANUP_PLAN.md` and STOP. Move nothing until the user approves the list (whole or edited).

## Step 4 — Execute (only after approval)
Apply the approved moves with `git mv` into `Build_Docs/_archive/`, so every move is reversible and shows in a diff. NEVER hard-delete. The user purges `_archive/` themselves later if they choose.

## Hard guarantees
- No file moves before the user approves the move-list. No hard deletes at any point.
- Touch only the docs set — nothing under `Reports/`, `src/`, `evals/`, `tests/`.
- Do not edit doc *contents* here (reduction is by moving whole files). Content merges are proposed only, executed in task 3 with approval.
- If scope or risk grows, STOP and report.

## Hand-off
After this completes, the active Build_Docs is the lean current set. That surviving set is the input task 3 writes the project index against.
