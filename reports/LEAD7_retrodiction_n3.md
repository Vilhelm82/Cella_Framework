# LEAD-7 — the n=3 complementarity retrodiction tier (g_F(u=0), Kerr-Newman)

**Date:** 2026-07-07. Certificates: `verification/lead7_test5_pole_orders_n3.py` (orders,
12/12 ×2) and `verification/lead7_test6_pole_coeffs_n3.py` (reflection coefficients, 5/5).
Curvature harness = the exact-partial 3D Ricci validated in Test 2 (flat ℝ³→0, 3-sphere
→6/a²). Domain: the outer physical wedge `W₊={S,J,Q>0, U_S>0}` (Test 4). This is the KN
analogue of the paper's n=2 RC-5 retrodiction tier (`C_ext`, `C_sch`).

## The order law (Test 5, certified)

`R[g_F(u=0)]` diverges at the three role divisors with **exact integer** pole orders, at
high precision at `W₊`-interior points:

| divisor | coordinate | order | type |
|---|---|---|---|
| extremal `T=0` | `δ = S − S_ext`, `S_ext=π√(4J²+Q⁴)` | **3** | generic |
| `Ω=0` | `J` | **4** | reflection-fixed |
| `Φ_e=0` | `Q` | **4** | reflection-fixed |

This is the n=3 realization of the paper's Result-6 law (order-3 generic / order-4
reflection-fixed), now with **both** charge reflections (`Ω=0`, `Φ_e=0`) as the
reflection-fixed pair and the extremal edge as the generic divisor.

## The universal reflection-face identity (Test 6-a, symbolic)

**Corrected DBP reflection normal form.** For a diagonal 3D metric that near a reflection
face is even in the small coordinate `x`, with the **collapsing native** component
`g_x = B(y,z)·x² + O(x⁴)` **and the two transverse components diverging as `x⁻²`**,
`g_y = A x⁻² + O(1)`, `g_z = C x⁻² + O(1)`, a symbolic Laurent expansion of the diagonal
Ricci scalar gives

```
R = −14 / B(y,z) · x⁻⁴ + O(x⁻²),
```

depending only on `B`. **The transverse `x⁻²` poles are essential** — with *finite*
transverse components the identity is false (`B x² dx² + dy² + dz²` is flat, `R=0`; an
earlier draft here mis-stated the transverse components as finite). The real KN reflection
faces do carry the transverse `x⁻²` poles (`G_S ~ A/J²` on `Ω=0`, etc.), so the lemma
applies, and each reflection coefficient is `−14` over the collapsing component's leading
coefficient `B`.

## Exact reflection-fixed coefficients (Test 6, certified)

Using the exact mass-charge couplings (Test 4) and the chart norm `q_i`, the collapsing
component's leading coefficient is closed-form, giving:

**Ω=0** (`R ~ C_Ω(S,Q)/J⁴`):
```
C_Ω(S,Q) = −3584·Q²·S⁵·π³·(πQ² − S)²
         / [ (π²Q⁴ + 16π²Q²S² − 2πQ²S + S²)
           · (π²Q⁴ + 16π²Q²S² − 2πQ²S + 16πS³ + S²)² ].
```

**Φ_e=0** (`R ~ C_Φ(S,J)/Q⁴`):
```
C_Φ(S,J) = −14336·J²·S⁵·π⁵·(2πJ − S)²·(2πJ + S)²·(4π²J² + S²)
         / [ (16π⁴J⁴ + 64π⁴J²S² − 8π²J²S² + S⁴)
           · (16π⁴J⁴ + 64π³J²S³ + 64π⁴J²S² − 8π²J²S² + 16πS⁵ + S⁴)² ].
```

Both are `−14/B` with `B` the closed-form collapsing-component coefficient
(`C_Ω = −14/B_J`, `C_Φ = −14/B_Q`; see the certificate for `B_J, B_Q`). Verified against
direct high-precision curvature (Richardson) to ~20 digits.

**Corner structure.** `C_Ω` carries the factor `(πQ² − S)²`, which vanishes exactly on
`Ω=0 ∩ extremal` (`S_ext = πQ²` at `J=0`); `C_Φ` carries `(2πJ − S)²`, vanishing on
`Φ_e=0 ∩ extremal` (`S_ext = 2πJ` at `Q=0`). The coefficients degenerate precisely where
two role divisors meet — the reflection-face pole "heals" into the generic extremal pole at
the corner. (The `(2πJ + S)²` factor in `C_Φ` is the `J→−J` reflection image, always
present.)

