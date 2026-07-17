# P1B REPORT — the damped arrow (resolved, with a corrected observable)
**Date:** 2026-07-02 · **Substrate:** [CONTAINER] `p1b_damped.py`, `p1b_diag.py`, `p1b_final.py` · **DF-6 FROZEN:** Rayleigh equal-joint damping in angle rates, discrete d'Alembert midpoint force via the wedge `W_i = q0_i ∧ q1_i`, symmetric ± split, γ = 1/10 at test.

## Proven structure
1. **Reversal defect ≡ γ·h·W_i, both circles, symbolically, all data** [PROVEN]. The arrow enters the discrete equations as exactly the velocity-odd Rayleigh impulse — the hinge the P1a theorem named, watched snapping.
2. **Corner identity persists for all γ** (damping is block-degree (1,0), below the corners) ⟹ ghosts (±i,±i) and **honest degree 30 in BOTH directions for all γ** [PROVEN — first reuse of the isotropic corner gate].
3. **Degree/count arrow-blindness at fixed k** [PROVEN mechanism + measured]: spectra are Zariski-locally-constant in γ and γ=0 is symmetric by the P1a theorem ⟹ small-γ spectra symmetric. Measured at γ=1/10: forward/backward 30/30 honest, 16/16 real.

## Prereg accounting (the kill condition fired — on the observable)
**P1b as preregistered ("damped asymmetry in the degree spectra") is REFUTED-BY-DERIVATION**, by the campaign's own P1a theorem plus γ-genericity, and confirmed by measurement. The prereg system worked exactly as designed: a frozen prediction died in public and is recorded as such. The framework's arrow claim survives in corrected form below.

## The certified arrow (corrected observable)
Field identity test: `U^bwd_x == U^fwd_{Rx}` (exact polynomial comparison, monic).
- **γ = 0 control: equal EXACTLY** — displacement 0.00e+00 (validates theorem + harness).
- **γ = 1/10: unequal as polynomials [CERTIFIED, exact]** — root-displacement field on the honest deg-30 fibers: **min 1.14e−6, median 1.63e−4, max 3.24e−2**, with real counts still 16/16. The arrow of time in this discrete system is invisible to every integer invariant measured and manifests as a quantitative displacement field between the backward fiber and the reversal-image of the forward fiber.

## Adopted observable + parked frontiers
Going forward, P1b-class claims use the reversal-conjugated eliminant mismatch (exact) and its displacement statistics (quantitative). Parked: (i) displacement scaling in γ (first-order theory predicts ∝ γ — quick sweep); (ii) the k→∞ degree-visible arrow (dissipative collapse onto attractors) — the true asymptotic home of a degree-level arrow.

## Harness note
Run-1's control "failure" was a comparison-line bug (root sets proved identical to 30 digits); run-1's defect printout exposed a sign error in the defect assembly (fixed; identity then exact). Both caught by the control discipline before any conclusion was drawn.
