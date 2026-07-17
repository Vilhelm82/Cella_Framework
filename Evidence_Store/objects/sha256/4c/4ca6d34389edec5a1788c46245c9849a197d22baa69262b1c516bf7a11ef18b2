# ARITH-I Stage A — session 1 note (the r=2 reduction, shear symbolic)

**Date:** 2026-07-06. **PREREG:** `32f2fb3a` (frozen pre-battery). **Open pins:**
`verification/arith_i_open_pins.py` `a2ef103d` (15/15 ×2). **Script:**
`reports/arithmetic_track/arith_i_stageA.py`, 11/11, byte-stable ×2
(sha in the commit). Paper-track fence: sets no engine priority.

## What closed this session

**SA-1 — eigenvalue algebra, symbolic in s.** In the eigen-frame of
`F_s = D²+sDS+P²−3` the surface is `λ₊X²+λ₋Y²+Z²=3`, `λ₊,₋=(1±r)/2`, `r=√(1+s²)`,
`λ₊>0`, `λ₋<0` — hyperboloid of one sheet, χ=0, two cone ends. The asymptotic-cone
link `{λ₊X²+λ₋Y²+Z²=0}∩S²`, projected out of the negative eigen-direction Y, is the
ellipse `(λ₊−λ₋)X²+(1−λ₋)Z²=−λ₋` with closed-form semi-axes

```
A(s) = 1/2 − 1/(2√(1+s²))              (= k², the Legendre modulus²)
C(s) = (√(1+s²) − 1)/(√(1+s²) + 1)
```

Keystone retrodiction (open-pin P3): `A(1) = (2−√2)/4`, `C(1) = 3−2√2`. ✓

**SA-2 — the algebraic collapse (exact).** The link speed² starts as a four-term
radical (two axis terms + the sphere-constraint dY² term over Y²). It collapses,
proven as a sympy identity in (A,C,t), to a single ratio of quadratics:

```
speed²(t) = (C + ν·sin²t)/(1 + ν·sin²t),      ν = (A−C)/(1−A).
```

This is the r=2 "primitive" the stage targets: the arc-length integrand is now a
first/third-kind elliptic form, and `L = 4∫₀^{π/2} √speed² dt`. The derivation (by
hand, machine-confirmed): with `c=cos²t`, numerator and denominator of speed² share
the linear-in-c form `[A(1−C)−(A−C)c]/[(1−C)−(A−C)c]`; the quadratic-in-c terms cancel
identically. This cancellation is the exactness of the r=2 density showing up
concretely — the reason the constant is *end data*.

**SA-3 — the reduction `∫∫_S K_G dA = −2L`, two independent numeric routes.** At
s∈{½,1,2}:
- route α: direct surface integral of the certified curvature `−12s²/q²` against the
  induced area element over the eigen-frame hyperboloid (2D quadrature, Y over the
  whole line via Y=tan p);
- route β: `−2·L(s)` from the SA-2 collapsed speed².

| s | ∫∫K dA (α) | −2L (β) | rel. gap |
|---|---|---|---|
| 1/2 | −2.9270043571 | −2.9270043571 | 2.4e-17 |
| 1 | −5.01049070266 | −5.01049070266 | 6.1e-18 |
| 2 | −7.22101047017 | −7.22101047017 | 1.6e-18 |

The 2D curvature integral collapsing to `−2×` a 1D arc length is the Cohn-Vossen-type
reduction, now corroborated in s (not just at the keystone). **K-1 checkpoint clean**
(direct route agrees with the certified keystone constant at s=1).

**SA-4 — the keystone Booth normal form; n and the weights emerge (K-4 checkpoint).**
`L(1)` from the collapsed speed² reproduces, to 6e-61,

```
L(1) = 2^(3/4)[(3+2√2)·Π(n; k²) − (2+2√2)·K(k²)],   n = (4−3√2)/8,  k² = (2−√2)/4,
```

regular Legendre path only (n<1; no singular ellippi — close-off case law). The
**underived characteristic n = (4−3√2)/8 is now an OUTPUT** of the reduction, and the
two Booth weights (3+2√2), (2+2√2) fall out with it. `−2L(1)` equals the standing
40-digit keystone constant. **K-4 does not fire** at the keystone.

**SA-5 — K-2 reconciliation, scoped (not yet closed).** The Legendre modulus² of the
period curve is `λ = A(s)`; the bare j of that λ-curve is

```
j_λ(s) = 256(1−λ+λ²)³ / (λ²(1−λ)²)
       = (1728s⁶ + 6912s⁴ + 9216s² + 4096)/(s⁶ + s⁴) ,   j_λ(1) = 10976.
```

The CALC-24 register is `j(s) = (1728s⁶−1728s⁴+576s²−64)/(s⁶+2s⁴+s²)`, `j(1)=128`.
These are **different rational functions**, and `10976 / 128` is exactly the
**index-2 isogeny** the close-off certified (`Φ₂(128,10976)=0`, the differential lives
on j=10976, 2-isogenous to the minimal j=128). So a naive "does A(s) reproduce the
register j(s)" comparison would *falsely* fire K-2; the correct K-2 test carries the
isogeny. Per the BRIEF's standing warning on double-cover/branch bookkeeping, this is
deferred rather than forced.

## What remains (Stage A, session 2)

1. **Symbolic-s weight extraction (family tier).** Reduce `L(s)` to `w₁(s)·Π(n(s);k²(s))
   + w₂(s)·K(k²(s))` with `n(s)`, `w₁(s)`, `w₂(s)` as closed forms (not just the s=1
   values). Fallback per PREREG if the CAS blows up: three numeric shears + rational
   fit, degree ≤ 6, family tier EMPIRICAL until symbolic lands. `k²(s)=A(s)` is already
   closed-form.
2. **Close K-2 with the isogeny.** Apply the 2-isogeny (or match via `j_λ(s)` ↔
   register `j(s)` under Φ₂ across ≥3 shears) so the register is retrodicted from the
   family, not merely at the keystone. This also decides whether the family symbol s is
   *identically* the register shear or an isogenous reparametrization.
3. **Exhibit the Gauss–Bonnet 1-form explicitly.** SA-3 corroborates `∫∫K dA=−2L`
   numerically; the symbolic primitive (the algebraic 1-form whose d is the density, so
   Stokes collapses the 2D integral to the link) is the T-A "primitive found" deliverable
   and the natural bridge into Stage B's exactness test at r=3.

## Ledger

Kills armed, none fired: K-1 clean (SA-3 s=1), K-4 clean (SA-4). K-2 scoped, K-3
belongs to Stage B. Family tier: EMPIRICAL (keystone exact; symbolic-s pending item 1).
