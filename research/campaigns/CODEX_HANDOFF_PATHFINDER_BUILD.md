# Codex Handoff — Cella Pathfinder Build

**Date:** 2026-07-11  
**Status:** Implementation handoff  
**Immediate target:** Recover the early Pathfinder design, lift it onto the new mathematical corpus, and deliver a first M2-integrated vertical slice that reduces total wall-clock time by returning the fastest admissible computational route.  

---

## 0. Read this before touching code

Pathfinder is neither a complete mathematical engine nor a passive route-ID selector.

Pathfinder:

```text
receives an external mathematical task through a host wrapper
lowers it to an internal route-analysis representation
uses native internal mathematical scouts and structural recognizers
constructs and compares admissible computational routes
returns the fastest admissible route through the wrapper
```

Pathfinder stops when it returns the route.

Other modules execute the route, reconstruct the result, construct certificates, replay certificates, and emit the final mathematical answer.

The product objective is:

```text
reduce end-to-end wall-clock time by preventing the host engine from
searching computational paths that Pathfinder can eliminate or bypass
using cheaper structural analysis.
```

Do not implement the invalid minimum-duration selector currently recorded as Pathfinder v1.1. Do not copy the over-scoped ownership model from Pathfinder v1.0.

---

## 1. Source-of-truth order

Read sources in this order.

### 1.1 Behavioral ground truth

```text
upload/pathfinder(1).py
```

This early prototype defines Pathfinder's behavioral DNA:

```text
route_plan
residual fingerprints
route-assembly classification
conservative rewrite generation
geometry/domain overlays
blocking-input detection
next-tool routing
burden/Pareto comparison through pathfinder_compare
```

Preserve its tested behavior before generalizing it.

### 1.2 Full mathematical terrain

```text
CELLA_ARCHITECTURE_v1.3.md
```

Use this for the complete route-family inventory and corpus parity targets. Its current Build-P ownership is not authoritative: several arithmetic, execution, reconstruction and certificate responsibilities were incorrectly fused into Pathfinder.

### 1.3 Inventory only, not ownership

```text
CELLA_PATHFINDER_MODULE_SPEC_v1.0.md
```

V1.0 preserves useful protocol, native-method and test requirements, but it over-scopes Pathfinder by absorbing:

```text
general coefficient services
general polynomial/Gröbner services
final reconstruction
certificate construction and replay
execution scheduling
artifact persistence
```

Mine it for internal route-analysis requirements and module interfaces. Do not reproduce its package ownership.

### 1.4 Explicitly invalid

```text
CELLA_PATHFINDER_MODULE_SPEC_v1.1.md
```

Do not implement this document. It incorrectly reduces Pathfinder to `argmin(predicted_duration)` over routes supplied by the caller. There is no `predicted_duration_ns` design.

### 1.5 New mathematical corpus

Inspect all available current sources, especially:

```text
project_sources/01-DBP_Curvature_Role_Reduction.md
project_sources/02-Canonical_Invariant_Reduction_Theorem.md
project_sources/03-Theorem_8_1_New_Math_Extension.md
project_sources/04-Theorem_8_1_Curvature_Orbit_Correction.md
project_sources/05-Gauge_Channel_Transport_Law.md
project_sources/06-Three_Channel_KG_Strong_Spec.md
project_sources/07-Three_Channel_KG_New_Math_Extension.md
project_sources/12-lead7_kn_n3_dbp_metric.tex
project_sources/13-pfc_normal_forms.tex
project_sources/14-self_glue_monodromy.txt
project_sources/15-dbp_orbit_calculus.tex
project_sources/16-DBP_Curvature_Constants_Corrected_Formulation.md
```

Also inspect these newer corpus files wherever they exist in the target repository or attached project:

```text
ROTATING_THREE_CHANNEL_WREATH_CLOSURE_2026-07-10.md
KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md
DEGREE_20_CROWN_CERTIFICATE_REPORT_2026-07-10.md
WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md
MACAULAY2_REALIZATION_POSET_WORKFLOW_2026-07-10.md
ROTATING_KUMMER_RANK_JUMP_LEMMA_REPORT_2026-07-10.md
R9_STATIC_CLOSURE_OPENING_DERIVATION_2026-07-10.md
galois_horizon_cover_v1_0.tex
REALIZATION_POSET_RUN_REPORT_2026-07-10.md
```

