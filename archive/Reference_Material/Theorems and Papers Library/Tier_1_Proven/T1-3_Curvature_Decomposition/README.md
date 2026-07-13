# Theorems 1–3 — Curvature Decomposition and Uniqueness

**Status:** PROVEN — Tier 1
**Type:** 3 Theorems (algebraic decomposition, geometric decomposition, uniqueness)
**Source:** Companion paper v3, Sections 3–4
**Dependencies:** Standard differential geometry (bordered Hessian, shape operator, det₂ identity)
**Downstream:** Theorem 4, Theorem 5, D-6, decomposition symmetry, CWRU validation, hierarchy

---

## Statements

**Theorem 1 (Algebraic Decomposition).** The bordered Hessian determinant for F(x₁, x₂, x₃) = 0 expands into 12 terms partitioning exhaustively as det(H_b) = Δ_c + Δ_s + Δ_m.

**Theorem 2 (Geometric Decomposition).** The shape operator decomposition Ŝ = Ŝ_c + Ŝ_s yields K_G = κ_c + κ_s + κ_int via the 2×2 determinant identity.

**Theorem 3 (Uniqueness).** The geometric decomposition is algebraically identical to the bordered Hessian decomposition: κ_c = −Δ_c/|g|⁴, κ_s = −Δ_s/|g|⁴, κ_int = −Δ_m/|g|⁴.

## Closed-Form Expressions

    κ_c = (2 g^T H_c² g − |g|² tr(H_c²)) / (2|g|⁴)
    κ_s = (|g|²(tr(H_s)² − tr(H_s²)) + 2 g^T H_s² g − 2 tr(H_s)(g^T H_s g)) / (2|g|⁴)
    κ_int = (2 g^T H_c H_s g − tr(H_s)(g^T H_c g)) / |g|⁴

## Verification Record

- 9 analytical test surfaces spanning 6 curvature regimes (companion paper Table 1)
- 138 domain adapter surfaces: 130 PASS / 4 SKIP / 1 genuine precision limitation / 3 reclassified
- Two independent computational systems, zero discrepancies on 7 analytical derivations
- Full verification in Running Validation Report (8 April 2026)
- Canonical regression surface: F = x₁² + x₁x₂ + x₃² − 3 at (1,1,1)

## Key Properties

- Decomposition is exact: K_G = κ_c + κ_s + κ_int holds identically
- Decomposition is coordinate-DEPENDENT: rotation redistributes components (OE-5)
- Decomposition ratios are scale-INVARIANT: all components scale by 1/λ² (D-14)
- For explicit surfaces: κ_int = 0 identically (D-6)

## Publication Status

- Companion paper v3 complete in project knowledge
- v4 required: cone counterexample qualification, symmetry profile, CWRU results
- Patent coverage: AU 2026902926

---

## ⚠ MANUAL PLACEMENT REQUIRED

Place a copy of `coupling_curvature_paper_v3.md` in this directory.
