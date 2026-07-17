# Monge Prohibition

**Status:** PARTIALLY PROVEN — Tier 2
**Type:** Partial theorem + corollary (AF attribution dropped)
**Source:** Session handoff 10 April 2026, Section 3.6
**Correction:** N-Variable Engine Handoff (11 April 2026), Section 4.2

---

## Statement (corrected)

For any explicit surface F = x_n − f(x₁, ..., x_{n-1}):

**Part 1 (PROVEN — D-6):** κ_int = 0 identically. This is a theorem. See `Tier_1_Proven/D6_Interaction_Vanishing_Explicit_Surfaces/`.

**Part 2 (Corollary of Monge formula):** κ_c and κ_s cannot both be positive. Specifically:

    κ_c = −f_xy² / (1 + f_x² + f_y²)²    ← always ≤ 0 (negative of a square over a positive)
    κ_s = f_xx · f_yy / (1 + f_x² + f_y²)² ← sign depends on f_xx · f_yy

Since κ_c ≤ 0 always on a Monge patch, κ_c and κ_s cannot both be positive.

## ⚠ Correction from N-Variable Handoff

The original formulation attributed the sign constraint to the Alexandrov-Fenchel inequality. This attribution is NOT supported. The constraint follows trivially from the sign structure of the Monge formula. The AF machinery is not needed.

> "Keep the κ_int = 0 result as a theorem (it is one). Drop the AF attribution. Document the sign constraint on κ_c as a corollary of the Monge formula, not as a separate theorem."
> — N-Variable Engine Handoff, Section 4.2

## Practical Consequence

Filed as Operating Envelope Constraint OE-5 (note: this OE-5 is distinct from the decomposition coordinate-dependence OE-5). Every regression-fitted constraint surface in the existing TEP/CMAPSS pipelines is a Monge patch and cannot access the regime where both κ_c > 0 and κ_s > 0. Physics-derived implicit constraint equations are required for full hierarchy diagnostics including any AF-related monitoring.

## What to Do Next

- Present Part 1 as proven (D-6)
- Present Part 2 as a corollary of the explicit surface formula
- Do NOT invoke Alexandrov-Fenchel
