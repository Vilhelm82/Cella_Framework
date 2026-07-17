# Dual Confinement

**Status:** HYPOTHESIS (reframed per N-Variable Engine Handoff) — Tier 2
**Type:** Hypothesis with partial empirical support
**Source:** Session handoff 10 April 2026, Section 3.3
**Reframing:** N-Variable Engine Handoff (11 April 2026), Section 4.3

---

## Statement (as hypothesis)

**Self-confinement:** If rank(H_s) = r_s, then e_k(Ŝ_s) = 0 identically for all k > r_s.

**Coupling-confinement:** If rank(H_c) = r_c, then e_k(Ŝ_c) = 0 identically for all k > r_c.

**Selection rule:** Interaction term (p, q) on Floor k = p+q survives iff rank(H_c) ≥ p AND rank(H_s) ≥ q.

## Evidence

- Self-confinement: empirically verified during Phase 0 on 2 surfaces (rank-0 and rank-1 H_s both gave κ_s = 0 exactly)
- Coupling-confinement: **untestable at n = 3** because rank(H_c) ≥ 2 always (rank lemma). First testable at n = 4.
- No formal proof has been produced

## ⚠ N-Variable Handoff Correction

The N-Variable Engine Handoff (11 April 2026) explicitly flags this as:

> "Dual Confinement Theorem — unproven conjecture. The claim that self-curvature is 'confined to lower floors' when H_s has low rank is stated as a theorem with expected test outputs, but no proof is provided. Reframe as a hypothesis to be tested."

## What to Do Next

1. Run the pre-registered test case: F = wx + yz + w² − 3 at (1,1,1,1) — requires n-variable engine
2. If hypothesis holds, pursue a formal proof from the properties of elementary symmetric polynomials of matrices with constrained rank
3. If it doesn't, document the counterexample
