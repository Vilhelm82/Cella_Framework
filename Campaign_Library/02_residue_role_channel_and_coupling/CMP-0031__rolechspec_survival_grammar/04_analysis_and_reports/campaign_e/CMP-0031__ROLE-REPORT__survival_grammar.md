# SURVIVAL GRAMMAR — Campaign E

The main scientific summary. Eval-tier; a structural grammar **inside the frozen bound**, not a complete theory.

## Headline

Campaign D's survival/collapse split (3381 / 1917 over 5298 separation classes) is **not arbitrary**: it is predicted by deterministic, exact, held-out-validated rules over purely **Hessian-structural** features. One sentence:

> A separation class **survives** the RoleChSpec quotient when its representatives are structurally **diverse** and non-degenerate (high diagonal-support diversity, full rank); it **collapses** as gauge residue when its representatives are structurally **uniform** (single diagonal-support pattern, total channel cancellation, thin coupling-graph families).

All predictors are §7 Hessian-structural. The count of distinct carriers (`n_direct_carriers`) — which also predicts survival — is deliberately **excluded** from mining as debug-only metadata, so the grammar is genuinely about Hessian structure, not carrier bookkeeping.

## What was found

- **2563 confirmed minimal rules** (support ≥ 10, 0 violations in the bound). **1759 are held-out validated** under leave-one-g-out; 804 are train-only; 0 rejected.
- **Survival is driven by `diag_support_set_size ≥ 4` with full-rank reps.** The strongest rules (all held-out validated):
  - `E-RULE-0001`: `any_rank_drop is_false AND channel_zero_pattern_set_size_r2 ≤ 4 AND diag_support_set_size ≥ 4` → SURVIVES (support 273)
  - `E-RULE-0003`: `any_channel_cancellation_r1 is_true AND any_rank_drop is_false AND diag_support_set_size ≥ 4` → SURVIVES (support 236)
- **Collapse is driven by structural uniformity.** The collapse rules (all train-only — see below):
  - `E-RULE-0026`: `all_channel_cancellation_r1 is_true AND channel_sign_pattern_set_size_r2 ≤ 2 AND graph_family_set == {open_chain, single_edge}` → COLLAPSES (support 30)
  - `E-RULE-0029`: `channel_sign_pattern_set_size_r2 == 1 AND diag_support_set_size == 1 AND graph_family_set == {single_edge, triangle}` → COLLAPSES (support 24)

`diag_support_set_size` (the number of distinct diagonal-support masks among a class's representatives) is the single most informative feature, and it points in **opposite directions** for the two outcomes: `≥ 4` ⇒ survive, `== 1` ⇒ collapse. This is the core of the grammar.

## Confirmed rules (sample — full set in `RULE_LEDGER.md` / `summary.json`)

See `RULE_LEDGER.md` for the reported 25 survive + 15 collapse rules with support and held-out status.

## Rejected near-rules / mixed families

The highest-support predicates are near-universal and do **not** discriminate (reported honestly, CL-E4):

| predicate | support | survive | collapse |
|---|---|---|---|
| `reduced_tower_is_zero is_false` | 5296 | 3381 | 1915 |
| `support_mask_set_size ≤ 20` | 5297 | 3380 | 1917 |
| `rank_max ≥ 2` | 5295 | 3378 | 1917 |

Coupling-graph family alone is also mixed (see `FAMILY_REPORT.md`): e.g. `graph_family_set == {open_chain, triangle}` is 1454 survive / 906 collapse (62% pure) — predictive only in conjunction with support-diversity features.

## Coverage summary

- Confirmed rules: 2563 (2546 survive-predicting, 17 collapse-predicting).
- Held-out validated: 1759 (all are survive-direction, robust across all three g-values).
- Train-only: 804 — including **every** collapse rule. The collapse grammar is **g-specific** within this bound: it does not (yet) generalise across all three gradients, whereas the survival grammar does.

## What remains unexplained

- The **collapse direction is only train-only.** No collapse predicate was found that holds with support and zero violations on every g-slice — the collapse families depend on the gradient. A g-invariant collapse rule, if one exists, needs richer or different features.
- Survival rules are abundant but **mostly conjunctions of 3**; no single Hessian feature cleanly separates the classes. The grammar is real but not low-dimensional.
- Why `diag_support_set_size` is the dominant axis is an empirical observation, not a derived theorem.

## Scope limits

Frozen Campaign A/D bound only (g ∈ {(1,1,1),(1,2,3),(2,-1,1)}, entries {-2..2}). n = 3. No n ≥ 4, no cross-gradient equivalence, no symbolic theorem beyond these finite-bound rules. Eval-tier only; no substrate promotion. Does not change the Campaign D result.

## Successor doors

- A g-invariant collapse rule (richer features: full sign/zero patterns, orbit-structure of the reps).
- Extend the grammar to n = 4 and test whether `diag_support_set_size`-style diversity remains the survival axis.
- Derive (rather than mine) why structural diversity ⇒ survival: connect to the gauge orbit dimension within a reduced-tower class.
