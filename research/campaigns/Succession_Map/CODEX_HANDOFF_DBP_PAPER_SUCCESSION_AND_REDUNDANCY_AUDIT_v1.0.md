# Codex handoff: DBP paper succession and redundancy audit v1.0

## Mission

Work from the live Cella Framework and Lloyd Mathematics Encyclopedia repositories. Research the full DBP-related paper and theorem corpus, identify overlap and redundancy, check the expanded on-disk library for stronger or overlooked work, and produce a theorem-level succession map.

The central question is not merely whether two documents discuss the same topic. It is:

> Does a newer canonical paper preserve every mathematical contribution of an older document, under the same or weaker hypotheses, while adding stronger results—so that the older document has no remaining unique mathematical, proof, computational, or expository value except historical provenance?

Do not edit, delete, move, or retire source documents during this task. Produce the evidence-backed map and recommendations first. “Retire” means “eligible to move to a historical archive after maintainer review,” never automatic deletion.

This is a repository-led research audit. The named files below are required starting points, not a closed list. Expand the audit whenever repository search, the Encyclopedia, the artifact ledger, citations, or dependency references reveal additional relevant material.

## Operating principles

1. Search the actual repositories before accepting any handoff, report, index, filename, or old gap statement as current.
2. Mathematical statements, proofs, derivations, exact workings, counterexamples, and hypotheses determine succession. Campaign status prose does not.
3. A document is not redundant merely because its headline theorem appears elsewhere. Preserve it if it contains a unique proof, construction, normalization, example, counterexample, algorithm, boundary case, or precise open problem that the proposed successor does not preserve.
4. A later paper may supersede an earlier theorem statement while the earlier document remains a useful proof dossier or computational supplement. Classify those separately.
5. Hashes may establish byte identity or mirror duplication. They are not mathematical evidence and must not become release gates.
6. Do not generate certificate bundles, schemas, checkpoint chains, digests, or dedicated verification programs for this audit. Existing exact computations may be inspected and cited. The required output is one coherent Markdown report.
7. Do not rerun expensive symbolic jobs merely to repeat a result already supported by retained proof workings. Run a focused calculation only when necessary to resolve a concrete mathematical conflict or ambiguity.
8. Preserve unrelated dirty-worktree changes. Begin with read-only discovery and keep the audit itself non-destructive.
9. Do not impose an arbitrary upper bound on the corpus. If additional relevant documents are found, include them and record why they entered the audit.

## Repository discovery

Do not assume repository locations from this handoff. Locate the live repositories and establish their current state.

Record:

- absolute repository roots;
- current branches and commits;
- `git status --short` for each repository;
- applicable `AGENTS.md` or repository instructions;
- the current Encyclopedia entry point, manifest, README, and source registry;
- the current artifact ledger and its generation date;
- whether the previously reported commits `4f016aa` for Cella Framework and `c964366` for the Encyclopedia are current, ancestors, or obsolete.

Use `rg --files` and `rg` as the primary discovery tools. Search both filenames and contents. Do not rely on a generated HTML index alone when source Markdown, TeX, theorem files, or publication packages are available.

## Expanded-library census

Locate and inspect the latest `LEDGER.csv`. The supplied session ledger recorded 547 rows and 508 unique artifact identities across Cella Framework and Lloyd Engine V4, but the live repository is authoritative.

Reconcile the ledger against:

- actual repository files;
- the Mathematics Encyclopedia source registry;
- registered campaign artifacts;
- completed-paper directories;
- theorem and lemma directories;
- derivations and proof dossiers;
- publication packages;
- historical and superseded directories;
- duplicate mirrors and renamed copies;
- files omitted from the ledger but cited by canonical papers;
- files registered in the ledger but missing from disk;
- files with the same title but materially different contents.

Use byte hashes only to identify exact duplicates. For nonidentical variants, compare their mathematical content and provenance rather than assuming the newest timestamp or highest version suffix is authoritative.

The audit must distinguish:

1. exact byte mirrors;
2. formatting-only variants such as source/PDF pairs;
3. renamed copies with identical mathematics;
4. earlier theorem versions genuinely strengthened later;
5. parallel papers with different mathematical roles;
6. conflicting variants requiring maintainer review;
7. historical planning material that never became a proof source.

## Required starting corpus

The following families must be researched. Add further items discovered through citations, references, the ledger, or the Encyclopedia.

### Paper I: role covers and active recharting

Start with:

