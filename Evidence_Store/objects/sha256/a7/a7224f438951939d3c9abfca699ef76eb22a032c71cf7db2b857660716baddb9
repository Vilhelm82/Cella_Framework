# c001 · three_channel_kg — STAGE D REPORT (frame honesty, CL-c7 PARTIAL)

- **Date:** 2026-06-23
- **Stage:** stage_d — frame honesty (CL-c7, PARTIAL by design)
- **Authority:** Frozen objects under `results/three_channel_kg/` (`manifest_v1.json`, `SCHEMA.md`,
  `FIXTURES.md`, `CLAIM_LEDGER.md`) verified vs `freeze_pins_sha256.json` (CLAIM_LEDGER intentionally
  unpinned; verified vs Stage A's frozen_authority_pin). Bench under
  `src/lloyd_v4/evals/three_channel_kg/` imported READ-ONLY from the stable main path and pinned in
  `depends_on`. Covenant embedded in the agent definition; R2/R3 dispositions. ORCHESTRATOR OVERRIDE:
  no `v4-campaign-discipline` skill loaded this session — frozen objects + embedded covenant are the
  sole binding authority.
- **Prereg pin (`prereg_sha256.pin`):** `ae399cb1d4fe5cd37afc615cdb2c5e4e2e2246e1ee9b6542d3484f73930e118a`
- **Records sha256 (`records.jsonl`, 12 records):**
  `0aceffdd3133713a0985381e347b958c730e012c2e0958e48f045c355a87238d`
  — **byte-stable:** two independent battery runs produced byte-identical records jsonl (verified by
  `cmp` and by `test_two_runs_byte_identical`); the canonical write reproduces the same sha.
- **Suite exit code:** `0` (17 tests: gate-bite × 3 + clauses/pins-match × 2 + 9-predictions-pass +
  frame-honesty assertions + 6 mutation guards + byte-stability).

## Pin verification (all match; no abort)

| Object | Pin (freeze_pins / launch cross-check) | Computed | Match |
|---|---|---|---|
| manifest_v1.json | `a28042d9…` | `a28042d9…` | ✓ |
| SCHEMA.md | `fe0eb353…` | `fe0eb353…` | ✓ |
| FIXTURES.md | `3d933e39…` | `3d933e39…` | ✓ |
| CLAIM_LEDGER.md (unpinned; vs Stage A pin) | `d6e395fe…` | `d6e395fe…` | ✓ |
| probe.py | `1f999658…` | `1f999658…` | ✓ |
| schema.py | `40335dc1…` | `40335dc1…` | ✓ |
| fixtures.py | `3d415011…` | `3d415011…` | ✓ |
| referee_total.py | `993ffd21…` | `993ffd21…` | ✓ |
| referee_channel.py | `28eff76c…` | `28eff76c…` | ✓ |
| oracle.py | `b8af9397…` | `b8af9397…` | ✓ |

The three pinned objects match `freeze_pins_sha256.json` exactly; all six bench files match the
launch-instruction cross-checks AND Stage A's `depends_on`. Re-verified at battery runtime by the
prereg-pin gate, clause-drift gate, and bench-pin gate (all proven to bite on tamper).

## Verdicts table (exact ℚ, no tolerance)

| Prediction | Claim(s) | Kill | PASS/FAIL | What it pins |
|---|---|---|---|---|
| P1_F12a_channels_move | CL-c7 | K7 | **PASS** | F12a generic rotation MOVES channels to `(−961/30625, 2713/30625, −3627/30625)` ≠ base `(−1/49, 1/49, −3/49)`; A=B′=C |
| P2_F12a_KG_invariant | CL-c7 | K7 | **PASS** | F12a `K_G = σ₂ = −3/49 = K_G_base` on A/B/B′/C; `q′=14` (intrinsic sum) |
| P3_F12b_channels_fixed | CL-c7 | K7 | **PASS** | F12b signed permutation FIXES channels at `(−1/49, 1/49, −3/49) = base`; A=B′=C (`S₃⋉{±}` at n=3) |
| P4_F12b_KG_invariant | CL-c7 | K7 | **PASS** | F12b `K_G = −3/49 = K_G_base` on A/B/B′/C; `q′=14` |
| P5_K7_not_fired | CL-c7 | K7 | **PASS** | K7 NOT fired: recharts orthogonal & legitimate (R∈SO(3) `RᵀR=I`,`det=+1`; P `PᵀP=I`,`|det|=1`) and `σ₂` invariant under both |
| P6_frame_relativity_contrast_R2 | CL-c7 | K7 | **PASS** | R2 contrast: F12a moves channels + sum fixed; F12b fixes channels + sum fixed (sum intrinsic under both) |
| P7_completeness_OPEN_Ksoft_flag | CL-c7, CL-c3c-ii | K-soft | **PASS** | CL-c3c-ii recorded OPEN; K-soft non-refuting FLAG; CL-c7 move = PARTIAL (not DEMONSTRATED) |
| P8_F12_preconditions | CL-c7 | — | **PASS** | P-frame: F12a/F12b carry frame on fixture & oracle; P-self-cert: oracle import-disjoint from A/B/B′ |
| P9_F12_type_gate_sqrt_q | CL-c7 | K8 | **PASS** | every F12 emission on A/B/B′ is exact `Fraction`; float operand at door → `TypeError` |

**9 / 9 PASS.**

## Headline

**Frame honesty holds, PARTIAL by design.** The signed `K_G = σ₂ = −3/49` is INTRINSIC — invariant
under both the generic rotation F12a and the signed permutation F12b, confirmed independently on
Path A (probe), Path B (Bareiss total), Path B′ (split shape operator) and Path C (frozen oracle).
The channel triple is FRAME-RELATIVE: it MOVES under a generic rotation
(`(−1/49, 1/49, −3/49) → (−961/30625, 2713/30625, −3627/30625)`) while remaining FIXED under the
signed permutation (the `S₃⋉{±}` stabilizer of the monomial decomposition at n=3). K7 (frame-
undeclared) does not fire: both recharts are legitimate orthogonal frame changes and `σ₂` is held
invariant, so no legitimate rechart is mistaken for a curvature error. Completeness — whether
`{σ_r}`+orientation determines the gauge+permutation class (CL-c3c-ii / L1) — is explicitly left
OPEN; K-soft is raised as a non-refuting FLAG, not closed.

## Proposed status moves

- **CL-c7 → PARTIAL** (explicitly **NOT** DEMONSTRATED). Gated on P1–P9 all PASS. Warrant: the
  provable frame-honesty core on the frozen F12 pin (R3, exact ℚ) — intrinsic sum (P2/P4),
  frame-relativity of channels under generic rotation (P1/P6, R2), `S₃⋉{±}` invariance under signed
  permutation (P3/P6), K7 not fired (P5) — with completeness (CL-c3c-ii / L1) left OPEN. Eval-tier;
  no substrate promotion; canonical only on Will's sign-off. The frozen ledger already marks CL-c7
  "PARTIAL by design"; this stage does not exceed that.
- **CL-c3c-ii → OPEN (no move).** Recorded OPEN — blocked on `{σ_r}`-completeness / L1. Stage D does
  NOT attempt to close it. No status move proposed.

## Kill status

- **K7 (frame-undeclared, refute): NOT FIRED.** Both recharts are legitimate (orthogonal) frame
  changes and `σ₂ = K_G` is held invariant under both F12a and F12b; no legitimate rechart is
  reported as a curvature error.
- **K-soft (completeness, non-refuting FLAG): RAISED as a flag, does not refute.** Completeness is
  unestablished. No in-scope witness of two surfaces with identical `{σ_r}`+orientation that are not
  gauge+permutation related was manufactured (that would reach into closing CL-c3c-ii, which is out
  of Stage-D scope). The exact-ℚ near-miss is recorded: F12a and F8-base share `σ₂ = −3/49` and
  orientation but differ in channels AND are frame-related (by R∈SO(3)) — the converse of the open
  K-soft question, not a closure of it. The FLAG does NOT fail any prediction.

## Defect-chain count

**0** (target: NONE). No prediction failed; no halt; no unforeseen cross-stage dependency. All
records re-validate via `schema.from_json` (role gate, exact-ℚ frac discipline, P-frame on channel
rows). The prereg froze before any battery code; clauses embedded verbatim and gated; bench imported
read-only and pinned.

## Will's desk

- **What is being asked of you:** accept **CL-c7 → PARTIAL** (not DEMONSTRATED) and **CL-c3c-ii →
  OPEN (no move)**. Both are eval-tier; nothing is canonical until you sign off. This is a fan-out
  stage; this report covers Stage D only.
- **The science, in one line:** the SUM is the invariant; the CHANNELS are the frame-relative
  representative — proven on the frozen F12 pin, with completeness honestly left open.
- **The one judgement call I made (please confirm):** the K-soft FLAG is recorded as
  "completeness unestablished" **without manufacturing an L1 witness**. I read the launch scope as
  forbidding any attempt to close CL-c3c-ii (and K-soft is non-refuting by construction), so I did
  not synthesize a non-frame-related `{σ_r}`-collision pair. If you want an actual L1 witness pair
  attempted, that is a successor task (it would touch `{σ_r}`-completeness, out of Stage-D scope).
- **No surfaced finding requiring a halt.** One structural note (not a defect): the worktree is
  bench-less by design, so the battery references the frozen bench at the stable **main** absolute
  path `/home/wlloyd/Lloyd_Engine_V4/src/lloyd_v4/evals/three_channel_kg/` (STAGE/RESULTS are still
  `__file__`-relative). On merge to main, the merge-packager may wish to retrofit `BENCH_DIR` to the
  `__file__`-relative `REPO_ROOT/src` form (as Stage A did post-gate); records content is
  path-independent, so that retrofit leaves the records sha256 unchanged.
