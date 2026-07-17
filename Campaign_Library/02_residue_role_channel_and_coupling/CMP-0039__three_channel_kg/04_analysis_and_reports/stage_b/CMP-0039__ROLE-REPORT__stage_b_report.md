# c001 · three_channel_kg — STAGE B REPORT (non-negativity impossibility)

- **Date:** 2026-06-23
- **Stage:** `stage_b` — non-negativity impossibility (FAN-OUT stage; ran in parallel with C/D/E).
- **Authority:** Frozen objects under `results/three_channel_kg/` (`manifest_v1.json`, `SCHEMA.md`,
  `FIXTURES.md`, `CLAIM_LEDGER.md`) verified vs `freeze_pins_sha256.json` (the three pinned objects);
  ABORT-on-mismatch passed (all pins match). Built+frozen bench under
  `src/lloyd_v4/evals/three_channel_kg/` imported READ-ONLY by exact file path from the stable main
  checkout and re-pinned in `depends_on` at runtime. Covenant loop; R1/R2/R3 dispositions.
  ORCHESTRATOR OVERRIDE honoured: no `v4-campaign-discipline` skill loaded — frozen objects + the
  embedded covenant are the sole binding authority.
- **Prereg pin (`prereg_sha256.pin`):** `6602b9e9511bc40d9ef6d8f08928dadd628e9c9b671f334ff4027a79461a467d`
- **Records sha256 (`records.jsonl`, 24 records):** `b26a3eb9ee6bbef2d732592b2d603643ec9194374ae9273655c47c44b4e0c1f2`
  — **byte-stable across two runs** (run1 == run2 == fresh-process run from a different CWD; sorted-keys
  serialisation, exact-ℚ `frac:n/d` strings, no float/time/random).
- **Suite exit code:** `0` (`test_stage_b.py`, 21 tests: gates bite, all 10 predictions pass, mutation
  guards prove a lying engine is caught, two-run byte-stability).

## Pin verification (ABORT-on-mismatch gate)

| Object | Pinned (freeze) | Computed | Match |
|---|---|---|---|
| `manifest_v1.json` | `a28042d9…` | `a28042d9…` | yes |
| `SCHEMA.md` | `fe0eb353…` | `fe0eb353…` | yes |
| `FIXTURES.md` | `3d933e39…` | `3d933e39…` | yes |
| bench `probe.py` | `1f999658…` | `1f999658…` | yes |
| bench `schema.py` | `40335dc1…` | `40335dc1…` | yes |
| bench `fixtures.py` | `3d415011…` | `3d415011…` | yes |
| bench `referee_total.py` | `993ffd21…` | `993ffd21…` | yes |
| bench `referee_channel.py` | `28eff76c…` | `28eff76c…` | yes |
| bench `oracle.py` | `b8af9397…` | `b8af9397…` | yes |

All `depends_on` content pins (manifest + six bench files) re-verified at runtime by the battery;
all `frozen_authority_pins` (SCHEMA/FIXTURES/CLAIM_LEDGER/freeze_pins) recorded in the prereg.

## Verdicts table

