# CLAIM LEDGER — Campaign D: Active Role-Channel Carrier

Eval-tier. Graded by `run_campaign_d.py`, re-checked by `verify_campaign_d.py`. Machine-readable mirror: `summary.json → claims`. Nothing here is canonical until Will signs off.

Status vocabulary: **PASS** / **FAIL** / **SCOPED_NO_WITNESS** / **PASS_WITH_WITNESS**.

| Claim | Statement | Verdict | Evidence |
|---|---|---|---|
| **CL-D1** | active graph recharting is exact and gauge-invariant | **PASS** | for all keystone gauges (and both gauge-pair fixtures): RoleChSpec invariant, direct Campaign A carrier *changes*, reduced K preserved; gauge-pair KC-D5 cross-check holds |
| **CL-D2** | active role charts preserve reduced Gaussian curvature | **PASS** | reduced K agrees across all solvable output roles for every fixture (e.g. hand-pin K = 3/98 for Product, Directive, Substrate) |
| **CL-D3** | active role-channel spectrum is nontrivial | **PASS** | hand-pinned fixture reproduced exactly: same K = 3/98 across roles, different channels (κ_c = -1/4, -1/784, -1/1764), κ_int = 0; values independently verified before pinning |
| **CL-D4** | passive permutation is not active recharting | **PASS** | hand-pin fixture: active role carrier size = 3 (> 1); passive direct-fingerprint orbit size = 1 |
| **CL-D5** | Campaign A separations gauge-classified | **PASS_WITH_WITNESS** | frozen A bound: 5298 candidate pairs; 3057 gauge-equivalent, 2241 not; 0 not-comparable; **3381 surviving role-channel separation groups**; classification complete, no KC-D5 violation |
| **CL-D6** | singular output roles are typed strata | **PASS** | fixture g=(0,1,1): role 0 `ROLE_CHART_UNAVAILABLE`, roles 1,2 available; no ZeroDivisionError / nan / inf / float |

## Kill conditions — all armed, all silent on truth, all proven to fire on mutants

| Kill | Fires when | Status | Mutant that fires it |
|---|---|---|---|
| KC-D1 | rechart fails CL-D3 | silent | `mutant_rechart_missing_Hkk`, `mutant_rechart_wrong_sign` |
| KC-D2 | RoleChSpec changes under gauge | silent | `mutant_rolechspec_direct` |
| KC-D3 | reduced K differs across roles | silent | (held on all fixtures) |
| KC-D4 | passive reported as active | silent | `mutant_active_size_via_passive` |
| KC-D5 | gauge-equivalent jets differ in RoleChSpec | silent | (empirically 3057 = 3057; gauge-pair fixtures) |
| KC-D6 | zero role denominator raises / nan / inf | silent | `mutant_rechart_zero_divide` |
| KC-D7 | any float in a canonical artifact | silent | `mutant_normalize_float` (encoder refuses) |
| KC-D8 | odd-order normalized rational when q_chart not square | silent | parity gate; `mutant_normalize_float` |
| KC-D9 | same-g candidate left undecided without typed reason | silent | gauge-solver false-pos/neg mutants; 0 not-comparable, 0 undecided this run |

**Kills fired this run: NONE.** Mutation controls (`tests/test_active_role_mutants.py`, 8 mutants) prove each check is non-tautological — see `MUTATION_REPORT.md`.

## Discipline
Exact ℚ, no tolerance; stdlib only; reuses Campaign A's exact-Q serialization unchanged; eval-tier only; no substrate package modified; two runs byte-identical (verified). **PENDING Will's sign-off.**
