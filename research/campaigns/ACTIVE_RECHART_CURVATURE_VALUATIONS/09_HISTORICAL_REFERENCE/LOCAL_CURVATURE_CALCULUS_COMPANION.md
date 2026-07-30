# Companion to Local Curvature Calculus for Inverse-Channel Metrics

**Purpose.**  
This file collects every external mathematical fact required by the research-program document  
`Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt` so that the program becomes self-contained.  
No proofs are repeated here; only the precise statements, normal forms, coefficients, and definitions that the program already treats as known are recorded.

**Sources.**  
- CV campaign (E1/E2, master quadric, intrinsic gauge)  
- Normal-form notes referenced by the program  
- Kerr–Newman 3/4/4 table  
- Dual-constant formulation (kept only for global context; not required by the local program)

---

## 1. Core definitions (to be frozen)

### 1.1 Diagonal divisor-monomial metric germ

A Riemannian metric germ of the form
\[
g = \operatorname{diag}(g_0,\dots,g_m)
\]
near a normal-crossing divisor \(D = \{x_1\cdots x_k = 0\}\) whose coefficients admit monomial-unit expansions
\[
g_i = h_i(x,y)\, x_1^{p_{i1}}\cdots x_k^{p_{ik}},\qquad h_i(0,y)\ne 0.
\]

### 1.2 Inverse-channel subclass (parity-fixed face)

The special collapse pattern
\[
g_x \sim B\, x^2,\qquad
g_{y_\alpha} \sim A_\alpha\, x^{-2}
\]
(with all components even in the collapsing coordinate \(x\)).

### 1.3 Curvature valuation

\[
\operatorname{val}_D\bigl(R[g]\bigr)
:=
\text{pole order of the scalar curvature \(R\) along \(D\)}.
\]

### 1.4 Metric valuation vector

The exponent matrix \((p_i)\) (or \((p_i,q_i)\) in codimension two) appearing in the monomial expansions of the metric coefficients.

---

## 2. Single-face theorems (already established)

### Theorem A — Generic quadratic collapse

**Hypothesis.**
\[
g_x = A x^2 + O(x^3),\qquad
g_{y_\alpha} = P_{\alpha 0} + P_{\alpha 1} x + O(x^2).
\]

**Conclusion.**
\[
R
=
\frac{1}{A}
\sum_{\alpha=1}^{m}
\frac{P_{\alpha 1}}{P_{\alpha 0}}
\, x^{-3}
+
O(x^{-2}).
\]

**Message.** Generic collapse detects transverse first drift.  
Pole order = 3; leading coefficient = transverse first drift scaled by \(1/A\).

### Theorem B — Parity-fixed inverse-channel face

**Hypothesis.**
\[
g_x = B x^2 + O(x^4),\qquad
g_{y_\alpha} = A_\alpha x^{-2} + O(1),
\]
all components even in \(x\).

**Conclusion.**
\[
R
=
-\frac{m(m+5)}{B}\, x^{-4}
+
O(x^{-2}).
\]

**Exact model (pure parity-fixed).**
\[
ds^2 = B x^2\, dx^2 + x^{-2}\sum_{\alpha=1}^{m} A_\alpha\, dy_\alpha^2
\quad\Longrightarrow\quad
R = -\frac{m(m+5)}{B}\, x^{-4}.
\]

**Special case \(m=2\) (Kerr–Newman faces).**
\[
R = -\frac{14}{B}\, x^{-4}.
\]

---

## 3. Intrinsic (metric-distance) gauge — Lemma E2

Let \(d\) be proper distance to the face.

- **Parity-fixed faces.**
  \[
  R\cdot d^2 \equiv -\frac{m(m+5)}{4}
  \]
  (pure number; the collapsing amplitude \(B\) is completely absorbed).

- **Generic faces.**  
  Intrinsic rate \(d^{-3/2}\); more precisely
  \[
  \lim R\cdot d^{3/2}
  =
  \Bigl(\sum\frac{P_{\alpha1}}{P_{\alpha0}}\Bigr)
  A^{-1/4}/2^{3/2}.
  \]

This is the coordinate-free form that kills the objection “pole order is a chart artifact.”

---

## 4. Master quadric (single object, three jobs)

\[
C(p)
=
-\frac12
\Biggl(
\sum_a p_a^2
+
\sum_{a<b} p_a p_b
-
(p_0+2)\sum_a p_a
\Biggr).
\]

**Jobs performed by one formula:**

1. Single-face monomial coefficient.  
2. Both corner vertex coefficients (evaluate per face).  
3. Cancellation condition (vanishing locus of \(C\)).

**Key evaluation.**
\[
C(2,-2,\dots,-2) = -m(m+5).
\]

**Vanishing locus contains:**

- generic faces (\(p_a=0\)),
- flat cones,
- scalar-flat isotropic exponents \(p_a = 4/(m+1)\)  
  (the metric \(dr^2 + \sum r^{4/(m+1)}\, dy^2\) is exactly scalar-flat, not merely leading-order).

---

## 5. Boundary robustness (E2, computer-verified claims)

