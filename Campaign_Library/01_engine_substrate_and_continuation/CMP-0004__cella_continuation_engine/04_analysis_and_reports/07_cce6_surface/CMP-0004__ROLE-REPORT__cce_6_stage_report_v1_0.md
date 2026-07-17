# CCE-6 native swept-surface clearance stage report v1.0

**Date:** 2026-07-14  
**Verdict:** MATHEMATICAL CLOSEOFF COMPLETE; PRODUCTION IMPORT READY  
**Released scope:** the two exact DBP corridors on
\(\mathscr S_{\mathbb Z}^{\rm nat}=\operatorname{im}L_{\mathbb Z}\)  
**Canonical certificate digest:**
`2d5a395d5cebcb18f2792850741c46848c02efbb0fa05265cf8ec35e86505a4f`

## 0. Outcome

The central CCE-6 theorem gap is closed.  The full Stage-2 sweep does not
have a fourth, independent surface obstruction.  After compactifying the
angular base and fibre, every collision equation factors through the three
marked curve divisors already carried by refined Gauss--Manin transport:

```text
T=0       <-> x=x_p
T-cV=0    <-> x=1
T-c^2 V=0 <-> x=infinity
```

The only new fibre-pair calculation is exact:

```text
Disc_Xi(N)  = -4(1-c) T (T-c^2 V)
Res(N,R)    = c^2 (T-cV)^2
```

where

```text
N = (T-c^2 V) Xi^2 + (1-c) T H^2
R = Xi^2 + H^2.
```

Thus a curve representative transported in the complement of
`x_p, 1, infinity` automatically admits a collision-free angular and fibre
sweep.  The CCE-2 tube bounds keep `c`, `1-c`, `1+c`, and `ab` uniformly
nonzero on both corridors.  Both angular gluing faces and both relative fibre
ends have been checked separately.

This discharges `SurfaceSweepClearanceUnproved` for the released native-image
scope.  It does not discharge the same refusal for an arbitrary route lacking
refined curve-admissibility evidence.

## 1. Why the earlier blocker looked larger than it is

The Stage-2 formulas were written in the affine `v` chart.  There,
`v=infinity`, `v=1/c`, and `v=1/c^2` look like three surface-specific
singular events.  The exact homogeneous calculation shows that they are
merely the pullbacks of the pole, branch point, and infinity already marked on
the boundary curve.

The prior instruction to establish an independent pointwise metric tube over
the whole product domain was sufficient but stronger than the homological
continuation theorem needs.  The correct exact admission proof has two
layers:

1. refined curve transport in the complement of the three disjoint marked
   sections; and
2. exact discriminant/resultant noncollision of the fibre configuration over
   that transported track.

The first is a finite-disk-chain isotopy of the existing CCE-3 class.  The
CCE-2 certificate already supplies exact separations for `m`, `1-m`, `x_p`,
`x_p-1`, `x_p-m`, and the two pole sheets.  These permit disjoint rational
closed section neighbourhoods; their complement in the compactified family
is proper with boundary and carries the required exact isotopy.  The second
layer is the polynomial calculation certified here.  No floating sweep,
sampled minimum, or generic-path assertion enters the proof.

## 2. Exact coordinate reduction

On the shear cover, set

```text
A = rho+1
B = rho-1
c = B/A
Delta1 = A T-B V
Delta2 = A^2 T-B^2 V.
```

The sweep equations clear to

```text
Delta1 C^2 = 2 V
Delta1 S^2 = A(T-V)
N_hat = Delta2 Xi^2 + 2 A T H^2
polar = T(Xi^2+H^2).
```

The verifier proves in
`Q(i)[rho,sigma,V,T,Xi,H]/(rho^2-1-sigma^2)` that

```text
2 A T-Delta2 = -B Delta1
Res(N_hat, Xi^2+H^2) = B^2 Delta1^2.
```

The Stage-1 coordinate is

```text
x   = 2 B V/Delta2
m   = B/(2 rho)
x_p = -2/B,
```

with the three supporting polynomial identities

```text
2 B V-Delta2       = -A Delta1
4 rho V-Delta2     = A^2(V-T)
B^2 V+Delta2       = A^2 T.
```

These identities prove the marked-divisor table without choosing square-root
branches.

## 3. Exact quantitative transfer

For normalized refined curve-track witnesses

```text
|T|       >= epsilon_infinity > 0
|T-cV|    >= epsilon_1        > 0
|T-c^2 V|>= epsilon_2        > 0,
```

the CCE-2 bounds imply

```text
|Disc(N)| >= (8/5) epsilon_infinity epsilon_2
|Res(N,R)|>= epsilon_1^2/102400
|(1-c)T| >= (2/5) epsilon_infinity
|D2|      >= epsilon_2.
```

The exact chordal separation of the five projective base points supplies the
same concrete witness on both released corridors:

```text
epsilon_infinity = epsilon_1 = epsilon_2 = 1/105186307200.
```

This is one quarter of the certified conservative pairwise separation
`1/26296576800`; it is not a sampled path radius.

