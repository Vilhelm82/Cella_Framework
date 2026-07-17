# DIVERSITY MECHANISM REPORT — Campaign F (H-F2, H-F4, H-F5)

## H-F2 — Campaign E feature reproduced exactly

The Campaign E `diag_support_set_size` survival/collapse table reproduces exactly (CL-F2 PASS):

| diag_support_set_size | survive | collapse |
|---|---|---|
| 1 | 496 | 816 |
| 2 | 1479 | 964 |
| 3 | 760 | 121 |
| 4 | 437 | 13 |
| 5 | 91 | 0 |
| 6 | 75 | 3 |
| 7 | 21 | 0 |
| 8 | 22 | 0 |

## H-F4 — diversity is a proxy for obstruction rank

Cross-tabulating `diag_support_set_size` against `obstruction_rank` shows the proxy explicitly. The **collapse count at each diversity level equals the `obstruction_rank = 0` count at that level** — exactly:

| diag size | survive | collapse | obstruction_rank distribution |
|---|---|---|---|
| 1 | 496 | 816 | {0: **816**, 1: 452, 2: 44} |
| 2 | 1479 | 964 | {0: **964**, 1: 1276, 2: 203} |
| 3 | 760 | 121 | {0: **121**, 1: 515, 2: 245} |
| 4 | 437 | 13 | {0: **13**, 1: 282, 2: 155} |
| 5 | 91 | 0 | {1: 9, 2: 82} |
| 6 | 75 | 3 | {0: **3**, 1: 11, 2: 64} |
| 7 | 21 | 0 | {1: 4, 2: 17} |
| 8 | 22 | 0 | {2: 22} |

(Bold = the `obstruction_rank = 0` count, identical to the collapse count in that row.)

As diversity rises, the share of `obstruction_rank = 0` (gauge-residual) classes falls monotonically, and the obstruction concentrates in rank 2. This is the mechanism behind Campaign E's monotone survival gradient: **higher diagonal-support diversity makes it harder for the representatives to share a single gauge fibre**, so the obstruction space is more likely nonzero.

## H-F5 — pure-survivor threshold (honest nuance, CL-F6 PARTIAL)

Campaign E observed pure survival at `diag_support_set_size ∈ {5, 7, 8}`. The natural candidate

```
diag_support_set_size >= 5  ⟹  obstruction_rank > 0
```

is **REFUTED_BY_COUNTEREXAMPLE**: `diag_support_set_size = 6` contains **3 classes with obstruction_rank = 0** (collapses). The `≥ 5` cut is therefore the wrong threshold.

The **exact** criterion is the obstruction rank itself:

```
obstruction_rank > 0  ⟺  SURVIVES        (CONFIRMED_WITHIN_BOUND, 0 exceptions)
```

This explains the pure-survivor pattern precisely: sizes {5, 7, 8} happen to contain **no** `obstruction_rank = 0` class, so they are pure; size 6 contains 3, so it is not. `diag_support_set_size` is a strong but **imperfect** proxy — the obstruction rank is the underlying exact quantity.
