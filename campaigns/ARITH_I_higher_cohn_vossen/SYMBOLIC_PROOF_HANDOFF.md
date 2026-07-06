# ARITH-I — symbolic proof of the r=3 STANDARD channel constant (handoff, corrected)

**For:** Will, to work over. **Date:** 2026-07-06 (v2, corrected).
**Correction (yours):** the first version proved `−2π²/5` for an *auxiliary
1/q-weighted* density; the **standard** channel constant is **`−2π²/√5`**. This doc is
the corrected, machine-checked proof (`reports/arithmetic_track/arith_i_stageB_proof.py`,
`f2f851ea`, 6/6, byte-stable ×2). Novelty/prior-art out of scope (your instruction).

**Claim proved.**
```
∫_S κ_{3;3,0} dA = −2π²/√5   (≈ −8.8276425)   — scale-invariant (all c).
```
Nonzero ⟹ **not exact** on the compact ellipsoid `S`. The value is `π²·(1/√5)`, an
**algebraic-irrational** multiple of `π²` (odd-`r` parity factor `√5 = √(n+1)`) — not a
π²-rational, and not an elliptic period.

---

## 0. THE NORMALIZATION (the part that bit — pin this first)

The r=3 pure-coupling channel numerator is the **bordered minor**, and it satisfies the
exact identity (verified in the certificate):
```
det[[Hc, g],[gᵀ, 0]] = − q · e_3(P Hc P) ,   P = I − g gᵀ/q ,  q = |g|² .
```
So the framework's grid-normalized bordered channel is
```
κ_{3;3,0} = (−1)³ · (bordered)/q^{(r+2)/2} = (−1)³ · (−q·e_3(P Hc P))·(−1)/q^{5/2}
          = − e_3(P Hc P) / q^{3/2}          (= the engine's (−1)^r e_r/q^{r/2}).
```
**Normalization is `q^{3/2}`, not `q^{5/2}`.** Writing `e_3(P Hc P)/q^{5/2}` (the
addendum-A5 wording) applies the *bordered* power `q^{(r+2)/2}` to the *compression*
object `e_3(P Hc P)` — an extra `1/q`. Two independent sanity checks that fix the power:
(i) the standard density must be **scale-invariant** (`κ dA → α⁰`; the `/q^{5/2}` one
scales as `1/c`); (ii) an odd-`r` constant should carry a `√q`-type factor (parity law)
— the `/q^{5/2}` version is rational, a tell.

The control is the same either way: `K_GK = e_3(P H P)/q^{3/2}` (full Gauss–Kronecker),
`∫_S K_GK dA = vol(S³) = 2π²` (Gauss-map degree, convex body).

---

## 1. Objects

- **Surface:** `F = Σ_{i=1}^4 y_i² + Σ_{i<j} y_i y_j − c = 0`. Hessian `H = I + J`
  (`J` = all-ones). Quadratic form `M = (I+J)/2`, eigenvalues `{5/2, ½, ½, ½}` —
  **positive definite ⟹ S is a compact ellipsoid ≅ S³, convex.**
- **Standard channel density:** `κ_{3;3,0} = − e_3(P Hc P)/q^{3/2}`, `Hc = J − I`,
  `g = Hy`, `q = |g|²`, `P = I − g gᵀ/q`. `e_3` = sum of 3×3 principal minors.
- **Compactness ⟹ the exactness test is `∫_S κ dA = 0?`** (on a compact oriented `M^m`,
  a top-form is exact iff its integral vanishes).

---

## 2. The proof

**L1 (compression determinant).** For `P = I − ν νᵀ`, `|ν|=1`, and symmetric 4×4 `A`,
`e_3(P A P) = det(A|_{ν^⊥}) = νᵀ adj(A) ν`.

**L2 (Gauss map).** `ν = g/√q` is a diffeo `S → S³` (S convex); `P = I − ν νᵀ`; and
`∫_S f·K_GK dA = ∫_{S³} f dΩ`. With `φ := κ_{3;3,0}/K_GK`,
```
∫_S κ_{3;3,0} dA = ∫_{S³} φ dΩ ,   φ = − e_3(P Hc P)/e_3(P H P) .
```
(Both `e_3`'s carry the same `q^{3/2}`, so it cancels in `φ` — leaving no explicit `q`.
Contrast the auxiliary object, whose extra `1/q` survived into `φ` and produced a
spurious cancellation.)

