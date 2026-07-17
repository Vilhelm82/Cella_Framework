# MCG Geometry-First Discovery Campaign

**Date:** 2026-05-19  
**Audience:** Claude Code / Codex-style repo implementation agent  
**Mode:** Discovery campaign first, confirmatory testing only after candidates exist  
**Scope:** V4 eval-layer research campaign. Do not modify Layer 0/1 primitives, status families, manifests, protocols, or fixture definitions unless explicitly requested in a later task.

---

## 0. Purpose

This campaign reframes MCG from a residue-first search into a **geometry-first discovery aperture**.

Instead of trying to derive geometry from leftover floating-point residue, use the known constraint geometry to generate candidate invariants, then ask whether BACL-filtered residue/lattice readback shadows those invariants.

The guiding question is:

```text
Does restraint curvature organize the selection of BACL-admissible lattice states?
```

The intended decomposition is:

```text
R = M ⊕ C ⊕ G
```

where:

```text
M = substrate-mandated lattice membership / availability.
C = conditioning amplification and stiffness response.
G = geometry-conditioned selection among BACL-admissible lattice states.
```

This is not a proof campaign yet. It is a structured discovery campaign to find and characterize C and G candidates.

---

## 1. Fixed context carried forward

Treat these as already established and do not relitigate them in this campaign.

### 1.1 BACL is M

BACL is the solved substrate law. It explains lawful integer-ULP lattice membership. It is consumed as the `M` filter.

Do not rediscover BACL. Do not treat M as a research target.

### 1.2 BACL does not select j

BACL says a residue lands on the admissible lattice. It does not determine which admissible lattice state/index is selected at a given route/fixture/point.

Therefore, the candidate G question is not:

```text
Is there lattice structure?
```

That is M-owned.

The candidate G question is:

```text
Which BACL-admissible lattice state is selected, and is that selection organized by geometry rather than only substrate or conditioning?
```

### 1.3 Discovery versus confirmation

Phases 0-2 are discovery and characterization. They may look, compare, prototype, rank, and discard. Do not impose pre-registered kill-switch logic in Phases 0-2.

Pre-registration returns only at Phase 3, after:

```text
at least one mechanism-bearing G candidate exists
AND
one positive C extractor exists
AND
normalization / grid / path-separation provenance is fixed
```

### 1.4 Active dual-arm lesson

A valid read is not independent resolution unless path/operand separation is recorded.

For any route-divergence or dual-readback observable, record:

```text
path identity
operand identity
operand offset
local lattice unit
offset level
separation class
```

A same-path or zero-offset read cannot promote to independent G evidence.

---

## 2. Campaign thesis

The campaign tests the discovery aperture:

```text
Use geometry to propose candidate G.
Use BACL to make the lattice readback lawful.
Use C to control amplification.
Then solve for whether geometric features organize BACL-admissible state selection.
```

The central candidate class is:

```text
G-curv: geometry-conditioned selection among BACL-admissible lattice states.
```

Examples:

```text
G-curv-1: Hessian/signature stratum organizes j-selection.
G-curv-2: principal-curvature ratio organizes route-pair phase state.
G-curv-3: null-tangent alignment event organizes transition grammar.
G-curv-4: lifted spectral family-tangent structure organizes BACL symbol sequences.
```

Do not claim any of these are true before characterization.

---

## 3. Lloyd tuple aperture

Represent each fixture as a Lloyd tuple:

```text
T = (
  constraint_family,
  physical_variables,
  family_parameters,
  route_bank,
  substrate_filter,
  curvature_readback,
  residue_readback,
  solve_for_target
)
```

### 3.1 Fields

`constraint_family`
: One or more constraints `F_i(x, θ) = 0`, or a fixture-specific equivalent already implemented in V4 eval modules.

`physical_variables`
: The variable vector `x` or scalar coordinate used by the fixture.

`family_parameters`
: A parameter `θ` or sweep coordinate. If a physical tangent is known, record it. If not, estimate only in discovery mode and mark provenance.

