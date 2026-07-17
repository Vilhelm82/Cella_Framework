# codex_task036_alpha_probe_sweep_signature_companion

## Repository

`/home/william_lloydlt/projects/V4/Lloyd_Engine_V4` (Lloyd Engine V4 main tree).

Clean-room enforcement: V1 / V3 source must not be imported, called, adapted, or bridged at runtime (Axiom 10). V3 reference evidence is permitted only as committed fixtures or copied test data.

## Current Verified Baseline

State at task commit, in `main`:

- All layers green through task035. Task035 closed; pre-reg moved to `Build_Docs/Agent_tasks/Completed/`.
- Full test suite collection succeeds (1101 tests collected) with the `--ignore=scratch` default in `pyproject.toml`.
- `primitives` layer provides: `typed_collection`, `typed_value`, `projective_ratio`, `stratified_quadratic_roots`, `typed_finite_difference`, `typed_log_log_slope`, `directional_alpha_probe`, `scalar_alpha_jet_bundle`, `singular_alpha_jet_bundle`, **`sweep_signature_probe`** (new from task035).
- `core.status` provides `SweepSignatureStatus` (new from task035).
- `AlphaProbeObservation` exposes the field set listed in `src/lloyd_v4/primitives/directional_alpha_probe.py` including `nested_window_fits`, `alpha_window_min/max/span`, `propagated_window_error`, `alpha_stability_status`, plus the n_* counts and declared-model fields. Adding optional fields with `None` defaults to this frozen dataclass is the existing extension pattern (the nested-window fields themselves were added this way).
- `SweepSignatureValue` exposes `cancellation_grade`, `drop_rate`, `slope_observation` (nested `LogLogSlopeObservation`), `n_input`, `n_observed`, `n_dropped`, the four per-status counts (`n_nonfinite`, `n_domain_refused`, `n_cancellation_dominated`, `n_delta_indeterminate`), and `expression_path`.
- Task035 calibration evidence on the 16 GR photon-sphere cases is committed at `Build_Docs/Reports/task035_sweep_signature_probe/calibration_observations.json`. This task references that evidence as the cross-check for joint-pattern expectations.

Full suite green at HEAD: required.

## Task Goal

Extend `directional_alpha_probe` to optionally invoke `sweep_signature_probe` as a sibling companion call. Attach typed sweep-signature evidence to `AlphaProbeObservation` as three new optional fields (`companion_sweep_signature_observation`, `companion_sweep_signature_status`, `companion_sweep_signature_trace_id`). The alpha_probe primary `AlphaProbeStatus` emission is unchanged; companion fields are informational evidence that consumers can use to disambiguate alpha-probe results (in particular, to distinguish "formulation-burdened" from "structurally unstable" interpretations of `alpha_unstable_window`). Caller opts in via a new keyword-only parameter; default behaviour is backwards-compatible. Establishes the integration pattern that tasks 037 and 038 will follow.

## Design Principles

1. **Axiom 5 + Axiom 8 (backwards compatibility).** Existing alpha_probe callers see no behavioural, schema, or serialization change when they do not opt in. With `companion_sweep_signature=False` (the default), the new fields are `None` and the result is bit-identical to pre-task036 alpha_probe output.
2. **Caller-opt-in trigger, not internal status-triggered.** Alpha_probe does NOT inspect its own status and conditionally invoke the companion. The decision to engage sweep_signature is the caller's. This matches task035 Design Principle 10 (sweep_signature_probe is a screening tool the caller deploys deliberately, not a side effect of upstream classification).
3. **Axiom 1 (informational companion).** Companion fields do not change alpha_probe's verdict. The combined-evidence interpretation (e.g., `alpha_unstable_window` + `sweep_signature_clean` → "structurally unstable, formulation appears fine") is the caller's responsibility. Alpha_probe emits independent evidence from two sibling primitives; downstream consumers compose them.
4. **Axiom 12 (sibling composition).** Both primitives sit at the `primitives` layer. Provenance records `alpha_probe` and `sweep_signature_probe` as sibling trace IDs of the same composed observation. No layer change.
5. **Reuse of caller inputs.** The companion call receives the same `g_callable`, `h_grid`, `eta`, `function_label`, and a deterministically-derived `probe_id` (suffix `"_companion_sweep_signature"`). No additional caller setup, no new grid construction.
6. **Axiom 11 (epistemic stance).** No new mathematical content. The companion call uses `sweep_signature_probe` as already shipped; no new constants, no new operations.
7. **Status family unchanged.** No new `AlphaProbeStatus` cells. No new combined status enum. The full cross-product of `AlphaProbeStatus` × `SweepSignatureStatus` interpretations is documented in `STATUS_CALCULUS.md` as a convention for consumers, not enforced via new typed cells.
8. **Symmetry deferred.** This task makes alpha_probe a consumer of sweep_signature_probe. The reverse direction (sweep_signature_probe optionally invoking alpha_probe) is not in scope — it would create a circular composition pattern. If a downstream consumer wants both perspectives, it calls both primitives directly.