**L3 (the two `e_3`'s).** `adj(H)=5I−J`, `adj(Hc)=3I−J`, so with `σ = Σν_i`:
```
e_3(P H P) = 5 − σ² ,   e_3(P Hc P) = 3 − σ²   ⟹   φ = − (3 − σ²)/(5 − σ²) .
```
**The `(5 − σ²)` does not cancel** — this is the crux; it is why the answer is
irrational.

**L4 (sphere reduction).** Write everything through `σ² = 4ω²`, `ω = ν·(ones)/2` (the
component along the all-ones unit axis); on `S³` the marginal of `ω` is `∝ √(1−ω²)`.
Split `(3−σ²)/(5−σ²) = 1 − 2/(5−σ²)`:
```
∫_{S³} dΩ = 2π² ,
∫_{S³} dΩ/(5−σ²) = π²(1 − 1/√5)      [from ∫_{−π/2}^{π/2} dθ/(1+4cos²θ) = π/√5,
                                       via t=tanθ ⟹ ∫₀^∞ 2dt/(5+t²)],
∫_{S³} (3−σ²)/(5−σ²) dΩ = 2π² − 2·π²(1 − 1/√5) = 2π²/√5 .
```

**Assemble.**
```
∫_S κ_{3;3,0} dA = ∫_{S³} φ dΩ = − 2π²/√5 .                        ∎
```

Ratio form: `∫κ/∫K_GK = −1/√5` (numeric grid check: `−0.4472135955` to 10 digits).

---

## 3. Where the √5 comes from (the one-line "why")

The channel constant is `−2π²·⟨(3−σ²)/(5−σ²)⟩_{S³}` up to `vol`. The `√5` is exactly
`√(A(A+B))` with `A=1, B=4` from `∫dθ/(A+B cos²θ)=π/√(A(A+B))` — i.e. from the eigenvalue
gap of `M` (the `5/2` vs `1/2`, ratio 5). Equivalently `√5 = √(n+1)`. This is the
odd-`r` parity `√q` showing up at the level of the *integral*; the auxiliary `1/q`
normalization killed it, which is why that version looked (misleadingly) rational.

---

## 4. General n (top order r = n−1) — REDO owed

The auxiliary-normalization general formulas (`−(n−2)/(2c(n+1))`, `−1/(n+1)`) are
**void**. Re-derive with the standard `q^{(n−1)/2}`:
```
φ = −((n−1) − σ²)/((n+1) − σ²),   ∫_S κ dA = − ∫_{S^{n−1}} ((n−1)−σ²)/((n+1)−σ²) dΩ .
```
`n=4` gives `−2π²/√5`. Expect a `√(n+1)` odd-parity factor for every n (from
`∫dθ/((n+1) − n·cos²θ)`-type reductions). Worth doing cleanly and confirming
numerically at `n=5` before banking a general law. *(The r=3-with-n>4 case, where `e_3`
is no longer the full compression determinant, is still a separate open thread.)*

---

## 5. Rigor points to nail by hand

1. **L1** — compression-determinant lemma `e_{n−1}(PAP)=νᵀadj(A)ν` on `|ν|=1` (cofactor
   expansion, or eigenvalues of the compression). Include the bordered-minor identity
   `det[[Hc,g],[gᵀ,0]]=−q·e_{n−1}(PHcP)` as the bridge that pins the `q^{(n−1)/2}` power.
2. **L2** — Gauss map is a diffeo because `S` is convex (`M`≻0 ⟹ all principal
   curvatures same sign ⟹ `K_GK>0`); orientation is consistent; the pullback statement
   `K_GK dA = N*(dΩ_{S³})` is standard.
3. **L4** — the reciprocal integral: `∫_{S³}dΩ/(5−σ²)=π²(1−1/√5)`; the only nontrivial
   piece is `∫dθ/(1+4cos²θ)=π/√5` (elementary, `t=tanθ`). The `S³` one-coordinate
   marginal `∝(1−ω²)^{(n−3)/2}` (here `(1−ω²)^{1/2}`) is standard.

---

## 6. Optional: the §I.3b Johnson route

v1.1 §I.3b gives the r=2 sibling `−q·e_2(P Hc P) = q·Σ_e h_e² − |H_c g|²` and the
Johnson-operator shadow law. A §I.3b-style closed form for `e_3(P Hc P)` would re-derive
L3 in role-channel language; here L1+L3 via the adjugate is the shortest path.

---

## 7. Files

- `reports/arithmetic_track/arith_i_stageB_proof.py` — corrected symbolic proof
  (`f2f851ea`, `−2π²/√5`).
- `reports/arithmetic_track/arith_i_stageB_verdict.py` — the numeric grid integrator
  (`843a7689`); as written it integrates the *auxiliary* `/q^{5/2}` density (annotated);
  change the exponent `2.5→1.5` to integrate the standard channel (ratio `−1/√5`).
- `campaigns/ARITH_I_higher_cohn_vossen/CORRECTION_2026-07-06_channel_normalization.md`
  — the normalization case law.
- `STAGE_B_VERDICT.md` (corrected header), `OPEN_B1_RESOLVED.md` (surface/density refs).
