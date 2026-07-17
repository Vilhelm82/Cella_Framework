# codex_task039_typed_log_log_slope_residual_statistics

## Repository

`/home/william_lloydlt/projects/V4/Lloyd_Engine_V4` (Lloyd Engine V4 main tree).

Clean-room enforcement: V1 / V3 source must not be imported, called, adapted, or bridged at runtime (Axiom 10). V3 reference evidence is permitted only as committed fixtures or copied test data.

## Current Verified Baseline

State at task commit, in `main`:

- All layers green through task036. `directional_alpha_probe` companion-call integration with `sweep_signature_probe` is shipped and exercised.
- `typed_log_log_slope` exposes `LogLogSlopeObservation` with fields: `slope`, `intercept`, `r_squared`, `standard_error`, `n_input_observations`, `n_used`, `log_f_min`, `log_f_max`, `expression_path`. Residuals are computed internally to derive `standard_error` but are not exposed.
- `sweep_signature_probe` (task035) uses `cancellation_grade = 1 - r_squared` as its cancellation discriminator. This is scale-invariant but has a known failure mode: for genuinely flat observables (true slope ≈ 0), r² → 0 even when the formulation is clean and residuals are at machine precision. The screen mis-classifies flat-clean as cancellation-burdened.
- **Empirical motivation**: Kerr ISCO_retrograde near-extremality investigation (scratch/kerr_extremal_alpha_recovery.py) found this exact failure mode. The observable 9 − r_ISCO_retro(1−δ) ≈ (45/16)·δ has α = 1 (linear). `directional_alpha_probe` correctly recovered α = 0.973 ± 0.013. `sweep_signature_probe` flagged it as `sweep_signature_cancellation_dominated` with `cancellation_grade = 0.805`, even though the underlying transfers were computed cleanly. The cancellation_grade reading was driven by `1 − r²` being high because the log-log fit is genuinely flat, not because of noise. This is a false positive of the screening tool.
- A clean fix exists: `typed_log_log_slope` already computes per-point residuals during the fit (these enter the `standard_error` calculation). Exposing residual statistics as additional fields on `LogLogSlopeObservation` enables consumers to use scale-aware cancellation discriminators. In log-transfer space, residuals are dimensionless — `residual_rms` near machine epsilon means a clean fit regardless of slope value.

Full suite green at HEAD: required.

## Task Goal

Extend `LogLogSlopeObservation` with residual statistics fields, populated by `typed_log_log_slope` from quantities it already computes internally. Add no new computation beyond aggregation of existing per-point residuals. Do NOT modify `sweep_signature_probe`, `directional_alpha_probe`, or any other downstream consumer — those become follow-up tasks. Task039 is strictly the parent-primitive extension that unblocks future consumer-side improvements.

## Design Principles

1. **Axiom 5 + Axiom 8 (backwards compatibility).** Existing consumers see no behavioural or schema change beyond additional fields with documented defaults. The numerical values of `slope`, `intercept`, `r_squared`, `standard_error`, etc., are bit-identical to pre-task039 output for the same input.
2. **Axiom 3 (no hidden guard rails).** The new fields expose statistics that already exist in the computation; they do not introduce new thresholds or policies. Threshold-based interpretation of these statistics is the consumer's job, not this primitive's.
3. **Axiom 12 (self-derivation).** All new field values are computed from quantities already produced during the regression. No new mathematical content beyond elementary aggregation.
4. **Axiom 11 (epistemic stance).** No new imports of forbidden mathematical content. `math` permitted for `sqrt`, `isfinite` (same usage profile as the existing primitive).
5. **Residuals in log-transfer space.** All residual fields are measured in the same space the slope fit operates on — log-transfer vs log-f. This is dimensionless (log of a ratio is dimensionless), making the statistics scale-invariant in the sense consumers want. A `residual_rms` near `1e-15` indicates float64-precision-floor fit quality; a `residual_rms` near `0.1` indicates significant fit noise.
6. **Status emission unchanged.** `typed_log_log_slope` continues to emit `SlopeStatus.SLOPE_OBSERVED`, `SLOPE_INSUFFICIENT_DATA`, `SLOPE_DEGENERATE_INPUT`. The new fields are populated only when status is `SLOPE_OBSERVED` (when no fit is performed, the fields default to `None` for the same reasons `standard_error` already defaults to `None`).
7. **Field consistency discipline.** Like the existing `nested_window_fits` pattern in `AlphaProbeObservation`, the new residual fields are jointly populated (all non-`None`) or jointly absent (all `None`). `__post_init__` enforces this.
8. **No new status cells.** No new entries in `SlopeStatus`. The residual statistics are descriptive, not classifying.

