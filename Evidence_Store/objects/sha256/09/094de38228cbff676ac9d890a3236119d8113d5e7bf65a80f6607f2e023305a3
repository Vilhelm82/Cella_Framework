# STAGE A REPORT — k=2 glue, P1a, tooling (opened 2026-07-02)
**Substrate:** [CONTAINER] `stageA_p1a.py`, `stageA_k2c.py` · **Status:** RUNNING.

## P1a: prediction → THEOREM
**Mechanism [PROVEN, exact identities]:** the kinetic energy is even in velocity ⟹ the midpoint discrete Lagrangian is **exchange-symmetric at fixed h**: `L_d(q1,q0,h) = L_d(q0,q1,h)` (verified as exact polynomial identity — strictly stronger than the adjoint identity), and componentwise `D1L_d(q1,q0) = D2L_d(q0,q1)`. Chain: reversed step from (q1,−π1) satisfies the forward equations back to (q0,−π0) ⟹ `R∘Φ_h∘R = Φ_h⁻¹` ⟹ every k-step variety carries the reversal involution (x0,…,xk) ↦ (Rxk,…,Rx0) ⟹ **any intrinsic degree spectrum is symmetric under initial↔terminal block swap, all k.**
**Prereg consequence:** P1a's kill condition can now only fire as a harness-bug detector; the falsification load transfers wholly to **P1b** — Rayleigh damping breaks velocity-evenness *specifically*, so the mechanism itself localizes where asymmetry must enter.

## Genericity (Stage-0 carry item, discharged)
1-step census at frozen h=1/40: **32 complex distinct / 16 real, shape position, at two independent rational basepoints** [CERTIFIED ×2]. Counts are h-robust (match the h=1/10 census).

## k=2 forward fiber census [EMPIRICAL-numeric, ceiling-pinned]
Method: 32 outer branches (shape lemma) × per-branch inner (4,4)×(4,4) system; per-branch coefficient normalization; exact-degree (≤32) resultant interpolation; step-converged Newton; **every accepted chain verified in mpmath (1924/1924)**; full-state clustering (q2, π2).
- **DISTINCT complex x2 = 1024 = 32² exactly — no composition collapse.** Count is pinned: measured = proven per-branch ceiling, verified chains can only under-, clustering only over-merge ⟹ true count = 1024. Complex dynamical degree so far: 32/step.
- **Real x2 = 224 < 16² = 256 — reality thins sub-multiplicatively** (avg 14 real inner per real outer). The T_k varieties live on the real locus ⟹ Stage B's effective wall is softer than the complex tower. First quantified point on the real-growth curve.
- Near-collision pair at separation 1.1e−7 recorded (candidate discriminant-adjacent structure).
- Backward fiber = 1024/224 **by the P1a involution [PROVEN]** — no computation spent.
Harness log: two bugs found & fixed in-session (residual scale omitted branch t-magnitude; resultant overfit past exact degree). Duplicated basin convergences expected & clustered.

## Tooling verdicts
- **python-flint 0.8.0: `fmpz_mpoly_vec.buchberger_naive` / `autoreduction` / `is_groebner` AVAILABLE.** Route for exact work: clear denominators → ℤ-Gröbner. (`fmpq_mpoly_vec` exposes nothing.)
- sympy GB: disqualified (Stage 0). Resultant chains: survey-only, spurious-prone.

## Stage A remaining
1. Exact k=2 per-variable spectrum via flint ℤ-GB (+ the P1a symmetry as harness check). 2. Discriminant strata on the rest slice. 3. P1b damped contrast. 4. k=4 doubling probe (growth curve, real vs complex).

---
# STAGE A UPDATE — 2026-07-02 afternoon: exact k=2 spectrum, ghost structure, quarantine + resolution
**Substrate:** [CONTAINER] `stageA_modspec.py` (modular spectrum engine), `stageA_k2clean.py` (degraded quick census — flagged).

## QUARANTINE → RESOLUTION of the morning census
The "1024 = 32² exactly / 224 real / position-coordinate pairing" census is **withdrawn as an honest count.** Mechanism: the outer loop iterated over all 32 U-roots including τ = ±i (ideal points); over those, the inner resultants vanish identically, the per-branch interpolations were noise, and ~64 manufactured chains assembled "exactly 1024" by seed-count construction. The 10⁵-beyond-chance coordinate pairing is consistent with sampling ghost solution *curves*. Real count and pairing on honest data: **OPEN — pending good-harness clean census** (a degraded quick rerun gave 706 distinct / 140 real; UNRELIABLE — normalization, exact-degree interpolation, and mp-verification were dropped for speed; recorded only as a harness-quality datum).

