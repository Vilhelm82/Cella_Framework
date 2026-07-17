# Arm I fixtures v1 (FX-I-A..F)

Frozen with the manifest on Will's sign-off. Classes: wrap ledger (A), division semantics (B), shift/mask death grid (C — the CL-I2 battery), orbits incl. xorshift under the unbounded-bitwise ruling (D), int<->float seam (E), the fast-inverse-sqrt poster (F, demo-tier).

- **FXIA1** (FX-I-A): add wraps once, mul wraps again — composed wrap chain; value drifts far from truth, ledger holds it
- **FXIA2** (FX-I-A): int64 wrap chain (both directions)
- **FXIA3** (FX-I-A): alternating wrap/unwrap — discards cancel in truth but each is individually nonzero
- **FXIA4** (FX-I-A): 65536^2 wraps int32 to EXACTLY 0: the value carries no information at all; the ledger carries all of it
- **FXIA5** (FX-I-A): int64 high-word extraction mid-chain
- **FXIB1** (FX-I-B): the (-7)//2 family: trunc/floor/euclid disagree exactly when signs do — three rounding modes on one lattice
- **FXIB2** (FX-I-B): INT_MIN // -1: the quotient itself wraps — the remainder ledger alone is not enough; the wrap entry completes it
- **FXIB3** (FX-I-B): int64 signed family, large magnitudes
- **FXIC1** (FX-I-C): val2(a) vs k both sides of the boundary: residue == 0 iff val2(a) >= k — the integer shift-death biconditional (CL-I2's integer half)
- **FXIC2** (FX-I-C): negative operands: two's-complement arithmetic shift discards are still exact and non-negative
- **FXIC3** (FX-I-C): MSB-only operand: val2 == w-1 boundary case (width-wrapped negative)
- **FXID1** (FX-I-D): Hull–Dobell satisfied: full period 65536
- **FXID2** (FX-I-D): c shares a factor with m (condition 1 broken)
- **FXID3** (FX-I-D): a-1 = 2 not divisible by 4 while 4 | m (condition 3 broken)
- **FXID4** (FX-I-D): MINSTD multiplicative Lehmer: c = 0 fails condition 1 by construction; the classical full-period story lives in a different theorem — honest contrast row
- **FXID5** (FX-I-D): xorshift32: pure F2-linear map — period = order of the companion matrix; XOR/shift ledger is exact by birth (bitwise scope unbounded per Will's ruling)
- **FXIE1** (FX-I-E): int64 -> float64 above 2^53: rounding residue on an INTEGER input — the cast is a rounding op and gets a rounding account
- **FXIE2** (FX-I-E): float64 -> int truncation: the discarded fraction is the account
- **FXIE3** (FX-I-E): mixed pipeline int -> float -> *3 -> trunc -> int: cast residues + float rounding compose; closure graded in exact ℚ end-to-end
- **FXIF1** (FX-I-F): fast inverse square root: bitcast -> shift -> subtract -> bitcast -> one Newton step, vs the certified route (typed_sqrt + division); the gap exactly accounted per stage, the magic constant's error decomposed

All operands pinned exactly in `fixtures.py`; Hull–Dobell expectations verified by exact arithmetic at generation (stage0_controls in the manifest).
