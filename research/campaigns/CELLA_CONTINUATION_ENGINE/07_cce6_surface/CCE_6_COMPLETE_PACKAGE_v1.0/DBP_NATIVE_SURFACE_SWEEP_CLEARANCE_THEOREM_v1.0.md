# Exact native DBP surface-sweep clearance theorem v1.0

**Campaign:** Cella Continuation Engine, CCE-6  
**Status:** PROVED at the native swept-image and exact domain-admission scope  
**Date:** 2026-07-14  
**Scope ceiling:** \(\mathscr S_{\mathbb Z}^{\rm nat}=\operatorname{im}L_{\mathbb Z}\); no claim about all surface homology

## 0. Result

The full Stage-2 surface sweep introduces no independent collision divisor
beyond three marked divisors of the already transported boundary curve.  In
homogeneous angular coordinates \([V:T]\), they are

\[
T=0,\qquad D_1:=T-cV=0,\qquad D_2:=T-c^2V=0.
\]

Under the exact Stage-1 birational coordinate \(x\), these are respectively

\[
x=x_p,\qquad x=1,\qquad x=\infty.
\]

The pulled-back norm and polar divisors have fibre collision resultant

\[
\boxed{\operatorname{Res}_{[\Xi:H]}(N,R)=c^2D_1^2},
\]

and the norm branch discriminant is

\[
\boxed{\operatorname{Disc}_{\Xi}(N)=-4(1-c)TD_2}.
\]

Consequently a Gauss--Manin-flat curve representative avoiding
\(x_p,1,\infty\) has a collision-free four-quadrant angular lift and a
collision-free relative fibre sweep.  The CCE-2 parameter tube bounds make
all remaining parameter factors uniformly nonzero on both exact corridors.
Thus curve admissibility transfers to full native-surface admissibility; no
extra surface route or unproved genericity assumption is required.

This theorem replaces the earlier informal instruction to "choose a thin
tube" with an exact divisor reduction, exact resultants, boundary-face
checks, and quantitative lower-bound formulas.

## 1. Exact coordinate ring

Work on the shear cover

\[
\rho^2=1+\sigma^2
\]

and put

\[
A=\rho+1,\qquad B=\rho-1,
\qquad a=\frac A2,\qquad b=\frac B2,
\qquad c=\frac BA.
\]

Then

\[
A-B=2,\qquad A+B=2\rho,\qquad AB=\sigma^2,
\]

so in particular

\[
ab=\frac{\sigma^2}{4},\qquad
1-c=\frac2A,\qquad
1+c=\frac{2\rho}{A}.
\]

The declared exact ring is

\[
\mathcal R=
\mathbb Q(i)[\sigma,\rho,V,T,\Xi,H]
\big/(\rho^2-1-\sigma^2),
\]

localized at the factors certified below.  To avoid rational denominators,
also define

\[
\Delta_1=AT-BV=A D_1,
\qquad
\Delta_2=A^2T-B^2V=A^2D_2.
\]

All identities in this report are polynomial identities in this localized
quotient ring.

## 2. Corridor parameter bounds

Both CCE-2 radius-\(1/8\) lifted tubes certify

\[
|\sigma|\ge\frac38,\qquad
|\rho|\ge\frac12,\qquad
|A|,|B|\ge\frac1{64},\qquad
|A|,|B|\le5,
\]

and

\[
|c|\ge\frac1{320},\qquad |c^{-1}|\ge\frac1{320}.
\]

The same nested certificates give the marked-curve separations

\[
|m|,|1-m|\ge\frac1{512},\qquad
|x_p|\ge\frac25,\qquad
|x_p-1|\ge\frac1{320},\qquad
|x_p-m|\ge\frac1{163840},
\]

and \(|y_p^2|\ge1/131072000\).  The last inequality keeps the two points
over \(x_p\) distinct.

The exact identities above therefore give

\[
\boxed{
|ab|\ge\frac9{256},\qquad
|1-c|\ge\frac25,\qquad
|1+c|\ge\frac15.
}
\]

In particular

\[
c(1-c)(1+c)ab\ne0
\]

throughout either certified corridor.  These bounds are inherited from the
existing CCE-2 certificates; they are not numerical sampling claims.