## Primitive-Sufficiency Gate

| Concept needed | Provided by | Parent layer |
|---|---|---|
| Per-point regression residuals during slope fit | already computed internally in `typed_log_log_slope` for `standard_error` derivation | `primitives` |
| Square root and sum operations for rms aggregation | substrate arithmetic (allowed per Axiom 11) | n/a |
| Max-absolute aggregation | substrate (built-in `max`) | n/a |
| Dataclass field addition with `None` defaults | existing pattern (`nested_window_fits` etc. in `AlphaProbeObservation`) | `primitives` |
| Existing `LogLogSlopeObservation` and `LogLogSlopeResult` types | `typed_log_log_slope` | `primitives` |

**Halt condition: none.** All concepts available; no parent-layer extension required.

## Required Deliverables

### Modified source files

1. `src/lloyd_v4/primitives/typed_log_log_slope.py`:
   - Add three new fields to `LogLogSlopeObservation`, each with `None` default:
     - `residual_rms: float | None = None` — root-mean-square of regression residuals in log-transfer space. Defined as `sqrt(sum(r_i²) / (n_used − 2))` where r_i = log|transfer_i| − (slope·log(f_i) + intercept). The (n − 2) denominator matches the convention used in the existing `standard_error` derivation (degrees of freedom for two-parameter linear regression). Returns `None` when status ≠ `SLOPE_OBSERVED` or when `n_used` < 3.
     - `residual_max_abs: float | None = None` — maximum absolute residual: `max(|r_i|)`. Returns `None` when status ≠ `SLOPE_OBSERVED` or when no residuals are computed.
     - `residual_relative_rms: float | None = None` — scale-normalised version. Defined as `residual_rms / max(|log|transfer_i|| for i)` when the denominator is non-zero, else `None`. This gives a dimensionless "fraction of typical log-magnitude" metric useful for cross-scale comparisons.
   - Update the fit-path code that already computes per-point residuals (for `standard_error`) to additionally compute these three statistics and pass them into the `LogLogSlopeObservation` constructor.
   - Update `__post_init__`: the three residual fields are jointly populated or jointly absent. Mixed states raise `ValueError` with a message naming which field is inconsistent. The three fields are also jointly populated iff `standard_error` is populated (same emission criterion). Joint inconsistency between the residual-trio and `standard_error` raises `ValueError`.
   - Update `to_json_safe()` to include the three new fields under keys `residual_rms`, `residual_max_abs`, `residual_relative_rms`.

2. `src/lloyd_v4/primitives/__init__.py`:
   - No new exports required. The existing `LogLogSlopeObservation` export now carries the optional fields automatically.

### Documentation

3. `Build_Docs/Architecture/LAYER_MANIFEST.md` + `layer_manifest.json` — if the machine-readable manifest carries a field-level shape spec for `LogLogSlopeObservation`, add the three new fields. If the manifest only lists exports, no change required.

4. `Build_Docs/Architecture/STATUS_CALCULUS.md` — no change (no new status cells introduced).

5. `Build_Docs/V4_GLOSSARY.md` — new entries:
   - `residual_rms`: definition, log-transfer-space convention, n−2 denominator, return-`None` rules.
   - `residual_max_abs`: definition, scale convention.
   - `residual_relative_rms`: definition, scale-normalisation rationale.
   - Plus a cross-reference under the existing `r_squared` entry noting that residual statistics provide a complementary view that is robust to slope magnitude: r² confuses flat-with-noisy in flat-slope regimes; residual_rms does not.

6. `Build_Docs/LIVE_CAMPAIGNS_LEDGER.md` — new entry: `typed_log_log_slope_residual_statistics` campaign, last touched at commit date, last result "task039 commit", next concrete step "task040 (sweep_signature_probe cancellation discriminator upgrade using residual_rms — currently sweep_signature_probe uses 1 − r² and exhibits flat-observable false positives, documented in Kerr retrograde scratch/kerr_extremal_alpha_recovery.py)".

