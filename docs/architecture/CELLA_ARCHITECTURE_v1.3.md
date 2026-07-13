# Cella Architecture

**Version:** 1.3  
**Date:** 2026-07-11  
**Status:** Canonical eventual-engine architecture with explicit module boundaries; not an as-built capability claim  
**Supersedes:** Cella Pathfinder Kernel Architecture v1.2r1  
**First module:** `cella.pathfinder`, specified independently in `CELLA_PATHFINDER_MODULE_SPEC_v1.0.md`  
**Target:** Build Cella as a modular, native, proof-carrying mathematical system while preserving the full intended scope: fast certified route discovery, exact ideal and scheme operations, algebraic extensions, real selection, Galois/Kummer/wreath reasoning, realization strata, and local geometry.

This document is self-contained. It preserves the entire eventual-engine design developed through v1.2r1 while separating its implementation modules. The standalone Pathfinder module is built first; the larger mathematical modules remain architectural targets and must not be fused into Pathfinder prematurely.

---

## 1. Executive decision

Cella should not be designed as a clone of Macaulay2, a Gröbner-basis command wrapped in result types, or an accumulation of specialist mathematical scripts.

The eventual system is:

```text
Cella =
    a modular proof-carrying mathematical engine
    whose first independent module is Pathfinder.
```

Pathfinder contributes the governing inversion:

```text
Finding a candidate is expensive.
Checking the right candidate is usually cheaper.

Therefore:
    find over cheap representations,
    preserve the discovered route,
    certify only the required claim exactly.
```

Pathfinder is the fast route kernel, not the eventual mathematical engine. It owns task normalization, route discovery, native modular scouting, reconstruction, certificate construction and canonical replay. It does not initially own realization posets, normalization theory, Kummer/wreath mathematics, exact real geometry or domain-specific clients.

The later Cella mathematical modules own scoped algebraic presentations, morphisms, covers, localizations, strata, field towers, group actions, accounts and domain claims. They consume Pathfinder through its public task API; Pathfinder never depends upward on them.

Structured routes may certify a claim without general closure search. The complete eventual engine still requires native ideal closure and all other mathematical operations enumerated in this document.

The eventual Cella public surface remains query-first:

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

The eventual mathematical engine compiles these high-level queries into claims and lower-level Pathfinder tasks. Pathfinder selects and certifies computational routes; the consuming mathematical module interprets the result in its own ontology.

The principal design consequence is:

```text
Pathfinder finds and certifies the cheapest sufficient route.
The larger Cella modules own the mathematical meaning of that route.
```

### 1.1 Normative module boundary

<pre style="color:#d1242f">EXTERNAL GAP — optional proposal source
        |
        v
separate wrapper package
        |
        v
CandidateSource protocol
</pre>

```text
CandidateSource protocol
        |
        v
cella.pathfinder                         first build
        |
        v
certified route result
        |
        v
cella.math.*                             future modules
```

Dependency direction is permanent:

```text
wrapper -> pathfinder
future mathematical module -> pathfinder

pathfinder -/-> wrapper implementation
pathfinder -/-> future mathematical module
```

Wrappers are candidate-ingress adapters, never Pathfinder core dependencies. An external source may propose a candidate but cannot construct a Cella certificate or public certified outcome. Pathfinder remains complete and testable with no wrapper installed.

<span style="color:#d1242f"><strong>EXTERNAL GAP — first wrapper fixture:</strong> the first integration test targets Macaulay2. It exercises only candidate ingress for an already admitted Pathfinder route. Native closure replaces its basis proposal; Macaulay2 is neither a build dependency nor a proof authority.</span>

### 1.2 Eventual Cella modules

| Module | Responsibility | Build relation |
|---|---|---|
| `cella.pathfinder` | Fast native route discovery, reconstruction, proof construction and replay | First independent module |
| `cella.ideals` | Ideal/scheme claims: elimination, localization, Hilbert data, radicals and decomposition | Future consumer of Pathfinder |
| `cella.algebra` | Factorization, quotient algebras, extensions, resultants, norms, traces and minimal polynomials | Future consumer |
| `cella.real` | Exact real roots, signs, chambers, emptiness and matrix selection | Future consumer |
| `cella.covers` | Morphisms, normalization, specialization, ramification, branch and realization posets | Future consumer |
| `cella.groups` | Valuations, Kummer modules, inertia, permutation and wreath structures | Future consumer |
| `cella.local` | Jets, Laurent/Newton data, germs, pole laws and local classifiers | Future consumer |
| `cella.geometry` | Role orbits, carriers, curvature and application-specific geometry | Future client layer |
| `cella.api` | Unified Python, MCP and CLI surfaces over the assembled modules | Final composition layer |

Each future module owns its mathematical claims and compiles its computational obligations into Pathfinder tasks. This document specifies their eventual composition without making them part of the first Pathfinder binary or package.

**Terminology rule:** the module-ownership table is normative. High-level mathematical services are never shorthand for Pathfinder ownership. The owning future Cella module defines and interprets each high-level claim, lowers it to normalized Pathfinder `TaskSpec` obligations, and assembles the returned certified routes. Only route-task normalization, route discovery, reconstruction, proof construction/replay and their native algebraic substrate belong to `cella.pathfinder` itself.

### 1.3 External dependency notation

External integrations are retained in this eventual architecture but are visually marked in red. Every red entry names the native gap that must be closed before the external source can be removed from that route.

<span style="color:#d1242f"><strong>EXTERNAL GAP</strong></span> means:

```text
the component is outside the Cella core;
it may be connected only through a wrapper;
it cannot certify or construct public outcomes;
its named mathematical capability remains native Cella build work.
```

Historical M2 corpus references are migration provenance, not runtime dependencies, and therefore are not colored red unless they describe an executable integration.

---

## 2. Register discipline

Four registers must remain distinct throughout implementation and documentation.

| Register | Meaning | Current status |
|---|---|---|
| **Legacy V4** | Typed/stratified numerical-geometry engine, its eval campaigns, protocols, observers, refinery, solver and history machinery | Partly reusable; not the new kernel |
| **Current Cella** | Exact-account arithmetic, restricted symbolic rational functions, exact geometry clients, constructive elementary annex, route planner, refusals, reproducibility records and MCP adapter | As described by the current package inventory; no general ideal or Gröbner engine |
| **Cella Pathfinder module** | Standalone fast-route kernel: native scout, reconstruction, proof construction/replay and wrapper protocol | First module; separately specified |
| **Eventual Cella engine** | The complete modular architecture retained here: ideals, finite algebra, real algebra, covers, groups, local geometry and unified APIs | Proposed composition; built after Pathfinder |

