# EXCEPTIONAL LOCUS REPORT — Campaign H (CL-H5)

The injectivity recovery uses a minor with determinant `16 g2⁴ (g1² + g3²)/(g1³ g3⁶)`. Its **numerator is g-only** (no `O`), and factors as

```
16 · g2⁴ · (g1² + g3²).
```

## Typing the factors

| factor | zero set | inside non-regular? |
|---|---|---|
| `16` | ∅ | — |
| `g2⁴` | `g2 = 0` | yes (`g1 g2 g3 = 0`) |
| `g1² + g3²` | over Q: `g1 = g3 = 0` | yes (`g1 = 0`) |

`g1² + g3²` is a **sum of squares**, hence positive definite over ℝ ⊇ ℚ; its only real (so only rational) zero is `g1 = g3 = 0`. (Over ℂ it would factor as `(g1 − i g3)(g1 + i g3)` — irrelevant over Q.)

## Result

The minor numerator vanishes only on `g2 = 0` or `g1 = g3 = 0`, both contained in the non-regular locus `g1 g2 g3 = 0`. Therefore on the **regular Q-locus** the minor is nonzero everywhere → the `r=1` coefficient matrix has rank 3 at every regular rational `g` → injectivity holds **with no exceptional stratum beyond regularity**.

```
regularity_denominator D_regular = g1 * g2 * g3
empty_on_regular_Q_locus = True
typed_strata = [ non_regular: g1*g2*g3 = 0  (ROLE_CHART_UNAVAILABLE / SINGULAR_GRADIENT) ]
```

**CL-H5: PASS.** No denominator component is silently discarded; the single sum-of-squares factor is explicitly typed and shown definite over Q.

> Scope note: the proof is stated **over Q**. Over a field where `−1` is a square, `g1² + g3² = 0` has nontrivial solutions and that locus would become a genuine exceptional stratum. This is explicitly *not claimed*.

## Correction (char-0 strengthening — additive; the over-Q claim above is unchanged)

An independent audit established that the scope note above is **conservative**: `g1² + g3² = 0` is **not** a genuine exceptional stratum, because that single `(g1²+g3²)`-bearing minor is not the only rank-3 witness — the rank does not drop there.

Verified exactly (recomputed from the H3 formulas, not cached):

- The 6×3 `r=1` coefficient matrix has **twenty** 3×3 minors. The minor on the three **coupling** rows (0,2,4) is `det = 32/(g1 g2 g3)` — its numerator in lowest terms is the **constant 32 = 2⁵**, nonzero on the *whole* regular locus over any field where 2 is invertible.
- Consequently the ideal of minor numerators is already `⟨1⟩`: the **Control** Gröbner basis `⟨minor numerators⟩` came back `⟨1⟩` (not the expected non-unit), so the Rabinowitsch saturation `⟨minor numerators, 1 − t·g1g2g3⟩ = ⟨1⟩` is **vacuous** — a single minor is already a unit over the regularity denominator. (The non-constant minors alone *do* share `g=0`, as expected.)
- `g1²+g3²=0` is covered by the coupling minor `32/(g1g2g3)`, so the rank is **3 at every regular point over the algebraic closure** of any char-≠2 field — including ℂ, not just ℚ.

**Sharp ceiling: char ≠ 2** (any field where 2 is invertible), recorded as **CL-H8** in the ledger. The factor `2` is the precise obstruction — and char 2 is itself a *derived structural wall*, not a margin (see `CHAR2_BOUNDARY_REPORT.md`, **CL-H9**). Reproducible exactly via `char_boundary.explicit_minor_certificate`. Nothing here alters CL-H5.
