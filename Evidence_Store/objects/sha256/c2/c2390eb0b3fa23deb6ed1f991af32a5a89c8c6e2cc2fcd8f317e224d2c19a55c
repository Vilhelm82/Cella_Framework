# CAMPAIGN — Exact Jet Primitive (typed second-order AD)

**Status:** READY v1, 2026-06-10. Pre-reads gate to be completed by the executing session. Authored in claude.ai strategy session following Shape of the Quiet completion (HR130).

**Scoreboard rows served:** `Build_Docs/PROBE_READINESS.md` A6 (deep-approach depth parity), A4 (indirect — removes FD route noise for future blowup work). Driver: HR130 / `results/shape_of_the_quiet/` — I3's FD-jet extractor floored at δ = 10⁻⁴ (the canonical ε^(1/4) second-difference wall for float64), producing a −12 decade depth deficit vs direct evaluation, while correctly self-flagging every bad rung (`fd_unresolved` / `format_precision_pinned`).

**One-line thesis:** the Quiet campaign's depth negative is attributable to the extraction route, not the substrate theory. A typed exact-jet primitive (value + gradient + Hessian in one pass, hyperdual/second-order forward AD) removes self-inflicted differencing noise. Pre-registered prediction below.

**Lineage note (clean-room rules apply):** the mathematics is the project's oldest asset — OG `HyperDual` (lloyd_core.py, March 2026), V3 `TorchFuncExactJet`. Neither may be imported. The primitive is re-derived and implemented V4-native under the typed substrate; OG/V3 serve as offline oracle and regression reference only (V3 via lv3_* MCP where expressible).

---

## Mandatory Pre-reads & Closed-results Check (executing session FIRST)