## Extremal coefficient (order 3) — EXACT closed form (Test 7)

The extremal edge is *not* a reflection face: in `(S,J,Q)` coordinates the metric is
analytic (`M=√U` is smooth), only the entropy component collapses (`g_SS ~ A₂δ²`,
`δ=S−S_ext`), the others stay finite, and the pole is odd order 3. A symbolic Laurent
expansion gives the structural identity

```
C_ext = (1/A₂)·(P₁/P₀ + R₁/R₀) = (1/A₂)·∂_S ln(g_JJ·g_QQ)|_{S_ext},
```

with `P₀,P₁ = g_JJ, ∂_S g_JJ` and `R₀,R₁ = g_QQ, ∂_S g_QQ` at extremal (the odd order
comes exactly from the linear-`δ` terms `P₁,R₁`). The collapsing coefficient has the same
shape as the reflection `B`:

```
A₂ = (4U + U_J² + U_Q²)²/(4U) · (1/U_J² + 1/U_Q²)   at extremal.
```

**Rationality.** The implicit-formula couplings `Λ = 2M(U_ii U_a − U_i U_ia)/U_i³`
(`M²=U`) are *rational* in `(S,J,Q,π)` — the radicals only lived in the chart functions,
not the couplings — so `g_JJ, g_QQ`, their `S`-derivatives and `A₂` are rational, and on
the extremal surface `J²=(S²−π²Q⁴)/(4π²)` the whole coefficient is a **rational function
of `(S,Q,π)`**. Its denominator factors as

```
den ∝ Q²π·(3Q²π+S)·(Q⁴π+Q²S−Q²π+S)·(Q⁴π²+4Q²S²π²−2Q²Sπ+S²)
      ·(Q⁴π²+Q²Sπ−Q²π²+2S²+Sπ)³·(Q¹⁰π³+Q⁸Sπ²−9Q⁶S²π³+3Q⁴S³π²+5Q²S⁴π+S⁵),
```

with a long (degree 14 in `S`, 28 in `Q`) polynomial numerator `N_ext`. Verified against
direct high-precision curvature. Sample values (on the extremal surface, in `(S,Q)`):
`C_ext(20,1) = −0.0660176096`, `C_ext(30,1) = −0.0727822594`, `C_ext(20,2) = −0.000549074077`.

**Open gate (honest caveat).** The denominator of `C_ext` is positive on the open edge
(`S>πQ²`); the numerator `N_ext` has *not* been sign-certified there. So the pole is order 3
at every open extremal point **where `N_ext≠0`** — i.e. generically. Proving `N_ext` has
fixed nonzero sign on `{Q>0, S>πQ²}` (or exhibiting its zero locus) would upgrade "generic
open points" to "all open points" of `T=0`. This is the one remaining proof obligation.

## Status of the n=3 complementarity

| piece | tier |
|---|---|
| metric identified & u=0 selection | **proven** (Test 3 + Test 4 structural) |
| interior-cleanliness (no spurious poles) | **theorem** (Test 4, on `W₊`) |
| pole **orders** 3/4/4 | numeric (high-precision fits, Test 5); the reflection orders follow symbolically from the `−14/B` lemma + `B≠0` (Test 6) |
| reflection-fixed **coefficients** `C_Ω`, `C_Φ` | **exact closed form** (Test 6), matched to curvature |
| extremal **coefficient** `C_ext` | **exact closed form** (Test 7); order-3 generic (pending the `N_ext` gate) |

The exact closed forms are established and match direct curvature. Two items remain to make
the retrodiction a **fully symbolic** proof (per the symbolic-proof handoff spec):
(1) the extremal `N_ext` sign gate above; (2) replacing the numeric order fits (Test 5) with
the exact symbolic Laurent lemmas — the generic order-3 lemma `(P₁/P₀+R₁/R₀)/A₂` and the
corrected reflection `−14/B` (transverse `x⁻²`) lemma — applied to the rational metric. The
coefficient values themselves are already exact.
