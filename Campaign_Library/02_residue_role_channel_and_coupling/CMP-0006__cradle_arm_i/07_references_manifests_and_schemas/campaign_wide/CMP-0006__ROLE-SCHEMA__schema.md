# Arm I record schema v1 (cai_record_v1)

One record per evaluated program per fixture per semantics. Big ints / Fractions serialize as strings (exactness survives JSON). Fields: see `schema.py` (slots dataclass; ad-hoc fields rejected at from_json).

**Role gate:** closure verdicts require a ledger AND role=probe — a verdict without an account is the untraceable belief this project types against.

**Per-kind closure identities (the law each ledger entry is graded by):**

- **two_complement**: width-w values live in [-2^(w-1), 2^(w-1)); wrap(x) = ((x + 2^(w-1)) mod 2^w) - 2^(w-1)
- **wrap**: value + discard*2^w == true Z result (add/sub/shl; mul as high_word)
- **remainder**: q*divisor + discard == dividend under the named semantics; trunc: sign(discard)==sign(dividend) or 0; floor: sign(discard)==sign(divisor) or 0; euclid: 0 <= discard < |divisor|
- **shifted_out_bits**: value*2^k + discard == input, 0 <= discard < 2^k (arithmetic shift; holds for negatives)
- **cast_residue**: Fraction(value) + discard == Fraction(true) (int<->float64 casts are rounding ops with exact Q accounts)
- **seam_bitcast**: lossless reinterpretation; discard == 0 by law; the typed SEAM event records the domain change (mechanism, not fence — Will 2026-06-12)

Freeze status: tracked in manifest_v1.json (frozen flag + freeze_pins_sha256.json on Will's sign-off).
