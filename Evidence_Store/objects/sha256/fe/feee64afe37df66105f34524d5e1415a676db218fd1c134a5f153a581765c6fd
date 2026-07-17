# Codex handoff — CCE-3 typed relative-class and CPV engine v1.0

**Campaign:** CCE-3 — Exact Relative Classes and CPV  
**Date:** 2026-07-14  
**Status:** executable proof-and-build handoff  
**Repository:** Cella  
**Prerequisite:** CCE-0, PF-0, CCE-1, and CCE-2 complete  
**Primary result:** first reusable symbolic continuation release for the two certified DBP corridors

---

## 0. Assignment

Implement and certify the exact coefficient-typed relative-class layer directly
above the completed CCE-2 corridor certificates.

The stage must turn the two route-fixed CCE-2 results into executable objects in

```text
H_Z(u) = H_1(C_u^o,{Q_0,Q_m};Z)
```

while explicitly retaining:

```text
ordinary compact cycles A and B
the selected-pole meridian mu
the endpoint-relative class delta
the boundary beta = [Q_m]-[Q_0]
the compact null submodule Lambda_ell = Z*A + Z*B
the coefficient ring and quotient scope
the upper/lower lateral distinction
the unresolved compact corrections
```

Construct CPV only as the exact half-sum of two independently certified
lateral classes after scalar extension. Enforce the coefficient-ring diamond

```text
             Z[1/2,i]
             /       \
         Z[1/2]      Z[i]
             \       /
                  Z
```

and certify the boundary obstruction proving that multiplication by `i` cannot
be replaced by an integral Picard--Lefschetz class after adding closed cycles.

This Markdown file is the complete campaign design. Do not create a second
planning document, clarification handoff, or companion prompt. Stage reports,
schemas, certificates, and the gap ledger are campaign outputs, not additional
instruction sources.

Terminate with exactly one of:

```text
COMPLETE
  The module, quotient, ring extensions, two lateral classes, CPV class,
  coefficient obstructions, certificates, verifier, API, and all gates are
  implemented and deterministically replayed.

BLOCKED
  A precise mathematical, authority, or implementation obligation is missing.
  Identify the exact failed invariant or absent theorem. Do not fill the gap
  with an inferred basis, rounded matrix, or zero compact correction.
```

Do not stop for a progress ceremony. Continue through all stages unless a real
blocker under this definition is reached.

---

## 1. Why CCE-3 is next

CCE-2 proved the geometry needed to identify the two routes:

```text
exact Q(i) polygonal representatives
positive radius-1/8 curve tubes
unique lifted continuation to rho=-sqrt(2)
upper/lower pole-side calibration
route-fixed quotient transport
deterministic source-bound certificates
```

What remains is the algebraic state those routes transport. Without CCE-3 the
engine cannot safely distinguish an integral lateral class, a compact-period
quotient, a rational CPV midpoint, a Gaussian-normalized class, and an absolute
representative with unknown compact correction.

CCE-3 closes that typing gap. It does not compute periods or solve the unknown
compact Picard--Lefschetz coordinates. Completion establishes the first reusable
symbolic CCE release and the substrate for later observable evaluation,
integral monodromy, realization equivalence, operation closure, surface
continuation, and a third realization. It does not itself prove those results.

---

## 2. Frozen starting state

Treat these results as immutable inputs unless an exact verifier finds a
contradiction.

### 2.1 Completed gates

```text
CCE-0                         complete
PF-0                          complete against live typed Pathfinder
CCE-1                         complete
CCE-2                         PROVED at curve-level exact-corridor scope
engine test programs          37/37 passed
DBP evaluator assertions      1,591 passed
PF-0 assertions               58 passed
CCE-1 assertions              24 passed
CCE-2 assertions              31 passed
standalone corridor checks    47 passed
```

### 2.2 Frozen digests

