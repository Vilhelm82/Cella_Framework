# Cella Hostile Benchmark Campaign Design

Date: 2026-07-08

## Goal

Build a hostile benchmark campaign that tests the Pathfinder thesis rather than
the MCP wrapper layer: Cella should identify cleaner computational routes before
SymPy, mpmath, Arb/FLINT, or unguided Cella walk into expression swell,
cancellation, precision escalation, or global-form traps.

## Architecture

Pathfinder is treated as an internal mathematical substrate. The benchmark may
call internal route functions and existing Cella primitives directly for trace
capture, but it must not frame Pathfinder as a user-facing MCP tool.

Each benchmark case is manifest-driven. The runner executes the same case across
declared engines:

- `cella_pathfinder`: Cella primitives with Pathfinder route metadata enabled.
- `cella_direct`: Cella primitives without route metadata where applicable.
- `sympy_naive`: direct symbolic parse/simplify/count path.
- `mpmath_naive`: direct numeric evaluation where applicable.
- `flint_arb`: optional baseline, reported as unavailable when the Python
  binding is absent.

The runner records raw JSON artifacts, route traces, and a summary of wins,
losses, and limits. A Cella win requires correct result or correct typed
refusal, an early route decision, and lower burden or cleaner telemetry than the
conventional baseline. A failure is any silent overclaim, wrong result, missing
route, or global expansion where a local normal form is available.

## MVP Case Families

### Arithmetic Cancellation

Cases include constant-offset collapse, square-root conjugates,
difference-of-squares, unresolved `cos(eps)-1`, and mixed chains where only some
sites are rewriteable. These cases test whether Pathfinder classifies the
operation before asking for precision.

### Symbolic Swell

Cases include rational functions and DBP-style coefficient forms where the
desired result is a compact normal-form route or exact rational-function record,
not expanded global algebra.

### Local Geometry

Cases include PFC parity-fixed faces, generic quadratic collapse, master-quadric
exponent vectors, and codimension-2 Newton wedges. These test whether Cella
routes to local germs instead of assembling scalar-curvature monsters.

### DBP Channel and Carrier

Cases include c001 Stage C pin/move, `g_i=0, q!=0` regularity, `q=0`
singularity, `K_G^2` versus channel-norm square, and the `n=5` scalar-spectrum
threshold. These test the latest authority hierarchy and channel semantics.

### High-Precision Period/Residue

The first MVP may record this family as a limit if no small deterministic
fixture is wired. The campaign must still reserve the lane because it is part of
the replacement-arithmetic thesis.

## Required Artifacts

- `benchmarks/pathfinder_hostile/manifest.json`: frozen case manifest.
- `src/cella/hostile_benchmark.py`: manifest runner and engine adapters.
- `tests/gate_pathfinder_hostile_benchmark.py`: deterministic MVP gate.
- `reports/pathfinder_hostile/*.json`: generated run records.

## Success Criteria

- The MVP benchmark runs from a single command with no network dependency.
- The manifest contains real Cella/DBP/PFC/arithmetic cases, not only toy
  wrapper checks.
- Results distinguish `pass`, `fail`, `limit`, and `unavailable`.
- Conventional baselines are honest: if SymPy/mpmath/FLINT are unavailable or a
  case is not applicable, the record says so.
- The summary explicitly separates demonstrated wins from remaining gaps.
- Existing MCP gates continue to pass.

