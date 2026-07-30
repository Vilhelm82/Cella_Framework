# Three-Channel K_G — Mathematical Extension Notes

This note is not a prose polish of the canonical three-channel specification. It is an expansion of the mathematical reach of the object.

The starting object is the signed, basis-relative split

\[
H = H_c + H_s,\qquad H_s=\operatorname{diag}(H),\qquad H_c=H-H_s,
\]

with \(g=\nabla F\), \(q=g^Tg\), and the hypersurface \(F=0\) at a regular point \(g\ne 0\).

For a surface in \(\mathbb R^3\), the canonical spec gives

\[
K_G=\kappa_c+\kappa_s+\kappa_{int},\qquad
\kappa_c=-\Delta_c/q^2,
\quad \kappa_s=-\Delta_s/q^2,
\quad \kappa_{int}=-\Delta_m/q^2.
\]

This document pushes that object outward in five directions:

1. all elementary curvature invariants, not just Gaussian curvature;
2. all powers/traces of the split shape operator;
3. exact rational density laws in arbitrary dimension;
4. a 3D channel phase-space normal form;
5. power-family formulas for monomial and Fermat-type surfaces.

---

## 1. Universal bordered-minor lift: all elementary curvatures

Let the ambient dimension be \(n\), so the hypersurface dimension is \(m=n-1\). Let \(\sigma_r(S)\) denote the \(r\)-th elementary symmetric curvature of the shape operator \(S\), for \(1\le r\le m\):

\[
\det(I+zS)=\sum_{r=0}^{m} z^r\sigma_r(S),
\qquad \sigma_0=1.
\]

Here \(\sigma_1=\operatorname{tr}S\), \(\sigma_2\) is the second elementary curvature, and \(\sigma_m\) is Gaussian-Kronecker curvature.

For each \(r\), define the bordered-minor polynomial

\[
\boxed{
\mathcal E_r(t,u)
=
(-1)^{r+1}
\sum_{|I|=r+1}
\det
\begin{pmatrix}
0 & g_I^T\\
g_I & (tH_c+uH_s)_I
\end{pmatrix}
}
\]

where \(I\) ranges over all coordinate subsets of size \(r+1\), and \(g_I,H_I\) mean restriction to those coordinates.

Then

\[
\boxed{
\sigma_r(S)=\frac{\mathcal E_r(1,1)}{q^{(r+2)/2}}
}
\]

and, since \(\mathcal E_r(t,u)\) is homogeneous of degree \(r\), define the channel pieces by

\[
\boxed{
\sigma_{r;p,q}
=
\frac{[t^p u^q]\mathcal E_r(t,u)}{q^{(r+2)/2}},
\qquad p+q=r.
}
\]

Thus

\[
\boxed{
\sigma_r(S)=\sum_{p+q=r}\sigma_{r;p,q}.
}
\]

This recovers the canonical \(\kappa_c,\kappa_s,\kappa_{int}\) when \(n=3,r=2\), but it also gives a channel decomposition of every elementary curvature invariant in every dimension.

### Exactness parity law

If \(g,H\in\mathbb Q\), then every coefficient \([t^pu^q]\mathcal E_r(t,u)\in\mathbb Q\). The normalization is

\[
q^{(r+2)/2}.
\]

Therefore:

- if \(r\) is even, \(\sigma_{r;p,q}\in\mathbb Q\);
- if \(r\) is odd, \(\sigma_{r;p,q}\in \mathbb Q/\sqrt q\), unless \(q\) is a rational square.

So the universally exact object is the **curvature density**

\[
\boxed{
\widehat\sigma_{r;p,q}:=[t^pu^q]\mathcal E_r(t,u)\in\mathbb Q.
}
\]

For Cella, this matters: in odd curvature order, exact-\(\mathbb Q\) closure belongs to the density unless the account is extended to \(\mathbb Q(\sqrt q)\) or the point has square gradient norm.

---

## 2. Explicit \(r=1\): channelized mean curvature / trace curvature

The first curvature invariant is

