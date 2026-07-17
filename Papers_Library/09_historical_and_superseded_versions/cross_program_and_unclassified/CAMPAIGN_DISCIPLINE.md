# V4 Campaign Discipline

Working methodology for any V4 eval-layer campaign — what disciplines apply, how to structure phases, how to audit honestly.

This document is **methodology, not substrate.** It does not extend V4 axioms or change layer manifests. It captures working practice for designing, running, and closing out eval-layer investigations so the practice doesn't drift between sessions.

**Source attribution.** Generalized from the (α−1) Exhaustion Campaign program of work (`/home/william_lloydlt/Documents/alpha_minus_one_exhaustion_campaign.md`, v1.0, compiled across Will + ChatGPT auditor + Claude). That document remains the (α−1)-specific application of the same discipline; this doc lifts the cross-cutting rules to V4-general scope.

---

## 1. Seven cross-cutting rules

These apply to every V4 campaign, regardless of subject matter. Each rule names what to do and what failure mode it guards against.

### 1.1 Pre-registration is binding

Every campaign and every sub-test registers its predictions, expected failure modes, observability rules, and status precedence **before running.** The registry is a frozen artifact; post-hoc reinterpretation is not permitted. If a result does not fit the registry, the registry was wrong and gets a new versioned entry — never a quiet rewrite.

**Failure mode this guards against:** post-hoc reframing of results to match a desired narrative; classifier integrity drift; "the test was supposed to show X" becoming "the test was supposed to show whatever it showed."

**Where pre-registration lives in V4:** `Build_Docs/Agent_tasks/` for Codex execution specs; the same pattern extends to broader campaign programs (preregistry.md per phase).

### 1.2 No substrate promotion within a campaign

Every result produced within a campaign is **eval-layer evidence.** No new status types, primitives, or axioms are promoted into V4 substrate as a consequence of an in-flight campaign. Promotion is a separate exercise with its own evidence threshold, conducted after closeout, under Axiom 11 and the substrate-derivation discipline.

**Failure mode this guards against:** the campaign accumulating eval-layer concepts that quietly become substrate, contaminating the typed-substrate derivation chain (Axiom 12).

### 1.3 Master audit metric: `wrong_clean_emit_count`

Every V4 campaign tracks the same master audit metric, decomposed four ways:
- `wrong_family_clean_emit` — apparatus confidently classified a non-family fixture as family.
- `wrong_off_family_clean_emit` — apparatus confidently classified a differently-family fixture into the wrong family member.
- `wrong_boundary_clean_emit` — apparatus issued algebraic classification on a fixture that should have been routed to boundary status.
- `wrong_refusal_failure` — apparatus refused on a fixture that should have classified cleanly.

The metric is the spine of any campaign. Detail is rich within each phase, but the question across the whole campaign reduces to: *did the apparatus confidently label the wrong kind of object?*

**V4-honest definition of "wrong":** Use V4's own declared uncertainty — `propagated_window_error` — not a naive frequentist `standard_error`. A wrong-clean-emit is one where `|observed − ground_truth| > propagated_window_error` AND the result was emitted with `validity.selectable = True` (or analogous "authoritative result" criteria). Using `standard_error` for this test ignores V4's substrate calculus and inflates the count artificially.

**Worked example:** §8.F1 of `Docs/vera_v4_unification_dossier.md` shows the audit applied to task024b — the only high-confidence emit (F4 form) appears 13.9σ off when audited naively but is *within* V4's declared `propagated_window_error` when audited honestly. **Honest audit lands a different verdict than naive audit.**

### 1.4 Surprise ledger

Every result that surprises — pleasantly or otherwise — gets logged separately from the campaign's main artifacts, with what was expected and what happened. Surprises are where the framework's edges are; they vanish from memory quickly if not captured at the moment.

**Storage:** one `surprise_ledger.md` per campaign, kept beside the campaign's main artifact dir. Append-only; revisions are noted but originals are not silently rewritten.

### 1.5 Cross-campaign reference palette

A single master table tracks every fixture across the campaign: surface description, predicted slope, predicted classification, observed slope per precision, observed status, classification stability across precisions, route metadata summary. As a campaign grows, this table becomes both pattern-spotter and inconsistency-catcher.

**V4 today:** no V4-wide master palette exists yet. When a campaign would benefit from one, build it alongside the campaign artifacts. Don't retrofit — start where needed.

### 1.6 Time-boxed phases

Each phase gets a watch, not a hard limit. Follow a result if it warrants it, but stay aware of which phase you are in. Confirmatory / load-bearing phases (typically the earliest) should consume the bulk of effort. The "unexpected" phase (where novel findings emerge) is where lost time is easiest to absorb. Constrained-exploration phases are where lost time is hardest to recover.