7. `Build_Docs/Reports/task039_typed_log_log_slope_residual_statistics_summary.md` — top-level summary. Required contents:
   - Deliverable manifest (line counts; mostly small additions to one source file plus tests)
   - Test counts (collected, passed, regression-suite delta)
   - Demonstration table: re-run a representative subset of the task035 GR-photon-sphere calibration with task039 residual statistics populated, showing the cleanly-separated `residual_rms` values for clean (≈ machine precision) versus cancellation-dominated (significantly above precision floor) cases.
   - Specific demonstration of the motivating Kerr retrograde case: run the observable `9 - r_ISCO_retro(1-delta)` and report `residual_rms` (expected near machine precision because the linear fit is genuinely clean) alongside `r²` (expected low because the slope is near 0). This is the concrete artefact that demonstrates why the new fields enable the future sweep_signature_probe upgrade.

8. `Build_Docs/Reports/task039_typed_log_log_slope_residual_statistics/` directory with:
   - `demonstration_script.py` — reproducible runner that produces the Kerr-retrograde comparison
   - `demonstration_observations.json` — structured outputs
   - `demonstration_observations.md` — narrative

## Required Tests

| Test file | What it verifies |
|---|---|
| `tests/test_task039_source_purity.py` | No V3 imports, no forbidden mathematical content per Axiom 11. |
| `tests/test_task039_typed_log_log_slope_residuals.py` | (a) For status = `SLOPE_OBSERVED`, all three residual fields are populated with finite floats. (b) For status ≠ `SLOPE_OBSERVED`, all three residual fields are `None`. (c) `residual_rms` matches an independent reference computation: `sqrt(sum(r_i²) / (n_used − 2))` for a hand-crafted dataset with known residuals. (d) `residual_max_abs` matches `max(|r_i|)`. (e) `residual_relative_rms` matches the documented quotient. (f) For a clean power-law observable (e.g., `lambda f: f**2`) sampled cleanly, `residual_rms < 1e-13` (machine-precision-floor evidence). (g) For a synthetic noisy observable (`lambda f: f**2 + numpy-free random noise added in a deterministic way`) of known noise amplitude, `residual_rms` recovers that amplitude within ~10%. (h) For a constant-slope-zero observable (`lambda f: 1.0`), the slope status is `SLOPE_DEGENERATE_INPUT` and all residual fields are `None`. |
| `tests/test_task039_kerr_retrograde_demonstration.py` | Specific real-world fixture: the Kerr ISCO retrograde observable `9 - r_ISCO_retro(1-delta)` sampled on a representative grid. Asserts that `r_squared < 0.5` (low because slope ≈ 0) AND `residual_rms < 1e-10` (clean because the formulation is genuinely smooth). This documents the failure mode of the existing r²-based discriminator and demonstrates that `residual_rms` correctly classifies the same case as well-formulated. |
| `tests/test_task039_serialization.py` | `to_json_safe` round-trip preserves all three new fields. Both populated and `None` states preserved. |
| `tests/test_task039_post_init_validation.py` | `__post_init__` enforces joint population/absence of the residual trio, AND joint consistency with `standard_error`. Constructing `LogLogSlopeObservation` with mixed states raises `ValueError`. |
| `tests/test_task039_layer_manifest.py` | If manifest carries field-level spec for `LogLogSlopeObservation`, the new fields are correctly registered. |

## Required Commands

```bash
# Red slice (before implementation)
pytest tests/test_task039_*.py --collect-only

# Implementation slice (red -> green)
pytest tests/test_task039_*.py -x

# Backwards-compatibility check (existing typed_log_log_slope tests must still pass unchanged)
pytest tests/test_task016_*.py -v
pytest tests/test_task017c_*.py -v

# Backwards-compatibility for downstream consumers
pytest tests/test_task018_directional_alpha_probe.py -v
pytest tests/test_task035_*.py -v
pytest tests/test_task036_*.py -v

# Full suite (no regressions)
pytest tests/

# Source audit
pytest tests/test_task039_source_purity.py -v
grep -RE "^(import|from) (cmath|numpy|scipy|sympy|mpmath)" src/lloyd_v4/primitives/typed_log_log_slope.py

# Manifest audit
pytest tests/test_task010a_layer_manifest_machine_readable.py
pytest tests/test_task010b_*.py

# Lineage audit
pytest tests/test_task010c_*.py
```

