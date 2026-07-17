# Gradient Focusing Classification

**Status:** HYPOTHESIS — Tier 3
**Type:** Diagnostic classification (proposed fifth fault class)
**Source:** Session handoff 10 April 2026, Section 3.4; Van der Waals critical point analysis
**Reframing:** N-Variable Engine Handoff (11 April 2026), Section 4.1

---

## Proposed Five-Fault Taxonomy

1. **Coupling fault** — κ_c changes via cross-derivative shift
2. **Self fault** — κ_s changes via diagonal Hessian shift
3. **Interaction fault** — κ_int changes via joint coupling-self shift
4. **Gradient modulation** — gradient drifts but Hessian structure fixed
5. **Gradient focusing** — |g| minimises at fixed numerator (NEW)

## Mechanism

K_G = numerator / |g|⁴. At a phase transition, |g| reaches a local minimum (one gradient component → 0 because the isotherm inflects). The |g|⁴ denominator shrinks, K_G spikes — but the numerator stays approximately constant. This is geometrically distinct from coupling/self/interaction faults.

## Evidence

- Observed on Van der Waals critical point
- Consistent with Finding 3 (cone tip progression — near-zero gradient amplification)
- Plausible physical interpretation: thermodynamic phase transitions correspond to gradient focusing rather than coupling singularities

## ⚠ N-Variable Handoff Correction

> "Not a theorem. The mathematical content is correct: when |g| → 0, the 1/|g|⁴ factor amplifies noise catastrophically. The physical interpretation — that thermodynamic phase transitions correspond to gradient focusing rather than coupling singularities — is plausible but untested across enough systems to be called a theorem. Reframe as a hypothesis."

## Engineering Response

Implement KG_num / KG_den tracking (numerator/denominator separation) regardless of the theoretical framing. This is the correct engineering response whether or not gradient focusing is formalised as a theorem.

## What to Do Next

- Implement numerator/denominator tracking in the engine
- Test gradient focusing signature across multiple phase-transition systems (not just Van der Waals)
- If pattern holds across ≥5 independent systems, upgrade to Tier 2
