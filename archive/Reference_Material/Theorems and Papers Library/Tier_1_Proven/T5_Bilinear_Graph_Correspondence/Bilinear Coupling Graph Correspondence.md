# Theorem 5 — Bilinear Coupling Graph Correspondence (n = 3)

**Status:** PROVEN — Tier 1
**Type:** Theorem
**Source:** Companion paper v3, Section 6
**Dependencies:** Theorems 1–3
**Downstream:** Essential Dimension Conjecture (Theorem 5 is the special case)

---

## Statement

For constraint surfaces where H_s = 0 everywhere (purely bilinear coupling):

(a) K_G = κ_c everywhere on the surface.
(b) κ_c = 0 at generic points iff the coupling polynomial factors.
(c) Factorability is equivalent to the coupling graph having open topology.

Therefore: K_G = 0 iff the coupling graph is open. Graph closure is necessary and sufficient for nonzero Gaussian curvature in bilinear systems.

## Mechanism

Factorability → generalised cylinder → developable → K_G = 0.

## Empirical Demonstration

The progression from the additive surface (no edges, K_G = 0) through the open chain x₁x₂ + x₂x₃ (two edges, K_G = 0) to the closed triangle x₁x₂ + x₂x₃ + x₃x₁ (three edges, K_G = 1/12) and the multiplicative coupling x₁x₂x₃ (K_G = 1/3). Curvature emerges precisely at graph closure.

## Scope Limitations

- Restricted to bilinear coupling (no higher-degree terms)
- Restricted to n = 3 variables
- At higher polynomial degree, factorability ≠ essential dim < n (see Essential Dimension Conjecture)
- At n > 3, graph topology inverts: the 4-ring has 4 edges but K = 0; the disconnected pair x₁x₂ + x₃x₄ has 2 edges but K ≠ 0

## Relationship to Essential Dimension

Theorem 5 is the special case of the Essential Dimension Conjecture restricted to bilinear forms in three variables, where factorability and essential dimension coincide. See `Tier_2_Derived/Essential_Dimension_Conjecture/`.
