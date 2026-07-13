# Alexandrov-Fenchel Engagement

**Status:** OBSERVED PATTERN — Tier 3
**Type:** Hypothesis with partial evidence
**Source:** Session handoff 10 April 2026, Section 3.5
**Reframing:** N-Variable Engine Handoff (11 April 2026), Section 4.4

---

## Hypothesis

When both Ŝ_c and Ŝ_s are positive semidefinite, the Alexandrov-Fenchel inequality holds:

    κ_int² ≥ 4 κ_c κ_s

The interaction is bounded from below — coupling and self curvature with the same sign cannot coexist without forced crosstalk. The AF gap metric Δ_AF = κ_int² − 4κ_cκ_s measures distance from AF saturation.

## Evidence

**Verified (exact saturation) on isotropic surface:**

F = x₁² + x₂² + x₃² + a(x₁x₂ + x₂x₃ + x₃x₁) − 3 at (1,1,1):

    κ_c = a²/(3c²)        where c = 2 + 2a
    κ_s = 4/(3c²)
    κ_int = −4a/(3c²)
    κ_int² = 16a²/(9c⁴) = 4 κ_c κ_s    EXACTLY
    Δ_AF = 0 for all a

The S₃ symmetry forces Ŝ_c and Ŝ_s into perfect eigenvector alignment — the AF equality condition.

**Correctly predicted disengagement on Van der Waals:**

rank(H_s) = 1 (only V is nonlinear), so κ_s = 0 on Floor 2 by self-confinement. AF bound permanently disengaged. The critical point is a gradient focusing event, not an AF transition. This was the right result and validated the confinement theorem in the process.

## ⚠ N-Variable Handoff Correction

> "No derivation connecting the Alexandrov-Fenchel inequality to this specific discriminant formula is provided. Do not implement this tracker until a derivation is produced. If a derivation is found and verified, add the tracker then. Computing a number with no proven geometric meaning and labelling it with a prestigious name is the kind of over-claim the validation programme exists to prevent."

## What to Do Next

1. Produce a formal derivation connecting AF to κ_int² ≥ 4κ_cκ_s
2. If derivation succeeds, implement Δ_AF tracker
3. If derivation fails, retire the AF attribution and investigate whether the observed pattern has a different source
