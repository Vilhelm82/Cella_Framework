# root-closure-atlas — ATLAS index (Stage 0 baseline map)

Append-only master palette: fixture × instrument × facet.
Stage-0 records: `stage_0/records/atlas_stage0.jsonl` (260 rows,
sha256 `ac3ab40dea296b569d2dbcb2558cc5fa4e5a7e49b7b6f11c669206cd8c933499`,
byte-stable ×2 incl. 128 live oracle calls).

## Classical baseline map (verdict_vs_certified_cell tallies)

| FX class | instrument | n | inside | outside_k | missed | ghost_accepted | na |
|---|---|---|---|---|---|---|---|
| FX-A | I1a_bisection | 2 | 0 | 2 | 0 | 0 | 0 |
| FX-A | I1b_newton | 3 | 2 | 1 | 0 | 0 | 0 |
| FX-A | I1c_halley | 3 | 2 | 1 | 0 | 0 | 0 |
| FX-A | I1d_secant | 3 | 2 | 1 | 0 | 0 | 0 |
| FX-A | I2_multi_start | 2 | 2 | 0 | 0 | 0 | 0 |
| FX-A | I2_solve_defaults | 2 | 2 | 0 | 0 | 0 | 0 |
| FX-B | I1a_bisection | 4 | 1 | 1 | 0 | 0 | 2 |
| FX-B | I1b_newton | 5 | 0 | 0 | 4 | 1 | 0 |
| FX-B | I1c_halley | 5 | 0 | 0 | 4 | 1 | 0 |
| FX-B | I1d_secant | 5 | 0 | 0 | 4 | 1 | 0 |
| FX-B | I2_multi_start | 4 | 0 | 0 | 3 | 1 | 0 |
| FX-B | I2_solve_defaults | 4 | 0 | 0 | 3 | 1 | 0 |
| FX-C | I1a_bisection | 7 | 4 | 2 | 0 | 0 | 1 |
| FX-C | I1b_newton | 10 | 4 | 0 | 3 | 0 | 3 |
| FX-C | I1c_halley | 10 | 4 | 0 | 5 | 0 | 1 |
| FX-C | I1d_secant | 10 | 5 | 0 | 5 | 0 | 0 |
| FX-C | I2_multi_start | 7 | 5 | 0 | 2 | 0 | 0 |
| FX-C | I2_solve_defaults | 7 | 6 | 1 | 0 | 0 | 0 |
| FX-D | I1a_bisection | 2 | 2 | 0 | 0 | 0 | 0 |
| FX-D | I1b_newton | 2 | 1 | 1 | 0 | 0 | 0 |
| FX-D | I1c_halley | 2 | 2 | 0 | 0 | 0 | 0 |
| FX-D | I1d_secant | 2 | 2 | 0 | 0 | 0 | 0 |
| FX-D | I2_multi_start | 2 | 1 | 1 | 0 | 0 | 0 |
| FX-D | I2_solve_defaults | 2 | 2 | 0 | 0 | 0 | 0 |
| FX-E | I1a_bisection | 2 | 0 | 0 | 0 | 0 | 2 |
| FX-E | I1b_newton | 3 | 0 | 0 | 0 | 1 | 2 |
| FX-E | I1c_halley | 3 | 0 | 0 | 0 | 2 | 1 |
| FX-E | I1d_secant | 3 | 0 | 0 | 0 | 3 | 0 |
| FX-E | I2_multi_start | 2 | 0 | 0 | 0 | 1 | 1 |
| FX-E | I2_solve_defaults | 2 | 0 | 0 | 0 | 1 | 1 |
| FX-F | I1a_bisection | 2 | 0 | 1 | 0 | 0 | 1 |
| FX-F | I1b_newton | 3 | 1 | 0 | 0 | 1 | 1 |
| FX-F | I1c_halley | 3 | 1 | 0 | 0 | 2 | 0 |
| FX-F | I1d_secant | 3 | 1 | 0 | 0 | 1 | 1 |
| FX-F | I2_multi_start | 2 | 1 | 0 | 0 | 1 | 0 |
| FX-F | I2_solve_defaults | 2 | 1 | 0 | 0 | 1 | 0 |
| FX-G | I1a_bisection | 2 | 1 | 0 | 0 | 0 | 1 |
| FX-G | I1b_newton | 3 | 2 | 0 | 1 | 0 | 0 |
| FX-G | I1c_halley | 3 | 0 | 0 | 1 | 0 | 2 |
| FX-G | I1d_secant | 3 | 2 | 0 | 1 | 0 | 0 |
| FX-G | I2_multi_start | 2 | 1 | 0 | 1 | 0 | 0 |
| FX-G | I2_solve_defaults | 2 | 1 | 0 | 1 | 0 | 0 |
| FX-H | I1a_bisection | 2 | 0 | 0 | 2 | 0 | 0 |
| FX-H | I1b_newton | 2 | 0 | 0 | 0 | 0 | 2 |
| FX-H | I1c_halley | 2 | 0 | 0 | 0 | 0 | 2 |
| FX-H | I1d_secant | 2 | 0 | 0 | 2 | 0 | 0 |
| FX-H | I2_multi_start | 2 | 0 | 0 | 0 | 0 | 2 |
| FX-H | I2_solve_defaults | 2 | 0 | 0 | 2 | 0 | 0 |
| FX-I | I1a_bisection | 2 | 1 | 1 | 0 | 0 | 0 |
| FX-I | I1b_newton | 6 | 0 | 1 | 3 | 0 | 2 |
| FX-I | I1c_halley | 6 | 4 | 0 | 2 | 0 | 0 |
| FX-I | I1d_secant | 6 | 0 | 2 | 4 | 0 | 0 |
| FX-I | I2_multi_start | 2 | 0 | 1 | 1 | 0 | 0 |
| FX-I | I2_solve_defaults | 2 | 1 | 0 | 1 | 0 | 0 |
| FX-J | I1a_bisection | 3 | 0 | 3 | 0 | 0 | 0 |
| FX-J | I1b_newton | 3 | 2 | 1 | 0 | 0 | 0 |
| FX-J | I1c_halley | 3 | 1 | 2 | 0 | 0 | 0 |
| FX-J | I1d_secant | 3 | 2 | 1 | 0 | 0 | 0 |
| FX-J | I2_multi_start | 3 | 2 | 1 | 0 | 0 | 0 |
| FX-J | I2_solve_defaults | 3 | 2 | 0 | 1 | 0 | 0 |
| FX-K | I1a_bisection | 4 | 1 | 3 | 0 | 0 | 0 |
| FX-K | I1b_newton | 4 | 3 | 1 | 0 | 0 | 0 |
| FX-K | I1c_halley | 4 | 3 | 1 | 0 | 0 | 0 |
| FX-K | I1d_secant | 4 | 1 | 3 | 0 | 0 | 0 |
| FX-K | I2_multi_start | 4 | 4 | 0 | 0 | 0 | 0 |
| FX-K | I2_solve_defaults | 4 | 4 | 0 | 0 | 0 | 0 |

