# SYMBOLIC RoleChSpec FORMULAS — Campaign H (Lemma H2, H3 / CL-H2, CL-H3)

## Lemma H2 — RoleChSpec depends only on the gauge-normal carrier (CL-H2)

Verified symbolically: for arbitrary `b`, `RoleChSpec_g(H_perp + G_g(b)) = RoleChSpec_g(H_perp)` — every chart channel-vector component is invariant under adding a gauge. Hence `RoleChSpec_g(H) = RoleChSpec_g(H_perp)`, i.e. RoleChSpec is a function of `(g, O)` alone. (`q_chart` is even more obviously gauge-independent: `g_chart` depends only on `g`.)

## Lemma H3 — closed RoleChSpec formulas in (g, O) (CL-H3)

`q_chart` per role: `(g1²+g2²+g3²)/g_k²` (depends only on g).
**`κ_int = 0` for every graph chart** (the `r=2` `(1,1)` component vanishes identically).

### r = 2 (even, homogeneous quadratic in O) — pure-self channel `κ̂_{0,2}`

| role | output | `κ̂_{0,2}` |
|---|---|---|
| Product | k=2 | `4 g1 g2 · O13 O23 / g3⁴` |
| Directive | k=0 | `4 g2 g3 · O12 O13 / g1⁴` |
| Substrate | k=1 | `4 g1 g3 · O12 O23 / g2⁴` |

The pure-coupling channel `κ̂_{2,0}` is a quadratic form in `O`, e.g. for Product:
`(−g3² O12² + 2 g2 g3 O12 O13 + 2 g1 g3 O12 O23 − g2² O13² − 2 g1 g2 O13 O23 − g1² O23²)/g3⁴`.

The three self-channels expose the three **pairwise products** `O13O23, O12O13, O12O23` — these determine `O` up to a global sign, which the (odd) `r=1` channels then fix.

### r = 1 (odd, linear in O) — the sign-resolving channels

For Product (k=2):
```
κ̂_{1,0} = (2 g1 g2 g3 O12 − 2 g1 g2² O13 − 2 g1² g2 O23)/g3⁴
κ̂_{0,1} = (2 g1 g2² O13 + 2 g1 g3² O13 + 2 g1² g2 O23 + 2 g2 g3² O23)/g3⁴
```
and cyclically for the other roles. These are **linear forms in O**, the basis of the injectivity proof (see `INJECTIVITY_IDEAL_REPORT.md`).

## Parity — why r=1 is the key

`H_chart` is **linear and homogeneous** in `O` (the gauge-normal Hessian has zero diagonal, so the chart entries carry no constant term). Therefore the `r=2` density (a determinant quadratic in `H_chart`) is **even** in `O` — blind to `O ↦ −O` — while the `r=1` density (linear in `H_chart`) is **odd**. The full RoleChSpec fingerprint contains both, so it resolves the sign and is injective.
