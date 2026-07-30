# Gauge-Channel Transport Law for the Three-Channel K_G Keystone

**Purpose:** Derive the exact chart-change / gauge action on the three-channel curvature decomposition

\[
K_G=\kappa_c+\kappa_s+\kappa_{int}
\]

for the keystone surface

\[
F=x_1^2+x_1x_2+x_3^2-3
\]

at \((1,1,1)\), and isolate the structural reason why the single-axis gauges \(e_1\) and \(e_2\) preserve \(\kappa_c\) while generic gauge directions do not.

---

## 1. Gauge action

For a gauge-renormalized defining function

\[
\widetilde F=\mu F,
\]

with \(\mu=1\) on the point, write

\[
a=\nabla\log \mu=(u,v,w).
\]

On the surface point,

\[
\widetilde g=g,
\]

and

\[
\boxed{
\widetilde H=H+ga^T+ag^T.
}
\]

For the keystone,

\[
g=(3,1,2),
\]

\[
H=\begin{pmatrix}
2&1&0\\
1&0&0\\
0&0&2
\end{pmatrix},
\]

so

\[
\widetilde H=
\begin{pmatrix}
2+6u&1+u+3v&2u+3w\\
1+u+3v&2v&2v+w\\
2u+3w&2v+w&2+4w
\end{pmatrix}.
\]

The denominator is fixed:

\[
|g|^4=(3^2+1^2+2^2)^2=14^2=196.
\]

---

## 2. Exact channel transport law

Substituting \(\widetilde H\) into the three-channel determinant partition gives:

\[
\boxed{
\kappa_c(u,v,w)=
{12uv+6uw+18vw+6w-1\over 49}.
}
\]

\[
\boxed{
\kappa_s(u,v,w)=
{12uv+6uw+3u+18vw+13v+2w+1\over 49}.
}
\]

\[
\boxed{
\kappa_{int}(u,v,w)=
-{24uv+12uw+3u+36vw+13v+8w+3\over 49}.
}
\]

Therefore

\[
\boxed{
\kappa_c(u,v,w)+\kappa_s(u,v,w)+\kappa_{int}(u,v,w)=-{3\over49}
}
\]

for every rational gauge vector \((u,v,w)\). The channel triple moves inside the affine plane

\[
\boxed{
\Delta\kappa_c+\Delta\kappa_s+\Delta\kappa_{int}=0.
}
\]

Relative to the base triple

\[
\left(-{1\over49},{1\over49},-{3\over49}\right),
\]

the gauge shifts are

\[
\boxed{
\Delta\kappa_c={6(2uv+uw+3vw+w)\over49},
}
\]

\[
\boxed{
\Delta\kappa_s={12uv+6uw+3u+18vw+13v+2w\over49},
}
\]

\[
\boxed{
\Delta\kappa_{int}=-{24uv+12uw+3u+36vw+13v+8w\over49}.
}
\]

---

## 3. Exact retrodiction of the four observed gauges

| gauge \(a=(u,v,w)\) | \(K_G\) | \((\kappa_c,\kappa_s,\kappa_{int})\) |
|---|---:|---:|
| \((1,0,0)\) | \(-3/49\) | \((-1/49,4/49,-6/49)\) |
| \((0,1,0)\) | \(-3/49\) | \((-1/49,2/7,-16/49)\) |
| \((1,-2,3)\) | \(-3/49\) | \((-97/49,-130/49,32/7)\) |
| \((-1/2,5,1)\) | \(-3/49\) | \((62/49,247/98,-377/98)\) |

All four are direct evaluations of the transport law above.

---

## 4. The \(\kappa_c\)-pinning surface

The pure coupling channel is preserved exactly when

\[
\Delta\kappa_c=0.
\]

For the keystone this is

\[
\boxed{
2uv+uw+3vw+w=0.
}
\]

Equivalently,

\[
\boxed{
w(u+3v+1)+2uv=0.
}
\]

When \(u+3v+1\neq0\), this gives the rational sheet

\[
\boxed{
w=-{2uv\over u+3v+1}.
}
\]

Thus \((1,0,0)\) and \((0,1,0)\) are not isolated coincidences. They lie on a full \(\kappa_c\)-preserving gauge sheet. In fact every pure \(e_1\)-axis gauge \((u,0,0)\) and every pure \(e_2\)-axis gauge \((0,v,0)\) preserves \(\kappa_c\) for all rational \(u,v\).

The pure \(e_3\)-axis does not:

\[
\Delta\kappa_c(0,0,w)={6w\over49}.
\]

So the asymmetry is structural.

---

## 5. Coupling-channel edge-vector lemma

For any three-variable surface, define the coupling edge vector

