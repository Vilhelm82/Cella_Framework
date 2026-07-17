# Generic Symmetric Monodromy of Weighted Multiquadratic Sums

## A complete all-\(k\) theorem with a Kummer–wreath lifting criterion

**Author:** Will Lloyd  
**Affiliation:** Lloyd Geometric Diagnostics Pty Ltd, Coffs Harbour, NSW, Australia  
**Date:** 2026-07-16  
**Status:** Completed theorem-and-proof paper, v1.0  
**Scope:** weighted-cover results in characteristic zero for arbitrary fixed
nonzero weights and \(k\ge3\); standalone Kummer criterion in
characteristic different from two

---

## Abstract

Fix \(k\ge 3\), distinct parameters \(a_1,\ldots,a_k\), and nonzero
weights \(c_1,\ldots,c_k\) over a field of characteristic zero.  On the
multiquadratic curve

\[
X_{\mathbf a}:\qquad w_i^2=u+a_i\quad(1\le i\le k),
\]

consider the weighted radical sum

\[
f_{\mathbf c}=\sum_{i=1}^k c_iw_i.
\]

We prove that, on a nonempty Zariski-open set of the parameters
\(\mathbf a\), this map has full symmetric monodromy.  Its degree is not
assumed: it is the exact pole count

\[
d(\mathbf c)
=
\#\left\{
\{\boldsymbol\eta,-\boldsymbol\eta\}:
\sum_i\eta_ic_i\ne0
\right\},
\]

and its geometric and generic arithmetic monodromy groups are both
\(S_{d(\mathbf c)}\).  The proof is uniform in \(k\) and in the nonzero
weight vector.  It identifies every possible ramification point, proves
generic nondegeneracy through the universal critical incidence, separates
critical values by the exact gradient

\[
d\,f_{\mathbf c}(P)
=
\frac12\sum_i\frac{c_i}{w_i(P)}\,da_i,
\]

and then uses connectedness plus simple local inertia to obtain the full
symmetric group.

The curve itself has

\[
g(X_{\mathbf a})=1+2^{k-2}(k-3),
\]

and the ramification divisor of \(f_{\mathbf c}\) has degree

\[
2^{k-1}(k-3)+2d(\mathbf c).
\]

For equal weights \(c_i=1\), the theorem gives the axial \(k\)-ellipse
degree

\[
\delta_k=
\begin{cases}
2^{k-1},&k\ \text{odd},\\[2mm]
2^{k-1}-\frac12\binom{k}{k/2},&k\ \text{even},
\end{cases}
\]

and hence the generic all-\(k\) group \(S_{\delta_k}\) for the DBP
mass-norm polynomial.  Finally, we prove a general conjugate
Kummer-module criterion: a valuation-parity matrix of full column rank
\(sd\) above any such base produces the exact closure group
\(C_2^s\wr S_{d(\mathbf c)}\).
This last statement is conditional only on displayed, falsifiable
valuation hypotheses; it does not assume them for a particular decorated
physical model.

---

## 1. The weighted family and the main result

### 1.1 Ground field and sign data

Let \(K\) be a field of characteristic zero and let \(\overline K\) be an
algebraic closure.  Geometric assertions are made after base change to
\(\overline K\).  Fix

\[
k\ge3,\qquad
\mathbf c=(c_1,\ldots,c_k)\in(K^\times)^k.
\]

Write

\[
\Sigma_k=\{\pm1\}^k/\{\boldsymbol\eta\sim-\boldsymbol\eta\}
\]

for the set of sign-pairs.  For
\([\boldsymbol\eta]\in\Sigma_k\), define

\[
A_{\boldsymbol\eta}(\mathbf c)
=\sum_{i=1}^k\eta_ic_i,
\qquad
B_{\boldsymbol\eta}(\mathbf a,\mathbf c)
=\sum_{i=1}^k\eta_ic_ia_i.
\]

Both equations \(A_{\boldsymbol\eta}=0\) and
\(B_{\boldsymbol\eta}=0\) are independent of the representative up to
an overall sign.  Put

\[
d(\mathbf c)
=
\#\left\{
[\boldsymbol\eta]\in\Sigma_k:
A_{\boldsymbol\eta}(\mathbf c)\ne0
\right\}.
\tag{1.1}
\]

### 1.2 The boundary-good parameter space

Let \(B_{\mathbf c}\subset\mathbb A^k_{\overline K}\) be the open set of
parameters \(\mathbf a=(a_1,\ldots,a_k)\) satisfying

\[
a_i\ne a_j\quad(i\ne j)
\tag{1.2}
\]

and

\[
B_{\boldsymbol\eta}(\mathbf a,\mathbf c)\ne0
\quad\text{whenever}\quad
A_{\boldsymbol\eta}(\mathbf c)=0.
\tag{1.3}
\]

This open set is nonempty: its complement is a finite union of proper
diagonals and hyperplanes over an infinite field.

For \(\mathbf a\in B_{\mathbf c}\), let \(X_{\mathbf a}\) be the smooth
projective curve with function field

\[
E_{\mathbf a}
=
\overline K(u)(w_1,\ldots,w_k),
\qquad
w_i^2=u+a_i.
\tag{1.4}
\]

Define

\[
f_{\mathbf c}:X_{\mathbf a}\longrightarrow\mathbb P^1,
\qquad
f_{\mathbf c}=\sum_{i=1}^k c_iw_i.
\tag{1.5}
\]

### Theorem 1.1 — weighted multiquadratic symmetric monodromy

For every \(k\ge3\) and every
\(\mathbf c\in(K^\times)^k\), there is a nonempty Zariski-open subset

\[
B_{\mathrm{GS}}(\mathbf c)\subset B_{\mathbf c}
\tag{1.6}
\]

such that, for every
\(\mathbf a\in B_{\mathrm{GS}}(\mathbf c)\):

1. \(X_{\mathbf a}\) is connected and
   \[
   g(X_{\mathbf a})=1+2^{k-2}(k-3);
   \tag{1.7}
   \]
2. the degree of \(f_{\mathbf c}\) is \(d(\mathbf c)\);
3. all ramification of \(f_{\mathbf c}\) occurs at finite points with
   every \(w_i\ne0\);
4. every ramification point is simple;
5. distinct ramification points have distinct branch values;
6. the geometric monodromy group is
   \[
   \operatorname{Mon}_{\mathrm{geom}}(f_{\mathbf c})
   \cong S_{d(\mathbf c)};
   \tag{1.8}
   \]
7. the ramification divisor has degree
   \[
   \deg R_{f_{\mathbf c}}
   =
   2^{k-1}(k-3)+2d(\mathbf c).
   \tag{1.9}
   \]

The corresponding generic arithmetic group over
\(K(\mathbf a)(y)\), where \(y=f_{\mathbf c}\), is also
\(S_{d(\mathbf c)}\).

The theorem is generic, not universal.  Section 8 gives exact points of
\(B_{\mathbf c}\) where critical values collide or critical points
degenerate.

---

## 2. The multiquadratic field and its primitive weighted sum

### Lemma 2.1 — independence of the radical square classes

If the \(a_i\) are pairwise distinct, then the classes of

\[
u+a_1,\ldots,u+a_k
\]

are linearly independent in
\(\overline K(u)^\times/\overline K(u)^{\times2}\).

#### Proof

Suppose

