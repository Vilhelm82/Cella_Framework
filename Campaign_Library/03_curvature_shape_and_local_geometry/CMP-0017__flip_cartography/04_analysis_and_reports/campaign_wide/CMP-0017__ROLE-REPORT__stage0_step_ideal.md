# STAGE 0 REPORT — the step ideal (flip_cartography)
**Date:** 2026-07-02 · **Substrate:** [CONTAINER] `stage0_core.py`, `stage0_probe.py`, `stage0_res.py` (exact-ℚ verdict paths; floats only in root-count diagnostics) · **Status:** Stage 0 OPEN — substantially advanced; remaining items listed at end.

## Definition freezes
- **DF-1 (parameters):** m₁=m₂=1, ℓ₁=ℓ₂=1 (point bobs), g=10. h provisional = 1/10; final freeze after the Stage-0 h-scan.
- **DF-2 (scheme):** reduced midpoint variational integrator on the torus embedding q=(c₁,s₁,c₂,s₂), φᵢ=cᵢ²+sᵢ²−1. Kinetic energy in ω-form: ωᵢ = cᵢṡᵢ − sᵢċᵢ; `T = ω₁² + ω₂²/2 + ω₁ω₂(c₁c₂+s₁s₂)`, `V = −g(2c₁+c₂)`. `L_d = h·L((q₀+q₁)/2, (q₁−q₀)/h)`. Momenta are **tangent-projected angular momenta** πᵢ = ⟨D₂L_d, ξᵢ(q₁)⟩ with ξᵢ the circle rotation fields — multipliers drop out identically; no hidden-constraint bookkeeping. State = (q, π₁, π₂); step generators (h-cleared): `h·[πᵢ + ⟨D₁L_d, ξᵢ(q₀)⟩] = 0` (i=1,2), `φ₁(q₁)=0`, `φ₂(q₁)=0`; update `πᵢ′ = ⟨D₂L_d, ξᵢ(q₁)⟩`.
- **DF-3 (flip predicate):** on the torus, crossing the inverted vertical for bob 2 is the point (c₂,s₂)=(−1,0). Discrete crossing at step k: `s₂⁽ᵏ⁻¹⁾·s₂⁽ᵏ⁾ < 0 ∧ c₂⁽ᵏ⁻¹⁾<0 ∧ c₂⁽ᵏ⁾<0`. Boundary/touch object T_k: `s₂⁽ᵏ⁾ = 0` on the c₂<0 branch.
- **DF-4 (metrics):** deferred to Stage C entry, per the frozen brief.

## Checks
| check | result | tier |
|---|---|---|
| Adjoint identity `L_d(q₁,q₀,−h) = −L_d(q₀,q₁,h)` | exact polynomial identity, verified | **PROVEN** — the scheme is self-adjoint; P1a tests the framework, not the code |
| h→0 consistency (in-equations reduce to π=∂L/∂ω; out-momenta match) | h¹-coefficients vanish exactly at two independent rational torus points | **CERTIFIED** (assembly); 2nd-order accuracy of midpoint variational = KNOWN BACKGROUND, import + cite at claim time |
| Constraint propagation | φ(q₁)=0 are generators | **PROVEN** by construction |
| Mass-matrix nondegeneracy | `det M = 2 − c_Δ² ≥ 1` on the whole torus | **PROVEN** — the "mass-matrix degenerate locus" failure mode is EMPTY for this system |

## Energy gates (derived, not assumed)
- **Point bobs (our system):** flip of bob 2 requires reaching (c₂,s₂)=(−1,0); `min_{c₁} V(c₁,−1) = −g`. Release-from-rest **no-flip gate: `2·cosθ₁ + cosθ₂ > 1`**. [PROVEN]
- **Uniform rods:** V = −(g/2)(3c₁+c₂); same argument gives **`3·cosθ₁ + cosθ₂ > 2`** — the Levien–Tan folklore constant reproduced and **explained: it is the rods system, not ours**. Conventions pinned; assuming the literature constant would have made P2 fire falsely at Stage B. [PROVEN]

