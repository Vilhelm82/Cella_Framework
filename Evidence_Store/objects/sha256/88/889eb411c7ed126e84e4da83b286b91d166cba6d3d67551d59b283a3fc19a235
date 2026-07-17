# codex_task041_structural_cancellation_analyzer

## Repository

`/home/william_lloydlt/projects/V4/Lloyd_Engine_V4` (Lloyd Engine V4 main tree).

Clean-room enforcement: V1 / V3 source must not be imported, called, adapted, or bridged at runtime (Axiom 10). V3 reference evidence is permitted only as committed fixtures or copied test data.

## Current Verified Baseline

State at task commit, in `main`:

- All layers green through task036. `directional_alpha_probe` companion-call integration with `sweep_signature_probe` shipped.
- `evals/refinery_mvp/` provides `BurdenVector` (per-(fixture, path) campaign-aggregated burden), `check_geometry_admissibility`, and `compare_burden_vectors` for Pareto-style ranking of algebraically-equivalent rewrites. **This infrastructure is empirical only**: it requires completed campaign reports before comparison.
- `evals/sterbenz_audit/` provides `rewrite_candidates.py` (generates candidate forms), `measurement_extension.py` (runs candidates through campaigns), and `n_way_pareto.py` (multi-candidate comparison). Also empirical only.
- BACL (Bit-Aligned Cancellation Lattice) is referenced in `evals/substrate_invariant_search_phase_g.py` and sibling phase docs, but exists as a *theoretical framework* without a runtime primitive that walks expression trees and predicts burden symbolically.
- **Empirical motivation**: scratch-folder exploration of Schwarzschild and Kerr ISCO observables (scratch/isco_alpha_recovery_extended.py, scratch/kerr_extremal_alpha_recovery.py, scratch/isco_pathological_cleaner.py, scratch/isco_pathological_minimal.py) iterated three rounds to determine which algebraic formulations are catastrophic and which are not. Specifically:
  - `outer_stable` (algebraically simplified): clean
  - `outer_naive` (Sterbenz-safe subtraction at end): clean — Sterbenz exact, signal O(√ε)
  - `r_+² − 36` form (difference-of-squares cancellation): clean — Sterbenz exact, signal O(√ε)
  - `(12+ε)² − 144` form (apparent cancellation): catastrophic at ε ~ 10⁻¹³ — Sterbenz exact, **but signal O(ε)**
  - `outer_pathological` (original, with safety-net early-return): catastrophic at ε ~ 10⁻¹² — synthesised zeros propagate
  - These four rounds of empirical testing could have been collapsed to a single symbolic analysis if the predictive primitive existed.
- **The methodological gap**: V4 currently detects pathology *after* running it. The natural BACL-aligned move is to predict pathology *before* running, by walking the expression tree and classifying each cancellation site.

Full suite green at HEAD: required.

## Task Goal

Introduce `structural_cancellation_analyzer` as a Layer 2 `evals` primitive that walks a typed expression tree (constructed via a small DSL), classifies each subtraction node by its cancellation pattern, and emits a typed `PredictedBurdenVector` compatible with the existing `evals/refinery_mvp/BurdenVector`. 

**Architectural decision (v1 baseline, ratified after scratch-prototype validation in scratch/symbolic_analyzer_mvp.py and scratch/symbolic_analyzer_v2.py)**: the analyzer treats the expression DSL as an *executable graph*, not just a syntactic tree. Signal-after-cancellation scaling is derived by *sample-evaluating* each subtraction's operands at a small number of probe points within the declared sweep range, then extracting the constant baseline and the perturbation's log-log exponent and leading coefficient from those samples. This eliminates the v1 limitation of earlier designs where 'buried constants' (constants emerging via composition through divisions, multiplications, or unary operations) could not be detected by pure AST pattern matching.

The analyzer's pattern vocabulary therefore collapses to a small set of cells whose membership is determined by sample-evaluation outcomes rather than by AST shape matching alone. This positions Lloyd Geometric Diagnostics with a forward-looking capability: predict pathological formulations before running them, complementary to the existing empirical detection.

## Design Principles

