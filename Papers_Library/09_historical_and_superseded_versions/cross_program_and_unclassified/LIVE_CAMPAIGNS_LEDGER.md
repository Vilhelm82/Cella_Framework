# V4 Live Campaigns Ledger

**Purpose:** Single source of truth for what is in flight in V4 *right now*, so a fresh session does not restart an existing campaign under a new name.

**Last updated:** 2026-05-26

---

## How to use this file

**Before proposing any new investigation, campaign, or report:**

1. Scan the **Active campaigns** section. If your proposed work fits inside an active campaign — even loosely — *continue that campaign*, do not start a new one.
2. Scan the **Aliases / known restart traps** section. If your proposed naming matches a known restart trap, stop and use the canonical name.
3. Scan the **Recently closed campaigns** section. If the work has already been done, cite the closed campaign and ask the user whether you should be extending it or doing something genuinely new.
4. Scan the **Open questions** section. If your work targets Q1–Q6, read the current status before proposing methodology.

**Every session must update this file** for any campaign it touches: change the *Last touched*, *Last result*, *Next concrete step*, and *Blockers* fields. The frozen fields (canonical name, purpose, scope, aliases) only change when the campaign is formally renamed or merged.

This file is short by design (target: under 400 lines). It is an index, not a synthesis. For depth: cite the underlying report directory and session handoff.

---

## Active campaigns

### substrate-construction-transplant-arc

