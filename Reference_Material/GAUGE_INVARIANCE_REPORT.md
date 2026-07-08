# GAUGE INVARIANCE REPORT — Campaign G (CL-G1, CL-G3)

## The exact gauge-image lemma (CL-G1)

For regular `g` and `ΔH = H2 − H1 ∈ Sym_3(Q)`:

```
O_ij(ΔH; g) = ΔH_ij − g_i·ΔH_jj/(2 g_j) − g_j·ΔH_ii/(2 g_i)
O_g(ΔH) = 0   ⟺   ΔH ∈ Im(G_g),   G_g(a) = g a^T + a g^T.
```

Verified by **two independent computations** (the closed formula and the off-diagonal residual of `ΔH − G_g(gauge_coeffs(ΔH))`), which agree on every sampled `ΔH`; and by the rank test `ΔH ∈ Im(G_g) ⟺ rank[basis] = rank[basis ∪ {ΔH}]`, which coincides exactly with `O = 0`. Construction controls: every `G_g(a)` has zero obstruction; every single-entry mutation is detected. `gauge_image_rank(g) = 3` for all six regular gradients.

## The proven direction (CL-G3) — gauge invariance holds, 0 counterexamples

`O_g(ΔH) = 0 ⟹ RoleChSpec_g(H1) = RoleChSpec_g(H2)` is Campaign D's gauge-invariance (CL-D1), re-verified here by **recomputation** (not cached labels). Gauge-positive controls `H2 = H + G_g(a)` across all six gradients × the edge / degenerate-channel / self-glue bases × four gauge vectors:

```
gauge_invariance_counterexamples (Type B): 0
```

**Outcome C (gauge-invariance failure) did not occur.** This is the expected, proven direction — its survival here confirms the obstruction formula and the RoleChSpec recomputation are consistent with Campaign D.

## Why this matters for the theorem

T-G is an "iff". This report establishes the gauge-image lemma (CL-G1) and the easy/proven implication (CL-G3) exactly. The hard implication — faithfulness, `O ≠ 0 ⟹ RoleChSpec differ` — is the subject of the adversarial attack in `FAITHFULNESS_SEARCH_REPORT.md` (no counterexample found).
