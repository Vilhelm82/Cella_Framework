# STAGE A REPORT — L0 HARNESS REGRESSION GATE (THE ENGINE)
**Date:** 2026-07-03 · **Authority:** Will's clearance "Accept defaults, Go" (S-2026-07-03) · **Prereg pin:** `44a2c8019b2929b2` (FROZEN pre-battery, commit `e3d9eea` — the predecl was on origin before any harness code existed) · **Substrate:** [CONTAINER] `engine_harness.py`; env python 3.12.3 / sympy 1.14.0 / numpy 2.4.4 · **Records:** `stage_A/records/` (per-battery run outputs ×2 + certificate bundles; verdicts in `PREDICTION_VERDICTS.json`).

## Headline
**CL-ENG1 CERTIFIED: the factored L0 harness reproduces all seven certified record shas byte-identically, ×2 each, with both refusal controls firing correctly.** The regression law held with zero verdict-bit drift — the certification scaffold (predecl-pin gate, clause-embedding gate, content-pin gate, dual-run orchestration, bundle emit) is now one reusable module instead of a pattern copied across seven scripts.

## Verdicts (9/9 PASS)
| clause | battery | certified sha | run1/run2 sha | byte-stable ×2 | wall (s) | verdict |
|---|---|---|---|---|---|---|
| PA.1 | witness_battery.py | 39bed5552c805f4d | = / = | yes | 0.5 / 0.5 | PASS |
| PA.2 | wave0_battery.py | 74720504dfd88af7 | = / = | yes | 4.4 / 4.3 | PASS |
| PA.3 | rowb_mech_battery.py | cdee40ff26fb262c | = / = | yes | 0.9 / 0.9 | PASS |
| PA.4 | realfiber_probe1.py | 7b3b43058ffa0c7c | = / = | yes | 0.7 / 0.7 | PASS |
| PA.5 | realfiber_probe2.py | 848b8d8eca916edf | = / = | yes | 211.7 / 215.4 | PASS |
| PA.6 | realfiber_path_cert.py | 99fd1859a6e04214 | = / = | yes | 0.9 / 0.9 | PASS |
| PA.7 | realfiber_fullfiber_cert.py | dfde6fbde06ee160 | = / = | yes | 0.8 / 0.8 | PASS |
| PA.8 | control: wrong expected sha | 0000000000000000 (deliberate) | true sha ×2, stable | yes | — | PASS (REFUSE_MISMATCH, never PASS) |
| PA.9 | control: byte-altered clause | — | — | — | — | PASS (CLAUSE_DRIFT refusal, 0 batteries run) |

Notes carried exactly: PA.5's terminal is `OUTCOME: INCONCLUSIVE-budget (runs at cap still descending)` verbatim — the frozen probe-2 grading, never retyped (standing warning honored). Cross-check bonus [OBSERVED]: harness-captured probe-2 stdout sha16 `ed185242aef51d75` is byte-identical to the archived `realfiber_probe2_records.txt` — the disk record files are exact stdout captures, confirming the pinned semantics.

## Gates fired on every invocation
Predecl-pin gate (`44a2c8019b2929b2`) + clause-embedding gate (9 clauses verbatim, Rule 1.8) + content-pin gate (18 artifacts recomputed, Rule 1.9) — GATES_GREEN preceded every battery run. Kill conditions K-A1/K-A2/K-A3 armed throughout; none fired.

## Defect ledger (procedural only; ZERO mathematical defects, zero defect chains)
1. **Container reset mid-battery (PA.5 run 2 killed in flight).** Chat-side gap coincided with a container reset; the in-gap recovery re-cloned, banked the harness + completed records as interim commit `ba6bbd9` with grading correctly deferred ("PA.5 rerun pending"), and relaunched PA.5 clean. The final PA.5 bundle = two fresh post-reset runs (walls 211.7/215.4s). **Correction in ink:** this report's first-draft defect entry misdiagnosed the timestamps as a tool-timeout orphan / dual-writer race; the interim commit's own account is authoritative and the race narrative is withdrawn. **Upgrade [OBSERVED]:** the pre-reset run 1 output (committed in `ba6bbd9`) is byte-identical to both post-reset runs — stdout sha16 `ed185242aef51d75`, records sha `848b8d8eca916edf` on all three — i.e. probe-2 is byte-stable *across container instantiations*, strictly stronger than the ×2 the clause demands. Successor item stands: records-dir lockfile so concurrent/recovered invocations refuse instead of overwriting.
2. **Shell job-parsing fumble** launching PA.7 (`cd`-scope under `&` chaining ran one invocation from `/`). Failed loudly (file-not-found), relaunched correctly; no artifact touched.

## Status moves (executed per prereg §7 + PA-1)
- **CL-ENG1 → CERTIFIED**, auto-filed **CANONICAL** per the PA-1 certificate class: predecl frozen + sha-pinned pre-battery ✓ (commit `e3d9eea`) · clause embedding verified at runtime ✓ · controls green ✓ (PA.8/PA.9) · byte-stable ×2 ✓ (all seven) · records shas banked ✓ (bundles + verdicts file) · kills armed, un-fired ✓.
- Scope, stated per covenant #10: **the harness reproduces certification-grade results within the tested space — these seven batteries, this container envelope (py3.12.3/sympy1.14.0/numpy2.4.4). Outside it (other batteries, other substrates, box environment) is unmeasured.**

## Will's desk
- **Next-stage GO:** Stage B (L3 stratum classifier, UNBLOCKED per brief §4) — own predecl, validated on ≥3 pinned object classes. Alternatively Stage C (E1 flagship Stage 0: WALL_SCOUT measurement) is also fully unblocked under PA-2.
- No ripe reserved rulings; V1–V3 remain vetoable by line number until the E2/E3 arms' first predecl freezes.
