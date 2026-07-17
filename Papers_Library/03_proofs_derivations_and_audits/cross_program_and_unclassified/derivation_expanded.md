# Status Note — Refined Residual Definitions for Lifted Joint F

## Refinement Performed
We implemented four different ways of computing the sum-of-squares portion of `F_joint = Σ F_i² - X²`:

- `naive`: standard left-to-right accumulation (`s += v*v`)
- `fsum`: `math.fsum` on the list of squares
- `pairwise`: simple tree/pairwise reduction
- `reversed`: right-to-left accumulation

For each strategy we computed `j = (sum_of_squares_strategy - X*X) / ulp(X*X)` on log-dense sampling near the critical point (small X).

## Result
All four strategies produced **statistically indistinguishable** results on both Morris-Thorne and Schwarzschild photon sphere:

- j_variance ≈ 1.78 × 10³⁰
- fraction of points within 0.1 of the discrete lattice {-1, -0.5, 0, 0.5, 1} ≈ 6.7 × 10^{-5}

This is dramatically worse than the classical Schwarzschild result (j_variance ≈ 0.50, 100% near lattice).

## Interpretation
Varying only the final accumulation order of the already-squared terms has negligible effect compared to the overall error in this regime.

The dominant source of the residual when evaluating these lifted joint constraints near their critical points is **not** the way the sum is accumulated. It is more likely located in:

- The evaluation of the individual constraint functions F_i themselves
- The subtraction F_joint + X² when |F_joint| and |X²| are both large before cancellation
- The overall conditioning of the problem at the lifted point

## Conclusion from This Refinement
The simple "different groupings of the sum-of-squares" refinement does **not** recover the clean j-lattice structure for these lifted fixtures.

Further progress would require defining the two "forms" at an earlier stage (before or during the computation of the individual F_i), or using a completely different residual construction that better isolates common-mode rounding in the lifted setting.

This is a calibrated negative result on one plausible refinement path. The classical four-form battery (especially Schwarzschild) remains the clearest environment in which this particular j-lattice phenomenon has been observed so far.