- `dbp_orbit_calculus.tex`;
- `CCE_8_FINITE_TOWER_NATURALITY_THEOREM_v1.0.md`;
- `Gauge_Channel_Transport_Law.md`;
- `Canonical_Invariant_Reduction_Theorem.md`;
- `Theorem_8_1_Curvature_Orbit_Correction.md` and its TeX/PDF sources;
- `role_channel_anisotropy.pdf`;
- `gtd_vs_dbp.pdf`;
- older role-channel briefs, reports, and exact campaign outputs referenced by these sources.

Test whether Paper I already subsumes the older orbit, transport, reduction, and curvature-orbit papers, or whether those sources retain unique theorems or proofs. Treat CCE-8 finite-tower naturality as a possible strengthening of Paper I’s finite-order recharting, not as proof of infinite-germ convergence or global gluing.

### Paper II and the local-curvature paper

Start with:

- `lead7_kn_n3_dbp_metric.tex` and its current render;
- `pfc_normal_forms.tex` and its current render;
- `LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0.md`;
- the corresponding weighted-jet proof program;
- `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md`;
- `LOCAL_CURVATURE_CALCULUS_COMPANION.md`;
- `Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt`;
- `LEAD7_masscharge_zeros_theorem.md`;
- LEAD7 candidate, pole-order, pullback, retrodiction, and extremal-sign reports;
- the PFC and curvature-valence briefs, claims, preregistrations, and research logs.

Determine whether these form:

- two genuinely distinct papers—general local calculus and Kerr–Newman application;
- one paper plus a redundant companion layer;
- or a consolidation in which one source preserves all mathematical content of another.

In particular compare:

- the general diagonal quadratic-collapse law;
- the variable-transverse weighted-jet strengthening;
- the nondegenerate condition
  `P1/P0 + R1/R0 != 0`;
- the Kerr–Newman strict negative extremal coefficient;
- the parity-fixed `-m(m+5)/B` law;
- the codimension-two Newton-wedge and vertex rule;
- proof methods and hypotheses;
- unique examples and open higher-codimension questions.

Do not conflate diagonal local-germ results with the still-open off-diagonal tensorial role-rechart covariance problem.

### Paper III: DBP elliptic periods, cycles, and continuation

Start with:

- `DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md`;
- `DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1.md`;
- `DBP_NATIVE_RELATIVE_PERIOD_ROUTE_THEOREM_v1.0.md`;
- `DBP_SURFACE_TO_LINK_CLOSEOFF_v1.0.md`;
- `DUAL_CONSTANT_CLOSEOFF.md`;
- `DBP_DUAL_SURFACE_CYCLE_STAGE1_v0.1.md`;
- `DBP_DUAL_SURFACE_CYCLE_STAGE2_v0.1.md`;
- `DBP_DUAL_SURFACE_CYCLE_STAGE3_v0.1.md`;
- the CCE-2 corridor theorem, calibration, insertion note, and divisor reduction;
- the CCE-3 relative-class theorem and retained mathematical report;
- `DBP_CCE5_ABSOLUTE_CALIBRATION_THEOREM_v1.0.md`;
- CCE-5 full-puncture and connection results;
- `DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_THEOREM_v1.0.md`;
- the CCE-6 Paper III insertion note and mathematical package;
- the native evaluator theorem/report only insofar as it contains mathematical formulas or constructions not already in Paper III;
- `16-DBP_Curvature_Constants_Corrected_Formulation.md` and earlier curvature-constant summaries.

Build a theorem-by-theorem absorption table. Check whether the consolidated Paper III actually preserves:

- every Landen and trace identity;
- surface-to-link reduction;
- dual boundary and surface-cycle constructions;
- full convergence and boundary arguments from Stages 1–3;
- native morphisms and coefficient separation;
- exact lateral corrections `lambda_up = B`, `lambda_down = -B`;
- the released corridor matrices;
- the fixed-curve comparison `(a,b,c)=(1,0,0)`;
- the exact limits of the native swept surface image;
- the remaining full-lattice and full-parameter-plane problems.

If Paper III states a theorem but delegates essential proof workings to an older dossier, that dossier is not fully redundant. Classify it as a retained proof appendix unless the workings are copied into or permanently linked from the canonical paper.

### Paper IV: Galois horizon and Kummer covers

Start with:

- `galois_horizon_cover_v1_0.tex` and its publication package;
- `self_glue_monodromy.tex` and earlier variants;
- `KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md`;
- `ROTATING_KUMMER_RANK_JUMP_LEMMA_REPORT_2026-07-10.md`;
- `ALL_K_MONODROMY_THEOREM_NOTE_2026-07-10.md`;
- `WREATH_COVER_INERTIA_BRANCH_STRATIFICATION` variants;
- normalized-incidence and realization-poset reports;
- Macaulay2 realization-poset workflows and retained outputs;
- Galois `k`-ellipse research maps and strategic memos;
- R5/R6/R7/R9 logs, proofs, audits, and draft variants;
- CCE-7 stage, gap, normalized-incidence import, static-root, and transport work.

