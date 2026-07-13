# CWRU Empirical Validation of Decomposition

**Status:** DEMONSTRATED — Tier 1
**Type:** Empirical result (first real-data confirmation)
**Source:** Validation Report, CWRU decomposition section (8 April 2026)
**Dependencies:** Theorems 1–3 (decomposition), Theorem 4 (gradient irreducibility)

---

## Key Findings

### D-9: Normal Bearing Operation is 100% Coupling-Dominated

- κ_c/K_G = 1.000 for healthy operation
- κ_s = −0.0002 (negligible)
- All constraint surface geometry arises from inter-channel coupling, not individual-channel nonlinearity

### Fault Introduction Creates Self-Curvature

- Inner race fault: κ_s increases by 250× (from −0.0002 to −0.048)
- Coupling ratio drops from 1.000 to 0.882
- The fault creates individual-channel nonlinearity that didn't previously exist

### D-10: Reference-Gradient Normalisation

| Metric | Without ref-gradient | With ref-gradient | Improvement |
|--------|:---:|:---:|:---:|
| K_G KS statistic | 0.231 | 0.410 | +78% |
| κ_c KS statistic | 0.250 | 0.451 | +80% |
| Ratio KS statistic | 0.574 | 0.574 | unchanged (invariant) |

The coupling ratio is gradient-scaling invariant by construction — confirmed empirically (0.574 with and without normalisation). This validates the theoretical prediction in companion paper Section 10.2.

## Significance

This is the bridge between the pure mathematics and the industrial application. The decomposition does exactly what the paper claims:

1. Healthy system: pure coupling (κ_s ≈ 0)
2. Fault introduced: self-curvature appears where none existed
3. Reference-gradient normalisation improves detection by ~80%
4. Coupling ratio is robust (gradient-invariant)

## Dataset

CWRU Bearing Fault Dataset (Case Western Reserve University). Standard benchmark for bearing fault detection. Triplets fitted from vibration sensor data.

## Candidate for Paper v4

These results should appear in the companion paper Section 10 (Diagnostic Implications), which is currently theoretical-only in v3.
