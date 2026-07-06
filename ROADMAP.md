# ROADMAP — gates

Gate-based, no dates. A gate closes only when its criterion is met and the result is
certified under the schema. Failing a kill condition is a finding, not a failure.

## Layer 0 — the harness

- **G0 — first primitive is real.** `Cell` round-trips: value ⊕ residue reconstructs the
  true object exactly on the rational-op class, and `tests/gate_zero.py` goes green.
  *CLOSED 2026-07-06 — first consequence of the self-ratifying admission standard
  (A-001 ESTABLISHED). Float rejection and immutability verified adversarially.*
- **G0.1 — residue algebra, species M.** Measurement defects compose across two chained
  observation maps; the composed account reconstructs exactly.
- **G0.2 — residue algebra, species R.** Representation defects (gauge motion) compose,
  their invisible subspace is enforced at type level, and a mixed M+R chain keeps the two
  species separated in the account. *This certifies the A-002 design conjecture — or
  refutes it, which reshapes Layer 0 and is worth knowing immediately.*
- **G0.3 — number tower.** ℚ(√q) arithmetic exact; no float constructor reachable from
  any verdict path.
- **G0.4 — refusals + certificate.** Every stub emits schema-conformant certificates;
  refusal paths produce refusal certificates, never exceptions or NaN; plain register
  renders for every token in the vocabulary.

## Layer 1 — the geometric substrate

- **G1.0 — jets and the carrier.** Gauge-normal form as canonical representation;
  carrier extraction certified against hand-pinned exact references.
- **G1.1 — the invariant tower.** σ tower + channel accounts on the analytical surface
  corpus (sphere, cylinder, saddle, torus, monkey saddle…), exact where the parity law
  says exact.
- **G1.2 — the sensor set.** Numerator tower, shape moment, localization channels, each
  admitted per A-007 with blindness statement + exact reference values.

## Layer 2 — the time-series bridge

- **G2.0 — the fit as observation map.** Windowed surface fit emits jets with typed fit
  defect; lockstep/degenerate windows refuse with stratum tokens.
- **G2.1 — noise floor + limit of detection** per the re-authored Validation Programme
  stages 2–3.

## Layer 3 — the diagnostic surface

- **G3.0 — capability contract opened** (A-006): method-by-method parity table against
  the origin inventory.
- **G3.1 — the A/B rerun.** Previously validated datasets rerun with the corrected
  sensors against the origin engine's recorded results, plus edge-localization scoring.
  **Kill: corrected sensors fail to beat the origin ratio sensors → the mathematical
  advantage does not transfer to data.**
- **G3.2 — expansion, blind, adversarial** (Validation Programme stages 4.2–6), including
  the isometric-bending attack with the parity-law defence. **Kill: shape moment adds no
  detections on ≥5-channel data.**
- **G3.3 — cross-method comparison + the six deliverable documents** (stages 7, 9).

## Standing constraints

- Standalone: zero code import from any previous repository, ever.
- Admission rule enforced (see `ADMISSIONS.md`).
- Exactness in the compute layer, statistics only in the detection layer; one certificate
  never mixes them.
- Double-run bit-identity before any result is emitted.
