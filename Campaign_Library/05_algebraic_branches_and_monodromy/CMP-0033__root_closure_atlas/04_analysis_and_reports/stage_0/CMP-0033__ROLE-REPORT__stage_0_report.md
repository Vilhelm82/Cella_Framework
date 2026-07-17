# root-closure-atlas — Stage 0 report (the bench + classical baseline)

**Status: STAGE 0 COMPLETE — P0.1–P0.6 ALL PASS (P0.1 at second attempt
with the first-attempt chain preserved); baseline atlas populated (260
records, 32 fixtures, byte-stable ×2 including 128 live oracle calls);
zero CL-status changes, as mandated. STOPPED at this report.**
**Date:** 2026-06-11 (machine date; +1-day canon drift on the record).
**Branch:** `campaign/root-closure-atlas`. **Freeze pins:** manifest
`ce2e5352…`, SCHEMA.md `cf319cf9…`, schema.py `e62db16d…` (Will's
sign-off; both deviations blessed — notes in SCHEMA.md / FIXTURES.md).
**Records:** sha256 `ac3ab40d…933499`. Full suite exit 0 (2001+
collected, baseline re-verified at start). 90 rca tests green.

## 1. Pre-registered predictions (mechanical grades)

| P | Verdict | Evidence |
|---|---|---|
| P0.1 determinism | **PASS** (second attempt; first preserved) | two full battery runs sha-identical (`ac3ab40d…`); first ×2 failed on 46 I2 records — V3's `probe_tree.children` order is session-unstable while every VALUE is stable; declared normalization (children sorted; nothing graded reads the tree); surprise ledger Entry 1 |
| P0.2 arbiter coherence | **PASS** | ℚ/M wall-sign agreement everywhere both apply; zero contradictions |
| P0.3 baseline false-convergence | **PASS** | classical judges report `converged` on FX-E ghosts: FXE1 — Newton, Halley, secant (×2 starts); FXE2 — secant. The exact arbiter certifies f ≥ 2⁻²⁰⁰ > 0: every one is a confidently-reported root of a function with no zero |
| P0.4 expressibility map | **PASS** | 32/32 fixtures carry live-probed `lv3_compile` records (note: the first probe implementation was vacuous — it tested transport, not acceptance; caught and fixed before freeze, disclosed §4) |
| P0.5 schema sufficiency | **PASS** | zero ad-hoc fields (every record validated at write); the one schema change — `exact_zero` as fifth certificate value — pinned pre-execution in the manifest `freeze_note` as the blessed amendment |
| P0.6 role gate | **PASS** | `test_rca_schema.py::test_role_gate_navigator_cannot_carry_verdicts` — constructed navigator-with-verdict record rejected |

## 2. The classical baseline map (the deliverable; ATLAS.md carries the full table)

Across 140 judge emissions (fixture × instrument × start):
**clean_emit_right 86 / wrong_family 6 / wrong_boundary 7 /
wrong_off_family 41 / wrong_refusal_failure 0** —
`wrong_clean_emit_summary.json`, §1.3 four-way per the brief's mapping.
**Zero own-promise violations**: every classical instrument did exactly
what its registered semantics promised — and was confidently wrong 54
times anyway. The gap between column 1 (promise kept) and column 2
(where the machine-truth root actually lives) IS the campaign's
opening exhibit.

Headlines, all arbiter-certified:

- **Ghosts are accepted** (FX-E → `wrong_family_clean_emit` = 6 judge
  emissions per the canonical summary taxonomy; raw record level: 13
  `ghost_accepted` rows across roles and classes, of which 8 sit on
  FX-E — 6 judge + 2 oracle). Newton's residual at the "root" satisfies
  1e-12 honestly — float cancellation manufactured the zero (B3/B5
  leverage, exactly as the taxonomy predicted). [Prose reconciled to
  `wrong_clean_emit_summary.json` per Will's Stage-0 acceptance ruling
  4; the summary counts JUDGE emissions only — 6 family + 7 boundary +
  41 off-family = 54.]
- **The pole is a root** (FXF2 → part of `wrong_boundary_clean_emit` =
  7 judge emissions): Newton, Halley (×2 starts), secant, and both I2
  oracle variants "converge" at/near the pole-borne sign change where
  NO root exists; the arbiter's `refusal` certificate names the pole.
  The classical lie has a name in the schema now.
- **Off-family landings dominate the wrong column** (41): multi-root
  fixtures (FX-I basin starts, FX-G's second root, FX-H Wilkinson, FX-C
  clusters) — judges deliver *a* root, not *the bracketed* root; the
  landing-vs-start variability FX-I was built for is on the record.
