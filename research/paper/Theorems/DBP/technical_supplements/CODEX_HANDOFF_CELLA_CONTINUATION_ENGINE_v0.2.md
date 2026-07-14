# Codex handoff — Cella Continuation Engine v0.1

**Audience:** Codex working in the Cella repository  
**Date:** 2026-07-14  
**Status:** implementation handoff  
**Primary campaign:** reusable certified continuation for the primary and dual DBP elliptic routes  
**Later adapters:** Galois/horizon cover, then role-cover transport

---

## 0. Assignment

Build the **Cella Continuation Engine (CCE)** as a typed, proof-carrying,
resumable continuation layer around the released DBP native relative-period
evaluator.

Do not turn the existing evaluator into an unrestricted numerical elliptic
library. Preserve evaluator v1.0 as an immutable terminal backend and regression
anchor. Put the new continuation semantics in a sibling package with explicit
adapters.

The core contract is:

```text
exact family manifest
+ exact selected state
+ exact admissible path
+ requested observable
+ requested proof precision
->
transported typed state
+ certified value enclosure, when defined
+ independently replayable certificate
```

The engine must continue the complete selected geometric state before evaluating
an observable. It must never identify a continuation solely by a decimal value,
a target name, or a sheet sign.

Work stage by stage. A failed proof obligation is a valid stopping point and must
produce a structured gap or refusal, not a numerical guess. Do not claim a later
stage because exploratory output looks convincing.

CCE exposes one proof-producing public operation. Pathfinder planning, certified
execution and certificate assembly occur in the same call:

```text
continue_certified(request)
  -> CertifiedResult
   | CertifiedPrefix
   | InsufficientProofBudget
   | UnsupportedRequest
```

Pathfinder is expected to construct valid plans by invariant, rather than emit
heuristic candidates requiring a second admissibility operation. This expected
behavior must first pass the Pathfinder confirmation gate defined below.

The independent verifier remains available for later replay, provenance,
tamper detection and third-party checking. It is not a mandatory second phase
of the normal computation workflow.
---

## 1. Operating instructions for Codex

Before editing:

```text
git rev-parse --show-toplevel
git status --short
rg --files | rg '(^|/)AGENTS\.md$|native_periods|DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR|CURVATURE_PERIODS|SELECTED_QUOTIENT|pyproject|pytest'
```

Then:

1. Read all applicable `AGENTS.md` files.
2. Preserve unrelated dirty work.
3. Inspect the existing implementation and tests before proposing a package
   layout.
4. Record and run the clean v1.0 baseline before changing production code.
5. Use small, reviewable changes and run the narrowest relevant tests after each
   change.
6. Run the complete release gates before closing a stage.
7. Do not commit, push, publish, or alter theorem papers unless the user asks.
8. Do not add a production dependency merely to make exploration convenient.

If the expected repository or source artifacts are missing, stop and produce a
precise inventory of what is present and what is needed. Do not reconstruct
missing source from filenames or from this handoff.

---

## 2. Authority and source order

Resolve and read these sources. When two sources appear to conflict, preserve the
narrower proved statement and document the conflict.

### Existing evaluator and campaign

```text
cella/engine/src/cella/native_periods/account.py
cella/engine/src/cella/native_periods/api.py
cella/engine/src/cella/native_periods/quadrature.py
cella/engine/src/cella/native_periods/terminal.py

cella/research/campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR/
  CODEX_HANDOFF_BUILD_DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR.md
  DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_BUILD_SPEC_v1.0.md
  DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_CONTRACTS_v1.0.json
  DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_GAP_LEDGER_v1.0.md
  DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_BUILD_KIT_MANIFEST_v1.0.md
  DBP_NATIVE_RELATIVE_PERIOD_ROUTE_THEOREM_v1.0.md
  DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1.md
  DBP_NATIVE_EVALUATOR_RELEASE_REPORT_v1.0.md
  DBP_NATIVE_EVALUATOR_RELEASE_REPORT_v1.0.json
  pathfinder_m1_scout.py
  periods.py
  verify_dbp_landen_trace_theorem.py
  verify_dbp_landen_trace_theorem_v1_1.py
  verify_dbp_native_relative_period_route.py
```

### Mathematical contracts

```text
/home/wlloyd/Cella Framework/research/paper/Theorems/DBP
  DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md
  especially Sections 7D–7F and Theorem 7F.1

  SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md
  especially coefficient typing and selected quotient classes

  DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md
  especially the open relative trace-path coefficients (a,b,c)

  the Stage-2 and Stage-3 dual surface-cycle reports and exact verifiers

  galois_horizon_cover_v1_0.tex
  only when the later algebraic-cover adapter begins
```

### Precedence

```text
proved theorem scope
    > exact release contract and verified machine record
    > Pathfinder guarantees confirmed by the PF-0 behavior audit
    > this implementation handoff
    > unconfirmed exploratory scripts
    > floating-point observations outside a proved construction invariant
```

Code behavior is authoritative for legacy compatibility, but it cannot broaden a
mathematical theorem.

---

## 3. Immutable evaluator v1.0 baseline

The first task is to create a local machine-readable baseline lock from the
released JSON and rerun every release gate.

Preserve all of the following:

```text
release verdict                         PASS
repository tests                        37 passed
evaluator gate assertions               1,570
exact theorem/route assertions           47 + 75 + 18
released evaluations                     6
hostile refusal cases                    6/6
production reachable modules             14
forbidden dependency hits                0
```

The canonical six-certificate bundle digest is:

