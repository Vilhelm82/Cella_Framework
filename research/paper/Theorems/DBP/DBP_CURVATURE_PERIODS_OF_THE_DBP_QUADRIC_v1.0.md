# Curvature Periods of the DBP Quadric

## Landen trace, relative surface cycles, and Picard--Lefschetz transport, consolidated theorem v1.0

**Date:** 2026-07-14  
**Version:** 1.0  
**Canonical role:** Paper III of the DBP paper ensemble  
**Absorbs mathematically:** the corrected Landen--Trace theorem, the native
relative-period route, the surface-to-link close-off, and dual surface-cycle
Stages 1--3  
**Proof dossiers retained separately:** the Stage 1--3 coordinate,
convergence, residue, and lattice reports, together with their exact
verification scripts  
**Verification:** Landen--Trace 75 exact gates; surface-cycle Stages 1--3
22/22, 17/17, and 22/22 exact gates; native-route verifier retained with its
source theorem

---

## 0. Status

This consolidated paper proves:

1. the two complementary DBP complete-integral differentials;
2. their explicit degree-two isogenies to \(E_{128}\);
3. their common descended trace differential;
4. their exact anti-translation differentials;
5. the exact primary and dual anti-periods;
6. the pole transport, CPV prescriptions, and monodromy;
7. the primary scalar interface from the original DBP curvature integral to
   the period \(I_{\rm primary}\), using the surface-to-link close-off;
8. the dual metric-quartic boundary chains and integral swept surface lift;
9. the two integral Picard--Lefschetz transports modulo ordinary compact
   periods;
10. the exact coefficient separation
    \(\mathbb Z,\mathbb Z[1/2],\mathbb Z[i],\mathbb Z[1/2,i]\) on the curve
    lattice and native swept surface lattice;
11. two pole-free finite-interval kernels for native evaluation of the fixed
    DBP path claims;
12. the corridor-restricted native morphism from relative boundary transport
    to the swept surface subsystem.

The corrected result is:

\[
\boxed{
\omega_\epsilon
=
\frac12\phi_\epsilon^*
\left(\iota_\epsilon^{-1}\Theta\right)
+
\frac12R_\epsilon\,d\log f_\epsilon.
}
\tag{0.1}
\]

The trace term is a non-torsion third-kind period on \(E_{128}\). The anti-translation term is logarithmic and elementary.

This theorem does **not** assert a scalar algebraic relation directly between the two different path values \(I_{\rm primary}\) and \(I_{\rm dual,CPV}\). Such a relation would additionally require a theorem comparing the two relative trace paths \(\Gamma_+\) and \(\Gamma_-\).

---

## 1. Parameters and complete-integral differentials

Put

\[
t=2^{1/4}>0,
\qquad
s=t^2=\sqrt2,
\qquad
\epsilon\in\{+1,-1\}.
\]

The primary channel is \(\epsilon=+1\); the dual channel is \(\epsilon=-1\). Define

\[
m_\epsilon=\frac{2-\epsilon s}{4},
\qquad
n_\epsilon=\frac{4-3\epsilon s}{8},
\tag{1.1}
\]

\[
A_\epsilon=3+2\epsilon s,
\qquad
B_\epsilon=2+2\epsilon s.
\tag{1.2}
\]

The exact parameter relations are

\[
m_++m_-=1,
\qquad
m_+m_-=\frac18,
\qquad
n_++n_-=1,
\tag{1.3}
\]

\[
n_\epsilon
=
-\frac{m_\epsilon^2}{1-2m_\epsilon}.
\tag{1.4}
\]

In particular,

\[
n_+<0,
\qquad
n_->1.
\]

Use

\[
K(m)=
\int_0^1
\frac{dr}{\sqrt{(1-r^2)(1-mr^2)}},
\]

\[
\Pi(n;m)=
\int_0^1
\frac{dr}
{(1-nr^2)\sqrt{(1-r^2)(1-mr^2)}}.
\tag{1.5}
\]

The DBP values are

\[
I_\epsilon
=
-t^7
\left[
A_\epsilon\Pi(n_\epsilon;m_\epsilon)
-B_\epsilon K(m_\epsilon)
\right],
\tag{1.6}
\]

with \(I_-\) interpreted as a Cauchy principal value on the real path.

Let

\[
C_\epsilon:
\qquad
y^2=x(x-1)(x-m_\epsilon).
\tag{1.7}
\]

Under

\[
x=m_\epsilon r^2,
\qquad
y=m_\epsilon r
\sqrt{(1-r^2)(1-m_\epsilon r^2)},
\tag{1.8}
\]

define

\[
F_\epsilon(x)
=
A_\epsilon
\frac{m_\epsilon}{m_\epsilon-n_\epsilon x}
-B_\epsilon,
\tag{1.9}
\]

\[
\boxed{
\omega_\epsilon
=
-\frac{t^7}{2}
F_\epsilon(x)\frac{dx}{y}.
}
\tag{1.10}
\]

If \(\gamma_\epsilon\) is the upper real path \(x:0\to m_\epsilon\), then

\[
\int_{\gamma_\epsilon}\omega_\epsilon=I_\epsilon.
\tag{1.11}
\]

---

## 2. Explicit degree-two isogenies

Set

\[
u=x-m_\epsilon,
\qquad
a_\epsilon=2m_\epsilon-1=-\frac{\epsilon s}{2},
\qquad
b=m_\epsilon(m_\epsilon-1)=-\frac18.
\tag{2.1}
\]

Then

\[
C_\epsilon:
\qquad
y^2=u^3+a_\epsilon u^2+bu.
\tag{2.2}
\]

The point

\[
T_\epsilon=(0,0)
\]

has order two, and translation by it is

\[
T_\epsilon(u,y)
=
\left(
\frac bu,
-\frac{b}{u^2}y
\right).
\tag{2.3}
\]

Define

\[
z=u+a_\epsilon+\frac bu,
\qquad
v=y\left(1-\frac b{u^2}\right).
\tag{2.4}
\]

Direct expansion gives

\[
v^2=z^3+\epsilon s z^2+z.
\tag{2.5}
\]

Choose

\[
\iota_\epsilon^2=\epsilon,
\qquad
\iota_+=1,
\qquad
\iota_-=i.
\tag{2.6}
\]

Then

\[
X=1+\epsilon sz,
\qquad
Y=\iota_\epsilon t^3v
\tag{2.7}
\]

maps the quotient to

\[
E_{128}:
\qquad
Y^2=X^3-X^2+X-1.
\tag{2.8}
\]

The composite degree-two isogeny is

\[
\boxed{
\phi_\epsilon(u,y)
=
\left(
1+\epsilon s
\left(u+a_\epsilon+\frac bu\right),
\ 
\iota_\epsilon t^3y
\left(1-\frac b{u^2}\right)
\right).
}
\tag{2.9}
\]

