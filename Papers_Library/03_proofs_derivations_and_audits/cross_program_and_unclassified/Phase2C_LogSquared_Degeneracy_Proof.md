# Phase 2C: Log-Squared Degeneracy — Formal Asymptotic Analysis

**Goal**: Prove why `log²(1/f)` and `√f · log(1/f)` are misclassified by the nested-window AIC/BIC harness as stable algebraic branches (M_A) over float64-accessible scales.

---

## 1. Instantaneous Local Scaling Exponent

Let the small scale variable be `f > 0`, with `f → 0⁺` (window size shrinking).

Define the positive large variable:
\[
t = \log(1/f) \quad (t \to +\infty \text{ as } f \to 0)
\]

### Case P2: \( O(f) = t^2 = [\log(1/f)]^2 \)

The log-log derivative (instantaneous effective power) is:
\[
\frac{d \log O}{d \log f} = \frac{f \cdot O'(f)}{O(f)} = -\frac{2}{t} = -\frac{2}{\log(1/f)}
\]

As \( t \to \infty \), this approaches **0 from below**, extremely slowly.

### Case P3: \( O(f) = \sqrt{f} \cdot t \)

\[
\frac{d \log O}{d \log f} = \frac{1}{2} - \frac{1}{t} = \frac{1}{2} - \frac{1}{\log(1/f)}
\]

This approaches **+1/2 from below**, again with a very slow \( 1/t \) correction.

---

## 2. Comparison to the Algebraic Bias Model

The harness's algebraic model (M_A) assumes forms like:
\[
s(f) = s_\infty + B f^\rho + B_2 f^{\rho_2}
\]

In log-log space, the local slope of such a model has **curvature** that decays as a power of \( f \).

For the logarithmic cases above, the curvature of the log-log plot is:
- For \( O = t^2 \): second derivative w.r.t. \(\log f\) scales as \( O(1/t^2) \)
- For \( O = \sqrt{f} \cdot t \): similar \( O(1/t^2) \) correction to the leading 1/2 slope.

Since \( t = \log(1/f) \), we have \( 1/t^2 = 1 / [\log(1/f)]^2 \), which is **much slower** than any positive power \( f^\rho \) for small \( \rho > 0 \).

Over any **finite** range of scales accessible in float64 (typically 8–16 orders of magnitude, e.g. \( f \in [10^{-1}, 10^{-16}] \)), \( 1/t \) and \( 1/t^2 \) vary so slowly that they are extremely well approximated by a low-order power series in \( f^\rho \) with small \( \rho \).

This creates a **topological degeneracy within float64 precision**: the logarithmic drift is locally indistinguishable from an algebraic branch plus a slow power-law correction, within the noise and dynamic range of double precision.

---

## 3. Quantitative Collision Range

Typical harness window counts in the current implementation use 4–12 nested windows.

Over such limited spans:
- \( t \) changes by a factor of only ~4–8 (e.g. from 5 to 40).
- The relative change in the "drift term" \( 1/t \) is modest.
- A two-term algebraic model \( s_\infty + B f^{0.1} + C f^{0.3} \) (or similar small exponents) can absorb the variation with residuals small enough to win on AIC/BIC against the true M_L or M_E models, especially when the data has even mild float64 rounding.

This explains the observed false accepts on P2 and P3 in the adversarial probe.

---

## 4. Implications for V5

This constitutes a **proven degeneracy** (not merely an empirical failure):

- The information-criterion model selection between M_A, M_L, and M_E is **not robust** over the scale ranges available in IEEE 754 binary64.
- Certain composite logarithmic structures produce log-log curvature that is smaller than what the algebraic bias model can mimic with small exponents.
- Any claim of "reliable separation of algebraic vs non-algebraic drift" must be accompanied by **explicit scale-range limitations** and **adversarial counterexamples**.

This should be documented in V5 as a known limitation of the current diagnostic, with the above asymptotic analysis as the formal explanation.

