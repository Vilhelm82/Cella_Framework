# INJECTIVITY REPORT — Campaign H (Lemma H4, CL-H4)

## The claim

`RoleChSpec_g(H_perp(O)) = RoleChSpec_g(H_perp(O'))  ⟹  O = O'` on the regular locus.

## Proof — explicit linear recovery (constructive)

The `r=1` channel vectors give **6 linear forms in `O = (O12, O13, O23)`** (two per output role). Their `6×3` coefficient matrix has **rank 3** (verified symbolically). A `3×3` minor has determinant

```
det = 16 g2⁴ (g1² + g3²) / (g1³ g3⁶),     numerator = 16 g2⁴ (g1² + g3²).
```

Since this minor is invertible, `O` is recovered as an **explicit linear function** of the corresponding RoleChSpec components:

```
O = (minor)^{-1} · (the three chosen r=1 channel values).
```

Therefore if two carriers `O, O'` give equal RoleChSpec, their `r=1` components agree, and the invertible minor forces `O = O'`. **RoleChSpec is injective in `O`.**

## Why linear recovery, not a hard ideal computation

The brief's fallback (build the equality ideal `I_equal`, test `rad(I_equal) = rad(I_diag)` via Gröbner/elimination after saturation) is **subsumed**: because the `r=1` channels are *linear* in `O` with a rank-3 coefficient matrix, `I_equal` already contains 3 independent linear forms `O − O'`, so it equals `⟨O12−O12', O13−O13', O23−O23'⟩` directly — no Gröbner basis is needed. The linear certificate is both simpler and exact.

## Saturation

The recovery requires `det ≠ 0`. Over **Q**, the numerator `16 g2⁴ (g1² + g3²)` is nonzero whenever `g1 g2 g3 ≠ 0` (since `g1² + g3² = 0` over Q forces `g1 = g3 = 0`, excluded by regularity). So the saturation denominator is exactly the regularity denominator `g1 g2 g3`, and there is **no exceptional stratum beyond regularity** over Q (see `EXCEPTIONAL_LOCUS_REPORT.md`).

**CL-H4: PASS** — `r1_coefficient_rank = 3`, minor numerator `16 g2⁴ (g1² + g3²)`, `injective_on_regular_Q_locus = True`.

### Note (additive): the recovery does not depend on the `(g1²+g3²)`-bearing minor

What matters for injectivity is the **rank**, not any particular minor. The minor used above carries a `(g1²+g3²)` factor (definite over Q, indefinite over ℂ), but the rank is certified 3 by *other* minors too. In particular the minor on the three **coupling** rows (0,2,4) is `det = 32/(g1 g2 g3)` — numerator the constant `32 = 2⁵` — which is nonzero on the entire regular locus over **any field where 2 is invertible**. So the rank is 3 at every regular point over every characteristic-0 field (and more), independent of `g1²+g3²`. This sharpens the ceiling from "over Q" to **char ≠ 2** (recorded as **CL-H8**); the `(g1²+g3²)` factor is an artifact of one minor, not a real obstruction.
