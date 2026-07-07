# LEAD-7 — Theorem: the mass-charge coupling zeros are exactly the role divisors

**Date:** 2026-07-07. Certificate: `verification/lead7_test4_masscharge_zeros.py` (10/10,
byte-stable ×2, SYMBOLIC). Upgrades the interior-cleanliness of the Candidate-F(u=0) metric
(`reports/LEAD7_test3_candF_n3.md`) from a finite numerical scan to a proof.

## Domain (corrected)

Let the Kerr-Newman graph be `M² = U(S,J,Q)`,
`U = S/(4π) + πJ²/S + Q²/2 + πQ⁴/(4S)`. The theorem holds on the **outer physical wedge**
```
W₊ = {S,J,Q > 0, U_S > 0} = {S,J,Q > 0, S² > π²(4J²+Q⁴)},
```
equivalently the outer-horizon branch `S = S₊ = π(2M²−Q²+2√disc)`, `disc>0`. **Not**
`{S,J,Q>0, disc>0}` alone: `disc>0` also contains the **inner** branch `S=S₋` where
`U_S<0`, on which a numerator can vanish in the interior (see the counterexample below).
`U_S>0` is positive Hawking temperature; `W₊` is the thermodynamically physical region and
the domain on which the metric `g_F(u=0)` lives.

## Statement

Each output chart `E_i = f_i(M, E_j, E_k)` solves `M²=U` for `E_i`; its **mass-charge
couplings** are the mixed second partials `Λ_{i,{M,j}} = ∂²E_i/∂M∂E_j` (pairs joining the
graph value `M` to one charge `E_j`).

**Theorem.** On `W₊`, every mass-charge coupling `Λ_{i,{M,j}}` is finite and nonzero. In
the closure `W̄₊`, every numerator zero **and** every native pole of the mass-charge
couplings is supported on
`{J=0} ∪ {Q=0} ∪ {U_S=0} = Ω=0 ∪ Φ_e=0 ∪ T=0`. Consequently the mass-charge inverse-channel
metric `g_F(u=0)_{ii} = q_i²·Σ_{mass-charge j} 1/Λ_{i,{M,j}}²` has **no interior curvature
singularity** — all its curvature divergences lie on the role boundaries.

## Proof (as certified)

**1. Uniform formula.** Implicit differentiation of `M²=U` (chart-independent) gives
```
∂E_i/∂M = 2M/U_i,          Λ_{i,{M,j}} = ∂²E_i/∂M∂E_j = 2M·(U_ii U_j − U_i U_ij)/U_i³.
```
The **pole** is the native divisor `U_i=0` (`U_S=0` ⇔ T=0 for the entropy chart, `U_J=0` ⇔
Ω=0, `U_Q=0` ⇔ Φ_e=0). The **zero** is the numerator `N_{ij} = U_ii U_j − U_i U_ij`.
Verified against explicit differentiation of the solved chart functions `f_S, f_J, f_Q`
for all six couplings (numeric, max mismatch ~10⁻³⁷). *(cert: T4-a)*

**2. Factorization.** The six numerators factor as (exact symbolic identities, cert T4-b):
| coupling | `N_{ij}` factorization | zero locus |
|---|---|---|
| `Λ_{S,{M,J}}` | `(J/2S²)·[π²(4J²+Q⁴)/S² + 1]` | J=0 (Ω=0) |
| `Λ_{S,{M,Q}}` | `(πQ/S²)·[(4J²+Q⁴)(1+πQ²/S)/2S + Q²U_S]` | Q=0 (Φ_e=0) |
| `Λ_{J,{M,S}}` | `(2π/S)U_S + 4π²J²/S³` | U_S=0 ∧ J=0 |
| `Λ_{J,{M,Q}}` | `(2π/S)·Q·(1+πQ²/S)` | Q=0 (Φ_e=0) |
| `Λ_{Q,{M,S}}` | `(1+3πQ²/S)U_S + πQ⁴(1+πQ²/S)/S²` | U_S=0 ∧ Q=0 |
| `Λ_{Q,{M,J}}` | `(2πJ/S)·(1+3πQ²/S)` | J=0 (Ω=0) |

