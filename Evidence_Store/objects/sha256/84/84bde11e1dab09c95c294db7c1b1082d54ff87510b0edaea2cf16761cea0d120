# MUTATION REPORT — Campaign A

Mutation controls prove the suite is **non-tautological**: it catches a lying engine.
Each mutant (`src/lloyd_v4/evals/channel_spectrum_carrier/mutants.py`) is a deliberately-wrong
variant; for each, `tests/test_channel_spectrum_carrier_mutants.py` shows the **correct** engine
passes a check and the **mutant fails the same check**. All 8 mutant tests pass (i.e. all mutants
are caught). The mutants are the only place a kill condition is permitted to fire.

| # | mutant | wrong behaviour | check that catches it | kill |
|---|---|---|---|---|
| 1 | `mutant_channel_vector_drop_mixed` | zeroes the mixed (p>0,q>0) interaction coefficients | reduction identity Σκ̂ = Ĉ_r(1,1) breaks (keystone: -8 ≠ -12) | KC-A1 |
| 2 | `mutant_channel_density_wrong_sign` | uses (-1)^r instead of (-1)^{r+1} | keystone Ĉ₂(1,1) = +12 ≠ pinned -12 | (sign) |
| 3 | `mutant_channel_vector_bad_split` | leaks the diagonal into H_c (H_s = 0) | keystone pure-coupling κ̂_{2;2,0} ≠ pinned -4 | KC (bad split) |
| 4 | `mutant_normalize_float` | float sqrt + float division; emits a float "rational" for odd order | (a) correct refuses to emit a value for σ₁∈Q(√14); (b) canonical encoder raises `TypeError` on the float | KC-A4 / KC-A5 |
| 5 | `mutant_gauge_H_no_shift` | returns H unchanged (pretends gauge moves nothing) | real gauge moves a channel; the no-op does not — "channels move" assertion fails | KC (no-shift) |
| 6 | `mutant_label_sensitive_fingerprint` | a label-*sensitive* fingerprint that changes under coordinate permutation | canonical (label-forgetting) passive orbit has size 1 (trivial); the mutant's orbit has size > 1, i.e. it falsely reports an active orbit | KC-A7 |
| 7 | `mutant_string_eq` | compares rationals by raw `"num/den"` string of **unreduced** pairs | `-12/196` and `-3/49` are the same rational (`Fraction ==` True) but compare unequal as strings — the string compare lies | KC (string compare) |

## Why these are not tautological

The keystone truth values used as the oracle are **hand-derived** (cofactor expansion) and frozen
as literal constants in the tests and in `fixtures.py` (PREREG_AMENDMENT_001 A1.2) — they are *not*
produced by the channel-density implementation under test. A mutant that lies is therefore measured
against an external truth, not against itself. In addition:

- the reduction identity (mutant 1) is checked by **two independent code paths** (Vandermonde
  interpolation vs direct (1,1) evaluation), so agreement is a genuine cross-check;
- the float mutant (4) is caught **structurally** — the canonical encoder refuses any float, so a
  float can never reach a graded artifact even if a future mutation tried;
- the passive/active mutant (6) is caught by the **label-forgetting** fingerprint, which is the
  invariant the whole separation search relies on.
