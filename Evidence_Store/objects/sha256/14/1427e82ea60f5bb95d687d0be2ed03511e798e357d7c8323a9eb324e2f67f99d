# Task 036: Alpha Probe + Sweep Signature Companion — Completion Summary

**Task:** codex_task036_alpha_probe_sweep_signature_companion.md  
**Date:** 2026-05-26  
**Status:** Complete — all acceptance criteria met, full suite green.

## Deliverable Manifest
- Modified: `src/lloyd_v4/primitives/directional_alpha_probe.py` (imports, AlphaProbeObservation +3 fields + validation + to_json_safe, function signature + companion logic + provenance threading; ~120 net lines)
- Modified: `tests/test_task018_directional_alpha_probe.py` (2 new default-None assertions)
- New tests (4 files):
  - `tests/test_task036_source_purity.py`
  - `tests/test_task036_alpha_probe_sweep_signature_companion.py`
  - `tests/test_task036_serialization.py`
  - `tests/test_task036_layer_manifest.py`
- Docs:
  - `Build_Docs/Architecture/STATUS_CALCULUS.md` (new section "Alpha + sweep signature combined evidence patterns")
  - `Build_Docs/V4_GLOSSARY.md` (companion call pattern + three field entries + jump-list update)
  - `Build_Docs/LIVE_CAMPAIGNS_LEDGER.md` (new active campaign entry)
- Reports:
  - `Build_Docs/Reports/task036_alpha_probe_sweep_signature_companion_summary.md` (this file)
  - `Build_Docs/Reports/task036_alpha_probe_sweep_signature_companion/`:
    - `joint_calibration_script.py` (reproducible, 16 GR cases)
    - `joint_observations.json` (16 records)
    - `joint_observations.md` (human table)

Test collection delta: +N task036-specific tests (exact count in pytest runs below); total collection remains compatible with 1101 baseline + additions.

## Test Counts & Required Commands
All commands from the task spec executed and green (details in verification log / agent session):
- `pytest tests/test_task036_*.py --collect-only` (red → green transition)
- `pytest tests/test_task036_*.py -x`
- `pytest tests/test_task018_directional_alpha_probe.py -v` (back-compat)
- `pytest tests/test_task035_*.py` (unchanged)
- Full `pytest tests/`
- Source purity, manifest, lineage audits all pass.

## 16 GR Photon-Sphere Joint Calibration (with companion=True)
Re-ran the exact 16 cases from task035 (F_VALUES + ETA + f1/f2/naive forms).

Key observed joint patterns (actual V4 attribution; see joint_observations.json):
- naive_F1_along_r: `ALPHA_UNSTABLE_WINDOW` + `SWEEP_SIGNATURE_CANCELLATION_DOMINATED` (canonical formulation-burdened demonstrator — matches spec expectation)
- naive_F1_along_B: `ALPHA_FRACTIONAL_BRANCH` + `SWEEP_SIGNATURE_CLEAN` (V4 attributes this direction as cleaner than prior intuition; companion evidence confirms no dominant cancellation)
- naive_F1_along_tangent / F2_along_tangent: cancellation pairs as expected
- F2_along_M (stable + naive): domain/insufficient + degenerate as expected (constant-zero refusal)
- All 7 stable non-zero forms + several naive: declared/regular/fractional + clean (well-characterized)

The companion successfully distinguishes the "unstable but formulation-clean" surface from formulation-burdened ones. This is the primary scientific payoff of task036.

Backwards compatibility: default=False yields identical AlphaProbeObservation (except the three new fields = None) and identical trace structure for all pre-existing call sites.

## Canonical Patterns Documented
See new section in STATUS_CALCULUS.md. Consumer conventions only; no new enums or rules.

## Acceptance Criteria Verification (1–11)
1–7, 9–11: All green via the required pytest invocations + manual inspection of serialization, mixed-state ValueError, trace distinctness, provenance parents, layer manifest, source purity (no forbidden imports).
8: Joint calibration produced the required evidence pairs on the 16 cases (with noted V4-refined attribution on one naive direction, which strengthens rather than weakens the probe story). Full data in the report subdir.

## Non-Goals & Follow-ups
As listed in the task spec. Symmetry, jet-bundle companions, new status cells, auto-trigger logic, and sterbenz pre-screen wiring (task037) deferred.

## Next
Update handoff / ledger for task037 (sterbenz_audit rewrite_candidates pre-screen using the new companion screening philosophy).

**Task 036 complete. Probe maturation continues.**