```text
legacy schema-1.1 bundle
aa97101da7ae03f127adf4dc7940128fbdc8ee425a21c2ef88b828c76afd2989

CCE-1 six-envelope bundle
c04ba9200de47bd5fc68e84e9c932ab63e5ea9eb41981b6bba3144272b7f84a3

PF-0 behavior confirmation
304fccce5ed1206f23969952634d10b250d8d4d7a7a955971afa8018c2372008

live 52-file Pathfinder closure
c5f0ac50100aa7e4f59389a978ef5fb661a714c442219c3266a1a4924e10b504

live DBP Pathfinder provider
04d94f508b01860f3c2a034f29f098e92a31e01e4fe1e5226046a34cfe74bd10

CCE-2 theorem
bfb0dc4c4678803cc46e791cbe60e87736ea41ce14db157e8fb1726e28b671fe

CCE-2 divisor reduction
cf893db1c6c2718a614dfdf519e220cbb3b7312aff62130c608ddd7598c1c93a

CCE-2 lateral calibration
f94cb784d7218e3fa2f03c024a4921457b1d517ddfa022c81a90865c4dec5143

upper/lower route manifests
63e19e63181d9573590d2ff4825787c95f4ecc1b99da8d510df370b7ccfaa62d
6216ca406c364cf382baabb7f6ea112ed095ce2393ac9d63f06636d5157565b5

upper/lower route certificates
d11b4f13afd11d142b6b319884bcf0d355f07fc20deecc6543646c760d57ffb8
60a13358149c2c672919d4380fa31178874d5ecb9899d1ac364773c56ee958c8

CCE-2 two-certificate bundle
637b0888db282e66f54f030bd28885cd3b0270ce7e211d2e6311baf0c3f0d629
```

Recompute these from repository bytes. A mismatch is a source-identity event,
not permission to silently update an expected value.

### 2.3 Admitted routes

Only these theorem-bound routes are admitted:

```text
ell_up
  word: a_+
  counterclockwise about +i
  windings about (0,+i,-i): (0,1,0)

ell_down
  word: a_-^(-1)
  clockwise about -i
  windings about (0,+i,-i): (0,0,-1)
```

Both run from `u_+=(1,+sqrt(2))` to `u_-=(1,-sqrt(2))`.

Consume the actual nested CCE-2 route certificates. A route label, winding
tuple, endpoint sheet, or success flag without its certificate is insufficient.
General route composition, reversal, and arbitrary homotopy classes remain out
of scope.

---

## 3. Authority and precedence

Read and bind before changing production code:

```text
research/campaigns/CELLA_CONTINUATION_ENGINE/
  CCE_CONTINUATION_ENGINE_FINAL_REPORT_v0.2.md
  CCE_CONTINUATION_ENGINE_FINAL_REPORT_v0.2.json
  PATHFINDER_BEHAVIOR_CONFIRMATION_REPORT_v1.0.md
  PATHFINDER_BEHAVIOR_CONFIRMATION_REPORT_v1.0.json
  CCE_1_STAGE_REPORT_v1.0.md
  CCE_2_STAGE_REPORT_v1.0.md
  CCE_2_STAGE_REPORT_v1.0.json
  CCE_2_GAP_LEDGER_v1.0.md
  DBP_EXACT_CORRIDOR_MANIFEST_v1.0.json
  DBP_EXACT_CORRIDOR_ROUTE_DIGESTS_v1.0.json
  DBP_EXACT_CORRIDOR_CLEARANCE_CERTIFICATES_v1.0.json

DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md
  Sections 7D and 7F; Theorem 7F.1

DBP_DUAL_SURFACE_CYCLE_STAGE3_v0.1.md
  Section 3

SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md

CODEX_HANDOFF_CELLA_CONTINUATION_ENGINE_v0.2.md
  Sections 5.2, 5.5--5.7, 7, 9, 10/CCE-3, and 12
```

Resolve exact repository paths and record SHA-256 digests. Precedence is:

```text
1. exact theorem statement and proved correction notices
2. replayed machine certificates and canonical manifests
3. CCE-2 stage report and gap ledger
4. selected quotient groupoid foundation
5. original continuation-engine handoff
6. implementation comments and historical notes
```

If higher-authority sources disagree on orientation, basis, boundary, ring, or
quotient, stop with `BLOCKED_SOURCE_CONFLICT` and report both statements.

The historical file

```text
research/campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR/pathfinder_m1_scout.py
```

must have zero production references and must not be imported, executed, or
used as evidence.

---

## 4. Exact mathematical contract

### 4.1 Relative lattice

On

```text
U_tilde^o = {(sigma,rho): rho^2=1+sigma^2, sigma!=0, rho!=0}
```

use

```text
c = (rho-1)/(rho+1)
m = (rho-1)/(2*rho)
n = -m^2/(1-2*m)

C_u       : y^2=x(x-1)(x-m(u))
C_u^o     : C_u minus {P_u^+,P_u^-}
Q_0       : (0,0)
Q_m       : (m,0)
H_Z(u)    : H_1(C_u^o,{Q_0,Q_m};Z).
```

The exact sequence contains

```text
0 -> H_1(C_u^o;Z) -> H_Z(u) -> Z*beta -> 0
beta = [Q_m]-[Q_0].
```

Bind an oriented marked basis equivalent to `(A,B,mu,delta)` with

