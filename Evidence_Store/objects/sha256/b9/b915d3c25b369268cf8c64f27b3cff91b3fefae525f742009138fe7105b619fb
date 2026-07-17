# MANIFEST — Campaign D: Active Role-Channel Carrier

**Campaign id:** `active_role_channel_carrier_campaign_d`
**Tier:** eval-tier only. No substrate promotion. Successor to Campaign A.
**Discipline:** exact `fractions.Fraction`; stdlib only; no float in any graded path; canonical rational form `{"num": n, "den": d}` (no `frac:n/d` in canonical artifacts); two-run byte-identical outputs (verified).

## Pre-registration
- [`PREREG.md`](PREREG.md) — recorded **before** any generated artifact. Carries the independently-verified CL-D3 truth table and the role→chart map (Product=k2, Directive=k0, Substrate=k1).

## Code (eval-tier package)
`src/lloyd_v4/evals/active_role_channel_carrier/`

| module | role |
|---|---|
| `implicit_graph.py` | §2.2 active graph rechart; `graph_jet_to_implicit`; typed `ROLE_CHART_UNAVAILABLE` |
| `role_spec.py` | `RoleChSpec`: output-role carriers (named P/D/S), `rolechspec_fingerprint`, reduced-K-by-role, active size |
| `gauge_solver.py` | exact same-`g` gauge solver (EQUIVALENT/NOT/UNDECIDED/NOT_COMPARABLE) |
| `fixtures.py` | hand-pinned CL-D3 graph jet, keystone, scalar-flat (from A), singular, gauge / non-gauge pairs |
| `quotient_search.py` | CL-D5 classification of Campaign A separations under gauge + role recharting |
| `serialize.py` | re-exports Campaign A canonical `{num,den}` serializer (no duplication) |
| `mutants.py` | 8 deliberately-wrong variants (§6) |
| `run_campaign_d.py` / `verify_campaign_d.py` | deterministic build, grading, byte-identity check |

Reuses Campaign A (`channel_spectrum_carrier`): `rational`, `determinants`, `carrier`, `actions`, `serialize`.
*Deviation note:* the recommended `classify.py` was unnecessary — Campaign D classification lives in `role_spec` (role carriers + named channels) and `gauge_solver` (gauge classes).

## Tests
`tests/test_active_role_*.py` — graph_rechart, hand_pins, gauge_invariance, passive_not_active, gauge_solver, campaign_a_candidates, singular_strata, serialization, mutants. **48 tests, all pass.**

## Artifacts (this directory)
`records.jsonl` (jet records + gauge-pair records), `summary.json` (CL-D1…D6 grading + quotient search), `sha256.txt`, and the reports `CLAIM_LEDGER.md`, `ACTIVE_ROLE_REPORT.md`, `GAUGE_QUOTIENT_REPORT.md`, `FIXTURES.md`, `MUTATION_REPORT.md`, `ATLAS_D_SUMMARY.md`.

## Reproduce
```bash
python -m lloyd_v4.evals.active_role_channel_carrier.run_campaign_d \
    --out results/active_role_channel_carrier/campaign_d
python -m lloyd_v4.evals.active_role_channel_carrier.verify_campaign_d \
    --dir results/active_role_channel_carrier/campaign_d
```
The runner takes ~45s (the CL-D5 quotient search scans the full frozen Campaign A bound). Two runs produce byte-identical `records.jsonl` and `summary.json`.

## Result (headline)
All of CL-D1 … CL-D6 PASS; **CL-D5 = PASS_WITH_WITNESS**; no kill fired. Of 5298 Campaign A separation classes, **3381 survive** the exact same-gradient gauge quotient + active role recharting. RoleChSpec is empirically the exact gauge invariant: gauge-equivalent ⟺ identical RoleChSpec (3057 = 3057; 2241 = 2241).
