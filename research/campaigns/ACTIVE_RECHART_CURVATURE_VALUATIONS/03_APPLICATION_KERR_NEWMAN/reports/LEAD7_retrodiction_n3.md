# LEAD-7 — the n=3 complementarity retrodiction tier (g_F(u=0), Kerr-Newman)

**Date:** 2026-07-07. Certificates: `verification/lead7_test5_pole_orders_n3.py` (orders,
12/12 ×2), `verification/lead7_test6_pole_coeffs_n3.py` (reflection coefficients, 5/5),
`verification/lead7_test7_extremal_coeff_n3.py` (extremal coefficient exact rational form,
4/4 ×2), and `verification/lead7_test8_extremal_gate_graphnorm.py` (extremal `N_ext` gate
CLOSED for the graph-norm metric — full-edge coefficient-positivity certificate, byte-stable
×2; the `_replacement.py` variant is refuted (wrong metric) and `_extremal_gate.py` is the
superseded Sturm-reduction path), `verification/lead7_test9_corner.py` (double-reflection
Schwarzschild corner: order 2, Newton wedge, closed-form metric limits, mixed term — clean ×2),
and `verification/lead7_test10_reflection_lemma.py` (general parity-fixed normal form
`R=−m(m+5)/B·x⁻⁴`, first-principles Ricci `m=1,2,3` — clean ×2). Curvature harness = the
exact-partial 3D Ricci validated in Test 2 (flat ℝ³→0, 3-sphere →6/a²). Domain: the outer physical wedge
`W₊={S,J,Q>0, U_S>0}` (Test 4). This is the KN analogue of the paper's n=2 RC-5 retrodiction
tier (`C_ext`, `C_sch`).

## The order law (SYMBOLIC — no fitted exponents)

`R[g_F(u=0)]` diverges at the three role divisors with **exact integer** pole orders. Both
orders now follow from closed-form Laurent normal forms, not numeric fits (Test 5's
high-precision fits are a consistency cross-check, not the source):

| divisor | coordinate | order | type | how it's fixed (symbolic) |
|---|---|---|---|---|
| extremal `T=0` | `δ = S − S_ext`, `S_ext=π√(4J²+Q⁴)` | **3** | generic | generic Laurent δ⁻³ lemma (Test 7 T7-a) + `A₂>0` (T7-e: `A₂` = δ²-coeff of `G_S` identically, a sum of positives) + `C_ext<0` (Test 8) |
| `Ω=0` | `J` | **4** | reflection-fixed | `−m(m+5)/B` lemma at `m=2` (Test 10) + `B_J>0` (Test 6) |
| `Φ_e=0` | `Q` | **4** | reflection-fixed | `−m(m+5)/B` lemma at `m=2` (Test 10) + `B_Q>0` (Test 6) |

This is the n=3 realization of the paper's Result-6 law (order-3 generic / order-4
reflection-fixed), now with **both** charge reflections (`Ω=0`, `Φ_e=0`) as the
reflection-fixed pair and the extremal edge as the generic divisor.

## The parity-fixed inverse-channel normal form (Test 10, symbolic — general `m`)