Do not silently skip a missing source. Record the missing filename in the handoff report and continue only with route families supported by available material.

---

## 2. The non-negotiable boundary

### 2.1 Pathfinder owns

```text
internal lowering for route analysis
internal exact/scout representations required to inspect structure
bounded native mathematical probes used only for route discovery
structural fingerprints
route-family recognizers
conservative transformation candidates
route admissibility from supplied/derived structural evidence
burden-vector and Pareto route comparison
route assembly
typed route output
wrapper-neutral serialization of the route
```

### 2.2 Pathfinder does not own

```text
the host's external mathematical objects
general-purpose public arithmetic services
general-purpose public polynomial or Gröbner services
final exact execution of the requested deliverable
final CRT/rational reconstruction service
ideal/scheme service APIs
factorization service APIs
exact-real service APIs
cover/Kummer/wreath execution APIs
local-geometry execution APIs
certificate construction
certificate replay or sealing
final result emission
```

### 2.3 Internal mathematics versus external mathematics

Pathfinder may use native internal arithmetic, polynomial shadows, finite-field probes, exact fractions, AST/IR rewrites and theorem recognizers to learn the route.

These methods must be:

```text
scoped to route discovery
unavailable as general mathematical result APIs
non-verdict-bearing
replaceable without changing the host mathematical object model
```

If a method produces the host's final answer rather than route evidence, it belongs in an execution module, not Pathfinder.

---

## 3. End-to-end contract

```text
Host mathematical task
    -> host wrapper lowers task
    -> Pathfinder internal problem IR
    -> internal scouts and structural recognizers
    -> route fingerprints and admissible route candidates
    -> burden/evidence comparison
    -> selected ComputationalRoute
    -> wrapper lifts route into host terms
    -> host execution modules walk route
    -> external certificate modules certify result
```

Pathfinder's public output is a route, never the final mathematical result.

---

## 4. Wall-clock objective

The release metric is total pipeline time:

```text
T_total =
    T_wrapper_lowering
  + T_pathfinder_analysis
  + T_selected_route_execution
  + T_certificate_construction
  + T_certificate_replay
  + T_wrapper_lifting
```

Compare against:

```text
T_baseline = host engine's existing route for the same exact deliverable
```

Pathfinder succeeds only when:

```text
same mathematical result
same or stronger required warrant
T_total < T_baseline
```

Do not report speedup using Pathfinder analysis time alone. Include wrapper, execution and certification overhead.

There is no wall-clock prediction field in the public contract. Route comparison is driven by actual scout evidence, structural burden and declared route admissibility. Measured wall-clock performance is the release gate.

---

## 5. Preserve the prototype before extending it

Create characterization tests around `upload/pathfinder(1).py` before refactoring.

Required prototype behaviors:

```text
no subtraction -> direct_ok
x - x -> collapse_symbolically
fully rewriteable catastrophic cancellation -> rewrite_candidate_needed
partially rewriteable catastrophic cancellation -> precision_budget_needed
benign cancellation -> direct_ok with monitoring route
unknown symbolic constants -> needs_declared_constants
unrecognized shape -> unsupported_shape
```

Preserve conservative rewrite families:

```text
self collapse
constant-offset collapse
scaled constant-offset collapse
difference of squares
sqrt conjugate
common-factor extraction
three-term regrouping
```

Preserve fingerprint distinctions:

```text
local shape class
residual order and evidence
scale class
account-closure status
burden vector
domain/refusal stratum
canonical cross-form
route-assembly class
site fingerprints
```

Preserve comparison behavior based on:

```text
declared-grid equivalence
BACL lattice burden
rounding-residual ULP burden
final-residual ULP burden
operation depth
stable deterministic tie-breaking
Pareto dominance
```

Do not reinterpret the prototype's `predicted_burden_vector` as predicted wall-clock duration.

---

## 6. Target internal architecture

Use this as the initial package boundary unless the repository already has an equivalent structure.

