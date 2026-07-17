# CAMPAIGN — Shape of the Quiet

**Status:** DRAFT v1, 2026-06-10. (a) Mandatory Pre-reads **COMPLETE** (executing session, 2026-06-10 — see below, incl. 3 reported conflicts); (b) Will's fixture audit **PENDING**. **BLOCKER:** the `lv3_*` MCP oracle is not configured in the executing environment (no `lloyd_v3` server in any reachable MCP config) — instrument I2 and `test_quiet_oracle_smoke.py` cannot run until it is registered. Authored in claude.ai strategy session; execution belongs to Claude Code / Cowork.

**Scoreboard rows served:** `Build_Docs/PROBE_READINESS.md` A4 (primary), A6 deep-approach (primary), A9 (stretch). This campaign exists to fill those rows — see the Milestone section of the scoreboard.

**One-line thesis:** at singular approach, the V4 typed probe keeps reading structure in the proximity regime where naive float64 and V3 are buried in substrate noise — and can say, per digit and per rung, which parts of the reading are phenomenon and which are substrate.

---

## Mandatory Pre-reads & Closed-results Check (executing session does this FIRST)

Completed at authoring time (2026-06-10):
- [x] `Build_Docs/PROBE_READINESS.md` — rows A4/A6/A9 verified open (ambiguous / partially_tested / not_attempted).
- [x] `Build_Docs/Agent_tasks/TASK_TEMPLATE.md` — this brief conforms.

