# Cella Continuation Engine scope-expansion investigation v1.0

## Decision rule

A historical handoff's release ceiling is not treated as a mathematical
prohibition.  Each natural enlargement was checked against the live theorem
sources and repository implementations.  Proved enlargements were
implemented; false enlargements were killed by proof; remaining gaps are
stated as concrete mathematical or engineering obligations.

## Results at a glance

| Stage | Expansion investigated | Result |
|---|---|---|
| CCE-4 | arbitrary certified precision | implemented for every integer `target_bits >= 16` |
| CCE-4 | arbitrary six-opcode program | not yet admitted; generic analytic disk semantics and tail scheduling are missing |
| CCE-5 | composition beyond two isolated corridors | implemented as the exact two-corridor fundamental groupoid |
| CCE-5 | whole regular parameter-plane groupoid | additional local generator calibration is required at `m=0,1/2,1,infinity` |
| CCE-6 | native image equals whole surface lattice | refuted: ranks are at most 4 versus 12 |
| CCE-6 | whole-lattice CPV non-descent | open Smith/saturation calculation, now isolated precisely |
| CCE-7 | arbitrary fixed-charge real route | implemented with adaptive exact Sturm transport |
| CCE-7 | full rational polygonal static chamber | implemented with all five parameters varying |
| CCE-7 | exact contact-wall specialization | implemented, including zero-charge signed-sheet coincidence |
| CCE-7 | generic complex braid continuation | real research gap: normalized incidence ramification/inertia decomposition is incomplete |
| CCE-8 | every finite role-jet order | implemented by exact truncated formal inversion |
| CCE-8 | typed role boundaries | implemented for chart-failure and channel-isotropy divisors |
| CCE-8 | equivalence of full role, horizon, and elliptic carriers | refuted as a structure-preserving full-carrier equivalence |
| Paper V | equivalence after reduction to a common skeleton | still open; the reduction object and maximality theorem are not formalized |
| Paper V | categorical closure | partly realized by current adapters; generic quotient/base-change/fibre-product closure still needs theorem hypotheses |
| Paper V | independent third realization | viable exact AC fold-cover candidate exists; it is a separate realization campaign, not a role-adapter operation |

## CCE-4

The historical precision set `(192,256,384)` was only a recertification
matrix.  The recurrence schedule already scales with the requested width.
The admission wrapper now accepts every exact integer precision at least 16;
both kernels certify and replay at 64 bits, and the complete historical plus
expanded gate passes 73 assertions.

The apparent “finite grammar” is still a sealed two-program grammar.  The
coefficient recurrences for `INPUT_AFFINE`, `ADD`, `SCALE_Q`, `MUL`, `SQRT`,
and `DIV` exist, but the analytic majorant is selected by the two fixed kernel
IDs.  A genuinely arbitrary program requires:

1. compositional complex-disk enclosures for each opcode;
2. branch selection and zero-separation witnesses for every `SQRT` and `DIV`;
3. a program-derived Cauchy majorant;
4. a schedule theorem turning that majorant into an exact tail bound.

This is additional proof-engine work, not a conceptual wall.  Merely relaxing
`_validate_spec` would be unsound because the legacy evaluator would still
execute one of the two fixed kernels.

## CCE-5

The upper and lower calibrated transports are no longer isolated calls.
`U,L` and their inverse arrows `u,l` now form a typed two-object groupoid.
Arbitrary endpoint-composable words have exact compact and relative matrices
in the common basis `(A,B,mu,delta_upper)`.  Inverse, composition, boundary,
and replay laws are certified; the CCE-5 gate passes 61 assertions.

This groupoid is not the whole punctured `m`-plane.  The rational connection
has singular locus

```text
m = 0, 1/2, 1, infinity.
```

The two DBP corridors calibrate one Galois branch transition with two lateral
choices.  Completing the regular-plane fundamental groupoid requires exact
local normal forms and topological matrices for a generator around every
remaining puncture.  In particular the displayed `(K,E,Pi)` basis has a
second-order coefficient at `m=1`, so one cannot read all monodromy matrices
off naive residues without first finding a logarithmic local basis.  That is
the next specific calculation.

## CCE-6

The completed package remains accepted without redoing its clearance proof.
The new investigation concerns the strictly larger target
`H_2(X,Y;Z)`.

The projective norm cover is a smooth `(2,2)` complete intersection in
`P^4`, hence a degree-four del Pezzo surface with `b2=6`.  Both `D_q` and
`D_infinity` are smooth anticanonical elliptic curves and meet transversely in
four points.  The Gysin and pair exact sequences give

```text
H_2(X;Z)       = Z^7
H_1(Y;Z)       = Z^5
H_2(X,Y;Z)     = Z^12.
```

The punctured elliptic relative source has rank four.  Since the completed
CCE-6 theorem proves the lift injective on its admissible source, its image has
rank at most four and cannot be the whole rank-twelve surface lattice.  This
settles surjectivity negatively.