\[
\prod_{i=1}^k(u+a_i)^{e_i}=r(u)^2,
\qquad e_i\in\{0,1\}.
\tag{2.1}
\]

At the discrete valuation \(v_j\) associated with \(u=-a_j\), the
left-hand side has valuation \(e_j\), because every factor with
\(i\ne j\) is a unit there.  The right-hand side has even valuation.
Thus \(e_j=0\) for every \(j\).  Hence no nontrivial square-class
relation exists. \(\square\)

### Corollary 2.2 — the signed cover

The extension \(E_{\mathbf a}/\overline K(u)\) has degree \(2^k\) and

\[
H:=\operatorname{Gal}(E_{\mathbf a}/\overline K(u))
\cong(C_2)^k,
\tag{2.2}
\]

where the \(i\)-th standard generator changes the sign of \(w_i\) and
fixes every other \(w_j\).

#### Proof

Adjoining independent square classes gives a multiquadratic extension of
degree \(2^k\).  The \(2^k\) independent sign changes exhaust its
automorphisms. \(\square\)

### Proposition 2.3 — the weighted sum is primitive

If every \(c_i\ne0\), as in the standing hypothesis, then

\[
\overline K(u,f_{\mathbf c})=E_{\mathbf a}.
\tag{2.3}
\]

Equivalently, the stabilizer of \(f_{\mathbf c}\) in \(H\) is trivial.

#### Proof

Let \(\tau_D\in H\) flip precisely the nonempty set
\(D\subset\{1,\ldots,k\}\).  If \(\tau_D\) fixed \(f_{\mathbf c}\), then

\[
0=f_{\mathbf c}-\tau_D(f_{\mathbf c})
=2\sum_{i\in D}c_iw_i,
\]

so

\[
\sum_{i\in D}c_iw_i=0.
\tag{2.4}
\]

Choose \(j\in D\) and apply the individual sign flip \(\tau_{\{j\}}\)
to (2.4).  Subtracting the transformed relation from (2.4) gives

\[
2c_jw_j=0,
\]

which is impossible in characteristic zero because \(c_j\ne0\) and
\(w_j\ne0\) in the function field.  Therefore no nonidentity element of
\(H\) fixes \(f_{\mathbf c}\).  By the Galois correspondence,
\(\overline K(u,f_{\mathbf c})=E_{\mathbf a}\). \(\square\)

### Corollary 2.4 — the weighted norm curve

The signed norm

\[
\Phi_{\mathbf a,\mathbf c}(u,y)
=
\prod_{\boldsymbol\eta\in\{\pm1\}^k}
\left(
y-\sum_i\eta_ic_iw_i
\right)
\tag{2.5}
\]

lies in \(\overline K[u,y]\), is irreducible in
\(\overline K(u)[y]\), and the normalization of its plane curve has
function field \(E_{\mathbf a}\) under \(y=f_{\mathbf c}\).

#### Proof

The product is invariant under every sign change in \(H\), so its
coefficients lie in \(\overline K(u)\).  Each \(w_i\) is integral over
\(\overline K[u]\); hence the product is integral over
\(\overline K[u]\).  Since \(\overline K[u]\) is integrally closed, its
coefficients lie in \(\overline K[u]\).

The \(H\)-orbit of \(f_{\mathbf c}\) has \(2^k\) elements by Proposition
2.3.  Therefore (2.5) is its minimal polynomial over
\(\overline K(u)\), and is irreducible.  The function field obtained by
imposing \(y=f_{\mathbf c}\) is
\(\overline K(u,f_{\mathbf c})=E_{\mathbf a}\), which identifies the
normalization. \(\square\)

---

## 3. Geometry of the signed cover

Let

\[
\pi:X_{\mathbf a}\longrightarrow\mathbb P^1_u
\tag{3.1}
\]

be the degree-\(2^k\) signed cover.

### Lemma 3.1 — finite branch points of \(\pi\)

Above each \(u=-a_i\), there are \(2^{k-1}\) points, each with
ramification index two.  There is no other finite ramification.

#### Proof

At \(u=-a_i\), the function \(w_i\) is a uniformizer and

\[
u+a_i=w_i^2.
\]

For \(j\ne i\), the value \(u+a_j=a_j-a_i\) is a nonzero unit, and its
square root has two independent residue choices.  Thus there are
\(2^{k-1}\) points above \(u=-a_i\), each with index two.

Away from the \(k\) zeros of the radicands, all \(u+a_i\) are units with
even valuation; the multiquadratic extension is unramified there.
\(\square\)

### Lemma 3.2 — places above infinity

There are \(2^{k-1}\) points above \(u=\infty\), each with ramification
index two.  They are naturally indexed by
\(\Sigma_k=\{\pm1\}^k/\pm1\).

#### Proof

Put \(s=u^{-1}\).  In the completion \(\overline K((s))\),

\[
w_i=s^{-1/2}(1+a_is)^{1/2}.
\]

After adjoining \(t=s^{1/2}\), the unit
\((1+a_it^2)^{1/2}\) belongs to \(\overline K[[t]]^\times\).  All
radicals therefore share the single ramified parameter \(t\); their
relative signs are independent.  Replacing \(t\) by \(-t\) changes every
sign simultaneously, so the distinct places are indexed by sign vectors
modulo global sign.  Hence there are \(2^{k-1}\) such places, all of
index two. \(\square\)

### Proposition 3.3 — genus

For every \(\mathbf a\) with pairwise distinct coordinates,

\[
g(X_{\mathbf a})=1+2^{k-2}(k-3).
\tag{3.2}
\]

#### Proof

The map \(\pi\) has degree \(2^k\).  There are \(k+1\) branch values:
\(-a_1,\ldots,-a_k,\infty\).  Above each are \(2^{k-1}\) points of
index two, so each branch value contributes \(2^{k-1}\) to the
ramification degree.  Riemann–Hurwitz gives

\[
\begin{aligned}
2g(X_{\mathbf a})-2
&=2^k(-2)+(k+1)2^{k-1}\\
&=2^{k-1}(k-3).
\end{aligned}
\]

Solving for \(g\) yields (3.2). \(\square\)

---

## 4. Boundary behavior and the exact degree of \(f_{\mathbf c}\)

### Lemma 4.1 — expansion at infinity

At the infinity place represented by
\([\boldsymbol\eta]\in\Sigma_k\), choose \(t\) so that \(u=t^{-2}\)
and

\[
w_i
=
\eta_it^{-1}
\left(
1+\frac{a_i}{2}t^2-\frac{a_i^2}{8}t^4+O(t^6)
\right).
\]

Then

\[
f_{\mathbf c}
=
A_{\boldsymbol\eta}t^{-1}
+\frac12B_{\boldsymbol\eta}t
-\frac18C_{\boldsymbol\eta}t^3
+O(t^5),
\tag{4.1}
\]

where

\[
C_{\boldsymbol\eta}
=\sum_i\eta_ic_ia_i^2.
\]

Consequently:

- if \(A_{\boldsymbol\eta}\ne0\), then \(f_{\mathbf c}\) has a simple
  pole at this place;
- if \(A_{\boldsymbol\eta}=0\) and
  \(B_{\boldsymbol\eta}\ne0\), then \(f_{\mathbf c}\) has a simple
  zero there.

In either case the map \(f_{\mathbf c}\) is unramified at the place.

#### Proof

The binomial expansion

