# REALFIBER_PREDECL — wave-1 row 2: real-fiber connectivity probe (SN-2)
**Date:** 2026-07-02 · **Status:** FROZEN on Will's "(2) then (3)"; sweep gate CLEARED (see `REALFIBER_SWEEP_NOTE.md`, sha `4d2539a1`) · **Written BEFORE battery code (covenant #2).** Substrate: Probe-1 [CONTAINER] exact ℚ; Probe-2 [BOX preferred] gated numerics, EMPIRICAL ceiling. Byte-stable ×2 per probe.

## Object (DF-R1)
```
F_ℝ = { W ∈ Sym₅(ℝ) : charpoly(W) = λ(λ²−4)λ² i.e. spec = {2,0,0,0,−2}, diag(W) = 0 }
A₁ = adj(K₁,₄)  (star)      A₂ = adj(C₄ ⊔ K₁)  (cycle+point)      both ∈ F_ℝ
Question: same path-component of F_ℝ?   Ambient orbit O_λ ≅ O(5)/(O(1)×O(3)×O(1)), dim 7 (smooth, connected —
stabilizer meets both components of O(5)); F_ℝ = μ⁻¹(0) ∩ O_λ for μ = diag; 0 need NOT be a regular value.
```
Known imports: Hermitian fiber connected [Atiyah 1982 — A₁, A₂ joined through ℂ]; complex splitting REFUTED; real question OPEN per sweep.

## Probe-1 — exact local geometry (runs this session)
Instrument: `ψ_W : so(5) → ℝ⁵, A ↦ diag([W,A])` (ROWB instrument, reused); commutant `c(W) = dim ker(ad_W|so(5))`.
**Hand-derivation pinned pre-freeze:** column(a,b) of ψ_W = `−2·W_ab·(e_a − e_b)`. Star: 4 columns `e₀−e_j` independent ⟹ rank 4. Cycle: 4 columns `e₀−e₁, e₁−e₂, e₂−e₃, e₃−e₀` sum to zero ⟹ rank 3.
- **P-R1:** membership control — both charpolys equal `λ⁵ − 4λ³` exactly.
- **P-R2:** `c(A₁) = c(A₂) = 3` (spectrum type (1,3,1)) ⟹ orbit-tangent dim 7 at both.
- **P-R3:** rank ψ = **4 at the star, 3 at the cycle** (per pinned derivation).
- **P-R4 (classification):** star = REGULAR point of μ|O_λ (local fiber dim 3); cycle = CRITICAL point (kernel-in-orbit dim 4 > 3). Consequence recorded if it certifies: **the two cospectral graphs occupy different strata of the same fiber** — a local structural datum; carried with the caveat in ink that *local* strata data cannot obstruct connectivity.
- **C-1 (genericity control):** ψ-rank = 4 at `RᵀA₁R` for a pinned rational Cayley R (generic non-fiber orbit point).
- **Kills:** K-1 controls fail → halt. K-2 P-R3 fails → the pinned hand-derivation is wrong; halt, derive in ink, re-freeze (no silent fix).

## Probe-2 — continuation bridge attempt (FROZEN NOW; runs on next Go, box preferred)
Attempt a real path star→cycle inside F_ℝ: flow along the certified distribution `D_W` toward the target orbit, projected-Newton correction onto the constraints `{c₂..c₅ fixed, diag = 0}` each step; distance objective = min over the 15-element S₅-orbit of A₂. Pinned: 20 starts (PRNG seed 20260702), 3 step-schedules, Newton gates g1–g3 as DF-7-style (hard convergence gate, no silent failures), tolerance ladder 1e−8→1e−12, both directions (star→cycle, cycle→star from smooth-stratum perturbed starts, since the cycle itself is predicted singular).
**Outcome typing (all three pay, committed now):**
- **A (bridge):** endpoint within tol of target orbit ⟹ connectivity EMPIRICALLY supported for the pair; certification obligation (a-posteriori path verification) named as its own successor predecl; the "real invariant separates cospectral graphs" branch closes for this pair.
- **B (persistent failure, all schedules):** OPEN stands, failure geometry banked (where flows stall = candidate wall data); escalation = topological attack (discrete-torus GKM / Saldanha–Tomei toolkit), own predecl.
- **C (locally-constant obstruction found en route):** discovery-grade — HALT to Will immediately.
No locally-constant obstruction candidate is currently known; Probe-2's stall data is the designated candidate generator. Predictions are never widened; a surprising rank or stall is reported as measured.

## Status-move rule
Probe-1 all-pass ⟹ local geometry CERTIFIED, strata datum banked; Probe-2 remains armed awaiting Will's Go. Any Probe-2 outcome routes to Will before wave-1 row 3.
