# Session Handoff — 2026-05-27 — GAP-003 typed_ulp Transplant Arc

**Campaign:** `substrate-construction-transplant-arc` (LIVE_CAMPAIGNS_LEDGER)
**Repo:** `/home/william_lloydlt/projects/V4/Lloyd_Engine_V4`
**V3 reference (read-only, never import):** `/home/william_lloydlt/Documents/Lloyd_Engine/lloyd_v3/`

---

## TL;DR — state of the world

**Transplant 1 (GAP-003 `typed_ulp`) is substantively COMPLETE.** The conditioning primitive
exists in the substrate with float64 + float32 paths, 45 tests green, all 12 known consumer sites
migrated, DRY-003 ULP-helper duplication consolidated, manifest + glossary + ledger + gap-inventory
all updated. GAP-012 (conditioning-primitive naming) closed alongside it.

**Transplant 2 (GAP-011 hardened dual-arm probe) is NEXT.** Discovery is done; a starting brief is
filed at `Build_Docs/Agent_tasks/transplant_2_gap011_starting_brief.md`. Two decisions block the
lift (destination package, v10/v11 dependency strategy). Do not start coding it before reading the
brief.

**Do NOT** propose K_G (GAP-005) as the next transplant. It is deferred until substrate-invariant-search
Gate 2 closes. This is a recurring wrong-turn; the ledger has an anti-restart note about it.

---

## What was completed this arc (chronological)

1. **GAP-012 naming decision** (prior session): primitive named `typed_ulp`; V4_GLOSSARY \u00a713
   disambiguation entry added distinguishing `core/conditioning.py` (L0 carrier dataclass) from the
   \u00a79 conditioning primitive (the L1 IEEE-754 lattice-geometry primitive that `typed_ulp` embodies).

2. **DRY-003 reconciliation audit** (`scratch/dry003_ulp_reconciliation_audit.py`): six ULP-helper
   variants tested across 31 grid points. Established the canonical behaviour (below) and found a
   **real bug**: `mcg_phase_1_g1_route_divergence:ulp_float64` and `mcg_gate_3_killswitch:ulp_float64`
   returned `0.0` for ALL subnormal inputs (8 grid points each).

3. **`typed_ulp` primitive built** at `src/lloyd_v4/primitives/typed_ulp.py` (pure stdlib: `math` +
   `struct`, no numpy). 6-status `UlpStatus` family, `TypedUlpValue` payload, two protocols.

4. **Float32 extension**: `typed_ulp(x, *, precision="float64")` dispatcher routes to
   `_typed_ulp_float64` / `_typed_ulp_float32`. Float32 path uses `struct` `>f`/`>L` round-trip.
   Found + fixed a second bug: `_round_to_float32` crashed with `OverflowError` for `|x| > FLT_MAX`
   (Python struct refuses to pack); now caught and saturated to \u00b1inf so it routes to
   `ULP_NONFINITE_INF`. Regression-tested.

5. **API rename**: public kwarg `format` \u2192 `precision` (matches V4 evals convention,
   `_ulp_of_value(value, precision)`). Old `format=` now raises `TypeError` (regression-tested).
   Internal `TypedUlpValue.format` field kept \u2014 it records the IEEE-754 format label, distinct
   from the precision selector.

6. **Tests**: `tests/test_typed_ulp.py` \u2014 45 tests, all green (26 float64 + 18 float32 + 1
   dispatcher). 0.31s runtime.

7. **Consumer migrations** (12 sites, all thin wrappers delegating to `typed_ulp`):
   - 2 MCG bug-fix sites: `mcg_phase_1_g1_route_divergence`, `mcg_gate_3_killswitch` (subnormal bug
     fixed \u2014 now returns 2^-1074 not 0.0).
   - 2 evals consumers: `scale_invariant_signature._ulp_of_float32`,
     `multi_precision_four_form.ulp_of_double` (byte-compatible, 0 mismatches vs bit-manip reference).
   - 8 cosmetic scratch sites (10 function bodies): `bacl_subnormal_audit`, `bacl_invariant_audit`
     (\u00d72), `c2_lattice_substrate_derivation`, `c2_lattice_sharpness_audit` (\u00d72),
     `c2_lattice_binade_danger_zone`, `c2_theorem_scope_gate`, `blowup_exponent_v4_audit`,
     `substrate_fingerprint_atlas_phase_beta`. Smoke-tested byte-identical to `typed_ulp` reference.