## Primitive-Sufficiency Gate

| Concept needed | Provided by | Parent layer |
|---|---|---|
| `directional_alpha_probe` operation and `AlphaProbeObservation` dataclass | `primitives` (existing) | `primitives` |
| `sweep_signature_probe` operation and `SweepSignatureValue` / `SweepSignatureStatus` / `SweepSignatureResult` | `primitives` (task035) | `primitives` |
| Provenance trace ID propagation and child-trace registration | `Provenance` | `core` |
| Optional field addition to a frozen `slots=True` dataclass with `None` defaults | substrate dataclass mechanics; existing precedent in `AlphaProbeObservation.nested_window_fits` and siblings | n/a |
| Serialization of optional `SweepSignatureValue` field via `to_json_safe` | `lloyd_v4.core.serialization.to_json_safe` (already handles None and nested dataclasses) | `core` |
| Test infrastructure for joint behaviour on the 16 GR ground-truth cases | task035's calibration script and observations | `primitives` (task035 artifacts) |

**Halt condition: none.** All concepts available. The task is a pure composition of existing primitives plus dataclass field extension.

## Required Deliverables

### Modified source files

1. `src/lloyd_v4/primitives/directional_alpha_probe.py`:
   - Add three new fields to `AlphaProbeObservation`, each with `None` default:
     - `companion_sweep_signature_observation: SweepSignatureValue | None = None`
     - `companion_sweep_signature_status: SweepSignatureStatus | None = None`
     - `companion_sweep_signature_trace_id: str | None = None`
   - Extend `to_json_safe()` to include the three new fields (serialized via `to_json_safe(self.companion_sweep_signature_observation)` and `.value` extraction for the status enum).
   - Extend `__post_init__` validation: all three companion fields are either jointly `None` or jointly non-`None`. Mixed states raise `ValueError` with a message naming which field is inconsistent. (Same discipline as the existing nested-window-fields validation.)
   - Add `companion_sweep_signature: bool = False` to the `directional_alpha_probe` callable signature as a keyword-only argument.
   - When `companion_sweep_signature=True`: after the primary alpha_probe computation completes and the `AlphaProbeObservation` is about to be constructed, invoke `sweep_signature_probe(g_callable, h_grid, eta=eta, function_label=function_label, probe_id=f"{probe_id}_companion_sweep_signature")` and populate the three companion fields from the result (`.value`, `.status`, `.provenance.trace_id`).
   - Import `sweep_signature_probe`, `SweepSignatureValue`, `SweepSignatureStatus`, `SweepSignatureResult` from `lloyd_v4.primitives.sweep_signature_probe`.

2. `src/lloyd_v4/primitives/__init__.py`:
   - No new exports required. The existing `AlphaProbeObservation` export now carries the optional fields automatically.

### New source files

None. Task036 is a pure modification of an existing primitive plus tests and documentation.

### Documentation

3. `Build_Docs/Architecture/STATUS_CALCULUS.md`:
   - New section "Alpha + sweep signature combined evidence patterns" (or similar). Document the consumer convention for interpreting `(AlphaProbeStatus, SweepSignatureStatus)` pairs, with the four canonical patterns:
     - `alpha_regular_integer` / `alpha_fractional_branch` / `alpha_negative_singularity` + `sweep_signature_clean` → "well-characterized: alpha is meaningful and the formulation is clean."
     - `alpha_unstable_window` + `sweep_signature_cancellation_dominated` → "formulation-burdened: the instability is a formulation issue, refinery may help."
     - `alpha_unstable_window` + `sweep_signature_clean` → "structurally unstable (or sub-screening-threshold formulation): the instability persists despite a clean-looking sweep; sweep_signature_probe is a low-sensitivity screen so this can also indicate borderline formulation issues."
     - `alpha_cancellation_dominated` + `sweep_signature_cancellation_dominated` → "concurrent cancellation evidence: both probes agree the formulation is too noisy."
   - Note explicitly that these patterns are consumer-side interpretation conventions, not new typed statuses, and that no `StatusTransitionRule` is registered to enforce them.

4. `Build_Docs/V4_GLOSSARY.md`:
   - New entries: `companion_sweep_signature_observation`, `companion_sweep_signature_status`, `companion_sweep_signature_trace_id`. Each entry one paragraph describing what the field carries and when it is populated.
   - New entry: `companion call pattern` — a glossary entry documenting the convention of one primitive optionally invoking another sibling primitive and attaching the result as an informational field. Reference task036 as the canonical example.