```text
47b82d536982fb27ff730da6311f0340e9da81ae04e3a91c3c78348d6c8cc66e
```

The six released certificate digests are:

```text
primary, 192 bits
525fdf2e47489665d32b42d7c1e4b264fdb03484a628915ae891acae39164a53

dual_cpv, 192 bits
abacc446b534fa1f7faad68547c1eb26a02271e7fbb42331e5186015d0402db8

primary, 256 bits
d1abc1f32245743ee0d8edaf6b1f7bc5617827121941fdaca738b762283cfa82

dual_cpv, 256 bits
1f9f15eaeb066a7b386fef3291e9cc60df2cc80ab8c5b017e89a1b56465abdf6

primary, 384 bits
bb649bafb2b28726d8e74857dfeb005ea7d4962600c58ce322f9fa3a800baadc

dual_cpv, 384 bits
3b18abf87358e8d1d24e77e6f06455097e6afaa602519d07a27b9dcfa709f36b
```

The existing public behavior and certificate bytes are immutable. A continuation
certificate may contain or reference a legacy certificate, but it must use a new
schema identifier and digest. Never revise the legacy schema and label the result
compatible.

Preserve the existing refusal semantics:

```text
wrong sheet / wrong path / missing CPV
  -> unsupported_relative_path:path_gate

altered pole or source identity
  -> route_identity_failed:source_ledger

tampered arithmetic account
  -> account_not_closed:account_ledger
```

Preserve evaluator v1.0 exactly: Pathfinder remains absent from the legacy
runtime and legacy certificate schema.

For the new CCE path, do not assume either that Pathfinder is untrustworthy or
that its output is valid by construction. First complete PF-0. If PF-0 confirms
the constructor invariant, Pathfinder may be imported into the new
proof-producing runtime and its canonical output may become certificate
evidence.

Arb/FLINT, CAS packages and external special-function libraries remain
non-certifying referees unless separately admitted by a later dependency and
proof-kernel decision.

If the clean baseline does not match the release record, stop implementation and
write a discrepancy report. Do not “repair” the baseline opportunistically.

---

## 4. First-release scope fence

The first CCE release is a certified continuation engine for the **two proved DBP
shear-cover corridors**, not arbitrary global continuation.

### Supported initially

```text
coefficient field       Q(sqrt(2), i), using the existing exact encoding
parameter family        the DBP shear elliptic family
paths                   exact representatives inside the two proved corridors
route endpoints         u_+ -> u_-
selected states         primary, upper lateral, lower lateral, CPV midpoint
coefficient rings       Z, Z[1/2], Z[i], Z[1/2,i]
singularities           avoided simple poles and certified removable forms
class status            full typed state and/or quotient modulo compact A/B
observables             theorem-compiled DBP curve and native swept observables
certification           exact path, topology, analytic account and replay
```

### Explicitly deferred research fronts

Do not mark any of these complete without a separate proof and gate:

```text
B-045: general analytic-atom composition for arbitrary computation DAGs
arbitrary rational differentials and a general Hermite reduction compiler
general algebraic number fields beyond Q(sqrt(2),i)
arbitrary paths in the full shear-parameter plane
unsupported discriminant or pole wall crossing
higher-order finite-part pole prescriptions
full A/B monodromy and the compact correction coefficients (a,b,c)
whole-surface homology beyond the native swept image
importing Pathfinder guarantees or outputs before completion of PF-0
runtime numerical CPV crossing
generic Arb-style or special-function-library breadth
```

The current evaluator has only a restricted composition lemma for two fixed
straight-line programs. For the first continuation release, use an explicitly
enumerated `KernelSpec` grammar derived from the audited evaluator operations.
Unknown operations must refuse. Do not claim that this closes B-045.

---

## 5. Mathematical contract: DBP elliptic adapter

### 5.1 Parameter cover

The exact parameter cover is:

```text
U_tilde^o = {
    (sigma,rho) in C^2 :
    rho^2 = 1 + sigma^2,
    rho != 0,
    sigma != 0
}
```

Define:

```text
c = (rho - 1)/(rho + 1)
m = (rho - 1)/(2*rho)
n = -m^2/(1 - 2*m)
```

The deck involution is:

```text
tau(sigma,rho) = (sigma,-rho)

c o tau = c^(-1)
m o tau = 1-m
n o tau = 1-n
```

The standard endpoints are:

```text
u_+ = (1,+sqrt(2))
u_- = (1,-sqrt(2))
```

An accepted input path is either an exact path in `U_tilde^o`, or an exact path
in the `sigma`-plane with a certified initial lift. In the second case, certify
the unique lifted branch and report its deck parity.

Endpoint agreement does not identify a route. The certificate must include exact
winding data about `sigma=+i` and `sigma=-i`.

The initial route manifests are the exact representatives of:

```text
ell_up     : u_+ -> u_- through the certified corridor about sigma=+i
ell_down   : u_+ -> u_- through the certified corridor about sigma=-i
```

Extract the actual path data from the Stage-3 sources. Do not substitute the
phrase “standard based path.” If those sources contain only an isotopy class and
no exact representative, record that as a route-specification gap. Derive and
prove a valid exact representative as a separate lemma before encoding it.

### 5.2 Full relative state

At an admissible parameter `u`, use:

```text
C_u       : y^2 = x(x-1)(x-m(u))
C_u^o     : C_u minus {P_u^+,P_u^-}
Q_0       : (0,0)
Q_m       : (m,0)
H_Z(u)    : H_1(C_u^o,{Q_0,Q_m};Z)
```