8. **Discipline-gate snapshots** bumped in 4 test files (`len(primitives.__all__)` 65\u219280):
   `test_task017b`, `test_task024b`, `test_task025`, `test_task026`.

9. **Registration + docs**: layer_manifest.json + LAYER_MANIFEST.md updated; LIVE_CAMPAIGNS_LEDGER
   updated (Status / Last result / Next step); task050 `parent_primitive_gaps.md` got a resolution
   tracker banner.

---

## Key facts worth preserving

### typed_ulp API surface (reference for future L1 primitives)

`typed_ulp(x: float, *, precision: str = "float64") -> TypedUlpResult`

- `precision` in {"float64", "float32"}; anything else raises `ValueError`. Old `format=` kwarg raises `TypeError` (do not reintroduce it).
- Returns the `TypedResult` envelope (`core.result`): `.value` / `.space` / `.status` / `.validity` / `.conditioning` / `.provenance` / `.protocol` / `.refusal`.
- `.value` is `TypedUlpValue(ulp, input_value, binade, is_subnormal, is_finite, format)`. `.value.ulp` is the float spacing; `.value.format` is the IEEE label ("float64"/"float32").
- 6-status `UlpStatus`: ULP_NORMAL, ULP_SUBNORMAL, ULP_ZERO, ULP_AT_EDGE, ULP_NONFINITE_INF, ULP_NONFINITE_NAN.
- Protocols: `TYPED_ULP_PROTOCOL` (producer), `FINITE_TYPED_ULP_PROTOCOL` (consumer).
- Pure stdlib (`math`, `struct`). Float32 via `struct` `>f`/`>L` bit round-trip; no numpy.

### Canonical ULP behaviour (the DRY-003 reference; any future helper must match)

| input class | float64 ulp | float32 ulp | status |
|---|---|---|---|
| normal x | 2^(binade-52) | 2^(binade-23) | ULP_NORMAL |
| subnormal x | 2^-1074 (=5e-324) | 2^-149 | ULP_SUBNORMAL |
| 0.0 | 2^-1074 | 2^-149 | ULP_ZERO |
| largest finite | +inf | +inf | ULP_AT_EDGE |
| +/-inf | (carries +inf) | (carries +inf) | ULP_NONFINITE_INF (refused) |
| nan | (carries nan) | (carries nan) | ULP_NONFINITE_NAN (refused) |

Canonical implementation reference is bit-manipulation nextafter (`_float_from_bits(bits+1) - x`), pure stdlib. The old `max(frexp(abs(x))[1] - 53, -1074)` floored form agrees on finite inputs but the floor silently produced wrong subnormal answers in two MCG sites.

### Bugs found + fixed this arc (do not regress)

1. Subnormal underflow in `mcg_phase_1_g1_route_divergence` + `mcg_gate_3_killswitch`: returned 0.0 for all subnormals. Fixed by migrating to `typed_ulp` (now 2^-1074).
2. Float32 OverflowError: `struct.pack(">f", x)` raises for |x| > FLT_MAX (~3.4e38) instead of rounding to inf. `_round_to_float32` now catches and saturates to +/-inf. Regression test: `test_float32_overflow_input_routed_to_nonfinite_inf`.

### Discipline-gate snapshot convention

4 test files assert `len(primitives.__all__) == 80`. The number = 65 baseline + 10 `sweep_signature_probe` (task035) + 5 `typed_ulp` (GAP-003). Any future primitive addition must bump this in all 4 files (`test_task017b`, `test_task024b`, `test_task025`, `test_task026`) AND verify the per-task `"<name>" not in primitives.__all__` checks still hold.

### Test state

