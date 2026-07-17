# REALFIBER PROBE-2 REPORT — the bridge attempt, the wall, and the theorem the wall handed us
**Date:** 2026-07-02 · **Predecl pin:** `9f706c1a74a21317` · **Records:** probe-2 numeric sha `848b8d8eca916edf` byte-stable ×2 (after seed fix, defect below); path certificate sha `99fd1859a6e04214` byte-stable ×2 · **Substrate:** [CONTAINER] (predecl said box-preferred; preference, not requirement — noted openly).

## Numeric probe, graded per the frozen rules
120 runs (20 starts × 3 schedules × 2 directions): **0 bridges; best distance 1.8930 against an initial gap of 2.0; 60 runs at step cap, 31 stalled.** Mechanical grade per the frozen outcome typing: not A (no bridge); not clean B (caps present) → **INCONCLUSIVE-budget as graded.** The mechanism extraction below shows the caps/stalls are STRUCTURAL, not budgetary — the flows were confined by theorem — but the frozen grader's verdict stands as written; no post-hoc retyping.
**Defect (1, tooling, in ink):** first battery pair failed byte-stability ×2 — per-run seeds were derived through Python's process-salted `hash()`. Fixed to a deterministic map; reruns byte-identical. The qualitative picture (0 bridges, ~1.9 floor) was unchanged across all four runs; the gate still failed as a gate should.

## Mechanism extraction (from the stall geometry) — then certification
The spectrum {2,0,0,0,−2} forces rank 2: every fiber point is
```
W = 2uuᵀ − 2vvᵀ ,   u ⊥ v orthonormal          [spectral decomposition, ±2 simple]
diag(W) = 0  ⟺  uᵢ² = vᵢ²  for all i            [Lemma-1c, symbolic]
```
Writing `uᵢ = εᵢcᵢ, vᵢ = δᵢcᵢ` (cᵢ ≥ 0, signs on active vertices): `W_ij = 2cᵢcⱼ(εᵢεⱼ − δᵢδⱼ)`, which vanishes unless `sᵢsⱼ = −1` for `s = εδ` — **every fiber point has support BIPARTITE between the two s-classes**, with the class weights forced to 1/2 each (`Σsᵢcᵢ² = 0`, `Σcᵢ² = 1`). Sign patterns are locally constant where all cᵢ ≠ 0 ⟹ **the all-active smooth pieces are bipartition-locked; changing the partition requires passing a vertex through cᵢ = 0** — a singular event. The star lives in the (1|4)-piece; the cycle has vertex 4 inactive and partition (2|2). The flows, confined to the star's smooth piece by construction, converged to the piece's distance floor (~1.89) and could not cross. **The numeric wall was the measurement of a real geometric separation** [floor value: EMPIRICAL; the locking mechanism: PROVEN by the sign-continuity argument].

## The certified path (the answer, for the pair)
Explicit 3-stage path, linear-in-t in c²-coordinates, ALL_PASS symbolically ×2 (sha `99fd1859`):
```
Stage 1: park vertex 4        c₄² : 1/8 → 0        (leaf exits; partition (1|4) → (1|3))
Stage 2: park vertex 2        c₂² : 1/6 → 0        (partition (1|3) → (1|2))
Stage 3: revive vertex 2 in the OTHER class; shrink c₀   →  partition (2|2), endpoint = C₄⊔K₁ exactly
```
Certified: Lemma-1 eigen/diag identities symbolic in full generality; stage constraints (Σc² ≡ 1, u·v ≡ 0, nonnegativity) identical in t; boundary continuity; endpoints equal the adjacency matrices EXACTLY; interior membership spot-certified exactly.
**VERDICT: K₁,₄ and C₄⊔K₁ are joined by an explicit continuous path inside the real zero-diagonal isospectral fiber [PROVEN — Level 6, certificate attached; Level 7-adjacent since the certificate is an independently runnable script].** The path crosses the singular strata exactly twice, as the locking mechanism demands.

## Consequences (census + question status)
1. **Real-fiber connectivity for the pair: ANSWERED — CONNECTED, constructively.** Complex case was Atiyah; the real case for this pair is now ours by construction. The wave-1 row-2 question closes for the pair.
2. **Row B two-axis reading finalized:** component-splitting TRIVIAL over both ℂ and ℝ for the pair; the discrete axis rests entirely on finite-orbit (Sₘ) distinctness. Probe-1's "different strata" finding is explained: strata = bipartition pieces; the two graphs occupy different pieces of a connected fiber.
3. **Still OPEN, honestly:** full-fiber connectivity for this λ (sketch exists — any balanced sign pattern reachable via park-and-revive; not yet written), and the GENERAL-spectrum real fiber question — our λ was tractable precisely because 0³ forces rank 2. The rank-2 trick does not generalize as-is.
4. **Prior-art obligation before any novelty word:** rank-2 prescribed-diagonal objects are frames-adjacent (pairs (u,v) with |uᵢ|=|vᵢ| ≈ signed 2-frames with equal-modulus coordinates); the balanced-sign combinatorics may exist in the eigensteps/frames literature. Sweep owed at claim boundary. Until then: PROVEN construction, novelty-silent.

## Status moves (Will's desk)
Wave-1 row 2: **CLOSED for the pair** (Probe-1 CERTIFIED + Probe-2 graded + path PROVEN). Successors eligible, each needing its own predecl: (a) full-fiber connectivity write-up (Level 5→6, days); (b) exact infimum of the piece-separation floor (the 1.893 as an algebraic number — optional, pretty); (c) wave-1 row 3 harvest. Nothing canonical until Will signs.