The two poles lie over:

```text
x_p = m/n = 2 - 1/m
```

Represent a marked state on a basis equivalent to:

```text
(A, B, mu, delta)
```

where:

```text
A,B     generate the ordinary compact elliptic lattice
mu      is the primitive selected-pole meridian
delta   is the selected endpoint-relative class
```

The state must also carry:

```text
sheet and branch labels
pole label and indentation side
endpoint ordering and orientation
boundary map
intersection convention
coefficient ring
known quotient submodule
known and unknown compact corrections
```

The boundary invariant is:

```text
partial(A) = partial(B) = partial(mu) = 0
partial(delta) = beta
beta = [Q_m] - [Q_0]
```

Integral lateral transport must preserve this boundary and act by an exact
integral unimodular map wherever a full lattice map is claimed. It must preserve
the declared intersection convention, for example `A.B=+1`.

Never reduce this state to a scalar before transport. A scalar-only engine loses
the compact-period and meridian information needed by the ensemble.

### 5.3 Singular set and clearance

Every route must carry a positive exact clearance certificate from the full
singular set relevant to its requested observable. At minimum certify:

```text
rho != 0
sigma != 0
m not in {0,1,infinity}
P_u^+ != P_u^-
P_u^+,P_u^- avoid Q_0,Q_m
the two third-kind poles stay distinct
```

For a native surface lift also certify avoidance of:

```text
v = 1/c
v = 1/c^2
the norm discriminant
the polar divisor
the swept-boundary collision locus
```

Acceptable proof mechanisms include exact factor signs, algebraic root
isolation, interval Newton, Rouché bounds, and certified subdivision.
Floating-point sampling is not a clearance proof.

The initial release must refuse an actual wall crossing. A later wall-crossing
adapter may admit one only after it has a proved local normal form, an oriented
vanishing cycle and an exact jump rule.

### 5.4 Branch continuation

At each local continuation center, isolate the selected branch and prove a
uniqueness statement of the form:

```text
F(c,y_0) = 0
0 notin F_y(D(c,r) x Y)
```

or an equivalent exact Rouché/interval-Newton condition.

For a Taylor step `h`, certify:

```text
q = |h|/r < 1
```

and an explicit Cauchy or Taylor remainder. If `|f| <= M` on the certified disk,
one admissible integral-tail form is:

```text
tail_N <= M*r*q^(N+2) / ((N+2)*(1-q))
```

Use the bound appropriate to the implemented recurrence and record its theorem
identifier. The next sheet is accepted only if its terminal enclosure lies in
exactly one root isolator in the overlap. Never select the nearest floating root
without a uniqueness witness.

The target termination theorem is:

```text
dist(gamma([0,1]), Sigma) >= eta > 0
    =>
for every requested p, a finite certified disk chain transports
the selected state and returns any requested supported enclosure
with width <= 2^(-p).
```

If the proof budget cannot establish this for a request, return a typed refusal.

### 5.5 Proved corridor transport

The engine must encode the proved quotient statements, not stronger integral
identities:

```text
G_up(delta_+)
  = delta_-^up + lambda_up

G_down(delta_+)
  = delta_-^down + lambda_down

lambda_up,lambda_down in Z*A_- + Z*B_-
```

Equivalently, modulo the ordinary compact lattice:

```text
G_up[delta_+]   = [delta_-^up]
G_down[delta_+] = [delta_-^down]
```

Do not set `lambda_up` or `lambda_down` to zero. Their exact compact coordinates
have not been determined.

The exact lateral relation is:

```text
delta_-^up - delta_-^down = -mu_-
```

The pole-side calculation must be certified from the path orientation and local
geometry, not inferred from the route name. Under the existing convention, the
return stem about `+i` selects the upper indentation and the route about `-i`
selects the lower indentation.

For a supported vanishing cycle `nu`, construct Picard–Lefschetz transport
exactly from the marked intersection form:

```text
T_nu(x) = x + <x,nu>*nu
```

Include the orientation and sign convention in the certificate. Never recover
an integral monodromy matrix by rounding an approximate period matrix.

### 5.6 Quotient and absolute-value typing

The null submodule is exactly:

```text
Lambda_ell = Z*A + Z*B
```

The quotient is:

```text
H_Z/Lambda_ell
```

The meridian is not in this null submodule. Upper and lower lateral routes
therefore remain distinct in the quotient.

Every output must state which of these it represents:

```text
exact class in H_Z
class in H_Z/Lambda_ell
scalar extension of one of those classes
period modulo a compact-period lattice
absolute period of a fixed representative
```

If only a quotient class is known, do not emit an absolute scalar period unless a
representative and its compact correction have been fixed. The possible values
form an affine torsor over the relevant compact-period lattice.

The open integral comparison is:

```text
[Gamma_-^up]
  = [Gamma_+] + a[A] + b[B] + c[mu]

[Gamma_-^down]
  = [Gamma_+] + a[A] + b[B] + (c+1)[mu]
```

The integers `(a,b,c)` and complete `A/B` monodromy matrices are research
outputs. They are not fixtures and must not be hard-coded.

### 5.7 CPV and coefficient typing

CPV is a derived midpoint of two separately certified lateral classes:

```text
delta_-^CPV
  = (delta_-^up + delta_-^down)/2
  = delta_-^up + mu_-/2
```

It is not a single integral path. The minimal displayed coefficient rings are:

