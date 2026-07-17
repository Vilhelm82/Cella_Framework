# WAVE0_PREDECL — Deficit Engine calibration (SN-2, layer 1 + imported anchors)
**Date:** 2026-07-02 · **Status:** FROZEN on Will's "freeze the wave-0 predecl too" · **Written BEFORE battery code (covenant #2).** Substrate: [CONTAINER], exact ℚ on all verdict paths, byte-stable ×2. Scope: CALIBRATION ONLY — the engine must reproduce two KNOWN blindnesses with certificates; no new-territory rows in wave 0.

## Pre-freeze recount (covenant #3, logged in ink)
Graph-row coefficient count corrected before freeze: on the zero-diagonal stratum `tr(W) ≡ 0`, so the char-poly summary carries **m−1** nonconstant coefficients, not m. Predicted deficits: `m(m−1)/2 − (m−1) = (m−1)(m−2)/2` → **3 at m=4, 6 at m=5** (chat-side draft said 5 at m=5 — superseded here, pre-freeze).

## Rows (pinned)
**Row A — our σ-row (the self-test).** `V` = O-space at n=5 (dim 10, pair-lex coords), `G` = S₅, `Φ` = (Ê₁..Ê₄) on the gauge-normal slice `H = M(O)`, g = (1,2,3,5,7). Points: O* = (1,−2,3,1,2,−1,4,−3,1,2) [the witness fixture]; O** = (2,1,−1,3,−2,1,1,2,−1,3) [genericity spot ×2]. Hidden-group generators: basis of `so(4)_g = {A skew : Ag = 0}` from pair-basis of g⊥; descended tangent vectors `δO_k = O_of([M(O*), A_k])`.
**Row B — weighted-graph spectra (the external anchor).** `V` = zero-diagonal symmetric weight space, `G` = S_m relabeling, `Φ` = nonconstant char-poly coefficients (c₂..c_m). Points: m=4: w = (1,2,3,4,5,6); m=5: w = (1,−2,3,1,2,−1,4,−3,1,2). Imported witness: K₁,₄ vs C₄⊔K₁ (0/1 weights, m=5) — the classical smallest cospectral pair.

## Predictions (graded mechanically)
- **P-A1:** rank dΦ_σ = 4 exactly at O* and O**; deficit = 6.
- **P-A2 (mechanism-match):** the 6 tangent vectors δO_k span dim 6 exactly AND Jacobian·δO_k = 0 exactly for all k (infinitesimal σ-invariance of the conjugation action, certified) — deficit fully accounted by the hidden group at this point.
- **P-B1:** c₁ ≡ 0 identically; rank dΦ = m−1 exactly at the pinned points; deficits 3 (m=4) and 6 (m=5).
- **P-B2 (imported witness reproduced):** the cospectral pair has exactly equal char polys in ℤ[λ] AND distinct S₅-orbits (degree-sequence certificate (4,1,1,1,1) ≠ (2,2,2,2,0)).
- **Controls:** C-1 deficit-0 control: Φ_id = the coordinate functions themselves (m=4 graph row) must give rank 6, deficit 0. C-2: Row-A rank identical at O* and O** (genericity ×2).

## Kill conditions (armed)
- **K-1:** any control fails → HALT, apparatus fault, route to Will.
- **K-2:** P-A1 or P-A2 fails → engine refuted at self-calibration (cannot reproduce our own certified blindness) → HALT to Will; SN-2 direction-kill fires.
- **K-3:** P-B1 or P-B2 fails → external-anchor failure → HALT to Will.
- No softening: a surprising rank is reported as measured; predictions are never widened post-hoc.

## Status-move rule
All pass ⟹ engine L1 = CERTIFIED at calibration; SN-2 gate cleared; wave-1 (row harvest, new territory) becomes eligible for its own predecl + Will's Go. Anything less: verdicts banked at true status, SN-2 kill clauses consulted.