## 3. Angular and fibre pullbacks

Stage 2 gives

\[
C^2=\frac{(1-c)V}{D_1},\qquad
S^2=\frac{T-V}{D_1},\qquad
C^2+S^2=1.
\]

In cleared form,

\[
\boxed{
\Delta_1 C^2=2V,\qquad
\Delta_1 S^2=A(T-V).
}
\]

The sum identity follows polynomially because

\[
2V+A(T-V)=AT-BV=\Delta_1.
\]

For compactified fibre coordinate \([\Xi:H]\), the norm double cover has
primitive branch polynomial

\[
N=D_2\Xi^2+(1-c)T H^2.
\]

Its denominator-cleared form is

\[
\boxed{\widehat N=\Delta_2\Xi^2+2AT H^2.}
\]

The pullback of the primitive polar divisor
\(a^2x_{\rm surf}^2+z_{\rm surf}^2=0\) is

\[
\boxed{T(\Xi^2+H^2)=0.}
\]

Thus its fibre component is

\[
R=\Xi^2+H^2,
\]

while its base component is exactly \(T=0\).

## 4. Exact collision computation

### 4.1 Norm branches

As a quadratic in \(\Xi\), the primitive norm polynomial has discriminant

\[
\operatorname{Disc}_{\Xi}(N)
=-4(1-c)TD_2.
\]

Equivalently, for the cleared polynomial,

\[
\operatorname{Disc}_{\Xi}(\widehat N)
=-8AT\Delta_2.
\]

Hence the two norm branch points collide only on

\[
A=0,\qquad T=0,\qquad D_2=0.
\]

The parameter factor \(A\) is excluded by CCE-2.  The other two factors are
marked base divisors handled below.

At the fibre boundary \(H=0\),

\[
\widehat N|_{H=0}=\Delta_2\Xi^2.
\]

Therefore the two relative endpoints \(Q_\pm\) remain distinct and outside
the norm divisor precisely when \(D_2\ne0\).  There is no additional
endpoint collision equation.

### 4.2 Norm versus polar divisor

For two binary diagonal quadratics

\[
u\Xi^2+vH^2,\qquad \Xi^2+H^2,
\]

their homogeneous resultant is \((v-u)^2\).  Here

\[
2AT-\Delta_2=-B\Delta_1.
\]

Consequently

\[
\boxed{
\operatorname{Res}_{[\Xi:H]}(\widehat N,R)
=B^2\Delta_1^2.
}
\]

Dividing by the harmless powers of \(A\) gives the primitive identity

\[
\boxed{
\operatorname{Res}_{[\Xi:H]}(N,R)=c^2D_1^2.
}
\]

Thus a norm branch point meets a fibre polar point only at \(c=0\) or
\(D_1=0\).  The first is excluded by CCE-2; the second is one marked base
divisor.  At \(H=0\), \(R=\Xi^2\ne0\), so a polar point never meets a
relative endpoint.

This resultant is the only genuinely surface-specific collision
calculation required by CCE-6.

## 5. Reduction to marked curve divisors

The exact Stage-1 coordinate map becomes particularly simple in the
\((A,B)\) variables:

\[
\boxed{
x=\frac{2BV}{\Delta_2},\qquad
m=\frac{B}{2\rho},\qquad
x_p=-\frac2B.
}
\]

Direct expansion gives

\[
2BV-\Delta_2=-A\Delta_1,
\]

\[
4\rho V-\Delta_2=A^2(V-T),
\]

and

\[
B^2V+\Delta_2=A^2T.
\]

Therefore

\[
\boxed{
\begin{array}{c|c}
\text{surface-sweep base divisor} & \text{marked curve divisor}\\
\hline
V=0 & x=0\\
V=T & x=m\\
T=0 & x=x_p\\
D_1=0 & x=1\\
D_2=0 & x=\infty
\end{array}}
\]

The first two are the allowed relative endpoints.  The last three are
exactly the pole, the remaining Legendre branch point, and the point at
infinity.  Hence the surface clearance predicate is not new data: it is the
pullback of the refined curve-admissibility predicate.

## 6. Swept-boundary faces

At \(V=0\),