\[
(1+a_it^2)^{1/2}
=
1+\frac{a_i}{2}t^2-\frac{a_i^2}{8}t^4+O(t^6)
\]

inserted into \(w_i^2=t^{-2}+a_i\) gives (4.1) after summing with
weights.  A function with a simple pole or simple zero is a local
parameter on the target, so the local degree is one. \(\square\)

### Lemma 4.2 — radical contacts are unramified

The map \(f_{\mathbf c}\) is unramified at every point above
\(u=-a_j\).

#### Proof

Use \(\tau=w_j\) as local parameter, so

\[
u=\tau^2-a_j.
\]

For \(i\ne j\), the function \(w_i\) is an analytic unit and an even
function of \(\tau\).  Hence

\[
f_{\mathbf c}
=
f_{\mathbf c}(0)+c_j\tau+O(\tau^2).
\]

The linear coefficient \(c_j\) is nonzero, so the local degree is one.
\(\square\)

### Proposition 4.3 — exact degree and ramification locus

For every \(\mathbf a\in B_{\mathbf c}\),

\[
\deg(f_{\mathbf c})=d(\mathbf c).
\tag{4.2}
\]

Every ramification point is finite, has \(w_i\ne0\) for all \(i\), and
satisfies

\[
C_1:=\sum_{i=1}^k\frac{c_i}{w_i}=0.
\tag{4.3}
\]

#### Proof

The degree of a nonconstant function on a smooth projective curve is the
degree of its pole divisor.  By Lemma 4.1, there is one simple pole for
each sign-pair with \(A_{\boldsymbol\eta}\ne0\), and no other pole.
Their number is \(d(\mathbf c)\), proving (4.2).

Lemmas 4.1 and 4.2 exclude infinity and the radical contacts from the
ramification locus.  At every remaining finite point, \(u\) is a local
parameter and

\[
\frac{df_{\mathbf c}}{du}
=
\frac12\sum_i\frac{c_i}{w_i}
=\frac12C_1.
\tag{4.4}
\]

Thus ramification occurs exactly where (4.3) holds. \(\square\)

### Corollary 4.4 — total ramification count

For every \(\mathbf a\in B_{\mathbf c}\), the ramification divisor,
counted with multiplicity, has degree

\[
\deg R_{f_{\mathbf c}}
=
2^{k-1}(k-3)+2d(\mathbf c).
\tag{4.5}
\]

#### Proof

Apply Riemann–Hurwitz to the degree-\(d(\mathbf c)\) map
\(f_{\mathbf c}:X_{\mathbf a}\to\mathbb P^1\):

\[
\deg R_{f_{\mathbf c}}
=
2g(X_{\mathbf a})-2+2d(\mathbf c).
\]

Insert Proposition 3.3. \(\square\)

### Corollary 4.5 — irreducibility in the \(u\)-direction

The element \(u\) has degree \(d(\mathbf c)\) over
\(\overline K(f_{\mathbf c})\).  Equivalently, the relation
\(\Phi_{\mathbf a,\mathbf c}(u,y)=0\), viewed as a polynomial in \(u\)
over \(\overline K(y)\), is irreducible of degree \(d(\mathbf c)\).

#### Proof

Proposition 2.3 gives

\[
E_{\mathbf a}
=\overline K(u,f_{\mathbf c})
=\overline K(f_{\mathbf c})(u).
\]

The degree
\([E_{\mathbf a}:\overline K(f_{\mathbf c})]\) equals the degree of the
map \(f_{\mathbf c}\), which is \(d(\mathbf c)\) by Proposition 4.3.
Therefore the minimal polynomial of \(u\) has degree \(d(\mathbf c)\).
Because \(\Phi_{\mathbf a,\mathbf c}\) is monic in \(y\), it is primitive
over the UFD \(\overline K[u]\).  Its irreducibility in
\(\overline K(u)[y]\) from Corollary 2.4 and Gauss's lemma therefore make
it irreducible in \(\overline K[u,y]\).  Regarding the same polynomial as
an element of \(\overline K[y][u]\), it is again primitive—otherwise a
nonunit content would be a factor in the bivariate polynomial ring—so a
second application of Gauss's lemma makes it irreducible in
\(\overline K(y)[u]\).  It is consequently the minimal relation of \(u\),
up to a nonzero scalar, and its \(u\)-degree is \(d(\mathbf c)\). \(\square\)

---

## 5. The universal critical incidence

The remaining task is to prove that the critical points are generically
simple and have distinct values.  The word “generically” must be earned:
Section 8 exhibits failures inside the boundary-good locus.

### 5.1 The proper relative ramification scheme

Let \(\mathcal X\to B_{\mathbf c}\) be the relative projective curve
obtained by normalizing
\(\mathbb P^1_u\times B_{\mathbf c}\) in the multiquadratic extension

\[
w_i^2=u+a_i.
\tag{5.1}
\]

The base and \(\mathbb P^1_u\times B_{\mathbf c}\) are excellent
Noetherian schemes, so normalization in this finite function-field
extension is finite.  Hence \(\mathcal X\) is projective over
\(B_{\mathbf c}\).  It is in fact smooth, as the following local checks
show.

On the affine chart the family is smooth.  Indeed, the equations
\(w_i^2-u-a_i=0\) have relative Jacobian rows

\[
(-1,0,\ldots,2w_i,\ldots,0).
\]

At most one \(w_i\) can vanish in a fiber because the \(a_i\) are
distinct, so these rows have full rank.

At infinity, work in the completed normalization over \(s=u^{-1}=0\).
At any geometric base point and any chosen place above infinity, there is
a uniformizer \(t\) with \(t^2=s\): after choosing the unit square root
in the completion, one may take

\[
t=\frac{\sqrt{1+a_1s}}{w_1}.
\]

Set \(z_i=tw_i\).  Then

\[
z_i^2=1+a_it^2.
\]

The equations \(z_i^2=1+a_it^2\) have, for every sign choice
\(z_i(0)=\eta_i\), unique solutions in the completed ring by Hensel's
lemma, since \(2\eta_i\) is invertible.  The completed local ring at a
base point \(b\) is therefore
\(\widehat{\mathcal O}_{B_{\mathbf c},b}[[t]]\).  Replacing
\((t,\boldsymbol\eta)\) by \((-t,-\boldsymbol\eta)\) describes the same
place, so the boundary branches are indexed by sign-pairs.  The completed
local criterion for smoothness now proves that the normalization is
smooth at infinity as well as on the finite chart.

The rational function \(f_{\mathbf c}\) extends to a morphism

\[
F:\mathcal X\longrightarrow
\mathbb P^1_y\times B_{\mathbf c}.
\tag{5.2}
\]

Indeed, the displayed infinity charts and Lemma 4.1 show that it has
either a simple pole or a regular simple zero on every boundary branch.
Define the relative ramification scheme \(\mathcal R\) as the zero scheme
of the homomorphism of line bundles

\[
dF:
F^*\Omega^1_{(\mathbb P^1_y\times B_{\mathbf c})/B_{\mathbf c}}
\longrightarrow
\Omega^1_{\mathcal X/B_{\mathbf c}}.
\tag{5.3}
\]

On any finite chart, this is the zero scheme of
\(d_{\mathcal X/B_{\mathbf c}}f_{\mathbf c}\); the line-bundle
formulation also defines it correctly at poles.

### Proposition 5.1 — finiteness of the critical scheme

