# The Transfer-Function Exponent Family at Algebraic Branch Points (V5 Manuscript)

*Draft Status: V5 Architecture — FINAL MATHEMATICAL SUBSTRATE LOCKED.*
*(Note: Corrected for F1-only task scope, window-count fragility, and cbrt excursions).*

---

## 1. Introduction & The Mathematical Substrate

The transfer-function exponent framework relies on the precise separation of algebraic structural invariants from floating-point arithmetic conditioning. To achieve this strictly within IEEE 754 binary64 space, the foundational topological invariants of the mapping space must be axiomatically bounded. 

The V5 architecture is built upon two verified substrate facts:
1.  **Binade-Aligned Cancellation Lattice (BACL) Invariant:** For normal floating-point numbers $a, b \in \mathbb{F}^+$ where $\text{ulp}(a) \ge \text{ulp}(b)$, the exact real difference satisfies $a - b = j \cdot \text{ulp}(b)$ for some integer $j \in \mathbb{Z}$. Subtraction within a structured binade hierarchy naturally collapses into an integer-lattice grain.
2.  **The No-Binade-Drop Property (Conjecture C):** A correctly-rounded square root operation applied to a normal float $f$ preserves the binade floor under canonical squaring. (Proven exhaustively for all 1,022 normal-range odd binade boundaries).

---

## 2. The $c_2$ Integer-Lattice Property 

**Observation 3 (Formerly Theorem 3): Cross-Fixture Lattice Alignments**
The lattice grain patterns observed across algebraic fixtures (e.g., the 0.5 grain in transformed-operand fixtures and the 0.25 grain in identity-operand fixtures) are not independent universal mathematical laws. Rather, they are empirical artifacts stemming directly from **The $c_2$ Integer-Lattice Property**. 

Because exact subtraction (via BACL) absorbs localized operation rounding within the normal range, the residual projections naturally align to these specific grid spacings depending on the chosen route. Therefore, the cross-fixture consistency is a symptom of the underlying lattice invariants, not a distinct theorem of universality.

### 2.1 Substrate Derivation of the $c_2$ Lattice Invariants
The $c_2$ integer-lattice theorem states that the reassociated form $c_2 = \text{round}(V_n + (x_{\text{term}} - 1))$ lands exactly on an integer multiple of $\text{ulp}(f)$. The scope is mathematically explicit: it holds for the normal range ($f \ge 2^{-1021}$). For $n=2$, the bound is tight ($|j| \le 1$). For $n=3$, the observed rank expands, demonstrating that universality is structural while rank is route-dependent. 

### 2.2 Higher-Order Roots, Composed Chains, and the Shattering Threshold
The $c_2$ integer-lattice rank expands as a function of the root degree $n$ and the quality of the root implementation. The first-order scaling law predicts that $|j|_{\text{max}} \approx O(n \cdot \epsilon_{\text{root}})$. 

**Empirical Reality Check ($n=4$):** Sandbox multi-precision traces for quartic fixtures reveal a perfectly clean integer lattice (0.25 residual grain, strictly bounded), demonstrating no immediate rank expansion or shattering at $n=4$. This cleanliness is a structural artifact of operation composition: the V4 substrate evaluates quartic roots via composed square roots (`sqrt(sqrt(f))`). Because IEEE 754 guarantees exact rounding for the native `sqrt` operation, the cascading truncation error is tightly minimized, artificially preserving the BACL invariant deeper into the chain.

**The Shattering Limit:** For native, non-composed higher-order root implementations, or as $n$ continues to grow, the cumulative intermediate truncation errors are expected to eventually violate the Conjecture C binade preservation constraint. At this boundary, the lattice rank is projected to undergo a discrete topological shattering into unstructured noise. 

### 2.3 Corollary 1: Top-Down Lattice Pre-Alignment
In finite-precision algebraic chains, delaying catastrophic cancellation preserves the BACL invariant. If a chain contains an exact Sterbenz subtraction that drops the operand into a lower binade, performing it *early* (e.g., $V_n - 1$) misaligns the preserved absolute error from subsequent operations, fracturing the residual lattice. Conversely, reassociating the chain to absorb local rounding in the highest active binade (e.g., $x - 1$) structurally pre-aligns the operands. The final cancellation is therefore governed by BACL, resulting in a strict integer-lattice footprint.

* **Addendum: The Sterbenz Phase Transition (Hypothesis).** Current empirical data suggests the optimal pre-alignment route may undergo a phase transition at the Sterbenz boundary. Inside the Sterbenz region ($V_n \approx 1$), early cancellation appears to trap absolute error, implying "late" reassociation is required to pre-align the global integer lattice. Outside this region, the error mechanics invert, favoring "early" classic subtraction. While this strongly supports the V4 engine's dynamic, runtime typed status calculus for routing, this transition remains a working hypothesis pending a definitive cross-boundary F2 campaign.

---

## 3. The Precision-Scaling Separation Manifold

**Theorem 2: The F1 Instrument Artifact and Open Precision-Scaling Boundaries**
The previously asserted collapse of the precision-scaling diagnostic ($R^2$ departure) on the F1 path is not a substrate boundary, but an instrument artifact. Sandbox multi-precision tracing confirms that the verification oracle (`decimal_50` and `float128`) simply reached its intrinsic noise floor. 