```text
cella/pathfinder/
  api/
    request.py
    route.py
    wrapper_protocol.py

  ir/
    problem.py
    expression.py
    algebraic.py
    scope.py
    obligation.py
    fingerprint.py
    burden.py

  scout/
    protocol.py
    residual.py
    modular_structure.py
    exact_account.py
    trace.py

  recognize/
    rewrite.py
    triangular.py
    complete_intersection.py
    modular_groebner.py
    finite_extension.py
    kummer.py
    cover.py
    real.py
    local_germ.py
    curvature.py

  plan/
    registry.py
    admissibility.py
    compare.py
    assemble.py
    select.py

  compat/
    legacy_pathfinder.py

  serialize/
    canonical.py
```

Host wrappers remain separate packages:

```text
cella-pathfinder-m2
cella-pathfinder-cella
```

Do not put M2 syntax or process control under `cella/pathfinder/`.

---

## 7. Core typed objects

### 7.1 Pathfinder request

```text
PathfinderRequest {
    request_id,
    target_obligation,
    external_binding,
    mathematical_context,
    available_route_families,
    supplied_scout_evidence,
    already_discharged_obligations,
    analysis_budget
}
```

The wrapper owns `external_binding`. Pathfinder must not reinterpret host variable identities.

### 7.2 Scout evidence

```text
ScoutEvidence {
    scout_family,
    scope,
    structural_fingerprint,
    actual_trace,
    burden_vector,
    stability,
    unresolved_inputs,
    retained_artifact_refs
}
```

Scout evidence is non-verdict-bearing.

### 7.3 Route contract

```text
RouteContract {
    route_family,
    accepted_problem_shape,
    required_hypotheses,
    required_evidence,
    produced_obligations,
    discharged_obligations,
    exceptional_branches,
    execution_module,
    certificate_obligations
}
```

### 7.4 Computational route

```text
ComputationalRoute {
    request_id,
    target_obligation,
    route_family,
    ordered_steps,
    data_dependencies,
    external_binding,
    required_intermediate_objects,
    required_hypotheses,
    certificate_obligations,
    exceptional_branches,
    completion_condition,
    supporting_scout_evidence
}
```

No field contains the final mathematical answer.

---

## 8. Route families to register from the corpus

Implement route recognition incrementally. Every recognizer must cite its source theorem/document and emit explicit hypotheses rather than silently assuming them.

### 8.1 Prototype arithmetic routes

```text
direct evaluation
symbolic self-collapse
constant-offset collapse
scaled-offset collapse
difference-of-squares rewrite
sqrt-conjugate rewrite
common-factor extraction
precision-budget escalation
BACL/Pareto form comparison
```

### 8.2 Structural algebra routes

```text
direct substitution
triangular/domain tower
regular sequence / complete intersection
degree-balance component closure
linear inverse ring map
modular Gröbner structure
elimination-order route
localization/saturation boundary split
factor/resultant route
finite-extension route
```

### 8.3 Kummer, cover and group routes

```text
Kummer square-class independence
valuation-parity lower bound
rotating Kummer rank-jump
Kummer finite-extension primeness
conjugate-module wreath lift
rotating three-channel wreath closure
self-glue exponent/gcd recognizer
branch/inertia stratification
normalization-aware cover route
```

### 8.4 Real and local routes

```text
invariant-floor exact-real route
Sturm/root-isolation escalation
matrix-pencil physical selection
local metric germ
parity-fixed face law
extremal-face law
Newton-wedge corner route
exact rational inertia
curvature role-orbit reduction
gauge-channel transport
```

### 8.5 Realization-poset routes

```text
contact restriction
structured incidence projection
generic-open route with retained boundary tasks
Kummer route to rotating IZ primeness
collision partition plus parity rows to inertia
lazy node/edge realization route
```

---

## 9. Route selection law

Do not use `predicted_duration_ns`.

Selection proceeds in this order:

```text
1. Reject routes whose explicit hypotheses or scope requirements are not met.
2. Prefer routes that discharge the target at the lowest sufficient invariant level.
3. Prefer direct structural routes over general search when both discharge the same target.
4. Prefer local/tower/symmetry routes over global expansion when their hypotheses hold.
5. Compare remaining routes using actual scout burden vectors and Pareto dominance.
6. Use a stable declared tie-break only after mathematical scope and burden comparison.
```