The morphism

\[
\mathcal R\longrightarrow B_{\mathbf c}
\tag{5.4}
\]

is finite and surjective.  Its affine realization is

\[
\widetilde{\mathcal C}
=
\left\{
(u,w_1,\ldots,w_k):
w_i\ne0,\ 
\sum_i\frac{c_i}{w_i}=0
\right\},
\tag{5.5}
\]

with parameter map

\[
q(u,\mathbf w)_i=w_i^2-u=a_i.
\tag{5.6}
\]

Precisely,

\[
\mathcal C
=q^{-1}(B_{\mathbf c})
\subset\widetilde{\mathcal C}
\tag{5.7}
\]

is the affine realization of \(\mathcal R\).

#### Proof

The scheme \(\mathcal R\) is closed in the proper family
\(\mathcal X\), hence is proper over \(B_{\mathbf c}\).  Lemmas 4.1 and
4.2 show that it misses infinity and every \(w_i=0\), so its points are
exactly the affine points (5.7).

This identification is scheme-theoretic.  On the chart where every
\(w_i\ne0\), the coordinate \(u\) is relative étale and \(du\) trivializes
\(\Omega^1_{\mathcal X/B_{\mathbf c}}\).  Equation (4.4) gives

\[
d_{\mathcal X/B_{\mathbf c}}f_{\mathbf c}
=\frac12C_1\,du.
\]

Therefore the zero scheme of \(dF\) on this chart is exactly
\(V(C_1)=\mathcal C\), with its displayed scheme structure.

On each fiber, \(f_{\mathbf c}\) is a nonconstant separable function on
a smooth projective curve.  Its ramification divisor is finite.  It is
nonempty because (4.5) is positive for \(k\ge3\).  Thus (5.4) is
quasi-finite and surjective.  A proper quasi-finite morphism is finite.
\(\square\)

### Proposition 5.2 — irreducibility of the critical incidence

The schemes \(\widetilde{\mathcal C}\) and \(\mathcal C\) are smooth
and irreducible of dimension \(k\).

#### Proof

Put

\[
x_i=\frac{c_i}{w_i}\in\mathbb G_m.
\]

Then (5.5) becomes

\[
\widetilde{\mathcal C}
\cong
\mathbb A^1_u\times
\left\{
(x_1,\ldots,x_k)\in(\mathbb G_m)^k:
\sum_i x_i=0
\right\}.
\tag{5.8}
\]

The hyperplane \(\sum x_i=0\), intersected with the torus, is a nonempty
open subset of an affine \((k-1)\)-space: solve for \(x_k\) and remove
the coordinate hyperplanes together with
\(\sum_{i<k}x_i=0\).  It is smooth and irreducible of dimension
\(k-1\).  Thus \(\widetilde{\mathcal C}\) is smooth and irreducible of
dimension \(k\).  By Proposition 5.1,
\(\mathcal C=q^{-1}(B_{\mathbf c})\) is nonempty; it is also open in
\(\widetilde{\mathcal C}\).  It therefore has the same properties and
dimension. \(\square\)

---

## 6. Generic folds and separation of branch values

### 6.1 Nondegeneracy

At a critical point, differentiate (4.4):

\[
\frac{d^2f_{\mathbf c}}{du^2}
=
-\frac14
\sum_i\frac{c_i}{w_i^3}.
\tag{6.1}
\]

Set

\[
C_3=\sum_i\frac{c_i}{w_i^3}.
\tag{6.2}
\]

A critical point is degenerate exactly when \(C_1=C_3=0\).

### Lemma 6.1 — \(C_3\) does not vanish identically on \(\mathcal C\)

The locus

\[
\mathcal D=\{C_1=C_3=0\}
\tag{6.3}
\]

is a proper closed subset of \(\mathcal C\), of dimension at most
\(k-1\).

#### Proof

In the coordinates \(x_i=c_i/w_i\), one has

\[
C_1=\sum_i x_i,
\qquad
C_3=\sum_i\frac{x_i^3}{c_i^2}.
\tag{6.4}
\]

Suppose \(C_3\) vanished identically on \(\sum_i x_i=0\).  Then the
linear form \(L=\sum_i x_i\) would divide the homogeneous cubic

\[
Q=\sum_i\frac{x_i^3}{c_i^2}.
\]

Choose three distinct indices \(p,q,r\), set all other variables to
zero, and substitute \(x_r=-x_p-x_q\).  The coefficient of
\(x_p^2x_q\) in the resulting polynomial is

\[
-\frac{3}{c_r^2},
\]

which is nonzero in characteristic zero.  Hence \(Q\) is not divisible
by \(L\).  Therefore \(C_3\) is a nonzero regular function on
\(\widetilde{\mathcal C}\).  Its restriction to the nonempty open
\(\mathcal C\) is still nonzero, so its zero locus there has dimension at
most \(k-1\). \(\square\)

### Proposition 6.2 — a nonempty open with only simple folds

There is a nonempty Zariski-open

\[
B_{\mathrm{nd}}(\mathbf c)\subset B_{\mathbf c}
\tag{6.5}
\]

such that every ramification point above it is simple.  Over this open,
\(\mathcal R\to B_{\mathrm{nd}}(\mathbf c)\) is finite étale.

#### Proof

By Proposition 5.1, \(q:\mathcal C\to B_{\mathbf c}\) is finite.
Consequently \(q(\mathcal D)\) is closed.  Lemma 6.1 gives

\[
\dim q(\mathcal D)\le k-1<\dim B_{\mathbf c},
\]

so its complement \(B_{\mathrm{nd}}(\mathbf c)\) is nonempty and open.

At a point outside \(\mathcal D\), equation (6.1) shows that the zero
of \(df_{\mathbf c}/du\) is simple, hence the map has ramification
index two.  For completeness, let a tangent vector to \(\mathcal C\)
lie in the kernel of \(dq\).  From
\(a_i=w_i^2-u\),

\[
2w_i\,\delta w_i-\delta u=0,
\qquad
\delta w_i=\frac{\delta u}{2w_i}.
\]

Tangency to \(C_1=0\) gives

\[
0=\delta C_1
=-\sum_i\frac{c_i\,\delta w_i}{w_i^2}
=-\frac{\delta u}{2}C_3.
\]

Since \(C_3\ne0\), one has \(\delta u=0\), hence every
\(\delta w_i=0\).  Thus \(dq\) has zero kernel.  Proposition 5.2 says
that \(\mathcal C\) and \(B_{\mathbf c}\) are smooth \(k\)-folds, so
\(dq\) is an isomorphism on tangent spaces.  The Jacobian criterion makes
\(q\) étale at every point above \(B_{\mathrm{nd}}(\mathbf c)\).  It is
already finite by Proposition 5.1, hence finite étale. \(\square\)

### 6.2 Variation of a critical value

Étale-locally on \(B_{\mathrm{nd}}(\mathbf c)\), choose a critical
section

\[
P(\mathbf a)
=(u(\mathbf a),w_1(\mathbf a),\ldots,w_k(\mathbf a)).
\]

Differentiating \(w_i^2=u+a_i\) gives

\[
2w_i\,dw_i=du+da_i.
\]

At a critical point,

