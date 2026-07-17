# WALL_SCOUT PREDECL — E1 FLAGSHIP STAGE 0 (umbrella: THE ENGINE Stage C)
**Status: FROZEN at commit, pre-battery (no scout code exists at freeze time). Date 2026-07-03.**
**Authority:** PA-2 B2 conversion (verbatim: *time+memory of projector construction, Molien series, and one bordered-Jacobian rank op at n = 6 and 7; inclusion threshold = fits the container session envelope with byte-stable ×2 — measured, not chosen*). Activated by Will's "Go" S-2026-07-03 after the box housekeeping sweep (PA-3 gate GREEN). Flagship home = `campaigns/shape_witness/` (B1 convention). This is a **measurement stage**: clauses govern protocol integrity; the measured numbers are banked regardless of which side of the envelope they land on.

## 1. Provenance chain (staleness-gate diagnosis, in ink)
Engine brief §4 inherits flagship brief pin `dd94b1b2` — that is the **freeze pin** (commit `b485d32`). Live brief = `3b3fca4292bc8aa7` (commit `fd53a18`); delta = 12 lines, the §10 reserved-rulings block dissolved into the §7 PA-2 conversion text. **Zero mathematical content moved** (verified by diff). This predecl pins the live hash and records the chain.

## 2. Pinned operations (exact ℚ throughout; the flagship's own pipeline, measured)
- **OP1(n) — projector construction.** `P_λ = (dim_λ / n!) Σ_{w∈S_n} χ_λ(w) ρ(w)` on the pair module `M^(n−2,2)` (dim `N = n(n−1)/2`), λ ∈ {triv=(n), std=(n−1,1), shape=(n−2,2)}, characters/dims from `evals/dbp_involution/rep_utils.py`, ρ = pair-permutation matrices, full n!-sum (the DF-S2 construction as instantiated in `witness_battery.py`). Gates: ranks `(1, n−1, n(n−3)/2)`, idempotency `P² = P`, partition `ΣP = I`.
- **OP2(n) — Molien series.** `M(t) = (1/n!) Σ_{classes} |cl| / det(I − t·ρ(w_cl))` over ℚ(t), series to `t³`; record graded invariant counts `(a₁, a₂, a₃)` at each n.
- **OP3(n) — one bordered-Jacobian rank op.** At the pinned fixture `(gₙ, Hₙ)`: compute `O = O_of(H)` (gauge-normal form, `O_ij = H_ij − g_i H_jj/(2g_j) − g_j H_ii/(2g_i)`); compute `Ê_r`, r = 1..4, as the witness bordered-minor sums (`(−1)^{r+1} Σ_{|I|=r+1} det[[0, g_I],[g_Iᵀ, H_II]]`); assemble the 7×N Jacobian `J = ∂(Ê₁..Ê₄, m2_triv, m2_std, m2_shape)/∂(pair coords)` — `Ê`-rows via exact adjugate cofactor sums (`∂det M/∂M_ab = adj(M)_ba`, summed over the two symmetric positions per pair, over all subsets containing the pair), `m2`-rows `= 2·(P_X O)` — and compute `rank_ℚ(J)`.
- Timings and peak RSS are recorded **outside** the hashed records blob; the blob carries only substrate-independent mathematical outputs (ranks, gate booleans, Molien counts, `Ê` values, Jacobian rank, blob-internal fixture echo).

## 3. Pinned fixtures
```
g_6   = (1, 2, 3, 5, 7, 11)
g_7   = (1, 2, 3, 5, 7, 11, 13)
offd_6 (15, lex pair order) = 1, -2, 3, 1, 2, -1, 4, -3, 1, 2, -5, 2, 3, -1, 7/2
offd_7 (21, lex pair order) = 1, -2, 3, 1, 2, -1, 4, -3, 1, 2, -5, 2, 3, -1, 7/2, 1, -4, 5/2, 3, -2, 9
H_n = sym_from_pairs(offd_n), diag = 0   (the witness H1 convention, extended)
```