It satisfies

\[
j(C_\epsilon)=10976,
\qquad
j(E_{128})=128,
\qquad
\Phi_2(128,10976)=0.
\tag{2.10}
\]

---

## 3. Trace theorem

On \(E_{128}\), define

\[
\boxed{
\Theta
=
8\frac{X-3}{X+7}\frac{dX}{Y}.
}
\tag{3.1}
\]

### Theorem 3.1 — Common trace differential

\[
\boxed{
\omega_\epsilon+T_\epsilon^*\omega_\epsilon
=
\phi_\epsilon^*
\left(\iota_\epsilon^{-1}\Theta\right).
}
\tag{3.2}
\]

Equivalently,

\[
(\phi_\epsilon)_*\omega_\epsilon
=
\iota_\epsilon^{-1}\Theta.
\tag{3.3}
\]

Thus

\[
(\phi_+)_*\omega_+=\Theta,
\qquad
(\phi_-)_*\omega_-=-i\Theta.
\tag{3.4}
\]

#### Proof

From (2.4),

\[
\frac{dz}{v}=\frac{du}{y}.
\]

From (2.7),

\[
\frac{dX}{Y}
=
\frac{\iota_\epsilon}{t}\frac{du}{y}.
\tag{3.5}
\]

Put

\[
d_\epsilon=m_\epsilon(1-n_\epsilon)
=
\frac{1+\epsilon s}{16}.
\]

In the \(u\)-coordinate,

\[
F_\epsilon(u)
=
A_\epsilon
\frac{m_\epsilon}{d_\epsilon-n_\epsilon u}
-B_\epsilon.
\tag{3.6}
\]

The exact rational trace identity is

\[
\boxed{
F_\epsilon(u)+F_\epsilon(b/u)
=
-4+\frac{40}{X+7}
=
-4\frac{X-3}{X+7}.
}
\tag{3.7}
\]

Translation preserves \(du/y\). Substitution of (3.7) into (1.10), followed by (3.5) and \(t^8=4\), yields (3.2). \(\square\)

---

## 4. Anti-translation differential

Define

\[
\boxed{
\alpha_\epsilon
=
\omega_\epsilon-T_\epsilon^*\omega_\epsilon.
}
\tag{4.1}
\]

The exact coefficient is

\[
\boxed{
F_\epsilon(u)-F_\epsilon(b/u)
=
A_\epsilon m_\epsilon n_\epsilon
\frac{u-b/u}
{(d_\epsilon-n_\epsilon u)
(d_\epsilon-n_\epsilon b/u)}.
}
\tag{4.2}
\]

Consequently,

\[
T_\epsilon^*\alpha_\epsilon=-\alpha_\epsilon
\tag{4.3}
\]

and

\[
(\phi_\epsilon)_*\alpha_\epsilon=0.
\tag{4.4}
\]

Thus \(\alpha_\epsilon\) does not descend as an ordinary meromorphic differential on the quotient.

### 4.1 Complete-interval reduction

Let

\[
\bar m_\epsilon=1-m_\epsilon,
\qquad
c_\epsilon=\frac{m_\epsilon}{m_\epsilon-n_\epsilon}.
\tag{4.5}
\]

For the DBP parameters,

\[
\frac{d_\epsilon}{m_\epsilon-n_\epsilon}
=
\bar m_\epsilon.
\tag{4.6}
\]

Under \(u=m_\epsilon(r^2-1)\),

\[
F_\epsilon(b/u)
=
A_\epsilon c_\epsilon
\frac{1-r^2}{1-\bar m_\epsilon r^2}
-B_\epsilon.
\tag{4.7}
\]

Therefore the anti-period remains on the complete interval \(r\in[0,1]\):

\[
\boxed{
\begin{aligned}
I_\epsilon-I_\epsilon^T
=
-t^7A_\epsilon
\Bigg[
&\Pi(n_\epsilon;m_\epsilon)
-\frac{c_\epsilon}{\bar m_\epsilon}K(m_\epsilon)\\
&+
\frac{c_\epsilon m_\epsilon}{\bar m_\epsilon}
\Pi(\bar m_\epsilon;m_\epsilon)
\Bigg].
\end{aligned}
}
\tag{4.8}
\]

There is no incomplete amplitude. Equation (4.8) is already a complete-period reduction.

---

## 5. Logarithmic closure of the anti differential

Put

\[
u_{0,\epsilon}=\frac{d_\epsilon}{n_\epsilon},
\qquad
u_{1,\epsilon}=\frac b{u_{0,\epsilon}}.
\tag{5.1}
\]

Then

\[
z_{0,\epsilon}
=
u_{0,\epsilon}+a_\epsilon+\frac b{u_{0,\epsilon}}
=
-4\epsilon s.
\tag{5.2}
\]

Define

\[
\ell_\epsilon
=
-\frac{2it}{\iota_\epsilon},
\qquad
R_\epsilon
=
\frac{4i}{\iota_\epsilon}.
\tag{5.3}
\]

Thus

\[
\ell_+=-2it,
\qquad
R_+=4i,
\tag{5.4}
\]

\[
\ell_-=-2t,
\qquad
R_-=4.
\tag{5.5}
\]

The identities

\[
\ell_\epsilon^2=z_{0,\epsilon},
\qquad
R_\epsilon\ell_\epsilon
=
\frac{t^7A_\epsilon m_\epsilon}{2d_\epsilon}
\tag{5.6}
\]

are exact.

Define the rational function

\[
\boxed{
f_\epsilon
=
\frac{y-\ell_\epsilon u}
{y+\ell_\epsilon u}.
}
\tag{5.7}
\]

### Theorem 5.1 — Exact logarithmic anti differential

\[
\boxed{
\alpha_\epsilon
=
R_\epsilon\,d\log f_\epsilon.
}
\tag{5.8}
\]

#### Proof

Let

\[
G_\epsilon(u)
=
u^3+a_\epsilon u^2+bu
=
y^2.
\]

From (4.2),

\[
F_\epsilon(u)-F_\epsilon(b/u)
=
-\frac{A_\epsilon m_\epsilon}{d_\epsilon}
\frac{u^2-b}
{(u-u_{0,\epsilon})(u-u_{1,\epsilon})}.
\tag{5.9}
\]

The curve equation gives

\[
uG_\epsilon'(u)-2G_\epsilon(u)
=
u(u^2-b).
\tag{5.10}
\]

Because \(\ell_\epsilon^2=z_{0,\epsilon}\),

\[
G_\epsilon(u)-\ell_\epsilon^2u^2
=
u(u-u_{0,\epsilon})(u-u_{1,\epsilon}).
\tag{5.11}
\]

Differentiating (5.7), then using (5.10) and (5.11), gives

