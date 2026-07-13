# Source Compilation for a Landen-Type Theorem  
## on the DBP Curvature Periods (Primary ↔ Dual)

**Purpose.**  
Collect every load-bearing fact from the existing corpus that is required to state and prove a Landen-type transformation relating the primary and dual DBP curvature constants.  
This file is the single companion needed to write the theorem; it does not contain the proof itself.

**Target theorem shape (to be proved).**  
There exists an explicit algebraic/modular transformation of the modulus (and a possible residue correction) such that

\[
I_{\rm primary}(\lambda)
\;=\;
\alpha(\sqrt{2})\,
I_{\rm dual}(1-\lambda)
\;+\;
\text{(possible residue / indentation term)},
\]

or an equivalent identity between the two complete-integral expressions after a quadratic change of the elliptic modulus.  
The identity must be compatible with the local curvature valuations already proved in `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md`.

---

## 1. The two elliptic curves and the 2-isogeny

### Minimal DBP curve (j = 128)
\[
E_{128}:\quad
y^2 = w(1-w)(1+w^2)
\quad\text{or minimally}\quad
Y^2 = X^3 - X^2 + X - 1.
\]
\[
j(E_{128}) = 128,
\qquad
\Delta(E_{128}) = -256 = -2^8.
\]
(Non-CM.)

### Legendre model used by the integrals
\[
\lambda = \frac{2-\sqrt{2}}{4},
\qquad
\lambda_{\rm dual} = \frac{2+\sqrt{2}}{4} = 1-\lambda.
\]
\[
\lambda(1-\lambda) = \frac18.
\]
\[
E_\lambda:\quad
y^2 = (1-x^2)(1-\lambda x^2)
\quad\text{or}\quad
Y^2 = X(1-X)(1-\lambda X).
\]
\[
j(E_\lambda) = 10976.
\]

### Isogeny
\[
\Phi_2(128,\,10976) = 0.
\]
Hence \(E_\lambda\) is 2-isogenous to \(E_{128}\) over a field containing \(\sqrt{2}\).  
This is the geometric source of any Landen-type identity (classical Landen arises from a degree-2 isogeny).

---

## 2. The two curvature constants (closed forms)

### Primary (physical total-curvature period)
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
with parameters
\[
k^2 = \frac{2-\sqrt{2}}{4} = \lambda,
\qquad
n = \frac{4-3\sqrt{2}}{8}.
\]
Certified numerical value (50 decimals available in the corpus):
\[
I_{\rm primary}
\approx
-5.01049070266041876905002116052677764805699485672160\ldots
\]
Status: **CERTIFIED / STANDING RESULT**.  
Mathematical type: third-kind dominated curvature period (not a first-kind lattice generator).

### Dual (Galois conjugate / CPV)
Apply \(\sqrt{2}\mapsto-\sqrt{2}\):
\[
k_{\rm dual}^2 = \frac{2+\sqrt{2}}{4} = 1-k^2,
\qquad
n_{\rm dual} = \frac{4+3\sqrt{2}}{8} = 1-n > 1.
\]
\[
I_{\rm dual}
=
-2^{7/4}
\Bigl[
(3-2\sqrt{2})\,\Pi(n_{\rm dual};k_{\rm dual}^2)
-
(2-2\sqrt{2})\,K(k_{\rm dual}^2)
\Bigr].
\]
Because \(n_{\rm dual}>1\) the integral has a pole on the real interval; the certified real value is the Cauchy principal value
\[
I_{\rm dual,CPV}
\approx
-3.988001085974558097719762257539087379694121855552360291\ldots
\]
(Do **not** use the older stale tail that ends \ldots41367660.)

Status: CPV value certified by independent regular routes; naive `ellippi(n>1)` is not admissible for certification.

---

## 3. Exact residue theorem (the monodromy piece of Landen)