However, this does not establish that the precision-scaling manifold is mathematically continuous across the full normal range. For the SR, Schwarzschild, and Pure Algebraic fixtures, the forward F1 residual scales exactly to zero at these analytical limits—meaning the diagnostic fit degenerates because there is no signal to measure. Furthermore, the critical F2 path—where the open $b_k \neq 0$ Sterbenz-region sub-claim lives—has not yet been fully measured. The exact mathematical boundaries of the separation manifold inside the Sterbenz region therefore remain strictly open.

### 3.1 The Information Loss Function (Backward Navigation)
Independent of the forward evaluation boundaries, the backward navigation graph across the exact subtraction node carries an irreducible width. At input binade index $k$, any attempt to invert the Sterbenz node forces an interval-bounded preimage whose relative uncertainty ($\Delta f / f$) scales exactly by $2^{W(k)}$, where $W(k) = \min(53, -\lfloor \alpha k + \log_2|c| \rfloor)$. This establishes a formal information-theoretic boundary on trace invertibility without asserting uninterrupted continuous geometry for the forward precision-scaling evaluation.

---

## 4. Topological Boundaries and Diagnostic Limits

### 4.1 Subnormal Boundary Transition
**Observation 4: Topological Decoupling at the Subnormal Boundary**
The scaling invariance supporting the precision-scaling manifold is strictly bound to the normal range ($f \ge 2^{-1022}$). When operands cross into the subnormal regime, the mathematical topology changes. Sandbox traces confirm that while the proportional binade scaling collapses (and the log-log separation diagnostic becomes mathematically invalid), the residual structure maps directly onto the uniform subnormal grid ($2^{-1074}$). 

**Theorem 4.1.1: The Subnormal Square-Root Identity**
While proportional scaling collapses, the structural preservation of the input operand for $n=2$ becomes absolute. It is mathematically guaranteed that for all subnormal inputs $f < 2^{-1022}$, the canonical square-root round-trip yields $V_2 \equiv f$ exactly. Because the intermediate root $R < 2^{-511}$ evaluates in the normal range, its maximum absolute rounding error is bounded by $2^{-565}$. The continuous error upon squaring ($2r\delta < 2^{-1075}$) is strictly smaller than the subnormal round-to-nearest-even threshold ($0.5 \cdot 2^{-1074}$). Consequently, the subnormal truncation perfectly annihilates the continuous error, resulting in a strict zero-residual identity ($j=0$) everywhere below the normal boundary.

**Derived Combinatorial Property of the Subnormal Cube Root:**
In stark contrast to the $n=2$ identity, the subnormal cube-root round-trip ($n=3$) produces a strictly asymmetric residual lattice, mapping predominantly (~98.7%) to the integer set $\{-4, \dots, +1\} \cdot 2^{-1074}$, with localized excursions spanning $\{-7, \dots, +3\}$ depending on the exact `numpy.cbrt` implementation evaluated. This is a mathematically bounded consequence of the convex error amplification of the inverse derivative ($3R^2$) interacting with the uniform subnormal grid.

### 4.2 The Nested-Window Bias Model and Diagnostic Limits
To separate pure fractional exponents from slow non-algebraic divergence, V5 implements a nested-window diagnostic modeling the finite-window bias $s(f) = s_\infty + B f^\rho$. This multi-model harness successfully isolates the true algebraic invariant ($s_\infty$) and explicitly rejects iterated-logarithm drift via a strict stability gate. However, this gate is **window-count fragile**: adversarial probing reveals it requires a minimum depth of $n_{\text{windows}} \ge 3$ to successfully reject certain essential structures (e.g., Fixture E), below which it produces false STABLE readings.

**Explicit Diagnostic Limitations (The Degeneracy Proof):** Beyond window-count fragility, adversarial stress-testing reveals that the diagnostic threshold is mathematically porous to specific hybrid structures, specifically $f(x) = \log^2(x)$ and $f(x) = \sqrt{x} \log(x)$. Asymptotic Taylor analysis proves that the instantaneous local scaling exponent of these functions decays as $O(1/t)$ where $t = \log(1/f)$. This constitutes a **proven topological degeneracy**: inside the finite dynamic range of binary64, this decay is information-theoretically indistinguishable from an algebraic branch plus a slow power-law correction ($M_A$). 

---

## Appendix: Provenance and Changes Since V4

To preserve structural honesty and prevent analytical drift, the following claims have been explicitly correctively reframed in V5:
1.  **Downgrade of Theorem 3:** Cross-fixture lattice alignment is no longer claimed as "universal"; it is documented as a strict consequence of IEEE 754 binade mapping (BACL).
2.  **Reframing of Theorem 2:** The previously claimed $R^2 = 1.0$ substrate collapse on the F1 path was a false instrument artifact. However, because the load-bearing F2 path remains unmeasured, the precision-scaling boundaries inside the Sterbenz region remain formally open rather than universally intact.
3.  **Explicit Diagnostic Vulnerabilities:** The nested-window harness is published alongside its mathematical blind spots (`log_squared`) and its window-count fragility, moving from assumed perfection to bounded reliability.
4.  **$n \ge 4$ Bounding:** Assertions regarding high-order integer lattices are now strictly bounded by the structural advantages of composed exact-rounded roots (`sqrt(sqrt)`), explicitly disclaiming universal shattering immunity for native generalized roots.

*(End of Draft)*