```text
delta^up, delta^down       : Z
delta^CPV                  : Z[1/2], not Z
i*delta^up, i*delta^down   : Z[i], not Z
i*delta^CPV                : Z[1/2,i]
```

Make the ring part of the class type, not a descriptive string attached after
the computation. Refuse a request whose declared ring is too small.

Multiplication by `i` cannot be replaced by an integral Picard–Lefschetz class
after adding closed cycles. The boundary obstruction is:

```text
partial(z) = i*beta
```

which is impossible for integral `z`, since its boundary lies in `Z*beta`.

The trace observables are normalized by:

```text
I_primary
  = (1/2)*integral_(Gamma_+) Theta - 2*pi

I_dual,CPV
  = -(i/2)*CPV integral_(Gamma_-) Theta
```

The released terminal evaluator uses the already-proved smooth reductions:

```text
primary
  = (1/2)*integral_0^1 g_+(t) dt - 2*pi

dual_cpv
  = (1/2)*integral_0^1 g_-(t) dt
```

The dual runtime is intentionally pole-free. Do not reinterpret that smooth
kernel as a runtime numerical crossing. A generic CPV result is accepted only
when both lateral route certificates, their exact meridian difference and their
typed half-sum are present.

### 5.8 Native surface lift

The surface adapter is defined only on the admissible curve subgroup:

```text
L_Z,u : H_Z^adm(u) -> H_2(X_u,Y_u;Z)

S_Z^nat(u) = image(L_Z,u)
```

It must carry an integral signed reduction:

```text
R_Z,u : S_Z^nat(u) -> H_Z^adm(u)
```

and verify:

```text
R_Z,u o L_Z,u = 4*id
```

The allowed consequences are:

```text
L_Z is injective
G_eta^S o L_Z = L_Z o G_eta^C
integral_(L_Z(delta)) K_u = integral_delta Omega_u
```

Do not treat `(1/4)R_Z` as an integral inverse; it is a left inverse only after
inverting `2`.

All conclusions are restricted to `S_Z^nat`. Do not claim:

```text
S_Z^nat equals the whole surface homology
the lifted meridian is primitive in the whole surface lattice
CPV is nonintegral against arbitrary whole-surface classes
R_Z extends integrally to the whole relative surface group
```

---

## 6. Software architecture

Prefer a sibling package so the legacy evaluator remains frozen. Adjust names
only to match established repository conventions.

```text
cella/engine/src/cella/continuation/
  __init__.py
  api.py                 public compile/continue/resume/verify operations
  model.py               immutable typed request/result/state records
  rings.py               Z, Z[1/2], Z[i], Z[1/2,i]
  algebraic.py           exact field elements and root isolators
  paths.py               exact segments, arcs, concatenation and reversal
  clearance.py           singular-divisor and tube-clearance proofs
  analytic.py            analytic disks, Taylor models and tail bounds
  transport.py           local steps, composition and transport matrices
  ledger.py              source, route, class, residue and account ledgers
  certificate.py         canonical encoding and digests
  verifier.py            independent replay entry point
  checkpoint.py          certified-prefix checkpoint and resumption
  refusals.py            stable refusal codes and obligations
  adapters/
    base.py              adapter protocol
    dbp_native_v1.py     immutable evaluator compatibility facade
    dbp_elliptic.py      shear-cover and relative-period semantics
    dbp_surface.py       native swept lift; later first-family stage
    dbp_horizon.py       algebraic-cover semantics; later second-family stage
    dbp_role.py          rational chart/role transport; deferred adapter
```

Initially wrap stable exact primitives in `native_periods`; do not move them.
Only extract shared code after a compatibility gate proves that the legacy path
and bytes are unchanged.

### Proof-producing single-pass architecture

Subject to PF-0 confirmation:

```text
adapter
  family equations, singular divisors, selected state, local-system data,
  exact topological events, observable normalization and endpoint meaning

Pathfinder
  accepts an admitted exact request
  constructs a valid route and execution schedule by invariant
  distinguishes unsupported input from a valid but inadequate schedule
  emits a canonical plan record and digest

continuation executor
  consumes the Pathfinder plan in the same public operation
  transports the typed state
  evaluates the supported observable
  closes the analytic and arithmetic accounts

certificate assembler
  records the Pathfinder construction, transported state, accounts,
  enclosure and canonical digest

verifier
  later replays the canonical construction and execution accounts
  for provenance, tamper detection or independent checking
```

The public workflow is one operation:

```text
request
  -> Pathfinder construction
  -> certified execution
  -> result plus replayable certificate
```

Do not describe Pathfinder output as an untrusted proposal unless PF-0 actually
finds a reachable invalid-output condition.

Validity and adequacy are separate:

```text
validity
  the constructed route, radii, panels and transitions satisfy Pathfinder's
  admitted-state invariants

adequacy
  the valid schedule is strong enough to attain the requested enclosure width
  under the supplied proof budget
```

An adequacy failure must not be reported as an invalid Pathfinder output.

After PF-0 confirmation, canonical Pathfinder output is certificate evidence
within the exact scope of the confirmed constructor invariant. The certificate
must preserve the Pathfinder version, exact request, admitted domain, canonical
plan and plan digest. Any numeric representation used by Pathfinder must be
documented with its precise semantics and assumptions.

---

## 7. Typed data model

Use immutable records. At minimum define:

