# Local Curvature Calculus for Diagonal Inverse-Channel Metrics

## Completed theorem-and-proof spine, v1.0

**Date:** 2026-07-12  
**Scope:** local scalar-curvature valuations near normal-crossing divisors  
**Curvature convention:** the round unit two-sphere has scalar curvature \(+2\)  
**Source policy:** this is a new additive manuscript; neither supplied calculus file nor any corpus source is altered

---

## Abstract

Let

\[
g=\sum_{i=1}^{n}g_i(t)\,(dt^i)^2
\]

be a positive diagonal metric near a normal-crossing divisor

\[
D=\{z_1\cdots z_k=0\},
\qquad
g_i=h_i(z,y)z^{P_i},
\]

where each \(h_i\) is a positive smooth unit and \(P_i\in\mathbb R^k\). We prove the exact local decomposition

\[
R[g]
=
\sum_{a=1}^{k}z^{-P_a-2e_a}F_a(z,y)
+
\sum_{\mu=k+1}^{n}z^{-P_\mu}F_\mu(z,y).
\]

The coefficient germs \(F_i\) are smooth and depend only on the exponent matrix and coordinatewise two-jets of the units. The boundary value of each normal coefficient is an explicit quadratic form in one column of the exponent matrix.

This one identity yields the general curvature valuation, the generic order-three law, the parity-fixed order-four law with coefficient \(-m(m+5)/B\), intrinsic proper-distance normalizations, coordinate robustness, the codimension-two Newton polygon, its codimension-\(k\) extension, and a complete cancellation hierarchy. The global scalar curvature never needs to be assembled.

---

## 1. Local objects

### Definition 1.1 — Diagonal divisor-monomial metric germ

Use local coordinates

\[
(t^1,\ldots,t^n)
=(z_1,\ldots,z_k,y_{k+1},\ldots,y_n)
\]

on the positive orthant \(z_a>0\), with

\[
D=\bigcup_{a=1}^{k}D_a,
\qquad
D_a=\{z_a=0\}.
\]

A diagonal divisor-monomial metric germ is

\[
g=\sum_{i=1}^{n}g_i(dt^i)^2,
\qquad
g_i=h_i(z,y)z^{P_i},
\qquad
z^{P_i}:=\prod_{a=1}^{k}z_a^{p_{ia}},
\]

where \(P_i=(p_{i1},\ldots,p_{ik})\in\mathbb R^k\) and every \(h_i\) extends smoothly and positively to the corner. The matrix

\[
P=(p_{ia})\in M_{n\times k}(\mathbb R)
\]

is the metric valuation matrix.

### Definition 1.2 — Curvature order

For a scalar germ \(f\) along \(D_a\), write

\[
\operatorname{ord}_{D_a}(f)=\lambda
\]

when \(f=z_a^\lambda u\) with \(u|_{D_a}\neq0\). Define the signed blow-up order

\[
\kappa_{D_a}(f):=-\operatorname{ord}_{D_a}(f).
\]

Thus \(\kappa>0\) is a pole, \(\kappa=0\) is finite nonzero order, and \(\kappa<0\) is vanishing.

For a positive weight \(w=(w_1,\ldots,w_k)\),

\[
\operatorname{ord}_w(z^\alpha)=\langle w,\alpha\rangle,
\qquad
\kappa_w=-\operatorname{ord}_w.
\]

### Definition 1.3 — Parity-fixed inverse-channel face

At a face \(x=0\), a germ is parity-fixed when it is invariant under \(x\mapsto-x\) in an adapted parity chart. The inverse-channel pattern in dimension \(m+1\) is

\[
g_x=Bx^2+O(x^4),
\qquad
g_{y_\alpha}=A_\alpha x^{-2}+O(1),
\qquad
\alpha=1,\ldots,m,
\]

with all component expansions even in \(x\).

---

## 2. Diagonal scalar curvature

Set

\[
H_i=\sqrt{g_i},
\qquad
u_i=\log H_i=\frac12\log g_i.
\]

For \(i\neq j\), define

\[
\beta_{ij}=\frac{\partial_iH_j}{H_i}.
\]

### Lemma 2.1 — Lamé formula

For a diagonal metric,