## 4. Frozen measurement clauses (verbatim; the scout embeds these exactly and refuses on drift)
MC.1: the scout computes OP1, OP2, OP3 at n=6 and n=7 in exact rational arithmetic on the pinned fixtures, and the records blob RECORDS_SHA256 is equal across two independent runs per substrate.
MC.2: envelope constants are ENVELOPE_T = 1200 seconds wall per op-run and ENVELOPE_M = 8192 MB peak RSS; the measured cost of an (op, n) is the maximum over the two primary runs.
MC.3: the inclusion verdict per n is INCLUDED iff all three ops fit both envelope constants on the primary substrate; otherwise WALL_AT(n, op, t_s, rss_mb) — a measured wall is the answer, never a failure.
MC.4: the primary substrate is the container per PA-2 B2 verbatim; a box run of the same battery is banked as secondary substrate-comparison data with no threshold authority.
MC.5: calibration control — witness_battery.py reproduces RECORDS_SHA256 39bed5552c805f4d via engine_harness certify on the primary substrate before the scout is graded.
MC.6: Molien degree-2 and degree-3 invariant counts at n=6 and n=7 are RECORDED as frozen numbers for the flagship; grading of P-F1 belongs to flagship Stage A, not to this scout.
MC.7: projector gates (rank triple (1, n-1, n(n-3)/2), idempotency, partition of identity) must pass at both n; a projector-gate failure is a mathematical halt, not a cost wall.

## 5. Kill conditions (armed, typed)
- **K-C1 (halt-stage):** records-blob sha mismatch between the two runs on either substrate (nondeterminism).
- **K-C2 (halt-stage):** projector-gate failure at n=6 or n=7 — mathematical failure, route to Will verbatim (MC.7).
- **K-C3 (halt-stage):** harness gate refusal (clause drift / pin mismatch) on any invocation.
- **Not a kill:** exceeding ENVELOPE — that is the measured wall (MC.3). Hard-abort ceiling: wall time > 3×ENVELOPE_T on any single op aborts that op and records WALL_EXCEEDED_ABORT(n, op) as a datum; the scout continues.

## 6. depends_on — content pins (sha256[:16] at freeze)
| artifact | sha256[:16] |
|---|---|
| campaigns/shape_witness/BRIEF_v1_DRAFT.md (live) | 3b3fca4292bc8aa7 |
| — freeze-pin provenance (commit b485d32) | dd94b1b23a297c10 |
| campaigns/shape_witness/witness_battery.py | abff00bd15d22c84 |
| campaigns/shape_witness/WITNESS_PREDECL.md (MC.5 runtime read) | 967c7909450ef944 |
| evals/dbp_involution/rep_utils.py | 0d838e5fd430461b |
| campaigns/the_engine/stage_A/engine_harness.py | 7f0e5e7e4f4d54a6 |
| campaigns/the_engine/stage_A/STAGE_A_PREDECL.md (harness authority) | 44a2c8019b2929b2 |
| 80_PROCESS_AMENDMENTS.md (PA-2 authority) | d03842f39c1e699b |

Scout gate at runtime: engine_harness `clause_gate` (MC.1–MC.7 verbatim) + `pin_gate` (table above) before any op runs — the harness's first consumer.

## 7. Status moves
- MC.1–MC.7 green ⟹ **WALL_VERDICT banked** (n-budget = the measured set; per-op cost table in ink); flagship Stage 0's B2 duty **DISCHARGED**; auto-files per PA-1 measurement class. Ladder (B3) and stop-rule (B4) remain armed for the flagship stages; nothing here pre-commits a degree climb.
- K-C1/C2/C3 ⟹ halt, route verbatim.

## 8. Economics
Per-op hard abort 3600 s (3×ENVELOPE_T); total stage = one session; box secondary backgrounded per long-run protocol.

frozen: true · version: 1 · referee: mechanical (blob-sha equality; envelope comparison against pinned constants) · author: Claude-container · activation authority: Will, S-2026-07-03