\[
\sigma_1(S)=\operatorname{tr}S.
\]

The universal formula gives

\[
\boxed{
\tau_c
=
\frac{2\sum_{i<j}g_i g_j H_{ij}}{q^{3/2}}
=
\frac{g^TH_cg}{q^{3/2}}
}
\]

and

\[
\boxed{
\tau_s
=
\frac{g^TH_sg-q\operatorname{tr}(H_s)}{q^{3/2}}
=
-\frac{\sum_i(q-g_i^2)H_{ii}}{q^{3/2}}.
}
\]

Thus

\[
\boxed{
\operatorname{tr}S=\tau_c+\tau_s.
}
\]

The averaged mean curvature is

\[
\boxed{
H_{mean}=\frac{\tau_c+\tau_s}{n-1}.
}
\]

The exact rational densities are

\[
\widehat\tau_c=2\sum_{i<j}g_i g_j H_{ij},
\qquad
\widehat\tau_s=g^TH_sg-q\operatorname{tr}(H_s).
\]

So the three-channel framework does not begin at Gaussian curvature. It starts already at mean curvature, but mean curvature lives in the odd-parity \(\mathbb Q/\sqrt q\) class unless density-scaled.

---

## 3. Explicit \(r=2\): the 3D formula becomes a local triple kernel for all \(n\)

For every coordinate triple \(I=\{i,j,k\}\), use the canonical 3D determinant partition on the restricted gradient and Hessian:

\[
\Delta_c^{ijk},\qquad \Delta_s^{ijk},\qquad \Delta_m^{ijk}.
\]

Then for arbitrary ambient dimension \(n\), the second elementary curvature decomposes as

\[
\boxed{
\sigma_{2,c}=-\frac{\sum_{i<j<k}\Delta_c^{ijk}}{q^2},
\qquad
\sigma_{2,s}=-\frac{\sum_{i<j<k}\Delta_s^{ijk}}{q^2},
\qquad
\sigma_{2,int}=-\frac{\sum_{i<j<k}\Delta_m^{ijk}}{q^2}.
}
\]

Thus the existing \(n=3\) \(K_G\) channel formula is not merely a surface formula. It is the atomic triple formula for the second elementary curvature in any ambient dimension.

This gives an immediate extension path:

- for \(n=3\), \(\sigma_2=K_G\);
- for \(n=4\), \(\sigma_2\) is the pairwise principal-curvature sum \(k_1k_2+k_1k_3+k_2k_3\);
- for general \(n\), \(\sigma_2\) is the scalar-curvature-like elementary invariant of the hypersurface.

All \(r=2\) channels remain exact in \(\mathbb Q\) for rational \(g,H\).

---

## 4. Gaussian-Kronecker curvature in arbitrary dimension

Set \(r=m=n-1\). The Gaussian-Kronecker curvature is

\[
K_{GK}=\sigma_{n-1}(S).
\]

The channel-generating polynomial is

\[
\boxed{
\mathcal K(t,u)
=
(-1)^n
\det
\begin{pmatrix}
0 & g^T\\
g & tH_c+uH_s
\end{pmatrix}.
}
\]

Then

\[
\boxed{
K_{GK;p,q}
=\frac{[t^pu^q]\mathcal K(t,u)}{q^{(n+1)/2}},
\qquad p+q=n-1.
}
\]

For \(n=3\), this gives

\[
K_{GK;2,0}=\kappa_c,
\qquad
K_{GK;1,1}=\kappa_{int},
\qquad
K_{GK;0,2}=\kappa_s.
\]

For \(n=4\), this gives four pieces:

\[
K_{GK}=K_{3,0}+K_{2,1}+K_{1,2}+K_{0,3}.
\]

Because \(n=4\) has \(q^{5/2}\) in the denominator, the exact-\(\mathbb Q\) object is the density

\[
\widehat K_{p,q}=[t^pu^q]\mathcal K(t,u).
\]

---

## 5. Curvature fingerprint polynomial: all elementary channels at once

Define the two-channel characteristic polynomial

