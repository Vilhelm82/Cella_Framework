# Derivation Note — ULP-Normalized F1–F2 Residual Lattice Geometry (Log-Dense Sterbenz Probe)

## Algebraic Foundation (unchanged from prior work)
F1 − F2 = (1 − x_term) − f_direct   (exact in reals; R^p cancels completely).

Any common rounding error e in the shared root R therefore appears in both F1 and F2 with the same leading-order effect. Subtraction cancels the common-mode component.

## Why ULP Normalization Matters
Absolute residuals (e.g. 5.55e-17) are binade-dependent. Normalizing by the local ulp(reference_operand) converts the residual into a dimensionless integer rank j:

    j = (F1 − F2 − closed) / ulp(f_direct)

If common-mode rejection of root round-off is complete, the remaining j should be dominated by deterministic lattice effects (integer or half-integer multiples arising from the different assembly paths of F1 vs F2).

## What This Run Measured (30,001 log-dense points at Sterbenz boundary)
- Schwarzschild: j_variance ≈ 0.501, 100% of points within 0.1 of the discrete set {-1, -0.5, 0, 0.5, 1}. Extremely strong quantization signal.
- sr / pure_algebraic / cbrt: j_variance 0.084–0.136, ~40% near the discrete lattice. Partial quantization.
- Negative control (F1−F4): dramatically higher variance on Schwarzschild (~9e7), confirming operand difference destroys the clean structure.

## Interpretation
The result on Schwarzschild is striking: after aggressive log-dense sampling right at the boundary, the normalized residual locks almost perfectly to a small integer/half-integer lattice.

The weaker signal on the other three fixtures suggests either:
- Fixture-specific geometry in how the split vs direct paths interact with rounding, or
- The current log window still mixes regimes of varying cancellation strength.

## Limitations (why PARTIAL)
- Only one density (30k) and one centering of the log window were used.
- No per-point tracking of which discrete value j lands on (full histogram not emitted in this pass).
- ULP reference was f_direct; alternative references (e.g. magnitude of F itself) were not cross-checked.
- No formal statistical test against the null hypothesis of uniform noise in j.

These limitations are explicitly recorded in the `not_established` section of result.json.

## Retrodiction
Two-layer gate (Retest C + prior absolute-residual dense task) passed cleanly before any new measurements were accepted.

All work performed strictly inside `scratch/f1_f2_common_mode_ulp_lattice_geometry/`. No substrate or normative documents touched.