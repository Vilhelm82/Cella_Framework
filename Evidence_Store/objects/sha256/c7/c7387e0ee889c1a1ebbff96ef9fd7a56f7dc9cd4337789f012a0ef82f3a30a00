# MANIFEST — Campaign A: Channel-Spectrum Carrier Atlas

**Campaign id:** `channel_spectrum_carrier_campaign_a`
**Tier:** eval-tier only. No substrate package is modified; nothing here is canonical until Will signs off.
**Discipline:** exact `fractions.Fraction` throughout; stdlib only (`fractions`, `json`, `hashlib`, `itertools`); no NumPy/SymPy/mpmath/Sage; no float tolerances in any graded path.

## Amendments
- [`PREREG_AMENDMENT_001.md`](PREREG_AMENDMENT_001.md) — schema/fixture hardening (canonical `{num,den}` serialization; hand-pinned keystone truth; named channel fields; v2-not-overwrite). Recorded **before** any canonical output file was emitted; does **not** alter the mathematical claims CL-A1 … CL-A6.

## Code (eval-tier package)
`src/lloyd_v4/evals/channel_spectrum_carrier/`

| module | role |
|---|---|
| `rational.py` | exact-Q discipline: float-refusing coercion, `q_of`, perfect-square / `sqrt_if_square` (parity) |
| `determinants.py` | fraction-free Bareiss `det_exact`, bordered builder, `split_hessian`, restriction, `rank_exact` |
| `carrier.py` | `channel_density`, `channel_vector` (Vandermonde), `density_carrier`, `density_fingerprint`, `reduced_density_tower`, `fingerprint_polynomial` |
| `classify.py` | sign/support/sign-patterns, Hessian coupling graph + family, strata |
| `actions.py` | `passive_permute` (CL-A2), `gauge_H` (CL-A3), `action_kind` (KC-A7) |
| `serialize.py` | canonical `{num,den}` encoder, byte-stable records, parity-safe `normalize_coefficient` (CL-A4) |
| `fixtures.py` | hand-curated n=3 / n=4 catalogue (keystone carries hand-pinned literal truth) |
| `separation.py` | bounded reproducible separation search (CL-A5) + interaction-order split (CL-A6) |
| `mutants.py` | 7 deliberately-wrong variants for mutation controls (§10) |
| `run_campaign_a.py` | deterministic `build_campaign`, grading, byte-stable emit |
| `verify_campaign_a.py` | rebuild + byte-identity + sha + re-grade |

## Tests
`tests/test_channel_spectrum_carrier_*.py` — density, reduction, passive, gauge, fixtures, separation, serialization, mutants. **164 tests, all pass** (`PYTHONPATH=src pytest -q tests/test_channel_spectrum_carrier_*.py`).

## Artifacts (this directory)
| file | content |
|---|---|
| `records.jsonl` | one record per fixture (19 fixtures); canonical `{num,den}` |
| `summary.json` | CL-A1 … CL-A6 grading, separation + split summaries |
| `sha256.txt` | sha256 of `records.jsonl` and `summary.json` |
| `CLAIM_LEDGER.md` | claim grading with evidence |
| `FIXTURES.md` | fixture catalogue |
| `ATLAS_SUMMARY.md` | what was found / not found / open |
| `SEPARATION_REPORT.md` | CL-A5 / CL-A6 search results, honest bounds |
| `MUTATION_REPORT.md` | the 7 mutants and how each is caught |

## Reproduce
```bash
python -m lloyd_v4.evals.channel_spectrum_carrier.run_campaign_a \
    --out results/channel_spectrum_carrier/campaign_a
python -m lloyd_v4.evals.channel_spectrum_carrier.verify_campaign_a \
    --dir results/channel_spectrum_carrier/campaign_a
```
Two runs produce byte-identical `records.jsonl` and `summary.json` (verified).

## Predating-files disclosure
No canonical output file predates `PREREG_AMENDMENT_001`. All artifacts in this directory are first-generation (`v1`) under the amended schema.
