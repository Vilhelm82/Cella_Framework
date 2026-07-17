# MUTATION REPORT — Campaign D

Eight deliberately-wrong variants (`src/lloyd_v4/evals/active_role_channel_carrier/mutants.py`).
For each, `tests/test_active_role_mutants.py` shows the correct engine passes a check and the
mutant fails the same check. All 9 mutant tests pass (all 8 mutants caught). Mutants are the
only place a kill condition is permitted to fire.

| # | mutant | wrong behaviour | check that catches it | kill |
|---|---|---|---|---|
| 1 | `mutant_rechart_missing_Hkk` | drops `H_{k,k} h_a h_b` from the graph 2nd derivative | hand-pin CL-D3 fails on roles where H_kk ≠ 0 (Directive k=0, Substrate k=1) | KC-D1 |
| 2 | `mutant_rechart_wrong_sign` | uses `+g_i/g_k` instead of `-g_i/g_k` | hand-pin CL-D3 channel values fail on k=0, k=1 (K stays 3/98 but κ_c, κ_s wrong) | KC-D1 |
| 3 | `mutant_rolechspec_direct` | returns the direct Campaign A carrier instead of the graph chart | RoleChSpec changes under gauge (not invariant) — CL-D1 fails | KC-D2 |
| 4 | `mutant_gauge_false_negative` | declares every pair gauge-not-equivalent | the true gauge pair `n3_gauge_pair_keystone` is EQUIVALENT — mutant says NOT | KC (gauge) |
| 5 | `mutant_gauge_false_positive` | declares every pair gauge-equivalent | the `n3_nongauge_pair` is NOT_EQUIVALENT — mutant says EQUIVALENT | KC (gauge) |
| 6 | `mutant_active_size_via_passive` | reports the passive-permutation orbit as the active role spectrum | hand-pin active size is 3; the passive orbit is 1 — they differ (passive ≠ active) | KC-D4 |
| 7 | `mutant_rechart_zero_divide` | divides by `g_k` without the zero check | on the singular fixture (`g_0=0`) it raises `ZeroDivisionError`; correct returns `ROLE_CHART_UNAVAILABLE` | KC-D6 |
| 8 | `mutant_normalize_float` | float sqrt / float division for normalization | correct refuses to emit a value for `Q(√q_chart)`; mutant emits a float, which the canonical encoder rejects with `TypeError` | KC-D7 / KC-D8 |

## Why these are not tautological

- The hand-pinned CL-D3 truth (mutants 1, 2) is **independently derived** (rechart formulas + Campaign A verified carrier) and frozen as literal constants; a lying rechart is measured against external truth, not itself.
- The gauge-solver mutants (4, 5) are caught by **constructed** fixtures: one is a literal gauge image (must be EQUIVALENT), the other a hand-pinned non-gauge pair (must be NOT_EQUIVALENT).
- The float mutant (8) is caught **structurally** — the canonical encoder refuses any float, so a float can never reach a graded artifact.
- The passive/active mutant (6) is caught because RoleChSpec genuinely separates the three output roles (size 3) while the passive orbit is trivial (size 1) — the two are not the same object.
