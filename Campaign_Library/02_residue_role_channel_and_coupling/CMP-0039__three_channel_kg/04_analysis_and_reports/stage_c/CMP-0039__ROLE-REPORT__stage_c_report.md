# Stage C report — gauge / single-edge (CLEAN RE-RUN)

**Campaign:** c001 `three_channel_kg` (SHA-frozen) · **Stage:** stage_c · **Date:** 2026-06-23

**Authority.** Frozen objects under `results/three_channel_kg/` (manifest_v1.json, SCHEMA.md,
FIXTURES.md, CLAIM_LEDGER.md) verified vs `freeze_pins_sha256.json`; built+frozen bench under
`src/lloyd_v4/evals/three_channel_kg/` imported READ-ONLY by exact file path from the stable main
checkout (`/home/wlloyd/Lloyd_Engine_V4`) and pinned in the prereg `depends_on`. The covenant loop
governs; R2 disposition (supplied frame); K4 armed. This is a **clean re-run of Stage C** per Will's
explicit ruling: a fresh runner, the CORRECT grader from the first scored run, NO mid-run grader fix,
reproducing the prior (correct) science with a clean transcript.

**Why this re-run.** A prior Stage C run reached the correct science (9/9, records sha `65d60163…`)
but only AFTER a mid-run grader fix: its first scored run emitted a genuine step-4 graded FAIL
(PC4/PC8 `pass:false`) because its "pins" predicate wrongly checked the WHOLE channel vector `C`
unchanged; it then fixed the grader and continued. The covenant requires HALT-and-route on ANY
step-4 FAIL. Will ordered a clean re-run with the correct grader from the start. This run delivers
that: the grading predicate keys the pin/move on the coupling channel **δκ_c** (governed by the
single-edge law), NOT the whole vector `C`.

---

## Pins (verified)

- **Frozen prereg pin:** `prereg.json` sha256
  `8e2a26444c8440daf82b9ce17f561f3d59ae4018db52cbaf4bd73b010a681464` == `prereg_sha256.pin`
  (copied verbatim from the prior worktree; re-verified IN PLACE in this worktree before any battery
  code ran). The prereg was frozen correctly BEFORE any battery code — only the prior battery was
  buggy; this prereg is unchanged and binding.
- **Bench content pins** (re-verified vs prereg `depends_on`, exact match):
  probe `1f999658…`, schema `40335dc1…`, fixtures `3d415011…`, referee_total `993ffd21…`,
  referee_channel `28eff76c…`, oracle `b8af9397…`, manifest `a28042d9…`.
- **Runtime gates (in the battery, fired green):** prereg-pin self-check; `GRADER_CLAUSES` embedded
  VERBATIM, string-compared against the frozen prereg `grader_clauses` (REFUSE on any drift);
  bench-pin drift gate (REFUSE on any sha mismatch). The suite proves each gate BITES a tampered
  contract (non-tautological).

## Records