```text
CoefficientRing
AlgebraicFieldSpec
AlgebraicNumber
ExactPathSegment
ExactPath
FamilyManifest
SingularDivisorManifest
RelativeModuleSpec
SelectedState
ObservableManifest
ProofBudget
PathfinderPlan
ContinuationRequest
RoutePlan
RouteCertificate
EvaluationCertificate
ContinuationCheckpoint
ContinuationResult
VerificationReport
Refusal
```

Important invariants:

```text
exact algebraic numbers use minimal polynomials plus isolating intervals
or rectangles, never decimal labels

paths contain exact segment data and orientation

states contain a basis digest, boundary map, intersection data,
coefficient ring and quotient submodule

every route plan contains the source theorem and manifest digests

every evaluation references a certified route digest

every resumed run verifies the checkpoint chain before continuing
```

The primary public API is:

```text
continue_certified(request)
  -> CertifiedResult
   | CertifiedPrefix
   | InsufficientProofBudget
   | UnsupportedRequest
```

Supporting operations are:

```text
resume_continuation(checkpoint)
compose_routes(left,right)
reverse_route(route)
evaluate_observable(state,observable,bits)
verify_continuation_certificate(certificate)
explain_outcome(outcome)
```

Pathfinder plan construction is internal to `continue_certified`. A diagnostic
operation may expose the canonical plan for inspection, but users do not need
to call separate `compile_route` and `certify_route` operations.

The result distinguishes:

```text
CertifiedResult
  the valid plan completed and the requested accounts closed

CertifiedPrefix
  a prefix completed and is independently replayable; the remainder is saved

InsufficientProofBudget
  the plan remains valid, but the requested enclosure width was not achieved

UnsupportedRequest
  the request lies outside Pathfinder's confirmed admitted domain
```

An MCP layer may expose these operations only after the Python core and verifier
are stable. It must return one of:

```text
status = certified
result + certificate digest

status = incomplete_certified_prefix
checkpoint + proved prefix + remaining path

status = refused
stable refusal code + failed proof obligation
```

Never return an uncertified bare decimal as a successful response.

---

## 8. Resumption and ongoing-work semantics

CCE is intended for continuing research computations over multiple runs. Make
checkpointing a proof feature, not only a performance cache.

A `ContinuationCheckpoint` must contain:

```text
source and family manifest digests
adapter id and version
Pathfinder version and confirmation-report digest
canonical Pathfinder plan digest
exact path digest
certified prefix endpoint
transported typed state
cumulative transport matrix or quotient action
cumulative pole/residue/winding ledger
cumulative analytic account
coefficient ring
previous checkpoint digest
next segment index
remaining exact path
canonical checkpoint digest
```

Resumption rules:

```text
verify the entire digest chain before resuming
require identical source, family, basis, ring and path manifests
resume only when the recorded Pathfinder version, admitted-domain identifier,
canonical plan and checkpoint chain reproduce their recorded digests
append new certified steps without rewriting prior evidence
compose prefix and suffix transports exactly
report only the prefix as certified if the suffix fails
```

Content-addressed reuse is allowed only when the exact problem, path fragment,
basis, coefficient ring and theorem manifests match. A cache hit must still pass
certificate verification.

---

## 9. Certificate model v2

Represent route admissibility and numerical evaluation as separate artifacts
created within the same `continue_certified` execution:

```text
RouteCertificate
  proves that the exact source, selected state and path define an admitted
  transport and records the resulting typed state

EvaluationCertificate
  references a RouteCertificate and proves a requested observable enclosure
```

Use a canonical schema containing at least:

```text
schema
  schema_id
  schema_version
  canonicalization_version

source_ledger
  adapter_id
  adapter_version
  family_manifest_digest
  differential_manifest_digest
  local_system_digest
  basis_digest
  theorem_ids_and_digests
  legacy_certificate_digest, if wrapped

pathfinder_ledger
  PF-0 confirmation-report digest
  confirmed behavior scope
  Pathfinder source and version digest
  exact request digest
  admitted-domain identifier
  canonical constructed plan
  canonical plan digest
  constructor-invariant identifiers
  numeric-representation semantics
  validity status
  adequacy parameters and requested proof budget

request
  exact start parameter
  exact path
  starting sheet
  selected class
  declared coefficient ring
  quotient submodule
  observable
  requested bits
  proof budget

domain_ledger
  discriminant and polar divisors
  exact path tubes
  clearance lower bounds
  root-isolation witnesses
  marked-point separation

continuation_ledger
  analytic or isolation disks
  overlap witnesses
  winding numbers
  sheet transitions
  exact transport events
  ordered transfer matrices

class_ledger
  coefficient ring
  starting and ending vectors
  boundary map checks
  intersection checks
  meridian relation
  CPV midpoint identity
  compact-period quotient
  unresolved compact corrections

singularity_ledger
  pole locations
  exact residues
  lateral or CPV policy
  polar-subtraction identity
  removable-singularity proof

analytic_ledger
  chart maps
  panel or disk schedule
  analytic radii
  recurrence orders
  Cauchy or Taylor bounds
  tail bounds

surface_ledger, when requested
  native-image membership
  L_Z and R_Z data
  R_Z L_Z = 4 id witness
  naturality and pairing witness

account_ledger
  exact component enclosures
  constants and normalizations
  final dyadic interval or rectangle
  achieved width

checkpoint_chain
  previous digest
  certified prefix
  remaining path digest

replay
  verifier version
  canonical certificate digest
```

The verifier must not trust precomputed booleans. It must replay the exact
equalities and inequalities needed for clearance, branch uniqueness, transport
typing, account closure and target width.