**3. Positivity of `U_S` on `W₊`.** By the horizon Vieta relations (cert T4-c):
`S_± = π(2M²−Q² ± 2√disc)` are the two roots of the entropy quadratic, with
`S_+S_− = π²(4J²+Q⁴)` and `S_+−S_− = 4π√disc`. Hence on the outer branch `S=S₊`
```
U_S = [S² − π²(4J²+Q⁴)]/(4πS²) = √disc / S_+  > 0   on W₊,   = 0 ⇔ disc=0 (extremal).
```

**4. Nonnegative-coefficient brackets.** After clearing positive powers of `S`, each
bracket in the table is a polynomial with **nonnegative** coefficients in the strictly
positive variables `(S,J,Q,U_S,π)` — equivalently, a positive monomial denominator times a
nonnegative-coefficient polynomial (cert T4-d). So each bracket is `> 0` on `W₊`.

**Role of the extremal divisor (corrected).** Generic `U_S=0` (`T=0`) is **not** a
numerator zero: `N_{J,S}` and `N_{Q,S}` vanish only where `U_S=0` **and** (`J=0` or `Q=0`),
i.e. codim-2 corners. `T=0` enters as the **native pole** of the entropy-chart couplings,
through the `U_i³ = U_S³` denominator of the uniform formula.

**Conclusion.** On `W₊` (`J,Q>0`, `U_S>0`), each numerator `N_{ij}` is a product/sum of
strictly-positive quantities, hence `> 0`. So no mass-charge coupling vanishes in `W₊`;
numerator zeros occur only on the boundary faces `{J=0}` (Ω=0), `{Q=0}` (Φ_e=0), or the
corners `{U_S=0}∩{·}` (extremal), and the extremal divisor appears additionally as the
native pole. ∎

**Curvature (analytic).** Each `Λ_{i,{M,j}}` is analytic, finite and nonzero on `W₊`, so
each `1/Λ²` is analytic on `W₊`. Since `q_i>0` in the interior, every diagonal entry
`g_{ii}` is positive and analytic, hence `det(g)=∏_i g_{ii} ≠ 0` on `W₊`. Therefore `g⁻¹`,
the Christoffel symbols, and the curvature tensor/scalar are finite analytic functions on
`W₊`, so no interior curvature singularity occurs. The interior-cleanliness observed
numerically in Test 3 is therefore exact.

## Why the domain must be `W₊` (inner-branch counterexample)

`{disc>0}` is **too big** — it admits an interior numerator zero on the inner branch. At
```
S = π√3/2,  J = 1/4,  Q = 1  ⟹  M² = U = 1/2 + 1/√3,  disc = 1/48 > 0,
```
one has `U_S = −1/(6π) < 0` (inner branch) and `N_{J,S} = (S²+4π²J²−π²Q⁴)/(2S³) = 0`. This
point satisfies `disc>0` but is excluded by `W₊ = {U_S>0}`. So the theorem must be stated on
`W₊`, not on `{disc>0}` (cert T4-e). This is exactly the physical/unphysical split: the
outer horizon has `T>0` (`U_S>0`), the inner horizon `T<0`.

## What this closes, and what remains

- **Closed (now a theorem):** the mass-charge inverse-channel metric `g_F(u=0)` has no
  spurious interior curvature poles; its only singularities are the three physical role
  divisors. Combined with Test 3 (orders 3/4/4 on those divisors, finite on Davies), the
  complementarity structure of `g_F(u=0)` is established with only the pole *coefficients*
  remaining numerical.
- **The charge-charge contrast (why u=0):** the charge-charge couplings `Λ_{i,{j,k}}` are
  *not* covered by this theorem and do have interior zeros (e.g. `Λ_{Q,{S,J}}=0` at
  (M,J,Q)=(2,0.826,1.699), Test 3 T3-3) — these are the LEAD-2 channel-isotropy strata.
  That is precisely why the metric must exclude them (u=0): including them (u>0) would pole
  in the interior. The theorem makes the u=0 selection structural.
- **Remaining for full certification:** the exact pole *coefficients* at each role divisor
  (the KN analogue of the n=2 RC-5 retrodiction tier `C_ext`, `C_sch` in the π-frame). The
  orders 3/4/4 are numeric; a closed form for the leading coefficients would complete the
  retrodiction.