Determine which theorem reports are fully absorbed into the current Paper IV publication package and which remain necessary supplements. The normalized incidence cover, true relative Jacobian branch ideal, generic inertia catalogue, and stored realization-poset outputs are established starting points. Do not label them as missing work.

Keep exact loop representatives, complex braid execution, and cross-transport separate if they remain open; do not retire the only document that specifies those residual problems precisely.

### Paper V and ensemble-level sources

Start with:

- `SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md`;
- `R3_AC_FOLD_INDEPENDENT_REALIZATION_THEOREM_v1.0.md`;
- `DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md`;
- all `DBP_UNIFIED_THEOREM_SPINE_DRAFT` variants;
- the post-8 authority manifest, outcome ledger, and final report;
- `DBP_CCE_ARTIFICIAL_RESTRICTION_LIVE_RECONCILIATION_v1.0.md`;
- the current Encyclopedia synthesis entries for SQG, R3, CCE-8, and the DBP arms;
- any newer capstone or selected-skeleton paper found on disk.

Do not assume that Paper V exists merely because its foundations exist. Distinguish:

- category and native-morphism foundations already proved;
- closure operations already proved in particular domains;
- the exact R3 realization and winding-parity functor;
- refuted unreduced carrier equivalence;
- the still-missing DBP-arm reduction functors;
- componentwise comparison diagrams;
- general closure under additional operations;
- three-way coherence.

The architecture and unified spine may become historical planning/ledger artifacts, but only after confirming that all valid theorem ownership, dependency, and residual-gap information is preserved elsewhere.

## Theorem-unit extraction

For every candidate document, record each distinct mathematical unit:

- stable identifier or a new audit identifier;
- theorem/lemma/proposition/construction name;
- exact statement;
- hypotheses and coefficient ring;
- carrier, quotient, selection, wall, and morphism data when relevant;
- proof location and proof method;
- exact formulas or matrices;
- examples or hostile cases;
- counterexamples and negative results;
- open problems and nonclaims;
- dependencies and downstream citations;
- proposed canonical successor.

Do not award novelty twice when the same theorem appears in multiple reports. Conversely, do not merge units merely because they share vocabulary.

## Subsumption test

An older document may be recommended for historical-only status only if all of the following are established:

1. Every mathematical unit maps to an explicit location in a retained successor.
2. The successor uses the same or weaker hypotheses, or any stronger hypothesis is justified and the lost generality is documented.
3. Exact constants, signs, orientations, coefficient rings, boundary conventions, and normalization choices are preserved.
4. Proof substance is retained in the successor or in a separately retained proof supplement.
5. Unique examples, counterexamples, and failure modes are preserved or deliberately catalogued as historical only.
6. No current source cites the older document as the sole proof authority for a live theorem.
7. No unresolved contradiction exists between the older and newer statements.
8. The proposed successor is itself canonical and present on disk.

If any condition fails, classify the document as retained, merge-required, proof-supplement, or unresolved—not retired.

## Classification vocabulary

Assign exactly one primary disposition to each artifact:

- `CANONICAL_RETAIN` — current paper or theorem source.
- `INDEPENDENT_COMPANION` — overlaps but has a distinct mathematical role.
- `MERGE_THEN_RETIRE` — unique material remains and must be absorbed first.
- `PROOF_SUPPLEMENT_RETAIN` — headline theorem is absorbed but detailed proof/workings remain unique.
- `COMPUTATIONAL_SUPPLEMENT_RETAIN` — unique reproducible exact computation remains useful.
- `HISTORICAL_ONLY` — fully subsumed; retain only for provenance.
- `EXACT_MIRROR` — byte-identical duplicate; designate one canonical location.
- `FORMAT_RENDER` — PDF/render paired with retained source.
- `SUPERSEDED_VARIANT` — earlier version replaced by a stronger or corrected version.
- `UNRESOLVED` — insufficient evidence, conflict, or missing successor.

For `MERGE_THEN_RETIRE`, list the exact sections or theorem units that must be transferred. For `HISTORICAL_ONLY`, identify the retained successor and explicitly state that no unique mathematical unit remains.

## Known status constraints to preserve

Use these as propositions to verify against the live sources, not as conclusions to copy blindly:

