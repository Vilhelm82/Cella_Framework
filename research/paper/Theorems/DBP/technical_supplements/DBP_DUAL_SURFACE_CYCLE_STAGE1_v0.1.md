# DBP Galois-Dual Surface-Cycle Route

## Stage 1: exact boundary cycle on the complexified metric link, v0.1

**Date:** 2026-07-14  
**Depends on:** `DBP_SURFACE_TO_LINK_CLOSEOFF_v1.0.md`,
`DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1.md`  
**Status:** the complexified link-to-dual-contour arrow is closed  
**Still open:** lifting this one-dimensional boundary chain through the
complexified noncompact surface to a two-dimensional relative/Borel--Moore
cycle

**Subsequent completion:** `DBP_DUAL_SURFACE_CYCLE_STAGE2_v0.1.md` constructs
that surface lift. The open statement above records the boundary at the time
of this Stage-1 theorem.

---

## 0. Result

The Galois-dual constant already has an exact geometric **boundary chain**.
It is not a real arc of the spherical link. It is a lateral relative chain on
the compactified metric quotient of the complexified link, passing one of the
two points at infinity.

At the keystone put

\[
m_\pm=\frac{2\mp\sqrt2}{4},\qquad
c_\pm=\frac{m_\pm}{1-m_\pm}=3\mp2\sqrt2,
\]

and, for either channel,

\[
h=1-c^2,\qquad
n=-\frac{c^2}{h}=-\frac{m^2}{1-2m}.
\tag{0.1}
\]

The metric quotient of the complexified spherical link is the elliptic
quartic

\[
\mathcal B_m:\qquad
W^2=c\,v(1-v)(1-cv)(1-c^2v),
\tag{0.2}
\]

with boundary differential

\[
\Omega_m=-4c(1-cv)\frac{dv}{W}.
\tag{0.3}
\]

There is an explicit isomorphism of the smooth compactifications

\[
\Phi_m:\mathcal B_m\longrightarrow
C_m:\ y^2=x(x-1)(x-m)
\tag{0.4}
\]

given by

\[
x=\frac{mhv}{1-c^2v},\qquad
y=\frac{m\sqrt{h/c}}{(1-c^2v)^2}W.
\tag{0.5}
\]

For the primary branch, \(\Phi_{m_+}^*\omega_+=\Omega_{m_+}\). For the
dual branch, choose

\[
\sqrt{h_-/c_-}=+i\sqrt{(c_-^2-1)/c_-}.
\tag{0.6}
\]

Then the exact phase relation is

\[
\boxed{\Phi_{m_-}^*\omega_-=i\Omega_{m_-}.}
\tag{0.7}
\]

The upper-sheet pole of \(\omega_-\) is the image of

\[
P_\infty^-:\qquad \frac{W}{v^2}\longrightarrow-i c_-^2,
\tag{0.8}
\]

and

\[
\operatorname{Res}_{P_\infty^-}(i\Omega_{m_-})=4.
\tag{0.9}
\]

Let \(\delta_-^\uparrow\) and \(\delta_-^\downarrow\) be the inverse images
of the upper- and lower-indented Legendre paths. These are honest lateral
relative one-cycles on \(\mathcal B_{m_-}\). With the orientation conventions
fixed in Section 5,

\[
\int_{\delta_-^\uparrow}i\Omega_{m_-}
=I_{\rm dual,CPV}-4\pi i,
\qquad
\int_{\delta_-^\downarrow}i\Omega_{m_-}
=I_{\rm dual,CPV}+4\pi i.
\tag{0.10}
\]

Consequently the rational relative chain

\[
\boxed{
\delta_-^{\rm CPV}
=\frac12\left(\delta_-^\uparrow+\delta_-^\downarrow\right)
}
\tag{0.11}
\]

satisfies

\[
\boxed{
\int_{\delta_-^{\rm CPV}}i\Omega_{m_-}=I_{\rm dual,CPV}.
}
\tag{0.12}
\]

This is the required one-dimensional input for the surface lift. It does not
yet assert that \(\delta_-^{\rm CPV}\) bounds a canonical complex surface
chain carrying the curvature two-form.