| Field | Value |
|---|---|
| **Canonical name** | `substrate-construction-transplant-arc` |
| **Aliases / merged from** | none (new arc opened 2026-05-26 from task050 substrate-layer audit) |
| **Purpose (frozen)** | Close the 12 primitive gaps identified by task050, lifting V3/scratch implementations into the V4 substrate per `Build_Docs/Architecture/SUBSTRATE_CONSTRUCTION.md`. Each lift is a "transplant" with a 4-part dissection gate (constants measured, theorems registered, bit-match or documented divergence, modelling commitments declared). |
| **Scope (frozen)** | The 12 GAP items from `Reports/task050/parent_primitive_gaps.md`. K_G (GAP-005) explicitly **deferred** until substrate-invariant-search Gate 2 closes. No new gaps may be opened inside this arc without an audit. |
| **Status** | Active; **Transplant 1 (GAP-003 `typed_ulp`) complete** 2026-05-27 — primitive landed in `src/lloyd_v4/primitives/typed_ulp.py` with both float64 and float32 paths (precision-dispatch kwarg). **45/45 tests green** (26 float64 + 18 float32 + 1 dispatcher). Both evals consumers migrated, all 10 DRY-003 scratch sites consolidated, layer manifest + V4_GLOSSARY §13 updated (GAP-012 closed). |
| **Last touched** | 2026-05-27 |
| **Last result** | GAP-003 `typed_ulp` + GAP-012 conditioning-name disambiguation closed. DRY-003 reconciliation audit established canonical behaviour and revealed `mcg_phase_1_g1_route_divergence:ulp_float64` underflow bug on subnormals (returned 0.0 for all 8 subnormal grid points). **MCG sites migrated 2026-05-27** (`mcg_phase_1_g1_route_divergence`, `mcg_gate_3_killswitch`): bug-fix confirmed via smoke-test (now returns 2^-1074). **Float32 path added 2026-05-27** via `precision=` kwarg dispatcher (pure stdlib struct round-trip, no numpy); OverflowError saturation for values > FLT_MAX routes to ULP_NONFINITE_INF (regression-tested); kwarg renamed `format`→`precision` to match V4 evals convention (old kwarg explicitly rejected via TypeError regression test). **Evals consumers migrated 2026-05-27**: `scale_invariant_signature._ulp_of_float32` and `multi_precision_four_form.ulp_of_double` now thin wrappers; byte-compatible on grid (0 mismatches against bit-manipulation reference). **8 remaining DRY-003 scratch sites migrated 2026-05-27** (10 function bodies total): `bacl_subnormal_audit`, `bacl_invariant_audit` (×2), `c2_lattice_substrate_derivation`, `c2_lattice_sharpness_audit` (×2), `c2_lattice_binade_danger_zone`, `c2_theorem_scope_gate`, `blowup_exponent_v4_audit`, `substrate_fingerprint_atlas_phase_beta` — all parse cleanly, smoke-tested against typed_ulp reference (byte-identical on (1.0, subnormal_2^-1030, 0.0) for float64; (1.0, subnormal_2^-130, 0.0) for float32). 4 discipline-gate snapshot tests bumped (`len(primitives.__all__)` 65→80) covering task017b/024b/025/026; focused regression returncode 0. Layer manifest (.json + .md) updated; 45/45 typed_ulp tests green. |
| **Next concrete step** | (a) ~~migrate the two MCG sites~~ DONE 2026-05-27; (b) ~~migrate remaining 10 DRY-003 sites~~ DONE 2026-05-27; (c) ~~float32 variant + evals consumers~~ DONE 2026-05-27; (d) **Transplant 2 = GAP-011 hardened dual-arm probe lift** (parallelisable; may surface need for `probes/` sub-package in LAYER_MANIFEST); (e) Transplant 3 = GAP-001 `typed_sqrt` + GAP-002 `typed_log` (requires GAP-009 L1 atomicity policy resolution first); (f) Choptuik γ-bias 20-seed audit + detection threshold false-positive calibration (honesty work flagged alongside pure-noise control); (g) task045 pre-reg revision (matched-filter needs lattice-aware detection statistic now that typed_ulp exists). |
| **Blockers** | GAP-009 (L1 atomicity policy) must resolve before Transplant 3. K_G (GAP-005) blocked on substrate-invariant-search Gate 2. |
| **Anti-restart note** | Do NOT propose K_G as Transplant 1 or 2 — the legacy `V4_Primitive_Design_Proposals.md` recommendation is superseded by the task050 audit. Methodology-mandated ordering (per `SUBSTRATE_CONSTRUCTION.md §9`) is: conditioning primitive (typed_ulp) first, then typed_sqrt / typed_log, then K_G only after substrate-invariant-search closes. Do NOT mint a separate "conditioning primitive" — `typed_ulp` IS the §9 conditioning primitive; see V4_GLOSSARY §13. |
| **Source** | [Reports/task050/](Reports/task050/), [Architecture/SUBSTRATE_CONSTRUCTION.md](Architecture/SUBSTRATE_CONSTRUCTION.md), `src/lloyd_v4/primitives/typed_ulp.py`, `tests/test_typed_ulp.py`, `scratch/dry003_ulp_reconciliation_audit.py` |

### sweep_signature_probe

| Field | Value |
|---|---|
| **Canonical name** | `sweep_signature_probe` |
| **Aliases / merged from** | none |
| **Purpose (frozen)** | Maintain the Layer 1 sweep-signature screening primitive and its calibration record for finite-precision observable sweeps. |
| **Scope (frozen)** | Primitive-level observable screening via `typed_finite_difference` + `typed_log_log_slope`; no refinery wiring, alpha-probe companion calls, or new fixture families inside task035. |
| **Status** | Active; task035 implementation complete |
| **Last touched** | 2026-05-25 |
| **Last result** | task035 commit |
| **Next concrete step** | follow-up tasks: (a) floor_proximate primitive with domain-realistic calibration set, (b) optional `typed_log_log_slope` residual-statistics extension if r_squared proves insensitive, (c) alpha_probe companion-call integration |
| **Blockers** | None for the standalone primitive. Follow-up calibration sets are intentionally deferred. |
| **Anti-restart note** | Do not start a new "burden sensor" or "sweep burden" primitive; continue this campaign and keep the primitive named `sweep_signature_probe`. |
| **Source** | [Reports/task035_sweep_signature_probe/](Reports/task035_sweep_signature_probe/), [Reports/task035_sweep_signature_probe_summary.md](Reports/task035_sweep_signature_probe_summary.md) |

### alpha_probe_sweep_signature_companion