Completed by the executing session 2026-06-10 (branch `campaign/exact-jet-primitive`, based on Quiet HEAD `24690f6` — main does NOT contain the Quiet artefacts the re-run gate needs):
- [x] `Build_Docs/Architecture/PROJECT_INDEX.md` read.
- [x] `HISTORICAL_RECORD.md` — HR130 present as written (uncommitted, awaiting Will; content matches this brief's baseline verbatim: FD floor δ=10⁻⁴, −12 decades, zero unflagged confidently-wrong, manifest pin `9a1d7ec6…`). HR129 confirmed (G2 ≡ S2 PROVEN analytic; κ from (S0,S1,S2) multivariate, FD reconstruction ≤4.7e-4). No HR131 exists. **No row closes a V4-native exact-jet/AD primitive** — rows checked: HR126–129 (transcendental set, Phase A), HR130; the only jet machinery on record is the FD route this campaign supersedes on the reading path.
- [x] `LIVE_CAMPAIGNS_LEDGER.md` — **known-stale citation:** the `shape-of-the-quiet` entry still shows the Phase-1 checkpoint state (ledger update is Will-reserved, listed as outstanding in WORKING_SET, which marks the campaign COMPLETE/HR130). No active campaign owns jet extraction: checked `substrate-invariant-search` (Phase A CLOSED; G2 carried as a tool — this campaign builds the extractor for it), `substrate-construction-transplant-arc` (GAP list has no jet/AD item), `certified-precision-spine` (refine-kernel transcendentals — a *consumer-side* parent here, not an owner), restart-trap alias table (no jet/AD trap).
- [x] `V4_GLOSSARY.md` — terms checked: G2/substrate jet (S0,S1,S2 — HR129 entry), `format_precision_pinned` (4-channel rule; HR130 measured it firing ~10 decades early at float64 depth — gap filed), BACL grain (max_ulp/2). "FD metrology" has no standalone entry (lives in the HR129/G2 entry + receipt). **Name-collision flag:** glossary `JetBundle` (`scalar_alpha_jet_bundle`/`singular_alpha_jet_bundle`) are α-recovery observers, NOT derivative jets — `exact_jet` naming keeps the spaces distinct; a §13 confusion-pair entry should be added at session end.
- [x] `TASKS_TO_REVISIT.md` — no fence on AD/jet work. R9's fence covers the rounding-residual/conditioning *discovery channel*; this campaign replaces the FD *reading route* and does not reopen it. R1 CLOSED (HR129).
- [x] `LAYER_MANIFEST.md` + `SUBSTRATE_CONSTRUCTION.md` — **the brief's expected placement ("primitives, atop core typed scalars") is not buildable as stated:** (i) core provides NO typed scalar arithmetic (no typed_add/sub/mul/div anywhere in the tree — verified by grep); (ii) primitives (L1) has parents = core only and the substrate purity gate forbids transcendental `math.*` there, while the typed transcendentals (typed_sin/cos/exp/log, refine kernel) live in observers (L1.5) — a primitives-layer exact_jet has no legal sin/cos/exp value lane. Per this brief's own DP4 (entry at EVAL-LAYER; substrate promotion out of scope) the layer-correct home THIS campaign is `src/lloyd_v4/evals/exact_jet.py`; the promotion-time home is observers (L1.5, may consume sibling typed transcendentals), NOT primitives. See Primitive-Sufficiency Gate findings filed at Phase 0 (micro-task list presented to Will).

**Closed-results verdict:** ☒ extension of HR130 + HR129 (Phase A jet work: G2 ≡ S2, κ from S0/S1/S2). Genuinely new: a typed, provenance-carrying second-order forward-AD primitive. The Phase A fd-metrology module is the thing being *superseded on the reading path*, not re-derived.

## Repository

`/home/wlloyd/Lloyd_Engine_V4` (canonical; `/mnt/fast/Lloyd_Engine_V4` is stale — never read). Branch: `campaign/exact-jet-primitive`. All standing clean-room and typed-pipeline rules inherited from the Quiet brief.

## Current Verified Baseline

- HR130: Quiet campaign complete; 302 records; I3 FD floor measured at δ=10⁻⁴; zero unflagged confidently-wrong rungs for I3.
- HR129: G2 ≡ S2 PROVEN analytic; κ recoverable from the jet (S0, S1, S2).
- Quiet manifest (pin 9a1d7ec6…) and fixtures remain frozen and reusable for the re-run stage.
- Executing session re-verifies against HISTORICAL_RECORD before trusting.

## Task Goal

Implement and promote a V4-native typed exact-jet primitive — one evaluation pass returning (F, ∇F, H) with full TypedResult composition (validity / conditioning / provenance / statuses propagated through every dual operation) — then re-run the Quiet F1a rung set with I3 wired to the exact jet, under the pre-registered prediction below.

## Pre-registered prediction (falsifiable, frozen before implementation)

**P1:** with the exact-jet route, I3 reads F1a κ(δ) within 64 ulp-relative of I1's direct evaluation at every rung δ = 10⁰ … 10⁻¹⁵.
**P2:** I3 retains its attribution property: zero unflagged confidently-wrong rungs (the flags adapt — `fd_unresolved` must no longer fire; any new floor must be flagged by a route-appropriate channel).
**P3:** the typed validity of each jet component is non-trivial (not vacuously valid): at least the conditioning channel must respond measurably across the ladder.
Failure of P1 is filed as a formula-conditioning gap, not patched in-campaign. Failure of P2 is a defect (stop, fix, re-run). Failure of P3 is a design gap (stop, file).

## Design Principles

1. **Provenance through the algebra.** Every dual-arithmetic operation composes TypedResult metadata. The genuinely new design problem of this campaign is the composition law: how validity/conditioning/provenance flow through ⊕, ⊗, ÷, pow, and the unary library (sin, cos, exp, log, sqrt, abs). Decide it once, record it in RESULT_TYPES.md as an amendment proposal, enforce it in tests.
2. **No silent fallbacks.** Degenerate cases (division by dual with zero real part, sqrt at 0, abs at 0) return typed refusals or flagged values — never exceptions swallowed, never NaN passed unflagged. The OG implementation's try/except patterns are the documented anti-pattern.
3. **Oracle, not import.** Validation against lv3 exact-jet outputs (where expressible) and against analytic closed forms. Zero V3/OG source enters the tree.
4. **Gate discipline.** The primitive enters at EVAL-LAYER; promotion to PROVEN requires the full test battery + the F1a re-run receipts. Substrate-tier promotion is out of scope for this campaign.

## Primitive-Sufficiency Gate

Required from parent layers: typed scalar arithmetic with provenance (core), the conditioning channel (metrology), refusal/status calculus (statuses). If any unary function lacks a typed parent (e.g. typed exp), list the parent-extension micro-task and STOP for approval before building it here.

## Required Deliverables

- ~~`src/lloyd_v4/primitives/exact_jet.py` (or layer-correct location per LAYER_MANIFEST)~~ **[CORRECTION 2026-06-10, Will's audit ruling 3 — authoring error, not drift: the layer-correct path is `src/lloyd_v4/evals/exact_jet.py` now (DP4 eval-layer entry; purity gate and L1 parent edges make primitives structurally unbuildable for this primitive), observers (L1.5) at promotion.]** + composition-law amendment proposal for RESULT_TYPES.md (proposal document in the campaign folder; the normative file is touched only on Will's approval of the law).
- F1a re-run records under `results/exact_jet_f1a_rerun/` (same fixtures, same arbiter policy, prediction P1–P3 graded mechanically).
- Updated `resolution_vs_proximity` figure overlaying the new I3 curve on the HR130 curves.
- HISTORICAL_RECORD entry draft (HR131) — left uncommitted for Will's review.
- PROBE_READINESS A6 row update draft (depth-parity outcome, whatever it is).

## Required Tests

- `test_jet_identities.py` — dual arithmetic vs analytic derivatives on a closed-form battery (polynomial, rational, transcendental, composite), to tight ulp tolerances.
- `test_jet_typed_composition.py` — provenance/validity/conditioning propagate per the recorded composition law; degenerate inputs produce typed refusals (Design Principle 2).
- `test_jet_oracle_crosscheck.py` — agreement with lv3 jets on expressible fixtures within pre-registered tolerance.
- `test_jet_determinism.py` — byte-identical jets on re-run.
- `test_quiet_rerun_gate.py` — re-run refuses unless the original manifest pin verifies (no fixture drift).

## Required Commands

Derive from CLAUDE.md conventions; record red slice / green slice / full suite / source audit in the campaign manifest.

## Non-Goals

- No eigensolve primitive (the F1b second-difference path already suffices; eigensolve is a future gap-driven task if a fixture forces it).
- No separator estimator work (see `CAMPAIGN_SEPARATING_ESTIMATOR_DRAFT.md` — explicitly downstream).
- No F3 Kerr, no wave-two fixtures, no substrate-tier promotion.

## Completion Report

`results/exact_jet_f1a_rerun/CAMPAIGN_REPORT.md` — composition law as built, P1–P3 verdicts with receipts, the overlay figure, gaps filed, plain-language answer: *did removing the FD route restore depth parity while keeping honesty?*

## Acceptance Criteria

1. Pre-reads ticked with citations.
2. Composition law recorded before implementation begins; tests enforce it.
3. P1–P3 graded mechanically from records; verdicts in the report verbatim regardless of direction.
4. All five test files green; full suite exit 0; source audit clean (zero V3/OG imports).
5. F1a re-run byte-stable on re-execution.
6. HR131 draft + A6 row draft produced, left for Will's review.
