# Arm I Stage A Report — wrap + shift ledgers + the CL-I2 unification

**Date:** 2026-06-12 (machine date). **Authority:** brief §7 Arm I
Stage A + Will's freeze GO + Stage-A checkpoint VERIFIED chat-side.
**Prereg:** FROZEN pre-emission, pin
`3c57f579684847b3055c0161c54d3b109784ae9b97afa18bb22853e0777250cc`;
dependency pins gate-enforced per rule 1.9 (manifest sha +
`precision_flow.py` content sha — the executed float-side instrument);
clause parity per rule 1.8. **Records:**
`stage_a/records/stage_a_records.jsonl`, sha256
`5be68f703eb2ba6b2a4ee1ba87492b548d6dc1a88e74893d132236838f136585`,
byte-stable ×2 (PIA.5). Suite exit 0; 19 cai tests.

## Verdicts

| Prediction | Verdict | Result |
|---|---|---|
| PIA.1 ledger exactness | **PASS 5/5** | Every FX-I-A chain: the deviation-fold reconstruction from (value, ledger, route) alone equals the independent native-ℤ referee exactly; every per-op closure identity holds at every step. |
| PIA.2 the unification | **PASS 19/19** | ONE predicate — ν₂(operand) ≥ window_floor — decided residue death identically with both instruments: 12/12 integer shift pairs (both sides of the val₂ boundary, negatives included) and 7/7 float dyadic-rational cases via HR133's imported rounder (both sides of every boundary). |
| PIA.3 no dead weight | **PASS** | Every-entry corruption sweeps: all entries load-bearing on every chain. FXIA4: value 0 carries nothing; the ledger reconstructs 2³². FXIA3: value == truth *coincidentally* — four nonzero discards cancel in the fold; right-by-cancellation certified lawful, not lucky (the integer cousin of HR134's coincidental-agreement class). |
| PIA.4 refusal honesty | **PASS 3/3** | Out-of-fragment op, out-of-range shift, non-representable seed: all typed; zero refusals on the lawful battery. |
| PIA.5 determinism | **PASS** | byte-stable ×2, sha `5be68f70…`. |

## The headline — CL-I2

**Integer shift-death and float dyadic death are one law.** On the
integer substrate the discard window is the k low bits a shift throws
away; on the float lattice it is everything below the spacing
2^(b−q+1) at precision q. In both worlds the residue dies exactly when
the operand's dyadic valuation covers the window — the same
comparison, evaluated once in shared code, agreed with the dedicated
instrument of each substrate on every pinned case, both directions of
every boundary. HR133's dyadic death was certified there as a float
phenomenon; this battery shows floats *inherit* it from ℤ.

*The account was born in float64; this is the first certificate that
it was never about floats* — the charter's question, answered on its
first scored battery.

## Status moves (frozen rules)

- **CL-I1 → DEMONSTRATED** (PIA.1 ∧ PIA.3 ∧ PIA.4).
- **CL-I2 → DEMONSTRATED** (PIA.2) — the arm's headline, landed at
  Stage A as designed.

## Defect chains

None — clean end-to-end. One authoring-time finding, locked by test
before the freeze: the **corruption-granularity law** — wrap-kind
entries are load-bearing at ±1, shifted-out entries at ±2^s (the floor
absorbs sub-quantum perturbations). The pinned battery has no shr
chains, so the frozen PIA.3 sweep is unaffected; the law is recorded,
not patched around.

## Will's desk

- Stage-A acceptance → Stage B GO (division-semantics fingerprints,
  CL-I3: trunc/floor/euclid as three rounding modes; the FX-I-B
  battery incl. INT_MIN//−1's quotient-wrap).
- **Reserved ruling #6 now ripe:** CL-I2 is certified — does HR133's
  row gain the dated unification note (by note, never by edit)?
- Kill conditions K-I1/K-I2/K-I3 stay armed for Stages B–D.