| Field | Value |
|---|---|
| **Canonical name** | `alpha_probe_sweep_signature_companion` |
| **Aliases / merged from** | none |
| **Purpose (frozen)** | Establish the companion-call integration pattern at the primitives layer: directional_alpha_probe optionally invokes sweep_signature_probe on the identical grid and attaches typed evidence for consumer disambiguation of unstable_window vs formulation-burdened cases. |
| **Scope (frozen)** | One-way companion from alpha_probe to sweep (no reverse to avoid cycles); three optional fields on AlphaProbeObservation; consumer conventions only (documented in STATUS_CALCULUS); joint calibration on the 16 GR photon-sphere cases; no new AlphaProbeStatus cells or transition rules. |
| **Status** | Active; task036 implementation complete |
| **Last touched** | 2026-05-26 |
| **Last result** | task036 commit |
| **Next concrete step** | task037 (sterbenz_audit pre-screen integration with sweep_signature_probe) |
| **Blockers** | None |
| **Anti-restart note** | Do not restart as "alpha_sweep_companion" or "joint_alpha_sweep"; this is the canonical companion call pattern campaign. |
| **Source** | [Reports/task036_alpha_probe_sweep_signature_companion/](Reports/task036_alpha_probe_sweep_signature_companion/), Build_Docs/Agent_tasks/codex_task036_alpha_probe_sweep_signature_companion.md |

### substrate-invariant-search

| Field | Value |
|---|---|
| **Canonical name** | `substrate-invariant-search` |
| **Aliases / merged from** | `mcg-discovery` (SUPERSEDED), `mcg-geometry-first` (merged 2026-05-23), `substrate-fingerprint-atlas` (parallel effort, partially absorbed) |
| **Purpose (frozen)** | Identify substrate-derived observables that capture substrate structure in a form usable downstream (G/C/M decomposition closure, L3 promotion). |
| **Scope (frozen)** | 1D operand chains and lifted-singularity multi-D fixtures. Eval-layer methodology; no substrate promotion within campaign. |
| **Status** | Active |
| **Current phase** | Authority under rewrite. Old authority `substrate_invariant_search_2026_05_23.md` retired; new authority `substrate_invariant_search_2026_05_26.md` pending. Pre-authority exploratory α-recovery characterisation completed 2026-05-26 as instrument-side input to the rewrite. |
| **Last touched** | 2026-05-26 |
| **Last result** | 2026-05-26 — Exploratory α-recovery instrument characterisation completed. Five of eleven `AlphaProbeStatus` cells empirically observed: FRACTIONAL_BRANCH, NEGATIVE_SINGULARITY, ZERO_BOUNDARY, INSUFFICIENT_DATA, plus REGULAR_INTEGER (caller-gated via `declared_alpha_band`). Rational radical family n=2..8 characterised at ~10⁻¹¹ floor; n=6 outlier (3.66σ from zero) resolved as libm `pow(x, 1/6)` composition signature with substrate-to-α amplification factor ≈10⁶ through the V4 chain. Negative-α regime via `singular_alpha_jet_bundle` characterised, empirically cleaner than positive-α radicals (10⁻¹³ floor) — mechanism: large-binade BACL gives bit-exact cancellation when |g(h)| → ∞. REGULAR_INTEGER cell documented as caller-gated (calculus refuses to round to integer without explicit tolerance). Findings: [Reports/substrate_invariant_search/2026_05_26_alpha_recovery_exploratory_findings.md](Reports/substrate_invariant_search/2026_05_26_alpha_recovery_exploratory_findings.md). All research-grade exploratory; no audit stamps. Prior context: 2026-05-25 authority rewrite initiated; original `substrate_invariant_search_2026_05_23.md` retired; Phases A-I recontextualised as constrained-instrument behavior, not citable as substrate-physics findings. Cross-fixture log-log slope agreement at branch (Schw 0.9962, PA 1.0000, |Δ|=0.0038 at N=5) recontextualised as motivating evidence for the rewrite. Campaign goal — substrate-derived K_G observable — remains research-grade open. |
| **Next concrete step** | Draft new campaign authority `substrate_invariant_search_2026_05_26.md` opening at §1 with the proper toolkit as required reading + foundational tools: BACL theorem as prediction engine, α as per-probe local observable, log-log slope at branch as derived observable, `typed_finite_difference` and `typed_log_log_slope` primitives, `transfer_function_exponent_family_v4.tex`. Pre-register Phase A under revised authority (extended candidate catalogue including derivative-class observables). 2026-05-25 slope-field finding placed in new authority's motivation section as the surprise that triggered the rewrite. 2026-05-26 α-recovery characterisation provides instrument-side baselines (status-cell coverage, routing-composition signature mechanism, REGULAR_INTEGER caller-gating, window-averaged α reporting) referenced when designing phases. |
| **Blockers** | Task 1 (audit framework extension to transfer observables — see `Docs/session_handoff_2026_05_25_audit_framework_priority.md`) blocks audit-stamped results from any new phase using `typed_log_log_slope` or `typed_finite_difference`. New phases can run research-grade pending Task 1 closure. Substrate-derivation of K_G remains research-grade open (Phase E Path A failed under constrained toolkit; Path B via BACL+α+slope not yet attempted). |
| **Anti-restart note** | **DO NOT** start a new campaign named "substrate observable catalogue," "substrate invariant inventory," "what survives M-subtraction," or "geometry-first substrate readback." Those are this campaign. Use this name. |
| **Source** | [Reports/substrate_invariant_search/](Reports/substrate_invariant_search/) |

