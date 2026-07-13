# CERTIFICATE SCHEMA — two registers, one object

Every result the engine emits is a certificate. A certificate has two registers rendered
from one underlying record — the plain register for humans, the machine register for
verification. Neither is optional.

## Design rules (fixed at Layer 0)

1. **The plain register uses ordinary language.** No internal jargon. Every sentence is
   either a value, a yes/no, or a named reason.
2. **The certificate certifies the computation and its account — never the world.**
   It may say "computed exactly" or "refused: rank-deficient window". It never says
   "fault present". Detection claims live in a separate detection statement that carries
   its own confidence figures and cites the certificates under it.
3. **Refusals are first-class results.** A refusal certificate looks the same as a value
   certificate, with the reason where the value would be.
4. **Anyone can re-run it.** The machine register contains everything needed to reproduce
   the result bit-for-bit.

## The plain register — four questions, always the same four

```
WHAT WAS COMPUTED
  One sentence naming the quantity and the data it was computed from.
  "Coupling-channel value for sensors (motor_current, shaft_speed, bearing_temp),
   window 14:02:00–14:03:00."

WHAT IS EXACT
  What part of this result is exact arithmetic, and what part carries a tracked
  leftover. If a leftover exists, one sentence on whether it is recoverable.
  "The value is exact given the fitted surface. The surface fit discarded a
   remainder; the remainder is recorded and small enough to change nothing here."

WHAT WAS REFUSED, AND WHY
  Anything the engine declined to compute, with the plain reason.
  "Curvature was refused for window 14:03–14:04: the three channels moved in
   lockstep, so no surface can be fitted (rank-deficient)."

WHAT WOULD CHANGE THIS RESULT
  The conditions this result depends on — what, if different, gives a different
  answer. "Recalibrating a sensor would NOT change this value (it is
  calibration-proof). A different window length could."
```

## The machine register

```
inputs:        content hash of every input (data slice, parameters, code version)
account:       the residue account — every observation map applied, each with its
               typed defect: exact remainder (species M: measurement) or
               representation motion (species R: gauge), or a refusal token
refusals:      typed tokens with stratum classification
number_type:   which rung of the exact tower each emitted value lives on
rerun:         double-run digest — the result is emitted only if two independent
               executions agree bit-for-bit
schema:        certificate schema version
```

## Vocabulary map (machine term → plain term)

| machine | plain register renders as |
|---|---|
| residue, species M | "leftover from measurement/rounding — recorded" |
| residue, species R | "difference of representation only — the underlying quantity is unchanged" |
| refusal: RANK_DEFICIENT | "channels moved in lockstep; no surface can be fitted" |
| refusal: SINGULAR_GRADIENT | "the surface has no well-defined direction here" |
| refusal: BELOW_DETECTION | "any real signal here is smaller than what was discarded" |
| gauge-invariant | "calibration-proof: recalibrating or rescaling sensors cannot change it" |
| exact (ℚ or ℚ(√q)) | "exact — no rounding anywhere in this number" |

This table grows only alongside the refusal vocabulary (see ADMISSIONS A-004 discipline).