No Cella capability is to be described as implemented merely because a corresponding theorem, Python research script, M2 output, wrapper result or current Cella helper exists.

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
| `proofs.py` | Lift narrow proof rules into the canonical replay semantics | First source of identity, Sturm, positivity, valuation and Newton proof nodes |
| `qsqrt.py` | Generalize | Finite algebraic extension and quotient-field layer |
| `pathfinder.py` | Preserve route-planning intent; replace execution model | Route-task normalizer, structural recognizers and cost planner; high-level claim compilation stays with owning modules |
| `cleanliness.py`, `residual_profile.py`, slope/observer modules | Quarantine to scout telemetry | Cost, conditioning and candidate-route estimates only |
| `carrier.py`, `tower.py`, `sensors.py`, `campaign.py` | Preserve as clients | Geometry regression corpus and theorem-directed routes |
| `periods.py`, `reference_lift.py` | Preserve as domain libraries | Formal period, role-orbit and wreath consumers of the new kernel |
| `mcp_server.py` | Lift the adapter discipline | Validation and transport around one semantic engine |
| V4 core protocols/provenance/history | Mine contracts, not universal types | Capability binding, trace identity, handled-state and replay patterns |
| V4 refinery/solver | Do not promote as foundation | Archived client experiments unless re-derived for a Pathfinder consumer |
| V4 eval campaigns | Preserve intact as adversarial corpus | Adversarial reference and mutation batteries; no seal authority |

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

M2 parity therefore means matching the requested mathematical outputs. Eventual Cella parity means matching those outputs while also supplying independently replayable warrants and correcting places where the current workflow only records an M2 attestation. Pathfinder supplies the certified route substrate; the owning mathematical modules supply the high-level claim semantics.

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

Native scouts may use finite fields, specializations, floating estimates, interval numerics, heuristics and parallel exploration. Separately installed wrappers may also submit candidates through the `CandidateSource` protocol. Scouts and wrappers may emit candidates and routes; they may never emit mathematical truth.

<span style="color:#d1242f"><strong>EXTERNAL GAP — wrapped candidate sources:</strong> an external engine may temporarily propose a candidate only through a separate wrapper package. The replacement gap is the corresponding native scout/search routine; wrapper availability never defines Pathfinder capability.</span>

```text
Route state      = CANDIDATE_RETAINED(candidate, route, stability, unresolved_obligations)
Replay verdict   = CERTIFIED(claim, value, verdict_certificate)
Module outcome   = CERTIFIED_RELATIVE(claim, value, certificate, assumptions)
                 | REFUSED_SCOPE(reason, salvage_manifest)
                 | REFUSED_BUDGET(reason, retained_route_state)
                 | DEFECT(invariant_violation)
```

Pathfinder v1 exposes only the exact `CERTIFIED` mathematical verdict. Retained routes are operational state, while relative claims and scope decisions belong to the owning future mathematical module.

### Law 3 — Structure precedes general search

Before selecting general closure or decomposition search, the owning Cella module's claim compiler checks for structure. Pathfinder contributes only the route-level recognizers applicable to its admitted task:

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

This is the principal route by which assembled Cella can outperform a one-to-one M2 replacement on the user's corpus.

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

Saturation must not silently erase the phenomenon under investigation. When a route proves a result on an open set, the owning Cella module creates exact boundary problems.

```text
Query
├── D(h): certified generic result
├── V(h_1): boundary case
├── V(h_2): rank-drop case
├── V(h_1,h_2): intersection case
└── unresolved leaf: exact ideal + typed status
```

This certified case tree is the owning mathematical module's natural output; its leaves may contain certified Pathfinder route results.

### Law 6 — Preserve presentations, towers and morphisms

Do not flatten an incidence cover, field tower or local germ into one large eliminant unless the requested claim demands it. Intermediate sheets, blocks and morphisms often contain the cheapest proof.

### Law 7 — Proof and provenance are orthogonal

```text
route history       != mathematical proof
double-run digest   != mathematical proof
M2 transcript       != mathematical proof
modular agreement   != mathematical proof
```

Cella records both:

```text
procedure_verdict
answer_verdict
```

A candidate discovered by an untrusted engine can still receive an exact answer verdict. A byte-stable computation can still lack a mathematical warrant.

### Law 8 — Support, scheme and real locus are distinct

The assembled engine never silently identifies:

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

For pole orders, branch behavior and curvature cliffs, Modules L/D first ask whether a finite local germ, valuation, Newton polytope or normal-form theorem settles the claim. They do not expand a global scalar merely because a generic CAS would; they lower only the required exact route obligations to Pathfinder.

### Law 11 — Candidate sources are outside the trust root

Native Pathfinder scouts and separately wrapped sources may propose. Only canonical Pathfinder replay may seal a certificate. A wrapper is a boundary adapter, not a backend embedded in the core.

<span style="color:#d1242f"><strong>EXTERNAL GAP — Macaulay2/Singular:</strong> retained only as optional candidate sources for admitted Pathfinder route tasks. The v1 replacement gap is native closure. Elimination, saturation, Hilbert, radical and decomposition remain native Module I work and are not borrowed through the Pathfinder wrapper.</span>

<span style="color:#d1242f"><strong>EXTERNAL GAP — FLINT/GMP:</strong> retained in the eventual architecture record as possible historical low-level accelerators, but excluded from the native Pathfinder core. Replacement requires Cella-owned arbitrary-precision integers, rationals, prime fields, matrices, CRT, reconstruction and factorization primitives.</span>

<span style="color:#d1242f"><strong>EXTERNAL GAP — symbolic proposal sources:</strong> a suitable symbolic program may be connected only through a separate `CandidateSource` wrapper. Replacement requires the corresponding native symbolic search route; its artifact never enters certificate semantics.</span>

<span style="color:#d1242f"><strong>EXTERNAL GAP — mpmath/numerical trackers:</strong> research observation sources only, not `CandidateSource` proof authorities. Replacement requires native exact-real, interval or certified path-lifting operations.</span>

### Law 12 — Refusal is total and typed

For every admitted query under a declared version and budget:

```text
Verdict = CERTIFIED | CERTIFIED_RELATIVE | none

ExecutionDisposition = SEALED
                     | ROUTE_RETAINED
                     | REFUSED_SCOPE
                     | REFUSED_BUDGET
                     | DEFECT
```

No hidden numerical downgrade, guessed scalar, uncaught exceptional stratum or internal execution exception may cross the public boundary.

### Law 13 — One semantic IR, certified internal lowering

Every claim, fixture and expression has one canonical semantic IR. A native worker may use a private optimized representation only through a hash-bound, typed lowering and decoding chain whose proof nodes are handled by canonical replay:

```text
CanonicalIR --certified lowering--> NativeExecutionIR
NativeExecutionIR --execution-->    NativeExecutionResult
NativeExecutionResult --decoding--> Candidate
```

Native execution representations declare their exact relation to the semantics:

| Representation | Interpretation | Verdict role |
|---|---|---|
| `GF(p)` | Homomorphic image, at an admissible prime | Scout and sound-rejection prescreen |
| Interval | Enclosure | Certified containment only |
| Float | Lossy observation | Scout only |
| Jet/tower | Exact quotient or algebra extension, as typed | Claim-specific |
| Exact `QQ`/`ZZ` | Identity on the declared domain | Certifying semantics |

A native worker may not re-derive meaning from an independent parser or implicit convention. External wrappers terminate at `CandidateArtifact` and never participate in this lowering chain.

### Law 14 — Identification requires isomorphism; transport is claim-specific

Merging two objects or substituting one for the other everywhere requires an explicit isomorphism certificate, including equivariance where a group acts and an inverse or canonical-form equality. Structural resemblance is `COMPARISON_ONLY`.

A particular claim may transport along a weaker certified morphism only when that morphism satisfies the claim's declared `transport_variance`. Transport does not imply identification.

### Law 15 — Observation families require adequacy

