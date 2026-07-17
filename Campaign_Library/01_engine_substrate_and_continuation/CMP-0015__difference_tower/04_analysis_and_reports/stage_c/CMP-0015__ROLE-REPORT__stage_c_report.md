# difference-tower — Stage C report (H6: the inversion figure)

**Status: STAGE C ALL PASS, FIRST RUN — C-P1 20/20 V-verdicts, C-P2
404/404 monotone steps (K3 NOT triggered), R-C1 retrodiction PASS, R-C2
108/108 noise-bound cells. The campaign's poster exists and says what
the thesis predicted.**
**Date:** 2026-06-12. **Branch:** `campaign/difference-tower`.
**Prereg:** frozen pre-execution, pin `3557b16a…d7b868` (with the full
ε-balance derivation, the R-C1 statement pinned before execution, and
the four-criterion informativeness dry-run). **Records:** sha256
`38c58b8d…eda16b`, byte-stable ×2 — **including the overlay figure PNG**
(sha `2a57e3ac…`). Full suite exit 0.

## 1. C-P1 — the raw V-window (arbiter-graded): **PASS 20/20 verdicts**

Every raw centered/forward Δ¹ error curve over j = 2..40 has its
measured minimum inside the analytically derived window
[round(j*) − 2, round(j*) + 2], where j* comes from the ε-balance with
DERIVED constants (u = 2⁻⁵³, two evaluations per curve value,
Sterbenz-exact subtraction, exact dyadic scaling — zero fitting):
h*_fwd = 2√(uM/|f″|), h*_cen = (3uM/|f‴|)^⅓. Ten fixture-points ×
both schemes, rational and annex alike. The h-dilemma's textbook
V-curve is now a measured, predicted object.

## 2. C-P2 — the lane curve (exact-ℚ, band-free, K3 LIVE): **PASS 404/404 — K3 NOT TRIGGERED**

Lane Δ¹ error vs the exact arbiter derivative, computed in ℚ at every
cell, compared exactly at every consecutive j-step over rule-derived
ladders reaching the lattice edge (forward to j = 53, centered to
j = 52): **monotone nonincreasing everywhere, no accuracy floor**. The
tails descend at the law slopes to the last realizable cell — forward
−1/j down to ~2⁻⁵⁷, centered −2/j down to ~2⁻¹¹¹. **The inversion is
real: where the raw curve turns back up, the lane curve keeps
descending. The cancellation that kills classical difference methods
is, on this substrate, reversed — H6's graded statement of the central
thesis, now certified in scope.**

## 3. R-C1 — the retrodiction gate: **PASS (mechanism story confirmed)**

Pinned pre-execution from the same ε-balance (statement in the frozen
prereg): all four failed Stage-B v2 fits straddle a predicted wall zone
(T3@0.5 forward — left wall, pre-asymptotic; T3@2.5 centered —
right-wall fail-predicted at noise fraction 5.1; T1@1.25 and T2@0.5
centered — right-wall zone); both fail-predicted rows are recorded
failures; all six pass-predicted rows passed; the four boundary-zone
rows (declared: u is a bound, libm realization varies) split 2/2 and
are recorded observationally. Stage B's finding #2 is now a
*predicted* phenomenon, not a story.

## 4. R-C2 — the noise formula as prediction: **PASS 108/108 cells**

At every windowed annex cell, both levels of the derived bound held:
curve-level |D_float − D_mp| ≤ N_scheme(h) and transfer-level
amplification ≤ 2·N_scheme(h)/δ with δ = η·h pinned as instrument
transfer. The perturbation-scale amplification that destabilized
Stage B's deep-end fits is quantitatively the derived formula —
verified, not narrated.

## 5. The overlay (OBSERVATIONAL deliverable)

`overlay_inversion_figure.png` — raw V-curves + lane curves, both
schemes, log₂|error| vs j, with the four Stage-B refusal points
annotated on their predicted walls (R-C1 confirmed, so the annotation
clause activated). Byte-stable across runs; no verdict rides on it.

## 6. Compliance

Prereg frozen first with: full derivation recorded; R-C1/R-C2 entered
as predictions pre-execution; informativeness dry-run (Amendment 3
standing law) — all four graded criteria pass under synthetic
predicted-law cases and fail under wrong-law controls. Byte-stable ×2;
records sha-pinned; every count names its unit; DP2 firings 0; H4
rules, atlas draft, substrate, registry untouched; suite exit 0.

— Claire, on the bench. STOPPED at the Stage-C report per the GO. Next
gate per the brief: H4 verdict-rule freeze (Will), pre-Stage-D.
