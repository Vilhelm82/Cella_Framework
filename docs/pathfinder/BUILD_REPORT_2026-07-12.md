# Pathfinder build report — 2026-07-12

**Authority:** `CODEX_PATHFINDER_FINISH_TONIGHT_HANDOFF.md` (finish the full v1.3 build)
**Prior state:** typed core with exactly two contact providers and one M2 fixture
**Result:** wrapper-independent kernel + 39 registered route families + generalized M2 wrapper; all gates closed

## 1. What was implemented

### Kernel (wrapper-independent, `src/cella/pathfinder/`)

| Component | Files | Content |
|---|---|---|
| Canonical task IR | `ir/expression.py`, `ir/polynomial.py`, `ir/problem.py` | Bounded exact expression shadow (AST → typed nodes, Fraction constants, budget-enforced); sparse polynomial shadow (exact expansion, monic/fresh-variable/weighted-degree/unit-leading detection, term budget); `NormalizedProblem` lowering (rings, ideals, strata, symmetry, cover, roles) with stable SHA-256 hashing |
| Structural fingerprint engine | `ir/fingerprint.py` | One typed record per request: algebraic shape, cancellation, scale class, factor/dependency, elimination shape, CI indicators, strata, symmetry/orbit, role/channel/carrier, cover/Kummer/wreath, local-germ, realization-poset axes; canonical id + provenance |
| Scout engine | `scout/` (10 modules) | Non-verdict probes: F2 rank/kernel, fresh-variable monic scan (v1.3 §11.7), triangular tower, weighted degree balance, sign-orbit completeness, self-glue trinomial gcd, expression cancellation shape, congruence-pivot rational inertia (1×1/2×2 pivots), Kummer parity matrix, DBP regularity q=gᵀg, exact Sturm chains, Newton corner vertices/support function |
| Provider registry + comparison | `plan/registry.py`, `plan/admissibility.py`, `plan/compare.py`, `plan/assemble.py`, `plan/select.py` | `RouteProvider` (contract + recognizer + native scouts + wrapper capabilities); shared admissibility helpers; deterministic comparison with invariant floor → structural preference → Pareto dominance → declared tie-break, recording WHY every loser lost (`RouteRejection`); `plan_request` enriches evidence via provider scouts and attaches the fingerprint |
| Compat boundary | `compat/__init__.py` | Legacy `route_plan` / `rewrite_candidates` / `pathfinder_compare` preserved behind the typed facade |

### Route families (39 registered; `recognize/`, one theorem family at a time, all cited)

- **Contact (pre-existing, preserved):** contact_restriction, signed_contact_orbit_projection
- **Prototype/rewrite:** symbolic_collapse_rewrite
- **Structural algebra:** direct_substitution, triangular_domain_tower, linear_inverse_ring_map, regular_sequence_complete_intersection, degree_balance_closure, generic_elimination (PF-PLAN-002 comparison candidate), localization_boundary_split, ordinary_host_computation
- **Algebra services:** finite_algebra_multiplication_matrix, factorization_shaped, modular_groebner_reconstruction
- **Kummer:** kummer_square_class_independence, valuation_parity_lower_bound, rotating_kummer_rank_jump, kummer_finite_extension_primeness (P4 / rotating IZ)
- **Wreath/cover:** conjugate_module_wreath_lift, rotating_three_channel_wreath_closure, self_glue_exponent_gcd, normalization_aware_cover, structured_incidence_projection, generic_open_boundary_split
- **Inertia strata:** branch_inertia_stratification, collision_partition_inertia
- **DBP curvature:** canonical_invariant_reduction, dbp_role_orbit_reduction, curvature_role_orbit, gauge_channel_transport
- **Local geometry:** local_metric_germ, parity_fixed_face, extremal_face, newton_wedge_corner
- **Exact real:** invariant_floor_real, sturm_escalation, matrix_pencil_selection, exact_rational_inertia
- **Realization:** lazy_realization_poset

Every provider: recognition predicate, required evidence, native scout, admissibility conditions, preserved-invariant declaration, burden vector, route assembler, wrapper capability requirements, and refusal conditions for mathematically invalid input (never for missing implementation). The silent-criterion nuance is enforced (rank-deficient parity matrices refuse `parity_rank_inconclusive` without claiming disproof).

### M2 wrapper (separate package, `tools/pathfinder_m2/`)

- `LIFTERS` registry dispatch: contact_restriction, signed_contact_orbit_projection, generic_elimination, kummer_finite_extension_primeness; unknown families refuse loudly (no silent fallback).
- New task lowerings: `M2GenericEliminationTask` (arbitrary declared-ring elimination; wrapper owns `**` → `^` syntax translation) and `M2DifferenceIdealPrimenessTask` (rotating IZ primeness).
- Capability advertisement (`capabilities.py`): 15 M2 primitives + liftable families.
- Route-only mode (`certified=False`) preserved across all lifters.

## 2. Tests and benchmark results

All gates pass (2026-07-12):