**General lemma (Will's `m(m+5)`).** The `−14/B` reflection identity is the `m=2` case of a
normal form for *one collapsing coordinate against a flat `m`-dimensional fibre*. For
`ds² = B x² dx² + x⁻² Σ_{α=1..m} A_α dy_α²` (`B>0`, `A_α>0`), a first-principles Ricci
computation gives **exactly**

```
R = − m(m+5)/B · x⁻⁴,     independent of all transverse amplitudes A_α.
```

Verified symbolically for `m=1,2,3` → `R = −6, −14, −24` times `x⁻⁴/B` (`lead7_test10`, clean
×2). The split `m(m+5) = 6m + m(m−1)` is *radial focusing* + *transverse fibre shear*; the
amplitudes drop out because they only rescale a flat fibre (warp curvature sees only `w'/w`,
`w''/w` with `w ∝ r^{−1/2}` after `r = √B x²/2`). **Asymptotic corollary:** with `y`-dependent
`B(y), A_α(y)` and even subleading terms, the leading Laurent coefficient is `−m(m+5)/B(y)`.
For a 3D state space (KN) `m=2`, giving `14` — so `C_Ω = −14/B_J`, `C_Φ = −14/B_Q` are
inevitable, not symbolic coincidences.

**As applied to KN (Test 6).** Near a reflection face, even in the small coordinate `x`, with
the collapsing native component `g_x = B(y,z)·x² + O(x⁴)` and the two transverse components
diverging as `x⁻²`, `g_y = A x⁻² + O(1)`, `g_z = C x⁻² + O(1)`:

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

**Metric normalization — the certified metric carries the graph "1+".** The DBP chart norm is
`q_i = 1+|∇f_i|² = 1+(4U+U_a²+U_b²)/U_i²` (the n=2 norm `q0=1+a²+b²`, `recert_gtd_dbp_n2.py`),
so `G_i = q_i²·U_i⁶/(4U)·Σ(1/D²) = (U_i²+4U+U_a²+U_b²)²·U_i²/(4U)·Σ(1/D²)`. The `+U_i²` (the
"1+") is **essential**: the graph-norm metric reproduces the banked direct-curvature `C_ext`
values EXACTLY (−0.0660176096, −0.0727822594, −0.000549074077 above), whereas dropping it to
`|∇f|²` gives −0.0656…, −0.0727…, −0.0002345… . It matters only in the finite *transverse*
channels: on a collapsing channel `U_i→0` makes `q_i→∞`, so the "1+" washes out and `A₂`,
`C_Ω`, `C_Φ` are normalization-independent (`B_J` identical to 10+ digits either way). An
earlier gate script (`lead7_test8_extremal_gate_replacement.py`) dropped the "1+" and is
therefore **refuted as the LEAD-7 certificate** (kept only as the record of the mis-step).

**The `N_ext` gate — CLOSED for the graph-norm metric by a full-edge coefficient-positivity
certificate (`verification/lead7_test8_extremal_gate_graphnorm.py`, byte-stable ×2).** The pole
is order 3 wherever `N_ext≠0`, i.e. wherever `C_ext≠0`. Closed unconditionally on the whole
open edge:
1. *Sign reduction:* since `A₂>0`, `g_JJ|ext>0`, `g_QQ|ext>0`,
   `sign(C_ext) = sign(∂_S log(g_JJ g_QQ))|_ext =: sign(L_ext)` — the gate is exactly
   *"`g_JJ·g_QQ` is strictly decreasing in `S` at the extremal surface"* (drops the `A₂`
   division and the huge numerator).
2. *Edge parametrisation:* write `q=Q²>0`, `t=S/(πQ²)>1`; then `L_ext = −P/D` for polynomials
   `P,D` in `(q,t,π)`.
3. *Coefficient positivity:* after extracting positive monomials in `π,q,t` and substituting
   `t=1+r` (`r>0`), `π²=9+b` (`b>0`, from `π>3`), each residual factor is a nonzero polynomial
   in the positive variables `q,r,b` with nonnegative coefficients, hence positive. `D` factors
   into **nine** such factors. `P` is quadratic in `q`, `P=A q²+B q+C`; `B,C` are
   coefficient-positive, and (after removing a positive monomial) `A=C₀·π²t²·(π²F+G)` with
   `F(t)=(t−1)·t³(t+3)³·H̃(t)`, `H̃=2t⁵+5t⁴−15t³−7t²+15t+8` of degree 5 and positive on `[1,∞)`
   (Sturm), so `F>0` for `t>1`; a second Sturm count gives `9F+G>0` on `[1,∞)`. Since `π²>9`
   and `F>0`, `π²F+G=(π²−9)F+(9F+G)>0`, so `A>0`. Therefore `P>0`, `D>0`, `L_ext=−P/D<0`.

**Status — CLOSED.** `C_ext<0` at *every* open point of the extremal edge (not merely on a
dense grid). This upgrades the extremal theorem from "generic open points" to **all open points
of `T=0`**: the extremal pole has exact order 3 throughout, completing the fully symbolic
retrodiction. (The earlier one-variable Sturm reduction on the `Q=1` slice — too slow for a
short-timeout run — is subsumed: the coefficient-positivity route needs only two bounded
low-degree Sturm counts.)

## The double-reflection (Schwarzschild) corner (Test 9)

Where the two order-4 faces `Ω=0` and `Φ_e=0` meet — the Schwarzschild ray `J=Q=0`, `S=s`
free — the curvature is **milder, not wilder**. Approach along `Q=ε`, `J=ρε^a`:

- **Metric corner limits (closed form, graph-norm),** `N₀(s)=s/π+1/(16π²)`:
  `ε⁶ G_S → N₀²s⁵/[π(s+8πρ²)²] = (16πs+1)²s⁵/[256π⁵(s+8πρ²)²]`, `G_J → N₀²πρ²/s`,
  `G_Q → N₀²s/(4πρ²)`. `G_S` collapses as `ε⁶`; `G_J,G_Q` are ε-independent, scale `ρ^{±2}`,
  product `G_JG_Q→N₀⁴/4` ρ-independent. The schematic `s⁷/[π³(s+8πρ²)²]` drops the graph-norm
  `U_S²=1/(16π²)` term; exact/schematic `= (1+1/(16πs))²` (≈1.04 at s=1, s-dependent).
- **Balanced radial order is exactly 2** (not 4, not 6): `ε²R → R₀(s,ρ)` finite, **negative**
  (`R₀(1,1)=−1801.25`, `R₀(2,1)=−263.64`). The `ε⁻⁶` metric collapse loses four orders to
  inverse-metric contraction + derivative cancellation.
- **Newton wedge:** along `J=ρε^a`, `R ~ ε^{−m(a)}` with `m(a)=max(4a−2, 4−2a)` — vertex
  `(1,2)`, edges `4−2a` (a≤1, Φ side, `m(0)=4`) and `4a−2` (a≥1, Ω side). **Minimum m=2 on the
  balanced diagonal:** the corner is the *mildest* point of the whole boundary.
- **Boundary links (exact residues of `C_Ω,C_Φ`):** `κ_Ω(s)=lim_{Q→0}C_Ω/Q²=−3584π³s/(16πs+1)²`,
  `κ_Φ(s)=lim_{J→0}C_Φ/J²=−14336π⁵/[s(16πs+1)²]`, with `ρ⁴R₀→κ_Ω` (ρ→0), `R₀/ρ²→κ_Φ` (ρ→∞).
- **Genuine mixed term:** `R₀` is *not* the two-face sum — `R₀(1,1)=−1801.25` vs superposition
  `κ_Ω+κ_Φ=−1711.56`, an excess `M=−89.70` (the cross term in `G_S`'s mixed denominator that
  neither single face resolves). So state `R₀<0`, but not as `−κ_Ω/ρ⁴−κ_Φρ²`.

All in `lead7_test9` (exact-partial curvature, clean ×2; the κ's are exact symbolic residues).

## Status of the n=3 complementarity

| piece | tier |
|---|---|
| metric identified & u=0 selection | **proven** (Test 3 + Test 4 structural) |
| interior-cleanliness (no spurious poles) | **theorem** (Test 4, on `W₊`) |
| pole **orders** 3/4/4 | **symbolic** — extremal 3 via generic δ⁻³ lemma (Test 7 T7-a) + `A₂>0` (T7-e) + `C_ext<0` (Test 8); reflection 4 via `−m(m+5)/B` at `m=2` (Test 10) + `B≠0` (Test 6). Test 5 high-precision fits are a cross-check, not the source |
| reflection-fixed **coefficients** `C_Ω`, `C_Φ` | **exact closed form** (Test 6), matched to curvature; `= −14/B` = the `m=2` case of `−m(m+5)/B` |
| extremal **coefficient** `C_ext` | **exact closed form** (Test 7), matches curvature to ~10⁻¹³; `A₂` = δ²-coeff of `G_S` identically (T7-e); order-3 at **all** open points — `N_ext` gate **closed** (Test 8) |
| **parity-fixed normal form** `R=−m(m+5)/B·x⁻⁴` | **theorem** (Test 10, first-principles Ricci `m=1,2,3`); amplitude-independent; the reusable lemma behind 3/4/4 |
| **double-reflection corner** (Schwarzschild) | order **exactly 2** (mildest boundary point), Newton wedge `max(4a−2,4−2a)`, closed-form metric limits, nonzero mixed term (Test 9) |

**Fully symbolic — no fitted exponents survive.** Both boundary types stand on closed-form
Laurent normal forms: reflection faces on `−m(m+5)/B` (Test 10), the extremal edge on
`C_ext = A₂⁻¹∂_S log(G_JG_Q)|_ext < 0` (Test 7 structural identity + T7-e `A₂` identification +
Test 8 sign). All three leading coefficients are exact closed forms matching direct curvature;
the orders 3/4/4 follow symbolically. Test 5's high-precision order fits are retained only as an
independent numeric cross-check. (Optional remaining, LEVER payoff: the physics-novelty writeup.)
