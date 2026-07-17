# WAVE0 REPORT — Deficit Engine calibration (SN-2)
**Date:** 2026-07-02 · **Predecl pin:** `c6fd7018a4602209` (frozen pre-battery) · **Records sha:** `74720504dfd88af7`, **byte-stable ×2** · **Substrate:** [CONTAINER] `wave0_battery.py`, exact ℚ on every verdict path; clause-embedding + predecl-pin gates enforced at runtime.

## Headline
**Engine layer 1 is CERTIFIED at calibration.** The deficit computation reproduced both pinned known-blindnesses with exact certificates — and on our own σ-row it did more than count: the six hidden-group directions sit *exactly* inside the Jacobian kernel over ℚ, so the deficit is fully accounted by the conjugation group at the pinned point. The searchlight turns on and correctly illuminates the two objects we already knew were in the dark.

## Verdicts
| item | outcome | measured |
|---|---|---|
| P-A1 | **PASS** | rank dΦ_σ = 4 at O* and O**; deficit = **6** |
| P-A2 (mechanism-match) | **PASS** | tangent span = **6** exactly; `Jacobian·δO_k = 0` exactly, all 6 generators — deficit fully group-accounted `[CERTIFIED]` |
| P-B1 | **PASS** | c₁ ≡ 0; rank 3 at m=4 (deficit **3**), rank 4 at m=5 (deficit **6**) — matches the pre-freeze recount `(m−1)(m−2)/2` |
| P-B2 (imported anchor) | **PASS** | K₁,₄ vs C₄⊔K₁: char polys exactly equal in ℤ[λ]; orbits distinct (degseq (4,1,1,1,1) ≠ (2,2,2,2,0)) |
| C-1 / C-2 | PASS | identity summary deficit 0; row-A rank identical ×2 points |

## Notes in ink
- **Pre-freeze recount** (covenant #3): the graph-row prediction was corrected from chat-draft "deficit 5 at m=5" to **6** before freezing — `tr(W) ≡ 0` on the zero-diagonal stratum removes one coefficient. The recount discipline caught it exactly where it should.
- **Defect (1, tooling):** first battery run crashed on JSON-serializing sympy Integers (plus one junk dead-code expression) — caught pre-grading by the run itself, fixed, rerun clean. Zero mathematical defects.
- **Row-B layer-2 is deliberately OPEN** (per SN-2): the graph deficit of 6 is *not* explained by orthogonal conjugation (destroys the zero diagonal). Whatever sweeps those fibers is wave-1's first genuinely open mechanism question — a known-blindness row already producing an unknown-mechanism question is the engine behaving as designed.

## Scoped closeout
Holds within the tested space: pinned points, n=5 σ-row, m∈{4,5} graph rows, generic-rank readings at 2 points (row A) / 1 point per m (row B). Untested: rank behavior on degenerate strata; any new-territory row; layer 3/4 machinery outside row A (where shape_witness already supplies them).

## Status moves (per predecl rule)
1. Engine L1 = **CERTIFIED at calibration**; SN-2 gate CLEARED.
2. **Wave-1 (row harvest — new territory) is now eligible**: requires its own predecl with a pinned row list (each row carrying its field-practice column) and Will's Go. Candidate rows queued from the gap atlas discussion: coupled-system Jacobian spectra vs species permutation; GTD response summaries vs the thermodynamic gauge; correspondence single-degree vs the full role-resolved spectrum; graph-row layer-2 mechanism hunt.
3. Nothing here is canonical until Will signs; flagship rulings and weld route remain open and untouched.
