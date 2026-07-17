# Floor 1 — Mean Curvature Decomposition

**Status:** PROVEN — Tier 1 (independently audited)
**Type:** Theorem
**Source:** Session handoff 10 April 2026, Section 3.2; Audit package
**Auditor:** William Lloyd
**Dependencies:** Standard mean curvature formula, Hessian decomposition H_F = H_c + H_s

---

## Statement

The mean curvature H of an implicit constraint surface decomposes exactly as:

    H = H_c + H_s     (no interaction term)

where:

    H_c = −g^T H_c g / (2|g|³)
    H_s = (|g|² tr(H_s) − g^T H_s g) / (2|g|³)

## Load-Bearing Claim

The "no interaction term" result is load-bearing. It was flagged as the focus of the independent audit. The absence of κ_int on Floor 1 (unlike Floor 2 where κ_int exists) follows from the linearity of trace and bilinearity of quadratic forms — the mean curvature formula is LINEAR in H_F, whereas the Gaussian curvature formula is QUADRATIC, which is why Floor 2 generates an interaction term but Floor 1 does not.

## Audit Record

- **Audit package:** `Audit_Package_MeanCurvatureDecomposition.md`
- **Auditor system prompt:** `auditor_system_prompt.txt`
- **Audit verdict:** `Audit_Report_Mean_Curvature_Decomposition.md`
- **Result:** CLEARED on all 6 subtleties; load-bearing no-interaction claim verified
- **Caveats:** Rounding errors in hand-computed decimals (symbolic forms correct); existing Workbench H_mean output deviates from analytical truth by ~5.7×10⁻⁷ (finite-difference noise)
- **Independent verification:** mpmath confirmed exact value of 6/(7√14) = 0.229081064496363758...

## Numerical Verification (Canonical Surface)

F = x₁² + x₁x₂ + x₃² − 3 at (1,1,1):

    H_c = −3/(14√14) ≈ −0.0572703
    H_s = 15/(14√14) ≈ 0.2863513
    H_c + H_s = 6/(7√14) ≈ 0.2290811 = H  ✓

## Significance

Floor 1 of the symmetric polynomial hierarchy. The clean two-way split (no interaction) means mean curvature provides an unambiguous coupling/self separation — even cleaner than K_G (Floor 2) which requires interpreting κ_int.

---