For confirmed Pathfinder scope, it checks that the recorded exact request,
Pathfinder version and canonical plan reproduce the recorded plan digest and
fall within the confirmed admitted domain. It then replays the transported
state, analytic accounts, arithmetic closure and output enclosure.

The verifier is not required to pretend that a valid-by-construction Pathfinder
plan was a heuristic candidate. Its role is deterministic replay, provenance,
account verification and tamper detection.

---

## 10. Implementation campaign

### CCE-0 — Repository audit and baseline lock

Tasks:

```text
inventory source, tests, schemas and campaign artifacts
run every legacy test and exact verifier
recreate the six released evaluations in clean processes
record exact versions, commands, timings and digests
create a baseline-lock JSON
```

Acceptance:

```text
all v1.0 gates match the released report
no production source changes
all six legacy certificates replay byte-identically
all hostile refusals retain their exact outcomes
```

Stop on any discrepancy.

### PF-0 — Confirm Pathfinder construction semantics

This gate must complete before Pathfinder is imported into the CCE runtime or
certificate schema.

The working hypothesis is:

```text
For every admitted request q,

    Pathfinder(q) -> ValidPlan

or

    Pathfinder(q) -> UnsupportedRequest.

No reachable admitted state returns an invalid plan.
```

Codex must confirm this from the actual implementation. Do not confirm it merely
because this handoff, the release report or the user states it.

#### Required audit

1. Locate and read the complete Pathfinder implementation, tests, architecture
   notes and callers.
2. Identify the admitted request domain, internal state representation, state
   transitions, terminal states, output constructors, failure states, numeric
   representations, rounding assumptions, determinism and canonicalization.
3. Trace every reachable output-producing branch. Establish whether validity is
   enforced structurally by constructors, transition invariants, exact guards or
   a previously proved theorem.
4. Determine whether hidden mutable state, ambient precision, platform behavior,
   cache content, iteration order or uncontrolled randomness can change the
   semantic output.
5. Separate invalid plans from valid but insufficient schedules, unsupported
   requests, resource exhaustion and implementation exceptions.
6. Confirm whether the released high-precision schedule failure was solely an
   adequacy failure—a valid schedule whose Cauchy remainder was too wide.
7. Run deterministic clean-process replay over all released DBP requests,
   boundary values of every admitted input field, output-producing transitions,
   unsupported inputs, precision-budget variations, and hostile cases.

Tests supplement the state-invariant argument; passing tests alone is not enough
to establish that invalid states are unreachable.

#### Required deliverables

```text
PATHFINDER_BEHAVIOR_CONFIRMATION_REPORT_v1.0.md
PATHFINDER_BEHAVIOR_CONFIRMATION_REPORT_v1.0.json
pathfinder admitted-domain schema
state-transition and constructor inventory
deterministic replay digests
validity-versus-adequacy test matrix
exact scope of any imported guarantee
```

#### Verdicts

```text
CONFIRMED
  Every admitted request produces a valid plan or a typed unsupported result.
  Pathfinder may be imported as the CCE plan constructor.

CONFIRMED_WITH_SCOPE
  The invariant holds only for an explicitly identified request or output
  subset. Import only that subset; retain checks or refusals elsewhere.

NOT_ESTABLISHED
  No invalid plan was found, but the implementation evidence is insufficient
  to prove unreachability. Preserve the current boundary and report the missing
  obligation without calling Pathfinder flawed.

CONTRADICTED
  A reproducible admitted input reaches an invalid output. Record the exact
  state, transition and counterexample before proposing a repair.
```

Only `CONFIRMED` and the explicitly enumerated portion of
`CONFIRMED_WITH_SCOPE` authorize Pathfinder output as CCE certificate evidence.

#### Acceptance

PF-0 passes only when Codex can state and support a precise theorem-shaped
contract such as:

```text
Pathfinder :
    AdmittedRequest
      -> ValidPlan | UnsupportedRequest

ValidPlan guarantees:
    route identity
    allowed sheet transition
    admissible radii and subdivisions
    canonical schedule representation
    deterministic plan digest
```

### CCE-1 — Compatibility facade and certificate envelope

Tasks:

```text
create immutable request/result models
create the adapter protocol
create dbp_native_v1 as a delegate to the untouched evaluator
create the single public continue_certified facade around the PF-0-authorized
Pathfinder constructor
create route/evaluation certificate envelopes
create canonical verification and checkpoint primitives
```

Acceptance:

```text
legacy API output and certificate bytes are unchanged
all six old digests remain unchanged
new envelope bytes are deterministic in two clean processes
the combined Pathfinder-plan, route and evaluation certificate is deterministic
tampering with the nested legacy certificate is rejected
resume refuses a mismatched source or path digest
```

### CCE-2 — Exact shear-cover path and sheet continuation

Tasks:

```text
implement exact path segments, concatenation and reversal
encode exact ell_up and ell_down manifests
certify winding around +i and -i
continue rho from +sqrt(2) to -sqrt(2)
prove local branch uniqueness and overlap matching
certify complete route clearance
```

Acceptance:

```text
both routes end on the proved rho=-sqrt(2) sheet
identity path transports identically
T(path_2 * path_1) = T(path_2) T(path_1)
T(path^-1) = T(path)^-1 where the exact state permits it
wrong winding, sheet, endpoint or path digest is rejected
segment, isolator or clearance tampering is rejected
certificates are byte-identical across clean processes
```

This stage may return sheet and route state before it evaluates a period.

