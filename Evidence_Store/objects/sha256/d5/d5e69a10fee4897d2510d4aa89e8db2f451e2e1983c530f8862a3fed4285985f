# FLAGSHIP STAGE A PREREG — QUADRATIC LAYER (arm: SHAPE READOUT, campaigns/shape_witness/)
**Status: FROZEN at commit, pre-battery (no Stage A battery code exists at freeze time). Date 2026-07-03.**
**Authority:** flagship brief §6 Stage A (live pin `3b3fca4292bc8aa7`), activated by Will's "flagship Stage A" S-2026-07-03. Stage 0 state: calibration green, Molien counts recorded (WALL_VERDICT), wall measured — INCLUDED(6,7). PA-1/2/3 in force.

## 1. Scope (brief §6 Stage A verbatim): CL-F1 proof; CL-F2 sweep ×2 byte-stable; the P-F3 witness hunt. Plus P-F1 completion at n=5.

## 2. Definitions in force (DF-S1/S2, frozen in the brief; restated operationally)
Pair module `M = ℚ^{pairs(n)}` lex order; Sₙ acts by simultaneous relabeling of g-coordinates and pair indices; projectors P_triv/P_std/P_shape per rep_utils characters with witness gates; `O = O_of(H)` gauge-normal form; `Ê_r` = witness bordered-minor sums; `m2_X(O) = ⟨P_X O, O⟩` (ℓ² inner product, DF-S2); δ_shape = π_shape(O₁) − π_shape(O₂).
**Orbit-distinctness lemma (grading rule, one-line proof):** for g with pairwise-distinct entries, π·g = g ⟹ π = id; hence (g,O₁) ~ (g,O₂) under the simultaneous Sₙ action iff O₂ = O₁. A conjugation pair with equal g and O₂ ≠ O₁ is orbit-distinct. [PROVEN]

## 3. Frozen clauses (verbatim; battery embeds exactly, refuses on drift)
FA.1: exact Molien on the pair module gives degree-2 invariant count a2 = 3 at n=5, n=6, and n=7.
FA.2: Frobenius-Schur indicators equal +1 for lambda in {(n),(n-1,1),(n-2,2)} at n=5,6,7, and the trace Gram tr(P_X P_Y) = delta_XY * rank(P_X) holds exactly at n=5,6,7.
FA.3: over the pinned conjugation sweep (seed 20260703, 40 pairs per n at n=5,6,7), every pair with delta_shape != 0 satisfies m2_shape(O1) != m2_shape(O2); a tie is recorded verbatim and routed as a mechanism-extraction lead, never silently widened.
FA.4: on every sweep pair, Ehat_r(H1) = Ehat_r(H2) exactly for r=1..4 (the sigma-tie mechanism holds on the full sweep).
FA.5: the P-F3 hunt follows the pinned adaptive protocol of section 5 and terminates in exactly one of WITNESS_FOUND, INCONCLUSIVE_BUDGET, or OBSTRUCTION_RECORDED; a found witness is certified by exact Ehat ties r=1..4, exact ties in all three m2's, O2 != O1, and pairwise-distinct g entries.
FA.6: relabeling control — on one pinned pair per n, all Ehat_r and all three m2's are exactly invariant under the pinned relabeling pi_n.
FA.7: witness_battery.py reproduces RECORDS_SHA256 39bed5552c805f4d via engine_harness certify on the primary substrate before Stage A is graded.

## 4. Sweep pins (FA.3/FA.4)
Seed 20260703 (Python `random.Random`), per n ∈ {5,6,7}: 40 pairs. Per pair: g = distinct rationals sampled without replacement from pool {1..23} ∪ {3/2, 5/2, 7/2, 9/2, 11/2}; H1 offd + diag entries uniform from {−5..5} \ {0} over pinned denominators {1,2,3}; A = cayley(u₁,v₁)·cayley(u₂,v₂), u,v integer vectors from {−3..3} projected ⊥ g (exact Gram–Schmidt over ℚ; resample on zero); H2 = AᵀH1A. Record per pair: Ê_r ties, δ_shape (zero/nonzero), m2 triple both sides, m2_shape tie flag, auto-tie flags for m2_triv and m2_std.