```text
A,B     ordinary compact elliptic generators
mu      positive primitive selected-pole meridian
delta   endpoint-relative generator

partial(A)=partial(B)=partial(mu)=0
partial(delta)=beta.
```

The basis manifest must state the endpoint, selected pole, orientations,
`A.B=+1`, and theorem evidence for primitivity. Do not infer a basis from four
labels in prose.

### 4.2 Endpoint coordinates

At `u_-`, choose `(A_-,B_-,mu_-,delta_-^up)`. Then

```text
delta_-^up    = (0,0,0,1)
delta_-^down  = (0,0,1,1)
```

because

```text
delta_-^up - delta_-^down = -mu_-.
```

Both have boundary `beta`.

### 4.3 Compact quotient

The null submodule is exactly

```text
Lambda_ell = Z*A + Z*B.
```

It does not include `mu`. For every admitted coefficient ring `R`, define

```text
q(a,b,c,d) = (c,d)
```

in quotient basis `(mu,delta)`. Thus

```text
q(delta_-^up)    = (0,1)
q(delta_-^down)  = (1,1).
```

Do not replace this with the quotient modulo every closed cycle; that would
erase the meridian and the lateral distinction.

### 4.4 Transport and compact uncertainty

The admitted statements are

```text
G_up(delta_+)   = delta_-^up   + lambda_up
G_down(delta_+) = delta_-^down + lambda_down

lambda_up,lambda_down in Lambda_ell(u_-).
```

Equivalently,

```text
q(G_up(delta_+))   = (0,1)
q(G_down(delta_+)) = (1,1).
```

`lambda_up` and `lambda_down` are independent unresolved compact-lattice
elements. Never set them to zero, equate them, round them from periods, assign
placeholder coordinates, or delete them during serialization.

Do not claim a full integral transport matrix. The complete `A/B` monodromy and
compact-correction coordinates are not known.

### 4.5 CPV and the crucial affine distinction

The selected endpoint CPV class is

```text
delta_-^CPV
  = (delta_-^up+delta_-^down)/2
  = delta_-^up+mu_-/2
  = (0,0,1/2,1).
```

Therefore

```text
q(delta_-^CPV) = (1/2,1)
2*delta_-^CPV  = delta_-^up+delta_-^down.
```

Because `mu_-` is primitive, CPV is in `H_Z tensor Z[1/2]` but not in `H_Z`.

The half-sum of the actual transported affine classes is instead

```text
(G_up(delta_+)+G_down(delta_+))/2
  = delta_-^CPV+(lambda_up+lambda_down)/2.
```

It retains compact ambiguity in `Lambda_ell tensor Z[1/2]`. Do not identify it
with the selected endpoint representative unless the corrections are later
fixed. Their compact quotient classes agree; that is the current claim.

### 4.6 Coefficient rings

Implement exactly:

```text
Z
Z[1/2]
Z[i]
Z[1/2,i].
```

Legal inclusions are

```text
Z -> Z[1/2] -> Z[1/2,i]
Z -> Z[i]   -> Z[1/2,i].
```

Minimal displayed rings:

| Class | Minimal ring |
|---|---|
| `delta_up`, `delta_down` | `Z` |
| `delta_CPV` | `Z[1/2]`, not `Z` |
| `i*delta_up`, `i*delta_down` | `Z[i]`, not `Z` |
| `i*delta_CPV` | `Z[1/2,i]` |

Scalar extension is explicit. Demotion requires exact membership proof.

### 4.7 No integral replacement for `i`

For `x=aA+bB+c*mu+d*delta`,

```text
partial(x)=d*beta.
```

Hence every phased lateral or CPV class has boundary `i*beta`. Integral
relative classes have boundary in `Z*beta`, and closed cycles have boundary
zero. No integral class can equal an `i`-normalized lateral or CPV class modulo
closed cycles. The verifier must replay this contradiction; a boolean flag is
not evidence.

### 4.8 Intersection scope

Mandatory data are only

```text
A.B=+1, B.A=-1, A.A=B.B=0.
```

Do not invent a full `4 x 4` intersection matrix involving `mu` and `delta`.
Represent additional entries as absent or theorem-scoped partial data. A full
unimodular transport claim is forbidden until its matrix is derived.

---

## 5. Exact data model

Use immutable records and canonical serialization. Names may follow repository
conventions; the semantics are mandatory.

### 5.1 Canonical rings and scalars

```text
CoefficientRingId = Z | Z_INV_2 | Z_I | Z_INV_2_I

DyadicGaussian
  real_numerator
  imag_numerator
  denominator_exponent

value=(real_numerator+i*imag_numerator)/2^denominator_exponent.
```

Canonicalization:

```text
exponent >= 0
zero = (0,0,0)
if exponent>0, numerators are not both even
Z: exponent=0, imag=0
Z[1/2]: imag=0
Z[i]: exponent=0
```

All arithmetic and membership checks use exact integers.

### 5.2 Basis and class records

```text
RelativeBasisManifest
  family_id, endpoint_id, selected_pole_id, basis_id
  ordered_generators=[A,B,mu,delta]
  generator_orientations
  boundary_vector=[0,0,0,1]
  compact_submodule_basis=[A,B]
  quotient_basis=[mu,delta]
  compact_intersection=[[0,1],[-1,0]]
  primitive_meridian_witness
  theorem_ids_and_digests
  canonical_digest

RelativeClassVector
  basis_digest, ring_id
  coordinates=[A,B,mu,delta]
  derived_boundary_coefficient
  canonical_digest

CompactQuotientClass
  basis_digest, ring_id, null_submodule_digest
  quotient_coordinates=[mu,delta]
  derived_boundary_coefficient
  representative_digest, optional
  canonical_digest
```

The verifier recomputes boundaries and quotient coordinates.

### 5.3 Affine compact uncertainty

```text
UnknownCompactCorrection
  symbol_id
  route_certificate_digest
  submodule_digest
  coefficient_ring
  status=unresolved

AffineRelativeClass
  known_representative, optional
  known_quotient_class
  uncertainty_terms
  ambient_basis_digest
  coefficient_ring
  boundary_coefficient
  claim_scope
  canonical_digest
```

Claim scopes:

```text
EXACT_ABSOLUTE_CLASS
EXACT_COMPACT_QUOTIENT_CLASS
AFFINE_OVER_COMPACT_SUBMODULE
SCALAR_EXTENDED_AFFINE_CLASS
```

Algebra may combine, scale, or cancel the same uncertainty symbol. It may not
cancel distinct symbols or assume either is zero. An affine object cannot be
coerced to an exact absolute vector.

### 5.4 Lateral pair and CPV

```text
CertifiedLateralPair
  upper/lower route certificate digests
  upper/lower selected classes
  upper/lower transport affine classes
  meridian relation witness
  common boundary witness
  quotient witnesses
  canonical_digest

CPVClassRecord
  lateral_pair_digest
  scalar_extension_witness
  selected_endpoint_half_sum
  quotient_half_sum
  transported_affine_half_sum
  compact_ambiguity_terms
  nonintegrality_witness
  minimal_ring
  canonical_digest
```

The three CPV class fields are deliberately distinct.

---

## 6. Exact operations and public API

Follow existing naming conventions, but support these semantics:

```text
construct_basis_manifest(endpoint,theorem_sources)
construct_selected_lateral(route_certificate)
construct_lateral_pair(upper_certificate,lower_certificate)

add_classes(x,y)
subtract_classes(x,y)
scale_class(s,x)
extend_scalars(x,target_ring)
restrict_scalars_if_member(x,target_ring)
take_compact_quotient(x)
compute_boundary(x)

form_cpv(lateral_pair,requested_ring)
multiply_by_i(class,requested_ring)
continue_relative_class_certified(request)
```

Every constructor verifies its inputs. Every algebraic operation preserves the
basis digest, null-submodule identity, boundary, coefficient ring, claim scope,
and unresolved uncertainty terms.

Required CPV behavior:

```text
CPV over Z              -> refuse RingTooSmall
CPV over Z[1/2]         -> accept
CPV over Z[i]           -> refuse RingTooSmall
CPV over Z[1/2,i]       -> accept
```

Required phase behavior:

```text
i*lateral over Z             -> refuse RingTooSmall
i*lateral over Z[i]          -> accept
i*CPV over Z[1/2]            -> refuse RingTooSmall
i*CPV over Z[1/2,i]          -> accept
integral replacement for i   -> refuse BoundaryObstruction
```

The first release supports only the certified `ell_up` and `ell_down` routes,
the selected `delta_+` input, and the endpoint lateral/CPV constructions in
this handoff.

An absolute scalar requires an exact representative and an evaluation stage.
Therefore:

```text
absolute scalar from quotient-only class -> AbsoluteRepresentativeUnknown
absolute scalar from affine compact coset -> AbsoluteRepresentativeUnknown
numeric CPV request                       -> EvaluationStageRequired
full transport matrix request             -> FullTransportMatrixUnavailable
```

Do not invoke the legacy evaluator to disguise missing representative data.
CCE-4 will attach bounded observables under its own contract.

---

## 7. Pathfinder policy

Use the live typed Pathfinder under

```text
engine/src/cella/pathfinder/
```

and the live DBP provider. Never use the historical scout.