All eleven commands must pass for completion.

## Non-Goals

- **Modify `sweep_signature_probe`'s discriminator.** Switching `cancellation_grade` from `1 − r_squared` to a residual-based metric is a follow-up task (task040). Task039 only exposes the building blocks.
- **Modify `directional_alpha_probe`.** The alpha probe's status emissions and field set are unchanged. It can read the new `LogLogSlopeObservation` fields if it wants, but it doesn't have to.
- **Modify `scalar_alpha_jet_bundle` or `singular_alpha_jet_bundle`.** These consume `directional_alpha_probe` and don't touch slope observations directly.
- **New status family.** No `SlopeStatus` additions. The residual statistics are descriptive, not classifying.
- **Higher-order residual statistics.** No skewness, kurtosis, higher moments. The three fields specified (rms, max_abs, relative_rms) are sufficient for the documented use case.
- **Per-point residuals as a separate field.** Exposing the full `residuals: tuple[float, ...]` array is tempting but adds significant payload to every `LogLogSlopeObservation` instance for marginal benefit. Deferred. Consumers needing per-point residuals can re-compute them from slope, intercept, and the source transfer collection.
- **Change to `standard_error` derivation.** The existing formula stays identical. The new fields are computed *alongside* the existing computation, not as replacements.
- **Documentation of consumer-side threshold values.** Recommended `residual_rms` thresholds for various use cases live in consumer documentation (sweep_signature_probe etc.), not in task039.

## Completion Report

`Build_Docs/Reports/task039_typed_log_log_slope_residual_statistics_summary.md` (top-level) plus `Build_Docs/Reports/task039_typed_log_log_slope_residual_statistics/` (demonstration sub-artifacts). Required contents listed in Required Deliverables items 7 and 8.

## Acceptance Criteria

1. All required source modifications applied at declared paths; all task039 tests pass via `pytest tests/test_task039_*.py -x`.
2. Full test suite green at task close (no regressions; same 1101+ collection plus new task039 tests).
3. `pytest tests/test_task016_*.py` and `pytest tests/test_task017c_*.py` pass unchanged — `typed_log_log_slope` backwards compatibility verified.
4. `pytest tests/test_task018_directional_alpha_probe.py`, `pytest tests/test_task035_*.py`, `pytest tests/test_task036_*.py` pass unchanged — downstream consumer backwards compatibility verified.
5. `pytest tests/test_task010a_layer_manifest_machine_readable.py` passes — manifest reconciled if updated.
6. `pytest tests/test_task039_source_purity.py` passes — no forbidden imports.
7. `pytest tests/test_task010c_*.py` passes — lineage corpus updated.
8. **Demonstration result on the motivating Kerr retrograde fixture**:
   - `r_squared < 0.5` (low, because the underlying slope is near 0)
   - `residual_rms < 1e-10` (clean, because the formulation is genuinely smooth)
   - These two readings together demonstrate that the new field correctly classifies a case the existing r²-based discriminator misclassifies.
9. **Clean-power-law sanity check**: for `lambda f: f**2` sampled on a typical log-spaced grid, `residual_rms` is within a small multiple of machine epsilon. Specific threshold: `residual_rms < 1e-13`.
10. **Joint-state validation**: constructing `LogLogSlopeObservation` with `residual_rms` set but `residual_max_abs` not (or any other mixed state of the trio + standard_error) raises `ValueError`. Test asserts this directly.
11. **Serialization round-trip**: both unpopulated (all-`None`) and populated states round-trip through `to_json_safe()` correctly. New keys appear in the documented order in the JSON output.

---

**Pre-registration committed prior to implementation. Re-evaluate scope and acceptance criteria against this document only after task close.**

**Subsequent tasks**:
- **task040**: `sweep_signature_probe` cancellation discriminator upgrade. Replace `cancellation_grade = 1 − r_squared` with a scale-aware metric based on `residual_rms`. Add a new status cell or revised threshold semantics. Will re-run the Kerr retrograde case as the regression test — should now classify as `sweep_signature_clean`. Will also re-run the task035 16 GR cases — should re-confirm the existing 11/3/2 partition with possibly tighter thresholds.
- **task041** (conditional): `sweep_signature_floor_proximate` primitive with domain-realistic calibration set, deferred from task035 Non-Goals.