1. **Axiom 1 (geometry precedes scalarization).** The analyzer's output is a structured `PredictedBurdenVector` with named fields, not a single scalar "burden score."
2. **Axiom 3 (no hidden guard rails).** Cancellation classification rules (constant-cancellation detection, Sterbenz-zone check, signal-scaling-class extraction via sample-evaluation) are declared with explicit calibration parameters (probe-point count, exponent rounding to clean fractions, constant-equality tolerance). No buried tolerances.
3. **Axiom 4 (multi-field validity).** Distinct status cells per analyzed expression: `analysis_complete`, `analysis_partial_unrecognised_present`, `analysis_unsupported_construct`, `analysis_refused_missing_annotation`. Each represents distinct evidence about why the analysis succeeded or did not.
4. **Axiom 8 (typed composition).** The analyzer emits via `STRUCTURAL_CANCELLATION_ANALYZER_PROTOCOL` (ProducerProtocol). The output `PredictedBurdenVector` is consumable by `compare_burden_vectors` (the existing Pareto comparator from `refinery_mvp`), enabling symbolic-vs-empirical comparison.
5. **Axiom 11 (epistemic stance).** No imports of forbidden mathematical content. The analyzer uses Python `ast` (stdlib) if AST extraction is supported, the `fractions` module (stdlib) for clean exponent representation, and our own typed arithmetic DSL. NO sympy, NO mpmath, NO symbolic computer algebra system. Sample-evaluation uses substrate-permitted numerical operations (the same primitives V4 uses elsewhere) — no foreign mathematical content imported.
6. **Axiom 12 (self-derivation).** The DSL types (Variable, Constant, BinaryOp, UnaryOp) and the sample-evaluation routine compose at the analyzer's own layer using core typed-result envelopes. No new mathematical content beyond evaluation and log-log slope extraction.
7. **Sample-evaluation, not pattern matching against AST shapes.** The analyzer probes each subtraction's operands at log-spaced sweep values within the declared range. From the resulting (sweep_value, function_value) tuples it extracts the constant baseline (limit as sweep → 0 if convergent) and the perturbation's log-log exponent. This handles buried constants correctly *by construction*, including the `r_+² − 36` form, the `r_+ − 6` Sterbenz-safe form, and arbitrary deeper compositions. The analyzer's pattern vocabulary is therefore minimal — see Design Principle 8.
8. **Minimal pattern vocabulary.** Only five cells: `NO_SUBTRACTION` (no cancellation site), `SELF_CANCELLATION` (operands structurally identical), `STERBENZ_SAFE_BENIGN` (operands share a constant baseline; sampled signal exponent < 1), `STERBENZ_SAFE_CATASTROPHIC` (operands share a constant baseline; sampled signal exponent ≥ 1), and `UNRECOGNISED` (sample-evaluation failed or produced inconclusive evidence). No special-case shapes (difference-of-squares, derivative-pattern, etc.) — they all collapse into the sample-evaluated cells.
9. **Calibration against empirical reality.** The analyzer's output for the four canonical ISCO outer forms and at least four additional calibration cases (a Kerr observable, a synthetic pure-power-law, a Sterbenz-with-O(ε)-signal synthetic, and a known-pathological-with-safety-net synthetic) must match the empirical Pareto ordering measured by V4's existing primitives.
10. **Conservative defaults.** When sample-evaluation produces fewer than three convergent probe points, or when log-log slope fit's r² is below threshold (0.8 by default), the site emits `UNRECOGNISED` rather than guessing. Better to refuse than to give a wrong prediction.
11. **Composes with empirical refinery, doesn't replace it.** The analyzer is a fast pre-filter. Empirical campaigns remain the final arbiter for cases the analyzer cannot resolve. Specifically: when the analyzer predicts "clean" for all candidates, the refinery_mvp can skip running them. When the analyzer predicts "one form dominates," the refinery still runs to verify. When the analyzer is uncertain, the refinery runs everything.
12. **Probe-point selection is declared.** The sample-evaluation routine accepts an explicit `n_samples` parameter (default 5) and probes at log-spaced values across the full declared sweep range. No hidden adaptive logic. If the caller wants more probe points, they pass them explicitly.

## Primitive-Sufficiency Gate