Define
\[
s=\sqrt{2},\quad
n=n_{\rm dual},\quad
m=k_{\rm dual}^2,\quad
P=-2^{7/4}(3-2s),\quad
x_0=1/\sqrt{n}.
\]
Bare third-kind differential:
\[
\omega_{\rm bare}
=
\frac{dx}{(1-n x^2)y},
\qquad
y^2=(1-x^2)(1-m x^2).
\]
DBP-weighted differential:
\[
\omega_{\rm DBP}
=
P\cdot\omega_{\rm bare}.
\]
Exact residues:
\[
\operatorname{Res}_{\rm bare}
=
-2^{1/4}(3+2\sqrt{2}),
\qquad
\operatorname{Res}_{\rm DBP}
=
P\cdot\operatorname{Res}_{\rm bare}
=
4.
\]
(The algebraic cancellation \((3-2\sqrt{2})(3+2\sqrt{2})=1\) produces the pure power of 2.)

Consequently the one-sided analytic continuations around the pole satisfy
\[
\text{upper} = I_{\rm dual,CPV} + 4\pi i,
\qquad
\text{lower} = I_{\rm dual,CPV} - 4\pi i,
\]
and the two-sided jump is \(8\pi i\).

This residue is the precise monodromy correction that any Landen-type identity must track when the path of integration crosses or indents around the pole.

---

## 4. Period-normalization controls

\[
\omega_1 = 2^{7/4}\,K(k^2),
\qquad
\operatorname{Im}(\omega_2) = -2^{3/4}\,K(k_{\rm dual}^2).
\]
These pin the Legendre lattice normalization and prevent silent scaling drift when transferring periods through the degree-2 isogeny between \(E_\lambda\) and \(E_{128}\).

---

## 5. Galois action that generates the dual

The automorphism
\[
\sigma:\quad\sqrt{2}\mapsto-\sqrt{2}
\]
acts on the coefficient field of the closed forms and on the Legendre parameter by
\[
\lambda\;\longmapsto\;1-\lambda,
\qquad
n\;\longmapsto\;1-n.
\]
It therefore interchanges the two integral expressions (up to the principal-value prescription).  
Any Landen identity is an explicit functional equation that realises this Galois action on the level of periods.

---

## 6. Local curvature valuations that the identity must respect

From `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md` (the finished local theory):

- On a parity-fixed face the scalar curvature of the inverse-channel metric has leading term
  \[
  R = -\frac{m(m+5)}{B}\,x^{-4}+O(x^{-2}).
  \]
  For the Kerr–Newman faces (\(m=2\)) this is \(-14/B\).

- On a generic face the leading term is order 3 with coefficient equal to the transverse first drift.

- The master quadric
  \[
  C(p)=-\frac12\Bigl(\sum p_a^2+\sum_{a<b}p_ap_b-(p_0+2)\sum p_a\Bigr)
  \]
  computes all normal-vertex coefficients; \(C(2,-2,\dots)=-m(m+5)\).

- Intrinsic gauges:
  \[
  R\cdot d^2\equiv-\frac{m(m+5)}{4}
  \quad\text{(parity-fixed)},
  \qquad
  R\cdot d^{3/2}\to\text{explicit constant}
  \quad\text{(generic)}.
  \]

Any Landen-type transformation of the global periods must be compatible with these local valuations: the singular behaviour of the integrand near every boundary divisor on the surface must match the local calculus after the modular transformation of the modulus.

---

## 7. Certification gates already available (from the dual-constants paper)

```
G1. Bare residue exactness: Res_bare == -2^{1/4}(3+2√2)
G2. Weighted residue exactness: P·Res_bare == 4
G3. Branch jump: one-sided − CPV == ±4πi ; upper−lower == 8πi
G4. Two-route CPV certification to ≥1e-130
G5. Certified decimal pin of I_dual_CPV
G6. λ(1−λ) == 1/8
G7. j(λ) == 10976
G8. Φ₂(128,10976) == 0
G9. Period controls ω₁, Im(ω₂)
```

