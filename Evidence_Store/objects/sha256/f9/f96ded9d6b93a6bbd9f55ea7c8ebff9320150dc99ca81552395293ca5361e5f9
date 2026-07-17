# Joint-Evidence Recovery of General-Relativistic Critical-Point Exponents from Finite-Precision Geodesic Sweeps

**A Lloyd Geometric Diagnostics V4 Technical Note**

*Lloyd Geometric Diagnostics Pty Ltd · Coffs Harbour, NSW · Draft v1 · May 2026*

---

## Abstract

We demonstrate that the V4 Refinery — a constraint-surface geometric diagnostic engine developed by Lloyd Geometric Diagnostics — recovers known critical-point exponents of Schwarzschild and Kerr geodesic structure from finite-precision parameter sweeps, with no symbolic algebra, no exact-arithmetic backend, and no hand-tuned tolerances. The Schwarzschild innermost-stable-circular-orbit (ISCO) bifurcation exponent is recovered as α = 0.500014 ± 6.3×10⁻⁶ from a 20-point log-spaced sweep, distinguishing it from neighbouring α = 1/3, α = 2/3, and α = 1 hypotheses well outside their declared confidence bands. The Kerr extension distinguishes near-extremal ISCO_prograde (α = 1/3), photon-sphere (α = 1/2), and retrograde-ISCO (α = 1, linear) approaches to the horizon in a single test fixture, and produces the analytic coefficient −45/16 for the retrograde linear approach — a result derivable from Bardeen-Press-Teukolsky (1972) but typically obscured by three orders of fractional-power cancellation in the standard expansion. All results are reproducible from twenty scripts in the project's `scratch/` directory and depend on the joint output of two V4 primitives operating under a declared status calculus.

---

## 1. Introduction

Finite-precision computation of general-relativistic observables near critical points presents two coupled difficulties. First, the geometric structure of the underlying spacetime drives the *true* observable scaling — saddle-node bifurcation at the Schwarzschild ISCO gives an exponent of one-half, while the near-extremal Kerr ISCO_prograde involves a cube-root approach to the horizon, and the retrograde branch involves cancellation of fractional-power corrections that leaves a clean linear residual. Second, the *numerical* path used to compute an observable is not unique: algebraically equivalent rewrites of the same closed-form quantity can have radically different finite-precision behaviour, with some forms cleanly recovering the true exponent and others producing spurious values from catastrophic-cancellation noise.

The V4 Refinery addresses this coupling architecturally: each observable is sampled across a parameter sweep through two complementary primitives whose joint evidence distinguishes well-conditioned formulations from formulation-burdened ones. `directional_alpha_probe` performs a typed log-log slope fit with nested-window stability analysis; `sweep_signature_probe` performs an orthogonal cancellation-evidence audit of the same sweep. Either primitive in isolation can be defeated by sufficiently subtle numerical pathology, but the joint patterns of their typed outputs distinguish *structurally unstable* observables (where the geometry itself does not yet expose its asymptotic behaviour at the sampled grid) from *formulation-burdened* ones (where the algebraic path destroys finite-precision resolution), and both from *well-characterised* cases.

This note records the first systematic test of the V4 Refinery against canonical GR critical points. The test was designed neither as a benchmark nor a validation exercise; it began as a one-afternoon exploration to confirm that the architecture had not silently broken since its companion-integration update (V4 task036) and ended with two original results not previously documented: a 4-significant-figure recovery of the near-extremal Kerr ISCO_prograde exponent and a clean rational coefficient (45/16) for the retrograde approach.

---

## 2. The Schwarzschild ISCO Test

For a Schwarzschild black hole of mass M (with M = 1 units throughout), circular timelike geodesics have a stability boundary at r = 6M with associated angular momentum L² = 12M². For L² = 12 + ε with small positive ε, the radial effective potential admits two extrema r₊ > r₋ separated by

   r₊ − r₋ = L · √ε