\[
\boxed{
\chi(z;t,u)=\det(I+z(tS_c+uS_s)).
}
\]

Then

\[
\boxed{
\chi(z;t,u)
=
\sum_{r=0}^{n-1}z^r\sum_{p+q=r}t^pu^q\sigma_{r;p,q}.
}
\]

This is the full channel spectrum.

For surfaces in \(\mathbb R^3\):

\[
\chi(z;t,u)
=1+z(t\tau_c+u\tau_s)
+z^2(t^2\kappa_c+tu\kappa_{int}+u^2\kappa_s).
\]

For hypersurfaces in \(\mathbb R^4\):

\[
\begin{aligned}
\chi(z;t,u)=1
&+z(t\sigma_{1;c}+u\sigma_{1;s})\\
&+z^2(t^2\sigma_{2;2,0}+tu\sigma_{2;1,1}+u^2\sigma_{2;0,2})\\
&+z^3(t^3K_{3,0}+t^2uK_{2,1}+tu^2K_{1,2}+u^3K_{0,3}).
\end{aligned}
\]

This is the strongest compact object: every curvature order, every channel order, one generating function.

---

## 6. Powers of the split shape operator

Let

\[
A=S_c,
\qquad B=S_s.
\]

The power traces

\[
P_k(t,u)=\operatorname{tr}(tA+uB)^k
\]

carry the noncommutative channel information. Because trace is cyclic, words collapse into cyclic classes.

The first four are:

\[
\boxed{
P_1=t\operatorname{tr}A+u\operatorname{tr}B.
}
\]

\[
\boxed{
P_2=t^2\operatorname{tr}A^2+2tu\operatorname{tr}(AB)+u^2\operatorname{tr}B^2.
}
\]

\[
\boxed{
P_3=t^3\operatorname{tr}A^3
+3t^2u\operatorname{tr}(A^2B)
+3tu^2\operatorname{tr}(AB^2)
+u^3\operatorname{tr}B^3.
}
\]

\[
\boxed{
\begin{aligned}
P_4={}&t^4\operatorname{tr}A^4
+4t^3u\operatorname{tr}(A^3B)
+4tu^3\operatorname{tr}(AB^3)
+u^4\operatorname{tr}B^4\\
&+4t^2u^2\operatorname{tr}(A^2B^2)
+2t^2u^2\operatorname{tr}(ABAB).
\end{aligned}
}
\]

Newton identities convert the power spectrum into elementary curvature channels.

For example, in tangent dimension 3, i.e. ambient \(n=4\), write

\[
a_1=\operatorname{tr}A,
\quad b_1=\operatorname{tr}B,
\quad a_2=\operatorname{tr}A^2,
\quad b_2=\operatorname{tr}B^2,
\quad c=\operatorname{tr}(AB),
\]

\[
a_3=\operatorname{tr}A^3,
\quad b_3=\operatorname{tr}B^3,
\quad d=\operatorname{tr}(A^2B),
\quad e=\operatorname{tr}(AB^2).
\]

Then the Gaussian-Kronecker channel pieces are

\[
\boxed{
K_{3,0}=\frac{a_1^3-3a_1a_2+2a_3}{6}
}
\]

\[
\boxed{
K_{2,1}=\frac{a_1^2b_1-2a_1c-b_1a_2+2d}{2}
}
\]

\[
\boxed{
K_{1,2}=\frac{a_1b_1^2-a_1b_2-2b_1c+2e}{2}
}
\]

\[
\boxed{
K_{0,3}=\frac{b_1^3-3b_1b_2+2b_3}{6}.
}
\]

This separates the two interaction orders in \(n=4\): two coupling directions against one self direction, and one coupling direction against two self directions.

---

## 7. Ambient trace formula for power words

For any channel word \(X_1\cdots X_k\), where each \(X_i\in\{c,s\}\), set \(H_{X_i}=H_c\) or \(H_s\). Let

\[
P=I-\frac{gg^T}{q}.
\]

Then

