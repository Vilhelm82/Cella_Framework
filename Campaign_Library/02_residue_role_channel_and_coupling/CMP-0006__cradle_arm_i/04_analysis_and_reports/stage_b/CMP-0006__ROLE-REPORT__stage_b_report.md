# Arm I Stage B Report — division-semantics fingerprints (CL-I3)

**Date:** 2026-06-12 (machine date). **Authority:** brief §7 Arm I
Stage B + Will's Stage-B GO; checkpoint VERIFIED chat-side (incl. the
a>0, b<0 trunc/euclid coincidence verified analytically). **Prereg:**
FROZEN pre-emission, pin
`b3b4901dca42c2339820723f78e4f68b32c787744539943f9de5228825d05044`;
manifest sha gate-enforced (rule 1.9); clause parity (rule 1.8).
**Records:** `stage_b/records/stage_b_records.jsonl`, sha256
`82f699105f152ea1deec3a019df893893541ce069cda05beec6fc38fe69e8eb2`,
byte-stable ×2 (PIB.5). Suite exit 0; 26 cai tests.

## Verdicts

| Prediction | Verdict | Result |
|---|---|---|
| PIB.1 semantics closure | **PASS 16/16** | Every (pair, semantics) row: q·b + r == a exactly; per-semantics remainder laws hold (trunc: sign-of-dividend; floor: sign-of-divisor; euclid: 0 ≤ r < |b|); width-wrap entries close where the quotient wraps. |
| PIB.2 the fingerprint law | **PASS 16/16, two-sided** | Measured pairwise splits == the derived sign-configuration predicates on every pair; zero splits at every exact division. Grid informative on all three comparisons. **K-I2 never fired.** |
| PIB.3 discard-channel taxonomy | **PASS** | INT_MIN//−1: exact division — all three semantics identical in ℤ and identically wrapped; the quotient-WRAP entry fires and closes the account while the semantics fingerprint stays zero. **Wrap is a width event, not a rounding-mode event.** And 13//3: a discard without a distinguisher — r ≠ 0, zero splits. |
| PIB.4 refusal honesty | **PASS 2/2** | Division by zero and unknown semantics typed; zero refusals on the lawful battery. |
| PIB.5 determinism | **PASS** | byte-stable ×2, sha `82f69910…`. |

## What the stage establishes

The three division semantics are certified as three rounding modes
whose disagreements are *exactly predictable from the sign
configuration and discard presence alone* — never from the quotients.
A fingerprint requires a discard the modes disagree about: exact
divisions never fingerprint (16/16 reverse direction), positive pairs
discard without fingerprinting, and the quotient-wrap channel is
orthogonal to the semantics channel entirely. This is the integer
instance of the conditional fingerprint law family (HR134
amendment-6 lineage): *routes differ exactly when a distinguishing
discard rounds* — third substrate, same law shape.

## Status moves (frozen rules)

- **CL-I3 → DEMONSTRATED** (PIB.1 ∧ PIB.2 ∧ PIB.3 ∧ PIB.4; K-I2
  never fired).

## Defect chains

None — second consecutive clean chain.

## Will's desk

- Stage-B acceptance → **Stage C GO**: orbits vs Hull–Dobell — the
  arm's non-triviality bar (CL-I4), with **K-I3 armed**: if the
  carry-ledger orbit analysis cannot recover the Hull–Dobell
  full-period conditions on the pinned LCG set, the arm closes
  honestly as having added nothing beyond divmod's restatement.
- Then Stage D (seam + poster; CL-I5/CL-I6) and the arm's close.