CCE-3 performs exact algebra over certified routes. Pathfinder may construct a
canonical operation plan for route-certificate validation, basis binding,
quotient transport, lateral-pair construction, ring extension, CPV formation,
and the boundary obstruction. The plan must arise from the exact request and
nested certificate identities. It must contain no floating radius, sampled
period, nearest-root choice, or new route proposal.

Within PF-0's admitted scope, the live constructor may be trusted to return a
structurally valid canonical plan. The CCE verifier still replays the plan,
algebra, provenance, and accounts for evidence and tamper detection.

Bind:

```text
PF-0 confirmation digest
live Pathfinder closure digest
live DBP provider digest
exact request digest
canonical plan bytes and digest
nested CCE-2 route certificate digests
```

If an existing CCE operation plan already composes these exact steps, bind and
reuse it. Do not manufacture a redundant Pathfinder layer merely to obtain a
digest.

---

## 8. Certificate and replay contract

Create a canonical certificate nested above CCE-2:

```text
CCE3RelativeClassCertificate
  schema
    schema_id, schema_version, canonicalization_version

  source_ledger
    repository_identity
    theorem_ids_and_digests
    basis_source_digests
    selected_quotient_groupoid_digest
    PF-0_digest
    Pathfinder_closure_digest
    DBP_provider_digest

  request_ledger
    exact_request_digest
    operation, selected_routes, input_class
    requested_ring, requested_claim_scope

  route_ledger
    nested upper/lower CCE-2 certificates as required
    route manifests, endpoint checks, lateral-side checks

  basis_ledger
    basis manifest, boundary map, compact submodule
    quotient map, primitive-meridian witness
    partial intersection form

  class_ledger
    selected representatives and quotient coordinates
    affine transported classes and compact uncertainties
    meridian and boundary identities

  coefficient_ledger
    source and target rings
    canonical scalars and extension steps
    minimal-ring or failed-membership witness

  cpv_ledger, when requested
    lateral class digests
    exact half-sum identity
    endpoint, quotient, and affine results
    half-compact ambiguity
    nonintegrality witness

  obstruction_ledger, when requested
    input boundary, phased boundary
    integral boundary lattice, exact contradiction

  checkpoint_chain
    previous_digest, certified_prefix, remaining_operations_digest

  replay
    verifier_version, canonical_certificate_digest
```

The verifier recomputes:

```text
dyadic-Gaussian normalization
ring membership and minimal ring
basis and route bindings
boundary and compact quotient maps
upper/lower endpoint coordinates
delta_up-delta_down=-mu
2*delta_CPV=delta_up+delta_down
transported half-sum compact ambiguity
boundary obstruction for i
all certificate and checkpoint digests
```

It must not trust summary booleans such as `is_integral`, `boundary_ok`,
`quotient_ok`, or `minimal_ring_ok`. Certificates and bundle digests must be
byte-identical in two clean processes.

---

## 9. Stable refusal vocabulary

Reuse existing types where semantics match. Add as needed:

```text
UnsupportedRoute
RouteCertificateRequired
RouteCertificateMismatch
UnsupportedInputClass
BasisManifestMismatch
BoundaryMismatch
IntersectionConventionMismatch
NullSubmoduleMismatch
QuotientScopeMismatch
PrimitiveMeridianUnproved
MeridianRelationMismatch
RingTooSmall
IllegalImplicitScalarExtension
ScalarRestrictionFailed
BoundaryObstruction
UnknownCompactCorrection
AbsoluteRepresentativeUnknown
FullTransportMatrixUnavailable
EvaluationStageRequired
UnsupportedOperation
SourceDigestMismatch
CheckpointMismatch
CertificateTampered
```

Distinguish `RingTooSmall` from `BoundaryObstruction`: the former requests a
valid class over an insufficient ring; the latter requests an integral
closed-cycle realization that cannot exist.

---

## 10. Implementation stages

### C3-0 — Preflight and locks

```text
record HEAD and dirty-worktree state
preserve unrelated changes
replay all CCE-0 through CCE-2 gates
recompute all Section 2 digests
resolve and digest theorem sources
confirm zero production references to the stale scout
verify the Paper III corridor-insertion status
```

If the CCE-2 insertion has not been applied, apply Appendix A only after the
CCE-2 exact verifier passes.

Acceptance: all locks match, both route certificates replay, no source conflict,
and unrelated worktree changes remain untouched.

### C3-1 — Basis, boundary, and quotient

```text
derive and bind the endpoint basis manifest
bind the positively oriented primitive meridian
encode the boundary map
encode Lambda_ell=Z*A+Z*B
encode quotient basis [mu,delta]
encode only the proved compact intersection convention
create an exact manifest verifier
```