| Gate | Result |
|---|---|
| `gate_pathfinder_typed_core` | CLOSED |
| `gate_pathfinder_prototype_characterization` | CLOSED |
| `gate_pathfinder_kernel_units` (new, 30+ checks) | CLOSED |
| `gate_pathfinder_mock_host` (new; wrapper independence, byte-determinism, order-noise immunity, boundary law) | CLOSED |
| `gate_pathfinder_providers_algebra` (79 checks) | CLOSED |
| `gate_pathfinder_providers_services` (57 checks) | CLOSED |
| `gate_pathfinder_providers_kummer` (129 checks) | CLOSED |
| `gate_pathfinder_providers_geometry` (121 checks) | CLOSED |
| `gate_mcp_pathfinder`, `gate_mcp_pathfinder_improved_spec` | CLOSED |
| `gate_pathfinder_m2_wrapper` (real M2; assertions updated for the registered generic candidate — documented in-file) | CLOSED |
| `gate_pathfinder_m2_extended` (new; real M2, two non-contact fixtures with exact baseline equivalence + certificate replay) | CLOSED |
| `gate_pathfinder_hostile_benchmark` | CLOSED |

Exact corpus retrodictions verified natively: static parity rank 10 and rotating rank 15; Kummer kernel bases; keystone channel triple anchor (K = −1/5625 at jet (5,7,2,3,4)); parity-fixed −m(m+5)/B with m=2 → −14; lead7 Sturm gate H̃ root count 0 on (1,∞); KN Newton corner A = −84 with balanced support 2; Lorentzian (2,1) signature of 2I−J.

Benchmarks: the frozen isolated signed-contact release benchmark was re-run in full AFTER the build (fresh alternating cold M2 processes, no cross-arm caches; `benchmarks/results/CONTACT_ORBIT_ISOLATED_BENCHMARK.*`, 2026-07-12):

- marginal median speedup **95% CI [1.996, 2.068]x** including certificate replay, Pathfinder faster in 30/30 isolated pairs, exact sign-test p = 1.86e-09;
- cold end-to-end median speedup 95% CI [1.0059, 1.0146]x, sign-test p = 1.4e-03;
- result equivalence: both routes independently equal all sixteen declared wall ideals;
- certificate status: triangular-presentation replay closed in every trial.

The paired confidence interval for time saved is strictly above zero with exact result equality on every trial — the performance law of the handoff is satisfied on the admitted target class.

## 3. Remaining genuine mathematical gaps

Eight entries, each with the exact missing native method and corpus location: `docs/pathfinder/GAP_LEDGER.md`. All are carried as explicit refusal strata or exceptional branches in the corresponding provider contracts.

## 4. Files changed

New kernel: `src/cella/pathfinder/ir/{expression,polynomial,problem,fingerprint}.py`, `scout/` (11 files), `plan/{admissibility,compare,assemble}.py`, `compat/__init__.py`; rewritten: `plan/{registry,select}.py`, `recognize/__init__.py`, package `__init__.py`.
New providers: `recognize/{rewrite,triangular,complete_intersection,elimination,finite_extension,modular_groebner,realization,kummer,wreath,cover,inertia_strata,curvature,local_germ,real}.py` (14 modules, 37 families).
M2 wrapper: `tools/pathfinder_m2/cella_pathfinder_m2/{wrapper,model,__init__}.py` extended; `capabilities.py` new.
Tests: `tests/gate_pathfinder_{kernel_units,mock_host,m2_extended}.py` new; `tests/gate_pathfinder_providers_{algebra,services,kummer,geometry}.py` new; `tests/gate_pathfinder_m2_wrapper.py` assertions evolved (documented).
Docs: `docs/pathfinder/{GAP_LEDGER.md,BUILD_REPORT_2026-07-12.md}` new; `REMAINING_ROUTE_FAMILY_TICKETS.md` statuses updated.

## 5. Reproduction command

```bash
cd "/home/wlloyd/Cella Framework"
# Complete test suite (kernel, providers, boundary, M2 integration):
for g in tests/gate_pathfinder_typed_core.py \
         tests/gate_pathfinder_prototype_characterization.py \
         tests/gate_pathfinder_kernel_units.py \
         tests/gate_pathfinder_mock_host.py \
         tests/gate_pathfinder_providers_algebra.py \
         tests/gate_pathfinder_providers_services.py \
         tests/gate_pathfinder_providers_kummer.py \
         tests/gate_pathfinder_providers_geometry.py \
         tests/gate_mcp_pathfinder.py \
         tests/gate_mcp_pathfinder_improved_spec.py \
         tests/gate_pathfinder_m2_wrapper.py \
         tests/gate_pathfinder_m2_extended.py \
         tests/gate_pathfinder_hostile_benchmark.py; do python "$g" || exit 1; done
# Isolated cache-clean release benchmark (fresh alternating M2 processes):
PYTHONPATH=src:tools/pathfinder_m2 python -m cella_pathfinder_m2.contact_orbit_isolated_benchmark
```

## 6. Boundary attestations

- No CAS, FLINT, GMP, CUDA, or external oracle inside `src/cella/pathfinder/`.
- No `predicted_duration` field anywhere in the public contract (gate-checked).
- Pathfinder returns routes only; certificate obligations are emitted, never discharged, inside the core (gate-checked).
- The contact-orbit provider is one provider among 39.