- Paper I proves rational recharting at every finite order; CCE-8 strengthens this to naturality across the finite truncation tower. Infinite analytic convergence and global chart gluing are not implied.
- Paper II’s Kerr–Newman sign/noncancellation result is closed. The general variable-transverse diagonal coefficient law is closed on the nondegenerate stratum. Off-diagonal role-rechart covariance remains separate.
- Paper III has exact released-corridor transport, exact compact corrections, `(a,b,c)=(1,0,0)`, and native surface clearance. Full regular-plane monodromy and whole-surface saturation are not thereby closed.
- Paper IV already contains the normalized incidence model and generic inertia foundation. Complex loops, braid execution, and cross-transport may remain open.
- R3 is an independent exact AC-fold realization. Its skeleton functor has kernel `2Z` and is not faithful. This does not by itself prove three-way coherence.
- Full unreduced carrier equivalence is refuted. Any positive equivalence theorem must concern explicit reductions or a common selected skeleton.
- The native CCE-6 surface image has rank four inside a rank-twelve target; do not relabel the native image as the whole surface lattice.

If the repository contains later work that strengthens or overturns any of these, follow the mathematics and document the change.

## Required output

Create exactly one final Markdown artifact:

`DBP_PAPER_SUCCESSION_AND_REDUNDANCY_MAP_v1.0.md`

It must be self-contained and contain:

1. repository and corpus snapshot;
2. canonical paper ensemble after the audit;
3. theorem-level succession matrix;
4. document disposition table;
5. exact-mirror and variant groups;
6. `CANONICAL_RETAIN` list;
7. `INDEPENDENT_COMPANION` list;
8. `MERGE_THEN_RETIRE` list with required transfers;
9. `PROOF_SUPPLEMENT_RETAIN` and `COMPUTATIONAL_SUPPLEMENT_RETAIN` lists;
10. `HISTORICAL_ONLY` retirement candidates with successor evidence;
11. unresolved conflicts or missing sources;
12. genuine open mathematical walls that survive consolidation;
13. a minimal editorial sequence for performing later merges safely;
14. a concise proposed post-consolidation directory architecture.

Use direct repository paths, theorem names, section anchors, and line numbers where practical. Include short paraphrases rather than copying long passages. A compact Mermaid or ASCII succession graph is welcome if it clarifies the ensemble, but the tables and prose must remain independently understandable.

Do not create JSON companions, digests, bundles, schemas, or a second report. Temporary local analysis files may be used but must not be committed as campaign artifacts.

## Expected succession hypotheses to test

These are useful starting hypotheses, not predetermined verdicts:

1. `pfc_normal_forms.tex` and `lead7_kn_n3_dbp_metric.tex` are probably independent companion papers: general local theory versus Kerr–Newman realization. The local-curvature companion and earlier LEAD7 reports may be merge-then-retire or historical-only.
2. Consolidated Paper III is intended to absorb the Landen theorem, native route theorem, surface-to-link close-off, and the Stage 1–3 theorem statements. Detailed Stage workings may remain proof supplements unless fully reproduced.
3. CCE-2, CCE-5, and CCE-6 theorem insertions may supersede their stage reports mathematically, while stage reports may retain unique derivations.
4. The Paper IV publication package may subsume many Galois research maps and theorem notes, but Macaulay2 workflows and exact realization-poset outputs may remain computational supplements.
5. `SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md` and the R3 theorem are not redundant with an architecture document. The architecture and unified spine may be historical once their live dependencies and open walls are preserved in the succession map or a future capstone.
6. Evaluator release reports belong to software/reproducibility documentation unless they contain mathematical constructions absent from Paper III.

Confirm, refine, or reject each hypothesis from the live source evidence.

## Completion conditions

The audit is complete only when:

- every relevant artifact discovered in the expanded census has a disposition;
- every `HISTORICAL_ONLY` candidate has a named canonical successor;
- every theorem unit in a retirement candidate maps to a retained source;
- every unique proof or exact construction is preserved somewhere;
- all exact mirrors and materially different variants are distinguished;
- no open problem is accidentally declared closed through document consolidation;
- no closed theorem remains described as a missing foundation;
- no repository source has been edited, moved, or deleted;
- the single succession-map report is coherent enough for the maintainer to approve a later consolidation pass without reconstructing this audit.

## Final response to the maintainer

Report:

- the path to `DBP_PAPER_SUCCESSION_AND_REDUNDANCY_MAP_v1.0.md`;
- the number of artifacts and theorem units audited;
- counts by disposition;
- the strongest immediately safe retirement candidates;
- documents that must first receive transferred material;
- unresolved mathematical or source-authority issues;
- confirmation that no source papers were modified or retired.