| Concept needed | Provided by | Parent layer |
|---|---|---|
| AST walking and pattern matching | Python `ast` (stdlib, permitted under Axiom 11 as substrate not mathematical content) | n/a (stdlib) |
| Typed result envelope, validity, conditioning, provenance | `TypedResult`, `Validity`, `Conditioning`, `Provenance` | `core` |
| Producer protocol declaration | `ProducerProtocol` | `core` |
| Status enum convention | `core.status` (new family `StructuralCancellationStatus`) | `core` |
| `BurdenVector` dataclass for output compatibility | `evals/refinery_mvp/BurdenVector` | `evals` |
| Pattern-matching primitives (recognising AST shapes) | new operations in this task, classified as Layer 2 evals operations | this task |
| Magnitude-scaling-class tracking (constant, O(eps), O(sqrt(eps)), etc.) | new typed enum in this task | this task |

**Halt condition: none.** All concepts available. The DSL and pattern-classification logic are *new operations at the evals layer*, but they're built from `core` envelopes plus the existing `BurdenVector` output type. No parent-layer extension required.

## Required Deliverables

### Source files

1. `src/lloyd_v4/evals/symbolic_analysis/__init__.py` — package init exposing the analyzer's public API.

2. `src/lloyd_v4/evals/symbolic_analysis/expression_dsl.py` — the small typed-arithmetic DSL:
   - `@dataclass(frozen=True) class Variable`: fields `name: str`, `sweep_range_low: float`, `sweep_range_high: float`. Represents a sweep variable with declared range. NOTE: `expected_scaling` is NOT required — sample-evaluation derives scaling empirically.
   - `@dataclass(frozen=True) class Constant`: field `value: float`. Wraps a constant.
   - `@dataclass(frozen=True) class BinaryOp`: fields `op: BinaryOpKind` (enum: ADD, SUB, MUL, DIV), `left: Node`, `right: Node`.
   - `@dataclass(frozen=True) class UnaryOp`: fields `op: UnaryOpKind` (enum: SQRT, NEG, plus minimal extension as needed for calibration set: POW with Fraction exponent for cube-root and other rational powers; ACOS if the Kerr photon sphere is in the calibration set), `operand: Node`.
   - `Node` type alias: `Variable | Constant | BinaryOp | UnaryOp`.
   - DSL ergonomic helpers: `add(a, b)`, `sub(a, b)`, `mul(a, b)`, `div(a, b)`, `sqrtN(a)`, `neg(a)`, `pow_node(a, exp: Fraction)`, etc. that auto-wrap numeric arguments in `Constant`.

3. `src/lloyd_v4/evals/symbolic_analysis/sample_probe.py` — the executable-graph evaluation core:
   - `evaluate_node(node: Node, env: dict[str, float]) -> float` — recursively evaluates the AST.
   - `@dataclass(frozen=True) class SampledProfile` with fields: `constant_part: float`, `perturbation_exponent: Fraction`, `perturbation_coefficient: float`, `samples: tuple[tuple[float, float], ...]`, `is_pure_perturbation: bool`, `fit_r_squared: float`.
   - `sample_profile(node: Node, sweep_var: Variable, n_samples: int = 5) -> SampledProfile` — probes the expression at `n_samples` log-spaced sweep values, extracts constant baseline and log-log perturbation fit.
   - `_round_to_clean_fraction(x: float) -> Fraction` — rounds an extracted slope to nearest clean rational (1, 1/2, 1/3, 2/3, 1, 4/3, 3/2, 5/3, 2, 5/2, 3, 4 are the v1 candidates).

4. `src/lloyd_v4/evals/symbolic_analysis/pattern_classifiers.py` — the minimal classifier:
   - `classify_subtraction(node: BinaryOp, sweep_var: Variable, n_samples: int = 5) -> CancellationSite`. Returns one of five cells (NO_SUBTRACTION, SELF_CANCELLATION, STERBENZ_SAFE_BENIGN, STERBENZ_SAFE_CATASTROPHIC, UNRECOGNISED) based on:
     - Self-cancellation check (structural equality of operands)
     - Sample-evaluation of both operands and the subtraction itself
     - Constant-equality check (operands share a non-zero baseline within tolerance)
     - Signal-exponent threshold (≥ 1 → catastrophic; < 1 → benign)
   - `_structural_equal(a: Node, b: Node) -> bool` — strict structural equality.
   - `_predicted_crossing_eps(constant_magnitude, signal_exponent, signal_coefficient) -> float | None` — first-crossing formula `(ε_machine · |C| / coef)^(1/p)`.

