# Coupling-Native Computation of Gaussian Curvature: Hypothesis and Investigation Plan

**Author:** William Lloyd
**Date:** 7 April 2026
**Status:** Hypothesis — pre-investigation
**Governing patents:** AU 2026902758, AU 2026902926, AU 2026903116
**Prerequisite:** Lloyd Framework validation Stage 1 (Tests 1.1–1.3, PASS)

---

## 1. Motivation

The Lloyd Framework diagnoses coupling degradation by computing the Gaussian curvature K_G of the constraint surface F(D, S, P) = 0. The current computation uses the bordered Hessian formula:

    K_G = −det(H_b) / |∇F|⁴

where H_b is the 4×4 bordered Hessian matrix. This formula is a general-purpose tool from classical differential geometry. It computes intrinsic curvature of any smooth implicit surface. It is mathematically correct and has been validated to <0.1% accuracy across six surface families (Validation Report, Stage 1).

However, the bordered Hessian formula is *domain-agnostic*. It treats F(x, y, z) = 0 as an abstract surface in three-space. It does not distinguish between curvature arising from inter-variable coupling (the diagnostic signal the framework seeks) and curvature arising from individual-variable nonlinearity (which conventional single-channel diagnostics already detect). The formula collapses both sources into a single scalar.

Validation results from Test 1.2 (MR-6 Interaction Curvature and Whole Fish Addendum) provide empirical evidence that these sources are structurally separable. The coupling graph progression demonstrates that K_G responds specifically to the *topology* of inter-variable coupling: open coupling graphs produce K_G = 0, closed graphs produce K_G ≠ 0, with magnitude increasing as coupling complexity grows.

This document proposes that a framework-native decomposition of K_G into coupling, self, and mixed components would: (a) provide richer diagnostic information than scalar K_G alone, (b) enable a more robust time-series computation path, and (c) connect the Lloyd Framework's empirical coupling diagnostic to a novel theoretical structure grounded in Theorem 8.1 and the centrifuge permutation group.

---

## 2. Definitions

### 2.1 Hessian Decomposition

For any twice-differentiable constraint equation F(x₁, x₂, x₃) = 0, the 3×3 Hessian matrix H_F admits a unique additive decomposition:

    H_F = H_self + H_cross

where:

    H_self = diag(F_{x₁x₁}, F_{x₂x₂}, F_{x₃x₃})

contains the diagonal (self-coupling) entries, and:

    H_cross = H_F − H_self

contains the off-diagonal (inter-variable coupling) entries F_{x_ix_j} for i ≠ j.

**Notation.** F_{x_ix_j} denotes ∂²F/∂x_i∂x_j. We write g_i = ∂F/∂x_i for the gradient components, and g = (g₁, g₂, g₃) for the gradient vector.

### 2.2 Bordered Hessian Determinant Expansion

The bordered Hessian is the 4×4 matrix:

    H_b = | 0    g₁   g₂   g₃  |
          | g₁   H₁₁  H₁₂  H₁₃ |
          | g₂   H₂₁  H₂₂  H₂₃ |
          | g₃   H₃₁  H₃₂  H₃₃ |

where H_{ij} = F_{x_ix_j}. Its determinant expands as a polynomial in the H_{ij} and g_i. Each monomial term in this expansion contains specific products of Hessian entries. We classify every term by its *coupling content*:

**Definition (Coupling content of a monomial).** A monomial term in det(H_b) has coupling content (p, q) where p is the number of cross-derivative factors (H_{ij} with i ≠ j) and q is the number of self-derivative factors (H_{ii}) appearing in the product.

**Definition (Term classes).**

- **Pure coupling terms:** (p ≥ 1, q = 0). Products containing only cross-derivatives and gradient components. No self-derivative factors.
- **Pure self terms:** (p = 0, q ≥ 1). Products containing only self-derivatives and gradient components. No cross-derivative factors.
- **Mixed terms:** (p ≥ 1, q ≥ 1). Products containing at least one of each.
- **Gradient-only terms:** (p = 0, q = 0). Products of gradient components alone. (These vanish identically in the bordered Hessian expansion.)

### 2.3 Proposed Decomposition

**Definition (Curvature decomposition).**

    det(H_b) = Δ_coupling + Δ_self + Δ_mixed

where Δ_coupling is the sum of all pure coupling terms, Δ_self is the sum of all pure self terms, and Δ_mixed is the sum of all mixed terms. This induces:

    K_G = K_coupling + K_self + K_mixed

where:

    K_coupling = −Δ_coupling / |∇F|⁴
    K_self     = −Δ_self / |∇F|⁴
    K_mixed    = −Δ_mixed / |∇F|⁴

