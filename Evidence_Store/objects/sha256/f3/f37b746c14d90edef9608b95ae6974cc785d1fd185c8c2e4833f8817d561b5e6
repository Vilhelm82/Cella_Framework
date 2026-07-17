# Dual Q-Source Companion Gap Search

Accepted outcome: `dual_q_source_gap_reduced_hard_cell`
Headline classification: `dual_q_source_gap_reduced_hard_cell`

## Test Design

This campaign keeps the split-constant `c=1/2` form and tests whether a companion q source can cover only the primary direct-q failure cells.

```text
F_direct = (R * R - 1/2) + (q_direct - 1/2)
F_route  = (R * R - 1/2) + (q_route  - 1/2)
```

The handoff rule is diagnostic: use the companion only inside direct-q non-half cells.

## Required Findings

1. Gap resolved: `False`.
2. Gap reduced to hard cell: `True`.
3. Best companion: `sqrt_ratio_squared`.
4. Primary support/mask: `f_binade_-1` with `16` half reads.
5. Primary gap indices: `[113, 117, 121, 135]`.
6. Covered gap indices: `[113, 117, 135]`.
7. Hard gap indices: `[121]`.
8. Union half count/fraction: `19` / `0.95`.
9. SR/pure controls promoted: `False` / `False`.
10. Double precision language justified: `False`.

## Fixture Findings

- `schwarzschild` (primary): outcome `dual_q_source_gap_reduced_hard_cell`; best `sqrt_ratio_squared` covers `[113, 117, 135]` with union `19` / `20`.
- `sr` (secondary): outcome `dual_q_source_no_improvement`; best `pow_square` covers `[]` with union `44` / `70`.
- `pure_affine_control` (affine_control): outcome `dual_q_source_no_improvement`; best `sqrt_roundtrip` covers `[1, 3, 4, 7, 12, 29, 32, 40, 56, 61]` with union `32` / `42`.

## Interpretation

The companion source reduces the split-constant gap from four cells to one hard cell. `sqrt_ratio_squared` and `cbrt_ratio_cubed` both cover indices `113`, `117`, and `135`; index `121` remains unresolved across the tested q sources.

This is a stronger result than the single-form split candidate: the union read reaches `19 / 20 = 0.95` on Schwarzschild `f_binade_-1`. It is still not a complete doubled read because one hard cell remains and the handoff is diagnostic, not yet an architecture rule.

## Verification

- `PYTHONPATH=src python -m lloyd_v4.evals.dual_q_source_companion_gap_search`
  Result: passed; generated artifact_dual_q_source_companion_gap_search.json and dual_q_source_companion_gap_search_report.md.
- `PYTHONPATH=src python -m pytest tests/test_dual_q_source_companion_gap_search.py -q`
  Result: passed; focused dual-q companion tests.
- `PYTHONPATH=src python -m pytest tests/test_dual_q_source_companion_gap_search.py tests/test_split_constant_integer_cell_diagnostic.py tests/test_split_constant_half_grid_form_search.py -q`
  Result: passed; focused compatibility subset.

## Artifacts

- `Build_Docs/Reports/dual_q_source_companion_gap_search/artifact_dual_q_source_companion_gap_search.json`
- `Build_Docs/Reports/dual_q_source_companion_gap_search/dual_q_source_companion_gap_search_report.md`
