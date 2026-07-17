# ARITH-I — Stage A COMPLETE (T-A closed for the whole family)

**Date:** 2026-07-06. **Supersedes** `CLOSE_STAGE_A.md` (which closed Stage A
"keystone-only" under the now-VOID fabricated stop condition —
`CORRECTION_2026-07-06_fabricated_stop_condition.md`). PREREG `32f2fb3a`.
Scripts, all byte-stable ×2: open pins `verification/arith_i_open_pins.py`
(`a2ef103d`); `reports/arithmetic_track/arith_i_stageA.py` (`ba9f270e`);
`arith_i_stageA_s2.py` (`b2d29718`); **`arith_i_stageA_family.py` (`4d60e109`)**.
Paper-track fence: no engine priority changed.

## Verdict

**Stage A COMPLETE. Target T-A is met for the entire quadric family**, not just the
keystone. Every constant in the primary closed form is now an OUTPUT of `s`:

```
INT_S K_G dA = -2 L(s),
L(s) = 2 g(s) [ Pi(n(s); k^2(s)) - (1 - C(s)) K(k^2(s)) ],

  r(s)   = sqrt(1 + s^2)
  k^2(s) = A(s) = 1/2 - 1/(2 r)                     (Legendre modulus^2, proven by
                                                     branch-point cross-ratio, SB-2)
  C(s)   = (r - 1)/(r + 1)
  n(s)   = (A - C)/(1 - C)   < 0                     (third-kind characteristic;
                                                     regular/hyperbolic Pi, no pole)
  g(s)   = 2 sqrt( (1 - A) / (C (1 - C)) )           (Byrd-Friedman period constant)
```

Equivalently, in the Booth weight normalization,
`INT_S K_G dA = -[ W_K(s) K(A) - W_Pi(s) Pi(n;A) ]`, `W_Pi(s)=4g`, `W_K(s)=4g(1-C)`.

## The derivation (first-principles, no cited Booth normal form)

1. **r=2 reduction + algebraic collapse (session 1).** `speed^2` of the spherical
   link collapses exactly to `(C+nu sin^2 t)/(1+nu sin^2 t)`, `nu=(A-C)/(1-A)`.
   `INT_S K_G dA = -2L` corroborated by two independent numeric routes (direct
   surface-curvature quadrature vs link length) at s∈{1/2,1,2}.
2. **Modulus proven (session 2, SB-2).** The differential's curve is
   `Y^2=(C+nu x^2)(1+nu x^2)(1-x^2)`; cross-ratio of its four branch points is
   `lambda = A(s)` exactly. So `k^2(s)=A(s)`.
3. **K-2 closed family-wide (session 2, SB-1).** `Phi_2(j_reg(s), j_lambda(s)) ≡ 0`:
   the CALC-24 register curve is 2-isogenous to the differential's modular curve for
   all s. `j_lambda(s)=(1728s^6+6912s^4+9216s^2+4096)/(s^6+s^4)`.
4. **Family-tier closed form (this session).** Substituting `x=sin t, v=x^2` gives
   `L = 2 INT_0^1 (C+nu v)/sqrt(Q) dv`, `Q=v(1-v)(1+nu v)(C+nu v)`. Key correction to
   the first attempt: `Q = -nu^2 (v-0)(v-1)(v-c)(v-d)`, so the Byrd-Friedman period
   constant keeps a `1/|nu|` factor: `I_0 = INT dv/sqrt(Q) = g K(A)` with
   `g = 2 sqrt((1-A)/(C(1-C)))`. The Moebius map `v = sin^2 phi/(u + w sin^2 phi)`,
   `u+w=1`, gives `I_1 = INT v dv/sqrt(Q) = (g/w)[K(A) - Pi(-w/(1-w); A)]`; solving,
   `w = |nu| = -nu` exactly, so `n = -w/(1-w) = nu/(1+nu) = (A-C)/(1-C)`. Then
   `L = 2C I_0 + 2 nu I_1` collapses to the boxed form.

**The keystone is a special case, reproduced symbolically:** `n(1) = (4-3 sqrt2)/8`
(the underived Booth characteristic — now derived), and the weights become
`4g(1) = 2^(7/4)(3+2 sqrt2)`, `4g(1)(1-C(1)) = 2^(7/4)(2+2 sqrt2)` — the certified
Booth weights, as OUTPUTS. `-2L(1)` = the standing 40-digit constant.

## Why the earlier "naive generalization" was refuted yet the real one is clean

Session 2 refuted `n=(4-3r)/8` (naive r-substitution) — correctly: the true
`n(s)=(A-C)/(1-C)` is a different function of `r` that merely *coincides* with
`(4-3√2)/8` at `s=1`. The five-minute discriminator did its job (it killed a wrong
guess); the right form came from the actual Legendre reduction, not pattern-matching.
Both facts stand and are banked.

## Kills

K-1 clean (keystone constant retrodicted), K-4 clean (`n` emerges — now for all s),
K-2 CLOSED family-wide. K-3 belongs to Stage B.

## Handoff to Stage B (r=3 exactness discriminator)

The r=2 density is exact (the algebraic collapse is its signature). Stage B: exhibit
the explicit r=2 algebraic primitive `eta` (`d eta = density`) as the validation of
the primitive-ansatz machinery, then run the ansatz search at r=3 (Route 1) with the
bump-deformation numeric corroboration (Route 2), K-3 armed. If r=3 is non-exact, the
banked `j_lambda(s)` and the family isogeny feed the transcendence branch (C2).
