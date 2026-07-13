# Reference_Material Handoff Index

This folder is reference material for Cella/DBP work. It is deliberately not a build
dependency. Status words inside these documents - "proven", "certified", "standing",
"closed", "accepted", "ratified" - are claims from origin material, not evidence for
Cella until re-proven in-repo with fresh derivation/code, exact arithmetic where
applicable, and byte-stable verification.

## Current Layout

- `papers/current/` - active paper sources, paper PDFs, and current theorem/brief notes.
- `reference_state/` - current state dashboard, current R&D brief, and latest calc-log diary.
- `campaign_outputs/` - campaign reports, ledgers, schemas, fixtures, and proof-extraction outputs.
- `framework_design/` - Cella design handoff notes.
- `scripts/` - current helper/certification scripts and machine-readable outputs.
- `archive/older_versions/` - superseded root-level versions moved out of the active path.
- `archive/old_program_sources/` - old-program source and archaeology material retained for retrodiction only.

## Consolidation Decisions

- Current standing dashboard: `reference_state/DBP_STANDING_RESULTS_v1.1.md`.
  Superseded: `archive/older_versions/DBP STANDING RESULTS.md`.
- Current R&D brief: `reference_state/DBP_RnD_Directions_Updated_With_Citations.md`.
  Superseded: `archive/older_versions/DBP_RnD_Directions_Exact_Role_Channel_Geometry.md`.
- Current LEAD-7 metric direction: `papers/current/LEAD7_Candidate_F_Elementary_Pair_Channel_Inverse_Metric.md`.
  Superseded: `archive/older_versions/LEAD7_Candidate_D_Output_Channel_Norm_Inverse_Metric.md`.
- Current Theorem 8.1 correction note: `papers/current/Theorem_8_1_Curvature_Orbit_Correction.md`.
  Superseded source note: `archive/older_versions/Theorem_8_1_New_Math_Extension.md`.
- Current Stage 3 script/report pair: `scripts/stage_3_certification_script_corrected.py` and
  `scripts/stage3_report_corrected.json`.
  Superseded: `archive/older_versions/stage_3_certification_script_v2.py` and
  `archive/older_versions/stage3_report_v2.json`.
- `papers/current/self_glue_monodromy.tex` and `papers/current/self_glue_monodromy.txt`
  are both retained as current format companions, not treated as older versions.
- `archive/old_program_sources/Calc_logs/dbp four role calc log v8.md` is retained as a
  historical duplicate within the snapshot series; the active latest diary copy is
  `reference_state/dbp_four_role_calc_log_v8.md`.

## Glossary

- `origin material` - Imported historical documents, scripts, reports, and papers used as reference.
- `current` - The latest visible version retained in the active reference path.
- `superseded` - An older or corrected version moved to `archive/older_versions/`.
- `old-program source` - Historical source/eval material moved under `archive/old_program_sources/`.
- `exact-Q` - Rational arithmetic over exact quantities, not float tolerances.
- `carrier` - A structured object carrying invariant/channel/account data.
- `channel` - A component of a decomposed carrier, usually self, coupling, or interaction.
- `RoleChSpec` - Active role-channel specification built from output-role graph charts.
- `gauge` - Defining-function freedom such as Hessian shifts by `g a^T + a g^T`.
- `retrodiction` - Checking current work against old-program claims without treating them as proof.
- `campaign output` - A report, ledger, fixture file, or schema emitted by a bounded eval campaign.

## Active Papers And Briefs