- `tests/test_typed_ulp.py`: 45/45 green.
- 4 discipline-gate files: green after the snapshot bump.
- Pre-existing failures NOT caused by this arc (leave alone or fix separately):
  - `test_task017c_multi_precision_theorem2`: 2 failures from a hardcoded path `/home/william_lloydlt/projects/V4/Docs/transfer_function_exponent_family_v3.tex` that does not exist on disk. Path bug, unrelated to ULP work.
  - `test_no_manifest_changes`: ~10 failures that are the discipline gate firing on uncommitted layer_manifest changes (sweep_signature_probe + typed_ulp). These resolve on commit, not real regressions.
- Broader 12-file regression never cleanly completed (timed out twice at the ~4-minute read ceiling). The 4 critical discipline gates + typed_ulp passed in a focused run (returncode 0). Worth a clean run with `-k "not campaign"` to dodge the slow task026c-029c campaign tests.

---

## Outstanding backlog (ranked)

1. **Transplant 2 = GAP-011 hardened dual-arm probe lift.** Brief at `Build_Docs/Agent_tasks/transplant_2_gap011_starting_brief.md`. Two blocking decisions: (a) destination package (`probes/` vs `evals/probes/` vs extend `branch/`); (b) v10/v11 scratch-dependency strategy (lift both / refactor away / transitional import). Refactor-away is cleanest substrate hygiene but real work.
2. **Choptuik gamma-bias 20-seed audit + detection-threshold false-positive calibration.** Honesty work flagged alongside the pure-noise control (`scratch/choptuik_step2_pure_noise_control.py`). The matched-filter "SNR" was shown to couple to FP roundoff/lattice structure, not true signal \u2014 pure power law + zero noise still produced 8.24 dB. Needs calibration before any detection claim ships.
3. **task045 pre-reg revision.** `Build_Docs/Agent_tasks/codex_task045_log_periodic_residual_probe.md` \u2014 the matched-filter primitive cannot honestly emit a continuous "SNR"; it needs a lattice-aware detection statistic. This is now *doable* because `typed_ulp` provides the lattice-spacing machinery.
4. **Transplant 3 = GAP-001 `typed_sqrt` + GAP-002 `typed_log`.** Closes Axiom 11' refinement criterion 1. BLOCKED on GAP-009 (L1 atomicity policy) resolving first.
5. **GAP-009 L1 atomicity policy decision.** Methodology question: are sqrt/log atomic L1 primitives, or do they decompose? Must resolve before Transplant 3.
6. **Documentation housekeeping** (low priority): mark `Primitive_Design_Proposals.md`, `Unification_Roadmap.md`, `V4_Triaged_Process_Tree.md` as "draft pre-methodology, superseded by task050 + SUBSTRATE_CONSTRUCTION"; move legacy catalogues to `Build_Docs/Reference/`; archive task035/036/050 to `Completed/`.

## Methodology reminders (these are load-bearing, do not drift)

- **Axiom 10 / V3_REFERENCE_LEDGER:** V3 is reference-only. Never import, call, adapt, or bridge to V3 at runtime. Look at V1/V3 for *mechanical-property guidance* (what design problem is real, what to attempt), never for the solution to copy. Every V4 design stands on its own derivation from typed-substrate axioms.
- **Axiom 11 (epistemic stance):** during substrate construction, no imports of named mathematical content (`math` is allowed for IEEE primitives like ldexp/frexp/struct; `numpy`/`scipy`/`sympy`/`mpmath` are NOT for substrate primitives). No hardcoded math constants as substrate. `typed_ulp` honours this: pure `math`+`struct`, IEEE-754 constants derived, no numpy.
- **Dissection gate (4 parts)** for every transplant: constants measured, theorems registered, bit-match or documented divergence, modelling commitments declared. See `SUBSTRATE_CONSTRUCTION.md`.
- **Methodology-mandated transplant ordering:** conditioning primitive (typed_ulp, DONE) \u2192 typed_sqrt/typed_log \u2192 K_G only after substrate-invariant-search closes. K_G is consumer-layer composition, NOT a substrate primitive.

## Tooling gotchas (this environment, process-tools-only)

This session ran with only Desktop Commander process tools (no edit_block/view/write_file). All edits went through `python3 -i` REPL via `interact_with_process`. Hard-won lessons:

- **Blank lines inside a function / `with` / `if` block terminate the block** in interactive `python3 -i`. Wrap multi-line logic in `exec(\"\"\"...\"\"\")` strings instead of typing blocks directly.
- **f-strings with nested escaped quotes** (e.g. `f"{\"site\":<20s}"`) raise SyntaxError in the REPL. Avoid them; use `.format()` or plain concatenation.
- **`del sys.modules['lloyd_v4...']` wipes the bound name** \u2014 you must re-import after clearing, or you get NameError / stale-module behaviour.
- **`read_process_output` has a ~4-minute ceiling.** Long pytest runs (the task026c\u2013029c campaign tests) exceed it. Use `-k "not campaign"` or run focused file subsets; capture with `subprocess.run(..., capture_output=True, timeout=N)` inside the REPL rather than streaming.
- **Import-insertion heuristic bug** (mine, this session): inserting an import after "the last top-level import line" landed it *inside* a multi-line `from X import (...)` block in `substrate_fingerprint_atlas_phase_beta.py`, breaking the paren. If you script import insertion, insert after the closing `)` of multi-line import blocks, not after the `from X import (` line.

## File inventory (created / modified this arc)

New:
- `src/lloyd_v4/primitives/typed_ulp.py`
- `tests/test_typed_ulp.py` (45 tests)
- `scratch/dry003_ulp_reconciliation_audit.py`
- `scratch/choptuik_step2_pure_noise_control.py` (+ `_results.json`)
- `Build_Docs/Agent_tasks/transplant_2_gap011_starting_brief.md`
- `Build_Docs/Agent_tasks/session_handoff_2026_05_27_gap003_typed_ulp_arc.md` (this file)

Modified (substrate/core):
- `src/lloyd_v4/core/status.py` (UlpStatus + StatusCode union)
- `src/lloyd_v4/primitives/__init__.py` (exports)
- `src/lloyd_v4/evals/scale_invariant_signature.py` (migrated `_ulp_of_float32`)
- `src/lloyd_v4/evals/multi_precision_four_form.py` (migrated `ulp_of_double`)

Modified (tests):
- `tests/test_task017b_multi_precision_instrument_model.py` (snapshot 65->80)
- `tests/test_task024b_schwarzschild_four_form.py` (snapshot 65->80)
- `tests/test_task025_path_law_discovery.py` (snapshot 65->80)
- `tests/test_task026_lattice_anomaly_investigation.py` (snapshot 65->80)

Modified (scratch DRY-003 migrations, 10 fn bodies):
- `scratch/mcg_phase_1_g1_route_divergence.py`, `scratch/mcg_gate_3_killswitch.py` (bug-fix)
- `scratch/bacl_subnormal_audit.py`, `scratch/bacl_invariant_audit.py` (x2)
- `scratch/c2_lattice_substrate_derivation.py`, `scratch/c2_lattice_sharpness_audit.py` (x2)
- `scratch/c2_lattice_binade_danger_zone.py`, `scratch/c2_theorem_scope_gate.py`
- `scratch/blowup_exponent_v4_audit.py`, `scratch/substrate_fingerprint_atlas_phase_beta.py`

Modified (docs):
- `Build_Docs/V4_GLOSSARY.md` (\u00a713 disambiguation \u2014 prior session)
- `Build_Docs/Architecture/layer_manifest.json` + `LAYER_MANIFEST.md` (typed_ulp registered)
- `Build_Docs/LIVE_CAMPAIGNS_LEDGER.md` (Status / Last result / Next step)
- `Build_Docs/Reports/task050/parent_primitive_gaps.md` (resolution tracker banner)

## First moves for the next session

1. Read this handoff + the Transplant 2 brief.
2. Decide whether to start Transplant 2, or knock out the smaller honesty items (Choptuik audit, task045 pre-reg) first \u2014 those are self-contained and now unblocked by typed_ulp.
3. If committing first: the `test_no_manifest_changes` failures clear on commit; do that before a clean regression so the gate is meaningful.
4. Clean regression run with `-k "not campaign"` to get a green baseline that actually completes.