\[
\boxed{
\operatorname{tr}(S_{X_1}\cdots S_{X_k})
=
(-1)^k q^{-k/2}
\operatorname{tr}(PH_{X_1}PH_{X_2}\cdots PH_{X_k}P).
}
\]

This avoids choosing a tangent basis. For even \(k\), the trace is rational for rational \(g,H\). For odd \(k\), it lives in \(\mathbb Q/\sqrt q\) unless density-scaled.

---

## 8. 3D channel phase-space normal form

For a surface in \(\mathbb R^3\), assume first that \(g_1g_2g_3\ne 0\). Define the coupling vector

\[
\boxed{
u=
(g_1H_{23},\;g_2H_{13},\;g_3H_{12})
}
\]

and the self vector

\[
\boxed{
w=
\left(
\frac{g_2g_3}{g_1}H_{11},
\frac{g_1g_3}{g_2}H_{22},
\frac{g_1g_2}{g_3}H_{33}
\right).
}
\]

Then the determinant channels become

\[
\boxed{
\Delta_c=2\|\nu\|^2-(\mathbf 1\cdot \nu)^2.
}
\]

\[
\boxed{
\Delta_s=\frac12\|w\|^2-\frac12(\mathbf 1\cdot w)^2
=-(w_1w_2+w_1w_3+w_2w_3).
}
\]

\[
\boxed{
\Delta_m=2\nu\cdot w.
}
\]

The pure coupling metric is

\[
2I-J,
\]

where \(J\) is the all-ones matrix. Its eigenvalues are \(2,2,-1\), so the pure coupling channel is Lorentzian:

- \(\Delta_c>0\): spacelike coupling, \(\kappa_c<0\);
- \(\Delta_c=0\): lightlike coupling, \(\kappa_c=0\) despite possible nonzero coupling Hessian;
- \(\Delta_c<0\): timelike coupling, \(\kappa_c>0\).

This explains several retrodiction cases immediately:

- open chain: nonzero coupling but lightlike \(\nu\), hence \(\kappa_c=0\);
- closed triangle: timelike \(\nu\), hence positive \(\kappa_c\);
- saddle: spacelike \(\nu\), hence negative \(\kappa_c\).

The total determinant numerator is

\[
\boxed{
\Delta=\Delta_c+
\Delta_s+
\Delta_m
=2\|\nu\|^2-(\mathbf 1\cdot\nu)^2
+\frac12\|w\|^2-rac12(\mathbf 1\cdot w)^2
+2\nu\cdot w.
}
\]

Equivalently,

\[
\boxed{
\Delta
=\frac12\|2\nu+w\|^2
-(\mathbf 1\cdot\nu)^2
-rac12(\mathbf 1\cdot w)^2.
}
\]

The curvature channels are then \(-\Delta_*/q^2\).

### Keystone in phase-space form

For

\[
F=x_1^2+x_1x_2+x_3^2-3
\quad\text{at}\quad (1,1,1),
\]

we have

\[
g=(3,1,2),\qquad q=14,
\]

\[
\nu=(0,0,2),
\qquad
w=(4/3,0,3).
\]

Thus

\[
\Delta_c=4,
\qquad
\Delta_s=-4,
\qquad
\Delta_m=12.
\]

Therefore

\[
\boxed{
\kappa_c=-1/49,
\qquad
\kappa_s=+1/49,
\qquad
\kappa_{int}=-3/49,
\qquad
K_G=-3/49.
}
\]

The keystone is not merely a signed-curvature example. It is an exact cancellation of the Lorentzian coupling and self quadratic forms, leaving only the bilinear interaction pairing.

---

## 9. Gauge law: representation curvature versus surface curvature

The total shape operator is invariant under changing the defining function by a nonzero factor. Let

\[
\widetilde F=\mu F.
\]

On the surface \(F=0\), after normalizing locally to \(\mu=1\),

\[
\widetilde g=g,
\qquad
\widetilde H=H+G,
\qquad
G=ga^T+ag^T,
\quad a=\nabla\log\mu.
\]

Because \(Pg=0\),

