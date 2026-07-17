# STAGE REPORT — shape_witness feasibility gate (queue item 2)
**Date:** 2026-07-02 · **Predecl pin:** `967c7909450ef944` (frozen pre-battery) · **Records sha:** `39bed5552c805f4d`, **byte-stable ×2** · **Substrate:** [CONTAINER] `witness_battery.py`, exact ℚ on every verdict path; clause-embedding gate + predecl-pin gate enforced at runtime; projector construction gated by rank(1/4/5)+idempotency+partition-of-identity (a Specht-character error cannot pass silently).

## Headline
**The Part III dimension threshold is now realized by an explicit certificate at n=5.** A pair of rational Hessians at the same regular gauge has its **entire σ-spectrum tied exactly** (all orders — stronger than the r≤4 minimum the dimension count requires) while the shape components differ in all 10 coordinates, and a **degree-2 exact-ℚ shape-moment invariant separates the pair.** The scalars are blind here by theorem; the tensor readout sees it by construction.

## Mechanism (the reusable part)
`H2 = Rᵀ H1 R` with `R = Cayley(uvᵀ−vuᵀ)`, `u,v ⊥ g`: R is exact-ℚ orthogonal with `Rg = g`, so `P = I − ggᵀ/q` commutes with R and the tangential operators are similar ⟹ **σ_r tied for ALL r** [PROVEN, and certified twice independently below]. Nothing in the construction protects the Sₙ-adapted isotypic components — and nothing did.

## Verdicts (graded mechanically)
| item | clause outcome | evidence |
|---|---|---|
| C-1 identity control | PASS | all readings equal on (H1,H1) |
| C-2 gauge control | PASS | `Ê_r`, O, shape all invariant under `H → H + gbᵀ + bgᵀ` (session gauge lemma confirmed numerically-exactly) |
| C-3 informativeness | PASS | perturbed pair: `Ê_r` differ — detector non-vacuous |
| P-W1 | **PASS** | `Ê_r(H1) = Ê_r(H2) = (244, −2620, −7912, −1384)`, r=1..4, exact |
| P-W2 (independent route) | **PASS** | q-cleared charpolys of `P·Hᵢ·P` identical in ℚ[z] |
| P-W3 | **PASS** | δ_shape ≠ 0 in **10/10** coordinates |
| P-W4 | **PASS on primary** | `m2_shape: 68/3 vs 19914692/1366875` (m3_shape also separates: `256/3 vs 4365368704/184528125`) |

Recorded, non-verdict: `m2_std` (314/15 vs 31010758/1366875) and `m2_triv` (32/5 vs 5408/1125) also move under conjugation — the whole isotypic moment vector is A-sensitive, not just the shape slot. **Correction filed in-session:** Claude's chat reading of run 1 attributed the m2_triv values to m2_shape; corrected here before banking (verify-before-assert applies to reading one's own output).

## Rigour ladder
The witness pair: **Level 7** (independently checkable exact-ℚ certificate; two independent σ-equality routes; reproducible, byte-stable ×2). The general statement "g-stabilizing conjugation produces σ-tied shape-separated pairs for all n≥5, generic data": **Level 4** (formulated; one instance). The completeness program (invariants of `π_shape(O)` completing the σ-tower through 8.1′): untouched by today — this was the feasibility gate.

## Scoped closeout
Holds within the tested space: n=5, `g=(1,2,3,5,7)`, the pinned H1 and primary A. Untested: genericity across (g, H1, A); n>5; whether m2_shape separates σ-tied pairs *generically* or this pair is lucky; behavior on the equal-g_i degenerate locus. Kill conditions K-2/K-3 never fired; backup rotations A2/A3 unused.

## GATE RECORD — 2026-07-02
Will confirmed ("confirmed", verbatim) following the four-part grounding statement in-session. Delta #1 filed to dashboard Part III in the same breath; carry block updated; flagship brief UNBLOCKED per the predecl status-move rule (not yet opened — awaiting Will's theatre call vs the weld routes).

## Proposed status moves (Will's desk — nothing canonical until signed)
1. Dashboard PROPOSED delta (Part III addendum): *"n=5 explicit witness [CERTIFIED, ×2 sha 39bed555]: full σ-spectrum tied by g-stabilizing conjugation (all orders, similarity mechanism [PROVEN]), shape components differ 10/10, separated by the degree-2 invariant m2_shape = ‖π_shape(O)‖². Dimension threshold realized constructively; the σ-tower's proven hole is now exhibited, not just counted."*
2. Queue-2 campaign brief unblocked per the predecl status-move rule — the flagship (completeness via 8.1′, generic-g theorem, n≥5 family statement) needs a Movement-1 brief + Stage −1 prior-art pass before anything freezes.
3. Defect chains this stage: **one** — the chat-side field misread (corrected same session, pre-banking; zero defects in the battery itself).