### 1.7 Fork discipline

If a mechanism produces signal where none was predicted, **stop expanding the current phase** and characterize that mechanism immediately. Do not fold an anomaly into ongoing tests. The anomaly is the campaign at that moment.

**Failure mode this guards against:** anomalies getting absorbed into noise, deferred indefinitely, or "explained away" instead of investigated; the campaign losing the signal it was set up to find.

---

## 2. Phase template

A V4 campaign typically has 4–6 phases. The phase shapes recur across campaigns, even when subject matter differs.

| Phase | Purpose | Closes when |
|---|---|---|
| **0 — Instrument capability gates** | Validate that the measurement instrument behaves as specified across every operational regime subsequent phases will stress. Pre-register pass/fail criteria for each gate. | Signed artifact: *"Instrument validated for backends X/Y/Z, route identity controls pass, status precedence regression passes."* Phase 1 cannot start until this exists. |
| **1 — Stress triangulation** | Determine whether the apparatus manufactures the candidate signal under stress mechanisms other than the one already tested. Each mechanism is a contrast pair on a smooth/null surface. | Each mechanism produces one of three verdicts: *geometric* (apparatus visibly stressed, classification appropriate, zero wrong-clean-emits), *apparatus* (signal where none should appear — fork triggered), *toothless* (no visible stress — inconclusive, scope-out). |
| **2 — Precision/backend robustness** | Determine whether the candidate finding is stable across precision and backend choices. | Each surviving fixture has a precision-invariance verdict (invariant / bounded drift / unstable) and any prior-result reproduction is documented. |
| **3A — Positive-space coverage** | Extend the finding to adjacent in-family cases. | Each fixture has a slope, distance-from-predicted recorded, and the extension verdict is one of: cleanly extends, breaks at boundary (fork), non-uniform (fork). |
| **3B — Negative-space mapping** | Confirm the finding does **not** appear where it geometrically shouldn't. | Each non-family fixture has a classification status; any unexpected family emission triggers a fork. *Master metric applies most strongly here — Phase 3B's clean-emit count is a direct hit on classifier integrity.* |
| **4 — Adjacent-invariant boundary mapping** | Map the local landscape around the finding. Scope-bounded; doesn't extend into general territory. | Local landscape mapped: at least one negative result confirmed, candidate neighbors identified or absent, apparatus-side artifacts catalogued. |
| **5 — Closeout synthesis** | Synthesize all prior phases into a campaign-final artifact. No new evidence. | Closeout artifact exists: master palette + surprise ledger + wrong-clean-emit summary + per-phase open questions + scoped verdict. |

Not every campaign needs all phases. Phase 0 is mandatory (no exceptions). Phase 5 is mandatory (the campaign closes formally). Intermediate phases are selected by what the campaign is testing.

---

## 3. Verdict vocabulary

V4 campaigns produce verdicts at multiple scales. The vocabulary should be consistent:

- **Per-test verdicts:** `geometric`, `apparatus`, `toothless` (from Phase 1 discipline).
- **Per-fixture verdicts (precision sweep):** `invariant`, `bounded_drift`, `unstable`.
- **Per-phase verdicts:** `closed` (all sub-tests produced one of the registered verdicts), `forked` (anomaly under characterization), `scoped_out` (gate failed; phase skipped with note).
- **Campaign closeout verdict:** scoped statement of the form *"Across stress mechanisms X/Y/Z; backends A/B/C; coverage range R; negative-space fixtures N₁..Nₖ; and adjacent invariant boundary tests T₁..Tₘ: the finding is [verdict] within the tested space. The following regimes were not tested and are noted as out-of-scope: ..."*

The closeout verdict is **scoped, not absolute.** "X is true" is forbidden; "X is true within the tested space; outside the tested space is unknown" is the correct form.

---

## 4. Audit metric in V4-honest terms

The `wrong_clean_emit_count` (rule 1.3) needs operational definitions that respect V4's substrate calculus. The following definitions apply across all V4 campaigns:

**"High-confidence emit" criteria (must all hold):**
- `refusal = None` (V4 substrate did not refuse)
- `protocol = ok` (protocol contract satisfied)
- `validity.selectable = True` (result can be selected as authoritative)
- Status string indicates stable classification (e.g., `alpha_stability_status = stable` for AlphaProbe; analogous fields for other observables)