### CCE-3 — Typed relative-class and CPV engine

Tasks:

```text
implement the exact (A,B,mu,delta) module record
implement boundary, intersection and quotient ledgers
continue the selected class along both corridors
derive pole-side and meridian events from the route
form CPV by exact scalar extension and half-sum
```

Acceptance:

```text
G_up[delta_+] and G_down[delta_+] match Theorem 7F.1
delta_-^up - delta_-^down = -mu_- verifies exactly
CPV is rejected over Z and accepted over Z[1/2]
i-lateral is rejected over Z and accepted over Z[i]
i-CPV is typed over Z[1/2,i]
unknown A/B corrections remain explicit unknowns
an absolute scalar request from quotient-only data is refused
```

Completion of CCE-0 through CCE-3 is the first useful continuation-engine
release. It supports reusable primary/dual route transport modulo compact
periods even before the full period-vector connection is available.

### CCE-4 — Bounded generic observable evaluation

Tasks:

```text
derive an audited finite KernelSpec opcode grammar from native_periods
compile both released smooth kernels through that grammar
reuse exact dyadic arithmetic, recurrence scheduling and analytic bounds
attach evaluation certificates to route certificates
add certified checkpoints at panel/disk boundaries
```

Do not generalize to arbitrary expression DAGs. Unknown operations refuse with
`unsupported_opcode`.

Acceptance:

```text
the generic path encloses all six released brackets
the legacy path remains byte-identical
results at increasing precision are nested
subdivision and checkpoint/resume preserve the enclosure
direct legacy and new continuation enclosures overlap
the dual observable remains an exact polar subtraction plus smooth evaluation,
not a numerical CPV cancellation
```

### CCE-5 — Certified Gauss–Manin/Picard–Fuchs continuation

Begin only after deriving an exact basis convention and differential system.

The analytic system may have the form:

```text
Y'(t) = A(t)Y(t) + b(t)
```

with homogeneous augmentation:

```text
d/dt [Y] = [A(t) b(t)] [Y]
     [1]   [  0    0 ] [1]
```

Keep the analytic connection matrix and exact topological transport in separate
accounts, then prove their compatibility.

Acceptance:

```text
every local transfer has a certified remainder
ordered transfer products replay exactly
topological matrices are exact integral matrices
boundary and intersection data are preserved
closed-loop matrices satisfy proved group relations
no matrix is accepted by numerical near-integrality
```

The decisive research target is to determine, rather than assume, `(a,b,c)` and
the complete `A/B` monodromy. If these remain open, the engine must retain its
quotient-valued output.

### CCE-6 — Native swept-surface adapter

Tasks:

```text
encode the admissible-domain predicate
implement typed L_Z and R_Z manifests
verify R_Z L_Z = 4 id
verify transport naturality and the period pairing
support curve and native swept-surface observables
```

Acceptance:

```text
G_surface L_Z = L_Z G_curve
integral_(L_Z(delta)) K = integral_delta Omega
R_Z L_Z = 4 id
curve and surface coefficient typing agrees
classes outside S_Z^nat are refused
no whole-surface conclusion is emitted
```

### CCE-7 — Algebraic-cover adapter for the Galois/horizon arm

Only start after the elliptic engine passes its release gates.

The shared core may provide paths, discriminant clearance, root isolation,
overlap matching, checkpoints, certificates and refusals. The adapter state is
different:

```text
initial labelled root set
selected physical root
terminal root isolators
sheet permutation
inertia element
Kummer parity or sign data
physical-selection evidence
```

Its transport is:

```text
T_gamma : Roots(F_0) -> Roots(F_1)
```

Do not identify this permutation action with relative-homology transport. They
share a continuation protocol, not a single unproved holonomy operator.

### CCE-8 — Role-cover adapter

This later adapter may reuse exact paths, chart clearance, certificates and
checkpoints for rational jet recharting, role permutations, channel data and
role-divisor refusals. It must have its own state and transport law. Do not infer
an intertwiner with the elliptic or Galois adapters.

---

## 11. Stable refusal vocabulary

Preserve the legacy refusal codes and add versioned CCE codes such as:

```text
unsupported_adapter
unsupported_path
unsupported_opcode
unsupported_coefficient_field
insufficient_coefficient_ring
route_manifest_missing
route_identity_failed
path_not_exact
path_hits_discriminant
path_hits_pole
polar_clearance_failed
marked_endpoint_collision
unsupported_wall_crossing
ambiguous_branch
branch_overlap_not_unique
sheet_transition_failed
endpoint_mismatch
transport_not_unimodular
boundary_not_preserved
intersection_not_preserved
cpv_lateral_pair_missing
cpv_policy_missing
invalid_polar_subtraction
quotient_representative_not_fixed
surface_class_outside_native_image
surface_scope_exceeded
proof_budget_exhausted
insufficient_recurrence_budget
transport_ledger_not_closed
residue_ledger_not_closed
analytic_account_not_closed
checkpoint_chain_invalid
certificate_digest_mismatch
hidden_runtime_dependency
```

Every refusal must contain:

```text
stable code
failed obligation
exact source/path location where possible
whether subdivision or a larger proof budget could help
whether a new theorem or adapter is required
no uncertified replacement value
```

Refusal is a certified outcome, not a crash and not an invitation to fall back to
floating-point nearest-root selection.

---

## 12. Mandatory tests

### Compatibility

```text
all existing tests and exact verifiers
six legacy byte-identical certificate replays
six released bracket/digest checks
legacy hostile refusal suite
standard-library dependency audit
```

