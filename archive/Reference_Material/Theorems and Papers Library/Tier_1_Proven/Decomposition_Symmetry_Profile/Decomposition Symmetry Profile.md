# Decomposition Symmetry Profile (D-13, D-14)

**Status:** PROVEN (empirically characterised) — Tier 1
**Type:** Empirical characterisation with theoretical backing
**Source:** Validation Report Test 1.2b (8 April 2026)
**Dependencies:** Theorems 1–3, Theorema Egregium

---

## Complete Symmetry Table

| Property | K_G | κ_c | κ_s | κ_int | Ratios (κ_c/K_G etc.) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| Translation | ✅ Preserved | ✅ Preserved | ✅ Preserved | ✅ Preserved | ✅ Preserved |
| Rotation | ✅ Preserved | ❌ Redistributed | ❌ Redistributed | ❌ Redistributed | ❌ Changed |
| Scaling (λ) | ✅ 1/λ² | ✅ 1/λ² | ✅ 1/λ² | ✅ 1/λ² | ✅ Preserved |
| Gradient scaling | ✅ Preserved | — | — | — | ✅ Preserved (CWRU) |

## Key Results

**D-13 (Coordinate Dependence — OE-5 CONFIRMED):** 30° rotation on the mixed surface x² + xy + z² − 3 changed the coupling ratio from 0.333 to 0.622 (+87% κ_c magnitude, +465% κ_s magnitude). The sum K_G preserved to 0.001%.

**D-14 (Scale Invariance):** Under uniform scaling by λ, every component scales by exactly 1/λ². All ratios preserved exactly. Tested on saddle (λ=2), mixed surface (λ=2), and paraboloid (λ=2).

## Verification Record

- MR-1d (Translation): 2 surfaces, all components individually preserved. PASS.
- MR-2d (Rotation): 1 surface, components redistributed, sum preserved. OE-5 CONFIRMED.
- MR-3d (Scaling): 3 surfaces, all components scale by 1/λ², all ratios preserved. PASS.

## Deployment Implications

1. **Fixed installations:** Decomposition interpretation valid (sensor frame doesn't change)
2. **Fleet comparisons (same sensor frame):** Valid via coupling ratio (scale-invariant)
3. **Fleet comparisons (different sensor orientations):** Require coordinate frame alignment
4. **Cross-site K_G comparison:** Always valid (intrinsic, Theorema Egregium)

## Candidate for Paper v4

This symmetry table belongs in the companion paper as a formal result, likely as a new subsection in Section 4 after gradient irreducibility.