### alpha-minus-one-exhaustion

| Field | Value |
|---|---|
| **Canonical name** | `alpha-minus-one-exhaustion` |
| **Aliases / merged from** | none |
| **Purpose (frozen)** | Establish, within the pre-registered phase structure, whether (α−1) is a property of the underlying geometry or an artifact of the measurement apparatus. |
| **Scope (frozen)** | Strictly bounded; exhausts (α−1) only, not the broader coupling-invariant program. See [alpha_minus_one_exhaustion_campaign.md](alpha_minus_one_exhaustion_campaign.md). |
| **Status** | Active, behind on pre-registered phases |
| **Current phase status** | Phase 0: ~60% piecemeal, no signed artifact. Phase 1: 1/6 mechanisms (cancellation) complete. Phase 2: ~90% (Task 017c). Phase 3A: ~40% (different α values than pre-registered). Phase 3B: 0% (was blocked → now unblocked pending v11 control-silence fix). Phase 4: ~5%. Phase 5: 0%. |
| **Last touched** | Phase 3B preregistry frozen 2026-05-17; execution not yet run. |
| **Last result** | Hardened dual-arm probe V1 (2026-05-18) removed the structural ceiling blocking Phase 3B. |
| **Next concrete step** | (a) Fix v11 control-silence logic (16 resolved records carry `legacy_v11_outcome = active_handoff_disqualified_control`). (b) Assemble the Phase 0 signed artifact from existing audit work. (c) Execute Phase 3B as pre-registered (six fixture classes, `wrong_clean_emit_count` tracked). |
| **Blockers** | v11 control-silence fix for Phase 3B execution. Phase 1 mechanisms 2–6 (mixed-binade, mixed-precision, division-near-zero, iteration-drift, subnormal) need pre-registration before running. |
| **Anti-restart note** | **DO NOT** start "negative-space mapping," "non-family fixture sweep," or "classifier integrity test" as a new campaign. That is Phase 3B of this campaign. |
| **Source** | [alpha_minus_one_exhaustion_campaign.md](alpha_minus_one_exhaustion_campaign.md), [Reports/phase3B_negative_space/](Reports/phase3B_negative_space/) |

### hardened-dual-arm-probe

