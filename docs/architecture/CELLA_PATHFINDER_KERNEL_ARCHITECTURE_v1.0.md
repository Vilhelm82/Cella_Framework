# Cella Pathfinder — Kernel Architecture and M2-Parity Design

**Version:** 1.0  
**Date:** 2026-07-11  
**Status:** Proposed canonical architecture; not an as-built capability claim  
**Target:** Replace the current Macaulay2-dependent research workflow with a Cella-native, proof-carrying, Python-importable and MCP-callable system while preserving the full intended scope: exact ideal and scheme operations, algebraic extensions, real selection, Galois/Kummer/wreath reasoning, realization strata, and local geometry.

---

## 1. Executive decision

Pathfinder should not be designed as a clone of Macaulay2, a Gröbner-basis command wrapped in Cella result types, or an accumulation of specialist mathematical scripts.

It should be designed as:

```text
Pathfinder =
    a proof-carrying,
    normalization-aware,
    stratifying algebraic-cover planner.
```

Its governing inversion is:

```text
Finding a candidate is expensive.
Checking the right candidate is usually cheaper.

Therefore:
    find over cheap representations,
    preserve the discovered route,
    certify only the required claim exactly.
```

Gröbner arithmetic remains essential, but it is one exact ideal engine inside Pathfinder. It is not Pathfinder's ontology. The system's native objects are scoped algebraic presentations, morphisms, covers, localizations, strata, field towers, group actions, accounts, claims, and certificates.

The public surface should be query-first:

```text
prove_membership
prove_ideal_equality
project_locus
restrict_to_open
classify_components
certify_dimension_and_degree
certify_prime_or_reduced
compute_minimal_polynomial
compute_square_class_rank
classify_inertia
select_real_sheet
certify_pole_order
```

The planner decides whether a query is best answered by substitution, symmetry, a regular-sequence theorem, modular Gröbner search, factorization, a resultant, a valuation argument, an exact real-algebraic method, a Kummer-module theorem, or a local normal form.

The principal design consequence is:

```text
Pathfinder computes the cheapest sufficient certificate,
not the largest conventional intermediate object.
```

---

## 2. Register discipline

Three registers must remain distinct throughout implementation and documentation.

| Register | Meaning | Current status |
|---|---|---|
| **Legacy V4** | Typed/stratified numerical-geometry engine, its eval campaigns, protocols, observers, refinery, solver and history machinery | Partly reusable; not the new kernel |
| **Current Cella** | Exact-account arithmetic, restricted symbolic rational functions, exact geometry clients, constructive elementary annex, route planner, refusals, reproducibility records and MCP adapter | As described by the current package inventory; no general ideal or Gröbner engine |
| **Cella Pathfinder** | Architecture specified here: claim compiler, exact algebra, modular scouts, proof kernel, ideal/scheme services, field/cover layers and stratified outputs | Proposed; to be built and certified |

No Pathfinder capability is to be described as implemented merely because a corresponding theorem, Python research script, M2 output, or current Cella helper exists.

The current Cella package already supplies exact rational-function operations, exact valuations, narrow Sturm and positivity proof primitives, exact quadratic-field arithmetic, geometry carriers, local pole laws, account ledgers, typed refusals, deterministic serialization and an MCP transport. It does not yet supply:

```text
domain-generic polynomial rings
general monomial orders
multivariate division and labelled normal forms
ideals and modules
S-polynomials and Gröbner completion
finite-field modular scouts
CRT and rational reconstruction
factorization
elimination and saturation certificates
Hilbert functions and scheme invariants
minimal primes or primary decomposition
general finite algebraic extensions
mathematical certificates for these results
```

### 2.1 Inheritance decision by current component

| Current asset | Decision | Pathfinder role |
|---|---|---|
| `cell.py`, `residue.py`, `observation.py` | Lift the exact-account contracts; do not universalize additive residue semantics | Arithmetic account subsystem and examples of typed reducers |
| `refusal.py` | Lift and generalize | Total outcome law, scope-bearing refusals and retry classification |
| `certificate.py` | Rename semantically | Reproducibility seal and canonical artifact digest, never mathematical proof |
| `symbolic.py` | Reuse formulas/tests; replace core representation | Seed requirements for sparse exact polynomials and rational functions |
| `proofs.py` | Lift narrow checkers and broaden independently | First source of identity, Sturm, positivity, valuation and Newton proof nodes |
| `qsqrt.py` | Generalize | Finite algebraic extension and quotient-field layer |
| `pathfinder.py` | Preserve route-planning intent; replace execution model | Claim compiler, structural recognizers, cost planner and stratifier |
| `cleanliness.py`, `residual_profile.py`, slope/observer modules | Quarantine to scout telemetry | Cost, conditioning and candidate-route estimates only |
| `carrier.py`, `tower.py`, `sensors.py`, `campaign.py` | Preserve as clients | Geometry regression corpus and theorem-directed routes |
| `periods.py`, `reference_lift.py` | Preserve as domain libraries | Formal period, role-orbit and wreath consumers of the new kernel |
| `mcp_server.py` | Lift the adapter discipline | Validation and transport around one semantic engine |
| V4 core protocols/provenance/history | Mine contracts, not universal types | Capability binding, trace identity, handled-state and replay patterns |
| V4 refinery/solver | Do not promote as foundation | Archived client experiments unless re-derived for a Pathfinder consumer |
| V4 eval campaigns | Preserve intact as adversarial corpus | Probe/referee/oracle and mutation batteries |

---

## 3. The actual parity target

The current M2 corpus does not merely ask for a Gröbner basis. It asks for this semantic deliverable surface:

```text
certified incidence ideals
certified ideal membership and equality
certified elimination/projection ideals
localized nonemptiness
dimension, codimension and grading-bound degree
minimal supports and component counts
prime, radical, reduced and primary status
scheme multiplicities and embedded components
exact specialization and degree-drop events
factorization and discriminants
real-fibre decisions
normalization-versus-projection comparisons
realization-poset incidence
```

The wider current mathematical corpus additionally requires:

```text
resultants and minimal polynomials
quotient fields and finite algebras
norms, traces and multiplication matrices
GF(p) factor-degree/Frobenius certificates
Smith normal forms and exact ranks
height-one valuations and parity rows
Kummer square-class modules
permutation, semidirect and wreath actions
branch, ramification, coalescence and rank-drop strata
exact real-root isolation and spectral selection
local Laurent/Newton/curvature normal forms
active role-jet and gauge-orbit reductions
```