Since the decomposition of det(H_b) is additive and exhaustive, the identity K_G = K_coupling + K_self + K_mixed holds exactly by construction. This is not an approximation.

---

## 3. Hypotheses

### Hypothesis 1 — Whole Fish Correspondence

**Statement:** For constraint equations where all coupling enters through bilinear terms (i.e., H_self = 0 everywhere), K_G = K_coupling exactly, and:

    K_coupling = 0  if and only if  the coupling polynomial factors
    K_coupling ≠ 0  if and only if  the coupling graph is closed

**Falsification criterion:** Find a bilinear constraint surface where K_G ≠ 0 but the coupling graph is open. Alternatively, find a bilinear surface where K_G = 0 but the coupling polynomial does not factor.

**Empirical basis:** The Whole Fish progression (Validation Report, Test 1.2 Addendum A):

| Equation | H_self | Coupling graph | K_G |
|---|---|---|---|
| x + y + z − 3 | 0 | No edges | 0 |
| xy + yz − 2 | 0 | Open chain | 0 |
| xy + yz + zx − 3 | 0 | Closed triangle | 1/12 |
| xyz − 1 | 0 at (1,1,1) | Three-way vertex | 1/3 |

**Predicted mechanism:** Factorability of the bilinear form → surface is a generalised cylinder → developable → K_G = 0. Non-factorability → closed coupling graph → non-developable → K_G ≠ 0. The pure coupling terms in Δ_coupling carry the entire curvature signal for this class.

### Hypothesis 2 — Diagnostic Separability

**Statement:** K_coupling, K_self, and K_mixed carry distinct diagnostic information. Specifically:

(a) K_coupling detects faults that change the inter-variable coupling structure (the "coupling-only" detections that are invisible to single-channel monitoring).

(b) K_self detects faults that change the nonlinearity of individual variables without altering the coupling (e.g., sensor saturation, individual component degradation).

(c) K_mixed detects faults where individual nonlinearity and inter-variable coupling interact (e.g., a nonlinear component operating in a regime where its nonlinearity affects the coupling path).

(d) Conventional single-channel diagnostics detect faults in categories (b) and (c) but are blind to category (a). The scalar K_G detects all three but does not distinguish between them.

**Falsification criterion:** Find a coupling-only fault (no individual channel shift) where K_coupling = 0 and K_self ≠ 0. This would demonstrate that the decomposition assigns the diagnostic signal to the wrong component. Alternatively, find a self-only fault where K_coupling ≠ 0.

**Test protocol:** Using benchmark fault data (CWRU bearing, ASHRAE RP-1043), inject controlled perturbations in three categories: (i) coupling-only (modify cross-terms), (ii) self-only (modify diagonal terms), (iii) mixed. Score K_coupling, K_self, K_mixed responses against fault category. If K_coupling responds primarily to coupling-only faults and K_self responds primarily to self-only faults, the decomposition is diagnostically meaningful.

### Hypothesis 3 — Cross-Derivative Sufficiency for Time-Series

**Statement:** For systems where coupling-only detection is the target diagnostic (i.e., faults invisible to single-channel methods), the cross-derivative terms alone suffice to compute K_coupling. This requires estimation of only three quantities from sensor data — F_{x₁x₂}, F_{x₂x₃}, F_{x₁x₃} — plus the gradient, rather than a full surface fit.

**Implication for the time-series engine:** The computation path simplifies from:

    Data → fit surface → compute all 9 second derivatives → bordered Hessian → K_G

to:

    Data → estimate 3 cross-channel sensitivities → K_coupling directly

The cross-channel sensitivities F_{x_ix_j} (i ≠ j) can be estimated from windowed local regression of each variable against the other two, which is numerically more stable than fitting a global implicit surface and differentiating it twice.

**Falsification criterion:** Demonstrate a case where the shortened path produces a qualitatively different diagnostic conclusion (detection vs non-detection) compared to the full bordered Hessian K_G, for a coupling-only fault. If K_coupling from the shortened path misses a coupling fault that scalar K_G catches, the cross-derivative path is insufficient.

**Robustness prediction:** K_coupling avoids the |∇F|⁴ amplification of Finding 3 in the denominator when it can be normalised differently (e.g., by |∇F|² or by cross-term magnitude). This prediction must be verified numerically.

### Hypothesis 4 — Centrifuge Invariants as Coupling Curvature

**Statement:** The six K_G values produced by the centrifuge (one per S₃ permutation of variable roles) contain structural information about the coupling geometry that is not captured by any single K_G evaluation. Specifically, the symmetric functions of the centrifuge output set — or equivalently, the character of the S₃ representation induced by the centrifuge action (Theorem 8.1) — define coupling invariants that characterise the surface geometry independently of the bordered Hessian.

**Sub-hypotheses:**

