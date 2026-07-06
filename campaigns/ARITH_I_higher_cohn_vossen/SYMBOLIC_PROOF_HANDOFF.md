# ARITH-I — symbolic proof of the r=3 channel constant (handoff)

**For:** Will, to work over / refine / present. **Date:** 2026-07-06.
**Status:** the proof is **complete and machine-checked** (`reports/arithmetic_track/
arith_i_stageB_proof.py`, `b3314de7`, 8/8, byte-stable ×2). This doc lays out the whole
argument, every definition it needs, the verification, the general-n extension, and the
rigor points still worth nailing by hand. Novelty/prior-art is explicitly **out of
scope** here (your instruction).

**Claim proved.**
```
∫_S κ_{3;3,0} dA = −2π²/(5c)          (c=1: −2π²/5 = −3.947841760…)
```
on the canonical n=4 surface, where `S = {F = 0}`. In particular it is **nonzero**, so
(the surface being a compact ellipsoid) the density is **not exact**; and the value is a
**rational multiple of vol(S³)=2π²** — a π²-rational, not an elliptic period.

---

## 1. Objects (all definitions, self-contained)

**Surface (canonical n=4, from CALC-04 / CALC-24 Part A):**
```
F(y) = Σ_{i=1}^4 y_i² + Σ_{i<j} y_i y_j − c = 0 ,   y ∈ ℝ⁴ .
```
Its Hessian is constant, `H = ∇²F = I + J` (`J` = all-ones matrix; `H_ii=2, H_ij=1`).
The quadratic form is `F + c = yᵀ M y` with `M = (I+J)/2`, eigenvalues `{5/2, 1/2, 1/2,
1/2}` — **positive definite**, so **S is an ellipsoid: a compact, connected, oriented
3-manifold, diffeomorphic to S³, convex.** (Contrast the non-compact n=3 keystone
hyperboloid — this compactness is the whole point.)

**Coupling channel density (CALC-15/15a; grid normalization `q^{(r+2)/2}`, r=3):**
```
g = H y ,   q = |g|² = gᵀg ,   P = I − g gᵀ/q  (⊥-projection off the gradient),
Hc = offdiag(H) = J − I ,
κ_{3;3,0} = (−1)³ e_3(P Hc P) / q^{5/2} = − e_3(P Hc P) / q^{5/2} .
```
`e_3(·)` = sum of the four 3×3 principal minors of a 4×4 matrix. `H°=Hc` (off-diagonal)
is the *coupling* channel — CALC-15a: using the full Hessian instead gives the
Gauss–Kronecker object "the paper rules out."

**Gauss–Kronecker control density (the calibrator):**
```
K_GK = e_3(P H P) / q^{3/2}          (full Gauss–Kronecker curvature of the hypersurface)
∫_S K_GK dA = vol(S³) = 2π²          (Gauss-map degree 1 for a convex body).
```

**Area element `dA`** = the induced Riemannian 3-volume on S.

---

## 2. The proof (five steps)

### L1 — Compression-determinant lemma
For the rank-3 projection `P = I − ν νᵀ` with `|ν| = 1`, and any symmetric 4×4 `A`,
```
e_3(P A P) = det( A restricted to ν^⊥ ) = νᵀ adj(A) ν ,
```
`adj(A)` = adjugate (transpose cofactor matrix). *(Classical: the 3 nonzero eigenvalues
of `PAP` are the eigenvalues of `A|_{ν^⊥}`; check on `A=diag(a,b,c,d)`, `ν=e₁`:
`det(A|_{e₁^⊥})=bcd`, `e₁ᵀadj(A)e₁ = bcd` ✓.)*

### L2 — Gauss-map change of variables
The Gauss map `ν = N(y) = g/√q` is a **diffeomorphism S → S³** (S convex). Under it the
tangential projector is exactly `P = I − ν νᵀ`, and for any function `f` on S,
```
∫_S f · K_GK dA = ∫_{S³} (f∘N⁻¹) dΩ .
```
Write `φ := κ_{3;3,0}/K_GK`. Then
```
∫_S κ_{3;3,0} dA = ∫_S φ · K_GK dA = ∫_{S³} φ dΩ ,
φ = κ/K_GK = − e_3(P Hc P) / ( q · e_3(P H P) ) .
```
(The extra `1/q` versus the geometric `K_GK` is the grid normalization `q^{5/2}` vs
`q^{3/2}`.)