M2 parity therefore means matching the requested mathematical outputs. Pathfinder parity means matching those outputs while also supplying an independently checkable warrant and correcting places where the current workflow only records an M2 attestation.

---

## 4. Governing design laws

### Law 1 — Claim before computation

Every request is compiled into a typed claim and a proof-obligation graph before an algorithm is chosen.

```text
ProblemContext + Query + RequiredGuarantee + Budget
    -> ClaimIR
    -> ProofObligationDAG
    -> candidate plans
```

The same ideal may be queried for membership, dimension, generic smoothness, prime support, real points or branch image. These are different claims and need not share the same cheapest route.

### Law 2 — Find cheaply, certify exactly

Scouts may use finite fields, specializations, floating estimates, interval numerics, external engines, heuristics and parallel exploration. They may emit candidates and routes. They may never emit mathematical truth.

```text
Scout output     = SCOUTED(candidate, route, confidence, unresolved_obligations)
Certifier output = CERTIFIED(claim, value, certificate)
                | REFUSED(reason, retained_evidence)
```

### Law 3 — Structure precedes general search

Before running a generic Gröbner or decomposition algorithm, Pathfinder checks for:

```text
direct substitution
triangularity
regular sequences / complete intersections
known symmetries and orbit transport
parity and grading constraints
finite-cover tower structure
norm/resultant structure
valuation or private-prime witnesses
local normal forms
spectral pencils
```

This is the principal route by which Pathfinder can outperform a one-to-one M2 replacement on the user's corpus.

### Law 4 — Genericity is data

Every inversion, denominator and nonvanishing hypothesis is represented explicitly. A generic result is never an unqualified result.

```text
CertifiedOnOpen(
    claim,
    open = D(h),
    excluded = V(h),
    certificate
)
```

### Law 5 — Every excluded boundary becomes a task

Saturation must not silently erase the phenomenon under investigation. When a route proves a result on an open set, Pathfinder creates exact boundary problems.

```text
Query
├── D(h): certified generic result
├── V(h_1): boundary case
├── V(h_2): rank-drop case
├── V(h_1,h_2): intersection case
└── unresolved leaf: exact ideal + typed status
```

This certified case tree is Pathfinder's natural output.

### Law 6 — Preserve presentations, towers and morphisms

Do not flatten an incidence cover, field tower or local germ into one large eliminant unless the requested claim demands it. Intermediate sheets, blocks and morphisms often contain the cheapest proof.

### Law 7 — Proof and provenance are orthogonal

```text
route history       != mathematical proof
double-run digest   != mathematical proof
M2 transcript       != mathematical proof
modular agreement   != mathematical proof
```

Pathfinder records both:

```text
procedure_verdict
answer_verdict
```

A candidate discovered by an untrusted engine can still receive an exact answer verdict. A byte-stable computation can still lack a mathematical warrant.

### Law 8 — Support, scheme and real locus are distinct

Pathfinder never silently identifies:

```text
minimal support
radical scheme
reduced scheme
primary component
embedded component
complex locus
real locus
physical chamber
```

### Law 9 — Degree is typed

A bare `degree = 24` is inadmissible. Degree must name its semantics:

```text
DegreeValue {
    value,
    grading,
    weights,
    affine_or_projective,
    homogenization,
    object_scope
}
```

`Degrees=>` and `MonomialOrder=>` are separate objects. A grading controls homogeneous data; a monomial order controls reduction.

### Law 10 — Locality before global swell

For pole orders, branch behavior and curvature cliffs, Pathfinder first asks whether a finite local germ, valuation, Newton polytope or normal-form theorem settles the claim. It does not expand a global scalar merely because a generic CAS would.

### Law 11 — Backends are disposable workers

M2, Singular, FLINT, a native F4 worker, a GPU modular worker or a numerical tracker may propose. Only a Pathfinder checker may certify.

### Law 12 — Refusal is total and typed

For every admitted query under a declared version and budget:

```text
Outcome = CERTIFIED | SCOUTED | REFUSED
```

No hidden numerical downgrade, guessed scalar, uncaught exceptional stratum or backend exception may cross the public boundary.

---

## 5. The semantic lift from Cella

### 5.1 Two axes, not one overloaded `Cell`

Current numerical Cella has the exact additive law:

```text
represented_value + exact_defect = true_value
```

That law remains valid for its admitted arithmetic account. It must not be stretched until modular images, quotient representatives or candidate bases are misleadingly called rounding residues.

Pathfinder requires two orthogonal axes:

```text
Axis A — account/reduction semantics
    how a representation reduces to its mathematical object

Axis B — epistemic status
    whether a claim about that object is scouted, certified or refused
```

### 5.2 Generalized reduction record

The correct lift is a typed reduction system:

```text
ReductionSystem[T,A] = {
    account_type: A,
    reducer: R : A -> T,
    reducer_laws,
    transport_witnesses,
    checker
}
```

Examples:

```text
Numeric account:
    A = (v,rho)
    R(A) = v + rho

Polynomial division account:
    A = (f,G,q_1,...,q_s,r)
    R(A) = sum_i q_i*g_i + r

CRT state:
    A = compatible residue images and coprime moduli
    R(A) = canonical residue modulo product(moduli)

Rational reconstruction state:
    A = modular residue, modulus, reconstruction bounds
    R(A) = candidate rational or AMBIGUOUS

Orbit reduction:
    A = representative, action, orbit/fibre data
    R(A) = invariant quotient datum
```

These account types share a reduction interface, not a false universal addition law.

### 5.3 Required semantic distinctions

```text
Residue
    exact additive defect of a lossy representation

ProjectionImage
    exact homomorphic image in a quotient or finite field

ReconstructionState
    partial CRT/Hensel/rational-reconstruction information

Candidate
    proposed but unverified object

Witness
    data intended to discharge a proof obligation

Certificate
    independently checkable warrant for a typed claim

ReproducibilitySeal
    content identity and deterministic replay evidence
```

The existing Cella `certificate.py` functionality should become `ReproducibilitySeal`. It is retained, but it is not the new mathematical certificate layer.

---

## 6. Native object model

The common object found across the current work is:

```text
PresentedObject = {
    coefficient_domain,
    ambient_ring_or_field,
    equations_or_presentation,
    base_morphism,
    localization,
    normalization_state,
    grading,
    monomial_or_local_order,
    group_or_chart_action,
    assumptions,
    proof_scope,
    dependencies
}
```

### 6.1 Foundational specs