\[
d\log f_\epsilon
=
\ell_\epsilon
\frac{u^2-b}
{y(u-u_{0,\epsilon})(u-u_{1,\epsilon})}
\,du.
\tag{5.12}
\]

Equations (1.10), (5.9), (5.12), and the normalization in (5.6) prove (5.8). \(\square\)

### Corollary 5.2 — Principal anti pole divisor

The pole-residue divisor of \(\alpha_\epsilon\) is the divisor of \(f_\epsilon\). Hence it is principal.

This is why non-torsion of the descended pole \(P=(-7,20i)\) does not obstruct reduction of the anti differential: the trace and anti sectors are different. Indeed, the trace of \(\alpha_\epsilon\) is zero.

---

## 6. Exact anti-periods

Along the upper complete-integral path,

\[
f_\epsilon(-m_\epsilon,0)=-1,
\qquad
\lim_{u\to0^-}f_\epsilon(u,y)=1.
\tag{6.1}
\]

### Theorem 6.1 — Primary anti-period

In the primary channel,

\[
f_+
=
\frac{y+2itu}{y-2itu}.
\]

For \(-m_+<u<0\) on the upper oval, \(f_+\) lies on the unit circle and its continuous argument increases from \(-\pi\) to \(0\). Therefore

\[
\Delta_{\gamma_+}\log f_+=i\pi.
\]

Using \(R_+=4i\),

\[
\boxed{
I_{\rm primary}-I_{\rm primary}^T
=
-4\pi.
}
\tag{6.2}
\]

Equivalently,

\[
\boxed{
I_{\rm primary}^T
=
I_{\rm primary}+4\pi.
}
\tag{6.3}
\]

With the standing numerical pin,

\[
I_{\rm primary}^T
\approx
7.55587991169875418480055237259123388873168274077882.
\tag{6.4}
\]

### Theorem 6.2 — Dual anti-period

In the dual channel,

\[
f_-
=
\frac{y+2tu}{y-2tu}.
\]

The real path crosses the simple zero corresponding to the third-kind pole. The real principal value is the endpoint difference of \(\log|f_-|\):

\[
\log|1|-\log|-1|=0.
\]

Hence

\[
\boxed{
\operatorname{CPV}
\left(
I_{\rm dual}-I_{\rm dual}^T
\right)
=
0.
}
\tag{6.5}
\]

Equivalently,

\[
\boxed{
I_{\rm dual}^{T,\rm CPV}
=
I_{\rm dual,CPV}.
}
\tag{6.6}
\]

The two one-sided logarithmic continuations have

\[
\boxed{
I_{\rm dual}-I_{\rm dual}^T
\in
\{-4\pi i,+4\pi i\}.
}
\tag{6.7}
\]

Their difference has magnitude \(8\pi i\).

---

## 7. Completed period formulas

Let

\[
\Gamma_\epsilon=\phi_\epsilon(\gamma_\epsilon).
\]

Then

\[
\Gamma_+:
\quad
X=1\longrightarrow+\infty,
\]

\[
\Gamma_-:
\quad
X=1\longrightarrow-\infty.
\tag{7.1}
\]

The trace theorem gives

\[
I_\epsilon+I_\epsilon^T
=
\iota_\epsilon^{-1}
\int_{\Gamma_\epsilon}\Theta,
\tag{7.2}
\]

with CPV in the dual channel. Combining (7.2) with the exact anti-periods yields the final channel formulas.

### Primary

\[
\boxed{
\int_{\Gamma_+}\Theta
=
2I_{\rm primary}+4\pi.
}
\tag{7.3}
\]

Equivalently,

\[
\boxed{
I_{\rm primary}
=
\frac12\int_{\Gamma_+}\Theta-2\pi.
}
\tag{7.4}
\]

### Dual CPV

\[
\boxed{
-i\,
\operatorname{CPV}
\int_{\Gamma_-}\Theta
=
2I_{\rm dual,CPV}.
}
\tag{7.5}
\]

Equivalently,

\[
\boxed{
I_{\rm dual,CPV}
=
-\frac i2
\operatorname{CPV}
\int_{\Gamma_-}\Theta.
}
\tag{7.6}
\]

Equations (7.4) and (7.6) are the completed DBP Landen–Trace reductions.

---

## 7A. Primary surface-to-period interface

Let

\[
S_\sigma=\{D^2+\sigma DS+P^2=3\},\qquad \sigma\ne0,
\]

and let \(\Gamma_\sigma^+\) be one component of the spherical link of the
asymptotic cone \(D^2+\sigma DS+P^2=0\). The surface-to-link close-off proves

\[
\boxed{
\int_{S_\sigma}K_G\,dA=-2L(\Gamma_\sigma^+).
}
\tag{7A.1}
\]

The proof is algebraic and family-wide. After orthogonal diagonalization to
\(ax^2-by^2+z^2=3\), it exhibits the global primitive

\[
\eta=-\frac{2ab\,y}{\sqrt q\,(a^2x^2+z^2)}(x\,dz-z\,dx),
\qquad d\eta=K_G\,dA,
\tag{7A.2}
\]

and evaluates its two oriented end limits exactly. An explicit reciprocal
tangent substitution identifies each end integral with the length of one
spherical-link component.

Combining (7A.1) with the exact Legendre reduction of that link gives, at the
keystone \(s=1\),

\[
\boxed{
\int_{S_1}K_G\,dA
=-2^{7/4}\left[(3+2\sqrt2)\Pi(n_+;m_+)
-(2+2\sqrt2)K(m_+)\right]
=I_{\rm primary}.
}
\tag{7A.3}
\]

Thus the primary scalar curvature constant is now an input proved from the
original surface, rather than a numerically retrodicted period value. This
does not identify \(I_{\rm dual,CPV}\) with a real region or cycle of the DBP
surface.

---

## 7B. Dual complex boundary-cycle interface

The dual relative path has an exact realization on the metric elliptic
quotient of the complexified spherical link. Put

\[
m=m_-,\qquad c=\frac{m}{1-m}=3+2\sqrt2,
\qquad h=1-c^2,
\qquad n=-\frac{c^2}{h}=n_-.
\]

Define

\[
\mathcal B_-:\quad
W^2=c\,v(1-v)(1-cv)(1-c^2v),
\qquad
\Omega_-=-4c(1-cv)\frac{dv}{W}.
\tag{7B.1}
\]

The map

\[
x=\frac{mhv}{1-c^2v},
\qquad
y=\frac{m\sqrt{h/c}}{(1-c^2v)^2}W
\tag{7B.2}
\]

is an isomorphism of smooth compactifications
\(\Phi_-:\mathcal B_-\to C_-\). With

\[
\sqrt{h/c}=+i\sqrt{(c^2-1)/c},
\]

the differential identity is

\[
\boxed{\Phi_-^*\omega_-=i\Omega_-.}
\tag{7B.3}
\]