5. `src/lloyd_v4/evals/symbolic_analysis/structural_cancellation_analyzer.py` — the main analyzer:
   - `analyze_expression(root: Node, sweep_variable: Variable, n_samples: int = 5) -> PredictedBurdenResult`
   - Walks the expression tree (via `walk_and_classify`), classifies each subtraction node, aggregates results.
   - Returns a `PredictedBurdenResult = TypedResult[PredictedBurdenVector, StructuralCancellationStatus]`.
   - `STRUCTURAL_CANCELLATION_ANALYZER_PROTOCOL: Final[ProducerProtocol]` declaring emitted statuses.

6. `src/lloyd_v4/evals/symbolic_analysis/predicted_burden_vector.py` — the output dataclasses:
   - `@dataclass(frozen=True, slots=True) class PredictedBurdenVector` with fields:
     - `n_catastrophic: int`
     - `n_sterbenz_safe_benign: int`
     - `n_self_cancellations: int`
     - `n_benign_subtractions: int`
     - `n_unrecognised: int`
     - `predicted_precision_crossing_epsilon: float | None` (largest crossing across all sites — worst-case dominant)
     - `cancellation_sites: tuple[CancellationSite, ...]` (per-site detail)
     - `expression_label: str`
     - `sweep_variable_name: str`
     - `sweep_variable_range: tuple[float, float]`
   - `@dataclass(frozen=True, slots=True) class CancellationSite` with fields:
     - `pattern: CancellationPattern`
     - `signal_exponent: Fraction`
     - `signal_coefficient: float`
     - `constant_magnitude: float`
     - `predicted_crossing_eps: float | None`
     - `description: str`
     - `location_hint: str` (AST path)

7. `src/lloyd_v4/core/status.py` — add `StructuralCancellationStatus` enum with cells:
   - `analysis_complete` — every subtraction in the expression was classified, no UNRECOGNISED cells, no UNSUPPORTED constructs
   - `analysis_partial_unrecognised_present` — analysis completed but at least one subtraction emitted UNRECOGNISED (sample-eval inconclusive)
   - `analysis_refused_missing_annotation` — caller did not declare sweep-variable range
   - `analysis_unsupported_construct` — expression contains a node type the analyzer does not handle

### Bridge to existing refinery_mvp

7. `src/lloyd_v4/evals/refinery_mvp/symbolic_to_empirical_bridge.py` — bridge that converts `PredictedBurdenVector` to the existing `BurdenVector` shape for Pareto comparison. Maps:
   - `n_catastrophic_cancellations` → contributes to a predicted `b_k_point_estimate` modifier
   - `predicted_precision_crossing_epsilon` → contributes to `operation_chain_depth`-equivalent
   - `cancellation_sites` → contributes to `provenance` field of the existing `BurdenVector`
   - Returns a `BurdenVector` instance with provenance noting it came from symbolic analysis (not from campaign measurements). Consumers can mix symbolic and empirical burden vectors in `compare_burden_vectors`.

### Documentation

8. `Build_Docs/Architecture/LAYER_MANIFEST.md` + `layer_manifest.json` — add the new `evals/symbolic_analysis/` package to the manifest. Declare its provided concepts (analyzer operation, DSL types, pattern classifiers) and parents (`core`, `evals/refinery_mvp`).

9. `Build_Docs/Architecture/STATUS_CALCULUS.md` — new section "Structural cancellation analysis strata" with the four cells listed above, and the declared precedence: `analysis_refused_missing_annotation → analysis_unsupported_construct → analysis_partial_unrecognised_present → analysis_complete`.