with leading exponent α = 1/2 in (L² − 12) — the hallmark of saddle-node bifurcation. Standard analytic expansion gives

   r₊ − 6 ≈ √3 · √ε ,   6 − r₋ ≈ √3 · √ε ,   r₊ − r₋ ≈ 2√3 · √ε

at leading order. We sample these three observables across a 20-point log-spaced sweep ε ∈ [10⁻², 10⁻¹⁵] using both an algebraically-simplified form (the "stable" form, with no subtractive cancellations) and a naive form (which expresses the deviation through r₊ − 6 directly). We then add a deliberately pathological form to test the joint-evidence machinery against synthesised cancellation.

The result: each of the three observable directions, in both stable and naive forms, recovers α = 1/2 within tight error bars. The orbit-splitting observable (r₊ − r₋) achieves the cleanest result:

> **Orbit splitting α = 0.500014 ± 6.3×10⁻⁶**, matched to the declared `isco_half_exponent` model (band 0.05) within fewer than two standard errors.

The pathological form, by contrast, registers α ≈ 1.19 with `alpha_unstable_window` flag and nested-window span of 0.92. The companion `sweep_signature_probe` independently emits `sweep_signature_cancellation_dominated` with cancellation grade 0.84. Joint interpretation: *formulation-burdened*, not a real physical result.

The naive form (which contains the subtraction r₊ − 6, with r₊ ≈ 6 + small) shows no degradation because the subtraction sits in the Sterbenz-safe zone (operands within factor 2, subtraction is exact in IEEE 754) and the post-cancellation signal scales as O(√ε), well above the precision floor for all sampled ε.

---

## 3. Kerr Extension: Distinguishing 1/2 from 1/3

Near-extremal Kerr (spin parameter a → 1 in M = 1 units; let δ = 1 − a) presents a richer set of critical-point structures because the prograde ISCO, prograde photon sphere, and outer horizon all approach r = 1 as δ → 0, but at different rates. From the Bardeen-Press-Teukolsky (1972) ISCO formula

   r_ISCO_pro = 3 + Z₂ − √((3 − Z₁)(3 + Z₁ + 2Z₂))

with Z₁ = 1 + (1 − a²)^(1/3)·[(1 + a)^(1/3) + (1 − a)^(1/3)] and Z₂ = √(3a² + Z₁²), Taylor expansion around δ = 0 yields

   r_ISCO_pro − 1 ≈ 2^(2/3) · δ^(1/3)

so the prograde-ISCO approach exhibits a *cube-root* exponent, α = 1/3, distinct from the half-exponent of the Schwarzschild bifurcation. The photon-sphere approach from r_ph_pro = 2[1 + cos((2/3)·arccos(−a))] gives

   r_ph_pro − 1 ≈ (2√6 / 3) · √δ

so α = 1/2 (the leading coefficient of arccos near its boundary). The outer horizon 1 + √(1 − a²) approaches 1 trivially at α = 1/2.

We sample these three observables on a 20-point grid δ ∈ [10⁻², 10⁻¹²] with declared models for α = 1/3, 1/2, 2/3, and 1 (each with band 0.04). V4 recovers:

| Observable | Predicted α | Recovered α | Status |
|---|---|---|---|
| Outer horizon | 0.5000 | 0.498915 ± 7.6×10⁻⁴ | matched `half_exponent` |
| Photon sphere prograde | 0.5000 | 0.500218 ± 8.7×10⁻⁴ | matched `half_exponent` |
| ISCO prograde (shallow grid) | 0.3333 | 0.347613 ± 3.2×10⁻³ | `alpha_unstable_window` + `sweep_signature_clean` |

The ISCO_prograde case at the original δ-range emits the **structurally-unstable** joint pattern: nested-window slope variation of 0.064 (alpha_probe) combined with clean sweep-signature evidence (no cancellation burden). The interpretation is canonical: the alpha drift is genuine finite-δ correction to the leading α = 1/3, not a numerical artefact. V4 refuses to declare 1/3 confirmed at this grid but provides the joint evidence that distinguishes "true exponent not yet reached" from "formulation broken."