\[
\Delta_1=AT,\qquad \Delta_2=A^2T,
\]

and

\[
\widehat N=AT(A\Xi^2+2H^2).
\]

Here \(C=0\) and the two \(C\)-sign branches glue.  The other angular
coordinate does not vanish, the fibre endpoints remain distinct, and the
norm/polar resultant is \(A^2B^2T^2\ne0\).

At \(V=T\),

\[
\Delta_1=2T,\qquad \Delta_2=4\rho T,
\]

and

\[
\widehat N=2T(2\rho\Xi^2+AH^2).
\]

Here \(S=0\) and the two \(S\)-sign branches glue.  Again the other angular
coordinate does not vanish, the endpoints remain distinct, and the
norm/polar resultant is \(4B^2T^2\ne0\).

The two angular coordinates could vanish simultaneously only if
\(V=0=V-T\), hence \(T=0\); that point is excluded.  The four-quadrant side
boundaries therefore cancel without a hidden corner collision.

## 7. Quantitative clearance transfer

Use the standard chordal distance on \(\mathbb P^1\), and normalize
\([V:T]\) by \(|V|^2+|T|^2=1\).  The five relevant base points are

\[
P_0=[0:1],\quad P_m=[1:1],\quad P_\infty=[1:0],
\quad P_1=[1:c],\quad P_2=[1:c^2].
\]

The coefficient bounds give

\[
\|[1:c]\|_2\le321,\qquad
\|[1:c^2]\|_2\le102401.
\]

The smallest conservative pairwise bound is the \(P_1,P_2\) bound:

\[
d_{\rm ch}(P_1,P_2)
=\frac{|c(c-1)|}
{\|[1:c]\|_2\|[1:c^2]\|_2}
\ge
\frac1{800\cdot321\cdot102401}
=\frac1{26296576800}.
\]

Direct determinant estimates for every other pair give larger lower bounds.
For example,

\[
\begin{aligned}
d_{\rm ch}(P_\infty,P_2)&\ge\frac1{10485862400},\\
d_{\rm ch}(P_m,P_2)&\ge\frac1{2560025},\\
d_{\rm ch}(P_0,P_2)&\ge\frac1{102401}.
\end{aligned}
\]

Choose the uniform exact exclusion radius

\[
\boxed{\varepsilon_*=\frac1{105186307200}.}
\]

The five radius-\(\varepsilon_*\) neighbourhoods are disjoint because their
centres have separation at least \(4\varepsilon_*\).  The primary interval
has chordal distance at least \(1/25\) from
\(P_\infty,P_1,P_2\), so it lies in their complement.  Choose the
disk-chain trivializations tangent to the three moving neighbourhood
boundaries.  The transported refined representative then satisfies

\[
\boxed{
|T|\ge\varepsilon_*,\qquad
|D_1|\ge\varepsilon_*,\qquad
|D_2|\ge\varepsilon_*.
}
\]

Indeed the relevant chordal numerators are respectively
\(T,D_1,D_2\), and the norms of \([1:c]\) and \([1:c^2]\) are at least one.
This supplies a concrete exact route-wide witness for both corridors.

More generally, let a refined curve-track certificate provide positive
rational witnesses

\[
|T|\ge\varepsilon_\infty,\qquad
|D_1|\ge\varepsilon_1,\qquad
|D_2|\ge\varepsilon_2.
\]

The witnesses refer respectively to clearance from
\(x_p,1,\infty\) under the table in Section 5.  Then the full surface
configuration has the exact lower bounds

\[
\boxed{
\begin{aligned}
|\operatorname{Disc}_{\Xi}(N)|
&\ge \frac85\varepsilon_\infty\varepsilon_2,\\
|\operatorname{Res}(N,R)|
&\ge \frac1{102400}\varepsilon_1^2,\\
|(1-c)T|&\ge\frac25\varepsilon_\infty,\\
|D_2|&\ge\varepsilon_2.
\end{aligned}}
\]

On the two gluing faces these specialize to

