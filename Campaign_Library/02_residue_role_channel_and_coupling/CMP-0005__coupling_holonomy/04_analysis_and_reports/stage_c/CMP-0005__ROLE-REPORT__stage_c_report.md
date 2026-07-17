# Geometry Arm — Stage C Report (the symbolic axis: Richardson refusal localisation)

**Date:** 2026-06-14 (machine date). **Authority:** brief §4 Stage C +
Will's ruling ("additive complements the goal, decisively. Freeze it for
CL-G5 as the positive fitness demonstration; … the multiplicative cell
goes in as the negative control, pinned to contaminate"). **Manifest:**
FROZEN, pin `648975d0…`. **Stage-C prereg:** FROZEN (`stage_c/prereg.json`,
pinned to the frozen manifest; PMG-C clauses verbatim per rule 1.8; the
new Stage-C code `symbolic.py` / `fixtures_c.py` / `run_stage_c.py` pinned
per rule 1.9). **Records:** `stage_c/records/stage_c_records.jsonl`, sha256
`5e9caa41…`, **byte-stable ×2** (PMG-C.5).

## The symbolic axis

A third refinement axis is added to the analytic (dyadic, q) × algebraic
(continued-fraction, d) pair: a **symbolic** axis whose residue is a
symbolic identity to be decided. The decision kernel is a declared,
terminating canonical form — the **multivariate polynomial normal form
over ℚ** in indeterminates `{x} ∪ {each distinct uninterpreted subterm}`.
Axiom 11 is honoured: sin / cos / exp / ln are **uninterpreted** symbols,
never evaluated numerically; no `math` / `mpmath` / `sympy` import; no
hardcoded constants. Axiom 6 is honoured (typed zero) with three **distinct**
outcomes: `identity_zero` (proven), `detected_nonzero` (decidable, in ℚ[x]),
`richardson_undecidable` (a nonzero normal form carrying a transcendental
symbol — the constant problem is in Richardson's undecidable class; refuse).

## Verdicts

| Prediction | Verdict | Result |
|---|---|---|
| **PMG-C.1** decidable column resolves exactly | **PASS** | The poly identity `(x+1)²−x²−2x−1` and the formal-transcendental identity `sin·(cos+1)−sin·cos−sin` resolve to `identity_zero`; the transcendental-free non-identity `x²+1` to `detected_nonzero`. Numeric (q,d) account `coupled` and sharp on every cell. |
| **PMG-C.2** Richardson refusal localises (additive; keystone) | **PASS** | `sin²+cos²−1`, `exp(x)exp(−x)−1`, `ln(exp(x))−x` each yield a typed `richardson_undecidable` refusal on the symbolic coordinate, while the numeric (q,d) holonomy stays exact ℚ and constant-offset invariant — a clean detector. The refusal does **not** bleed. |
| **PMG-C.3** typed-zero discipline (Axiom 6) | **PASS** | The three outcomes are distinct and never conflated; a transcendental nonzero normal form is never reported `detected_nonzero`. The naive no-guard classifier (control) mis-certifies `sin²+cos²−1` — proving the Richardson guard is load-bearing. |
| **PMG-C.4** detection boundary (multiplicative negative control) | **PASS (contaminates as pinned)** | The **same** Richardson factor multiplied into the coupling survives the mixed difference: the holonomy becomes `S·holonomy_g` and is handed an undecidable factor. The organ **refuses** the holonomy (`holonomy_entangled_undecidable`, verdict null, refusal recorded), never certifying a clean ℚ value. |
| **PMG-C.5** determinism | **PASS** | byte-stable ×2, sha `5e9caa41…`. |

Class tally: 7 records — 3 `symbolic_certified_sharp`, 3
`symbolic_refused_localised`, 1 `holonomy_entangled_undecidable` (the
negative control, recorded as a typed refusal). Zero `FAIL_bleed`.
**K-G4 (refute-row) armed throughout; it did not fire** — no additive
cell let the symbolic refusal touch a decidable numeric account.

## Status moves (per the frozen STATUS_MOVE_RULES)

- **CL-G5 → DEMONSTRATED** — on the additive structure (the positive
  fitness): every decidable cell resolves exactly with a sharp numeric
  account, and every additive Richardson cell refuses-localised (typed
  refusal on the symbolic coordinate, numeric holonomy exact + offset-
  invariant, a clean ℚ detector). **And the boundary holds**: the
  multiplicative negative control contaminates as pinned — the holonomy is
  handed the undecidable factor and is refused, never falsely certified.

## The asymmetry (Will's detection ruling, on the record)

The two models are **not symmetric**, and that is the result that makes
CL-G5 non-vacuous:

- **Additive** — the symbolic term is constant across (q,d), so it cancels
  in the mixed second difference exactly as TRUE does. The holonomy stays a
  clean ℚ value and remains a working **early-warning detector** of
  coupling, no matter that the symbolic identity is undecidable. The
  undecidability is quarantined on the symbolic coordinate.
- **Multiplicative** — the symbolic factor `S` survives the mixed
  difference; the holonomy becomes `S·holonomy_g`, with `S` Richardson-
  undecidable. The holonomy is **handed an undecidable factor**; deciding
  even whether it is zero requires resolving the transcendental identity.
  The honest organ refuses the holonomy rather than certify a clean value.

So refusal localisation is a property of the **additive (added-axis)
structure** — not a universal claim. The negative control draws that
boundary on the assessment's own evidence: change the structure and the
detector property is genuinely lost. (This is **not** a K-G4 event: the
contamination is genuine and correct, not the false bleed K-G4 guards
against. The clean coupling holonomy is preserved as a sub-quantity in the
record, so nothing is lost — it simply cannot be read off the entangled
object.)

## Scope held (the fences)

- **SPINE FENCE honored** (manifest, verbatim): Stage C is a *measurement*
  of refusal localisation on named fixtures. **No spine claim, no
  cross-domain G-claim.** `[INFERENCE]` (Cella-as-trunk) stays `[INFERENCE]`.
- **Axioms 6 & 11 are the substance, not decoration**: the symbolic kernel
  decides only the polynomial-identity sub-problem and refuses outside it;
  the transcendentals are uninterpreted; the refusal is principled, not a
  hidden capability gap.

## What Stage C establishes (and what is next)

A symbolic refinement axis can be added to the exact-ℚ holonomy account
**without the symbolic axis's undecidability reaching the analytic/algebraic
account** — provided it enters additively. The Richardson refusal is typed
and localised; the holonomy remains a clean detector. The boundary is drawn
on the assessment's own evidence: a multiplicative entanglement hands the
holonomy an undecidable factor, and the organ refuses it.

**Next: Stage D** — the three-account balance + at least one non-archimedean
(2-adic) encoding (CL-G6, CL-G8). **STOP at this report for Will's
acceptance before Stage D.**
