# DBP Surface-to-Link Close-Off

## Exact primitive and family-wide boundary theorem, v1.0

**Date:** 2026-07-13  
**Scope:** the primary Gaussian-curvature constant for the shear family
\(F_s=D^2+sDS+P^2-3\), with \(s\ne0\)  
**Closes:** the Stage-A reduction
\(\int_{S_s}K_G\,dA=-2L(\Gamma_s)\), previously supported only by
independent numerical quadratures  
**Does not claim:** a surface cycle or forbidden surface region for the
Galois-dual constant

---

## 0. Result

Let

\[
S_s=\{(D,S,P)\in\mathbb R^3:D^2+sDS+P^2=3\},\qquad s\ne0,
\]

and let \(\Gamma_s^+\) be either component of the spherical link of its
asymptotic cone,

\[
\Gamma_s=\{D^2+sDS+P^2=0\}\cap S^2.
\]

Write \(L(\Gamma_s^+)\) for the length of one component. Then

\[
\boxed{\displaystyle
\int_{S_s}K_G\,dA=-2L(\Gamma_s^+).
}
\tag{0.1}
\]

The factor two is the contribution of the two antipodal cone ends. The proof
below is direct: it diagonalizes the quadric, constructs a global algebraic
primitive for \(K_GdA\), evaluates that primitive at both ends, and identifies
the resulting one-dimensional integral with the spherical-link length by an
explicit substitution. No Cohn--Vossen, Gauss--Bonnet, or Booth reduction is
used as a black box.

Combined with the independently established Legendre reduction of the link,
(0.1) gives the family-wide closed form

\[
\int_{S_s}K_G\,dA
=-4g(s)\bigl[\Pi(n(s);A(s))-(1-C(s))K(A(s))\bigr],
\tag{0.2}
\]

where, with \(r=\sqrt{1+s^2}\),

\[
A(s)=\frac12-\frac1{2r},\qquad
C(s)=\frac{r-1}{r+1},\qquad
n(s)=\frac{A-C}{1-C},\qquad
g(s)=2\sqrt{\frac{1-A}{C(1-C)}}.
\tag{0.3}
\]

At \(s=1\), (0.2) is the primary DBP curvature constant

\[
I_{\rm primary}
=-2^{7/4}\left[(3+2\sqrt2)\Pi\!\left(\frac{4-3\sqrt2}{8};
\frac{2-\sqrt2}{4}\right)
-(2+2\sqrt2)K\!\left(\frac{2-\sqrt2}{4}\right)\right].
\tag{0.4}
\]

---

## 1. Orthogonal diagonalization

Put

\[
r=\sqrt{1+s^2},\qquad
a=\frac{1+r}{2},\qquad
b=\frac{r-1}{2}.
\tag{1.1}
\]

Then \(a,b>0\), \(a-b=1\), and \(ab=s^2/4\). The \((D,S)\)-block has
eigenvalues \(a\) and \(-b\). An orthogonal change of coordinates therefore
puts the surface in the form

\[
S_s:\qquad ax^2-by^2+z^2=3.
\tag{1.2}
\]

Orthogonal changes preserve both \(K_GdA\) and the spherical length of the
asymptotic link, so it is enough to prove the theorem for (1.2).

For reference, one may take an angle \(\varphi\) satisfying

\[
\cos(2\varphi)=\frac1r,\qquad \sin(2\varphi)=\frac{s}{r},
\]

and set

\[
x=\cos\varphi\,D+\sin\varphi\,S,qquad
y=-\sin\varphi\,D+\cos\varphi\,S,qquad z=P.
\tag{1.3}
\]

---

## 2. Global parametrization and curvature form

A global parametrization of (1.2) is

\[
X(u,t)=\left(
\sqrt{\frac3a}\cosh u\cos t,
\sqrt{\frac3b}\sinh u,
\sqrt3\cosh u\sin t
\right),
\tag{2.1}
\]

with \(u\in\mathbb R\) and \(t\in\mathbb R/2\pi\mathbb Z\). Define

\[
p(t)=a\cos^2t+\sin^2t,qquad
\Delta(u,t)=p(t)\cosh^2u+b\sinh^2u.
\tag{2.2}
\]

For

\[
F=ax^2-by^2+z^2-3,qquad
q=\lVert\nabla F\rVert^2,
\]

the implicit-surface formula gives

\[
K_G=\frac{\nabla F^{T}\operatorname{adj}(\operatorname{Hess}F)\nabla F}{q^2}
=-\frac{48ab}{q^2}
=-\frac{12s^2}{q^2}.
\tag{2.3}
\]

Moreover,

\[
q\circ X=12\Delta,
\]

and direct evaluation of \(X_u\times X_t\) yields

\[
\boxed{\displaystyle
X^*(K_GdA)
=-\frac{\sqrt{ab}\cosh u}{\Delta(u,t)^{3/2}}\,du\wedge dt.
}
\tag{2.4}
\]

The right-hand side is \(O(e^{-2|u|})\), uniformly in \(t\), proving absolute
convergence of the total-curvature integral.

---

## 3. A global algebraic primitive

Since

\[
\Delta=p+(p+b)\sinh^2u,
\]

define

