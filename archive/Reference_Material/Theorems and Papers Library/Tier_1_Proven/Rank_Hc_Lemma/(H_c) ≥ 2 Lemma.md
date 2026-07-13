# rank(H_c) ≥ 2 Lemma

**Status:** PROVEN — Tier 1
**Type:** Lemma
**Source:** Discovered during Phase 0 audit (10 April 2026); proven by Gemini audit (Auditor Task #4)
**Dependencies:** None (pure linear algebra)
**Downstream:** Dual Confinement Theorem (constrains testability)

---

## Statement

For any nonzero symmetric matrix M ∈ Sym(n, ℝ) with zero diagonal entries (M_ii = 0 for all i), the rank of M is at least 2.

## Proof

By contradiction. Assume rank(M) = 1. Then M = λvvᵀ for some nonzero v ∈ ℝⁿ and λ ≠ 0. The diagonal entries M_ii = λv_i². Since M_ii = 0 for all i, we require v_i = 0 for all i, hence v = 0, contradicting nonzero rank. Therefore rank(M) ≥ 2.

## Structural Consequence

Since H_c is a symmetric matrix with zero diagonal (by construction), any nonzero H_c has rank ≥ 2. This means:

1. **Coupling-confinement is untestable at n = 3.** The confinement theorem says e_k(Ŝ_c) = 0 for k > rank(H_c). At n = 3, the only floor is Floor 2 (k = 2). Since rank(H_c) ≥ 2, the confinement bound never engages — coupling curvature is always allowed on Floor 2.

2. **Coupling-confinement first engages at n = 4.** At n = 4, Floor 3 exists (k = 3). If rank(H_c) = 2, then e₃(Ŝ_c) = 0 — coupling curvature vanishes on the top floor.

3. **HVP Tests 2.4 and 2.5 are mathematically invalid** as originally written (they assumed rank(H_c) = 1 was possible). Flagged for revision.