10. `Build_Docs/V4_GLOSSARY.md` — new entries: `MagnitudeClass`, `CancellationPattern`, `PredictedBurdenVector`, `CancellationSite`, `structural_cancellation_analyzer`. Plus an "architecturally complementary pair" entry: **`PredictedBurdenVector` (evals/symbolic_analysis layer, symbolic pre-prediction) vs `BurdenVector` (evals/refinery_mvp layer, empirical campaign aggregation) — both feed `compare_burden_vectors` for Pareto ranking; symbolic is fast and conservative, empirical is slow and authoritative.**

11. `Build_Docs/LIVE_CAMPAIGNS_LEDGER.md` — new entry: `structural_cancellation_analyzer` campaign. Last touched at commit date, last result "task041 commit", next concrete step "task042 (extend pattern vocabulary: derivative-pattern, log-singularity, trigonometric-boundary)".

12. `Build_Docs/Reports/task041_structural_cancellation_analyzer_summary.md` — top-level summary. Required contents:
    - Deliverable manifest (file paths, line counts)
    - Test counts (collected, passed, regression-suite delta)
    - **The canonical calibration table**: the four ISCO outer forms (`outer_stable`, `outer_naive`, `r_+² − 36`, `(12+ε)² − 144`) analysed symbolically. Each form's predicted `PredictedBurdenVector` is shown alongside the empirical V4 measurement from scratch. The predicted Pareto ordering must match the empirical Pareto ordering.
    - Coverage gaps explicitly documented: which patterns the v1 analyzer handles vs which it cannot (deferred to task042+).

13. `Build_Docs/Reports/task041_structural_cancellation_analyzer/` directory with:
    - `calibration_script.py` — runs the analyzer on the four ISCO forms and produces the side-by-side prediction/empirical table.
    - `calibration_observations.json` — structured outputs.
    - `calibration_observations.md` — narrative.

## Required Tests

| Test file | What it verifies |
|---|---|
| `tests/test_task041_source_purity.py` | No V3 imports, no forbidden mathematical content per Axiom 11 (especially no sympy, no mpmath, no scipy). |
| `tests/test_task041_dsl_construction.py` | Variable / Constant / BinaryOp / UnaryOp construct correctly; immutability; frozen-dataclass invariants. |
| `tests/test_task041_sample_probe.py` | `sample_profile` correctly extracts constant baseline and perturbation exponent for: (a) pure power law `lambda eps: eps**0.5` → constant=0, exponent=1/2; (b) constant-plus-perturbation `lambda eps: 1 + 2*eps` → constant=1, exponent=1; (c) constant-only `lambda eps: 7.5` → constant=7.5, is_pure_perturbation=False, exponent ≈ 0. Log-log slope fit r² is ≥ 0.99 for clean cases. |
| `tests/test_task041_pattern_classifiers.py` | Each pattern classifier returns the correct CancellationPattern for hand-constructed test cases: `(c + ε) − c` → STERBENZ_SAFE_BENIGN with signal exponent 1 → wait, this is actually catastrophic by our threshold; verify the classifier returns STERBENZ_SAFE_CATASTROPHIC; `r_+ − 6` (constant 6 emerges via sample-eval, signal O(√ε)) → STERBENZ_SAFE_BENIGN; `r_+² − 36` (constant 36 via sample-eval, signal O(√ε)) → STERBENZ_SAFE_BENIGN; `(12+ε)² − 144` (constant 144 via sample-eval, signal O(ε)) → STERBENZ_SAFE_CATASTROPHIC; `x - x` → SELF_CANCELLATION. |
| `tests/test_task041_isco_canonical_calibration.py` | The four ISCO outer forms analysed by the full analyzer produce the expected Pareto ordering: outer_stable (no subtractions) dominates outer_naive ≈ r_+² − 36 form (STERBENZ_SAFE_BENIGN, signal O(√ε), predicted crossing well below the sweep range) dominate `(12+ε)² − 144` form (STERBENZ_SAFE_CATASTROPHIC, signal O(ε), predicted crossing ~ 10⁻¹⁵). The predicted crossings must match the empirical crossings (measured in scratch) within one order of magnitude. The leading coefficient extracted by sample-eval for `outer_naive` must match √3 ≈ 1.73 within 5%, for `r_+² − 36` form must match 12√3 ≈ 20.8 within 5%, and for `(12+ε)² − 144` form must match 24 within 1%. |
| `tests/test_task041_extended_calibration.py` | Four additional calibration cases beyond ISCO: (a) Kerr photon sphere `r_ph(1-δ) - 1` → STERBENZ_SAFE_BENIGN with signal O(√δ), leading coef matching 2√6/3 ≈ 1.633 within 5%; (b) synthetic pure power law `lambda eps: eps**(1/3)` → NO_SUBTRACTION, constant_part=0; (c) synthetic catastrophic `lambda eps: (1+eps) - 1` → STERBENZ_SAFE_CATASTROPHIC with predicted crossing ~ ε_machine; (d) synthetic clean Sterbenz `lambda eps: (1+sqrt(eps)) - 1` → STERBENZ_SAFE_BENIGN with predicted crossing ~ ε_machine². |
| `tests/test_task041_bridge_to_burden_vector.py` | The symbolic-to-empirical bridge produces valid `BurdenVector` instances that are consumable by `compare_burden_vectors`. Pareto comparison of a symbolic vs an empirical burden vector for the same form yields consistent verdicts (within documented divergence margins). |
| `tests/test_task041_serialization.py` | `to_json_safe` round-trip preserves all `PredictedBurdenVector` fields including the nested `CancellationSite` tuple. |
| `tests/test_task041_protocol_compatibility.py` | `STRUCTURAL_CANCELLATION_ANALYZER_PROTOCOL` emits the declared status family; protocol violation raises `ProtocolViolationError`. |
| `tests/test_task041_layer_manifest.py` | Manifest tests pass with the new evals subpackage registered. |

