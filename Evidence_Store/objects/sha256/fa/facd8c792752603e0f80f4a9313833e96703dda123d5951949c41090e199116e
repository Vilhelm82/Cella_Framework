# difference-tower — Stage 0 report (the bench / instrument gate)

**Status:** Stage-0 instruments BUILT and bench-green. **AWAITING WILL'S
MANIFEST FREEZE SIGN-OFF** (brief: "Manifest freeze (D3) … gate[s] on
Will's sign-off at marked points"). Nothing below is a graded campaign
result; every artifact is labelled PREFREEZE-BENCH.
**Date:** 2026-06-12. **Branch:** `campaign/difference-tower`.
**Authority:** `Build_Docs/Agent_tasks/CAMPAIGN_DIFFERENCE_TOWER.md`
(GO 2026-06-12).

## 1. Baseline re-verification (brief §4)

Full suite at campaign open, before any campaign code: **exit 0**,
1126 outcomes run (1125 passed + 1 skipped, matching the HR133-close
record), 650 slow-deselected, 1776 collected. After Stage-0 code:
**exit 0**, 2001 collected = 1776 baseline + exactly the 225 new
difference-tower tests. `test_source_purity.py`: 2 passed.

## 2. Deliverables built

| D | Artifact | Where |
|---|---|---|
| D1 | EFT-callable lift (built ONCE; atlas imports) | `src/lloyd_v4/evals/difference_tower/eft_eval.py` |
| D2 | tower constructor (lane + raw + referee; 3 schemes; realizability via typed_ulp) | `…/tower.py` |
| D3 | fixture manifest **v1 DRAFT, frozen: false** (+ deterministic generator) | `results/difference_tower/stage_0/manifest.json`, `…/make_manifest.py` |
| D4 | dual arbiter (symbolic-Q + mpmath annex; coherence cross-checked) | `…/arbiter.py` |
| — | expression class + manifest loader/freeze-gate + bench runner | `…/expr.py`, `…/manifest.py`, `…/run_stage0.py` |
| D7 | surprise ledger initialized (append-only) | `results/difference_tower/surprise_ledger.md` |

**The lift's falsifiable seam (HR129 rule, brief H1):** `eval_lane` carries
TRUE(x) as a per-node Q-deviation composed THROUGH the recorded EFT
residues (unordered TwoSum consumed literally from `bigraded_jet._two_sum`;
FMA TwoProd; div residual pair — CITATIONS E1/E3/E4, cited not re-derived).
A wrong residue breaks TRUE and H1 fails. The H1 referee (`eval_exact`)
is pure-Fraction recursion: no float, no EFT content, different stencil
composition (one-shot binomial vs the lane side's iterative differencing).

## 3. Stage-0 bench results (PREFREEZE — for the freeze decision)

- **H1 gate: PASS — 1329/1329 cells equal bit-for-bit in Q.** Units:
  (fixture, point, scheme, j, m) cells over the manifest gate grid, all
  rational-class fixtures (P0–P4, P10, R1a/b, R2a/b, R3, K1–K3 incl.
  cells AT the kinks, where TRUE is pure Q on both paths).
- **Realizability refusal demo: refused as expected**
  (`stencil_not_realizable`): P2 at RN(1/10), j=2, m=2 — the full-53-bit
  significand point cannot host a wide stencil; typed refusal, never
  silent rounding.
- **Annex lane refusal demo: refused as expected** (`annex_not_q_exact`):
  C1 = sqrt(x)·sqrt(x) — lane TRUE is not Q-carried through sqrt;
  enclosure grading is the annex seam (brief §0 rule 1).
- **Arbiter coherence: PASS** — 8/8 overlap rows (P2, P4, R1a, R3 ×
  {3/4, 5/2}), every measured gap exactly 0.0 against acceptance ≤ 1e-25;
  annex accept arm (sin′(1/2) = cos(1/2) to 1e-30) and honest-refusal arm
  (starved dps ladder ⇒ None) both exercised in tests.
- **Byte-stability ×2: CONFIRMED** — records sha256
  `caee20dcfc3d750d353bf777f4f62f11b13f239449dc60f8e3ddde320a2e49ac`,
  stable-summary sha256 `20ba9e48…e4a52ed`, identical across runs.
- Tests: **225 passed** across the seven §13 files.
- Telemetry (non-verdict-bearing, brief §0 rule 3): full gate run 0.21 s
  wall — far inside the declared 180 s budget.

## 4. Design decisions surfaced for the freeze review

1. **Per-point j-ladders.** First manifest draft attached one ladder per
   fixture; the manifest-validity test caught that RN(1/10)'s binade
   headroom cannot realize j=2 stencils. Restructured to
   `gate_grid: [{point, j-ladder}]` — the brief's "pinned per
   fixture-point" wording, now enforced structurally. (Pre-freeze
   implementation correction, disclosed; no pins existed.)
2. **C1/C2 classed `true_class: "annex"`.** sqrt(x)·sqrt(x) and
   sqrt(x·x) have rational composite TRUE but irrational lane
   intermediates — the Q-carry cannot pass through sqrt. They are
   H1-EXEMPT by class; raw towers consume them (H5/H6) and enclosure
   grading covers their TRUE. **Decision point: confirm or re-class.**
3. **Below the residual-representability sufficient condition
   (RESIDUAL_FLOOR, HR132 amendment), the lift REFUSES the Q-claim**
   rather than degrading to BOUNDED as HR132's membrane object does —
   referee-class strictness: a tower cell is either exact in Q or not
   emitted. **Decision point: confirm refusal-over-degrade.**
4. **Kink calculus pinned:** one-sided abs rule at an argument zero
   d±|u|(x) = ±|d±u(x)| (derived from the difference quotient at
   u(x)=0); Q-jets REFUSE at an abs-argument zero (`jet_at_kink`) —
   higher-order ground truth never guesses across a kink (H4's floor
   rules remain Will-gated, untouched here).
5. **Centered odd-m stencils live on the half-grid** (offsets
   (m/2 − k)·h), realizability-checked like any node; cell divisor h^m;
   ascending-node iterative differencing ≡ binomial with
   (−1)^(m−k)·C(m,k) (Jordan, cited convention).
6. **K-class fixtures participate in H1** (abs is Q-exact pointwise,
   including AT kinks) — exactness needs no smoothness.

## 5. Early observations (OBSERVATIONAL, no verdicts)

- Δ^(d+1) ≡ 0 landed exactly on every polynomial bench cell touched
  (H3's positive side looks alive); K1 cells off the kink terminate at
  Δ² ≡ 0, straddling cells do not — the "locally polynomial" certificate
  semantics previewed exactly as the brief frames it.
- The raw centered tower at C1 already shows reading-noise at j=9
  (1.0000000000000568 vs TRUE 1) — H6's inversion figure has material.

## 6. What freeze means (when Will signs)

1. Set `"frozen": true` in `manifest.json` (Will's call applies it or
   delegates the mechanical edit), write `manifest_sha256.pin`.
2. Re-run `run_stage0` in FROZEN mode → the signed instrument-gate
   artifact (same grid, gate must remain green).
3. Stage A (H1 full grid + H3 two-sided) proceeds per brief §9.

— Claire, on the bench. STOPPED at the Stage-0 artifact per the GO.