| Field | Value |
|---|---|
| **Canonical name** | `hardened-dual-arm-probe` |
| **Aliases / merged from** | `foldreadback-probe0` (precursor: v10, v11), `dual-arm-behavior-verification`, `dual-arm-probe-offset-comb` |
| **Purpose (frozen)** | Operationalise the six-condition dual-arm discrimination rule with construction-time gates and run-time per-record `hardened_status`. Validate that ARM-N reads genuinely new data (real float64 path/operand separation), not numerically-collapsed restatement. |
| **Scope (frozen)** | Eval-layer probe; no substrate promotion. F2/F4 SR fixture as proving ground; cross-fixture extension deferred. |
| **Status** | Active; V1 complete and operative |
| **Last touched** | 2026-05-18 V1 closeout |
| **Last result** | 15/15 tests pass; on F2/F4 SR fixture: 16 `gap_resolved` records, 17 `armN_zero_path_separation`, 8 inactive/outside. First V4 dataset satisfying full operational discipline. |
| **Next concrete step** | (a) Fix v11 control-silence logic so the 16 `gap_resolved` records can advance (currently `advanceable=False` in V4 validity stamp). (b) Cross-fixture extension to Schwarzschild, pure_algebraic, cbrt. |
| **Blockers** | None for V1. v11 control-silence fix is the immediate operational item. |
| **Anti-restart note** | **DO NOT** start a new "dual-arm probe redesign" or "fold-readback v12" without checking the V1 closeout. The hardened V1 *is* the production probe. |
| **Source** | [Reports/hardened_dual_arm_probe/](Reports/hardened_dual_arm_probe/), [Architecture/DUAL_ARM_PROBE_PRINCIPLES.md](Architecture/DUAL_ARM_PROBE_PRINCIPLES.md), [Architecture/V4_dual_probe_design_and_reference_hygiene.md](Architecture/V4_dual_probe_design_and_reference_hygiene.md) |

### layer-3-promotion

| Field | Value |
|---|---|
| **Canonical name** | `layer-3-promotion` |
| **Aliases / merged from** | "refinery MVP," "decision-law MVP," "solver MVP" (these are L3 sub-components, not separate campaigns) |
| **Purpose (frozen)** | Move Layer 3 (refinery / decision-law / solver) from partial/non-authoritative to substrate-authoritative under explicit promotion gates. |
| **Scope (frozen)** | All L3 modules. Refinery MVP (Task 030) and Sterbenz audit (Task 031) are eval-layer instances feeding this. |
| **Status** | Active; deferred until gates close |
| **Promotion gates** | Gate 1 (chain-property cross-fixture support): **closed ✓** (Tasks 028, 029c). Gate 2 (joint-state must reveal a *derivable* law): **open** — currently descriptive only. Gate 3 (negative-space sweep): **open** — depends on Phase 3B execution. |
| **Last touched** | Refinery MVP Task 030 (2026-05-14); Sterbenz audit Task 031 (2026-05-14); Cross-fixture refinery audit (2026-05-17). |
| **Last result** | Sub-lattice alignment identified as a separate optimization criterion from operation-level exactness (Task 031). Universal across 4 fixtures × 2 radical degrees ([task032_cross_fixture_refinery_audit/](Reports/task032_cross_fixture_refinery_audit/)). |
| **Next concrete step** | Multi-fixture refinery audit: repeat Task 031's six-candidate Pareto audit on Schwarzschild, SR, and cbrt to confirm whether sub-lattice alignment generalises. |
| **Blockers** | Gate 2 requires a derivable joint-state law (currently descriptive only). substrate-invariant-search frontier is the primary candidate path to Gate 2. Gate 3 requires Phase 3B execution from alpha-minus-one-exhaustion. |
| **Anti-restart note** | **DO NOT** propose a new "L3 substrate work," "refinery rebuild," "decision-law architecture," or "solver promotion" as fresh investigation. These are all this campaign. The MVPs (Tasks 030, 031) are eval-layer instances *feeding* this; they are not separate L3 efforts. |
| **Source** | [Architecture/LAYER_MANIFEST.md](Architecture/LAYER_MANIFEST.md), [Reports/task030_refinery_mvp/](Reports/task030_refinery_mvp/), [Reports/task031_sterbenz_audit/](Reports/task031_sterbenz_audit/) |

