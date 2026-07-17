# DBP Galois-Dual Surface-Cycle Route

## Stage 2: lift of the dual boundary chain to the complexified surface, v0.1

**Date:** 2026-07-14  
**Depends on:** `DBP_SURFACE_TO_LINK_CLOSEOFF_v1.0.md`,
`DBP_DUAL_SURFACE_CYCLE_STAGE1_v0.1.md`  
**Status:** the lateral and CPV boundary chains now have explicit
relative/Borel--Moore surface lifts  
**Coefficient convention:** the literal continued curvature cycle gives
\(-i\) times the real-normalized dual period; multiplication of the cycle by
\(i\), equivalently multiplication of the continued curvature form by \(i\),
gives \(I_{\rm dual}\)

---

## 0. Result

Stage 1 constructed the metric elliptic boundary curve

\[
\mathcal B_-:\qquad
W^2=c\,v(1-v)(1-cv)(1-c^2v),
\qquad c=3+2\sqrt2,
\tag{0.1}
\]

the differential

\[
\Omega_-=-4c(1-cv)\frac{dv}{W},
\tag{0.2}
\]

and two lateral chains \(\delta_-^\uparrow,\delta_-^\downarrow\) satisfying

\[
\int_{\delta_-^\uparrow}i\Omega_-
=I_{\rm dual,CPV}-4\pi i,
\qquad
\int_{\delta_-^\downarrow}i\Omega_-
=I_{\rm dual,CPV}+4\pi i.
\tag{0.3}
\]

This report constructs complex surface chains

\[
\mathfrak C_-^\uparrow,
\mathfrak C_-^\downarrow
\tag{0.4}
\]

on the complexified norm double cover of the original keystone quadric such
that

\[
\boxed{
\int_{\mathfrak C_-^\uparrow}\mathcal K
=\int_{\delta_-^\uparrow}\Omega_-,
\qquad
\int_{\mathfrak C_-^\downarrow}\mathcal K
=\int_{\delta_-^\downarrow}\Omega_-.
}
\tag{0.5}
\]

Here \(\mathcal K\) is the algebraic continuation of the Gaussian-curvature
two-form. The real-normalized dual cycles are the complex-coefficient classes

\[
\boxed{
\Sigma_-^\uparrow=i\mathfrak C_-^\uparrow,
\qquad
\Sigma_-^\downarrow=i\mathfrak C_-^\downarrow.
}
\tag{0.6}
\]

They obey

\[
\boxed{
\int_{\Sigma_-^\uparrow}\mathcal K
=I_{\rm dual,CPV}-4\pi i,
\qquad
\int_{\Sigma_-^\downarrow}\mathcal K
=I_{\rm dual,CPV}+4\pi i.
}
\tag{0.7}
\]

Therefore

\[
\boxed{
\Sigma_-^{\rm CPV}
=\frac12\left(\Sigma_-^\uparrow+\Sigma_-^\downarrow\right)
=\frac i2\left(\mathfrak C_-^\uparrow+
\mathfrak C_-^\downarrow\right)
}
\tag{0.8}
\]

is a complex-coefficient relative/Borel--Moore surface cycle with

\[
\boxed{
\int_{\Sigma_-^{\rm CPV}}\mathcal K=I_{\rm dual,CPV}.
}
\tag{0.9}
\]

Equivalently, the geometric half-sum

\[
\mathfrak C_-^{\rm CPV}
=\frac12\left(\mathfrak C_-^\uparrow+
\mathfrak C_-^\downarrow\right)
\]

satisfies

\[
\int_{\mathfrak C_-^{\rm CPV}}i\mathcal K
=I_{\rm dual,CPV}.
\tag{0.10}
\]

This closes the existence and period-evaluation parts of the complex surface
cycle. It does not claim that the normalized cycle has integral coefficients,
that it is represented by a real surface region, or that Gauss--Manin
transport selects it uniquely without possible additions by compact periods.

---

## 1. The norm double cover and curvature form

For a diagonal member of the shear family write

\[
F_c=ax^2-by^2+z^2-3,
\qquad
a=\frac1{1-c},
\qquad
b=\frac c{1-c}.
\tag{1.1}
\]

Then

\[
a-b=1,
\qquad
c=\frac ba.
\tag{1.2}
\]

The primary keystone has \(c_+=3-2\sqrt2\). Its Galois companion has

\[
c_-=3+2\sqrt2=\frac1{c_+},
\]