\[
\begin{aligned}
d\bigl(f_{\mathbf c}(P)\bigr)
&=\sum_i c_i\,dw_i\\
&=\frac12\left(\sum_i\frac{c_i}{w_i}\right)du
  +\frac12\sum_i\frac{c_i}{w_i}\,da_i\\
&=\frac12\sum_i\frac{c_i}{w_i(P)}\,da_i.
\end{aligned}
\tag{6.6}
\]

This exact covector is the separation mechanism.

### Proposition 6.3 — generic critical-value separation

There is a nonempty Zariski-open

\[
B_{\mathrm{GS}}(\mathbf c)
\subset B_{\mathrm{nd}}(\mathbf c)
\tag{6.7}
\]

such that distinct critical points have distinct critical values.

#### Proof

Form the off-diagonal ordered-pair scheme

\[
\mathcal P
=
\left(
\mathcal R\times_{B_{\mathrm{nd}}}\mathcal R
\right)\setminus\Delta.
\tag{6.8}
\]

The diagonal of a finite étale morphism is open and closed, so its
complement \(\mathcal P\) is again finite étale over
\(B_{\mathrm{nd}}(\mathbf c)\).  Let its two
critical points be

\[
P=(u,w_1,\ldots,w_k),
\qquad
Q=(v,z_1,\ldots,z_k),
\]

and put

\[
h=f_{\mathbf c}(P)-f_{\mathbf c}(Q).
\]

Equation (6.6) gives

\[
dh
=
\frac12\sum_i
c_i\left(\frac1{w_i}-\frac1{z_i}\right)da_i.
\tag{6.9}
\]

Because \(\mathcal P\) is étale over the parameter space, the
\(da_i\) form a cotangent basis.  If \(dh=0\), every coefficient in
(6.9) vanishes.  Since \(c_i\ne0\), this gives \(w_i=z_i\) for every
\(i\).  Then

\[
u+a_i=w_i^2=z_i^2=v+a_i
\]

forces \(u=v\), so \(P=Q\), contradicting the removal of the diagonal.
Thus \(dh\) is nowhere zero on \(\mathcal P\).

It follows that \(h\) is nonconstant on every irreducible component of
\(\mathcal P\).  Its zero locus is therefore either empty or has
dimension at most \(k-1\).  Since
\(\mathcal P\to B_{\mathrm{nd}}(\mathbf c)\) is finite, the image of
this zero locus is closed and proper.  Remove the finite union of these
images.  The complement is the required nonempty open
\(B_{\mathrm{GS}}(\mathbf c)\). \(\square\)

---

## 7. Full symmetric monodromy

### Theorem 7.1 — geometric group

For every \(\mathbf a\in B_{\mathrm{GS}}(\mathbf c)\),

\[
\operatorname{Mon}_{\mathrm{geom}}(f_{\mathbf c})
=S_{d(\mathbf c)}.
\tag{7.1}
\]

#### Proof

The curve \(X_{\mathbf a}\) is connected, so the monodromy action on a
generic fiber is transitive.  By Propositions 6.2 and 6.3, each branch
value contains exactly one ramification point of index two.  Its local
inertia is therefore a single transposition.

The geometric monodromy group is generated by the inertia groups at the
branch values.  Indeed, quotienting the Galois closure by the normal
subgroup generated by all those inertia groups would produce a finite
everywhere-étale cover of \(\mathbb P^1\); over an algebraically closed
field of characteristic zero, such a connected cover is trivial.  Thus
the group is transitive and generated by transpositions.

Make a graph whose vertices are the \(d(\mathbf c)\) sheets and whose
edges are the generating transpositions.  The orbits of the generated
group are exactly the connected components of this graph.  Transitivity
makes the graph connected, and the edge transpositions of a connected
graph generate the full symmetric group.  Hence the monodromy group is
\(S_{d(\mathbf c)}\). \(\square\)

### Corollary 7.2 — generic arithmetic group

Let the \(a_i\) be algebraically independent over a characteristic-zero
ground field containing the \(c_i\), and let \(y=f_{\mathbf c}\).  The
Galois group of the degree-\(d(\mathbf c)\) minimal polynomial of \(u\)
over

\[
K(a_1,\ldots,a_k)(y)
\]

is \(S_{d(\mathbf c)}\).

#### Proof

All constructions and bad-locus images used to define the good open are
defined over \(K\), and the generic point lies in that nonempty open.
After base change to \(\overline K(a_1,\ldots,a_k)\), Theorem 7.1
therefore gives the geometric generic group \(S_{d(\mathbf c)}\).  The geometric
group is a normal subgroup of the arithmetic generic group, while the
arithmetic group is itself a subgroup of \(S_{d(\mathbf c)}\) through
its action on the \(d(\mathbf c)\) roots.  Hence it is squeezed between
\(S_{d(\mathbf c)}\) and itself. \(\square\)

This completes the proof of Theorem 1.1.

---

## 8. Sharpness: three exact exceptional configurations

The removed loci are mathematical, not editorial.  The following examples
show that the boundary-good space is larger than the simple-branching
space.

### Example 8.1 — two simple critical points with one critical value

Take \(k=3\), \(c_1=c_2=c_3=1\), and let
\(\zeta^3=1\) with \(\zeta\ne1\).  Put

\[
u=0,\qquad
(w_1,w_2,w_3)=(1,\zeta,\zeta^2),
\qquad
(a_1,a_2,a_3)=(1,\zeta^2,\zeta).
\]

The \(a_i\) are distinct.  Moreover,

\[
C_1
=
1+\zeta^2+\zeta
=0,
\]

while

\[
C_3
=
1+\zeta^{-3}+\zeta^{-6}
=3\ne0.
\]

Thus \(P=(1,\zeta,\zeta^2)\) is a simple critical point.  The globally
opposite point \(-P\) is another simple critical point, but

\[
f(P)=1+\zeta+\zeta^2=0=f(-P).
\]

For odd \(k\) there are no balanced infinity classes, so this parameter
point lies in \(B_{\mathbf 1}\).  It is excluded only by the
critical-value collision locus.

### Example 8.2 — a degenerate critical point

Take \(k=5\), equal weights, and

\[
(x_1,\ldots,x_5)=(-20,-14,-1,17,18).
\]

Then

\[
\sum_i x_i=0
\]

and

\[
\sum_i x_i^3
=
-8000-2744-1+4913+5832
=0.
\]

Set

\[
u=0,\qquad
w_i=x_i^{-1},\qquad
a_i=x_i^{-2}.
\]

The absolute values \(20,14,1,17,18\) are distinct, so the \(a_i\) are
pairwise distinct.  Since \(x_i=1/w_i\),

\[
C_1=\sum_i\frac1{w_i}=0,
\qquad
C_3=\sum_i\frac1{w_i^3}=0.
\]

This is a degenerate critical point inside the boundary-good locus.

### Example 8.3 — why the balanced first moment is required

Take \(k=4\), equal weights,

\[
\boldsymbol\eta=(1,1,-1,-1),
\qquad
\mathbf a=(1,4,2,3).
\]

Then

\[
A_{\boldsymbol\eta}=1+1-1-1=0,
\]

\[
B_{\boldsymbol\eta}=1+4-2-3=0,
\]

but

\[
C_{\boldsymbol\eta}=1^2+4^2-2^2-3^2=4.
\]

The expansion (4.1) becomes

\[
f_{\mathbf1}
=-\frac12t^3+O(t^5).
\]

Thus the infinity place has local degree three.  Condition (1.3)
excludes exactly this higher boundary ramification.

