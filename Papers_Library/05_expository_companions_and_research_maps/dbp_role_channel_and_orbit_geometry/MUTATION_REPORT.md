# MUTATION REPORT — Campaign H

Ten deliberately-wrong variants (`src/lloyd_v4/evals/rolechspec_symbolic_proof_extraction/mutants.py`).
For each, `tests/test_campaign_h_mutants.py` shows the correct engine passes a check and the mutant
fails the same check. All mutant tests pass (all 10 caught). Mutants are the only place a kill is permitted.

| # | mutant | wrong behaviour | check that catches it | kill |
|---|---|---|---|---|
| M1 | `mutant_gauge_coeffs_no2` | `a_i = H_ii/g_i` (no factor 2) | `H_perp` diagonal is nonzero | K-H1 |
| M2 | `mutant_obstruction_sign` | flips a sign in `O_ij` | `H_perp` off-diagonal ≠ the obstruction | K-H1 |
| M3 | `mutant_keep_diagonal` | does not subtract the gauge | `H_perp` diagonal is nonzero | K-H1 |
| M4 | `mutant_unsaturated_nonzero` | claims nonzero-on-regular without saturating | `nonzero_on_regular_Q(g1−g2)` is False (a regular rational zero), mutant says True | K-H3 |
| M5 | `mutant_drop_role` | omits one output role from RoleChSpec | the full RoleChSpec has 3 roles; the mutant has 2 (incomplete) | K-H3 |
| M6 | `mutant_hash_equal` | compares components by hash of the string form | `(O12+O13)²` vs its expansion are symbolically equal but hash-unequal | K-H3 |
| M7 | `mutant_is_zero_float` | float substitution with a tolerance | an exactly-nonzero `1/10¹²` is called "zero" under the tolerance | K-H6 |
| M8 | `mutant_drop_exceptional` | drops the typed exceptional component | the report's `typed_strata` / sum-of-squares factor disappear | K-H4 |
| M9 | `mutant_cached_rolechspec` | returns a cached coarse label | two genuinely different gauge-normal jets are wrongly equated | (cached-label) |
| M10 | `mutant_trivial_identity` | "proves" only `O=O' ⟹ equal` (the easy direction) | `injectivity_checked = False` — the substantive converse is missing | K-H3 |

## Why these are not tautological

- **The normal form is checked by construction** (M1, M2, M3): the diagonal must vanish and the off-diagonals must equal the obstruction; any gauge/formula corruption breaks that symbolically.
- **Saturation is mandatory** (M4): a factor with a regular rational zero (`g1−g2`) is rejected by `nonzero_on_regular_Q`; skipping the check admits a false injectivity.
- **Equality must be complete and symbolic** (M5, M6, M10): a dropped role, a hash comparison, or a one-direction "proof" each fails a completeness/exactness check.
- **No float in the verdict path** (M7): the proof uses exact `==0`; a tolerant float comparison provably misjudges a tiny exact nonzero.
- **Exceptional components cannot be hidden** (M8): the typed strata are recomputed and reported.
- **RoleChSpec is recomputed, never cached** (M9).
