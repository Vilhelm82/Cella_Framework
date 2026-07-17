# COLLAPSE LIMITATION REPORT — Campaign F (H-F6, CL-F7)

Campaign E reported collapse rules as train-only / g-specific. Campaign F characterizes the collapse families exactly, without pretending to solve them globally.

## Collapse = obstruction_rank 0 (exact)

All **1917** collapse classes have `obstruction_rank = 0` — their representatives lie in a single same-gradient gauge fibre. There are **no** collapses with positive obstruction rank.

| collapse breakdown | distribution |
|---|---|
| by obstruction_rank | {0: **1917**} |
| by gradient g | g0=(1,1,1): 32 · g1=(1,2,3): 1311 · g2=(2,-1,1): 574 |
| by diag_support_set_size | {1: 816, 2: 964, 3: 121, 4: 13, 6: 3} |

## What this says

- **Collapse is structurally uniform.** 1780 of 1917 collapses (93%) sit at `diag_support_set_size ∈ {1,2}` — the lowest diversity. The mechanism: low diagonal-support diversity makes it easy for all representatives to share one gauge fibre, so the obstruction space is zero.
- **Collapse is g-specific.** The distribution across gradients is highly uneven — `g=(1,1,1)` produces only 32 collapses, `g=(1,2,3)` produces 1311. This is the g-specificity Campaign E observed (its collapse rules were all train-only / g-dependent). The collapse families do **not** generalise uniformly across gradients.
- **The size-6 anomaly is real and reported.** 3 collapses occur at `diag_support_set_size = 6` — the counterexamples to the `≥ 5` pure-survivor threshold. They are `obstruction_rank = 0` classes (gauge-residual) that happen to carry diverse diagonal support; the obstruction rank, not the diversity count, is what determines their collapse.

## What is NOT claimed

- No global solution of the collapse families is claimed. The result is the exact characterization `collapse ⟺ obstruction_rank 0` plus the measured g-distribution and diversity-distribution — **a structural typing, not a g-invariant theory of collapse**.
- A g-invariant collapse rule (if one exists) would need richer features than the present support/rank/diversity set; it is left as a successor door.

**Target result, supported by the records:** *Collapse = structurally uniform + g-specific same-gradient gauge-fibre normal form.*
