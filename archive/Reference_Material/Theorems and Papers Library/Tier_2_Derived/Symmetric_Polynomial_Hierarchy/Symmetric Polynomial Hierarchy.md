# Symmetric Polynomial Hierarchy

**Status:** DERIVED, AWAITING n-VARIABLE VALIDATION — Tier 2
**Type:** Theorem (in waiting)
**Source:** Session handoff 10 April 2026, Section 3.1; hierarchy_report.docx
**Dependencies:** Shape operator decomposition Ŝ = Ŝ_c + Ŝ_s
**Blockers:** n-variable engine needed for Floor 3+ computational validation

---

## Statement

The k-th elementary symmetric polynomial of the shape operator eigenvalues decomposes into k+1 terms of definite coupling-self order via the mixed discriminant expansion:

    e_k = e_k(Ŝ_c) + Σ_{p+q=k, p≥1, q≥1} D_{(p,q)}(Ŝ_c, Ŝ_s) + e_k(Ŝ_s)

## Floor Structure

| Floor | k | Curvature type | Components | Interaction terms | Independently verified? |
|-------|---|---------------|-----------|-------------------|------------------------|
| 1 | 1 | Mean curvature | 2 | 0 (no interaction) | ✅ YES (Gemini audit) |
| 2 | 2 | Gaussian curvature (n=3) | 3 | 1 (κ_int) | ✅ YES (138 surfaces) |
| 3 | 3 | e₃ (n=4 required) | 4 | 2 distinct orders | ❌ NO (needs n-var engine) |
| k | k | e_k | k+1 | k−1 | ❌ NO (k ≥ 3) |

For an n-variable system: n−1 floors total, n(n+1)/2 − 1 total diagnostic channels.

## What's Proven vs What's Derived

- **Proven:** Floor 1 (mean curvature, audited) and Floor 2 (K_G decomposition, 138 surfaces)
- **Derived:** The general floor expansion follows from the standard expansion of determinants of sums of matrices. The mathematical argument is clean.
- **Not yet validated:** Any floor ≥ 3 has not been computationally verified because the n-variable engine doesn't exist yet.

## What to Say in Presentation

"The K_G decomposition is Floor 2 of an (n−1)-floor building. Floor 1 — mean curvature — has been independently audited and has a clean two-way split with no interaction term. The general hierarchy is derived but awaits n-variable engine validation."

---

## ⚠ MANUAL PLACEMENT REQUIRED

Place `hierarchy_report.docx` in `Supporting_Documents/`.
