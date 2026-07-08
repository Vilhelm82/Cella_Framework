# Canonical Invariant Reduction Theorem — Channel/Gauge Form

## Theorem: Channel account reduces canonically to invariant curvature

Let \(F:\mathbb R^n\to\mathbb R\) define a smooth hypersurface \(F=0\) at a regular point \(x\), with

\[
g=\nabla F(x),\qquad H=\nabla^2F(x),\qquad q=g^Tg\ne0.
\]

Fix the privileged coordinate basis and split the Hessian into self and coupling parts:

\[
H=H_s+H_c,
\qquad
H_s=\operatorname{diag}(H),
\qquad
H_c=H-H_s.
\]

For \(1\le r\le n-1\), define the channel-density polynomial

\[
\widehat{\mathcal C}_r(t,u)
=
(-1)^{r+1}
\sum_{|I|=r+1}
\det
\begin{pmatrix}
0 & g_I^T\\
g_I & (tH_c+uH_s)_I
\end{pmatrix}.
\]

Expand

\[
\widehat{\mathcal C}_r(t,u)
=
\sum_{p+q=r}t^pu^q\widehat\kappa_{r;p,q}.
\]

Then the normalized channel curvatures are

\[
\kappa_{r;p,q}=\frac{\widehat\kappa_{r;p,q}}{q^{(r+2)/2}},
\]

and the canonical elementary curvature invariant is their sum:

\[
\boxed{
\sigma_r
=
\sum_{p+q=r}\kappa_{r;p,q}
=
\frac{\widehat{\mathcal C}_r(1,1)}{q^{(r+2)/2}}.
}
\]

Equivalently, the channel vector

\[
C_r=(\kappa_{r;r,0},\kappa_{r;r-1,1},\ldots,\kappa_{r;0,r})
\]

has a canonical reduction map

\[
\boxed{
\Sigma:C_r\longmapsto \sum_{p+q=r}\kappa_{r;p,q}=\sigma_r.
}
\]

Thus the invariant object is the quotient

\[
\boxed{
C_r/\ker\Sigma\cong \sigma_r,
\qquad
\ker\Sigma=
\{\delta C_r:\sum\delta\kappa_{r;p,q}=0\}.
}
\]

The channel decomposition is therefore not itself an intrinsic scalar invariant. It is an exact account of how the invariant curvature is distributed across self/coupling/interactions in a chosen chart, basis, and defining-function gauge. The total curvature is invariant; the channel account is a representative in the affine fiber over that invariant.

---

## The three-variable Gaussian case

For \(n=3\), \(r=2\), the theorem reduces to

\[
C_2=(\kappa_c,\kappa_{int},\kappa_s),
\]

with

\[
\boxed{
K_G=\kappa_c+\kappa_s+\kappa_{int}.
}
\]

The zero-sum transport plane is

\[
\boxed{
\ker\Sigma
=\{(a,b,c):a+b+c=0\}.
}
\]

So any chart or gauge change preserving the represented surface may move the channel triple, but only inside the affine plane

\[
\boxed{
\kappa_c+\kappa_s+\kappa_{int}=K_G.
}
\]

For the keystone

\[
F=x_1^2+x_1x_2+x_3^2-3
\quad\text{at}\quad(1,1,1),
\]

this gives the canonical base representative

\[
\boxed{
(\kappa_c,\kappa_s,\kappa_{int})
=
\left(-\frac1{49},\frac1{49},-\frac3{49}\right),
\qquad
K_G=-\frac3{49}.
}
\]

---

## Gauge transport law

A defining-function gauge

\[
\widetilde F=\mu F,
\qquad \mu(x)=1,
\qquad a=\nabla\log\mu(x),
\]

fixes the gradient and shifts the Hessian by

\[
\boxed{
\widetilde g=g,
\qquad
\widetilde H=H+ga^T+ag^T.
}
\]

Because the tangent projector \(P=I-gg^T/q\) satisfies \(Pg=0\),

\[
P(ga^T+ag^T)P=0.
\]

Therefore every total elementary curvature \(\sigma_r\) is preserved, while the channel account may change:

\[
\boxed{
C_r(\widetilde g,\widetilde H)-C_r(g,H)\in\ker\Sigma.
}
\]

For \(n=3,r=2\), this is exactly

\[
\boxed{
\delta\kappa_c+\delta\kappa_s+\delta\kappa_{int}=0.
}
\]

This is the true chart-change action: not scalar change, but zero-sum redistribution of channel account.

---

## Passive role permutations are trivial

For a permutation matrix \(P_\sigma\),

\[
(g,H)\mapsto(P_\sigma g,P_\sigma HP_\sigma^T)
\]

is only a passive coordinate relabelling. Since

\[
\operatorname{diag}(P_\sigma HP_\sigma^T)
=P_\sigma\operatorname{diag}(H)P_\sigma^T,
\]

the self/coupling split is equivariant. Hence

\[
\boxed{
C_r(P_\sigma g,P_\sigma HP_\sigma^T)=C_r(g,H)
}
\]

up to label order. The passive \(S_n\) orbit collapses to a singleton. It is a covariance check, not a new invariant.

The nontrivial role action is active recharting: solving the same relation in a different output role changes the defining function, hence induces a gauge transport. Total curvature remains fixed; channel representatives can differ by zero-sum shifts.

---

## Single-edge coupling corollary, n=3

Define the weighted coupling-edge vector

\[
\nu=(g_1H_{23},\,g_2H_{13},\,g_3H_{12}).
\]

Then

\[
\boxed{
\Delta_c=\nu^T(2I-\mathbf1\mathbf1^T)\nu,
}
\]

so the pure coupling channel is governed by a Lorentzian quadratic form.

For a pure single-axis gauge \(a=te_i\), with \(\{i,j,k\}=\{1,2,3\}\),

\[
\boxed{
\delta\kappa_c(te_i)
=
\frac{4t\,g_1g_2g_3H_{jk}}{q^2}.
}
\]

Thus a single-axis gauge preserves \(\kappa_c\) exactly when the opposite coupling edge vanishes:

\[
\boxed{
te_i\text{ pins }\kappa_c
\iff
H_{jk}=0.
}
\]

For the keystone, the only active coupling edge is \(H_{12}=1\). Therefore the \(e_1\) and \(e_2\) gauges preserve \(\kappa_c\), while the \(e_3\) gauge moves it.

---

## Canonical invariant reduction

The whole construction reduces to the exact sequence

\[
\boxed{
0\longrightarrow\ker\Sigma
\longrightarrow
\operatorname{ChannelAccount}_r
\xrightarrow{\ \Sigma\ }
\operatorname{InvariantCurvature}_r
\longrightarrow0.
}
\]

In words:

\[
\boxed{
\text{channel account}
=
\text{canonical invariant}
+
\text{zero-sum gauge residue}.
}
\]

So the pure form is:

> **Compute the full channel spectrum, then reduce by the summation quotient. The quotient is the intrinsic curvature invariant; the fiber is the exact channel account explaining how that invariant is represented in the chosen chart.**

This unifies the three-channel \(K_G\), gauge-transport table, role-chart correction, and single-axis pinning lemma into one canonical invariant reduction.
