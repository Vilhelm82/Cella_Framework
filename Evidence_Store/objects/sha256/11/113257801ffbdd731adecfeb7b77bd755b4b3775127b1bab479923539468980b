# STAGE B REPORT — rung k=2 (flip_cartography)
**Date:** 2026-07-02 · **Prereg:** v2 pin `96b3e09c29a9c182` + rung-2 predecl pin `3a675143fa646118` · **Battery:** `stage_B/stageB_k2.py` · **Substrate:** [BOX] official ×2 (`runW_a.log`, `runW_b.log`) · **Byte-stability:** RESULTS-SHA256 `aa5c0d1ac0ac2b19` identical across both runs.

## Arm W (principal-chain shooting) — CLOSED
| item | verdict |
|---|---|
| PB.1' (tier: CERTIFIED-numeric, margin ledger, per predecl clause) | **PASS** — 140 principal witnesses, 0 violations, 0 unresolved |
| Exact-boundary point | 1, **PROVEN**: the inverted equilibrium (theta1,theta2)=(0,pi) is a discrete fixed point of the scheme (at q0=(1,0,-1,0), rest, both discrete force pairings vanish by s1=s2=0 symmetry ⟹ q1=q0, pi'=0 exactly) ⟹ it lies on T_k for every k with energy margin identically 0 — the equality case of the gate, satisfying <= |
| PB.2 (P1a involution, witness level) | **PASS** — 140/140 backward matches, 0 mismatches [SP-2(c) TRUE] |
| SP-2(a) tongue wider at k=2 | TRUE — 35 u-values vs 9 at k=1 |
| SP-2(b) | TRUE |

## NEW OBSERVED — tongue-extent scaling law
```
extent(k=1) = ±1/1000 = ±4/4000        extent(k=2) = ±17/4000
ratio ≈ 4.25 ≈ k²
```
Mechanism candidate [STRUCTURAL, not certified]: ballistic drift — cumulative s2
displacement over k steps ≈ Σ_{j=1..k} (2j−1)·10h² = 10k²h², so the u-half-width of the
principal tongue grows as k². **Freezable rung-3 prediction: extent(k=3) ≈ ±36/4000
(window ±(32..40)/4000).** To be frozen in the rung-3 predecl BEFORE any k=3 run.

## Arm T (symbolic tower) — WALL BANKED
K_wall(sympy-resultant tower, u-chart, k=2) = **level L1**: res_t2 of a bidegree-6 pair
in (t2,ta,tb,x1,u). Killed at 1040 s elapsed (2.5× the frozen 420 s/level clock),
RSS 560 MB, no completion. Per predecl this is a banked reading, not a kill.
Corner content at the L1 shared strip: all five (·²+1) factors present [SP-2(d)
observed at the completed strip stage]. Declared successor route: modular spectrum
engine (GF(p) per-point univariate tower + exact-degree interpolation, the Stage-A
pattern) — next pass. Exact-algebraic PB.1' at k=2 remains a banked obligation
pending that eliminant (predecl tier clause exercised as designed).

## Harness ledger (found + fixed in-session, before any verdict)
1. py3.14 box default multiprocessing start-method broke the pool (container py3.12
   masked it) — pinned 'fork'.
2. Two-tier redesign: float64 candidate scan + mp dps-60 certification (floats never
   touch a verdict); pooled over u. Witness run: 7.7 s full grid.
3. Self-correction: the original tower was never reaped — long-resultant silence was
   misread as a crash. Rule filed: a silent sympy resultant is a working sympy resultant;
   check the process, not the log.

## Scope
Frozen system (DF-1/2/3, h=1/40), rung k=2, stated grids, witness-level certification
tier per predecl. Off-grid completeness and the exact k=2 eliminant are untested here.

## Next
Rung 3 witness arm (freeze the k² extent prediction first — the cheap, sharp
falsification moment), then the modular tower for the exact k=2 honest eliminant.