5. `Build_Docs/LIVE_CAMPAIGNS_LEDGER.md`:
   - New entry: `alpha_probe_sweep_signature_companion` campaign. Last touched at commit date, last result "task036 commit", next concrete step "task037 (sterbenz_audit pre-screen)".

6. `Build_Docs/Reports/task036_alpha_probe_sweep_signature_companion_summary.md` — top-level headline summary following the task017c convention. Required contents:
   - Deliverable manifest (file paths, line counts; mostly modifications + small test additions)
   - Test counts (collected, passed, regression-suite delta — should be the same 1101 collection size plus N task036 tests)
   - The 16 GR cases re-run with `companion_sweep_signature=True`; joint-status table cross-referenced against task035's standalone calibration
   - The four canonical pattern interpretations from `STATUS_CALCULUS.md`, with the specific GR cases that exercise each
   - Backwards-compatibility evidence: pre-existing test_task018 tests pass unchanged with `companion_sweep_signature=False` (the default)

7. `Build_Docs/Reports/task036_alpha_probe_sweep_signature_companion/` directory with:
   - `joint_calibration_script.py` — reproducible script that runs alpha_probe with `companion_sweep_signature=True` across the 16 GR cases and emits the joint observations
   - `joint_observations.json` — structured outputs (one record per case, with both alpha_probe and companion sweep_signature evidence)
   - `joint_observations.md` — human-readable narrative

## Required Tests

| Test file | What it verifies |
|---|---|
| `tests/test_task036_source_purity.py` | No V3 imports, no forbidden mathematical content per Axiom 11. |
| `tests/test_task036_alpha_probe_sweep_signature_companion.py` | (a) Default `companion_sweep_signature=False` produces `None` for all three companion fields and bit-identical alpha_probe result for representative cases. (b) Opt-in `companion_sweep_signature=True` populates all three companion fields with valid types. (c) The 16 GR cases produce the expected joint patterns (see Acceptance Criterion 8). (d) F1_along_B naive specifically exhibits `alpha_unstable_window` + `sweep_signature_clean` — the canonical demonstrative pattern. (e) F1_along_r naive specifically exhibits `alpha_unstable_window` (or `alpha_cancellation_dominated`) + `sweep_signature_cancellation_dominated` — the canonical formulation-burdened pattern. (f) `AlphaProbeObservation.__post_init__` rejects mixed states (one companion field set, the others not). (g) Companion trace ID is distinct from primary alpha_probe trace ID. |
| `tests/test_task036_serialization.py` | `to_json_safe` round-trip preserves all three companion fields when populated, and emits `None` when unpopulated. JSON shape includes the new fields under known keys. |
| `tests/test_task036_layer_manifest.py` | Manifest tests still pass with the modified `AlphaProbeObservation` field set. If `layer_manifest.json` carries a field-level shape spec, update it; otherwise no change required. |
| `tests/test_task018_directional_alpha_probe.py` (existing, modified) | Existing tests pass unchanged. Add one or two new assertions that the three new companion fields default to `None` in pre-existing construction paths. |

## Required Commands

```bash
# Red slice (before implementation)
pytest tests/test_task036_*.py --collect-only

# Implementation slice (red -> green)
pytest tests/test_task036_*.py -x

# Backwards-compatibility check (task018 tests must still pass)
pytest tests/test_task018_directional_alpha_probe.py -v

# Full suite (no regressions)
pytest tests/

# Source audit
pytest tests/test_task036_source_purity.py -v
grep -RE "^(import|from) (cmath|numpy|scipy|sympy|mpmath)" src/lloyd_v4/primitives/directional_alpha_probe.py

# Manifest audit
pytest tests/test_task010a_layer_manifest_machine_readable.py
pytest tests/test_task010b_*.py

# Lineage audit
pytest tests/test_task010c_*.py
```

All eight commands must pass for completion.

## Non-Goals