---

## 1. From the spherical link to the metric quartic

Write the diagonalized asymptotic link using the squared semi-axes

\[
A=m,\qquad C=c=\frac{m}{1-m}.
\tag{1.1}
\]

The parameter relation from the shear family becomes

\[
\nu=\frac{A-C}{1-A}
=-\frac{m^2}{(1-m)^2}
=-c^2.
\tag{1.2}
\]

On one quadrant put \(v=\sin^2t\). The complexified link can be written
locally as

\[
X^2=m(1-v),\qquad Z^2=cv,
\qquad Y^2=1-m(1-v)-cv.
\tag{1.3}
\]

The algebraic continuation of the squared arc-speed is

\[
\left(\frac{ds}{dt}\right)^2
=\frac{c-c^2v}{1-c^2v}
=\frac{c(1-cv)}{1-c^2v}.
\tag{1.4}
\]

Since

\[
dt=\frac{dv}{2\sqrt{v(1-v)}},
\]

adjoining the metric square root and quotienting by the four quadrant
symmetries gives (0.2). On the real primary branch, \(0<c_+<1\), take
\(W>0\) over \(0<v<1\). One quadrant contributes

\[
\frac12c(1-cv)\frac{dv}{W}.
\tag{1.5}
\]

Four quadrants and the two oriented cone ends therefore give

\[
L(\Gamma_1^+)=2\int_0^1c(1-cv)\frac{dv}{W},
\]

\[
\int_{S_1}K_G\,dA=-2L(\Gamma_1^+)
=\int_{\delta_+}\Omega_{m_+},
\tag{1.6}
\]

where \(\delta_+\) is the lift of \(v:0\to1\) with \(W>0\). Thus
\(\Omega_m\) is the exact boundary differential inherited from the proved
surface-to-link formula, with all quadrant and end multiplicities included.

The distinction between the complexified link and (0.2) matters: (0.2) is its
**metric elliptic quotient**. It includes the square root needed by arc length
and is the correct one-dimensional object for the period map.

---

## 2. Exact map to the Legendre cubic

Set

\[
d=1-c^2v.
\tag{2.1}
\]

Under (0.5), direct factorization gives

\[
x=\frac{mhv}{d},\qquad
x-m=\frac{m(v-1)}d,
\qquad
x-1=\frac{cv-1}d.
\tag{2.2}
\]

Hence

\[
x(x-1)(x-m)
=\frac{m^2h}{cd^4}
\left[c\,v(1-v)(1-cv)(1-c^2v)\right]
=y^2.
\tag{2.3}
\]

The inverse coordinate is

\[
v=\frac{x}{mh+c^2x}.
\tag{2.4}
\]

Thus (0.5) is birational with a birational inverse and extends to an
isomorphism of the nonsingular compactifications.

The characteristic in (0.1) is exactly the Booth/Landen characteristic.
Indeed, because \(n=-c^2/h\),

\[
\frac{m}{m-nx}=1-c^2v=d,
\tag{2.5}
\]

and therefore

\[
\frac{m}{m-nx}-(1-c)=c(1-cv).
\tag{2.6}
\]

Differentiating (0.5) gives

\[
\frac{dx}{y}=\sqrt{ch}\,\frac{dv}{W}.
\tag{2.7}
\]

Equations (2.6)--(2.7) prove the differential identity

\[
\boxed{
\Omega_m
=\Phi_m^*\left[
-\frac4{\sqrt{ch}}
\left(\frac{m}{m-nx}-(1-c)\right)\frac{dx}{y}
\right].
}
\tag{2.8}
\]

This is the chain-level link-to-Legendre map that was absent from the earlier
scalar close-off.

---

## 3. Keystone normalization and the Galois phase

Let \(t=2^{1/4}>0\). For the primary channel,

\[
c_+=3-2\sqrt2,\qquad h_+>0,
\]

and the exact normalization is

\[
\frac{8c_+}{\sqrt{c_+h_+}}=t^7.
\tag{3.1}
\]

Since

