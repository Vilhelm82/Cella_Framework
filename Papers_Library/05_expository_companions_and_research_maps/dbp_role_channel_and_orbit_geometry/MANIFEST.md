# Manifest — DBP 2-Primary Involution Campaign

**Final classification:** `THESIS_CONFIRMED_LOCAL_ONLY`
**Records:** 102 graded claims, all `COMPUTER_VERIFIED`; two runs content-byte-stable.
**Discipline:** exact arithmetic only (no float in any graded verdict); independent
Murnaghan–Nakayama referee; non-tautology proved by `mutation_check.py` (4/4 mutations caught).

## Engine / referee (`evals/dbp_involution/`)

| File | Role |
|---|---|
| `rep_utils.py` | **Referee** — independent S_n rep theory (M–N on beta-sets, character inner products, integral `std_n`). Self-test: `python3 rep_utils.py`. |
| `dbp_carrier.py` | **Engine under test** — `L_int`/`L_flag` carriers, gauge, conjugation action, `q⊗q` lift, projectors, std⊗std split, explicit mod-p linear algebra. Derived from CALC-14; nothing lifted from the parallel `dbp_prime2_structure` campaign. |
| `harness.py` | verdict vocabulary + records/JSON plumbing |
| `stage0_regression.py` | P0.1–P0.3 banked-gate reproduction (STOP gates) |
| `stageA_sym_wedge_split.py` | P-A1–P-A3 Sym/∧ split; carrier = symmetric half |
| `stageB_O_parity_vs_tau.py` | P-B1–P-B3 O-parity vs tensor-swap (needs `PYTHONPATH=src`) |
| `stageC_integral_snf.py` | P-C1–P-C3 integral torsion / Smith normal form |
| `stageD_char2_rolechspec.py` | P-D1–P-D3 char-2 faithfulness, all n (needs `PYTHONPATH=src`) |
| `stageE_monodromy_alt_probe.py` | P-E1–P-E4 monodromy alternating-carrier hunt |
| `run_all.py` | driver → `records.jsonl`, `prediction_verdicts.json` |
| `mutation_check.py` | non-tautology proof (a lying engine/referee must be caught) |

## Results (`results/dbp_involution/`)

| File | Contents |
|---|---|
| `prereg.md` | pre-registered thesis, discipline, predictions, gates |
| `records.jsonl` | 102 graded records (one JSON object per claim) |
| `prediction_verdicts.json` | per-stage verdicts + final classification |
| `report.md` | full synthesis (executive verdict, stage table, the 5 thesis questions, final sentence) |
| `sha256.txt` | checksums of the files above + the eval scripts |

> Not part of this campaign: `results/dbp_involution/dbp_prime2_structure/` is the **separate,
> parallel** `dbp_prime2_structure` campaign's output (left untouched; excluded from this manifest
> and sha256).

## Reproduce

```
cd evals/dbp_involution
python3 rep_utils.py                                   # referee self-test (all pass)
python3 run_all.py                                     # full campaign
PYTHONPATH=../../src python3 mutation_check.py         # non-tautology proof
```

## Stage verdicts

| Stage | Verdict |
|---|---|
| 0 | ALL_GATES_PASS |
| A | carrier_is_symmetric_half |
| B | O_parity_not_tau |
| C | integral_split_confirmed |
| D | char2_phantom_generalizes (linear core all-n; nonlinear n=3; all-n nonlinear OPEN) |
| E | no_canonical_comparison_map |

**Nothing canonical until Will signs off.**
