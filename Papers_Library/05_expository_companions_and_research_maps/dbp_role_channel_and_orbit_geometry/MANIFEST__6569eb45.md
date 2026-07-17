# MANIFEST — Campaign E: RoleChSpec Survival/Collapse Grammar

**Campaign id:** `rolechspec_survival_grammar_campaign_e`
**Tier:** eval-tier only. No substrate promotion. Successor to Campaign D; explains the D split structurally within the same frozen bound.
**Discipline:** exact `fractions.Fraction`; stdlib only; no float in any graded path; canonical `{"num": n, "den": d}` (no `frac:n/d` in canonical artifacts); deterministic, two-run byte-identical (verified).

## Pre-registration
- [`PREREG.md`](PREREG.md) — recorded before any generated artifact. Fixes the question, the fixed inputs (3381/1917), the non-tautology discipline (forbidden predictor fields; `n_direct_carriers` excluded from mining), the rule class, and the held-out protocol.

## Code (eval-tier package)
`src/lloyd_v4/evals/rolechspec_survival_grammar/`

| module | role |
|---|---|
| `features.py` | separation-class substrate + per-class **structural** feature record. Architecturally barred from importing the RoleChSpec / gauge engine or the target labels (KC-E2). |
| `labels.py` | per-class survival/collapse label from Campaign D RoleChSpec (TARGET source). |
| `rule_miner.py` | deterministic apriori-style minimal pure-rule miner (bitset support; no ML / float / randomness). |
| `rule_eval.py` | rule support / violations + leave-one-g-out held-out validation. |
| `mutants.py` | 8 deliberately-wrong variants (§12). |
| `serialize.py` | re-exports Campaign A canonical `{num,den}` serializer. |
| `run_campaign_e.py` / `verify_campaign_e.py` | deterministic build, grading, byte-identity check. |

Reuses Campaign A (`channel_spectrum_carrier`) and Campaign D (`active_role_channel_carrier`).
*Deviation note:* the recommended `fixtures.py` was unnecessary — the campaign operates on the full frozen enumeration; sanity is covered by synthetic miner tests + small-range feature/label tests.

## Tests
`tests/test_rolechspec_survival_grammar_*.py` — labels, features (incl. non-leakage source scan), miner (synthetic), mutants. **39 tests, all pass.**

## Artifacts (this directory)
`records.jsonl` (5298 per-class records), `summary.json` (CL-E1…E6 grading + rule ledger), `sha256.txt`, and the reports `CLAIM_LEDGER.md`, `SURVIVAL_GRAMMAR.md`, `RULE_LEDGER.md`, `FAMILY_REPORT.md`, `FEATURE_SCHEMA.md`, `MUTATION_REPORT.md`.

## Reproduce
```bash
python -m lloyd_v4.evals.rolechspec_survival_grammar.run_campaign_e \
    --out results/rolechspec_survival_grammar/campaign_e
python -m lloyd_v4.evals.rolechspec_survival_grammar.verify_campaign_e \
    --dir results/rolechspec_survival_grammar/campaign_e
```
The runner takes ~65s (per-class RoleChSpec labelling over the full frozen bound). Two runs are byte-identical.

## Result (headline)
CL-E1…E6 all PASS; no kill fired. The Campaign D split (3381 survive / 1917 collapse) is reproduced exactly and explained by a deterministic, held-out-validated structural grammar: **diagonal-support diversity + full rank predicts survival; structural uniformity predicts collapse.**
