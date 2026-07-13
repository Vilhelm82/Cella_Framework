# Lloyd Diagnostic Framework — Theorems and Papers Library
## Master Index

**Author:** William Lloyd
**Curator:** Dr. Nora Kessler (validation partner)
**Created:** 15 April 2026
**Last updated:** 15 April 2026

---

## Purpose

This repository is the definitive inventory of every theoretical result, empirical finding, and publication-ready document in the Lloyd Diagnostic Framework. Each result is classified by readiness level and cross-referenced to its proof source, verification record, and dependent results.

If you get in front of the right people and they ask you to produce your best work, this is the map of what you have.

---

## Tier Classification

**Tier 1 — PROVEN AND BATTLE-TESTED:** Complete proofs, independent verification by at least two computational systems with no shared context, and (where applicable) empirical validation on real data. Defensible under expert scrutiny.

**Tier 2 — DERIVED, NEEDS TIGHTENING:** Clear derivations and empirical support, but either not yet through a full independent audit cycle, awaiting n-variable engine validation, or flagged for reframing by the N-Variable Engine Handoff (11 April 2026).

**Tier 3 — HYPOTHESES AND OBSERVATIONS:** Interesting findings needing more evidence or formal derivation. Present as observations if asked, not as results.

---

## Tier 1 — Proven and Battle-Tested

| # | Result | Type | Proof source | Verification | Folder |
|---|--------|------|-------------|--------------|--------|
| 1 | **Theorem 8.1: Invariant Maximality** | Theorem + 2 Corollaries | `theorem_8_1.pdf` | Self-contained proof; Corollary 3 covers all nonlinear domains | `Tier_1_Proven/T8.1_Invariant_Maximality/` |
| 2 | **Theorems 1–3: Curvature Decomposition** | 3 Theorems | Companion paper v3, Sections 3–4 | 9 analytical surfaces + 138 domain adapter surfaces; two independent computational systems, zero discrepancies on 7 derivations | `Tier_1_Proven/T1-3_Curvature_Decomposition/` |
| 3 | **Theorem 4: Gradient Irreducibility** | Theorem | Companion paper v3, Section 4.2 | Both unequal and equal cross-derivative cases covered | `Tier_1_Proven/T4_Gradient_Irreducibility/` |
| 4 | **Theorem 5: Bilinear Graph Correspondence (n=3)** | Theorem | Companion paper v3, Section 6 | Empirical progression: plane → open → closed → multiplicative | `Tier_1_Proven/T5_Bilinear_Graph_Correspondence/` |
| 5 | **D-6: κ_int = 0 for all explicit surfaces** | Theorem (structural) | Hessian structure of Monge patches | Verified on all 138 decomposition suite surfaces and all time-series computations | `Tier_1_Proven/D6_Interaction_Vanishing_Explicit_Surfaces/` |
| 6 | **Mean Curvature Decomposition (Floor 1)** | Theorem | Audit package + independent Gemini audit | CLEARED WITH CAVEATS; no-interaction claim verified across 6 subtleties; mpmath precision verification | `Tier_1_Proven/Floor1_Mean_Curvature_Decomposition/` |
| 7 | **rank(H_c) ≥ 2 Lemma** | Lemma | Proof by contradiction | Structurally important: coupling-confinement untestable at n=3 | `Tier_1_Proven/Rank_Hc_Lemma/` |
| 8 | **Decomposition Symmetry Profile** | Empirical characterisation (D-13, D-14) | Validation Report Test 1.2b | Translation/scaling/rotation fully characterised; OE-5 confirmed | `Tier_1_Proven/Decomposition_Symmetry_Profile/` |
| 9 | **CWRU Empirical Validation** | Empirical result | Validation Report, 8 April 2026 | First real-data confirmation of decomposition diagnostic separation | `Tier_1_Proven/CWRU_Empirical_Validation/` |

## Tier 2 — Derived, Needs Tightening

| # | Result | Type | Status | Blocker | Folder |
|---|--------|------|--------|---------|--------|
| 10 | **Symmetric Polynomial Hierarchy** | Theorem (in waiting) | Derived; Floor 1 and Floor 2 independently verified | n-variable engine needed for Floor 3+ validation | `Tier_2_Derived/Symmetric_Polynomial_Hierarchy/` |
| 11 | **Dual Confinement** | Hypothesis (reframed) | Self-confinement verified on 2 surfaces; coupling-confinement untestable at n=3 | Needs formal proof; n-variable handoff flags as unproven | `Tier_2_Derived/Dual_Confinement/` |
| 12 | **Monge Prohibition** | Partial theorem | κ_int = 0 part is PROVEN (D-6). Sign constraint on κ_c follows from Monge formula, not AF. | Drop AF attribution; reframe sign constraint as corollary | `Tier_2_Derived/Monge_Prohibition/` |
| 13 | **Two Lights Computation** | Proposed method | Mathematically justified; infrastructure exists in lloyd_core.py | Implementation and testing not completed | `Tier_2_Derived/Two_Lights_Computation/` |
| 14 | **Essential Dimension Conjecture** | Partial theorem + conjecture | "If" direction effectively proven; "only if" falsified by cone (D-12) | Needs restating with ruled/developable exclusion | `Tier_2_Derived/Essential_Dimension_Conjecture/` |

