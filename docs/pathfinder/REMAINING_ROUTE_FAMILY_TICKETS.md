# Pathfinder remaining build tickets

**Status date:** 2026-07-12
**Current state:** general kernel + 39 registered route families; all gates closed

## PF-M2-002 — Performance-discriminating structured ideal fixture

**Status: completed (2026-07-11).** The recorded sixteen-contact stage-2 workload is frozen in `benchmarks/CONTACT_ORBIT_FIXTURE.md`. Thirty cache-isolated pairs measured a 2.04594x marginal median speedup including certificate replay and a 1.00969x cold end-to-end median speedup.

## PF-M2-003 — Resident-host diagnostic adapter

**Status: open (diagnostic only).** A resident-session M2 adapter measuring deployment-shaped marginal cost remains future diagnostic work; it cannot replace the frozen cold-process release protocol.

## PF-PLAN-002 — Generic elimination contract

**Status: completed (2026-07-12).** `generic_elimination` is registered in `recognize/elimination.py` as a typed admissible comparison candidate with explicit scope, burden, and certificate obligations. The M2 wrapper lifts it (`_lift_generic_elimination_route`) and refuses loudly when the selected route cannot be lifted; no silent fallback exists (see `tests/gate_pathfinder_m2_wrapper.py`, updated assertions).

## PF-COMPAT-002 — Typed prototype adapters

**Status: substantially completed (2026-07-12).** Typed request/evidence/candidate objects carry residual fingerprints (`ir/fingerprint.py`), conservative rewrite recognition (`recognize/rewrite.py` + `scout/expression.py`), and Pareto comparison with loser records (`plan/compare.py`). The legacy dictionary surface remains available through `pathfinder.compat` and all characterization/MCP gates close through it. Remaining: retiring the legacy encoder entirely once MCP callers migrate.

## PF-ALG-001 — Triangular and direct-substitution recognizers

**Status: completed (2026-07-12).** `recognize/triangular.py`: `direct_substitution`, `triangular_domain_tower`, `linear_inverse_ring_map`, with hypotheses/source references and no polynomial execution services exposed.

## PF-ALG-002 — Complete-intersection and degree-balance recognizers

**Status: completed (2026-07-12).** `recognize/complete_intersection.py`: `regular_sequence_complete_intersection` (fresh-variable monic certificate, v1.3 §11.7) and `degree_balance_closure`, with positive/wrong-scope/missing-hypothesis/mutation fixtures in `tests/gate_pathfinder_providers_algebra.py`.

## PF-KUMMER-001 — Kummer finite-extension route

**Status: completed (2026-07-12).** `recognize/kummer.py`: `kummer_finite_extension_primeness` implements the private-prime lemma (squarefree gcd + pairwise-coprime constants); the M2 wrapper lifts it and `tests/gate_pathfinder_m2_extended.py` executes and certifies the rotating IZ fixture externally (codim 6, degree 64 replay).

## PF-COVER-001 — Wreath and branch/inertia route family

**Status: completed (2026-07-12).** `recognize/wreath.py` (conjugate-module wreath lift, rotating three-channel closure, self-glue exponent/gcd), `recognize/cover.py` (normalization-aware cover, structured incidence projection, generic-open boundary split), `recognize/inertia_strata.py` (branch/inertia stratification, collision-partition inertia) — one theorem family at a time, each with citations and hostile fixtures.

## PF-REAL-001 — Exact-real and local-geometry families

**Status: completed (2026-07-12).** `recognize/real.py` (invariant-floor, Sturm escalation, matrix-pencil selection, exact rational inertia) and `recognize/local_germ.py` (local metric germ, parity-fixed face, extremal face, Newton-wedge corner) with explicit refusal strata; native Sturm/Newton/inertia scouts in `scout/`.

## PF-REALIZE-001 — Lazy realization-poset planner

**Status: completed (2026-07-12).** `recognize/realization.py`: `lazy_realization_poset` returns the dependency-aware node/edge route with boundary and multiplicity records; realization execution and certificates remain external.

## Genuine mathematical gaps

See `docs/pathfinder/GAP_LEDGER.md` — eight entries, each naming the exact missing native method and corpus location; all are carried as explicit refusal strata or exceptional branches in the corresponding contracts.
