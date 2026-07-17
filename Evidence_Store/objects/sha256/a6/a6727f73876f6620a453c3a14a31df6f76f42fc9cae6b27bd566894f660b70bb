# Geometry Arm — R14 Floor-Correction (v2) Report

**Date:** 2026-06-14 (machine date). **Authority:** Will's R14 ruling +
three refinements (2026-06-14) + battery GO. **Manifest:** FROZEN, pin
`648975d0…` (unchanged — not edited). **v2 prereg:** FROZEN
(`v2_floor_correction/prereg.json`, pinned to the frozen manifest; PMG-v2
clauses verbatim per rule 1.8; v2 code `detection_v2.py` /
`fixtures_v2.py` / `run_v2.py` pinned per rule 1.9). **Records:**
`v2_floor_correction/records/v2_records.jsonl`, sha256 `25db59b1…`,
**byte-stable ×2** (PMG-v2.4).

## What this corrects

The v1 detection floor was a hardcoded constant (`2⁻⁴⁰` Stage B, `2⁻⁸`
Stage D) — an axiom breach (Axiom 3 undeclared guard rail, Axiom 11
hardcoded constant; **TASKS_TO_REVISIT R14**). The corrected detection has
**no floor constant**: `below_detection` is the `T_token` of the typed
residue (design-doc Primitive 1, "underflow-to-zero, true ≠ 0"), the
observation map Φ reading **zero for a nonzero true value**, computed
per-operand from the operand + precision — the project's own dyadic-death
law (HR133/HR136), which the organ already carried as `dead_axis`.

- **float64 (CL-G4):** `below_detection` ⟺ `holonomy_float == 0 ∧ coupling ≠ 0`.
- **2-adic (CL-G8 floor box):** `below_detection_2adic` ⟺ `Φ₂(v,k) == 0 ∧ v ≠ 0` (i.e. `v₂(v) ≥ k`).

## Verdicts (both halves; all 5 cells == frozen pins)

| cell | role | v2 verdict | v1 (superseded) |
|---|---|---|---|
| `UNDERFLOW-WITNESS-ULP` | new witness (A) | **`below_detection`** | — |
| `V1-REGRADE-BOUND-BELOW` | v1 re-grade (B) | **`separated_clean`** | `below_detection` → **FLIP** |
| `V1-REGRADE-BOUND-ABOVE` | v1 re-grade (B) | `separated_clean` | `separated_clean` (consistent) |
| `2ADIC-UNDERFLOW-WITNESS` | new witness (A) | **`below_detection_2adic`** | — |
| `V1-REGRADE-FLOOR-2ADIC` | v1 re-grade (B) | **`nonarch_closed`** | `below_detection_2adic` → **FLIP** |

- **(A) the corrected verdict fires** at the genuine resolution boundary
  (Δ = 1 ULP → coupling −2⁻¹⁰⁴, float holonomy underflows to 0; v = 2¹²/3,
  v₂ = 12 ≥ k, Φ₂ reads 0). Authored witnesses that *exercise* the verdict
  (no constant defines it), documented as true-ULP / genuine-v₂ boundaries.
- **(B) the old verdict was wrong**, on v1 evidence **verbatim** (operands
  read read-only from the frozen fixtures): −2⁻⁴² is *above* float64's ULP
  2⁻⁵² (representable) → `separated_clean`; 3/5 is fully resolved at 12
  digits (Φ₂ = 1639 ≠ 0) → `nonarch_closed`. **Two flips** = the breach
  mislabeled representable/resolved cells as exhausted.
- **The cascade is pinned and load-bearing:** `below_detection` is a subset
  of `separated_accounted` (both have account ≠ 0). The control proves loose
  ordering reads the underflow witness as `separated_accounted` (T_token
  swallowed); the pinned order surfaces `below_detection`.
- **Zero `FAIL_*`** — the refute-row was armed (a witness failing to fire,
  or any FAIL, would mean the corrected design is wrong); it did not fire.

## Status moves

- **CL-G4 → DEMONSTRATED (corrected, v2).** Float underflow witness reads
  `below_detection` (cascade-pinned); v1 BOUND-BELOW flips to
  `separated_clean`; BOUND-ABOVE stays clean.
- **CL-G8 floor box → DEMONSTRATED (corrected, v2).** 2-adic underflow
  witness reads `below_detection_2adic`; v1 FLOOR-2ADIC flips to
  `nonarch_closed`. (CL-G8's closure + warrant-refusal legs were never
  floor-dependent and stood on v1.)
- The v1 verdicts for these cells are **SUPERSEDED-BY-v2** (flawed-floor).

## No-tamper (Will's ruling honoured)

The frozen v1 records are **byte-identical and untouched** — re-verified
this run: `stage_b/records/…` sha `a8147815…` UNTOUCHED, `stage_d/records/…`
sha `bbccba94…` UNTOUCHED, manifest `648975d0…` not edited. v1 is preserved
as recorded (flawed-floor) evidence; v2 is a separate emission. The breach
is demonstrated *on* v1, not *by editing* v1 — the HR133 "v1 preserved → v2"
precedent. (The manifest's informational `DETECTION_FLOOR_P=40` economics
probe remains in the frozen manifest; it gates no verdict and is left
untouched per no-tamper — noted, not used.)

## What this unblocks

Stage E (CL-G7 — boundary-inhabitation + the composed-gate) can now build on
the corrected `T_token` representation-exhaustion instead of the constant:
the composed-gate is *coupling-degeneracy ∘ representation-exhaustion*, so it
composes exactly this fix. **STOP at this report for Will's acceptance before
Stage E.**