Every verdict-bearing observation family carries a claim-specific adequacy theorem. Derived channels—jets, parities, valuations, projections and shadows—may decide a claim only when their adequacy for that claim is certified. Otherwise an object-level channel is required.

Canonical boundaries are:

```text
derivatives alone are inadequate for homogeneity because they miss constants
valuation-parity rank is a lower bound until it meets an upper bound or relations close the gap
quadratic jets determine exact inertia but not classifications along null directions
```

### Law 16 — Refusals preserve discharged work

Every refusal of a composite claim contains a salvage manifest enumerating each discharged sub-obligation, its certificate, scope and warrant vector. A composite refusal without a salvage manifest is malformed.

### Law 17 — Negative claims are first-class

Nonmembership, real emptiness, scope emptiness and absence of a proposed component require typed positive witnesses for the negative conclusion. Failure to find a positive witness is never a negative certificate.

### Law 18 — Termination is proved per routine

Every recursive or iterative kernel routine supplies either:

```text
1. a routine-specific well-founded descent measure; or
2. a monotonically consumed resource budget.
```

A global meter covers every search loop, including general Gröbner search, factorization, radical membership, CAD, interpolation search and certificate discovery. Refusal taxonomy gives halts meaning; it does not prove that they occur.

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
    replay_rule
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

Every mathematical certificate carries the following orthogonal warrant vector:

```text
proof_grade:
    SELF_CONTAINED | THEOREM_REDUCTION | RELATIVE_CERTIFICATE

dependency_state:
    INLINE_VERIFIED | PINNED_VERIFIED | PINNED_UNVERIFIED

relation_grade:
    IDENTITY | ISOMORPHISM | INTERTWINER | COMPARISON_ONLY

scope:
    assumptions, family, localization, characteristic, semantics
```

`COMPARISON_ONLY` is inadmissible in a proof DAG. `PINNED_UNVERIFIED` forces the public state `CERTIFIED_RELATIVE`, and every unverified dependency must also appear explicitly in `scope.assumptions`. An unverified dependency may never be concealed inside `CERTIFIED`.

Warrant composition retains the complete proof DAG and derives summary fields by explicit rules:

```text
proof_grade:
    SELF_CONTAINED o SELF_CONTAINED             -> SELF_CONTAINED
    any edge using a verified theorem           -> THEOREM_REDUCTION
    any edge using a pinned unverified claim    -> RELATIVE_CERTIFICATE

relation_grade:
    IDENTITY o r                                 -> r
    ISOMORPHISM o ISOMORPHISM                    -> ISOMORPHISM
    ISOMORPHISM o INTERTWINER                    -> INTERTWINER
    INTERTWINER o INTERTWINER                    -> INTERTWINER
    COMPARISON_ONLY o anything                   -> INADMISSIBLE

dependency_state:
    weakest state present; PINNED_UNVERIFIED is absorbing

scope:
    union assumptions; compatibility-checked meet of opens
```

After relation composition, the canonical replay machine verifies that the result satisfies the consuming claim's transport variance:

```text
COVARIANT_IDENTITY
INVARIANT_UNDER_ISOMORPHISM
BASE_CHANGE_WITH_HYPOTHESES
ORDER_PRESERVING_ONLY
NONTRANSPORTABLE
```

Unsupported transport raises `TRANSPORT_UNSUPPORTED`.

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

### 6.6 Typed negative-claim certificates

Negative ideal membership uses the cheapest sufficient route:

```text
N1  Separating ring map
    phi : R -> S
    phi(I) = 0, checked on generators
    phi(f) != 0

    S may be the base field when a rational evaluation exists,
    a certified algebraic extension, or a structured quotient.

N2  Separating functional on a certified finite-dimensional quotient
    pi : R -> Q
    pi(I) subseteq W, with W a certified subspace closed under
    the quotient relations
    lambda : Q -> k
    lambda(W) = 0
    lambda(pi(f)) != 0

N3  Certified Groebner basis and a nonzero normal form with its
    complete reduction trace
```

For N2, a finite sample of ideal elements is insufficient: the certificate proves `W` contains the entire image `pi(I)`.

Nonradicality is a positive negative-claim certificate:

```text
CERTIFIED_NOT_RADICAL {
    h,
    exponent m >= 2,
    membership witness for h^m in I,
    one N1/N2/N3 nonmembership witness for h notin I
}
```

Thus `I != sqrt(I)` is certified, never represented as failure to prove radical equality.

Real emptiness has separately typed certificates:

```text
REAL_EMPTY_STURM
REAL_EMPTY_PREORDERING
REAL_EMPTY_ARCHIMEDEAN_MODULE
REAL_EMPTY_CAD_CELL
```

For equalities `f_i = 0` and weak inequalities `g_j >= 0`, the general preordering certificate is:

```text
-1 = sum_i h_i*f_i
     + sum_{alpha in {0,1}^m}
         sigma_alpha * product_j g_j^(alpha_j)
```

where the `h_i` are arbitrary polynomials and each `sigma_alpha` is supplied as an explicit sum of squares. A quadratic-module form is admitted only with a certified Archimedean hypothesis. Strict inequalities and inequations use declared exact encodings.

---

## 7. The stratifying Cella claim-compiler contract

The stratifying claim compiler is an eventual Cella contract implemented by each owning mathematical module. It does not dispatch a command name directly to an algorithm. It lowers a high-level claim to normalized Pathfinder `TaskSpec` obligations; Pathfinder begins at that route-task boundary.

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
    submit constructed certificate to canonical replay
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
replay cost
predicted boundary branching
cache reuse
```

The existing residual-profile and cleanliness machinery can inform this planner, but its telemetry remains non-verdict-bearing.

### 7.1 Scout contract and fitting admissibility

Every scout result carries one typed stability readout:

```text
NUMERIC_MARGIN(value, derived_floor)
DISCRETE_AGREEMENT(count, exceptions)
STRUCTURAL_GAP(witness)
NOT_APPLICABLE
```

Low stability increases expected certification cost but does not prohibit exact checking. The planner may check immediately whenever checking is cheaper than another refinement round.

An aggregate fit, interpolation or cluster consensus may propose a candidate. It certifies nothing until all five obligations are discharged:

```text
1. certified degree or complexity bound
2. typed admissible sample points
3. exact reconstruction
4. exact residual replay at every sample
5. final defining-identity certificate
```

Objects with exceptional fibres declare their exceptional loci rather than being rejected for failure of constant per-sample structure. A dual-lane disagreement is a conflict only when both lanes are certified adequate for the quantity; otherwise the event is `DUAL_LANE_UNRESOLVABLE`.

The post-certification winner audit may update a scout calibration ledger. The ledger may reorder routes, never alter verdicts. Each route record pins the calibration-ledger snapshot hash and planner version so adaptive planning remains reproducible.

Iteration scheduling uses the full structure of prior iterations, not a scalar success/failure residual alone. Round-trip residuals, recursive drift, role transport and parameter sweeps form a recommended non-normative scout vocabulary; no proof may depend on that vocabulary.

### 7.2 Symmetry admission and structural scheduling

The planner admits an action to the symmetry registry only when it receives:

```text
1. an automorphism sigma of the carrier
2. generator-wise containment sigma(f_i) in I
3. equality sigma(I) = I
```

In a Noetherian carrier, item 3 may be discharged by the stabilization argument from `sigma(I) subseteq I` and invertibility. Outside the Noetherian setting, explicit inverse containment is required. Detection is scouting; admission is certified. Failure raises `SYMMETRY_UNADMITTED`.

### 7.3 Certified descent and scope composition

Holonomy and other continuous readouts may propose `STOP`, `DESCEND` or `SPLIT`; ideal-theoretic certificates alone decide:

```text
STOP:
    I : h^infinity = <1>
    The inverted open is empty. In particular h in sqrt(I) is a
    certified empty-open result.