`route_bank`
: Algebraically equivalent arithmetic routes or fixture forms. Route identity must be recorded explicitly.

`substrate_filter`
: BACL lattice unit and BACL state/index readback.

`curvature_readback`
: Geometry-derived quantities such as Jacobian rank, Hessian signature, curvature ratios, lifted Hessian null vector, family-tangent alignment, spectral gaps, and condition metrics.

`residue_readback`
: BACL-normalized lattice state, j-sequence, route-pair symbol, phase offset, transition grammar, fingerprint slot, path/operand separation.

`solve_for_target`
: The candidate relation being explored between geometry features and substrate-filtered readback.

---

## 4. Key design principle: geometry proposes, residue audits

Do not start by asking which residue statistic looks interesting.

Start from geometric strata and ask how lattice-state selection behaves across those strata.

The first scout should ask:

```text
Do conditioning-resistant geometric strata organize BACL j-selection or route-pair symbol transitions after conditioning covariates are recorded?
```

Not:

```text
Does spectral gap predict j?
```

Spectral gap and condition number are likely C-covariates, not first G candidates.

---

## 5. Observable taxonomy

Every candidate observable must declare its family.

```text
value_magnitude
lattice_symbol
transition_grammar
route_pair_phase
fingerprint_slot
path_separation
spectral_geometry
curvature_stratum
conditioning_response
```

Rules:

```text
Magnitude that vanishes after M-subtraction is M-owned or anti-candidate.
Symbol structure that survives M-filtering remains eligible.
A route observable without path/operand separation telemetry is incomplete.
A geometry observable without conditioning covariates is C-confounded by default.
```

---

## 6. Normalization provenance requirement

Every lattice or phase readback must carry unit provenance.

Record:

```json
{
  "normalization_unit": "ulp(final_output) | ulp(rounding_step_operand) | ulp(control_coordinate)",
  "unit_source_value": "...",
  "unit_binade": "...",
  "route_stage": "final | intermediate | reverse | recomposed",
  "normalization_role": "readback | mechanism | control"
}
```

If two defensible normalizations exist, do not choose silently. Name both and run both as sibling observables.

Suggested sibling observables:

```text
J_final = residue normalized by final route-output ULP.
J_step  = residue normalized by natural ULP at the rounding step that produced it.
```

---

## 7. Candidate ledger states

Create a candidate ledger for every MCG observable.

Each candidate must have one current state:

```text
anti_candidate
M_owned
C_confounded
grid_artifact_candidate
normalization_unresolved
path_separation_unresolved
unexplained_correlation
unresolved_candidate
geometry_candidate
ready_for_phase3
```

Definitions:

`anti_candidate`
: Observable is structurally unsuitable or already known to be substrate-dominated.

`M_owned`
: Observable vanishes or is fully explained by BACL/M.

`C_confounded`
: Observable varies, but conditioning/stiffness covariates plausibly explain it.

`grid_artifact_candidate`
: Observable varies with grid family or binade sampling in a way that blocks geometric interpretation.

`normalization_unresolved`
: Competing ULP/normalization choices change the result.

`path_separation_unresolved`
: Route readback lacks path/operand separation telemetry.

`unexplained_correlation`
: Observable correlates with geometry but has no named mechanism.

`unresolved_candidate`
: Observable survives early filters but lacks enough evidence.

`geometry_candidate`
: Observable is organized by geometry, survives M/C/grid/path controls, and has a named mechanism.

`ready_for_phase3`
: Candidate has a named mechanism, positive C extractor exists, grid/normalization/path provenance is fixed, and a confirmatory test can be pre-registered.

---

## 8. Phase 0 — M contract and aperture setup

### Goal

Create a short working contract that defines what M explains and what remains eligible for C/G discovery.

### Deliverables

```text
Build_Docs/Reports/mcg_geometry_first/phase_0_m_contract.md
Build_Docs/Reports/mcg_geometry_first/candidate_ledger.json
```

### Required contents

`phase_0_m_contract.md` must state:

