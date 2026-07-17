# MANIFEST — Campaign G: RoleChSpec Gauge-Obstruction Faithfulness

**Campaign id:** `campaign_g_rolechspec_gauge_obstruction_faithfulness`
**Tier:** eval-tier only. No substrate promotion. Does not change Campaign A/D/E/F artifacts. **Campaign type: adversarial theorem test.**
**Discipline:** exact `fractions.Fraction`; stdlib only; no float / no NumPy / no tolerance in any verdict path; canonical `{"num": n, "den": d}`; deterministic, two-run byte-identical (verified).

## Pre-registration
- [`PREREG.md`](PREREG.md) — recorded before any generated report. States the theorem T-G, the two counterexample types, the pre-check result (0 failures over 46 875 jets / 8 584 RoleChSpec buckets), and the registered expectation (Outcome A).

## Code (eval-tier package)
`src/lloyd_v4/evals/rolechspec_gauge_obstruction_faithfulness/`

| module | role |
|---|---|
| `exact_linear.py` | rank / RREF / vec_sym over Q (code-disjoint from Campaign F) |
| `gauge_map.py` | `G_g(a) = g a^T + a g^T`, gauge basis, `gauge_image_rank`, `in_gauge_image` |
| `obstruction.py` | `O_ij` two independent ways (closed formula + `ΔH − G_g(a)` residual) |
| `rolechspec_local.py` | RoleChSpec **recomputed** (Campaign D engine, not cached labels) + regularity typing |
| `sample_spaces.py` | 6 attack gradients, Hessian sweeps, edge-topology + degenerate-channel families |
| `self_glue_families.py` | exact local jets of `D^m + D^k S + P^p − 3` |
| `pair_search.py` | faithfulness sweep, gauge-positive controls, targeted mutations, F retrodiction |
| `run_campaign_g.py` | deterministic build, grading (CL-G1…G8), byte-stable emit, verify |
| `mutants.py` | 10 deliberately-wrong variants (§10) |

Reuses A/D/F (RoleChSpec recomputation, separation classes for retrodiction). The obstruction is implemented **independently** of Campaign F as an adversarial cross-check; CL-G2 confirms both agree.

## Tests
`tests/test_campaign_g_*.py` — exact_linear, obstruction_formula, rolechspec_gauge_invariance, faithfulness_search, self_glue_structured, non_tautology, mutants, byte_stability. **Fast suite passes; slow full-build + CL-G2 retrodiction pass under `-m ""`.**

## Artifacts (this directory)
`records.jsonl` (per-stage + any counterexample records — 0 here), `summary.json` (CL-G1…G8 + sweeps + retrodiction), `sha256.txt`, and the reports `FAITHFULNESS_SEARCH_REPORT.md`, `GAUGE_INVARIANCE_REPORT.md`, `EXCEPTIONAL_LOCUS_REPORT.md`, `SELF_GLUE_STRESS_REPORT.md`, `MUTATION_REPORT.md`, `CLAIM_LEDGER.md`.

## Reproduce
```bash
python -m lloyd_v4.evals.rolechspec_gauge_obstruction_faithfulness.run_campaign_g \
    --out results/rolechspec_gauge_obstruction_faithfulness
```
~73s (deep sweep + 6-gradient broad sweep + F retrodiction + targeted + self-glue). `run_campaign_g.verify(dir)` rebuilds and checks byte-identity.

## Result (headline)
Status **PASS**, no kill fired, **Outcome A**. 0 faithfulness counterexamples, 0 gauge-invariance counterexamples. Every RoleChSpec bucket is exactly one same-gradient gauge orbit (max obstruction rank in any bucket = 0). The RoleChSpec Gauge-Obstruction Theorem survives the exact-Q adversarial sweep — **finite-tested, not globally proven.**
