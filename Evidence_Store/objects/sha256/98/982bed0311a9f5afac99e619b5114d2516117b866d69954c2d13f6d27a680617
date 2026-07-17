# MUTATION REPORT — Campaign G

Ten deliberately-wrong variants (`src/lloyd_v4/evals/rolechspec_gauge_obstruction_faithfulness/mutants.py`).
For each, `tests/test_campaign_g_mutants.py` shows the correct engine passes a check and the mutant
fails the same check. All mutant tests pass (all 10 caught). Mutants are the only place a kill is permitted.

| # | mutant | wrong behaviour | check that catches it | kill |
|---|---|---|---|---|
| M1 | `mutant_obstruction_no_factor2` | drops the factor 2 in `a_i = ΔH_ii/(2 g_i)` | a true gauge difference no longer has zero obstruction | K-G1 |
| M2 | `mutant_obstruction_sign` | flips the sign of one off-diagonal term | a true gauge difference no longer has zero obstruction | K-G1 |
| M3 | `mutant_float_rank` | rank via float elimination | miscounts an exact rank-1 set as 2 | K-G5 |
| M4 | `mutant_cached_rolechspec` | returns a cached coarse label instead of recomputing | two genuinely different regular jets are wrongly equated | K-G6 |
| M5 | `mutant_accept_singular` | types a singular jet (`g_0 = 0`) as REGULAR | the regularity gate would reject it; the mutant accepts | K-G4 |
| M6 | `mutant_shuffle_rolechspec` | a non-gauge-invariant "RoleChSpec" (raw Hessian entries) | a gauge pair (RoleChSpec equal) is wrongly reported different | K-G2 (gauge invariance) |
| M7 | `mutant_skip_self_glue` | claims the self-glue stage PASSED without running it | completeness: PASS with `n_samples = 0` | (CL-G6) |
| M8 | `mutant_suppress_counterexamples` | drops counterexample records | a planted counterexample disappears from the result | (completeness) |
| M9 | `mutant_weak_equal` | compares RoleChSpec by a truncated-string prefix | two distinct fingerprints with a shared prefix compare equal | K-G3 (false faithfulness) |
| M10 | `mutant_forbidden_import_source` | a verdict path that imports survival labels for equality | the non-tautology source scan flags the forbidden import | K-G6 |

## Why these are not tautological

- **The obstruction formula is checked by construction** (M1, M2): a true gauge difference `G_g(a)` must have zero obstruction, computed two independent ways; any corruption breaks that exactly.
- **Exactness is structural** (M3): the campaign uses exact `Q` rank everywhere; a float rank gives a provably wrong answer.
- **RoleChSpec is recomputed, never cached** (M4, M10): a cached/label shortcut is caught either by recomputation distinguishing the jets or by the source scan flagging a forbidden label import.
- **Singularities are typed** (M5): the regularity gate refuses non-regular jets; a mutant that accepts them is caught.
- **Equality is complete and gauge-invariant** (M6, M9): a non-invariant or truncated comparison breaks the proven gauge direction or fabricates faithfulness.
- **Counterexamples and stages cannot be hidden** (M7, M8): completeness checks catch a skipped stage or a suppressed counterexample.