---

## 9. The equal-weight axial specialization

Set

\[
c_1=\cdots=c_k=1.
\]

Then

\[
A_{\boldsymbol\eta}=\sum_i\eta_i.
\]

If \(k\) is odd, no sign vector is balanced, so every one of the
\(2^{k-1}\) sign-pairs contributes a pole.  If \(k\) is even, there are
\(\binom{k}{k/2}\) balanced sign vectors and hence
\(\frac12\binom{k}{k/2}\) balanced sign-pairs.  Therefore

\[
d(\mathbf1)
=\delta_k
=
\begin{cases}
2^{k-1},&k\text{ odd},\\[2mm]
2^{k-1}-\dfrac12\binom{k}{k/2},&k\text{ even}.
\end{cases}
\tag{9.1}
\]

### Corollary 9.1 — all-\(k\) axial mass-norm group

Let \(N_1,\ldots,N_k\) be algebraically independent over \(\mathbb Q\),
and set

\[
a_i=N_i^2,\qquad
w_i^2=u+N_i^2,\qquad
4M=\sum_iw_i.
\]

Let

\[
N_k(u;M)
=
\prod_{\boldsymbol\eta\in\{\pm1\}^k}
\left(
4M-\sum_i\eta_iw_i
\right).
\tag{9.2}
\]

For every \(k\ge3\), the splitting field of \(N_k(u;M)\), viewed as a
polynomial in \(u\) over
\(\mathbb Q(N_1,\ldots,N_k)(M)\), has Galois group

\[
\operatorname{Gal}_{u}
\left(N_k/\mathbb Q(N_1,\ldots,N_k)(M)\right)
\cong S_{\delta_k}.
\tag{9.3}
\]

#### Proof

Equation (9.2) is the equal-weight instance of (2.5), with target
coordinate \(y=4M\).  The parameter substitution

\[
\mathbb Q(a_1,\ldots,a_k)
\subset
\mathbb Q(N_1,\ldots,N_k),
\qquad
a_i=N_i^2,
\]

is finite algebraic.  The two parameter fields therefore have the same
algebraic closure inside a chosen common closure; write

\[
\Omega
:=
\overline{\mathbb Q(a_1,\ldots,a_k)}
=
\overline{\mathbb Q(N_1,\ldots,N_k)}.
\]

Equivalently, the
dominant finite parameter map
\((N_i)\mapsto(N_i^2)\) pulls the nonempty good open
\(B_{\mathrm{GS}}(\mathbf1)\) back to a nonempty open.  In particular,
for every balanced sign vector the form
\(\sum_i\eta_iN_i^2\) is nonzero at the generic point.

The geometric generic group over \(\Omega(M)\) remains
\(S_{\delta_k}\) by Theorem 7.1.  The arithmetic group over
\(\mathbb Q(N_1,\ldots,N_k)(M)\) contains that geometric group and is a
subgroup of the same symmetric group, so it is \(S_{\delta_k}\).
Corollary 4.5, applied after this parameter base change, gives
irreducibility in \(u\), and (9.1) gives the degree \(\delta_k\).
\(\square\)

The first four cases are:

| \(k\) | \(\delta_k\) | \(g(X_{\mathbf a})\) | \(\deg R_f\) | generic group |
|---:|---:|---:|---:|---|
| 3 | 4 | 1 | 8 | \(S_4\) |
| 4 | 5 | 5 | 18 | \(S_5\) |
| 5 | 16 | 17 | 64 | \(S_{16}\) |
| 6 | 22 | 49 | 140 | \(S_{22}\) |

The previously computed cases \(k=3,4,5,6\) are therefore independent
arithmetic checks, not load-bearing steps in the all-\(k\) proof.

---

## 10. Conjugate Kummer modules above the symmetric base

The base theorem determines the permutation quotient of a decorated
cover.  The kernel is a separate square-class problem.  This section
states and proves the exact reusable criterion.

### 10.1 Setup

Let \(F\) be a field of characteristic different from two.  Let
\(K_0/F\) be a finite separable extension of degree \(d\), let \(E/F\)
be its normal closure, and put

\[
G=\operatorname{Gal}(E/F),
\qquad
I=\operatorname{Hom}_F(K_0,E).
\]

The action of \(G\) on \(I\) is by postcomposition,
\(g(i)=g\circ i\), and is transitive.  Choose

\[
r_1,\ldots,r_s\in K_0^\times
\]

and write

\[
r_{\alpha,i}=i(r_\alpha)
\qquad
(1\le\alpha\le s,\ i\in I).
\]

Define the decorated sheet field

\[
H_{\mathrm{dec}}
=K_0(\sqrt{r_1},\ldots,\sqrt{r_s})
\]

and

\[
L
=
E\left(
\sqrt{r_{\alpha,i}}:
1\le\alpha\le s,\ i\in I
\right).
\tag{10.1}
\]

All fields are taken inside one fixed separable closure of \(F\).  For the
distinguished inclusion \(K_0\hookrightarrow E\), choose the displayed
square roots compatibly, so \(H_{\mathrm{dec}}\subset L\).

Let

\[
V=\mathbb F_2^s\otimes_{\mathbb F_2}\mathbb F_2[I]
\]

with basis \(e_{\alpha,i}\), and define

\[
\theta:V\longrightarrow E^\times/E^{\times2},
\qquad
\theta(e_{\alpha,i})=[r_{\alpha,i}].
\tag{10.2}
\]

Put

\[
R=\ker\theta,
\qquad
W=\operatorname{im}\theta=V/R.
\tag{10.3}
\]

Give \(V\) the permutation action
\(g(e_{\alpha,i})=e_{\alpha,g(i)}\).  The map \(\theta\) is
\(G\)-equivariant, so \(R\) is \(G\)-stable.  Thus \(R\) is the module
of multiplicative square relations and \(W\) is the concrete conjugate
Kummer submodule of \(E^\times/E^{\times2}\).

### Theorem 10.1 — normal closure and Kummer kernel

The field \(L\) is the normal closure of \(H_{\mathrm{dec}}/F\), and
restriction gives
an exact sequence

\[
1\longrightarrow W^\vee
\longrightarrow\operatorname{Gal}(L/F)
\longrightarrow G
\longrightarrow1,
\tag{10.4}
\]

where

\[
W^\vee=\operatorname{Hom}_{\mathbb F_2}(W,\mathbb F_2)
\cong\operatorname{Gal}(L/E).
\]

#### Proof

Let \(N\) be the normal closure of \(H_{\mathrm{dec}}/F\).  Because
\(K_0\subset H_{\mathrm{dec}}\), the field \(N\) contains the normal
closure \(E\) of \(K_0/F\).  The extension
\(H_{\mathrm{dec}}/F\) is separable.  Hence every
\(i:K_0\hookrightarrow E\) extends, by the extension-of-embeddings
theorem, to an \(F\)-embedding of \(H_{\mathrm{dec}}\), and any such
extension sends

\[
\sqrt{r_\alpha}\longmapsto
\pm\sqrt{r_{\alpha,i}}.
\]

Thus \(N\) contains every generator displayed in (10.1), so
\(L\subseteq N\).

Conversely, every \(F\)-embedding of \(L\) permutes the embeddings
\(i\in I\) through \(G\) and sends each displayed square root to a
signed square root of another displayed radicand.  Hence it preserves
\(L\).  Therefore \(L/F\) is normal and separable and contains
\(H_{\mathrm{dec}}\),
so \(N\subseteq L\).  Thus \(L=N\).