## Required Commands

```bash
# Red slice (before implementation)
pytest tests/test_task041_*.py --collect-only

# Implementation slice (red -> green)
pytest tests/test_task041_*.py -x

# Backwards-compatibility check
pytest tests/test_task030_*.py -v  # refinery_mvp not regressed
pytest tests/test_task031_*.py -v  # sterbenz_audit not regressed
pytest tests/test_task035_*.py -v  # sweep_signature_probe not regressed
pytest tests/test_task036_*.py -v  # alpha-probe companion not regressed

# Full suite (no regressions)
pytest tests/

# Source audit
pytest tests/test_task041_source_purity.py -v
grep -RE "^(import|from) (sympy|mpmath|scipy|numpy)" src/lloyd_v4/evals/symbolic_analysis/

# Manifest audit
pytest tests/test_task010a_layer_manifest_machine_readable.py
pytest tests/test_task010b_*.py

# Lineage audit
pytest tests/test_task010c_*.py
```

## Non-Goals

- **Full symbolic algebra system.** No general equation solving, no algebraic simplification, no symbolic differentiation. The analyzer recognises a fixed vocabulary of patterns; expressions not matching its vocabulary emit `UNRECOGNISED` and downstream consumers fall back to empirical measurement.
- **Automatic AST extraction from Python lambdas.** The caller constructs the expression tree explicitly using the DSL types. `inspect.getsource()` + `ast.parse()` from a lambda is a future capability (task043 perhaps) but requires handling closures, function calls, etc. Out of scope here.
- **Nonlinear-primitive boundary analysis.** `sqrt` near 0, `log` near 1, `arccos` near ±1 have singular behaviour that this analyzer treats coarsely (as magnitude classes). Fine-grained boundary analysis is a follow-up task.
- **Floor-proximate prediction.** Predicting which observables would emit `sweep_signature_floor_proximate` from task035's deferred status cell is a separate capability and depends on task038 landing first.
- **Replacing the empirical refinery.** The analyzer is a fast pre-filter. The empirical refinery (`refinery_mvp` + `sterbenz_audit`) remains the authoritative ranking when the analyzer is uncertain or when calibration evidence is needed.
- **Multi-variable sweep analysis.** Task041 supports a single declared sweep variable. Multi-variable (e.g., (ε, η) jointly) is deferred.
- **Integration with `directional_alpha_probe` or `sweep_signature_probe`.** Those primitives continue to operate empirically. A future task can add an optional `predicted_burden` companion field to their results, mirroring task036's companion-call pattern.
- **task037, task038, task039 scope changes.** Those follow-up tasks are still planned independently. Task041 informs their motivation but does not subsume them.

