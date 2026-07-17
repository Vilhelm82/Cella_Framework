# Shape of the Quiet — Campaign Report

**Date:** 2026-06-10 · **Branch:** `campaign/shape-of-the-quiet` · **Manifest:** v1 FROZEN, pin `9a1d7ec6…` · **Scoreboard rows served:** A4 (primary), A6 (primary), A9 (stretch — F3 deferred, not run)

Per `CAMPAIGN_DISCIPLINE.md`. Every number below is read from the committed byte-stable JSONL records (`records/`, 302 records) through the committed analysis code; measurement vs inference is marked throughout.

---

## 1. Baseline re-verification

Done at Phase 0 (brief, pre-reads section): all five baseline lines confirmed against `HISTORICAL_RECORD.md`; three conflicts reported and ruled on by Will (Phase-2h staleness → G2 vocabulary; attribution-category mismatch → pre-registered aggregation; E-at-depth caveat → arbiter referees). The lv3 oracle was unreachable at session start (no MCP registration); registered by Will, smoke-verified v1.27.0.

## 2. Manifest & discipline

- Frozen after Will's audit (F1b interpretation confirmed with form-borne scope note; F2c sin control approved; tolerances and F2 claim regime k≥7 approved). Hash-pinned; `require_frozen_manifest()` gates the sweep and is byte-tamper-tested.
- Two pre-execution addendum amendments, both recorded with rationale BEFORE any recorded sweep: (1) r²-gate → standard-error gate for the F2 channel rule (r² is shape-inappropriate for near-flat transfers); (2) dual arbiter: I3 graded against the exact-arithmetic ideal of its own pre-registered estimator (the transfer route responds to window curvature at exactly 2× the direct slope — definitional, not substrate). All instruments' raw signed errors vs the direct quantity are also recorded per rung (ruling 3).
- Determinism [measured]: full re-run byte-identical; `test_quiet_determinism` (rungs {0,5,10,14} end-to-end, including the V3 oracle round-trip) green. **Acceptance Criterion 6 requires a second pass on a different day — pending; record it here when run.**
- Source audit [measured]: substrate purity gate green; the only raw transcendental in the sweep module is `math.sin` inside I1's evaluator (naive by definition, addendum-sanctioned). I3's path uses the pre-registered Phase A extractor + typed primitives only.

### Day-2 determinism record (AC6) — added 2026-06-12

Re-run on post-merge `main` (commit e8ce507) on a calendar day distinct from the day-1 runs recorded above: `PYTHONPATH=src python3 -m pytest tests/test_quiet_determinism.py -q` → "", exit 0. Byte-stability of the frozen Quiet artifacts holds across calendar days; the same-calendar-day objection is retired. **HR130 AC6: SATISFIED.**

## 3. Per-fixture outcomes

### F1a — Schwarzschild deep approach, κ(δ) (serves A6)

[measured] The quantity itself is benign at depth: κ(δ) **saturates at 4.0** as δ→0 (M=1), and the arbiter's 1-ulp ground classification is `phenomenon_dominated` at **every** rung — the structure is resolvable by float64 all the way to the representability edge (k=15; k=16+ collapses to r=2 exactly, recorded as domain refusals).

| instrument | last trustworthy rung | story |
|---|---|---|
| I1 naive float64 | **k=15** | reads κ at ~1e-16 relative error at every rung — the closed form has no catastrophic regime here, and κ's saturation makes it forgiving of the `1−2/r` cancellation |
| I2 V3 oracle | **k=15** | identical depth, trust=1.0 throughout |
| I3 V4 typed probe | **k=3** | the FD-jet κ-reconstruction (HR129 §3b machinery) degrades from k=4 (rel. error 1.3e3 at k=4); one honest `fd_unresolved` refusal at k=5; self-flags `format_precision_pinned` from k=4 onward |

**Depth advantage I3 − I2: −12 decades.** [measurement] This is the campaign's headline honest negative (Design Principle 1): on this fixture the V4 probe's curvature extractor is the instrument that gets buried first, while the instruments it was built to audit read the saturating κ cleanly. **Zero unflagged confidently-wrong rungs for any instrument:** every I3 rung with error >10·tol carries the fpp self-flag — the typed instrument knows it is in a bad regime even when its value is wrong. That self-awareness is real and measured; the depth is not there.