Completed by the executing session 2026-06-10 (Claude Code, branch `campaign/shape-of-the-quiet`):
- [x] `Build_Docs/Architecture/PROJECT_INDEX.md` read (§3 closed-results guard, §4 open frontier).
- [x] `Build_Docs/Architecture/HISTORICAL_RECORD.md` — no row closes deep-approach attribution for Schwarzschild / blowup-exponent / Kerr. Rows checked: HR17 (task024b Schwarzschild four-form — PROVEN, shallow region only, V3 overlay 1-ulp); HR22 (Kerr-leap RETIRED as physics-overreach — a framing guardrail, not a result closure; F3 must respect CLAUDE.md §9); HR56 (lifted-singularity audit — Kerr retrograde a=0.9 float32 honest refusal, no deep ladder); HR77 (blowup σ1=1.000 PARTIAL — σ4/σ5 not reached; V3 K_G deliberately not reproduced); HR91 (v3_calibration_fixtures PARTIAL — Schwarzschild K_G healthy r∈[2.1,100]; deep approach unexplored; −2 eigenvalue untested); HR129 (substrate-invariant-search Phase A closeout — `G2 ≡ S2` PROVEN analytic, the V4-native curvature extractor; κ its lossy projection). Deep-approach attribution is OPEN on all three fixture families.
- [x] `Build_Docs/Architecture/LIVE_CAMPAIGNS_LEDGER.md` — campaigns checked: `substrate-invariant-search` (Phase A CLOSED 2026-06-07; this campaign uses `G2` as a delivered tool and does NOT reopen the R9-fenced rounding-residual channel); `blowup_exponent_v4_audit` (Recently-closed table — closed at audit depth; F2 extends, does not re-derive); `v3_calibration_fixtures` (HR91 PARTIAL — F1 extends its constraint surface past r=2.1); `certified-precision-spine` (typed transcendental set complete 2026-06-07 — I3-side instrument maturity); restart-trap alias table — "Shape of the Quiet" matches no trap. **MCG Phase 2h status: LANDED** — see Dependency note resolution below.
- [x] `Build_Docs/Architecture/V4_GLOSSARY.md` — terms checked: attribution categories (§"phenomenon/substrate/ambiguous/format_precision_pinned" — NOTE conflict #2 below: the instrument's 4 channels ≠ the scoreboard's 4 categories), BACL, BACL grain vs lattice grain (§13 confusion pair), E primitive (fails T2 format-invariance at near-singular coordinates — directly load-bearing for deep rungs), K_G (eval-layer only, Goldman 2005 import), G2 (PROVEN analytic), blowup exponent σ1, `b_k` letter-collision pair.
- [x] `Build_Docs/Architecture/TASKS_TO_REVISIT.md` — no silent re-opening. Checked: R1 (CLOSED — successor authority written; K_G resolves to G2); R9 (fenced — this campaign does not reopen the additive-residual G channel); R7 (blowup σ1 + v3_calibration_fixtures are `asserted_only`, no regression tests — this campaign's four required tests partially remediate that gap); R3 (curvature pivot — G2/HR129 is the de-facto resolution; no dangling re-invocation here).

**Dependency-note resolution (Phase 2h), 2026-06-10:** Phase 2h **has landed** — artefacts: `Build_Docs/Reports/mcg_geometry_first/phase_2h_v3_bridge.md`, `phase_2h_v3_bridge.json` (byte-stable), `phase_2h_v3_oracle_crosscheck.json` (non-primary), generator `src/lloyd_v4/evals/mcg_geometry_first_v3_bridge.py`, `tests/test_mcg_geometry_first_v3_bridge.py` (10 tests). HOWEVER: what landed is the *descriptive mapping* (K_G / condition_number / hessian_eigenvalue_diagnostics = `diagnostic_neighbour` of E; near_umbilic / null_direction = `not_applicable_in_1d`) — its own MD_Q2 explicitly excludes the V4-native K_G vocabulary F1's −2-eigenvalue attribution needs. That vocabulary now exists via a different route: **HR129's `G2 = (2/ln2)(y''/y−(y'/y)²) ≡ S2` jet vocabulary (PROVEN analytic), with κ recoverable multivariately from the full jet `(S0,S1,S2)`**. Proposed scoping (pending Will's confirmation at manifest audit): F1's attribution vocabulary builds on the existing G2/(S0,S1,S2) substrate jet — no new primitive, no minimal-slice bridge build — satisfying Design Principle 4.

**Closed-results verdict (authoring-time, executing session re-confirms):**
☒ extension of `PROBE_READINESS.md rows A4 / A6 / A9` + `blowup_exponent_v4_audit/` + `v3_calibration_fixtures/`. Genuinely new content: comparative three-instrument resolution study on a proximity ladder, with per-rung typed attribution. No prior campaign compares instrument depth at singular approach.

**Dependency note (Phase 2h):** Fixture F1's −2-eigenvalue / K_G attribution requires V4-native K_G vocabulary (the smoke-test learning: the E discriminator does not appear in V3's K_G output). If the Phase 2h bridge has not landed, Stage 2 of this campaign is the minimal slice of it: only what F1 needs, no more. Do not build the full bridge inside this campaign.

---

## Repository

- Canonical worktree: `/home/wlloyd/Lloyd_Engine_V4` (THE `/home` COPY). `/mnt/fast/Lloyd_Engine_V4` is a STALE clone — never read from it.
- Clean-room rules (inherited, unchanged): V3 participates as an ORACLE ONLY, via the `lloyd_v3` MCP tools (`lv3_diagnose`, `lv3_singularity`, `lv3_branch_classify`, `lv3_observe_full`, …). No V3 source, vocabulary, or test design is imported into the V4 substrate. V1/OG engines are historical reference only.
- All V4-side computation goes through the typed pipeline; raw-float side channels are a defect by definition.

## Current Verified Baseline (authoring-time)

- Substrate primitives mature: BACL (multi-format, zero violations), Conjecture C (proven, float64 normal), c2 lattice theorem, E primitive (1D validated).
- A5 closed: V3's machine-ε noise floor is BACL-derived across Schwarzschild / SR / Sphere / Ohm fixtures.
- A6 partial: Schwarzschild K_G(r) healthy on r ∈ [2.1, 100]; deep approach unexplored; −2 eigenvalue untested.
- A4 ambiguous: V4-native σ1 = 1.000 ± 0.000 across 15 simple zeros of ζ, J₀, Ai; V3's K_G value not yet reproducible V4-native.
- Executing session must re-verify this baseline against `HISTORICAL_RECORD.md` before trusting it.

**Baseline re-verification (executing session, 2026-06-10).** All five baseline lines CONFIRMED against `HISTORICAL_RECORD.md` / `PROBE_READINESS.md` / `V4_GLOSSARY.md` (BACL: glossary §BACL, 31k+ records zero violations; Conjecture C: proven float64 normal — and *stronger* than stated: C_subnormal n=2 closed 2026-06-05, HR121; c2 lattice: proven conditional on C; E 1D validated: Phase 2g; A5/A6/A4 statuses match scoreboard rows verbatim). Conflicts found and reported, NOT silently reconciled:
1. **Phase 2h framing is stale.** The brief (and scoreboard [v1] note) treat the V3 diagnostic bridge as possibly-pending; it landed (artefacts cited above). But the *substance* of the dependency stands: landed Phase 2h excludes V4-native K_G (its MD_Q2). The brief's "use its artefacts" branch and its "minimal F1-only slice" branch are therefore BOTH wrong as written — the post-authoring fact is HR129's G2 jet vocabulary, which supersedes the need for either. Decision required at manifest audit.
2. **Attribution-category mismatch.** The brief's Metric 4 ("I3's four-category attribution": phenomenon / substrate / contaminated / ambiguous, per scoreboard) does not match the existing instrument's four output channels (glossary: phenomenon / substrate / ambiguous / **format_precision_pinned**; no **contaminated** channel exists in any V4 instrument). The manifest must pin an explicit mapping (proposal: per-rung instrument channels are recorded raw; "contaminated" is a *campaign-level* verdict assembled from mixed per-rung attributions, never emitted per-rung).
3. **E primitive caveat, load-bearing at depth:** E fails T2 format-invariance at near-singular coordinates (glossary §E). On the deep rungs (δ → 10⁻¹⁴, |base_operand| → small) any E-based attribution channel enters exactly the regime where this caveat bites — per-fixture tolerance/validity wiring must account for it.

## Task Goal

Quantify, on a shared proximity ladder toward a singular locus, the last trustworthy rung for each of three instruments — naive float64, V3 (oracle), V4 typed probe — and produce per-rung V4 attributions (phenomenon / substrate / contaminated / ambiguous). Deliver one headline figure: trustworthy-depth vs proximity, per instrument, per fixture. Update scoreboard rows A4, A6, (A9) with the outcome — whatever the outcome is.

## Design Principles

1. **Honest by construction.** If V4 shows no depth advantage, that is a publishable-to-ourselves result and goes on the scoreboard verbatim. The campaign is not designed to flatter the probe.
2. **Arbiter, not vibes.** Ground truth per rung comes from an mpmath high-precision computation (≥ 50 dps, raised until self-consistent across +10 dps) of the same quantity, where the quantity is well-defined. "Trustworthy" is defined against the arbiter, not against expectations.
3. **Determinism.** Every run bit-identical on re-execution. Seeds, environments, and tool versions recorded in the campaign manifest.
4. **No new substrate primitives.** If a fixture exposes a missing primitive, STOP, file the gap against the scoreboard, and end the stage. Gap-driven iteration is the loop working as designed — mid-campaign primitive invention is the loop failing.

## Fixtures

- **F1 — Schwarzschild deep approach (serves A6).** Constraint surface as in `v3_calibration_fixtures/`, extended: proximity parameter δ = r − 2M on a log ladder δ = 10⁰ … 10⁻¹⁴ (extend toward grain while the arbiter remains self-consistent). Two sub-passes: (a) K_G(δ) reading per instrument; (b) the −2 eigenvalue claim, M-variable fixture, at each rung it remains computable.
- **F2 — Blowup-exponent family at branch points (serves A4).** The 15 simple zeros of ζ, J₀, Ai from `blowup_exponent_v4_audit/`. Ladder: approach distance to the zero, 10⁰ … 10⁻¹⁴ scaled by local ulp. Quantity: exponent estimate (σ1) and, where Phase-2h vocabulary exists, V4-native K_G.
- **F3 (stretch) — Kerr extremal approach (serves A9).** a → M on a log ladder in (M − a). Only attempted if F1+F2 complete inside budget; requires Will to confirm the Kerr constraint-surface form.
- Will may swap or veto fixtures at audit. Fixture definitions are frozen in the campaign manifest before any sweep runs.

## Instruments

- **I1 — Naive float64.** Textbook computation of the target quantity, no safeguards. The honest baseline.
- **I2 — V3 oracle.** Same quantity via `lv3_*` MCP calls. V3's own trust/validity flags recorded.
- **I3 — V4 probe.** Typed pipeline end-to-end: value + validity + conditioning + provenance + BACL/E attribution per rung.
- **Arbiter — mpmath.** Per Design Principle 2.

## Metrics

1. **Last trustworthy rung** per instrument per fixture: deepest δ where |estimate − arbiter| ≤ tol (tol pre-registered per fixture in the manifest) AND the instrument self-reports valid. Note instruments that report *confidently wrong* values past their floor — that failure mode is a first-class result.
2. **Divergence onset**: first rung where the instrument departs the arbiter by > tol.
3. **Depth advantage**: Δdecades between I3's and I2's last trustworthy rung (headline number).
4. **Attribution table**: per rung, I3's four-category attribution with provenance.
5. **Attribution quality**: fraction of rungs where I3's attribution is consistent with the arbiter-derived classification (e.g. rungs where the arbiter shows the float64 reading is pure rounding must be attributed substrate, not phenomenon).

## Required Deliverables

- `results/shape_of_the_quiet/` — manifest, per-fixture per-rung records (JSONL), arbiter records.
- `results/shape_of_the_quiet/resolution_vs_proximity.(png|svg)` — the one figure.
- `results/shape_of_the_quiet/attribution_table.md`
- Campaign report per `CAMPAIGN_DISCIPLINE.md`, including the honest-failure section.
- `Build_Docs/PROBE_READINESS.md` rows A4 / A6 / (A9) updated with status + evidence pointers.

## Required Tests

- `test_quiet_determinism.py` — re-run of one fixture rung-set is bit-identical.
- `test_quiet_shallow_agreement.py` — at δ = 10⁰…10⁻², all three instruments agree with the arbiter within tol (sanity: the ladder is wired correctly).
- `test_quiet_oracle_smoke.py` — `lv3_*` MCP reachable and returning well-formed results for one known point.
- `test_quiet_manifest_frozen.py` — sweep refuses to run if fixture/tol manifest hash differs from the pre-registered one.

## Required Commands

Executing session derives these from the repo's existing conventions (`CLAUDE.md` command reference): red slice, green slice, full suite, source audit. Record them in the campaign manifest.

## Non-Goals

- No V3 code import; no V4 substrate changes; no new primitives (see Design Principle 4).
- No repo extraction or restructuring (see `TASK_ROOT_HYGIENE.md` — separate, bounded).
- No publication framing. Internal attribution only.
- No Bell (A7) — blocked on Will's surface specification; out of scope here.

## Completion Report

`results/shape_of_the_quiet/CAMPAIGN_REPORT.md`: baseline re-verification, manifest, per-fixture outcomes, the figure, attribution-quality number, scoreboard diffs, gaps filed, and a one-paragraph plain-language answer to: *did the probe earn its three months?*

## Acceptance Criteria

1. Pre-reads section above fully ticked with citations.
2. Fixture manifest frozen and hash-pinned before first sweep.
3. F1 and F2 complete: every rung has records from I1, I2, I3, and arbiter (or an explicit typed refusal).
4. The figure exists and is generated from the records by committed code.
5. Scoreboard rows A4 and A6 carry updated statuses with evidence pointers — whatever direction the evidence went.
6. Determinism test passes twice on different days.
7. Zero raw-float side channels in I3's path (source audit clean).