\[
R
=
-2\sum_{i<j}\frac1{H_iH_j}
\left[
\partial_i\beta_{ij}
+\partial_j\beta_{ji}
+\sum_{\ell\neq i,j}\beta_{\ell i}\beta_{\ell j}
\right].
\tag{2.1}
\]

#### Proof

The nonzero Christoffel symbols of an orthogonal metric are

\[
\Gamma^i_{ii}=\partial_i\log H_i,
\qquad
\Gamma^i_{ij}=\partial_j\log H_i,
\qquad
\Gamma^i_{jj}=-\frac{H_j\partial_iH_j}{H_i^2}
\quad(i\neq j),
\]

and the symbols with three distinct indices vanish. Substitution into \(R^i{}_{jij}\) gives the coordinate-plane sectional curvature

\[
K_{ij}
=
-\frac1{H_iH_j}
\left[
\partial_i\beta_{ij}
+\partial_j\beta_{ji}
+\sum_{\ell\neq i,j}\beta_{\ell i}\beta_{\ell j}
\right].
\]

Since \(R=2\sum_{i<j}K_{ij}\), (2.1) follows. \(\square\)

### Lemma 2.2 — Directional curvature channels

Define

\[
\mathcal Q_j(u)
:=
\sum_{i\neq j}
\left[
\partial_j^2u_i
+(\partial_ju_i)^2
-(\partial_ju_j)(\partial_ju_i)
\right]
+
\sum_{\substack{r<s\\r,s\neq j}}
(\partial_ju_r)(\partial_ju_s).
\tag{2.2}
\]

Then

\[
\boxed{
R[g]
=
-2\sum_{j=1}^{n}e^{-2u_j}\mathcal Q_j(u)
=
-2\sum_{j=1}^{n}\frac{\mathcal Q_j(u)}{g_j}.
}
\tag{2.3}
\]

#### Proof

Because

\[
\beta_{ij}=e^{u_j-u_i}\partial_i u_j,
\]

we have

\[
\frac1{H_iH_j}\partial_i\beta_{ij}
=
e^{-2u_i}
\left[
\partial_i^2u_j
+(\partial_i u_j)^2
-(\partial_i u_i)(\partial_i u_j)
\right],
\]

and

\[
\frac{\beta_{\ell i}\beta_{\ell j}}{H_iH_j}
=
e^{-2u_\ell}(\partial_\ell u_i)(\partial_\ell u_j).
\]

Grouping (2.1) by differentiation direction gives (2.3). \(\square\)

Equation (2.3) is the engine of the calculus: scalar curvature is a sum of \(n\) directional channels, and the \(j\)-th channel is divided only by \(g_j\).

---

## 3. Exact divisor-channel decomposition

Write

\[
u_i
=
\frac12\log h_i
+
\frac12\sum_{a=1}^{k}p_{ia}\log z_a.
\tag{3.1}
\]

### Theorem 3.1 — General local decomposition

For every diagonal divisor-monomial metric germ,

\[
\boxed{
R[g]
=
\sum_{a=1}^{k}z^{-P_a-2e_a}F_a(z,y)
+
\sum_{\mu=k+1}^{n}z^{-P_\mu}F_\mu(z,y),
}
\tag{3.2}
\]

where

\[
F_a=-2h_a^{-1}z_a^2\mathcal Q_a(u),
\qquad
F_\mu=-2h_\mu^{-1}\mathcal Q_\mu(u).
\tag{3.3}
\]

Every \(F_i\) is smooth up to the corner. It depends only on \(P\), the units \(h_i\), and first and second derivatives of those units in the single coordinate direction \(t^i\).

#### Proof

For a normal direction \(z_a\),

\[
\partial_a u_i
=
\frac{p_{ia}}{2z_a}
+\frac12\partial_a\log h_i,
\]

\[
\partial_a^2u_i
=
-\frac{p_{ia}}{2z_a^2}
+\frac12\partial_a^2\log h_i.
\]

Hence \(\mathcal Q_a\) has at worst a \(z_a^{-2}\) pole and \(z_a^2\mathcal Q_a\) is smooth. Since \(g_a^{-1}=h_a^{-1}z^{-P_a}\),

\[
-2g_a^{-1}\mathcal Q_a=z^{-P_a-2e_a}F_a.
\]

For a tangential direction \(\mu>k\), the monomial factors are constant under \(\partial_\mu\), so \(\mathcal Q_\mu\) is smooth and