```text
BACL explains lattice membership / availability.
BACL does not explain which j is selected.
Magnitude-only residue collapse is M-owned unless symbolic structure remains.
G candidates must target selection/organization among BACL-admissible states.
C candidates must target conditioning amplification/stiffness.
```

`candidate_ledger.json` must initialize at least:

```text
G-curv-1: Hessian/signature stratum vs j-selection
G-curv-2: principal-curvature ratio vs route-pair phase
G-curv-3: null-tangent alignment vs transition grammar
G-route-1: path/operand-separated F1/F2 route-pair phase
C-def-1: finite-difference conditioning response
C-def-2: Jacobian/Hessian spectral response
C-def-3: perturbation amplification ladder
```

### Phase 0 exit

Exit when the M contract and candidate ledger exist. No scientific conclusion yet.

---

## 9. Phase 1 — Geometry readback table

### Goal

Build the geometry-side table that will generate candidate G strata.

### Fixtures

Start with existing V4 fixtures only. Do not invent new fixtures in Phase 1.

Suggested first fixtures:

```text
SR four-form fixture
Schwarzschild four-form fixture
Pure algebraic fixture if available
Lifted singularity audit fixtures if their code is available
```

Use whichever are available in the repo. Record unavailable fixtures explicitly.

### Geometry readback fields

For each point/context where available, compute or record:

```text
fixture_name
coordinate
route/context id
constraint id
J_rank
J_condition or condition proxy
Hessian signature
Hessian eigenvalue summary
principal-curvature ratio or curvature proxy
lifted Hessian null vector if applicable
family tangent if available
null-tangent alignment if applicable
spectral_gap
near-degenerate flag
geometry_stratum label
```

### Important warning

Treat these as C-covariates by default:

```text
J_condition
spectral_gap
smallest singular value
near-null eigenvalue magnitude
```

Treat these as first-pass G-strata candidates, but not proof:

```text
Hessian signature
curvature ratio class
null-tangent alignment event
closed-form geometry anchor
family-tangent class
```

### Deliverables

```text
Build_Docs/Reports/mcg_geometry_first/phase_1_geometry_table.json
Build_Docs/Reports/mcg_geometry_first/phase_1_geometry_characterization.md
```

### Phase 1 exit

Exit when the geometry table is created and geometry strata are characterized. No residue claim yet.

---

## 10. Phase 2 — BACL-filtered readback table

### Goal

Build the substrate-filtered readback table joined to the geometry table.

### Readback fields

For each matching point/route/context, compute:

```text
raw residual
BACL lattice unit
BACL j or lattice index
phase modulo 1
j_sequence context
route pair symbol, e.g. (j_A, j_B)
transition class
fingerprint/atlas slot if available
path identity
operand identity
operand delta
local lattice unit for operand delta
offset level
path separation class
normalization provenance
```

### Required path separation classes

```text
nonzero_operand_offset
zero_operand_offset
same_path_duplicate
path_distinct_operand_equal
separation_unobservable
separation_not_applicable
```

### Required normalizations

Run sibling normalization observables if possible:

```text
J_final
J_step
```

If only one can be computed, record why.

### Deliverables

```text
Build_Docs/Reports/mcg_geometry_first/phase_2_joined_readback_table.json
Build_Docs/Reports/mcg_geometry_first/phase_2_readback_characterization.md
```

### Phase 2 exit

Exit when geometry features and BACL-filtered readback are joined row-by-row. Still no confirmatory claim.

---

## 11. Phase 2b — C extractor scaffold

### Goal

Build a positive C profile so later G candidates are not just C in a nicer jacket.

### C profile fields

Start with a vector, not one scalar:

```text
J_condition
local Jacobian sensitivity
Hessian spectral spread
near-null spectral gap
finite-difference perturbation amplification slope
rank stability
null-direction stability
condition stratum
```

### Calibration ladder

Run C profile on:

```text
well-conditioned control
moderately conditioned fixture
near-singular / ill-conditioned fixture
exact-zero or calibration route if available
```

### C acceptance for discovery use

