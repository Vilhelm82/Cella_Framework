# Cubic Role-Branch Census

Surface: `F = x1^3 + x1*x2 + x3^2 - 3`.

## x1 Role Solve

- Slice: `x3 = 2`.
- Base frame: `beta = 0`, roots ordered by `(Re, Im)`.
- Finite branch permutations, CCW order: `[[1, 0, 2], [0, 2, 1], [2, 1, 0]]`.
- Finite cycle types: `[[2, 1], [2, 1], [2, 1]]`.
- Distinct transpositions in common frame: `True`.
- Large loop permutation: `[0, 2, 1]`.
- Hurwitz `m_big == CCW product`: `True`.
- Contractible loop identity: `True`.
- Strained non-enclosing loop identity: `True`.

### x1 Branch Strata

Rows are sorted by `lasso_order_index`, the `[0, 2*pi)` CCW order used by the lasso run.

| role | lasso_order_index | branch_point | monodromy | channel_vector (kappa_c,kappa_s,kappa_int) | channel_content | note |
|---|---:|---|---|---|---|---|
| x1 | 0 | `3*2**(1/3)/4 + 3*2**(1/3)*sqrt(3)*I/4` | `[1, 0, 2]` | `unavailable` | `unavailable` | normalized kappa entries are algebraic at this coalescence, not exact Q |
| x1 | 1 | `-3*2**(1/3)/2` | `[0, 2, 1]` | `unavailable` | `unavailable` | normalized kappa entries are algebraic at this coalescence, not exact Q |
| x1 | 2 | `3*2**(1/3)/4 - 3*2**(1/3)*sqrt(3)*I/4` | `[2, 1, 0]` | `unavailable` | `unavailable` | normalized kappa entries are algebraic at this coalescence, not exact Q |

## x2 Role Solve

- Degree: `1`.
- Monodromy: `[0]`.
- Stratum `x1=0` typed as `role-denominator pole`.
- This is a role-denominator pole stratum, not branch monodromy.

## x3 Role Solve

- Slice: `x1 = 1`.
- Polynomial: `x3**2 + x2 - 2`.
- Monodromy: `[1, 0]`.
- Cycle type: `[2]`.

## Certificate Summary

- Overall status: `PASS`.
- Status counts: `{'CERTIFIED_PERMUTATION': 14, 'UNCERTIFIED_STEP_MATCH': 0, 'UNCERTIFIED_CLOSURE_MATCH': 0, 'NON_BIJECTIVE_CLOSURE': 0, 'CONTINUATION_PROXIMITY_DISAGREEMENT': 0, 'LOOP_HITS_DISCRIMINANT': 0, 'ROOT_FIDELITY_FAILURE': 0, 'DISCRIMINANT_ORACLE_MISMATCH': 0, 'COALESCENCE_ORACLE_MISMATCH': 0, 'COMMON_FRAME_NOT_DISTINCT': 0, 'HURWITZ_FACTORIZATION_FAILURE': 0}`.
- Coalescence oracle matches: `True`.
