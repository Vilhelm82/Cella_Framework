# MUTATION REPORT — Campaign E

Eight deliberately-wrong variants (`src/lloyd_v4/evals/rolechspec_survival_grammar/mutants.py`).
For each, `tests/test_rolechspec_survival_grammar_mutants.py` shows the correct engine passes a
check and the mutant fails the same check. All mutant tests pass (all 8 caught). Mutants are the
only place a kill condition is permitted to fire.

| # | mutant | wrong behaviour | check that catches it | kill |
|---|---|---|---|---|
| 1 | `mutant_class_features_with_leak` | injects `survival_label` into the feature table | `assert_no_forbidden` raises on the leaked target field | KC-E2 / KC-E9 |
| 2 | `mutant_all_survive` | labels every class SURVIVES | `label_counts` no longer matches the true mixed split | KC-E1 |
| 3 | `mutant_all_collapse` | labels every class COLLAPSES | `label_counts` no longer matches the true split | KC-E1 |
| 4 | `mutant_bad_rule_no_violations` | reports a mixed predicate as 0-violation | `evaluate_rule` recomputes the true violation count (> 0) | KC-E3 |
| 5 | `mutant_enumerate_skip` | silently drops 1/5 of classes | class count ≠ 5298 | KC-E7 |
| 6 | `mutant_float_feature` | pushes `rank_min` through `float` | canonical encoder raises `TypeError` on the float | KC-E5 |
| 7 | `mutant_unstable_features` | emits `graph_family_set` as a raw (unordered) `set` | canonical encoder raises `TypeError` on the non-canonical set | KC-E6 (byte-stability) |
| 8 | `mutant_holdout_always_validated` | marks a rule held-out validated without evaluating | `heldout_status` re-evaluates and returns `RULE_TRAIN_ONLY` for a g-specific rule | KC-E4 / CL-E5 |

## Why these are not tautological

- The non-leakage guard is **architectural**: `features.py` imports no target engine (a source-scan test enforces it), and `assert_no_forbidden` is a runtime gate. Mutant 1 must go out of its way to inject the target, and is caught immediately.
- The label mutants (2, 3) are measured against the **independently reproduced** Campaign D split (3381 / 1917), not against themselves.
- The float and set mutants (6, 7) are caught **structurally** by the canonical encoder, which refuses anything that is not an exact `{num,den}` / int / bool / str / list — so a float or a raw set can never reach a graded artifact.
- The held-out mutant (8) is caught by re-running the exact leave-one-g-out evaluation, which finds the rule has no support on some held-out gradient.
