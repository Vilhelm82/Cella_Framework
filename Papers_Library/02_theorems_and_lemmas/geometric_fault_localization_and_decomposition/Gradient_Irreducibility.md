# Theorem 4 — Gradient Irreducibility

**Status:** PROVEN — Tier 1
**Type:** Theorem
**Source:** Companion paper v3, Section 4.2
**Dependencies:** Theorems 1–3

---

## Statement

The gradient components g_i enter κ_c as free variables. A perturbation that changes g while holding H_c fixed generically changes κ_c.

## Proof Summary

Writing Q = H_c² − ½tr(H_c²)I, we have κ_c = g^T Q g / |g|⁴. For any nonzero H_c, Q is not proportional to the identity:

- **Unequal cross-derivatives:** H_c² has unequal diagonal entries, preventing Q from being scalar.
- **Equal cross-derivatives:** H_c² has identical diagonal entries BUT nonzero off-diagonal entries (products of distinct cross-derivatives), which again prevents Q from being a scalar multiple of I.

Both cases covered in v3 (the original paper only addressed the unequal case).

## Geometric Interpretation

The gradient defines the tangent plane. Changing the gradient tilts the plane, slicing the ambient coupling tensor H_c at a different angle. The coupling curvature is the cross-section of H_c projected onto the tangent plane, and the tangent plane's orientation is an irreducible part of the measurement.

## Significance

No alternative formulation of coupling curvature on an implicit constraint surface can eliminate the gradient dependence. This is not an artefact — it is a fundamental property of curvature measurement on implicit surfaces. Engineering mitigation strategies (direct cross-derivative monitoring, reference-gradient normalisation, ratio tracking) are documented in the companion paper Section 10.2.