DESCEND:
    I + <h> is proper
    dim R/(I + <h>) < dim R/I

SPLIT, zero-divisor route:
    g*h in sqrt(I)
    g notin sqrt(I)
    h notin sqrt(I)

    hence V(I) = V(I + <g>) union V(I + <h>),
    with both children proper.

SPLIT, certified-component route:
    certified minimal components P_i
    h lies in some P_i and not in others
```

Termination of this stratifier uses:

```text
mu(node) = (V(sqrt(I)), remaining_obligation_rank, remaining_budget)
```

The first component is ordered by strict closed inclusion. Noetherianity makes this order well-founded; each `DESCEND` or `SPLIT` child is certified to be a strictly smaller closed set. Obligation rank handles recursion preserving the carrier. Exhaustion after certified decreases is `REFUSED_BUDGET`; an unproved recursive edge is `DEFECT`.

Scopes compose only after a compatibility decision:

```text
compatible
    -> form the meet of opens and evaluate nonvacuity
certified empty
    -> CERTIFIED_SCOPE_EMPTY
compatibility unknown
    -> SCOPE_NONVACUITY_NOT_CERTIFIED
contradictory characteristics or incompatible localizations
    -> SCOPE_INCOMPATIBLE, or CERTIFIED_SCOPE_EMPTY when emptiness
       itself is certified
```

The nonvacuity status is:

```text
CERTIFIED_SCOPE_NONEMPTY
CERTIFIED_SCOPE_EMPTY
SCOPE_NONVACUITY_NOT_CERTIFIED
```

Geometric and real nonvacuity are different claim semantics. Saturation, dimension drop or an algebraic point may certify geometric nonvacuity; a real pipeline requires a real point or a certified real-dimension route. A rational point is sufficient when available, never assumed to exist.

---

## 8. Kernel architecture

```text
MODULE P — cella.pathfinder                         FIRST BUILD
    P0  task/source/candidate protocols
    P1  native ZZ, GF(p), QQ and exact matrices
    P2  rings, orders, polynomials and labelled reduction
    P3  route planning and native modular scouting
    P4  CRT, reconstruction and witness construction
    P5  canonical certificate IR and replay machine
    P6  multiprocessing, checkpoints and artifact store

MODULE I — cella.ideals                            FUTURE
    elimination, localization, Hilbert data, radicals, components,
    primary decomposition and scheme multiplicities

MODULE A — cella.algebra                           FUTURE
    factorization, resultants, finite algebras, fields, norms,
    traces and minimal polynomials

MODULE R — cella.real                              FUTURE
    real roots, signs, chambers, emptiness and exact matrix selection

MODULE C — cella.covers                            FUTURE
    normalization, morphisms, specialization, ramification,
    branch data and realization posets

MODULE G — cella.groups                            FUTURE
    valuations, Kummer modules, inertia, permutation and wreath data

MODULE L — cella.local                             FUTURE
    series, jets, Newton data, germs and local classifiers

MODULE D — cella.geometry                          FUTURE CLIENTS
    Galois horizon, DBP orbit, curvature, periods and domain applications

MODULE API — composed Cella surfaces               FINAL COMPOSITION
    Python package, MCP adapter, CLI and artifact inspection
```

<pre style="color:#d1242f">EXTERNAL GAP — WRAPPER BOUNDARY                  SEPARATE PACKAGES
    CandidateSource protocol implementations
    first integration: Macaulay2 wrapper
    replacement: the corresponding native proposal/search route
</pre>

Only Module P is part of the first build. The remaining sections of this document specify future modules and their eventual composition. They are retained in full so Pathfinder's interfaces do not foreclose the complete engine.

<span style="color:#d1242f"><strong>EXTERNAL GAP — wrapper boundary:</strong> wrapper implementations remain outside Module P and outside the trust root. The first Macaulay2 wrapper tests candidate ingress; native Pathfinder route discovery and replay remain independently buildable. Each wrapper capability names the native route required to replace its candidate source.</span>

### 8.1 Verification trust root

Every certificate is checked by one deterministic bounded replay machine. Proof-producing operations serialize reductions, multipliers, orderings and branches into the certificate DAG; replay performs no search, route selection or alternative computation. Loops over recorded steps, canonical sorting and normalization are permitted. Verification cost is bounded as a function of the canonically encoded certificate size.

Homomorphic polynomial identities may first be replayed modulo admissible primes derived deterministically from the certificate hash. A modular failure is a sound rejection; surviving certificates still receive exact replay. This prescreen never certifies an identity. Its rejection event is `CERTIFICATE_PRESCREEN_REJECT`.

Confirmation oracles and parser-diverse recomputation are not part of the architecture. Construction and replay share the canonical certificate semantics but not search authority: search code cannot seal a public result, and replay code contains no candidate-discovery routines.

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

Pathfinder v1 owns:

```text
gcd / extended gcd
content and primitive part
exact division
modular inverse
CRT with compatibility witness
rational reconstruction
dense and sparse exact matrix operations required by admitted closure tasks
```

Later owning modules add, natively:

```text
square-free decomposition
general Bareiss and modular determinants
rank and nullspace outside the closure-task surface
Smith and Hermite normal forms
extension-field and quotient-algebra arithmetic
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
11. Submit the constructed certificate to canonical exact replay.
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

Canonical replay also verifies:

```text
G is monic
G is interreduced
the declared order is admissible
the order and ring fingerprints match the claim
```

Initially every pair may be checked. Later, a native proof-producing sufficient-pair criterion may provide a smaller sufficient pair set, provided the criterion decisions themselves are replayable.

### 10.4 Route record versus proof

```text
ScoutTrace:
    primes, modular bases, clusters, schedules, CRT history, timings

GroebnerCertificate:
    G, U, V, critical-pair witnesses, ring/order fingerprints
```

The verdict certificate remains valid if the native scout strategy or candidate source is replaced.

### 10.5 Bounded evaluate-interpolate reconstruction

Evaluate-interpolate is a third exact reconstruction lane beside CRT/rational reconstruction and Hensel lifting. It is admissible only with:

```text
certified degree bound in the parameter
distinct admissible exact nodes
pole and degree-drop checks at every node
exact reconstruction
per-node residual replay
final defining-identity certificate
```

An inadmissible specialization is recorded and replaced. Agreement at sampled nodes without the degree bound and final identity is scouting only.

---

## 11. Module I — Certified ideal and scheme services

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

A certified GB supplies a leading monomial ideal. Canonical combinatorial replay rules then validate:

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

General decomposition may use native modular equidimensional, colon, factorization and recursive-splitting routes. The owning module must construct the witnesses for the exact claimed level:

```text
I = intersection_i Q_i
rad(Q_i) = P_i
P_i is prime
Q_i is P_i-primary
minimality/noncontainment
embedded-component accounting
```