\[
PGP=0.
\]

So the **total** curvature is unchanged.

But the channel split is taken before projection, so \(G_c\) and \(G_s\) need not vanish separately. For a pure gauge Hessian \(H=G\) in \(\mathbb R^3\), the determinant pieces are

\[
\boxed{
\Delta_c=
\Delta_s
=-4g_1g_2g_3(a_1a_2g_3+a_1a_3g_2+a_2a_3g_1),
}
\]

\[
\boxed{
\Delta_m=
+8g_1g_2g_3(a_1a_2g_3+a_1a_3g_2+a_2a_3g_1).
}
\]

Thus

\[
\Delta_c+
\Delta_s+
\Delta_m=0,
\]

but the channel vector moves along

\[
\boxed{
(\kappa_c,\kappa_s,\kappa_{int})=\lambda(1,1,-2).
}
\]

This is the **gauge-null channel direction**.

Consequences:

1. The total \(K_G\) is an intrinsic surface invariant.
2. The three-channel vector is a defining-function-relative diagnostic unless a canonical gauge is fixed.
3. If the physical variables/sensor channels privilege a defining expression, this is acceptable and useful.
4. If one wants gauge-invariant channel diagnostics, the split must be performed after passing to the projected second fundamental form \(B=PHP\), not directly on \(H\). That gives a different object and should not be mixed with the canonical keystone channels without an explicit mode label.

This is not a defect; it is an account law. The channels can carry representation residue exactly, while their sum carries geometric curvature.

---

## 10. Sensitivity / channel gradients in 3D phase coordinates

Using \(\nu,w\) from §8:

\[
\Delta_c=2\|\nu\|^2-(\mathbf1\cdot\nu)^2,
\qquad
\Delta_s=\frac12\|w\|^2-\frac12(\mathbf1\cdot w)^2,
\qquad
\Delta_m=2\nu\cdot w.
\]

Therefore

\[
\boxed{
\nabla_\nu\Delta_c=4\nu-2(\mathbf1\cdot\nu)\mathbf1,
\qquad
\nabla_w\Delta_s=w-(\mathbf1\cdot w)\mathbf1.
}
\]

\[
\boxed{
\nabla_\nu\Delta_m=2w,
\qquad
\nabla_w\Delta_m=2\nu.
}
\]

These are exact rational sensitivity formulas on any coordinate patch where the \(\nu,w\) chart is valid. They can drive exact optimization, perturbation analysis, or channel-stability tests.

---

## 11. Power-family formulas: monomial hypersurfaces in \(\mathbb R^3\)

Consider

\[
F=x^a y^b z^c-1
\]

at a regular point on the surface, with positive integer exponents and nonzero coordinates. On \(F=0\), define

\[
q=\left(\frac{a}{x}\right)^2+
\left(\frac{b}{y}\right)^2+
\left(\frac{c}{z}\right)^2.
\]

Then the complete three-channel curvature is

\[
\boxed{
\kappa_c
=
\frac{3a^2b^2c^2}{x^2y^2z^2q^2}.
}
\]

\[
\boxed{
\kappa_s
=
\frac{abc(3abc-2ab-2ac-2bc+a+b+c)}{x^2y^2z^2q^2}.
}
\]

\[
\boxed{
\kappa_{int}
=
-\frac{2abc(3abc-ab-ac-bc)}{x^2y^2z^2q^2}.
}
\]

and the total is

\[
\boxed{
K_G
=
\frac{abc(a+b+c)}{x^2y^2z^2q^2}.
}
\]

At \((1,1,1)\), this reduces to

\[
q=a^2+b^2+c^2,
\]

\[
\boxed{
K_G=\frac{abc(a+b+c)}{(a^2+b^2+c^2)^2}.
}
\]

The multilinear case \(a=b=c=1\) gives

\[
K_G=1/3,
\qquad
\kappa_c=1/3,
\qquad
\kappa_s=0,
\qquad
\kappa_{int}=0.
\]

The first non-multilinear power case \(a=2,b=1,c=1\) gives, at \((1,1,1)\),

