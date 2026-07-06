# RC-7 — the shape moment (isotypic readout), re-proven (exact-ℚ tier)

**Certificate:** `verification/recert_shape_moment.py` — byte-stable ×2, stdout sha16
`d63a6549c11af9a2`, exit 0. Fresh code, zero-import: S₄ characters recomputed **two
ways** (textbook table + fresh Murnaghan–Nakayama on beta-sets, asserted equal); no
sympy; exact `Fraction` on every verdict path.

## Statement re-proven — retrodiction of [SR] I.6 / CALC-30 (n=4 witness)

Shape-moment carrier `Λ_{k,{j,l}}(H) = −(H_jl − H_jk − H_kl + H_kk)`, over the 12 flags
`(chart k, pair {j,l} ⊆ roles\{k})`. The CALC-30 finite two-state witness (role-0
gauge-fixed slice):

```
        (H11,H22,H33)  (H12,H13,H23)
  H0  =   ( 2,-1, 3)    ( 1,-2, 1)
  H   =   (-2,-2,-6)    ( 2,-1,-1)
```

reproduced exactly from the formula:
`A(H0)=(-1,2,-1,-1,-4,-4,2,2,5,-5,-2,-5)`, `A(H)=(-2,1,1,4,1,4,4,1,4,5,5,2)`.
Per-chart magnitude identical `(C)(H0)=(C)(H)=(6,33,33,54)`; carriers differ.
`ΔA = A(H)−A(H0) = (-1,-1,2,5,5,8,2,-1,-1,10,7,7)`, `‖ΔA‖² = 324`.

Isotypic norms of `ΔA` under S₄, by two independent routes:

```
   triv   std   (2,2)   (2,1,1)   sgn      Σ
   147    153    24       0        0      324
```

- **Route 1** — character isotypic projectors `P_λ = (d_λ/24) Σ_g χ^λ(g) ρ(g)`,
  verified idempotent, symmetric, and `Σ_λ P_λ = I` on the 12-space.
- **Route 2** (no character theory) — Parseval `Σ = 324 = ‖ΔA‖²`; `triv = (Σ ΔA)²/12
  = 42²/12 = 147` by projection on the all-ones flag vector; `sgn` and `(2,1,1)`
  forced `0` because `ΔA ∈ Im(L) = triv ⊕ std ⊕ (2,2)`.

**`sgn = 0` is structural, not witness luck.** The flag module decomposes as
`triv ⊕ 2·std ⊕ (2,1,1) ⊕ (2,2)`; the L-image is `triv ⊕ std ⊕ (2,2)`, so the shape
content is exactly the `(2,2)` doublet the per-chart magnitude is blind to.

## Dimension threshold (n ≥ 5), re-derived (CALC-27)

Scalars `σ_r` resolve the shape iff `(n−1) ≥ dim S^(n−2,2) = n(n−3)/2 ⟺ n²−5n+2 ≤ 0
⟺ n ≤ 4`:

```
 n   dim_shape  #σ_r  resolves  kernel≥
 3      0        2      yes       0
 4      2        3      yes       0      (V₄ accident)
 5      5        4      no        1
 6      9        5      no        4
 7     14        6      no        8
```

"Scalars insufficient at n ≥ 5" holds by dimension alone — K-3's dominance clause stands.

## Scope, stated exactly

n=4 witness retrodicted exact-ℚ; the threshold algebra is proven for all n. Gauge-fixed
slice (role-0 row = 0); the pair-module isotypic decomposition is the gauge-invariant
Hessian quotient (CALC-27). This discharges P2's **target-value** retrodiction. The
fresh per-corpus two-route sensor reference values (Stage A) build on these projectors.

## Tier & gate

`[computer-verified — exact ℚ, byte-stable ×2]` (quintuple, Parseval, carrier
reproduction, projector certificate) / `[proven]` (threshold inequality).
**Gate K-3: NOT fired.**

## Load-bearing pins (confirmed unedited during the run)

```
verification/recert_shape_moment.py                            fa6e3cc249408604
old_program_sources/Calc_logs/dbp four role calc log v8.md     e22842706809a85c   (CALC-30 target source)
stdout(recert_shape_moment.py)                                 d63a6549c11af9a2   (byte-stable ×2)
```