If only minimal supports are proved, `cella.ideals` must not label the result a primary decomposition.

### 11.6 Structured decomposition claim grades

The decomposition service exposes four independent guarantees:

```text
CERTIFIED_MINIMAL_PRIMES
    the complete set MinAss(I)

CERTIFIED_RADICAL
    sqrt(I) = intersection_i P_i

CERTIFIED_RADICAL_EQUALITY
    I = sqrt(I)

CERTIFIED_NOT_RADICAL
    I != sqrt(I), with an explicit element or nilpotence witness

CERTIFIED_PRIMARY_DECOMPOSITION
    I = intersection_i Q_i with primary, embedded and multiplicity data
```

For a nonreduced ideal, `cella.ideals` certifies the negative radical-equality claim rather than
turning it into a refusal. If primary decomposition is in the released task surface, it must also
complete that task natively. For example:

```text
I = <x^2,y>

MinAss(I) = {<x,y>}
sqrt(I) = <x,y>
I != sqrt(I)
generic length = 2
I is <x,y>-primary
```

This prevents a support calculation from being mistaken for scheme equality.

### 11.7 Certified reduced complete-intersection theorem

Let:

```text
R = Q[x_1,...,x_n]
I = <f_1,...,f_c> != R
height(I) = c
f_1,...,f_c a certified regular sequence
```

The route is Gröbner-free only when height and regularity come from structural witnesses. Otherwise its cost includes the Gröbner or equivalent completion used to establish them.

A normative structural certificate is the fresh-variable monic sequence: order the generators so each is monic in a variable absent from all earlier generators. A monic polynomial in a fresh variable is a non-zero-divisor over any coefficient ring, so the sequence is regular without a domain assumption on intermediate quotients. The canonical replay machine checks the fresh-variable and leading-coefficient conditions syntactically.

For the current incidence ideal:

```text
w_i^2 - u - N_i^2           monic in fresh w_i, i = 1,...,4
w_1+w_2+w_3+w_4-4M         monic in fresh M
```

This supplies the height-five regular-sequence certificate used by the structured route.

Fix either a positive grading making `I` and the candidates homogeneous, or a declared
homogenization whose affine closure and components at infinity are certified. Every degree below
is bound to this `DegreeSpec`.

Let `P_1,...,P_r` be distinct candidate ideals. If `cella.ideals` constructs and replay-seals certificates for:

```text
I subseteq P_i                         for every i
P_i prime                              for every i
height(P_i) = c                        for every i
a c-by-c Jacobian minor nonzero in R/P_i
degree(I) = sum_i degree(P_i)          in one DegreeSpec
```

then:

```text
MinAss(I) = {P_1,...,P_r}
sqrt(I) = intersection_i P_i
I = sqrt(I)
I = intersection_i P_i
```

The reasoning is:

```text
regular sequence
-> complete intersection
-> Cohen-Macaulay
-> no embedded associated primes and S_1

Jacobian witnesses
-> generic reducedness and R_0 on each candidate

degree balance
-> no missing minimal component and generic length one

R_0 + S_1
-> reduced
```

The output is simultaneously a minimal-prime, radical, radical-equality and prime-primary
decomposition certificate.

### 11.8 Localization correction

For a declared open set, first construct:

```text
I_open = I : d^infinity
```

Saturation may destroy the displayed complete-intersection presentation. Before applying the
theorem, `cella.ideals` must re-certify:

```text
I_open = <g_1,...,g_c>
height(I_open) = c
g_1,...,g_c a regular sequence
```

Generator count equal to codimension is diagnostic only. The reported degree is the degree of the
saturated closure `V(I:d^infinity)` under its declared `DegreeSpec`, while removed components are
retained as boundary tasks.

### 11.9 Structured decomposition route ladder

The planner attempts:

```text
Route A  direct substitution and symmetry
Route B  complete-intersection theorem and degree balance
Route C  triangular/domain tower
Route D  Kummer or finite-extension primeness
Route E  factor/resultant candidate discovery
Route F  modular Gröbner reconstruction
Route G  native equidimensional/colon/splitting primary decomposition
```

Routes A-D can close without Gröbner search when their witnesses are supplied directly. Routes F-G
provide arbitrary-ideal completeness.

Prime certificates may use:

```text
P1  explicit linear elimination and inverse ring maps
P2  monic triangular irreducible extension tower
P3  explicit parametrization/isomorphism to a certified domain
P4  Kummer or finite-extension irreducibility over Frac(B)
```

For the rotating difference ideal, P4 applies to:

```text
IZ ~= B[J]/<J^2-(gamma-4P)/16>
```

once `B` is certified a domain and `[gamma-4P]` is certified nonsquare.

### 11.10 Decomposition proof obligations

When any Gröbner candidate participates, the mathematical certificate includes:

```text
G = U*F
F = V*G

S(g_i,g_j) = sum_k q_ijk*g_k
LM(q_ijk*g_k) < lcm(LM(g_i),LM(g_j))
```

and exact polynomial-combination witnesses for every containment. A Boolean normal-form result or
digest is insufficient.

An intersection replay using the same division/elimination kernel is labelled:

```text
same_kernel_consistency_replay
```

It is useful mutation resistance, not an independent proof lane. The theorem witnesses, replayed
by the one canonical replay machine, carry the answer warrant.

A failed Jacobian gate returns:

```text
GENERIC_REDUCEDNESS_NOT_CERTIFIED
```

It does not by itself prove nonreducedness; it may expose a wrong candidate, incorrect codimension,
singular presentation or failed theorem hypothesis.

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

This is the desired Modules A/G behavior, lowering only its exact polynomial and reconstruction obligations to Pathfinder:

```text
recognize field-tower structure
select Kummer proof
certify primeness directly
avoid irrelevant decomposition work
```

---

## 13. Module A — Finite algebra, field and factorization

### 13.1 Factorization

Factorization follows the same cheap-search/proof-producing-construction pattern, with factor-specific verdict nodes handled by the canonical replay semantics.

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

## 14. Module C — Normalization, morphism and cover services

`cella.covers` must preserve the distinction between:

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

## 15. Module G — Valuation, Kummer and group services

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

For radicands `a_1,...,a_r`, `cella.groups` constructs:

```text
span_F2([a_1],...,[a_r]) subset K*/K*2
```

A valuation-parity matrix gives a certified lower bound on rank. Exact rank is promoted only when the lower bound meets the generator upper bound or explicit relations close the gap.

Rows of the parity matrix are divisor-loop valuation parities and columns are the adjoined square classes. Its exact law is:

```text
rank(parity matrix) <= rank(square-class module)
```

Equality requires the parity lower bound to meet the generator upper bound or explicit square-class relations to close the gap.

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

## 16. Module R — Exact real algebra and physical selection

Elimination over `QQ` returns complex Zariski closure data. Physical selection requires a separate exact real layer.

The planner follows the invariant-floor doctrine: discharge a claim at the lowest sufficient exact invariant level. Coefficient data such as traces, elementary symmetric functions, determinants and characteristic-polynomial coefficients precede root isolation. Spectrum access is an escalation only when the claim concerns roots, their order or their selection as such.

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

## 17. Modules L/D — Local germ, jet and curvature services

