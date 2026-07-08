# Cella Hostile Benchmark Campaign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a manifest-driven hostile benchmark that measures whether internal Cella Pathfinder routing improves real arithmetic, symbolic, DBP, and local-geometry workflows over direct Cella and conventional baselines.

**Architecture:** Add a focused benchmark runner that lives outside the MCP surface. The runner loads a JSON manifest, dispatches cases to internal Cella route/primitives and optional SymPy/mpmath/FLINT baselines, then writes raw JSON reports with pass/fail/limit/unavailable statuses.

**Tech Stack:** Python standard library, existing `src/cella` modules, optional SymPy/mpmath/FLINT imports when available.

---

### Task 1: MVP Hostile Manifest

**Files:**
- Create: `benchmarks/pathfinder_hostile/manifest.json`
- Test: `tests/gate_pathfinder_hostile_benchmark.py`

- [ ] **Step 1: Write the failing test**

Create `tests/gate_pathfinder_hostile_benchmark.py` with imports from `cella.hostile_benchmark`, a manifest load check, and assertions that arithmetic, local-geometry, DBP, symbolic, and period/residue families are present.

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src python tests/gate_pathfinder_hostile_benchmark.py`

Expected: import failure because `cella.hostile_benchmark` does not exist.

- [ ] **Step 3: Add the manifest**

Create a JSON manifest with cases:

- `arith_constant_offset`
- `arith_sqrt_conjugate`
- `arith_unresolved_cos`
- `symbolic_rational_normal_form`
- `pfc_parity_fixed`
- `pfc_corner_wedge`
- `dbp_stage_c_channel_predicate`
- `dbp_regular_gi_zero`
- `dbp_n5_carrier_required`
- `period_residue_lane_reserved`

- [ ] **Step 4: Re-run test**

Expected: still fails until the runner exists.

### Task 2: Runner and Engine Adapters

**Files:**
- Create: `src/cella/hostile_benchmark.py`
- Test: `tests/gate_pathfinder_hostile_benchmark.py`

- [ ] **Step 1: Implement manifest loading**

Add `load_manifest(path)` and validate required fields: `campaign`, `version`, `cases`.

- [ ] **Step 2: Implement Cella Pathfinder adapter**

Add `run_cella_pathfinder(case)` that uses `route_plan`, `diag_germ_classifier`, `corner_frontface`, and `symbolic_rational` based on each case family.

- [ ] **Step 3: Implement direct and conventional adapters**

Add `run_cella_direct(case)`, `run_sympy_naive(case)`, `run_mpmath_naive(case)`, and `run_flint_arb(case)`. Optional dependencies must return `unavailable` rather than raising.

- [ ] **Step 4: Implement summary logic**

Add `run_manifest(manifest_path, output_path=None)` and summary counts for `pass`, `fail`, `limit`, and `unavailable`.

- [ ] **Step 5: Re-run the gate**

Run: `PYTHONPATH=src python tests/gate_pathfinder_hostile_benchmark.py`

Expected: manifest loads, runner produces JSON, MVP route assertions pass.

### Task 3: Reports and Regression

**Files:**
- Create runtime output: `reports/pathfinder_hostile/mvp-report.json`
- Test: existing gates

- [ ] **Step 1: Run the hostile benchmark**

Run: `PYTHONPATH=src python -m cella.hostile_benchmark --manifest benchmarks/pathfinder_hostile/manifest.json --output reports/pathfinder_hostile/mvp-report.json`

Expected: report JSON is written and summary has no `fail` statuses for the Cella Pathfinder engine.

- [ ] **Step 2: Run existing gates**

Run:

```bash
PYTHONPATH=src python tests/gate_pathfinder_hostile_benchmark.py
PYTHONPATH=src python tests/gate_mcp_pathfinder.py
PYTHONPATH=src python tests/gate_mcp_campaign.py
PYTHONPATH=src python tests/gate_mcp.py
```

Expected: all gates close.

### Self-Review

- Spec coverage: the plan covers manifest, internal runner, optional baselines, raw reports, and gate verification.
- Placeholder scan: no placeholder implementation steps; the MVP case ids are explicit.
- Type consistency: manifest path, report path, and runner function names are consistent across tasks.

