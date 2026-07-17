# MANIFEST — Campaign F: RoleChSpec Diversity Mechanism

**Campaign id:** `campaign_f_rolechspec_diversity_mechanism`
**Tier:** eval-tier only. No substrate promotion. Does not change Campaign A/D/E artifacts. Successor to Campaign E.
**Discipline:** exact `fractions.Fraction`; stdlib only; no float in any graded path; canonical `{"num": n, "den": d}`; deterministic, two-run byte-identical (verified).

## Pre-registration
- [`PREREG.md`](PREREG.md) — recorded before any generated report. States the hypothesis, the exact obstruction formula, the two-lane non-tautology rule, and the verified expectations (H-F3 PASS_STRONG; H-F5 size-6 exception).

## Code (eval-tier package)
`src/lloyd_v4/evals/rolechspec_diversity_mechanism/`

| module | role |
|---|---|
| `exact_linear.py` | exact rank over Q (no float, no NumPy) |
| `gauge_obstruction.py` | **Lane 2** — the obstruction `O_ij`, `obstruction_rank` (base + pairwise), `gauge_image_rank`, obstruction patterns. Analytic from `(g,H)`; imports no RoleChSpec/gauge-verdict |
| `features_structural.py` | **Lane 1** — Hessian structural features (`diag_support_set_size`, `diag_span_rank`, `hessian_span_rank`); imports no target engine / labels / Lane 2 |
| `load_records.py` | reconstruct classes + survival labels (OUTCOME source; reuses Campaign E enumeration + Campaign D RoleChSpec) |
| `mechanism_tables.py` | cross-tabs combining both lanes with the label as outcome |
| `theorem_candidates.py` | H-F3/F5 verdicts + Candidate Theorem F |
| `run_campaign_f.py` | deterministic build, grading (CL-F1…F8), byte-stable emit, verify |
| `mutants.py` | 9 deliberately-wrong variants (§9) |

Reuses Campaign A/D/E. *Lane separation is enforced by source-scan tests* (Lane 1 and Lane 2 import neither each other nor the RoleChSpec/gauge engine).

## Tests
`tests/test_campaign_f_*.py` — exact_linear, gauge_obstruction, integrity_counts, feature_reproduction, non_tautology, mechanism, mutants, byte_stability. **Fast suite passes; slow full-bound integrity/feature-reproduction tests pass under `-m ""`.**

## Artifacts (this directory)
`records.jsonl` (5298 per-class analysis records), `summary.json` (CL-F1…F8 + mechanism tables + theorem candidate), `sha256.txt`, and the reports `OBSTRUCTION_RANK_REPORT.md`, `DIVERSITY_MECHANISM_REPORT.md`, `THEOREM_CANDIDATES.md`, `COLLAPSE_LIMITATION_REPORT.md`, `MUTATION_REPORT.md`, `CLAIM_LEDGER.md`.

## Reproduce
```bash
python -m lloyd_v4.evals.rolechspec_diversity_mechanism.run_campaign_f \
    --out results/rolechspec_diversity_mechanism
```
~47s (per-class RoleChSpec labelling over the full frozen bound). `run_campaign_f.verify(dir)` rebuilds and checks byte-identity.

## Result (headline)
Status **PASS**, no kill fired. **Survival ⟺ obstruction_rank > 0, exactly, 0 exceptions** over all 5298 classes. `diag_support_set_size` is unmasked as a support-level proxy for a positive exact gauge-obstruction space (Candidate Theorem F: CONFIRMED_WITHIN_BOUND). CL-F6 is PARTIAL: the literal `diag ≥ 5` threshold is refuted by size 6, but the obstruction criterion confirms and explains the pure-survivor sizes.