The upper-sheet pole is the image of

\[
P_\infty^-:\quad W/v^2\to-i c^2,
\qquad
\operatorname{Res}_{P_\infty^-}(i\Omega_-)=4.
\tag{7B.4}
\]

The upper and lower lateral paths pull back to relative boundary cycles
\(\delta_-^\uparrow,\delta_-^\downarrow\). In the \(v\)-coordinate each has
the form

```text
0 -> -infinity -> P_infinity^- -> +infinity -> 1,
```

with opposite choices of side at infinity. Their rational half-sum satisfies

\[
\boxed{
\delta_-^{\rm CPV}
=\frac12(\delta_-^\uparrow+\delta_-^\downarrow),
\qquad
\int_{\delta_-^{\rm CPV}}i\Omega_-=I_{\rm dual,CPV}.
}
\tag{7B.5}
\]

Thus the dual has an exact complex boundary-cycle interpretation. Its
two-dimensional lift is supplied by Section 7C.

---

## 7C. Dual complex surface-cycle lift

Put

\[
a=\frac1{1-c},
\qquad
b=\frac c{1-c},
\qquad c=3+2\sqrt2,
\]

and form

\[
\widetilde{\mathcal S}_c:\quad
ax^2-by^2+z^2=3,
\qquad
w^2=4(a^2x^2+b^2y^2+z^2).
\tag{7C.1}
\]

The algebraic curvature form is

\[
\mathcal K_c
=-48ab\,
\frac{\iota_{\nabla F_c}(dx\wedge dy\wedge dz)}{w^5}.
\tag{7C.2}
\]

In the algebraic hyperbolic coordinate \(\xi=\sinh u\), let

\[
Z^2=p+(p+b)\xi^2.
\]

The fiber primitive gives

\[
\int_{\ell_t}\mathcal K_c
=-\frac{2\sqrt{ab}}{p\sqrt{p+b}}dt.
\tag{7C.3}
\]

On the Stage-1 quartic coordinate,

\[
p=\frac1{1-cv},
\qquad
p+b=\frac{1-c^2v}{(1-c)(1-cv)}.
\tag{7C.4}
\]

The finite discriminants \(1/c^2\) and \(1/c\) lie in \((0,1)\), while the
dual path runs through the complementary arc via infinity. The fiber class
therefore transports along both lateral paths.

The four-quadrant construction uses one copy of each oriented angular branch,
one primitive oriented relative fiber interval, and coefficients only
\(\pm1\). Its side boundaries cancel pairwise over \(\mathbb Z\). It thus
defines an integral transfer on the admissible boundary subgroup,

\[
L_{\mathbb Z}:\mathcal H_{\mathbb Z}^{\rm adm}
\longrightarrow
H_2(\overline{\widetilde{\mathcal S}_c}\setminus D_q,
D_\infty;\mathbb Z),
\qquad
L_{\mathbb Z}(\delta)=\mathfrak C(\delta).
\tag{7C.5}
\]

Write

\[
\mathscr S_{\mathbb Z}^{\rm nat}:=\operatorname{im}L_{\mathbb Z}
\tag{7C.6}
\]

for the native swept surface lattice. This is not identified with the whole
integral surface homology. The two lateral images
\(\mathfrak C_-^\uparrow=L_{\mathbb Z}(\delta_-^\uparrow)\) and
\(\mathfrak C_-^\downarrow=L_{\mathbb Z}(\delta_-^\downarrow)\) satisfy

\[
\int_{\mathfrak C_-^\pm}\mathcal K_c
=\int_{\delta_-^\pm}\Omega_-.
\tag{7C.7}
\]

Only now extend coefficients and define
\(\Sigma_-^\pm=i\mathfrak C_-^\pm\). Then

\[
\int_{\Sigma_-^\uparrow}\mathcal K_c
=I_{\rm dual,CPV}-4\pi i,
\qquad
\int_{\Sigma_-^\downarrow}\mathcal K_c
=I_{\rm dual,CPV}+4\pi i,
\tag{7C.8}
\]

and

\[
\boxed{
\int_{\frac12(\Sigma_-^\uparrow+
\Sigma_-^\downarrow)}\mathcal K_c
=I_{\rm dual,CPV}.
}
\tag{7C.9}
\]

The dual diagonal equation is the original complexified keystone surface
under \((x,y,z)\mapsto(y,x,-z)\). The cycle in (7C.9) has complex
coefficients and is not asserted to be a real region. More precisely, the
normalized lateral classes lie over \(\mathbb Z[i]\), and their normalized
CPV half-sum lies over \(\mathbb Z[1/2,i]\). Their integral transport classes
are determined next.

---

## 7D. Integral Picard--Lefschetz transport

Let \(\sigma\) be the shear parameter and write

\[
\rho=\sqrt{1+\sigma^2},\qquad
c=\frac{\rho-1}{\rho+1},\qquad
m=\frac12-\frac1{2\rho},\qquad
n=-\frac{m^2}{1-2m}.
\tag{7D.1}
\]

An odd winding around \(\sigma=+i\) or \(-i\) changes \(\rho\) to \(-\rho\), so

\[
(c,m,n)\longmapsto(c^{-1},1-m,1-n).
\tag{7D.2}
\]

In the relative coordinate \(u=x/m\), the pole is

\[
u_p=\frac1n=\frac{2m-1}{m^2}.
\tag{7D.3}
\]

On the return stem from \(+i\), the continued value of \(m\) approaches
\(m_-\) from the lower half-plane. Since

\[
\frac{du_p}{dm}=\frac{2(1-m)}{m^3}>0
\quad\text{at }m=m_-,
\tag{7D.4}
\]

the pole approaches the final interval from below, selecting the upper
indentation. The route through \(-i\) gives the lower indentation.

Put

\[
\mathcal H_{\epsilon,\mathbb Z}
=H_1(C_\epsilon^\circ,\{Q_0,Q_m\};\mathbb Z),
\qquad
\Lambda_\epsilon^{\rm ell}
=\mathbb Z[A_\epsilon]+\mathbb Z[B_\epsilon].
\tag{7D.5}
\]

Here and below **modulo ordinary compact periods** means modulo
\(\Lambda_\epsilon^{\rm ell}\). The pole meridian is not included in this
submodule. If \(G_{+i}\) and \(G_{-i}\) denote Gauss--Manin transport along
the two specified corridors, then the primary relative class \(\delta_+\)
satisfies

\[
\boxed{
G_{+i}[\delta_+]=[\delta_-^\uparrow],
\qquad
G_{-i}[\delta_+]=[\delta_-^\downarrow]
\quad\text{in }\mathcal H_{-,\mathbb Z}/\Lambda_-^{\rm ell}.
}
\tag{7D.6}
\]

If \(\mu_-\) is the primitive positive meridian about the selected dual pole,
then