## Tier 3 — Hypotheses and Observations

| # | Result | Type | Evidence | Folder |
|---|--------|------|----------|--------|
| 15 | **Gradient Focusing Classification** | Diagnostic hypothesis | Van der Waals critical point; cone tip progression | `Tier_3_Hypotheses/Gradient_Focusing_Classification/` |
| 16 | **Alexandrov-Fenchel Engagement** | Observed pattern | Exact saturation on isotropic surface; correctly predicted disengagement on VdW | `Tier_3_Hypotheses/Alexandrov_Fenchel_Engagement/` |
| 17 | **Essential Dim Collapse at AF Saturation** | Observation (single surface) | Isotropic surface: K_G=0, factorisation, dim drop 3→1 at a=2 | `Tier_3_Hypotheses/Essential_Dimension_Collapse_AF/` |
| 18 | **GR Applications** | Results from earlier work | Schwarzschild κ_c/κ_s=12/5; ISCO cancellation; Λ as Class 1 passenger | `Tier_3_Hypotheses/GR_Applications/` |

---

## Dependency Graph

```
Theorem 8.1 (Invariant Maximality)
  └── Governs ALL coupling-structural invariants
      ├── Theorems 1–3 (K_G Decomposition = Floor 2)
      │   ├── Theorem 4 (Gradient Irreducibility)
      │   ├── Theorem 5 (Bilinear Graph Correspondence)
      │   │   └── Essential Dimension Conjecture (generalises T5)
      │   │       └── Cone Counterexample D-12 (qualifies conjecture)
      │   ├── D-6 (κ_int = 0 on explicit surfaces)
      │   │   ├── Monge Prohibition (corollary of D-6 + Monge formula)
      │   │   └── Two Lights Method (enabled by D-6)
      │   ├── Decomposition Symmetry Profile (D-13, D-14)
      │   └── CWRU Empirical Validation (confirms diagnostic separation)
      ├── Floor 1 Mean Curvature Decomposition
      │   └── No interaction term (load-bearing, audited)
      └── Symmetric Polynomial Hierarchy (unifies Floors 1, 2, ..., n-1)
          ├── Dual Confinement (rank-based selection rule)
          │   └── rank(H_c) ≥ 2 Lemma (structural constraint)
          └── AF Engagement (observed pattern on hierarchy)
              └── Essential Dim Collapse at AF Saturation (single observation)
```

---

## Patent Coverage

| Patent | Filing date | PCT deadline | Coverage |
|--------|-----------|-------------|----------|
| AU 2026902758 | 28 March 2026 | 28 March 2027 | Core K_G diagnostic on constraint surfaces |
| AU 2026902926 | 1 April 2026 | 1 April 2027 | Coupling curvature decomposition |
| AU 2026903116 | 4 April 2026 | 4 April 2027 | Photonic computing mesh fault localization |
| Fourth provisional (draft) | Not yet filed | — | N-variable extension, hierarchy, essential dimension |

---

## Files Requiring Manual Placement

The following files are referenced but not held in this repository. William must place them manually:

1. `Tier_1_Proven/T8.1_Invariant_Maximality/theorem_8_1.pdf` — standalone proof document
2. `Tier_1_Proven/Floor1_Mean_Curvature_Decomposition/Audit_Report_Mean_Curvature_Decomposition.md` — Gemini audit verdict
3. `Tier_1_Proven/Floor1_Mean_Curvature_Decomposition/Audit_Package_MeanCurvatureDecomposition.md` — audit submission package
4. `Supporting_Documents/hierarchy_report.docx` — comprehensive hierarchy theorem report
5. `Supporting_Documents/Hierarchy_Validation_Programme.md` — HVP v1.0
6. `Supporting_Documents/Phase0_Audit_Findings.md` — Workbench audit results
7. `Patents/fourth_provisional_patent_v2.md` — fourth patent draft (from project knowledge)

---

## Presentation Order (The Pitch)

If presenting to a technical audience with limited time:

1. **Lead:** Theorem 8.1 — coupling kernel as provably complete diagnostic basis
2. **Core:** Theorems 1–4 — decomposition with uniqueness and irreducibility
3. **Bridge:** CWRU empirical result — "100% coupling baseline, fault introduces self-curvature"
4. **Depth:** Theorem 5 → Essential dimension story (with honest cone boundary)
5. **Forward:** Hierarchy as structural preview (Floor 1 audited, general case derived)
6. **Reserve:** GR applications, AF engagement, gradient focusing — if conversation goes deep

---

*"The goal is not to prove the framework works. The goal is to document exactly where it works, exactly where it doesn't, and exactly where you're not sure yet. That's what makes it science."*
— N. Kessler, April 2026
