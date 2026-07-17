# Arm I Stage C Report — orbits vs Hull–Dobell (CL-I4, the bar)

**Date:** 2026-06-12 (machine date). **Authority:** brief §7 Arm I
Stage C + Will's Stage-C GO; checkpoint VERIFIED chat-side (both
collapse mechanisms verified analytically). **Prereg:** FROZEN
pre-emission, pin
`d012925d8db7a10227f546930c2c1a9d9ac79244c33e33d573f2a5355d1005ba`;
manifest sha gate-enforced (rule 1.9); clause parity (rule 1.8).
**Records:** `stage_c/records/stage_c_records.jsonl`, sha256
`bf12f568b206af27462e5fe7b4ec8ee9a82fd5f38ff8bb18a8434e2eef5bf57e`,
byte-stable ×2 (PIC.5). Suite exit 0; 34 cai tests.

## Verdicts

| Prediction | Verdict | Result |
|---|---|---|
| PIC.1 orbit ledger exactness | **PASS 3/3** | The carry fold M_n = a·M_{n−1} + carry_n·2^w reconstructs the exact unwrapped trajectory: wrapped + M == a^n·seed + c·(a^n−1)/(a−1) in ℤ at every pinned sample step, including n = 65536 — Stage A's fold, holding over sixty-five thousand composed steps. |
| PIC.2 the bar | **PASS 3/3 — K-I3 NEVER FIRED** | Measured projection towers == pinned fingerprints, one-to-one with the exact Hull–Dobell profiles. Full: every window full. c1-broken: the parity window FROZEN (P₁ = 1). c3-broken: the mod-4 window fails to double (P₂ = 2). **Discrimination held: both broken LCGs share total period 32768; the tower separates what the plain period cannot.** |
| PIC.3 honest budgets + 𝔽₂ | **PASS** | MINSTD: zero fixed point exact; typed `period_exceeds_pinned_budget` at 200k, recorded as consistent-not-proof. xorshift32: 𝔽₂-linearity certified 10/10 pinned pairs, domain seam typed; typed cap refusal. |
| PIC.4 refusal discipline | **PASS** | Exactly the two pinned budget refusals, none elsewhere. |
| PIC.5 determinism | **PASS** | byte-stable ×2, sha `bf12f568…`. |

## What the stage establishes

The non-triviality charge is answered by measurement. A plain period
counter — divmod restated — reads 32768 for both broken generators
and cannot say which law each one broke. The carry-ledger analysis
reads the same orbits through the ledger's own dyadic windows and
names the broken condition per fixture: the parity window freezes
exactly when c shares a factor with m; the mod-4 window fails to
double exactly when a ≡ 3 mod 4. The Hull–Dobell theorem — external,
classical, computed independently — agrees with the tower fingerprint
one-to-one. **The integer ledger carries structure the value channel
provably does not.** This is the ord₂-of-HR133 pattern on its third
outing: measured orbit structure graded against a number-theoretic
formula, exact everywhere.

## Status moves (frozen rules)

- **CL-I4 → DEMONSTRATED** (PIC.1 ∧ PIC.2 ∧ PIC.3 ∧ PIC.4; the K-I3
  honest-close branch was live and wired, and was not taken).

## Defect chains

None — third consecutive clean chain.

## Will's desk

- Stage-C acceptance → **Stage D GO** (the last stage): the int↔float
  seam (CL-I5: cast residues typed and exact,
  schema-indistinguishable from arithmetic residues) + the poster
  (CL-I6: fast inverse square root, the 0x5f3759df bit-route vs the
  certified route, the gap exactly accounted per stage).
- Then the Arm I close: 4 of 6 claim rows already DEMONSTRATED; the
  arm-level close draft follows the atlas pattern (reserved
  conversations: none outstanding for this arm beyond the close
  itself; Arm M ordering already ruled).
