# STAGE B REPORT — rung k=1 under PREREG v2 (flip_cartography)
**Date:** 2026-07-02 · **Prereg:** v2, pin `96b3e09c29a9c182` (FROZEN) · **Battery:** `stage_B/stageB_v2.py` · **Substrate:** [BOX] official x2 (`run2a_k1_v2.log`, `run2b_k1_v2.log`) + [CONTAINER] smoke · **Byte-stability:** RESULTS-SHA256 `723454a5247d6224` identical across box run A, box run B, and the container run — x2 satisfied, cross-machine byte-identity as a bonus (sympy 1.14.0 / mpmath 1.3.0 both sides).

## Verdicts
| item | verdict |
|---|---|
| PB.1' (energy gate, principal sheet) | **PASS, non-vacuous** — 38 principal witnesses, 0 violations |
| PB.2 (fwd == bwd, all charts) | PASS exactly (x/inv, x/bot, u/inv) |
| PB.3 (corner ghosts present + stripped) | PASS — x-chart (x2^2+1)^6 (x1^2+1)^9; u-chart (u^2+1)^6 (x1^2+1)^9; shared (t1^2+1)(x1^2+1) strip ledgered, corner-class certified |
| SP-1 (a)/(b)/(c) | TRUE / TRUE / TRUE — prediction graded, all clauses |
| KB.1 | did NOT fire under the corrected object |

## The physical T_1 (first exact fate curve of the campaign)
Honest eliminant is a single (14,24)-bidegree curve, multiplicity 1, in every chart
(x/inv sha16 `127d9475a31d1dc3`, x/bot `a3a500c8b5af736b` — the bot sha matches run-1
verbatim, free cross-run reproducibility; u/inv `9f355a0ebe3b84ca`). DF-7 classification:
- **x-chart grid (43 lines, 68 real witnesses): 68/68 GHOST**, min margin mu = 0.602.
  The 20 run-1 energy violators are fully attributed to ghost sheets. SP-1(a) confirmed.
- **u-chart grid (238 witnesses): 38 PRINCIPAL** (max mu = 5.5e-64 — Newton lands on
  (c2,s2)=(-1,0) to ~60 digits) vs 200 GHOST (min mu = 7.65e-5); separation ledger
  1.4e+59 >= 1e10. The principal tongue hugs u = 0 (theta2 = pi), exactly where the
  chart-completeness clause predicted it. All 38 satisfy 2c1+c2 <= 1 exactly.
- Ghost energy violations (PB.5 data, not kills): 20 (x-chart) + 6 (u-chart).

## Correction to KB1_AUDIT.md D1 (registry-20 row filed)
The removed lc factor x2^4 is NOT pure junk: the v2 fiber check (terminal circle-1
pinned at (-1,0)) finds gcd degree 5 on the x2=0 line — **genuine chart-infinity
solutions, ghost class** (teleport: theta2(0)=0 to (theta1,theta2)(1)=(pi,pi) in one
step). D1's removal was correct; its "textbook artifact, no solutions" characterization
was incomplete. Silent-removal ban in v2 is what caught this.

## Leads banked
- **Near-tangent ghost (mu = 7.65e-5) at the tongue edge**: a ghost sheet grazing the
  principal continuation = discriminant-adjacent structure, same family as the Stage-A
  branch-12 real-multiplicity outlier. Feeds B4. [OBSERVED]
- Ghost census asymmetry between charts (20 vs 6 violations) — chart-dependence of
  where ghost sheets go energy-hot. [OBSERVED]

## Scope statement
Everything above holds for the frozen system (DF-1/2/3, h = 1/40) at rung k = 1 on the
stated grids; deeper rungs, other h, and off-grid completeness are untested here.

## Next
Rung k=2: two-step glue with principal-chain certification (DF-7 applied per step),
modular-engine elimination, same gates. Then the ladder until the wall.
