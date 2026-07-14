# CCE-2R exact-corridor scope lock v1.0

**Date:** 2026-07-14  
**Base commit:** `50683b971399236abe413cafcf2c56c5b1b9228c`  
**Stage:** R0 complete; production edits not yet begun

## Theorem target

Prove and certify two explicit seven-segment paths in the punctured
`sigma`-plane, their unique path lifts from `(1,+sqrt(2))` to
`(1,-sqrt(2))`, a radius-`1/8` regular base tube and its nonsingular pullback
cover, exact curve-family and third-kind-pole clearance, and the terminal
upper/lower lateral selection. The output is a curve-level CCE-2 route
certificate. It does not claim a surface-sweep certificate.

The upper path uses the handoff vertices and a counterclockwise square about
`+i`, hence word `a_+`. The lower path uses the complex-conjugate vertices and
the conjugate clockwise square about `-i`, hence word `a_-^(-1)`. This choice
refines Stage 3's phrase "analogously using the lower half-plane": Stage 3's
pole-side calculation is explicitly the complex-conjugate calculation, while
its transport claim is modulo the compact `A/B` lattice and is unchanged by
reversing the odd local branch loop up to a compact Picard--Lefschetz term.
The selected orientation and that quotient-level invariance must be replayed;
winding parity alone is not corridor evidence.

## Exact curve divisor manifest

The mandatory CCE-2 curve ledger is reduced to the following exact factors.

| Layer | Required noncollision | Exact reduction |
|---|---|---|
| base | punctures and endpoint route | `sigma != 0`, `sigma-i != 0`, `sigma+i != 0` |
| shear cover | regular double cover | `rho != 0`; equivalently `sigma != +/-i` |
| cover denominators | finite `c,m,n` formulas | `rho != 0`, `rho-1 != 0`, `rho+1 != 0` |
| elliptic fibre | distinct `0,1,m,infinity` | `m != 0,1,infinity` |
| derived parameters | `n != 0,1,infinity`, `c != 0,infinity` | the same `rho`, `rho-1`, `rho+1` factors |
| marked endpoints | `Q_0 != Q_m`; neither collides with the third-kind poles | `m != 0`, `x_p != 0,m` |
| pole pair | `P^+ != P^-`; poles avoid elliptic branch points | `y_p^2 != 0`, `x_p != 0,1,m` |
| relative local system | punctures remain distinct from marked endpoints | the preceding marked/pole factors |

The identities to be proved and used for the reduction are:

```text
(rho-1)(rho+1) = sigma^2
m = (rho-1)/(2rho),       1-m = (rho+1)/(2rho)
1-2m = 1/rho
n = -(rho-1)^2/(4rho),    1-n = (rho+1)^2/(4rho)
c = (rho-1)/(rho+1)
x_p = -2/(rho-1)
x_p-1 = -(rho+1)/(rho-1)
x_p-m = -(rho+1)^2/(2rho(rho-1))
y_p^2 = -(rho+1)^3/(rho(rho-1)^3)
```

Thus every mandatory curve collision is excluded by positive lower bounds for
`|sigma|`, `|sigma-i|`, `|sigma+i|`, `|rho|`, `|rho-1|`, and `|rho+1|`, with
the displayed rational functions carrying the bounds to `m,n,c,x_p,y_p^2`.

## Surface boundary

The current CCE-2 model has no surface observable or surface divisor manifest;
it transports a curve route and selected relative class. Clearance from
`v=1/c`, `v=1/c^2`, the norm discriminant, the surface polar divisor, and the
swept-boundary collision locus therefore remains a CCE-6 obligation. No
surface-route certificate or whole-surface conclusion is imported here.

## Frozen authorities

- Stage 3 SHA-256: `bdaabb1a1015f7b6b3055321b422a3b6d84053c808d2e3669ea646ff3de82670`
- Paper III SHA-256: `c5d790829434f848057529ef77ff855e3bc4d9f582e1d766dc2f273b4c76aeb6`
- CCE-2 gap SHA-256: `29a7b7351910ee401b57fbd75112ce613394f90993239f44edc0f0b678f57894`
- PF-0 report SHA-256: `304fccce5ed1206f23969952634d10b250d8d4d7a7a955971afa8018c2372008`
- live DBP provider SHA-256 before R5:
  `2899b471bca4b1cd056e0b3bc61875511b671c29ff6bdebae2df8c4a0a617683`

The stale evaluator-campaign scout has zero production references and is not
an authority or evidence input.

