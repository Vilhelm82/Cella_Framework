# Geometry Arm — Stage B Report (the keystone: finite-precision separation)

**Date:** 2026-06-13 (machine date). **Authority:** brief §4 Stage B +
Will's freeze signature and battery GO ("accepted GO", with the
reframed CL-G3 blessed). **Manifest:** FROZEN, pin `648975d0…`
(`results/coupling_holonomy/freeze_pins_sha256.json`). **Stage-B
prereg:** FROZEN (`stage_b/prereg.json`, pinned to the frozen manifest;
PMG-B clauses verbatim per rule 1.8; the new Stage-B code
`finite_precision.py` / `fixtures_b.py` / `run_stage_b.py` pinned per
rule 1.9). **Records:** `stage_b/records/stage_b_records.jsonl`, sha256
`a8147815640536…`, **byte-stable ×2** (PMG-B.4).

## The separator

In float64 the loop-holonomy carries two contributions at once: the
real coupling-holonomy (Stage A's exact-ℚ value) and the arithmetic
**route fingerprint** — the rounding committed while computing it.
Stage B computes the holonomy in float64 carrying an **exact
error-free-transform account** ρ (TwoSum / TwoProduct via `math.fma`),
so that on every cell

> **coupling (exact ℚ)  ==  holonomy_float  +  account**

closes exactly in ℚ. The account *is* the separator. The HR134
amendment-6 protection predicate (L1–L4) reads the operation structure
and predicts when the fingerprint is provably zero.

## Verdicts

| Prediction | Verdict | Result |
|---|---|---|
| **PMG-B.1** the separator closes (CL-G3); predicate **sound** | **PASS** | On all 8 cells `coupling == holonomy_float + account` exactly in ℚ. No protected cell carries a nonzero fingerprint — the predicate's guarantee (protected ⟹ fingerprint 0) holds on every cell. |
| **PMG-B.2** coincidental class **named, not banked** | **PASS** | The two `COINC` cells round (not predicate-protected) yet their four corner residues are common-mode and cancel → fingerprint 0; reported as `separated_coincidental`, distinct from a protected read and **not** banked as CL-M4. The derived witness (0.1 = RN(1/10)) is genuine rounding: fingerprint −1/2⁵⁸ ≠ 0, coupling recovered exactly by the account. |
| **PMG-B.3** the boundary is distinct (CL-G4) | **PASS** | The protected boundary pair straddles the pinned floor 2⁻⁴⁰: `BOUND-ABOVE` (coupling −2⁻³⁸) certifies (`separated_clean`); `BOUND-BELOW` (coupling −2⁻⁴²) refuses (`below_detection`). Both protected (no rounding) — exhaustion isolated from the fingerprint. |
| **PMG-B.4** determinism | **PASS** | byte-stable ×2, sha `a8147815…`. |

Class tally: 8 records — 4 `separated_clean` (PROT-1/2/3 + BOUND-ABOVE),
2 `separated_coincidental` (COINC-1/2), 1 `separated_accounted`
(ROUND-WITNESS-0.1), 1 `below_detection` (BOUND-BELOW). Zero FAIL.
**K-G3 (refute-row) armed throughout; it did not fire** — the account
closed on every cell and no protected cell carried a fingerprint.

## Status moves (per the frozen STATUS_MOVE_RULES)

- **CL-G3 → DEMONSTRATED** — the account closes on every cell, the
  predicate is sound on every cell (no protected cell with a nonzero
  fingerprint), the derived witness shows genuine accounted rounding,
  and protected cells read clean. **Stated honestly: separation is via
  the EFT account; the predicate is a *sound* (not complete) guarantee;
  the coincidental class is named.** This is richer than the brief's
  clean two-sided phrasing — see the finding below.
- **CL-G4 → DEMONSTRATED** — the protected boundary pair certifies
  above / refuses below the pinned floor; the boundary is a distinct
  event from the coupling value (both boundary cells are protected, so
  the only reason to refuse below is exhaustion, not rounding).

## The finding — the predicate is sound, not complete (the CL-M4 cousin)

The brief framed CL-G3 as a clean two-sided biconditional: predicate
holds ⟺ fingerprint zero. **The battery does not support the reverse
direction, and that is the result, not a defect.** `COINC-1` and
`COINC-2` are *not* predicate-protected (their corner products need
more than 53 bits) yet their fingerprint is exactly zero, because the
four corner residues are **common-mode and cancel in the mixed second
difference**.

This is the **finite-precision reproduction of Arm M CL-M4** ("corner
deviations are common-mode") surfacing inside the holonomy — the
reproduction the reframe brief said was *owed and must not be banked
from the exact-ℚ result*. Stage B reaches it on its own evidence, so it
is recorded as DEMONSTRATED-here, not inherited:

- **`separated_clean`** — predicate-protected; fingerprint 0; coupling read clean. *(The sound direction.)*
- **`separated_coincidental`** — not protected, but common-mode corner residues cancel → fingerprint 0. *(The CL-M4 finite-precision cousin. A named class, not a failure, not a clean read.)*
- **`separated_accounted`** — not protected; fingerprint ≠ 0; coupling **recovered** exactly by adding the account. *(The genuine-rounding witness, 0.1 = RN(1/10).)*
- **`below_detection`** — |coupling| below 2⁻⁴⁰ (CL-G4; isolated from rounding).

So the honest CL-G3 is **"the coupling-holonomy is separable from the
route fingerprint in finite precision via the exact EFT account; the
protection predicate is a sound guarantee of a clean read; coincidental
common-mode cancellation is a named third class."** The predicate is
how you *certify* a clean read in advance; the account is what makes the
separation *hold* in every case, certified or not.

## Scope held (the fences)

- **SPINE FENCE honored** (manifest, verbatim): Stage B is a
  *measurement* of finite-precision separability on named fixtures. **No
  spine claim, no cross-domain G-claim.** `[INFERENCE]` (Cella-as-trunk)
  stays `[INFERENCE]`; the spine is confirmed only at charter level iff
  both arms survive.
- **CL-M4 not banked, reproduced.** The coincidental class is graded on
  Stage B's own battery (the float corner residues, made exact by the
  EFT), not lifted from Arm M's exact-ℚ result. The lineage note
  (CL-M4 → this) is provenance, not a transplant of the verdict.
- **Account = HR132 EFT; predicate = HR134 amendment-6.** Both are
  graded prior wins consulted as design references (Stage −1 audit);
  the `(q,d)`-axis holonomy operator over them is the new object.

## What Stage B establishes (and what is next)

The keystone holds: **in declared finite precision, the coupling-holonomy
is separable from the arithmetic route fingerprint — exactly, on every
cell — by the EFT account, with the HR134 protection predicate as a
sound advance certificate and coincidental common-mode cancellation as a
named class.** This is the test the exact-ℚ probe sidestepped by
construction (Stage A), now passed off exact ℚ. It is **evidence for**,
not confirmation of, the cella-as-trunk spine.

**Next: Stage C** — add the symbolic axis and the Richardson refusal,
and show the refusal localises to the symbolic coordinate while the
analytic and algebraic accounts stay sharp (CL-G5). **STOP at this
report for Will's acceptance before Stage C.**