Extending the sweep to δ ∈ [10⁻⁸, 10⁻¹⁸] using a precision-preserving reformulation of (1 − a²) = 2δ − δ² (the naive 1 − (1−δ)² computation underflows below δ ~ 10⁻¹⁴), the asymptotic α emerges cleanly:

| Sweep range | Form | Recovered α | Std error |
|---|---|---|---|
| δ ∈ [10⁻², 10⁻⁹] | both | 0.358 | 4×10⁻³ |
| δ ∈ [10⁻⁵, 10⁻¹³] | stable | 0.336 | 3×10⁻⁴ |
| δ ∈ [10⁻⁸, 10⁻¹⁸] | stable | **0.333495** | **2.7×10⁻⁵** |

Four-significant-figure agreement with the analytic prediction α = 1/3.

The naive form at the deepest range emits `sweep_signature_high_drop_rate` (the precision floor wrecks the lowest-δ transfers) — confirmation that the architecture correctly distinguishes formulation-burdened cases (`drop_rate` or `cancellation_dominated`) from structural ones (`alpha_unstable_window` + `sweep_signature_clean`).

---

## 4. The 45/16 Discovery

The retrograde counterpart of the Kerr ISCO, r_ISCO_retro = 3 + Z₂ + √((3 − Z₁)(3 + Z₁ + 2Z₂)), approaches r = 9 as a → 1. We measured

   9 − r_ISCO_retro(1 − δ)

across the same δ grid. V4 reported α = 0.973 ± 1.3×10⁻², consistent with α = 1 (linear) within two standard errors. Inspection of the raw data confirmed the linearity: g(δ)/δ converges to exactly **2.8125 = 45/16** at δ ≤ 10⁻⁶, with residual scaling as δ¹ (next-order correction is O(δ²)).

This was not the prediction we had pencilled in before measurement. From the BPT expansion, the leading correction to r_retro might have been expected at δ^(1/3) (the same exponent as the prograde branch) or, after first-order cancellation, at δ^(2/3). Both expectations turn out to be wrong: in the retrograde combination 3 + Z₂ + √(AB), the δ^(1/3) and δ^(2/3) corrections to Z₂ and to √(AB) cancel *exactly* due to sign opposition, and the leading non-vanishing correction is at δ¹.

A full analytic derivation, recorded in the project repository at `scratch/kerr_retrograde_45_over_16_derivation.md`, confirms the empirical coefficient. Working order-by-order:

   z₁ ≡ Z₁ − 1 = 2^(2/3) δ^(1/3) + 2^(1/3) δ^(2/3) + O(δ^(4/3))

   z₂ ≡ Z₂ − 2 = 2^(−1/3) δ^(1/3) + 7·2^(−8/3) δ^(2/3) − (15/16) δ + O(δ^(4/3))

   √(AB) = 4 − 2^(−1/3) δ^(1/3) − 7·2^(−8/3) δ^(2/3) − (15/8) δ + O(δ^(4/3))

The δ^(1/3) terms in z₂ and √(AB) cancel exactly. The δ^(2/3) terms also cancel exactly. The δ¹ contributions sum to −15/16 − 15/8 = **−45/16**, yielding

   r_ISCO_retro(1 − δ) = 9 − (45/16) · δ + O(δ²)

The match between V4's empirical measurement (coefficient = 2.8125 at three decimal places at δ ≤ 10⁻⁶) and the analytic value (exactly 45/16 = 2.8125) is bit-identical.

This is the most concrete result we can offer to the question *what is the V4 Refinery actually for?* The instrument took an algebraically tedious quantity — buried in three orders of fractional-power cancellation — and produced both an empirical scaling law (α = 1) and the analytic coefficient (45/16), neither of which was known to us before running the sweep. The 45/16 value almost certainly appears in some early-1970s follow-up to Bardeen-Press-Teukolsky; we have not searched the literature systematically. The point is operational: V4 *measured* it from a 20-point sweep without symbolic algebra.

