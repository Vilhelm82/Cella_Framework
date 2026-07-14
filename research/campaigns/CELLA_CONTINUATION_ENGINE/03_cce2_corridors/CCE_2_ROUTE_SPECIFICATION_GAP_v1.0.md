# CCE-2 exact-route specification gap v1.0

**Date:** 2026-07-14  
**Verdict:** **CCE-2 not admitted — exact corridor representative is absent**

## Evidence

The Stage-3 authority states only:

```text
Fix the standard based path from sigma=1 to a small circle about +i through
the upper half-plane, wind once, and return on the same stem.
```

The lower route is defined analogously. It does not specify the stem as exact
segments, the circle radius and basepoint, a rational/algebraic
parameterization, an exact tube, or a clearance lower bound.

Theorem 7F.1 refers back to those “lifted Stage-3 corridors” and asks the reader
to choose thin tubular neighborhoods avoiding the discriminant, marked-point,
pole, norm-discriminant, polar-divisor, and swept-boundary collision loci. This
is an existence-level corridor statement, not a machine-readable exact path
manifest.

The exact Stage-2 and Stage-3 verifiers pass **17/17** and **22/22** gates,
respectively. Their gates certify the algebraic involution, pole motion,
lateral/meridian coefficients, surface identities, and boundary obstruction.
They contain no exact segment, arc, winding-chain, tube, or clearance gate.

## Failed obligation

CCE-2 requires exact `ell_up` and `ell_down` representatives before it may
claim path identity, branch continuation, winding, or positive clearance.
Substituting the phrase “standard based path” would violate the handoff.

## Required separate lemma

A route-specification lemma must provide, for each corridor:

1. an exact piecewise segment/arc parameterization from `sigma=1` back to
   `sigma=1` with the required odd winding;
2. an exact initial lift and proof that `rho` ends on `-sqrt(2)`;
3. exact winding numbers about both `+i` and `-i`;
4. a positive exact tube clearance from `sigma=0`, `rho=0`, `m=0,1,infinity`,
   pole collisions, marked endpoints, and both third-kind poles;
5. for the surface scope, clearance from `v=1/c`, `v=1/c^2`, the norm
   discriminant, polar divisor, and swept-boundary collision locus;
6. exact branch-isolation and overlap witnesses along a finite disk chain.

Until that lemma exists and is independently checked, no CCE-2 path code or
certificate claim is emitted. CCE-0, PF-0, and CCE-1 are unaffected.
