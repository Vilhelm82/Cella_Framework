# DBP Landen–Trace Theorem

## Corrected and completed trace-and-splitting theorem, v1.1

**Date:** 2026-07-12  
**Supersedes mathematically:** v1.0 wherever v1.0 described the anti-translation period as an unresolved analytic component  
**Preservation policy:** v1.0 and every supplied source remain unchanged  
**Primary surface interface:** \`DBP_SURFACE_TO_LINK_CLOSEOFF_v1.0.md\`  
**Verification:** verify_dbp_landen_trace_theorem_v1_1.py; 75 exact gates, no floating-point arithmetic

---

## 0. Status

The DBP Landen–Trace theorem is complete as a theorem about:

1. the two complementary DBP complete-integral differentials;
2. their explicit degree-two isogenies to \(E_{128}\);
3. their common descended trace differential;
4. their exact anti-translation differentials;
5. the exact primary and dual anti-periods;
6. the pole transport, CPV prescriptions, and monodromy;
7. the primary scalar interface from the original DBP curvature integral to
   the period \(I_{\rm primary}\), using the surface-to-link close-off.

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
S_s=\{D^2+sDS+P^2=3\},\qquad s\ne0,
\]

and let \(\Gamma_s^+\) be one component of the spherical link of the
asymptotic cone \(D^2+sDS+P^2=0\). The surface-to-link close-off proves

\[
\boxed{
\int_{S_s}K_G\,dA=-2L(\Gamma_s^+).
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

### Not claimed

The theorem does not claim

\[
I_{\rm primary}
=
\alpha(\sqrt2)I_{\rm dual,CPV}
+\text{elementary correction}.
\]

Equations (7.4) and (7.6) involve different relative paths of the non-torsion differential \(\Theta\). Comparing those paths is a separate relative-homology problem. Non-torsion alone neither proves nor disproves every possible scalar relation between their special values.

The primary scalar identity
\(\int_{S_1}K_GdA=I_{\rm primary}\) is now proved by the surface-to-link
close-off and the exact link-to-Legendre reduction. What remains separate is a
chain-level pushforward of the original curvature two-form to
\(\omega_+\), the interface with the local curvature valuation calculus, and
any surface-cycle interpretation of \(I_{\rm dual,CPV}\).

---

## 10. Verification

Run:

    python3 verify_dbp_landen_trace_theorem_v1_1.py

The verifier first executes every v1.0 isogeny, trace, residue, modular-polynomial, and non-torsion gate. It then checks:

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

All 75 exact gates pass. No special-function package, floating-point comparison, imported Landen formula, or transcendence assumption is used.

---

*End of corrected and completed DBP Landen–Trace Theorem v1.1.*
