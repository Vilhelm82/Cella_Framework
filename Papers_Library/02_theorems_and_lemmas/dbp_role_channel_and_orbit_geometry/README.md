# Theorem 8.1 — Invariant Preservation under Role Transposition

**Status:** PROVEN — Tier 1
**Type:** Theorem + 2 Corollaries
**Source:** `theorem_8_1.pdf` (standalone proof, 4 pages)
**Dependencies:** None (foundational result)
**Downstream:** Governs every coupling-structural invariant in the framework

---

## Statement

**Theorem 1 (Invariant Preservation).** Let φ be a function on well-posed DBP triples.

(i) The coupling kernel K = (K_spec, K_hol, κ) is T-invariant: K(T_σ(τ)) = K(τ) for all σ ∈ S₃.

(ii) If φ factors through K, then φ is a DBP invariant.

(iii) If φ is coupling-structural and a DBP invariant, then φ factors through K.

(iv) The DBP invariants that do not factor through K are precisely the value-symmetric functions.

**Corollary 2 (Exhaustive Decomposition).** Every T-invariant function decomposes uniquely as φ = φ_K + φ_sym, where φ_K factors through K (coupling-structural) and φ_sym factors through the elementary symmetric polynomials e₁, e₂, e₃ (value-symmetric). There is no third category.

**Corollary 3 (Nonlinear Domains).** For couplings with κ > 0 at generic operating points, K is a complete invariant — every T-invariant function factors through K.

---

## Significance

This is the framework's completeness result. It proves the diagnostic basis is exhaustive: there is no coupling information that K misses. For aerospace certification (DO-178C Level A), this supports the argument that the invariant basis is provably complete.

The theorem is upstream of all other results. The decomposition (Theorems 1–3), the hierarchy, the essential dimension work — all produce coupling-structural invariants that factor through K.

## Verification Record

- Self-contained proof in `theorem_8_1.pdf`
- Proof structure: dichotomy between coupling data and role-labelled values
- Scope section confirms extensibility to higher-order derivative augmentations
- No subsequent development has required revision (assessed 15 April 2026)

## Interaction with Later Results

- The decomposition components (κ_c, κ_s, κ_int) are coupling-structural but NOT T-invariant — they carry role-specific information below the level 8.1 addresses
- The hierarchy theorem adds concrete structured examples of coupling-structural invariants (one per floor) that 8.1 governs
- Natural extension to S_n for n-variable systems uses the same proof structure

---

## ⚠ MANUAL PLACEMENT REQUIRED

Place `theorem_8_1.pdf` in this directory.