(4a) **Centrifuge spectrum.** The set {K_G^(π) : π ∈ S₃} has a characteristic spectrum (pattern of degeneracies, ratios between non-degenerate values) that encodes the coupling class more richly than the single-permutation coupling class label ("Class 1" / "Class 2").

(4b) **Permutation-symmetric invariants.** The elementary symmetric polynomials of the centrifuge outputs — σ₁ = ΣK_G^(π), σ₂ = Σ_{i<j} K_G^(πᵢ)K_G^(πⱼ), σ₃ = ΠK_G^(π) — are intrinsic to the surface and encode geometric information about the coupling that is lost in any single-permutation evaluation.

(4c) **Centrifuge-native curvature.** There exists a function C(σ₁, σ₂, σ₃, ..., σ₆) of the centrifuge invariants that recovers K_G at any single permutation as a special case but provides additional discriminatory power between coupling topologies. This function C would be a framework-native geometric invariant — derived from the Lloyd Framework's own structure (Theorem 8.1, S₃ group action) rather than from classical differential geometry.

**Falsification criterion:** If the centrifuge outputs for two geometrically distinct surfaces (distinct K_G profiles, distinct coupling topologies) produce identical symmetric polynomials (σ₁, σ₂, ..., σ₆), then the centrifuge invariants do not carry additional information and Hypothesis 4c is falsified. Additionally, if σ₁ through σ₆ can be expressed purely in terms of the single-point K_G and the coupling class, no new information is present.

**Investigation protocol:** Run the centrifuge on all Stage 1 validation surfaces plus the Whole Fish progression at multiple operating points. Tabulate the full six-element spectrum and compute σ₁ through σ₆. Look for: (i) surfaces with identical scalar K_G but different centrifuge spectra, (ii) a systematic relationship between centrifuge spectrum and coupling graph topology, (iii) invariant combinations that are preserved under the metamorphic relations (translation, rotation, scaling) when individual centrifuge outputs change.

---

## 4. Analytical Investigation Plan

### Phase 1 — Determinant Expansion (Week 1)

Expand det(H_b) symbolically for the general 4×4 bordered Hessian. Classify every monomial term by coupling content (p, q). Express Δ_coupling, Δ_self, and Δ_mixed in closed form as functions of the gradient components g_i and Hessian entries H_{ij}.

**Deliverable:** Explicit formulae for Δ_coupling, Δ_self, Δ_mixed.

**Verification gate:** Δ_coupling + Δ_self + Δ_mixed = det(H_b) at all Stage 1 test points. This is an identity, not an approximation — any discrepancy is a computation error.

### Phase 2 — Whole Fish Validation (Week 1)

Evaluate K_coupling, K_self, K_mixed at all Whole Fish progression surfaces (WF-1 through WF-4) and all Test 1.1 surfaces.

**Predictions to verify:**

| Surface | K_coupling | K_self | K_mixed | K_G (known) |
|---|---|---|---|---|
| x + y + z − 3 (plane) | 0 | 0 | 0 | 0 |
| xy + yz − 2 (open chain) | 0 | 0 | 0 | 0 |
| xy + yz + zx − 3 (closed triangle) | 1/12 | 0 | 0 | 1/12 |
| xyz − 1 (three-way) | ? | 0 at (1,1,1) | ? | 1/3 |
| z − x² − y² (paraboloid) | 0 | ? | 0 | 4/(1+4x²+4y²)² |
| x² + y² + z² − 1 (sphere) | 0 | ? | 0 | 1.0 |
| z − xy (saddle) | ? | 0 | 0 | −1/(1+x²+y²)² |

The "?" entries are predictions to be filled in during Phase 2. Key structural predictions:

- Surfaces with no cross-derivatives (sphere, paraboloid) must have K_coupling = 0 and K_mixed = 0, with all curvature in K_self.
- Surfaces with no self-derivatives (bilinear: saddle, Whole Fish) must have K_self = 0 and K_mixed = 0, with all curvature in K_coupling.
- Surfaces with both (xyz − 1 at generic points) may have nonzero K_mixed.
- If any of these structural predictions fail, the decomposition does not separate coupling from self in the way hypothesised, and either the definitions need revision or the hypothesis is wrong.

**Falsification gate:** If the paraboloid (no cross-derivatives) produces nonzero K_coupling, Hypothesis 2 is falsified.

### Phase 3 — Centrifuge Spectrum Analysis (Week 2)

Run the full centrifuge on each test surface at multiple operating points. Tabulate all six K_G values per surface. Compute σ₁ through σ₆. Investigate:

(a) Whether centrifuge spectra distinguish surfaces that scalar K_G does not.
(b) Whether the symmetric polynomials are invariant under the validated metamorphic relations (MR-1 through MR-3).
(c) Whether a relationship exists between the spectrum and the coupling graph topology identified in the Whole Fish result.

