# Claude Code Task 3 of 3 — Project Knowledge Index

**Date:** 2026-05-30
**Mode:** Reads the current (post-cleanup) docs + the historical record. Produces the consolidated, digestible orientation. Propose merges; execute a merge only on approval.
**Sequence:** Run LAST — after task 1 (`HISTORICAL_RECORD.md`) and task 2 (Build_Docs cleanup). It MUST be written against the docs that actually survive task 2, not the pre-cleanup pile.

---

## Goal
A single concise `PROJECT_INDEX.md` a new session reads at start to know, without hunting: (a) what V4 is and its design rules / architecture principles, (b) what already exists / is established, (c) the obvious open questions to start on. Orientation that prevents duplication by making the current state and open frontier obvious — not a reactive blocker.

## Step 1 — Consolidate the surviving design docs
Read the lean canonical design / architecture / rules docs left after task 2, plus `HISTORICAL_RECORD.md`. Where several docs cover the same ground, propose a cohesive merge into the smallest consistent set. Propose merges in a short plan; execute a merge only if the user approves it. No deletions (supersede via task 2's `_archive/`).

## Step 2 — Write `Build_Docs/PROJECT_INDEX.md` (the digestible front door)
Concise — readable in a few minutes. Contents:
- What V4 is (one paragraph) + the layer architecture in brief.
- The design rules / axioms in brief, each LINKING to its canonical doc — do not copy, link.
- What's established: link to `HISTORICAL_RECORD.md` (the proven / partial / refuted table).
- The current open questions / frontier, drawn from the `OPEN` rows of `HISTORICAL_RECORD.md` and from `LIVE_CAMPAIGNS_LEDGER.md`.
- A map of the living docs and where everything canonical now lives.

## Step 3 — Write the living-docs update protocol (anti-staleness)
Into `PROJECT_INDEX.md`, state explicitly and briefly:
- Which docs are LIVING: `PROJECT_INDEX.md`, `LIVE_CAMPAIGNS_LEDGER.md`, `V4_GLOSSARY.md`, `HISTORICAL_RECORD.md`.
- The rule: any session that changes project state updates the relevant living doc before it ends — new result -> `HISTORICAL_RECORD.md` + closeout; campaign change -> ledger; new/renamed term -> glossary; structural change -> `PROJECT_INDEX.md`.
- Add a one-line pointer at the top of the parent `CLAUDE.md`: "Session start: read `Lloyd_Engine_V4/Build_Docs/PROJECT_INDEX.md` first."

## Hard guarantees
- `PROJECT_INDEX.md` LINKS canonical docs; it does not duplicate their content (duplication is how docs go stale).
- Propose doc merges; execute a merge only with explicit user approval. No deletions.
- Keep it concise — if the index can't be read in a few minutes, it is too long; push detail back into the linked canonical docs.
- If scope grows, STOP and report.

## Result
Three artifacts then orient any new session: `PROJECT_INDEX.md` (what exists + rules + open questions), `HISTORICAL_RECORD.md` (what's proven), `LIVE_CAMPAIGNS_LEDGER.md` (what's in flight) — a lean, current, non-stale spine.
