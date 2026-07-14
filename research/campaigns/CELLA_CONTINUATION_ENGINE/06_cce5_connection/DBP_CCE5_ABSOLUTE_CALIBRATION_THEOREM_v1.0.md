# DBP CCE-5 absolute calibration theorem v1.0

## 1. Marking

Write the Legendre fibre in relative coordinate (u=x/m). Its ordered branch
sections are

\[
0,\quad 1,\quad q=1/m,\quad \infty,
\]

and the selected third-kind pole is (p=1/n). At both real endpoint fibres
choose the standard symplectic marking as follows.

- (A) is the double of the selected lift of the interval from (0) to (1).
- (B) is the vanishing cycle obtained by doubling an arc from (1) to (q),
  oriented so that its holomorphic period is (+2iK(1-m)).
- (mu) is the positive meridian about the selected pole.
- (delta) is the selected lift from (0) to (1), with the stated lateral
  indentation when (p\in(0,1)).

Orient (A\cdot B=+1). The boundary map has coordinates

\[
\partial(A,B,\mu,\delta)=(0,0,0,\beta).
\]

## 2. Exact braid carried by the released corridors

On the lifted shear cover

\[
m=\frac{\rho-1}{2\rho},\qquad
q=\frac1m=\frac{2\rho}{\rho-1},\qquad
p=\frac1n=\frac{2m-1}{m^2}.
\]

The upper CCE-2 polygon lifts from $\rho=+\sqrt2$ to
$\rho=-\sqrt2$. On its central horizontal segment it crosses the negative
$\rho$-sheet over the positive imaginary $\sigma$-axis. There $q$ crosses
the open interval $(0,1)$ once from the lower to the upper half-plane. The
lower corridor is complex conjugate: $q$ crosses once from upper to lower.
No other branch section crosses the selected contour; the CCE-2 marked-section
separations and CCE-6 refined representative theorem exclude a collision.

This crossing statement is exact. Since $q=2\rho/(\rho-1)$, $q$ is real
exactly when $\rho$ is real. On the interiors of the seven rational polygon
segments, $1+\sigma^2$ can be positive real only at the midpoint of the
central segment; the other imaginary-axis midpoint has
$|\operatorname{Im}\sigma|=3/2$ and hence $1+\sigma^2<0$. At the central
midpoint

\[
\sigma=\frac i2,\qquad \rho=-\frac{\sqrt3}{2},\qquad
q=4\sqrt3-6.
\]

The inequalities $0<q<1$ follow without approximation from
$6<4\sqrt3<7$, equivalently $36<48<49$. Parameterizing the upper central
segment by increasing real part gives

\[
\frac{d\rho}{ds}=\frac{\sigma}{\rho}=-\frac{i}{\sqrt3},
\qquad
\frac{dq}{ds}=\frac{-2}{(\rho-1)^2}\frac{d\rho}{ds}
\in i\mathbb R_{>0},
\]

so the crossing direction is lower-to-upper. Complex conjugation proves the
opposite direction for the lower corridor. Thus the signed crossing number is
$+1$ above and $-1$ below, with no sampling argument.

A full ordered braid of $q$ about the fixed branch section $1$ lifts to the
square of the Dehn twist about $B$. Hence the compact transport is

\[
G_\uparrow(A)=A+2B,\qquad G_\uparrow(B)=B,
\]

\[
G_\downarrow(A)=A-2B,\qquad G_\downarrow(B)=B.
\]

Both matrices preserve $A\cdot B=+1$, have determinant one, and are mutual
inverses after identifying the endpoint markings.

The relative contour is one half of the branch-cut double. Its contour
deformation therefore receives one, not two, copies of the oriented vanishing
cycle. Combining this with the already proved pole-side selection gives

\[
\boxed{
G_\uparrow(\delta_+)=\delta_-^\uparrow+B_-,\qquad
G_\downarrow(\delta_+)=\delta_-^\downarrow-B_-.
}
\]

Therefore

\[
\boxed{\lambda_\uparrow=B_-,\qquad\lambda_\downarrow=-B_-.}
\]

In the route-specific ordered endpoint bases
((A_-,B_-,\mu_-,\delta_-^\uparrow)) and
((A_-,B_-,\mu_-,\delta_-^\downarrow)), the column-action matrices are

\[
M_\uparrow=
\begin{pmatrix}
1&0&0&0\\
2&1&0&1\\
0&0&1&0\\
0&0&0&1
\end{pmatrix},\qquad
M_\downarrow=
\begin{pmatrix}
1&0&0&0\\
-2&1&0&-1\\
0&0&1&0\\
0&0&0&1
\end{pmatrix}.
\]

They preserve the boundary vector and restrict to symplectic compact
matrices. Since
(\delta_-^\uparrow-\delta_-^\downarrow=-\mu_-), they refine the former
quotient statement to

\[
G_\uparrow(\delta_+)-G_\downarrow(\delta_+)=2B_- -\mu_-.
\]

The compact corrections cancel in the rational half-sum:

\[
\boxed{
\frac{G_\uparrow(\delta_+)+G_\downarrow(\delta_+)}2
=\delta_-^{\rm CPV}.
}
\]

## 3. Analytic compatibility

For the ordered DBP period vector

\[
Y=(K(m),E(m),\Pi(m^2/(2m-1);m))^T,
\]

differentiation under the marked contour and elementary integration-by-parts
reduction give the CCE-5 rational connection (Y'=M(m)Y). Contour deformation
along the upper/lower braid adds the period of (\pm B); doubling the open
contour gives the compact law (A\mapsto A\pm2B). Thus the analytic connection
and the integral matrices above are two realizations of the same marked-chain
transport, not a numerical near-integrality inference.

As a scalar check, the holomorphic component obeys the exact continuation law

\[
K(m_+)\longmapsto K(m_-)
\mathbin{\pm}2iK(1-m_-),
\]

which is precisely the period realization of (A\mapsto A\pm2B) under the
chosen orientation.

## 4. Fixed-curve trace-path comparison

On (E_{128}^{\circ}), define (A_E) independently as the selected lift of
the oriented real projective circle: it follows (\Gamma_-^\uparrow) from
(Q=(1,0)) to (O), then returns along (-\Gamma_+), with the upper detour at
the selected pole. This is an embedded nonseparating circle and hence a
primitive class. Choose (B_E) as an explicit symplectic completion, oriented
by (A_E\cdot B_E=+1), and retain the positive pole meridian (mu_E).

Then, by the geometric definitions and
(\Gamma_-^\uparrow-\Gamma_-^\downarrow=-\mu_E),

\[
[\Gamma_-^\uparrow]=[\Gamma_+]+[A_E],
\]

\[
[\Gamma_-^\downarrow]=[\Gamma_+]+[A_E]+[\mu_E].
\]

Thus the exact relative comparison integers in this frozen marking are

\[
\boxed{(a,b,c)=(1,0,0).}
\]

The coordinate statement is marking-dependent; the geometric equalities and
the difference by one positive meridian are invariant.
