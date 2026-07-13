# LEAD-7 — pole-order check of the candidate DBP metrics (Kerr n=2)

**Date:** 2026-07-07. Method: Gaussian curvature `R[g]` via the Brioschi formula with
exact-lambdified channel partials (up to 3rd order) assembled numerically (mpmath,
dps=50); pole order = `−slope(log|R| vs log ε)` approaching each boundary
(ε=1e-2…1e-5). Davies point `σ=6√(3+2√3), J=6`. EMPIRICAL (numeric orders).

## Result

| candidate | extremal (σ→J) | Schwarzschild (J→0) | R(Davies) | vs paper (3 / 4) |
|---|---|---|---|---|
| **A** paper diagonal `g^DBP=diag(−1/κ_c^D,−1/κ_c^S)` | **3.0** | **4.0** | −2.8e−5 (finite) | **MATCHES** |
| **B** carrier-pullback `(dO_c)ᵀ(dO_c)` | ~7.8 | R→0 (no pole) | ~1e−43 (≈0) | FAILS |
| **C** three-channel pullback `Σ(dκ_c²+dκ_s²)` | ~7.9 | ~4.2 | 0 (finite) | FAILS (extremal) |

## Reading

- **Method validated:** Candidate A reproduces the paper's Result-6 order law to clean
  integers (extremal 3, Schwarzschild 4, finite on Davies). So the Brioschi + pole-fit
  machinery is correct, and 3/4 is the established n=2 target.
- **Candidate B (the carrier-pullback — my earlier "better" recommendation) FAILS the
  pole-order diagnostic.** Its curvature diverges order ~8 on extremal (not 3) and does
  **not** diverge on Schwarzschild (R→0), so it is **not even complementary**. The
  earlier probe (`LEAD7_pullback_probe.md`) showed the *metric* diverges on both
  boundaries — but that is necessary, not sufficient: the *curvature* is the
  complementarity diagnostic, and B's curvature is wrong. **Recommendation retracted.**
- **Candidate C (three-channel pullback) is complementary** (both boundaries diverge,
  Davies finite) but with the **wrong extremal order** (~8 vs 3). A genuinely different
  geometry, not the paper's DBP metric.

## Lesson (banked)

Metric-divergence-on-boundary is a weaker check than curvature-pole-order. I promoted
Candidate B on the weaker check; the pole-order test (Will's call) refuted it. Standing
guard for LEAD-7: **a candidate metric is judged by R[g]'s pole orders (3/4 on Kerr),
not by whether the metric components blow up.**

## Consequence for LEAD-7

The paper's "cheap" diagonal `g^DBP` is the one that carries the canonical n=2 order law;
the pullback shortcut does not reproduce it, so it does **not** dissolve the n=3
generalization problem. Options going forward:
1. **Generalize the diagonal construction to n=3 directly** (the original LEADS plan):
   the difficulty is genuine (several off-diagonal couplings per chart) — enumerate the
   S₃-equivariant ways to assemble `h_3` from the channels and screen by the 6
   constraints + the D3 pole-order law.
2. **A different canonical metric** whose curvature (not just metric) reproduces 3/4 and
   generalizes — the pullback failed; the anisotropy-Hessian `Hess(A_c)` and a
   curvature-matching construction remain untested.
3. Keep C on the bench: its complementarity (with different orders) may itself be a
   result worth characterizing, but it is not "the" DBP metric.

Next: refine B/C's extremal order to a clean value (is it exactly 8?) at higher
precision, and test option-2 candidates before committing Stage A to the diagonal
enumeration.