\[
\eta=A(u,t)\,dt,
\qquad
A(u,t)=-\frac{\sqrt{ab}\sinh u}
{p(t)\sqrt{p(t)+(p(t)+b)\sinh^2u}}.
\tag{3.1}
\]

The elementary identity

\[
\frac{d}{du}
\left[
\frac{\sinh u}{\sqrt{p+(p+b)\sinh^2u}}
\right]
=\frac{p\cosh u}{[p+(p+b)\sinh^2u]^{3/2}}
\tag{3.2}
\]

immediately gives

\[
\boxed{d\eta=K_GdA.}
\tag{3.3}
\]

This primitive is global on the cylinder. In the eigenframe coordinates it is
the algebraic one-form

\[
\boxed{\displaystyle
\eta=-\frac{2ab\,y}{\sqrt q\,(a^2x^2+z^2)}(x\,dz-z\,dx).
}
\tag{3.4}
\]

Indeed,

\[
dt=\frac{\sqrt a\,(x\,dz-z\,dx)}{ax^2+z^2},
\]

and substituting (2.1) into (3.4) gives (3.1). The denominator
\(a^2x^2+z^2\) cannot vanish on (1.2), since \(x=z=0\) would imply
\(-by^2=3\). Thus (3.4) has none of the pole-chart singularities of the
standard spherical Gauss-map potential.

---

## 4. Boundary evaluation at the two ends

Let

\[
S_U=X([-U,U]\times S^1).
\]

From (3.1),

\[
\lim_{U\to\infty}A(U,t)=-f(t),\qquad
\lim_{U\to\infty}A(-U,t)=+f(t),
\tag{4.1}
\]

where

\[
f(t)=\frac{\sqrt{ab}}{p(t)\sqrt{p(t)+b}}.
\tag{4.2}
\]

The boundary orientation is \(+dt\) at \(u=U\) and \(-dt\) at \(u=-U\).
Stokes' theorem and dominated convergence therefore give

\[
\int_{S_s}K_G\,dA
=\lim_{U\to\infty}\int_{\partial S_U}\eta
=-2\int_0^{2\pi}f(t)\,dt.
\tag{4.3}
\]

The two terms in (4.3) are the equal contributions of the two cone ends.

---

## 5. Exact identification with the spherical-link length

The positive component of the spherical link of

\[
ax^2-by^2+z^2=0
\]

is parametrized by

\[
w(\theta)=\left(\frac{\cos\theta}{\sqrt a},
\frac1{\sqrt b},\sin\theta\right),
\qquad
\gamma(\theta)=\frac{w(\theta)}{\lVert w(\theta)\rVert}.
\tag{5.1}
\]

A direct differentiation gives

\[
\lVert\gamma'(\theta)\rVert
=\frac{\sqrt{ab}\sqrt{p(\theta)+b}}
{a+b\cos^2\theta+ab\sin^2\theta}.
\tag{5.2}
\]

Both (4.2) and (5.2) have fourfold symmetry. On one quadrant set

\[
\tan t=\sqrt{\frac{a+b}{1+b}}\cot\theta.
\tag{5.3}
\]

Writing \(x=\tan\theta\) and
\(y=\tan t=\sqrt{(a+b)/(1+b)}/x\), direct substitution gives

\[
f(t)\,|dt|=\lVert\gamma'(\theta)\rVert\,d\theta.
\tag{5.4}
\]

Consequently,

\[
\int_0^{2\pi}f(t)\,dt
=\int_0^{2\pi}\lVert\gamma'(\theta)\rVert\,d\theta
=L(\Gamma_s^+).
\tag{5.5}
\]

Combining (4.3) and (5.5) proves (0.1).

---

## 6. Period corollary and theorem-interface status

The previously established spherical-link parametrization gives

\[
L(\Gamma_s^+)
=2g(s)\bigl[\Pi(n(s);A(s))-(1-C(s))K(A(s))\bigr].
\tag{6.1}
\]

Equations (0.1) and (6.1) prove (0.2), rather than merely retrodicting it
numerically. At \(s=1\),

\[
n(1)=\frac{4-3\sqrt2}{8},\qquad
4g(1)=2^{7/4}(3+2\sqrt2),\qquad
4g(1)(1-C(1))=2^{7/4}(2+2\sqrt2),
\]

so (0.4) follows.

The primary scalar chain is therefore closed:

\[
\text{DBP surface curvature}
\longrightarrow
\text{spherical-link length}
\longrightarrow
\text{third-kind elliptic period}
\longrightarrow
\text{Landen--trace formula}.
\]

This close-off does not identify the Galois-conjugate principal-value period
with curvature over another real region or cycle of the original DBP surface.
That dual geometric interpretation remains a separate problem.

---

## 7. Audit consequences

1. The former Stage-A label "empirical arc-length identity" is superseded by
   Theorem (0.1).
2. The earlier numerical comparisons at \(s\in\{1/2,1,2\}\) remain useful
   regression checks but are no longer proof-bearing.
3. The later Gauss-map primitive correctly established local exactness; (3.4)
   supplies a global end-adapted primitive and (4.1)--(5.5) supply the missing
   boundary calculation.
4. The family-wide \(K/\Pi\) expression is now unconditional.
5. No claim about a dual surface cycle is promoted by this result.

---

*End of DBP Surface-to-Link Close-Off v1.0.*
