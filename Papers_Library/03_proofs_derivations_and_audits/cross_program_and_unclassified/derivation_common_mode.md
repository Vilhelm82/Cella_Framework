# Derivation Note — F1–F2 Common-Mode in Sterbenz Region (Dense Probe)

## Algebraic Identity (exact reals)
For all four fixtures the forms are constructed such that:

- F1 = R^p - f_direct
- F2 = R^p - 1 + x_term

Therefore:

F1 - F2 = (R^p - f_direct) - (R^p - 1 + x_term) = (1 - x_term) - f_direct

The R^p term cancels exactly. The result is independent of the shared root value R (and therefore of any rounding error in computing R = root(f_direct)).

## IEEE-754 Common-Mode Argument
When F1 and F2 are evaluated using the *identical* float64 value of R (bit-identical, as verified in Retest C), the rounding error e = fl(root(f_direct)) - exact_root is the same additive perturbation for both forms (to first order).

Subtracting two expressions that each contain the same erroneous R^p therefore cancels the leading error term contributed by root round-off.

The residual after subtracting the algebraic closed form is then expected to be:
- Quantisation / rounding effects from the final subtractions and the (1 - x_term) - f_direct evaluation itself.
- Higher-order effects from the fact that the error is not purely additive after the power (R+e)^p.

## What This Run Measured
An 8001-point dense sampling in a Sterbenz-proximal window (small perturbation parameter) for each fixture showed:

- F1-F2 residuals after closed-form subtraction remained at or below ~1.11e-16.
- Median residual near machine zero.
- First-difference variance extremely low.

Negative control (F1-F4, different root operand) produced larger peak deviations on the same grids (in 3/4 fixtures).

## Limitations of Current Evidence (why PARTIAL)
- The precise "maximum-sawtooth" sub-window was not adaptively located per fixture.
- Only first-difference std used as sawtooth proxy (no proper Lomb-Scargle or FFT periodogram against the expected spatial frequency of root rounding).
- 8001 points is dense but not exhaustive.
- No per-point ULP scaling of the residual relative to local F magnitude was performed in this pass.

These are the explicit items listed in `not_established` in result.json.

## Retrodiction Gate
Cleared 2026-06-01 by `retrodiction_gate.py` reproducing the 2026-05-31 Retest C summary statistics to within floating-point determinism on all four fixtures.

All work performed strictly inside `scratch/f1_f2_common_mode_rejection_sterbenz_dense/`. No substrate or normative docs touched.