\[
a_-=-\frac{\sqrt2-1}{2},
\qquad
b_-=-\frac{\sqrt2+1}{2},
\qquad
a_-b_-=\frac14.
\tag{1.3}
\]

The dual diagonal equation

\[
a_-x^2-b_-y^2+z^2=3
\tag{1.4}
\]

is the original complexified keystone quadric after the
orientation-preserving orthogonal change

\[
(x,y,z)\longmapsto(y,x,-z).
\tag{1.5}
\]

Thus the construction below produces a cycle on the original complexified
DBP surface, not on an unrelated quadric.

Put

\[
q_c=\lVert\nabla F_c\rVert^2
=4(a^2x^2+b^2y^2+z^2)
\tag{1.6}
\]

and form the norm double cover

\[
\widetilde{\mathcal S}_c:\qquad
F_c=0,
\qquad
w^2=q_c.
\tag{1.7}
\]

The algebraic continuation of the curvature two-form is

\[
\boxed{
\mathcal K_c
=-48ab\,
\frac{\iota_{\nabla F_c}(dx\wedge dy\wedge dz)}{w^5}.
}
\tag{1.8}
\]

On the positive real sheet this is \(K_GdA\), since

\[
K_G=-\frac{48ab}{q_c^2},
\qquad
dA=\frac{\iota_{\nabla F_c}(dx\wedge dy\wedge dz)}{\sqrt{q_c}}.
\]

The global primitive from the primary close-off extends meromorphically:

\[
\eta_c
=-\frac{2ab\,y}{w(a^2x^2+z^2)}(x\,dz-z\,dx),
\qquad
d\eta_c=\mathcal K_c.
\tag{1.9}
\]

The surface cycles will avoid the polar divisor of (1.9) by lateral
transport.

---

## 2. Algebraic hyperbolic fiber

Use \(\xi=\sinh u\) and write

\[
\Psi_c(\xi,t)=
\left(
\sqrt{\frac3a}\sqrt{1+\xi^2}\cos t,
\sqrt{\frac3b}\,\xi,
\sqrt3\sqrt{1+\xi^2}\sin t
\right).
\tag{2.1}
\]

This satisfies \(F_c\circ\Psi_c=0\). Define

\[
p(t)=a\cos^2t+\sin^2t.
\tag{2.2}
\]

Then

\[
\frac{q_c\circ\Psi_c}{12}
=p(t)+(p(t)+b)\xi^2.
\tag{2.3}
\]

Introduce the fiber double cover

\[
\mathcal F_t:\qquad
Z^2=p+(p+b)\xi^2,
\qquad
w=\sqrt{12}\,Z.
\tag{2.4}
\]

On this cover,

\[
\boxed{
\Psi_c^*\mathcal K_c
=-\frac{\sqrt{ab}}{Z^3},d\xi\wedge dt,
}
\tag{2.5}
\]

and

\[
\boxed{
\Psi_c^*\eta_c
=-\frac{\sqrt{ab}\,\xi}{pZ}\,dt.
}
\tag{2.6}
\]

Indeed,

\[
d_\xi\left(\frac{\xi}{Z}\right)
=\frac{p}{Z^3}\,d\xi,
\tag{2.7}
\]

so differentiating (2.6) proves (2.5) without a choice of integration
contour.

The compactified fiber has two distinguished points at infinity,

\[
Q_\pm(t):\qquad
\frac Z\xi\longrightarrow\pm\sqrt{p+b}.
\tag{2.8}
\]

Let \(\ell_t\) be the relative fiber class from \(Q_-\) to \(Q_+\), calibrated
by the real primary line \(\xi:-\infty\to+\infty\). Equations (2.6)--(2.8)
give the exact fiber integral

\[
\boxed{
\int_{\ell_t}\Psi_c^*\mathcal K_c
=-\frac{2\sqrt{ab}}{p\sqrt{p+b}}\,dt.
}
\tag{2.9}
\]

The integrand is \(O(|\xi|^{-3})d\xi\), so the fiber integral is absolutely
convergent at both noncompact ends.

---

## 3. The angular lift of the Stage-1 quartic

Let \(v\) be the Stage-1 metric-quartic coordinate. The exact relation between
the surface angle \(t\) and the standard ellipse angle is

\[
\tan^2t=a\frac{1-v}{v}.
\tag{3.1}
\]

Equivalently,

\[
\cos^2t=\frac{(1-c)v}{1-cv},
\qquad
\sin^2t=\frac{1-v}{1-cv}.
\tag{3.2}
\]

Substitution into (2.2) gives the decisive simplification

