# PREREG — Campaign E: RoleChSpec Survival/Collapse Grammar

**Status:** pre-registration, recorded **before** any generated artifact.
**Tier:** eval-tier only. No substrate promotion. Successor to Campaign D. Does not change the Campaign D result; explains it structurally within the same frozen bound.
**Discipline:** exact `fractions.Fraction`; stdlib only; no float in any graded path; canonical `{"num": n, "den": d}` (no `frac:n/d` in canonical artifacts); deterministic, two-run byte-identical.

## Question

> Given the Campaign A separation classes and Campaign D quotient labels, which **structural** features predict whether a class survives RoleChSpec quotienting or collapses as defining-function gauge residue?

## Fixed inputs (reproduced as an integrity gate, not re-argued)

```
Campaign A separation groups : 5298
Campaign D surviving groups  : 3381
Campaign D collapsed groups  : 1917
```
A class **SURVIVES_ROLECHSPEC** iff its distinct-direct-carrier representatives yield ≥ 2 distinct RoleChSpec fingerprints; else **COLLAPSES_GAUGE_RESIDUAL**. (CL-E1 halts the campaign if 3381 / 1917 / 0 do not reproduce exactly.)

## Frozen bound

g ∈ {(1,1,1), (1,2,3), (2,-1,1)}; symmetric Hessian entries in {-2,-1,0,1,2}; zero Hessian skipped. (Identical to Campaign A/D.)

## Non-tautology discipline

**Target-only / forbidden as predictors** (KC-E2, KC-E9): RoleChSpec equality, RoleChSpec fingerprint, gauge-solver verdict, survival/collapse label, direct-carrier fingerprint, candidate-id ordering, summary verdict fields.

**`n_direct_carriers` is class metadata, NOT a rule-mining predictor.** It counts distinct direct-carrier fingerprints, which §7 marks debug-only; to stay strictly within the declared structural feature schema and clear of any tautology, the rule miner does **not** use it. (It empirically predicts survival well, but is reported only as a debug/metadata observation, never as a confirmed structural rule.)

**Predictor-allowed structural features** (§7): Hessian rank / rank_drop / trace, diagonal & off-diagonal support masks and their per-class set sizes, sign and zero patterns, coupling-graph family / edges / edge-count, channel zero/sign patterns (r=1,2 from the direct carrier), scalar-flat flags, channel-cancellation flags, reduced-tower zero flags, regularity strata, and class-level aggregates over these.

## Rule class (deterministic, exact — no ML, no float, no randomness)

Conjunctions of 1–3 (optionally 4) predicates of the forms: `feature == / != value`, `contains`, `subset-of` / `intersects` a finite set, `int <= / >= const`, `bool is true/false`. A **confirmed** rule has support ≥ 10 and violations == 0 (pure) inside the bound, and uses no forbidden field. Only **minimal** rules are reported (no proper sub-conjunction is also pure). High-support **mixed** families are reported honestly with counterexamples.

## Held-out validation

Leave-one-g-out over g1=(1,1,1), g2=(1,2,3), g3=(2,-1,1): for each confirmed rule, train on two g-values and require zero violations on the held-out g-slice → `RULE_VALIDATED_HELDOUT`, else `RULE_TRAIN_ONLY`.

## Claims

- **CL-E1** Campaign D labels reproduced exactly (3381 / 1917 / 0, total 5298).
- **CL-E2** every class gets a deterministic structural feature record; 5298 records; byte-identical across runs.
- **CL-E3** ≥ 1 non-tautological structural rule with support ≥ 10, violations == 0 (else `SCOPED_NO_RULE`, honestly).
- **CL-E4** large impure families reported as mixed with counterexamples (≥ top-10 high-support rejected/mixed).
- **CL-E5** every confirmed rule labelled held-out-validated or train-only.
- **CL-E6** mutation controls catch all deliberately-wrong variants.

## Kill conditions (armed)

KC-E1 D counts fail to reproduce · KC-E2 feature builder reads forbidden fields · KC-E3 confirmed rule has a violation · KC-E4 held-out-validated rule fails a held-out slice · KC-E5 float in a machine artifact · KC-E6 two runs differ byte-for-byte · KC-E7 a class dropped without typed reason · KC-E8 below-threshold rule reported confirmed · KC-E9 tautological predicate reported as structural · KC-E10 mutants not caught.

## Non-goals
n ≥ 4 theory; branch monodromy; fourth-role/S4; substrate promotion; cross-gradient gauge equivalence; full role-equivalence quotient; symbolic theorems beyond the finite-bound rules. The deliverable is a structural grammar inside the frozen bound, with explicit unresolved families.