Acceptance: rank/order are explicit; boundary values replay; the modeled kernel
of `q` is exactly the `A/B` span; `mu` survives; `A.B=+1` and primitivity are
source-bound.

### C3-2 — Exact ring engine

```text
implement canonical dyadic Gaussian scalars
implement four ring identifiers
implement exact arithmetic, membership, promotion, and restriction
implement minimal-ring detection
implement canonical serialization and hostile parsing
```

Acceptance: integer-exact arithmetic, unique canonical forms, correct ring
diamond, exact demotion, and rejection of malformed/noncanonical encodings.

### C3-3 — Exact, quotient, and affine classes

```text
implement RelativeClassVector and CompactQuotientClass
implement UnknownCompactCorrection and AffineRelativeClass
preserve boundary, ring, basis, scope, and uncertainty through algebra
```

Acceptance: quotient data are derived; `lambda_up/down` stay distinct and
unresolved through serialization/checkpointing; affine classes cannot be
coerced to absolute vectors.

### C3-4 — Import the two CCE-2 transports

```text
replay both nested route certificates
derive endpoint lateral side from certified geometry
construct selected endpoint classes
construct affine transported classes
verify compact quotient coordinates
```

Acceptance:

```text
upper endpoint class = (0,0,0,1), quotient=(0,1), uncertainty=lambda_up
lower endpoint class = (0,0,1,1), quotient=(1,1), uncertainty=lambda_down
both boundaries=beta
wrong route, side, basis, endpoint, or digest refuses
```

### C3-5 — Meridian, CPV, and phase separation

```text
verify delta_up-delta_down=-mu
construct the certified lateral pair
extend to Z[1/2] and form endpoint/quotient CPV
form transported affine half-sum with uncertainty retained
implement multiplication by i
implement the integral boundary-obstruction verifier
```

Acceptance:

```text
2*delta_CPV=delta_up+delta_down
delta_CPV=(0,0,1/2,1)
CPV refuses over Z and accepts over Z[1/2]
i-lateral refuses over Z and accepts over Z[i]
i-CPV accepts over Z[1/2,i]
affine half-sum retains (lambda_up+lambda_down)/2
integral replacement for i refuses by replayed boundary contradiction
```

### C3-6 — Certificates and checkpoints

Define the canonical schema, nest CCE-2 certificates, bind live Pathfinder
identity where used, implement deterministic replay and certified-prefix
resume, and add field-level tamper tests.

Acceptance: identical clean-process bytes/digests; all algebra is replayed;
route, ring, basis, boundary, uncertainty, scope, and checkpoint tampering fail.

### C3-7 — API and compatibility

Expose the narrow typed operations, integrate with the existing envelope,
preserve legacy and route-only behavior, and add stable refusal serialization.

Acceptance: no changed legacy result; CCE-2 route outputs remain unchanged;
CCE-3 returns class certificates rather than numeric values; unsupported scalar,
matrix, surface, and evaluation requests refuse.

### C3-8 — Closeout

Run all engine gates, focused verifiers, hostile tests, and two clean-process
determinism checks. Produce Section 13 artifacts and record commands, counts,
digests, timings, changed files, scope, and remaining gaps.

Do not update theorem claims merely because software represents them. Apart from
Appendix A's already-proved CCE-2 insertion, edit a theorem only for a genuinely
new independently verified mathematical result.

---

## 11. Mandatory tests

### 11.1 Rings

```text
canonical zero/unit and dyadic reduction
exact arithmetic and equality
membership in all four rings
all legal promotions and illegal implicit promotions
successful/failed exact restrictions
minimal rings for lateral, CPV, i-lateral, i-CPV
malformed and noncanonical encoding rejection
```

### 11.2 Basis, boundary, quotient

```text
ordered basis digest and wrong-order rejection
wrong selected pole/endpoint rejection
all four generator boundaries and boundary linearity
compact intersection convention
unclaimed full-intersection entries remain absent
primitive-meridian witness and tamper rejection
q(A)=q(B)=0, q(mu)=(1,0), q(delta)=(0,1)
modeled kernel equals A/B span; mu is not killed
wrong null submodule and quotient tampering rejection
```

### 11.3 Lateral classes and uncertainty

```text
both route certificate replays
exact upper/lower coordinates and common boundary
delta_up-delta_down=-mu
opposite sign and route-side swaps reject
lambda_up and lambda_down present, distinct, and nonzero-unassumed
uncertainties survive serialization, scaling, checkpoint, and resume
same-symbol cancellation only; different symbols never cancel
absolute-vector coercion rejects
```

### 11.4 CPV and phase