- `papers/current/Canonical_Invariant_Reduction_Theorem.md` - States the channel/gauge reduction theorem from channel vectors to invariant curvature sums.
- `papers/current/DBP_Curvature_Constant_Summary.pdf` - One-page summary of the DBP keystone total-curvature constant and elliptic-integral reduction.
- `papers/current/DBP_Curvature_Constants_Corrected_Formulation.md` - Corrected arithmetic-track formulation of DBP curvature constants and exact elliptic parameters.
- `papers/current/DBP_Curvature_Role_Reduction.md` - Detailed role-reduction paper/brief tying curvature channels, gauge structure, and active role geometry.
- `papers/current/Gauge_Channel_Transport_Law.md` - Describes how gauge motion transports channel allocations while preserving invariant sums.
- `papers/current/LEAD7_Candidate_F_Elementary_Pair_Channel_Inverse_Metric.md` - Current LEAD-7 metric direction preserving elementary pair-channel zeros.
- `papers/current/Lead_C_Role_Singularity_Valuation_Theorem_Brief.md` - Brief on role-singularity valuation and boundary behavior.
- `papers/current/Theorem_8_1_Curvature_Orbit_Correction.md` - Corrects the passive-orbit issue in Theorem 8.1 by requiring active role recharting.
- `papers/current/Three_Channel_KG_New_Math_Extension.md` - Expands three-channel `K_G` to broader elementary curvature and channel-density directions.
- `papers/current/Three_Channel_KG_Strong_Spec.md` - Canonical strong specification for signed three-channel Gaussian curvature `K_G`.
- `papers/current/dbp_orbit_calculus.tex` - LaTeX source for the active role-jet orbit calculus paper.
- `papers/current/gtd_vs_dbp.pdf` - Paper comparing GTD and DBP curvature readings on thermodynamic surfaces.
- `papers/current/role_channel_anisotropy.pdf` - Paper on role-channel anisotropy as an exact local invariant.
- `papers/current/self_glue_monodromy.tex` - LaTeX source for the self-composed constraint-surface monodromy paper.
- `papers/current/self_glue_monodromy.txt` - Text/handoff form of the self-glue monodromy paper.

## Reference State

- `reference_state/DBP_STANDING_RESULTS_v1.1.md` - Canonical standing-results dashboard that supersedes v1.0 and older dashboard copies.
- `reference_state/DBP_RnD_Directions_Updated_With_Citations.md` - Current R&D direction brief using the standing-results dashboard and citation context.
- `reference_state/dbp_four_role_calc_log_v8.md` - Latest full calc-log diary snapshot, retained as history rather than current state.

## Campaign Outputs

### Precision Flow

- `campaign_outputs/precision_flow/CAMPAIGN_REPORT-1.md` - Precision Flow close-out report covering stages A-D, exact grading, failures, fixes, and disposition.

### Three Channel KG

- `campaign_outputs/three_channel_kg/CENSUS.md` - Cubic role-branch census with monodromy, branch strata, and certificate summary.
- `campaign_outputs/three_channel_kg/CLAIM_LEDGER.md` - Append-only claim ledger for the c001 `three_channel_kg` campaign.
- `campaign_outputs/three_channel_kg/FIXTURES.md` - Fixture definitions and pins for the three-channel K_G campaign.
- `campaign_outputs/three_channel_kg/SCHEMA.md` - Record/schema description for the three-channel K_G campaign output.

### Symbolic RoleChSpec

- `campaign_outputs/symbolic_rolechspec/EXCEPTIONAL_LOCUS_REPORT.md` - Exceptional-locus report for symbolic RoleChSpec proof extraction.
- `campaign_outputs/symbolic_rolechspec/FAITHFULNESS_SEARCH_REPORT.md` - Faithfulness search report for RoleChSpec/gauge-obstruction equivalence.
- `campaign_outputs/symbolic_rolechspec/GAUGE_INVARIANCE_REPORT.md` - Gauge-invariance report for RoleChSpec under same-gradient gauge motion.
- `campaign_outputs/symbolic_rolechspec/GAUGE_NORMAL_FORM_PROOF.md` - Proof note for gauge normal form and obstruction coordinates.
- `campaign_outputs/symbolic_rolechspec/INJECTIVITY_IDEAL_REPORT.md` - Injectivity ideal report for recovering obstruction data from RoleChSpec forms.
- `campaign_outputs/symbolic_rolechspec/MUTATION_REPORT.md` - Mutation-control report for symbolic RoleChSpec proof extraction.
- `campaign_outputs/symbolic_rolechspec/RAW_CHART_ROLECHSPEC_REPORT.md` - Raw chart-level RoleChSpec report before gauge-normal reduction.
- `campaign_outputs/symbolic_rolechspec/SELF_GLUE_STRESS_REPORT.md` - Self-glue stress report for adversarial RoleChSpec cases.
- `campaign_outputs/symbolic_rolechspec/SYMBOLIC_ROLECHSPEC_FORMULAS.md` - Symbolic formula report for RoleChSpec components.

