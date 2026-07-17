# Geometry Arm — Stage D Report (three-account balance + non-archimedean)

**Date:** 2026-06-14 (machine date). **Authority:** brief §4 Stage D +
Will's freeze and battery GO ("accepted, stage d go"; the F9 "registered
measurement" framing for CL-G6 blessed). **Manifest:** FROZEN, pin
`648975d0…`. **Stage-D prereg:** FROZEN (`stage_d/prereg.json`, pinned to
the frozen manifest; PMG-D clauses verbatim per rule 1.8; the new Stage-D
code `padic.py` / `fixtures_d.py` / `run_stage_d.py` pinned per rule 1.9).
**Records:** `stage_d/records/stage_d_records.jsonl`, sha256 `bbccba94…`,
**byte-stable ×2** (PMG-D.5).

## The non-archimedean account

Stages A–C probed two **archimedean** encodings of a real — dyadic
place-value and continued fractions. Both live at the single archimedean
place ∞; their agreement is robustness across *bookkeeping*, not across
*places*. Stage D adds the genuinely-different observation: a
**non-archimedean (2-adic)** account, governed by the ultrametric. The
kernel (`padic.py`) is stdlib `fractions` only (Axiom 11): the p-adic
valuation, `|·|_p` / `|·|_∞`, the 2-adic truncation `Φ₂(v,k)` of a 2-adic
integer, and the product formula.

## Verdicts

| Prediction | Verdict | Result |
|---|---|---|
| **PMG-D.1** three-account balance closes (CL-G6) | **PASS** | On every balance cell the three accounts close (value = observed + residue, exact ℚ; dyadic, CF, 2-adic) and the product formula `|v|_∞·|v|_2·∏_{p odd}|v|_p == 1` exactly in ℚ. Registered as a measurement (F9): the adelic shape is observed to close, not asserted as a discovery. |
| **PMG-D.2** the non-archimedean place is load-bearing | **PASS** | On every `v₂≠0` cell (BAL-1/2/3, v₂ = 2/3/3) dropping the 2-adic account leaves the archimedean-only product at 4, 8, 8 — **≠ 1**. The balance needs the non-archimedean place; two agreeing archimedean encodings are not "encoding-agnostic." |
| **PMG-D.3** non-archimedean closure + lattice-floor box (CL-G8) | **PASS** | NARCH-CLOSE: the 2-adic account closes (`v₂(R)=5 ≥ k=4`, within the floor) → `nonarch_closed`. FLOOR-2ADIC: residue `v₂=13 > 8` → `below_detection_2adic` (the non-archimedean analog of CL-G4). |
| **PMG-D.4** warrant refusal on holonomy extrapolation (CL-G8) | **PASS** | WARRANT-EXTRAP at out-of-grid (q,d)=(5,2) → `warrant_refused`; an in-grid query is warranted (the refusal is not vacuous). |
| **PMG-D.5** determinism | **PASS** | byte-stable ×2, sha `bbccba94…`. |

Tally: 6 records — 3 `balanced`, 1 `nonarch_closed`, 1
`below_detection_2adic` (refusal), 1 `warrant_refused` (refusal). Zero
`FAIL_balance`. **The refute-row (FAIL_balance) was armed; it did not fire.**

## Status moves (per the frozen STATUS_MOVE_RULES)

- **CL-G6 → DEMONSTRATED** — the three-account balance closes exactly in ℚ
  on every cell, and the non-archimedean place is shown load-bearing
  (archimedean-only breaks the balance). The product-formula shape is a
  **registered measurement** (F9; not asserted as a discovery — it is the
  known adelic product formula, used as the cross-place reconciliation
  check).
- **CL-G8 → PARTIAL (by design, DEMONSTRATED at the partial scope)** — a
  non-archimedean closure holds, the 2-adic floor box refuses below 2⁻⁸,
  and the warrant refusal fires on an out-of-grid holonomy query. **Full
  refusal/encoding coverage is NOT claimed** (the deliberate partiality).

## Honest scope (what CL-G6 is and is not)

The product formula is a **known theorem**, so "it closes" is not itself a
discovery — and CL-G6 does not pretend otherwise. Its content is twofold:
(1) the three-account organ computes all places in **exact ℚ** and they
reconcile, and (2) the non-archimedean place is **load-bearing** — the
precise, exact-ℚ statement that the 2-adic account carries information the
archimedean encodings cannot supply (drop it and the product ≠ 1). The full
adelic / product-formula structure beyond this registered measurement stays
**fenced** (brief §5; the F9 discipline — measure, never hunt).

## Scope held (the fences)

- **SPINE FENCE honored** (manifest, verbatim): Stage D is a *measurement*
  of cross-place reconciliation on named fixtures. **No spine claim, no
  cross-domain G-claim.** "Encoding-agnostic" is the navigation target
  FX-G-E tests, now with a genuinely non-archimedean place — not an
  asserted invariant. `[INFERENCE]` (Cella-as-trunk) stays `[INFERENCE]`.
- **Axiom 11** holds throughout: stdlib `fractions`, no `math`/`mpmath`/
  `sympy`, no hardcoded constants, exact ℚ.

## What Stage D establishes (and what is next)

The exact residue account survives the move from two archimedean encodings
to a genuinely non-archimedean place: the three accounts reconcile exactly
in ℚ, and the non-archimedean place is necessary (not decorative). The
2-adic account closes its own residue, refuses below its floor, and the
organ refuses to extrapolate the holonomy off the pinned grid.

**Next: Stage E** — boundary-inhabitation classification (Q3) + the
composed-gate (the conical blind spot: coupling-degeneracy ∘
representation-exhaustion), CL-G7. The **last stage of the geometry arm**.
**STOP at this report for Will's acceptance before Stage E.**
