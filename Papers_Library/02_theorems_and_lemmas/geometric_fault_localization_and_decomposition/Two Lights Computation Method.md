# Two Lights Computation Method

**Status:** PROPOSED, NOT YET VALIDATED — Tier 2
**Type:** Computational method with mathematical justification
**Source:** Discovery D-11, Validation Report (8 April 2026); Running Validation Report "Two Lights" section
**Dependencies:** D-6 (κ_int = 0 on explicit surfaces), Theorema Egregium

---

## The Problem

The bordered Hessian formula K_G = −det(H_b)/|∇F|⁴ divides by the fourth power of the gradient magnitude. When the gradient is dominated by one component, the |∇F|⁴ denominator amplifies numerical noise catastrophically. This is Finding 3 / OE-4.

## The Solution

Eliminate the variable with the largest gradient component using the implicit function theorem to obtain an explicit surface z = f(x, y). Compute curvature from the explicit formula:

    K = (f_xx · f_yy − f_xy²) / (1 + f_x² + f_y²)²

Key properties:
- First derivatives f_x = −g_i/g_k are ratios with |f_x| ≤ 1 by construction
- Denominator (1 + f_x² + f_y²)² is always in [1, 9]
- No fourth-power gradient magnitude. No amplification catastrophe.
- κ_int = 0 by D-6, guaranteeing a clean two-way decomposition

## Three Proposed Variants

**Variant A (Single best projection):** Eliminate argmax|g_i|. Simplest. Falls back to bordered Hessian if g_k ≈ 0.

**Variant B (Stability-weighted ensemble — "two lights"):** Compute from all three eliminations, weight by w_k = |g_k|²/|∇F|². Best-conditioned projection dominates. Weighted average is exact (K_G is intrinsic).

**Variant C (Centrifuge-projection hybrid):** Use the centrifuge's identified natural coupling to select the elimination variable. Combines diagnostic richness with numerical stability.

## Infrastructure

The `projections` method in `lloyd_core.py` already computes f_xx, f_yy, f_xy for all three variable eliminations via `proj_2nd`. The infrastructure exists; the computation path needs wiring.

## Current Status

- Mathematically justified
- Infrastructure exists in engine
- Implementation scheduled 9 April but **not confirmed as completed**
- Testing plan defined (re-run 4 SKIP cases, 138-surface regression, cone-tip progression)

## What to Say in Presentation

Present as a proposed computational architecture with mathematical justification, not as a validated method. If asked about numerical conditioning: "We have a projection-based alternative that eliminates the |∇F|⁴ denominator entirely. The infrastructure exists; validation is in progress."