```text
DomainSpec
    ZZ | GF(p) | QQ | GF(p^k) | RationalFunctionField | AlgebraicExtension

RingSpec
    coefficient domain, ordered variables, relations, canonical encoding

GradingSpec
    grading group/matrix, variable degrees, homogeneity contract

OrderSpec
    global admissible monomial order and deterministic tie-break

LocalOrderSpec
    local/weighted order with a declared standard-basis algorithm

BudgetSpec
    time, memory, degree, terms, coefficient bits, pairs, primes, proof size
```

### 6.2 Algebraic presentations

```text
Polynomial
RationalFunction
Matrix
IdealPresentation
ModulePresentation
QuotientAlgebra
FiniteFieldExtension
LocalizedRing
SchemePresentation
OpenSubscheme
MorphismPresentation
CoverPresentation
FieldTower
```

### 6.3 Geometric and structural presentations

```text
Stratum
Divisor
ValuationPlace
BranchLocus
RamificationLocus
CoalescenceLocus
RankDropLocus
RealChamber
GroupAction
OrbitCarrier
KummerModule
InertiaDatum
Jet
LocalGerm
NewtonPolytope
MatrixPencil
```

### 6.4 Proof and execution objects

```text
ClaimSpec
ProofObligation
ProofDAG
RoutePlan
ScoutTrace
ReconstructionTrace
Witness
Certificate
Refusal
Provenance
ReproducibilitySeal
ArtifactManifest
```

All semantic objects are immutable, canonically serialized and content-addressed.

### 6.5 Certificate-family matrix

| Claim family | Minimum independent witness |
|---|---|
| Polynomial identity | Canonical exact zero difference or expression-DAG identity |
| Ideal membership/equality | Polynomial combination witnesses; both containments for equality |
| Gröbner basis | Origin/containment matrices, standard critical-pair representations, reducedness and order fingerprint |
| Elimination/projection | Certified elimination basis or structural norm/resultant map; explicit closure semantics |
| Localization | Saturation/elimination witness plus exact inverted element set |
| Hilbert/dimension/degree | Certified leading ideal and combinatorial Hilbert witness, or certified regular sequence |
| Prime/reduced/primary | Domain/radical/colon or decomposition witnesses at exactly the claimed level |
| Factorization | Product, multiplicity, coprimality and irreducibility witnesses |
| Finite field extension | Irreducible defining polynomial, quotient coordinates, degree and multiplication representation |
| Norm/trace/minimal polynomial | Multiplication matrix or resultant identity plus irreducibility/degree witness where claimed |
| Morphism/ramification | Finite presentation, relative differential/Jacobian/Fitting witness and declared étale open |
| Valuation | Height-one prime, local parameter/factor order, unit witness and prolongation law |
| Kummer rank | Exact parity matrix over `F_2`, valuation warrants, upper bound and relation witnesses |
| Wreath/monodromy | Base group, module rank, action/block data, generators and group-order witness |
| Specialization | Ring map, denominator and degree checks, fibre algebra, multiplicity/nilpotent accounting |
| Real root/selection | Rational isolation, exact signs/order, chamber and spectral/definiteness witness |
| Local germ/pole | Truncated expansion, certified remainder order, leading-unit nonvanishing, parity/Newton data |

---

## 7. The stratifying claim compiler

The claim compiler is Pathfinder's centre. It does not dispatch a command name directly to an algorithm.

```text
compile(context, query):
    normalize semantic object
    validate domain/order/grading/localization
    derive requested claim
    expand proof obligations
    detect structure and symmetries
    enumerate legal plans
    choose minimum expected certificate cost
    execute scouts
    reconstruct witnesses
    invoke independent checker
    split exceptional strata when necessary
    emit certified case tree or typed refusal
```

The optimization target is:

```text
minimize expected_total_cost(plan)

subject to:
    certificate_grade(plan) >= requested_grade
    every domain hypothesis is discharged or exposed
    every exceptional locus is retained
```

Cost includes:

```text
term count
max total and weighted degree
coefficient bit length
matrix dimensions and density
critical-pair count
modular-prime count
reconstruction modulus
certificate byte size
checker cost
predicted boundary branching
cache reuse
```

The existing residual-profile and cleanliness machinery can inform this planner, but its telemetry remains non-verdict-bearing.

---

## 8. Kernel architecture

```text
L0  Constitution and canonical IR
    outcome law, scopes, assumptions, budgets, serialization, provenance

L1  Exact domains
    ZZ, GF(p), QQ, exact matrices, CRT, reconstruction primitives

L2  Polynomial and module engine
    sparse/dense representations, orders, grading, division, labelled reductions

L3  Small independent proof kernel
    identities, membership, ideal equality, GB, factor and Hilbert checkers

L4  Claim compiler and structural recognizers
    substitutions, symmetry, regular sequences, towers, valuations, local forms

L5  Scout plane
    modular GB/F4/F5, specialization, numerical/spectral, external backends

L6  Reconstruction plane
    support alignment, CRT, rational reconstruction, Hensel, witness lifting

L7  Certified ideal and scheme services
    elimination, localization, Hilbert data, components, decomposition

L8  Finite algebra and real-algebra services
    factorization, resultants, fields, norms, traces, roots, matrix pencils

L9  Cover, group and valuation services
    normalization, ramification, Kummer modules, inertia, wreath/monodromy

L10 Domain clients
    Galois horizon, realization poset, DBP orbit, curvature germs, periods

L11 Public surfaces
    Python package, MCP adapter, CLI, artifact verifier
```

The proof kernel is deliberately smaller than the scout plane. It must be able to check artifacts produced by workers it does not trust.

---

## 9. Exact coefficient and polynomial substrate

### 9.1 Initial exact domains

The mandatory coefficient substrate is:

```text
ZZ
GF(p)
QQ
```

The full target adds:

```text
GF(p^k)
QQ(t_1,...,t_r)
finite separable extensions F[a]/(f)
finite quotient algebras
localized coefficient rings
```

Float is allowed only as a pre-scout estimator. No float coefficient may enter a candidate intended for exact certification.

### 9.2 Core exact operations

```text
gcd / extended gcd
content and primitive part
exact division
modular inverse
CRT with compatibility witness
rational reconstruction
square-free decomposition
dense and sparse exact matrices
Bareiss and modular determinants
rank, nullspace, Smith/Hermite normal forms
```

### 9.3 Polynomial representation

The engine requires:

```text
canonical exponent vectors
canonical coefficient normalization
sparse distributive representation
dense univariate specialization where profitable
global monomial orders
separate grading metadata
fast divisibility lookup
deterministic term and basis ordering
labelled reduction traces
```