\[
\delta_-^\uparrow-\delta_-^\downarrow=-\mu_-,
\qquad
\delta_-^{\rm CPV}
=\delta_-^\uparrow+\frac12\mu_-.
\tag{7D.7}
\]

Thus the curve CPV class lies over \(\mathbb Z[1/2]\) but not over
\(\mathbb Z\). Both lateral classes have the same primitive endpoint boundary
\(\beta=[Q_m]-[Q_0]\). Every closed curve has boundary zero, so an integral
relative class congruent after complexification to \(i\delta_-^\pm\), even
modulo all closed cycles, would have to have boundary \(i\beta\). This is
impossible in \(\mathbb Z\beta\). Hence integral Picard--Lefschetz transport
does not replace the factor \(i\).

Surface-lift naturality gives, on the native swept lattice,

\[
\boxed{
G_{+i}^{\mathscr S}[\mathfrak C_+]
=[\mathfrak C_-^\uparrow],
\qquad
G_{-i}^{\mathscr S}[\mathfrak C_+]
=[\mathfrak C_-^\downarrow]
\pmod{L_{\mathbb Z}(\Lambda_-^{\rm ell})}.
}
\tag{7D.8}
\]

The actual integral transports have the unnormalized curvature periods

\[
\int_{G_{+i}^{\mathscr S}\mathfrak C_+}\mathcal K_c
\equiv-iI_{\rm dual,CPV}-4\pi,
\qquad
\int_{G_{-i}^{\mathscr S}\mathfrak C_+}\mathcal K_c
\equiv-iI_{\rm dual,CPV}+4\pi
\pmod{\Lambda_{\mathcal K}^{\rm ell}}.
\tag{7D.9}
\]

The surface non-descent statement is proved in Section 7F for
\(\mathscr S_{\mathbb Z}^{\rm nat}\). No assertion is made there about
arbitrary classes in the whole surface relative-homology group.

---

## 7E. Pole-free finite-interval compilation

The trace-path formulas can be compiled into ordinary algebraic integrals on
the fixed interval \([0,1]\). This is a consequence of the preceding period
theorems, not a new geometric realization.

Define

\[
J_+=\int_{\Gamma_+}\Theta,
\qquad
H_-=-i\operatorname{CPV}\int_{\Gamma_-}\Theta.
\tag{7E.1}
\]

Then

\[
I_{\rm primary}=\frac12J_+-2\pi,
\qquad
I_{\rm dual,CPV}=\frac12H_-.
\tag{7E.2}
\]

Put \(w=1-t\) and \(s=\sqrt2\), and define

\[
P_+(t)=t^4+2t^2w^2+2w^4,
\tag{7E.3}
\]

\[
g_+(t)=
16\frac{t^2-2w^2}{t^2+8w^2}\frac1{\sqrt{P_+(t)}},
\tag{7E.4}
\]

\[
P_-(t)=t^4-2t^2w^2+2w^4
=(t^2-w^2)^2+w^4,
\tag{7E.5}
\]

\[
g_-(t)=
-\frac{16t^2}
{\sqrt{P_-(t)}
\left(t^2+2w^2+s\sqrt{P_-(t)}\right)}.
\tag{7E.6}
\]

### Theorem 7E.1 — native pole-free kernels

The two DBP trace periods satisfy

\[
\boxed{
J_+=\int_0^1g_+(t)\,dt,
\qquad
H_-=\int_0^1g_-(t)\,dt.
}
\tag{7E.7}
\]

Both radicands are strictly positive on \([0,1]\), both integrands extend
continuously to the endpoints, and no principal-value operation remains in
the dual kernel.

#### Proof: primary path

On

\[
\Gamma_+:X=1\longrightarrow+\infty
\]

set \(X=1+z^2\), \(z\in[0,\infty)\). Then

\[
Y=z\sqrt{z^4+2z^2+2},
\]

and direct substitution into \(\Theta\) gives

\[
J_+=
\int_0^\infty
16\frac{z^2-2}{z^2+8}
\frac{dz}{\sqrt{z^4+2z^2+2}}.
\tag{7E.8}
\]

With

\[
z=\frac{t}{1-t}=\frac tw,
\tag{7E.9}
\]

clearing the common power \(w^{-4}\) under the square root transforms
(7E.8) into the first identity in (7E.7). The endpoint values are

\[
g_+(0)=-2\sqrt2,
\qquad
g_+(1)=16.
\tag{7E.10}
\]

The polynomial \(P_+\) is a sum of nonnegative terms, and \(t,w\) cannot
vanish simultaneously. Hence \(P_+>0\) on the closed interval.

#### Proof: dual path and exact polar subtraction

On

\[
\Gamma_-:X=1\longrightarrow-\infty
\]

use the sheet

\[
Y=+i\sqrt{-(X-1)(X^2+1)},
\qquad X<1,
\]

and set \(X=1-z^2\), \(z\in[0,\infty)\). For
\(\beta=-i\Theta\),

\[
H_-=\operatorname{CPV}\int_0^\infty h_-(z)\,dz,
\]

\[
h_-(z)=
16\frac{z^2+2}{z^2-8}
\frac1{\sqrt{z^4-2z^2+2}}.
\tag{7E.11}
\]

The pole is at \(z_0=2\sqrt2\) and has residue four. Introduce the exact
polar kernel

\[
p(z)=\frac{16\sqrt2}{z^2-8}
=\frac d{dz}
\left[
4\log\left|
\frac{z-2\sqrt2}{z+2\sqrt2}
\right|
\right].
\tag{7E.12}
\]

It has the same residue and

\[
\operatorname{CPV}\int_0^\infty p(z)\,dz=0.
\tag{7E.13}
\]

Therefore

\[
H_-=\int_0^\infty r_-(z)\,dz,
\]

\[
r_-(z)=
\frac{16}{z^2-8}
\left(
\frac{z^2+2}{\sqrt{z^4-2z^2+2}}-\sqrt2
\right).
\tag{7E.14}
\]

The apparent singularity is removable; its value at \(z_0\) is

\[
r_-(z_0)=-\frac{16\sqrt2}{25}.
\tag{7E.15}
\]

After the compactification (7E.9), put

\[
A=t^2+2w^2,
\qquad
D=t^2-8w^2.
\]

The initial compactified kernel is

\[
16\frac{A/\sqrt{P_-}-\sqrt2}{D}.
\tag{7E.16}
\]

The exact identity

\[
A^2-2P_-=-t^2D
\tag{7E.17}
\]

rationalizes the numerator and cancels \(D\) identically, yielding (7E.6).
Moreover,

\[
g_-(0)=0,
\qquad
g_-(1)=16(1-\sqrt2),
\tag{7E.18}
\]

and at the former pole