Under a boundary-adapted change
\[
x = c(y)\, x' + k\, (x')^2,\qquad c>0,
\]

- the transformed collapsing amplitude becomes \(B' = B\, c^4\);
- the order-4 pole law remains form-invariant when read with \(B'\):
  \[
  \text{leading coefficient} = -\frac{m(m+5)}{B'};
  \]
- the odd (order-3) coefficient vanishes if and only if the change preserves parity (\(k=0\)).

Thus pole order is invariant, and the normalised leading coefficient is form-invariant under parity-preserving boundary changes.

---

## 6. Codimension-two corner data (already computed for KN)

For a normal-crossing corner \(D=\{xy=0\}\) the polar support of \(R\) is controlled by the vertices
\[
V_1 = \bigl(-(p_1+2),-q_1\bigr),\quad
V_2 = \bigl(-p_2,-(q_2+2)\bigr),\quad
V_0 = (-p_0,-q_0)
\]
after deletion of vertices whose coefficients vanish (master-quadric cancellation).

**Kerr–Newman spectator fan (validated cross-check).**

- Wedge support: \(\max(4a-2,\,4-2a)\).  
- Vertex coefficients (balanced assignment): \(A=-84\), \(B=-12\).  
- Sector-weight alternative (one side): \(-28 = 2\cdot(-14)\).

(The B1 crown experiment decides which weighting is realised.)

---

## 7. Kerr–Newman divisor table (flagship application)

| Divisor              | Local type       | Pole order |
|----------------------|------------------|------------|
| \(T=0\)              | generic collapse | 3          |
| \(\Omega=0\) or \(J=0\) | parity-fixed   | 4          |
| \(\Phi_e=0\) or \(Q=0\) | parity-fixed   | 4          |
| \(J=Q=0\)            | corner           | Newton polygon |

This table is the concrete payoff of Theorems A and B plus the corner rule.

---

## 8. Lamé formula (engine E1)

For a diagonal metric \(g=\sum_i H_i^2 (dx^i)^2\) with Lamé coefficients \(H_i\) and
\[
\beta_{ij} = \frac{\partial_i H_j}{H_i}\quad(i\neq j),
\]
the scalar curvature is
\[
R
=
-2\sum_{i<j}
\frac{1}{H_i H_j}
\Biggl[
\partial_i\beta_{ij}
+
\partial_j\beta_{ji}
+
\sum_{k\neq i,j}
\beta_{ki}\beta_{kj}
\Biggr].
\]

This is the computational engine that turns a metric germ into \(R\) without expanding the full Christoffel–Ricci expression by hand. (Verified for fully general \(n=3\); \(n=4\) polynomial fixtures exist but need lightening before re-run.)

---

## 9. Dual constants (global context only)

**Not required by the local calculus.**  
Recorded solely so that later reconstruction / ambient-light questions have a fixed reference.

- **Primary** (physical total curvature):
  \[
  I_{\rm primary}
  =
  -2^{7/4}
  \Bigl[
  (3+2\sqrt{2})\,\Pi(n;k^2)
  -
  (2+2\sqrt{2})\,K(k^2)
  \Bigr],
  \]
  with \(k^2=(2-\sqrt{2})/4\), \(n=(4-3\sqrt{2})/8\).  
  Numerical pin \(\approx -5.01049070266041876905\ldots\)

- **Dual** (Galois conjugate, CPV):
  obtained by \(\sqrt{2}\mapsto-\sqrt{2}\);  
  \(I_{\rm dual,CPV}\approx -3.98800108597455809772\ldots\)  
  Residue of the DBP-weighted third-kind differential = exactly 4;  
  one-sided jumps \(\pm 4\pi i\).

Status of dual as physical ambient light: **unsupported** until a cycle is exhibited.

---

## 10. What the local program still owes (not supplied by this companion)

1. Full human-readable proofs of Theorems A and B (the statements are here; the write-ups are not).  
2. The general curvature-valuation formula for arbitrary diagonal monomial-unit germs.  
3. Complete codimension-two Newton-polygon theorem (cancellation classification).  
4. Coordinate-robustness theorem written as a formal statement + proof.  
5. The short “Definitions and Theorem Statements” spine document called for by Stage 10 of the program.  
6. One synthetic non-KN example with full calculation.

---

## 11. Minimal self-contained core for immediate use

If only the absolute minimum is needed to start writing proofs, the following six items are sufficient:

1. Definition of diagonal divisor-monomial metric germ.  
2. Definition of parity-fixed inverse-channel face.  
3. Theorem A (generic order-3 + transverse drift).  
4. Theorem B (parity-fixed order-4 + coefficient \(-m(m+5)/B\)).  
5. Intrinsic gauge: \(R\cdot d^2 = -m(m+5)/4\) on parity faces.  
6. Master quadric \(C(p)\) with the evaluation \(C(2,-2,\ldots)=-m(m+5)\).

Everything else in this companion is supporting or global context.

---

*End of companion.*  
This file is intended to be placed beside  
`Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt`  
so that the research program no longer depends on external notes for its load-bearing mathematical content.