Local orders and Laurent/Puiseux work are separate capabilities and must use standard-basis semantics rather than pretending a non-well-order is an ordinary Gröbner order.

---

## 10. Modular Pathfinder for Gröbner computation

### 10.1 Scout flow

For an ideal over `QQ`:

```text
1. Clear denominators and record the exact scaling map.
2. Primitive-normalize the integer generators.
3. Reject primes dividing denominators, contents or declared bad loci.
4. Run parallel GB scouts over GF(p).
5. Canonicalize each modular basis.
6. Cluster by leading-monomial ideal and basis support.
7. Learn useful pair/signature/reduction schedules.
8. Align compatible modular bases and labelled transformations.
9. Accumulate CRT images.
10. Rationally reconstruct G and its witnesses.
11. Submit the candidate to the exact checker.
12. On candidate failure, classify and retry; never emit it as truth.
```

Cross-prime agreement is reconnaissance, not certification.

### 10.2 Prime-event taxonomy

Internal prime events include:

```text
PRIME_DIVIDES_INPUT_DENOMINATOR
PRIME_COLLAPSES_LEADING_COEFFICIENT
PRIME_CHANGES_INPUT_DEGREE
PRIME_HITS_EXCLUDED_LOCUS
CHARACTERISTIC_SENSITIVE_IDENTITY
LEADING_IDEAL_OUTLIER
BASIS_SUPPORT_MISMATCH
```

Unlucky primes are discarded with evidence. They are not terminal user refusals.

### 10.3 Full Gröbner certificate

Let:

```text
F = (f_1,...,f_m)
G = (g_1,...,g_s)
I = <F>
J = <G>
```

The exact certificate must prove both containments:

```text
G = U*F       proves J subseteq I
F = V*G       proves I subseteq J
```

For every required critical pair it supplies a standard representation:

```text
S(g_i,g_j) = sum_k q_ijk*g_k

LM(q_ijk*g_k) < lcm(LM(g_i),LM(g_j))
```

The checker also verifies:

```text
G is monic
G is interreduced
the declared order is admissible
the order and ring fingerprints match the claim
```

Initially every pair may be checked. Later, a certified Buchberger/Gebauer-Moeller/F5 criterion can provide a smaller sufficient pair set.

### 10.4 Route record versus proof

```text
ScoutTrace:
    primes, modular bases, clusters, schedules, CRT history, timings

GroebnerCertificate:
    G, U, V, critical-pair witnesses, ring/order fingerprints
```

The proof remains valid if the scout backend is replaced.

---

## 11. Certified ideal and scheme services

### 11.1 Membership and equality

```text
f in <G>
```

is certified by:

```text
f = sum_i q_i*g_i
```

Ideal equality requires explicit witnesses in both directions.

### 11.2 Elimination and projection

`project_locus` returns the Zariski closure of a projection unless stronger image conditions are proved. The output type must say so.

The generic route is a certified elimination-order basis. Structural routes may use triangular substitution, norms or resultants.

### 11.3 Localization and saturation

The semantic object is an open restriction, not merely a modified generator list:

```text
OpenScheme(I; D(f))
```

The standard exact route is:

```text
I : f^infinity
    = (<I, 1-t*f> intersect R)
```

The result must retain `f != 0` in its scope.

### 11.4 Hilbert data

A certified GB supplies a leading monomial ideal. A combinatorial checker then validates:

```text
Hilbert function/series
Krull dimension
codimension
graded degree
standard monomials or standard pairs
```

For homogeneous complete intersections, a shorter regular-sequence certificate may replace generic Hilbert computation.

### 11.5 Components and decompositions

The result schema separates:

```text
minimal_supports
radical
reduced
prime
primary
embedded_components
multiplicities
```

General decomposition may use modular GTZ-style/equidimensional routes, factorization, ideal quotients and recursive splitting. The certifier must independently verify the claimed level:

```text
I = intersection_i Q_i
rad(Q_i) = P_i
P_i is prime
Q_i is P_i-primary
minimality/noncontainment
embedded-component accounting
```

If only minimal supports are proved, Pathfinder must not label the result a primary decomposition.

---

## 12. Structure-first routes extracted from the current corpus

The current realization-poset workflow is an unusually good demonstration of why Pathfinder should not imitate M2's search path.

### 12.1 Contact restrictions

On a signed contact component:

```text
C_eps = <
    u,
    w_i - eps_i*N_i,
    4M - sum_i eps_i*N_i
>
```

Define:

```text
s_eps = product_i eps_i

c_eps =
    eps_1*N_2*N_3*N_4 +
    eps_2*N_1*N_3*N_4 +
    eps_3*N_1*N_2*N_4 +
    eps_4*N_1*N_2*N_3
```

Then direct substitution gives:

```text
e3(w)|C_eps = s_eps*c_eps

delta|C_eps = -16*J^2
    when s_eps = +1

delta|C_eps = -4*(P+4*J^2)
    when s_eps = -1
```

Hence:

```text
IR + C_eps  = C_eps + <c_eps>
IZ + C_even = C_even + <J^2>
IZ + C_odd  = C_odd + <P+4J^2>
```

These are substitution certificates, not Gröbner-search problems.

### 12.2 Complete-intersection degree route

Once regularity is certified under the declared grading:

```text
deg(IX)                 = 2^4       = 16
deg(IR)                 = 16*3      = 48
deg(IZ)                 = 16*4      = 64
deg(IR+IZ)              = 16*3*4    = 192
deg(C_eps)              = 2
deg(C_eps+IZ)           = 2*4       = 8
deg(Sub_eps)            = 2*3       = 6
deg(IR+C_eps+IZ)        = 2*3*4     = 24
```

The certificate is a regular-sequence/height witness plus the declared weighted degrees. It avoids repeated generic Hilbert computations.

### 12.3 Kummer route to the prime difference ideal

After eliminating `M`, let `B` denote the normalized sheet domain. The rotating difference algebra has the form:

```text
IZ ~= B[J] / <J^2 - (gamma-4P)/16>
```

The identity:

```text
gamma*(gamma-4P) = 4*u*beta^2
```

gives:

```text
[gamma-4P] = [u]*[gamma]
```

in the square-class group. Once the independence of `[u]` and `[gamma]` and the domain status of `B` are certified, the quadratic is irreducible over `Frac(B)`. This supplies a direct domain/prime certificate for `IZ` and can replace the slow generic primary-decomposition search for this node.

This is the desired Pathfinder behavior:

```text
recognize field-tower structure
select Kummer proof
certify primeness directly
avoid irrelevant decomposition work
```

---

## 13. Finite algebra, field and factorization layer

### 13.1 Factorization

Factorization follows the same scout/certifier pattern, but needs its own certificate semantics.

```text
f = c * product_i f_i^e_i
```

Multiplication back certifies only a factor product. Complete factorization additionally requires:

```text
content and primitive-part normalization
square-free multiplicities
pairwise coprimality
irreducibility of each f_i over the declared field
```

The planner may use modular factor patterns, Hensel lifting and recombination as scouts. Irreducibility witnesses are separate.

### 13.2 Quotient fields and finite algebras

Required objects include:

```text
K = F[u]/<N(u)>
A = F[x_1,...,x_n]/I
Frac(B)
K(m) = K[m]/<m^2-u>
```

Native operations:

```text
normal form in quotient algebra
zero/equality/inverse tests
multiplication matrices
norm and trace
minimal polynomial
primitive-element test
separability
base change and compositum
```

### 13.3 Resultants and discriminants

Resultants may be computed through subresultants, Sylvester/Bézout determinants or modular reconstruction. Certificates must verify the defining determinant/remainder identity rather than merely trust a printed polynomial.

The discriminant of an eliminant is typed as a root-coalescence detector for that polynomial. It is not automatically the ramification divisor of a normalized incidence cover.

---

## 14. Normalization, morphism and cover layer

Pathfinder must preserve the distinction between:

```text
root collision of an eliminant
ramification of the incidence morphism
branch image downstairs
relation/rank-drop divisor
nonreduced special fibre
```

Native operations include:

```text
incidence_cover
factor_cover_through
normalize_or_record_normalization_state
relative_ramification
branch_image
compare_normalization_and_discriminant
specialize_cover
split_fibre
```

Relative ramification should be computed from the morphism—through relative differentials, Jacobian or Fitting ideals under certified hypotheses—not inferred solely from a discriminant.

A cover is output-role-relative. The same relation projected onto different outputs defines different covers and may have different degrees and groups.

---

## 15. Valuation, Kummer and group layer

### 15.1 Valuation objects

```text
ValuationPlace = {
    height_one_prime,
    local_parameter,
    valuation_rule,
    residue_characteristic,
    ramification_index,
    regularity_scope
}
```

Certificates include factor multiplicities or local expansions, unit/nonunit witnesses and prolongation rules.

### 15.2 Kummer modules

For radicands `a_1,...,a_r`, Pathfinder constructs:

```text
span_F2([a_1],...,[a_r]) subset K*/K*2
```

A valuation-parity matrix gives a certified lower bound on rank. Exact rank is promoted only when the lower bound meets the generator upper bound or explicit relations close the gap.

```text
KummerCertificate = {
    radicands,
    conjugate action,
    valuation places,
    parity matrix,
    exact F2 row reduction,
    relation witnesses,
    rank conclusion,
    excluded characteristics/strata
}
```

### 15.3 Wreath and monodromy objects

Native group data includes:

```text
permutation groups
finite modules
semidirect products
wreath products
block systems
colored cycle classes
inertia generators
```

A wreath certificate combines:

```text
base permutation-group certificate
conjugate character-module rank
faithful action
cover tower/block witness
group-order equality
```

Numerical continuation may scout branch cycles. It certifies monodromy only after every loop, lift and permutation assignment receives exact or interval-validated path-lifting evidence.

### 15.4 Structural group recognizers

The self-glue and cover work supplies theorem-directed recognizers that should run before a generic group computation. For a layer of the form:

```text
x^m + s*x^k - c
d = gcd(m,k)
```

the planner records the candidate geometric layer structure:

```text
C_d wreath S_(m/d)
```

subject to the exact separability, coprimality, base-field and branch hypotheses of the selected theorem. Pure powers and coprime trinomials appear as typed endpoint cases. The recognizer emits a proof obligation for every hypothesis; it does not promote a group merely from the exponent pattern.

Likewise, for a decorated cover:

```text
base monodromy G
+ conjugate radicand module W
+ valuation rows spanning W*
-> Kummer kernel and wreath lift
```

This permits one normalized sheet plus symmetry transport to replace explicit construction of every conjugate radical.

---

## 16. Exact real algebra and physical selection

Elimination over `QQ` returns complex Zariski closure data. Physical selection requires a separate exact real layer.

Required operations:

```text
Sturm/subresultant root counts
rational isolating intervals
Thom encodings/sign determination
real emptiness
ordered-field positivity
real component filtering
exact matrix definiteness
generalized-eigenvalue enclosure
```

The physical-root result should carry:

```text
defining polynomial or pencil
isolating interval
root index/order
chamber assumptions
definiteness witness
spectral witness when used
```

For the axial mass problem the target operation is:

```text
u_phys = lambda_max(S)^(-2)
```

with exact rational enclosure of the extremal generalized eigenvalue and a proof that this root is the first spectrahedral exit in the declared strict chamber.

---

## 17. Local germ, jet and curvature layer

The geometry corpus should remain a client of the algebra kernel, but its route logic belongs in Pathfinder.

Native local objects:

```text
exact finite jets
Laurent and truncated series
parity actions
leading units
divisor valuations
multivariate Newton polytopes
weighted approaches
local metric germs
```

Preferred routes:

```text
local metric germ + parity
    -> face pole order and leading coefficient

Newton vertices + nonzero coefficient certificates
    -> corner support function and balanced rays

role-jet orbit + gauge action
    -> invariant carrier and channel account
```

Global curvature expansion is a fallback, not a default.

---

## 18. Realization poset as a native artifact

The realization poset should not be a postprocessed table of M2 outputs. It should be a first-class proof object.

```text
RealizationNode = {
    stratum_id,
    defining_scheme,
    localization,
    support_components,
    scheme_multiplicities,
    codimension,
    typed_degree,
    real_status,
    incident_divisors,
    inertia_rows,
    certificates
}

RealizationEdge = {
    source,
    target,
    relation: inclusion | specialization | closure | normalization_preimage,
    witness
}
```

Construction is lazy and demand-driven. Intersections and saturations are computed once, content-addressed and reused. A combinatorial candidate node is distinguished from a realized, generically realized, nonreduced or unrealized node.

The semantic handoff to inertia is:

```text
certified realized stratum
+ collision partition
+ certified incident parity rows
-> local inertia group
```

---

## 19. Current M2 corpus parity map

The frozen parity fixture begins with the exact ring fingerprint:

```text
S = QQ[M,N1,N2,N3,N4,J,u,w1,w2,w3,w4]

weights:
    M,N1,N2,N3,N4,w1,w2,w3,w4 -> 1
    J,u                         -> 2

monomial_order = GRevLex

IX = <
    w1^2-u-N1^2,
    w2^2-u-N2^2,
    w3^2-u-N3^2,
    w4^2-u-N4^2,
    w1+w2+w3+w4-4M
>

IR = IX + <det(J_rel)>
IZ = IX + <delta>

D_generic =
    2*M*(N1*N2*N3*N4)*
    product_{a<b}(N_a^2-N_b^2)
```

Every reproduced value must point to this complete fingerprint or to an explicit specialization/base-change derived from it.

| Current stage | Pathfinder query | Preferred first route | Required proof |
|---|---|---|---|
| Incidence model/quintic | `project_locus(IX, sheet_vars)` | signed norm/tower recognition, then elimination if needed | norm or elimination certificate; principal generator; typed degree |
| Sixteen contact walls | `project_locus(C_eps)` | one substitution proof plus sign-orbit transport | ring-map and orbit witnesses |
| Difference ideal | `certify_prime(IZ)` | quadratic tower + Kummer square-class witness | base-domain + irreducible-quadratic certificate |
| Generic node table | `realization_poset(...)` | substitutions and complete-intersection route | localization, regular-sequence, Hilbert and incidence witnesses |
| Slice projections | `specialize_then_project` | exact map, reuse cached generic DAG | specialization and elimination certificates |
| Minimal supports | `classify_components` | symmetry/structured splitting, then modular decomposition | prime/support completeness witnesses |
| Collision analysis | `compare_ramification_and_discriminant` | normalized morphism plus resultant/factor route | Fitting/Jacobian, resultant and exact quotient witnesses |
| Real nodes | `real_locus_status` | elementary positivity/Sturm | ordered-field certificate |
| Multiplicity-two nodes | `scheme_multiplicity` | direct restriction to `<J^2>` | ideal equality, radical and local-length witness |

---

## 20. Corrections exposed by the parity audit

Pathfinder's acceptance corpus must correct rather than reproduce the following bookkeeping defects.

### 20.1 Saturated versus unsaturated invariants

The current stage-4 code computes codimension and degree before saturation, then tests only saturated properness. Results phrased as generic-open invariants must instead use:

```text
codim(I : D^infinity)
degree(I : D^infinity)
```

or carry a certificate that saturation preserves the relevant top-dimensional structure.

### 20.2 Misstated slice degree

The printed `deltaSliceA` eliminant has:

```text
generic physical weighted degree = 20
degree in (M,J) after fixed charges = 12
degree in (X=M^2,Y=J^2) = 6
```

It is not degree 24 under the declared conventions. Typed degree metadata must make such ambiguity impossible.

### 20.3 Exact wall exclusion

For the even slice polynomial:

```text
f(1)  = 690259302656
f(3)  = -6274195341056
f(5)  = -102565662125824
f(7)  = -1021662878922496
f(9)  = 22425097021696
f(11) = 2157043244612546816
```

Evenness handles the negative walls. Pathfinder should emit these exact remainders or a gcd/Bézout witness, not call the check numerical.

### 20.4 Support versus scheme claims

One minimal prime proves one minimal support. It does not by itself prove reducedness, absence of embedded components or a primary decomposition. These receive separate fields and guarantees.

### 20.5 Degree-drop typing

The equal-charge collision eliminant is quartic in `u`, not quintic. The special fibre must carry an explicit degree-drop event rather than inherit the generic label.

### 20.6 Generic-open fingerprint

Every run must hash the exact inverted factors and assumptions. Similar prose descriptions of a generic open are insufficient.

### 20.7 Incomplete current deliverables

The parity program must include outputs requested by the workflow but not fully executed in the present run:

```text
full symbolic base images of surviving codimension-two strata
minimal supports for Ceven+IZ and Codd+IZ
minimal supports and scheme status for both codimension-three nodes
full symbolic generic mass-branch projection
complete component/containment Hasse computation
explicit dimension/codimension proof for ramDeltaSlice
```

### 20.8 Execution-shape baseline

The current package executes approximately:

```text
24 elimination calls
38 saturation calls
5 minimal-prime calls
1 primary-decomposition call
1 discriminant call
```

Twenty-four saturation calls are repeated eager work caused by reloading three derived objects in eight isolated stages. Pathfinder's lazy proof DAG should eliminate this repetition before lower-level algorithm optimization is attempted.

---

## 21. Content-addressed proof DAG and execution economy

The current staged corpus repeats the same model loads and many saturations. Pathfinder should make repeated work structurally impossible.

Every node key includes:

```text
ring fingerprint
coefficient domain
variable order
grading
monomial/local order
canonical generators
localization
specialization map
algorithm version
checker version
assumption set
```

Cached objects include:

```text
modular bases
leading ideals
CRT states
exact candidate bases
transformation matrices
saturations
eliminations
Hilbert data
factorizations
field multiplication matrices
valuation rows
verified certificates
```

The runtime is lazy. It computes only nodes demanded by a claim. Shared prerequisites are evaluated once and reused across Python, MCP and CLI requests.

Scout work is parallel. Proof checking remains deterministic. Large witnesses live in immutable artifacts referenced by content hash.

---

## 22. Refusal and retry calculus

### 22.1 Internal retryable events

```text
SCOUT_NO_CONSENSUS
CRT_MODULUS_INSUFFICIENT
RATIONAL_RECONSTRUCTION_AMBIGUOUS
CANDIDATE_SUPPORT_MISMATCH
CANDIDATE_CONTAINMENT_FAILED
CANDIDATE_BUCHBERGER_FAILED
HENSEL_LIFT_INCOMPLETE
```

These normally trigger replanning or a wider scout budget.

### 22.2 Terminal scope/budget refusals

```text
UNSUPPORTED_COEFFICIENT_DOMAIN
NON_ADMISSIBLE_MONOMIAL_ORDER
LOCAL_ORDER_REQUIRES_STANDARD_BASIS
UNSUPPORTED_WILD_CHARACTERISTIC
NONSEPARABLE_EXTENSION_UNSUPPORTED
NORMALIZATION_REQUIRED
DEGREE_BUDGET_EXCEEDED
COEFFICIENT_BUDGET_EXCEEDED
MEMORY_BUDGET_EXCEEDED
CERTIFICATE_BUDGET_EXCEEDED
BOUNDARY_STRATIFICATION_BUDGET_EXCEEDED
```