\[
t_0=\frac{2\sqrt2}{1+2\sqrt2},
\qquad
g_-(t_0)=-\frac{128+144\sqrt2}{25}.
\tag{7E.19}
\]

Finally,

\[
P_-=(t^2-w^2)^2+w^4>0
\]

on \([0,1]\). This proves continuity, positivity of the radicand, and the
second identity in (7E.7). \(\square\)

### Evaluator scope

The theorem compiles exactly the two fixed DBP path claims. The primary route
requires one ordinary integral and a certified value of \(\pi\); the dual
route requires one ordinary integral and no runtime CPV operation. The pole
and residue remain in the certificate ledger even though they disappear from
the execution kernel. No claim is made here about a general elliptic-integral
normal form or arbitrary parameter family.

---

## 7F. Native transport and scalar-extension separation

This subsection packages Sections 7B--7D as a morphism theorem. Its base is
the two corridor system actually used in the Picard--Lefschetz calculation;
it is not a global assertion over the entire shear-parameter plane.

### Parameter cover and admissible corridors

Let

\[
\widetilde U^\circ=
\left\{(\sigma,\rho)\in\mathbb C^2:
\rho^2=1+\sigma^2,
\ \rho\ne0,
\ \sigma\ne0\right\}.
\tag{7F.1}
\]

On this cover put

\[
c=\frac{\rho-1}{\rho+1},
\qquad
m=\frac{\rho-1}{2\rho},
\qquad
n=-\frac{m^2}{1-2m}.
\tag{7F.2}
\]

The deck involution

\[
\tau(\sigma,\rho)=(\sigma,-\rho)
\tag{7F.3}
\]

obeys

\[
c\tau=c^{-1},
\qquad
m\tau=1-m,
\qquad
n\tau=1-n.
\tag{7F.4}
\]

Let

\[
u_+=(1,\sqrt2),
\qquad
u_-=(1,-\sqrt2).
\]

Write \(\ell_\uparrow\) and \(\ell_\downarrow\) for the lifted Stage-3
corridors from \(u_+\) to \(u_-\) about \(\sigma=+i\) and \(\sigma=-i\),
respectively.

**Lemma 7F.A — exact representatives of the two DBP corridors.** The upper
corridor is represented in the \(\sigma\)-plane by the certified seven-segment
\(\mathbb Q(i)\) polygon with word \(a_+\), counterclockwise about
\(\sigma=+i\). The lower is its complex conjugate, with word \(a_-^{-1}\),
clockwise about \(\sigma=-i\). Each admits an open radius-\(1/8\) curve-level
tube avoiding \(\sigma=0\) and \(\rho=0\); its lift from
\((1,+\sqrt2)\) is unique in the nonsingular pullback cover and ends at
\((1,-\sqrt2)\). On the return stem the upper route has
\(\operatorname{Im}(m)<0\) and selects \(\delta_-^\uparrow\); the lower has
\(\operatorname{Im}(m)>0\) and selects \(\delta_-^\downarrow\). Therefore
\(G_\uparrow[\delta_+]=[\delta_-^\uparrow]\) and
\(G_\downarrow[\delta_+]=[\delta_-^\downarrow]\) modulo
\(\mathbb Z[A_-]+\mathbb Z[B_-]\).

For absolute representatives retain the independent unresolved corrections

\[
G_\uparrow(\delta_+)=\delta_-^\uparrow+\lambda_\uparrow,
\qquad
G_\downarrow(\delta_+)=\delta_-^\downarrow+\lambda_\downarrow,
\qquad
\lambda_\uparrow,\lambda_\downarrow\in
\mathbb Z[A_-]+\mathbb Z[B_-].
\tag{7F.5a}
\]

This is a curve-level corridor statement; it does not certify a surface sweep.
The exact representatives and clearance witnesses are the CCE-2 manifests and
route certificates.

Choose thin tubular neighbourhoods on which

\[
m\notin\{0,1,\infty\},
\tag{7F.5}
\]

the two third-kind poles remain distinct from each other and the marked
endpoints, and the swept boundary chain avoids \(v=1/c,1/c^2\), the norm
discriminant, and the polar divisor. These are the **admissible corridors**
in the theorem below.

For \(u\) on either corridor define

\[
C_u:y^2=x(x-1)(x-m(u)),
\qquad
C_u^\circ=C_u\setminus\{P_u^+,P_u^-\},
\tag{7F.6}
\]

where \(P_u^\pm\) lie over

\[
x_p=\frac mn=2-\frac1m.
\]

With \(Q_0=(0,0)\) and \(Q_m=(m,0)\), put

\[
\mathscr H_{\mathbb Z}(u)
=H_1(C_u^\circ,\{Q_0,Q_m\};\mathbb Z).
\tag{7F.7}
\]

Along each corridor these groups form an integral Gauss--Manin local system.
Its endpoint exact sequence contains

\[
0\longrightarrow H_1(C_u^\circ;\mathbb Z)
\longrightarrow\mathscr H_{\mathbb Z}(u)
\mathop{\longrightarrow}^{\partial_C}
\mathbb Z\beta\longrightarrow0,
\qquad
\beta=[Q_m]-[Q_0].
\tag{7F.8}
\]

Fix a Gauss--Manin marking of the ordinary elliptic lattice

\[
\Lambda^{\rm ell}(u)=\mathbb Z[A_u]+\mathbb Z[B_u].
\tag{7F.9}
\]

### Theorem 7F.1 — native transport, lift naturality, and coefficients

On each admissible corridor the following hold.

1. **Integral lateral transport.** The Gauss--Manin isomorphisms
   \(G_\uparrow,G_\downarrow:\mathscr H_{\mathbb Z}(u_+)\to
   \mathscr H_{\mathbb Z}(u_-)\) satisfy

   \[
   \begin{aligned}
   G_\uparrow(\delta_+)
   &=\delta_-^\uparrow+\lambda_\uparrow,\\
   G_\downarrow(\delta_+)
   &=\delta_-^\downarrow+\lambda_\downarrow,
   \end{aligned}
   \qquad
   \lambda_\uparrow,\lambda_\downarrow\in\Lambda_-^{\rm ell}.
   \tag{7F.10}
   \]

2. **Integral swept transfer.** The Stage-2 construction restricts to a
   homomorphism

   \[
   L_{\mathbb Z,u}:\mathscr H_{\mathbb Z}^{\rm adm}(u)
   \longrightarrow H_2(X_u,Y_u;\mathbb Z),
   \tag{7F.11}
   \]

   where

   \[
   X_u=\overline{\widetilde{\mathcal S}_u}\setminus D_q,
   \qquad
   Y_u=D_\infty\cap X_u.
   \tag{7F.12}
   \]

   Its image is \(\mathscr S_{\mathbb Z}^{\rm nat}(u)\). There is an
   integral signed reduction

   \[
   R_{\mathbb Z,u}:\mathscr S_{\mathbb Z}^{\rm nat}(u)
   \longrightarrow\mathscr H_{\mathbb Z}^{\rm adm}(u)
   \tag{7F.13}
   \]

   such that

   \[
   \boxed{R_{\mathbb Z,u}L_{\mathbb Z,u}=4\operatorname{id}.}
   \tag{7F.14}
   \]

   In particular \(L_{\mathbb Z,u}\) is injective.