### Exact paths and groupoid laws

```text
identity
composition
reversal
associativity of certified route composition
exact winding about +i and -i
upper/lower endpoint sheet
homotopy inside a certified tube, where the theorem supplies it
tampered path segment and tampered winding
```

### Algebraic branch tracking

```text
unique initial root isolator
unique overlap match
ambiguous overlap refusal
discriminant-clearance refusal
endpoint mismatch refusal
deterministic subdivision
```

### Relative classes and rings

```text
boundary preservation
intersection preservation
integral unimodularity when claimed
upper/lower meridian identity
2*delta_CPV = delta_up + delta_down
CPV refusal over Z
i-lateral refusal over Z
explicit scalar extension
unknown compact corrections survive serialization and composition
```

### Analytic evaluation

```text
requested-width proof
nested 128/192/256-bit or release precision brackets
subdivision invariance
checkpoint/resume equivalence
direct legacy/new-engine enclosure overlap
tail-bound tampering
account tampering
unsupported opcode refusal
```

### Surface adapter

```text
native-image membership
R_Z L_Z = 4 id
lift naturality
pairing identity
outside-native-image refusal
whole-surface scope refusal
```

### Certificate and trust boundary

```text
clean-process byte determinism
source digest tampering
basis digest tampering
ring tampering
route/evaluation certificate mismatch
checkpoint-chain tampering
legacy evaluator remains Pathfinder-free at runtime
new CCE inclusion agrees exactly with the PF-0 verdict
every admitted Pathfinder request reaches a valid plan or typed unsupported state
validity and adequacy failures are distinguished
clean-process Pathfinder plans and digests are deterministic
Pathfinder source/version tampering is detected
canonical plan tampering is detected
PF-0 scoped guarantees are not applied outside their admitted domain
external referee packages absent from production closure
```

Use property tests only when their generated inputs remain exact and every failure
is reproducible from a serialized seed. Random floating tests may be diagnostic
but cannot replace exact gates.

---

## 13. Deliverables for each completed stage

Produce or update:

```text
code and focused tests
machine-readable request/result schemas
machine-readable certificate schemas
baseline-lock JSON
test/refusal matrix
stage report in Markdown
stage report in canonical JSON
gap ledger separating proved, implemented, experimental and deferred items
benchmark report with cold, marginal and verifier timings
dependency-closure report
```

Every stage report must state:

```text
exact commit or worktree identity
files changed
commands run
tests/assertions passed and failed
certificate digests
supported mathematical scope
known quotient or scalar-extension status
open proof obligations
the PF-0 verdict and imported Pathfinder scope; any external referee use remains
identified separately as non-evidence
```

Do not update the theorem papers merely because software architecture changed.
Update a theorem source only after a separately checked mathematical result has
actually changed its claim ledger.

---

## 14. Definition of done

### First reusable release: CCE-0 through CCE-3

Done means all of the following are true:

```text
evaluator v1.0 remains byte-identical and all legacy gates pass
both exact DBP corridor representatives are certified
rho sheet continuation is proved from +sqrt(2) to -sqrt(2)
the full typed (A,B,mu,delta) state is transported
upper and lower quotient classes are distinguished
the exact meridian relation is independently replayed
CPV exists only as the typed half-sum over Z[1/2]
i-normalized classes retain their Gaussian coefficient type
absolute and quotient-valued outputs cannot be confused
certified-prefix checkpoints resume deterministically
PF-0 confirms Pathfinder's admitted domain and valid-plan constructor invariant
valid schedules that miss a target width return InsufficientProofBudget rather
than being classified as invalid plans
every new CCE certificate deterministically replays against the confirmed
Pathfinder version and canonical plan without external numerical libraries
the legacy evaluator remains unchanged and retains its original dependency boundary
all unsupported paths, rings, walls and scope claims refuse cleanly
```

### Reusable numerical release: add CCE-4

In addition:

```text
both released terminal kernels pass through the bounded generic grammar
all six released brackets are enclosed by the new route
legacy certificates remain unchanged
new route and evaluation certificates are deterministic and independently checked
```

### Full family-level Picard–Lefschetz engine: add CCE-5

This title is earned only when the exact period-vector connection and integral
topological transport are both certified. Determining `(a,b,c)` is a decisive
demonstration, but do not make it a fabricated completion condition: if the
theorem remains open, report a correct quotient engine and leave the gate open.

---

## 15. Immediate start sequence

Begin with exactly this sequence:

```text
1. Locate the repository root and applicable instructions.
2. Inventory native_periods, Pathfinder, campaign artifacts, exact verifiers
   and tests.
3. Read the release JSON and regenerate a baseline-lock record.
4. Run the complete legacy release suite in clean processes.
5. Report any mismatch before editing production code.
6. Complete PF-0 by auditing Pathfinder's admitted state space, transitions,
   output constructors, determinism and validity-versus-adequacy behavior.
7. Issue a PF-0 verdict and confirmation report.
8. Import Pathfinder into the CCE runtime only to the extent authorized by
   CONFIRMED or CONFIRMED_WITH_SCOPE.
9. Create the continuation package skeleton and immutable models.
10. Implement the single public continue_certified operation around the
    confirmed Pathfinder constructor and existing evaluator.
11. Add deterministic combined certificates, checkpointing and verifier tests.
12. Close the compatibility stage before extending the supported DBP paths.
```

The governing doctrine is:

```text
construct by invariant; execute and certify in one operation; retain replayable proof.
```