On `V=0`, the discriminant and resultant bounds become

```text
(8/5) epsilon_infinity^2
epsilon_infinity^2/102400.
```

On `V=T`, they become

```text
(16/125) epsilon_infinity^2
epsilon_infinity^2/640000.
```

The three epsilon witnesses may be serialized by an explicit exact PL
representative.  At class-transport scope their existence follows from the
finite compact refined Gauss--Manin track; the displayed formulas are the
universal exact transfer that the Cella adapter replays.

## 4. Swept-boundary and endpoint checks

| Face/event | Exact result |
|---|---|
| `V=0` | `C=0`; only the `C` sign pair glues; `Delta2=A^2 T` |
| `V=T` | `S=0`; only the `S` sign pair glues; `Delta2=4 rho T` |
| `C=S=0` | Forces `T=0`, already excluded |
| Fibre infinity `H=0` | `N_hat=Delta2 Xi^2`; endpoints distinct iff `D2!=0` |
| Polar at `H=0` | `R=Xi^2`; no polar/endpoint collision |
| Norm/polar collision | Exactly `c(T-cV)=0`; both factors excluded |

Therefore side-boundary cancellation and relative endpoint placement remain
valid over the complete upper and lower parameter corridors, not only at the
dual endpoint.

## 5. Delivered artifacts

| Artifact | Role | SHA-256 |
|---|---|---|
| `DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_THEOREM_v1.0.md` | Full theorem and proof | `8f59e6641a9d7d588d284c3570695b43ebf7f77abd395beef6af2c1c6e0a3ef7` |
| `DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_CERTIFICATE_v1.0.json` | Source-bound exact manifest | `5326bb2fe928c107264cd45f693fd7e0102551ab8aa60f61e339fa4eeabd6397` |
| `verify_dbp_native_surface_sweep_clearance.py` | Dependency-free exact replay | `d196955cc9d5eec7261c7b7ca1edbbd27bf93a98c53409141ffd3a0fc8e0fd00` |
| `CCE_6_GAP_LEDGER_v1.0.md` | Closed/open scope ledger | `9c02f428d54472be8648eaec97cb3c1006da624e947bb866ecbbcf9407aec0ef` |
| `CCE_6_PAPER_III_INSERTION_NOTE_v1.0.md` | Authorized source insertion | `f8d7908579784a2bdc017d09dd0039aac067f1f9244a41411a7fddbd95e30cdb` |

## 6. Replay evidence

The standalone verifier performs 89 assertions.  It checks:

- all seven source-file hashes;
- both nested route identities, route-manifest digests, and canonical
  clearance-certificate digests;
- the shear-cover quotient identities by exact polynomial reduction;
- angular numerator closure;
- norm/polar resultant factorization;
- all three curve-divisor identities;
- both full boundary-face specializations;
- norm and polar restrictions at fibre infinity;
- all corridor-derived rational coefficients;
- the serialized quantitative ledger and scope refusals.

Successful replay output:

```text
CCE-6 native surface-clearance replay: 89 assertions passed
canonical certificate digest: 2d5a395d5cebcb18f2792850741c46848c02efbb0fa05265cf8ec35e86505a4f
```

## 7. Cella import contract

The live Cella merge should do exactly the following.

1. Place the theorem, certificate, verifier, gap ledger, and insertion note
   under the CCE campaign directory and source-bind them in the CCE-6 bundle.
2. Nest the unchanged upper/lower CCE-2 clearance certificate digests and the
   applicable CCE-3 class certificate digest.
3. Admit only the two declared route IDs unless a new route supplies refined
   curve-admissibility evidence for `x_p, 1, infinity`.
4. Recompute the collision identities and rational transfer coefficients;
   do not trust manifest success booleans.
5. Keep the native carrier typed as `image(L_Z)` and replay the existing
   integral `L_Z/R_Z`, naturality, pairing, boundary, and coefficient-ring
   accounts against this domain certificate.
6. Refuse an outside-image request with `OutsideNativeSurfaceImage`, a
   whole-surface promotion with `WholeSurfaceScopeUnproved`, and an unbound
   route with `SurfaceRouteAdmissibilityMissing`.
7. Preserve CCE-1 through CCE-4 certificate locks and the CCE-2 route digests
   byte-for-byte.

The adapter does not need a second surface Pathfinder route.  It consumes the
existing curve route and class certificates plus this exact clearance
transfer.

## 8. Scope reconciliation

The mathematical CCE-6 blocker is closed.  A live-repository API merge,
checkpoint envelope, and gate registration are implementation integration,
not missing theorem work; they were not falsely claimed in this scratch
workspace because the live Cella source tree was not supplied here.

The following claims remain out of scope:

```text
S_Z^nat = all surface homology
(1/4) R_Z is integral
the lifted meridian is primitive in the whole surface lattice
an arbitrary unverified route has a valid sweep
CCE-3 affine compact corrections have been numerically guessed
```

Within the two certified corridors and native image, CCE-6 is ready to import
and release.