3. **Naturality and pairing.** If \(G_\eta^C\) and
   \(G_\eta^{\mathscr S}\) denote curve and surface transport along
   \(\eta\in\{\uparrow,\downarrow\}\), then

   \[
   \boxed{
   G_\eta^{\mathscr S}L_{\mathbb Z,u_+}
   =L_{\mathbb Z,u_-}G_\eta^C.
   }
   \tag{7F.15}
   \]

   Moreover,

   \[
   \boxed{
   \int_{L_{\mathbb Z,u}(\delta)}\mathcal K_u
   =\int_\delta\Omega_u.
   }
   \tag{7F.16}
   \]

4. **Native morphism.** For either corridor separately, take its fundamental
   groupoid, its admissible oriented subgroupoid, its regular/wall stratum
   poset, and the source representation

   \[
   (\mathscr H_{\mathbb Z}^{\rm adm},\Lambda^{\rm ell},[\delta]).
   \]

   Give the target the representation

   \[
   (\mathscr S_{\mathbb Z}^{\rm nat},
   L_{\mathbb Z}(\Lambda^{\rm ell}),[L_{\mathbb Z}(\delta)]).
   \]

   Then

   \[
   (\operatorname{id},\operatorname{id},L_{\mathbb Z})
   \tag{7F.17}
   \]

   is a native \(\mathbb Z\)-morphism of selected quotient groupoids in the
   sense of the companion category theorem.

5. **Exact coefficient separation.** With \(\mu_-\) the primitive selected
   pole meridian,

   \[
   \delta_-^\uparrow-\delta_-^\downarrow=-\mu_-,
   \qquad
   \delta_-^{\rm CPV}
   =\delta_-^\uparrow+\frac12\mu_-.
   \tag{7F.18}
   \]

   The minimal displayed coefficient rings are

   | class | coefficient ring |
   |---|---:|
   | \(\delta_-^\uparrow,\delta_-^\downarrow\) and their native lifts | \(\mathbb Z\) |
   | \(\delta_-^{\rm CPV}\) and its native lift | \(\mathbb Z[1/2]\), not \(\mathbb Z\) |
   | \(i\delta_-^\uparrow,i\delta_-^\downarrow\) and their native lifts | \(\mathbb Z[i]\), not \(\mathbb Z\) |
   | \(i\delta_-^{\rm CPV}\) and its native lift | \(\mathbb Z[1/2,i]\) |

   Thus \(\mathbb Z\to\mathbb Q\to\mathbb C\) is valid only as a coarse
   scalar-extension ladder.

6. **No integral replacement for \(i\).** Multiplication by \(i\) cannot be
   implemented by an integral Picard--Lefschetz class after adding closed
   curve cycles. The same obstruction holds in
   \(\mathscr S_{\mathbb Z}^{\rm nat}\) after adding lifted closed surface
   cycles.

#### Proof

Part 1 is the pole-side calculation of Section 7D. The return stem about
\(+i\) approaches the dual pole from below and selects the upper indentation;
the return stem about \(-i\) selects the lower indentation. Gauss--Manin
transport is integral, and the unspecified closed correction lies in the
marked \(A/B\) module, proving (7F.10).

For Part 2, the swept chain uses the four angular sign branches, a primitive
oriented relative fiber interval, and coefficients \(\pm1\). All angular
side boundaries cancel in integral pairs and the fiber ends are relative to
\(Y_u\); hence the construction preceding (7C.5) is defined over
\(\mathbb Z\), proving (7F.11).

Let

\[
G=\{(+,+),(-,+),(-,-),(+,-)\}\cong(\mathbb Z/2)^2,
\qquad
\chi(\varepsilon_C,\varepsilon_S)=\varepsilon_C\varepsilon_S.
\tag{7F.19}
\]

The alternating angular orientation is the signed transfer

\[
\operatorname{Tr}_\chi(\gamma)
=\sum_{g\in G}\chi(g)\gamma_g.
\tag{7F.20}
\]

Define signed reduction by multiplying the \(g\)-branch by \(\chi(g)\) and
projecting it to the base chain, then cap the relative fiber interval with
its primitive integral dual class. This is a chain map on the native transfer
subcomplex. Consequently

\[
R_{\mathbb Z}\operatorname{Tr}_\chi(\gamma)
=\sum_{g\in G}\chi(g)^2\gamma=4\gamma.
\tag{7F.21}
\]

This proves (7F.14). The relative groups in (7F.7) are free abelian, so
\(4\delta=0\) implies \(\delta=0\); therefore \(L_{\mathbb Z}\) is
injective. Notice that \(\tfrac14R_{\mathbb Z}\) is a left inverse only
after inverting 2. Equation (7F.14) alone does not make a lifted meridian
primitive in the whole surface lattice.

For Part 3 choose a Gauss--Manin-flat family of boundary representatives
along either corridor. Conditions (7F.5) and the admissibility requirements
ensure that the two fiber endpoints stay distinct, the relative fiber class
stays flat, and the four angular branches retain their gluing pattern. The
swept chains therefore form an isotopy of integral relative chains. Sweeping
before or after transport gives the same class, proving (7F.15). Fiber
integration, with the primary orientation calibration, is exactly (7F.16).

Part 4 now follows directly. Equation (7F.15) says that
\(L_{\mathbb Z}\) is a natural transformation; it sends
\(\Lambda^{\rm ell}\) into its lifted compact-period submodule and preserves
the selected lateral quotient class. These are precisely the native-morphism
conditions. The upper and lower corridors are treated as two separate
admissible groupoids because their endpoint classes differ by the meridian.

For Part 5, the local indentation relation gives (7F.18). The pole meridian
is primitive in \(H_1(C_-^\circ;\mathbb Z)\), so its half is not integral.
If the native CPV lift were integral in
\(\mathscr S_{\mathbb Z}^{\rm nat}\), injectivity and (7F.14) would force the
curve CPV class to be integral, a contradiction. Multiplication by \(i\) and
the combination of the midpoint with \(i\) give exactly the other two rings
in the table.

Finally, either lateral class and the CPV class have endpoint boundary
\(\beta\). If an integral curve class \(z\) were congruent after
complexification to \(i\delta\) modulo any closed curve class, then

\[
\partial_Cz=i\beta,
\tag{7F.22}
\]

which is impossible because \(\partial_Cz\in\mathbb Z\beta\). On the native
swept lattice define