\[
-2g_\mu^{-1}\mathcal Q_\mu=z^{-P_\mu}F_\mu.
\]

Summing the channels proves (3.2). \(\square\)

### Corollary 3.2 — Finite base support

The outer divisor exponents of scalar curvature lie in the finite set

\[
\boxed{
V_a=-P_a-2e_a\quad(a\le k),
\qquad
V_\mu=-P_\mu\quad(\mu>k).
}
\tag{3.4}
\]

Normal dependence of the units produces only inward shifts \(V_i+\beta\), \(\beta\in\mathbb N^k\).

### Corollary 3.3 — Finite-jet principle

If the first nonzero curvature coefficient occurs at inward order \(|\beta|=N\), then the valuation and leading coefficient are determined by \(P\) and a finite \((N+2)\)-jet of the units.

There is no uniform jet bound after arbitrary cancellations. A smooth flat coefficient can have every Taylor coefficient zero; such a term is smaller than every power and creates no finite-order pole. Analytic or polyhomogeneous units give an actual Newton expansion. Smooth units give the same conclusion through the first finite nonzero jet.

---

## 4. The master quadric

Fix a normal direction \(a\le k\) and put

\[
\lambda_i=p_{ia}.
\]

Define

\[
\boxed{
C_a(P)
=
-\frac12
\left[
\sum_{i\neq a}\lambda_i^2
+
\sum_{\substack{r<s\\r,s\neq a}}\lambda_r\lambda_s
-(\lambda_a+2)\sum_{i\neq a}\lambda_i
\right].
}
\tag{4.1}
\]

### Theorem 4.1 — Normal-vertex coefficient

\[
\boxed{
F_a|_D=\frac{C_a(P)}{h_a|_D}.
}
\tag{4.2}
\]

#### Proof

Use

\[
\partial_a u_i=\frac{\lambda_i}{2z_a}+O(1),
\qquad
\partial_a^2u_i=-\frac{\lambda_i}{2z_a^2}+O(1)
\]

in (2.2). The boundary value of \(z_a^2\mathcal Q_a\) is

\[
\frac14
\left[
\sum_{i\neq a}\lambda_i^2
+
\sum_{\substack{r<s\\r,s\neq a}}\lambda_r\lambda_s
-(\lambda_a+2)\sum_{i\neq a}\lambda_i
\right].
\]

Multiplication by \(-2/h_a\) gives (4.2). \(\square\)

For one face, with normal exponent \(p_0\) and transverse exponents \(p_1,\ldots,p_m\), this is

\[
C(p)
=
-\frac12
\left[
\sum_\alpha p_\alpha^2
+
\sum_{\alpha<\beta}p_\alpha p_\beta
-(p_0+2)\sum_\alpha p_\alpha
\right].
\tag{4.3}
\]

The same quadratic form supplies single-face monomial coefficients, normal corner-vertex coefficients, and the first structural cancellation equation \(C=0\).

---

## 5. Single-face calculus

Let \(x=z_1\), let \(p_i=p_{i1}\), and write \(g_x=g_0\), \(g_{y_\alpha}=g_\alpha\).

### Theorem 5.1 — General single-face valuation

There are smooth germs \(F_0,\ldots,F_m\) such that

\[
R
=
x^{-(p_0+2)}F_0(x,y)
+
\sum_{\alpha=1}^{m}x^{-p_\alpha}F_\alpha(x,y),
\tag{5.1}
\]

with

\[
F_0(0,y)=\frac{C(p)}{h_0(0,y)}.
\tag{5.2}
\]

The curvature order is the largest noncancelled member of

\[
p_0+2-\operatorname{ord}_xF_0,
\qquad
p_\alpha-\operatorname{ord}_xF_\alpha.
\tag{5.3}
\]

The bare exponent maximum is valid only after its coefficient is checked.

### Theorem 5.2 — Generic quadratic collapse

Assume

\[
g_x=Ax^2+O(x^3),
\qquad
g_{y_\alpha}=P_{\alpha0}+P_{\alpha1}x+O(x^2),
\qquad
A,P_{\alpha0}>0.
\]

Then

\[
\boxed{
R
=
\frac1A
\sum_{\alpha=1}^{m}
\frac{P_{\alpha1}}{P_{\alpha0}}
x^{-3}
+O(x^{-2}).
}
\tag{5.4}
\]