\[
\nu=(\nu_1,\nu_2,\nu_3)
=(g_1H_{23},\;g_2H_{13},\;g_3H_{12}).
\]

Then

\[
\boxed{
\Delta_c=2\|\nu\|^2-(\mathbf 1\cdot\nu)^2
=
u^T(2I-J)\nu,
}
\]

where \(J=\mathbf1\mathbf1^T\). The metric \(2I-J\) has signature \((2,1)\). The pure coupling channel is therefore a Lorentzian quadratic form in the weighted coupling-edge vector.

Under gauge \(a=(a_1,a_2,a_3)\), the off-diagonal Hessian entries shift by

\[
H'_{ij}=H_{ij}+g_i a_j+a_i g_j.
\]

Therefore the edge vector shifts by

\[
\boxed{
\delta\nu_1=g_1(g_2a_3+g_3a_2),
}
\]

\[
\boxed{
\delta\nu_2=g_2(g_1a_3+g_3a_1),
}
\]

\[
\boxed{
\delta\nu_3=g_3(g_1a_2+g_2a_1).
}
\]

The coupling-channel shift is

\[
\boxed{
\delta\Delta_c
=2\nu^T(2I-J)\delta\nu+\delta\nu^T(2I-J)\delta\nu.
}
\]

Since

\[
\kappa_c=-{\Delta_c\over |g|^4},
\]

this gives the exact gauge law for \(\kappa_c\).

---

## 6. Why \(e_1\) and \(e_2\) preserve \(\kappa_c\) on the keystone

For the keystone,

\[
H_{12}=1,
\qquad
H_{13}=H_{23}=0,
\]

so the base coupling vector is

\[
\nu=(0,0,2).
\]

A pure \(e_1\)-gauge gives

\[
\delta\nu=(0,2u,2u).
\]

A pure \(e_2\)-gauge gives

\[
\delta\nu=(6v,0,6v).
\]

Both are null directions for the Lorentzian coupling metric and are tangent to the \(\Delta_c\)-level surface through \(\nu=(0,0,2)\). Hence they preserve \(\Delta_c\), and therefore preserve \(\kappa_c\), exactly.

A pure \(e_3\)-gauge gives

\[
\delta\nu=(3w,3w,0),
\]

which is not tangent to the same level surface. It changes

\[
\Delta\kappa_c={6w\over49}.
\]

This proves that the observed pinning of \(\kappa_c\) under \(e_1,e_2\) is not accidental. It is the edge-incidence structure of the keystone coupling: the original mixed Hessian lives on edge \((1,2)\), and gauges at the endpoints of that edge move \(\nu\) along null tangent directions, while a gauge at the opposite vertex does not.

---

## 7. General single-edge lemma

Suppose a surface has, at the point, exactly one nonzero coupling edge

\[
H_{ij}=h,
\]

with \(H_{ik}=H_{jk}=0\), and let \(k\) be the remaining index. Then the base coupling vector has only one nonzero component:

\[
\nu_k=g_kh.
\]

A pure gauge along either endpoint \(e_i or \(e_j\) adds a null vector tangent to the \(\Delta_c\)-level set. Hence

\[
\boxed{
\delta\kappa_c(t e_i)=0,
\qquad
\delta\kappa_c(t e_j)=0
}
\]

for all rational \(t\).

A pure gauge along the opposite vertex \(e_k\) generally changes \(\kappa_c\) linearly:

\[
\boxed{
\delta\Delta_c=-4t\,g_i g_j g_k h,
}
\]

and therefore

\[
\boxed{
\delta\kappa_c={4t\,g_i g_j g_k h\over |g|^4}.
}
\]

For the keystone, \((i,j,k)=(1,2,3)\), \(g=(3,1,2)\), \(h=1\), and \(|g|^4=196\), so

\[
\delta\kappa_c={4t\cdot3\cdot1\cdot2\over196}={6t\over49},
\]

matching the exact keystone law.

---

## 8. Interpretation

The gauge action proves that the channel triple is a representation-relative diagnostic, not an intrinsic scalar. The total curvature stays fixed:

\[
K_G=-{3\over49}.
\]

The channel triple moves inside the plane

\[
\kappa_c+\kappa_s+\kappa_{int}=-{3\over49}.
\]

The pure coupling channel is governed by a Lorentzian edge-vector norm. This explains why some gauges preserve \(\kappa_c\), some move it, and generic gauges move all three channels.

The clean statement is:

\[
\boxed{
\text{gauge changes do not alter }K_G,\text{ but act nontrivially on the channel allocation.}
}
\]

For the keystone specifically:

\[
\boxed{
\text{endpoint gauges of the active coupling edge preserve }\kappa_c;
\text{ opposite-vertex gauges move it.}
}
\]

