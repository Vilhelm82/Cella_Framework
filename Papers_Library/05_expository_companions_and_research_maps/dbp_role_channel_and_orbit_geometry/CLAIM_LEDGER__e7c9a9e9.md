# CLAIM LEDGER — Campaign E: RoleChSpec Survival/Collapse Grammar

Eval-tier. Graded by `run_campaign_e.py`, re-checked by `verify_campaign_e.py`. Machine-readable mirror: `summary.json → claims`. Nothing canonical until Will signs off.

| Claim | Statement | Verdict | Evidence |
|---|---|---|---|
| **CL-E1** | Campaign D labels reproduced exactly | **PASS** | 3381 survive / 1917 collapse / 0 undecided / 5298 total — exact |
| **CL-E2** | deterministic structural feature record per class, no forbidden field | **PASS** | 5298 feature records; `assert_no_forbidden` enforced in `class_features`; byte-identical across runs |
| **CL-E3** | non-tautological structural rule, support ≥ 10, violations == 0 | **PASS** | 2563 confirmed minimal rules; top `E-RULE-0001` support 273; predictors are §7 Hessian-structural only (`n_direct_carriers` excluded) |
| **CL-E4** | large impure families reported as mixed with counterexamples | **PASS** | 25 mixed families reported (e.g. `reduced_tower_is_zero is_false`: S=3381, C=1915) |
| **CL-E5** | every confirmed rule labelled held-out-validated or train-only | **PASS** | leave-one-g-out: 1759 validated, 804 train-only, 0 rejected |
| **CL-E6** | mutation controls catch all deliberately-wrong variants | **PASS** | 8 mutants in `mutants.py`, proven caught by the mutation test suite |

## Kill conditions — all armed, none fired

| Kill | Fires when | Status |
|---|---|---|
| KC-E1 | D counts fail to reproduce | silent (3381/1917/0 exact) |
| KC-E2 | feature builder reads forbidden fields | silent (features.py imports no target engine; `assert_no_forbidden` guards) |
| KC-E3 | confirmed rule has a violation | silent (miner confirms only pure rules) |
| KC-E4 | held-out-validated rule fails a held-out slice | silent (re-evaluated exactly) |
| KC-E5 | float in a machine artifact | silent (canonical encoder refuses float) |
| KC-E6 | two runs differ byte-for-byte | silent (verified identical) |
| KC-E7 | a class dropped without typed reason | silent (5298 classes, count-gated) |
| KC-E8 | below-threshold rule reported confirmed | silent (min_support 10 enforced) |
| KC-E9 | tautological predicate reported as structural | silent (forbidden-field check per rule passes) |
| KC-E10 | mutants not caught | silent (all 8 caught) |

**Kills fired this run: NONE.** See `MUTATION_REPORT.md` for the non-tautology proofs.

## Discipline
Exact ℚ, no tolerance; stdlib only; no ML / fitted floats / randomness; predictor features strictly §7 Hessian-structural (target labels, RoleChSpec, gauge verdicts, and `n_direct_carriers` excluded from mining); eval-tier only; no substrate modified; two runs byte-identical. **PENDING Will's sign-off.**
