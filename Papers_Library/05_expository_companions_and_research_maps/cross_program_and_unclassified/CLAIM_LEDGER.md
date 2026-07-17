# WARP claim ledger (append-only)

Algebra arm of `the-shared-residual` (charter OPEN; geometry arm CLOSED + RATIFIED, HR138). Eval-tier; SPINE FENCED.

| Claim | Statement | Stage | Status | Evidence |
|---|---|---|---|---|
| CL-W1 | decidable core ([ANALYTIC]+confirm): away from the ÷0/0^neg locus, D_static(C) <=> C factors, biconditional with ZERO false verdicts on FX-W-A/C(non-transcendental)/E; independent gate D_dynamic vs the exact-ℚ referee on a path that never reads D_static | A | **NOT_YET_PROBED** | — |
| CL-W2 | type property ([MEASURED]): factorability reads the operation TYPE, never the realised residue / float-lane value / operand-cancellation exposure; AST-seam asserts the verdict path's independence; UNDERFLOW-WITNESS-ULP cited (total cancellation, still factors) | A | **NOT_YET_PROBED** | — |
| CL-W3 | the Richardson wall (split-graded): FX-W-D shows D_static does-not-factor / D_dynamic factors-after-simplification, the split coinciding with expression-equality (one declared oracle call); fixture split [MEASURED], general semi-decidability [ANALYTIC] (Richardson 1968), never claimed measured | A | **NOT_YET_PROBED** | — |
| CL-W4 | additive over free modules ([ANALYTIC]+confirm): for every free ℚ-module carrier (FX-W-E) additive reconstruction closes against the independent referee, ZERO failures; T,v in M => T-v in M; independent gate = exact-ℚ truth off the residue path | B | **NOT_YET_PROBED** | — |
| CL-W5 | KEYSTONE — the quotient edge (make-or-break): on ℙ¹(ℚ) additive reconstruction is ill-defined (representative-dependent residue), PGL₂/Möbius is the named native reconstruction; ⊕ is additive iff the carrier is a free ℚ-module — locates the family edge (a boundary, not a pass). Additive-failure half graded [ANALYTIC] (§10.5; foregone on ℙ¹) | B | **NOT_YET_PROBED** | — |
| CL-W6 | (deliberately PARTIAL) quotient / token-boundary coverage: ℙ¹ is THE representative quotient; other quotients are a fenced extension; the ÷0 token-boundary is touched (FX-W-B totality) but the general token-boundary ⊕ stays a separate brief. Full coverage never claimed | cross | **NOT_YET_PROBED** | — |

## Status moves (append-only log)

**Stage A — applied 2026-06-14 (Will's GO; verification reproduced). Prior rows above are unchanged.**

| Claim | Move | Stage | Evidence |
|---|---|---|---|
| CL-W1 | NOT_YET_PROBED → **DEMONSTRATED** | A | PMW.1 PASS 6/6 — `D_static == D_dynamic == "factors"` on FX-W-A/C, independent commuted-tree referee matched `true_q` exactly in ℚ; K-W1/K-W2 not fired. records sha256 `c540c1e0860406336e0639e015f0cf9cad9be7d1baa2c3da37583b9a28517c82`; prereg pin `b2790acf…`. |
| CL-W2 | NOT_YET_PROBED → **DEMONSTRATED** | A | PMW.2 PASS — AST-seam clean (verdict path reads no float/residue/exposure), `D_static` verdict point-invariant, UNDERFLOW-WITNESS-ULP (FXWC1) float `0.0` yet factors (R_exact-by-composition); factorability ≠ float-lane exactness. records sha256 `c540c1e0…`. |
| CL-W3 | NOT_YET_PROBED → **DEMONSTRATED** | A | PMW.3 PASS 3/3 — FX-W-D split `D_static` does_not_factor / oracle factors-after-simplification coincides with expression-equality; fixture split [MEASURED], general semi-decidability [ANALYTIC] (Richardson 1968), not measured. K-W4 not fired. records sha256 `c540c1e0…`. |

**Stage B — applied 2026-06-14 (Will's GO; verification reproduced incl. independent Möbius recompute). Prior rows unchanged.**

| Claim | Move | Stage | Evidence |
|---|---|---|---|
| CL-W4 | NOT_YET_PROBED → **DEMONSTRATED** | B | PMB.1 PASS 3/3 — free-module additive reconstruction `v ⊕_add ρ == TRUE` closes on ℚ, ℚⁿ, ℚⁿˣᵐ (residue in-module; recovers the pinned exact-ℚ TRUE off the residue path), zero failures; [ANALYTIC]+confirm. K-W3 not fired. records sha256 `71ca79585b7959f5c494f392c3fa0a5bf1baf235510c010da9497402091500d5`; prereg pin `b4b9d9dd…`. |
| CL-W5 | NOT_YET_PROBED → **DEMONSTRATED** | B | KEYSTONE — **located boundary: ⊕ additive iff free ℚ-module; additive-failure [ANALYTIC], Möbius reconstruction [MEASURED]**. On ℙ¹(ℚ) the additive residue between representatives differs while cross-multiply (a·d==b·c) certifies the same point; the PGL₂/Möbius action maps equal→equal and moves the point. K-W3 not fired. records sha256 `71ca7958…`. |
| CL-W6 | (no move) → **PARTIAL (by design)** | cross | Coverage statement, not a battery claim: ℙ¹ is THE representative quotient; other quotients + the general token-boundary ⊕ are fenced extensions. Full coverage never claimed. |

Kill conditions armed (brief §4):
- **K-W1** — HALT (campaign dies): any pure-R_exact rational-op DAG (away from ÷0/0^neg) that D_dynamic finds does NOT factor. The decidable-core foundational claim is false; the campaign stops, chain preserved.
- **K-W2** — HALT (arm): D_static != D_dynamic on the rational-op class in either direction (a false verdict). The decider is broken; the arm halts.
- **K-W3** — REFUTE-ROW (continue — the make-or-break): CL-W5 fails — either additive ⊕ DOES descend on ℙ¹, or a free ℚ-module carrier fails additive in CL-W4. Halt the row, preserve the witness, name what reconstructs instead, reduce scope, keep the chain.
- **K-W4** — REFUTE-ROW: CL-W3 — the D_static/D_dynamic split does NOT coincide with expression-equality (the wall is located elsewhere than predicted).
- **K-W5** — DESCOPE (pre-declared): the ℙ¹/PGL₂ parent build or a quotient extension exceeds the Stage-0 budget -> fence per the pre-registered schedule, never silently.

SPINE FENCE (brief §9; the manifest's verbatim fence, carried). This arm MEASURES factorability and the ⊕-carrier on named fixtures. It carries NO claim that the coupling/account primitive is the universal substrate spine, and NO cross-domain G-claim. [INFERENCE] (cella-as-trunk) stays [INFERENCE]. WARP closing satisfies the ALGEBRA-ARM HALF of the charter only — it is NOT the last gate to the spine; the unfence is a charter-level disposition reserved to Will, and requires BOTH arms to survive AND a separate spine-confirmation (SPINE_STATUS.md HR138). Eval-tier only; no substrate promotion in-campaign (Rule 1.2).
