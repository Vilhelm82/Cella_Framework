# Conjecture C — No-Binade-Drop for Correctly-Rounded Sqrt — Proof Audit Preregistry

> **Status: FROZEN 2026-05-18 pre-measurement.** Per `CAMPAIGN_DISCIPLINE.md` Rule 1.1, binding.

## 0. Context

The c2 lattice sharpness audit ([`../c2_lattice_sharpness_audit/closeout.md`](../c2_lattice_sharpness_audit/closeout.md), Amendment II) established a conjecture-conditional theorem:

> **Theorem (conditional on Conjecture C, n=2):** c2 = round(V_2 + round(x_term − 1)) is an integer multiple of ulp(f_float), provided Conjecture C holds.

Conjecture C is the load-bearing piece. This audit attempts to prove it.

## 1. The statement (FROZEN)

> **Conjecture C (no-binade-drop for correctly-rounded sqrt under canonical squaring).**
>
> Let f ∈ float64 with f ∈ [2^k, 2^(k+1)) for some integer k in the IEEE 754 binary64 normal range (k ∈ [−1022, +1023]). Let R = round-to-nearest-even(sqrt(f)) ∈ float64. Then the float64 product `round-to-nearest-even(R · R) ≥ 2^k`.
>
> **Equivalent statement.** Correctly-rounded sqrt strictly preserves the binade-floor under canonical float squaring.

## 2. Proof strategy (FROZEN)

The proof proceeds by case analysis on the parity of k.

### Case A: k even (k = 2m)

For any f ∈ [2^(2m), 2^(2m+1)):
- `sqrt(2^(2m)) = 2^m`, which is **itself a float64** (a normalized binary value with mantissa 1.0...0 and exponent m).
- `sqrt(f) ∈ [2^m, 2^(m+1/2)) ⊂ [2^m, 2^(m+1))`.
- For `f = 2^(2m)` exactly: `sqrt(f) = 2^m` exactly, so `R = 2^m`, and `R · R = 2^(2m) = 2^k`. Result is **exact**, equality holds.
- For `f > 2^(2m)`: `sqrt(f) > 2^m`. By round-to-nearest, `R` is the nearest float to `sqrt(f)`. The nearest float at or above `2^m` is `2^m` itself (since `2^m` is a float) or higher. So `R ≥ 2^m`. Therefore `R · R ≥ 2^(2m) = 2^k`. The float64 product `round(R · R)` either equals `R · R` exactly (if representable) or rounds to a nearby float, which is at least `2^k` because `R · R ≥ 2^k`.

### Case B: k odd (k = 2m + 1)

For any f ∈ [2^(2m+1), 2^(2m+2)):
- `sqrt(2^(2m+1)) = sqrt(2) · 2^m`. This is an **irrational** number, NOT a float.
- The two floats surrounding `sqrt(2) · 2^m` are `R_below(m)` and `R_above(m)`, where (in hex form) `R_below(m) = 0x1.6a09e667f3bccp+m` and `R_above(m) = 0x1.6a09e667f3bcdp+m`. These have the same mantissa pattern, just different exponents — the mantissa pattern of correctly-rounded `sqrt(2)`.
- By the structure of round-to-nearest-even applied at `sqrt(2) · 2^m`: the audit will verify empirically that `R = R_above(m)` for every normal-range m. The verification is direct because both candidates and `sqrt(2)·2^m` are computable.
- For `f = 2^(2m+1)` exactly: `R = R_above(m)`, and `R · R = R_above(m)²`. Will verify that `R · R > 2^(2m+1)` (strictly), and that `round(R · R) ≥ 2^(2m+1)`.
- For `f > 2^(2m+1)`: `sqrt(f) > sqrt(2)·2^m`, so `R ≥ R_above(m)` (round-to-nearest from above moves R upward, never below). Hence `R · R ≥ R_above(m)² > 2^k`.

### Joint conclusion

For both cases, `R · R ≥ 2^k` (real value), and the float64 rounding `round(R · R)` produces a float ≥ `2^k`. Therefore `V_2 = round(R · R) ≥ 2^k`. **∎**

## 3. Empirical verification (FROZEN)

The proof above uses one empirical step: "`R = R_above(m)` for every normal-range m." This must be verified across all binade boundaries 2^k for k odd in the normal range.

### Plan

1. For every k odd in {−1021, −1019, …, +1021}, compute:
   - `f = 2^k` exactly in float64
   - `R = math.sqrt(f)` in float64 (correctly-rounded per IEEE 754)
   - `R_below = math.nextafter(R, 0)`
   - `R_above = R` (by claim) — verified to equal `R_above(m) = 0x1.6a09e667f3bcdp+m`
   - `R · R` in float64
   - Check: `R · R ≥ 2^k`?

2. For every k even in same range, compute:
   - `f = 2^k`
   - `R = math.sqrt(f)`
   - Check: `R = 2^(k/2)` exactly?
   - `R · R` — check equals `2^k`?

3. For each k, sample f values **within** the binade [2^k, 2^(k+1)) at the densest interesting positions:
   - The first 1000 floats above 2^k (most dangerous edge)
   - Mid-binade samples (random or evenly-spaced)
   - The last 1000 floats below 2^(k+1) (upper edge, less dangerous but worth covering)
   - For each f, verify `round(R · R) ≥ 2^k`

### Pre-registered predictions