Kummer theory over \(E\) identifies the Galois group obtained by
adjoining square roots with the dual of the span of their square
classes.  That span is \(W\), hence
\(\operatorname{Gal}(L/E)\cong W^\vee\).  Both \(E/F\) and \(L/F\) are
finite Galois.  Every \(F\)-automorphism of \(E\) therefore extends to an
\(F\)-automorphism of \(L\), again by the extension-of-embeddings theorem.
Restriction to \(E\) is consequently surjective, and its kernel is
\(\operatorname{Gal}(L/E)\), proving (10.4). \(\square\)

In general, if

\[
\rho=\dim_{\mathbb F_2}W=sd-\dim_{\mathbb F_2}R,
\]

then

\[
[L:E]=2^\rho,
\qquad
|\operatorname{Gal}(L/F)|=2^\rho|G|.
\]

This determines the kernel and the order even when maximality fails.  It
does not assert that the abstract \(G\)-module \(W\) alone determines the
extension class in (10.4).

### Theorem 10.2 — valuation-rank criterion

Choose discrete valuations \(v_1,\ldots,v_m\) of \(E\), and form the
matrix

\[
\mathcal A
=
\left(
v_q(r_{\alpha,i})\bmod2
\right)
\in M_{m\times sd}(\mathbb F_2).
\tag{10.5}
\]

If

\[
\operatorname{rank}_{\mathbb F_2}\mathcal A=sd,
\tag{10.6}
\]

then \(R=0\), \(W=V\), and

\[
\dim_{\mathbb F_2}W=sd.
\]

#### Proof

A square-class relation is a vector
\(\lambda=(\lambda_{\alpha,i})\in V\) for which

\[
\prod_{\alpha,i}
r_{\alpha,i}^{\lambda_{\alpha,i}}
\]

is a square in \(E\).  Every valuation of a square is even, so applying
the selected valuations gives

\[
\mathcal A\lambda=0.
\]

Full column rank forces \(\lambda=0\).  Thus \(\theta\) is injective and
\(W=V\). \(\square\)

### Corollary 10.3 — orbit form

Fix a distinguished embedding \(i_0\in I\).  Suppose there are discrete
valuations

\[
v^{(1)},\ldots,v^{(s)}
\]

of \(E\) and a matrix

\[
\mathcal B=(b_{\beta\alpha})\in M_s(\mathbb F_2)
\]

satisfying

\[
v^{(\beta)}(r_{\alpha,i})
\equiv
\begin{cases}
b_{\beta\alpha},&i=i_0,\\
0,&i\ne i_0
\end{cases}
\pmod2.
\tag{10.7}
\]

If \(\mathcal B\) is invertible, then the \(sd\) conjugate radicands are
square-class independent.

#### Proof

For a valuation \(v\) and \(g\in G\), define

\[
(g v)(x)=v(g^{-1}x).
\]

For every \(j\in I\), choose \(g_j\in G\) with \(g_j(i_0)=j\), and use
the transported valuations \(g_jv^{(\beta)}\).  Since

\[
(g_jv^{(\beta)})(r_{\alpha,\ell})
=v^{(\beta)}(r_{\alpha,g_j^{-1}(\ell)}),
\]

its parity is \(b_{\beta\alpha}\) when \(\ell=j\) and zero otherwise.
After ordering rows by valuation and sheet, and columns by radicand and
sheet, the parity matrix is

\[
\mathcal B\otimes I_d.
\]

Its rank is \(sd\).  Apply Theorem 10.2. \(\square\)

### Theorem 10.4 — maximal Kummer–wreath lift

If \(R=0\), then

\[
\operatorname{Gal}(L/F)
\cong
(C_2^s)^I\rtimes G
=
C_2^s\wr_I G.
\tag{10.8}
\]

In particular,

\[
\left|\operatorname{Gal}(L/F)\right|
=2^{sd}|G|.
\]

#### Proof

Choose square roots
\(x_{\alpha,i}=\sqrt{r_{\alpha,i}}\).  An automorphism
\(\tau\in\operatorname{Gal}(L/F)\) restricts to some \(g\in G\) and
acts by

\[
\tau(x_{\alpha,i})
=
\varepsilon_{\alpha,i}(\tau)
x_{\alpha,g(i)},
\qquad
\varepsilon_{\alpha,i}(\tau)\in\{\pm1\}.
\]

Let \(G\) act on sign arrays \(\delta\in(C_2^s)^I\) by

\[
(g\cdot\delta)_{\alpha,j}
=\delta_{\alpha,g^{-1}(j)},
\]

and reindex the displayed source signs by

\[
\delta_{\alpha,j}(\tau)
=\varepsilon_{\alpha,g^{-1}(j)}(\tau).
\]

For \(\tau_1,\tau_2\) restricting to \(g_1,g_2\), direct composition
gives

\[
\delta(\tau_1\tau_2)
=\delta(\tau_1)\bigl(g_1\cdot\delta(\tau_2)\bigr).
\]

This gives an injective signed-permutation representation

\[
\operatorname{Gal}(L/F)
\hookrightarrow
(C_2^s)^I\rtimes G.
\tag{10.9}
\]

It is injective because an automorphism fixing \(E\) and every chosen
square root fixes the generators of \(L\).

When \(R=0\), Theorem 10.1 gives

\[
\left|\operatorname{Gal}(L/F)\right|
=|W^\vee||G|
=2^{sd}|G|.
\]

The target of (10.9) has the same order.  Therefore the injection is an
isomorphism. \(\square\)

### Corollary 10.5 — weighted multiquadratic decorated covers

Fix \(\mathbf a\in B_{\mathrm{GS}}(\mathbf c)\) geometrically and set

\[
F=\overline K(y),
\qquad
K_0=\overline K(X_{\mathbf a}),
\qquad
y=f_{\mathbf c}.
\]

Then \([K_0:F]=d(\mathbf c)\), and the normal closure of \(K_0/F\) has
group \(S_{d(\mathbf c)}\).  Choose
\(r_1,\ldots,r_s\in K_0^\times\).  If their \(sd(\mathbf c)\)
conjugates in the normal closure have a valuation-parity matrix of full
column rank \(sd(\mathbf c)\), then

\[
\operatorname{Gal}(L/F)
\cong
C_2^s\wr S_{d(\mathbf c)}.
\tag{10.10}
\]

#### Proof

Theorem 7.1 supplies \(G=S_{d(\mathbf c)}\).  Theorem 10.2 supplies
\(R=0\), and Theorem 10.4 gives (10.10). \(\square\)

The identical implication holds over the generic arithmetic base
\(F=K(\mathbf a)(y)\), using Corollary 7.2, whenever the radicands are
defined over its degree-\(d(\mathbf c)\) sheet field and the same full
column-rank condition is verified in the normal closure.

Corollary 10.5 is a criterion, not an automatic closure claim.  The exact
remaining mathematical obligation is to prove \(R=0\), equivalently that
the \(sd(\mathbf c)\) conjugate square classes are independent.  A
sufficient divisor-based certification route is:

1. define the radicands in the sheet field;
2. choose discrete valuations of the normal closure;
3. compute the parity of every conjugate at those valuations, allowing
   odd zeros or odd poles;