## Completion Report

`Build_Docs/Reports/task041_structural_cancellation_analyzer_summary.md` (top-level headline) plus `Build_Docs/Reports/task041_structural_cancellation_analyzer/` (calibration sub-artifacts).

## Acceptance Criteria

1. All required source files exist at declared paths; all task041 tests pass via `pytest tests/test_task041_*.py -x`.
2. Full test suite green at task close (no regressions; same 1101+ collection plus new task041 tests).
3. `pytest tests/test_task030_*.py`, `pytest tests/test_task031_*.py`, `pytest tests/test_task035_*.py`, `pytest tests/test_task036_*.py` pass unchanged.
4. `pytest tests/test_task010a_layer_manifest_machine_readable.py` passes — new evals subpackage registered correctly.
5. `pytest tests/test_task041_source_purity.py` passes — no forbidden imports, especially no sympy, mpmath, scipy, numpy.
6. `pytest tests/test_task010c_*.py` passes — lineage corpus updated.
7. **The canonical calibration on the four ISCO outer forms** produces this exact Pareto ordering:
   - `outer_stable`: PredictedBurdenVector with `n_catastrophic_cancellations = 0`, `predicted_precision_crossing_epsilon = None`
   - `outer_naive`: PredictedBurdenVector with `n_catastrophic_cancellations = 0`, `n_sterbenz_safe_cancellations = 1`, `predicted_precision_crossing_epsilon = None`
   - `r_+² − 36`: PredictedBurdenVector with `n_catastrophic_cancellations = 0`, `n_sterbenz_safe_cancellations = 1` (the difference-of-squares pattern), `predicted_precision_crossing_epsilon` between 10⁻²² and 10⁻¹⁸
   - `(12+ε)² − 144`: PredictedBurdenVector with `n_catastrophic_cancellations = 1` (CATASTROPHIC_LINEAR_SIGNAL), `predicted_precision_crossing_epsilon` between 10⁻¹⁴ and 10⁻¹²
8. **Cross-check with empirical evidence**: each predicted-crossing-epsilon matches the empirical value (measured by V4's existing primitives in scratch) within one order of magnitude. The closeout summary documents the comparison side-by-side.
9. The bridge to `BurdenVector` produces instances that `compare_burden_vectors` accepts and ranks consistently with the symbolic Pareto ordering.
10. **Magnitude-class tracking is correct for all hand-tested operator combinations** (no longer applicable in v2 — magnitude tracking has been replaced by sample-evaluation; the equivalent check is that `sample_profile` extracts the correct constant baseline and perturbation exponent for the curated test cases in `tests/test_task041_sample_probe.py`).
11. `analysis_unsupported_construct` and `analysis_partial_unrecognised_present` fire correctly for hand-crafted out-of-vocabulary expressions; analyzer does NOT silently produce incorrect predictions when faced with unrecognised patterns.

---

**Pre-registration committed prior to implementation. Re-evaluate scope and acceptance criteria against this document only after task close.**

**Task ordering rationale**: Task041 lands BEFORE task039 (typed_log_log_slope residual statistics) because it changes the motivation for several follow-up tasks. With symbolic burden prediction available, the residual-rms field becomes valuable not just for sweep_signature_probe but for cross-validating the symbolic analyzer (empirical residual_rms should track symbolic predicted-precision-crossing). Task037 (sterbenz_audit pre-screen) gains an additional gating stage: symbolic pre-screen first, then sweep_signature pre-screen, then full empirical campaign.

**Updated subsequent-task roadmap**:
- **task041** (this task): structural cancellation analyzer
- **task042**: pattern-vocabulary extension (derivative-pattern, log-singularity, trig-boundary)
- **task037**: sterbenz_audit pre-screen with symbolic + sweep_signature pre-screens
- **task039**: typed_log_log_slope residual statistics (now also serves cross-validation of task041)
- **task038**: floor_proximate primitive
- **task040**: sweep_signature_probe discriminator upgrade
- **task043** (conditional): AST extraction from Python lambdas via `inspect.getsource()` for ergonomic caller API
- **task044** (deferred): multi-variable sweep analysis