### L3 — The two `e_3`'s are quadratic forms in `σ = Σν_i`
Adjugates of the constant matrices:
```
adj(H)  = 5I − J        (H=I+J: eigenvalues 5,1,1,1, det 5, H⁻¹=I−J/5)
adj(Hc) = 3I − J        (Hc=J−I: eigenvalues 3,−1,−1,−1, det −3, Hc⁻¹=−I+J/3)
```
With `νᵀ J ν = (Σν_i)² = σ²` and `|ν|=1`, L1 gives
```
e_3(P H P)  = νᵀ(5I−J)ν = 5 − σ² ,
e_3(P Hc P) = νᵀ(3I−J)ν = 3 − σ² .
```

### L4 — `q` from the constraint, and the cancellation
`g = Hy = 2My`, `ν = 2My/√q`, so `y = √q M⁻¹ν/2`; the constraint `yᵀMy = c` gives
```
q = 4c / (νᵀ M⁻¹ ν) ,   M⁻¹ = 2H⁻¹ = 2I − 2J/5 ,   νᵀM⁻¹ν = 2(5−σ²)/5
⟹ q = 10c/(5 − σ²) .
```
Therefore `q · e_3(P H P) = [10c/(5−σ²)]·(5−σ²) = 10c` — **the `(5−σ²)` cancels** —
```
φ = −(3 − σ²)/(10c) .
```

### L5 — Two S³ moments finish it
`σ² = (Σν_i)² = Σν_i² + Σ_{i≠j}ν_iν_j = 1 + (cross terms)`, and on S³ the cross terms
integrate to 0 by symmetry, while `∫_{S³}1\,dΩ = vol(S³) = 2π²`:
```
∫_{S³} σ² dΩ = 2π² ,   ∫_{S³}(3 − σ²) dΩ = 3·2π² − 2π² = 4π² .
```
Hence
```
∫_S κ_{3;3,0} dA = ∫_{S³} φ dΩ = −(1/(10c))·4π² = −2π²/(5c) .            ∎
```

---

## 3. Verification (what's already checked)

- **Symbolic (machine-checked):** `arith_i_stageB_proof.py` (`b3314de7`, 8/8 ×2) verifies
  L1/L3 (`e_3(PHP)=5−σ²`, `e_3(PHcP)=3−σ²`, adjugates), L4 (`q=10c/(5−σ²)`, the
  cancellation `φ=−(3−σ²)/(10c)`), L5 (`∫(3−σ²)=4π²`), and assembles `−2π²/(5c)`.
- **Independent numeric (the original verdict):** `arith_i_stageB_verdict.py` (`843a7689`)
  — direct grid integration over the ellipsoid gives `∫κ = −3.9483`, `∫K_GK = 19.7415 ≈
  2π²` (control), ratio `−0.2000000` to 7 digits, and the `1/c` scaling (`c=2 → −1/10`).
- **Point cross-check:** at `y=(1,0,0,0)` (so `c=1`): `σ²=25/7`, `q=7`, `e_3(PHcP)=3−25/7
  =−4/7` ✓ (matches the raw density), `e_3(PHP)=10/7`, `φ=2/35`.

---

## 4. General n (top order r = n−1) — and a correction

The identical chain runs for the top-order channel `κ_{n−1;n−1,0}` on the same
symmetric family `F=Σy_i²+Σ_{i<j}y_iy_j−c` in ℝⁿ:
```
adj(H)=(n+1)I−J,  adj(Hc)=(−1)^{n−1}(J−(n−1)I),  q = 2c(n+1)/((n+1)−σ²),
φ = (σ² − (n−1))/(2c(n+1)),   ∫_{S^{n−1}} σ² dΩ = vol(S^{n−1}),
∫_S κ_{n−1;n−1,0} dA = −(n−2)·vol(S^{n−1}) / (2c(n+1)),
ratio = ∫κ/∫K_GK = −(n−2)/(2c(n+1)).
```
At `n=4`: `−2/(2·5c) = −1/(5c)` ✓.

