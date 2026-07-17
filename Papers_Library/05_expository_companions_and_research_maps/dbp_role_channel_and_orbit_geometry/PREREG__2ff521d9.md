# PREREG — Campaign F: RoleChSpec Diversity Mechanism

**Status:** pre-registration, recorded **before** any generated report.
**Tier:** eval-tier only. No substrate promotion. Does not change Campaign A/D/E artifacts. Successor to Campaign E.
**Discipline:** exact `fractions.Fraction`; stdlib only; no float in any graded path; canonical `{"num": n, "den": d}`; deterministic, two-run byte-identical.

## Question

Campaign E showed structural diversity (esp. `diag_support_set_size`) predicts RoleChSpec survival. Campaign F asks **why** — is the diversity axis a proxy for an exact gauge-obstruction rank? The target is a mechanism, not another classifier.

## Central hypothesis (H-F0)

RoleChSpec survival occurs when the representatives of a reduced carrier class **cannot** be absorbed by the same-gradient gauge fibre `H → H + g a^T + a g^T`; collapse occurs when they all lie in one gauge fibre. Structural diversity is the visible Hessian-level shadow of this obstruction.

## Exact gauge-obstruction (the central formula)

For fixed regular `g` (all `g_i ≠ 0`) and `ΔH = H' − H` symmetric, a same-gradient gauge difference forces `a_i = ΔH_ii / (2 g_i)`, leaving the off-diagonal obstruction

```
O_ij(ΔH; g) = ΔH_ij − g_i·ΔH_jj/(2 g_j) − g_j·ΔH_ii/(2 g_i)     (i < j)
```

`O(ΔH;g) = 0  ⟺  ΔH ∈ Im(a ↦ g a^T + a g^T)`. For n=3, `O = (O_12, O_13, O_23)`.
`obstruction_rank(class) = rank_Q { O(H_r − H_0; g) }`.

## Two lanes (non-tautology — failure if violated)

- **Lane 1 — structural grammar features:** Hessian support/rank/sign/diversity only.
- **Lane 2 — analytic mechanism variables:** exact gauge-obstruction ranks from `(g,H)`.

Neither lane reads: RoleChSpec fingerprint/equality, gauge verdict label, survival/collapse label, direct-carrier fingerprint, `n_direct_carriers`. The label is used only as an **outcome** for comparison.

## Verified findings (computed before pinning; reported here as the registered expectation)

- **H-F3 = PASS_STRONG (exact, 0 exceptions):** over all 5298 classes,
  `obstruction_rank = 0 → 0 survive / 1917 collapse`; `rank 1 → 2549 / 0`; `rank 2 → 832 / 0`.
  **Survival ⟺ obstruction_rank > 0.**
- **H-F2 reproduces** the Campaign E `diag_support_set_size` table exactly (size 1→496/816, 4→437/13, 5→91/0, 7→21/0, 8→22/0).
- **H-F5 honest nuance:** the candidate `diag_support_set_size ≥ 5 ⟹ obstruction_rank > 0` is **REFUTED** — size **6** contains 3 classes with `obstruction_rank = 0` (collapses). The exact criterion is `obstruction_rank > 0`, which explains why sizes {5,7,8} are pure survivors and 6 is not. This exception will be reported, not hidden.
- `gauge_image_rank = 3` for all three regular gradients.

## Claims

- **CL-F1** integrity: Campaign D/E counts reproduce (5298 / 3381 / 1917 / 0).
- **CL-F2** feature reproduction: Campaign E `diag_support_set_size` table reproduces exactly.
- **CL-F3** exact gauge-obstruction formula: passes gauge-construction unit tests (`O(g a^T+a g^T)=0`; mutation detected).
- **CL-F4** obstruction-rank mechanism: graded PASS_STRONG / PASS_ASYMMETRIC / PARTIAL / FAIL with full cross-tab.
- **CL-F5** diversity/rank monotonicity: exact tables.
- **CL-F6** pure-survivor threshold: graded; the `≥5` candidate refuted by size 6, obstruction criterion confirmed.
- **CL-F7** collapse limitation: collapse = obstruction_rank 0 = structurally uniform; g-specificity reported, not solved.
- **CL-F8** non-tautology / mutation controls: 9 mutants caught.

## Candidate Theorem F

For regular same-gradient n=3 classes in the frozen A/D/E atlas, RoleChSpec survival is controlled by the obstruction space `O(Span_Q{H_r − H_0}; g)`: nonzero ⟹ ≥2 gauge-inequivalent active-role sections (survive); zero ⟹ same gauge fibre (collapse). `diag_support_set_size` is a support-level proxy. **This is a theorem candidate confirmed within the frozen bound, not an assumed truth.**

## Non-goals
n ≥ 4 claims; substrate promotion; mining new predictive rules as the main deliverable; changing A/D/E artifacts; cross-gradient equivalence; a complete theorem outside the frozen bound.