The first implementation should preserve the prototype's burden comparator and generalize it rather than replacing it with a wall-clock predictor.

Wall-clock measurements are fed back into benchmark reports and later calibration work, not represented as fabricated per-request truth.

---

## 10. Native internal-method rule

All route-analysis methods in Pathfinder must be implemented in the project source tree.

For the first build:

```text
Python is the orchestration and reference implementation language.
Use fractions.Fraction for bounded exact rational analysis where sufficient.
Use compact native Python IRs first.
Profile before introducing C++.
Move only demonstrated hot analysis kernels to C++20.
Do not add CUDA.
Do not link GMP, FLINT, a CAS or another mathematical library into Pathfinder core.
```

The M2 integration is a wrapper/client test, not a Pathfinder core dependency.

---

## 11. First M2 vertical slice

The first wrapper must prove the complete boundary:

```text
M2 task
    -> wrapper lowering
    -> Pathfinder internal analysis
    -> selected typed route
    -> wrapper lifting
    -> M2 receives executable route
```

Choose one real corpus task that has:

```text
an existing measurable M2 baseline
a structurally cheaper route already justified in the corpus
an exact result comparison
a certificate path outside Pathfinder
```

Preferred fixture order:

```text
1. a structured ideal route that avoids a known expensive generic operation
2. rotating IZ primeness through the Kummer finite-extension route
3. one realization-poset node with repeated elimination/saturation pressure
```

Before implementing the wrapper, record in `benchmarks/FIRST_M2_FIXTURE.md`:

```text
exact M2 input
baseline M2 command sequence
baseline output
candidate route families
selected structural route and its source theorem
modules that execute each returned step
certificate obligations
measurement protocol
```

The wrapper may translate and return the route. It may not perform route selection itself and may not silently execute a fallback route if Pathfinder fails.

---

## 12. Build phases

### Phase 0 — Repository and source audit

```text
read AGENTS.md and repository instructions
inventory existing packages and tests
preserve the dirty worktree
locate every named corpus source
write a one-page ownership map before editing
```

### Phase 1 — Freeze prototype behavior

```text
copy the prototype into a test fixture, not production code
write characterization tests
record current decisions, fingerprints, rewrites and comparisons
make no semantic changes until tests are green
```

### Phase 2 — Build typed Pathfinder IR

```text
replace unstructured dicts at the public boundary
retain a compatibility encoder for legacy output
separate external bindings from internal mathematical shadows
define typed ScoutEvidence, RouteContract and ComputationalRoute
```

### Phase 3 — Lift prototype engines

```text
port residual fingerprinting
port conservative rewrite recognizers
port geometry overlays into registered recognizers
port burden/Pareto comparison
preserve deterministic behavior
```

### Phase 4 — Register new-math route families

```text
add route contracts one theorem family at a time
attach source references and hypothesis emitters
add positive and hostile fixtures for each recognizer
do not implement the downstream mathematical executor
```

### Phase 5 — Build M2 wrapper

```text
canonical request lowering
canonical route lifting
real first fixture
no M2 code in Pathfinder core
no silent fallback
```

### Phase 6 — Wall-clock campaign

```text
measure baseline and Pathfinder end-to-end routes
include all overhead
verify result equality and certificate grade
record route selection evidence
publish benchmark report
```

### Phase 7 — Optimize only measured hot spots

```text
profile internal analysis
use CPU multiprocessing only for independent scout probes if it lowers T_total
consider C++20 only for demonstrated hot kernels
keep canonical route output identical
leave CUDA out
```

---

## 13. Required tests

### 13.1 Prototype compatibility

```text
all characterization fixtures pass
legacy route decisions remain stable
legacy fingerprints remain stable or receive an explicit migration record
legacy rewrite candidates remain conservative
legacy pathfinder_compare winner and Pareto relations remain stable
```

### 13.2 Route-recognizer tests

Every new recognizer needs:

```text
positive fixture
missing-hypothesis fixture
wrong-scope fixture
exceptional-stratum fixture where applicable
mutation that must prevent route admission
expected certificate-obligation output
```

### 13.3 Boundary tests

```text
Pathfinder returns a route, never a final answer
external variable identities survive wrapper round trip
host-specific objects do not leak into core IR
execution modules are referenced but never invoked by route selection tests
certificate obligations are emitted but never discharged inside Pathfinder
```

### 13.4 Determinism tests

```text
same request and scout evidence -> byte-identical route
input ordering noise does not change canonical route
stable tie-break is used only after admissibility and burden comparison
```

### 13.5 Performance tests

```text
baseline and Pathfinder paths produce the same exact deliverable
required certificate replay succeeds outside Pathfinder
all wrapper and certification overhead is included
Pathfinder route lowers total wall-clock time on its admitted target class
memory usage is recorded
```

---

## 14. Benchmark report schema

For every corpus benchmark, record:

```text
benchmark_id
source_document
host and host version
hardware/process limits
cold/warm policy
mathematical target
baseline route
Pathfinder route
route evidence
baseline wall time
wrapper-lowering time
Pathfinder-analysis time
selected-route execution time
certificate construction/replay time
wrapper-lifting time
total Pathfinder wall time
speedup ratio
peak memory
result-equivalence status
certificate status
```

Do not claim a speedup if total Pathfinder wall time is not lower.

---

## 15. Prohibited shortcuts

```text
Do not implement v1.1's minimum-duration selector.
Do not move the complete mathematical engine into Pathfinder.
Do not use M2 or another CAS inside Pathfinder core.
Do not use an external result as a certificate.
Do not add a confirmation oracle.
Do not silently fallback to the host's default route.
Do not emit a mathematical result from Pathfinder.
Do not use float values as verdict-bearing route evidence.
Do not add CUDA in the first build.
Do not benchmark Pathfinder analysis without downstream execution/certification time.
```

---

## 16. Deliverables

Codex must leave the repository with:

```text
1. corrected Pathfinder build specification
2. source ownership/module map
3. prototype characterization tests
4. typed Pathfinder IR and route output
5. lifted prototype recognizers and comparator
6. initial new-math route registry
7. separate M2 wrapper
8. first real M2 vertical-slice fixture
9. end-to-end wall-clock benchmark harness
10. benchmark report
11. explicit remaining route-family build tickets
```

---

## 17. Definition of done for the first build

The first build is complete only when:

```text
the early prototype behavior is preserved by characterization tests
Pathfinder uses native internal mathematical analysis to discover a route
the selected route is typed and wrapper-neutral
Pathfinder returns no final mathematical answer
the M2 wrapper returns the selected route to M2
M2 and external modules execute and certify that route
the exact result matches the baseline
the certificate requirement is met outside Pathfinder
total measured wall-clock time is lower than the baseline on the declared fixture
no external mathematical dependency or CUDA code exists in Pathfinder core
```

---

## 18. First Codex actions

Execute these actions in order:

```text
1. Inspect repository instructions and current worktree.
2. Locate the prototype and all named corpus sources.
3. Produce `docs/pathfinder/OWNERSHIP_MAP.md` from this handoff.
4. Produce prototype characterization tests without refactoring behavior.
5. Select and document the first M2 benchmark fixture.
6. Draft the corrected build spec around the tested prototype behavior.
7. Implement the typed IR and compatibility layer.
8. Lift one route family at a time with tests.
9. Build the M2 wrapper only after the route contract is stable.
10. Run the complete end-to-end wall-clock comparison.
```

Do not start by building coefficient, Gröbner, reconstruction or certificate service packages inside Pathfinder. Add only bounded internal analysis methods required to discover the selected route.

---

## 19. Canonical handoff statement

```text
Recover Pathfinder from the early route-planning prototype and lift it
onto the complete new mathematical route corpus.

Pathfinder must use native internal mathematical intelligence to discover
the fastest admissible computational route, return that route through a
host wrapper, and stop.

The external mathematical modules execute and certify the route.

The build succeeds only when the complete wrapped pipeline produces the
same exact certified result in less total wall-clock time than the host's
existing route.
```

**END HANDOFF**