**"Wrong" criterion:**
- `|observed − ground_truth| > propagated_window_error` (V4's honest declared uncertainty), **not** `standard_error` (the naive frequentist local-fit uncertainty)

The two uncertainty fields express different things: `standard_error` is local fit; `propagated_window_error` is the substrate's full propagated uncertainty given window heterogeneity. Auditing against the former without the latter inflates the wrong-clean-emit count artificially.

**Per-campaign metric output:** a single row per campaign in a `wrong_clean_emit_summary.json`, decomposed into the four sub-metrics from rule 1.3.

---

## 5. Worked example: the dual-arm offset/comb campaign

The recent V4 dual-arm probe work is a worked example of campaign discipline applied to a sub-investigation. Five eval-layer task reports produced a synthesis:

[`Build_Docs/Reports/dual_arm_probe_offset_comb_findings/dual_arm_probe_offset_comb_findings.md`](Reports/dual_arm_probe_offset_comb_findings/dual_arm_probe_offset_comb_findings.md)

Underlying reports (all in `Build_Docs/Reports/`):
- [`hard_cell_q_source_exhaustion_search`](Reports/hard_cell_q_source_exhaustion_search/) — found that a natural sqrt/cbrt pair covered the hard cells on the native grid.
- [`route_pair_selection_stability_audit`](Reports/route_pair_selection_stability_audit/) — found that the same pair failed under ULP perturbations; the coverage was native-grid-specific.
- [`route_bank_offset_guard_audit`](Reports/route_bank_offset_guard_audit/) — found that route-bank success was exactly predicted by the operand-offset guard (precision/recall 1.0/1.0).
- [`zero_offset_transcendental_q_source_search`](Reports/zero_offset_transcendental_q_source_search/) — found that `pow(math.e, math.log(q_direct))` closed the zero-offset cells, but as a diagnostic rounded-nextafter nudge, **not** a clean algebraic route.
- [`controlled_offset_dither_readback`](Reports/controlled_offset_dither_readback/) — found that controlled offsets improved a target-aware zero selector but not predeclared readback.

**Synthesized constraint** (eval-layer empirical, **not** substrate-promoted): *"An ARM-W gap is resolved by ARM-N only if ARM-N has non-zero path/operand separation from ARM-W AND passes its own independent instrument law. Activation alone is not evidence of resolution."* Plus 4 corollaries (separation telemetry required; zero-offset ARM-N is underpowered; target-aware selection stays banned; diagnostic routes ≠ production routes).

This is the **synthesis-as-output-of-campaign-discipline** pattern. Rules 1.2 and 1.3 apply: nothing here gets auto-promoted into V4 substrate. If a future task wants to bring dual-arm into Layer 3, the substrate-promotion gate is a separate exercise that respects these eval-layer constraints.

---

## 6. Where this lives in V4's structure

- `Build_Docs/Architecture/` — axioms, substrate design, normative architecture. **Off limits** for campaign-output without substrate-promotion review.
- `Build_Docs/Agent_tasks/` — Codex execution specs (pre-registrations live here).
- `Build_Docs/Reports/` — task summaries, campaign artifacts, per-phase closeouts.
- `Build_Docs/CAMPAIGN_DISCIPLINE.md` — *this document.*
- `Docs/` — session handoffs, paper draft, unification dossiers.
- `src/lloyd_v4/evals/` — eval-layer code that produces campaign outputs.

---

## 7. Open methodological items

- **No V4-wide master palette exists yet.** When the next campaign starts, build the palette as a campaign artifact. Don't try to retrofit one across the 78+ existing reports.
- **The `wrong_clean_emit_count` framework specified in §4 has been prototype-applied only to task024b** (one form, one fixture). Extending to other tasks needs per-task schema knowledge for the high-confidence-emit criteria and ground-truth comparison. Each new task = one schema-mapping pass.
- **The (α−1) exhaustion campaign reached Phase 5 via Vera execution** (16-phase artifact set in `/home/william_lloydlt/projects/Vera/campaign/`). V4-side absorption of findings is in progress via `Docs/vera_v4_unification_dossier.md`. **The campaign is deliberately NOT closed** — user's position is that closeout would be premature because the campaign has not actually been exhaustive on (α−1). Phase 3A rational-α coverage, Phase 3B negative-space, and Phase 4 adjacent-invariant boundary work appear to be regions where the parameter space remains under-tested. Phase 5 (closeout synthesis) is held open until exhaustion is genuinely reached.

---

*Authored 2026-05-17 as part of mining the dual-arm probe offset/comb findings and the (α−1) exhaustion campaign program for V4-usable methodology. Generalizes the (α−1)-specific discipline to V4-wide scope; original (α−1) doc remains authoritative for that campaign's specifics.*
