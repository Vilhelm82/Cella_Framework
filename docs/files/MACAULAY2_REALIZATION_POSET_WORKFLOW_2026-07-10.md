# Macaulay2 Workflow for the Horizon Wreath-Cover Realization Poset

**Date:** 2026-07-10  
**Companion script:** `horizon_wreath_inertia_model.m2`  
**Purpose:** Determine which higher branch strata are actually realized, without confusing projected sheet crossings with ramification

## 1. Model the incidence cover first

Use the polynomial ring

```text
Q[M,N1,N2,N3,N4,J,u,w1,w2,w3,w4]
```

and the incidence ideal

```text
IX = (
  w1^2-u-N1^2,
  w2^2-u-N2^2,
  w3^2-u-N3^2,
  w4^2-u-N4^2,
  w1+w2+w3+w4-4M
).
```

This retains the normalized radical signs. Do not begin with the quintic eliminant alone: at `N_a^2=N_b^2`, different incidence points can project to the same `u`-root, so the polynomial discriminant sees a collision even when the normalized cover is unramified.

The expected basic checks are

```text
codim IX = 5,
dim(S/IX) = 6.
```

## 2. Compute relative ramification, not merely singularities

For the projection to the observable base, differentiate the five incidence equations with respect to

```text
(u,w1,w2,w3,w4).
```

The determinant is

```text
ramDet = 8 e3(w),
```

where

```text
e3(w)=w1*w2*w3+w1*w2*w4+w1*w3*w4+w2*w3*w4.
```

Therefore the true relative ramification ideal upstairs is

```text
IR = IX+(e3(w)).
```

This ideal is more informative than either `singularLocus(S/IX)` or the discriminant of the eliminated quintic:

- `singularLocus` tests the intrinsic singularities of the incidence space;
- `IR` tests failure of etaleness of its projection to the base;
- the eliminant discriminant also records projected crossings.

## 3. Define the channel divisors upstairs

On the incidence cover define

```text
alpha = e4(w)+u*e2(w)+u^2,
beta  = e3(w)+u*e1(w),
gamma = 2*(alpha+P),
delta = gamma-4P-16J^2,
P     = N1*N2*N3*N4.
```

The relevant ideals are

```text
Iu = IX+(u),
Ig = IX+(gamma),
IZ = IX+(delta).
```

Decompose these ideals upstairs before projecting them. In particular, `primaryDecomposition IZ` tells us whether the rotating difference divisor is irreducible or splits on the incidence cover. Projection should be the final step.

## 4. Encode all signed contact components

For `epsilon in {+1,-1}^4`, use

```text
C_epsilon = IX+(
  u,
  w1-epsilon1*N1,
  w2-epsilon2*N2,
  w3-epsilon3*N3,
  w4-epsilon4*N4
).
```

Its base image should be

```text
4M-epsilon1*N1-epsilon2*N2-epsilon3*N3-epsilon4*N4=0.
```

The reciprocal sub-balance polynomial is

```text
c_epsilon =
  epsilon1*N2*N3*N4+
  epsilon2*N1*N3*N4+
  epsilon3*N1*N2*N4+
  epsilon4*N1*N2*N3.
```

The non-transverse contact stratum is

```text
Sub_epsilon=C_epsilon+(c_epsilon).
```

The script checks that `Sub_epsilon` lies in `IR`, which is the algebraic signature of the order-four colored inertia derived in the theorem.

## 5. Build the realization poset by ideal sums

For closed strata upstairs, intersection is computed by adding ideals:

```text
V(I) intersect V(K) = V(I+K).
```

The first incidence table should contain:

```text
IR,
C_even,
C_odd,
IZ,
C_even+IZ,
C_odd+IZ,
IR+IZ,
Sub_even,
Sub_odd,
IR+C_even+IZ,
IR+C_odd+IZ.
```

For each entry record:

```text
codimension inside X,
degree,
minimal primes,
whether it is empty after saturation,
base-image ideal after elimination.
```

Containment reverses ideal inclusion. If `I subset J`, then `V(J) subset V(I)`.

## 6. Saturate only by the boundary being excluded

On the generic open, saturate by

```text
2*M*P*product_{a<b}(N_a^2-N_b^2).
```

Do not use that saturation while studying `M=0`, `P=0`, or a charge-collision divisor. Use a separate saturation appropriate to each boundary calculation. Otherwise Macaulay2 will correctly delete the very stratum you are trying to inspect.

## 7. Work in this order

1. Load `horizon_wreath_inertia_model.m2` and confirm its assertions.
2. Recover the quintic by eliminating only `w1,...,w4`, retaining `u`.
3. Compute `IR` upstairs and verify `ramDet=8e3(w)`.
4. Test the 16 contact images.
5. Decompose `IZ` upstairs.
6. Compute pairwise intersections and codimensions upstairs.
7. Run exact rational slices before full symbolic projection.
8. Eliminate the sheet variables only for strata that survive the preceding tests.
9. Use the full symbolic base after the slice computations expose the expected components.

## 8. Recommended first slice

Use

```text
N1=4,
N2=8,
N3=12,
N4=20,
```

leaving `M` and `J` symbolic. This is the exact R9 wall-witness charge vector and avoids the zero-charge and equal-charge boundaries. It is suitable for checking:

- the mass branch image;
- the factorization of the rotating difference image;
- odd/even contact intersections with `delta=0`; and
- the ramification--difference intersection.

After that, use a two-parameter slice retaining one charge variable if a component disappears under the fixed-charge slice.

## 9. Do not build the five-sheet splitting field directly

Macaulay2 should resolve the geometry on one normalized incidence sheet. The audit-verified `S_5` theorem supplies the orbit of that geometry across the five sheets, while the Kummer valuation theorem supplies the inertia labels.

Trying to adjoin all five quintic roots and all fifteen square roots in one ring would reproduce a group already proved and make the realization-poset calculation needlessly difficult.

## 10. Outputs needed for the next audit

Save the following verbatim:

```text
gens massFiberIdeal,
gens massBranchBase on the first slice,
minimalPrimes IZ,
primaryDecomposition IZ if it terminates,
codimension and degree of every named intersection,
minimal primes of IR+IZ,
minimal primes of Sub_even and Sub_odd,
the projected ideals of all nonempty codimension-two strata.
```

Those outputs are enough to build the realized branch-incidence poset and attach the already-classified local group to each node.