[inference, high confidence] Mechanism: the FD jet differentiates `log2|w|` with `w = δ/(2+δ)` → tiny; the relative FD steps cross binades of `w` and the plateau gate selects steps where the quotient is cancellation-noise. The Phase A receipt's own boundary-row behaviour (operand-variation guard) anticipated this; the guard fires only at k=5, i.e. it under-fires by ~8 rungs on this ladder — an instrument-calibration gap worth filing (§6).

### F1b — the −2 eigenvalue (serves A6)

Scope note (Will's audit ruling): V3's −2 was **form-borne** — definitional from the X² lifting in the lifted-compatibility construction. F1b attributes **readability of a representation-layer invariant**, not emergent geometry.

[measured] I1 (eigvalsh) reads −2 **exactly** (error 0.0) at all 16 rungs. I3 (typed second difference on the decoupled z-block, h = 2^(binade(z)−6)) reads it to ≤1.8e-12 — five orders inside the 1e-9 tol — at all 16 rungs. I2: the V3 MCP surface exposes no Hessian-eigenvalue diagnostic (probed; pinned pre-sweep) → `oracle_quantity_unavailable` at every rung; V3's neighbour diagnostics recorded verbatim.

**The form-borne invariant is readable to the representability edge by both the naive and the typed instrument; V3-via-MCP cannot read it at all.** As the scope note requires: this says nothing about emergent geometry — the −2 lives in the representation layer and survives because the constraint form carries it exactly.

### F2 — blowup-exponent family, σ1 per rung (serves A4)

[measured] σ1 → 1.000 readable deep into the ladder by both I1 and I3 on all three families:

| family | I1 last trustworthy | I3 last trustworthy | I2 |
|---|---|---|---|
| ζ (critical line) | k=14 | k=14 (error 3e-16 at k=14) | `oracle_inexpressible` — `zeta` not in the V3 compiler allowlist |
| J₀ | k=14 | k=14 | `oracle_inexpressible` |
| Ai | k=14 | k=13 | `oracle_inexpressible` |
| sin (F2c control) | k=14 | k=14 | **alive**: last trustworthy k=14, but error grows steeply (4e-7 → 4e-5 → 3.9e-3 over k=10→14) — V3's classifier visibly approaching its floor exactly where the ladder bottoms out |

- ζ caveat (pre-registered): no pure-float64 ζ exists; I1-ζ is mpmath-computed/float64-truncated, so its noise floor is unrepresentative — J₀/Ai (scipy float64) are the honest I1 baselines.
- At k=14 the arbiter ground class goes `indeterminate` on most loci: the 1-ulp input transfer of the windowed σ1 becomes comparable to the quantity — **the measured edge of the quiet for this ladder geometry**.
- I3 vs I1 at the bottom (J₀/Ai, k=14): I1 still inside tol (2.9e-3, 7.3e-4); I3 outside (5.9e-2, 6.0e-2) **with its channel honestly at `ambiguous`** (the standard-error gate catches its own degradation). [inference] The transfer estimator divides function noise by δ = d/16, amplifying float64 evaluation noise ~16× relative to direct value reads — the typed route trades a thin slice of depth for self-diagnosis.
- F2c argument-reduction offsets recorded per rung as data (fl64(kπ) − kπ true), as ruled.

## 4. The attribution-quality number and the frozen verdicts

[measured, frozen mechanical rule] All six fixture groups land **`ambiguous`**, because attribution quality < 0.9 everywhere: F1a 0.25, F1b 0.25, ζ 0.83, J₀ 0.81, Ai 0.76, sin 0.83. The rule was applied exactly as frozen; it was NOT adjusted after seeing data (ruling 2).

[measured diagnosis of the misses] They are concentrated in two specific places, and both are findings about the *channel rules*, not about the readings:
1. **The glossary E-unsafe (|w|<1e-4) fpp rule fires from k=4 on F1.** On F1b the readings it flags are *exact to 1.8e-12* — the rule (calibrated on float32-era readback pipelines) is ~10 decades premature for direct-arithmetic float64 readings. This single rule accounts for the 0.25 scores.
2. **Shallow curved windows (k=0,1) on F2:** I3's channel honestly says `ambiguous` (slope standard error 0.09–0.17 — the window genuinely isn't a power law yet) while the arbiter calls the quantity resolvable. Honest conservatism scored as inconsistency.