\[
\begin{array}{c|cc}
&V=0&V=T\\
\hline
|D_1|&\ge\varepsilon_\infty&\ge\frac25\varepsilon_\infty\\
|D_2|&\ge\varepsilon_\infty&\ge\frac2{25}\varepsilon_\infty\\
|\operatorname{Disc}(N)|
&\ge\frac85\varepsilon_\infty^2
&\ge\frac{16}{125}\varepsilon_\infty^2\\
|\operatorname{Res}(N,R)|
&\ge\frac1{102400}\varepsilon_\infty^2
&\ge\frac1{640000}\varepsilon_\infty^2.
\end{array}
\]

These are exact rational transfers, not floating estimates.  A metric
representative certificate may instantiate the three \(\varepsilon\)'s;
for the two released routes they are all instantiated by
\(\varepsilon_*\).  At the homology-local-system level their positivity is
automatic as follows.

The CCE-2 lifted route is a finite compact disk chain.  Over it the marked
sections \(x_p,1,\infty\), and the two points above \(x_p\), are mutually
disjoint by the certified separations in Section 2.  Choose disjoint closed
section neighbourhoods with rational radii below those bounds.  The
complement inside the proper compactified curve family is a proper manifold
with boundary, so Ehresmann trivialization on each disk and exact overlap
matching transport the primary relative representative through the refined
complement.  Its compact PL track is disjoint from the deleted
neighbourhoods, so each displayed minimum is strictly positive; rational
numbers below the three minima provide exact witnesses.  This is the refined
Gauss--Manin representative of the already certified CCE-3 class, not a
second choice of homology class.

Over that track, the nonzero discriminant and resultant make the four-point
fibre divisor configuration locally trivial.  The primary fibre interval
therefore transports in its complement.  Compactness again supplies positive
distance from norm and polar divisors, while the formulas above certify that
no collision can destroy that isotopy.  This proves corridor-wide clearance
of the complete parameter-by-angular-by-fibre sweep.

## 8. Theorem

### Theorem CCE6.1 — exact clearance transfer for the native DBP sweep

Let \(\ell_\uparrow\) or \(\ell_\downarrow\) be either CCE-2 exact lifted
corridor with its certified radius-\(1/8\) tube, and let
\(\delta_+\) be the selected primary relative class.  Transport its primary
representative in the refined curve complement obtained by deleting
\(x_p,1,\infty\).  Then:

1. the refined representative exists over the whole corridor and forgets to
   the CCE-3 Gauss--Manin transport of \(\delta_+\);
2. its four-quadrant angular lift has no pole, branch, or corner collision;
3. its relative norm-cover fibre interval transports without meeting the
   norm or polar divisor and keeps two distinct endpoints on \(D_\infty\);
4. the resulting swept chains form an integral isotopy in
   \(H_2(X_u,Y_u;\mathbb Z)\);
5. the upper and lower terminal chains are respectively the native lifts of
   the certified upper and lower lateral curve classes, including any compact
   correction carried by the CCE-3 affine account;
6. any positive curve-track witnesses
   \((\varepsilon_\infty,\varepsilon_1,\varepsilon_2)\) transfer to the
   explicit full-sweep lower bounds in Section 7.

Hence the native lift commutes with the two certified transports:

\[
G_\eta^{\mathscr S}L_{\mathbb Z,u_+}
=L_{\mathbb Z,u_-}G_\eta^C,
\qquad \eta\in\{\uparrow,\downarrow\},
\]

on the declared native image.  The earlier CCE-6
`SurfaceSweepClearanceUnproved` blocker is discharged at this scope.

## 9. Scope and non-claims

This theorem proves domain admission for the two exact DBP corridors and the
native swept image.  It does not assert:

- that \(\mathscr S_{\mathbb Z}^{\rm nat}\) is the whole surface homology;
- that \(\tfrac14R_{\mathbb Z}\) is integral;
- primitivity of a lifted meridian in the whole surface lattice;
- an absolute CCE-3 representative when its compact correction remains
  affine;
- a full surface transport matrix outside the native image;
- admission of arbitrary paths not carrying the refined curve-clearance
  predicate.

The exact signed-transfer identity
\(R_{\mathbb Z}L_{\mathbb Z}=4\operatorname{id}\), period pairing, boundary
typing, and coefficient-ring separation remain as stated in Paper III; the
new result supplies the missing domain theorem needed to use them along the
two certified corridors.
