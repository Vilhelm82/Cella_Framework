# Cella Continuation Engine campaign

This directory is organized by campaign task. Start here, then enter exactly
one task folder; do not search the former flat root for stage artifacts.

| Folder | Task scope | Principal contents |
|---|---|---|
| `00_campaign_authority/` | Campaign-wide authority and reconciliation | Cross-stage reports, gap ledgers, scope-expansion audit |
| `01_cce0_recertification/` | CCE-0 baseline recertification | Frozen baseline lock and recertification reports |
| `02_cce1_pathfinder/` | CCE-1 Pathfinder adapter | Stage report, behavior inventory, admitted-domain schema, refusal matrix |
| `03_cce2_corridors/` | CCE-2 exact DBP corridors | Route manifests, clearance theorem and certificates, lateral calibration, standalone replays |
| `04_cce3_relative_classes/` | CCE-3 typed relative classes | Coefficient rings, class relations, exact construction and replay |
| `05_cce4_evaluator/` | CCE-4 bounded evaluator | Evaluator reports, exact enclosure benchmark and replay |
| `06_cce5_connection/` | CCE-5 relative connection | Exact K/E/Pi connection, absolute calibration, puncture-germ audit and replay |
| `07_cce6_surface/` | CCE-6 native surface sweep | Completed supplied package, engine-import records, topology expansion and replay |
| `08_cce7_horizon/` | CCE-7 horizon/static chamber | Stage records and normalized-incidence inertia import |
| `09_cce8_role_cover/` | CCE-8 finite role cover | Stage records and finite-tower naturality theorem |
| `10_post8_universalization/` | Post-8 universalization and R3 | Outcome ledger, LEAD-7 audit, independent AC-fold realization |
| `shared_schemas/` | Cross-stage data contracts | Request/result schema |
| `agent_tasks/` | Incoming work specifications | Handoffs and scope-revision instructions; not mathematical evidence by themselves |

## Replay entry points

- CCE-2: `03_cce2_corridors/verify_dbp_exact_corridor_paths.py`,
  `verify_dbp_corridor_clearance.py`, and
  `verify_dbp_corridor_lift_and_lateral_class.py`
- CCE-3: `04_cce3_relative_classes/verify_cce3_relative_class_certificates.py`
- CCE-4: `05_cce4_evaluator/verify_cce4_bounded_evaluation.py`
- CCE-5--8 direct mathematics: `00_campaign_authority/verify_cce5_8_release_bundle.py`
- CCE-5 expansion: `06_cce5_connection/verify_cce5_full_puncture_germs.py`
- CCE-6 supplied theorem: `07_cce6_surface/CCE_6_COMPLETE_PACKAGE_v1.0/verify_dbp_native_surface_sweep_clearance.py`
- CCE-6 topology expansion: `07_cce6_surface/verify_cce6_whole_surface_topology.py`
- Post-8 direct mathematics: `10_post8_universalization/verify_post8_promoted_bundle.py`
- LEAD-7 symbolic expansion: `10_post8_universalization/verify_lead7_variable_transverse_laurent.py`

Run engine-backed replays from the repository root with
`PYTHONPATH=engine/src`. The supplied CCE-6 package accepts `--root` when a
different checkout or upload layout is being replayed.

## Retrieval and authority notes

- Folder placement identifies the task that produced an artifact; it does not
  turn a report into a restriction on later mathematical investigation.
- Campaign authority and stage reports are reference points. Identified logical
  expansions remain subjects for investigation and belong in the applicable
  stage or post-8 folder.
- Files in `agent_tasks/` describe requested work. Use the resulting theorem,
  certificate, implementation, and replay artifacts as evidence.
- `research/campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR/pathfinder_m1_scout.py`
  is a valid campaign-local scout. It is not the primary production Pathfinder
  under `engine/src/cella/pathfinder/`; choose between them by task scope rather
  than treating either location as globally forbidden or deprecated. See
  `00_campaign_authority/PATHFINDER_IMPLEMENTATION_CLASSIFICATION_v1.0.md`.

The former flat-root paths were retired by the task-folder reorganization on
2026-07-14. Per-artifact hash bundles and checkpoint schemas were removed on
the same date: mathematical proof and exact replay are the campaign evidence.
The CCE-0 Pathfinder baseline lock is retained solely as the comparison
baseline for later Pathfinder behavior.
