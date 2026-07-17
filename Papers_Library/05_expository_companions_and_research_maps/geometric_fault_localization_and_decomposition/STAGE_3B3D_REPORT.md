# STAGE 3b.3-d — CORESTRICTION-MECHANISM TEST — STAGE REPORT (S-2026-07-05b)
**Authority:** PREREG_3B3D (frozen pre-battery, pin `8bf25627`). **Records:**
grades + reads ×2 on all systems (shas in records/); raw RURs box-only,
sha'd. **Regression gate:** rebuilt M-B system byte-identical to the banked
`m33_mb.ms` before any adjunction. **Envelope:** ~4 min/job vs 1800 s.
**Defect chains: ZERO.** PD.1 feasibility note in ink (squarefree parts of
~5000-digit integers infeasible; delivered the exact subset-square relation
pattern instead — the cancellation structure, which is the mechanism data).

## Verdicts
| id | verdict | reading |
|---|---|---|
| PD.0 | **PASS** | all three systems dim 0, ideal_deg 192, lf = u, grades ×2 |
| PD.1 | recorded ×2 | component norm classes pair: c(deg-96) ≡ +1 alone; c(deg-3) ≡ −m, c(deg-92) ≡ +m (same magnitude class m, small-prime part 59·397·26539·…); c(deg-1) ≡ −□ — cancellation = (−1)(−m)(+m)(+1) |
| PD.2 | **FAIL as staked — routed** | N(D1), N(D2) individually NOT ±□ at n=4 (both classes nontrivial). The n=5 s1 per-denominator law does NOT descend. THE DATUM: since N(D1)·N(D2) = +□, necessarily **class(N(D1)) = class(N(D2))** — nontrivial and EQUAL |
| PD.3 | **HOLDS** + bonus discriminator | control N(E) non-square AND class(N(E)) ≠ class(N(D_i)) — the shared class is **D-pairing-specific, not variety-borne** |
| PD.4 | **HOLDS** | D = 1 + Σ Plücker(U,v)² certified symbolically (Lagrange identity; D is a value of the 2-fold Pfister form ⟨1,1,1,1⟩ pattern at n=4) |

## THE MECHANISM STATEMENT THIS STAGE EXTRACTED
```
UNIFYING LAW [STRUCTURAL; certified instances n=4 miniature + n=5 s1 + 9/9 product slices]:
  class( N(D1) ) = class( N(D2) )   in Q*/(Q*)^2, on every tested tie variety
  — the product-square law N(D1·D2) = +□ is EXACTLY this equality.
  At n=5 s1 the common class is trivial (per-denominator squares — a special case);
  at n=4 it is nontrivial. The law is the EQUALITY, not the triviality.
```
Corroborations: (i) at the n=4 rational tie point, D1 = D2 = 10142/91
exactly (both localizations, independent runs) — the point lies on the
DIAGONAL D1 = D2, the natural fixed locus of a swap; (ii) the component-
level pairing (PD.1) shows the same shared-class shape inside the algebra.
Mechanism candidate, sharpened: a ℚ-rational correspondence of the tie
variety carrying D1 to D2 (up to squares) — the ι-candidate reborn as a
FUNCTION-SWAP (not a point-involution; that was killed by unequal factor
degrees). Natural construction target: the parameter transformation
exchanging the two Cayley factors of the conjugation word (R1R2 ↔ R2R1
or inverse), which fixes the tie conditions (conjugate families) and
exchanges D1 ↔ D2. If that map exists ℚ-rationally on the variety, the
equality follows by norm functoriality — a one-page proof obligation.

## Will's desk (stage close)
1. Accept 3b.3-d close (PD.2's routed branch = this report).
2. Next probe candidate (needs new freeze): **construct the swap
   correspondence** — check whether (t1,t2,t3) ↦ the R2R1-word parameters
   defines a ℚ-rational automorphism of the miniature tie variety with
   D1∘swap = D2·(square). PASS ⟹ the norm law becomes a THEOREM with a
   one-page proof; FAIL ⟹ the equality needs a subtler source (Brauer/
   corestriction route). Alternatives: rational-point geometry (§M4 a),
   miniature Frobenius (§M4 c), or session close.

*GROUNDED — Will, S-2026-07-05b ("Accept 3b.3-d close"); the PD.2 routing is
thereby resolved-as-recorded. Swap-correspondence proof target remains on
the desk, unruled. All numbers ×2-backed in records/.*