| Prediction | Claims | Kills | PASS/FAIL | Headline result (exact ℚ) |
|---|---|---|---|---|
| P1 K1 sign-blindness silent on true F8 object | CL-c3 | K1 | **PASS** | `K_G=−3/49<0` (so `K_G≥0` false); `K_G==Σch`; `κ_int=−3/49` present; `Δ_m=12≠0` not dropped ⟹ K1 silent |
| P2 every sign-blind proxy fires K1 on F8 | CL-c3 | K1 | **PASS** | all 5 proxies `≥0` and `≠−3/49` ⟹ all FIRE: `K_G²=9/2401`, `H²=18/343`, `p≥0`, `κ_c+κ_s=0`, omit-tuple |
| P3 CL-c3 impossibility (both-sign witnesses) | CL-c3 | K1 | **PASS** | `K_G(F8)=−3/49<0` (negative witness) ∧ `K_G(F6)=+1>0` (positive) ⟹ no `p≥0` represents signed `K_G` |
| P4 CL-c3b symbolic indefinite over ℚ[g,H] (UNIVERSAL) | CL-c3b | — | **PASS** | `det(H_b)` (12 monomials) specialises to `−t`; `K_G(t)=+t` deg-1 nonconstant; `K_G(1)=+1>0`, `K_G(−1)=−1<0` ⟹ numerator indefinite, structural both-signs |
| P5 CL-c3c-i Σ kernel is 2-dim | CL-c3c-i | — | **PASS** | `Σ=[[1,1,1]]` rank 1 over ℚ ⟹ nullity `3−1=2`; `Σ(1,−1,0)=Σ(1,0,−1)=0`, independent |
| P6 CL-c6 κ_int both signs on family | CL-c6 | — | **PASS** | F10 `κ_int=−1/9<0`, F11 `κ_int=+2/9>0` agree across Path A/B′/C |
| P7 BOTH_SIGN_WITNESSES present | CL-c3, CL-c6 | K1 | **PASS** | F6 `+1`, F8 `−3/49`, F10 `(2/9,1/3,0,−1/9)`, F11 `(0,−1/9,−1/9,2/9)`; all agree A/B/B′/C |
| P8 K11 singular refusal underwrites `q²>0` | CL-c3b | K11 | **PASS** | `g=(0,0,0)` typed REFUSED on A/B/B′ (no numeric); F6 (`q=4`) returns `K_G=+1`, not refused |
| P9 √q-leak type gate | CL-c3, CL-c3b, CL-c6 | K8 | **PASS** | every emitted value on {F6,F8,F10,F11} is `Fraction`; float operand ⟹ `TypeError` at door |
| P10 preconditions (P-self-cert, P-frame) | all | — | **PASS** | oracle imports none of A/B/B′/fixtures (and vice-versa); F6/F8/F10/F11 each carry a frame |

**10 / 10 predictions PASS.**

## Headline

The signed three-channel `K_G` is **provably not representable by any non-negative scalar**, and it is
**structurally two-signed**: a finite exact-ℚ negative witness (keystone F8, `K_G=−3/49<0`) coexists
with a positive witness (sphere F6, `K_G=+1>0`), and the universal mechanism is established
symbolically over `ℚ[g,H]` — `K_G=−det(H_b)/q²` with `q²>0` on every regular jet, and the numerator
`det(H_b)` is **indefinite** (it specialises along the regular family `g=(1,0,0), H=diag(0,t,1)` to the
non-constant polynomial `K_G(t)=+t`, taking both strict signs). The intrinsic map `Σ` has a 2-dimensional
kernel (rank 1 ⟹ nullity 2), and the channel tuple is non-collapsible on the family (`κ_int` attains both
signs, F10 `−1/9` / F11 `+2/9`). The MANDATORY meta-thesis kill **K1** is silent on the true signed
object and fired by every sign-blind proxy.

## Proposed status moves (NOT applied to the shared ledger — for the merge-packager)

| Claim | From | Proposed | Warrant | Gating predictions (all PASS) |
|---|---|---|---|---|
| **CL-c3** (no non-negative scalar represents signed `K_G`) | NOT_YET_PROBED | **DEMONSTRATED** | **[PROVEN]** (R1 logic-forced, impossibility/existence) | P1 ∧ P2 ∧ P3 ∧ P7 |
| **CL-c3b** (numerator indefinite ⟹ both signs, structural) | NOT_YET_PROBED | **DEMONSTRATED** | **[PROVEN]** (R1 UNIVERSAL — symbolic over ℚ[g,H], not finite-only) | P4 ∧ P8 (+ P3/P7 corroboration) |
| **CL-c3c-i** (`Σ:ℚ³→ℚ` has 2-dim kernel) | NOT_YET_PROBED | **DEMONSTRATED** | **[PROVEN]** (exact-ℚ linear algebra, rank-nullity) | P5 |
| **CL-c6** (channel tuple non-collapsible; both signs of `κ_int`) | NOT_YET_PROBED | **DEMONSTRATED** | frozen family (finite, exact ℚ — NOT a ℚ[g,H] universal) | P6 (+ P7 corroboration) |