\[
A_+=\frac1{c_+},\qquad
B_+=\frac{1-c_+}{c_+},
\tag{3.2}
\]

equation (2.8) is precisely

\[
\Phi_{m_+}^*\omega_+=\Omega_{m_+}.
\tag{3.3}
\]

Galois conjugation sends

\[
m_+\mapsto m_-=1-m_+,qquad
c_+\mapsto c_-=\frac1{c_+},
\qquad n_+\mapsto n_-=1-n_+.
\tag{3.4}
\]

Now \(c_->1\) and \(h_-=1-c_-^2<0\). With the branch (0.6),

\[
\frac4{\sqrt{c_-(c_-^2-1)}}=\frac{t^7}{2c_-},
\tag{3.5}
\]

so (2.8) becomes

\[
\Omega_{m_-}=-i\,\Phi_{m_-}^*\omega_-.
\tag{3.6}
\]

Multiplication by \(i\) is therefore not an inserted numerical convention.
It is the exact phase required to turn the analytically continued metric
differential into the real-normalized dual third-kind differential.

---

## 4. The dual contour on the metric quartic

On the dual Legendre cubic let \(\gamma_-\) be the upper real path

\[
x:0\longrightarrow m_-,\qquad y>0.
\tag{4.1}
\]

The pole lies at

\[
x_p=\frac{m_-}{n_-},
\qquad 0<x_p<m_-.
\tag{4.2}
\]

By (2.4),

\[
v(x)=\frac{x}{m_-h_-+c_-^2x}.
\tag{4.3}
\]

The denominator vanishes exactly at \(x=x_p\), because

\[
x_p=-\frac{m_-h_-}{c_-^2}.
\tag{4.4}
\]

Furthermore,

\[
v(0)=0,qquad v(m_-)=1,
\tag{4.5}
\]

and along the real path

\[
x:0\to x_p^-\quad\Longleftrightarrow\quad v:0\to-\infty,
\]

\[
x:x_p^+\to m_-\quad\Longleftrightarrow\quad v:+\infty\to1.
\tag{4.6}
\]

Thus the dual boundary contour is explicit:

```text
v = 0  --->  -infinity  --->  P_infinity^-  --->  +infinity  --->  v = 1.
```

The two choices of side around \(P_\infty^-\) are
\(\delta_-^\uparrow\) and \(\delta_-^\downarrow\). They avoid the finite
quartic branch points

\[
v=\frac1{c_-^2},\qquad v=\frac1{c_-},
\tag{4.7}
\]

which explains why no real segment of the dual spherical link can represent
the path: both of those branch points lie in \((0,1)\), while the correct
relative chain runs through the negative real direction and infinity.

An upper indentation in the \(x\)-plane maps to the lower passage around
infinity in the \(v\)-sphere, and a lower indentation maps to the upper
passage. This follows from

\[
v\sim\frac{x_p}{c_-^2(x-x_p)}.
\tag{4.8}
\]

---

## 5. Residue, lateral values, and the CPV chain

The quartic has two points at infinity,

\[
P_\infty^\pm:\qquad
\frac{W}{v^2}\longrightarrow\pm i c_-^2.
\tag{5.1}
\]

Using the local coordinate \(\tau=1/v\), equation (0.3) gives

\[
\operatorname{Res}_{P_\infty^+}(i\Omega_{m_-})=-4,
\qquad
\operatorname{Res}_{P_\infty^-}(i\Omega_{m_-})=+4.
\tag{5.2}
\]

With the square-root choice (0.6), \(P_\infty^-\) maps to the pole on the
upper Legendre sheet. Therefore the source residue agrees, including sign,
with the certified weighted residue of \(\omega_-\).

Let \(\gamma_-^\uparrow\) bypass \(x_p\) by a small upper semicircle and
\(\gamma_-^\downarrow\) by a small lower semicircle, both oriented from
\(0\) to \(m_-\). Since the upper semicircle is clockwise,

\[
\int_{\gamma_-^\uparrow}\omega_-
=I_{\rm dual,CPV}-i\pi(4),
\]