The geometry corpus should remain a client of the algebra kernel. Its theorem and route logic belongs in `cella.local`/`cella.geometry`; those modules lower exact algebraic tasks to Pathfinder.

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

Global curvature expansion is a general route, not the default route.

### 17.1 Exact rational inertia

The local classifier computes symmetric-form inertia over `QQ` by congruence reduction using both 1-by-1 and 2-by-2 pivots. A block

```text
[[0,b],[b,0]]
```

contributes one positive and one negative direction. Sylvester's law is applied to the resulting block diagonal form; no floating eigendecomposition is admitted.

The outcomes distinguish the certified quadratic result from any higher-order obligation:

```text
INERTIA_CERTIFIED_WITH_NULLITY(rank, signature, nullity)

HIGHER_JET_REQUIRED_FOR_CLASSIFICATION
    only when a further classification depends on behavior along
    quadratic null directions; the certified inertia remains valid
```

### 17.2 Shared transport interface, without cross-domain identification

The Kummer-cover, defining-function gauge and chart-role systems each have their own normative theorems. They share an engineering interface—structure group, transport operation, holonomy readout and base/fibre separation—but this cross-domain correspondence has `relation_grade = COMPARISON_ONLY`.

The gauge transport theorem certifies its defining-function system only; it does not prove Kummer monodromy. The parity matrix certifies the Kummer lower bound under its tame valuation hypotheses. Framed-jet permutation transport is certified by its own orbit theorem. No arm underwrites another without an exhibited intertwiner.

---

## 18. Module C — Realization poset as a native artifact

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

| Current stage | Owning Cella-module query | Preferred first route | Required proof |
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

The assembled Cella acceptance corpus must correct rather than reproduce the following bookkeeping defects.

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

Evenness handles the negative walls. `cella.real` should construct these exact remainders or a gcd/Bézout witness and lower them to canonical replay, not call the check numerical.

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

Twenty-four saturation calls are repeated eager work caused by reloading three derived objects in eight isolated stages. The assembled Cella proof DAG, backed by Pathfinder's artifact store, should eliminate this repetition before lower-level algorithm optimization is attempted.

---

## 21. Content-addressed proof DAG and execution economy

The current staged corpus repeats the same model loads and many saturations. The assembled Cella artifact DAG should make repeated work structurally impossible, with Pathfinder caching reusable route artifacts underneath it.

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
replay-semantics version
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

Scout work is parallel. Canonical replay remains deterministic. Large witnesses live in immutable artifacts referenced by content hash.

---

## 22. Refusal and retry calculus

The public envelope has orthogonal mathematical-verdict and execution-disposition axes:

```text
verdict = CERTIFIED
    Proof DAG closes under canonical replay and contains no
    PINNED_UNVERIFIED dependency.

verdict = CERTIFIED_RELATIVE
    Claim is discharged conditional on explicitly named unverified
    dependencies. Every such dependency appears in scope.assumptions.

verdict = none; disposition = ROUTE_RETAINED
    Candidate evidence and checkpoint are retained without a mathematical answer.

verdict = none; disposition = REFUSED_SCOPE
    Query lies outside the declared aperture.

verdict = none; disposition = REFUSED_BUDGET
    Metered resources are exhausted after all recursive transitions
    recorded their required certified decrease.

verdict = none; disposition = DEFECT
    A kernel invariant is violated.
```

Semantic totality, operational termination and refusal-taxonomy completeness are separate guarantees. Every routine supplies its own well-founded measure or metered budget under Law 18.

### 22.1 Internal retryable events

```text
SCOUT_NO_CONSENSUS
CRT_MODULUS_INSUFFICIENT
RATIONAL_RECONSTRUCTION_AMBIGUOUS
CANDIDATE_SUPPORT_MISMATCH
CANDIDATE_CONTAINMENT_FAILED
CANDIDATE_PAIR_CLOSURE_FAILED
HENSEL_LIFT_INCOMPLETE
```

These normally trigger replanning or a wider scout budget.

### 22.2 Terminal admissibility, scope and budget outcomes

A missing native operation is never represented by one of these outcomes. It is an unreleased module obligation. `REFUSED_SCOPE` is reserved for a query that is outside an intentionally declared mathematical aperture, not for a route that the owning module has merely failed to implement.

```text
NON_ADMISSIBLE_MONOMIAL_ORDER
INCOMPATIBLE_SCOPE_ASSUMPTIONS
REQUESTED_GUARANTEE_OUTSIDE_DECLARED_APERTURE
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
NONDETERMINISTIC_CANONICALIZATION
CERTIFICATE_REPLAY_MISMATCH
SEAL_ATTEMPT_BEFORE_REPLAY
RECURSIVE_EDGE_WITHOUT_CERTIFIED_DECREASE
```

Defects must never be rebranded as mathematical refusals.

---

## 23. Public result and certificate envelope

```text
{
  "schema_version": "...",
  "verdict": "CERTIFIED | CERTIFIED_RELATIVE | null",
  "execution_disposition": "SEALED | ROUTE_RETAINED | REFUSED_SCOPE | REFUSED_BUDGET | DEFECT",
  "claim": {...},
  "scope": {
    "ambient": {...},
    "open_set": {...},
    "assumptions": [...],
    "exceptional_strata": [...],
    "semantics": "geometric | real",
    "compatibility": "compatible | empty | unknown | incompatible",
    "nonvacuity": "CERTIFIED_SCOPE_NONEMPTY | CERTIFIED_SCOPE_EMPTY | SCOPE_NONVACUITY_NOT_CERTIFIED"
  },
  "value": {...},
  "account": {...},
  "proof_bundle": {
    "verdict_certificate": {...},
    "route_transcript": {...}
  },
  "warrant": {
    "proof_grade": "...",
    "dependency_state": "...",
    "relation_grade": "...",
    "scope": {...}
  },
  "route": {...},
  "route_state": {...},
  "stability_readout": {...},
  "procedure_verdict": {...},
  "answer_verdict": {...},
  "provenance": {...},
  "reproducibility_seal": {...},
  "refusal": null | {"reason": "...", "salvage_manifest": [...]},
  "artifacts": [...]
}
```

`route_transcript`, `route_state`, `provenance` and `reproducibility_seal` do not substitute for the verdict certificate.

---

## 24. Python, MCP and runtime design

### 24.1 Separate modules, shared canonical protocols

Module P exposes the first semantic kernel through Python and CLI. Future Cella modules consume its canonical task and certificate protocols without becoming Pathfinder dependencies. The eventual MCP layer validates, routes and serializes across assembled modules; it contains no mathematical algorithms.

### 24.2 Recommended implementation split

```text
First build — cella.pathfinder:
    Python public/orchestration layer
    native C++20 mathematical kernel
    CPU-only multiprocessing
    Cella-owned coefficient, polynomial and replay primitives

Future Cella modules:
    separate packages consuming Pathfinder tasks and certified results
    no upward dependency from Pathfinder

Optional source integrations:
    separate wrapper distributions implementing CandidateSource
    never linked or imported by the Pathfinder core
```

The semantics and certificate format do not depend on a wrapper, external program or future mathematical module.