## Framework Design

- `framework_design/Cella_Kernal_design.txt` - Cella pathfinder/route-planning design handoff note. Filename spelling is retained from source.

## Current Scripts

- `scripts/dual_constant_comp.py` - Helper script for dual constant comparison.
- `scripts/stage_3_certification_script_corrected.py` - Current corrected Stage 3 certification script.
- `scripts/stage3_report_corrected.json` - Current corrected Stage 3 machine-readable report.

## Archive: Older Versions

- `archive/older_versions/DBP STANDING RESULTS.md` - Superseded standing-results dashboard copy, replaced by v1.1.
- `archive/older_versions/DBP_RnD_Directions_Exact_Role_Channel_Geometry.md` - Superseded R&D brief, replaced by the cited updated version.
- `archive/older_versions/LEAD7_Candidate_D_Output_Channel_Norm_Inverse_Metric.md` - Superseded LEAD-7 Candidate D note, replaced by Candidate F.
- `archive/older_versions/Theorem_8_1_New_Math_Extension.md` - Earlier Theorem 8.1 extension note, superseded for role-curvature use by the correction note.
- `archive/older_versions/stage_3_certification_script_v2.py` - Superseded Stage 3 v2 certification script.
- `archive/older_versions/stage3_report_v2.json` - Superseded Stage 3 v2 report.

## Archive: Old Program Sources