- **The extremal Kerr merger point certifies exactly** (FXC_kerr2):
  `exact_zero` at the float 1.0 in ℚ — the A9 degeneracy is exactly
  certifiable when the parameter is exact; classical judges nearby
  report converged at xtol with values up to ~10⁵ lattice steps from
  the point (recorded per record).
- **S3's vocabulary collapse is now queryable**: `v3_status_bucket`
  populated on all 64 oracle records; `residual_ok_coordinate_
  indeterminate` covers ghost/tangency/cluster/multi-root exactly as
  the pre-screen predicted.

## 3. Deliverable inventory

D1 schema FROZEN (deviation note §SCHEMA.md; P0.5 amendment pinned) ·
D2 instruments (I1a–d with registered rules + fired-rule reporting; I2
real `MultiStartInput`/`SolveForInput` models, multi_start primary +
solve_defaults variant; I3 stub NOT_YET_PROBED) · D3 dual arbiter
(certified terminal cells; `exact_zero`/`refusal`/`none` special
certificates; mp escalation w/ honest cap refusal; coherence) · D4
manifest v1 FROZEN, 32 fixtures incl. FXB4 added at freeze (m=4,
even × non-dyadic), live-probed expressibility 32/32 · D5 claim ledger
seeded CL-1..7 all NOT_YET_PROBED (unchanged by Stage 0) · D6 atlas
populated + ATLAS.md baseline map · D7 this report +
`wrong_clean_emit_summary.json` + `surprise_ledger.md` (1 entry).

## 4. Disclosures (defects caught in-stage, all pre-freeze or pre-P0-grade)

1. **Vacuous expressibility probe** (caught pre-freeze): the first
   implementation tested the MCP *wrapper* for an error flag that does
   not exist there — recorded accepted=True unconditionally (HR129 in
   probe form). Fixed to read the oracle's own `ok`/`error` payload
   fields; manifest regenerated with honest probes before freeze.
2. **Wrong I2 parameter models** (caught pre-battery): `multi_start`/
   `solve_for` take `equation/values/solve_index`, not my guessed field
   names; fixed from the live tool schemas.
3. **Three even-crossing bracket pins** (caught by the pre-freeze
   wall-sign check): both Kerr horizons / both FXG1 roots inside one
   bracket — corrected to single-crossing brackets before any pin.
4. **Classical crash at the pole midpoint** (FXF2, caught run 1):
   bisection's midpoint hits x = 1.0 exactly; recorded as the judge's
   `refused` with the crash named — Python-classical semantics, honest.
5. **P0.1 first-attempt failure** — see P0.1 row + surprise Entry 1.

## 5. Facet A recommendation (per §14)

Scope sketch: the exact-sign certificate + lattice bracket closure as
the I3 probe's first organ — exact-ℚ sign at stencil walls via the EFT
lift (`evals/difference_tower/eft_eval.py`, imported, never rebuilt),
producing the same `CertifiedCell` objects the arbiter mints, but from
the PROBE side, on fixtures where `eval_exact` is in class; the arbiter
then grades probe-cells against arbiter-cells (instrument vs referee,
HR130 pattern). Primitive-sufficiency gap from §7: NONE remaining — the
lift exists (HR134). CL-1 and CL-7 are Facet A's rows. Battery: the
FX-A/D/E/F/G/K rational class first; annex via the certified elementary
set (Stage-E enclosure pattern) second.

## 6. Will's-desk items (§15.10)

1. **Name adoption** — candidates on the ledger entry (root-closure
   atlas / zero atlas / sign-closure survey); covenant holds, none used.
2. **TWO-CURVATURES fold-in decision** (Facet E written to work either
   way).
3. **Scoreboard (PROBE_READINESS) application text — DRAFTED, reserved
   to you per this GO's explicit clause** (stricter-clause-governs over
   the general canonical-write ruling): *"root-closure-atlas Stage 0
   (baseline): A4/A9 first contact made — Kerr-Δ extremal merger point
   certifies exact_zero in ℚ at a = 1.0; the FX-J zeros battery exists
   with M-certified cells. No row status changes: Stage 0 is baseline
   only; CL-1..7 all NOT_YET_PROBED."*
4. **Ledger close-of-stage refresh** — applied mechanically already
   (maintenance law); the OPEN entry now reads Stage 0 COMPLETE.
5. **Facet A GO** (§5 above) when you want the first organ built.

— Claire, on the bench, 2026-06-11 (machine date). STOPPED at the
Stage-0 report.