The coefficient is independent of the cubic coefficient of \(g_x\) and all quadratic transverse data.

#### Proof

Here \(p_0=2\), every \(p_\alpha=0\), and \(C(p)=0\). The nominal order-four normal vertex cancels.

Write

\[
u_0=\log x+\frac12\log A+O(x),
\]

\[
u_\alpha
=
\frac12\log P_{\alpha0}
+
\frac12\frac{P_{\alpha1}}{P_{\alpha0}}x
+O(x^2).
\]

In \(\mathcal Q_0\), the only \(x^{-1}\) term is

\[
-(\partial_xu_0)(\partial_xu_\alpha)
=
-\frac1{2x}\frac{P_{\alpha1}}{P_{\alpha0}}+O(1).
\]

Therefore

\[
\mathcal Q_0
=
-\frac1{2x}
\sum_\alpha\frac{P_{\alpha1}}{P_{\alpha0}}
+O(1).
\]

Since \(g_x^{-1}=A^{-1}x^{-2}+O(x^{-1})\), the normal channel gives (5.4). Tangential channels are \(O(1)\), and the remaining normal terms are \(O(x^{-2})\). \(\square\)

### Corollary 5.3 — Generic cancellation

If

\[
\sum_\alpha P_{\alpha1}/P_{\alpha0}=0,
\]

the order-three coefficient vanishes. The \(x^{-2}\) layer must then be inspected; “order three with zero coefficient” is not a valid conclusion.

### Theorem 5.4 — Parity-fixed inverse-channel face

Assume every component is even in \(x\) and

\[
g_x=Bx^2+O(x^4),
\qquad
g_{y_\alpha}=A_\alpha x^{-2}+O(1),
\qquad
B,A_\alpha>0.
\]

Then

\[
\boxed{
R
=
-\frac{m(m+5)}B x^{-4}
+O(x^{-2}).
}
\tag{5.5}
\]

The transverse amplitudes \(A_\alpha\) do not enter the leading coefficient.

#### Proof

The exponent vector is

\[
(p_0,p_1,\ldots,p_m)=(2,-2,\ldots,-2).
\]

Equation (4.3) gives

\[
C(2,-2,\ldots,-2)=-m(m+5).
\]

The normal vertex is \(x^{-4}\); every transverse base vertex is \(x^2\), hence nonpolar. Equation (4.2) gives the leading term. Evenness removes the inward shift by one, so the next possible normal term is \(x^{-2}\). \(\square\)

### Theorem 5.5 — Pure parity model

For

\[
d\ell^2=Bx^2(dx)^2+x^{-2}\sum_{\alpha=1}^{m}A_\alpha(dy_\alpha)^2,
\]

the formula is exact:

\[
\boxed{
R=-\frac{m(m+5)}B x^{-4}.
}
\tag{5.6}
\]

#### Independent proof

Set \(r=\sqrt B\,x^2/2\). Then

\[
d\ell^2=(dr)^2+w(r)^2h_{\mathrm{flat}},
\qquad
w\propto r^{-1/2}.
\]

For an \(m\)-dimensional flat fibre,