[inference, post-hoc, clearly labelled — NOT a pre-registered result] Restricting to the frozen claim regime (k≥7), where the verdict rule already looks: ζ 0.968, sin 0.952, J₀ 0.914 — clearing 0.9, which would yield `phenomenon` for those families — Ai 0.865, F1a/F1b still 0.25. This is a diagnostic, not a verdict; promoting it would require a manifest re-freeze and re-audit.

## 5. Honest-failure section

- **No depth advantage for the V4 probe anywhere on this campaign.** F1a: −12 decades vs V3. F2: parity with naive float64 minus a thin slice at the very bottom. The probe's value showed up as *self-awareness* (refusals, fpp flags, ambiguous channels exactly where its readings degrade — zero unflagged confidently-wrong rungs across all 302 records, vs I2's F2c error growing 4 decades with `stability: stable` self-reports), not as depth.
- **The fpp channel rule is miscalibrated at float64 depth** (finding #1 above) — it cost F1b a `phenomenon`-grade readability verdict the raw errors plainly support.
- **The FD-jet extractor under-guards**: its operand-variation guard fired at 1 of the ~12 rungs where its κ reading was outside tol.
- **The frozen tol was generous to I2-F2c**: V3's alpha hit 0.39×tol at k=14 and rising — one more rung would have exposed it; the ladder ended first.
- F3 (Kerr) not attempted — F1+F2 consumed the budget; needs Will's surface form and a manifest v2 anyway.
- Acceptance Criterion 6 (determinism on two different days) is half-met: day 1 green; day 2 pending.

## 6. Gaps filed (Design Principle 4 — none required new primitives mid-campaign)

1. **Instrument-calibration gap:** the `format_precision_pinned` E-unsafe threshold (|w|<1e-4) needs float64-depth recalibration; it is the single largest attribution-quality cost. (Channel rule, not a primitive.)
2. **Guard gap:** the Phase A operand-variation guard under-fires on deep-approach ladders (fired k=5 only; readings bad from k=4 through k=15). Candidate fix lives inside the existing fd-metrology module's declared gates.
3. **Oracle surface gap (informational):** V3-via-MCP exposes no Hessian-eigenvalue diagnostic and cannot express ζ/J₀/Ai — two structural boundaries of the oracle, now documented with probes.

## 7. Scoreboard diffs

See `Build_Docs/PROBE_READINESS.md` rows A4/A6 (updated this session, evidence pointers to this folder). A9 untouched (F3 not run).

## 8. Did the probe earn its three months?

[plain language; marked inference where it is one] On these ladders, the typed probe did not out-read anything: naive float64 and V3 read the Schwarzschild approach to the edge of representability, and the probe's own curvature extractor drowned eleven decades early. What the probe did do — measurably, on every one of 302 rungs — is *know its own state*: it refused, or flagged the format regime, or downgraded its channel, every single time its reading was bad, while the V3 oracle walked toward its floor on the sin control reporting `stable` the whole way, and could not even express two-thirds of the F2 fixtures or the −2 quantity. The honest answer is: **as a deeper instrument, no — not on these fixtures; as an instrument that cannot be confidently wrong, yes, and that property is now quantified.** The quiet, on this evidence, starts where the *extractors* fail, several decades before the format itself runs out — and the probe is currently the only instrument that says so out loud.

## 9. Reproduction

```bash
# gate + required tests (oracle must be reachable)
PYTHONPATH=src python -m pytest tests/test_quiet_*.py
# full sweep (refuses if manifest hash != pin)
PYTHONPATH=src python -m lloyd_v4.evals.shape_of_the_quiet_sweep
# analysis: metrics.json + attribution_table.md + figure, from records only
PYTHONPATH=src python -m lloyd_v4.evals.shape_of_the_quiet_analysis
```
Environment pins in the manifest; oracle binary + version asserted at run time.
