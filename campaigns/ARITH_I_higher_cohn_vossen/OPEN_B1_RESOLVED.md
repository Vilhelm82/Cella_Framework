# OPEN B-1 RESOLVED — the r=3 surface + density, pinned from surfaced references

**Date:** 2026-07-06. **Trigger:** Will surfaced the two missing [CONTAINER]
references (`dbp_four_role_calc_log_v8.md`, `DBP_STANDING_RESULTS.md`) after Stage B
s1 paused at the family gate — per the standing rule *"always pause work when a
reference document is not in the repo and I'll surface it."* This note records what
they pin (re-verification still applies: values below are retrodiction targets to
re-derive in-repo, never trusted on their face).

## What the references pin

**1. The density `κ_{r;p,q}` (CALC-15/15a).** The channel density is
`Ĉ_r(t,u) =` bordered minors of `M = t·H_c + u·H_s` normalized by `q^{(r+2)/2}`
(the grid normalization); `κ_{r;p,q}` = the `t^p u^q` coefficient. **CALC-15a is
decisive on `H°`:** *"use coupling-mode (H_c) minors (the t^r part), never full
bordered Hessians, or it computes the Gauss–Kronecker object the paper rules out."*
This CONFIRMS Stage B s2 (SBC-3): `H° = H_c` (off-diagonal channel), grid
normalization `q^{(r+2)/2}` — the exact object I isolated by the σ/grid discriminator.

**2. The explicit r=3 pure-coupling density (CALC-32/33).** Per (chart k, 3-subset
`{j,l,m}`), the hollow 3×3 coupling minor collapses (`det[[0,a,b],[a,0,c],[b,c,0]]
=2abc`) to a product of three coupling numerators:

```
D_{k,jlm}(O) = Λ_{k,{j,l}} · Λ_{k,{j,m}} · Λ_{k,{l,m}}   ( = ½ × 3×3 coupling minor )
Λ_{k,{j,l}}  = −(H_{jl} − H_{jk} − H_{kl} + H_{kk})       ( CALC-14 carrier numerator )
κ_{3;3,0}    = D_{k,jlm} / q^{5/2}                        ( grid normalization, r=3 )
```

For the depth-3 Specht realization `S^{(n−3,3)}` the theorem needs `n≥2r=6` (CALC-32:
certified n=6,7; CALC-33/34/35: proven all r, n≥2r). A nonzero `e_3`/coupling-minor
needs `n≥4`.

**3. The canonical n=4 surface (CALC-04, named in CALC-24 Part A).**

```
F = Σ_{i=1}^n y_i²  +  Σ_{i<j} y_i y_j  −  c        (fully-coupled symmetric quadratic)
```

the n-role analog of the keystone; CALC-24 calls the n=4 member "the canonical n=4
surface." The S_n-symmetric jet is the gradient `g=(1,…,1)` (CALC-08/32/33).

## The reframing this forces (a genuine finding — CALC-24 Part A)

> "The total-curvature elliptic period is a 2-surface object … for n≥4 roles the
> surface is (n−1)-dimensional and the invariant changes species (Gauss–Kronecker /
> Chern–Gauss–Bonnet). 'The n-role curvature elliptic period' does not type-check
> past n=3 — the elliptic handle is bonded to the 3-role / 2-surface geometry."

Consequence for ARITH-I: **the r≥3 grid integral is NOT the 2-surface elliptic-period
object the addendum (A4/A5) imagined.** On the n=3 keystone the order axis tops out at
`r=n−1=2` (so `κ_{3;·}` does not exist there — this also explains Stage B s1 SBB-1's
`e_3≡0` at n=3, from the other direction). The genuine r=3 object lives on the n≥4
surface, where it is a top-form on an (n−1)≥3-manifold — an odd-dimensional
Gauss–Kronecker-type integral, not a Riemann-surface period. The `[CONTAINER]` addendum
row that said "∫∫ κ_{r;p,q} dA converges for every slot on the quadric, r≥1" was loose
for r≥3: on the 2-surface those slots don't exist; on the n≥4 manifold the integral is
a volume integral of different species. This is banked as the corrected framing.

## Sharpened T-B (what the r=3 exactness test now asks — precisely)

On the canonical n=4 surface `F = Σy_i² + Σ_{i<j}y_iy_j − c` (a 3-manifold in ℝ⁴), is
the order-3 pure-coupling channel density

```
κ_{3;3,0}(y) = [ Σ_{k=1}^4 Λ_{k,{jlm}}(y) with {j,l,m}={1..4}\{k} ] / q(y)^{5/2}
```

(built from the graph-Hessian at each surface point) **exact** — the top 3-form
`κ_{3;3,0} dV = dω` for an algebraic 2-form `ω`? YES → higher Cohn-Vossen for the
channel density (end data); NO → interior period of the n=4 geometry.
Note the FULL Gauss–Kronecker density on this 3-manifold is end-data by the Gauss-map
degree (odd-dim, no Pfaffian) — the CHANNEL density (coupling-only, CALC-15a) is the
non-trivial case, which is exactly why it is the question.

## Method (unchanged, now validated at r=2)

Route 1 = the SBC-4 ansatz, lifted to the 3-manifold: `ω` a 2-form (3 component
functions) with algebraic coefficients (`q`-power / azimuthal-factor denominators),
solve `dω = κ_{3;3,0} dV` by linear algebra; the r=2 grid-channel primitive
(`3c18c25e`) is the validated template. Route 2 = bump deformation, K-3 armed.

## Status

OPEN B-1 CLOSED (surface + density pinned from the references, re-derivation to
follow). Reframing banked. Next: retrodict the density on the n=4 surface (recover the
CALC-32 realization / a keystone-consistent value as the calibration anchor), then run
the r=3 exactness verdict.
