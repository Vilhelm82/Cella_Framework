# CLAIM LEDGER — Campaign F: RoleChSpec Diversity Mechanism

Eval-tier. Graded by `run_campaign_f.py`; byte-stability checked by `run_campaign_f.verify`. Machine-readable mirror: `summary.json → claims`. Nothing canonical until Will signs off.

Status vocabulary: **PASS** / **PARTIAL** / **FAIL** / **REFUSED**.

| Claim | Statement | Verdict | Evidence |
|---|---|---|---|
| **CL-F1** | integrity reproduction | **PASS** | counts reproduce exactly: 5298 total / 3381 survive / 1917 collapse / 0 undecided |
| **CL-F2** | feature reproduction | **PASS** | Campaign E `diag_support_set_size` pinned rows reproduce exactly (1→496/816, 4→437/13, 5→91/0, 7→21/0, 8→22/0) |
| **CL-F3** | exact gauge-obstruction formula | **PASS** | construction self-check: `O(g a^T+a g^T; g)=0`; single-entry mutation detected; unit-tested |
| **CL-F4** | obstruction-rank mechanism | **PASS** (PASS_STRONG) | obstruction_rank 0→0/1917, 1→2549/0, 2→832/0; **survive ⟺ rank>0, 0 exceptions** |
| **CL-F5** | diversity/rank monotonicity | **PASS** | exact diag-size × obstruction-rank tables; base vs pairwise obstruction rank agree (0 disagreements) |
| **CL-F6** | pure-survivor threshold | **PARTIAL** | `diag ≥ 5 ⟹ rank>0` REFUTED_BY_COUNTEREXAMPLE (size 6, 3 classes); the exact `rank>0 ⟺ survive` criterion CONFIRMED_WITHIN_BOUND |
| **CL-F7** | collapse limitation | **PASS** | all 1917 collapses have obstruction_rank 0; structurally uniform (93% at diag-size {1,2}); g-specific (g0:32, g1:1311, g2:574) |
| **CL-F8** | non-tautology / mutation controls | **PASS** | two-lane source scans pass; 9 mutants all caught |

## Kill conditions — all armed, none fired

| Kill | Fires when | Status |
|---|---|---|
| K-F1 | D/E counts not reproduced | silent |
| K-F2 | E diag table not reproduced | silent |
| K-F3 | obstruction formula fails on gauge differences | silent |
| K-F4 | feature layer reads forbidden labels / RoleChSpec / gauge verdict | silent (source scans + runtime gate) |
| K-F5 | mutation controls miss leakage / corruption | silent (9/9 caught) |
| K-F6 | obstruction rank unrelated to survival | silent (PASS_STRONG) |
| K-F7 | byte-stability fails | silent (two runs identical) |

**Kills fired: NONE.** Overall status **PASS**.

## Honesty register (acceptance §12.10 — separate the kinds of fact)

- **Proven exact facts:** the obstruction formula characterises the gauge image; `obstruction_rank 0 ⟺` single gauge fibre; one gauge fibre ⟹ one RoleChSpec ⟹ collapse (via Campaign D's proven gauge-invariance).
- **Measured finite-bound facts:** `obstruction_rank > 0 ⟹ survive` (0 exceptions in the frozen bound) — the converse, confirmed empirically.
- **Theorem candidate:** Candidate Theorem F (CONFIRMED_WITHIN_BOUND), not proven beyond the bound.
- **Unresolved exception families:** the `diag ≥ 5` threshold is refuted by size 6 (3 classes); collapse is g-specific and only structurally typed, not globally solved.

## Discipline
Exact ℚ, no float; stdlib only; Lane 1 / Lane 2 strictly separated; survival label used only as outcome; eval-tier only; no substrate modified; two runs byte-identical. **PENDING Will's sign-off.**
