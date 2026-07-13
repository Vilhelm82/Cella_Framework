# PROOF — CL-F1 (QUADRATIC BASIS)
**Claim.** For n ≥ 5, `{m2_triv, m2_std, m2_shape}` is a basis of the space of Sₙ-invariant quadratic forms on the pair module `M = M^(n−2,2) = ℚ^{pairs(n)}`.
**Status: PROVEN modulo classical representation theory (cited); CERTIFIED at n = 5, 6, 7 by the Stage A battery (FA.1 + FA.2). Prereg: FLAGSHIP_STAGE_A_PREREG.md.**

## Setup
Sₙ acts on M by permuting pair indices (the action induced by relabeling {1..n}). The decomposition into irreducibles is
```
M^(n−2,2)  ≅  S^(n)  ⊕  S^(n−1,1)  ⊕  S^(n−2,2)        (n ≥ 4)
```
— Young's rule for the two-row partition (n−2,2) [classical; corpus: computer-verified n = 4..9, Part I]. For n ≥ 5 the three summands are pairwise non-isomorphic and nonzero, of dimensions 1, n−1, n(n−3)/2. The decomposition is multiplicity-free.

## Step 1 — dimension of the invariant bilinear forms
By Schur's lemma, for a multiplicity-free module over a field of characteristic 0,
```
dim (M ⊗ M*)^{Sₙ}  =  Σ_λ (multiplicity of λ)²  =  1 + 1 + 1  =  3.
```

## Step 2 — all three land in the symmetric part
Every irreducible representation of Sₙ is defined over ℚ, hence real, with Frobenius–Schur indicator +1 [classical]. For an FS(+1) irreducible, the (unique up to scale) invariant bilinear form is **symmetric**. Cross-block pairings vanish (distinct irreducibles, Schur). Therefore
```
dim (Sym² M*)^{Sₙ} = 3,     dim (Λ² M*)^{Sₙ} = 0.
```

## Step 3 — the three moments are independent
`m2_X(O) = ⟨P_X O, O⟩` is Sₙ-invariant (P_X commutes with the action), and as a quadratic form its matrix is P_X. The projectors are orthogonal idempotents:
```
tr(P_X P_Y) = δ_XY · rank(P_X) ≠ 0,
```
so the three forms are pairwise trace-orthogonal and nonzero ⟹ linearly independent. Three independent vectors in a 3-dimensional space are a basis. ∎

## Corollary (ladder forcing, brief §3)
The degree-≤2 invariant supply is at most (n−1) σ-functions + 3 moments ≤ n+2, against a σ-fiber orbit space of dimension n(n−1)/2 − (n−1) (orbits are finite: distinct-entry g has trivial stabilizer). At n = 5 that is 7 functions against a 6-dimensional fiber with finite orbits — and the σ-blindness witness (39bed555) shows the σ-block is degenerate on shape directions. Degree 2 cannot be complete; the ladder must climb to degree 3. (P-F3's constructed witness, if found, realizes this count as an explicit tied pair.)

## Certificate hooks (battery FA.1 + FA.2)
1. Exact Molien: a₂ = 3 at n = 5, 6, 7 — independent count of Step 1+2's conclusion.
2. FS indicators: `ν(χ_λ) = (1/n!) Σ_w χ_λ(w²) = +1` for the three λ at n = 5, 6, 7 — Step 2's input, verified.
3. Trace Gram `tr(P_X P_Y) = δ_XY rank(P_X)` exactly at n = 5, 6, 7 — Step 3, verified.

## Known-background boundary (novelty hygiene)
Steps 1–3 are classical machinery; **no novelty is claimed for CL-F1 itself** — the brief prices it as the cheap PROVEN floor of the arm. The arm's novelty candidates live above it (σ-relative separation, the shape readout, CL-F3/F5), per the brief's §1 crown restriction.