\[
K_G=2/9,
\qquad
\kappa_c=1/3,
\qquad
\kappa_s=0,
\qquad
\kappa_{int}=-1/9.
\]

So increasing a single power creates interaction curvature even when the total remains positive.

---

## 12. Additive Fermat-type surfaces

For

\[
F=A x^a+B y^b+C z^c-D,
\]

there is no coupling Hessian, so

\[
\boxed{
\kappa_c=0,
\qquad
\kappa_{int}=0,
\qquad
K_G=\kappa_s.
}
\]

With

\[
g_x=Aa x^{a-1},\quad
H_{xx}=Aa(a-1)x^{a-2},
\]

and analogously for \(y,z\),

\[
\boxed{
K_G
=
\frac{
 g_x^2H_{yy}H_{zz}
+g_y^2H_{xx}H_{zz}
+g_z^2H_{xx}H_{yy}
}{(g_x^2+g_y^2+g_z^2)^2}.
}
\]

This includes spheres, ellipsoids in implicit diagonal form, paraboloids, and rational superquadrics whenever the evaluated powers stay in the exact account class.

---

## 13. Quadratic mixed surfaces

For the general quadratic surface

\[
F=ax^2+by^2+cz^2+2fxy+2exz+2dyz-C,
\]

write

\[
H_{11}=2a,
\quad H_{22}=2b,
\quad H_{33}=2c,
\quad H_{12}=2f,
\quad H_{13}=2e,
\quad H_{23}=2d.
\]

Then, wherever \(g_1g_2g_3\ne0\), the phase-space vectors are

\[
\nu=(2dg_1,2eg_2,2fg_3),
\]

\[
w=\left(
\frac{2ag_2g_3}{g_1},
\frac{2bg_1g_3}{g_2},
\frac{2cg_1g_2}{g_3}
\right).
\]

All channels follow from

\[
\Delta_c=2\|\nu\|^2-(\mathbf1\cdot\nu)^2,
\qquad
\Delta_s=\frac12\|w\|^2-rac12(\mathbf1\cdot w)^2,
\qquad
\Delta_m=2\nu\cdot w.
\]

This is a compact exact classifier for every rational quadratic implicit surface in three variables.

---

## 14. Channel ratios and interaction dominance

When \(K_G\ne0\), define the normalized channel barycentric coordinates

\[
\boxed{
R_c=\frac{\kappa_c}{K_G},
\qquad
R_s=\frac{\kappa_s}{K_G},
\qquad
R_{int}=\frac{\kappa_{int}}{K_G}.
}
\]

They satisfy

\[
\boxed{
R_c+R_s+R_{int}=1.
}
\]

For the keystone,

\[
(R_c,R_s,R_{int})=\left(\frac13,-\frac13,1\right).
\]

That is the cleanest diagnostic statement of the regime: the interaction channel contributes 100% of the final curvature after pure coupling and pure self cancel each other exactly.

---

## 15. Practical strongest next mathematical target

The canonical 3-channel \(K_G\) is now only the first surface-level member of a larger algebra:

\[
\boxed{
\text{Channel geometry} =
\left\{\sigma_{r;p,q}:1\le r\le n-1,\;p+q=r\right\}.
}
\]

The implementation target should therefore not be a hard-coded three-number return alone. The stronger target is a channel spectrum carrier:

\[
\boxed{
\mathsf{ChannelSpectrum}(r,p,q,\widehat\sigma_{r;p,q},q,parity,normalization,provenance).
}
\]

For \(n=3\), this specializes to:

- trace/mean channels: \(\tau_c,\tau_s\);
- Gaussian channels: \(\kappa_c,\kappa_s,\kappa_{int}\);
- power traces: \(P_k(t,u)\), reducible by Cayley-Hamilton after \(k=2\).

For \(n>3\), it gives:

- all elementary curvature orders;
- separated interaction orders \((p,q)\);
- exact rational densities even when normalized curvature leaves \(\mathbb Q\).

This is the expanded mathematical object with real reach.
