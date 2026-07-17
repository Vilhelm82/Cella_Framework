# Geometry Arm — Stage A Report (holonomy lanes, exact ℚ)

**Date:** 2026-06-13 (machine date). **Authority:** brief §4 Stage A +
Will's freeze signature ("GO"). **Manifest:** FROZEN, pin
`648975d0…` (`results/coupling_holonomy/freeze_pins_sha256.json`).
**Prereg:** FROZEN (`stage_a/prereg.json`, pinned to the frozen
manifest; GRADER_CLAUSES verbatim per rule 1.8). **Records:**
`stage_a/records/stage_a_records.jsonl`, sha256
`b347566b436616b9a8e0a2e53ebf11d903021c415ca3804742d3dd241b2df76b`,
**byte-stable ×2** (PMG.4).

## Verdicts

| Prediction | Verdict | Result |
|---|---|---|
| **PMG.1** holonomy law, exact in ℚ, vs the independent referee | **PASS** | 9/9 live cells. Separable (`x+y`) holonomy == 0 exactly; the bilinear product (`x·y`) holonomy == −(Δx·Δy) exactly (closed cross-term); the nonlinear (`1/(x+y)`) holonomy reproduced by the independent transformed-tree referee exactly in ℚ. Reading gap == account gap. Referee matched on **every** cell. |
| **PMG.2** cross-encoding closure | **PASS** | The law holds across the **two genuinely-different encodings of one real** (dyadic analytic axis × continued-fraction algebraic axis) on every live cell — it indexes by the two refinement budgets, not by variables. |
| **PMG.3** typed refusals | **PASS** | Dead-axis cells refuse (`refusal=dead_axis`, verdict null), never certified — the live-points discipline as a typed refusal (Stage-0 control + organ). |
| **PMG.4** determinism | **PASS** | byte-stable ×2, sha `b347566b…`. |

Tally: 9 records — 3 `separable` (`x+y`), 6 `coupled` (`x·y`, `1/(x+y)`,
3 cells each). Zero FAIL. **K-G1 (campaign halt) and K-G2 (arm halt)
armed throughout; neither fired.**

## Status moves (per the frozen rules)

- **CL-G1 → DEMONSTRATED** — the holonomy law is exact in ℚ on every
  live cell and the independent referee matches exactly (a lane bug
  could not certify itself).
- **CL-G2 → DEMONSTRATED** — cross-encoding closure across dyadic ×
  continued-fraction.

## Scope held (the fences)

- **SPINE FENCE honored** (manifest, verbatim): this is a *measurement*
  of coupling-holonomy on named fixtures. **No spine claim, no
  cross-domain G-claim.** `[INFERENCE]` (Cella-as-spine) stays
  `[INFERENCE]`; the spine is confirmed only at charter level iff both
  arms survive.
- **CL-M4 NOT banked.** Stage A is exact-ℚ; it does **not** discharge
  the finite-precision coupling-vs-rounding separation. That is
  **Stage B's keystone (CL-G3)** — the fight exact ℚ sidesteps by
  construction.

## What Stage A establishes (and what it deliberately does not)

The coupling-as-holonomy law — coupling == the mixed second difference
of the exact residue; 0 iff additively separable; the exact cross-term
when coupled — is **DEMONSTRATED in exact ℚ across two refinement axes
that are different encodings of one real**. This is the
cross-representation lift of Arm M's operator-level result (Arm M ⊂
this; arrow `V4 → probe`). It is **evidence for**, not confirmation of,
the cella-as-trunk spine.

**Stage B is the real fight:** lift the battery off exact ℚ into
declared finite precision and separate the coupling-holonomy from the
arithmetic route fingerprint under the HR134 amendment-6 protection
predicate (CL-G3). The exact-ℚ probe could not reach it; the campaign
must. **STOP at this report for Will's acceptance before Stage B.**