<span style="color:#d1242f"><strong>EXTERNAL GAP — GMP/FLINT-class arithmetic:</strong> the earlier architecture permitted these libraries as low-level workers. They remain recorded as an external acceleration possibility for the eventual engine, but the first Pathfinder module replaces them with native arbitrary-precision integer, rational, prime-field, matrix, CRT and reconstruction implementations.</span>

<span style="color:#d1242f"><strong>EXTERNAL GAP — CUDA/GPU worker:</strong> retained only as an eventual acceleration seam. It is excluded from the first Pathfinder build. Replacement prerequisite before any later GPU work is a complete, profiled CPU-native batch-reduction route with identical certificate semantics.</span>

### 24.3 Public query surface

The first Pathfinder surface is deliberately module-shaped:

```text
cella.pathfinder.solve(task_spec, sources=[])
cella.pathfinder.verify(certificate_or_manifest)
cella.pathfinder.resume(route_state, additional_budget)
cella.pathfinder.explain(result)
cella.pathfinder.capabilities()
```

The eventual composed Cella MCP surface should remain small:

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
  pathfinder/                         MODULE P — FIRST BUILD
    api/
      task
      result
      source_protocol
    ir/
      domain
      ring
      grading
      order
      polynomial
      route
      certificate
    native/
      bignat
      bigint
      rational
      prime_field
      matrix
      monomial
      polynomial
      reduction
      closure
      modular
      crt
      reconstruction
    planner/
      cost
      schedule
      native_source
      candidate_ingress
    proof/
      nodes
      builder
      replay
      seal
    runtime/
      scheduler
      worker
      budget
      checkpoint
      artifact_store

  ideals/                             MODULE I — FUTURE
    ideal
    elimination
    localization
    hilbert
    radical
    components
    decomposition

  algebra/                            MODULE A — FUTURE
    factor
    quotient
    finite_extension
    resultant
    norm_trace
    minpoly

  real/                               MODULE R — FUTURE
    sturm
    isolation
    sign
    emptiness
    pencil

  covers/                             MODULE C — FUTURE
    morphism
    normalization
    ramification
    branch
    specialization
    realization_poset

  groups/                             MODULE G — FUTURE
    permutation
    module
    kummer
    inertia
    wreath
    monodromy

  local/                              MODULE L — FUTURE
    valuation
    series
    newton
    germ
    inertia

  geometry/                           MODULE D — FUTURE CLIENTS
    jets
    role_orbit
    carrier
    curvature

  api/                                FINAL COMPOSITION
    python
    mcp
    cli
```

<p style="color:#d1242f"><strong>EXTERNAL GAP — optional wrapper distributions:</strong> these are not children of <code>cella/</code>, never link into Pathfinder, and each manifest capability names the native search route required to replace it.</p>

<pre style="color:#d1242f">cella-pathfinder-m2
cella-pathfinder-singular
cella-pathfinder-custom-source
</pre>

Current Cella geometry, period and benchmark modules become future clients or are adapted behind these interfaces. Legacy V4 eval campaigns remain corpus material, not dependencies of Module P.

---

## 26. Build program without scope reduction

The builds below order construction; they do not narrow the eventual target. Only Build P is the first product. Later modules remain separate packages until an explicit composition decision.

### Build P — standalone `cella.pathfinder`

Build the complete CPU-native route kernel defined by `CELLA_PATHFINDER_MODULE_SPEC_v1.0.md`:

```text
canonical TaskSpec and CandidateSource protocol
Cella-owned ZZ/GF(p)/QQ and exact matrices
RingSpec, GradingSpec and OrderSpec
sparse polynomials and labelled reduction
native serial/batch closure and modular scouting
prime scheduling, CRT and rational reconstruction
witness construction and canonical replay
multiprocessing, checkpoints and immutable artifacts
Python API and CLI
```

Build P excludes CUDA and every external mathematical dependency from its core. It accepts optional candidates through wrappers without importing those wrappers.

<span style="color:#d1242f"><strong>EXTERNAL GAP — first integration test:</strong> `cella-pathfinder-m2` is built as a separate wrapper package to prove the `CandidateSource` boundary. Its initial manifest exposes only `CLOSE_BASIS` over the declared `QQ` polynomial-ring fixture. It returns a candidate artifact that receives native witness construction and replay. Native closure is the exact replacement route and is completed before Build P release. Elimination, saturation, Hilbert, radical and decomposition operations are not smuggled through this wrapper; they remain native Module I build work. Macaulay2 is not required to build, test or run Pathfinder core.</span>

### Build I — `cella.ideals`

Build elimination, localization, intersection, Hilbert data, typed degree, nonemptiness, radicals, support/component classification and primary decomposition. Implement the structured decomposition route ladder, the reduced-complete-intersection theorem, P1/P3 domain maps and P4 Kummer certificates. This module compiles its closure and membership obligations into Pathfinder tasks.

### Build A — `cella.algebra`

Build factorization, resultants, discriminants, quotient fields, finite extensions, minimal polynomials, norms and traces. Factorization may use its own scout/certificate recursion while sharing Pathfinder task and artifact protocols.

### Build R — `cella.real`

Build Sturm/subresultant methods, root isolation, sign determination, real emptiness and matrix-pencil selection. Keep geometric and real scope semantics separate.

### Build C — `cella.covers`

Build normalization-aware morphisms, specialization, relative differentials, ramification, branch images and realization-poset artifacts.

### Build G — `cella.groups`

Build valuations, Kummer modules, inertia, permutation actions, semidirect products, wreath products and monodromy certificates.

### Build L/D — `cella.local` and domain clients

Port the active role-jet, carrier, exact inertia, curvature-germ, Newton-corner, period and root-selection clients onto the separate modules and run the complete hostile regression program.

### Final composition — `cella.api`

Assemble Python, MCP and CLI surfaces only after module boundaries and dependency direction have remained stable. Pathfinder remains independently installable and usable.

Every build annotates each recursive or iterative routine with its well-founded measure or monotonically consumed budget. This is a merge gate, not deferred documentation.

---

## 27. Acceptance gates

### 27.0 Pathfinder module gates

The first module must independently pass:

```text
native exact coefficient arithmetic
native ring/order/polynomial lowering
proof-producing labelled reduction
native modular route discovery and deterministic reconstruction
canonical replay with no search or confirmation oracle
CPU multiprocessing with byte-stable merge order
wrapper-free build and test execution
separate optional-wrapper boundary integration
no dependency on any future Cella mathematical module
```

<span style="color:#d1242f"><strong>EXTERNAL TEST — Macaulay2:</strong> the first optional-wrapper gate runs the separately installed M2 `CLOSE_BASIS` fixture. Its replacement gap is the native closure route already required by Build P; absence of M2 cannot skip or alter any core gate.</span>

### 27.1 Mathematical gates

The assembled Cella engine must:

```text
certify both ideal containments for every reconstructed GB
certify every claimed critical-pair closure
distinguish grading from monomial order
distinguish support from scheme structure
distinguish complex projection closure from real image
bind every generic result to its exact localization
bind every specialization to a parameter map and degree behavior
emit exact certificates or refuse
prevent PINNED_UNVERIFIED dependencies from entering CERTIFIED
expose every unverified dependency in CERTIFIED_RELATIVE scope assumptions
require claim-specific adequacy for every verdict-bearing observation family
reject COMPARISON_ONLY edges from proof DAGs
compose transport only under the claim's declared variance
separate minimal primes, radical, radical equality and primary decomposition
re-certify complete-intersection hypotheses after saturation
type every degree by grading/homogenization and object scope
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
canonical replay runs without scout, planner or candidate-source code
all wrapped candidates enter through the same CandidateSource protocol
route and answer verdicts remain separate
reproducibility seals never upgrade certificate grade
slice evidence never promotes a generic theorem
low scout stability prices a route but does not itself block exact checking
rational witness points are used only when certified to exist
geometric scope evidence never silently becomes real nonvacuity
```

<span style="color:#d1242f"><strong>EXTERNAL GAP — candidate wrappers:</strong> Macaulay2, Singular, suitable symbolic programs or any later proposal source must be observationally identical at the `CandidateSource` boundary. Each wrapper remains separately installed and each capability it supplies retains a named native replacement task. FLINT/GMP are not source wrappers and are excluded from Pathfinder linkage; numerical trackers are research observers only.</span>

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
conditional-as-absolute-certificate mutations
comparison-edge-in-proof-DAG mutations
incompatible-scope-meet mutations
inadequate-observation-family mutations
characteristic-2/wild-inertia mutations
cache-key and stale-proof mutations
```