\[
R=-2m\frac{w''}{w}-m(m-1)\left(\frac{w'}w\right)^2.
\]

Using \(w'/w=-1/(2r)\), \(w''/w=3/(4r^2)\), and \(4r^2=Bx^4\) gives (5.6). \(\square\)

### Proposition 5.6 — Scalar-flat monomial locus

For

\[
d\ell^2=(dr)^2+r^{2a}\sum_{\alpha=1}^{m}(dy_\alpha)^2,
\]

\[
R=-m\bigl((m+1)a^2-2a\bigr)r^{-2}.
\]

Thus \(a=2/(m+1)\), equivalently transverse metric exponent \(4/(m+1)\), is exactly scalar-flat. This is a structural zero of the master quadric, not merely a cancelled displayed approximation.

---

## 6. Coordinate and intrinsic robustness

### Theorem 6.1 — Divisor order is invariant

Let \(x\) and \(x'\) define the same smooth divisor, with

\[
x=u(x',y')x',
\qquad
u|_D>0.
\]

Then every scalar germ satisfies

\[
\operatorname{ord}_{x=0}(f)=\operatorname{ord}_{x'=0}(f).
\]

#### Proof

If \(f=x^\lambda v\), \(v|_D\neq0\), then

\[
f=(x')^\lambda u^\lambda v
\]

and \(u^\lambda v\) is again a nonzero unit. \(\square\)

### Theorem 6.2 — Normal-crossing robustness

Suppose a boundary-adapted diffeomorphism preserves the components of a simple normal crossing up to permutation:

\[
z_a=u_a(z',y')z'_{\sigma(a)},
\qquad
u_a|_D>0.
\]

Then the multivaluation and Newton support transform only by \(\sigma\); unit factors change front coefficients but not exponent vectors. A monomial blow-up transforms exponent vectors by its integer linear map.

The diagonal representation need not remain diagonal under this change. The valuation survives because \(R[g]\) is a scalar. Formula (2.3) may be used in any one adapted orthogonal chart without claiming that its individual directional summands are coordinate-invariant.

### Proposition 6.3 — Parity change to second order

For the pure parity model, let

\[
x=c(y)x'+k(y)(x')^2+O((x')^3),
\qquad
c>0.
\]

Then the leading normal metric amplitude is

\[
B'=Bc^4,
\]

and

\[
R
=
-\frac{m(m+5)}{Bc^4}(x')^{-4}
+
\frac{4m(m+5)k}{Bc^5}(x')^{-3}
+O((x')^{-2}).
\tag{6.1}
\]

Thus the order-four law is form-invariant. The displayed odd coefficient vanishes iff \(k=0\). Full parity preservation requires the normal coordinate change to be odd, not merely quadratic-free to one order.

#### Proof

The metric result follows from \(Bx^2(dx)^2\) and \(dx=c\,dx'+O(x')\). Also

\[
x^{-4}
=
c^{-4}(x')^{-4}
-4kc^{-5}(x')^{-3}
+O((x')^{-2}).
\]

Substitute (5.6). \(\square\)

### Theorem 6.4 — Proper-distance gauges

Let \(d\) be proper normal distance to the face.

For the parity-fixed face,

\[
d=\frac{\sqrt B}{2}x^2+O(x^4),
\]

so

\[
\boxed{
\lim_{x\to0}R\,d^2=-\frac{m(m+5)}4.
}
\tag{6.2}
\]

For the generic face, set

\[
\Theta=\sum_\alpha P_{\alpha1}/P_{\alpha0}.
\]

Then

\[
d=\frac{\sqrt A}{2}x^2+O(x^3),
\]

and

\[
\boxed{
\lim_{x\to0}R\,d^{3/2}
=
\frac{\Theta A^{-1/4}}{2^{3/2}}.
}
\tag{6.3}
\]

These are intrinsic singularity rates.

---

## 7. Newton polyhedra and corners

### Definition 7.1 — Curvature support

Expand the smooth coefficients in (3.2):

\[
F_i(z,y)=\sum_{\beta\in\mathbb N^k}f_{i,\beta}(y)z^\beta.
\]

First combine equal exponent vectors:

\[
c_\alpha(y)
=
\sum_{i,\beta:\,V_i+\beta=\alpha}f_{i,\beta}(y).
\]

At \(y=y_0\), define

\[
\mathcal S_R(y_0)=\{\alpha:c_\alpha(y_0)\neq0\}
\]

and

\[
\mathcal N_R
=
\operatorname{conv}\bigl(\mathcal S_R+\mathbb R_{\ge0}^k\bigr).
\]

### Theorem 7.2 — Weighted curvature valuation

Assume analytic or polyhomogeneous coefficients, or stop at the first finite nonzero smooth jet. Along

\[
z_a=\rho_a\epsilon^{w_a},
\qquad
\rho_a>0,\quad w_a>0,
\]

write

\[
R(\rho\epsilon^w,y_0)
=
\sum_\lambda\epsilon^\lambda
\mathcal F_{w,\lambda}(\rho,y_0),
\]

where

\[
\mathcal F_{w,\lambda}(\rho,y_0)
=
\sum_{\substack{\alpha\in\mathcal S_R\\
\langle w,\alpha\rangle=\lambda}}
c_\alpha(y_0)\rho^\alpha.
\]

Then

\[
\boxed{
\kappa_w(R)
=
-\min\{\lambda:
\mathcal F_{w,\lambda}(\rho,y_0)\neq0\}.
}
\tag{7.1}
\]

For generic \(\rho\), this is the negative support function of \(\mathcal N_R\). If the leading front coefficient vanishes at a special ratio, the order drops to the next nonzero face.

#### Proof

Substitute the monomial path, group equal powers of \(\epsilon\), and select the first nonzero group. \(\square\)

### Corollary 7.3 — When deleting a vertex is complete

If every outer coefficient \(F_i(0,y_0)\) is nonzero after exponent collisions are combined, the leading Newton polyhedron is generated by the finite base vertices (3.4).

If an outer coefficient vanishes, deleting that vertex is complete only when its coefficient germ is identically zero or the metric is pure monomial in the normal variables. Otherwise the next inward Taylor layer must be inserted.

### Theorem 7.4 — Closed three-dimensional corner formula

Use coordinates \((s,x,y)\) and suppose

\[
g_s=h_0(s)x^{p_0}y^{q_0},
\qquad
g_x=h_1(s)x^{p_1}y^{q_1},
\qquad
g_y=h_2(s)x^{p_2}y^{q_2}.
\]

Then

\[
R
=
\frac{A}{2h_1}x^{-(p_1+2)}y^{-q_1}
+
\frac{B}{2h_2}x^{-p_2}y^{-(q_2+2)}
+
L_sx^{-p_0}y^{-q_0},
\tag{7.2}
\]

where

\[
A
=
-p_0^2+p_0p_1-p_0p_2+2p_0+p_1p_2-p_2^2+2p_2,
\tag{7.3}
\]

\[
B
=
-q_0^2+q_0q_2-q_0q_1+2q_0+q_2q_1-q_1^2+2q_1.
\tag{7.4}
\]

If \(a_i=\sqrt{h_i}\) and \(\ell_i=a_i'/a_i\), then

\[
L_s
=
-\frac2{h_0}
\left[
\frac{a_1''}{a_1}
+\frac{a_2''}{a_2}
-\ell_0(\ell_1+\ell_2)
+\ell_1\ell_2
\right].
\tag{7.5}
\]

The three possible exponent vertices are

\[
V_x=(-(p_1+2),-q_1),
\quad
V_y=(-p_2,-(q_2+2)),
\quad
V_s=(-p_0,-q_0).
\]

#### Proof

The units are independent of \(x,y\), so the normal coefficient germs in (3.2) are constant in the normal variables. Equations (7.3) and (7.4) are twice the corresponding master quadrics. Equation (7.5) is the tangential channel (2.2). \(\square\)

### Theorem 7.5 — Complete cancellation hierarchy

The leading order changes in exactly four ways.

1. **Structural channel cancellation:** a master coefficient \(C_a(P)\) or tangential coefficient vanishes.
2. **Exponent-collision cancellation:** several channels share one exponent vector, so their coefficients cancel after summation.
3. **Front-face cancellation:** distinct vertices lie on one supporting face and their front polynomial vanishes at a special approach ratio.
4. **Higher-jet cancellation:** one or more inward Taylor layers vanish after an outer coefficient vanishes.

These cases are exhaustive because (3.2) is an exact finite sum of base monomials times smooth coefficient germs.

### Corollary 7.6 — Codimension \(k\)

The base curvature polytope of a codimension-\(k\) diagonal monomial-unit germ has at most \(n\) directional vertices

\[
V_a=-P_a-2e_a,
\qquad
V_\mu=-P_\mu.
\]

The weighted order and coefficient follow from Theorem 7.2. No new global curvature calculation is needed as \(k\) increases.

### Theorem 7.7 — Weighted initial-form calculus

To allow several competing leading monomials in one metric component, let every \(g_i\) be polyhomogeneous and fix a positive weight \(w\). Set

\[
\gamma_i=\operatorname{ord}_w(g_i),
\qquad
G_i=\operatorname{in}_w(g_i),
\]

and assume the front form \(G_i\) is nonzero at the positive approach ratio under consideration. Extend \(w\) by zero on tangential coordinates and call the coordinate weights \(\widetilde w_j\).

The \(j\)-th curvature channel obeys

\[
\operatorname{ord}_w(R_j)
\ge
-\gamma_j-2\widetilde w_j.
\tag{7.6}
\]

At the smallest candidate weight, the curvature front form is obtained by applying (2.2)–(2.3) to the weighted initial metric and retaining terms of that weight. If the sum is nonzero, it is \(\operatorname{in}_w(R)\). If it vanishes, the next filtered layer must be evaluated.

#### Proof

In the \(w\)-filtration, multiplication adds orders, inversion negates order when the initial form is nonzero, and \(\partial_j\) lowers order by at most \(\widetilde w_j\). Every term of \(\mathcal Q_j\) contains either one second derivative or two first derivatives in direction \(j\), so

\[
\operatorname{ord}_w(\mathcal Q_j)\ge-2\widetilde w_j.
\]

Multiplication by \(g_j^{-1}\) gives (7.6). Passing the rational differential expression to the associated graded object gives the front-form rule, unless the leading sum cancels. \(\square\)

### Consequence 7.8 — Exponents versus front metrics

- If every \(G_i\) is one monomial times a nonzero unit, the master quadrics determine the normal front coefficients.
- If a \(G_i\) contains several monomials, the exponent polygon still bounds the order, but the full front metric determines the coefficient.
- Ratio-dependent mixed coefficients therefore require the leading face polynomials. They are front-form data, not information contained in the exponent matrix alone.

---

## 8. Complete non-Kerr–Newman examples

### Example 8.1 — A two-face corner

Consider

\[
\boxed{
d\ell^2
=
x^{-2}y^{-2}(ds)^2+x^2(dx)^2+y^2(dy)^2.
}
\tag{8.1}
\]

The exponent rows are

\[
P_s=(-2,-2),
\qquad
P_x=(2,0),
\qquad
P_y=(0,2).
\]

The normal master coefficients are

\[
C_x=C_y=-6,
\]

and the tangential coefficient is zero because all units are constant. Thus

\[
\boxed{
R=-6x^{-4}-6y^{-4}.
}
\tag{8.2}
\]

For an independent check, put \(r=x^2/2\), \(t=y^2/2\). Then

\[
d\ell^2=(dr)^2+(dt)^2+w(r,t)^2(ds)^2,
\qquad
w=(4rt)^{-1/2}.
\]

For a one-dimensional warped fibre over a flat two-dimensional base,

\[
R=-2w^{-1}\Delta w
=
-\frac3{2r^2}-\frac3{2t^2}
=
-6x^{-4}-6y^{-4}.
\]

Along \(x=\rho\epsilon^a\), \(y=\epsilon^b\),

\[
\kappa_{(a,b)}(R)=\max(4a,4b).
\]

On the balanced face \(a=b\), the front coefficient is

\[
-6(\rho^{-4}+1),
\]

which never cancels for \(\rho>0\).

### Example 8.2 — Exact structural cancellation

For

\[
d\ell^2=(dr)^2+r^{4/(m+1)}\sum_{\alpha=1}^{m}(dy_\alpha)^2,
\]

Proposition 5.6 gives \(R\equiv0\). The nominal \(r^{-2}\) vertex is deleted by the master-quadric equation itself. This is the clean control showing why a zero vertex coefficient must not be reported as a pole.

---

## 9. Kerr–Newman specialization

The supplied inverse-channel Kerr–Newman work contributes the following already-derived local germs.

### 9.1 Single faces

| Divisor | Local type | Curvature result |
|---|---|---|
| \(T=0\) | generic quadratic collapse with finite transverse channels | order \(3\), coefficient from Theorem 5.2 |
| \(\Omega=0\) or \(J=0\) | parity-fixed inverse-channel face, \(m=2\) | order \(4\), coefficient \(-14/B_J\) |
| \(\Phi_e=0\) or \(Q=0\) | parity-fixed inverse-channel face, \(m=2\) | order \(4\), coefficient \(-14/B_Q\) |

### 9.2 Double-reflection corner

The sectorwise corner exponents are

\[
P_s=(-6,0),
\qquad
P_x=(2,-2),
\qquad
P_y=(-2,2).
\]

The normal vertices are

\[
V_x=(-4,2),
\qquad
V_y=(2,-4),
\]

and the raw master coefficients are

\[
A=-84,
\qquad
B=-12.
\]

Hence neither vertex cancels. Along \(x=\rho\epsilon^a\), \(y=\epsilon\),

\[
\boxed{
m(a)=\max(4a-2,\,4-2a).
}
\]

The minimum \(m(1)=2\) occurs on the balanced direction.

The balanced KN metric contains competing monomials whose leading face depends on the projective ratio \(\rho\). The vertices and wedge come from the exponent support. The nontrivial coefficient as a function of \(\rho\) comes from the full weighted initial metric through Theorem 7.7; it does not follow from the exponent matrix alone. This retains the supplied mixed-front result without pretending that two isolated face residues determine it.

The global KN curvature expression is not used by the general proofs.

---

## 10. Closed results, corrections, and retained content

### Closed here

1. A self-contained diagonal scalar-curvature identity.
2. An exact directional decomposition in arbitrary codimension.
3. The finite base-support curvature-valuation theorem.
4. The master quadric and normal-vertex proof.
5. Full proofs of generic order three and parity-fixed order four.
6. Proper-distance invariants.
7. Boundary-defining-function and normal-crossing robustness.
8. Codimension-two and codimension-\(k\) Newton rules.
9. The weighted initial-form extension.
10. A complete cancellation hierarchy.
11. Two exact non-KN controls.

### Corrections made explicitly

1. Deleting a zero outer vertex is not always the end: a non-monomial unit may have a nonzero inward jet.
2. Equal exponent vectors must be combined before a vertex is retained or deleted.
3. A Newton support function gives the generic ratio; a special ratio can cancel the full leading face.
4. “Finitely many derivatives” has no uniform depth after arbitrary cancellation.
5. Parity preservation is an odd coordinate condition, not merely the absence of one quadratic coefficient to all orders.
6. At a multi-monomial corner, exponents determine candidate order while the complete front metric determines the mixed coefficient.

### Retained without diminution

- the generic \(3\) law;
- the parity-fixed \(4\) law;
- the universal coefficient \(-m(m+5)/B\);
- the intrinsic gauge \(Rd^2=-m(m+5)/4\);
- the master quadric;
- the KN \(3/4/4\) face classification;
- the KN corner vertices, wedge, balanced order \(2\), and mixed front;
- the principle that local divisor data replace global curvature expansion.

---

## 11. Reproducibility recipe

An implementation needs:

1. the diagonal components \(g_i\);
2. the metric valuation matrix \(P\);
3. the leading unit or front-form germs;
4. coordinatewise first and second derivatives;
5. canonical grouping of equal exponent vectors;
6. inward unit jets only when an outer coefficient cancels;
7. the requested weight and approach ratio.

The calculation order is:

1. verify positivity on the declared germ;
2. form the directional channels \(\mathcal Q_j\);
3. apply the exact decomposition (3.2);
4. evaluate \(C_a(P)/h_a\);
5. group exponent collisions;
6. inspect inward jets if required;
7. select the Newton supporting face;
8. evaluate its front coefficient at the declared ratio;
9. report pole order and leading coefficient.

Numerical curvature is a downstream consistency check, not the source of the valuation.

---

## 12. Verification record

The companion file *verify_local_curvature_calculus.py* uses only the Python standard library and exact fractions. It performs:

- 75 independent rational two-jet comparisons between a direct Christoffel/Ricci contraction and the directional formula (2.3), in dimensions \(2,3,4\);
- a generic order-three fixture and a data-independence control;
- a generic leading-coefficient cancellation fixture;
- even parity fixtures with the \(x^{-3}\) channel forced to zero;
- exact pure parity models for \(m=1,\ldots,7\);
- scalar-flat master-quadric controls for \(m=1,\ldots,7\);
- algebraic equivalence of the master quadric and the closed corner coefficients;
- the synthetic corner \((-4,0),(0,-4)\);
- the KN raw coefficients \((-84,-12)\) and vertices \((-4,2),(2,-4)\);
- the second-order boundary-coordinate transformation.

All checks pass exactly; no floating tolerance and no external symbolic package is used.

---

## 13. Canonical theorem order

The shortest paper spine is:

1. directional-curvature identity, (2.2)–(2.3);
2. divisor-channel decomposition, (3.2);
3. master-quadric theorem, (4.2);
4. generic quadratic-collapse theorem, (5.4);
5. parity-fixed inverse-channel theorem, (5.5);
6. coordinate and intrinsic robustness, §6;
7. Newton valuation theorem, (7.1);
8. cancellation classification, Theorem 7.5;
9. weighted initial-form theorem, Theorem 7.7;
10. codimension-\(k\) corollary and examples.

The central object is the exact divisor-channel decomposition (3.2). The face laws and Newton calculus are its one- and many-divisor projections.