\[
\int_{\gamma_-^\downarrow}\omega_-
=I_{\rm dual,CPV}+i\pi(4).
\tag{5.3}
\]

Pulling back by \(\Phi_{m_-}\) and using (0.7) proves (0.10)--(0.12). It also
gives

\[
\int_{\delta_-^\uparrow-\delta_-^\downarrow}i\Omega_{m_-}
=-8\pi i.
\tag{5.4}
\]

Reversing the naming of the two lateral sides reverses the sign in (5.4), but
not its magnitude or the CPV half-sum.

---

## 6. Homological meaning and present limit

Let \(D_\infty=P_\infty^++P_\infty^-\). The lateral chains naturally live
in relative homology

\[
H_1\bigl(\overline{\mathcal B}_{m_-}\setminus D_\infty,
\{v=0,v=1\};\mathbb Z\bigr).
\tag{6.1}
\]

Each lateral chain is integral. The CPV object is their half-sum and therefore
belongs canonically to the same relative group with \(\mathbb Q\)-coefficients.
Their difference is a meridian of \(P_\infty^-\), detected by the residue
pairing (5.4).

This construction removes the first ambiguity in the surface-cycle program:
the dual contour is now known explicitly on the geometric boundary curve. It
does **not** yet settle which Gauss--Manin transport from the primary real
cycle should be preferred. Branch-loop transports around \(s=+i\) and
\(s=-i\) are the natural candidates for the two lateral classes, but their
possible additions by ordinary periods still require a Picard--Lefschetz
calculation. The CPV half-sum removes the local residue ambiguity, not every
possible global period ambiguity.

For that reason the theorem proved here is a boundary-cycle theorem, not yet a
canonicity theorem for a two-dimensional surface cycle.

---

## 7. Exact input supplied to Stage 2

The next stage is now sharply specified. Complexify the diagonal surface and
the norm square:

\[
\mathcal S^\mathbb C:\quad ax^2-by^2+z^2=3,
\]

\[
\widetilde{\mathcal S}^\mathbb C:\quad
ax^2-by^2+z^2=3,
\qquad w^2=q=4(a^2x^2+b^2y^2+z^2).
\tag{7.1}
\]

The algebraic primitive from the primary close-off,

\[
\eta=-\frac{2ab\,y}{w(a^2x^2+z^2)}(x\,dz-z\,dx),
\qquad d\eta=K_G\,dA,
\tag{7.2}
\]

already extends meromorphically to this double cover. Stage 2 must construct
two lateral relative two-chains \(\Sigma_-^\uparrow,\Sigma_-^\downarrow\)
such that:

1. their oriented end boundaries reduce to the chains
   \(\delta_-^\uparrow,\delta_-^\downarrow\) above;
2. they avoid the polar divisor of \(\eta\) except for the prescribed lateral
   passage;
3. Stokes' theorem is valid after end truncation and indentation;
4. their half-sum has integral \(I_{\rm dual,CPV}\);
5. their difference is the surface meridian whose boundary residue is
   \(8\pi i\).

The central new problem is therefore no longer finding the dual contour. It is
proving that this exact contour admits a convergent, geometrically controlled
lift through the complexified noncompact fiber.

That problem is completed in `DBP_DUAL_SURFACE_CYCLE_STAGE2_v0.1.md`: the
hyperbolic fiber is transported on the norm double cover, the four angular
quadrants are glued, and the resulting lateral and CPV surface periods are
evaluated exactly.

---

## 8. Completion ledger

```text
CLOSED       complexified link metric quotient B_m
CLOSED       exact isomorphism B_m -> C_m
CLOSED       primary normalization Phi_+^* omega_+ = Omega_+
CLOSED       dual phase Phi_-^* omega_- = i Omega_-
CLOSED       pole = P_infinity^- and residue +4
CLOSED       two lateral dual boundary cycles
CLOSED       CPV as their rational half-sum
OPEN         canonical Gauss-Manin class modulo ordinary periods
CLOSED LATER lift to a relative/Borel-Moore surface two-cycle
CLOSED LATER convergence and Stokes theorem for that lift
```
