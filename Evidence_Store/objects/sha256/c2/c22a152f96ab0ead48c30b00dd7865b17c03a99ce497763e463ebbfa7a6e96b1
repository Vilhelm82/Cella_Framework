# Arm M Stage C Report — raw commutator + plaquettes (CL-M4, CL-M5)

**Date:** 2026-06-12 (machine date). **Authority:** brief §4 Arm M
Stage C + Will's Stage-C GO; checkpoint VERIFIED chat-side (common-mode
corner cancellation verified analytically). **Prereg:** FROZEN
pre-emission, pin
`0ee1cbe714a5a9a29fb3ec7acf8bf779f4b85ecaf979e8bc3f194fb42d5dbe5c`.
**Records:** `stage_c/records/stage_c_records.jsonl`, sha256
`bd2a5b2d451204e70287de40c81a9fbb207fa4e5a6d1213b22103fbb0566a51c`,
byte-stable ×2 (PMC.5). Suite exit 0.

## Verdicts

| Prediction | Verdict | Result |
|---|---|---|
| PMC.1 Clairaut attribution | **PASS 11/11** | Both orders close on every cell; the defect attributed twice over: C_raw == D₂ − D₁ == the signed residue-sum gap, exactly. Zero unattributed defect anywhere. |
| PMC.2 the conditional law | **PASS — K-M3 NEVER FIRED** | 7/7 protected cells read exactly zero (the theorem direction — including anisotropic cells whose corners round: corner deviations are common-mode and cancel). The predicate-selected witness fingerprinted exactly as pinned (FXMA1's binade-spanning cell, C_raw = 2.84e-14, fully attributed), the trivariate second witness too; 2 coincidental cancellations counted. |
| PMC.3 plaquettes | **PASS 6/6** | Holonomy ledger-folded and fully attributed on every plaquette; \|H\| ≤ the exposure bound with zero violations; the channel partition closes onto the bound exactly; the protected coarse plaquette reads zero; ulp plaquettes nonzero as pinned; all three trivariate faces scored. |
| PMC.4 refusals | **PASS** | Pole-corner probe typed; zero refusals on the lawful battery. |
| PMC.5 determinism | **PASS** | byte-stable ×2, sha `bd2a5b2d…`. |

## What the stage establishes

**The Clairaut defect of the raw float substrate is not noise — it is
the account gap, exactly.** When the two differentiation orders
disagree, the disagreement equals the difference of their
rounding-residue ledgers, to the last bit; when every subtraction is
exact, equality is a theorem regardless of how the corners rounded
(common-mode cancellation, verified analytically at the checkpoint
and measured 7/7). The fingerprint law family takes its **fourth
substrate instance** (HR134 float routes; Arm I division semantics;
Arm I shift windows via CL-I2; now the multivariate commutator), with
the coincidental-cancellation class sighted for the third time.
Plaquette transport adds the loop-level account: realized holonomy
never exceeds exposure, and the damage partitions exactly into
per-variable, coupling, and loop channels — the account has direction
AND curvature bookkeeping, with nothing unattributed.

## Status moves (frozen rules)

- **CL-M4 → DEMONSTRATED** (PMC.1 ∧ PMC.2 ∧ PMC.4; K-M3 silent).
- **CL-M5 → DEMONSTRATED** (PMC.3 ∧ PMC.4).

## Defect chains

None at the battery. The sharpened law (common-mode corners) was an
authoring-time derivation, frozen before any emission.

## Will's desk

- Stage-C acceptance → **Stage D GO**: directional smoothness verdicts
  on the kink loci (CL-M6) — per-order, per-direction smooth/kink/
  can't-certify with the diagonal-locus grid-blindness as a typed
  refusal class (the FX-M-E battery: |x|+|y|, x·|y|, max, max3).
- Then Stage E (landing decomposition + the T1 stretch + CL-M9's
  registered curvature measurement) and the arm's close. Arm M
  stands at 5 of 9 claim rows DEMONSTRATED.