## Degrees & branch structure (first readings of the degree instrument)
- Step generators: per-block degrees (q₀-block 2, q₁-block 2, π 1, h 2, g 1), total 6. **The step relation is biquadratic in (state₀, state₁).**
- Forward branch count per step: **≤ 2⁴ = 16** [PROVEN, Bézout]. Exact value [OPEN]: naive resultant chain returned a degree-124 eliminant (factors 30+30+32+32, 64 real candidates) — **spurious-dominated, rejected against the proven ceiling** (brief failure mode #1, caught as designed). Saturated elimination → Stage A bake-off.
- Tooling verdicts: sympy lex-Gröbner DNF at 280 s on the per-step solve; resultant chain 15 s but contaminated; **python-flint 0.8.0 installed and importable** — primary engine candidate for Stage A.

## Remaining to close Stage 0
1. h-scan → final DF-1 freeze of h. 2. Energy-behavior diagnostic trajectory (float diagnostic, non-verdict). 3. Exact per-step branch count via saturated elimination (flint).

---
# STAGE 0 CLOSURE — 2026-07-02 (same day, second pass)
**Substrate:** [CONTAINER] `stage0_branchcount.py`, `stage0_census.py`, `stage0_close.py`, `stage0_hscan.py`.

## CORRECTION (self-refutation, logged in ink)
The morning claim "forward branch count ≤ 2⁴=16 [PROVEN, Bézout]" is **REFUTED — by our own exact computation.** The momentum generators are bidegree (2,2) across the two circles; on the compactified torus ≅ ℙ¹×ℙ¹ (Weierstrass t-charts, each ambient degree pulling back doubled) the honest multihomogeneous ceiling is 4·4+4·4 = **32**. The computation hits it exactly.

## Branch census at the frozen basepoint [CERTIFIED]
Weierstrass reduction → bivariate (4,4)×(4,4) system → lex Gröbner (2.5 s, **shape position**): quotient dim = **32 complex solutions, all distinct** (squarefree eliminant deg 32); **16 real**（shape lemma, leading-coeff gcd 0); **no solutions at the excluded charts** Cᵢ=−1 (consistency gcds degree 0). **Physical-branch membership:** the Newton branch from near-identity satisfies the eliminant to |uni(t₂*)|/scale = 5.6e−40 — the dynamics lives inside the census. Root sanity 6/6 at 40 dps (the earlier 0/6 was a double-precision conditioning trap in the checker, not the mathematics). By the adjoint identity, **backward branch count = 32** [PROVEN symmetry, no computation]. Genericity across basepoints: [EXPECTED — Stage A spot-check item].

## h-scan (gated) and DF-1 final freeze
Newton stepper upgraded with a **hard convergence gate** + halving predictor after the first pass produced a silent failure (h=0.05: solver died at step 18; constraint residual 0.56; its "flip at step 18" was numerical fiction — row discarded; the gate now makes such failures loud).

| h | steps | halt | maxRelE | endRelE | maxφ | revErr | 1st flip |
|---|---|---|---|---|---|---|---|
| 1/10 | 100 | gate @ 20 | — | — | 9e−13 | — | — |
| 1/20 | 200 | gate @ 18 | — | — | 4e−13 | — | — |
| **1/40** | 400 | clean | 9.3e−2 | 8.2e−4 | 7e−13 | 5.4e−7 | step 129, t=3.225 |
| 1/80 | 800 | clean | 2.3e−2 | 2.2e−3 | 1e−12 | 7.4e−4 | step 258, t=3.225 |

O(h²) verified: maxRelE ratio 4.04 under halving [EMPIRICAL, 2-pt Richardson]. Flip-time h-agreement **0.00%**. Gate fires at h ≥ 1/20 are a *solver* verdict (root unreachable by Newton+predictor at whips), not integrator nonexistence — revisit only if larger h becomes strategically necessary.
**DF-1 FROZEN: h = 1/40** (criterion, stated pre-decision: largest h with no gate fire, φ ≤ 1e−12, revErr ≤ 1e−6, flip-time agreement with h/2 ≤ 2%).

## Step-budget line for Stage A/B (honest tension)
At h=1/40 the first flip at a mid-regime IC is step ~129; immediate-flip corner (near double-inverted) ~12–40 steps. The exact reach must climb to k ≈ 20–130 via the biquadratic degrees + composition doubling, or T_k claims restrict to the immediate corner. This is Stage A/B's battleground, now with a number on it.

## STAGE 0: **CLOSED** per the frozen gate — all consistency checks pass, degrees recorded, energy gate derived, h frozen, branch structure certified.

---
# STAGE 0 CORRECTION 2 — 2026-07-02 (via the Stage-A exact engine)
**The one-step branch census is revised: 32 = 30 honest + 2 ideal.** The exact eliminant factors over ℚ as `U = (T²+1)·U₃₀` [PROVEN, sympy exact factorization]. T = ±i are not torus points — they are the second circle's **complex points at infinity** (the conic's ideal points, where the Weierstrass chart is singular). The Stage-0 "excluded chart" check tested only the chart-missed point (−1,0); the conic's ideal points were never checked — the named spurious-component trap, one door over from where I guarded it.
**What survives untouched:** all 16 real branches (±i non-real), physical-branch membership, shape position, the multihomogeneous ceiling 32 (correct for the ℙ¹×ℙ¹ compactification). **What changes:** honest torus degree per step = **30**; the "tight" reading of the ceiling was compactification bookkeeping.
