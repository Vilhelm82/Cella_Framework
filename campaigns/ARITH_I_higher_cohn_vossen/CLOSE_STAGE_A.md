# ARITH-I — Stage A CLOSE (keystone-complete, K-2 closed family-wide)

**Date:** 2026-07-06 (two sessions, the hard stop-condition budget). **PREREG:**
`32f2fb3a`. **Open pins:** `verification/arith_i_open_pins.py` `a2ef103d` (15/15 ×2).
**Scripts:** `reports/arithmetic_track/arith_i_stageA.py` (`ba9f270e`, 11/11 ×2) +
`arith_i_stageA_s2.py` (`b2d29718`, 6/6 ×2). **Notes:** `ARITH_I_STAGE_A_SESSION1.md`,
this file. Paper-track fence: no engine priority changed.

## Verdict

**Stage A CLOSED — keystone-complete.** The campaign's core target (T-A) is met at
the keystone: the r=2 total-curvature reduction is derived first-principles, the
underived characteristic `n = (4−3√2)/8` and the Booth weights `(3+2√2), (2+2√2)`
**emerge as outputs** of the eigenvalue algebra (not cited from Booth), and the
certified constant is retrodicted by two independent routes. The kill conditions
K-1 and K-4 are clean; **K-2 is closed family-wide**; K-3 belongs to Stage B.

## What was established

1. **The r=2 algebraic collapse (exact, symbolic — SA-2).** The spherical-link
   speed² collapses from a four-term radical to a single ratio of quadratics,
   `speed²(t) = (C + ν·sin²t)/(1 + ν·sin²t)`, `ν=(A−C)/(1−A)`, proven as a sympy
   identity. The quadratic-in-`cos²t` terms cancel identically — the concrete
   signature that the r=2 density is exact (why the constant is *end data*).

2. **The reduction `∫∫_S K_G dA = −2L` (SA-3).** Corroborated at s∈{½,1,2} by two
   independent numeric routes — a direct 2D surface-curvature quadrature of the
   certified `−12s²/q²` vs the 1D link arc length — agreeing to ~17 digits. The
   Cohn-Vossen-type collapse of a 2D integral to `−2×` a 1D length, now in `s`.

3. **The curve modulus is `k²(s) = A(s)` (SB-2, proven).** The arc-length
   differential lives on `Y² = (C+νx²)(1+νx²)(1−x²)`; the cross-ratio of its four
   branch points is `λ = A(s)` exactly. So
   `k²(s) = A(s) = ½ − 1/(2√(1+s²))` is the genuine Legendre modulus² (this pins
   the session-1 SA-5 scoping: the modulus was left open there, it is A(s)).

4. **K-2 CLOSED family-wide (SB-1).** The classical modular polynomial vanishes
   identically in `s`:

   ```
   Φ₂( j_reg(s), j_λ(s) ) ≡ 0 ,
   j_reg(s) = (1728s⁶−1728s⁴+576s²−64)/(s⁶+2s⁴+s²)          [CALC-24 register]
   j_λ(s)   = (1728s⁶+6912s⁴+9216s²+4096)/(s⁶+s⁴)           [differential curve]
   ```

   The CALC-24 register curve is 2-isogenous to the r=2 total-curvature
   differential's modular curve **for every shear**, not just the keystone. The
   family `F_s = D²+sDS+P²−3` retrodicts the register up to the certified index-2
   isogeny (`Φ₂(128,10976)=0` at s=1, close-off §4, now a family identity). K-2
   does not fire.

## Refuted (banked negative results — the discriminators the BRIEF mandates)

- **Naive Booth generalization REFUTED (SB-3a).** `n=(4−3r)/8` with weights
  `(3+2r),(2+2r)` (`r=√(1+s²)`) reproduces the keystone (`P^(4/3)=2` at s=1) but
  fails off it (`|P^(4/3)−2|=144` at s=2, in fact complex). The keystone Booth form
  does **not** generalize by naive r-substitution.
- **Polynomial-in-r (K,E) weights REFUTED (SB-3b).** `L(s)=wK(r)K(A)+wE(r)E(A)`
  with `wK,wE` degree-≤3 polynomials in `r`: no fit (held-out residual ~1e-3). The
  natural (K,E) weights are not low-degree rational in `r`.

Both kills validate the BRIEF's standing warning (A3 polar-dual case law): elegant
coefficient-matching is not evidence; the five-minute numeric test earns its keep.

## Parked (family tier) — blocker named

**Family-tier symbolic `n(s), w₁(s), w₂(s)`:** PARKED. Blocker, precisely: the
arc-length reduction is naturally a `(K, E)` combination on the A-curve, while the
Booth `(K, Π(n))` presentation trades `E` for `Π` at a **special value** of the
third-kind parameter; that special `n(s)` is not a naive r-substitution (SB-3 kills
both naive routes). Deriving `n(s)` in closed form requires carrying out the
Legendre reduction of `∫(C+νv)dv/√(v(1−v)(1+νv)(C+νv))` to the `{K(A),E(A)}` basis
with the root-algebra weights (rational in `A,C`, hence in `r`, but not low-degree),
then applying the `Π`↔`(K,E)` special-argument reduction. Bounded, well-posed, and
independent of everything above — it changes no established result, only upgrades the
family tier from EMPIRICAL to symbolic. `k²(s)=A(s)` is already closed-form and
proven.

## Handoff to Stage B

The SA-2 collapse shows the r=2 density is exact; **exhibiting the explicit algebraic
primitive `η` (dη = density) at r=2 is the validation of the primitive-ansatz
machinery** that Stage B then runs at r=3 (the T-B exactness discriminator). Stage B
opens with that r=2 warm-up, then the r=3 ansatz search (Route 1) + bump-deformation
corroboration (Route 2), K-3 armed. `j_λ(s)` and the family isogeny are banked inputs
for the transcendence branch (C2) if r=3 turns out non-exact.

## Ledger

Kills: K-1 clean, K-4 clean, K-2 CLOSED family-wide, K-3 → Stage B. Family tier:
EMPIRICAL (keystone exact, `k²(s)=A(s)` closed, K-2 closed; symbolic weights parked).