| # | Prediction | Threshold |
|---|---|---|
| P_C1 | For every k even in normal range, `R = math.sqrt(2^k) = 2^(k/2)` exactly | strict, all binade boundaries |
| P_C2 | For every k even, `R · R = 2^k` exactly at the boundary | strict |
| P_C3 | For every k odd in normal range, `R = math.sqrt(2^k)` equals `R_above(k//2) = 0x1.6a09e667f3bcdp+(k//2)` | strict, all binade boundaries |
| P_C4 | For every k odd, `R · R` (the float64 product) is strictly greater than `2^k` | strict |
| P_C5 | For every k in normal range and every sampled f ∈ [2^k, 2^(k+1)) (boundary, first 1000 above, mid-binade), `round(R · R) ≥ 2^k` | strict, zero counterexamples |
| P_C6 | The above proof structure (Case A + Case B) is sound modulo the empirically-verified step in §2 Case B | review of proof |

## 4. Pre-registered failure modes

| ID | Condition |
|---|---|
| F_C1 | `R ≠ 2^(k/2)` for some k even — would refute Case A's premise |
| F_C2 | `R · R ≠ 2^k` for some k even at the boundary — would refute Case A's conclusion |
| F_C3 | `R ≠ R_above(k//2)` for some k odd — would refute Case B's empirical premise (need stronger analysis) |
| F_C4 | `R · R ≤ 2^k` for some k odd in real arithmetic — would refute Case B |
| F_C5 | `round(R · R) < 2^k` for any sampled f in any binade — would directly refute Conjecture C |
| F_C6 | Any case where the proof's claimed reasoning has a logical gap |

## 5. V4 typed outputs

Each binade-boundary record:

```json
{
  "k": int,
  "k_parity": "even" | "odd",
  "f_target": float (= 2^k),
  "R_sqrt": float,
  "R_above_predicted": float,
  "R_below_predicted": float,
  "R_matches_predicted": bool,
  "R_squared_real_value": [string, mpmath representation],
  "R_squared_float": float,
  "R_squared_float_geq_2_to_k": bool,
  "validity": {defined, finite, observable, selectable, advanceable}
}
```

In-binade sample records: same structure with additional `position` field indicating "first_1000_above" / "mid_binade" / "last_1000_below" and the sample index.

Cross-binade aggregator:

```json
{
  "audit_name": "conjecture_c_proof_audit",
  "n_binades_tested": int,
  "n_normal_range_even_k_tested": int,
  "n_normal_range_odd_k_tested": int,
  "n_in_binade_samples_per_binade": int,
  "total_records": int,
  "F_C1_count": int,
  "F_C2_count": int,
  ...
  "F_C5_count": int,
  "verdict": "C_proven" | "C_falsified" | "C_unresolved",
  "proof_writeup_location": "scratch/conjecture_c_proof_audit.py with proof comments"
}
```

## 6. Closeout criteria

1. Empirical verification across all normal-range binade boundaries (≈ 2000 k values) AND sample f values within each binade. Target: ≥ 2 million c2 lattice checks.
2. Each pre-registered prediction (P_C1–P_C5) audited explicitly.
3. P_C6 (proof soundness review) addressed in closeout writeup.
4. Verdict assigned:
   - **C_proven**: All P_C1–P_C5 hold strictly AND proof structure is sound.
   - **C_proven_with_caveat**: P_C1–P_C5 hold but the empirical step in Case B suggests refinement (e.g., R is sometimes the rounded float just above R_above).
   - **C_falsified**: Any failure mode triggered.
   - **C_unresolved**: Empirical evidence inconclusive at edge cases (e.g., subnormal-adjacent binades).
5. Byte-stable reproducibility.
6. Phase next list:
   - Machine-checkable formalization (Lean / Coq) if proven
   - Formulate Conjectures C_3, C_4, C_5 for cbrt, quartic, quintic
   - Re-examine c2 lattice campaign closeouts to remove "conditional on C" qualifier for n=2
7. Literature audit logged separately.

## 7. Out of scope

- Subnormal range (Conjecture C restricted to normal range). Subnormal cases require separate treatment.
- Other root degrees (C_3, C_4, C_5) — Phase next.
- Other floating-point formats (float32, float128, bf16) — likely the same proof structure applies, but verification is separate.
- Non-binary radices — out of scope.
- Alternative rounding modes (round-toward-zero, round-toward-infinity) — proof depends on round-to-nearest-even.

## 8. Estimated complexity of the proof

The proof is **case analysis on parity of k** plus **one direct empirical verification** for each case:

- **Case A (k even):** trivial — `sqrt(2^(2m)) = 2^m` exactly, `2^m · 2^m = 2^(2m)` exactly. ~3 lines.
- **Case B (k odd):** requires:
  - Identifying R_above(m) and R_below(m).
  - Verifying that `R = R_above(m)` (correctly-rounded sqrt at the binade boundary picks the upper neighbor). This is empirical but exhaustively checkable.
  - Showing `R_above(m)² > 2^(2m+1)` strictly, AND that `round(R · R)` rounds to a float ≥ `2^(2m+1)`. Both can be checked numerically for each m.
- **Joint conclusion:** `round(R · R) ≥ 2^k` in all cases.

Total: ~1 page of writing for the case-analysis structure, plus exhaustive numerical verification of the "R = R_above" step.

## 9. References

- Amendment II of [`../c2_lattice_sharpness_audit/closeout.md`](../c2_lattice_sharpness_audit/closeout.md): explicit framing of C as load-bearing open problem
- IEEE 754 binary64 standard (especially round-to-nearest-even semantics)
- Hauser, Markstein, Boldo et al. on correctly-rounded sqrt error analysis (existing literature — relevant background)
- Discipline: `CAMPAIGN_DISCIPLINE.md` Rule 1.1