**Deliverable:** Centrifuge spectrum table for all test surfaces. Assessment of whether the spectra carry diagnostic information beyond scalar K_G.

### Phase 4 — Time-Series Cross-Derivative Path (Week 3)

Implement the shortened computation path (Hypothesis 3) using only cross-derivatives and gradient estimates from windowed sensor data. Run on synthetic data generated from known analytical surfaces. Compare K_coupling (shortened path) against K_coupling (bordered Hessian decomposition, Phase 2) on the same data.

**Verification gate:** Agreement within 5% (the time-series acceptance gate from the validation programme).

**Noise robustness comparison:** Add white Gaussian noise at SNR = 20dB to the synthetic data. Compare the coefficient of variation of K_coupling (shortened path) against K_G (bordered Hessian). If the shortened path has lower variance, it is more robust for time-series deployment.

---

## 5. Relationship to Existing Framework Components

### 5.1 Theorem 8.1

Theorem 8.1 establishes that the S₃ group action on the variable triple (D, S, P) induces a well-defined action on the coupling equivalence classes, and that the coupling kernel K factorises under this action. Hypothesis 4 extends this by conjecturing that the centrifuge spectrum — the concrete numerical output of the S₃ action — encodes additional geometric information beyond single-point K_G. If confirmed, this would connect Theorem 8.1's algebraic structure to a novel computational object.

### 5.2 Whole Fish Principle

The Whole Fish principle (empirically: coupling curvature is non-decomposable; the curvature of the whole exceeds the sum of curvatures of the parts) is given a precise mathematical mechanism by Hypothesis 1: graph closure of the coupling topology is necessary and sufficient for nonzero K_coupling in the bilinear case. The decomposition makes the Whole Fish principle computable, not just observable.

### 5.3 Existing Benchmark Results

The framework's benchmark results (5/6 domain wins, 0% false alarms, speed advantage over MFDFA) were obtained using scalar K_G. If Hypothesis 2 holds, the coupling-only detections in those benchmarks should have K_coupling ≫ K_self, providing retroactive evidence that the framework's diagnostic power comes specifically from the coupling component. This would strengthen the commercial value proposition: not just "we detect more faults" but "we detect a *specific class of faults* that are structurally invisible to methods that don't measure coupling geometry."

---

## 6. Scope and Limitations

This investigation is analytical and computational. It does not claim to have derived the formulae or confirmed the hypotheses. All statements in Section 3 are hypotheses with pre-committed falsification criteria. Each hypothesis will be accepted, modified, or rejected based on the investigation results.

The decomposition Δ_coupling + Δ_self + Δ_mixed = det(H_b) is an algebraic identity and requires no validation. The hypotheses concern whether this identity is *diagnostically meaningful* — whether the components carry distinct physical information that the scalar sum obscures.

Hypothesis 4 (centrifuge invariants) is the most speculative. It may be that the six centrifuge outputs contain no information beyond what scalar K_G plus coupling class already encode. If so, Hypothesis 4 is falsified cleanly, and the result is documented as a negative finding of scientific value.

Nothing in this investigation modifies the validated bordered Hessian computation. The decomposition is an additional layer of analysis on top of the existing framework, not a replacement. The bordered Hessian K_G remains the ground truth for all validation purposes.

---

## 7. Success Criteria

| Outcome | Implication | Next step |
|---|---|---|
| Hypotheses 1 and 2 confirmed | K_G decomposition is diagnostically meaningful. Coupling curvature can be separated from self-curvature. | Implement decomposition in Workbench. Add K_coupling, K_self, K_mixed to diagnostic output. Rerun Stage 4 benchmarks with decomposed metrics. |
| Hypothesis 3 confirmed | Time-series engine has a more robust computation path for coupling-only detection. | Implement cross-derivative path as primary time-series computation. Use full bordered Hessian as cross-check. |
| Hypothesis 4 confirmed | Centrifuge invariants define a framework-native geometric object. | Separate paper: "Coupling Curvature from Permutation Group Structure." Connects Theorem 8.1 to novel computation. |
| Hypothesis 1 or 2 falsified | Decomposition does not separate coupling from self as hypothesised. The bordered Hessian's "mixing" may be intrinsic to the geometry. | Document as a negative result. Investigate whether a different decomposition (e.g., based on tangent-plane projection) achieves separation. |
| Hypothesis 4 falsified | Centrifuge spectrum contains no information beyond scalar K_G + class. | Document as a boundary finding. The centrifuge's value is in the degeneracy pattern, not in the numerical spectrum. |

---

*"The bordered Hessian got us here. What the validation revealed is pointing toward something that may not need it."*

— Investigation notes, 7 April 2026