Encoded from the prereg `status_move_rules` R-dispositions: CL-c3 is impossibility/existence → R1
logic-forced [PROVEN] from a finite exact-ℚ both-sign witness; CL-c3b is UNIVERSAL → the symbolic
identity over ℚ[g,H] was established (no finite-only downgrade); CL-c3c-i is an exact-ℚ linear-algebra
fact; CL-c6 is finite both-sign witnesses on the family. **Eval-tier only; nothing canonical until Will
signs off.**

## Armed kill outcome

- **K1 (sign-blindness, MANDATORY, refute)** — did NOT fire on the true signed F8 object (all four
  trip-conditions false: `K_G<0`, `K_G==Σch`, `κ_int` present, `Δ_m` not dropped), and FIRED on every
  sign-blind proxy (each `≥0`, `≠−3/49`). The meta-thesis kill is satisfied: the true object passes (no
  false positive), the lies are caught.
- **K8 (√q-leak), K11 (singular-lie/refuse-not-lie)** — both held (P9, P8). No leak; genuine `q=0`
  refused on all three paths.

## Defect-chain count

**NONE (0).** No prediction FAILED; no chain to preserve; no HALT. All gates bite, all referee paths
(A/B/B′/C) agree exact-ℚ on every witness, byte-stability holds, suite exits 0.

## Will's desk

- **What moved:** CL-c3, CL-c3b, CL-c3c-i, CL-c6 → **DEMONSTRATED** (the first three carry [PROVEN]).
  This closes the "non-negativity impossibility" arm: the signed object cannot be a magnitude, it is
  structurally two-signed (universal over ℚ[g,H]), `Σ` has a genuine 2-dim kernel, and `κ_int` is
  irreducibly two-signed on the family.
- **The universal warrant for CL-c3b is symbolic, not finite.** Per R1 I did NOT downgrade to a
  finite-only warrant. The numerator `det(H_b)` is proven indefinite over `ℚ[g,H]` by specialising the
  full 9-indeterminate symbolic determinant to a regular 1-parameter family and reading the non-constant
  `K_G(t)=+t`. If you want the indefiniteness witnessed on a *different* regular slice (e.g. a moving
  gradient rather than `g=(1,0,0)`), that is a strengthening, not a correction — flag it for a successor.
- **Pinned note carried from Stage A finding #2 (honoured, not re-litigated):** the manifest
  `stage0_controls` `κ²=9/2401` is `K_G²=(−3/49)²` — the squared TOTAL, a legitimate sign-blind proxy —
  **NOT** the channel-norm `κ_c²+κ_s²+κ_int²=11/2401`. The battery treats `9/2401` strictly as the `K_G²`
  proxy and records `11/2401` as reference-only. No transcription error introduced.
- **Collision discipline:** wrote ONLY inside `results/three_channel_kg/stage_b/`. Did not touch the
  frozen bench, any sibling stage dir, or the shared `CLAIM_LEDGER.md`. The ledger close block is written
  into `stage_b/` for the merge-packager to append.
- **One process note (not a finding, not a defect):** the bench is on `main` and this worktree branches
  from the pre-bench base, so the battery resolves `BENCH_DIR` to the stable main checkout
  (`/home/wlloyd/Lloyd_Engine_V4/src/...`) by detecting the `.claude/worktrees/<name>` segment, while
  writing records beside itself in the worktree. Post-merge on `main` the same code resolves the bench
  via the `__file__`-relative root. Records content is path-independent (sha identical across CWDs).
- **No surfaced cross-stage dependency.** Stage B is self-contained on its claims/fixtures/kills.