- `archive/old_program_sources/30_GLOSSARY_DISAMBIGUATION.md` - Name-collision glossary for old DBP/V4 program terms.
- `archive/old_program_sources/THE_ENGINE_CLAIM_LEDGER.md` - Old engine claim-ledger snapshot.
- `archive/old_program_sources/gauge_channel_transport_probe.py` - Old gauge/channel transport probe source.
- `archive/old_program_sources/theorem_8_1_curvature_orbit_probe.py` - Old Theorem 8.1 curvature-orbit probe.
- `archive/old_program_sources/theorem_8_1_role_jet_probe.py` - Old Theorem 8.1 role-jet probe.
- `archive/old_program_sources/Calc_logs/dbp four role calc log.md` - Earliest archived four-role calc-log snapshot.
- `archive/old_program_sources/Calc_logs/dbp four role calc log v2 .md` - Archived four-role calc-log v2 snapshot.
- `archive/old_program_sources/Calc_logs/dbp four role calc log v3.md` - Archived four-role calc-log v3 snapshot.
- `archive/old_program_sources/Calc_logs/dbp four role calc log v8.md` - Archived duplicate of the latest v8 calc-log snapshot.
- `archive/old_program_sources/constant_hunt_bytecode/__init__.cpython-314.pyc` - Recovered bytecode package marker for lost constant-hunt sources.
- `archive/old_program_sources/constant_hunt_bytecode/alt_scalar.cpython-314.pyc` - Recovered bytecode for the old alternate scalar constant-hunt module.
- `archive/old_program_sources/constant_hunt_bytecode/dbp_total_curvature.cpython-314.pyc` - Recovered bytecode for the old DBP total-curvature module.
- `archive/old_program_sources/constant_hunt_bytecode/run_constant_hunt.cpython-314.pyc` - Recovered bytecode for the old constant-hunt runner.
- `archive/old_program_sources/dbp_involution_evals/dbp_carrier.py` - Old DBP involution carrier implementation.
- `archive/old_program_sources/dbp_involution_evals/harness.py` - Old DBP involution eval harness.
- `archive/old_program_sources/dbp_involution_evals/mutation_check.py` - Old DBP involution mutation-control checks.
- `archive/old_program_sources/dbp_involution_evals/rep_utils.py` - Old representation-theory utilities for DBP involution evals.
- `archive/old_program_sources/dbp_involution_evals/stage0_regression.py` - Old Stage 0 regression battery for DBP involution.
- `archive/old_program_sources/dbp_involution_evals/stageA_sym_wedge_split.py` - Old Stage A symmetric/wedge split battery.
- `archive/old_program_sources/eng2_fault_semantics/CL_ENG2_FAULT_SEMANTICS.md` - Claim ledger for the old ENG2 fault-semantics campaign.
- `archive/old_program_sources/eng2_fault_semantics/PREREG_BPRIME.md` - B-prime preregistration for ENG2 fault semantics.
- `archive/old_program_sources/eng2_fault_semantics/PREREG_DRAFT.md` - Draft preregistration for ENG2 fault semantics.
- `archive/old_program_sources/eng2_fault_semantics/PREREG_ENG2.md` - ENG2 preregistration packet.
- `archive/old_program_sources/eng2_fault_semantics/PREREG_v2.md` - Version 2 preregistration for ENG2 fault semantics.
- `archive/old_program_sources/eng2_fault_semantics/SHADOW_LAW_THEOREM.md` - Old shadow-law theorem writeup.
- `archive/old_program_sources/eng2_fault_semantics/STAGE_B_REPORT.md` - Stage B ENG2 fault-semantics report.
- `archive/old_program_sources/eng2_fault_semantics/STAGE_BPRIME_REPORT.md` - Stage B-prime ENG2 fault-semantics report.
- `archive/old_program_sources/eng2_fault_semantics/bprime_battery.py` - B-prime battery runner for ENG2 fault semantics.
- `archive/old_program_sources/eng2_fault_semantics/bprime_verdicts.json` - B-prime verdict payload.
- `archive/old_program_sources/eng2_fault_semantics/eng2_battery.py` - ENG2 campaign battery runner.
- `archive/old_program_sources/eng2_fault_semantics/fixtures_bprime.json` - B-prime fixture payload.
- `archive/old_program_sources/eng2_fault_semantics/fixtures_eng2.json` - ENG2 fixture payload.
- `archive/old_program_sources/eng2_fault_semantics/fixtures_stageB.json` - Stage B fixture payload.
- `archive/old_program_sources/eng2_fault_semantics/freeze_pins.sha256` - Freeze pins for ENG2 fault semantics.
- `archive/old_program_sources/eng2_fault_semantics/freeze_pins_bprime.sha256` - Freeze pins for B-prime ENG2 artifacts.
- `archive/old_program_sources/eng2_fault_semantics/freeze_pins_eng2.sha256` - Freeze pins for ENG2 artifacts.
- `archive/old_program_sources/eng2_fault_semantics/prediction_verdicts.json` - Prediction verdict payload for ENG2 fault semantics.
- `archive/old_program_sources/eng2_fault_semantics/shadow_law_verify.py` - Verification script for the old shadow-law theorem.
- `archive/old_program_sources/eng2_fault_semantics/stageB_battery.py` - Stage B battery runner for ENG2 fault semantics.
- `archive/old_program_sources/shape_witness/BRIEF_v1_DRAFT.md` - Draft brief for the old shape-witness campaign.
- `archive/old_program_sources/shape_witness/CLAIM_LEDGER.md` - Claim ledger for the old shape-witness campaign.
- `archive/old_program_sources/shape_witness/PROOF_CL_F1.md` - Proof note for shape-witness claim CL-F1.
- `archive/old_program_sources/shape_witness/WALL_VERDICT.md` - Wall-verdict report for the shape-witness campaign.
- `archive/old_program_sources/shape_witness/WITNESS_PREDECL.md` - Witness predeclaration for the shape-witness campaign.
