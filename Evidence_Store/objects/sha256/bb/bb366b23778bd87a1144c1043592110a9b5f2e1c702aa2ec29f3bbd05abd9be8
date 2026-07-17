# STAGE B REPORT — fold-point extraction, k=1..7
**Date:** 2026-07-02 · **Governing:** FOLD_PREDECL pin `cf95a3c905544828` (frozen pre-battery) under PREREG v2 · **Battery:** `stage_B/stageB_fold.py` · **Substrate:** [BOX] ×2 byte-stable, sha `7b3c6773d339e5f7`.

## Verdicts
FP-1 **PASS** (all five banked grid floors reproduced exactly by floor(4000·u*)); FP-2 **PASS** (mirror folds exact to solver precision, fold pair {(θ1*,u*),(−θ1*,−u*)}); FP-3 **PASS** (r > 0, strictly increasing). Newton residuals ≤ 1e−40 per acceptance, chains fully DF-7 gated.

## The exact tongue edges (first strata points of the campaign)
| k | 4000·u*(k) | θ1*(k) | r(k) = 4.5k² − 4000u* |
|---|---|---|---|
| 1 | 4.41713879787 | −0.61763 | 0.08286 |
| 2 | 17.6369119368 | −0.62403 | 0.36309 |
| 3 | 39.5678859692 | −0.63470 | 0.93211 |
| 4 | 70.0688687065 | −0.64964 | 1.93113 |
| 5 | 108.96411284  | −0.66887 | 3.53589 |
| 6 | 156.061443062 | −0.69240 | 5.93856 |
| 7 | 211.17017419  | −0.72025 | 9.32983 |
(40-digit values in the run logs.)

## Findings
1. **The "sharp quadratic" fully resolved [CLOSED]:** k(9k−1)/2 was a floor artifact — the
   smooth fold curve's grid floors coincided with it for k ≤ 4 (k=4 by 0.069) and decohered
   at k=5 (108.96 vs 110). The ladder's refutation and the fold curve now tell one story.
2. **Correction law r(k) [OBSERVED, form unidentified as promised]:** local log-log exponent
   climbs 2.33 → 2.93 across k=2..7 (approaching cubic from below); no polynomial of degree
   ≤ 4 fits the seven 40-digit values; FP-4 returns no verdict, per predecl. Mechanism
   obligation: analytic short-time expansion of the fold condition (from-rest parity makes
   the continuum expansion even in t; the observed drift says the discrete/nonlinear
   corrections interact — a symbolic derivation, queued).
3. **θ1* migration [OBSERVED]:** the extremal release angle drifts monotonically
   −0.618 → −0.720 with k; the +u edge lives at negative θ1 (fold-pair symmetry, banked
   after a wrong-basin seed was caught by the u>0 assertion).
4. These seven points are the first exact **discriminant-stratum data of the campaign** —
   the B4 machinery live, with the branch-12 connection still open.

## Scope
Frozen system, principal sheet, rungs 1–7, solver-precision certification tier.
