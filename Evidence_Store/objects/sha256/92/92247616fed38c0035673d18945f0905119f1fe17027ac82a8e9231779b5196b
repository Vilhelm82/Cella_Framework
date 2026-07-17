# OBSTRUCTION RANK REPORT — Campaign F (H-F3, CL-F4)

## The mechanism

For fixed regular gradient `g` and `ΔH = H' − H` symmetric, a same-gradient defining-function gauge difference forces `a_i = ΔH_ii/(2 g_i)`, leaving the off-diagonal obstruction

```
O_ij(ΔH; g) = ΔH_ij − g_i·ΔH_jj/(2 g_j) − g_j·ΔH_ii/(2 g_i)     (i < j),
O(ΔH;g) = 0  ⟺  ΔH ∈ Im(a ↦ g a^T + a g^T).
```

For a class, `obstruction_rank = rank_Q { O(H_r − H_0; g) }` — the dimension of the gauge-obstruction space spanned by its representatives relative to a base. (Base-relative and pairwise ranks agree everywhere; `base_vs_pairwise` disagreements = 0.)

## Result — exact, zero exceptions

| obstruction_rank | survive | collapse |
|---|---|---|
| 0 | **0** | **1917** |
| 1 | **2549** | 0 |
| 2 | **832** | 0 |

**Survival ⟺ obstruction_rank > 0**, with **0 counterexamples** over all 5298 classes. Verdict: **PASS_STRONG** (CL-F4 PASS).

## Why this is exactly the mechanism

- Gauge-equivalence at fixed `g` is an equivalence relation, and `O(ΔH;g) = 0` iff `ΔH` is a gauge image. So `obstruction_rank = 0` iff all representatives lie in **one** same-gradient gauge fibre.
- RoleChSpec is the gauge-invariant carrier (Campaign D, CL-D1): gauge-equivalent ⟹ identical RoleChSpec. Therefore one gauge fibre ⟹ one RoleChSpec ⟹ **collapse**.
- `obstruction_rank > 0` ⟹ ≥ 2 gauge-inequivalent sections ⟹ ≥ 2 distinct RoleChSpec ⟹ **survive**.

The measured perfect alignment (0/1917, 2549/0, 832/0) is the empirical confirmation that the converse also holds within the bound: gauge-inequivalent representatives always carry distinct RoleChSpec here.

## Supporting facts

- `gauge_image_rank = 3` for all three regular gradients (the gauge map `a ↦ g a^T + a g^T` is full-rank on `Sym_3`'s 3-dimensional gauge subspace).
- The obstruction formula passes its construction self-check exactly: `O(g a^T + a g^T; g) = 0`; a single-entry mutation is detected (CL-F3 PASS).

This upgrades Campaign E's empirical "diversity predicts survival" to an exact statement: **survival is governed by a positive gauge-obstruction rank**, and structural diversity is its visible Hessian-support shadow (see `DIVERSITY_MECHANISM_REPORT.md`).