The unresolved question is not “is the lift onto?” but “what are the Smith
factors of its rank-four image?”  An intersection matrix against integral
dual relative cycles, or an integral extension of signed reduction, will
decide whether the lifted meridian is divisible by two in the whole lattice.
The proof is in `CCE_6_WHOLE_SURFACE_TOPOLOGY_OBSTRUCTION_v1.0.md`; its exact
audit passes 19 assertions.

## CCE-7

Three real-static enlargements are complete:

1. any exact rational `4M` route at fixed integral charges, forward or
   backward, with adaptive Sturm subdivision;
2. any exact rational polygonal route varying `4M,N1,N2,N3,N4`, admitted by
   endpoint positivity of the concave strict-chamber margin and by exact
   nonvanishing of every affine `Ni-Nj` and `Ni+Nj` factor;
3. typed boundary points at `4M=sum|Ni|`, including the distinction between a
   simple physical contact and the additional signed-sheet coincidence caused
   by a zero charge.

The shadow labels follow the exact squared-charge ordering, so varying or
reordered charges do not silently corrupt sheet names.  The gate passes 47
assertions.

Generic complex braid continuation is not obtainable by applying the
quintic discriminant blindly.  The live normalization-aware cover provider
records a certified counterexample: the eliminant discriminant contains
projected sheet crossings that are not ramification.  The repository's R12
ledger still requires decomposition of the normalized incidence
ramification ideal and local inertia at the complex sub-balance and
critical-sheet components.  Contact walls used by the real classifier are
generically unramified and therefore do not supply those braid generators.

The exact missing artifact is a factorized relative-ramification/inertia
ledger from the upstairs incidence model, followed by exact meridian paths.
Until then, claiming a generic complex braid adapter would conflate collision
images with branch divisors.

## CCE-8 and Paper V

Paper I states finite-order rational closure, not order-two closure.  The new
adapter stores a normalized bivariate Taylor polynomial and recursively
solves `P=f(D,S)` for `D=g(P,S)` degree by degree.  Every coefficient remains
in `Q[jet,a^-1]`; `s^2=t^2=(st)^3=e` is replayed on the full truncation.  The
order-two projection exactly matches the released formulas and channel
account.  The gate passes 53 assertions, including an active order-four
fixture.

Paper I also treats singular strata as typed data.  Chart failures `a=0` and
`b=0`, and the three channel-numerator isotropy divisors, now have an exact
boundary classifier rather than only an undifferentiated refusal.

### Full-carrier equivalence

A structure-preserving equivalence of the unreduced carriers is false:

```text
role carrier      finite S3 orbit over a positive-dimensional jet/account space
horizon carrier   generically five discrete root sheets with S5 monodromy
elliptic carrier  rank-four integral relative-homology local system
```

These have incompatible generic fibre type, cardinality/dimension, isotropy,
and monodromy.  The repository independently proves in the self-glue setting
that a monodromy `S3` and the role `S3` act on rows and columns as a commuting
`S3 x S3`, not as one diagonal group.  Shared representation names therefore
do not manufacture a geometric identification.

The viable Paper-V theorem is the architecture's narrower target: strict
non-equivalence of full carriers plus equivalence of explicit reductions to a
common quotient-selection skeleton.  The negative half is now supported.
The positive half remains open because the common skeleton, reduction
functors, and maximality/data-minimization property have not been defined
with enough precision to test full faithfulness and essential surjectivity.

### Closure

The current engine already supplies exact identity, inverse, composition,
restriction to admitted chambers, coefficient typing, and typed boundary
events in concrete adapters.  This is evidence for closure under those named
operations, not yet the general Paper-V category theorem.  The remaining
proof-bearing definitions are:

1. normal symmetry subgroupoid and saturated sub-local-system quotients;
2. admissible base change with selected-section preservation;
3. compatibility/transversality conditions for fibre products;
4. functorial specialization of inertia, wall, and valuation labels.

### Independent third realization

The architecture's AC power-flow fold cover is a legitimate separate target:

\[
v^2+(2QX-E^2)v+X^2(P^2+Q^2)=0,
\qquad
\Delta=E^4-4E^2QX-4P^2X^2.
\]

It has a `C2` sheet exchange, exact chamber `Delta>0`, high-voltage selection
from the no-load root `v=E^2`, and square-root fold wall.  No mathematical
obstruction was found.  It is not an expansion of the role rechart operation,
however; it needs its own family, path, wall, and certificate adapter before
it can serve as Paper V's independent realization.

## Verification ledger

```text
CCE-4 gate                         73 assertions passed
CCE-5 gate                         61 assertions passed
CCE-6 whole-surface audit          19 assertions passed
CCE-7 gate                         47 assertions passed
CCE-8 gate                         53 assertions passed
CCE-5--8 expanded release replay   32 assertions passed
```
