# CAMPAIGN DRAFT — The Separating Estimator (read through the noise)

**Status:** DRAFT v0, 2026-06-10. NOT ready for execution. Explicitly downstream of `CAMPAIGN_EXACT_JET_PRIMITIVE.md`; to be revised against its results (HR131), the HR130 §6 gap filings (E-rule recalibration), and Will's wave-two fixture selections before any pre-reads gate is attempted. This document captures design intent while it is fresh.

**Scoreboard rows served (anticipated):** A4 (deep blowup attribution), A6 (depth beyond formula-friendly fixtures), and the Milestone section's standing question — converting "never confidently wrong" into measured depth.

**Origin:** Shape of the Quiet (HR130) demonstrated the choice as currently built: instruments that walk to their floor *saying stable* (I2 on the sin control: four decades of error, self-reported healthy) versus an instrument that refuses at the first invalid signal (I3: zero unflagged wrong, −12 decades of depth). This campaign builds the third instrument: one that walks the degraded regime *reading*, separating phenomenon from substrate, refusing only where the separation model itself loses scope.

**The handrail principle (Will, 2026-06-10):** *the shape of the quiet is the handrail you find in the pitch black; determining the real handrail over some phantom object is critical before we shift our full weight onto it.* The failure mode that kills is grabbing the phantom rail while self-reporting stable. Separation is rail verification: every reading carries its split, and the weight goes only on the phenomenon component, with stated confidence.

---

## Design thesis

Refusal is the correct response to **unmodellable** contamination. V4's substrate program (BACL, Conjecture C, c2 lattice, fingerprint atlas, lawful precision scaling) is a **deterministic model of the contamination**. Where the model holds, the honest action is not refusal but **separation**: report reading = phenomenon-estimate ⊕ substrate-component, with typed confidence on the split. Honesty = calibrated claims, not silence. The refusal channel is retained for out-of-scope regimes — the coastline moves deeper; it never reaches zero (HR130 measured the arbiter's own edge at k = 14; the quiet keeps an interior).

## Three mechanisms (stackable; each independently testable)

### M1 — Substrate deconvolution
The known lattice structure (BACL rungs, binade ladder, c2 consequences) is the instrument response function of arithmetic. In the contaminated regime, fit the substrate model to the observed residual structure and report the deconvolved phenomenon estimate with typed uncertainty. Scope inherits the theorems' scopes verbatim (float64 normal range etc.); outside scope, M1 abstains.

### M2 — Route-ensemble separation (from B4)
Evaluate the target through k algebraically equivalent routes. The phenomenon is route-invariant by definition; each route's substrate fingerprint is distinct (B4, fingerprint atlas). **Common mode across routes = phenomenon; differential mode = substrate.** Lock-in amplification with algebraic equivalence as the reference signal.
**Calibration channel:** closed loops in the rewrite graph cancel the phenomenon exactly — loop traversals measure *pure substrate* from the same evaluations (the rewrite-holonomy object, 2026-06-10 discussion). Open paths read signal+noise; loops read noise alone; subtract.

### M3 — Precision-ladder extrapolation (from B2)
Residual scaling across formats is lawful and mechanism-invariant (float16/32/64 verified, HR-cited). Read at multiple formats plus one cheap mpmath rung, fit the known scaling law, extrapolate the zero-substrate limit, and carry typed provenance on the extrapolation itself. Deterministic Richardson — no Monte Carlo, because the noise model is exact in scope.

## Output type (the new contract)

A `SeparatedReading`: { phenomenon_estimate, substrate_component, split_confidence, mechanism_provenance (which of M1–M3 contributed and their agreement), scope_status (in-scope / out-of-scope per theorem), refusal (reserved for out-of-scope or mechanism-disagreement beyond pre-registered bounds) }. Mechanism disagreement is itself first-class data.

## Fixture requirements (wave two — Will selects)

Surfaces with **no well-conditioned closed form** — terrain where every instrument must difference, transport, or compose long chains, so substrate contamination is unavoidable rather than route-optional. HR130's lesson: F1a's quiet was hostile to differencing, friendly to direct evaluation; wave two must be hostile to *everything*. Candidates to consider at revision time: catastrophic-cancellation forms of the Quiet fixtures, composed transcendental chains, the F3 Kerr extremal approach (post surface-form decision), and at least one fixture where I1 (naive direct) demonstrably fails silently — the separator's value is only visible on terrain that punishes naivety.

## Pre-registered prediction (to be frozen at v1, stated now as intent)

On wave-two fixtures: the separator's phenomenon-estimate remains within pre-registered tolerance of the arbiter at depths where (a) I1 is confidently wrong, (b) I2 is confidently wrong or inexpressible, and (c) refusal-mode I3 has already abstained — i.e. measured depth advantage with retained zero-unflagged-wrong. The headline figure: depth-at-calibrated-accuracy per instrument, separator overlaid on the HR130 curves.

## Known open questions (resolve before v1 freeze)

1. E-rule recalibration (HR130 §6 gap) — M1's validity gating must not inherit the ~10-decade-early misfire.
2. Route-set selection for M2 — how many routes, chosen how, and the loop basis for the holonomy calibration channel.
3. Composition with the exact-jet primitive — M2/M3 on jet components, not just scalar reads.
4. Cost model — M2 multiplies evaluations by route count; pre-register the budget.
5. Whether mechanism agreement (M1 vs M2 vs M3 concordance) should gate the split_confidence formally — likely yes; define the calculus.

## Non-goals (standing, inherited)

No V3/OG imports; no post-hoc rule tuning; no substrate-theorem scope extensions smuggled in as estimator features — if a mechanism needs a theorem beyond current scope, that is a separate substrate campaign first.

## Revision protocol

This draft is revised to v1 only after: HR131 lands (exact-jet results), the E-rule gap is dispositioned, and Will selects wave-two fixtures. v1 then conforms fully to TASK_TEMPLATE.md (pre-reads gate, sufficiency gate, tests, commands, acceptance criteria) before any execution.