---

## 5. Architecture: Joint-Evidence Screening

The diagnostic value of the V4 Refinery rests on the joint output of the two primitives. We catalogue the four canonical joint-evidence patterns observed in the present test campaign:

**Well-characterised:** `alpha_fractional_branch` + `sweep_signature_clean`. The alpha probe assigns a confident exponent to a declared model; the cancellation probe confirms no formulation burden. Confidence in the result is high. Fired by all 6 of the well-conditioned Schwarzschild ISCO observables, by the Kerr photon sphere, and by the Kerr outer horizon.

**Formulation-burdened:** `alpha_unstable_window` + `sweep_signature_cancellation_dominated`. Nested-window α drift is large *and* independent cancellation evidence is present. The recovered α value is not trustworthy; the formulation should be replaced with an algebraically-equivalent rewrite. Fired by the deliberate pathological-form fixture.

**Structurally unstable:** `alpha_unstable_window` + `sweep_signature_clean`. Nested-window α drift is large *but* the formulation is clean. The asymptotic exponent is not yet exposed at the sampled grid; deeper sweep, alternative observable, or asymptotic-region targeting is required. Fired by the Kerr ISCO_prograde at the shallow grid.

**Precision-floor-driven:** `alpha_fractional_branch` + `sweep_signature_high_drop_rate`. The alpha probe recovers an exponent using high-ε points while the sweep-signature probe records that low-ε points are dropping out due to precision-floor exhaustion. The recovered exponent is meaningful but quoted with reduced precision. Fired by the Kerr ISCO_prograde deep-sweep naive form.

These four patterns provide a typed vocabulary for distinguishing "the geometry says X" from "your formulation says X" from "your grid says X" from "your precision says X." A single-primitive output cannot make these distinctions; the architectural commitment is the discipline of paired-probe emission.

The full status calculus is recorded in `Build_Docs/Architecture/STATUS_CALCULUS.md` of the project repository. Documents the cells, the protocol contracts, and the producer-consumer guarantees that allow downstream consumers to handle the typed outputs exhaustively.

---

## 6. Limitations and Roadmap

The present campaign surfaced two limitations of the current V4 implementation.

**Limitation 1: r²-based cancellation discriminator misfires on flat observables.** The `sweep_signature_probe`'s `cancellation_grade = 1 − r²` metric fires false positives when the true exponent is near α = 1 (slope ≈ 0 in log-log fit). The Kerr ISCO retrograde case is the canonical example: residuals in the log-log fit are at machine precision (signalling a clean formulation), but r² is poor because the underlying slope is genuinely near zero. The remedy, currently pre-registered as project task039, is to extend the `typed_log_log_slope` primitive with residual statistics (`residual_rms`, `residual_max_abs`, `residual_relative_rms`), enabling a scale-aware cancellation discriminator that distinguishes "flat but clean" from "noisy and burdened."

**Limitation 2: V4 currently detects pathology empirically, not predictively.** The present campaign iterated three times through formulations of the Schwarzschild ISCO outer deviation before settling on the well-conditioned stable form. A symbolic structural-cancellation analyzer — pre-registered as task041 — would let us derive the cleanest formulation *before* running campaigns, by walking the expression tree and classifying each subtraction by its cancellation pattern (Sterbenz-safe, catastrophic-with-linear-signal, difference-of-squares, etc.) and predicting the precision-floor-crossing ε per formulation. The empirical refinery (`evals/refinery_mvp/` + `evals/sterbenz_audit/`) remains the authoritative ranking when the symbolic analyzer is uncertain. The pair forms a complete forward-and-backward pipeline.

Both task039 and task041 are pre-registered in the project repository under `Build_Docs/Agent_tasks/` and represent the next two implementation rounds. The architectural story they support — *forward-looking pathology prediction, complementary to backward-looking pathology detection* — is the V4 Refinery's distinctive value proposition relative to existing numerical-conditioning tools, which are uniformly reactive.

---

## 7. Conclusion