4. account for ramification when transporting proposed divisor data into
   the normal closure; and
5. prove that the resulting matrix has full column rank
   \(sd(\mathbf c)\).

If Corollary 10.3 is used, zero off-sheet parity and an invertible seed
matrix \(\mathcal B\) are additional hypotheses of that convenient orbit
form.  They are not necessary for Theorem 10.2, and valuation rank itself
is only one sufficient way to prove \(R=0\); a direct square-class
argument is equally valid.  In every route, the base permutation group
does not need to be recomputed.

---

## 11. Downstream consequences and strict boundaries

### 11.1 What is now closed

Under the standing hypotheses—pairwise distinct \(a_i\), every
\(c_i\ne0\), and the boundary-good condition where required—the paper
proves, without per-\(k\) induction or an infinite certificate sequence:

- the exact degree of every weighted radical-sum map;
- the genus of the multiquadratic source curve;
- the complete boundary ramification analysis;
- generic simplicity and critical-value separation;
- full symmetric base monodromy for every \(k\ge3\);
- the equal-weight DBP group \(S_{\delta_k}\) for every \(k\ge3\); and
- the exact conditional mechanism for maximal Kummer–wreath lifts.

For the DBP paper ensemble, this supplies the arbitrary-\(k\) base theorem
needed to strengthen the released horizon-cover paper beyond its
four-charge base.

The downstream interface is deliberately small:

| downstream use | reusable input from this paper | case-specific obligation that remains |
|---|---|---|
| released horizon-cover paper | \(d(\mathbf c)\), genus, ramification count, and \(S_{d(\mathbf c)}\) for every \(k\ge3\) | translate its notation and state the relevant weight specialization |
| Kummer or crown decoration | the base quotient \(G=S_{d(\mathbf c)}\) and Theorems 10.1–10.4 | define the concrete radicands and prove \(R=0\) |
| low-\(k\) computations | exact formulas against which certificates can be checked | retain them as independent validation, not proof steps |
| braid or wall analysis | the generic simple branch locus and transposition inertia | construct explicit paths or braid words |
| a physical charge slice | a generic ambient theorem and exact exceptional loci | prove that the slice meets \(B_{\mathrm{GS}}(\mathbf c)\), then analyze special points |

### 11.2 What is not claimed

Nothing in the argument claims:

- simple branching at every point of \(B_{\mathbf c}\);
- any result when two \(a_i\) coincide;
- any result for a vanishing weight \(c_i\);
- a positive-characteristic analogue of the weighted symmetric-monodromy
  theorem;
- maximal Kummer rank without a proof that \(R=0\);
- explicit complex braid words for the branch points;
- a closure theorem for iterated self-glue towers; or
- a physical branch-selection statement at special charge vectors.

In particular, full symmetric base monodromy does not by itself imply a
full wreath product.  A failure of maximality is exactly
\(R\ne0\), where \(R\) is the concrete \(G\)-stable module of
multiplicative square relations among the conjugate radicands.

---

## 12. Provenance and correction record

This paper is an additive theorem source.  It was reconstructed from the
canonical Cella DAG object at
`DAG_Library/canonical/theorem-dag.json`, as reported by the DAG service at
revision

```text
sha256:acd9d4c392fb9e65353db0d4a35d82dcb69f5e1ef913dc99435cd1254fe39ca3
```

and from the following retained sources:

- `ALL_K_MONODROMY_THEOREM_NOTE_2026-07-10.md`;
- `GS_GENERIC_MORSE_LEMMA_PROOF_2026-07-10.md`;
- `KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md`;
- `LOG_ENTRY_R6_R7_generic_descent_v2.md`; and
- `AUDIT_REPORT_R6_R7_GENERIC_DESCENT.md`.

The relevant live-DAG closure was:

| DAG node | role in this paper | disposition here |
|---|---|---|
| `DBP:note:allk_monodromy` | all-\(k\) base theorem source | re-proved, repaired, and generalized to arbitrary nonzero fixed weights |
| `DBP:proof:gs_morse` | generic Morse and value-separation source | rebuilt through the finite relative ramification scheme |
| `DBP:thm:kummer_wreath_lift` | general \((G,d)\) lift | restated with the exact square-class and rank hypotheses |
| `DBP:paper:IV` | principal downstream consumer | supplied with an arbitrary-\(k\) base theorem; manuscript integration remains separate |
| `DBP:gap:IV1`, `DBP:gap:IV2` | stale-label and integration gaps | mathematical content supplied here; DAG status is unchanged pending registration and integration |
| `DBP:gap:IV3` | concrete all-\(k\) crown/Kummer instantiation | not closed; this paper isolates its remaining obligation as \(R=0\) |
| `DBP:gap:IV7` | explicit complex braid transport | outside scope and still open |

Those documents provided discovery and provenance.  The proof imports
standard foundations including: Riemann–Hurwitz; the Galois correspondence;
Gauss's lemma; Hensel's lemma; finiteness of normalization over excellent
Noetherian schemes; the completed-local criterion for smoothness;
proper-plus-quasi-finite implies finite; closed-image and dimension facts
for finite morphisms; the Jacobian criterion for étaleness; triviality of
connected finite étale covers of \(\mathbb P^1\) over an algebraically
closed characteristic-zero field; generation of geometric monodromy by
local inertia; the extension-of-embeddings theorem; and quadratic Kummer
theory.  Every family-specific calculation and implication is given in
the paper.

Three proof repairs are incorporated:

1. **Primitive-element repair.**  A cancellation claim based only on one
   odd valuation is insufficient because unit terms may cancel.  Proposition
   2.3 instead uses the exact action of individual sign flips.
2. **Relative-critical-scheme repair.**  Finiteness of the critical
   incidence is not assumed.  Proposition 5.1 constructs it as a closed
   subscheme of the proper relative curve and proves it finite before
   closed-image and dimension arguments are used.
3. **Kummer-maximality repair.**  “Full rank” is replaced everywhere by
   the exact condition \(\operatorname{rank}\mathcal A=sd\), and the
   valuation method is identified as sufficient rather than necessary.

The earlier theorem note remains valuable as a historical development
record and as the location of independent low-\(k\) computations.  Within
its stated hypotheses, the present paper is the self-contained proof
authority for the weighted and all-\(k\) base-monodromy statements.

---

## 13. Conclusion

The equal-weight axial mass norm is one member of a broader and rigid
family.  On a multiquadratic cover, a weighted radical sum with every
coefficient nonzero is a primitive function.  Its poles determine its exact degree, its critical
incidence is irreducible, its degenerate points and value collisions occupy
proper parameter loci, and outside those loci every local branch cycle is a
transposition.  Connectedness then leaves no intermediate permutation
group:

\[
\operatorname{Mon}(f_{\mathbf c})=S_{d(\mathbf c)}.
\]

The reusable content is therefore not a list of groups at isolated values
of \(k\).  It is a uniform geometric mechanism:

\[
\text{multiquadratic source}
\longrightarrow
\text{finite critical incidence}
\longrightarrow
\text{generic simple folds}
\longrightarrow
S_d.
\]

Above that base, maximal wreath lifting has one additional question:
whether the concrete conjugate square classes are independent, or
equivalently \(R=0\).  A valuation matrix of full column rank \(sd\)
certifies that condition and hence produces the exact wreath product.
This cleanly separates what is universal from what each downstream
realization must still prove.
