# Transplant 2 — GAP-011 Hardened Dual-Arm Probe Lift — Starting Brief

**Status:** Discovery complete; transplant work not yet started.
**Drafted:** 2026-05-27, immediately after Transplant 1 (GAP-003 typed_ulp) substantively closed.
**Belongs to campaign:** `substrate-construction-transplant-arc` (see LIVE_CAMPAIGNS_LEDGER).

---

## What the transplant moves

| from | to | size |
|---|---|---|
| `scratch/hardened_dual_arm_probe.py` | `src/lloyd_v4/<DECISION>/hardened_dual_arm_probe.py` | 593 lines, ~23.7 KB |

The probe is an **L3 eval-layer instrument** (composes L1/L2 primitives into a 6-condition resolution rule). Per the existing campaign log it is V1-complete and operative (`15/15 tests pass; 16 gap_resolved records on the production fixture set`). The transplant is *lifecycle*, not *substrate-construction*: working code, wrong location.

## Architectural decision required (BLOCKS the lift)

GAP-011 specs the target as either:
- `src/lloyd_v4/probes/hardened_dual_arm_probe.py` (new sub-package), or
- extend `src/lloyd_v4/branch/` to host it.

The probe's own module docstring (lines 29-31) says it is **eval-layer only** and explicitly does NOT promote the dual-arm pattern into substrate (referencing `DUAL_ARM_PROBE_PRINCIPLES.md` "What these constraints are NOT").

**Decision points for the next session:**

1. Is `branch/` semantically a home for evaluation-time probes, or for something else? (Inspect its current contents.)
2. Are probes a peer category to `evals/`, or a sub-category of it (`evals/probes/`)?
3. Does the V4 layer model already have a slot for "L3 instrument that wraps lower-level runners" (e.g. v10/v11), or does this transplant define one?

Recommend: read `src/lloyd_v4/branch/` and `src/lloyd_v4/evals/` contents + their `__init__.py` declarations before choosing.

## Transitive dependency chain (must be resolved)

The probe imports:
- `scratch.run_foldreadback_probe0_v10_active_dualarm` as `v10`
- `scratch.run_foldreadback_probe0_v11_genuine_separation` as `v11`

Both are still in scratch. Options:
- **(A)** Lift `v10` and `v11` alongside the probe.
- **(B)** Refactor the probe to depend only on substrate primitives, replacing the scratch v10/v11 imports with a thinner internal arm-evaluation helper.
- **(C)** Lift only the probe; leave it importing from `scratch.` via a documented "transitional import" pattern (technical debt).

Option (B) is the cleanest substrate hygiene but is real work (the probe "Wraps v11s machinery; does not re-implement arm evaluation" per docstring line 8). Option (A) doubles the surface area. Option (C) violates the spirit of substrate construction.

## Dissection-gate checklist (must complete before merge)

Per SUBSTRATE_CONSTRUCTION.md §6, every transplant requires:

1. **Constants measured.** What numerical thresholds, frozen allow-lists, and falloff parameters live in the probe? (`ALLOWED_ROUTE_KINDS`, `ALLOWED_ACTIVATION_RULES`, `ALLOWED_SELECTION_RULES` visible from lines 58-60 — read full file.)
2. **Theorems registered.** What invariants does the probe enforce? (6 conditions c1-c6, ARM-W gap membership, diagnostic-route capping, same-route control opt-in.)
3. **Bit-match or documented divergence.** Move-only with no behaviour change should be bit-for-bit identical on the existing 16-record test fixture.
4. **Modelling commitments declared.** The frozen `DualArmConfig` already does this at construction time — verify the dissection-gate uses this as evidence.

## Files that must be updated alongside the lift

From the importer grep (excluding `.zip`, `pycache`, and `.pytest_cache`):

**Doc/report files (need path-update only):**
- `Build_Docs/Architecture/DUAL_ARM_PROBE_PRINCIPLES.md`
- `Build_Docs/PROBE_READINESS.md`
- `Build_Docs/V4_GLOSSARY.md`
- `Build_Docs/LIVE_CAMPAIGNS_LEDGER.md` (campaign `hardened-dual-arm-probe` entry)
- `Build_Docs/Reports/hardened_dual_arm_probe/*` (preregistry, closeout, archived tests)
- `Build_Docs/Reports/task050/*` (4 reports reference it)
- `Build_Docs/Reports/substrate_fingerprint_atlas*/closeout.md`
- `Build_Docs/Reports/mcg_*` (3 mentions)
- `Build_Docs/Agent_tasks/*` (3 handoff docs)

**Code files (need import-update):**
- `scratch/substrate_fingerprint_atlas.py`
- `scratch/substrate_fingerprint_atlas_phase_gamma.py`

**Tests:** `Build_Docs/Reports/hardened_dual_arm_probe/archived_tests/test_hardened_dual_arm_probe.py` is currently archived; un-archiving + re-running under the new import path is part of the dissection gate (criterion 3, bit-match).

## Layer manifest registration

Per GAP-011: "Wire its protocols into LAYER_MANIFEST."

Need to declare:
- The producer protocol (what the probe emits — `HardenedProbeResult` with `hardened_status`, 6-condition checklist, validity stamp, underpromotion reasons).
- The consumer protocol (what it accepts — `DualArmConfig` shape, fixture records).

Pattern reference: GAP-003 `TYPED_ULP_PROTOCOL` / `FINITE_TYPED_ULP_PROTOCOL` in `src/lloyd_v4/primitives/typed_ulp.py`. The probe will have larger protocols since it composes multiple inputs.

## Suggested step ordering for the next session

1. **Decide the destination** (`probes/` vs `branch/` vs `evals/probes/`) — read existing layouts, pick.
2. **Decide v10/v11 strategy** (lift both / refactor away / transitional import) — option (B) preferred.
3. **Read the full 593-line source** + the archived test file to inventory the dissection-gate evidence (constants, theorems, validity stamps).
4. **Draft the L3 result dataclass + protocols** in the new module.
5. **Move + update imports** in the 2 scratch consumers; un-archive the test file under the new path.
6. **Update LAYER_MANIFEST.json + .md** with the new module + protocols.
7. **Bit-match run** of the archived test against the moved module.
8. **Ledger update:** mark Transplant 2 complete; bump the `substrate-construction-transplant-arc` Status / Last result / Next concrete step.

## Estimated effort

Larger than Transplant 1 was (Transplant 1 was ~one session of substantive work + several sessions of consumer migrations). Transplant 2 is one substantial design decision (architectural placement) + a code move + a dependency-chain resolution. Realistic estimate: 1-2 focused sessions if the dependency strategy is option (B), 1 session if option (C).

---