- **records.jsonl sha256:** `65d601637a428655c6a8e5140895b5b2a78a64a7f2961b5a9d60bb1d72a2ea5a`
  (== Will's hard acceptance target; the records were always correct).
- **Two-run byte-stable:** `records.jsonl` ≡ `records_run2.jsonl` — byte-identical (`cmp` clean);
  both report sha `65d60163…`. 47 records. Deterministic sorted-keys serialisation, exact-Q
  `frac:n/d` strings, no float/time/random.
- **Suite exit code:** **0** (20 tests: gate-bite × 6, all-9-pass + anchors, mutation guards × 8,
  byte-stability).

## Verdicts

| # | Prediction | Verdict | Units / witness |
|---|---|---|---|
| PC1 | keystone F8 base jet (A/B/B′/C agree) | **PASS** | exact ℚ; `q=14, ∏g=6, q²=196`; `(K_G,κ_c,κ_s,κ_int)=(−3/49,−1/49,1/49,−3/49)`; `tr(PHP)=12/7` |
| PC2 | single-edge law at keystone | **PASS** | exact ℚ; e1 PINS (0), e2 PINS (0), e3 MOVES 6/49 per unit t; e3 @ t∈{1,2,3,−4,1/2} → {6,12,18,−24,3}/49 |
| PC3 | every σ_r preserved under gauge | **PASS** | exact ℚ; `K_G=−3/49`, `tr(PHP)=12/7`, `q=14` invariant on A/B/B′ at every edge/t |
| PC4 | δC ∈ ker Σ | **PASS** | exact ℚ; `Σ(δC)=0` on e1/e2/e3 at every t; **δκ_c pins on e1/e2, moves on e3** (NOT the vector); A==B′ |
| PC5 | single-edge law symbolic over ℚ | **PASS** | 0 residual monomials per edge (zero polynomial in ℚ[g,H,t]) |
| PC6 | K_G/σ_r invariance symbolic over ℚ | **PASS** | 0 det-residual monomials per edge; `q²·(PH′P−PHP)` zero 3×3 matrix per edge |
| PC7 | two-derivation under gauge (A==B′) | **PASS** | exact ℚ; Path-A channels == Path-B′ channels on the gauged jet, all edges/t |
| PC8 | K4 mutant guards | **PASS** | booleans + exact-ℚ; σ-breaking mutant changes K_G; wrong-law mutant differs; e1-moves claim FALSE; true gauge passes |
| PC9 | preconditions (P-self-cert, P-frame) | **PASS** | import-graph disjoint (oracle ⟂ A/B/B′/fixtures); every channel row carries a frame |

**9/9 PASS.**

## Headline

**CL-c4 → DEMONSTRATED (R2; symbolic over ℚ).** The single-edge gauge is the border shear
`H → H + t(g eᵢᵀ + eᵢ gᵀ)` (g unchanged). Because `P g = 0` (tangent projector `P = I − g gᵀ/q`
annihilates the gradient), the gauge generator satisfies `P(g eᵢᵀ + eᵢ gᵀ)P = 0`, so the tangent
shape operator `P H P` is EXACTLY fixed — proven symbolically over ℚ (PC6). Hence **every** `σ_r` is
preserved (σ₂ = K_G = −3/49 ∈ ℚ; σ₁ = tr(PHP)/|g| ∈ ℚ(√14), rational handle tr(PHP) = 12/7
invariant), not merely the sum. `δC ∈ ker Σ` (PC4): the channel triple TRADES within the 2-dim
kernel — `δκ_c` pins on e1/e2 while `κ_s` and `κ_int` move oppositely. The single-edge law
`δκ_c(t·eᵢ) = 4t·∏g·H_{jk}/q²` is a symbolic identity over ℚ[g,H,t] (PC5), witnessed exactly at the
keystone F8 (PC1/PC2: **e1 pins, e2 pins, e3 moves 6/49** per unit t). K_G invariant on Paths A/B/B′;
the two channel derivations agree on the moved decomposition (PC7).

**Concrete witness (e1, t=1) reproduced exactly:** base `(κ_c,κ_s,κ_int)=(−1/49,1/49,−3/49)` →
gauged `(−1/49,4/49,−6/49)`; `δC=(0, 3/49, −3/49)`; `δκ_c=0` (PINS), `Σ(δC)=0`, `K_G=−3/49`
invariant — the channel VECTOR moves (`deltaC_nonzero=True`) even though `δκ_c` pins.

## Proposed status moves

- **CL-c4: `NOT_YET_PROBED → DEMONSTRATED`** (all nine gating predictions PC1–PC9 PASS). Warrant
  scope per the frozen prereg `on_pass`: gauge-invariance of every σ_r (symbolic over ℚ via PC6) +
  δC ∈ ker Σ (PC4) + the single-edge law as a symbolic identity over ℚ (PC5), witnessed exactly at
  the keystone F8 (PC1/PC2), corroborated across Paths A/B/B′. R2: channels frame-relative in the
  supplied DBP frame, the sum K_G intrinsic. **Eval-tier; NO substrate promotion; canonical only on
  Will's sign-off.**

## Defect chain

**Count: NONE (0).** No prediction FAILed; no mid-run grader fix; the grader was correct from the
first scored run. Kills fired: **NONE** (K4 silent on truth; each of its branches shown by the suite
to bite a constructed mutant). Preconditions hold (P-self-cert, P-frame; run not void).

## Clean-transcript attestation (the whole point of this re-run)

The grader keyed the pin/move on **δκ_c** from the very first scored run. The FIRST `battery.py` run
graded **9/9 PASS** — no step-4 FAIL, no PC4/PC8 `pass:false`, no mid-run grader edit. The
`prediction_verdicts.json` was produced by a single mechanical grade with `halt:false`,
`defect_chain_count:0`. The transcript contains exactly two battery runs (byte-identical) plus the
grade — no fix-and-continue.

---

## Will's desk

- **Decision requested:** sign off CL-c4 `NOT_YET_PROBED → DEMONSTRATED`? Eval-tier proposal only;
  nothing canonical, no substrate promotion (geometry spine fence stays CLOSED) until you say so.
- **What you are buying:** a gauge that fixes every shape invariant σ_r (not just the sum), proven
  as a symbolic identity over ℚ — the channels are frame-relative (they trade within ker Σ) but the
  intrinsic content (every σ_r, hence K_G) is gauge-rigid. The single-edge law is a polynomial
  identity over ℚ, not a finite coincidence; the keystone witnesses e1/e2 pin and e3 moves 6/49.
- **Clean transcript:** this re-run was ordered to replace a prior run that emitted a genuine step-4
  FAIL then fixed-and-continued (a covenant violation). This run delivers the SAME verified science
  (records sha `65d60163…`, 9/9) with the correct grader from the first scored run, NO mid-run fix —
  the transcript is clean. Hard acceptance criteria all met.
- **Open items / findings:** NONE. No unforeseen cross-stage dependency; no shared-file collision.
  Wrote only inside `results/three_channel_kg/stage_c/`. Did NOT touch the shared `CLAIM_LEDGER.md`.