\[
\boxed{
p=\frac1{1-cv},
\qquad
p+b=\frac{1-c^2v}{(1-c)(1-cv)}.
}
\tag{3.3}
\]

Therefore the only finite angular/fiber discriminants are

\[
v=\frac1{c^2},
\qquad
v=\frac1c.
\tag{3.4}
\]

For the dual value \(c>1\), both lie strictly between zero and one. The dual
boundary contour from Stage 1 has affine description

```text
0 -> -infinity -> P_infinity^- -> +infinity -> 1,
```

so it avoids both finite discriminants. This proves that the relative fiber
class \(\ell_t\) can be transported along either lateral contour without
meeting \(q_c=0\) or the angular pole \(p^{-1}=0\). The sole limiting
degeneration occurs at \(P_\infty^-\), already bypassed laterally.

Differentiating (3.1), fixing the sign on the primary real quadrant, and then
continuing algebraically gives

\[
dt=-\frac{\sqrt{1-c}}
{2(1-cv)\sqrt{v(1-v)}}\,dv.
\tag{3.5}
\]

Using (3.3) and

\[
W^2=c\,v(1-v)(1-cv)(1-c^2v)
\]

now yields

\[
\boxed{
\frac{\sqrt{ab}}{p\sqrt{p+b}}\,dt
=-\frac12c(1-cv)\frac{dv}{W}.
}
\tag{3.6}
\]

This is the missing surface-fiber-to-metric-quartic identity.

---

## 4. Four-quadrant gluing and the swept surface chain

Equation (3.2) defines the angular sign cover over the \(v\)-sphere. More
explicitly, introduce \(C=\cos t\) and \(S=\sin t\) with

\[
C^2=\frac{(1-c)v}{1-cv},
\qquad
S^2=\frac{1-v}{1-cv},
\qquad C^2+S^2=1.
\tag{4.1}
\]

Over an oriented path from \(v=0\) to \(v=1\), take the four sign choices
\((C,S)\), and alternate the direction of the base path. At \(v=0\), the two
branches differing only in the sign of \(C\) meet because \(C=0\); at
\(v=1\), the branches differing only in the sign of \(S\) meet because
\(S=0\). The four lifted intervals therefore concatenate to a closed angular
cycle. Calibrate its orientation at \(0<c<1\) by the ordinary circle
\(t\in\mathbb R/2\pi\mathbb Z\), then continue the gluing algebraically to
\(c=c_-\).

For a lateral Stage-1 path \(\delta\), let

\[
\operatorname{Circ}(\delta)
\tag{4.2}
\]

denote this closed four-quadrant angular lift. Over every point of
\(\operatorname{Circ}(\delta)\), sweep the relative fiber class \(\ell_t\).
After applying \(\Psi_c\) and the orientation-preserving identification (1.5),
the resulting locally finite two-chain on the original complexified norm
cover is denoted

\[
\mathfrak C(\delta).
\tag{4.3}
\]

The side boundaries at \(v=0,1\) cancel under quadrant gluing. The two
\(\xi\)-ends lie on the divisor at infinity and hence give no boundary in
Borel--Moore homology. In a smooth compactification this is equivalently a
relative class

\[
\mathfrak C(\delta)
\in
H_2\left(
\overline{\widetilde{\mathcal S}_1^{\mathbb C}}\setminus D_q,
D_\infty;\mathbb C
\right),
\tag{4.4}
\]

where \(D_q=\{w=0\}\) and \(D_\infty\) is the surface divisor at infinity.

On one quadrant, (2.9) and (3.6) give the fiber pushforward. The four
oriented quadrants contribute with the same sign; calibration by the primary
real surface fixes the total factor. Consequently,

\[
\boxed{
(\pi_v)_!\mathcal K_c
=-4c(1-cv)\frac{dv}{W}
=\Omega_c.
}
\tag{4.5}
\]

Therefore every admissible boundary chain satisfies the chain-level identity

\[
\boxed{
\int_{\mathfrak C(\delta)}\mathcal K_c
=\int_\delta\Omega_c.
}
\tag{4.6}
\]

Taking \(\delta=\delta_-^\uparrow\) or
\(\delta_-^\downarrow\) proves (0.5).

---

## 5. Lateral and CPV surface cycles

Define the geometric lateral lifts

\[
\mathfrak C_-^\uparrow
=\mathfrak C(\delta_-^\uparrow),
\qquad
\mathfrak C_-^\downarrow
=\mathfrak C(\delta_-^\downarrow).
\tag{5.1}
\]

Stage 1 proved