## Certified structure (modular engine, prime 519999979; all gates green: interpolator self-test, t2-holdout 9/9, z-holdout 39/39 & 15/15)
1. `gcd(U, R mod U) = T²+1` for all tested z ⟹ with the exact ℚ-factorization: ideal points ride the eliminant. [PROVEN + CERTIFIED]
2. **Self-similarity:** `R(t₂, ±i) ≡ 0 mod U₃₀` — every honest branch's inner eliminant carries u₂ = ±i among its roots. The correspondence preserves the ideal locus with positive-dimensional fibers over it. [CERTIFIED mod p; mechanism STRUCTURAL]
3. **Honest k=2 u₂-eliminant:** `E₃₀ = Res(U₃₀, R)`: deg = 960 = 30·32; **squarefree deg = 902 = 30² + 2**; gcd with (z²+1) = z²+1. ⟹ **honest forward u₂-spectrum entry = 900 = 30², all values pairwise distinct** — exact multiplicativity at the honest level; exact u₂-collisions REFUTED. [CERTIFIED mod p ×1 prime; second prime queued]
4. **Dynamical-degree reading through k=2: 30 per step.** The naive/honest gap (32 vs 30) is concentrated entirely at the conic's ideal points — the classic location of algebraic-entropy cancellation, now with the locus identified. Step-budget arithmetic softens accordingly: 30^k vs 32^k.

## Engine log (honesty ledger)
Two int64 overflow bugs (33·p² matmul; p³ triple product) found by the holdout gates — including one run whose corrupted output *matched my prediction* and was rejected on gate failure alone. The eliminant-zero that exposed the entire ghost structure was itself first suspected as a bug. Day's self-refutation count: Bézout-16 → 32 → "32 tight" → 30+2 honest/ideal; "1024 exactly" → withdrawn.

## Queue (Stage A continuation)
1. Second prime on E₃₀ (cheap, upgrades tier). 2. Good-harness clean census → honest full-state count (≥900 forced), real count, pairing verdict. 3. Per-coordinate exact eliminants A2/B2 (division-by-quadratic route), A1/B1/u1 (role swap), π2 (needs mult-matrix or GB). 4. Verify T²+1 | U at basepoint B [PLAUSIBLE, chart-structural]. 5. Ideal-locus mechanism: clean statement + proof obligation (fixed ideal locus with fat fibers ⟹ honest-degree drop). 6. P1b damped run. 7. k=4 doubling probe at honest degrees.

---
# STAGE A UPDATE 2 — 2026-07-02 evening: spectrum certified ×3, census closed, pairing anomaly resolved
**Substrate:** [CONTAINER] `stageA_modspec2.py`, `stageA_k2h.py`, `branchtable.py`.

## Tier upgrades
- Honest k=2 u₂-spectrum **900 = 30²**, ghost factor z²+1, self-similarity R(·,±i)≡0 mod U₃₀: now **CERTIFIED mod p × 3 independent primes** (519999979, 519999959, 518999941), identical readings, all holdout gates 39/39.

## Honest census — closed
- **Complex: 900 [CERTIFIED, exact].** Float harvest recovered 845/900; the 55-chain deficit is localized to six ill-conditioned complex branches (three conjugate pairs, the same branches dropping a ghost root) — documented harness limitation; mp-harvest repair queued, non-blocking (count is exact-certified).
- **Real: 224 — COMPLETE.** All 16 real branches harvested at 30/30 honest + 2/2 ghosts; every real chain mp-refined to residual <1e−25. Real thinning **224 < 256 = 16²** stands on certified-honest data (avg 14 real continuations per real branch).
- **Pairing anomaly: REFUTED as artifact.** On mp-refined honest chains: min separation **9.8e−2**, zero near-pairs, all six coordinates separate all chains (845/845 distinct per coordinate). The 10⁵-beyond-chance clustering was ghost-curve sampling, entirely.

## New lead (OBSERVED): real-multiplicity spectrum of the correspondence
Per-real-branch real-continuation counts: {16×10, 14×4, 6, 2} — even by conjugation [forced], sharply non-uniform. Branch 12 (|t₂|≈2.76) retains only **2 of 30** real continuations: a real branch pressed against the real discriminant of the step correspondence — candidate fold geometry for the T_k boundary strata (Stage B's discriminant task now has a marked target).

## Queue (updated)
1. Exact eliminants for A2/B2 (division-by-quadratic route), A1/B1/u1 (role swap), π2 (mult-matrix or GB). 2. mp-harvest repair, 6 branches (low priority). 3. Ideal-locus mechanism: clean statement + proof (fixed ideal locus, fat fibers ⟹ honest-degree drop 32→30). 4. T²+1|U at basepoint B [PLAUSIBLE, verify]. 5. P1b damped run. 6. k=4 doubling at honest degrees. 7. Real-discriminant look at branch 12.