**Correction to the earlier note:** the staked guess `ratio = −1/(n+1)` is **wrong in
general** — it coincides with `−(n−2)/(2(n+1))` only at `n=4` (`2/10 = 1/5 = 1/(n+1)`).
The correct top-order law is `−(n−2)/(2c(n+1))`. Worth confirming numerically at `n=5`
(predicts ratio `−3/(2·6) = −1/4` at c=1) before banking as a theorem. *(The r=3 channel
with n fixed but n>4 — where `e_3` is no longer the full compression determinant — is a
genuinely different computation and is NOT covered by this chain; that's a separate
open thread.)*

---

## 5. Rigor points to nail by hand (for you to work over)

1. **L1 as a clean statement/proof.** State the compression-determinant identity
   `e_{n−1}(P A P) = νᵀadj(A)ν` on `|ν|=1` as a lemma with a two-line proof (eigenvalues
   of the compression, or the adjugate/cofactor expansion). It's classical but the
   write-up should own it.
2. **L2 orientation & convexity.** The Gauss map is a diffeomorphism because S is convex
   (`M` pos. def. ⟹ all principal curvatures same sign ⟹ `K_GK>0`), so the change of
   variables carries the correct orientation and no Jacobian sign issues. Worth one
   sentence pinning `∫_S f K_GK dA = ∫_{S³} f∘N⁻¹ dΩ` to the standard "Gauss map pulls
   back the S³ area form to `K_GK dA`" fact.
3. **L5 moment.** `∫_{S^{m}} ν_iν_j dΩ = δ_{ij}·vol(S^m)/(m+1)` (standard Dirichlet
   moment); the cross-term vanishing and `Σν_i²=1` are all you use. One line.
4. **The scaling law** (already clean, include it): under `y→αy`, `κ→α^{−5}κ`,
   `dA→α³dA`, so `∫κ ∝ 1/c` (`c→α²c`); `K_GK dA` is scale-invariant, `∫K_GK=2π²` for all
   c. This is why the constant carries a `1/c` and the *scale-free* statement is
   `c·∫κ = −2π²/5`, or the ratio `∫κ/∫K_GK = −1/(5c)`.

---

## 6. Connections / optional strengthenings

- **v1.1 §I.3b (the Johnson closed form)** gives `−q·e_2(P Hc P) = q·Σ_e h_e² − |H_c g|²`
  and `shadow(Q_ν)=s(g)[(n−2)I − A₁·Johnson J(n,2)]`. That is the *r=2* sibling of L3;
  a §I.3b-style closed form for `e_3(P Hc P)` would re-derive L3 from the framework's own
  triangle/Johnson machinery rather than the adjugate lemma — a nice alternative route if
  you want the proof phrased in role-channel language. (Here L1+L3 via the adjugate is the
  shortest path and needs nothing external.)
- **What the constant "is".** `∫κ = −(1/5)·∫K_GK = −(1/5)·(Gauss-map degree)·vol(S³)`.
  The `−1/5` is `⟨φ·(−10c)⟩ = ⟨3−σ²⟩ / (…)`, i.e. it is set entirely by the **average of
  `σ² = (ν·1)²` over S³**, which is `1`. Cleanly: the channel constant is fixed by the
  first spherical moment of the all-ones direction — no elliptic input anywhere. This is
  the structural reason it is a π²-rational, and the sharpest one-line "why" for a
  write-up.

---

## 7. Files

- `reports/arithmetic_track/arith_i_stageB_proof.py` — the symbolic proof (`b3314de7`).
- `reports/arithmetic_track/arith_i_stageB_verdict.py` — the independent numeric verdict
  + control (`843a7689`).
- `campaigns/ARITH_I_higher_cohn_vossen/STAGE_B_VERDICT.md` — the verdict writeup /
  reframing (C1/C2 dissolved; compact-ellipsoid species).
- `campaigns/ARITH_I_higher_cohn_vossen/OPEN_B1_RESOLVED.md` — surface/density/reference
  provenance (calc log v8, standing results v1.1).