### vera-unification

| Field | Value |
|---|---|
| **Canonical name** | `vera-unification` |
| **Aliases / merged from** | none |
| **Purpose (frozen)** | Absorb Vera campaign observations into V4 via strip-and-replicate protocol (strip Vera vocabulary; replicate substantive observations natively in V4; cite Vera as independent observation source). |
| **Scope (frozen)** | Vera observations only. No Vera vocabulary, ontology, or test designs admitted into V4 substrate. |
| **Status** | Active; most replications in design status |
| **Last touched** | 2026-05-25 |
| **Last result** | Comprehensive test ledger added: [vera_v4_test_ledger_2026_05_25.md](../../Docs/vera_v4_test_ledger_2026_05_25.md). 16 dossier-level F-entries + ~30 granular sub-tests including form-coverage extension (F2/F3/F4 vs Vera's F1-only coverage). Vera campaign archived to `/home/william_lloydlt/projects/_archive/Vera_2026_05/` after extraction. |
| **Next concrete step** | Execute Track A pre-Task-1 sub-tests per test ledger §7: F6.x (cross-task honest-refusal audit), F15.x/F16.x (V4 hardened V1 cross-reference), F9.1 (Sterbenz sub-battery audit), F8.x (N-invariance per primitive), F13.x (AlphaProbe discrimination), F11.x (sweep-coordinate sensitivity on SR). Track B sub-tests blocked pending Task 1 (audit framework extension). |
| **Blockers** | Track B sub-tests (F1.x wrong-clean-emit on non-AlphaProbe; F2.x/F4.x/F11.x/F14.x verdicts) blocked by Task 1 (audit framework extension to transfer observables). Track A unblocked. |
| **Anti-restart note** | **DO NOT** start a "cross-validation campaign" or "independent corroboration program" without checking this. Vera *is* the cross-validation campaign. **DO NOT** import Vera vocabulary into V4 substrate under any circumstances (this is an axiomatic rule — see Architecture/VERA_REFERENCE_LEDGER.md). |
| **Source** | [Architecture/VERA_REFERENCE_LEDGER.md](Architecture/VERA_REFERENCE_LEDGER.md), [vera_v4_unification_dossier.md](../../Docs/vera_v4_unification_dossier.md), [vera_v4_test_ledger_2026_05_25.md](../../Docs/vera_v4_test_ledger_2026_05_25.md). Vera campaign archive: `/home/william_lloydlt/projects/_archive/Vera_2026_05/` |

### paper-hardening

| Field | Value |
|---|---|
| **Canonical name** | `paper-hardening` |
| **Aliases / merged from** | none |
| **Purpose (frozen)** | Maintain [transfer_function_exponent_family_v4.tex](transfer_function_exponent_family_v4.tex) as the authoritative paper draft of the transfer-function exponent law, with all claims tracing back to substrate derivations or observed phenomena with provenance lineage. |
| **Scope (frozen)** | The paper draft and its supporting evidence base. Axiom 11 governs: no named-mathematical content as substrate. |
| **Status** | Active; revised May 23 to include Phase H substrate signature evidence |
| **Last touched** | 2026-05-23 (Phase H integration); 2026-05-25 (cross-fixture slope-space closure adds to evidence base). |
| **Last result** | Cross-fixture slope-space agreement at branch (|Δ|=0.0038 at N=5) independently validates the transfer-function-exponent-family law through substrate signature data, in addition to the typed-primitive validation already documented. |
| **Next concrete step** | Integrate cross-fixture slope-space closure result into paper §6 or §9. Final hardening pass: verify every claim traces to substrate derivation or observed phenomenon. |
| **Blockers** | None. Three open sub-claims of Theorem 3 (paper §10) are documented as open, not blocking. |
| **Anti-restart note** | **DO NOT** start a new paper draft or rewrite. The .tex file in `Build_Docs/` is the authoritative draft. Revisions go to that file. |
| **Source** | [transfer_function_exponent_family_v4.tex](transfer_function_exponent_family_v4.tex), [Docs/session_handoff_paper_hardening.md](../../Docs/session_handoff_paper_hardening.md) |

---

## Recently closed campaigns

Citing here so a fresh session does not propose restarting them. Each entry links to the report directory or summary.

| Campaign | Status | Source |
|---|---|---|
| L0/L1/L1.5/L2 substrate buildout (Tasks 000–019) | Closed; foundational | [Reports/task000](Reports/task000/) through [task019_summary.md](Reports/task019_summary.md) |
| Multi-precision instrument validation | Closed; R²=1.0 regular region | [task017c_summary.md](Reports/task017c_summary.md) |
| Four-form battery cross-fixture invariance (Tasks 024b–029c) | Closed; five invariants confirmed | [task029c_summary.md](Reports/task029c_summary.md) |
| Refinery MVP + Sterbenz audit (Tasks 030–031) | Closed; sub-lattice alignment discovered | [task031_sterbenz_audit_summary.md](Reports/task031_sterbenz_audit_summary.md) |
| Lattice-grain block (Tasks 032–034) | Closed; H2-refined + H3-converges | [task034_schwarzschild_quartic_transformed_n4_summary.md](Reports/task034_schwarzschild_quartic_transformed_n4_summary.md) |
| BACL invariant + multi-format + subnormal audits | Closed; BACL proven unified | [Reports/bacl_invariant_audit/](Reports/bacl_invariant_audit/) |
| Conjecture C proof | Closed; proven for sqrt normal range | [Reports/conjecture_c_proof_audit/](Reports/conjecture_c_proof_audit/) |
| c2 lattice theorem + scope gate | Closed; proven conditional on C | [Reports/c2_lattice_substrate_derivation/](Reports/c2_lattice_substrate_derivation/) |
| Lifted singularity V4 audit | Closed; structural + empirical invariants confirmed | [Reports/lifted_singularity_v4_audit/](Reports/lifted_singularity_v4_audit/) |
| Observability rule F4 audit | Closed; rule correctly tuned, do not extend | [Reports/observability_rule_audit_F4/](Reports/observability_rule_audit_F4/) |
| Blowup exponent V4 audit | Closed at audit depth; σ₁=1.000 universal | [Reports/blowup_exponent_v4_audit/](Reports/blowup_exponent_v4_audit/) |
| Substrate fingerprint atlas (Phase α + β) | Closed; partial absorption into substrate-invariant-search | [Reports/substrate_fingerprint_atlas_phase_beta/](Reports/substrate_fingerprint_atlas_phase_beta/) |
| Fold-readback probe v10 + v11 | Closed; superseded by hardened-dual-arm-probe V1 | [Reports/foldreadback_probe0_v11_genuine_separation/](Reports/foldreadback_probe0_v11_genuine_separation/) |
| MCG gate-3 killswitch | Closed (HALT terminal); reformed as substrate-invariant-search | [Reports/mcg_gate_3_killswitch/](Reports/mcg_gate_3_killswitch/) |
| May 16 phenomenology cluster (15 probes) | Closed; mostly negative results, fixture-specific findings retired | (15 directories dated 2026-05-16) |

---

## Open questions — current status

These map back to [where_i_got_stuck.md](where_i_got_stuck.md). Read this section before proposing methodology that targets any of Q1–Q6.

| Question | Status | Where it stands |
|---|---|---|
| Q1: What is casting the patterns? | Partially answered, no unified statement | Three partial answers exist: constraint surface geometry via canonical K_G (eval-layer); Sterbenz boundary mechanism (one b_k component); arithmetic-path conditioning amplitude (Theorem 3). G empirically absent in 1D scope. |
| Q2: Why does the route matter? | Answered at multiple levels | Route-bank offset guard (exact predictor); precision-scaling separation (per-path b_k); sub-lattice alignment (Task 031); four-form cross-fixture invariance. |
| Q3: Why doubling ladder? | Answered | BACL theorem (integer-ulp lattice; binade-to-binade ulp doubling). Proven from IEEE 754. |
| Q4: What is the boundary doing? | Answered | Transfer law f^(α−1) controls asymptotic amplitude. Sterbenz boundary controls path-conditioning. |
| Q5: Real vs measurement? | Solved in regular region; **worse near boundary** | Theorem 3 + Task 017c R²=1.0 in regular region. Paper §6 table shows b_k is *larger* in Sterbenz region than in regular region. Q5 in the boundary regime remains open. |
| Q6: Tooling wall | Addressed, not solved | Hardened dual-arm probe V1 discriminates whether ARM-N reads genuinely new data. Does not extend the observable region below the noise floor. No fundamentally finer substrate-compliant instrument has been built. |

### Original observations Obs 1–7

| Observation | Status | Operationalisation |
|---|---|---|
| Obs 1: Two forms behave differently | Closed | F1/F2/F3/F4 four-form battery, cross-fixture Theorem 4 |
| Obs 2: Fractal | **Silently dropped — needs explicit retirement or genuine characterisation** | No V4 report directly characterises self-similarity. Open question. |
| Obs 3: Doubling ladder | Closed | BACL |
| Obs 4: Silent form is silent because of path | Closed | F3 identity silence across all fixtures and precisions |
| Obs 5: More routes, more fingerprints | Closed | Route-bank offset guard; sub-lattice alignment; four-form battery |
| Obs 6: Amplitude varies with boundary | Closed | Transfer law + Sterbenz boundary directional bias |
| Obs 7: Lawful precision scaling | Closed | Theorem 3 + Task 017c (R²=1.0) |

---

## Aliases / known restart traps

A fresh session that proposes any of the names in the left column should instead use the canonical campaign in the right column.

| Restart-trap name | Use this canonical campaign instead |
|---|---|
| "MCG campaign," "MCG discovery," "MCG geometry-first," "G/C/M decomposition campaign," "M-subtraction sweep" | `substrate-invariant-search` |
| "Substrate fingerprint atlas continuation," "barcode hypothesis test" | `substrate-invariant-search` (Phase α+β already absorbed) |
| "Substrate observable catalogue," "irreducible basis search," "candidate invariant inventory" | `substrate-invariant-search` |
| "Negative-space mapping," "non-family fixture sweep," "classifier integrity sweep," "wrong-clean-emit audit" | `alpha-minus-one-exhaustion` Phase 3B |
| "Stress triangulation," "apparatus stress test" | `alpha-minus-one-exhaustion` Phase 1 |
| "Instrument capability gates," "subnormal model validation," "backend inventory" | `alpha-minus-one-exhaustion` Phase 0 |
| "Refinery rebuild," "L3 substrate work," "decision-law architecture," "solver promotion," "refinery MVP v2" | `layer-3-promotion` |
| "Multi-fixture Sterbenz audit," "Sterbenz dominance generalisation" | `layer-3-promotion` (next concrete step) |
| "Fold-readback v12," "dual-arm probe redesign," "dual-arm hardening" | `hardened-dual-arm-probe` |
| "Vera cross-validation," "independent corroboration program," "Vera observation absorption" | `vera-unification` |
| "Paper rewrite," "transfer-function paper revision," "new draft" | `paper-hardening` (edit the .tex file in place) |

---

## Update protocol

Every session that touches a campaign must:

1. Update **Last touched** date.
2. Update **Last result** with one-line summary.
3. Update **Next concrete step** if the previous step is done.
4. Update **Blockers** if anything changed.
5. If the campaign closes, move its entry to **Recently closed campaigns** with a one-line outcome.
6. If a new campaign is genuinely needed (not aliasable), add it under **Active campaigns** with all frozen fields populated, justify its independence in a comment, and update **Aliases / known restart traps** if it has predictable restart-trap names.

Frozen fields (canonical name, purpose, scope, aliases) do not change without explicit renaming or merging — both of which are conscious decisions, not silent rewrites.

The file is short by design. Resist the urge to add narrative; cite the source instead.