```text
both lateral certificates required
exact half-sum identity and coordinates
CPV boundary=beta
CPV rejects over Z and accepts over Z[1/2]
primitive half-meridian nonintegrality witness
affine half-sum retains half compact ambiguity
endpoint/transported CPV conflation rejects
phased classes use the exact minimal rings
boundary(i*class)=i*beta
integral replacement rejects by BoundaryObstruction
```

### 11.5 Certificate and regression

```text
two-clean-process byte determinism
source, PF-0, Pathfinder, nested-route, basis, ring, coordinate tampering
uncertainty-deletion and claim-scope-escalation tampering
checkpoint-chain tampering
all existing engine tests and assertion suites
all three frozen legacy/CCE-1/CCE-2 bundle locks unchanged
zero production references to pathfinder_m1_scout.py
```

---

## 12. Hostile/refusal fixtures

At minimum:

```text
route label without nested certificate
upper/lower manifest-side swaps
endpoint sheet mismatch or unknown path
general route composition request
full A/B monodromy request
any assertion lambda_up=0, lambda_down=0, or lambda_up=lambda_down
quotient that kills mu
CPV over Z or Z[i]
i-lateral over Z; i-CPV over Z[1/2]
integral replacement for a phased class
absolute scalar from quotient or affine class
numeric evaluation or surface lift in CCE-3
whole-surface conclusion
unproved full intersection matrix
malformed scalar or wrong basis/null-submodule digest
deleted compact uncertainty
stale Pathfinder pointer
```

Every refusal is stable, machine-readable, and deterministic.

---

## 13. Required deliverables

### Production and verification

```text
exact ring, relative-class, quotient, and uncertainty implementations
lateral-pair and CPV implementation
CCE-3 API integration
canonical schema/serializer and standalone verifier
focused CCE-3 gate and hostile fixtures
```

Use cohesive modules under `engine/src/cella/continuation/` and the live
Pathfinder tree. Audit existing architecture before choosing filenames; do not
duplicate canonicalization or envelope logic.

### Machine-readable artifacts

```text
DBP_RELATIVE_CLASS_BASIS_MANIFEST_v1.0.json
DBP_COEFFICIENT_RING_DIAMOND_v1.0.json
DBP_LATERAL_CLASS_RELATIONS_v1.0.json
CCE_3_RELATIVE_CLASS_CERTIFICATE_SCHEMA_v1.0.json
CCE_3_CERTIFICATE_BUNDLE_v1.0.json
CCE_3_TEST_REFUSAL_MATRIX_v1.0.json
```

### Closeout artifacts

```text
CCE_3_STAGE_REPORT_v1.0.md
CCE_3_STAGE_REPORT_v1.0.json
CCE_3_GAP_LEDGER_v1.0.md
```

The Markdown report must stand alone and state verdict, repository/worktree
identity, changed files, commands, counts, all digests, supported scope, rings,
refusals, retained corrections, Pathfinder/PF-0 scope, paper edits, timings,
dependency closure, and open obligations.

Timing is diagnostic, never theorem evidence.

---

## 14. Explicit non-goals

Do not claim or implement as completed research:

```text
lambda_up/down coordinates
integers (a,b,c) comparing primary and dual classes
complete A/B transport matrices
absolute primary/dual scalar equivalence
arbitrary-precision period continuation
general route composition/reversal or wall crossing
surface-sweep clearance or native surface certificates
whole-surface homology statements
ensemble equivalence or closure under extra operations
an independent third realization
```

Preserve the data later campaigns require without pretending to solve them.

---

## 15. Definition of done

All must hold:

```text
source-bound four-generator module and executable boundary
explicit ordinary compact A/B submodule; meridian survives its quotient
both nested CCE-2 route certificates replay
exact upper/lower endpoint classes
independent affine compact uncertainties retained
exact meridian and CPV identities
selected CPV distinguished from transported affine half-sum
full coefficient-ring diamond enforced
no-integral-i obstruction replayed
absolute, quotient, affine, and scalar-extended scopes are distinct
stable refusals for all unsupported requests
deterministic checkpoint/resume and clean-process bundle
legacy, CCE-1, and CCE-2 locks unchanged
stale Pathfinder scout has zero production references
accurate standalone stage report and gap ledger
```

Passing software tests without these mathematical distinctions is not done.

---

## 16. Expected successful gap ledger