C-def is usable as a covariate when it shows a monotone or otherwise characterized response on known-conditioning fixtures.

Do not define C as everything not explained by M or G.

### Deliverables

```text
Build_Docs/Reports/mcg_geometry_first/phase_2b_c_profile.json
Build_Docs/Reports/mcg_geometry_first/phase_2b_c_characterization.md
```

---

## 12. Phase 2c — Grid and normalization stability checks

### Goal

Prevent G candidates from being grid-family or normalization artifacts.

### Grid families

If cheap and fixture supports it, compare:

```text
canonical grid
linear grid over same domain
log2/binade-spaced grid if relevant
deterministic jittered/stratified grid preserving endpoints and count
```

Do not force new grids into fixtures that have strict canonical-grid semantics without recording the change as exploratory.

### Stability questions

For each candidate observable, ask:

```text
Do dominant states persist?
Do transition grammars persist?
Does fixture ordering persist?
Does entropy range persist?
Does cross-binade fraction persist?
Does phase offset persist?
```

### Deliverables

```text
Build_Docs/Reports/mcg_geometry_first/phase_2c_grid_stability.json
Build_Docs/Reports/mcg_geometry_first/phase_2c_grid_stability.md
```

---

## 13. Phase 2d — Solve-for scout

### Goal

Use the V3 solve-for instinct in V4 form: solve for candidate relations between geometry strata and BACL-filtered selection states.

Do not solve over naked residuals. Solve over typed, BACL-filtered, provenance-recorded readbacks.

### Candidate relation families

Explore simple, interpretable relation families first:

```text
threshold relation
monotone relation
stratum lookup relation
phase-lock relation
transition-boundary relation
null/anti-null relation
no relation
```

### Inputs

Use:

```text
phase_1_geometry_table.json
phase_2_joined_readback_table.json
phase_2b_c_profile.json
phase_2c_grid_stability.json if available
```

### Output per candidate

Each candidate relation must report:

```text
candidate_id
geometry_feature
readback_feature
relation_family
conditioning covariates considered
normalization used
grid family used
fit/association summary
mechanism hypothesis
failure modes
ledger_state
```

### Promotion rules inside discovery

Promote to `geometry_candidate` only if:

```text
survives M filtering
not explained by C covariates in first-pass characterization
stable or characterized across grid family
normalization provenance fixed
path separation recorded if route-based
has a named mechanism
```

If correlation exists but no mechanism:

```text
ledger_state = unexplained_correlation
```

If C covariates dominate:

```text
ledger_state = C_confounded
```

If grid instability dominates:

```text
ledger_state = grid_artifact_candidate
```

### Deliverables

```text
Build_Docs/Reports/mcg_geometry_first/phase_2d_solve_for_scout.json
Build_Docs/Reports/mcg_geometry_first/phase_2d_candidate_characterization.md
Build_Docs/Reports/mcg_geometry_first/candidate_ledger_updated.json
```

---

## 14. Phase 3 — First confirmatory separation probe, gated

Do not implement Phase 3 until Phase 2d produces at least one `ready_for_phase3` candidate.

### Entry gate

Phase 3 may start only if all are true:

```text
1. M/BACL filter applied.
2. Candidate survives as non-M structure.
3. Candidate has a named mechanism.
4. Positive C extractor exists and C-confound is characterized.
5. Grid stability is characterized.
6. Normalization provenance is fixed.
7. Path/operand separation is recorded if route-based.
8. Candidate ledger marks it ready_for_phase3.
```

### Phase 3 mode

This is where pre-registration returns.

Create:

```text
Build_Docs/Reports/mcg_geometry_first/phase_3_preregistry.md
```

Only then run the confirmatory test.

### Phase 3 question

For a single candidate:

```text
Are M, C, and candidate G separable or entangled on a chosen fixture/control set?
```

### Phase 3 outcomes

```text
G_separable_supported
G_C_entangled
G_M_owned_after_hardening
G_grid_artifact_after_hardening
G_normalization_unstable
G_path_separation_failed
G_not_supported
```