\[
\Phi_-^*\omega_-=i\Omega_-.
\tag{5.2}
\]

Combining (4.6) and (5.2) gives

\[
\int_{\mathfrak C_-^\uparrow}\mathcal K
=-iI_{\rm dual,CPV}-4\pi,
\]

\[
\int_{\mathfrak C_-^\downarrow}\mathcal K
=-iI_{\rm dual,CPV}+4\pi.
\tag{5.3}
\]

The factor \(-i\) is the same Galois phase already isolated at the boundary
level. It is not a new surface ambiguity. Passing to complex coefficients as
in (0.6) gives the real-normalized lateral values (0.7).

The lateral difference is a surface meridian over \(P_\infty^-\):

\[
\int_{\mathfrak C_-^\uparrow-
\mathfrak C_-^\downarrow}\mathcal K=-8\pi,
\tag{5.4}
\]

and hence

\[
\int_{\Sigma_-^\uparrow-
\Sigma_-^\downarrow}\mathcal K=-8\pi i.
\tag{5.5}
\]

Their half-sum cancels the meridian and proves (0.9).

---

## 6. Convergence and Stokes justification

Fix a representative of either lateral boundary class that stays a positive
distance from \(P_\infty^-\). Its image in the compactified
\(v\)-curve is compact and avoids the two finite discriminants (3.4). Hence:

1. \(p\), \(p+b\), and the endpoint branches in (2.8) are uniformly
   nonzero along the representative;
2. the relative fiber class can be chosen continuously and away from
   \(Z=0\) and from the polar chart of \(\eta_c\);
3. the fiber integrand is uniformly \(O(|\xi|^{-3})d\xi\);
4. fiber integration and base integration may be interchanged;
5. the four angular side boundaries cancel pairwise.

For a direct Stokes proof, truncate the fiber at \(|\xi|=R\), retain a fixed
lateral indentation in the base, and apply (1.9). Equation (2.6) has limits

\[
\lim_{Q_+}\Psi_c^*\eta_c
=-\frac{\sqrt{ab}}{p\sqrt{p+b}}dt,
\]

\[
\lim_{Q_-}\Psi_c^*\eta_c
=+\frac{\sqrt{ab}}{p\sqrt{p+b}}dt.
\tag{6.1}
\]

The difference is (2.9). Dominated convergence applies as \(R\to\infty\).
The remaining base indentation is precisely the Stage-1 lateral contour, so
its meridian contribution is fixed by

\[
\operatorname{Res}_{P_\infty^-}(i\Omega_-)=4.
\tag{6.2}
\]

Thus the two lateral surface periods differ by \(8\pi i\) after dual
normalization, and their half-sum is the Cauchy-principal-value surface
period. No unrecorded polar boundary remains.

---

## 7. What has and has not been geometrized

The result gives three equivalent exact statements:

\[
I_{\rm dual,CPV}
=\int_{\Sigma_-^{\rm CPV}}\mathcal K,
\tag{7.1}
\]

\[
I_{\rm dual,CPV}
=\int_{\mathfrak C_-^{\rm CPV}}i\mathcal K,
\tag{7.2}
\]

\[
I_{\rm dual,CPV}
=\int_{\delta_-^{\rm CPV}}i\Omega_-.
\tag{7.3}
\]

Equation (7.1) is a genuine surface-period statement, but its cycle has
coefficients in \(\mathbb C\). Equation (7.2) uses an honest geometric
half-sum and the Galois-normalized curvature form. Neither is a real-region
integral.

The remaining canonicity question is narrower: determine the precise
Picard--Lefschetz transport from the primary integral cycle and decide whether
an integral relative class, possibly after adding a compact period cycle, can
replace the coefficient \(i\). The present theorem does not need that stronger
claim to realize and evaluate the dual surface period.

---

## 8. Completion ledger

```text
CLOSED       complexified norm double cover and algebraic curvature 2-form
CLOSED       exact hyperbolic fiber and meromorphic primitive
CLOSED       avoidance of q=0 along both dual lateral contours
CLOSED       four-quadrant angular gluing
CLOSED       fiber pushforward K_form -> Omega_-
CLOSED       two geometric lateral Borel-Moore surface chains
CLOSED       complex-coefficient lateral cycles with offsets +/-4*pi*i
CLOSED       CPV surface cycle and integral I_dual_CPV
OPEN         Picard-Lefschetz transport class modulo compact periods
OPEN         integral-coefficient replacement for the normalization by i
NOT CLAIMED  a second real or classically forbidden surface region
```