## v3_status_bucket × fixture class (S3 collapse, queryable)

| FX class | bucket | n |
|---|---|---|
| FX-A | coordinate_localized | 2 |
| FX-A | residual_ok_coordinate_indeterminate | 2 |
| FX-B | residual_ok_coordinate_indeterminate | 8 |
| FX-C | residual_ok_coordinate_indeterminate | 14 |
| FX-D | coordinate_localized | 3 |
| FX-D | residual_ok_coordinate_indeterminate | 1 |
| FX-E | coordinate_localized | 2 |
| FX-E | residual_ok_coordinate_indeterminate | 2 |
| FX-F | coordinate_localized | 4 |
| FX-G | coordinate_localized | 2 |
| FX-G | residual_ok_coordinate_indeterminate | 2 |
| FX-H | coordinate_localized | 4 |
| FX-I | coordinate_localized | 2 |
| FX-I | residual_ok_coordinate_indeterminate | 2 |
| FX-J | coordinate_localized | 5 |
| FX-J | residual_ok_coordinate_indeterminate | 1 |
| FX-K | coordinate_localized | 5 |
| FX-K | residual_ok_coordinate_indeterminate | 3 |

*(Stage 0 changes no CL row; all advantage claims remain NOT_YET_PROBED — this map is the diff baseline for every later facet.)*