- **Internal status-triggered companion call.** Alpha_probe does not inspect `AlphaProbeStatus` and decide whether to invoke `sweep_signature_probe`. Caller-opt-in only. Auto-trigger logic, if useful, becomes a follow-up task.
- **New `AlphaProbeStatus` cells.** No new alpha-probe statuses to represent companion-confirmed formulation-burdened vs structurally-unstable. The cross-product interpretation lives as a consumer convention in `STATUS_CALCULUS.md`.
- **New combined status family.** No new enum representing `(AlphaProbeStatus × SweepSignatureStatus)` tuples. Adds noise without typed-composition benefit at this stage.
- **`StatusTransitionRule` for combined evidence.** If a future consumer wants to enforce a specific joint-evidence interpretation as a transition, that becomes a separate task. Task036 ships the evidence pairs; consumers compose.
- **`scalar_alpha_jet_bundle` / `singular_alpha_jet_bundle` companion call.** The two jet-bundle primitives are not modified. They continue to use `directional_alpha_probe` without companion. If they would benefit from companion evidence, that becomes follow-up tasks.
- **Reverse-direction companion call.** `sweep_signature_probe` does not gain an optional `companion_alpha_probe` parameter. The composition is one-way to avoid circular-composition risk.
- **`evals/sterbenz_audit/` integration.** Refinery pre-screen wiring is task037.
- **Floor-proximate primitive.** Deferred to task038.
- **New ground-truth fixtures.** The 16 GR photon-sphere cases plus task035's synthetic edge cases are the calibration set; nothing new is introduced.

## Completion Report

`Build_Docs/Reports/task036_alpha_probe_sweep_signature_companion_summary.md` (top-level headline) plus `Build_Docs/Reports/task036_alpha_probe_sweep_signature_companion/` (joint-calibration sub-artifacts). Required contents listed in Required Deliverables items 6 and 7.

## Acceptance Criteria

1. All required source modifications applied at declared paths; all task036 tests pass via `pytest tests/test_task036_*.py -x`.
2. Full test suite green at task close (no regressions; same 1101 collection plus new task036 tests).
3. `pytest tests/test_task018_directional_alpha_probe.py` passes unchanged — backwards compatibility verified.
4. `pytest tests/test_task035_*.py` passes unchanged — task035 untouched by task036's modifications.
5. `pytest tests/test_task010a_layer_manifest_machine_readable.py` passes — manifest test still green after `AlphaProbeObservation` field-set change.
6. `pytest tests/test_task036_source_purity.py` passes — no forbidden imports.
7. `pytest tests/test_task010c_*.py` passes — lineage corpus updated to record the new sibling composition from `directional_alpha_probe` to `sweep_signature_probe`.
8. **Joint calibration result on the 16 GR photon-sphere test cases with `companion_sweep_signature=True`:**
   - **F1_along_B naive**: `AlphaProbeStatus.ALPHA_UNSTABLE_WINDOW` + `SweepSignatureStatus.SWEEP_SIGNATURE_CLEAN` (canonical demonstrative pattern — sweep_signature's clean classification confirms screening philosophy)
   - **F1_along_r naive**, **F1_along_tangent naive**, **F2_along_tangent naive**: alpha-probe emits `ALPHA_UNSTABLE_WINDOW` or `ALPHA_CANCELLATION_DOMINATED` + sweep_signature emits `SWEEP_SIGNATURE_CANCELLATION_DOMINATED` (formulation-burdened patterns; joint evidence indicates the instability is a formulation issue not a structural one)
   - **F2_along_M stable and naive**: alpha-probe refuses or emits `ALPHA_INSUFFICIENT_DATA` / `ALPHA_DOMAIN_REFUSED` + sweep_signature emits `SWEEP_SIGNATURE_DEGENERATE_INPUT` (both refusing the constant-zero observable)
   - **The remaining 9 cases** (7 stable non-zero forms + F1_along_M naive + F2_along_r naive + F2_along_B naive, minus F2_along_M which is already covered) match a declared alpha model + emit `SWEEP_SIGNATURE_CLEAN`
   - Per-case results recorded in `joint_observations.json` and summarised in `joint_observations.md`.
9. Mixed-state validation: constructing `AlphaProbeObservation` with one companion field set and the others `None` raises `ValueError`. Test asserts this directly.
10. Serialization round-trips both unpopulated (all-`None`) and populated companion fields; the new keys appear in `to_json_safe()` output in the documented order.
11. Companion `trace_id` is distinct from the primary alpha_probe trace ID; provenance lineage records the companion as a sibling-trace child.

---

**Pre-registration committed prior to implementation. Re-evaluate scope and acceptance criteria against this document only after task close. Subsequent tasks:**

- **task037**: `evals/sterbenz_audit/rewrite_candidates.py` pre-screen integration with `sweep_signature_probe` (uses the screening philosophy directly at the refinery layer)
- **task038**: `sweep_signature_floor_proximate` primitive with domain-realistic calibration set (Kerr ISCO or Rayleigh-Bénard near-onset)
- **task039** (conditional): `typed_log_log_slope` residual-statistics extension if `r_squared` proves insensitive on real cancellation patterns from task036's joint calibration
- **task040** (deferred): geometric oracle primitive for sweep-sampling nullity / K_G / coupling-graph evidence