## 5. P-F3 hunt protocol (pinned adaptivity; n=5; pinned g_h = (1,2,3,5,7), H_h = witness H1 fixture)
- **H0 (measure first):** from the FA.3 sweep at n=5, record the auto-tie rates of m2_triv and m2_std across conjugation pairs.
- **Branch U (if both auto-tie on ALL n=5 sweep pairs):** the tie system collapses to the single equation m2_shape(O(A(t)ᵀH_hA(t))) = m2_shape(O(H_h)) with A(t) = cayley(u₁+t·e, v₁)·cayley(u₂, v₂) on pinned rational u,v,e; clear denominators, solve the univariate polynomial exactly over ℚ; accept rational roots t* with O₂ ≠ O₁; ≤ 8 pinned (u,v,e) slices.
- **Branch G (otherwise):** 3 tie equations {m2_X(O(AᵀH_hA)) = m2_X(O(H_h))} on the two-Cayley family with 3 free rational unknowns (remaining parameters pinned per slice); Gröbner/resultant over ℚ; accept rational solutions with O₂ ≠ O₁; ≤ 8 pinned slices; per-slice hard abort 600 s (abort = slice datum, not kill).
- Exhaustion of slices ⟹ INCONCLUSIVE_BUDGET (P-F3 not refuted; absence-in-budget ≠ nonexistence). Any exact structural obstruction discovered (e.g. an identity forcing a tie to be impossible on the family) ⟹ OBSTRUCTION_RECORDED + routed (that is a lead).

## 6. Kill conditions (armed, typed)
- **K-FA1 (halt-stage):** records-blob sha mismatch between the two runs (nondeterminism).
- **K-FA2 (halt-stage):** FA.1 or FA.2 failure — the CL-F1 certificate layer contradicts the classical mechanism; route to Will verbatim.
- **K-FA3 (halt-stage):** harness gate refusal (clause drift / pin mismatch).
- **Not kills:** an FA.3 tie (mechanism-extraction lead, routed per brief); P-F3 INCONCLUSIVE_BUDGET; a hunt-slice abort.

## 7. depends_on — content pins (sha256[:16] at freeze)
| artifact | sha256[:16] |
|---|---|
| campaigns/shape_witness/BRIEF_v1_DRAFT.md (live) | 3b3fca4292bc8aa7 |
| campaigns/shape_witness/witness_battery.py (Cayley/Ê/projector source pattern) | abff00bd15d22c84 |
| campaigns/shape_witness/WITNESS_PREDECL.md | 967c7909450ef944 |
| campaigns/shape_witness/WALL_SCOUT_PREDECL.md (Stage 0 provenance) | b8d6c404131e7db7 |
| evals/dbp_involution/rep_utils.py | 0d838e5fd430461b |
| campaigns/the_engine/stage_A/engine_harness.py | 7f0e5e7e4f4d54a6 |
| portfolio/80_PROCESS_AMENDMENTS.md | d03842f39c1e699b |

## 8. Status-move rules
- FA.1 + FA.2 green ⟹ CL-F1 → **CERTIFIED at n=5,6,7**; combined with the proof artifact `PROOF_CL_F1.md` (classical mechanism: multiplicity-freeness + Schur + FS(+1) ⟹ dim(Sym²M*)^{Sₙ} = 3) ⟹ CL-F1 → **PROVEN** (auto-file per PA-1 with the proof doc routed to Will for the judgment-class read).
- FA.3/FA.4 green across the sweep ⟹ CL-F2 → **EMPIRICAL** (structural upgrade only via mechanism work, not this stage).
- FA.5 WITNESS_FOUND ⟹ P-F3 → **CERTIFIED witness banked** (degree-2 insufficiency realized); INCONCLUSIVE_BUDGET ⟹ P-F3 stays open with the budget recorded.
- Any FA.3 tie or FA.5 obstruction ⟹ routed to Will same breath (brief Stage A gate).

## 9. Economics
Sweep + certificates: minutes-class (wall-scout margins). Hunt: ≤ 8 slices × 600 s hard abort. Total stage = one session. Primary substrate = container (continuity); box secondary optional for speed, informational.

frozen: true · version: 1 · referee: mechanical (exact equalities; sweep counters; hunt outcome enum) · author: Claude-container · activation authority: Will, S-2026-07-03