| Obligation | Expected status |
|---|---|
| Exact upper/lower corridors | PROVED, imported from CCE-2 |
| Typed `(A,B,mu,delta)` module | PROVED AND IMPLEMENTED |
| Boundary and compact quotient | PROVED AND IMPLEMENTED |
| Meridian relation | PROVED AND IMPLEMENTED |
| CPV over `Z[1/2]` | PROVED AND IMPLEMENTED |
| Gaussian ring separation | PROVED AND IMPLEMENTED |
| No integral replacement for `i` | PROVED AND IMPLEMENTED |
| Compact corrections | RETAINED AS AFFINE UNCERTAINTY |
| Absolute compact corrections and full A/B matrices | OPEN |
| Bounded observables | DEFERRED TO CCE-4 |
| General Gauss--Manin/Picard--Fuchs continuation | DEFERRED TO CCE-5 |
| Surface clearance/native lift | DEFERRED TO CCE-6 |
| Galois/horizon adapter | DEFERRED TO CCE-7 |
| Realization equivalence and third realization | SEPARATE RESEARCH GATES |

Do not upgrade an open item because an interface or placeholder exists.

---

## 17. Immediate execution order

```text
1. Record repository/worktree identity; preserve unrelated changes.
2. Replay CCE-0/PF-0/CCE-1/CCE-2 and frozen digests.
3. Resolve/digest mathematical authority.
4. Verify or apply Appendix A's narrow Paper III insertion.
5. Produce and verify the basis manifest.
6. Implement exact rings and the coefficient diamond.
7. Implement exact, quotient, and affine classes.
8. Import both CCE-2 route certificates.
9. Build lateral classes and verify the meridian relation.
10. Build endpoint, quotient, and affine CPV objects.
11. Implement the i-boundary obstruction.
12. Implement certificate, standalone replay, and checkpoints.
13. Integrate API and stable refusals.
14. Run hostile/tamper/determinism/regression tests.
15. Emit bundle, reports, benchmarks, and gap ledger.
```

If a genuine missing theorem appears, preserve verified work, emit `BLOCKED`
with the smallest exact obligation, and do not substitute an assumption.

---

## Appendix A. Paper III corridor insertion carried from CCE-2

Use only if the verified CCE-2 result has not already been incorporated. Place
after the paragraph introducing the Stage-3 corridors, adjusting numbering but
not content.

> **Lemma — exact representatives of the two DBP corridors.** The upper
> corridor is represented in the `sigma`-plane by the certified seven-segment
> `Q(i)` polygon with word `a_+`, counterclockwise about `sigma=+i`. The lower
> is its complex conjugate, with word `a_-^{-1}`, clockwise about `sigma=-i`.
> Each admits an open radius-`1/8` curve-level tube avoiding `sigma=0` and
> `rho=0`; its lift from `(1,+sqrt(2))` is unique in the nonsingular pullback
> cover and ends at `(1,-sqrt(2))`. On the return stem the upper route has
> `Im(m)<0` and selects `delta_-^up`; the lower has `Im(m)>0` and selects
> `delta_-^down`. Therefore `G_up[delta_+]=[delta_-^up]` and
> `G_down[delta_+]=[delta_-^down]` modulo `Z[A_-]+Z[B_-]`.

Retain:

```text
G_up(delta_+)   = delta_-^up   + lambda_up
G_down(delta_+) = delta_-^down + lambda_down
lambda_up,lambda_down in Z[A_-]+Z[B_-].
```

Cite exact CCE-2 manifests/certificates. Do not call the curve tube a surface
sweep, remove compact corrections, or assert an absolute scalar equality.

---

## Appendix B. The theorem compiled by CCE-3

### Theorem CCE-3.1 — typed lateral transport and CPV separation

For the certified CCE-2 corridors and marked endpoint basis
`(A_-,B_-,mu_-,delta_-^up)`, with primitive positive `mu_-` and
`Lambda_ell=Z*A_-+Z*B_-`:

1. The exact quotient transports are `(0,1)` and `(1,1)` in basis
   `(mu,delta)`, while the absolute transports remain affine over independent
   `lambda_up,lambda_down` in `Lambda_ell`.
2. `delta_-^up-delta_-^down=-mu_-`.
3. `delta_-^CPV=delta_-^up+mu_-/2` lies in `H_Z tensor Z[1/2]` but not `H_Z`.
4. The transported affine half-sum is
   `delta_-^CPV+(lambda_up+lambda_down)/2`; only its compact quotient is fixed.
5. The minimal rings for lateral, CPV, phased lateral, and phased CPV classes
   are `Z`, `Z[1/2]`, `Z[i]`, and `Z[1/2,i]`.
6. No integral class is congruent to a phased lateral or CPV class modulo
   closed cycles, since its boundary would have to be `i*beta`, outside
   `Z*beta`.

The CCE-3 verifier establishes all six statements by exact replay from nested
route certificates, the basis manifest, and coefficient arithmetic.
