# CORRECTION — the r=3 channel density carried the wrong q-power (caught by Will)

**Owned, dated: 2026-07-06 (Will, direct).** Case law, same class as the fabricated
stop condition: an inherited defect in the addendum's own wording, surviving because it
*looked* right, caught by re-verification — not by process.

## What was wrong

The verdict computation and its first "proof" used the density
```
kappa_aux = − e_3(P Hc P) / q^{5/2}          (grid power q^{(r+2)/2}=q^{5/2} on the COMPRESSION e_3)
```
and got the clean `∫_S κ_aux dA = −2π²/5` (a π²-rational). **That object is not the
standard r=3 pure-coupling channel** — Will's diagnosis: it is a *1/q-weighted
compression-density*. The standard channel that retrodicts the certified values
(`κ_c = −1/49` at r=2) is
```
kappa_{3;3,0} = (−1)^3 e_3(P Hc P) / q^{3/2}          (engine /q^{r/2})
```
because the bordered-minor numerator obeys the exact identity (verified,
`arith_i_stageB_proof.py`)
```
det[[Hc, g],[gᵀ, 0]] = − q · e_3(P Hc P) ,
```
so the framework's grid-normalized bordered channel `−det[…]/q^{(r+2)/2}` equals
`e_3(P Hc P)/q^{3/2}`, **not** `/q^{5/2}`. `κ_aux = κ_{3;3,0}/q`.

**Root cause:** the addendum A5 wrote the density as "`e_3(P H° P)/q^{5/2}`" —
applying the *bordered*-minor grid power `q^{(r+2)/2}` to the *compression* object
`e_3(P Hc P)`. The two normalizations agree only after the `−q` of the
bordered↔compression identity is accounted for. A5's formula was self-inconsistent, and
the session inherited it verbatim. (The addendum A5 was written by a prior session
"hot"; this is its second inherited defect after the fabricated stop condition.)

## Two tells that were missed (and should be standing checks)

1. **Scale-invariance.** A genuine curvature integral (Gauss–Bonnet / Gauss–Kronecker
   species) is scale-invariant. `κ_aux dA → α^{−2}` under `y→αy` (so `∫ ∝ 1/c`) — a
   red flag. The standard `κ_{3;3,0} dA → α^0` is scale-invariant (`∫κ = −2π²/√5` for
   all c), like `∫K_GK = 2π²`.
2. **Parity.** The parity law says odd `r` lives in `ℚ(√q)`. The standard constant
   carries `√5 = √(n+1)` (odd-parity); the auxiliary `−2π²/5` was rational — the extra
   `1/q` had washed the parity `√` out. A rational odd-r channel constant should have
   been suspicious on its face.

## The corrected result (machine-checked, `f2f851ea`, 6/6 ×2)

```
∫_S κ_{3;3,0} dA = − 2π² / √5           (scale-invariant, all c)
```
Same proof skeleton (Gauss map ⟹ `∫κ dA = ∫_{S³} φ dΩ`; `e_3(P A P)=νᵀadj(A)ν`;
`adj(H)=5I−J`, `adj(Hc)=3I−J` ⟹ `e_3(PHP)=5−σ²`, `e_3(PHcP)=3−σ²`) but now
`φ = −(3−σ²)/(5−σ²)` — **the `(5−σ²)` does NOT cancel** (the cancellation in the
auxiliary version was the artifact). The surviving denominator makes the sphere integral
`∫_{S³} dΩ/(5−σ²) = π²(1−1/√5)` (from `∫dθ/(1+4cos²θ)=π/√5`), giving `−2π²/√5`.

## What changes / what stands

- **Exactness verdict: UNCHANGED.** `−2π²/√5 ≠ 0`, so on the compact ellipsoid the
  standard density is still **not exact**. K-3 still not triggered.
- **Value & character: CHANGED.** `−2π²/5` (π²-rational) → `−2π²/√5` (π²·algebraic-
  irrational, odd-parity `√5`). Still not an elliptic period; the C1/C2 dichotomy still
  dissolves into "π²·algebraic on the compact ellipsoid" — but now with the parity `√`.
- **General-n (top order r=n−1): the earlier `−(n−2)/(2(n+1))` and `−1/(n+1)` are BOTH
  void** (they were computed with the auxiliary normalization). Re-derive from
  `∫κ = −∫_{S^{n−1}}((n−1)−σ²)/((n+1)−σ²)dΩ`; expect a `√(n+1)` odd-parity factor. Not
  yet redone.

## Standing check added

For any odd-r channel constant: (i) confirm the density is **scale-invariant** before
integrating; (ii) expect a `√q`-type (odd-parity) factor in the answer — a *rational*
odd-r constant is a normalization-error signal. And: the q-power on a compression object
`e_r(P Hc P)` is `q^{r/2}` (engine), which equals the bordered grid power `q^{(r+2)/2}`
only after the `det[[Hc,g],[gᵀ,0]] = −q e_r` identity. Never read the bordered power
onto the compression object directly (the A5 mistake).
