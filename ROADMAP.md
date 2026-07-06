# ROADMAP — gates

Gate-based, no dates. A gate closes only when its criterion is met and the result is
certified under the schema. Failing a kill condition is a finding, not a failure.

## Layer 0 — the harness

- **G0 — first primitive is real.** `Cell` round-trips: value ⊕ residue reconstructs the
  true object exactly on the rational-op class, and `tests/gate_zero.py` goes green.
  *CLOSED 2026-07-06 — first consequence of the self-ratifying admission standard
  (A-001 ESTABLISHED). Float rejection and immutability verified adversarially.*
- **G0.1 — residue algebra, species M.** *CLOSED 2026-07-06* — `tests/gate_01.py`
  7/7 ×2 (`13e19bc7`): scalar + matrix carriers, multiplicative chains additive with
  current-input residues, original-truth mutant fails by exactly `T·δ₁δ₂`.
- **G0.2 — residue algebra, species R + single account.** *CLOSED 2026-07-06* —
  certified twice over: the mathematics by the G0.2 campaign (Stages 0/A/B/C, frozen
  preregs, conjecture DEMONSTRATED on the covered class) and the implementation by
  `tests/gate_02.py` 13/13 ×2 (`2d0bde4f`): 720-ordering account uniqueness through
  the API, attribution fold, two-epoch law with boundary guard, asymmetry law,
  owned holonomy with nonzero witness.
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

## DESIGN FREEZE — containment rules

These bind the build the way the admission standard binds introductions. Purpose: every
planned R&D outcome lands with blast radius zero or confined to interfaces shaped here.

1. **Two-ledger accounts.** The M and R ledgers never mix in composition. Their
   unification under one algebra is a certification target (G0.2) — never a dependency
   of any consuming code. If G0.2 refutes unification, a theorem changes status; no
   code breaks.
2. **Parameterized radicand.** `QSqrt` is `a + b·√r` for arbitrary positive non-square
   rational `r`. Never hardcode `r = g·g` — multi-constraint normalization may want
   Gram determinants, and a parameterized radicand absorbs that without a touch.
3. **Block interfaces, generic n.** Every constraint input is typed as a block (list of
   constraints); codim-1 implementations refuse blocks of length > 1 with a typed
   `CODIM_UNSUPPORTED` refusal — the API can always express what the theory cannot yet
   compute. Carrier extraction reads O from H directly (proven for general n); channel
   recovery is an n=3 cross-check, not the pathway. All isotypic/projector linear
   algebra is written for general n, never n=3 hardcoded.
4. **Scoped certificate claims.** Every completeness or identity claim states its tier
   (local/global; codim-1/system) in the certificate itself. Claims extend or gain
   qualifiers as R&D lands; they are never retracted.

**STOP-LINE.** Do not build: system-level (codim ≥ 2) fitting semantics — that is
exactly what the E2 theory determines, and anything invented there now is a guess
wearing code; cascade/monodromy machinery beyond token vocabulary — [interpretation]
tier until the transfer conjecture is tested. The build and the R&D converge at this
seam by design instead of colliding.

## Standing constraints

- Standalone: zero code import from any previous repository, ever.
- Admission rule enforced (see `ADMISSIONS.md`).
- Exactness in the compute layer, statistics only in the detection layer; one certificate
  never mixes them.
- Double-run bit-identity before any result is emitted.
