# FLAGSHIP STAGE A REPORT — QUADRATIC LAYER (SHAPE READOUT arm)
**Date:** 2026-07-03 · **Prereg:** `FLAGSHIP_STAGE_A_PREREG.md`, pin `d5e69a10fee4897d` (FROZEN pre-battery, commit `4f2269d`, on origin via merge `975ab59`) · **Battery:** `flagship_stageA_battery.py` (`81bc3de5`) — engine_harness consumer, gates green every invocation.

## Substrate ruling (in ink)
Prereg §9 named the container primary as a continuity convention. The container silently died twice inside the hunt's Branch G (OOM signature: no traceback, no flag; first during symbolic assembly, second during the interpolation grid), while the box completed the identical deterministic schedule **twice, byte-stable, sha `268f6fe00d77f51a`**, with all pre-hunt sections' heartbeats matching the container's before each death. **Will's ruling, verbatim: "grade on box."** FA.7 calibration re-run on the box immediately pre-grading: PA.1 PASS ×2. Additional instrument defect banked: the container liveness poll self-matched its own probe cmdline (`pgrep -f`) for several turns — polls now discount self-matches.

## Verdicts (graded on box ×2, sha 268f6fe00d77f51a)
| clause | statement (abbrev.) | verdict |
|---|---|---|
| FA.1 | Molien a₂ = 3 at n = 5, 6, 7 | **PASS** — (3, 3, 3) exact |
| FA.2 | FS indicators +1 ×3λ ×3n; trace Gram diagonal = ranks | **PASS** — all exact |
| FA.3 | sweep: every nonzero-δ pair separated by m2_shape | **PASS** — 120/120 nonzero-δ, 120/120 separated, zero ties |
| FA.4 | σ-tie (Ê_r equal, r=1..4) on every sweep pair | **PASS** — 120/120 |
| FA.5 | hunt terminates in the frozen outcome enum | **PASS** — INCONCLUSIVE_BUDGET (all 8 eliminations capped at 600 s) |
| FA.6 | relabeling invariance control per n | **PASS** ×3 |
| FA.7 | witness calibration on primary pre-grading | **PASS** — PA.1 on box, 0.29/0.27 s |
Kills K-FA1/2/3 armed; none fired. Byte-stability ×2 on the graded substrate; cross-substrate agreement on every section the container completed before dying.

## Status moves
- **CL-F1 → PROVEN.** Certificates FA.1+FA.2 green at n = 5, 6, 7; `PROOF_CL_F1.md` supplies the classical mechanism (multiplicity-freeness + Schur + FS(+1) ⟹ dim(Sym²M*)^{Sₙ} = 3; the three trace-orthogonal moments are a basis). Proof doc routed to Will for the judgment-class read; no novelty claimed for F1 itself (brief §1 crown restriction).
- **CL-F2 → EMPIRICAL** at 120/120 across n = 5, 6, 7. Structural upgrade requires mechanism work, not more sweep.
- **P-F1 → CERTIFIED** (the ×3-values-of-n Molien check complete; a₂ = 3 everywhere).
- **P-F3 → OPEN, with structure banked.** The v1 hunt graded INCONCLUSIVE_BUDGET as frozen. The route-(b) follow-up (HUNT_ADDENDUM v2 → v2.3, msolve engine) found: on all eight slice families the tie locus is **dimension 1** — certified per slice by 0-dimensional plane sections — with 32 blind sections rational-point-free, section eliminants irreducible of degree 12, saturation multiplicities (2,2) uniform, parametrization tangent rank 3 [two exact secant scales], and H simple-spectrum [CERTIFIED]. Over ℚ̄ the witnesses form curves on every slice; ℚ-rationality is the open question. Mechanism probe (a″) authorized by Will.

## Ladder-forcing corollary (banked)
Degree-2 + σ supply ≤ n+2 invariants against fiber dimension n(n−1)/2 − (n−1); with CL-F1 PROVEN and the witness σ-blindness, the climb to degree 3 is forced by count — Stage B's mandate, independent of P-F3's witness status.
