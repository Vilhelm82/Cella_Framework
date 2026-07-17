# Geometry Arm — Stage E Report (the last: boundary-inhabitation + the composed-gate)

**Date:** 2026-06-14 (machine date). **Authority:** brief §4 Stage E +
Will's freeze + battery GO; the composed-gate guard (2026-06-14) confirmed
and accepted. **Manifest:** FROZEN, pin `648975d0…`. **Stage-E prereg:**
FROZEN (`stage_e/prereg.json`, pinned to the frozen manifest; PMG-E clauses
verbatim per rule 1.8; the new Stage-E code `composed_gate.py` /
`fixtures_e.py` / `run_stage_e.py` pinned per rule 1.9). **Records:**
`stage_e/records/stage_e_records.jsonl`, sha256 `307e766b…`, **byte-stable
×2** (PMG-E.4).

## The composed-gate (event-based, per the guard)

Two distinct boundary primitives compose: **coupling-degeneracy** (the exact
coupling-holonomy vanishes — a fact of the object) and
**representation-exhaustion** (the observation map reads zero — a fact of
Φ). The gate fires on the EVENT `holonomy_float == 0` (resp. `Φ₂(v,k) == 0`)
and attributes via the **exact account/value** — never via a residue-branch
label. The event is **typing-neutral** (a fact of Φ regardless of `T_token`
vs `R_exact`-by-composition), so CL-G7 does not freeze the `below_detection`
typing — that reconciles at the close draft (**R15**). The exhausted
coupling `−2⁻¹⁰⁴` is a **normal, representable** float: working-precision
cancellation recovered exactly by the account, **not** line-151 underflow.

## Verdicts (7 cells == frozen pins; byte-stable ×2)

| Prediction | Verdict | Result |
|---|---|---|
| **PMG-E.1** the gate fires on the EVENT | **PASS** | The composed-gate reads `(exhaustion_event, coupling-degeneracy)` and attributes by the exact account; the reading carries no `below_detection`/`T_token` field. `attributed_by = exact_account`. |
| **PMG-E.2** the conical blind spot is real and attributed | **PASS** | `COMPOSED-DEGENERATE` (coupling 0) and `COMPOSED-EXHAUSTED` (coupling −2⁻¹⁰⁴) give **byte-identical float holonomy (0)**; the account is the sole attributor (0 vs −2⁻¹⁰⁴). The first measured composed-gate failure. `NOT-AT-GATE` (holo_f ≠ 0) doesn't fire. 2-adic analog: `Φ₂ = 0` for v ≠ 0. |
| **PMG-E.3** inhabitation classified by tier | **PASS** | `inhabited_sharp` (3/8, death budget 3); `inhabited_conservative` (1/3, non-dyadic limit — typed refusal); `un_inhabitable` (1+2⁻⁶⁰, death budget 60 > lattice precision 53 — typed refusal). Lattice precision DERIVED from `sys.float_info.mant_dig`. |
| **PMG-E.4** determinism | **PASS** | byte-stable ×2, sha `307e766b…`. |

Tally: 7 records — 5 verdicts (degenerate / exhausted / not_at_gate /
exhausted_2adic / inhabited_sharp) + 2 typed refusals (conservative,
un_inhabitable). Zero `FAIL`. The refute-row (account-not-closing /
broken blind spot) was armed; it did not fire — the account closed on
every composed cell (CL-G3 holds).

## CL-G7's headline (and its formal half — the control)

The two gate cells prove the account **CAN** separate the two boundary
primitives. CL-G7's headline is the stronger claim — that the account is the
**SOLE** channel — and its formal half is the pinned informativeness control
(**`account_is_load_bearing_control_fails`**, in the frozen prereg): a
**float-only** reading returns the SAME verdict (`degenerate(float-only)`)
for both cells, because both read `holonomy_float == 0` — it CANNOT separate
them. The account-based reading returns distinct verdicts. So no channel but
the exact account survives the projection: **the account is not an
enhancement at the composed gate; it is the only thing that works.**

## Status moves (per the frozen STATUS_MOVE_RULES)

- **CL-G7 → DEMONSTRATED** — (a) the composed-gate fires on the event and
  attributes via the account; (b) the conical blind spot is real (identical
  float readings, opposite exact couplings, the account the sole attributor,
  and the control proves float-only cannot separate); (c) the three
  inhabitation tiers classify as pinned.

## Scope held (the fences)

- **SPINE FENCE honored** (manifest, verbatim): Stage E is a *measurement* of
  the composed-gate and inhabitation on named fixtures. **No spine claim, no
  cross-domain G-claim.** `[INFERENCE]` (Cella-as-trunk) stays `[INFERENCE]`.
- **Event-based, typing-neutral (R15):** CL-G7 does not depend on the
  `below_detection` typing; the close-draft reconciliation (B/D/E) is not
  pre-empted.
- **No magic constants:** the lattice precision is `sys.float_info.mant_dig`;
  the exhaustion is the Φ-event, not a floor (R14 stays corrected).

## What Stage E closes

The geometry arm is **fully graded**: all eight CL-G claims resolve —
CL-G1/G2 (A), CL-G3 (keystone) / G4 (B; G4 corrected via the v2
floor-correction), CL-G5 (C), CL-G6 / G8-partial (D; G8 floor box corrected
via v2), and **CL-G7 (E)**. The composed-gate is where the arm's thesis pays
off in one cell: two boundary primitives project to a single float observable
(0), and the exact account is the only channel that carries the distinction.

**Next: the geometry-arm CLOSE DRAFT** — carry all eight claims, land R15's
`below_detection` typing reconciliation across B/D/E in one pass, and inventory
the findings. The charter still awaits the algebra arm (WARP) before the spine
unfences. **STOP at this report for Will's acceptance before the close draft.**