\[
\partial_{\mathscr S}:=\partial_C R_{\mathbb Z}.
\tag{7F.23}
\]

Then

\[
\partial_{\mathscr S}L_{\mathbb Z}(\delta)=4\partial_C\delta.
\tag{7F.24}
\]

Lifted closed cycles lie in its kernel, whereas an \(i\)-normalized lateral
or CPV lift has boundary \(4i\beta\), outside \(\mathbb Z\beta\). This proves
Part 6. \(\square\)

### Exact scope of the surface conclusion

The theorem proves coefficient non-descent inside the actual native image
\(\mathscr S_{\mathbb Z}^{\rm nat}\). It does not prove that the lifted
meridian is primitive or that the CPV midpoint is nonintegral in the whole
group \(H_2(X_-,Y_-;\mathbb Z)\). Extending the conclusion to arbitrary
surface classes requires an integral extension of \(R_{\mathbb Z}\), or an
equivalent local-product/intersection functional, on that full group.

---

## 8. Pole transport and non-torsion trace sector

Both complementary pole pairs map to

\[
X=-7.
\tag{8.1}
\]

On \(E_{128}\),

\[
P=(-7,20i),
\qquad
-P=(-7,-20i).
\tag{8.2}
\]

The residues are

\[
\operatorname{Res}_{P}(\Theta)=4i,
\qquad
\operatorname{Res}_{P}(-i\Theta)=4.
\tag{8.3}
\]

The point \(P\) is non-torsion. Exact good reductions give:

\[
\operatorname{ord}_{\mathbb F_{13}}(\bar P)=4,
\qquad
\operatorname{ord}_{\mathbb F_{29}}(\bar P)=6.
\]

If \(P\) had finite order \(N\), good reduction would force both

\[
N=4\cdot13^a
\qquad\text{and}\qquad
N=6\cdot29^b,
\]

which is impossible. Therefore the pole divisor of \(\Theta\) is non-torsion.

This non-torsion statement belongs to the **trace sector**. It does not imply non-reducibility of \(\alpha_\epsilon\), because

\[
(\phi_\epsilon)_*\alpha_\epsilon=0
\]

and \(\alpha_\epsilon=R_\epsilon d\log f_\epsilon\).

---

## 9. Exact completion boundary

### Closed

1. Complementary DBP parameters and coefficient involution.
2. Explicit degree-two isogenies \(C_\epsilon\to E_{128}\).
3. Common trace differential \(\Theta\).
4. Exact trace identity.
5. Explicit anti-invariant rational coefficient.
6. Complete-interval \(K/\Pi\) reduction of the anti-period.
7. Exact logarithmic form of the anti differential.
8. Primary anti-period \(-4\pi\).
9. Dual CPV anti-period \(0\), with one-sided values \(\pm4\pi i\).
10. Exact primary and dual trace-path formulas.
11. Pole transport to \(X=-7\), residue \(4\), and non-torsion of the trace pole.
12. Primary scalar surface-to-link-to-period interface, including an explicit
    global primitive and exact evaluation of both cone ends.
13. Dual complex boundary-cycle interface, including the exact metric-quartic
    map, the point-at-infinity pole, both lateral classes, and their CPV
    half-sum.
14. Integral swept surface transfer on the norm double cover, including the
    fiber pushforward, lateral image classes, and coefficient-extended CPV
    half-sum.
15. Upper and lower integral Picard--Lefschetz transport classes modulo
    ordinary compact periods.
16. Primitive curve-meridian proof that the CPV midpoint is defined over
    \(\mathbb Z[1/2]\) but not \(\mathbb Z\), and its transfer to the native
    swept surface lattice by injectivity.
17. Boundary-lattice obstruction to replacing the normalization factor
    \(i\) by an integral curve class or native swept surface class modulo
    the corresponding closed-period submodule.
18. Corridor-restricted native-morphism theorem, including
    \(R_{\mathbb Z}L_{\mathbb Z}=4\operatorname{id}\), lift naturality, and
    the exact coefficient-ring diamond.
19. Pole-free primary and dual finite-interval kernels, including exact
    pre-evaluation cancellation of the dual pole.

### Not claimed

The theorem does not claim

\[
I_{\rm primary}
=
\alpha(\sqrt2)I_{\rm dual,CPV}
+\text{elementary correction}.
\]

Equations (7.4) and (7.6) involve different relative paths of the non-torsion differential \(\Theta\). Comparing those paths is a separate relative-homology problem. Non-torsion alone neither proves nor disproves every possible scalar relation between their special values.

More exactly, the open or excluded claims are:

```text
OPEN / NOT CLAIMED
  exact A/B coefficients comparing Gamma_+ and Gamma_-
  complete A/B monodromy matrices on the full relative basis
  a scalar algebraic relation between the two special values
  a second real dual surface region
  transcendence or algebraic independence
  the local curvature-valuation interface
  coefficient non-descent for arbitrary classes in the full surface lattice
```

The last item is narrower than the closed native-image result: it requires an
integral extension of the signed reduction to all of
\(H_2(X_-,Y_-;\mathbb Z)\), or an equivalent intersection calculation.

---

## 10. Verification

The computational supplement is a verifier matrix, not a single completion
claim:

| component | exact verifier | recorded result |
|---|---|---:|
| Landen trace and logarithmic anti differential | `verify_dbp_landen_trace_theorem_v1_1.py` | 75 gates |
| native finite-interval compilation | `verify_dbp_native_relative_period_route.py` | source certificate retained |
| boundary metric quartic | `verify_dbp_dual_surface_cycle_stage1.py` | 22/22 |
| swept surface transfer | `verify_dbp_dual_surface_cycle_stage2.py` | 17/17 |
| lateral Picard--Lefschetz lattice | `verify_dbp_dual_surface_cycle_stage3.py` | 22/22 |

The Landen verifier checks, among other identities:

- \(n_\epsilon=-m_\epsilon^2/(1-2m_\epsilon)\);
- \(A_\epsilon m_\epsilon=1-m_\epsilon\);
- \(d_\epsilon/(m_\epsilon-n_\epsilon)=1-m_\epsilon\);
- the explicit anti-invariant rational coefficient;
- its complete-interval pullback;
- the complete \(K/\Pi\) partial fraction;
- the logarithmic numerator identity;
- the logarithmic denominator factorization;
- the \(d\log\) kernel;
- \(\ell_\epsilon^2=z_{0,\epsilon}\);
- the exact residue normalization;
- the two endpoint values.

All reported gates are exact. They do not by themselves verify the new
topological statements (7F.14)--(7F.17); those follow from the signed-transfer
and isotopy proofs in Section 7F. No special-function package,
floating-point comparison, imported Landen formula, or transcendence
assumption is used in the exact gates.

---

*End of Curvature Periods of the DBP Quadric, consolidated theorem v1.0.*
