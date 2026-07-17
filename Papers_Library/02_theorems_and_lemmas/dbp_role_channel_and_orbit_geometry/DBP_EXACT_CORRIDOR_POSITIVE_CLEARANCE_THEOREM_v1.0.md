# Theorem — exact DBP corridors and positive clearance v1.0

Let `U^o=C\{0,+i,-i}` and let `rho^2=1+sigma^2`.  Define `gamma_up` by the
ordered vertices

```text
(1,0), (1/2,1), (1/2,3/2), (-1/2,3/2),
(-1/2,1/2), (1/2,1/2), (1/2,1), (1,0),
```

and define `gamma_down` by complex conjugating every vertex.  Coordinates are
ordered rational pairs `(Re sigma, Im sigma)` and consecutive pairs are joined
affinely.

## Claim

The unique path lifts `ell_up,ell_down` beginning at
`u_+=(1,+sqrt(2))` end at `u_-=(1,-sqrt(2))`.  Moreover:

1. `gamma_up` has a counterclockwise local square, reduced word `a_+`, and
   winding vector `(wind_0,wind_+i,wind_-i)=(0,1,0)`.
2. `gamma_down` is the conjugate clockwise representative, has reduced word
   `a_-^(-1)`, and winding vector `(0,0,-1)`.
3. Both paths and the open radius-`1/8` base tube avoid `0,+i,-i`; the
   nonsingular pullback cover and every curve-level divisor in the divisor
   reduction artifact have the positive rational bounds certified there.
4. The upper return stem has `Im(m)<0` and selects `delta_-^up`; the lower has
   `Im(m)>0` and selects `delta_-^down`.
5. In relative homology modulo `Lambda_ell=Z[A]+Z[B]`,

   ```text
   G_up[delta_+]   = [delta_-^up],
   G_down[delta_+] = [delta_-^down].
   ```

## Proof

The stem and reverse stem cancel as an exact path word.  The remaining upper
square is counterclockwise about `+i`; its conjugate is clockwise about `-i`.
This structural decomposition proves the displayed reduced words, not merely
their abelian winding vectors.  It is the exact replacement permitted by the
Stage-3 corridor theorem: Stage 3 specifies an upper-half-plane local
generator and the conjugate lower construction, while its transported class
is taken modulo compact `A/B` cycles.  Reversing an odd local branch meridian
changes only the compact Picard–Lefschetz correction at that quotient level;
the explicitly recorded small-loop orientation retains the information needed
by any later absolute-period refinement.

For each affine segment `z(t)=z_0+td` and each puncture `a`, the verifier
minimizes the exact quadratic `|z(t)-a|^2` at `t=0`, `t=1`, or the rational
stationary point.  Every minimum is positive.  The route bounds are
`|sigma|>=1/2`, distance to the enclosed branch `>=1/2`, distance to the other
branch `>=1`, and `|sigma|<=2`.  Subtracting `1/8` proves positive tube bounds
`3/8,3/8,7/8`.

An ordered chain of 29 rational disks of radius `1/4` covers the seven
segments.  Every closed disk avoids all three punctures and consecutive disks
contain a displayed rational midpoint in their strict intersection.  The
unbranched double cover over each disk has two analytic sheets; the initial
isolator and overlap component determine exactly one continued root.  Odd
branch winding gives deck parity `-1`, hence the terminal isolator contains
`-sqrt(2)`.  This is unique path lifting in the pullback cover, not a false
global section over the odd-winding tube.

The identities and rational inequalities in
`DBP_EXACT_CORRIDOR_DIVISOR_REDUCTION_v1.0.md` carry these base bounds to every
curve, denominator, pole, endpoint, and pole-pair divisor.  Finally the exact
sign argument in `DBP_CORRIDOR_LATERAL_CALIBRATION_v1.0.md`, valid for the
explicit interval `0<h<=1`, proves the two pole-side selections.  The Stage-3
relative transport theorem then gives the stated quotient classes.  This
proves the claim.

## Scope boundary

This theorem certifies the base route, its unique path lifts, the regular
pullback cover, and the curve family with marked endpoints and third-kind
poles.  Surface-sweep clearance is not certified and remains a CCE-6
obligation.  Paper III is not edited by this result.
