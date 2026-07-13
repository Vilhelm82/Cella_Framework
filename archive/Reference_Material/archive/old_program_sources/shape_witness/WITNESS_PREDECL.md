# WITNESS_PREDECL — n=5 σ-blind shape witness (queue item 2 feasibility gate)
**Date:** 2026-07-02 · **Status:** FROZEN on Will's "run n=5" instruction (the test as stated in-session verbatim: "same g, two Hessians with identical full σ-spectrum but different shape components") · **Predecl written BEFORE battery code exists** (covenant #2). Battery substrate: [CONTAINER], exact ℚ only (Fractions/sympy Rational), no floats on any verdict path. Byte-stable ×2 required.

## Object & mechanism (committed pre-run)
n=5, fixed regular gauge `g`. Witness constructed by **g-stabilizing rational rotation conjugation**:
```
A = u vᵀ − v uᵀ  (skew, u·g = v·g = 0)  →  R = (I−A)(I+A)⁻¹  (Cayley: exact-ℚ orthogonal, Rg = g)
H2 = Rᵀ H1 R
```
**Mechanism [claimed PROVEN, to be verified in-battery]:** P = I − ggᵀ/q commutes with R (Rg=g) ⟹ tangential operators P·Hᵢ·P are similar ⟹ σ_r(g,H1) = σ_r(g,H2) for ALL r, exactly. Nothing in the construction protects the Sₙ-adapted shape component `π_shape(O)`.
Exact-ℚ σ-detector: bordered-minor sums `Ê_r(H) = (−1)^(r+1) Σ_{|I|=r+1} det[[0,g_Iᵀ],[g_I,H_I]]` (Extension §1 at t=u=1). Gauge lemma (this session, row/col reduction): `Ê_r(H + gbᵀ + bgᵀ) = Ê_r(H)` for all r, b.
Isotypic projectors on the 10-dim pair module built from `evals/dbp_involution/rep_utils.py` Specht characters (λ = (5),(4,1),(3,2)); gated by rank checks 1/4/5, idempotency, and partition-of-identity — a character error cannot pass silently.

## Pinned fixtures (content pins; the battery embeds these verbatim)
```
g  = (1, 2, 3, 5, 7)
H1 = diagonal 0; off-diag lex (12,13,14,15,23,24,25,34,35,45) = (1, −2, 3, 1, 2, −1, 4, −3, 1, 2)
u  = (2,−1,0,0,0)   v  = (3,0,−1,0,0)          [primary A]
u2 = (5,0,0,−1,0)   v2 = (7,0,0,0,−1)          [backup A2, fires only under K-2]
u3 = (0,3,−2,0,0)   v3 = (0,5,0,−2,0)          [backup A3, fires only under K-2]
b  = (1,−1,2,0,1)                               [gauge control]
C-3 perturbation: H1 with entry (1,2) += 1
```
Invariant list, order fixed: `m2_shape = ‖π_shape(O)‖²` (primary), `m3_shape = tr(M(π_shape O)³)` (secondary), `(m2_triv, m2_std)` (recorded; separation by these alone = PARTIAL, not PASS).

## Predictions (graded mechanically)
- **P-W1:** Ê_r(H1) = Ê_r(H2) exactly, r = 1..4. [forced by mechanism if mechanism holds]
- **P-W2 (independent route):** charpoly(P·H1·P) = charpoly(P·H2·P) exactly in ℚ[z] (q cleared). [forced]
- **P-W3:** δ = π_shape(O(H1)) − π_shape(O(H2)) ≠ 0 exactly. [expected, not forced]
- **P-W4:** m2_shape(O1) ≠ m2_shape(O2). [expected; fallback m3_shape; only-triv/std ⟹ PARTIAL]
- **Controls:** C-1 identity pair → everything equal. C-2 gauge pair (H1 vs H1+gbᵀ+bgᵀ) → Ê_r equal, O equal, shape equal. C-3 perturbed pair → some Ê_r differs (detector non-vacuous).

## Kill conditions (armed)
- **K-1:** any control fails → HALT, route to Will (apparatus fault).
- **K-2:** δ_shape = 0 for A, A2, AND A3 → HALT: hidden O(4)_g-invariance of the shape component under conjugation — anomaly-grade finding, but this battery stops.
- **K-3:** P-W3 passes but no predeclared invariant separates → SEP FAIL banked honestly as "degree ≤3 moment invariants insufficient on this witness"; HALT for Will; successor rung needs a new predecl.

## Status-move rule
All controls pass + P-W1..W4 pass ⟹ bank to dashboard (PROPOSED delta): *"n=5 witness pair exists explicitly [CERTIFIED]: full σ-spectrum tied, shape components differ, separated by an exact-ℚ degree-2 shape-moment invariant — the Part III dimension threshold realized by construction; mechanism = g-stabilizing conjugation."* Queue-2 campaign brief becomes unblocked. Anything less: verdicts banked at true status, no dashboard delta without Will.
