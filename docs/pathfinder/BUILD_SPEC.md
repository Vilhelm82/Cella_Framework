# Pathfinder corrected build specification

**Version:** 0.1 implementation baseline  
**Authority:** `campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md`  
**Behavioral reference:** characterized `src/cella/_legacy_pathfinder.py`, formerly `src/cella/pathfinder.py`  
**Boundary:** route discovery and selection only

## Product contract

Pathfinder lowers wrapper-neutral task metadata into a route-analysis IR, gathers bounded non-verdict-bearing scout evidence, recognizes explicit route families, rejects inadmissible candidates, compares the remaining candidates by invariant sufficiency and evidenced burden, and returns one deterministic `ComputationalRoute`.

It never executes the requested mathematical deliverable and never returns the final answer. Host wrappers preserve external object identities. Execution and certificate modules consume the returned route after Pathfinder stops.

```text
host task -> wrapper lowering -> PathfinderRequest
          -> scouts/recognizers -> admissible RouteCandidate set
          -> Pareto/declared tie-break selection -> ComputationalRoute
          -> host execution -> external certification -> host result
```

## Public typed objects

### `PathfinderRequest`

Required fields:

```text
request_id
target_obligation
external_binding
mathematical_context
available_route_families
supplied_scout_evidence
already_discharged_obligations
analysis_budget
```

`external_binding` is opaque to Pathfinder except for stable key lookup. The wrapper owns its semantics and variable identities.

### `ScoutEvidence`

Required fields:

```text
scout_family
scope
structural_fingerprint
actual_trace
burden_vector
stability
unresolved_inputs
retained_artifact_refs
```

Evidence can support route admissibility but cannot assert that the host deliverable has been proved or computed.

### `RouteContract`

Required fields:

```text
route_family
accepted_problem_shape
required_hypotheses
required_evidence
produced_obligations
discharged_obligations
exceptional_branches
execution_module
certificate_obligations
```

Every recognizer cites its theorem/source and emits unmet hypotheses explicitly.

### `ComputationalRoute`

Required fields:

```text
request_id
target_obligation
route_family
ordered_steps
data_dependencies
external_binding
required_intermediate_objects
required_hypotheses
certificate_obligations
exceptional_branches
completion_condition
supporting_scout_evidence
```

Forbidden fields include a final mathematical result, fabricated proof status, and `predicted_duration_ns` or equivalent wall-clock guesses.

## Selection law

Selection is deterministic and ordered:

1. Reject candidates outside declared scope or with unmet hypotheses/evidence.
2. Reject candidates that do not discharge the target obligation.
3. Prefer the lowest sufficient invariant level.
4. Prefer a direct structural route over general search when warrants match.
5. Prefer local, tower, or symmetry routes over global expansion when hypotheses hold.
6. Compare actual scout burden vectors using Pareto dominance.
7. Apply a stable declared route-family tie-break only to the remaining frontier.

The prototype's declared-grid equivalence and BACL/residual/depth comparator remain compatibility behavior. A predicted burden is mathematical/computational structure, not predicted elapsed time.

## First registered structural route

`contact_restriction` recognizes a signed contact component whose explicit substitutions reduce a target polynomial before projection. For benchmark `m2-even-contact-delta-slice-a-v1`, admissibility requires:

```text
sign_product = +1
characteristic != 2
declared exact slice N1=4, N2=8, N3=12, N4=20
target generator is delta from the bound model
```

It returns ordered instructions to apply contact substitutions, retain the reduced generator `J^2` with multiplicity, apply the exact slice, and solve the linear contact wall. It does not construct the M2 ideal.

The external certificate obligations are:

```text
contact substitutions satisfy IX
delta + 16*J^2 vanishes modulo Ceven
Ceven + IZ + sliceA equals the structural upstairs ideal
the structural base ideal equals the baseline eliminated ideal
J^2 is retained rather than replaced by J
```

The exact M2 equivalence gate is `benchmarks/pathfinder_m2/gate_even_contact_equivalence.m2`.

## Package migration

The former single-file `cella.pathfinder` module is a tested public surface. Migration to the package layout is staged:

1. freeze its behavior with characterization tests;
2. move the implementation behind a package facade that re-exports `route_plan`, `rewrite_candidates`, and `pathfinder_compare` unchanged;
3. introduce typed IR and canonical serialization beside that facade;
4. adapt legacy dictionaries to typed requests/routes;
5. add recognizers incrementally, beginning with `contact_restriction`;
6. remove the compatibility implementation only after every existing gate and MCP caller uses the typed core.

No M2 syntax, subprocess control, final reconstruction, or certificate implementation enters `src/cella/pathfinder/`.

## Release gates

A route family is releasable only when:

- typed serialization is byte-deterministic;
- unsupported or incomplete scope is an explicit refusal;
- the host baseline and selected route produce the same exact deliverable;
- the certificate path is external and replayable;
- the full wrapped median time includes lowering, analysis, execution, certification, replay, and lifting;
- at least seven measured post-warm-up trials show `T_total < T_baseline`.

No performance claim is made by this specification or by the current M2 algebra-equivalence fixture.
