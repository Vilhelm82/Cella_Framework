# MUTATION REPORT — Campaign F

Nine deliberately-wrong variants (`src/lloyd_v4/evals/rolechspec_diversity_mechanism/mutants.py`).
For each, `tests/test_campaign_f_mutants.py` shows the correct engine passes a check and the mutant
fails the same check. All mutant tests pass (all 9 caught). Mutants are the only place a kill is permitted.

| # | mutant | wrong behaviour | check that catches it | kill |
|---|---|---|---|---|
| M1 | `mutant_features_label_leak` | adds `survival_label` as a feature | `assert_no_forbidden` raises | K-F4 |
| M2 | `mutant_features_rolechspec` | adds a RoleChSpec-fingerprint key as a feature | `assert_no_forbidden` raises | K-F4 |
| M3 | `mutant_features_gauge_verdict` | adds a gauge-verdict key as a feature | `assert_no_forbidden` raises | K-F4 |
| M4 | `mutant_obstruction_no_factor2` | drops the factor 2 in `a_i = ΔH_ii/(2 g_i)` | a true gauge difference no longer has zero obstruction | K-F3 |
| M5 | `mutant_obstruction_sign_flip` | flips the sign of one off-diagonal correction term | a true gauge difference no longer has zero obstruction | K-F3 |
| M6 | `mutant_rank_float` | computes rank with float elimination | miscounts an exact rank-1 set `[[1/10,2/10,3/10],[7/10,14/10,21/10]]` as 2 | K-F (float) |
| M7 | `mutant_shuffle_labels` | permutes survival/collapse labels | the obstruction mechanism verdict is no longer PASS_STRONG | K-F6 (alignment) |
| M8 | `mutant_drop_exceptions` | suppresses the reported `≥5` counterexamples | the completeness check finds `n_ge5_counterexamples` zeroed | K-F (completeness) |
| M9 | `mutant_features_n_direct` | adds `n_direct_carriers` to the feature table | `assert_no_forbidden` raises (it is debug-only metadata) | K-F4 |

## Why these are not tautological

- **Lane separation is architectural** (not just runtime): source-scan tests (`test_campaign_f_non_tautology.py`) prove `features_structural.py` and `gauge_obstruction.py` import no RoleChSpec/gauge engine, no labels, no NumPy, no `float(`. M1–M3, M9 must inject a forbidden key explicitly and are caught by the runtime gate.
- **The obstruction formula is checked by construction** (M4, M5): a true gauge difference `g a^T + a g^T` must have zero obstruction; any formula corruption breaks that exactly.
- **Float is caught structurally** (M6): the campaign uses exact `Q` rank; a float rank gives a provably wrong answer on an exact near-singular set.
- **Label integrity is checked** (M7): shuffling the outcome labels destroys the measured PASS_STRONG alignment, so a label-corrupting engine cannot pass H-F3.
- **Exceptions cannot be hidden** (M8): the `≥5`-threshold counterexamples (size 6) are recomputed and reported; suppressing them fails the completeness check (and the report explicitly carries the size-6 anomaly).
