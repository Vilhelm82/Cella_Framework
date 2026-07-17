# Claude Code Workflow — Chronological Development Audit (READ-ONLY)

**Drafted:** 2026-05-30
**Runs in:** Claude Code dynamic workflow.
**SCOPE — READ-ONLY.** This audit only *reads* the project and *writes its own report documents*. It does
NOT edit, move, rename, archive, delete, or roll back anything. No engine, test, eval, or doc is modified.
The only new files are the reports in §7, written under `Build_Docs/Reports/_audit/`.

---

## 1. What this answers
Reconstruct the project's development chronologically and show whether work has drifted from the original
intent ("north star"). For each main build-progress point: what it set out to build, whether it delivered,
what the whole project looked like at that point, and how far that state sits from the north star.

## 2. Sources
- Engine: `src/lloyd_v4/**`
- Task history: `Build_Docs/Agent_tasks/`, `Build_Docs/Reports/`, git history, `../Docs/session_handoff_*.md`
- **Origin anchors (the north-star reference):** `Build_Docs/where_i_got_stuck.md` (Q1–Q6), the earliest
  reports/handoffs, the original framing.

## 3. Phase 1 — Engine capability map
What the engine can and cannot currently do, per module, test-backed; include layer-manifest lineage.
Read-only. → writes `Build_Docs/Reports/_audit/CAPABILITY_MAP.md`.

## 4. Phase 2 — Fix the North Star + find the build-progress points
1. From the origin anchors, state the original intent + Q1–Q6 in one **frozen** paragraph — the fixed
   reference every later state is measured against. Not revised by later evidence.
2. Segment the history into the main build-progress points (significant arcs / milestones), in chronological
   order.

## 5. Phase 3 — Arc State Reports (the fan-out; the core deliverable)
One agent per build-progress point, in chronological order, each carrying the prior report forward. Each
writes `Build_Docs/Reports/_audit/NN_<arc>.md` on this fixed template:
1. **What the arc set out to build** — its stated goal, from its handoff / brief / pre-registration.
2. **Did it accomplish that?** — delivered / partial / failed / pivoted, with evidence.
3. **Project state at completion** — point-in-time snapshot: what the engine could do, which layers existed,
   the then-active direction, what was open or blocked.
4. **North-star distance** — on-vector / advancing / diverging, in which dimension, with evidence.

The ordered set is a flipbook: read top to bottom, drift shows as the north-star distance trending away.
(The `substrate-construction-transplant-arc` gets a report like any other arc; its fields 2 and 4 should note
whether substrate work began before substrate-invariant-search Gate 2, per CLAUDE.md §9 "no designing ahead
of evidence." This is analysis only — no recommendation to act, no change proposed.)

## 6. Phase 4 — Adversarial check (read-only; sharpens the analysis)
Independent agents try to refute each report's "did it deliver" and "north-star distance" claims before they
are finalised. A claim stands only if the refutation fails. No file is changed — this only improves trust.

## 7. Outputs (all new, all under `Build_Docs/Reports/_audit/`)
1. `CAPABILITY_MAP.md` — current engine capabilities.
2. `NN_<arc>.md` — the Arc State Reports (the flipbook).
3. `DEVELOPMENT_TIMELINE.md` — index of the flipbook with the north-star-distance trend.
4. `DRIFT_SYNTHESIS.md` — overall finding: where the distance holds steady vs trends away, with evidence.

Nothing outside this directory is created or touched.

## 8. Hard guarantees (pass verbatim to every agent)
- **Read anything; write ONLY into `Build_Docs/Reports/_audit/`.** Do not edit, move, rename, delete, or
  git-modify any existing file. No archiving. No rollback. No substrate, test, or eval edits.
- Classify by evidence — git dates, file headers, the ledger, the layer manifest, the reconstructed timeline.
  Cite the evidence and a confidence level per claim.
- Reconstruct intent from the record; the **user is ground truth** on intent. Report "the record shows X;
  arc Y diverges from it" — do not assert the project's true intent or certify scientific correctness.
- Do not read V3-flagged material (CLAUDE.md §5).

## 9. Operational (dynamic workflow)
- Route mechanical stages (capability-map enumeration) to a cheaper model; keep the strong model for Phases
  2, 3, 4. Use `/effort xhigh` for maximum reasoning if you want it.
- Read commands are already allowlisted in `.claude/settings.local.json`.
- Up to 16 agents concurrent, 1,000 total; ~50 build-points fit easily. Watch with `/workflows`; don't exit
  mid-run (resume is in-session only).

## 10. Trigger prompt (paste into Claude Code on `snapshot/full-worktree-2026-05-30`)

> Create a workflow that runs the READ-ONLY chronological development audit at
> Build_Docs/Agent_tasks/claude_code_workflow_2026_05_30_chronological_drift_audit.md. It is read-only: read
> anything, but write only new report files under Build_Docs/Reports/_audit/, and edit/move/delete nothing
> else. Route mechanical stages to a cheaper model and keep the strongest model for the reasoning phases.
> Build the capability map (Phase 1); fix the North Star from the origin anchors and identify the main
> build-progress points (Phase 2); fan out one agent per build-progress point in chronological order to write
> an Arc State Report — intent / did-it-deliver / project-state-at-completion / north-star distance (Phase 3);
> run an adversarial check on those claims (Phase 4). Produce CAPABILITY_MAP.md, the per-arc reports,
> DEVELOPMENT_TIMELINE.md, and DRIFT_SYNTHESIS.md under Build_Docs/Reports/_audit/. Make no edits to any
> existing file.
