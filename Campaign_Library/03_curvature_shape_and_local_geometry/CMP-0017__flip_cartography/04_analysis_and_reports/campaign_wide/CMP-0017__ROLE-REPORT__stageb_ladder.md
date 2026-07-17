# STAGE B REPORT — sequential prediction ladder, rungs k=3,4,5
**Date:** 2026-07-02 · **Governing:** PREREG v2 (pin 96b3e09c) + LADDER_PREDECL (pin 7dfe1b65, ledger appended per rung, every window committed pre-run) · **Battery:** `stage_B/stageB_ladder.py` · **Substrate:** [BOX], byte-stable x2 every rung (shas c6b62f6d / b34ed2c4 / b9a449a0).

## Ladder results (all windows frozen before their runs)
| k | witnesses | u-values | w(k)·4000 | rule window | verdict | sharp candidate | sharp verdict |
|---|---|---|---|---|---|---|---|
| 1 | 38 (rung-1) | — | 4 | — | — | — | — |
| 2 | 140 | 35 | 17 | — | — | — | — |
| 3 | 312 | 79 | 39 | [32,40] | **PASS** | — | — |
| 4 | 552 | 141 | 70 | [58,80] | **PASS** | 70 (k(9k−1)/2) | **HIT exact** |
| 5 | 848 | 217 | 108 | [92,125] | **PASS** | 110 | **REFUTED** (−2) |

PB.1' PASS and PB.2 PASS at every rung; exact-boundary lemma point present at every rung
as proven; zero unresolved margins.

## The law, honestly stated
- **[EMPIRICAL, 5 rungs]** tongue half-width leading behavior `w(k) ≈ (9/2)k²` grid units
  (second differences 13,22,31,38 → 9,9,7).
- **[REFUTED]** the exact quadratic `w(k)·4000 = k(9k−1)/2` — made one true out-of-sample
  hit (k=4) then missed k=5 by 2; furthermore NO quadratic is consistent with all five
  grid-floored measurements (the floor-constraint system is empty). The deviation is
  real, negative, and growing: the ballistic (constant-acceleration) regime degrades as
  the chain accumulates velocity.
- Grid quantization caveat: each w(k) is the floor of the true fold-edge u*(k) at 1/4000
  resolution; the refutation survives it (108 measured excludes true edge ≥ 109/4000).

## Mechanism identification (named, not yet executed)
The tongue edge is where the two theta1 witness roots merge — a double root of the
principal-sheet flip condition: **the edges are real-discriminant FOLD points of the
principal sheet.** Extracting u*(k) exactly (solve s2^(k) = d(s2^(k))/d(theta1) = 0 at
dps 60, no grid floor) turns the ladder law into fold-locus geometry — and is the B4
discriminant-strata machinery arriving on schedule, with branch-12 as the standing
witness target. This is the highest-ROI next move.

## Scope
Frozen system, rungs 3–5, stated grids, witness-arm tier. The exact eliminants (modular
tower) and the fold extraction are the banked successors.