### 22.3 Mathematical nonexistence decisions

These are certified answers, not failures:

```text
IDEAL_IS_UNIT
REAL_LOCUS_EMPTY
ELEMENT_NOT_IN_IDEAL
RADICAND_DEPENDENT
NO_PRIMITIVE_ELEMENT_OF_REQUESTED_FORM
PROPOSED_COMPONENT_NOT_PRESENT
```

### 22.4 Engine defects

```text
INTERNAL_INVARIANT_VIOLATION
CHECKER_DISAGREEMENT
NONDETERMINISTIC_CANONICALIZATION
CERTIFICATE_REPLAY_MISMATCH
```

Defects must never be rebranded as mathematical refusals.

---

## 23. Public result and certificate envelope

```text
{
  "schema_version": "...",
  "outcome": "certified | scouted | refused",
  "claim": {...},
  "scope": {
    "ambient": {...},
    "open_set": {...},
    "assumptions": [...],
    "exceptional_strata": [...]
  },
  "value": {...},
  "account": {...},
  "certificate": {...},
  "route": {...},
  "procedure_verdict": {...},
  "answer_verdict": {...},
  "provenance": {...},
  "reproducibility_seal": {...},
  "refusal": null | {...},
  "artifacts": [...]
}
```

`route`, `provenance` and `reproducibility_seal` do not substitute for `certificate`.

---

## 24. Python, MCP and runtime design

### 24.1 One semantic engine

Python, MCP and CLI call the same kernel. The MCP layer validates, routes and serializes; it contains no mathematical algorithms.

### 24.2 Recommended implementation split

```text
High-performance kernel:
    Rust core with exact-domain/backend interfaces
    GMP/FLINT-class low-level arithmetic allowed as workers

Independent verification:
    small checker crate
    plus a minimal pure-Python reference verifier for portable replay

Public API:
    Python bindings
    MCP stdio/server adapter
    CLI for artifact verification and long jobs
```

The semantics and certificate format must not depend on a particular low-level backend.

### 24.3 Public query surface

The MCP surface should remain small:

```text
cella.solve(query_spec)
cella.verify(certificate_or_manifest)
cella.resume(reconstruction_state, additional_budget)
cella.explain(result)
cella.capabilities()
```

Python may expose typed convenience methods around the same `QuerySpec`.

### 24.4 Exact serialization

```text
QQ element       -> signed numerator + positive denominator
GF(p) element    -> canonical residue + modulus
monomial         -> exponent vector tied to RingSpec
polynomial       -> sorted term list
order            -> full typed order definition
degree           -> DegreeValue with grading fingerprint
large proof      -> content-addressed immutable artifact
```

No JSON float is accepted as an exact coefficient.

---

## 25. Module map

```text
cella/
  core/
    outcome
    scope
    assumptions
    provenance
    serialization
    artifact
    budget

  exact/
    zz
    fp
    qq
    matrix
    crt
    reconstruction

  poly/
    monomial
    grading
    order
    polynomial
    division
    module

  proof/
    identity
    membership
    groebner
    hilbert
    factor
    field
    decomposition
    real
    verifier

  planner/
    claim_ir
    obligations
    cost
    structure_recognizers
    strategy
    stratifier

  scout/
    modular_gb
    specialization
    factor
    numeric
    external_adapter

  reconstruct/
    basis
    transformation
    hensel
    witness

  ideal/
    ideal
    elimination
    localization
    hilbert
    components
    decomposition

  algebra/
    quotient
    finite_extension
    resultant
    norm_trace
    minpoly

  real/
    sturm
    isolation
    sign
    pencil

  cover/
    morphism
    normalization
    ramification
    branch
    specialization
    realization_poset

  group/
    permutation
    module
    kummer
    inertia
    wreath
    monodromy

  local/
    valuation
    series
    newton
    germ

  geometry/
    jets
    role_orbit
    carrier
    curvature

  api/
    python
    mcp
    cli
```

Current Cella geometry, period and benchmark modules become clients or are adapted behind these interfaces. Legacy V4 eval campaigns remain regression suites, not dependencies of the proof kernel.

---

## 26. Build program without scope reduction

The phases below order construction; they do not narrow the canonical target.

### Phase A — Constitutional kernel and verifier

Build canonical `DomainSpec`, `RingSpec`, `GradingSpec`, `OrderSpec`, `ClaimSpec`, outcome law, artifact format and exact checker. Accept M2 output initially as an untrusted candidate source. This immediately tests the scout/certifier boundary against the existing corpus.

### Phase B — Exact polynomial and structural core

Build `ZZ/GF(p)/QQ`, exact matrices, sparse polynomials, labelled division, substitution, ring maps, symmetry transport, regular-sequence and complete-intersection certificates.

### Phase C — Native modular Gröbner Pathfinder

Build prime scheduling, modular GB workers, leading-ideal clustering, CRT/rational reconstruction, transformation-matrix lifting and exact Gröbner certificates.

### Phase D — Certified ideal/scheme parity

Build elimination, localization, intersection, Hilbert data, typed degree, nonemptiness, support/component classification and realization-poset artifacts. Retire the bulk of current M2 stages here.

### Phase E — Factor, finite algebra and exact real layer

Build factorization, resultants, discriminants, quotient fields, minimal polynomials, norms/traces, root isolation and matrix-pencil selection.

### Phase F — Decomposition completion

Build radical, minimal-prime and primary-decomposition planners with independent proof schemas, including embedded-component and multiplicity accounting.

### Phase G — Cover/Kummer/wreath integration

Build normalization-aware morphisms, ramification, specialization, valuations, Kummer modules, inertia, wreath and monodromy certificates. Replace expensive generic searches with the recent structural theorems wherever their hypotheses certify.

### Phase H — Local geometry and full corpus lift

Port the active role-jet, carrier, curvature-germ, Newton-corner, period and root-selection clients onto the new kernel and run the complete hostile regression program.

---

## 27. Acceptance gates

### 27.1 Mathematical gates

Pathfinder must:

```text
certify both ideal containments for every reconstructed GB
certify every claimed critical-pair closure
distinguish grading from monomial order
distinguish support from scheme structure
distinguish complex projection closure from real image
bind every generic result to its exact localization
bind every specialization to a parameter map and degree behavior
emit exact certificates or refuse
```

### 27.2 M2 corpus parity gates

It must reproduce and certify:

```text
codim IX = 5
dim(S/IX) = 6
det(J_rel) = 8*e3(w)
IR = IX + <e3>

the principal mass eliminant:
    degree in u = 5
    declared graded degree = 16
    leading coefficient = -2^24*M^6
    J absent

all 16 contact projections
the prime/reduced IZ result over QQ
the eleven-node generic-open table on the correct saturated objects
slice-A projections, factors, exact wall exclusions and real statuses
the equal-charge degree drop and discriminant/ramification comparison
the multiplicity-two even-contact node
```

### 27.3 Epistemic gates

```text
scout code cannot construct CERTIFIED outcomes
checker runs without scout backend
M2/Singular/SymPy/FLINT candidates are treated identically
route and answer verdicts remain separate
reproducibility seals never upgrade certificate grade
slice evidence never promotes a generic theorem
```

### 27.4 Adversarial gates

```text
bad-prime mutations
leading-ideal collision mutations
wrong monomial-order mutations
missing-containment-witness mutations
factor-product-with-reducible-factor mutations
support-versus-primary mutations
unsaturated-versus-saturated invariant mutations
degree/grading mutations
generic-to-special-fibre promotion mutations
real-versus-complex image mutations
characteristic-2/wild-inertia mutations
cache-key and stale-proof mutations
```

### 27.5 Runtime gates

```text
byte-stable canonical outputs
content-pinned inputs and checker
deterministic verification
resume from retained CRT/Hensel state
lazy content-addressed DAG reuse
time/memory/pair/term/coefficient/proof telemetry
large-artifact streaming by manifest
```

---

## 28. Explicit engineering and research obligations

These gaps remain part of the architecture; they are not reasons to shrink it.

```text
efficient labelled modular F4/F5 witness reconstruction
proof compression for large critical-pair families
complete irreducibility certificates when no simple modular witness exists
positive-dimensional prime and primary certificates
normalization algorithms and certificates
general height-one valuation construction
square-class relation solving when valuation rank is inconclusive
wild/residue-characteristic-two inertia
non-normal-crossing local models
nonseparable and noncoprime cover towers
certified numerical path lifting for monodromy
Puiseux and local standard-basis verification
codimension-three-and-higher curvature fronts
certified generalized-eigenvalue implementation
formal-proof export if later required
```

Every such obligation receives a typed capability status and refusal route. None is silently delegated to an opaque backend verdict.

---

## 29. What is lifted, generalized, retired and quarantined

### Lift at the constitutional level

```text
typed refusal
exact canonical serialization
separate probe/referee lanes
procedure-answer orthogonality
content pins and provenance
byte-stable replay
performance telemetry as non-verdict evidence
frozen fixtures and mutation controls
MCP as transport only
```

### Generalize

```text
Cell                -> typed reduction accounts + epistemic outcomes
certificate.py      -> ReproducibilitySeal + mathematical certificates
symbolic.py         -> domain-generic polynomial/ideal substrate
proofs.py           -> small independent proof kernel
qsqrt.py            -> arbitrary finite algebraic extensions
pathfinder.py       -> claim compiler, stratifier and route planner
cleanliness burden  -> algebraic cost and proof-burden model
geometry strata     -> universal scope/open/boundary semantics
```

### Retire from the base kernel

```text
legacy TypedResult as universal carrier
projection-specific refinery/solver as foundational dependencies
floating fits as proof
digest equality as mathematical certification
implicit backend monomial-order semantics
silent approximate fallback
global expansion as default geometry route
```

### Quarantine as optional scouts or clients

```text
M2, Singular, FLINT, SymPy, mpmath
external PSLQ/period harnesses
legacy eval campaigns
specialized DBP/Galois scripts
numerical monodromy trackers
```

They remain useful. They simply do not sit in the trust root.

---

## 30. Canonical statement

The strongest coherent design is:

```text
Cella Pathfinder is a claim-first mathematical runtime.

It preserves algebraic presentations, morphisms, towers,
localizations, symmetry and strata; discovers candidate routes over
cheap representations; reconstructs only the required objects and
witnesses; verifies each claim in a small exact checker; and returns
either a proof-carrying result, an explicitly scouted candidate, or a
typed refusal with the unresolved algebraic leaf retained.

Its Gröbner engine is modular and certificate-producing.
Its scheme engine is support/multiplicity aware.
Its cover engine is normalization and specialization aware.
Its field engine is valuation and Kummer aware.
Its geometry engine is local-germ and orbit aware.

Macaulay2 parity is the first corpus gate, not the architectural ceiling.
```

---

## 31. Source basis for this synthesis

This architecture was pulled from the following current surfaces and their stated evidence boundaries:

```text
Current implementation inventories:
    README.md
    README_lloyd_v4.md
    README_V4_Evals.md
    README(1).md

Cella/V4 capability and audit records:
    CELLA_V4_TECHNICAL_CAPABILITY_SPECIFICATION.md
    HISTORICAL_RECORD.md
    Cella_Project_Synthesis.md
    AUDIT_UPDATE_2026-06-26.md

Current geometry and orbit mathematics:
    DBP_Curvature_Role_Reduction.md
    Canonical_Invariant_Reduction_Theorem.md
    Theorem_8_1_New_Math_Extension.md
    Theorem_8_1_Curvature_Orbit_Correction.md
    Gauge_Channel_Transport_Law.md
    Three_Channel_KG_Strong_Spec.md
    Three_Channel_KG_New_Math_Extension.md
    lead7_kn_n3_dbp_metric.tex
    pfc_normal_forms.tex
    self_glue_monodromy.txt
    dbp_orbit_calculus.tex

Recent Galois/Kummer/cover corpus:
    GALOIS_K_ELLIPSE_RESEARCH_MAP_v1_6.md
    DEGREE_20_CROWN_CERTIFICATE_REPORT_2026-07-10.md
    KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md
    R9_STATIC_CLOSURE_OPENING_DERIVATION_2026-07-10.md
    ROTATING_KUMMER_RANK_JUMP_LEMMA_REPORT_2026-07-10.md
    ROTATING_THREE_CHANNEL_WREATH_CLOSURE_2026-07-10.md
    WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md

M2 corpus and run interpretation:
    MACAULAY2_REALIZATION_POSET_WORKFLOW_2026-07-10.md
    REALIZATION_POSET_RUN_REPORT_2026-07-10.md
    staged .m2 scripts and raw outputs described by README(1).md
```

The architecture distinguishes theorem text, executable calculation, raw output, finite specialization evidence, generic claim and proposed engine capability. Their inclusion here does not flatten those evidence grades.