These are the numerical and algebraic checks that a finished Landen identity must pass (or re-derive).

---

## 8. What is still missing for a geometric proof (open items)

1. **Explicit meromorphic differential** on the original DBP surface whose periods are \(I_{\rm primary}\) and \(I_{\rm dual}\), derived without assuming the closed-form \(K/\Pi\) expressions.  
2. **Riemann bilinear relations / period matrix** on \(E_\lambda\) (or on \(E_{128}\)) that relate the first-kind and third-kind periods.  
3. **Transfer of the third-kind data through the degree-2 isogeny** with explicit index-2 period bookkeeping.  
4. **Cycle** \(C^\sigma\) (physical or classically forbidden) such that \(\int_{C^\sigma}K_G = I_{\rm dual}\).  
5. **Compatibility check** that the local valuations of the integrand, after the Landen transformation of the modulus, reproduce the face laws of the local curvature calculus.

Items 1–4 are exactly the open list already recorded in the dual-constants formulation; item 5 is the new interface with the finished local calculus.

---

## 9. Minimal statement that can be written today (formal / closed-form Landen)

Using only the closed forms, the isogeny, and the residue:

**Proposition (formal Landen for the DBP curvature periods).**  
Let \(\lambda=(2-\sqrt{2})/4\) and let \(\sigma\) be the automorphism \(\sqrt{2}\mapsto-\sqrt{2}\). Then the two complete-integral expressions satisfy
\[
I_{\rm primary}(\lambda)
=
\sigma\bigl(I_{\rm dual}(1-\lambda)\bigr)
\]
as formal expressions in \(K\) and \(\Pi\), while the geometrically meaningful real values differ by the principal-value prescription and the residue jump \(\pm4\pi i\) when a path of integration is continued around the pole of the third-kind differential.

(This is the formal skeleton; the geometric theorem upgrades it by exhibiting the cycle and the isogeny correspondence of differentials.)

---

## 10. Recommended proof order for the full geometric theorem

1. Write the original surface integral as an explicit meromorphic form \(\omega\) on a model of the DBP surface (or on its elliptic quotient).  
2. Push \(\omega\) forward to \(E_\lambda\) via the known reduction; identify it with a multiple of the third-kind differential whose CPV is \(I_{\rm primary}\).  
3. Apply the Galois action / 2-isogeny to obtain \(\omega^\sigma\) on the conjugate model; show its CPV is \(I_{\rm dual}\).  
4. Construct the cycle \(C^\sigma\) (possibly by adding a residue loop around the pole) so that \(\int_{C^\sigma}\omega^\sigma = I_{\rm dual}\).  
5. Verify that the local Laurent expansions of the integrand near every boundary divisor, after the modular transformation, reproduce the face laws of the local curvature calculus (order 3 / order 4 with the universal coefficients).  
6. Package the resulting identity as a Landen-type transformation of the modulus together with the residue correction of 4.

---

## 11. Files in the corpus that supply the above

| Content | Source file |
|---------|-------------|
| Curves, isogeny, closed forms, residue 4, CPV, gates | `DBP_Curvature_Constants_Corrected_Formulation.md` |
| Local face laws, master quadric, valuations, robustness | `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md` |
| Exact verification of face laws & master quadric | `verify_local_curvature_calculus.py` |
| Global cover / Galois context (optional monodromy constraints) | Wreath / Kummer / R9 suite |
| Unified spine (architecture, non-identification rules) | `DBP_UNIFIED_THEOREM_SPINE_DRAFT_v0_1.tex` |

---

*End of source compilation.*  
All numerical pins, algebraic identities, and local valuation laws required to state and prove a Landen-type theorem for the DBP curvature periods are collected above. The geometric existence of the conjugate cycle and the explicit meromorphic form on the surface remain the only open steps.