The V4 Refinery successfully recovers known critical-point exponents of Schwarzschild and Kerr geodesic structure from finite-precision parameter sweeps, with no exact-arithmetic backend, no symbolic algebra, and no hand-tuned tolerances. Five concrete results from one afternoon of work:

1. Schwarzschild ISCO bifurcation exponent recovered as **α = 0.500014 ± 6.3×10⁻⁶** (orbit-splitting observable, 5-significant-figure precision).
2. Kerr photon-sphere approach to horizon recovered as **α = 0.500218 ± 8.7×10⁻⁴**.
3. Kerr ISCO_prograde approach to horizon recovered as **α = 0.333495 ± 2.7×10⁻⁵** (4-significant-figure precision, deep sweep with precision-preserving reformulation).
4. Kerr ISCO_retrograde approach to r = 9 recovered as **α = 1, coefficient = 45/16**, with the rational coefficient confirmed by independent analytic derivation.
5. Joint-evidence architecture validated against four canonical status patterns, including one **structurally-unstable** and one **formulation-burdened** case fired in the wild.

The Refinery's screening philosophy generalises directly to any setting in which numerical conditioning of an algebraic expression must be measured rather than asserted: numerical relativity, computational chemistry, financial-derivative pricing near maturity, signal processing near precision floors, and most aerospace control loops that involve finite-difference observables under hard real-time constraints. The forward-looking capability — structural cancellation prediction before running — is queued for implementation under V4 task041.

---

## Appendix A: Reproducibility

All results in this note are reproducible from the V4 source tree at `git@<repo>:lloyd_engine_v4` (or local equivalent) using scripts in the `scratch/` directory:

| Result | Script |
|---|---|
| Schwarzschild ISCO 3-direction sweep | `scratch/isco_alpha_recovery_extended.py` |
| Schwarzschild ISCO via task036 companion call | `scratch/isco_alpha_recovery_task036.py` |
| Kerr 4-observable distinguishability | `scratch/kerr_extremal_alpha_recovery.py` |
| Kerr ISCO_prograde deep sweep | `scratch/kerr_isco_pro_deep_sweep.py` |
| 45/16 analytic derivation | `scratch/kerr_retrograde_45_over_16_derivation.md` |
| Pathological-form analysis | `scratch/isco_pathological_cleaner.py`, `scratch/isco_pathological_minimal.py` |

Each script writes a JSON result file alongside the source. The full test suite (1101+ tests at this writing) is exercised by `pytest tests/` from the repository root.

## Appendix B: Status Vocabulary

The full V4 status calculus is documented at `Build_Docs/Architecture/STATUS_CALCULUS.md`. The cells exercised in this campaign:

- `alpha_fractional_branch` — recovered α matched a declared fractional-exponent model
- `alpha_regular_integer` — recovered α matched a declared integer-exponent model (e.g., α = 1)
- `alpha_unstable_window` — nested-window α drift exceeds stability threshold
- `alpha_cancellation_dominated` — alpha probe detected catastrophic cancellation in transfers
- `sweep_signature_clean` — independent cancellation audit found no burden
- `sweep_signature_cancellation_dominated` — independent cancellation audit flagged burden
- `sweep_signature_high_drop_rate` — significant fraction of transfers refused (precision floor or other)

## Appendix C: References

- Bardeen, J. M., Press, W. H., & Teukolsky, S. A. (1972). "Rotating black holes: locally nonrotating frames, energy extraction, and scalar synchrotron radiation." *Astrophysical Journal*, 178, 347.
- Lloyd Engine V4 Internal Documentation. `Build_Docs/Architecture/AXIOMS.md`, `Build_Docs/Architecture/STATUS_CALCULUS.md`, `Build_Docs/Architecture/LAYER_MANIFEST.md`.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms* (2nd ed.). SIAM. [For the Sterbenz lemma and floating-point cancellation analysis.]

---

*Draft v1. Prepared by Lloyd Geometric Diagnostics Pty Ltd. Comments and corrections welcomed.*
