# ROWB_MECH_PREDECL — wave-1 row 1: graph-slice mechanism certification (SN-2, Species II candidate)
**Date:** 2026-07-02 · **Status:** FROZEN on Will's "Go with the amended two-axis taxonomy" · **Written BEFORE battery code (covenant #2).** Substrate: [CONTAINER], exact ℚ on all verdict paths, byte-stable ×2.

## The candidate (Will's, verbatim mechanism; recount checked by hand pre-freeze)
`ψ_W : so(m) → ℝᵐ, A ↦ diag([W,A])`, with `[W,A]_ii = −2·Σ_{j≠i} W_ij A_ij`; row-sums cancel pairwise ⟹ image ⊆ trace-zero hyperplane ⟹ generic rank ≤ m−1. Candidate sweep: `D_W = {[W,A] : A ∈ ker ψ_W}` — **conjugation-along-the-slice**, a point-dependent distribution, not a group. A-priori PROVEN before any computer runs: char-poly coefficients are constant along `e^{−tA}We^{tA}` ⟹ `D_W ⊆ ker dΦ` unconditionally; the entire load is **equality**, checkable at points by dimension match.

## Pinned fixtures
```
m=4:  W* off-diag (lex) = (1, 2, 3, 4, 5, 6)        W** = (2, 1, −1, 3, −2, 1)
m=5:  W* off-diag (lex) = (1, −2, 3, 1, 2, −1, 4, −3, 1, 2)   W** = (2, 1, −1, 3, −2, 1, 1, 2, −1, 3)
so(m) basis: E_ab = e_a e_bᵀ − e_b e_aᵀ, a<b (lex).  Summary Φ = nonconstant char-poly coeffs c₂..c_m.
```

## Runtime gates (refuse, don't improvise)
- **G1 (spectrum simplicity):** charpoly squarefree at every pinned point, exact gcd test — P2's commutant argument requires simple spectrum; a non-simple point fires K-3, no silent re-pin.
- **G2:** clause embedding + this predecl's sha pin, string-compared at runtime.

## Predictions (graded mechanically, per point)
- **P1:** rank ψ_W = m−1 exactly at all four pinned points.
- **P2:** dim D_W = (m−1)(m−2)/2 exactly (= 3 at m=4, 6 at m=5); mechanism: ker ψ_W ∩ commutant = 0 under G1.
- **P3 (a-priori-proven, run as pipeline control):** Jacobian(dΦ)·d = 0 exactly for every spanning vector d of D_W.
- **P4 (the equality — the row's verdict):** dim D_W = dim ker dΦ (deficit recomputed in-battery, not imported), whence with P3: `ker dΦ = D_W` at the point. All four points.
- **Controls:** C-1 = P3 (failure = pipeline bug, not mathematics); C-2 genericity ×2 points per m; C-3 = G1 logged.

## Species verdict rule (two-axis, per SN-2 addendum)
P1–P4 all pass at all points ⟹ **Row B layer-2 = Species II [CERTIFIED at pinned points]**; combined with the wave-0 cospectral witness, Row B two-axis reading = **(II, discrete splitting NONTRIVIAL)** — the first complete two-axis row in the census.

## Kill conditions (armed)
- **K-1:** P3/C-1 fails → HALT, apparatus fault.
- **K-2:** rank or span comes up short of prediction → **the gap IS the finding** (un-swept continuous directions beyond the candidate) → HALT to Will with the measured gap; predictions are never widened.
- **K-3:** G1 fails at a pinned point → HALT to Will for re-pin ruling.

## Scope & prior-art posture (binding on claim language)
This row certifies a mechanism at points; it claims no novelty. The fiber-dimension arithmetic is moment-map-adjacent KNOWN territory (diag = torus moment map on the isospectral orbit; Schur–Horn / Tomei / Brockett double-bracket neighborhood) — full prior-art sweep is OWED at any claim boundary; the engine framing (two-axis blindness census, exact-ℚ point certificates) is the candidate contribution locus, and even that waits for the sweep.

## Status-move rule
All pass ⟹ Row B mechanism CERTIFIED; taxonomy v2 gains its first Species-II instance; wave-1 row 2+ (new-territory harvest) eligible for the next predecl + Will's Go. Anything less: verdicts banked at true status; K-2's gap, if fired, becomes wave-1 row 1b by its own predecl.