---

## 15. Phase 4 — Unification question, gated

Do not start Phase 4 unless Phase 3 supports at least one separable G candidate.

Question:

```text
Is M ⊕ C ⊕ G the substrate shadow of D ⊕ S = P?
```

This is the original ambition, placed last.

---

## 16. Required report style

For Phases 0-2:

```text
Use discovery/characterization language.
No pass/fail headline except for implementation checks.
No kill-switch language.
No severity language for routine negative results.
No “confirmed G” claim.
```

Allowed discovery states:

```text
candidate
anti_candidate
M_owned
C_confounded
grid_artifact_candidate
normalization_unresolved
path_separation_unresolved
unexplained_correlation
geometry_candidate
ready_for_phase3
```

For Phase 3+:

```text
Use pre-registered confirmatory decision language.
```

---

## 17. Anti-claims and banned promotion language

Do not claim:

```text
MCG decomposition proven.
G discovered.
Double precision.
Half-ULP resolution.
Geometry extracted from residue.
C solved.
D⊕S=P substrate shadow confirmed.
```

Allowed if supported:

```text
candidate geometry-conditioned BACL state selection
candidate route-pair phase structure
candidate curvature-indexed transition grammar
C-confounded structure
M-owned observable
unexplained correlation
ready-for-Phase-3 candidate
```

---

## 18. Minimal implementation sequence for Claude Code

### Task A — Phase 0 contract and ledger

Create:

```text
Build_Docs/Reports/mcg_geometry_first/phase_0_m_contract.md
Build_Docs/Reports/mcg_geometry_first/candidate_ledger.json
```

No code beyond static report/ledger generation unless needed.

### Task B — Geometry table builder

Create an eval-layer module if needed:

```text
src/lloyd_v4/evals/mcg_geometry_first_geometry.py
```

Create:

```text
phase_1_geometry_table.json
phase_1_geometry_characterization.md
```

### Task C — BACL readback joiner

Create an eval-layer module if needed:

```text
src/lloyd_v4/evals/mcg_geometry_first_readback.py
```

Create:

```text
phase_2_joined_readback_table.json
phase_2_readback_characterization.md
```

### Task D — C profile scaffold

Create:

```text
phase_2b_c_profile.json
phase_2b_c_characterization.md
```

### Task E — Grid/normalization stability

Create:

```text
phase_2c_grid_stability.json
phase_2c_grid_stability.md
```

### Task F — Solve-for scout

Create:

```text
phase_2d_solve_for_scout.json
phase_2d_candidate_characterization.md
candidate_ledger_updated.json
```

Stop here unless a candidate reaches `ready_for_phase3`.

---

## 19. Testing requirements

Add focused tests only for implementation correctness and artifact schema, not scientific confirmation.

Suggested tests:

```text
phase 0 ledger contains required candidate ids
geometry table emits required fields
readback table emits BACL unit and normalization provenance
route candidates emit path separation fields
zero/same-path route cannot be marked independent
C profile emits vector fields, not a single catch-all scalar
grid stability output records all attempted grid families
solve-for scout cannot promote unexplained correlation to ready_for_phase3
candidate ledger states are from allowed set
reports are generated deterministically / byte-stably where practical
```

Run the smallest reasonable existing subset covering:

```text
fixture imports
eval module imports
artifact schema
no manifest/status/primitives changed
```

Report exact commands in each closeout.

---

## 20. Expected first useful outcomes

The most valuable early outcomes are likely not positives. Good early results include:

```text
Observable X is M-owned.
Observable Y is C-confounded.
Observable Z is grid-artifact candidate.
Observable W is normalization-unresolved.
Route-pair candidate R requires nonzero path/operand separation.
Geometry feature H organizes j-selection only after excluding high-condition points.
```

These are not failures. They sharpen the aperture.

---

## 21. One-sentence campaign summary

MCG Geometry-First asks whether restraint curvature organizes the selection of BACL-admissible lattice states, with BACL as M, conditioning as C, and geometry-conditioned state selection as the candidate G.