The decomposition battery must include:

| Ideal | Required assembled-Cella result |
|---|---|
| `<x*y>` | Certify all four grades with components `<x>` and `<y>`. |
| `<x^2-y^2>` over `Q` | Certify all four grades with `<x-y>` and `<x+y>`. |
| `<x^2,y>` | Certify minimal prime and radical `<x,y>`, certify `I != sqrt(I)`, certify that `I` is `<x,y>`-primary, and record generic length two. |
| `<x^2,x*y>` | Certify the CI theorem route inapplicable, then certify `<x^2,x*y> = <x> intersect <x^2,y>` with both primary components and the embedded component retained. |
| `<x*y>:x^infinity` | Certify `<y>` and retain `<x>` as a removed boundary component. |
| `<w^2-u-N^2,u>` on `D(2N)` | Certify the two contact components by direct linear/domain maps. |
| rotating `IZ` | Certify primeness through the Kummer finite-extension route once its hypotheses are admitted. |

### 27.5 Runtime gates

```text
byte-stable canonical outputs
content-pinned inputs and replay semantics
deterministic verification
one canonical deterministic replay machine
deterministic hash-derived modular prescreen primes
resume from retained CRT/Hensel state
lazy content-addressed DAG reuse
calibration-ledger snapshot and planner-version pins
per-routine termination measure or monotonically consumed budget
global metering of every search loop
time/memory/pair/term/coefficient/proof telemetry
large-artifact streaming by manifest
```

---

## 28. Explicit engineering and research obligations

These gaps remain part of the architecture; they are not reasons to shrink it.

```text
efficient native labelled batch-closure witness reconstruction
proof compression for large critical-pair families
per-claim observation-adequacy theorem library
per-routine termination annotations for every existing search routine
native coefficient-domain extensions beyond the mandatory initial domains
native strong-basis semantics over ZZ, including coefficient divisibility and complete S/G obligations
local and standard-basis routes
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

For the KN closure pilot, extremal noncancellation is treated as a negative-membership-shaped obligation. It may discharge at N1 by a separating exact evaluation or ring-map witness. A rational stratum point is preferred when it exists; otherwise the witness may land in a certified algebraic extension or structured quotient. Existence of a rational point is never assumed.

Every such obligation is assigned to its owning module as explicit native build work. An unimplemented operation blocks that module's release claim; it is not silently delegated to a wrapper or converted into a shipped capability apology.

---

## 29. What is lifted, generalized, retired and quarantined

### Lift at the constitutional level

```text
typed refusal
exact canonical serialization
separate search and seal authority under one replay semantics
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
proofs.py           -> primitive proof nodes in the canonical replay machine
qsqrt.py            -> arbitrary finite algebraic extensions
pathfinder.py       -> route-task normalizer, structural recognizers and cost planner
cleanliness burden  -> algebraic cost and proof-burden model
geometry strata     -> universal scope/open/boundary semantics
```

### Retire from the base kernel

```text
legacy TypedResult as universal carrier
projection-specific refinery/solver as foundational dependencies
floating fits as proof
digest equality as mathematical certification
implicit worker or source monomial-order semantics
silent approximate substitution
global expansion as default geometry route
```

### External wrappers and research clients

<span style="color:#d1242f"><strong>EXTERNAL GAP — candidate-source wrappers:</strong> Macaulay2, Singular and suitable symbolic programs may be retained only as separately distributed `CandidateSource` processes. Their native replacement gaps are the exact search routes each manifest exposes; they never link into Pathfinder or contribute proof edges.</span>

<span style="color:#d1242f"><strong>EXTERNAL GAP — rejected low-level accelerators:</strong> GMP and FLINT remain recorded only as historical or optional eventual-engine acceleration references. They are not `CandidateSource` implementations and are never linked into native Pathfinder. Replacement requires the Cella-owned coefficient, factorization and matrix primitives assigned to Modules P and A.</span>

<span style="color:#d1242f"><strong>EXTERNAL GAP — numerical research sources:</strong> mpmath and numerical trackers remain research observation sources only. Replacement requires native exact-real, interval and certified path-lifting routes; their observations never enter a verdict certificate.</span>

<span style="color:#d1242f"><strong>EXTERNAL GAP — specialist harnesses:</strong> external PSLQ/period harnesses and numerical monodromy trackers remain research clients. Replacement requires native relation reconstruction, certified period evaluation and certified path lifting.</span>

Legacy eval campaigns and specialized DBP/Galois scripts remain corpus fixtures and future clients, not runtime dependencies.

### Non-normative transport correspondence

Several domain systems share the minimized engineering shape

```text
S = (C, G acting on C, R subseteq C/G, section s : R -> C)
```

with a declared structure group, transport, quotient, chamber or admissible region, and section. Chart permutations, Kummer covers and defining-function gauges instantiate this interface but are not thereby identified. Their groups and semantics differ, and the correspondence has `relation_grade = COMPARISON_ONLY`.

The correspondence may organize software and suggest scouts. It is inadmissible in proof DAGs and may never be used to make the theorem of one domain prove another. General closure beyond per-family certificates remains an explicit research obligation.

---

## 30. Canonical statement

The strongest coherent design is:

```text
Cella is an eventual modular, claim-first mathematical engine.

It preserves algebraic presentations, morphisms, towers,
localizations, symmetry and strata across separate mathematical modules.

Its first module, cella.pathfinder, is the standalone fast-route kernel.
It performs native route discovery, reconstruction, proof construction
and canonical replay. It accepts candidate artifacts from optional
external wrappers without depending on those wrappers or granting them
certificate authority.

Later modules own ideals and schemes, finite algebra, real algebra,
covers, groups, valuations, local germs and geometry. They consume
Pathfinder but are not joined to it until their own module builds begin.

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

Corrected structured decomposition layer:
    2026-07-11-cella-native-ideal-decomposition.md v1.1

Integrated architecture audits:
    CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1_2r_DELTA.md
    CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1_2r1_DELTA.md
```

The architecture distinguishes theorem text, executable calculation, raw output, finite specialization evidence, generic claim and proposed engine capability. Their inclusion here does not flatten those evidence grades.
