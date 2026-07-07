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

For a diagonal 3D metric that near a reflection face is even in the small coordinate `x`,
with the **vanishing** component `g_x = B(y,z)·x² + O(x⁴)` and the other two finite, a
symbolic Laurent expansion of the diagonal Ricci scalar gives

```
R = −14 / B(y,z) · x⁻⁴ + O(x⁻²),
```

**independent of every other metric datum** (the two finite components and all subleading
terms drop out). So each reflection-face coefficient is `−14` over the leading coefficient
of the single collapsing metric component.

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

## Extremal coefficient (order 3) — high precision, closed form open

The extremal divisor is a `√disc` branch point (not a reflection face), so the `−14/B`
identity does not apply; only the entropy component collapses (`g_SS ~ δ²`), the others
stay finite, and the pole is odd order 3. Leading coefficients `C_ext(J,Q) = lim_{δ→0}
R·δ³` (high precision):

| (J, Q) | `S_ext` | `C_ext` |
|---|---|---|
| (3, 1) | 19.1096 | −0.06497050672 |
| (2, 1) | 12.9531 | −0.05296128512 |
| (3, 2) | 22.6543 | −0.000862697853 |
| (2, 1.5) | — | −0.00415193621 |

Its exact closed form is the remaining open sub-item of the n=3 retrodiction (a
branch-point Laurent computation, structurally harder than the reflection faces).

## Status of the n=3 complementarity

| piece | tier |
|---|---|
| metric identified & u=0 selection | **proven** (Test 3 + Test 4 structural) |
| interior-cleanliness (no spurious poles) | **theorem** (Test 4, on `W₊`) |
| pole **orders** 3/4/4 | **certified** (Test 5) |
| reflection-fixed **coefficients** `C_Ω`, `C_Φ` | **exact closed form** (Test 6) |
| extremal **coefficient** `C_ext` | high-precision numeric; closed form open |

The n=3 DBP complementarity law is now established for `g_F(u=0)` at the coefficient level
on the reflection-fixed divisors, with only the generic-edge coefficient left to close.
