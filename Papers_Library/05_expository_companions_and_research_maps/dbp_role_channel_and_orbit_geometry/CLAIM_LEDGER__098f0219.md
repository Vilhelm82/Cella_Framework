# CLAIM LEDGER — Campaign G: RoleChSpec Gauge-Obstruction Faithfulness

Eval-tier adversarial theorem test. Graded by `run_campaign_g.py`; byte-stability checked by `run_campaign_g.verify`. Machine-readable mirror: `summary.json → claims`. Nothing canonical until Will signs off.

| Claim | Statement | Verdict | Evidence |
|---|---|---|---|
| **CL-G1** | gauge-obstruction formula `ker(O_g) = Im(G_g)` | **PASS** | two independent computations agree; gauge diffs → O=0; mutations → O≠0; `gauge_image_rank=3` for all 6 g |
| **CL-G2** | Campaign F retrodiction | **PASS** | G's own obstruction reproduces F: obstruction_rank 0→[0,1917], 1→[2549,0], 2→[832,0] |
| **CL-G3** | gauge invariance: `O=0 ⟹ RoleChSpec equal` | **PASS** | 0 Type-B counterexamples across 6 g × bases × gauges (Outcome C did not occur) |
| **CL-G4** | faithfulness attack: search `O≠0 ∧ RoleChSpec equal` | **PASS** | **0 Type-A counterexamples**; 19 999 regular jets bucket-by-RoleChSpec (max obstruction rank in any bucket = 0) + 751 targeted pairs; + 46 875-jet pre-check |
| **CL-G5** | exceptional-locus typing | **PASS** | REGULAR / ROLE_CHART_UNAVAILABLE / SINGULAR_GRADIENT / OUT_OF_SCOPE; no raw exceptions |
| **CL-G6** | self-glue structured stress | **PASS** | 25 structured jets from `D^m + D^k S + P^p − 3`; 0 counterexamples on regular jets |
| **CL-G7** | non-tautology | **PASS** | RoleChSpec recomputed (no cached labels); equality path label-free and float-free (source-scan tests) |
| **CL-G8** | mutation controls | **PASS** | 10 mutants all caught |

## Kill conditions — all armed, none fired

| Kill | Fires when | Status |
|---|---|---|
| K-G1 | obstruction formula broken (`O=0` but ΔH∉Im, or reverse) | silent |
| K-G2 | gauge invariance broken (`O=0`, RoleChSpec differ) | silent (0 Type-B) |
| K-G3 | faithfulness broken (`O≠0`, RoleChSpec equal) | silent (0 Type-A) |
| K-G4 | raw singular crash | silent (typed strata) |
| K-G5 | float / tolerance leakage | silent (exact Q everywhere) |
| K-G6 | cached-label leakage | silent (RoleChSpec recomputed) |

**Kills fired: NONE.** Status **PASS**, outcome **A — theorem survives the adversarial sweep**.

## Outcome (acceptance §14)

**Outcome A.** No exact-Q counterexample found. The RoleChSpec Gauge-Obstruction Theorem (T-G) survives across exhaustive small rational sweeps, targeted obstruction mutations, gauge-positive controls, and structured self-glue families.

> RoleChSpec is a **faithful invariant of `Sym_3(Q)/Im(G_g)` on the regular active-role locus** — finite-tested, **not globally proven**. The remaining work is a proof of the converse outside the finite sweep.

## Discipline
Exact ℚ, no float/tolerance in any decision; RoleChSpec recomputed (no cached labels) — the two computations of the obstruction are code-disjoint cross-checks; eval-tier only; no substrate modified; two runs byte-identical. **PENDING Will's sign-off.**
