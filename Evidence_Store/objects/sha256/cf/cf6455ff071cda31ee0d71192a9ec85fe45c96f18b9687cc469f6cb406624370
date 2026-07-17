# V4 Agent Task Specification: Phase 2 Mathematical Foundations

## 1. Operational Mandate
This task specification is designed for execution by an autonomous coding agent (Claude Code) operating within the Lloyd V4 substrate. 

**Discipline Gates (STRICT):**
* **Zero-Axiom Tolerance:** No assumed floating-point behaviors. All claims must be backed by reproducible IEEE 754 raw hex traces or exact mathematical reduction.
* **No V3 Authority:** Do not import, call, or adapt any V3 legacy K_G solvers. 
* **Observation-Only Until Proven:** If a structural invariant is found, it remains a descriptive observation until a derivation from IEEE 754 axioms is provided.

## 2. Task A: Precision-Scaling Separation Manifold Boundary Test
**Target:** Discover the exact geometric mechanics of collapse for the $C_{p,k} = a + u_p b_k$ model outside the regular region.

* **Objective:** The linear precision-scaling model holds perfectly ($R^2 = 1.0$) in the regular region. We must locate the exact geometric boundary where this collapses and mathematically isolate the dominating artifact.
* **Execution Plan:**
  1. Construct a stress-test grid for the four V4 fixtures (Schwarzschild, SR, pure-algebraic, cube-root) that intentionally drives the operands *out* of the regular region and *through* the Sterbenz boundary.
  2. Execute the multi-precision measurement ($float32$, $float64$, $float128$, $decimal_{50}$) continuously across this boundary.
  3. Track the $R^2$ of the linear fit $C_{p,k}$ against $u_p$.
* **Burden of Proof:**
  * Identify the exact $f$ threshold where $R^2$ diverges from 1.0.
  * Provide the mathematical term (e.g., cross-term compounding, catastrophic cancellation of a specific higher-order bit) that dominates the residual outside the regular region.
  * **Artifact Required:** A JSON trace of the exact floating-point values at the boundary of collapse.

## 3. Task B: Subnormal Topology Audit ($f < 2^{-1022}$)
**Target:** Map the topological breakdown of the transfer-function exponent law and the $c_2$ lattice when operands cross into the subnormal regime.

* **Objective:** Conjecture C and the $c_2$ integer-lattice property are currently strictly gated to the normal range. Because subnormals have uniform spacing ($2^{-1074}$) rather than binade-proportional spacing, the scaling invariance dies. We need to know what happens to the residual structure.
* **Execution Plan:**
  1. Generate a sweep grid strictly in the subnormal regime: $f \in [2^{-1074}, 2^{-1022})$.
  2. Run the $c_2 = \text{round}(V_n + (x_{\text{term}} - 1))$ algebraic chains for $n=2$ (sqrt) and $n=3$ (cbrt).
  3. Measure the residuals against $\text{ulp}(f)$ (which is statically $2^{-1074}$ in this regime).
* **Burden of Proof:**
  * Does the residual form a new subnormal-specific lattice, or does it shatter into unstructured noise?
  * How does the limiting log-log slope ($\alpha - 1$) degrade as $f \to 0^+$ in subnormals?
  * **Artifact Required:** Raw float64 hex traces of the transition pairs crossing $2^{-1022}$, demonstrating the breakdown of Conjecture C.

## 4. Task C: Nested-Window Bias Harness (Task 023b Fulfillment)
**Target:** Implement the finite-window bias proposition and separate pure algebraic branches from non-algebraic drift.

* **Objective:** The current single-window alpha classification incorrectly accepts iterated-logarithm drift (Fixture E) as a small fractional exponent. We must build the V4 typed fitting harness that implements the nested-window diagnostic.
* **Execution Plan:**
  1. Implement a nested-window processor that fits $s(f) = s_\infty + B f^\rho$ across sequential sub-windows of the $h$-grid.
  2. Implement the Automatic Stability Diagnostic (model comparison between $M_A$ algebraic, $M_L$ logarithmic/slow variation, and $M_E$ essential).
  3. Point this harness at Fixture C (slow algebraic drift), Fixture D (logarithmic divergence), and Fixture E (iterated-log drift).
* **Burden of Proof:**
  * The harness MUST successfully classify Fixture E as non-algebraic drift, explicitly rejecting it as a stable fractional branch.
  * The harness MUST successfully isolate $s_\infty$ from the finite-window bias $B f^\rho$ in Fixture C.
  * **Artifact Required:** The execution script and the emitted `TypedResult` JSON showing the nested-window variance and the winning information-criterion model.

## 5. Deliverables & Handoff
Upon completion, the agent must output:
1. `agent_sandbox_results.json`: Containing the raw floating-point traces and statistical fits.
2. `sandbox_summary_report.md`: A strict, zero-axiom breakdown of the mathematical mechanics discovered.
3. No code is to be promoted to the V4 substrate (Layer 1) until these proofs are reviewed. All work remains in `scratch/` or `evals/`.
